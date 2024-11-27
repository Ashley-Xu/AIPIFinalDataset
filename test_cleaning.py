import unittest
from unittest.mock import patch
import pandas as pd
from cleaning import load_data, clean_data, calculate_age

class TestCleaningFunctions(unittest.TestCase):

    @patch('cleaning.pd.read_csv')
    def test_load_data(self, mock_read_csv):
        # Mock the return value of pd.read_csv
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_csv.return_value = mock_df

        # Call the function
        result = load_data('dummy_path.csv')

        # Assert the result is as expected
        mock_read_csv.assert_called_once_with('dummy_path.csv')
        pd.testing.assert_frame_equal(result, mock_df)

    def test_clean_data(self):
        # Create a mock DataFrame
        df = pd.DataFrame({
            'education': ['High School', 'College'],
            'educationLevel': ['High School', 'College'],
            'no_of_days_x': [10, 20],
            'no_of_days_y': [10, 20],
            'cityName': [None, 'New York'],
            'country': ['USA', None],
            'jobTitle': [None, 'Engineer']
        })

        # Call the function
        result = clean_data(df)

        # Check the result
        self.assertNotIn('educationLevel', result.columns)
        self.assertNotIn('no_of_days_y', result.columns)
        self.assertIn('no_of_days', result.columns)
        self.assertEqual(result['cityName'].tolist(), ['unknown', 'New York'])
        self.assertEqual(result['country'].tolist(), ['USA', 'unknown'])
        self.assertEqual(result['jobTitle'].tolist(), ['unknown', 'Engineer'])

    def test_calculate_age(self):
        # Create a mock DataFrame
        df = pd.DataFrame({
            'birthDate': ['1990-01-01', '2000-01-01'],
            'createDate': ['2020-01-01', '2020-01-01']
        })

        # Call the function
        result = calculate_age(df)

        # Check the result
        self.assertEqual(result['user_age'].tolist(), [30, 20])

if __name__ == '__main__':
    unittest.main()
