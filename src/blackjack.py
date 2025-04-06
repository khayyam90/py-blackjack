import random

def generateAllCards():
    figures = ["A", 2,3,4,5,6,7,8,9,10, "J", "Q", "K"]
    colours = ["H", "D", "C", "S"]
    result = []

    # let's play with 6 games
    for i in range(6):
        for f in figures:
            for c in colours:
                result.append(str(f) + c)
            
    # let's shuffle the cards
    random.shuffle(result)    
    return result


def rateCards(cards, MAX_VALUE):
    cardsWithoutColours = [c[0:-1] for c in cards]
    cardsWithoutAces = [c for c in cardsWithoutColours if c != "A"]
    acesCount = len(cards) - len(cardsWithoutAces)

    result = 0
    for c in cardsWithoutAces:
        if (c in ["K", "Q", "J"]):
            result += 10
        else:
            result += int(c)

    result += acesCount

    if result > MAX_VALUE:
        return -1; # lost

    usedAces = 0
    while usedAces < acesCount and result + 10 <= MAX_VALUE:
        usedAces += 1
        result += 10

    return result

def chooseOneRandomCard(game):
    item = game.pop(0)
    return game, item

def isBlackjackCombination(cards, rate, MAX_VALUE):
    return len(cards) == 2 and rate == MAX_VALUE

def simulateOneGame(playerLimitForStay, MAX_VALUE):    
    game = generateAllCards()

    # first, 2 cards for the bank
    game, bank1 = chooseOneRandomCard(game)
    game, bank2 = chooseOneRandomCard(game)

    # then cards for the player as long as he wants a new card
    pointsPlayer = 0
    playerCards = []
    while pointsPlayer >= 0 and pointsPlayer < playerLimitForStay:
        game, card = chooseOneRandomCard(game)
        playerCards.append(card)
        pointsPlayer = rateCards(playerCards, MAX_VALUE)

    # did we lose ?
    if pointsPlayer > MAX_VALUE:
        # player loses
        return -1
    else:
        # now the bank will play
        bankCards = [bank1, bank2]
        pointsBank = rateCards(bankCards, MAX_VALUE)

        # the bank continues at 16 and stays at 17        
        while pointsBank >= 0 and pointsBank < 17:
            game, card = chooseOneRandomCard(game)
            bankCards.append(card)
            pointsBank = rateCards(bankCards, MAX_VALUE)
            
        if pointsBank > MAX_VALUE:
            # player wins
            if isBlackjackCombination(playerCards, pointsPlayer, MAX_VALUE):
                return 1.5
            else:
                return 1
        else:
            if pointsPlayer > pointsBank:
                if isBlackjackCombination(playerCards, pointsPlayer, MAX_VALUE):
                    return 1.5 # players wins with blackjack
                else:
                    return 1	# players wins without blackjack
            else:
                if pointsPlayer < pointsBank:
                    return -1	# players loses
                else:
                    # draw: player and bank have the same score
                            
                    # if the player has blackjack and the bank does not
                    if isBlackjackCombination(playerCards, pointsPlayer, MAX_VALUE) and not isBlackjackCombination(bankCards, pointsBank, MAX_VALUE):				
                        return 1.5
                        
                    # if the bank has blackjack and the player does not
                    if isBlackjackCombination(bankCards, pointsBank, MAX_VALUE) and not isBlackjackCombination(playerCards, pointsBank, MAX_VALUE):					
                        return -1
                            
                    # draw, player gets its money back
                    return 0