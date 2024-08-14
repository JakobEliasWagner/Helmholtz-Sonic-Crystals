import argparse
import pathlib
import shutil

from hsc import Helmholtz

# Setup argument parser
parser = argparse.ArgumentParser(description="Creates a dataset for given input file.")
parser.add_argument("--output_dir", required=True, default="out/test")
parser.add_argument("--input_file", required=True, default="domain.ini")
parser.add_argument("--n_threads", required=False, default=1)

# Parse arguments
args = parser.parse_args()

# Assign variables from arguments
in_file = pathlib.Path(args.input_file).resolve()
out_dir = pathlib.Path(args.output_dir).resolve()
n_threads = int(args.n_threads)


def create_dataset(description_file: pathlib.Path, output_dir: pathlib.Path):
    """Creates a dataset for the given description and saves the results to a directory.

    :param description_file: path to the description file in ini format
    :param output_dir: directory to which the result directory is written
    :return:
    """
    # properties of the entire run
    shutil.copy(description_file, output_dir.joinpath(description_file.name))

    # generate data and save it
    data_generator = Helmholtz(description_file, output_dir)
    data_generator.run(n_threads)


if __name__ == "__main__":
    create_dataset(in_file, out_dir)
