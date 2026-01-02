#!/usr/bin/env python3

import ev3dev.ev3 as ev3


class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self):
        """
        Moves the sensor one step to read the next bar code value
        """
        # implementation
        pass

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        # implementation
        pass

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        # implementation
        pass

    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        # implementation
        pass
