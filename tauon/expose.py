import functools
import inspect

from .util import Error

__all__ = ("ExposedData", "expose", "get_exposed_data", "is_exposed", "ExposeError")


class CustomArgSpecError(Error):
    pass


class CustomArgSpec:
    def __init__(self, func):
        self.func = func
        self.name = None
        self.args = []
        self.keywords = None
        self.varargs = None
        self.defaults = ()

        self._get_arg_spec()

        if inspect.ismethod(func) or (self.args and self.args[0] == "self"):
            del self.args[0]

    def _get_arg_spec(self):
        parameters = inspect.signature(self.func).parameters.values()
        for param in parameters:
            if param.kind == param.POSITIONAL_ONLY:
                self.args.append(param.name)
            elif param.kind == param.KEYWORD_ONLY:
                self.args.append(param.name)
                self.defaults += (param.default,)
            elif param.kind == param.POSITIONAL_OR_KEYWORD:
                self.args.append(param.name)
                if param.default is not param.empty:
                    self.defaults += (param.default,)
            elif param.kind == param.VAR_KEYWORD:
                self.keywords = param.name
            elif param.kind == param.VAR_POSITIONAL:
                self.varargs = param.name
            else:
                raise CustomArgSpecError(f"Unknown parameter kind: `{param.kind}`")


MARK = "_exposed_data"


class ExposeError(Error):
    pass


class ExposedData:
    def __init__(self, spec, aliases=None, description=None, hidden=None):
        self.aliases = aliases or ("default",)
        self.description = description or ""
        self.hidden = hidden or False
        self.spec = spec

    @property
    def require(self):
        return len(self.spec.args) if self.spec.args else 0


class ExposedFunction:
    def __init__(self, *aliases, description=None, hidden=False):
        self._aliases = tuple(aliases)
        self._description = description
        self._hidden = hidden

    def __call__(self, routine):
        if not self._aliases:
            self._aliases = (routine.__name__,)

        if not self._description:
            self._description = inspect.getdoc(routine)

        spec = CustomArgSpec(routine)

        if spec.defaults:
            kwarg = spec.args[-len(spec.defaults)]
            raise ExposeError(
                f"No keyword argument allowed `{kwarg}` on `{routine.__name__}`"
            )

        if spec.keywords:
            raise ExposeError(
                f"No keyword wildcard allowed `{spec.keywords}` on `{routine.__name__}`"
            )

        setattr(
            routine,
            MARK,
            ExposedData(
                aliases=self._aliases,
                description=self._description,
                hidden=self._hidden,
                spec=spec,
            ),
        )

        return functools.wraps(routine)(routine)


def expose(*aliases, **kwargs):
    return ExposedFunction(*aliases, **kwargs)


def get_exposed_data(routine):
    try:
        return getattr(routine, MARK)
    except AttributeError as exc:
        name = routine.__name__ if hasattr(routine, "__name__") else repr(routine)
        raise ExposeError(f"`{name}` is not exposed") from exc


def is_exposed(routine):
    return hasattr(routine, MARK)
