# core functions for the nano builder
import os
from tqdm import tqdm
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
from nbd.models.modded_cfm.modded_cfm import ModelWrapper

# from ..models.electrons.geneleeff import ElectronClassifier
from torch.utils.data import DataLoader

from torchdiffeq import odeint


def isReco(y_pred):
    p = np.random.rand(y_pred.size)

    # Temporary fix for efficiency model
    # p = np.random.uniform(0, 0.5, y_pred.size)
    return y_pred > p


def compute_efficiency(model, model_path, data, device="cpu", batch_size=10000):
    print(f"Computing efficiency using {model}")
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
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
    oversampling_factor=1,
):
    a_gen = a_gen_data[gen_columns]
    ev_struct = ak.num(a_gen[gen_columns[0]])
    print(f"Number of objects: {sum(ev_struct)}")

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
    # add np.repeat for oversampling here if needed
    if oversampling_factor > 1:
        reco_struct = np.repeat(reco_struct, oversampling_factor, axis=0)
        masked_gen["evt_idx"] = ak.Array(np.arange(len(masked_gen)))
        masked_gen = ak.concatenate(
            [masked_gen for _ in range(oversampling_factor)], axis=0
        )
        masked_gen = masked_gen[
            ak.argsort(masked_gen["evt_idx"], axis=0, ascending=True)
        ]

    print(f"Number of objects after selection: {sum(reco_struct)}")

    to_flash = ak.to_dataframe(masked_gen).reset_index(drop=True)

    if oversampling_factor > 1:
        to_flash = to_flash.drop(columns=["evt_idx"])

    # drop mask column
    # to_flash = to_flash.drop(columns=["Mask"])

    return to_flash, reco_struct


def nan_resampling(total, to_flash, flow, device):
    total = torch.tensor(total, dtype=torch.float32).to(device)
    gen = torch.tensor(to_flash.values, dtype=torch.float32).to(device)
    nan_mask = torch.isnan(total).any(axis=1)
    if nan_mask.any():
        print("Resampling nan values")
        nan_idx = torch.argwhere(nan_mask)
        # Generate new samples
        flow.eval()
        while True:
            with torch.no_grad():
                total[nan_idx] = flow.sample(1, context=gen[nan_mask])
                if not torch.isnan(total[nan_idx]).any():
                    print("Resampling done")
                    break
    total = total.detach().cpu().numpy()
    return total


def flash_simulate(
    flow_loader,
    model_path,
    to_flash,
    gen_columns,
    reco_columns,
    vars_dictionary,
    scale_file_path,
    reco_struct,
    continuous=False,
    device="cpu",
    batch_size=10000,
    saturate_ranges_path=None,
    gen_postrpocessing_dict=None,
    oversampling_factor=1,
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

    if continuous:
        sampler = ModelWrapper(flow, context_dim=len(gen_columns))
        timesteps = 100
        t_span = torch.linspace(0, 1, timesteps).to(device)

    tot_sample = []
    leftover_sample = []
    times = []
    leftover_shape = 0
    print(f"Batch size: {batch_size}")
    with torch.no_grad():
        for batch_idx, y in enumerate(tqdm(data_loader, ascii=True)):
            # print(f"Batch: {batch_idx}/{len(data_loader)}")
            y = y.float().to(device, non_blocking=True)
            if len(y) == batch_size:
                start = time.time()

                if not continuous:
                    while True:
                        try:
                            sample = flow.sample(1, context=y)
                            break
                        except AssertionError:
                            print("Error, retrying")
                if continuous:
                    x0_sample = torch.randn(len(y), len(reco_columns)).to(device)
                    initial_conditions = torch.cat([x0_sample, y], dim=-1)

                    sample = odeint(
                        sampler,
                        initial_conditions,
                        t_span,
                        atol=1e-6,
                        rtol=1e-6,
                        method="dopri5",
                    )[-1, :, : len(reco_columns)]

                else:
                    raise ValueError("Continuous should be True or False")

                taken = time.time() - start
                # print(f"{(batch_size / taken):.0f} Hz")
                times.append(taken)
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                tot_sample.append(sample)

            else:
                leftover_shape = len(y)
                start = time.time()
                while True:
                    try:
                        sample = flow.sample(1, context=y)
                        break
                    except AssertionError:
                        print("Error, retrying")
                taken = time.time() - start
                # print(f"{(leftover_shape / taken):.0f} Hz")
                times.append(taken)
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                leftover_sample.append(sample)

    print(f"Main sampling done with mean rate: {(batch_size / np.mean(times)):.0f} Hz")

    reco_dim = len(reco_columns)
    tot_sample = np.array(tot_sample)
    leftover_sample = np.array(leftover_sample)
    if leftover_shape > 0:
        tot_sample = np.reshape(
            tot_sample, ((len(data_loader) - 1) * batch_size, reco_dim)
        )
        leftover_sample = np.reshape(leftover_sample, (leftover_shape, reco_dim))
        total = np.concatenate((tot_sample, leftover_sample), axis=0)
    else:
        tot_sample = np.reshape(tot_sample, (len(data_loader) * batch_size, reco_dim))
        total = tot_sample

    total = nan_resampling(total, to_flash, flow, device)

    if gen_postrpocessing_dict is not None:
        to_flash = postprocessing(to_flash, None, gen_postrpocessing_dict, None, None)

    total = pd.DataFrame(total, columns=reco_columns)

    total = postprocessing(
        total, to_flash, vars_dictionary, scale_file_path, saturate_ranges_path
    )

    # These lines are needed to avoid TStreamerInfo warnings when writing FlashSim tree
    d_out = dict(zip(total.columns, total.values.T))
    a_out = ak.zip(d_out)

    final_dict = {}
    for col in a_out.fields:
        final_dict[col] = ak.unflatten(a_out[col], reco_struct, axis=0)

    a_flash = ak.Array(final_dict)

    return a_flash
