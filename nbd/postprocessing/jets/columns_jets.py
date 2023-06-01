# conditioning and reco columns for jets

jet_cond = [
    "MClosestMuon_dr",
    "MClosestMuon_pt",
    "MClosestMuon_deta",
    "MClosestMuon_dphi",
    "MSecondClosestMuon_dr",
    "MSecondClosestMuon_pt",
    "MSecondClosestMuon_deta",
    "MSecondClosestMuon_dphi",
    "GenJet_eta",
    "GenJet_mass",
    "GenJet_phi",
    "GenJet_pt",
    "MGenJet_EncodedPartonFlavour_light",
    "MGenJet_EncodedPartonFlavour_gluon",
    "MGenJet_EncodedPartonFlavour_c",
    "MGenJet_EncodedPartonFlavour_b",
    "MGenJet_EncodedPartonFlavour_undefined",
    "MGenJet_EncodedHadronFlavour_b",
    "MGenJet_EncodedHadronFlavour_c",
    "MGenJet_EncodedHadronFlavour_light",
]

jet_names = [
    "area",
    "bRegCorr",
    "bRegRes",
    "btagCSVV2",
    "btagDeepB",
    "btagDeepCvB",
    "btagDeepCvL",
    "btagDeepFlavB",
    "btagDeepFlavCvB",
    "btagDeepFlavCvL",
    "btagDeepFlavQG",
    "cRegCorr",
    "cRegRes",
    "chEmEF",
    "chFPV0EF",
    "chHEF",
    "cleanmask",
    "etaMinusGen",
    "hadronFlavour",
    "hfadjacentEtaStripsSize",
    "hfcentralEtaStripSize",
    "hfsigmaEtaEta",
    "hfsigmaPhiPhi",
    "jetId",
    "mass",
    "muEF",
    "muonSubtrFactor",
    "nConstituents",
    "nElectrons",
    "nMuons",
    "neEmEF",
    "neHEF",
    "partonFlavour",
    "phiMinusGen",
    "ptRatio",
    "puId",
    "puIdDisc",
    "qgl",
    "rawFactor",
]

reco_columns = [f"Jet_{name}" for name in jet_names]


# NOTE we are calling the ratio/minus variables with the same name as the original
# for i, name in enumerate(reco_columns):
#     if name == "MElectron_pt":
#         reco_columns[i] = "MElectron_ptRatio"
#     elif name == "MElectron_phi":
#         reco_columns[i] = "MElectron_phiMinusGen"
#     elif name == "MElectron_eta":
#         reco_columns[i] = "MElectron_etaMinusGen"
