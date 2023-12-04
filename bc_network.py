import torch
import torch.nn as nn
import torch.nn.functional as F

class BCPlayingNetwork(nn.Module):

    def __init__(self):
        super().__init__()
        # as defined in Demirdover et al.
        self.playNet = nn.Sequential(
            nn.Linear(260,83),
            nn.Sigmoid(),
            nn.Linear(83,52),
            nn.Sigmoid()
        )

    def forward(self, state):
        return self.playNet(state)

class BCPassingNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # as defined in Demirdover et al.
        self.playNet = nn.Sequential(
            nn.Linear(104,35),
            nn.Sigmoid(),
            nn.Linear(35,52),
            nn.Sigmoid()
        )

    def forward(self, state):
        return self.playNet(state)