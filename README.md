
[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)
[![Kataocda scenario](https://img.shields.io/badge/katacoda-homepage-blue)](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer)


# ❔ About

[yamlfixer](https://github.com/opt-nc/yamlfixer) automates the fixing
of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

# 📑 Prerequisites

💡 **You can try the install process online thanks to the dedicated [Katacoda scenario](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer).**

In order for it to work, `yamlfixer` needs that the following
utilities are already installed on your system, in a directory present
in your `$PATH` :

- [x] `Python v3.6` (or higher)
- [x] `yamllint v1.26.3` (or higher)

Then simply copy the `yamlfixer` file to a directory present in your
`$PATH`, and ensure it is executable, for example:

```shell
cp yamlfixer /usr/local/bin
chmod 0755 /usr/local/bin/yamlfixer
```


# 🚀 Usage

This software automatically fixes some errors and warnings reported by
`yamllint`.



```shell
$ yamlfixer [--debug] [--verbose] [--backup] *.yml - thisfile.yaml
```

or:

```shell
$ yamlfixer [--help] [--version]
```

This will launch `yamllint` on each specified filename, then parse its
output and try to fix the reported problems. The special filename `-`
means `stdin`, and is assumed if there's no other filename argument.

If input is read from `stdin`, the corrected output will be sent to
`stdout`.
Other files will be overwritten if needed. Original files,
`stdin` excepted, can be preserved as `.orig` if the `--backup`
command line option is used.

Diagnostic information is sent to stderr in verbose or debug modes.

This command exits with `0` if all input files either are skipped or
successfully pass `yamllint` strict mode, else `-1`.

**IMPORTANT:** Not all problems are fixable by `yamlfixer`. Due to the
fact that `yamllint` doesn't currently report all faulty lines,
`yamlfixer` might even introduce indentation problems under some
circumstances.

⚠️**Use at your own risk, you have been warned...** ⚠️

# 🐋 Docker

A Docker image containing `yamlfixer` tool is [published on DockerHub](https://hub.docker.com/r/optnc/yamlfixer)
so **you don't have to deal with prerequisites.**

Install it :

```shell
alias yamlfixer="docker run --rm optnc/yamlfixer yamlfixer"
```

Use it :

```shell
yamlfixer --version
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

To contact the authors of this software, simply fill an issue on this project. 

OPT-NC, aka _Office des Postes et Télécommunications de Nouvelle-Calédonie_,
has a corporate website on [www.opt.nc](https://www.opt.nc)
