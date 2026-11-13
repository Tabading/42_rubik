
# assign int numbers to the various cube possitions
# corners edges facelets etc
# IntEnum needed for checking order with <>.

from enum import IntEnum


class Constants(IntEnum):
    FOLDER = "move_tables"
    MAX_MOVE = 18
    MAX_SYM = 48
    MAX_UDSLICE_PERM = 24  # 24 possible permutations for UDSlice edges

    MAX_TWIST_PHASE1 = 2187  # 3^7 possible corner orientations in phase 1
    MAX_FLIP_PHASE1 = 2048  # 2^11 possible edge orientations in phase 1
    MAX_SLICE_SORTED_PHASE1 = 11880  # 12*11*10*9 possible positions  in phase1
    MAX_SLICE_PHASE1 = 495  # also MAX_SLICE_SORTED // MAX_UDSLICE_PERM

    MAX_U_EDGES_PHASE2 = 1680  # 1680 for solved
    MAX_CORNERS_PHASE2 = 40320  # 8! corner permutations in phase 2
    MAX_UD_EDGES_PHASE2 = 40320  # 8! edge permutations in the U & D in phase 2


class Color(IntEnum):
    U = 0
    R = 1
    F = 2
    D = 3
    L = 4
    B = 5


class Corner(IntEnum):
    ''' The 8 Corner Positions in Order. '''

    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3

    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7


class Edge(IntEnum):
    ''' The 12 Edge Positions in Order.
    U-edges (up)
    D-edges (down)
    UD-Slice edges (middle) '''

    UR = 0
    UF = 1
    UL = 2
    UB = 3

    DR = 4
    DF = 5
    DL = 6
    DB = 7

    FR = 8
    FL = 9
    BL = 10
    BR = 11


class Move(IntEnum):
    ''' All 18 possible moves .
    3 is the same as doing the backwards move.
    https://cube-solver.com/ to see how the moves look on a cube. '''

    U1 = 0
    U2 = 1
    U3 = 2

    R1 = 3
    R2 = 4
    R3 = 5

    F1 = 6
    F2 = 7
    F3 = 8

    D1 = 9
    D2 = 10
    D3 = 11

    L1 = 12
    L2 = 13
    L3 = 14

    B1 = 15
    B2 = 16
    B3 = 17


class BasicSymm(IntEnum):
    ''' 4 Basic Symmetries used to create the 48 Cube Symmetries. '''

    S_URF3 = 0
    S_F2 = 1
    S_U4 = 2
    S_LR2 = 3
