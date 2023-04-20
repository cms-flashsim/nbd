import numpy as np

reco_objects = ["Electron", "Muon", "Jet"]


def get_reco_columns(fields):
    cols = np.array(
        [
            [var for var in fields if var.startswith(f"{obj}_") or var == f"n{obj}"]
            for obj in reco_objects
        ]
    )
    return cols.flatten()
