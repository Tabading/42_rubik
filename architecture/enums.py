
# assign int numbers to the various cube possitions
# corners edges facelets etc
# IntEnum needed for checking order with <>.

from enum import IntEnum


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
