from card import Card
from enum_suit import Suit
from typing import List
from agent import Agent
from human_agent import HumanAgent
import random


class GameEngine:
    deck: List[Card]
    agentList: List[Agent]
    currentTrickList: List[Card]
    turnPlayerIndex: int
    roundNumber: int
    heartsBroken: bool
    training: bool
    end: bool
    human: bool

    def __init__(self, train=False):
        self.currentTrickList = []
        self.deck = []
        self.agentList = []
        self.heartsBroken = False
        self.training = train
        self.end = False
        self.human = False

    def createDeck(self):
        for suit in Suit:
            for rank in range(2, 15):
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def set_agent_list(self, agentList):
        self.agentList = agentList
        for agent in agentList:
            if type(agent) is HumanAgent:
                self.human = True

    def deal(self):
        self.shuffle()
        playerIndex = 0
        while self.deck:
            cardToAdd: Card = self.deck.pop()
            cardToAdd.agent = self.agentList[playerIndex]
            self.agentList[playerIndex].hand.append(cardToAdd)
            playerIndex += 1
            if playerIndex > len(self.agentList) - 1:
                playerIndex = 0

    def start_game(self):
        self.roundNumber = 0
        while True:
            self.next_round()
            if self.end:
                break

    def first_turn(self):
        # 2 of clubs goes first
        for index, agent in enumerate(self.agentList):
            for card in agent.hand:
                if (card.suit == Suit.CLUB and card.value == 2):
                    self.turnPlayerIndex = index - 1
                    break
        self.next_turn()

    def next_turn(self):
        self.turnPlayerIndex += 1
        if (self.turnPlayerIndex > 3):
            self.turnPlayerIndex = 0

        currentAgent: Agent = self.agentList[self.turnPlayerIndex]
        cardSelected: Card = currentAgent.perform_action()
        self.currentTrickList.append(currentAgent.hand.pop(currentAgent.hand.index(cardSelected)))
        if len(self.currentTrickList) < 4:
            self.next_turn()
        else:
            self.trick_end()

    def trick_end(self):
        if any(card.suit == Suit.HEART for card in self.currentTrickList):
            self.heartsBroken = True

        winningCard = self.currentTrickList[0]
        for card in self.currentTrickList:
            if (card.suit == winningCard.suit and card.value > winningCard.value):
                winningCard = card

        self.turnPlayerIndex = self.agentList.index(winningCard.agent) - 1

        if self.human:
            currentTrickListString = ",".join(
                map(lambda card: card.suit.name + " " + str(card.value), self.currentTrickList))
            print("The stack was: " + currentTrickListString)
            print("Player", self.agentList.index(winningCard.agent), "won the stack with", winningCard.suit.name, str(winningCard.value))

        while self.currentTrickList:
            winningCard.agent.cardsWon.append(self.currentTrickList.pop())

        trick_penalty = self.score_trick()

        if self.training:
            for agent in self.agentList:
                if agent == winningCard.agent:
                    agent.train_trick(trick_penalty)
                else:
                    agent.train_trick(0)

        if len(self.agentList[0].hand) == 0:
            return
        else:
            self.next_turn()

    def pass_cards(self):
        # no passing every fourth round
        if self.roundNumber % 4 == 0:
            return

        cardsToPass: List[List[Card]] = []
        for agent in self.agentList:
            cardsToPass.append(agent.pass_cards())

        # pass right
        if self.roundNumber % 4 == 1:
            self.pass_cards_helper(cardsToPass[0], self.agentList[0], self.agentList[1])
            self.pass_cards_helper(cardsToPass[1], self.agentList[1], self.agentList[2])
            self.pass_cards_helper(cardsToPass[2], self.agentList[2], self.agentList[3])
            self.pass_cards_helper(cardsToPass[3], self.agentList[3], self.agentList[0])

        # pass left
        elif self.roundNumber % 4 == 2:
            self.pass_cards_helper(cardsToPass[0], self.agentList[0], self.agentList[3])
            self.pass_cards_helper(cardsToPass[1], self.agentList[1], self.agentList[0])
            self.pass_cards_helper(cardsToPass[2], self.agentList[2], self.agentList[1])
            self.pass_cards_helper(cardsToPass[3], self.agentList[3], self.agentList[2])

        # pass across
        elif self.roundNumber % 4 == 3:
            self.pass_cards_helper(cardsToPass[0], self.agentList[0], self.agentList[2])
            self.pass_cards_helper(cardsToPass[1], self.agentList[1], self.agentList[3])
            self.pass_cards_helper(cardsToPass[2], self.agentList[2], self.agentList[0])
            self.pass_cards_helper(cardsToPass[3], self.agentList[3], self.agentList[1])

    def pass_cards_helper(self, cardsToPass: List[Card],passingAgent: Agent, recievingAgent: Agent):
        for i in range(3):
            cardToPass = passingAgent.hand.pop(passingAgent.hand.index(cardsToPass[i]))
            cardToPass.agent = recievingAgent
            recievingAgent.hand.append(cardToPass)

    def scoring(self):
        for agent in self.agentList:
            agent.set_round_score()
            agent.cardsWon.clear()
        for agent in self.agentList:
            if agent.roundScore == 26:
                agent.roundScore = -26
                for agents in self.agentList:
                    agents.roundScore += 26
                break
        for agent in self.agentList:
            agent.score += agent.roundScore

    def score_trick(self):
        currentScore = 0
        for card in self.currentTrickList:
            if card.suit == Suit.HEART:
                currentScore += 1
            if card.suit == Suit.SPADE and card.value == 12:
                currentScore += 13
        return currentScore

    def next_round(self):
        self.heartsBroken = False
        self.createDeck()
        if self.roundNumber != 0:
            self.scoring()
            if self.human:
                self.print_final_scores()

        if self.training:
            for agent in self.agentList:
                agent.train_round(agent.roundScore)
            if self.roundNumber > 1000:
                print("finished playing")
                num = 0
                for agent in self.agentList:
                    agent.save("RLAgent"+str(num))
                    num += 1
                self.end = True
                return
            if self.roundNumber % 100 == 0:
                print("training round", self.roundNumber)

        else:
            for agent in self.agentList:
                if agent.score > 100:
                    print("finished playing")
                    self.print_final_scores()
                    self.end = True
                    return

        self.roundNumber += 1
        self.deal()
        self.pass_cards()
        self.first_turn()

    def print_final_scores(self):
        print("scores:")
        print("Agent 1: " + str(self.agentList[0].score))
        print("Agent 2: " + str(self.agentList[1].score))
        print("Agent 3: " + str(self.agentList[2].score))
        print("Agent 4: " + str(self.agentList[3].score))

    def dprint(self):
        for card in self.deck:
            print(card.suit.name + ":" + str(card.value))
