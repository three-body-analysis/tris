# Data Generation and Acquisition Scheme

The data is acquired from [here](https://archive.stsci.edu/pub/kepler/lightcurves/tarfiles/EclipsingBinaries/).

We download all `.tgz` files from here, and untar them.

Following this, we are able to combine light curves via the Kepler ID and then get our final TAR files.

To run this, you simply need to run `load.sh`, either using `bash` or `sh`.

This also ideally works on Windows with Git Bash.