# the loop for generating new events starting from gen-level information in the files
import os
from nbd.builder.nanomaker import nanomaker
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nfiles", type=int, default=-1, help="Number of files")
parser.add_argument(
    "--resume",
    type=int,
    default=1,
    help="Resume from file number (starts from 1)",
)
parser.add_argument("--range", type=int, default=-1, help="Number of events per file")
parser.add_argument("--device", type=str, default="cuda:0", help="Device to use")
args = parser.parse_args()

obj_list = ["Electron", "Electron_fromJets", "Muon", "Jet"]

ROOT.EnableImplicitMT()

mc_dir = "/gpfs/ddn/srm/cms//store/mc"

### DrellYan new
prod_camp = "RunIISummer20UL18NanoAODv9"
sample = "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8"
nano = "NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2"


### DrellYan old
# prod_camp = "RunIIAutumn18NanoAODv6"
# sample = "DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8"
# nano = "NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1"

### TT
# prod_camp = "RunIISummer20UL18NanoAODv9"
# sample = "TTJets_TuneCP5_13TeV-madgraphMLM-pythia8"
# nano = "NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1"

### TT training
# mc_dir = "/gpfs/ddn/cms/user/cattafe/mc/"
# prod_camp = "RunIIAutumn18NanoAODv6"
# sample = "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"
# nano = "NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1"

flash_dir = "/gpfs/ddn/cms/user/cattafe/FlashSim"

# flash_dir = "/gpfs/ddn/cms/user/cattafe/FlashSim/no_eff/" # no efficiency for electrons


if __name__ == "__main__":
    print("Starting the generation of new events")

    # Get FullSim path
    root_nano = os.path.join(mc_dir, prod_camp, sample, nano)
    # FlashSim path
    new_dir = os.path.join(flash_dir, prod_camp, sample, nano)

    # Make FlashSim directory
    if os.path.isdir(new_dir) is False:
        os.makedirs(new_dir)

    # Get list of subdirectories of FullSim dataset
    subdirs = os.listdir(root_nano)

    # Make subdirectories in FlashSim dataset
    for subdir in subdirs:
        if os.path.isdir(os.path.join(new_dir, subdir)) is False:
            os.mkdir(os.path.join(new_dir, subdir))

    # Get list of files in FullSim dataset as subdir/file.root
    files = [
        os.path.join(subdir, file)
        for subdir in subdirs
        for file in os.listdir(os.path.join(root_nano, subdir))
    ]

    # Get paths to FullSim files
    input_files = [os.path.join(root_nano, file) for file in files]
    original_len = len(input_files)

    # Get paths to FlashSim files
    output_files = [os.path.join(new_dir, file) for file in files]

    # Test on a single file
    # files = ["~/43C42694-5B0A-7D47-B7E8-59249FFD69CD.root"]  # DY
    # files = ["~/151B72D8-0233-8D4E-AE8A-6611942542C0.root"]  # TTJets

    if args.nfiles > 0:
        input_files = input_files[(args.resume - 1) : (args.resume - 1 + args.nfiles)]
        output_files = output_files[(args.resume - 1) : (args.resume - 1 + args.nfiles)]
    else:
        input_files = input_files[(args.resume - 1) :]
        output_files = output_files[(args.resume - 1) :]

    print(f"We will process a total of {len(input_files)} files out of {original_len}")

    if args.range > 0:
        limit = args.range
    else:
        limit = None

    # generation loop
    for i, (input, output) in enumerate(zip(input_files, output_files)):
        print(f"File {args.resume + i}/{original_len}", end=" ")
        if args.nfiles > 0:
            print(f"[{i+1}/{args.nfiles} of the requested files]", end="")
        print("\n")
        nanomaker(input, output, obj_list, device=args.device, limit=limit)
