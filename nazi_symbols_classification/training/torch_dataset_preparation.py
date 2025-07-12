import os
import torch
import matplotlib.image as mpimg
from torch.utils.data import Dataset


class ImageData(Dataset):
    """Custom dataset for loading images and their labels from a DataFrame."""
    def __init__(self, df, data_directory, transform, label_column):
        super().__init__()
        self.df = df
        self.data_directory = data_directory
        self.transform = transform
        self.label_column = label_column

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        img_name = self.df.path[index]
        label = self.df[self.label_column][index]

        img_path = os.path.join(self.data_directory, img_name)
        try:
            image = mpimg.imread(img_path)
        except Exception:
            if img_path.endswith(".png"):
                image = mpimg.imread(img_path, format="jpg")
            else:
                image = mpimg.imread(img_path, format="png")
        image = self.transform(image)
        return image, label


def get_device():
    """Determine the device to use for PyTorch operations."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def to_device(data, device):
    """Move data to the specified device."""
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


class ToDeviceLoader:
    """Data loader that moves batches to a specified device."""
    def __init__(self, data, device):
        self.data = data
        self.device = device

    def __iter__(self):
        for batch in self.data:
            yield to_device(batch, self.device)

    def __len__(self):
        return len(self.data)
