
# -*- coding: utf-8 -*-
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

def run():
    """Main function."""
    # Ensure we read from stdin in case it's redirected
    if ("-" not in sys.argv[1:]) and not sys.stdin.isatty():
        sys.argv.append("-")

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
    cmdline.add_argument("-l", "--listfixers",
                         action="store_true",
                         help="output the list of available fixers.")
    mutuallyexclusive.add_argument("-n", "--nochange",
                                   action="store_true",
                                   help="don't modify anything.")
    mutuallyexclusive = cmdline.add_mutually_exclusive_group()
    mutuallyexclusive.add_argument("-j", "--jsonsummary",
                                   action="store_true",
                                   help="output JSON summary to stderr.")
    mutuallyexclusive.add_argument("-p", "--plainsummary",
                                   action="store_true",
                                   help="output plain text summary to stderr.")
    mutuallyexclusive.add_argument("-s", "--summary",
                                   action="store_true",
                                   help="output colored plain text summary to stderr. "
                                   "If stderr is not a TTY output is identical to --plainsummary.")
    cmdline.add_argument("-t", "--tabsize",
                         type=int,
                         default=2,
                         help="sets the number of spaces to replace tabs "
                         "with, default is %(default)i.")
    cmdline.add_argument("filenames",
                         nargs="*",
                         metavar="file",
                         default=["-"], # Read from stdin if no file is specified
                         help="the YAML files to fix. Use `-` to read from `stdin`.")
    if cmdline.prog == "__main__.py":
        cmdline.prog = "yamlfixer"
    arguments = cmdline.parse_args()
    yfixer = YAMLFixer(arguments)
    if arguments.listfixers:
        return yfixer.listfixers()
    return yfixer.fix()

if __name__ == '__main__':
    sys.exit(run())
