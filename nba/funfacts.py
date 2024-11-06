import pandas as pd
from sqlite3 import Connection
from typing import Tuple

def get_top_countries(con: Connection) -> pd.DataFrame:
    """Get the top 5 countries with the most players.
    
    Args:
        con (Connection): SQLite database connection

    Returns:
        pd.DataFrame: DataFrame containing:
            country: Country name
            player_count: Number of players from that country
    """
    query = """
    SELECT country, COUNT(*) AS player_count
    FROM common_player_info
    WHERE country IS NOT NULL
    GROUP BY country
    ORDER BY player_count DESC
    LIMIT 5
    """
    return pd.read_sql(query, con)

def get_height_extremes(con: Connection) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get the tallest and shortest players.
    
    Args:
        con (Connection): SQLite database connection

    Returns:
        Tuple containing:
            pd.DataFrame: Tallest player info with columns:
                person_id, first_name, last_name, display_first_last, height
            pd.DataFrame: Shortest player info with same columns
    """
    # Tallest Player
    tallest_query = """
    SELECT person_id, first_name, last_name, display_first_last, height
    FROM common_player_info
    WHERE height IS NOT NULL
    ORDER BY CAST(height AS REAL) DESC
    LIMIT 1
    """
    
    # Shortest Player
    shortest_query = """
    SELECT person_id, first_name, last_name, display_first_last, height
    FROM common_player_info
    WHERE height IS NOT NULL
      AND height != '' 
      AND CAST(height AS REAL) IS NOT NULL
    ORDER BY CAST(height AS REAL) ASC
    LIMIT 1
    """
    
    return pd.read_sql(tallest_query, con), pd.read_sql(shortest_query, con)

def get_biggest_blowout(con: Connection) -> pd.DataFrame:
    """Get the game with the largest point differential.
    
    Args:
        con (Connection): SQLite database connection

    Returns:
        pd.DataFrame: DataFrame containing game info with columns:
            game_id: Unique game identifier
            game_date: Date of the game
            team_name_home: Home team name
            team_name_away: Away team name
            point_difference: Absolute difference in points between teams
    """
    query = """
    SELECT game_id, game_date, team_name_home, team_name_away, 
           ABS(pts_home - pts_away) AS point_difference
    FROM game
    ORDER BY point_difference DESC
    LIMIT 1
    """
    return pd.read_sql(query, con)

def get_common_matchups(con: Connection) -> pd.DataFrame:
    """Get the most repeated match-ups between teams.
    
    Args:
        con (Connection): SQLite database connection

    Returns:
        pd.DataFrame: DataFrame containing:
            team_name_home: Home team name
            team_name_away: Away team name
            matchup_count: Number of times these teams played each other
    """
    query = """
    SELECT team_name_home, team_name_away, COUNT(*) AS matchup_count
    FROM game
    GROUP BY team_name_home, team_name_away
    ORDER BY matchup_count DESC
    LIMIT 5
    """
    return pd.read_sql(query, con)

def print_all_funfacts(con: Connection) -> None:
    """Print all fun facts about NBA data.
    
    Args:
        con (Connection): SQLite database connection
    """
    # Top countries
    top_countries = get_top_countries(con)
    print("\n=== Top Countries with Most Players ===")
    for _, row in top_countries.iterrows():
        print(f"{row['country']}: {row['player_count']} players")
    
    # Height extremes
    tallest, shortest = get_height_extremes(con)
    print("\n=== Height Extremes ===")
    print(f"Tallest: {tallest.iloc[0]['display_first_last']} ({tallest.iloc[0]['height']})")
    print(f"Shortest: {shortest.iloc[0]['display_first_last']} ({shortest.iloc[0]['height']})")
    
    # Biggest blowout
    blowout = get_biggest_blowout(con)
    print("\n=== Biggest Blowout ===")
    print(f"Date: {blowout.iloc[0]['game_date']}")
    print(f"{blowout.iloc[0]['team_name_home']} vs {blowout.iloc[0]['team_name_away']}")
    print(f"Point Difference: {blowout.iloc[0]['point_difference']}")
    
    # Common matchups
    matchups = get_common_matchups(con)
    print("\n=== Most Common Matchups ===")
    for _, row in matchups.iterrows():
        print(f"{row['team_name_home']} vs {row['team_name_away']}: {row['matchup_count']} games")
