import unittest
from scripts.access_log_analyzer import *
from unittest.mock import patch

class UnitTests(unittest.TestCase):
    @patch("builtins.input", return_value="/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")   # simulate input
    def test_input_file(self, mock_input):
        result = input_file()
        self.assertEqual(result, "")

    def test_extracted_data_from_apache_combined_format_file(self):
        result = extract_data_from_file(1, "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")
        self.assertEqual(result, "")

    def test_total_number_of_requests(self):
        result = total_number_of_requests([{},{}])
        self.assertEqual(result, "")

    def test_IP_frequencies(self):
        result = IP_frequencies([{},{}])
        self.asserEqual(result, "")

    def test_status_code_destribution(self):
        result = status_code_destribution([{},{}])
        self.assertEqual(result, "")

    def test_error_percentage():
        pass

    def test_hourly_traffics(all_data_dict_list):