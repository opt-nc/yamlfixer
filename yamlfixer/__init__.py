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

"""yamlfixer automates the fixing of problems reported by yamllint
by feeding it with files and parsing its output."""

import time

__version__ = "0.4.5"
__author__ = "OPT-NC"
__license__ = "GPLv3+"
__copyright__ = "Copyright (C) 2021-%s %s" % (time.strftime("%Y",
                                                            time.localtime(time.time())),
                                              __author__)
