import numpy as np
from scipy import ndimage


class Blinker:

    def subtract(self, img1, img2):
        """Return absolute pixel difference of two aligned images."""
        pass

    def threshold(self, diff, sigma=3.0):
        """Return binary mask where pixels exceed sigma * std(diff)."""
        pass

    def find_candidates(self, mask):
        """Return list of (x, y) pixel centroids of blobs in binary mask."""
        pass
