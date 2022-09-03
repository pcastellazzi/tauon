__all__ = ["ArgumentList"]

ASSIGNMENT_SEPARATOR = "="
LONG_OPTION_SEPARATOR = "--"
SHORT_OPTION_SEPARATOR = "-"


class ArgumentList(list):
    @staticmethod
    def is_option(text):
        return text.startswith(SHORT_OPTION_SEPARATOR) or text.startswith(
            LONG_OPTION_SEPARATOR
        )

    def __init__(self, argv):
        super().__init__()
        self._normalize(argv)

    def _normalize(self, argv):
        for arg in argv:
            if arg.startswith(LONG_OPTION_SEPARATOR):
                try:
                    idx = arg.index(ASSIGNMENT_SEPARATOR)
                except ValueError:
                    self.append(arg)
                else:
                    self.append(arg[:idx])
                    self.append(arg[idx + 1 :])
            elif arg.startswith(SHORT_OPTION_SEPARATOR):
                try:
                    idx = arg.index(ASSIGNMENT_SEPARATOR)
                except ValueError:
                    options = arg[1:]
                    value = None
                else:
                    options = arg[1:idx]
                    value = arg[idx + 1 :]

                for option in options:
                    self.append(SHORT_OPTION_SEPARATOR + option)

                if value is not None:
                    self.append(value)
            else:
                self.append(arg)
