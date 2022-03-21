

[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)
[![Kataocda scenario](https://img.shields.io/badge/katacoda-homepage-blue)](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer)

![PyPI](https://img.shields.io/pypi/v/yamlfixer-opt-nc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yamlfixer-opt-nc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yamlfixer-opt-nc)

# ![yamlfixer's logo](logo/candidates/1-64x64.png) yamlfixer

# ❔ About

[yamlfixer](https://github.com/opt-nc/yamlfixer) automates the fixing
of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

# 📑 Installation

💡 **You can try the install process online thanks to the dedicated [Katacoda scenario](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer).**

The easiest way to install `yamlfixer` is from
[pypi](https://pypi.org/project/yamlfixer-opt-nc/), as described
below.


## 🐧Linux install

```shell
python3 -m pip install yamlfixer-opt-nc
```

## 🪟 Windows install

```shell
python -m pip install yamlfixer-opt-nc
```


# 🚀 Usage

This software automatically fixes some errors and warnings reported by
`yamllint`.

```shell
usage: yamlfixer [-h] [-v] [-b] [-B BACKUPSUFFIX] [-d] [-j | -p | -s] [file [file ...]]

Fix formatting problems in YAML documents. If no file is specified,
then reads input from `stdin`.

positional arguments:
  file                the YAML files to fix. Use `-` to read from `stdin`.

optional arguments:
  -h, --help          show this help message and exit
  -v, --version       display this program's version number and exit.
  -b, --backup        make a backup copy of original files as `.orig`
  -b, --backup        make a backup copy of original files.
  -B BACKUPSUFFIX, --backupsuffix BACKUPSUFFIX
                      sets the suffix for backup files, `.orig` is
                      the default.
  -d, --debug         output debug information to stderr.
  -l, --listfixes     output the list of available fixes.
  -j, --jsonsummary   output JSON summary to stderr.
  -p, --plainsummary  output plain text summary to stderr.
  -s, --summary       output colored plain text summary to stderr.
                      If stderr is not a TTY output is identical to
                      --plainsummary.
```

yamlfixer launches `yamllint` on each specified filename, then parses
its output and try to fix the reported problems. The special filename
`-` means `stdin`, and is assumed if there's no other filename
argument.

If input is read from `stdin`, the corrected output will be sent to
`stdout`.

Other files will be overwritten if needed. Original files,
`stdin` excepted, can be preserved as `.orig` if the `--backup`
command line option is used.

Both summaries and diagnostic information are sent to stderr.

This command exits with `-3` if there are incompatible command line
options. It exits with `-2` if yamllint is not available on your
system. Otherwise it exits with `0` if all input files either are
skipped or successfully pass `yamllint` strict mode, else `-1`.

**IMPORTANT:** Not all problems are fixable by `yamlfixer`. Due to the
fact that `yamllint` doesn't currently report all faulty lines,
`yamlfixer` might even introduce indentation problems under some
circumstances.

⚠️**Use at your own risk, you have been warned...** ⚠️

# 💪 Tips and tricks

Find here a set of tips & tricks about how to achieve great things.

Don't find the usecase you're looking for ➡️ [🎫 Fill a dedicated issue so we could share your idea with the comunity](https://github.com/opt-nc/yamlfixer/issues/new?assignees=&labels=help+wanted&template=ask-for-command-line-script---.md&title=Request+for+script+or+oneLiner)

## ⏩ One liners

Most of use love short and efficient command lines. Here are some ready to use ones : 

### Piping `json`  summary through `jq`

```
yamlfixer --jsonsummary bad.yml 2>&1 | jq
```

So you can get a nicely colored (and validated `json` output) : 

```json
  "filestofix": 1,
  "passedstrictmode": 1,
  "modified": 0,
  "skipped": 0,
  "notwriteable": 0,
  "unknown": 0,
  "details": {
    "/home/jerome/yamlfixer/bad.yml": {
      "status": "PASSED",
      "issues": 0,
      "handled": 0
    }
  }
}
```

### Check if `yamlfixer` could fix a `yaml` and get the exit code

See how piping fixing and linting can be interesting... and get exit code
so you can go further in automation :

```
yamlfixer <bad.yml | yamllint --format parsable --strict -
echo $?
```

# 🔖 Related contents

- [Dedicated Post explaining how we are using this project to automate `yaml` linting and fixing](https://dev.to/adriens/let-ci-check-fix-your-yamls-kfa)
- [GH Action relying on this project](https://github.com/marketplace/actions/yaml-fixer)
- [Dedicated Katacoda scenario](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer) so you can see it live

# 📖 Licensing information

```
Copyright (C) 2021-2022 OPT-NC

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
```

# 🧑‍🤝‍🧑 Contact

To contact the [authors](AUTHORS.md) of this software, simply fill an
issue on this project.

OPT-NC, aka _Office des Postes et Télécommunications de Nouvelle-Calédonie_, check
[`OPT-NC`](https://github.com/opt-nc) Github Organization page for more.
