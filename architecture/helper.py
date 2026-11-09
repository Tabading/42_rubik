

def rotate_right():
    pass


def rotate_left():
    pass


# def binomial_coefficient(n, k):
#     if n >= k >= 0:
#         return (factorial(n)) // (factorial(k) * factorial(n - k))
#     else:
#         return 0


def handle_ori_change(o_A, o_B):
    ''' handle the orientation change when multiplying the cubes.

    - a normal cube can have ori 0, 1, 2
    - a mirrored cube can have 3, 4, 5
        - mirrored means it was affected by the S_LR symmetry

    each ori +- 3 is essentially mod(3) but in a way that we can also 
    end up in the mirrored range. '''
    ori = 0
    # 2 normal
    if o_A < 3 and o_B < 3:
        ori = o_A + o_B
        if ori >= 3:
            ori -= 3
    # both results are 3 - 5, so mirrored. order matters, can't be combined
    # A normal, B mirrored
    elif o_A < 3 <= o_B:
        ori = o_A + o_B
        if ori >= 6:
            ori -= 3
    # A mirrored, B normal
    elif o_A >= 3 > o_B:
        ori = o_A - o_B
        if ori < 3:
            ori += 3
    # Both mirrored result normal cube
    elif o_A >= 3 and o_B >= 3:
        ori = o_A - o_B
        if ori < 0:
            ori += 3
    return ori

