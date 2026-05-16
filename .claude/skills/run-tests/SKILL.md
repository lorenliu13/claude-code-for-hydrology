---
name: run-tests
description: Run pytest on the current exercise directory and report pass/fail summary
---

Run pytest on the files in the current working directory and report the results.

1. Run: `python -m pytest . -v --tb=short`
2. Report the number of tests passed, failed, and errored
3. For any failures, show the test name and the assertion error message
4. If all tests pass, confirm "All tests passing ✓"
5. If tests fail, suggest which function or file to investigate first
