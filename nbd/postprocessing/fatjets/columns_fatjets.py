fatjet_cond = [
    "GenJetAK8_pt",
    "GenJetAK8_phi",
    "GenJetAK8_eta",
    "GenJetAK8_hadronFlavour",
    "GenJetAK8_partonFlavour",
    "GenJetAK8_mass",
    "GenJetAK8_ncFlavour",
    "GenJetAK8_nbFlavour",
]

jet_names = [
    "pt",
    "eta",
    "phi",
    "msoftdrop",
    "particleNetMD_XbbvsQCD",
]

reco_columns = [f"FatJet_{name}" for name in jet_names]