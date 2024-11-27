'''

import unittest
import pandas as pd
from EDA import load_data, calculate_numerical_stats, calculate_categorical_freq_counts

class TestEDAFunctions(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            'gender': ['male', 'female', 'male'],
            'ageFilterMin': [18, 20, 22],
            'ageFilterMax': [25, 30, 28],
            'swipe_likes': [10, 15, 5],
            'swipe_passes': [5, 10, 15]
        })

    def test_load_data(self):
        df = load_data('Tinder_Data_v3_Clean_Edition.csv')
        self.assertIsInstance(df, pd.DataFrame)

    def test_calculate_numerical_stats(self):
        stats = calculate_numerical_stats(self.df)
        self.assertIn('range', stats.columns)

    def test_calculate_categorical_freq_counts(self):
        freq_counts = calculate_categorical_freq_counts(self.df)
        self.assertIn('gender', freq_counts)
        self.assertEqual(freq_counts['gender']['male'], 2)

if __name__ == '__main__':
    unittest.main()


'''






    # test_eda_functions.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from EDA import load_data, calculate_numerical_stats, calculate_categorical_freq_counts, plot_age_filter_by_gender

class TestEDAFunctions(unittest.TestCase):

    @patch('EDA.pd.read_csv')
    def test_load_data(self, mock_read_csv):
        # Mock the return value of pd.read_csv
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_csv.return_value = mock_df

        # Call the function
        result = load_data('dummy_path.csv')

        # Assert the result is as expected
        mock_read_csv.assert_called_once_with('dummy_path.csv')
        pd.testing.assert_frame_equal(result, mock_df)

    def test_calculate_numerical_stats(self):
        # Create a mock DataFrame
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 6, 7, 8, 9]
        })

        # Call the function
        result = calculate_numerical_stats(df)

        # Check the result
        expected_columns = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'range']
        self.assertTrue(all(col in result.columns for col in expected_columns))
        self.assertEqual(result.loc['A', 'range'], 4)
        self.assertEqual(result.loc['B', 'range'], 4)

    def test_calculate_categorical_freq_counts(self):
        # Create a mock DataFrame
        df = pd.DataFrame({
            'C': ['cat', 'dog', 'cat', 'bird'],
            'D': ['apple', 'banana', 'apple', 'apple']
        })

        # Call the function
        result = calculate_categorical_freq_counts(df)

        # Check the result
        self.assertEqual(result['C'].to_dict(), {'cat': 2, 'dog': 1, 'bird': 1})
        self.assertEqual(result['D'].to_dict(), {'apple': 3, 'banana': 1})

    @patch('EDA.plt.show')
    def test_plot_age_filter_by_gender(self, mock_show):
        # Create a mock DataFrame
        df = pd.DataFrame({
            'gender': ['male', 'female', 'male', 'female'],
            'ageFilterMin': [18, 20, 22, 24],
            'ageFilterMax': [30, 32, 34, 36]
        })

        # Call the function
        plot_age_filter_by_gender(df)

        # Assert that plt.show() was called
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()