import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A pandas DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path)

def calculate_numerical_stats(df):
    """
    Calculate descriptive statistics for numerical columns in a DataFrame.

    Parameters:
    df (DataFrame): The DataFrame containing the data.

    Returns:
    DataFrame: A DataFrame with descriptive statistics for each numerical column, including range.
    """
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    numerical_stats = df[numerical_columns].describe().transpose()
    numerical_stats['range'] = numerical_stats['max'] - numerical_stats['min']
    return numerical_stats

def calculate_categorical_freq_counts(df):
    """
    Calculate frequency counts for categorical columns in a DataFrame.

    Parameters:
    df (DataFrame): The DataFrame containing the data.

    Returns:
    dict: A dictionary with column names as keys and frequency counts as values.
    """
    categorical_columns = df.select_dtypes(include=[object, 'category']).columns
    return {col: df[col].value_counts() for col in categorical_columns}

def plot_age_filter_by_gender(df):
    """
    Plot the average age filter by gender using a bar plot.

    Parameters:
    df (DataFrame): The DataFrame containing the data with 'gender', 'ageFilterMin', and 'ageFilterMax' columns.
    """
    age_filter_data = df[['gender', 'ageFilterMin', 'ageFilterMax']]
    age_filter_summary = age_filter_data.groupby('gender').agg({
        'ageFilterMin': 'mean',
        'ageFilterMax': 'mean'
    }).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='gender', y='value', hue='variable', 
                data=pd.melt(age_filter_summary, ['gender'], value_vars=['ageFilterMin', 'ageFilterMax']))
    plt.title('Average Age Filter by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Age')
    plt.legend(title='Age Filter')
    plt.show()

def main():
    """
    Main function to load data, calculate statistics, and plot data.
    """
    df = load_data('Tinder_Data_v3_Clean_Edition.csv')
    print(calculate_numerical_stats(df))
    print(calculate_categorical_freq_counts(df))
    plot_age_filter_by_gender(df)

if __name__ == '__main__':
    main()
