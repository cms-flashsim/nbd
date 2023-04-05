import os
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
from torch.utils.data import DataLoader
import core


def simulator(
    rdf,
    derived_vars_func,
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
):

    # extract
    rdf_ass = derived_vars_func(rdf)
    a_gen_data = ak.from_rdataframe(rdf_ass, columns=gen_columns)

    model_i = model(len(gen_columns))
    to_flash, reco_struct = core.select_gen(
        a_gen_data, gen_columns, model_i, model_path, device, eff, batch_size=batch_size,
    )

    a_flash = core.flash_simulate(
        flow_loader,
        flow_path,
        to_flash,
        gen_columns,
        reco_columns,
        vars_dictionary,
        scale_file_path,
        reco_struct,
        device="cpu",
        batch_size=10000,
        saturate_ranges_path=saturate_ranges_path,
    )
    # temporary fix to change charges
    charges = ak.unflatten(to_flash.GenElectron_charge, reco_struct)
    a_flash["Electron_charges"] = charges

    return a_flash
