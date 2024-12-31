import unittest
from pathlib import Path
import user_data_proccesor
import json
import tempfile
from unittest.mock import patch, call

"""
This file contains the tests for the user_data_proccesor.py library.
"""

class TestUserDataProccesor(unittest.TestCase):

    # Test if the read_csv function returns the expected data
    def test_read_csv_ret_expected(self):
        data = user_data_proccesor.read_csv(Path("data.csv"), Path("template.json"))
        expected = json.loads(Path("test_files/expected_output.json").read_text())
        self.assertListEqual(data, expected)

    # Test if output is saved correctly
    def test_json_saved_correctly(self):
        expected = json.loads(Path("test_files/expected_output.json").read_text())
        # Use a temporary file to store the output without modifying the original
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "output.json"
            user_data_proccesor.write_to_output(expected, output_path)
            output = json.loads(output_path.read_text())
        self.assertListEqual(output, expected)

    # Test printing of the tags is correct
    def test_prints_ret_expected(self):
        with patch("builtins.print") as mock_stdout:
            data_array = user_data_proccesor.read_csv(Path("test_files/small_good_data.csv"), Path("template.json"))
            user_data_proccesor.tag_users_iterative(data_array)
            self.assertEqual(3, mock_stdout.call_count) # 3 calls to print
            # Check the output of the print calls
            mock_stdout.assert_has_calls([
                call("Grace Davis is not a spender."),
                call("Hank Martinez is a spender."),
                call("David Garcia is not a spender.")
            ])

    def test_template_with_bad_json_exits(self):
        with self.assertRaises(SystemExit):
            user_data_proccesor.read_csv(
                Path("test_files/small_good_data.csv"), Path("test_files/not_json_template.json"))
    
    def test_template_with_bad_format_exits(self):
        with self.assertRaises(SystemExit):
            user_data_proccesor.read_csv(
                Path("test_files/small_good_data.csv"), Path("test_files/bad_format_template.json"))
    
    def test_csv_with_missing_column_key_exits(self):   
        with self.assertRaises(SystemExit):
            user_data_proccesor.read_csv(
                Path("test_files/small_missing_column_key.csv"), Path("template.json"))

    def test_csv_with_missing_columns_reports(self):
        with patch("builtins.print") as mock_stdout:
            data_array = user_data_proccesor.read_csv(
                Path("test_files/small_missing_columns_data.csv"), Path("template.json"))
            user_data_proccesor.tag_users_iterative(data_array)
            # Check the output of the print calls
            mock_stdout.assert_has_calls([
                call("Taging user: Hank Martinez, failed due to ValueError: invalid literal for int() with base 10: ''"),
                call("Taging user: David Garcia, failed due to ValueError: invalid literal for int() with base 10: 'None'")
            ])

    def test_csv_with_bad_typed_data_reports(self):
        with patch("builtins.print") as mock_stdout:
            data_array = user_data_proccesor.read_csv(
                Path("test_files/small_bad_data.csv"), Path("template.json"))
            user_data_proccesor.tag_users_iterative(data_array)
            # Check the output of the print calls
            mock_stdout.assert_has_calls([
                call("Taging user: Grace Davis, failed due to ValueError: invalid literal for int() with base 10: 'hello'"),
                call("Taging user: Hank  Martinez, failed due to ValueError: Invalid name: Hank  Martinez -name should contain only letters and at most one space."),
                call("Taging user: Davi8909Garcia, failed due to ValueError: Invalid name: Davi8909Garcia -name should contain only letters and at most one space.")
            ])

if __name__ == "__main__":
    unittest.main()
