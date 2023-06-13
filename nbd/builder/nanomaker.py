import os
import psutil
import gc
import time
import numpy as np
import ROOT
import uproot
import awkward as ak
import pandas as pd
import torch
import nbd.builder.object_simulator as object_simulator
from nbd.builder.objs_dicts import objs_dicts, reco_objects, merge_dict
from nbd.utils.reco_full import get_reco_columns


def nanomaker(
    input_file,
    output_file,
    objects_keys=None,
    device="cpu",
    limit=None,
    filter_ak8=False,
    oversampling_factor=1,
):
    process = psutil.Process(os.getpid())
    print(f"Processing file {input_file}")

    file = ROOT.TFile.Open(input_file)
    events = file.Events
    lumi = file.LuminosityBlocks
    runs = file.Runs
    meta = file.MetaData

    print(
        f"Memory usage before processing: {(process.memory_info().rss / 1024 / 1024):.0f} MB"
    )

    if limit is not None:
        full = ROOT.RDataFrame(events).Range(limit)
    else:
        full = ROOT.RDataFrame(events)

    if filter_ak8:
        full = full.Filter("nFatJet >= 2").Filter(
            "GenJetAK8_pt[0] > 250 && GenJetAK8_pt[1] > 250"
        )

    # Getting the list of columns
    full_columns_list = full.GetColumnNames()

    full_columns_ = []
    for name in full_columns_list:
        full_columns_.append(str(name))

    # Temporary fix: LHEPdfWeight leads to a segmentation fault when calling ak.from_rdataframe
    full_columns = [name for name in full_columns_ if name != "LHEPdfWeight"]

    # Selecting FullSim reco variables to copy in the FullSim tree
    # Reco objects are defined in reco_full.py

    old_reco_columns = get_reco_columns(full_columns, reco_objects)

    # Create a type dictionary for the right casting
    type_dict = dict(
        zip(old_reco_columns, [full.GetColumnType(name) for name in old_reco_columns])
    )

    # Selecting the other variables

    remaining_columns = [var for var in full_columns if var not in old_reco_columns]

    a_rest = ak.from_rdataframe(full, columns=remaining_columns)

    # repeat for oversampling
    if oversampling_factor > 1:
        print(f"Oversampling of factor {oversampling_factor}...")
        a_rest["ev_idx"] = ak.Array(np.arange(len(a_rest)))
        a_rest = ak.concatenate([a_rest for _ in range(oversampling_factor)], axis=0)
        a_rest = a_rest[ak.argsort(a_rest["ev_idx"], axis=0, ascending=True)]
        print("Done")

    # Flash simulation

    flash_dict = {}
    for obj in objects_keys:
        # memory usage
        print(
            f"Memory usage before simulating {obj}: {(process.memory_info().rss / 1024 / 1024):.0f} MB"
        )
        print(f"Simulating {obj} collection...")
        a_flash = object_simulator.simulator(
            full,
            device=device,
            oversampling_factor=oversampling_factor,
            **objs_dicts[obj],
        )
        print(
            f"Memory usage after simulating {obj}: {(process.memory_info().rss / 1024 / 1024):.0f} MB"
        )
        print(f"Done")
        flash_dict[obj] = a_flash

    # Merge

    if merge_dict:
        for key in merge_dict.keys():
            print(f"Merging {key} collections...")
            # Get pt column name and nObject
            pt_col = [
                col
                for col in flash_dict[merge_dict[key][0]].fields
                if col.endswith("_pt")
            ][0]
            obj_name = pt_col.replace("_pt", "", 1)
            counter_col = f"n{obj_name}"

            input_list = []
            for subkey in merge_dict[key]:
                if subkey not in flash_dict.keys():
                    raise ValueError(f"Object {subkey} not found in flash_dict")
                # remove counter column (it breaks ak.concatenate)
                flash_dict[subkey] = flash_dict[subkey][
                    [x for x in (flash_dict[subkey]).fields if x != counter_col]
                ]
                input_list.append(flash_dict[subkey])
                # remove all subcollections from the main dictionary
                del flash_dict[subkey]

            # Merge all subcollections
            merged = ak.concatenate(input_list, axis=1)
            # Add the merged collection to the main dictionary
            flash_dict[key] = merged
            # Pt sort
            flash_dict[key] = flash_dict[key][
                ak.argsort(flash_dict[key][pt_col], axis=-1, ascending=False)
            ]
            # Add counter column
            flash_dict[key][counter_col] = ak.num(flash_dict[key][pt_col], axis=-1)

        print("Done")

    print(
        f"Memory after all object simulation: {(process.memory_info().rss / 1024/ 1024):.0f} MB"
    )

    # explicit check on dict keys
    # merge same type of reco on the evet with ak.concatenate (for flash)
    print("Making the final dictionary...")
    dict_1 = dict(
        zip(
            a_rest.fields,
            [a_rest[field] for field in a_rest.fields if field != "ev_idx"],
        )
    )
    for key in flash_dict.keys():
        dict_2 = dict(
            zip(
                flash_dict[key].fields,  # TODO check if fields are the same
                [flash_dict[key][field] for field in flash_dict[key].fields],
            )
        )
        total = {**dict_1, **dict_2}
        dict_1 = total

    print("Done")

    print(
        f"Memory after merging all collections: {(process.memory_info().rss / 1024/ 1024):.0f} MB"
    )

    print("Writing the FlashSim tree...")

    to_file = ak.to_rdataframe(total)

    # Cast the reco variables to the right type

    for name, type in type_dict.items():
        if name in total.keys():
            to_file = to_file.Redefine(name, f"({type}) {name}")

    to_file.Snapshot("Events", output_file)

    print("Done")

    # add a new ttrees to the output file

    print("Writing the FullSim tree...")
    a_full = ak.from_rdataframe(full, columns=old_reco_columns + ["run", "event"])
    d_full = dict(zip(a_full.fields, [a_full[field] for field in a_full.fields]))
    old_reco = ak.to_rdataframe(d_full)

    opts = ROOT.RDF.RSnapshotOptions()
    opts.fMode = "Update"
    old_reco.Snapshot("FullSim", output_file, "", opts)

    print("Done")

    print("Writing others trees...")
    outfile = ROOT.TFile.Open(output_file, "UPDATE")
    outfile.cd()
    lumi.CloneTree().Write()
    runs.CloneTree().Write()
    meta.CloneTree().Write()
    outfile.Close()

    print(
        f"Memory after writing the output file: {(process.memory_info().rss / 1024/ 1024):.0f} MB"
    )
    file.Close()

    del (
        file,
        full,
        lumi,
        runs,
        meta,
        old_reco,
        to_file,
        a_rest,
        a_full,
        total,
        d_full,
        dict_1,
        dict_2,
        flash_dict,
        input_list,
        merged,
        type_dict,
        opts,
    )
    gc.collect()

    print("Done")
