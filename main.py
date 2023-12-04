from random_agent import RandomAgent
from human_agent import HumanAgent
from rl_agent import RLAgent
from game_engine import GameEngine


def main():
    gameEngine = GameEngine(collect=True, savePath="human_data")
    agentList = [HumanAgent(gameEngine), RLAgent(gameEngine, "RLAgent1"), RLAgent(gameEngine, "RLAgent2"), RLAgent(gameEngine, "RLAgent3")]
    gameEngine.set_agent_list(agentList)
    gameEngine.start_game()


if __name__ == "__main__":
    main()
