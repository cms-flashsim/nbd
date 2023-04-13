import os
import ROOT
import awkward as ak
import numpy as np

# path = os.path.join(
#     ".",
#     "..",
#     "FlashSim-Electrons",
#     "extraction",
#     "dataset",
#     "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
# )

path = "../43C42694-5B0A-7D47-B7E8-59249FFD69CD.root"


full = ROOT.RDataFrame("Events", path).Range(10)

full_columns_list = full.GetColumnNames()

full_columns = []
for name in full_columns_list:
    full_columns.append(str(name))

print(type(full_columns[0])) 

a_full = ak.from_rdataframe(full, columns=full_columns)

print(a_full.fields)
