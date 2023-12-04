from agent import Agent
from typing import List
import random
import torch
from bc_network import BCPlayingNetwork
from bc_network import BCPassingNetwork
import os
import torch.nn as nn
import torch.nn.functional as F


class BCAgent(Agent):

    playingAgent: BCPlayingNetwork
    passingAgent: BCPassingNetwork
    round_states: List[torch.tensor]
    round_rewards: List[int]
    passing_state: torch.tensor

    def __init__(self, gameEngine, loadPath = None):
        super().__init__(gameEngine)
        if loadPath is not None:
            self.playingAgent = torch.load(os.path.join(loadPath, "Playing.pt"))
            self.passingAgent = torch.load(os.path.join(loadPath, "Passing.pt"))
        else:
            self.playingAgent = BCPlayingNetwork()
            self.passingAgent = BCPassingNetwork()

    def choose_action(self, state, possibleActionList):
        action_state = [card[1:] for card in state]
        state_tensor = torch.tensor(action_state, dtype=torch.float).flatten()
        probabilities = self.playingAgent(state_tensor)
        sorted_probs, indices = torch.sort(probabilities)
        hand_values = [card.get_numerical_value() for card in possibleActionList]
        for index in indices:
            if index+2 in hand_values:
                return possibleActionList[hand_values.index(index+2)]

    def pass_cards(self):
        cardList = []
        game_state = self.determine_state()
        passing = [card[1:2] + [0] for card in game_state]
        best_sets = []
        best_reward = 0
        passing_tensor = torch.tensor(passing, dtype=torch.float).flatten()
        probabilities = self.passingAgent(passing_tensor)
        sorted_probs, indices = torch.sort(probabilities)
        hand_values = [card.get_numerical_value() for card in self.hand]
        for index in indices:
            if index + 2 in hand_values:
                cardList.append(self.hand[hand_values.index(index + 2)])
                if len(cardList) == 3:
                    break
        return cardList

    def train_trick(self, trick_penalty):
        return # BC trains offline

    def train_round(self, round_penalty):
        return # BC trains offline

    def save(self, save_path):
        return # BC trains offline
