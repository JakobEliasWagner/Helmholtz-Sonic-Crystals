import argparse
import pathlib

import numpy as np
from tqdm import tqdm

from hsc.domain_properties import (
    AdiabaticAbsorberDescription,
    Description,
    NoneDescription,
)
from hsc.solver import HelmholtzSolver

# Setup argument parser
parser = argparse.ArgumentParser(description="Creates a convergence sturdy.")
parser.add_argument("--output_dir", required=True)
parser.add_argument("--input_file", required=False)  # ignored
parser.add_argument("--n_threads", required=False, default=1)  # ignored

# Parse arguments
args = parser.parse_args()

# Assign variables from arguments
out_dir = pathlib.Path(args.output_dir).resolve()

N_ELEMENTS = 15

F = np.linspace(2e3, 20e3, 31)
C = 343.0
RHO = 1.2
WAVE_LENGTH = C / F


def perform_study():
    descriptions = []
    absorber_des = AdiabaticAbsorberDescription(
        depth=3 * max(WAVE_LENGTH), degree=3, round_trip=1e-25
    )
    descriptions.append(
        Description(
            F,
            RHO,
            C,
            n_left=1.0,
            n_right=1.0,
            elements_per_lambda=N_ELEMENTS,
            absorber=absorber_des,
            crystal=NoneDescription(grid_size=22e-3, n=10),
        )
    )

    # setup
    solver = HelmholtzSolver(out_dir=out_dir, element=("CG", 2))

    # solve all domains
    for description in tqdm(descriptions):
        solver(description)
        description.save_to_json(out_dir)


if __name__ == "__main__":
    perform_study()
