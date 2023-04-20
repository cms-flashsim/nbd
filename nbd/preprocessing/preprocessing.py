import numpy as np
import pandas as pd


def transform(df, column_name, function, p):
    """
    Performs a function tranformation on column
    """
    print(f"Applying {function} with parameters {p}...")
    df[column_name] = df[column_name].apply(lambda x: function(x * p[0] + p[1]))
    return df[column_name]


def process_column_var(column_name, operations, df):
    for i, op in enumerate(operations):
        if op[0] == "":
            function = op[1]
            p = op[2]
            df[column_name] = transform(df, column_name, function, p)
        else:
            pass
    return df[column_name]


def preprocessing(
    df,
    vars_dictionary,
):
    """
    preprocessing general function given any dataframe and its dictionary
    """

    for column_name, operation in vars_dictionary.items():
        df[column_name] = process_column_var(column_name, operation, df)

    return df
