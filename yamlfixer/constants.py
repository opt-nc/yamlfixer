
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

"""Constants for yamlfixer."""

FIX_PASSEDLINTER = 0
FIX_MODIFIED = 1
FIX_SKIPPED = 2
FIX_PERMERROR = 3

FIXER_UNHANDLED = -1
FIXER_HANDLED = 0

EXIT_OK = 0
EXIT_NOK = -1
EXIT_PROBLEM = -2
EXIT_CMDLINEERROR = -3
