__all__ = ["ArgumentList"]


class ArgumentList(list):
    def __init__(self, argv):
        super().__init__()
        self._normalize(argv)

    def _normalize(self, argv):
        for arg in argv:
            if arg[0:2] == "--":
                try:
                    idx = arg.index("=")
                except ValueError:
                    self.append(arg)
                else:
                    self.append(arg[:idx])
                    self.append(arg[idx + 1 :])
            elif arg[0] == "-":
                try:
                    idx = arg.index("=")
                except ValueError:
                    options = arg[1:]
                    value = None
                else:
                    options = arg[1:idx]
                    value = arg[idx + 1 :]

                for option in options:
                    self.append("-" + option)

                if value is not None:
                    self.append(value)
            else:
                self.append(arg)
