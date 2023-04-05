# define the dictionaries of objects to be simulated and their parameters
from extraction.electrons import electrons 

objs_dicts = {
    "Electron": {
    "derived_vars_func": electrons.extractGenElectronFeatures
    model,
    model_path,
    flow_loader,
    flow_path,
    gen_columns,
    reco_columns,
    vars_dictionary,
    scale_file_path,
    device="cpu",
    batch_size=10000,
    saturate_ranges_path=None,
    eff=True,
    }
}
