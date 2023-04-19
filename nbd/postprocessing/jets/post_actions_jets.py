import numpy as np

# from nbd.postprocessing.jets.columns_jets import

"""
Dictionary of postprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

unsmearing: ["d", [inf, sup]]
transformation: ["i", func, [a, b]]  # func(x - b) / a

In the case of multiple operations, order follows the operation list indexing.
"""

keys = ["eta", "mass", "phi", "pt"]
full_keys = [f"MJets_{key}" for key in keys]
post_actions = [
    [["a", "GenJet_eta"]],
    [["m", "GenJet_mass"]],
    [["a", "GenJet_phi"], ["pmp"]],
    [["m", "GenJet_pt"]],
]

target_dictionary_jets = dict(zip(full_keys, post_actions))
