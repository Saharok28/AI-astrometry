from astropy.coordinates import Angle
import astropy.units as u


def format_mpc_line(obs_code, date_str, ra_deg, dec_deg, mag, band,
                    designation="       ", note2="C"):
    """
    Format one MPC 80-column optical CCD observation line.

    Column layout (1-indexed):
      1- 5  packed permanent number (blank if unnumbered)
      6-12  provisional designation (7 chars, e.g. 'K10V00B')
      13    discovery flag
      14    note 1
      15    note 2 ('C' = CCD)
      16-32 date: 'YYYY MM DD.ddddd ' (17 chars)
      33-44 RA:  'HH MM SS.ss ' (12 chars)
      45-56 Dec: '±DD MM SS.s ' (12 chars)
      57-65 blank (9 chars)
      66-70 magnitude (5 chars, e.g. '17.0 ')
      71    band filter
      72-77 blank (6 chars)
      78-80 observatory code

    Args:
        obs_code (str):    3-char MPC observatory code (e.g. 'Z99', '704')
        date_str (str):    'YYYY MM DD.ddddd' observation UTC date
        ra_deg (float):    Right Ascension in degrees J2000.0
        dec_deg (float):   Declination in degrees J2000.0
        mag (float|None):  Measured magnitude, or None if unknown
        band (str):        Filter letter ('R', 'V', 'G', 'w', etc.)
        designation (str): 7-char packed provisional designation (default blank)
        note2 (str):       Note 2 field — 'C' for CCD, blank for visual

    Returns:
        str: Exactly 80 characters per MPC optical observation standard.
    """
    ra = Angle(ra_deg * u.deg)
    dec = Angle(dec_deg * u.deg)

    ra_str = ra.to_string(unit=u.hourangle, sep=' ', precision=2, pad=True)
    dec_str = dec.to_string(unit=u.deg, sep=' ', precision=1,
                            alwayssign=True, pad=True)

    mag_str = f"{mag:4.1f} " if mag is not None else "     "

    line = (
        f"     "                    # cols  1- 5: no permanent number
        f"{designation:<7}"[:7]    # cols  6-12: provisional designation
        f" "                        # col  13: discovery flag
        f" "                        # col  14: note 1
        f"{note2:1}"               # col  15: note 2
        f"{date_str:<17}"[:17]     # cols 16-32: YYYY MM DD.ddddd + trailing space
        f"{ra_str:<12}"[:12]       # cols 33-44: HH MM SS.ss
        f"{dec_str:<12}"[:12]      # cols 45-56: ±DD MM SS.s
        f"         "               # cols 57-65: blank
        f"{mag_str}"               # cols 66-70: magnitude
        f"{band:1}"                # col  71: band
        f"      "                  # cols 72-77: blank
        f"{obs_code:>3}"[:3]       # cols 78-80: observatory code
    )

    return line[:80].ljust(80)
