ele_cond = [
    "GenElectron_eta",
    "GenElectron_phi",
    "GenElectron_pt",
    "GenElectron_charge",
    "GenElectron_statusFlag0",
    "GenElectron_statusFlag1",
    "GenElectron_statusFlag2",
    "GenElectron_statusFlag3",
    "GenElectron_statusFlag4",
    "GenElectron_statusFlag5",
    "GenElectron_statusFlag6",
    "GenElectron_statusFlag7",
    "GenElectron_statusFlag8",
    "GenElectron_statusFlag9",
    "GenElectron_statusFlag10",
    "GenElectron_statusFlag11",
    "GenElectron_statusFlag12",
    "GenElectron_statusFlag13",
    "GenElectron_statusFlag14",
    "ClosestJet_dr",
    "ClosestJet_dphi",
    "ClosestJet_deta",
    "ClosestJet_pt",
    "ClosestJet_mass",
    "ClosestJet_EncodedPartonFlavour_light",
    "ClosestJet_EncodedPartonFlavour_gluon",
    "ClosestJet_EncodedPartonFlavour_c",
    "ClosestJet_EncodedPartonFlavour_b",
    "ClosestJet_EncodedPartonFlavour_undefined",
    "ClosestJet_EncodedHadronFlavour_b",
    "ClosestJet_EncodedHadronFlavour_c",
    "ClosestJet_EncodedHadronFlavour_light",
]

eff_ele = ele_cond.copy()

pu = [
    "Pileup_gpudensity",
    "Pileup_nPU",
    "Pileup_nTrueInt",
    "Pileup_pudensity",
    "Pileup_sumEOOT",
    "Pileup_sumLOOT",
]

ele_cond = ele_cond + pu

ele_names = [
    "convVeto",
    "deltaEtaSC",
    "dr03EcalRecHitSumEt",
    "dr03HcalDepth1TowerSumEt",
    "dr03TkSumPt",
    "dr03TkSumPtHEEP",
    "dxy",
    "dxyErr",
    "dz",
    "dzErr",
    "eInvMinusPInv",
    "energyErr",
    "eta",
    "hoe",
    "ip3d",
    "isPFcand",
    "jetPtRelv2",
    "jetRelIso",
    "lostHits",
    "miniPFRelIso_all",
    "miniPFRelIso_chg",
    "mvaFall17V1Iso",
    "mvaFall17V1Iso_WP80",
    "mvaFall17V1Iso_WP90",
    "mvaFall17V1Iso_WPL",
    "mvaFall17V1noIso",
    "mvaFall17V1noIso_WP80",
    "mvaFall17V1noIso_WP90",
    "mvaFall17V1noIso_WPL",
    "mvaFall17V2Iso",
    "mvaFall17V2Iso_WP80",
    "mvaFall17V2Iso_WP90",
    "mvaFall17V2Iso_WPL",
    "mvaFall17V2noIso",
    "mvaFall17V2noIso_WP80",
    "mvaFall17V2noIso_WP90",
    "mvaFall17V2noIso_WPL",
    "mvaTTH",
    "pfRelIso03_all",
    "pfRelIso03_chg",
    "phi",
    "pt",
    "r9",
    "seedGain",
    "sieie",
    "sip3d",
    "tightCharge",
    "charge",
]

reco_columns = [f"Electron_{name}" for name in ele_names]

for i, name in enumerate(reco_columns):
    if name == "Electron_pt":
        reco_columns[i] = "Electron_ptRatio"
    elif name == "Electron_phi":
        reco_columns[i] = "Electron_phiMinusGen"
    elif name == "Electron_eta":
        reco_columns[i] = "Electron_etaMinusGen"
