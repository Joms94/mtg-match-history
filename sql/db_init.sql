/* Initialises all required tables for this project.
Written for Postgres on Supabase.

The database is always "postgres" on Supabase,
with one database allocated per project.*/

ALTER DATABASE postgres
SET
  datestyle TO 'ISO, DMY';


/* Tables will be separated by semantic model purpose.
Fact = transaction-level data. I.e., match history.
Dim = dimensions. Tertiary pieces of information
that enrich the facts.*/

CREATE SCHEMA IF NOT EXISTS fact;

CREATE SCHEMA IF NOT EXISTS dim;

DROP TABLE IF EXISTS postgres.fact.match_detail;
DROP TABLE IF EXISTS postgres.fact.matches;
DROP TABLE IF EXISTS postgres.fact.staging_matches;
DROP TABLE IF EXISTS postgres.dim.commanders;
DROP TABLE IF EXISTS postgres.dim.players;


/* Stores basic information on each player.*/

CREATE TABLE postgres.dim.players (
    player_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    player_name VARCHAR(40) NOT NULL,
    alias VARCHAR(40) -- For public data vis.
);


/* Stores commander information, such as
the commander's name and their colour identity.*/

CREATE TABLE postgres.dim.commanders (
    commander_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    commander_name VARCHAR(80) NOT NULL,
    cost SMALLINT NOT NULL,
    is_white BOOLEAN DEFAULT FALSE,
    is_blue BOOLEAN DEFAULT FALSE,
    is_black BOOLEAN DEFAULT FALSE,
    is_red BOOLEAN DEFAULT FALSE,
    is_green BOOLEAN DEFAULT FALSE
);


/* Stores a row for each match.*/

CREATE TABLE postgres.fact.matches (
    match_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    match_date DATE DEFAULT NOW(),
    players INT NOT NULL
);


/* Stores a row for each player in the match and
whether or not they won.
Accommodates for oddball games of two-headed giant
where you might have two winners, or games that have
more or less than four players.*/

CREATE TABLE postgres.fact.match_detail (
    match_detail_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, -- Unique to the row.
    match_id INT NOT NULL, -- Unique to the match.
    player_id INT NOT NULL,
    commander_id INT NOT NULL,
    is_winner BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_match FOREIGN KEY(match_id) REFERENCES fact.matches(match_id),
    CONSTRAINT fk_player FOREIGN KEY(player_id) REFERENCES dim.players(player_id),
    CONSTRAINT fk_commander FOREIGN KEY(commander_id) REFERENCES dim.commanders(commander_id)
);


/* Table for storing raw input data before being
assigned to appropriate tables.

I keep my match history in a spreadsheet, but
it's structured for input convenience rather than
analysis. Change the layout of this table to suit
how you're currently storing your input data.

My input spreadsheet doesn't accommodate for
more than four players, or more than one winner.
However, given how rare either of those things
are, I'll just edit the DB manually as and
when that occurs.*/

CREATE TABLE postgres.fact.staging_matches (
    match_date DATE DEFAULT NOW(),
    player_one_name VARCHAR(40) NOT NULL,
    player_one_commander VARCHAR(80) NOT NULL,
    player_two_name VARCHAR(40) NOT NULL,
    player_two_commander VARCHAR(80) NOT NULL,
    player_three_name VARCHAR(40),
    player_three_commander VARCHAR(80),
    player_four_name VARCHAR(40),
    player_four_commander VARCHAR(80),
    winner_name VARCHAR(40),
    winner_commander VARCHAR(80)
);