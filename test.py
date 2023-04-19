# the loop for generating new events starting from gen-level information in the files
import sys
import os

from tqdm import tqdm
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))

from nbd.builder.nanomaker import nanomaker
from nbd.builder.objs_dicts import objs_dicts

if __name__ == "__main__":
    print("Starting the generation of new events")
    # root_nano = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
    # new_root = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/"
    # files = [
    #     os.path.join(d, f)
    #     for d in os.listdir(root_nano)
    #     for f in os.listdir(os.path.join(root_nano, d))
    # ]

    # files_paths = [os.path.join(root_nano, f) for f in files]
    # files_paths = files_paths[:1]
    # files_paths = ["~/43C42694-5B0A-7D47-B7E8-59249FFD69CD.root"] # DY
    files_paths = ["~/151B72D8-0233-8D4E-AE8A-6611942542C0.root"]  # TTJets

    print(files_paths)
    print(f"We will process a total of {len(files_paths)} files")

    # generation loop
    for path in tqdm(files_paths):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        nanomaker(path, "null", ["Electron", "Jet"], device=device, limit=1000)
