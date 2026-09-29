"""Test suite for src/registration.py.

This file is intentionally left for you to implement. See the assignment
handout for the required test-design work:

  - Section 4: Equivalence partitioning
  - Section 5: Boundary-value analysis
  - Section 6: Positive and negative testing with pytest
  - Section 7: Parametrization and fixtures
  - Section 8: Organize and demonstrate the test suite (markers, README)

`registration` is importable directly (see pyproject.toml's `pythonpath`
setting), e.g.:

    from registration import can_register, calculate_registration_fee
"""

# TODO: implement your tests here.



import pytest

from registration import calculate_registration_fee, can_register

# Every test in this file is a fast, isolated unit test.
pytestmark = pytest.mark.unit



# 6(a) can_register - POSITIVE tests

@pytest.mark.positive
@pytest.mark.parametrize(
    "current, course",
    [
        (9, 3),    # typical student, typical course (CUR-V1, CC-V1, TOT-V1)
        (0, 1),    # new student, smallest course
        (12, 2),   # full-time student adding a small course
        (14, 4),   # heavy load, largest course, total exactly 18
    ],
    ids=["typical-load", "first-course", "full-time-plus-2", "heavy-load-reaches-18"],
)
def test_registration_allowed_for_valid_load_with_prerequisite_met(current, course):
    assert can_register(current, course, True) is True


@pytest.mark.positive
@pytest.mark.parametrize("course", [1, 2, 3, 4])
def test_registration_allowed_for_every_valid_course_size_when_load_is_low(course):
    # CC-V1 has only four values, so test all of them.
    assert can_register(5, course, True) is True



# 6(b) can_register - NEGATIVE tests


@pytest.mark.negative
@pytest.mark.parametrize(
    "current, course",
    [(0, 1), (9, 3), (14, 4)],
    ids=["new-student", "typical-student", "heavy-load"],
)
def test_registration_rejected_when_prerequisite_not_met(current, course):
    # Everything else is valid; only PRE-I1 is violated.
    assert can_register(current, course, False) is False


@pytest.mark.negative
@pytest.mark.parametrize(
    "current",
    [-5, -1, 16, 20],
    ids=["well-below-0", "just-below-0", "just-above-15", "well-above-15"],
)
def test_registration_rejected_when_current_credits_outside_0_to_15(current):
    # CUR-I1 and CUR-I2
    assert can_register(current, 1, True) is False


@pytest.mark.negative
@pytest.mark.parametrize(
    "course",
    [-1, 0, 5, 10],
    ids=["negative-course", "zero-credit-course", "just-above-4", "well-above-4"],
)
def test_registration_rejected_when_course_credits_outside_1_to_4(course):
    # CC-I1 and CC-I2
    assert can_register(5, course, True) is False


@pytest.mark.negative
def test_registration_rejected_when_total_credits_exceed_18():
    # 15 + 4 = 19. Both inputs are valid on their own, so ONLY the
    # resulting-load rule (TOT-I1) can reject this.
    assert can_register(15, 4, True) is False


@pytest.mark.negative
def test_registration_rejected_when_multiple_rules_broken():
    # Over the credit limit AND missing prerequisite: still rejected.
    assert can_register(15, 4, False) is False



# can_register BOUNDARY tests


@pytest.mark.boundary
@pytest.mark.parametrize(
    "current, expected",
    [
        (-1, False), (0, True), (1, True),     # lower edge of current_credits
        (14, True), (15, True), (16, False),   # upper edge of current_credits
    ],
    ids=["cur=-1", "cur=0", "cur=1", "cur=14", "cur=15", "cur=16"],
)
def test_current_credits_boundaries(current, expected):
    # course=1 keeps the total <= 16, so only the 0..15 rule matters.
    assert can_register(current, 1, True) is expected


@pytest.mark.boundary
@pytest.mark.parametrize(
    "course, expected",
    [
        (0, False), (1, True), (2, True),      # lower edge of course_credits
        (3, True), (4, True), (5, False),      # upper edge of course_credits
    ],
    ids=["course=0", "course=1", "course=2", "course=3", "course=4", "course=5"],
)
def test_course_credits_boundaries(course, expected):
    # current=5 keeps the total <= 10, so only the 1..4 rule matters.
    assert can_register(5, course, True) is expected


@pytest.mark.boundary
@pytest.mark.parametrize(
    "current, course, expected",
    [
        (13, 4, True),    # total 17: just below the cap
        (14, 4, True),    # total 18: on the cap
        (15, 3, True),    # total 18: on the cap, from the max current load
        (15, 4, False),   # total 19: just above the cap
    ],
    ids=["total=17", "total=18(14+4)", "total=18(15+3)", "total=19"],
)
def test_resulting_credit_load_boundary_at_18(current, course, expected):
    assert can_register(current, course, True) is expected



# 6(c) calculate_registration_fee - POSITIVE tests


@pytest.mark.positive
@pytest.mark.parametrize(
    "total, expected_fee",
    [
        (6, 600.0),     # FEE-V1: below the 12-credit transition
        (12, 1200.0),   # at the transition: all credits at $100
        (15, 1425.0),   # FEE-V2: above the transition: 1200 + 3*75
    ],
    ids=["below-12", "at-12", "above-12"],
)
def test_fee_calculated_below_at_and_above_12_credit_transition(total, expected_fee):
    assert calculate_registration_fee(total) == pytest.approx(expected_fee)


@pytest.mark.positive
def test_fee_returns_float():
    assert isinstance(calculate_registration_fee(10), float)


@pytest.mark.boundary
@pytest.mark.parametrize(
    "total, expected_fee",
    [
        (0, 0.0), (1, 100.0),                         # lower edge of valid range
        (11, 1100.0), (12, 1200.0), (13, 1275.0),     # rate change at 12
        (17, 1575.0), (18, 1650.0),                   # upper edge of valid range
    ],
    ids=["fee@0", "fee@1", "fee@11", "fee@12", "fee@13", "fee@17", "fee@18"],
)
def test_fee_boundaries(total, expected_fee):
    assert calculate_registration_fee(total) == pytest.approx(expected_fee)



# 6(d) calculate_registration_fee - NEGATIVE tests


@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize("total", [-1, 19], ids=["just-below-0", "just-above-18"])
def test_fee_raises_value_error_just_outside_valid_range(total):
    with pytest.raises(ValueError, match="between 0 and 18"):
        calculate_registration_fee(total)


@pytest.mark.negative
@pytest.mark.parametrize(
    "total",
    [-10, 25, 100],
    ids=["far-below-0", "far-above-18", "absurdly-large"],
)
def test_fee_raises_value_error_for_invalid_credit_totals(total):
    # FEE-I1 and FEE-I2
    with pytest.raises(ValueError):
        calculate_registration_fee(total)






# Section 7 - Fixture-driven test

@pytest.mark.positive
def test_valid_student_baseline_is_allowed_to_register(valid_student):
    assert can_register(**valid_student) is True


@pytest.mark.negative
def test_valid_student_rejected_once_prerequisite_removed(valid_student):
    valid_student["prerequisite_met"] = False   # changes only this test's copy
    assert can_register(**valid_student) is False


@pytest.mark.negative
def test_valid_student_rejected_when_course_pushes_load_over_18(valid_student):
    valid_student["current_credits"] = 15
    valid_student["course_credits"] = 4
    assert can_register(**valid_student) is False


@pytest.mark.resource
def test_registration_outcomes_can_be_logged_to_temp_file(registration_log):
    """Uses the yield fixture: a temp file created before, removed after."""
    scenarios = [(9, 3, True), (15, 4, True), (0, 1, False)]
    with registration_log.open("a") as log:
        for current, course, prereq in scenarios:
            allowed = can_register(current, course, prereq)
            fee = calculate_registration_fee(current + course) if allowed else ""
            log.write(f"{current},{course},{prereq},{allowed},{fee}\n")

    rows = registration_log.read_text().strip().splitlines()
    assert rows[0].startswith("current_credits")          # header from setup
    assert rows[1:] == [
        "9,3,True,True,1200.0",
        "15,4,True,False,",
        "0,1,False,False,",
    ]