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
from nbd.builder.objs_dicts import objs_dicts


def nanomaker(file_path, new_file_path, objects_keys=None, device="cpu", limit=None):
    if limit is not None:
        full = ROOT.RDataFrame("Events", file_path).Range(limit)
    else:
        full = ROOT.RDataFrame("Events", file_path)

    full_columns_list = full.GetColumnNames()

    full_columns = []
    for name in full_columns_list:
        full_columns.append(str(name))

    a_full = ak.from_rdataframe(full, columns=full_columns)
    print("Awkward array created")

    flash_list = []
    for obj in objects_keys:
        a_flash = object_simulator.simulator(full, device=device, **objs_dicts[obj])
        flash_list.append(a_flash)

    # explicit check on dict keys
    # merge same type of reco on the evet with ak.concatenate (for flash)
    dict_1 = dict(zip(a_full.fields, [a_full[field] for field in a_full.fields]))
    for i in range(len(objects_keys)):
        dict_2 = dict(
            zip(
                flash_list[i].fields,
                [flash_list[i][field] for field in flash_list[i].fields],
            )
        )
        total = {**dict_1, **dict_2}
        dict_1 = total

    to_file = ak.to_rdataframe(total)
    to_file.Snapshot("Events", "~/test_TTJets.root")
    # a_full.to_root("output.root", treename="Events")
