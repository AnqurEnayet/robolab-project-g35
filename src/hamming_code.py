#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union

# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """ Return codes for the Hamming Code interface """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'

class HammingCode:
    """ Provides decoding capabilities for the specified Hamming Code """

    def __init__(self):
        """ Initializes the class HammingCode with all values necessary. """
        self.total_bits = 11  # n
        self.data_bits = 6    # k
        self.parity_bits = 5  # r (includes p5)

        # Predefined non-systematic generator matrix G'
        self.gns = [
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        ]

        self.g = self.__convert_to_g(self.gns)
        self.h = self.__derive_h(self.g)
        
        self.syndrome_map = {}
        rows_h = len(self.h)
        cols_h = len(self.h[0])
        for col_idx in range(cols_h):
            col_vector = tuple(self.h[r][col_idx] for r in range(rows_h))
            self.syndrome_map[col_vector] = col_idx

    def _dot_product_mod2(self, vec_a: List[int], vec_b: List[int]) -> int:
        return sum(a * b for a, b in zip(vec_a, vec_b)) % 2

    def __convert_to_g(self, gns: List):
        """ Converts a non-systematic generator matrix into a systematic one. """
        m = [row[:] for row in gns]
        rows = len(m)

        # Forward Elimination (Row Echelon)
        for i in range(rows):
            if m[i][i] == 0:
                # Find pivot
                for j in range(i + 1, rows):
                    if m[j][i] == 1:
                        m[i], m[j] = m[j], m[i]
                        break
            
            # Eliminate below
            for j in range(i + 1, rows):
                if m[j][i] == 1:
                    m[j] = [x ^ y for x, y in zip(m[j], m[i])]

        # Backward Elimination (Reduced Row Echelon)
        for i in range(rows - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                if m[j][i] == 1:
                    m[j] = [x ^ y for x, y in zip(m[j], m[i])]

        return m

    def __derive_h(self, g: List):
        """ Derives H = [P^T | I] from G = [I | P]. """
        k = self.data_bits
        r_matrix = len(g[0]) - k # Calculate purely matrix parity bits (4)

        p_part = [row[k:] for row in g]

        # Transpose P
        p_transposed = [
            [p_part[j][i] for j in range(len(p_part))] 
            for i in range(len(p_part[0]))
        ]

        # Identity Matrix
        identity = [[1 if i == j else 0 for j in range(r_matrix)] for i in range(r_matrix)]

        # Concatenate P^T and I
        return [row_p + row_i for row_p, row_i in zip(p_transposed, identity)]

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """ Encodes the given word. """
        if len(source_word) != self.data_bits:
            raise ValueError(f"Input must be length {self.data_bits}")

        # Matrix Multiplication
        # c = u * G
        encoded_bits = []
        cols_g = len(self.g[0])
        
        for i in range(cols_g):
            col_g = [self.g[row][i] for row in range(self.data_bits)]
            bit = self._dot_product_mod2(source_word, col_g)
            encoded_bits.append(bit)

        encoded_bits.append(sum(encoded_bits) % 2)

        return tuple(encoded_bits)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """ Decodes the word using syndrome lookup. """
        if len(encoded_word) != self.total_bits:
            raise ValueError(f"Encoded word must be length {self.total_bits}")

        hamming_part = list(encoded_word[:10])
        received_p5 = encoded_word[10]

        # Check p5 parity
        has_parity_error = (sum(hamming_part) % 2) != received_p5

        # Calculate Syndrome
        # vector S = H * r^T
        syndrome = []
        for row_h in self.h:
            syndrome.append(self._dot_product_mod2(hamming_part, row_h))
        
        syndrome_tuple = tuple(syndrome)
        syndrome_is_zero = all(b == 0 for b in syndrome)

        if syndrome_is_zero:
            if not has_parity_error:
                return tuple(hamming_part[:self.data_bits]), HCResult.VALID
            else:
                return tuple(hamming_part[:self.data_bits]), HCResult.CORRECTED
        else:
            if has_parity_error:
                # Non-zero syndrome + Parity Error = Single bit error
                error_idx = self.syndrome_map.get(syndrome_tuple, -1)
                
                if error_idx != -1:
                    hamming_part[error_idx] ^= 1 # Flip bit
                    return tuple(hamming_part[:self.data_bits]), HCResult.CORRECTED
            
            return None, HCResult.UNCORRECTABLE