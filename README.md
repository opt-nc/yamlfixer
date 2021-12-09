# yamlfixer
Automates the fixing of problems reported by
[yamllint](https://github.com/adrienverge/yamllint) by parsing its
output.

This software automatically fixes some errors and warnings reported by
yamllint.

usage:

```
$ yamlfixer *.yml - thisfile.yaml
```

This will launch yamllint on each specified file name (`-` is _stdin_),
then parse its output and try to fix reported problems in that file.

If input is read from _stdin_, the corrected output will be sent to
_stdout_. Other files will be overwritten if needed.

Diagnostic information is sent to stderr.

**IMPORTANT:** Not all problems are fixable by _yamlfixer_. Due to the way
[yamllint](https://github.com/adrienverge/yamllint) works, it doesn't
currenlty report all faulty lines, _yamlfixer_ might even introduce
indentation problems under some circumstances. Use at your own risk,
you have been warned...
