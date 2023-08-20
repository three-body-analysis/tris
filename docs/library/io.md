# Input/Output

!!! Info "Note"
    This library currently supports `pandas.DataFrame` objects, and `fits`, `excel`, `csv` and `json` file types. 
    Further developments would involve adding support for light curves from 
    [`lightkurve`](https://docs.lightkurve.org/). Stay tuned for updates!


Tris offers a very simple wrapper to read your files into proper `pandas.DataFrame` objects that can be fed into 
subsequent algorithms. Literally, it's as simple as just:

```py
>>> tris.read("data/combined/kplr001026032.fits")
            time          flux
0     131.512714  12319.001953
1     131.533148  12321.861328
2     131.553583  12317.918945
3     131.574017  12307.453125
4     131.594452  12308.416992
...          ...           ...
1619  164.902637  12541.321289
1620  164.923071  12549.753906
1621  164.943505  12551.208008
1622  164.963939  12547.056641
1623  164.984374  12547.208008

[1624 rows x 2 columns]
```

The data reading algorithm for Tris is quite simple, and there are specific functions available for different formats.
The `read_csv`, `read_json`, `read_fits` and `read_excel` functions help us read the 

