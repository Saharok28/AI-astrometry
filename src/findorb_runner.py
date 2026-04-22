import subprocess
import os


class FindOrbRunner:

    def __init__(self, findorb_path):
        self.executable = findorb_path

    def run(self, obs_file, output_file):
        """Call find_orb binary with obs_file and capture stdout to output_file."""
        result = subprocess.run(
            [self.executable, obs_file],
            capture_output=True,
            text=True,
            check=False,
        )
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result

    def parse_elements(self, output_file):
        """Parse orbital elements from find_orb output file. Returns dict. Stub."""
        return {}
