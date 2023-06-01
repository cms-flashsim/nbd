import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "jets.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def extractGenJetFeatures(df):
    """for going from GenJet to reco jet

    Args:
        df (rdataframe): original rdataframe (should be cleaned? to be decided)

    Returns:
        rdataframe: rdataframe with new features
    """
    # NOTE: we are not using the full sim information here, but only the gen jet
    extracted = (
        # df.Define("buffer", "Muon_genPartIdx")
        # .Define("MuonMaskJet", "buffer >=0")
        df.Define("MuonMaskJet", "Muon_genPartIdx >=0")
        .Define("MatchedGenMuons", "Muon_genPartIdx[MuonMaskJet]")
        # .Define("JetMask", "Jet_genJetIdx >=0  && Jet_genJetIdx < nGenJet")
        # .Define("MatchedGenJets", "Jet_genJetIdx[JetMask]")
        .Define("MGenJet_hadronFlavourUChar", "GenJet_hadronFlavour,")
        .Define(
            "MGenJet_hadronFlavour",
            "static_cast<ROOT::VecOps::RVec<int>>(MGenJet_hadronFlavourUChar)",
        )
        .Define("MGenJet_partonFlavour", "GenJet_partonFlavour")
        .Define(
            "MGenJet_EncodedPartonFlavour_light",
            "gen_jet_flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_gluon",
            "gen_jet_flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_c",
            "gen_jet_flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_b",
            "gen_jet_flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_undefined",
            "gen_jet_flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_b",
            "gen_jet_flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_c",
            "gen_jet_flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_light",
            "gen_jet_flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )
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
