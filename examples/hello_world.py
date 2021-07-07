from tauon import Command, CommandError, expose


class HelloWorld(Command):
    """We use docstring for documentation."""

    def __init__(self):
        super().__init__()
        self.greeting = "Hello World!"

    @expose("-h", "--help")
    def help_(self):
        """Show help and exit."""
        print(self.get_help())
        sys.exit(1)

    # we don't want to show the default command when help is requested
    @expose(hidden=True)
    def default(self):
        print(self.greeting)
        sys.exit(0)


if __name__ == "__main__":
    import sys

    try:
        HelloWorld().execute(sys.argv[1:])
    except CommandError as exc:
        # we got a parsing error, print it
        print(f"ERROR: {exc}")
        sys.exit(2)
