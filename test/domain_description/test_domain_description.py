import pathlib
import tempfile

import numpy as np


def test_create_description_instance(descriptions):
    for des in descriptions:
        assert des.height == des.crystal.grid_size
        assert des.crystal_box.size[0] == des.crystal.n * des.crystal.grid_size
        assert np.allclose(des.wave_lengths, des.c / des.frequencies)
        assert np.allclose(des.ks, des.frequencies / des.c * 2.0 * np.pi)


def test_crystal_descriptions_correct(descriptions, crystal_descriptions):
    for des, c_des in zip(descriptions, crystal_descriptions):
        assert des.crystal == c_des


def test_serialize_description(descriptions):
    ds = [des.serialize() for des in descriptions]
    for o in ds:
        assert isinstance(o, dict)


def test_can_save_to_json(descriptions):
    with tempfile.TemporaryDirectory() as fp:
        fp_path = pathlib.Path(fp)

        for des in descriptions:
            des.save_to_json(fp_path)

        files = list(fp_path.glob("*.json"))

        assert len(files) == len(descriptions)
