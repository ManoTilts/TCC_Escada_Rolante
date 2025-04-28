import unittest
from src.utils.json_reader import read_json

class TestJsonReader(unittest.TestCase):

    def test_read_json_valid(self):
        data = read_json('path/to/valid/game_output.json')
        self.assertIsInstance(data, dict)  # Assuming the JSON data is a dictionary
        self.assertIn('game_mode', data)
        self.assertIn('score', data)
        self.assertIn('reaction_speed', data)

    def test_read_json_invalid(self):
        with self.assertRaises(FileNotFoundError):
            read_json('path/to/invalid/game_output.json')

    def test_read_json_empty(self):
        data = read_json('path/to/empty/game_output.json')
        self.assertEqual(data, {})  # Assuming an empty JSON file returns an empty dictionary

if __name__ == '__main__':
    unittest.main()