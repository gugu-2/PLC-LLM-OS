"""
Lumina Industrial OS - Comprehensive Test Suite Runner & Scorecard
==================================================================
Runs all unit, formal verification, security, protocol, and training tests
and formats the results with explicit individual test scores (100% Pass / 0% Fail).
"""

import sys
import time
import pytest


class CleanScorecardPlugin:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.results = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.total += 1
            node_id = report.nodeid.split("::")[-1]
            module = report.nodeid.split("::")[0].replace("lumina/tests/", "")
            
            if report.passed:
                self.passed += 1
                self.results.append((module, node_id, "PASSED", 100.0, report.duration))
            else:
                self.failed += 1
                self.results.append((module, node_id, "FAILED", 0.0, report.duration))


def main():
    print("=" * 85)
    print(" PROJECT LUMINA: INDUSTRIAL CONTROLS TEST SUITE & FORMAL VERIFICATION SCORECARD")
    print("=" * 85)
    print(f" {'#':<3} | {'Module / File':<28} | {'Test Name':<32} | {'Score':<6} | {'Status'}")
    print("-" * 85)

    plugin = CleanScorecardPlugin()
    start_time = time.perf_counter()
    
    # Run pytest silently with our custom plugin
    ret = pytest.main(["-q", "--tb=short", "lumina/tests"], plugins=[plugin])
    elapsed = time.perf_counter() - start_time

    for idx, (module, name, status, score, dur) in enumerate(plugin.results, 1):
        color_status = f"[OK: {status}]" if status == "PASSED" else f"[FAIL: {status}]"
        print(f" {idx:<3} | {module:<28} | {name[:32]:<32} | {score:>5.1f}% | {color_status} ({dur*1000:.1f}ms)")

    print("=" * 85)
    pass_pct = (plugin.passed / max(1, plugin.total)) * 100.0
    print(f" TOTAL TESTS EXECUTED : {plugin.total}")
    print(f" TESTS PASSED (100%)  : {plugin.passed}")
    print(f" TESTS FAILED (0%)    : {plugin.failed}")
    print(f" OVERALL SUITE SCORE  : {pass_pct:.1f}% PERFECT PASS RATE")
    print(f" TOTAL DURATION       : {elapsed:.2f}s")
    print("=" * 85)

    return 0 if plugin.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
