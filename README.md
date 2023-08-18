# An Automated Screening System for Trinary Star System Candidates

[![Python Package tests status](https://github.com/three-body-analysis/codebase/actions/workflows/python-package.yml/badge.svg)](https://github.com/three-body-analysis/codebase/actions?query=workflow%3Apython-package)
[![Python Package using Conda tests status](https://github.com/three-body-analysis/codebase/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/three-body-analysis/codebase/actions?query=workflow%3Apython-package-conda)
[![Docs CI status](https://github.com/three-body-analysis/codebase/actions/workflows/docs.yml/badge.svg)](https://three-body-analysis.github.io/codebase/)

This repository comprises the codebase for our paper, "An Automated Screening System for Trinary Star System Candidates",
that has been submitted to _Physica Scripta_.

This open-source tool offers a specialized method to determine "observed-minus-computed" (OC) diagrams from astronomical
flux time series data (lightcurves) obtained from NASA's Kepler and K2 missions.


## Basic Guide to Codebase

[//]: # (- `data` - Contains the acquired `.fits` files that contain the light curves for all objects classified as EBs.)
- `datagen` - Contains the data generation and acquisition scheme to get the files in `data`.
- `docs` - Contains the documentation code for the codebase.
- `logbooks` - Personal Logbooks of us determining our ideal algorithm. It uses an older version of the codebase.
- `notebooks` - Notebooks to test our code and visualise them, and also to give examples of usage
- `pipeline` - Currently contains (early-stage) versions of our improved library code that will later be deployed on PyPI.
- `pipelining` - Older versions of `datagen`.
- `src` and `utils` - Older versions of `pipeline`.
- `manual_classification.xlsx` - Post Algorithm Manual Classification done by us.

Do note that in our codebase, you will see references to a `data/` folder. This folder contains the acquired `.fits` 
files that contain the light curves for all objects classified as EBs. You can install this by running 
`datagen/load.sh`.

## TODO: Cleanup

This repo is currently being cleaned up to make way for a more organised library structure. The directories 
`pipelining`, `src`, `utils` will soon be removed. Hence, we would recommend not dealing with these directories or 
integrating them into your codebases. Likely, `pipeline` will be renamed to `src`.
