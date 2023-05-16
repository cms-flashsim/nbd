import os
import ROOT
import awkward as ak

path = os.path.join(
    ".",
    "..",
    "FlashSim-Electrons",
    "extraction",
    "dataset",
    "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
)

rdf = ROOT.RDataFrame("Events", path).Range(5)


awk = ak.from_rdataframe(rdf, ["run", "event"])

awk.show(limit_cols=1000)