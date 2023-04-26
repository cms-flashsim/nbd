# define the dictionaries of objects to be simulated and their parameters

# electrons imports
from nbd.models.electrons.geneleeff import ElectronClassifier
from nbd.models.electrons.fromgenele import load_mixture_model
from nbd.extraction.electrons import electrons
from nbd.postprocessing.electrons.columns_ele_old import ele_cond, reco_columns, eff_ele
from nbd.postprocessing.electrons.post_actions_ele_old import (
    target_dictionary as target_dictionary_ele,
)

# jets imports
from nbd.extraction.jets import jets
from nbd.models.jets.jets_muons import load_model
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
from nbd.postprocessing.muons.post_actions_muons import target_dictionary_muons
from nbd.preprocessing.gen_muons.pre_actions_gen_muons import gen_dictionary_muons
from nbd.postprocessing.gen_muons.post_actions_gen_muons import cond_dictionary_muons

objs_dicts = {
    "Electron": {
        "derived_vars_func": electrons.extractGenElectronFeatures,
        "eff_model": ElectronClassifier,
        "eff_model_path": "/home/users/cattafe/FlashSim-Electrons/efficiencies/models/efficiency_electrons.pt",
        "flow_loader": load_mixture_model,
        "flow_path": "/home/users/cattafe/wipfs/generation/electrons/EM1/checkpoint-latest.pt",
        "eff_columns": eff_ele,
        "gen_columns": ele_cond,
        "reco_columns": reco_columns,
        "vars_dictionary": target_dictionary_ele,
        "scale_file_path": "/home/users/cattafe/nbd/nbd/postprocessing/electrons/scale_factors_ele_old.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/nbd/nbd/postprocessing/electrons/saturate_ranges_ele.json",
        "eff": True,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "Jet": {
        "derived_vars_func": jets.extractGenJetFeatures,
        "eff_model": None,
        "eff_model_path": None,
        "flow_loader": load_model,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/test/model_jets_final_@epoch_420.pt",
        "eff_columns": None,
        "gen_columns": jet_cond,
        "reco_columns": reco_columns_jets,
        "vars_dictionary": target_dictionary_jets,
        "scale_file_path": None,
        "batch_size": 10000,
        "saturate_ranges_path": None,
        "eff": False,
        "preprocess_dict": None,
        "gen_postprocessing_dict": None,
    },
    "Muon": {
        "derived_vars_func": muons.extractGenMuonFeatures,
        "eff_model": None,
        "eff_model_path": None,
        "flow_loader": load_model,
        "flow_path": "/gpfs/ddn/cms/user/cattafe/test/model_muons_final_@epoch_580.pt",
        "eff_columns": None,
        "gen_columns": muon_cond,
        "reco_columns": reco_columns_muons,
        "vars_dictionary": target_dictionary_muons,
        "scale_file_path": None,
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/nbd/nbd/postprocessing/muons/saturate_ranges_muon.json",
        "eff": False,
        "preprocess_dict": gen_dictionary_muons,
        "gen_postprocessing_dict": cond_dictionary_muons,
    },
}
