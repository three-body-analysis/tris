# An Automated Screening System for Trinary Star System Candidates

[![Python Package tests status](https://github.com/three-body-analysis/codebase/actions/workflows/python-package.yml/badge.svg)](https://github.com/three-body-analysis/codebase/actions?query=workflow%3Apython-package)
[![Python Package using Conda tests status](https://github.com/three-body-analysis/codebase/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/three-body-analysis/codebase/actions?query=workflow%3Apython-package-conda)
[![Docs CI status](https://github.com/three-body-analysis/codebase/actions/workflows/docs.yml/badge.svg)](https://github.com/three-body-analysis/codebase/actions?query=workflow%3Adocs)




## Basic Guide to Codebase

[//]: # (- `data` - Contains the acquired `.fits` files that contain the light curves for all objects classified as EBs.)
- `datagen` - Contains the data generation and acquisition scheme to get the files in `data`.
- `logbooks` - Personal Logbooks of us determining our ideal algorithm. It uses an older version of the codebase.
- `notebooks` - Notebooks to test our code and visualise them, and also to give examples of usage
- `pipeline` - Currently contains (early-stage) versions of our improved library code that will later be deployed on PyPI.
- `pipelining` - Older versions of `datagen`.
- `src` and `utils` - Older versions of `pipeline`.
- `manual_classification.xlsx` - Post Algorithm Manual Classification done by us.

Do note that in our codebase, you will see references to a `data/` folder. This folder contains the acquired `.fits` 
files that contain the light curves for all objects classified as EBs. You can install this by running 
`datagen/load.sh`.