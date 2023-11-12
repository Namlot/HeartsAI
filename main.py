from random_agent import RandomAgent
from human_agent import HumanAgent
from game_engine import GameEngine

def main():

    gameEngine = GameEngine()
    agentList = [RandomAgent(gameEngine),RandomAgent(gameEngine),RandomAgent(gameEngine),RandomAgent(gameEngine)]
    gameEngine.set_agent_list(agentList)
    gameEngine.start_game()
    




if __name__ == "__main__":
    main()