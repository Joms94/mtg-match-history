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


/* Populate matches and match detail.*/

WITH unpivoted_matches AS (
  SELECT
    p1_match.staging_matches_id,
    p1_det.player_id,
    p1_com.commander_id,
    CASE
      WHEN p1_det.player_name = p1_match.winner_name
      THEN 1
      ELSE 0
    END AS is_winner,
    p1_match.match_date
  FROM postgres.mtg.fact_staging_matches AS p1_match
  INNER JOIN postgres.mtg.dim_players AS p1_det
    ON p1_det.player_name = p1_match.player_one_name
  INNER JOIN postgres.mtg.dim_commanders AS p1_com
    ON p1_com.commander_name = p1_match.player_one_commander
  UNION ALL
  SELECT
    p2_match.staging_matches_id,
    p2_det.player_id,
    p2_com.commander_id,
    CASE
      WHEN p2_det.player_name = p2_match.winner_name
      THEN 1
      ELSE 0
    END AS is_winner,
    p2_match.match_date
  FROM postgres.mtg.fact_staging_matches AS p2_match
  INNER JOIN postgres.mtg.dim_players AS p2_det
    ON p2_det.player_name = p2_match.player_two_name
  INNER JOIN postgres.mtg.dim_commanders AS p2_com
    ON p2_com.commander_name = p2_match.player_two_commander
  UNION ALL
  SELECT
    p3_match.staging_matches_id,
    p3_det.player_id,
    p3_com.commander_id,
    CASE
      WHEN p3_det.player_name = p3_match.winner_name
      THEN 1
      ELSE 0
    END AS is_winner,
    p3_match.match_date
  FROM postgres.mtg.fact_staging_matches AS p3_match
  INNER JOIN postgres.mtg.dim_players AS p3_det
    ON p3_det.player_name = p3_match.player_three_name
  INNER JOIN postgres.mtg.dim_commanders AS p3_com
    ON p3_com.commander_name = p3_match.player_three_commander
  UNION ALL
  SELECT
    p4_match.staging_matches_id,
    p4_det.player_id,
    p4_com.commander_id,
    CASE
      WHEN p4_det.player_name = p4_match.winner_name
      THEN 1
      ELSE 0
    END AS is_winner,
    p4_match.match_date
  FROM postgres.mtg.fact_staging_matches AS p4_match
  INNER JOIN postgres.mtg.dim_players AS p4_det
    ON p4_det.player_name = p4_match.player_four_name
  INNER JOIN postgres.mtg.dim_commanders AS p4_com
    ON p4_com.commander_name = p4_match.player_four_commander
),
match_insert AS (
  INSERT INTO postgres.mtg.fact_matches(match_date, players, staging_matches_id)
  SELECT
    match_date,
    COUNT(staging_matches_id) AS players,
    staging_matches_id
  FROM unpivoted_matches
  GROUP BY match_date, staging_matches_id
  ORDER BY staging_matches_id
  RETURNING match_id, staging_matches_id
)
INSERT INTO postgres.mtg.fact_match_detail(match_id, player_id, commander_id, is_winner)
SELECT
  ins.match_id,
  matches.player_id,
  matches.commander_id,
  CAST(matches.is_winner AS BOOLEAN)
FROM match_insert AS ins
INNER JOIN unpivoted_matches AS matches
  ON matches.staging_matches_id = ins.staging_matches_id
ORDER BY ins.staging_matches_id;
