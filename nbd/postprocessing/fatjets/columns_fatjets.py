fatjet_cond = [
    "MGenJetAK8_pt",
    "MGenJetAK8_phi",
    "MGenJetAK8_eta",
    "MGenJetAK8_hadronFlavour",
    "MGenJetAK8_partonFlavour",
    "MGenJetAK8_mass",
    "MGenJetAK8_ncFlavour",
    "MGenJetAK8_nbFlavour",
    "Mhas_H_within_0_8",
]

jet_names = [
    "pt",
    "eta",
    "phi",
    "msoftdrop",
    "particleNetMD_XbbvsQCD",
]

reco_columns = [f"FatJet_{name}" for name in jet_names]
