import os
import ROOT
import awkward as ak
import numpy as np
import pandas as pd

path = os.path.join(
    ".",
    "..",
    "FlashSim-Electrons",
    "extraction",
    "dataset",
    "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
)

d = ROOT.RDataFrame("Events", path).Range(10)

a = ak.from_rdataframe(d, ["Electron_pt", "Electron_eta", "Electron_pt", "Pileup_nTrueInt"])


a.show(limit_cols=1000)

