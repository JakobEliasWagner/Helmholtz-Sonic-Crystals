import pathlib
import tempfile

import numpy as np
import pandas

from hsc import HelmholtzDataset


def test_load_xdmf(example_dataset):
    assert True


def test_load_comsol(example_dataset):
    with tempfile.TemporaryDirectory() as dir_handle:
        name = pathlib.Path(dir_handle).joinpath("mock_file.csv")

        df = pandas.DataFrame(
            columns=["%x", "y"]
            + [
                f"acpr2.p_t (Pa) @ freq={freq:.0f}"
                for freq in np.linspace(100, 20000, 10)
            ]
        )
        for i in range(18):
            df.loc[i] = [i, i] + [k * (1 + 1j) for k in range(10)]
        df["%x"] = df["%x"].astype(float)
        df["y"] = df["y"].astype(float)

        header = "".join(["hello\n"] * 8)

        with open(name, "w") as ict:
            ict.writelines(header)
        df.to_csv(name, header=True, mode="a", index=False)
        dset = HelmholtzDataset.from_comsol_file(name, example_dataset.description)

        assert np.allclose(dset.frequencies, np.round(np.linspace(100, 20000, 10)))
        assert np.allclose(dset.x, np.outer(np.arange(0, 18), np.ones(2)))
        assert np.allclose(dset.p, (1 + 1j) * np.outer(np.arange(10), np.ones(18)))
