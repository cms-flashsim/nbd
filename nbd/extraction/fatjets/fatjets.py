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
        df.Define(
            "GenPart_IsLastB",
            "(GenPart_pdgId >=500 && GenPart_pdgId < 600) | (GenPart_pdgId >=5000 && GenPart_pdgId < 6000) && (GenPart_statusFlags &(1<<13))!=0",
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
            "GenJetAK8_nbFlavour",
            "count_nHadrons(GenPart_eta_goodb, GenPart_phi_goodb, GenJetAK8_eta, GenJetAK8_phi)",
        )
        .Define("GenPart_IsLastC", "(GenPart_pdgId >=400 && GenPart_pdgId < 500) | (GenPart_pdgId >=4000 && GenPart_pdgId < 5000) && (GenPart_statusFlags &(1<<13))!=0")
        .Define("GenPart_IsLastC_m", "Take(GenPart_IsLastC, GenPart_genPartIdxMother)")
        .Define("GenPart_parent_IsNotLastC", "(GenPart_genPartIdxMother == -1 | GenPart_IsLastC_m ==0)")
        .Define("GenPart_IsGoodC", "GenPart_IsLastC && GenPart_parent_IsNotLastC")
        .Define("GenPart_eta_goodc", "GenPart_eta[GenPart_IsGoodC]")
        .Define("GenPart_phi_goodc", "GenPart_phi[GenPart_IsGoodC]")
        .Define("GenJetAK8_ncFlavour", "count_nHadrons(GenPart_eta_goodc, GenPart_phi_goodc, GenJetAK8_eta, GenJetAK8_phi)")
    )

    return extracted
