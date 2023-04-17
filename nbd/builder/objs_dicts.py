# define the dictionaries of objects to be simulated and their parameters
from nbd.extraction.electrons import electrons
from nbd.models.electrons.geneleeff import ElectronClassifier
from nbd.models.electrons.fromgenele import load_mixture_model
from nbd.postprocessing.electrons.columns_ele_old import ele_cond, reco_columns, eff_ele
from nbd.postprocessing.electrons.post_actions_ele_old import target_dictionary


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
        "vars_dictionary": target_dictionary,
        "scale_file_path": "/home/users/cattafe/nbd/nbd/postprocessing/electrons/scale_factors_ele_old.json",
        "batch_size": 10000,
        "saturate_ranges_path": "/home/users/cattafe/nbd/nbd/postprocessing/electrons/saturate_ranges_ele.json",
        "eff": True,
    }
}
