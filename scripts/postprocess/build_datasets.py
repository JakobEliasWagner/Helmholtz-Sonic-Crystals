import argparse
import pathlib

from loguru import logger

from hsc.preprocessing import build_pressure_dataset, build_transmission_loss_dataset

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Creates csv datasets for given input dir."
)
parser.add_argument("--out-dir", default="out")
parser.add_argument("--in-dir", required=True)
parser.add_argument("--pressure", action=argparse.BooleanOptionalAction)
parser.add_argument("--tl", action=argparse.BooleanOptionalAction)


def build_datasets(data_dir: pathlib.Path, out_dir: pathlib.Path, args):
    logger.info(f"Args: {args}.")

    if args.tl:
        logger.info("Start building TL dataset.")
        build_transmission_loss_dataset(data_dir, out_dir)
    if args.pressure:
        logger.info("Start building pressure dataset.")
        build_pressure_dataset(data_dir, out_dir)


if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()

    # Assign variables from arguments
    in_dir = pathlib.Path.cwd().joinpath(args.in_dir)
    out_dir = pathlib.Path.cwd().joinpath(args.out_dir)

    build_datasets(in_dir, out_dir, args)
