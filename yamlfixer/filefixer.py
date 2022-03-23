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

"""yamlfixer's FileFixer class."""

import sys
import os
import subprocess

from .constants import FIX_PASSEDLINTER, FIX_MODIFIED, FIX_SKIPPED, FIX_PERMERROR
from .constants import FIXER_HANDLED
from .constants import EXIT_PROBLEM

from .problemfixer import ProblemFixer

LINTERCOMMAND = 'yamllint --format parsable --strict -'

class FileFixer: # pylint: disable=too-many-instance-attributes
    """To hold file fixing logic."""
    def __init__(self, yamlfixer, filename):
        """Initialize a file to fix."""
        self.yfixer = yamlfixer
        self.filename = filename
        self.loffset = self.coffset = 0
        self.shebang = ''
        self.incontents = None
        self.lines = []
        self.issues = self.issueshandled = 0

    def canonicalizeproblems(self, linteroutput):
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
                pass # No problem reported on shebang line by yamllint
            # This line won't ever see the fixer so all subsequent lines must be offset by -1
            self.loffset = -1

        return problemlines

    def lint(self):
        """Launches the linter on a file's contents.

           Returns the (linter's exitcode, linter's stdout) tuple.
        """
        linter = subprocess.run(LINTERCOMMAND,
                                shell=True,
                                capture_output=True,
                                text=True,
                                check=False,
                                input=self.incontents,
                                encoding='utf-8')
        return (linter.returncode, linter.stdout)

    def load(self):
        """Loads the input file's contents."""
        if self.filename == '-':
            try:
                self.incontents = sys.stdin.read()
            except KeyboardInterrupt:
                self.yfixer.error("\nInterrupted at user's request.")
                self.incontents = ""
        else:
            try:
                with open(self.filename, 'r') as yamlfile:
                    self.incontents = yamlfile.read()
            except FileNotFoundError as msg:
                self.yfixer.error(f"{msg}")

    def dump(self, outcontents):
        """Dumps the new file's contents."""
        if (self.incontents is None) or (outcontents == self.incontents):
            retcode = FIX_SKIPPED
        else:
            retcode = FIX_MODIFIED
        if self.yfixer.arguments.nochange:
            # We don't want to modify anything
            if self.filename == '-': # Always dump original input to stdout in this case
                sys.stdout.write(self.shebang + (self.incontents or ''))
                sys.stdout.flush()
        else:
            # It seems we really want to fix things.
            if self.filename == '-': # Always dump to stdout in this case
                sys.stdout.write(self.shebang + (outcontents or ''))
                sys.stdout.flush()
            elif retcode == FIX_MODIFIED: # Don't write unnecessarily
                try:
                    if self.yfixer.arguments.backup: # pylint: disable=no-member
                        # Try to make a backup of the original file
                        try:
                            os.replace(self.filename,
                                       f"{self.filename}{self.yfixer.arguments.backupsuffix}")
                        except PermissionError as msg:
                            self.yfixer.error(f"impossible to create a backup : {msg}")
                    # Overwrite the original file with the new contents
                    with open(self.filename, 'w') as yamlfile:
                        yamlfile.write(self.shebang + (outcontents or ''))
                except PermissionError as msg:
                    self.yfixer.error(f"impossible to save fixed contents : {msg}")
                    retcode = FIX_PERMERROR
        return retcode

    def fix(self):
        """Fix a file's contents."""
        # Load the file's contents in memory
        self.load()

        # Skip that file if we don't want to modify it
        if (self.incontents is None) or self.incontents.startswith('$ANSIBLE_VAULT;'):
            return self.dump(self.incontents)

        # Lint the file's contents
        (ltexitcode, ltstdout) = self.lint()
        if not ltexitcode:
            self.dump(self.incontents)
            return FIX_PASSEDLINTER
        if ltexitcode == 127: # yamllint not found !
            self.yfixer.error("yamllint is not in your PATH, please ensure it's installed.")
            sys.exit(EXIT_PROBLEM)

        # Organize the set of problems to fix
        linestofix = self.canonicalizeproblems(ltstdout)

        # Now handle each of the problems reported by yamllint
        self.lines = self.incontents.splitlines()
        for linenumber in sorted(linestofix.keys()):
            self.coffset = 0
            for colnumber in sorted(linestofix[linenumber].keys()):
                for problem in linestofix[linenumber][colnumber]:
                    # pylint: disable=line-too-long
                    self.yfixer.debug(f"({linenumber}+{self.loffset}, {colnumber}+{self.coffset}) => [{problem}]")
                    handled = ProblemFixer(self, linenumber, colnumber, problem)()
                    if handled == FIXER_HANDLED:
                        self.issueshandled += 1
                        self.yfixer.debug(f"HANDLED: #{self.issueshandled}")
                    else:
                        self.yfixer.debug("UNHANDLED")
        return self.dump('\n'.join(self.lines) + '\n')
