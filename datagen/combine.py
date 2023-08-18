import os
from astropy.table import Table, vstack
from tqdm import tqdm
from multiprocessing import Pool
import time

rear_codes = {
    "EB_Q0_long": "-2009131105131_llc.fits",
    "EB_Q1_long": "-2009166043257_llc.fits",
    "EB_Q2_long": "-2009259160929_llc.fits",
    "EB_Q3_long": "-2009350155506_llc.fits",
    "EB_Q4_long": "-2010078095331_llc.fits",
    "EB_Q5_long": "-2010174085026_llc.fits",
    "EB_Q6_long": "-2010265121752_llc.fits",
    "EB_Q7_long": "-2010355172524_llc.fits",
    "EB_Q8_long": "-2011073133259_llc.fits",
    "EB_Q9_long": "-2011177032512_llc.fits",
    "EB_Q10_long": "-2011271113734_llc.fits",
    "EB_Q11_long": "-2012004120508_llc.fits",
    "EB_Q12_long": "-2012088054726_llc.fits",
    "EB_Q13_long": "-2012179063303_llc.fits",
    "EB_Q14_long": "-2012277125453_llc.fits",
    "EB_Q15_long": "-2013011073258_llc.fits",
    "EB_Q16_long": "-2013098041711_llc.fits",
    "EB_Q17_long": "-2013131215648_llc.fits"
}


def get_matching_files(data_path, front_code):
    matches = []
    for f in rear_codes.keys():
        temp_path = f + "/" + front_code + rear_codes[f]
        if os.path.exists(data_path + "/" + temp_path):
            matches.append(temp_path)
    return matches


def concatenate_fits(data_path, list_of_filenames, out_path, out_name):
    tables = [Table.read(data_path + "/" + i, format="fits")[["TIME", "SAP_FLUX"]] for i in list_of_filenames]
    combined = vstack(tables, metadata_conflicts="silent")
    combined.write(out_path + "/" + out_name, overwrite="True", format="fits")


def process_file(front_code, data_path="data/unzipped", out_path="data/combined"):
    matches = get_matching_files(data_path, front_code)
    concatenate_fits(data_path, matches, out_path, front_code + ".fits")


def get_all_files(data_path):
    all_files = set()
    all_directories = [dirs for _, dirs, _ in os.walk(data_path)][0]  # This is a little cursed

    for i in all_directories:
        files = os.walk(data_path + "/" + i)
        for file in files:
            for code in file[2]:
                all_files.add(code.split("-")[0])

    return list(all_files)


if __name__ == "__main__":
    all_files = get_all_files("data/unzipped")
    print(all_files)

    now = time.time()

    with Pool(processes=6) as pool:
        pool.map(process_file, tqdm(all_files))

    print(time.time() - now)
