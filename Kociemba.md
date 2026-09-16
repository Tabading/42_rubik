
# Table of Contents
- [Description](#description)
    - 

# Kociemba Two-Phase-Algorithm
Kociemba's two-phase algorithm quickly finds a reasonably short suboptimal solution. A randomly scrambled cube would be typically solved in a ***fraction of a second in 20 moves or less***, but without any guarantee that the solution found is optimal. it is split in 2 Phases: \
- Phase 1: Orient all Edges and Corners correctly, so the cube can be solved using only 180° rotations of the sides (R2, L2, F2, B2) and U/D 
- Phase 2: solve the cube

## Description

## Phase 1


## Phase 2


# Notes

## EO Edge Orientation 
If the Edge is oriented in a way that it can be brought into position using only natural moves it's a good edge. To recognize if thats the case you need to know about the 2 'edge orbits'. This only works if what you consider Up and Front stays the same, so don't change perspecktive. From here there's 2 Rules for finding the Edges easily:
- Rule 1: look for L and R stickers on orbit 1. Their edges are bad.
- Rule 2: Look for U and D stickers on orbit 2. Their edges are bad.


### Natural / Unnatural Moves
The 6 basic moves: R, U, L, D, F, B can be seperated into 2 groups:
- Natural moves: All R, U, L, and D moves. Let’s call them “natural” because they’re fast and comfortable for your hands.
- Unnatural moves: All F and B moves. Let’s call them “unnatural” because they’re more awkward (unless in specific hand positions).


### Orbits
A Rubik has 2 Orbits, with each edge side belonging to one or the other. Following a sticker when using only natural moves, you can see it only moves on that orbit.
- The Up / Down Edges belong to orbit 1
- The Right / Left Edges belong to orbit 2
- The Front / Back Edges ore opposite from their UD RL connection, speak top/bottom layer edges are orbit 2, middle layer edges orbit 1

For better visual look at https://www.zzmethod.com/tutorial/eo.


## Corner Orientation
For this Algorithm, a Corner is oriented when the U/D facing stickers are either U or D collored.




- https://www.youtube.com/watch?v=RPXcIUnKvQ8
- https://www.zzmethod.com/tutorial/eo

