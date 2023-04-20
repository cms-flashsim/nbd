import numpy as np


# replicate the actions on the dfm dataframe
gen_dictionary_muons = {
    "MGenMuon_pt": [["t", np.log, [1, 0]]],
    "MClosestJet_pt": [["t", np.log1p, [1, 0]]],
    "MClosestJet_mass": [["t", np.log1p, [1, 0]]],
    "Pileup_sumEOOT": [["t", np.log, [1, 0]]],
    "Pileup_sumLOOT": [["t", np.log1p, [1, 0]]],
}
