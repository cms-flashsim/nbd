import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset


class GenDataset(Dataset):
    def __init__(self, df, columns, oversampling_factor=1):
        data = df.loc[:, columns].values
        if oversampling_factor > 1:
            data = np.repeat(data, oversampling_factor, axis=0)
        self.train_data = torch.tensor(data, dtype=torch.float32)

    def __len__(self):
        return len(self.train_data)

    def __getitem__(self, idx):
        return self.train_data[idx]