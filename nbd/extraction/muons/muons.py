import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "muons.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def extractGenMuonFeatures(df):
    """for going from GenJet to reco jet

    Args:
        df (rdataframe): original rdataframe (should be cleaned? to be decided)

    Returns:
        rdataframe: rdataframe with new features
    """
    extracted = (
        df.Define(
            "MuonMaskJ",
            "(GenPart_pdgId == 13 | GenPart_pdgId == -13)&&((GenPart_statusFlags & 8192) > 0)",
        )
        .Define("MGenMuon_eta", "GenPart_eta[MuonMaskJ]")
        .Define("MGenMuon_pdgId", "GenPart_pdgId[MuonMaskJ]")
        .Define("MGenMuon_charge", "charge(MGenMuon_pdgId)")
        .Define("MGenMuon_phi", "GenPart_phi[MuonMaskJ]")
        .Define("MGenMuon_pt", "GenPart_pt[MuonMaskJ]")
        .Define("MGenPart_statusFlags", "GenPart_statusFlags[MuonMaskJ]")
        .Define("MGenPart_statusFlags0", "BitwiseDecoder(MGenPart_statusFlags, 0)")
        .Define("MGenPart_statusFlags1", "BitwiseDecoder(MGenPart_statusFlags, 1)")
        .Define("MGenPart_statusFlags2", "BitwiseDecoder(MGenPart_statusFlags, 2)")
        .Define("MGenPart_statusFlags3", "BitwiseDecoder(MGenPart_statusFlags, 3)")
        .Define("MGenPart_statusFlags4", "BitwiseDecoder(MGenPart_statusFlags, 4)")
        .Define("MGenPart_statusFlags5", "BitwiseDecoder(MGenPart_statusFlags, 5)")
        .Define("MGenPart_statusFlags6", "BitwiseDecoder(MGenPart_statusFlags, 6)")
        .Define("MGenPart_statusFlags7", "BitwiseDecoder(MGenPart_statusFlags, 7)")
        .Define("MGenPart_statusFlags8", "BitwiseDecoder(MGenPart_statusFlags, 8)")
        .Define("MGenPart_statusFlags9", "BitwiseDecoder(MGenPart_statusFlags, 9)")
        .Define("MGenPart_statusFlags10", "BitwiseDecoder(MGenPart_statusFlags, 10)")
        .Define("MGenPart_statusFlags11", "BitwiseDecoder(MGenPart_statusFlags, 11)")
        .Define("MGenPart_statusFlags12", "BitwiseDecoder(MGenPart_statusFlags, 12)")
        .Define("MGenPart_statusFlags13", "BitwiseDecoder(MGenPart_statusFlags, 13)")
        .Define("MGenPart_statusFlags14", "BitwiseDecoder(MGenPart_statusFlags, 14)")
        .Define(
            "MClosestJet_dr",
            "closest_jet_dr(GenJet_eta, GenJet_phi,MGenMuon_eta, MGenMuon_phi)",
        )
        .Define(
            "MClosestJet_deta",
            "closest_jet_deta(GenJet_eta, GenJet_phi,MGenMuon_eta, MGenMuon_phi)",
        )
        .Define(
            "MClosestJet_dphi",
            "closest_jet_dphi(GenJet_eta, GenJet_phi,MGenMuon_eta, MGenMuon_phi)",
        )
        .Define(
            "MClosestJet_pt",
            "closest_jet_pt(GenJet_eta, GenJet_phi,MGenMuon_eta, MGenMuon_phi, GenJet_pt)",
        )
        .Define(
            "MClosestJet_mass",
            "closest_jet_mass(GenJet_eta, GenJet_phi,MGenMuon_eta, MGenMuon_phi, GenJet_mass)",
        )
    )

    return extracted
