import torch
from torch.utils.data import Dataset
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image

HIGH_RES = 512
LOW_RES = HIGH_RES // 4

highres_transform = A.Compose(
    [
        A.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        ToTensorV2(),
    ]
)

lowres_transform = A.Compose(
    [
        A.Resize(width=LOW_RES, height=LOW_RES, interpolation=Image.BICUBIC),
        A.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        ToTensorV2(),
    ]
)

both_transforms = A.Compose(
    [
        A.RandomCrop(width=HIGH_RES, height=HIGH_RES),
    ]
)


class EliDataset(Dataset):
    def __init__(self, filepaths):
        self.filepaths = filepaths

    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, index):
        encoded_path = self.filepaths[index]

        encoded_img = cv2.imread(encoded_path)

        encoded_img = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2RGB)

        encoded_img = both_transforms(image=encoded_img)["image"]
        low_res = lowres_transform(image=encoded_img)["image"]

        return low_res.type(torch.FloatTensor), self.filepaths[index]
