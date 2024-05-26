import argparse
import pathlib

import numpy as np
import pandas as pd

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Splits csv file into train and test samples."
)
parser.add_argument("--tl-file", required=True)
parser.add_argument("--out-dir", type=str, default="out")
parser.add_argument("--train-frac", type=float, default=0.1)


def split_transmission_loss(
    tl_file: pathlib.Path, out_dir: pathlib.Path, test_frac: float = 0.1
):
    df = pd.read_csv(tl_file)

    crystal_cols = ["radius", "inner_radius", "gap_width"]

    unique_crystals = df[crystal_cols].drop_duplicates()
    n_observations = len(unique_crystals)

    test_crystals = unique_crystals.sample(int(np.round(n_observations * test_frac)))
    train_crystals = unique_crystals.drop(test_crystals.index)

    test_set = pd.merge(test_crystals, df, on=crystal_cols, how="left")
    train_set = pd.merge(train_crystals, df, on=crystal_cols, how="left")

    test_set.to_csv(out_dir.joinpath(f"{tl_file.name}_test.csv"), index=False)
    train_set.to_csv(out_dir.joinpath(f"{tl_file.name}_train.csv"), index=False)


if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()

    # Assign variables from arguments
    tl_file = pathlib.Path.cwd().joinpath(args.tl_file)
    out_dir = pathlib.Path.cwd().joinpath(args.out_dir)

    split_transmission_loss(tl_file, out_dir, args.train_frac)
