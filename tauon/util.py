from inspect import getmro

__all__ = ("Error", "get_config")


class Error(Exception):
    pass


class Config:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def get_config(instance):
    parameters = {}

    for parent in reversed(getmro(instance.__class__)):
        if hasattr(parent, "Config"):
            for key, value in parent.Config.__dict__.items():
                if not key.startswith("_"):  # skip private variables
                    parameters[key] = value

    return Config(**parameters)
