import os
import ROOT

module_path = os.path.join(os.path.dirname(__file__), "fatjets.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


def extractGenFatJetsFeatures(df):
    """for going from GenJetAK8 to reco ak8jet

    Args:
        df (rdataframe): original rdataframe (should be cleaned? to be decided)

    Returns:
        rdataframe: rdataframe with new features
    """
    extracted = (
        df.Define("GenJetAK8Mask", "GenJetAK8_pt >= 250")
        .Define("MGenJetAK8_pt", "GenJetAK8_pt[GenJetAK8Mask]")
        .Define("MGenJetAK8_phi", "GenJetAK8_phi[GenJetAK8Mask]")
        .Define("MGenJetAK8_eta", "GenJetAK8_eta[GenJetAK8Mask]")
        .Define("MGenJetAK8_hadronFlavour", "GenJetAK8_hadronFlavour[GenJetAK8Mask]")
        .Define("MGenJetAK8_partonFlavour", "GenJetAK8_partonFlavour[GenJetAK8Mask]")
        .Define("MGenJetAK8_mass", "GenJetAK8_mass[GenJetAK8Mask]")
        .Define("GenPart_pdgId_abs", "abs(GenPart_pdgId)")
        .Define(
            "GenPart_IsLastB",
            "(GenPart_pdgId_abs >=500 && GenPart_pdgId_abs < 600) | (GenPart_pdgId_abs >=5000 && GenPart_pdgId_abs < 6000) && (GenPart_statusFlags &(1<<13))!=0",
        )
        .Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")
        .Define(
            "GenPart_parent_IsNotLastB",
            "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
        )
        .Define("GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
        .Define("GenPart_eta_goodb", "GenPart_eta[GenPart_IsGoodB]")
        .Define("GenPart_phi_goodb", "GenPart_phi[GenPart_IsGoodB]")
        .Define(
            "MGenJetAK8_nbFlavour",
            "count_nHadrons(GenPart_eta_goodb, GenPart_phi_goodb, MGenJetAK8_eta, MGenJetAK8_phi)",
        )
        .Define(
            "GenPart_IsLastC",
            "(GenPart_pdgId_abs >=400 && GenPart_pdgId_abs < 500) | (GenPart_pdgId_abs >=4000 && GenPart_pdgId_abs < 5000) && (GenPart_statusFlags &(1<<13))!=0",
        )
        .Define("GenPart_IsLastC_m", "Take(GenPart_IsLastC, GenPart_genPartIdxMother)")
        .Define(
            "GenPart_parent_IsNotLastC",
            "(GenPart_genPartIdxMother == -1 | GenPart_IsLastC_m ==0)",
        )
        .Define("GenPart_IsGoodC", "GenPart_IsLastC && GenPart_parent_IsNotLastC")
        .Define("GenPart_eta_goodc", "GenPart_eta[GenPart_IsGoodC]")
        .Define("GenPart_phi_goodc", "GenPart_phi[GenPart_IsGoodC]")
        .Define(
            "MGenJetAK8_ncFlavour",
            "count_nHadrons(GenPart_eta_goodc, GenPart_phi_goodc, MGenJetAK8_eta, MGenJetAK8_phi)",
        )
    )

    return extracted
