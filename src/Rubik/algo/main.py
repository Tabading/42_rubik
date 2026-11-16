import pre_compute.move_tables


# use to compare binary move tables to check if i did it correctly
def files_equal(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            b1 = f1.read(4096)
            b2 = f2.read(4096)

            if b1 != b2:
                return False

            if not b1:
                return True


print(files_equal("twophase/move_twist", "move_tables/corner_twist_table"))
