"""
Entry point — run the full asteroid astrometry pipeline on a folder of FITS images.
"""
import argparse
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Asteroid astrometry pipeline")
    p.add_argument("image_dir", help="Directory with FITS images")
    p.add_argument("--obs-code", required=True, help="MPC observatory code")
    p.add_argument("--out", default="report.txt", help="Output MPC report file")
    return p.parse_args()


def main():
    args = parse_args()
    print(f"[pipeline] images:   {args.image_dir}")
    print(f"[pipeline] obs code: {args.obs_code}")
    print("[pipeline] not implemented yet — fill in module stubs first")
    sys.exit(0)


if __name__ == "__main__":
    main()
