from textwrap import dedent

from tauon import Command, expose

__all__ = (
    "ExampleProgram0",
    "ExampleProgram1",
    "ExampleProgram2",
    "ExampleProgram3",
    "ExampleProgram4",
    "ExampleProgram5",
    "ExampleProgram6",
)


class ExampleProgram0(Command):
    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram0
        """
    )


class ExampleProgram1(Command):
    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram1 [commands]

        Commands:
            command1 *arg1
        """
    )

    @expose()
    def command1(self, *arg1):
        pass


class ExampleProgram2(Command):
    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram2 [options]

        Options:
            -h, --help
        """
    )

    @expose("-h", "--help")
    def help(self):
        pass


class ExampleProgram3(Command):
    """
    This program do magic.
    We support multiline descriptions.
    """

    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram3 [options] [commands]

        This program do magic.
        We support multiline descriptions.

        Options:
            -s, --sum arg1 *arg2                Sum all values

        Commands:
            hello name
            sum arg1 *arg2                      Sum all values
        """
    )

    def __init__(self):
        super().__init__()
        self.total = 333

    @expose(hidden=True)
    def default(self):
        pass

    @expose()
    def hello(self, name):
        pass

    @expose("sum", description="Sum all values")
    def cmdsum(self, arg1, *arg2):
        self.total = 444 + int(arg1) + sum(int(i) for i in arg2)

    @expose("-s", "--sum", description="Sum all values")
    def optsum(self, arg1, *arg2):
        self.total = 555 + int(arg1) + sum(int(i) for i in arg2)


class ExampleProgram4(Command):
    EXPECTED_DESCRIPTION = "banana"

    class Config:
        help = "banana"
        label = "banana"
        description = "banana"


class ExampleProgram5(Command):
    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram5 [commands]

        Commands:
            exampleprogram3 *argv               This program do magic.
        """
    )

    class Config:
        subcommands = (ExampleProgram3(),)


class ExampleProgram6(Command):
    EXPECTED_DESCRIPTION = dedent(
        """
        Usage: exampleprogram6
        """
    )

    @expose(hidden=True)
    def hidden_command(self):
        pass

    @expose("-H", "--hidden", hidden=True)
    def hidden_option(self):
        pass
