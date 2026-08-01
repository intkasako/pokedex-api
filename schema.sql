CREATE TABLE IF NOT EXISTS types(
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL
);

INSERT INTO types (name_) VALUES ('Normal'); --1
INSERT INTO types (name_) VALUES ('Fire'); --2
INSERT INTO types (name_) VALUES ('Water'); --3
INSERT INTO types (name_) VALUES ('Electric'); --4
INSERT INTO types (name_) VALUES ('Grass'); --5
INSERT INTO types (name_) VALUES ('Ice'); --6
INSERT INTO types (name_) VALUES ('Fighting'); --7
INSERT INTO types (name_) VALUES ('Poison'); --8
INSERT INTO types (name_) VALUES ('Ground'); --9
INSERT INTO types (name_) VALUES ('Flying'); --10
INSERT INTO types (name_) VALUES ('Psychic'); --11
INSERT INTO types (name_) VALUES ('Bug'); --12
INSERT INTO types (name_) VALUES ('Rock'); --13
INSERT INTO types (name_) VALUES ('Ghost'); --14
INSERT INTO types (name_) VALUES ('Dragon'); --15
INSERT INTO types (name_) VALUES ('Dark'); --16
INSERT INTO types (name_) VALUES ('Steel'); --17
INSERT INTO types (name_) VALUES ('Fairy'); --18


CREATE TABLE IF NOT EXISTS pokemon(
    pokemon_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL UNIQUE,
    type_primary_id INTEGER NOT NULL,
    type_secondary_id INTEGER,
    generation INTEGER NOT NULL,

    FOREIGN KEY(type_primary_id) REFERENCES types(type_id),
    FOREIGN KEY(type_secondary_id) REFERENCES types(type_id)
);