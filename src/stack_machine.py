#!/usr/bin/env python3

# Our pre-defined Stack class
from stack import Stack
# System defaults
from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self)
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.stack = Stack()

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute with length of 6 (0, 0, 0, 0, 0, 0)
        Returns:
            SMState: Current state of the stack machine
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        pass

    def peek(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack. Internally calls the Stack's peek() method.

        Returns:
            union: Can be tuple, str or None
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        pass
