# alie

[![pypi badge][pypi_badge]][pypi_base]
[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]

Register aliases with ease 👟

![alie usage][gif]

## Installation

Install from pip:

    pip install alie

Add to your bash profile:

```bash
# make sure aliases are updated after running _alie
alie () { _alie "$@"; source ~/.alie }

# load registered aliases on new shells
source ~/.alie
```

## Usage

List aliases:

    alie

Create new alias:

```bash
alie hello "echo hello world"
```

Delete alias:

    alie hello

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

The intellectual property of this work belongs to Memorial Sloan Kettering Cancer Center. This package was created using [Cookiecutter] and the [leukgen/cookiecutter-toil] project template.

[cookiecutter]: https://github.com/audreyr/cookiecutter
[codecov_badge]: https://codecov.io/gh/jsmedmar/alie/branch/master/graph/badge.svg
[codecov_base]: https://codecov.io/gh/jsmedmar/alie
[pypi_badge]: https://img.shields.io/pypi/v/alie.svg
[pypi_base]: https://pypi.python.org/pypi/alie
[travis_badge]: https://img.shields.io/travis/jsmedmar/alie.svg
[travis_base]: https://travis-ci.org/jsmedmar/alie
[gif]: https://user-images.githubusercontent.com/8843150/44878536-22374a00-ac75-11e8-8ed0-6d69efd2c495.gif
