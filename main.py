from random_agent import RandomAgent
from human_agent import HumanAgent
from rl_agent import RLAgent
from game_engine import GameEngine


def main():
    gameEngine = GameEngine()
    agentList = [HumanAgent(gameEngine), RLAgent(gameEngine,"RLAgent0"), RLAgent(gameEngine,"RLAgent0"), RLAgent(gameEngine,"RLAgent0")]
    gameEngine.set_agent_list(agentList)
    gameEngine.start_game()


if __name__ == "__main__":
    main()
