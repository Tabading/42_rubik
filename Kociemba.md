
# Table of Contents
- [Kociemba Two-Phase-Algorithm](#kociemba-two-phase-algorithm)
- [Phase 1](#phase-1)
    - [(x, y, z) Coordinates Phase 1](#x-y-z-coordinates-phase-1)
        - [x Corner Orientation Coordinate](#x-corner-orientation-coordinate)
        - [y Edge Orientation Coordinate](#y-edge-orientation-coordinate)
        - [z UDSlice Coordinate](#z-udslice-coordinate)
- [Notes](#notes)
    - [EO Edge Orientation](#eo-edge-orientation)
        - [Natural / Unnatural Moves](#natural-/-unnatural-moves)
        - [Orbits](#orbits)
    - [Corner Orientation](#corner-orientation)
    - [Resources](#resources)

# Kociemba Two-Phase-Algorithm
Kociemba's two-phase algorithm quickly finds a reasonably short suboptimal solution. A randomly scrambled cube would be typically solved in a ***fraction of a second in 20 moves or less***, but without any guarantee that the solution found is optimal. it is split in 2 Phases: 
- Phase 1: Orient all Edges and Corners correctly, so the cube can be solved using only 180° rotations of the sides (R2, L2, F2, B2) and U/D 
- Phase 2: solve the cube

# Phase 1
Look for maneuvers which transform a scrambled cube to a G1 state. G1 Describes a subset of cube states that have Corners and Edges Oriented correctly. To do that efficently the cube state is described with 3 coordinates: (x, y, z). x is the Corner orientation Coordinate, y is the Edge orientation Coordinate, z is the UDSlice Coordinate. All G1 cube states have (0, 0, 0) as their coordinates.

## (x, y, z) Coordinates Phase 1
In Phase 1 x, y and z are as described below. All coordinates are needed information, but functionally Edge orientation and UDSlice coordinates are combined and reduced through symmetry reduction.

### x Corner Orientation Coordinate
The orientation of the 8 corners are described by a number from 0 to 2186 (3^7 - 1). Going by Corner Order URF, UFL, ULB, UBR, DFR, DLF, DBL, (DRB), do the following:

    s = 0
    n = 6
    for Corner:
        s += Corner.o * 3^n
        n--
    
    essentialy URF.o*3^6 + UFL.o*3^5 etc.
    DRB is ignored in the calculation.

    ! This ONLY works with the 'is replaced by' representation.

### y Edge Orientation Coordinate
The orientation of the 12 edges is described by a number from 0 to 2047 (2^11 - 1). Going by Edge Order of UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, (BR), the orientation numbers of 0 and 1 make up a binary number, which turned into decimal is our coordinate. This can be easily done like this:

    s = 0
    for edge:
        s = 2 * s + edge.o

    BR is ignored.

### z UDSlice Coordinate
The UDSlice coordinate is number from 0 to 494 (12*11*10*9/4! - 1) which is determined by the positions of the 4 UDSlice edges. The order of the 4 UDSlice edges within the positions is ignored.

Take all 12 Edges, number them from 0 - 11, and check where the 4 UD Edges are. \
Imagine it like this with x being a UDSlice:

    Position n  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 
    Edge        | UR | UF | UL | UB | DR | DF | DL | DB | FR | FL | BL | BR | 
    UDSlice     |    |    |    |    |    |    |    |    |  x |  x |  x |  x | 

Starting at 0 go through it with k = -1. Each time you encounter an x k++ up to 3 max (0, 1, 2, 3). If there are non x spaces when k >= 0 take it as a binomial coefficient C(n, k). For example:

    Position n  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 
    Edge        | UR | UF | UL | UB | DR | DF | DL | DB | FR | FL | BL | BR | 
    UDSlice     |    |    |    |  x |    |    |  x |    |    |  x |    |  x | 

    0 - 2 k = -1: no C()
    3 -> k++
    4 - 5 k = 0: C(4, 0), C(5, 0)
    6 -> k++
    7 - 8 k = 1: C(7, 1), C(8, 1)
    9 -> k++
    10 k = 2: C(10, 2)
    11 k++

The Formel to turn this binomial coefficient into a number:

    C(n, k) = (n!) / ((k!) * (n - k)!)

For Example:

    C(4, 0) = (4!) / ((0!) * (4 - 0)!) = 1
    C(5, 0) = (5!) / ((0!) * (5 - 0)!) = 1

    C(7, 1) = (7!) / ((1!) * (7 - 1)!) = 7
    C(8, 1) = (8!) / ((1!) * (8 - 1)!) = 8

    C(10, 2) = (10!) / ((2!) * (10 - 2)!) = 45

    z = 45 + 8 + 7 + 1 + 1 = 62



# Phase 2
Transforms the cube from a G1 state into a solved one, using only moves of this subgroup, being G1 = <U,D,R2,L2,F2,B2>. Simmilar to phase 1, any cube can be described using 3 coordinates: The corner permutation coordinate (0..40319), the phase 2 edge permutation coordinate (0..40319), and the phase2 UDSlice coordinate (0..23). 

## (x, y, z) Coordinates Phase 20

### Corner permutation Coordinate
The corner permutation coordinate is given by a number from 0 to 40319 (8! - 1). \
Like in Phase 1 the corners have a certain order going:
- URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB. 

URF has low value, DRB high. Each corner gets a number depending on how many corners LEFT of their position in the order, are higher value. \
Take this example for the R-move:

    Order       | URF | UFL | ULB | UBR | DFR | DLF | DBL | DRB |
    Corner c.   | DFR | UFL | ULB | URF | DRB | DLF | DBL | UBR |
    number      |  0  |  1  |  1  |  3  |  0  |  1  |  1  |  4  |

    c:UBR -> DFR, DLF, DBL, DRB are higher value, all left of current position -> 4
    c:DBL -> DRB is higher, left of position -> 1
    c:DLF -> DBL, DRB higher, only DRB left of position -> 1
    c:DRB -> highest -> 0
    c:URF -> lowets, has 3 to the left -> 3
    c:ULB -> UBR, DFR, DLF, DBL, DRB higher, only DFR to the left -> 1
    c:UFL -> ULB, UBR, DFR, DLF, DBL, DRB higher, only DFR to the left -> 1
    c:DFR -> leftmost -> 0 (always 0 = ignore)

The permutation coordinate is made from these numbers, like so:

    1*1! + 1*2! + 3*3! + 0*4! + 1*5! + 1*6! + 4*7! = 21021
    (number*1! + number*2! ...)


### Edge permutation Coordinate
The edge permutation coordinate is described in an analogous way by a number from 0 to 12! - 1. \
It's created like the corner permutation coordinate, using the order:
- UR, UF, UL, UB
- DR, DF, DL, DB
- FR, FL, BL, BR
Take this example for the R-move:

    Order       | UR | UF | UL | UB | DR | DF | DL | DB | FR | FL | BL | BR |
    Edge e.     | FR | UF | UL | UB | BR | DF | DL | DB | DR | FL | BL | UR |
    number      |  0 |  1 |  1 |  1 |  0 |  2 |  2 |  2 |  5 |  1 |  1 | 11 |

    1*1! + 1*2! + 1*3! + 0*4! + 2*5! + 2*6! + 2*7! + 5*8! + 1*9! + 1*10! + 11*11! = 443289849



### Phase 2 UDSlice Coordinate
The phase 2 UDSlice coordinate should have a range from 0..23 because it represents the 4! permutations of the UDSlice edges in their slice. But we use an extension of the UDSlice coordinate instead, which is used in the huge optimal solver anyway and where we also regard the order of the four edges.

IE: See the UDSlice coordinate, it can be 0 (G1 state) despite the edges not being orderd correctly. They are numbererd 8 9 10 11. For this go through and find their current order, for example 10 8 9 11 or smth. Then going backwards check how many edges to the left have a higher number.

    array = [10, 8, 9, 11]
    x = 0

    for (j = 3, 3 >= 1, j--)
        s = 0
        for (k = j - 1, k >= 0, k--)
            if (array[k] > array[j])
                s++
        x = (x + s) * j

for example:

    array = [10, 8, 9, 11]
    
    11 has no bigger bums to the left
    x = (0 + 0) * 3
    x = 0

    9 has 1 bigger
    x = (0 + 1) * 2
    x = 2

    8 has 1 bigger
    x = (2 + 1) * 1
    x = 3

    so the coordinate would be 3

another example:

    array = [11, 10, 9, 8]
    x = (0 + 3) * 3 = 9
    (9 + 2) * 2 = 22
    (22 + 1) * 1 = 23


# Notes

## Permutations
Applying a move to a cube state rearanges the facelets/stickers. That rearangement is called a Permutation. \
Ex: \
F = 

| Position | URF | UFL | ULB | UBR | DFR | DLF | DBL | DRB |
|---|---|---|---|---|---|---|---|---|
| Replaced by | c:UFL; o:1 | c:DLF; o:2 | c:ULB; o:0 | c:UBR; o:0 | c:URF; o:2 | c:DFR; o:1 | c:DBL; o:0 | c:DRB; o:0 |


In this case the corner URF is replaced by the corner currently at UFL adding +1 to its orientation, etc.

There's 2 ways of representing changes like this, "is replaced by" & "is carried to". Unless specified otherwise the algorithm uses the "is replaced by" representation.

## EO Edge Orientation 
If the Edge is oriented in a way that it can be brought into position using only natural moves it's a good edge. To recognize if that's the case you need to know about the 2 'edge orbits'. This only works if what you consider Up and Front stays the same, so don't change perspective. From here there's 2 Rules for finding the Edges easily:
- Rule 1: look for L and R stickers on orbit 1. Their edges are bad.
- Rule 2: Look for U and D stickers on orbit 2. Their edges are bad.


### Natural / Unnatural Moves
The 6 basic moves:
- R ight
- U p
- L eft
- D own
- F ront
- B ack

can be seperated into 2 groups:
- Natural moves: All R, U, L, and D moves. Let’s call them “natural” because they’re fast and comfortable for your hands.
- Unnatural moves: All F and B moves. Let’s call them “unnatural” because they’re more awkward (unless in specific hand positions).


### Orbits
A Rubik has 2 Orbits, with each edge side belonging to one or the other. Following a sticker when using only natural moves, you can see it only moves on that orbit.
- The Up / Down Edges belong to orbit 1
- The Right / Left Edges belong to orbit 2
- The Front / Back Edges are opposite from their UD RL connection, speak top/bottom layer edges are orbit 2, middle layer edges orbit 1

For better visual look at https://www.zzmethod.com/tutorial/eo.


## Corner Orientation
For this Algorithm, a Corner is oriented when the U/D facing stickers are either U or D collored. Kociemba gives each Corner a orientation number o:(0, 1 or 2), to describe their state:
- 0 = Oriented
- 1 = clockwise twist
- 2 = counter clockwise twist

That doesn't make much sense. Just accept they exist and that 0 is the goal. \
Each possible move has a table describing how corner c and orientation o change with it. Here is an example for F:

F = 

| Position | URF | UFL | ULB | UBR | DFR | DLF | DBL | DRB |
|---|---|---|---|---|---|---|---|---|
| Replaced by | c:UFL; o:1 | c:DLF; o:2 | c:ULB; o:0 | c:UBR; o:0 | c:URF; o:2 | c:DFR; o:1 | c:DBL; o:0 | c:DRB; o:0 |

- Note that corners moving between U and D are +2 and the rest that's affected +1.

This looks worse than it is. \
Imagine we have a cube-state-object that for each position (URF, UFL etc) has .c = corner currently here, and .o it's current orientation.
Taking the first Position as example, on move F position URF.c is replaced by UFL.c, UFL.o getting +1 added.

Now .o can still only be 0, 1, 2, so how does that work after multiple moves? .c and .o can be calculated through 2 formula: 

    (A * B)(x).c = A(B(x).c).c
    (A * B)(x).o = A(B(x).c).o + B(x).o

Think of the variables like this:
- A = Current State (bsp: scrabled cube currently has ULB.c = DBL ULB.o = 2)
- B = Move to apply (table contents)
- x = Position for which to calculate

Lets do an example with F * L. (F used as current state here for simplicety). \
calculate x = DLF:

    (A * B)(x).c = A(B(x).c).c
    (F * L)(DLF).c = F(L(DLF).c).c
    (F * L)(DLF).c = F(UFL).c
    (F * L)(DLF).c = DLF

    (A * B)(x).o = A(B(x).c).o + B(x).o
    (F * L)(DLF).o = F(L(DLF).c).o + L(DLF).o
    (F * L)(DLF).o = F(UFL).o + 2
    (F * L)(DLF).o = 2 + 2
    (F * L)(DLF).o = 4

    Here is the issue, 4 is invalid orientation.
    What Kociemba doesn't tell you directly is that EACH result is put through mod(3). 
    So take that formular instead as:
        (A * B)(x).o = (A(B(x).c).o + B(x).o) % 3
    
    (F * L)(DLF).o = 4 % 3 = 1

    After F L: DLF.c = DLF, DLF.o = 1
    

## Move Tables
Calculating the result of each move every time isn't very time efficient. Move Tables are simply an array where we save those calculations so they only need to be done once. Each Coordinate has a Move Table where for each possible Coordinate are 18 possible saved move calculations.

Using the Corner orientation as Example:

    array[2186][18]

    for i = 0 <= 2186:
        // create a cube with orientation i
        for 6 moves:
            for 3 variants:
                // apply move to cube and save result inside array[i][]

If this Table / result is saved outside runtime in a file or something, it can be loaded by the programme.


## Equivalent Cubes & Symetry
When 2 Cubes are Equivalent they take the same number of moves to solve. Each Cube state has 48 equivalent cubes, through symetry & reflektions. These 48 symetries are generated by 4 "basic" symetries:

- S_URF3: 120* turn around the axis through URF and DBL. (turn R to F then U to R)
- S_F2:   180* turn around the axis through F & B center. (turn U to D -> L & R switch too)
- S_U4:   90* turn araund the axis through U & D center. (turn R to F)
- S_LR2:  reflection of the RL-slice plane. mirror elements (slice the cube in half from the top and mirror along the cut):
    - R & L swap
    - U D F B reflekt onto themselves (left right halves mirrored)

These 4 basic symmetries have Permutations for Edges & Corners each. 

Any of the 48 symmetries is uniquely generated by the product

    (S_URF3)^x1 * (S_F2)^x2 * (S_U4)^x3 * (S_LR2)^x4

Here we have (x1,x2,x3,x4) where:
- x1 from 0..2 
- x2 from 0..1 
- x3 from 0..3 
- x4 from 0..1 

This tuple is mapped to a number 0..47 by:

    16*x1 + 8*x2 + 2*x3 + x4

Like this the touple gives each Symetry an Index i:
    
    16*0 + 8*0 + 2*0 + 0 = 0
    16*0 + 8*0 + 2*0 + 1 = 1
    16*0 + 8*0 + 2*1 + 0 = 2
    16*0 + 8*0 + 2*1 + 1 = 3
    16*0 + 8*0 + 2*2 + 0 = 4
    16*0 + 8*0 + 2*2 + 1 = 5
    16*0 + 8*0 + 2*3 + 0 = 6
    16*0 + 8*0 + 2*3 + 1 = 7
    16*0 + 8*1 + 2*0 + 0 = 8
    etc...

So you basically create a move table CornerSym, EdgeSym, CentSym with indexes 0..47 and depending on the x values use the specific S_() permutations. for ex:

    16*0 + 8*0 + 2*0 + 0 = 0 -> no changes
    16*0 + 8*0 + 2*0 + 1 = 1 -> do 1 (S_LR2)
    16*0 + 8*0 + 2*2 + 0 = 4 -> do 2 (S_U4)
    16*0 + 8*0 + 2*3 + 1 = 7 -> do 3 (S_U4) + 1 (S_LR2)
    16*0 + 8*1 + 2*0 + 0 = 8 -> do 1 (S_F2)
    etc..

For Inversing the Symmetry[i] you find a different one that reverses it. After creating the other Symetries go through all 48 and check which symmetry can reverse it. \
ex:

    for j in range(48):
        for k in range(48):
            c = CornMult(CornSym[j], CornSym[k]) // corner orientation math ( (A * B)(x).c = A(B(x).c).c )

            if ( // check if correctly oriented
                c[URF].c == URF
                and c[UFL].c == UFL
                and c[ULB].c == ULB
            ):
                InvIdx[j] = k // j is undone by k
                break

Two cubes with the permutations A and B are only equivalent if there is an i with

    S(i)^-1 * A * S(i) = B

    -1 means do the reverse

## A mathematical view of Coordinates: Cosets (Subgroups)
Ok, remember all the coordinates this algorythm uses? They're used to create subgroups and cosets. \
We have a subgroup for all diffrent types of coordinates:

| Subgroup of G | Coset coordinate | Used in |
|---|---:|---|
| Corner orientation = 0 | 0–2186 | Phase 1 |
| Edge orientation = 0 | 0–2047 | Phase 1 |
| UDSlice = 0 | 0–494 | Phase 1 |
| FlipUDSlice = 0 | 0–494 × 2048 − 1 | Phase 1 (combines the above two) |
| Corner permutation = 0 | 0–40319 | Phase 2 |
| (UD face) edge permutation = 0 | 0–40319 (8! − 1) | Phase 2 (only edges not in UDSlice) |
| UDSliceSort = 0 | 0–11879 | Phase 2 (in Phase 2, only uses 0–23) |


So we get a subgroup H (called diffrent in explanation) with a bunch of cosets for each coordinate type. The H is always for coordinate 0, after that there's a coset for each coordinate. \
Think of 2 randomly scrambled cubes, those cubes might have the same Corner Orientation coordinate despite having diffrences in the other coordinates. Both of those cubes would belong to the same corner orientation coset; The one corresponding to their coordinate.

### Subgroup example
Subgroup C0 (Corner orientation coordinate).

    C0 = { g from G with g(x).o = 0 for all corners x}
    C0 is made up from all g (permutations) inside G (ALL Permutations used for coordinates) where corner orientation is = 0 for all Corners x.

The right cosets are defined by:

    C0*g = {a*g | a from C0}

    C0*g:   coset (there's 1 for all 0..2186 corner orientation coordinates)
    C0:     subgroup with many permutations where .o = 0 for all corners
    a:      element from C0, 1 permutation with .o = 0 for all corners
    g:      element from G, any possible permutation? maybe

The multiplication C0*g is solved like any two permutations:

    (a*g)(x).o = a(g(x).c).o + g(x).o 

But since all orientations .o from a (C0) are 0, this can be simplefied to:
    
    = 0 + g(x).o 
    = g(x).o

So all elements of the coset C0\*g have the same corner orientations (defined by the permutation g) and all elements of C0\*g have the same corner orientation coordinate. And if on the other hand two permutations have the same corner orientation coordinate, they are in the same coset. The formal proof is a bit more lengthy.


### Formal proof
If permutations a & b have the same corner orientation coordinate, a(x).o = b(x).o for all corners x is true.

    cb:=b^-1(x).c 
    ob:=b^-1(x).o

    cb = inverse b .c
    ob = inverse b .o

    (corner x is replaced by corner cb and the orientation of cb is increased by ob when put into position x) .

    b(cb).c = x 
    b(cb).o = -ob

    (b is the inverse of b^-1 (cb), so corner cb is replaced by corner x and the orientation of x is decreased by ob when put in position cb).

a and b are in the same coset of C0 if and only if a*b^-1 is in C0. Now we have for all corners x

    (a*b^-1)(x).o   = a(b^-1(x).c).o + b^-1(x).o 
                    = a(cb).o + ob                  // corners a & b should be the same
                    = b(cb).o + ob                  // switched since we have  b(cb).o = -ob, but not  a(cb).o = -ob
                    = -ob + ob 
                    = 0 (which was to be demonstrated)

### Cosets (basics)
we have a group G with a subgroup H. H is a coset already but doesn't contain all elements of G. That's where cosets come in: we get a right/left factor g (Hg / gH), thats added/multiplied with H.\
Take this exmple:

    G       = {0, 1, 2, 3, 4, 5}

    H       = {0, 3} | subgroup & coset(right & left)
    1 + H   = {1, 4} | coset (left)
    2 + H   = {2, 5} | coset (left)

There's also an Index of H in G: [G:H]


## Coordinates and Symmetry
Cordinates represent cosets, each coset usually consists of many permutations. \
If you move the whole cube and recolor it or you do a conjugation with a symmetry S(i) as explained in "Equivalent Cubes & Symetry" , the coordinates usually change.

You must be careful if you want to map a coordinate by a symmetry conjugation to another coordinate. If you have two different permutations P and Q in a coset, S(i)-1\*P\*S(i) and S(i)-1\*Q\*S(i) always have to be in the same coset, else you cannot do this mapping nor can you define equivalent cosets.

This restricts the symmetries which are appliable here. It is not difficult to show that exactly those symmetries S(i) are appliable, for which the subgroup H which defines the cosets has the property S(i)-1\*H\*S(i) = H.


| Coordinate | Full symmetry group (48 elements) | Subgroup generated by S_F2, S_U4 and S_LR2 (16 elements) | Used in |
|---|---|---|---|
| Corner orientation (twist) | No | Yes | Phase 1, optimal solvers |
| Edge orientation (flip) | No* | No* | — |
| UDSlice | No | Yes | — |
| FlipUDSlice | No | Yes | Phase 1, optimal solver, 64,430 equivalence classes |
| Corner permutation | Yes** | Yes | Phase 2, 2,768 equivalence classes |
| Phase 2 edge permutation | No | Yes | Phase 2 |
| UDSliceSorted coordinate | No | Yes | Huge optimal solver, 788 equivalence classes |

*It is possible to give another definition for the edge-orientations, so that the full symmetry group can be used with the edge orientation coordinate. But we prefer the usual definition which is better suited for the two-phase algorithm.
**Not used in Cube Explorer


# Resources

- https://www.youtube.com/watch?v=RPXcIUnKvQ8
- https://www.zzmethod.com/tutorial/eo
- https://kociemba.org/math/CubeDefs.htm#cornfaceturns
- https://kociemba.org/cube.htm
- https://en.wikipedia.org/wiki/Iterative_deepening_A*
- https://en.wikipedia.org/wiki/Coset
