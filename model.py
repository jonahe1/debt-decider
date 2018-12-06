import random

incomeUncert = 0.01
findJobUncert = 0.5
interestRate = 0.05
startingAge = 18 * 12
deathAge = 80 * 12
roundConst = -3

incomeRange = [10000 / 12, 500000 / 12]
maxTotalDebt = 1000000
maxNewDebt = 10000


def compound_interest_monthly(principal, rate, numMonths):
    return principal * (1 + (rate / 12))**numMonths


class Agent:
    def __init__(self):
        self.debt = 0
        self.income = int(round(random.randint(incomeRange[0], incomeRange[1]), roundConst))
        self.interest = interestRate
        self.isUnemployed = False
        self.ageInMonths = startingAge

    def get_state(self):
        return {
            'debt': self.debt,
            'income': self.income,
            'age': self.ageInMonths / 12,
            'employed': int(not self.isUnemployed),
        }

    def update_agent(self):
        self.debt = int(compound_interest_monthly(self.debt, self.interest, 1))
        self.ageInMonths += 1
        if not self.isUnemployed:
            self.debt -= self.income
            rand = random.random()
            if rand < incomeUncert:
                self.isUnemployed = True
        else:
            rand = random.random()
            if rand < findJobUncert:
                self.isUnemployed = False
        if self.is_bankrupt():
            return -1
        return 0

    def is_dead(self):
        return self.ageInMonths >= deathAge

    def random_action(self):
        return int(round(random.randint(0, maxNewDebt), roundConst))

    def take_on_debt(self, amount):
        if self.debt + amount > maxTotalDebt:
            return
        self.debt += amount

    def is_bankrupt(self):
        return (self.debt * self.interest) > (self.income)

    def reward(self, action):
        if self.debt + action > maxTotalDebt:
            return 0
        if self.is_bankrupt():
            return -99999999999
        elif self.is_dead():
            return 9999999999
        else:
            return action
