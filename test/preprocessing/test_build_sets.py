import pathlib
import tempfile

from hsc.preprocessing import (build_pressure_dataset,
                               build_transmission_loss_dataset)


def test_build_sets(example_dset_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_in = pathlib.Path(example_dset_dir)
        tmp_out = pathlib.Path(tmpdir).joinpath("out")

        build_pressure_dataset(tmp_in, tmp_out)
        build_transmission_loss_dataset(tmp_in, tmp_out)

        assert len(list(pathlib.Path(tmp_out).glob("*.csv"))) == 2
