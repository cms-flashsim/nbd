# the loop for generating new events starting from gen-level information in the files
import sys
import os

from tqdm import tqdm
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))

from nbd.builder.nanomaker import nanomaker
from nbd.builder.objs_dicts import objs_dicts

if __name__ == "__main__":

    root = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
    new_root = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/"
    files_paths = [
        os.path.join(d, f)
        for d in os.listdir(root)
        for f in os.listdir(os.path.join(root, d))
    ]

    files_paths = files_paths[3:4]

    print(f"We will process a total of {len(files_paths)} files")

    # generation loop
    for path in tqdm(files_paths):
        path_str = str(path)
        nanomaker(path_str, "null", objs_dicts, device="cuda:0",  limit=1000)