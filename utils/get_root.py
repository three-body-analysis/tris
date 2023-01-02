from pathlib import Path


# I wanted this to be recursive but I guess not
def get_project_root() -> Path:
    return Path(__file__).parent.parent
