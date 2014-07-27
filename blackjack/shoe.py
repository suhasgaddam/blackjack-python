#!/usr/bin/python
"""This module provides the :class:`shoe` object
"""

import blackjack.card as card
import random
import logging

#: a logger object
LOGGER = logging.getLogger(__name__)

class Shoe(object):
    """A Shoe object

    Contains :attr:`_number_of_decks` * (13 * 4) :class:`blackjack.card.Card`
    objects
    """

    #: an array of unused :class:`blackjack.card.Card` objects that are waiting
    #: to be dealt
    _cards = []

    #: an array of played :class:`blackjack.card.Card` objects
    _used_cards = []

    #: an array of :class:`blackjack.card.Card` objects that are currently
    #: being played on the :class:`blackjack.table.Table`
    _in_play_cards = []

    #: the number of sets of decks
    _number_of_decks = None

    def __init__(self, number_of_decks):
        """
        :param int number_of_decks: a number greater than 0 that represents the
            sets of decks that will be created
        :raises: ValueError
        """
        # check to make sure that number_of_decks is greater than 0
        # throw ValueError if input argument is bad
        if number_of_decks > 0:
            self._number_of_decks = number_of_decks
        else:
            raise ValueError("number_of_decks must be greater than 0 : %d"
                             % number_of_decks)

        # create a single set of cards (13*4) for _number_of_decks
        LOGGER.debug("Creating a new deck with %d sets of decks",
                     self._number_of_decks)

        self._cards = []
        self._used_cards = []
        self._in_play_cards = []

        # create a complete new deck for each self._number_of_decks
        for _ in range(self._number_of_decks):
            deck = []
            for suit in card.POSSIBLE_SUIT:
                for number in card.POSSIBLE_NUMBER:
                    deck.append(card.Card(number, suit))
            self._cards += deck

    def shuffle_shoe(self):
        """Shuffle the unused set of cards :attr:`_cards`

        .. todo:: Maybe use a different `random.shuffle`?
        """
        LOGGER.debug("Shuffling shoe")
        random.shuffle(self._cards)

    def is_valid_shoe(self):
        """Checks if there are enough cards to play the next round

        .. todo:: Why >= 30 cards? This should depend on the number of players
            at the table

        :returns: True if there are enough cards to play the next round
        :rtype: bool
        """
        LOGGER.debug("Number of cards left : %d", len(self._cards))
        return len(self._cards) >= 30

    def deal(self):
        """Deals a single :class:`blackjack.card.Card` from :attr:`_cards`

        :returns: a single :class:`blackjack.card.Card`
        :rtype: :class:`blackjack.card.Card`
        """
        LOGGER.debug("Number of cards left : %d", len(self._cards))

        # deal the last card from the unused _cards array
        deal_card = self._cards.pop()

        # add the newly dealt card to the _in_play_cards array
        self._in_play_cards.append(deal_card)

        LOGGER.debug("Dealing : %s", deal_card)
        return deal_card

    def burn(self, cards):
        """Remove `cards` from the :attr:`_in_play_cards` array and add them to
        :attr:`_used_cards` array

        :param array cards: an array of :class:`blackjack.card.Cards`
        """
        for burn_card in cards:
            LOGGER.debug("Burning %s", burn_card)
            self._in_play_cards.remove(burn_card)
            self._used_cards.append(burn_card)

    def check_shoe(self):
        """Check to make sure all the cards are accounted for

        .. todo:: Maybe an exception should be raised if cards go missing
        .. todo:: Should the missing cards be shown or listed?

        :returns: True if all cards are accounted for
        """

        # start with a simple card count check
        if self._number_of_decks*(13*4) != (len(self._cards)
                                            + len(self._in_play_cards)
                                            + len(self._used_cards)):
            return False

        return_value = True

        # go through all piles of cards and create a dictionary with
        # [suit][number] = number of occurrences of card
        card_dict = {}
        for pile in [self._cards, self._in_play_cards, self._used_cards]:
            for c_card in pile:
                if not c_card.get_suit() in card_dict:
                    card_dict[c_card.get_suit()] = {}
                if not c_card.get_number() in card_dict[c_card.get_suit()]:
                    card_dict[c_card.get_suit()][c_card.get_number()] = 1
                else:
                    card_dict[c_card.get_suit()][c_card.get_number()] += 1

        # go through generated card_dictionary to make sure that there are the
        # appropriate number of occurrences for each card
        for suit in card_dict.keys():
            for number in card_dict[suit].keys():
                if self._number_of_decks != card_dict[suit][number]:
                    #print "Missing: %s" % card.Card(number, suit)
                    return_value = False

        return return_value

