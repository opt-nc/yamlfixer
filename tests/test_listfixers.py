# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 OPT-NC
# Copyright (C) 2016 Adrien Vergé
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Tests invocation from the command line."""

from io import StringIO
import sys
from textwrap import dedent
import unittest

from yamlfixer.constants import EXIT_OK
from yamlfixer.__main__ import parse_commandline
from yamlfixer.yamlfixer import YAMLFixer


class ListFixersTestCase(unittest.TestCase):
    """Tests the --listfixers command line option."""

    def test_listfixers(self):
        """\
        Fixers:
          - comment not indented like content (comments-indentation)
          - found forbidden document end
          - found forbidden document start
          - line too long
          - missing document end
          - missing document start
          - missing starting space in comment (comments)
          - no new line character at the end of file
          - syntax error: expected '<document start>', but found '<stream end>' (syntax)
          - syntax error: expected <block end>, but found '<block mapping start>'
          - syntax error: expected <block end>, but found '<block sequence start>' (syntax)
          - syntax error: expected <block end>, but found '?'
          - syntax error: found character '\\t' that cannot start any token (syntax)
          - syntax error: mapping values are not allowed here
          - too few spaces after comma (commas)
          - too few spaces before comment (comments)
          - too few spaces inside brackets (brackets)
          - too few spaces inside empty brackets (brackets)
          - too many blank lines
          - too many spaces after colon (colons)
          - too many spaces after comma (commas)
          - too many spaces after hyphen (hyphens)
          - too many spaces before colon (colons)
          - too many spaces before comma (commas)
          - too many spaces inside braces (braces)
          - too many spaces inside brackets (brackets)
          - too many spaces inside empty brackets (brackets)
          - trailing spaces (trailing-spaces)
          - truthy value should be one of [false, true] (truthy)
          - wrong indentation: expected
          - wrong new line character: expected \\n
          - wrong new line character: expected \\r\\n
        """  # noqa: D205, D208, D210, D301, D400
        sys.stderr = StringIO()
        yfixer = YAMLFixer(parse_commandline(["yamlfixer", "--listfixers"]))

        retcode = yfixer.listfixers()  # act

        output = sys.stderr.getvalue()
        sys.stderr = sys.__stderr__
        assert retcode == EXIT_OK
        assert output == dedent(self.test_listfixers.__doc__)
