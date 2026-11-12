
from enums import Corner as Co, Edge as Ed

# Permutation & orientation changes after Move

# U Move
U_cc = [Co.UBR, Co.URF, Co.UFL, Co.ULB, Co.DFR, Co.DLF, Co.DBL, Co.DRB]
U_co = [0, 0, 0, 0, 0, 0, 0, 0]
U_ec = [Ed.UB, Ed.UR, Ed.UF, Ed.UL, Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
U_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# R Move
R_cc = [Co.DFR, Co.UFL, Co.ULB, Co.URF, Co.DRB, Co.DLF, Co.DBL, Co.UBR]
R_co = [2, 0, 0, 1, 1, 0, 0, 2]
R_ec = [Ed.FR, Ed.UF, Ed.UL, Ed.UB, Ed.BR, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FL, Ed.BL, Ed.UR]
R_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# F Move
F_cc = [Co.UFL, Co.DLF, Co.ULB, Co.UBR, Co.URF, Co.DFR, Co.DBL, Co.DRB]
F_co = [1, 2, 0, 0, 2,  1, 0, 0]
F_ec = [Ed.UR, Ed.FL, Ed.UL, Ed.UB, Ed.DR, Ed.FR, Ed.DL, Ed.DB, Ed.UF, Ed.DF, Ed.BL, Ed.BR]
F_eo = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# D Move
D_cc = [Co.URF, Co.UFL, Co.ULB, Co.UBR, Co.DLF, Co.DBL, Co.DRB, Co.DFR]
D_co = [0, 0, 0, 0, 0, 0, 0, 0]
D_ec = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
D_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# L Move
L_cc = [Co.URF, Co.ULB, Co.DBL, Co.UBR, Co.DFR, Co.UFL, Co.DLF, Co.DRB]
L_co = [0, 1, 2, 0, 0, 2, 1, 0]
L_ec = [Ed.UR, Ed.UF, Ed.BL, Ed.UB, Ed.DR, Ed.DF, Ed.FL, Ed.DB, Ed.FR, Ed.UL, Ed.DL, Ed.BR]
L_eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# B Move
B_cc = [Co.URF, Co.UFL, Co.UBR, Co.DRB, Co.DFR, Co.DLF, Co.ULB, Co.DBL]
B_co = [0, 0, 1, 2, 0, 0, 2, 1]
B_ec = [Ed.UR, Ed.UF, Ed.UL, Ed.BR, Ed.DR, Ed.DF, Ed.DL, Ed.BL, Ed.FR, Ed.FL, Ed.UB, Ed.DB]
B_eo = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]


