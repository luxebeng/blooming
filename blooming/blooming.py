#!/usr/bin/env python3
"""
This file uses docopt with the built in cmd module to realize entry point as an
interactive command application.

Usage:
blooming upgrade_image <image_name>
blooming l2ng_testcase
blooming (-i | --interactive)
blooming (-h | --help | --version)

Options:
-i, --interactive  Interactive Mode
-h, --help  Show this screen and exit.
"""
import cmd
import sys

from docopt import DocoptExit, docopt

from .image_upgrade import imageupgrade
from .l2ng_testcase import l2ng_testcase


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(blooming) '
    file = None

    @docopt_cmd
    def do_upgrade_image(self, arg):
        """Usage: upgrade_image <image_name>"""

        file = arg['<image_name>']
        imageupgrade(file)

    @docopt_cmd
    def do_l2ng_testcase(self):
        """Usage: l2ng_testcase"""

        l2ng_testcase()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


def main():
    opt = docopt(__doc__, sys.argv[1:], version='1.0.6')

    if opt['--interactive']:
        MyInteractive().cmdloop()
    elif opt['upgrade_image']:
        file = opt['<image_name>']
        imageupgrade(file)
    elif opt['l2ng_testcase']:
        l2ng_testcase()


if __name__ == "__main__":
    main()
