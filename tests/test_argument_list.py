import pytest

from tauon.argument_list import ArgumentList


@pytest.mark.parametrize(
    ("actual", "expected"),
    [
        (["--long-option"], ["--long-option"]),
        (["--long-option", "value"], ["--long-option", "value"]),
        (["--long-option="], ["--long-option", ""]),
        (["--long-option=value"], ["--long-option", "value"]),
        (["--long-option=long value"], ["--long-option", "long value"]),
    ],
)
def test_long_options(actual, expected):
    assert ArgumentList(actual) == expected


@pytest.mark.parametrize(
    ("actual", "expected"),
    [
        (["-s"], ["-s"]),
        (["-s", "value"], ["-s", "value"]),
        (["-s="], ["-s", ""]),
        (["-s=value"], ["-s", "value"]),
        (["-s=long value"], ["-s", "long value"]),
        (["-abc=value"], ["-a", "-b", "-c", "value"]),
    ],
)
def test_short_options(actual, expected):
    assert ArgumentList(actual) == expected
