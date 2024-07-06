/* Load data from staging into appropriate tables.
If a dimension does not currently exist, a new
entry needs to first be added to the appropriate
table. Similarly, match details can only be
populated once the match itself has been logged.*/


/* Populate players table.*/

INSERT INTO postgres.dim.players (
  player_name
)
SELECT DISTINCT unpivoted_players
FROM (
  SELECT player_one_name AS unpivoted_players
  FROM postgres.fact.staging_matches
  UNION ALL
  SELECT player_two_name
  FROM postgres.fact.staging_matches
  UNION ALL
  SELECT player_three_name
  FROM postgres.fact.staging_matches
  UNION ALL
  SELECT player_four_name
  FROM postgres.fact.staging_matches
) AS current_players
WHERE unpivoted_players IS NOT NULL
AND unpivoted_players NOT IN (
  SELECT player_name FROM postgres.dim.players
);