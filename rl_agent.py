from agent import Agent
from typing import List
import random
import torch
from rl_networks import PlayingNetwork
from rl_networks import PassingNetwork
import os
import torch.nn as nn
import torch.nn.functional as F


class RLAgent(Agent):

    normalPlayingAgent: PlayingNetwork
    normalPassingAgent: PassingNetwork
    round_states: List[torch.tensor]
    round_rewards: List[int]
    passing_state: torch.tensor

    def __init__(self, gameEngine, loadPath = None):
        super().__init__(gameEngine)
        if loadPath is not None:
            self.normalPlayingAgent = torch.load(os.path.join(loadPath, "normalPlaying.pt"))
            self.normalPassingAgent = torch.load(os.path.join(loadPath, "normalPassing.pt"))
        else:
            self.normalPlayingAgent = PlayingNetwork()
            self.normalPassingAgent = PassingNetwork()

        if gameEngine.training:
            self.playingOptimizer = torch.optim.SGD(self.normalPlayingAgent.parameters(), lr=0.01, momentum=0.9)
            self.passingOptimizer = torch.optim.SGD(self.normalPassingAgent.parameters(), lr=0.01, momentum=0.9)
            self.round_rewards = []
            self.round_states = []

    def choose_action(self, state, possibleActionList):
        action_state = [card[1:] for card in state]
        best_cards = []
        best_reward = 0
        state_tensor = torch.tensor(action_state, dtype=torch.float).flatten()
        for card in possibleActionList:
            state_tensor[(card.get_numerical_value() - 2) * 5 + 2] = 1
            state_tensor[(card.get_numerical_value() - 2) * 5] = 0
            predicted_reward = self.normalPlayingAgent(state_tensor)
            state_tensor[(card.get_numerical_value() - 2) * 5 + 2] = 0
            state_tensor[(card.get_numerical_value() - 2) * 5] = 1
            if predicted_reward > best_reward:
                best_cards.clear()
                best_cards.append(card)
            elif predicted_reward == best_reward:
                best_cards.append(card)
        choice = random.choice(best_cards)
        if self.gameEngine.training:
            state_tensor[(choice.get_numerical_value() - 2) * 5 + 2] = 1
            state_tensor[(choice.get_numerical_value() - 2) * 5] = 0
            self.round_states.append(state_tensor.clone().detach())
        return choice

    def pass_cards(self):
        cardList = []
        game_state = self.determine_state()
        passing = [card[1:2] + [0] for card in game_state]
        best_sets = []
        best_reward = 0
        passing_tensor = torch.tensor(passing, dtype=torch.float).flatten()
        for i in range(13):
            for j in range(i+1, 13):
                for k in range(j+1, 13):
                    passing_tensor[(self.hand[i].get_numerical_value() - 2) * 2 + 1] = 1
                    passing_tensor[(self.hand[j].get_numerical_value() - 2) * 2 + 1] = 1
                    passing_tensor[(self.hand[k].get_numerical_value() - 2) * 2 + 1] = 1
                    predicted_reward = self.normalPassingAgent(passing_tensor)
                    passing_tensor[(self.hand[i].get_numerical_value() - 2) * 2 + 1] = 0
                    passing_tensor[(self.hand[j].get_numerical_value() - 2) * 2 + 1] = 0
                    passing_tensor[(self.hand[k].get_numerical_value() - 2) * 2 + 1] = 0
                    if predicted_reward > best_reward:
                        best_sets.clear()
                        best_sets.append([i, j, k])
                    elif predicted_reward == best_reward:
                        best_sets.append([i, j, k])
        choice = random.choice(best_sets)
        if self.gameEngine.training:
            passing_tensor[(self.hand[choice[0]].get_numerical_value() - 2) * 2 + 1] = 1
            passing_tensor[(self.hand[choice[1]].get_numerical_value() - 2) * 2 + 1] = 1
            passing_tensor[(self.hand[choice[2]].get_numerical_value() - 2) * 2 + 1] = 1
            self.passing_state = passing_tensor.clone().detach()

        for i in range(3):
            cardList.append(self.hand[choice[i]])
        return cardList

    def train_trick(self, trick_penalty):
        self.round_rewards.append(max(0,(4-trick_penalty)/8))
        return

    def train_round(self, round_penalty):
        if self.gameEngine.roundNumber == 0:
            return
        round_reward = max(0,(10-round_penalty)/10)
        self.round_rewards = [trick_reward + round_reward for trick_reward in self.round_rewards]
        for i in range(len(self.round_rewards)):
            self.playingOptimizer.zero_grad()
            play_reward = torch.tensor([self.round_rewards[i]], dtype=torch.float)
            play_state = self.round_states[i]
            predicted_play_reward = self.normalPlayingAgent(play_state)
            play_loss = F.mse_loss(predicted_play_reward, play_reward)
            play_loss.backward()
            self.playingOptimizer.step()
        self.round_rewards.clear()
        self.round_states.clear()

        self.passingOptimizer.zero_grad()
        pass_reward = torch.tensor([round_reward],dtype=torch.float)
        predicted_pass_reward = self.normalPassingAgent(self.passing_state)
        pass_loss = F.mse_loss(predicted_pass_reward, pass_reward)
        pass_loss.backward()
        self.passingOptimizer.step()

        return

    def save(self, save_path):
        torch.save(self.normalPlayingAgent, os.path.join(save_path, "normalPlaying.pt"))
        torch.save(self.normalPassingAgent, os.path.join(save_path, "normalPassing.pt"))
        return