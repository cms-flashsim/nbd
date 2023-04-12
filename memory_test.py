import os
import ROOT
import awkward as ak
import numpy as np

path = os.path.join(
    ".",
    "..",
    "FlashSim-Electrons",
    "extraction",
    "dataset",
    "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
)

full = ROOT.RDataFrame("Events", path).Range(10)

full_columns_list = list(full.GetColumnNames())
print(full_columns_list[:2])
for col in full_columns_list:
    print(type(col))
# full_columns = list((str(col) for col in full_columns_list))

# print(full_columns)

# a_full = ak.from_rdataframe(full, columns=full_columns)

# print(a_full.fields)
