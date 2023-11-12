from agent import Agent
import random

class RandomAgent(Agent):
     def choose_action(self, state, possibleActionList):
        return  random.choice(possibleActionList)
     
     def pass_cards(self):
        cardList = []
        for i in range(3):
         nextCard = random.choice(self.hand)
         cardList.append(self.hand.pop(self.hand.index(nextCard)))
        return cardList