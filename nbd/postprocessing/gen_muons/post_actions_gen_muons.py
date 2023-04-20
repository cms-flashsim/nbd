import numpy as np


# replicate the actions on the dfm dataframe
cond_dictionary_muons = {
    "MGenMuon_pt": [["i", np.exp, [1, 0]]],
    "MClosestJet_pt": [["i", np.expm1, [1, 0]]],
    "MClosestJet_mass": [["i", np.expm1, [1, 0]]],
    "Pileup_sumEOOT": [["i", np.exp, [1, 0]]],
    "Pileup_sumLOOT": [["i", np.expm1, [1, 0]]],
}
