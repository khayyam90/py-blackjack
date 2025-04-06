
from matplotlib import pyplot as plt
from blackjack import generateAllCards, simulateOneGame

MAX_VALUE = 21


# plot
fig, ax = plt.subplots()

nbEpochs = 100000

for n in range(13, 20):
    evolution = list()
    result = 0
    for i in range(nbEpochs):
        cards = generateAllCards()
        result += simulateOneGame(n, MAX_VALUE)
        evolution.append(result)

    ax.plot(range(nbEpochs), evolution, label=n)

plt.legend(loc="lower left")
plt.xlabel("Epochs")
plt.ylabel("Earnings")
plt.title("Earnings based on STAY strategy");

plt.show()