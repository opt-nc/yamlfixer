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

"""yamlfixer's main class."""

import sys
import os
import json

from .constants import FIX_PASSEDLINTER, FIX_MODIFIED, FIX_SKIPPED, FIX_PERMERROR
from .constants import EXIT_OK, EXIT_NOK
from .filefixer import FileFixer
from .problemfixer import ProblemFixer

COLORSEQ = {"PASSED": "38;2;0;255;0m",
            "MODIFIED": "38;2;0;0;255m",
            "SKIPPED": "38;2;255;0;255m",
            "ERROR": "38;2;255;0;0m",
            "UNKNOWN": "38;2;255;255;0m",
           }

class YAMLFixer:
    """To hold files fixing logic."""
    def __init__(self, arguments):
        """Initialize the fixer for all files."""
        self.arguments = arguments
        self.passed = self.modified \
            = self.skipped \
            = self.permerrors \
            = self.unknown = 0
        self.summary = []

    def info(self, message): # pylint: disable=no-self-use
        """Output an informational message to stderr."""
        sys.stderr.write(f"{message}\n")

    def debug(self, message):
        """Output a debug message to stderr if debug mode is active."""
        if self.arguments.debug:
            sys.stderr.write(f"DEBUG: {message}\n")

    def error(self, message): # pylint: disable=no-self-use
        """Output an error message to stderr."""
        sys.stderr.write(f"ERROR: {message}\n")

    def statistics(self):
        """Output some statistics."""
        if self.arguments.summary or self.arguments.plainsummary:
            self.info(f"Files to fix: {len(self.arguments.filenames)}")
            self.info(f"{self.passed} files successfully passed yamllint strict mode")
            self.info(f"{self.modified} files were modified")
            self.info(f"{self.skipped} files were skipped")
            self.info(f"{self.permerrors} files were not writeable")
            self.info(f"{self.unknown} files with unknown status")
            for (status, filename, issues, handled) in self.summary:
                if issues:
                    msg = f" (handled {handled}/{issues})"
                else:
                    msg = ""
                if self.arguments.summary and sys.stderr.isatty():
                    status = f"\033[{COLORSEQ.get(status.strip(), '0m')}{status}\033[0m"
                self.info(f"{status} {filename}{msg}")
            if self.arguments.nochange:
                message = "WARNING: No file was modified per user's request !"
                if self.arguments.summary and sys.stderr.isatty():
                    self.info(f"\033[38;2;255;0;0m{message}\033[0m")
                else:
                    self.info(f"{message}")
        elif self.arguments.jsonsummary:
            summarymapping = {"filestofix": len(self.arguments.filenames),
                              "passedstrictmode": self.passed,
                              "modified": self.modified,
                              "skipped": self.skipped,
                              "notwriteable": self.permerrors,
                              "unknown": self.unknown,
                              "details": {},
                              "nochangemode": self.arguments.nochange,
                             }
            for (status, filename, issues, handled) in self.summary:
                summarymapping["details"][filename] = {"status": status.strip(),
                                                       "issues": issues,
                                                       "handled": handled,
                                                      }
            self.info(json.dumps(summarymapping, indent=4))

    def listfixers(self):
        """List all the available fixers."""
        availablefixers = []
        for methodname in [m for m in dir(ProblemFixer) if m.startswith('fix_')]:
            docstring = getattr(ProblemFixer, methodname).__doc__
            for prob in [pb.strip()[2:] for pb in docstring.splitlines()[1:]]:
                if prob:
                    availablefixers.append(prob)
        self.info("fixers:")
        for fixstr in sorted(availablefixers):
            self.info(f"  - {fixstr}")
        return EXIT_OK

    def fix(self):
        """Fix all files."""
        for filename in self.arguments.filenames:
            if filename == '-':
                absfilename = '<stdin>'
            else:
                absfilename = os.path.abspath(filename)
            filetofix = FileFixer(self, filename)
            # pylint: disable=no-member
            self.debug(f"Fixing {absfilename} ... ")
            status = filetofix.fix()
            if status == FIX_PASSEDLINTER:
                self.debug(f"passed linter's strict mode.")
                txtstatus = "  PASSED"
                self.passed += 1
            elif status == FIX_MODIFIED:
                self.debug(f"was modified.")
                txtstatus = "MODIFIED"
                self.modified += 1
            elif status == FIX_SKIPPED:
                self.debug(f"was skipped.")
                txtstatus = " SKIPPED"
                self.skipped += 1
            elif status == FIX_PERMERROR:
                self.debug(f"was not writeable.")
                txtstatus = "   ERROR"
                self.permerrors += 1
            else:
                self.error(f"unknown fixing status [{status}]")
                txtstatus = " UNKNOWN"
                self.unknown += 1
            self.summary.append((txtstatus,
                                 absfilename,
                                 filetofix.issues,
                                 filetofix.issueshandled))

        self.statistics()
        if (self.passed + self.skipped) == len(self.arguments.filenames):
            return EXIT_OK
        return EXIT_NOK
