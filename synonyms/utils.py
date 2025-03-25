import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from environment import engine

# Add the parent directory to sys.path to import from database
# sys.path.append(str(Path.cwd().parent))

from database.db_classes import Translations

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
import numpy as np

Session = sessionmaker(bind=engine)


def get_all_translations() -> list[Translations]:
    """
    Retrieve all translations from the database using the Translations class.
    
    Returns:
        list: A list of all translation records from the database
    """
    session = Session()
    try:
        translations = session.query(Translations).all()
        return translations
    except Exception as e:
        print(f"Error retrieving translations: {e}")
        return []
    finally:
        session.close()


def translation_to_documents(translations: list[Translations]) -> list[Document]:
    translation_docs = []
    for translation in translations:
        doc = Document(
            page_content=translation.translation
        )
        translation_docs.append(doc)
    
    return translation_docs


class SynonymFinder:

    def __init__(self):
        self.translation_docs: list[Document] = translation_to_documents(get_all_translations())
        self.embeddings = OpenAIEmbeddings()
        self.doc_embeddings = self.embeddings.embed_documents([doc.page_content for doc in self.translation_docs])


    def get_relevant_documents(self, query: str, n: int, documents: list, open_AI_embeddings: OpenAIEmbeddings, doc_embeddings: list) -> list:
        """
        Find the N most relevant documents for a given query word using LangChain embeddings and cosine similarity.

        Args:
            query (str): The input word to find similar documents for
            n (int): Number of relevant documents to return
            documents (list): List of Document objects to search through

        Returns:
            list: The N most relevant Document objects sorted by similarity
        """

        # Get embeddings for query and documents
        query_embedding = open_AI_embeddings.embed_query(query)

        # Calculate cosine similarities
        similarities = []
        for i, doc_embedding in enumerate(doc_embeddings):
            similarity = np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            similarities.append((similarity, i))

        # Sort by similarity and get top N
        similarities.sort(reverse=True)
        top_n_indices = [idx for _, idx in similarities[:n]]

        # Return the most relevant documents
        return [documents[idx] for idx in top_n_indices]

    def similar_translations(self, query: str, n: int = 3) -> list[str]:
        relevant_docs = self.get_relevant_documents(
            query, 
            n=n, 
            documents=self.translation_docs, 
            open_AI_embeddings=self.embeddings, 
            doc_embeddings=self.doc_embeddings
            )

        return [doc.page_content for doc in relevant_docs]
