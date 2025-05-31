from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from environment import engine

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
import numpy as np

from vocabulary.lib.dict_classes import PartOfSpeech

Session = sessionmaker(bind=engine)


@dataclass
class TranslationWithPartOfSpeech:
    translation: str
    part_of_speech: str


@dataclass
class DocumentWithScore:
    document: Document
    score: float


@dataclass
class SynonymWithScore:
    synonym: str
    score: float


def get_all_translations() -> list[TranslationWithPartOfSpeech]:
    """
    Retrieve all translations from the database using the Translations class.

    Returns:
        list: A list of all translation records from the database
    """
    session = Session()
    try:
        # Use SQLAlchemy ORM objects instead of raw SQL
        from database.db_classes import Words, LatinWordsTranslationsMappings, Translations

        translations_raw = (
            session.query(
                Translations.translation,
                Words.part_of_speech,
            )
            .join(LatinWordsTranslationsMappings, Words.id == LatinWordsTranslationsMappings.word_id)
            .join(Translations, LatinWordsTranslationsMappings.translation_id == Translations.id)
            .filter(Words.lang == 'latin')
            .all()
        )
        translations = [TranslationWithPartOfSpeech(translation=x[0], part_of_speech=x[1]) for x in translations_raw]
        return translations
    except Exception as e:
        print(f"Error retrieving translations: {e}")
        return []
    finally:
        session.close()


def translation_to_documents(translations: list[TranslationWithPartOfSpeech]) -> list[Document]:
    translation_docs = []
    for translation in translations:
        doc = Document(
            page_content=translation.translation,
            metadata={"part_of_speech": translation.part_of_speech}
        )
        translation_docs.append(doc)

    return translation_docs


class SynonymFinder:

    def __init__(self):
        self.translation_docs: list[Document] = translation_to_documents(get_all_translations())
        self.embeddings = OpenAIEmbeddings()
        self.doc_embeddings = self.embeddings.embed_documents([doc.page_content for doc in self.translation_docs])

    def cosine_similarities(self, query_embedding: list[float]) -> list[(float, int)]:
        similarities = []
        for i, doc_embedding in enumerate(self.doc_embeddings):
            similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            similarities.append((similarity, i))

        return similarities

    def get_similar_documents(self, query: str, documents: list,
                              part_of_speech: PartOfSpeech = None) -> list[DocumentWithScore]:
        """
        Find the N most relevant documents for a given query word using LangChain embeddings and cosine similarity.

        Args:
            query (str): The input word to find similar documents for
            documents (list): List of Document objects to search through
            part_of_speech (PartOfSpeech): Optional parameter to filter by part of speech

        Returns:
            list: The N most relevant Document objects sorted by similarity
        """

        # Get embeddings for query and documents
        query_embedding = self.embeddings.embed_query(query)

        similarities = sorted(self.cosine_similarities(query_embedding), reverse=True)

        docs_with_scores: list[DocumentWithScore] = [DocumentWithScore(documents[idx], similarity_score) for
                                                     similarity_score, idx in similarities]

        return docs_with_scores

    def similar_translations(self, query: str, n: int = 3, part_of_speech: PartOfSpeech = None) -> list[
        SynonymWithScore]:
        queried_docs: list[DocumentWithScore] = self.get_similar_documents(
            query,
            documents=self.translation_docs
        )

        if part_of_speech is not None:
            relevant_docs = [x for x in queried_docs if x.document.metadata['part_of_speech'] == part_of_speech.value]
        else:
            relevant_docs = queried_docs

        return [SynonymWithScore(doc.document.page_content, doc.score) for doc in relevant_docs[:n]]
