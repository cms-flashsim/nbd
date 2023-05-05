import numpy as np

# from nbd.postprocessing.jets.columns_jets import

"""
Dictionary of postprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

unsmearing: ["d", [inf, sup]]
transformation: ["i", func, [a, b]]  # func(x) - b / a

In the case of multiple operations, order follows the operation list indexing.
"""

keys = ["eta", "phi", "pt", "msoftdrop", "particleNetMD_XbbvsQCD"]
full_keys = [f"FatJet_{key}" for key in keys]
post_actions = [
    [["a", "GenJetAK8_eta"], ["s"]],
    [["a", "GenJetAK8_phi"], ["pmp"], ["s"]],
    [["m", "GenJetAK8_pt"], ["s"]],
    [["m", "GenJetAK8_mass"], ["lower_b", 0, -10], ["s"]],
    [["s"]],
]

target_dictionary_fatjets = dict(zip(full_keys, post_actions))
