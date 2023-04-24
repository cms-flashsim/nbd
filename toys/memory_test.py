import os
import json
import ROOT
import awkward as ak
import numpy as np

awk = ak.Array(
    [
        {"pt": [21.6], "eta": [0.108], "scalar": 15.8},
        {"pt": [], "eta": [], "scalar": 16.2},
        {"pt": [56], "eta": [0.6], "scalar": 0},
    ]
)

awk = ak.Array(
    [
        {"Electron_pt": [21.6], "Electron_eta": [0.108], "Muon_pt": [15.8]},
        {"Electron_pt": [], "Electron_eta": [], "Muon_pt": [16.2]},
        {"Electron_pt": [56], "Electron_eta": [0.6], "Muon_pt": []},
    ]
)


awk = ak.Array(
    [
        {"Electron_pt": [21.6, 53, 9], "Electron_eta": [0.108, 0.3, 0.1]},
        {"Electron_pt": [], "Electron_eta": []},
        {"Electron_pt": [12], "Electron_eta": [0.6]},
    ]
)

awk = awk[ak.argsort(awk["Electron_pt"], axis=1, ascending=False, highlevel=False)]

awk.show(limit_cols=1000)


ele = {"Electron_pt": awk.Electron_pt, "Electron_eta": awk.Electron_eta}
# muo = {"Muon_pt": awk.Muon_pt}

df_ele = ak.to_rdataframe(ele)

df_ele.Snapshot("ele", "test.root")

# del df_ele

# df_muo = ak.to_rdataframe(muo)

# opts = ROOT.RDF.RSnapshotOptions()
# opts.fMode = "UPDATE"

# df_muo.Snapshot("muo", "test.root", "", opts)

# path = os.path.join(
#     ".",
#     "..",
#     "FlashSim-Electrons",
#     "extraction",
#     "dataset",
#     "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
# )

# events = uproot.open(f"{path}:Events")

# special = [
#     "GenJetAK8",
#     "HLTriggerFinalPath",
#     "HLTriggerFirstPath",
#     "L1Reco",
#     "L1simulation",
#     "LHEPart",
#     "LHEPdfWeight",
#     "LHEReweightingWeight",
#     "LHEScaleWeight",
#     "LHEWeight",
#     "SoftActivityJetHT",
#     "SoftActivityJetHT10",
#     "SoftActivityJetHT2",
#     "SoftActivityJetHT5",
#     "SoftActivityJetNjets10",
#     "SoftActivityJetNjets2",
#     "SoftActivityJetNjets5",
#     "fixedGridRhoFastjetCentralCalo",
#     "fixedGridRhoFastjetCentralChargedPileUp",
#     "fixedGridRhoFastjetCentralNeutral",
# ]

# probl = [
#     "GenJet",
#     "HLT",
#     "L1",
#     "LHE",
#     "SoftActivityJet",
#     "SoftActivityJetHT",
#     "fixedGridRhoFastjetCentral",
# ]

# d = {}

# for var in events.keys():
#     for collection in collections:
#         if var.startswith(collection):
#             if collection in probl:
#                 if np.any([var.startswith(s) for s in special]):
#                     pass
#                 else:
#                     if collection not in d:
#                         if "_" in var:
#                             d[collection] = [var.replace(f"{collection}_", "", 1)]
#                         else:
#                             d[collection] = [var]
#                     else:
#                         if "_" in var:
#                             d[collection].append(var.replace(f"{collection}_", "", 1))
#                         else:
#                             d[collection].append(var)
#             else:
#                 if collection not in d:
#                     if "_" in var:
#                         d[collection] = [var.replace(f"{collection}_", "", 1)]
#                     else:
#                         d[collection] = [var]
#                 else:
#                     if "_" in var:
#                         d[collection].append(var.replace(f"{collection}_", "", 1))
#                     else:
#                         d[collection].append(var)

# d["SoftActivityJetHT"] = ["SoftActivityJetHT"]

# sorted_dict = {key: value for key, value in sorted(d.items())}
# sorted_dict = {key: sorted(value) for key, value in sorted_dict.items()}


# with open("collections.json", "w") as f:
#     json.dump(sorted_dict, f, indent=4)
