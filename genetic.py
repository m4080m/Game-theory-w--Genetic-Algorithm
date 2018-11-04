import numpy as np
import matplotlib.pyplot as plt

MAX_SIZE = 200
MAX_MONEY = 1000
K = 6.0
GENERATION = 800
PICK_COUNT = int((MAX_SIZE / 2))
MUTATION_PICK = int((MAX_SIZE / 3))
MUTATION_MAGNITUDE = 10

player1 = [np.random.randint(0, MAX_MONEY) for _ in range(MAX_SIZE)]
player2 = [np.random.choice([True, False]) for _ in range(MAX_SIZE)]

print(player1)
print(player2)

max_value = []
min_value = []
avg_value = []
true_count = []

def true_cnt():
    cnt = 0
    for item in player2:
        if item:
            cnt += 1
    return cnt

print(np.average(player1))
print(true_cnt() / MAX_SIZE)

for loop in range(GENERATION):
    player1_get = []; player2_get = []
    for i in range(MAX_SIZE):
        if player2[i] == False:
            player1_get.append(0)
            player2_get.append(0)
        else:
            player1_get.append(player1[i])
            player2_get.append(MAX_MONEY - player1[i])

    p1_bestPrice = max(player1_get)
    p1_worstPrice = min(player1_get)

    ##if(loop > 5 and abs(np.min(player1) - min_value[len(min_value) - 1]) > 100):
    ##    print(player1)
    ##    print(player2)
    max_value.append(np.max(player1))
    min_value.append(np.min(player1))
    avg_value.append(np.average(player1))
    true_count.append(true_cnt())

    if loop == GENERATION - 1:
        break

    def player1_FitnessFunction(price):
        if p1_bestPrice == p1_worstPrice:
            return K
        else:
            return 1.0 + (price - p1_worstPrice) * (K - 1) / (p1_bestPrice - p1_worstPrice)

    p1_sumOfFitness = 0
    for i in range(MAX_SIZE):
        p1_sumOfFitness += player1_FitnessFunction(player1_get[i])

    def player1_Pick():
        point = np.random.uniform(0, p1_sumOfFitness)
        sum = 0
        for i in range(MAX_SIZE):
            sum += player1_FitnessFunction(player1_get[i])
            if(point < sum):
                return i

    p1_pick = np.sort(player1_get)[MAX_SIZE - PICK_COUNT :]
    for i in range(MAX_SIZE):
        player1[i] = int(np.average(np.random.choice(p1_pick, np.random.randint(1, PICK_COUNT))))

    p2_bestPrice = max(player2_get)
    p2_worstPrice = min(player2_get)

    def player2_FitnessFunction(price):
        if p2_bestPrice == p2_worstPrice:
            return K
        else:
            return 1.0 + (price - p2_worstPrice) * (K - 1) / (p2_bestPrice - p2_worstPrice)

    p2_sumOfFitness = 0
    for i in range(MAX_SIZE):
        p2_sumOfFitness += player2_FitnessFunction(player2_get[i])

    def player2_Pick():
        point = np.random.uniform(0, p2_sumOfFitness)
        sum = 0
        for i in range(MAX_SIZE):
            sum += player2_FitnessFunction(player2_get[i])
            if(point < sum):
                return i

    p2_pick = []
    for i in range(MAX_SIZE):
        p2_pick.append(player2[player2_Pick()])
    player2 = p2_pick

    p2_pick = np.random.choice(MAX_SIZE, MUTATION_PICK, replace = False)
    for i in p2_pick:
        player2[i] = np.random.choice([True, False])

    #Mutation
    p1_pick = np.random.choice(MAX_SIZE, MUTATION_PICK, replace = False)
    for i in p1_pick:
        player1[i] += np.random.randint(-MUTATION_MAGNITUDE, MUTATION_MAGNITUDE)
        if player1[i] < 0:
            player1[i] = 0
        elif player1[i] > MAX_MONEY:
            player1[i] = MAX_MONEY

print(player1)
print(player2)

print(np.average(player1))
print(true_cnt() / MAX_SIZE)

plt.grid(True)
plt.xlim(1, GENERATION)
plt.ylim(0, MAX_MONEY)
#plt.plot(range(0, GENERATION), max_value, 'r')
#plt.plot(range(0, GENERATION), min_value, 'b')
plt.plot(range(0, GENERATION), avg_value, 'r')
plt.show()

plt.grid(True)
plt.xlim(1, GENERATION)
plt.ylim(0, MAX_SIZE)
#plt.plot(range(0, GENERATION), max_value, 'r')
#plt.plot(range(0, GENERATION), min_value, 'b')
plt.plot(range(0, GENERATION), true_count, 'b')
plt.show()
