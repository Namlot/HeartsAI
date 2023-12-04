from agent import Agent
import random


class RandomAgent(Agent):
    def choose_action(self, state, possibleActionList):
        return random.choice(possibleActionList)

    def pass_cards(self):
        return random.sample(self.hand, 3)

    def train_trick(self, trick_penalty):
        return # RandomAgent does not utilize training

    def train_round(self, round_penalty):
        return # RandomAgent does not utilize training

    def save(self, save_path):
        return # RandomAgent does not utilize training