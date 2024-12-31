from pathlib import Path # for reading files
import csv # for reading csv files
import json # for reading/writing json files (e.g. output, template)
from multiprocessing import Pool # for parallel processing
import re # for use of regular expressions
import time # for simulating processing time

"""
This is a library for processing user data from a csv file and tagging users as spenders or non-spenders.
The library contains the following functions and classes:
    1. read_csv: Reads csv file and returns python dictionary with data in json format
    2. write_to_output: Writes the data_array to a json file at the output_path
    3. User: A class used to tag a user as a spender or non-spender based on their expenses
    4. tag_users_iterative: Tags each user as a spender or non-spender using User.tag in iterative manner
    5. tag_users_parallel: Tags each user as a spender or non-spender using User.tag in parallel manner
"""

def read_csv(data_path:Path, template_path:Path) -> list[dict]:
    """
    Reads csv file and returns python dictionary with data in json format

    Args:
        1. data_path: path to the csv file with data
        2. template_path: path to json template file that fits the csv data

    Returns:
        data_array: array of dictionaries. Each dictionary is a row in the csv file processed using the template
    """
    data_array = []
    template = template_path.read_text() # template as a string
    try:
        with data_path.open("rt") as my_data_csv:
            # Create a CSV reader object that reads each row in the file as a dictionary
            # The keys are the column names and the values are the row values
            data_reader = csv.DictReader(my_data_csv)

            placeholder_keys = set(re.findall(r'\{(\w+)\}', template))
            if set(data_reader.fieldnames) != placeholder_keys:
                print("Mismatch in columns between csv data and template")
                exit()

            for row in data_reader:
                try:
                    # Replace placeholders in template and append dictionary to data_array
                    data_array.append(json.loads(template.format(**row)))
                
                except KeyError as key_error:
                    print(f"KeyError: {key_error} not found in template")
                    exit()
                except json.JSONDecodeError as json_error:
                    print("Template is not valid json format. JSONDecodeError: {json_error}")
                    exit()
                except Exception as error:
                    print(f"Unexpected error when processing csv: {error}")
                    exit()
    except FileNotFoundError as file_error:
        print(f"Error opening data_path: {data_path}, result is FileNotFoundError: {file_error}")
        exit()

    return data_array

def write_to_output(data_array:list[dict], output_path:Path) -> None:
    """
    Writes the data_array to a json file at the output_path

    Args:
        data_array: array of dictionaries to be written to a json file
        output_path: path to the output json file

    Returns:
        None
    """
    with output_path.open("wt") as my_output_json:
        json.dump(data_array, my_output_json, indent=4)
    return None

class User:
    """
    This class is used to tag a user as a spender or non-spender based on their expenses.
    A user is considered a spender if their total expenses (of food and clothes) exceed their salary (expenses > salary).
    Else, (expenses <= salary) they are considered a non-spender.
    Only one method is defined in this class, which is a static method named tag.
    """
    @staticmethod
    def tag(user_dict: dict) -> None:
        """
        Tags a user as a spender or non-spender based on their expenses and salary and prints the result
        
        Args:
            user_dict: a dictionary containing the user's name, salary, food expenses, and clothing expenses

        Returns:
            None
        """
        try:

            # Validate that the user's name contains only letters
            name = user_dict['user']['name']
            if not re.match(r"^[a-zA-Z]+(?: [a-zA-Z]+)?$", name):  # Match letters and at most one space
                raise ValueError(f"Invalid name: {name} -name should contain only letters and at most one space.")

            expenses_sum = sum(map(int, user_dict["expenses"].values()))
            if expenses_sum > int(user_dict["user"]["salary"]):
                print(f"{user_dict['user']['name']} is a spender.")
            else:
                print(f"{user_dict['user']['name']} is not a spender.")

        except ValueError as value_error:
            print(f"Taging user: {user_dict['user']['name']}, failed due to ValueError: {value_error}")
        
        time.sleep(0.1) # Simulate a delay in processing
        return None
        
def tag_users_iterative(data_array:list[dict]) -> None:
    """
    Tags each user as a spender or non-spender using User.tag in iterative manner and prints the result.

    Args:
        data_array: array of dictionaries, where each dictionary is a row in the csv file processed using the template

    Returns:
        None
    """
    for user_dict in data_array:
        User.tag(user_dict)
    return None

def tag_users_parallel(data_array:list[dict]) -> None:
    """
    Tags each user as a spender or non-spender using User.tag in parallel manner and prints the result.

    Args:
        data_array: array of dictionaries, where each dictionary is a row in the csv file processed using the template

    Returns:
        None
    """

    with Pool() as pool:
        pool.map(User.tag, data_array)
    return None
