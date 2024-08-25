import torch
from torch import nn
from efficientnet_pytorch import EfficientNet


device = "cuda" if torch.cuda.is_available() else "cpu"

def get_net():
    net = EfficientNet.from_pretrained('efficientnet-b2')
    num_ftrs = net._fc.in_features
    net._fc = nn.Linear(num_ftrs, 4)
    return net.to(device)

def load_model(path):
    checkpoint = torch.load(path)
    model = get_net()
    model.load_state_dict(checkpoint['model_state_dict'])
    return model
