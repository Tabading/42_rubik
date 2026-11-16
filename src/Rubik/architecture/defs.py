
from enums import Color, Corner as Co, Edge as Ed
from CubieCube import CubieCube

# Permutation & orientation changes after Move

# U Move
U_cc = [Co.UBR, Co.URF, Co.UFL, Co.ULB,
        Co.DFR, Co.DLF, Co.DBL, Co.DRB]
U_co = [0, 0, 0, 0, 0, 0, 0, 0]
U_ec = [Ed.UB, Ed.UR, Ed.UF, Ed.UL,
        Ed.DR, Ed.DF, Ed.DL, Ed.DB,
        Ed.FR, Ed.FL, Ed.BL, Ed.BR]
U_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# R Move
R_cc = [Co.DFR, Co.UFL, Co.ULB, Co.URF,
        Co.DRB, Co.DLF, Co.DBL, Co.UBR]
R_co = [2, 0, 0, 1, 1, 0, 0, 2]
R_ec = [Ed.FR, Ed.UF, Ed.UL, Ed.UB,
        Ed.BR, Ed.DF, Ed.DL, Ed.DB,
        Ed.DR, Ed.FL, Ed.BL, Ed.UR]
R_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# F Move
F_cc = [Co.UFL, Co.DLF, Co.ULB, Co.UBR,
        Co.URF, Co.DFR, Co.DBL, Co.DRB]
F_co = [1, 2, 0, 0, 2,  1, 0, 0]
F_ec = [Ed.UR, Ed.FL, Ed.UL, Ed.UB,
        Ed.DR, Ed.FR, Ed.DL, Ed.DB,
        Ed.UF, Ed.DF, Ed.BL, Ed.BR]
F_eo = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# D Move
D_cc = [Co.URF, Co.UFL, Co.ULB, Co.UBR,
        Co.DLF, Co.DBL, Co.DRB, Co.DFR]
D_co = [0, 0, 0, 0, 0, 0, 0, 0]
D_ec = [Ed.UR, Ed.UF, Ed.UL, Ed.UB,
        Ed.DF, Ed.DL, Ed.DB, Ed.DR,
        Ed.FR, Ed.FL, Ed.BL, Ed.BR]
D_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# L Move
L_cc = [Co.URF, Co.ULB, Co.DBL, Co.UBR,
        Co.DFR, Co.UFL, Co.DLF, Co.DRB]
L_co = [0, 1, 2, 0, 0, 2, 1, 0]
L_ec = [Ed.UR, Ed.UF, Ed.BL, Ed.UB,
        Ed.DR, Ed.DF, Ed.FL, Ed.DB,
        Ed.FR, Ed.UL, Ed.DL, Ed.BR]
L_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# B Move
B_cc = [Co.URF, Co.UFL, Co.UBR, Co.DRB,
        Co.DFR, Co.DLF, Co.ULB, Co.DBL]
B_co = [0, 0, 1, 2, 0, 0, 2, 1]
B_ec = [Ed.UR, Ed.UF, Ed.UL, Ed.BR,
        Ed.DR, Ed.DF, Ed.DL, Ed.BL,
        Ed.FR, Ed.FL, Ed.UB, Ed.DB]
B_eo = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

# basic move array for move_tables

basic_move_cubies = [CubieCube()] * 6
basic_move_cubies[Color.U] = CubieCube(U_cc, U_co, U_ec, U_eo)
basic_move_cubies[Color.R] = CubieCube(R_cc, R_co, R_ec, R_eo)
basic_move_cubies[Color.F] = CubieCube(F_cc, F_co, F_ec, F_eo)
basic_move_cubies[Color.D] = CubieCube(D_cc, D_co, D_ec, D_eo)
basic_move_cubies[Color.L] = CubieCube(L_cc, L_co, L_ec, L_eo)
basic_move_cubies[Color.B] = CubieCube(B_cc, B_co, B_ec, B_eo)

# all move array for symmetry_tables

# 3 * 6 = 18 every basic move can be done 3 times
all_move_cube = [CubieCube()] * 18
for i in Color:
    cubi = CubieCube()
    for j in range(3):
        cubi.multiply(basic_move_cubies[i])
        all_move_cube[3 * i + j] = CubieCube(cubi.cc, cubi.co, cubi.ec, cubi.eo)