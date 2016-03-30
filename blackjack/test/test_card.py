#!/usr/bin/python

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))

import pytest
import blackjack.card as card

import random
import string

def test_functional():
    for suit in ('hearts', 'diamonds', 'spades', 'clubs'):
        for number in xrange(1, 14):
            newCard = card.Card(number, suit);

            if (1 == number):
                assert (newCard.is_ace())
                value = [1, 11]
                numberString = 'Ace'
            elif (number > 10):
                assert (False == newCard.is_ace())
                value = [10]
                if (11 == number):
                    numberString = 'Jack'
                elif (12 == number):
                    numberString = 'Queen'
                elif (13 == number):
                    numberString = 'King'
            else:
                assert (False == newCard.is_ace())
                value = [number]
                numberString = number

            assert (value == newCard.get_value())
            assert (number == newCard.get_number())
            assert (suit == newCard.get_suit())

            newCardString = "%s of %s" % (numberString, suit.title())
            assert (newCardString == newCard.__str__())

def test_disallowed():
    def __randomSuit(length=5):
           return ''.join(random.choice(string.letters) for i in range(length))

    # disallowed number
    for number in (random.randint(-50, 49) for _ in xrange(random.randint(0,49))):
        if ((number >= 1) and (number <= 13)):
            continue
        with pytest.raises(ValueError):
            newCard = card.Card(number, 'hearts')

    # dissllowed suit
    for i in xrange(random.randint(0,49)):
        with pytest.raises(ValueError):
            newCard = card.Card(random.randint(0,13), __randomSuit())

    for suit in ('HEARTSS', 'DIAMOONNDSA', 'SSPADDES', 'CCLLUUBBSS'):
        with pytest.raises(ValueError):
            newCard = card.Card(random.randint(0,13), suit)

