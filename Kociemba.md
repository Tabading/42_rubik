
# Table of Contents
- [Description](#description)
    - 

# Kociemba Two-Phase-Algorithm
Kociemba's two-phase algorithm quickly finds a reasonably short suboptimal solution. A randomly scrambled cube would be typically solved in a ***fraction of a second in 20 moves or less***, but without any guarantee that the solution found is optimal. it is split in 2 Phases: \
- Phase 1: Orient all Edges and Corners correctly, so the cube can be solved using only 180° rotations of the sides (R2, L2, F2, B2) and U/D 
- Phase 2: solve the cube

## Description

## Phase 1
Look for maneuvers which transform a scrambled cube to a G1 state. G1 Describes a subset of cube states that have Corners and Edges Oriented correctly. To do that efficently the cube state is described with 3 coordinates: (x, y, z). All G1 cube states have (0, 0, 0) as their coordinates.


## Phase 2


# Notes

## (x, y, z) Coordinates 1
In Phase 1 x, y and z are as follows:

### x Corner Orientation Coordinate
The orientation of the 8 corners are described by a number from 0 to 2186 (3^7 - 1).


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

F = \
Position    | URF       | UFL       | ULB       | UBR       | DFR       | DLF       | DBL       | DRB \
replaced by | c:UFL;o:1 | c:DLF;o:2 | c:ULB;o:0 | c:UBR;o:0 | c:URF;o:2 | c:DFR;o:1 | c:DBL;o:0 | c:DRB,o:0

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
    






- https://www.youtube.com/watch?v=RPXcIUnKvQ8
- https://www.zzmethod.com/tutorial/eo

