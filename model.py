import random

incomeUncert = 0.01
findJobUncert = 0.5
interestRate = 0.05
startingAge = 18 * 12
deathAge = 80 * 12
roundConst = -3

balanceRange = [10000, 10000000]
debtRange = [2 * balanceRange[0], 2 * balanceRange[1]]
incomeRange = [20000 / 12, 2000000 / 12]


def compound_interest_monthly(principal, rate, numMonths):
    return principal * (1 + (rate / 12))**numMonths


class Agent:
    def __init__(self):
        self.balance = int(round(random.randint(balanceRange[0], balanceRange[1]), roundConst))
        self.debt = int(round(random.randint(debtRange[0], debtRange[1]), roundConst))
        self.income = int(round(random.randint(incomeRange[0], incomeRange[1]), roundConst))
        self.interest = interestRate
        self.isUnemployed = False
        self.ageInMonths = startingAge

    def get_state(self):
        return {
            'balance': self.balance,
            'debt': self.debt,
            'income': self.income,
            'age': self.ageInMonths / 12,
            'employed': not self.isUnemployed,
        }

    def update_agent(self):
        self.debt = compound_interest_monthly(self.debt, self.interest, 1)
        self.ageInMonths += 1
        if not self.isUnemployed:
            self.balance += self.income
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
        return int(round(random.randint(0, 300000), roundConst))

    def pay_off_debt(self, amount):
        if amount > self.balance:
            return
        self.debt -= amount
        self.balance -= amount

    def take_on_debt(self, amount):
        self.debt += amount

    def is_bankrupt(self):
        return (self.debt * self.interest) > (self.income + self.balance)

    def reward(self, action):
        new_debt = action['new_debt']
        debt_payment = action['debt_payment']
        if self.is_bankrupt():
            return -99999999999
        elif self.is_dead():
            return 9999999999
        else:
            return new_debt
