import os
import sys

# Entrypoint for load testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tests.load.test_cases.test_load_runner import run_load_test_suite

if __name__ == "__main__":
    sys.exit(run_load_test_suite())

