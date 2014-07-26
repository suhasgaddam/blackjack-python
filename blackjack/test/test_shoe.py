#!/usr/bin/python

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))

import pytest
import blackjack.shoe as shoe
import blackjack.card as card

import pprint
import itertools

import numpy
import string

def local_check_shoe(sss):
    card_dict = dict((suit, dict((number, 0) for number in card.POSSIBLE_NUMBER)) for suit in card.POSSIBLE_SUIT)

    cards_iter = itertools.chain(sss._cards, sss._in_play_cards, sss._used_cards)
    for cc in cards_iter:
        card_dict[cc.get_suit()][cc.get_number()] += 1

    return not any(any(occurences != sss._number_of_decks for occurences in card_dict[suit].itervalues()) for suit in card.POSSIBLE_SUIT)

def is_deck_ordered(sss):
    if sss._in_play_cards or sss._used_cards:
        return False

    ordered_shoe = shoe.Shoe(sss._number_of_decks)

    if len(ordered_shoe._cards) != len(sss._cards):
        return False


    for a_card, b_card in zip(ordered_shoe._cards, sss._cards):
        if (a_card.get_number() != b_card.get_number()) and (a_card.get_suit() != b_card.get_suit()):
            return False

    return True

def test_functionality():
    new_shoe = shoe.Shoe(4)
    while new_shoe.is_valid_deck():
        dealt_card = new_shoe.deal()
        assert local_check_shoe(new_shoe)
        assert new_shoe.check_shoe()
        new_shoe.burn([dealt_card])

def test_bad_number_of_decks():
    with pytest.raises(ValueError):
        new_shoe = shoe.Shoe(0)
    for i in xrange(numpy.random.randint(50)):
        with pytest.raises(ValueError):
            new_shoe = shoe.Shoe(numpy.random.randint(-50, 0))

def test_shuffle_deck():
    new_shoe = shoe.Shoe(4)
    assert is_deck_ordered(new_shoe)
    new_shoe.shuffle_deck()
    assert not is_deck_ordered(new_shoe) 

    new_shoe.deal()
    assert not is_deck_ordered(new_shoe) 

    new_shoe = shoe.Shoe(4)
    new_shoe._cards.pop()
    assert not is_deck_ordered(new_shoe) 

def test_bad_deck_missing_cards():
    new_shoe = shoe.Shoe(4)
    new_shoe._cards.pop()
    assert not local_check_shoe(new_shoe)
    assert not new_shoe.check_shoe()

    new_shoe = shoe.Shoe(4)
    new_shoe._cards.pop()
    new_shoe._cards.pop()
    new_shoe._cards.pop()
    assert not local_check_shoe(new_shoe)
    assert not new_shoe.check_shoe()

def test_bad_deck_repeated_cards():
    def _get_random_index(high):
        return numpy.random.randint(high)

    new_shoe = shoe.Shoe(4)

    random_card_index = _get_random_index(len(new_shoe._cards))
    chosen_card = new_shoe._cards[random_card_index]
    copied_chosen_card = card.Card(chosen_card.get_number(), chosen_card.get_suit())

    new_random_card_index = random_card_index
    while random_card_index == new_random_card_index:
        new_random_card_index = _get_random_index(len(new_shoe._cards))

    assert local_check_shoe(new_shoe)
    assert new_shoe.check_shoe()
    new_shoe._cards[new_random_card_index] = copied_chosen_card
    assert not local_check_shoe(new_shoe)
    assert not new_shoe.check_shoe()

