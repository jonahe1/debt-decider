from model import Agent, deathAge, startingAge
import csv

with open('financial_lives.csv', 'wb') as f:
    w = csv.writer(f)

    for a in range(1000):
        agent = Agent()

        for n in range(deathAge - startingAge + 1):
            state = agent.get_state()
            action = agent.random_action()
            reward = agent.reward(action)
            agent.take_on_debt(action)
            state.update({
                'action': action,
                'reward': reward
            })
            if a is 0 and n is 0:
                w.writerow(state.keys())
            agent.update_agent()
            w.writerow(state.values())
