import os
import ROOT
import awkward as ak
import numpy as np

# path = os.path.join(
#     ".",
#     "..",
#     "FlashSim-Electrons",
#     "extraction",
#     "dataset",
#     "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
# )

# objs_dicts = {
#     "Electron": {
#     "model_path":"~/FlashSim-Electrons/efficiencies/models/efficiency_electrons.pt",
#     "flow_path": "~/wipfs/generation/electrons/EM1/checkpoint-latest.pt",
#     }
# }

# def printtt(model_path, flow_path):
#     print(model_path)
#     print(flow_path)

# obj_keys = ["Electron"]

# for obj in obj_keys:
#     printtt(**objs_dicts[obj])

awk_2 = ak.Array(
    [
        {"Electron_pt": [12, 40], "Electron_eta": [0.4, 0.5]},
        {"Electron_pt": [20.0], "Electron_eta": [0.2]},
        {"Electron_pt": [21.0], "Electron_eta": [0.3]},
    ]
)

awk_2["Mask"] = ak.Array([[True, False], [True], [False]])

a = awk_2["Mask"][awk_2["Mask"]]
print(ak.num(a))
#a.show(limit_cols=1000)

b = awk_2[awk_2["Mask"]]
b.show(limit_cols=1000)