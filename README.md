# PS 2 Ex 3
# Authors: CMN, JMR
# Auditors: CW, LPH

# Setup

## Envrionment

Install the required packages by running:

```bash
conda env create -f environment.yml
```

Activate the environment by running:

```bash
conda activate solution_ps2_ex3_database
```

## Pre-commit

This repository uses pre-commit to run some checks before each commit. To install pre-commit, run:

```bash
pre-commit install
```

To run the checks manually, run:

```bash
pre-commit run --all-files
```

# Getting the data

1. create a Kaggle account: https://www.kaggle.com/
2. get API keys and user name
   - Go to your account, and click on your profile in the top right
   - Then click on "Settings"
   - Scroll down to the API section and click on "Create New Token"
   - Get your username and API key from there

We have written a data loader function for you in the "nba/data_loader.py".This allows you to
download the data with by running the script from the terminal. Run the following command in the
terminal being at the root of the repository.

```bash
python nba/data_loader.py -u "your_user_name" -k "your_api_key" -d "wyattowalsh/basketball"
```

Replace "your_user_name" and "your_api_key" with your username and API key. This creates a json
file at "~/.kaggle/kaggle.json" with your username and API key, which is used to authenticate your
account and download the data.

# Fun Facts

We have provided some functions to extract interesting fun facts from the NBA data. These functions are located in the `nba/funfacts.py` file. Below is a brief description of each function:

1. **get_top_countries(con: Connection) -> pd.DataFrame**:
    - Retrieves the top 5 countries with the most NBA players.
    - Returns a DataFrame with columns: `country` and `player_count`.

2. **get_height_extremes(con: Connection) -> Tuple[pd.DataFrame, pd.DataFrame]**:
    - Retrieves the tallest and shortest players.
    - Returns a tuple of DataFrames:
        - Tallest player info with columns: `person_id`, `first_name`, `last_name`, `display_first_last`, `height`.
        - Shortest player info with the same columns.

3. **get_biggest_blowout(con: Connection) -> pd.DataFrame**:
    - Retrieves the game with the largest point differential.
    - Returns a DataFrame with columns: `game_id`, `game_date`, `team_name_home`, `team_name_away`, `point_difference`.

4. **get_common_matchups(con: Connection) -> pd.DataFrame**:
    - Retrieves the most repeated match-ups between teams.
    - Returns a DataFrame with columns: `team_name_home`, `team_name_away`, `matchup_count`.

5. **print_all_funfacts(con: Connection) -> None**:
    - Prints all the fun facts about NBA data using the above functions.

To use these functions, you need to have a valid SQLite database connection. You can call these functions and pass the connection object to get the desired fun facts.

# Fitness Analysis

We have also provided some functions to analyze the fitness metrics of NBA players. These functions are located in the `nba/fitness.py` file. Below is a brief description of each function:

1. **calculate_bmi(weight: float, height: float) -> float**:
    - Calculates the Body Mass Index (BMI) using weight and height measurements.
    - Returns the BMI value calculated using the formula: `703 * (weight / height^2)`.

2. **plot_metric_by_position(data: pd.DataFrame, metric: str, title: str, ylabel: str) -> None**:
    - Creates a box plot showing the distribution of a metric across different positions.
    - Takes a DataFrame containing position and metric data, the name of the column containing the metric to plot, the title for the plot, and the label for the y-axis.
    - Displays the plot using `plt.show()`.

To use these functions, you need to have the necessary data in a pandas DataFrame. You can call these functions and pass the required parameters to perform the fitness analysis and visualization.

# Home Team Analysis

We have also provided some functions to analyze the performance of home teams in NBA games. These functions are located in the `nba/home_team.py` file. Below is a brief description of each function:

1. **prepare_game_data(games_df: pd.DataFrame) -> pd.DataFrame**:
    - Prepares game data by converting dates and adding time-based columns.
    - Takes a DataFrame containing game data with columns: `game_date`, `day_of_week`.
    - Returns a DataFrame with added columns: `year`, `month`, `day_of_week`.

2. **calculate_yearly_stats(games_df: pd.DataFrame) -> pd.DataFrame**:
    - Calculates yearly statistics for home team performance.
    - Takes a DataFrame containing game data with columns: `year`, `game_id`, `wl_home`, `point_diff`.
    - Returns a DataFrame grouped by year containing: `game_id` (count of games per year), `wl_home` (home win percentage), `point_diff` (mean and standard deviation of point differential).

3. **calculate_day_stats(games_df: pd.DataFrame) -> pd.DataFrame**:
    - Calculates statistics by day of week.
    - Takes a DataFrame containing game data with columns: `day_of_week`, `wl_home`.
    - Returns a DataFrame grouped by day of week containing: `wl_home` (home win percentage), `day_name` (three letter day abbreviation).

4. **plot_home_advantage(games_df: pd.DataFrame, yearly_stats: pd.DataFrame, day_stats: pd.DataFrame) -> Tuple[plt.Figure, float, float]**:
    - Creates visualization of home court advantage statistics.
    - Takes a DataFrame containing game data, a DataFrame with yearly statistics, and a DataFrame with day of week statistics.
    - Returns a tuple containing:
        - `plt.Figure`: Figure with 3 subplots showing:
            1. Home win percentage over time with point differential variance.
            2. Home win percentage by day of week.
            3. Distribution of point differential.
        - `float`: Overall average home win percentage.
        - `float`: Overall average point differential.

To use these functions, you need to have the necessary game data in a pandas DataFrame. You can call these functions and pass the required parameters to perform the home team analysis and visualization.
