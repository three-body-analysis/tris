import numpy as np


def expand_mask(mask: np.ndarray, expand_by: int):
    for i in range(1, expand_by + 1):
        mask[:-1] = mask[:-1] | mask[1:]
        mask[1:] = mask[1:] | mask[:-1]
        # Shifts the mask once per iteration and does a binary or with itself
    return mask
