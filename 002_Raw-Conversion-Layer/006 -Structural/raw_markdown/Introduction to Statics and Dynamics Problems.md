Introduction to

# STATICS

and

DYNAMICS Problem Book

## Rudra Pratap and Andy Ruina Spring 2001

 c Rudra Pratap and Andy Ruina, 1994-2001. All rights reserved. No part of this book may be reproduced, stored in a retrieval system, or transmitted, in any form or by any means, electronic, mechanical, photocopying, or otherwise, without prior written permission of the authors.

This book is a pre-release version of a book in progress for Oxford University Press.

The following are amongst those who have helped with this book as editors, artists, advisors, or critics: Alexa Barnes, Joseph Burns, Jason Cortell, Ivan Dobrianov, Gabor Domokos, Thu Dong, Gail Fish, John Gibson, Saptarsi Haldar, Dave Heimstra, Theresa Howley, Herbert Hui, Michael Marder, Elaina McCartney, Arthur Ogawa, Kalpana Pratap, Richard Rand, Dane Quinn, Phoebus Rosakis, Les Schae er, David Shipman, Jill Startzell, Saskya van Nouhuys, Bill Zobrist. Mike Coleman worked extensively on the text, wrote many of the examples and homework problems and created many of the mgures. David Ho has brought almost all of the artwork to its present state. Some of the homework problems are modimcations from the Cornell’s Theoretical and Applied Mechanics archives and thus are due to T&AM faculty or their libraries in ways that we do not know how to give proper attribution. Many unlisted friends, colleagues, relatives, students, and anonymous reviewers have also made helpful suggestions.

Software used to prepare this book includes TeXtures, BLUESKY’s implementation of LaTeX, Adobe Illustrator and MATLAB.

Most recent text modimcations on January 21, 2001.

### Contents

- Problems for Chapter 1 . . . . . . . . . . . . . . . . . . . . . . . . . . 0
- Problems for Chapter 2 . . . . . . . . . . . . . . . . . . . . . . . . . . 2
- Problems for Chapter 3 . . . . . . . . . . . . . . . . . . . . . . . . . . 10
- Problems for Chapter 4 . . . . . . . . . . . . . . . . . . . . . . . . . . 15
- Problems for Chapter 5 . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- Problems for Chapter 6 . . . . . . . . . . . . . . . . . . . . . . . . . . 31
- Problems for Chapter 7 . . . . . . . . . . . . . . . . . . . . . . . . . . 41
- Problems for Chapter 8 . . . . . . . . . . . . . . . . . . . . . . . . . . 60
- Problems for Chapter 9 . . . . . . . . . . . . . . . . . . . . . . . . . . 74
- Problems for Chapter 10 . . . . . . . . . . . . . . . . . . . . . . . . . . 83
- Problems for Chapter 11 . . . . . . . . . . . . . . . . . . . . . . . . . . 88
- Problems for Chapter 12 . . . . . . . . . . . . . . . . . . . . . . . . . . 100 Answers to *’d questions


Problems for Chapter 1 1

Introduction to mechanics Because no mathematical skills have been taught so far, the questions below just demonstrate the ideas and vocabulary you should have gained from the reading.

- 1.1 What is mechanics?
- 1.2 Brieﬂy deﬁne each of the words below (using rough English, not precise mathematical language):

- a) Statics,
- b) Dynamics,
- c) Kinematics,
- d) Strength of materials,
- e) Force,
- f) Motion,
- g) Linear momentum,
- h) Angular momentum,
- i) A rigid body.


- 1.3 This chapter says there are three “pillars” of mechanics of which the third is ‘Newton’s’ laws, what are the other two?
- 1.4 This book orgainzes the laws of mechanics into 4 basic laws numberred 0-III, not the standard ‘Newton’s three laws’. What are these four laws (in English, no equations needed)?
- 1.5 Describe, as precisely as possible, a problem that is not mentionned in the book but which is a mechanics problem. State which quantities are given and what is to be determined by the mechanics solution.
- 1.6 Describe an engineering problem which is not a mechanics problem.
- 1.7 About how old are Newton’s laws?
- 1.8 Relativity and quantum mechanics have overthrown Newton’s laws. Why are engineers still using them?
- 1.9Computationispartofmodernengineering.


- a) What are the three primary computer skills you will need for doing problems in this book?
- b) Give examples of each (different thatn the examples given).
- c) (optional) Do an example of each on a computer.


Vector skills for mechanics

##### 2.1 Vector notation and vec-tor addition

- 2.1 Represent the vector r = 5mıˆ − 2mˆ in three different ways.
- 2.2 Whichoneofthefollowingrepresentations of the same vector F is wrong and why?

ıˆ

ˆ

2N 3N -3Nıˆ + 2Nˆ

√13N

√13N

a) b)

c) d)

- 2
- 3


- 2
- 3


problem 2.2:

(Filename:pﬁgure2.vec1.2)

- 2.3 There are exactly two representations that describe the same vector in the following pictures. Match the correct pictures into pairs.

ıˆ

ˆ

a) b)

e) f)

c) d)

30o 30o

4N

- 2N

4N

2√3N

2N(-ıˆ +

√3ˆ)

- 3Nıˆ + 1Nˆ 3N(13ıˆ + ˆ)


problem 2.3:

(Filename:pﬁgure2.vec1.3)

- 2.4 Find the sum of forces F1 = 20Nıˆ − 2Nˆ, F2 = 30N(√12

ıˆ + √12

ˆ), and F3 = −20N(−ıˆ +

√3ˆ).

- 2.5 In the ﬁgure shown below, the position vectors are rAB = 3ftkˆ, rBC = 2ftˆ, and


rCD = 2ft(ˆ + kˆ). Find the position vector rAD.

rBC

- A
- B C


rCD

rAB

D

kˆ

ˆ

###### problem 2.5:

(Filename:pﬁgure2.vec1.5)

- 2.6 The forces acting on a block of mass m = 5kg are shown in the ﬁgure, where F1 = 20N, F2 = 50N, and W = mg. Find the sum F (= F1 + F2 + W)?

- 3
- 4 4


3

W

F1 F2

problem 2.6:

(Filename:pﬁgure2.vec1.6)

- 2.7 Three position vectors are shown in the ﬁgure below. Given that rB/A = 3m(12ıˆ + √3

2 ˆ) and rC/B = 1mıˆ − 2mˆ, ﬁnd rA/C.

ıˆ

ˆ

A

B

C

problem 2.7:

(Filename:pﬁgure2.vec1.7)

- 2.8 Given that the sum of four vectors Fi,i = 1 to 4, is zero, where F1 = 20Nıˆ, F2 = −50Nˆ, F3 = 10N(−ıˆ + ˆ), ﬁnd F4.
- 2.9 Three forces F = 2Nıˆ − 5Nˆ, R =


10N(cosθıˆ+sinθˆ) and W = −20Nˆ, sum up to zero. Determine the angle θ and draw the force vector R clearly showing its direction.

- 2.10Given that R1 = 1Nıˆ+1.5Nˆ and R2 =
- 3.2Nıˆ − 0.4Nˆ, ﬁnd 2 R1 + 5 R2.


- 2.11 For the unit vectors λˆ1 and λˆ2 shown below, ﬁnd the scalars α and β such that αλˆ2 − 3λˆ2 = βˆ.

x

y

60o 1

1

λˆ1

λˆ2

problem 2.11:

(Filename:pﬁgure2.vec1.11)

- 2.12 In the ﬁgure shown, T1 = 20√2N, T2 = 40N, and W is such that the sum of the three forces equals zero. If W is doubled, ﬁnd α and

β such that α T1,β T2, and 2 W still sum up to zero.

x

y

60o 45o

T1

T2

W

problem 2.12:

(Filename:pﬁgure2.vec1.12)

- 2.13 In the ﬁgure shown, rods AB and BC are each 4 cm long and lie along y and x axes, respectively. Rod CD is in the xz plane and makes an angle θ = 30o with the x-axis.

- (a) Find rAD in termsofthevariablelength

.

- (b) Find and α such that rAD = rAB − rBC + αkˆ.


y

x

z

4 cm

4 cm

A B

D

C

30o

problem 2.13:

(Filename:pﬁgure2.vec1.13)

- 2.14 Find the magnitudes of the forces F1 =


30Nıˆ−40Nˆ and F2 = 30Nıˆ+40Nˆ. Draw the two forces, representing them with their

magnitudes.

2.15 Two forces R = 2N(0.16ıˆ + 0.80ˆ) and W = −36Nˆ act on a particle. Find the magnitude of the net force. What is the direction of this force?

- 2.16InProblem2.13, ﬁnd suchthatthelength of the position vector rAD is 6cm.
- 2.17 In the ﬁgure shown, F1 = 100N and F2 = 300N. Find the magnitude and direction of F2 − F1.

x

y

F1

F2 45o 30o

F2- F1

problem 2.17:

(Filename:pﬁgure2.vec1.17)

- 2.18 Let two forces P and Q act in the direction shown in the ﬁgure. You are allowed to change the direction of the forces by changing the angles α and θ while keeping the magniitudes ﬁxed. What should be the values of α and θ if the magnitude of P + Q has to be the maximum?

x

y

P

Q

α θ

problem 2.18:

(Filename:pﬁgure2.vec1.18)

- 2.19 Two points A and B are located in the xy plane. The coordinates of A and B are (4mm, 8mm) and (90mm, 6mm), respectively.

- (a) Draw position vectors rA and rB.
- (b) Find the magnitude of rA and rB.
- (c) How far is A from B?


- 2.20 In the ﬁgure shown, a ball is suspended witha0.8mlongcordfroma2mlonghoistOA.


- (a) Find the position vector rB of the ball.
- (b) Find the distance of the ball from the origin.


A

y

0.8m

2 m

B

45o

O

x

problem 2.20:

(Filename:pﬁgure2.vec1.20)

- 2.21 A 1m × 1m square board is supported by two strings AE and BF. The tension in the string BF is 20N. Express this tension as a vector.

x

y

E

F

2 m

2 m

2.5m

1 m

1

1

1 m

A B

D C

plate

problem 2.21:

(Filename:pﬁgure2.vec1.21)

- 2.22 The top of an L-shaped bar, shown in the ﬁgure, is to be tied by strings AD and BD to the points A and B in the yz plane. Find the length of the strings AD and BD using vectors rAD and rBD.

A

B

1 m

2 m

30o

y

x z

problem 2.22:

(Filename:pﬁgure2.vec1.22)

- 2.23 A cube of side 6inis shown in the ﬁgure.


- (a) Find the position vector of point F, rF, from the vector sum rF = rD+ rC/D+ rF/c.
- (b) Calculate | rF|.
- (c) Find rG using rF. y


z

E F

D C

H G

x

A B

problem 2.23:

(Filename:pﬁgure2.vec1.23)

- 2.24 A circular disk of radius 6inis mounted on axle x-x at the end an L-shaped bar as shown in the ﬁgure. The disk is tipped 45o with the horizontal bar AC. Two points, P and Q, are marked on the rim of the plate; P directly parallel to the center C into the page, and Q at the highest point above the center C. Taking the

base vectorsıˆ,ˆ, andkˆ as shown in the ﬁgure, ﬁnd

- (a) the relative position vector rQ/P,
- (b) the magnitude | rQ/P|.


![image 1](Introduction to Statics and Dynamics Problems_images/imageFile1.png)

![image 2](Introduction to Statics and Dynamics Problems_images/imageFile2.png)

A

12"

x x

45o

6"

O

Q

Q

D

D C

C

P

ıˆ 6"

ˆ

kˆ

problem 2.24:

(Filename:pﬁgure2.vec1.24)

- 2.25 Find the unit vector λˆAB, directed from point A to point B shown in the ﬁgure.

x

y

1 m

1 m

2 m

3 m

A

B

problem 2.25:

(Filename:pﬁgure2.vec1.25)

- 2.26 Find a unit vector along string BA and express the position vector of A with respect to B, rA/B, in terms of the unit vector.

x

z

y

A

3 m B

2.5m

1.5m

1 m

problem 2.26:

(Filename:pﬁgure2.vec1.26)

- 2.27 In the structure shown in the ﬁgure, = 2ft,h = 1.5ft. The force in the spring is F = k rAB, wherek = 100lbf/ft. Findaunitvector λˆAB along AB and calculate the spring force F = FλˆAB.


y

C

B

30o

h

x

O

problem 2.27:

(Filename:pﬁgure2.vec1.27)

- 2.28 Express the vector rA = 2mıˆ − 3mˆ + 5mkˆ intermsofitsmagnitudeandaunitvector indicating its direction.
- 2.29 Let F = 10lbfıˆ + 30lbfˆ and W = −20lbfˆ. Find a unit vector in the direction of

the net force F + W, and express the the net force in terms of the unit vector.

- 2.30 Let λˆ1 = 0.80ıˆ + 0.60ˆ and λˆ2 = 0.5ıˆ + 0.866ˆ.


- (a) Show that λˆ1 and λˆ2 are unit vectors.
- (b) Is the sum of these two unit vectors also a unit vector? If not, then ﬁnd a unit vector along the sum of λˆ1 and λˆ2.


2.31IfamassslidesfrompointAtowardspoint B along a straight path and the coordinates of points A and B are (0 in, 5in, 0in) and (10in, 0in, 10in), respectively, ﬁnd the unit vector

λˆ AB directed from A to B along the path.

- 2.32 Write the vectors F1 = 30Nıˆ +40Nˆ −

10Nkˆ, F2 = −20Nˆ + 2Nkˆ, and F3 = −10Nıˆ − 100Nkˆ as a list of numbers (rows or columns). Find the sum of the forces using a computer.

2.2 The dot product of two vectors

- 2.33 Express the unit vectors nˆ and λˆ in terms of ıˆ and ˆ shown in the ﬁgure. What are the x and y components of r = 3.0ftnˆ −1.5ftλˆ ? ∗


y

###### λˆ nˆ

###### ˆ

θ

x

ıˆ

###### problem 2.33:

(Filename:eﬁg1.2.27)

- 2.34 Find the dot product of two vectors F = 10lbfıˆ−20lbfˆ and λˆ = 0.8ıˆ+0.6ˆ. Sketch

F and λˆ and show what their dot product represents.

- 2.35 The position vector of a point A is rA = 30cm√ ıˆ. Find the dot product of rA with λˆ =

3

2 ıˆ + 12ˆ.

- 2.36 Fromtheﬁgurebelow,ﬁndthecomponent of force F in the direction of λˆ .

x

y

30o 10o

λˆ

F= 100N

problem 2.36:

(Filename:pﬁgure2.vec1.33)

- 2.37 Find the angle between F1 = 2Nıˆ + 5Nˆ and F2 = −2Nıˆ + 6Nˆ.
- 2.38 A force F is directed from point A(3,2,0) to point B(0,2,4). If the x-component of the force is 120 N, ﬁnd the y- and z-components of F.
- 2.39Aforceactingonabeadofmassm isgiven as F = −20lbfıˆ+22lbfˆ+12lbfkˆ. What is the angle between the force and the z-axis?
- 2.40 Given ω = 2rad/sıˆ + 3rad/sˆ, H1 = (20ıˆ+30ˆ)kgm2/s and H2 = (10ıˆ+15ˆ+ 6kˆ)kgm2/s, ﬁnd (a) the angle between ω and H1 and (b) the angle between ω and H2.
- 2.41 The unit normal to a surface is given as nˆ = 0.74ıˆ + 0.67ˆ. If the weight of a block on this surface acts in the −ˆ direction, ﬁnd the angle that a 1000 N normal force makes with the direction of weight of the block.
- 2.42 Vector algebra. For each equation below state whether:


- (a) The equation is nonsense. If so, why?
- (b) Is always true. Why? Give an example.
- (c) Is never true. Why? Give an example.
- (d) Is sometimes true. Give examples both ways.


You may use trivial examples.

- a) A + B = B + A
- b) A + b = b + A
- c) A · B = B · A
- d) B/ C = B/C
- e) b/ A = b/A
- f) A = ( A· B) B+( A· C) C+( A· D) D


- 2.43 Use the dot product to show ‘the law of cosines’; i. e.,

c2 = a2 + b2 + 2ab cosθ.

(Hint: c = a+ b; also, c · c = c · c)

b c

a

θ

problem 2.43:

(Filename:pﬁgure.blue.2.1)

- 2.44 (a) Draw the vector r = 3.5inıˆ +

3.5inˆ−4.95inkˆ. (b) Find the angle this vector makes with the z-axis. (c) Find the angle this vector makes with the x-y plane.

- 2.45 In the ﬁgure shown, λˆ andnˆ are unit vectors parallel and perpendicular to the surface AB, respectively. A force W = −50Nˆ acts on the block. Find the components of W along λˆ and nˆ.

ıˆ

ˆ

30o

A

O B

λˆ

nˆ

W

problem 2.45:

(Filename:pﬁgure2.vec1.41)

- 2.46 From the ﬁgure shown, ﬁnd the compo-

nents of vector rAB (you have to ﬁrst ﬁnd this position vector) along

- (a) the y-axis, and
- (b) along λˆ .


y

x

z

A

B 3 m

30o

2 m

2 m 1 m

λˆ

problem 2.46:

(Filename:pﬁgure2.vec1.42)

- 2.47 The net force acting on a particle is F = 2Nıˆ + 10Nˆ. Find the components of this force in another coordinate system with basis vectors ıˆ = −cosθıˆ + sinθˆ and ˆ = −sinθıˆ − cosθˆ. For θ = 30o, sketch the

vector F and show its components in the two coordinate systems.

- 2.48 Find the unit vectors eˆR and eˆθ in terms of ıˆ and ˆ with the geometry shown in ﬁgure.


What are the componets of W along eˆR and eˆθ?

θ

ˆ

ıˆ

W

eˆθ

eˆR

problem 2.48:

(Filename:pﬁgure2.vec1.44)

- 2.49 Write the position vector of point P in terms of λˆ1 and λˆ2 and

- (a) ﬁnd the y-component of rP,
- (b) ﬁnd the component of rP alon λˆ1.


x

y

θ1

θ2

1

2

P

λˆ1

λˆ2

problem 2.49:

(Filename:pﬁgure2.vec1.45)

- 2.50 What is the distance between the point A and the diagonal BC of the parallelepiped shown? (Use vector methods.)

A

1

3 4

C

|B|
|---|


problem 2.50:

(Filename:pﬁgure.blue.2.3)

- 2.51 Let F1 = 30Nıˆ +40Nˆ −10Nkˆ, F2 = −20Nˆ + 2Nkˆ, and F3 = F3xıˆ + F3yˆ −

F3zkˆ. If the sum of all these forces must equal zero, ﬁnd the required scalar equations to solve

for the components of F3.

- 2.52 A vector equation for the sum of forces results into the following equation:

F 2

(ıˆ −

√3ˆ) +

R 5

(3ıˆ + 6ˆ) = 25Nλˆ

where λˆ = 0.30ıˆ − 0.954ˆ. Find the scalar equations parallel and perpendicular to λˆ .

- 2.53 Let α F1 + β F2 + γ F3 = 0, where


F1, F2, and F3 are as given in Problem 2.32. Solve for α,β, and γ using a computer.

- 2.54 Write a computer program (or use a canned program) to ﬁnd the dot product of two 3-D vectors. Test the program by com-

puting the dot products ıˆ · ıˆ,ıˆ · ˆ, and ˆ · kˆ. Now use the program to ﬁnd the components of F = (2ıˆ + 2ˆ − 3kˆ)N along the line rAB = (0.5ıˆ − 0.2ˆ + 0.1kˆ)m.

- 2.55 Let rn = 1m(cosθnıˆ + sinθnˆ), where θn = θ0 − n θ. Using a computer generate the required vectors and ﬁnd the sum

44

n=0

ri, with  θ = 1o and θ0 = 45o.

2.3 Cross product, moment, and moment about an axis

- 2.56 Find the cross product of the two vectors shown in the ﬁgures below from the information given in the ﬁgures.

|2<br><br>a|4<br><br>60o b|
|---|---|
| | |


x

y

|3<br><br>a 10|4<br><br>5o b|
|---|---|
| | |


x

y

| |4<br><br>30o<br><br>a|
|---|---|
| |x<br><br>4<br><br>30o|


y

|45o 5|4<br><br>a|
|---|---|
| |45o x|


y

|b|3<br><br>3|
|---|---|
|2<br><br>2|x<br><br>a|


y

|b|3<br><br>3|
|---|---|
|2<br><br>2|x<br><br>a|


y

x

y

|(-1,2)<br><br>a|b (2,2)|
|---|---|
|(-1,-1)|x<br><br>(2,-1)|


y

(

b

- a
- b


a=3ˆı+ˆ

b = 4ˆ

(a) (b)

(c) (d)

(e) (f)

(g) (h)

problem 2.56:

(Filename:pﬁgure2.vec2.1)

- 2.57 Vector algebra. For each equation below state whether:


- (a) The equation is nonsense. If so, why?
- (b) Is always true. Why? Give an example.
- (c) Is never true. Why? Give an example.
- (d) Is sometimes true. Give examples both ways.


You may use trivial examples.

- a) B × C = C × B
- b) B × C = C · B
- c) C · ( A × B) = B · ( C × A)
- d) A×( B× C) = ( A· C) B−( A· B) C


- 2.58 What is the moment M produced by a 20

- N force F acting in the x direction with a lever arm of r = (16mm)ˆ?

2.59 Find the moment of the force shown on the rod about point O.

x

y

![image 3](Introduction to Statics and Dynamics Problems_images/imageFile3.png)

![image 4](Introduction to Statics and Dynamics Problems_images/imageFile4.png)

O

F= 20N

2m

45o

problem 2.59:

(Filename:pﬁgure2.vec2.2)

2.60 Find the sum of moments of forces W and T about the origin, given that W = 100N, T = 120N,  = 4m, and θ = 30o.

x

y

O

T

W θ

/2

/2

problem 2.60:

(Filename:pﬁgure2.vec2.3)

2.61 Find the moment of the force

- a) about point A
- b) about point O.


α= 30o

F= 50N

- O 2 m


- 2.62 In the ﬁgure shown, OA = AB = 2m. The force F = 40N acts perpendicular to the arm AB. Find the moment of F about O, given that θ = 45o. If F always acts normal to the arm AB,wouldincreasingθ increasethemagnitude of the moment? In particular, what value of θ will give the largest moment?


1.5m

A

problem 2.61:

(Filename:pﬁgure2.vec2.4)

y

F

B

θ A

O

x

problem 2.62:

(Filename:pﬁgure2.vec2.5)

- 2.63 Calculate the moment of the 2kNpayload on the robot arm about (i) joint A, and (ii) joint B,if 1 = 0.8m, 2 = 0.4m, and 3 = 0.1m.

x

y

2 kN

A

B

O

30o

45o

C

1

2

3

problem 2.63:

(Filename:pﬁgure2.vec2.6)

- 2.64 During a slam-dunk, a basketball player pullsonthehoopwitha250lbfatpointCofthe ring as shown in the ﬁgure. Find the moment of the force about

- a) the point of the ring attachment to the board (point B), and
- b) the root of the pole, point O.


| |1.5'|
|---|---|
|3'| |


O

250lbf

15o

6"

10'

board

B

A

basketball hoop

problem 2.64:

(Filename:pﬁgure2.vec2.7)

- 2.65 During weight training, an athelete pulls a weight of 500Nwith his arms pulling on a hadlebar connected to a universal machine by a cable. Find the moment of the force about the shoulder joint O in the conﬁguration shown.


###### problem 2.65:

(Filename:pﬁgure2.vec2.8)

- 2.66 Find the sum of moments due to the two weights of the teeter-totter when the teetertotter is tipped at an angle θ from its vertical position. Giveyouranswerintermsofthe variables shown in the ﬁgure.

h O

B

OA=h AB=AC=

W

W

C

A

θ

α α

problem 2.66:

(Filename:pﬁgure2.vec2.9)

- 2.67 Find the percentage error in computing the moment of W about the pivot point O as a function of θ, if the weight is assumed to act normal to the arm OA (a good approximation when θ is very small).

O θ

A

W

problem 2.67:

(Filename:pﬁgure2.vec2.10)

- 2.68 What do you get when you cross a vector and a scalar? ∗
- 2.69 Why did the chicken cross the road? ∗
- 2.70 Carry out the following cross products in different ways and determine which method takes the least amount of time for you.

- a) r = 2.0ftıˆ + 3.0ftˆ − 1.5ftkˆ; F = −0.3lbfıˆ − 1.0lbfkˆ; r × F =?
- b) r = (−ıˆ + 2.0ˆ + 0.4kˆ)m; L = (3.5ˆ − 2.0kˆ)kgm/s; r × L =?
- c) ω = (ıˆ − 1.5ˆ)rad/s; r = (10ıˆ − 2ˆ + 3kˆ)in; ω × r =?


- 2.71 A force F = 20Nˆ −5Nkˆ acts through a point A with coordinates (200 mm, 300 mm,


-100 mm). What is the moment M(= r × F) of the force about the origin?

2.72CrossProductprogramWriteaprogram that will calculate cross products. The input to the function should be the components of the two vectors and the output should be the components of the cross product. As a model, here is a function ﬁle that calculates dot products in pseudo code.

%program definition

- z(1)=a(1)*b(1);
- z(2)=a(2)*b(2);
- z(3)=a(3)*b(3);


- w=z(1)+z(2)+z(3);

- 2.73 Find a unit vector normal to the surface ABCD shown in the ﬁgure.

4"

5"

5"

D

A

C

B x

z

y

problem 2.73:

(Filename:eﬁg1.2.11)

- 2.74 If the magnitude of a force N normal to the surface ABCD in the ﬁgure is 1000 N, write N as a vector. ∗

x

z

y

A

B

D 1m 1m

1m

1m C 1m

problem 2.74:

(Filename:eﬁg1.2.12)

- 2.75 The equation of a surface is given as z = 2x − y. Find a unit vector nˆ normal to the surface.
- 2.76 In the ﬁgure, a triangular plate ACB, attached to rod AB, rotates about the z-axis. At the instant shown, the plate makes an angle of 60o with the x-axis. Find and draw a vector normal to the surface ACB.

|45o 45o<br><br>1m<br><br>C| |
|---|---|
|o| |


x

z

y 60o

- A
- B


problem 2.76:

(Filename:eﬁg1.2.14)

- 2.77 What is the distance d between the origin and the line AB shown? (You may write your solution in terms of A and B before doing any arithmetic). ∗




z

A

1

kˆ

A

ˆ

ıˆ

d O

1

y

B

1

B

x

problem 2.77:

(Filename:pﬁgure.blue.1.3)

- 2.78 What is the perpendicular distance between the point A and the line BC shown? (There are at least 3 ways to do this using various vector products, how many ways can you ﬁnd?)

x

y

B A

0 2 3

3

C

ıˆ

ˆ

problem 2.78:

(Filename:pﬁgure.blue.2.2)

- 2.79 Given a force, F1 = (−3ıˆ+2ˆ +5kˆ)N acting at a point P whose position is given by

r P/O = (4ıˆ − 2ˆ + 7kˆ)m, what is the moment about an axis through the origin O with

direction λˆ = √25

ˆ + √15

ˆ?

- 2.80 Drawing vectors and computing with vectors. The point O is the origin. Point A has xyz coordinates (0,5,12)m. Point B has xyz coordinates (4,5,12)m.

- a) Make a neat sketch of the vectors OA, OB, and AB.
- b) Find a unit vector in the direction of OA, call it λˆ O A.
- c) Find the force F which is 5N in size and is in the direction of OA.
- d) What is the angle between OA and OB?
- e) What is r BO × F?
- f) What is the moment of F about a line parallel to the z axis that goes through the point B?


- 2.81 Vector Calculations and Geometry. The 5N force F1 is along the line OA. The 7N force F2 is along the line OB.


- a) Find a unit vector in the direction OB. ∗
- b) Find a unit vector in the direction OA. ∗


c) Write both F1 and F2 as the product of their magnitudes and unit vectors in their directions. ∗

- d) What is the angle AOB? ∗
- e) What is the component of F1 in the x-direction? ∗
- f) What is r DO × F1? ( r DO ≡ r O/D is the position of O relative to D.) ∗
- g) What is the moment of F2 about the axis DC? (The moment of a force about an axis parallel to the unit vector λˆ is

deﬁnedas Mλ = λˆ ·( r × F)where r is the position of the point of application of the force relative to some point on the axis. The result does not depend on which point on the axis is used or which point on the line of action of F is used.). ∗

- h) Repeat the last problem using either a different reference point on the axis DC or the line of action OB. Does the solution agree? [Hint: it should.] ∗


z

A B

5m

F2

F1 4m

3m

O

y

D C

x

problem 2.81:

(Filename:p1sp92)

- 2.82 A, B, and C are located by position vectors r A = (1,2,3), r B = (4,5,6), and rC = (7,8,9).

- a) Use the vector dot product to ﬁnd the angle BAC (A is at the vertex of this angle).
- b) Use the vector cross product to ﬁnd the angle BC A (C is at the vertex of this angle).
- c) Find a unit vector perpendicular to the plane ABC.
- d) How far is the inﬁnite line deﬁned by AB fromtheorigin? (Thatis,howclose is the closest point on this line to the origin?)
- e) Is the origin co-planar with the points A, B, and C?


- 2.83 Points A, B, and C in the ﬁgure deﬁne a plane.


- a) Find a unit normal vector to the plane. ∗
- b) Find the distance from this inﬁnite plane to the point D. ∗


c) What are the coordinates of the point on the plane closest to point D? ∗

z

- 4

5

- 5


B

(3, 2, 5)

D

1

(0, 7, 4)

2 3 4

C x y

7

A

(5, 2, 1) (3, 4, 1)

problem 2.83:

(Filename:pﬁgure.s95q2)

##### 2.4 Equivalant force systems and couples

- 2.84 Find the net force on the particle shown in the ﬁgure.

ıˆ

ˆ

4

3

6 N

P

8 N

10N

problem 2.84:

(Filename:pﬁgure2.3.rp1)

- 2.85 Replace the forces acting on the particle of mass m shown in the ﬁgure by a single equivalent force.

ıˆ

ˆ

T 45o 30o

mg

m

2T

T

problem 2.85:

(Filename:pﬁgure2.3.rp2)

- 2.86 Find the net force on the pulley due to the belt tensions shown in the ﬁgure.


30o 50N

###### ˆ

50N

ıˆ

###### problem 2.86:

(Filename:pﬁgure2.3.rp3)

- 2.87 Replace the forces shown on the rectangular plate by a single equivalent force. Where should this equivalent force act on the plate and why?

300mm

200mm

4 N

6 N

5 N

- A D
- B C


problem 2.87:

(Filename:pﬁgure2.3.rp4)

- 2.88 ThreeforcesactonaZ-sectionABCDEas shown in the ﬁgure. Point C lies in the middle of the vertical section BD. Find an equivalent force-couple system acting on the structure and make a sketch to show where it acts.

C

D E

A B

60N 0.5m

0.5m

0.6m

40N

100N

problem 2.88:

(Filename:pﬁgure2.3.rp5)

- 2.89 The three forces acting on the circular plate shown in the ﬁgure are equidistant from the center C. Find an equivalent force-couple system acting at point C.


3 2 F

C R

F

F

###### problem 2.89:

(Filename:pﬁgure2.3.rp6)

2.90 Theforcesandthemomentactingonpoint C of the frame ABC shown in the ﬁgure are Cx = 48N, Cy = 40N, and Mc = 20N·m. Find an equivalent force couple system at point B.

Cy

B

C

Cx

- 1.5m

1.2m

A

MC

problem 2.90:

(Filename:pﬁgure2.3.rp7)

- 2.91 Find an equivalent force-couple system for the forces acting on the beam in Fig. ??, if the equivalent system is to act at


- a) point B,
- b) point D.


2 kN

A B D

C

2 m 1 kN 2kN

2 m

problem 2.91:

(Filename:pﬁgure2.3.rp8)

- 2.92 In Fig. ??, three different force-couple systems are shown acting on a square plate. Identify which force-couple systems are equivalent.

| | |
|---|---|
| | |
|0.2m| |


20N

|20N<br><br>6N·m|
|---|


20N

40N

30N

30N

30N

30N

0.2m

problem 2.92:

(Filename:pﬁgure2.3.rp9)

- 2.93 The force and moment acting at point C of a machine part are shown in the ﬁgure where


Mc is not known. It is found that if the given force-couplesystemisreplacedbyasinglehorizontal force of magnitude 10N acting at point A then the net effect on the machine part is the same. What is the magnitude of the moment Mc?

- A
- B


20cm

MC

10N C

30cm

problem 2.93:

(Filename:pﬁgure2.3.rp10)

##### 2.5 Center of mass and center of gravity

- 2.94 An otherwise massless structure is made of four point masses, m, 2m, 3m and 4m, located at coordinates (0, 1m), (1m, 1m), (1m, −1m), and (0, −1m), respectively. Locate the center of mass of the structure. ∗
- 2.95 3-D: The following data is given for a structural system modeled with ﬁve point masses in 3-D-space:


###### mass coordinates (in m)

- 0.4kg (1,0,0)
- 0.4kg (1,1,0)
- 0.4kg (2,1,0)


- 0.4kg (2,0,0)
- 1.0kg (1.5,1.5,3)

Locate the center of mass of the system.

- 2.96 Write a computer program to ﬁnd the center of mass of a point-mass-system. The input to the program should be a table (or matrix) containing individual masses and their coordinates. (It is possible to write a single program for both 2-D and 3-D cases, write separate programs for the two cases if that is easier for you.) Check your program on Problems 2.94 and 2.95.


2.97 Find the center of mass of the following composite bars. Each composite shape is made oftwoormoreuniformbarsoflength0.2mand mass 0.5kg.

(a) (b)

(c)

problem 2.97:

(Filename:pﬁgure3.cm.rp7)

- 2.98 Find the center of mass of the following two objects [Hint: set up and evaluate the needed integrals.]

y

y

O x

m = 2 kg

- (a)

O x

- (b)


r = 0.5 m

r = 0.5 m

m = 2 kg

problem 2.98:

(Filename:pﬁgure3.cm.rp8)

- 2.99 Find the center of mass of the following plates obtained from cutting out a small section from a uniform circular plate of mass 1kg (priortoremovingthecutout)andradius1/4m.


200 mm x 200 mm

- (a)
- (b)


r = 100 mm

100 mm

problem 2.99:

(Filename:pﬁgure3.cm.rp9)

Free body diagrams

##### 3.1 Free body diagrams

- 3.1 How does one know what forces and moments to use in

- a) the statics force balance and moment balance equations?
- b) thedynamicslinearmomentumbalance and angular momentum balance equations?


- 3.2 A point mass m is attached to a piston by two inextensible cables. There is gravity. Draw a free body diagram of the mass with a little bit of the cables.

A

9a

6a

5a

B G

C

ıˆ

ˆ

problem 3.2:

(Filename:pﬁgure2.1.suspended.mass)

- 3.3 Simple pendulum. For the simple pendulum shown the “body”— the system of interest

—isthemassandalittlebitofthestring. Draw a free body diagram of the system.

θ L

problem 3.3:

(Filename:pﬁgure.s94h2p1)

- 3.4 Draw a free body diagram of mass m at the instant shown in the ﬁgure. Evaluate the left hand side of the linear momentum balance equation ( F = m a) as explicitly as possible. Identify the unknowns in the expression.


x

F = 50 N

x

m = 10 kg

h

y

frictionless

problem 3.4:

(Filename:pﬁg2.2.rp1)

- 3.5 A1000 kgsatelliteisinorbit. Itsspeedisv anditsdistancefromthecenteroftheearthis R. Drawafreebodydiagramofthesatellite. Draw another that takes account of the slight drag force of the earth’s atmosphere on the satellite.

![image 5](Introduction to Statics and Dynamics Problems_images/imageFile5.png)

R

v m

problem 3.5:

(Filename:pﬁgure.s94h2p5)

- 3.6 The uniform rigid rod shown in the ﬁgure hangs in the vertical plane with the support of the spring shown. Draw a free body diagram of the rod.

| | |
|---|---|
| | |


m k

/3

problem 3.6:

(Filename:pﬁg2.1.rp1)

- 3.7 FBD of rigid body pendulum. The rigid body pendulum in the ﬁgure is a uniform rod of mass m. Draw a free body diagram of the rod.


g

θ

| | |
|---|---|
| | |


uniform rigid bar, mass m

problem 3.7:

(Filename:pﬁgure2.rod.pend.fbd)

- 3.8 A thin rod of mass m rests against a frictionless wall and on a frictionless ﬂoor. There is gravity. Draw a free body diagram of the rod.

A

B

L G

| | |
|---|---|
| | |


θ

problem 3.8:

(Filename:ch2.6)

- 3.9 A uniform rod of mass m rests in the back of a ﬂatbed truck as shown in the ﬁgure. Draw a free body diagram of the rod, set up a suitable coordinate system, and evaluate F for the rod.

|m| |
|---|---|
| | |


frictionless

problem 3.9:

(Filename:pﬁg2.2.rp5)

- 3.10 A disc of mass m sits in a wedge shaped groove. Thereisgravityandnegligiblefriction. The groove that the disk sits in is part of an assemblythatisstill. Drawafreebodydiagram of the disk. (See also problems 4.15 and 6.47.)

θ1 θ2 x

y

r

problem 3.10:

(Filename:ch2.5)

- 3.11 A pendulum, made up of a mass m attached at the end of a rigid massless rod of length , hangs in the vertical plane from a hinge. The pendulum is attached to a spring and a dashpot on each side at a point  /4 from the hinge point. Draw a free body diagram of the pendulum (mass and rod system) when the pendulum is slightly away from the vertical equilibrium position.


| |1/4|
|---|---|
|c|c 3/4<br><br>|


k k

m

problem 3.11:

(Filename:pﬁg2.1.rp5)

- 3.12 The left hand side of the angular momentum balance (Torque balance in statics) equation requires the evaluation of the sum of moments about some point. Draw a free body diagram of the rod shown in the ﬁgure and compute MO as explicitly as possible. Now

compute MC. How many unknown forces does each equation contain?

C O

| | |
|---|---|
| | |


m = 5 kg L/2

L

1

3

problem 3.12:

(Filename:pﬁg2.2.rp3)

- 3.13 A block of mass m is sitting on a frictionless surface at points A and B and acted upon at point E by the force P. There is gravity. Draw a free body diagram of the block.

| | |
|---|---|
| | |


b

2b

2d

d

C D

A B

G

E P

problem 3.13:

(Filename:ch2.1)

- 3.14 A mass-spring system sits on a conveyer belt. The spring is ﬁxed to the wall on one end. The belt moves to the right at a constant


speed v0. The coefﬁcient of friction between the mass and the belt is µ. Draw a free body diagram of the mass assuming it is moving to the left at the time of interest.

k

m

µ

problem 3.14:

(Filename:pﬁg2.1.rp6)

- 3.15 A small block of mass m slides down an incline with coefﬁcient of friction µ. At an instant in time t during the motion, the block has speed v. Draw a free body diagram of the block.

m

µ

α

problem 3.15:

(Filename:pﬁg2.3.rp5)

- 3.16 Assume that the wheel shown in the ﬁgure rolls without slipping. Draw a free body diagram of the wheel and evaluate F and

MC. What would be different in the expressions obtained if the wheel were slipping?

C

P

F = 10 N m = 20 kg

r

R

problem 3.16:

(Filename:pﬁg2.2.rp4)

- 3.17 A compound wheel with inner radius r and outer radius R is pulled to the right by a 10N force applied through a string wound around the inner wheel. Assume that the wheel rolls to the right without slipping. Draw a free body diagram of the wheel.

C

P

r R

F = 10 N

m = 20 kg

problem 3.17:

(Filename:pﬁg2.1.rp8)

- 3.18 A block of mass m is sitting on a frictional surface and acted upon at point E by the horizontal force P through the center of mass. The block is resting on sharp edge at point B and is supported by a small ideal wheel at point A. There is gravity. Draw a free body diagram of the block including the wheel, assuming the block is sliding to the right with coefﬁcient of friction µ at point B.


2b

b

C D

d

E P

| | |
|---|---|
| | |


2d

G

A B

problem 3.18:

(Filename:ch2.2)

- 3.19 A spring-mass model of a mechanical system consists of a mass connected to three springs and a dashpot as shown in the ﬁgure. The wheels against the wall are in tracks (not shown)thatdonotletthewheelsliftoffthewall so the mass is constrained to move only in the vertical direction. Draw a free body diagram of the system.

k

k

k

c

||m|
|---|
|
|---|


problem 3.19:

(Filename:pﬁg2.1.rp2)

- 3.20 A point mass of mass m moves on a frictionless surface and is connected to a spring withconstantk andunstretchedlength . There is gravity. At the instant of interest, the mass has just been released at a distance x to the right from its position where the spring is unstretched.

- a) Draw a free body diagram of the of the mass and spring together at the instant of interest.
- b) Draw free body diagrams of the mass and spring separately at the instant of interest.


(See also problem 5.32.)

x

m

problem 3.20:

(Filename:ch2.10)

- 3.21 FBD of a block. The block of mass 10kg is pulled by an inextensible cable over the pulley.


- a) Assuming the block remains on the ﬂoor, draw a free diagram of the block.
- b) Draw a free body diagram of the pulley and a little bit of the cable that rides over it.


x F = 50 N

x

m = 10 kg

h

y

frictionless

problem 3.21:

(Filename:pﬁgure2.1.block.pulley)

- 3.22 A pair of falling masses. Two masses A & B are spinning around each other and falling towards the ground. A string, which you can assume to be taught, connects the two masses. A snapshot of the system is shown in the ﬁgure. Draw free body diagrams of

- a) mass A with a little bit of string,
- b) mass B with a little bit of string, and
- c) the whole system.


A

B

m

m 30o

problem 3.22:

(Filename:pﬁgure.s94h2p4)

- 3.23 A two-degree of freedom spring-mass system is shown in the ﬁgure. Draw free body diagrams of each mass separately and then the two masses together.

m1

x1 k4

- k1
- k2


k3

x2

||m2|
|---|
|
|---|


problem 3.23:

(Filename:pﬁg2.1.rp4)

- 3.24 The ﬁgure shows a spring-mass model of a structure. Assume that the three masses are displaced to the right by x1, x2 and x3 from the static equilibrium conﬁguration such that x1 <


- x2 < x3. Draw free body diagrams of each mass and evaluate F in each case. Ignore gravity.


x1

x2 x3

k3

k5 k6

k1

k4

m m

M

k2

problem 3.24:

(Filename:pﬁg2.2.rp10)

- 3.25 In the system shown, assume that the two masses A and B move together (i.e., no relative slip). Draw a free body diagram of mass A and evaluate the left hand side of the linear momentum balance equation. Repeat the procedure for the system consisting of both masses.

µ = 0.2

k

F

- A
- B


ıˆ

ˆ

problem 3.25:

(Filename:pﬁg2.2.rp2)

- 3.26 Two identical rigid rods are connected together by a pin. The vertical stiffness of the system is modeled by three springs as shown in the ﬁgure. Draw free body diagrams of each rod separately. [This problem is a little tricky and there is more than one reasonable answer.]

m m

k 2k k

problem 3.26:

(Filename:pﬁg2.1.rp3)

- 3.27 A uniform rod rests on a cart which is being pulled to the right. The rod is hinged at one end (with a frictionless hinge) and has no friction at the contact with the cart. The cart rolls on massless wheels that have no bearing friction (ideal massless wheels). Draw FBD’s of


- a) the rod,
- b) the cart, and
- c) the whole system.


A

θ

B F

problem 3.27:

(Filename:pﬁgure.s94h2p6)

3.28FBD’sofsimplependulumanditsparts. The simple pendulum in the ﬁgure is composed of a rod of negligible mass and a pendulum bob of mass m.

- a) Draw a free body diagram of the pendulum bob.
- b) Draw a free body diagram of the rod.
- c) Draw a free body diagram of the rod and pendulum bob together.


g

###### θ

rigid, massless

m

problem 3.28:

(Filename:pﬁgure2.simp.pend.fbd)

- 3.29 Forthedoublependulumshownintheﬁg-

ure, evaluate F and MO at the instant shown in terms of the given quantities and un-

known forces (if any) on the bar.

θ1

θ2

massless

m

O

problem 3.29:

(Filename:pﬁg2.2.rp6)

- 3.30 See also problem 11.4. Two frictionless blocks sit stacked on a frictionless surface. A force F is applied to the top block. There is gravity.

a) Draw a free body diagram of the two blockstogetherandafreebodydiagram of each block separately.

g F m1

m2

problem 3.30:

(Filename:ch2.3)

- 3.31 For the system shown in the ﬁgure draw free body diagrams of each mass separately assuming that there is no relative slip between the two masses.


µ = 0.2

|A|
|---|


k F

|B|
|---|


problem 3.31:

(Filename:pﬁg2.1.rp7)

- 3.32 Two frictionless prisms of similar right triangular sections are placed on a frictionless horizontal plane. The top prism weighs W and the lower one, nW. Draw free body diagrams of

- a) the system of prisms and
- b) each prism separately.


a

b

W

nW

φ

φ

problem 3.32:

(Filename:pﬁgure.blue.28.2)

- 3.33 In the slider crank mechanism shown, draw a free body diagram of the crank and

evaluate F and MO asexplicitlyaspossible.

massless

Crank of mass m

θ

ω

problem 3.33:

(Filename:pﬁg2.2.rp9)

- 3.34 FBD of an arm throwing a ball. An arm throws a ball up. A crude model of an arm is that it is made of four rigid bodies (shoulder, upper arm, forearm and a hand) that are connected with hinges. At each hinge there are muscles that apply torques between the links. Draw a FBD of


- a) the ball, the shoulder (ﬁxed to the wall),
- b) the upper arm,
- c) the fore-arm,
- d) the hand, and
- e) the whole arm (all four parts) including the ball.


Write the equation of angular momentum balance about the shoulder joint A, evaluating the left-hand-side as explicitly as possible.

A

B

C D

problem 3.34:

(Filename:eﬁg2.1.23)

- 3.35 An imagined testing machine consists of a box fastened to a wheel as shown. The box always moves so that its ﬂoor is parallel to the ground (like an empty car on a Ferris Wheel). Two identical masses, A and B are connected togetherbycords1and2asshown. Theﬂoorof the box is frictionless. The machine and blocks are set in motion when θ = 0o, with constant θ˙ = 3 rad/s. Draw free body diagrams of:

- a) the system consisting of the box, blocks, and wheel,
- b) the system of box and blocks,
- c) the system of blocks and cords,
- d) the system of box, block B, cord 2, and a portion of cord 1 and,
- e) the box and blocks separately.


θ

A B

pivot

1m

1 2 θ˙

problem 3.35:

(Filename:pﬁgure.blue.52.1)

- 3.36 Free body diagrams of a double ‘physical’ pendulum. A double pendulum is a system where one pendulum hangs from another. Draw free body diagrams of various subsystems in a typical conﬁguration.

- a) Draw a free body diagram of the lower stick, the upper stick, and both sticks in arbitrary conﬁgurations.
- b) Repeat part (a) but use the simplifying assumption that the upper bar has negligible mass.


O

φ1

φ2

problem 3.36:

(Filename:pﬁgure.s94h2p3)

- 3.37 The strings hold up the mass m = 3kg. There is gravity. Draw a free body diagram of the mass.


z

B D

C

y

1m

3m

A

1m

x

4m 4m

problem 3.37:

(Filename:pﬁgure2.1.3D.pulley.fbd)

- 3.38 Mass on inclined plane. A block of mass m rests on a frictionless inclined plane. It is supported by two stretched springs. The mass is pulled down the plane by an amount δ and released. Draw a FBD of the mass just after it is released.

m

k

k

30o

- 1m 2m
- 2m


δ

problem 3.38:

(Filename:eﬁg2.1.24)

- 3.39 Hanging a shelf. A shelf with negligible mass supports a 0.5kgmass at its center. The shelf is supported at one corner with a ball and socket joint and the other three corners with strings. At the moment of interest the shelf is in a rocket in outer space and accelerating at 10m/s2 in the k direction. The shelf is in the xy plane. Draw a FBD of the shelf.

1m

.48m

A C B

D

E

H

G

1m

1m

32m

ıˆ ˆ

kˆ

problem 3.39:

(Filename:ch3.14)

- 3.40 A massless triangular plate rests against a frictionless wall at point D and is rigidly attached to a massless rod supported by two ideal bearings. A ball of mass m is ﬁxed to the centroid of the plate. There is gravity. Draw a free body diagram of the plate, ball, and rod as a system.


d=c+(1/2)b d

y

D

e h

G

z

B

x

a

c

b

A

problem 3.40:

(Filename:ch2.9)

- 3.41 An undriven massless disc rests on its edge on a frictional surface and is attached rigidly by a weld at point C to the end of a rod that pivots at its other end about a ball-andsocket joint at point O. There is gravity.


- a) Draw a free body diagram of the disk and rod together.
- b) Draw free body diagrams of the disc and rod separately.
- c) What would be different in the free body diagram of the rod if the ball-andsocket was rusty (not ideal)?


z

ω

R L

ball and socket

y

C

O weld

x

problem 3.41:

(Filename:ch2.7)

Statics

##### 4.1Staticequilibriumofonebody

- 4.1 To evaluate the equation F = m a for someproblem, astudentwrites F = Fxıˆ−

(Fy − 30N)ˆ + 50Nkˆ in the xyz coordinate system, but a = 2.5m/s2ıˆ + 1.8m/s2ˆ −

azkˆ in a rotated x y z coordinate system. If ıˆ = cos60oıˆ + sin60oˆ, ˆ = −sin60oıˆ +

cos60oˆ and kˆ = kˆ, ﬁnd the scalar equations for the x , y , and z directions.

- 4.2 N small blocks each of mass m hang vertically as shown, connected by N inextensible strings. Find the tension Tn in string n. ∗

m m m

m m m

- n = 1

n = N - 2 n = N - 1 n = N

- n = 2
- n = 3
- n = 4


problem 4.2:

(Filename:pﬁgure2.hanging.masses)

- 4.3 See also problem 7.98. A zero length


spring (relaxed length 0 = 0) with stiffness k = 5N/m supports the pendulum shown. Assume g = 10 N/m. Find θ for static equilibrium. ∗

0 = 0 k = 5 N/m

D = 4 m

g = 10 m/s

y

m = 2 kg

x

θ

L = 3 m

problem 4.3:

(Filename:pﬁgure2.blue.80.2.a)

- 4.4 What force should be applied to the end of the string over the pulley at C so that the mass at A is at rest?

m

A

B C

F

3m

2m 3m

4m

ıˆ

ˆ g

problem 4.4:

(Filename:f92h1p1.a)

4.2 Elementary truss analysis

The ﬁrst set of problems concerns math skills that can be used to help solve truss problems. If computer solution is not going to be used, the following problems can be skipped.

- 4.5 Write the following equations in matrix form to solve for x, y, and z:

2x − 3y + 5 = 0, y + 2πz = 21,

1 3

x − 2y + πz − 11 = 0.

- 4.6 Are the following equations linearly independent?

- a) x1 + 2x2 + x3 = 30
- b) 3x1 + 6x2 + 9x3 = 4.5
- c) 2x1 + 4x2 + 15x3 = 7.5.


- 4.7 Write computer commands (or a program) tosolvefor x, y and z fromthefollowingequations with r as an input variable. Your program should display an error message if, for a particular r, the equations are not linearly independent.

- a) 5x + 2r y + z = 2
- b) 3x + 6y + (2r − 1)z = 3
- c) 2x + (r − 1)y + 3r z = 5.


Find the solutions for r = 3, 4.99, and 5.

- 4.8 An exam problem in statics has three unknown forces. A student writes the following three equations (he knows that he needs three equations for three unknowns!) — one for the force balance in the x-direction and the other twoforthemomentbalanceabouttwodifferent points.


- a) F1 − 12 F2 + √12

F3 = 0

- b) 2F1 + 32 F2 = 0

- c) 52 F2 +


√2F3 = 0.

Can the student solve for F1, F2, and F3 uniquely from these equations? ∗

- 4.9 What is the solution to the set of equations:

x + y + z + w = 0 x − y + z − w = 0 x + y − z − w = 0 x + y + z − w = 2?

- 4.3 Advanced truss analysis: determinacy, rigidity, and redundancy
- 4.4 Internal forces
- 4.5 Springs


- 4.10 What is the stiffness of two springs in parallel?
- 4.11 What is the stiffness of two springs in series?
- 4.12 What is the apparant stiffness of a pendulum when pushed sideways.
- 4.13 Optimize a triangular truss for stiffness and for strength and show that the resulting design is not the same.


- 4.6Structuresandmachines
- 4.14 See also problems 6.18 and 6.19. Find

the ratio of the masses m1 and m2 so that the system is at rest.

m1

m2

A

B 30o

60o

g

problem 4.14:

(Filename:pulley4.c)

- 4.15 (See also problem 6.47.) What are the forces on the disk due to the groove? Deﬁne any variables you need.


r

- y


θ1 θ2 x

problem 4.15:

(Filename:ch2.5.b)

- 4.16Twogearsatrest. Seealsoproblems7.77 and ??. At the input to a gear box, a 100lbf force is applied to gear A. At the output, the


machinery (not shown) applies a force of FB to the output gear. Assume the system of gears

is at rest. What is FB?

no slip

FB = ?

RA

RB

RC

C

A B

FA = 100 lb

problem 4.16: Two gears.

(Filename:pg131.3.a)

- 4.17 See also problem 4.18. A reel of mass M and outer radius R is connected by a horizontal string from point P across a pulley to a hanging object of mass m. The inner cylinder of the


reel has radius r = 12 R. The slope has angle θ. There is no slip between the reel and the slope.

There is gravity.

- a) Find the ratio of the masses so that the system is at rest. ∗
- b) Find the corresponding tension in the string, in terms of M, g, R, and θ. ∗
- c) Findthecorrespondingforceonthereel at its point of contact with the slope, point C, in terms of M, g, R, and θ. ∗


- d) Another look at equilibrium. [Harder] Draw a careful sketch and ﬁnd a point where the lines of action of the gravity force andstringtensionintersect. Forthereel tobeinstaticequilibrium,thelineofaction of the reaction force at C must pass through this point. Using this information, what must the tangent of the angle φ of the reaction force at C be, measured with respect to the normal to the slope? Doesthisansweragreewiththat you would obtain from your answer in part(c)? ∗
- e) Whatistherelationshipbetweentheangle ψ of the reaction at C, measured withrespecttothenormaltotheground, and the mass ratio required for static equilibrium of the reel? ∗


Check that for θ = 0, your solution gives Mm = 0 and FC = Mgˆ and for θ = π2 , it gives m M = 2 and FC = Mg(ıˆ + 2ˆ).

M massless

g

P

R

G

r

###### ˆ

m

C

ıˆ

θ

problem 4.17:

(Filename:pﬁgure2.blue.47.3.a)

4.18 This problem is identical to problem 4.17 except for the location of the connection point of the string to the reel, point P. A reel of mass M and outer radius R is connected by an inextensible string from point P across a pulleytoahangingobjectofmassm. Theinner

cylinder of the reel has radius r = 12 R. The slope has angle θ. There is no slip between the

reel and the slope. There is gravity. In terms of M, m, R, and θ, ﬁnd:

- a) theratioofthemassessothatthesystem is at rest, ∗
- b) the corresponding tension in the string, and ∗
- c) thecorrespondingforceonthereelatits


point of contact with the slope, point C.

∗

Check that for θ = 0, your solution gives m M = 0 and FC = Mgˆ and for θ = π2 , it gives Mm = −2 and FC = Mg(ıˆ −2ˆ).The negative mass ratio is impossible since mass cannot be negative and the negative normal force is impossible unless the wall or the reel or both can ‘suck’ or they can ‘stick’ to each other (that is, provide some sort of suction, adhesion, or magnetic attraction).

M

g

massless

R

G

r

|P<br><br>ıˆ C<br><br>ˆ<br><br>θ| |
|---|---|
| | |


m

problem 4.18:

(Filename:pﬁgure2.blue.47.3.b)

- 4.19 Two racks connected by three gears at rest. See also problem 7.86. A 100lbf force is applied to one rack. At the output, the ma-

chinery (not shown) applies a force of FB to the other rack. Assume the gear-train is at rest.

What is FB?

massless rack

massless rack

no slip

FB = ?

RA

RC A b C RE d E

no slip 100 lb

x B

y

problem 4.19: Two racks connected by three gears.

(Filename:ch4.5.a)

- 4.20 In the ﬂyball governor shown, the mass of each ball is m = 5kg, and the length of each link is = 0.25 m. There are frictionless hinges at points A, B, C, D, E, F where the links are connected. The central collar has mass m/4. Assuming that the spring of constant k = 500 N/m is uncompressed when θ = π radians, what is the compression of the spring?

m m/4 m

θ θ

fixed

A B

F C E D

k

problem 4.20:

(Filename:summer95p2.2.a)

- 4.21 Assume a massless pulley is round and has outer radius R2. It slides on a shaft that has radius Ri. Assume there is friction between the shaft and the pulley with coefﬁcient of friction µ, and friction angle φ deﬁned by µ = tan(φ). Assume the two ends of the line that are wrapped around the pulley are parallel.


a) What is the relation between the two tensions when the pulley is turning? You may assume that the bearing shaft touches the hole in the pulley at only one point. ∗ .

- b) Plug in some reasonable numbers for

Ri, Ro and µ (or φ) to see one reason why wheels (say pulleys) are such a good idea even when the bearings are not all that well lubricated. ∗

- c) (optional) To further emphasize the point look at the relation between the two string tensions when the bearing is locked (frozen, welded) and the string slides on the pulley with same coefﬁcient of friction µ (see, for example, BeerandJohnstonStaticssection8.10). Look at the force ratios from parts (a) and (b) for a reasonable value of µ, say µ = 0.2. ∗


FBD

###### ˆ

ıˆ

Ro

O

T1

Ri

Forces of bearing on pulley

T2

###### problem 4.21:

(Filename:pﬁgure.blue.20.2)

- 4.22 A massless triangular plate rests against a frictionless wall at point D and is rigidly attached to a massless rod supported by two ideal bearings ﬁxed to the ﬂoor. A ball of mass m is ﬁxed to the centroid of the plate. There is gravity and the system is at rest What is the reaction at point D on the plate?

a

b

c

d=c+(1/2)b d

e h

x

y

z

A

B

D

G

problem 4.22:

(Filename:ch3.1b)

- 4.7 Hydrostatics
- 4.8 Advanced statics


- 4.23 See also problem 5.119. For the three cases (a), (b), and (c), below, ﬁnd the tension in the string AB. In all cases the strings hold up the mass m = 3kg. You may assume the local gravitational constant is g = 10m/s2. In all cases the winches are pulling in the string so that the velocity of the mass is a constant 4m/s


upwards (in the kˆ direction). [ Note that in problems (b) and (c), in order to pull the mass up at constant rate the winches must pull in the strings at an unsteady speed.] ∗

(a)

(b) winch

winch

B B

C

3m 4m

| |A|
|---|---|
|m| |


A

z

|m<br><br>|
|---|


x

2m 3m

(c)

winch winch

z

B D

1m

winch

C

1m

y

3m

A

x

4m

4m

problem 4.23:

(Filename:f92h1p1)

- 4.24 The strings hold up the mass m = 3kg. You may assume the local gravitational constant is g = 10m/s2. Find the tensions in the strings if the mass is at rest.

A

B D

C

3m

4m

1m

1m

4m

z

y

x

problem 4.24:

(Filename:f92h1p1.b)

- 4.25 Hanging a shelf. A uniform 5kg shelf is supported at one corner with a ball and socket joint and the other three corners with strings. At the moment of interest the shelf is at rest. Gravity acts in the−kˆ direction. The shelf is in the xy plane.


- a) Draw a FBD of the shelf.
- b) Challenge: without doing any calculations on paper can you ﬁnd one of the reaction force components or the tension in any of the cables? Give yourself a few minutes of staring to try to ﬁnd this force. If you can’t, then come back to this question after you have done all the calculations.
- c) Write down the equation of force equilibrium.
- d) Write down the moment balance equation using the center of mass as a reference point.
- e) By taking components, turn (b) and (c) into six scalar equations in six unknowns.
- f) Solve these equations by hand or on the computer.
- g) Instead of using a system of equations try to ﬁnd a single equation which can


be solved for TEH. Solve it and compare to your result from before. ∗

h) Challenge: For how many of the reactions can you ﬁnd one equation which will tell you that particular reaction without knowing any of the other reactions? [Hint, try moment balance about variousaxesaswellasaforcebalancein an appropriate direction. It is possible to ﬁnd ﬁve of the six unknown reaction components this way.] Must these solutions agree with (d)? Do they?

G

A B

C

32m

H

1m

E

.48m

kˆ

1m

1m

D

ıˆ ˆ

problem 4.25:

(Filename:pﬁgure.s94h2p10.a)

Unconstrained motion of particles

##### 5.1 Force and motion in 1D

- 5.1 In elementary physics, people say “F = ma“ What is a more precise statement of an equation we use here that reduces to F = ma for one-dimensional motion of a particle?


- 5.2 Does linear momentum depend on reference point? (Assume all candidate points are ﬁxed in the same Newtonian reference frame.)


- 5.3 The distance between two points in a bicycle race is 10 km. How many minutes does a bicyclist take to cover this distance if he/she maintains a constant speed of 15 mph.
- 5.4 Given that x˙ = k1 + k2t, k1 = 1ft/s, k2 = 1ft/s2, and x(0) = 1ft, what is x(10s)?
- 5.5 Find x(3s) given that x˙ = x/(1s) and x(0) = 1m

or, expressed slightly differently, x˙ = cx and x(0) = x0,

where c = 1s−1 and x0 = 1m. Make a sketch of x versus t. ∗

- 5.6 Given that x˙ = A sin[(3rad/s)t], A = 0.5m/s, and x(0) = 0m, whatis x(π/2s)?
- 5.7 Given that x˙ = x/s and x(0s) = 1m, ﬁnd x(5s).
- 5.8 Let a = ddtv = −kv2 and v(0) = v0. Find t such that v(t) = 12v0.

- 5.9 A sinusoidal force acts on a 1kg mass as shown in the ﬁgure and graph below. The mass is initially still; i. e.,


x(0) = v(0) = 0.

- a) What is the velocity of the mass after 2π seconds?
- b) What is the position of the mass after 2π seconds?
- c) Plot position x versus time t for the motion.


F(t)

5 N

2π sec 0

t

x

F(t)

||1 kg|
|---|
|
|---|


problem 5.9:

(Filename:pﬁgure.blue.6.1)

- 5.10 A motorcycle accelerates from 0mph to 60mph in 5 seconds. Find the average acceleration in m/s2. How does this acceleration compare with g, the acceleration of an object falling near the earth’s surface?
- 5.11 A particle moves along the x-axis with

an initial velocity vx = 60m/s at the origin when t = 0. For the ﬁrst 5s it has no acceleration, and thereafter it is acted upon by a retarding force which gives it a constant acceleration ax = −10m/s2. Calculate the velocity and the x-coordinate of the particle when t = 8s and when t = 12s, and ﬁnd the maximum positive x coordinate reached by the particle.

- 5.12 The linear speed of a particle is given as

v = v0 + at, where v is in m/s, v0 = 20m/s, a = 2m/s2, and t is in seconds. Deﬁne appropriate dimensionless variables and write a dimensionless equation that describes the relation of v and t.

- 5.13 A ball of mass m has an acceleration a = cv2ıˆ. Find the position of the ball as a function of velocity.
- 5.14 A ball of mass m is dropped from rest at a height h above the ground. Find the position and velocity as a function of time. Neglect air friction. When does the ball hit the ground? What is the velocity of the ball just before it hits?
- 5.15 A ball of mass m is dropped vertically from rest at a height h above the ground. Air resistance causes a drag force on the ball directly proportional to the speed v of the ball,

Fd = bv. The drag force acts in a direction opposite to the direction of motion. Find the velocity and position of the ball as a function of time. Find the velocity as a function of position. Gravity is non-negligible, of course.

- 5.16 A grain of sugar falling through honey has a negative acceleration proportional to the difference between its velocity and its ‘terminal’


- velocity (which is a known constant vt). Write this sentence as a differential equation, deﬁning any constants you need. Solve the equation assuming some given initial velocity v0. [hint: acceleration is the time-derivative of velocity]
- 5.17 The mass-dashpot system shown below is released from rest at x = 0. Determine an equation of motion for the particle of mass m thatinvolvesonly x˙ and x (aﬁrst-orderordinary differentialequation). Thedampingcoefﬁcient of the dashpot is c.

x

M

c g

problem 5.17:

(Filename:pﬁgure.blue.151.2)

- 5.18 Due to gravity, a particle falls in air with a drag force proportional to the speed squared.

- (a) Write F = m a in terms of variables you clearly deﬁne,
- (b) ﬁnd a constant speed motion that satisﬁes your differential equation,
- (c) pick numerical values for your constantsandfortheinitialheight. Assume the initial speed is zero


- (i) set up the equation for numerical solution,
- (ii) solve the equation on the computer,
- (iii) make a plot with your computer solution and show how that plot supports your answer to (b).


- 5.19 A ball of mass m is dropped vertically from rest at a height h above the ground. Air resistance causes a drag force on the ball proportional to the speed of the ball squared,

Fd = cv2. The drag force acts in a direction opposite to the direction of motion. Find the velocity as a function of position.

- 5.20 A force pulls a particle of mass m towards the origin according to the law (assume same equation works for x > 0, x < 0)


F = Ax + Bx2 + Cx˙

Assume x˙(0) = 0. Using numerical solution, ﬁnd values of A, B,C,m, and x0 so that

- (a) the mass never crosses the origin,
- (b) the mass crosses the origin once,
- (c) the mass crosses the origin many times.


- 5.21 Acaracceleratestotherightwithconstant accelerationstartingfromastop. Thereiswind resistance force proportional to the square of the speed of the car. Deﬁne all constants that you use.

- a) What is its position as a function of time?
- b) What is the total force (sum of all forces) on the car as a function of time?
- c) How much power P is required of the engine to accelerate the car in this manner (as a function of time)?


problem 5.21: Car.

(Filename:s97p1.2)

- 5.22 A ball of mass m is dropped vertically from a height h. The only force acting on the ball in its ﬂight is gravity. The ball strikes the ground with speed v− and after collision it rebounds vertically with reduced speed v+ directly proportional to the incoming speed, v+ = ev−,where0 < e < 1. Whatisthemaximum height the ball reaches after one bounce, in terms of h, e, and g. ∗

- a) Do this problem using linear momentum balance and setting up and solving the related differential equations and “jump” conditions at collision.
- b) Dothisproblemagainusingenergybalance.


- 5.23 A ball is dropped from a height of h0 = 10montoahardsurface. Aftertheﬁrstbounce,

it reaches a height of h1 = 6.4m. What is the vertical coefﬁcient of restitution, assuming it is decoupled from tangential motion? What is the height of the second bounce, h2?

h0 h1

g h2

problem 5.23:

(Filename:Danef94s1q7)

- 5.24 In problem 5.23, show that the number of bounces goes to inﬁnity in ﬁnite time, assuming that the vertical coefﬁcient is ﬁxed. Find


the time in terms of the initial height h0, the coefﬁcient of restitution, e, and the gravitational constant, g.

##### 5.2 Energy methods in 1D

- 5.25 The power available to a very strong accelerating cyclist is about 1 horsepower. Assume a rider starts from rest and uses this constant power. Assume a mass (bike + rider) of 150lbm, a realistic drag force of

.006lbf/(ft/s)2v2. Neglect other drag forces.

- (a) What is the peak speed of the cyclist?
- (b) Using analytic or numerical methods make a plot of speed vs. time.
- (c) What is the acceleration as t → ∞ in this solution?
- (d) What is the acceleration as t → 0 in your solution?


- 5.26 Given v˙ = −gRr22 , where g and R are constantsandv = drdt . Solveforv asafunction of r if v(r = R) = v0. [Hint: Use the chain rule of differentiation to eliminate t, i.e., ddtv = dv dr · drdt = ddrv · v. Or ﬁnd a related dynamics problem and use conservation of energy.]

• • •

Also see several problems in the harmonic oscillator section.

5.3 The harmonic oscillator

The ﬁrst set of problems are entirely about the harmonic oscillator governing differential equation, with no mechanics content or context.

- 5.27 Given that x¨ = −(1/s2)x, x(0) = 1m, and x˙(0) = 0 ﬁnd:

- a) x(π s) =?
- b) x˙(π s) =?


- 5.28 Given that x¨ + x = 0, x(0) = 1, and x˙(0) = 0, ﬁnd the value of x at t = π/2 s.
- 5.29 Given that x¨ +λ2x = C0, x(0) = x0, and x˙(0) = 0, ﬁnd the value of x at t = π/λ s.

• • •

Thenextsetofproblemsconcernonemassconnectedtooneormorespringsandpossiblywith a constant force applied.

- 5.30 Consider a mass m on frictionless rollers. The mass is held in place by a spring with stiffness k and rest length . When the spring is relaxed the position of the mass is x = 0. At times t = 0 the mass is at x = d and is let go with no velocity. The gravitational constant is g. In terms of the quantities above,


- a) What is the acceleration of the block at t = 0+?
- b) What is the differential equation governing x(t)?
- c) What is the position of the mass at an arbitrary time t?


d) What is the speed of the mass when it passes through x = 0?

x

d

m

problem 5.30:

(Filename:pﬁgure.blue.25.1)

###### 5.31 Spring and mass. A spring with rest

length 0 is attached to a mass m which slides frictionlessly on a horizontal ground as shown. At time t = 0 the mass is released with no initialspeedwiththespringstretchedadistance d. [Remember to deﬁne any coordinates or base vectors you use.]

- a) Whatistheaccelerationofthemassjust after release?
- b) Find a differential equation which describes the horizontal motion of the mass.
- c) What is the position of the mass at an arbitrary time t?
- d) What is the speed of the mass when it passes through the position where the spring is relaxed?


0 d

m

problem 5.31:

(Filename:s97f1)

###### 5.32 Reconsider the spring-mass system inproblem 3.20. Let m = 2kg and k = 5N/m.The mass is pulled to the right a distance

x = x0 = 0.5m from the unstretched position and released from rest. At the instant of release, noexternalforcesactonthemassother than the spring force and gravity.

- a) What is the initial potential and kinetic energy of the system?
- b) What is the potential and kinetic energy of the system as the mass passes through the static equilibrium (unstretched spring) position?


x

m

problem 5.32:

(Filename:ch2.10.a)

###### 5.33 Reconsider the spring-mass system fromproblem 5.30.

a) Find the potential and kinetic energy of the spring mass system as functions of time.

- b) Using the computer, make a plot of the potential and kinetic energy as a function of time for several periods of oscillation. Are the potential and kinetic energy ever equal at the same time? If so, at what position x(t)?
- c) Make a plot of kinetic energy versus potential energy. What is the phase relationship between the kinetic and potential energy?


- 5.34 For the three spring-mass systems shown in the ﬁgure, ﬁnd the equation of motion of the mass in each case. All springs are massless and are shown in their relaxed states. Ignore gravity. (In problem (c) assume vertical motion.) ∗

m

k, 0 k, 0

m

k, 0

m

k, 0

k, 0

- (a)
- (b)
- (c)


F(t)

F(t)

x

y

F(t)

problem 5.34:

(Filename:summer95f.3)

- 5.35 A spring and mass system is shown in the ﬁgure.


- a) First,asareview,letk1,k2,andk3 equal zero and k4 be nonzero. What is the natural frequency of this system?
- b) Now, let all the springs have non-zero stiffness. What is the stiffness of a single spring equivalent to the combina-

tion of k1,k2,k3,k4? What is the frequency of oscillation of mass M?

- c) What is the equivalent stiffness, keq, of all of the springs together. That is, if you replace all of the springs with one spring, what would its stiffness have to be such that the system has the same natural frequency of vibration?


- k1 x

- k2 k4


k3

||M|
|---|
|
|---|


problem 5.35:

(Filename:pﬁgure.blue.159.3)

- 5.36 The mass shown in the ﬁgure oscillates in the vertical direction once set in motion by displacing it from its static equilibrium position. The position y(t) of the mass is measured from the ﬁxed support, taking downwards as positive. The static equilibrium position is ys and

the relaxed length of the spring is 0. At the instant shown, the position of the mass is y and its velocity y˙, directed downwards. Draw a free body diagram of the mass at the instant of interest and evaluate the left hand side of the energy balance equation (P = E˙K).

k

ys

y

||m|
|---|
|
|---|


problem 5.36:

(Filename:pﬁg2.3.rp1)

- 5.37 Mass hanging from a spring. A mass m is hanging from a spring with constant k which


has the length l0 when it is relaxed (i. e., when no mass is attached). It only moves vertically.

- a) DrawaFreeBodyDiagramofthemass.
- b) Write the equation of linear momentum balance. ∗
- c) Reduce this equation to a standard differential equation in x, the position of the mass. ∗
- d) Verify that one solution is that x(t) is constant at x = l0 + mg/k.
- e) What is the meaning of that solution? (That is, describe in words what is going on.) ∗
- f) Deﬁne a new variable xˆ = x − (l0 + mg/k). Substitute x = xˆ+(l0+mg/k) into your differential equation and note that the equation is simpler in terms of the variable xˆ. ∗
- g) Assume that the mass is released from an an initial position of x = D. What is the motion of the mass? ∗
- h) What is the period of oscillation of this oscillating mass? ∗
- i) Whymightthissolutionnotmakephysical sense for a long, soft spring if D >  0 + 2mg/k)? ∗


l0

k

x

||m|
|---|
|
|---|


###### problem 5.37:

(Filename:pg141.1)

The following problem concerns simple harmonic motion for part of the motion. It involves pasting together solutions.

- 5.38 One of the winners in the egg-drop contestsponsoredbyalocalchapterofASMEeach spring, was a structure in which rubber bands held the egg at the center of it. In this problem, we will consider the simpler case of the egg to be a particle of mass m and the springs to be linear devices of spring constant k. We will also consider only a two-dimensional version of the winning design as shown in the ﬁgure. If the frame hits the ground on one of the straight sections, what will be the frequency of vibration of the egg after impact? [Assume small oscillations and that the springs are initially stretched.]

ground

egg, m

k k

k

problem 5.38:

(Filename:pﬁgure.blue.149.1)

- 5.39 A person jumps on a trampoline. The trampoline is modeled as having an effective vertical undamped linear spring with stiffness k = 200lbf/ft. The person is modeled as a rigid mass m = 150lbm. g = 32.2ft/s2.


- a) What is the period of motion if the person’s motion is so small that her feet never leave the trampoline? ∗
- b) Whatisthemaximumamplitudeofmotion for which her feet never leave the trampoline? ∗
- c) (harder) If she repeatedly jumps so that her feet clear the trampoline by a height h = 5ft, what is the period of this motion? ∗


problem5.39: Apersonjumpsonatrampoline.

(Filename:pﬁgure3.trampoline)

##### 5.4 More on vibrations:damping

- 5.40 If x¨ + cx˙ + kx = 0, x(0) = x0, and x˙(0) = 0, ﬁnd x(t).
- 5.41 A mass moves on a frictionless surface. It is connected to a dashpot with damping coefﬁcient b to its right and a spring with constant k and rest length to its left. At the instant of interest, the mass is moving to the right and the spring is stretched a distance x from its position where the spring is unstretched. There is gravity.

- a) Draw a free body diagram of the mass at the instant of interest.
- b) Evaluate the left hand side of the equation of linear momentum balance as explicitly as possible. ∗


. x

m

k b

problem 5.41:

(Filename:ch2.11)

5.5 Forced oscillations and resonance

- 5.42 A 3kg mass is suspended by a spring (k = 10N/m) and forced by a 5N sinusoidally oscillating force with a period of 1s. What is the amplitude of the steady-state oscillations (ignore the “homogeneous” solution)
- 5.43 Given that θ¨ + k2θ = β sinωt, θ(0) = 0, and θ(˙ 0) = θ˙0, ﬁnd θ(t) .
- 5.44 A machine produces a steady-state vibration due to a forcing function described by


Q(t) = Q0 sinωt, where Q0 = 5000N. The machine rests on a circular concrete foundation. The foundation rests on an isotropic, elastic half-space. The equivalent spring constant of the half-space is k = 2,000,000N·m and has a damping ratio d = c/cc = 0.125. The machine operates at a frequency of ω = 4 Hz.

- (a) Whatisthenaturalfrequencyofthesystem?
- (b) If the system were undamped, what would the steady-state displacement be?
- (c) What is the steady-state displacement given that d = 0.125?
- (d) How much additional thickness of concrete should be added to the footing to reduce the damped steady-state amplitude by 50%? (The diameter must be held constant.)


##### 5.6 Coupled motions in 1D

The primary emphasis of this section is setting up correct differential equations (without sign errors) and solving these equations on the computer. Experts note: normal modes are coverred in the vibrations chapter. These ﬁrst problems are just math problems, using some of the skills that are needed for the later problems.

- 5.45 Write the following set of coupled second order ODE’s as a system of ﬁrst order ODE’s.

- x¨1 = k2(x2 − x1) − k1x1
- x¨2 = k3x2 − k2(x2 − x1)


- 5.46 See also problem 5.47. The solution of a set of a second order differential equations is:

ξ(t) = A sinωt + B cosωt + ξ∗ ξ(˙ t) = Aω cosωt − Bω sinωt,

where A and B are constants to be determined from initial conditions. Assume A and B are the only unknowns and write the equations in matrix form to solve for A and B in terms of ξ(0) and ξ(˙ 0).

- 5.47 Solve for the constants A and B in Problem 5.46 using the matrix form, if ξ(0) = 0, ξ(˙ 0) = 0.5, ω = 0.5rad/s and ξ∗ = 0.2.
- 5.48 A set of ﬁrst order linear differential equations is given:


x˙1 = x2 x˙2 + kx1 + cx2 = 0

Write these equations in the form x˙ = [A] x, where x =

x1 x2

.

5.49WritethefollowingpairofcoupledODE’s as a set of ﬁrst order ODE’s.

- x¨1 + x1 = x˙2 sint
- x¨2 + x2 = x˙1 cost


- 5.50 The following set of differential equations can not only be written in ﬁrst order form but in matrix form x˙ = [A] x + c. In general things are not so simple, but this linear case is prevalant in the analytic study of dynamical systems.

- x˙1 = x3
- x˙2 = x4
- x˙3 + 5 2x1 − 4 2x2 = 2 2v1∗
- x˙4 − 4 2x1 + 5 2x2 = − 2v1∗


- 5.51 Write each of the following equations as a system of ﬁrst order ODE’s.


- a) θ¨ + λ2θ = cost,
- b) x¨ + 2px˙ + kx = 0,


c) x¨ + 2cx˙ + k sin x = 0.

- 5.52 A train is moving at constant absolute velocity vıˆ. A passenger, idealized as a point mass, is walking at an absolute absolute velocity uıˆ, where u > v. What is the velocity of the passenger relative to the train?

• • •

- 5.53 Two equal masses, each denoted by the letter m, are on an air track. One mass is connected by a spring to the end of the track. The other mass is connected by a spring to the ﬁrst mass. The two spring constants are equal and represented by the letter k. In the rest (springs arerelaxed)conﬁguration, themassesareadistance apart. Motion of the two masses x1 and x2 is measured relative to this conﬁguration.

- a) Draw a free body diagram for each mass.
- b) Write the equation of linear momentum balance for each mass.
- c) Write the equations as a system of ﬁrst order ODEs.
- d) Pick parameter values and initial conditions of your choice and simulate a motion of this system. Make a plot of the motion of, say, one of the masses vs time,
- e) Explain how your plot does or does not make sense in terms of your understanding of this system. Is the initial motion in the right direction? Are the solutions periodic? Bounded? etc.


k

x1

||m|
|---|
|
|---|


k

x2

||m|
|---|
|
|---|


problem 5.53:

(Filename:pﬁgure.s94f1p4)

- 5.54 Two equal masses, each denoted by the letter m, are on an air track. One mass is connected by a spring to the end of the track. The other mass is connected by a spring to the ﬁrst mass. The two spring constants are equal and represented by the letter k. In the rest conﬁguration (springs are relaxed) the masses are a distance apart. Motion of the two masses x1 and x2 is measured relative to this conﬁguration.


- a) Writethepotentialenergyofthesystem

for arbitrary displacements x1 and x2 at some time t.

- b) Write the kinetic energy of the system

at the same time t in terms of x˙1, x˙2, m, and k.

- c) Write the total energy of the system.


x1

x2

k

k

||m|
|---|
|
|---|


||m|
|---|
|
|---|


problem 5.54:

(Filename:pﬁgure.twomassenergy)

- 5.55 Normal Modes. Three equal springs (k) hold two equal masses (m) in place. There is

no friction. x1 and x2 are the displacements of the masses from their equilibrium positions.

- a) How many independent normal modes of vibration are there for this system? ∗
- b) Assume the system is in a normal mode

of vibration and it is observed that x1 = A sin(ct) + B cos(ct) where A, B, and

c are constants. What is x2(t)? (The answer is not unique. You may express your answer in terms of any of A, B, c, m and k. ) ∗

- c) Find all of the frequencies of normalmode-vibration for this system in terms of m and k. ∗


||m|
|---|
|
|---|


||m|
|---|
|
|---|


x1

k k k

x2

problem 5.55:

(Filename:pﬁgure.f93f2)

- 5.56 A two degree of freedom spring-mass system. A two degree of freedom mass-spring system, madeupoftwounequalmassesm1 and m2 and three springs with unequal stiffnesses k1, k2 and k3, is shown in the ﬁgure. All three springs are relaxed in the conﬁguration shown. Neglect friction.

- a) Derive the equations of motion for the two masses. ∗
- b) Does each mass undergo simple harmonic motion? ∗


k1 k2 k3

x1 x2

||m2|
|---|
|
|---|


||m1|
|---|
|
|---|


problem 5.56:

(Filename:pﬁgure.s94h5p1)

- 5.57 For the three-mass system shown, draw a free body diagram of each mass. Write the spring forces in terms of the displacements x1, x2, and x3.


L L L L

k k k k

m

m m

x1 x2 x3

problem 5.57:

(Filename:s92f1p1)

- 5.58 The springs shown are relaxed when xA = xB = xD = 0. In terms of some or all of mA,mB,mD, xA, xB, xD, x˙A, x˙B, x˙C, and k1,k2,k3,k4,c1, and F, ﬁnd the acceleration of block B. ∗

| | | | |
|---|---|---|---|
| | |mD| |
|k3| | | |
| | | | |


||mA|
|---|
|
|---|


xA xB xD

k1

k4 c1 k2 mB

A B D

problem 5.58:

(Filename:pﬁgure.s95q3)

- 5.59 A system of three masses, four springs, and one damper are connected as shown. Assume that all the springs are relaxed when xA = xB = xD = 0. Given k1, k2, k3, k4, c1, mA, mB, mD, xA, xB, xD, x˙A, x˙B, and x˙D, ﬁnd the acceleration of mass B, aB = x¨Bıˆ. ∗

mA

xA xB xD

k1 c1

k4 k2 mB k3

||mD|
|---|
|
|---|


A B D

problem 5.59:

(Filename:pﬁgure.s95f1)

- 5.60 Equations of motion. Two masses are connectedtoﬁxedsupportsandeachotherwith the three springs and dashpot shown. The force F acts on mass 2. The displacements x1 and x2 are deﬁned so that x1 = x2 = 0 when the springsareunstretched. Thegroundisfrictionless. The governing equations for the system shown can be writen in ﬁrst order form if we deﬁne v1 ≡ x˙1 and v2 ≡ x˙2.

- a) Write the governing equations in a neat ﬁrst order form. Your equations should be in terms of any or all of the constants

m1, m2, k1, k2,k3, C, the constant force F, and t. Getting the signs right is important.

- b) Write computer commands to ﬁnd and

plot v1(t) for 10 units of time. Make up appropriate initial conditions.

- c) For constants and initial conditions of


your choosing, plot x1 vs t for enough time so that decaying erratic oscillations can be observed.

k1 k2

| | | |
|---|---|---|
| | | |
|k3| | |


x1

x2 F c

|m2|
|---|


||m1|
|---|
|
|---|


problem 5.60:

(Filename:p.f96.f.3)

- 5.61 x1(t) and x2(t) are measured positions on two points of a vibrating structure. x1(t) is shown. Some candidates for x2(t) are shown. Whichofthe x2(t)couldpossiblybeassociated with a normal mode vibration of the structure? Answer “could” or “could not” next to each


###### choice. (If a curve looks like it is meant to be a sine/cosine curve, it is.)

X1(t)

X2 ?

- a)

- b)

- c)

- d)

- e)


X2 ?

X2 ?

X2 ?

X2 ?

###### problem 5.61:

(Filename:pﬁgure.blue.144.1)

- 5.62 For the three-mass system shown, one of the normal modes is described with the eigen-

vector (1, 0, -1). Assume x1 = x2 = x3 = 0 when all the springs are fully relaxed.

- a) Whatistheangularfrequency ω forthis mode? Answer in terms of L,m,k, and g. (Hint: Note that in this mode of vibration the middle mass does not move.) ∗
- b) Make a neat plot of x2 versus x1 for one cycle of vibration with this mode.


m

x1 x2 x3 m m k k k k

L L L L

problem 5.62:

(Filename:pﬁgure.blue.160.2)

- 5.63 The three beads of masses m, 2m, and m connected by massless linear springs of con-


stant k slide freely on a straight rod. Let xi denote the displacement of the ith bead from its equilibrium position at rest.

- a) Write expressions for the total kinetic and potential energies.
- b) Write an expression for the total linear momentum.
- c) Draw free body diagrams for the beads and use Newton’s second law to derive the equations for motion for the system.
- d) Verify that total energy and linear momentum are both conserved.
- e) Show that the center of mass must either remain at rest or move at constant velocity.
- f) What can you say about vibratory (sinusoidal) motions of the system?


Static equilibrium

k k

configuration m

m 2m

Displaced configuration

m 2m m

x1 x2 x3

###### problem 5.63:

(Filename:pﬁgure.blue.161.1)

- 5.64 The system shown below comprises three identical beads of mass m that can slide frictionlesslyontherigid,immobile,circularhoop. The beads are connected by three identical linear springs of stiffness k, wound around the hoop as shown and equally spaced when the springs are unstretched (the strings are unstretched when θ1 = θ2 = θ3 = 0.)

- a) Determine the natural frequencies and associated mode shapes for the system. (Hint: you should be able to deduce a ‘rigid-body’ mode by inspection.)
- b) If your calculations in (a) are correct, then you should have also obtained the mode shape (0,1,−1)T . Write down themostgeneralsetofinitialconditions sothattheensuingmotionofthesystem is simple harmonic in that mode shape.
- c) Since (0,1,−1)T is a mode shape, then by “symmetry”, (−1,0,1)T and (1,−1,0)T arealsomodeshapes(draw a picture). Explain how we can have three mode shapes associated with the same frequency.
- d) Without doing any calculations, compare the frequencies of the constrained system to those of the unconstrained system, obtained in (a).


m

m

m k

k

k

g = 0

R = 1

θ2 θ1

θ3

![image 6](Introduction to Statics and Dynamics Problems_images/imageFile6.png)

![image 7](Introduction to Statics and Dynamics Problems_images/imageFile7.png)

![image 8](Introduction to Statics and Dynamics Problems_images/imageFile8.png)

![image 9](Introduction to Statics and Dynamics Problems_images/imageFile9.png)

![image 10](Introduction to Statics and Dynamics Problems_images/imageFile10.png)

![image 11](Introduction to Statics and Dynamics Problems_images/imageFile11.png)

problem 5.64:

(Filename:pﬁgure.blue.158.1)

- 5.65 Equations of motion. Two masses are connected to ﬁxed supports and each other with the two springs and dashpot shown. The displacements x1 and x2 are deﬁned so that x1 = x2 = 0 when both springs are unstretched.

ForthespecialcasethatC = 0and F0 = 0 clearly deﬁne two different set of initial conditions that lead to normal mode vibrations of this system.

c M1 M2

x1

k1 k2

x2

F0 sin(λt)

problem 5.65:

(Filename:p.s96.p3.1)

- 5.66 As in problem 5.59, a system of three masses, four springs, and one damper are connected as shown. Assume that all the springs are relaxed when xA = xB = xD = 0.


- a) In the special case when k1 = k2 = k3 = k4 = k, c1 = 0, and mA = mB = mD = m, ﬁnd a normal mode of vibration. Deﬁne it in any clear way and explain or show why it is a normal mode in any clear way. ∗
- b) In the same special case as in (a) above,


ﬁnd another normal mode of vibration.

∗

xA xB xD

k4 k2 k3

||mD|
|---|
|
|---|


|mB|
|---|


k1 c1

mA

A B D

problem 5.66:

(Filename:pﬁgure.s95f1a)

- 5.67 As in problem 5.143, a system of three masses, four springs, and one damper are connected as shown. In the special case when c1 = 0, ﬁnd the normal modes of vibration.

| | | | |
|---|---|---|---|
| | |mD| |
|k3| | | |
| | | | |


||mA|
|---|
|
|---|


xA xB xD

k1

k4 c1 k2 mB

A B D

problem 5.67:

(Filename:pﬁgure.s95q3a)

- 5.68 Normal modes. All three masses have m = 1kg and all 6 springs are k = 1N/m. The system is at rest when x1 = x2 = x3 = 0.


- a) Findasmanydifferentinitialconditions as you can for which normal mode vibrations result. In each case, ﬁnd the associated natural frequency. (we will call two initial conditions [v] and [w] different if there is no constant c so that

[v1 v2 v3] = c[w1 w2 w3]. Assume the initial velocities are zero.)

- b) For the initial condition [x0] = [ 0.1m 0 0 ],


[x˙0] = [ 0 2m/s 0 ] whatistheinitial(immediatelyafterthe start) acceleration of mass 2?

x1

x2 x3

ıˆ

k

k k

k k

k

||m1|
|---|
|
|---|


||m2|
|---|
|
|---|


||m3|
|---|
|
|---|


problem 5.68:

(Filename:pﬁgure3.f95p2p2)

##### 5.7 Time derivative of a vector: position, velocity and acceleration

- 5.69 The position vector of a particle in the xyplane is given as r = 3.0mıˆ + 2.5mˆ. Find (a) the distance of the particle from the origin and (b) a unit vector in the direction of r.
- 5.70 Given r(t) = Asin(ωt)ıˆ + Btˆ + Ckˆ, ﬁnd

- (a) v(t)
- (b) a(t)
- (c) r(t) × a(t).


- 5.71 A particle of mass =3kg travels in space with its position known as a function of time, r = (sin ts)mıˆ+(cos ts)mˆ+test m/skˆ. At t = 3s, ﬁnd the particle’s

a) velocity and b) acceleration.

- 5.72 A particle of mass m = 2kg travels in the xy-plane with its position known as a function of time, r = 3t2 m/s2ıˆ+4t3sm3 ˆ. At t = 5s, ﬁnd the particle’s

a) velocity and ∗ b) acceleration. ∗

- 5.73 If r˙ = (u0 sin t)ıˆ + v0ˆ and r(0) = x0ıˆ + y0ˆ, with u0, v0, and , ﬁnd r(t) = x(t)ıˆ + y(t)ˆ. ∗
- 5.74 The velocity of a particle of mass m on a frictionless surface is given as v = (0.5m/s)ıˆ − (1.5m/s)ˆ. If the displacement is given by r = vt, ﬁnd (a) the distance traveled by the mass in 2 seconds and (b) a unit vector along the displacement.
- 5.75 For v = vxıˆ + vyˆ + vzkˆ and a = 2m/s2ıˆ−(3m/s2 −1m/s3 t)ˆ −5 m/s4 t2kˆ, write the vector equation v = a dt as three scalar equations.
- 5.76 Find r(5s) given that r˙ = v1 sin(ct)ıˆ+v2ˆ and r(0) = 2mıˆ+3mˆ

and that v1 is a constant 4m/s, v2 is a constant 5m/s, and c is a constant 4s−1. Assume ıˆ and ˆ are constant.

- 5.77 Let r˙ = v0 cosαıˆ + v0 sinαˆ +

(v0 tanθ − gt)kˆ, where v0, α, θ, and g are constants. If r(0) = 0, ﬁnd r(t).

- 5.78 On a smooth circular helical path the velocity of a particle is r˙ = −R sintıˆ +

R costˆ + gtkˆ. If r(0) = Rıˆ, ﬁnd r((π/3)s).

- 5.79 Draw unit vectors along ω = (4.33rad/s)ıˆ + (2.50rad/s)ˆ and r = (0.50ft)ıˆ − (0.87ft)ˆ and ﬁnd the angle between the two unit vectors.
- 5.80 What is the angle between the x-axis and the vector v = (0.3ıˆ − 2.0ˆ + 2.2kˆ)m/s?
- 5.81 The position of a particle is given by r(t) = (t2 m/s2ıˆ + e ts mˆ). What are the velocity and acceleration of the particle? ∗

- 5.82 A particle travels on a path in the xy-plane given by y(x) = sin2( mx )m. where x(t) = t3(sm3 ). What are the velocity and acceleration of the particle in cartesian coordinates when

t = (π)

1 3 s?

- 5.83 A particle travels on an elliptical path given by y2 = b2(1 − ax22 ) with constant speed v. Find the velocity of the particle when x = a/2 and y > 0 in terms of a, b, and v.

- 5.84 Aparticletravelsonapathinthe xy-plane given by y(x) = (1−e− mx )m. Make a plot of the path. It is known that the x coordinate of the particle is given by x(t) = t2 m/s2. What is the rate of change of speed of the particle? What angle does the velocity vector make with the positive x axis when t = 3s?

- 5.85 A particle starts at the origin in the xy-

plane, (x0 = 0, y0 = 0) and travels only in the positive xy quadrant. Its speed and x coordi-

nate are known to be v(t) = 1 + (s42 )t2 m/s and x(t) = t m/s, respectively. What is r(t) in cartesian coordinates? What are the velocity, acceleration, and rate of change of speed of the particle as functions of time? What kind of path is the particle on? What are the distance of the particle from the origin and its velocity and acceleration when x = 3m?

5.8 Spatial dynamics of a particle

- 5.86 What symbols do we use for the following quantities? What are the deﬁnitions of these quantities? Which are vectors and which are scalars? What are the SI and US standard units for the following quantities?


- a) linear momentum
- b) rate of change of linear momentum
- c) angular momentum
- d) rate of change of angular momentum
- e) kinetic energy
- f) rate of change of kinetic energy
- g) moment
- h) work
- i) power


- 5.87 Does angular momentum depend on reference point? (Assume that all candidate points are ﬁxed in the same Newtonian reference frame.)
- 5.88 Does kinetic energy depend on reference point? (Assume that all candidate points are ﬁxed in the same Newtonian reference frame.)
- 5.89 What is the relation between the dynamics ‘Linear Momentum Balance’ equation and the statics ‘Force Balance’ equation?
- 5.90 What is the relation between the dynamics‘AngularMomentumBalance’equationand the statics ‘Moment Balance’ equation?
- 5.91 A ball of mass m = 0.1kg is thrown from a height of h = 10m above the ground with velocity v = 120km/hıˆ − 120km/hˆ. What is the kinetic energy of the ball at its release?
- 5.92 A ball of mass m = 0.2kg is thrown from a height of h = 20m above the ground with velocity v = 120km/hıˆ−120km/hˆ −

10km/hkˆ. What is the kinetic energy of the ball at its release?

- 5.93 How do you calculate P, the power of all external forces acting on a particle, from the forces Fi and the velocity v of the particle?
- 5.94 A particle A has velocity vA and mass mA. A particle B has velocity vB = 2 vA and mass equal to the other mB = mA. What is the relationship between:

- a) LA and LB,
- b) HA/C and HB/C, and
- c) EKA and EKB?


- 5.95 A bullet of mass 50 g travels with a velocity v = 0.8km/sıˆ + 0.6km/sˆ. (a) What is the linear momentum of the bullet? (Answer in consistent units.)
- 5.96 A particle has position r = 4mıˆ+7mˆ, velocity v = 6m/sıˆ − 3m/sˆ, and acceleration a = −2m/s2ıˆ + 9m/s2ˆ. For each po-

sition of a point P deﬁned below, ﬁnd H P, the angular momentum of the particle with respect to the point P.

- a) r P = 4mıˆ + 7mˆ,
- b) r P = −2mıˆ + 7mˆ, and
- c) r P = 0mıˆ + 7mˆ,
- d) r P = 0


- 5.97 The position vector of a particle of mass 1 kg at an instant t is r = 2mıˆ − 0.5mˆ. If the velocity of the particle at this instant is v = −4m/sıˆ + 3m/sˆ, compute (a) the linear momentum L = m v and (b) the angular momentum ( HO = r/O × (m v)).
- 5.98 The position of a particle of mass m = 0.5kg is r(t) = sin(ωt)ıˆ + hˆ; where ω = 2rad/s,h = 2m,  = 2m, and r is measured from the origin.


- a) Find the kinetic energy of the particle at t = 0s and t = 5s.
- b) Findtherateofchangeofkineticenergy at t = 0s and t = 5s.


- 5.99 For a particle

EK =

- 1

- 2


m v2.

Why does it follow that E˙K = m v · a? [hint: write v2 as v · v and then use the product rule of differentiation.]

- 5.100 Consider a projectile of mass m at some instant in time t during its ﬂight. Let v be the velocity of the projectile at this instant (see the ﬁgure). In addition to the force of gravity, a drag force acts on the projectile. The drag force is proportional to the square of the speed (speed≡ | v| = v) and acts in the opposite direction. Find an expression for the net power of these forces (P = F · v) on the particle.

v

θ

problem 5.100:

(Filename:pﬁg2.3.rp3)

- 5.101 A 10gm wad of paper is tossed in the air (in a strong turbulent wind). The position, velocity, and acceleration of its center of mass are r = 3mıˆ+3mˆ+6mkˆ, v = −9m/sıˆ+ 24m/sˆ + 30m/skˆ, and a = −10m/s2ıˆ + 24m/s2ˆ + 32m/s2kˆ, respectively. Find the

linear momentum L and its rate of change L˙ of the the potato’s center of mass.

- 5.102 A 10gm wad of paper is tossed into the air. At a particular instant of interest, the position, velocity, and acceleration of its center of mass are r = 3mıˆ + 3mˆ + 6mkˆ, v = −9m/sıˆ + 24m/sˆ + 30m/skˆ, and

a = −10m/s2ıˆ + 24m/s2ˆ + 32m/s2kˆ, respectively. What is the translational kinetic energy of the wad at the instant of interest?

- 5.103 A 2 kg particle moves so that its position r is given by

r(t) = [5sin(at)ıˆ + bt2ˆ + ctkˆ]m

where a = π/sec,b = .25/sec2,c = 2/sec.

- a) Whatisthelinearmomentumoftheparticle at t = 1sec?
- b) What is the force acting on the particle at t = 1sec?


- 5.104 A particle A has mass mA and velocity vA. A particle B at the same location has mass mB = 2 mA and velocity equal to the other vB = vA. Point C is a reference point. What is the relationship between:


- a) LA and LB,
- b) HA/C and HB/C, and
- c) EKA and EKB?


- 5.105 A particle of mass m = 3kg moves in space. Its position, velocity, and acceleration at a particular instant in time are r = 2mıˆ+3mˆ+5mkˆ, v = −3m/sıˆ+8m/sˆ+ 10m/skˆ, and a = −5m/s2ıˆ + 12m/s2ˆ +

16m/s2kˆ, respectively. For this particle at the instant of interest, ﬁnd its:

- a) linear momentum L,
- b) rate of change of linear momentum L˙ ,
- c) angular momentum about the origin HO,
- d) rate of change of angular momentum about the origin H˙ O,
- e) kinetic energy EK, and
- f) rate of change of kinetic energy E˙K.


- 5.106 A particle has position r = 3mıˆ − 2mˆ+4mkˆ, velocity v = 2m/sıˆ−3m/sˆ+

- 7m/skˆ, and acceleration a = 1m/s2ıˆ −
- 8m/s2ˆ + 3m/s2kˆ. For each position of a point P deﬁned below, ﬁnd the rate of change of angular momentum of the particle with respect to the point P, H˙ P.


- a) r P = 3mıˆ − 2mˆ + 4mkˆ,
- b) r P = 6mıˆ − 4mˆ + 8mkˆ,
- c) r P = −9mıˆ + 6mˆ − 12mkˆ, and
- d) r P = 0


- 5.107 A particle of mass m = 5kg has position, velocity, and acceleration r = 2mˆ, v = 3m/sıˆ, and a = −7m/s2ıˆ, respectively, at a particular instant of interest. At the instant of interest ﬁnd its:


- a) linear momentum L,
- b) rate of change of linear momentum L˙ ,
- c) angular momentum about the origin HO,
- d) rate of change of angular momentum about the origin H˙ O,
- e) kinetic energy EK, and
- f) rate of change of kinetic energy E˙K.
- g) the net force F on the particle,
- h) the net moment on the particle about

the origin MO due to the applied forces, and

- i) rate of change of work W˙ = P done on the particle by the applied forces.


Particle FBD

###### F

problem 5.107: FBD of the particle

(Filename:pﬁgure1.1.part.fbd)

- 5.108 Aparticleofmassm = 6kgismovingin space. Its position, velocity, and acceleration at a particular instant in time are r = 1mıˆ − 2mˆ+4mkˆ, v = 3m/sıˆ+4m/sˆ−7m/skˆ,

and a = 5m/s2ıˆ + 11m/s2ˆ − 9m/s2kˆ, respectively. For this particle at the instant of interest, ﬁnd its:

- a) the net force F on the particle,
- b) the net moment on the particle about

the origin MO due to the applied forces, and

- c) the power P of the applied forces.


Particle FBD

F

problem 5.108: FBD of the particle

(Filename:pﬁgure1.1.part.fbdb)

- 5.109 A particle of mass m = 3kg is moving in the xz-plane. Its position, velocity, and acceleration at a particular instant of interest are r = 4mıˆ+2mkˆ, v = 3m/sıˆ−7m/skˆ, and

a = 3m/s2ıˆ−4m/s2kˆ, respectively. For this particle at the instant of interest, ﬁnd:

- a) the net force F on the particle,
- b) the net moment on the particle about

the origin MO due to the applied forces, and

- c) rate of change of work W˙ = P done on the particle by the applied forces.


Particle FBD

F

problem 5.109: FBD of the particle

(Filename:pﬁgure1.1.part.fbda)

- 5.110 A particle of mass m = 3kg is moving in the xy-plane. Its position, velocity, and acceleration at a particular instant of interest are r = 2mıˆ + 3mˆ, v = −3m/sıˆ + 8m/sˆ, and a = −5m/s2ıˆ + 12m/s2ˆ, respectively. For this particle at the instant of interest, ﬁnd its:


a) linear momentum L,

- b) rate of change of linear momentum L˙ ,
- c) angular momentum about the origin HO,
- d) rate of change of angular momentum about the origin H˙ O,
- e) kinetic energy EK, and
- f) rate of change of kinetic energy E˙K.


- 5.111 At a particular instant of interest, a particle of mass m1 = 5kg has position, velocity, and acceleration r1 = 3mıˆ, v1 = −4m/sˆ, and a1 = 6m/s2ˆ, respectively, and a particle of mass m2 = 5kg has position, velocity, and acceleration r2 = −6mıˆ, v2 = 5m/sˆ, and

a2 = −4m/s2ˆ, respectively. For the system of particles, ﬁnd its

- a) linear momentum L,
- b) rate of change of linear momentum L˙
- c) angular momentum about the origin HO,
- d) rate of change of angular momentum about the origin H˙ O,
- e) kinetic energy EK, and
- f) rate of change of kinetic energy E˙K.


- 5.112 A particle of mass m = 250 gm is shot straight up (parallel to the y-axis) from the xaxis at a distance d = 2m from the origin. The velocity of the particle is given by v = vˆ

where v2 = v02 − 2ah, v0 = 100m/s, a = 10m/s2 and h is the height of the particle from the x-axis.

- a) Find the linear momentum of the particle at the outset of motion (h = 0).
- b) Find the angular momentum of the particle about the origin at the outset of motion (h = 0).
- c) Find the linear momentum of the particle when the particle is 20m above the x-axis.
- d) Find the angular momentum of the particle about the origin when the particle is 20m above the x-axis.


- 5.113 For a particle, F = m a. Two forces


F1 and F2 act on a mass P as shown in the ﬁgure. P has mass 2lbm. The acceleration of the mass is somehow measured to be a = −2ft/s2ıˆ + 5ft/s2ˆ.

- a) Write the equation F = m a

in vector form (evaluating each side as much as possible).

- b) Write the equation in scalar form (use any method you like to get two scalar equations in the two unknowns F1 and F2).
- c) Write the equation in matrix form.


d) Find F1 = | F1| and F2 = | F2| by the

following methods:

- (a) from the scalar equations using hand algebra,
- (b) from the matrix equation using a computer, and
- (c) from the vector equation using a cross product.


y

P

45o

F1 F2

30o

x

problem 5.113:

(Filename:h1.63a)

z 1.2m

B

1.2m

T2

A

T1

1.2m

1.2m

y x

C

1m

1m

FBD

z 1.2m

1.2m

B

A

1.2m

T2 λˆ2

1.2m

T1λˆ1

y x

C

1m

1m

mg

problem 5.116:

(Filename:eﬁg1.2.7)

- 5.114 Three forces, F1 = 20Nıˆ − 5Nˆ, F2 = F2xıˆ + F2zkˆ, and F3 = F3λˆ , where λˆ = 12ıˆ +

√3

2 ˆ, act on a body with mass 2kg. The acceleration of the body is a = −0.2m/s2ıˆ + 2.2m/s2ˆ + 1.7m/s2kˆ. Writetheequation F = m a asscalarequations and solve them (most conveniently on a computer) for F2x, F2z, and F3.

- 5.115 The rate of change of linear momentum of a particle is known in two directions:

L˙ x = 20kgm/s2, L˙ y = −18kgm/s2 and unknown in the z direction. The forces act-

ing on the particle are F1 = 25Nıˆ+32Nˆ + 75Nkˆ, F2 = F2xıˆ+F2yˆ and F3 = −F3kˆ. Using F =

L˙ , separatethevectorequation into scalar equations in the x, y, and z directions. Solve these equations (maybe with the help of a computer) to ﬁnd F2x, F2y, and F3.

- 5.116 A block of mass 100 kg is pulled with two strings AC and BC. Given that the tensions


T1 = 1200N and T2 = 1500N, neglecting gravity, ﬁnd the magnitude and direction of the

acceleration of the block. [ F = m a ]

- 5.117 Neglecting gravity, the only force acting on the mass shown in the ﬁgure is from the string. Find the acceleration of the mass. Use the dimensions and quantities given. Recall that lbf is a pound force, lbm is a pound mass, and lbf/lbm = g. Use g = 32ft/s2. Note also that 32 + 42 + 122 = 132.

y

z

x

m

a = ?

m = 2.5 lbm

string pulley

3'

3 lbf 12'

4'

ıˆ

ˆ

kˆ

problem 5.117:

(Filename:pﬁgure.blue.4.1)

- 5.118 Three strings are tied to the mass shown withthedirectionsindicatedintheﬁgure. They


have unknown tensions T1, T2, and T3. There is no gravity. The acceleration of the mass is

kˆ)m/s2.

given as a = (−0.5ıˆ + 2.5ˆ + 13

- a) Given the free body diagram in the ﬁgure, write the equations of linear momentum balance for the mass.
- b) Find the tension T3. ∗


λˆ3 = 131 (−3ıˆ + 12ˆ + 4kˆ)

T3 = ?

z

kˆ

T3λˆ3

ˆ

ıˆ

y

m = 6kg

T2 T1

x

a = (−.5ıˆ + 2.5ˆ + 13kˆ)sm2

problem 5.118:

(Filename:pﬁgure.blue.1.2)

- 5.119 For part(c) of problem 4.23, assume now that the mass at A has non-zero acceleration of (1m/s2)ıˆ + (2m/s2)ˆ + (3m/s2)kˆ. Find the tension in the three ropes at the instant shown.
- 5.120 A small object (mass= 2kg) is being pulled by three strings as shown. The acceleration of the object at the position shown is a = −0.6ıˆ − 0.2ˆ + 2.0kˆ m/s2.

- a) Draw a free body diagram of the mass.
- b) Write the equation of linear momentum balance for the mass. Use λ’s as unit vectors along the strings.
- c) Find the three tensions T1, T2, and T3 at the instant shown. You may ﬁnd these tensions by using hand algebra with the scalar equations, using a computer with the matrix equation, or by using a cross product on the vector equation.


y x

z

C

m

T1

T2

T3

1m

4m

1.5m

2m

2m

problem 5.120:

(Filename:pﬁgure.s94h2p9)

- 5.121 Use a computer to draw a square with corners at (1,0), (0,−1), (−1,0), (0,1). This must be done with scientiﬁc software and not with a purely graphics program.
- 5.122 Draw a Circle on the Computer. We will be interested in keeping track of the motions of systems. A simple example is that of a particle going in circles at a constant rate. One can draw a circle quite well with a compass or with simple drawing programs. But, more complicated motions will be more difﬁcult. Draw a circle on the computer and label the drawing (using computer generated lettering) with your name and the date.


- a) You can program the circular shape any way that you think is fun (or any other way if you don’t feel like having a good time). Your circle should be round. Measure its length and width with a ruler,theyshouldbewithin10%ofeach other (mark the dimensions by hand on your drawing).
- b) A good solution will clearly document andexplainthecomputermethodology.


###### problem 5.126:

- 5.123 What curve is deﬁned by x = cos(t)2 and y = sin(t) ∗ cos(t) for 0 ≤ t ≤ π ? Try to ﬁgure it out without a computer. Make a computer plot.
- 5.124 Particle moves on a strange path. Given that a particle moves in the xy plane for 1.77s obeying r = (5m)cos2(t2/s2)ıˆ+(5m)sin(t2/s2)cos(t2/s2)ˆ

where x and y are the horizontal distance in meters and t is measured in seconds.

- a) Accuratelyplotthetrajectoryoftheparticle.
- b) Mark on your plot where the particle is going fast and where it is going slow. Explain how you know these points are the fast and slow places.


- 5.125 COMPUTER QUESTION: What’s the plot? What’s the mechanics question? Shown are shown some pseudo computer commands that are not commented adequately, unfortunately, and no computer is available at the moment.

- a) Draw as accurately as you can, assigning numbers etc, the plot that results from running these commands.
- b) See if you can guess a mechanical situation that is described by this program. Sketch the system and deﬁne the variables to make the script ﬁle agree with the problem stated.


ODEs = {z1dot = z2

z2dot = 0} ICs = {z1 =1, z2=1} Solve ODEs with ICs from t=0 to t=5 plot z2 and z1 vs t on the same plot

problem 5.125:

(Filename:pﬁgure.s94f1p3)

Here begins a series of problems concerning the motion of particles over noninﬁnitesimal time.

- 5.126 A particle is blown out through the uniform spiral tube shown, which lies ﬂat on a horizontal frictionless table. Draw the particle’s path after it is expelled from the tube. Defend your answer.


(Filename:pﬁgure.blue.29.1)

- 5.127 A ball going to the left with speed v0 bounces against a frictionless rigid ramp which is sloped at an angle θ from the horizontal. The collision is completely elastic (the coefﬁcient of restitution e = 1). Neglect gravity.

- a) Find the velocity of the ball after the collision. You may express your answer in terms of any combination of m, θ, v0, ıˆ, ˆ, nˆ, and λˆ .

nˆ = sinθıˆ + cosθˆ λˆ = −cosθıˆ + sinθˆ

ıˆ = sinθnˆ + −cosθλˆ ˆ = cosθnˆ + sinθλˆ

- b) For what value of θ would the vertical component of the speed be maximized?


v0

ball

θ

x

y

λˆ

nˆ

problem 5.127:

(Filename:ballramp)

- 5.128 Bungy Jumping. In a new safer bungy jumping system, people jump up from the ground while suspended from a rope that runs over a pulley at O and is connected to a stretched spring anchored at B. The pulley has negligible size, mass, and friction. For the situation shown the spring AB has rest length


0 = 2m and a stiffness of k = 200N/m. The inextensible massless rope from A to P has length r = 8m, the person has a mass of 100 kg. Take O to be the origin of an xy coordinate system aligned with the unit vectors ıˆ and ˆ

a) Assume you are given the position of thepersonr = xıˆ+yˆ andthevelocity ofthepersonv = x˙ıˆ+ ˙yˆ. Findheracceleration in terms of some or all of her position, her velocity, and the other parametersgiven. Usethenumbersgiven, where supplied, in your ﬁnal answer.

b) Given that bungy jumper’s initial position and velocity arer0 = 1mıˆ−5mˆ andv0 = 0write MATLAB commands to ﬁnd her position at t = π/

√2s.

c) Find the answer to part (b) with pencil and paper (a ﬁnal numerical answer is desired).

10 m A

###### ˆ

B

k

O

ıˆ

= 10 m/s2

g

m

ground, no contact after jump off

P

###### problem 5.128:

(Filename:s97p1.3)

- 5.129 A softball pitcher releases a ball of mass

- m upwards from her hand with speed v0 and angle θ0 from the horizontal. The only external force acting on the ball after its release is gravity.


- a) What is the equation of motion for the ball after its release?
- b) What are the position, velocity, and acceleration of the ball?
- c) What is its maximum height?
- d) At what distance does the ball return to the elevation of release?
- e) What kind of path does the ball follow and what is its equation y as a function of x?


- 5.130 Find the trajectory of a not-verticallyﬁred cannon ball assuming the air drag is proportional to the speed. Assume the mass is 10kg, g = 10m/s, the drag proportionality constant is C = 5N/(m/s). The cannon ball is launched at 100m/s at a 45 degree angle.

- • Draw a free body diagram of the mass.
- • Write linear momentum balance in vector form.
- • Solve the equations on the computer and plot the trajectory.
- • Solve the equations by hand and then use the computer to plot your solution.


- 5.131 See also problem 5.132. A baseball pitching machine releases a baseball of mass m


from its barrel with speed v0 and angle θ0 from the horizontal. The only external forces acting on the ball after its release are gravity and air resistance. The speed of the ball is given by v2 = x˙2 + y˙2. Taking into account air resistance on the ball proportional to its speed squared, Fd = −bv2eˆt, ﬁnd the equation of motionfortheball, afteritsrelease, incartesian coordinates. ∗

- 5.132 The equations of motion from problem 5.131 are nonlinear and cannot be solved in closed form for the position of the baseball. Instead, solvetheequationsnumerically. Make a computer simulation of the ﬂight of the baseball, as follows.

- a) Convert the equation of motion into a system of ﬁrst order differential equations. ∗
- b) Pick values for the gravitational constant g, the coefﬁcient of resistance b,

and initial speed v0, solve for the x and y coordinates of the ball and make a plots its trajectory for various initial angles θ0.

- c) UseEuler’s, Runge-Kutta, orothersuitable method to numerically integrate the system of equations.
- d) Use your simulation to ﬁnd the initial angle that maximizes the distance of travel for ball, with and without air resistance.
- e) If the air resistance is very high, what is a qualitative description for the curve described by the path of the ball?


- 5.133 In the arcade game shown, the object of the game is to propel the small ball from the ejector device at O in such a way that is passes through the small aperture at A and strikes the contact point at B. The player controls the angle θ at which the ball is ejected and the


initial velocity vo. The trajectory is conﬁned to the frictionless xy-plane, which may or may not be vertical. Find the value of θ that gives success. The coordinates of A and B are (2 , 2 ) and (3 , ), respectively, where is your favorite length unit.

y

A

θ

B

O

x

ejector device

problem 5.133:

(Filename:pﬁgure.blue.32.1)

##### 5.9 Central force motion and celestial mechanics

Experts note that none of these problems use polar or other fancy coordinates. Such descriptions come later in the text. At this point we wanttolayoutthebasicequationsandthequalitative features that can be found by numerical integration of the equations.

- 5.134 Under what circumstances is the angular momentum of a system, calculated relative to a point C which is ﬁxed in a Newtonian frame, conserved?
- 5.135 A satellite is put into an elliptical orbit around the earth (that is, you can assume the orbit is closed) and has a velocity vP at position P. Find an expression for the velocity vA at position A. The radii to A and P are, respec-

tively, rA and rP. [Hint: both total energy and angular momentum are conserved.]

![image 12](Introduction to Statics and Dynamics Problems_images/imageFile12.png)

A rA rP P

RE

vA

vP

problem 5.135:

(Filename:pﬁgure.blue.64.2)

- 5.136 The mechanics of nuclear war. A missile, modelled as a point, is launched on a ballistic trajectory from the surface of the earth. The force on the missile from the earth’s gravity is F = mgR2/r2 and is directed towards the center of the earth. When it is launched


from the equator it has speed v0 and in the direction shown, 45◦ from horizontal. For the purposes of this calculation ignore the earth’s rotation. That is, you can think of this problem as two-dimensional in the plane shown. If you need numbers, use the following values:

m = 1000kg is the mass of the missile, g = 10m/s2 is earth’s gravitational con-

stant at the earth’s surface,

R = 6,400,000m is the radius of the earth, and

v0 = 9000m/s r(t) is the distance of the missile from the

center of the earth.

a) Draw a free body diagram of the missile. Write the linear momentum balance equation. Break this equation into x and y components. Rewrite these equations as a system of 4 ﬁrst order ODE’s suitable for computer solution. Write appropriate initial conditions for the ODE’s.

b) Using the computer (or any other means) plot the trajectory of the rocket after it is launched for a time of 6670 seconds. [Use a much shorter time whendebuggingyourprogram.] Onthe same plot draw a (round) circle for the earth.

y

![image 13](Introduction to Statics and Dynamics Problems_images/imageFile13.png)

45o

![image 14](Introduction to Statics and Dynamics Problems_images/imageFile14.png)

x

problem 5.136:

(Filename:pﬁgure.s94q12p1)

- 5.137 A particle of mass 2kg moves in the horizontal xy-plane under the inﬂuence of a central force F = −k r (attraction force proportional to distance from the origin), where k = 200N/m and r is the position of the particle relative to the force center. Neglect all other forces.


- a) Show that circular trajectories are possible, and determine the relation be-

tween speed v and circular radius ro which must hold on a circular trajec-

tory. [hint: Write F = m a, break into x and y components, solve the separate scalar equations, pick fortuitous values for the free constants in your solutions.]

- b) It turns out that trajectories are in general elliptical, as depicted in the diagram.


Foraparticularellipticaltrajectorywith a = 1m and b = 0.8m, the velocity of the particle at point 1 is observed to be perpendicular to the radial direction, with magnitude v1, as shown. When the particle reaches point 2, its velocity is again perpendicular to the radial direction.

Determine the speed increment  v which would have to be added (instantaneously) to the particle’s speed at point 2 to transfer it to the circular trajectory through point 2 (the dotted curve). Express your answer in terms of v1.

|a|b<br><br>a|
|---|---|
|O|b|


2

v1

1

problem 5.137:

(Filename:pﬁgure.blue.72.1)

##### 5.10 Coupled motions of particles in space

- 5.138 Linear momentum balance for general systems with multiple interacting parts moving more or less independently reduces to F = m a if you interpret the terms correctly. What does this mean? What is F? What ism? What is a?
- 5.139 A particle of mass m1 = 6kg and a particle of mass m2 = 10kg are moving in the xyplane. At a particular instant of interest, particle 1 has position, velocity, and acceleration r1 = 3mıˆ+2mˆ, v1 = −16m/sıˆ+6m/sˆ,

and a1 = 10m/s2ıˆ −24m/s2ˆ, respectively, and particle 2 has position, velocity, and accel-

eration r2 = −6mıˆ − 4mˆ, v2 = 8m/sıˆ + 4m/sˆ, and a2 = 5m/s2ıˆ − 16m/s2ˆ, respectively.

- a) Find the linear momentum L and its

rate of change L˙ of each particle at the instant of interest.

- b) Find the linear momentum L and its

rate of change L˙ of the system of the two particles at the instant of interest.

- c) Find the center of mass of the system at the instant of interest.
- d) Findthevelocityandaccelerationofthe center of mass.


- 5.140 A particle of mass m1 = 5kg and a particle of mass m2 = 10kg are moving in space. At a particular instant of interest, particle 1 has position, velocity, and acceleration


r1 = 1mıˆ + 1mˆ v1 = 2m/sˆ

- a1 = 3m/s2kˆ

respectively, and particle 2 has position, velocity, and acceleration

r2 = 2mıˆ v2 = 1m/skˆ

- a2 = 1m/s2ˆ


respectively. For the system of particles at the instant of interest, ﬁnd its

- a) linear momentum L,
- b) rate of change of linear momentum L˙ ,
- c) angular momentum about the origin HO,
- d) rate of change of angular momentum about the origin H˙ O,
- e) kinetic energy EK, and
- f) rate of change of kinetic energy.


- 5.141 Two particles each of mass m are connected by a massless elastic spring of spring constant k and unextended length 2R. The systemslideswithoutfrictiononahorizontaltable, so that no net external forces act.

- a) Is the total linear momentum conserved? Justify your answer.
- b) Can the center of mass accelerate? Justify your answer.
- c) Draw free body diagrams for each mass.
- d) Derive the equations of motion for each mass in terms of cartesian coordinates.
- e) What are the total kinetic and potential energies of the system?
- f) For constant values and initial conditions of your choosing plot the trajectoriesofthetwoparticlesandofthecenter of mass (on the same plot).


x

y

θ R

m

m

R

problem 5.141:

(Filename:pﬁgure.blue.65.2)

- 5.142 Two ice skaters whirl around one another. They are connected by a linear elastic cord whose center is stationary in space. We wishtoconsiderthemotionofoneoftheskaters by modeling her as a mass m held by a cord that exerts k Newtons for each meter it is extended from the central position.


- a) Draw a free body diagram showing the forces that act on the mass is at an arbitrary position.
- b) Write the differential equations that describe the motion.
- c) Describe in physical and mathematical terms the nature of the motion for the three cases


- a) ω < √k/m ;

- b) ω =

√k/m ;

- c) ω > √k/m.


(You are not asked to solve the equation of motion.)

ice skater 1 θ

r

1

ice skater 2

0 (fixed)

problem 5.142:

(Filename:pﬁgure.blue.154.1)

- 5.143 Theory question. If you are given the total mass, the position, the velocity, and the acceleration of the center of mass of a system ofparticlescanyouﬁndtheangularmomentum

HO of the system, where O is not at the center of mass? If so, how and why? If not, then give

a reason and/or a counter example. ∗

- 5.144 The equation ( v 1 − v 2) · nˆ = e( v2 − v1) · nˆ relates relative velocities of two point masses before and after frictionless impact in the normal direction nˆ of the impact. If v 1 = v1xıˆ + v1yˆ, v 2 = −v0ıˆ, e = 0.5, v2 = 0, v1 = 2ft/sıˆ − 5ft/sˆ, and

nˆ = √12

(ıˆ +ˆ), ﬁnd the scalar equation relating the velocities in the normal direction.

- 5.145 See also problem 5.150. Assuming

θ, v0, and e to be known quantities, write the following equations in matrix form set up to

solve for v Ax and v Ay:

sinθv Ax + cosθv Ay = ev0 cosθ cosθv Ax − sinθv Ay = v0 sinθ.

- 5.146 Set up the following equations in matrix form and solve for vA and vB, if v0 = 2.6m/s, e = 0.8, mA = 2kg, and mB = 500g:

mAv0 = mAvA + mBvB −ev0 = vA − vB.

- 5.147 The following three equations are obtained by applying the principle of conservation of linear momentum on some system.

m0v0 = 24.0m/s ma − 0.67mBvB − 0.58mCvC 0 = 36.0m/s mA + 0.33mBvB + 0.3mCvC 0 = 23.3m/s mA − 0.67mBvB − 0.58mCvC.

Assume v0, vB, and vC are the only unknowns. Write the equations in matrix form set up to solve for the unknowns.

- 5.148 See also problem 5.149. The following three equations are obtained to solve for v Ax, v Ay, and v Bx: (v Bx − v Ax)cosθ = v Ay sinθ − 10m/s


v Ax sinθ = v Ay cosθ − 36m/s mBv Bx + mAv Ax = (−60m/s)mA.

Set up these equations in matrix form.

- 5.149 Solve for the unknowns v Ax , v Ay, and

v Bx in problem 5.148 taking θ = 50o, mA = 1.5mB and mB = 0.8kg. Use any computer program.

- 5.150 Using the matrix form of equations in Problem 5.145, solve for v Ax and v Ay if θ = 20o and v0 = 5ft/s.
- 5.151 Two frictionless masses mA = 2kg and mass mB = 5kg travel on straight collinear paths with speeds VA = 5m/s and VB = 1m/s, respectively. The masses collide since

VA > VB. Find the amount of energy lost in thecollisionassumingnormalmotionisdecoupled from tangential motion. The coefﬁcient of restitution is e = 0.5.

A B

VA VB

problem 5.151:

(Filename:Danef94s3q7)

- 5.152 Two frictionless pucks sliding on a plane collide as shown in the ﬁgure. Puck A is initially at rest. Given that (VB)i = 1.0m/s, (VA)i = 0, and (VA)f = 0.5m/s, ﬁnd the approach angle φ and rebound angle γ. The coefﬁcient of restitution is e = 0.9.

A

B

(VA)f

(VB)f (VA)i=0

(VB)i

φ

γ γ

problem 5.152:

(Filename:Danef94s2q8)

- 5.153 Reconsider problem 5.152. Given in-

stead that γ = 30◦, (VA)i = 0, and (VA)f = 0.5m/s, ﬁnd the initial velocity of puck B.

- 5.154 A bullet of mass m with initial speed v0 is ﬁred in the horizontal direction through


- block A of mass mA and becomes embedded in
- block B of mass mB. Each block is suspended bythinwires. ThebulletcausesAandBtostart


moving with speed of vA and vB respectively. Determine

- a) the initial speed v0 of the bullet in terms of vA and vB, ∗
- b) the velocity of the bullet as it travels from block A to block B,and ∗
- c) the energy loss due to friction as the bullet (1) moves through block A and


(2) penetrates block B. ∗

v0 m

mA mB A B

problem 5.154:

(Filename:pﬁgure.blue.23.1)

5.155 A massless spring with constant k is held compressed a distance δ from its relaxed length by a thread connecting blocks A and B which are still on a frictionless table. The blocks have mass mA and mB, respectively. The thread is suddenlybutgentlycut, theblocksﬂyapartand the spring falls to the ground. Find the speed of block A as it slides away. ∗

spring, k mA

mB

thread

problem 5.155:

(Filename:pﬁgure.blue.32.2)

Constrained straight line motion

##### 6.1 1-D constrained motionand pulleys

- 6.1 Write the following equations in matrix form for aB, aC, and T:

4aB + aC = 0 2T = −(25kg) aB

64kgm/s2 = T + (10kg) ac.

- 6.2 The two blocks, m1 = m2 = m, are connectedbyaninextensiblestring AB. Thestring

canonlywithstandatension Tcr. Findthemaximum value of the applied force P so that the string does not break. The sliding coefﬁcient of friction between the blocks and the ground is µ.

m1 m2

B P µ

g

problem 6.2:

(Filename:Danef94s3q5)

- 6.3 A train engine of mass m pulls and accelerates on level ground N cars each of mass m. The power of the engine is Pt and its speed is vt. Find the tension Tn between car n and car n+1. Assume there is no resistance to rolling for all of the cars. Assume the cars are connected with rigid links. ∗

n=1 n=2 n=N-2 n=N-1 n=N

m m m m m

problem 6.3:

(Filename:pﬁgure.newtrain)

- 6.4 Two blocks, each of mass m, are connected together across their tops by a massless string of length S; the blocks’ dimensions are small compared to S. They slide down a slope of angle θ. Do not neglect gravity but do neglect friction.


- a) Draw separate free body diagrams of each block, the string, and the system of the two blocks and string.
- b) Write separate equations for linear momentum balance for each block, the string, and the system of blocks and string.
- c) What is the acceleration of the center of mass of the two blocks?


- d) What is the force in the string?
- e) What is the speed of the center of mass for the two blocks after they have traveledadistanced downtheslope,having started from rest. [Hint: You need to dot your momentum balance equations with a unit vector along the ramp in order to reduce this problem to a problem in one dimensional mechanics.]


m

s

m θ

problem 6.4:

(Filename:pﬁgure.blue.27.1)

6.5 Two blocks, each of mass m, are connected together across their tops by a massless string of length S; the blocks’ dimensions are small compared to S. They slide down a slope of angle θ. The materials are such that the coefﬁcient of dynamic friction on the top block is µ and on the bottom block is µ/2.

- a) Draw separate free body diagrams of each block, the string, and the system of the two blocks and string.
- b) Write separate equations for linear momentum balance for each block, the string, and the system of blocks and string.
- c) What is the acceleration of the center of mass of the two blocks?
- d) What is the force in the string?
- e) What is the speed of the center of mass for the two blocks after they have traveledadistanced downtheslope,having started from rest.
- f) How would your solutions to parts (a) and (c) differ in the following two variations: i.) If the two blocks were interchanged with the slippery one on top or ii.) if the string were replaced by a massless rod? Qualitative responses to this part are sufﬁcient.


m

s

m θ

problem 6.5:

(Filename:pﬁgure.blue.27.1a)

- 6.6 Acartofmass M, initiallyatrest, canmove horizontally along a frictionless track. When t = 0, a force F is applied as shown to the cart. During the acceleration of M by the force F, a small box of mass m slides along the cart from the front to the rear. The coefﬁcient of friction between the cart and box is µ, and it is assumed that the acceleration of the cart is sufﬁcient to cause sliding.

- a) Draw free body diagrams of the cart, the box, and the cart and box together.
- b) Write the equation of linear momentum balance for the cart, the box, and the system of cart and box.
- c) Show that the equations of motion for the cart and box can be combined to give the equation of motion of the mass center of the system of two bodies.
- d) Find the displacement of the cart at the timewhentheboxhasmovedadistance


along the cart.

m F M

|m|
|---|


no friction

problem 6.6:

(Filename:pﬁgure.blue.28.1)

- 6.7 A motor at B allows the block of mass m = 3kg shown in the ﬁgure to accelerate downwards at 2m/s2. There is gravity. What is the tension in the string AB?

|A| |
|---|---|
|m| |


B

problem 6.7:

(Filename:pﬁgure.blue.12.2)

- 6.8 For the mass and pulley system shown in the ﬁgure, the point of application A of the force moves twice as fast as the mass. At some instant in time t, the speed of the mass is x˙ to the left. Find the input power to the system at time t.


A

F

m

problem 6.8:

(Filename:pﬁg2.3.rp8)

6.9Pulleyandmasses. Twomassesconnected by an inextensible string hang from an ideal pulley.

- a) Find the downward acceleration of mass B. Answer in terms of any or all ofmA, mB, g, andthepresentvelocities of the blocks. As a check, your answer should give aB = g when mA = 0 and aB = 0 when mA = mB. ∗ .
- b) Find the tension in the string. As a check, your answer should give T = mBg = mAg when mA = mB and T = 0 when mA = 0. ∗


g

mA

mB

problem 6.9:

(Filename:pﬁgure3.f95p1p2)

- 6.10 The blocks shown are released from rest. Make reasonable assumptions about strings, pulleys, string lengths, and gravity.

- a) What is the acceleration of block A at t = 0+ (just after release)?
- b) What is the speed of block B after it has fallen 2 meters?


mA = mB = m

A

B

problem 6.10:

(Filename:pﬁgure.blue.29.2)

- 6.11 What is the acceleration of block A? Use g = 10m/s2. Assume the string is massless and that the pulleys are massless, round, and have frictionless bearings.

2 kg

32 kg

||A|
|---|
|
|---|


||B|
|---|
|
|---|


ıˆ

ˆ

problem 6.11:

(Filename:pﬁgure.f93q4)

- 6.12 For the system shown in problem 6.9, ﬁnd the acceleration of mass B using energy balance (P = E˙K).
- 6.13 For the various situations pictured, ﬁnd the acceleration of the mass A and the point B shown using balance of linear momentum


( F = m a). Deﬁne any variables, coordinates or sign conventions that you need to do your calculations and to deﬁne your solution.

∗

- (a) F

m

- (b)

m

- (c)

m

- (d)


m A B

F

B

A

F

A

B

B

F

A

problem 6.13:

(Filename:pulley1)

- 6.14 For each of the various situations pictured in problem 6.13 ﬁnd the acceleration of the

mass using energy balance (P = E˙K). Deﬁne any variables, coordinates, or sign conventions that you need to do your calculations and to deﬁne your solution.

- 6.15 What is the ratio of the acceleration of pointAtothatofpointBineachconﬁguration? In both cases, the strings are inextensible, the pulleys massless, and the mass and force the same. ∗

m

A F

m B F

problem 6.15:

(Filename:sum95.p1.p3)

- 6.16 See also problem 6.17. Find the acceleration of points A and B in terms of F and m. Assume that the carts stay on the ground, have good (frictionless) bearings, and have wheels of negligible mass.


A B F

||m|
|---|
|
|---|


||m|
|---|
|
|---|


problem 6.16:

(Filename:pﬁgure.s94q5p1)

- 6.17 For the situation pictured in problem 6.16 ﬁnd the accelerations of the two masses using

energy balance (P = E˙K). Deﬁne any variables, coordinates, orsignconventionsthatyou need to do your calculations and to deﬁne your solution.

- 6.18 See also problem 6.19. For the various situations pictured, ﬁnd the acceleration of the mass A and the point B shown using balance of linear momentum ( F = m a). Deﬁne any variables, coordinates or sign conventions that you need to do your calculations and to deﬁne your solution.


- a) ∗
- b) ∗


F

- (b)

(a)

A B

m1

m2

A

B 30o

60o

g

||m|
|---|
|
|---|


- (c)


A B

F

| | |
|---|---|
| | |
| | |


||m|
|---|
|
|---|


massless

problem 6.18:

(Filename:pulley4)

- 6.19Forthevarioussituationspicturedinproblem 6.18 ﬁnd the acceleration of the mass using energy balance (P = E˙K). Deﬁne any variables, coordinates, or sign conventions that you need to do your calculations and to deﬁne your solution.
- 6.20 A person of mass m, modeled as a rigid body is sitting on a cart of mass M > m and pullingthemasslessinextensiblestringtowards herself. The coefﬁcient of friction between her seat and the cart is µ. All wheels and pulleys are massless and frictionless. Point B is attached to the cart and point A is attached to the rope.


a) If you are given that she is pulling rope in with acceleration a0 relative to herself(thatis,aA/B ≡ aA−aB = −a0ıˆ) and that she is not slipping relative to the cart, ﬁnd aA. (Answer in terms of some or all of m, M,g,µ,ıˆ and a0.)

- b) Find the largest possible value of a0 without the person slipping off the cart? (Answer in terms of some or all of m, M, g and µ. You may assume her legs get out of the way if she slips backwards.)
- c) If instead, m < M, what is the largest possible value of a0 without the person slipping off the cart? (Answer in terms of some or all of m, M, g and µ. You may assume her legs get out of the way if she slips backwards.)


###### ˆ

g

ıˆ

ideal pulley

m A

M

B

problem 6.20: Pulley.

(Filename:s97p2.2)

- 6.21 Two blocks and a pulley. Two equal masses are stacked and tied together by the pulley as shown. All bearings are frictionless. All rotating parts have negligible mass. Find

- a) the acceleration of point A, and
- b) the tension in the line.


m

m

F

B

A

C

ıˆ

ˆ

problem 6.21:

(Filename:p.s96.p1.1)

- 6.22 The pulleys are massless and frictionless. Neglect air friction. Include gravity. x measures the vertical position of the lower mass fromequilibrium. y measurestheverticalposition of the upper mass from equilibrium. What is the natural frequency of vibration of this system? ∗


k

m

y

m

x

problem 6.22:

(Filename:pﬁgure.s95q4)

- 6.23 See also problem 6.24. For the situation pictured, ﬁnd the acceleration of the mass A and the points B and C shown using balance of linear momentum ( F = m a). Deﬁne any variables, coordinates or sign conventions that you need to do your calculations and to deﬁne your solution. [Hint: the situation with point C is tricky and the answer is subtle.]

A

B

| | |
|---|---|
| | |


C m

F

problem 6.23:

(Filename:pulley2)

- 6.24 For situation pictured in problem 6.23, ﬁnd the acceleration of point A using energy

balance (P = E˙K). Deﬁne any variables, coordinates, or sign conventions that you need to do your calculations and to deﬁne your solution.

- 6.25 Pulley and spring. For the mass hanging at the right, ﬁnd the period of oscillation. Assume a massless pulley with good bearings. The massless string is inextensible. Only vertical motion is of interest. There is gravity. [Hint: DrawFBD,carefullykeeptrackofstring length to ﬁgure spring stretch, set up equations of motion and solve them.]


k g

| | |
|---|---|
||m|
|---|
| |


problem 6.25:

(Filename:pﬁgure.s94h4p4)

- 6.26 The spring-mass system shown (m = 10 slugs (≡ lb·sec2/f t), k = 10lb/f t) is excited by moving the free end of the cable vertically according to δ(t) = 4sin(ωt)in, as shown in theﬁgure. Assumingthatthecableisinextensibleandmasslessandthatthepulleyismassless, do the following.

- a) Derive the equation of motion for the block in terms of the displacement x from the static equilibrium position, as shown in the ﬁgure.
- b) Ifω = 0.9rad/s, checktoseeifthepulley is always in contact with the cable (ignore the transient solution).


Static equilibrium position at δ = 0 and x = 0

x

δ(t)

g

m

problem 6.26:

(Filename:pﬁgure.blue.151.1)

- 6.27 Theblockofmassm hangingonthespring with constant k and a string shown in the ﬁgure is forced (by an unseen agent) with the force F = A sin(ωt). (Do not neglect gravity). The pulley is massless.

- a) What is the differential equation governing the motion of the block? You may assume that the only motion is vertical motion. ∗
- b) Given A, m and k, for what values of ω would the string go slack at some point in the cyclical motion? (You should neglect the homogeneous solution to the differential equation.) ∗


m

F = A sin(ωt)

k

problem 6.27:

(Filename:pﬁgure.blue.155.1)

- 6.28 Block A, with mass mA, is pulled to the right a distance d from the position it would have if the spring were relaxed. It is then released from rest. Assume ideal string, pulleys and wheels. The spring has constant k.


a) What is the acceleration of block A just

after it is released (in terms of k, mA, and d)? ∗

b) What is the speed of the mass when the mass passes through the position where the spring is relaxed? ∗ .

B C

| |A|
|---|---|
| | |
| | |


D E G

x ıˆ

problem 6.28:

(Filename:pﬁgure.f93q5)

- 6.29 What is the static displacement of the mass from the position where the spring is just relaxed?

m

A

d

k, L0 g

problem 6.29:

(Filename:pulley3.a)

- 6.30 For the two situations pictured, ﬁnd the acceleration of point A shown using balance of linear momentum ( F = m a). Assuming both masses are deﬂected an equal distance from the position where the spring is just relaxed, how much smaller or bigger is the acceleration of block (b) than of block(a). Deﬁne any variables, coordinate system origins, coordinates or sign conventions that you need to do your calculations and to deﬁne your solution.

A

L

K,L0

- (a)

m

A

d

K,L0

- (b)


m

problem 6.30:

(Filename:pulley3)

- 6.31 For each of the various situations pictured in problem 6.30, ﬁnd the acceleration of the


mass using energy balance (P = E˙K). Deﬁne any variables, coordinates, or sign conventions that you need to do your calculations and to deﬁne your solution.

##### 6.2 2D and 3D forces even thoughthemotionisstraight

- 6.32 Mass pulled by two strings. F1 and F2 are applied so that the system shown accelerates to the right at 5m/s2 (i.e., a = 5m/s2ıˆ+ 0ˆ) and has no rotation. The mass of D and

forces F1 and F2 are unknown. What is the tension in string AB?

A

C

B m

D

4

4

3

3

- F1
- F2


ıˆ

ˆ

problem 6.32:

(Filename:pg9.1)

- 6.33 A point mass m is attached to a piston by two inextensible cables. The piston has upwards acceleration ayˆ. There is gravity. In terms of some or all of m, g,d, and ay ﬁnd the tension in cable AB. ∗

| | |
|---|---|
| | |


9d

6d

5d A

B

C

ıˆ

ˆ

g

problem 6.33:

(Filename:ch3.13)

- 6.34 A point mass of mass m moves on a frictional surface with coefﬁcient of friction µ and is connected to a spring with constant k and unstretched length . There is gravity. At the instant of interest, the mass is at a distance x to the right from its position where the spring is unstretched and is moving with x˙ > 0 to the right.


- a) Draw a free body diagram of the mass at the instant of interest.
- b) Attheinstantofinterest, writetheequation of linear momentum balance for the block evaluating the left hand side as explicitly as possible. Let the acceleration of the block be a = x¨ıˆ.


x

m

problem 6.34:

(Filename:ch2.10a)

- 6.35 Find the tension in two strings. Consider the mass at B (2kg) supported by two strings in the back of a truck which has acceleration of 3m/s2. Use your favorite value for the gravitational constant. What is the tension TAB in the string AB in Newtons?

1m

1m

B

A C

x

y

problem 6.35:

(Filename:pﬁgure.s94h2p8)

- 6.36 Guyed plate on a cart A uniform rectangular plate ABCD of mass m is supported by a rod DE and a hinge joint at point B. The dimensions are as shown. The cart has accel-

eration axıˆ due to a force F. There is gravity. What must the acceleration of the cart be in order for the rod DE to be in tension? ∗

| | |
|---|---|
| | |


- A
- B


D

C E

F

2

3 4

cart

ıˆ

ˆ

problem 6.36: Uniform plate supported by a hinge and a cable on an accelerating cart.

(Filename:tﬁgure3.2D.a.guyed)

- 6.37 A uniform rectangular plate of mass m is supported by two inextensible cables AB and CD and by a hinge at point E on the cart as


shown. The cart has acceleration axıˆ due to a force not shown. There is gravity.

- a) Draw a free body diagram of the plate.
- b) Write the equation of linear momentum balance for the plate and evaluate the left hand side as explicitly as possible.
- c) Write the equation for angular momentum balance about point E and evaluate the left hand side as explicitly as possible.


a

3a 3a

D

A

2a

B C

G

2a

| | |
|---|---|
| | |


###### ˆ

E ıˆ

###### problem 6.37:

(Filename:ch2.12)

- 6.38 See also problem 6.67. A uniform rectangular plate of mass m is supported by an inextensible cable CD and a hinge joint at point E on the cart as shown. The hinge joint is attached to a rigid column welded to the ﬂoor of the cart. The cart is at rest. There is gravity. Find the tension in cable CD.

3 3

2 G

| | |
|---|---|
| | |


A

B C

D

E ıˆ

ˆ 2

problem 6.38:

(Filename:ch3.11.b)

- 6.39 A uniform rectangular plate of mass m is supported by an inextensible cable AB and a hinge joint at point E on the cart as shown. The hinge joint is attached to a rigid column welded to the ﬂoor of the cart. The cart has

acceleration axıˆ. There is gravity. Find the tension in cable AB. (What’s ‘wrong’ with this problem? What if instead point B was at the bottom left hand corner of the plate?) ∗

3 3

2 G

| | |
|---|---|
| | |


A

B

C

D

E

a = axıˆ

ıˆ

ˆ 2

problem 6.39:

(Filename:ch3.11a)

- 6.40 See also 6.41. A block of mass m is sitting on a frictionless surface and acted upon at point E by the horizontal force P through the center of mass. Draw a free body diagram of the block. There is gravity. Find the acceleration of the block and reactions on the block at points A and B.


2b

b

C D

d

E P

| | |
|---|---|
| | |


G

2d

A B

problem 6.40:

(Filename:ch3.9)

- 6.41 Reconsider the block in problem 6.40. This time, ﬁnd the acceleration of the block and the reactions at A and B if the force P is applied instead at point D. Are the acceleration and the reactions on the block different from those found if P is applied at point E?
- 6.42 A block of mass m is sitting on a frictional surface and acted upon at point D by the horizontal force P. The block is resting on a sharp edge at point B and is supported by an ideal wheel at point A. There is gravity. Assuming the block is sliding with coefﬁcient of friction µ at point B, ﬁnd the acceleration of the block and the reactions on the block at points A and B.

| | |
|---|---|
| | |


b

2b

2d

d

C D

A B

G

P

E

problem 6.42:

(Filename:ch3.12)

- 6.43 A force FC is applied to the corner C of a box of weight W with dimensions and center of gravity at G as shown in the ﬁgure. The coefﬁcient of sliding friction between the ﬂoor and the points of contact A and B is µ. Assuming

that the box slides when FC is applied, ﬁnd the acceleration of the box and the reactions at A

and B in terms of W, FC, θ, b, and d.

| | |
|---|---|
| | |


b

2b

b

C d

A B

G

FC θ

problem 6.43:

(Filename:Mikes92p3)

- 6.44 Forces of rod on a cart. A uniform rod


with mass mr rests on a cart (mass mc) which is being pulled to the right. The rod is hinged at one end (with a frictionless hinge) and has no friction at the contact with the cart. The cart is rolling on wheels that are modeled as having no mass and no bearing friction (ideal massless wheels). Find:

- a) The force on the rod from the cart at

point B. Answer in terms of g, mr, mc, θ and F.

- b) The force on the rod from the cart at point A.


A

θ

B F

problem 6.44:

(Filename:pﬁgure.s94h3p3)

- 6.45 At the instant shown, the mass is moving to the right at speed v = 3m/s. Find the rate of work done on the mass.

m = 10 kg h

frictionless

F = 50 N x

problem 6.45:

(Filename:pﬁg2.3.rp9)

- 6.46 The box shown in the ﬁgure is dragged in the x-direction with a constant acceleration a = 0.5m/s2ıˆ. At the instant shown, the velocity of (every point on) the box is v = 0.8m/sıˆ.

- a) Find the linear momentum of the box.
- b) Find the rate of change of linear momentum of the box.
- c) Find the angular momentum of the box about the contact point O.
- d) Find the rate of change of angular momentum of the box about the contact point O.


x

y

| | |
|---|---|
| | |


O

1m

m = 2 kg

2m

30o

problem 6.46:

(Filename:pﬁgure3.mom.rp1)

- 6.47 (See also problem 4.15.) The groove and disk accelerate upwards, a = aˆ. Neglecting gravity, what are the forces on the disk due to the groove?


r

y

θ1 θ2 x

problem 6.47:

(Filename:ch2.5.ba)

6.48 The following problems concern a box thatisinthebackofapickuptruck. Thepickup truck is accelerating forward at an acceleration of at. The truck’s speed is vt. The box has sharp feet at the front and back ends so the only place it contacts the truck is at the feet. The center of mass of the box is at the geometric center of the box. The box has height h, length

and depth w (into the paper.) Its mass is m. There is gravity. The friction coefﬁcient between the truck and the box edges is µ.

In the problems below you should express your solutions in terms of the variables given in the ﬁgure, , h, µ, m, g, at, and vt. If any variables do not enter the expressions comment on why they do not. In all cases you may assume that the box does not rotate (though it might be on the verge of doing so).

- a) Assuming the box does not slide, what is the total force that the truck exerts on the box (i.e. the sum of the reactions at A and B)?
- b) Assuming the box does not slide what are the reactions at A and B? [Note: You cannot ﬁnd both of them without additional assumptions.]
- c) Assuming the box does slide, what is the total force that the truck exerts on the box?
- d) Assuming the box does slide, what are the reactions at A and B?
- e) Assuming the box does not slide, what is the maximum acceleration of the truck for which the box will not tip over (hint: just at that critical acceleration what is the vertical reaction at B?)?
- f) What is the maximum acceleration of the truck for which the block will not slide?
- g) The truck hits a brick wall and stops instantly. Does the block tip over?


Assuming the block does not tip over, how far does it slide on the truck before stopping (assume the bed of the truck is sufﬁciently long)?

###### ˆ

g

y ıˆ

| |m cm<br><br>|µ at vt<br><br>A B<br><br>| | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
|h<br><br>|
|---|---|---|
||µ at vt<br><br>A B<br><br>| | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | |


x

|µ at vt<br><br>A B<br><br>| | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |


###### problem 6.48:

(Filename:pﬁgure.blue.22.1)

- 6.49 A collection of uniform boxes with various heights h and widths w and masses m sit on a horizontal conveyer belt. The acceleration a(t) of the conveyer belt gets extremely large sometimes due to an erratic over-powered motor. Assume the boxes touch the belt at their left and right edges only and that the coefﬁcient of friction there is µ. It is observed that some boxes never tip over. What is true about µ, g, w, h, and m for the boxes that always maintain contact at both the right and left bottom edges? (Write an inequality that involves some or all of these variables.)

motor

problem 6.49:

(Filename:pﬁgure.f93q3)

- 6.50 Afterfailureofhernormalbrakes, adriver pulls the emergency brake of her old car. This actionlockstherearwheels(frictioncoefﬁcient


= µ) but leaves the well lubricated and light front wheels spinning freely. The car, braking inadequately as is the case for rear wheel braking, hits a stiff and slippery phone pole which compresses the car bumper. The car bumper is modeled here as a linear spring (constant = k, rest length = l0, present length = ls). The car is still traveling forward at the moment of interest. The bumper is at a height hb above the ground. Assume that the car, excepting the bumper, is a non-rotating rigid body and that the wheels remain on the ground (that is, the bumperiscompliantbutthesuspensionisstiff).

• What is the acceleration of the car in terms of g, m, µ, lf , lr, k, hb, hcm, l0, and ls (and any other parameters if needed)?

y

x

| | |
|---|---|
| | |


hcm lr lf ls hb

C D

problem 6.50:

(Filename:pﬁgure.s94q4p1)

6.51 Car braking: front brakes versus rear brakesversusallfourbrakes. Thereareafew puzzlesindynamicsconcerningthedifferences between front and rear braking of a car. Here is one you can deal with now. What is the peak deceleration of a car when you apply: the front brakes till they skid, the rear brakes till they skid, and all four brakes till they skid? Assume that the coefﬁcient of friction between rubber and road is µ = 1 (about right, the coefﬁcient of friction between rubber and road varies between about .7 and 1.3) and that g = 10m/s2 (2% error). Pick the dimensions and mass of the car, but assume the center of mass height h is above the ground. The height h, should be lessthanhalfthewheelbasew, thedistancebetween the front and rear wheel. Further assume that the CM is halfway between the front and back wheels (i.e., lf = lr = w/2). Assume also that the car has a stiff suspension so the car does not move up or down or tip during braking; i. e., thecardoesnotrotateinthe xy-plane. Neglect the mass of the rotating wheels in the linear and angular momentum balance equations. Treat this problem as two-dimensional problem; i. e., the car is symmetric left to right, does not turn left or right, and that the left and right wheels carry the same loads. To organize your work, here are some steps to follow.

- a) Draw a FBD of the car assuming rear wheel is skidding. The FBD should show the dimensions, the gravity force, whatyouknowaprioriabouttheforces on the wheels from the ground (i.e.,

that the friction force Fr = µNr, and that there is no friction at the front wheels), and the coordinate directions. Labelpointsofinterestthatyouwilluse in your momentum balance equations. (Hint: also draw a free body diagram of the rear wheel.)

- b) Write down the equation of linear momentum balance.
- c) Writedowntheequationofangularmomentum balance relative to a point of your choosing. Some particularly usefulpointstouseare: thepointabovethe front wheel and at the height of the center of mass; the point at the height of the center of mass, behind the rear wheel that makes a 45 degree angle line down to the rear wheel ground contact point; and the point on the ground straight under the front wheel that is as deep as the wheel base is long.
- d) Solvethemomentumbalanceequations for the wheel contact forces and the deceleration of the car. If you have used any or all of the recommendations from part (c) you will have the pleasure of only solving one equation in one unknown at a time. ∗
- e) Repeat steps (a) to (d) for front-wheel skidding. Note that the advantageous points to use for angular momentum balance are now different. Does a car


stop faster or slower or the same by skidding the front instead of the rear wheels? Would your solution to (e) be

different if the center of mass of the car was at ground level(h=0)? ∗

- f) Repeat steps (a) to (d) for all-wheel skidding. There are some shortcuts here. You determine the car deceleration without ever knowing the wheel reactions (or using angular momentum balance) if you look at the linear momentum balance equations carefully. ∗
- g) Does the deceleration in (f) equal the sum of the deceleration in (d) and (e)? Why or why not? ∗
- h) What peculiarity occurs in the solution for front-wheel skidding if the wheel baseistwicetheheightoftheCMabove ground and µ = 1? ∗
- i) What impossibility does the solution predict if the wheel base is shorter than twice the CM height? What wrong assumption gives rise to this impossibility? What would really happen if one tried to skid a car this way? ∗


y

x

| | |
|---|---|
| | |


h C D

lr lf

problem 6.51:

(Filename:pﬁgure.s94h3p6)

- 6.52 At time t = 0, the block of mass m is released at rest on the slope of angle φ. The coefﬁcient of friction between the block and slope is µ.

- a) Whatistheaccelerationoftheblockfor µ > 0? ∗
- b) Whatistheaccelerationoftheblockfor µ = 0? ∗
- c) Find the position and velocity of the

block as a function of time for µ > 0.

∗

- d) Find the position and velocity of the


block as a function of time for µ = 0.

∗

φ

m

µ

g

problem 6.52:

(Filename:Danef94s1q5)

- 6.53 Asmallblockofmassm1 isreleasedfrom rest at altitude h on a frictionless slope of angle α. Attheinstantofrelease, anothersmallblock of mass m2 is dropped vertically from rest at


the same altitude. The second block does not interact with the ramp. What is the velocity of the ﬁrst block relative to the second block after t seconds have passed?

d

g

m1 m2

h

t=0

α

problem 6.53:

(Filename:ch8.7)

- 6.54 Block sliding on a ramp with friction. A square box is sliding down a ramp of angle θ with instantaneous velocity vıˆ . It is assumed to not tip over.

- a) What is the force on the block from the ramp at point A? Answer in terms of any or all of θ, , m, g, µ, v, ıˆ , and ˆ . As a check, your answer should reduce to mg2 ˆ when θ = µ = 0. ∗

- b) In addition to solving the problem by hand, see if you can write a set of computer commands that, if θ, µ, , m, v and g were speciﬁed, would give the correct answer.
- c) Assuming θ = 80◦ and µ = 0.9, can the box slide this way or would it tip over? Why? ∗


µ

µ

A

m

B

G

θ

ıˆ

ˆ

ˆ

ı ˆ

problem 6.54:

(Filename:pﬁgure3.f95p1p1)

- 6.55 A coin is given a sliding shove up a ramp with angle φ with the horizontal. It takes twice as long to slide down as it does to slide up. What is the coefﬁcient of friction µ between the coin and the ramp. Answer in terms of some or all of m, g,φ and the initial sliding velocity v.
- 6.56Askiddingcar. Whatisthebrakingacceleration of the front-wheel braked car as it slides downhill. Expressyouranswerasafunctionof any or all of the following variables: the slope θ of the hill, the mass of the car m, the wheel base , and the gravitational constant g. Use µ = 1. ∗


/4

/2

cm

ˆ

ıˆ

θ

problem 6.56: A car skidding downhill on a slope of angle θ

(Filename:pﬁgure3.car)

- 6.57 Two blocks A and B are pushed up a frictionless inclined plane by an external force F as shown in the ﬁgure. The coefﬁcient of friction between the two blocks is µ = 0.2. The masses of the two blocks are mA = 5kg and mB = 2kg. Find the magnitude of the maximum allowable force such that no relative slip occurs between the two blocks.

30o

µ=0.2 µ=0

A

B

F

problem 6.57:

(Filename:summer95f.1)

- 6.58 A bead slides on a frictionless rod. The

spring has constant k and rest length 0. The bead has mass m.

- a) Given x and x˙ ﬁnd the acceleration of the bead (in terms of some or all of

D, 0, x, x˙,m,k and any base vectors that you deﬁne).

- b) If the bead is allowed to move, as constrained by the slippery rod and the spring, ﬁnd a differential equation that must be satisﬁed by the variable x. (Do nottrytosolvethissomewhatuglynonlinear equation.)
- c) In the special case that 0 = 0∗ ﬁnd how long it takes for the block to return to its starting position after release with no initial velocity at x = x0.


D

x

m

k, 0

problem 6.58:

(Filename:p.s96.p1.2)

- 6.59 A bead oscillates on a straight frictionless wire. The spring obeys the equation F = k


( − o), where = length of the spring and 0 is the ’rest’ length. Assume

###### x(t = 0) = x0, x˙(t = 0) = 0.

- a) Write a differential equation satisﬁed by x(t).
- b) What is x˙ when x = 0? [hint: Don’t try to solve the equation in (a)!]
- c) Note the simpliﬁcation in (a) if o = 0 (spring is then a so-called “zero– length” spring).
- d) For this special case ( o = 0) solve the equation in (a) and show the result agrees with (b) in this special case.


D

m

x

problem 6.59:

(Filename:pﬁgure.blue.60.1)

- 6.60 Acartonaspringyleash. Acart B (mass m) rolls on a frictionless level ﬂoor. One end of an inextensible string is attached to the the cart. The string wraps around a pulley at point A and the other end is attached to a spring with constant k. When the cart is at point O, it is in static equilibrium. The spring and room height are such that the spring would be relaxed if the end of the cart B was in the air at the ceiling pulley, point A. The ceiling height is h. The gravitational constant is g. The cart is pulled a horizontal distance d from the center of the room (at O) and released.

- a) Assuming that the cart never leaves the ﬂoor, what is the speed of the cart when it passes through the center of the room, in terms of m, h, g and d. ∗
- b) Does the cart undergo simple harmonic motion for small or large oscillations (specify which if either)? (Simple harmonic motion is when position is sinewave and/or cosine-wave function of time.) ∗


k

m

h

d

A

O

B g

problem 6.60:

(Filename:cartosc)

- 6.61 The cart moves to the right with constant acceleration a. The ball has mass m.


Thespringhasunstretchedlength 0 andspring constantk. Assumingtheballisstationarywith respect to the cart ﬁnd the distance from O to A in terms of k, 0, and a . [Hint: ﬁnd θ ﬁrst.]

O

A

θ

problem 6.61:

(Filename:Danef94s3q6)

- 6.62 Consider a person, modeled as a rigid body, riding an accelerating motorcycle (2-D). The motorcycle is accelerating. The person is a rigid body. The person is sitting on the seat and cannot slide fore or aft, but is free to rock in the plane of the motorcycle(as if there is a hinge connecting the motorcycle to the rider at the seat). The person’s feet are off the pegs and the legs are sticking down and not touching anything. The person’s arms are like cables (they are massless and only carry tension). Assume all dimensions and masses are known (youhavetodeﬁnethemcarefullywithasketch and words). Assume the forward acceleration of the motorcycle is known. You may use numbers and/or variables to describe the quantities of interest.

- a) Draw a clear sketch of the problem showingneededdimensioninformation and the coordinate system you will use.
- b) Draw a Free Body Diagram of the rider.
- c) Write the equations of linear and angular momentum balance for the rider.
- d) Findallforcesontheriderfromthemotorcycle (i.e., at the hands and the seat).
- e) What are the forces on the motorcycle from the rider?


- 6.63 Acceleration of a bicycle on level ground. 2-D . A very compact bicycler (modeled as a point mass M at the bicycle seat C with height h, and distance b behind the front wheel contact), rides a very light old-fashioned bicycle (all components have negligible mass) that is well maintained (all bearings have no frictional torque) and streamlined (neglect air


resistance). The rider applies a force Fp to the pedal perpendicular to the pedal crank (with

length Lc). No force is applied to the other pedal. The radius of the front wheel is Rf .

- a) Assuming no slip, what is the forward acceleration of the bicycle? [ Hint: draw a FBD of the front wheel and crank, and another FBD of the whole bicycle-rider system.] ∗
- b) (Harder) Assuming the rider can push arbitrarily hard but that µ = 1, what is the maximum possible forward acceleration of the bicycle. ∗


M

g

C

h = 2Rf

LC

Rf

A

B

a b

problem 6.63:

(Filename:f.3)

- 6.64 A320lbmmassisattachedatthecornerC of a light rigid piece of pipe bent as shown. The pipe is supported by ball-and-socket joints at A and D and by cable EF. The points A, D, and E are fastened to the ﬂoor and vertical sidewall ofapick-uptruckwhichisacceleratinginthezdirection. The acceleration of the truck is a = 5ft/s2kˆ. There is gravity. Find the tension in cable EF. ∗

x

y

ball & socket

ball & socket

- A

D

E

- B C 15'


12'

6'

12'

z

F 6'

problem 6.64:

(Filename:mikef91p1)

- 6.65 A 5ft by 8ft rectangular plate of uniform density has mass m = 10lbm and is supported by a ball-and-socket joint at point A and the lightrodsCE,BD, and GH. Theentiresystem is attached to a truck which is moving with


acceleration aT. The plate is moving without rotation or angular acceleration relative to the truck. Thus, the center of mass acceleration of the plate is the same as the truck’s. Dimensions are as shown. Points A, C, and D are ﬁxed to the truck but the truck is not touching the plate atanyotherpoints. Findthetensioninrod BD.

- a) If the truck’s acceleration is acm = (5ft/s2)k, what is the tension or compression in rod BD? ∗
- b) If the truck’s acceleration is acm = (5ft/s2)ˆ+(6ft/s2)kˆ, what is the tension or compression in rod GH? ∗


y

D

2'

C

- 3'

8'

- 4'

4'

- 5'




A

E

H

6'

B

x

z

2'

G

problem 6.65:

(Filename:Mikesp92p1)

- 6.66 Hanging a shelf. A shelf with negligible mass supports a 0.5kg mass at its center. The shelf is supported at one corner with a ball and socket joint and the other three corners with strings. At the moment of interest the shelf is in a rocket in outer space and accelerating at 10m/s2 in the k direction. The shelf is in the xy plane.


- a) Draw a FBD of the shelf.
- b) Challenge: without doing any calculations on paper can you ﬁnd one of the reaction force components or the tension in any of the cables? Give yourself a few minutes of staring to try this approach. If you can’t, then come back to this question after you have done all the calculations. ∗
- c) Write down the linear momentum balance equation (a vector equation). ∗
- d) Writedowntheangularmomentumbalance equation using the center of mass as a reference point. ∗
- e) By taking components, turn (b) and (c) into six scalar equations in six unknowns. ∗
- f) Solve these equations by hand or on the computer. ∗
- g) Instead of using a system of equations try to ﬁnd a single equation which can

be solved for TEH. Solve it and compare to your result from before. ∗

- h) Challenge: For how many of the reactions can you ﬁnd one equation which will tell you that particular reaction without knowing any of the other reactions? [Hint, try angular momentum balance about various axes as well as linear momentum balance in an appropriate direction. It is possible to ﬁnd ﬁve of the six unknown reaction components this way.] Must these solutions agree with (d)? Do they?


G

A B

C

32m

H

1m

E

.48m

kˆ

1m

1m

D

ıˆ ˆ

problem 6.66:

(Filename:pﬁgure.s94h2p10)

- 6.67 See also problem 6.38. A uniform rectangular plate of mass m is supported by an inextensible cable CD and a hinge joint at point E on the cart as shown. The hinge joint is attached to a rigid column welded to the ﬂoor of

the cart. The cart has acceleration axıˆ. There is gravity. Find the tension in cable CD.

3 3

2 G

| | |
|---|---|
| | |


A

B C

D

E

a = axıˆ

ıˆ

ˆ 2

problem 6.67:

(Filename:ch3.11)

- 6.68 The uniform 2kg plate DBFH is held by six massless rods (AF, CB, CF, GH, ED, and EH) which are hinged at their ends. The supportpointsA,C,G,andEareallacceleratingin thex-direction with accelerationa = 3m/s2i. There is no gravity.

a) What is { F}·ıˆ for the forces acting

on the plate? b) What is the tension in bar CB?

y

z

1m

1m

A 1m B

D C

E F

G

H

x

problem 6.68:

(Filename:pﬁgure.s94q3p1)

- 6.69 A massless triangular plate rests against a frictionless wall of a pick-up truck at point D and is rigidly attached to a massless rod supported by two ideal bearings ﬁxed to the ﬂoor of the pick-up truck. A ball of mass m is ﬁxed to the centroid of the plate. There is gravity.


The pick-up truck skids across a road with acceleration a = axıˆ+azkˆ. Whatisthereaction at point D on the plate?

d=c+(1/2)b d

y

D

e h

G

z

B

x

a

c

b

A

problem 6.69:

(Filename:ch3.1a)

- 6.70 Towing a bicycle. A bicycle on the level xy plane is steered straight ahead and is being towed by a rope. The bicycle and rider are modeled as a uniform plate with mass m (for the convenience of the artist). The tow force F applied at C has no z component and makes an angle α with the x axis. The rolling wheel contacts are at A and B. The bike is tipped an angle φ from the vertical. The towing force F is just the magnitude needed to keep the bike accelerating in a straight line without tipping any more or less than the angle φ. What is the acceleration of the bicycle? Answer in terms of some or all of b,h,α,φ,m,g and ˆ (Note: F should not appear in your ﬁnal answer.)

F

A

C

B

x

z

y

φ

φ π/2-α

α

h b

problem 6.70:

(Filename:s97f3)

- 6.71 An airplane in ﬂight. An airplane is in straight level ﬂight but is accelerating in the forward direction. In terms of some or all of the following parameters,


- • mtot ≡ the total mass of the plane (including the wings),
- • D= the drag force on the fuselage,
- • FD= the drag force on each wing,
- • g= gravitational constant, and,
- • T = the thrust of one engine.


- a) What is the lift on each wing FL? ∗
- b) What is the acceleration of the plane aP? ∗


c) A free body diagram of one wing is shown. The mass of one wing is mw. What, in terms of mtot, mw, FL, FD, g, a,b, c, and are the reactions at the base of the wing (where it is attached

to the plane), F = Fxıˆ + Fyˆ + Fzkˆ and M = Mxıˆ + Myˆ + Mzkˆ? ∗

j

i

FBD of airplane

k

T

FD

FL

T

mtotg

FD

D

FL

FBD of wing

Fy ,My

Fx ,Mx

Fz ,Mz

c mwg

a b

T

FD

FL

problem 6.71: An airplane in ﬂight, a free body diagram of the plane, and a free body diagram of one wing

(Filename:pﬁgure3.airplane)

- 6.72 A rear-wheel drive car on level ground. The two left wheels are on perfectly slippery ice. The right wheels are on dry pavement. The negligible-mass front right wheel at B is steered straight ahead and rolls without slip. The right rear wheel at C also rolls without slip and drives the car forward with velocity v = vˆ and acceleration a = aˆ. Dimensions are as shown and the car has mass m . What is the sideways force from the ground on the right front wheel at B? Answer in terms of any or all of m, g, a, b, , w, and ıˆ. ∗


ice

m

B

h

b

C

w w/2

kˆ

ˆ

ıˆ

cartoon to show dimensions

B

h

b

C

w w/2

problem 6.72:

(Filename:pﬁgure3.f95p1p3)

- 6.73 A somewhat crippled car slams on the brakes. The suspension springs at A, B, and C are frozen and keep the car level and at constant height. The normal force at D is kept equal

to ND by the only working suspension spring which is on the left rear wheel at D. The only brake which is working is that of the right rear wheel at C which slides on the ground with friction coefﬁcient µ. Wheels A, B, and D roll freely without slip. Dimensions are as shown.

- a) Find the acceleration of the car in terms of some or all of m,w, ,b,h,g,µ,ˆ, and ND.
- b) From the information given could you also ﬁnd all of the reaction forces at all of the wheels? If so, why? If not, what can’t you ﬁnd and why? (No credit for correctanswer. Creditdependsonclear explanation.)


C

B

A

G D

Suspension at left rear wheel keeps normal

force equal to ND

Right rear wheel locks with friction µ

Front wheels roll without slip

b w w/2

h A D

C

B

ıˆ

ˆ

kˆ

g

problem 6.73:

(Filename:s97p2.3)

- 6.74 Speeding tricycle gets a branch caught in the right rear wheel. A scared-stiff tricyclist riding on level ground gets a branch stuck in the right rear wheel so the wheel skids with friction coefﬁcient µ. Assume that the center ofmassofthetricycle-personsystemisdirectly


above the rear axle. Assume that the left rear wheelandthefrontwheelhavenegligiblemass, good bearings, and have sufﬁcient friction that they roll in the ˆ direction without slip, thus constraining the overall motion of the tricycle. Dimensions are shown in the lower sketch. Findtheaccelerationofthetricycle (intermsof some or all of  , h, b, m, [Icm],µ, g, ıˆ, ˆ,

and kˆ). [Hint: check your answer against special cases for which you might guess the answer, such as when µ = 0 or when h = 0.]

kˆ

ˆ

ıˆ

rolling contact

rolling contact

A B

D

branch caught in spokes, skidding

C

g

G

kˆ

ˆ

h

A B

D

ıˆ

b

C

problem 6.74:

(Filename:p.f96.f.1)

##### 7.1 Kinematics of a particlein circular motionskills

- 7.1 If a particle moves along a circle at constant rate (constant θ˙) following the equation


r(t) = R cos(θ˙t)ıˆ + R sin(θ˙t)ˆ

which of these things are true and why? If not true, explain why.

- (a) v = 0
- (b) v = constant
- (c) | v| = constant
- (d) a = 0
- (e) a = constant
- (f) | a| = constant
- (g) v ⊥ a


- 7.2 The motion of a particle is described by the following equations:

- x(t) = 1m · cos((5rad/s) · t),
- y(t) = 1m · sin((5rad/s) · t).


- a) Show that the speed of the particle is constant.
- b) There are two points marked on the path of the particle: P with coordinates (0,1m) and Q with coordinates (1m,0). How much time does the particle take to go from P to Q?
- c) What is the acceleration of the particle at point Q?


- 7.3 Find a planar motion of a particle where the velocity and acceleration are always orthogonal. ∗
- 7.4 A bead goes around a circular track of radius 1ft at a constant speed. It makes around the track in exactly 1s.

- a) Find the speed of the bead.
- b) Find the magnitude of acceleration of the bead.


- 7.5 A 200mm diameter gear rotates at a constant speed of 100rpm.


- a) What is the speed of a peripheral point on the gear?
- b) If no point on the gear is to exceed the centripetal acceleration of 25m/s2, ﬁnd the maximum allowable angular speed (in rpm) of the gear.


- 7.6 A particle executes circular motion in the xy-plane at a constant angular speed θ˙ = 2rad/s. Theradiusofthecircularpathis0.5m. Theparticle’smotionistrackedfromtheinstant when θ = 0, i.e., at t = 0, θ = 0. Find the velocity and acceleration of the particle at

- a) t = 0.5s and
- b) t = 15s.


Draw the path and show the position of the particle at each instant.

- 7.7 A particle undergoes constant rate circular motion in the xy-plane. At some instant t0, its velocityisv(t0) = −3m/sıˆ+4m/sˆ andafter

5s the velocity is v(t0 + 5s) = 5/

√2m/s(ıˆ + ˆ). If the particle has not yet completed one revolution between the two instants, ﬁnd

- a) the angular speed of the particle,
- b) the distance traveled by the particle in 5s, and
- c) the acceleration of the particle at the two instants.


- 7.8 See also problem 7.9. A bead on a circular path of radius R in the xy-plane has rate of change of angular speed α = bt2. The bead starts from rest at θ = 0.

- a) What is the bead’s angular position θ (measuredfromthepositive x-axis)and angular speed ω as a function of time ?
- b) What is the angular speed as function of angular position?


- 7.9 Reconsider the bead from problem 7.8. This time, it has rate of change of angular speed proportional to angular position rather than time, α = cθ3/2. The bead starts from rest at θ = 0. What is the angular position and speed of the bead as a function of time? [Hint: this problem has 2 answers! (one of which you can ﬁnd with a quick guess.)]
- 7.10 Repeat problem 7.51 but assume that the moment of interest is at position B with θ = 60◦.
- 7.11 Solve ω˙ = α, given ω(0) = ω0 and α is a constant.
- 7.12 Solve θ¨ = α, given θ(0) = θ0, θ(˙ 0) = ω˙0, and α a constant.
- 7.13 Given ω˙ = ddtθ˙ = α (a constant), ﬁnd an expression for ω as a function of θ if ω(θ =

0) = w0.

- 7.14 Given that θ¨ −λ2θ = 0, θ(0) = π/2, and θ(˙ 0) = 0, ﬁnd the value of θ at t = 1s.
- 7.15 Two runners run on a circular track sideby-side at the same constant angular rate ω about the center of the track. The inside runner is in a lane of radius ri and the outside runner


- is in a lane of radius ro. What is the velocity of the outside runner relative to the inside runner in polar coordinates?
- 7.16 A particle oscillates on the arc of a circle with radius R according to the equation θ =

θ0 cos(λt). What are the conditions on R,θ0, and λ so that the maximum acceleration in this motion occurs at θ = 0. “Acceleration” here meansthemagnitudeoftheaccelerationvector.

7.2Dynamicsofaparticlein circular motion

skills

- 7.17 Force on a person standing on the equator. The total force acting on an object of mass m, moving with a constant angular speed ω on a circular path with radius r, is given by F = mω2r. Find the magnitude of the total force acting on a 150lbm person standing on the equator. Neglect the motion of the earth around the sun and of the sun around the solar system, etc. The radius of the earth is 3963mi. Give your solution in both pounds (lbf) and Newtons (N). ∗
- 7.18 The sum of forces acting on a mass m = 10lbm is F = 100lbfıˆ − 120lbfˆ. The particle is going in circles at constant rate with r = 18in and eˆr = cos30oıˆ + sin30oˆ. Using F = m a, ﬁnd v.
- 7.19 The acceleration of a particle in planar


circularmotionisgivenby a = αreˆθ−ω2reˆr, where α is the angular acceleration, ω is the angular speed and r is the radius of the circular path. Using F = m a, ﬁnd the expressions for Fx and Fy in terms of α, ω, r, and θ, given that eˆr = cosθıˆ + sinθˆ and eˆθ = −sinθıˆ + cosθˆ.

7.20Consideraparticlewithmassm incircular motion. Let θ¨ = α, θ˙ = ω, and r = −rıˆ. Let F = Freˆr + Fθeˆθ, where eˆr = −ıˆ and eˆθ = kˆ. Using F = m a, express

Fr and Fθ in terms of α, ω, r, and m.

7.21 A bead of mass m on a circular path of radius R in the xy-plane has rate of change of angular speed α = ct3. The bead starts from rest at θ = 0.

- a) What is the angular momentum of the bead about the origin at t = t1?
- b) What is the kinetic energy of the bead at t = t1.


y

- (I)

A

B

O

θ¨ = 0

x

y

45o

R

- (II)


- 7.26 A particle of mass 3kg moves in the xyplane so that its position is given by

r(t) = 4m[cos(

2πt s

)ıˆ + sin(

2πt s

)ˆ].

- a) What is the path of the particle? Show how you know what the path is.
- b) What is the angular velocity of the particle? Is it constant? Show how you know if it is constant or not.
- c) What is the velocity of the particle in polar coordinates?
- d) What is the speed of the particle at t = 3s?
- e) What net force does it exert on its surroundings at t = 0s? Assume the x and y axis are attached to a Newtonian frame.
- f) What is the angular momentum of the particleatt = 3saboutpoint O located at the origin of the coordinate system that the particle is referenced to?


- 7.27 Going in circles — a comparison of constant and nonconstant rate motion. A 100 gmmassisgoingincirclesofradius R = 20cm at a constant rate θ˙ = 3rad/s. Another identical mass is going in circles of the same radius but at a non-constant rate. The second mass is accelerating at θ¨ = 2rad/s2 and at position A, it happens to have the same angular speed as the ﬁrst mass.


- 7.22 A 200 gm particle goes in circles about a ﬁxed center at a constant speed v = 1.5m/s. It takes 7.5s to go around the circle once.

- a) Find the angular speed of the particle.
- b) Find the magnitude of acceleration of the particle.
- c) Take center of the circle to be the origin of a xy-coordinate system. Find the net force on the particle when it is at θ = 30o from the x-axis.


- 7.23 A race car cruises on a circular track at a constant speed of 120mph. It goes around the track once in three minutes. Find the magnitude of the centripetal force on the car. What applies this force on the car? Does the driver have any control over this force?
- 7.24 A particle moves on a counter-clockwise, origin-centered circular path in the xy-plane at a constant rate. The radius of the circle is r, the mass of the particle is m, and the particle completes one revolution in time τ.

- a) Neatly draw the following things:

- 1. The path of the particle.
- 2. A dot on the path when the particle is at θ = 0◦, 90◦, and 210◦, where θ is measured from the x-axis (positive counter-clockwise).
- 3. Arrows representing eˆR, eˆθ, v, and a at each of these points.


- b) Calculate all of the quantities in part (3) above at the points deﬁned in part (2), (represent vector quantities in terms of the cartesian base vectors ıˆ and ˆ). ∗
- c) If this motion was imposed by the tension in a string, what would that tension be? ∗
- d) Isradialtensionenoughtomaintainthis motion or is another force needed to keep the motion going (assuming no friction) ? ∗
- e) Again, if this motion was imposed by


the tension in a string, what is Fx, the x component of the force in the string, when θ = 210◦? Ignore gravity.

- 7.25 The velocity and acceleration of a 1kg particle, undergoing constant rate circular motion, are known at some instant t: v = −10m/s(ıˆ + ˆ), a = 2m/s2(ıˆ − ˆ).


R

45o

x

B

A

O

θ¨ = 2rad/s2

problem 7.27:

(Filename:pﬁgure.s94h8p2)

- 7.28 Asmallmassm isconnectedtooneendof a spring. The other end of the spring is ﬁxed to the center of a circular track. The radius of the track is R, the unstretched length of the spring is l0(< R), and the spring constant is k.

- a) With what speed should the mass be launched in the track so that it keeps going at a constant speed?
- b) If the spring is replaced by another spring of same relaxed length but twice the stiffness, what will be the new required launch speed of the particle?


- 7.29 A bead of mass m is attached to a spring with constant k. The bead slides without friction in the tube shown. The tube is driven at a


constant angular rate ω0 about axis AA by a motor (not pictured). There is no gravity. The

unstretched spring length is r0. Find the radial position r of the bead if it is stationary with respect to the rotating tube. ∗

- a) Find and draw the accelerations of the two masses (call them I and II) at position A.
- b) Find H˙ O for both masses at position A. ∗
- c) Find HO forbothmassesatpositionsA

and B. Do the changes in HO between the two positions reﬂect (qualitatively)

the results obtained in (b)? ∗

- d) If the masses are pinned to the center O by massless rigid rods, is tension in the rods enough to keep the two motions going? Explain.


A'

m

ω0

![image 15](Introduction to Statics and Dynamics Problems_images/imageFile15.png)

![image 16](Introduction to Statics and Dynamics Problems_images/imageFile16.png)

- a) Write the position of the particle at time t using eˆR and eˆθ base vectors.
- b) Find the net force on the particle at time t.
- c) At some later time t∗, the net force on the particle is in the−ˆ direction. Find the elapsed time t − t∗.
- d) After how much time does the force on the particle reverse its direction.


![image 17](Introduction to Statics and Dynamics Problems_images/imageFile17.png)

![image 18](Introduction to Statics and Dynamics Problems_images/imageFile18.png)

![image 19](Introduction to Statics and Dynamics Problems_images/imageFile19.png)

![image 20](Introduction to Statics and Dynamics Problems_images/imageFile20.png)

![image 21](Introduction to Statics and Dynamics Problems_images/imageFile21.png)

r 0

A

problem 7.29:

(Filename:Danef94s2q6)

- 7.30 A particle of mass m is restrained by a string to move with a constant angular speed ω around a circle of radius R on a horizontal frictionless table. If the radius of the circle is reduced to r, by pulling the string with a force F through a hole in the table, what will the particle’s angular velocity be? Is kinetic energy is conserved? Why or why not?

F

r m

problem 7.30:

(Filename:pﬁgure.blue.44.1)

- 7.31 An ‘L’ shaped rigid, massless, and frictionless bar is made up of two uniform segments of length = 0.4m each. A collar of mass m = 0.5kg, attached to a spring at one end, slides frictionlessly on one of the arms of the ‘L’. The spring is ﬁxed to the elbow of the ‘L’ and has a spring constant k = 6N/m. The structure rotates clockwise at a constant rate ω = 2rad/s. If the collar is steady at a distance 34 = 0.3m away from the elbow of the ‘L’, ﬁnd the relaxed length of the spring, 0. ∗

.

|3/4|ω|
|---|---|
| | |
|motor<br><br>m k<br><br>ıˆ<br><br>ˆ| |


x

y

O

problem 7.31: Forces in constant rate circular motion.

(Filename:pﬁgure.Lbar)

- 7.32 A massless rigid rod with length attached to a ball of mass M spins at a constant angular rate ω which is maintained by a motor (not shown) at the hinge point. The rod can


only withstand a tension of Tcr before breaking. Find the maximum angular speed of the ball so that the rod does not break assuming

a) there is no gravity, and b) there is gravity (neglect bending

stresses).

M

y

ω

x

problem 7.32:

(Filename:Danef94s2q5)

- 7.33 A 1m long massless string has a particle of 10grams mass at one end and is tied to a stationary point O at the other end. The particle rotates counter-clockwise in circles on a frictionless horizontal plane. The rotation rate is 2π rev/sec. Assume an xy-coordinate system in the plane with its origin at O.

- a) Make a clear sketch of the system.
- b) What is the tension in the string (in Newtons)? ∗
- c) What is the angular momentum of the mass about O? ∗
- d) When the string makes a 45◦ angle with the positive x and y axis on the plane, the string is quickly and cleanly cut. What is the position of the mass 1 sec later? Make a sketch. ∗


- 7.34 A ball of mass M ﬁxed to an inextensible rod of length and negligible mass rotates about a frictionless hinge as shown in the ﬁgure. A motor (not shown) at the hinge point accelerates the mass-rod system from rest by

applying a constant torque MO. The rod is initially lined up with the positive x-axis. The

rod can only withstand a tension of Tcr before breaking. At what time will the rod break and after how many revolutions? Include gravity if you like.

M

ω

x

y

problem 7.34:

(Filename:pﬁgure5.mike.sum95)

- 7.35 A particle of mass m, tied to one end of a rod whose other end is ﬁxed at point O to a motor, moves in a circular path in the vertical plane at a constant rate. Gravity acts in the −ˆ direction.


a) Find the difference between the maximum and minimum tension in the rod.

∗

- b) Find the ratio Tmax T where T = Tmax − Tmin. A criterion for ignoring gravity might be if the variation in tension is less than 2% of the maximum tension; i.e., when Tmax T < 0.02. For a given length r of the rod, ﬁnd the rotation rate ω for which this condition is met. ∗ .

- c) For ω = 300rpm, what would be the length of the rod for the condition in part (b) to be satisﬁed? ∗ .


###### ˆ

m

ıˆ

r

O

g

problem 7.35:

(Filename:pﬁgure4.rph)

- 7.36 A massless rigid bar of length L is hinged at the bottom. A force F is applied at point A at the end of the bar. A mass m is glued to the bar at point B, a distance d from the hinge. There is no gravity. What is the acceleration of point A at the instant shown? Assume the angular velocity is initially zero.

A F

B d

x

y

problem 7.36:

(Filename:pﬁgure.blue.10.1)

- 7.37 The mass m is attached rigidly to the rotating disk by the light rod AB of length .


Neglect gravity. Find MA (the moment on the rod AB from its support point at A) in terms of

θ˙ and θ¨. What is the sign of MA if θ˙ = 0 and θ¨ > 0? What is the sign if θ¨ = 0 and θ˙ > 0?

A

B θ(t)

R

m

O

problem 7.37:

(Filename:pﬁgure.blue.84.2)

7.38Pendulausingenergymethods. Findthe equations of motion for the pendula in problem 7.94 using energy methods. ∗ .

- 7.39 Tension in a simple pendulum string. A simple pendulum of length 2m with mass 3kg is released from rest at an initial angle of 60◦ from the vertically down position.

- a) What is the tension in the string just after the pendulum is released?
- b) What is the tension in the string when the pendulum has reached 30◦ from the vertical?


- 7.40 Simply the simple pendulum. Find the nonlinear governing differential equation for a simple pendulum

θ¨ = −

g l

sinθ

- as many different ways as you can.


θ

problem 7.40: A simple pendulum.

(Filename:spend)

- 7.41 Tension in a rope-swing rope. Model a swinging person as a point mass. The swing starts from rest at an angle θ = 90◦. When the rope passes through vertical the tension in the rope is higher (it is hard to hang on). A person wants to know ahead of time if she is strong enough to hold on. How hard does she have to hang on compared, say, to her own weight? You are to ﬁnd the solution two ways. Use the same m, g, and L for both solutions.


- a) Find θ¨ as a function of g, L,θ, and m. This equation is the governing differential equation. Write it as a system of ﬁrst order equations. Solve them numerically. Once you know θ˙ at the time the rope is vertical you can use other mechanics relations to ﬁnd the tension. If you like, you can plot the tension as a function of time as the mass falls.
- b) Use conservation of energy to ﬁnd θ˙ at θ = 0. Then use other mechanics relations to ﬁnd the tension. ∗


A

θ L

B

m

problem 7.41:

(Filename:pﬁgure.s94h8p5)

- 7.42 Pendulum. A pendulum with a negligible-mass rod and point mass m is realeased from rest at the horizontal position θ = π/2.

- a) Find the acceleration (a vector) of the mass just after it is released at θ = π/2 in terms of  ,m, g and any base vectors you deﬁne clearly.
- b) Find the acceleration (a vector) of the mass when the pendulum passes through the vertical at θ = 0 in terms of  ,m, g and any base vectors you deﬁne clearly
- c) Find the string tension when the pendulumpassesthroughtheverticalatθ = 0 (in terms of  ,m and g).


x

y

θ

m

g

problem 7.42:

(Filename:s97p2.1)

- 7.43 Simple pendulum, extended version. A point mass M = 1kg hangs on a string of length L = 1m. Gravity pulls down on the mass with force Mg, where g = 10m/s2. The pendulum lies in a vertical plane. At any time t, the angle between the pendulum and the straight-down position is θ(t). There is no air friction.


- a) Equation of motion. Assuming that you know both θ and θ˙, ﬁnd θ¨. There are several ways to do this problem. Use any ways that please you. ∗
- b) Tension. Assuming that you know θ and θ˙, ﬁnd the tension T in the string.
- c) Reaction components. Assuming you know θ and θ˙, ﬁnd the x and y components of the force that the hinge support causes on the pendulum . Deﬁne your coordinate directions sensibly.


- d) Reduction to ﬁrst order equations. The equation that you found in (a) is a nonlinear second order ordinary differential equation. It can be changed to a pair of ﬁrst order equations by deﬁning a new variable α ≡ θ˙. Write the equation from (a) as a pair of ﬁrst order equations. Solving these equations is equivalent to solving the original second order equation. ∗
- e) Numerical solution. Given the initial conditions θ(t = 0) = π/2 and α(t = 0) = θ(˙ t = 0) = 0, one should be able to ﬁnd what the position and speed of the pendulum is as a function of time. Using the results from (b) and (c) one can also ﬁnd the reaction components. Using any computer and any method you like, ﬁnd: θ(t), θ(˙ t) & T(t). Make a single plot, orthreeverticallyalignedplots,ofthese variables for one full oscillation of the pendulum.
- f) Maximum tension. Using your numerical solutions, ﬁnd the maximum value of the tension in the rod as the mass swings. ∗
- g) Period of oscillation. How long does it take to make one oscillation?
- h) Other observations. Make any observations that you think are interesting about this problem. Some questions: Does the solution to (f) depend on the length of the string? Is the solution to (f) exactly 30 or just a number near 30? How does the period found in (g) compare to the period found by solving the linear equation θ¨ + (g/l)θ = 0, based on the (inappropriate-to-use in this case) small angle approximation sinθ = θ?


7.44 Bead on a hoop with friction. A bead slides on a rigid, stationary, circular wire. The coefﬁcient of friction between the bead and the wire is µ. The bead is loose on the wire (not a tight ﬁt but not so loose that you have to worry about rattling). Assume gravity is negligible.

a) Given v, m, R, & µ; what is v˙? ∗ b) If v(θ = 0) = v0, how does v depend

on θ, µ, v0 and m? ∗

y

v

m θ

O R

x

problem 7.44:

(Filename:pﬁgure.s94h10p1)

- 7.45 Particle in a chute. One of a million non-interacting rice grains is sliding in a circular chute with radius R. Its mass is m and it slides with coefﬁcient of friction µ (Actually it slides, rolls and tumbles — µ is just the effective coefﬁcient of friction from all of these interactions.) Gravity g acts downwards.

- a) Find a differential equation that is satisﬁed by θ that governs the speed of the rice as it slides down the hoop. Parameters in this equation can be m, g, R and µ [Hint: Draw FBD, write eqs of mechanics, express as ODE.]
- b) Find the particle speed at the bottom of the chute if R = .5m, m = .1grams, g = 10m/s2, and µ = .2 as well as the initial values of θ0 = 0 and its initial downward speed is v0 = 10m/s. [Hint: you are probably best off seeking a numerical solution.]


R

θ

µ

m g

problem 7.45:

(Filename:p.f96.p3.1)

- 7.46 Due to a push which happened in the past,


the collar with mass m is sliding up at speed v0 on the circular ring when it passes through the point A. The ring is frictionless. A spring of constant k and unstretched length R is also pulling on the collar.

- a) What is the acceleration of the collar at

A. Solve in terms of R, v0, m, k, g and any base vectors you deﬁne.

- b) What is the force on the collar from the ring when it passes point A? Solve in


terms of R, v0, m, k, g and any base vectors you deﬁne.

g

R

A collar

problem 7.46:

(Filename:s93q4Ruina)

- 7.47 Atoyusedtoshootpelletsismadeoutofa thin tube which has a spring of spring constant k on one end. The spring is placed in a straight section of length ; it is unstretched when its length is . The straight part is attached to a (quarter)circulartubeofradius R,whichpoints up in the air.

- a) A pellet of mass m is placed in the device and the spring is pulled to the left by an amount . Ignoring friction along the travel path, what is the pellet’s velocity v as it leaves the tube? ∗
- b) What force acts on the pellet just prior to its departure from the tube? What about just after? ∗


k R

problem 7.47:

(Filename:pﬁgure.blue.toygun)

- 7.48 Ablockwithmassm ismovingtotheright

at speed v0 when it reaches a circular frictionless portion of the ramp.

- a) What is the speed of the block when it reaches point B? Solve in terms of R, v0, m and g.
- b) What is the force on the block from the ramp just after it gets onto the ramp at


point A? Solve in terms of R, v0, m and g. Remember, force is a vector.

R

A

B

g

v0

problem 7.48:

(Filename:s93q4Sachse)

- 7.49 A car moves with speed v along the surface of the hill shown which can be approximated as a circle of radius R. The car starts at a point on the hill at point O. Compute the magnitude of the speed v such that the car just leaves the ground at the top of the hill.


g

O

R

problem 7.49:

(Filename:pﬁgure.blue.65.1)

##### 7.3 Kinematics of a rigid body in planar circular motion

###### skills

- 7.50 Find v = ω × r, if ω = 1.5rad/skˆ and r = 2mıˆ − 3mˆ.
- 7.51 A particle goes around a circle shown in the ﬁgure, at the moment of interest, with angular velocity ω = 5rad/skˆ and angular

acceleration α = 2rad/s2kˆ. Find, draw, and label the tangential and normal acceleration

a) of the particle at the location A. ∗ b) of the particle at the location B.

r = 10 in

A

B

x

y

θ

problem 7.51:

(Filename:eﬁg1.2.18)

- 7.52 A motor turns a uniform disc of radius R counter-clockwise about its mass center at a constant rate ω. The disc lies in the xyplane and its angular displacement θ is measured (positive counter-clockwise) from the xaxis. What is the angular displacement θ(t) of

the disc if it starts at θ(0) = θ0 and θ(˙ 0) = ω? What are the velocity and acceleration of a point P at position r = xıˆ + yˆ?

- 7.53 A disc is rotating at 15 rpm. How many seconds does it take to rotate by 180 degrees? Whatistheangularspeedofthediscin rad/s?
- 7.54 Two discs A and B rotate at constant speeds about their centers. Disc A rotates at 100rpm and discB rotates at 10rad/s. Which is rotating faster?


- 7.55 Find the angular velocities of the second, minute, and hour hands of a clock.
- 7.56 A motor turns a uniform disc of radius R counter-clockwise about its mass center at a constant rate ω. The disc lies in the xyplane and its angular displacement θ is measured (positive counter-clockwise) from the xaxis. What are the velocity and acceleration of

a point P at position r P = cıˆ + dˆ relative to the velocity and acceleration of a point Q

at position r Q = 0.5(−dıˆ + cˆ) on the disk? (c2 + d2 < R2.)

- 7.57 A 0.4m long rod AB has many holes along its length such that it can be pegged at any of the various locations. It rotates counterclockwise at a constant angular speed about a peg whose location is not known. At some instant t, the velocity of end B is vB = −3m/sˆ. After 20π s, the velocity of end B is vB = −3m/sıˆ. If the rod has not completed one revolution during this period,

a) ﬁnd the angular velocity of the rod, and b) ﬁnd the location of the peg along the

length of the rod.

B

A

ıˆ

ˆ

problem 7.57:

(Filename:pﬁgure4.3.rp9)

- 7.58 A circular disc of radius r = 250mm rotates in the xy-plane about a point which is atadistanced = 2r awayfromthecenterofthe disk. At the instant of interest, the linear speed of the center C is 0.60m/s and the magnitude of its centripetal acceleration is 0.72m/s2.


- a) Find the rotational speed of the disk.
- b) Is the given information enough to locate the center of rotation of the disk?
- c) If the acceleration of the center has no component in theˆ direction at the moment of interest, can you locate the center of rotation? If yes, is the point you locate unique? If not, what other information is required to make the point unique?


| | |
|---|---|
| | |


C r

###### ˆ

ıˆ

###### problem 7.58:

(Filename:pﬁgure4.3.rp8)

- 7.59 A disc C spins at a constant rate of two revolutions per second counter-clockwise about its geometric center, G, which is ﬁxed. A point P is marked on the disk at a radius of one meter. At the moment of interest, point P is on the x-axis of an xy-coordinate system centered at point G.

- a) Draw a neat diagram showing the disk, the particle, and the coordinate axes.
- b) What is the angular velocity of the disk, ωC?
- c) What is the angular acceleration of the disk, ω˙ C?
- d) What is the velocity vP of point P?
- e) What is the acceleration aP of point P?


- 7.60 A uniform disc of radius r = 200mm is mounted eccentrically on a motor shaft at point O. The motor rotates the disc at a constant angular speed. At the instant shown, the velocity of the center of mass is vG = −1.5m/sˆ.

- a) Find the angular velocity of the disc.
- b) Find the point with the highest linear speed on the disc. What is its velocity?


|2 r<br>3<br><br><br>| |
|---|---|
| | |


O

G r

x

y

problem 7.60:

(Filename:pﬁgure4.3.rp4)

- 7.61 The circular disc of radius R = 100mm rotates about its center O. At a given instant,


point A onthediskhasavelocityvA = 0.8m/s in the direction shown. At the same instant, the tangent of the angle θ made by the total acceleration vector of any point B with its radial line to O is 0.6. Compute the angular acceleration α of the disc.

vA

B

A

R

θ

aB

O

###### problem 7.61:

(Filename:pﬁgure.blue.43.2)

- 7.62 Show that, for non-constant rate circular motion, the acceleration of all points in a given radial line are parallel.

O

a

problem 7.62:

(Filename:pﬁgure.DH.5.1a)

- 7.63 A motor turns a uniform disc of radius R about its mass center at a variable angular rate ω with rate of change ω˙, counterclockwise. The disc lies in the xy-plane and its angular displacement θ is measured from the x-axis, positive counter-clockwise. What are the velocity and acceleration of a point

P at position r P = cıˆ + dˆ relative to the velocity and acceleration of a point Q at po-

sition r Q = 0.5(−dıˆ + yˆ) on the disk? (c2 + d2 < R2.)

- 7.64 Bit-stream kinematics of a CD. A Compact Disk (CD) has bits of data etched on concentric circular tracks. The data from a track is read by a beam of light from a head that is positioned under the track. The angular speed of the disk remains constant as long as the head is positioned over a particular track. As the head moves to the next track, the angular speed of the disk changes, so that the linear speed at any track is always the same. The data stream comes out at a constant rate 4.32 × 106 bits/second. When the head is positioned on the outermost track, for which r = 56mm, the disk rotates at 200rpm.

- a) What is the number of bits of data on the outermost track.
- b) ﬁnd the angular speed of the disk when the head is on the innermost track (r = 22mm), and
- c) ﬁnd the numbers of bits on the innermost track.


- 7.65 A horizontal disk D of diameter d = 500mm is driven at a constant speed of 100rpm. A small disk C can be positioned anywhere between r = 10mm and r = 240mm on diskD by sliding it along the overhead shaft and then ﬁxing it at the desired position with a set screw (see the ﬁgure). Disk


y

C rolls without slip on disk D. The overhead shaft rotates with disk C and, therefore, its rotational speed can be varied by varying the position of disk C. This gear system is called brush gearing. Find the maximum and minimum rotational speeds of the overhead shaft. ∗

massless rods such that the whole structure behaves like a rigid body. The structure rotates counterclockwise at a constant rate of 60rpm. At the instant shown, ﬁnd the force in each rod.

ω

R

O

m = 0.5 kg m

x

Side View

M

|set scre<br><br>C|![image 22](Introduction to Statics and Dynamics Problems_images/imageFile22.png)<br><br>![image 23](Introduction to Statics and Dynamics Problems_images/imageFile23.png)<br><br>![image 24](Introduction to Statics and Dynamics Problems_images/imageFile24.png)<br><br>![image 25](Introduction to Statics and Dynamics Problems_images/imageFile25.png)<br><br>![image 26](Introduction to Statics and Dynamics Problems_images/imageFile26.png)<br><br>![image 27](Introduction to Statics and Dynamics Problems_images/imageFile27.png)<br><br>![image 28](Introduction to Statics and Dynamics Problems_images/imageFile28.png)<br><br>![image 29](Introduction to Statics and Dynamics Problems_images/imageFile29.png)<br><br>w bearing<br><br>![image 30](Introduction to Statics and Dynamics Problems_images/imageFile30.png)<br><br>![image 31](Introduction to Statics and Dynamics Problems_images/imageFile31.png)| |
|---|---|---|
|r<br><br>D<br><br>| | |


C

1m 45o

problem 7.70:

(Filename:pﬁgure.blue.87a.1)

- 7.71 Neglecting gravity, calculate α = ω˙ = θ¨ at the instant shown for the system in the ﬁgure.

F=10N

2 kg pt. mass

4 cm

5 cm

4 cm

1 cm

rigid massless θ tubing

problem 7.71:

(Filename:pﬁgure.blue.20.1)

- 7.72 A disk of mass M and radius R is attached to an electric motor as shown. A coin of mass m rests on the disk, with the center of the coin a distance r from the center of the disk. Assume that m M, and that the coefﬁcient of friction between the coin and the disk is µ. The motor delivers a constant power P to the disk. The disk starts from rest when the motor is turned on at t = 0.

- a) What is the angular velocity of the disk as a function of time?
- b) What is its angular acceleration?
- c) At what time does the coin begin to slip off the disk? (It will sufﬁce here to give the equation for t that must be solved.)


G

R

r

coin, mass = m

disk, mass = M

z

ω

IG = 12 MR2

g

problem 7.72:

(Filename:pﬁgure.blue.45.1)

- 7.73 2-D constant rate gear train. The angular velocity of the input shaft (driven by a motor not shown) is a constant, ωinput = ωA.


problem 7.67:

(Filename:pﬁg4.1.rp10)

Top View

7.68 The hinged disk of mass m (uniformly distributed) is acted upon by a force P shown in the ﬁgure. Determine the initial angular acceleration and the reaction forces at the pin O.

r

C

![image 32](Introduction to Statics and Dynamics Problems_images/imageFile32.png)

![image 33](Introduction to Statics and Dynamics Problems_images/imageFile33.png)

![image 34](Introduction to Statics and Dynamics Problems_images/imageFile34.png)

![image 35](Introduction to Statics and Dynamics Problems_images/imageFile35.png)

![image 36](Introduction to Statics and Dynamics Problems_images/imageFile36.png)

![image 37](Introduction to Statics and Dynamics Problems_images/imageFile37.png)

![image 38](Introduction to Statics and Dynamics Problems_images/imageFile38.png)

![image 39](Introduction to Statics and Dynamics Problems_images/imageFile39.png)

g

D

O

100 rpm

30o

problem 7.65:

R

(Filename:pﬁgure4.rpc)

P

- 7.66 Two points A and B are on the same machine part that is hinged at an as yet unkown location C. Assume you are given that points

at positions rA and rB are supposed to move in given directions, indicated by unit vectors as

λˆ A and λˆ B. For each of the parts below, illustrate your results with two numerical examples

(in consistent units): i) rA = 1ıˆ, rB = 1ˆ, λˆ A = 1ˆ, and λˆ B = −1ıˆ (thus rC = 0), and ii) a more complex example of your choosing.

- a) Describe in detail what equations must be satisﬁed by the point rC.
- b) Write a computer program that takes as input the 4 pairs of numbers [ rA], [ rB], [λˆ A] and [λˆ B] and gives as output the pair of numbers [λˆ C].
- c) Find a formula of the form rC = ... that explicitly gives the position vector for point C in terms of the 4 given vectors.


7.4Dynamicsofarigidbody in planar circular motion

skills

- 7.67 The structure shown in the ﬁgure consists of two point masses connected by three rigid,


30o

problem 7.68:

(Filename:pﬁgure.blue.41.3)

- 7.69Athinuniformcirculardiscofmass M and radius R rotates in the xy plane about its center of mass point O. Driven by a motor, it has rate of change of angular speed proportional to angular position, α = dθ5/2. The disc starts from rest at θ = 0.

- a) What is the rate of change of angu-

lar momentum about the origin at θ = π 3 rad?

- b) What is the torque of the motor at θ = π 3 rad?

- c) What is the total kinetic energy of the disk at θ = π3 rad?


- 7.70 A uniform circular disc rotates at constant angular speed ω about the origin, which is also the center of the disc. It’s radius is R. It’s total mass is M.


- a) What is the total force and moment required to hold it in place (use the origin as the reference point of angular momentum and torque).
- b) What is the total kinetic energy of the disk?


What is the angular velocity ωoutput = ωC of the output shaft and the speed of a point on the

outer edge of disc C, in terms of RA, RB, RC, and ωA?

no slip

###### ωA

###### ωC

RC

RA RB

A B

C

problem 7.73: A set of gears turning at constant rate.

(Filename:ch4.3)

- 7.74 2-D constant speed gear train. Gear A is connected to a motor(not shown) and gear B, which is welded to gear C, is connected to a taffy-pulling mechanism. Assume you know the torque Minput = MA and angular velocity ωinput = ωA of the input shaft. Assume the bearings and contacts are frictionless.

- a) What is the input power?
- b) What is the output power?
- c) What is the output torque Moutput =


MC, the torque that gear C applies to its surroundings in the clockwise direction?

RA

MA

RB

RC

ωA

A B

C

no slip

ωC

problem 7.74:

(Filename:pﬁgure.s94h6p5)

- 7.75 Accelerating rack and pinion. The two gears shown are welded together and spin on a frictionless bearing. The inner gear has radius 0.5m and negligible mass. The outer disk has 1m radius and a uniformly distributed mass of 0.2kg. They are loaded as shown with the force F = 20N on the massless rack which is held in place by massless frictionless rollers. At the time of interest the angular velocity is ω = 2rad/s (though ω is not constant). The point P is on the disk a distance 1m from the center. At the time of interest, point P is on the positive y axis.


- a) What is the speed of point P?
- b) What is the velocity of point P?
- c) What is the angular acceleration α of the gear?
- d) What is the acceleration of point P?
- e) What is the magnitude of the acceleration of point P?
- f) What is the rate of increase of the speed of point P?


uniform disk

m = 2kg F=20N

###### ω

P

1m

.5m

massless inner disk

no slip

y

massless rack

x

problem 7.75: Accelerating rack and pinion

(Filename:pg45.2)

- 7.76 A 2-D constant speed gear train. Shaft B is rigidly connected to gears G4 and G3. G3 meshes with gear G6. Gears G6 and G5 are both rigidly attached to shaft CD. Gear G5 meshes with G2 which is welded to shaft A. Shaft A and shaft B spin independently. The input torque Minput = 500N·m and the spin rate ωinput = 150rev/min.. Assume the bearings and contacts are frictionless.

- a) What is the input power? ∗
- b) What is the output power? ∗
- c) What is the angular velocity ωoutputof the output shaft? ∗
- d) What is the output torque Moutput? ∗


- x
- y z


C

A

D

G1

G2 G3 G4

G6

G5

B

C D

A B

G5

G1

G2 G3

G4

Front view G6

ωout

ωin

RG5 = 3RG2 3RG3 = 5RG6

ωout ωin

problem 7.76:

(Filename:pﬁgure.s94h6p6)

- 7.77 Two gears rotating at constant rate. See also problems 4.16 and ??. At the input to a gear box a 100lbf force is applied to gear A. At theoutput, themachinery(notshown)applies a


forceof FB totheoutputgear. Gear A rotatesat constant angular rate ω = 2rad/s, clockwise.

- a) What is the angular speed of the right gear?
- b) What is the velocity of point P?
- c) What is FB?
- d) If the gear bearings had friction, would


FB have to be larger or smaller in order to achieve the same constant velocity?

e) Ifinsteadofapplyinga100lbftotheleft gear it is driven by a motor (not shown) at constant angular speed ω, what is the angular speed of the right gear?

no slip

RA

RB

RC

A B

- FA = 100 lb

FB = ?

C

problem 7.77: Two gears.

(Filename:pg131.3)

- 7.78 Two racks connected by a gear. A 100lbf force is applied to one rack. At the output the machinery (not shown) applies a force

FB to the other rack.

- a) Assume the gear is spinning at constant rate and is frictionless. What is FB?
- b) If the gear bearing had friction, would


that increase or decrease FB to achieve the same constant rate?

uniform disk m = 10 lbm

massless racks 100 lbf FB = ?

6 in

ω

problem 7.78: Two racks connected by a gear.

(Filename:ch4.4)

- 7.79 Constant rate rack and pinion. The two gears shown are welded together and spin on a frictionless bearing. The inner gear has radius 0.5m and negligible mass. The outer gear has 1m radius and a uniformly distributed mass of 0.2kg. Amotor(notshown)rotatesthedisksat constant rate ω = 2rad/s. The gears drive the massless rack which is held in place by massless frictionless rollers as shown. The gears and the rack have teeth that are not shown in the ﬁgure. The point P is on the outer gear a distance 1.0m from the center. At the time of interest, point P is on the positive y axis.




- a) What is the speed of point P? ∗
- b) What is the velocity of point P? ∗
- c) What is the acceleration of point P? ∗
- d) What is the velocity of the rack vr? ∗
- e) What is the force on the rack due to its contact with the inner gear? ∗


ω

P

vr

1m

.5m

no slip

y

x

problem 7.79: Constant rate rack and pinion

(Filename:ch4.2)

- 7.80 Belt drives are used to transmit power between parallel shafts. Two parallel shafts, 3m apart, are connected by a belt passing over thepulleys A and B ﬁxedtothetwoshafts. The driver pulley A rotates at a constant 200rpm. The speed ratio between the pulleys A and B is 1:2.5. The input torque is 350N·m. Assume no loss of power between the two shafts.

- a) Find the input power. ∗
- b) Find the rotational speed of the driven pulley B ∗ .
- c) Find the output torque at B. ∗


3m

(driven) B

A (driver)

r = 100 mm

problem 7.80:

(Filename:pﬁgure4.rpd)

- 7.81 In the belt drive system shown, assume that the driver pulley rotates at a constant angular speed ω. If the motor applies a constant

torque MO on the driver pulley, show that the tensions in the two parts, AB and CD, of the belt must be different. Which part has a greater tension? Does your conclusion about unequal tension depend on whether the pulley is massless or not? Assume any dimensions you need.

driven pulley

B

driver pulley

A

D C

MO

problem 7.81:

(Filename:pﬁgure4.rpe)

- 7.82 A belt drive is required to transmit 15 kW power from a 750mm diameter pulley rotating at a constant 300rpm to a 500mm diameter pulley. The centers of the pulleys are located 2.5mapart. Thecoefﬁcientoffrictionbetween the belt and pulleys is µ = 0.2.


- a) (See problem 7.102.) Draw a neat diagram of the pulleys and the belt-drive system and ﬁnd the angle of lap, the contact angle θ, of the belt on the driver pulley.
- b) Find the rotational speed of the driven pulley.
- c) (See the ﬁgure in problem 7.102.) The power transmitted by the belt is given by power = net tension × belt speed,

i.e., P = (T1 − T2)v, where v is the linear speed of the belt. Find the maximum tension in the belt. [Hint:

- T1

- T2 = eµθ (see problem 7.102).]


- d) Thebeltinusehasa15mm×5mmrectangular cross-section. Find the maximum tensile stress in the belt.


10 kg

|C| |
|---|---|
| | |


A

60 cm

5 kg

B

F = 310 N

20 kg 40 cm

problem 7.84:

(Filename:pﬁgure.s94h8p4)

- 7.83 A bevel-type gear system, shown in the ﬁgure, is used to transmit power between two shafts that are perpendicular to each other. The driving gear has a mean radius of 50mm and rotates at a constant speed ω = 150rpm. The mean radius of the driven gear is 80mm and the driven shaft is expected to deliver a torque

of Mout = 25N·m. Assuming no power loss, ﬁnd the input torque supplied by the driving shaft

driving gear

ıˆ

ˆ

problem 7.83:

(Filename:pﬁgure4.rpa)

- 7.84 Disk pulleys. Two uniform disks A and B of non-negligible masses 10kg and 5kg respectively, are used as pulleys to hoist a block of mass 20kg as shown in the ﬁgure. The block is pulled up by applying a force F = 310N at one end of the string. Assume the string to be massless but ‘frictionful’ enough to not slide on the pulleys. Use g = 10m/s2.


- a) Find the angular acceleration of pulley B. ∗
- b) Find the acceleration of block C. ∗
- c) Find the tension in the part of the string between the block and the overhead pulley. ∗


- 7.85 A spindle and pulley arrangement is used to hoist a 50kg mass as shown in the ﬁgure. Assume that the pulley is to be of negligible mass. When the motor is running at a constant 100rpm,

- a) Find the velocity of the mass at B.
- b) Find the tension in strings AB and CD.


![image 40](Introduction to Statics and Dynamics Problems_images/imageFile40.png)

![image 41](Introduction to Statics and Dynamics Problems_images/imageFile41.png)

![image 42](Introduction to Statics and Dynamics Problems_images/imageFile42.png)

![image 43](Introduction to Statics and Dynamics Problems_images/imageFile43.png)

| |B|
|---|---|
| | |


motor r = 150 mm

r = 250 mm

A 50 kg

C

D

spindle r = 300 mm

problem 7.85:

(Filename:pﬁgure4.rpg)

- 7.86 Two racks connected by three constant rate gears. See also problem 4.19. A 100lbf force is applied to one rack. At the output, the


machinery (not shown) applies a force of FB to the other rack.

- a) Assume the gear-train is spinning at constant rate and is frictionless. What is FB? ∗
- b) If the gear bearings had friction would

that increase or decrease FB to achieve the same constant rate?

- c) If instead of applying a 100lbf to the left rack it is driven by a motor (not shown) at constant speed v, what is the speed of the right rack? ∗


y

FB = ?

massless rack

x B

RC A b C RE d E

RA

no slip

no slip 100 lb

massless rack

problem 7.86: Two racks connected by three gears.

(Filename:ch4.5)

- 7.87 Two racks connected by three accelerating gears. A 100lbf force is applied to one rack. At the output, the machinery (not shown) applies a force of FB to the other rack.

- a) Assume the gear-train is spinning at constant rate and is frictionless, what is FB?
- b) If the gear bearings had friction would

that increase or decrease FB to achieve the same constant rate?

- c) If the angular velocity of the gear is increasing at rate α does this increase or decrease FB at the given ω.


massless rack

massless rack

no slip

FB = ?

RA

RC A b C RE d E

no slip 100 lb

x B

y

problem 7.87: Two racks connected by three gears.

(Filename:pg131.2)

- 7.88 3-D accelerating gear train. This is really a 2-D problem; each gear turns in a different parallel plane. Shaft B is rigidly connected to gears G4 and G5. G5 meshes with gear G6. Gears G6 and G5 are both rigidly attached to shaft AD. Gear G5 meshes with G2 which is welded to shaft A. Shaft A and shaft B spin independently. Assume you know the torque Minput, angular velocity ωinput and the angu-


lar acceleration αinput of the input shaft. Assume the bearings and contacts are frictionless.

- a) What is the input power?
- b) What is the output power?
- c) What is the angular velocity ωoutput of the output shaft?
- d) What is the output torque Moutput?


x

G5

C

G6

G5

ωout

C D

A

G6

G1 ωin

D

G1

B

A

y

G2

ωout

G4 G2 G3

B ωin

G3

G4

###### = 3 RG

RG

2

5

###### 3 RG

###### = 5 RG

Front view

z

3

6

problem 7.88: A 3-D set of gears turning at constant rate.

(Filename:3dgeartrain)

- 7.89 A uniform disk of mass M and radius R rotatesaboutahinge O inthexy-plane. Apoint mass m is ﬁxed to the disk at a distance R/2 from the hinge. A motor at the hinge drives the disk/point mass assembly with constant angular acceleration α. What torque at the hinge does the motor supply to the system?
- 7.90 The asymmetric dumbbell shown in the ﬁgure is pivoted in the center and also attached to a spring at one quarter of its length from the bigger mass. When the bar is horizontal, the

compression in the spring is ys. At the instant of interest, the bar is at an angle θ from the

horizontal; θ is small enough so that y ≈ L2 θ. If, at this position, the velocity of mass ‘m’ is

vˆ and that of mass 3m is −vˆ, evaluate the power term ( F · v) in the energy balance equation.

massless

L

3m m

k

problem 7.90:

(Filename:pﬁg2.3.rp4)

- 7.91 The dumbbell shown in the ﬁgure has a torsional spring with spring constant k (tor-


sional stiffness units are kN·m

rad ). The dumbbell oscillates about the horizontal position with small amplitude θ. At an instant when the angular velocity of the bar is θ˙kˆ, the velocity of theleftmassis−Lθ˙ˆ andthatoftherightmass is Lθ˙ˆ. Find the expression for the power P of the spring on the dumbbell at the instant of interest.

###### ˆ

torsional spring constant k

ıˆ

2m m

L L

###### problem 7.91:

(Filename:pﬁg2.3.rp10)

- 7.92 A physical pendulum. A swinging stick is sometimes called a ‘physical’ pendulum. Take the ‘body’, the system of interest, to be the whole stick.

- a) Draw a free body diagram of the system.
- b) Write the equation of angular momentum balance for this system about point O.
- c) Evaluatetheleft-hand-sideasexplicitly as possible in terms of the forces showing on your Free Body Diagram.
- d) Evaluate the right hand side as completely as possible. You may use the following facts:


v = lθ˙ cosθˆ + −lθ˙ sinθıˆ a = −lθ˙2 cosθıˆ + sinθˆ

+lθ¨ cosθˆ − sinθıˆ

where is the distance along the pendulum from the top, θ is the angle by which the pendulum is displaced counter-clockwise from the vertically downposition,ıˆ is verticallydown, and ˆ is to the right. You will have to set up and evaluate an integral.

| | |
|---|---|
| | |


O

L

ıˆ

ˆ

θ

problem 7.92:

(Filename:ppend)

- 7.93 Which of (a), (b), and (c) are two force members?


Swinging rod with mass

(a)

(b)

Stationary rod with mass

| |
|---|
| |


uniform rigid bar, mass m

θ

g g

| | |
|---|---|
| | |


uniform rigid bar, mass m

(c)

Massless swinging rod

g

θ

m rigid, massless bar

problem 7.93:

(Filename:pﬁgure2.two.force)

- 7.94 For the pendula in the ﬁgure :

- a) Without doing any calculations, try to ﬁgure out the relative durations of the periods of oscillation for the ﬁve pendula (i.e. the order, slowest to fastest) Assume small angles of oscillation.
- b) Calculate the period of small oscillations. [Hint: use balance of angular momentum about the point 0]. ∗
- c) Rank the relative duration of oscillations and compare to your intuitive solution in part (a), and explain in words why things work the way they do.


| | |
|---|---|
| | |


(a)

(c) (d) (e)

(b)

rigid, massless bar

M

M

M

2m

1m

- 1m

1m

- 2m


M

M

M

θ θ θ

g

rigid, massless bar

uniform bar M = 1kg

rigid, massless bar

rigid, massless bar

θ θ

2m

2m

O O

O O O

problem 7.94:

(Filename:pg144.1n)

- 7.95 A massless 10 meter long bar is supported by a frictionless hinge at one end and has a 3.759kg point mass at the other end. It is released at t = 0 from a tip angle of φ = .02radians measured from vertically upright position (hinge at the bottom). Use g = 10ms−2.


- a) Using a small angle approximation and the solution to the resulting linear differential equation, ﬁnd the angle of tip at t = 1s and t = 7s. Use a calculator, not a numerical integrator.
- b) Using numerical integration of the nonlinear differential equation for an inverted pendulum ﬁnd φ at t = 1s and t = 7s.
- c) Make a plot of the angle versus time for yournumericalsolution. Includeonthe sameplottheangleversustimefromthe approximate linear solution from part (a).
- d) Comment on the similarities and differences in your plots.


- 7.96 Aspring-mass-dampersystemisdepicted in the ﬁgure. The horizontal damping force

applied at B is given by FD = −cy˙B The dimensions and parameters are as follows:

rB/0 = 2 f t rA/0 = = 3 f t

k = 2lbf/ft c = 0.3lbf · s/ft

For small θ, assume that sin(θ) ≈ θ and cos(θ) ≈ 1.

- a) Determine the natural circular frequencyofsmalloscillationsaboutequilibrium for the pendulum shown. The static equilibrium position is θ = 0 (pendulum hanging vertically), so the spring is at its rest point in this position. Idealize the pendulum as a point mass attached to a rigid massless rod of length 1, so I O = m 2. Also use the “small angle approximation” where appropriate.
- b) Sketch a graph of θ as a function of t(t ≥ 0) if the pendulum is released from rest at position θ = 0.2rad when t = 0. Your graph should show the correct qualitative behavior, but calculations are not necessary.


| |B<br><br>c<br><br>|
|---|---|
| |θ|


m

O

A

k

x

y

g

problem 7.96:

(Filename:pﬁgure.blue.157.2)

- 7.97 Arigidmasslessrodhastwoequalmasses


mB and mC (mB = mC = m) attached to it at distances 2L and 3 , respectively, measured along the rod from a frictionless hinge located at a point A. The rod swings freely from the hinge. There is gravity. Let φ denote the angle of the rod measured from the vertical. Assume

that φ and φ˙ are known at the moment of interest.

- a) What is φ¨? Solve in terms of m, , g, φ and φ˙.
- b) What is the force of the hinge on the rod? Solve in terms of m, , g, φ, φ˙, φ¨ and any unit vectors you may need to deﬁne.
- c) Would you get the same answers if you put a mass 2m at 2.5 ? Why or why not?


2

φ

m

rigid massless bar

m

problem 7.97:

(Filename:pﬁgure.twomasspend)

- 7.98 See also problem 4.3. A zero length

spring (relaxed length 0 = 0) with stiffness k = 5N/m supports the pendulum shown.

- a) Findθ¨ assumingθ˙ = 2rad/s, θ = π/2. ∗
- b) Find θ¨ as a function of θ˙ and θ (and k, , m, and g.) ∗


[Hint: use vectors (otherwise it’s hard)] [Hint: For the special case, kD = mg, the

solution simpliﬁes greatly.]

D = 4 m

m = 2 kg

0 = 0 k = 5 N/m

g = 10 m/s

θ

x

y

= 3 m

problem 7.98:

(Filename:pﬁgure.blue.80.2)

- 7.99 Robotics problem: Simplest balancing of an inverted pendulum. You are holding a stick upside down, one end is in your hand, the other end sticking up. To simplify things, think of the stick as massless but with a point mass at the upper end. Also, imagine that it is only a two-dimensional problem (either you can ignore one direction of falling for simplicity or imagine wire guides that keep the stick from moving in and out of the plane of the paper on which you draw the problem).


Younotethatifyoumodelyourholdingthe stick as just having a stationary hinge then you

get φ¨ = gl sinφ. Assuming small angles, this hingeleadstoexponentiallygrowingsolutions.

Upside-down sticks fall over. How can you prevent this falling?

One way to do keep the stick from falling over is to ﬁrmly grab it with your hand, and if the stick tips, apply a torque in order to right it. This corrective torque is (roughly) how your ankles keep you balanced when you stand upright. Your task in this assignment is to design a robot that keeps an inverted pendulum balanced by applying appropriate torque.

Your model is: Inverted pendulum, length

, point mass m, and a hinge at the bottom with a motor that can apply a torque Tm. The stick might be tipped an angle φ from the vertical. A horizontal disturbing force F(t) is applied to the mass (representing wind, annoying friends, etc).

- a) Draw a picture and a FBD
- b) Write the equation for angular momentum balance about the hinge point. ∗
- c) Imagine that your robot can sense the angle of tip φ and its rate of change φ˙ and can apply a torque in response to that sensing. That is you can make

Tm any function of φ and φ˙ that you want. Can you ﬁnd a function that will makethependulumstayupright? Make a guess (you will test it below).

- d) Testyourguessthefollowingway: plug it into the equation of motion from part (b), linearize the equation, assume the disturbing force is zero, and see if the solution of the differential equation has exponentially growing (i.e. unstable) solutions. Go back to (c) if it does and ﬁnd a control strategy that works.
- e) Pick numbers and model your system on a computer using the full non-linear equations. Use initial conditions both close to and far from the upright position and plot φ versus time.
- f) If you are ambitious, pick a non-zero forcing function F(t) (say a sine wave of some frequency and amplitude) and see how that affects the stability of the solution in your simulations.

C

A

![image 44](Introduction to Statics and Dynamics Problems_images/imageFile44.png)

![image 45](Introduction to Statics and Dynamics Problems_images/imageFile45.png)

x

y

φ

eˆθ eˆr

m

- g


###### problem 7.99:

(Filename:pﬁgure.s94h9p1)

7.100 Balancing a system of rotating particles. A wire frame structure is made of four concentric loops of massless and rigid wires, connected to each other by four rigid wires presently coincident with the x and y axes. Three masses, m1 = 200grams, m2 = 150grams and m3 = 100grams, are glued to the structure as shown in the ﬁgure. The structurerotatescounter-clockwiseataconstantrate θ˙ = 5rad/s. There is no gravity.

- a) Find the net force exerted by the struc-

ture on the support at the instant shown.

∗

- b) You are to put a mass m at an appropriate location on the third loop so that the net force on the support is zero. Find the appropriate mass and the location on the loop.


- r3=30 cm
- r4=40 cm


y

ω

=20 cm

| |r2<br><br>m1|
|---|---|
|m2|m|


r1=10 cm

x

30o

45o 3

problem 7.100:

(Filename:pﬁgure.s94h6p2)

- 7.101Aropeoflength andtotalmassm isheld ﬁxed at one end and whirled around in circular motion at a constant rate ω in the horizontal plane. Ignore gravity.

- a) Findthetensionintheropeasafunction of r, the radial distance from the center of rotation to any desired location on the rope. ∗
- b) Where does the maximum tension occur in the rope? ∗ .
- c) At what distance from the center of rotation does the tension drop to half its maximum value? ∗ .


- 7.102 Assume that the pulley shown in ﬁgure(a) rotates at a constant speed ω. Let the angle of contact between the belt and pulley surface be θ. Assume that the belt is massless and that the condition of impending slip exists between the pulley and the belt. The free body diagram of an inﬁnitesimal section ab of the belt is shown in ﬁgure(b).


- a) Write the equations of linear momentum balance for section ab of the belt in the ıˆ and ˆ directions.
- b) Eliminate the normal force N from the two equations in part (a) and get a differential equation for the tension T in termsofthecoefﬁcientoffrictionµand The contact angle θ.


c) Show that the solution to the equation in part (b) satisﬁes TT1

2 = eµθ, where T1 and T2 are the tensions in the lower and the upper segments of the belt, respectively.

- a
- b


T2

dθ ω

θ

T1

- (a)
- (b)


###### ˆ

b

ıˆ

T dFf = µdN

a

dN

T+dT

dθ/2

dθ

###### problem 7.102:

(Filename:pﬁgure4.rpf)

##### 7.5 Polar moment of inertia:

##### Izzcm and IzzO Skills

- 7.103 A point mass m = 0.5kg is located at x = 0.3m and y = 0.4m in the xy-plane. Find the moment of inertia of the mass about the z-axis. ∗
- 7.104 A small ball of mass 0.2kg is attached to a 1m long inextensible string. The ball is to execute circular motion in the xy-plane with the string fully extended.

- a) What is value of Izz of the ball about the center of rotation? ∗
- b) How much must you shorten the string to reduce the moment of inertia of the ball by half? ∗


- 7.105 Two identical point masses are attached to the two ends of a rigid massless bar of length

(one mass at each end). Locate a point along the length of the bar about which the polar moment of inertia of the system is 20% more than that calculated about the mid point of the bar.

∗

- 7.106 A dumbbell consists of a rigid massless bar of length and two identical point masses m and m, one at each end of the bar.

- a) About which point on the dumbbell is

its polar moment of inertia Izz a minimum and what is this minimum value? ∗

- b) About which point on the dumbbell is


its polar moment of inertia Izz a maximum and what is this maximum value? ∗

- 7.107 Think ﬁrst, calculate later. A light rigid rod AB of length 3 has a point mass m at end A and a point mass 2m at end B. Point C is the center of mass of the system. First, answer the following questions without any calculations and then do calculations to verify your guesses.


- a) Aboutwhichpoint A, B, orC, isthepo-

lar moment of inertia Izz of the system a minimum? ∗

- b) About which point is Izz a maximum? ∗
- c) What is the ratio of IzzA and IzzB? ∗
- d) Is the radius of gyration of the system greater, smaller, or equal to the length of the rod? ∗


y

x

problem 7.107:

m

- A
- B
- C


3

2m

(Filename:pﬁgure4.4.rp1)

- 7.108 Do you understand the perpendicular axis theorem? Three identical particles of mass m are connected to three identical massless rods of length and welded together at point O as shown in the ﬁgure.

- a) Guess (no calculations) which of the three moment of inertia terms IxxO , IyyO ,

IzzO is the smallest and which is the biggest. ∗

- b) Calculate the three moments of inertia to check your guess. ∗
- c) If the orientation of the system is changed, so that one mass is along the x-axis, will your answer to part (a) change?
- d) Findtheradiusofgyrationofthesystem for the polar moment of inertia. ∗ m m


m

O

120o

120o

x

y

problem 7.108:

(Filename:pﬁgure4.4.rp3)

- 7.109 Show that the polar moment of inertia IzzO of the uniform bar of length and mass m,


shown in the ﬁgure, is 13m 2, in two different ways:

- a) by using the basic deﬁnition of polar moment of inertia IzzO = r2 dm, and
- b) by computing Izzcm ﬁrst and then using the parallel axis theorem.


y

m O

x

problem 7.109:

(Filename:pﬁgure4.4.rp5)

- 7.110 Locate the center of mass of the tapered rod shown in the ﬁgure and compute the polar

moment of inertia Izzcm. [Hint: use the variable thickness of the rod to deﬁne a variable mass

density per unit length.]

m = 1 kg 20 mm

5 mm

100 mm

x

y

problem 7.110:

(Filename:pﬁgure4.4.rp6)

- 7.111 Ashortrodofmassm andlengthh hangs from an inextensible string of length .

- a) Find the moment of inertia IzzO of the rod.
- b) Find the moment of inertia of the rod

IzzO by considering it as a point mass located at its center of mass.

- c) Find the percent error in IzzO in treating the bar as a point mass by comparing theexpressionsinparts(a)and(b). Plot the percent error versus h/ . For what valuesofh/ isthepercentageerrorless than 5%?


O

x

y

![image 46](Introduction to Statics and Dynamics Problems_images/imageFile46.png)

![image 47](Introduction to Statics and Dynamics Problems_images/imageFile47.png)

h

m

problem 7.111:

(Filename:pﬁgure4.4.rp11)

- 7.112 A small particle of mass m is attached to the end of a thin rod of mass M (uniformly distributed), which is pinned at hinge O, as depicted in the ﬁgure.


- a) Obtain the equation of motion governing the rotation θ of the rod.
- b) Whatisthenaturalfrequencyofthesystem for small oscillations θ?


O

/3

g

M

2 /3 θ

m

problem 7.112:

(Filename:pﬁgure.blue.151.3)

- 7.113 A thin rod of mass m and length is hinged with a torsional spring of stiffness K at A, and is connected to a thin disk of mass M and radius R at B. The spring is uncoiled when

θ = 0. Determine the natural frequency ωn of the system for small oscillations θ, assuming that the disk is:

- a) welded to the rod, and ∗
- b) pinned frictionlessly to the rod. ∗


A

M

R

B

K

m θ

g

problem 7.113:

(Filename:pﬁgure.blue.151.4)

- 7.114 Do you understand the parallel axis theorem? A massless square plate ABCD has four identical point masses located at its corners.

- a) Find the polar moment of inertia Izzcm. ∗
- b) Find a point P on the plate about which

the system’s moment of inertia Izz is maximum? ∗

- c) Find the radius of gyration of the system. ∗


m m

m m

- A D
- B C x


y

problem 7.114:

(Filename:pﬁgure4.4.rp2)

- 7.115 Perpendicular axis theorem and symmetry. For the massless square plate with four point masses on the corners, the polar moment


of inertia Izzcm = 0.6kg · m2. Find Ixxcm of the system. ∗

- A D
- B C x


m m

y

m m

problem 7.115:

(Filename:pﬁgure4.4.rp4)

- 7.116 A uniform square plate (2m on edge) has a corner cut out. The total mass of the remainingplateis3kg. Itspinsabouttheorigin at a constant rate of one revolution every π s.

- a) What is the moment of inertia of the plate about point O?
- b) Where is the center of mass of the plate at the instant shown?
- c) What are the velocity and acceleration of the center of mass at the instant shown?
- d) What is the angular momentum of the plate about the point O at the instant shown?
- e) What are the total force and moment required to maintain this motion when the plate is in the conﬁguration shown?
- f) What is the total kinetic energy of the plate?


x

y

1m

2m

2m

1m

ω

O

problem 7.116:

(Filename:pﬁgure.blue.87b.1)

- 7.117 A uniform thin triangular plate of mass m, height h , and base b lies in the xy-plane.


- a) Set up the integral to ﬁnd the polar moment of inertia IzzO of the plate. ∗
- b) Show that IzzO =

m 6

(h2 +3b2) by evaluating the integral in part (a).

- c) Locate the center of mass of the plate and calculate Izzcm.


y

A

h

m O

x

b B

problem 7.117:

(Filename:pﬁgure4.4.rp9)

- 7.118 A uniform thin plate of mass m is cast in the shape of a semi-circular disk of radius R as shown in the ﬁgure.

- a) Find the location of the center of mass of the plate
- b) Find the polar moment of inertia of the plate, Izzcm. [Hint: It may be easier to


set up and evaluate the integral for IzzO and then use the parallel axis theorem

to calculate Izzcm.]

O

m

R

x

y

problem 7.118:

(Filename:pﬁgure4.4.rp10)

- 7.119 A uniform square plate of side = 250mm has a circular cut-out of radius r = 50mm. The mass of the plate is m =

- 1

- 2


kg.

- a) Find the polar moment of inertia of the plate.
- b) Plot Izzcm versus r/ .
- c) Find the limiting values of Izzcm for r = 0 and r = .


m

r

x

y

problem 7.119:

(Filename:pﬁgure4.4.rp7)

- 7.120 A uniform thin circular disk of radius r = 100mm and mass m = 2kg has a rectangular slot of width w = 10mm cut into it as shown in the ﬁgure.


a) Find the polar moment of inertia IzzO of the disk.

- e) Assume that you don’t know θ, θ˙ or θ¨ but you do know that F1 is applied to the rod, perpendicular to the rod at m1. What is θ¨? (Neglect gravity.)
- f) If F1 were applied to m2 instead of m1, would θ¨ be bigger or smaller?


- 7.126 Therodshownisuniformwithtotalmass m and length . The rod is pinned at point 0. A linear spring with stiffness k is attached at the point A at height h above 0 and along the rod as shown. When θ = 0, the spring is unstretched. Assume that θ is small for both parts of this problem.

- a) Find the natural frequency of vibration (in radians per second) in terms of m, g, h, and k.
- b) If you have done the calculation above correctly there is a value of h for which the natural frequency is zero. Call this value of h, hcrit. What is the behavior of the system when h < hcrit? (Desired is a phrase pointing out any qualitative change in the type of motion with some justiﬁcation.)


h

O

A

k

uniform rod, θ mass m

g

problem 7.126:

(Filename:pﬁgure.blue.153.2)

- 7.127 Auniformstickoflength andmassm is a hair away from vertically up position when it isreleasedwithnoangularvelocity(a‘hair’isa technical word that means ‘very small amount, zero for some purposes’). It falls to the right. What is the force on the stick at point O when the stick is horizontal. Solve in terms of , m, g, ıˆ, and ˆ. Carefully deﬁne any coordinates, base vectors, or angles that you use.

O

ıˆ

ˆ

problem 7.127:

(Filename:pﬁgure.s94q8p1)

- 7.128 Acceleration of a trap door. A uniform bar AB of mass m and a ball of the same mass are released from rest from the same horizontal position. The bar is hinged at end A. There is gravity.


b) Locate the center of mass of the disk and calculate Izzcm.

y

w O

= 1 + 2

1

x

m

![image 48](Introduction to Statics and Dynamics Problems_images/imageFile48.png)

![image 49](Introduction to Statics and Dynamics Problems_images/imageFile49.png)

O x

2

m1

r

θ

m2

F1

problem 7.120:

problem 7.122:

(Filename:pﬁgure4.4.rp8)

(Filename:pﬁgure.blue.82.1)

- 7.123 A uniform rigid rod rotates at constant speed in the xy-plane about a peg at point O. The center of mass of the rod may not exceed a

speciﬁed acceleration amax = 0.5m/s2. Find the maximum angular velocity of the rod.

= 0.5 m

x

y

O

![image 50](Introduction to Statics and Dynamics Problems_images/imageFile50.png)

![image 51](Introduction to Statics and Dynamics Problems_images/imageFile51.png)

problem 7.123:

(Filename:pﬁgure4.3.rp3)

- 7.124 A uniform one meter bar is hung from a hinge that is at the end. It is allowed to swing freely. g = 10m/s2.

- a) What is the period of small oscillations for this pendulum?
- b) Suppose the rod is hung 0.4m from one end. What is the period of small oscillations for this pendulum? Can you explain why it is longer or shorter than when it is is hung by its end?


- 7.125 A motor turns a bar. A uniform bar of length and mass m is turned by a motor whose shaft is attached to the end of the bar at O. The angle that the bar makes (measured counter-clockwise) from the positive x axis is θ = 2π t2/s2. Neglect gravity.


##### 7.6 Using Izzcm and IzzO in me-chanics equations

- 7.121 Motor turns a dumbbell. Two uniform bars of length and mass m are welded at right angles. Attheendsofthehorizontalbararetwo more masses m. The bottom end of the vertical rod is attached to a hinge at O where a motor keeps the structure rotating at constant rate ω (counter-clockwise). What is the net force and moment that the motor and hinge cause on the structure at the instant shown?

m m m

m

O

x

y

ıˆ

ˆ

ω motor

problem 7.121:

(Filename:pﬁgure.s94h5p5)

- 7.122 An object consists of a massless bar with


- a) Draw a free body diagram of the bar.
- b) Find the force acting on the bar from the motor and hinge at t = 1s.
- c) Find the torque applied to the bar from the motor at t = 1s.
- d) What is the power produced by the motor at t = 1s?


two attached masses m1 and m2. The object is hinged at O.

- a) What is the moment of inertia of the object about point O (IzzO)?
- b) Given θ, θ˙, and θ¨, what is HO, the angular momentum about point O?
- c) Given θ, θ˙, and θ¨, what is H˙ O, the rate of change of angular momentum about point O?
- d) Given θ, θ˙, and θ¨, what is T, the total kinetic energy?


###### ˆ

![image 52](Introduction to Statics and Dynamics Problems_images/imageFile52.png)

![image 53](Introduction to Statics and Dynamics Problems_images/imageFile53.png)

ıˆ

- a) Which point on the rod has the same acceleration as the ball, immediately after release. ∗
- b) What is the reaction force on the bar at end A just after release? ∗


θ

motor O

problem 7.125:

(Filename:pﬁgure.f93f1)

y

L m m A B C

![image 54](Introduction to Statics and Dynamics Problems_images/imageFile54.png)

A

![image 55](Introduction to Statics and Dynamics Problems_images/imageFile55.png)

###### ˆ

C

problem 7.128:

d

m

(Filename:pﬁgure.s94h8p3)

ıˆ

θ

###### ω

G

| | |
|---|---|
| | |


O m

x

motor

m

problem 7.132: A bent bar is rotated by a motor.

- 7.129 A pegged compound pendulum. See also problem 7.130. A uniform bar of mass m and length hangs from a peg at point C and swings in the vertical plane about an axis passing through the peg. The distance d from the center of mass of the rod to the peg can be changed by putting the peg at some other point along the length of the rod.


B

problem 7.129:

(Filename:pg85.3)

(Filename:pﬁgure.s94h8p6)

###### 7.133 2-D problem, no gravity. A uniform

stick with length and mass Mo is welded to a pulley hinged at the center O. The pulley

has negligible mass and radius Rp. A string is wrapped many times around the pulley. At time t = 0, the pulley, stick, and string are at rest and a force F is suddenly applied to the string. How long does it take for the pulley to make one full revolution? ∗

7.130Givenθ¨, θ˙, andθ, whatisthetotalkinetic energy of the pegged compound pendulum in problem 7.129?

- a) Find the angular momentum of the rod as about point C.
- b) Find the rate of change of angular momentum of the rod about C.
- c) How does the period of the pendulum vary with d? Show the variation by plotting the period against d . [Hint, you must ﬁrst ﬁnd the equations of motion, linearize for small θ, and then solve.] ∗

- d) Find the total energy of the rod (using the height of point C as a datum for potential energy).
- e) Find θ¨ when θ = π/6.
- f) Find the reaction force on the rod at C, as a function of m, d, , θ, and θ˙.
- g) For the given rod, what should be the value of d (in terms of ) in order to have the fastest pendulum? ∗
- h) Test of Schuler’s pendulum. The pendulum with the value of d obtained in (g) is called the Schuler’s pendulum. It isnotonlythefastestpendulumbutalso the “most accurate pendulum”. The claim is that even if d changes slightly over time due to wear at the support point, the period of the pendulum does not change much. Verify this claim by calculating the percent error in the time period of a pendulum of length


stick, mass = Mo

- 7.131 A slender uniform bar AB of mass M is hinged at point O, so it can rotate around O without friction. Initially the bar is at rest in the vertical position as shown. A bullet of mass m

and horizontal velocity Vo strikes the end A of the bar and sticks to it (an inelastic collision). Calculate the angular velocity of the system the bar with its embedded bullet, immediately after the impact.

m

M

O

B

A

Vo

- 1/3 L
- 2/3 L


problem 7.131:

(Filename:pﬁgure.blue.78.1)

- 7.132 Motor turns a bent bar. Two uniform barsoflength anduniformmassm arewelded at right angles. One end is attached to a hinge at O where a motor keeps the structure rotating at a constant rate ω (counterclockwise). What is the net force and moment that the motor and hinge cause on the structure at the instant shown.


F

Rp

O

massless pulley

problem 7.133: String wraps around a pulley with a stick glued to it.

(Filename:p2.3)

###### 7.134 A thin hoop of radius R and mass M ishung from a point on its edge and swings in itsplane. Assuming it swings near to the positionwhere its center of mass G is below the hinge:

- a) What is the period of its swinging oscillations?
- b) If, instead, thehoopwassettoswinging in and out of the plane would the period of oscillations be greater or less?


O

frictionless pivot

R

θ

G

= 1m under the following three conditions: (i) initial d = 0.15m and after some wear d = 0.16m, (ii) initial d = 0.29m and after some wear d = 0.30m, and (iii) initial d = 0.45m and after some wear d = 0.46m. Which pendulum shows the least error in its time period? Do you see any connection between this result and the plot obtained in (c)?

problem 7.134:

(Filename:pﬁgure.blue.145.1)

###### 7.135 The uniform square shown is releasedfrom rest at t = 0. What is α = ω˙ = θ¨immediately after release?

- a) neglecting gravity ∗
- b) including gravity. ∗


up y

###### θ

uniform square, mass=M

x

problem 7.135:

(Filename:pﬁgure.blue.42.2)

- 7.136 A square plate with side and mass m is hinged at one corner in a gravitational ﬁeld g. Find the period of small oscillation.

g

problem 7.136:

(Filename:p.f96.p3.2)

- 7.137 A wheel of radius R and moment of inertia I about the axis of rotation has a rope wound around it. The rope supports a weight W. Write the equation of conservation of energy for this system, and differentiate to ﬁnd the equation of motion in terms of acceleration. Check the solution obtained by drawing separate free-body diagrams for the wheel and for the weight, writing the equations of motion for each body, and solving the equations simultaneously. Assume that the mass of the rope is negligible, and that there is no energy loss during the motion.

W

θ R

problem 7.137:

(Filename:pﬁgure.blue.136.1)

- 7.138 A disk with radius R has a string wrapped around it which is pulled with a force F. The disk is free to rotate about the axis through O normal to the page. The moment of inertia of the disk about O is Io. A point A is


marked on the string. Given that xA(0) = 0 and that x˙A(0) = 0, what is xA(t)?

A

F

xA

R

xA(0) = 0 x˙A(0) = 0 xA(t) = ?

O

Inextensible string wound around spool

hinge

Spool has mass moment of inertia, IO

problem 7.138:

(Filename:pﬁgure.blue.42.1)

- 7.139 Oscillating disk. A uniform disk with mass m and radius R pivots around a frictionless hinge at its center. It is attached to a masslessspringwhichishorizontalandrelaxed when the attachment point is directly above the center of the disk. Assume small rotations and the consequent geometrical simpliﬁcations. Assume the spring can carry compression. What is the period of oscillation of the disk if it is disturbed from its equilibrium conﬁguration? [You may use the fact that, for the disk shown, H˙ O = 12mR2θ¨kˆ, where θ is the angle of rotation of the disk.]. ∗

k

R

m

g

problem 7.139:

(Filename:pg147.2)

- 7.140 This problem concerns a narrow rigid hoop. For reference, here are dimensions and values you should use in this problem: mass of hoop mhoop = 1kg radius of hoop Rhoop = 3m, and gravitational acceleration g = 10m/s2.

- a) The hoop is hung from a point on its edge and swings in its plane. Assuming its swings near to the position where its center of mass is below the hinge.
- b) What is the period of its swinging oscillations?
- c) If, instead, thehoopwassettoswinging in and out of the plane would the period of oscillations be greater or less?


- 7.141 The compound pulley system shown in the ﬁgure consists of two pulleys rigidly connected to each other. The radii of the two pul-


leys are: Ri = 0.2 m and Ro = 0.4 m. The combinedmomentofintertiaofthetwopulleys about the axis of rotation is 2.7 kg·m2. The two masses, m1 = 40 kg and m2 = 100 kg, are released from rest in the conﬁguration shown. Just after release,

- a) ﬁnd the angular acceleration of the pulleys, and ∗
- b) ﬁnd the tension in each string. ∗


Ro

Ri

m1 m2

problem 7.141:

(Filename:summer95p2.1)

- 7.142 Consider a system of two blocks A and B and the reel C mounted at the ﬁxed point O, as shown in the ﬁgure. Initially the system is at rest. Calculate the velocity for the block B after it has dropped a vertical distance h.

Given: h, mass of block A, MA, coefﬁcient of friction µ, slope angle θ, mass of the reel,

MC, moment of inertia I about point O radius of gyration of the reel KC, outer radius of the

reel RC, inner radius of the reel 12 RC, mass of the block B MB. The radius of gyration K

is deﬁned by Izzcm = mK2. (Apply the workenergy principle.) ∗

h

1/2 RC MB

RC MC,KC

V=2

At t=0, VA=0

At t=0, VB=0

θ

O

MA

µ

problem 7.142:

(Filename:pﬁgure.blue.135.1)

- 7.143 Gear A with radius RA = 400mm is rigidly connected to a drum B with radius


RB = 200mm. The combined moment of inertia of the gear and the drum about the axis of

rotationis Izz = 0.5 kg · m2. GearAisdriven by gear C which has radius RC = 300mm. As the drum rotates, a 5kg mass m is pulled up by a string wrapped around the drum. At the instant of interest, The angular speed and angular acceleration of the driving gear are 60rpm and 12rpm/s, respectively. Find the acceleration of the mass m. ∗

ωC,αC

RA

RB RC

A

B C

no slip

y m

x

problem 7.143:

(Filename:summer95f.2)

- 7.144 Two gears accelerating. See also problems 7.77 and 4.16. At the input to a gear box a 100lbf force is applied to gear A. At the output the machinery (not shown) applies a force of FB to the output gear.

- a) Assume the gear is spinning at constant rate and is frictionless, what is FB?
- b) If the gear bearing had friction would that increase or decrease FB?
- c) If the angular velocity of the gear is increasing at rate α does this increase or decrease FB at the given ω.


RA

RB RC

A

B

C

no slip

FA = 100 lb

FB = ?

problem 7.144: Two gears.

(Filename:pg131.3.aa)

- 7.145 Frequently parents will build a tower of blocks for their children. Just as frequently, kids knock them down. In falling (even when they start to topple aligned), these towers invariably break in two (or more) pieces at some point along their length. Why does this breaking occur? What condition is satisﬁed at the point of the break? Will the stack bend towards or away from the ﬂoor after the break?

This? or This?

problem 7.145:

(Filename:pﬁgure.blue.129.1)

- 7.146 Massless pulley, dumbell and a hanging mass. A mass M falls vertically but is withheld by a string which is wrapped around an ideal massless pulley with radius a. The pulley is welded to a dumbell made of a massless rod welded to uniform solid spheres at A and B of radius R, each of whose center is a distance from O. At the instant in question,


the dumbell makes an angle θ with the positive x axis and is spinning at the rate θ˙. Point C is a distance h down from O. In terms of some or all of m, M,a, R, ,h,g,θ, θ˙, and ˆ, ﬁnd the acceleration of the mass.

R

M A

θ

a

O

R

M h

###### ˆ

B

g

C

ıˆ

m

problem 7.146:

(Filename:s97p3.1)

7.147 Two racks connected by a gear. A 100lbf force is applied to one rack. At the output the machinery (not shown) applies a force FB to the other rack.

- a) Assume the gear is spinning at constant rate and is frictionless. What is FB?
- b) If the gear bearing had friction, would

that increase or decrease FB to achieve the same constant rate?

- c) If the angular velocity of the gear is increasing at rate α, does this increase or decrease FB at the given ω.
- d) If the output load FB is given then the motion of the machine can be found from the input load. Assume that the machine starts from rest with a given output load. So long as rack B moves in the opposite direction of the output force FB the output power is positive.


- (a) For what values of FB is the output power positive?
- (b) For what values of FB is the output work maximum if the machine starts from rest and runs for a ﬁxed amount of time?


###### ω

uniform disk m = 10 lbm

6 in

massless racks 100 lbf FB = ?

problem 7.147: Two racks connected by a gear.

(Filename:pg131.1)

- 7.148 2-D accelerating gear train. See also problem 7.74. Assume you know the torque

Minput = MA and angular velocity ωinput = ωA of the input shaft. Assume the bearings and contacts are frictionless. Assume you also know the input angular acceleration ω˙ and the moments of inertia IA, IB and IC of each of the disks about their centers .

- a) What is the input power?
- b) What is the output power?
- c) What is the angular velocity ωoutput = ωC of the output shaft?
- d) What is the output torque Moutput = MC?


RA

MA

RB

MC

RC

ωA

A B

C

no slip

ωC

problem 7.148: A set of gears turning at variable rate.

(Filename:pg129.1)

- 7.149 A stick welded to massless gear that rolls against a massless rack which slides on frictionless bearings and is constrained by a linear spring. Neglect gravity. The spring is relaxed when the angle θ = 0. Assume the

system is released from rest at θ = θ0. What is the acceleration of the point P at the end of the stick when θ = 0? Answer in terms of any or all of m, R, , θ0, k, ıˆ, and ˆ. [Hint: There are several steps of reasoning required. You might want to draw FBD(s), use angular momentum balance, set up a differential equation, solve it, plug values into this solution, and use the result to ﬁnd the quantities of interest.

P

k R

m, θ

ıˆ

ˆ

problem 7.149:

(Filename:p.f96.p2.2)

- 7.150 A tipped hanging sign is represented by a point mass m. The sign sits at the end of a massless, rigid rod which is hinged at its point of attachment to the ground. A taut massless elastic cord helps keep the rod vertical. The tension T in the very stretchy cord is idealized as constant during small displacements. (Note also that φ ≡ θ during such motions). Consider all hinges to be frictionless and motions to take place in the plane of the paper.


a) Write the angular momentum of the mass about 0 when the rod has an angular velocity θ˙.

- b) Find the differential equation that governs the mass’s motion for small θ.
- c) Describe the motion for T > mg2 , T =


2 , and T < mg2 . Interpret the differences of these cases in physical terms.

mg

string

L

φ

g

m

θ

L

rigid rod

O

problem 7.150:

(Filename:pﬁgure.blue.153.1)

Advanced topics in circular motion

##### 8.1 3-D description of circu-lar motion

8.1If Aand B are perpendicular, what is| A× ( A× B)|intermsof| A|and| B|? (Hint: make a neat 3-D sketch.)

- 8.2 A circular disk of radius r = 100mm rotates at constant speed ω about a ﬁxed but unknown axis. At the instant when the disk is in the xy-plane, the angular velocity of each point on the diameter AB (which is parallel to the x-

axis) is v = −2m/skˆ. At the same instant, the magnitude of the acceleration of the center of mass C is 50m/s2.

- a) Find the angular velocity of the disk.
- b) Find the location of the axis of rotation.
- c) Find the acceleration of points A and B.


A C B r

ıˆ

ˆ

kˆ

| | |
|---|---|
| | |


problem 8.2:

(Filename:pﬁgure4.3.rp10)

- 8.3 In the expression for normal acceleration

an = ω × ( ω × r), the parenthesis around ω × r is important because vector product is nonassociative. Showing ω×( ω× r)  = ( ω× ω) × r is almost trivial. (why?) Take ω1 = ω1kˆ, ω2 = ω2ıˆ +ω1kˆ and r = aıˆ −bˆ and show that ω1×( ω2× r)  = ( ω1× ω2)× r.

- 8.4 In circular motion the velocity is v = ω× r, where ω is the angular velocity and r is the position vector of the point of interest relative to a point on the axis of rotation. Compute v in the three cases below, draw the circular orbit, and show the vectors ω, r, and v.


- a) ω = 2rad/skˆ, r = 3mıˆ + 4mˆ.
- b) ω = 4.33rad/sıˆ + 2.5rad/sˆ, r = 0.5mıˆ − 0.87mˆ.


c) ω = 2rad/sıˆ + 2rad/sˆ + 2.83rad/skˆ, r = 3.5mıˆ+3.5mˆ − 4.95mkˆ.

- 8.5 The following questions are about the velocity and acceleration formulae for the nonconstant rate circular motion about a ﬁxed axis:

v = ω × r a = ω˙ × r + ω × ( ω × r)

- a) For planar circular motion about the zaxis, take

ω˙ = αkˆ, ω = ωkˆ, and r = ReˆR

and show that the velocity and acceleration formulae reduce to the formulae from elementary physics: v = ωReˆθ and a = −ω2ReˆR + Rαeˆθ.

- b) Draw a schematic picture of a particle (or a point on a rigid body) going in circles about a ﬁxed axis in 3-D. Take two distinctpointsontheaxisanddrawvec-


tors r1 and r2 from these two points to the particle of interest. Show, using theformulaefor v and a above,thatthe acceleration and velocity of the particle are the same irrespective of which r is used and thus conclude that the vector r can be taken from any point on the axis of rotation.

- 8.6 A rectangular plate with width w = 1m and length = 2m is rigidly attached to a shaft along one of its edges. The shaft rotates about the x-axis. The center of mass of the plate goes around at a constant linear speed v = 2.5m/s.

a) Find the angular velocity of the plate. b) At the instant shown, ﬁnd the velocity

of point P.

w

z

x

y

problem 8.6:

(Filename:pﬁgure4.3.rp1)

- 8.7 The solid cylinder shown has an angular velocity ω of magnitude 40 rad/s. The vector ω lies in the yz-plane. The origin O of the coordinate frame is at the center of the cylinder and is at rest. Find the following quantities:


- a) The vector ω.
- b) The velocity vA/B of point A relative to point B.


c) The acceleration aA of point A.

z

###### ω

y

A O

30o

x

300 mm

B

problem 8.7:

(Filename:pﬁgure.blue.37.1)

- 8.8 A rigid body rotates about a ﬁxed axis and has an angular acceleration α = 3π2(ıˆ +

1.5 ˆ + 1.5 kˆ)rad/s2. At a certain instant, the velocity of a point A of the body has xcomponent and y-component equal to 3 and −4 m/s, respectively. Find the magnitude vA of the velocity of point A.

- 8.9 Particle attached to a shaft, no gravity. See also problem 8.10. A shaft of negligible mass spins at a constant rate. The motor at A imposes this rate if needed. The bearing at A preventstranslationofitsendoftheshaftinany direction but causes no torques other than that

of the motor (which causes a torque in the kˆ direction). The frictionless bearing at C holds that end of the shaft from moving in the ıˆ and ˆ directions but allows slip in the kˆ direction. A bar of negligible mass is welded at right angles to the shaft. A small sphere of mass 1kg is attached to the free end of the bar. There is no gravity. The shaft is spinning counterclockwise (when viewed from the positive kˆ direction) at 3rad/s. In the conﬁguration of interest the rod BD is parallel to the ıˆ direction.

- a) What is the position vector of the mass in the given coordinate system at the instant of interest?
- b) What is angular velocity vector of the shaft?
- c) What are the velocity and acceleration of the particle at the instant of interest?


m = 1 kg

motor

0.2 m

0.1 m

0.1 m

ıˆ ˆ kˆ

massless

B

D

C

A y

![image 56](Introduction to Statics and Dynamics Problems_images/imageFile56.png)

![image 57](Introduction to Statics and Dynamics Problems_images/imageFile57.png)

![image 58](Introduction to Statics and Dynamics Problems_images/imageFile58.png)

![image 59](Introduction to Statics and Dynamics Problems_images/imageFile59.png)

![image 60](Introduction to Statics and Dynamics Problems_images/imageFile60.png)

![image 61](Introduction to Statics and Dynamics Problems_images/imageFile61.png)

x

z

problem 8.9:

(Filename:ch4.9)

- 8.10 Reconsider the particle on a shaft in problem 8.9.


of a point halfway down the rod BD relative the velocity and acceleration of the particle?

x direction) at angular speed ω with angular acceleration ω˙. At the instant of interest, the crooked rod lies in the xy-plane.

- a) What is the velocity of a point halfway downtherod BD relativetothevelocity of the mass at D?
- b) What is the acceleration of a point halfway down the rod BD relative to the acceleration of the mass at D?


x

motor

![image 62](Introduction to Statics and Dynamics Problems_images/imageFile62.png)

m = 1 kg

- a) In the coordinate system shown, what is the position vector of the point P on the rod?
- b) In the coordinate system shown, what are angular velocity and angular acceleration vectors of the rod and shaft?
- c) In the coordinate system shown, what is the velocity and acceleration of point P?
- d) What is the velocity and acceleration of point P relative to point Q?


![image 63](Introduction to Statics and Dynamics Problems_images/imageFile63.png)

![image 64](Introduction to Statics and Dynamics Problems_images/imageFile64.png)

D

![image 65](Introduction to Statics and Dynamics Problems_images/imageFile65.png)

![image 66](Introduction to Statics and Dynamics Problems_images/imageFile66.png)

![image 67](Introduction to Statics and Dynamics Problems_images/imageFile67.png)

0.1 m

A y

x

z

motor

massless

![image 68](Introduction to Statics and Dynamics Problems_images/imageFile68.png)

m = 1 kg

![image 69](Introduction to Statics and Dynamics Problems_images/imageFile69.png)

![image 70](Introduction to Statics and Dynamics Problems_images/imageFile70.png)

0.2 m

D

![image 71](Introduction to Statics and Dynamics Problems_images/imageFile71.png)

ıˆ ˆ kˆ

B

![image 72](Introduction to Statics and Dynamics Problems_images/imageFile72.png)

![image 73](Introduction to Statics and Dynamics Problems_images/imageFile73.png)

0.1 m

A y

z

0.1 m

massless

C

0.2 m

problem 8.12:

ıˆ ˆ kˆ

B

(Filename:ch5.3.copy)

0.1 m

- 8.13 Crooked rod. A one meter long uniform rodisweldedatitscenteratanangleφ toashaft as shown. The shaft is supported by bearings at its ends and spins at a constant rate ω. At the instant of interest, the crooked rod lies in the xy-plane.

- a) In the coordinate system shown, what is the position vector of the point P on the rod at the instant of interest? ∗
- b) In the coordinate system shown, what is the velocity and acceleration of point P at the instant of interest? ∗


![image 74](Introduction to Statics and Dynamics Problems_images/imageFile74.png)

![image 75](Introduction to Statics and Dynamics Problems_images/imageFile75.png)

O

weld

1.0 m

Q

P

0.5 m

0.25 m 0.5 m

φ

x

y

problem 8.13: A crooked rod spins on a shaft.

(Filename:ch4.7)

- 8.14 Crooked rod, again. Reconsider the crooked rod on a shaft in problem 8.13. What are the velocity and acceleration of point P relative to point Q?

![image 76](Introduction to Statics and Dynamics Problems_images/imageFile76.png)

![image 77](Introduction to Statics and Dynamics Problems_images/imageFile77.png)

O

weld

1.0 m

Q

P

0.5 m

0.25 m 0.5 m

φ

x

y

problem 8.14: A crooked rod spins on a shaft.

(Filename:pﬁgure4.crooked.a)

- 8.15 Crooked rod. A one meter long uniform rodisweldedatitscenteratanangleφ toashaft


1.0 m

C

problem 8.10: Particle attached to a shaft, no gravity

P

![image 78](Introduction to Statics and Dynamics Problems_images/imageFile78.png)

![image 79](Introduction to Statics and Dynamics Problems_images/imageFile79.png)

0.25 m 0.5 m

(Filename:pﬁgure4.particleshaft1.a)

y

Q

φ

- 8.11 Particle attached to a shaft, no gravity. See also problem 8.12. A shaft of negligible mass spins at variable rate. The motor at A imposes this rate if needed. The bearing at A preventstranslationofitsendoftheshaftinany direction but causes no torques other than that

of the motor (which causes a torque in the kˆ direction). The frictionless bearing at C holds that end of the shaft from moving in the ıˆ and ˆ directions but allows slip in the kˆ direction. The shaft is welded orthogonally to a bar, also of negligible mass, which is attached to a small ball of (non-negligible) mass of 1kg. There is no gravity. At the instant of interest, the shaft is spinning counterclockwise (when viewed from the positive kˆ direction) at ω = 3rad/s and ω˙ = 5rad/s2. In the conﬁguration of interest the rod BD is parallel with the ıˆ direction.

- a) In the coordinate system shown, what is the position vector of the particle at the instant of interest?
- b) In the coordinate system shown, what are angular velocity and angular acceleration vectors of the shaft?
- c) In the coordinate system shown, what is the velocity and acceleration of the particle at the instant of interest?


m = 1 kg

motor

0.2 m

0.1 m

0.1 m

ıˆ ˆ kˆ

massless

B

D

C

A y

![image 80](Introduction to Statics and Dynamics Problems_images/imageFile80.png)

![image 81](Introduction to Statics and Dynamics Problems_images/imageFile81.png)

![image 82](Introduction to Statics and Dynamics Problems_images/imageFile82.png)

![image 83](Introduction to Statics and Dynamics Problems_images/imageFile83.png)

![image 84](Introduction to Statics and Dynamics Problems_images/imageFile84.png)

![image 85](Introduction to Statics and Dynamics Problems_images/imageFile85.png)

x

z

problem 8.11:

(Filename:ch5.3)

- 8.12 Reconsider the particle on a shaft in problem 8.11. What is the velocity and acceleration


x

O

0.5 m

weld

problem 8.15: A crooked rod spins on a shaft.

(Filename:ch5.4)

8.16 A rigid rod OP of length L = 500mm is welded to a shaft AB at an angle θ = 30◦. The shaft rotates about its longitudinal axis at a constant rate ω = 120rpm. At the instant shown, the rod OP is in the the xz-plane.

- a) Neatly draw the path of point P. At the instant shown, draw the basis vectors eˆr and eˆθ and express them in terms of the basis vectors ıˆ, ˆ, kˆ.
- b) Find the radius of the circular path of point P and calculate the velocity and acceleration of the point using planar circular motion formulae v = θ˙eˆθ and a = −θ˙2Reˆr.
- c) Find the position vector r ≡ r P/O of point P. Use this position vector to compute the velocity and acceleration of point P using the general formulae v = ω× r and a = ω× ω× r. Show that the answers obtained here are the same as those in (b).


x

A

P O

30o

y

B

- as shown. The shaft is supported by bearings
- at its ends and spins at a variable rate. At the instant of interest the shaft is spinning counterclockwise (when viewed from the positive


z

ω

problem 8.16:

(Filename:pﬁgure4.2.rp1)

- 8.17 A uniform rectangular plate ABCD of width and length 2 rotates about its diagonal AC ataconstantangularspeedω = 5rad/s. At the instant shown, the plate is in the xz-plane.

- a) Find the velocity and acceleration of point B at the instant shown.
- b) Find the velocity and acceleration of point B when the plate is in the yzplane.


|A O C z<br><br>![image 86](Introduction to Statics and Dynamics Problems_images/imageFile86.png)<br><br>![image 87](Introduction to Statics and Dynamics Problems_images/imageFile87.png)<br><br>![image 88](Introduction to Statics and Dynamics Problems_images/imageFile88.png)<br><br>![image 89](Introduction to Statics and Dynamics Problems_images/imageFile89.png)<br><br>![image 90](Introduction to Statics and Dynamics Problems_images/imageFile90.png)<br><br>β|![image 91](Introduction to Statics and Dynamics Problems_images/imageFile91.png)<br><br>![image 92](Introduction to Statics and Dynamics Problems_images/imageFile92.png)<br><br>r normal to the axis of rotation). Using particular mass locations that you choose, show that 2 particles give a different value for H˙ C than a single par-|
|---|---|
|B<br><br>L y<br><br>ω<br><br>|ω<br><br>ticle at the center of mass. [Moral: In general, H˙ C  = rcm/C × mtot acm.]|


D

2L

x

problem 8.17:

(Filename:pﬁgure4.2.rp2)

- 8.18 Arectangularplateofwidthw = 100mm and length = 200mm rotates about one of its diagonals at a constant angular rate ω = 3rad/s. There is a ﬁxed coordinate system xyz with the origin at the center of the plate and the x-axis aligned with the axis of rotation. Another set of axes x y z , aligned with the principal axes of the plate, has the same origin but is attached to the plate and therefore, rotates with the plate. At the instant of interest, the plate is in the xy-plane and the two axes z and z coincide. Find the velocity of the corner point P as follows:

- a) Writetheangularvelocity ωoftheplate in terms of its components in the two coordinate systems.
- b) Find the velocity of point P in both coordinate systems using the expressions for ω found in part (a).
- c) Find the perpendicular distance d of point P from the axis of rotation, and show that the linear speed of point P calculated from velocities found in part (b) is ωd in each case.


O

x' y'

d

P

x

y

problem 8.18:

(Filename:pﬁgure4.3.rp11)

- 8.19 A cone of angle β sits on its side on a horizontal disk of radius r = 100mm as shown in the ﬁgure. The cone is attached to shaft AB


that turns in the bearing. The disk rotates at a constant angular speed ω = 120rpm. Assume that the cone rolls without slip on the disk. Thus, the disk drives the cone-and-shaft assembly causing it to turn in the bearing. Find the angular velocity of the cone as a function of the cone angle β. In particular, ﬁnd the angular velocity of the cone for

- a) 2-D (particles in the plane, axis of rotation normal to the plane). Show, by

calculating the sum in H˙ C that the result is the same when using the two particles or when using a single particle at the center of mass (with mass equal to the sum of the two particles). You may do the general problem or you may pickparticularappropriatelocationsfor the masses, particular masses for the masses, a speciﬁc point C, a speciﬁc axis and a particular rotation rate.

- b) 3-D (particles not in a common plane


- a) β = 30◦, and
- b) β = 90◦ (or 90◦ minus a hair if that makes you more comfortable).


A

B

problem 8.19:

- 8.22 The rotating two-mass system shown in the ﬁgure has a constant angular velocity ω = 12rad/sıˆ. Assume that at the instant shown, the masses are in the xy-plane. Take m = 1kg and L = 1m.

- a) Find the linear momentum L and its rate of change L˙ for this system.
- b) Find the angular momentum HO about


point O and its rate of change H˙ O for this system.

![image 93](Introduction to Statics and Dynamics Problems_images/imageFile93.png)

![image 94](Introduction to Statics and Dynamics Problems_images/imageFile94.png)

![image 95](Introduction to Statics and Dynamics Problems_images/imageFile95.png)

![image 96](Introduction to Statics and Dynamics Problems_images/imageFile96.png)

![image 97](Introduction to Statics and Dynamics Problems_images/imageFile97.png)

![image 98](Introduction to Statics and Dynamics Problems_images/imageFile98.png)

x

z

y L

m

m

L

L

L

A

O

ıˆ C

ˆ kˆ

problem 8.22:

(Filename:pﬁgure4.2.rp4)

- 8.23 Particle attached to a shaft, no gravity. A shaft of negligible mass spins at constant rate. The motor at A imposes this rate if needed. The bearing at A prevents translation of its end of the shaft in any direction but causes no torques other than that of the motor


(Filename:pﬁgure4.rpb)

##### 8.2 Dynamics of ﬁxed axis rotation

- 8.20 Let P(x, y, z) be a point mass on an abstract massless body that rotates at a constant rate ω about the z-axis. Let C(0,0, z) be the center of the circular path that P describes during its motion.

- a) Show that the rate of change of angular momentum of mass P about the origin O is given by

H˙ O = −mω2Rzeˆθ

where R = x2 + y2 is the radius of the circular path of point P.

- b) Is there any point on the axis of rotation


(z-axis) about which H˙ is zero. Is this point unique?

axis

C

P

z

y

x

O

ω = θ˙kˆ

θ˙

θ

problem 8.20:

(Filename:pﬁgure4.2.rp5)

- 8.21 System of Particles going in a circle. Assume for the problems below that you have two mass points going in circles about a common axis at a ﬁxed common angular rate.


(which causes a torque in thekˆ direction). The frictionless bearing at C holds that end of the shaft from moving in the ıˆ and ˆ directions

but allows slip in the kˆ direction. The shaft is welded orthogonally to a bar, also of negligible mass, which is attached to a small ball of(nonnegligible) mass of 1kg. There is no gravity. The shaft is spinning counterclockwise (when viewedfromthepositivekˆ direction)at3rad/s. In the conﬁguration of interest the rod BD is parallel with the ıˆ direction.

- a) What is the tension in the rod BD? ∗
- b) WhatareallthereactionforcesatAand C? ∗


z

R

- 8.28 A small rock swings in circles at constant angularrateω. Itishungbyastringwithlength

the other end of which is at the origin of a good coordinate system. The rock has mass m and the gravitational constant is g. The string makes an angle of φ with the negative z axis. The mass rotates so that if you follow it with the ﬁngers of your right hand, your right thumb points up the z-axis. At the moment of interest the mass is passing through the yz-plane.

- a) Draw a free body diagram of the rock.
- b) Howlongdoesittaketomakeonerevolution? Howdoesthiscomparewiththe period of oscillation of a simple pendulum. ∗
- c) Find the following quantities in any order that pleases you. All solutions should be in terms of m, g, , φ, ω and the unit vectors ıˆ, ˆ, and kˆ.


- • The tension in the string (T).
- • The velocity of the rock ( v).
- • The acceleration of the rock ( a).
- • The rate of change of the angular momentum about the +x axis (dHx/dt).


∗

- y

z

circle around

- z-axis


x

φ m

problem 8.28:

(Filename:pﬁgure.blue.14.2)

- 8.29 Consider the conﬁguration in problem 8.28. What is the relation between the angle (measured from the vertical) at which it hangs and the speed at which it moves? Do an experiment with a string, weight and stop watch to check your calculation. ∗
- 8.30 A small block of mass m = 5kg sits on an inclined plane which is supported by a bearing at point O as shown in the ﬁgure. At the instant of interest, the block is at a distance L = 0.5m from where the surface of the incline intersects the axis of rotation. By experiments, the limiting rate of rotation of the turntable before the block starts sliding up the inclined plane is found to be ω = 125rpm. Find the coefﬁcient of friction between the block and the incline.


- c) What is the torque that the motor at A causes on the shaft? ∗
- d) There are two ways to do problems (b) and (c): one is by treating the shaft, bar and mass as one system and writing the momentum balance equations. The other is to use the result of (a) with action-reaction to do statics on the shaft BC. Repeat problems (b) and (c) doing itthewayyoudidnotdoittheﬁrsttime.


ω

ω

R

SIDE VIEW

φ g

x

motor

![image 99](Introduction to Statics and Dynamics Problems_images/imageFile99.png)

m = 1 kg

![image 100](Introduction to Statics and Dynamics Problems_images/imageFile100.png)

![image 101](Introduction to Statics and Dynamics Problems_images/imageFile101.png)

φ

D

![image 102](Introduction to Statics and Dynamics Problems_images/imageFile102.png)

![image 103](Introduction to Statics and Dynamics Problems_images/imageFile103.png)

![image 104](Introduction to Statics and Dynamics Problems_images/imageFile104.png)

0.1 m

A y

z

massless

0.2 m

problem 8.25:

ıˆ ˆ kˆ

B

(Filename:pﬁgure.s95q6)

0.1 m

- 8.26 Mr. X swings his daughter Y about the vertical axis at a constant rate ω = 1rad/s. Y is merely one year old and weighs 12kg. Assuming Y to be a point mass located at the center of mass, estimate the force on each of her shoulder joints.

| | |
|---|---|
| | |


P

Mr. X

Y

L

d θ

ω

problem 8.26:

(Filename:pﬁgure4.2.rp12)

- 8.27 A block of mass m = 2kg supported by a light inextensible string at point O sits on the surface of a rotating cone as shown in the ﬁgure. The cone rotates about its vertical axis of symmetry at constant rate ω. Find the value of ω in rpm at which the block loses contact with the cone.


C

problem 8.23:

(Filename:pﬁgure.s94h7p1)

- 8.24 Particle attached to a shaft, with gravity. Consider the same situation as in problem 8.23 with the following changes: There is gravity (pointing in the −i direction). At the time of interest the rod BD is parallel to the +j direction.

- a) What is the force on D from the rod BD?(NotethattherodBDisnota‘twoforce’ member. Why not?)
- b) WhatareallthereactionforcesatAand C?
- c) What is the torque that the motor at A causes on the shaft?
- d) Do problems (b) and (c) again a different way.


- 8.25 A turntable rotates at the constant rate of ω = 2rad/s about the z axis. At the edge of the 2m radius turntable swings a pendulum which makes an angle φ with the negative z direction. The pendulum length is = 10m. The pendulum consists of a massless rod with a point mass m = 2kg at the end. The gravitational constant is g = 10m/s2 pointing in the −z direction. A perspective view and a side view are shown.


ω

O

- a) What possible angle(s) could the pendulum make in a steady motion. In other words, ﬁnd φ for steady circular motion of the system. It turns out that this quest leads to a transcendental equation. You are not asked to solve this equation but you should have the equation clearly deﬁned. ∗
- b) How many solutions are there? [hint, sketch the functions involved in your ﬁnal equation.] ∗
- c) Sketch very approximately any equilibrium solution(s) not already sketched onthesideviewinthepictureprovided.


m

α

problem 8.27:

(Filename:pﬁgure4.2.rp11)

ω

m

L C

O

problem 8.30:

(Filename:pﬁgure4.2.rp9)

- 8.31 Particle sliding in circles in a parabolic bowl. As if in a James Bond adventure in a big slippery radar bowl, a particle-like human with mass m is sliding around in circles at speed v. The equation describing the bowl is z = CR2 = C(x2 + y2).

- a) Find v in terms of any or all of R, g, and C.
- b) Nowsayyouaregivenω,C andg. Find v and R if you can. Explain any oddities.


problem 8.31:

(Filename:p.f96.p2.1)

- 8.32 Mass on a rotating inclined platform. A block of mass m = 5kg is held on an inclined platform by a rod BC as shown in the ﬁgure. The platform rotates at a constant angular rate ω. Thecoefﬁcientoffrictionbetweentheblock and the platform is µ. θ = 30o, L = 1m, and

- g = 9.81m/s2. (a) Assuming ω = 5rad/s and µ = 0 ﬁnd the tension in the rod. (b) If µ = .3 what is the range of ω for which the block would stay on the ramp without slipping even if there were no rod? ∗


ω

C

rod B

platform

A L

m

θ

ıˆ ˆ

kˆ

problem 8.32:

(Filename:pﬁgure.s94h5p6)

- 8.33 A circular plate of radius r = 10cm rotates in the horizontal plane about the vertical axis passing through its center O. Two identical point masses hang from two points on the plate diametrically opposite to each other as shown in the ﬁgure. At a constant angular speed ω, the two masses maintain a steady state angle θ from their vertical static equilibrium.


a) Findthelinearspeedandthemagnitude of the centripetal acceleration of either of the two masses.

b) Find the steady state ω as a function of θ. Do the limiting values of θ, θ → 0 and θ → π/2 give sensible values of ω?

ω g

r

O

θ θ

m m

problem 8.33:

(Filename:pﬁgure4.2.rp6)

- 8.34 For the rod and mass system shown in the ﬁgure, assume that θ = 60◦, ω ≡ θ˙ = 5rad/s, and = 1m. Find the acceleration of mass B at the instant shown by

- a) calculating a = ω × ω × r where r is the position vector of point B with

respect to point O, i.e., r = r B/O, and by

- b) calculating a = −Rθ˙2eˆR where R is the radius of the circular path of mass B.


|O| | |
|---|---|---|
| | | |


O

A

B

C

x

y

ω

problem 8.34:

(Filename:pﬁgure4.2.rp7)

- 8.35 A spring of relaxed length 0 (same as the diameter of the plate) is attached to the mid point of the rods supporting the two hanging masses.


- a) Find the steady angle θ as a function of the plate’s rotation rate ω and the spring constant k. (Your answer may include other given constants.)
- b) Verify that, for k = 0, your answer for θ reduces to that in problem 8.33.
- c) Assume that the entire system sits inside a cylinder of radius 20cm and the axis of rotation is aligned with the longitudinal axis of the cylinder. The maximum operating speed of the ro-


tating shaft is 200rpm (i.e., ωmax = 200rpm). If the two masses are not to touch the walls of the cylinder, ﬁnd the required spring stiffness k.

ω g

r

O

/2

θ θ

k=2r

0=2r

m m

problem 8.35:

(Filename:pﬁgure4.2.rp8)

- 8.36 Flyball governors are used to control the ﬂow of working ﬂuid in steam engines, diesel engines, steam turbines, etc. A spring-loaded ﬂyball governor is shown schematically in the ﬁgure. As the governor rotates about the verticalaxis, thetwomassestendtomoveoutwards. The rigid and massless links that connect the outer arms to the collar, in turn, try to lift the central collar (mass m/4) against the spring. The central collar can move along the vertical axis but the top of the governor remains ﬁxed. The mass of each ball is m = 5 kg, and the length of each link is l = 0.25 m. There are frictionless hinges at points A, B, C, D, E, F wherethelinksareconnected. Findtheamount the string is elongated, x, when the governor rotates at 100 rpm, given that the spring constant k = 500 N/m, and that in this steady state, θ = 90o. ∗

Fixed

m m m/4

θ θ

A B F C

E D

k

problem 8.36:

(Filename:summer95p2.2)

- 8.37 Crooked rod. A 2 long uniform rod of mass m is welded at its center to a shaft at an angle φ as shown. The shaft is supported by bearings at its ends and spins at a constant rate ω.


- a) What are H˙ O and L˙ ?
- b) Calculate H˙ /O using the integral deﬁnition of angular momentum. ∗
- c) What are the six reaction components if there is no gravity? ∗
- d) Repeatthecalculations,includinggravity g. Which reactions change and by how much? ∗


m = 1kg 1 = √2m

2d

8.41 A uniform narrow shaft of length 2L and mass 2M is bent at an angle θ half way down its length. It is spun at constant rate ω.

B

P

![image 105](Introduction to Statics and Dynamics Problems_images/imageFile105.png)

![image 106](Introduction to Statics and Dynamics Problems_images/imageFile106.png)

C

string A

- a) What is the magnitude of the force that must be applied at O to keep the shaft spinning?
- b) (harder) What is the magnitude of the moment that must be applied at O to keep the shaft spinning?


y

φ

45o

45o 45o

x

O

weld

x E

![image 107](Introduction to Statics and Dynamics Problems_images/imageFile107.png)

problem 8.37:

![image 108](Introduction to Statics and Dynamics Problems_images/imageFile108.png)

![image 109](Introduction to Statics and Dynamics Problems_images/imageFile109.png)

(Filename:h6.4)

O

![image 110](Introduction to Statics and Dynamics Problems_images/imageFile110.png)

1m

![image 111](Introduction to Statics and Dynamics Problems_images/imageFile111.png)

ω

![image 112](Introduction to Statics and Dynamics Problems_images/imageFile112.png)

D

y ω z

8.38Fortheconﬁgurationinproblem8.37, ﬁnd two positions along the rod where concentrating one-half the mass at each of these positions

L θ

problem 8.43: Uniform rod attached to a shaft.

L

A B

gives the same H˙ O.

(Filename:pg89.1)

problem 8.41: Spinning rod. No gravity.

- 8.39 Rod on a shaft. A uniform rod is welded to a shaft which is connected to frictionless bearings. The rod has mass m and length and is attached at an angle γ at its midpoint to the midpoint of the shaft. The length of the

shaft is 2d. A motor applies a torque Mmotor along the axis of the shaft. At the instant shown

in the ﬁgure, assume m, , d, ω and Mmotor are known and the rod lies in the yz-plane.

- a) Find the angular acceleration of the shaft.
- b) Themomentthattheshaftappliestothe rod.
- c) The reaction forces at the bearings.


motor

z

x

y

problem 8.39: Rod on a shaft.

(Filename:pg79.2)

- 8.40 Rod spins on a shaft. A uniform rod R with length R and mass m spins at constant rate ω about the z axis. It is held by a hinge at A and a string at B. Neglect gravity. Find the tension in the string in terms of ω, R and m. ∗


(Filename:f.4)

- 8.44 3D, crooked bar on shaft falls down. A massless, rigidshaftisconnectedtofrictionless

hinges at A and B. A bar with mass Mb and length is welded to the shaft at 45o. At time

t = 0 the assembly is tipped a small angle θ0 from the yz-plane but has no angular velocity. It then falls under the action of gravity. What is θ at t = t1 (assuming t1 is small enough so that θ1 is much less than 1)?

Looking down y-axis

A

B 45o

z

|z<br><br>x<br><br>![image 113](Introduction to Statics and Dynamics Problems_images/imageFile113.png)<br><br>![image 114](Introduction to Statics and Dynamics Problems_images/imageFile114.png)<br><br>θ|
|---|


y

x

g

problem 8.44: A crooked rod welded to a shaft falls down.

(Filename:p2.4)

8.3 Moment of inertia matrices: [Icm] and [IO]

- 8.45 Find the moment of inertia matrix [IO] of the system shown in the ﬁgure, given that m = 0.25kg and = 0.5m. Which components in the matrix [IO] will change if one mass is removed and the other one is doubled?


8.42Fortheconﬁgurationinproblem8.41, ﬁnd twopositionsalongthebentportionoftheshaft where concentrating one-half its mass at each

of these positions gives the same H˙ O and L˙ .

8.43 Rod attached to a shaft.√2m rod is attached to a shaft which spins atA uniform 1kg, a constant rate of 1rad/s. One end of the rod is connected to the shaft by a ball-and-socket joint . The other end is held by two strings (or pin jointed rods) that are connected to a rigid cross bar. The cross bar is welded to the main shaft. Ignore gravity.

- a) Draw a free body diagram of the rod AB, including a bit of the strings.
- b) Find the tension in the string DB. Two approaches:

- (i) Write the six equations of linear and angular momentum balance (about any point of your choosing) and solve them (perhaps using a computer) for the tension TDB.
- (ii) Write the equation of angular momentum balance about the axis AE. (That is, take the equation of angular momentum balance about point A and dot both sides with a vector in the direction of rE/A.) Use this calculation to ﬁnd TDB and compare to method ii.


- c) Find the reaction force (a vector) at A.


B

R

A string 45o

x

D

y ω z

problem 8.40:

(Filename:pﬁgure.s95f4)

y

m m

/2 /2

massless

O

x

problem 8.45:

(Filename:pﬁgure4.4.rp12)

- 8.46 A dumbbell (two masses connected by a massless rod of length ) lies in the xy plane. Compute the moments and products of inertia of this body about the x, y, and z axes. What are the principal axes of this body?

z x

y

θ

point mass, m

point mass, m 2

problem 8.46:

(Filename:pﬁgure.blue.38.2)

- 8.47 Equivalent dumbbell. It is a great fact that, for the purposes of dynamics, every rigid body can be replaced by a massless rigid structure holding six masses. The structure looks like a child’s jack. It has three orthogonal bars with three pairs of point masses along the bars. The center of the jack is at the center of mass. The bars are in the directions of the eigenvectors of the moment of inertia matrix of the body (the principal directions). For ﬂat objects one only needs four point masses. Where should one put four masses on a massless disk to make it equivalent to a uniform and ‘massful’ disk in problem 8.50(a). That is, what set of four masses has the same total mass, the same center of mass location, and the same moment of inertia matrix as a uniform disk?
- 8.48 Three identical solid spheres of mass m and radius r are situated at (b,0,0),(0,b,b), and (−b,0,2b) relative to the origin O. Find all nine components of [IO] of the system of three spheres.


Hint: [Icm] for each sphere is

######  

######  .

2 5mr2 0 0

0 25mr2 0 0 0 25mr2

Use the parallel axis theorem.

r,m

z

r,m

b b

y

b b b

O

r,m

x

problem 8.48:

(Filename:pﬁgure.blue.49.2)

- 8.49 Find the moment of inertia matrix [IO] for the ‘L’-shaped rod shown in the ﬁgure. The mass of the rod is m = 1.5kg and each leg is

= 0.4m long. You may ignore the width of the rod.

O x

y

m

problem 8.49:

(Filename:pﬁgure4.4.rp13)

- 8.50 Moment of Inertia Matrix. This problem concerns a uniform ﬂat disk of radius R0 with mass Md = Mdisc. In the two parts of this problem, you are to calculate the moment of inertia matrix for the disk. In the ﬁrst part, do it by direct integration and, in the second part, by using a change of basis.


- a) Using a coordinate system that is lined up with the disk so that the z axis is normal to the disk and the origin of the coordinate system is at the center of mass (the center) of the disk, calculate the moment of inertia matrix for the disk. [Hint: use polar coordinates, and use dm =

(M/π R2O)d A, and d A = R dR dθ.]

- b) Use a coordinate system x y z aligned as follows: the origin of the coordinate system is at the center of the disk, the z axis makes an angle φ with the z axis which is normal to the plane of the (measuredfromthez axistowardsthez axis), the disk intersects the x y plane along the y axis. The y axis and the y axis are coincident. Calculate the moment of inertia matrix for the disk. Alternate method: use the solution from (a) above with a change of basis.


x z'

φ φ

x'

z

G

uniform disk mass = Md, radius = Ro

y,y'

problem 8.50:

(Filename:f92h7p1)

- 8.51 For each of the shapes below, mark the approximate location of the center of mass and the principal axes about the center of mass

b

L

b

b

a

c

homogeneous sphere

homogeneous rectangular parallelapiped

massless rod holding two equal masses

capital "J"

problem 8.51:

(Filename:pﬁgure.blue.52.2)

- 8.52 Find the moment of inertia matrix [Icm] for the uniform solid cylinder of length and radius r shown in the ﬁgure.

r

O

y

z

x

problem 8.52:

(Filename:pﬁgure4.4.rp16)

- 8.53 An ‘L’-shaped structure consists of two thin uniform rectangular plates each of width w = 200mm. The vertical plate has height


y

- h = 400mm and the horizontal plate has depth d = 300mm. The plates are welded at right angles along the side measuring 200mm. The total mass of the structure is m = 0.7kg. Find the moment of inertia matrix [IO].


- a) [IG] =

8 0 0 0 16 0 0 0 8

kgm2, and

∗

- b) [IG] =


mass = m

![image 115](Introduction to Statics and Dynamics Problems_images/imageFile115.png)

![image 116](Introduction to Statics and Dynamics Problems_images/imageFile116.png)

8 0 0 0 16 −4 0 −4 8

L

kgm2. ∗

z

x

z

problem 8.61:

d

(Filename:pﬁgure.blue.99.1)

- 8.58 Find the z component of H = [IG] ω for ω = 2rad/skˆ and

[IG] =

10.20 −2.56 0 −2.56 10.20 0

0 0 14.00

lbmft2.

- 8.59 For ω = 5rad/sλˆ , ﬁnd λˆ such that the angle between ω and H = [IG] · ω is zero if

[IG] =

3 0 2 0 6 0 2 0 3

kgm2.

- 8.60 Calculation of HO and H˙ O. You will consider a disc spinning about various axes through the center of the disc O. For the most

part, you are concerned with calculating H˙ O. But, you should keep in mind that the purpose

of the calculation might be to calculate reaction forces and moments. Every point on the disk moves in circles about the same axis at the same number of radians per second. These problems can be done at least three different ways: using the[I]’s from problem 8.50, direct

integration of the deﬁnition of H˙ O, and using the equivalent dumbbell (with the deﬁnition of

H˙ O). You should do them all three ways, ﬁrst using the way you are most comfortable with.

- a) Assume that the conﬁguration is as in problem 8.50(a) and that the disk is spinning about the z axis at the constant rate of ωk. What are HO and H˙ O?
- b) Assume that the conﬁguration is as in problem 8.50(b) and that the disk is spinning about the z axis at the constant


rateofωk. Whatare HO and H˙ O? (In this problem there are two ways to use

[I]: one is in the xyz coordinate system, the other is in a coordinate system aligned nicely with the disk. )

- 8.61 What is the angular momentum H for:


- 8.62 A hoop is welded to a long rigid massless shaft which lies on a diameter of the hoop. The shaft is parallel to the x-axis. At the moment of interest the hoop is in the xy-plane of a coordinate system which has its origin O at the center of the hoop. The hoop spins about the x-axis at 1rad/s. There is no gravity.

- a) What is [IG] of the hoop?
- b) What is HO of the hoop?


x

y

z

O

problem 8.62:

(Filename:pﬁgure.blue.47.2)

- 8.63 Two thin rods, each of mass m and length d, are welded perpendicularly to an axle of mass M and length , which is supported by a ball-and-socket joint at A and a journal bearing

at B. A force F = −Fıˆ+Gkˆ acts at the point P as shown in the ﬁgure. Determine the initial angular acceleration α and initial reactions at point B.

z

x y

- A
- B


M P d

m

m

d

F

/4

/4

/2

α

problem 8.63:

(Filename:pﬁgure.blue.89.1)

- 8.64 Thethinsquareplateofmass M andsidec is mounted vertically on a vertical shaft which


h

O x

w

y

problem 8.53:

(Filename:pﬁgure4.4.rp14)

- 8.54 A solar panel consists of three rectangular plates each of mass m = 1.2kg, length = 1 and width w = 0.5m The two side panels are inclined at 30◦ with the plane of the middle panel. Evaluate all components of the moment of inertia matrix [IO] of the solar panel.

θ

θ

w

O

y x

z

problem 8.54:

(Filename:pﬁgure4.4.rp15)

8.4 Mechanics using [Icm] and [IO]

- 8.55 Find the angle between ω and H = [IG] ω, if ω = 3rad/skˆ and

[IG] =

20 0 0 0 20 0 0 0 40

kg·m2.

- 8.56 Find the projection of H = [IG] ω in the direction of ω, if ω = (2ıˆ − 3ˆ)rad/s and


a) A uniform sphere rotating with angular

5.4 0 0 0 5.4 0 0 0 10.8

velocity ω (radius R, mass m)?

[IG] =

lbmft2.

rotates with angular speed ω0. In the ﬁxed x, y, z coordinatesystemwithoriginatthecenter of mass (with which the plate is currently aligned) what are the vector components of ω?

b) A rod shown in the ﬁgure rotating about its center of mass with these angular velocities: ω = ωıˆ, ω = ωˆ, and ω = ω(ıˆ + ˆ)/

8.57Compute ω×([IG]· ω)for the following two cases. In each case ω = 2.5rad/sˆ.

√2?

What are the components of Hcm?

c

M

z

c

x

y

ω0

problem 8.64:

(Filename:pﬁgure.blue.35.2)

8.65 If you take any rigid body (with weight ), skeweritwithanaxle, holdtheaxlewithhinges that cause no moment about the axle, and hold it so that it cannot slide along the axle, it will swing like a pendulum. That is, it will obey the equations:

θ¨ = −C sinθ, or (a) φ¨ = +C sinφ, (b)

where

θ istheamountofrotationabouttheaxismeasuring zero when the center of mass is directly below the z -axis; i. e., when the center of mass is in a plane containing the z -axis and the gravity vector,

φ istheamountofrotationabouttheaxismeasuring zero when the center of mass is directly above the z -axis,

C= Mtotal gd sinγ/Iz z , Mtotal is the total mass of the body, g is the gravitational constant, d is the perpendicular distance from the axis

to the center of mass of the object,

γ is the angle of tip of the axis from the ver-

tical, Iz z is the moment of inertia of the object about the skewer axis.

- a) How many examples of such pendula can you think of and what would be the values of the constants? (e.g. a simple pendulum?, a broom upside down on your hand?, a door?, a box tipping on one edge?, a bicycler stopped at a red light and stuck in her new toe clips?, a person who got rigor mortis and whose ankles went totally limp at the same time?,...)
- b) A door with frictionless hinges is misaligned by half an inch (the top hinge is half an inch away from the vertical line above the other hinge). Estimate the period with which it will swing back and forth. Use reasonable magnitudes of any quantities you need.


c) Can you verify the formula (a simple pendulum and a swinging stick are special cases)?

z'

y γ y' γ

z

d x,x'

| | |
|---|---|
| | |


θ g

Side View

y y'

γ γ

z'

d

| | |
|---|---|
| | |


z

problem 8.65: 3-D pendulum on a hinge.

(Filename:pﬁgure4.3Dpend)

8.66 A hanging rod going in circles. A uniform rod with length and mass m hangs from a well greased ball and socket joint at O. It swingsincirclesatconstantrate ω = ωkwhile the rod makes an angle φ with the vertical (so it sweeps a cone).

- a) Calculate HO and H˙ O.
- b) Using H˙ O andangularmomentumbalance, ﬁnd the rotation rate ω in terms of φ, g, , and m. How long does it take to make one revolution? ∗
- c) If another stick rotates twice as fast while making the same angle φ, what must be its length compared to ?
- d) Is there a simple way to describe what two uniform sticks of different length and different cone angle φ both have in common if their rate of rotation ω is the same? (Ifyouaccuratelydrawtwosuch sticks, you should see the relation.)
- e) Find the reaction force at the ball and socket joint. Is this force parallel to the stick?


O

ball & socket joint

φ

kˆ

| | |
|---|---|
| | |


m

ˆ

ω

ıˆ

problem 8.66:

(Filename:pﬁgure.s94h6p3)

- 8.67 From discrete to continuous. n equal beads of mass m/n each are glued to a rigid massless rod at equal distances l = L/n from each other. For n = 4, the system is shown in the ﬁgure, but you are to consider the general problemwithn masses. Therodswingsaround the vertical axis maintaining angle φ.

- a) Find the rate of rotation of the system as a function of g, L, n, and φ for constant rate circular motion. [Hint: You may need these series sums: 1 + 2 + 3 + ··· + n = n(n2+1) and 12 + 22 + 32 + ··· + n2 = n(n+1)(62n+1).] ∗

- b) Set n = 1 in the expression derived in (a) and check the value with the rate of rotation of a conical pendulum of mass m and length .
- c) Now, put n → ∞ in the expression obtained in part (a). Does this rate of rotation make sense to you? [Hint: How does it compare with the rate of rotation for the uniform stick of Problem 8.66?]


m/4

m/4

m/4

m/4

A

ω

/4

φ

ıˆ

ˆ

kˆ

problem 8.67:

(Filename:pﬁgure.s94h6p4)

- 8.68 Spinning dumbbell. Two point masses are connected by a rigid rod of negligible mass and length 2√2L. The rod is welded to a shaft that is along the y axis. The shaft is spinning at a constant rate ω driven by a motor at A (Not shown). At the time of interest the dumbbell is in the yz-plane. Neglect gravity.


- a) What is the moment of inertia matrix about point O for the dumbbell at the instant shown? ∗
- b) What is the angular momentum of the dumbbell at the instant shown about point O. ∗
- c) What is the rate of change of angular momentum of the dumbbell at the instant shown? Calculate the rate of change of angular momentum two different ways:


- (i) by adding up the contribution of both of the masses to the rate of change of angular momentum (i.e. H˙ = ri ×(mi ai)) and
- (ii) by calculating Ixy and Iyz, calculating H, and then calculating H˙ from ω × H. ∗


###### kˆ

d) What is the total force and moment (at the CM of the dumbbell) required to keep this motion going? Do the calculation in the following ways:

Z

z

b/2

ıˆ

b/2

ω

C

G O

- (i) Using angular momentum balance (about any point of your choice) for the shaft dumbbell system.
- (ii) By drawing free body diagrams of the masses alone and calculating the forces on the masses. Then use action and reaction and draw a free body diagram of the remaining (massless) part of the shaft-dumbbell system. Then use moment balance for this system. ∗


Y

β

problem 8.71:

ω

h/2 h/2

(Filename:pﬁgure4.rpi)

x

X

y

OXYZ - Fixed Frame

- 8.72 A thin triangular plate of base b, height h, and mass m is attached to a massless shaft whichpassesthroughthebearingsLandR.The plate is initially vertical and then, provoked by a teensy disturbance, falls , pivoting around the shaft. The bearings are frictionless. Given,

rcm = (0,

2 3

b,

1 3

h),

IxxO =

m 2

(b2 + h2/3),

IyyO = mh2/6, IzzO = mb2/2, Iyycm = mh2/18,

IzyO = −mbh/4,

- a) what is the plate’s angular velocity as it passes through the downward vertical position?
- b) Compute the bearing reactions when the plate swings through the downward vertical position.


R

L

O

b

h

x

z

y

g

problem 8.72:

(Filename:pﬁgure.blue.86.1)

- 8.73 A welded structural tubing framework is proposedtosupportaheavyemergencysearchlight. To select properly the tubing dimensions it is necessary to know the forces and moments at the critical section AA, when the framework is moving. The frame moves as shown.


(base vectors, ıˆ,ˆ,kˆ)

Gxyz - Moving "Body" Frame

(base vectors, eˆx,eˆy,eˆz)

problem 8.69:

m

ω

(Filename:pﬁgure.blue.36.1)

z y

45o weld

- 8.70 A uniform rectangular plate spins about a

ﬁxed axis. The constant torque My is applied about the Y axis. The plate is held by bearings at the corners of the plate at A and B. At the instant shown the plate and the y z axis attached to the plate are in the Y Z plane. Neglect gravity. At t = 0 the plate is at rest.

- a) Att = 0+ (i.e.,justafterthestart),what is the acceleration of point D? Give your answer in terms of any or all of

c,d,m, My,ıˆ,ˆ, and kˆ (the base vectors aligned with the ﬁxed XY Z axes),

and IYYcm

[You may use IYYcm in your answer. Or you could use this result from the

change of coordinates formulae in linear algebra: IYYcm = (cos2 β)Iycm y + (sin2 β)Izcm z to get an answer in terms of c, d, m, and My.]

∗

- b) At t = 0+, what is the reaction at B? ∗ plate mass = m


A O B

D c

d

d

c

Z

z'

X x' y'

Y My

β

problem 8.70:

(Filename:pﬁgure.s95q8)

- 8.71 A uniform semi-circular disk of radius r = 0.2m and mass m = 1.5kg is attached to a shaft along its straight edge. The shaft is tipped very slightly from a vertical upright position. Find the dynamic reactions on the bearings supporting the shaft when the disk is in the vertical plane (xz) and below the shaft.


O

m

x

Looking down x-axis

![image 117](Introduction to Statics and Dynamics Problems_images/imageFile117.png)

z

45o

![image 118](Introduction to Statics and Dynamics Problems_images/imageFile118.png)

y

A B

problem 8.68: Crooked spinning dumbbell.

(Filename:pg84.3)

8.69 A uniform rectangular plate of mass m, height h, and width b spins about its diagonal at a constant angular speed ω, as shown in the ﬁgure. The plate is supported by frictionless bearings at O and C. The plate lies in the Y Zplane at the instant shown.

(Note: cos(β) = b/ (h2 + b2),sin(β) = h/ (h2 + b2)

- a) Compute the angular momentum of the plate about G (with respect to the body axis Gxyz shown).
- b) Ignoring gravity determine the net torque (moment) that the supports impose on the body at the instant shown. (Express your solution using base vectors and components associated with the inertial XY Z frame.)
- c) Calculate the reactions at O or C for the conﬁguration shown. ∗
- d) In the case when h = b = 1m what is the vertical reaction at C (still neglecting gravity).


a) Determine the magnitude and direction of the dynamic moments (bending and twisting) and forces (axial and shear) at sectionAAoftheframeif, attheinstant shown, the frame has angular velocity ωo and angular acceleration αo. Assume that the mass per unit length of the pipe is ρ.

L

L

A A

L

ω0 α0

###### problem 8.73:

(Filename:pﬁgure.blue.88.1)

- 8.74 A uniform cube with side 0.25m is glued to a pipe along the diagonal of one of its faces ABCD. The pipe rotates about the y-axis at a constant rate ω = 30rpm. At the instant of interest, the face ABCD is in the xy-plane.

- a) Find the velocity and acceleration of point F on the cube.
- b) Find the position of the center of mass ofthecubeandcomputeitsacceleration acm.
- c) Supposethattheentiremassofthecube is concentrated at its center of mass. What is the angular momentum of the cube about point A?


E

B

F

G

H

C

A D

z

x

ω y

problem 8.74:

(Filename:pﬁgure4.2.rp3)

- 8.75 A uniform square plate of mass m and side length b is welded to a narrow shaft at one corner. The shaft is perpendicular to the plate and has length . The upper end of the shaft is connected to a ball and socket joint at O. The assembly is rotating about the z axis through


O at the ﬁxed rate ω = ωkˆ which happens to be just right to make the plate horizontal and the shaft vertical, as shown. The gravitational constant is g.

- a) What is ω in terms of m, , b, and g?
- b) Is the reaction at O on the rod-plate assembly in the direction of the line from G to O? (Why?)


O

kˆ

ˆ

ıˆ

b

G

b

problem 8.75:

(Filename:pﬁgure.s94q6p1)

- 8.76 A spinning box. A solid box B with dimensions a, a, and 2a (where a = .1m) and mass=1kg. Itissupportedwithballandsocket joints at opposite diagonal corners at A and B. It is spinning at constant rate of (50/π)rev/sec and at the instant of interest is aligned with the ﬁxed axis ıˆ,ˆ, and kˆ. Neglect gravity.

- a) What is ωB?
- b) What is ω˙ B?
- c) What is HB/cm?
- d) What is H˙ B/cm?
- e) What is r B/A × F B (where F B is the reaction force on B at B)? A dimensional vector is desired.
- f) If the hinges were suddenly cut off when B was in the conﬁguration


shown, what would be ω˙ B immediately afterwards?

A

B a

a

2a a = 0.1m

ıˆ

ˆ

kˆ

problem 8.76:

(Filename:pﬁgure.s94f1p2)

- 8.77 Uniform rod attached to a shaft. A uniform1kg, √2mrodisattachedtoashaftwhich spins at a constant rate of 1rad/s. One end of the rod is connected to the shaft by a balland-socket joint. The other end is held by two strings (or pin jointed rods) that are connected to a rigid cross bar. The cross bar is welded to the main shaft. Ignore gravity. Find the reaction force at A.


m = 1kg l = 2 m

###### string

B

C

A

45

o

o

45

o

45

E

x

1m

###### z

D

y

###### problem 8.77:

(Filename:s97f2)

- 8.78Arounddiskspinscrookedlyonashaft. A thin homogeneous disk of mass m and radius r is welded to the horizontal axle AB. The normal to the plane of the disk forms an angle β with the axle. The shaft rotates at the constant rate ω.

- a) What is the x component of the angular momentum of the disk about point G the center of mass of the disk?
- b) What is the x component of the rate of change of angular momentum of the disk about G?
- c) At the given instant, what is the total force and moment (about G) required to keep the disk spinning at constant rate?


A

B

uniform disk of mass = m radius = r

x

y

ω z

nˆ

tˆ

G β

problem 8.78: A round disk spins crookedly on a shaft.

(Filename:pg92.2)

- 8.79 A uniform disk of mass m = 2kg and radius r = 0.2m is mounted rigidly on a massless axle. The normal to the disk makes an angle β = 60o with the axle. The axle rotates at a constant rate ω = 60rpm. At the instant shown in the ﬁgure,


- a) Find the angular momentum HO of the disk about point O. ∗
- b) Draw the angular momentum vector indicating its magnitude and direction. ∗
- c) As the disk rotates (with the axle), the angular momentum vector changes. Does it change in magnitude or direction, or both? ∗


- 8.85 Three equal length (1m) massless bars are welded to the rigid shaft AB which spins at constant rate ω = ωıˆ. Three equal masses (1kg) are attached to the ends of the bars. At the moment of interest the masses are all in the xy plane as shown. Where should what masses be added to make the system shown dynamically balanced? [The solution is not unique.]

120o

120o

120o 15o

Length of bars is 1 m Each mass is 1 kg

A

E

D

C

O

B

ıˆ

ˆ

problem 8.85:

(Filename:pﬁgure.s94q7p1)

- 8.86 Dynamic balance of a system of particles. Three masses are mounted on a massless shaft AC with the help of massless rigid rods.


- a) Whatisthetensioninthewire? Answer in terms of some or all of R,m,φ and ω.
- b) What is the reaction force at the hinge at O?


d) Find the direction of the net torque on the system at the instant shown. Note, only the direction is asked for. You can answer this question based on parts (b) and (c). ∗

x

z z'

uniform disk of mass = m radius = r

tˆ

φ

ω

nˆ = kˆ

A

y'

B

A

φ

β

O

y

y

R

B

ω z

x

n ˆ

x

β

z

problem 8.81:

O Front View (xz-plane)

(Filename:s97p3.3)

- 8.82 A disoriented disk rotating with a shaft. A uniform thin circular disk with mass m = 2kg and radius R = 0.25m is mounted on a massless shaft as shown in the ﬁgure. The shaft spins at a constant speed ω = 3rad/s. At the instant shown, the disk is slanted at 30◦ with the xy-plane. Ignore gravity.

- a) Find the rate of change of angular momentum of the disk about its center of mass. ∗
- b) Find the rate of change of angular momentum about point A. ∗
- c) Find the total force and moment required at the supports to keep the motion going. ∗


motor

A

B

D

C

R=0.25 m m=2 kg

![image 119](Introduction to Statics and Dynamics Problems_images/imageFile119.png)

![image 120](Introduction to Statics and Dynamics Problems_images/imageFile120.png)

![image 121](Introduction to Statics and Dynamics Problems_images/imageFile121.png)

![image 122](Introduction to Statics and Dynamics Problems_images/imageFile122.png)

![image 123](Introduction to Statics and Dynamics Problems_images/imageFile123.png)

![image 124](Introduction to Statics and Dynamics Problems_images/imageFile124.png)

ω

1m 0.5m

30o

1m

ıˆ 1m ˆ kˆ

problem 8.82:

(Filename:pﬁgure.s94h8p1)

8.5 Dynamic balance

- 8.83 Is ω = (2ıˆ +5kˆ)rad/s an eigenvector of

[IG] =

8 0 0 0 16 −4 0 −4 8

kgm2?

- 8.84 Find the eigenvalues and eigenvectors of


problem 8.79:

(Filename:summer95p2.3)

Mass m1 = 1kg and mass m2 = 1.5kg. The shaft rotates with a constant angular velocity

- 8.80 A uniform disk spins at constant angular velocity. The uniform disk of mass m and radius r spins about the z axis at the constant rate ω. Its normal nˆ is inclined from the z axis by the angle β and is in the xz plane at the moment of interest. What is the total force and moment (relative to O) needed to keep this disk spinning at this rate? Answer in terms of m, r, ω, β and any base vectors you need.

A

B

uniform disk of mass = m radius = r

x

y

ω z

tˆ

β

β

O

O Front View (xz-plane)

nˆ = kˆ

n ˆ

z

x

problem 8.80:

(Filename:p.f96.p3.3)

- 8.81 Spinning crooked disk. A rigid uniform disk of mass m and radius R is mounted to a shaft with a hinge. An apparatus not shown keeps the shaft rotating around the z axis at a constant ω. At the instant shown the hinge axis is in the x direction. A massless wire, perpendicular to the shaft, from the shaft at A to the edge of the disk at B keeps the normal to the plate (the z direction) at an angle φ with the shaft.


ω = 5rad/skˆ. At the instant shown, the three masses are in the xz-plane. Assume frictionless bearings and ignore gravity.

- a) Find the net reaction force (the total of alltheforces)ontheshaft. Isthesystem statically balanced?
- b) Find the rate of change of angular momentum H˙ /A, using H˙ /A =

i ri/A × mi ai.

- c) Find the angular momentum about

point A, H/A. Use this intermediate result to ﬁnd the rate of change of an-

gular momentum H˙ /A, using H˙ /A = ω× H/A and verify the result obtained in (b).

- d) What is the value of the resultant unbalanced torque on the shaft? Propose a design to balance the system by adding an appropriate mass in an appropriate location.


![image 125](Introduction to Statics and Dynamics Problems_images/imageFile125.png)

motor

.05m

![image 126](Introduction to Statics and Dynamics Problems_images/imageFile126.png)

![image 127](Introduction to Statics and Dynamics Problems_images/imageFile127.png)

D

![image 128](Introduction to Statics and Dynamics Problems_images/imageFile128.png)

A

![image 129](Introduction to Statics and Dynamics Problems_images/imageFile129.png)

![image 130](Introduction to Statics and Dynamics Problems_images/imageFile130.png)

![image 131](Introduction to Statics and Dynamics Problems_images/imageFile131.png)

![image 132](Introduction to Statics and Dynamics Problems_images/imageFile132.png)

m1 m1

![image 133](Introduction to Statics and Dynamics Problems_images/imageFile133.png)

![image 134](Introduction to Statics and Dynamics Problems_images/imageFile134.png)

B

0.2m

.05m

C

.05m

0.1m

![image 135](Introduction to Statics and Dynamics Problems_images/imageFile135.png)

![image 136](Introduction to Statics and Dynamics Problems_images/imageFile136.png)

ıˆ m2 ˆ kˆ

0.1m

.05m

5 0 0 0 5 −3 0 −3 10

[IG] =

kgm2.

problem 8.86:

(Filename:pﬁgure.s94h7p2)

- 8.87 For what orientation of the rod φ is the system shown dynamically balanced?

![image 137](Introduction to Statics and Dynamics Problems_images/imageFile137.png)

![image 138](Introduction to Statics and Dynamics Problems_images/imageFile138.png)

O

weld

1.0 m

Q

P

0.5 m

0.25 m 0.5 m

φ

x

y

problem 8.87:

(Filename:ch4.7.c)

- 8.88 A uniform square plate with 1m sides and 1kg mass is mounted (as shown) with a shaft that is in the plane of the square but not parallel to the sides. What is the net force and moment required to maintain rotation at a constant rate?

30o

30o

side view end view

ω

problem 8.88:

(Filename:pﬁgure.blue.87d.1)

- 8.89 An equilateral uniform triangular plate withsidesoflength platespinsatconstantrate ω about an axis through its center of mass. The axis is coplanar with the triangle. The angle φ is arbitrary. When φ = 0◦, the base of the triangle is parallel to the axis of rotation. Find the net force and moment required to maintain rotation of the plate at a constant rate for any φ. For what angle φ is the plate dynamically balanced?


A

B

φ

ω

Side View

A B

φ

problem 8.89:

(Filename:Mikef91p3)

- 8.90 An abstract problem. This problem concerns a system rigidly attached to a massless rod spinning about a ﬁxed axis at a ﬁxed rate. That is, whether or not the system is a rigid body, it is moving as if it were a rigid body. Every point in the system is moving in circles about the same axis at the same number of radians per second. The position of a particle of the system relative to the axis is R. The po-

sition relative to some point C is rC. In all cases, the body rotates about the axis shown.

The total mass of all the objects is Mtot. Point O is at the center of mass of the system and is at a distance d from the rotation axis and is on the x-axis at the moment of interest. Assume there is no gravity. At the point A, the rod is free to slide in the z-direction. But, at point B, the rod is constrained from moving in the z-direction. TheFBDofthesystemisshown in the ﬁgure. Referring to the free body diagram, there are six scalar unknown reactions in this 3 dimensional problem.

- a) The general case: Imagine that you know H˙ O = H˙0xıˆ + H˙0yˆ + H˙0zkˆ

and also L˙ = L˙xıˆ+L˙yˆ+L˙zkˆ. How would you ﬁnd the six unknown reac-

tions Ax, Ay, MAz, Bx, By, Bz? [Reduce the problem to one of solving six equations in six unknowns.]

- b) TheGeneralResult: Is MAz necessarily equal to zero? Prove your result or ﬁnd a counter-example. ∗
- c) Static Balance:. If d = 0 is it true thatallreactionforcesareequaltozero? Prove your result or ﬁnd a counter example. ∗


1m

1m

Bz Bx

Ax

Ay

d

x

y

Mz

By ω

problem 8.90:

(Filename:pﬁgure.s94h7p3)

- 8.91 A uniform block spins at constant angular velocity. The magnitude of the angular velocity is ω. The center of mass G is on the


axis of rotation. The ıˆ, ˆ, and kˆ directions are parallel to the sides with lengthes b, c and d, respectively. Answer in terms of some or all of ω, m, b, c, d, ıˆ, ˆ, and kˆ.

- a) Find vH.
- b) Find aH.
- c) What is the sum of all the moments about point G of all the reaction forces at A and B?


d) Are there any values of b, c, and d for which this block is dynamically balancedforrotationaboutanaxisthrough a pair of corners? Why?

c

d

b H

ıˆ

kˆ ˆ

problem 8.91:

(Filename:p.f96.p2.3)

8.92 Dynamic Balance. Consider each of the objects shown in turn (so to speak), each spinning about the z axis which is horizontal. In each case the center of mass is half way between the bearings (not shown). Gravity is in the −ˆ direction. State whether it is possible to spin the object at constant rate with constant bearing reactions of mgˆ/2 and no other applied torques (‘yes’) or might not be (‘no’). Give a brief explanation of your answer (enough to distinguish an informed answer from a guess).

- a) Axis along centerline of a uniform rectangular plate.
- b) Axis orthogonal to uniform rectangular plate and through its centroid.
- c) Axis orthogonal to uniform rectangular plate and not through its centroid.
- d) Axis orthogonal to uniform but totally irregular shaped plate and through its centroid.
- e) Axis along the diagonal of a uniform rhombus.
- f) Axis through the center of a uniform sphere.
- g) Axis through the diagonal of a uniform cube.
- h) Axis with two equal masses attached as shown.
- i) Axis with three equal masses attached as shown, all in a common plane with the axis, with φ not equal to 30◦.
- j) An arbitrary rigid body which has center of mass on the axis and two of its moment-of-inertia eigenvectors perpendicular to the axis. (no picture)


θ

| | | |
|---|---|---|
| | | |


(a)

![image 139](Introduction to Statics and Dynamics Problems_images/imageFile139.png)

ω

| | |
|---|---|
| | |


![image 140](Introduction to Statics and Dynamics Problems_images/imageFile140.png)

(b)

problem 8.93:

(c)

(Filename:pﬁgure.s94h7p5)

(d)

| | |
|---|---|
| | |


(e)

(f)

(g)

m R

(h)

R

m

120o

(i)

120o φ

###### problem 8.92:

(Filename:s97p3.2)

- 8.93 Dynamic tire balancing. Where should you place what weights in order to dynamically balance the tire?


Assume that a car tire can be modeled as a uniform disk of radius one foot and mass 20lbm. Assume the tire has been mounted crooked by one degree (the plane of the disk makes an 89◦ angle with the car axle). This crooked wheel is statically balanced since its center of mass is on the axis of rotation. But it isdynamicallyunbalancedsinceitwobblesand willwobblethecar. Carshopsputlittleweights on unbalanced wheels to balance them. They ﬁgure out where to put the weights by using

- a little machine that measures the wheel wobble. But you don’t need such a machine for this problem because you have been told where all the mass is located.


There are many approaches to solving this problem and there are also many correct solutions. You should ﬁnd any correct solution. [oneapproach: guessagoodlocationtoputtwo masses and then ﬁgure out how big they have to be to make the tire dynamically balanced.]

General planar motion of particles and rigid bodies

##### 9.1 Kinematics of planarrigid-body motion

- 9.1 A particle moves along the two paths (1) and (2) as shown.

- a) In each case, determine the velocity of the particle in terms of b, θ, and θ˙. ∗
- b) Find the x and y coordinates of the path as functions of b and r or b and θ. ∗


0 5 10 15

-5

0

5 r θ1/2 = b

θ = br

y

x

x

y

- (1)
- (2)


-5 0 5

- -4

- -2


0

2

4

problem 9.1:

(Filename:polarplot0)

- 9.2 For the particle path (1) in problem 9.1, ﬁnd the acceleration of the particle in terms of b, θ, and θ˙.
- 9.3 For the particle path (2) in in problem 9.1, ﬁnd the acceleration of the particle in terms of

b, θ, and θ˙.

- 9.4 A body moves with constant velocity V in a straight line parallel to and at a distance d from the x-axis.


- a) Calculate θ˙ in terms of V,d, and θ.
- b) Calculate the eˆθ component of acceleration.


Carefully deﬁne, using a sketch and/or words, any variables, coordinate systems, and reference frames you use. Express your answers using any convenient coordinate system (just make sure its orientation has been clearly deﬁned).

###### v

d θ

x

problem 9.4:

(Filename:pﬁgure.blue.62.1)

- 9.5 The slender rod AB rests against the step of height h, while end “A” is moved along the ground at a constant velocity vo. Find φ˙ and φ¨ in terms of x, h, and vo. Is φ˙ positive or negative? Is φ¨ positive or negative?

A

B

h

x

φ vo

problem 9.5:

(Filename:pﬁgure.blue.98.1)

- 9.6 A ten foot ladder is leaning between a ﬂoor and a wall. The top of the ladder is sliding down the wall at one foot per second. (The foot is simultaneously sliding out on the ﬂoor). When the ladder makes a 45 degree angle with the vertical what is the speed of the midpoint of the ladder?
- 9.7 A stone in a wheel. A round wheel rolls to the right. At time t = 0 it picks up a stone the road. The stone is stuck in the edge of the wheel. You want to know the direction of the rock’s motion just before and after it next hits the ground. Here are some candidate answers:


- • When the stone approaches the ground its motion is tangent to the ground.
- • The stone approaches the ground at angle x (you name it).
- • When the stone approaches the ground its motion is perpendicular to the ground.
- • Thestoneapproachesthegroundatvarious angles depending on the following conditions(...you list the conditions.)


Although you could address this question analytically, you are to try to get a clear answer by looking at computer generated plots. In particular, you are to plot the pebble’s path for a small interval of time near when the stone next touches the ground. You should pick the parameters that make your case for an answer the strongest. You may make more than one plot.

###### Here are some steps to follow:

- a) Assuming the wheel has radius Rw and the pebble is a distance Rp from the center (not necessarily equal to Rw). The pebble is directly below the center of the wheel at time t = 0. The wheel spins at constant clockwise rate ω. The x-axis is on the ground and x(t = 0) = 0. The wheel rolls without slipping. Using a clear well labeled drawing (use a compass and ruler or a computer drawing program), show that

x(t) = ωt Rw − Rp sin(ωt) y(t) = Rw − Rp cos(ωt)

- b) Using this relation, write a program to make a plot of the path of the pebble

- as the wheel makes a little more than one revolution. Also show the outline of the wheel and the pebble itself
- at some intermediate time of interest. [Use any software and computer that pleases you.]


- c) Change whatever you need to change to make a good plot of the pebble’s path for a small amount of time as the pebble approaches and leaves the road. Also show the wheel and the pebble at some time in this interval.
- d) In this conﬁguration the pebble moves a very small distance in a small time so your axes need to be scaled. But make sure your x- and y- axes have the same scale so that the path of the pebble and the outline of the wheel will not be distorted.
- e) How does your computer output buttress your claim that the pebble approaches and leaves the ground at the angles you claim?
- f) Think of something about the pebble in the wheel that was not explicitly asked in this problem and explain it using the computer, and/or hand calculation and/or a drawing.


9.8Auniformdiskofradiusr rollsataconstant rate without slip. A small ball of mass m is attached to the outside edge of the disk. What is the force required to hold the disk in place when the mass is above the center of the disk?

- 9.9 Rolling at constant rate. See also problem 9.39. A round disk rolls on the ground at constant rate. It rolls 114 revolutions over the time of interest.

- a) Particle paths. Accurately plot the paths of three points: the center of the disk C, a point on the outer edge that is initially on the ground, and a point that is initially half way between the former two points. [Hint: Write a parametric equation for the position of the points.

First ﬁnd a relation between ω and vC. Then note that the position of a point is the position of the center plus the position of the point relative to the center.] Draw the paths on the computer, make sure x and y scales are the same (In MATLAB, use the axis(’equal’) command for the same scaling).

- b) Velocity of points. Find the velocity of the points at a few instants in the motion: after 14, 12, 34, and 1 revolution. Draw the velocity vector (by hand) on your plot. Draw the direction accurately and draw the lengths of the vectors in proportion to their magnitude. You can ﬁnd the velocity by differentiating the position vector or by using relative motion formulas appropriately. Draw the disk at its position after one quarter revolution. Note that the velocity of the points is perpendicular to the line connecting the points to the ground contact.

- c) Acceleration of points. Do the same as above but for acceleration. Note that the acceleration of the points is parallel to the line connecting the points to the center of the disk.


C

P

| | |
|---|---|
| | |


problem 9.9:

(Filename:pﬁgure.s94h11p2)

- 9.10 The concentric wheels are welded to each other and roll without slip on the rack and stationary support. The rack moves to the right at

vr = 1m/s. What is the velocity of point A in the middle of the wheels shown?

stationary support

concentric wheels

no slip rack

2 cm 2 cm

A

vr

problem 9.10:

(Filename:pﬁgure.blue.118.1)

- 9.11 Questions (a) - (e) refer to the cylinders in the conﬁguration shown ﬁgure. Question (f) is closely related. Answer the questions in terms


of the given quantities (and any other quantities you deﬁne if needed).

the velocities of the two ends of the rod are vA = −1m/sıˆ and vB = 1m/sˆ.

- a) What is the speed (magnitude of velocity) of point c?
- b) What is the speed of point P?
- c) What is the magnitude of the acceleration of point c?
- d) What is the magnitude of the acceleration of point P?
- e) What is the radius of curvature of the path of the particle P at the point of interest?
- f) In the special case of A = 2b what is the curve which particle P traces (for all time)? Sketch the path.


- a) Find the angular velocity of the rod.
- b) Find the center of rotation of the rod. A


![image 141](Introduction to Statics and Dynamics Problems_images/imageFile141.png)

![image 142](Introduction to Statics and Dynamics Problems_images/imageFile142.png)

= 1.0 m

###### ˆ

θ = 45o

ıˆ

B

###### problem 9.13:

(Filename:pﬁgure4.3.rp6)

- 9.14 A square plate ABCD rotates at a constant angular speed about an unknown point in its plane. At the instant shown, the velocities of the two corner points A and D are

vA = −2ft/s(ıˆ + ˆ) and vD = −(2ft/s)ıˆ, respectively.

- a) Find the center of rotation of the plate.
- b) Find the acceleration of the center of mass of the plate.


G

C

- A D
- B ıˆ


| | |
|---|---|
| | |


ˆ

problem 9.14:

(Filename:pﬁgure4.3.rp7)

- 9.15 Consider the motion of a rigid ladder which can slide on a wall and on the ﬂoor as shown in the ﬁgure. The point A on the ladder moves parallel to the wall. The point B moves parallel to the ﬂoor. Yet, at a given instant, both have velocities that are consistent with the ladderrotatingaboutsomespecialpoint,thecenter of rotation (COR). Deﬁne appropriate dimensions for the problem.


ω

O A

P b

c

problem9.11: Alittlecylinder(withouter radiusb andcenteratpointc)rollswithoutslipping inside a bigger ﬁxed cylinder (with inner radius A and center at point O). The absolute angular velocity of the little cylinder ω is constant. P is attached to the outside edge of the little cylinder. At the instant of interest, P is on the line between O and c.

(Filename:pﬁgure.blue.50.1)

- 9.12 See also problems 10.31, 10.35, and

11.28. Arm OC rotates with constant rate ω1. Disc D of radiusr rotates about point C at con-

stant rate ω2 measured with respect to the arm OC. What are the absolute velocity and accel-

erationofpoint P onthedisc, vP and aP? (To do this problem will require deﬁning a moving frame of reference. More than one choice is possible.) ∗

- a) Pickasuitablemovingframeanddothe problem.
- b) Pickanothersuitablemovingframeand redo the problem. Make sure the answers are the same.


C

O

r

disk D

P

L

θ

ω1

ω2

problem 9.12:

(Filename:Mikes93p1)

- 9.13 Auniformrigidrod AB oflength = 1m rotates at a constant angular speed ω about an unknown ﬁxed point. At the instant shown,


- a) Find the COR for the ladder when it is at some given position (and moving, of course). Hint, if a point is A is ‘going in circles’ about another point C, that other point C must be in the direction perpendicular to the motion of A.
- b) As the ladder moves, the COR changes with time. What is the set of points on the plane that are the COR’s for the ladderasitfallsfromstraightuptolying on the ﬂoor?


A

ladder

wall

B

floor

problem 9.15:

(Filename:pﬁgure.blue.96.1)

- 9.16 A car driver on a very boring highway is carefully monitoring her speed. Over a one hour period, the car travels on a curve with constant radius of curvature, ρ = 25mi, and its speed increases uniformly from 50mph to 60mph. What is the acceleration of the of the car half-way through this one hour period, in path coordinates?
- 9.17 Find expressions for eˆt, at, an, eˆn, and the radius of curvature ρ, at any position (or time) on the given particle paths for

- a) problem 5.81, ∗
- b) problem 5.83,
- c) problem 10.5,
- d) problem 5.85,
- e) problem 5.84, and
- f) problem 5.82.


- 9.18 A particle travels at non-constant speed on an elliptical path given by y2 = b2(1 −

- x2 a2 ). Carefully sketch the ellipse for particular values of a and b. For various positions of the particle on the path, sketch the position vector r(t); the polar coordinate basis vectors eˆr and eˆθ; and the path coordinate basis vectors eˆn and eˆt. At what points on the path are eˆr and eˆn parallel(or eˆθ and eˆt parallel)?


9.2 Unconstrained Dynamics of 2-D rigid-body planar motion

- 9.19 A uniform disc of mass m and radius r rotates with angular velocity ωkˆ. Its center of mass translates with velocity v = x˙ıˆ + y˙ˆ in the xy-plane. What is the total kinetic energy of the disk?
- 9.20 The uniform rectangle of width a = 1m, length b = 2m, and mass m = 1kg in the ﬁgure is sliding on the x − y plane with no friction. At the moment in question, point C is at xC = 3m and yC = 2m. The linear momentum is L = 4ıˆ + 3ˆ (kg·m/s) and the angular momentum about the center of mass


is Hcm = 5kˆ(kg·m/s2). Find the acceleration of any point on the body that you choose. (Mark it.) [Hint: You have been given some useless information.]

y

no applied forces

x

C

a b

30o

problem 9.20:

(Filename:pﬁgure.blue.101.1)

- 9.21 TheverticalpoleABofmassm andlength is initially, at rest on a frictionless surface. A

tension T is suddenly applied at A. What is

- x¨cm? What is θ¨AB? What is x¨B? Gravity may be ignored.

T

m

B

A x

- y


problem 9.21:

(Filename:pﬁgure.blue.95.1)

- 9.22 Force on a stick in space. 2-D . No gravity. A uniform thin stick with length and mass m is, at the instant of interest, parallel to the y axis and has no velocity and no angular velocity. The force F = Fıˆ with F > 0 is suddenly applied at point A. The questions below concern the instant after the force F is applied.


- a) What is the acceleration of point C, the center of mass? ∗
- b) What is the angular acceleration of the stick? ∗
- c) What is the acceleration of the point A? ∗
- d) (relatively harder) What additional force would have to be applied to point


B to make point B’s acceleration zero?

∗

- A

C

- B


###### problem 9.22:

F = Fıˆ

###### ˆ

ıˆ

(Filename:pﬁgure.s94h10p2)

- 9.23 A uniform thin rod of length and mass m stands vertically, with one end resting on a frictionless surface and the other held by someone’s hand. The rod is released from rest, displaced slightly from the vertical. No forces are applied during the release. There is gravity.

- a) Find the path of the center of mass.
- b) Find the force of the ﬂoor on the end of the rod just before the rod is horizontal.


- 9.24 A uniform disk, with mass center labeled as point G, is sitting motionless on the frictionless xy plane. A massless peg is attached to a point on its perimeter. This disk has radius of 1m and mass of 10kg. A constant force of F = 1000Ni is applied to the peg for .0001s (one ten-thousandth of a second).

- a) What is the velocity of the center of mass of the center of the disk after the force is applied?
- b) Assuming that the idealizations named in the problem statement are exact is your answer to (a) exact or approximate?
- c) What is the angular velocity of the disk after the force is applied?
- d) Assuming that the idealizations named in the problem statement are exact is your answer to (c) exact or approximate?


- 9.25 A uniform thin ﬂat disc is ﬂoating in space. It has radius R and mass m. A force F is applied to it a distance d from the center in the y direction. Treat this problem as two-dimensional.


- a) What is the acceleration of the center of the disc? ∗
- b) What is the angular acceleration of the disk? ∗


- y


R F d

x

problem 9.25:

(Filename:pﬁgure.blue.102.1)

- 9.26 A uniform rectangular metal beam of mass m hangs symmetrically by two strings as shown in the ﬁgure.

- a) Draw a free body diagram of the beam and evaluate F.
- b) Repeat (a) immediately after the left string is cut.


3

2

| | |
|---|---|
| | |


A B

m

problem 9.26:

(Filename:pﬁg2.2.rp8)

- 9.27 A uniform slender bar AB of mass m is suspended from two springs (each of spring constant K) as shown. If spring 2 breaks, determine at that instant

- a) the angular acceleration of the bar,
- b) the acceleration of point A, and
- c) the acceleration of point B.


A B

1 2

L

problem 9.27:

(Filename:pﬁgure.blue.50.2)

- 9.28 Two small spheres A and B are connected byarigidrodoflength = 1.0ftandnegligible mass. The assembly is hung from a hook, as shown. Sphere A is struck, suddenly breaking its contact with the hook and giving it a hori-


zontal velocity v0 = 3.0ft/s which sends the assembly into free fall. Determine the angular momentum of the assembly about its mass center at point G immediately after A is hit. After the center of mass has fallen two feet, determine:

- a) the angle θ through which the rod has rotated,
- b) the velocity of sphere A,
- c) the total kinetic energy of the assembly of spheres A and B and the rod, and


d) the acceleration of sphere A.

A,W

v = v0

W = 5 lb

g

G

B,2W

θ

2 ft

problem 9.28:

(Filename:pﬁgure.blue.105.1)

The next several problems concern Work, power and energy

- 9.29 Verify that the expressions for work done by a force F, W = F S, and by a moment M, W = M θ, are dimensionally correct if S and  θ are linear and angular displacements respectively.
- 9.30 Calculate the energy stored in a spring usingtheexpression EP = 12kδ2 ifthespringis compressed by 100 mm and the spring constant is 100 N/m.

- 9.31 A point mass ‘m’ is pulled straight up by two strings. The two strings pull the mass symmetrically about the vertical axis with constant and equal force t. At an instant in time t, the position and the velocity of the mass are y(t)ˆ and y˙(t)ˆ, respectively. Draw a free body diagram of the mass at the instant of interest and evaluatethelefthandsideoftheenergybalance equation (P = E˙K).

h

T L T

m

x

y

problem 9.31:

(Filename:pﬁg2.3.rp2)

- 9.32 In a rack and pinion system, the rack is acted upon by a constant force F = 50N and has speed v = 2m/s in the direction of the force. Find the input power to the system.


ω

r

problem 9.32:

F = 50 N

(Filename:pﬁg2.3.rp6)

- 9.33 The driving gear in a compound gear train rotates at constant speed ω0. The driving torque is Min. If the driven gear rotates at a constant speed ωout, ﬁnd:

- a) the input power to the system, and
- b) the output torque of the system assuming there is no power loss in the system; i.e., power in = power out.


driving gear radius r driven gear radius R

ωin M

ωout

problem 9.33:

(Filename:pﬁg2.3.rp7)

- 9.34 An elaborate frictionless gear box has an input and output roller with Vin = const. Assumingthat Vout = 7Vin andtheforcebetween the left belt and roller is Fin = 3lb:


- a) What is Fout (draw a picture deﬁning the signs of Fin and Fout)?. ∗
- b) Is Fout greater or less than the Fin? (Assume Fin > 0.) Why? ∗


gear box

black box (frictionless)

Vin Vout

Positive power in Positive

power out

problem 9.34:

(Filename:pﬁgure.blue.138.1)

- 9.3 Special topics in planar kinematics
- 9.4 Mechanics of contacting bodies: rolling and sliding


- 9.35 A uniform disc of mass m and radius r rolls without slip at constant rate. What is the total kinetic energy of the disk?
- 9.36Anon-uniformdiscofmassm andradiusr rolls without slip at constant rate. The center of


mass is located at a distance r2 from the center of the disc. What is the total kinetic energy

of the disc when the center of mass is directly above the center of the disc?

- 9.37 Falling hoop. A bicycle rim (no spokes, tube, tire, or hub) is idealized as a hoop with mass m and radius R. G is at the center of the hoop. An inextensible string is wrapped around the hoop and attached to the ceiling. The hoop is released from rest at the position shown at t = 0.

- a) Find yG at a later time t in terms of any or all of m, R, g, and t.
- b) Does G movesidewaysasthehoopfalls and unrolls?


![image 143](Introduction to Statics and Dynamics Problems_images/imageFile143.png)

m,R

yG

problem 9.37:

(Filename:p.s96.p3.2)

- 9.38 A uniform disk with radius R and mass m has a string wrapped around it. The string is pulled with a force F. The disk rolls without slipping.

- a) What is the angular acceleration of the

disk, αDisk = −θ¨kˆ? Make any reasonable assumptions you need that are consistent with the ﬁgure information and the laws of mechanics. State your assumptions. ∗

- b) Find the acceleration of the point A in the ﬁgure. ∗


A

F = 1N

2 m x

uniform disk, I = 0.5 kg m2 M = 1 kg

G

Rolling contact, no slip

problem 9.38:

(Filename:pﬁgure.blue.43.1)

- 9.39 Ifapebbleisstucktotheedgeofthewheel in problem 9.9, what is the maximum speed of the pebble during the motion? When is the force on the pebble from the wheel maximum? Draw a good FBD including the force due to gravity.


P

C

| | |
|---|---|
| | |


problem 9.39:

(Filename:pﬁgure.s94h11p2.a)

- 9.40 Spool Rolling without Slip and Pulled by a Cord. See also problem 9.42. The lightweight spool is nearly empty but a lead ball with mass m has been placed at its center. A force F is applied in the horizontal direction to the cord wound around the wheel. Dimensions are as marked. Coordinate directions are as marked.

- a) What is the acceleration of the center of the spool? ∗
- b) What is the horizontal force of the ground on the spool? ∗


Ro roll without C Ri

slip F

ıˆ

ˆ

problem 9.40:

(Filename:pﬁgure.s94h11p5)

- 9.41 A ﬁlm spool is placed on a very slippery table. Assume that the ﬁlm and reel (together) have mass distributed the same as a uniform disk of radius Ri. What, in terms of Ri, Ro, m, g, ıˆ, ˆ, and F are the accelerations of points C and B at the instant shown (the start of motion)?

Ro C Ri

B frictionless contact

(no friction) F

ıˆ

ˆ

problem 9.41:

(Filename:p.f96.f.4)

- 9.42 Again, Spool Rolling without Slip and Pulled by a Cord. Reconsider the spool from problem 9.40. This time, a force F is applied vertically to the cord wound around the wheel. In this case, what is the acceleration of the center of the spool? Is it possible to pull the cord at some angle between horizontal and vertical so that the angular acceleration of the spool or the acceleration of the center of mass is zero?

If so, ﬁnd the angle in terms of Ri, R0, m, and F.

- 9.43 A napkin ring lies on a thick velvet tablecloth. The thin ring (of mass m, radius r) rolls without slip as a mischievous child pulls the tablecloth (mass M) out with acceleration A. The ring starts at the right end (x = d). You can make a reasonable physical model of this situation with an empty soda can and a piece of paper on a ﬂat table.


- a) What is the ring’s acceleration as the tablecloth is being withdrawn?
- b) How far has the tablecloth moved to the right from its starting point x = 0 when the ring rolls off its left-hand end?
- c) Clearly describe the subsequent motion of the ring. Which way does it end up rolling at what speed?
- d) Would your answer to the previous question be different if the ring slipped on the cloth as the cloth was being pulled out?


napkin ring r tablecloth

m

x

A

d

problem 9.43:

(Filename:pﬁgure.blue.51.1)

- 9.44 A block of mass M is supported by two rollers (uniform cylinders) each of mass m and radius r. They roll without slip on the block and the ground. A force F is applied in the horizontal direction to the right, as shown in the ﬁgure. Given F, m, r, and M, ﬁnd:

- a) the acceleration of the block,
- b) the acceleration of the center of mass of this block/roller system,
- c) the reaction at the wheel bases,
- d) theforceoftherightwheelontheblock,
- e) the acceleration of the wheel centers, and
- f) the angular acceleration of the wheels.

F M

- g


problem 9.44:

(Filename:pﬁgure.blue.108.2)

- 9.45 Dropped spinning disk. 2-D . A uniform disk of radius R and mass m is gently dropped onto a surface and doesn’t bounce. When it is


released it is spinning clockwise at the rate θ˙0. Thediskskidsforawhileandtheniseventually rolling.

- a) What is the speed of the center of the disk when the disk is eventually rolling

(answer in terms of g, µ, R, θ˙0, and m)? ∗

- b) In the transition from slipping to rolling, energy is lost to friction. How does the amount lost depend on the coefﬁcient of friction (and other parameters)? How does this loss make or not make sense in the limit as µ → 0 and the dissipation rate → zero? ∗


y

θ˙ g

R

x

µ

problem 9.45:

(Filename:pﬁgure.s95q10)

9.46Diskonaconveyorbelt. Auniformmetal cylinder with mass of 200kg is carried on a conveyerbeltwhichmovesat V0 = 3m/s. The diskisnotrotatingwhenonthebelt. Thediskis delivered to a ﬂat hard platform where it slides for a while and ends up rolling. How fast is it moving (i.e. what is the speed of the center of mass) when it eventually rolls? ∗

m = 200 kg r = 0.1m

no rotation

no slip

y

rolling disk

x Vo

| | |
|---|---|
| | |


| | |
|---|---|
| | |


belt

problem 9.46:

(Filename:pﬁgure.s94h11p3)

- 9.47 A rigid hoop with radius R and mass m is rolling without slip so that its center has trans-

lational speed vo. It then hits a narrow bar with height R/2. When the hoop hits the bar suddenly it sticks and doesn’t slide. It does hinge freelyaboutthebar,however. Thegravitational constant is g. How big is vo if the hoop just barely rolls over the bar? ∗

R

R/2

hoop of mass m

vo rigid bar

g

problem 9.47:

(Filename:pﬁgure.blue.87.5)

- 9.48 2-D rolling of an unbalanced wheel. A wheel, modeled as massless, has a point mass (mass = m) at its perimeter. The wheel is released from rest at the position shown. The wheel makes contact with coefﬁcient of friction µ.


- a) What is the acceleration of the point P justafterthewheelisreleasedifµ = 0?
- b) What is the acceleration of the point P justafterthewheelisreleasedifµ = 2?
- c) Assuming the wheel rolls without slip (no-slip requires, by the way, that the friction be high: µ = ∞) what is the velocity of the point P just before it touches the ground?


###### ˆ

R

g

P ıˆ

problem 9.48:

(Filename:pﬁgure.s94f1p1)

###### 9.49 Spool and mass. A reel of mass M and

moment of inertia Izzcm = I rolls without slipping upwards on an incline with slope-angle α.

It is pulled up by a string attached to mass m as shown. Find the acceleration of point G in terms of some or all of M,m, I, R,r,α, g and any base vectors you clearly deﬁne.

M, I

g

R

massless pulley

G

r

m

no slip

α

problem 9.49:

(Filename:s97f4)

###### 9.50 Two objects are released on two identicalramps. One is a sliding block (no friction),the other a rolling hoop (no slip). Both havethe same mass, m, are in the same gravity ﬁeldand have the same distance to travel. It takesthe sliding mass 1 s to reach the bottom of theramp. How long does it take the hoop? [Usefulformula: “s = 12at2”]

m

L

φ

g

L

R m

φ

problem 9.50:

(Filename:pﬁgure.blue.51.2)

###### 9.51 The hoop is rolled down an incline that is30◦ from horizontal. It does not slip. It doesnot fall over sideways. It is let go from rest att = 0.

- a) At t = 0+ what is the acceleration of the hoop center of mass?
- b) At t = 0+ what is the acceleration of the point on the hoop that is on the incline?
- c) At t = 0+ what is the acceleration of the point on the hoop that is furthest from the incline?


d) After the hoop has descended 2 vertical meters (and traveled an appropriate distance down the incline) what is the acceleration of the point on the hoop that is (at that instant) furthest from the incline?

30o

problem 9.51:

(Filename:pﬁgure.blue.47.1)

9.52 A uniform cylinder of mass m and radius r rolls down an incline without slip, as shown below. Determine: (a) the angular acceleration α of the disk; (b) the minimum value of the coefﬁcient of (static) friction µ that will insure no slip.

g

r

30o

problem 9.52:

(Filename:pﬁgure.blue.49.3)

9.53Raceofrollers. Auniformdiskwithmass M0 and radius R0 is allowed to roll down the frictionless but quite slip-resistant (µ = 1) 30◦ ramp shown. It is raced against four other objects (A, B, C and D), one at a time. Who wins the races, or are there ties? First try to construct any plausible reasoning. Good answers will be based, at least in part, on careful use of equations of mechanics. ∗

- a) Block A hasthesamemassandhascen-

terofmassadistance R0 fromtheramp. It rolls on massless wheels with frictionless bearings.

- b) Uniform disk B has the same mass (MB = M0)buttwicetheradius(RB = 2R0).
- c) Hollow pipe C has the same mass (MC = M0) and the same radius (RC = R0).
- d) Uniform disk D has the same radius (RD = R0) but twice the mass (MD = 2M0).


Can you ﬁnd a round object which will roll as fast as the block slides? How about a massless cylinder with a point mass in its center? Can you ﬁnd an object which will go slower than the slowest or faster than the fastest oftheseobjects? Whatwouldtheybeandwhy? (This problem is harder.)

| | |
|---|---|
| | |


R0

θ

L

| | |
|---|---|
| | |


R0

A B

| | |
|---|---|
| | |


C D

problem 9.53:

(Filename:pﬁgure.s94h11p4)

- 9.54 A roller of mass M and polar moment of

inertiaaboutthecenterofmass IG is connected to a spring of stiffness K by a frictionless hinge

- as shown in the ﬁgure. Consider two kinds of friction between the roller and the surface it moves on:


- 1. Perfect slipping (no friction), and
- 2. Perfect rolling (inﬁnite friction).


- a) What is the period of oscillation in the ﬁrst case?
- b) What is the period of oscillation in the second case?


K

roller, M, IG hinge G

friction

problem 9.54:

(Filename:pﬁgure.blue.141.2)

- 9.55 A uniform cylinder of mass m and radius R rolls back and forth without slipping through small amplitudes (i.e., the springs attached at point A on the rim act linearly and the vertical change in the height of point A is negligible). Thesprings, whichactbothincompressionand tension, areunextendedwhenAisdirectlyover C.


- a) Determine the differential equation of motion for the cylinder’s center.
- b) Calculate the natural frequency of the system for small oscillations.


k A k

x

C

R

problem 9.55:

(Filename:pﬁgure.blue.152.1)

RC

RD

problem 9.56: A disk rolls without slip inside a bigger cylinder.

(Filename:h12.3)

9.56 A disk rolls in a cylinder. For all of the problems below, the disk rolls without slip and s back and forth due to gravity.

- a) Sketch. Draw a neat sketch of the disk in the cylinder. The sketch should show all variables, coordinates and dimension used in the problem.
- b) FBD. Draw a free body diagram of the disk.
- c) Momentum balance. Write the equations of linear and angular momentum balance for the disk. Use the point on the cylinder which touches the disk for the angular momentum balance equation. Leave as unknown in these equations variables which you do not know.
- d) Kinematics. The disk rolling in thecylinderisaone-degree-of-freedom system. That is, the values of only one coordinate and its derivatives are enough to determine the positions, velocities and accelerations of all points. The angle that the line from the center of the cylinder to the center of the disk makes from the vertical can be used as such a variable. Find all of the velocitiesandaccelerationsneededinthemomentum balance equation in terms of this variable and it’s derivative. [Hint: you’ll need to think about the rolling contact in order to do this part.]
- e) Equation of motion. Write the angular momentum balance equation as a single second order differential equation.
- f) Simple pendulum? Does this equation reduce to the equation for a pendulum with a point mass and length equal to the radius of the cylinder, when the disk radius gets arbitrarily small? Why, or why not?
- g) How many? How many parts can one simple question be divided into?


- 9.57 A uniform hoop of radius R1 and mass m rolls from rest down a semi-circular track of

radius R2 as shown. Assume that no slipping occurs. At what angle θ does the hoop leave the track and what is its angular velocity ω and the linear velocity v of its center of mass at that instant? If the hoop slides down the track without friction, so that it does not rotate, will it leave at a smaller or larger angle θ than if it rolls without slip (as above)? Give a qualitative argument to justify your answer.

HINT: Here is a geometric relationship between angle φ hoop turns through and angle θ subtended by its center when no slipping occurs: φ = [(R1 + R2)/R2]θ. (You may or may not need to use this hint.)

c

(Hint)

- R1
- R2


O

A

O

A θ

ω φ

tˆ

nˆ

problem 9.57:

(Filename:pﬁgure.blue.46.1)

9.5 Collisions

- 9.58 The two blocks shown in the ﬁgure are identical except that one rests on two springs whiletheotheronesitsontwomasslesswheels. Draw free body diagrams of each mass as each is struck by a hammer. Here we are interested in the free body diagrams only during collision. Therefore, ignore all forces that are much smaller than the impulsive forces. State in words why the forces you choose to show should not be ignored during the collision.


m m

k k

problem 9.58:

(Filename:pﬁg2.1.rp9)

- 9.59 These problems concerns two colliding masses. In the ﬁrst case In (a) the smaller mass hits the hanging mass from above at an angle 45◦ with the vertical. In (b) second case the smaller mass hits the hanging mass from below

at the same angle. Assuming perfectly elastic impact between the balls, ﬁnd the velocity of thehangingmassjustafterthecollision. [Note, these problems are not well posed and can only be solved if you make additional modeling assumptions.]

45o

45o

m

m

M M

V

V

(a) (b)

problem 9.59:

(Filename:pﬁg2.2.rp7)

- 9.60 A narrow pole is in the middle of a pond with a 10m rope tied to it. A frictionless ice skater of mass 50kg and speed 3m/s grabs the rope. The rope slowly wraps around the pole. What is the speed of the skater when the rope is 5m long? (A tricky question.)

pole m = 50 kg

v0 = 3m/s

rope

10 m 5 m

problem 9.60:

(Filename:pﬁgure.blue.49.1)

- 9.61 The masses m and 3m are joined by a light-weight bar of length 4 . If point A in the center of the bar strikes ﬁxed point B vertically


with velocity V0, and is not permitted to rebound, ﬁnd θ˙ of the system immediately after impact.

4

2

- A
- B


V0 3m

m

Neglect gravity

problem 9.61: Neglect gravity!

(Filename:pﬁgure.blue.81.1)

- 9.62 Two equal masses each of mass m are joined by a massless rigid rod of length . The assembly strikes the edge of a table as shown in the ﬁgure, when the center of mass is moving downward with a linear velocity v and the system is rotating with angular velocity φ˙ in the counter-clockwise sense. The impact is ’elastic’. Find the immediate subsequent motion of the system, assuming that no energy is lost during the impact and that there is no gravity. Show that there is an interchange of translational and rotational kinetic energy.

φ ˙ v

problem 9.62:

(Filename:pﬁgure.blue.137.2)

- 9.63 In the absence of gravity, a thin rod of mass m and length is initially tumbling


with constant angular speed ωo, in the counterclockwise direction, while its mass center has

constant speed vo, directed as shown below. The end A then makes a perfectly plastic collision with a rigid peg O (via a hook). The velocity of the mass center happens to be perpendicular to the rod just before impact.

- a) What is the angular speed ωf immediately after impact?
- b) What is the angular speed 10 seconds after impact? Why?
- c) What is the loss in energy in the plastic collision?


Before impact

O hook

A

vo

G

ωo

d

After impact

O

Perfectly plastic collision

G

ωf

problem 9.63:

(Filename:pﬁgure.blue.78.2)

- 9.64 Agymnastofmassm andextendedheight L is performing on the uneven parallel bars. About the x, y, z axes which pass through her center of mass, her radii of gyration are kx, ky, and kz, respectively. Just before she grasps the top bar, her fully extended body is horizontal and rotating with angular rate ω; her center of mass is then stationary. Neglect any friction between the bar and her hands and assume that she remains rigid throughout the entire stunt.

- a) What is the gymnast’s rotation rate just after she grasps the bar? State clearly any approximations/assumptions that you make.
- b) Calculate the linear speed with which herhips(CM)strikethelowerbar. State all assumptions/approximations.
- c) Describe (in words, no equations please) her motion immediately after her hips strike the lower bar if she releases her hands just prior to this impact.


L/2

L/2

Just as top bar is grasped

L

cm upper bar lower bar

ω

θ

y z

problem 9.64:

(Filename:pﬁgure.blue.130.2)

- 9.65 An acrobat modelled as a rigid body. An acrobat is modeled as a uniform rigid mass m oflengthl. Theacrobatfallswithoutrotation in the position shown from height h where she was stationary. She then grabs a bar with a ﬁrm but slippery grip. What is h so that after the subsequent motion the acrobat ends up in a stationary handstand? [ Hints: Note what quantities are preserved in what parts of the motion.] ∗

L

h

bar BEFORE

DURING

AFTER

problem 9.65:

(Filename:pﬁgure.s94h10p4)

- 9.66 Acrudesee-sawisbuiltwithtwosupports separated by distance d about which a rigid plank (mass m, length L) can pivot smoothly. The plank is placed symmetrically, so that its


center of mass is midway between the supports when the plan is at rest.

- a) While the left end is resting on the left support, the right end of the plank is lifted to an angle θ and released. At

what angular velocity ω1 will the plank strike the right hand support?

- b) Followingtheimpact, theleftendofthe plank can pivot purely about the right end if d/L is properly chosen and the


right end does not bounce. Find ω2 under these circumstances.

L

c.m.

| | |
|---|---|
| | |


#### d

Just Before Collision

- ω1
- ω2


Just After Collision

| | |
|---|---|
| | |


problem 9.66:

(Filename:pﬁgure.blue.81.2)

- 9.67 Baseball bat. In order to convey the ideas without making the calculation to complicated, some of the simplifying assumptions here are highly approximate. Assume that a bat is a


uniform rigid stick with length L and mass ms. The motion of the bat is a pivoting about one end held ﬁrmly in place with hands that rotate but do not move. The swinging of the bat occurs by the application of a constant torque Ms at the hands over an angle of θ = π/2 until the point of impact with the ball. The ball has mass mb and arrives perpendicular to the bat at an absolute speed vb at a point a distance from the hands. The collision between the bat and the ball is completely elastic.

a) To maximize the speed vhit of the hit ball How heavy should a baseball bat be? Where should the ball hit the bat? Here are some hints for one way to approach the problem.

- • Find the angular velocity of the bat just before collision by drawing a FBD of the bat etc.
- • Find the total energy of the ball and bat system just before the collision.
- • Draw a FBD of the ball and of the bat during the collision (with this model there is an impulse at


the hands on the bat). Call the magnitude of the impulse of the ball on the bat (and visa versa)

Fdt.

- • Use various momentum equations to ﬁnd the angular velocity of the bat and velocity of the ball just after the collision in terms of Fdt and other quantities above. Use these to ﬁnd the energy of the system just after collion.
- • Solve for the value of Fdt that conserves energy. As a check you should see if this also predicts that the relative separation speed of the ball and bat (at the impact point) is the same as the relative approach speed (it should be).
- • You now know can calculte vhit in terms of mb,ms, Ms, L, , and vb.
- • Find the maximum of the above


expression by varying ms and . Pick numbers for the ﬁxed quantities if you like.

- b) Canyouexplaininwordswhatiswrong with a bat that is too light or too heavy?
- c) Which aspects of the model above do you think lead to the biggest errors in predictingwhatarealballplayershould pick for a bat and place on the bat to hit the ball?
- d) Describe as clearly as possible a different model of a baseball swing that you think would give a more accurate prediction. (You need not do the calculation).


Kinematics using time-varying base vectorsProblemsforallthreesectionsofthischapter are combined.

##### 10.1 Polar coordinates andpath coordinates

- 10.2 Rotating reference frames
- 10.3Generalexpressionsfor velocity and acceleration


- 10.1 Express the basis vectors (ıˆ ,ˆ ) associated with axes x and y in terms of the standard basis (ıˆ,ˆ) for θ = 30o.

x

y

x'

y'

θ

problem 10.1:

(Filename:eﬁg1.2.23)

- 10.2 Body frames are frames of reference attached to a body in motion. The orientation of a coordinate system attached to a body frame B is shown in the ﬁgure at some moment of interest. For θ = 60o, express the basis vectors (bˆ1,bˆ2) in terms of the standard basis (ıˆ,ˆ).


y

B

bˆ2

bˆ1

###### θ

x

problem 10.2:

(Filename:eﬁg1.2.24)

- 10.3 Find the components of (a) v = 3m/sıˆ + 2m/sˆ + 4m/skˆ in the rotated basis (ıˆ ,ˆ ,kˆ ) and (b) a = −0.5m/s2ˆ +

3.0m/s2kˆ in the standard basis (ıˆ,ˆ,kˆ). (y and y are in the same direction and x and z are in the xz plane.)

x

y, y'

z

x'

z'

θ

θ

problem 10.3:

(Filename:eﬁg1.2.25)

- 10.4 For Q given in problem 12.22 and M =

25N·mEˆ 1 − 32N·mEˆ 2, ﬁnd the eˆ2 component of M without calculating [Q]{ M}.

- 10.5 A particle travels in a straight line in the xy-plane parallel to the x-axis at a distance y = in the positive x direction. The position of the particle is denoted by r(t). The angle of r measured positive counter-clockwise from the x axis is decreasing at a constant rate with magnitude ω. If the particle starts on the y axis at θ = π/2, what is r(t) in cartesian coordinates?
- 10.6 Given that r(t) = ct2ıˆ and that θ(t) = d sin(λt) ﬁnd v(t)

- (a) in terms of ıˆ and ˆ,
- (b) in terms of ıˆ and ˆ .


r(t)

ıˆ

ıˆ'

ˆ' ˆ

θ

problem 10.6:

(Filename:pﬁg3.1.DH1)

- 10.7 Abugwalksonastraightlineengravedon a rotating turntable (the bug’s path in the room is not a straight line). The line passes through the center of the turntable. The bug’s speed on thislineis1in/s(thebug’sabsolutespeedisnot 1in/s). The turntable rotates at a constant rate of 2 revolutions every π s in a positive sense about the z-axis. It’s surface is always in the


xy-plane. At time t = 0, the engraved line is aligned with the x-axis, the bug is at the origin and headed towards the positive x direction.

- a) What is the x component of the bug’s velocity at t = π s?
- b) What is the y component of the bug’s velocity at t = π seconds?
- c) What is the y component of the bug’s acceleration at t = π?
- d) What is the radius of curvature of the bug’s path at t = 0?


- 10.8 A bug walks on a turntable. In polar coordinates, the position of the bug is given by

R = Reˆr, where the origin of this coordinate system is at the center of the turntable. The

(eˆr,eˆθ) coordinate system is attached to the turntable and, hence, rotates with the turntable. The kinematical quantities describing the bugs motion are R˙ = −R˙0, R¨ = 0, θ˙ = ω0, and θ¨ = 0. A ﬁxed coordinate system Oxy has origin O at the center of the turntable. As the bug walks through the center of the turntable:

- a) What is its speed?
- b) What is its acceleration?
- c) What is the radius of the osculating circle (i.e., what is the radius of curvature of the bug’s path?).


- 10.9 Actual path of bug trying to walk a straight line. A straight line is inscribed on a horizontal turntable. The line goes through the center. Let φ be angle of rotation of the


turntable which spins at constant rate φ˙0. A bug starts on the outside edge of the turntable ofradius R andwalkstowardsthecenter,passes through it, and continues to the opposite edge of the turntable. The bug walks at a constant speedvA, asmeasuredbyhowfarherfeetmove per step, on the line inscribed on the table. Ignore gravity.

- a) Picture. Make an accurate drawing of the bug’s path as seen in the room (which is not rotating with the turntable). In order to make this plot, you will need to assume values of vA and φ˙0 and initial values of R and φ. You will need to write a parametric equation for the path in terms of variables that you can plot (probably x and y coordinates). You will also need to pick a range of times. Your plot should include the instant at which the bug walks through the origin. Make sure your x− and y− axes are drawn to the same scale. A computer plot would be nice.
- b) Calculate the radius of curvature of the bug’s path as it goes through the origin.


∗

- c) Accurately draw (say, on the computer) the osculating circle when the bug is at the origin on the picture you drew for (a) above.
- d) Force. What is the force on the bugs feet from the turntable when she starts her trip? Draw this force as an arrow on your picture of the bug’s path.
- e) Force. What is the force on the bugs feet when she is in the middle of the turntable? Draw this force as an arrow on your picture of the bug’s path.


- 10.12 A turntable oscillates with displacement xC(t) = Asin(st)ıˆ. The disc of the turntable rotates with angular speed and acceleration ωD andω˙ D. Asmallbugwalksalongline DE with velocity vb relative to the turntable. At the instant shown, the turntable is at its maximum amplitude x = A, the line DE is currently aligned with the z-axis, and the bug is passing through point B on line DE. Point B is a distance a from the center of the turntable, point C. Find the absolute acceleration of the bug, ab. ∗

![image 144](Introduction to Statics and Dynamics Problems_images/imageFile144.png)

![image 145](Introduction to Statics and Dynamics Problems_images/imageFile145.png)

![image 146](Introduction to Statics and Dynamics Problems_images/imageFile146.png)

![image 147](Introduction to Statics and Dynamics Problems_images/imageFile147.png)

ωD,ω˙D

a

B

C

D

E

x

y z

problem 10.12:

(Filename:Mikes93p2)

- 10.13 See also problem 10.15. A small .1kg toy train engine is going clockwise at a constant rate (relative to the track) of 2m/s on a circular track of radius 1m. The track itself is on a turntable B that is rotating counter- clockwise at a constant rate of 1rad/s. The dimensions are as shown. At the instant of interest the train is pointing due south (−j) and is at the center


- 10.10 A small bug is crawling on a straight line scratched on an old record. The scratch, at its closest, is a distance = 6cm from the center of the turntable. The turntable is turning clockwise at a constant angular rate ω = 2rad/s. The bug is walking, relative to the turntable, at

a constant rate vB/T = 12cm/s, straight along the scratch in the y-direction. At the instant of interest, everything is aligned as shown in ﬁgure. The bug has a mass mB = 1 gram.

- a) What is the bug’s velocity?
- b) What is the bug’s acceleration?
- c) What is the sum of all forces acting on the bug?
- d) Sketch the path of the bug in the neighborhood of its location at the time of interest (indicate the direction the bug is moving on this path).


bug

x

y

vB/T

ω

problem 10.10:

(Filename:pﬁgure.blue.55.2)

- 10.11 A bug of mass m = 1kg walks on a straight line marked through the center of a turntable on the back of a pick-up truck, exactly as in problem 10.17. Evaluate the absolute velocity and acceleration of the bug in the following situations (in cartesian coordinates):


|KinematicalQuantitiesO of the turntable.|
|---|


| | |xT|x˙T|x¨T<br><br>|rb<br><br>|r˙b|r¨b|θ|ω<br><br>|ω˙|
|---|---|---|---|---|---|---|---|---|---|---|


a) What is the velocity of the train relative

|(a)| |4m|3m/s<br><br>|0m/s2|1m|0m/s|0m/s2 to<br><br>|the turntab37o|le0rad v/B/s?<br><br>|0rad/s2|
|---|---|---|---|---|---|---|---|---|---|---|
|(b)| |”|”<br><br>|2m/s2|”<br><br>|”|”<br><br>|”<br><br>|”<br><br>|”|
|(c)| |”|”<br><br>|0m/s2<br><br>|”|”<br><br>|”b) W|hatistheaπ/2rad<br><br>|bsolutevel1rad/s|ocityofthe”|
|(d)| |”<br><br>|”<br><br>|”<br><br>|”|”<br><br>|1m/s2 v<br><br>|? 0rad|0rad/s<br><br>|”|
|(e)| |”|”|”|0m<br><br>|1m/s|0m/s2 c) W|” hat is the a<br><br>|1rad/s cceleratio|” n of the trai|
|( f )| |”<br><br>|”<br><br>|”|1m|0m/s<br><br>|” at|ive to the tπ/2rad<br><br>|urntable0rad/s a|3rad? /s2|
|(g)| |”<br><br>|”<br><br>|2m/s2|”<br><br>|5m/s|−2m/s2|0rad|”<br><br>|/0rad/s2<br><br>B|
|(h)| |”<br><br>|”|”|”|0m/s<br><br>|0m/d)s2 W|hat is the aπ/2rad<br><br>|bsolute ac”<br><br>|celeration o2rad/s2|
|(i)| |”|”<br><br>|4m/s2|”<br><br>|”|” tra<br><br>|in0rad a?<br><br>|2rad/s|0rad/s2|


train

n rel-

f the

- e) What is the total force acting on the train?
- f) Sketch the path of the train for one revolution of the turntable (surprise)?


###### ˆ

North

turntable, B

track

1m

East O

ıˆ

problem 10.13:

(Filename:pﬁgure.f93f4)

10.14 A giant bug walks on a horizontal disk. An x − y − z frame is attached to the disk. The disk is rotating about the z axis (out of the paper) and simultaneously translating with respect to an inertial frame X − Y − Z plane. In eachofthecasesshownintheﬁgure, determine the total force acting on the bug. In each case, the dotted line is scratched on the disk and is the path the bug follows walking in the direction of the arrow. The location of the bug is marked with a dot. At the instants shown, the x − y − z coordinate system shown is aligned with the inertial X − Y − Z frame (which is not shown in the pictures). In this problem:

r = the position of the center of the disk, v = the velocity of the center of the disk, a = the acceleration of the center of the disk,

the angular velocity of the disk (i.e., = k),

˙ = the angular acceleration of the disk, u = the speed of the bug traversing the dotted line (arc length on the disk per unit time), u˙ = du/dt, and m = 1kg = mass of the bug.

y

1m

- u = 0 u˙ = 0

= 0 ˙ = 0

- u = 1 m/s u˙ = 0


r = 0ıˆ + 0ˆ v = 0ıˆ + 0ˆ a = 3m/s2ıˆ + 0ˆ

45o

- a)

C

1m

- b)

- c) C

1m

e) C

- d) C 1m


C

x

y

45o

###### = 0

x

- ˙ = 0

r = 0ıˆ + 0ˆ v = 0ıˆ + 0ˆ a = 0ıˆ + 0ˆ

r = 0ıˆ + 0ˆ v = 0ıˆ + 0ˆ a = 0ıˆ + 0ˆ

r = 0ıˆ + 0ˆ v = 0ıˆ + 0ˆ a = 0ıˆ + 0ˆ

r = 0ıˆ + 0ˆ v = 0ıˆ + 0ˆ a = 0ıˆ + 0ˆ

u = 0 u˙ = 0

= 0

- ˙ = 1 rad/s2


y

1m

x

1m

y

- u = 0 u˙ = 0

= 1 rad/s ˙ = 0

- u = 1 m/s u˙ = 0


x

y

45o x

###### = 1 rad/s˙ = 0

###### problem 10.14:

(Filename:pﬁgure.blue.117.1)

- 10.15 Repeat questions (a)-(f) for the toy train in problem 10.13 going counter-clockwise at constant rate (relative to the track) of 2m/s on the circular track.
- 10.16 A honeybee, sensing that it can get a cheap thrill, alights on a phonograph turntable that is being carried by a carnival goer who is riding on a carousel. The situation is sketched below. The carousel has angular velocity of 5rpm, which is increasing (accelerating) at 10rev/min2; the phonograph rotates at a constant 33 1/3 rpm. The honeybee is at the outer edge of the phonograph record in the position shown in the ﬁgure; the radius of the record is 7 inches. Calculate the magnitude of the acceleration of the honeybee.

carousel

30o

bee

12'

turntable

problem 10.16:

(Filename:pﬁgure.blue.67.2)

- 10.17 See also problem 10.11. Consider a turntable on the back of a pick-up truck. A bug walks on a line on the turntable. The line may or may not be drawn through the center of the turntable. The truck may or may not be going at constant rate. The turntable may or may not be spinning, and, if it spins, it may or may not goataconstantrate. Thebugmaybeanywhere


on the line and may or may not be walking at a constant rate.

- a) Draw a picture of the situation. Clearly deﬁne all variables you are going to use. What is the moving frame, and what is the reference point on that frame?
- b) One term at a time. For each term in the ﬁve term acceleration formula, ﬁnd a situation where all but one term is zero. Use the turntable as the moving

frame, thebugastheparticleofinterest.

∗

- c) Two terms at a time. (harder) How many situations can you ﬁnd where a pair of terms is not zero but all other terms are zero? (Don’t try to do all 10 cases unless you really think this infamous formula is fun. Try at least one or two.) ∗


y

turntable

xT

x

O'

Truck

Blow-up of turntable:

bug

rb

ω θ

P

O'

problem 10.17: Picking apart the ﬁve term acceleration formula.

(Filename:pﬁgure.blue.75.1)

10.18 Slider crank kinematics (No FBD required!). 2-D . Assume R, ,θ,θ,˙ θ¨ are given. The crank mechanism parts move on the xy plane with the x direction being along the piston. Vectors should be expressed in terms of ıˆ,ˆ, and kˆ components.

- a) What is the angular velocity of the crank OA? ∗
- b) What is the angular acceleration of the crank OA? ∗
- c) What is the velocity of point A? ∗
- d) What is the acceleration of point A? ∗
- e) What is the angular velocity of the connecting rod AB? [Geometry fact: r AB = 2 − R2 sin2 θ ıˆ−R sinθˆ] ∗

- f) For what values of θ is the angular velocity of the connecting rod AB equal to zero (assume θ˙  = 0)? (you need not answer part (e) correctly to answer this question correctly.) ∗


A

crank rod

R

O

θ

M

B

###### ˆ

piston

motor

ıˆ

###### problem 10.18:

(Filename:pﬁgure.s95q12)

- 10.19 Slider-Crank. See also problem 11.34. Consider a slider-crank mechanism. Given θ, θ˙, θ¨, L, and R, can you ﬁnd the velocity and acceleration of B? There are many ways to do this problem.

M

O

A

B

R L

motor

crank rod

piston

θ

ıˆ

ˆ

problem 10.19:

(Filename:f.5)

- 10.20 Thecrank ABwithlength LAB = 1inch in the crank mechanism shown rotates at a con-

stant rate θ˙AB = ωAB = 2π rad/s counterclockwise. Theinitialangleofrotationisθ = 0 at t = 0. The connecting rod BC has a length of LBC = 2in.

- a) What is the velocity of point B at the end of the crank when θ = π/2rad?
- b) What is the velocity of point C at the end of the connecting rod when θ = π/2rad?
- c) What is the angular velocity of the connecting rod BC when θ = π/2rad?
- d) What is the angular velocity of the connecting rod BC as a function of time?


B

LAB

LBC

C A

ωAB = 2π rad/s

θ

problem 10.20:

(Filename:pﬁgure.blue.116.1)

- 10.21 See also problem 10.22. The two rods AB and DE, connected together through a collar C, rotate in the vertical plane. The collar C is pinned to the rod AB but is free to slide on the frictionless rod DE. At the instant shown, rodABisrotatingclockwisewithangular speed ω = 3rad/s and angular acceleration α = 2rad/s2. Find the angular velocity of rod DE. ∗


B D C

- 10.24 A bar of length = 5ft, body D, connects sliders A and B on an L-shaped frame, body L, which itself is rotating at constant speed about an axle perpendicular to the plane of the ﬁgure through the point O and relative to

a ﬁxed frameF , ωL/F = 0.5rad/sk . At the instant shown, bodyLis aligned withthex−y axes, slider A is xA = 4ft from point O, slider B is yB = 3ft from O. The speed and acceleration of slider B relative to the frame L are vB/L = −2ft/sˆ and aB/L = −2ft/s2ˆ, respectively.

Determine:

- a) The absolute velocity of the slider A, vA/F , and
- b) The absolute angular velocity of bar AB, body D, ωD/F .


x

y

A

B

L O

D

ωL/F xA

yB

problem 10.24:

(Filename:pﬁgure.blue.115.1)

- 10.25 See also problem 11.35. The link AB is supported by a wheel at D and its end A is constrained so that it only has horizontal velocity. No slipping occurs between the wheel and the link. The wheel has an angular velocity ω and radius r. The distance O A = .

Given: ω, r, and . (β = sin−1 r ). Determine the angular velocity of the link AB and velocity of the point A.

r

D

B

A

O β

ω

problem 10.25:

(Filename:pﬁgure.blue.121.1)

- 10.26 See also problem 11.36. A solid cylinder of radius R and mass M rolls without slip along the ground. A thin rod of mass m and length L is attached by a frictionless pin P to the cylinder’s rim and its right end is dragged


![image 148](Introduction to Statics and Dynamics Problems_images/imageFile148.png)

![image 149](Introduction to Statics and Dynamics Problems_images/imageFile149.png)

P

![image 150](Introduction to Statics and Dynamics Problems_images/imageFile150.png)

![image 151](Introduction to Statics and Dynamics Problems_images/imageFile151.png)

L

m R

M

θ vA

0.5 m

###### problem 10.26:

(Filename:pﬁgure.blue.116.2)

45o

ω,α

A E

- 10.27 The slotted link CB is driven in an oscillatory motion by the link ED which rotates about D with constant angular velocity

θ˙ = ωD. The pin P is attached to ED at ﬁxed radius d and engages the slot on CB as shown. Find the angular velocity and acceleration θ˙ and θ¨ of CB when θ = π/2.

E B P

C D

d θ

φ

problem 10.27:

(Filename:pﬁgure.blue.65.3)

- 10.28 The rod of radius r = 50mm shown has a constant angular velocity of ω = 30rad/s counterclockwise. Knowing that rod AD is 250mm long and distance d = 150mm, determine the acceleration of collar D when θ = 90◦.


problem 10.21:

(Filename:summer95f.4)

- 10.22Reconsiderproblem10.21. Thetworods AB and DE, connected together through a collar C, rotate in the vertical plane. The collar C is pinned to the rod AB but is free to slide on the frictionless rod DE. At the instant shown, rodABisrotatingclockwisewithangular speed ω = 3rad/s and angular acceleration α = 2rad/s2. Find the angular acceleration of rod DE. ∗


B D C

![image 152](Introduction to Statics and Dynamics Problems_images/imageFile152.png)

![image 153](Introduction to Statics and Dynamics Problems_images/imageFile153.png)

![image 154](Introduction to Statics and Dynamics Problems_images/imageFile154.png)

![image 155](Introduction to Statics and Dynamics Problems_images/imageFile155.png)

0.5 m

45o

ω,α

A E

problem 10.22:

θ ω

(Filename:summer95f.4.a)

- A

r

- B D C


d

- 10.23 Collar A is constrained to slide on a horizontal rod to the right at constant speed


vA. It is connected by a pin joint to one end of a rigid bar AB with length which makes an angle θ with the horizontal at the instant of interest. A second collar B connected by a pin joint to the other end of the rigid bar AB slides on a vertical rod.

###### problem 10.28:

(Filename:pﬁgure.blue.120.1)

- a) Find the velocity of point B. Answer in terms of vA, θ, , ıˆ and ˆ.
- b) Find the angular speed θ˙ of the rod? Answer in terms of vA, θ, , ıˆ and ˆ.


10.29Pickingapartthepolarcoordinateformula for velocity. See also problems 10.30 and11.52. Thisproblemconcernsasmallmass m that sits in a slot in a turntable. Alternatively you can think of a small bead that slides on a rod. The mass always stays in the slot (or on the rod). Assume the mass is a little bug that can walk as it pleases on the rod (or in the slot) and you control how the turntable/rod rotates. Name two situations in which one of the terms is zero but the other is not in the two term polar coordinate formula for velocity, R˙eˆR + Rθ˙eˆθ. You should thus gain some insight into the meaning of each of the two terms in that formula. ∗

###### nˆ λˆ

B

y

at a constant speed vA along the (frictionless) horizontal ground.

x

- a) For the position shown (where P is directly above the contact point), ﬁnd P’s

velocity vP and the rod’s angular velocity ω.

- b) Find P’s acceleration aP and the angular acceleration α of the rod.


B

C

A

###### problem 10.23:

(Filename:s93q5)

y

10.37 Double pendulum, Again. For the double pendulum in problem 10.36, φ¨1 and φ¨2 are also known at the instant shown. For the instant shown, answer the following questions in terms of , φ1, φ˙1, φ¨1, φ2, φ˙2, and φ¨2.

- b) problem 5.83,
- c) problem 10.5,
- d) problem 5.85,
- e) problem 5.84, and
- f) problem 5.82.


Top view

###### ω

- a) What is the absolute acceleration of point A?
- b) What is the acceleration of point B relative to point A?
- c) What is the absolute acceleration of point B?


x

- 10.34 A particle travels at non-constant speed on an elliptical path given by y2 = b2(1 − x2 a2 ). Carefully sketch the ellipse for particular values of a and b. For various positions of the particle on the path, sketch the position vector r(t); the polar coordinate basis vectors eˆr and eˆθ; and the path coordinate basis vectors eˆn and eˆt. At what points on the path are eˆr and eˆn parallel(or eˆθ and eˆt parallel)?

- 10.35 For the conﬁguration in problem 9.12,

taking ω2 to be the angular velocity of disk D relative to the rod, what is the absolute angular acceleration of the disk, D? What is the absolute angular acceleration of the disk if ω1 and ω2 are not constant?

C

O

r

disk D

P

L

θ

ω1

ω2

problem 10.35:

(Filename:doublerot.ang.accel)

- 10.36 Double pendulum. See also problem 10.37. The double pendulum shown is made up of two uniform bars, each of length


O

Top view

y

ω

![image 156](Introduction to Statics and Dynamics Problems_images/imageFile156.png)

![image 157](Introduction to Statics and Dynamics Problems_images/imageFile157.png)

φ1

![image 158](Introduction to Statics and Dynamics Problems_images/imageFile158.png)

![image 159](Introduction to Statics and Dynamics Problems_images/imageFile159.png)

A

x

φ2

problem 10.29:

(Filename:pﬁgure.s94h9p4b)

B

problem 10.37:

- 10.30 Picking apart the polar coordinate formula for acceleration. Reconsider the conﬁgurations in problem 10.29. This time, name four situations in which all of the terms, but one, in the four term polar coordinate for-

mula for acceleration, a = (R¨ − Rθ˙2)eˆR + (2R˙θ˙+Rθ)¨ eˆθ, are zero. Each situation should pick out a different term. You should thus gain some insight into the meaning of each of the four terms in that formula. ∗

- 10.31 For the conﬁguration in problem 9.12 whatistheabsoluteangularvelocityofthedisk, D? ∗

C

O

r

disk D

P

L

θ

ω1

ω2

problem 10.31:

(Filename:doublerot1)

- 10.32 A car driver on a very boring highway is carefully monitoring her speed. Over a one hour period, the car travels on a curve with constant radius of curvature, ρ = 25mi, and its speed increases uniformly from 50mph to 60mph. What is the acceleration of the of the car half-way through this one hour period, in path coordinates?
- 10.33 Find expressions for eˆt, at, an, eˆn, and the radius of curvature ρ, at any position (or time) on the given particle paths for


(Filename:ch7.8.a)

and mass m. At the instant shown, φ1, φ˙1, φ2, and φ˙2 are known. For the instant shown, answer the following questions in terms of , φ1, φ˙1, φ2, and φ˙2.

- a) What is the absolute velocity of point A?
- b) What is the velocity of point B relative to point A?
- c) What is the absolute velocity of point B?


O

φ1

A

φ2

B

problem 10.36:

a) problem 5.81, ∗

(Filename:ch7.8)

Mechanics of planar mechanisms

##### 11.1 Dynamics of particlesin the context of 2D mech-anisms

- 11.1 Several of the problems below concern a narrow rigid hoop and/or a small bead. For reference here are dimensions and values you should use in working the problems: mass of bead mbead = 2grams, mass of hoop mhoop = 1kg, radiusofhoop Rhoop = 3m, gravitational


acceleration g = 10m/s2 (or zero). A bead slides on a frictionless circular hoop . The center of the circular hoop is the origin O of a ﬁxed (Newtonian) coordinate system Oxyz. The hoop is on the xy plane. Gravity is in the negative z direction. The hoop is kept from moving by little angels who arrange to let the bead slide by unimpeded. At t = 0, the speed of the bead is 4m/s, it is traveling counterclockwise (looking down the z-axis), and it is on the x-axis. There are no external forces applied.

- a) At t = 0 what is the bead’s kinetic energy ?
- b) At t = 0 what is the bead’s linear momentum ?
- c) At t = 0 what is the bead’s angular momentum about the origin?
- d) At t = 0 what is the bead’s acceleration?
- e) At t = 0 what is the radius of the osculating circle of the bead’s path ρ?
- f) At t = 0 what is the force of the hoop on the bead?
- g) At t = 0 what is the net force of the angel’s hands on the hoop?
- h) At t = 27s what is the x-component of the bead’s linear momentum?


Just when the bead above has traveled around the wire exactly 12 times the angels suddenly (but gently) let go of the hoop which is now free to slide on the frictionless xy plane. Call this time t = 0. At t = 0+ we can assume the angels have fully let go.

- i) Att = 0+ whatisthelinearmomentum of the bead and hoop system?
- j) At t = 0+ what is the rate of change of the linear momentum of the bead and hoop system?


k) At t = 0+ What is the value of the accelerationofthebead? (Hint:abead = ahoop center + abead/hoop center)

- 11.2 A warehouse operator wants to move a crate of weight W = 100lb from a 6ft high platform to ground level by means of a roller conveyer as shown. The rollers on the inclined planearewelllubricatedandthusassumedfrictionless; the rollers on the horizontal conveyer are frictional, thus providing an effective frictioncoefﬁcientµ. Assumetherollersaremassless.

- a) What are the kinetic and potential energies(pick a suitable datum) of the crate at the elevated platform, point A?
- b) What are the kinetic and potential energies of the cart at the end of the inclined plane just before it moves onto the horizontal conveyor, point B.
- c) Using conservation of energy, calculate the maximum speed attained by the crate at point B, assuming it starts moving from rest at point A.
- d) If the crate slides a distance x, say, on the horizontal conveyor, what is the energy lost to sliding in terms of µ, W, and x?
- e) Calculate the value of the coefﬁcient of friction, µ, such that the crate comes to rest at point C.


24 ft 8 ft

A 6 ft

100 lb

frictional C B

frictionless

problem 11.2:

(Filename:pﬁgure.blue.30.1)

- 11.3 On a wintry evening, a student of mass m starts down the steepest street in town, Steep Street, which is of height h and slope θ. At the top of the slope she starts to slide (coefﬁcient of dynamic friction µ).


- a) What is her initial kinetic and potential energy?
- b) What is the energy lost to friction as she slides down the hill?
- c) What is her velocity on reaching the bottom of the hill? Ignore air resistance and all cross streets (i.e. assume the hill is of constant slope).
- d) If, upon reaching the bottom of the street, she collides with another student of mass M and they embrace, what is their instantaneous mutual velocity just after the embrace?


e) Assuming that friction still acts on the level ﬂats on the bottom, how much time will it take before they come to rest?

m

Steep St.

h

M θ

x

problem 11.3:

(Filename:pﬁgure.blue.25.2)

- 11.4 Reconsider the system of blocks in problem 3.30, this time with equal mass, m1 = m2 = m. Also, now, both blocks are frictional and sitting on a frictional surface. Assume that both blocks are sliding to the right with the top block moving faster. The coefﬁcient of friction

between the two blocks is µ1. The coefﬁcient offrictionbetweenthelowerblockandtheﬂoor

is µ2. It is known that µ1 > 2µ2.

- a) Draw free body diagrams of the blocks together and separately.
- b) Write the equations of linear momentum balance for each block.
- c) Find the acceleration of each block for the case of frictionless blocks. For the frictional blocks, ﬁnd the acceleration of each block. What happens if µ1 >> µ2?


- 11.5 An initially motionless roller-coaster car of mass 20 kg is given a horizontal impulse


F dt = Pi at position A, causing it to move along the track, as shown below.

- a) Assuming that the track is perfectly frictionless from point A to C and that thecarneverleavesthetrack, determine the magnitude of the impulse I so that the car “just makes it” over the hill at B.
- b) In the ensuing motion, assume that the horizontal track C − D is frictional and determine the coefﬁcient of friction required to bring the car to a stop a D.


g µ=?

B 10 m

20 m

C D

y

ˆ

30 m

x

A

ıˆ

problem 11.5:

(Filename:pﬁgure.blue.21.2)

bug

- 11.6 Masses m1 = 1kg and m2 kg move on the frictionless varied terrain shown. Initially,

m1 has speed v1 = 12m/s and m2 is at rest. The two masses collide on the ﬂat section. The coefﬁcient of restitution in the collision is e = 0.5. Find the speed of m2 at the top of the ﬁrst hill of elevation h1 = 1m. Does m2 make it over the second hill of elevation h2 = 4m?

m1 m2

v1

g

- h1
- h2


problem 11.6:

(Filename:Danef94s2q7)

- 11.7 The two differential equations:

R¨ − Rθ˙2 = 0 2R˙θ˙ + Rθ¨ = 0

have the general solution

R = d2 + (v(t − t0))2 θ = θ0 + tan−1(v(t − t0)/d)

where θ0, d, t0, and v are arbitrary constants. This solution could be checked by plugging backintothedifferentialequations—youneed not do this (tediousl) substitution. The solution describes a curve in the plane. That is, if for a range of values of t, the values of R and θ were calculated and then plotted using polar coordinates, a curve would be drawn. What can you say about the shape of this curve?

[Hints:

- a) Actually make a plot using some random values of the constants and see what the plot looks like.
- b) Write the equation F = ma for a particle in polar coordinates and think of a force that would be relevant to this problem.
- c) The answer is something simple. ]


- 11.8 A scotch yoke, a device for converting rotary motion into linear motion, is used to make a horizontal platform go up and down. The motion of the platform is y = A sin(ωt) with constant ω. A dead bug with mass m is standing on the platform. Her feet have no glue on them. There is gravity.


- 11.11 (See also problem 11.10.) A newer kind of gun. As an attempt to make an improvement on the ‘new gun’ demonstrated in

problem 11.9, a person adds a length 0 to the shaft on which the bead slides. Assume there is no friction between the bead (mass m) and the wire. Assume the bead starts at l = 0 with l˙ = v0. Therigidrod, onwhichthebeadslides, rotates at a constant rate ω = ω0. Find l(t) in terms of 0,m,v0, and ω0.

| | | |
|---|---|---|
| | | |


l ω

problem 11.11:

(Filename:pﬁgure.s94f1p5)

- 11.12 Abugofmassm walksstraight-forwards

with speed vA and rate of change of speed v˙A on a straight light (assumed to be massless) stick. The stick is hinged at the origin so that it is always horizontal but is free to rotate about the z axis. Assume that the distance the bug is from the origin , , the angle the stick makes with the x axis, φ, and its rate of change, φ˙, are known at the instant of interest. Ignore gravity. Answer the following questions in terms of φ, φ˙, , m, vA, and v˙A.

- a) What is φ¨?
- b) What is the force exerted by the rod on the support?
- c) What is the acceleration of the bug?


x

y

O

A

φ,φ˙

bug, m

massless rod

frictionless hinge

problem 11.12:

(Filename:pﬁgure.blue.55.1)

- 11.13 Slippery bead on straight rotating


platform

y

g

A Peg fixed

to disc ω

problem 11.8:

(Filename:pﬁgure.blue.34.1)

###### 11.9 A new kind of gun. See also prob-

lems 11.10 and 11.11. Assume ω = ω0 is a constant for the rod in the ﬁgure. Assume the massisfreetoslide. Att = 0, therodisaligned withthe x-axisandthebeadisonefootfromthe origin and has no radial velocity (dR/dt = 0).

- a) Find a differential equation for R(t). ∗
- b) Turn this equation into a differential equation for R(θ). ∗
- c) How far will the bead have moved after onerevolutionoftherod? Howfarafter two? ∗
- d) What is the speed of the bead after

one revolution of the rod (use ω0 = 2π rad/s = 1rev/sec)? ∗

- e) Howmuchkineticenergydoesthebead have after one revolution and where did it come from? ∗


y

ω R

![image 160](Introduction to Statics and Dynamics Problems_images/imageFile160.png)

![image 161](Introduction to Statics and Dynamics Problems_images/imageFile161.png)

![image 162](Introduction to Statics and Dynamics Problems_images/imageFile162.png)

![image 163](Introduction to Statics and Dynamics Problems_images/imageFile163.png)

θ

x

problem 11.9:

(Filename:pﬁgure.s94h9p5)

###### 11.10 The new gun gets old and rusty. (Seealso problem 11.11.) Reconsider the bead on arod in problem 11.9. This time, friction cannotbe neglected. The friction coefﬁcient is µ. Atthe instant of interest the bead with mass m has

- a) Draw a free body diagram of the bug.
- b) What is the acceleration of the platform and, hence, the bug?
- c) Write the equation of linear momentum balance for the bug.
- d) What condition must be met so that the bug does not bounce the platform?
- e) What is the maximum spin rate ω that can be used if the bug is not to bounce off the platform?


radius R0 with rate of change R˙0. The angle θ is zero and ω is a constant. Neglect gravity.

stick. A long stick with mass ms rotates at a constant rate and a bead, modeled as a point mass, slides on the stick. The stick rotates at constant rate ω = ωkˆ. There is no gravity. The bead has mass mb. Initially the mass is at a distance R0 from the hinge point on the stick and has no radial velocity (R˙ = 0). The initial angle of the stick is θ0, measured counterclockwise from the positive x axis.

- a) What is R¨ at this instant? Give your answer in terms of any or all of R0, R˙0, ω, m, µ, eθ, eR, ıˆ, and ˆ. ∗
- b) Afteraverylongtimeitisobservedthat theangleφ betweenthepathofthebead and the rod/trough is nearly constant. What, in terms of µ, is this φ? ∗


- R˙ = 0 at t = 0, what are the components of the acceleration vector in the directions normal and tangential to the path of the bead after one revolution? Neglect gravity.
- 11.16 A bead of mass m = 1gm bead is constrained to slide in a straight frictionless slot in a disk which is spinning counterclockwise at constant rate ω = 3rad/s per second. At time t = 0, the slot is parallel to the x-axis and the bead is in the center of the disk moving out

(in the plus x direction) at a rate R˙o = .5m/s. After a net rotation θ of one and one eighth

(1.125) revolutions, what is the force F of the disk on the bead? Express this answer in terms ofıˆ andˆ. Make the unreasonable assumption that the slot is long enough to contain the bead for this motion.

x

y

ω

problem 11.16:

(Filename:pﬁgure.f93q11)

- 11.17 Bead on springy leash in a slot on a turntable. The bead in the ﬁgure is held by a spring that is relaxed when the bead is at the origin. The constant of the spring is k. The turntable speed is controlled by a strong stiff motor.

- a) Assume ω = 0 for all time. What are possible motions of the bead?
- b) Assumeω = ω0 isaconstant. Whatare possible motions of the bead? Notice there are two cases depending on the value of ω0. What is going on here?


O

x

y

ω

problem 11.17: Mass in a slot.

(Filename:pg57.1a)

- 11.18 A small bead with mass m slides without friction on a rigid rod which rotates about the z axis with constant ω (maintained by a stiff motor not shown in the ﬁgure). The bead is also attached to a spring with constant K, the


other end of which is attached to the rod. The spring is relaxed when the bead is at the center position. Assume the bead is released pulled to a distance d from the center of the rod and then released with an initial R˙ = 0. If needed, you may assume that K > mω2.

- a) What is the torque, as a function of the

net angle the stick has rotated, θ − θ0, required in order to keep the stick rotating at a constant rate ?

- b) What is the path of the bead in the xyplane? (Drawanaccuratepictureshowing about one half of one revolution.)
- c) How long should the stick be if the bead istoﬂyinthenegative x-directionwhen it gets to the end of the stick?
- d) Add friction. How does the speed of the bead over one revolution depend on µ, the coefﬁcient of friction between the bead and the wire? Make a plot of

| vone revolution|versusµ. [Note, you have been working with µ = 0 in the

problems above.]

- e) A ﬁnite rigid body. What would change if instead of a point mass you modeled the bead as a ﬁnite rigid body (2-D), with center of mass on the stick, but contact at various places on the stick? (Do the frictionless case only.)


- a) Derive the equation of motion for the position of the bead R(t).
- b) Howisthemotionaffectedbylargeversus small values of K?
- c) What is the magnitude of the force of the rod on the bead as the bead passes through the center position? Neglect gravity. Answer in terms of m, ω, d, K.
- d) Write an expression for the Coriolis acceleration. Give an example of a situation in which this acceleration is important and explain why it arises.


y

ω = constant

![image 164](Introduction to Statics and Dynamics Problems_images/imageFile164.png)

![image 165](Introduction to Statics and Dynamics Problems_images/imageFile165.png)

- 11.14 Mass on a lightly greased slotted turntable or spinning uniform rod. Assume that the rod/turntable in the ﬁgure is massless and also free to rotate. Assume that at t = 0, the angular velocity of the rod/turntable is 1rad/s, that the radius of the bead is one meter, and that the radial velocity of the bead, dR/dt, is zero. The bead is free to slide on the rod. Where is the bead at t = 5sec?

Top view

Top view

x

y

ω

![image 166](Introduction to Statics and Dynamics Problems_images/imageFile166.png)

![image 167](Introduction to Statics and Dynamics Problems_images/imageFile167.png)

x

y

![image 168](Introduction to Statics and Dynamics Problems_images/imageFile168.png)

![image 169](Introduction to Statics and Dynamics Problems_images/imageFile169.png)

ω

problem 11.14:

(Filename:pﬁgure.s94h9p4a)

- 11.15 A bead slides in a frictionless slot in a turntable. Theturntablespinsaconstantrateω. The slot is straight and goes through the center of the turntable. If the bead is at radius Ro with


![image 170](Introduction to Statics and Dynamics Problems_images/imageFile170.png)

![image 171](Introduction to Statics and Dynamics Problems_images/imageFile171.png)

O

x

problem 11.18:

(Filename:pﬁgure.s94q9p1)

11.19 A small ball of mass mb = 500 grams may slide in a slender tube of length l = 1.2m.

and of mass mt = 1.5kg. The tube rotates freely about a vertical axis passing through its centerC.(Hint: Treatthetubeasaslenderrod.)

- a) If the angular velocity of the tube is ω = 8rad/s as the ball passes through

C with speed relative to the tube, v0, calculate the angular velocity of the tube just before the ball leaves the tube. ∗

- b) Calculate the angular velocity of the

tube just after the ball leaves the tube.

∗

- c) If the speed of the ball as it passes Cis v = 1.8m/s, determine the transverse andradialcomponentsofvelocityofthe ball as it leaves the tube. ∗
- d) After the ball leaves the tube, what constant torque must be applied to the tube (about its axis of rotation) to bring it to rest in 10s? ∗


A

eˆθ eˆr

y

- b) the absolute acceleration of the mass at the instant of cutting, ∗
- c) the tension in string BC at the instant of cutting. ∗


ω

m

y

![image 172](Introduction to Statics and Dynamics Problems_images/imageFile172.png)

C

![image 173](Introduction to Statics and Dynamics Problems_images/imageFile173.png)

![image 174](Introduction to Statics and Dynamics Problems_images/imageFile174.png)

![image 175](Introduction to Statics and Dynamics Problems_images/imageFile175.png)

g

C

C

A

L

B

2/3L 1/3L

B

###### ˆ

problem 11.19:

θ

A

(Filename:pﬁgure.blue.91.1)

2L

x

ıˆ

- 11.20 Toy train car on a turn-around. The 0.1kg toy train’s speedometer reads a constant 1m/s when, heading west, it passes due north of point O. The train is on a level straight track which is mounted on a spinning turntable whose center is ‘pinned’ to the ground. The turntable spins at the constant rate of 2rad/s. What is the force of the turntable on the train? (Don’t worry about the z-component of the force.) ∗

toy train

O

North

ıˆ

0.5m ˆ

turntable

ω = 2 rad/s

one way

problem 11.20:

(Filename:pﬁgure.s94h12p1)

- 11.21 A shell moves down a barrel. At the instant of interest the barrel is being raised at

a constant angular speed ω1. Simultaneously the gun turret (the structure which holds the barrel) rotates about the vertical axis at a constant rate ω2. At the instant of interest, the barrel is tipped up an angle θ and the mass m is moving at speed v along the frictionless barrel. Neglecting gravity, ﬁnd the force of the barrel on the shell.

O

θ

vo

z x

y turret

shell

problem 11.21: A shell moves along a canon barrel.

(Filename:pg122.2)

- 11.22 Due to forces not shown, the cart moves to the right with constant acceleration ax. The


problem 11.22:

problem 11.24: Rod on a Moving Support(2-D).

(Filename:Danef94s1q6)

(Filename:p3.1)

- 11.25 Balancing a broom. Assume the hand is accelerating to the right with acceleration a = aıˆ. What is the force of the hand on the broom in terms of m,  , θ, θ,˙ a, ıˆ, ˆ, and

g? (You may not have any eˆR or eˆθ in your answer.)

C

A

![image 176](Introduction to Statics and Dynamics Problems_images/imageFile176.png)

![image 177](Introduction to Statics and Dynamics Problems_images/imageFile177.png)

x

y

eˆθ eˆr

m

g

θ

ıˆ

ˆ

problem 11.25:

(Filename:p.f96.f.2)

11.2 Dynamics of rigid bodies in one-degreeof-freedom mechanisms

- 11.26 A conservative vibratory system has the following equation of conservation of energy. m(Lθ)˙ 2−mgL(1−cosθ)+K(aθ)2 = Constant

- a) Obtain the differential equation of motion of this system by differentiating this energy equation with respect to t.
- b) Determine the circular frequency of small oscillations of the system in part (a). HINT: (Let sin ∼= θ ∼= and cosθ ∼= 1 − θ2/2).


- 11.27 A motor at O turns at rate ωo whose rate of change is ω˙o. At the end of a stick connected to this motor is a frictionless hinge attached to a second massless stick. Both sticks have length L. At the end of the second stick is a mass


- 11.23 The forked arm mechanism pushes the bead of mass 1kg along a frictionless hyperbolic spiral track given by r = 0.5θ(m/rad). The arm rotates about its pivot point at O with constant angular acceleration θ¨ = 1rad/s2 driven by a motor (not shown). The arm starts from rest at θ = 0o.

- a) Determine the radial and transverse components of the acceleration of the beadafter2shaveelapsedfromthestart of its motion.
- b) Determine the magnitude of the net force on the mass at the same instant in time.


θ O

bead

hyperbolic spiral track

r

r=0.5θ radm

problem 11.23:

(Filename:pﬁgure.blue.53.1)

- 11.24 A rod is on the palm of your hand at point A. Its length is . Its mass m is assumed to be concentrated at its end at C. Assume that you know θ and θ˙ at the instant of interest. Also assume that your hand is accelerating both vertically and horizontally with


ahand = ahxıˆ+ahyˆ. Coordinates and directions are as marked in the ﬁgure.

- a) Draw a Free Body Diagram of the rod.
- b) Assume that the hand is stationary. Solve for θ¨ in terms of g, , m, θ, and θ˙.
- c) If the hand is not stationary but θ¨ has beendeterminedsomehow, ﬁndthevertical force of the hand on the rod in terms of θ¨, θ˙, θ, g, , m, ahx, and ahy.


ball B has mass mB. At time t = 0, the string AB is cut. Find

a) the tension in string BC before cutting,

∗

m. For the conﬁguration shown, what is θ¨? Answer in terms of ωo, ω˙o, L, m, θ, and θ˙. Ignore gravity.

L

m

θ

L

π/2 at time of interest

ωO,ω˙O

problem 11.27:

(Filename:pﬁgure.blue.119.1)

- 11.28 (See also problems 10.31 and 10.35.) In problem 9.12, ﬁnd

- a) the angular momentum about point O, ∗
- b) the rate of change of angular momentum of the disk about point O, ∗
- c) the angular momentum about point C, ∗
- d) the rate of change of angular momentum of the disk about point C. ∗


Assume the rod is massless and the disk has mass m.

C

O

r

disk D

P

L

θ

ω1

ω2

problem 11.28:

(Filename:doublerot.ang.mom)

- 11.29 Robot arm, 2-D . The robot arm AB is rotating about point A with ωAB = 5rad/s and ω˙ AB = 2rad/s2. Meanwhile the forearm BC is rotating at a constant angular speed with

respect to AB of ωBC/AB = 3rad/s. Gravity cannot be neglected. At the instant shown, ﬁnd the net force acting on the object P which has mass m = 1kg. ∗

x

y

| | |m|
|---|---|---|
| | | |


1m 2m

30o A

B

C

P

ωAB, ω˙AB

ωBC/AB

problem 11.29:

(Filename:pﬁgure.s94h12p5)

- 11.30 A crude model for a column, shown in the ﬁgure, consists of two identical rods of mass m and length with hinge connections, a linear torsional spring of stiffness K attached to the center hinge (the spring is relaxed when θ = 0), and a load P applied at the top end.


a) Obtain the exact nonlinear equation of motion.

- b) Obtain the squared natural frequency for small motions θ.
- c) Check the stability of the straight equilibrium state θ = 0 for all P ≥ 0 via minimum potential energy. How do these results compare with those from part(b)?


y

K

m, m,

P x

θ

problem 11.30:

(Filename:pﬁgure.blue.159.2)

11.31 A thin uniform rod of mass m rests against a frictionless wall and on a frictionless ﬂoor. There is gravity.

- a) Draw a free body diagram of the rod.
- b) The rod is released from rest at θ =

θ0  = 0. Write the equation of motion of the rod. ∗

- c) Using the equation of motion, ﬁnd the

initial angular acceleration, ω˙ AB, and the acceleration of the center of mass,

aG, of the rod. ∗

- d) Find the reactions on the rod at points A and B. ∗
- e) Find the acceleration of point B. ∗
- f) When θ = θ20, ﬁnd ωAB and the acceleration of point A. ∗


A

L G

| | |
|---|---|
| | |


θ B

problem 11.31:

(Filename:ch7.1)

11.32Barleansonacrookedwall. Auniform 3lbm bar leans on a wall and ﬂoor and is let go from rest. Gravity pulls it down.

- a) Draw a Free Body Diagram of the bar.
- b) Kinematics: ﬁnd the velocity and acceleration of point B in terms of the velocity and acceleration of point A
- c) Using equations of motion, ﬁnd the acceleration of point A.
- d) Do the reaction forces at A and B add up to the weight of the bar? Why or why not? (You do not need to solve for the reaction forces in order to answer this part.)


B

2.5 ft

30o 45o

A

problem 11.32:

(Filename:pﬁgure.s94h10p3)

- 11.33 Two blocks, each with mass m, slide without friction on the wall and ﬂoor shown. They are attached with a rigid massless rod of length that is pinned at both ends. The system is released from rest when the rod makes an angleof45◦. Whatistheaccelerationoftheblock B immediately after the system is released?

grease

![image 178](Introduction to Statics and Dynamics Problems_images/imageFile178.png)

massless rigid rod of length

|A<br><br>m|
|---|


![image 179](Introduction to Statics and Dynamics Problems_images/imageFile179.png)

|B<br><br>m|
|---|


π/4

grease

mA = mB = m

problem 11.33:

(Filename:pﬁgure.blue.98.2)

- 11.34 Slider Crank. 2-D . No gravity. Refer to the ﬁgure in problem 10.19. What is the tension in the massless rod AB (with length L) when the slider crank is in the position with θ = 0 (piston is at maximum extent)? Assume the crankshaft has constant angular velocity ω, that the connecting rod AB is massless, that the cylinder walls are frictionless, that there is no gas pressure in the cylinder, that the piston has mass M and the crank has radius R.

M

O

A

B

R L

motor

crank rod

piston

θ

ıˆ

ˆ

problem 11.34:

(Filename:slidercrank.tension)

- 11.35 In problem 10.25, ﬁnd the force on the wheel at point D due to the rod.


B

D

ω

r

O β

A

problem 11.35:

(Filename:roddisc.force)

- 11.36 In problem 10.26, ﬁnd the force on the rod at point P.

P

m R

M

L

θ vA

problem 11.36:

(Filename:rodcyl.force)

- 11.37 Slider-Crank mechanism. The slider crankmechanismshownisusedtopusha2lbm block P. Arm AB and BC are each 0.5ft long. Given that arm AB rotates counterclockwise at a constant 2 revolutions per second, what is the force on P at the instant shown? ∗

P A

B

C D

M N

60o 60o

problem 11.37:

(Filename:pﬁgure.s94h11p1)

- 11.38 Consider the 4-bar linkage AB, BC, CD and the ground DA. The bars are connected by well lubricated hinges at A, B, and C. At D, bar CD is driven by the motor which spins at constant rate. Do not ignore gravity.

- a) Draw a Free Body Diagram of the linkage ABCD (with ‘cuts’ at A and D but not at B and C.)
- b) Draw Free Body Diagrams of each of thebarsAB,BCandCD.Usethelawof action and reaction in these diagrams. If you can, do this problem a few times, each with a different vector notation.
- c) Repeat problem (b) but this time assume that the mass of bar BC is negligible. [Hint, this implies that the laws of statics apply to bar BC, which has connections at the two points B and C.]


.75m

A

B

C

D

motor turns bar CD

1m

π/4

α

problem 11.38: Free Body Diagram Exercise

(Filename:pﬁgure.s94h2p7)

- 11.39 Thelargemassesm atC and A weresupportedbythelighttriangularplateABC,whose corners follow the guide. B enters the curved guide with velocity V. Neglecting gravity, ﬁnd the vertical reactions (in the y direction) at A


and B. (Hint: for the rigid planar body ABC, ﬁnd y¨A and y¨B intermsofacmy andθ¨, assuming θ˙ = 0 initially.)

A

b B

m

a

V

y

m

C

R

x

problem 11.39:

(Filename:pﬁgure.blue.85.2)

- 11.40 An idealized model for a car comprises a rigid chassis of mass Mc and four identical rigid disks (wheels) of mass Mw and radius R, as shown in the ﬁgure. Initially in motion with

speed v0, the car is momentarily brought to rest by compressing an initially uncompressed spring of stiffness k. Assume no frictional losses.

- a) Assuming no wheel slip, determine the compression of the spring required to stop the car. ∗
- b) While the car is in contact with the spring but still moving forward, in which direction is the tangential force on any one of the wheels (due to contact with the ground) pointing? Why? (Illustrate with a sketch). ∗
- c) Repeat part (a) assuming now that the ground is perfectly frictionless from points A to B shown in the ﬁgure. ∗


k

A B

R

Vo Mc Mw

R

g

problem 11.40:

(Filename:pﬁgure.blue.135.2)

- 11.41 Whilewalkingdownaﬂatstretchofroad you see a dejected Greg Lemond riding by. His riding “tuck” is so good that you realize that you can totally neglect air resistance when you think about him and his bike. Further, you can regard his and the bike’s combined mass (all 70 kg)) as concentrated at a point in his stomach somewhere. Greg’s left foot has just fallen off the pedal so he is only pedaling with his right foot, which at the moment in question is at its lowest point in the motion. You note that, relative to the ground the right foot is only going 3/4 as fast as the bike (since it is going backwards relative to the bike), though you can’t make out all the radii of his frictionless gears and rigid round wheels. Greg, ever in touch with his body, tells you he is pushing back on the pedal with a force of 70 N. You would like to know Greg’s acceleration.


- a) In your ﬁrst misconceived experiment you set up a 70 kg bicycle in your laboratory and balance it with strings that cause no fore or aft forces. You tie a string to the vertically down right pedal andpullbackwithaforceof70N.What acceleration do you measure?
- b) What is Greg’s actual acceleration? [Hint: Greg’s massless leg is pushing forward on his body with a force of 70 N]


Lemond's stomach

problem 11.41:

(Filename:pﬁgure.blue.34.2)

- 11.42 Which way does the bike accelerate? Abicyclewithallfrictionlessbearingsisstanding still on level ground. A horizontal force F is applied on one of the pedals as shown. There is no slip between the wheels and the ground. The bicycle is gently balanced from falling over sideways. It is heavy enough so that both wheels stay on the ground. Does the bicycle accelerate forward, backward, or not at all? Make any reasonable assumptions about the dimensions and mass. Justify your answer as clearly as you can, clearly enough to convince a person similar to yourself but who has not seen the experiment performed.

F No slip

problem 11.42:

(Filename:pﬁgure.s94h14p2)

11.3 Dynamics of multidegree-of-freedom mechanisms

- 11.43 Particle on a springy leash. A particle with mass m slides on a rigid horizontal frictionless plane. It is held by a string which is in turn connected to a linear elastic spring with constant k. The string length is such that the spring is relaxed when the mass is on top of the hole in the plane. The position of the particle is r = xıˆ+yˆ. For each of the statements below, state the circumstances in which the statement is true (assuming the particle stays on the plane). Justify your answer with convincing explanation and/or calculation.


rest in the conﬁguration shown. [Hint: What is the acceleration of A relative to B?]

- a) The force of the plane on the particle is mgkˆ.
- b) x¨ + mk x = 0

- c) y¨ + mk y = 0

- d) r¨ + mk r = 0, where r = | r|

- e) r = constant
- f) θ˙ =constant
- g) r2θ˙ = constant.
- h) m(x˙2 + y˙2) + kr2 = constant
- i) Thetrajectoryisastraightlinesegment.
- j) The trajectory is a circle.
- k) The trajectory is not a closed curve.


- f) Express the conservation of energy in cartesian coordinates. ∗
- g) Express the conservation of energy in polar coordinates. ∗
- h) Show that (a) implies (f) and (b) implies (g) even if you didn’t note them a-priori. ∗
- i) Find the general motion by solving the equations in (a). Describe all possible paths of the mass. ∗
- j) Can the mass move back and forth on a line which is not the x or y axis? ∗


- a) Find the acceleration of point B just after the dumbell is released.
- b) Find the velocity of point A just before it hits the ﬂoor


A

###### ˆ

g ıˆ

y

θ B

x

###### problem 11.47:

(Filename:s97f5)

- 11.48 After a winning goal one second beforetheclockranoutapsychologicallystunned hockey player (modeled as a uniform rod) standsnearlyvertical, stationaryandrigid. The playersperfectlyslipperyskatesstarttopopout from under her as she falls. Her height is , her mass m, her tip from the vertical θ, and the gravitational constant is g.

- a) What is the path of her center of mass as she falls? (Show clearly with equations, sketches or words.)
- b) What is her angular velocity just before she hits the ice, a millisecond before she sticks our her hands and brakes her fall (ﬁrst assume her skates remain in contact the whole time and then check the assumption)?
- c) Findadifferentialequationthatonlyinvolves θ, its time derivatives, m, g, and


. (This equation could be solved to ﬁnd θ as a function of time. It is a nonlinear equation and you are not being asked to solve it numerically or otherwise.)

- 11.49 Falling hoop. A bicycle rim (no spokes, tube, tire, or hub) is idealized as a hoop with mass m and radius R. G is at the center of the hoop. An inextensible string is wrapped around the hoop and attached to the ceiling. The hoop is released from rest at the position shown at t = 0.


- x

m

k

- y v0 θ


kˆ ˆ

O

ıˆ

problem 11.45:

problem 11.43: Particle on a springy leash.

(Filename:pﬁgure.blue.73.1)

- 11.46 Cart and pendulum A mass mB = 6kg hangs by two strings from a cart with mass

mC = 12kg. Before string BC is cut string AB is horizontal. The length of string AB is r = 1m. At time t = 0 all masses are stationary and the string BC is cleanly and quietly cut. After some unknown time tvert the string AB is vertical.

- a) What is the net displacement of the cart xC at t = tvert? ∗
- b) What is the velocity of the cart vC at t = tvert? ∗
- c) What is the tension in the string at t = tvert? ∗
- d) (Optional)Whatist = tvert? [Youwill either have to leave your answer in the form of an integral you cannot evaluate analytically or you will have to get part of your solution from a computer.]


|A<br><br>C<br><br>B r<br><br>strings<br><br>mC<br><br>x mB<br><br>y<br><br>|
|---|


problem 11.46:

(Filename:pﬁgure.s94h12p3)

- 11.47 A dumbell slides on a ﬂoor. Two point masses m at A and B are connected by a massless rigid rod with length . Mass B slides on a frictionless ﬂoor so that it only moves horizontally. Assume this dumbell is released from


(Filename:pg69.1)

- 11.44 “Yo-yo” mechanism of satelite despinning. A sattelite, modeled as a uniform disk, is“de-spun”bythefollowingmechanism. Before launch two equal length long strings are attached to the sattelite at diametrically opposite points and then wound around the sattelite with the same sense of rotation. At the end of the strings are placed 2 equal masses. At the startofde-spinningthetwomassesarereleased fromtheirpositionwrappedagainstthesatelite. Find the motion of the sattelite as a function of time for the two cases: (a) the strings are wrappedinthesamedirectionastheinitialspin, and (b) the strings are wrapped in the opposite direction as the initial spin.
- 11.45 A particle with mass m is held by two long springs each with stiffness k so that the springs are relaxed when the mass is at the origin. Assume the motion is planar. Assume that the particle displacement is much smaller than the lengths of the springs.


- a) Find yG at a later time t in terms of any or all of m, R, g, and t.
- b) Does G movesidewaysasthehoopfalls and unrolls?


- a) Write the equations of motion in cartesian components. ∗
- b) Write the equations of motion in polar coordinates. ∗
- c) Express the conservation of angular momentum in cartesian coordinates. ∗
- d) Express the conservation of angular momentum in polar coordinates. ∗
- e) Show that (a) implies (c) and (b) implies (d) even if you didn’t note them a-priori. ∗


![image 180](Introduction to Statics and Dynamics Problems_images/imageFile180.png)

yG

m,R

###### problem 11.49:

(Filename:p.s96.p3.2)

|%newgunscript.m quiz 13 soln - A Ruina 4/27/95 z0 = [0,3,1,0]; % [Theta, omega, R, v] tfinal = 10000 ; tol = 1e-7 ;<br><br>[t,z] = ode45(’newgunfun’, 0, tfinal, z0, tol); thetamax=max(z(:,1));<br><br>plot(log10(t),z(:,1)); title(’andys plot’); xlabel(’log10 (time)’); ylabel(’theta’); axis([-5, log10(tfinal), 0 3])<br><br>text(-4.5,2.5 ,[’theta max= ’ ,num2str(thetamax,9)] ) text(-4.5,2.25,[’tol = ’ ,num2str(tol,9)] ) text(-4.5,2, [’tfinal = ’ ,num2str(tfinal,9)] )|
|---|


- 11.50 A model for a yo-yo comprises a thin disk of mass M and radius R and a light drum of radius r, rigidly attached to the disk, around which a light inextensible cable is wound. Assuming that the cable unravels without slipping

on the drum, determine the acceleration aG of the center of mass.

R M

G

r

ıˆ ˆ

g

problem 11.50:

(Filename:pﬁgure.blue.41.2)

- 11.51 A uniform rod with mass mR pivots without friction about point A in the xy-plane.

A collar with mass mC slides without friction on the rod after the string connecting it to point A is cut. There is no gravity. Before the string is cut, the rod has angular velocity ω1.

- a) What is the speed of the collar after it ﬂies off the end of the rod? Use the following values for the constants and initial conditions: mR = 1kg, mC = 3kg, a = 1m, = 3m, and ω1 = 1rad/s
- b) Consider the special case mR = 0. Sketch (approximately) the path of the motion of the collar from the time the string is cut until some time after it leaves the end of the rod.


![image 181](Introduction to Statics and Dynamics Problems_images/imageFile181.png)

![image 182](Introduction to Statics and Dynamics Problems_images/imageFile182.png)

![image 183](Introduction to Statics and Dynamics Problems_images/imageFile183.png)

A

a uniform rod, mass mR

string

collar, mass mC x

y ω

![image 184](Introduction to Statics and Dynamics Problems_images/imageFile184.png)

![image 185](Introduction to Statics and Dynamics Problems_images/imageFile185.png)

problem 11.51:

(Filename:pﬁgure.blue.54.1)

- 11.52 (See also problem 11.53. ) Assume the rod in the ﬁgure for problem 10.29 has polar moment of inertia Iozz. Assume it is free to rotate. The bead is free to slide on the rod. Assume that at t = 0 the angular velocity of the rod is 1rad/s, that the radius of the bead is one meter and that the radial velocity of the bead, dR/dt, is zero.


- a) Draw separate free body diagrams of the bead and rod.
- b) Write equations of motion for the system. ∗
- c) Use the equations of motion to show

that angular momentum is conserved.

∗

- d) Findoneequationofmotionforthesystem using: (1) the equations of motion for the bead and rod and (2) conservation of angular momentum. ∗
- e) Write an expression for conservation of energy. Lettheinitialtotalenergyofthe system be, say, E0. ∗
- f) As t goes to inﬁnity does the bead’s distance go to inﬁnity? Its speed? The angular velocity of the turntable? The net angle of twist of the turntable? ∗


|function zdot=newgunfun(t,z) m=.25; I=2;<br><br>theta = z(1); omega = z(2); R = z(3); v = z(4);<br><br>zdot = [ omega,<br><br>-2*m*omega*R*v/(I + m*Rˆ2), v, omegaˆ2* R ];|
|---|


y

Top view

###### ω

andys plot

theta max= 2.52859593 tol = 1e-07 tfinal = 10000

x

theta

- 0

- 0.5

- 1

1.5

2

- 2.5

- 3




-5 -4 -3 -2 -1 0 1 2 3 4

log10 (time)

Top view

y

###### problem 11.53:

(Filename:q13soln)

ω

![image 186](Introduction to Statics and Dynamics Problems_images/imageFile186.png)

![image 187](Introduction to Statics and Dynamics Problems_images/imageFile187.png)

![image 188](Introduction to Statics and Dynamics Problems_images/imageFile188.png)

![image 189](Introduction to Statics and Dynamics Problems_images/imageFile189.png)

x

11.54 A primitive gun rides on a cart (mass M) and carries a cannon ball (of mass m) on a platform at a height H above the ground. The cannon ball is dropped through a frictionless tube shaped like a quarter circle of radius R.

problem 11.52: Coupled motion of bead and rod and turntable.

(Filename:pﬁgure.s94h9p4b.a)

- a) If the system starts from rest, computethehorizontalspeed(relativetothe ground) that the cannon ball has as it leaves the bottom of the tube. Also ﬁnd the cart’s speed at the same instant.
- b) Computethevelocityofthecannonball relative to the cart.
- c) If two balls are dropped simultaneously through the tube, what speed does the cart have when the balls reach the bottom? Is the same ﬁnal speed also achieved if one ball is allowed to depart the system entirely before the second ball is released? Why/why not?


11.53 Numerically simulate the coupled system in problem 11.52. Use the simulation to show that the net angle of the turntable or rod is ﬁnite.

- a) Write the equations of motion for the system from part (b) in problem 11.52 as a set of ﬁrst order differential equations. ∗
- b) Numerically integrate the equations of motion. (Below, we show a solution using MATLAB.)


m

| |R|
|---|---|
|L<br><br>M| |


H

problem 11.54:

(Filename:pﬁgure.blue.18.1)

- 11.55 Two frictionless prisms of similar right triangular sections are placed on a frictionless horizontal plane. The top prism weighs W and the lower one nW. The prisms are held in the initial position shown and then released, so that the upper prism slides down along the lower one until it just touches the horizontal plane. The center of mass of a triangle is located at one-third of its height from the base. Compute the velocities of the two prisms at the moment

just before the upper one reaches the bottom.

∗

a

b

W

nW

φ

φ

problem 11.55:

(Filename:pﬁgure.blue.28.2a)

- 11.56 Mass slides on an accelerating cart. 2D. A cart is driven by a powerful motor to move along the 30◦ sloped ramp according to the formula: d = d0 + vot + a0t2/2 where d0, v0, and a0 are given constants. The cart is held from tipping over. The cart itself has a 30◦ sloped upper surface on which rests a mass (givenmassm). Thesurfaceonwhichthemass rests is frictionless. Initially the mass is at rest with regard to the cart.


- a) What is the force of the cart on the mass? [in terms of g,d0,v0,t,a0,m,g,ıˆ, and ˆ.] ∗
- b) For what values of d0, v0, t anda0 is the accelerationofthemassexactlyvertical (i.e., in the ˆ direction)? ∗


motor driven wheels

###### ˆ

µ = 0

ıˆ

30o

d g

30o

###### problem 11.56:

(Filename:pﬁgure.s95q11)

- 11.57 A thin rod AB of mass WAB = 10lbm and length LAB = 2ft is pinned to a cart C of mass WC = 10lbm, the latter of which is free to move along a frictionless horizontal surface, as shown in the ﬁgure. The system is released fromrestwiththerodinthehorizontalposition.

- a) Determine the angular speed of the rod asit passes through the vertical position (at some later time). ∗
- b) Determine the displacement x of the cart at the same instant. ∗
- c) After the rod passes through vertical, it is momentarily horizontal but on the left side of the cart. How far has the cart moved when this conﬁguration is reached?


|B| |
|---|---|
|released| |


x

from rest

A

- A

C

- B
- C


some later time

not to scale

problem 11.57:

(Filename:pﬁgure.blue.115.3)

- 11.58 As shown in the ﬁgure, a block of mass m rolls without friction on a rigid surface and is at position x (measured from a ﬁxed point). Attached to the block is a uniform rod of length


which pivots about one end which is at the center of mass of the block. The rod and block have equal mass. The rod makes an angle θ with the vertical. Use the numbers below for the values of the constants and variables at the time of interest:

= 1m

m = 2kg θ = π/2

dθ/dt = 1rad/s d2θ/dt2 = 2rad/s2 x = 1m dx/dt = 2m/s d2x/dt2 = 3m/s2

- a) What is the kinetic energy of the system?
- b) What is the linear momentum of the system (momentum is a vector)?


g

y θ

uniform rod, mass m

pin connection

A m frictionless, massless rollers

x

problem 11.58:

(Filename:pﬁgure.blue.14.1)

- 11.59 A pendulum of length hangs from a cart. The pendulum is massless except for a point mass of mass mp at the end. The cart rolls without friction and has mass mc. The cart is initially stationary and the pendulum is released from rest at an angle θ. What is the acceleration of the cart just after the mass is released? [Hints: aP = aC + aP/C. The answeris aC = (g/3)iinthespecialcasewhen mp = mc and θ = π/4. ]

C

P

mC

mP

θ

ıˆ

ˆ

problem 11.59:

(Filename:pﬁgure.f93q12)

- 11.60 Due to the application of some unknown force F, the base of the pendulum A is accel-

erating with aA = aAi. There is a frictionless hinge at A. The angle of the pendulum θ with the x axis and its rate of change θ˙ are assumed to be known. The length of the massless pendulum rod is . The mass of the pendulum bob M. There is no gravity. What is θ¨? (Answer in terms of aA, , M, θ and θ˙.)

F

A

M

θ

x

y

problem 11.60:

(Filename:pﬁgure.blue.115.2)

- 11.61 Pumping a Swing Can a swing be pumped by moving the support point up and down?


For simplicity, neglect gravity and consider the problem of swinging a rock in circles on a string. Let the rock be mass m attached to a string of ﬁxed length . Can you speed it up bymovingyourhandupanddown? How? Can you make a quantitative prediction? Let xS be a function of time that you can specify to try to make the mass swing progressively faster.

xs

L

θ

m

problem 11.61:

(Filename:pﬁgure.blue.59.1)

- 11.62 Using free body diagrams and appropriate momentum balance equations, ﬁnd differential equations that govern the angle θ and the vertical deﬂection y of the system shown. Be clear about your datum for y. Your equations should be in terms of θ, y and their timederivatives, as well as M,m, , and g.

M

m

k

θ

problem 11.62:

(Filename:pﬁg2.1.rp11)

- 11.63 The two blocks shown are released from rest at t = 0. There is no friction and the cable is initially taut. (a) What is the tension in the cable immediately after release? (Use any reasonablevalueforthegravitationalconstant). (b) What is the tension after 5 s?

horizontal line

30o

30o

2m

2kg

2kg

rigid surface (Newtonian frame)

problem 11.63:

(Filename:pﬁgure.blue.18.2)

- 11.64 Carts A and B are free to move along a frictionless horizontal surface, and bob C is connected to cart B by a massless, inextensible cord of length , as shown in the ﬁgure. Cart A


movestotheleftataconstantspeedv0 = 1m/s and makes a perfectly plastic collision (e = 0) with cart B which, together with bob C, is stationary prior to impact. Find the maximum vertical position of bob C, hmax, after impact. The masses of the carts and pendulum bob are mA = mB = mC = 10kg.

After Collision Before collision (dotted lines)

g = 9.81 m/sec

Frictionless

Vo

B A

B A

hmax

C

problem 11.64:

(Filename:pﬁgure.blue.137.3)

- 11.65 See also problem 3.29. A double pendulum is made of two uniform rigid rods, each of length . The ﬁrst rod is massless. Find equations of motion for the second rod. Deﬁne any variables you use in your solution.

m

massless

m

m

problem 11.65:

(Filename:pﬁg2.1.rp10)

- 11.66 Amodelofwalkinginvolvestwostraight legs. During the part of the motion when one foot is on the ground, the system looks like the picture in the ﬁgure, conﬁned to motion in the x − y plane. Write two equations from which one could ﬁnd θ¨1, and θ¨2 given θ1,θ2,θ˙1,θ˙2andallmassandlengthquantities.



Hint:

- M/A =

- H˙ /A whole system

M/B =

- H˙ /B for bar BC




 

A

B

C

α

x

y

θ1

θ2

g

problem 11.66:

(Filename:pﬁgure.blue.100.1)

11.4 Advanced problems in 2D motion

- 11.67 A pendulum is hanging from a moving support in the xy-plane. The support moves in a known way given by r(t) = r(t)ıˆ. For the following cases, ﬁnd a differential equation whose solution would determine θ(t), measured clockwise from vertical; then ﬁnd an expression for d2θ/dt2 in terms of θ and r(t):


- a) with no gravity and assuming the pendulumrodismasslesswithapointmass of mass m at the end,
- b) as above but with gravity,
- c) assumingthependulumisauniformrod of mass m and length .


- 11.68 Robotics problem: balancing a broom stick by sideways motion. See also problem 7.99 and problem 8. Try to balance a broom stick by moving your hand horizontally. Model your hand contact with the broom as a hinge. You can model the broom as a uniform stick or as a point mass at the end of a stick your choice.

- a) Equation of motion. Given the acceleration of your hand (horizontal only), the current tip, and the rate of tip of the broom, ﬁnd the angular acceleration of the broom. ∗
- b) Control? Can you ﬁnd a hand acceleration in terms of the tip and the tip rate that will make the broom balance upright? ∗


C

A

![image 190](Introduction to Statics and Dynamics Problems_images/imageFile190.png)

![image 191](Introduction to Statics and Dynamics Problems_images/imageFile191.png)

x

y

L

φ

eˆθ eˆr

m

g

problem 11.68:

(Filename:pﬁgure.s94h10p5)

- 11.69 Balancing the broom again: vertical shaking works too. You can balance a broom by holding it at the bottom and applying appropriate torques, as in problem 7.99 or by moving your hand back and forth in an appropriate manner, as in problem 11.68. In this problem, you will to try to balance the broom differently. The lesson to be learned here is more subtle, andyoushouldprobablyjustwonderatitrather than try to understand it in detail.


In the previous balancing schemes, you used knowledge of the state of the broom (θ and θ˙) to determine what corrective action to apply. Now balance the broom by moving it in a way that ignores what the broom is doing. In the language of robotics, what you have been doing before is ‘closed-loop feedback’ control. The new strategy, which is simultaneously more simple minded and more subtle, is an ‘open loop’ control. Imagine that your hand connection to the broom is a hinge.

eˆθ eˆr

- a) Given the tip angle φ, the tip rate φ˙ and the values of the various parameters (m, R, L, g)ﬁndφ¨. [Youmayassumeφ and φ˙ are small.] ∗
- b) Using the result of (a) or any other clear reasoning ﬁnd the conditions on the parameters(m, R, L, g)thatmakevertical passive dynamic standing stable. [Stable means that if the person is slightly perturbed from vertically up that their resulting motion will be such that they remainnearlyverticallyupforallfuture time.] answer below is questionable, says someone ∗


- a) Pictureandmodel. Assumeyourhand oscillates sinusoidally up and down with some frequency and some amplitude. The broom is instantaneously at some angle from vertical. Draw a picture which deﬁnes all the variables you will use. Use any mass distribution that you like.
- b) FBD. Draw a FBD of the broom.
- c) Momentum balance. Write the equation of angular momentum balance about the point instantaneously coinciding with the hinge.
- d) Kinematics. Use any geometry and kinematics that you need to evaluate thetermsintheangularmomentumbalance equation in terms of the tip angle anditstimederivativesandotherknown quantities (take the vertical motion of your hand as ‘given’). [Hint: There are many approaches to this problem.]
- e) Equation of motion. Using the angular momentum balance equation, write agoverningdifferentialequationforthe tip angle. ∗
- f) Simulation. Taking the hand motion as given, simulate on the computer the system you have found.
- g) Stability? Can you ﬁnd an amplitude and frequency of shaking so that the broom stays upright if started from a near upright position? You probably cannot ﬁnd linear equations to solve that will give you a control strategy. So, this problem might best be solved by guessing on the computer. Successful strategies require the hand acceleration to be quite a bit bigger than g, the gravitational constant. The stability obtained is like the stability of an undamped uninverted pendulum — oscillations persist. You improve the stabilityalittlebyincludingalittlefriction in the hinge.
- h) Dinner table experiment for nerdy eaters. If you put a table knife on a table and put your ﬁnger down on the tip of the blade, you can see that this experiment might work. Rapidly shake your hand back and forth, keeping the knife from sliding out from your ﬁnger but with the knife sliding rapidly on the table. Note that the knife aligns with the direction of shaking (use scratchresistant surface). The knife is different from the broom in some important ways: there is no gravity trying to ‘unalign’ it and there is friction between the knife and table that is much more signiﬁcant than the broom interaction with the air. Nonetheless, the experiment should convince you of the plausibility of the balancing mechanism. Because of the large accelerations required, you cannot do this experiment with a broom.


m

y

![image 192](Introduction to Statics and Dynamics Problems_images/imageFile192.png)

C

![image 193](Introduction to Statics and Dynamics Problems_images/imageFile193.png)

g

L

###### ˆ

θ

A

x

ıˆ

yhand

(h)

Table

Shake knife back-&-forth in this direction

φ

L

G

Press finger here

R

problem 11.69: The sketch of the knife on the table goes with part (h).

(Filename:pﬁgure.vert.shake)

problem 11.71:

(Filename:pﬁgure.s94q11p1)

##### 11.5 Dynamics of rigid bodies in multi-degree-offreedom 2D mechanisms

##### 11.6 Advanced dynamics of planar motion

11.72 Consider a rigid spoked wheel with no rim. Assume that when it rolls a spoke hits the ground and doesn’t bounce. The body just swings around the contact point until the next spoke hits the ground. The uniform spokes have length R. Assume that the mass of the wheel is m, and that the polar moment of inertia about its center is I (use I = mR2/2 if you want to get a better sense of the solution). Assume that just before collision number n, the angularvelocityofthewheelisωn−,thekinetic energy is Tn−, the potential energy (you must clearly deﬁne your datum) is Un−. Just after collision n the angular velocity of the wheel is ωn+. The Kinetic Energy is TN+, the potential energy (you must clearly deﬁne your datum) is Un+. The wheel has k spokes (pick k = 4 if you have trouble with abstraction). This problem is not easy. It can be answered at a variety of levels. The deeper you get into it the more you will learn.

- 11.70 Double pendulum. The double pendulum shown is made up of two uniform bars, each of length and mass m. The pendulum is released from rest at φ1 = 0 and φ2 = π/2. Just after release what are the values of φ¨1 and φ¨2? Answer in terms of other quantities. ∗

φ1

φ2

O

A

B

problem 11.70:

(Filename:pﬁgure.s94h12p2)

- 11.71 A rocker. A standing dummy is modeled as having massless rigid circular feet of radius R rigidly attached to their uniform rigid body of length L and mass m. The feet do not slip on the ﬂoor.


- a) What is the relation between ωn− and Tn−?
- b) What is the relation between ωn− and ωn+?
- c) Assume ‘rolling’ on level ground. What is the relation between ωn+ and ωn+1?
- d) Assume rolling down hill at slope θ. What is the relation between ωn+ and ωn+1?


- e) Can it be true that ωn+ = ω(n+1)+? About how fast is the wheel going in this situation?
- f) As the number of spokes m goes to inﬁnity, in what senses does this wheel become like an ordinary wheel?


k evenly spaced spokes

2R

problem 11.72:

(Filename:pﬁgure.blue.109.1)

General motion in 3-D

##### 12.1 Orientation in 3-D

- 12.1 Find a rotation from a picture.
- 12.2 Velocity and acceleration of points on a rigid body: ω and α


###### 12.2 A particle moves on a helix. Say youknow that a particle moves according to theequation

r = R cosθıˆ + R sinθˆ + zkˆ

where R is a constant, θ = c1t, and z = c2t.

- a) Find v at general time t.
- b) Find a at general time t.
- c) Find eˆt at general time t.
- d) Find eˆn at general time t.
- e) Write a in terms of eˆt and eˆn.
- f) What is the radius of the osculating circle? Check your answer to see if it makes sense in the special case when c2 = 0.


###### 12.3 A curious chef tosses a potato in the air.Being a part-time dynamicist, she has just theright instruments in her kitchen and measuresthe absolute angular velocity of the potato tobe ω = 1ıˆ+2ˆ +3kˆ(rad/s) and the absolutecenter of mass velocity to be vG = 3ıˆ+4ˆ +5kˆ(in/s), at a particular instant in time. Atthe same instant in time, she notes the positionof an eye on the potato relative to its center of

mass, point G, is r E/G = 1inıˆ. (The high quality potato came from the market with the center of mass already marked inside it. ) ıˆ, ˆ,

and kˆ are basis vectors in the kitchen frame.

- a) What is the velocity of the potato eye relative to G, vE/G?
- b) What is the absolute velocity of the potato eye, vE?


- 12.3 Instantaneous dynamics and “inverse dynamics” in 3-D
- 12.4 Under what circumstances is the linear momentum of a system conserved (that is, does not change with time)?
- 12.5 For a continuous system, where at a given instant in time velocity depends on position, v = v( x), (a) how is linear momentum deﬁned? (b) How is rate of change of linear momentum deﬁned?
- 12.6 For what pointsC, with positions rC, are the balance of angular momentum equations

MC =

H˙ C, correct:

- a) the origin,
- b) the center of mass, and
- c) any point anywhere?


- 12.7 Bead on a stationary 3-D wire. A bead with mass m slides on a frictionless wire that is ﬁxed in space. The wire is twisted and curved in complicated ways. There is no gravity. The only force on the bead comes from the wire.


The initial speed of the bead is v0. Justify your answers to the following questions with text and/or equations. Add any extra assumptions if you feel they are required.

- a) Is it true that F = m a (where F is the total force on the bead and a its acceleration?)?
- b) Is the momentum of the bead,m v, constant?
- c) Is the kinetic energy of the bead, 12mv2, constant?

- d) Whatisthespeedofthebeadatt = 3s?
- e) Is the acceleration always such that a ·

eˆt = 0 (where eˆt is the unit tangent to the wire)?

- f) Is the acceleration always such that a ·

eˆn = 0 (where eˆn is the unit normal to the wire)?

- g) Using any notation you like to describe the wire shape, write an expression for the force F on the bead from the wire.
- h) For a circular wire, what is the direction of the force from the bead on the wire?
- i) For a helical wire, (say, r =


r0 cosθıˆ + r0 sinθˆ + Cθkˆ), what is the direction of the force from the bead on the wire? ∗

- 12.8 A 500kg roller coaster car travels along a track deﬁned by the conical spiral r = z, θ = −2z. If θ˙ = 2rad/s isconstant, determine the force exerted on the car by the track when z = 5m. Assume that the gravitational force acts in the negative z direction. Remember to express the force in vector form.
- 12.9 When do you use which term in H˙ O formula for a rigid body? To do the angular momentum balance about an arbitrary point O

we write MO =

H˙ O where the most general formula for H˙ O for one rigid body is H˙ O = rcm/o×m acm+[Icm]· ω˙ + ω×([Icm]· ω).

Give examples of motions of a rigid body (you may also use a point mass) in which

a) only one term at a time in the above for-

mulafor H˙ O survives(threeexamples) and

b) only two terms at a time in the formula survive (three examples).

- 12.10 (See also problems 12.33, 12.35, and 12.38.) Find the reaction supplied by the environment to the system of bodies ABD so that each body spins at a constant rate in problem 12.27. ∗
- 12.11 Disk suspended at corner by a ball and socket joint. See also problem 12.13. A disk with negligible mass has two point masses glued to it. It is stationary and horizontal when it is allowed to fall, but it is held back by a balland-socket joint at one point on its perimeter. Just after the disk is released, what is the acceleration of the point P? Is it up or down? ∗

massless disk

P

R

m x

y

z

30o m

problem 12.11:

(Filename:pﬁgure.s94h13p2)

- 12.12 A car driving in circles counterclockwise at constant speed so that its left rear


tire has speed vo (the middle of the tire, that is, or the location of the ground contact point.) The radius of the circle that the tire travels on is Ro. The radius of the tire is ro. Right next to the tire is the car fender (i.e., the fender overlaps the outer face of the tire. In fact the fender is rubbing on the tire just a little, but not quite enough to disturb any insects that might be in the neighborhood).

- a) What is the angular velocity of the car? ∗
- b) What is the angular velocity of the tire relative to the car? ∗
- c) What is the angular velocity of the tire? ∗
- d) What is the total torque applied to the car (not including the tires as part of the car, therotatingengineisalsomassless) relative to the car center of mass? ∗
- e) What is the total torque on the car relative to the center of the circle around which it is traveling? ∗
- f) What is the angular momentum of the tire relative to its center of mass (use any sensible model of the tire, say a rigid disk.)? ∗
- g) What is the rate of change of angular momentum of the tire (relative to its center of mass)? ∗
- h) What is the total torque of all the forces applied to the tire from the road and the

carascalculatedatthecenterofthetire?

∗

- i) A bug is climbing straight up on the

car fender named at speed vg. At the instant of interest she is right next to the center of the wheel. What is her velocity and acceleration? What is the total force acting on her? ∗

- j) Another bug is climbing on a straight linemarkedonthetireatconstantspeed

vb. He is in the middle of the tire at the instant of interest. What is his absolute velocity and acceleration? What is the total force acting on him? (Both bugs are at the same place at the instant of interest and walking on lines that are, at the moment, parallel.)

- k) Redotheproblem,questions(a)-(j),but thistimethecarspeedisincreasingwith


acceleration ao. Questions (a) - (j) of this problem are a special case of question (k). You should check that your answers from (k) reduce to the answers in questions (a) - (j). Or, if you are really cocky, you should skip the ﬁrst questions and only do (k). Then, display your answers for the special case ao = 0.

12.13 The moment of inertia matrix. Reconsider the system of problem 12.11 — a disk with negligible mass that has two point masses glued to it.

- a) Find the moment of inertia matrix [IO] of the system.
- b) Findtheangularaccelerationofthesystem when released from rest in the conﬁguration shown. You may use your answer from problem 12.11.


- 12.14 A square plate in space. A uniform square plate with mass m and sides with length 2L is ﬂoating stationary in space. A force of magnitude F is suddenly applied to it at point A. Using the coordinates shown the moment of inertia matrix for this plate is:

[I/cm] =

mL2 3

1 0 0 0 1 0 0 0 2

- a) What is the acceleration of the center of the plate aG? ∗
- b) What is the angular acceleration of the plate ω˙ ∗
- c) What is the acceleration ofpoint B aB? ∗


ıˆ

ˆ

kˆ

- F

2L

2L

- G


B

problem 12.14:

(Filename:pﬁgure.f93f5)

- 12.15 Force on a rectangular plate in space. A uniform rectangular plate of mass m = 10lbm is ﬂoating in space. A force F = 5lbf is suddenly applied at a corner that is perpendicular to the plate.

- a) Find the acceleration of the center of mass of the plate. ∗ a = −16ft/s2kˆ
- b) Find the angular acceleration of the plate. ∗
- c) Some of the plate accelerates in the direction of the force and some accelerates back towards the tail of the force vector. What part of the plate accelerates in the opposite direction of the applied force?


F

x

1 ft 2 ft

y

z

m

problem 12.15:

(Filename:pﬁgure.s94h13p3)

- 12.16 Force on a square plate. A constant force with magnitude F is applied, in the direction shown in the yz plane, to the corner B ofauniformsquareplatewithsidelength d and mass m. Before the force is applied the plate is at rest in space with no other forces applied to it. Consider the time immediately after the time of the force application.


- a) What, in terms of m, F, d, ıˆ, ˆ, kˆ, and φ is the acceleration of point B?
- b) For what angle φ is the acceleration of point B in the direction of the force?
- c) Find another direction for F so that the force at B and the acceleration at B are parallel (not necessarily in the ˆ-kˆ plane). [Physical reasoning will probably work more easily than mathematical reasoning.]
- d) Find yet another direction for F so that the force at B and the acceleration at B are parallel (not necessarily in the ˆ-kˆ plane).


φ

ˆ

ıˆ

y

F

kˆ

x

B

z

m

d d

problem 12.16:

(Filename:p.s96.p3.3)

- 12.17 (See also problems 12.32, 12.34, and 12.37.) Find the reaction supplied by the environment to the system of bodies ABD so that each body spins at a constant rate in problem 12.31.

- 12.4 Time evolving dynamicsofanunconstrainedrigid body in 3-dimensions

12.18 A rigid body ﬂies through the air and tumbles. Find the equations of motion and solve them for your choice of parameters and initial conditions.

- 12.5 Kinematics of motion relative to a moving and rotating reference frame in 3D


- 12.19 Find the rotation matrix [R] for θ = 30o


such that {eˆ } = [R]{eˆ}, where eˆ = {ıˆ,ˆ,kˆ}. Using the rotation matrix, ﬁnd the components of v = 2m/sıˆ − 3m/sˆ + 1m/skˆ in the rotated coordinate system.

z

z'

θ

y'

θ

y

x, x'

problem 12.19:

(Filename:eﬁg1.2.28)

- 12.20 A circular plate rotates at a constant an-

gular velocity ω = 5rad/skˆ. A set of coordinate axes x y z is glued to the plate at its center and thus rotates with ω. Find the rate of change basis vectors ıˆ , ˆ , and kˆ using the Q˙ formula.

- 12.21 A rigid body B rotates in space with

angular velocity ω = (2ıˆ + 3ˆ − kˆ)rad/s. A set of local coordinate axes x y z is ﬁxed to the body at its center of mass. The position vector r P of a point P is given in local coordinates: r P = (5ıˆ +ˆ )m. Find the velocity ( r˙ P) of point P using the Q˙ formula.

- 12.22 The rotation matrix between two coordinate systems with basis vectors (eˆ1,eˆ2,eˆ3)

and (Eˆ 1,Eˆ 2,Eˆ 3) is Q such that {eˆ} = [Q]{E}. Find the components of a =

(−2eˆ1+3eˆ3)m/s2 in the(Eˆ 1,Eˆ 2,Eˆ 3)basis if Q =

 

1 0 0 0 12 −

√3 2

0

√3 2

1 2

 .

- 12.23 Let B and F be two moving rigid bodies. Show that B ω˙ B/F = F ω˙ B/F .
- 12.24 George is driving his car on the highway on a rainy day. His windshield wipers are on. He notices that a drop of water on the wiper blade is moving along the blade at approximately 3in/s. Although the wipers rotate at variable angular speed, he approximates that when the wiper is parallel to his nose, its angular speed is π/2rad/s. In George’s coordinate system (attached to his frame of reference and moving with him), the wiper is rotating in the positiveˆ direction and the water-drop is mov-

ing in the positivekˆ direction at the moment of interest. Find the velocity of the water-drop in George’s frame of reference.

- 12.25 Apersonsitsonabarstoolwhichspinsat angular speed . Simultaneously, (s)he hoists a beer glass of mass m up at angular speed ω relativetothebarstoolwithastraight, rigidarm of length L. θ measures the the angle of her/his arm with respect to the XY plane. XY Z is an inertial coordinate system; Y Z lies in the plane of the paper. If you use moving axes to do this problem, specifyclearlyhis/herorientationand motion.


- a) What is the angular velocity of the person’s arm?
- b) What is the angular acceleration of the person’s arm?
- c) What is the linear velocity of the beer glass relative to inertial space?
- d) What is the linear acceleration of the beer glass relative to inertial space?
- e) Describe how you would point an absolutely full glass such that the beer will not spill out.


z

L m ω θ

y

x

problem 12.25:

(Filename:pﬁgure.blue.118.2)

- 12.26 Kinematics of a disk spinning on a spinning rod. The rigid rod R rotates at constant rate about the z axis. Attached to this rod, a distance R from the origin, is the center C of a disk C with diameter D. The disk is rotating at constant rate ω about an axis y that is attachedto, androtateswith, therod. Apoint B is on the outer edge of the disk. At the moment of interest, the system is in the conﬁguration shown with rCB = (D/2)kˆ.

- a) What is the absolute angular velocity of the disk, ωD? ∗
- b) What is the absolute angular acceleration of the disk αD? ∗
- c) What is the absolute velocity of point B, vB? ∗
- d) What is the absolute acceleration of point B, aB? ∗


O x,x'

y

y'

C

B D

D

R ω

R

problem 12.26:

(Filename:pﬁgure.s95f3a)

- 12.27 See also problems 12.33, 12.35, and 12.38. Body A rotates with respect to a New-


tonian frame F at a constant angular rate ω0 about axis OO . Body B, a ‘fork’, rotates with respect to body A at a constant angular rate ω1 about axis P P . Bodies A and B are

of negligible mass. Body D, a uniform disc of mass m, rotates with respect to body B, at a constant angular rate ω2 about axis CC . Each of the bodies is turned at constant rate by motors(not shown.) At the instant shown, ﬁnd the absolute angular velocity of body D, ωD/F . ∗

z

O

ω0

x y

P

L

G

B A

D,m

C'

ω1

F

E r

O'

P'

C

ω2

problem 12.27:

(Filename:Danef94s1q2)

- 12.28 A particle P of mass m is attached to the edge of the disk of radius R, as shown in the ﬁgure. The disk spins about its center line with constant angular speed ω rad/s relative to the shaft OB. The shaft OB rotates with angular speed rad/s. For the instant when the disk lies in the Y Z plane, and the particle is on the Y axis, as shown:

- a) Find the particle’s velocity relative to XY Z.
- b) Calculatetheparticle’saccelerationrelative to XY Z.
- c) Calculate the force F acting on the particle.


Ifyouchoosetouseanothercoordinatesystem, deﬁne it explicitly.

xyz: fixed frame

X Y

Z

mass, m P

ω

O

B

R

problem 12.28:

(Filename:pﬁgure.blue.123.1)

- 12.29 See also problem 12.53. Two identical thin disks, bodies C and D , of radius r are connected (perpendicularly) to opposite ends of a thin axle, as depicted below. The axle rotates about the ﬁxed Z axis at a constant angular speed , and the disks roll without slipping. Determine:


(a) The total angular velocity of each disk,

ωC and ωD, and

z

(b) The total angular acceleration of each

O

O

disk, αC and αD.

(Express your answers relative to the rotating basis { ıˆ,ˆ,kˆ}.)

ω0

ω0

x y

x y

L

L

z R

G P'

G P'

A B

A B

R

Q

Q

C' P

C' P

kˆ ˆ

D,m

D,m

ω1

ω1

r r

F

F

E r

E r

O y

D C

ıˆ

O'

O'

C

C

x

ω2

ω2

problem 12.31:

problem 12.34:

(Filename:Danef94s3q2)

(Filename:bikefork1.alt)

problem 12.29:

(Filename:pﬁgure.blue.119.2)

- 12.35 (See also problems 12.33, 12.38, and 12.10.) Fortheconﬁgurationinproblem12.27, ﬁnd the velocity and acceleration of point the point on the edge of the disk directly above its center point E using the alternative method.

ω0

ω1

ω2

L

F

B A

D,m

O

O'

C

C'

P

P'

G

x y

z

E r

problem 12.35:

(Filename:bikefork.alt)

- 12.36 To simulate the ﬂight conditions of a space vehicle, engineers have developed the centrifuge, shown diagrammatically in the ﬁgure. A main truss arm of length = 15m, rotates about the AA axis. The pilot sits in the capsule which may rotate about axis CC. The seat for the pilot may rotate inside the capsule about an axis perpendicular to the page and going through the point B. These rotations are controlled by a computer that is set to simulate certain maneuvers corresponding to the entry and exit from the earth’s atmosphere, malfunctions of the control system, etc. When a pilot sits in the capsule, his head, particularly his ears, has the position shown in the enlarged ﬁgure, a distance r = 1m from point B.


- 12.32 (See also problems 12.34, 12.37, and 12.17.) For the system in problem 12.31, ﬁnd the absolute angular acceleration of frame D, F ω˙ D, at the instant shown.

ω0

ω1

ω2

L

F

A B

D,m

O

O'

C

C' P

G P'

Q

x y

z

E r

problem 12.32:

(Filename:bikefork1.ang.accel)

- 12.33 (See also problems 12.35, 12.38, and 12.10.) For the system in problem 12.27, ﬁnd the absolute angular acceleration of frame D, F ω˙ D, at the instant shown. ∗

ω0

ω1

ω2

L

F

B A

D,m

O

O'

C

C'

P

P'

G

x y

z

E r

problem 12.33:

(Filename:bikefork.ang.accel)

- 12.34 (See also problems 12.32, 12.37, and 12.17.) Fortheconﬁgurationinproblem12.31, ﬁnd the velocity and acceleration of point Q on the disk using the alternative method.


- 12.30 Kinematics of a rolling cone. See also problem 8.19. A solid cone with circular-base radius r and height h moves as follows. Point O is ﬁxed in space. The cone surface always contacts the plane but may roll and/or slide. The axis of the cone OB rotates about the vertical axis with constant angular velocity−ω1ıˆ. The cone spins about this moving axis ˆ with constant angular rate ω2.

- a) Attheinstantshownwhatisthevelocity of point B? (in terms of some or all of ω1, ω2, r, h, ıˆ, ˆ, and kˆ) ∗
- b) At the instant shown what is the angular acceleration of the cone? (in terms of

some or all of ω1, ω2,r, h, ıˆ, ˆ, and kˆ) ∗

- c) If the disk is rolls with no slip, ﬁnd ω1 in terms of ω2, r and h. ∗
- d) If the disk rolls with no slip and point B has constant speed v ﬁnd the magnitude of the angular acceleration of the cone in terms of v, r and h. ∗


r

h

- A
- B O


ω1

ω2

x

y

y'

z

problem 12.30: Cone rolling on a plane

(Filename:pﬁgure.s95q14)

- 12.31 See also problems 12.32, 12.34, 12.37, and 12.17. Body A rotates with respect to a Newtonian frame F at a constant angular rate


The main arm is rotating at = 10rpm and accelerating at ˙ = 5rev/min2, the capsule is rotating at a constant speed about CC at ωc = 10rpm, and the seat rotates at a speed of ωs = 5rpm inside the capsule.

- ω0 about axis OO . Body B, a ‘fork’, rotates with respect to body A at a constant angular


rate ω1 about axis P P . Bodies A and B are of negligible mass. Body D, a uniform disc of mass m, rotates with respect to body B, at a constant angular rate ω2 about axis CC . Each of the bodies is turned at constant rate by motors(not shown.) At the instant shown, ﬁnd the absolute velocity and acceleration of point Q on the disk.

- a) Determine the acceleration, in terms of how many g’s, that the pilot’s head is subjected to by choosing a moving coordinates system xyz centered at B and ﬁxed to the capsule.
- b) Repeatthecalculationsof(A)byletting xyz be ﬁxed to the seat. ∗


- 12.40 A bead P rides on a frictionless thin circular hoop of radius R. The hoop rotates about its diameter at a constant angular speed ω in the vertical plane. Find, in terms of θ,θ˙ and ω and base vectors you deﬁne (a) the velocity of the bead (a vector) and (b) the acceleration of the bead (a vector).

P

R

![image 194](Introduction to Statics and Dynamics Problems_images/imageFile194.png)

![image 195](Introduction to Statics and Dynamics Problems_images/imageFile195.png)

ω

θ

problem 12.40:

(Filename:pﬁgure4.2.rp10)

- 12.41 Athinrodofmassm andlength L moves while making contact with the frictionless sur-


- c) Choose another moving coordinates system to solve the same problem.
- d) A pilot has different tolerances for acceleration components. They are roughly:


O

ω0

x y

L

G P'

A B

Q

- (a) In a vertical direction, i.e., toe to head – 5 g’s. (Here the pilot experiences blackout or may pass out completely.)
- (b) Front to rear – 1.5 g’s. (Here vision becomes greatly distorted.)


C' P

D,m

ω1

F

E r

O'

C

ω2

Arrangeatestprogramonthecentrifugesothat each acceleration is reached separately while the other accelerations are kept below one- half their tolerance levels.

problem 12.37:

(Filename:bikefork1.ang.mom)

- 12.38 (See also problems 12.33, 12.35, and 12.10.) Reconsider the system in problem 12.27. Bodies A and B are of negligible mass and body D is a uniform disc of mass m. Find the angular momentum and rate of change of angular momentum of the system of bodies ABD about:

- a) point G ∗
- b) point E. ∗


Make reasonable assumptions about moments of inertia.

ω0

ω1

ω2

L

F

B A

D,m

O

O'

C

C'

P

P'

G

x y

z

E r

problem 12.38:

(Filename:bikefork.ang.mom)

- 12.39 Reconsider problem 12.48. A thin uniform disk D of mass m = 2kg and radius r = 0.2m is mounted on a massless shaft AB as shown in the ﬁgure. Rod CO is welded to the shaft and has negligible mass. The shaft rotates at a constant angular speed = 120rpm about the positive x-axis. The disk spins about its own axis at a constant rate ω = 60rpm with respect to the shaft (or bar CO). Find the dynamic reactions on the bearings at A and B at the instant shown. ∗


x

ωc ωs

| | |
|---|---|
| | |


r

y

B

seat & pilot

bearing

, ˙

capsule

face (the eˆ1 − eˆ2 plane) at its tip A, as shown in the ﬁgure. θ is assumed to be constant and

A

Z

the rod always remains in the eˆ3,eˆr plane.

x

- a) What is the kinematical relation betweenthevelocityofthecenterofmass,

vG, and the angular velocity of the rod, ω?

- b) Obtain the equations of motion of the rod in terms of the speed of point A and the angle φ.


y

Y O

C

C

B

| | |
|---|---|
| | |


truss

capsule

bearings bearings

A

The unit vectors eˆ∗1 and eˆ∗3 lie in the (eˆ3−

problem 12.36:

er) plane and eˆ∗2 is normal to the (eˆ3 − eˆr) plane. The starred basis vectors are written in

(Filename:pﬁgure.blue.128.1)

terms of the the standard basis as follows:

eˆr = cosθeˆ1 + sinθeˆ2,

##### 12.6 Mechanisms in 3-D

- eˆ∗1 = sinφeˆ3 + cosφeˆr, eˆ∗3 = cosφeˆ3 + sinφeˆr, and
- eˆ∗2 = −sinθeˆ1 + cosθeˆ1.


g

m,L

12.37 (See also problems 12.32, 12.34, and 12.17.) Reconsider the system in problem 12.31. Bodies A and B are of negligible mass and body D is a uniform disc of mass m. Find the angular momentum and rate of change of angular momentum of the system of bodies ABD about:

eˆ*3

eˆ3

kˆ

ˆ

ω

G

φ

eˆ1 eˆ2

ıˆ

eˆ*2

C D 0.4 m

m = 2 kg r = 0.2 m

eˆ*1

A

A B

θ eˆr

O

- a) point G
- b) point E.


1 m

problem 12.41:

problem 12.39:

Make reasonable assumptions about moments of inertia.

(Filename:pﬁgure.blue.125.2)

(Filename:summer95f.5.a)

- 12.42 A cosmonaut who is otherwise free to move in 3-dimensional space ﬁnds himself stuck to the surface of a giant stationary cylinder with slippery magnets. There is no friction and (net) gravity is negligible. θ and z are cylindricalcoordinatesthatarealignedwiththe cylinder and mark the position of the cosmonaut relative to the cylinder. The cylinder has radius a. A nearby astronaut notes that at time

t = 0: θ = θ0, θ˙ = θ˙0, z = z0, and z˙ = z˙0. What does she predict for the location of the cosmonaut (the values of θ and z) at an arbitrary later time t? You can assume that both the cylinder and the astronaut were stationary in the same Newtonian (inertial) frame.

z

x

y

θ

problem 12.42:

(Filename:pﬁgure.blue.68.1)

- 12.43 You are an astronaut in free space and your jet pack is no longer operating. You wish to reorient your body in order to face the central government buildings so as to salute your national leaders before reentering the atmosphere. Discuss whether this maneuver can be done in terms of momentum, energy, or other dynamical concepts. (You are free to move your arms and legs, but you are not allowed to throw anything.) [For aliens and those less patriotic, the same problem arises in the case of a trampoline jumper who decides to change direction in mid-air. Is it possible?]
- 12.44 A collar slides on the rigid rod ABC that has a 30◦ bend at B as shown in the ﬁgure. The collariscurrentlyatpoint D ontherod. Therod ABC is held by ﬁxed hinges that are aligned with the z-axis, and rotates at the constant rate


- ω1 = 2rad/s. The collar has mass mD = 1kg.


- a) Assume a mechanism not shown constrains the collar to slide out along the rod at the constant rate u = 1m/s (u is the distance along the rod traveled per unit time). What is the net force that acts on the collar when it is 1m from B?
- b) Assume that the contact between the collarandtherodisfrictionlessandthat no forces act on the collar besides those due to the rod (e.g. neglect gravity). At the instant shown in the picture, assume that u = 1m/s (because of some initial conditionsnotdiscussedhere)butisnot necessarily constant in time. What is the acceleration of the collar?


ω1 = 2rad/s = const. mD = 1kg

A

ω1

y

B

O

30o

1m 0.5m

z

x

D C

Bead slides on rigid bent rod. Rod in yz-plane at instant shown.

u

problem 12.44:

(Filename:pﬁgure.blue.58.1)

- 12.45 A biﬁlar pendulum is formed of a rod of length a and mass m, supported by two ﬁlaments of length and separation 2b. What is the frequency of small ‘torsional’ oscillations about a vertical axis though the rod’s mid-point 0?

b

2b

a

O

m

g

problem 12.45:

(Filename:pﬁgure.blue.157.1)

- 12.46 A triﬁlar pendulum is formed of a thin horizontal disk of radius a and mass m, hung by three wires a distance below the ceiling. The wire attachments are equally spaced on the perimeterofthedisk. Theattachmentpointson the ceiling form an equilateral triangle.

- a) If the support wires are vertical what is the period of oscillation?
- b) How big should the triangle on the ceiling be to minimize the period of oscillation?
- c) To maximize the period of oscillation?


12.7 Circles on circles and other special 3-D motions

- 12.47 Sometimes thrown footballs (and frisbees too!) wobble and sometimes they spin smoothly. Describe as best you can why these motions differ.
- 12.48 See also problem 12.39. A thin uniform diskD ofmassm = 2kgandradiusr = 0.2m


is mounted on a massless shaft AB as shown in the ﬁgure. Rod CO is welded to the shaft and has negligible mass. The shaft rotates at a constant angular speed = 120rpm about the positive x-axis. The disk spins about its own axis at a constant rate ω = 60rpm with respect to the shaft (or bar CO). Find the absolute angular velocity and acceleration of the disk. ∗

kˆ

ˆ

ω

ıˆ

C D 0.4 m

m = 2 kg r = 0.2 m

A B

O

1 m

problem 12.48:

(Filename:summer95f.5)

12.49 A thin circular disk of mass m and radius R is mounted on a thin light axle, coincident withitsaxisofsymmetry. Theaxleissupported by bearings A and B attached to a turntable, as shown in the ﬁgure. The turntable spins at a constant speed abouteˆ3, while the disk spins about its axle at a constant speed µ relative to the turntable (via motors not shown). The radial unit vector er = cos( t)eˆ1 + sin( t)eˆ2 is ﬁxed to the turntable and aligned with eˆ1 at time t = 0. Compute the vertical components of the reaction forces at A and B. Will the reaction forces change with time?

eˆ3

g

- eˆ1
- eˆ2


B

µ

A

eˆr

eˆ3

The eˆr-eˆ3 plane (side view)

A R

B

µ

eˆr

L a

L

problem 12.49:

(Filename:pﬁgure.blue.127.2)

12.50Steadyprecessionofaspinningdisk. A uniform disk of mass m = 2kg and radius R = 0.25m is rigidly mounted on a massless axle AB which is supported by frictionless bearings at A and B. The axle, in turn, is mounted on a massless semi-circular gimbal as shown in the ﬁgure. The gimbal rotates about the vertical x-axis, which passes through the center of the disk D, at a constant rate = 2rad/s. The

wheel axle. (You should assume that the wheel axle is horizontal, that the wheel rolls without slip and that the wheel deformation and gravity arenegligible.) Atthisinstant, whatistheforce that the tread causes on the pebble? Resolve this force into east, north and upwards components. [Hint: several intermediate calculations are probably required.]

forces acting between the wheel and the horizontal surface. What is the vertical reaction on the bottom of the wheel? ∗

axle AB is spinning at a constant rate ω = 120rpm with respect to the gimbal. At the instant shown, the axle is aligned with the zaxis and the disk D is in the xy-plane. Ignore gravity. At the instant of interest:

z ball and

- x
- y


ω R

socket

B

- a) What is the angular velocity ωD of the disk? ∗
- b) What is the angular acceleration of the disk? ∗
- c) What is the net torque required to keep the motion going? ∗
- d) What are the reaction forces at the bearings A and B? ∗


L

O weld

- 12.56 A child constructs a spinning top from a solid sphere with radius a and mass m attached to a massless rod of length 2d. The sphere pivots freely about O. It is set spinning with a constant rate φ˙ and precessing with a constant rateψ˙ . Thetopoftherodisheldbyahorizontal cord.

Note: The moments of inertia of a solid sphere of mass m and radius a about any axis through the center is (2/5)ma2. (All products of inertia are zero, due to symmetry.)

- a) Using an axis system attached as shown (z lies along the shaft, x is out of the page and y is chosen to produce a righthanded system), write the body’s angular velocity ω as well as the angular velocity of the moving coordinate system relative to inertial space.
- b) Whatisthesphere’sinertiatensorabout O?
- c) What is the top’s angular momentum about O?
- d) Compute the tension in the cord. cord z


y

d

d

 ˙

θ

φ

problem 12.56:

(Filename:pﬁgure.blue.110.1)

- 12.57 A thin disk of mass m and radius R is connected by a massless shaft of length L to a free swivel joint at O. The disk spins about the shaft at rate ω and proceeds in a steady slow precession (rate ) about the vertical.


problem 12.52:

(Filename:s92f1p7)

A

- 12.53 In problem 12.29, ﬁnd the angular momentum and rate of change of angular momentum of the two disks about point O. Assume that the mass of each disk is m.

O y

z R

x

R

r r

ıˆ

kˆ ˆ

D C

problem 12.53:

(Filename:twodisks.ang.mom)

- 12.54 A vehicle of mass m, width b, and height h rolls without slip along a road which runs into the page(along the z-axis.) The inertial properties about the vehicle center of mass are


m = 2kg R = 0.25m

D

B

ω

O

0.5m

ıˆ ˆ kˆ

problem 12.50:

(Filename:pﬁgure.s94h13p4)

- 12.51 A cyclist rides a ﬂat, circular track of radiusr = 150ftataconstanttangentialspeedof v = 22ft/s on 27in diameter wheels. Assuming that the bicycle is vertical, determine the total angular velocity and angular acceleration of the wheel of the bike in the sketch (the rest of the bicycle is not shown). Use the coordinates given in the sketch.

| | |
|---|---|
| | |


r

ˆ ıˆ

kˆ

x

z

y

v

problem 12.51:

(Filename:pﬁgure.blue.90.2)

- 12.52 Rolling disk presses down. A rigid disk (idealized as ﬂat) with radius R and mass m is rigidly attached (welded) to a rigid massless stick with length L which is connected by a ball-and-socket joint to the support at point O. The wheel rolls on a horizontal surface. Point O isattheheightofthecenterofthewheel. The stickrevolvesaroundOatarateofω. Saygravity is negligible and, even though the wheel is rolling, you may assume there are no frictional


Ixxcm,Iyycm,Izzcm, and Ixycm = Ixzcm = Iyzcm = 0. Make additional assumptions as needed to get

ananswertotheproblem. Computethecontact forces acting on each wheel normal to the road in the following cases:

- a) The vehicle moves at constant speed v along a straight road.
- b) The vehicle moves at constant speed v along a circular road (radius ρ) curving to the left. Does the right or left wheel experience the larger force?


Rear end view

y

wheel

h

x y

- a) Write the disk’s inertia tensor about O. Specify the axes that you have chosen.
- b) Write the disk’s angular momentum

about O, HO, in the same coordinate system.

- c) Calculate the rate of change of angular momentum about O, H˙ O.
- d) Compute the precession rate for the slow precession case (ω ).


b

problem 12.54:

(Filename:pﬁgure.blue.90.1)

12.55 A car drives counter-clockwise in circles at constant speed V. The radius of the circle that the left rear wheel travels on is R. The radius of the wheel is r. Just when the wheel is rolling due north a pebble of mass m, which is stuck in the tread, is passing directly above the

y

y

H˙

![image 196](Introduction to Statics and Dynamics Problems_images/imageFile196.png)

![image 197](Introduction to Statics and Dynamics Problems_images/imageFile197.png)

L O

H

b a

| | |
|---|---|
| | |


ω θ

P

![image 198](Introduction to Statics and Dynamics Problems_images/imageFile198.png)

r

z x

![image 199](Introduction to Statics and Dynamics Problems_images/imageFile199.png)

ω2

O

m

x

R

z

problem 12.57:

problem 12.58:

(Filename:pﬁgure.blue.107.1)

y

(Filename:pﬁgure.s94h14p4)

O

z

x

h

O

ω1

12.58 Spinning and precessing top. (hard question) The picture schematically shows what is going on when a spinning top is in steady precession. The top is, approximately, spinning at constant rate about its symmetry axis. This axis is in turn (so to speak) rotating about the y axis at a constant rate. This rotation about the y axis is called precession. The angular momentum vector thus changes in time as the top precesses and the angular momentum vector also precesses. The picture is a reasonable approximation if the top is rotating much faster than it is precessing. The picture is not accurate if the precession rate is not much smaller than the rotation rate. Here are some questions to help you see why.

problem 12.59:

(Filename:pﬁgure.blue.122.1)

- 12.60 buzzing coin If you drop a round coin it will often go round and round progressively faster before buzzing to a stop. In terms of parameters you deﬁne, what is the frequency of this buzzing as a function of the tip angle? This problem is more subtle than a straightforward calculation as there are many solutions for a coin rolling at a given tip angle in circles. What feature picks out the solutions that are observed with real coins?

12.8 Motion relative to the earth

- 12.61 Estimate the sideways force (Pounds or Newtons) required for a person to walk a straight marked path over the North pole. Radius of earth ≈ 4000 miles ≈ 2 × 107 feet ≈ 6×106 meters. Make other simplifying approximations so that you can do the arithmetic without a calculator.
- 12.62 Foucoult pendulum
- 12.63 Estimating the error of using the earth as a Newtonian frame
- 12.64 The path of an air mass sliding on a frictionless earth


- a) If the top is precessing as well as spinning what is the direction of the angular velocity vector?
- b) What is the direction of the angular momentum vector of the top? Is it parallel to the top’s axis? Is it parallel to the angular velocity vector?
- c) How does the angular momentum vector differ from that shown in the ﬁgure?
- d) Does this difference affect any predictionsabouttheprecessionrateofaspinning top?
- e) Assume the top is on a pedestal and is horizontal as it precesses. In this case the correct precession rate is predicted by the naive/approximate theory that the angular momentum is just that due to spin and that this vector precesses with the top axis. Why does this simpliﬁcation happen to work?


12.59 An amusement park ride consists of two cylinder-shaped cars of length = 8ft and radius r = 3ft mounted at opposite ends of a long arm of length 2h = 20ft which is pivoted at its center as shown in the ﬁgure. The arm is constrained to rotate about the horizontal axle O − O. Each car can also rotate about its own axis. Car A, presently at the top of its ﬂight, is spinning (much to the discomfort of its occupants) on its own axis as shown at a constant rateofω2 = 5rad/srelativetotheverticalarm. The vertical arm is rotating about axis O−O at the rate ω1 = 0.5rad/s in the direction shown, as seen by a ground observer. The point P, located at x = a = 2ft and z = b = 1ft and representing a point in the inner ear of a passenger, is undergoing absolute velocity and acceleration vP and aP, respectively. Find the vectors vP and aP. (Ifyouareusingamoving coordinate system to determine vP and aP, state clearly how it moves).

### Answers to *’d problems

2.33 ) rx = r · ıˆ = (3cosθ + 1.5sinθ)ft, ry = r · ˆ =

(3sinθ − 1.5cosθ)ft. 2.68 ) No partial credit. 2.69 ) To get chicken road sin theta.

2.74 ) N = 1000N√3 (ıˆ + ˆ + kˆ). 2.77 ) d = 32. 2.81a) λˆ OB = √150(4ıˆ + 3ˆ + 5kˆ).

- b) λˆ O A = √134(3ˆ + 5kˆ).

- c) F1 = √5N34(3ˆ + 5kˆ), F2 = √7N50(4ıˆ + 3ˆ + 5kˆ).

- d) AOB = 34.45deg.

- e) F1x = 0
- f) r DO × F1 = √ 10034ˆ − √6034kˆ N·m.

- g) Mλ = √14050 N·m.

- h) Mλ = √14050 N·m.(same as (7))


2.83a) nˆ = 13(2ıˆ + 2ˆ + kˆ). b) d = 1. c) 13(−2,19,11).

2.94 ) (0.5m, −0.4m)

- 4.2 ) T1 = Nmg, T2 = (N − 1)mg, TN = (1)mg, and in general Tn = (N + 1 − n)mg
- 4.3 ) Suprise! This pendulum is in equilibrium for all values of θ.


- 4.8 ) Yes.


- 4.17a) Mm = RRcossinθ+θ r = 1+2sin2cosθ θ .

- b) T = mg = 2Mg1+sin2cosθ θ .

- c) FC = Mg −2cos2sinθ+θ 1ıˆ + ˆ (where ıˆ and ˆ are aligned with the horizontal and vertical directions)

- d) tanφ = 2+sincosθ θ . Needs somewhat involved trigonometry, geometry, and algebra.

- e) tanψ = Mm = 1+2sin2cosθ θ .


- 4.18a) Mm = RRcossinθ−θ r = 2cos2sinθ−θ 1.


- b) T = mg = 2Mg2cossinθθ−1.

- c) FC = 1−2cosMg θ sinθıˆ + (cosθ − 2)ˆ .


= RRoo+−RRii sinsinφφ

###### 4.21a) FF1

2

- b) For Ro = 3Ri and µ = 0.2, FF1

2

≈ 1.14.

- c) FF1


###### = eµθ = e0.2π ≈ 1.87.

2

√26

- 4.23 ) (a)TAB = 30N, (b) TAB = 30017 N, (c)TAB = 5


2 N

- 4.25g) TEH = 0 as you can ﬁnd a number of ways.
- 5.5 ) x(3s) = 20m


5.22 ) hmax = e2h. 5.34 ) (a) mx¨ + kx = F(t), (b) mx¨ + kx = F(t), and (c)

my¨ + 2ky − 2k 0 2y

= F(t) 5.37b) mg − k(x − 0) = mx¨ c) x¨ + mk x = g + km 0

0+y2

- e) This solution is the static equilibrium position; i.e., when the mass is hanging at rest, its weight is exactly balanced by the upwards force of the spring at this constant position x.
- f) x¨ˆ + mk xˆ = 0

- g) x(t) = D − 0 + mgk cos mk t + ( 0 + mgk )

- h) period=2π mk .

- i) If the initial position D is more than 0 +2mg/k, then the spring is in compression for part of the motion. A ﬂoppy spring would buckle.


5.39a) period= 2πk

= 0.96s

m

- b) maximum amplitude=0.75ft
- c) period= 2 2gh + mk π + 2tan−1 2mgkh ≈ 1.64s.


5.41 ) LHS of Linear Momentum Balance: F = −(kx +

bx˙)ıˆ + (N − mg)ˆ.

- 5.55a) Two normal modes.

b) x2 = const ∗ x1 = const ∗ (A sin(ct) +

B cos(ct)),where const = ±1. c) ω1 = 3mk, ω2 = mk .

- 5.56a)


m1 0 0 m2

x ¨1 x¨2 +

0 0

k1 + k2 −k2

x1 x2 =

−k2 k2 + k3

b) If we start off by assuming that each mass undergoes simple harmonic motion at the same frequency but different amplitudes, we will ﬁnd that this twodegree-of-freedom system has two natural frequencies. Associated with each natural frequency is a ﬁxed ratio between the amplitudes of each mass. Each mass will undergo simple harmonic motion at one of the two natural frequencies only if the initial displacements of the masses are in the ﬁxed ratio associated with that frequency.

5.58) aB = x¨Bıˆ = m1B [−k4xB − k2(xB − xA) + c1(x˙D −

x˙B) + k3(xD − xB)]ıˆ.

- 5.59 ) aB = x¨Bıˆ = m1B [−k4xB − c1(x˙B − x˙A) + (k2 + k3)(xD − xB)].


###### 5.62a) ω = 2mk.

- 5.66a) One normal mode: [1,0,0].


√17 4 ].

b) The other two normal modes: [0,1, 1±

5.72a) v(5s) = (30ıˆ + 300ˆ)m/s. b) a(5s) = (6ıˆ + 120ˆ)m/s2.

- 5.73 ) r(t) = x0 + u0 − u0 cos( t) ı ˆ + (y0 + v0t)ˆ.


- 5.81 ) v = 2t m/s2ıˆ + e ts m/sˆ, a = 2m/s2ıˆ + e ts m/s2ˆ.


- 5.118 ) T3 = 13N

- 5.131 ) Equation of motion: −mgˆ − b(x˙2 + y˙2) √x ˙ıˆ+˙yˆ

x˙2+˙y2

= m(x¨ıˆ + y¨ˆ).

- 5.132a) System of equations:

x˙ = vx y˙ = vy

- v˙x = −

b m

vx vx2 + v2y

- v˙y = −g −


b m

vy vx2 + v2y

- 5.143) No. You need to know the angular momenta of the particles relative to the center of mass to complete the calculation, information which is not given.

- 5.154a) v0 = m1 (mvB + mBvB + mAvA).

- b) v1 = (m+mmB)vB.

- c) (1) Eloss = 12m v02 − m+mmB v2B − 12mAv2A. Eloss = 12m (m+mmB)2v2B − (m + mB)v2B .


- 5.155 ) vA = m2mBkδ2

A+mBmA .

- 6.3 ) Tn = vPt


t

n N .

- 6.9a) aB = mmBA+−mmBA g


b) T = 2mmAmB

A+mB g.

- 6.13 ) (a) aA = aB = mF ıˆ, where ıˆ is parallel to the ground and pointing to the right., (b) aA = 2mF ıˆ, aB = 4mF ıˆ, (c) aA = 2Fmıˆ, aB = 4Fmıˆ, (d) aA = mF ıˆ, aB = −mF ıˆ.


- 6.15 ) ratio of the acceleration of A to that of point B, aaA


B

= 81.

- 6.18a) aA = 5mF ıˆ, aB = 25mF ıˆ, where ıˆ is parallel to the ground and points to the right.


b) aA = (4m1g+m2)(2m2 −

√3m2)λˆ1, aB = −2(4m1g+m2)(2m2−

√3m2)λˆ2, whereλˆ1 isparallelto the slope that mass m1 travels along, pointing down andtotheleft, andλˆ2 isparalleltotheslopethatmass m2 travels along, pointing down and to the right.

- 6.22 ) angular frequency of vibration ≡ λ = 6564mk .


- 6.27a) mx¨ + 4kx = A sinωt + mg, where x is the distance measured from the unstretched position of the center of the pulley.

b) The string will go slack if ω > 4mk 1 − mgA .

- 6.28a) aA = −9mkdA ıˆ.


b) v = 3d mk

A

√39 28 m(ay + g)

6.33 ) TAB = 5

6.36 ) ax > 32g 6.39 ) Can’t solve for TAB.

- 6.51d) Normal reaction at rear wheel: Nr = 2(hmgµ+ww), normal reaction at front wheel: Nf = mg − 2(hmgµ+ww), deceleration of car: acar = −2(hµµg+ww).

- e) Normal reaction at rear wheel: Nr = mg − 2(wmg−wµh), normal reaction at front wheel: Nf = 2(wmg−wµh), deceleration of car: acar = −2(wµ−gwµh). Car stops more quickly for front wheel skidding. Car stops at same rate for front or rear wheel skidding if h = 0.

- f) Normal reaction at rear wheel: Nr = mg(w/w2−µh), normal reaction at front wheel: Nf = mg(w/w2+µh), deceleration of car: acar = −µg.

- g) No. Simple superposition just doesn’t work.
- h) No reaction at rear wheel.
- i) Reaction at rear wheel is negative. Not allowing for rotation of the car in the xy-plane gives rise to this impossibility. In actuality, the rear of the car would ﬂip over the front.


- 6.52a) a = g(sinφ − µcosφ)ıˆ, where ıˆ is parallel to the


slope and pointing downwards

- b) a = g sinφ
- c) v = g(sinφ − µcosφ)tıˆ, r = g(sinφ − µcosφ)t22

- d) v = g sinφtıˆ, r = g sinφt22ıˆ


6.54a) RA = (1−µ)mg2 cosθ (ˆ − µıˆ ). c) No tipping if NA = (1−µ)mg2 cosθ > 0; i.e., no tipping

if µ < 1 since cosθ > 0 for 0 < θ < π2 .(Here µ = 0.9)

6.56 ) braking acceleration= g(12 cosθ − sinθ). 6.60a) v = d mk .

b) The cart undergoes simple harmonic motion for any

size oscillation. 6.63a) abike = FMRpLfc .

b) max( abike)=a+bga+2R

.

f

6.64 ) TEF = 640√2lbf. 6.65a) TBD = 92.6lbm · ft/s2.

- b) TGH = 5√61lbm · ft/s2. 6.66b) TEH = 0

- c) (RCx − TAB)ıˆ + (RCy − T√GD2 )ˆ + (TH E + RCz +


T√GD2 )kˆ = m a = 10Nkˆ.

- d) Mcm = (T√GD2 − TH E − RCz)ıˆ + (RCz − T√GD2 − TH E)ˆ + (TAB + RCx − RCy − T√GD2 )kˆ = 0

- e) RCx − TAB = 0

RCy −

TGD

√2 = 0 RCz +

TGD

√2 + TEH = 5N −TEH +

TGD

√2 − RCz = 0 −TEH −

TGD

√2 + RCz = 0 TAB −

TGD

√2 + RCx − RCy = 0

- f) RCx = 5N, RCy = 5N, RCz = 5N, TGD = √102 N, TEH = 0N, TAB = 5N.

- g)FindmomentaboutCD axis; e.g.,( MC = rcm/C× m acm) · λˆCD, where λˆCD is a unit vector in the direction of axis CD.


- 6.71a) FL = 12mtotg. b) aP = m1tot [2(T − FD) − D]ıˆ. c) F = m mtotw (2T − D − 2FD) − T + FD ı ˆ +

(mwg − FL)ˆ and M = (bFL − amwg)ıˆ + (bFD − cT) + ammw

tot

(2T − D − 2FD)  ˆ.

6.72 ) sideways force = FBıˆ = w2maı ˆ. 7.3 )

- • one solution is r = R(cos(ωt)ıˆ + sin(ωt)ˆ) with R and ω constants,
- • another solution is r = [Atıˆ + Bt2ˆ]/ 1 + 4B2t2/A2,

- • general solution is any motion where speed = v = | v| is a constant.


- 7.17 ) F = 0.52lbf = 2.3N


- 7.24b) For θ = 0◦,


eˆr = ıˆ eˆt = ˆ

2πr

τ ˆ a = −

v =

4π2r

τ2 ıˆ, for θ = 90◦,

eˆr = ˆ eˆt = −ˆı v = −

2πr

τ ıˆ a = −

4π2r

τ2 ˆ,

and for θ = 210◦,

√3

- 1

- 2ˆ


eˆr = −

2 ıˆ − eˆt =

√3

- 1

- 2ıˆ −


2 ˆ v = −

√3πr τ ˆ +

πr

τ ıˆ a =

2√3π2r

2π2r

τ2 ıˆ +

###### τ2 ˆ.

c) T = 4mτπ22r . d) Tension is enough.

7.27b) ( H˙ O)I = 0, ( H˙ O)I I = 0.0080N·mkˆ.

c) Position-A: ( HO)I = 0.012N·m · skˆ,( HO)I I = 0.012N·m · skˆ, Position-B: ( HO)I0.012N·m · skˆ, ( HO)I I = 0.014N·m · skˆ.]

7.29 ) r = k−krmoω2

.

o

7.31 ) 0 = 0.2m 7.33b) T = 0.16π4N.

c) HO = 0.04π2 kg·m/skˆ d) r = [

√2

√2

2 + v sin(π4t )]ˆ. 7.35a) 2mg.

2 − v cos(π4t )]ıˆ + [

√99g/r

###### b) ω =

###### c) r ≈ 1m (r > 0.98m)

7.38 ) (b) θ¨ + 23Lg sinθ = 0 7.41b) The solution is a simple multiple of the person’s

weight.

- 7.43a) θ¨ = −(g/L)sinθ d) α˙ = −(g/L)sinθ, θ˙ = α f) Tmax = 30N
- 7.44a) v˙ = −µvR2. b) v = v0e−µθ.


7.47a) The velocity

of departure is vdep = k(  )m 2 − 2GRˆ, where ˆ is perpendicular to the curved end of the tube.

b) Just before leaving the tube the net force on the pellet is due to the wall and gravity, Fnet = −mgˆ − m | vdep|2

R ıˆ; Just after leaving the tube, the net force

on the pellet is only due to gravity, Fnet = −mgˆ. 7.51 ) at = 20in/s2ˆ., an = −250in/s2ıˆ. 7.65 ) ωmin = 10rpm and ωmax = 240rpm 7.76a) 7.85 kW

- b) 7.85 kW
- c) 750 rev/min
- d) 100N·m.


7.79a) vP = 2m/s.

- b) v P = −2m/sıˆ.
- c) aP = −4m/s2ˆ.
- d) vr = 1m/sλˆr, where λˆr is a unit vector pointing in the direction of the rack, down and to the right.


e) No force needed to move at constant velocity.

- 7.80a) Pin = 7.33kilo-watts


- b) 500rpm
- c) Mout = 140N·m


- 7.84a) αB = 20rad/s2 (CW) b) a = 4m/s2 (up) c) T = 280N.


- 7.86a) FB = 100lbf. c) vright = v.


###### 7.94b)

(b) T = 2.29s (e) T = 1.99s

(b) has a longer period than (e) does since in (b) the moment of inertia about the center of mass (located at the same position as the mass in (e)) is non-zero.

- 7.98a) θ¨ = 0 rad/s2.


b) θ¨ = sinm θ (Dk − mg). 7.99b) −F(t) cosφ − mg sinφ + Tm = −m 2φ¨. 7.100a) (a) F = 0.33Nıˆ − 0.54Nˆ.

7.101a) T(r) = m2ωL2 (L2 − r2) b) at r = 0; i.e., at the center of rotation c) r = L/

√2 7.103 ) Izz = 0.125kg · m2. 7.104a) 0.2kg · m2.

b) 0.29m. 7.105 ) At 0.72 from either end

- 7.106a) (Izz)min = m 2/2, about the midpoint. b) (Izz)max = m 2, about either end
- 7.107a) C

- b) A
- c) IzzA/IzzB = 2
- d) smaller, rgyr = IzzC/(3m) =


√2

- 7.108a) Biggest: IzzO; smallest: IyyO = IxxO .


3 2

m 2 = IyyO. IzzO = 3m 2. d) rgyr = .

b) IxxO =

(M+m2 )+K (M+m3 )L2+M R22

###### 7.113a) ωn = gL

.

(M+m2 )+K (M+m3 )L2 . Frequency higher than in (a)

b) ωn = gL

###### 7.114a) Izzcm = 2m 2b) P ≡ A, B, C, or D

√2

c) rgyr =  /

- 7.115 ) IxxO = IyyO = 0.3kg · m2. 2m bh


b

hx/b

(x2 + y2) dy dx.

- 7.117a) IzzO =


0

0

- 7.128a) Point at 2L/3 from A b) mg/4 directed upwards.


- 7.129c) T = √2π g/ 


1

12(d/ ) + d g) d = 0.29

- 7.132a) Net force: Fnet = −(3mω22L )ıˆ − (mω22L )ˆ, Net moment: Mnet = 0.


b) Net force: Fnet = −(3mω22L )ıˆ + (2mg − mω22L )ˆ,

Net moment: Mnet = 3mgL2

###### kˆ.

- 7.133 ) Trev = 2M3FRO 2pπ .

- 7.139 ) period = π 2km.

- 7.141a) α = θ¨kˆ =?rad/s2kˆ (oops). b) T = 538N.

- 7.142 ) vB = 2gh[mB−2mA(sinθ+µcosθ)] 4mA+mB+4mC KRC

C

2 .

- 7.143 ) am = 0.188m/s2


- 8.13a) r P/O = 0.5m (cosφ)ıˆ + sinφˆ .


b) v P = (0.5ω sinφkˆ)m/s, aP = (−0.5ω2 sinφˆ)m/s2.

- 8.23a) TDB = 0.9N.


- b) F A = −0.3Nıˆ, FC = −0.6Nıˆ
- c) Torquemotor = 0.


- 8.25a) Angles φ for steady circular motion are solutions to 10tanφ = 8 + 40sinφ.


b) φ = [1.3627rad,−0.2735rad,−1.2484rad,−2,9813rad], four solutions, found numerically. Graphically, the solutions are the interns of the curves f1(φ) = 10tanφ and f2(φ) = 8 + 40sinφ between −π and π.

8.28b) Period of revolution= 2ωπ , Period of simple pendu-

lum (for small oscillations)= 2π Lg , where is the length of the pendulum.

c) T = mω2L (strange that φ drops out!), vrock =

−ωL sinφıˆ, arock = −ω2L sinφˆ, dHdtx = −mωL2 sinφ cosφ.

8.29 ) φ = cos−1(ωg2L ). 8.32 ) (a) T = −69.2N, (b) 1.64rad/s < ω < 3.47rad/s

8.36 ) x = −0.554m 8.37b) H˙ O = −121 mω2 2 sinφ cosφkˆ.

c) F A = (121 mω2 2/d sinφ cosφ)ˆ, F B = − F A. d) F A = (121 mω2 2/d sinφ cosφ + 12mg)ˆ, F B  =

###### − F A. 8.40 ) T =

√2mω2R

6 . 8.57a) ω × ([IG] · ω) = 0 kg·m2/s2.

b) ω × ([IG] · ω) = −25ıˆkg·m2/s2. 8.66b) ω2 = 2L3cosg φ, Trev = 2ωπ .

- 8.67a) ω2 = L(2n+3g n1)cosφ.

- 8.68a) [IO] = mL2


 

 ,

4 0 0 0 2 −2 0 −2 2

in terms of the coordinate system shown. b) HO = 2mL2ω(−ˆ + kˆ). c) H˙ O = −2mL2ω2ıˆ. d) F = 0, MO = −2mL2ω2ıˆ.

- 8.69c) RO = −mω2bh(b2−h2) 12(b2+h2)

3 2

kˆ = − RC.

8.70a) aD = IMYYcmy

√2dc

c2+d2

ıˆ. b) B = − MyI

cm Y Z

2IYYcm

√

c2+d2

ıˆ. 8.79a) HO = (−0.108ıˆ + 0.126k )kg·m2/s

- b) HO is in the x z plane at the moment of interest and at an angle α ≈ 41◦, clockwise from the z -axis.
- c) HO does not change in magnitude (m, R, ω, β are

constants). HO rotates with the disk; i.,e., it changes direction.

- d) H˙ O = the rate of change of HO. The tip of HO goes in a circle. At the instant of interest, the change will


be in the ˆ or ˆ direction. Thus, MO = H˙ O will be in the ˆ direction.

8.82a) H˙ cm = 9

√3

128 N·mˆ = 0.122N·mˆ b) H˙ A = −26.89N·mˆ c) RA = −4.56Nıˆ, RC = −13.439Nıˆ, Mz = 0.

- 8.90b) MAz is always zero. c)No. Seeproblems8.68and8.37forcounter-examples.
- 9.1 ) plot(2): θ(t) = br(t) and v = θb˙eˆr + θbθ˙eˆt. 9.1 ) plot(2): x = r cos(br) and y = r sinbr or x =


θ b cos(θ) and y = θb sinθ

9.12 ) v P = ω1L(cosθˆ − sinθıˆ) + (ω1 + ω2)rıˆ, aP =

−ω12L(cosθıˆ + sinθˆ) + (ω1 + ω2)2ˆ. 9.17a)

eˆt =

2t

s ıˆ + e tsˆ 4 ts22 + e2st

at =

4t sm3 + e2st m/s2 4 ts22 + e2st

an =

(2 − 2 ts)e2st m/s2ıˆ + (4 ts22 − 4 ts)e ts m/s2ˆ 4 ts22 + e2st eˆn =

e tsıˆ − 2 tsˆ

4 ts22 + e2st ρ =

(4 ts22 + e2st ) (2 − 2 ts)e ts

m

- 9.22a) acm = mF ıˆ.


- b) α = −6mF

k ˆ.

- c) aA = 4mF ıˆ.

- d) F B = F2 ıˆ


9.25a) a = mF ˆ. b) α = Fd m R22

kˆ. 9.34a) Fout = 37 lb.

b) Fout is always less than the Fin.

- 9.38a) αDisk = −43 rad/s2kˆ. b) aA = 83 m/s2ıˆ.

- 9.40a) aC = (F/m)(1 − Ri/RO)ıˆ. b) (−Ri/RO)Fıˆ.

- 9.45a) speed v = R3θ˙.

b) The energy lost to friction is Ef ric = mR

2θ˙02

6 . The energy lost to friction is independent of µ for µ > 0. Thus, the energy lost to friction is constant for given m, R, and θ˙0. As µ → 0, the transition time to rolling → ∞. It is not true, however, that the energy lost to friction → 0 as µ → 0. Since the energy lost is constant for any µ > 0, the disk will slip for longer and longer times so that the distance of slip goes to inﬁnity. The dissipation rate → 0 since the constant energy is divided by increasing transition time. The energy lost is zero only for µ = 0.

- 9.46 ) V = 2m/s.
- 9.47 ) vo = 2


√

2gR 3 .

- 9.53 ) Accelerations of the center of mass, where ıˆ is parallel to the slope and pointing down: (a) acm = g sinθıˆ, (b) acm = 23g sinθıˆ, (c) acm = 12g sinθıˆ, (d) acm =

- 2

- 3g sinθıˆ. So, the block is fastest, all uniform disks are second, and the hollow pipe is third.


- 9.65 ) h = 2L/3]
- 10.11 ) (g) v P = 8m/sıˆ, aP = 0; (h) v P = 3m/sıˆ, aP = 0.


- 10.12 ) ab = −(s2A + aω2D + 2ωDvb)ıˆ − aω˙ Dkˆ.


- 10.17b) One case: aP = aO , where P refers to the bug; the bugstandsstillontheturntable, thetruckaccelerates, and the turntable does not rotate.


c) One case: aP = aO + aP/D, where D is the turntable; the bug accelerates along a straight line on the turntable, the truck accelerates, and the turntable does not rotate.

- 10.18a) ωO A = θ˙kˆ.


- b) αO A = θ¨kˆ.
- c) v A = −Rθ˙ sinθıˆ + Rθ˙ cosθˆ.
- d) aA = −(Rθ˙2 cosθ + Rθ¨ sinθ)ıˆ + (Rθ¨ cosθ − Rθ˙2 sinθ)ˆ.
- e) ωAB = √−Rθ˙cosθ 2−R2 sin2 θ

.

- f) θ = (2n + 1)π2 , n = 0,±1,±2,....


- 10.21 ) ωDE = −ω2


kˆ = −1.5rad/skˆ 10.22 ) αDE = 3.5rad/s2kˆ

- 10.29 ) One situation: v = Rθ˙eˆθ;the case of a particle constrained to move in a circle.
- 10.30 ) One situation: a = R¨eˆR; the case of no rotation (θ˙ = θ¨ = 0).
- 10.31 ) ωD = (ω1 + ω2)kˆ. 10.33a)


s ıˆ + e tsˆ 4 ts22 + e2st

2t

eˆt =

4t sm3 + e2st m/s2 4 ts22 + e2st

at =

(2 − 2 ts)e2st m/s2ıˆ + (4 ts22 − 4 ts)e ts m/s2ˆ 4 ts22 + e2st eˆn =

an =

e tsıˆ − 2 tsˆ

4 ts22 + e2st ρ =

(4 ts22 + e2st ) (2 − 2 ts)e ts

m

###### 11.9a) R¨(t) − ωo2R(t) = 0.

- b) d2dRθ(θ)2 − R(θ) = 0.

- c) R(θ = 2π) = 267.7ft, R(θ = 4π) = 1.43 × 105 ft.
- d) v = 2378.7ft/s
- e) EK = (2.83 × 106) × (mass)(ft/s)2.


###### 11.10a) R¨ = R0ω2 − 2µR˙0ω.

b) φ = sin−1 1

.

√

1+µ2−µ)2+1

(

- 11.19a) ω− = 4rad/s, where the minus sign ‘-’ means ‘just before leaving’.


- b) ω+ = 4rad/s, where the plus sign ‘+’ means ‘just after leaving’.
- c) vr = 3.841m/s, vt = 2.4m/s.
- d) torque=0.072N·m


- 11.20 ) F = −0.6Nˆ.


√34

- 11.22a) TBC = m


13 (2ax + g).

- b) a = 341 [(25ax + 15g)ıˆ + (15ax − 25g)ˆ]

- c) TBC = m √134(5ax + 3g).


- 11.28a) HO = mL2ω1 + 12mr2(ω1 + ω2) k ˆ.


- b) H˙ O = 0.
- c) HC = 12mr2(ω1 + ω2)kˆ.

- d) H˙ C = 0.


- 11.29 ) F = m a = −109.3Nıˆ − 19.54Nˆ.


- 11.31b) θ¨ = −23Lg cosθ.


c) From the diagram, we see ω˙AB = −θ(¨ t = 0)kˆ =

3g

- 2L cosθ0, aG = 34g cosθ0[sinθ0ıˆ − cosθ0ˆ].

- d) RA = 34mg sinθ0 cosθ0ıˆ, RB = mg[1 −

3 4g cos2 θ0]ˆ.

- e) aB = 32g sinθ0 cosθ0ıˆ.

- f) At θ = θ20 , ωAB = 3Lg(sinθ0 − sin θ20 )kˆ, aA = −3g 12 cos2 θ20 + sin θ20(sinθ0 − sin θ20 )  ˆ.




- 11.37 ) There are many solution methods. −8π2 poundals


to the left. (Note: 1 poundal = 1ft · lbm · s−2.)

2 0

- 11.40a) = (Mc+6Mw)v


k .

- b) Tangential forces point toward the wall!
- c) = (Mc+4Mw)v


2 0

k .

###### 11.45a) −k(xıˆ + yˆ) = m(x¨ıˆ + y¨ˆ).

- b) −kreˆr = m(r¨ − rθ˙2)eˆr + m(rθ¨ + 2r˙θ)˙ eˆt.
- c) dtd (xy˙ − yx˙) = 0.

- d) dtd (r2θ)˙ = 0.

- e)dotequationin(a)with(xˆ−yıˆ)toget(xy¨−yx¨) = 0 whichcanberewrittenas(c); dotequationin(b)with

eˆt to get (rθ¨ + 2r˙θ)˙ = 0 which can be rewritten as (d).

- f) 12m(x˙2 + y˙2) + 12k(x2 + y2) = const.

- g) 12m(r˙2 + (rθ)˙ 2) + 12kr2=const.

- h) dot equation in (a) with v = x˙ıˆ + y˙ˆ to get m(x¨x˙ + y¨y˙)+k(xx˙ + yy˙ ) = 0 which can be rewritten as (f).
- i) x = A1 sin(ωt + B1), y = A2 sin(ωt + B2), where ω = mk . The general motion is an ellipse.

- j) Yes. Consider B1 = B2 = 0, A1 = 1, and A2 = 2.


###### 11.46a) 0.33mıˆ

- b) vC = 1.82m/sıˆ.
- c) T ≈ 240N.

11.52b)

R¨ − Rθ˙2 = 0 (Izz + mR2)θ¨ + 2mRR˙θ˙ = 0

c)Thesecondequationinpart(b)canberewritteninthe

form dtd Izz + mR2)θ˙ = 0. The quantity inside the derivativeisangularmomentum; thus, itisconserved

and equal to a constant, say, (H/o)0, which can be found in terms of the initial conditions.

- d) R¨ − R (Ho)

2 0

(IzzO+mR2)2 = 0.

- e) E0 = 12mR˙2 + 12ω(H/o)0.

- f) The bead’s distance goes to inﬁnity and its speed approaches a constant. The turntable’s angular velocity goes to zero and its net angle of twist goes to a constant.


###### 11.53a)

θ˙ = ω ω˙ = −

2mRvω Izz + mR2

R˙ = v v˙ = ω2R

11.55 ) v2x = 2g(a−b)tanφ

, v2y = v2x n+n1 tanφ,

2 tan2 φ)

(1+n1 + n+n1

v1x = −vn2x , v1y = 0, where 2 refers to the top wedge and 1 refers to the lower wedge.

√3

4 ıˆ + 34ˆ . b) For a0 = −g, the acceleration of the mass is exactly

###### 11.56a) F = m(g + a0)

vertical; d0, v0, and t could be anything.

###### 11.57a) angular speed = 8.8rad/s.b) displacement = 0.5ft.

11.68a) For point mass: φ¨ = (g/L)sinφ −(ahand/L)cosφ.

b) There are many correct solutions. Test your solution with a computer simulation. Show your result with appropriate plots.

- 11.69e) φ¨ − y ¨+Lg sinφ = 0, where y(t) is the vertical displacement of your hand and φ(t) is the angle of the broom from the vertical.

- 11.70 ) φ¨1 = 0, φ¨2 = −3g/2 .

- 11.71a) φ¨ + 3(R − L2 )Lg2 φ = 0. b) This ﬁrst-order approximation show that stable

standing requires R > L2 . R = L2 is neutrally stable (like a wheel).

- 12.7i) −(cosθıˆ + sinθˆ).


- 12.10 ) Net force: F = m(−omega02L)ˆ, Net moment: M/G = 12mr2(−ω0ω1ıˆ + ω0ω2ˆ − ω1ω2kˆ).


- 12.11 ) aP = 0.732gkˆ.


kˆ.

- 12.12a) ωcar = vRo


- b) ωtire/car = −vro eˆr, where eˆr is parallel to the axle of the wheel and moves with the car and k is perpendicular to the ground.

- c) ωtire = vRo

kˆ − vro eˆr.

- d) total torque, M = 0.
- e) M = 0.
- f) Hcm = mv4or2 −r2eˆr + R1

kˆ .

- g) H˙ cm = H˙ cm = −mv

2 or

2R eˆt.

- h) Mcm = −mv

2 or

2R eˆt.

- i) abug = −v


2 o

R eˆr + vorvg eˆt, Fbug = mbug abug.

- 12.14a) aG = mF


kˆ.

- b) ω˙ = mL3F (ıˆ − ˆ).

- c) aB = 4mF


kˆ. kˆ. b) ω˙ = (96ıˆ + 48ˆ)rad/s2

- 12.15a) aB = 4mF


- 12.26a) ωD/F = k ˆ + ωˆ.


- b) αD/F = − ωıˆ.
- c) vB = Rˆ + 12ωDıˆ.

- d) aB = − 2Rıˆ +  ωDˆ − 12ω2Dkˆ.


- 12.27 ) ωD/F = ω2ıˆ + ω1ˆ + ω0kˆ.


- 12.30a) vB = −√ω1h2 h2+r2


###### kˆ.

kˆ.

###### b) αC/F = − ω1ω21+ h r

2

###### c) ω1 = √ ω2h2+r2

.

2 .

###### d) αC/F = hrv2 1 + h r

- 12.33 ) F ω˙D = −ω0ω1ıˆ + ω0ω2ˆ − ω1ω2kˆ.


- 12.36b) aP = −(  ˙ +2r ωs)ıˆ+(2r ωc− 2)ˆ−r(ωc2+ ωs2)kˆ.


12.38a) H/G = 12mr2ω2ıˆ + 14mr2ω1ˆ + mω0(L2 + 14r2)kˆ, H˙ /G = 12mr2(−ω0ω1ıˆ + ω0ω2ˆ − ω1ω2kˆ).

b) H/E = 12mr2ω2ıˆ+ 14mr2ω1ˆ+ 14mr2ω0kˆ, H˙ /E = H˙ /G = 12mr2(−ω0ω1ıˆ + ω0ω2ˆ − ω1ω2kˆ). 12.39 ) Ay = −3.16N, By = 3.16N, Az = Bz =

−63.16N 12.48 ) ωD = 2π(2ıˆ + ˆ)rad/s and αD = 8π2kˆ rad/s2 12.50a) ωD = (2ıˆ + 4πkˆ)rad/s

- b) αD = −8π rad/s2ˆ
- c) M = −π2 N·mˆ

- d) RA = π2 Nıˆ, RB = − RA


12.52 ) N = ω22mR

kˆ

