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
        "GenJet_partonFlavour",
        "GenJet_hadronFlavour",
    ]

jet_names = [
        "area",
        "btagCMVA",
        "btagCSVV2",
        "btagDeepB",
        "btagDeepC",
        "btagDeepFlavB",
        "btagDeepFlavC",
        "eta",
        "bRegCorr",
        "mass",
        "nConstituents",
        "phi",
        "pt",
        "qgl",
        "muEF",
        "puId",
        "jetId",
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
