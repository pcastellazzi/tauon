__all__ = ("ArgumentList",)

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
                if (idx := arg.find(ASSIGNMENT_SEPARATOR)) > 0:
                    self.append(arg[:idx])
                    self.append(arg[idx + 1 :])
                else:
                    self.append(arg)
            elif arg.startswith(SHORT_OPTION_SEPARATOR):
                if (idx := arg.find(ASSIGNMENT_SEPARATOR)) > 0:
                    options = arg[1:idx]
                    value = arg[idx + 1 :]
                else:
                    options = arg[1:]
                    value = None
                for option in options:
                    self.append(SHORT_OPTION_SEPARATOR + option)
                if value is not None:
                    self.append(value)
            else:
                self.append(arg)
