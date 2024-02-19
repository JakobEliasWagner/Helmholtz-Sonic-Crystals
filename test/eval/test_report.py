import pathlib
from typing import Dict

import pytest

from hsc import HelmholtzDataset
from hsc.eval import report


@pytest.fixture(scope="module")
def some_report():
    class TestReport(report.Report):
        @staticmethod
        def run(out_dir: pathlib.Path, data_sets: Dict[str, HelmholtzDataset]):
            pass

        def __init__(self):
            super().__init__()

    return TestReport()


def test_report_init(some_report):
    some_report.run(pathlib.Path.cwd(), {})
