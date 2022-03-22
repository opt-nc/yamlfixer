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

"""yamlfixer's ProblemFixer class."""

from .constants import FIXER_HANDLED, FIXER_UNHANDLED

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
                line = self.ffixer.lines[self.linenum]
                left = line[:self.colnum]
                right = line[self.colnum:]
                self.ffixer.yfixer.debug(f'Calling {methodname}("{left}", "{right}")')
                getattr(self, methodname)(left, right)
                return FIXER_HANDLED
        self.ffixer.yfixer.debug(f"No handler found")
        return FIXER_UNHANDLED

    def get_indentation(self, offset=0):
        """Returns the indentation of the current (possibly offset) line."""
        lnum = self.linenum
        if offset:
            direction = int(offset/abs(offset))
            lnum += direction
            try:
                while offset:
                    while (0 < lnum < len(self.ffixer.lines)) \
                      and not self.ffixer.lines[lnum].strip():
                        lnum += direction
                    offset -= direction
            except IndexError:
                # We're past EOF, so just take the last line of the file
                # which is most probably empty anyway...
                lnum = -1
        line = self.ffixer.lines[lnum]
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

    def fix_syntax_tabchar(self, left, right): # pylint: disable=unused-argument
        """Fix:
             - syntax error: found character '\\t' that cannot start any token (syntax)
        """
        line = self.ffixer.lines[self.linenum][:]
        self.ffixer.lines[self.linenum] = line.expandtabs(self.ffixer.yfixer.arguments.tabsize)
        self.ffixer.coffset += len(self.ffixer.lines[self.linenum]) - len(line)

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
        elif self.ffixer.lines[self.linenum-1][previndentation:].startswith("-"):
            # same as above, because yamllint allows no space before item
            previndentation += 1
        self.ffixer.lines[self.linenum] = ' ' * previndentation + (left + right).lstrip()
        self.ffixer.coffset += previndentation - indentation
