# Tris

[![Python Package tests status](https://github.com/three-body-analysis/tris/actions/workflows/python-package.yml/badge.svg)](https://github.com/three-body-analysis/tris/actions?query=workflow%3Apython-package)
[![Docs CI status](https://github.com/three-body-analysis/tris/actions/workflows/docs.yml/badge.svg)](https://three-body-analysis.github.io/tris/)
[![PyPI Latest Release](https://img.shields.io/pypi/v/tris.svg)](https://pypi.org/project/tris/)
[![PyPI Downloads](https://static.pepy.tech/badge/tris)](https://pepy.tech/project/tris)

This repository comprises the codebase for our paper, "Tris: A Screening System for Trinary Star System Candidates",
that is in the process of being submitted to _The Astronomical Journal_.

**Tris** (**Tri**nary **S**creener) is an open-source tool that offers a specialized method to determine "observed-minus-computed" (OC) diagrams from 
astronomical flux time series data (lightcurves) obtained from NASA's Kepler and K2 missions.

Here is a brief outline of the algorithm:

<p align="center">
    <img src="img/methodology.png" alt="Diagram of Algorithm"/><br>
    <span>Diagram of Algorithm.</span>
</p>

Basic Guide to Codebase
-------------

[//]: # (- `data` - Contains the acquired `.fits` files that contain the light curves for all objects classified as EBs.)
[//]: # (- `logbooks` - Personal Logbooks of us determining our ideal algorithm. It uses an older version of the codebase.)
[//]: # (- `pipelining` - Older versions of `datagen`.)
- `datagen` - Contains the data generation and acquisition scheme to get the files in `data`.
- `docs` - Contains the documentation code for the codebase.
- `notebooks` - Notebooks to test our code and visualise them, and also to give examples of usage
- `old` - Older versions of `tris`. Also contains logbooks of our work.
- `tris` - Currently contains (early-stage) versions of our improved library code that will later be deployed on PyPI.
- `manual_classification.xlsx` - Post Algorithm Manual Classification done by us.

Do note that in our codebase, you will see references to a `data/` folder. This folder contains the acquired `.fits` 
files that contain the light curves for all objects classified as EBs. You can install this by running 
`datagen/load.sh` (from the project root).

Documentation
-------------

Read the documentation at [`https://three-body-analysis.github.io/tris/`](https://three-body-analysis.github.io/tris/).


Setup and Installation
-------------

### Installing from PyPI

Yes, we have published `tris` on PyPI! To install `tris` and all its dependencies, the easiest method would be to use 
`pip` to query PyPI. This should, by default, be present in your Python installation. To, install run the following 
command in a terminal or Command Prompt / Powershell:

```bash
$ pip install tris
```

Depending on the OS, you might need to use `pip3` instead. If the command is not found, you can choose to use the
following command too:

```bash
$ python -m pip install tris
```

Here too, `python` or `pip` might be replaced with `py` or `python3` and `pip3` depending on the OS and installation 
configuration. If you have any issues with this, it is always helpful to consult 
[Stack Overflow](https://stackoverflow.com/).

### Installing from Source

To install from source, you need to get the following:

#### Git

Git is needed to install this repository. This is not completely necessary as you can also install the zip file for this 
repository and store it on a local drive manually. To install Git, follow 
[this guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

After you have successfully installed Git, you can run the following command in a terminal / Command Prompt etc:

```bash
$ git clone https://github.com/three-body-analysis/tris.git
```

This stores a copy in the folder `tris`. You can then navigate into it using `cd tris`.

#### Poetry

This project can be used easily via a tool know as Poetry. This allows you to easily reflect edits made in the original 
source code! To install `poetry`, you can also install it using `pip` by typing in the command as follows:

```bash
$ pip install poetry
```

Again, if you have any issues with `pip`, check out [here](#installing-from-pypi).

After this, you can use the following command to install this library:

```bash
$ poetry install
```


> [!WARNING]  
> Note that this is part of a research work in the process of being published, hence this codebase will not be exceedingly updated. [Issues](https://github.com/three-body-analysis/tris/issues) and [Pull Requests](https://github.com/three-body-analysis/tris/pulls) are appreciated, so that we can work to make this library more usable by the larger astronomical community.

