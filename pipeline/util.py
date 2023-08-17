# pipeline/util.py
import numpy as np

__all__ = [
    "expand_mask",
    "close_to",
    "align_data"
]


def expand_mask(mask: np.ndarray, expand_by: int) -> np.ndarray:
    for i in range(1, expand_by + 1):
        mask[:-1] = mask[:-1] | mask[1:]
        mask[1:] = mask[1:] | mask[:-1]
        # Shifts the mask once per iteration and does a binary or with itself
    return mask


def close_to(x, y, epsilon):
    return ((x <= y) & (y <= x + epsilon)) | ((x - epsilon <= y) & (y <= x))


def align_data(data, new_offset):
    return data - data[0] + new_offset
