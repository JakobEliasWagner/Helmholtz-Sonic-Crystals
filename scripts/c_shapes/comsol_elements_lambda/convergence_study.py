import argparse
import pathlib

import numpy as np
from tqdm import tqdm

from hsc.domain_properties import (
    AdiabaticAbsorberDescription,
    CShapeDescription,
    Description,
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

F = np.array([4.8e3])
C = 343.0
RHO = 1.2
WAVE_LENGTH = C / F

N_ELEMENTS = np.linspace(10, 15, 31).tolist()


def perform_study():
    descriptions = []
    for freq, wl in zip(F, WAVE_LENGTH):
        for ne in N_ELEMENTS:
            absorber_des = AdiabaticAbsorberDescription(
                depth=3.0 * wl, degree=3, round_trip=1e-25
            )
            descriptions.append(
                Description(
                    np.array([freq]),
                    RHO,
                    C,
                    n_left=1.0,
                    n_right=1.0,
                    elements_per_lambda=ne,
                    absorber=absorber_des,
                    crystal=CShapeDescription(
                        grid_size=22e-3,
                        n=10,
                        radius=6.5e-3,
                        inner_radius=5e-3,
                        gap_width=2e-3,
                    ),
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
