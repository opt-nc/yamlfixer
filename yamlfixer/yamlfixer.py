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
from contextlib import suppress

from . import __version__
from .constants import FIX_PASSEDLINTER, FIX_MODIFIED, FIX_FIXED, FIX_SKIPPED, FIX_PERMERROR
from .constants import EXIT_OK, EXIT_NOK
from .common import YAMLFixerBase
from .filefixer import FileFixer
from .problemfixer import ProblemFixer

STATUSES = {FIX_PASSEDLINTER: {"msg": "passed linter's strict mode",
                               "counter": "passed",
                               "color": "green"},
            FIX_MODIFIED: {"msg": "was modified",
                           "counter": "modified",
                           "color": "blue"},
            FIX_FIXED: {"msg": "was fixed",
                        "counter": "fixed",
                        "color": "lime"},
            FIX_SKIPPED: {"msg": "was skipped",
                          "counter": "skipped",
                          "color": "magenta"},
            FIX_PERMERROR: {"msg": "was not writable",
                            "counter": "notwritable",
                            "color": "red"}}


class YAMLFixer(YAMLFixerBase):
    """To hold files fixing logic."""

    def __init__(self, arguments):
        """Initialize the fixer for all files."""
        super().__init__(arguments)
        self.debug(f"yamlfixer v{__version__}")
        self.debug(f"arguments={repr(arguments)}")
        self.extensions = [f".{e.strip()}" for e in self.arguments.ext.split(",")]
        self.filenames = self._generate_unique_filenames(self.arguments.filenames)
        self.summary = {"filestofix": len(self.filenames),
                        "passed": 0,
                        "modified": 0,
                        "fixed": 0,
                        "skipped": 0,
                        "notwritable": 0,
                        "unknown": 0,
                        "nochangemode": self.arguments.nochange,
                        "details": {}}

    def _matchesext(self, filename):
        """Return True if filename matches the set of extensions, else False."""
        return any(filename.endswith(ext) for ext in self.extensions)

    def _recurse(self, path, fnmapping, level=0):
        """Find all files in a directory recursively."""
        self.debug(f"SCAN [{path}] at level {level} with limit {self.arguments.recurse}")
        if (self.arguments.recurse < 0) or (level <= self.arguments.recurse):
            with suppress(PermissionError), os.scandir(path) as dircontents:
                for entry in dircontents:
                    if entry.is_file() and self._matchesext(entry.name):
                        # Ensures uniqueness based on absolute path
                        fnmapping[os.path.abspath(entry.path)] = entry.path
                    elif (entry.is_dir(follow_symlinks=self.arguments.followsymlinks)
                          and ((self.arguments.recurse < 0) or (level < self.arguments.recurse))):
                        self._recurse(entry.path, fnmapping, level + 1)

    def _generate_unique_filenames(self, fnames):
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
                    self._recurse(name, fnmapping)
                else:
                    # Ensures uniqueness based on absolute path
                    fnmapping[os.path.abspath(name)] = name
        return sorted(fnmapping.values())

    def _statistics(self):
        """Output some statistics."""
        if self.arguments.summary or self.arguments.plainsummary:
            self.info(f"Files to fix: {self.summary['filestofix']}")
            self.info(f"{self.summary['passed']} files were already correct before")
            self.info(f"{self.summary['modified']} files were modified but problems remain")
            self.info(f"{self.summary['fixed']} files were entirely fixed")
            self.info(f"{self.summary['skipped']} files were skipped")
            self.info(f"{self.summary['notwritable']} files were not writable")
            self.info(f"{self.summary['unknown']} files with unknown status")
            rjustifyto = max([len(STATUSES.get(s, {"counter": "unknown"})["counter"])
                              for s in (list(STATUSES.keys()) + ["unknownstatusvalue"])])
            for filename in self.summary["details"]:
                filedetails = self.summary["details"][filename]
                status = filedetails["status"].rjust(rjustifyto)
                if filedetails["issues"]:
                    msg = f" (handled {filedetails['handled']}/{filedetails['issues']})"
                else:
                    msg = ""
                if self.arguments.summary:
                    with suppress(KeyError):
                        # Yellow for unknown status
                        status = self.colorize(status, STATUSES[filedetails["numericstatus"]].get("color", "yellow"))
                self.info(f"{status} {filename}{msg}")
            if self.arguments.nochange:
                message = "No file was modified per user's request !"
                if self.arguments.summary:
                    self.warning(message)
                else:
                    self.info(f"WARNING: {message}")  # Ensure it's not colorized
        elif self.arguments.jsonsummary:
            self.info(json.dumps(self.summary, indent=4))

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
        try:
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
                    result = STATUSES.get(status, {"msg": f"unknown fixing status [{status}]",
                                                   "counter": "unknown"})
                    if status not in STATUSES:
                        self.error(f"{result['msg']}")
                    else:
                        self.debug(f"{result['msg']}")
                    self.summary[result["counter"]] += 1
                    self.summary["details"][uifilename] = {"numericstatus": status,
                                                           "status": result["counter"].upper(),
                                                           "issues": filetofix.issues,
                                                           "handled": filetofix.issueshandled}
            self._statistics()
            if (self.summary["passed"] + self.summary["skipped"] + self.summary["fixed"]) == self.summary["filestofix"]:
                return EXIT_OK
        except PermissionError as msg:
            self.error(msg)
        return EXIT_NOK
