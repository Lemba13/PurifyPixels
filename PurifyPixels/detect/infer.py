from .model import load_model
from .dataset import SteganalysisDataset
import os
from matplotlib import pyplot as plt
import torch
from scipy.special import softmax
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
labels = ["Cover", "JMiPOD", "JUNIWARD", "UERD"]


def predict_steganography(image_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, '..', 'checkpoints/detector.bin')
        model = load_model(model_path)
        model.eval()
        image = SteganalysisDataset(image_path)
        image = image[0].to(device).float()
        output = model(image).to("cpu").detach().numpy()
        return labels[np.argmax(softmax(output))]



    
