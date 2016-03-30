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

## Development

    git clone https://github.com/suhasgaddam/blackjack-python.git
    cd blackjack-python

It is recommended you use `virtualenv` as it will help manage dependencies in such a way that they will not conflict with your system-wide packages.

    vagrant@vagrant-ubuntu-wily-64:~$ virtualenv blackjack-python/
    Running virtualenv with interpreter /usr/bin/python2
    New python executable in blackjack-python/bin/python2
    Also creating executable in blackjack-python/bin/python
    Installing setuptools, pip...done.
    vagrant@vagrant-ubuntu-wily-64:~$ cd blackjack-python/
    vagrant@vagrant-ubuntu-wily-64:~/blackjack-python$ source bin/activate
    (blackjack-python)vagrant@vagrant-ubuntu-wily-64:~/blackjack-python$ deactivate
    vagrant@vagrant-ubuntu-wily-64:~/blackjack-python$

To install the Python dependencies, run `pip install -r requirements.txt`. Please note the tests currently rely on `numpy` (though c.f. TODO below), which will only install properly via `virtualenv` if you have the python header files available (`apt-get install python-dev` on Debian/Ubuntu).

## Running tests

You can run tests via the `pytest` module:

    (blackjack-python)vagrant@vagrant-ubuntu-wily-64:~/blackjack-python$ python -m pytest blackjack/test/
    ====================================== test session starts ======================================
    platform linux2 -- Python 2.7.10, pytest-2.9.1, py-1.4.31, pluggy-0.3.1
    rootdir: /home/vagrant/blackjack-python/blackjack/test, inifile:
    collected 15 items
    
    blackjack/test/test_card.py ..
    blackjack/test/test_dealer.py ..
    blackjack/test/test_player.py ......
    blackjack/test/test_shoe.py .....
    
    =================================== 15 passed in 0.21 seconds ===================================

## References

   * `pip` [requirements files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
   * `virtualenv` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

## TODO

   * Remove `numpy` as a dependency in the tests - we should be able to achieve the same thing with `random.randint`
