import os
import sys
import time
from datetime import datetime

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from tests.utils.excel_generator import create_excel_report


def generate_dast_excel_report(test_results, output_path=None, total_duration=0.0):
    if output_path is None:
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "test-cases", "dast_test_cases.xlsx"))

    passed = sum(1 for r in test_results if r.get("Status") == "PASS")
    failed = sum(1 for r in test_results if r.get("Status") == "FAIL")
    skipped = sum(1 for r in test_results if r.get("Status") == "SKIPPED")
    blocked = sum(1 for r in test_results if r.get("Status") == "BLOCKED")
    total = len(test_results)
    pass_rate = (passed / total * 100.0) if total > 0 else 0.0

    summary = {
        "title": "GroWise DAST Security Vulnerability Assessment Report",
        "category": "DAST Security Testing (Web Only)",
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "blocked": blocked,
        "pass_rate": pass_rate,
        "execution_time": f"{total_duration:.2f}s",
        "environment": os.environ.get("CI_ENV", "CI/CD GitHub Actions - OWASP ZAP & Security Engine"),
        "build_commit": os.environ.get("GITHUB_SHA", "main-build-latest")[:10],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "deployment_readiness": "PASS" if failed == 0 and blocked == 0 and total >= 350 else "FAIL"
    }

    categories = ["SECURITY_HEADERS", "AUTH_SECURITY", "INJECTION_ATTACKS", "XSS_SECURITY", "ACCESS_CONTROL", "INFO_DISCLOSURE", "HTTP_METHODS"]
    filepath = create_excel_report(output_path, summary, test_results, category_sheets=categories)
    print(f"[DAST EXCEL] Report saved successfully to: {filepath}")
    return filepath

