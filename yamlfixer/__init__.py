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

"""yamlfixer automates the fixing of problems reported by yamllint.

yamlfixer passes files through yamllint and parses its output
to try to fix each of the reported problems.
"""

import time

__version__ = "0.9.7"
__author__ = "OPT-NC"
__license__ = "GPLv3+"
__year__ = time.strftime("%Y", time.localtime(time.time()))
__copyright__ = f"Copyright (C) 2021-{__year__} {__author__}"
