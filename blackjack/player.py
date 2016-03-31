#!/usr/bin/python
"""This module provides the :class:`Player` object.
This module also has 2 constants that represent player actions: :attr:`STAY`
and :attr:`HIT`.

.. todo:: Maybe use enumerations for player actions instead of constants?
"""

import logging

#: a logger object
LOGGER = logging.getLogger(__name__)

#: represents when a player stays
STAY = 'STAY'

#: represents when a player hits
HIT = 'HIT'

class Player(object):
    """A Player object
    """

    def __init__(self, name):
        """
        :param str name: a player's name
        """

        #: an array that contains all the :class:`blackjack.card.Card` in a
        #: :class:`Player` hand
        self._cards = None

        #: a string that contains the name of the :class:`Player`
        self._name = None

        #: an array that holds all the possible blackjack counts for the
        #: :class:`blackjack.card.Card` objects in :attr:`_cards`
        self._count = None

        # reset all the internal variables
        self.reset()
        self._name = name

    def __repr__(self):
        """This method returns a string with the player's name

        .. todo:: Maybe include players's cards?

        :returns: human readable string with player's name
        :rtype: str
        """
        return "Player %s" % self._name

    def __str__(self):
        """
        :returns: :func:`__repr__`
        :rtype: str
        """
        return self.__repr__()

    def action(self):
        """This method is called when it is the turn of the :class:`Player`

        The current basic strategy is hit if any count in :attr:`_count` is
        less than 15

        .. todo:: Refactor to include a 'real' strategy or at least the
            ability to 'plugin' strategy options

        :returns: an blackjack action which the
            :class:`blackjack.dealer.Dealer` will interpret
        :rtype: str
        """
        # if blackjack, STAY
        # if any count < 15, HIT
        # else STAY
        if self.is_blackjack():
            return STAY
        elif any((c < 15) for c in self._count):
            return HIT
        else:
            return STAY

    def add_card(self, card):
        """This method should only be called by the
        :class:`blackjack.dealer.Dealer`. Only the dealer can add cards to a
        :class:`Player`.

        When a card is added, the :attr:`_count` array is updated with
        :meth:`update_count` and :meth:`prune_count`

        :param card: the card to add to :attr:`_cards`
        :type card: :class:`blackjack.card.Card`
        """
        LOGGER.debug("Adding : %s", card)

        # add to cards in hand
        self._cards.append(card)

        LOGGER.debug("Current cards : %s", self._cards)

        # update the possible blackjack counts
        self.update_count()
        # remove any counts over 21
        self.prune_count()

    def update_count(self):
        """Update the :attr:`_count` array with the last card's value

        .. todo:: Add more code comments
        .. todo:: Possibly change the local variable name count
        """
        LOGGER.debug("Old Count : %s", self._count)
        # get last card added
        last_card = self._cards[-1]
        new_count = []
        for value in last_card.get_value():
            temp_count = list(self._count)
            for i, count in enumerate(temp_count):
                temp_count[i] = count + value
            new_count += temp_count

        self._count = new_count
        LOGGER.debug("New Count : %s", self._count)

    def prune_count(self):
        """Remove any counts that are greater than 21
        """
        LOGGER.debug("Old Count : %s", self._count)
        # keep counts that are less than or equal to 21
        self._count = [x for x in self._count if x <= 21]
        LOGGER.debug("New Count : %s", self._count)

    def is_blackjack(self):
        """Check if there is a blackjack.

        A blackjack is when there is an Ace and a face card.

        :returns: True if blackjack
        :rtype: bool
        """
        # check if there is an Ace and a card with value 10
        # order of cards in hand do no matter
        if 2 == len(self._cards):
            if self._cards[0].is_ace() or self._cards[1].is_ace():
                if ((10 == self._cards[0].get_value()[0]) or
                        (10 == self._cards[1].get_value()[0])):
                    LOGGER.debug("Blackjack! : %s", self._cards)
                    return True

        return False

    def is_winner(self):
        """This method checks if a count of 21 exists in :attr:`_count`

        :returns: True if a count of 21 exists
        :rtype: bool
        """
        return 21 in self._count

    def is_loser(self):
        """This method checks if there are 0 legal counts in :attr:`_count`

        :returns: True if there are 0 legal counts
        :rtype: bool
        """
        return 0 == len(self._count)

    def winner(self):
        """This method is only called when there is a winning count of 21. It
        is only called by the :class:`blackjack.dealer.Dealer`.
        """
        if self.is_winner():
            LOGGER.debug("Winner winner chicken dinner?! : %s", self._cards)
            self.is_blackjack()

    def loser(self):
        """This method is only called when there 0 legal counts. It is only
        called by the :class:`blackjack.dealer.Dealer`.
        """
        if self.is_loser():
            LOGGER.debug("Loser loser :(")

    def reset(self):
        """This method resets all the internal arrays

        The :class:`blackjack.card.Card` objects in hand are emptied and
        returned. The counts are zeroed out.

        :returns: all :class:`blackjack.card.Card` objects in hand
        :rtype: array of :class:`blackjack.card.Card` objects
        """
        used_cards = self._cards
        self._cards = []
        self._count = [0]
        return used_cards

