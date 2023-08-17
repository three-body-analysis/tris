import requests
from tqdm import tqdm

EB_URL = "https://archive.stsci.edu/pub/kepler/lightcurves/tarfiles/EclipsingBinaries/"

for i in tqdm(range(0, 18)):
    r = requests.get(EB_URL + "EB_Q" + str(i) + "_long.tgz", allow_redirects=True)
    with open("data/zipped/EB_Q" + str(i) + "_long.tgz", "wb+") as f:
        f.write(r.content)

