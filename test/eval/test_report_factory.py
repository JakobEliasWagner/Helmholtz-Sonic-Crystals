import pathlib
import tempfile

import pytest

from hsc.eval import AllReportsFactory


@pytest.mark.slow
def test_gap_report(example_dataset):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir).joinpath("out")
        fac = AllReportsFactory(
            {
                "example": example_dataset,
                "example 2": example_dataset,
                "example 3": example_dataset,
            },
            tmp_dir_path,
        )
        fac.run()

        assert len(list(tmp_dir_path.rglob("*.pdf"))) == 13
