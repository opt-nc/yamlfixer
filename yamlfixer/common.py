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
from contextlib import suppress

COLORS = {"black": (0, 0, 0),
          "white": (255, 255, 255),
          "red": (255, 0, 0),
          "lime": (0, 255, 0),
          "blue": (0, 0, 255),
          "yellow": (255, 255, 0),
          "cyan": (0, 255, 255),
          "magenta": (255, 0, 255),
          "silver": (192, 192, 192),
          "gray": (128, 128, 128),
          "maroon": (128, 0, 0),
          "olive": (128, 128, 0),
          "green": (0, 128, 0),
          "purple": (128, 0, 128),
          "teal": (0, 128, 128),
          "navy": (0, 0, 128),
          "gold": (255, 215, 0),
          "darkorange": (255, 140, 0)}

LEVELS = {"ERROR": "red",
          "WARNING": "darkorange",
          "DEBUG": "gray"}


class YAMLFixerBase:
    """Base class for yamlfixer."""

    def __init__(self, arguments):
        """Save command line arguments."""
        self._out = sys.stderr
        self._outwantscolors = self._out.isatty() or arguments.forcecolors
        self.arguments = arguments

    def _output(self, message, level=None):
        """Output a message with optional level to stderr."""
        if level is not None:
            message = f"{level}: {message}"
        with suppress(KeyError):
            message = self.colorize(message, LEVELS[level])
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

    def colorize(self, message, color):
        """Return a colorized message if output stream is a tty."""
        if self._outwantscolors:
            with suppress(KeyError):
                message = f"\033[38;2;{';'.join([str(s) for s in COLORS[color]])}m{message}\033[0m"
        return message
