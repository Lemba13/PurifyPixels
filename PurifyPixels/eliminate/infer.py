from .model import Generator
from .dataset import EliDataset
from torch.utils.data import DataLoader
import torch
import os
import numpy as np

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def purify_image(img_path: str):
    """
    Purifies an image using a pre-trained generator model to remove steganographic content

    Args:
        img_path (str): The file path to the image to be purified.

    Returns:
        tuple: A tuple containing:
            - out (numpy.ndarray): The purified image as a NumPy array with shape (H, W, C).
            - fpath (str): The file path of the input image.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '..', 'checkpoints/generator.pt')

    model = Generator()
    model.load_state_dict(torch.load(model_path))
    model = model.to(device)
    
    ds = EliDataset([img_path])
    dl = DataLoader(ds,
                    batch_size=1,
                    shuffle=True,
                    num_workers=1,
                    pin_memory=True,
                    drop_last=False,
                    persistent_workers=True)

    img, fpath = next(iter(dl))

    with torch.no_grad():
        raw_out = model(img.to(device))

    out = raw_out.detach().cpu().squeeze(0).permute(1,2,0).numpy()
    out = (out*255).astype(np.uint8)

    return out, fpath[0]


    
