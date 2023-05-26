import numpy as np

def get_reco_columns(fields, reco_objects):
    cols = [
        [var for var in fields if var.startswith(f"{obj}_") or var == f"n{obj}"]
        for obj in reco_objects
    ]

    return list(np.concatenate(cols).flat)
