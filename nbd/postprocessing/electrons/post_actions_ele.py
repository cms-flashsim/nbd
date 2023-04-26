import numpy as np

# NOTE need to fix unsmearing ops
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
    "MElectron_charge": [["c", 0, [-1, 1]]],
    "MElectron_convVeto": [["d", None, None], ["s"]],
    "MElectron_deltaEtaSC": [["i", np.tan, [10, 0]], ["s"]],
    "MElectron_dr03EcalRecHitSumEt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_dr03HcalDepth1TowerSumEt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_dr03TkSumPt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_dr03TkSumPtHEEP": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_dxy": [["i", np.tan, [20, 0]], ["s"]],
    "MElectron_dxyErr": [["i", np.exp, [1, 1e-3]], ["s"]],
    "MElectron_dz": [["i", np.tan, [10, 0]], ["s"]],
    "MElectron_dzErr": [["i", np.exp, [1, 1e-3]], ["s"]],
    "MElectron_eInvMinusPInv": [["i", np.tan, [10, 0]], ["s"]],
    "MElectron_energyErr": [["i", np.expm1, [1, 0]], ["s"]],
    "MElectron_etaMinusGen": [
        ["i", np.tan, [20, 0]],
        ["s"],
        ["a", "GenElectron_eta"],
        ["rename", "Electron_eta"],
    ],
    "MElectron_hoe": [["d", [-np.inf, -6]], ["i", np.exp, [1, 1e-3]], ["s"]],
    "MElectron_ip3d": [["i", np.exp, [1, 1e-3]], ["s"]],
    "MElectron_isPFcand": [["d", None, None], ["s"]],
    "MElectron_jetPtRelv2": [["i", np.expm1, [1, 0]], ["s"]],
    "MElectron_jetRelIso": [["i", np.exp, [10, 1e-2]], ["s"]],
    "MElectron_lostHits": [["d", None, None], ["s"]],
    "MElectron_miniPFRelIso_all": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_miniPFRelIso_chg": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_mvaFall17V1Iso": [["s"]],
    "MElectron_mvaFall17V1Iso_WP80": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V1Iso_WP90": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V1Iso_WPL": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V1noIso": [["s"]],
    "MElectron_mvaFall17V1noIso_WP80": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V1noIso_WP90": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V1noIso_WPL": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2Iso": [["s"]],
    "MElectron_mvaFall17V2Iso_WP80": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2Iso_WP90": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2Iso_WPL": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2noIso": [["s"]],
    "MElectron_mvaFall17V2noIso_WP80": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2noIso_WP90": [["d", None, None], ["s"]],
    "MElectron_mvaFall17V2noIso_WPL": [["d", None, None], ["s"]],
    "MElectron_mvaTTH": [["s"]],
    "MElectron_pfRelIso03_all": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_pfRelIso03_chg": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "MElectron_phiMinusGen": [
        ["i", np.tan, [20, 0]],
        ["s"],
        ["a", "GenElectron_phi"],
        ["rename", "Electron_phi"],
    ],
    "MElectron_ptRatio": [["s"], ["m", "GenElectron_pt"], ["rename", "Electron_pt"]],
    "MElectron_r9": [["i", np.exp, [1, 1e-2]], ["s"]],
    "MElectron_seedGain": [["d", None, None], ["s"]],
    "MElectron_sieie": [["i", np.exp, [10, 1e-1]], ["s"]],
    "MElectron_sip3d": [["i", np.expm1, [1, 0]], ["s"]],
    "MElectron_tightCharge": [["d", None, None], ["s"]],
}
