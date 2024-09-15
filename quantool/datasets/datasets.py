import numpy as np


def load_dict_of_vec() -> dict:
    """Load 3 lists of numbers in a dictionary."""
    return {
        "a": list(range(1, 10)),
        "b": list(range(4, 13)),
        "c": list(range(7, 16)),
    }
