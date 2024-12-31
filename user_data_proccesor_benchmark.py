import time
from pathlib import Path
import click
import user_data_proccesor

def benchmark(tagger_func: callable, data_array:list[dict], iterations:int) -> float:
    """
    Calculates the average time taken to tag users using the tagger_func on the data_array for the given number of iterations.

    Args:
        tagger_func: a callable function that tags users as spenders or non-spenders
        data_array: array of dictionaries, where each dictionary is a row in the csv file processed using the template
        iterations: number of iterations to run the tagger_func

    Returns:
        float: the average time taken to tag users in seconds
    """
    sum_time = 0
    for i in range(iterations):
        start_time = time.time()
        tagger_func(data_array)
        sum_time += time.time() - start_time
    return sum_time / iterations

@click.command()
@click.option("--size_multiplier", type=int, default=100, help="Multiplier for the size of the data")
@click.option("--iterations", type=int, default=3, help="Number of iterations to run the benchmark")
def run_benchmark(size_multiplier:int, iterations:int) -> None:
    """
    Runs the benchmark function to compare the time taken to tag users iteratively and in parallel.

    Args:
        data_path: path to the csv data file
        template_path: path to the json template file
        iter: boolean flag to tag users iteratively or in parallel

    Returns:
        None
    """
    try:
        # [:1] is used to get the first row of the data to use as a template for the rest of the data
        # This will allow us to test performance on whicher size of data we want
        # On other circumstances, we might have wanted to draw the replicated line randomly or choose WC option
        data_as_json = user_data_proccesor.read_csv(Path("data.csv"),Path("template.json"))[:1] * size_multiplier
        iter_time = benchmark(user_data_proccesor.tag_users_iterative, data_as_json, iterations)
        parallel_time = benchmark(user_data_proccesor.tag_users_parallel, data_as_json, iterations)

    except FileNotFoundError as file_not_found_error:
        print(f"Error reading the file: {file_not_found_error}")
        exit()

    print(f"Average (over {iterations} iterations) time taken to tag users iteratively: {iter_time} seconds ")
    print(f"Average (over {iterations} iterations) time taken to tag users in parallel: {parallel_time} seconds")

    return None

if __name__ == "__main__":
    run_benchmark()
