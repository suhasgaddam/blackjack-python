#!/usr/bin/python
"""This module provides the :class:`Card` object.
This module also has 3 constant attributes that help validate or string format
the :class:`Card` object: :attr:`POSSIBLE_SUIT`, :attr:`POSSIBLE_NUMBER`, and
:attr:`VALUE_TRANSLATION`
"""

#: an array with all the possible suit strings
POSSIBLE_SUIT = ['hearts', 'diamonds', 'spades', 'clubs']

#: an array with the range [1, 13]
POSSIBLE_NUMBER = range(1, 14, 1)

#: a dictionary which translates the special face cards to strings
VALUE_TRANSLATION = {
    1  : 'Ace',
    11 : 'Jack',
    12 : 'Queen',
    13 : 'King',
}

class Card(object):
    """A Card object
    """

    #: Holds an integer in the range [1, 13] which represents the card number
    _number = None

    #: Holds the suit as a lowercase string
    _suit = None

    def __init__(self, number, suit):
        """
        :param int number: a number between 1 and 13, inclusive
        :param str suit: a case-independent string in :attr:`POSSIBLE_SUIT`
        :raises: ValueError
        """
        # throw ValueError if input argument is bad
        base_error_str = 'A new Card cannot be created.'

        # check if number is within [1, 13]
        if number in POSSIBLE_NUMBER:
            self._number = number
        else:
            raise ValueError(base_error_str + " Number (%s) is not within"
                             " range." % number)

        # check if suit is allowed
        # ignore case if suit.lower() in POSSIBLE_SUIT:
        # throw ValueError if input argument is bad
        if suit.lower() in POSSIBLE_SUIT:
            self._suit = suit
        else:
            raise ValueError(base_error_str + " Suit ('%s') is not in"
                             " %s." % (suit, POSSIBLE_SUIT))

    def _translate_number(self):
        """This is a hidden method that changes the card number to a
        human-readable string

        'Ace' for 1

        :returns: human-readable string for face cards or card number
        :rtype: str
        """
        if self._number in VALUE_TRANSLATION:
            return VALUE_TRANSLATION[self._number]
        else:
            return self._number

    def __repr__(self):
        """This method returns a nice string representation of the card object

        useful in printing card object as "%s"

        :returns: human readable string represenation of card object
        :rtype: str
        """
        return "%s of %s" % (self._translate_number(), self._suit.title())

    def __str__(self):
        """
        :returns: :func:`__repr__`
        :rtype: str
        """
        return self.__repr__()

    def get_value(self):
        """ This method returns the blackjack value of card in an array
        format

        if Ace, return [1, 11]

        if face card, return [10]

        otherwise return [:attr:`_number`]

        :returns: blackjack value of card in an array
        :rtype: array
        """
        if 1 == self._number:
            return [1, 11]
        elif self._number > 10:
            return [10]
        else:
            return [self._number]

    def get_number(self):
        """This method returns the raw number

        :returns: :attr:`_number`
        :rtype: int
        """
        return self._number


    def get_suit(self):
        """This method returns the suit

        :returns: :attr:`_suit`
        :rtype: str
        """
        return self._suit

    def is_ace(self):
        """This method checks if card is an Ace

        :returns: True if card is an Ace
        :rtype: bool
        """
        return 1 == self._number

