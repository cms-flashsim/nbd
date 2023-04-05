import os
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
from torch.utils.data import DataLoader



if __name__=='__main__':

    full = ROOT.RDataFrame("Events", "")
    full_columns = full.GetColumnNames()

    # extract
    # 


    a_full = ak.from_rdataframe(full, columns=full_columns)

    a_data = ak.from_rdataframe(full)

    a_flash = flash_simulate(
        flow_loader,
        model_path,
        to_flash,
        gen_columns,
        reco_columns,
        vars_dictionary,
        scale_file,
        reco_struct,
    )

    a_full = ak.concatenate([a_full, a_flash], axis=1)

    a_full.to_root('output.root', treename='Events