import argparse
import pathlib
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Setup argument parser
parser = argparse.ArgumentParser(description="Plots all samples from a transmission loss csv.")
parser.add_argument("--tl-file", required=True)


def plot_transmission_loss(tl_file: pathlib.Path):
    df = pd.read_csv(tl_file)

    unique_crystals = df[["radius", "inner_radius", "gap_width"]].drop_duplicates()

    num_evals = len(df) // len(unique_crystals)

    x = np.empty((len(unique_crystals), 1, 3))
    u = x
    y = np.empty((len(unique_crystals), num_evals, 1))
    v = np.empty((len(unique_crystals), num_evals, 1))

    for i, (_, crystal) in enumerate(unique_crystals.iterrows()):
        c_df = df.loc[
            (df["radius"] == crystal["radius"])
            * (df["inner_radius"] == crystal["inner_radius"])
            * (df["gap_width"] == crystal["gap_width"])
            ]

        x[i] = np.array([crystal["radius"], crystal["inner_radius"], crystal["gap_width"]]).reshape(1, 3)
        y[i] = np.array([c_df["frequency"].to_list()]).reshape(num_evals, 1)
        v[i] = np.array([[c_df["transmission_loss"].to_list()]]).reshape(num_evals, 1)

    for xi, ui, yi, vi in zip(x, u, y, v):
        dfi = pd.DataFrame({
            "frequency": yi.squeeze(),
            "transmission loss": vi.squeeze()
        })

        fig, ax = plt.subplots()
        sns.lineplot(dfi, x="transmission loss", y="frequency", ax=ax, orient="y")
        sns.lineplot(x=[0, 0], y=[2000, 20000], c='k')
        plt.suptitle(f"{ui}")
        plt.show()
        plt.close(fig)


if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()

    # Assign variables from arguments
    tl_file = pathlib.Path.cwd().joinpath(args.tl_file)

    plot_transmission_loss(tl_file)
