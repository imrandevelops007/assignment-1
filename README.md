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