import numpy as np

"""
Dictionary of postprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

unsmearing: ["d", [inf, sup]]
transformation: ["i", func, [a, b]]  # (func(x) - b) / a

In the case of multiple operations, order follows the operation list indexing.
"""


target_dictionary_muons = {
    "Muon_etaMinusGen": [
        ["i", np.tan, [100, 0]],
        ["s"],
        ["a", "MGenMuon_eta"],
        ["rename", "Muon_eta"],
    ],
    "Muon_phiMinusGen": [
        ["i", np.tan, [80, 0]],
        ["s"],
        ["a", "MGenMuon_phi"],
        ["pmp"],
        ["rename", "Muon_phi"],
    ],
    "Muon_ptRatio": [
        ["i", np.tan, [10, -10]],
        ["s"],
        ["m", "MGenMuon_pt"],
        ["rename", "Muon_pt"],
    ],
    "Muon_dxy": [["i", np.tan, [150, 0]], ["s"]],
    "Muon_dxyErr": [["i", np.expm1, [1, 0]], ["s"]],
    "Muon_dz": [["i", np.tan, [50, 0]], ["s"]],
    "Muon_dzErr": [["i", np.exp, [1, 0.001]]],
    "Muon_ip3d": [["i", np.exp, [1, 0.001]]],
    "Muon_jetPtRelv2": [["d", [-np.inf, -4], -6.9], ["i", np.exp, [1, 0.001]]],
    "Muon_jetRelIso": [["i", np.exp, [1, 0.08]]],
    "Muon_pfRelIso04_all": [
        ["d", [-np.inf, -7.5], -11.51],
        ["i", np.exp, [1, 0.00001]],
    ],
    "Muon_pfRelIso03_all": [
        ["d", [-np.inf, -7.5], -11.51],
        ["i", np.exp, [1, 0.00001]],
    ],
    "Muon_pfRelIso03_chg": [
        ["d", [-np.inf, -7.5], -11.51],
        ["i", np.exp, [1, 0.00001]],
    ],
    "Muon_ptErr": [["i", np.exp, [1, 0.001]]],
    "Muon_sip3d": [["i", np.exp, [1, 1]]],
    "Muon_isGlobal": [["c", 0.5, [0, 1]]],
    "Muon_isPFcand": [["c", 0.5, [0, 1]]],
    "Muon_isTracker": [["c", 0.5, [0, 1]]],
    "Muon_mediumId": [["c", 0.5, [0, 1]]],
    "Muon_softId": [["c", 0.5, [0, 1]]],
    "Muon_softMvaId": [["c", 0.5, [0, 1]]],
    "Muon_charge": [["genow", "MGenMuon_charge"]],
}
