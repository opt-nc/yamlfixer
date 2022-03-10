[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)


# ❔ About

`yamlfixer` automates the fixing of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

# 📑 Prerequisites

In order for it to work, `_yamlfixer_` needs that the following
utilities are already installed on your system, in a directory present
in your `_$PATH_` :

- [x] `_Python_ v3.6` (or higher)
- [x] `_yamllint_ v1.26.3` (or higher)

Then simply copy the `_yamlfixer_` file to a directory present in your
`_$PATH_`, and ensure it is executable, for example:

```shell
cp yamlfixer /usr/local/bin
chmod 0755 /usr/local/bin/yamlfixer
```

# 🚀 Usage

This software automatically fixes some errors and warnings reported by
`_yamllint_`.



```shell
$ yamlfixer [--debug] [--verbose] [--backup] *.yml - thisfile.yaml
```

or:

```shell
$ yamlfixer [--help] [--version]
```

This will launch `_yamllint_` on each specified file name (`-` is `_stdin_`),
then parse its output and try to fix the reported problems.

If input is read from `_stdin_`, the corrected output will be sent to
`_stdout_`.
Other files will be overwritten if needed. Original files,
`_stdin_` excepted, can be preserved as` _.orig_` if the `_--backup_`
command line option is used.

Diagnostic information is sent to stderr in verbose or debug modes.

This command exits with `0` if all input files either are skipped or
successfully pass `_yamllint_` strict mode, else `-1`.

**IMPORTANT:** Not all problems are fixable by `_yamlfixer_`. Due to the
way `_yamllint_` works, it doesn't currenlty report all faulty lines,
`_yamlfixer_` might even introduce indentation problems under some
circumstances.

⚠️**Use at your own risk, you have been warned...** ⚠️

# 🐋 Docker

A Docker image containing `yamlfixer` tool is published on DockerHub on each release.

You can use it this way :

```shell
docker pull optnc/yamlfixer
docker run -i -t --rm optnc/yamlfixer /bin/sh
```

# 🔖 Related contents

- [Dedicated Post explaining how we are using this project to automate `yaml` linting and fixing](https://dev.to/adriens/let-ci-check-fix-your-yamls-kfa)
- [GH Action relying on this project](https://github.com/marketplace/actions/yaml-fixer)

# 📖 Licensing information

```
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
```


# 🧑‍🤝‍🧑 Contact

To contact the authors of this software, simply fill an issue on this project. 

OPT-NC, aka _Office des Postes et Télécommunications de Nouvelle-Calédonie_,
has a corporate website on [www.opt.nc](https://www.opt.nc)
