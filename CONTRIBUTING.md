![GitHub](https://img.shields.io/github/license/opt-nc/yamlfixer)

[![Docker Image](https://img.shields.io/badge/docker-homepage-blue)](https://hub.docker.com/r/optnc/yamlfixer)
[![Katacoda scenario](https://img.shields.io/badge/katacoda-homepage-blue)](https://www.katacoda.com/opt-labs/courses/devops-tools/yamlfixer)

![PyPI](https://img.shields.io/pypi/v/yamlfixer-opt-nc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yamlfixer-opt-nc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yamlfixer-opt-nc)

# How to contribute to yamlfixer

Be sure that we will welcome all contributions to `yamlfixer`,
provided they meet the following requirements :

* Each contribution must be licensed under very same terms as
  yamlfixer itself, i.e. the
  [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)
  version 3, or (at your option) any later version.
  
* Each contribution should be kept as simple as possible, and should
  be specific to a particular bug, issue, or feature. For example,
  instead of sending a huge contribution that both fixes an existing
  issue and adds a new feature, please send two smaller contributions
  instead : one which fixes the issue, and the other one which adds
  the new feature.
  
* Each contribution must not make yamlfixer stop to work as expected.

* Each contribution must not make any linter or test suite fail (see
  **Code Quality** below).

* If possible, each contribution should come with a modification to
  yamlfixer's test suite ensuring this contribution works as expected.

## Code Quality

To make the quality of yamlfixer's code improve over time, we currently rely
on linting and testing. Testing is currently a work in progress though...

If you want to increase the chances we will accept your contributions
to this project, you need to install the same tools as us, and use them.

### Installation of developer tools

Simply install them with [pip](https://pip.pypa.io/en/stable/), this
has to be done only once.

```shell
python -m pip install \
    coverage \
    pytest \
    yamllint \
    pylint \
    flake8 \
    flake8-aaa \
    flake8-bugbear \
    flake8-comprehensions \
    flake8-debugger \
    flake8-docstrings \
    flake8-eradicate \
    flake8-expression-complexity \
    flake8-fixme \
    flake8-import-order \
    flake8-markdown \
    flake8-mutable \
    flake8-plugin-utils \
    flake8-polyfill \
    flake8-pytest \
    flake8-pytest-style \
    flake8-simplify \
    flake8-typing-imports \
    flake8-use-fstring \
    flake8-variables-names \
    mccabe \
    pep8-naming \
    pycodestyle \
    pyflakes
```

### Lint, install and test your code

You must then verify that your code works as expected, and doesn't
break either the linting process or the testing process. You can do
this each time with the commands below.

```shell
cd yamlfixer
flake8 .
pylint yamlfixer
python -m pip install --force-reinstall .
coverage run --source=yamlfixer -m unittest discover
rm -fr build yamlfixer_opt_nc.egg-info
```

If none of the above commands gives an error, then your code is ready
to be submitted to https://github.com/opt-nc/yamlfixer/pulls so feel 
free to do so.
