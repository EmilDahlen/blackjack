import random


class deck:  # A class is collection of objects, data and functions. This class is a class that define what a deck of
    # cards is and what functions it can enact

    def create_deck(self):  # This function creates a list of 52 tuples that symbolize playing cards
        deck = list()
        card_number = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]  # From this row and two rows
        # down, we have three different characteristics that the cards hold
        card_value = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        card_suit = ["♡", "♤", "♢", "♧"]
        for i in card_suit:
            for o, number in enumerate(card_number):
                deck.append((number, i, card_value[o]))  # Appends "cards" to the list with three different values
        return deck  # Because this is a function, we have a return-value, if we didn't it would be called a method
        # We return the deck so upon calling the function, we retrieve the local variable "deck"

    def __init__(self):
        self.cards = deck.create_deck(self)

    def rotate_deck(self, shift):
        net_shift = abs(shift) % len(self.cards)
        for i in range(net_shift):
            if shift > 0:
                popped = self.cards.pop(len(self.cards) - 1)
                self.cards.insert(0, popped)
            if shift < 0:
                popped = self.cards.pop(0)
                self.cards.append(popped)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def pick_card(self, number_of_cards):
        active_card = []
        if number_of_cards != 0:
            for i in range(number_of_cards):
                active_card.append(self.cards[i])
            deck.rotate_deck(self, i + 1)
            return active_card


class player:

    def __init__(self, money, name):
        self.cards = []
        self.money = money
        self.is_dealer = False
        self.name = name

    def join_game(self, game):
        game.player_list.append(self)
        game.player_bets.append(0)

    def put_in_bet(self):
        while True:
            if self.money <= 0:
                return -1
            amount = int(input(self.name + " you have " + str(self.money) + "\nHow much do you want to bet: "))
            if amount <= self.money:
                self.money -= amount
                return amount
            else:
                print("You don't have enough money to bet: " + str(amount))

    def show_card(self, card_position):
        active_card = self.cards[card_position]
        print('┌───────┐')
        print(f'| {active_card[0][0]:<2}    |')
        print('|       |')
        print(f'|   {active_card[0][1]}   |')
        print('|       |')
        print(f'|    {active_card[0][0]:>2} |')
        print('└───────┘')

    def show_cards(self):
        card_visuals = list()
        for card in self.cards:
            card_visual = list()
            card_visual.append('┌───────┐')
            card_visual.append(f'| {card[0][0]:<2}    |')
            card_visual.append('|       |')
            card_visual.append(f'|   {card[0][1]}   |')
            card_visual.append('|       |')
            card_visual.append(f'|    {card[0][0]:>2} |')
            card_visual.append('└───────┘')

            card_visuals.append(card_visual)
        for i, _ in enumerate(card_visuals[0]):
            for j, visual in enumerate(card_visuals):
                print(visual[i], end=" ")
            print("")

    def hit(self, game):
        self.cards.append(game.deck.pick_card(1))

    def double(self, game, player_index):
        if game.player_bets[player_index] <= self.money:
            game.player_bets[player_index] = game.player_bets[player_index] * 2
            self.money -= game.player_bets[player_index]
            self.cards.append(game.deck.pick_card(1))
            return
        print("You don't have enough money to double!")

    def get_value(self, card):
        return card[0][2]

    def count_cards(self):
        card_count = 0
        card_order = self.cards
        card_order.sort(key=self.get_value)
        for i in card_order:
            if i[0][0] == "A" and card_count >= 11:
                card_count += 1
            else:
                card_count += i[0][2]
        return card_count


class game:

    def __init__(self):
        self.deck = deck()
        self.deck.shuffle_deck()
        self.player_list = []
        self.player_bets = []
        self.player_remove = []
        self.dealer = player(0, "Dealer")
        self.dealer.is_dealer = True

    def ask(self, player, player_index):
        bet = self.player_bets[player_index]
        while True:
            answer = input(
                player.name + " your current bet is " + str(bet) + ". Do you want to hit, double or stand: ").lower()
            if answer == "hit":
                player.hit(self)
                return False
            if answer == "double":
                player.double(self, player_index)
                return False
            if answer == "stand":
                return True
            else:
                print("You failed to enter any of the right terms")

    def start(self):
        for i, player in enumerate(self.player_list):
            bet = player.put_in_bet()
            if bet > 0:
                self.player_bets[i] = bet
            else:
                print(player.name + " has insignificant funds")
                self.player_remove.append(i)
        if len(self.player_remove) > 0:
            for i in self.player_remove:
                self.player_bets.pop(i)
                self.player_list.pop(i)
        if len(self.player_list) < 1:
            return
        self.dealer.hit(self)
        self.dealer.hit(self)
        for i in self.player_list:
            i.hit(self)
            i.hit(self)

    def round(self):
        if len(self.dealer.cards) == 0:
            return
        print("One of the dealers cards is:")
        self.dealer.show_card(1)
        for i, player in enumerate(self.player_list):
            while True:
                if player.count_cards() == 21:
                    print(str(player.name) + " your cards are:")
                    player.show_cards()
                    print("Your cards sum are: " + str(player.count_cards()))
                    break
                if player.count_cards() > 21:
                    print(str(player.name) + " your cards are:")
                    player.show_cards()
                    print("Your cards sum are: " + str(player.count_cards()))
                    print("You are BUST!")
                    break
                print(str(player.name) + " your cards are:")
                player.show_cards()
                print("Your cards sum are: " + str(player.count_cards()))
                if self.ask(player, i) == True:
                    break
        while True:
            if self.dealer.count_cards() < 17:
                self.dealer.hit(self)
            if self.dealer.count_cards() >= 17:
                break
        print("Dealers cards are:")
        self.dealer.show_cards()
        print("Dealers cards sum are: " + str(self.dealer.count_cards()))

    def winner(self):
        for i, player in enumerate(self.player_list):
            if player.count_cards() == self.dealer.count_cards() or player.count_cards() >= 22 and self.dealer.count_cards() >= 22:
                player.money += self.player_bets[i]
                print(str(player.name) + ": PUSH")
            elif self.dealer.count_cards() < player.count_cards() <= 21 or player.count_cards() <= 21 < self.dealer.count_cards():
                player.money += self.player_bets[i] * 2
                print(str(player.name) + ": WIN\nYou won: " + str(self.player_bets[i]))
            else:
                print(str(player.name) + ": LOSE\nYou lost: " + str(self.player_bets[i]))

    def play_game(self):
        self.start()
        self.round()
        self.winner()
        self.deck.shuffle_deck()
        self.dealer.cards = []
        rematch = []
        for i, player in enumerate(self.player_list):
            player.cards = []
            while True:
                ask_rematch = input(player.name + " do you want to play again? Yes or no\n").lower()
                if ask_rematch == "yes":
                    rematch.append(player)
                    break
                if ask_rematch == "no":
                    break
                print("You failed to enter any of the right terms. Enter yes or no")
        self.player_remove = []
        self.player_list = rematch
        self.play_game()


table_1 = game()
player1 = player(0, "Player1")
player2 = player(1000, "Player2")
player1.join_game(table_1)
player2.join_game(table_1)
table_1.play_game()