# core functions for the nano builder
import os
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
from matplotlib import pyplot as plt
from nbd.utils.gendataset import GenDataset
from nbd.postprocessing.postprocessing import postprocessing
from nbd.postprocessing.electrons.columns_ele_old import pu

# from ..models.electrons.geneleeff import ElectronClassifier
from torch.utils.data import DataLoader


def isReco(y_pred):
    p = np.random.rand(y_pred.size)

    # Temporary fix for efficiency model
    # p = np.random.uniform(0, 0.5, y_pred.size)
    return y_pred > p


def compute_efficiency(model, model_path, data, device="cpu", batch_size=10000):
    model.load_state_dict(torch.load(model_path))
    model = model.to(device)
    model.eval()
    X = GenDataset(data, data.columns).train_data.to(device)
    loader = torch.utils.data.DataLoader(X, batch_size=batch_size, shuffle=False)
    y_pred = np.array([])
    with torch.no_grad():
        for batch in loader:
            out = model.predict(batch)  # predict
            y_pred = np.concatenate((y_pred, out.cpu().numpy().flatten()))

    mask = isReco(y_pred)
    return mask


def select_gen(
    a_gen_data,
    eff_columns,
    gen_columns,
    eff_model,
    eff_model_path,
    device="cpu",
    eff=True,
    batch_size=10000,
):
    a_gen = a_gen_data[gen_columns]
    ev_struct = ak.num(a_gen[gen_columns[0]])
    print(ev_struct)

    if eff:
        a_eff = a_gen_data[eff_columns]
        df_eff = ak.to_dataframe(a_eff).reset_index(drop=True)
        eff_mask = compute_efficiency(
            eff_model, eff_model_path, df_eff, device, batch_size=batch_size
        )
    else:
        eff_mask = np.ones(ak.sum(ev_struct), dtype=bool)

    a_eff_mask = ak.unflatten(eff_mask, ev_struct)

    # a_gen = a_gen_data[gen_columns]
    a_gen["Mask"] = a_eff_mask

    if set(pu) <= set(gen_columns):
        gen_columns_nopu = [var for var in gen_columns if var not in pu]

        masked_gen = a_gen[gen_columns_nopu][a_gen["Mask"]]

        # add back Pileup columns (creates empty events for masked-out events)
        for col in pu:
            masked_gen[col] = a_gen[col]
    else:
        # if eff:
        masked_gen = a_gen[gen_columns][a_gen["Mask"]]
        # else:
        #     masked_gen = a_gen[gen_columns]

    reco_struct = ak.num(masked_gen[gen_columns[0]], axis=1)

    to_flash = ak.to_dataframe(masked_gen).reset_index(drop=True)
    # drop mask column
    # to_flash = to_flash.drop(columns=["Mask"])

    return to_flash, reco_struct


def flash_simulate(
    flow_loader,
    model_path,
    to_flash,
    gen_columns,
    reco_columns,
    vars_dictionary,
    scale_file_path,
    reco_struct,
    device="cpu",
    batch_size=10000,
    saturate_ranges_path=None,
    gen_postrpocessing_dict=None,
):
    dataset = GenDataset(to_flash, gen_columns)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    flow_tuple = flow_loader(
        device=device, model_dir=os.path.dirname(__file__), filename=model_path
    )
    # assumes flow is always the frist element of the tuple
    flow = flow_tuple[0]
    flow = flow.to(device)

    flow.eval()

    tot_sample = []
    leftover_sample = []
    times = []

    print(f"Batch size: {batch_size}")
    with torch.no_grad():
        for batch_idx, y in enumerate(data_loader):
            print(f"Batch: {batch_idx}/{len(data_loader)}")

            y = y.float().to(device, non_blocking=True)
            if len(y) == batch_size:
                start = time.time()
                while True:
                    try:
                        sample = flow.sample(1, context=y)
                        break
                    except AssertionError:
                        print("Error, retrying")
                taken = time.time() - start
                # print(f"{(batch_size / taken):.0f} Hz")
                times.append(taken)
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                tot_sample.append(sample)

            else:
                leftover_shape = len(y)
                while True:
                    try:
                        sample = flow.sample(1, context=y)
                        break
                    except AssertionError:
                        print("Error, retrying")
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                leftover_sample.append(sample)

    print(f"Mean rate: {batch_size / np.mean(times)} Hz")

    reco_dim = len(reco_columns)
    tot_sample = np.array(tot_sample)
    tot_sample = np.reshape(tot_sample, ((len(data_loader) - 1) * batch_size, reco_dim))
    leftover_sample = np.array(leftover_sample)
    leftover_sample = np.reshape(leftover_sample, (leftover_shape, reco_dim))
    total = np.concatenate((tot_sample, leftover_sample), axis=0)

    # save hist of all 5 variables
    ranges = [[0.4, 1.5], [-0.10, 0.10], [-0.10, 0.10], [-2, 4], [-1, 1.1]]
    for i in range(5):
        plt.figure()
        plt.hist(total[:, i], bins=100, range=ranges[i])
        plt.savefig(f"hist_{i}pre.png")
    
    if gen_postrpocessing_dict is not None:
        to_flash = postprocessing(to_flash, None, gen_postrpocessing_dict, None, None)
    total = pd.DataFrame(total, columns=reco_columns)

    total = postprocessing(
        total, to_flash, vars_dictionary, scale_file_path, saturate_ranges_path
    )

        # save hist of all 5 variables
    for j in total.columns:
        plt.figure()
        plt.hist(total[j].values, bins=100)
        plt.savefig(f"hist_{j}post.png")
    # These lines are needed to avoid TStreamerInfo warnings when writing FlashSim tree
    d_out = dict(zip(total.columns, total.values.T))
    a_out = ak.zip(d_out)

    final_dict = {}
    for col in a_out.fields:
        print(col)
        final_dict[col] = ak.unflatten(a_out[col], reco_struct, axis=0)

    a_flash = ak.Array(final_dict)

    return a_flash
