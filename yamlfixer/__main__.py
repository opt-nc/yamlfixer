# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 OPT-NC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Execute yamlfixer from the command line."""

import sys
import os
import argparse

from . import __version__, __copyright__
from .yamlfixer import YAMLFixer

GPLBLURB = """
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def parse_commandline(argv=None):
    """Parse the command line and return the parsed arguments."""
    # Parse the command line arguments
    cmdline = argparse.ArgumentParser(description="Fix formatting problems in YAML documents. "
                                      "If no file is specified, then reads input from `stdin`.",
                                      epilog=f"{__copyright__}\n{GPLBLURB}",
                                      fromfile_prefix_chars="@",
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    cmdline.add_argument("-v", "--version",
                         action="version",
                         version=f"yamlfixer v{__version__}",
                         help="display this program's version number and exit.")
    mutuallyexclusive = cmdline.add_mutually_exclusive_group()
    mutuallyexclusive.add_argument("-b", "--backup",
                                   action="store_true",
                                   help="make a backup copy of original files.")
    cmdline.add_argument("-B", "--backupsuffix",
                         default=".orig",
                         help="sets the suffix for backup files, `%(default)s` is the default.")
    cmdline.add_argument("-d", "--debug",
                         action="store_true",
                         help="output debug information to stderr.")
    cmdline.add_argument("-D", "--diffto",
                         metavar="DIFF_FILE",
                         default=os.devnull,
                         help="name of the file a unified diff will be written to. Defaults to `%(default)s`.")
    cmdline.add_argument("-e", "--ext",
                         metavar="EXTENSIONS",
                         default="yaml,yml,yamllint",
                         help="comma separated list of acceptable extensions when searching "
                         "directories for YAML files. Defaults to `%(default)s`.")
    cmdline.add_argument("-f", "--forcecolors",
                         action="store_true",
                         help="force colorized output even if stream is not a TTY.")
    cmdline.add_argument("-F", "--followsymlinks",
                         action="store_true",
                         help="follow symbolic links when recursing directories.")
    cmdline.add_argument("-l", "--listfixers",
                         action="store_true",
                         help="output the list of available fixers.")
    cmdline.add_argument("-N", "--nosyntax",
                         action="store_true",
                         help="don't try to fix syntax errors.")
    mutuallyexclusive.add_argument("-n", "--nochange",
                                   action="store_true",
                                   help="don't modify anything.")
    cmdline.add_argument("-r", "--recurse",
                         metavar="LEVEL",
                         type=int,
                         default=0,
                         help="sets the maximum recursion level for directories. Default is "
                         "`%(default)i` meaning no recursion, and "
                         "any negative value means no limit.")
    mutuallyexclusive = cmdline.add_mutually_exclusive_group()
    mutuallyexclusive.add_argument("-j", "--jsonsummary",
                                   action="store_true",
                                   help="output JSON summary to stderr.")
    mutuallyexclusive.add_argument("-p", "--plainsummary",
                                   action="store_true",
                                   help="output plain text summary to stderr.")
    mutuallyexclusive.add_argument("-s", "--summary",
                                   action="store_true",
                                   help="output colorized plain text summary to stderr. "
                                   "If stderr is not a TTY output is identical to --plainsummary "
                                   "unless --forcecolors is also used.")
    cmdline.add_argument("-t", "--tabsize",
                         type=int,
                         default=2,
                         help="sets the number of spaces to replace tabs "
                         "with, default is `%(default)i`.")
    mutuallyexclusive = cmdline.add_mutually_exclusive_group()
    mutuallyexclusive.add_argument("-c", "--config-file",
                                   metavar="CONFIG_FILE",
                                   default=None,
                                   help="path to yamllint's custom configuration file, none by default.")
    mutuallyexclusive.add_argument("-C", "--config-data",
                                   metavar="CONFIG_DATA",
                                   default=None,
                                   help="custom configuration for yamllint as YAML source, none by default.")
    cmdline.add_argument("filenames",
                         nargs="*",
                         metavar="FILE_or_DIR",
                         default=["-"],  # Read from stdin if no file is specified
                         help="the YAML files to fix. Use `-` to read from `stdin`.")
    if cmdline.prog == "__main__.py":
        cmdline.prog = "yamlfixer"
    arguments = cmdline.parse_args(argv)
    if arguments.tabsize < 1:
        cmdline.error(f"invalid tabsize value '{arguments.tabsize}'")
    return arguments


def run(argv=None):
    """Run the program with an optional list of command line arguments."""
    arguments = parse_commandline(argv)
    yfixer = YAMLFixer(arguments)
    if arguments.listfixers:
        return yfixer.listfixers()
    return yfixer.fix()


if __name__ == '__main__':
    sys.exit(run())
