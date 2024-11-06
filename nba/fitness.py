import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import DataFrame

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate Body Mass Index (BMI) using weight and height measurements.
    
    Args:
        weight (float): Weight in pounds
        height (float): Height in inches
        
    Returns:
        float: BMI value calculated using the formula: 703 * (weight / height^2)
    """
    return 703 * (weight / (height ** 2))

def plot_metric_by_position(data: pd.DataFrame, metric: str, title: str, ylabel: str) -> None:
    """Create a box plot showing the distribution of a metric across different positions.
    
    Args:
        data (DataFrame): DataFrame containing position and metric data
        metric (str): Name of the column containing the metric to plot
        title (str): Title for the plot
        ylabel (str): Label for the y-axis
        
    Returns:
        None: Displays the plot using plt.show()
    """
    # Calculate mean for each position
    position_mean = data.groupby('position')[metric].mean().sort_values()
    
    # Calculate the number of observations for each position 
    position_counts = data['position'].value_counts()
    
    # Reorder positions by increasing mean
    ordered_positions = position_mean.index.tolist()
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='position', y=metric, data=data, order=ordered_positions, boxprops=dict(alpha=0.5))
    plt.xticks(rotation=45)
    plt.title(title, fontsize=16)
    plt.xlabel('Position', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(False)
    
    # Denote the mean and number of observations for each position
    for pos in ordered_positions:
        mean_val = position_mean[pos]
        count_val = position_counts[pos]
        plt.scatter(x=ordered_positions.index(pos), y=mean_val, color='red', zorder=5)
        plt.text(x=ordered_positions.index(pos), y=mean_val + 0.3, s=f'{mean_val:.2f}', color='red', ha='center', va='bottom', fontsize=8)
        plt.text(x=ordered_positions.index(pos), y=plt.ylim()[0] + 0.4, s=f'n={count_val}', color='black', ha='center', va='top', fontsize=8)
    
    plt.show()