import os
from nbd.builder.nanomaker import nanomaker

import ROOT

# ROOT::EnableImplicitMT()

obj_list = ["Electron", "Electron_fromJets", "Muon", "Jet"]

# processes = ["DYM50", "DYZpt-0To50", "DYZpt-50To100", "DYZpt-100To250", "DYZpt-250To400", "DYZpt-400To650", "DYZpt-650ToInf"]
# "106X_upgrade2018_realistic_v16_L1v1-v1"  "106X_upgrade2018_realistic_v16_L1v1-v2"
process = "DYM50"
if process == "DYM50":
    nano = "106X_upgrade2018_realistic_v16_L1v1-v2"
else:
    nano = "106X_upgrade2018_realistic_v16_L1v1-v1"

full_dir = os.path.join("/scratchnvme/malucchi/hbb_samples", process, nano)

flash_dir = os.path.join("/scratchnvme/cattafe/FlashSim-Samples", process, nano)

if os.path.isdir(flash_dir) is False:
    os.makedirs(flash_dir)

subdirs = os.listdir(full_dir)

for subdir in subdirs:
    if os.path.isdir(os.path.join(flash_dir, subdir)) is False:
        os.mkdir(os.path.join(flash_dir, subdir))

files = [
    os.path.join(subdir, file)
    for subdir in subdirs
    for file in os.listdir(os.path.join(full_dir, subdir))
]

input_files = [os.path.join(full_dir, file) for file in files]

output_files = [os.path.join(flash_dir, file) for file in files]

print(f"Input files: {input_files}")
print(f"Output files: {output_files}")

print(f"We will process a total of {len(input_files)} files")

for input, output in zip(input_files, output_files):
    nanomaker(input, output, obj_list, device="cuda:0", limit=None)
