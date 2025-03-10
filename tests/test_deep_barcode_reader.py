"""Package level tests"""

from deep_barcode_reader import __version__


def test_version() -> None:
    """Unit test for checking the version of the code"""
    assert __version__ == "0.3.0"
