import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "jets.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def extractGenJetFeatures(df):
    """for going from GenJet to reco electron

    Args:
        df (rdataframe): original rdataframe (should be cleaned? to be decided)

    Returns:
        rdataframe: rdataframe with new features
    """
    extracted = (
        df.Define("MuonMaskJet", "Muon_genPartIdx >=0")
        .Define("MatchedGenMuons", "Muon_genPartIdx[MuonMaskJet]")
        .Define("JetMask", "Jet_genJetIdx >=0  && Jet_genJetIdx < nGenJet")
        .Define("MatchedGenJets", "Jet_genJetIdx[JetMask]")
        .Define(
            "MuonMaskJ",
            "(GenPart_pdgId == 13 | GenPart_pdgId == -13)&&((GenPart_statusFlags & 8192) > 0)",
        )
        .Define("MMuon_pt", "GenPart_pt[MuonMaskJ]")
        .Define("MMuon_eta", "GenPart_eta[MuonMaskJ]")
        .Define("MMuon_phi", "GenPart_phi[MuonMaskJ]")
        .Define(
            "MClosestMuon_dr",
            "closest_muon_dr(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MClosestMuon_deta",
            "closest_muon_deta(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MClosestMuon_dphi",
            "closest_muon_dphi(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MClosestMuon_pt",
            "closest_muon_pt(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi, MMuon_pt)",
        )
        .Define(
            "MSecondClosestMuon_dr",
            "second_muon_dr(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MSecondClosestMuon_deta",
            "second_muon_deta(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MSecondClosestMuon_dphi",
            "second_muon_dphi(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi)",
        )
        .Define(
            "MSecondClosestMuon_pt",
            "second_muon_pt(GenJet_eta, GenJet_phi,MMuon_eta, MMuon_phi, MMuon_pt)",
        )
    )

    return extracted
