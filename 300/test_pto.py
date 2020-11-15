import pytest

import pto
from pto import four_day_weekends


def test_four_day_weekends_invalid_call():
    with pytest.raises(ValueError) as e:
        four_day_weekends(True)
    assert str(e.value) == pto.ERROR_MSG


def test_four_day_weekends_invalid_call_custom_error_message():
    new_msg = "You're calling it wrong dude!"
    pto.ERROR_MSG = new_msg
    with pytest.raises(ValueError) as e:
        four_day_weekends(True)
    assert str(e.value) == new_msg


@pytest.fixture
def default_output(capfd):
    four_day_weekends()
    return capfd.readouterr()[0].splitlines()


@pytest.fixture
def default_workdays_output(capfd):
    four_day_weekends(show_workdays=True)
    return capfd.readouterr()[0].splitlines()


@pytest.fixture
def october_output(capfd):
    four_day_weekends(start_month=10)
    return capfd.readouterr()[0].splitlines()


@pytest.fixture
def october_workdays_output(capfd):
    four_day_weekends(start_month=10, show_workdays=True)
    return capfd.readouterr()[0].splitlines()
    

@pytest.fixture
def reduced_pto_output(capfd):
    four_day_weekends(start_month=10, paid_time_off=120)
    return capfd.readouterr()[0].splitlines()


def test_number_of_weekends_with_default(default_output):
    assert "18 Four-Day Weekends" in default_output[0]


def test_number_of_weekends_with_october(october_output):
    assert "11 Four-Day Weekends" in october_output[0]


def test_number_of_weekends_reduced_pto(reduced_pto_output):
    assert "11 Four-Day Weekends" in reduced_pto_output[0]


def test_number_of_pto_days_with_default(default_output):
    assert "200 (25 days)" in default_output[2]


def test_number_of_pto_days_with_reduced(reduced_pto_output):
    assert "120 (15 days)" in reduced_pto_output[2]


def test_pto_balance_with_default(default_output):
    assert "-88 (11 days)" in default_output[3]


def test_pto_balance_with_october(october_output):
    assert "-24 (3 days)" in october_output[3]


def test_pto_balance_with_reduced(reduced_pto_output):
    assert "-56 (7 days)" in reduced_pto_output[3]


def test_last_chance_with_default(default_output):
    assert "2020-09-18 - 2020-09-21 *" in default_output[10]


def test_last_chance_with_reduced(reduced_pto_output):
    assert "*" in reduced_pto_output[8] 


def test_last_chance_with_pto_over(capfd):
    four_day_weekends(start_month=10, paid_time_off=284)
    output = capfd.readouterr()[0].splitlines()
    for line in output:
        assert "*" not in line


def test_last_chance_with_bit_reduced_pto(capfd):
    four_day_weekends(paid_time_off=160)
    output = capfd.readouterr()[0].splitlines()
    assert "*" in output[13]


def test_last_chance_with_tiny_nonfullday_pto(capfd):
    four_day_weekends(start_month=11, paid_time_off=55)
    output = capfd.readouterr()[0].splitlines()
    assert "*" in output[7]


def test_number_of_workdays_with_default(default_workdays_output):
    assert "(23 days)" in default_workdays_output[0]


def test_number_of_workdays_with_october(october_workdays_output):
    assert "(14 days)" in october_workdays_output[0]


def test_random_october_workday(october_workdays_output):
    assert october_workdays_output[10] == "2020-12-10"


def test_random_october_weekend_off(october_output):
    assert october_output[10] == "2020-11-13 - 2020-11-16"


def test_first_workday_with_default(default_workdays_output):
    assert default_workdays_output[1] == "2020-08-03"


def test_last_workday_with_default(default_workdays_output):
    assert default_workdays_output[-1] == "2020-12-31"
