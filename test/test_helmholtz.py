import pathlib
import tempfile

import pytest

from hsc import Helmholtz


@pytest.mark.slow
def test_helmholtz(example_c_domain_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = pathlib.Path(tmpdir)
        helm = Helmholtz(example_c_domain_file, tmp_dir)

        helm.run(2)

        assert len(list(tmp_dir.glob("*.xdmf"))) == 2
