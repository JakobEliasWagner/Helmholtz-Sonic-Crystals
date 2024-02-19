import pathlib
import tempfile

import pytest
from eval import PressureReport


@pytest.mark.slow
def test_pressure_report(example_dataset):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        PressureReport.run(
            tmp_dir_path,
            data_sets={"example": example_dataset, "example 2": example_dataset},
        )

        assert tmp_dir_path.joinpath("pressure").is_dir()
        assert len(list(tmp_dir_path.rglob("*.pdf"))) == 1
