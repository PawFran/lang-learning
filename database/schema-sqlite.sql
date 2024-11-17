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
	"external_word_id"	INTEGER NOT NULL,
	"part_of_speech"	TEXT NOT NULL,
	FOREIGN KEY("part_of_speech") REFERENCES "parts_of_speech"("name"),
	FOREIGN KEY ("lang") REFERENCES "languages"("name"),
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("lang", "external_word_id", "part_of_speech")
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
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("base_word_acc", "infinite_acc", "perfect_acc", "supine_acc"),
	FOREIGN KEY("conjugation") REFERENCES "latin_conjugations"("name")
);
CREATE TABLE IF NOT EXISTS "latin_translations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"text"	TEXT NOT NULL UNIQUE,
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
	UNIQUE("base_acc", "gen_acc"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "latin_words_translations_mapping" (
    "id" INTEGER NOT NULL UNIQUE,
	"word_id"	INTEGER,
	"translation_id"	INTEGER,
	"part_of_speech"	TEXT,
	PRIMARY KEY("id", AUTOINCREMENT),
	UNIQUE("word_id", "translation_id", "part_of_speech"),
	FOREIGN KEY("word_id") REFERENCES "words"("word_id"),
    FOREIGN KEY("translation_id") REFERENCES "latin_translations"("id"),
    FOREIGN KEY("part_of_speech") REFERENCES "parts_of_speech"("name")
);
CREATE TABLE IF NOT EXISTS "latin_adverbs" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "latin_prepositions" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "latin_conjunctions" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "latin_pronouns" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "latin_adjectives" (
	"id"	INTEGER,
	"base"	TEXT NOT NULL,
	"base_acc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
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

-- ### VIEWS ###
-- TODO fix joins: word_id it not enough, words table must be joined as well and external_word_id must be added
CREATE VIEW nouns_with_translations as
SELECT base_acc, gen_acc, text, example from latin_nouns n
	join latin_words_translations_mapping m on n.id = m.word_id
	join latin_translations t on t.id = m.translation_id
order by text
/* nouns_with_translations(base_acc,gen_acc,text,example) */;

CREATE VIEW verbs_with_translations as
SELECT base_word_acc, infinite_acc, perfect_acc, supine_acc, conjugation, text, example from latin_verbs v
	join latin_words_translations_mapping m on v.id = m.word_id
	join latin_translations t on t.id = m.translation_id
order by text
/* verbs_with_translations(base_word_acc,infinite_acc,perfect_acc,supine_acc,conjugation,text,example) */;

CREATE VIEW view_translation_last_correct as SELECT word_pl, max(datetime(time)) as last_correct from translation_results where is_correct = "True" group by word_pl order by last_correct desc
/* view_translation_last_correct(word_pl,last_correct) */;

CREATE VIEW view_translation_correct_ratio as
select * from
	(select word_pl, correct_translation, sum(correct) as correct, count(*) - sum(correct) as incorrect, round(sum(correct) / cast(count(*) as REAL) * 100, 0) as "correct %" FROM
		(SELECT *,
			CASE WHEN LOWER(is_correct) = 'true' THEN 1 ELSE 0 END AS correct
		from translation_results)
	group by word_pl)
order by "correct %" asc, incorrect desc, correct asc
/* view_translation_correct_ratio(word_pl,correct_translation,correct,incorrect,"correct %") */;

CREATE VIEW view_translation_results as
select ratio.word_pl, correct_translation, correct, incorrect, "correct %", last_correct
from view_translation_correct_ratio ratio
left join view_translation_last_correct last
on last.word_pl = ratio.word_pl
/* view_translation_results(word_pl,correct_translation,correct,incorrect,"correct %",last_correct) */;
