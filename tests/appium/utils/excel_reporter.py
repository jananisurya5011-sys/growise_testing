import os
import sys
import time
from datetime import datetime

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from tests.utils.excel_generator import create_excel_report


def generate_appium_excel_report(test_results, output_path=None, total_duration=0.0):
    if output_path is None:
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "test-cases", "appium_test_cases.xlsx"))

    passed = sum(1 for r in test_results if r.get("Status") == "PASS")
    failed = sum(1 for r in test_results if r.get("Status") == "FAIL")
    skipped = sum(1 for r in test_results if r.get("Status") == "SKIPPED")
    blocked = sum(1 for r in test_results if r.get("Status") == "BLOCKED")
    total = len(test_results)
    pass_rate = (passed / total * 100.0) if total > 0 else 0.0

    summary = {
        "title": "GroWise Appium Mobile Automation Test Report",
        "category": "Appium Mobile Testing",
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "blocked": blocked,
        "pass_rate": pass_rate,
        "execution_time": f"{total_duration:.2f}s",
        "environment": os.environ.get("CI_ENV", "CI/CD GitHub Actions - Android Emulation"),
        "build_commit": os.environ.get("GITHUB_SHA", "main-build-latest")[:10],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "deployment_readiness": "PASS" if failed == 0 and blocked == 0 and total >= 351 else "FAIL"
    }

    categories = ["UI_UX", "FUNCTIONAL", "UNIT", "VALIDATION", "NEGATIVE", "REGRESSION", "E2E", "DEPLOYABILITY"]
    filepath = create_excel_report(output_path, summary, test_results, category_sheets=categories)
    print(f"[APPIUM EXCEL] Report saved successfully to: {filepath}")
    return filepath

