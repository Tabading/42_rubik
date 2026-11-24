
from os import path, mkdir
import array as ar
import architecture.CubieCube as cc
from architecture.enums import Constants as Const, Color, FOLDER
import architecture.defs as defs
cubi = cc.CubieCube()

if not path.exists(FOLDER):
    mkdir(FOLDER)

# Move_Twist
fname = "corner_twist_table"
size = Const.MAX_TWIST_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    twist = ar.array('H', [0] * size)
    for i in range(Const.MAX_TWIST_PHASE1):
        cubi.set_twist(i)  # sets cube state for all 2187 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.corner_multiply(defs.basic_move_cubies[j])
                twist[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_twist()
            cubi.corner_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    twist.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    twist = ar.array('H')
    twist.fromfile(file, size)
file.close()


# Move_Flip
fname = "edge_flip_table"
size = Const.MAX_FLIP_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    flip = ar.array('H', [0] * size)
    for i in range(Const.MAX_FLIP_PHASE1):
        cubi.set_flip(i)  # sets cube state for all 2048 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.edge_multiply(defs.basic_move_cubies[j])
                flip[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_flip()
            cubi.edge_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    flip.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    flip = ar.array('H')
    flip.fromfile(file, size)
file.close()

# Move_Slice_Sorted
fname = "slice_sorted_table"
size = Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    ss = ar.array('H', [0] * size)
    for i in range(Const.MAX_SLICE_SORTED_PHASE1):
        cubi.set_slice_sorted(i)  # sets cube state for all 11880 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.edge_multiply(defs.basic_move_cubies[j])
                ss[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_slice_sorted()
            cubi.edge_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    ss.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    ss = ar.array('H')
    ss.fromfile(file, size)
file.close()

# Move_U_Edges
fname = "u_edge_table"
size = Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    ss = ar.array('H', [0] * size)
    for i in range(Const.MAX_SLICE_SORTED_PHASE1):
        cubi.set_u_edges(i)  # sets cube state for all 11880 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.edge_multiply(defs.basic_move_cubies[j])
                ss[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_u_edges()
            cubi.edge_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    ss.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    ss = ar.array('H')
    ss.fromfile(file, size)
file.close()

# Move_D_Edges
fname = "d_edge_table"
size = Const.MAX_SLICE_SORTED_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    ss = ar.array('H', [0] * size)
    for i in range(Const.MAX_SLICE_SORTED_PHASE1):
        cubi.set_d_edges(i)  # sets cube state for all 11880 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.edge_multiply(defs.basic_move_cubies[j])
                ss[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_d_edges()
            cubi.edge_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    ss.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    ss = ar.array('H')
    ss.fromfile(file, size)
file.close()

# Move_UD_Edges
fname = "phase2_ud_edge_table"
size = Const.MAX_UD_EDGES_PHASE2 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    ss = ar.array('H', [0] * size)
    for i in range(Const.MAX_UD_EDGES_PHASE2):
        cubi.set_ud_edges(i)  # sets cube state for all 40320 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.edge_multiply(defs.basic_move_cubies[j])
                ss[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_ud_edges()
            cubi.edge_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    ss.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    ss = ar.array('H')
    ss.fromfile(file, size)
file.close()

# Phase2_Edgemerge from coord.py



# Move_Corners
fname = "phase2_corner_perm_table"
size = Const.MAX_CORNERS_PHASE2 * Const.MAX_MOVE
if not path.isfile(path.join(FOLDER, fname)):
    print("create " + fname + " ...")
    ss = ar.array('H', [0] * size)
    for i in range(Const.MAX_CORNERS_PHASE2):
        cubi.set_corners(i)  # sets cube state for all 40320 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.corner_multiply(defs.basic_move_cubies[j])
                ss[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_corners()
            cubi.corner_multiply(defs.basic_move_cubies[j])
    file = open(path.join(FOLDER, fname), 'wb')
    ss.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(FOLDER, fname), 'rb')
    ss = ar.array('H')
    ss.fromfile(file, size)
file.close()

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
