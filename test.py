import unittest
from unittest.mock import patch
from io import StringIO
from main import generate_abbreviations

class TestGenerateAbbreviations(unittest.TestCase):

    def test_generate_abbreviations(self):
        names = ["Common Ash", "Bay Willow"]
        values = {'A': 25, 'B': 8, 'C': 8, 'D': 9, 'E': 35, 'F': 7, 'G': 9, 'H': 7, 'I': 25, 'J': 3, 'K': 6,
                  'L': 15, 'M': 8, 'N': 15, 'O': 20, 'P': 8, 'Q': 1, 'R': 15, 'S': 15, 'T': 15, 'U': 20,
                  'V': 7, 'W': 7, 'X': 3, 'Y': 7, 'Z': 1}
    
        expected_output = {'COS': ('Common Ash', 38), 'BAI': ('Bay Willow', 53)}
    
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            generate_abbreviations(names, values)
            actual_output = mock_stdout.getvalue().strip()

        # Extract the relevant part for comparison
        actual_abbreviations = {}
        for line in actual_output.split("\n"):
            parts = line.split(":")
            if len(parts) == 2:
                key, value = parts
                actual_abbreviations[key.strip()] = tuple(map(str.strip, value.split('(')))

        self.assertEqual(actual_abbreviations, expected_output, f"Expected: {expected_output}\nActual: {actual_abbreviations}")

if __name__ == '__main__':
    unittest.main()
