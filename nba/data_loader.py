# The click package enables command-line interface functionality
# by using decorators to define commands and options.
# It parses command-line arguments and passes them to
# the corresponding functions, making it easy to create CLI tools.
import kaggle
import os
import json
from pathlib import Path
import click


def kaggle_api_key(
    user_name: str | None = None, api_key: str | None = None
) -> None:
    """
    Function that takes the kaggle API key as input and saves it to
    ~/.kaggle/kaggle.json if it doesn't exist
    """
    if user_name is not None and api_key is not None:
        # Create ~/.kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_dir.mkdir(parents=True, exist_ok=True)

        # Path to kaggle.json
        kaggle_json = kaggle_dir / "kaggle.json"

        # Create the JSON content
        api_config = {"username": user_name, "key": api_key}

        # Write the config file if it doesn't exist
        if not kaggle_json.exists():
            with open(kaggle_json, "w") as f:
                json.dump(api_config, f)

            # Set file permissions to be readable only by the user
            os.chmod(
                kaggle_json, 0o600
            )  # read and write permission only for the user
            print(f"Kaggle API key has been saved to {kaggle_json}")


def kaggle_download_data(dataset: str) -> None:
    """
    Function that downloads the NBA database from Kaggle
    """
    # Create the data directory if it doesn't exist
    root_path = Path(__file__).parent.parent
    data_path = root_path / "data"
    data_path.mkdir(parents=True, exist_ok=True)

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=data_path, unzip=True)
    print(f"Data has been downloaded to {data_path}")


# This decorator turns the function into
# a Click command-line interface (CLI) command.
@click.command()  # type: ignore
# This decorator defines a command-line option for the CLI command.
@click.option(  # type: ignore
    "--dataset",
    "-d",
    required=True,
    help='Kaggle dataset identifier (e.g., "username/dataset-name")',
)
# This decorator defines a command-line option for the CLI command.
@click.option(  # type: ignore
    "--user-name",
    "-u",
    required=False,
    help="Your Kaggle username",
)
# This decorator defines a command-line option for the CLI command.
@click.option(
    "--api-key", "-k", required=False, help="Your Kaggle API key"
)  # type: ignore
def main(
    dataset: str,
    user_name: str | None = None,
    api_key: str | None = None,
) -> None:
    kaggle_api_key(user_name=user_name, api_key=api_key)
    kaggle_download_data(dataset=dataset)


# This code block calls the main function
# to execute the script when it is run directly.
if __name__ == "__main__":
    main()
