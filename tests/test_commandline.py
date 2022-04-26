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
import unittest

from yamlfixer.__main__ import run


class RunContext():
    """Context manager for ``run()`` to capture streams."""

    def __init__(self, case):
        """Initialize context manager."""
        self.stdout = self.stderr = None
        self.outstream = self.errstream = None
        self._raises_ctx = case.assertRaises(SystemExit)  # noqa: PT009, T003

    def __enter__(self):
        """Enter context."""
        self._raises_ctx.__enter__()
        sys.stdout = self.outstream = StringIO()
        sys.stderr = self.errstream = StringIO()
        return self

    def __exit__(self, *exc_info):
        """Exit context."""
        self.stdout, sys.stdout = self.outstream.getvalue(), sys.__stdout__
        self.stderr, sys.stderr = self.errstream.getvalue(), sys.__stderr__
        return self._raises_ctx.__exit__(*exc_info)

    @property
    def returncode(self):
        """Fake property."""
        return self._raises_ctx.exception.code


class CommandLineTestCase(unittest.TestCase):
    """Test suite for the command line."""

    @classmethod
    def setUpClass(cls):
        """Set up, empty for now."""
        super(CommandLineTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Tear down, empty for now."""
        super(CommandLineTestCase, cls).tearDownClass()

    def test_run_with_bad_arguments(self):
        """Test launching yamlfixer with incorrect arguments."""
        with RunContext(self) as ctx:
            run(('--unknown-arg', ))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(ctx.stderr, r'^usage')

        with RunContext(self) as ctx:
            run(('-c', './conf.yaml', '-C', 'relaxed', 'file'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -C\/--config-data: '
            r'not allowed with argument -c\/--config-file$'
        )

        with RunContext(self) as ctx:
            run(('-b', '-n'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -n\/--nochange: '
            r'not allowed with argument -b\/--backup$'
        )

        with RunContext(self) as ctx:
            run(('-j', '-s'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -s\/--summary: '
            r'not allowed with argument -j\/--jsonsummary$'
        )

        with RunContext(self) as ctx:
            run(('-p', '-s'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -s\/--summary: '
            r'not allowed with argument -p\/--plainsummary$'
        )

        with RunContext(self) as ctx:
            run(('-p', '-j'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -j\/--jsonsummary: '
            r'not allowed with argument -p\/--plainsummary$'
        )

        with RunContext(self) as ctx:
            run(('-p', '-j'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -j\/--jsonsummary: '
            r'not allowed with argument -p\/--plainsummary$'
        )

        with RunContext(self) as ctx:
            run(('-r', '3.5'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: argument -r\/--recurse: invalid int value: \'3.5\'$'
        )

        with RunContext(self) as ctx:
            run(('-t', '-3'))
        assert ctx.returncode == 2
        assert ctx.stdout == ''
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'error: invalid tabsize value \'-3\'$'
        )
