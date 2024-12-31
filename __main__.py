from pathlib import Path
import user_data_proccesor
import click

# Use the click library to create a command line interface for the user_data_processor.py script.
@click.command()
@click.option("--data_path", type=Path, help="Path to the csv data file")
@click.option("--template_path", type=Path, help="Path to the json template file")
@click.option("--output_path", type=Path, help="Path to the output json file")
@click.option("--iter", type=bool, default=True, help="Tag users iteratively")
def process_input(data_path:Path, template_path:Path, output_path:Path, iter:bool=True) -> None:
    """
    This function reads the data from the csv file, processes it, and writes the output to a json file.

    Args (from click options):
        data_path: path to the csv data file
        template_path: path to the json template file
        output_path: path to the output json file
        iter: boolean flag to tag users iteratively or in parallel

    Returns:
        None
    """
    data_as_json = user_data_proccesor.read_csv(data_path, template_path)

    # Make sure the output directory exists
    if output_path.parent.exists() == False:
        print("Creating output directory")
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the data to the output file
    user_data_proccesor.write_to_output(data_as_json, output_path)

    if iter:
        user_data_proccesor.tag_users_iterative(data_as_json)
    else:
        user_data_proccesor.tag_users_parallel(data_as_json)

    return None

if __name__ == "__main__":
    process_input()     
    

