import os
import sys

# Entrypoint for DAST testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tests.dast.test_cases.test_dast_runner import run_dast_test_suite

if __name__ == "__main__":
    sys.exit(run_dast_test_suite())

