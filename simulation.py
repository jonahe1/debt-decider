from model import Agent, deathAge, startingAge
import csv

with open('financial_lives.csv', 'wb') as f:
    w = csv.writer(f)

    for i in range(1000):
        agent = Agent()

        for n in range(deathAge - startingAge + 1):
            state = agent.get_state()
            if n is 0:
                w.writerow(state.keys())
                w.writerow(state.values())
            action = agent.random_action()
            reward = agent.reward(action)
            agent.take_on_debt(action)
            agent.update_agent()
            state.update({
                'action': action,
                'reward': reward
            })
            state = state
            w.writerow(state.values())
