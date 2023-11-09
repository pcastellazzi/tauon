from inspect import getmembers

from .argument_list import ArgumentList
from .expose import expose, get_exposed_data, is_exposed
from .formatter import DefaultFormatter
from .util import Error, get_config

__all__ = ("Command", "CommandError")


class CommandError(Error):
    pass


class Command:
    class Config:
        description = None
        formatter = DefaultFormatter
        help = None  # noqa: A003
        subcommands = None
        label = None
        usage = None

    @staticmethod
    def dispatch(name, action, argv):
        data = get_exposed_data(action)

        if (available := len(argv)) < data.require:
            msg = f"Not enough arguments for `{name}`, expected `{data.require}` got `{available}`"

            raise CommandError(msg)

        if data.spec.varargs:
            args = argv[:]
            del argv[:]
        else:
            high = min([data.require, available])
            args = argv[:high]
            del argv[:high]

        action(*args)

    def __init__(self):
        self.config = get_config(self)
        self.commands = {}
        self.options = {}
        self.scan_actions()
        self.formatter = self.config.formatter(self)

    def __call__(self, argv):
        self.execute(argv)

    def add_action(self, action):
        for name in get_exposed_data(action).aliases:
            if ArgumentList.is_option(name):
                self.options[name] = action
            else:
                self.commands[name] = action

    def add_subcommand(self, command):
        @expose(command.get_label(), description=command.get_description()[0])
        def action(*argv):
            return command(list(argv))

        self.commands[command.get_label()] = action

    def execute(self, argv):
        args = ArgumentList(argv)
        while args:
            arg = args.pop(0)
            if ArgumentList.is_option(arg):
                if arg in self.options:
                    self.dispatch(arg, self.options[arg], args)
                else:
                    msg = f"Unexpected option `{arg}`"
                    raise CommandError(msg)
            else:
                if arg in self.commands:
                    self.dispatch(arg, self.commands[arg], args)
                    break
                msg = f"Unexpected command `{arg}`"
                raise CommandError(msg)
        else:
            if "default" in self.commands:
                self.dispatch("default", self.commands["default"], [])
            else:
                msg = f"Missing default action on `{self.get_label()}`"
                raise CommandError(msg)

    def get_description(self):
        return self.formatter.get_description()

    def get_help(self):
        return self.formatter.get_help()

    def get_label(self):
        return self.formatter.get_label()

    def get_usage(self):
        return self.formatter.get_usage()

    def scan_actions(self):
        for _, action in getmembers(self, predicate=is_exposed):
            self.add_action(action)

        if self.config.subcommands:
            for cmd in self.config.subcommands:
                self.add_subcommand(cmd)
