import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mpc_formatter import format_mpc_line


def test_line_is_80_chars():
    line = format_mpc_line("704", "2025 04 22.12345", 56.75, 24.1167, 17.0, "R")
    assert len(line) == 80


def test_obs_code_at_cols_78_80():
    line = format_mpc_line("Z99", "2025 04 22.12345", 56.75, 24.1167, 17.0, "R")
    assert line[77:80] == "Z99"


def test_band_at_col_71():
    line = format_mpc_line("704", "2025 04 22.12345", 56.75, 24.1167, 17.0, "V")
    assert line[70] == "V"


def test_note2_ccd_at_col_15():
    line = format_mpc_line("704", "2025 04 22.12345", 56.75, 24.1167, 17.0, "R")
    assert line[14] == "C"


def test_unknown_magnitude():
    line = format_mpc_line("704", "2025 04 22.12345", 56.75, 24.1167, None, "R")
    assert len(line) == 80
    assert line[65:70] == "     "
