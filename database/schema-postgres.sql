-- Your database schema. Use the Schema Designer at http://localhost:8001/ to add some tables.
-- Your database schema adapted for PostgreSQL

CREATE TABLE latin_conjugations (
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (name)
);

CREATE TABLE latin_declensions (
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (name)
);

CREATE TABLE languages (
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (name)
);

CREATE TABLE parts_of_speech (
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (name)
);

CREATE TABLE words (
    lang TEXT NOT NULL,
    word_id INTEGER NOT NULL,
    part_of_speech TEXT NOT NULL,
    FOREIGN KEY (part_of_speech) REFERENCES parts_of_speech (name),
    PRIMARY KEY (lang, word_id, part_of_speech)
);

CREATE TABLE latin_verbs (
    id SERIAL PRIMARY KEY,
    base_word TEXT NOT NULL,
    base_word_acc TEXT NOT NULL,
    infinite TEXT NOT NULL,
    infinite_acc TEXT NOT NULL,
    perfect TEXT NOT NULL,
    perfect_acc TEXT NOT NULL,
    supine TEXT,
    supine_acc TEXT,
    additional_info TEXT,
    conjugation TEXT NOT NULL,
    UNIQUE (base_word_acc, infinite_acc, perfect_acc, supine_acc),
    FOREIGN KEY (conjugation) REFERENCES latin_conjugations (name)
);

CREATE TABLE latin_translations (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL UNIQUE,
    example TEXT,
    associated_case TEXT
);

CREATE TABLE genres (
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (name)
);

CREATE TABLE latin_nouns (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL,
    gen TEXT NOT NULL,
    gen_acc TEXT NOT NULL,
    declension TEXT NOT NULL,
    genre TEXT NOT NULL,
    only_pl BOOLEAN NOT NULL,
    FOREIGN KEY (genre) REFERENCES genres (name),
    FOREIGN KEY (declension) REFERENCES latin_declensions (name),
    UNIQUE (base_acc, gen_acc)
);

CREATE TABLE latin_words_translations_mapping (
    word_id INTEGER,
    translation_id INTEGER,
    part_of_speech TEXT,
    FOREIGN KEY (part_of_speech) REFERENCES parts_of_speech (name),
    PRIMARY KEY (word_id, translation_id, part_of_speech)
);

CREATE TABLE latin_adverbs (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL UNIQUE
);

CREATE TABLE latin_prepositions (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL UNIQUE
);

CREATE TABLE latin_conjunctions (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL UNIQUE
);

CREATE TABLE latin_pronouns (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL UNIQUE
);

CREATE TABLE latin_adjectives (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,
    base_acc TEXT NOT NULL UNIQUE
);

-- Changed TEXT to BOOLEAN for PostgreSQL
-- Use TIMESTAMP for date-time storage in PostgreSQL
CREATE TABLE translation_results (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    session_id INTEGER NOT NULL UNIQUE,
    lang TEXT NOT NULL,
    word_pl TEXT NOT NULL,
    correct_translation TEXT NOT NULL,
    user_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL, 
    answer_time TIMESTAMP NOT NULL,
    FOREIGN KEY (lang) REFERENCES languages (name) 
);

-- Views for PostgreSQL
-- CREATE VIEW nouns_with_translations AS
-- SELECT base_acc, gen_acc, text, example 
-- FROM latin_nouns n
-- JOIN latin_words_translations_mapping m ON n.id = m.word_id
-- JOIN latin_translations t ON t.id = m.translation_id
-- ORDER BY text;

-- CREATE VIEW verbs_with_translations AS
-- SELECT base_word_acc, infinite_acc, perfect_acc, supine_acc, conjugation, text, example 
-- FROM latin_verbs v
-- JOIN latin_words_translations_mapping m ON v.id = m.word_id
-- JOIN latin_translations t ON t.id = m.translation_id
-- ORDER BY text;

-- CREATE VIEW view_translation_last_correct AS 
-- SELECT word_pl, MAX(time) AS last_correct 
-- FROM translation_results 
-- WHERE is_correct = TRUE 
-- GROUP BY word_pl 
-- ORDER BY last_correct DESC;

-- CREATE VIEW view_translation_correct_ratio AS 
-- SELECT word_pl, correct_translation, SUM(correct) AS correct, COUNT(*) - SUM(correct) AS incorrect, 
--     ROUND(SUM(correct)::DECIMAL / COUNT(*) * 100) AS "correct %" 
-- FROM (
--     SELECT *,
--         CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END AS correct
--     FROM translation_results
-- ) AS subquery
-- GROUP BY word_pl, correct_translation
-- ORDER BY "correct %" ASC, incorrect DESC, correct ASC;

-- CREATE VIEW view_translation_results AS
-- SELECT ratio.word_pl, correct_translation, correct, incorrect, "correct %", last_correct
-- FROM view_translation_correct_ratio ratio
-- LEFT JOIN view_translation_last_correct last
-- ON last.word_pl = ratio.word_pl;