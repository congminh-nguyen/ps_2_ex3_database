import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Tuple

def prepare_game_data(games_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare game data by converting dates and adding time-based columns.
    
    Args:
        games_df (pd.DataFrame): DataFrame containing game data with columns:
            game_date, day_of_week
            
    Returns:
        pd.DataFrame: DataFrame with added columns:
            year: Year extracted from game_date
            month: Month extracted from game_date
            day_of_week: Converted to integer type
    """
    games_df['game_date'] = pd.to_datetime(games_df['game_date'])
    games_df['year'] = games_df['game_date'].dt.year
    games_df['month'] = games_df['game_date'].dt.month
    games_df['day_of_week'] = games_df['day_of_week'].astype(int)
    return games_df

def calculate_yearly_stats(games_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly statistics for home team performance.
    
    Args:
        games_df (pd.DataFrame): DataFrame containing game data with columns:
            year, game_id, wl_home, point_diff
            
    Returns:
        pd.DataFrame: DataFrame grouped by year containing:
            game_id: Count of games per year
            wl_home: Home win percentage (0-100)
            point_diff: Mean and standard deviation of point differential
    """
    return (games_df.groupby('year')
            .agg({
                'game_id': 'count',
                'wl_home': lambda x: (x == 'W').mean() * 100,
                'point_diff': ['mean', 'std']
            })
            .reset_index())

def calculate_day_stats(games_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate statistics by day of week.
    
    Args:
        games_df (pd.DataFrame): DataFrame containing game data with columns:
            day_of_week, wl_home
            
    Returns:
        pd.DataFrame: DataFrame grouped by day of week containing:
            wl_home: Home win percentage (0-100)
            day_name: Three letter day abbreviation (Sun, Mon, etc.)
    """
    day_stats = (games_df.groupby('day_of_week')
                .agg({'wl_home': lambda x: (x == 'W').mean() * 100})
                .reset_index())
    day_stats['day_name'] = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return day_stats

def plot_home_advantage(games_df: pd.DataFrame, yearly_stats: pd.DataFrame, day_stats: pd.DataFrame) -> Tuple[plt.Figure, float, float]:
    """Create visualization of home court advantage statistics.
    
    Args:
        games_df (pd.DataFrame): DataFrame containing game data
        yearly_stats (pd.DataFrame): DataFrame with yearly statistics
        day_stats (pd.DataFrame): DataFrame with day of week statistics
        
    Returns:
        tuple containing:
            plt.Figure: Figure with 3 subplots showing:
                1. Home win percentage over time with point differential variance
                2. Home win percentage by day of week
                3. Distribution of point differential
            float: Overall average home win percentage
            float: Overall average point differential
    """
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 2)
    
    # 1. Home Win % Over Time
    ax1 = fig.add_subplot(gs[0, :])
    sns.lineplot(data=yearly_stats, x='year', y='home_win_pct', ax=ax1, color='blue', linewidth=2)
    ax1.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax1.fill_between(yearly_stats['year'],
                     yearly_stats['home_win_pct'] - yearly_stats['point_diff_std']/2,
                     yearly_stats['home_win_pct'] + yearly_stats['point_diff_std']/2,
                     alpha=0.2)
    ax1.set_title('Home Team Win % Over Time (with Point Differential Variance)', fontsize=12)
    ax1.set_ylabel('Home Win %')

    # 2. Win % by Day of Week  
    ax2 = fig.add_subplot(gs[1, 0])
    sns.barplot(data=day_stats, x='day_name', y='wl_home', ax=ax2)
    ax2.set_title('Home Win % by Day of Week', fontsize=12)
    ax2.set_ylabel('Home Win %')

    # 3. Point Differential Distribution
    ax3 = fig.add_subplot(gs[1, 1])
    sns.histplot(data=games_df, x='point_diff', bins=50, ax=ax3)
    ax3.axvline(x=0, color='red', linestyle='--')
    ax3.set_title('Distribution of Point Differential\n(Home - Away)', fontsize=12)
    ax3.set_xlabel('Point Differential')

    # Add overall stats
    avg_home_win = (games_df['wl_home'] == 'W').mean() * 100
    avg_point_diff = games_df['point_diff'].mean()
    text = (f"Overall Stats:\n"
            f"Average Home Win %: {avg_home_win:.1f}%\n"
            f"Average Point Diff: {avg_point_diff:.1f}")
    fig.text(0.98, 0.98, text, fontsize=10, ha='right', va='top',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    return fig, avg_home_win, avg_point_diff