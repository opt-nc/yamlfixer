# -*- coding: utf-8 -*-

"""yamlfixer automates the fixing of problems reported by yamllint
by feeding it with files and parsing its output."""

import sys
import os
import time
import subprocess
import argparse
import json

__version__ = "0.3.8"
__author__ = "OPT-NC"
__license__ = "GPLv3+"
__copyright__ = "Copyright (C) 2021-%s %s" % (time.strftime("%Y",
                                                            time.localtime(time.time())),
                                              __author__)

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

LINTERCOMMAND = 'yamllint --format parsable --strict -'

FIX_PASSEDLINTER = 0
FIX_MODIFIED = 1
FIX_SKIPPED = 2
FIX_PERMERROR = 3

FIXER_UNHANDLED = -1
FIXER_HANDLED = 0

EXIT_OK = 0
EXIT_NOK = -1
EXIT_PROBLEM = -2

COLORSEQ = {"PASSED": "38;2;0;255;0m",
            "MODIFIED": "38;2;0;0;255m",
            "SKIPPED": "38;2;255;0;255m",
            "ERROR": "38;2;255;0;0m",
            "UNKNOWN": "38;2;255;255;0m",
           }

class ProblemFixer:
    """To hold problem fixing logic."""
    fixers = {}
    def __init__(self, filefixer, linenum, colnum, problem):
        """Intializes a problem fixer."""
        self.ffixer = filefixer
        self.linenum = linenum + self.ffixer.loffset - 1
        self.colnum = colnum + self.ffixer.coffset - 1
        self.problem = problem
        if not self.fixers:
            for methodname in [m for m in dir(self) if m.startswith('fix_')]:
                docstring = getattr(self, methodname).__doc__
                for prob in [pb.strip()[2:] for pb in docstring.splitlines()[1:]]:
                    if prob:
                        self.fixers[prob] = methodname

    def __call__(self):
        """Make it callable."""
        for (fixerkey, methodname) in self.fixers.items():
            if self.problem.startswith(fixerkey):
                # pylint: disable=line-too-long
                self.ffixer.yfixer.debug(f"Calling {methodname} because [{fixerkey}] matches [{self.problem}]")
                line = self.ffixer.lines[self.linenum]
                left = line[:self.colnum]
                right = line[self.colnum:]
                getattr(self, methodname)(left, right)
                return FIXER_HANDLED
        self.ffixer.yfixer.debug(f"No handler found for [{self.problem}]")
        return FIXER_UNHANDLED

    def get_indentation(self, offset=0):
        """Returns the indentation of the current (possibly offset) line."""
        line = self.ffixer.lines[self.linenum + offset]
        return len(line) - len(line.lstrip())

    #
    # Fixing code below.
    #
    # To fix a new kind of problem, simply add a fix_whatever method
    # and ensure its docstring is formatted the same way as the
    # existing ones. Each docstring lists each problem its method
    # should fix, exactly as it is reported by yamllint. Matching is
    # done from the beginning of yamllint's output after the
    # warning/error level.
    #

    def fix_missing_docstart(self, left, right): # pylint: disable=unused-argument
        """Fix:
             - missing document start
        """
        self.ffixer.lines.insert(0, '---')
        self.ffixer.loffset += 1

    def fix_newlineateof(self, left, right): # pylint: disable=unused-argument,no-self-use
        """Fix:
             - no new line character at the end of file
        """
        # We simply ignore it, because we always add \n when dumping.

    def fix_truthy(self, left, right):
        """Fix:
             - truthy value should be one of [false, true] (truthy)
        """
        for trueval in ('on', 'yes', 'true'):
            if right.lower().startswith(trueval):
                self.ffixer.lines[self.linenum] = left + 'true' + right[len(trueval):]
                self.ffixer.coffset += len('true') - len(trueval)
                return
        for falseval in ('off', 'no', 'false'):
            if right.lower().startswith(falseval):
                self.ffixer.lines[self.linenum] = left + 'false' + right[len(falseval):]
                self.ffixer.coffset += len('false') - len(falseval)
                return

    def fix_toofew_spacesbefore(self, left, right):
        """Fix:
             - too few spaces before comment (comments)
        """
        spaces = ' '
        if left[-1] != ' ':
            spaces += ' '
        self.ffixer.lines[self.linenum] = left + spaces + right
        self.ffixer.coffset += len(spaces)

    def fix_trailingspaces(self, left, right):
        """Fix:
             - trailing spaces (trailing-spaces)
        """
        # No need to adjust coffset because we are at EOL by definition
        self.ffixer.lines[self.linenum] = (left + right).rstrip()

    def fix_toomany_blanklines(self, left, right): # pylint: disable=unused-argument
        """Fix:
             - too many blank lines
        """
        parts = self.problem.split()
        blanklines = int(parts[4][1:])
        maxblanklines = int(parts[6].split(')')[0])
        nblines = blanklines - maxblanklines
        del self.ffixer.lines[self.linenum - nblines + 1:self.linenum + 1]
        self.ffixer.loffset -= nblines

    def fix_syntax_tabchar(self, left, right):
        """Fix:
             - syntax error: found character '\\t' that cannot start any token (syntax)
        """
        # TODO: We replace TAB with a single space for now
        # TODO: yamllint only reports the first one
        # TODO: use expandtabs after reading indentation size from .yamllint if possible
        self.ffixer.lines[self.linenum] = left + ' ' + right[1:]

    def fix_missingspace(self, left, right):
        """Fix:
             - missing starting space in comment (comments)
             - too few spaces after comma (commas)
        """
        self.ffixer.lines[self.linenum] = left + ' ' + right
        self.ffixer.coffset += 1

    def fix_toomany_spacesafter(self, left, right):
        """Fix:
             - too many spaces after colon (colons)
             - too many spaces after comma (commas)
             - too many spaces after hyphen (hyphens)
        """
        pos = self.colnum
        while (pos > 0) and (left[pos - 1] == ' '):
            pos -= 1
        self.ffixer.lines[self.linenum] = left[:pos] + right
        self.ffixer.coffset -= (self.colnum - pos)

    def fix_toomany_spacesother(self, left, right):
        """Fix:
             - too many spaces inside braces (braces)
             - too many spaces inside brackets (brackets)
             - too many spaces before comma (commas)
             - too many spaces before colon (colons)
        """
        pos = self.colnum
        while (pos > 0) and (left[pos - 1] == ' '):
            pos -= 1
        self.ffixer.lines[self.linenum] = left[:pos] + right[1:]
        self.ffixer.coffset -= (self.colnum - pos + 1)

    def fix_comment_notindentedlike(self, left, right):
        """Fix:
             - comment not indented like content (comments-indentation)
        """
        if self.linenum > 0:
            indentation = self.get_indentation(-1)
            # If previous line is similarly indented then use indentation of next line
            if indentation == self.colnum:
                indentation = self.get_indentation(+1)
        else:
            indentation = self.get_indentation(+1)
        self.ffixer.lines[self.linenum] = ' ' * indentation + (left + right).lstrip()
        self.ffixer.coffset += (indentation - self.colnum)

    def fix_wrong_indentation(self, left, right):
        """Fix:
             - wrong indentation: expected
        """
        # TODO: yamllint only reports the first faulty line in a block :-(
        # TODO: see https://github.com/adrienverge/yamllint/issues/427
        # TODO: we fix anyway, knowing that we may need to launch the command
        # TODO: several times to finally fix the problem.
        parts = self.problem.split()
        expected = int(parts[3])
        found = int(parts[6])
        offset = expected - found
        if expected > found:
            self.ffixer.lines[self.linenum] = (' ' * offset) + left + right
        else:
            # expected < found because we woudln't be there otherwise anyway
            self.ffixer.lines[self.linenum] = (left + right)[-offset:]
        self.ffixer.coffset += offset

    def fix_linetoolong(self, left, right): # pylint: disable=unused-argument
        """Fix:
             - line too long
        """
        # TODO: currently we fix this by disabling the error in yamllint, it's the easiest way
        self.ffixer.lines.insert(self.linenum, ' ' * self.get_indentation() \
                             + '# yamllint disable-line rule:line-length')
        self.ffixer.loffset += 1

    def fix_syntax_mappingvalues_nah(self, left, right):
        """Fix:
             - syntax error: mapping values are not allowed here
             - syntax error: expected <block end>, but found '<block mapping start>'
             - syntax error: expected <block end>, but found '?'
        """
        indentation = self.get_indentation()
        previndentation = self.get_indentation(-1)
        if self.ffixer.lines[self.linenum-1][previndentation:].startswith("- "):
            # if previous line is a list item, indent like item itself
            previndentation += 2
        self.ffixer.lines[self.linenum] = ' ' * previndentation + (left + right).lstrip()
        self.ffixer.coffset += previndentation - indentation


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
        if self.filename == '-': # Always dump to stdout in this case
            sys.stdout.write(self.shebang + (outcontents or ''))
            sys.stdout.flush()
        elif retcode == FIX_MODIFIED: # Don't write unnecessarily
            try:
                if self.yfixer.arguments.backup: # pylint: disable=no-member
                    # Try to make a backup of the original file
                    try:
                        os.replace(self.filename, f"{self.filename}.orig")
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
                    debuginfo = f"({linenumber}, {colnumber})/({self.loffset}, {self.coffset}) => {problem}"
                    handled = ProblemFixer(self, linenumber, colnumber, problem)()
                    if handled == FIXER_HANDLED:
                        self.issueshandled += 1
                    # pylint: disable=line-too-long
                    self.yfixer.debug(f"{((handled == FIXER_HANDLED) and 'HANDLED') or 'UNHANDLED'}: {debuginfo}")
        return self.dump('\n'.join(self.lines) + '\n')


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
        elif self.arguments.jsonsummary:
            summarymapping = {"filestofix": len(self.arguments.filenames),
                              "passedstrictmode": self.passed,
                              "modified": self.modified,
                              "skipped": self.skipped,
                              "notwriteable": self.permerrors,
                              "unknown": self.unknown,
                              "details": {},
                             }
            for (status, filename, issues, handled) in self.summary:
                summarymapping["details"][filename] = {"status": status.strip(),
                                                       "issues": issues,
                                                       "handled": handled,
                                                      }
            self.info(json.dumps(summarymapping, indent=4))

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


def run():
    """Main function."""
    # Ensure we read from stdin in case it's redirected
    if ("-" not in sys.argv[1:]) and not sys.stdin.isatty():
        sys.argv.append("-")

    # Parse the command line arguments
    cmdline = argparse.ArgumentParser(description="Fix formatting problems in YAML documents. "
                                      "If no file is specified,\nthen reads input from `stdin`.",
                                      epilog=f"{__copyright__}\n{GPLBLURB}",
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    cmdline.add_argument("-v", "--version",
                         action="version",
                         version=f"yamlfixer v{__version__}",
                         help="display this program's version number and exit.")
    cmdline.add_argument("-b", "--backup",
                         action="store_true",
                         help="make a backup copy of original files as `.orig`")
    cmdline.add_argument("-d", "--debug",
                         action="store_true",
                         help="output debug information to stderr.")
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
    cmdline.add_argument("filenames",
                         nargs="*",
                         metavar="file",
                         default=["-"], # Read from stdin if no file is specified
                         help="the YAML files to fix. Use `-` to read from `stdin`.")
    arguments = cmdline.parse_args()
    return YAMLFixer(arguments).fix()
