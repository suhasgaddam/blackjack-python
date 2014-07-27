#!/usr/bin/python

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))

import pytest
import blackjack.player as player
import blackjack.shoe as shoe
import blackjack.card as card

import numpy

def test_functionality():
    suit = card.POSSIBLE_SUIT[0]

    new_player = player.Player('Tester')
    card_numbers = [2, 7]
    for number in card_numbers:
        new_player.add_card(card.Card(number, suit))
    assert [sum(card_numbers)] == new_player._count

    new_player.reset()
    card_numbers = [1, 7]
    for number in card_numbers:
        new_player.add_card(card.Card(number, suit))
    assert sorted([sum(card_numbers), 11+7]) == sorted(new_player._count)

def test_is_blackjack():
    def _check_is_blackjack(card_numbers, blackjack=True):
        new_player = player.Player('Tester')
        suit = card.POSSIBLE_SUIT[numpy.random.randint(4)]
        for number in card_numbers:
            new_player.add_card(card.Card(number, suit))

        if blackjack:
            assert new_player.is_blackjack()
            assert player.STAY == new_player.action()
        else:
            assert not new_player.is_blackjack()

    for face_card in [10, 11, 12, 13]:
        card_numbers = [1, face_card]

        _check_is_blackjack(card_numbers)
        _check_is_blackjack(reversed(card_numbers))

    _check_is_blackjack([1, 10, 10], False)
    _check_is_blackjack([10, 1, 10], False)
    _check_is_blackjack([10, 10, 1], False)

    _check_is_blackjack([1, 2, 3, 4, 5, 6], False)


    _check_is_blackjack([7, 8, 6], False)

def test_is_winner():
    def _check_is_winner(card_numbers, winner=True):
        new_player = player.Player('Tester')
        suit = card.POSSIBLE_SUIT[numpy.random.randint(4)]
        for number in card_numbers:
            new_player.add_card(card.Card(number, suit))

        if winner:
            assert new_player.is_winner()
            new_player.winner()
        else:
            assert not new_player.is_winner()
            new_player.loser()

    _check_is_winner([1, 10, 10])
    _check_is_winner([10, 1, 10])
    _check_is_winner([10, 10, 1])

    _check_is_winner([1, 2, 3, 4, 5, 6])

    _check_is_winner([7, 8, 6])

    _check_is_winner([7, 8, 6, 10], False)
    _check_is_winner([10, 10, 5], False)
    _check_is_winner([5, 5, 5, 5, 5], False)
    _check_is_winner([6, 6, 6, 4], False)

def test_is_loser():
    def _check_is_loser(card_numbers, loser=True):
        new_player = player.Player('Tester')
        suit = card.POSSIBLE_SUIT[numpy.random.randint(4)]
        for number in card_numbers:
            new_player.add_card(card.Card(number, suit))

        if loser:
            assert new_player.is_loser()
            new_player.loser()

    _check_is_loser([1, 10, 10], False)
    _check_is_loser([10, 1, 10], False)
    _check_is_loser([10, 10, 1], False)

    _check_is_loser([1, 2, 3, 4, 5, 6], False)

    _check_is_loser([7, 8, 6], False)

    _check_is_loser([7, 8, 6, 10])
    _check_is_loser([10, 10, 5])
    _check_is_loser([5, 5, 5, 5, 5])
    _check_is_loser([6, 6, 6, 4])

def test_silly_strategy():
    def _check_action(card_numbers, action=player.STAY):
        new_player = player.Player('Tester')
        suit = card.POSSIBLE_SUIT[numpy.random.randint(4)]
        for number in card_numbers:
            new_player.add_card(card.Card(number, suit))

        assert action == new_player.action()

    _check_action([1, 10, 10], player.STAY)
    _check_action([10, 1, 10], player.STAY)
    _check_action([10, 10, 1], player.STAY)

    _check_action([1, 2, 3, 4, 5, 6], player.STAY)

    _check_action([7, 8, 6], player.STAY)

    _check_action([10, 4], player.HIT)
    _check_action([10, 5], player.STAY)
    _check_action([10, 6], player.STAY)

    _check_action([1, 3], player.HIT)
    _check_action([1, 4], player.HIT)
    _check_action([1, 5], player.HIT)

def test_string_representaion():
    name = 'Bob'
    assert "Player %s" % name == "%s" % player.Player(name)

