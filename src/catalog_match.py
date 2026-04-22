from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u


class CatalogMatcher:

    def query_gaia(self, center: SkyCoord, radius_deg=0.5, mag_limit=19.0):
        """Query Gaia DR3 around center and return astropy Table. Stub."""
        raise NotImplementedError

    def match(self, detections: list, catalog_coords: SkyCoord,
              tolerance_arcsec=3.0):
        """
        Cross-match detected SkyCoords with catalog.
        Returns (matched_detections, matched_catalog, unmatched_detections). Stub.
        """
        raise NotImplementedError
