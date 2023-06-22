
void MakeTreeFunc(std::string inFileputFile, std::string outputFile) {

  // Open inFileput file
  // ? Or pass the open file to the function
  TFile *inFile = TFile::Open(inFileputFile.c_str());
  // Get other trees
  TTree *oldLumi = (TTree *)inFile->Get("LuminosityBlocks");
  TTree *oldRuns = (TTree *)inFile->Get("Runs");
  TTree *oldMetaData = (TTree *)inFile->Get("MetaData");
  // Get the events tree
  TTree *oldEvents = (TTree *)inFile->Get("Events");
  auto listOfBranches = {
      "Electron_*",
      "nElectron",
  }; // List of simulated branches
  int entries = -1;

  // Clone the events tree
  // SetStatus 0 for all the branches that we have simulated
  oldEvents->SetBranchStatus("*", 1);
  for (auto branch : listOfBranches) {
    oldEvents->SetBranchStatus(branch, 0);
  }

  TFile *outFile = TFile::Open(outputFile.c_str(), "RECREATE"); // ? or UPDATE
  TTree *newEvents = new TTree("Events", "Events");
  // newEvents->CopyEntries(oldEvents, entries, );

  // auto oldBranch = oldEvents->GetBranch("nElectron");
  // auto newBranch = newEvents->GetBranch("nElectron");
  // cout << "Old Address" << oldBranch->GetAddress() << endl;
  // cout << "New Address" << newBranch->GetAddress() << endl;

  // Third file from which we want to copy the nElectron branch
  // TFile *thirdFile =
  // TFile::Open("~/3FF6EC80-4D51-B746-B120-32E958184013.root"); TTree
  // *thirdEvents = (TTree *)thirdFile->Get("Events");

  // auto branch = thirdEvents->GetBranch("nElectron");
  // Check if the branch has an address
  // if (!branch->GetAddress()) {
  //   std::cout << "No address" << std::endl;
  // }
  // Create the new branch
  // newEvents->Branch("nElectron", branch->GetAddress(), "nElectron/I");
  // Copy the selected entries

  newEvents->CopyEntries(oldEvents, entries, "fast", true);

  // ! Add the FlashSimulated branches inFile the newEvents tree

  // Create the FullSim tree
  oldEvents->SetBranchStatus("*", 0);
  for (auto branch : listOfBranches) {
    oldEvents->SetBranchStatus(branch, 1);
  }

  TTree *fullSim = oldEvents->CloneTree(0);
  fullSim->CopyEntries(oldEvents, entries);
  fullSim->SetName("FullSim");

  // Clone the other trees
  TTree *newLumi = oldLumi->CloneTree();
  TTree *newRuns = oldRuns->CloneTree();
  TTree *newMetaData = oldMetaData->CloneTree();

  outFile->Write();
}

void MakeTree() {
  // MakeTreeFunc(" ~/3FF6EC80-4D51-B746-B120-32E958184013.root",
  // "~/output.root");
  MakeTreeFunc(" ~/OversampledTH/test_oversampling.root", "~/output.root");
}