![License](https://img.shields.io/github/license/opt-nc/yamlfixer) ![Build](https://img.shields.io/github/workflow/status/opt-nc/yamlfixer/Checks)

[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)
[![Katacoda scenario](https://img.shields.io/badge/katacoda-homepage-blue)](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer)

![PyPI](https://img.shields.io/pypi/v/yamlfixer-opt-nc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yamlfixer-opt-nc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yamlfixer-opt-nc)

# ![yamlfixer's logo](https://github.com/opt-nc/yamlfixer/blob/main/logo/candidates/1-64x64.png) `yamlfixer`

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


## 🐧 Linux install

```shell
python3 -m pip install yamlfixer-opt-nc
```

## 🪟 Windows install

```shell
python -m pip install yamlfixer-opt-nc
```
## `pipx` setup

For an optimal experience we recommand using [`pipx`](https://pypa.github.io/pipx/).

To install : 

```shell
pipx install yamlfixer-opt-nc
pipx list
```

To upgrade : 

```shell
pipx upgrade yamlfixer-opt-nc
```

To uninstall :

```
pipx uninstall yamlfixer-opt-nc
```

# 🚀 Usage

This software automatically fixes some errors and warnings reported by
`yamllint`.

```shell
usage: yamlfixer [-h] [-v] [-b] [-B BACKUPSUFFIX] [-d] [-D DIFF_FILE] [-e EXTENSIONS] [-f]
                 [-F] [-l] [-N] [-n] [-r LEVEL] [-j | -p | -s] [-t TABSIZE]
                 [-c CONFIG_FILE | -C CONFIG_DATA]
                 [FILE_or_DIR [FILE_or_DIR ...]]

Fix formatting problems in YAML documents. If no file is specified, then reads input from `stdin`.

positional arguments:
  FILE_or_DIR           the YAML files to fix. Use `-` to read from `stdin`.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         display this program's version number and exit.
  -b, --backup          make a backup copy of original files.
  -B BACKUPSUFFIX, --backupsuffix BACKUPSUFFIX
                        sets the suffix for backup files, `.orig` is the default.
  -d, --debug           output debug information to stderr.
  -D DIFF_FILE, --diffto DIFF_FILE
                        name of the file a unified diff will be written to.
                        Defaults to `/dev/null`.
  -e EXTENSIONS, --ext EXTENSIONS
                        comma separated list of acceptable extensions when searching directories
                        for YAML files. Defaults to `yaml,yml,yamllint`.
  -f, --forcecolors     force colorized output even if stream is not a TTY.
  -F, --followsymlinks  follow symbolic links when recursing directories.
  -l, --listfixers      output the list of available fixers.
  -N, --nosyntax        don't try to fix syntax errors.
  -n, --nochange        don't modify anything.
  -r LEVEL, --recurse LEVEL
                        sets the maximum recursion level for directories. Default is `0` meaning
                        no recursion, and any negative value means no limit.
  -j, --jsonsummary     output JSON summary to stderr.
  -p, --plainsummary    output plain text summary to stderr.
  -s, --summary         output colorized plain text summary to stderr. If stderr is not a TTY
                        output is identical to --plainsummary unless --forcecolors is also used.
  -t TABSIZE, --tabsize TABSIZE
                        sets the number of spaces to replace tabs with, default is `2`.
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        path to yamllint's custom configuration file, none by default.
  -C CONFIG_DATA, --config-data CONFIG_DATA
                        custom configuration for yamllint as YAML source, none by default.
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
syntax. For example you could do something like this :

```shell
$ find . -type f -name "*.yml" >list-of-yaml-files
$ yamlfixer --nochange --summary @list-of-yaml-files
```

Although this could probably be shortened to :

```shell
$ yamlfixer --nochange --summary --recurse -1 .
```

**IMPORTANT:** Not all problems are fixable by `yamlfixer`. Due to the
fact that `yamllint` doesn't currently report all faulty lines,
`yamlfixer` might even introduce indentation problems under some
circumstances.

⚠️**Use at your own risk, you have been warned...** ⚠️

# GitHub Action

You can now use this software as a GitHub Action, available from https://github.com/opt-nc/yamlfixer-action .
This GitHub Action will automatically create Pull Requests to your repository with the changes made by yamlfixer.

# Fixers

yamlfixer currently (as of 0.9.6) can fix the following problems as reported by `yamllint` :

  - comment not indented like content (comments-indentation)
  - found forbidden document end
  - found forbidden document start
  - line too long
  - missing document end
  - missing document start
  - missing starting space in comment (comments)
  - no new line character at the end of file
  - syntax error: expected `'<document start>'`, but found `'<stream end>'` (syntax)
  - syntax error: expected `<block end>`, but found `'<block mapping start>'`
  - syntax error: expected `<block end>`, but found `'<block sequence start>'` (syntax)
  - syntax error: expected `<block end>`, but found `'?'`
  - syntax error: found character '\t' that cannot start any token (syntax)
  - syntax error: mapping values are not allowed here
  - too few spaces after comma (commas)
  - too few spaces before comment (comments)
  - too few spaces inside empty brackets (brackets)
  - too few spaces inside brackets
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

An always up-to-date list of fixers can be obtained with `yamlfixer --listfixers`.

Please read our [TODO list](https://github.com/opt-nc/yamlfixer/blob/main/TODO.md)
to see which problems are still unsupported but which we plan to support some day.

**IMPORTANT : fixing syntax errors is done on a best effort basis and
may work only partially or not at all for you. Use the -N|--nosyntax
command line switch do prevent `yamlfixer` from trying to fix syntax
errors.**

# 💪 Tips and tricks

Find here a set of tips & tricks about how to achieve great things.

Don't find the usecase you're looking for ➡️ [🎫 Fill a dedicated issue so we could share your idea with the comunity](https://github.com/opt-nc/yamlfixer/issues/new?assignees=&labels=help+wanted&template=ask-for-command-line-script---.md&title=Request+for+script+or+oneLiner)

## ⏩ One liners

Most of us love short and efficient command lines. Here are some ready to use ones : 

### Piping `json` summary through `jq`

```
yamlfixer --jsonsummary examples/good.yml 2>&1 | jq
```

So you can get a nicely colorized (and validated `json` output) : 

```json
{
  "filestofix": 1,
  "passed": 1,
  "modified": 0,
  "fixed": 0,
  "skipped": 0,
  "notwritable": 0,
  "unknown": 0,
  "nochangemode": false,
  "details": {
    "examples/good.yml": {
      "numericstatus": 0,
      "status": "PASSED",
      "issues": 0,
      "handled": 0
    }
  }
}
```

### Check if `yamlfixer` could fix a `yaml` and get the exit code

See how to produce a patch file without modifying the original one,
and get the exit code so you can go further in automation :

```shell
$ yamlfixer --nochange --summary --diffto my.patch examples/bad.yml
Files to fix: 1
0 files were already correct before
0 files were modified but problems remain
1 files were entirely fixed
0 files were skipped
0 files were not writable
0 files with unknown status
      FIXED examples/bad.yml (handled 4/4)
WARNING: No file was modified per user's request !

$ echo $?
0

$ cat my.patch
diff -u "examples/bad.yml" "examples/bad.yml-after"
--- "examples/bad.yml"
+++ "examples/bad.yml-after"
@@ -1,4 +1,4 @@
-
+---
 name: Build HelloYaml

 # yamllint disable-line rule:truthy
@@ -17,6 +17,4 @@
           cache: 'maven'

       - name: Build with Maven
-          run: mvn package
-
-
+        run: mvn package
$ 
```

You can then manually apply the patch file to modify `examples/bad.yml` if
that's what you want to do :

```shell
$ patch -p0 <my.patch
patching file examples/bad.yml
$
```

But of course, it would have been simpler to not use the `--nochange`
command line option in the first place, so that the file would have
been fixed automatically.

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

# Contributing

You can contribute to this project by [filing an issue](https://github.com/opt-nc/yamlfixer/issues)
or by [sending a pull request](https://github.com/opt-nc/yamlfixer/pulls)

Please read our [contributing guidelines](https://github.com/opt-nc/yamlfixer/blob/main/CONTRIBUTING.md)
before.


# 🧑‍🤝‍🧑 Contact

To contact the [authors](AUTHORS.md) of this software, simply fill an
issue on this project.

OPT-NC, aka _Office des Postes et Télécommunications de Nouvelle-Calédonie_, check
[`OPT-NC`](https://github.com/opt-nc) Github Organization page for more.
