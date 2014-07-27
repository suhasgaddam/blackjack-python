#!/usr/bin/python
"""This module provides the :class:`Dealer` object.
"""

import logging

#: a logger object
LOGGER = logging.getLogger(__name__)

import blackjack.player as p

class Dealer(p.Player):
    """A Dealer object.

    Orchestrates the entire blackjack game
    """
    #: a reference to the :class:`blackjack.table.Table` that the dealer is
    #: sitting
    _table = None

    def __init__(self, name, table):
        """
        :param str name: a player's name
        :param table: the table of the :class:`Dealer`
        :type table: :class:`blackjack.table.Table`
        """
        super(Dealer, self).__init__(name)
        self._table = table

    def __repr__(self):
        """This method returns a string with the dealer's name

        .. todo:: Maybe include dealer's cards?

        :returns: human readable string with dealer's name
        :rtype: str
        """
        return "Dealer %s" % self._name

    def start(self):
        """The workhorse method. This method is called directly after the
        :class:`blackjack.table.Table` is initialized.

        This method gives the :class:`Dealer` control and allows
        :class:`Dealer` to go through the motions of a normal blackjack game.

        .. todo:: Parameterize this based on number of players(I think max 5
            cards per player)
        .. todo:: Create method to go through all players and reset/burn cards
        .. todo:: Some sort of betting strategy/engine
        .. todo:: Handle betting before dealing cards
        .. todo:: Handle not busting out but losing against dealer
        """
        self._table.shuffle_shoe()
        # check if there are enough cards to play a full round
        while self._table.is_valid_shoe():
            # iterate through all players and get old cards/clean all used
            # cards from table
            for current_player in self._table.get_players():
                self._table.return_cards(current_player.reset())
            # deal initial 2 cards
            for _ in range(2):
                for current_player in self._table.get_players():
                    current_player.add_card(self._table.deal())

            for current_player in self._table.get_players():
                while True:
                    status = current_player.action()
                    if p.STAY == status:
                        break
                    elif p.HIT == status:
                        current_player.add_card(self._table.deal())

                # check if player is a winner/loser
                if current_player.is_winner():
                    current_player.winner()
                if current_player.is_loser():
                    current_player.loser()

            # iterate through all players and get old cards/clean all used
            # cards from table
            for current_player in self._table.get_players():
                self._table.return_cards(current_player.reset())

