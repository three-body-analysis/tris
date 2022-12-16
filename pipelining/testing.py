import astropy

from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt

from astroquery.mast import Mast, Observations

filename = "data/kplr004940201-2013131215648_llc.fits"

fits.info(filename)

