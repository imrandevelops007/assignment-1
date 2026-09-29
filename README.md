# Assignment 1 — Course Registration System (Starter Code)

This is the starter code for SE 413/513 Assignment 1. The business logic in
`src/registration.py` is complete and **must not be modified** — your task
is to design and implement the test suite in `tests/`.

## Project layout

```
assignment-1/
|-- src/registration.py        (provided — do not modify)
|-- tests/test_registration.py (implement your tests here)
|-- tests/conftest.py          (implement your fixtures here)
|-- pyproject.toml
|-- README.md
```

## Setup

1. (Recommended) Create and activate a virtual environment:

   ```
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. Install pytest:

   ```
   pip install pytest
   ```

## Running the tests

From the project root:

```
pytest
```

`pyproject.toml` already registers four pytest markers you may use:
`unit`, `positive`, `negative`, and `boundary` (you may register additional
markers of your own if useful). Once you've applied markers to your tests
(Section 8 of the assignment), you can run subsets, e.g.:

```
pytest -m positive
pytest -m boundary
```

## Notes

- Do not modify `src/registration.py`. If you believe there is a defect in
  it, contact the instructor rather than changing it yourself.
- `registration` is importable directly in your tests (no `src.` prefix
  needed), e.g. `from registration import can_register`.



## Section 4: Equivalence Partitioning

### 4(a) Equivalence-partition table

Classes are derived from the specified rules, not arbitrary ranges. Each class
is a set of inputs the specification says must be handled the same way.

**`can_register(current_credits, course_credits, prerequisite_met)`**

| Input / condition | Class ID | Class | Valid? | Expected result |
|---|---|---|---|---|
| `current_credits` | CUR-V1 | 0 ≤ current ≤ 15 | Valid | may register (if other rules hold) |
| | CUR-I1 | current < 0 | Invalid | `False` |
| | CUR-I2 | current > 15 | Invalid | `False` |
| `course_credits` | CC-V1 | 1 ≤ course ≤ 4 | Valid | may register (if other rules hold) |
| | CC-I1 | course < 1 (0 or negative) | Invalid | `False` |
| | CC-I2 | course > 4 | Invalid | `False` |
| `prerequisite_met` | PRE-V1 | `True` | Valid | may register (if other rules hold) |
| | PRE-I1 | `False` | Invalid | `False` |
| Resulting load (`current + course`) | TOT-V1 | total ≤ 18 | Valid | may register (if other rules hold) |
| | TOT-I1 | total > 18 | Invalid | `False` |

**`calculate_registration_fee(total_credits)`**

| Input | Class ID | Class | Valid? | Expected result |
|---|---|---|---|---|
| `total_credits` | FEE-V1 | 0 ≤ total ≤ 12 | Valid | `100 × total` |
| | FEE-V2 | 13 ≤ total ≤ 18 | Valid | `1200 + 75 × (total − 12)` |
| | FEE-I1 | total < 0 | Invalid | raises `ValueError` |
| | FEE-I2 | total > 18 | Invalid | raises `ValueError` |

The valid fee range is split into two classes (FEE-V1 and FEE-V2) because the
specification applies a different rate to each: $100/credit up to 12 credits,
and $75/credit for credits above 12.

**Observation on the resulting-load rule:** since `current_credits` is at most 15
and `course_credits` is at most 4, the largest total reachable with otherwise-valid
inputs is 15 + 4 = 19. The invalid class TOT-I1 therefore has exactly one reachable
member, (15, 4). It is the only input that exercises the "does not exceed 18" rule
on its own, so it must be tested explicitly.

### 4(b) Representative values

| Class ID | Representative value(s) | Why this value |
|---|---|---|
| CUR-V1 | 9 | mid-range, clearly valid, not near either edge |
| CUR-I1 | −5 | clearly below 0 |
| CUR-I2 | 20 | clearly above 15 |
| CC-V1 | 3 | mid-range course size |
| CC-I1 | 0 | a zero-credit course (not a real course) |
| CC-I2 | 10 | clearly above 4 |
| PRE-V1 | `True` | only possible value |
| PRE-I1 | `False` | only possible value |
| TOT-V1 | (9, 3) → total 12 | valid load, well under the cap |
| TOT-I1 | (15, 4) → total 19 | the only reachable over-limit combination |
| FEE-V1 | 6 | inside the $100/credit range |
| FEE-V2 | 15 | inside the $75/credit range |
| FEE-I1 | −10 | clearly below 0 |
| FEE-I2 | 25 | clearly above 18 |

**Why these values give useful coverage without testing every input:**

- By definition, every value in an equivalence class should be handled the same
  way, so one representative per class is enough to detect a defect that affects
  the whole class, such as a missing or inverted check.
- Mid-range values are chosen on purpose so they are *not* also boundaries. If
  one fails, the failure clearly belongs to the class, not to an edge case. The
  edges themselves are covered separately in Section 5 (boundary-value analysis).
- In negative tests, all other inputs are held at valid values so that **only one
  rule is broken at a time**. Otherwise, one rule returning `False` early could
  hide a missing check for another rule. For example, (20, 3, True) tests only
  CUR-I2, and (9, 3, False) tests only PRE-I1.
- This reduces an effectively unlimited input space to about 14 representative
  values, while still exercising every rule in the specification.


  


## Section 5: Boundary-Value Analysis

### 5(a) + 5(b) Boundaries, neighboring values, and expected behavior

Each boundary is tested at **just below / on / just above**. The other inputs are
held at safe valid values so only the boundary under test can change the result:
`course_credits = 1` when testing current-credit edges, `current_credits = 5` when
testing course-credit edges, and `prerequisite_met = True` throughout.

**`can_register`**

| Boundary | Test value | Expected | Reason |
|---|---|---|---|
| `current_credits` lower edge (0) | −1 | `False` | below valid range |
| | **0** | `True` | minimum valid value |
| | 1 | `True` | just inside |
| `current_credits` upper edge (15) | 14 | `True` | just inside |
| | **15** | `True` | maximum valid value (15 + 1 = 16 ≤ 18) |
| | 16 | `False` | above valid range |
| `course_credits` lower edge (1) | 0 | `False` | below valid range |
| | **1** | `True` | minimum valid value |
| | 2 | `True` | just inside |
| `course_credits` upper edge (4) | 3 | `True` | just inside |
| | **4** | `True` | maximum valid value |
| | 5 | `False` | above valid range |
| Resulting load edge (18) | 13 + 4 = 17 | `True` | just under the cap |
| | **14 + 4 = 18** | `True` | exactly on the cap |
| | **15 + 3 = 18** | `True` | on the cap, reached from the maximum current load |
| | 15 + 4 = 19 | `False` | exceeds 18 |

**`calculate_registration_fee`**

| Boundary | Test value | Expected | Reason |
|---|---|---|---|
| Valid-range lower edge (0) | −1 | `ValueError` | below valid range |
| | **0** | $0 | minimum valid value |
| | 1 | $100 | just inside |
| Rate transition (12) | 11 | $1,100 | last credits fully at $100 |
| | **12** | $1,200 | all 12 credits at $100 |
| | 13 | $1,275 | 1,200 + 1 × 75, first credit at $75 |
| Valid-range upper edge (18) | 17 | $1,575 | 1,200 + 5 × 75 |
| | **18** | $1,650 | maximum valid value: 1,200 + 6 × 75 |
| | 19 | `ValueError` | above valid range |

### 5(c) How a wrong comparison operator would be revealed

An off-by-one operator mistake only changes behavior **at the boundary value itself**.
Every mid-range value from Section 4 still gives the correct result, so only a
boundary test can expose the defect. Examples:

- Writing `0 < current_credits` instead of `0 <= current_credits` would wrongly
  reject a student with 0 credits. The test at **current = 0** (expected `True`)
  would fail.
- Writing `course_credits < 4` instead of `<= 4` would reject every 4-credit
  course. The test at **course = 4** would fail.
- Writing `total >= 18` instead of `total > 18` would reject a load of exactly 18.
  The tests at **14 + 4** and **15 + 3** would fail.
- Writing `0 <= total_credits < 18` for the fee would make 18 credits raise
  `ValueError`. The test at **total = 18** (expected $1,650) would fail.

**The fee transition at 12 is a special case.** If `total_credits <= 12` were
mistakenly written as `< 12`, the value 12 would go through the $75 branch and give
1,200 + 0 × 75 = $1,200, which is the same answer. No test can detect this change
because the behavior is identical, so it is not a real
defect. It shows that **13**, the first value where the two rates give different
results, is the value that actually verifies the rate change. That is why 11, 12
and 13 are all tested.





## Sections 6–7: Where each requirement is implemented

All tests are in `tests/test_registration.py`; fixtures are in `tests/conftest.py`.

| Requirement | Implemented in |
|---|---|
| 6(a) Positive registration tests | `test_registration_allowed_for_valid_load_with_prerequisite_met`, `test_registration_allowed_for_every_valid_course_size_when_load_is_low`, `test_valid_student_baseline_is_allowed_to_register` |
| 6(b) Negative registration tests | `test_registration_rejected_when_prerequisite_not_met`, `test_registration_rejected_when_current_credits_outside_0_to_15`, `test_registration_rejected_when_course_credits_outside_1_to_4`, `test_registration_rejected_when_total_credits_exceed_18`, `test_registration_rejected_when_multiple_rules_broken` |
| 6(c) Fee below / at / above 12 | `test_fee_calculated_below_at_and_above_12_credit_transition`, `test_fee_boundaries` |
| 6(d) Invalid fee inputs with `pytest.raises(ValueError)` | `test_fee_raises_value_error_just_outside_valid_range`, `test_fee_raises_value_error_for_invalid_credit_totals` |
| 7(a) `@pytest.mark.parametrize` | Used for every group of similar cases, including all equivalence-class and boundary tests. Each case has a readable `ids=` label. |
| 7(b) Reusable fixture used by ≥ 2 tests | `valid_student` in `conftest.py`, used by 3 tests |
| 7(c) Yield fixture with setup and cleanup | `registration_log` in `conftest.py`, used by `test_registration_outcomes_can_be_logged_to_temp_file` |

`registration_log` creates a uniquely named temporary folder with a CSV file,
`yield`s the file to the test, then deletes the folder. The cleanup code is in a
`finally` block after the `yield`, so pytest runs it whether the test passes or
fails.

---

## Section 8: Organizing and running the test suite

### 8(a) Markers

The four pre-registered markers are applied, plus one I added (registered in `pyproject.toml`):

| Marker | Meaning | Tests |
|---|---|---|
| `unit` | every test in the file (applied module-wide with `pytestmark`) | 57 |
| `positive` | valid / expected-success scenarios | 13 |
| `negative` | invalid input / expected-failure scenarios | 20 |
| `boundary` | boundary values from Section 5 | 25 |
| `resource` | *(added)* uses the temporary on-disk yield fixture | 1 |

A test can carry more than one marker. For example, the fee tests at −1 and 19
are both `negative` and `boundary`.

### 8(b) Commands

Run from the project root, with the virtual environment activated:

```
pytest                              # full suite (57 tests)
pytest -v                           # full suite, one line per test case
pytest -m positive                  # positive tests only
pytest -m negative                  # negative tests only
pytest -m boundary                  # boundary-value tests only
pytest -m "negative and boundary"   # invalid values just outside a valid range
pytest -m "not boundary"            # everything except the boundary tests
pytest -s -m resource               # shows the fixture's SETUP / CLEANUP messages
```

### 8(c) Evidence that the full suite passes

```
(.venv) PS E:\assignment-1> pytest
===================================== test session starts ======================================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: E:\assignment-1
configfile: pyproject.toml
testpaths: tests
collected 57 items

tests\test_registration.py .........................................................      [100%]

====================================== 57 passed in 0.30s ======================================
```

Setup and cleanup of the yield fixture (`pytest -s -m resource`):

```
[SETUP] created temporary log at C:\Users\USER\AppData\Local\Temp\registration_log_aa72jyyq\registrations.csv
.
[CLEANUP] removed C:\Users\USER\AppData\Local\Temp\registration_log_aa72jyyq (exists afterwards: False)
=============================== 1 passed, 56 deselected in 0.03s ===============================
```

### How the suite avoids test dependencies and state leakage

- **Function-scoped fixtures.** `valid_student` builds a new dictionary for every
  test. When a test changes it (e.g. sets `prerequisite_met = False`), only that
  test's copy is affected. There is no shared, module-level mutable data.
- **Pure functions under test.** `can_register` and `calculate_registration_fee`
  keep no state between calls, so calling them in one test cannot affect another.
- **Isolated temporary resource.** `registration_log` gives each test its own
  uniquely named folder (`tempfile.mkdtemp`) and always deletes it afterwards, so
  nothing is left on disk for a later test to find.
- **No ordering assumptions.** Every test sets up everything it needs itself and
  never relies on another test having run first, so the tests can run in any
  order or individually (e.g. `pytest -m boundary`) and still pass.