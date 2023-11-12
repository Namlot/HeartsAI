from agent import Agent

class HumanAgent(Agent):
     def choose_action(self, state, possibleActionList):
        print("It's the next human agents turn")
        currentTrickListString = ",".join(map(lambda card: card.suit.name + " " + str(card.value), self.gameEngine.currentTrickList))
        print("currently on the stack is: " + currentTrickListString)
        handString = ",".join(map(lambda card: card.suit.name + " " + str(card.value), self.hand))

        print("your hand is: "  + handString)
        print()
        print("Possible actions are: ")
        for index, card in enumerate(possibleActionList):
            print(str(index) + ": " + card.suit.name + "  " + str(card.value))
      
        user_input = input("Enter a number:")
        while(not user_input.isdigit() or int(user_input) < 0 or int(user_input) > len(possibleActionList) - 1):
            print("Please try again:")
            user_input = input("Enter a number:")
        print()
        print()
        return  possibleActionList[int(user_input)]
     

     def pass_cards(self):
        cardList = []
        print("It's the next human agents turn to pass cards")
        for i in range(3):
            for index, card in enumerate(self.hand):
                  print(str(index) + ": " + card.suit.name + "  " + str(card.value))
            user_input = input("Select a card: ")
            while(not user_input.isdigit() or int(user_input) < 0 or int(user_input) > len(self.hand) - 1):
                  user_input = input("ERROR TRY AGAIN, Enter a number:")
            cardList.append(self.hand.pop(int(user_input)))
            print()
            print()
        return cardList