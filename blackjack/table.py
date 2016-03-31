#!/usr/bin/python
"""This module provides the :class:`Table`.
"""

import logging

#: a logger object
LOGGER = logging.getLogger(__name__)

import blackjack.player as player
import blackjack.dealer as dealer
import blackjack.shoe as shoe

class Table(object):
    """A Table object

    .. todo:: Handle player's bets and betting in general
    """

    def __init__(self, number_of_decks=5, bank_seed_money=10000,
                 number_of_players=5, dealer_name='Bob'):
        """
        .. todo:: Randomize player names
        .. todo:: Possibly create bank object?

        :param int number_of_decks: the sets of decks to initialize the
            :class:`blackjack.shoe.Shoe`
        :param int bank_seed_money: seed the table's bank
        :param int number_of_players: number of players at the table
        """

        #: Holds the amount of money the bank has
        self._bank = None

        #: Holds the :class:`blackjack.shoe.Shoe`
        self._shoe = None

        #: Holds the :class:`blackjack.dealer.Dealer`
        self._dealer = None

        #: Holds a list of all :class:`blackjack.player.Player` objects at the table
        self._players = None

        #: Does nothing for now
        self._playerBets = None

        self.reset()
        self._shoe = shoe.Shoe(number_of_decks)
        self._bank = bank_seed_money
        self._players = []
        self._dealer = dealer.Dealer(dealer_name, self)

        # dealer is also a player with strict rules/strategy
        # dealer is always dealt first
        self._players.append(self._dealer)
        # create players and add them to _players array
        for i in range(number_of_players):
            self._players.append(player.Player(i))

        self.start()

    def shuffle_shoe(self):
        """Shuffle the :class:`blackjack.shoe.Shoe`
        """
        self._shoe.shuffle_shoe()

    def is_valid_shoe(self):
        """Check if the shoe is valid

        .. todo:: This should depend on the number of players
        .. todo:: Maybe implement cutting the shoe/deck?

        :return: :meth:`blackjack.shoe.Shoe.is_valid_shoe`
        :return: bool
        """
        return self._shoe.is_valid_shoe()

    def deal(self):
        """Deal a card

        :return: :meth:`blackjack.shoe.Shoe.deal`
        :rtype: :class:`blackjack.card.Card`
        """
        return self._shoe.deal()

    def return_cards(self, cards):
        """Return played/used cards back to the :class:`blackjack.shoe.Shoe`

        :param array cards: an array of :class:`blackjack.card.Card`
        """
        self._shoe.burn(cards)

    def get_players(self):
        """Returns an array of all players at the table

        :returns: an array of all :class:`blackjack.player.Player` objects
        :rtype: array
        """
        return self._players

    def reset(self):
        """Reset the table's players

        .. todo:: Maybe reset the bank's money? And all other internal
            variables
        """
        self._players = []

    def start(self):
        """Starts the blackjack game by calling
        :meth:`blackjack.dealer.Dealer.start`
        """
        self._dealer.start()

