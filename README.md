tauon
=====

tauon is a library for creating command line interfaces in an object oriented way.

The following features are implemented:

* gnu style long options (--long-option, --long-option=value, --long-option value)
* gnu style short options (-s, -s=value, -s value)
* gnu style combined short options (-xvf file => -x -v -f=file)
* user defined commands
* nested commands
* per command options
* per command help
* auto generated help


```python
from tauon import Command, expose

class HelloWorld(Command):
    """We use docstring for documentation."""

    @expose('-h', '--help')
    def help(self)
        """Show help and exit."""
        print(self.get_help())
        sys.exit(1)

    @expose()
    def default(self):
        print('Hello World!')

if __name__ == '__main__':
    import sys
    app = HelloWorld()
    app(sys.argv[1:])
```

