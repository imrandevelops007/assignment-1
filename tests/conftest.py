"""Shared pytest fixtures for the registration test suite.

Add reusable fixtures here as needed for Section 7 of the assignment
(e.g., a fixture providing representative student data used by multiple
tests, and a yield-based fixture that sets up and cleans up a temporary
resource).
"""

# TODO: implement your fixtures here.





import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def valid_student():
    """A representative student who is allowed to register (Section 7b).

    Values come from the valid equivalence classes:
      current_credits = 9  (CUR-V1)
      course_credits  = 3  (CC-V1)
      prerequisite_met = True (PRE-V1)
      resulting load  = 12 (TOT-V1)

    Tests start from this baseline and change ONE value, so each negative
    test isolates a single rule. A new dict is built for every test, so a
    test that changes it cannot affect any other test.
    """
    return {"current_credits": 9, "course_credits": 3, "prerequisite_met": True}


@pytest.fixture
def registration_log():
    """Yield-based fixture: a temporary log file on disk (Section 7c).

    Setup:    create a unique temporary folder and an empty CSV log file.
    Yield:    give the log file path to the test.
    Cleanup:  delete the folder.

    The cleanup is in a ``finally`` block after ``yield``, so it runs even if
    the test fails. Run ``pytest -s -m resource`` to see the SETUP and
    CLEANUP messages printed around the test.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="registration_log_"))
    log_file = tmp_dir / "registrations.csv"
    log_file.write_text("current_credits,course_credits,prerequisite_met,allowed,fee\n")
    print(f"\n[SETUP] created temporary log at {log_file}")
    try:
        yield log_file
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"\n[CLEANUP] removed {tmp_dir} (exists afterwards: {tmp_dir.exists()})")