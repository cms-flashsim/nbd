import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "taus.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def jet_cleaning(d):
    cleaned = (
        d.Define("TMPGenElectronMask", "abs(GenPart_pdgId) == 11")
        .Define("TMPGenElectron_pt", "GenPart_pt[TMPGenElectronMask]")
        .Define("TMPGenElectron_eta", "GenPart_eta[TMPGenElectronMask]")
        .Define("TMPGenElectron_phi", "GenPart_phi[TMPGenElectronMask]")
        .Define("TMPGenMuonMask", "abs(GenPart_pdgId) == 13")
        .Define("TMPGenMuon_pt", "GenPart_pt[TMPGenMuonMask]")
        .Define("TMPGenMuon_eta", "GenPart_eta[TMPGenMuonMask]")
        .Define("TMPGenMuon_phi", "GenPart_phi[TMPGenMuonMask]")
        .Define("TMPGenTauMask", "abs(GenPart_pdgId) == 15")
        .Define("TMPGenTau_pt", "GenPart_pt[TMPGenTauMask]")
        .Define("TMPGenTau_eta", "GenPart_eta[TMPGenTauMask]")
        .Define("TMPGenTau_phi", "GenPart_phi[TMPGenTauMask]")
        .Define(
            "CleanGenJet_mask_ele",
            "Tclean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, TMPGenElectron_pt, TMPGenElectron_eta, TMPGenElectron_phi)",
        )
        .Define(
            "CleanGenJet_mask_muon",
            "Tclean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, TMPGenMuon_pt, TMPGenMuon_eta, TMPGenMuon_phi)",
        )
        .Define(
            "CleanGenJet_mask_tau",
            "Tclean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, TMPGenTau_pt, TMPGenTau_eta, TMPGenTau_phi)",
        )
        .Define("CleanGenJetMask", "CleanGenJet_mask_ele && CleanGenJet_mask_muon")
        .Define("CleanGenJet_pt", "GenJet_pt[CleanGenJetMask]")
        .Define("CleanGenJet_eta", "GenJet_eta[CleanGenJetMask]")
        .Define("CleanGenJet_phi", "GenJet_phi[CleanGenJetMask]")
        .Define("CleanGenJet_mass", "GenJet_mass[CleanGenJetMask]")
        .Define(
            "CleanGenJet_hadronFlavour_uchar", "GenJet_hadronFlavour[CleanGenJetMask]"
        )
        .Define(
            "CleanGenJet_hadronFlavour",
            "static_cast<ROOT::VecOps::RVec<int>>(CleanGenJet_hadronFlavour_uchar)",
        )
        .Define("CleanGenJet_partonFlavour", "GenJet_partonFlavour[CleanGenJetMask]")
    )

    return cleaned


def extractGenTauFeatures(df):
    """for getting gentau, recotau and cleaned genjet features

    Args:
        df (rdataframe): original rdataframe (should be cleaned by jet copies)

    Returns:
        rdataframe: rdataframe with new features
    """
    df1 = jet_cleaning(df)
    extracted = (
         df1.Define(
            "TauMaskJ",
            "(GenPart_pdgId == 15 | GenPart_pdgId == -15)&&((GenPart_statusFlags & 8192) > 0)",
        )
        .Define("MGenTau_eta", "GenPart_eta[TauMaskJ]")
        .Define("MGenTau_pdgId", "GenPart_pdgId[TauMaskJ]")
        .Define("MGenTau_charge", "Tcharge(MGenTau_pdgId)")
        .Define("MGenTau_phi", "GenPart_phi[TauMaskJ]")
        .Define("MGenTau_pt", "GenPart_pt[TauMaskJ]")
        .Define("MGenPart_statusFlags", "GenPart_statusFlags[TauMaskJ]")
        .Define("MGenPart_statusFlags0", "TBitwiseDecoder(MGenPart_statusFlags, 0)")
        .Define("MGenPart_statusFlags1", "TBitwiseDecoder(MGenPart_statusFlags, 1)")
        .Define("MGenPart_statusFlags2", "TBitwiseDecoder(MGenPart_statusFlags, 2)")
        .Define("MGenPart_statusFlags3", "TBitwiseDecoder(MGenPart_statusFlags, 3)")
        .Define("MGenPart_statusFlags4", "TBitwiseDecoder(MGenPart_statusFlags, 4)")
        .Define("MGenPart_statusFlags5", "TBitwiseDecoder(MGenPart_statusFlags, 5)")
        .Define("MGenPart_statusFlags6", "TBitwiseDecoder(MGenPart_statusFlags, 6)")
        .Define("MGenPart_statusFlags7", "TBitwiseDecoder(MGenPart_statusFlags, 7)")
        .Define("MGenPart_statusFlags8", "TBitwiseDecoder(MGenPart_statusFlags, 8)")
        .Define("MGenPart_statusFlags9", "TBitwiseDecoder(MGenPart_statusFlags, 9)")
        .Define("MGenPart_statusFlags10", "TBitwiseDecoder(MGenPart_statusFlags, 10)")
        .Define("MGenPart_statusFlags11", "TBitwiseDecoder(MGenPart_statusFlags, 11)")
        .Define("MGenPart_statusFlags12", "TBitwiseDecoder(MGenPart_statusFlags, 12)")
        .Define("MGenPart_statusFlags13", "TBitwiseDecoder(MGenPart_statusFlags, 13)")
        .Define("MGenPart_statusFlags14", "TBitwiseDecoder(MGenPart_statusFlags, 14)")
        .Define(
            "ClosestJet_dr",
            "Tclosest_jet_dr(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi)",
        )
        .Define(
            "ClosestJet_deta",
            "Tclosest_jet_deta(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi)",
        )
        .Define(
            "ClosestJet_dphi",
            "Tclosest_jet_dphi(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi)",
        )
        .Define(
            "ClosestJet_pt",
            "Tclosest_jet_pt(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_pt)",
        )
        .Define(
            "ClosestJet_mass",
            "Tclosest_jet_mass(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_mass)",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_light",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_gluon",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_c",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_b",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_undefined",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_b",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_c",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_light",
            "Tclosest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenTau_eta, MGenTau_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )     
    )
    
    return extracted