# Asteroid Astrometry Pipeline

AI-assisted pipeline for detecting and measuring comets and asteroids in FITS images, verifying orbits with FindOrb, and generating MPC observation reports.

## Project structure

```
src/
  image_loader.py    — FITS loading, WCS parsing, normalization
  blinker.py         — image subtraction / blinking for moving object detection
  detector.py        — PyTorch Faster R-CNN detector (fine-tunable)
  astrometry.py      — plate solving + sub-pixel centroiding
  catalog_match.py   — Gaia DR3 catalog cross-matching
  findorb_runner.py  — subprocess wrapper for find_orb binary
  mpc_formatter.py   — MPC 80-column observation line formatter
  main.py            — CLI entry point

config/config.yaml   — observatory code, thresholds, paths
tests/               — pytest unit tests
data/                — FITS images (not tracked by git)
models/              — trained .pt weights (not tracked by git)
```

## Quick start

```bash
pip install -r requirements.txt
python src/main.py /path/to/fits/images --obs-code Z99 --out report.txt
```

## Pipeline stages

1. Load FITS images with calibration (bias/dark/flat)
2. Align images and detect moving objects via image subtraction
3. Plate-solve field with astrometry.net
4. Centroid candidates, convert pixel → RA/Dec
5. Cross-match with Gaia to reject known stars
6. Verify orbit with FindOrb
7. Write MPC-formatted observation report

## Status

Work in progress — module stubs in place, implementation pending.
