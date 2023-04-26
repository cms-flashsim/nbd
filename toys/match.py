import sys
import os
import ROOT

module = os.path.join(os.path.abspath(os.path.dirname(__file__)), "extraction.h")
ROOT.gInterpreter.ProcessLine(f'#include "{module}"')
# ROOT.EnableImplicitMT()

path = str(sys.argv[1])

file = ROOT.TFile.Open(path)

events = file.Events
full = file.FullSim

events.AddFriend(full, "FullSim")

rdf = ROOT.RDataFrame(events)

rdf = (
    rdf.Define("GenPart_ElectronIdx_empty", "Electron_genObjMatchMaker(GenPart_pt)")
    .Define(
        "GenPart_genElectron_ElectronIdx",
        "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, FullSim.Electron_pt, FullSim.Electron_eta, FullSim.Electron_phi, FullSim.Electron_charge, GenPart_ElectronIdx_empty, 0)",
    )
    .Define("GenElectronMask", "abs(GenPart_pdgId) == 11")
    .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
    .Define(
        "GenElectron_FullMatched",
        "GenPart_genElectron_ElectronIdx[GenElectronMask] >= 0",
    )
    .Define("FullMatched", "GenElectron_pt[GenElectron_FullMatched]")
)


n_full = full.Histo1D("FullMatched").GetEntries()

flash = ROOT.RDataFrame("Events", path)

n_flash = flash.Histo1D("Electron_pt").GetEntries()

print(f"Flash: {n_flash}")
print(f"Full: {n_full}")
