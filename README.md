blackjack-python
================

A Python Implementation Of Blackjack


## Getting started

Currently, this is not an interactive game. Creating the `Table` object will cause the game to run its course.

Note you need to load the logging config first if you want to see what happens under the covers.

    >>> import json, logging.config
    >>> logging_config = json.load(open('blackjack/conf/logging.conf','r'))
    >>> from blackjack import table
    >>> t = table.Table()
