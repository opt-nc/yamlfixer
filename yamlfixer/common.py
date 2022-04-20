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

"""yamlfixer's base class."""

import sys


class YAMLFixerBase:
    """Base class for yamlfixer."""
    def __init__(self, arguments):
        """Saves command line arguments."""
        self._out = sys.stderr
        self.outisatty = self._out.isatty()
        self.arguments = arguments

    def _output(self, message, level=None):
        """Output a message with optional level to stderr."""
        if level is not None:
            self._out.write(f"{level}: ")
        self._out.write(f"{message}\n")

    def debug(self, message):
        """Output a debug message."""
        if self.arguments.debug:
            self._output(message, level="DEBUG")

    def error(self, message):
        """Output an error message."""
        self._output(message, level="ERROR")

    def warning(self, message):
        """Output a warning message."""
        self._output(message, level="WARNING")

    def info(self, message):
        """Output an informational message."""
        self._output(message)
