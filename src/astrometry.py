from astropy.wcs import WCS
import numpy as np


class PlateSolver:

    def solve(self, image_path, ra_hint=None, dec_hint=None, radius_deg=1.0):
        """Submit FITS to astrometry.net and return solved WCS header. Stub."""
        raise NotImplementedError

    def centroid(self, data, x, y, box=15):
        """Return sub-pixel (cx, cy) centroid via intensity-weighted moments."""
        half = box // 2
        y0, y1 = max(0, y - half), min(data.shape[0], y + half + 1)
        x0, x1 = max(0, x - half), min(data.shape[1], x + half + 1)
        patch = data[y0:y1, x0:x1].astype(float)
        patch -= patch.min()
        total = patch.sum() or 1.0
        ys, xs = np.mgrid[y0:y1, x0:x1]
        return float((xs * patch).sum() / total), float((ys * patch).sum() / total)

    def pixel_to_sky(self, wcs, x, y):
        """Convert pixel (x, y) to SkyCoord using provided WCS."""
        return wcs.pixel_to_world(x, y)
