import astropy.io.fits as fits
from astropy.wcs import WCS
import numpy as np


class FitsLoader:

    def load(self, filepath):
        """Return (header, data) from a FITS file."""
        try:
            with fits.open(filepath) as hdul:
                # some telescopes store image data in extension [1], not [0]
                idx = next((i for i, h in enumerate(hdul) if h.data is not None), 0)
                header = hdul[idx].header
                data = hdul[idx].data
            return header, data
        except FileNotFoundError:
            print(f"Error: file not found — {filepath}")
            return None, None
        except Exception as e:
            print(f"Error opening FITS: {e}")
            return None, None

    def get_wcs(self, header):
        """Return WCS object parsed from FITS header."""
        try:
            return WCS(header)
        except Exception as e:
            print(f"Error building WCS: {e}")
            return None

    def normalize(self, data):
        """Min-max normalize array to [0, 1]."""
        lo, hi = np.min(data), np.max(data)
        if hi == lo:
            return np.zeros_like(data, dtype=float)
        return (data - lo) / (hi - lo)
