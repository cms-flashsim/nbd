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

target_dictionary = {
    "mvaLowPt": [["s"]],
    "mvaTTH": [["s"]],
    "filteredphi": [["s"]],
    "segmentComp": [["s"]],
    "softMva": [["s"]],
    "cleanmask": [["c", 0.5, [0, 1]], ["s"]],
    "highPtId": [["d", None, None], ["s"]],
    "highPurity": [["c", 0.5, [0, 1]], ["s"]],
    "inTimeMuon": [["c", 0.5, [0, 1]], ["s"]],
    "isStandalone": [["c", 0.5, [0, 1]], ["s"]],
    "looseId": [["c", 0.5, [0, 1]]],
    "mediumPromptId": [["c", 0.5, [0, 1]]],
    "miniIsoId": [["d", None, None]],
    "multiIsoId": [["d", None, None]],
    "mvaId": [["d", None, None]],
    "mvaLowPtId": [["d", None, None]],
    "nStations": [["d", None, None], ["s"]],
    "nTrackerLayers": [["d", None, None], ["s"]],
    "pfIsoId": [["d", None, None]],
    "puppiIsoId": [["d", None, None]],
    "tightCharge": [["c", 1, [0, 2]], ["s"]],
    "tightId": [["c", 0.5, [0, 1]]],
    "tkIsoId": [["c", 1.5, [1, 2]]],
    "triggerIdLoose": [["c", 0.5, [0, 1]]],
    "etaMinusGen": [
        ["i", np.tan, [100, 0]],
        ["s"],
        ["a", "MGenMuon_eta"],
        ["rename", "Muon_eta"],
    ],
    "phiMinusGen": [
        ["i", np.tan, [80, 0]],
        ["s"],
        ["a", "MGenMuon_phi"],
        ["pmp"],
        ["rename", "Muon_phi"],
    ],
    "ptRatio": [
        ["i", np.tan, [10, -10]],
        ["s"],
        ["m", "MGenMuon_pt"],
        ["rename", "Muon_pt"],
    ],
    "dxy": [["i", np.tan, [150, 0]], ["s"]],
    "dxyErr": [["i", np.expm1, [1, 0]], ["s"]],
    "dxybs": [["i", np.tan, [50, 0]], ["s"]],
    "dz": [["i", np.tan, [50, 0]], ["s"]],
    "dzErr": [["i", np.exp, [1, 0.001]], ["s"]],
    "ip3d": [["i", np.exp, [1, 0.001]], ["s"]],
    "jetPtRelv2": [
        ["d", [-np.inf, -4], np.log(0.001)],
        ["i", np.exp, [1, 0.001]],
        ["s"],
    ],
    "jetRelIso": [["i", np.exp, [1, 0.08]], ["s"]],
    "pfRelIso04_all": [
        ["d", [-np.inf, -7.5], np.log(0.00001)],
        ["i", np.exp, [1, 0.00001]],
        ["s"],
    ],
    "pfRelIso03_all": [
        ["d", [-np.inf, -7.5], np.log(0.00001)],
        ["i", np.exp, [1, 0.00001]],
        ["s"],
    ],
    "pfRelIso03_chg": [
        ["d", [-np.inf, -7.5], np.log(0.00001)],
        ["i", np.exp, [1, 0.00001]],
        ["s"],
    ],
    "miniPFRelIso_all": [
        ["d", [-np.inf, -6.5], np.log(0.001)],
        ["i", np.exp, [1, 0.001]],
        ["s"],
    ],
    "miniPFRelIso_chg": [
        ["d", [-np.inf, -6.5], np.log(0.001)],
        ["i", np.exp, [1, 0.001]],
        ["s"],
    ],
    "tkRelIso": [
        ["d", [-np.inf, -6.5], np.log(0.001)],
        ["i", np.exp, [1, 0.001]],
        ["s"],
    ],
    "ptErr": [["i", np.exp, [1, 0.001]], ["s"]],
    "sip3d": [["i", np.exp, [1, 1]], ["s"]],
    "isGlobal": [["c", 0.5, [0, 1]], ["s"]],
    "isPFcand": [["c", 0.5, [0, 1]], ["s"]],
    "isTracker": [["c", 0.5, [0, 1]], ["s"]],
    "mediumId": [["c", 0.5, [0, 1]]],
    "softId": [["c", 0.5, [0, 1]]],
    "softMvaId": [["c", 0.5, [0, 1]]],
    "charge": [["c", 0.0, [-1, 1]]],
}

target_dictionary_muons = {}
for key, value in target_dictionary.items():
    target_dictionary_muons["Muon_" + key] = value
