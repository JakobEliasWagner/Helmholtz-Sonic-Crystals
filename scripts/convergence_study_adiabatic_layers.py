import pathlib
import argparse
from tqdm import tqdm
from hsc.solver import HelmholtzSolver
from hsc.domain_properties import Description, AdiabaticAbsorberDescription, NoneDescription
import numpy as np

# Setup argument parser
parser = argparse.ArgumentParser(description="Creates a covnergence sturdy.")
parser.add_argument("--output_dir", required=True)
parser.add_argument("--input_file", required=False)  # ignored
parser.add_argument("--n_threads", required=False, default=1)  # ignored

# Parse arguments
args = parser.parse_args()

# Assign variables from arguments
out_dir = pathlib.Path(args.output_dir).resolve()

N_LAMBDAS = np.linspace(.5, 10, 10)
DEGREES = (1, 2, 3, 4, 5, 6, 7)

F = 1000.
C = 343.
RHO = 1.2


def perform_study():
    descriptions = []

    for degree in DEGREES:
        for n_lambda in N_LAMBDAS:
            absorber_des = AdiabaticAbsorberDescription(
                depth=n_lambda,
                degree=degree
            )
            descriptions.append(
                Description(
                    np.array([F]),
                    RHO,
                    C,
                    n_left=.5,
                    n_right=.5,
                    elements_per_lambda=15,
                    absorber=absorber_des,
                    crystal=NoneDescription(
                        22e-3,
                        n=10
                    )
                )
            )

    # setup
    solver = HelmholtzSolver(out_dir=out_dir, element=("CG", 2))

    # solve all domains
    for description in tqdm(descriptions):
        solver(description)
        description.save_to_json(out_dir)


if __name__ == '__main__':
    perform_study()
