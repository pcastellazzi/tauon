from pytest import mark, raises

from tauon.command import CommandError

from .fixtures import ExampleProgram0, ExampleProgram3, ExampleProgram5

TEST_ACTIONS = (
    ([], 333),
    (["sum", "1"], 445),
    (["sum", "1", "2"], 447),
    (["sum", "1", "2", "3"], 450),
    (["--sum", "1"], 556),
    (["--sum", "1", "2"], 558),
    (["--sum", "1", "2", "3"], 561),
)


def test_unknown_command():
    expected = "Unexpected command `unknown`"
    with raises(CommandError) as err:
        ExampleProgram0()(["unknown"])
    assert str(err.value) == expected


def test_unknown_option():
    expected = "Unexpected option `--unknown`"
    with raises(CommandError) as err:
        ExampleProgram0()(["--unknown"])
    assert str(err.value) == expected


def test_no_default_command():
    expected = "Missing default action on `exampleprogram0`"
    with raises(CommandError) as err:
        ExampleProgram0()([])
    assert str(err.value) == expected


def test_wrong_number_of_arguments():
    expected = "Not enough arguments for `hello`, expected `1` got `0`"
    with raises(CommandError) as err:
        ExampleProgram3()(["hello"])
    assert str(err.value) == expected


@mark.parametrize("sample, expected", TEST_ACTIONS)
def test_dispatcher(sample, expected):
    prog3 = ExampleProgram3()
    prog3(sample)
    assert prog3.total == expected


@mark.parametrize("sample, expected", TEST_ACTIONS)
def test_subcommands(sample, expected):
    prog5 = ExampleProgram5()
    prog5(["exampleprogram3"] + sample)
    assert prog5.config.subcommands[0].total == expected
