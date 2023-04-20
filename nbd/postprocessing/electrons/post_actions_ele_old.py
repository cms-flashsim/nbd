import numpy as np

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
    "Electron_charge": [["genow", "GenElectron_charge"]],
    "Electron_convVeto": [["d", None, None], ["s"]],
    "Electron_deltaEtaSC": [["s"]],
    "Electron_dr03EcalRecHitSumEt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_dr03HcalDepth1TowerSumEt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_dr03TkSumPt": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_dr03TkSumPtHEEP": [
        ["d", [-np.inf, -2], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_dxy": [["i", np.tan, [150, 0]], ["s"]],
    "Electron_dxyErr": [["i", np.exp, [1, 1e-3]], ["s"]],
    "Electron_dz": [["i", np.tan, [50, 0]], ["s"]],
    "Electron_dzErr": [["i", np.exp, [1, 1e-3]], ["s"]],
    "Electron_eInvMinusPInv": [["i", np.tan, [150, 0]], ["s"]],
    "Electron_energyErr": [["i", np.expm1, [1, 0]], ["s"]],
    "Electron_etaMinusGen": [
        ["i", np.tan, [100, 0]],
        ["s"],
        ["a", "GenElectron_eta"],
        ["rename", "Electron_eta"],
    ],
    "Electron_hoe": [
        ["d", [-np.inf, -6], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_ip3d": [["i", np.exp, [1, 1e-3]], ["s"]],
    "Mlectron_isPFcand": [["d", None, None], ["s"]],
    "Electron_jetPtRelv2": [["i", np.expm1, [1, 0]], ["s"]],
    "Electron_jetRelIso": [["i", np.exp, [10, 1e-2]], ["s"]],
    "Electron_lostHits": [["d", None, None], ["s"]],
    "Electron_miniPFRelIso_all": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_miniPFRelIso_chg": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_mvaFall17V1Iso": [["s"]],
    "Electron_mvaFall17V1Iso_WP80": [["d", None, None], ["s"]],
    "Electron_mvaFall17V1Iso_WP90": [["d", None, None], ["s"]],
    "Electron_mvaFall17V1Iso_WPL": [["d", None, None], ["s"]],
    "Electron_mvaFall17V1noIso": [["s"]],
    "Electron_mvaFall17V1noIso_WP80": [["d", None, None], ["s"]],
    "Electron_mvaFall17V1noIso_WP90": [["d", None, None], ["s"]],
    "Electron_mvaFall17V1noIso_WPL": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2Iso": [["s"]],
    "Electron_mvaFall17V2Iso_WP80": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2Iso_WP90": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2Iso_WPL": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2noIso": [["s"]],
    "Electron_mvaFall17V2noIso_WP80": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2noIso_WP90": [["d", None, None], ["s"]],
    "Electron_mvaFall17V2noIso_WPL": [["d", None, None], ["s"]],
    "Electron_mvaTTH": [["s"]],
    "Electron_pfRelIso03_all": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_pfRelIso03_chg": [
        ["d", [-np.inf, -5.5], np.log(1e-3)],
        ["i", np.exp, [1, 1e-3]],
        ["s"],
    ],
    "Electron_phiMinusGen": [
        ["i", np.tan, [80, 0]],
        ["s"],
        ["a", "GenElectron_phi"],
        ["rename", "Electron_phi"],
    ],
    "Electron_ptRatio": [
        ["i", np.tan, [10, -10]],
        ["s"],
        ["m", "GenElectron_pt"],
        ["rename", "Electron_pt"],
    ],
    "Electron_r9": [["i", np.tan, [10, -0.15]], ["i", np.exp, [1, 1e-2]], ["s"]],
    "Electron_seedGain": [["d", None, None], ["s"]],
    "Electron_sieie": [["i", np.tan, [1, -1.25]], ["i", np.exp, [10, 1e-1]], ["s"]],
    "Electron_sip3d": [["i", np.expm1, [1, 0]], ["s"]],
    "Electron_tightCharge": [["d", None, None], ["s"]],
}
