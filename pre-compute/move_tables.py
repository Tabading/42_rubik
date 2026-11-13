
from os import path
import array as ar
import architecture.CubieCube as cc
from architecture.enums import Constants as Const, Color
import architecture.defs as defs


cubi = cc.CubieCube()
# Move_Twist

fname = "move_twist_table"
size = Const.MAX_TWIST_PHASE1 * Const.MAX_MOVE
if not path.isfile(path.join(Const.FOLDER, fname)):
    print("create " + fname + " ...")
    twist = ar.array('H', [0] * size)
    for i in range(Const.MAX_TWIST_PHASE1):
        cubi.set_twist(i)  # sets cube state for all 2187 possibilities
        for j in Color:  # 6 possible moves URFLDB
            for k in range(3):  # 3 times per move
                cubi.corner_multiply(defs.basic_move_cubies[j])
                twist[Const.MAX_MOVE * i + 3 * j + k] = cubi.get_twist()
            cubi.corner_multiply(defs.basic_move_cubies[j])
    file = open(path.join(Const.FOLDER, fname), 'wb')
    twist.tofile(file)
else:
    print("load " + fname + " ...")
    file = open(path.join(Const.FOLDER, fname), 'rb')
    twist = ar.array('H')
    twist.fromfile(file, size)
file.close()


# Move_Flip
# Move_Slice_Sorted

# Move_U_Edges
# Move_D_Edges
# Move_UD_Edges
# Phase2_Edgemerge

# Move_Corners
