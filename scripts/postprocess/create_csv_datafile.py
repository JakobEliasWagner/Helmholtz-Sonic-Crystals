import argparse
import pathlib

from loguru import logger

from hsc.preprocessing import build_pressure_dataset, build_transmission_loss_dataset

parser = argparse.ArgumentParser(
    prog="CreateCsvDatafiles",
    description="Creates CSV data files for a specific dataset.",
)

parser.add_argument("in_dir")
parser.add_argument("out_dir")
parser.add_argument("--transmission-loss", action=argparse.BooleanOptionalAction)
parser.add_argument("--pressure", action=argparse.BooleanOptionalAction)


def main(args):
    # info and setup
    in_dir = pathlib.Path.cwd().joinpath(args.in_dir)
    samples = len(list(in_dir.glob("*.xdmf")))
    out_dir = pathlib.Path.cwd().joinpath(args.out_dir)
    total_files = 0
    if args.transmission_loss:
        logger.info("Selected to create transmission loss dataset.")
        total_files += 1
    if args.pressure:
        logger.info("Selected to create pressure dataset.")
        total_files += 1
    logger.info(
        f"Creating a total of {total_files} files in {out_dir} from {in_dir} containing a total of {samples} samples."
    )

    # transmission loss dataset (faster)
    if args.transmission_loss:
        logger.info("Start building transmission loss dataset.")
        build_transmission_loss_dataset(in_dir=in_dir, out_dir=out_dir)
        logger.info("Finished building transmission loss dataset.")

    # pressure dataset (very slow)
    if args.pressure:
        logger.info("Start building pressure dataset.")
        build_pressure_dataset(in_dir=in_dir, out_dir=out_dir)
        logger.info("Finished building pressure dataset.")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
