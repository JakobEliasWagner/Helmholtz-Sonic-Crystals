import pathlib
import tempfile

import pytest
from eval import GapReport


@pytest.mark.slow
def test_gap_report(example_dataset):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        GapReport.run(
            tmp_dir_path,
            data_sets={
                "example": example_dataset,
                "example 2": example_dataset,
                "example 3": example_dataset,
            },
        )

        assert tmp_dir_path.joinpath("tl_gaps").is_dir()
        assert len(list(tmp_dir_path.rglob("*.pdf"))) == 10
