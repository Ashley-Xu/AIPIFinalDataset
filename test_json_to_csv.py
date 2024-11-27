import unittest
from unittest.mock import patch, mock_open
import json_to_csv

class TestJsonToCsv(unittest.TestCase):

    def setUp(self):
        # Mock data to be used in tests
        self.mock_data = [
            {
                "_id": "user1",
                "messages": {
                    "sent": {"day1": 5, "day2": 3},
                    "received": {"day1": 2, "day2": 4}
                },
                "matches": {"day1": 1, "day2": 2},
                "swipeLikes": {"day1": 10, "day2": 15},
                "swipePasses": {"day1": 5, "day2": 7},
                "user": {
                    "birthDate": "1990-01-01",
                    "ageFilterMin": 18,
                    "ageFilterMax": 30,
                    "cityName": "New York",
                    "country": "USA",
                    "createDate": "2020-01-01",
                    "education": "College",
                    "gender": "male",
                    "interestedIn": "female",
                    "genderFilter": "female",
                    "instagram": "user1_insta",
                    "spotify": "user1_spotify",
                    "jobs": [{"title": "Engineer"}],
                    "educationLevel": "Bachelor"
                }
            }
        ]

    def test_calculate_messages(self):
        expected_result = [("user1", 8, 6)]
        result = json_to_csv.calculate_messages(self.mock_data)
        self.assertEqual(result, expected_result)

    def test_calculate_matches(self):
        expected_result = [("user1", 2, 3)]
        result = json_to_csv.calculate_matches(self.mock_data)
        self.assertEqual(result, expected_result)

    def test_calculate_swipes(self):
        expected_result = [("user1", 25, 12)]
        result = json_to_csv.calculate_swipes(self.mock_data)
        self.assertEqual(result, expected_result)

    def test_extract_user_info(self):
        expected_result = [(
            "user1", "1990-01-01", 18, 30, "New York", "USA", "2020-01-01",
            "College", "male", "female", "female", "user1_insta", "user1_spotify",
            "Engineer", "Bachelor"
        )]
        result = json_to_csv.extract_user_info(self.mock_data)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
