from abc import ABC, abstractmethod
from card import Card
from typing import List
from enum_suit import Suit

class Agent(ABC):
    hand: List[Card]
    cardsWon: List[Card]
    score : int
    roundScore: int

    def __init__(self, gameEngine: "GameEngine"):
        self.hand = []
        self.cardsWon = []
        self.gameEngine = gameEngine
        self.score = 0
        self.roundScore = 0
    
    def set_round_score(self):
        currentScore : int  = 0
        for card in self.cardsWon:
            if card.suit == Suit.HEART:
                currentScore += 1
            if card.suit == Suit.SPADE and card.value == 12:
                currentScore += 13
        self.roundScore = currentScore

    
    
    def perform_action(self) -> Card:
        state = self.determine_state()
        possibleActionList = self.determine_possible_actions()
        # print("It's my turn")
        # if len(self.gameEngine.currentTrickList) > 0:
        #     print("leading card is: " + str(self.gameEngine.currentTrickList[0].suit) + " "  + str(self.gameEngine.currentTrickList[0].value))
        # print("heartsBroken = " + str(self.gameEngine.heartsBroken))
        # print("my hand")
        # for card in self.hand:
        #     print(str(card.suit) + str(card.value))
        # print("my possible actions")
        # for card in possibleActionList:
        #     print(str(card.suit) + str(card.value))
        return self.choose_action(state,possibleActionList)

    def determine_state(self):

        stateArray : List[List[int]] = []

        #in my hand
        for card in self.hand:
            stateArray.append([card.get_numerical_value(),1,0,0,0])

        #in someone elses hand
        for agent in self.gameEngine.agentList:
            if(agent != self):
                for card in agent.hand:
                    stateArray.append([card.get_numerical_value(),0,1,0,0])

        #currently in play
        for card in self.gameEngine.currentTrickList:
            stateArray.append([card.get_numerical_value(),0,0,1,0])

        #already played
        for agent in self.gameEngine.agentList:
            if(agent != self):
                for card in agent.cardsWon:
                    stateArray.append([card.get_numerical_value(),0,0,0,1])

        stateArray = sorted(stateArray, key=lambda entry: entry[0])

        return stateArray
    
    def determine_possible_actions(self):


        #if you have the two of clubs you must play it        
        possibleActionList = list(filter(lambda card: card.suit == Suit.CLUB and card.value == 2, self.hand))
        if len(possibleActionList) > 0:
            return possibleActionList
        
        #you must match the leading card if possible
        if len(self.gameEngine.currentTrickList) > 0:
            leadingSuit : Suit = self.gameEngine.currentTrickList[0].suit
            possibleActionList = list(filter(lambda card: card.suit == leadingSuit, self.hand))
            if len(possibleActionList) > 0:
               return possibleActionList

        #then you may play any card unless hearts suit is not yet broken and you are first
        if len(self.gameEngine.currentTrickList) == 0 and not self.gameEngine.heartsBroken:
            possibleActionList = list(filter(lambda card: card.suit != Suit.HEART, self.hand))
            if len(possibleActionList) > 0:
               return possibleActionList
            
        #then you may play any card
        return self.hand

    def dprint(self):
        print("Agent")
        for card in self.hand:
            print(str(card.value) + ":" + card.suit.name)

    @abstractmethod
    def choose_action(self, state, possibleActionList) -> Card:
        pass

    @abstractmethod
    def pass_cards(self) -> List[Card]:
        pass
    
