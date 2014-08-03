#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

__author__ = "Lars Solberg"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Lars Solberg"


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Defaulting to null output in case Caculator class is imported


class BowlingCalculator(object):
    """
    Calculates your bowling score with as many frames/rounds as you want.

    To run/test, feed the script with the round scores as the first input. Example "python bowling_calculator.py 1/-/x-/23xx22-/1/1"
      - means miss/gutter-ball
      x is a strike
      / is a spare
      0-9 is normal points

    To use as a module, import it and use the calculate(). Example "BowlingCalculator().calculate('1/-/x-/23xx22-/1/1')"

    To run the doctests, start the script with -m doctest -v. Example "python -m doctest -v bowling_calculator.py"'
    """

    def help(self):
        print('Bowling calculator')
        print(self.__doc__)

    def _normalize(self, frames):
        """
        Normalize script input and turn it into an array with 1 item per item. All of 'abc', 'a b c' and 'ab c' (arrays and strings) will turn into ['a', 'b', 'c'] (lowercase)
        >>> BowlingCalculator()._normalize('abc')
        ['a', 'b', 'c']
        >>> BowlingCalculator()._normalize(['a', 'bc'])
        ['a', 'b', 'c']
        >>> BowlingCalculator()._normalize(['a', 'b', 'c'])
        ['a', 'b', 'c']
        """
        return [ i for i in ''.join(frames).lower() ]

    def _get_points_from_character(self, character):
        """
        >>> BowlingCalculator()._get_points_from_character('-')
        0

        >>> BowlingCalculator()._get_points_from_character('4')
        4

        >>> BowlingCalculator()._get_points_from_character('x')
        10
        """
        if character.isdigit():
            return int(character)
        elif character == '-':
            return 0
        else:
            return 10  # Since it must be a strike or spare

    def calculate(self, frames):
        """
        >>> BowlingCalculator().calculate('XxXxXxXxXxXx')
        300

        >>> BowlingCalculator().calculate('9-9-9-9-9-9-9-9-9-9-')
        90

        >>> BowlingCalculator().calculate('5/5/5/5/5/5/5/5/5/5/5')
        150

        >>> BowlingCalculator().calculate('--x--x--x--x--x--')
        50

        >>> BowlingCalculator().calculate('1/-/x-/23xx22-/1/1')
        129

        >>> BowlingCalculator().calculate('0000000000000000000/x')
        20

        >>> BowlingCalculator().calculate('000000000000000000xxx')
        30

        >>> BowlingCalculator().calculate('0000000000000000000/1')
        11
        """

        total_points = 0
        index = 0

        frames = self._normalize(frames)
        frame_count = len(frames)

        logger.debug('')

        for i in frames:

            logger.debug('Throw %s is %s' % (index + 1, i))

            # The last frame is special. There is no bonus points added..
            last_frame = True if index + 3 >= frame_count else False

            if i.isdigit():
                try:
                    if frames[index+1] != '/':
                        total_points += self._get_points_from_character(i)
                        logger.debug('  Adding %s points' % (i))
                    else:
                        logger.debug('  Got %s points, but not adding them since next throw is a spare' % (i))
                except IndexError:
                    total_points += self._get_points_from_character(i)

            elif i == 'x':
                logger.debug('  Strike - adding 10 points')
                total_points += 10

                if last_frame:
                    logger.debug('  We are at the last round, so no bonuses is calculated')
                else:
                    bonus_points = self._get_points_from_character(frames[index+2]) + self._get_points_from_character(frames[index+1])
                    logger.debug('  Adding %s bonus points (the points for the next two throws)' % (bonus_points,))
                    total_points += bonus_points

            elif i == '/':
                logger.debug('  Spare - adding 10 points')
                total_points += 10

                if last_frame:
                    logger.debug('  We are at the last round, so no bonuses is calculated')
                else:
                    bonus_points = self._get_points_from_character(frames[index+1])
                    logger.debug('  Adding %s bonus points (the points for the next one throw)' % (bonus_points,))
                    total_points += bonus_points

            elif i == '-':
                logger.debug('  Gutter-ball/miss - No new points..')

            index += 1

            logger.debug('  Total points is now %s' % (total_points,))
            logger.debug('')

        logger.debug('Point list: %s' % (total_points,))
        return total_points

if __name__ == '__main__':
    logger.addHandler(logging.StreamHandler())  # Display info when running script manually
    logger.setLevel(logging.INFO)  # Set to logging.DEBUG for debug

    bc = BowlingCalculator()

    frames = sys.argv[1:]  # [0] is the script name

    if frames:
        logger.debug('Starting score calculation for %s' % (''.join(frames)))
        print(bc.calculate(frames))
    else:
        bc.help()

    sys.exit(0)
