from cards import Deck, hand_value, is_blackjack


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        if hide:
            dealer_cards = ["??"] + [
                f"{r}{s}" for r, s in dealer[1:]
            ]
        else:
            dealer_cards = [
                f"{r}{s}" for r, s in dealer
            ]

        print("Dealer:", " ".join(dealer_cards))
        print(
            "Player:",
            " ".join(f"{r}{s}" for r, s in player),
            "=",
            hand_value(player)
        )

    def get_wager(self):
        while True:
            print(f"Chips available: {self.chips}")

            try:
                wager = int(input("Enter your wager: ").strip())
            except ValueError:
                print("Invalid wager. Enter a whole number.")
                continue

            if wager <= 0:
                print("Wager must be greater than 0.")
                continue

            if wager > self.chips:
                print("You cannot wager more chips than you have.")
                continue

            return wager

    def settle(self, result, wager):
        if result == "win":
            self.chips += wager
            print(f"You win {wager} chips!")
        elif result == "blackjack":
            winnings = (wager * 3) // 2
            self.chips += winnings
            print(f"Blackjack! You win {winnings} chips!")
        elif result == "loss":
            self.chips -= wager
            print(f"You lose {wager} chips.")
        else:
            print("Push. Your wager is returned.")

        print(f"Chips: {self.chips}")

    def round(self):
        wager = self.get_wager()

        deck = Deck()

        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        print("\n--- New Round ---")

        self.show(player, dealer)

        # Check natural Blackjacks
        player_blackjack = is_blackjack(player)
        dealer_blackjack = is_blackjack(dealer)

        if player_blackjack or dealer_blackjack:
            self.show(player, dealer, hide=False)

            if player_blackjack and dealer_blackjack:
                print("Both have Blackjack.")
                self.settle("push", wager)

            elif player_blackjack:
                self.settle("blackjack", wager)

            else:
                print("Dealer has Blackjack.")
                self.settle("loss", wager)

            return True

        # Player's turn
        while True:
            player_value = hand_value(player)

            if player_value > 21:
                print("Player busts.")
                self.settle("loss", wager)
                return True

            if player_value == 21:
                print("Player has 21.")
                break

            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                print("Game ended.")
                return False

            elif key == "s":
                break

            elif key == "h":
                card = deck.draw()
                player.append(card)

                print(f"You drew: {card[0]}{card[1]}")
                self.show(player, dealer)

            else:
                print("Invalid command. Enter h, s, or q.")

        # Dealer's turn
        print("\nDealer's turn.")

        while hand_value(dealer) < 17:
            card = deck.draw()
            dealer.append(card)
            print(f"Dealer drew: {card[0]}{card[1]}")

        self.show(player, dealer, hide=False)

        player_value = hand_value(player)
        dealer_value = hand_value(dealer)

        # Dealer bust
        if dealer_value > 21:
            print("Dealer busts.")
            self.settle("win", wager)
            return True

        # Player wins
        if player_value > dealer_value:
            self.settle("win", wager)

        # Dealer wins
        elif player_value < dealer_value:
            self.settle("loss", wager)

        # Push
        else:
            self.settle("push", wager)

        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)

        while self.chips > 0:
            if not self.round():
                return

            if self.chips <= 0:
                print("You are out of chips.")
                return

            choice = input("\nPlay again? [y/n]: ").strip().lower()

            if choice == "n":
                print(f"Game over. Final chips: {self.chips}")
                return

            while choice != "y":
                print("Invalid command. Enter y or n.")
                choice = input("Play again? [y/n]: ").strip().lower()

        print("You are out of chips.")