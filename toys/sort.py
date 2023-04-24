import os
import ROOT
import awkward as ak
import pandas as pd

# path = os.path.join(
#     ".",
#     "..",
#     "FlashSim-Electrons",
#     "extraction",
#     "dataset",
#     "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
# )

# rdf = ROOT.RDataFrame("Events", path).Range(5)

# awk = ak.from_rdataframe(rdf, ["Electron_pt", "Electron_eta"])

a = ak.Array(
    [
        {"Electron_pt": [21.6, 15, 45], "Electron_eta": [0.108, 18, 0.6]},
        {"Electron_pt": [], "Electron_eta": []},
        {"Electron_pt": [56, 12, 30], "Electron_eta": [0.6, 0.4, 0.3]},
    ]
)

b = a[a.Electron_pt > 20]
struct = ak.num(b.Electron_pt, axis=1)

df = ak.to_dataframe(b)

d = dict(zip(df.columns, df.values.T))

# # Metodo 1
# f = ak.zip(d)
# f = ak.unflatten(f, struct)

# Metodo 2
f = ak.zip(d)
tmp_dict = {}
for col in f.fields:
    print(f[col])
    a = ak.unflatten(f[col], struct, axis=0)
    tmp_dict[col] = a
    print(a)

f = ak.Array(tmp_dict)
f.show(limit_cols=1000)
f = f[ak.argsort(f["Electron_pt"], axis=-1, ascending=False, highlevel=False)]
f.show(limit_cols=1000)

to_rdf = dict(zip(f.fields, [f[field] for field in f.fields]))
rdf = ak.to_rdataframe(to_rdf)
rdf.Snapshot("Events", "test.root")

