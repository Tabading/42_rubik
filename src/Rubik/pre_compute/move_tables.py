
from os import path, mkdir
import array as ar
import architecture.CubieCube as cc
from architecture.enums import Constants as Const, Color, FOLDER
import architecture.defs as defs

if not path.exists(FOLDER):
    mkdir(FOLDER)

cubi = cc.CubieCube()


# maybe add progess
def create_table(fname, size, coord_amt, set_func, get_func, mult_func, phase2=False):
    if not path.isfile(path.join(FOLDER, fname)):
        print("create " + fname + " ...")
        table = ar.array('H', [0] * size)
        for i in range(coord_amt):
            if (i + 1) % 200 == 0:
                print('.', end='', flush=True)
            if (i + 1) % 16000 == 0:
                print('')
            set_func(i)  # sets cube state for all possibilities
            for j in Color:  # 6 possible moves URFLDB
                for k in range(3):  # 3 times per move
                    mult_func(defs.basic_move_cubies[j])
                    # only R2, F2, L2 and B2 in phase 2
                    if phase2 and j in [Color.R, Color.F, Color.L, Color.B] and k != 1:
                        continue
                    table[Const.MAX_MOVE * i + 3 * j + k] = get_func()
                mult_func(defs.basic_move_cubies[j])
        file = open(path.join(FOLDER, fname), 'wb')
        table.tofile(file)
        print()
    else:
        print("load " + fname + " ...")
        file = open(path.join(FOLDER, fname), 'rb')
        table = ar.array('H')
        table.fromfile(file, size)
    file.close()
    return table


# Move_Twist
corner_twist = create_table(
    "corner_twist_table",
    Const.MAX_TWIST_PHASE1 * Const.MAX_MOVE,
    Const.MAX_TWIST_PHASE1,
    cubi.set_twist,
    cubi.get_twist,
    cubi.corner_multiply
)


# Move_Flip
edge_flip = create_table(
    "edge_flip_table",
    Const.MAX_FLIP_PHASE1 * Const.MAX_MOVE,
    Const.MAX_FLIP_PHASE1,
    cubi.set_flip,
    cubi.get_flip,
    cubi.edge_multiply
)


# Move_Slice_Sorted
slice_sorted = create_table(
    "slice_sorted_table",
    Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE,
    Const.MAX_SLICE_SORTED_PHASE1,
    cubi.set_slice_sorted,
    cubi.get_slice_sorted,
    cubi.edge_multiply
)


# Move_U_Edges
u_edge = create_table(
    "u_edge_table",
    Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE,
    Const.MAX_SLICE_SORTED_PHASE1,
    cubi.set_u_edges,
    cubi.get_u_edges,
    cubi.edge_multiply
)


# Move_D_Edges
d_edge = create_table(
    "d_edge_table",
    Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE,
    Const.MAX_SLICE_SORTED_PHASE1,
    cubi.set_d_edges,
    cubi.get_d_edges,
    cubi.edge_multiply
)


# Move_UD_Edges
ud_edge = create_table(
    "phase2_ud_edge_table",
    Const.MAX_UD_EDGES_PHASE2 * Const.MAX_MOVE,
    Const.MAX_UD_EDGES_PHASE2,
    cubi.set_ud_edges,
    cubi.get_ud_edges,
    cubi.edge_multiply,
    True
)


# Phase2_Edgemerge from coord.py



# Move_Corners
corner_perm = create_table(
    "phase2_corner_perm_table",
    Const.MAX_CORNERS_PHASE2 * Const.MAX_MOVE,
    Const.MAX_CORNERS_PHASE2,
    cubi.set_corners,
    cubi.get_corners,
    cubi.corner_multiply
)


# -------------------------------------------------------


def files_equal(file1, file2):
    ''' tester function, compares 2 binary files, used to check valid
    generation of the move tables
    '''

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            b1 = f1.read(4096)
            b2 = f2.read(4096)

            if b1 != b2:
                return False

            if not b1:
                return True


if __name__ == "__main__":
    print(files_equal("../../twophase/move_twist",
                      "move_tables/corner_twist_table"))
    print(files_equal("../../twophase/move_flip",
                      "move_tables/edge_flip_table"))
    print(files_equal("../../twophase/move_slice_sorted",
                      "move_tables/slice_sorted_table"))
    
    print(files_equal("../../twophase/move_u_edges",
                      "move_tables/u_edge_table"))
    print(files_equal("../../twophase/move_d_edges",
                      "move_tables/d_edge_table"))
    print(files_equal("../../twophase/move_ud_edges",
                      "move_tables/phase2_ud_edge_table"))
    print(files_equal("../../twophase/move_corners",
                      "move_tables/phase2_corner_perm_table"))
