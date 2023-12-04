from agent import Agent
from typing import List
import random
import torch
from bc_network import BCPlayingNetwork
from bc_network import BCPassingNetwork
import os
import torch.nn as nn
import torch.nn.functional as F

def main():
    playingData = torch.load(os.path.join("human_data", "playingData.pt"))
    passingData = torch.load(os.path.join("human_data", "passingData.pt"))

    playNet = BCPlayingNetwork()
    passNet = BCPassingNetwork()

    playingOptimizer = torch.optim.Adam(playNet.parameters(), lr=0.1)
    passingOptimizer = torch.optim.Adam(passNet.parameters(), lr=0.1)
    loss_function = nn.BCELoss()

    playingStates = playingData[:, :-1]
    idxs = playingData[:, -1].type(torch.long)
    idxs -= 2
    playingActions = F.one_hot(idxs, 52).type(torch.float)

    for i in range(2000):
        # zero out automatic differentiation from last time
        playingOptimizer.zero_grad()
        # run each state in batch through policy to get predicted logits for classifying action
        pred_action_logits = playNet(playingStates)
        # now compute loss by comparing what the policy thinks it should do with what the demonstrator didd
        loss = loss_function(pred_action_logits, playingActions)
        if i % 100 == 0:
            print("iteration", i, "bc loss", loss)
        # back propagate the error through the network to figure out how update it to prefer demonstrator actions
        loss.backward()
        # perform update on policy parameters
        playingOptimizer.step()

    passingStates = passingData[:, :-3]
    idxs = passingData[:, -3:].type(torch.long)
    idxs -= 2
    passingActions = F.one_hot(idxs[:,0], 52).type(torch.float) + F.one_hot(idxs[:,1], 52).type(torch.float) + F.one_hot(idxs[:,2], 52).type(torch.float)

    for i in range(2000):
        # zero out automatic differentiation from last time
        passingOptimizer.zero_grad()
        # run each state in batch through policy to get predicted logits for classifying action
        pred_pass = passNet(passingStates)
        # now compute loss by comparing what the policy thinks it should do with what the demonstrator didd
        loss = loss_function(pred_pass, passingActions)
        if i % 100 == 0:
            print("iteration", i, "bc loss", loss)
        # back propagate the error through the network to figure out how update it to prefer demonstrator actions
        loss.backward()
        # perform update on policy parameters
        passingOptimizer.step()

    torch.save(playNet, os.path.join("BCAgent", "playing.pt"))
    torch.save(passNet, os.path.join("BCAgent", "passing.pt"))

if __name__ == "__main__":
    main()
