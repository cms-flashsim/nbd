import ROOT
import os

module = os.path.join(os.path.dirname(__file__), "extraction.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module}"')

ROOT.EnableImplicitMT()

d = ROOT.RDataFrame("Events", "~/test_TTJets.root")

cleaned = (
    d.Define("TMPGenElectronMask", "abs(GenPart_pdgId) == 11")
    .Define("TMPGenElectron_pt", "GenPart_pt[TMPGenElectronMask]")
    .Define("TMPGenElectron_eta", "GenPart_eta[TMPGenElectronMask]")
    .Define("TMPGenElectron_phi", "GenPart_phi[TMPGenElectronMask]")
    .Define("GenMuonMask", "abs(GenPart_pdgId) == 13")
    .Define("GenMuon_pt", "GenPart_pt[GenMuonMask]")
    .Define("GenMuon_eta", "GenPart_eta[GenMuonMask]")
    .Define("GenMuon_phi", "GenPart_phi[GenMuonMask]")
    .Define(
        "CleanGenJet_mask_ele",
        "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, TMPGenElectron_pt, TMPGenElectron_eta, TMPGenElectron_phi)",
    )
    .Define(
        "CleanGenJet_mask_muon",
        "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, GenMuon_pt, GenMuon_eta, GenMuon_phi)",
    )
    .Define("CleanGenJetMask", "CleanGenJet_mask_ele && CleanGenJet_mask_muon")
    .Define("CleanGenJet_pt", "GenJet_pt[CleanGenJetMask]")
    .Define("CleanGenJet_eta", "GenJet_eta[CleanGenJetMask]")
    .Define("CleanGenJet_phi", "GenJet_phi[CleanGenJetMask]")
    .Define("CleanGenJet_mass", "GenJet_mass[CleanGenJetMask]")
    .Define("CleanGenJet_hadronFlavour_uchar", "GenJet_hadronFlavour[CleanGenJetMask]")
    .Define(
        "CleanGenJet_hadronFlavour",
        "static_cast<ROOT::VecOps::RVec<int>>(CleanGenJet_hadronFlavour_uchar)",
    )
    .Define("CleanGenJet_partonFlavour", "GenJet_partonFlavour[CleanGenJetMask]")
)


matched = (
    cleaned.Define("GenPart_ElectronIdx_empty", "Electron_genObjMatchMaker(GenPart_pt)")
    .Define(
        "GenPart_genElectron_ElectronIdx",
        "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, Electron_pt, Electron_eta, Electron_phi, Electron_charge, GenPart_ElectronIdx_empty, 0)",
    )
    .Define("GenPart_MElectronIdx_empty", "Electron_genObjMatchMaker(GenPart_pt)")
    .Define(
        "GenPart_genElectron_MElectronIdx",
        "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, MElectron_ptRatio, MElectron_etaMinusGen, MElectron_phiMinusGen, MElectron_charge, GenPart_MElectronIdx_empty, 0)",
    )
    .Define(
        "GenElectronMask",
        "abs(GenPart_pdgId) == 11",
    )
    .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
    .Define(
        "GenElectron_FullMatched",
        "GenPart_genElectron_ElectronIdx[GenElectronMask] >= 0",
    )
    .Define("FullMatched", "GenElectron_pt[GenElectron_FullMatched]")
    .Define(
        "GenElectron_FlashMatched",
        "GenPart_genElectron_MElectronIdx[GenElectronMask] >= 0",
    )
    .Define("FlashMatched", "GenElectron_pt[GenElectron_FlashMatched]")
)


n_full = matched.Histo1D("FullMatched").GetEntries()

n_flash = d.Histo1D("MElectron_ptRatio").GetEntries()

# n_flash = (
#     matched.Histo1D("FlashMatched").GetEntries()
#     / matched.Histo1D("GenElectron_pt").GetEntries()
# )

print(f"Flash: {n_flash}")
print(f"Full: {n_full}")
