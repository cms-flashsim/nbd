import numpy as np

reco_objects = ["Electron", "Muon", "Jet"]


def get_reco_columns(fields):
    cols = [
        [var for var in fields if var.startswith(f"{obj}_") or var == f"n{obj}"]
        for obj in reco_objects
    ]

    return list(np.concatenate(cols).flat)


x = get_reco_columns(["Electron_pt", "Muon_pt", "Jet_pt"])
