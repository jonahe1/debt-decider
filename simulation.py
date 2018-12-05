from model import Agent, deathAge, startingAge
import csv

with open('financial_lives.csv', 'wb') as f:
    w = csv.writer(f)

    agents = []
    for i in range(1000):
        agents.append(Agent())

    for n in range(deathAge - startingAge + 1):
        new_debt_actions = [agent.random_action() for agent in agents]
        debt_payment_actions = [agent.random_action() for agent in agents]
        states = [agent.get_state() for agent in agents]
        rewards = [agent.reward({'new_debt': a[0], 'debt_payment': a[1]}) for a in zip(new_debt_actions, debt_payment_actions)]
        for j, agent in enumerate(agents):
            agent.take_on_debt(new_debt_actions[j])
            agent.pay_off_debt(debt_payment_actions[j])
            agent.update_agent()
        for i, state in enumerate(states):
            state.update({
                'new_debt': new_debt_actions[i],
                'debt_payment': debt_payment_actions[i],
                'reward': rewards[i]
            })
            states[i] = state
        if n is 0:
            w.writerow(states[0].keys())
        for state in states:
            w.writerow(state.values())
