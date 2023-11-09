# ruff: noqa: ARG001

import pytest

from tauon.expose import ExposeError, expose, get_exposed_data


def test_invalid_functions():
    def action0(arg1=1):
        pass

    def action1(arg1, arg2=1):
        pass

    def action2(**kwargs):
        pass

    table = (
        (action0, "No keyword argument allowed `arg1` on `action0`"),
        (action1, "No keyword argument allowed `arg2` on `action1`"),
        (action2, "No keyword wildcard allowed `kwargs` on `action2`"),
    )

    for sample, expected in table:
        with pytest.raises(ExposeError) as err:
            expose()(sample)
        assert str(err.value) == expected


def test_invalid_functions_py3():
    def action0(*args, arg1=1):
        pass

    def action1(arg1, *, arg2=1):
        pass

    def action2(arg1, *arg2, arg3=1):
        pass

    table = (
        (action0, "No keyword argument allowed `arg1` on `action0`"),
        (action1, "No keyword argument allowed `arg2` on `action1`"),
        (action2, "No keyword argument allowed `arg3` on `action2`"),
    )

    for sample, expected in table:
        with pytest.raises(ExposeError) as err:
            expose()(sample)
        assert str(err.value) == expected


def test_valid_functions():
    def action0():
        pass

    def action1(arg1):
        pass

    def action2(arg1, arg2):
        pass

    def action3(*arg1):
        pass

    def action4(arg1, *arg2):
        pass

    table = (
        (action0, {"aliases": ("action0",), "require": 0}),
        (action1, {"aliases": ("action1",), "require": 1}),
        (action2, {"aliases": ("action2",), "require": 2}),
        (action3, {"aliases": ("action3",), "require": 0}),
        (action4, {"aliases": ("action4",), "require": 1}),
    )

    for sample, expected in table:
        data = get_exposed_data(expose()(sample))
        assert data.aliases == expected["aliases"]
        assert data.require == expected["require"]
        assert data.description == ""
        assert data.hidden is False


def test_description():
    def action():
        """
        Some help goes here
        """

    data = get_exposed_data(expose()(action))
    assert data.description == "Some help goes here"


def test_hidding():
    @expose(hidden=True)
    def action():
        pass

    data = get_exposed_data(action)
    assert data.hidden is True


def test_expose_on_function():
    @expose("-h", "--help", description="Some help goes here")
    def action():
        pass

    data = get_exposed_data(action)
    assert data.aliases == ("-h", "--help")
    assert data.description == "Some help goes here"


def test_expose_on_method():
    class ExampleProgram:
        @expose("-h", "--help", description="Some help goes here")
        def action(self):
            pass

    data = get_exposed_data(ExampleProgram.action)
    assert data.aliases == ("-h", "--help")
    assert data.description == "Some help goes here"


def test_unexposed():
    def action():
        pass

    expected = "`action` is not exposed"
    with pytest.raises(ExposeError) as error:
        get_exposed_data(action)
    assert str(error.value) == expected
