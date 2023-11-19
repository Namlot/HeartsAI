from agent import Agent
import random


class RandomAgent(Agent):
    def choose_action(self, state, possibleActionList):
        return random.choice(possibleActionList)

    def pass_cards(self):
        cardList = []
        for i in range(3):
            nextCard = random.choice(self.hand)
            cardList.append(nextCard)
        return cardList

    def train_trick(self, trick_penalty):
        return # RandomAgent does not utilize training

    def train_round(self, round_penalty):
        return # RandomAgent does not utilize training

    def save(self, save_path):
        return # RandomAgent does not utilize training