# yamlfixer
yamlfixer automates the fixing of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

# Prerequisistes
In order for it to work, _yamlfixer_ needs that the following
utilities are already installed on your system, in a directory present
in your _$PATH_ :

- _Python_ v3.6 or higher
- _yamllint_ v1.26.3 or higher

# Usage
This software automatically fixes some errors and warnings reported by
_yamllint_.

usage:

```
$ yamlfixer [--debug] [--verbose] [--backup] *.yml - thisfile.yaml
```

or:

```
$ yamlfixer [--help] [--version]
```

This will launch _yamllint_ on each specified file name (`-` is _stdin_),
then parse its output and try to fix the reported problems.

If input is read from _stdin_, the corrected output will be sent to
_stdout_. Other files will be overwritten if needed. Original files,
_stdin_ excepted, can be preserved as _.orig_ if the _--backup_
command line option is used.

Diagnostic information is sent to stderr in verbose or debug modes.

This command exits with `0` if all input files either are skipped or
successfully pass _yamllint_ strict mode, else `-1`.

**IMPORTANT:** Not all problems are fixable by _yamlfixer_. Due to the
way _yamllint_ works, it doesn't currenlty report all faulty lines,
_yamlfixer_ might even introduce indentation problems under some
circumstances.
**Use at your own risk, you have been warned...**

# Licensing information
Copyright (C) 2021 OPT-NC

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

# Contact

OPT-NC, aka _Office des Postes et Télécommunications de Nouvelle-Calédonie_,
has a corporate website on [www.opt.nc](https://www.opt.nc)

You can contact the author of this software at
[jerome.alet@opt.nc](mailto:jerome.alet@opt.nc)
