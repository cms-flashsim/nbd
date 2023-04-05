import os
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
from torch.utils.data import DataLoader
import nbd.builder.object_simulator as object_simulator
from objs_dicts import objs_dicts


def nanomaker(file_path, new_file_path, objects_keys=None, device='cpu', limit=1000):

    if limit is not None:
        full = ROOT.RDataFrame("Events", file_path).Range(limit)
    else:
        full = ROOT.RDataFrame("Events", file_path)
    full_columns = full.GetColumnNames()

    a_full = ak.from_rdataframe(full, columns=full_columns)

    flash_list = []
    for i in range(len(objects_keys)):
        a_flash = object_simulator.simulator(
            full,
            device=device,
            **objs_dicts[i]
        )

        flash_list.append(a_flash)

    # explicit check on dict keys
    # merge same type of reco on the evet with ak.concatenate (for flash)
    dict_1 = dict(zip(a_full.fields, [a_full[field] for field in a_full.fields]))
    for i in range(len(objects_keys)):
        dict_2 = dict(zip(flash_list[i].fields, [flash_list[i][field] for field in flash_list[i].fields]))
        total = dict_1 | dict_2
        dict_1 = total

    merged = ak.zip(total, depth_limit=1)
    to_file = ak.to_rdataframe(merged)
    to_file.Snapshot("Events", "~/test.root")
    # a_full.to_root("output.root", treename="Events")
