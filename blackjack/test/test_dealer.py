#!/usr/bin/python

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))

import pytest
import blackjack.dealer as dealer
import blackjack.table as table

def test_dummy():
    for i in range(5):
        t = table.Table()

def test_string_representation():
    name = 'Lob'
    assert "Dealer %s" % name == "%s" % dealer.Dealer(name, None)

