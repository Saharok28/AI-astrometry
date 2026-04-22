import numpy as np
import pytest
from astropy.io import fits
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from image_loader import FitsLoader


@pytest.fixture
def sample_fits(tmp_path):
    data = np.random.rand(100, 100).astype(np.float32)
    hdu = fits.PrimaryHDU(data)
    path = tmp_path / "test.fits"
    hdu.writeto(path)
    return str(path)


def test_load_returns_header_and_data(sample_fits):
    loader = FitsLoader()
    header, data = loader.load(sample_fits)
    assert header is not None
    assert data.shape == (100, 100)


def test_load_missing_file():
    loader = FitsLoader()
    header, data = loader.load("nonexistent.fits")
    assert header is None and data is None


def test_normalize_range():
    loader = FitsLoader()
    arr = np.array([[0.0, 50.0], [100.0, 200.0]])
    norm = loader.normalize(arr)
    assert norm.min() == pytest.approx(0.0)
    assert norm.max() == pytest.approx(1.0)


def test_normalize_constant_array():
    loader = FitsLoader()
    arr = np.full((10, 10), 5.0)
    assert (loader.normalize(arr) == 0.0).all()
