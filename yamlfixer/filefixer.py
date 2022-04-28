
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

"""yamlfixer's FileFixer class."""

import sys
import os
import subprocess
import difflib
import shlex
from contextlib import suppress

from .constants import FIX_PASSEDLINTER, FIX_MODIFIED, FIX_FIXED, FIX_SKIPPED, FIX_PERMERROR
from .constants import FIXER_HANDLED
from .constants import EXIT_PROBLEM
from .common import YAMLFixerBase
from .problemfixer import ProblemFixer

# Base YAML linting command
LINTERCOMMAND = "yamllint --format parsable --strict"

# Just in case we reintroduce a check later on...
ALLOWEDMIMETYPES = ["text/plain",
                    "text/vnd.yaml",
                    "text/yaml",
                    "text/x-yaml",
                    "application/yaml",
                    "application/x-yaml"]


class FileFixer(YAMLFixerBase):  # pylint: disable=too-many-instance-attributes
    """To hold file fixing logic."""

    def __init__(self, arguments, filename):
        """Initialize a file to fix."""
        super().__init__(arguments)
        self.filename = filename
        self.loffset = self.coffset = 0
        self.shebang = ''
        self.incontents = None
        self.lines = []
        self.issues = self.issueshandled = 0

    def _canonicalizeproblems(self, linteroutput):
        """Create a nested mapping of lines and columns to fix."""
        problemlines = {}
        for line in linteroutput.splitlines():
            (_, linenumber, colnumber, message) = line.split(':', 3)
            (_, msg) = message.strip().split(' ', 1)
            colstofix = problemlines.setdefault(int(linenumber), {})
            # On a given line, there could be several problems on the same column
            coltofix = colstofix.setdefault(int(colnumber), [])
            coltofix.append(msg)
            self.issues += 1

        # If there's a shebang line we ignore it and any problem reported on it
        if (self.incontents is not None) and self.incontents.startswith('#!'):
            eolpos = self.incontents.find('\n') + 1
            self.shebang = self.incontents[:eolpos]
            self.incontents = self.incontents[eolpos:]
            try:
                del problemlines[1]
                self.issues -= 1
            except KeyError:
                pass  # No problem reported on shebang line by yamllint
            # This line won't ever see the fixer so all subsequent lines must be offset by -1
            self.loffset = -1

        return problemlines

    def lint(self, content):
        """Launch the linter on a file's content.

        Returns the (linter's exitcode, linter's stdout) tuple.
        """
        command = LINTERCOMMAND
        if self.arguments.config_data:
            confdata = self.arguments.config_data.strip()
            if confdata:
                command = f"{command} --config-data {shlex.quote(confdata)}"
        elif self.arguments.config_file:
            conffile = self.arguments.config_file.strip()
            if conffile:
                command = f"{command} --config-file {shlex.quote(conffile)}"
        command = f"{command} -"
        self.debug(f"Executing linter with {repr(command)}")
        linter = subprocess.run(command,
                                shell=True,
                                capture_output=True,
                                text=True,
                                check=False,
                                input=content,
                                encoding='utf-8')
        self.debug(f"Linter's exit code is {repr(linter.returncode)}")
        return (linter.returncode, linter.stdout)

    def load(self):
        """Load the input file's content."""
        try:
            if self.filename == '-':
                try:
                    self.incontents = sys.stdin.read()
                except KeyboardInterrupt:
                    self.error("\nInterrupted at user's request.")
                    self.incontents = ""  # Initialized but empty
            else:
                try:
                    with open(self.filename, 'r', encoding='utf-8') as yamlfile:
                        self.incontents = yamlfile.read()
                except (FileNotFoundError, PermissionError) as msg:
                    self.error(f"{msg}")
        except (UnicodeDecodeError, IsADirectoryError) as msg:
            self.error(f"{self.filename} doesn't seem to be YAML : {msg}")

    def diff(self, finalcontent):
        """Return a unified diff of original content to final one."""
        differences = []
        original = (self.shebang + (self.incontents or '')).splitlines(keepends=True)
        final = finalcontent.splitlines(keepends=True)
        if original != final:
            relbefore = f'"{self.filename}"'
            relafter = f'"{self.filename}-after"'
            differences.append(f"diff -u {relbefore} {relafter}\n")
            differences.extend(list(difflib.unified_diff(original,
                                                         final,
                                                         fromfile=relbefore,
                                                         tofile=relafter)))
        with suppress(IndexError):  # would be raised if original file was empty
            if not original[-1].endswith("\n"):
                # No newline at EOF
                # We know differences won't be empty then
                nbplus = 0
                diffix = len(differences)
                while (diffix > 0) and differences[diffix - 1].startswith("+"):
                    nbplus += 1
                    diffix -= 1
                differences.insert(-nbplus, "\n\\ No newline at end of file\n")
        return differences

    def dump(self, outcontents):
        """Dump the new file's contents."""
        if (self.incontents is None) or (outcontents == self.incontents):
            retcode = FIX_SKIPPED
        else:
            retcode = FIX_MODIFIED
        finaloutput = self.shebang + (outcontents or '')
        if self.arguments.nochange:
            # We don't want to modify anything
            if self.filename == '-':  # Always dump original input to stdout in this case
                sys.stdout.write(self.shebang + (self.incontents or ''))
                sys.stdout.flush()
        else:
            # It seems we really want to fix things.
            if self.filename == '-':  # Always dump to stdout in this case
                sys.stdout.write(finaloutput)
                sys.stdout.flush()
            elif retcode == FIX_MODIFIED:  # Don't write unnecessarily
                try:
                    if self.arguments.backup:
                        # Try to make a backup of the original file
                        try:
                            os.replace(self.filename,
                                       f"{self.filename}{self.arguments.backupsuffix}")
                        except PermissionError as msg:
                            self.error(f"impossible to create a backup : {msg}")
                    # Overwrite the original file with the new contents
                    with open(self.filename, 'w', encoding='utf-8') as yamlfile:
                        yamlfile.write(finaloutput)
                except PermissionError as msg:
                    self.error(f"impossible to save modified contents : {msg}")
                    retcode = FIX_PERMERROR

        # We've successfully modified the file, so we lint its new contents
        if retcode == FIX_MODIFIED:
            (ltexitcode, _) = self.lint(finaloutput)
            if not ltexitcode:
                # We know we have succesfully fixed the file
                # because it now passes yamlllint's strict mode.
                retcode = FIX_FIXED
        return (retcode, self.diff(finaloutput))

    def fix(self):
        """Fix a file's contents."""
        # Load the file's contents in memory
        self.load()

        # Skip that file if we don't want to modify it
        if (self.incontents is None) or self.incontents.startswith('$ANSIBLE_VAULT;'):
            return self.dump(self.incontents)

        # Lint the file's contents
        (ltexitcode, ltstdout) = self.lint(self.incontents)
        if not ltexitcode:
            (_, differences) = self.dump(self.incontents)
            return (FIX_PASSEDLINTER, differences)
        if ltexitcode == 127:  # yamllint not found !
            self.error("yamllint is not in your PATH, please ensure it's installed.")
            sys.exit(EXIT_PROBLEM)

        # Organize the set of problems to fix
        linestofix = self._canonicalizeproblems(ltstdout)

        # Now handle each of the problems reported by yamllint
        self.lines = self.incontents.splitlines()
        for linenumber in sorted(linestofix.keys()):
            self.coffset = 0
            for colnumber in sorted(linestofix[linenumber].keys()):
                for problem in linestofix[linenumber][colnumber]:
                    self.debug(f"({linenumber}+{self.loffset}, {colnumber}+{self.coffset}) => [{problem}]")
                    handled = ProblemFixer(self, linenumber, colnumber, problem)()
                    if handled == FIXER_HANDLED:
                        self.issueshandled += 1
                        self.debug(f"HANDLED: #{self.issueshandled}")
                    else:
                        self.debug("UNHANDLED")
        return self.dump('\n'.join(self.lines) + '\n')
