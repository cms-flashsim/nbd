# define the dictionaries of objects to be simulated and their parameters
import os

# electrons imports
from nbd.models.electrons.geneleeff import ElectronClassifier
from nbd.models.electrons.fromgenele import load_mixture_model
from nbd.extraction.electrons import electrons

from nbd.models.electrons.geneleeff import JetClassifier as Electron_JetClassifier

# old model imports
# from nbd.postprocessing.electrons.columns_ele_old import ele_cond, reco_columns, eff_ele
# from nbd.postprocessing.electrons.post_actions_ele_old import (
#     target_dictionary as target_dictionary_ele,
# )
from nbd.postprocessing.electrons.columns_ele import (
    ele_cond,
    ele_jet_cond,
    reco_columns,
    eff_ele,
    eff_ele_jet,
)
from nbd.postprocessing.electrons.post_actions_ele import (
    target_dictionary as target_dictionary_ele,
)
from nbd.postprocessing.electrons.post_actions_ele_jet import (
    target_dictionary as target_dictionary_ele_jet,
)

# jets imports
from nbd.extraction.jets import jets
from nbd.models.jets.jets_muons import load_mixture_model as load_model_jets
from nbd.postprocessing.jets.columns_jets import (
    reco_columns as reco_columns_jets,
    jet_cond,
)
from nbd.postprocessing.jets.post_actions_jets import target_dictionary_jets

# muons imports
from nbd.extraction.muons import muons
from nbd.postprocessing.muons.columns_muons import (
    muon_cond,
    reco_columns as reco_columns_muons,
)
from nbd.models.jets.jets_muons import load_mixture_model as load_model_muons
from nbd.postprocessing.muons.post_actions_muons import target_dictionary_muons
from nbd.preprocessing.gen_muons.pre_actions_gen_muons import gen_dictionary_muons
from nbd.postprocessing.gen_muons.post_actions_gen_muons import cond_dictionary_muons

# fat jets imports
from nbd.extraction.fatjets import fatjets
from nbd.models.fatjets.fat_jets import load_mixture_model as load_model_fatjets
from nbd.postprocessing.fatjets.columns_fatjets import (
    reco_columns as reco_columns_fatjets,
    fatjet_cond,
)
from nbd.postprocessing.fatjets.post_actions_fatjets import target_dictionary_fatjets

saturate_file_path_fatjets = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "postprocessing/fatjets/saturate_ranges_fatjets.json",
)

objs_dicts = {
    "Electron": {
        "derived_vars_func": electrons.extractGenElectronFeatures,
        "eff_model": ElectronClassifier,
        "eff_model_path": "/home/users/cattafe/FlashSim-Electrons/efficiencies/models/efficiency_electrons.pt",
        "flow_loader": load_mixture_model,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/FlashSim-Models/Electron_EEMAF_HF_model285.pt",
        "eff_columns": eff_ele,
        "gen_columns": ele_cond,
        "reco_columns": reco_columns,
        "vars_dictionary": target_dictionary_ele,
        "scale_file_path": "/home/users/cattafe/trainer/trainer/training/electrons/electrons/scale_factors_ele_ele.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/trainer/trainer/training/electrons/electrons/ranges_ele_ele.json",
        "eff": True,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "Electron_fromJets": {
        "derived_vars_func": electrons.extractGenJetFeatures,
        "eff_model": Electron_JetClassifier,
        "eff_model_path": "/home/users/cattafe/FlashSim-Electrons/efficiencies/models/efficiency_jets.pt",
        "flow_loader": load_mixture_model,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/FlashSim-Models/Electron_fromJets_EJMAF_HF_model250.pt",
        "eff_columns": eff_ele_jet,
        "gen_columns": ele_jet_cond,
        "reco_columns": reco_columns,
        "vars_dictionary": target_dictionary_ele_jet,
        "scale_file_path": "/home/users/cattafe/trainer/trainer/training/electrons/jets/scale_factors_ele_jet.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/trainer/trainer/training/electrons/jets/ranges_ele_jet.json",
        "eff": True,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "Jet": {
        "derived_vars_func": jets.extractGenJetFeatures,
        "eff_model": None,
        "eff_model_path": None,
        "flow_loader": load_model_jets,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/FlashSim-Models/Jets_MAF1_epoch470.pt",
        "eff_columns": None,
        "gen_columns": jet_cond,
        "reco_columns": reco_columns_jets,
        "vars_dictionary": target_dictionary_jets,
        "scale_file_path": "/home/users/cattafe/trainer/trainer/training/jets/scale_factors_jets.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/trainer/trainer/training/jets/ranges_jets.json",
        "eff": False,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "Muon": {
        "derived_vars_func": muons.extractGenMuonFeatures,
        "eff_model": None,
        "eff_model_path": None,
        "flow_loader": load_model_muons,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/FlashSim-Models/Muons_MAF_epoch750.pt",
        "eff_columns": None,
        "gen_columns": muon_cond,
        "reco_columns": reco_columns_muons,
        "vars_dictionary": target_dictionary_muons,
        "scale_file_path": "/home/users/cattafe/trainer/trainer/training/muons/scale_factors_muons.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/trainer/trainer/training/muons/ranges_muons.json",
        "eff": False,
        # "preprocess_dict": gen_dictionary_muons,
        # "gen_postprocessing_dict": cond_dictionary_muons,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "FatJets": {
        "derived_vars_func": fatjets.extractGenFatJetsFeatures,
        "eff_model": None,
        "eff_model_path": None,
        "flow_loader": load_model_fatjets,
        "flow_path": "/gpfs/ddn/cms/user/fvaselli/fat_jets_weights/model_@epoch_999.pt",
        "eff_columns": None,
        "gen_columns": fatjet_cond,
        "reco_columns": reco_columns_fatjets,
        "vars_dictionary": target_dictionary_fatjets,
        "scale_file_path": None,
        "batch_size": 10000,
        "saturate_ranges_path": saturate_file_path_fatjets,
        "eff": False,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
}

reco_objects = [
    "Electron",
    # "Muon",
    # "Jet",
    # "FatJet",
]  # list of FullSim branches to be copied and saved in the dedicated tree

merge_dict = {}  # "Electron": ["Electron", "Electron_fromJets"]

# all the columns that are needed for the extraction

needed_columns = [
    "GenPart_pdgId",
    "GenPart_pt",
    "GenPart_eta",
    "GenPart_phi",
    "GenPart_statusFlags",
    "GenPart_genPartIdxMother",
    "GenJet_pt",
    "GenJet_eta",
    "GenJet_phi",
    "GenJet_partonFlavour",
    "GenJet_hadronFlavour",
    "GenJetAK8_pt",
    "GenJetAK8_eta",
    "GenJetAK8_phi",
    "GenJetAK8_mass",
    "GenJetAK8_partonFlavour",
    "GenJetAK8_hadronFlavour",
]
