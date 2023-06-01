import numpy as np

# from nbd.postprocessing.jets.columns_jets import

"""
Dictionary of postprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

unsmearing: ["d", [inf, sup]]
transformation: ["i", func, [a, b]]  # func(x) - b / a

In the case of multiple operations, order follows the operation list indexing.
"""

target_dictionary = {
    "area": [["s"]],
    "bRegCorr": [["s"]],
    "bRegRes": [["s"]],
    "btagDeepFlavB": [["s"]],
    "btagDeepFlavCvB": [["s"]],
    "btagDeepFlavCvL": [["s"]],
    "btagDeepFlavQG": [["s"]],
    "cRegCorr": [["s"]],
    "cRegRes": [["s"]],
    "chFPV0EF": [["s"]],
    "neEmEF": [["s"]],
    "neHEF": [["s"]],
    "puIdDisc": [["s"]],
    "qgl": [["s"]],
    "rawFactor": [["s"]],
    "btagCSVV2": [["d", [-np.inf, -0.01], -1], ["s"]],
    "btagDeepB": [["d", [-np.inf, -0.01], -1], ["s"]],
    "btagDeepCvB": [["d", [-np.inf, -0.01], -1], ["s"]],
    "btagDeepCvL": [["d", [-np.inf, -0.01], -1], ["s"]],
    "chEmEF": [["d", [-np.inf, 0], 0], ["s"]],
    "chHEF": [["i", np.tan, [50, -50]], ["s"]],
    "cleanmask": [["c", 0.5, [0, 1]], ["s"]],
    "etaMinusGen": [["s"], ["a", "GenJet_eta"], ["rename", "Jet_eta"]],
    "hadronFlavour": [["uhf"]],
    "hfadjacentEtaStripsSize": [["c", 0.5, [0, 1]]],
    "hfcentralEtaStripSize": [["c", 0.5, [0, 1]]],
    "hfsigmaEtaEta": [["d", [-np.inf, 0], -1], ["s"]],
    "hfsigmaPhiPhi": [["d", [-np.inf, 0], -1], ["s"]],
    "jetId": [["uj"]],
    "mass": [["s"]],
    "muEF": [["d", [-np.inf, 0], 0], ["s"]],
    "muonSubtrFactor": [["d", [-np.inf, 0], 0], ["s"]],
    "nConstituents": [["d", None, None], ["s"]],
    "nElectrons": [["d", None, None], ["s"]],
    "nMuons": [["d", None, None], ["s"]],
    "partonFlavour": [["upf"]],
    "phiMinusGen": [["s"], ["a", "GenJet_phi"], ["pmp"], ["rename", "Jet_phi"]],
    "ptRatio": [["s"], ["m", "GenJet_pt"], ["rename", "Jet_pt"]],
    "puId": [["upu"]],
}

# overwrite the dict adding Jet_ prefix
target_dictionary_jets = {}
for key, value in target_dictionary.items():
    target_dictionary_jets["Jet_" + key] = value
