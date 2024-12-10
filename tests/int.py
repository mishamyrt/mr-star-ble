"""integer utils tests"""

import pytest

from mr_star_ble.int import split_uint16


def test_split_uint16():
    """Test split_uint16"""
    assert split_uint16(0x1234) == (0x12, 0x34)
    assert split_uint16(0x0078) == (0x00, 0x78)
    assert split_uint16(0x8000) == (0x80, 0x00)

    try:
        split_uint16(-1)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True

    try:
        split_uint16(0x10000)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
