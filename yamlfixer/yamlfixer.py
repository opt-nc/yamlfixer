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

"""yamlfixer's main class."""

import os
import json

from .constants import FIX_PASSEDLINTER, FIX_MODIFIED, FIX_FIXED, FIX_SKIPPED, FIX_PERMERROR
from .constants import EXIT_OK, EXIT_NOK
from .common import YAMLFixerBase
from .filefixer import FileFixer
from .problemfixer import ProblemFixer

STATUSCOLORS = {"PASSED": "green",
                "MODIFIED": "blue",
                "FIXED": "lime",
                "SKIPPED": "magenta",
                "ERROR": "red",
                "UNKNOWN": "yellow"}


class YAMLFixer(YAMLFixerBase):  # pylint: disable=too-many-instance-attributes
    """To hold files fixing logic."""
    def __init__(self, arguments):
        """Initialize the fixer for all files."""
        super().__init__(arguments)
        self.debug(f"arguments={repr(self.arguments)}")
        self.extensions = [f".{e.strip()}" for e in self.arguments.ext.split(",")]
        self.passed = self.modified \
            = self.fixed \
            = self.skipped \
            = self.permerrors \
            = self.unknown = 0
        self.summary = []
        self.filenames = self.generate_unique_filenames(self.arguments.filenames)

    def matchesext(self, filename):
        """Returns True if filename matches the set of extensions, else False."""
        for ext in self.extensions:
            if filename.endswith(ext):
                return True
        return False

    def recurse(self, path, fnmapping, level=0):
        """Find all files in a directory recursively."""
        self.debug(f"SCAN [{path}] at level {level} with limit {self.arguments.recurse}")
        if (self.arguments.recurse < 0) or (level <= self.arguments.recurse):
            try:
                with os.scandir(path) as dircontents:
                    for entry in dircontents:
                        if entry.is_file() and self.matchesext(entry.name):
                            # Ensures uniqueness based on absolute path
                            fnmapping[os.path.abspath(entry.path)] = entry.path
                        elif entry.is_dir(follow_symlinks=False):
                            self.recurse(entry.path, fnmapping, level+1)
            except PermissionError:
                pass

    def generate_unique_filenames(self, fnames):
        """Generate a list of unique filenames."""
        fnmapping = {}
        for name in fnames:
            # os.path.isdir() returns False instead of raising an exception
            # if we don't have sufficient permissions, so we have to do
            # a workaround to skip such directories
            try:
                os.path.getsize(name)
            except PermissionError:
                pass
            except FileNotFoundError:
                if name == '-':  # For <stdin>
                    fnmapping[name] = name
            else:
                if os.path.isdir(name):
                    self.recurse(name, fnmapping)
                else:
                    # Ensures uniqueness based on absolute path
                    fnmapping[os.path.abspath(name)] = name
        return sorted(fnmapping.values())

    def statistics(self):
        """Output some statistics."""
        if self.arguments.summary or self.arguments.plainsummary:
            self.info(f"Files to fix: {len(self.filenames)}")
            self.info(f"{self.passed} files were already correct before")
            self.info(f"{self.modified} files were modified but problems remain")
            self.info(f"{self.fixed} files were entirely fixed")
            self.info(f"{self.skipped} files were skipped")
            self.info(f"{self.permerrors} files were not writeable")
            self.info(f"{self.unknown} files with unknown status")
            for (status, filename, issues, handled) in self.summary:
                if issues:
                    msg = f" (handled {handled}/{issues})"
                else:
                    msg = ""
                if self.arguments.summary:
                    try:
                        status = self.colorize(status, STATUSCOLORS[status.strip()])
                    except KeyError:
                        pass
                self.info(f"{status} {filename}{msg}")
            if self.arguments.nochange:
                message = "No file was modified per user's request !"
                if self.arguments.summary:
                    self.warning(message)
                else:
                    self.info(f"WARNING: {message}")  # Ensure it's not colored
        elif self.arguments.jsonsummary:
            summarymapping = {"filestofix": len(self.filenames),
                              "passedstrictmode": self.passed,
                              "modified": self.modified,
                              "fixed": self.fixed,
                              "skipped": self.skipped,
                              "notwriteable": self.permerrors,
                              "unknown": self.unknown,
                              "details": {},
                              "nochangemode": self.arguments.nochange}
            for (status, filename, issues, handled) in self.summary:
                summarymapping["details"][filename] = {"status": status.strip(),
                                                       "issues": issues,
                                                       "handled": handled}
            self.info(json.dumps(summarymapping, indent=4))

    def listfixers(self):
        """List all the available fixers."""
        availablefixers = []
        for methodname in [m for m in dir(ProblemFixer) if m.startswith('fix_')]:
            docstring = getattr(ProblemFixer, methodname).__doc__
            for prob in [pb.strip()[2:] for pb in docstring.splitlines()[1:]]:
                if prob:
                    availablefixers.append(prob)
        self.info("Fixers:")
        for fixstr in sorted(availablefixers):
            if ((not fixstr.startswith("syntax error")) or (not self.arguments.nosyntax)):
                self.info(f"  - {fixstr}")
        return EXIT_OK

    def fix(self):
        """Fix all files."""
        with open(self.arguments.diffto, 'w', encoding='utf-8') as diffto:
            for filename in self.filenames:
                if filename == '-':
                    uifilename = '<stdin>'
                else:
                    uifilename = filename
                filetofix = FileFixer(self.arguments, filename)
                self.debug(f"Fixing {uifilename} ... ")
                (status, unidiff) = filetofix.fix()
                diffto.writelines(unidiff)
                if status == FIX_PASSEDLINTER:
                    self.debug("passed linter's strict mode.")
                    txtstatus = "  PASSED"
                    self.passed += 1
                elif status == FIX_MODIFIED:
                    self.debug("was modified.")
                    txtstatus = "MODIFIED"
                    self.modified += 1
                elif status == FIX_FIXED:
                    self.debug("was fixed.")
                    txtstatus = "   FIXED"
                    self.fixed += 1
                elif status == FIX_SKIPPED:
                    self.debug("was skipped.")
                    txtstatus = " SKIPPED"
                    self.skipped += 1
                elif status == FIX_PERMERROR:
                    self.debug("was not writeable.")
                    txtstatus = "   ERROR"
                    self.permerrors += 1
                else:
                    self.error(f"unknown fixing status [{status}]")
                    txtstatus = " UNKNOWN"
                    self.unknown += 1
                self.summary.append((txtstatus,
                                     uifilename,
                                     filetofix.issues,
                                     filetofix.issueshandled))

        self.statistics()
        if (self.passed + self.skipped + self.fixed) == len(self.filenames):
            return EXIT_OK
        return EXIT_NOK
