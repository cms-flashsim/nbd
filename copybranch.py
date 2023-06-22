import numpy as np
import ROOT
import time
import torch
from nbd.models.electrons.geneleeff import ElectronClassifier

model = ElectronClassifier(2)


# f1=ROOT.TFile.Open("/scratch/arizzi/45000E5B-82CA-E143-85F3-610BCF163EF4.root")
# f3=ROOT.TFile.Open("c.root","RECREATE")
f3 = ROOT.TFile.Open("c.root")


@ROOT.Numba.Declare(["RVec<float>", "RVec<float>"], "RVec<float>")
def jetSim(x, y):
    npx = np.array([i for i in x])
    npy = np.array([i for i in y])
    npx *= 1.1
    xy = np.stack((npx, npy), axis=1)
    input = torch.tensor(xy, dtype=torch.float32)
    output = model.predict(input)
    # return xy.flatten()
    return output.detach().numpy().flatten()


if False:
    t1 = f1.Get("Events")
    t3 = t1.CloneTree(0)
    buff = numpy.zeros(1, dtype=numpy.dtype("i8"))
    buff2 = numpy.zeros(1, dtype=numpy.dtype("i8"))
    t3.Branch("GenEvent", buff, "GenEvent/L")
    t3.Branch("GenEventFold", buff2, "GenEventFold/L")
    print("start")
    tstart = time.perf_counter()
    for i, e in enumerate(t1):
        buff[0] = i
        for j in range(4):
            buff2[0] = j
            t3.Fill()
    time1 = time.perf_counter()
    t3.Write()
    time2 = time.perf_counter()
    print(time1 - tstart, time2 - tstart)

else:
    t3 = f3.Get("Events")
ROOT.gInterpreter.ProcessLine("using namespace ROOT::VecOps;")
rdf = ROOT.RDataFrame(t3)
r = rdf.Define("FlashJets", "Numba::jetSim(GenJet_pt,GenJet_eta)")
# r1=r.Define("ptindex","Enumerate(GenJet_pt)")
# r2=r1.Define("FlashJet_pt","Take(FlashJets,ptindex)")
r2 = r.Define("FlashJet_pt", "Take(FlashJets,Enumerate(GenJet_pt)*2)").Define(
    "FlashJet_eta", "Take(FlashJets,Enumerate(GenJet_pt)*2+1)"
)
r2.Display(
    ["FlashJets", "FlashJet_pt", "FlashJet_eta", "GenJet_pt", "GenJet_eta"]
).Print()

print(t3.GetEntries())
# 3.Scan("Jet_pt:GenEvent:GenEventFold")
