import numpy as np

from hsc.utility import xdmf_to_numpy


def test_xml_to_numpy(example_xdmf):
    data = xdmf_to_numpy(example_xdmf)

    assert isinstance(data["Geometry"], np.ndarray)
    assert isinstance(data["Values"], np.ndarray)
    assert isinstance(data["Frequencies"], np.ndarray)
