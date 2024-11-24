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
CREATE TABLE IF NOT EXISTS "latin_translations" (
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
    FOREIGN KEY("translation_id") REFERENCES "latin_translations"("id"),
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

 ### VIEWS ###
create view words_with_translations as
select header, w.part_of_speech, translation, example, associated_case from words w
join latin_words_translations_mappings m on w.id = m.word_id
join latin_translations t on t.id = m.translation_id

CREATE VIEW translation_last_asked as
select word_pl, max(datetime(time)) as last_asked
from translation_results
group by word_pl
order by last_asked desc

CREATE VIEW translation_correct_ratio as
select * from
	(select word_pl, correct_translation, sum(correct) as correct, count(*) - sum(correct) as incorrect, round(sum(correct) / cast(count(*) as REAL) * 100, 0) as "correct %" FROM
		(SELECT *,
			CASE WHEN LOWER(is_correct) = 'true' THEN 1 ELSE 0 END AS correct
		from translation_results)
	group by word_pl)
order by "correct %" asc, incorrect desc, correct asc

create view next_to_be_asked as
select ratio.word_pl, correct_translation, last_asked, correct, incorrect, "correct %", ratio.idx as correct_idx, last_asked.idx as time_idx, ratio.idx + last_asked.idx as sum_idx
from (
	select *, ROW_NUMBER() over (order by last_asked asc) as idx
	from translation_last_asked
	) last_asked
join (
	select *, ROW_NUMBER() over (order by "correct %" asc, incorrect desc, correct asc) as idx
	from translation_correct_ratio
	) ratio
on last_asked.word_pl = ratio.word_pl
order by sum_idx asc

--CREATE VIEW nouns_with_translations as
--select base_acc, gen_acc, text, example
--    from latin_nouns n
--	join words w on n.id = w.external_word_id
--	join latin_words_translations_mapping m on w.id = m.word_id
--	join latin_translations t on m.translation_id = t.id
--
--CREATE VIEW verbs_with_translations as
--select base_word_acc, infinite_acc, perfect_acc, supine_acc, conjugation, text, example from latin_verbs v
--join words w on v.id = w.id
--join latin_words_translations_mappings m on w.id = m.word_id
--join latin_translations t on t.id = m.translation_id

-- why it's empty ?
--CREATE VIEW words_with_translations as
--select * from words w
--join latin_adjectives adj on adj.id = w.id
--join latin_adverbs adv on adv.id = w.id
--join latin_conjunctions c on c.id = w.id
--join latin_nouns n on n.id = w.id
--join latin_prepositions prep on prep.id = w.id
--join latin_pronouns pron on pron.id = w.id
--join latin_verbs v on v.id = w.id
--join latin_words_translations_mappings m on w.id = m.word_id
--join latin_translations t on t.id = m.translation_id
--
--CREATE VIEW translation_last_correct as
--SELECT word_pl, max(datetime(time)) as last_correct
--from translation_results
--where is_correct = "True"
--group by word_pl
--order by last_correct desc
--
--
--CREATE VIEW translation_statistics as
--select ratio.word_pl, correct_translation, correct, incorrect, "correct %", last_correct
--from translation_correct_ratio ratio
--left join translation_last_correct last
--on last.word_pl = ratio.word_pl
