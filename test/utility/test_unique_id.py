import pytest

from hsc.utility import UniqueId


def test_custom_seed():
    with pytest.warns(UserWarning):
        uid = UniqueId(seed=42)
    print(uid)
