import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deckStr = ""
        for card in self.deck:
            deckStr = deckStr + str(card) + "\n"
        return deckStr

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total = self.total + self.bet

    def lose_bet(self):
        self.total = self.total - self.bet


class Player:

    def __init__(self):
        self.hand = Hand()
        self.chips = Chips()

    def refresh(self):
        self.hand = Hand()

    def take_bet(self):
        invalidBet = True
        while invalidBet:
            try:
                betAsk = int(input('\nEnter your bet: '))
                if self.chips.total < betAsk:
                    print(
                        f'You dont have the funds! Enter below {self.chips.total}')
                else:
                    self.chips.bet = betAsk
                    invalidBet = False
            except:
                print('Thats not a number!')


def hit(deck, hand):
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while playing:
        choice = input('\nDo you want to hit or stand? h or s: ')
        if 'h' == choice:
            hit(deck, hand)
            print(f'\nPlayer value: {hand.value}')
        elif 's' == choice:
            playing = False
        else:
            print('Invalid choice, try again')


def show_some(player, dealer):
    print('\nDealer cards:\n<card hidden>')
    print(dealer.hand.cards[1])
    print('\nPlayer cards:')
    print(*player.hand.cards, sep='\n')
    print(f'\nPlayer value: {player.hand.value}')


def show_all(player, dealer):
    print('\nDealer cards:')
    print(*dealer.hand.cards, sep='\n')
    print(f'\nDealer value: {dealer.hand.value}')
    print('\nPlayer cards:')
    print(*player.hand.cards, sep='\n')
    print(f'\nPlayer value: {player.hand.value}')


def player_busts(player, dealer):
    player.chips.lose_bet()
    print('\nPlayer busts!\n')


def player_wins(player, dealer):
    player.chips.win_bet()
    print('\nPlayer wins!\n')


def dealer_busts(player, dealer):
    player.chips.win_bet()
    print('\nDealer busts!\n')


def dealer_wins(player, dealer):
    player.chips.lose_bet()
    print('\nDealer wins!\n')


def push():
    print('Its a push! No one wins')


# Print an opening statement
print('\nWelcome to Blackjack!\n')

player = Player()
dealer = Player()

while True:

    # Create & shuffle the deck, deal two cards to each player

    deck = Deck()
    deck.shuffle()

    player.refresh()
    dealer.refresh()

    hit(deck, dealer.hand)
    hit(deck, dealer.hand)
    hit(deck, player.hand)
    hit(deck, player.hand)

    # Prompt the Player for their bet

    player.take_bet()

    # Show cards (but keep one dealer card hidden)

    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player.hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

    # If player's hand exceeds 21, run player_busts() and break out of loop
    if player.hand.value > 21:
        player_busts(player, dealer)
        # Show all cards
        show_all(player, dealer)

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.hand.value <= 21:
        while dealer.hand.value < 17:
            hit(deck, dealer.hand)

        # Show all cards
        show_all(player, dealer)

        # Run different winning scenarios
        if dealer.hand.value > 21:
            dealer_busts(player, dealer)

        elif dealer.hand.value > player.hand.value:
            dealer_wins(player, dealer)

        elif player.hand.value > dealer.hand.value:
            player_wins(player, dealer)

        else:
            push()

    # Inform Player of their chips total

    print(f'\nPlayer winnings: {player.chips.total}')

    if player.chips.total > 0:
        # Ask to play again
        new_game = input(
            "\nWould you like to play another hand? Enter 'y' or 'n' ")

        if new_game[0].lower() == 'y':
            playing = True

    if not playing:
        print("\nThanks for playing!")
        break
