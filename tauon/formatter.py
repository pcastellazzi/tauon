import inspect
import re
from abc import ABC, abstractmethod
from textwrap import dedent

from .expose import get_exposed_data
from .util import get_config

__all__ = ["Formatter", "DefaultFormatter"]


class Formatter(ABC):
    def __init__(self, command):
        self.command = command

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_label(self):
        pass

    @abstractmethod
    def get_usage(self):
        pass

    @abstractmethod
    def get_help(self):
        pass


class DefaultFormatter(Formatter):
    class Config:
        empty_line = ""
        new_line = "\n"
        separator = ", "
        tab = " " * 4
        usage_label = "Usage"
        commands_label = "Commands"
        options_label = "Options"

    def __init__(self, command):
        super().__init__(command)
        self.config = get_config(self)
        self.visible_commands = self.get_visible_actions(self.command.commands)
        self.visible_options = self.get_visible_actions(self.command.options)

    def get_description(self):
        return self.text_to_lines(
            self.command.config.description or self.get_default_description()
        )

    def get_label(self):
        return self.command.config.label or self.get_default_label()

    def get_usage(self):
        return self.text_to_lines(self.command.config.usage or self.get_default_usage())

    def get_help(self):
        return self.command.config.help or self.get_default_help()

    def get_default_description(self):
        return inspect.getdoc(self.command.__class__)

    def get_default_label(self):
        return re.sub("Command$", "", self.command.__class__.__name__).lower()

    def get_default_usage(self):
        usage = f"{self.config.usage_label}: {self.command.get_label()}"

        if self.visible_options:
            usage += f" [{self.config.options_label.lower()}]"

        if self.visible_commands:
            usage += f" [{self.config.commands_label.lower()}]"

        return usage

    def get_default_help(self):
        blocks = (
            self.command.get_usage(),
            self.command.get_description(),
            self.get_options_help(),
            self.get_commands_help(),
        )

        lines = []
        for block in blocks:
            if block:
                lines.append(self.config.empty_line)
                lines.extend(block)

        lines.append(self.config.empty_line)

        return self.config.new_line.join(lines)

    def get_commands_help(self):
        return self.get_actions_help(self.config.commands_label, self.visible_commands)

    def get_options_help(self):
        return self.get_actions_help(self.config.options_label, self.visible_options)

    def get_actions_help(self, title, actions):
        if not actions:
            return None

        text = [f"{title}:"]
        for action in actions:
            text.append(self.get_action_description(action))

        return text

    def get_action_description(self, method, ljust=40):
        data = get_exposed_data(method)
        args = " ".join(data.spec.args)

        if data.spec.varargs:
            if args:
                args = f"{args} *{data.spec.varargs}"
            else:
                args = f"*{data.spec.varargs}"

        description = self.config.tab + self.config.separator.join(data.aliases)

        if args:
            description = description + " " + args

        if data.description:
            description = description.ljust(ljust) + data.description

        return description  # noqa: R504

    def get_visible_actions(self, actions):
        # pylint: disable=no-self-use
        visible_actions = [
            actions[key] for key in actions if not get_exposed_data(actions[key]).hidden
        ]

        return sorted(
            set(visible_actions), key=lambda action: get_exposed_data(action).aliases[0]
        )

    def text_to_lines(self, text):
        if text:
            return dedent(text).strip().split(self.config.new_line)
        return []
