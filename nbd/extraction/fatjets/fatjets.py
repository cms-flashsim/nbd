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
    extracted = df

    return extracted
