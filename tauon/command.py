import inspect

from .argument_list import ArgumentList
from .expose import expose, get_exposed_data, isexposed
from .formatter import DefaultFormatter  # pylint: disable=deprecated-module
from .util import Error, get_config

__all__ = ["Command", "CommandError"]


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
            if name.startswith("-"):
                self.options[name] = action
            else:
                self.commands[name] = action

    def add_subcommand(self, command):
        @expose(command.get_label(), description=command.get_description()[0])
        def action(*argv):
            return command(list(argv))

        self.commands[command.get_label()] = action

    def dispatch(self, name, action, argv):
        # pylint: disable=no-self-use
        data = get_exposed_data(action)
        available = len(argv)

        if available < data.require:
            raise CommandError(
                f"Not enough arguments for `{name}`, expected `{data.require}` got `{available}`"
            )

        if data.spec.varargs:
            args = argv[:]
            del argv[:]
        else:
            high = min([data.require, available])
            args = argv[:high]
            del argv[:high]

        action(*args)

    def execute(self, argv):
        args = ArgumentList(argv)
        while args:
            arg = args.pop(0)
            if arg.startswith("-"):
                if arg in self.options:
                    self.dispatch(arg, self.options[arg], args)
                else:
                    raise CommandError(f"Unexpected option `{arg}`")
            else:
                if arg in self.commands:
                    self.dispatch(arg, self.commands[arg], args)
                    break
                raise CommandError(f"Unexpected command `{arg}`")
        else:
            if "default" in self.commands:
                self.dispatch("default", self.commands["default"], [])
            else:
                raise CommandError(f"Missing default action on `{self.get_label()}`")

    def get_description(self):
        return self.formatter.get_description()

    def get_help(self):
        return self.formatter.get_help()

    def get_label(self):
        return self.formatter.get_label()

    def get_usage(self):
        return self.formatter.get_usage()

    def scan_actions(self):
        for _, action in inspect.getmembers(self, predicate=isexposed):
            self.add_action(action)

        if self.config.subcommands:
            for cmd in self.config.subcommands:
                self.add_subcommand(cmd)
