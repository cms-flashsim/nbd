import os
import sys
import json
import numpy as np
import pandas as pd


from matplotlib import pyplot as plt


def multiply_by_gen(df, gen_df, column_name, gen_column_name):
    print("Multiplied!")
    print(df[column_name])
    df[column_name] = df[column_name] * gen_df[gen_column_name]
    print(df[column_name])
    return df[column_name]


def add_gen(df, gen_df, column_name, gen_column_name):
    df[column_name] = df[column_name] + gen_df[gen_column_name]
    return df[column_name]


def restore_range(column_name, scale_dict, df):
    """
    Restore data range to the original value before dividing by max
    """
    scale = scale_dict[column_name]
    df[column_name] = df[column_name] * scale
    return df[column_name]


def inverse_transform(df, column_name, function, p):
    df[column_name] = df[column_name].apply(lambda x: (function(x) - p[1]) / p[0])
    return df[column_name]


def unsmearing(df, column_name, interval):
    """Unsmearing for in variables. We have gaussian and uniform smearing.
    If we have interval, that means that we built a fake gaussian dataset
    in the selected interval, and then we just have to compute the sample mean
    in this range.
    """
    val = df[column_name].values
    if interval != None:
        mask_condition = np.logical_and(val >= interval[0], val <= interval[1])

        # Assuming that the value to be unsmeared is always np.log(1e-3),
        # which corresponds to an int value of 0 after a np.log(x + 1e-3)
        # transformation

        val[mask_condition] = np.log(1e-3)
    else:
        df[column_name] = np.rint(df[column_name].values)
    return df[column_name]


def cut_unsmearing(df, column_name, cut, x1, x2):
    val = df[column_name].values
    df[column_name] = np.where(val < cut, x1, x2)
    return df[column_name]


def process_column_var(column_name, operations, df):
    for op in operations:
        if op[0] == "d":
            mask_condition = op[1]
            df[column_name] = unsmearing(df, column_name, mask_condition)

        elif op[0] == "c":
            cut = op[1]
            vals = op[2]
            df[column_name] = cut_unsmearing(df, column_name, cut, *vals)

        elif op[0] == "i":
            function = op[1]
            p = op[2]
            df[column_name] = inverse_transform(df, column_name, function, p)

        else:
            return df[column_name]
    return df[column_name]


def process_column_var_gen(column_name, operations, df, gen_df):
    for op in operations:
        print(op[0])
        if op[0] == "m":
            print(column_name)
            gen_column_name = op[1]
            df[column_name] = multiply_by_gen(df, gen_df, column_name, gen_column_name)

        elif op[0] == "a":
            print(column_name)
            gen_column_name = op[1]
            df[column_name] = add_gen(df, gen_df, column_name, gen_column_name)

        else:
            return df[column_name]
    return df[column_name]


def postprocessing(
    df, gen_df, vars_dictionary, scale_file_path, saturate_ranges_path=None
):
    """
    Postprocessing general function given any dataframe and its dictionary
    """

    with open(scale_file_path) as scale_file:
        scale_dict = json.load(scale_file)

    for column_name, operation in vars_dictionary.items():
        df[column_name] = restore_range(column_name, scale_dict, df)
        df[column_name] = process_column_var(column_name, operation, df)

    # df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis="columns")]
    if saturate_ranges_path != None:
        # Saturate ranges is a json file with the ranges to saturate
        with open(saturate_ranges_path) as saturate_file:
            saturate_dict = json.load(saturate_file)

        for col, ranges in saturate_dict.items():
            if col in saturate_dict.keys():
                min = ranges[0]
                max = ranges[1]
                val = df[col].values
                saturated = np.where(val < min, min, val)
                saturated = np.where(saturated > max, max, saturated)
                df[col] = saturated

    for column_name, operation in vars_dictionary.items():
        print("pre-multiply")
        df[column_name] = process_column_var_gen(column_name, operation, df, gen_df)

    return df
