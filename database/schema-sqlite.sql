CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "latin_conjugations" (
	"name"	TEXT NOT NULL UNIQUE,
	UNIQUE("name"),
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "latin_declensions" (
	"name"	TEXT NOT NULL UNIQUE,
	UNIQUE("name"),
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "languages" (
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "parts_of_speech" (
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "words" (
    "id"	INTEGER NOT NULL UNIQUE,
	"lang"	TEXT NOT NULL,
	"header"	TEXT NOT NULL,
	"part_of_speech"	TEXT NOT NULL,
	FOREIGN KEY("part_of_speech") REFERENCES "parts_of_speech"("name"),
	FOREIGN KEY ("lang") REFERENCES "languages"("name"),
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("lang", "header", "part_of_speech")
);
CREATE TABLE IF NOT EXISTS "latin_verbs" (
	"id"	INTEGER NOT NULL,
	"base_word"	TEXT NOT NULL,
	"base_word_acc"	TEXT NOT NULL,
	"infinite"	TEXT NOT NULL,
	"infinite_acc"	TEXT NOT NULL,
	"perfect"	TEXT NOT NULL,
	"perfect_acc"	TEXT NOT NULL,
	"supine"	TEXT,
	"supine_acc"	TEXT,
	"additional_info"	TEXT,
	"conjugation"	TEXT NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("base_word_acc", "infinite_acc", "perfect_acc", "supine_acc"),
	FOREIGN KEY("id") REFERENCES "words"("id"),
	FOREIGN KEY("conjugation") REFERENCES "latin_conjugations"("name")
);
CREATE TABLE IF NOT EXISTS "translations_from_latin" (
	"id"	INTEGER NOT NULL UNIQUE,
	"translation"	TEXT NOT NULL UNIQUE,
	"example"	TEXT,
	"associated_case"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "genres" (
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "latin_nouns" (
	"id"	INTEGER NOT NULL UNIQUE,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL,
	"gen"	TEXT NOT NULL,
	"gen_acc"	TEXT NOT NULL,
	"declension"	TEXT NOT NULL,
	"genre"	TEXT NOT NULL,
	"only_pl"	TEXT NOT NULL,
	FOREIGN KEY("genre") REFERENCES "genres"("name"),
	FOREIGN KEY("declension") REFERENCES "latin_declensions"("name"),
	FOREIGN KEY("id") REFERENCES "words"("id"),
	UNIQUE("base_acc", "gen_acc"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "latin_words_translations_mappings" (
    "id" INTEGER NOT NULL UNIQUE,
	"word_id"	INTEGER,
	"translation_id"	INTEGER,
	"part_of_speech"	TEXT,
	PRIMARY KEY("id", AUTOINCREMENT),
	UNIQUE("word_id", "translation_id", "part_of_speech"),
	FOREIGN KEY("word_id") REFERENCES "words"("id"),
    FOREIGN KEY("translation_id") REFERENCES "translations_from_latin"("id"),
    FOREIGN KEY("part_of_speech") REFERENCES "parts_of_speech"("name")
);
CREATE TABLE IF NOT EXISTS "latin_adverbs" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("id") REFERENCES "words"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "latin_prepositions" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("id") REFERENCES "words"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "latin_conjunctions" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("id") REFERENCES "words"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "latin_pronouns" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("id") REFERENCES "words"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "latin_adjectives" (
	"id"	INTEGER,
	"masculinum"	TEXT NOT NULL,
	"masculinum_acc"	TEXT NOT NULL,
	"femininum"	TEXT NOT NULL,
	"femininum_acc"	TEXT NOT NULL,
	"neutrum"	TEXT NOT NULL,
	"neutrum_acc"	TEXT NOT NULL,
	FOREIGN KEY("id") REFERENCES "words"("id"),
    UNIQUE("masculinum_acc", "femininum_acc", "neutrum_acc"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "translation_results" (
	"id"	INTEGER,
	"user"	TEXT NOT NULL,
	"session_id"	INTEGER NOT NULL,
	"lang"	TEXT NOT NULL,
	"word_pl"	TEXT NOT NULL,
	"correct_translation"	TEXT NOT NULL,
	"user_answer"	TEXT NOT NULL,
	"is_correct"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

--CREATE TABLE IF NOT EXISTS "translation_results" (
--	"id"	INTEGER,
--	"user"	TEXT NOT NULL,
--	"session_id"	INTEGER NOT NULL,
--	"from_lang"	TEXT NOT NULL,
--	"to_lang"	TEXT NOT NULL,
--	"from_word"	TEXT NOT NULL,
--	"to_word"	TEXT NOT NULL,
--	"user_answer"	TEXT NOT NULL,
--	"time"	TEXT NOT NULL,
--	PRIMARY KEY("id" AUTOINCREMENT)
--);
