import requests

url = "https://archive.stsci.edu/pub/kepler/lightcurves/tarfiles/EclipsingBinaries/"
for i in range(0, 18):
    if i not in [999]:  # This is just a filter if you aborted a download halfway
        r = requests.get(url + "EB_Q" + str(i) + "_long.tgz", allow_redirects=True)
        open("data/zipped/EB_Q" + str(i) + "_long.tgz", "wb").write(r.content)
