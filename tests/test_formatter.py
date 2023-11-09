import pytest

from .fixtures import (
    ExampleProgram0,
    ExampleProgram1,
    ExampleProgram2,
    ExampleProgram3,
    ExampleProgram4,
    ExampleProgram5,
    ExampleProgram6,
)


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        (ExampleProgram0, []),
        (
            ExampleProgram3,
            ["This program do magic.", "We support multiline descriptions."],
        ),
        (ExampleProgram4, ["banana"]),
    ],
)
def test_description(sample, expected):
    assert sample().get_description() == expected


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        (ExampleProgram0, ExampleProgram0.EXPECTED_DESCRIPTION),
        (ExampleProgram1, ExampleProgram1.EXPECTED_DESCRIPTION),
        (ExampleProgram2, ExampleProgram2.EXPECTED_DESCRIPTION),
        (ExampleProgram3, ExampleProgram3.EXPECTED_DESCRIPTION),
        (ExampleProgram4, ExampleProgram4.EXPECTED_DESCRIPTION),
        (ExampleProgram5, ExampleProgram5.EXPECTED_DESCRIPTION),
        (ExampleProgram6, ExampleProgram6.EXPECTED_DESCRIPTION),
    ],
)
def test_help(sample, expected):
    assert sample().get_help() == expected


@pytest.mark.parametrize(
    ("sample", "expected"),
    [(ExampleProgram0, "exampleprogram0"), (ExampleProgram4, "banana")],
)
def test_label(sample, expected):
    assert sample().get_label() == expected


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        (ExampleProgram0, "Usage: exampleprogram0"),
        (ExampleProgram1, "Usage: exampleprogram1 [commands]"),
        (ExampleProgram2, "Usage: exampleprogram2 [options]"),
        (ExampleProgram3, "Usage: exampleprogram3 [options] [commands]"),
        (ExampleProgram4, "Usage: banana"),
    ],
)
def test_usage(sample, expected):
    assert sample().get_usage() == [expected]
