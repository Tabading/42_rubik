
# step 1 create CubieCube so i can start on the percompute of the tables
from enums import Corner as Co, Edge as Ed

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
        '''

        if co_per is None:
            self.co_per = [Co(i) for i in range(8)]
        else:
            self.co_per = co_per[:]
        if co_ori is None:
            self.co_ori = [0] * 8
        else:
            self.co_ori = co_ori[:]

        if ed_per is None:
            self.ed_per = [Ed(i) for i in range(12)]
        else:
            self.ed_per = ed_per[:]
        if ed_ori is None:
            self.ed_ori = [0] * 12
        else:
            self.ed_ori = ed_ori[:]

#  math

    def corner_multiply(self, b):
        ''' (self * B).co_per[x] = self.co_per[ B.co_per[x] ]
            (self * B).co_ori[x] = self.co_ori[ B.co_per[x] ] + B.co_ori[x]
        '''
        cp = [0] * 8
        co = [0] * 8
        ori = 0
        for i in Co:
            cp = self.co_per[b.co_per[i]]
            ori_self = self.co_ori[b.co_per[i]]
            ori_b = b.co_ori[i]
            




    def edge_multiply():
        pass

    def multiply():
        pass

#  getter setter

    def get_twist():
        '''twist = Corner orientation'''
        pass

    def set_twist():
        pass

    def get_flip():
        '''flip = Edge orientation'''
        pass

    def set_flip():
        pass

    def get_slice():
        '''slice = UDSlice orientation'''
        pass

    def set_slice():
        pass

    def get_slice_sorted():
        '''slice_sorted = UDSlice orientation + order'''
        pass

    def set_slice_sorted():
        pass

    def get_u_edges():
        ''''''
        pass

    def set_u_edges():
        pass

    def get_d_edges():
        ''''''
        pass

    def set_d_edges():
        pass

    def get_corners():
        ''''''
        pass

    def set_corners():
        pass

    def get_ud_edges():
        ''''''
        pass

    def set_ud_edges():
        pass

#  other

    def verify():
        pass
