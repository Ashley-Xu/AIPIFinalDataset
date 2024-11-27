# tinder_data_cleaning.py

import pandas as pd
import numpy as np

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Perform data cleaning operations."""
    # Drop columns if they are the same
    if (df['education'] == df['educationLevel']).all():
        df = df.drop(columns=['educationLevel'])
    
    if (df['no_of_days_x'] == df['no_of_days_y']).all():
        df = df.drop(columns=['no_of_days_y'])
    
    df = df.rename(columns={'no_of_days_x': 'no_of_days'})
    
    # Fill missing values
    df['cityName'].fillna('unknown', inplace=True)
    df['country'].fillna('unknown', inplace=True)
    df['jobTitle'].fillna('unknown', inplace=True)
    
    return df

def calculate_age(df):
    """Calculate user age from birthDate and createDate."""
    df['birthDate'] = pd.to_datetime(df['birthDate'])
    df['createDate'] = pd.to_datetime(df['createDate'])
    df['user_age'] = (df['createDate'] - df['birthDate']).dt.days // 365
    return df


def main():
    df = load_data('Tinder_Data_v2.csv')
    df = clean_data(df)
    df = calculate_age(df)
    df.to_csv('Tinder_Data_v3_Clean_Edition.csv', index=False)

if __name__ == '__main__':
    main()
