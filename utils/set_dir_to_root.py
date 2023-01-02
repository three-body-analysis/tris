import os

from utils.get_root import get_project_root


# This is needed because of how I set up the relative file accessing
# It is also very stupid and ugly, I will not do this in the future I hope
def set_dir_to_root():
    ROOT_DIR = get_project_root()
    os.chdir(ROOT_DIR)
