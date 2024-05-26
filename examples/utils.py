import pathlib
import tarfile
import tempfile
from typing import List

import hsc


def load_tar(path: pathlib.Path) -> List[hsc.HelmholtzDataset]:
    datasets = []
    with tarfile.open(path) as tar_file:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = pathlib.Path(tmp_dir)
            tar_file.extractall(path=tmp_dir)
            for file in tmp_dir.rglob("*.xdmf"):
                datasets.append(hsc.HelmholtzDataset.from_xdmf_file(file))
    return datasets
