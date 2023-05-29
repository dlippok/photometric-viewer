# Photometric Viewer
GTK 4 based application for viewing IES and LDT photometric files.

![Screenshot](docs/screenshots/Screenshot.png "Screenshot")

## Installation

You can install Photometric viewer by running `pip3` in the root directory:

```shell
pip3 install .
```

## Development

### Set up development environment

First, Python setup virtual environment. As the project requires pygobject packages to be present, the easiest way to setup it is to inherit it from your global site packages:
```shell
python3 -m venv venv --system-site-packages
```

Next, activate your virtual environment and install all  missing dependencies:

```shell
. ./venv/bin/activate
```


### Running tests
```shell
python3 setup.py test
```

### Starting the application

```shell
python3 run.py
```

## Authors

- [Damian Lippok](https://github.com/dlippok)