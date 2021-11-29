import random
import os


    ###############################################################################################################################
    ### This program is simulation of blackjack with features such as creating and loading game-files, this is done with a specialized dump- and load method ##
    ### This program uses object oriented programming, that will say, using classes and objects                                                                                                   ##
    ### Video on object oriented programming in python: https://www.youtube.com/watch?v=ZDa-Z5JzLYM                                                                                 ##
    ##############################################################################################################################




def str_to_bool(string):
    # converts strings to booleans
    if string == "True":
        return True
    if string == "False":
        return False
    else:
        print("str_to_bool *ERROR*")

def tuple_to_str(tuple):
    # converts tuple to string
    string = str(tuple)
    string = string.replace("(", "")
    string = string.replace(")", "")
    return string

def str_to_tuple(string):
    # converts string to tuple
    return tuple(map(func, string.split(', ')))

def func(string):
    # tries if string can be converted to an integer, otherwise remove comma
    try:
        return int(string)
    except ValueError:
        return string.replace("'", "")
    
    #########################################################
    ### A class defines objects with atributes, functions and methods  ##
    ########################################################
    
class deck:
    # deck class, stores 52 tuples representing cards, also creates the tuples, aswell as shuffles the list, and can deal a card

    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        # creates a list of 52 tuples that represent playing cards
        deck = list()
        card_number = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        card_value = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        card_suit = ["♡", "♤", "♢", "♧"]
        for suit in card_suit:
            for value, number in zip(card_value, card_number):
                # "zip" unpacks two list in a for loop
                deck.append((number, suit, value)) 
        return deck 

    def rotate_deck(self, shift):
        # rotates the cards list n steps
        net_shift = abs(shift) % len(self.cards)
        # if shifts > the list we we take the rest of a divition between the values
        for _ in range(net_shift):
            if shift > 0:
                popped = self.cards.pop(len(self.cards) - 1)
                self.cards.insert(0, popped)
            if shift < 0:
                popped = self.cards.pop(0)
                self.cards.append(popped)

    def shuffle_deck(self):
        # shuffles cards list
        random.shuffle(self.cards)

    def pick_card(self, hand):
        # appends one card for cards list to the argument list called hand, which is intended to be a player hand
        hand.append(self.cards[0])
        deck.rotate_deck(self, 1)

class player:    
    # player class, has atributes that keep track of its name, cards, money and position in game sequence
    
    def __init__(self, money, name):
        self.name = name
        self.cards = []
        self.money = money
        
        # atributes below are to keep track of position in game sequence
        self.is_dealer = False
        self.has_betted = False
        self.has_had_round = False
        self.has_got_dealt = False
        self.game_done = False

    def join_game(self, game):
        # appends self (object) to game atribute player_list, this is so game objects can acess all player objects
        game.player_list.append(self)
        game.player_bets.append(0)

    def put_in_bet(self):
        # askes player how much they want to bet, if it is more than their balance it askes again and also if the amount can't be converted to an integer
        while True:
            if self.money <= 0:
                return -1
            while True:
                amount = (input(self.name + " you have " + str(self.money) + "\nHow much do you want to bet: "))
                try:
                    amount = int(amount)
                    break
                except:
                    print("*Enter an Integer*")
            if amount <= self.money:
                self.money -= amount
                return amount
            print("You don't have enough money to bet: " + str(amount))

    def show_card(self, card_position):
        # prints a card with "number" and "suit"
        active_card = self.cards[card_position]
        print('┌───────┐')
        print(f'| {active_card[0]:<2}    |')
        print('|       |')
        print(f'|   {active_card[1]}   |')
        print('|       |')
        print(f'|    {active_card[0]:>2} |')
        print('└───────┘')

    def show_cards(self):
        # prints all cards in a list by appending each card to a list then appending all those lists to another list, then printing the cards on the correct row
        card_visuals = list()
        for card in self.cards:
            card_visual = list()
            card_visual.append('┌───────┐')
            card_visual.append(f'| {card[0]:<2}    |')
            card_visual.append('|       |')
            card_visual.append(f'|   {card[1]}   |')
            card_visual.append('|       |')
            card_visual.append(f'|    {card[0]:>2} |')
            card_visual.append('└───────┘')

            card_visuals.append(card_visual)
        for i, _ in enumerate(card_visuals[0]):
            for j, visual in enumerate(card_visuals):
                print(visual[i], end=" ")
            print("")

    def hit(self, game):
        # deals a card
        game.deck.pick_card(self.cards)

    def double(self, game, player_index):
        # tries to double bet amount, if succesful, it deals another card aswell, if not ot prints that you dont have enough money to double
        if game.player_bets[player_index] <= self.money:
            game.player_bets[player_index] = game.player_bets[player_index] * 2
            self.money -= game.player_bets[player_index]
            self.cards.append(game.deck.pick_card(1))
            return True
        print("You don't have enough money to double!")
        return False

    def get_value(self, card):
        # gets value for card-tuple
        return card[2]

    def count_cards(self):
        # counts all cards in a cards list and arranges all aces as the optimal value
        card_value = int()
        ace_count = int()
        card_order = self.cards
        card_order.sort(key=self.get_value)
        for i in card_order:
            if i[0] == "A":
                ace_count += 1
            else:
                card_value += i[2]
        for i in range(ace_count):
            # checks all possible ace-value arrangements till it's below 21
            if card_value + ((ace_count - i) *11) + i > 21:
                pass
            else:
                card_value += ((ace_count-i)*11)+i
        return card_value

class game:
    # class game, has atributes such as player_list, player_bets and a dealer-player object
    fileDir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, name):
        if name != "":
            self.load(name)
            return
        while True:
            self.name = input("Enter game name: ")
            if "." in self.name:
                print("Enter a name that doesn't contain a \".\"")
                pass
            if "/" in self.name:
                print("Enter a name that doesn't contain a \"/\"")
                pass
            else:
                break
        self.file_name = os.path.join(self.fileDir, "Saves", self.name)
        self.file = open(self.file_name, "w+", encoding = "utf-8")
        self.deck = deck()
        self.deck.shuffle_deck()
        self.player_list = []
        self.player_bets = []
        self.player_remove = []
        self.dealer = player(0, "Dealer")
        self.dealer.is_dealer = True
        while True:
            ask_for_player = input("Enter \"add player\" or \"start game\": ").lower()
            if ask_for_player == "add player":
                self.add_player_m()
            if ask_for_player == "start game":
                self.play_game()
                break

    def load(self, name):
        self.name = name
        self.file_name = os.path.join(self.fileDir, "Saves", self.name)
        self.file = open(self.file_name, "r+", encoding="utf-8")
        self.deck = deck()
        self.deck.shuffle_deck()
        self.player_list = []
        self.player_bets = []
        self.player_remove = []
        self.dealer = player(0, "Dealer")
        self.dealer.is_dealer = True
        self.load_game()

    def load_game(self):
        player_save = self.file.read().split("\n")
        for player in player_save:
            player_data = player.split(";")
            player_name = player_data[0]
            player_money = int(player_data[1])
            self.add_player_a(player_money, player_name)
        for i, player in enumerate(self.player_list):
            data_list = player_save[i]
            player_data = data_list.split(";")
            player.has_betted = str_to_bool(player_data[2])
            player.has_had_round = str_to_bool(player_data[3])
            player.has_got_dealt = str_to_bool(player_data[4])
            player.game_done = str_to_bool(player_data[5])
            self.player_bets[i] = int(player_data[-1])
            for i in range(len(player_data) - 7):
                player.cards.append(str_to_tuple(player_data[i + 6]))

        
        self.play_game()

    def write_player(self, player, i):
        self.file.write(
            player.name + ";" + 
            str(player.money) + ";" + 
            str(player.has_betted) +  ";" + 
            str(player.has_had_round) + ";" + 
            str(player.has_got_dealt)+ ";" + 
            str(player.game_done))
        for card in player.cards:
            self.file.write(";" + tuple_to_str(card))
        if len(self.player_bets) > 0:
            self.file.write(";" + str(self.player_bets[i]))
        else:  
            self.file.write(";" + 0)

    def write_state(self):
        self.file.truncate(0)
        self.file.seek(0)
        self.write_player(self.dealer, 0)
        for i, player in enumerate(self.player_list):
            self.file.write("\n")
            self.write_player(player, i)

    def add_player_a(self, money, name):
        player(money, name).join_game(self)


    def add_player_m(self):
        while True:
            player_name = input("Enter player name: ")
            if ";" in player_name:
                print("Enter a name that doesn't contain a \";\"")
            else:
                break
        while True:
                player_money = input("Enter player balance: ")
                try:
                    player_money = int(player_money)
                    break
                except:
                    print("*Enter an Integer*")
        player(player_money,  player_name).join_game(self)
        print("Player \"" + player_name + "\" was added to game \"" + self.name + "\" and has a balance of: " +str(player_money))

    def ask(self, player, player_index):
        bet = self.player_bets[player_index]
        while True:
            answer = input(player.name + " your current bet is " + str(bet) + ". Do you want to hit, double or stand: ").lower()
            if answer == "hit":
                player.hit(self)
                return False
            if answer == "double":
                availability = player.double(self, player_index)
                if not availability:
                    pass
                return False
            if answer == "stand":
                return True
            else:
                print("You failed to enter any of the right terms")

    def start(self):
        for i, player in enumerate(self.player_list):
            if player.has_betted == True:
                break
            bet = player.put_in_bet()
            if bet > 0:
                self.player_bets[i] = bet
            else:
                print(player.name + " has insignificant funds")
                self.player_remove.append(i)
            player.has_betted = True
            self.write_state()
        if len(self.player_remove) > 0:
            for i in self.player_remove:
                self.player_bets.pop(i)
                self.player_list.pop(i)
        if len(self.player_list) < 1:
            return
        if self.dealer.has_got_dealt == False:
            self.dealer.hit(self)
            self.dealer.hit(self)
            self.dealer.has_got_dealt = True
        self.write_state()
        for player in self.player_list:
            if player.has_got_dealt == False:
                player.hit(self)
                player.hit(self)
                player.has_got_dealt = True
            self.write_state()

    def round(self):
        if len(self.dealer.cards) == 0:
            return
        print("One of the dealers cards is:")
        self.dealer.show_card(1)
        for i, player in enumerate(self.player_list):
            if player.has_had_round == False:
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
                player.has_had_round = True
            self.write_state()
        if self.dealer.has_had_round == False:
            while True:
                if self.dealer.count_cards() < 17:
                    self.dealer.hit(self)
                if self.dealer.count_cards() >= 17:
                    break
            self.dealer.has_had_round = True
        self.write_state()
        print("Dealers cards are:")
        self.dealer.show_cards()
        print("Dealers cards sum are: " + str(self.dealer.count_cards()))

    def winner(self):
        for i, player in enumerate(self.player_list):
            if self.dealer.game_done == False:
                if player.count_cards() == self.dealer.count_cards() or player.count_cards() >= 22 and self.dealer.count_cards() >= 22:
                    player.money += self.player_bets[i]
                    print(str(player.name) + ": PUSH")
                elif self.dealer.count_cards() < player.count_cards() <= 21 or player.count_cards() <= 21 < self.dealer.count_cards():
                    player.money += self.player_bets[i] * 2
                    print(str(player.name) + ": WIN\nYou won: " + str(self.player_bets[i]))
                else:
                    print(str(player.name) + ": LOSE\nYou lost: " + str(self.player_bets[i]))
            self.write_state()
        

    def play_game(self):
        self.start()
        self.round()
        self.winner()
        rematch = []
        for player in self.player_list:
            while True:
                if player.money <= 0:
                    break
                ask_rematch = input(player.name + " do you want to play again? Yes or No\n").lower()
                if ask_rematch == "yes":
                    rematch.append(player)
                    break
                if ask_rematch == "no":
                    break
                print("You failed to enter any of the right terms")
        for player in self.player_list:
            player.cards = []
            player.has_betted = False
            player.has_had_round = False
            player.has_got_dealt = False
            player.game_done = False
            self.write_state()
        self.dealer.has_betted = False
        self.dealer.has_had_round = False
        self.dealer.has_got_dealt = False
        self.dealer.game_done = False
        self.file.truncate(0)
        self.file.seek(0)
        self.deck.shuffle_deck()
        self.dealer.cards = []
        self.player_remove = []
        self.write_state()
        self.player_list = rematch
        if len(self.player_list) > 0:
            self.play_game()
        else:
            return


while True:
    file_manage = input("Enter Load or Create: ").lower()
    if file_manage == "load":
        game_name = input("Enter the name of the save file: ")
        game(game_name)
        break
    if file_manage == "create":
        game("")
        break
    print("You failed to enter any of the right terms")
