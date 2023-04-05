# define the functions to extract the features for electrons
import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "electrons.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def cleanGenJetCollection(df):
    """returns expanded rdataframe
    with cleaned GenJet collection: removing copies of genele and genmuon from genjet collection
    To be used for derived gen variables (closest jet, etc.)

    Args:
        df (rdataframe): original rdataframe

    Returns:
        rdataframe: expanded df
    """
    cleaned = (
        df.Define("TMPGenElectronMask", "abs(GenPart_pdgId) == 11")
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


def extractGenElectronFeatures(df):
    """returns expanded rdataframe
    with gen electron features for going genele to recoele

    Args:
        df (rdataframe): cleaned rdataframe from cleanGenJetCollection function

    Returns:
        rdataframe: expanded df
    """

    df = cleanGenJetCollection(df)

    extracted = (
        df.Define("GenElectronMask", "abs(GenPart_pdgId == 11)")
        .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
        .Define("GenElectron_eta", "GenPart_eta[GenElectronMask]")
        .Define("GenElectron_phi", "GenPart_phi[GenElectronMask]")
        .Define("GenElectron_pdgId", "GenPart_pdgId[GenElectronMask]")
        .Define("GenElectron_charge", "charge(GenElectron_pdgId)")
        .Define("GenElectron_statusFlags", "GenPart_statusFlags[GenElectronMask]")
        .Define("GenElectron_statusFlag0", "BitwiseDecoder(GenElectron_statusFlags, 0)")
        .Define("GenElectron_statusFlag1", "BitwiseDecoder(GenElectron_statusFlags, 1)")
        .Define("GenElectron_statusFlag2", "BitwiseDecoder(GenElectron_statusFlags, 2)")
        .Define("GenElectron_statusFlag3", "BitwiseDecoder(GenElectron_statusFlags, 3)")
        .Define("GenElectron_statusFlag4", "BitwiseDecoder(GenElectron_statusFlags, 4)")
        .Define("GenElectron_statusFlag5", "BitwiseDecoder(GenElectron_statusFlags, 5)")
        .Define("GenElectron_statusFlag6", "BitwiseDecoder(GenElectron_statusFlags, 6)")
        .Define("GenElectron_statusFlag7", "BitwiseDecoder(GenElectron_statusFlags, 7)")
        .Define("GenElectron_statusFlag8", "BitwiseDecoder(GenElectron_statusFlags, 8)")
        .Define("GenElectron_statusFlag9", "BitwiseDecoder(GenElectron_statusFlags, 9)")
        .Define(
            "GenElectron_statusFlag10", "BitwiseDecoder(GenElectron_statusFlags, 10)"
        )
        .Define(
            "GenElectron_statusFlag11", "BitwiseDecoder(GenElectron_statusFlags, 11)"
        )
        .Define(
            "GenElectron_statusFlag12", "BitwiseDecoder(GenElectron_statusFlags, 12)"
        )
        .Define(
            "GenElectron_statusFlag13", "BitwiseDecoder(GenElectron_statusFlags, 13)"
        )
        .Define(
            "GenElectron_statusFlag14", "BitwiseDecoder(GenElectron_statusFlags, 14)"
        )
        .Define(
            "ClosestJet_dr",
            "closest_jet_dr(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "ClosestJet_dphi",
            "closest_jet_dphi(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "ClosestJet_deta",
            "closest_jet_deta(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "ClosestJet_pt",
            "closest_jet_pt(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_pt)",
        )
        .Define(
            "ClosestJet_mass",
            "closest_jet_mass(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_mass)",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_gluon",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_undefined",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )
    )
    return extracted


def extractGenJetFeatures(df):
    """for going from GenJet to reco electron

    Args:
        df (rdataframe): original rdataframe (should be cleaned? to be decided)

    Returns:
        rdataframe: rdataframe with new features
    """
    extracted = (
        df.Define(
            "GenJet_EncodedPartonFlavour_light",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_gluon",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_c",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_b",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_undefined",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define("GenJet_hadronFlavour_uchar", "GenJet_hadronFlavour")
        .Define(
            "GenJet_hadronFlavour_int",
            "static_cast<ROOT::VecOps::RVec<int>>(GenJet_hadronFlavour_uchar)",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_b",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_c",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_light",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{0})",
        )
    )

    return extracted


def extractionGenPhotonFeatures(df):
    """for going from GenPhoton to reco electron

    Args:
        df (rdataframe): original rdataframe

    Returns:
        rdataframe: rdataframe with new features
    """
    extracted = (
        df.Define("GenPhotonMask", "GenPart_pdgId == 22")
        .Define("GenPhoton_pt", "GenPart_pt[GenPhotonMask]")
        .Define("GenPhoton_eta", "GenPart_eta[GenPhotonMask]")
        .Define("GenPhoton_phi", "GenPart_phi[GenPhotonMask]")
        .Define("GenPhoton_statusFlags", "GenPart_statusFlags[GenPhotonMask]")
        .Define("GenPhoton_statusFlag0", "BitwiseDecoder(GenPhoton_statusFlags, 0)")
        .Define("GenPhoton_statusFlag1", "BitwiseDecoder(GenPhoton_statusFlags, 1)")
        .Define("GenPhoton_statusFlag2", "BitwiseDecoder(GenPhoton_statusFlags, 2)")
        .Define("GenPhoton_statusFlag3", "BitwiseDecoder(GenPhoton_statusFlags, 3)")
        .Define("GenPhoton_statusFlag4", "BitwiseDecoder(GenPhoton_statusFlags, 4)")
        .Define("GenPhoton_statusFlag5", "BitwiseDecoder(GenPhoton_statusFlags, 5)")
        .Define("GenPhoton_statusFlag6", "BitwiseDecoder(GenPhoton_statusFlags, 6)")
        .Define("GenPhoton_statusFlag7", "BitwiseDecoder(GenPhoton_statusFlags, 7)")
        .Define("GenPhoton_statusFlag8", "BitwiseDecoder(GenPhoton_statusFlags, 8)")
        .Define("GenPhoton_statusFlag9", "BitwiseDecoder(GenPhoton_statusFlags, 9)")
        .Define("GenPhoton_statusFlag10", "BitwiseDecoder(GenPhoton_statusFlags, 10)")
        .Define("GenPhoton_statusFlag11", "BitwiseDecoder(GenPhoton_statusFlags, 11)")
        .Define("GenPhoton_statusFlag12", "BitwiseDecoder(GenPhoton_statusFlags, 12)")
        .Define("GenPhoton_statusFlag13", "BitwiseDecoder(GenPhoton_statusFlags, 13)")
        .Define("GenPhoton_statusFlag14", "BitwiseDecoder(GenPhoton_statusFlags, 14)")
    )

    return extracted
