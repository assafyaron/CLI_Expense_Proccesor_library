# CLI Tool For Proccessing User Expenses 

## From A Bird's View

This program implements a libary designed to process user expenses given in a CSV file into a json template. Each User will be tagged and printed as a spender\non-spender based on their expenses vs. salary.

## Design Decisions

Logic and file structure allow modularity. Changes in template will not cause changes in code.

Inconsisent compatability between json and CSV files will cause exit() since the output will make no sense.

On the other hand, 'glitching' lines in the CSV will only be reported and raise exceptions allowing the user to still recover the 'majorly' correct output file.

## File Structure

- `template.json`: The JSON template used to structure the user data.
- `data.csv`: The CSV file containing the user data.
- `output.json`: The output file where the processed data will be saved.
- `__main__.py`: The main Python script that processes our data using the user_data_proccesor libray.
- `user_data_proccesor.py`: Libary created for processing user data from a CSV file and tagging users as spenders or non-spenders.
- `user_data_proccesor_benchmark.py`: Compares runtimes between iterative and parallel tagging.
- `user_data_proccesor_tester.py`: Runs tests on user_data_proccesor library.

## Setup

Make sure to install click libary

```
pip install click
```

## Usage

1. **Interfacing commandline**:
    Run the CLI use the following command:  
    ```
    python .\__main__.py --data_path="data.csv" --template_path="template.json" --output_path="output.json"
    ```
    To run parallely use:
    ```
    python .\__main__.py --data_path="data.csv" --template_path="template.json" --output_path="output.json" --iter=False
    ```

2. **View Output**: The output will be written to `output.json`, and the console will display which users are tagged as spenders or non-spenders.

## Benchmarking

Using `user_data_proccessor_benchmark` we compare runtime of two methods for tagging users:
1. **Iterative Tagging**: Processes each user sequentially.
2. **Parallel Tagging**: Uses multiple processes to tag users concurrently, improving performance for larger datasets.

We derived to the conclusion that tagging parallely granted us 5X speed up.

Run benchmark function using:

```
python .\user_data_proccesor_benchmark.py --size_multiplier=100 --iterations=3
```
## Testing

Using `user_data_proccessor_tester`. In the command line run:
```
python .\user_data_proccesor_tester.py
```

## Example Workflow

1. **Input CSV (`data.csv`)**:
    ```csv
    name,salary,food_expenses,clothing_expenses
    Haim,2000,500,300
    Yossi,1500,700,600
    Hagit,1800,200,100
    ```

2. **Template (`template.json`)**:
    ```json
    {
        "user": {
            "name": "{name}",
            "salary": "{salary}"
        },
        "expenses": {
            "food": "{food}",
            "clothing": "{clothing}"
        },
        "welcome_message": "Hello {name}, welcome"
    }
    ```

3. **Output JSON (`output.json`)**:
    ```json
    [
        {
            "user": {
                "name": "Haim",
                "salary": 2000
            },
            "expenses": {
                "food": 500,
                "clothing": 300
            },
            "welcome_message": "Hello Haim, welcome"
        },
        {
            "user": {
                "name": "Yossi",
                "salary": 1500
            },
            "expenses": {
                "food": 700,
                "clothing": 600
            },
            "welcome_message": "Hello Yossi, welcome"
        },
        {
            "user": {
                "name": "Hagit",
                "salary": 1800
            },
            "expenses": {
                "food": 200,
                "clothing": 100
            },
            "welcome_message": "Hello Hagit, welcome"
        }
    ]
    ```

4. **Console Output**:
    ```bash
    Haim is a spender
    Yossi is a spender
    Hagit is not a spender
    ```
