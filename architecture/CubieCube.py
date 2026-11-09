
# step 1 create CubieCube so i can start on the percompute of the tables
from enums import Corner as Co, Edge as Ed
from helper import handle_ori_change
from math import comb
# NOTES
# Co(i) returns an actual Corner enum member so we can later do
# corner_per.URF() or smth.
# [:] creates shallow copy, else it would point to same lst


class CubieCube():

    def __init__(self, co_per=None, co_ori=None, ed_per=None, ed_ori=None):
        ''' Initializes the cube as default or with given values.
        -------------------------------------------------
        | index i       | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
        | permutation   |URF|UFL|ULB|UBR|DFR|DLF|DBL|DRB|
        | orientation   | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
        -------------------------------------------------
        same for edges

        individual values not coordinates:
        cc = corner permutation
        co = corner orientation
        ec = edge permutation
        eo = edge orientation
        '''

        if co_per is None:
            self.cc = [Co(i) for i in range(8)]
        else:
            self.cc = co_per[:]
        if co_ori is None:
            self.co = [0] * 8
        else:
            self.co = co_ori[:]

        if ed_per is None:
            self.ec = [Ed(i) for i in range(12)]
        else:
            self.ec = ed_per[:]
        if ed_ori is None:
            self.eo = [0] * 12
        else:
            self.eo = ed_ori[:]

#  math

    def corner_multiply(self, b):
        ''' (A * B).c[x] = A.c[ B.c[x] ]
            (A * B).o[x] = A.o[ B.c[x] ] + B.o[x]

            Applies the permutation of a cube b to the Corners of the
            class cube. Changes permutation .cc and orientation .co
        '''
        cc = [0] * 8
        co = [0] * 8
        # fill new arrays with updated values
        for i in Co:
            cc[i] = self.cc[b.cc[i]]
            ori_A = self.co[b.cc[i]]
            ori_B = b.co[i]
            co[i] = handle_ori_change(ori_A, ori_B)
        # update the values
        for i in Co:
            self.cc[i] = cc[i]
            self.co[i] = co[i]

    def edge_multiply(self, b):
        ''' (A * B).c[x] = A.c[ B.c[x] ]
            (A * B).o[x] = B.o[x] + A.o[ B.c[x] ]

            Applies the permutation of a cube b to the Edges of the
            class cube. Changes permutation .ec and orientation .eo
        '''
        ec = [0] * 12
        eo = [0] * 12
        # fill new arrays with updated values
        for i in Ed:
            ec[i] = self.ec[b.ec[i]]
            # % 2 so the result is always 0 or 1
            eo[i] = (b.eo[i] + self.eo[b.ec[i]]) % 2
        # update the values
        for i in Ed:
            self.ec = ec[i]
            self.eo = eo[i]

    def multiply(self, b):
        ''' Applie the permutations of b to class cube for
            Corners & Edges
        '''
        self.corner_multiply(b)
        self.edge_multiply(b)

#  getter setter

    def get_twist(self):
        ''' Twist = Corner orientation coordinate.
            The orientation of the 8 corners are described by
            a number from 0 to 2186 (3^7 - 1).
        '''
        coord = 0
        for i in range(Co.URF, Co.DRB):
            coord = 3 * coord + self.co[i]
        return coord

    def set_twist(self, twist):
        ''' Apply a corner orientation to class cube.

            go through corners 6 to 0
            take corner orienatation|twist % 3
            -> reverse of how we get it

            sum of all eight corner twists must be divisible by 3
            ((3 - parity % 3) % 3) calculates the orientation
            needed to make the total sum divisible by 3,
            First () can result in 3, second % is necessary
        '''
        parity = 0
        # go form 6 to 0 | 7 corners
        for i in range(Co.DRB - 1, Co.URF - 1, -1):
            self.co[i] = twist % 3
            parity += self.co[i]
            twist //= 3  # // floor division, returns int
        self.co[Co.DRB] = ((3 - parity % 3) % 3)

    def get_flip(self):
        ''' Flip = Edge orientation Coord.
            The orientation of the 12 edges is described by a
            number from 0 to 2047 (2^11 - 1).
        '''
        coord = 0
        for i in range(Ed.UR, Ed.BR):
            coord = 2 * coord + self.eo[i]
        return coord

    def set_flip(self, flip):
        ''' Apply a Edge orientation to class cube.

            get the individual values by reversing how we cot the number
            and calculate the only possible last value
        '''
        parity = 0
        for i in range(Ed.BR - 1, Ed.UR - 1, -1):
            self.eo[i] = flip % 2
            parity += self.eo[i]
            flip //= 2
        self.eo[Ed.BR] = ((2 - parity % 2) % 2)

    def get_slice(self):
        ''' Slice = UDSlice orientation coordinate.
        Get the location of the UD-slice edges FR,FL,BL and BR
        ignoring their permutation.
        0<= slice < 495 in phase 1, slice = 0 in phase 2.

        Entirely Different from the Documentation, just Why?!
        '''
        coord = 0
        k = 0
        for i in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ec[i] <= Ed.BR:  # if current edge is UDSlice
                coord += comb((11 - i), k + 1)
                k += 1
        return coord

    def set_slice(self, coord):
        ''' Ignore specific positions, first go through all
        edge positions, if the coord minus the cooeficient is bigger
        than 0 its a UDSlice edge. The rest is just filled with the other
        edges.'''

        UDSlices = [Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        otherSlices = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        a = coord
        # all edges invalid
        for i in Ed:
            self.ec[i] = -1

        k = 4
        # set UD-Slice edges
        for i in Ed:
            if a - comb(11 - i, k) >= 0:
                self.ec[i] = UDSlices[4 - k]
                a -= comb(11 - i, k)
                k -= 1

        k = 0
        # set other edges
        for i in Ed:
            if self.ec[i] == -1:
                self.ec[i] == otherSlices[k]
                k += 1

    def get_slice_sorted(self):
        '''slice_sorted = UDSlice orientation + order
        0 <= slice_sorted < 11880 in phase 1, 0 <= slice_sorted < 24
        in phase 2, slice_sorted = 0 for solved cube.'''
        pass

    def set_slice_sorted(self):
        pass

    def get_u_edges(self):
        ''''''
        pass

    def set_u_edges(self):
        pass

    def get_d_edges(self):
        ''''''
        pass

    def set_d_edges(self):
        pass

    def get_corners(self):
        ''''''
        pass

    def set_corners(self):
        pass

    def get_ud_edges(self):
        ''''''
        pass

    def set_ud_edges(self):
        pass

#  other

    def verify():
        pass
