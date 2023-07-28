fatjet_cond = [
    "MgenjetAK8_pt",
    "MgenjetAK8_phi",
    "MgenjetAK8_eta",
    "MgenjetAK8_hadronFlavour",
    "MgenjetAK8_partonFlavour",
    "MgenjetAK8_mass",
    "MgenjetAK8_ncFlavour",
    "MgenjetAK8_nbFlavour",
]

jet_names = [
    "pt",
    "eta",
    "phi",
    "msoftdrop",
    "particleNetMD_XbbvsQCD",
]

reco_columns = [f"FatJet_{name}" for name in jet_names]
