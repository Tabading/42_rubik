
# step 1 create CubieCube so i can start on the percompute of the tables
from enums import Color, Corner as Co, Edge as Ed
import defs 
from helper import handle_ori_change, rotate_left, rotate_right
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
        | permutation c |URF|UFL|ULB|UBR|DFR|DLF|DBL|DRB|
        | orientation o | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
        -------------------------------------------------
        same for edges

        individual values not coordinates:
        cc = corner permutation
        co = corner orientation
        ec = edge permutation
        eo = edge orientation
        '''

        # corner
        if co_per is None:
            self.cc = [Co(i) for i in range(8)]
        else:
            self.cc = co_per[:]
        if co_ori is None:
            self.co = [0] * 8
        else:
            self.co = co_ori[:]

        # edge
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
            (A * B).o[x] = A.o[ B.c[x] ] + B.o[x]

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
        ''' Apply the permutations of b to class cube for
            Corners & Edges
        '''

        self.corner_multiply(b)
        self.edge_multiply(b)

#  getter setter

    def corner_parity(self):
        ''' Return corner parity.

        Go backwards through self.cc | corner permutation,
        if a number to the left is bigger than the current number
        parity, +1

        ex:
        | index i       | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
        | permutation c | 5 | 6 | 2 | 1 | 0 | 3 | 4 | 7 |

        i = 7
            0-6 no bigger par = 0
        i = 6
            0-5 2 bigger par = 2
        i = 5
            0-4 2 bigger par = 4
        i = 4
            0-3 no bigger par = 4
        i = 3
            0-2 3 bigger par = 7
        i = 2
            0-1 2 bigger par = 9
        i = 1
            0 not bigger par = 9
        
        '''

        par = 0
        for i in range(Co.DRB, Co.URF, -1):  # 7 - 1
            for j in range(i - 1, Co.URF - 1, -1):  # i - 0
                if self.cc[j] > self.cc[i]:
                    par += 1
        return par

    def edge_parity(self):
        ''' Return edge parity. '''

        par = 0
        for i in range(Ed.BR, Ed.UR, -1):  # 11 - 1
            for j in range(i - 1, Ed.UR - 1, -1):  # i - 0
                if self.ec[j] > self.ec[i]:
                    par += 1
        return par

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
        ''' Apply a corner orientation coordinate to class cube.

            Go through corners 6 to 0
            take corner orienatation|twist % 3
            -> reverse of how we create it

            sum of all eight corner twists must be divisible by 3
            ((3 - parity % 3) % 3) calculates the orientation
            needed to make the total sum divisible by 3,
            First () can result in 3, second % is necessary
        '''

        parity = 0
        for i in range(Co.DRB - 1, Co.URF - 1, -1):
            self.co[i] = twist % 3
            parity += self.co[i]
            twist //= 3
        self.co[Co.DRB] = ((3 - parity % 3) % 3)

    def get_flip(self):
        ''' Flip = Edge orientation Coordinate.
            The orientation of the 12 edges is described by a
            number from 0 to 2047 (2^11 - 1).
        '''

        coord = 0
        for i in range(Ed.UR, Ed.BR):
            coord = 2 * coord + self.eo[i]
        return coord

    def set_flip(self, flip):
        ''' Apply a Edge orientation coordinate to class cube.

            Get the individual values by reversing how we got the number
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
            if Ed.FR <= self.ec[i] <= Ed.BR:
                coord += comb((11 - i), k + 1)
                k += 1
        return coord

    def set_slice(self, coord):
        ''' Ignore specific positions, first go through all
        edge positions, if coord - cooeficient is bigger
        than 0 it's a UDSlice edge. The rest is just filled with the other
        edges.'''

        UDSlices = [Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        otherSlices = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        a = coord

        # all edges invalid
        for i in Ed:
            self.ec[i] = -1

        # set UD-Slice edges
        k = 4
        for i in Ed:
            if a - comb(11 - i, k) >= 0:
                self.ec[i] = UDSlices[4 - k]
                a -= comb(11 - i, k)
                k -= 1

        # set other edges
        j = 0
        for i in Ed:
            if self.ec[i] == -1:
                self.ec[i] == otherSlices[j]
                j += 1

    def get_slice_sorted(self):
        '''slice_sorted = UDSlice orientation + permutation|order
        0 <= slice_sorted < 11880 in phase 1,
        0 <= slice_sorted < 24 in phase 2,
        slice_sorted = 0 for solved cube.

        Do the same as in in get_slice AND save which edge is encountered
        in an array. This saves them backwards.
        Go through that array backwards and see how often you need to rotate
        the values for the correct numbers to be in the correct space.

        decode coord1 with // 24, coord2 with % 24
        '''

        coord1 = 0  # orientation | location
        coord2 = 0  # permutation | order
        arr = [0] * 4

        # get coord1
        k = 0
        for i in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ec[i] <= Ed.BR:
                coord1 += comb((11 - i), k + 1)
                arr[3 - k] = self.ec[i]  # save encountered edge
                k += 1

        # get coord2
        # ignore last edge, when 3 edges are in position, the
        # last is automatically correct
        for i in range(3, 0, -1):
            k = 0
            while arr[i] != i + 8:  # + 8 because edges 8 - 11
                # i goes down, correctly positiond nums stay in place
                rotate_left(arr, 0, i)
                k += 1  # counts rotations
            coord2 = (i + 1) * coord2 + k

        return 24 * coord1 + coord2

    def set_slice_sorted(self, coord):
        ''' Set edges corresponding to given coord. we get placement & order of
        the UD edges from coord, all other edges are in numerical order.

        - Decode coord back into coord1 & coord2 | orientation & permutation
        - First invalidate all edges to -1
        - Use coord2 to rotate UDSlices into the specified order they should be
            encountered in
        - Use coord1 to find the locations for those slices and put them there in
            new order
        - Fill other edges in orderof array
        '''

        UDSlices = [Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        otherSlices = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        coord1 = coord // 24  # orientation | location
        coord2 = coord % 24  # permutation / order

        # all edges invalid
        for i in Ed:
            self.ec[i] = -1

        # change UDSlices array to be correct permutation/order
        for i in range(1, 4):
            k = coord2 % (i + 1)
            coord2 //= (i + 1)
            while k > 0:
                rotate_right(UDSlices, 0, i)
                k -= 1

        # set UD-Slice edges
        k = 4
        for i in Ed:
            if coord1 - comb(11 - i, k) >= 0:
                self.ec[i] = UDSlices[4 - k]
                coord1 -= comb(11 - i, k)
                k -= 1

        # set other edges
        j = 0
        for i in Ed:
            if self.ec[i] == -1:
                self.ec[i] == otherSlices[j]
                j += 1

# region: for u & d edges:
# Almost the same as slice except for 1 thing:
#   we rotate the array 4 to the right. so the solved location coordinate
#   (not the order)
#   for d it's 0 like slice, since it's essentially checking for the
#   exact same locations:
#
#    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | position
#    | U | U | U | U | D | D | D | D | M | M | M  | M  | normal like for slice
#    | M | M | M | M | U | U | U | U | D | D | D  | D  | rotated 4 to right
#
# So since the solved location for D, when rotated, is the same as Slice they
# share the solved state number 0.
# For U it's diffrent since its solved state after rotation is in the middle,
# so it ends up as 69 for solved (1656 = 24*(69) + 0)
# endregion

    def get_u_edges(self):
        ''' Get the permutation and location of edges UR, UF, UL and UB.
        0 <= u_edges < 11880 in phase 1,
        0 <= u_edges < 1680 in phase 2,
        u_edges = 1656 for solved cube.
        (is it because we get it from a = 69? . . .)

        Don't miss the rotating of self.ec, needs to be considered
        when setting too

        decode coord1 with // 24, coord2 with % 24
        '''

        coord1 = 0  # orientation | location
        coord2 = 0  # permutation | order
        arr = [0] * 4

        # modify permutation : explanation in comment "for u & d edges"
        ec_modified = self.ec[:]
        for i in range(4):
            rotate_right(ec_modified, 0, 11)

        # get coord1
        k = 0
        for i in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.UR <= ec_modified[i] <= Ed.UB:
                coord1 += comb((11 - i), k + 1)
                arr[3 - k] = ec_modified[i]  # save encountered edge
                k += 1

        # get coord2
        for i in range(3, 0, -1):
            k = 0
            while arr[i] != i:
                # i goes down, correctly positiond nums stay in place
                rotate_left(arr, 0, i)
                k += 1  # counts rotations
            coord2 = (i + 1) * coord2 + k

        return 24 * coord1 + coord2

    def set_u_edges(self, coord):
        ''' Set edges corresponding to given coord. we get placement & order of
        the U edges from coord, all other edges are in numerical order.

        - Decode coord back into coord1 & coord2 | orientation & permutation
        - First invalidate all edges to -1
        - Use coord2 to rotate UDSlices into the specified order they should be
            encountered in
        - Use coord1 to find the locations for those slices and put them there
            in new order
        - Fill other edges in order of array
        - rotate 4 left to reverse rotation when getting coordinate
        '''

        USlices = [Ed.UR, Ed.UL, Ed.UL, Ed.UR]
        otherSlices = [Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        coord2 = coord % 24  # permutation / order
        coord1 = coord // 24  # placement

        # all edges invalid
        for i in Ed:
            self.ec[i] = -1

        # change USlices array to be correct permutation/order
        for i in range(1, 4):
            k = coord2 % (i + 1)
            coord2 //= (i + 1)
            while k > 0:
                rotate_right(USlices, 0, i)
                k -= 1

        # set U-Slice edges
        k = 4
        for i in Ed:
            if coord1 - comb(11 - i, k) >= 0:
                self.ec[i] = USlices[4 - k]
                coord1 -= comb(11 - i, k)
                k -= 1

        # set other edges
        j = 0
        for i in Ed:
            if self.ec[i] == -1:
                self.ec[i] == otherSlices[j]
                j += 1

        # rotate 4 left
        for j in range(4):
            rotate_left(self.ec, 0, 11)

    def get_d_edges(self):
        ''' Get the permutation and location of edges DR, DF, DL and DB.
        0 <= d_edges < 11880 in phase 1,
        0 <= d_edges < 1680 in phase 2,
        d_edges = 0 for solved cube.

        Don't miss the rotating of self.ec, needs to be considered
        when setting too

        decode coord1 with // 24, coord2 with % 24
        '''

        coord1 = 0
        coord2 = 0
        arr = [0] * 4

        # modify permutation : explanation in comment "for u & d edges"
        ec_modified = self.ec[:]
        for i in range(4):
            rotate_right(ec_modified, 0, 11)

        # get coord1
        k = 0
        for i in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.DR <= ec_modified[i] <= Ed.DB:
                coord1 += comb((11 - i), k + 1)
                arr[3 - k] = ec_modified[i]  # save encountered edge
                k += 1

        # get coord2
        for i in range(3, 0, -1):
            k = 0
            while arr[i] != i + 4:
                # i goes down, correctly positiond nums stay in place
                rotate_left(arr, 0, i)
                k += 1  # counts rotations
            coord2 = (i + 1) * coord2 + k

        return 24 * coord1 + coord2

    def set_d_edges(self, coord):
        ''' Set edges corresponding to given coord. we get placement & order of
        the D edges from coord, all other edges are in numerical order.

        - Decode coord back into coord1 & coord2 | orientation & permutation
        - First invalidate all edges to -1
        - Use coord2 to rotate UDSlices into the specified order they should be
            encountered in
        - Use coord1 to find the locations for those slices and put them there
            in new order
        - Fill other edges in order of array
        - rotate 4 left to reverse rotation when getting coordinate
        '''

        DSlices = [Ed.DR, Ed.DL, Ed.DL, Ed.DR]
        otherSlices = [Ed.FR, Ed.FL, Ed.BL, Ed.BR, Ed.UR, Ed.UF, Ed.UL, Ed.UB]
        coord2 = coord % 24  # permutation / order
        coord1 = coord // 24  # placement

        # all edges invalid
        for i in Ed:
            self.ec[i] = -1

        # change DSlices array to be correct permutation/order
        for i in range(1, 4):
            k = coord2 % (i + 1)
            coord2 //= (i + 1)
            while k > 0:
                rotate_right(DSlices, 0, i)
                k -= 1

        # set D-Slice edges
        k = 4
        for i in Ed:
            if coord1 - comb(11 - i, k) >= 0:
                self.ec[i] = DSlices[4 - k]
                coord1 -= comb(11 - i, k)
                k -= 1

        # set other edges
        j = 0
        for i in Ed:
            if self.ec[i] == -1:
                self.ec[i] == otherSlices[j]
                j += 1

        # reverse rotation
        for j in range(4):
            rotate_left(self.ec, 0, 11)

    def get_corners(self):
        ''' Get the permutation of the 8 corners.
        0 <= corners < 40320 defined but unused in phase 1,
        0 <= corners < 40320 in phase 2,
        corners = 0 for solved cube

        Again, Different from documentation
        '''

        cp = list(self.cc)
        coord = 0
        for i in range(Co.DRB, Co.URF, -1):
            k = 0
            while cp[i] != i:
                rotate_left(cp, 0, i)
                k += 1
            coord = (i + 1) * coord + k
        return coord

    def set_corners(self, coord):
        ''' decode coord and apply the corner permutation to
        class cube
        '''

        self.cp = list(range(Co.URF, Co.DRB + 1))
        for i in Co:
            k = coord % (i + 1)
            coord //= i + 1
            while k > 0:
                rotate_right(self.cp, 0, i)
                k -= 1

    def get_ud_edges(self):
        ''' Get the permutation of the 8 U and D edges.
        ud_edges undefined in phase 1 !!
        0 <= ud_edges < 40320 in phase 2
        ud_edges = 0 for solved cube.

        this assumes the UDSlice edges are in right locations
        so automatically the first 8 of self.ec are the U & D
        Slices. If that doesn't work this will loop endlessly.
        '''

        ec = self.ec[0:8]
        coord = 0
        for i in range(Ed.DB, Ed.UR, -1):
            k = 0
            while ec[i] != i:
                rotate_left(ec, 0, i)
                k += 1
            coord = (i + 1) * coord + k
        return coord

    def set_ud_edges(self, coord):
        ''' Set U & D edges acording to coord

        first fill positions in numerical order
        then apply rotations we get from coord
        '''

        for i in range(Ed.UR, Ed.DB + 1):
            self.ec[i] = i

        for i in range(Ed.UR, Ed.DB + 1):
            k = coord % (i + 1)
            coord //= i + 1
            while k > 0:
                rotate_right(self.ec, 0, i)
                k -= 1

#  other

    def verify(self):
        ''' check if cubie is a valid cube.
        return true if valid.
        return error str if False'''

        edges = [0] * 12
        corners = [0] * 8

        # check edge permutation
        for i in Ed:
            edges[self.ec[i]] += 1
        for i in Ed:
            if edges[i] != 1:
                return 'Error: Edge Permutation issue.'

        # check edge orientation
        ori = 0
        for i in Ed:
            ori += self.eo[i]
        if ori % 2 != 0:
            return 'Error: Edge Flip|Orientation issue.'

        # check corner permutation
        for i in Co:
            corners[self.cc[i]] += 1
        for i in Co:
            if corners[i] != 1:
                return 'Error: Corner Permutation issue.'

        # check corner orientation
        ori = 0
        for i in Co:
            ori += self.co[i]
        if ori % 3 != 0:
            return 'Error: Corner Twist|Orientation issue.'

        # check parity
        if self.corner_parity() != self.edge_parity():
            return 'Error: Edge and Corner Parities not equal.'

        return True



basic_move_cubies = [CubieCube()] * 6
basic_move_cubies[Color.U] = CubieCube(defs.U_cc, defs.U_co, defs.U_ec, defs.U_eo)
basic_move_cubies[Color.R] = CubieCube(defs.R_cc, defs.R_co, defs.R_ec, defs.R_eo)
basic_move_cubies[Color.F] = CubieCube(defs.F_cc, defs.F_co, defs.F_ec, defs.F_eo)
basic_move_cubies[Color.D] = CubieCube(defs.D_cc, defs.D_co, defs.D_ec, defs.D_eo)
basic_move_cubies[Color.L] = CubieCube(defs.L_cc, defs.L_co, defs.L_ec, defs.L_eo)
basic_move_cubies[Color.B] = CubieCube(defs.B_cc, defs.B_co, defs.B_ec, defs.B_eo)


# 3 * 6 = 18 every basic move can be done 3 times
all_move_cube = [CubieCube()] * 18
for i in Color:
    cubi = CubieCube()
    for j in range(3):
        cubi.multiply(basic_move_cubies[i])
        all_move_cube[3 * i + j] = CubieCube(cubi.cc, cubi.co, cubi.ec, cubi.eo)