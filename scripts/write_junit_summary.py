"""Write a short GitHub Actions summary from a pytest JUnit XML report."""

from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _usage() -> str:
    return "Usage: python scripts/write_junit_summary.py <report_path> <title>"


def _find_suite(root: ET.Element) -> ET.Element | None:
    if root.tag == "testsuite":
        return root
    return root.find("testsuite")


def _case_name(case: ET.Element) -> str:
    return f"{case.attrib.get('classname', '')}::{case.attrib.get('name', '')}"


def main() -> int:
    if len(sys.argv) != 3:
        print(_usage(), file=sys.stderr)
        return 1

    report_path = Path(sys.argv[1])
    title = sys.argv[2]
    summary_target = os.environ.get("GITHUB_STEP_SUMMARY")

    if not summary_target:
        print("GITHUB_STEP_SUMMARY is not set.", file=sys.stderr)
        return 1

    summary_path = Path(summary_target)

    with summary_path.open("a", encoding="utf-8") as summary:
        summary.write(f"## {title}\n\n")

        if not report_path.exists():
            summary.write("JUnit XML report was not generated.\n")
            return 0

        root = ET.parse(report_path).getroot()
        suite = _find_suite(root)

        tests = int(suite.attrib.get("tests", 0)) if suite is not None else 0
        failing_cases: list[str] = []
        skipped_cases: list[str] = []
        xfailed_cases: list[str] = []
        error_count = 0
        failure_count = 0
        for case in root.iter("testcase"):
            if case.find("failure") is not None:
                failing_cases.append(_case_name(case))
                failure_count += 1
                continue

            if case.find("error") is not None:
                failing_cases.append(_case_name(case))
                error_count += 1
                continue

            skipped_node = case.find("skipped")
            if skipped_node is None:
                continue

            skipped_type = (skipped_node.attrib.get("type") or "").strip().lower()
            if skipped_type == "pytest.xfail":
                xfailed_cases.append(_case_name(case))
            else:
                skipped_cases.append(_case_name(case))

        xfailed_count = len(xfailed_cases)
        skipped_count = len(skipped_cases)
        passed = tests - failure_count - error_count - xfailed_count - skipped_count

        summary.write("| Passed | Failed | Errors | Xfailed | Skipped |\n")
        summary.write("| --- | --- | --- | --- | --- |\n")
        summary.write(
            f"| {passed} | {failure_count} | {error_count} | {xfailed_count} | {skipped_count} |\n\n"
        )

        if failing_cases:
            summary.write("### Failed cases\n\n")
            for case_name in failing_cases[:10]:
                summary.write(f"- `{case_name}`\n")
            summary.write("\n")

        if xfailed_cases:
            summary.write("### Xfailed cases\n\n")
            for case_name in xfailed_cases[:10]:
                summary.write(f"- `{case_name}`\n")
            summary.write("\n")

        if skipped_cases:
            summary.write("### Skipped cases\n\n")
            for case_name in skipped_cases[:10]:
                summary.write(f"- `{case_name}`\n")
            summary.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
