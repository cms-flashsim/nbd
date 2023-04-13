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

objs_dicts = {
    "Electron": {
    "model_path":"~/FlashSim-Electrons/efficiencies/models/efficiency_electrons.pt",
    "flow_path": "~/wipfs/generation/electrons/EM1/checkpoint-latest.pt",
    }
}

def printtt(model_path, flow_path):
    print(model_path)
    print(flow_path)

obj_keys = ["Electron"]

for obj in obj_keys:
    printtt(**objs_dicts[obj])
    
