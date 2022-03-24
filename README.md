

[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)
[![Kataocda scenario](https://img.shields.io/badge/katacoda-homepage-blue)](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer)

![PyPI](https://img.shields.io/pypi/v/yamlfixer-opt-nc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yamlfixer-opt-nc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yamlfixer-opt-nc)

# ![yamlfixer's logo](logo/candidates/1-64x64.png) `yamlfixer`

# ❔ About

[yamlfixer](https://github.com/opt-nc/yamlfixer) automates the fixing
of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

# 🎬 Demo

Click on the white triangle in the image below to view a short video demonstration:

[![asciicast](https://asciinema.org/a/478928.svg)](https://asciinema.org/a/478928)

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
usage: yamlfixer [-h] [-v] [-b] [-B BACKUPSUFFIX] [-d] [-j | -p | -s] [-t TABSIZE] [file [file ...]]

Fix formatting problems in YAML documents. If no file is specified,
then reads input from `stdin`.

positional arguments:
  file                the YAML files to fix. Use `-` to read from `stdin`.

optional arguments:
  -h, --help          show this help message and exit
  -v, --version       display this program's version number and exit.
  -b, --backup        make a backup copy of original files.
  -B BACKUPSUFFIX, --backupsuffix BACKUPSUFFIX
                      sets the suffix for backup files, `.orig` is
                      the default.
  -d, --debug         output debug information to stderr.
  -l, --listfixers    output the list of available fixers.
  -n, --nochange      don't modify anything.
  -j, --jsonsummary   output JSON summary to stderr.
  -p, --plainsummary  output plain text summary to stderr.
  -s, --summary       output colored plain text summary to stderr.
                      If stderr is not a TTY output is identical to
                      --plainsummary.
  -t TABSIZE, --tabsize TABSIZE
                      sets the number of spaces to replace tabs with,
                      default is 2.
```

yamlfixer launches `yamllint` on each specified filename, then parses
its output and tries to fix the reported problems. The special
filename `-` means `stdin`, and is assumed if there's no other
filename argument.

If input is read from `stdin`, the corrected output will be sent to
`stdout`.

Other files will be overwritten if needed. Original files, `stdin`
excepted, can be preserved as `.orig` if the `--backup` command line
option is used. You can specify any other backup filename suffix with
the `--backupsuffix` command line option.

Both summaries and diagnostic information are sent to stderr.

This command exits with status `2` if there are incompatible command
line options. It exits with `-2` if yamllint is not available on your
system. Otherwise it exits with `0` if all input files either are
skipped, entirely fixed, or already successfully passed `yamllint`
strict mode before, else `-1`.

For convenience, all or parts of the command line arguments can be
read from a file, one per line, by using the well known `@argsfile`
syntax.

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
  "fixed": 0,
  "skipped": 0,
  "notwriteable": 0,
  "unknown": 0,
  "details": {
    "/home/jerome/yamlfixer/bad.yml": {
      "status": "PASSED",
      "issues": 0,
      "handled": 0
    }
  },
  "nochangemode": false
}
```

### Check if `yamlfixer` could fix a `yaml` and get the exit code

See how piping fixing and linting can be interesting... and get exit code
so you can go further in automation :

```
yamlfixer <bad.yml | yamllint --format parsable --strict -
echo $?
```
# 🧰 Single purpose tools worth knowing

- [`ytt`](https://carvel.dev/ytt/) : _"YAML templating tool that works on YAML structure (instead of text)."_
- [`jq`](https://stedolan.github.io/jq/) : _"lightweight and flexible command-line JSON processor."_
- [`vimdiff`](https://www.tutorialspoint.com/vim/vim_diff.htm) : _"edit two, three or four versions of a file with Vim and show differences"_
- [`icdiff`](https://www.jefftk.com/icdiff) : _"improved colored diff "_
- [`gomplate`](https://gomplate.ca/) : _"A flexible commandline tool for template rendering. Supports lots of local and remote datasources."_

# 🔖 Related contents

- [Dedicated Post explaining how we are using this project to automate `yaml` linting and fixing](https://dev.to/adriens/let-ci-check-fix-your-yamls-kfa)
- [GH Action relying on this project](https://github.com/marketplace/actions/yaml-fixer)
- [Dedicated Katacoda scenario](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer) so you can see it live
- [Yamlfixer video intro (French, 15')](https://youtu.be/_FiVaMFITkI)
- [From `cli` to community DEV.to blog post](https://dev.to/adriens/we-wanted-to-create-a-tool-to-fix-yamlsthen-we-got-a-community-42ji) to better understand `yamlfixer inception, history`and roadmap

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
