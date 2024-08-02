/* Load data from staging into appropriate tables.
If a dimension does not currently exist, a new
entry needs to first be added to the appropriate
table. Similarly, match details can only be
populated once the match itself has been logged.*/


/* Populate players table.*/

INSERT INTO postgres.mtg.dim_players (
  player_name
)
SELECT DISTINCT unpivoted_players
FROM (
  SELECT player_one_name AS unpivoted_players
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_two_name
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_three_name
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_four_name
  FROM postgres.mtg.fact_staging_matches
) AS current_players
WHERE unpivoted_players IS NOT NULL
AND unpivoted_players NOT IN (
  SELECT player_name FROM postgres.mtg.dim_players
);


/* Populate commanders table.*/

INSERT INTO postgres.mtg.dim_commanders (
  commander_name -- Will sort out insertion of other characteristics later.
)
SELECT DISTINCT unpivoted_commanders
FROM (
  SELECT player_one_commander AS unpivoted_commanders
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_two_commander
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_three_commander
  FROM postgres.mtg.fact_staging_matches
  UNION ALL
  SELECT player_four_commander
  FROM postgres.mtg.fact_staging_matches
) AS current_commanders
WHERE unpivoted_commanders IS NOT NULL
AND unpivoted_commanders NOT IN (
  SELECT commander_name FROM postgres.mtg.dim_commanders
);