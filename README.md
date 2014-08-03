# Bowling Calculator #

This is a simple bowling score calculator that takes text as input and suport an arbitrary number of throws.

## Run ##
Feed the script with the round scores as the first input. Example:

    # python bowling_calculator.py 1/-/x-/23xx22-/1/1
    129

**x** is a strike, **/** is a spare, **-** means miss/gutter-ball and **0-9** is normal points

## As a module ##
To use the calculator as a module, import it and use the calculate() function. Example:

    >>> from bowling_calculator import BowlingCalculator
    >>> BowlingCalculator().calculate('1/-/x-/23xx22-/1/1')
    129

## Run tests ##
We use inline (doctests) tests to keep the module simple and portable.
To run the doctests, start the script with -m doctest -v. Example `python -m doctest -v bowling_calculator.py`

## Supported python versions ##
This module runs fine on python 2.7 and above (including 3.x).
