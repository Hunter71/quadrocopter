import os.path
from typing import Optional

from typer import Argument, Exit, Option, Typer, echo, run

from quadrocopter import __app_name__, __version__
from quadrocopter.data_reader import DataReader
from quadrocopter.pathfinder import PathFinder

app = Typer()


@app.callback()
def main(
    filename: Optional[str] = Argument(default=None, help="Read input data from a given file"),
    version: Optional[bool] = Option(None, "--version", "-v", is_eager=True),
) -> None:
    if version:
        echo(f"{__app_name__} ver. {__version__}")
        raise Exit()

    if filename:
        if not os.path.exists(filename):
            print(f"Error: file '{filename}' does not exist ⛔️ ")
            raise Exit(code=1)

        input_data = DataReader.read_from_file(filename)
    else:
        input_data = DataReader.read_prompt()

    start_point, stop_point, transmitters = input_data

    result = PathFinder.exists_safe_path(start_point, stop_point, transmitters)
    print(f"For given {start_point=}, {stop_point=} and {transmitters=}")
    print(f"Safe flight is {'POSSIBLE 🚀 ' if result else 'NOT POSSIBLE ❌ '}")


if __name__ == "__main__":
    run(main)
