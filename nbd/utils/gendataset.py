import pandas as pd
import torch
from torch.utils.data import Dataset


class GenDataset(Dataset):
    def __init__(self, df, columns):
        data = df.loc[:, columns]
        self.train_data = torch.tensor(data.values, dtype=torch.float32)

    def __len__(self):
        return len(self.train_data)

    def __getitem__(self, idx):
        return self.train_data[idx]