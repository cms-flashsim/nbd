import os
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
from torch.utils.data import DataLoader
import nbd.builder.core as core
from nbd.preprocessing.preprocessing import preprocessing


def simulator(
    rdf,
    derived_vars_func,
    eff_model,
    eff_model_path,
    flow_loader,
    flow_path,
    eff_columns,
    gen_columns,
    reco_columns,
    vars_dictionary,
    scale_file_path,
    device="cpu",
    batch_size=10000,
    saturate_ranges_path=None,
    eff=True,
    preprocess_dict=None,
    gen_postprocessing_dict=None,
):
    # extract
    rdf_ass = derived_vars_func(rdf)
    if eff == True:
        a_gen_data = ak.from_rdataframe(
            rdf_ass, columns=eff_columns + gen_columns
        )  # no duplicate fields awkward 2.0
        if eff_model is not None:
            eff_model_init = eff_model(len(eff_columns))
        else:
            raise ValueError("Efficiency model path should be declared")
    else:
        a_gen_data = ak.from_rdataframe(rdf_ass, columns=gen_columns)
        eff_model_init = None
    to_flash, reco_struct = core.select_gen(
        a_gen_data,
        eff_columns,
        gen_columns,
        eff_model_init,
        eff_model_path,
        device=device,
        eff=eff,
        batch_size=batch_size,
    )

    if preprocess_dict is not None:
        to_flash = preprocessing(to_flash, preprocess_dict)

    a_flash = core.flash_simulate(
        flow_loader,
        flow_path,
        to_flash,
        gen_columns,
        reco_columns,
        vars_dictionary,
        scale_file_path,
        reco_struct,
        device=device,
        batch_size=10000,
        saturate_ranges_path=saturate_ranges_path,
        gen_postrpocessing_dict=gen_postprocessing_dict,
    )

    pt_col = [col for col in a_flash.fields if col.endswith("_pt")][0]
    # sort by pt
    a_flash = a_flash[ak.argsort(a_flash[pt_col], axis=-1, ascending=False)]

    return a_flash
