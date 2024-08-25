import cv2
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from torchvision import transforms


class SteganalysisDataset(Dataset):

    # This class only returns a single image by doing the necessary preprocessing (similar to the ones used during training)
    def __init__(self, data_path):
        self.data_path = data_path

    
    def __getitem__(self, index: int):
        image = cv2.imread(self.data_path).astype(np.float64)
        image /= 255.0
        
        transform = transforms.ToTensor()
        image = transform(image)
        return image.unsqueeze(0)