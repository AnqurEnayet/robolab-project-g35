#!/usr/bin/env python3

import pytest
from hamming_code import *
from stack_machine import *


def test_example(capfd):
    """
        Example implementation of whole workflow:
            - Decode valid/correctable codes and
            - Execute the opcodes on the stack machine
            - Checking the final result afterward
    """
    assert()
