![image 1](Matrix Analysis of Framed Structures_images/imageFile1.png)

![image 2](Matrix Analysis of Framed Structures_images/imageFile2.png)

Matrix Analysis

###### ofFramed Structures

![image 3](Matrix Analysis of Framed Structures_images/imageFile3.png)

###### Matrix Analysis ofFramed Structures

###### Third Edition

###### William Weaver, Jr.

Professor Emeritus ofStructural Engineering, Stanford University

###### James M. Gere

Professor Emeritus ofStructural Engineering, Stanford University

###### ~ VAN NOSTRAND REINHOLD

~ _______ New York

![image 4](Matrix Analysis of Framed Structures_images/imageFile4.png)

Copyright © 1990 by Van Nostrand Reinhold Softcover reprint ofthe hardcover 1st edition 1990

Library of Congress Catalog Card Number 89-21458 ISBN-13: 978-1-4684-7489-3

All rights reserved. Certain portions of this work © 1965, 1980 by Van Nostrand Reinhold. No part of this work covered by the copyright hereon may be reproduced or used in any form or by any means-graphic, electronic, or mechanical, including photocopying, recording, taping, or information storage and retrieval systems-without written permission of the publisher.

Van Nostrand Reinhold 115 Fifth Avenue New York, New York 10003

Van Nostrand Reinhold International Company Limited 11 New Fetter Lane London EC4P 4EE, England

Van Nostrand Reinhold 480 La Trobe Street Melbourne, Victoria 3000, Australia

Nelson Canada 1120 Birchmount Road Scarborough, Ontario M1K 5G4, Canada

16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 Library of Congress Cataloging-in-Publication Data Weaver, William, 1929-

Matrix analysis of framed structures/William Weaver, Jr., James M. Gere.-3rd ed.

p. cm. Includes bibliographical references. ISBN-13: 978-1-4684-7489-3 e-ISBN-13: 978-1-4684-7487-9 DOl: 10.1007/978-1-4684-7487-9

2. Matrices. I. Gere,

1. Structural analysis (Engineering) James M. II. Title. TA645.W36 1990 624.1 '773-dc20

89-21458 C1P

![image 5](Matrix Analysis of Framed Structures_images/imageFile5.png)

###### Preface

Matrix analysis of structures is a vital subject to every structural analyst, whether working in aero-astro, civil, or mechanical engineering. It provides a comprehensive approach to the analysis of a wide variety of structural types, and therefore offers a major advantage over traditional metho~ which often differ for each type of structure. The matrix approach also provides an efficient means of describing various steps in the analysis and is easily programmed for digital computers. Use of matrices is natural when performing calculations with a digital computer, because matrices permit large groups of numbers to be manipulated in a simple and effective manner.

This book, now in its third edition, was written for both college students and engineers in industry. It serves as a textbook for courses at either the senior or first-year graduate level, and it also provides a permanent reference for practicing engineers. The book explains both the theory and the practical implementation of matrix methods of structural analysis. Emphasis is placed on developing a physical understanding of the theory and the ability to use computer programs for performing structural calculations.

In preparing this new edition, we have tried to maintain the strengths of the earlier editions while also adding new material to allow personal computers to be used in the solution of problems. The direct stiffness method is presented in detail because it is the best and most general approach for the analysis of structures by digital computation. The flexibility method is included as a supplementary method, partly for completeness and partly because it often is necessary to obtain stiffnesses and fixed-end actions by flexibility techniques.

Throughout the book, new examples and problems have been added to aid in teaching the subject. Two new topics, repeated substructures and the omission of axial strains in frames, are now included in Chapter 6. A new chapter, "Finite-Element Method for Framed Structures," has been added at the end of the text to show how the analysis of framed structures fits within the scope of the more general finite-element method. This chapter also provides an introduction to the finite-element method, using only onedimensional elements to model the slender members of framed structures.

Prerequisites for the study of matrix analysis of structures are statics, mechanics of materials, algebra, and introductory calculus. In addition, a previous course in elementary structural analysis is certainly beneficial, although not essential. Elementary matrix algebra is used throughout the

v

![image 6](Matrix Analysis of Framed Structures_images/imageFile6.png)

vi Preface

book, and the reader must be familiar with basic matrix operations, such as addition, multiplication, and inversion. Because these topics are not difficult, the reader can acquire the necessary knowledge of matrices through self-study during a period of only two or three weeks.

Computer programs for the six basic types of framed structures are given in Chapter 5 in the form ofFORTRAN-oriented flow charts. These programs are available on a diskette that also contains the data for all examples shown in that chapter. The diskette may be purchased from Dr. Paul R. Johnston, Manager, Structural Analysis, Failure Analysis Associates, 149 Commonwealth Drive, Menlo Park, CA 94025 [phone (415) 688-7210]. For this purpose, a tear-out order form is included at the back of the book.

The first chapter of the book covers the fundamental concepts of structural analysis that are needed for the remaining chapters. Those who have previously studied structural theory will find that this material is mostly review. However, anyone encountering this subject for the first time will need to become thoroughly familiar with the basic topics presented here.

The flexibility and stiffness methods are introduced in Chapters 2 and 3, respectively. Each of these chapters explains the theory in detail, with examples and problems, and concludes with a section on formalizing the method (Sections 2.7 and 3.6). Although these last sections show the general mathematical approach, they are indirect and are not needed for implementing the methods. In Chapter 4 the direct stiffness method is developed further in a computer-oriented manner, as preparation for programming. Then in Chapter 5 the stiffness method is applied in FORTRAN-oriented flow charts of programs for the analysis of the six basic types of framed structures.

Because the emphasis in the first five chapters is on fundamental concepts, the treatment of many special topics is postponed to Chapter 6. Included in that chapter are such matters as symmetric structures, nonprismatic members, elastic connections, and so on. These topics can be considered as modifications of the basic procedures described in earlier chapters. As already explained, a new Chapter 7 describes how the finite-element method can be applied to framed structures.

Problems for hand solution are given at the ends of the chapters, and they are generally placed in order of increasing difficulty. New problems have been added to all problem sets, and those of Chapter 6 are completely new. The examples and problems in Chapters 1, 2, 3, and 6 (and the Appendixes) are in literal form. Numerical examples and problems of Chapters 4 and 5 are in both US and SI units.

References for further study, lists of notations, five appendixes, and answers to problems are at the end of the book. The appendixes contain tables of useful information, a description of the unit-load method for calculating displacements (Appendix A), and computer routines for solving equations (Appendix D).

![image 7](Matrix Analysis of Framed Structures_images/imageFile7.png)

Preface vii

The authors wish to thank the graduate students at Stanford and the teachers at other colleges and universities who contributed ideas to this book. Special appreciation is due Paul R. Johnston, who modified the programs for use with personal computers and produced new outputs for Chapter 5. Jeffrey E. Jones solved and organized the problem sets in an excellent manner, using a text editor on his own computer. Finally, Judith C. Clark did an outstanding job of word processing for parts of the revised manuscript.

William Weaver, Jr. James M. Gere

![image 8](Matrix Analysis of Framed Structures_images/imageFile8.png)

###### Contents

Preface/v

- 1 Basic Concepts of Structural Analysis/ 1

1. 1 Introduction /1 1.2 Types of Framed Structures/1

1. 3 Defonnations in Framed Structures /4 1.4 Actions and Displacements/ 7

1. 5 Equilibrium/13

- 1.6 Compatibility / 14
- 1.7 Static and Kinematic Indetenninacy / 14


1. 8 Structural Mobilities /21

- 1.9 Principle of Superposition/22
- 1.10 Action and Displacement Equations /25
- 1.11 Flexibility and Stiffness Matrices /31
- 1.12 Equivalent Joint Loads/36
- 1.13 Energy Concepts /38
- 1.14 Virtual Work/44 References /48 Problems /48


- 2 Fundamentals of the Flexibility Method/ 55

- 2.1 Introduction/ 55
- 2.2 Flexibility Method/55
- 2.3 Examples/63
- 2.4 Temperature Changes, Prestrains, and Support Displacements/75
- 2.5 Joint Displacements, Member End-Actions, and Support Reactions / 80
- 2.6 Flexibilities of Prismatic Members/86
- 2.7 Fonnalization of the Flexibility Method /92 Problems /107


- 3 Fundamentals of the Stiffness Method/ 117


- 3.1 Introduction /117
- 3.2 Stiffness Method /117
- 3.3 Examples / 129


ix

![image 9](Matrix Analysis of Framed Structures_images/imageFile9.png)

x Contents

- 3.4 Temperature Changes, Prestrains and Support Displacements/149
- 3.5 Stiffness of Prismatic Members/153
- 3.6 Formalization of the Stiffness Method/157 Problems / 168


- 4 Computer-Oriented Direct Stiffness Method/181

- 4.1 Introduction/ 181
- 4.2 Direct Stiffness Method /181
- 4.3 Complete Member Stiffness Matrices/ 184
- 4.4 Formation of Joint Stiffness Matrix /192
- 4.5 Formation of Load Vector/ 193
- 4.6 Rearrangement of Stiffness and Load Arrays / 196
- 4.7 Calculation of Results/197
- 4.8 Analysis of Continuous Beams/199
- 4.9 Example/209
- 4.10 Plane Truss Member Stiffnesses /215
- 4.11 Analysis of Plane Trusses/219
- 4.12 Example/228
- 4.13 Rotation of Axes in Two Dimensions /233
- 4.14 Application to Plane Truss Members/235
- 4.15 Rotation of Axes in Three Dimensions/239
- 4.16 Plane Frame Member Stiffnesses/24I
- 4.17 Analysis of Plane Frames /245
- 4.18 Example/250
- 4.19 Grid Member Stiffnesses /254
- 4.20 Analysis of Grids/258
- 4.21 Space Truss Member Stiffnesses/26I
- 4.22 Selection of Space Truss Member Axes/263
- 4.23 Analysis of Space Trusses/267
- 4.24 Space Frame Member Stiffnesses /270
- 4.25 Analysis of Space Frames/277 Problems /281


- 5 Computer Programs for Framed Structures/291


5. 1 Introduction/ 291

- 5.2 FORTRAN Programming and Flow Charts/291
- 5.3 Program Notation/298
- 5.4 Preparation of Data/ 300
- 5.5 Description of Programs/306
- 5.6 Continuous Beam Program /309
- 5.7 Plane Truss Program/325
- 5.8 Plane Frame Program/330
- 5.9 Grid Program/ 340
- 5.10 Space Truss Program/345


![image 10](Matrix Analysis of Framed Structures_images/imageFile10.png)

Contents

xi

- 5.11 Space Frame Program/353
- 5.12 Combined Program for Framed Structures/368 References /372


- 6 Additional Topics for the Stiffness Method/373

- 6.1 Introduction/373
- 6.2 Rectangular Framing/374
- 6.3 Symmetric and Repeated Structures /378
- 6.4 Loads Between Joints/383
- 6.5 Automatic Dead Load Analysis/386
- 6.6 Temperature Changes and Prestrains/387
- 6.7 Support Displacements/388
- 6.8 Oblique Supports/389
- 6.9 Elastic Supports /391
- 6.10 Translation ofAxes/394
- 6.11 Member Stiffnesses and Fixed-End Actions from Flexibilities/396
- 6.12 Nonprismatic Members /402


- 6. 13 Curved Members /409
- 6. 14 Releases in Members/414
- 6. 15 Elastic Connections /419
- 6.16 Shearing Deformations/422
- 6.17 Offset Connections /424
- 6.18 Axial-Flexural Interactions /428
- 6.19 Axial Constraints in Frames /432 References /441 Problems /442


- 7 Finite-Element Method for Framed Structures/447


7. 1 Introduction/447

- 7.2 Stresses and Strains in Continua/448
- 7.3 Virtual-Work Basis of Finite-Element Method/449
- 7.4 One-Dimensional Elements/453
- 7.5 Application to Framed Structures /464 References /467


General References /468 Notation /470

- Appendix A. Displacements of Framed Structures /476 A.l Stresses and Deformations in Slender Members /476


- A.2 Displacements by the Unit-Load Method/485
- A.3 Displacements of Beams /493
- A.4 Integrals of Products for Computing Displacements /493 References /495


![image 11](Matrix Analysis of Framed Structures_images/imageFile11.png)

Contents

xii

- Appendix B. End-Actions for Restrained Members/498
- Appendix C. Properties of Sections/505
- Appendix D. Computer Routines for Solving Equations/506 D.I Factorization Method for Symmetric Matrices/506

- D.2 Subprogram FACTOR/512
- D.3 Subprogram SOLVER/514
- D.4 Subprogram BANFAC/514
- D.5 Subprogram BANSOL/518 References /518


- Appendix E. Solution without Rearrangement/ 520 Answers to Problems /523 Index/541 Order Form for Diskette /547


![image 12](Matrix Analysis of Framed Structures_images/imageFile12.png)

###### 1Basic Concepts ofStructural Analysis

1.1 Introduction. This book describes matrix methods for the analysis of framed structures with the aid of a digital computer. Both the flexibility and stiffness methods of structural analysis are covered, but emphasis is placed upon the latter because it is more suitable for computer programming. While these methods are applicable to discretized structures of all types, only framed structures will be discussed. After mastering the analysis of framed structures, the reader will be prepared to study the finite element method for analyzing more elaborate discretized continua (see Chapter 7 and textbooks on finite elements listed in General References).

In this chapter various preliminary matters are considered in preparation for the matrix methods of later chapters. These subjects include descriptions of the types of framed structures to be analyzed and their deformations due to loads and other causes. Also discussed are the basic concepts of equilibrium, compatibility, determinacy, mobility, superposition, flexibility and stiffness coefficients, equivalent joint loads, energy, and virtual work.

1.2 Types of Framed Structures. All of the structures that are analyzed in later chapters are called framed structures and can be divided into six categories: beams, plane trusses, space trusses, plane frames, grids, and space frames. These types of structures are illustrated in Fig. I-I and described later in detail. These categories are selected because each represents a class of structures having special characteristics. Furthermore, while the basic principles of the flexibility and stiffness methods are the same for all types of structures, the analyses for these six categories are sufficiently different in the details to warrant separate discussions of them.

Every framed structure consists of members that are long in comparison to their cross-sectional dimensions. The joints of a framed structure are points of intersection of the members, as well as points of support and free ends of members. Examples of joints are points A, B, C, and D in Figs. I-Ia and l-ld. Supports may befixed, as at support A in the beam of Fig. I-la, or pinned, as shown for support A in the plane frame of Fig. I-Id, or there may be roller supports, illustrated by supports Band C in Fig. I-Ia. In special instances the connections between members or between members and supports may be elastic (or semi-rigid). However, the discussion of this possibility will be postponed until later (see Secs. 6.9 and 6.15). Loads on a framed structure may be concentrated forces, distributed loads, or couples.

1

![image 13](Matrix Analysis of Framed Structures_images/imageFile13.png)

- 2 Chapter 1 Basic Concepts of Structural Analysis


Consider now the distinguishing features of each type of structure shown in Fig. 1-1. A beam (Fig. 1-1 a) consists of a straight member having one or more points of support, such as points A, B, and C. Forces applied to a beam are assumed to act in a plane which contains an axis of symmetry of the cross section of the beam (an axis of symmetry is also a principal axis of the cross section). Moreover, all external couples acting on the beam have their moment vectors normal to this plane, and the beam deflects in the same plane (the plane ofbending) without twist. (The case of a beam which does not fulfill these criteria is discussed in Sec. 6.17.) Internal stress resultants may exist at any cross section of the beam and, in the general case, may include an axial force, a shearing force, and a bending moment.

A plane truss (Fig. 1-1 b) is idealized as a system of members lying in a plane and interconnected at hinged joints. All applied forces are assumed to act in the plane of the structure, and all external couples have their moment vectors normal to the plane, just as in the case of a beam. The loads may consist of concentrated forces applied at the joints, as well as loads that act on the members themselves. For purposes of analysis, the latter loads may be replaced by statically equivalent loads acting at the joints. Then the analysis of a truss subjected only to joint loads will result in axial forces of tension or compression in the members. In addition to these axial forces, there will be bending moments and shearing forces in those members having loads that act directly upon them.

A space truss (see Fig. 1-1 c) is similar to a plane truss, except that the members may have any directions in space. The forces acting on a space truss may be in arbitrary directions, but any couple acting on a member must have its moment vector perpendicular to the axis of the member. The reason for this requirement is that a truss member is incapable of supporting a twisting moment.

A plane frame (Fig. I-ld) is composed of members lying in a single plane and having axes of symmetry in that plane (as in the case of a beam). The joints between members (such as joints B and C) are rigid connections. The forces acting on a frame and the translations of the frame are in the plane of the structure; all couples acting on the frame have their moment vectors normal to the plane. The internal stress resultants acting at any cross section of a plane frame member may consist in general of a bending moment, a shearing force, and an axial force.

A grid is a plane structure composed of continuous members that either intersect or cross one another (see Fig. I-Ie). In the latter case the connections between members are often considered to be hinged, whereas in the former case the connections are assumed to be rigid. While in a plane frame the applied forces all lie in the plane of the structure, those applied to a grid are normal to the plane of the structure; and all couples have their vectors in the plane of the grid. This orientation of loading may result in torsion as well as bending in some of the members. Each member is assumed to have two axes of symmetry in the cross section, so that bending and torsion occur

![image 14](Matrix Analysis of Framed Structures_images/imageFile14.png)

- 1.2 Types of Framed Structures 3


![image 15](Matrix Analysis of Framed Structures_images/imageFile15.png)

![image 16](Matrix Analysis of Framed Structures_images/imageFile16.png)

(0)

![image 17](Matrix Analysis of Framed Structures_images/imageFile17.png)

( b)

![image 18](Matrix Analysis of Framed Structures_images/imageFile18.png)

(e) -)

###### A

(d)

![image 19](Matrix Analysis of Framed Structures_images/imageFile19.png)

![image 20](Matrix Analysis of Framed Structures_images/imageFile20.png)

(e)

- Fig. 1-1. Types of framed structures: (a) beam, (b) plane truss, (c) space truss,


- (d) plane frame, (e) grid, and (f) space frame.


independently of one another (see Sec. 6.17 for a discussion of nonsymmetric members).

The final type of structure is a space frame (Fig. 1-1f). This is the most general type of framed structure, inasmuch as there are no restrictions on the locations of joints, directions of members, or directions of loads. The individual members of a space frame may carry internal axial forces, torsional moments, bending moments in both principal directions of the cross section, and shearing forces in both principal directions. The members are assumed to have two axes of symmetry in the cross section, as explained above for a grid.

The reader should be aware that not all framed structures fit neatly into the six categories described above. For example, some plane and space

![image 21](Matrix Analysis of Framed Structures_images/imageFile21.png)

4 Chapter 1 Basic Concepts of Structural Analysis

frames contain members that are pinned at their ends and function as truss members. Such members can be created from frame members by releasing their ends from transmitting moments, as described in Sec. 6.14. Other topics in Chapter 6 provide modifications to make the analytical models for framed structures more versatile.

However, the slender members in framed structures are normally considered to be only one-dimensional. If two- and three-dimensional parts (such as plates, shells, and solids) appear in the analytical model, the method of finite elements is required. After discretization by that approach, the analysis proceeds in a manner similar to that for framed structures.

It will be assumed throughout most of the subsequent discussions that the structures being considered have prismatic members; that is, each member has a straight axis and uniform cross section throughout its length. Nonprismatic members are treated later by a modification of the basic approach (see Sec. 6.12).

1.3 Deformations in Framed Structures. When a structure is acted upon by loads, the members of the structure will undergo deformations (or small changes in shape) and, as a consequence, points within the structure will be displaced to new positions. In general, all points of the structure except immovable points of support will undergo such displacements. The calculation of these displacements is an essential part of structural analysis,

- as will be seen later in the discussions of the flexibility and stiffness methods. However, before considering the displacements, it is first necessary to have an understanding of the deformations that produce the displacements.


To begin the discussion, consider a segment of arbitrary length cut from a member of a framed structure, as shown in Fig. 1-2a. For simplicity the bar is assumed to have a circular cross section. At any cross section, such

- as at the right-hand end of the segment, there will be stress resultants that in the general case consist of three forces and three couples. The forces are the axial force Nx and the shearing forces V\, and Vz; the couples are the twisting moment Tx and the bending moments My and Mz. Note that moment vectors are shown in the figure with double-headed arrows, in order to distinguish them from force vectors. The deformations of the bar can be analyzed by taking separately each stress resultant and determining its effect on an infinitesimal element of the bar. Such an element is obtained by isolating a portion of the bar between two cross sections a small distance dx apart (see Fig. 1-2a).


The effect of the axial force Nx on the element is shown in Fig. 1-2b. Assuming that the force acts through the centroid of the cross-sectional area, it is found that the element is uniformly extended, the significant strains in the element being normal strains in the x direction. In the case of a shearing force Vy (Fig. 1-2c), one cross section of the bar is displaced laterally with respect to the other. There may also be some distortion of the cross sections, but this usually has a negligible effect on the determination ofdisplacements

![image 22](Matrix Analysis of Framed Structures_images/imageFile22.png)

- 1.3 Deformations in Framed Structures


5

y

![image 23](Matrix Analysis of Framed Structures_images/imageFile23.png)

I "

###### I \ I \

O~/ -------xI

###### // J

/

(0)

![image 24](Matrix Analysis of Framed Structures_images/imageFile24.png)

![image 25](Matrix Analysis of Framed Structures_images/imageFile25.png)

###### dx

( b )

(c )

![image 26](Matrix Analysis of Framed Structures_images/imageFile26.png)

![image 27](Matrix Analysis of Framed Structures_images/imageFile27.png)

###### McB"+",)M'

I I

l .1

###### dx

(d)

(e)

- Fig. 1-2. Types of deformations: (b) axial, (e) shearing, (d) flexural, and


- (e) torsional.


and can be disregarded. A bending moment Mz (Fig. 1-2d) causes relative rotation of the two cross sections so that they are no longer parallel to one another. The resulting strains in the element are in the longitudinal direction of the bar, and they consist of contraction on the compression side and extension on the tension side. Finally, the twisting moment Tx causes a relative rotation of the two cross sections about the x axis (see Fig. 1-2e) and, for example, point A is displaced to A'. In the case of a circular bar, twisting produces only shearing strains; and the cross sections remain plane. For other cross-sectional shapes, distortion of the cross sections will occur.

The deformations shown in Figs. I-2b, I-2c, I-2d, and I-2e are called axial, shearing, flexural, and torsional deformations, respectively. Their evaluation is dependent upon the cross-sectional shape of the bar and the mechanical properties of the material. This book is concerned only with materials that are linearly elastic, that is, materials that follow Hooke's law. For such materials the various formulas for the deformations, as well as

![image 28](Matrix Analysis of Framed Structures_images/imageFile28.png)

6 Chapter 1 Basic Concepts of Structural Analysis

those for the stresses and strains in the element, are given for reference purposes in Appendix A, Sec. A.l.

Figure 1-2 shows two sets of sign conventions that are intended for different purposes. The first convention appears in Fig. 1-2a, where the actions Nn Vy, • • ., Mz are in the positive directions of the reference axes x, y, and z for the purpose of writing equilibrium equations (see Sec. 1.5). This rule is commonly known as the "statics" sign convention. On the other hand, the infinitesimal elements in Figs. 1-2b through 1-2e have equal and opposite internal stress resultants causing their deformations. The positive senses of these actions and the corresponding deformations will be taken (arbitrarily) as shown in the figures. This "beam" sign convention allows thrust, shear, moment, and torque diagrams to be plotted along the length of the bar. Both of these sign conventions could be reversed if desired, but those given in the figures are usually the preferred choices.

The displacements in a structure are caused by the cumulative effects of the deformations of all the elements. There are several ways of calculating these displacements in framed structures, depending upon the type of deformation being considered as well as the type of structure. For example, deflections of beams considering only flexural deformations can be found by direct integration of the differential equation for bending ofa beam. Another method, which can be used for all types of framed structures including beams, trusses, grids, and frames, is the unit-load method, discussed later in Sec. 1.14. In both of these methods, as well as others in common use, it is assumed that the displacements of the structure are small.

In any particular structure under investigation, not all types of deformations will be of significance in calculating the displacements. For example, in beams the flexural deformations normally are the only ones ofimportance, and it is usual to ignore the axial deformations. Of course, there are exceptional situations in which beams are required to carry large axial forces, and under such circumstances the axial deformation must be included in the analysis. It is also possible for axial forces to produce a beam-column action which has a nonlinear effect on the displacements (see Sec. 6.18).

For truss structures of the types shown in Figs. 1-lb and 1-lc, the analyses are made in two parts. If the joints of the truss are idealized as hinges and if all loads act only at the joints, then the analysis involves only axial deformations of the members. The second part of the analysis is for the effects of the loads that act on the members between the joints, and this part is essentially the analysis of simply supported beams. If the joints of a truss-like structure actually are rigid, then bending occurs in the members even though all loads may act at the joints. In such a case, flexural deformations could be important, and in this event the structure may be analyzed as a plane or space frame.

In plane frames (see Fig. I-ld) the significant deformations are flexural and axial. Ifthe members are slender and are not triangulated in the fashion ofa truss, the flexural deformations are much more important than the axial

![image 29](Matrix Analysis of Framed Structures_images/imageFile29.png)

ones. However, the axial contributions should be included in the analysis of a plane frame if there is any doubt about their relative importance.

In grid structures (Fig. I-Ie) the flexural deformations are always important, but the cross-sectional properties of the members and the method of fabricating joints will determine whether or not torsional deformations must be considered. If the members are thin-walled open sections, such as 1beams, they are likely to be very flexible in torsion, and large twisting moments will not develop in the members. Also, if the members of a grid are not rigidly connected at crossing points, there will be no interaction between the flexural and torsional moments. In either of these cases, only flexural deformations need be taken into account in the analysis. On the other hand, if the members of a grid are torsionally stiff and rigidly interconnected at crossing points, the analysis must include both torsional and flexural deformations. Usually, there are no axial forces present in a grid because the forces are normal to the plane of the grid. This situation is analogous to that in a beam having all its loads perpendicular to the axis of the beam, in which case there are no axial forces in the beam. Thus, axial deformations are not included in a grid analysis.

Space frames (Fig. 1-1f) represent the most general type of framed structure, with respect to both geometry and loads. Therefore, it follows that axial, flexural, and torsional deformations all may enter into the analysis of a space frame, depending upon the particular structure and loads.

Shearing deformations are usually very small in framed structures and hence are seldom considered in the analysis. However, their effects may always be included if necessary in the analysis of a beam, plane frame, grid, or space frame (see Sec. 6.16).

There are other effects, such as temperature changes and prestrains, that may be of importance in analyzing a structure. These subjects are discussed in later chapters in conjunction with the flexibility and stiffness methods of analysis.

1.4 Actions and Displacements. The terms "action" and "displacement" are used to describe certain fundamental concepts in structural analysis. An action (sometimes called a generalized force) is most commonly a single force or a couple. However, an action may also be a combination of forces and couples, a distributed loading, or a combination of these actions. In such combined cases, however, it is necessary that all the forces, couples, and distributed loads be related to one another in some definite manner so that the entire combination can be denoted by a single symbol. For example, if the loading on the simply supported beam AB shown in Fig. 1-3 consists oftwo equal forces P, it is possible to consider the combination of the two loads as a single action and to denote it by one symbol, such as

- F. It is also possible to think of the combination of the two loads plus the two reactions RA and RB at the supports as a single action, since all four


![image 30](Matrix Analysis of Framed Structures_images/imageFile30.png)

- 8 Chapter 1 Basic Concepts of Structural Analysis


A ( ( 8

###### A A

RA1--LI3-+-LI3---+-L13-1Rs

Fig. 1-3.

forces have a unique relationship to one another. In a more general situation, it is possible for a very complicated loading system on a structure to be treated as a single action if all components of the load are related to one another in a definite manner.

In addition to actions that are external to a structure, it is necessary to deal also with internal actions. These actions are the resultants of internal stress distributions, and they include bending moments, shearing forces, axial forces, and twisting moments. Depending upon the particular analysis being made, such actions may appear as one force, one couple, two forces, or two couples. For example, in making static equilibrium analyses of structures these actions normally appear as single forces and couples, a:s illustrated in Fig. 1-4a. The cantilever beam shown in the figure is subjected

- at end B to loads in the form of actions PI and MI' At the fixed end A the reactive force and reactive couple are denoted RA and M A, respectively. In order to distinguish these reactions from the loads on the structure, they are drawn with a slanted line (or slash) across the arrow. This convention for identifying reactions will be followed throughout the text (see also Fig. 1-3 for an illustration of the use of the convention). In calculating the axial


(0 )

-----2st(c) r 8

(b)

Fig. 1-4.

![image 31](Matrix Analysis of Framed Structures_images/imageFile31.png)

force N, bending moment M, and shearing force V at any section of the beam in Fig. 1-4a, such as at the midpoint, it is necessary to consider the static equilibrium of a portion of the beam. One possibility is to construct a free-body diagram of the right-hand half of the beam, as shown in Fig. 1-4b. In so doing, it is evident that each of the internal actions appears in the diagram as a single force or couple.

There are situations, however, in which the internal actions appear as two forces or couples. This case occurs most commonly in structural analysis when a "release" is made at some point in a structure, as shown in Fig. 1-5 for a continuous beam. If the bending moment is released at joint B of the beam, the result is the same as if a hinge were placed in the beam at that joint (see Fig. 1-5b). Then, in order to take account of the bending moment MB in the beam, it must be considered as consisting of two equal and opposite couples MB that act on the left- and right-hand portions of the beam with the hinge, as shown in Fig. 1-5c. In this illustration the moment MB is assumed positive in the directions shown in the figure, signifying that the couple acting on the left-hand beam is counterclockwise and the couple acting on the right-hand beam is clockwise. Thus, for the purpose of analyzing the beam in Fig. 1-5c, the bending moment at point B may be treated

- as a single action consisting of two couples. Similar situations are encountered with axial forces, shearing forces, and twisting moments, as illustrated later in the discussion of the flexibility method of analysis.


A second basic concept is that of a displacement, which is most commonly a small translation or rotation at some point in a structure. A translation refers to the distance moved by a point in the structure, and a rotation means the angle of rotation of the tangent to the elastic curve (or its

p P A

![image 32](Matrix Analysis of Framed Structures_images/imageFile32.png)

###### ! B ! c

A ~ ~

###### I--L .1. L--l

(0)

###### A ( B ( C

![image 33](Matrix Analysis of Framed Structures_images/imageFile33.png)

~ ~ ~

- (b)

A c

- (c)


![image 34](Matrix Analysis of Framed Structures_images/imageFile34.png)

Fig. '-5.

![image 35](Matrix Analysis of Framed Structures_images/imageFile35.png)

nonnal) at a point. For example, in the cantilever beam of Fig. l-4c, the translation Ll of the end of the beam and the rotation () at the end are both considered as displacements. Moreover, as in the case of an action, a displacement may also be regarded in a generalized sense as a combination of translations and rotations. As an example, consider the rotations at the hinge at point B in the two-span beam in Fig. l-5c. The rotation of the righthand end ofthe member AB is denoted ()I, while the rotation of the left-hand end of member Be is denoted ()2' Each of these rotations is considered as a displacement. Furthennore, the sum of the two rotations, denoted as (), is also a displacement. The angle () can be considered as the relative rotation

- at point B between the ends of members AB and Be. Another illustration of displacements is shown in Fig. 1-6, in which a


plane frame is subjected to several loads. The horizontal translations LlA' LlB' and Lle of joints A, B, and e, respectively, are displacements, as also are the rotations ()A, ()B, and ()e of these joints. Joint displacements of these types play important roles in the analysis of framed structures.

It is frequently necessary in structural analysis to deal with actions and displacements that correspond to one another. Actions and displacements are said to be corresponding when they are of an analogous type and are located at the same point on a structure. Thus, the displacement corresponding to a concentrated force is a translation ofthe structure at the point where the force acts, although the displacement is not necessarily caused by the force. Furthermore, the corresponding displacement must be taken along the line of action of the force and must have the same positive direction as the force. In the case of a couple, the corresponding displacement is a rotation at the point where the couple is applied and is taken positive in the same sense as the couple.

As an illustration, consider again the cantilever beam shown in Fig. l-4a. The action PI is a concentrated force acting downward at the end of the beam, and the downward translation Ll at the end of the beam (see Fig. 1-4c) is the displacement that corresponds to this action. Similarly, the couple Ml and the rotation (J are a corresponding action and displacement. It

![image 36](Matrix Analysis of Framed Structures_images/imageFile36.png)

Fig. 1-6.

![image 37](Matrix Analysis of Framed Structures_images/imageFile37.png)

- 1.4 Actions and Displacements 11


should be noted, however, that the displacement .:l corresponding to the load P, is not caused solely by the force P" nor is the displacement () corresponding to M, caused by M, alone. Instead, in this example, both.:l and () are displacements due to P, and M, acting simultaneously on the beam. In general, if a particular action is given, the concept of a corresponding displacement refers only to the definition of the displacement, without regard to the actual cause of that displacement. Similarly, if a displacement is given, the concept of a corresponding action will describe a particular kind of action on the structure, but the displacement need not be caused by that action.

As another example of corresponding actions and displacements, refer to the actions shown in Fig. 1-5c. The beam in the figure has a hinge at the middle support and is acted upon by the two couples MB, which are considered as a single action. The displacement corresponding to the action M B consists in general of the sum of the counterclockwise rotation (), of the left-hand beam and the clockwise rotation (}2 ofthe right-hand beam. Therefore, the angle () (equal to the sum of (), and (}2) is the displacement corresponding to the action MB• This displacement is the relative rotation between the two beams at the hinge and has the same positive sense as MB• If the angle () is caused only by the couples M B, then it is described as the displacement corresponding to MB and caused by MB' This displacement can be found with the aid of the table of beam displacements given in Appendix A (see Table A-3, Case 5), and is equal to

###### () = () + () = MBL + MBL = 2MBL

###### , 2 3EI 3EI 3EI

in which L is the length of each span and EI is the flexural rigidity of the beam.

There are other situations, however, iri which it is necessary to deal with a displacement that corresponds to a particular action but is caused by some other action. As an example, consider the beam in Fig. 1-5b, which is the same as the beam in Fig. 1-5c except that it is acted upon by two forces P instead of the couples MB• The displacement in this beam corresponding to M B consists of the relative rotation at joint B between the two beams, positive in the same sense as M B, but due to the loads P only. Again using the table of beam displacements (Table A-3, Case 2), and also assuming that the forces P act at the midpoints of the members, it is found that the displacement () corresponding to MB and caused by the loads P is

###### PV PV PV

###### () = (), + (}2 = 16EI + 16EI = 8EI

The concept of correspondence between actions and displacements will become more familiar to the reader as additional examples are encountered in subsequent work. Also, it should be noted that the concept can be

![image 38](Matrix Analysis of Framed Structures_images/imageFile38.png)

extended to include distributed actions, as well as combinations of actions of all types. However, these more general ideas have no particular usefulness in the work to follow.

In order to simplify the notation for actions and displacements, it is desirable in many cases to use the symbol A for actions, including both concentrated forces and couples, and the symbol D for displacements, including both translations and rotations. Subscripts can be used to distinguish between the various actions and displacements that may be ofinterest in a particular analysis. The use of this type of notation is shown in Fig. 1-7, which portrays a cantilever beam subjected to actions AI, A2, and A3• The displacement corresponding to A I and due to all loads acting simultaneously is denoted by DI in Fig. 1-7a; similarly, the displacements corresponding to A2 and A3 are denoted by D2 and D3.

Now consider tfIe cantilever beam subjected to action Al only (see Fig. 1-7b). The displacement corresponding to Al in this beam is denoted by Dll• The significance of the two SUbscripts is as follows. The first subscript indicates that the displacement corresponds to action A I, and the second indicates that the cause of the displacement is action A I' In a similar manner, the displacement corresponding to A2 in this beam is denoted by D2h where the first subscript shows that the displacement corresponds to A2 and the second shows that it is caused by AI' Also shown in Fig. 1-7b is the displacement D31, corresponding to the couple A3 and caused by AI'

The displacements caused by action A2 acting alone are shown in Fig.

- 1-7c, and those caused by A3 alone are shown in Fig. 1-7d. In each case the subscripts for the displacement symbols follow the general rule that the first subscript identifies the displacement and the second gives the cause of the displacement. In general, the cause may be a single force, a couple, or an entire loading system. Unless specifically stated otherwise, this convention for subscripts will always be used in later discussions.


![image 39](Matrix Analysis of Framed Structures_images/imageFile39.png)

![image 40](Matrix Analysis of Framed Structures_images/imageFile40.png)

(0)

![image 41](Matrix Analysis of Framed Structures_images/imageFile41.png)

![image 42](Matrix Analysis of Framed Structures_images/imageFile42.png)

Fig. '·7.

![image 43](Matrix Analysis of Framed Structures_images/imageFile43.png)

- 1.5 Equilibrium 13


For the beams pictured in Fig. 1-7 it is not difficult to determine the various displacements (see Table A-3, Cases 7 and 8). Assuming that the beam has flexural rigidity EI and length L, it is found that the displacements for the beam in Fig. 1-7b are

D = 5A I L3

D = AIV

II 24EI

21 48EI

In a similar manner the remaining six displacements in Figs. 1-7c and d (DI2' D 22, ... , D33) can be found. Then the displacements in the beam under all loads acting simultaneously (see Fig. 1-7a) are determined by summation, as follows:

DI = Dl1 + DI2 + DI3 D2 = D21 + D22 + D23 D3 = D31 + D32 + D33

These summations are expressions of the principle of superposition, which is discussed more fully in Sec. 1.9.

1.5 Equilibrium. One of the objectives of any structural analysis is to determine various actions pertaining to the structure, such as reactions

- at the supports and internal stress resultants (bending moments, shearing forces, etc.). A correct solution for any of these quantities must satisfy all conditions of static equilibrium, not only for the entire structure, but also for any part of the structure taken as a free body.


Consider now any free body subjected to several actions. The resultant of all the actions may be a force, a couple, or both. If the free body is in static equilibrium, the resultant vanishes; that is, the resultant force vector and the resultant moment vector are both zero. A vector in three-dimensional space may always be resolved into three components in mutually orthogonal directions, such as the x, y, and z directions. If the resultant force vector equals zero, then its components also must be equal to zero, and therefore the following equations of static equilibrium are obtained:

(l-la)

In these equations the expressions !Fx' !Fy, and !F, are the algebraic sums of the x, y, and z components, respectively, of all the force vectors acting on the free body. Similarly, if the resultant moment vector equals zero, the moment equations of static equilibrium become:

L M, =0 (l-lb)

in which !M.r, !My, and !M, are the algebraic sums ofthe moments about the x, y, and z axes, respectively, of all the couples and forces acting on the free body. The six relations in Eqs. (1-1) represent the static equilibrium equations for actions in three dimensions. They may be applied to any free

![image 44](Matrix Analysis of Framed Structures_images/imageFile44.png)

14 Chapter 1 Basic Concepts of Structural Analysis

body such as an entire structure, a portion ofa structure, a single member, or a joint of a structure.

When all forces acting on a free body are in one plane and all couples have their vectors normal to that plane, only three of the six equilibrium equations will be useful. Assuming that the forces are in the x-y plane, it is apparent that the equations '!.Fz = 0, '!.Mx = 0, and '!.M~ = 0 will be satisfied automatically. The remaining equations are

LFx=O LFy=O LMz=O (1-2)

and these equations become the static equilibrium conditions for actions in the x-y plane.

In the stiffness method of analysis, the basic equations to be solved are those which express the equilibrium conditions at the joints of the structure, as described later in Chapter 3.

1.6 Compatibility. In addition to the static equilibrium conditions, it is necessary in any structural analysis that all conditions of compatibility be satisfied. These conditions refer to continuity of the displacements throughout the structure and are sometimes referred to as conditions of geometry. As an example, compatibility conditions must be satisfied at all points of support, where it is necessary that the displacements of the structure be consistent with the support conditions. For instance, at a fixed support there can be no translation and no rotation of the axis of the member.

Compatibility conditions must also be satisfied at all points throughout the interior of a structure. Usually, it is compatibility conditions at the joints of the structure that are of interest. For example, at a rigid connection between two members the displacements (translations and rotations) of both members must be the same.

In the flexibility method of analysis the basic equations to be solved are equations that express the compatibility of the displacements, as will be described in Chapter 2.

1.7 Static and Kinematic Indeterminacy. There are two types of indeterminacy that must be considered in structural analysis, depending upon whether actions or displacements are of interest. When actions are the unknowns in the analysis, as in the flexibility method, then static indeterminacy must be considered. In this case, indeterminacy refers to an excess of unknown actions (internal actions and external reactions), as compared to the number of equations of static equilibrium that are available at the joints. The number of such equations for each joint depends upon the type of structure. If these equations are sufficient for finding all actions, both external and internal, then the structure is statically determinate. If there are more unknown actions than equations, the structure is statically indeterminate. The simply supported beam shown in Fig. 1-3 and the cantilever beam of Fig. 1-4 are examples of statically determinate structures, because in both

![image 45](Matrix Analysis of Framed Structures_images/imageFile45.png)

1.7 Static and Kinematic Indeterminacy 15

cases all reactions and stress resultants can be found from equilibrium equations alone. On the other hand, the continuous beam of Fig. I-Sa is statically indeterminate.

The unknown actions in excess of those that can be found by static equilibrium are known as static redundants, and the number of such redundants represents the degree of static indeterminacy of the structure. Thus, the two-span beam of Fig. I-Sa is statically indeterminate to the first degree, because there is one redundant action. For instance, it can be seen that it is impossible to calculate all of the reactions for the beam by static equilibrium alone. However, after the value of one reaction is obtained (by one means or another), the remaining reactions and all internal stress resultants can be found by statics alone.

To formalize the procedure for counting the number of static redundants, consider the following equation: (Number of redundants) = (Number of unknown actions)

- (Number of joint equilibrium equations) (a)

This expression yields the degree of static indeterminacy, which may be positive, zero, or negative. A zero result means the structure is statically determinate; whereas, a negative result implies a mobile structure (see Sec. 1.8). Table 1-1 summarizes the number of unknown actions per member and the number ofequilibrium equations perjoint for the various types of framed structures. The number 2 for a beam member implies that axial forces and deformations are to be omitted.

Alternatively, a less formal procedure involves counting the number of releases necessary to obtain a statically determinate structure. This approach is usually the quick and easy way to handle simple structures and can always be checked by the formal counting method in Eq. (a).

Figure 1-8 shows a few more examples of statically indeterminate structures. The propped cantilever beam in Fig. 1-8a is indeterminate to the first

Table 1-1

Numbers for Counting Degrees of Static and Kinematic Indeterminacy

Type of Unknown Actions Equilibrium Equations Displacements Structure per Member per Joint per Joint

Beam 2 2 2 Plane Truss I 2 2 Space Truss I 3 3 Plane Frame 3 3 3 Grid 3 3 3 Space Frame 6 6 6

![image 46](Matrix Analysis of Framed Structures_images/imageFile46.png)

Chapter 1 Basic Concepts of Structural Analysis

16

![image 47](Matrix Analysis of Framed Structures_images/imageFile47.png)

![image 48](Matrix Analysis of Framed Structures_images/imageFile48.png)

(0)

w

![image 49](Matrix Analysis of Framed Structures_images/imageFile49.png)

{~!fffffttffftttffft

###### M....

(e)

###### fR...

( b)

Fig. 1-8. Examples of statically indeterminate structures.

degree because there are five unknown actions (two internal and three external) but only four equations of equilibrium (two at each joint). On the other hand, the fixed-end beam in Fig. 1-8b has one more unknown reaction; so it is statically indeterminate to the second degree.

The plane truss in Fig. 1-8c has eleven members, six joints, and three reaction force components at two points of support. Thus, there are fourteen unknown actions, consisting of eleven bar forces and three reactive forces. Furthermore, twelve equations of joint equilibrium are available (two per joint at six joints). Therefore, the number of static redundants is two, as indicated by Eq. (a). This conclusion may also be reached by cutting two bars, such as X and Y, thereby releasing the axial forces in those members. The remaining structure is then statically determinate because all reactions and bar forces can be found using the equations of equilibrium.

As another example of the alternative method for determining the degree of indeterminateness of a structure, consider the plane frame shown in Fig. 1-6. The object is to make cuts, or releases, in the frame until the structure has become statically determinate. If bars AB and Be are cut, the structure that remains consists of three cantilever portions (the supports of the cantilevers are at D, E, and F), each of which is statically determinate. Each bar that is cut represents the removal (or release) of three actions (axial force, shearing force, and bending moment) from the original structure. Because a total of six actions was released, the degree of indeterminacy of the frame is six.

A distinction may also be made between external and internal indeterminateness. External indeterminateness refers to the calculation of the reactions for the structure. Normally, there are six equilibrium equations available for the determination of reactions in a space structure, three for a plane structure, and two for a linear (beam) structure. Therefore, a space structure with more than six reactive actions, a plane structure with more than three reactions, or a beam with more than two reactions will usually be

![image 50](Matrix Analysis of Framed Structures_images/imageFile50.png)

1.7 Static and Kinematic Indeterminacy 17

8

Fig. '-9. Three-hinged arched truss.

externally indetenninate. Examples of external indetenninateness can be seen

- in Fig. 1-8. The propped cantilever beam is externally indetenninate to the first degree, the fixed-end beam is externally indetenninate to the second degree, and the plane truss is statically detenninate externally.

Internal indetenninateness refers to the calculation of stress resultants within the structure, assuming that all reactions have been found previously. For example, the truss in Fig. 1-8c is internally indetenninate to the second degree, although it is externally detenninate, as noted above.

The total degree of indetenninateness of a structure is the sum of the external and internal degrees of indetenninateness. Thus, the truss in Fig. 1-8c is indetenninate to the second degree when considered in its entirety. The beam in Fig. 1-8a is externally indetenninate to the first degree and internally detenninate, inasmuch as all stress resultants can be readily found after all the reactions are known. The plane frame in Fig. 1-6 has nine reactive actions, and therefore it is externally indetenninate to the sixth degree. Internally, the frame is detenninate because all stress resultants can be found if the reactions are known. Therefore, the frame has a total indeterminateness of six, as previously observed.

Occasionally, there are special conditions of construction that affect the degree of indetenninacy of a structure. The three-hinged arched truss shown

- in Fig. 1-9 has a central hinge at joint B that makes it possible to calculate all four reactions by statics. For the truss shown, the bar forces in all members can be found after the reactions are known. Therefore, the structure is statically detenninate overall, as may be confinned by the counting procedure.


Several additional examples of statically indetenninate structures are given at the end of this section. Other examples will be encountered in Chapter 2 in connection with the flexibility method of analysis. See Reference [1]* for more details on fonnalized counting procedures for static indetenninacy.

In the stiffness method of analysis, the displacements of the joints of the structure become the unknown quantities. Therefore, the second type of

*Numbers in square brackets indicate references at the end of the chapter.

![image 51](Matrix Analysis of Framed Structures_images/imageFile51.png)

18 Chapter 1 Basic Concepts of Structural Analysis

indetenninacy, known as kinematic indeterminacy, becomes important. In order to understand this type of indetenninacy, it should be recalled that joints in framed structures are defined to be located at all points where two or more members intersect, at points of support, and at free ends. When the structure is subjected to loads, each joint will undergo displacements in the fonns of translations and rotations, depending upon the configuration of the structure. In some cases the joint displacements will be known because of restraint conditions that are imposed upon the structure. At a fixed support, for instance, there can be no displacements of any kind. However, there will be other joint displacements that are not known in advance, and which can be obtained only by making a complete analysis of the structure. These unknown joint displacements are the kinematically indetenninate quantities, which are sometimes called kinematic redundants. Their number represents the degree of kinematic indetenninacy of the structure, or the number of degrees offreedom for joint displacement.

To illustrate the concepts of kinematic indetenninacy, it is useful to consider again the examples of Fig. I-S. Beginning with the beam in Fig. I-Sa, it is seen that end A is fixed and cannot undergo any displacement. On the other hand, joint B has one degree of freedom for joint displacement, which is rotation. Thus, the beam is kinematically indetenninate to the first degree, and there is only one unknown joint displacement to be calculated.

The second example of Fig. I-S is a fixed-end beam. Such a beam has no unknown joint displacements, and therefore is kinematically detenninate. By comparison, the same beam was statically indetenninate to the second degree.

The third example in Fig. I-S is the plane truss that was previously shown to be statically indetenninate to the second degree. Joint A of this truss may undergo two independent components of translation (see Table 1-1) and hence has two degrees of freedom. Rotation of a joint of a truss has no physical significance because, under the assumption ofhinged joints, rotation of a joint produces no effects in the members of the truss. Thus, the degree of kinematic indetenninacy of a truss is always found as if the truss were subjected to loads at the joints only. This philosophy is the same as in the case of static indetenninacy, wherein only axial forces in the members are considered as unknowns. The joints B, D, and E of the truss in Fig. I-Sc also have two degrees of freedom each, while the restrained joints C and F have zero and one degree of freedom, respectively. Thus, the truss has a total of nine degrees of freedom for joint translation and is kinematically indetenninate to the ninth degree.

The rigid frame shown in Fig. 1-6 offers another example of a kinematically indetenninate structure. Because the supports at D, E, and F of this frame are fixed, there can be no displacements at these joints. However, joints A, B, and C each possess three degrees of freedom, because each joint may undergo horizontal and vertical translations and a rotation. Thus, the total number of degrees of kinematic indetenninacy for this frame is nine.

![image 52](Matrix Analysis of Framed Structures_images/imageFile52.png)

- 1.7 Static and Kinematic Indeterminacy 19


If the effects of axial deformations are omitted from the analysis, the degree of kinematic indeterminacy is reduced. There would be no possibility for vertical displacement of any of the joints because the columns would not change length. Furthermore, the horizontal translations of joints A, B, and C would be equal. In other words, if axial deformations are omitted, the only independent joint displacements are the rotations of joints A, B, and C and one horizontal translation (such as that of joint B). Therefore, the structure would be considered to be kinematically indeterminate to the fourth degree.

The following equation represents a formal procedure for counting the number of degrees of freedom: (Number of degrees of freedom) = (Number of possible joint displace-

ments) - (Number of restraints) (b)

The last column in Table 1-1 gives the possible number of displacements per joint for the six types of framed structures. Again, the number 2 for a beam joint implies that axial deformations are to be disregarded.

Alternatively, the number of degrees of freedom may be found by counting the number of joint restraints necessary to obtain a kinematically determinate structure (with no joint displacements). This short-cut approach is, of course, equivalent to using Eq. (b). If axial strains in plane and space frames are to be omitted, the number of degrees of freedom is reduced by the number of straight members in the structure.

Example 1. The space truss shown in Fig. 1-10 has pin supports at A, B, and C. The degrees of static and kinematic indeterminacy for the truss are to be obtained using the numbers in line 3 of Table 1-1.

In determining the degree of static indeterminacy, it can be noted that there are three equations of equilibrium available at every joint of the truss (see Table 1-1) for the purpose of calculating bar forces and reactions. Thus, a total of 18 equations of statics is available. The number of unknown actions is 21, because there are 12 bar forces and 9 reactions (three at each support) to be found. Therefore, the truss is statically indeterminate to the third degree. More specifically, the truss is externally indeterminate to the third degree, because there are nine reactions but only six equations for the equilibrium of the truss as a whole. The truss is internally deter-

![image 53](Matrix Analysis of Framed Structures_images/imageFile53.png)

Fig. 1-10. Example 1.

![image 54](Matrix Analysis of Framed Structures_images/imageFile54.png)

20 Chapter 1 Basic Concepts of Structural Analysis

minate because all bar forces can be found by statics after the reactions are determined.

Each of the joints D, E, and F has three degrees of freedom for joint displacement, because each joint can translate in three mutually orthogonal directions. Therefore, the truss is kinematically indeterminate to the ninth degree.

Example 2. The degrees of static and kinematic indeterminacy are to be found for the space frame shown in Fig. l-lla, using the numbers in the last line of Table 1-1.

There are various ways in which the frame can be cut in order to reduce it to a statically determinate structure. One possibility is to cut all four of the bars EF, FG, GH, and EH, thereby giving the released structure shown in Fig. l-llb. Because each release represents the removal of six actions (axial force, two shearing forces, twisting couple, and two bending moments) the original frame is statically indeterminate to the 24th degree.

The number of possible joint displacements at E, F, G, and H is six at each joint (three translations and three rotations); therefore, the frame is kinematically indeterminate to the 24th degree.

Now consider the effect of omitting axial deformations from the analysis. The degree of static indeterminacy is not affected because the same number of actions will still exist in the structure. On the other hand, there will be fewer degrees of freedom for joint displacement because eight members do not change lengths. Thus, it is finally concluded that the degree of kinematic indeterminacy is 24 - 8 = 16 when axial deformations are excluded from consideration.

Consider next the effect of replacing the fixed supports at A, B, C, and D by immovable pinned supports. The effect of the pinned supports is to reduce the number of reactions at each support from six to three. Therefore, the degree of static indeterminacy becomes 12 less than with fixed supports, or a total of 12 degrees. At the same time, three additional degrees of freedom for rotation have been added at each support, so that the degree of kinematic indeterminacy has been increased by 12 when compared to the frame with fixed supports. It can be seen that removing restraints at the supports of a structure serves to decrease the degree of static indeterminacy, while increasing the degree of kinematic indeterminacy.

Example 3. The grid shown in Fig. 1-12a lies in a horizontal plane and is supported at A, D, E, and H by simple supports. The joints at B, C, F, and G are

![image 55](Matrix Analysis of Framed Structures_images/imageFile55.png)

![image 56](Matrix Analysis of Framed Structures_images/imageFile56.png)

£f----:c---~

###### A o

###### (0) (b)

Fig. 1-11. Example 2.

![image 57](Matrix Analysis of Framed Structures_images/imageFile57.png)

- 1.8 Structural Mobilities 2J o H


Br-------7'

A E

(a) (b)

Fig. 1-12. Example 3.

rigid connections. Find the degrees of static and kinematic indeterminacy using the numbers in line 5 of Table 1-1.

Because there are no axial forces in the members of a grid, only vertical reactions are developed at the supports of this structure. Therefore, the grid is externally indeterminate to the first degree, because only three equilibrium equations are available for the structure in its entirety, but there are four reactions. After removing one reaction, the grid can be made statically determinate by cutting one member, such

- as CG (see Fig. 1-12b). The release in member CG removes three actions (shearing force in the vertical direction, twisting moment, and bending moment). Thus, the grid can be seen to be internally indeterminate to the third degree and statically indeterminate overall to the fourth degree.


In general, there are three degrees of freedom for displacement at each joint of a grid (one translation and two rotations). Such is the case at joints B, C, F, and G of the grid shown in Fig. 1-12a. However, at joints A, D, E, and H only two joint displacements are possible, inasmuch as joint translation is prevented. Therefore, the grid shown in the figure is kinematically indeterminate to the 20th degree.

1.8 Structural Mobilities. In the preceding discussion of external static indeterminacy, the number of reactions for a structure was compared with the number of equations of static equilibrium for the entire structure taken as a free body. If the number of reactions exceeds the number of equations, the structure is externally statically indeterminate; if they are equal, the structure is externally determinate. However, it was tacitly assumed in the discussion that the geometrical arrangement of the reactions was such as to prevent the structure from moving when loads act on it. For instance, the beam shown in Fig. 1-13a has three reactions, all of which are in the same direction. It is apparent, however, that the beam will move to the left when the inclined load P is applied. A structure of this type is said to be mobile (or kinematically unstable). Other examples of mobile structures are the frame of Fig. 1-13b and the truss of Fig. 1-13c. In the structure of Fig. 1-13b the three reactive forces are concurrent (their lines of action intersect at point 0). Therefore, the frame is mobile because it cannot support a general load, such as the force P, which does not act through point O. In the truss of Fig. 1-13c there are two members that are collinear at joint A, and there is no other member meeting at that joint. Again, the structure is

![image 58](Matrix Analysis of Framed Structures_images/imageFile58.png)

22

Chapter 1 Basic Concepts of Structural Analysis

p

###### /

(0)

###### o

/1''"

###### // I "

###### / I , / I '

(e)

/1'

1

###### I

(b)

Fig. 1-13. Mobile structures.

mobile because it is incapable of supporting the load P in its initial configuration.

From the examples ofmobile structures given in Fig. 1-13, it is apparent that both the supports and the members ofany structure must be adequate in number and in geometrical arrangement to insure that the structure is not movable. Only structures meeting these conditions will be considered for analysis in subsequent chapters.

1.9 Principle of Superposition. The principle of superposition is one of the most important concepts in structural analysis. It may be used whenever linear relationships exist between actions and displacements (the conditions under which this assumption is valid are described later in this section). In using the principle of superposition it is assumed that certain actions and displacements are imposed upon a structure. These actions and displacements cause other actions and displacements to be developed in the structure. Thus, the former actions and displacements have the nature of causes, while the latter are effects. In general terms the principle states that the effects produced by several causes can be obtained by combining the effects due to the individual causes.

In order to illustrate the use of the principle of superposition when actions are the cause, consider the beam in Fig. 1-14a. This beam is subjected to loads At and A 2, which produce various actions and displacements throughout the structure. For instance, reactions RA, RB, and MB are developed at the supports, and a displacement D is produced at the midpoint of the beam. The effects of the actions At and A2 acting sepa-

![image 59](Matrix Analysis of Framed Structures_images/imageFile59.png)

l.9 Principle of Superposition 23

![image 60](Matrix Analysis of Framed Structures_images/imageFile60.png)

![image 61](Matrix Analysis of Framed Structures_images/imageFile61.png)

- (b )
- (c)


![image 62](Matrix Analysis of Framed Structures_images/imageFile62.png)

Fig. 1-14. Effects of actions.

rately are shown in Figs. 1-14b and 1-14c. In each case there is a displacement at the midpoint of the beam and reactions at the ends. A single prime is used to denote quantities associated with the action AI, and a double prime is used for quantities associated with A 2•

According to the principle of superposition, the actions and displacements caused by Al and A2 acting separately (Figs. 1-14b and 1-14c) can be combined in order to obtain the actions and displacements caused by AI and A2 acting simultaneously (Fig. 1-14a). Thus, the following equations of

superposition can be written for the beam in Fig. 1-14: RA = R~ + R~ MB = M~ + M~

###### RB = R~ + R~ D = D' + D"

(1-3)

Of course, similar equations of superposition can be written for other actions and displacements in the beam, such as stress resultants at any cross section of the beam and displacements (translations and rotations) at any point along the axis of the beam. This manner of using superposition was illustrated previously in Sec. 1.4.

A second example of the principle of superposition, in which displacements are the cause, is given in Fig. 1-15. The figure portrays again the beam AB with one end simply supported and the other fixed. When end B of the beam is displaced downward through a distance ~ and, at the same time, is caused to be rotated through an angle e(see Fig. 1-15a), various actions and displacements in the beam will be developed. For example, the reactions at each end and the displacement at the center are shown in Fig. 1-15a. The next two sketches (Figs. I-15b and 1-15c) show the beam with

![image 63](Matrix Analysis of Framed Structures_images/imageFile63.png)

24 Chapter 1 Basic Concepts of Structural Analysis

![image 64](Matrix Analysis of Framed Structures_images/imageFile64.png)

###### A

~

###### ~t 0

(0)

![image 65](Matrix Analysis of Framed Structures_images/imageFile65.png)

![image 66](Matrix Analysis of Framed Structures_images/imageFile66.png)

(e)

Fig. 1·15. Effects of displacements.

the displacements d and () occurring separately. The reactions at the ends and the displacement at the center are again denoted by the use of primes; a single prime is used to denote quantities caused by the displacement d, and double primes are used for quantities caused by the rotation e. When the principle of superposition is applied to the reactions and the displacement at the midpoint, the superposition equations again take the form of Eqs. (1-3). This example illustrates how actions and displacements caused by displacements can be superimposed. The same principle applies to any other actions and displacements in the beam.

The principle of superposition may be used also if the causes consist of both actions and displacements. For example, the beam in Fig. 1-15a could

be subjected to various loads as well as to the displacements d and e. Then the actions and displacements in the beam can be obtained by combining those due to each load and displacement separately.

As mentioned earlier, the principle of superposition will be valid whenever linear relations exist between actions and displacements of the structure. This occurs whenever the following three requirements are satisfied: (1) the material ofthe structure follows Hooke's law; (2) the displacements of the structure are small; and (3) there is no interaction between axial and flexural effects in the members. The first of these requirements means that the material is perfectly elastic and has a linear relationship between stress and strain. The second requirement indicates that all calculations involving the over-all dimensions of the structure can be based upon the original dimensions of the structure (which is also a basic assumption for calculating displacements by the methods described in Appendix A). The third requirement implies that the effect of axial forces on the bending of the members

![image 67](Matrix Analysis of Framed Structures_images/imageFile67.png)

1.10 Action and Displacement Equations 25

is neglected. This requirement refers to the fact that axial forces in a member, in combination with even small deflections of the member, will have an effect on the bending moments. The effect is nonlinear and can be omitted from the analysis when the axial forces (either tension or compression) are not large. (A method of incorporating such effects into the analysis is described in Sec. 6.18.)

When all three of the requirements listed above are satisfied, the structure is said to be linearly elastic, and the principle of superposition can be used. Since this principle is fundamental to the flexibility and stiffness methods of analysis, it will always be assumed in subsequent discussions that the structures being analyzed meet the stated requirements.

In the preceding discussion of the principle of superposition it was assumed that both actions and displacements were of importance in the analysis, as is generally the case. An exception, however, is the analysis of a statically determinate structure for actions only. Since an analysis of this kind requires the use of equations of equilibrium but does not require the calculation of any displacements, it can be seen that the requirement of linear elasticity is superfluous. An example is the determination ofthe reactions for a simply supported beam under several loads. The reactions are linear functions of the loads regardless of the characteristics of the material of the beam. It is still necessary, however, that the deflections of the beam be small, since otherwise the positions of the loads and reactions would be altered.

1.10 Action and Displacement Equations. The relationships that exist between actions and displacements play an important role in structural analysis and are used extensively in both the flexibility and stiffness methods. A convenient way to express the relationship between the actions on a structure and the displacements of the structure is by means of action and displacement equations. A simple illustration of such equations is obtained by considering the linearly elastic spring shown in Fig. 1-16. The action A will compress the spring, thereby producing a displacement D of the end of the spring. The relationship between A and D can be expressed by a displacement eqllation, as follows:

###### D = FA (1-4)

In this equation F is the flexibility of the spring and is defined as the displacement produced by a unit value of the action A.

The relationship between the action A and the displacement D for the

Fig. 1-16. Linearly elastic spring.

![image 68](Matrix Analysis of Framed Structures_images/imageFile68.png)

26 Chapter 1 Basic Concepts of Structural Analysis

spring in Fig. 1-16 can also be expressed by an action equation which gives A in terms of D. That is,

###### A = SD (1-5)

In this equation S is the stiffness of the spring, which is defined as the action required to produce a unit displacement. It can be seen from Eqs. (1-4) and (1-5) that the flexibility and stiffness of the spring are inverse to one another, as follows:

1

1

F = - = S-l

S = - = F-1

(1-6)

S

F

The flexibility of the spring has units of length divided by force, while the stiffness has units offorce divided by length.

The same general relationships (Eqs. 1-4 to 1-6) that apply to the spring will hold also for any linearly elastic structure that is subjected to a single action. An example is given in Fig. 1-17a, which shows a simply supported beam acted upon by a concentrated force A at the midpoint. The displacement D shown in the figure is the vertical, downward deflection of the beam at the point where A acts upon the beam. Hence, in this example the displacement D not only corresponds to A but also is caused by A. The action and displacement equations given previously (Eqs. 1-5 and 1-4, respectively) are valid for the beam of Fig. 1-17a, provided that the flexibility F and the stiffness S are determined appropriately. In this case the flexibility F is seen to be the displacement produced by a unit value of the load, as shown in Fig. 1-17b (see Case 2 of Table A-3 in Appendix A). Thus,

~~

###### l---L/2-..J--L/2-J

(0 )

###### ~"'~=-___--lkc-l_ ~

\ - ~

###### F

- (b)

~-........\-~

1

- (c)


###### Fig. 1-17. Flexibility and stiffness of a beam subjected to a single load.

![image 69](Matrix Analysis of Framed Structures_images/imageFile69.png)

1.10 Action and Displacement Equations 27

in which L is the length of the beam and EI is the flexural rigidity. The stiffness S, equal to the inverse of the flexibility, is the action required to produce a unit value of the displacement (see Fig. 1-17c). Hence,

###### S=v

48EI

Note again that S has units of force divided by length. Also, it should be emphasized that the simple relationships expressed by Eq. (1-6) are valid only when the structure is subjected to a single load.

Now consider a more general example in which a structure is acted upon by three loads (Fig. 1-18a). The loads on the beam are denoted by AI, A2, and A3, and are taken positive in the directions (or senses) shown in the figure. The deflected shape produced by the loads acting on the beam is shown in Fig. 1-18b. In this figure the displacements in the beam corresponding to AI, A 2, and A 3, and caused by all three loads acting simulta-

~(b) -

(0 )

~

###### ~~. F. .. ~

II

(c)

###### ~

~ F22_

12

(d)

~13 --

~)1

(e)

###### Fig. 1-18. Illustration of flexibility coefficients.

![image 70](Matrix Analysis of Framed Structures_images/imageFile70.png)

28 Chapter 1 Basic Concepts of Structural Analysis

neously, are denoted by D1, D2, and D3, respectively, and are assumed positive in the same directions (or senses) as the corresponding actions.

By using the principle of superposition, each of the displacements in

- Fig. 1-18b can be expressed as the sum of the displacements due to the loads At. A 2, and A3 acting separately. For example, the displacement Dl is given by the expression


Dl = Dl1 + D12 + D13

in which Dl1 is the displacement corresponding to Al and caused by At. D12 is the displacement corresponding to Al and caused by A 2, and D13 is the displacement corresponding to Al and caused by A3. In a similar manner two additional equations can be written for D2 and D3. Each of the displacements appearing on the right-hand sides of such equations is a linear function of one of the loads; that is, each displacement is directly proportional to one ofthe loads. For example, D12 is a displacement caused by A2 alone, and it is equal to A2 times a certain coefficient. Denoting such coefficients by the symbol F, it is possible to write equations for the displacements D 1, D2, and D3 explicitly in terms of the loads, as follows:

Dl = Fl1AI + F12A2 + F13A3 D2 = F21Al + F22A2 + F23A3 D3 = F31AI + F32A2 + F33A3

(1-7)

In the first ofthese equations the expression Fl1Al represents the displacement Dl1, the expression F12A2 represents the displacement D12, and so forth. Each term on the right-hand sides of the above equations is a displacement that is written in the form of a coefficient times the action that produces the displacement. The coefficients are called flexibility coefficients, or more simply, flexibilities.

Each flexibility coefficient F represents a displacement caused by a unit value of a load. Thus, the coefficient Fll represents the displacement corresponding to action Al and caused by a unit value of AI; the coefficient F 12 is the displacement corresponding to A 1 and caused by a unit value of A 2; and so forth. The physical significance of the flexibility coefficients is shown in Figs. 1-18c, 1-18d, and 1-18e. The displacements of the beam caused by a unit value of the action Al are shown in Fig. 1-18c. All of the flexibility coefficients in this figure have a second sUbscript equal to one, thereby denoting the cause ofthe displacements. The first subscript in each case identifies the displacement by denoting the action that corresponds to it. Similar comments apply also to the displacements pictured in Figs. 1-18d and 1-18e. The calculation offlexibilities may be a simple or a difficult task, depending upon the particular structure being investigated. An example involving a very simple structure is given at the end of Sec. 1.11. The more general use of flexibility coefficients in structural analysis, as well as methods for calculating them, will be shown in Chapter 2.

Instead of expressing the displacements in terms of the actions, as was

![image 71](Matrix Analysis of Framed Structures_images/imageFile71.png)

1.10 Action and Displacement Equations 29

done in Eqs. (1-7), it is also possible to write action equations expressing the actions in terms of the displacements. Such equations can be obtained, for instance, by solving simultaneously the displacement equations. Thus, if Eqs. (1-7) are solved for the actions in terms of the displacements, the resulting action equations have the form

Al = SllDI + SI2D2 + SI3D3 A2 = S21DI + S22D2 + S23D3 Aa = S31DI + S32D2 + S33D3

(1-8)

in which each S is a stiffness coefficient or, more simply, a stiffness. As stated previously, a stiffness represents an action due to a unit displacement. Thus, the stiffness coefficient S11 represents the action corresponding to A I when a unit displacement of type DI is introduced while the other displacements, namely, D2 and D3, are kept equal to zero. Similarly, the stiffness coefficient S12 is the action corresponding to A I caused by a unit displacement of type D2 while DI and D3 are equal to zero. By continuing in this manner, all of the stiffness coefficients can be defined as actions produced by unit displacements.

Physical interpretations of the stiffness coefficients are shown in Fig. 1-19. The first two parts of the figure (Figs. 1-19a and 1-19b) are repeated from Fig. 1-18 in order to show the actions and displacements in the original beam. In Fig. 1-19c the beam is shown with a unit displacement corresponding to A I induced in the structure while the displacements corresponding to A2 and A3 are made equal to zero. To impose these displacements on the beam requires that appropriate artificial restraints be provided. These are shown in the figure by the simple supports corresponding to Al and A2 and the rotational restraint corresponding to A 3. The restraining actions developed by these artificial supports are the stiffness coefficients. For example, it can be seen from the figure that S11 is the action corresponding to Al and caused by a unit displacement corresponding to Al while the displacements corresponding to A2 and A3 are retained

- at zero. The stiffness coefficient S21 is the action corresponding to A2 caused by a unit displacement corresponding to A I while the displacements corresponding to A2 and A3 are made equal to zero, and so on, for the other stiffnesses. Note that each stiffness coefficient is a reaction for the restrained structure, and therefore a slanted line is used across the vector in order to distinguish it from a load vector. Each stiffness coefficient is shown acting in its assumed positive direction, which is automatically the same direction as the corresponding action. If the actual direction of one of the stiffn~sses is opposite to that assumed, then the coefficient will have a negative v,1lue when it is calculated. The stiffness coefficients caused by unit displacl'ments corresponding to A2 and A3 are shown in Figs. 1-19d and 1-1ge.


The calcula~ion of the stiffness coefficients for the continuous beam of

- Fig. 1-19 would le a lengthy task. However, in analyzing a structure by the


![image 72](Matrix Analysis of Framed Structures_images/imageFile72.png)

30 Chapter 1 Basic Concepts of Structural Analysis

~(b)~-

(0)

###### ~)

tS'3 +S23 S33

(e) t

Fig. 1-19. Illustration of stiffness coefficients.

stiffness method (as is done in Chapters 3 and 4), this difficulty is avoided by limiting the calculation of stiffnesses to very special structures that are obtained by completely restraining all the joints ofthe actual structure. The primary purpose of the preceding discussion and the following two examples is to aid the reader in visualizing the physical significance of stiffness and flexibility coefficients, without regard to matters of practical calculation.

Example 1. The beam shown in Fig. 1-20 is subjected to loads A 1 and A2 at the free end. The physical significance of the flexibility and stiffness coefficients corresponding to these actions is to be portrayed by means of sketches.

Unit loads corresponding to the actions Al and A2 are shown in Figs. I-20b and I-20c, respectively. The displacements produced by these unit loads, and which correspond to the actions A I and A 2, are the flexibility coefficients. These coefficients (F", F21, F12, and F22) are identified in the figures.

The stiffness coefficients (see Figs. I-20d and I-20e) are found by imposing unit displacements corresponding to Al and A 2, respectively, while at the same time maintaining the other corresponding displacement equal to zero. To accomplish this result requires the introduction of suitable restraints against translation and rotation at the free end of the beam. The restraint actions corresponding to Al and A2 are the stiffness coefficients, and they are labeled in the figures.

![image 73](Matrix Analysis of Framed Structures_images/imageFile73.png)

1.11 Flexibility and Stiffness Matrices 31

A,!

![image 74](Matrix Analysis of Framed Structures_images/imageFile74.png)

)A2

A '4\

(0)

1

![image 75](Matrix Analysis of Framed Structures_images/imageFile75.png)

###### A 4: ~--.JF"

F. f

(b) 2'

![image 76](Matrix Analysis of Framed Structures_images/imageFile76.png)

###### £: ~P~2

\;- 1

(e) 22

£ ~ ~nl--t

![image 77](Matrix Analysis of Framed Structures_images/imageFile77.png)

- (d) 5,,~ 52'

~ ~ f=

t )522

t

- (e)


![image 78](Matrix Analysis of Framed Structures_images/imageFile78.png)

t5•2

Fig. 1-20. Example 1.

Example 2. The plane truss illustrated in Fig. 1-21a is subjected to two loads Al and A2• The sketches in Figs. 1-21b, 1-2Ic, 1-21d, and 1-21e show the physical significance of the flexibility and stiffness coefficients corresponding to A I and A2• Note that the stiffnesses shown in Figs. 1-21d and 1-2le are the restraint actions required when the loaded joint of the truss is displaced a unit distance in the directions of Al and A 2 , respectively. A restraint of this type is provided by a pinned support.

1.11 Flexibility and Stiffness Matrices. In the preceding section the meaning of action and displacement equations was discussed with reference to particular examples. It is easy to generalize from that discussion and thereby to obtain the equations for a structure subjected to any number of corresponding actions and displacements. Thus, if the number of actions applied to the structure is n, the equations that give the n corresponding displacements are (compare with Eqs. 1-7)

FIlAI + Fl2A2 + F2lAI + F22A2 + (1-9)

In these equations each displacement D corresponds to one of the actions A and is caused by all ofthe actions acting simultaneously on the structure.

![image 79](Matrix Analysis of Framed Structures_images/imageFile79.png)

32 Chapter 1 Basic Concepts of Structural Analysis

![image 80](Matrix Analysis of Framed Structures_images/imageFile80.png)

lID"-- ---.:o!>--_ A,

( 0 )

![image 81](Matrix Analysis of Framed Structures_images/imageFile81.png)

![image 82](Matrix Analysis of Framed Structures_images/imageFile82.png)

###### F"

(c)

( b )

![image 83](Matrix Analysis of Framed Structures_images/imageFile83.png)

![image 84](Matrix Analysis of Framed Structures_images/imageFile84.png)

~

###### ",,,

###### ,,,

S' Z

............SIt

###### (d) l,~S2' ( e)

Fig. 1-21. Example 2.

For example, D J is the displacement corresponding to A 1 and caused by all of the actions At. A2, • • • , An. Each flexibility coefficient F represents a displacement caused by a unit value of one of the actions, while the other actions are zero. For example, F21 is the displacement corresponding to action A2 and caused by a unit value of the action A I' In general, the flexibility coefficient Fu is the i-th displacement (that is, the displacement corresponding to the i-th action) due to a unit value of the J-th action. The coefficient is taken as positive when it is in the positive direction (or sense) of the i-th action.

In matrix form the displacement equations (Eqs. 1-9) become

###### [DI

###### [Fll FI2 F1nl[AIJ

###### J

.~~ = ~2.1 F22 ~2~ .~~ Dn Fnl Fn2 Fnn An

or

D = FA (1-10)

in which D is a displacement matrix of order 11 x l; F is a square flexihility

![image 85](Matrix Analysis of Framed Structures_images/imageFile85.png)

1.11 Flexibility and Stiffness Matrices 33

matrix of order n x 11; and A is an action or load matrix of order n xl" The flexibility coefficients Fu that appear on the principal diagonal of Fare called direct flexibility coefficients and represent displacements caused by unit values of the corresponding actions. The remaining flexibility coefficients are called cross flexibility coefficients, and each represents a displacement caused by a unit value of an action that does not correspond to the displacement. It is apparent that i = j for the direct flexibilities and i f j for the cross flexibilities.

The action equations for the structure with n actions A acting upon it can be obtained by solving simultaneously Eqs. (1-9) for the actions in terms of the displacements. This operation gives the following action equations:

###### Al = SIIDl + Sl2D2 +

###### A2 S21D l + S22D2 +

(1-11)

All

These action equations in matrix form are

Sln]fDl]~.2:1 .~~

Sun Dn

S"2

or

A = SD (1-12)

As described previously, the matrices A and D represent the action and displacement matrices of order n x 1. The matrix S is a square stiffness matrix of order 11 x n. Each stiffness coefficient Su can be defined as the i-th action due to a unit value of the j-th displacement, assuming that the remaining displacements are equal to zero. If i = j the coefficient is a direct stiffness coefficient; if i =1= j, it is a cross stiffness coefficient.

Because Eqs. (1-11) were obtained from Eqs. (1-9) and the actions A and displacements D appearing in these equations are corresponding, it follows that the flexibility and stiffness matrices are related in a special manner. This relationship can be seen by solving Eq. (1-10) for A, giving the expression

(1-13)

in which F-1 denotes the inverse of the flexibility matrix F. The vectorst A and D in this equation are the same as those in Eq. (1-12) and, therefore, it is apparent that

*Identifiers for matrices are printed in bold-face type to distinguish them from scalars. tThe term vector is frequently used for a matrix of one column or one row.

![image 86](Matrix Analysis of Framed Structures_images/imageFile86.png)

34 Chapter 1 Basic Concepts of Structural Analysis

and F = S-I (1-14)

This relationship shows that the stiffness matrix is the inverse of the flexibility matrix and vice versa, provided that the same set of actions and corresponding displacements is being considered in both the action and displacement equations.

A somewhat different situation that occurs in structural analysis is the following. A set of displacement equations relating actions Al and corresponding displacements Dl is obtained for a particular structure, as follows:

Dl = FIAI

In this equation F1 is the flexibility matrix relating the displacements Dl to the actions AI. Independently, a set ofaction equations relating another set of actions A2 to the corresponding displacements D2 may be written for the same structure. Thus,

A2 = S2D2

It is, of course, not true that the flexibility and stiffness matrices FI and S2 are the inverse of one another. However, it is always possible to obtain the inverse of Fl, and this inverse can correctly be called a stiffness matrix. Specifically, it is the stiffness matrix Sl that is associated with the action equation relating Al and Dl. That is,

Al = FllDl = SlDl

Similarly, the inverse of the matrix S2 is a flexibility matrix relating D2 and A2, as follows:

D2 = SilA2 = F2A2

This discussion shows that a flexibility or stiffness matrix is not an array that is determined only by the nature of the structure; it is also related directly to the set of actions and displacements that is under consideration. The important fact to be remembered is that the flexibility matrix F obtained for a structure being analyzed by the flexibility method (see Chapter 2) is not the inverse ofthe stiffness matrix S for the same structure being analyzed by the stiffness method (see Chapter 3). The reason is that different sets of actions and corresponding displacements are utilized in the two methods.

Example. The prismatic cantilever beam shown in Fig. 1-22a is subjected to actions Al and Az at the free end. The corresponding displacements are denoted by DI and Dz in the figure.

The flexibility coefficients are identified in Figs. 1-22b and 1-22c and can be evaluated without difficulty (see Table A-3, Appendix A).

![image 87](Matrix Analysis of Framed Structures_images/imageFile87.png)

1.11 Flexibility and Stiffness Matrices

35

~ =do'

02 )A2

- (a)

~ ~>

F21

- (b)

~ --=---::t;;J<F,2

F2~- )

- (c)


Fig. 1-22. Example of flexibility and stiffness coefficients.

Therefore, the displacement equations are

###### L3 L2

Dl = 3EIA l + 2EIA2

###### V L

###### D2 = 2EIA l + EIA2

and it is seen that the flexibility matrix is

L3

[

F = 3EI

###### L2

2EI

The stiffness coefficients are the restraint actions shown in Figs. 1-22d and

- 1-22e. In this particular example, the coefficients are reactions for a fixed-end beam, and their expressions can be obtained from a table offixed-end actions. Such a table is given in Appendix B (see Table B-4), from which the following expressions are obtained:


###### s _4EI

22 - L

Thus, the action equations are

![image 88](Matrix Analysis of Framed Structures_images/imageFile88.png)

36 Chapter I Basic Concepts of Structural Analysis

and the stiffness matrix is

12EI _ 6EI]

###### L3 L2

[

S = 6EI 4EI

###### -U- L

When the flexibility and stiffness matrices are multiplied, the identity matrix I is obtained, as follows:

###### FS=SF=[~ ~J=I

Thus, the matrices F and S are the inverse of one another because the same set of actions and corresponding displacements was considered in both cases.

1.12 Equivalent Joint Loads. In general, the loads on a structure may be divided into two types: loads acting at the joints and loads acting on the members. Loads of the latter type can be replaced by equivalent loads acting at the joints. Such substitutions are called equivalent joint loads. When these loads are added to the actual joint loads, the total loads which result are called combined joint loads. Thereafter, the structure can be analyzed by matrix methods for the effects of the combined joint loads.

It is advantageous in the analysis if the combined joint loads are evaluated in such a manner that the resulting displacements of the structure are the same as the displacements produced by the actual loads. This result can be achieved if the equivalent loads are obtained through the use of fixed-end actions, as demonstrated by the example in Fig. 1-23. Part (a) of this figure shows a beam ABC supported at joints A and B and subjected to several loads. Some of these loads are actualjointloads (see Fig. 1-23b) while the remaining loads act on the members (see Fig. 1-23c). To accomplish the replacement of the member loads by equivalent joint loads, the joints of the structure are restrained against all displacements. For the beam in the figure, this procedure results in two fixed-end beams (Fig. 1-23d). When these fixed-end beams are subjected to the member loads, a set of fixed-end actions is produced. The end-actions can be obtained by means of the formulas in Appendix B and are shown in Fig. 1-23d for the particular loads in this example. The same fixed-end actions are also shown in Fig. 1-23e, where they are represented as restraint actions for the restrained structure. If these restraint actions are reversed in direction, they constitute a set offorces and couples that is equivalent to the member loads. Such equivalent joint loads, when added to the actual joint loads (Fig. 1-23b), produce the combined joint loads shown in Fig. 1-23f. Then

![image 89](Matrix Analysis of Framed Structures_images/imageFile89.png)

1.12 Equivalent Joint Loads

37

###### w ~ P, P2

~-.-'}f;-----'j---.--Tjj1 8 i ~

###### 1---L--+L/2 +L/2--J

( 0)

(d)

(b)

wL

21+~212

~::

###### c

(f)

(e)

Fig. 1·23. Combined joint loads.

the combined loads are used in carrying out the structural analysis, which is described later.

In general, the combined joint loads for any type of structure can be found by the procedure illustrated in Fig. 1-23. The first step is to separate the actual joint loads from the member loads. Then the structure is restrained against joint displacement by introducing appropriate joint restraints. Next, the restraint actions produced by the member loads on the restrained structure are calculated, using the formulas given in Table B-l. The negatives of these actions are the equivalent joint loads. Such loads are added to the actual joint loads to give the combined loads.

It was stated earlier that the displacements of the structure under the action of the combined loads should be the same as those produced by the actual loads. In order to observe that this requirement is satisfied, consider again the beam pictured in Fig. 1-23. It is apparent from the figure that the superposition of the combined loads (Fig. 1-23f) and the actions on the restrained structure (Fig. 1-23e) will give the actual loads on the beam (Fig. 1-23a). It follows, therefore, that the superposition of the joint displacements in the beams of Figs. 1-23e and 1-23fmust produce the joint displacements in the actual beam. But, since all joint displacements for the restrained beam are zero, it can be concluded that the joint displacements in the beam under the actual loads and the combined loads are the same.

![image 90](Matrix Analysis of Framed Structures_images/imageFile90.png)

Furthermore, the support reactions for the structure sUbjected to the combined loads are the same as the support reactions caused by the actual loads. This conclusion also can be verified by superposition of the actions in the beams of Figs. 1-23e and 1-23f. All restraint actions in the beam of Fig. 1-23e are negated by the equal and opposite equivalent joint loads acting on the beam of Fig. 1-23f. Hence, the reactions for the beam with the combined loads are the same as for the beam with the actual loads (Fig. 1-23a). This conclusion, as well as the one in the preceding paragraph, applies to all types offramed structures.

In contrast to the preceding conclusions, the member end-actions caused by the combined joint loads acting on the structure are not usually the same as those caused by the actual loads. Instead, the end-actions due to the actual loads must be obtained by adding the end-actions in the restrained structure to those caused by the combined loads. For example, in the case of the beam shown in Fig. 1-23, the actual end-actions (Fig. 1-23a) are found by superimposing the end-actions from the beams in Figs.

- 1-23e and 1-23f. The latter will be obtained as a result of the structural analysis itself, and the former are known from the calculations for the fixedend actions.


The remaining quantities of interest in a structural analysis performed by the flexibility method are the redundant actions themselves. Whether or not the redundant actions are the same in the actual structure and the structure with the combined joint loads depends upon the particular situation. If the redundant action is a reaction for the structure, it will be the same in both cases. If it is a member end-action, it must be treated in the manner described above for end-actions.

1.13 Energy Concepts. Most of the equations in this book are derived from principles of equilibrium, compatibility, and superposition. However, energy methods also playa vital role in structural theory, especially for the analysis of discretized continua by finite elements. In this section the concepts of strain energy and complementary strain energy will be developed and related to stiffnesses and flexibilities. The discussion pertains only to structures for which strains and displacements are small and no energy is dissipated in the static loading process. That is, the external work of gradually applied loads is equal to the energy stored in the structure, and the system is said to be conservative.

When a structure is loaded statically, various types of internal stresses and strains occur, depending upon the nature of the problem. Figure 1-24 shows the most general case of an infinitesimal element within a threedimensional solid [2]. Appearing in the figure are three components of normal stresses (CTx, CTy, and CTz) and six components of shearing stresses (Tx)" Tyz• etc.). The shearing stresses are not all independent; from equilibrium of the element the following relationships are known:

![image 91](Matrix Analysis of Framed Structures_images/imageFile91.png)

39

I.B Energy Concepts

,y, v

###### I

###### I I

###### zyt :

T

###### /7TZX

###### ----x,v

CTZ }----

./

./

./

./

./

./

./

###### /

dx

z,w

###### Fig. 1-24. Stresses on an infi nitesimal element.

###### TXY = Tyx Tzx = Txz (a)

Consequently, only six independent components of stress need be considered in the most general case.

Corresponding to the normal stresses are three types of normal strains (E x' E y, and Ez), defined as

###### au av

###### aw

Z az (b)

E =-

E =-

x ax EY =-ay

where u, v, and ware displacements (translations) in the x, y, and z directions, respectively. Similarly, six shearing strains (-YxV' l'\,z' etc.) correspond to the six shearing stresses. However, only three are Independent, as can be seen from the following definitions of shearing strains:

###### av aw

###### au av

all' au

'YZX = ax +-az = 'Yxz (c)

'V - + -'V

I yz - az ay - I zy

'V - + -'V

'XY-ayax- 'YX

For convenience, the six independent stresses and corresponding strains will be represented as column vectors. Thus,

![image 92](Matrix Analysis of Framed Structures_images/imageFile92.png)

- CT1 CT,r El E.r
- CT2 CTy E2 E.v


u= CT3 CTz E = E3 E, (d)

- CT4 T,ry E4 Y,I"Y
- CT5 T yZ E5 YYZ
- CT6 TZ.1' E6 YZ.1'


These vectors and their associated coordinate axes constitute a complete description of the state of stress and strain at any point in a three-dimensional body.

Figure 1-25 shows typical stress-strain diagrams for nonlinear and linear elastic materials. For simplicity, only one type of normal stress CT is plotted against the corresponding normal strain E. Strain energy is defined as the internal work of stresses acting through incremental strains, integrated over the total strains and over the volume. For the nonlinear case in

- Fig. 1-25a, the strain energy U may be written as


(1-15)

in which V denotes volume and ns is the number of strain components Ei (see Eq. d) involved in a particular problem. The expression in parentheses represents the area between the curve and the strain axis in Fig. 1-25a. Evaluation of this integral for the linear case in Fig. 1-25b (where CT = ECT/E;) produces the result

u',

###### rL

-f-_l- fzz;=zzz.;~

du

du

II E,;

###### --1-d.

(a)

(b)

###### Fig. 1-25. Stress-strain diagrams: (a) nonlinear and (b) linear.

![image 93](Matrix Analysis of Framed Structures_images/imageFile93.png)

1.13 Energy Concepts 41

###### u 1n.f 1f

= - L CTjE; dV = - UTE dV

(1-16)

2 i=1 V 2 v

in which O'T is the transpose of the column matrix 0'. Note that the indicialsummation form of the expression for U is equivalent to the matrix-multiplication form, but the latter is more convenient.

Complementary strain energy is defined as the internal work of strains mUltiplied by incremental stresses, integrated over the total stresses and over the volume. For the nonlinear case in Fig. 1-25a, the expression for complementary strain energy U* is

(1-17)

Here the term in parentheses represents the area between the curve and the stress axis in Fig. 1-25a. Evaluating this integral for the linear case in

- Fig. 1-25b (where E = CTEJCTi) gives the result


###### 1n" f 1f

U* = - L EjCTj dV = - ETU dV

(1-18)

2 ;=1 v 2 v

in which ET is the transpose of the column matrix E. Comparison of Eqs. (1-16) and (1-18) shows that the strain energy is equal to the complementary strain energy for linearly elastic materials. Of course, this fact can also be observed from Fig. 1-25b.

The external work ofloads may be written in a manner similar to that for strain energy, but for concentrated surface loads no integration over the volume is required. For this purpose, Fig. 1-26 shows nonlinear and linear load-displacement diagrams for a single load P and the corresponding displacement a. The external work W of all such loads in the nonlinear case is given by

p p

###### -t-tzzz~-t- -t--y- t,m=zz;>zzz£

###### dP dP

(a) (b)

###### Fig. 1-26. Load-displacement diagrams: (a) nonlinear and (b) linear.

![image 94](Matrix Analysis of Framed Structures_images/imageFile94.png)

Chapter I Basic Concepts of Structural Analysis

np I:l.j

W = j~1 10 Pd,1, (1-19)

in which np is the number ofloads. The integral in Eq. (1-19) represents the area between the curve and the displacement axis in Fig. 1-26a. Performing this integration for the linear case in Fig. 1-26b yields

(1-20)

The symbol AT in the latter form of this expression denotes the transpose of a column vector containing all of the applied actions, and D is a column vector of the corresponding displacements.

In addition, the complementary work of loads takes a form similar to that for complementary strain energy. For the nonlinear case in Fig. 1-26a, the complementary work of loads W* is defined as

np Pj

###### W* = j~1 10 ,1, dP (1-21)

In this instance the integral is seen to be the area between the curve and the load axis in Fig. 1-26a. Intem-ation for the linear case in Fig. 1-26b gives

- 1 np 1

W* = - L; ,1,.p. = - DTA

- 2 j =1 1 J 2


(1-22)

For the linear case, Eqs. (1-20) and (1-22) show that the work of the loads is equal to the complementary work of the loads, as can be observed from Fig. 1-26b.

For linearly elastic structures, it is possible to express strain energy and complementary strain energy in terms of stiffnesses and ftexibilities instead of stresses and strains. The first expression of this type is obtained by using the principle of conservation of energy, which states that the work of the loads W equals the strain energy U stored in the structure. Furthermore, the applied actions are known to be related to the corresponding displacements by either ftexibilities (Eq. 1-10) or stiffnesses (Eq. 1-12). Substitution of the latter relationship into the transposed form of Eq. (1-20) produces

- 1

U = W = -DTSD

- 2


(1-23)

###### Similarly, the principle ofconservation of complementary energy leads to the second expression

U* = W* = !ATFA

(1-24)

2

![image 95](Matrix Analysis of Framed Structures_images/imageFile95.png)

1.13 Energy Concepts 43

which results from substituting Eq. (1-10) into the transpose of Eq. (1-22). Of course, it is also true that U = U':' and W = W':', as has been shown before.

Energy theorems developed by Castigliano, Crotti, and Engesser [3] are widely used by structural engineers for establishing equilibrium and compatibility equations. Castigliano 's first theorem states that if the strain energy of an elastic body is expressed as a function of a set of displacements, the first partial derivative of that function with respect to a particular displacement is equal to the corresponding action. This theorem is valid for either nonlinear or linear elasticity, and application to the linear case of Eq. (1-23) gives

###### au 1/

~- = 2: Sit,D", = Ai

(j=\,2, .... 1I) ( \-25)

dDi "'~1

which may be verified by performing the detailed operations of matrix multiplication and differentiation. Equation (1-25) represents a set of II equilibrium conditions for a linearly elastic structure.

The Crotti-Engesser theorem states that if the complementary strain energy is written in terms of a set of applied actions, the first partial derivative of such a function with respect to a particular action is equal to the corresponding displacement. Differentiation of Eq. (1-24) in this manner yields

1/

2: Fj".Ah C~ Dj (j=1,2..... 1I) ( \-26)

"'~1

Equation (1-26) represents a .,et of 11 compatibility conditions for a linearly elastic structure.

Although the Crotti-Engesser theorem is valid for either nonlinear or linear systems, it is applied here only to the linear case. Thus, the complementary strain energy U'" in Eq. (1-26) could be replaced by the strain energy U. This specialized form of the Crotti-Engesser theorem is known as Castigliano's second theorem, which is valid only for linearly elastic structures.

By further differentiation of Eqs. (1-25) and (1-26), it is possible to obtain stiffnesses and flexibilities from strain energy and complementary strain energy. On the one hand, differentiating Eq. (1-25) with respect to D" yields a typical stiffness term Sj,," as follows:

- j = \, 2,. .. II
- k = \, 2, .... 11


(1-27)

Thus, it is seen that S)", is equal to the second partial derivative of U (expressed in terms of displacements) with respect to D j and D/.".

![image 96](Matrix Analysis of Framed Structures_images/imageFile96.png)

44 Chapter 1 Basic Concepts of Structural Analysis

On the other hand, differentiation of Eq. (1-26) with respect to Ak results in a typical flexibility coefficient Fik• That is,

- j = 1,2, ... , n
- k = 1,2, ... , n


(1-28)

Hence, Fik is equal to the second partial derivative of U* (expressed as a function of applied actions) with respect to Ai and A k•

At this point in the discussion it is convenient to observe reciprocal relations for stiffnesses and flexibilities. If the sequence of differentiation in Eq. (1-27) is reversed, the result must be the same, showing that

(1-29)

Because all pairs of cross stiffnesses are equal, the matrix S must be symmetric. Thus, it is equal to its own transpose, as follows:

(1-30)

This equality is also evident from Eq. (1-23), because U is a scalar and can be transposed.

Similarly, reversal of the sequence of differentiation in Eq. (1-28) shows that

(1-31)

Therefore, all pairs of cross flexibilities are equal,* and the matrix F is symmetric and equal to its own transpose. Hence,

(1-32)

This equality may also be deduced from Eq. (1-24) by observing that U* is a scalar and can be transposed.

Illustrations of the reciprocal relations discussed here can be seen by referring to the example at the end of Sec. 1.11. In that example the cross flexibilities FI2 and F21 are equal, and the flexibility matrix is symmetric. Similarly, the cross stiffnesses S12 and S21 are equal, and the stiffness matrix is also symmetric. Many additional examples of the reciprocal relations will be encountered later in connection with the flexibility and stiffness methods of analysis.

1.14 Virtual Work. This section will be devoted to concepts of virtual work and energy, as distinguished from the real work and energy discussed in the preceding section. Virtual work methods are more versatile than those involving real work because the displacements utilized may be due to influences other than the applied loads. When such loads are subjected to virtual displacements, they act at constant values instead of increasing gradually from zero. Use of this rather subtle idea provides additional

*Tbe reciprocal relation for flexibilities is also called Maxwell's theorem. because it was first presented by J. C. Maxwell in 1864.

![image 97](Matrix Analysis of Framed Structures_images/imageFile97.png)

1.14 Virtual Work 45

techniques for establishing equilibrium or compatibility conditions for structures. Furthermore, any desired actions, displacements, stiffnesses, or flexibilities may be determined without having to formulate strain energy or take derivatives.

Consider a conservative structure that is in a state of equilibrium under the influence of a set of applied actions A that cause internal stresses u. Then let the structure be subjected to any pattern of compatible virtual deformations that may be of interest. Such deformations must be continuous within the structure and consistent with geometric boundary conditions, but otherwise the selection is arbitrary. Included in the pattern will be external virtual displacements ilD, corresponding to the real actions A; and there also will be internal virtual strains ilE, corresponding to the real stresses u. The principle of virtual work states that the external virtual work of the real actions A multiplied by the virtual displacements ilD is equal to the internal virtual work of the real stresses u mUltiplied by the virtual strains ilE, integrated over the volume.

The external virtual work ilW is given by

(1-33) and the internal virtual work ilU may be written as

ilU = IvuTilEdV (1-34)

- A more appropriate name for this quantity is virtual strain energy. Applying the principle of virtual work gives the equality


- (1-35)
- (1-36)


ilW = ilU

and substituting Eqs. (1-33) and (1-34) into Eq. (1-35) produces ATilD = JvUTilE dV

To understand this virtual work equality, one should think of the real actions doing external work as they act at constant values through the virtual displacements. Simultaneously, the real stresses do internal work as they act at constant values during the virtual strains.

Equation (1-36) is true only if the structure is in equilibrium when it is also subjected to compatible virtual deformations. Conversely, ifEq. (1-36) is true, the structure is proven to be in equilibrium. In fact, equations of equilibrium may be derived from Eq. (1-36) by introducing appropriate stress-strain and strain-displacement relationships for the structure. This approach will be used in Chapter 7 for the analysis of framed structures by the method of finite elements.

At present, a useful technique for calculating actions and stiffnesses will be developed by specializing Eq. (1-36) as follows. If an action Aj is

unknown (such as a reaction), it can be found by letting oDj = 1 while all

other elements of 00 are zero. Then Eq. (1-36) yields

![image 98](Matrix Analysis of Framed Structures_images/imageFile98.png)

46 Chapter I Basic Concepts of Structural Analysis

(a)

where BEj is a vector of internal virtual strains for the condition BDj = 1. The equivalent transposed form

###### (1)Aj = IvBEJU dV (1-37)

will be more convenient in the ensuing discussion.

Equation (1-37) represents a technique known as the unit-displacement method, which can also be used to calculate stiffness coefficients. For this purpose, define a vector D of real displacements corresponding to the actions A, and let Dk = 1 while all other elements of D are zero. In this case the quantity Aj in Eq. (1-37) becomes the action oftypej due to a unit displacement of type k, which is the definition for Sjk' Thus, Eq. (1-37) becomes

###### (1)Sjk = Iv BEJ Uk dV (1-38)

in which Uk is a vector of internal stresses for the condition Dk = 1. This integral equation for Sjk, derived by the unit-displacement method, is used more frequently than the differential equation (Eq. 1-27) developed from strain energy in the preceding section.

To see the physical meaning of Eq. (1-38), it is helpful to refer to an example, such as that at the end of Sec. 1.11 (see Fig. 1-22). For the stiffness term S12 as an illustration, Eq. 0-38) gives

###### (1)S12 =IvBETU2dV (b)

In this case the external virtual work is equal to the product of S12 in Fig. 1-22e and the unit displacement (oftype 1) in Fig. 1-22d. The internal virtual work is calculated as the product of the stresses of type 2 (Fig. 1-22e) and the virtual strains of type 1 (Fig. 1-22d). Because such calculations are likely to be confusing, the subscripts on both sides of Eq. (1-38) have been arranged in the same sequence (by earlier transposition) to serve as a memory guide.

All of the concepts discussed so far in this section have complementary counterparts that may be examined by introducing the notion of virtual loads instead of virtual displacements. Such an approach leads to the unitload method, which is unexcelled for the purpose ofcalculating deflections and f1exibilities for framed structures. To begin, suppose that a conservative structure is in a state ofcompatible deformation with external displace-

- ments D and internal strains E. Then subject the structure to any desired set of virtual loads that are in equilibrium. Included in the set will be virtual actions BA, corresponding to the real displacements D; and there also will be internal virtual stresses 00, corresponding to the real strains E. The


![image 99](Matrix Analysis of Framed Structures_images/imageFile99.png)

1.14 Virtual Work 47

principle of complementary virtual work states that the external work of the virtual actions aA multiplied by the real displacements D is equal to the internal work of the virtual stresses &r multiplied by the real strains e, integrated over the volume.

The external complementary virtual work aW* will be written as

- (1-39)
- (1-40)


and the internal complementary virtuallt'ork OU* is

au* = Iv &rTe dV

This quantity is called the complementary virtual strain energy. Application of the principle of complementary virtual work yields

oW* = oU" (1-41)

Substitution ofEqs. (1-39) and (1-40) into Eq. (1-41) gives

OATD = Iv OUTe dV (1-42)

To visualize the nature of this complementary virtual work equality, it is helpful to imagine the virtual loads acting at constant values through the real displacements while the virtual stresses act at constant values during the real strains. Thus, one may think of the virtual loads as existing before the real displacements occur, instead of the sequence first described.

Equation (1-42) applies only to a structure in a compatible state ofdeformation when it is also subjected to virtual loads in equilibrium. Conversely, if Eq. (1-42) is true, the structure is proven to be in a compatible state. It follows that compatibility equations may be derived from Eq. (1-42) by bringing in appropriate strain-stress and stress-action relationships for the structure. However, this approach will not be pursued here because it is not suitable for the analysis of framed structures.

Instead, a method for calculating displacements and flexibilities will be developed by specializing Eq. (1-42) as follows. If the value of a particular displacement Dj is desired, it can be found by introducing a unit load oAj = 1 while all other elements ofoA are zero. (Typically, equilibrium is maintained by virtual reactions that do no work.) Then Eq. (1-42) becomes

(l)Dj = Iv ouTe dV (1-43)

where OUj is a vector of internal virtual stresses for the condition oAj = 1.

This unit-load method can also be used to calculate flexibility coefficients. To do this, let the vector A contain real actions corresponding to the displacements D, and let A" = 1 while all other elements of A are zero. In this instance the quantity Dj in Eq. (1-43) becomes the displacement of type j due to a unit action of type k, which is the definition for Fjk• Thus,

![image 100](Matrix Analysis of Framed Structures_images/imageFile100.png)

48 Chapter 1 Basic Concepts of Structural Analysis

(1)fjk= Ll)(JJtkdV (1-44)

in which Ek is a vector of internal strains for the condition At 1. This integral equation for fjb derived by the unit-load method, is much more useful than the differential equation (Eq. 1-28) developed from complementary strain energy in the preceding section.

As an illustration, consider the example at the end of Sec. 1.11 (see Fig. 1-22). Application of Eq. 0-44) to the calculation of the flexibility coefficient F21 gives

0)F21 = 1Vl)(JIEIdV (c)

Here the external complementary virtual work is equal to the product of the unit load (of type 2) in Fig. 1-22c and the flexibility F21 in Fig. 1-22b. The internal complementary virtual work is equal to the product of the virtual stresses of type 2 (Fig. 1-22c) and the strains oftype 1 (Fig. 1-22b). Note that subscripts on both sides of Eq. (1-44) have been deliberately arranged in the same sequence to serve as a memory guide.

Detailed examples of the unit-load method applied to various types of framed structures appear in Appendix A.2 for convenient reference throughout the book. In studying that appendix, the reader will see that for the slender members of framed structures it is simpler to work with stress resultants and corresponding displacements than with actual stresses and strains.

References

- 1. Norris, C. H., Wilbur, J. B., and Utku, S., Elementary Structural Analysis, 3rd ed., McGraw-Hill, New York, 1976.
- 2. Timoshenko, S. P., and Goodier, J. N., Theory of Elasticity, 3rd ed., McGraw-Hill, New York, 1970.
- 3. Gere, J. M., and Timoshenko, S. P., Mechanics of Materials, 3rd ed., PWS-Kent, Boston, MA, 1990.


Problems

- 1.4-1. A prismatic member is subjected to equal and opposite axial forces P at

the ends, thereby producing uniform tension in the bar. Define the displacement that corresponds to the two forces P.

- 1.4-2. Define the actions that correspond to the displacements Ae and 8e in the

plane frame shown in Fig. 1-6.

- 1.4-3. The simply supported beam shown in the figure has constant flexural


rigidity EI and length L. The loads on the beam are two actions Al and A2 as illustrated. Using Table A-3, obtain expressions in terms of A .. A2, E, I, and L for

![image 101](Matrix Analysis of Framed Structures_images/imageFile101.png)

Problems 49 each of the following: (a) the displacement D11 corresponding to action AI and caused by action AI acting alone; (b) the displacement DI2 corresponding to action AI and caused by A2 acting alone; and (c) the displacement DI corresponding to AI and caused by both actions acting simultaneously.

###### IAI A

A t ~2

A I 'k\

###### ~L12----+-----LI2~

Prob. 1.4-3.

1.4-4. For the cantilever beam shown in the figure, determine the displacements D11 , D21 , and D:lI using Table A-3. Assume that the beam has constant flexural rigidity EI.

Prob. 1.4-4.

1.4-5. The overhanging beam shown in the figure is subjected to loads Alo A 2, and Aa. Assuming constant flexural rigidity EI for the beam, determine the displacements D11 , D23, and D33 using Table A-3.

a; r2

B ~:3

A I i£ J

###### ~L12---4--LI2--+-L12

Prob. 1.4-5.

1.7-1. (a) What is the degree ofkinematic indeterminacy for a simply supported beam (see figure)? (b) If the effects of axial deformations are neglected, what is the degree of kinematic indeterminacy? (c) and (d) Repeat questions (a) and (b) for a cantilever beam that is fixed at one end and free at the other.

###### I

Prob. 1.7-1.

- 1.7-2. (a) What is the degree of static indeterminacy for the continuous beam shown in Fig. l-la? (b) What is the degree of kinematic indeterminacy? (c) If the effects of axial deformations are neglected, what is the degree of kinematic indeterminacy?
- 1.7-3. (a) Determine the number of degrees of static indeterminacy for the plane truss shown in Fig. I-lb. (b) Determine the degree of kinematic indeterminacy.
- 1.7-4. What is the degree of kinematic indeterminacy for the plane truss shown in Fig. 1-9?


![image 102](Matrix Analysis of Framed Structures_images/imageFile102.png)

50 Chapter 1 Basic Concepts of Structural Analysis

- 1.7-5. Determine the degrees of (a) static indeterminacy and (b) kinematic inde-

terminacy for the space truss in Fig. I-le.

- 1.7-6. Repeat Prob. 1.7-2 for the plane frame shown in the figure.

- Prob. 1.7-6.

1.7-7. Repeat Prob. 1.7-2 for the plane frame with pinned supports (see figure).

11

- Prob. 1.7-7.


- 1.7-8. Repeat Prob. 1.7-2 for the plane frame shown in the figure.

Prob. 1.7·8.

- 1.7-9. Repeat Prob. 1.7-2 for the plane frame shown in Fig. l-ld.
- 1.7-10. Repeat Prob. 1.7-2 for the plane frame shown in the figure.

Prob. 1.7-10.

- 1.7-11. For the grid shown in the figure, find (a) the degree of static indeter-


minacy and (b) the degree of kinematic indeterminacy.

Prob. 1.7-11.

![image 103](Matrix Analysis of Framed Structures_images/imageFile103.png)

51

Problems

- 1.7-12. Solve the preceding problem for the grid shown in the figure.

Prob. 1.7-12.

- 1.7-13. Repeat Prob. 1.7-11 for the grid shown in Fig. I-Ie.
- 1.7-14. Repeat Prob. 1.7-2 for the space frame shown in the figure.

Prob. 1.7-14.

- 1.7-15. For the space frame shown in the figure. repeat Prob. 1.7-2.

Prob. 1.7-15.

- 1.7-16. Repeat Prob. 1.7-2 for the space frame pictured in Fig. I-If.
- 1.7-17. For the space frame in the figure, repeat Prob. 1.7-2.


Prob. 1.7-17.

![image 104](Matrix Analysis of Framed Structures_images/imageFile104.png)

52 Chapter 1 Basic Concepts of Structural Analysis

1.10-1 to 1.10-10. Illustrate by means of sketches the physical significance of the flexibility and stiffness coefficients corresponding to the actions shown in the figures.

# A ~ A'11

tl A2 A2

- Prob. 1.10-1. GAl A2~

A ~ Prob. 1.10-7.

- Prob. 1.10-2.

~

tl t2

- Prob. 1.10-3.

~

(\2 (I

- Prob. 1.10-4. Prob. 1.10-8.

~

!AI (}A2

~

AI

- Prob. 1.10-5.

~

Aln A2t)A3

4 A2

- Prob. 1.10-6. Prob. 1.10-9. A2


###### AI

Prob. 1.10-10.

1.14-1. The simply supported beam shown in the figure has constant flexural rigidity EI. By the unit-load method of Appendix A.2, determine the following displacements due to actions AI and A2 applied simultaneously: (a) rotation at point A (positive counterclockwise); (b) translation at mid-span (positive upward); and (c) rotation at mid-span (positive counterclockwise).

~ -

n etc B

Ai A2

###### I--Ll2--Ll2-1

Prob. 1.14-1.

![image 105](Matrix Analysis of Framed Structures_images/imageFile105.png)

Problems 53

1.14-2. The cantilever beam shown in the figure has constant flexural rigidity El. By the unit-load method of Appendix A.2, calculate all terms in the flexibility matrix relating actions A I and A2 to their corresponding displacements.

Al ctA2

~-"":"------1~ B

###### _L/2~~L/2~1

Prob. 1.14-2.

1.14-3. For the overhanging beam in the figure, determine all coefficients in the flexibility matrix relating actions A I and A2 to their corresponding displacements. Use the unit-load method of Appendix A.2, assuming that the beam has constant flexural rigidity El.

Prob. 1.14-3.

1.14-4. The figure shows a truss subjected to an action Al in the form of a horizontal force at joint A and an action A2 consisting of two equal and opposite forces at joints A and D. All members of the truss are prismatic and have axial rigidity EA. Using the truss example in Appendix A.2 as a guide, find the displace-

- ments DI and D2 corresponding to Al and A2 and caused by these actions applied simultaneously.


###### A B

###### j

Al -cr------o-

A2

###### ~A2_I

Prob. 1.14-4.

1.14-5. The truss shown in the figure has the same axial rigidity EA for all of its members, which are prismatic. By the unit-load method of Appendix A.2, calculate all coefficients in the flexibility matrix relating actions Al and A2 to their corresponding displacements.

![image 106](Matrix Analysis of Framed Structures_images/imageFile106.png)

54 Chapter 1 Basic Concepts of Structural Analysis

-1

###### J

Prob. 1.14-5.

- 1.14-6. For the truss shown in the figure, determine the flexibility coefficients


F 12, F22, and F23• Use the unit-load method of Appendix A.2, assuming that all members are prismatic and have axial rigidity EA.

3L

###### L

Prob. 1.14-6.

![image 107](Matrix Analysis of Framed Structures_images/imageFile107.png)

###### 2Fundamentals of theFlexibility Method

2.1 Introduction. Basic concepts of the flexibility method (also called the force method) are described in this chapter. The flexibility method is a generalization of the Maxwell-Mohr method developed by J. C. Maxwell in 1864 and O. C. Mohr in 1874. In this approach statically indeterminate structures are analyzed by writing compatibility equations in terms of flexibility coefficients and selected redundants. Also involved in such equations are displacements calculated for a statically determinate version of the original structure (with the redundants released). Because the flexibility method requires extensive use of calculated displacements, the material in Appendix A will be referenced frequently.

The flexibility method is presented in matrix form in order to permit immediate generalization to complicated structures, even though the first problems to be solved are very simple and are devised solely to illustrate the basic concepts. A primary advantage of matrix notation is that it serves to organize the work and helps to avoid errors. Moreover, the solution process for a given problem is carried out in this chapter by finding the inverse of the flexibility matrix. This approach is symbolically convenient and is acceptable for small problems with few redundants. However, it is computationally more efficient to solve the simultaneous equations (as explained in Appendix D) than to calculate the inverse.

It should be realized at the outset that the flexibility method is not conducive to computer programming because the choice of redundants is not unique. In spite of this drawback, the student is urged to learn the method because it is useful for hand calculations. It also provides a good background for learning the stiffness method, which is mathematically similar and much more suitable for computer programming.

In this chapter the flexibility method is first developed for the basic purpose of finding redundants in structures that are subjected to applied loads only. Subsequently, the effects of temperature changes, prestrains, and support displacements are considered; and formulas for calculating joint displacements, member end-actions, and support reactions are developed as well. Then flexibility matrices for individual members are presented and used in assembling the over-all flexibility matrix for the structure by a formal procedure.

2.2 Flexibility Method. In order to illustrate the fundamental ideas of the flexibility method, consider the example shown in Fig. 2-1a. The

55

![image 108](Matrix Analysis of Framed Structures_images/imageFile108.png)

AABC~

AA---- r ----1~C

###### II--'---L-----1°1

(b)

###### A~I!;e@D1c

(e)

(e) B

Fig. 2-1. Illustration of flexibility method.

prismatic beam ABC in the figure has two spans of equal length and is subjected to a uniform load of intensity w. The beam is statically indeterminate to the first degree, since there are four possible reactions (two reactions at A, one at B, and one at C) and three equations of static equilibrium for actions in a plane. Because the loads are perpendicular to the beam, however. there is no need to consider a horizontal reaction at point A. The reaction RB at the middle support will be taken as the statical redundant, although other possibilities also exist. If this redundant is released (or removed), a statically determinate released structure is obtained. In this case, the released structure is the simply supported beam shown in Fig. 2-1b.

Under the action of the uniform load w, the released structure will deflect as illustrated in Fig. 2-1c. The displacement of the beam at point B is denoted as AB and is given by the expression (see Table A-3 of Appendix

A)

5wV

AB = 384EI

in which EI is the flexural rigidity of the beam. However, the actual beam is assumed to have no translation (that is, no settlement) at point B. Therefore, the redundant reaction RB must be such as to produce in the released structure an upward displacement equal to AB (see Fig. 2-ld). According to the principle of superposition, the final displacement at point B in the released structure is the resultant of the displacements caused by the load w and the redundant RB. The upward displacement due to RB is

- A = RBL3
- B 48EI


![image 109](Matrix Analysis of Framed Structures_images/imageFile109.png)

- as obtained from Table A-3 ofthe Appendix. Equating the two expressions obtained above for ~B gives


5wL4 R B L3 384EI 48EI

(2-1)

The unknown reaction RB may be obtained by solving Eq. (2-1):

5wL

RB =--8

After RB has been found, the remaining reactions for the two-span beam can be found from static equilibrium equations.

In the preceding example, the procedure was to calculate displacements in the released structure caused by both the loads and the redundant action and then to formulate an equation pertaining to these displacements. Equation (2-1) expressed the fact that the downward displacement due to the load was equal to the upward displacement due to the redundant. In general, an equation of this type can be called an equation of compatibility, because it expresses a condition relating the displacements ofthe structure. It may also be called an equation of superposition, since it is based upon the superposition of displacements caused by more than one action. Still another name would be equation of geometry, because the equation expresses a condition that applies to the geometry of the structure.

A more general approach that can be used in solving the two-span beam of Fig. 2-1a consists of finding the displacement produced by a unit value of RB and then multiplying this displacement by RB in order to obtain the displacement caused by RB• Also, it is more general and systematic to use a consistent sign convention for the actions and displacements at B. For example, it may be assumed that both the displacement at B and the reaction at B are positive when in the upward direction. Then the application of a unit force (corresponding to RB) to the released structure, as shown in Fig. 2-1e, results in a positive displacement 8B• This displacement is given by the expression

(2-2)

The displacement caused by RB acting alone on the released structure is 8BRB• The displacement caused by the uniform load w acting alone on the released structure is

~B = 384EI (2-3) This displacement is negative because ~B is assumed to be positive when

![image 110](Matrix Analysis of Framed Structures_images/imageFile110.png)

in the upward direction. Superposition ofthe displacements due to the load wand the reaction RB must produce zero displacement ofthe beam at point

- B. Thus, the compatibility equation is


- (2-4)
- (2-5)


from which

IlB

RB = --8B

When the expressions given above for 8Band IlB (see Eqs. 2-2 and 2-3) are substituted into Eq. (2-5), the result is

R _ 5wL

B- 8

which is the same as that obtained before. The positive sign in this result denotes the fact that RB is in the upward direction.

An important part of the preceding solution consists of writing the superposition equation (Eq. 2-4) which expresses the geometrical fact that the beam does not deflect at the support B. Included in this equation are the effects of the load and the redundant reaction. The displacement caused by the reaction has been conveniently expressed as the product ofthe reaction itself and the displacement caused by a unit value of the reaction. The latter is a flexibility coefficient, since it is the displacement due to a unit action. If all terms in the equation are expressed with the same sign convention, then the sign ofthe final result will denote the true direction ofthe redundant action.

If a structure is statically indeterminate to more than one degree, the approach used in the preceding example must be further organized, and a more generalized notation must be introduced. To illustrate these features, another example ofa prismatic beam will be considered (see Fig. 2-2a). The beam shown in the figure is statically indeterminate to the second degree; hence, a statically determinate released structure may be obtained by removing two redundant actions from the beam. Several choices for the redundants and the corresponding released structures are possible. Four such possibilities for the released structure are shown in Figs. 2-2b, 2-2c, 2-2d, and 2-2e. In the first of these figures, the reactive moment at A and the force at B are taken as the redundants; thus, the rotational restraint at A and the translational restraint at B are removed from the original beam in order to obtain the released structure. In the next case (Fig. 2-2c) the reactive moment at A and the internal bending moment at B are released. Therefore, the released structure has no rotational restraint at A and no restraint against bending moment at B. The latter condition is represented by the presence of a hinge in the beam at point B. The released structure shown in Fig. 2-2d is obtained by releasing both the reaction and bending

![image 111](Matrix Analysis of Framed Structures_images/imageFile111.png)

- ~ DOL' DOL2

P,i M C t; ~M fZ tP3

~A {7;\ ~A I -,C

f.-L/2+-L/2-to:L/2+ L/2-1

0, O2 ( f )

(0 )

Fz,

F"

###### A :l

~ t1

(b) ~

(g)

###### A ~

~

(c) F.

###### ~ (d) ~ ~ ~,"

~ (h)

(e)

Fig. 2·2. Illustration of flexibility method.

moment at point B. Lastly, the released structure shown in Fig. 2-2e is obtained by selecting the reactions at joints Band C as the redundants. This particular released structure is selected for the analysis which follows, although any of the others would be suitable. All of the released structures shown in Fig. 2-2 are statically determinate and immobile. In general, only structures of this type will be used in the discussions of the flexibility method.

The redundant actions that are selected for the analysis are denoted as QJ and Q2 in Fig. 2-2a. These actions are the reactive forces atjoints Band

- C. In Fig. 2-2f is shown the released structure acted upon by the various loads on the original beam, which in this example are assumed to be three concentrated forces PI, P2, and Pa and a couple M. These loads produce displacements in the released structure, and, in particular, displacements that correspond to QJ and Q2 are produced at joints Band C. These displacements are denoted D QLJ and DQL2 in the figure. In this notation the symbol DQL is used to represent a displacement corresponding to a redundant Q and caused by the loads on the structure. The numerical subscripts that follow the symbol denote the redundant to which the displacement corresponds. Thus, it is convenient to envisage DQL as one symbol, while the numbers that follow the symbol are the subscripts.* In Fig. 2-2f the


"In computer programming, the symbol D"L would be written DQL because of the necessity that all characters, whether alphabetic or numeric, be on the same line. When subscripts are present, they can be added to the basic symbol. For example, in a computer program DQL(1) is the usual way of writing DQ1•1• A similar style can be used for the other symbols that are encountered in subsequent work.

![image 112](Matrix Analysis of Framed Structures_images/imageFile112.png)

60 Chapter 2 Fundamentals of the Flexibility Method

displacements DQL are shown in their assumed positive direction, which is upward. The positive directions for the displacements must always be the same as the positive directions of the redundants to which the displacements correspond. Since the redundants are assumed to be positive when in the upward direction, the displacements are also positive upward.

In order to obtain the various flexibility coefficients that appear in the equations of compatibility, unit values of the redundants Ql and Q2 are applied separately to the released structure. For the condition Ql = 1 shown in Fig. 2-2g, the flexibility coefficient Fll is the displacement corresponding to Ql due to a unit value of Ql' and the coefficient F21 is the displacement corresponding to Q2 due to a unit value of Ql' For the condition Q2 = 1 shown in Fig. 2-2h, F12 is the displacement corresponding to Ql due to a unit value of Q2, and F22 is the displacement corresponding to Q2 due to a unit value of Q2' The flexibility coefficients are shown in their positive directions.

The superposition equations expressing the conditions of compatibility

- at joints Band C of the actual beam may now be written. Since the translational displacements at supports Band C are zero, the equations become


DQL1 + FllQl + F12Q2 = 0

(2-6) DQL2 + F21Ql + F22Q2 = 0

The first of these equations represents the total displacement at B, which consists ofthree parts: the displacement due to loads, the displacement due to Ql' and the displacement due to Q2' The superposition of all three displacements gives the total displacement, which is zero. Similar comments apply to the second equation. The two equations can be solved simultaneously for Ql and Q2, after which all other actions in the beam can be found by statics.

It is desirable at this stage of the discussion to write the superposition equations in a slightly more general form. It is always possible that support movements corresponding to the redundants will occur in the original beam, and these displacements can be included readily in the analysis. Assume that DQl and DQ2 represent the actual displacements in the beam corresponding to QI and Q2' Thus, DQI represents the support displacement at B, with the upward direction being positive. Similarly, DQ2 is the support displacement at C. The superposition equations express the fact that the final displacements corresponding to Ql and Q2 are equal to the sums of the displacements caused by the loads and the redundants; thus, the equations are:

DQl = DQL1 + FllQl + F12Q2 DQ2 = DQL2 + F21Ql + F22Q2

(2-7)

If there are no support displacements, as assumed in this problem, then DQl and DQ2 are both zero, and Eqs. (2-7) reduce to Eqs. (2-6). If there are

![image 113](Matrix Analysis of Framed Structures_images/imageFile113.png)

2.2 Flexibility Method 61

support displacements that do not correspond to a redundant, such as a displacement at joint A, they must be handled by the methods described later in Sec. 2.4.

The superposition equations (2-7) can be written in matrix form as

(2-8)

in which DQ is the matrix of actual displacements corresponding to the redundants, DQL is the matrix of displacements in the released structure corresponding to the redundant actions Q and ~ue to the loads, and F is the flexibility matrix for the released structure corresponding to the redundant actions Q. For the equations given above, these matrices are:

It should be noted that an alternate (and more consistent) symbol for a flexibility coefficient F would be Darb which represents a displacement in the released structure corresponding to a redundant Q and caused by a unit value of a redundant Q. Thus, the matrix F could also be denoted as DQU for consistency in notation, but the use of F for "flexibility" is more convenient.

The vector Q of redundants can be obtained by solving Eq. (2-8). Symbolically, the result is

(2-9)

in which F-1 denotes the inverse of the flexibility matrix. From this equation the redundants can be calculated after first obtaining the matrices DQ , DQL, and F. The first of these matrices will be known from the support conditions that exist in the original structure, while the last two are calculated from the properties of the released structure. The problem can be considered as solved when the matrix Q is known, since all other actions then can be found by static equilibrium. When the actions throughout the structure have been found, the displacements at any point can also be found. A method for incorporating into the analysis the calculation of actions and displacements at various points in the structure will be given in Sec. 2.5.

The matrix Du normally will be a null matrix 0 (that is, a matrix with all elements equal to zero), except when one or more of the redundants is a support reaction that has a support displacement corresponding to it. If the matrix DQ is null, Eq. (2-9) for the redundant actions Q becomes

(2-10)

This equation may be used instead of Eq. (2-9) whenever the displacements DQ are zero.

![image 114](Matrix Analysis of Framed Structures_images/imageFile114.png)

To show the use of the matrix equations given above, consider again the beam in Fig. 2-2a. In order to have a specific example, assume that the beam has constant flexural rigidity EI in both spans and that the actions on the beam are as follows:

###### M=PL P3 = P

Also, assume that there are no support displacements at any ofthe supports ofthe structure.

The matrices to be found first in the analysis are D Q, DQLo and F, as

mentioned previously. Since in the original beam there are no displacements corresponding to QI and Q2, the matrix DQ is a null matrix. The matrix DQL represents the displacements in the released structure corresponding to the redundants and caused by the loads. These displacements are found by considering Fig. 2-2f, which shows the released structure under the action of the loads. The displacements in this beam corresponding to QI and Q2 can be found by the methods described in Appendix A (see Example 3, Sec. A.2), and the results are:

97PV DQL2 = 48EI

D _ 13PL3

QLl - 24EI

The positive signs in these expressions show that both displacements are upward. From the results given above, the vector DQL is obtained:

###### PV [26] DQL = 48EI 97

The flexibility matrix F is found by referring to the beams pictured in Figs. 2-2g and 2-2h. The beam in Fig. 2-2g, which is subjected to a unit load corresponding to QI' has displacements given by the expressions

Similarly, the displacements in the beam of Fig. 2-2h are

###### 8L3 F22 = 3EI

5V

F12 =--6EI

From the results listed above, the flexibility matrix can be formed:

###### V[2 5]

###### F = 6EI 5 16

The inverse of the flexibility matrix can be found by anyone of several standard methods, the result being

###### -I = 6EI [16 -5]

F 7V -5 2

![image 115](Matrix Analysis of Framed Structures_images/imageFile115.png)

2.3 Examples 63

It should be noted that both the flexibility matrix and its inverse are symmetric matrices.

As the final step in the analysis, Eq. (2-10) may be used to obtain the redundant actions Q, as follows:

###### Q= [QIJ = - 6EI [ 16

-5J PV [26J P [ 69 J 2 48EI 97 = 56 -64

Q2 7V-5

From this expression it is seen that the vertical reactions at supports Band C of the beam in Fig. 2-2a are

8P

Q = 69P

Q2 =--

I 56

7

The negative sign for Q2 indicates that this reaction is downward.

The redundant actions having been obtained in the manner shown in this example, the remaining actions in the beam can be found from static equilibrium equations. Also, the displacements at any point in the beam can now be obtained without difficulty, inasmuch as all actions can be considered as known. For example, one method of finding displacements is to subdivide the beam into two simple beams. Then each simple beam is acted upon by known moments at the ends as well as by the loads, and the displacements can be calculated.

While the matrix equations of the flexibility method (Eqs. 2-8, 2-9, and 2-10) were derived by discussion ofthe two-span beam ofFig. 2-2, they are actually completely general. They can be applied to any statically indeterminate framed structure having any number of degrees of indeterminacy. Of course, in this event the matrices appearing in the equations will be of a different order than for the two-span beam. In general, if there are n degrees of statical indeterminacy, the order of the flexibility matrix F will be n x n, and the order of all the other matrices will be n x 1. In the next section several examples of finding redundant actions by the flexibility method will be given.

2.3 Examples. In order to illustrate the application of the flexibility method to structures of various types, several examples are given in this section. In each example it is assumed that the object of the analysis is to calculate the values of certain selected redundants; hence, the problem is considered to be solved when the matrix Q is determined. The redundants are selected in each example primarily for illustrative purposes; however, many other choices of redundants are possible.

Example 1. The beam AB shown in Fig. 2-3a is fixed at both ends and is subjected to a concentrated load P and a couple M at the midpoint. It is assumed that the beam has constant flexural rigidity EI.

In order to begin the analysis by the flexibility method, two redundant actions must be selected. In this example the vertical reaction and the reactive moment at

![image 116](Matrix Analysis of Framed Structures_images/imageFile116.png)

![image 117](Matrix Analysis of Framed Structures_images/imageFile117.png)

![image 118](Matrix Analysis of Framed Structures_images/imageFile118.png)

~

- (b)
- (c)

~)1

~ F,2

- (d) F22


![image 119](Matrix Analysis of Framed Structures_images/imageFile119.png)

![image 120](Matrix Analysis of Framed Structures_images/imageFile120.png)

Fig. 2·3. Example 1: Fixed-end beam.

end B of the beam are selected as redundants and are denoted in Fig. 2-3a as QI and Q2, respectively. The redundant QI is assumed to be positive in the upward direction, and Q2 is assumed positive in the clockwise direction. Other possible choices for the redundants include the reactive moments at both ends and the bending moment and shearing force at any section along the beam.

For the redundants shown in Fig. 2-3a, the released structure consists ofa cantilever beam (see Fig. 2-3b). The displacements in this beam corresponding to QI and Q2 and caused by the loads P and M are denoted by D(lLI and DQL2 in the figure. These displacements can be found with the aid ofTable A-3 in the Appendix, and are as follows:

SPL'1 3ML2 DQLI = - 48EI - 8EI

PU ML D(m = 8EI + 2EI

Since D(u., is downward, it is negative (opposite to Q,); but DQL2 is positive because it is clockwise (same as Q2)' Therefore, the vector DQL can be written as

###### L [(-SPU - 18ML)] DQL = 48EI (6PL + 24M)

![image 121](Matrix Analysis of Framed Structures_images/imageFile121.png)

###### 2.3 Examples 65

The flexibility coefficients are the displacements of the released structure caused by unit values of QI and Q2. as shown in Figs. 2-3c and 2-3d. These coefficients are as follows:

1:\

F" = 3~1

The flexibility matrix F can now be written, after which its inverse can be determined; these matrices are:

###### F-' -2EI [6

L [ 2U F = 6EI -3L

3L ] 2U

- L" 3L

The displacements in the fixed-end beam (Fig. 2-3a) corresponding to QI and Q" are both zero, since there is no vertical translation and no rotation at support B. Therefore, D'l is a null matrix, and the redundants can be found from Eq. (2-10). Substituting F-' and D'lL into that equation gives the following:

2EI [6 3L] L [(-5PU - 18ML)1 I [(4PL + 12M)] Q = -----v 3L 2U 48EI (6PL + 24M) J = 8L (PU + 2ML)

Therefore, the reactive force and moment at end B of the beam (see Fig. 2-3a) are

PL M

###### Q2 =8 + 4

These results can be confirmed by comparison with the formulas given in Appendix B (see Cases 1 and 2 of Table B-1).

Example 2. The three-span continuous beam shown in Fig. 2-4a has constant flexural rigidity EI and is acted upon by a uniform load l\' in span AB and concentrated loads P at the midpoints of spans BC and CD. Since the structure is statically indeterminate to the second degree, two redundant actions must be selected. In this example, the bending moments at joints Band C are chosen. When these moments are removed from the beam by inserting hinges at Band C, the released structure is seen to consist of three simple beams (Fig. 2-4b). The redundant moments Q, and Qz are shown acting in their positive directions in Fig. 2-4b. Each redundant consists of two couples, one acting on each adjoining span of the structure. For example, the left-hand couple in QI acts on beam AB in the counterclockwise direction, while the right-hand couple in Q, acts on span BC in the clockwise direction. The positive direction of each Q corresponds to that of a bending moment which produces compression at the top of the beam. Therefore, a positive sign in the final solution for either Q, or Q2 means that the redundant moment produces compression at the top of the beam; if negative, the redundant moment produces tension at the top of the beam.

The displacement corresponding to one of the redundant moments consists of the sum oftwo rotations, one in each adjoining span. For example, the displacement corresponding to Q, consists of the counterclockwise rotation at joint B of the righthand end of member AB plus the clockwise rotation at joint B of the left-hand end of member BC. In a similar manner, the displacement corresponding to Qz is the sum of the two rotations at joint C.

The displacements Dw., and Dim corresponding to Q, and Qz, respectively, and caused by the loads acting on the released structure, are shown in Fig. 2-4c.

![image 122](Matrix Analysis of Framed Structures_images/imageFile122.png)

Chapter 2 Fundamentals of the Flexibility Method

66

###### r c r 0

![image 123](Matrix Analysis of Framed Structures_images/imageFile123.png)

4 ~

###### I---L---J.L12+42+L/2-+L/21

![image 124](Matrix Analysis of Framed Structures_images/imageFile124.png)

(0)

![image 125](Matrix Analysis of Framed Structures_images/imageFile125.png)

###### J$: ~~B ~~~C ~

A

0

(b)

![image 126](Matrix Analysis of Framed Structures_images/imageFile126.png)

###### DOL' °OL2

###### A~rVI ~

B ~C

(C)

F" F2,

![image 127](Matrix Analysis of Framed Structures_images/imageFile127.png)

###### A~ ~

###### 8 c

###### (d)

fi2 F22

![image 128](Matrix Analysis of Framed Structures_images/imageFile128.png)

###### ~1

~~c

(e)

Fig. 2-4. Example 2: Continuous beam.

Because the counterclockwise rotation at end B of member AB due to the uniform load w is

I1'L'J

24£1

and the clockwise rotation of end B of member Be due to the load P is

###### PL2 16£1

it follows that the displacement DIJL! is

In a similar manner, the displacement DIJL2 is seen to be

###### PV PV PV

DIJL2 = 16£1 + 16£1 = BEl

![image 129](Matrix Analysis of Framed Structures_images/imageFile129.png)

2.3 Examples 67

Thus, the vector DYL can be written as

D = L [(2I1'L + 3P)J

###### YI 48£1 6P

The flexibility matrix must be found next. For this purpose, unit values of QI and Q2 are shown acting on the beams in Figs. 2-4d and 2-4e. The flexibility coefficient Fll (see Fig. 2-4d) is the sum of two rotations at joint B; one rotation is in span AB and the other is in span Be. Similarly, the coefficient F21 is the sum of the rotations at joint C. In Fig. 2-4d, however, the rotation in span CD is zero. Therefore, F21 is equal to the rotation in span BC alone. Similar comments apply to the flexibility coefficients shown in Fig. 2-4e. The rotations produced at the ends of a simply supported beam by a couple of unit value applied at one end of the beam are

L L

3EI and 6EI

at the near and far ends of the span, respectively, as given in Case 5, Table A-3. From these formulas the flexibility coefficients pictured in Figs. 2-4d and 2-4e can be obtained, as follows:

###### L

2L

Fll = 3EI

FI2 = 6EI 2L

L

F.,.)=--

F21 = 6EI

###### -- 3EI

Therefore, the flexibility matrix is

F= 6~1[1 ~J

and its inverse becomes

###### F-' =2EI [ 4 -41J

###### 5L -I

The displacements DIJ' and DIJ2 in the original beam (Fig. 2-4a) corresponding to QI and Q2, respectively, are both zero because the beam is continuous across supports Band C. Therefore, the matrix D(~ is null and Eq. (2-10) can be used to determine the redundants, as shown:

-I J£[(2I1'L+3P)J=_~[ (8I1'L+6P) J

Q = _2EI [ 4 5L -I

4 48EI 6P 120 (-2I1'L + 21P)

Thus, the redundant bending moments QI and Q2 are given by the following formulas:

II'U PL

QI = -15-20

Having obtained these moments at the supports, the remaining bending moments in the beam, as well as shearing forces and reactions, can be found by statics.

Example 3. The plane truss shown in Fig. 2-5a is statically indeterminate to the second degree. The horizontal reaction at the support B (positive to the right) and the axial force in bar AD (positive when tension) are selected as the redundants,

![image 130](Matrix Analysis of Framed Structures_images/imageFile130.png)

68 Chapter 2 Fundamentals of the Flexibility Method

###### 2P

P

2P (0 ) ( b)

P

<;c--------;;>--i~ -

###### F;,

(c) (d) (e)

Fig. 2-5. Example 3: Plane truss.

resulting in the released structure shown in .Fig. 2-5b. In that figure the support at B has been removed, thereby releasing the reactive force QJ, and the bar AD has been cut at some intermediate location in order to release the axial force Q2 in the bar. Many other combinations of bar forces and reactions could be taken as redundants in this example, and each,would give a different released structure. In all cases in which the force in a bar is selected as a redundant, the bar must be cut to obtain the released structure. The cut bar then remains as part of the released structure, because its deformations must be inchlded in the calculation of displacements. It should be observed that Q2 consists of a pair of equal and opposite forces acting on the cut ends of bar AD. This type of redundant is analogous to those described in Example 2, where a redundant bending moment was considered as a pair of couples acting on the released structure (see Fig. 2-4b). From this discussion it follows that a displacement corresponding to Q2 consists of a relative translation of the cut ends of bar AD. When the cut ends are displaced toward one another, the displacement is in the same direction as Q2 and hence is positive. When the cut ends are displaced apart from one another, the displacement is negative.

The first step in the analysis consists of determining the displacements in the released structure corresponding to QI and Q2 and due to the loads P and 2P acting at joint A. These displacements are denoted as D QL1 and DQL2 and are represented by vectors in Fig. 2-Sc. This manner of representing the displacements is used in lieu of drawing the structure in its displaced configuration, which may become difficult for complicated structures. The determination of these displacements may be carried out by the unit-load method, as illustrated in Example 1 of Sec. A.2 in the Appendix. Assuming that all members of the truss have the same axial rigidity EA, it is found that the displacements due to the loads P and 2P are

![image 131](Matrix Analysis of Framed Structures_images/imageFile131.png)

###### 2.3 Examples 69

Therefore, the vector D(JI is

###### D __ PL [3.828] (JL - EA 2

The minus sign for Dill! means that it is a displacement to the left, and the minus sign for D"L2 means that the cut ends of the bars are moved apart from one another.

The next step in the analysis involves the determination of the displacements in the released structure corresponding to Q, and Qz and caused by unit values of Q, and Qz. Such displacements will constitute the flexibility matrix F and also can be found by the unit-load method. When using the unit-load method for the released structure shown in Fig. 2-5, it is essential that all members of the released structure, including bar AD. be included in the calculations. The flexibility coefficient FII is the displacement corresponding to Q, and caused by a unit value of Q, and is shown as a vector displacement in Fig. 2-5d. This displacement is

###### L - L

FII = EA (1 + 2y2) = 3.828 EA

The flexibility coefficient F2, is the displacement corresponding to Qz and due to a unit value of Q, (see Fig. 2-5d). Similarly, the coefficients F,z and F22 represent displacements in the released structure of Fig. 2-5e. When all of these displacements are obtained, the results are as follows:

###### L - L

F'2 = F2 , = '2F.I (4 + y2) = 2.707 leA

2L - L

F22 = EA (1 + y2) = 4.828 EA

Finally, the flexibility matrix can be formed and its inverse determined:

F - ~ [3.828 2.707]

- EA 2.707 4.828 F-1 _ EA [ 0.4328 -0.2426]

- L -0.2426 0.3431

Assuming that there are no support displacements in the truss. the redundants Q can be found by means of Eq. (2-10):

Q = EA [ 0.4328 -0.2426] PL [3.828] = P [ 1.172]

L -0.2426 0.3431 EA 2 -0.243 Therefore, the horizontal reactive force at B (Fig. 2-5a) is

Q, = I.172P and the axial force in bar AD is

###### Q2 = -0.243P

![image 132](Matrix Analysis of Framed Structures_images/imageFile132.png)

The minus sign for Q2 shows that the member is in compression. From the above results, one can calculate the remaining reactions and bar forces by statics.

Now assume that when the loads P and 2P act on the truss, support B moves a small distance s horizontally to the left. Therefore, the displacement Dell (see Eq. 2-7) is equal to minus s. The displacement DU2 is zero, since it represents the relative displacement of the cut ends ofbar AD in the original truss. The redundants Q can now be found from Eq. (2-9), as follows:

###### =[-0'433S~A+1.172pl

Q = EA [ 0.4328 -0.2426] { [-s] + PL [3.828] } L -0.2426 0.3431 0 EA 2

sEA

0.247 - 0.243P Therefore, the horizontal reaction at B is

sEA

QI = -0.433 L + 1.I72P and the force in bar AD is

sEA

Q2 = 0.243 L - 0.243P

In this example there was a redundant action (QI) corresponding to the support displacement at joint B. Of course, if other redundants had been selected, such as the forces in the two diagonal bars, the displacement at support B could not have been included in the vector DQ• Then it would be necessary to account for the support displacement by another means, such as that described later in Sec. 2.4.

Example 4. The plane frame shown in Fig. 2-6a has fixed supports at A and C and is acted upon by the vertical load P at the midpoint of member AB. It is desired to analyze the frame, taking into account the effects of both flexural and axial deformations. The inclusion of axial effects is for illustrative purposes only; normally, in a frame of this type, only flexural effects need be considered, and the analysis would be simplified slightly. The members ofthe frame have constant flexural rigidity EI and constant axial rigidity EA. The structure is statically indeterminate to the third degree, and a suitable released structure (see Fig. 2-6b) is obtained by cutting the frame atjoint B. thereby releasing two forces and a bending moment. These released actions are the redundants QIo Q2, and Qa, as shown in Fig. 2-6b. A displacement in the released structure corresponding to Ql consists of the horizontal translation ofend B of member AB (taken positive to the right) plus the horizontal translation of end B of member BC (taken positive to the left). In other words, a displacement corresponding to Ql consists of the sum of two translations and represents a relative displacement between the two points labeled B in Fig. 2-6b. In a similar manner the displacements corresponding to Q2 and Qa can be defined as the sum of two vertical translations and two rotations, respectively, at joint B.

The displacements in the released structure caused by the load P and corresponding to QI' Q2, and Qa are shown in Fig. 2-6c. For example, the displacement DULl is shown in the figure to consist of two horizontal translations, as described in

![image 133](Matrix Analysis of Framed Structures_images/imageFile133.png)

2.3 Examples 71

{dl

{o l

S2 F.. ~,c;2

ItB~---F,2 l'.l-1

F,2 C

F22t

{bl {el

F;3 1'33

--- -1

~~ rrv23

t F,3

F;3 F,3 C

{el { f l

Fig. 2-6. Example 4: Plane frame.

the preceding paragraph. Similarly, the displacements D/lL2 and D/lL:l are shown as two vertical translations and two rotations, respectively. It is not difficult to calculate these displacements due to the force P. inasmuch as the released structure consists of two cantilever members. First, taking the member AB in Fig. 2-6c, it is seen that the displacements at end B are as follows:

###### PU

8El

These expressions are based upon only the flexural deformations of member AB because there are no axial deformations. Secondly, the member BC in Fig. 2-6c must be considered. In this example there is no load on member BC and hence no displacements at end B; therefore,

(D/lLlhc = (D/lL2)RC = (D/l[.:l)BC = 0

The final displacements caused by the load P can now be obtained by combining the above results:

Therefore, the matrix DQL is

![image 134](Matrix Analysis of Framed Structures_images/imageFile134.png)

The flexibility matrix must be determined next. Consider first the released structure with the action Q, = 1 applied to it, as shown in Fig. 2-6d. The displacements corresponding to Q" Q2, and Q3 are shown in the figure as the flexibility coefficients F", F 2" and F:lI . If both axial and flexural deformations are considered, the displacements at end B of member AB are

L

(FII)AB = EA

Also, the displacements at end B of member Be are

Therefore, the final values of the three flexibility coefficients shown in Fig. 2-6d are

Next, the same kind of analysis must be made for actions Q2 = I and Q3 = I acting on the released structure. These conditions are shown in Figs. 2-6e and 2-6f, and the various flexibility coefficients are found to be as follows:

###### L2

L:l H

- F22 = 3EI + EA L2
- F23 = 2EI


- F32 = 2EI L H
- F33 = EI + EI


Finally, the flexibility matrix can be assembled:

H2 2EI

###### L H3

0

EA + 3EI

F= 0 3EIL3 + EAH

L2

(a)

2EI L H EI + EI

H2 V 2EI 2EI

If axial deformations were to be neglected in the analysis, the two fractions in F containing the a.xial rigidity EA in the denominators would be omitted.

The next step in the solution is to obtain the inverse of the flexibility matrix and then to substitute it, as well as the matrix DQL, into Eq. (2-10). It is possible to use Eq. (2-10) in this example because the displacements DQ are all equal to zeto, inasmuch as joint B in the original frame (Fig. 2-6a) is a rigid connection. However, the inverse of the flexibility matrix F given above cannot be obtained conveniently in literal form, as was done in the preceding examples where F was a 2 x 2 matrix. For this reason the flexibility matrix in Eq. (a) will be simplified by letting H = L and by introducing a nondimensional parameter y, defined as

I

y = AL2

With this notation the flexibility matrix can be rewritten as

![image 135](Matrix Analysis of Framed Structures_images/imageFile135.png)

- 2.3. Examples 73


_ ~ [2V(l + 3'}')

-3L] 3L

(b)

F - 6EI 0

-3L

12

Note that when the cross-sectional area A becomes large, the parameter,}, tends to zero. In that case the factor (1 + 3'}') in Eq. (b) becomes unity.

The inverse of the flexibility matrix F, as given in Eq. (b), is found to be

F-) = --EI [3a-93 3-a93 -6La6La) ]

2L3a)a2 6La) -6La) 4L2i

This matrix contains three additional dimensionless parameters, which are defined as follows:

a2 = 1 + 12'}' a:j = 5 + 24'}' Substitution ofF-t and DQL into Eq. (2-10) produces

_p [ 3a~ ] Q = 32ala2 2ia~~~

where

as = 13 + 84'}'

a~ = 1 - 12'}'

In terms of ,}" the redundants are

3P 1 - 12'}'

QI = - 32 (1 + 3'}')(l + 12'}')

###### 13P 1 + 84'}'/13

Q2 = 32 (1 + 3'}')(l + 12'}')

PL 1 - 12'}' Q:j = -16 1 + 12'}'

The minus signs for Ql and Q3 show that these actions are opposite in direction to the positive senses shown in Fig. 2-6b.

For typical plane frames the magnitude of'}' is of the order IO-a; so the factors

- 1 - 12 '}', etc., are approximately 1.0. If axial deformations are neglected altogether (that is, if'}' = 0), the redundants become


###### Q _ 13P

###### PL

Qa = -16

2 - 32

These values are sufficiently accurate for most practical purposes.

Example 5. The grid structure shown in Fig. 2-7a is in a horizontal plane (x-z plane) and carries a load P acting in the vertical direction. The supports of the grid at A and C are fixed, and the members AB and BC have length L, flexural rigidity EI, and torsional rigidity GJ (see Appendix A for definition of torsional rigidity). The redundants that are chosen for this example are released by cutting the grid atjoint B (Fig. 2-7b), thereby giving a released structure in the form of two cantilever beams. Each redundant consists of a pair of actions, and these actions

![image 136](Matrix Analysis of Framed Structures_images/imageFile136.png)

###### 74 Chapter 2 Fundamentals of the Flexibility Method

###### r

(d)

- (b) (e)
- (c) (f)


Fig. 2-7. Example 5: Grid.

are shown in their assumed positive senses in Fig. 2-7b. There are no other internal actions at joint B. because in a grid with only vertical loads there are no horizontal forces between members and no couples about a vertical axis.

When the load P is applied to the released structure (Fig. 2-7c), displacements DQL are produced. These displacements are shown in their positive directions in the figure. Note that a translational displacement is denoted by a single-headed arrow, while a rotation is denoted by a double-headed arrow. This representation is analogous to the convention that is used when indicating forces and couples. The displacements shown in Fig. 2-7c can be obtained without difficulty, and then the matrix DQL can be formed:

###### PU [ 5L]

###### DQL = 48EI _~

The flexibility coefficients are the displacements shown in Figs. 2-7d, 2-7e, and

- 2-7f. For these figures, it is assumed that unit values ofthe redundants QI> Q2, and Qa are applied one at a time to the released structure. The desired coefficients can be obtained from the figures, and the flexibility matrix is found to be


- 2U L2 U
- 3EI 2EI 2EI


L2 L L

F=

0

2EI EI + GJ

L2

L L

0

2EI EI + GJ

![image 137](Matrix Analysis of Framed Structures_images/imageFile137.png)

This matrix can be written in a simpler form by introducing a nondimensional parameter p, defined as the ratio of the flexural and torsional rigidities:

p=-El

###### GJ

With this notation the flexibility matrix can be put into the following form:

-3L 1

L [4L2 3L

F = 6EI 3L 6(1 + p)

6(1 ~ p)

-3L 0

The inverse of F is

###### -6Lbl

L2b:1

###### -3U

in which the following additional nondimensional parameters are used:

###### bl = 1 + P b2 = 1 + 4p b:l = 5 + 8p

Finally, substitution into Eq. (2-10) yields the vector of redundants:

###### Q -P [2blb~l

###### = 16b b -Lb~ I 2 -3Lp

where

b~ = 2 + 5p

Thus, the redundants are as follows:

Q __!.. 2 + 5p 1 - 8 1 + 4p

PL 2 + 5p

Q2 = 16 (l + p)(l + 4p) 3PL p

Qa = 16(l + p)(l + 4p)

If the members AB and Be are torsionally very weak, then p can be considered as infinitely large. The above formulas then give the following values for the redundants (after dividing the numerators and denominators by p):

This result could also be obtained by assuming that a spherical hinge exists at B which transmits vertical force but not moment. Such a grid would be statically indeterminate to the first degree.

2.4 Temperature Changes, Prestrains, and Support Displacements. It is frequently necessary to include in the analysis of a structure not only the effects of loads but also the effects of temperature changes, prestrains of members, and displacements of one or more supports. In most cases

![image 138](Matrix Analysis of Framed Structures_images/imageFile138.png)

76 Chapter 2 Fundamentals of the Flexibility Method

these effects can be incorporated into the analysis by including them in the calculation ofdisplacements in the released structure. As an example, consider the effects of temperature changes. If the changes are assumed to occur in the released structure, there will be displacements corresponding to the redundant actions Q. These displacements can be identified by the symbol DOT, which is analogous to the symbol DQL used previously to represent displacements in the released structure corresponding to the redundants and caused by the loads. The temperature displacements DOT in the released structure may be due to either uniform changes in temperature or to differential changes in temperature, as discussed in Appendix A.

When the matrix DQT of displacements due to temperature changes has been obtained, it can be added to the matrix DQL of displacements due to loads to give the sum of aU displacements in the released structure. Then these total displacements can be used in the equation of superposition (see Eq. 2-8) in place of DQL alone. Therefore, the superposition equation becomes

DQ =DQL +DQT +FQ

which can be solved for the vector Q of redundants as before. An illustration ofthe calculation ofthe vector DQT to be used in this equation is given in a later example.

The effects ofprestrains in any member ofthe structure can be handled in a manner analogous to that for temperature changes. By prestrain of a member is meant an initial deformation ofthe member due to any ofvarious causes. For example, a truss member may be fabricated with a length greater or less than the theoretical length ofthe member, or a beam may be fabricated with an initial curvature. It can be seen intuitively that a truss member having prestrains consisting of an initial elongation will produce the same effects in the truss as ifthe member had been heated uniformly to a temperature that would produce the same increase in length. Thus, the method of analysis for prestrain effects is similar to that for temperature changes. The first step is to assume that the prestrains occur in the released structure. Then the displacements in the released structure corresponding to the redundants must be found. These displacements are denoted DQP, signifying that they correspond to the redundants and are due to prestrain effects. The matrix DQp for the prestrain displacements can then be added to the matrices DQL and DQT to give the sum of aU displacements in the released structure. Then the sum of all displacements is included in the equation of superposition, as follows:

DQ = DQL + DQT + DQp +FQ

As before, the superposition equation can be solved for the matrix of redundants Q. An example involving the calculation of prestrain displacements will be given later.

Lastly, consider the possibility ofknown displacements occurring at the

![image 139](Matrix Analysis of Framed Structures_images/imageFile139.png)

restraints (or supports) of a structure. There are two possibilities to be considered, depending upon whether or not the restraint displacement corresponds to one of the redundant actions Q. If the restraint displacement does correspond to a redundant, its effects can be taken into account by including the displacement in the vector DQ of actual displacements in the structure. This procedure was discussed before in Sec. 2.2 and was illustrated in Sec. 2.3 in an example of a statically indeterminate truss (see Example 3). In a more general situation, however, there will be restraint displacements that do not correspond to any of the selected redundants. In that event, the effects of such restraint displacements must be incorporated in the analysis of the released structure in the same manner as in the case of temperature and prestrain effects. When the restraint displacements are assumed to occur in the released structure, there will be displacements DQR corresponding to the redundants Q. When these displacements have been found, the matrix DQR can be obtained. Then this matrix can be added to the other matrices representing displacements in the released structure.

The combination of all matrices representing displacements in the released structure will be denoted DQC in future discussions. It can be expressed as follows:

(2-11)

Thus, the matrix DQC contains displacements due to all causes, including loads, temperature changes, prestrain effects, and restraint displacements. With this notation, a generalized form of the superposition equation for the flexibility method becomes

(2-12)

The superposition equation used previously (Eq. 2-8) can be considered as a special case of Eq. (2-12). When the latter equation is solved for Q, the result is

(2-13)

and this equation may be used in place of Eq. (2-9) when causes other than loads must be considered. Of course, in any particular analysis it is not likely that all of the matrices given in Eq. (2-11) will be of interest. Some examples of the use of the above equations will now be given.

Example 1. In order to illustrate the analysis of a structure when temperature changes are present, consider the two-span beam ABC in Fig. 2-8a. The beam is assumed to be subjected to a linear temperature gradient such that the top surface of the beam has a temperature change .:l T2, while the lower surface has a change .:l T1• Previously, this same beam was analyzed for the effects of loads (see Fig. 2-2), and in that solution the reactions at supports Band C were taken as the redundants QI and Q2' These same redundants will be used again in solving for the thermal effects. Therefore, the inverse of the flexibility matrix may be taken from the former solution (see Sec. 2.2) to be

![image 140](Matrix Analysis of Framed Structures_images/imageFile140.png)

~A ATAT,z B AT2 C

~ AT, ~

###### f---L -to, L--102

###### (0)

ATz O~OQTZ

~

###### AT,

(bl

Fig. 2-8. Example 1: Continuous beam of Fig. 2-2.

F-l - 6EI [16 -52]

###### -7L" -5

Also, the vector D'l (see Eq. 2-13) giving the actual displacements in the beam is a null vector (D'l = 0).

The released structure for the beam ABC is the cantilever beam shown in Fig. 2-8b. If the temperature change ATI is greater than AT2, the released beam will deflect upward, as indicated in the figure. The displacements corresponding to the redundants are denoted DQn and DQn. These displacements can be calculated by the unit-load method described in Appendix A (see Example 4 in Sec. A.2). Thus, the displacements DQTI and DQn are found to be

a(ATI - AT2)L2 d 2a(ATI - AT2)L2

2d an d

respectively. In these expressions a is the coefficient of thermal expansion for the material, and d is the depth of the beam. The vector DQT is

D= a(ATI - AT2)L2[I]

QT 2d 4

If only the effects of temperature are considered in the analysis of the beam, the vector DQT becomes the vector DQC in Eq. (2-13). Then the redundants as found from that equation are

The signs on the elements of Q show that the redundant reaction QI is upward when A T, is greater than A T2, while the redundant Q2 is downward. If ATI is less than AT2, the directions of the redundants will be reversed. Of course, if ATI is equal to AT2, the redundants are zero.

If the combined effects of both loads and temperature are desired, the matrix DQC in Eq. (2-13) is taken as the sum of DQT (obtained above) and DQL (obtained in Sec. 2.2). Values of the redundants under the combined conditions will be the sum of the values obtained for temperature changes and loads taken separately.

Example 2. As a second example illustrating the effects of a temperature change, consider the plane truss shown previously in Fig. 2-5a and assume that bar BD has its temperature increased uniformly by an amount AT. The resulting elonga-

![image 141](Matrix Analysis of Framed Structures_images/imageFile141.png)

- 2.4 Temperature Changes, Prestrains, and Support Displacements 79


A

###### I

L

L~

Fig. 2-9. Example 2: Plane truss of Fig..2-S.

tion will produce displacements DQT in the released structure corresponding to the redundants. These displacements, denoted DQTI and DQ72' are shown in Fig. 2-9 in their positive directions (compare with Fig. 2-5c, which shows the displacements in the released structure due to loads). The displacements DQT can be readily found by the unit-load method, as illustrated in Example 2 of Sec. A.2. By this means the vector DOT is found to be:

The temperature effects can now be incorporated into the analysis of the truss by including the matrix DOT in the calculation of Doc (see Eq. 2-11).

If the member BD of the truss in Fig. 2-5a were fabricated with a length L + e instead of L, the analysis could be handled in the same manner as shown above for a temperature change in the bar. The only difference is that the prestrain elongation e would replace the temperature elongation otLI1 T for bar BD. Therefore, the vector of prestrain displacements in the released structure would be (see Example 2, Sec. A.2):

A prestrain of any other bar could be handled in a similar fashion.

Example 3. This example illustrates how restraint displacements can be taken into account. Refer again to the two-span beam shown in Fig. 2-2a and assume that the following two support displacements occur. Joint A undergoes a known rotation in the clockwise direction of f3 radians, and joint B is displaced downward by a distance s. The displacement at B corresponds to one of the redundants and therefore is accounted for in the vector DQ, which now becomes

###### [-s]

D'l = 0

![image 142](Matrix Analysis of Framed Structures_images/imageFile142.png)

I--L ---+·1......· -L--l

Fig. 2-10. Example 3: Support rotation in released structure.

The minus sign is required in the first element inasmuch as QI is positive when upward. The restraint displacement at support A is included in the analysis by means ofthe matrix DQR (see Eq. 2-11). This matrix consists ofthe displacements in the released structure (see Fig. 2-10) when joint A is rotated through the clockwise angle 13. Therefore, the displacements DQR' and DIJR2 corresponding to QI and Q2 are

###### -f3L and -2f3L

respectively. These terms are negative because they are downward. Thus, the matrix DQR is

Finally, this matrix can be included in the calculation of DQc, after which Eq. (2-13) can be solved for the redundants. As in the other illustrations, the values of the redundants due to the combined effects will be equal to the sum of the values obtained separately.

2.5 Joint Displacements, Member End-Actions, and Support Reactions. In the preceding sections the emphasis was on finding redundant actions by the flexibility method. The redundant actions may be either internal stress resultants (such as axial forces and bending moments) or external reactions at points of support. In all cases it is possible to find other actions in the structure by using principles of static equilibrium after the redundants have been calculated. Such calculations would normally include the support reactions and the actions at the ends of each member (member end-actions). Furthermore, when all actions in the structure are available, it is possible to calculate all displacements. Usually the displacements of primary interest are the translations and rotations of the joints.

Instead of following the procedure described above, it is more systematic to incorporate the calculations for the joint displacements, member end-actions, and support reactions directly into the basic computations for the flexibility method. That is, the task of finding the various actions and displacements that are of interest can be performed in parallel with the computations for finding the redundants instead ofpostponing them as separate calculations to be performed after the redundants are determined.

In order to demonstrate the procedure for making a complete analysis of a structure, the two-span beam example given previously in Fig. 2-2 will now be extended. The beam to be analyzed is shown again in Fig. 2-11a. Assume that it is desired to calculate not only the redundants Ql and Q2 for the beam, but also the joint displacements, member end-actions, and support reactions. The joint displacements in a structure will be denoted by

![image 143](Matrix Analysis of Framed Structures_images/imageFile143.png)

- 2.5 Joint Displacements, Member End-Actions, and Support Reactions 81


![image 144](Matrix Analysis of Framed Structures_images/imageFile144.png)

(0 )

t 80 (8 C0

![image 145](Matrix Analysis of Framed Structures_images/imageFile145.png)

AM2 AM4 CA

![image 146](Matrix Analysis of Framed Structures_images/imageFile146.png)

###### tM1 AMJ

###### t

r

(b )

![image 147](Matrix Analysis of Framed Structures_images/imageFile147.png)

r M~

3

Dola

~ -'-- --

( 1

ARa tARL1

DOLl DOL 2

AROZ1C~ -,.

( c )

![image 148](Matrix Analysis of Framed Structures_images/imageFile148.png)

~OJ021

F" 0.1011

-t====]FZ1

tAROl1

(d )

![image 149](Matrix Analysis of Framed Structures_images/imageFile149.png)

F. 0.1012 ~OJOZZ

###### ~Z~ =====+-;;;-r

###### AROZZ( 1

tAR01Z (e) t1

Fig. 2-11. Joint displacements, member end-actions, and support reactions.

the general symbol DJ, and numerical subscripts will be used to identify the individual joint displacements. For example, in the beam of Fig. 2-11a the two joint displacements to be found are the rotations at joints Band C. These displacements will be denoted DJl and DJ2, respectively, and are assumed to be positive when counterclockwise, as shown in the figure.

The member end-actions are the couples and forces that act at the ends of a member when it is considered to be isolated from the remainder of the structure. For the beam under consideration, the end-actions are the bending moments and shearing forces at the ends of the members, as shown in Fig. 2-11b. These end-actions must be evaluated according to a specified sign convention, which may be either a deformation sign convention (related to how the member is deformed) or a statical sign convention (related to the direction of the action in space). The positive directions shown in Fig. 2-11 b are based upon a statical sign convention that upward forces and counterclockwise moments are positive. In general, the endactions are denoted by the symbol AM and are distinguished from one

![image 150](Matrix Analysis of Framed Structures_images/imageFile150.png)

82 Chapter 2 Fundamentals of the Flexibility Method

another by numerical subscripts. In the example ofFig. 2-11 there are eight end-actions. However, it will be assumed arbitrarily that only the four actions labeled AMI, A M2, A M3, and AM4 in Fig. 2-11b are to be calculated. The end-actions AMI and AM2 are the shearing force and bending moment at the right-hand end of member AB, while A M3 and AM4 are the shearing force and bending moment at the left-hand end of member Be. Thus, the first two end-actions are located just to the left ofjoint B, and the last two are located just to the right ofjoint B. In this particular example, the sum ofthe shearing forces AMI and A M3 must be equal to the redundant reaction Ql because there is no vertical load on the beam at joint B. Also, the sum of the bending moments AM2 and AM4 must be equal to the moment M acting as a load at joint B.

Finally, consider the support reactions for the beam in Fig. 2-11a. The two reactions at supports Band C will be determined automatically since they are the redundants Ql and Q2' The remaining reactions, denoted generally by the symbol AR, consist ofa vertical force and a moment at support A. These reactions are labeled ARI and AR2 in Fig. 2-11a and are assumed positive in the directions shown. While the sign convention for reactions may be selected arbitrarily in each particular case, the positive directions shown in the figure will customarily be used in this book.

The principle of superposition provides the means for finding displacements D J, end-actions AM, and reactions AR for the beam in Fig. 2-11a. Previously, this principle was applied to the released structures shown in Figs. 2-11c, 2-11d, and 2-11e in order to obtain an equation for the redundants Q (see Eq. 2-8). In a similar manner, the principle of superposition may be used to obtain the joint displacements DJ in the beam ofFig. 2-11a. In order to accomplish this result, it is necessary to evaluate the displacements in the released structure (Figs. 2-11c, 2-11d, and 2-11e) corresponding to the displacements DJ. In the released structure subjected to the loads, these displacements are denoted by the general symbol DJL and, in particular, the rotations atjoints Band C are labeled D JLJ and D JL2, respectively. Both of these quantities can be found from an analysis of the cantilever beam in Fig. 2-11c.

Next, the released structure subjected to unit values of the redundants must be considered (Figs. 2-11d and 2-11e). The displacements corresponding to DJ are denoted as DJQ, in which the letter Q is used to indicate that these joint displacements are caused by unit values ofthe redundants. Consider, for example, the released structure subjected to a unit value of the redundant Ql (Fig. 2-11d). The joint displacements caused by this load are denoted D JQU and D JQ21, in which the first numerical subscript identifies the particular displacement being considered and the second subscript denotes the redundant which is causing the displacement. In the same manner, joint displacements DJQJ2 and DJQ22 caused by a unit value of Q2 are shown in Fig. 2-11e.

The principle of superposition may now be used to obtain the displacements DJ in the actual beam. Superimposing the displacements from the

![image 151](Matrix Analysis of Framed Structures_images/imageFile151.png)

2.5 Joint Displacements, Member End-Actions, and Support Reactions 83

beams in Figs. 2-1lc, 2-11d, and 2-11e gives the displacements in the beam of Fig. 2-11a:

###### DJ\ = DJLI + DJQIIQI + DJQI2Q2 DJ2 = DJL2 + DJQ21QI + DJQ22Q2

These equations can be expressed in simpler form by the following matrix equation:

###### DJ = DJL + DJQQ

(2-14)

in which the various matrices are

DJL = iDJLlj

###### lnJL2

~JQll

JQ21 DJQ22 Q = [~J

DJQ = DJQ12j

Of course, in a more general situation the matrices may be ofgreater order than in this example. If there are j joint displacements to be obtained, the order of the vectors DJ and DJL will be j x 1. If the number of redundants is q, so that the Q matrix is of order q XI, then the matrix DJQ will be rectangular and oforderj x q. Equation (2-14) can be used to calculate the displacements DJ by matrix operations only, after the matrices DJL, DJQ' and Q have been obtained.

In a manner similar to that used in obtaining Eq. (2-14), the principle of superposition may be used to obtain the member end-actions AM and the reactions AR• In these cases the superposition equations are

AM = AML + AMQQ An = AnL + AnQQ

- (2-15)
- (2-16)


in which AM and An are vectors of member end-actions and reactions in the actual beam (Fig. 2-11a); AML and AnL are vectors of member end-actions and reactions in the released structure due to loads; and AMQ and AnQ are matrices of end-actions and reactions in the released structure due to unit values of the redundants. In the example of Fig. 2-11 the matrices AM and AML are of order 4 X 1 because there are four end-actions being considered; the matrices AR and ARL are of order 2 X 1 because there are two reactions being considered; and the matrices AMQ and ARQ are of order 4 X 2 and 2 X 2, respectively. In the general case in which there are m member endactions, r reactions, and q redundants, the matrices AM and AML are oforder m xl, AMQ is of order m X q, AR and ARL are of order r xl, and ARQ is of order r X q.

From the above discussion it is seen that the steps to be followed in analyzing a structure by the flexibility method include rather extensive analyses ofthe released structure. With the loads on the released structure,

![image 152](Matrix Analysis of Framed Structures_images/imageFile152.png)

84 Chapter 2 Fundamentals of the Flexibility Method

it is necessary to find the actions and displacements that constitute the matrices DQL, DJL, AML, and ARL• With the unit values of the redundants acting on the released structure it is necessary to determine the matrices F,

- DJQ, AMQ, and ARQ• Then Eq. (2-8) is solved first, yielding the vector Q of redundants, after which Eqs. (2-14) through (2-16) can be evaluated for the vectors DJ, AM, and AR• By this means all actions and displacements of interest in the actual structure can be found.

When the effects of temperature changes, prestrains, and support displacements must be taken into account, the only changes in the superposition equations are in the first terms on the right-hand sides of the equal signs. These terms represent the actions and displacements in the released structure and must include the effects of all influences. This situation was described in the preceding section for the displacements corresponding to the redundants, and Eq. (2-12) was derived as a generalized form of Eq. (2-8). Using the same approach, a more general form for Eq. (2-14) becomes the following:

(2-17)

in which the vector DJC represents the combined effects in the released structure and is given by the following expression:

(2-18)

In Eq. (2-18) the matrices D JT, D JP, and DJR represent joint displacements due to temperature changes, prestrains, and restraint displacements, respectively. The restraint displacements that are considered in obtaining

- DJR are those that do not correspond to redundants. Those that do correspond to redundarits are represented in the matrix DQ•


There is no need to generalize Eqs. (2-15) and (2-16) to account for temperature changes, prestrains, and support displacements. None ofthese influences will produce any actions or reactions in a statically determinate released structure; instead, the structure will merely change its configuration to accommodate these effects. Such influences are propagated into the matrices AM and AR through the values of the redundantsQ, which are obtained by solving Eq. (2-12).

In summary, the procedure in any particular example is to analyze the released structure for all causes and then to sum the appropriate matrices,

- as shown in Eqs. (2-11) and (2-18). Then the redundants are found from Eq. (2-13), after which the various actions and displacements may be obtained from Eqs. (2-15), (2-16), and (2-17).


Example. An extended solution for the two-span beam shown in Fig. 2-11 will now be given for the case of loads only. It is assumed that the object of the analysis is to calculate the various joint displacements DJ, member end-actions AM, and reactions AR that are shown in Figs. 2-11a and 2-11b. The beam has constant flexural rigidity EI and is acted upon by the loads PI, M, P2, and P3, which are assumed to have the following values: .

![image 153](Matrix Analysis of Framed Structures_images/imageFile153.png)

###### 2.5 Joint Displacements, Member End-Actions, and Support Reactions 85

###### M = PL P3 = P

When these loads act upon the released structure (Fig. 2-11c), the joint displacements DJI.l and DJLZ are found to be

5PU

DJI.1 = 4EI

Therefore, the vector DJL is

PU [lOJ

DJ!. = 8EI 13

The member end-actions in the beam of Fig. 2-11 c can be found by static equilibrium. For instance, AJILI and A.l1L2 are the shearing force and bending moment just to the left of the point where the couple M is applied. These quantities are equal to

PzL

###### M - -2- + P"L

-Pz + P" and

respectively, or

###### 3PL

A.llLl = 0

A.llL2 = -2-

Similarly, the shearing force and bending moment just to the right of point B in the beam of Fig. 2-llc are

PL

2

Thus, the matrix AM!. is

o

3PL

2

A~IL =

o

-2PL Also, the reactions in the beam of Fig. 2-llc are

###### AHL = [-!~l

2 -1

The joint displacements due to unit values of the redundants are shown in Figs. 2-lld and 2-lle. These displacements can be readily calculated for the released structure and are given in the matrix DJQ:

The member end-actions and reactions in the beams of Figs. 2-11d and 2-11e are found by statics and constitute the matrices AWl and AHQ:

AMQ=[~ -t]

ARtl = -L -I-2LJ

[ -I

o -L

![image 154](Matrix Analysis of Framed Structures_images/imageFile154.png)

86 Chapter 2 Fundamentals of the Flexibility Method

The matrices D(R and F which appear in Eq. (2-8) were determined previously for the beam in Fig. 2-11 (see Art. 2.2) and the vector Q of redundants was found to be

###### P [ 69]

Q = 56 -64

Substitution of this matrix as well as the matrices DJL and DJQ into Eq. (2-14) gives the joint displacements in the actual beam:

PV [17]

DJ = 112EI -5

This result shows that the rotation D,ll at joint B is in the counterclockwise sense and equal to

###### 17PV

###### D,ll = 112EI

while the rotation at joint Cis

and is clockwise, as indicated by the negative sign.

The member end-actions AM and reactions AR are obtained by substituting the appropriate matrices given above into Eqs. (2-15) and (2-16). The results are

###### AM --~56[2~LJ64

P [107]

AR = 56 31L

36L

which can be readily verified by static equilibrium.

2.6 Flexibilities of Prismatic Members. In the examples and problems ofthis chapter, certain flexibility coefficients (such as L3/3E1) for prismatic members have been used frequently. They appear so often because the flexibility coefficients of a structure are calculated from the contributions ofindividual members. Therefore, it is worthwhile to construct member flexibility matrices for prismatic members in various types of framed structures. Such matrices are required in the formalized approach to the flexibility method described in the next section. They can also be inverted to obtain member stiffness matrices (see Sec. 3.5).

It is necessary to define member-oriented axes for an individual member and to distinguish them from structure-oriented axes for the whole structure. (Such axes are also referred to as local coordinates and global coordinates, respectively.) Figures 2-12a through 2-12d show structureand member-oriented axes for various types offramed structures. Each of the figures contains a typical member i that is connected to joints j and k ofthe structure. The axes labeled x. y. and z in each figure represent structure-oriented axes, that is, axes oriented in some convenient manner to the

![image 155](Matrix Analysis of Framed Structures_images/imageFile155.png)

87

- 2.6 Flexibilities of Prismatic Members


y

![image 156](Matrix Analysis of Framed Structures_images/imageFile156.png)

###### I

f'M

###### CD - ---x

![image 157](Matrix Analysis of Framed Structures_images/imageFile157.png)

###### k

(0)

###### y y

![image 158](Matrix Analysis of Framed Structures_images/imageFile158.png)

![image 159](Matrix Analysis of Framed Structures_images/imageFile159.png)

YM7 7

~

x

--- . / 0) / /

rM J /

}---~----~---x

-- ---- --k~

###### XM

(b)

(el

![image 160](Matrix Analysis of Framed Structures_images/imageFile160.png)

Y

\ 0 ~XM

###### /u>!k

###### / I I

###### rM I 7 I 7 x _______-----1(/......':::....,J/II / / /

(d)

Fig. 2-12. Structure- and member-oriented axes for (a) beam member, (b) plane truss or plane frame member, (c) grid member, and (d) space truss or space frame member.

structure as a whole. On the other hand, the axes labeled XM, YM, and ZM are associated with the particular member under consideration and are called member-oriented axes. These axes are assumed to have their origin

- at the j end of the member. The XM axis is aligned with the member axis and is taken positive fromj to k. Axes YM and ZM lie in the principal planes of bending for a member, but this arrangement is not essential for analyzing trusses.


Member flexibility matrices will now be developed for prismatic members that are restrained at theirj ends and free at their k ends, starting with

![image 161](Matrix Analysis of Framed Structures_images/imageFile161.png)

88 Chapter 2 Fundamentals of the Flexibility Method

![image 162](Matrix Analysis of Framed Structures_images/imageFile162.png)

(0)

![image 163](Matrix Analysis of Framed Structures_images/imageFile163.png)

###### (b)

![image 164](Matrix Analysis of Framed Structures_images/imageFile164.png)

(e)

Fig. 2-13. Flexibilities for beam member.

the beam member shown in Fig. 2-13a. In this case the YM axis is chosen so that bending takes place in the xM-YM plane (a principal plane of bending). Two kinds of end-actions are indicated at the k end of the member in Fig. 2-13a: a shearing force AMI (positive in the Y M direction) and a bending moment AM2 (positive in the ZM sense). The flexibility matrix of interest here is a 2 x 2 array relating AMI and AM2 to the corresponding displacements DMI (translation in the YM direction) and DM2 (rotation in the ZM sense). Figures 2-13b and 2-13c show the application of unit loads AMI = 1 and AM2 1 to obtain the terms in the beam flexibility matrix FMi, as follows:

###### FM,-_[FM11 FM12]'-_ 3ElL3 2ElL2j

[

(2-19)

I 2

F F L L

M21 .1122, 2El El

These terms were found previously in the example at the end of Sec. 1.11.

The truss member in Fig. 2-14a has only one end-ac~ion to be considered for the purpose of calculating member flexibilities, namely, the axial

![image 165](Matrix Analysis of Framed Structures_images/imageFile165.png)

- ( a)
- ( b)


Fig. 2-14. Flexibility for truss member.

force AM at the k end of the member (note that a positive value of AM corresponds to a tensile force in the member). The corresponding displacement DM consists of a translation in the xM direction at the k end. Therefore, the single value of FM; for this case is

(2-20)

which is the change in length of the member due to a unit axial load AM = 1 (see Fig. 2-14b). This member flexibility pertains to either a plane truss or a space truss, and it is not influenced by the orientations of axes YM and 2M·

Figure 2-15a shows a plane frame member that is fixed at the j end and free at the k end. As with the beam, the XM-YM plane is defined to be a principal plane of bending. If axial strains are to be neglected, the member flexibility matrix is the same as that for a beam (see Eq. 2-19). However, if axial strains are to be considered, the member flexibility matrix contains the term in Eq. (2-20) as well. Figure 2-15a shows the three member endactions required for this purpose. They are the axial force A.I1J in the XM direction, the shearing force AM2 in the YM direction, and the bending moment A M3 in the 2M sense. Corresponding displacements DMIo DM2, and DM3 consist of translation in the XM direction, translation in the Y M direction, and rotation in the 2M sense. Figures 2-15b, c, and d show the application of unit loads that produce the terms in the following 3 x 3 plane frame member flexibility matrix:

![image 166](Matrix Analysis of Framed Structures_images/imageFile166.png)

90 Chapter 2 Fundamentals of the Flexibility Method

(e) (d)

###### Fig. 2-15. Flexibilities for plane frame member.

L EA

0 0 FMi = FM21 FM22 FM23 0

FMll FM12 FM13

V L2

--3EI (2-21)

2EI L2 L

FM31 FM32 FM33 0

2EI EI

It is seen that this equation is a combination of Eqs. (2-19) and (2-20).

The flexibility matrix for a grid member also can be obtained by augmenting that for a beam, because bending again occurs in the XM-YM plane. Figure 2-16a shows a grid member with a shearing force component AMI (acting in the YM direction), a torsional moment AM2 (acting in the XM

YM AM1

0 t AM2

I

~~ ~

AM3~1;--XM

L

ZM

(0) (b)

~________ ~ __ FM22

(e) (d)

###### Fig. 2-16. Flexibilities for grid member.

![image 167](Matrix Analysis of Framed Structures_images/imageFile167.png)

sense), and a bending moment A M3 (acting in the ZM sense). This sequence for numbering actions follows the rule of taking forces before moments (and corresponding translations before rotations). As illustrated in Figs. 2-16b, c, and d, the terms in the 3 x 3 flexibility matrix for a grid member are found to be

L2

L3

0

FMll FM12 F M13

###### 2EI

3EI

FMi= FM21 F M22 F M23 0 L

0 (2-22)

GJ

L2

0 L

F M31 F M32 F M33

2EI

EI

In this case the first and third actions and displacements are coupled by flexural terms, whereas the second and third were coupled in Eq. (2-21).

To obtain the flexibility matrix for a space frame member, it is necessary to consider three force components and three moment components applied to the k end, as shown in Fig. 2-17a. For this type of member, both the XM-YM plane and the XWZM plane are principal planes of bending. The

###### t __~

~62

-- ~ ~-=rT

1

~

###### ~"H

FM22

(b) (c)

###### -=:::::::::::::Zi/(, ----

1 ~44

###### FM33

~

~

(e) (d) FM53

"~M55 ~~66

###### ----:7JfFM35 @ -====?,~

~

(I) (g)

###### Fig. 2-17. Flexibilities for space frame member.

![image 168](Matrix Analysis of Framed Structures_images/imageFile168.png)

92 Chapter 2 Fundamentals of the Flexibility Method

end-actions in Fig. 2-17a are numbered in the sequence x, y, and z, with forces taken before moments. Elements of the member flexibility matrix appear in Figs. 2-17b through 2-17g. These terms are readily evaluated (see Table A-3 in Appendix A) and placed in a 6 x 6 member flexibility matrix,

- as follows:


L

0 0 0 0 0

EA

###### L3

###### L2

###### 0 --3El 0 0 --

0

z 2Elz

L3 _L2

0 0 -- 0 -- 0 FMi= 3Ely 2Ely

(2-23)

###### L

0 0 0

0 0

GJ

###### _L2 L

0 0 -- 0 0

2Ely Ely

L2

###### L

0 --

0 0 0

2Elz Elz

In this array the symbols ly and lz denote moments of inertia of the cross section of the member about the YM and ZM axes, respectively.

2.7 Formalization of the Flexibility Method. It is possible to assemble the flexibility matrix for a released structure from the flexibility matrices ofindividual members using a formal matrix multiplication procedure. Such a technique is developed in this article from the principle ofcomplementary virtual work (see Sec. 1.14). The reader will find the formalized approach described herein to be both interesting and orderly but not computationally efficient. Therefore, it has not been generally accepted in practice for solving realistic problems. The primary benefits to be gained from studying this material are increased understanding of the flexibility method and preparation for a similar treatment of the stiffness method at the end of the next chapter.

To begin the formulation, recall from the preceding section that the flexibility matrix FMi for an individual member relates the end-displacements DMi to the corresponding end-actions AM;' as follows:

(2-24)

As an arbitrary choice, the member i was taken to be fixed at thej end and free at the k end. Thus, the actions AMi are at the k end ofthe member, and the vector DMi contains the relative displacements ofthe k end with respect to thej end.

Use of the subscript i in Eq. (2-24) means that the relationship pertains only to the i-th member in a given structure. If the equation is repeated for all of the members in a structure, the results can be expressed in the form

![image 169](Matrix Analysis of Framed Structures_images/imageFile169.png)

2.7 Formalization of the Flexibility Method 93

OM! FM! 0 0 0 0 AM! OM2 0 FM2 0 0 0 AM2 OM3 0 0 FM3 0 0 AM3

(2-25)

Ow 0 0 0 FMi 0 AMi OMm 0 0 0 0 FMm AMm

in which the subscript m equals the number of members. Equation (2-25) can be written more concisely as

(2-26)

where the symbol FM represents a diagonal matrix of submatrices FMi. One may think of the matrix FM as the flexibility matrix for the unassembled structure because it merely consists of a collection of member flexibility matrices arranged in a diagonal pattern. For this reason it is given the name unassembledflexibility matrix. The size of F Mdepends upon the number of members and the order of a typical submatrix FMi. For example, ifFMi is of order 3 x 3 (as in a grid), then the order of FM is 3m x 3m. Also note that the vectors AM and OM in Eq. (2-26) contain end-actions AMi and relative end-displacements OMi for all of the members in the structure (see Eq. 2-25).

As the next step, all of the member end-actions in AM will be related to certain structural actions As applied to the released structure. The vector of structural actions As consists of joint loads AJ (listed first) and redundant actions AQ (listed second).* If loads are not applied at the joints, they must be converted to equivalent joint loads (see Sec. 1.12) before this analysis can proceed. When the relationships between AM and As are expressed in matrix form, the result is

(2-27)

The matrix BMS in Eq. (2-27) is an action transformation matrix that relates AM to As for the released structure. The terms in BMS are found by elementary principles of static equilibrium. For this reason it is called the equilibrium (or statics) matrix. Note that the matrix BMS is partitioned into submatrices BMJ and BMQ, which relate AM to AJ and AQ, respectively. Each column in the submatrix BMJ consists of the member end-actions caused by a unit value of a joint load applied to the released structure. For completeness, terms in BMJ are developed for all possible joint loads, regardless of whether such loads actually exist. Similarly, each column in the submatrix BMQ contains member end-actions due to a unit value of a redundant applied to the released structure.

Now suppose that an arbitrary set of virtual loads I)As is applied to the released structure. As with the vector As, let I)As consist of virtual joint

*The symbol AQ, used here to represent redundant actions, has the same meaning as the symbol Q used in previous sections.

![image 170](Matrix Analysis of Framed Structures_images/imageFile170.png)

94 Chapter 2 Fundamentals of the l'lexibility Method

loads I>AJ and virtual redundants I>AQ. Then an expression similar to Eq. (2-27) can be written for the resulting virtual member end-actions I>AM, as follows:

I>AM=BMSI>As=[BMJ BMQ][:!J (2-28)

The equilibrium matrix BMS in this equation is the same as that in Eq. (2-27).

External complementary virtual work I> W* produced by the virtual loads I>As and the actual displacements Ds may be expressed as

###### I>W* = I>A~Ds = [I>AJ I>A~] [gJ (2-29)

where the symbols DJ and DQrepresent actual displacements corresponding to the joint loads and the redundants, respectively. In a similar manner the internal complementary virtual work I>U* generated by the virtual member end-actions I>AM and the actual relative end-displacements DM takes the form

(2-30) By the principle of complementary virtual work, expressions (2-29) and

- (2-30) are equated to obtain (2-31)

Substitution ofEqs. (2-26), (2-27), and (2-28) into the right-hand side of Eq.

- (2-31) yields I>A~Ds = I>A~B~sF MBMSAs (2-32)


Because the virtual loads in BAs are arbitrary, this vector may be cancelled from both sides of Eq. (2-32) to produce

Ds = FsAs (2-33) where

(2-34)

It is seen that the matrix F s relates the displacements Ds to the actions As in Eq. (2-33). This flexibility matrix is formed by the congruence transformation in Eq. (2-34), using the BMsmatrix as the postmultiplier of FM and the transposed matrix B~s as the premultiplier ofFM. By this operation the unassembled flexibility matrix FM is transformed to the assembledflexibility matrix Fs for the whole structure.

In order to examine the assembled flexibility matrix F s in more detail, it will be partitioned into submatrices pertaining to the joint loads AJ, the redundant actions AQ, and their corresponding displacements, DJ and DQ.

![image 171](Matrix Analysis of Framed Structures_images/imageFile171.png)

- 2.7 Formalization of the Flexibility Method 95


This partitioning may be accomplished by writing the expanded form of Eq. (2-33) as

(2-35)

where

FJJ = BlI.)FMBMJ FQJ = BlIQFMBMJ

FJQ = BI1JFMB~IQ FQ<1 = BIIQ F'.1 B~IQ

Note that each of the submatrices FJJ, FJQ, FQJ, and FQQ is formed by a congruence transformation, using as operators B:\lJ and B~IQ (the two parts of B:\18 from Eq. 2-27). Because the submatrix FQQ relates the displacements DQ to the redundant actions AQ, it is recognized to be the same as the flexibility matrix F discussed in previous sections. Other tie-ins with earlier material will be made after the formalized solution is completely set up.

Unknowns in Eq. (2-35) consist of the joint displacements D.) and the redundant actions AQ• Therefore, it becomes advantageous to rewrite Eq.

- (2-35) as two separate matrix equations: DJ = FJJAJ + FJQAQ DQ = FQJAJ + FQQ AQ

Solving the second of these equations for the redundants gives

AQ = FQ~(DQ - FQJAJ)

- (2-36a)
- (2-36b)


(2-37)

which symbolically represents the key that unlocks the whole problem. Once the redundants AQ have been found, they can be substituted into Eq.

- (2-36a) to obtain the joint displacements DJ . In a complete analysis, the other items to be evaluated are the member


end-actions AM and the support reactions AR• Equation (2-27) provides the means for calculating the member end-actions caused by the joint loads and the redundants, using the BMS matrix. It is important to realize, however, that equivalent joint loads may be contained in the vector AJ as well as actual joint loads. Therefore, the member end-actions computed from Eq. (2-27) must be added to initial fixed-end actions to obtain the final values of member end-actions (see Sec. 1.12). This combination of effects can be stated in equation form as

(2-38) where the symbol AMF represents fixed-end actions.

In a similar manner, the support reactions caused by joint loads and redundants may be evaluated with an action transformation operator BRS that relates AR to As, as follows:

(2-39)

![image 172](Matrix Analysis of Framed Structures_images/imageFile172.png)

96 Chapter 2 Fundamentals of the Flexibility Method

In this expression the matrix BRS is partitioned into submatrices BRJ and BRQ, which relate AR to AJ and AQ, respectively. Each column in the submatrix BRJ consists of the support reactions due to a unit value of a joint load applied to the released structure. Similarly, each column in the submatrix BRQ contains reactions caused by a unit value ofa redundant applied to the released structure.

If actual or equivalent joint loads are applied directly to the supports, they must be taken into account by adding their negatives to the support reactions calculated from Eq. (2-39). These effects can be stated as

AR = - ARC + BRJAJ + BRQ AQ (2-40) where the symbol ARC denotes combined loads (actual and equivalent) applied directly to the supports.

Equations of the flexibility method developed by superposition principles in previous articles will now be compared with their counterparts derived by complementary virtual work in this article. The comparable equations for calculating redundants are

Q = F-1(DQ - DQd (2-9) repeated

and

(2-37) repeated

It is seen that Q = AQ, F = FQQ, and DQL = FQJAJ (note the use offlexibility coefficients to obtain DQd.

Comparable equations for determining joint displacements are

(2-14)

repeated

and

(2-36a) repeated

Thus, DJL = FJJAJ and DJQ = FJQ (note the use of flexibility coefficients to obtain DJL).

For the purpose of evaluating member end-actions, the comparable equations are

(2-15)

repeated

and

(2-38) repeated

Therefore, AML = AMF + BMJAJ and AMQ = BMQ. In this instance the steps for obtaining AML as the sum of two parts are clearly evident.

FinaUy, the comparable equations for evaluating support reactions are

###### AR = ARL + ARQQ (2-16)

repeated

and

![image 173](Matrix Analysis of Framed Structures_images/imageFile173.png)

2.7 Formalization of the Flexibility Method 97

(2-40)

repeated

Hence, ARL = -ARC + BRJAJ and ARQ = B RQ• Here the procedure for calculating ARL as the sum of two terms is explicitly shown.

In summary, formalization of the flexibility method leads to the concept of the assembled flexibility matrix Fs for the whole structure. It is partitioned into submatrices associated with joint actions and redundant actions (see Eq. 2-35) and their corresponding displacements. The calculation of redundants and joint displacements by the formalized approach involves more extensive use of flexibility coefficients than before. In addition, the steps for evaluating member end-actions and support reactions become clearly evident. Therefore, one is less likely to make mistakes in analyzing a given structure.

It is implied that all joint displacements, member end-actions, and support reactions are to be calculated as a routine matter. This can be a disadvantage in large problems, where the selectivity inherent in the less formal approach of previous sections may be more appealing. In order to be selective in the formalized version, the analyst may omit columns of the BMS and BRS matrices that correspond to zero values ofactual and equivalent joint loads. However, omitting columns of the BMS matrix precludes the calculation of corresponding joint displacements by Eq. (2-36a) because the required rows of FJJ and FJQ will not be generated. It is also possible to omit rows of the BRS matrix corresponding to support reactions that are not of interest. On the other hand, all rows of the BMS matrix must be retained for the purpose of assembling the structure flexibility matrix from the member flexibility matrices.

Examples will now be given to show how the formalized version of the flexibility method can be applied to various types of framed structures. In each example it is assumed that all joint displacements, member endactions, and support reactions are to be calculated. Only the effects ofloads are considered, but the influences of temperature changes, prestrains, and support displacements can be readily included in the form of equivalent joint loads.

Example 1. The first example involves the analysis of the statically indeterminate truss shown in Fig. 2-18a. The truss has six members, as indicated by the circled numbers in the figure, and all members are assumed to have the same axial rigidity EA. There are two loads acting on the truss atjoint A, and support restraints exist at joints B, C. and D. (The same truss was solved previously as Example 3 of Sec. 2.3.)

In this problem all of the loads on the truss are in the form ofjoint loads; hence, it is not necessary to replace member loads by equivalent loads at the joints. However, if member loads are present, the determination of equivalent joint loads is quite simple. They can be found from the formulas for pinned-end actions for truss members, which are given in Table B-5 of Appendix B. The equivalent loads are in the form of forces only, since there are no bending moments produced at the ends of a truss member.

![image 174](Matrix Analysis of Framed Structures_images/imageFile174.png)

98 Chapter 2 Fundamentals of the Flexibility Method

rA"

B

0

I x

L

(b)

~-------L-------+~ AR3

(a)

(tl

r>?f~Q'=l

###### t~~

###### It It

(g) (h)

Fig. 2-18. Example 1: Plane truss.

The redundant actions Am and AQ2 for the truss are selected as the horizontal reactive force at support B and the axial force in bar AD, respectively. The first of these redundants is assumed to be positive when in the positive x direction, and the second is positive when the member is in tension.

![image 175](Matrix Analysis of Framed Structures_images/imageFile175.png)

###### 2.7 Formalization of the Flexibility Method 99

In addition to finding the redundants, it is assumed in this example that all member end-actions, reactions, and joint displacements are to be determined. The member end-actions are axial forces at the k ends of all the members, as shown in Fig. 2-14a for a typical member. While the member end-actions in general must be taken

- at a designated k end for each member, it can be seen that, in the case of a truss with joint loads only, the end-actions are the same at both ends. Therefore, in this example it is not necessary to designate specifically the end of each member at which the end-action is determined; instead, either end can be used.


The truss has four reactions to be determined; the reactions at joints C and D are denoted ARlo A RZ , and AR:l (see Fig. 2-18a) while the remaining reaction is the redundant Am itself. Also, the four unknown joint displacements (denoted D.J', .... DJ4) are shown in Fig. 2-18b. The reactions and joint displacements are assumed positive when in the positive directions of the x and y axes.

The unassembled flexibility matrix FM (see Eq. 2-25) for this example is

oI 1.4140 00 00 00 00l L 0 0 1.414 0 0 0

[

F,I = EA 0 0 0 1 0 0

- o 0 0 0 1 0
- o 0 0 0 0 I.J


where the diagonal terms are flexibilities of the six members.

Figures 2-18c through 2-18h illustrate the procedure for finding the B\ls and BRS matrices for the released structure. The first of these action transformation arrays consists of member forces due to unit values of AJI through A Q2• From statics it is found to be

0 1 0 0 0 -0.707 0 0 0 0 0 1

HIlS =[B:.lJ B:l1<1J=

1.414 0 0 0 1.414 1

- -I 0 1 0 -I -0.707
- -I 0 0 0 0 -0.707 0 0 0 1 0 -0.707


In accordance with Eq. (2-27), this 6 x 6 matrix BMS is partitioned column-wise into the 6 x 4 submatrix B:lIJ and the 6 x 2 submatrix BM(.J, pertaining to joint loads and redundants, respectively. The first column in BMJ contains member forces caused by the unit load A.J' = 1 shown in Fig. 2-18c. In addition, the member forces listed in the second, third, and fourth columns of BMJ are due to unit values of A.J2, A.J:l> and A.J" respectively (see Figs. 2-18d, e, and fl. Similarly, the first and second columns of the submatrix BM(.J are member forces due to unit values of the redundants A(ll and A (;2 , respectively (see Figs. 2-18g and h).

For later use in calculating reactions, the BRS matrix can also be determined at this stage of the analysis:

o 0

###### 0: 1 ~J

-I : -I

-I 0

0:-1

o -I

This 3 x 6 array BRS is partitioned into the 3 x 4 submatrix BRJ and the 3 x 2

![image 176](Matrix Analysis of Framed Structures_images/imageFile176.png)

100 Chapter 2 Fundamentals of the Flexibility Method

submatrix BRQ, as indicated by Eq. (2-39). Columns of the submatrix BRJ contain support reactions caused by unit values of AJI through AJ4 (see Figs. 2-18c through 0. Also, the columns of BRQ consist of reactions due to unit values of AQI and AQ2 (see Figs. 2-18g and h).

After the above arrays have been found, the remainder of the solution is straightforward. From Eq. (2-34) the assembled flexibility matrix Fs is calculated by matrix mUltiplication as

F S= B~sFMBMS = [FJJ FJQ]

FQJ FQQ

4.828 0 - 1 0 i3.828 3.414

o 1 0 0: 0 -0.707 ---------------------------+--------------1o 00 01 0I:I -I0 -0.707-0.707

L

EA

3.828 0 -I 0: 3.828 2.707 3.414 -0.707 -0.707 -0.707: 2.707 4.828

which is partitioned in accordance with Eq. (2-35). Then the solution for the redundants AQ may be obtained from Eq. (2-37), using a null matrix for DQ, as follows:

- -1 0 [-1]-2 PL
- -0.707 -0.707] g EA


AQ = FQ~(DQ - FQJAJ )

= _ EA [ 0.4328 -0.2426] [3.828 0 L -0.2426 0.3431 3.414 -0.707

= [ 1.I72J P -0.243

These results for the redundants agree with those found earlier in Example 3 of Sec.

2.3.

The next step in the solution consists of finding the joint displacements DJ from Eq. (2-36a):

DJ = F.J,J AJ + FJ(l A Q

=fA[~~28 ~ -? gl[=~lP+E~[3J28

3.414]

- -0.707 [ 1.172] P
- -0.707 -0.243
- -0.707


o 0 o;J ~J 0

= [-~2828J PL +[~:~~~] PL = [=~:g~] PL 1 EA -1 EA 0 EA o 0.172 0.172

Then member end-actions AM (axial forces in this case) are obtained from Eq. (2-38), using a null matrix for AMF, as follows:

AM = AMF + BMJAJ + BMQAQ

###### o o

o o

- -0.707 1 1
- -0.707
- -0.707
- -0.707


100 000 000 010

1.414

1.414

[ 1.172J P

- -1
- -1 o


-0.243

-1

o o

000o 0

![image 177](Matrix Analysis of Framed Structures_images/imageFile177.png)

2.7 Formalization of the Flexibility Method

101

- -2 o
- -1.414 1 1 o


0.172

- -1.828
- -0.243 o o


- -0.243

1.414

- -1 0.172 0.172


p

p=

p+

1.172 0.172

Finally, the support reactions AI< may be calculated with Eq. (2-40). In this instance the matrix Aw is null, and the result is

An = -ARC + BRJAJ + BH"A"

###### [-, 0 0

= -1 -1 0 -M~~] P-+['-: ~l[-0.2431.172]p

1 0 -1

###### =[']3 P+[- Lin]-1.172 P=[-0 172]1.828 P

-1 1.172 0.172

Thus, the complete analysis of the truss, including the determination of all joint displacements, all member end-actions, and all support reactions, has been accomplished by the formalized approach to the flexibility method.

Example 2. The two-span continuous beam shown in Fig. 2-19a is subjected to a uniform load It' (equal to 4P IL) in span AB and two concentrated forces P in span Be. Both members have the same length L, but the flexural rigidity of member AB is twice that of member Be. The objectives of the analysis are to determine end-actions, support reactions, and joint displacements for the beam.

Members AB and BC are denoted as members 1 and 2, respectively; and the k ends of these members are taken as ends Band C, respectively. Thus, the four endactions used in the analysis are the shearing forces and bending moments at the right-hand ends of the members. These end-actions will be numbered sequentially from 1 to 4, and their positive directions are in accordance with the axes shown in the figure (see Fig. 2-13a for the sign convention for end-actions).

The redundant actions are selected as the reactive moment at A and the bending moment at B. Because there is a moment applied as a load at joint B when the actual loads are replaced by combined joint loads, ambiguity will result unless A(J2 is taken a small distance to one side of the joint. Therefore, in this example it is assumed that A{J2 is the bending moment to the right ofjoint B. The released structure associated with this selection of redundants is shown in Fig. 2-19b. Note that both redundants are assumed to be positive whc!n they cause compression on the upper part of the beam.

The reactive forces in the y direction at the supports, as well as the two joint displacements (rotations at B and C), are identified in Fig. 2-19c. A fourth reactive action is the couple at support A, but since this reaction is chosen as one of the redundants it is not necessary to include it in the vector AR•

The determination of the combined joint loads is illustrated in Fig. 2-19d, which shows the two fixed-end beams obtained by restraining the joints against displacements. The negatives of the fixed-end actions for these beams constitute the equivalent joint loads. Then, the equivalent loads are added to any actual joint loads

![image 178](Matrix Analysis of Framed Structures_images/imageFile178.png)

102 Chapter 2 Fundamentals of the Flexibility Method

A02

~~ ~C

(b)

###### ,-foilAB d"2k¥C

tAR2 tAR3

(e)

###### 4P

;LC~( CijT, , ,Bt~)Pi 2PL(~B9 ( ( C~~PL

###### 2P 2P tp pt -9

(d)

~A ':P.'i :P:~

2P~

)~L

(e)

#### ~t+ ~t+ • 4 t+ ~ft

###### AJI =1 AJ2 =1

r---.

~

~

(f) (g)

A02 = f

###### 4, 4t ~ 4- ¥ ~

A01 =1

~

f+ t+ t+ t~ t+

(h) (I)

###### Fig. 2-19. Example 2: Continuous beam.

![image 179](Matrix Analysis of Framed Structures_images/imageFile179.png)

2.7 Formalization of the Flexibility Method 103

(none in this example) to obtain the combined joint loads, which are shown in Fig. 2-1ge.

The flexibility matrices for the individual members can be found readily (see Eq.2-19):

###### L [4U 6L] FM2 = 2FMl = 12El 6L 12

and, therefore, the unassembled flexibility matrix FM is

oo 00 1

2U 3L FM = 12EI 0 0

L [ 3L 6

4L2 6L o 0 6L 12

- as given by Eq. (2-25). The BMS and BRS matrices for this example are found by analyzing the released


structure subjected to the conditions A.1l = 1 through AQ2 = 1 shown in Figs. 2-19f through 2-19i. From the member end-actions due to these unit loads, the 4 x 4 matrix B~IS is found to be

BM(J]=t[-~ J!g -t]

o L:O 0

Similarly, the support reactions shown in Figs. 2-l9fthrough 2-19i are listed in the 3 x 4 matrix BRS, as follows:

###### o :-1 1]

1 : 1 -2 -1 : 0 1

BRS = [BRJ

From Eq. (2-34) the assembled flexibility matrix Fs is found to be

F.Ja] _ ~ [t_~l~_J]

Faa - 12EI 1 0 I 2 1 2 2: \ 6

With this matrix available, the solution for the redundants may be carried out, using a null matrix for DQ in Eq. (2-37):

Then the joint displacements DJ can be determined from Eq. (2-36a), as follows:

###### 2] [ 0] PL

2 -\ 9

Next, the member end-actions A~l are calculated with Eq. (2-38). In this example the nonzero fixed-end actions in the vector A~lF are drawn from Fig. 2-19d. Thus,

![image 180](Matrix Analysis of Framed Structures_images/imageFile180.png)

[-;~]f ![-l g][IJPL ![6 -l][ 0]

PL

9

9 9+L 0-1 2 9+LO I -I

-2L 0 L 0 0

[-;~lf [-l]f [-l]~-[-2]~

9 9 + -2 9 + -I 9 2 3

-2L 2L 0 0

Similarly, the support reactions AR can be found with Eq. (2-40), using nonzero reactions in the vector ARC drawn from Fig. 2-1ge:

AR = - ARC + BRJAJ + BRQAQ

~tl]P+±[-U]Ul~L+±[-H] [-~l ~L ~ [i~] ~+UJ~+ [~;1~ ~m';

The redundants ~ calculated above pertain to the beam with combined joint loads (see Fig. 2-1ge). However, these redundants are actually member end-actions; so their final values must account for initial fixed-end actions, as in Eq. (2-38).Thus,

###### (AQ)filiul = AQF +AQ = [=~J ~L + [-~J ~L = [=G ~L

where the fixed-end actions in AQF are obtained from Fig. 2-19d.

Example 3. The plane frame shown in Fig. 2-20a has constant EI for all members and is subjected to two concentrated forces. Only flexural effects are to be considered in the analysis, and the reactive force in the x direction at support D is chosen as the redundant action.

The j ends of members I, 2, and 3 are selected arbitrarily as points A, B, and D, respectively. In accordance with this selection, the member end-actions at the k ends are the shearing forces and bending moments shown in Fig. 2-20b.

The joint displacements for the frame are also shown in Fig. 2-20b. They consist of the rotation at joint A, the translation and rotation at B, the rotation at C, and the rotation at D. Because axial deformations are neglected in this example, there is only one independent joint translation (DJ2). The reactions for the frame also are identified in Fig. 2-20b; only three reactions need to be considered, inasmuch as the fourth reaction is the redundant AQ•

The equivalent joint loads are found by restraining all joints of the structure, calculating the fixed-end actions caused by the member loads, and then reversing their directions. In this example the only member load is the force P acting on member BC; thus, when joints Band C are restrained, the fixed-end actions are those shown in Fig. 2-20c. The negatives of these fixed-end actions are added to the actual joint loads to give the combined loads shown in Fig. 2-20d.

The member flexibility matrices are obtained by applying Eq. (2-19) to each member of the frame:

![image 181](Matrix Analysis of Framed Structures_images/imageFile181.png)

###### 2.7 Formalization of the Flexibility Method

lOS

p

###### ®

###### A ---x

(b)

(0)

20PI)4PL

###### 3f!:.( 7P

27 t 27

27 27

,,--:-

2"

(e)

(d)

###### ft

f-z

(0

(el

###### f±

(gl

(h)

(,)

Fig. 2·20. Example 3: Plane frame (flexural effects only).

![image 182](Matrix Analysis of Framed Structures_images/imageFile182.png)

Then the unassembled flexibility matrix FM is formed by placing the above matrices on the principal diagonal (see Eq. 2-25). Inasmuch as H = Ll2, this matrix becomes

U 3L 0 0 0 0 3L 12 0 0 0 0

L 0 0 8£2 12L 0 0 - 24£1 0 0 12L 24 0 0

FM

0 0 0 0 L2 3L 0 0 0 0 3L 12

Figures 2-20e through 2-20j depict the analyses required to fill the BMS and BRS matrices for this example, When the released structure is analyzed for member endactions due to these six unit-load cases, the 6 x 6 matrix BMS becomes

0 -2L 0 0 0 :-2L

-2L L2 0 0 0

P

I

I

BMS = [BM.) BMQ] = 2~ -2 L -2 -2 -2

I 0 0 0 0 2L 2L

I

I L2

I

0 0 0 0 0

###### 2L

I

###### I

0 0 0 0 -2L :-£2 In addition, the support reactions for these six cases constitute the 3 x

6 matrix

BRS:

BRS = [BRJ -2L 0 0 o :~ll

I [ 0

BRQ] = 2L 2 -L 2 2 2: 0

-2 L -2 -2 -2: 0 The assembled flexibility matrix Fs, calculated from Eq. (2-34), is

Fs = B~sFMBMS = [;~~ ~~:]

20 -7L 8 -4 -4 -9L

-7L 3£2 -4L 2L 2L 4£2 L 8 -4L 8 -4 -4 -6L

24£1 -4 2L -4 8 8 6L

- -:1_____f~___.:-::.4. ____11____fQ _-' __J!--_
- -9L 4U -6L 6L 9L: 8£2


In this case there is only one redundant, and its solution from Eq. (2-37) is

AQ = FQ"b(DQ - FQJAJ)

###### = _ 3£1 [-9L 4£2 -6L

L'l

###### 5P

12

Next, the joint displacements DJ are determined using Eq. (2-36a), as follows:

![image 183](Matrix Analysis of Framed Structures_images/imageFile183.png)

Problems 107

For this purpose, the fixed-end actions in A~IF are drawn from Fig. 2-20c. Finally, Eq. (240) gives the support reactions as

###### °2 °2

###### ~] _2;L !... + [-~] (_5P)

###### r°°J

-2 4L 24 ° 12

-2 -2

[0] P [-54] P [45] P [-I]p

= ~~ 108 + - ~~ 108 + ~ 108 = ~ T2

where the terms in the vector ARc are obtained from Fig. 2-20d. In this case the

equivalentjointload - 20PI27 at point B is transmitted directly to the supportat point A. Similady, the equivalent joint load -7PI27 at point C is transmitted directly to the support at point D.

###### Problems

###### The problems for Sec. 2.3 are to be solved by the flexibility method using Eq. (2-9). In each problem the redundant actions are to be obtained, unless stated otherwise.

2.3-1. Determine the reactive moments at each end of the fixed-end beam

![image 184](Matrix Analysis of Framed Structures_images/imageFile184.png)

108 Chapter 2 Fundamentals of the Flexibility Method shown in Fig. 2-3a, due to the force P and moment M acting at the middle of the span. The beam has constant flexural rigidity EI and length L. Select the reactive moments themselves as the redundant actions, and assume these moments are positive when they produce compression on the bottom of the beam. Take the first redundant at end A of the beam and the second at end B.

- 2.3-2. Analyze the two-span beam shown in Fig. 2-2a by taking the reactive moment at support A and the bending moment just to the left of support B as the redundants QI and Q2, respectively. Assume that these moments are positive when they produce compression on the top of the beam. Also, assume that the loads on the beam are PI = 2P, M = PL, P2 = P, P3 = P, and the flexural rigidity EI is constant.
- 2.3-3. Analyze the two-span beam of Fig. 2-2a if support B is displaced downward by a small distance s. Select the redundants to be the vertical reactions at supports Band e, as shown in Fig. 2-2a, and omit the effects of the loads in the analysis. Assume that EI is constant for both spans.
- 2.3-4. Find the redundant actions for the two-span beam of Fig. 2-2a using the released structure shown in Fig. 2-2b. Assume that EI is constant for the beam and that the loads are PI = P, M = 0, P2 = P, P3 = P. Number the redundants from left to right along the beam; also, assume that the redundant moment is positive when counterclockwise, and that the redundant force is positive when upward.
- 2.3-5. Determine the bending moments at supports Band e of the continuous beam shown in the figure, using these moments as the redundants QI and Q2, respectively. Assume that the redundants are positive when they produce compression on the top of the beam. The beam has constant flexural rigidity EI.


~ A AI) ~17c~ ~ ~ 110

###### I--L-----+-L ·1· 1.5L-----.J

Prob. 2.3-5.

2.3-6. Find the bending moments at supports Band e of the continuous beam (see figure), using these moments as the redundants QI and Q2, respectively. Assume that QI and Q2 are positive when they produce compression on the top of the beam. The flexural rigidity of the beam is EI.

###### lLA6

###### *18

W

~c

###### ~L +

Prob. 2.3-6.

2.3-7. Analyze the plane truss shown in Fig. 2-5a by taking the forces in the two diagonal members AD and Be as the redundants QI and Q2' respectively. Assume that tension in a member is positive, and assume that there are no support displacements. All members have the same axial rigidity EA.

![image 185](Matrix Analysis of Framed Structures_images/imageFile185.png)

- 2.3-8. Solve the preceding problem using the force in member AD and the reaction at D as the redundants Ql and Q2' respectively.
- 2.3-9. For the plane truss in the figure, find the redundant member forces QI and Q2' Assume that the cross-sectional area of member AB is O.6A, that for AD is O.8A, and those for AC and AE are equal to A.


r

1

O.8L

~

###### !.---O.6L --++--O.6L----1

Prob. 2.3-9.

2.3-10. Find the forces in the members AE and CE of the truss shown in the figure by taking these member forces as the redundants QI and Q2, respectively. The axial rigidity for the vertical and horizontal members is EA and for the diagonal members is 2EA.

p p

p B

"2

Prob.2.3-10.

2.3-11. Find the forces in the members AB and BC of the truss in the figure, using these forces as the redundants QI and Q2' respectively. Let H = 3L14 and PI

= P2 = P, and assume that all members have the same axial rigidity EA.

Prob. 2.3-11.

![image 186](Matrix Analysis of Framed Structures_images/imageFile186.png)

110 Chapter 2 Fundamentals of the Flexibility Method

- 2.3-12. Calculate the redundant reactions Q, and Q2 at the pinned support (point

C) of the plane frame in the figure, omitting axial deformations. Let EI be constant.

Prob.2.3·12

- 2.3-13. Determine the redundant moments Q, = M8 (internal moment at B)


- and Q2 = Me (internal moment at C) for the plane frame shown in the figure. Neglect axial deformations of members in the analysis, and assume that EI is constant.


r-fF-----H-~c

Prob.2.3-13

2.3-14. Find the redundant reactions Q, and Q2 at the pinned support (point D) of the plane frame in the figure, disregarding axial deformations. Assume that EI is constant for all members.

Prob. 2.3-14

2.3-15. Analyze the plane frame shown in Fig. 2-6a due to a uniform load of intensity w acting downward on member AB. Omit the load P from the analysis, and let H = L. Use the redundants Q" Q2, and Q3 shown in Fig. 2-6b, and consider only the effects of flexural deformations.

![image 187](Matrix Analysis of Framed Structures_images/imageFile187.png)

- 2.3-16. Obtain the flexibility matrix F for the plane frame in Fig. 2-6a, corresponding to the redundants shown in Fig. 2-6b, by considering flexural, axial, and shearing deformations. Both members have flexural rigidity EI, axial rigidity EA, and shearing rigidity GAlf(see Sec. A.I).
- 2.3-17. For the plane frame shown in the figure, find the flexibility matrix F for the following conditions: (a) considering flexural deformations only and (b) considering flexural, axial, and shearing deformations. Select the redundants Q"


Q2, and Q3 as the axial force, shearing force, and bending moment, respectively, at the midpoint of member Be. Take these quantities as positive when in the same directions as the actions Q" Q2, and Q3 shown in Fig. 2-6b. Assume that all members of the frame have flexural rigidity EI, axial rigidity EA, and shearing rigidity GAIf.

2.3-18. Obtain the flexibility matrix F for the plane frame in the preceding problem if the redundants Q" Q2, and Q3 are the horizontal force (positive to the right), vertical force (positive upward), and moment (positive when counterclockwise), respectively, at support D. Consider only the effects of flexural deformations and assume that each member has constant EI.

J Ii

B C

I. 2L~

Prob. 2.3-17 and Prob. 2.3-18.

2.3-19. Find the redundants Q, and Q2 for the plane frame shown in the figure, considering only flexural deformations. The flexural rigidity EI is the same for all members.

P

B C

~L/2+L/2 L----1 ~L

1

###### +°2

Prob. 2.3-19.

2.3-20. Find the reactions at the support D of the plane frame shown in the figure by taking those reactions as the redundants. Assume that Q, is the horizontal

p

i L/

3

B r--'---------.. C

~-.-

I H

A

D~~

~~L-----;

Prob. 2.3-20.

![image 188](Matrix Analysis of Framed Structures_images/imageFile188.png)

112 Chapter 2 Fundamentals of the Flexibility Method

reaction (positive to the right) and Q2 is the vertical reaction (positive upward). Consider only the effects of flexural defonnations in the analysis. Let H = Ll3; and assume that the flexural rigidity of member BC is 2EI, whereas that for members AB and CD is EI.

2.3-21. Obtain the flexibility matrix F for the grid shown in Fig. 2-7a, considering both flexural and torsional defonnations, if the reactions at support C are taken

- as the redundants. Assume that QI is the force in the positive y direction, Q2 is the positive moment about the x axis, and Q3 is the positive moment about the z axis. The flexural and torsional rigidities of the members are EI and GJ, respectively.

2.3-22. Calculate the redundant reaction Q at support D for the horizontal grid shown in the figure. The grid is constructed of three members (AB, BC, and CD) that are rigidly joined at right angles and supported by simple supports at A, B, C, and D. Each member has flexural rigidity EI, torsional rigidity GJ, and length L. Assume that the loads P act at the midpoints of members AB and Be.

Prob. 2.3-22.

2.3-23. Detennine the redundant moments QI and Q2 at support D of the grid shown in the figure. The supports at A and C are simple supports, and the support

- at D is a fixed support. The members of the grid are rigidly connected at joint B; also, members AB, BC, and BD each have flexural rigidity EI and torsional rigidity GJ (where GJ = EI). The load P acts at the midpoint of member BC, and LI Ll2.


A

A

###### I--L

Prob. 2.3-23.

2.3-24. The grid in the figure has no moment-torque interactions where the beams cross each other. Calculate the interacting tensile forces QI and Q2 due to the unifonnly distributed load w. For this purpose, assume that the x-beam crosses over the two z-beams and that EI is constant for all members.

![image 189](Matrix Analysis of Framed Structures_images/imageFile189.png)

###### Problems

113

y

7

L

)',( x

L

/

Prob. 2.3-24.

2.3-25. The space frame ABeD has pin supports at A, e, and D; thus, each support is capable of resisting a force in any direction, but is not capable of transmitting a moment. The members are rigidly connected at joint B. Each member of the frame is of tubular cross section with length L, flexural rigidity EI, and axial rigidity EA. The effects of both flexural and axial deformations are to be considered. Obtain in literal form the flexibility matrix F, assuming that the redundants QI, Q2,

- and Q3 are the reactions at D in the x direction, at e in the x direction, and at e in


the z direction, respectively, as shown in the figure.

A

Prob. 2.3-25.

2.3-26. Determine the matrices DQL and F for the space frame shown in the figure, considering flexural and torsional deformations. The load on the frame is a

y p

'-+------,1 ---x

z

L

Prob. 2.3-26.

![image 190](Matrix Analysis of Framed Structures_images/imageFile190.png)

114 Chapter 2 Fundamentals of the Flexibility Method vertical force P acting at joint B. The frame has a fixed support at A and a pin support

- at D, and the members are rigidly connected at right angles to one another at joints Band C. The redundants are selected as the reactions at joint D, as shown in the figure. Each member of the frame has flexural rigidity EI and torsional rigidity GJ.


- 2.4-1. Find the redundant reactions Q\ and Qz at support B of the fixed-end beam shown in Fig. 2-3a, assuming that the beam is subjected to a temperature differential such that the top of the beam has a temperature change d Tz and the bottom of the beam has a change d T\. The coefficient of thermal expansion for the material is a, the depth of the beam is d, and the flexural rigidity is EI. Omit the effects of the loads in the analysis.
- 2.4-2. Obtain the matrix DQT for the continuous beam shown in Fig. 2-4a, assuming that members BC and CD are heated to a temperature change d T\ on the lower surface, while the upper surface has a temperature change d Tz. Let a denote the coefficient of thermal expansion, and let d denote the depth of the beam. (Use


- the redundants Q\ and Q2 shown in Fig. 2-4b.)

- 2.4-3. The prismatic beam member in the figure has constant initial curvature cf>\ in the left-hand half and -cf>\ in the right-hand half. Determine the fixed-end actions at point B [Q\ = shearing force (positive upward) and Qz = bending moment (positive counter-clockwise)] required for zero displacements at that point.
- 2.4-4. Obtain the matrix DQT for the plane truss shown in Fig. 2-5a, assuming that the entire truss has its temperature increased uniformly by an amount d T. Use


- the redundants Q\ and Q2 shown in Fig. 2-5b, and let a denote the coefficient of thermal expansion.


2.4-5. Find the redundant reactions Q\ and Q2 at support B of the fixed-end

- beam shown in Fig. 2-3a, assuming that the beam is constructed initially of two straight segments rigidly joined together but slightly out of alignment (see figure). The angle between the two halves of the beam is (3, and the flexural rigidity of the beam is EI. Do not include the effects of the loads in the analysis.


I---L/2--j'>fool~f---L/2---1

Prob.2.4-5

2.4-6. Obtain the matrix DQP for the plane truss shown in Fig. 2-5a assuming that members AB and CD are constructed with lengths L + e instead ofL. Take the redundants Q\ and Q2 as shown in Fig. 2-5b.

![image 191](Matrix Analysis of Framed Structures_images/imageFile191.png)

Problems 115

- 2.4-7. Suppose that members AB and Be of the truss in Prob. 2.3-10 are fabricated too short by the amounts - e and - 2e. Find the matrix DQP' using the same redundants QI and Q2 as before.
- 2.4-8. Find the redundant reactions QI and Q2 at support B of the fixed-end


- beam shown in Fig. 2-3a, assuming that support A rotates {3 radians in the clockwise direction and support B is displaced downward by a distance s. The flexural rigidity of the beam is EI. Omit the effects of the loads in the analysis.

- 2.4-9. Obtain the matrix DOR for the plane truss of Fig. 2-5a if support e is displaced downward a distance s. Use the redundants QI and Q2 shown in Fig.

- 2-5b.


- 2.4-10. Find the matrix DQR for the continuous beam shown in Fig. 2-4a if support B is displaced downward a distance Sl and support eis displaced downward a distance S2' The redundants QI and Q2 are to be taken as shown in Fig. 2-4b.
- 2.4-11. The plane frame in the figure is fabricated with the angle of 7r/2 at point B made too large by the amount Ms. Omitting axial strains in the prismatic members, find the redundant reactions QI and Q2 at point eafter the frame is forced into place.


A~-----,------~

Prob. 2.4-11.

EI

..........-

0,

2-4.12. Obtain the matrix Doc, representing the combined effects in the released structure, for the plane frame shown in Fig. 2-6a if, in addition to the load P, the frame has its temperature increased uniformly by an amount Ll T, support A is displaced downward by an amount s, and support C rotates clockwise by an amount {3. The members of the frame have flexural rigidity EI and coefficient of thermal expansion ex. Take the redundants QI' Q2, and Q3 as shown in Fig. 2-6b.

Problems 2.5-1 to 2.5-3 are to be solved using Eqs. (2-14), (2-15), and (2-16). AsslIme that reactions and joint displacements are positive to the right, upward, and counterclockwise.

2.5-1. Find the joint displacements and support reactions for the continuous

- beam shown in Fig. 2-4a, assuming that the intensity w of the distributed load is such that wL = P. The beam has constant flexural rigidity EI. The four joint displacements and four reactions are to be numbered consecutively from left to right in the figure. Use the solution given in Example 2, Sec. 2.3, for the redundants.


![image 192](Matrix Analysis of Framed Structures_images/imageFile192.png)

116 Chapter 2 Fundamentals of the Flexibility Method

2.5-2. For the plane truss shown in Fig. 2-5a, obtain the horizontal and vertical displacements ofjoint A, the forces in members AB, AC, and BD, and the horizontal and vertical reactions at support C. Assume that there are no support displacements, and consider only the effects of the loads in the analysis. Assume that all members have axial rigidity EA and that tension in a member is positive. Number the displacements, member forces, and reactions in the order stated above. Use the solution given in Example 3, Sec. 2.3, for the redundants.

- 2.5-3. For the plane frame in Fig. 2-6a, obtain the displacements of joint B


(translations in the horizontal and vertical directions, and rotation) and the reactions at support C. Consider only flexural deformations in the analysis, and use the results of Example 4, Sec. 2.3, in the solution.

![image 193](Matrix Analysis of Framed Structures_images/imageFile193.png)

###### 3Fundamentals of theStiffness Method

3.1 Introduction. The stiffness method (also known as the displacernent method) is the primary method used in matrix analysis of structures. One of its advantages over the flexibility method is that it is conducive to computer programming. Once the analytical model of a structure has been defined, no further engineering decisions are required in the stiffness method in order to carry out the analysis. In this respect it differs from the flexibility method, although the two approaches have similar mathematical forms. In the flexibility method the unknown quantities are redundant actions that must be arbitrarily chosen; but in the stiffness method the unknowns are the joint displacements in the structure, which are automatically specified. Thus, in the stiffness method the number of unknowns to be calculated is the same as the degree of kinematic indeterminacy of the structure.

In this chapter the stiffness method is developed on the basis of writing joint equilibrium equations in terms of stiffness coefficients and unknown joint displacements. A kinematically determinate version of the original structure (with the joint displacements restrained) proves to be useful for the purpose of characterizing such equilibrium conditions as action superposition equations. Because the stiffness method requires extensive use of restraint actions due to various causes, the material in Appendix B will be quite helpful. As in the preceding chapter, the effects of temperature changes, prestrains, and support displacements are considered as well as the effects of loads; and procedures for calculating member end-actions and support reactions are also developed. After the basic concepts of the stiffness method have been thoroughly discussed, the method is formalized into a procedure for assembling the overall stiffness matrix ofthe structure from individual member stiffness matrices. This approach will be further systematized (and simplified) in Chapter 4 as preparation for programming on a digital computer.

3.2 Stiffness Method. In order to illustrate the concepts of the stiffness method in their simplest form, consider the analysis of the beam in

- Fig. 3-1a. This beam has a fixed support at A and a roller support at B; and it is subjected to a uniform load of intensity w. The beam is kinematically indeterminate to the first degree (if axial deformations are neglected) because the only unknown joint displacement is the rotation ()B at joint B.


117

![image 194](Matrix Analysis of Framed Structures_images/imageFile194.png)

The first phase of the analysis is to determine this rotation. Then the various actions and displacements throughout the beam can be determined, as will be shown later.

In the flexibility method a statically determinate released structure is obtained by altering the actual structure in such a manner that the selected redundant actions are zero. The analogous operation in the stiffness method is to obtain a kinematically determinate structure by altering the actual structure in such a manner that all unknown displacements are zero. Since the unknown displacements are the translations and rotations of the joints, they can be made equal to zero by restraining the joints of the structure against displacements of any kind. The structure obtained by restraining all joints of the actual structure is called the restrained structure. For the beam in Fig. 3-1a the restrained structure is obtained by restraining joint B against rotation. Thus, the restrained structure is the fixed-end

- beam shown in Fig. 3-1b. When the loads act on the restrained beam (see Fig. 3-1b), there will be


a couple MB developed at support B. This reactive couple is in the clockwise direction and is given by the expression

WL2

M B =--

(3-1)

12

tIIJ5T1i59*

###### Rf--L 88 ·1

(0 )

(e)

Fig. 3-1. Illustration of stiffness method.

![image 195](Matrix Analysis of Framed Structures_images/imageFile195.png)

which can be found from the table offixed-end moments given in Appendix

- B (see Table B-l). Note that the couple MB is an action corresponding to the rotation 8B, which is the unknown quantity in the analysis. Because there is no couple at joint B in the actual beam of Fig. 3-1a, it is necessary to consider next that the restrained beam is sUbjected to a couple equal and opposite to the couple M B' Such a couple is shown acting on the beam in


- Fig. 3-1c. When the actions acting on the two beams in (b) and (c) are superimposed, they produce the actions on the actual beam. Thus, the analysis of the beam in Fig. 3-1a can be considered as the superposition of the analyses shown in Figs. 3-1b and 3-1c. It follows, therefore, that the rotation produced by the couple M B in Fig. 3-1 c is equal to 8B, the unknown rotation in the actual beam.


The relation between the moment MB and the rotation 8B in the beam of Fig. 3-1c is

(3-2)

in which E1 is the flexural rigidity of the beam. Equation (3-2) is obtained from Case 3 of Table B-4. Equating the two expressions for the moment MB from Eqs. (3-1) and (3-2) gives the equation

wV 4E1 12=L 8B

from which

wL3

8 ---

###### B - 48E1

Thus, the rotation at joint B of the beam has been determined.

In a manner analogous to that used in the flexibility method, it is convenient in the above example to consider the restrained structure under the effect of a unit value of the unknown rotation. It is also more systematic to formulate the equation for the rotation as an equation of superposition and to use a consistent sign convention for all terms in the equation. This procedure will now be followed for the beam in Fig. 3-1.

The effect of a unit value of the unknown rotation is shown in Fig. 3-1d, where the restrained beam is acted upon by a couple mB that produces a unit value of the rotation 8B at the right-hand end. Since the moment mB is an action corresponding to the rotation 8B and caused by a unit value of that rotation (while all other joint displacements are zero), it is recognized that mB is a stiffness coefficient for the restrained structure (see Sec. 1.10). The value of the couple mB (see Eq. 3-2) is

4EI mB=L

![image 196](Matrix Analysis of Framed Structures_images/imageFile196.png)

In formulating the equation of superposition the couples at joint B will be superimposed as follows. The couple in the restrained beam subjected to the load (Fig. 3-1b) will be added to the couple mB (corresponding to a unit value of 0B) multiplied by 0B itself. The sum of these two terms must give the couple at joint B in the actual beam, which is zero in this example. All terms in the superposition equation will be expressed in the same sign convention, namely, that couples and rotations at joint B are positive when counterclockwise. According to this convention, the couple MB in the beam of Fig. 3-1 b is negative:

WL2

12

The equation for the superposition of moments at support B now becomes

(3-3) or

WL2 4El

--- +-OB = 0

###### 12 L

Solving this equation yields

which is the same result as before. The positive sign for the result means that the rotation is counterclockwise.

The most essential part of the preceding solution consists of writing the action superposition equation (3-3), which expresses the fact that the moment at B in the actual beam is zero. Included in this equation are the moment caused by the loads on the restrained structure and the moment caused by rotating the end B of the restrained structure. The latter term in the equation was expressed conveniently as the product of the moment caused by a unit value of the unknown displacement (stiffness coefficient) times the unknown displacement itself. The two effects are summed algebraically, using the same sign convention for all terms in the equation. When the equation is solved for the unknown displacement, the sign of the result will give the true direction of the displacement. The equation may be referred to either as an equation ofaction superposition or as an equation ofjoint equilibrium. The latter name is used because the equation may be considered to express the equilibrium of moments at joint B.

Having obtained the unknown rotation 0B for the beam, it is now possible to calculate other quantities, such as member end-actions and reactions. As an example, assume that the reactive force R acting at support A of the beam (Fig. 3-1a) is to be found. This force is the sum of the corre-

![image 197](Matrix Analysis of Framed Structures_images/imageFile197.png)

sponding reactive force RA at support A in Fig. 3-1b and (JB times the force rAin Fig. 3-1d, as shown in the following superposition equation:

The forces RA and rAcan be readily calculated for the restrained beam (see Case 6, Table B-1, and Case 3, Table B-4).

###### RA=T ,.A --- L2

lI'L 6El

When these values, as well as the previously found value for (JR. are substituted into the equation above, the result is

511'L

###### R=--

8

The same concepts can be used to calculate any other actions or displacements for the beam. However, in all cases the unknownjoint displacements must be found first.

If a structure is kinematically indeterminate to more than one degree, a more organized approach to the solution, as well as a generalized notation, must be introduced. For this purpose, the same two-span beam used previously as an example in the flexibility method will be analyzed now by the stiffness method (see Fig. 3-2a). The beam has constant flexural rigidity El and is subjected to the loads PI, M, Pz, and P3• Since rotations can occur atjoints Band C, the structure is kinematically indeterminate to the second degree when axial deformations are neglected. Let the unknown rotations at these joints be DI and D2, respectively, and assume that counterclockwise rotations are positive. These unknown displacements may be determined by solving equations of superposition for the actions at joints Band

- C, as described in the following discussion. The first step in the analysis consists of applying imaginary restraints at


the joints to prevent all joint displacements. The restrained structure which is obtained by this means is shown in Fig. 3-2b and consists of two fixedend beams. The restrained structure is assumed to be acted upon by all of the loads except those that correspond to the unknown displacements. Thus, only the loads PI' Pz, and P3 are shown in Fig. 3-2b. All loads that correspond to the unknown joint displacements, such as the couple M in this example, are taken into account later. The moments ADLl and ADL2 (Fig. 3-2b) are the actions of the restraints (against the restrained structure) corresponding to DI and D2, respectively, and caused by loads acting on the structure. For example, the restraint action ADLl is the sum of the reactive moment at B due to the load PI acting on member AB and the reactive moment at B due to the load P2 acting on member Be. These actions can

![image 198](Matrix Analysis of Framed Structures_images/imageFile198.png)

122 Chapter 3 Fundamentals of the Stiffness Method

![image 199](Matrix Analysis of Framed Structures_images/imageFile199.png)

(0)

![image 200](Matrix Analysis of Framed Structures_images/imageFile200.png)

~e==

~ADL'

(b)

S,'{'\ S2'~

![image 201](Matrix Analysis of Framed Structures_images/imageFile201.png)

1r;\=e C~

###### t

(e)

S'2{,\. S22r7\

![image 202](Matrix Analysis of Framed Structures_images/imageFile202.png)

###### ~e 1~

~A

(d)

Fig. 3-2. Illustration of stiffness method.

be found with the aid of formulas for fixed-end moments in beams (see Appendix B), as illustrated later.

In order to generate the stiffness coefficients at joints Band C, unit values of the unknown displacements DI and D2 are induced separately in the restrained structure. A unit displacement corresponding to DI consists of a unit rotation of joint B, as shown in Fig. 3-2c. The displacement D2 remains equal to zero in this beam. Thus, the actions corresponding to DI and D2 are the stiffness coefficients Sl1 and S21, respectively. These stiffnesses consist of the couples exerted by the restraints on the beam atjoints Band C, respectively. The calculation ofthese actions is not difficult when formulas for fixed-end moments in beams are available. Their determination in this example will be described later. The condition that D2 is equal to unity while DI is equal to zero is shown in Fig. 3-2d. In the figure the stiffness S12 is the action corresponding to DI while the stiffness S22 is the action corresponding to D2• Note that in each case the stiffness coefficient is the action that the artificial restraint exerts upon the structure.

Two superposition equations expressing the conditions pertaining to the moments acting on the original structure (Fig. 3-2a) at joints Band C may

![image 203](Matrix Analysis of Framed Structures_images/imageFile203.png)

3.2 Stiffness Method 123

now be written. Let the actions in the actual structure corresponding to Dl and D2 be denoted AD! and A D2, respectively. These actions will be zero in all cases except when a concentrated external action is applied at a joint corresponding to a degree offreedom. In the example of Fig. 3-2, the action AD! is equal to the couple M while the action AD2 is zero. The superposition equations express the fact that the actions in the original structure (Fig.

- 3-2a) are equal to the corresponding actions in the restrained structure due to the loads (Fig. 3-2b) plus the corresponding actions in the restrained structure due to the unit displacements (Figs. 3-2c and 3-2d) multiplied by the displacements themselves. Therefore, the superposition equations are


AD! = ADLl + 511D1 + 512D2 AD2 = ADL2 + 521D1 + 522D2

(3-4)

The sign convention used throughout these equations is that moments are positive when in the same sense (counterclockwise) as the corresponding unknown displacements.

When Eqs. (3-4) are expressed in matrix form, they become

###### AD = ADL + SD (3-5)

In this equation the vector AD represents the actions in the original beam corresponding to the unknown joint displacements D; the vector ADL represents actions in the restrained structure corresponding to the unknown joint displacements and caused by the loads (that is, all loads except those corresponding to the unknown displacements); and S is the stiffness matrix corresponding to the unknown displacements. The stiffness matrix S could also be denoted ADD, since it represents actions corresponding to the unknown joint displacements and caused by unit values of those displacements. For the example of Fig. 3-2 the matrices are as follows:

###### S= [511

###### AD = [ADl]

ADL = [ADLl] ADL2

521

AD2

In general, these matrices will have as many rows as there are unknown joint displacements. Thus, if d represents the number ofunknown displacements, the order of the stiffness matrix S is d x d, while AD, ADL, and D are vectors of order d x 1.

Subtracting ADL from both sides of Eq. (3-5) and then premultiplying by S-1 gives the following equation for the unknown displacements:

(3-6)

This equation represents the solution for the displacements in matrix terms because the elements of AD, ADL, and S are either known or may be obtained from the restrained structure. Moreover, the member end-actions and reactions for the structure may be found after the joint displacements are known. The procedure for performing such calculations will be illustrated later.

![image 204](Matrix Analysis of Framed Structures_images/imageFile204.png)

124 Chapter 3 Fundamentals of the Stiffness Method

At this point it can be observed that the term - AOL in Eq. (3-6) represents a vector of equivalentjoint loads, as described previously in Sec. 1.12. Such loads are defined as the negatives of restraint actions corresponding to the unknown joint displacements, and they are caused by loads applied to members of the restrained structure. When these equivalent joint loads are added to the actual joint loads AD, the results are called combinedjoint loads

- (see Sec. 1.12). Thus, the parentheses in Eq. (3-6) contain combined joint loads for the stiffness method of analysis.


In order to demonstrate the use of Eq. (3-6), the beam in Fig. 3-2a will be analyzed for the values of the loads previously given as

###### PI = 2P M = PL P2 = P P3 = P

When the loads Ph P2, and P3 act upon the restrained structure (Fig.

- 3-2b), the actions ADLl and A DL2, corresponding to DI and D 2, respectively, are developed by the restraints at B and c. Since the couple M corresponds to one of the unknown displacements, it is taken into account later by means of the matrix AD. The actions ADLl and ADL2 are found from the formulas for fixed-end moments (see Case 1, Table B-l) as


PIL P2L PL

ADLI = - -8- + -8- = - 8

P2L PL

ADL2 = - -8- = 8 Therefore, the matrix ADL is

###### ADL =-PL [-1]

###### 8 -1

It may be observed from these calculations that the load P3 does not enter into the matrix ADL, hence, it does not affect the calculations for the joint displacements. However, this load does affect the calculations for the reactions of the actual beam, which are given later.

The stiffness matrix S consists of the stiffness coefficients shown in Figs. 3-2c and 3-2d. Each coefficient is a couple corresponding to one of the unknown displacements and due to a unit value of one of the displacements. Elements of the first column of the stiffness matrix are shown in

- Fig. 3-2c, and elements of the second column in Fig. 3-2d. In order to find these coefficients, consider first the fixed-end beam shown in Fig. 3-3. This


###### L-(~A--= =<~ )-L

2EI ~4EI

6EI t--

L

---16EI

(2 T

Fig. 3-3. Member stiffnesses for a beam member.

![image 205](Matrix Analysis of Framed Structures_images/imageFile205.png)

3.2 Stiffness Method 125

beam is subjected to a unit rotation at end B, and, as a result, the moment developed at end B is 4EIIL while the moment at the opposite end is 2EIIL (see Case 3, Table B-4). The reactive forces at the ends of the beam are each equal to 6ElIV, and are also indicated in the figure. All of the actions shown in Fig. 3-3 are called member stiffnesses, because they are actions at the ends of the member due to a unit displacement of one end. The end of the beam which undergoes the unit displacement is sometimes called the near end of the beam, and the opposite end is called the far end. Thus, the member stiffnesses at ends A and B are sometimes referred to as the stiffnesses at the far and near ends of the beam. The subject of member stiffnesses is dealt with more extensively in Sec. 3.5 and in Chapter 4.

The task of calculating the joint stiffnesses 5 11 and 521 in Fig. 3-2c may now be performed through the use of member stiffnesses. When the beam is rotated through a unit angle at joint B, a moment equal to 4EIIL is developed at B because of the rotation of the end of member AB. Also, a moment equal to 4EliL is developed at B because of the rotation of the end of member BC. Thus, the total moment at B, equal to 5 11, is

4El 4El 8El 511 = --L + --L = --L

(a)

The stiffness 521 is the moment developed atjoint C when joint B is rotated through a unit angle. Since joint C is at the far end of the member, the stiffness coefficient is

Both 5 11 and 521 are positive because they act in the counterclockwise sense. The stiffness coefficients 512 and 522 are shown in Fig. 3-2d. The first of these is equal to 2ElIL, since it is an action at the far end of the member BC, while the latter is equal to 4EIIL since it is at the near end of the member.

The stiffness matrix S can be formed using the stiffness coefficients described above, as follows:

###### s= El[8 2J

###### L 2 4

Each of the elements in S is a joint stiffness, inasmuch as it represents the action at one of the joints of the structure due to a unit value of a displacement at one of the joints. In this example, the joint stiffness 511 (see Fig.

- 3-2c) is the sum of the near-end member stiffnesses (see Eq. a) for the two members meeting at the joint. Similarly, the stiffness 522 is a near-end member stiffness. On the other hand, the stiffnesses 512 and 521 consist of far-end member stiffnesses for members which connect to a joint that is rotated. In a more general example, it will be found that stiffness elements


![image 206](Matrix Analysis of Framed Structures_images/imageFile206.png)

126 Chapter 3 Fundamentals of the Stiffness Method

On the principal diagonal are always composed ofnear-end stiffnesses while those off the diagonal may consist of either far-end or near-end stiffnesses,

- as will be seen in later examples. After the stiffness matrix S is determined, its inverse can be found. Thus,


-1 L [ 2

S = 14El -1

The next matrix to be determined is the matrix AD, representing the actions in the actual structure corresponding to the unknown displacements. In this example the external load that corresponds to the rotation DI is the couple M (equal to PL) at joint B. There is no moment at joint C corresponding to D2, and therefore the matrix AD is

Now that the matrices AD, S-I, and ADL have been obtained, the matrix of displacements D in the actual structure can be found by substituting them into Eq. (3-6), as follows:

###### L [ 2-IJ {[PLJ PL [-IJ} PV [17J

D=14El -1 4 0 -8 -1 =112EI-5

Thus, the rotations Dl and D2 at joints Band Care

5PL2

D _ 17PV 1 - 112El

D =---

2 112El (b)

These results agree with the joint displacements found by the flexibility method in the example of Sec. 2.5.

The next step after finding the joint displacements is to determine the member end-actions and the reactions for the structure. As in the flexibility method, there are two approaches that can be followed when performing the calculations by hand. One approach is to obtain the end-actions and reactions by making separate calculations after the joint displacements have been found. The other approach is to set up the calculations in a systematic manner in parallel with the calculations for finding the displacements. In this chapter only the second approach will be utilized.

In order to show how the calculations are performed, consider again the two-span beam shown in Fig. 3-2. As in the flexibility method, the matrices of member end-actions and reactions in the actual structure (Fig. 3-2a) will be denoted AM and AR, respectively. In the restrained structure subjected to the loads (Fig. 3-2b), the matrices of end-actions and reactions corresponding to AM and AR will be denoted AML and ARL, respectively. It should be noted again that when any reference is made to the loads on the restrained structure, it is assumed that all of the actual loads are taken into account except those that correspond to an unknown displacement. Thus,

![image 207](Matrix Analysis of Framed Structures_images/imageFile207.png)

3.2 Stiffness Method 127

the joint load M shown in Fig. 3-2a does not appear on the restrained structure in Fig. 3-2b. However, all other loads are considered to act on the restrained beam in Fig. 3-2b, including the load P3' This load does not affect the end-actions AML in the restrained structure, but the reactions ARL are affected. Each of the matrices AM and AML is of order m xl, assuming that m represents the number of member end-actions to be found. Similarly, the matrices AR and ARL are of order r xl, in which r denotes the number of reactions to be found.

In the restrained structure subjected to unit displacements (Figs. 3-2c and 3-2d), the matrices of end-actions and reactions will be denoted AMD and ARD, respectively. The first column ofeach of the matrices will contain the actions obtained from the restrained beam in Fig. 3-2c while the second column is made up of actions obtained from the beam in Fig. 3-2d. In the general case the matrices AMD and ARD are of order m x d and r x d, respectively, in which d represents the number of unknown displacements.

The superposition equations for the end-actions and reactions in the actual structure may now be expressed in the matrix form

###### AM = AML + AMDD AR = ARL + ARDD

- (3-7)
- (3-8)


The above two equations and Eq. (3-5) together constitute the three action superposition equations of the stiffness method. The complete solution of a structure consists of solving for the matrix D of displacements from Eq. (3-6) and then substituting into Eqs. (3-7) and (3-8) to determine AM and AR• When this is done, all joint displacements, member end-actions, and reactions for the structure will be known.

Consider now the use of Eqs. (3-7) and (3-8) in the solution of the twospan beam shown in Fig. 3-2. The unknown displacements D have already been found (see Eqs. b), and all that remains is the determination of the matrices AML> ARL, AMD, and ARD• Assume that the member end-actions to be calculated are the shearing force AMI and moment AM2 at end B of member AB, and the shearing force A M3 and moment AM4 at end B of member Be. These are the same end-actions considered previously in the solution by the flexibility method (see Fig. 2-11b), and are selected solely for illustrative purposes. Also, assume that the reactions to be calculated are the force ARI and couple AR2 at support A, and the forces AR3 and AR4 at supports Band C (see Fig. 3-2a). The first two of these reactions are the same as in the earlier solution, and the last two are the redundants from the earlier solution. All of these actions are assumed positive when either upward or counterclockwise.

In the restrained structure subjected to the loads (Fig. 3-2b), the endactions and reactions in terms of the loads PI, P2, and P3 are seen to be as follows:

![image 208](Matrix Analysis of Framed Structures_images/imageFile208.png)

Chapter 3 Fundamentals of the Stiffness Method

128

###### P2L

###### PI

AMLI = 2

AML4 = -8-

P2

###### PI

ARL4 = 2 - P3

ARLl = 2

The values of the loads (PI = 2P, P2 = P, P3 = P) can now be substituted into these expressions, after which the matrices AML and ARL can be formed as

The matrices AMD and ARD are obtained from an analysis of the beams shown in Figs. 3-2c and 3-2d. For example, the member end-action AMDll is the shearing force at end B of member AB due to a unit displacement corresponding to DI (Fig. 3-2c). Thus, this end-action is

###### 6EI

AMDll = - L2

- as can be seen from Fig. 3-3. The reaction ARDll is the vertical force at support A in the beam of Fig. 3-2c, and is


###### 6EI

###### ARDll = L2

In a similar manner, the other member end-actions and reactions can be found for the beam shown in Fig. 3-2c. These quantities constitute the first columns of the matrices AMD and A RD• The terms in the second columns are found by similar analyses that are made for the beam shown in Fig. 3,2d. The results are as follows:

4Lu f

j]

6

-6

EI 4L AMD = L2 6

EI 2L

[

ARD = L2 0

-6

Substituting the matrices AML and AMD given above, as well as the matrix D obtained earlier, into Eq. (3-7) gives the following:

AM=:[+]+~![-:L~Jl:~;I [~~J=~[~LJ

###### L 4L 2L 36L

These results agree with those found previously by the flexibility method

![image 209](Matrix Analysis of Framed Structures_images/imageFile209.png)

3.3 Examples 129

# Pl10731Ll

- (see Sec. 2.5). By substituting the matrices ARL, ARD, and D into Eg. (3-8) the reactions are found to be


AR = 56 69 -64

These results also agree with those obtained previously by the flexibility method.

The method of solution described above for the two-span beam in Fig. 3-2 is quite general in its basic concepts, and the matrix equations (3-5) to (3-8) may be used in the solution of any type of framed structure. Also, the equations apply to structures having any number of degrees of kinematic indeterminacy n, in which case the order of the stiffness matrix S will be n x n. Several examples illustrating the stiffness method are given in the following section.

3.3 Examples. The examples presented in this section illustrate the application of the stiffness method to several types of structures. In each example the object of the calculations is to determine the unknown joint displacements and certain selected member end-actions and reactions. Because the number of degrees of kinematic indeterminacy is small, the problems are suitable for solution by hand. All of the examples are solved in literal form in order to show clearly how the various terms in the matrices are obtained.

Example 1. The three-span continuous beam shown in Fig. 3-4a has fixed supports at A and D and roller supports at Band C; the length of the middle span is equal to 1.5 times the length ofeach end span. The loads on the beam are assumed to be two concentrated forces acting downward at the positions shown, a uniform load of intensity H' acting on spans BC and CD, and a clockwise couple M applied

- at joint C. All members of the beam are assumed to have the same flexural rigidity EI.


The unknown joint displacements for the beam are the rotations at supports B and C, denoted DI and D 2, respectively, as shown in Fig. 3-4b. For illustrative purposes in this example, it will be assumed that the only member end-actions to be determined are the shearing force A.HI and the moment Am at the left-hand end of member AB, and the shearing force AM3 and moment A.l14 at the left-hand end of member BC, as shown in Fig. 3-4b. The reactions to be found in this example are the vertical forces ARl and AR2 at supports Band C, respectively. Other reactions could also be obtained if desired. All of the end-actions, reactions, and joint displacements are assumed to be positive when upward or counterclockwise.

The only load on the structure that corresponds to one of the unknown joint displacements is the couple M, which corresponds to the rotation D2 (except that it is in the opposite sense). Therefore, the vector AD of actions corresponding to the unknown displacements is

![image 210](Matrix Analysis of Framed Structures_images/imageFile210.png)

130 Chapter 3 Fundamentals of the Stiffness Method

~11 ~21

###### yr ~ ~

- (a)
- (b)


~

###### 1

(d)

(\512 (""\522

###### ~ 4;+=- ~

~

(e)

(

~~r~II---L-If..L...J:;--'-~ ~*J,-,-!b.L-l-W....I.......f.!~

###### VAOL1

V AoL2

(c)

Fig. 3-4. Example 1: Continuous beam.

The remaining loads on the beam are taken into account by considering them to act on the restrained structure shown in Fig. 3-4c. This structure consists of fixed-end beams and is obtained by preventing joints Band C from rotating. The actions ADLI and ADL2 exerted on the beam by the artificial restraints are the couples at supports Band C. Each of the couples is an action corresponding to a displacement D and caused by loads on the beam. The couples can be evaluated without difficulty by referring to the formulas for fixed-end moments given in Table B-1 of Appendix B (see Cases 1 and 6). Hence,

A __ PL w(1.5L)2 __ PL 3wV

DLI - 8 + 12 - 8 + 16

w(1.5L)2 wV 5wV

ADL2 = - 12 +12 = - ~ Thus, the vector ADL becomes

###### = 1:.. [-6P +9WLJ

ADL 48 -5wL

The end-actions AML and the reactions ARL for the restrained beam of Fig. 3-4c can be determined also by referring to the table of fixed-end actions. For example, the end-action AMLI is the shearing force at the left-hand end of member AB and is equal to P12; similarly, the reaction ARLI is the vertical reaction at support B, obtained as follows:

A _ !.. P w(1.5L) _ 3P 3wL

RLI - 2 + + 2 - 2 + 4

![image 211](Matrix Analysis of Framed Structures_images/imageFile211.png)

3.3 Examples 131

By continuing in the same manner, all of the required actions in the restrained structure can be found. The resulting vectors AML and ARL are

###### P

2

_[3;+3';'1

PL

8

A,IL

###### 3l1"L Am - 5l1"L

4 4

###### 311'L2

16

Note that the load P acting downward at Jomt B affects the reactions in the restrained beam but not the member end-actions.

In order to simplify the subsequent calculations, assume now that the following relationships exist between the various loads on the beam:

###### M = PL

Substitution of these relations into the matrices given in the preceding paragraphs yields

PL [ 3J

ADL = 4s -5

The next step in the solution is the analysis of the restrained·beam for the effects of unit displacements corresponding to the unknowns. The two conditions to be taken into account are unit rotations at joints Band C. as illustrated in Figs. 3-4d and 3-4e. The four couples acting at joints Band C in these figures represent the elements of the stiffness matrix S. With the formulas given in Fig. 3-3, each of these stiffnesses can be found without difficulty, as shown in the following calculations:

###### 4EI 4EI 20EI

- 511 = 522 = L + 1.5L = ~ 2EI 4EI
- 512 = 521 = 1.5L = 3L


Therefore, the stiffness matrix S becomes

and the inverse matrix is

###### S--I L [ 5 = 32EI -I

The joint displacements may now be found by substituting the matrices S-l, AD, and All] into Eq. (3-6) and evaluating D, as follows:

-IJ { [OJ PL [ 3J} PU [ 7J

L [ 5 D = 32EI -I

5 PL -I - 4s -5 = 384EI -53

![image 212](Matrix Analysis of Framed Structures_images/imageFile212.png)

132 Chapter 3 Fundamentals of the Stiffness Method

This matrix gives the rotations at joints Band C of the continuous beam shown in Fig.3-4a.

For the determination of the member end-actions and the reactions, it is necessary to consider again the restrained beams shown in Figs. 3-4d and 3-4e. In each of these beams there are end-actions and reactions that correspond to the end-actions and reactions selected previously and shown in Fig. 3-4b. These quantities for the beams with unit displacements are denoted AJJD and A RD, respectively. For example, the end-action AMDll is the shearing force at the left-hand end of member AB due to a unit value of DI (see Fig. 3-4d). The end-action A,U/J21 is the moment at the same location. In all cases the first subscript identifies the end-action itself and the second signifies the unit displacement that produces the action. The reactions in the beams of Figs. 3-4d and 3-4e follow a similar pattern, with ARDll and A RlJ2! being the reactions at supports Band C, respectively, due to a unit value of the displacement DI (Fig. 3-4d). With this identification scheme in mind, and also using the formulas given in Fig. 3-3, it is not difficult to calculate the various end-actions and reactions. For example, the end-actions in the beam of Fig. 3-4d are the following:

AJiD11 = U AMiJ2I = L2El AJ/lJ:ll = (1.5L)26El = 8El3L2 AJJD41 = 1.5L4EI = 3L8El

6El

Also, the reactions in the same beam are

6El 6EI lOEI

6El 8El

ARDII = - U + (1.5L? = - 3V

ARD2! = - (1.5L)2 = - 3V

Similarly, the end-actions and reactions for the beam in Fig. 3-4e can be found, after which the matrices A:l1D and AnD are constructed. These matrices are

###### 2EI[9 0]3L 0

2El [-5 4]

A:l1D = 3V 4 4

AnD = 3V -4 5

4L 2L

The final steps in the solution consist of calculating the matrices AM and An for the end-actions and reactions in the original beam of Fig. 3-4a. These matrices are obtained by substituting into Eqs. (3-7) and (3-8) the matrices D, A ML, A MD, A nL, and ARD, all of which have been determined above. The results become

P 93L351 ] AM = 576 248

###### P [1049]

[

AR = 576 427

30L

Thus, all of the selected end-actions and reactions for the beam have been calculated.

Example 2. The continuous beam ABC shown in Fig. 3-5a has a fixed support at A, a roller support at B, and a guided support at C, Therefore, the only unknown joint displacements are the rotation at support B and the vertical translation at support C, These displacements are denoted D! and D2, respectively, as identified in Fig. 3-5b. The beam has constant flexural rigidity EI and is subjected to the loads PI and P2, acting at the positions shown in the figure. It will be assumed that the loads are given as follows:

![image 213](Matrix Analysis of Framed Structures_images/imageFile213.png)

3.3 Examples

133

![image 214](Matrix Analysis of Framed Structures_images/imageFile214.png)

###### B

###### L/2+L/2+ L/2+L/2--l

![image 215](Matrix Analysis of Framed Structures_images/imageFile215.png)

(0)

![image 216](Matrix Analysis of Framed Structures_images/imageFile216.png)

- (b)
- (c)


![image 217](Matrix Analysis of Framed Structures_images/imageFile217.png)

###### Cl511 t521

![image 218](Matrix Analysis of Framed Structures_images/imageFile218.png)

###### ~I----====!e=-\!;"=t-===---{~

1

![image 219](Matrix Analysis of Framed Structures_images/imageFile219.png)

Fig. 3·5. Example 2: Continuous beam.

For illustrative purposes in this example, certain member end-actions and all of the reactions for the beam are to be calculated. The selected end-actions are the shearing force Am and the moment Am at the right-hand end of member AB (see Fig. 3-5b), and the reactions are the vertical force ARl and couple AR2 at support A, the vertical force AU:l at support B. and the couple A R, at support C (see Fig. 3-5b). All actions and displacements are shown in their positive directions in the figure.

The restrained structure is obtained by preventing rotation at joint B and translation at joint C. thereby giving the two fixed-end beams shown in Fig. 3-5c. Due to the loads on this restrained structure, the actions corresponding to the unknown displacements Dare

Pz P

###### ADDZ = 2 = '2

Also, the member end-actions in the same beam have the formulas

Pl

AMLl = 2 = P

![image 220](Matrix Analysis of Framed Structures_images/imageFile220.png)

134 Chapter 3 Fundamentals of the Stiffness Method

and the reactions are

PI

A - P1L _ PL

ARLI =2 = P

RL2- 8-4

PI P2 3P

ARL3 =2 +2 =2 A __ P

2L __ PL

RL4- 8- 8

From the values given above, the following matrices that are required in the solution can be formed:

###### P[-L]

ADL =8" 4

Mter obtaining the matrices of actions due to loads, the next step is to analyze the restrained beam for unit values of the unknown displacements, as shown in Figs. 3-5d and 3-5e. The stiffnesses Sl1 and S21 caused by a unit rotation at joint B are readily obtained from the formulas given in Fig. 3-3, as follows:

6EI

###### S21=-V

In the case of a unit displacement corresponding to D2 (Fig. 3-5e), it is necessary to have formulas for the forces and couples at the ends of a fixed-end beam subjected to a translation of one end relative to the other. The required formulas can be obtained from Table B-4 of Appendix B (see Case 2). When the translation is equal to unity, the couples at the ends are equal to 6EIIV, and the forces are equal to 12EIIV, as shown in Fig. 3-6. From these values, the stiffnesses S12 and S 22 for the beam in Fig. 3-5e are seen to be

6EI

###### S12=-V

Therefore, the stiffness matrix can be constructed, and its inverse obtained as

s = 2EI [ 4V -36L]

-1 _ ~[6 3L] S - 30EI 3L 4V

V -3L

The inverse matrix, as well as the matrix ADL determined previously, can now be substituted into Eq. (3-6) in order to obtain the matrix D of unknown displacements. The matrix AD appearing in the equation is a null matrix since there are no loads on the original beam corresponding to either Dl or D2• The solution for Dis found to be

![image 221](Matrix Analysis of Framed Structures_images/imageFile221.png)

![image 222](Matrix Analysis of Framed Structures_images/imageFile222.png)

###### L3 r--- /.3

lUI .} L ___-l12EI

Fig. 3-6. Member stiffnesses for a beam member.

![image 223](Matrix Analysis of Framed Structures_images/imageFile223.png)

3.3 Examples 135

PU [ -6 ]

D = 240El -13L

The matrices AMD and ARD which appear in Eqs. (3-7) and (3-8) represent the end-actions and reactions, respectively, in the restrained beams of Figs. 3-5d and 3-5e. The first column of each matrix is associated with a unit value of the displacement D, (Fig. 3-5d), and the second column with a unit value of D2 (Fig. 3-5e). All of the elements in these matrices can be obtained with the aid of the formulas given in Figs. 3-3 and 3-6, and the results are as follows:

3L 2El L2

2El[-3 01

oo ]

AMll =[;2 2L OJ [

ARD =--U 0

- -6
- -3L


u

Then the matrices A~, and AR can be found by substituting the matrices A~IL' A~ID' ARL, AnD, and D into Eqs. (3-7) and (3-8), producing

###### P [17]4L

###### P [ 23]

AM = 20 - 7L

###### AR = 20 ~~

Thus, all of the desired member end-actions and support reactions, as well as the joint displacements, have been calculated.

Example 3. The purpose of this example is to illustrate the analysis of a plane truss by the stiffness method. The truss to be solved is shown in Fig. 3-7a and consists of four members meeting at a common joint E. This particular truss is selected because it has only two degrees of freedom for joint displacement, namely, the horizontal and vertical translations at joint E. However, most of the ensuing discussion pertaining to the solution of this truss is also applicable to more complicated trusses.

It is a convenience in the analysis to identify the bars of the truss numerically. Therefore, the members are numbered from 1 to 4 as shown by the numbers in circles in Fig. 3-7a. Also, for the purposes of general discussion it will be assumed that the four members have lengths L" L 2, L3, and L 4, and axial rigidities EA I , EA2, EA'3, and EA., respectively. Later, all of these quantities will be given specific values in order that the solution may be carried to completion.

The loads on the truss consist of the two concentrated forces P, and P2 acting

- at joint Eo as well as the weights of the members. The weights act as uniformly distributed loads along the members and are assumed to be of intensity H'I, H'2, H"3, and H'4, respectively, for each of the four members. In all cases the intensity IF is the weight of the member per unit distance measured along the axis of the member. For example, the total weight of member 1 is wILl'


The unknown displacements at joint Eo denoted D, and D2 in Fig. 3-7b, are taken as the horizontal and vertical translations of the joint. These displacements, as well as the applied loads at joint Eo will be assumed positive when directed toward the right or upward. The member end-actions to be calculated are selected as the axial forces in the four members at the ends Ao Bo Co and D, respectively. These actions are shown in Fig. 3-7b and are denoted AM" Am, A M3, and AM,' Because of the weights of the members, the axial forces at the other ends (that is, at

![image 224](Matrix Analysis of Framed Structures_images/imageFile224.png)

136 Chapter 3 Fundamentals of the Stiffness Method

A

c

###### ~M3

(a) ( b)

###### A

__ 1")0------,,.,,(; ------

AMLl AOLl

###### B

###### (c)

( d) (e)

Fig. 3-7. Example 3: Plane truss.

joint E) will have different values from those at ends A, B, C, and D. The axial force at end E of each member could be included in the calculations ifdesired; also, the shearing forces at the ends could be included. However, the axial forces at E and the shearing forces are omitted in this example for simplicity. The end-actions are assumed positive when they produce tension in the members. It is superfluous to calculate reactions for the truss in Fig. 3-7 inasmuch as the reactions are the same as the end-actions. However, there are other situations, such as when several members of a truss are joined at one point of support, in which the reactions should be determined separately.

The loads PI and P2 acting at joint E of the structure (Fig. 3-7a) are loads that correspond to the unknown displacements DI and D2, respectively. Therefore, these loads appear in the vector AD as follows:

![image 225](Matrix Analysis of Framed Structures_images/imageFile225.png)

3.3 Examples 137

The remaining loads on the truss are considered to act on the restrained structure. which is obtained by preventing translation ofjoint E (Fig. 3-7c). Each member of the truss is, therefore, in the condition indicated in Fig. 3-8, which shows an inclined truss member that is supported at both ends by immovable pin supports. For purposes ofgeneral discussion, the points of support are denoted A and B in the figure. The weight of the member itself is represented by the uniform load of intensity II'. The reactions for the member are two vertical forces, each of which is equal to onehalf the weight of the member (see Appendix B, Table B-5). Therefore, the actions AfJ/. for the restrained truss shown in Fig. 3-7c can be readily calculated. The actions to be determined at joint E are the horizontal force Am.l and the vertical force A DL2 , which correspond to the displacements Dl and D2, respectively. Since the weights of the members produce no horizontal reactions. the action Au/.! must be zero. However, the action ADL2 will be equal to one-half the weight of all members meeting at joint E. Therefore, the vector ADL becomes

The quantity W is the total weight of all members meeting at joint E. which in this example is also the total weight of the truss.

For the purpose of calculating the end-actions for the members, it is also necessary to obtain the vector A~IL from a consideration of the restrained structure shown in Fig. 3-7c. This vector consists of the end-actions A JJLl , A.llJ.2, AIlL:J, and A.\JJA, which are shown in the figure in the positive directions (tension in the members). Each such quantity is given by the general formula

- -II'L sin 'Y

2

in which ')i is the angle between the axis of the member and the horizontal; and the minus sign indicates that the force is compression. To apply this formula to the truss in Fig. 3-7, it is necessary first to identify the angles between the members and the horizontal. Lettheseangles be denoted,to,2,,:J,and'4for thefourmembers 1,2, 3, and 4, respectively. These angles are shown in Fig. 3-7a for all membeb except member 1, which is assumed to be horizontal in this particular example. Thus, the end-action A.l1L2, for example, is given by the expression

1I'2L 2 •

AML2 = - -2- sm 12

Fig. 3-8. End-actions for restrained truss member.

![image 226](Matrix Analysis of Framed Structures_images/imageFile226.png)

138 Chapter 3 Fundamentals of the Stiffness Method and it can be seen that the vector AML is the following:

This vector can be evaluated in any particular case by substituting the appropriate values for each member of the truss. If it is assumed that member 1 is horizontal and member 4 is vertical, then the first and last elements of the vector can be simplified to zero and -w4LJ2, respectively.

To obtain the stiffness matrix S, it is necessary to impose unit displacements corresponding to DI and D2 on the restrained structure, as shown in Figs. 3-7d and 3-7e, respectively. The actions corresponding to the joint displacements are the four joint stiffnesses Su, S21> S12, and S22' Each of these stiffnesses is shown in the figure acting in the positive direction. The joint stiffnesses are composed of contributions from each member of the truss; that is, from the stiffnesses ofthe members themselves. For example, Su is the total force in the horizontal direction when a unit displacement in that direction is imposed upon the truss (see Fig. 3-7d) and consists ofthe sum ofthe horizontal components ofthe forces in all members ofthe truss. Thus, to obtain the joint stiffnesses shown in the figure it is first necessary to find the forces acting on the individual members when joint E is displaced.

The forces acting on a typical truss member due to a unit horizontal displacement of one end are shown in Fig. 3-9a. For purposes of general discussion, the lower and upper ends of the member are denoted as ends A and B. respectively. The upper end of the member is assumed to be moved a unit distance to the right, while all other end displacements are zero. As a result, the member becomes lengthened, and restraint forces are required at each end. The elongation of the member is determined from the displacements occurring at end B, as shown in Fig. 3-9b. From the triangle in the figure it is seen that the elongation of the member is cos 'Y, in which 'Y is the angle of inclination of the member. Therefore, the tensile force in the member is (see Fig. 3-9a)

EA

TCosy

in which EA is the axial rigidity and L is the length ofthe member. The components of this axial force in the horizontal and vertical directions are also shown in the figure. These components, which are member stiffnesses, can be readily determined from the geometry ofthe figure.

In the case of a unit vertical displacement of end B of the member (Fig. 3-9c), the axial force in the member is

EA .

Tsmy

from which the components in the horizontal and vertical directions can be easily found. All of the forces for this case are shown in Fig. 3-9c.

If the lower end A of the member in Fig. 3-9a is displaced a unit distance to the right while the upper end B remains fixed, all of the actions shown in the figure will have their directions reversed. The same thing happens to the member shown in Fig. 3-9c if end A is displaced upward a unit distance while end B remains fixed.

![image 227](Matrix Analysis of Framed Structures_images/imageFile227.png)

3.3 Examples

139

![image 228](Matrix Analysis of Framed Structures_images/imageFile228.png)

T£A COS T SIn. T

T£A COS T

###### £A 2

###### TCOS T

£A 2 TCOS T

###### £A

T COS T

LfA SIn-Y.

(0 )

cLA sin T cos T

###### £A .

TSln T COS T

EA ,

T SIn T----tr'7'

(C)

Fig. 3-9. Member stiffnesses for a plane truss member.

All of the formulas given in Fig. 3-9 are suitable for use in analyzing plane trusses by the stiffness method when the calculations are being performed by hand. Later, a more systematic approach to the use of member stiffnesses will be given, not only for trusses but also for other types of structures (see Sec. 3.5 and Chapter 4).

Now consider again the calculation of the joint stiffnesses for the restrained truss shown in Figs. 3-7d and 3-7e. The stiffness S" is composed of contributions from the various members of the truss. For example, the contribution to S" from member 3 (see Fig. 3-9a) is

###### EA3

-- cos2 13

###### L3

Similarly, the contribution of member 3 to the stiffness S2' (see Fig. 3-9a) becomes "'"'L;EA3 cos 13 sm. 13

Expressions of the same form as the two formulas given above can be written for all four members of the truss. The sums of such expressions yield the stiffnesses S" and S21' Inasmuch as member I is horizontal b', = 0) and member 4 is vertical ('Y4

= 90°), these sums for the stiffnesses are

![image 229](Matrix Analysis of Framed Structures_images/imageFile229.png)

140 Chapter 3 Fundamentals of the Stiffness Method

S11 = --y;:EA, + -z:;EA2 COS2 'Y2 + I:;EA3 COS2 'Y3

S EA2 . EA3 .

2' =-L COS 'Y2 sm 'Y2 + -L COS 'Y3 sm 'Y3

2 3

By following an analogous procedure but using the formulas in Fig. 3-9c, the stiffnesses SI2 and S22 (see Fig. 3-7e) are obtained, as follows:

###### S EA2 • EA3 .

'2 = -L sm 'Y2 cos 'Y2 + -L sm 'Y3 cos 'Y3

2 3

###### S EAz • 2 EA3 . 2 EA. 22 = --L2 sm 'Y2 + --L3 sm 'Y3 + --L.

The above four expressions constitute the elements of the stiffness matrix S. The remaining steps in the calculation of the joint displacements consist of inverting S and substituting it into Eq. (3-6). This part of the solution will be performed later using specific values for the quantities EA, L, and 'Y. Before proceeding to that stage of the solution, however, the matrix AMD of member end-actions in the restrained structures of Figs. 3-7d and 3-7e will be obtained in general terms.

All of the member end-actions due to the unit joint displacements are shown in Figs. 3-7d and 3-7e. For example, the axial force AMD3l is the force in member 3 due to a unit value of the displacement D,. Each such force is obtained by referring to Fig. 3-9a or 3-9c. The force AMD3" for instance, is given by the expression

###### L;EA3 cos 'Y3

as found from Fig. 3-9a. If one proceeds in this manner, all of the end-actions due to unit displacements can be found, and the matrix AMD becomes

EA,

o

###### L,

- -z:;EA2 sm. 'Y2
- ---y;;EA3 sm. 'Y3


-z:;EA2 cos 'Y2 ---y;;EA3 cos 'Y3

EA4

o

###### L4

As mentioned previously, other end-actions, as well as reactions, may also be included in the analysis. Under such conditions, the appropriate formulas from Fig. 3-9 can be used in finding the values of the various actions due to the unit displacements. When all of the required matrices have been formed, Eqs. (3-6) through (3-8) are used in finding the resultant effects.

The preceding discussion has served to illustrate in general terms how the various matrices are obtained in a truss analysis. In order to complete the solution of the truss in Fig. 3-7, it is necessary to assume specific values for the quantities appearing in the matrices. Therefore, it will be assumed that all members have the same length L, the same axial rigidity EA, and the same weight w per unit length. Furthermore, it is assumed that the angles between adjoining members are 30 degrees, so that the angles between the members and the horizontal are

'Yl = 0 'Y4 = 90"

![image 230](Matrix Analysis of Framed Structures_images/imageFile230.png)

3.3 Examples 141

Also, the total weight W of the truss is

###### W = 4wL

When these substitutions are made, the matrices described above simplify to the following:

###### ADL=ll'L [~] S~EA[4 V3]

2L 0 4

0 2 0 l

###### wL EA v3

4 0 AMD=2L ~J 2 0 The inverse of S is

AML

S~I 2L [4 -0]

13EA -0 4

and the vector D, found from Eq. (3-6), is

###### D =~ [4PI - 0p2 + 20w.L ]

###### 13EA -0PI + 4P2 - 8wL

Into this vector can be substituted any particular values of the loads PI and P2, as well as the weight l1' per unit length. Then the vector AM of end-actions (or member forces) can be found by substituting the matrices AML, AMD, and D into Eq. (3-7) and solving. If the weight of the truss is not included in the analysis, the matrices ADL and AML become null.

As a particular case, assume that PI = 0, P2 = -p, and wL = PlIO. Then the vectors D and AM are found to be

D=12PL [0]

960

- -61
- -1570
- -410


65EA -4

These results show that, under the assumed loading, joint E is displaced to the right and downward, and all members of the truss are subjected to compression except member 1.

Example 4. The analysis of the plane frame ABC shown in Fig. 3-lOa is described in this example. This frame was analyzed previously by the flexibility method in Example 4 of Sec. 2.3. When using the stiffness method, the first step is to determine the number of unknown joint displacements. In this example. the number of unknowns depends upon whether both flexural and axial deformations are considered in the analysis. If both types of deformation are included. joint B can

![image 231](Matrix Analysis of Framed Structures_images/imageFile231.png)

Chapter 3 Fundamentals of the Stiffness Method

142

(0)

(b)

###### p(~A

8 p

"2

###### ...-HZ6£I c

c

~t6£I

2£I ~ L2

(d) H

( c)

Fig. 3-10. Example 4: Plane frame (flexural effects only).

translate as well as rotate. An analysis of this kind is made later in the section. However, in a plane frame it is normally not necessary to include the axial deformations. If they are omitted, joint B will rotate but not translate, and there will be only one unknown displacement D (see Fig. 3-lOb). In addition to finding this joint displacement, it will be assumed arbitrarily that the following end-actions and reactions are to be found as part of the solution: the axial force AMI' shearing force AM2 , and moment AM3 at the right-hand end of member AB (see Fig. 3-lOb) and the three reactions ARI , AR2, and AR3 at support A. Both members of the frame are assumed to have the same flexural rigidity EI.

The restrained structure (Fig. 3-1Oc) is obtained by preventing rotation ofjoint B. The action ADL corresponding to the unknown displacement D and caused by the load Pis

###### PL

###### ADL =-g

The end-actions and reactions in the restrained structure due to the load P are

###### PL

###### P

AML3 =-g

AML2 ="2

###### PL

###### P

###### ARL3 = g

ARL2 ="2

ARLl = 0

All of the reactions in the restrained structure due to the load P are shown in Fig. 3-1Oc. It should be recalled at this stage of the calculations that the restraint at joint

![image 232](Matrix Analysis of Framed Structures_images/imageFile232.png)

3.3 Examples 143 B is a rotational restraint only, and hence it offers no restraint against translation. Therefore, horizontal and vertical forces can be transmitted through joint B from one member to the other. As a result, the vertical reactive force PI2 at the righthand end of member AB is sustained at joint C rather than at joint B. The vectors ADL, AML, and ARL become

In this problem the vector AD is a null vector containing one zero element because there is no couple applied as a load at joint B of the frame.

The stiffness matrix for the frame is found by imposing a unit displacement corresponding to D on the restrained structure (see Fig. 3-lOd). From the figure it is seen that the stiffness S is

Therefore, the stiffness matrix S and its inverse are

8-1 _ [ LH ]

- 4EI(L + H)

The end-actions and reactions for the restrained frame of Fig. 3-lOd are evaluated next. Again recalling that there is only a rotational restraint at joint B, it is seen that the reactions for the restrained frame have the values shown in Fig. 3-10d. Therefore, the matrices of end-actions and reactions are as follows:

6EI 6EI H2 Jii

6EI

6EI L2 V 4EI 2EI L L

ARD =

AMD

All of the above matrices are now substituted into Eqs. (3-6), (3-7), and (3-8), producing the results

PV [ H ]

D = 32EI L + H

-3V ] [ 3V ]

###### = 16H(: + H) H(8L + 5H) AR = 16H(: H) H(8L + 11H)

[

-2HV + HL(2L + 3H) In the special case when H = L, these results simplify to

###### P [ -3] P [ 3]

PV

AM = 32 13 AR = 32 19

D = 64EI

-2L 5L

The three elements of the vector AM have the same physical meanings as the redundant actions QIo Q2, and Q3 of Example 4, Sec. 2.3 (compare Figs. 3-lOb and 26b). Therefore, the values given above for the end-actions agree with those of QI,

![image 233](Matrix Analysis of Framed Structures_images/imageFile233.png)

144 Chapter 3 Fundamentals of the Stiffness Method

Q2, and Q3 obtained in the earlier example for the case when axial deformations are neglected.

When axial deformations are included in the analysis of the plane frame in Fig. 3-lOa, three degrees of freedom must be recognized at joint B instead of only one. The displacements Db D2, and D3 for this case are shown in Fig. 3-11a. The restrained structure for this new analysis is obtained by preventing horizontal translation, vertical translation, and rotation at joint B (see Fig. 3-11b). The actions in this restrained structure corresponding to the unknown displacements and caused by the load P are shown in the figure as A DLb A DL2, and A DL3• These restraint actions are

ADL2 ="2 ADL3 = - 8PL

P

###### ADLI = 0

Thus, the vector ADL is

###### Ao, ~~[-~J

As before, the vector AD is a null vector because there are no forces or couples applied as loads at joint B.

###### c c

(0 l (b l

A

###### c

(c l (dl

###### c

(e l

###### Fig. 3-11. Example 4: Plane frame (flexural and axial effects!.

![image 234](Matrix Analysis of Framed Structures_images/imageFile234.png)

3.3 Examples 145

The elements of the stiffness matrix for the frame are pictured in Figs. 3-11c, d, and e. These figures show the actions developed at the restrainedjoint B when unit displacements corresponding to DI, D2, and D3 are introduced. Each action can be found from the expressions for end-actions due to a unit displacement (see Figs. 3-3,3-6, and 3-9). Thus, the stiffness matrix is

LEA + 12ElHI 0 6ElH2 S= 0

------u-12EI +IfEA 6ElL2

6EI 6EI 4EI 4EI H2 V T+li

The inverse of this 3 x 3 matrix cannot be obtained easily in literal form. Therefore, the problem will be simplified by letting H = L and by using the dimensionless parameter

AL2

V =--

1

which is the reciprocal of the parameter y used previously for analyzing this frame by the flexibility method. Then the stiffness matrix becomes

_ EI [12 + v 0 6L ] S - V 0 12 + v -6L

###### 6L -6L 8L2

and its inverse is

###### -36L2 4L2ca 6Lci

where

CI = 12 + v

C3 = 5 + 2v Substitution of S-I and ADL into Eq. (3-6) yields

PU [6LC"] D = 64Elc C - 2Lc5

I 2 -C I C 4

in which

###### C5 = 4 + 13v

c" = 12 - v

In terms of v, the joint displacements are

3PL3 12 - v

DI = 32EI (12 + v)(3 + v)

- -PV 4 + 13v D2 = 32El (12 + v)(3 + v)
- -PU 12 - v


###### Da = 64EI u--;

If the quantity v is large, the values of DI and D2 tend to zero; and the value of D3 becomes PVI64El, as in the first part of this example.

![image 235](Matrix Analysis of Framed Structures_images/imageFile235.png)

146 Chapter 3 Fundamentals of the Stiffness Method

Example 5. The grid shown in Fig. 3-12a consists of two members (AB and BC) that are rigidly joined at B. The load on the grid is a concentrated force P acting at the midpoint of member AB. Each member is assumed to have constant flexural rigidity EI and torsional rigidity GJ. Because the supports at A and Care fixed, the only unknown joint displacements for the structure occur at joint B. These are a translation D, in the y direction, a rotation D2 about the x axis, and a rotation D3 about the z axis, as indicated in Fig. 3-12b. In the figure the positive direction of each displacement vector is assumed to be the same as the positive direction ofone ofthe coordinate axes. As in earlier articles, a double-headed arrow is used to distinguish a rotation from a translation. The number of degrees of freedom of the grid happens to be the same as the degree of static indeterminacy (see Example 5, Sec. 2.3).

To begin analyzing the grid by the stiffness method, an artificial restraint is supplied at joint B to prevent displacements corresponding to D" D2 , and D3 (see Fig. 3-12c). When the loads act upon this restrained structure, the actions ADL (corresponding to the displacements D) are developed at the restraint. These actions are evaluated readily by making use of the formulas for fixed-end actions in beams (see Appendix B). In the case of the load P acting on member AB, the restraint actions are

###### PL

###### P

ADLl ="2

AlJL2 = 0 A DL3 =

8

###### y

B L

###### _LIZY

.!

(0 )

D, Bt ___D2

A

~

- (b)
- (c)


Fig. 3-12. Example 5: Grid.

![image 236](Matrix Analysis of Framed Structures_images/imageFile236.png)

3.3 Examples

147

s,',

###### + s;,

~~s'

~A~!1!2'

(e)

(d)

###### S"2

s"

t~S~2

###### S:~E~

~'i-A_____B--{r~ ~

###### (g)

( f )

(\ )

(h)

Fig. 3-12. (Continued)

and, hence, the vector Am. is

The vector AD, representing actions applied to the actual beam (Fig. 3-12a) corresponding to the unknown displacements, is a null vector because there are no concentrated forces or couples at joint B.

The stiffness matrix for the grid is found by analyzing the restrained structure for the effects of unit values of the unknown displacements. In the case of a unit value of D1, joint B is displaced upward by a unit distance without rotating. Then the actions developed at the restraint corresponding to Dlo D2, and Da are the joint stiffnesses S11, S210 and S31, respectively. The effects of this unit translation on members AB and BC are shown separately in Figs. 3-12d and 3-12e. In Fig. 3-12d the contributions of member AB to the joint stiffnesses are shown with a single prime, while in Fig. 3-12e the contributions from member BC are shown with a double prime. From the figures it can be seen that the stiffness terms are as follows:

S' __ 6EI 31 - L2 S" _ 6EI

S;I = 0

21 - L2 5';1 = 0

Therefore, the joint stiffnesses, found by summing the effects from both members, are

6EI S21=---yy

In a similar manner the stiffnesses resulting from unit rotations corresponding

![image 237](Matrix Analysis of Framed Structures_images/imageFile237.png)

148 Chapter 3 Fundamentals of the Stiffness Method

to D2 and D3 can be found. The contributions from the individual members are pictured in Figs. 3-12fthrough 3-12i, and can be evaluated by inspection. In the case ofa unit value of D2 (see Figs. 3-12fand 3-12g) the contributions are

S' _ GJ

22 - L

S" _ 6EI

###### S" _ 4EI

'2 - L2

22 - L

For a unit value of D3 the contributions (see Figs. 3-12h and 3-12i) become S' _ 4EI

33 - L

###### S" _ GJ 33 - L

Summing the individual terms given above yields the joint stiffnesses

6EI

4EI GJ

###### S22 =Y+T

S'2=V

6EI

4El GJ

S,;) =-V S2;) = 0

###### S:l3=Y+T

Finally, the stiffness matrix S can be expressed in the following form:

###### EI [ 24 6L

S = V 6L (4 + YJ)U

-6L 0 in which the dimensionless parameter YJ is

The quantity YJ is the reciprocal of the parameter p used in solving this same grid by the flexibility method. The inverse matrix is

###### -6Ld,

###### -366Ld,]

12d3

###### -36

12£13

in which the following additional parameters are used:

d, = 4 + YJ

The quantities YJ, db d2, and d3 depend only on the ratio of the torsional rigidity GJ to the bending rigidity EI.

The displacements at joint B can be found by substituting the matrices AOL and S~' into Eq. (3-6) and solving for D. This yields the result

from which

![image 238](Matrix Analysis of Framed Structures_images/imageFile238.png)

3.4 Temperature Changes, Prestrains, and Support Displacements

149

PV 5 + 27J DJ = -96£/~

D _ PU 5 + 27J

2 - 16£1 (1 + 7J)(4 + 7J)

3PU I

D - --- -----:1 - 16£1 (I +7J)(4 + 7J)

If the members AB and Be are torsionally very weak, the grid can be considered to consist of two members joined at B by a hinge that is capable of transmitting a vertical force but not a couple. In the analysis of such a grid by the stiffness method, the only joint displacement to be treated as an unknown in the analysis is the translation in the y direction. Its value can be found from the result given above for DJ by letting 7J become zero. Thus,

In general, the analysis of a grid consisting of beams that cross one another (thereby transmitting a vertical force but no moment at each crossing point) will have one unknown joint displacement at each such point.

End-actions and reactions for the grid can also be calculated, following the general techniques illustrated in the preceding examples. Such calculations are given as problems at the end of the chapter.

3.4 Temperature Changes, Prestrains, and Support Displacements.

The effects of temperature changes, prestrain of members, and support displacements can be readily incorporated into the analysis of a structure by the stiffness method. A convenient procedure is to consider all such effects to occur in the restrained structure and to add the resulting actions to the actions produced by the loads. For example, in the restrained structure subjected to loads only, it is necessary to calculate the actions ADL corresponding to the unknown displacements (see Eq. 3-5). When temperature changes are assumed to occur in the same restrained structure, additional actions corresponding to the unknown displacements may occur. Such actions will be denoted by the symbol ADT, which is consistent with the symbol ADL except that the cause is temperature rather than loads. The same idea can be applied to prestrains and restraint displacements, which will produce in the restrained structure the actions ADP and A DR, respectively. When all such actions have been determined for the restrained structure, the vectors ADL, ADT, A DP, and ADR can be formed. These vectors are of order 11 x 1, where 11 denotes the number of unknown displacements. The sum of these vectors represents the combination of all actions corresponding to the unknown displacements, and is denoted ADC• Hence, this vector is

A DC = ADL + ADT + Aop + A Dn (3-9)

The vector ADC is included in the first of the three equations of superposition, in place of the matrix ADL alone (see Eq. 3-5):

![image 239](Matrix Analysis of Framed Structures_images/imageFile239.png)

###### AD = ADC + SD (3-10)

This equation is a more general equation of the stiffness method and should be used instead of Eq. (3-5) whenever effects other than loads are to be included in the calculations. The equation can be solved for the displacements as follows:

D = S-I(AD - ADd (3-11)

From this form it can be seen that the term - ADC constitutes a vector of equivalent joint loads (see Sec. 1.12).

Temperature changes, prestrains, and support displacements also affect the determination of member end-actions and reactions in a structure. The vectors of end-actions in the restrained structure due to these causes are denoted AMT, AMP, and AMR, respectively, and the combination of all such actions, including loads, is the vector

(3-12)

In an analogous manner the combination of all reactions due to these causes in the restrained structure gives the vector ARC:

###### ARC = ARL + ART + ARP + ARR (3-13)

in which the four matrices on the right-hand side of the equation represent reactions due to loads, temperature changes, prestrains, and restraint displacements, respectively. The equations of superposition for the member end-actions and the reactions now become

###### AM = AMC + AMDD AR = ARC + ARDD

(3-14) (3-15)

These equations may be considered as generalized forms of Eqs. (3-7) and (3-8), which were used previously when only loads acted on the structure. The use of the above equations will now be illustrated by extending the two-span beam example given in Sec. 3.2 (see Fig. 3-2).

The beam to be analyzed is pictured again in Fig. 3-13a. The loads are not shown in the figure because their effects were considered in the earlier example. The unknown joint displacements DJ and D2 are indicated in Fig. 3-13a by the curved arrows. For illustrative purposes, consider first the effects of temperature changes, and assume that member BC is subjected to a linear temperature gradient such that the lower surface of the beam has a temperature change 6 TJ , while the upper surface changes 6 T2• Member AB is assumed to remain at a constant temperature. When these temperature effects are assumed to occur in the restrained structure (see Fig. 3-13b), there will be moments developed at the ends ofmember Be. Therefore, a restraint action ADTJ will be developed at joint B corresponding to the displacement D J and an action ADT2 will be developed at joint C corresponding to D 2. These actions are shown in their positive directions in the figure and can be evaluated from the expressions for fixed-end actions due to temperature

![image 240](Matrix Analysis of Framed Structures_images/imageFile240.png)

3.4 Temperature Changes, Prestrains, and Support Displacements 151

(\1 (\2

~1-A'--------'¥¥"'--B-----"l¥

###### I--L-----1·1---L~

(0 )

(b)

###### j~~

###### J AOR1 ~R2

(c)

Fig. 3·13. Continuous beam with temperature differential and support displacement.

changes given in Table B-2 of Appendix B. Thus,

a EI(!1 T] - !1 T2 )

ADTJ = -ADT2 = d

in which a is the coefficient of thermal expansion, EI is the flexural rigidity of the beam, and d is the depth of the beam. The vector ADT can now be expressed as

A = aEI(LT] - LT2 )I Il

OT d L-1

This vector can be added to the vector AOL obtained in the example of Sec. 3.2 to give the sum Aoc for use in Eq. (3-10), assuming that the beam is to be analyzed for the combined effects of the loads (see Fig. 3-2a) and the temperature differential in member Be. Of course, the displacements calculated for both effects together will be the sum of the displacements obtained when the loads and the temperature effects are considered separately.

In a similar manner the member end-actions and the reactions due to the temperature change in member Be can be determined from the restrained beam in Fig. 3-13b. In this particular example the member endactions are zero in span AB, and in member Be are the same fixed-end actions discussed above. Also, in this example all the reactions are zero inasmuch as the temperature differential does not produce any vertical force at joints Band C. However, in a more general situation there will be values for both the end-actions and the reactions; and these two sets of values are placed into the vectors AMT and ART, respectively. Then these quantities are added to the corresponding quantities caused by the loads, and the combined vectors are substituted into Eqs. (3-14) and (3-15).

![image 241](Matrix Analysis of Framed Structures_images/imageFile241.png)

The procedure is similar for prestrain effects and support displacements. In both cases three vectors ofactions in the restrained structure are to be determined (ADP, AMP, ARP, and ADR, AMR, ARR). All of these vectors can be evaluated readily when the fixed-end actions are known. Such fixedend actions are given in Tables B-3 and B-4 of Appendix B. Suppose, for example, that support B of the beam is known to undergo a downward displacement equal to s (see Fig. 3-13c). This results in actions ADRl and ADR2, which are evaluated as follows (see Table B-4):

6E1s 6E1s ADRl = -- - -- = 0

6E1s

ADR2 = ---L2

L2 L2

The vector ADR is formed from these expressions and then included in the calculation of ADC (see Eq. 3-9). In a similar manner the vectors of endactions and reactions (AMR and ARR) due to the support displacement shown in Fig. 3-13c can be found. These vectors are included in the calculations for AMC and ARC (see Eqs. 3-12 and 3-13).

As an example in which prestrain effects are to be determined, consider the analysis ofthe plane truss shown in Fig. 3-7. Previously, this truss was analyzed for the effects of the loads acting at joint E and for the weights of the members. Now assume that one of the members, such as member 3, is constructed with a length L3 + e, instead of the theoretical length L3. The effect of the additional increment of length is assumed to take place in the restrained truss shown in Fig. 3-7c. The result is that actions A DP1 and ADP2 are developed at joint E, corresponding to Dl and D2, respectively, and an axial force AMP3 is developed in member 3, corresponding to the action AM3• All of these actions can be found without difficulty. For instance, the axial force is

EA3e

AMP3 = ---

L3

and the vector AMP becomes

L3o

The horizontal and vertical components of the axial force in the member are used to obtain the actions atjoint E in the restrained truss:

EA3e

A DP1 = - -- cos 1'3

###### L3

Therefore, the vector ADP is

ADP = _ EA3e [c~s 1'3]

L3 sm 1'3

![image 242](Matrix Analysis of Framed Structures_images/imageFile242.png)

3.5 Stiffnesses of Prismatic Members 153

The vectors ADP and AMP, found above, are added to the vectors ADL and AML, found in the earlier example, to give the combined vectors ADC and AMC' Then these vectors are used in Eqs. (3-11) and (3-14) when solving for the joint displacements and the member end-actions. The final results for the combined effects of loads and prestrains will be the sum of the results obtained for loads and prestrains occurring separately.

3.5 Stiffnesses of Prismatic Members. Commonly recurring stiffness coefficients (such as 4EIIL) for prismatic members may be placed into member stiffness matrices for various types offramed structures. Terms in such a matrix are defined as holding actions at the ends ofa member due to unit displacements of one end relative to the other. The type of member stiffness matrix SM; to be considered in this article is the inverse of the type of member flexibility matrix FMi discussed in Sec. 2.6. Thus,

SM; = F;;j\ (3-16)

Recall that FM; pertains to a member i that is fixed at the j end and free at the k end (see Figs. 2-13 through 2-17). Flexibilities in this matrix are defined as the relative displacements of the k end of the member with respect to the j end, due to unit actions at the k end. On the other hand, the inverse matrix SM; contains holding actions at the k end of the member, required for unit relative displacements of the k end with respect to the j end. Such member stiffnesses will be found directly by inducing unit displacements at the k ends of members for the same types of framed structures considered before. Formulas for the stiffness terms in SM; may be obtained from Table B-4 in Appendix B, and the results can be checked by the inversion process mentioned above. Member stiffness matrices developed in this manner will be used in the formalized approach to the stiffness method described in the next section.

Figure 3-14a shows a prismatic beam member i with both the j and k ends fixed. As before, the member-oriented axes are arranged so that the XM -YM plane is a principal plane of bending. Indicated by arrows at the k end of the member are the two kinds of displacements of interest: a translation DMl in the YM direction and a rotation DM2 in the ZM sense. The member stiffness matrix to be obtained is a 2 x 2 array relating DMl and DM2 to the corresponding actions AMl (force in the YM direction) and AM2 (moment in the ZM sense). Figures 3-14b and 3-14c show the restraint actions at the k end of the member due to unit displacements DMl = 1 and DM2 = 1. These terms form the beam stiffness matrix SMi. as follows:

###### _6E1]U

###### sM12] [ V12E1

(3-17)

= 6£1

4£1

SM22 - V

L

![image 243](Matrix Analysis of Framed Structures_images/imageFile243.png)

(b)

Fig. 3-14. Stiffnesses for beam member.

It is seen that this matrix is the inverse of the beam flexibility matrix FMi in Eq. (2-19).

For the truss member in Fig. 3-15a, only the axial translation DM at the k end need be considered. The corresponding action AM is the axial force at the k end, and the single member stiffness (see Fig. 3-15b) is found to be

(3-18)

which is the reciprocal ofthe flexibility F..,n in Eq. (2-20).

The stiffness matrix for a plane frame member is the same as that for a beam (see Eq. 3-17) if axial strains are to be neglected. Otherwise, if axial strains are to be considered, the term in Eq. (3-18) must also be included. In the latter case three displacement components at the k end of the member are required, as indicated in Fig. 3-16a. They are the translation DM! in the XM direction, the translation DM2 in the YM direction, and the rotation DM3 in the Z.'J sense. Figures 3-16b, c, and d show unit values of these displacements and the corresponding restraint actions that constitute the following 3 x 3 array:

###### EA

- 0 0

SMll SM!2 SM!3

L

###### 12EI 6EI

0 ----- (3-19)

SMi= SM2! SM22 SM23

L3 L2

###### 6EI 4EI

0 --

SM3! SM32 SM33

###### L2 L

![image 244](Matrix Analysis of Framed Structures_images/imageFile244.png)

3.5 Stiffnesses of Prismatic Members 155

###### o DM

~j k~---XM

/ I__E--L-_~I

ZM

(0)

(b)

Fig. 3-15. Stiffness for truss member.

This plane frame member stiffness matrix is, of course, the inverse of the flexibility matrix in Eq. (2-21).

Figure 3-17a illustrates a grid member for which bending occurs in the X,~rYM plane, as with a beam or plane frame member. Indicated at the k end of the member are a translation DMI in the YM direction, a rotation D.'d2 in the X.II sense, and a rotation D.l13 in the ZM sense. Unit values of these displacements produce the stiffness terms shown in Figs. 3-17b, c, and d. The resulting 3 x 3 member stiffness matrix is

###### YM

###### DM2

t

~ CD ~DMI

~-j-~/ 7'-xM

/

I~E~_____L__D_M_3__~.1

(e) tSM22

(b)

~411

(e) (d)

###### Fig. 3-16. Stiffnesses for plane frame member.

![image 245](Matrix Analysis of Framed Structures_images/imageFile245.png)

156 Chapter 3 Fundamentals of the Stiffness Method

J\r

###### ~_"""""""'~I~~i-r

t5Mt3

~f--------\%1:;

5.4133

(d)

(c)

###### Fig. 3-17. Stiffnesses for grid member.

###### 12EI

o

SMll SM12 SM13

###### L3

GJ

o

o V o 4EIL

(3-20)

L

6EI

SM31 SM32 SM33

which is the inverse of the flexibility matrix given in Eq. (2-22).

Determination ofthe stiffness matrix for a space frame member requires that six kinds ofdisplacements be considered at the k end. Indicated in Fig. 3-18a are three components of translation D Mb DM2, and DM3 (in the XM, YM, and ZM directions) and three components of rotation DM4, DM5, and DM6 (in the XM, YM, and ZM senses). As before, the XM -YM plane and the XM -ZM plane are taken to be principal planes of bending. Figures 3-18b through 3-18g show stiffness coefficients at the k end of the member due to unit values of the displacements DM1 through D M6• These terms become the nonzero elements in the following 6 x 6 member stiffness matrix:

###### EA

0 o o 0 0

L

12Elz

6Elz

0 0 0

0

L3

L2

6Ely

12E/y

0

0 L2 (3-21) 0 0

0 0

###### L3

SMi=

###### GJ

0

0 0

L

6Ely

4Ely

0

0

0 0

L2

###### L

6Elz

4Elz

---

0 0 0

0

L2

L

![image 246](Matrix Analysis of Framed Structures_images/imageFile246.png)

3.6 Formalization of the Stiffness Method 157

This matrix is the inverse of the flexibility matrix in Eq. (2-23), and the notation is the same as before.

OM5t

YM

°M2t

CD

~~-!M4 XM

/~i

I~ LOM6/ ~I

OM3/ k

ZM

(a)

tSM22

~ ~~" ~ ~~

SM62

###### I I

(b) (e)

~5-=;7>'_""_____=-___~__-=-j~;3/1 ~r

###### ~'~S;44

A(

/sM33 (e)

(d)

----- j""

7

SM66

(0 (g)

Fig. 3-18. Stiffnesses for space frame member.

3.6 Formalization of the Stiffness Method. As with the flexibility method, it is possible to assemble the stiffness matrix for a framed structure from the contributions of individual members by a formal matrix multiplication procedure. The principle of virtual work (see Sec. 1.14) will be used for this purpose, assuming that all loads (actual or equivalent) are applied at the joints. While this approach is not computationally efficient, the reader should benefit from studying this material because it provides a good

![image 247](Matrix Analysis of Framed Structures_images/imageFile247.png)

158 Chapter 3 Fundamentals of the Stiffness Method

background for the more direct method of assembling the stiffness matrix described in the next chapter.

From the preceding section, the stiffness matrix SMi for an individual member i relates the end-actions AMi to the corresponding end-displacements DM; by the expression

(3-22)

It should be recalled that the actions in AMi were chosen to be those at the k end of the member, and the vector DMi contains the relative displacements of the k end with respect to the jend. If Eq. (3-22) is repeated for all ofthe members in a structure, the expression becomes

AMI SMI 0 0 0 0 OM! AM2 0 SM2 0 0 0 OM2 AM3 0 0 SM3 0 0 OM3

(3-23)

AMi 0 0 0 Sm; 0 OM; AMm 0 0 0 0 SMm OM In

where m is the number of members. In more concise matrix notation, Eq. (3-23) may be written as

(3-24)

The symbol SM represents the diagonal matrix of submatrices SM; appearing in Eq. (3-23), and it is called the unassembled stiffness matrix for the whole structure. Furthermore, the vectors AM and OM in Eq. (3-24) contain the end-actions AM; and relative end-displacements OMi for all of the members in the structure. For a beam type of structure there will be 2m items in each of these vectors, and the matrix SM will be of order 2m x 2m. If the structure is a grid, the order of SM will be 3m x 3m. and so on for other types of structures.

An essential step in the present method is to determine the effects of joint displacements for all of the members in the restrained structure. For this purpose a vector ofjoint displacements OJ for the whole structure will be introduced. This vector contains free (but unknown) joint displacements OF listed first and known restraint displacements OR at the supports listed second. The former displacements are those that are free to occur in the actual structure, whereas the latter displacements are specified as boundary conditions. If there are no support displacements specified in a given problem, all of the terms in OR will be zero. When the effects of the joint displacements (in OJ) upon the member displacements (in OM) are cast into matrix form, the result is

###### OM =CMJOJ = [CMF CMR] [~:J (3-25)

The symbol CMJ in this equation represents a displacement transformation

![image 248](Matrix Analysis of Framed Structures_images/imageFile248.png)

3.6 Formalization of the Stiffness Method 159

matrix relating DM to DJ for the restrained structure. The elements of CMJ are determined from compatibility considerations; so it is referred to as the compatibility (or kinematics) matrix. This array is partitioned column-wise into submatrices CMF and CMR, which relate DM to DF and DR, respectively. Each column in the submatrix CM~ contains the member displacements caused by a unit value of an unknown joint displacement in the restrained structure. Similarly, each column in the submatrix ClVlR consists of member displacements due to a unit value of a support displacement in the restrained structure. For completeness, terms in CMR are developed for all support restraints, regardless of whether support displacements are zero or nonzero.

Next, consider an arbitrary set of small virtual displacements to be induced at all of the joints of the structure, including the points where it is supported. As with the vector D), let the first part of oD) contain virtual free displacements oDF; and let the second part consist of virtual support displacements oDR• The resulting virtual member end-displacements ODM can now be written in terms of oD) and its parts, as follows:

ODM = CI>UoDJ = [CMF C~IRJ [~g:] (3-26)

The compatibility matrix C~u in this equation is the same as that in Eq. (3-25).

The external virtual work 0 W generated by the real joint actions A" and the virtual joint displacements oD., takes the form

oW = AIoD.! = [Al At;] [~~:] (3-27)

in which the symbols AF and AR denote the parts of AJ corresponding to the free and restrained displacements, respectively. Similarly, the internal virtual work 0U of the real member end-actions AM and the virtual relative end-displacements ODM may be stated as

(3-28)

According to the principle of virtual work, expressions (3-27) and (3-28) must be equal. Thus,

(3-29)

When Eqs. (3-24), (3-25), and (3-26) are substituted into the right-hand side of Eq. (3-29), the result is

(3-30) Cancelling the arbitrary vector oDJ and transposing Eq. (3-30) yields

A.! = S.rD.! (3-31) where

(3-32)

![image 249](Matrix Analysis of Framed Structures_images/imageFile249.png)

160 Chapter 3 Fundamentals of the Stiffness Method

Thus, the matrix SJ can be identified as the joint stiffness matrix relating the actions AJ to the displacements OJ in Eq. (3-31). It is formed by the congruence transformation in Eq. (3-32), using the CMJ matrix as the postmultiplier of SM and the transposed matrix Cl'1J as the premultiplier. In this manner the unassembled stiffness matrix SM is transformed to the assembled stiffness matrix SJ for all of the joints in the structure.

It is useful to partition the joint stiffness matrix SJ into submatrices pertaining to the free joint displacements OF, the support displacements DR, and their corresponding actions, AF and AR. Thus, the expanded form of Eq. (3-31) is

(3-33)

where

SFR = C~F SM CMR SRR = C~R SM CMR

SFF = C~F SM CMF SRF = C~RSM CMF

Each of the submatrices SFF, SFR, SRF, and SRR is obtained by a congruence transformation, using as operators CMF and CMR (the two parts of CMJ from Eq. 3-25). At this point it can be seen that the submatrix SrF relates the joint actions AF to the free joint displacements OF. Therefore, it must be the same as the stiffness matrix S (without subscripts) discussed in previous sections. Such correlations with earlier material will be taken up in detail after all steps in the formalized approach have been covered.

The free joint displacements OF and the support reactions AR constitute the unknowns in Eq. (3-33). For convenience in solution, this equation will be rewritten as two separate matrix equations:

AF = SFFDF + SFRDR AR = SRFDF + SRR DR

- (3-34a)
- (3-34b)


The first of these equations may be solved (symbolically) for the unknown joint displacements, as follows:

(3-35)

This expression represents the key step in the analysis, because the other quantities of interest have already been formulated in terms of the free displacements OF.

Support reactions may now be calculated from Eq. (3-34b). However, if actual or equivalent joint loads are applied directly to the supports, they should also be taken into account. This may be accomplished by adding their negatives to the results from Eq. (3-34b), as follows:

(3-36)

In this expression the symbol ARC denotes combined loads (actual and equivalent) applied directly to the supports.

A formula for member end-actions caused by joint displacements can

![image 250](Matrix Analysis of Framed Structures_images/imageFile250.png)

3.6 Formalization of the Stiffness Method

161

be obtained by substituting Eq. (3-25) into Eq. (3-24), yielding

(a)

AM = SMDM = SMCMJDJ

The form of this expression shows that the calculations proceed memberby-member, using the compatibility conditions in matrix CMJ and individual member stiffnesses in SM' The member end-actions computed from Eq. (a) must be added to any initial fixed-end actions that may exist. Therefore, the final expression for AM (in expanded form) becomes

(3-37)

in which AML is a vector of fixed-end actions due to loads applied to the members.

Equations of the stiffness method developed by superposition principles in previous sections will now be correlated with similar expressions derived here by virtual work. The comparable equations for calculating unknown joint displacements (including the effects of support displacements) are

(3-11)

modified

and

(3-35)

repeated

It is evident that D = DF, S= SFF' AD - ADL = AF, and ADR = SFRDR

(note the use of stiffness coefficients to obtain ADR). In either case the last term within the parentheses represents equivalent joint loads due to support displacements.

Comparable equations for determining support reactions are

(3-15)

modified

and

(3-36)

repeated

Thus, ARL = -ARC, ARD = SRF, and ARR = SRRDR(note the use of stiffness coefficients to obtain ARR)'

In addition, the comparable equations for obtaining member endactions are

(3-14)

modified

and

(3-37)

repeated

![image 251](Matrix Analysis of Framed Structures_images/imageFile251.png)

162 Chapter 3 Fundamentals of the Stiffness Method Hence, AMD = SMCMF and AMR = SMCMRDR(note the use of member stiffnesses and compatibility conditions to obtain AMD and AMR)·

In summary, formalization of the stiffness method leads to the concept of the assembled stiffness matrix SJ for all of the joints in the structure. It is partitioned into submatrices associated with unknown joint displacements DF and specified support displacements DR (see Eq. 3-33) as well as their corresponding actions. By this approach the calculation of support reactions and the effects of support displacements are automatically included within the basic formulation. Consequently, there is extensive use of stiffness coefficients associated with the supports.

To be selective in the formalized version, the analyst may omit columns of the CMR matrix corresponding to zero values of support displacements. Of course, if all such displacements are zero, the CMR part of the compatibility matrix can be omitted altogether. However, this would preclude the calculation of support reactions by Eq. (3-36) because the matrix SRF (as well as SFR and SRR) would not be generated.

Example 1. Figure 3-19a shows a continuous beam that was analyzed previously by the flexibility method (see Example 2 in Sec. 2.7). Equivalent joint loads for this problem appear in Fig. 3-19b, which illustrates the restrained structure. ~n another figure of the same type (Fig. 3-19c), the six possible joint displacements are indicated. Two of these displacements (DF1 and Dn) are free to occur, while four of them (DR1 through DR4) are restrained. One of the latter displacements is specified to be nonzero (DR3 = 5), but the others are all zero.

Stiffness matrices for the individual members of this continuous beam are found by Eq. (3-17) to be

###### 2EI [ 12 -6L ] S,II = 2SM2 = U -6L 4U

With these arrays as submatrices, the stiffness matrix SM for the unassembled structure becomes

- o 0]
- o 0


12 -6L

S = 2EI -6L 4L2 M V 0 0

[

o 0 -3L6 -3L2U

- as given by Eq. (3-23). Figures 3-19d through 3-19i illustrate the six conditions of unit displacements


required to generate the 4 x 6 compatibility matrix CMJ for the restrained structure. In order to show clearly the meaning of each term in CMJ, it will be partitioned rowwise as well as column-wise. Thus,

0 0 1-1 -L 1 0]

C - [ClF

~::] = ~-1--61--6--~~---~f-~-

MJ - C2F [

-I 1 I 0 0 0 0

in which the SUbscripts 1 and 2 refer to member numbers. Terms in the first column of CMJ are the displacements at the k ends of members 1 and 2, relative to their j ends, due to the condition DFI = 1. From Fig. 3-19d it is easy to see thatfor member

![image 252](Matrix Analysis of Framed Structures_images/imageFile252.png)

3.6 Formalization of the Stiffness Method 163

(a)

###### t2P VP r

A~ ~B ~c

###### h hL hL

3 9 9

(b)

tOR1 =0 t°R3=1) tOR4=0

###### A~ :)B ~c

/ /

###### °R2=0 °F1 °F2

(c)

DF2 =l~r

###### OF1=1~1 _----'1=:11)L

~ ~

~j~k~ ~

(d) (e)

(0 (g)

(h) (i)

Fig. 3-19. Example 1: Continuous beam.

1 the translation and rotation of the k end, relative to the) end, are zero and unity, respectively. However, it is not obvious that for member 2 the translation and rotation of the k end, relative to the} end, are -L and -I, respectively. As an aid to understanding this subtle point, a dashed line i~ drawn tangent to the} end of member 2 in Fig. 3-19d. Then it is seen that the translation of the k end, relative to the} end, is equal to -(1)L. In addition, the rotation of the k end of member 2, relative to its) end, is equal to -I. Terms in the other five columns of CMJ can be obtained from Figs. 3-1ge through 3-19i in a similar manner.

![image 253](Matrix Analysis of Framed Structures_images/imageFile253.png)

###### 164 Chapter 3 Fundamentals of the Stiffness Method

The joint stiffness matrix SJ for the assembled structure is found from Eq. (3-32) to be

###### 6L2 V: 6L 2V -3L -3L

__~:__J_~~1___~____9___)_~__=}b_

6L 0 12 6L - 12 0

S CT S C [SFF SFRJ 2£1

###### J = MJ M MJ = SRF SRR = V 2V 0: 6L 4V -6L 0 -3L 3L: -12 -6L 18 -6 -3L -3L: 0 0 -6 6

Then Eq. (3-35) provides the solution for the joint displacements as

DF = SFf!(AF - SFRDR)

-3L -3LJ [g])

###### ~2;El[ -~ -i] (P.'[~]

3L -3L 8o

= [~J is~~ + [ -~] I~~

In addition, the support reactions (see Eq. 3-36) are given by

###### AR = -ARC + SRFDF + SRRDR

= _[-- Ll32]p + 2£1 [ 6L2V - 3 U -3L - 1 -3L

###### 12 6L -12

###### + 2£1 6L 4V -6L

[

U -12o -6L0 -618

###### =[1]1:.+ [=i~L] 6£18

10 3 63 llU

2 -22

Finally, the member end-actions are obtained from Eq. (3-37), as follows:

###### AM = AML + SM(CMFDF + CMRDR)

=[-j~] ~+SM[-1 ~] ([~J is~1+[-~] I~~)

###### -2L -I I

###### +SM[-~ ~! -i ~] [~]

o 0 0 0 0

_[-~] 1:. [-ici~L] 12£18

- o2 3 + -10555L llU

The parts of this solution due to the applied loads in Fig. 3-19a are the same as those found previously by the flexibility method in Sec. 2.7.

![image 254](Matrix Analysis of Framed Structures_images/imageFile254.png)

3.6 Formalization of the Stiffness Method 165

Example 2. A plane truss is to be analyzed for the vertical load and the horizontal support displacements shown in Fig. 3-20a. Of the eight possible joint displacements in this example, only the x and y translations at point A (denoted by DFJ and DF2) are free to occur, while all others are restrained. To be selective in

![image 255](Matrix Analysis of Framed Structures_images/imageFile255.png)

###### I

Y

###### A( (0

-1

I0cr------=-~0

___ x

###### c

I~--- L-----~

![image 256](Matrix Analysis of Framed Structures_images/imageFile256.png)

(a)

![image 257](Matrix Analysis of Framed Structures_images/imageFile257.png)

(el

(b)

![image 258](Matrix Analysis of Framed Structures_images/imageFile258.png)

![image 259](Matrix Analysis of Framed Structures_images/imageFile259.png)

(d) (el

Fig. 3-20. Example 2: Plane truss.

![image 260](Matrix Analysis of Framed Structures_images/imageFile260.png)

166 Chapter 3 Fundamentals of the Stiffness Method the analysis, the only support reactions that will be determined are the horizontal forces at points Band D, corresponding to the specified support displacements DR! = DR2 = a.

Cross-sectional areas of members 1through 4 are equal to A, whereas those for

members 5 and 6 are equal to vlzA. Therefore, the axial stiffnesses ofall members

(Eq. 3-18) are EAIL, and the unassembled stiffness matrix (Eq. 3-23) is

###### EA

SM = LIs where the symbol Is denotes an identity matrix of order 6.

The four conditions needed for a 6 x 4 compatibility matrix appear in Figs. 3-20b through 3-20e. Hence, for this restrained structure,

-1 0 1 0

0 0 0 1 CMJ = [CMF CMR] = 00 01 00 00

-1Iv1z lIVZ 0 lIVZ 0 0 lIVZ 0

where each row pertains to a different member. Then the assembled stiffness matrix (Eq. 3-32) is found to be

3 -1: -2 -)]

SJ = C~JSMCMJ = [~::: ~::J = ~1 ~~----~-t--~ --J

[

-1 1 I 0 3

The remainder of the solution is straightforward. First, Eq. (3-35) produces the free joint displacements

DF = SF"J(AF - SFRDR)

= 4EAL [ 31 31] ([ - P0 ] - EA2L [-02 - 11] [1]1 a)

###### = [=n :e~ +[6] a

Next, Eq. (3-36), with ARC = 0, gives the support reactions

AR = SRFDF + SRRDR

###### = ~1[=i ~]( [=n:e~+[6]a)+~1 [~

###### = [-n~+U] ~~a

Last, Eq. (3-37), with AML = 0, yields the member end-actions AM = SM(CMFDF + CMRDR)

-) 0 1

0 1 0

- 0 0 0

= SM

- 0 1 0 0 0 0


([=~J:e~ +[6]a)+SM 0

UJa

-I/VZ lIVZ 0 I/V2 0 0 lIVZ 0

= {I, 0, -3,0, -VZ, 0}P14 + {O, 1,0,0,0, lIvZ}EAaIL

![image 261](Matrix Analysis of Framed Structures_images/imageFile261.png)

3.6 Formalization of the Stiffness Method 167

Thus, only members I, 3, and 5 are stressed by the load; and only members 2 and 6 are stressed by the support displacements.

Example 3. The third example consists of a rectangular plane frame with prismatic members, subjected to a lateral force P, as shown in Fig. 3-2Ia. There are no support displacements, and axial strains in the members are to be neglected. For members 1,2, and 3 the j ends are taken to be at points A. C, and D. respectively. To be selective in this example, only the joint displacements and the member endactions (at the k ends) will be determined. Support reactions at points C and D will be the same as the end-actions at thej ends of members 2 and 3.

When axial strains are neglected in a plane frame member, its stiffness matrix is the same as that for a beam member (see Eq. 3-17). Therefore, the member stiffness matrices for this problem are

£1 [3 -3L]

EI [ 12 -6L ] S,,12 = SM3 = L3 -6L 4L2

SMI = V -3L 4U

(Note that the flexural rigidity and the length of member I are double those of members 2 and 3.) Then the unassembled stiffness matrix (Eq. 3-23) becomes

3 -3L 0 0 0 0 -3L 4L2 0 0 0 0

£1 0 0 12 -6L 0 0 L3 0 0 -6L 4U 0 0

SM

0 0 0 0 12 -6L 0 0 0 0 -6L 4U

Figures 3-21b, c, and d show the three displacement patterns required to generate the compatibility submatrix CM~ for the restrained structure. Thus, for the displacements indicated,

-2L 0 0

###### [C,,]

---1----------1 -------0 CMF = C2F

- 0 0 -I
- 1 0 0


C3F - - -------- - - - - - ----

###### 0 0 -I 0 0

which is partitioned row-wise according to members. The assembled stiffness submatrix SFF (see Eq. 3-33) can now be determined as

###### 3L3L]

12

The solution for free joint displacements (Eq. 3-35) involves no support movements. Therefore, the results are simply

133 -3L]-3L [0]0 = [-3]-3 --PV

L [ 13

OF = SvtAF = -- - 3

84EI - 3L

###### 3L 5V P 5L 84£1

Similarly, member end-actions (Eq. 3-37) depend only upon the values of OF, as follows:

AM = SMCMFDF = SM{6L, 0, -5L, -3, -5L, -3}PV/84EI

= {3, -3L, -7,3L, -7,3L}PI14

![image 262](Matrix Analysis of Framed Structures_images/imageFile262.png)

168 Chapter 3 Fundamentals of the Stiffness Method

pi~~~--------------2~t---------------'·18

~ CD -----.

###### Et@ L

----------x

D

(a)

(b) (e)

(d)

Fig. 3-21. Example 3: Plane frame (flexural effects only).

These values, together with principles of static equilibrium applied to members 2 and 3, are sufficient to determine the reactions at points C and D.

Problems

The problems for Sec. 3.3 are to be solved by the stiffness method using Eqs. (3-6) to (3-8). Assume all actions and displacements are positive either to the right. upward, or counterclockwise. unless stated otherwise.

![image 263](Matrix Analysis of Framed Structures_images/imageFile263.png)

Problems 169

- 3.3-1. Find the reactions for the beam AB shown in Fig. 3-1a. The beam carries a uniform load of intensity II' and has constant flexural rigidity EI. The reactions are to be taken in the following order: (1) the force at support A, (2) the moment at support A, and (3) the force at support B.
- 3.3-2. Find the end-actions for member AB of the beam shown in Fig. 3-1a if, instead of the uniform load, the beam is subjected to a vertical, downward, concentrated force P at the midpoint. The beam has constant flexural rigidity EI, and the end-actions are to be taken in the following order: (1) the shearing force at the lefthand end, (2) the moment at the left-hand end, and (3) the shearing force at the right-hand end.
- 3.3-3. Find the reactions for the beam AB shown in the figure. The beam has a fixed support at end A and a guided support at end B, and is subjected to two concentrated loads acting at the positions shown. Assume that the beam has constant flexural rigidity EI. The reactions are to be taken in the following order: (1) and (2), the vertical force and moment, respectively, at support A; and (3), the moment at support B.


~A r r

###### I--L/3-+-L/3-+-L/3--1

Prob. 3.3-3.

3.3-4. Analyze the two-span beam shown in Fig. 3-2a if P1 = P, M = PL, P2

0, and P3 = O. Assume that members AB and BC have lengths Land 1.5L, respectively, and that the flexural rigidity EI is constant for both spans. Determine end-actions for the members as follows: (1) the shearing force at end A of member AB, (2) the moment at end A of member AB, (3) the shearing force at end B of member BC, and (4) the moment at end B of member Be. Determine reactions for the structure as follows: (1) and (2), the forces at supports Band C, respectively. The unknown displacements are to be numbered from left to right along the beam.

3.3-5. Analyze the beam ABC shown in Fig. 3-5a if P1 = 3P2 = P. Assume that the lengths of members AB and BC are Land 2L, respectively, and that the loads P 1 and P2 act at the midpoints of the members. Also assume that the flexural rigidity El is constant for both spans. Determine the following end-actions for the beam: (1) the shearing force at the left-hand end of member AB and (2) the moment at the left-hand end of member AB. Determine the following reactions: (1) the force

- at support Band (2) the moment at support e. The unknown displacements are to


be numbered from left to right along the beam.

3.3-6. Analyze the three-span beam shown in the figure if Ll = L2 = L3 = L, P1 = P, P2 = P3 = 0, M = 0, and wL = P. The flexural rigidity EI is constant for all members. Determine the following end-actions: (1) and (2), the shearing force and moment, respectively, at the left-hand end of member AB; (3) and (4), the shearing force and moment, respectively, at the right-hand end of member AB. Determine the following reactions: (1) and (2), the forces at supports Band C,

![image 264](Matrix Analysis of Framed Structures_images/imageFile264.png)

170 Chapter 3 Fundamentals of the Stiffness Method respectively. The unknown displacements are to be numbered from left to right along the beam.

###### I--L1 -I- L2 -I- L3--J

Prob. 3.3-6 and Prob. 3.3-7.

- 3.3-7. Analyze the three-span beam in the preceding problem if LI = L3 = L, L2 = 2L, PI = P2 = P3 = p, M = PL, and wL = P. The flexural rigidity for members AB and CD is EI and for member BC is 2EI. Determine the end-moments for all members, numbering the six actions consecutively from left to right. Also, determine reactions as follows: (1) and (2), the forces at supports Band C, respectively. The unknown displacements are to be numbered from left to right along the beam.
- 3.3-8. Obtain the stiffness matrix S for the continuous beam shown in the figure, assuming that the beam has constant flexural rigidity EI. The unknown displacements are to be numbered consecutively from left to right along the beam.


A B C 0

A 4¥ ~ ~

\--L -II' 2L ·1· L-1

Prob. 3.3-8.

- 3.3-9. Solve the preceding problem for the beam of Prob. 2.3-5.
- 3.3-10. Solve Prob. 3.3-8 for a continuous beam on simple supports having five

equal spans.

- 3.3-11. Obtain the stiffness matrix S for the beam shown in the figure, assuming


that it has constant flexural rigidity EI. The unknown displacements are to be numbered from left to right along the beam with translation preceding rotation when both occur at the same joint.

###### ~A B C 0

###### l--L--",""""I·~~ L-+L/"4\2J

Prob. 3.3-11.

3.3-12. Obtain the stiffness matrix S for the beam shown in the figure, assuming that the flexural rigidity of the middle span is twice that of the end spans. The unknown displacements are to be numbered from left to right in the figure.

~A B C o~

EI ~ 2EI ~ EI

I--L-+-L--I--L--l

Prob. 3.3-12.

![image 265](Matrix Analysis of Framed Structures_images/imageFile265.png)

3.3-13. Obtain the stiffness matrix S for the four-span continuous beam shown in the figure if LI = L4 = L, L2 = L3 = 1.5L, Ell = EI4 = EI, and EI2 = EI3 = 2EI. The unknown displacements are to be numbered from left to right along the beam.

###### A BCD E

A El, ~ El2 ~El3~ El4 ~

###### I-L,-+-L2-+-L3+-L4--1

Prob. 3.3-13.

3.3-14. Find the reactions at the supports A and C for the beam with fixed ends shown in the figure. Assume that EII = 2EI and EI2 = EI. Number the reactions in the following order: vertical force at A, moment at A, vertical force at C. and moment at C. (Hint: Perform the calculations by considering AB and BC as separate members of the structure.)

r r:8 c,

EI, El2

###### ~L/2+L/2+--L---j

Prob. 3.3-14.

3.3-15. Calculate the translations D, and D2 of joint B in the plane truss (see figure), where the axial rigidity EA is the same for all members. The loading consists of the dead weights of the members. (Let IV = weight per unit length of each member.)

###### I

c 1

3L

3L

A

###### ~4L

Prob. 3.3-15.

3.3-16. For the plane truss in the figure, determine the translations D, and D2 at joint B. A uniformly distributed loading of intensity 2PlL per unit length is applied normal to member AB. Note that each member has a cross-sectional area proportional to its length.

![image 266](Matrix Analysis of Framed Structures_images/imageFile266.png)

172 Chapter 3 Fundamentals of the Stiffness Method

###### I

###### 3L

###### ~4L----~.+I~.----4L----~

Prob. 3.3-16.

3.3-17. Solve for the translations D, and D2 of joint B for the plane truss in the figure, where the loading consists of the dead weights of the members. Let w = weight per unit length of each member having axial rigidity EA. Note that member AB has axial rigidity 2EA and weight 2w per unit length.

"I

3L

t-~

###### L

~~-£A

Prob. 3.3-17.

3.3-18. Find the axial forces in all members of the truss shown in the figure. The truss is subjected to a horizontal force P at joint A. Omit the weights of the members from the analysis. Each member has length L and axial rigidity EA. Assume that tensile force in a member is positive, and use the numbering system shown in the figure.

Prob. 3.3-18.

3.3-19. Calculate the axial forces in all members of the truss due to the force P only (see figure), assuming that EA is the same for all members. Assume that tensile

![image 267](Matrix Analysis of Framed Structures_images/imageFile267.png)

forces are positive, and use the numbering system shown in the figure. (Hint: Because of the symmetry of the structure and loading, there is only one unknown joint displacement.)

p

A

###### f

###### L

###### oj

I--L .1. L----..j

Prob.3.3-19.

- 3.3-20. Solve the preceding problem if, in addition to the force P, the weights of all members are included in the analysis. Assume that each member has weight w per unit length. Calculate the axial forces at the upper ends of the members.
- 3.3-21. Find the axial forces in all members of the truss for Prob. 3.3-19 if there is a horizontal force P acting to the right at joint A (in addition to the upward force P). Assume that EA is the same for all members. Omit the effects of the weights of the members.
- 3.3-22. Find the axial forces in the members of the truss shown in the figure if all members have the same length L and the same axial rigidity EA. The angles between the members are 45 degrees, and the load P makes an angle of 45 degrees with member 5, which is horizontal. Omit the effects of the weights of the members.


Prob. 3.3-22.

3.3-23. Calculate the horizontal and vertical reactions at the supports of the truss shown in the figure due to the weights of the members. Number the six reactions

- in a counterclockwise order around the truss beginning at joint A, and take the horizontal reaction before the vertical reaction when both occur at the same support. Each member has the same axial rigidity EA and the same weight w per unit length.


Prob. 3.3-23.

![image 268](Matrix Analysis of Framed Structures_images/imageFile268.png)

3.3-24. Construct the stiffness matrix S for the truss shown in the figure. All members have the same axial rigidity EA. Number the unknown joint displacements

- in a counterclockwise order around the truss beginning at joint B, and take the horizontal displacement before the vertical displacement when both occur at the same joint.


Prob. 3.3-24.

- 3.3-25. Obtain the stiffness matrix S for the truss shown in Fig. 2-5a, assuming that all members have the same axial rigidity EA. Number the joint displacements in a counterclockwise order around the truss beginning at joint D, and take the horizontal displacement before the vertical displacement when both occur at the same joint.
- 3.3-26. Obtain the stiffness matrix S for the truss of Prob. 2.3-10 if the axial rigidity for the vertical and horizontal members is EA and for the diagonal members is 2EA. Number the joint displacements as described in the preceding problem, but begin with joint E.
- 3.3-27. The figure shows a plane frame with flexural rigidities of 2El and El in members AB and Be. Determine the joint rotations D J and D2 at points Band C, omitting axial strains in the members.


A ~---,..a.;"----.,.,

Prob. 3.3-27.

3.3-28. Calculate the joint rotations DJ and D2 at points Band C of the plane frame shown in the figure. All members have flexural rigidity El, and axial deformations are to be disregarded.

![image 269](Matrix Analysis of Framed Structures_images/imageFile269.png)

###### Problems

175

1

L

~

A

Prob. 3.3-28.

3.3-29. Solve for the rotations D J and D2 at joints Band C of the plane frame in the figure. Omit axial strains in members, and assume that El is constant throughout.

###### ----1-- ~L ~

Prob. 3.3-29.

3.3-30. The figure shows a plane frame with flexural rigidities -fiEl for member AB and El for members BC and CD. Determine the rotations DJ and D2 of joints Band C, disregarding axial deformations.

B

Prob. 3.3-30.

![image 270](Matrix Analysis of Framed Structures_images/imageFile270.png)

- 3.3-31. Analyze the plane frame shown in Fig. 3-lOa if a clockwise couple M acts at joint B. Omit the load P from the analysis, and consider only flexural deformations, letting L = H. Determine the end-actions and reactions shown in Fig.

- 3-lOb.


- 3.3-32. Find the reactions at joints A and D for the plane frame shown in the figure, considering only flexural deformations. Assume that all members have flexural rigidity EI and that L = 1.5H. Number the reactions in the following order, first for joint A and then for joint D: horizontal force, vertical force, and moment.


Prob. 3.3-32.

3.3-33. Analyze the plane frame shown in the figure, considering only the effects of flexural deformations. Assume that M = 2wL 2, H = L, and that both members have flexural rigidity EI. Determine the following end-actions: (I) the axial force, (2) the shearing force, and (3) the moment at end B of member Be. Also determine the reactions at support C, taking the horizontal force before the vertical force.

Prob. 3.3-33.

- 3.3-34. Obtain the stiffness matrix S for the plane frame of Prob. 2.3-17, considering (a) flexural deformations only and (b) flexural and axial deformations. Number the unknown displacements for part (a) as follows: horizontal displacement of B, rotation of B, and rotation of e. For part (b), number the displacements by taking joint B before joint C, and by taking the displacements at a joint in the following order: horizontal translation, vertical translation, and rotation. Assume that all members have flexural rigidity EI and axial rigidity EA.
- 3.3-35. Obtain the stiffness matrix S for the plane frame of Prob. 2.3-19, considering only flexural deformations. Number the unknown displacements in the same sequence that the joints are labeled.


![image 271](Matrix Analysis of Framed Structures_images/imageFile271.png)

Problems 177

3.3-36. Obtain the stiffness matrix S for the plane frame shown in the figure if only flexural deformations are taken into account. The flexural rigidities for the columns are Ell and for the beams are E12• Number the unknown joint displacements in the following order: (I) horizontal translation of beam AB, (2) horizontal translation of beam CD, (3) rotation of joint A, (4) rotation of B, (5) rotation of C, and (6) rotation of D.

"-------'1

A B

~c------10 +

H

Prob. 3.3·36.

- 3.3-37 Find the reactions at support A for the grid in Fig. 3-12a. The load on the grid consists of the concentrated force P shown in the figure. and both members have the same flexural rigidity El and torsional rigidity GJ. Number the reactions in the following order: (1) force in the y direction, (2) moment about the x axis. and (3) moment about the zaxis. Assume all actions and displacements are positive when their vectors are in the positive directions of the coordinate axes.
- 3.3-38 Find the member end-actions at end C of member BC for the grid in Fig. 3-12a. The only load on the grid is the concentrated force P shown in the figure. and both members have flexural rigidity El and torsional rigidity GJ. Number the end-actions as follows: (1) shearing force in the y direction, (2) bending moment about the x axis. and (3) twisting moment about the z axis. Use the sign convention described in the preceding problem.
- 3.3-39. Determine the displacements D \0 D 2, and D3 at joint B of the grid shown in Fig. 3-12a due only to the weight of the members. Assume that each member has weight w per unit length, and that the rigidities El and GJ are the same for both members.
- 3.3-40 Analyze the grid in Fig. 3-12a if there is a simple support at joint B. The support prevents translation in the y direction but does not offer any restraint against rotation of the joint. The load on the grid consists of the force P shown in the figure, and both members have the same flexural rigidity El and torsional rigidity GJ. Number the unknown displacements in the following order: (I) rotation about the x axis and (2) rotation about the z axis. Determine the reactions at support A. using the numbering system and sign convention described in Prob. 3.3-37.
- 3.3-41. Obtain the stiffness matrix S for the grid of Prob. 2.3-22. All members of the grid have the same flexural rigidity El and torsional rigidity GJ. Number the


![image 272](Matrix Analysis of Framed Structures_images/imageFile272.png)

178 Chapter 3 Fundamentals of the Stiffness Method unknown joint displaceme'.. " in the same sequence that the joints are labeled, taking at each joint the rotation about the x axis before the rotation about the z axis, Assume all displacements are positive when their vectors are in the positive directions of the axes,

3.3-42. Determine the stiffness matrix S for the grid pictured in Prob, 2,3-23, Assume that the members AB, BC, and BD each have length L, flexural rigidity EI, and torsional rigidity G], Number the unknown joint displacements in the same sequence that the joints are labeled, taking the displacements at each joint (when they exist) in the following order: translation in the y direction, rotation about the x axis, and rotation about the z axis, Assume all displacements are positive when their vectors are in the positive directions of the axes,

###### In solving the problems for Sec, 3A, assume that all actions and displacements are positive either to the right, upward, or counterclockwise,

3.4-1. Find the reactions for the beam of Fig, 3-2a, due to a linear temperature gradient such that the lower surface of member AB has a temperature change AT

###### J '

while the upper surface changes AT2, Omit the loads from the analysis, and assume that both members have the same flexural rigidity EI, The depth of member AB is d, and the coefficient of thermal expansion is (x. Take the reactions in the following order: vertical force at A, moment at A, force at B, and force at C.

- 3.4-2. Find the reactions for the beam of Fig. 3-2a if support B is displaced downward a distance S1 and support C is displaced downward a distance S2' Omit the loads from the analysis, and assume that both members have flexural rigidity EI. Take the reactions in the order described in the preceding problem.
- 3.4-3. Determine member end-actions and reactions for the beam of Fig. 3-4a if member BC initially has a sharp bend at the position shown in the accompanying figure (the angle f3 is a small angle). Omit the loads from the analysis, and assume all members have the same flexural rigidity EI. Determine the end-actions andreactions shown in Fig. 3-4b.


###### B P

###### LL------+i-.I~-O.5L---lc

Prob. 3.4-3.

- 3.4-4. Find the end-actions and reactions shown for the beam in Fig. 3-5b if the entire beam has a linear temperature gradient such that the lower surface has a temperature change ATJ, while the upper surface changes AT2• Omit the loads from the analysis. Assume that both members have flexural rigidity EI, depth d, and thermal coefficient (x.
- 3.4-5. Suppose that the beam in Prob. 3.3-14 is subjected to temperature changes of ATJ on the lower surface and AT2 on the upper surface. Let the depths of members AB and BC be d and d/3, and take (X as the temperature coefficient.


![image 273](Matrix Analysis of Framed Structures_images/imageFile273.png)

Problems 179 Calculate the displacements at point B and the end-actions for member AB due only to this condition.

- 3.4-6. If the two-part beam in the figure has temperature changes as shown,

determine the displacements at point B and the end-actions for member Be.

EI 3EI

!:::.Tz 8 !:::.Tz

A C

!:::.T1

~IE

!:::.T1

L L .1

Prob. 3.4-6.

- 3.4-7. Find the rotation at point B on the beam in the figure due to a support


translation AB in the y direction at that point. Then evaluate the reactions at A, B, and e.

Prob. 3.4-7.

- 3.4-8. Solve Prob. 3.3-3 if support A rotates clockwise by an amount (3, in which (3 is a small angle. Omit the loads from the analysis.
- 3.4-9. Determine the vectors A DC and ARC for the beam of Prob. 3.3-6 if, in addition to the loads, the following effects occur: support A is displaced downward a distance s, support D rotates counterclockwise through an angle (3, and the entire beam has a linear temperature gradient (ATI is the temperature change on the bottom and AT2 is the temperature change on the top).
- 3.4-10. Assume that the plane truss of Fig. 3-7a has its temperature increased uniformly by an amount AT. Omitting the loads from the analysis, find the endactions shown in Fig. 3-7b. The coefficient of thermal expansion is a, all members have the same axial rigidity EA and length L, and the angles between the members and the horizontal are 1'1 = 0, 1'2 = 30°, 1'3 = 60°, and 1'4 = 90°.
- 3.4-11. Solve Prob. 3.3-18 if member 2 initially has length L + e instead of L. Omit the loads from the analysis.
- 3.4-12. Determine the vectors A DC and A MC for the truss of Prob. 3.3-19 if the following effects occur: support C is displaced upward a distance s, and members 1 and 3 have their temperature raised by an amount AT. The coefficient of thermal expansion is a.


![image 274](Matrix Analysis of Framed Structures_images/imageFile274.png)

180 Chapter 3 Fundamentals of the Stiffness Method

- 3.4-13. Detennine the vector ADC for the truss of Prob. 3.3-24, considering the following effects: support A is displaced to the left a distance s, member BC has an initial length L + e instead ofL, and the entire truss has its temperature increased by .l T. The coefficient of thennal expansion is a.
- 3.4-14. Find the vectors ADC and AMC forthe plane frame in Fig. 3-lla if the following effects occur: member AB has its temperature increased unifonnly by an amount .l T, member BC has a linear temperature gradient (.l T, is the temperature change on the left and .l T2 the temperature change on the right), support C is displaced downward a distance s" and support A is displaced downward a distance s2. Assume that both members have the same flexural rigidity EI and axial rigidity EA. Also, assume H = L, the coefficient of thennal expansion is a, and the depth of the members is d. The unknown displacements D and member end-actions AM are to be taken as shown in Figs. 3-11a and 3-lOb, respectively. Omit the load P from the analysis.


![image 275](Matrix Analysis of Framed Structures_images/imageFile275.png)

4

###### Computer·Oriented Direct Stiffness Method

4.1 Introduction. In the preceding chapter the stiffness method was developed initially by superposition of actions for the free displacement coordinates (Sec. 3.2). Then the method was formalized and extended in Sec. 3.6 using the compatibility matrix eMJ and the virtual work concept. With this second approach the complete joint stiffness matrix SJ (for both free and restrained displacements) was assembled by the triple matrix multiplication given as Eq. (3-32). While the formal version is enlightening and well organized, it involves a large and sparse compatibility matrix containing terms that are not easy to evaluate correctly. Neither the generation of this matrix nor the multiplication process for assembly would be suitable for computer programming. A better methodology consists of drawing ideas from both approaches and adding a few computer-oriented techniques to evolve what is known as the direct stiffness method.

The primary objective of this chapter is to further develop the stiffness method into a form that may be readily programmed on a digital computer. In fact, the procedures established in this chapter have their counterparts in the form of flow charts in Chapter 5. In Sec. 4.2 the direct stiffness method is described, and an outline is presented for the purpose of organizing the calculations into a sequence that is conducive to programming. Since member stiffnesses play an essential role in the analyses of all types of framed structures, this topic is treated next in Sec. 4.3. Then other aspects of the direct stiffness method common to all types of framed structures are discussed in Secs. 4.4 through 4.7. These matters are demonstrated with a familiar example that has been solved previously. The remaining sections of the chapter deal with applications to various types of framed structures. For simplicity, only prismatic members and the effects of applied loads are considered in this chapter. Methods for handling nonprismatic members, temperature changes, prestrains, support displacements, and other effects are described in Chapter 6.

4.2 Direct Stiffness Method. The key to simplifying the assembly process for the joint stiffness matrix SJ is to use member stiffness matrices for actions and displacements at both ends of each member. If the member displacements are referenced to structural (global) coordinates, they coincide with joint displacements. In that case all of the geometric complications must be handled locally, and the transfer of member information to

181

![image 276](Matrix Analysis of Framed Structures_images/imageFile276.png)

structural arrays is straightforward. That is, the stiffness matrix and the equivalent load vector can be assembled by direct addition instead of by matrix multiplication.

Thus, the assembly of the joint stiffness matrix, assuming m members, may be stated as

m

SJ = L SMSi

(4-1)

i=1

In this expression the symbol SMSi represents the i-th member stiffness matrix with end-actions and displacements (for both ends) taken in the directions of structural axes. To be conformable for matrix addition, all such member stiffness matrices should be expanded to the same size as SJ by augmenting them with rows and columns of zeros. However, this operation can be avoided in computer programming by merely placing terms from SMSi into SJ where they belong.

Similarly, an equivalent joint load vector AE can be constructed from member contributions, as follows:

m

AE = - L A MSi (4-2)

i=l

In this instance AMSi is a vector of fixed-end actions in the directions of the structural axes at both ends of member i. As before, it is theoretically necessary to augment AMSi with zeros to make it conformable for matrix addition, but this step can be avoided in programming. The equivalent joint loads in Eq. (4-2) will be added to actual loads applied at the joints to form the total (or combined) load vector.

In order to separate terms pertaining to the free displacements of the structure from those for support restraints, it is necessary to rearrange and partition the stiffness and load matrices. This rearrangement of terms may be accomplished after the assembly is completed. However, in a computer program the rearrangement is more easily done when the information is transferred from small member arrays to large structural arrays.*

After the stiffness and load matrices have been rearranged, the solution proceeds in the manner already established in Sec. 3.6. Thus, the basic solution for free joint displacements (see Eq. 3-35), due to loads only, becomes

(4-3)

in which AFC is a vector of combined joint loads (actual and equivalent) corresponding to DF• While it is symbolically convenient to imply inversion ofthe stiffness matrix SFF in Eq. (4-3), it is not efficient to actually calculate

*While it is possible to solve the equations of equilibrium "in-place" without rearrangement (see Appendix E), it is computationally more efficient to separate the independent equations from the dependent equations.

![image 277](Matrix Analysis of Framed Structures_images/imageFile277.png)

4.2 Direct Stiffness Method 183

SF} in a computer program. Instead, the coefficient matrix SFt should be factored and the solution for Dr obtained in forward and backward sweeps. (The topics offactorization and solution are covered in Appendix D.)

Other items of interest consist of support reactions and member endactions. Due to the effects of loads only, Eq. (3-36) gives the reactions

###### (4-4)

In addition, Eq. (3-37) for the member end-actions may be rewritten so that it pertains to only one member at a time, as follows:

###### (4-5)

All of the matrices in this expression are referenced to member axes. The action vector A~IL i contains fixed-end actions (in the directions of member axes) due to loads applied on the member itself. In addition, the member stiffness matrix SM i has terms (in member directions) for both ends of the member. Consequently, the vector DM i must consist of displacements (in member directions) at both ends of the member. These displacements can be obtained by expressing the joint displacements at the j and k ends as components in the member directions.

A computer program for the analysis of a structure by the direct stiffness method divides conveniently into several phases. These phases are not the same as those in Chapter 3 for hand calculations. One difference is that when using a computer it is desirable to work in the early phases of the program with only the data pertaining to the structure. This part of the program includes the formation of the stiffness matrix, which is a property of the structure. Subsequently, the load data is manipulated, after which the final results of the analysis are computed. This sequence is particularly efficient if more than one load system is being considered, because the initial phases of the calculations need not be repeated. The steps to be considered in the subsequent discussions are the following:

- (1) Identification of Structural Data. Information pertammg to the structure itself must be assembled and recorded. This information includes the number of members, the number of joints, the number of degrees of freedom, and the elastic properties of the material. The locations of the joints of the structure are specified by means of geometric coordinates. In addition, the section properties of each member in the structure must be given. Finally, the conditions of restraint at the supports of the structure must be identified. In computer programming, all such information is coded in some convenient way, as will be shown subsequently in this chapter and also in Chapter 5.
- (2) Construction of Stiffness Matrix. The stiffness matrix is an inherent property of the structure and is based upon the structural data only. In computer programming it is convenient to obtain the joint stiffness matrix by summing contributions from individual member stiffness matrices (a


![image 278](Matrix Analysis of Framed Structures_images/imageFile278.png)

- discussion of complete member stiffnesses is given in Sec. 4.3). The joint stiffness matrix to be considered is related to all possible joint displacements, including support displacements, as was discussed in Sec. 3.6. This array shall be called the over-alljoint stiffness matrix. Its formation and rearrangement are described in Secs. 4.4 and 4.6, respectively.
- (3) Identification ofLoad Data. All loads acting on the structure must be specified in a manner suitable for computer programming. Both joint loads and member loads must be given. The former may be handled directly, but the latter are handled indirectly by supplying as data the fixed-end actions caused by the loads on the members.
- (4) Construction ofLoad Vector. The fixed-end actions due to loads on members may be converted to equivalent joint loads, as described previously in Sec. 1.12. These equivalent joint loads may then be added to the actual joint loads to produce a problem in which the structure is imagined to be loaded at the joints only. Formation and rearrangement of the load vector are described in Secs. 4.5 and 4.6, respectively.
- (5) Calculation of Results. In the final phase of the analysis all of the joint displacements, reactions, and member end-actions are computed. The calculation of member end-actions proceeds member by member (see Eq.


- 4-5) instead of for the structure as a whole. Such calculations require the use of complete member stiffness matrices for member directions, a subject that is covered in the next section. A simple calculation of this type is demonstrated for illustrative purposes in Sec. 4.7.


There are many possible variations in organizing the stiffness method for computer programming. The phases of analysis listed above constitute an orderly approach having certain essential features that are advantageous when dealing with large, complicated frameworks. These steps will be discussed and illustrated by means of a familiar example in the following sections.

4.3 Complete Member Stiffness Matrices. In order to construct the joint stiffness matrix with the summation process indicated by Eq. (4-1), it is necessary to generate complete member stiffness matrices SMSi for structure-oriented axes. In addition, member stiffness matrices SMi for memberoriented axes are required for the purpose ofcalculating member end-actions with Eq. (4-5). It is always possible to obtain the member stiffnesses with respect to the member axes, as is done in this section, and then to transform these stiffnesses to the structural axes. The procedures for accomplishing this transformation are described later in the chapter for each type of structure.

In the special case of a continuous beam, the member axes are inherently parallel to those for the structure as a whole; so no transformation is necessary. Thus,

(a)

![image 279](Matrix Analysis of Framed Structures_images/imageFile279.png)

4.3 Complete Member Stiffness Matrices 185

###### YM

Sf r1

2t ta

~~~f-'-J_'_____0::::/_____--,'k~--2 ~ ----xM

~I AI

~ ~c~--------_L------,<-'-2~~

/

Fig. 4-1. Space frame member.

Figure 4-1 shows a prismatic space frame member i that is fully restrained at both ends, which are denoted as ends j and k. Orthogonal member-oriented axes also appear in the figure, with the origin located at point j. The X,H axis coincides with the centroidal axis of the member and is positive in the sense from j to k. The)'.lf and Z;H axes are principal axes for the member; that is, the X,W)'M and X,I1ZM planes are principal planes of bending. It is assumed that the shear center and the centroid of the member coincide so that twisting and bending of the member may occur independently of one another. This restriction is normally satisfied in framed structures; however, it is possible to make a more general analysis if necessary (see Sec. 6.17).

Properties of the member shown in Fig. 4-1 will be defined in a systematic fashion for the purpose of computer programming for complex structures. Let L denote the length of the member and Ax the area of the cross section. (The subscript X is needed because the symbol A without subscript is used as an identifier for actions.) Principal moments of inertia of the cross section of the member with respect to the YM and ZM axes are denoted /y and I z, respectively. Also, let the torsion constant for the member be Ix, which is the same as the constant J that appears in Chapters 2 and 3 and the Appendices. Since the symbol J has use as an index for joints of the structure in computer programming, the use of the symbol Ix for the torsion constant is more desirable. The torsion constant l~ is not to be interpreted as the polar moment of inertia of the cross section except in the special case of a circular cylindrical member.

Member stiffnesses for the restrained member shown in Fig. 4-1 consist ofactions exerted on the member by the restraints when unit displacements (translations and rotations) are imposed at each end ofthe member. Values of these restraint actions may be obtained from Table B-4 in Appendix B.

![image 280](Matrix Analysis of Framed Structures_images/imageFile280.png)

186 Chapter 4 Computer-Oriented Direct Stiffness Method

The unit displacements are considered to be induced one at a time while all other end displacements are retained at zero; also, they are assumed to be positive in the XM, YM, and ZM directions. Thus, the positive senses of the three translations and the three rotations at each end of the member are indicated by arrows in Fig. 4-1. In the figure the single-headed arrows denote translations, and the double-headed arrows represent rotations. At jointj the translations are numbered 1,2, and 3 and the rotations are numbered 4, 5, and 6. Similarly, at the k end of the member 7, 8, and 9 are translations and 10, 11, and 12 are rotations. In all cases the displacements are taken in the order XM, YM, and ZM, respectively.

The member stiffnesses for the twelve possible types of end displacements (shown in Fig. 4-1) are summarized pictorially in Fig. 4-2. In each case the various restraint actions (or member stiffnesses) are shown as vectors. An arrow with a single head represents a force vector, and an arrow with a double head represents a moment vector. All vectors are drawn in the positive senses, but in cases where the restraint actions are actually negative a minus sign precedes the expression for the stiffness coefficient.

In order to see how the member stiffnesses are determined, consider case (1) in Fig. 4-2. The restraint actions shown in the figure arise because ofa unit translation of the j end of the member in the positive XM direction. All other displacements are zero. This displacement causes a pure compressive force EAxlL in the member. At thej end of the member this force is equilibrated by a restraint action of EAxlL in the positive XM direction, and at the k end of the member the restraint action has the same value but is in the negative XM direction. All other restraint actions are zero in this case.

Case (2) in Fig. 4-2 involves a unit translation ofthej end ofthe member in the positive YM direction, while all other displacements are zero. This displacement causes both moment and shear in the member. At thej end, the restraint actions required to keep the member in equilibrium are a lateral force of 12Elz/L3 in the positive YM direction and a moment 6ElzIV in the positive ZM sense (see Table B-4). At the k end of the member the restraint actions are the same except that the lateral force acts in the negative YM direction.

All of the member stiffnesses shown in the figure are derived by determining the values of the restraint actions required to hold the distorted member in equilibrium. The reader should verify all of the expressions before proceeding further. These stiffnesses can be used to formulate stiffness matrices for the members of different types of structures. In the most general case (a space frame), it is possible for the member to undergo any ofthe twelve displacements shown in Fig. 4-2. The stiffness matrix for such a member, denoted SMio is therefore of order 12 x 12, and each column in the matrix represents the actions caused by one of the unit displacements. The space frame member stiffness matrix is shown in Table 4-1; it is, of

![image 281](Matrix Analysis of Framed Structures_images/imageFile281.png)

###### a.,r;.

:!l

###### §i

'"'"~

1:1"

....

###### ""'I

("')

'1:1;-

~

"'"

~

;;-

'"

.,tI>

tI>

o3

3

tI>

tI>

![image 282](Matrix Analysis of Framed Structures_images/imageFile282.png)

###### ---k~XM;!-

###### JIM

###### ------x~~ikM

atj.atj.atj.Fig.4-2.Memberstiffnesses:(1)unittranslation(2)unittranslation(3)unittranslation(4)unitrotationX MVMZMXM

\l",p;'t -6Hz

L •

GI)(-T

t4~IYL2~ly

###### -6~;0~HY

4~ly~hIZ

___k~

L'

###### L

(6!

(4)

I(5)I

MjY

atj.atj.atj.(5)unitrotation(6)unitrotation(Continuedonnextpage.)VMZM

Z/fl

Z/fl

/

/

![image 283](Matrix Analysis of Framed Structures_images/imageFile283.png)

###### X/flE

-~XM--f------+--,

k~XM

###### t-y6El

--,$1t_12ElzL'

1-.1EAX_EAx

###### L'

~JLkL

y/!2El

hlzL'

k~

###### LJ

(3)

(1)

(2)

MjY

Y/fl

Y/fl

t12Elz

I

Z/fl

ZM

![image 284](Matrix Analysis of Framed Structures_images/imageFile284.png)

a

###### ==~

Q.

~

~

;!J

o:;.

6.,;.

Q.

###### ...:I

a

~

1l

###### n=-D)

.,iD

'Il

o

###### -a

no

~

-g

gg

....

.,~

![image 285](Matrix Analysis of Framed Structures_images/imageFile285.png)

###### ~=1-11'"XMk~~__

Fig.4·2.(Continued)(7)Unittranslationatk.(8)unittranslationatk.(9)unittranslationatk.(10)unitrotationatXMYMZMXM

__6Ely.o;r------xM

###### Z'.';71'----

###### f1_~t

.2~hf~4~lr

~tf.L'L'

4~lz/

~3/

###### )/'~pt

(10)ZM

IZM(11)YM

ZM1121

YM

IYM

6Clz

###### /

![image 286](Matrix Analysis of Framed Structures_images/imageFile286.png)

###### -L',/---.fk7~--rl----XM12ElyL'

ll'IN~-XM1_EAx

__-7!l_~_-,-I_';yl'--'./_'~;r

k.(11)unitYrotationatk.and(1 2)unitrotationatk.MZM

~t.12EIZ

ffL'L'.k

t6Clrj.::?

r//'2El

ZML'

(91

(8)

(7)ZM

###### IYM

YM

###### IYM

t6Ely

Z

_12Cl

7

ZM

![image 287](Matrix Analysis of Framed Structures_images/imageFile287.png)

- -030000000
- -IF-IF§iL"L"


LI~

;:;"I6EI%4Elz

'JJ12EI,6EI}.12EI,.6EI,-

a0500000I00uL

12E1z0-..,""200000000L3L'L"U

Table4.](""J

~

""1...

Qo

###### IC

.....

..,LL'

""LL312Elz6EI%

I6Elz2ElzI""0060'"00000IL2LLL'I

0Space Frame Member Stiffness Matrix3

""GI,_GI-A04000000000'"L

"0

###### ""-EA,

[45326789111012

I12Elz_6E/z12E1zz_ 6El

###### +j

6;1,1

###### rL"L22

I-----------------------------------------------+------------------------------------------------=S\li

70000000000

###### 0L'L'VL"

00L

4EI,.,2EI,.6EII_ 6E/,·

4Ell

6El1

###### LLL'L'

000L'LL'

---800000000L3

0000

GI,

0

0

El,12

6EI,.

00000L

6Elz

000

000

_EAx

IEA.,_EA.,

LL

0

I

2Elz

00000

2E1,.

6EI,.

000

_GI,

0

0

_12E/,

6EI,

10000

6Elz

00II

090

012

![image 288](Matrix Analysis of Framed Structures_images/imageFile288.png)

190 Chapter 4 Computer-Oriented Direct Stiffness Method

course, symmetrical. The rows and columns of the matrix are numbered down the side and across the top to assist the reader in identifying a particular element. In addition, the matrix is partitioned in order to delineate the portions associated with the two ends of the member. Thus, the complete member stiffness matrix has the form

SM; = [SMj} SMjkJ

(b)

SMkj SMkk ;

where the SUbscripts j and k attached to the submatrices refer to the ends of the member.

The member stiffness matrices needed for other structures, such as continuous beams and plane frames, are of lesser order than the matrix shown in Table 4-1. This is because only certain of the end displacements shown in Figs. 4-1 and 4-2 are considered in the analyses of such structures. As an example of how such a member stiffness matrix is formed, the stiffness matrix for a member in a continuous beam will now be developed.

Consider one member of a continuous beam between supports denoted asj and k, as shown in Fig. 4-3a. The XM, YM, and ZM axes are taken in the directions shown in the figure, so that the X~YM plane is the plane of bending of the beam. In a member of a continuous beam there are four significant types ofdisplacements that can occur at the ends ofthe member. These displacements are indicated in Fig. 4-3b by the vectors numbered 1 through 4. The corresponding member stiffness matrix is of order 4 x 4 and is shown in Table 4-2. The elements of this matrix are obtained from cases (2), (6), (8), and (12) of Fig. 4-2.

For continuous beam problems in which the supports do not allow translational displacements at joints, only the rotations shown in Fig. 4-3c are possible. In such a case the first and third rows and columns ofSM could be deleted, and the reduced member stiffness matrix would consist of the remaining elements as shown in Table 4-3.

The member stiffness matrix given in Table 4-2 will be used in the anal-

Table 4·2

Prismatic Beam Member Stiffness Matrix

12Elz 6Elz II _12Elz 6EI z

###### L3 V I L3 L2

I

I

6Elz 4Elz II _ 6El z 2Elz

###### I L2 L

I

U L

###### I

###### -----------------------+----------------------

S~i =

I

_12EIz _ 6Elz

I 12Elz _ 6El z L3 U I

I

La L2

- I

6Elz 2Elz

- II _ 6Elz 4Elz


I

###### L2 L I

V L

I

![image 289](Matrix Analysis of Framed Structures_images/imageFile289.png)

~,3 ('umpkte :\Iemher Stiff'ness :\hltril'l's 191

Table 4-3

Reduced Member Stiffness Matrix

###### llllll- ~ ° t ~

/ ~ ~

k

XM

###### / I. L ~I

###### ZM

(0)

###### I"

1t

###### ° t

3

~/ k~ XM

###### /{ /.

###### /

###### /zM

(b)

YM

)!-=--/_----=0=---·-----,i;,~ --xM

###### /. (c)

Fig, 4-3, Continuous beam member.

![image 290](Matrix Analysis of Framed Structures_images/imageFile290.png)

192 Chapter 4 Computer-Oriented Direct Stiffness Method

ysis of continuous beams. Member stiffness matrices for other types of framed structures will be discussed in later sections.

4.4 Formation of Joint Stiffness Matrix. The process of forming the joint stiffness matrix will be explained in conjunction with the two-span beam example shown in Fig. 4-4a. This beam is the same one that was analyzed previously in Chapters 2 and 3, except that no particular loading system is indicated. As before, assume that the flexural rigidity Elz of the beam is constant throughout its length. In order to develop the necessary stiffness terms, consider the unloaded beam to be completely restrained at all joints, as shown in Fig. 4-4b. In this figure an arbitrary numbering system is indicated for the six possible joint displacements that could occur in the structure. The numbers shown will be called joint displacement indexes. At each joint, taken from left to right, the y translation is numbered before the z rotation. Displacements numbered 4 and 6 (rotations at B and C) are actually free to occur, but those numbered I, 2, 3, and 5 are restrained by the supports.

Formation of the joint stiffness matrix SJ is accomplished by summing contributions from the complete member stiffness matrices for members I and 2 (see Eq. 4-1). The pattern of contributions is indicated in Table 4-4 by the two sections of SJ delineated with dashed lines and overlapping in the central portion. The 4 x 4 upper left-hand section receives contributions from the stiffness matrix of member AB (see Table 4-2, Sec. 4.3), and the 4 x 4 lower right-hand section receives terms from the stiffness matrix of member Be. Together, these two member stiffness matrices (which are

y

0) CD

/~A

x

~8 ~c

IE L ~I E L ~I

###### z

(a)

###### 1j

###### 3j

5t

0

0)

###### /~A /~8 /~c

2 4 6

(b)

###### Fig. 4-4. Beam example.

![image 291](Matrix Analysis of Framed Structures_images/imageFile291.png)

4.5 Formation of Load Vector

193

Table 4-4

Joint Stiffness Matrix for Beam of Fig. 4-4b

Member AB

:: 12

###### 6L -12 6L 0 4U -6L 2U 0

0 0

###### I 6L

I

###### -6L 24 0 I -12 2U 0 8U

I

6L : 2U·

S, = ::-12

I

E1x

I

###### 6L

###### I -6L

- - - - , ----~------ -,

###### L"

0 -12 -6L 12 -6L 0 ___ 6!-_____U:"_____~§L 4L~_,

0

0

Member Be

both the same in this example) constitute the joint stiffness matrix for the two-span beam. In the overlapping portion of SJ, elements consist of the sums of contributions from members AB and Be. For example, the element Sm (equal to 24Elz1L3) is the sum of SMD (equal to 12E/zIL3) for member AB plus SMII (equal to 12Elz1L3) for member Be. Similarly, SJ34 (equal to 0) is the sum of SM34 (equal to -6E/zIL2) for member AB plus SMI2 (equal to 6E/zIL2) for member Be. Other elements of SJ outside of the overlapping portion but inside the dashed lines consist of single contributions from either member AB or member Be. Elements of SJ outside of the dashed lines are all zero due to the nature of the structure. Thus, the use of the arbitrary numbering system results in a joint stiffness matrix in which the contributions from member stiffnesses may be clearly seen.

If the stiffness matrix SJ in Table 4-4 is to be useful, the actual degrees of freedom and support restraints for the structure must be recognized. Then the matrix can be rearranged by interchanging rows and columns in such a manner that stiffnesses corresponding to the degrees of freedom are listed first and those corresponding to support restraints are listed second. This rearrangement process will be covered in Sec. 4.6 after the load vector has been discussed.

4.5 Formation of Load Vector. After finding the joint stiffness matrix, the next step in the analysis is to consider the loads on the structure. It is convenient initially to handle the loads at the joints and the loads on the members separately. The reason for doing so is that the joint loads and the member loads are treated in different ways. The joint loads are ready for immediate placement into a vector of actions to be used in the solution, but the loads on the members are taken into account by calculating the fixed-end actions that they produce. These fixed-end actions may then be transformed into equivalent joint loads and combined with the actual joint loads on the structure (see Sec. 1.12 for a discussion of equivalent joint loads).

The loads applied at the joints may be listed in a vector AJ , which contains the applied loads corresponding to all possible joint displacements, including those at support restraints. The elements in AJ are numbered in the same sequence as the joint displacements. For the two-span beam

![image 292](Matrix Analysis of Framed Structures_images/imageFile292.png)

194 Chapter 4 Computer-Oriented Direct Stiffness Method

y

(a)

2P p

###### :L{~f--A~t-B~):L

###### p} tp

- (b)
- (c)


Fig. 4-5. Actual and equivalent joint loads.

example, the arbitrary numbering system is shown in Fig. 4-4b. Ifthis beam is subjected to the loads shown in Fig. 4-5a, the joint loads are the moment M = PL at joint B and the force P at joint C. Therefore, the vector AJ takes the form*

AJ = {O, 0, 0, M, P, O}

The moment M and the force P in the vector AJ are positive because M acts counterclockwise and P acts upward. In general, the joint loads on a continuous beam may be a force and a moment at every joint.

The remaining loads on the structure act on the members and are shown applied to the two members of the restrained structure in Fig. 4-5b. Also shown in this figure are the fixed-end actions at the ends of the members. For convenience, these fixed-end actions shall be compiled into a rectan-

*As mentioned previously, braces { } are used to denote a column vector that is written in a row to save space.

![image 293](Matrix Analysis of Framed Structures_images/imageFile293.png)

4.5 Formation of Load Vector 195

gular matrix AML in which each column contains the end-actions for a given member. Thus, the format of AML will be taken as follows:

AML = [AML1 AML2 ... AMLi ... A MLm] (4-6) In this arrangement each submatrix AML i is a column vector pertaining to a given member i and is ready to be used in Eq. (4-5). The number ofcolumns in AML will always be equal to m, the number of members in the structure.

In a beam there are two significant types of fixed-end actions: shearing force and bending moment. Therefore, each column of the matrix AML will contain for one member the shearing force and bending moment at the left end (the j end), followed by the shear and moment at the right end (the k end). As shown in Fig. 4-5b, the fixed-end actions on member AB consist of the force P and the moment PU4 at the left-hand end accompanied by the force P and the moment - PU4 at the right-hand end. These actions constitute the first column of AML, as follows:

###### AMLI = {P, PU4, P, -PU4}

The second column of A,n. is filled in a similar manner from the fixed-end actions for member Be (see Fig. 4-5b). This column is

###### AML2 = {PI2, PL/S, PI2, -PL/S}

When the fixed-end actions are reversed in direction, they constitute equivalent joint loads, which are assembled in accordance with Eq. (4-2). Since the member axes for a beam are always taken parallel to the structural axes, the following identity holds:

(a)

That is, transformation of member end-actions to structural directions is not required for a beam. Thus, for the two-span example, Eq. (4-2) gives

AE = - {P, PL/4, P, -PU4, 0, O} - {O, 0, PI2, PL/S, PI2, -PUS}

= {-P, -PL/4, -3PI2, PL/S, -PI2, PL/S}

The equivalent joint loads are listed in this vector in the sequence denoted by the arbitrary numbering system in Fig. 4-4b. In addition, the terms in AE are shown in Fig. 4-5c, where it is seen that only the actions at joint B consist of contributions from both members.

Actual joint loads (vector AJ) may be added to equivalent joint loads (vector AE) to produce the vector of combined joint loads Ac, as follows:

(4-7)

Substituting into this expression the terms obtained above for AJ and AE yields

###### Ac = {-P, -PL/4, -3PI2, 9PUS, PI2, PUS}

In the next section this combined load vector will be rearranged in a manner similar to that for the stiffness matrix.

![image 294](Matrix Analysis of Framed Structures_images/imageFile294.png)

196 Chapter 4 Computer-Oriented Direct Stiffness Method

4.6 Rearrangement of Stiffness and Load Arrays. As mentioned previously, the stiffness matrix and the load vector will be rearranged and partitioned so that terms pertaining to the degrees offreedom are separated from those for the support restraints. The beam example in Fig. 4-4a has two degrees of freedom, which are the rotations at points Band C. Figure

- 4-6 shows revised displacement indexes for the joints of the restrained structure. It is seen that the free displacements are numbered before the support displacements. Otherwise, the sequence of numbering is from left to right, with translations taken before rotations at each joint. These revised displacement indexes may be computed automatically by examining the actual restraint condition for each possible joint displacement. If it is not restrained, the displacement index must be reduced by the cumulative number of restraints encountered up to that point. In such a case, the new index is computed as


(j)new = U)old - Cjo (a)

in which Cjo represents the cumulative number of restraints for the old index. On the other hand, if the displacement under consideration is actually restrained, the new index is determined by the formula

(b)

where n is the number of degrees of freedom. Expressions (a) and (b) will be implemented in a formal way later in this chapter (see Sec. 4.9).

For the present example, a comparison of Fig. 4-6 and Fig. 4-4b shows that the actual degrees of freedom correspond to displacements 4 and 6 of the original numbering system. Therefore, the fourth and sixth rows and columns of the joint stiffness matrix SJ must be put into the first and second positions. As the first step, rows 4 and 6 of the matrix in Table 4-4 are switched to the first and second rows while all other rows are moved downward without changing their order. Then the array takes the form shown in Table 4-5. Next, the fourth and sixth columns in Table 4-5 are moved to the first two columns, and all other columns are moved to the right without

y

###### Fig. 4-6. Revised displacement indexes.

![image 295](Matrix Analysis of Framed Structures_images/imageFile295.png)

4.7 Calculation of Results 197

Table 4-5

Joint Stiffness Matrix with Rows Rearranged

###### 6L 2U 0 8U -6L 2U 0 0 6L 2U -6L 4U

###### S.J = 12 6L -12 6L 0 0 Elz 6L 4U -6L 2U 0 0 L'l

-12 -6L 24 0 -12 6L 0 0 -12 -6L 12 -6L

changing their order. This manipulation produces the rearrangedjoint stiffness matrix shown in Table 4-6. Such a matrix is always symmetric and is partitioned in the following manner:

(4-8)

In this expression the subscripts F and R refer to free and restrained displacements, respectively.

Similarly, the combined load vector Ac for the example can be rearranged to conform to the numbering system of Fig. 4-6. In this instance the fourth and sixth terms in Ac are moved to the first and second positions while all others are moved toward the end without changing their order. This rearrangement gives

I

Ac = {9PL/8, PL/8, :-P, -PL/4, -3P/2, P12} which is partitioned in the form

###### Ac = [~::] (4-9)

Thus, the combined loads corresponding to free joint displacements are separated from those corresponding to support restraints.

4.7 Calculation of Results. In the final phase of the analysis, matrices generated in previous steps are used to find unknown joint displacements DF, support reactions AR, and member end-actions AM i for each

Table 4-6

Joint Stiffness Matrix with Columns Rearranged

###### 8U 2U

###### I 6L 2U 0 -6L 2U 4U

I

I

----------------+-------------------------------I 0 0 6L -6L

6L 0: 12 6L -12 0 Elz 2U 0 I 6L 4U -6L 0

S.J =

I L'l

###### 0 6L

I -12 -6L 24 -12

I

I

-6L -6L

I 0 0 -12 12

![image 296](Matrix Analysis of Framed Structures_images/imageFile296.png)

198 Chapter 4 Computer-Oriented Direct Stiffness Method

member. First, the unknown displacements are obtained from Eq. (4-3), which gives for the two-span beam

###### -IJ [9J P L P U [17J

__\ _ L [ 2 OF - SFFAFc - 14Elz -1

###### 4 1""""8 = 112Elz -5

Next, the support reactions are found by substituting the matrices ARC, SRF, and OF into Eq. (4-4). This substitution for the example yields the following results:

##### A=P[1]+2EIzII ~l[17J P U =.!...l;~l]

R 4 6 V ° 3 -5 112Elz 56 69

-2 -3 -3 -64 The values of the displacements and the reactions given above are the same

- as those obtained previously in Sec. 3.2. In order to calculate member end-actions by Eq. (4-5), it is necessary to


set up m displacement vectors OM; (i = 1, 2, ... , m), each of which contains displacements of the ends of member i in the directions ofmember axes. At this stage of the analysis, all joint displacements are known and can be used to fill each of the vectors OM; in some systematic way. For two- and three-dimensional structures, a transformation of such displacements from structural directions to member directions is required. However, in a beam this difficulty is not encountered. That is,

(a)

where the identifier OMSi represents the vector of displacements at the ends of member i in the structural directions. For the beam example the displacements at the ends of member AB are

OM! = {O, 0, 0, 17}PV/112Elz and those for member BC are

###### OM2 = {O,17,0, -5}PV/112Elz

The order in which the displacements are listed in these vectors follows the pattern given in Fig. 4-3b.

Having the above vectors on hand, one may then apply Eq. (4-5) twice (once for each member) in order to evaluate the final end-actions for members AB and BC. In both applications the member stiffness matrix SM; is the same and is given in Table 4-2 (see Sec. 4.3). Thus, the end-actions become

###### P [ L4] [ 0] PV P [31L107]

AM! =AML! +SM10Ml ="4 4 +SM! ° 112Elz=56 5 -L 17 20L

![image 297](Matrix Analysis of Framed Structures_images/imageFile297.png)

4.8 Analysis of Continuous Beams 199

and

A\12.,= AM!2 +SM2DM2 = -8 4 +SM2 ° ---112EIz = -56 - 8 -L -5 °

p L 17 PP P 36L

###### r 4J r °1 r

###### 1

64

It should be evident that these end-actions could also be used to compute support reactions as an alternative to using Eq. (4-4).

The above calculations may appear at first to be unnecessarily extensive and cumbersome, and indeed they are for the small structure used as an example. Their virtue, however, lies in the fact that they represent an orderly procedure that can be readily programmed for a digital computer. Other efficiencies not conducive to hand calculations will be seen in the computer programs of the next chapter.

4.8 Analysis of Continuous Beams. The continuous beams to be discussed in this section are assumed to consist of prismatic members rigidly connected to each other and supported at various points along their lengths. The joints of a continuous beam will be selected normally at points of support and at any free (or overhanging) ends. However, in those cases where there are changes in the cross section between points of support, so that the member consists of two or more prismatic segments, it is always possible to analyze the beam by considering a joint to exist at the change in section. This technique of solution will be illustrated in the example of the next section. Another method of analyzing a beam with changes in section, and which does not require the introduction of additional joints to the structure, is described later in Sec. 6.12.

A continuous beam having m members and m + 1 joints is shown in

- Fig. 4-7a. The x-y plane is the plane of bending of the beam. The members are numbered above the beam in the figure, and the joints are numbered below the beam. In each case the numbering is from left to right along the beam. The central part of Fig. 4-7a shows the i-th member framing at the left end into a joint designated as joint j and at the right end into a joint designated as joint k. Note that the member and joint numbering systems are such that the joint number j must be equal numerically to the member number i, and the joint number k must be equal to i + 1. These particular relationships between the member numbers and the joint numbers are, of course, valid only for a continuous beam. Also, it can be seen that in this case the total number of joints, denoted henceforth as njo is always one more than the number of members; thus, nj = m + 1.


Support restraints of two types may exist at any joint in a continuous beam. These are a restraint against translation in the y direction and a restraint against rotation about the z axis. For example, joint 1 of the beam in the figure is assumed to be fixed, and therefore is restrained against both

![image 298](Matrix Analysis of Framed Structures_images/imageFile298.png)

200 Chapter 4 Computer-Oriented Direct Stiffness ivlethod

###### IY

A A x

21 i-I i+l/ (m-l m

/~ IA

2 j k m m+l

z

(a)

Y

3 2j-l 2k-l 2m-l 2m+l

11

###### i t t

###### t t i

i

/~ 7~ ~~ /~ /'~ /~-x

/2 4 2j 2k 2m 2m+2

z

( b)

jl kl

###### t

/~. i ~

/k j2 k2

(c)

Fig. 4-7. Numbering system for a continuous beam.

translation and rotation; joints 2, j, and m are restrained against translation only; and joints k and m + 1 are not restrained at all.

In a continuous beam the displacements are due primarily to flexural deformations, and only such deformations will be considered in this section. The effects of shearing deformations can be included in the analysis if necessary, as described later in Sec. 6.16. In either case, however, the omission of axial deformations means that a maximum of two possible displacements may occur at any joint. These are the translation in the y direction and the rotation about the z axis. A numbering system for all ofthe possible joint displacements is indicated in Fig. 4-7b. Starting at the left-hand end of the structure and proceeding to the right, the translation and rotation at each joint are numbered in sequence. Since the translation at a particular joint is numbered before the rotation, it follows that in all cases the number representing the translation is equal to twice the joint number minus one, while the number for the rotation is twice the joint number. For instance,

- at joint j the translation and rotation are numbered 2j - 1 and 2j, respectively. Similar comments apply to the other joints, such as joints k, m, and m + 1. It is evident that the total number ofpossible joint displacements is twice the number of joints, or 2nj. Furthermore, if the total number of support restraints against translation and rotation is denoted nr. the number of actual displacements, or degrees offreedom, is


n = 2nj - nr = 2m + 2 - nr

(4-10)

in which n is the number of degrees offreedom.

![image 299](Matrix Analysis of Framed Structures_images/imageFile299.png)

4.8 Analysis of Continuous Beams 201

The analysis of a continuous beam consists of setting up the necessary stiffness and load matrices and applying the equations of the direct stiffness method to the particular problem at hand. For this purpose, the most important matrix to be generated is the over-all joint stiffness matrix SJ' The joint stiffness matrix consists of contributions from the beam stiffnesses SMi given previously in Sec. 4.3 (see Table 4-2). For example, the i-th member in the continuous beam of Fig. 4-7 contributes to the stiffnesses of the joints j and k at the left and right ends of the member, respectively. Therefore, it is necessary to relate the end-displacements of member i to the displacements of joints j and k by means of an appropriate indexing system.

In order to relate the end-displacements of a particular member to the displacements ofthe joints, consider the typical member i as shown in Fig.

- 4-7c. The displacements of the ends of this member will be denotedjl and j2 at the left end, and kl and k2 at the right end. In both cases the translation is numbered before the rotation. These are the same member end-displacements that were numbered 1,2,3, and 4 in Fig. 4-3b. However, the use ofa new notation, such asjl,j2, k 1, and 1<2, is desired in order to have a symbol that can be used in computer programming to represent the number for the end-displacement. The four end-displacements of member i are related to the joint numbers by the following expressions (compare Figs.


- 4-7b and c):


jl = 2j - 1 1<1 = 21< - 1

j2 = 2j 1<2 = 21<

(4-11)

Because in the continuous beam of Fig. 4-7 the joint numbers j and k are equal numerically to i and i + 1, respectively, the end-displacements are also given by

jl = 2i - 1 I< 1 = 2i + 1

j2 = 2i 1<2 = 2i + 2

(4-12)

Thus, the above equations serve to index the possible joint displacements at the left and right ends of any member i in terms of either the joint numbers (Eqs. 4-11) or the member numbers (Eqs. 4-12). Such an indexing system is necessary for the purpose of constructing the joint stiffness matrix from the member stiffness matrices. The system also proves to be useful when calculating end-actions in the members due to displacements of the joints, as shown later.

As discussed previously, the over-all joint stiffness matrix SJ is made up of contributions from individual member stiffnesses. Hence, it is convenient to assess such contributions for one typical member i in the beam, and then to repeat the process for all members from 1 through m. A typical member i from a continuous beam is shown again in Fig. 4-8, with adjacent members i-I and i + 1 also indicated. In part (a) of the figure the beam is shown with a unit displacement corresponding to j 1; that is, a y translation at the left end of the member. The four actions developed at joints j

![image 300](Matrix Analysis of Framed Structures_images/imageFile300.png)

and k at the two ends of member i are stiffness coefficients SJ and are elements of the over-all joint stiffness matrix. Each such stiffness will have two subscripts as it appears in the joint stiffness matrix. The first subscript is the number (or index) that denotes the location of the action itself, and the second is the index for the unit displacement causing the action. Thus, the stiffness at joint j in the y direction has subscripts j 1 and j 1, meaning that the action corresponds to a displacement oftypejl and is caused by a unit displacement of type jl. This stiffness is denoted, therefore, by the symbol (SJh.Jb as shown in Fig. 4-8a. Of course, the actual value of the indexjl is obtained from Eqs. (4-12). Similarly, each ofthe remaining three stiffnesses in Fig. 4-8a has a first sUbscript that identifies the type of displacement to which the stiffness corresponds. However, each of them has the same second subscript, denoting the unit displacement oftypej1.

The joint stiffnesses due to the remaining three possible joint displacements at the ends of member i are shown in Figs. 4-8b, 4-8c, and 4-8d. In each figure the four joint stiffnesses are shown with the appropriate subscripts that indicate (1) the type ofaction and (2) the unit displacement. The reader should verify the notation for each of the stiffnesses shown in Fig.

- 4-8. The next step is to express the joint stiffness coefficients shown in Fig.


- 4-8 in terms of the various member stiffnesses that contribute to the joint stiffnesses. This step requires that the member stiffnesses be obtained from Table 4-2, which gives the stiffnesses for a continuous beam member (see Fig. 4-3b for the indexing system to Table 4-2). For example, the contribution to the joint stiffness (SJ)il,Jl from member i-I (see Fig. 4-8a) is the stiffness SM33 for that member. Similarly, the contribution to (SJh,Jl from member i is the stiffness SMU for member i. These two contributions will be denoted (SM33)i-l and (SMU)i' respectively. In general, the contribution of one member to a particular joint stiffness will be denoted by appending the member subscript to the member stiffness itself. The latter quantity is obtained from the appropriate member stiffness matrix, which is Table 4-2 for a continuous beam having two possible displacements at each joint. From this discussion it can be seen that the joint stiffness coefficients shown in Fig. 4-8a are given in terms of the member stiffnesses by the following expressions:


(SJ)JIJl = (SM33)i-l + (SMU)i (SJ)J2Jl = (SM43)i-l + (SM2l)i (SJ)klJl = (SM3l)i

(4-13)

(SJ)k2Jl = (SM4l)i

which represent the transfer of elements of the first column of the member stiffness matrix to the appropriate locations in SJ' The first two joint stiffnesses consist of the sum of contributions from members i-I and i. The last two stiffnesses involve contributions from member i only. This pattern of mUltiple terms when the stiffness is at the near end of the member, and

![image 301](Matrix Analysis of Framed Structures_images/imageFile301.png)

4.8 Analysis of Continuous Beams 203

![image 302](Matrix Analysis of Framed Structures_images/imageFile302.png)

(0 )

![image 303](Matrix Analysis of Framed Structures_images/imageFile303.png)

/

![image 304](Matrix Analysis of Framed Structures_images/imageFile304.png)

(b )

(c)

![image 305](Matrix Analysis of Framed Structures_images/imageFile305.png)

###### /, 7 /

###### (S)j2.n (S).2.OZ

(d)

Fig. 4-8. Joint stiffnesses for a continuous beam.

single tenns when the stiffness is at the far end ofthe member, is typical of all types of framed structures. Of course, there are occasional exceptions, such as at the end of a continuous beam, where there is only a single contribution even though the stiffness is at the near end.

Expressions that are analogous to Eqs. (4-13) are easily obtained for a unit rotation about the z axis atjointj. This rotation is a unit displacement of type j2 for member i, as shown in Fig. 4-8b. The expressions for the joint stiffnesses in terms of the member stiffnesses are (from the second column of the member stiffness matrix)

(SJ)iIJ2 = (SM34);-1 + (SMI2); (SJ)i2J2 = (SM44);-1 + (SM22); (SJhIJ2 = (SM32);

(4-14)

(SJ)k2.i2 = (SM42);

Similarly, for a unit y translation at joint k (see Fig. 4-8c) the stiffnesses are (from the third column)

![image 306](Matrix Analysis of Framed Structures_images/imageFile306.png)

(SJ)il.kl = (SMdi (SJ)i2.kl = (SM23)i (SJhl.kl = (SM33)i + (SMll)i+l (SJ)k2.kl = (SM43)i + (SM21)i+l

(4-15)

Finally, the expressions for a unit z rotation at joint k (see Fig. 4-8d) are (from the fourth column)

(SJ)il,k2 = (SMI4)i (SJ)i2.k2 = (SM24)i (SJ)kl.k2 = (SM34)i + (SMI2)i+l (SJ)k2.k2 = (SM44)i + (SM22)i+l

(4-16)

Equations (4-13) through (4-16) show that the sixteen elements of the 4 x 4 member stiffness matrix [SML for member i contribute to sixteen of the joint stiffnesses in a very regular pattern. This pattern may be observed schematically in Fig. 4-9b, which indicates the formation of the joint stiffness matrix for a six-span continuous beam shown with restrained joints in Fig. 4-9a. For this structure the number of joints is seven, the number of possible joint displacements is fourteen, and therefore the joint stiffness matrix is of order 14 x 14. The indexing scheme is shown down the left-

![image 307](Matrix Analysis of Framed Structures_images/imageFile307.png)

1

3 5 7 9 11

13

###### t t t t t

###### t

t

1

###### /

2

4

5

3

6

###### / f

/~

/~

/~

/~

/~

4 6 8 10 12

2

14

(0)

![image 308](Matrix Analysis of Framed Structures_images/imageFile308.png)

1 2 3 4 5 6 7 B 9 10 11 12 13 14

###### l f0:

- -0;f0: 1 ~~~
- -0;~~ ~~IX


B

- 2~
- 3 ~
- 4
- 5
- 6
- 7 B


~ ;~ ~~ ~tz~ 3

9

~

- 2 o
- 3
- 4

- 2

5

- 3

6

- 4


- 7


~~ ~

1

~ ~ -0; ~f0 ~ ~ f0:~S8:;g

~ 4 1

~/;

~t/:: /;t%:

~Q<,i ~ 5 1 ~Z -0;10:

- 9
- 10
- 11
- 12
- 13
- 14


-0: -0:~tz~ 6 1

~ ~ ~ ~ /; /; ~~ ~ ~ 1 ~~ ~ ~

e 1 9 2 10 3 11 4 12 5 13 6 14 7

(b)

Fig. 4-9. Joint stiffness matrix for a continuous beam.

![image 309](Matrix Analysis of Framed Structures_images/imageFile309.png)

4.8 Analysis of Continuous Beams 205

hand edge and across the upper edge of the matrix in Fig. 4-9b. The contributions of individual members are indicated by the hatched blocks, each of which is of the order 4 x 4. The blocks are numbered in their upper righthand comers to identify the members that are being considered. The overlapping blocks, which are of order 2 x 2 in this example, denote elements of S} which receive contributions from two adjacent members. All elements outside the shaded blocks are zero.

The stiffness matrix illustrated in Fig. 4-9b is the over-all matrix for all

possible joint displacements.* In order to analyze a given beam, however,

the matrix must be rearranged into the partitioned form given by Eq. (4-8). Suppose, for example, that the actual beam has simple supports at all joints, as shown in Fig. 4-10a. The rearranged and partitioned stiffness matrix for this case is indicated in Fig. 4-lOb. To obtain this rearranged matrix, rows and columns of the original matrix have been switched in proper sequence in order to place the stiffnesses pertaining to the actual degrees of freedom in the first seven rows and columns. At the same time, the stiffnesses pertaining to the support restraints have been placed in the last seven rows and columns. As an aid in the rearranging process, the new row and column designations are listed in Fig. 4-9b down the right side and across the bottom of the array. The rearrangement of the original stiffness matrix in this manner is equivalent to numbering the degrees of freedom and support restraints as shown in Fig. 4-lOa. However, the general approach in this chapter, as explained earlier, is to generate the stiffness matrix using a numbering system like that shown in Fig. 4-9a, and then to rearrange rows and columns as was done in the example of Figs. 4-9 and

4-10.

In summary, the procedure to be followed in generating the joint stiffness matrix SJ consists of taking the members in sequence and evaluating their contributions one at a time. For the typical member i, the procedure is as follows. First, the possible displacements at ends j and k of the member are related to the member number by calculating the indexes j 1, j2, k 1, and k2 (see Eqs. 4-12). Then the member stiffness matrix SM; is generated, and the elements of this matrix are transferred to SJ as indicated by the terms with SUbscripts i in Eqs. (4-13) through (4-16). After all members have been processed in this manner, the matrix SJ is complete. It may then be rearranged and partitioned in accordance with Eq. (4-8).

After obtaining the stiffness matrix, the next step is to obtain the load vectors. Consider first the vector AJ of actual joint loads. This vector contains 2nj elements, each of which corresponds to one of the possible joint displacements shown in Fig. 4-7b. Thus, at each joint there are two possible applied loads, namely, a force in the y direction and a couple in the z sense. These loads are shown in Fig. 4-11 and are denoted (AJhk-l and (AJhk' respectively. The subscripts used in identifying these actions are the same

*Note that the semi-band width for this type of matrix will always be four.

![image 310](Matrix Analysis of Framed Structures_images/imageFile310.png)

Chapter 4 Computer-Oriented Direct Stiffness Method

###### 206

![image 311](Matrix Analysis of Framed Structures_images/imageFile311.png)

9 10 II 12 13 14

6

###### /4)1t 2/~f 3 t 4 t 5 t 6 t

f

2 3 4 5 6 7

(0)

1 2 3 4 5 6 7 8 9 1110 12 13 14

![image 312](Matrix Analysis of Framed Structures_images/imageFile312.png)

10::r::-::: 10::~ ~ I ~ ~10::

- 1~
- 2
- 3
- 4
- 5
- 6
- 7
- 8
- 9
- 10
- 11
- 12
- 13
- 14


~

~

~ ~ t;0~

###### I:"::

~~ ~f::9St':

~

I ~~~

I ~~ (\: ~ ~ ~ft;0 t;010:: 10:: - - ~~

~~

- [/;

~ -

###### R

~

~ ~ ~ ~

~~~ I ~~~

r::-:::

~V

I ~ ~ 'l::

~

I f%:~10:: t%l ~f;&t%

r/;f!:X:~

~ ~

r/

!j0l V,~

(b)

Fig. 4-10. Rearranged joint stiffness matrix for a continuous beam.

as the numbering system for the possible joint displacements (see Fig. 4-7b). Thus, the vector AJ takes the form

The elements in this vector are known immediately from the given loads on the beam.

Consider next the formation of the matrix AML of fixed-end actions due to loads and the construction of the vector AE of equivalent joint loads. Figure 4-12b shows again the i-th member of a continuous beam, but with lateral loads applied along the length. The actions at the ends of member i with its ends fixed are denoted as follows:

![image 313](Matrix Analysis of Framed Structures_images/imageFile313.png)

![image 314](Matrix Analysis of Framed Structures_images/imageFile314.png)

Fig. 4-11. Joint loads for a continuous beam.

![image 315](Matrix Analysis of Framed Structures_images/imageFile315.png)

207

4.8 Analysis of Continuous Beams

(AML)l,i = force in the y direction at the left end (AML)2,i = moment in the z sense at the left end (AMLhi = force in the y direction at the right end (AML)4,i = moment in the z sense at the right end

In general, the first subscript for a fixed-end action denotes the action itself, and the second denotes the member. Thus, for a continuous beam, the matrix AML of fixed-end actions will be of order 4 x m, as follows:

(AML)l.i (AMI-h,i (A,I1L)3,i (A ML)4,i

(4-18)

The elements in this matrix are fixed-end actions that can be found from the formulas given in Appendix B.

The vector AE of equivalent joint loads may be constructed from the elements ofthe matrix AML• The process for doing this can be visualized by referring again to Fig. 4-12. The member i shown in part (b) of the figure contributes to the equivalent loads at joints j and k, which are at the ends of the member. The equivalent loads at these joints are shown in Figs. 4-12a and 4-12c, and are denoted by the same subscripts used previously for the possible joint displacements (see Fig. 4-7b). Thus, the vector AE has the general form

###### AE = {(AE)t. (AEh, ... , (AEhH, (AEb, (AEb-t.

(4-19)

(AE)2k, ••• , (A E)2m+2}

The individual elements of the vector AE consist of contributions from the two adjoining members. Consider first the force (AEhH in the y direction atjointj (see Fig. 4-12a). This action, which also may be denoted (AE)2i-l> is composed of the negative of the end-action (AML)l, i from member i (see Fig. 4-12b) and a similar contribution from the adjacent member i - 1 on the left. The latter contribution is the negative of the force (AMLh'i _ I at the right-hand end of member i - 1. By analogous reasoning the expressions for the other three equivalent loads can be obtained, thus giving the following results:

###### (AE12*_,

1ITI11TIII t

###### /t(AML1,,1 i /l(AML13" />

(AML 12,1 (AML14,i (AE1u (b 1 (c 1

###### (AE 12 /

(01

Fig. 4-12. Loads on a continuous beam member.

![image 316](Matrix Analysis of Framed Structures_images/imageFile316.png)

(AE)2.i-l = (A E)2i-l = -(AMLh,i-l - (AML)t,i (AE)2.i = (A E)2i = -(AMLki-l - (AMLh,i

(4-20)

(AE)2k-l = (AE)2i+l = - (AML)3,i - (A.\fL)l.i+1 (AEhk = (AEhi+2 = - (AML)4,i - (AML)2,i+l

The method for obtaining the vector AE consists of taking the members in sequence and evaluating their contributions one at a time. Thus, successive columns of the matrix AML are considered, and the elements of each column are transferred to the appropriate elements in the vector AE as indicated by the terms with subscripts i in Eqs. (4-20). After all members of the beam have been considered in this fashion, the vector AE is complete. It may be added to the vector AJ according to Eq. (4-7) to form the vector Ac ofcombined joint loads. Lastly, the vector Ac can be rearranged so that the first part becomes AFC and the second part becomes ARC, as explained in Sec. 4.6 (see Eq. 4-9).

After the required matrices and vectors have been formulated by the methods described above, the solution for the free joint displacements DF and the support reactions AR consists simply of substituting into Eqs. (4-3) and (4-4), respectively, and performing the indicated matrix multiplications. After finding the joint displacements DF, which correspond only to the degrees of freedom of the structure, it is convenient to form the overall joint displacement vector DJ containing elements that correspond to all possible joint displacements (see Fig. 4-7b). For a continuous beam, the vector DJ will be order 2nj x 1. It will contain values given by the vector DF (corresponding to degrees offreedom), and the remaining elements (corresponding to support restraints) will be zero. In general, the form of the vector DJ is

DJ = {(DJ)1, (DJ)2, ... , (DJ)2.i-l, (DJ)2i> (DJh-l'

(DJ)2k, ... ,(DJ)2m+2} (4-21)

Elements from this vector are used in calculating member end-actions, as described in the following.

To evaluate member end-actions, Eq. (4-5) must be applied once for each member ofthe structure. When written in detailed form, the equation is the following:

SM12 SM22 SM32 SM42

SM13

SM23 SM33 SM43

(4-22)

The vector AMLi is obtained from the i-th column of the matrix AML given previously, and the stiffness matrix SMi is obtained from Table 4-2. The

![image 317](Matrix Analysis of Framed Structures_images/imageFile317.png)

vector DMi represents the end-displacements for member i. These displacements are obtained from the vector DJ by taking the four consecutive displacements that are associated with member i. In general, the four displacements shown in Eq. (4-22), that is, D Mlo D M2, D M3, and D M4, are equal to the displacements (D./)jl, (D./)j2, (D./hl' and (D./hz, respectively, from the vector DJ• Thus, the four end-displacements for any member can be extracted from the vector DJ without difficulty.

Equation (4-22) can be further expanded by substituting into it the elements of S:VI j and D:'.! i and performing the matrix multiplication. When this is done, the following four equations are obtained:

(4-23)

Equations (4-22) and (4-23) are equivalent, of course, and either may be used for the purpose of computing the member end-actions.

The analysis of continuous beams using the highly organized method described above is demonstrated by an example in the next section. In the solution, the steps described in this section are followed as much as possible. Naturally, such procedures are very cumbersome for a hand solution, but they are used here deliberately in order to illustrate the way in which the solution is carried out by means of a computer program. Such a program for the analysis of continuous beams is presented in Sec. 5.6.

4.9 Example. The continuous beam shown in Fig. 4-13a is to be analyzed as described in the preceding section. The beam is restrained against translation at support C and against both translation and rotation at points A and D. At point B the flexural rigidity of the beam changes from EI to 2EI. Therefore, point B is taken to be a joint in the structure.

![image 318](Matrix Analysis of Framed Structures_images/imageFile318.png)

x

(0 )

###### IY

###### r f r r

###### /~}----/~~__2-;1~3___3=---__/---,t!_X

/2 4 6 8

z (b)

Fig. 4-13. Example (continuous beam).

The member and joint numbering systems are shown in Fig. 4-13b, and it is seen that the number of members m is three, the number of JOInts I1j is four, and the number ofsupport restraints 11r is five. Therefore, the number ofdegrees offreedom 11 is equal to three (see Eq. 4-10).

The member properties and the joint displacement indexes computed from Eq. (4-12) are given in Table 4-7. The moment of inertia and length of each member can be considered as given data (or input) to the analysis. The remaining quantities in the table are computed from the member numbers. Joint information for the beam is indicated in Table 4-8. In this table the indexes of all possible displacements are listed for each joint of the beam. This is followed by a joint restraint list, in which the numeral 1 is used to indicate the existence of a restraint, while a zero indicates no restraint (or a degree of freedom). Cumulative addition of the values in the restraint list produces the cllmulative restmim list given in the next column. The last column of the table shows the joint displacement indexes when they are revised so that the degrees of freedom are numbered before the actual restraints. These revised indexes are obtained by applying expressions (a) and (b) in Sec. 4.6. Thus, the two columns in Table 4-8 containing joint numbers and the restraint list can be considered as input, while the other three columns can be derived from the data in the input columns.

Table 4-7

Member Information for Beam of Fig. 4-13a

Indexes for EndMember Joint Numbers at Displacements of Number Ends ofMember Member Iz Length

i j k jl j2 kl k2

1 1 2 1 2 3 4 1 L 2 2 3 3 4 5 6 2I L 3 3 4 5 6 7 8 21 2L

![image 319](Matrix Analysis of Framed Structures_images/imageFile319.png)

###### Table 4-8

Joint Information for Beam of Fig. 4-13a

Indexes for Joint Cumulative Revised

Joint All Possible Restraint Restraint Displacement Number Displacements List List Indexes

I 1 1 1 4 2 1 2 5

- 2 3 0 2 1 4 0 2 2
- 3 5 1 3 6 6 0 3 3
- 4 7 1 4 7 8 1 5 8


In preparation for generating the over-all joint stiffness matrix SJ' the member stiffness matrices for all three members of the structure are given in Table 4-9. These are formed from Table 4-2 given in Sec. 4.3. The elements of the first member stiffness matrix SM) for member 1 are transferred to SJ according to Eqs. (4-13) through (4-16). The contributions to SJ from member I appear in Table 4-10 within the upper left-hand portion enclosed by dashed lines. In a similar manner, elements from SM2 and SM3 are transferred to SJ as shown by the two remaining portions of Table 4-10 that are delineated by dashed lines. In the regions where the portions enclosed by dashed lines overlap, the elements shown in the table are the sums of two terms, one from each of two member stiffness matrices. Note that all elements in the table are to be multiplied by the factor EI/L3• The numbering system for the stiffness matrix appears on the left side and across the top of the matrix and is in accordance with the numbering system shown in Fig. 4-13b.

Next, the matrix SJ is rearranged according to the revised displacement indexes

###### Table 4-9

Member Stiffness Matrices

6L -12

EI 6L 4V -6L 6L2V ] S~11 = L'l -12 -6L 12 -6L

[ 12

6L 2V -6L 4V

12L -24

EI 12L 8V -12L 12L4V ] S~)2 = L'l -24 -12L 24 -12L

[ 24

12L 4V -12L 8V

[

EI 3L 4V -3L 3L]2V

3 3L -3

S~l:l = L'l -3 -3L 3 -3L

3L 2V -3L 4V

![image 320](Matrix Analysis of Framed Structures_images/imageFile320.png)

212 Chapter 4 Computer-Oriented Direct Stiffness Method

Table 4-10 Joint Stiffness Matrix for Beam of Fig. 4-13

(All elements in the matrix are to be multiplied by the factor EIIV)

###### --------------------------------12I 6L2 -123 46L 50 06 70 08 4 6L 4U -6L 2U: 0 0 0 0 5 -12 -6L : -36--------6L--:---.::-Z4-----12T-: 0 0 I

###### I

- 2
- 3
- 4
- 5
- 6
- 7
- 8


I---0---6L ----O-----,--.::-2r----~-f2l---:2U: 6L 12U: ---2T-12L----~9i-4U :1--~3------3L--:0 0 62

I

- o 0 :I _______________________________12L 4U: -9L 12U: - 3L 2U:I 3
- o 0 0 0: -3 -3L 3 -3L: 7
- o 0 0 0 :____}f______~~~______::.~_____~f~_: 8


4 5 I 2 6 3 7 8

given in the last column of Table 4-8. This list is indicated by the numbers on the right side and across the bottom of the matrix in Table 4-10. The third, fourth, and sixth rows and columns are to be shifted to the first three positions, and all other rows and columns are to be shifted downward and to the right without changing their order. The resulting rearranged joint stiffness matrix is presented in Table 4-11. This matrix is partitioned, as shown by the dashed lines, in the manner given by Eq. (4-8).

The 3 x 3 stiffness matrix SFF is drawn from Table 4-11 as follows:

6L

El [ 36 SFF = L3 6L

I2L] 4U

12U

12L

4U

12U

Inversion of this matrix produces

- -6L 72
- -18


32U

- -30L]
- -18 99


-1 _ L

[

SrF - 756El -6L -30L

Thus, all of the calculations involving the properties of the structure have been completed, and information concerning the loads on the structure may now be processed.

###### Table 4-11

Rearranged Joint Stiffness Matrix for Beam of Fig. 4-13

(All elements in the matrix are to be multiplied by the factor EllV)

2 3 4 5 6 7 8

- 1 36 6L 12L -12 -6L -24 0 0
- 2 6L 12U 4U 6L 2U -12L 0 0
- 3 _l~_______~f~_____!~~~__~____~_______~_______~Jf_____~}~______~~~
- 4 -12 6L 0 12 6L 0 0 0
- 5 -6L 2L2 0 6L 4U 0 0 0
- 6 -24 -I2L -9L 0 0 27 -3 3L
- 7 0 0 - 3L 0 0 - 3 3 - 3L
- 8 0 0 2U 0 0 3L - 3L 4U


![image 321](Matrix Analysis of Framed Structures_images/imageFile321.png)

4.9 Example

213

Table 4-12

###### Actions Applied at Joints

###### Force iny Moment in Joint Direction z Sense

I 0 0

- 2 -P PL
- 3 -P 0
- 4 0 0


Inspection of Fig. 4-13a shows that loads are applied at joints Band Conly Goints 2 and 3 in Fig. 4-13b). These joint loads are listed in Table 4-12 in a manner that is suitable for input to a computer program. Next, these actions are placed in the vector AJ as follows (see Eq. 4-17):

AJ = {O, 0, -P, PL, -P, 0, 0, O}

Fixed-end actions AML are tabulated row-wise in Table 4-13, which is transposed with respect to the arrangement in Eq. (4-18). The elements of AML are transferred to the vector of equivalent joint loads AE as indicated by Eqs. (4-20). First, the fixed-end actions for member 1 are transferred to the first four elements of AE; then the actions for member 2 are transferred to elements three to six of AE; and lastly, the actions for member 3 are transferred to the last four elements of AE• When the vector has been generated in this manner, the result is

###### AE = {-P, -PLl4, -2P, 0, -2P, -PLl12, -P, PLl3}

The vectors AJ and AE are now combined using Eq. (4-7) to obtain the vector Ac

###### Ac = {-P, -PLl4, -3P, PL, -3P, -PLlI2, -P, PLl3}

This vector must be rearranged by placing the third, fourth, and sixth elements into the first three positions and moving all other elements toward the end without changing their order. This rearrangement results in the following vector:

###### Ac = {-3P, PL, -PLlI2, -P, -PLl4, -3P, -P, PLl3}

in which the first three elements are the vector AFC

###### A~·c = {-3P, PL, -PLlI2}

and the last five are the elements of ARC (see Eq. 4-9)

ARC = {-P, -PLl4, -3P, -P, PLl3}

Table 4-13

###### Fixed-End Actions Due to Loads

###### Member

(A.1ll)4.i

(AJnki (AJILki (AJILhi

- -PLl4
- -PLl4
- -PLl3


P PLl4 P P PLl4 P P PLl3 P

- 1
- 2
- 3


![image 322](Matrix Analysis of Framed Structures_images/imageFile322.png)

214 Chapter 4 Computer-Oriented Direct Stiffness Method

Having all of the required matrices on hand, one may complete the solution by first calculating the free joint displacements DF using Eq. (4-3). Hence,

DF =SF'JAFC =75~E1[ ~~Z2 -;; ~~t] [~~1] ~

-30L -IS 99 -L

PU [-39SL]

= 3024E1 366

255

The vector DF may now be used in obtaining the vector DJ of all possible joint displacements by referring to the original and revised displacement indexes shown in Table 4-S. These indexes show that DJ3 = Db DJ~ = D2, and DJ6 = D;j. All other elements of DJ are zero because they correspond to support restraints. Thus, the vector DJ becomes the following:

###### PU

D.J = 3024EI {O, 0, -39SL, 366,0,255,0, O}

Next, the support reactions AR may be determined from Eq. (4-4). For this purpose the matrix SRF is obtained from the lower left-hand portion of Table 4-11. The calculation for AR is as follows:

AR = -ARC + SRFDF

=12P 3L3612] + VEI [12~6L-24 -12L2U6L

oo J

[

-39SL PU

12 0 0

- -9L [366]3024EI
- -3L 255 2U


-4L 0 0

= l:OS[ 1:0~J

753

###### -166L

Finally, the member end-actions AM i are obtained by repeated applications of Eq. (4-5) (see also Eq. 4-22). Since there are three members in this example, three calculations of this type are required. For member 1 the calculations are as follows:

AMI = AMLI + SMIDMI

###### =t [1]+SMI[-39t]3tz~~1=2~2 [J~iL]

###### -L 366 25SL

In the above equation the vector DMI consists of the first four elements of DJ • Similarly, the equations for AM2 and AM3 are

AM2 = AML2 + SM2DM2

=~[ ~]+SM2[-~~L]3:Z~~1= :;2 [ 4~iL]

###### -L 255 -169L

![image 323](Matrix Analysis of Framed Structures_images/imageFile323.png)

4.10 Plane Truss Member Stiffnesses 215

AM3 = AML3 + SM3DM3

###### P [ L3] [OJ255 PL2 P [1263]676L

= 3 3 + SMa 0 3024EI = 1008 753

###### -L 0 -166L

in which the vector DM2 is made up of the third through the sixth elements of D.h and the vector DM:1 consists of the last four elements of DJ• Thus, all of the joint displacements, support reactions, and member end-actions are determined, and the problem is considered to be completed.

4.10 Plane Truss Member Stiffnesses. Determination of the complete member stiffness matrix fora typical truss member is a preliminary to the analysis of plane trusses. A typical member i within a plane truss is

- shown in Fig. 4-14a. The joints at the ends of this member are denoted as joints j and k. The plane truss itself is assumed to lie in the x-y plane, where x and yare reference axes for the structure. The joint translations are the unknown displacements in the analysis, and all of these translations


Fig. 4·14. Numbering system for a plane truss member.

![image 324](Matrix Analysis of Framed Structures_images/imageFile324.png)

may be expressed conveniently by their components in the x and Y directions. For the typical member i, the positive directions ofthe four displacement components at its ends (with respect to the structure-oriented axes) are indicated in Fig. 4-14b.

It is convenient when dealing with inclined members in a framed structure to make use ofdirection cosines. The direction cosines for the member

- shown in Fig. 4-14b are the cosines of the angles '}II and '}I2 between the axis of the member and the x and Y axes, respectively. These angles will always be taken at the j end of the member. The corresponding direction cosines


are denoted as ex and ey and are given as follows:

ex = cos '}II ey = cos '}I2 = sin '}II

The direction cosines for the member can also be expressed in terms of the coordinates of the joints j and k. If the x and y coordinates ofjoints j and k are denoted by (Xj, Yj) and (Xk, Yk), respectively, the direction cosines become

c - Yk - Yj

y - L (4-24)

in which L is the length of the member. The length L may be computed from the coordinates of the joints at the ends of the member as follows:

L = V(Xk - Xj)2 + (Yk - YY (4-25)

Both direction cosines are positive when the member is oriented as shown in Fig. 4-14b, that is, when the x and Y coordinates of joint k are greater than those for jointj. Ifthe angle '}II is greater than 90°, the formulas given above are still valid, and one or both of the direction cosines will be negative.

In the analysis of a plane truss, as in the case of any other type of framed structure, it is convenient to generate the joint stiffness matrix SJ by assessing the contributions from member stiffnesses. In the case of a continuous beam this operation is straightforward (see Sec. 4.8) because the member-oriented axes may be taken parallel to, or coincident with, the structure-oriented axes. Thus, the beam member stiffness matrix for member-oriented axes, as derived in Sec. 4.3, can be used directly when obtaining joint stiffnesses for the structure axes. For any other type of framed structure, however, the member axes will not necessarily be parallel to the structural axes. For example, the x-Y axes in Fig. 4-14b are structure-oriented axes, whereas the member axes XM and YM are assumed to be along the axis of the member and perpendicular to the member, as shown in Fig. 4-14c. The stiffness matrix SMi for these member-oriented axes can be obtained readily by referring to cases (1) and (7) of Fig. 4-2. With the numbering system shown in Fig. 4-14c for the end-displacements with respect to the XlfYM axes, it becomes evident that the stiffness matrix SMi for those axes has the form shown in

![image 325](Matrix Analysis of Framed Structures_images/imageFile325.png)

4.10 Plane Truss Member Stiffnesses 217

Table 4-14

Plane Truss Member Stiffness Matrix for Member Axes (Fig. 4-14c)

Table 4-14. In the table, the axial rigidity of the member is denoted by EAx, and the matrix is partitioned as before.

Because the matrix SJ is based upon axes oriented to the structure, it also becomes necessary to obtain member stiffnesses for the structural axes. The member stiffnesses for the structural axes may be found in either of two ways. The first method consists of a direct formulation of the stiffnesses. In this approach, unit displacements in the directions of the structural axes (see Fig. 4-14b) are induced at the ends of the member, and the corresponding restraint actions in the same directions are calculated. These actions become the elements of the member stiffness matrix for the structural axes. The second method for finding the member stiffness matrix consists of first obtaining the stiffness matrix for member-oriented axes (see Table 4-14) and then transforming this matrix to the structure-oriented axes by a process of rotation of axes. With an appropriate transformation matrix, the rotation of axes may be executed by matrix multiplications, as will be described in a later section.

The member stiffness matrix for a plane truss member will now be developed by the direct method. For this purpose it is necessary to consider unit displacements in the x and y directions at both ends of the member. The first such displacement is shown in Fig. 4-15a and consists of a unit translation in the x direction at thej end of the member. As a result of this displacement, an axial force is induced in the member. This force can be calculated from the axial shortening of the member, which is numerically equal to the x direction cosine Cx for the member (see Fig. 4-15a). The axial compressive force in the member due to this change of length is equal to

EAx C

L x

The restraint actions at the ends of the member in the x and y directions, which are equal to the components of the axial force, are the desired member stiffnesses for the structural axes. Such stiffnesses are identified by the symbol SMS (see Fig. 4-15a) in order to distinguish them from the stiffnesses SM for the member axes (see Table 4-14). The numbering system for the stiffnesses SMS is shown in Fig. 4-14b. The restraint action at endj in the x

![image 326](Matrix Analysis of Framed Structures_images/imageFile326.png)

(0 )

SMS42

t SMS32

~

###### k

- (b)

y

- (c)

j

- (d) SM524


###### t

~SM514

j

Fig. 4-15. Plane truss member stiffnesses for structural axes.

direction, denoted as SMSII' must be equal to the x component of the force in the member. Therefore, this stiffness is equal to the axial force times the x direction cosine, as follows:

EAx 2

SMSll = L Cx

Also, the restraint action atj in the y direction is equal to the y component of the force in the member:

EAx

SMS21 = L CxCy

The restraint actions at the k end of the member in Fig. 4-15a are readily found by static equilibrium, as follows:

![image 327](Matrix Analysis of Framed Structures_images/imageFile327.png)

4.11 Analysis of Plane Trusses 219

S S - EAx C2

MS31 = - MSll - - T x

###### EAx

###### SMS41 = -SMS21 = -T CxCy

The expressions given above for the four stiffnesses shown in Fig. 4-15a constitute the elements of the first column of the matrix SMSi' The second, third, and fourth columns of SMSi may be obtained in a similar manner from Figs. 4-15b, 4-15c, and 4-15d, respectively, to give the 4 x 4 stiffness matrix shown in Table 4-15. The reader should verify for himself the remaining elements in this matrix.

Table 4-15

Plane Truss Member Stiffness Matrix for Structural Axes (Fig. 4-14b)

###### c~ c,c,,: -q -C'C'j

[ J r

s"s; = S'.lSjj S'.IS)k = EAy __~'-c:'~_____.~Lj__~~~C::~____=-._~j~

S S L -c~ -c,c,: q c,C,

'IS kj :\IS kk

###### -CXcy -c}: c,Cr C}

4.11 Analysis of Plane Trusses. As an initial step in the analysis of a plane truss, all of the joints and members must be numbered. The joints of the structure are numbered consecutively from 1 through nj, where nj is the total number ofjoints. In addition, the members are numbered from 1 through m, where m is the total number of members. The order in which the joints and members are numbered is immaterial. However, after the numbering is completed, it is necessary to record the two joint numbers that are associated with each member. This association of joint numbers with member numbers is necessary in order to ascertain which elements of the joint stiffness matrix SJ and the equivalent load vector AE receive contributions from each member.

To illustrate the arbitrary numbering of the joints and members, a plane truss is shown in Fig. 4-16a. In the figure the joint numbers appear adjacent to the joints, while the member numbers are enclosed in circles adjacent to the members. The numbering system for this structure is shown in Table 4-16. It is necessary for purposes of analysis to identify a j end and a k end

Table 4-16

Listing of Members and Joints for Truss of Fig. 4-16a

Member 1 2 3 4 5 6 7 8 9

- Joint j 2 6 4 3 4 1 6 1 2
- Joint k 5 5 1 5 2 5 3 6 1


![image 328](Matrix Analysis of Framed Structures_images/imageFile328.png)

220 Chapter 4 Computer-Oriented Direct Stiffness Method

3

(0)

( b)

Fig. 4-16. Numbering systems for members and joints of plane trusses.

for each member, as shown in the table, although the selection itself is arbitrary.

While the methods of analysis in this chapter do not require any particular order of numbering joints and members, it is only natural to number them in a systematic pattern whenever feasible. For example, in some structures a natural order may be from left to right or from top to bottom, as shown by the plane truss in Fig. 4-16b. The geometry of this truss suggests that a systematic pattern for numbering the joints is to proceed from top to bottom and left to right. A systematic pattern for the members consists of numbering consecutively the horizontal members, the vertical members, and then the diagonal members, as shown in the figure. The numbering system for this structure is summarized in Table 4-17. Note again that it is necessary to identify one end of each member as being the j end and one end as the k end.

Many possible schemes for numbering the joints and members ofa truss can be organized, depending mainly on personal preference. If it is desired to improve the efficiency of the solution, the numbering system may be selected to minimize the amount of rearrangement ofthe over-all joint stiff-

Table 4-17

Listing of Members and Joints for Truss of Fig. 4-16b

Member 1 2 3 4 5 6 7 8 9 10 11

Jointj 1 3 2 4 1 3 5 1 2 3 4 Joint k 3 5 4 6 2 4 6 4 3 6 5

![image 329](Matrix Analysis of Framed Structures_images/imageFile329.png)

4.11 Analysis of Plane Trusses 221

ness matrix S1' This procedure might be convenient for hand calculations. but the advantage disappears when the analysis is programmed for a computer.

A better choice would be to minimize the semi-band width of matrix SJ to save space and time when setting up and solving the action equations on a computer. Joints of the truss in Fig. 4-16b were numbered in vertical sweeps instead of horizontal sweeps for this reason.

After numbering the members and joints, the next step in the analysis is to identify all possible joint displacements and the degrees offreedom. The number of the former will be twice the number ofjoints, or 2nj, since each joint may undergo a translation in both the x and y directions. The number of degrees offreedom n is given by the expression

n = 2nj - n,. (4-26) in which n,. denotes the number of support restraints.

The possible joint displacements will be numbered in the same order as the joints, taking the x translation before the y translation at each joint. Thus, the x translation at joint I becomes displacement number I, the y translation at joint I becomes displacement number 2, the x translation at joint 2 becomes displacement number 3, and so forth, until at the last joint the x and)' translations are numbered 211j - I and 211jo respectively. In general, at joint j of the truss the x and y translations have the indexes 2j - I and 2j. respectively.

In order to construct the stiffness matrix SJ from the member stiffnesses, it is useful to relate the indexes for the possible joint displacements to the end displacements for a particular member, as was done in the analysis of continuous beams. For this purpose consider the typical member i. shown in Fig. 4-17, which frames intojointsj and k at the ends. The x and y axes in the figure are assumed to be structure-oriented axes. The enddisplacements of this member may be identified by the indexes jl, j2, k 1, and k2, as shown in the figure. These indexes for the member are related to the joint numbers j and k as follows:

jl = 2j - 1 kl = 2k - 1

j2 = 2j k2 = 2k

(4-27)

Fig. 4-17. End-displacements for plane truss member.

![image 330](Matrix Analysis of Framed Structures_images/imageFile330.png)

These relations follow directly from the numbering system for the possible joint displacements, which is described above.

The joint stiffness matrix consists of contributions from the individual members. Therefore, the member stiffnes matrix SMSi (see Sec. 4-10, Table 4-15) for each member must be determined and its elements placed in the proper positions in the matrix SJ. In order to see how this is accomplished, consider again a typical member i (Fig. 4-18a). This member contributes to the stiffness of joints j and k at its ends. If a unit displacement in the x direction is induced in the restrained structure, as shown in the figure, there will be restraint actions in the x and y directions at both joints. At jointj the action in the x direction is the joint stiffness (Sj)j I,jI, and the action in the y direction is the stiffness (Sj)j2,jl' Similarly, the actions at joint k are denoted (Sjh I,jI and (SA2,j I' The two actions at joint j consist of contributions from the member i, plus contributions from all other members that frame into joint j, The latter contributions will be denoted for simplicity by the indefinite

###### (S)"",

- (a) (e)
- (b) (d)


###### Fig, 4-18, Joint stiffnesses for a plane truss,

![image 331](Matrix Analysis of Framed Structures_images/imageFile331.png)

symbol r.,SMS' The contributions from member i, however, will be written in precise form because they are the terms of current interest. In the case of the stiffness (Sj)j Lj I the contribution from member i is the member stiffness SMSI" and for the stiffness (Sj)j2,j I the contribution is SMS21' For the stiffnesses at joint k, only contributions from member i are involved, which are SMS31 and SMS41 for the x and y directions. Thus, the expressions for the joint stiffnesses shown in Fig. 4-18a are

(SJ)il,jl = l SMS + (S.~[Sl1); (SJ)i2,il = l SMS + (SMS21); (SJh1.i1 = (SMS31);

(4-28) (SJ)k2,il = (SMS41)i

Each of the above stiffnesses is due to a unit x translation at joint j, and each receives a contribution from the first column of the matrix SMS; for member i.

Expressions similar to Eqs. (4-28) may be written for a unit translation of the restrained structure in the y direction at joint j, as shown in Fig. 4-18b. These expressions involve the second column of SMS; and are as follows:

(SJ)il,i2 = l SMS + (SMSI2); (SJ)i2,i2 = l SMS + (SMS22); (SJhl,j2 = (SMS32); (SJ)k2,j2 = (SMS42);

(4-29)

Also, for a unit x translation at k (Fig. 4-18c) the joint stiffnesses which receive contributions from the third column of SMS; are

(SJ)jl,kl = (SMSI3); (SJ)i2,kl = (SMsdi (SJhl,kl = l SMS + (SMS33); (SJ)k2,kl = l SMS + (SMS43);

(4-30)

Finally, the stiffnesses for a unit y translation at k (see Fig. 4-18d) receive contributions from the fourth column of SMS;, as follows:

(SJ)jl,k2 = (SMS14); (SJ)i2,k2 = (SMS24)i (SJhl,k2 = l SMS + (SMS34)i (SJh2,k2 = l SMS + (SMS44);

(4-31)

The pattern of contributions of member stiffnesses to the joint stiffness matrix, as expressed by the above equations, is determined by the geometry of the truss and the system for numbering joints and members. The pattern for the structure shown in Fig. 4-19 will be used as an example. Joints and members for the truss are numbered as shown in the figure, and the possible joint displacements (shown by arrows) are numbered according to Eqs. (4-27). For this structure there are six members and four joints,

![image 332](Matrix Analysis of Framed Structures_images/imageFile332.png)

-5

Fig. 4-19. Example (plane truss).

and the over-all joint stiffness matrix is of order 8 x 8. The positions of the member contributions to the joint stiffness matrix are indicated by crosses in Figs. 4-20a through 4-20f, and the final stiffness matrix is a composite of these contributions. As an example, the joint stiffness SJl1 is made up of contributions from members 1,2, and 3, as shown in Fig. 4-20a, 4-20b, and 4-20c. Therefore, the stiffness is:

SJ11 = (SM811)' + (5M811h + (5M811h

1 2 3 4 5 678

12345678

- 1 X X X X
- 2 X X X X
- 3 X X X X
- 4 X X X X
- 5
- 6
- 7
- 8


- 1 X X X X
- 2 X X X X
- 3
- 4
- 5 X X X X
- 6 X X X X
- 7
- 8 (b) Member 2


- 1
- 2
- 3
- 4
- 5
- 6

12345678

X X X X

X X

X X

- 7 X X x x
- 8 X X x x (e) Member 3


###### (0) Member 1

###### 1 2 345 6 7 B

###### 1 2345678

12345678

- 1
- 2
- 3
- 4
- 5 X X X X
- 6 X X X X
- 7 X X X X B X X X X


- 1
- 2
- 3 X X X X
- 4 X X X X
- 5
- 6
- 7 X X X X
- 8 X X X X (e) Member 5


- 1
- 2
- 3 X X X X
- 4 X X X X
- 5 X X X X
- 6 X X X X
- 7
- 8 (d) Member 4


(f) Member 6

###### Fig. 4-20. Contributions of member stiffnesses to joint stiffnesses for plane truss example.

![image 333](Matrix Analysis of Framed Structures_images/imageFile333.png)

As another illustration, consider the joint stiffness 5134, which is composed of member stiffnesses from members 1, 4, and 5. This stiffness is

S.J~4 = (SUS34)1 + (SMSI2)4 + (S.HSI2h

- as can be seen by referring to Figs. 4-20a, 4-20d, and 4-20e. In the particular example of Fig. 4-19, the stiffness matrix S" does not

have to be rearranged because ofthe sequence in which the joints are numbered. The first four rows and columns of S.J are associated with the degrees of freedom, and the last four rows and columns pertain to the support restraints. However, this is a special case, and even a small change in the structure, such as placing a roller support at joint 3, would make a rearrangement necessary.

The vectors associated with the loads on a truss will be discussed next. The first one to be considered is the vector A.J of actions (or loads) applied

- at the joints. At a typical joint 11., two orthogonal force components may exist, as shown in Fig. 4-21. The action (A.J)2k-1 is the force in the positive x direction, and the action (A.J)2k is the force in the positive y direction. The vector A.J, therefore, will have the following form:


(4-32)

in which there are 2nj elements corresponding to the 211j possible joint displacements.

Consider next the matrix ofactions A~lL due to loads acting on the members when the joints of the truss are restrained against translation. Loads acting on member i are illustrated in Fig. 4-22b, which also shows a set of member-oriented axes Xu and YM. The actions AMLi for member i are defined with respect to the XM and YM axes, as follows:

(Audl,i = force in the X;H direction at the j end (AMLh.i = force in the YH direction at the j end (AMLh.i = force in the Xu direction at the k end (A.~lIJ4,i = force in the YM direction at the II. end

These end-actions may be obtained for any particular loading conditions by referring to the tables in Appendix B. The matrix AM! is of order 4 x m and is of the same form as that given by Eq. (4-18) for continuous beams,

(AJl2k

###### Fig. 4·21. Joint loads for a plane truss.

![image 334](Matrix Analysis of Framed Structures_images/imageFile334.png)

(0 )

Fig. 4-22. Loads on a plane truss member.

The vector AE of equivalent joint loads may be constructed from the elements of the matrix AML• This vector is of the same form as that given by Eq. (4-32), except that AE replaces A}. To illustrate the calculation of the equivalent joint loads, consider the action (AEhj-1 shown in Fig. 4-22a. This action is made up of contributions from member i, plus terms from all other members meeting at the joint. The latter contributions will be denoted by the indefinite symbol EAMS' The terms from member i, however, can be readily expressed using the end-actions in the i-th column of AML• All that is necessary is to take the components in the x direction of the end-actions at joint j, and to reverse their signs. Thus, the contribution of member i to the equivalent load (AEhj _I is

###### -Cxi(AML)l,i + CYi(AMLki

in which Cx; and CYi are the direction cosines for member i. By proceeding in this manner, the equivalent loads at joints j and k (see Figs. 4-22a and 4-22c) can be found as

(AE)2.I-l = - I A MS - Cxl(AML)l,i + CYi(AML)2,i (AE)2J = - I AMS - CYi(AMLkl - Cxi(AML)2,1 (AEhk-l = -I A MS - Cxl(AMLh,i + C yi(AML)4,i (AE)2k = -I A MS - CYi(AMLh,i - Cxi(AML)4,i

(4-33)

These equations give the contributions of member i to the equivalent joint loads, as indicated earlier in Eq. (4-2). By applying the equations consecutively to all members ofthe truss, the equivalentjoint loads can be obtained for all joints.

The contributions of member i to the vector AE may also be ascertained by the method of rotation of axes. This procedure is demonstrated for plane truss structures in Sec. 4. 14.

![image 335](Matrix Analysis of Framed Structures_images/imageFile335.png)

- 4.11 Analysis of Plane Trusses 227


The vectors AJ and AE may be added together (see Eq. 4-7) to form the vector Ac. The latter vector is then rearranged if necessary in order to isolate the vector AFC (see Eq. 4-9). Then the vector AFC and the inverse matrix SFt are used in calculating the free joint displacements DF, as given by Eq. (4-3). Next, the vector of free joint displacements DF can be expanded into the vector DJ of all possible joint displacements. The vector DJ has 2nj elements, and those elements which correspond to the support restraints are zero. As the next step, the solution for the support reactions is obtained in the usual manner by means of Eq. (4-4).

The final task of solving for the member end-actions may be carried out by means ofEq. (4-5). This equation must be applied once for each member of the structure. Note that when written in expanded form, the equation has the same form as Eq. (4-22). The vector AMLi is obtained from the i-th column of the matrix AML described above. The matrix SM i is the stiffness matrix for the i-th member with respect to member axes (see Table 4-14).

The vector DM i in Eg. (4-5) consists of the end-displacements for member

- i in the directions of the member axes. These displacements can be calculated from the joint displacements Dj, which are in the directions of the structural axes. For instance, the first element DM I in the vector DM i represents the displacement of joint j in the XM direction. This displacement is given by the following expression:

D,UI = (DJ)jlCXi + (DJ)j2Cri

in which (DJ) jl and CDJL2 are the displacements of joint j in the x and y directions, respectively (see Fig. 4-17). Similarly, the displacement ofjoint

- j in the YM direction can be expressed in terms of CDJ) jl and (DJ) j2 by the following:


In addition, the end-displacements at joint k may be obtained as follows:

D M3 = (DJhlCXi + (DJ)k2C y; DM~ = -(DJ)klCYi + CDJh2CXi

The above expressions for the elements of DM i can now be substituted into Eq. (4-5). When similar substitutions for the elements of SMi are made, the equation can be expanded into the following four separate equations:

EAxi

(AMki = (AML)l,i + L. {[(DJ)jl - (DJ)kl] CXi

1

+ [(DJ)j2 - (DJ)dCyi} (AM)2.i = (AMLh.i

(4-34)

EAxi

(A,1f)3.i = (AMLhi - L. {[(DJ)jl - CDJ)kl]CXi

1

###### + [(DJ)j2 - (DJh2]CY;}

![image 336](Matrix Analysis of Framed Structures_images/imageFile336.png)

228 Chapter 4 Computer-Oriented Direct Stiffness Method

These equations may now be applied repeatedly for all members of the truss. For each member the displacements DJ which appear in the equations must be extracted in the appropriate manner from the vector DJ of all joint displacements.

Another method for obtaining the vector DM ;, which appears in Eq. (4-5), is to use rotation of axes. This method is described later in Sec. 4.14.

An example analysis of a plane truss structure appears in the next section, and a computer program for the analysis of plane trusses is presented in Sec.

###### 5.7.

4.12 Example. The plane truss shown in Fig. 4-23a is to be analyzed using the methods described in the previous section. The truss is restrained at points C and D by hinge supports that prevent translations in both the x and y directions. The loads on the truss consist of both joint loads and member loads.

An arbitrary system for numbering the members and joints is given in Fig. 4-23b, which shows the restrained structure. Member numbers are indicated in

(0)

###### t o.3L-.J I 0

###### 0.6L--1

(b)

3 ~~~~~----~==4~-------X

###### Fig. 4-23. Example (plane truss).

![image 337](Matrix Analysis of Framed Structures_images/imageFile337.png)

4.12 Example 229

Table 4-18

Joint Information for Truss of Fig. 4-23a

Restraint loint Coordinates List

x y x y I 0 0.8L 0 0

- 2 0.6L 0.8L 0 0
- 3 0 0 I I
- 4 0.6L 0 1 I


circles adjacent to the members, and joint numbers are indicated by numbers adjacent to the joints. The numbering system for joint displacements is represented by numbers adjacent to the arrows, which denote the positive directions of the possible displacements. Of course, the displacement numbering system derives from the joint numbering system according to Eqs. (4-27). Note that the system shown in Fig. 4-23b for numbering the joints (and hence the displacements) obviates the necessity of rearranging the matrices in the analysis. However, this will not be the case in general.

With the origin of coordinates selected at joint 3, as shown in Fig. 4-23a, the x and y coordinates of that point are both zero. Coordinates for all of the joints in the structure are given in Table 4-18 in terms of the length L of one of the diagonal members. Table 4-18 also gives the restraint list for the structure. As in the continuous beam example, the integer I in the restraint list indicates that a restraint exists, and the presence of a zero indicates that a restraint does not exist.

Table 4-19 contains the member information for the truss of Fig. 4-23a (note that the cross-sectional areas are proportional to the lengths). The member numbers, joint numbers, and cross-sectional areas are essential data, but the lengths of members and their direction cosines can be computed from the coordinates of the joints at the ends of the members (see Eqs. 4-24 and 4-25). Note that the arbitrary choice of which end of a member is to be denoted j or k determines the signs of the direction cosines.

As a preliminary step for generating the over-all joint stiffness matrix SJ, the

Table 4-19

Member Information for Truss of Fig. 4-23a

Direction Cosines

Member jointj loint k Area Length Cx C y

I 1 2 0.6A\. 0.6L 1.0 0

- 2 3 4 0.6Ay 0.6L 1.0 0
- 3 3 I 0.8A\ 0.8L 0 1.0
- 4 4 2 0.8A\ 0.8L 0 1.0
- 5 I 4 A.\ L 0.6 -0.8
- 6 3 2 Ay L 0.6 0.8


![image 338](Matrix Analysis of Framed Structures_images/imageFile338.png)

230 Chapter 4 Computer-Oriented Direct Stiffness Method Table 4-20 Member Stiffness Matrices for Structural Axes

or

###### 8."~Ed-!

8""~Ed-1

0 EJ)

0 -1

- 0 0 o 2 0 0 o 6
- 0 1 o 3 0 1 o 7 0 0 o 4 0 0 o 8


°IT

1 2 3 4 5 6 (j) 8 0 0 0

###### "]' u

###### MX[ T

0 0

EAx 1 0 -1 8

0 1 0 -1 6

SMS3 =T 0 0 0 o 1 SMS4 = T 0 0 o 3 0 -1 0 1 2 -1 0 1 4 5 6 1 2 7 8 3 4

-0.48 -0.36 0.48] I

[ 036

EAx -0.48 0.64 0.48 -0.64 2 S~IS5 = T -0.36 0.48 0.36 -0.48 7 0.48 -0.64 -0.48 0.64 8

1 2 7 8

[ 0.3. 0.48 -0.36 -0.48],

EA 0.48 0.64 -0.48 -0.64 6 SMS6 = LX -0.36 -0.48 0.36 0.48 3 -0.48 -0.64 0.48 0.64 4

5 6 3 4

individual member stiffness matrices SMSi are summarized in Table 4-20. These matrices are formed from Table 4-15 given in Sec. 4.lO. The elements of each of these matrices may be transferred to the appropriate locations in SJ by calculating the indexes jl, j2, kl, and k2 given by Eqs. (4-27) and then making the transfers according to Eqs. (4-28) through (4-31). As an aid in this process, the numerical values of the indexesjl,j2, kl, and k2 are given in Table 4-20 down the right-hand side and across the bottom of each matrix SMS;' As an example of the transferring process, consider the element (SMS13)2' which is the element in the first row and third column of the matrix SMSi for member 2. This element is encircled in Table 4-20, and its value is - EAxlL. The row and column indexes of SJ for the element are also encircled in Table 4-20. They indicate that the element is to be transferred to the position in the fifth row and the seventh column ofthe matrix SJ. This element is encircled in Table 4-21, which shows the appearance of the matrix SJ after the

###### Table 4-21

Joint Stiffness Matrix for Truss of Fig. 4-23a

1.36 -0.48 -1.00 0 I 0 0 -0.36 0.48

- -0.48 1.64 0 0 II 0 -1.00 0.48 -0.64
- -1.00 0 1.36 0.48 II -0.36 -0.48 0 0


0 0 0.48 1.64 I -0.48 -0.64 0 -1.00

I I

L ------------------------------+------------------------------

SJ = EAx

I

0 0 -0.36 -0.48 II 1.36 0.48 E-1.00) 0 0 -1.00 -0.48 -0.64 II 0.48 1.64 0 0

-0.36 0.48 0 0 II -1.00 0 1.36 -0.48 0.48 -0.64 0 -1.00 ,I 0 0 -0.48 1.64

![image 339](Matrix Analysis of Framed Structures_images/imageFile339.png)

4.12 Example 231

Table 4-22

Inverse of Stiffness Matrix

r2.50l

-OWl 1

0.733 2.053

S-I =~ 0.733 0.824 0.601 -0.176 FF EAx 2.053 0.601 2.503 -0.733 -0.601 -0.176 -0.733 0.824

transferring process is completed. The matrix is partitioned in accordance with Eq. (4-8), and the 4 x 4 stiffness matrix SFF appears automatically in the upper left-hand portion with no necessity for rearrangement in this example. The inverse of the matrix SH' is shown in Table 4-22 for use in subsequent calculations.

The loads applied to the structure appear in Fig. 4-23a. Those applied at joints are listed in Table 4-23, and the actions at the ends of the members in the restrained structure (caused by loads on members) are summarized in Table 4-24. The joint loads are placed in the vector AJ (see Eq. 4-32). Hence,

AJ = P{0,0,2, 1,0,0,0,0}

Actions in the rows of Table 4-24 form columns of the matrix AML. Next, the elements of AML are transferred to the vector of equivalent joint loads AE, as indicated by Eqs. (4-33). The resulting vector is as follows:

AE = P{1.0, 2.0,0.5, -2.5, 1.0, -1.0,0.5, -1.5}

To understand how the terms in vector At: are obtained, consider the loaded members one at a time. As an example, member 4 has itsj end at joint 4 and its k end at joint 2. Consequently, its direction cosines are Cx = 0 and Cj" = 1.0 (see Table 4-19). For this member Eqs. (4-33) yield

(AEh = -lAMS + (A",fL)2.~ (AEls = -lAMS - (AMLh.4

- (AE)3 = -lAMS + (AML)4,4
- (AE)4 = -lAMS - (AMLh.4


Thus, the contributions of member 4 to At: are

AE4 = P{O, 0, 0.5, -0.5,0,0,0.5, -0.5} and so on for the other loaded members.

Then the vectors AJ and AE are added (see Eq. 4-7) to form the combined load vector Ac, as follows:

Table 4-23

Actions Applied at Joints

Force in x Force in y Direction Direction

loint

- 1 0 0
- 2 2P P
- 3 0 0
- 4 0 0


![image 340](Matrix Analysis of Framed Structures_images/imageFile340.png)

232 Chapter 4 Computer-Oriented Direct Stiffness Method

Table 4-24

###### Actions at Ends of Restrained Members Due to Loads

Member (A.llLki (AJlLh,i (AJlLhi (A,\IlJ.,i

I 0 -2P 0 2P

- 2 0 P 0 P
- 3 0 P 0 P
- 4 0.5P 0,5P 0.5P 0.5P
- 5 0 0 0 0
- 6 0 0 0 0


Ac = P{ 1.0,2,0,2.5, -1.5, 1.0, -1.0,0.5, -1.5}

As mentioned earlier, there is no need to rearrange this vector. The first four elements constitute the vector

AFc = P{ 1.0, 2.0, 2,5, -1.5} and the last four elements are

ARC = P{1.0, -1.0,0,5, -1.5}

The solution may be completed by first calculating the free joint displacements DF, using Eq. (4-3), with the following result:

DF -- S-!FFAFc -_ EA,\PL {10,001,4.147,10.611, -4,020}

The vector DJ for this structure contains the vector DF in the first part and zeros in the latter part.

PL

DJ = EA,\ {10.001, 4.147, 10.611, -4,020,0,0,0, O}

In the next step the support reactions AR are computed using Eq, (4-4) with the matrix SRF obtained from the lower left-hand portion of Table 4-21

AR = -ARC + SRFDF = P{-2.89, -5.67, -2.11, 7.67}

As the last step in the analysis, the member end-actions AMi are obtained for each member by applying either Eq. (4-5) or Eqs. (4-34). The results of these calculations are summarized in Table 4-25. This step completes the analysis of the plane truss structure for the given loads,

Table 4-25

###### Final Member End-Actions

Member (AM)!,i (A,uL (A,Ula.i (A,lI).,i

###### I -0.61OP -2.000P 0.61OP 2.000P

- 2 0.0 l.OOOP 0.0 I.OOOP
- 3 -4.147P I.OOOP 4.147P l.OOOP
- 4 4.520P 0.500P -3.520P O.500P
- 5 2.683P 0.0 -2.683P 0.0
- 6 -3.150P 0.0 3.150P 0.0


![image 341](Matrix Analysis of Framed Structures_images/imageFile341.png)

4.13 Rotation of Axes in Two Dimensions 233

4.13 Rotation of Axes in Two Dimensions. As mentioned previously in Sec. 4.10, the direct method of formulating member stiffnesses is satisfactory for continuous beams and trusses. On the other hand, a method employing rotation of axes is well suited to more complex structures. In this section rotation of axes for two-dimensional vectors is formulated on a geometric basis, and in the next section the method is applied in the analysis of plane trusses. Then in Sec. 4.15 the subject of rotation of axes in three dimensions is discussed, and in subsequent sections other types of structures are treated using this technique.

In order to begin the discussion, consider an action A, which lies in the X-Y plane (see Fig. 4-24). Two sets of orthogonal axes with origin at 0 are shown in the figure. The xs, Ys axes will later be taken parallel to a set of structural reference axes, and the XM, YM set will be taken as a pair of memberoriented axes. The XM, YM axes are rotated from the xs, Ys axes by the angle 'Y. Let the direction cosines of the XM axis with respect to the axes Xs and Ys be All and 11.12, respectively. It is evident from Fig. 4-24 that these direction cosines may be expressed in terms of the angle 'Y as follows:

All = cos 'Y 11.12 = cos(90° - 'Y) = sin 'Y (a)

Also, let the direction cosines of the YM axis with respect to the axes Xs and Ys be A2J and 11.22, respectively. These direction cosines may also be expressed in terms of the angle 'Y.

A21 = cos(90° + y) = - sin y A22 = cos Y (b)

For anyone of the direction cosines above, the first subscript refers to the XM. YM axes, and the second subscript refers to the Xs. Ys axes. Moreover, the number 1 denotes the x direction (either XM or xs), and the number 2 denotes the Y direction (either YM or Ys). For example, AI2 is the direction cosine of the XM axis with respect to the Ys axis.

###### 1\

###### \

I ~M

o

Axs

Fig. 4-24. Rotation of axes in two dimensions.

![image 342](Matrix Analysis of Framed Structures_images/imageFile342.png)

The action A may be resolved into two orthogonal components Axs and Ays in the Xs and Ys directions, respectively, as shown in Fig. 4-24. Alternatively, A may also be resolved into two orthogonal components AXM and A YM in the directions XM and YM, respectively, as shown also in the figure. The latter set of componen'ts may be expressed in terms of the former set by inspection of the geometry in Fig. 4-24. It may be observed that AXM is equal to the sum of the projections ofAxs and Ays on the XM axis. In addition, A YM is equal to the sum of the projections ofAxs and Ays on the YM axis. Therefore, the expressions for AXM and A YM are

AXM = AllAxs + A12Ays A YM = A21A XS + A22A YS

(c)

In matrix form, these equations become

(4-35)

Substitution of expressions (a) and (b) into Eq. (4-35) yields the following alternative form:

###### [~'::J =[_~~s: ~~~ ~J[~'::J (4-36)

Equations (4-35) and (4-36) may also be stated in concise form by the expression

(4-37)

In this equation, AM is a vector consisting of the components of the action A parallel to the XM, YM axes, As is a vector containing the components of the action A parallel to the Xs, Ys axes, and R is a matrix of direction cosines which will be referred to as the rotation matrix. As shown by Eqs. (4-35) and (4-36), the rotation matrix in a two-dimensional problem is as follows:

(4-38)

It is also possible to express the Xs. Ys set of components of the action A in terms of the XM. YM set of components. This transformation may be accomplished by observing that Axs is equal to the sum of the projections ofAxM and A YM on the Xs axis, and that Ays is equal to the sum of the projections ofAxM and A YM on the Ys axis. Thus,

Axs = AllAxM + A21A YM A YS = A12AxM + A22A YM

(d)

When expressed in matrix form, these equations become

[AXSJ = [All A21J[AXMJ

(4-39)

A YS A12 A22 A YM

![image 343](Matrix Analysis of Framed Structures_images/imageFile343.png)

4.14 Application to Plane Truss Members 235

or

###### 'Y] [AXM] cOS'Y AYM

###### [AXSJ = [C?S 'Y

Ays sm 'Y - sin

(4-40)

Equations (4-39) and (4-40) may be represented concisely by the matrix equation

(4-41) in which RT is the transpose of the rotation matrix R.

Finally, from Eqs. (4-37) and (4-41) it is apparent that the transpose of R is equal to its inverse.

(4-42) Therefore, the rotation matrix R is an orthogonal matrix.*

Because small displacements as well as actions may be treated as vectors, the relationships formulated above for the action A may be applied equally well to a small displacement D. Thus, equations similar to Eqs. (4-37) and (4-41) can be written for displacements, as follows:

- (4-43)
- (4-44)


DM = RDs Ds = RTDM

In these equations the vector DM consists of the components of the displacement D parallel to the member axes, and the vector Ds contains those parallel to the structural axes.

The concepts of rotation of axes discussed above are applied to plane truss structures in the next section.

4.14 Application to Plane Truss Members. A typical plane truss member;, framing intojointsj and k at the ends, is shown in Fig. 4-25. For

###### L,

y

###### Fig. 4·25. Rotation of axes for plane truss member

*For further discussion of orthogonal matrices, see any text on matrix algebra.

![image 344](Matrix Analysis of Framed Structures_images/imageFile344.png)

convenience, the member is oriented in such a manner that its direction cosines are positive. The member axes XM, YM are rotated through the angle 'Y from the axes xs, Ys, which are parallel to the reference axes x, Y for the structure as a whole. For the purpose of rotational transformations it is immaterial whether one refers to the xs, Ys set of axes or the parallel x, Y set.

As a preliminary step in the use of rotation of axes in a plane truss analysis, the rotation matrix R will be expressed in terms of the direction cosines of the member axis XM. Inspection of Fig. 4-25 shows that the direction cosines of that axis in terms of the angle 'Yare

Cx = cos 'Y Cy = sin 'Y Then the rotation matrix (see Eq. 4-38) becomes

R = [ C?S 'Y sin 'Y] = [ Cx -sm'Y cOS'Y -Cy

(4-45)

Next, the action-displacement relationships in the XM and YM directions at the ends of member i may be expressed by the following:

(4-46)

Equation (4-46) is the same as Eq. (4-5) when the vector AML;, which appears in the latter equation, is null. Thus, Eq. (4-46) gives the actions at the ends of the member due to the displacements of the ends. The member stiffness matrix SMi (see Eq. 4-46) was developed in Sec. 4.10 and presented in Table 4-14. The objective now is to transform this matrix for member axes into the matrix SMSi for structural axes (see Table 4-15).

Before transforming it to structural axes, Eq. (4-46) may be written in partitioned form (omitting the SUbscript i), as follows:

1!;AMI]=[SMll~!;:--1;;:-r~;:~--~-~:~SMI2: SMI3 SMI4] lDMI]~!;

###### [

(a)

###### AM4 SM41 SM42: SM43 SM44 DM4

The SUbscripts 1, 2, 3, and 4 used in this equation refer to the memberoriented directions shown in Fig. 4-14c. Equation (a) may also be written in the following manner:

[ AMi] = [SMii SMik] [DMi] AMk SMki SMkk DMk

(b)

In this equation the subscripts j and k attached to the submatrlces refer to thej and k ends of the member. The terms AMi> AMk, DMi, and DMk in Eq. (b) represent two-dimensional vectors (either actions or displacements) at the ends of the member in the directions of member axes (see Fig. 4-14c). Therefore, they can be expressed with respect to the structural axes (see Fig. 4-14b) by using the appropriate rotation formulas from the preceding section.

![image 345](Matrix Analysis of Framed Structures_images/imageFile345.png)

- 4.14 Application to Plane Truss Members 237


These fonnulas are Eqs. (4-37) and (4-43). When these relations are substituted into Eq. (b), it becomes

###### [:!:~J = [~;~~ ~::J [:g:~J (c)

The submatrices ASh Ask. Dsj, and DSk represent the two-dimensional action and displacement vectors at the ends of the member with respect to the structural axes.

An equivalent fonn of Eq. (c) is the following:

To simplify the writing of this equation, let RT be the rotation transformation matrix for actions and displacements at both ends of the member.

RT = [~ ~J (4-47)

Equation (d) then may be rewritten as follows:

(e)

The vectors As and Ds in Eq. (e) consist of the actions and displacements at the ends of the member in the directions of structural axes (see Fig. 4-14b).

Premultiplying both sides of Eq. (e) by the inverse of RT gives:

(f)

Since the submatrix R is orthogonal, the matrix RT is also orthogonal. This fact can be seen by multiplying RT by its transpose, as follows:

RtRT= [~T ~TJ [~ ~J = [R~R R?RJ

= [R~R R~RJ = [~ ~J = I

Hence, the transpose of RT is also the inverse of RT:

RTI = Rt (4-48) and substitution of Eq. (4-48) into Eq. (f) yields:

As = RtSMRTDs (4-49)

Since the action-displacement equation that relates the actions As and displacements Ds is

(4-50)

in which SMS is the member stiffness matrix for structural axes, it is readily seen by comparing Eqs. (4-49) and (4-50) that

![image 346](Matrix Analysis of Framed Structures_images/imageFile346.png)

(4-51) Evaluation of the matrix SMS from this equation is performed as follows:

###### SMS = l~;-~~;_LLJl

- o 0 ,Cx -Cy
- o 0 iCy Cx


###### L ,--: L lc,. c,:, 0 01

,

EAx

###### :-EAx

0

0

0 0 0 0 -Cy c,: 0 0

X ---------- --------- ---- -----1----- ----

0 o 0 i Cx Cy L L o 0 :-Cy c,

-EAx

EAx

0

0 0 0 0

When this matrix multiplication is executed, the result is the matrix SMS (see Table 4-15), which was previously obtained by direct formulation.

In addition to the transformation of the member stiffness matrix from member axes to structural axes, the rotation of axes concept can also be used for other purposes in the stiffness method of analysis. One important application arises in the construction of the equivalent load vector AE from elements of the matrix AML. Contributions to the former array (the elements of which are in the directions of structural axes) from the latter array (which has elements in the directions of member axes) may be obtained by the following transformation:

(4-52)

In this expression the vector AMSi represents fixed-end actions in the directions of structural axes, whereas the vector AMLi is the i-th column of the matrix AML. In expanded form, Eq. (4-52) becomes

The resulting terms in AMSi, with the signs reversed, represent the incremental portions of AE given previously in Eqs. (4-33).

Another significant application of the rotation of axes concept appears in the calculation of final member end-actions. This computation consists

![image 347](Matrix Analysis of Framed Structures_images/imageFile347.png)

- 4.15 Rotation of Axes in Three Dimensions 239


of the superposition of the initial actions in member i and the effects ofjoint displacements. This superposition procedure is expressed by Eq. (4-5), which is repeated here.

(4-5)

The vector DM i in this equation must be ascertained from the vector ofjoint displacements DJ• The latter displacements are in the directions of structural axes, but the former displacements are in the directions of member axes. Therefore, the vector DM i may be obtained by the following transformation:

(4-53)

in which DJi is the vector ofjoint displacements for the ends of member i. Substitution of Eq. (4-53) into Eq. (4-5) produces the following expression:

(4-54)

Equation (4-54) may also be written in the expanded form

(AM)l,;ll(AML)l,i1

(AMh,i _ (AML)2,i (AMh.i - (AMLh.i (AMki (AML)4,i

[

###### +EAxil~ ~ -~ ~l [-~:: ~;: ~ ~ llig~~~:1

L; - o1 00 01 00 00 00 -CCx;Yi CCXtYi (D(DJJhi)k2

In this expression the subscripts jl, j2, kl, and k2 carry the definitions given previously by Eqs. (4-27). When the matrix multiplications indicated above are performed, the resulting four equations are the same as Eqs. (4-34) obtained in Sec. 4.11 by direct formulation.

In summary, the concept of rotation of axes has several useful applications in the stiffness method of analysis. The member stiffness matrix for members axes SM i may be transformed into the member stiffness matrix for structural axes SMS i by means of Eq. (4-51). In addition, the contributions AMsi to the equivalent load vector AE from a given member may be evaluated conveniently by rotation of axes, as shown by Eq. (4-52). Also, the final member end-actions can be obtained by the rotation ofaxes formulation given by Eq. (4-54).

It will be seen later that the matrix equations given above for rotation ofaxes in plane trusses can be generalized and applied to more complicated types of structures.

4.15 Rotation of Axes in Three Dimensions. Consider the action A shown in three dimensions in Fig. 4-26. The two sets oforthogonal axes Xs. Ys, Zs and XM, YM, ZM are analogous to the two sets of axes in the two-

![image 348](Matrix Analysis of Framed Structures_images/imageFile348.png)

240 Chapter 4 Computer-Oriented Direct Stiffness Method

![image 349](Matrix Analysis of Framed Structures_images/imageFile349.png)

-------71

A~ / I

###### _-'1\/,/'>(/ /\ I___! XM

\ AXM-----r

###### \ / I

###### I \ / Axs

/

Fig. 4-26. Rotation of axes in three dimensions.

dimensional case in Fig. 4-24. Let the direction cosines of the XM axis with respect to the xs, ys, Zs axes be AU, A12, and A13' They are defined to be the cosines of the angles between the axis XM and the three axes xs, Ys, and zs, respectively. Also, let the direction cosines for the YM axis be A21> A22, and A23, and let those for the ZM axis be A31> A32, and A33'

The action A may be represented by a set of three orthogonal components Axs, Ays, and Azs in the xs, Ys, and Zs directions, respectively, as shown in Fig. 4-26. Alternatively, this action may be represented by a second set of components AXM, AyM, and AZM in the XM, YM, and ZM directions, which are also indicated in the figure. The latter components may be related to the former as in the two-dimensional case. For example, AXM is equal to the sum of the projections of Axs, Ays, and Azs on the XM axis. The components AYM and AZM can be expressed in a similar manner, and the following relationship results:

(4-55)

If a three-dimensional rotation matrix R is defined as follows,

A13] A23

(4-56)

A33

then Eq. (4-55) can be written in the form

![image 350](Matrix Analysis of Framed Structures_images/imageFile350.png)

- 4.16 Plane Frame Member Stiffnesses 241


A~I = RAs (4-57) which is the same form as Eq. (4-37) for the two-dimensional case.

It is also possible to express the xs, Ys, Zs set of components of the action A in terms of the xM, YM, ZM set of components. For example, Axs is equal to the sum of the projections of A.LI{, AY,I{, and AZM on the Xs axis. Expressing the components in this manner leads to the following relationship:

- (4-58)
- (4-59)


This equation may be written concisely as As = RTAM which is the same form as Eq. (4-41) in the two-dimensional case.

It is apparent from Eqs. (4-57) and (4-59) that the transpose of the 3 x 3 matrix R is equal to its inverse. Therefore, this matrix is orthogonal, as in the two-dimensional case.

Relationships corresponding to the above equations, which are derived for actions, hold also for the transformation of small displacements in three dimensions. Thus, the components D:\I of a displacement D in the XJ/, YAl> ZM directions may be written in terms of the components Ds in the xs, Ys, Zs directions as follows:

(4-60)

Also, the vector Ds may be expressed in terms of the vector DM by the relationship:

(4-61)

Equations (4-60) and (4-61) are of the same form as Eqs. (4-43) and (4-44) for the two-dimensional case. Thus, the relationships for rotation of axes in three dimensions are completely analogous to those for two dimensions, except that the matrix R is of order 3 x 3 instead of 2 x 2, and the vectors are of order 3 x 1 instead of 2 x 1.

4.16 Plane Frame Member Stiffnesses. In preparation for the analysis of plane frames, the member stiffness matrix for a typical plane frame member is developed in this section. The matrix is first formulated with respect to member axes and then transformed to structural axes by the method of rotation of axes.

Figure 4-27a shows a typical member i within a plane frame. The joints at the ends of the member are denoted j and k, as in previous structures. The orthogonal set of axes x, y, and Z shown in Fig. 4-27 are reference axes for the structure. The plane frarlle lies in the x-y plane, which is assumed to be a principal plane of bending for all of the members. The members of

![image 351](Matrix Analysis of Framed Structures_images/imageFile351.png)

242 Chapter 4 Computer-Oriented Direct Stiffness Method

###### t

-

(0)

z

###### x'"

\Y"2\ -rt7/ 2~iis

5 4/ 5

Y", \/ kt___ 4

-r

l~j I. 1

) ~

/3 3

###### ~: '01 j-. '0'

Fig. 4-27. Numbering system for a plane frame member.

the frame are assumed to be rigidly connected, and the significant displacements of the joints consist of translations in the x-y plane and rotations in the Z sense.

The possible displacements of the ends ofa typical member i are indicated in Fig. 4-27b for member-oriented axes XM, YM, and ZM. The member axes are rotated from the structural axes about the ZM axis through the angle 1'. The six end-displacements, shown in their positive senses, consist of translations in the XM and YM directions and a rotation in the ZM (or z) sense at the ends j and k, respectively. If unit displacements of these types are induced at each end of the member one at a time, the resulting restraint actions will constitute the elements of the member stiffness matrix SM; for member axes. These restraint actions may be drawn from cases (1), (2), (6), (7), (8), and (12) of Fig. 4-2 in Sec. 4.3. The resulting 6 X 6 member stiffness matrix for member axes is given in Table 4-26.

![image 352](Matrix Analysis of Framed Structures_images/imageFile352.png)

4.16 Plane Frame Member Stiffness 243

### 6:1,I

Table 4-26

Plane Frame Member Stiffness Matrix for Member Axes (Fig. 4-27b)

###### EAx

EAx

0 0

0

###### L L

12EI7-

###### 12EI7- 6EI7-

0

0

###### L" L2 L" L2

6E1z 2E1z

###### 6EI7- 4EI7-

0

0

###### L" L L" L

S:\Ii =

-------------------------------~-------------------------------

I I

EAx

EAx

o

o

o

###### o

###### I

L

L

###### I

6E1z :

12E1z

o

o

I

###### L2

L2

###### L"

I

###### I I

6E1z

4E1z

2EI7-

o

o

###### I I

L

###### L

I

Consider next the task of transforming the member stiffness matrix SM (omitting the subscript i) to the stiffness matrix for structural axes SMS' Figure 4-27c indicates the six possible displacements at the ends of member i in the directions of the structural axes. In order to transform the member stiffness matrix from member axes to structural axes, the rotation transformation matrix RT for a plane frame member is required. As a first step, the 3 x 3 rotation matrix R will be expressed in terms of the direction cosines of the member shown in Fig. 4-27b. This may be accomplished by writing the direction cosines A of the member axes in terms of the angle 'Y and then substituting the direction cosines Cx and Cy for the member, as follows:

.\13] [cos'Y sin'Y 0] [ CX

###### Cy 0]

(4-62)

.\23 = -sin'Y cOS'Y 0 = -CY

Cx 0

.\33 0 0 1 0

o 1

The rotation transformation matrix RT for a plane frame member takes the same form as Eq. (4-47).

###### RT = [~ ~J (4-63)

In Eq. (4-63) the submatrix R is the 3 x 3 rotation matrix given by Eq. (4-62).

Having the rotation transformation matrix on hand, one may then calculate the member stiffness matrix for structural axes using the type of operation shown previously by Eq. (4-51).

(4-64)

in which the matrix RT is given by Eq. (4-63). The member stiffness matrix that results from this transformation is presented in Table 4-27. This matrix will be used in the analysis of plane frames in the next section.

![image 353](Matrix Analysis of Framed Structures_images/imageFile353.png)

I7czEAx12ElzC'C',)__(EAx12El(EAx12EIz)C'CC(EAx12EIz)L'yIyy-T--VCxCL'[xL3[L3CLx+yI+yyX

,_ (EAx12EIzC')_(EAx_12EIz)CCIyL'xyyL'xL'T--VCxCLCLyL3ILL3++XXX

C6El_6Elz,zEAx12ElzC'I(EAx12Elz)_zx(EAx12Elz)CC_ (EAx12EIC')C'

_6ElCzIC~)_6ElzCC1zy_(EAx12EIEAx_12EIz) CxCC'C'_(EAx12Elz)CCy_(EAx12E/z+I

--------------------------------------------------+--------------------------------------------------

Iz6ElC

Iz6El6ElCz

2Elz6EII_6ElC4Elzzz_6ElCzz6ElCx

I4Elz6ElC_6El2Elzz_6ElCzzz6ElCIx

vL'IyCxL'LL'yLI

VCx IL'L'[['yyLI

yI-vcx-T--VCxCTCY+-VxL'LxLL3L'y+yXI

LxL3LL3yL'yL'L'+L'LYLXI

Plane Frame Member Stiffness Matrix for Structural(Fig. 4-27c)Axes

Table4-27

z(EAx12EIz)EAx12EIC'C' 6ElzCI

I

I

I

I

I

ISMS.=

t

![image 354](Matrix Analysis of Framed Structures_images/imageFile354.png)

4.17 Analysis of Plane Frames. In this section a procedure is given for analyzing plane frames of the type illustrated in Fig. 4-27a. Actions applied to such a frame are assumed to be forces in the plane of the structure (the x-y plane) or moment vectors normal to the plane.

As a preliminary step in the analysis, the members and joints of the structure must be numbered. The numbering techniques described in Sec. 4.11 for plane trusses may also be applied to plane frames. The joints are numbered consecutively 1 through nj, and the members are numbered consecutively 1 through m. The sequence of numbering is arbitrary, but each member and each joint must have a number.

Since both axial* and flexural deformations will be taken into account in the analyses of plane frames, the possibility exists for three independent displacements at each joint. These displacements are taken to be the translations of the joint in the x and y directions and the rotation in the z sense. Thus, the possible displacements at ajointj may be designated as follows:

3j - 2 = index for translation in the x direction 3j - 1 = index for translation in the y direction 3j = index for rotation in the z sense

In addition, the number of degrees of freedom n in a plane frame is calculated from the number of joints nj and the number of restraints n r by the following expression:

(4-65)

A particular member i in a plane frame will have joint numbers j and k at its ends, as shown in Fig. 4-28. Indexes for the possible displacements of the joints associated with this member are also shown in Fig. 4-28. These displacement indexes are calculated as follows:

Fig. 4-28. End-displacements for plane frame member.

*Ifaxial defonnations in members are to be omitted from the analysis, constraints must be introduced to prevent length changes of members (see Sec. 6.19).

![image 355](Matrix Analysis of Framed Structures_images/imageFile355.png)

246 Chapter 4 Computer-Oriented Direct Stiffness Method

jl = 3j - 2 kl = 3k - 2

j2 = 3j - 1 k2 = 3k - 1

- j3 = 3j
- k3 = 3k


(4-66)

In order to construct the joint stiffness matrix in an orderly fashion, the following procedure is recommended. First, the 6 X 6 stiffness matrix SMSi for structural axes is generated for the i-th member in the frame (see Sec. 4.16, Table 4-27). Member i contributes to the stiffnesses of joints j and k at the ends of the member. Therefore, appropriate elements from the matrix SMSi for this member may be transferred to the over-all joint stiffness matrix Sj through an organized handling of subscripts. The first column in the matrix SMSi consists of restraint actions at j and k due to a unit translation at the j end of member i in the x direction (index j 1). This column is transferred to the matrix S] as follows:

(5J)il,il = I 5MS + (5MSll)i (5J)i2,il = I 5MS + (5MS21)i (5J)i3JI = I 5MS + (5MS31)i (5Jhl,il = (5MS41)i (5J)k2,il = (5MS51)i (5Jh3,il = (5MS61)i

(4-67)

In these equations the first three stiffness coefficients consist of the sums of contributions from all members which frame into jointj, including member i. The last three stiffnesses involve contributions from member i only.

Expressions similar to Eqs. (4-67) may also be written for a unit translation of joint j in the y direction (index j 2).

(4-68)

Thus, the elements of the second column of SMS for member i are transferred as contributions to the matrix SJ'

Similarly, for a unit rotation of joint j in the z sense (index j3), the expressions for transferring the third column of SMS are

(5J)il,i3 = I 5MS + (5MSI3)i

(4-69)

Expressions for transferring the fourth column of SMS to the matrix SJ are similar to the above equations, except that the first three stiffnesses consist of contributions from member i only and the last three are sums of contributions from all members framing into joint k. Thus, for a unit translation ofjoint k in the x direction (index kl), the expressions are as follows:

(4-70)

![image 356](Matrix Analysis of Framed Structures_images/imageFile356.png)

Similarly, for a unit translation of joint k in the y direction (index k2), the expressions for transferring the fifth column of S~IS are

(4-71)

(S"h:1,k2 = ~ SMS + (SMS65);

Finally, for a unit rotation of joint k in the:: sense (index k3), the following equations apply:

(4-72)

(S")"':3,k:1 = ~ S.IIS + (S.11866);

In the process of transferring elements from the member stiffness matrix S~IS to the over-all joint stiffness matrix S.], as described above, there is no attempt to take advantage of the symmetry which exists in the matrices. Recognition of this symmetry allows short cuts in the transfer procedure which can readily be made.

Construction of the complete matrix SJ consists ofgenerating and transferring the matrix SMS for all members (l through In) of the structure. After the matrix S./ is generated, it must be rearranged if necessary into the form given by Eq. (4-8).

In the next phase of the analysis, vectors associated with loads on the frame are formed. External actions applied at joints constitute the vector A./. Figure 4-29 shows the actions at a typical joint k in a plane frame. The action (A J)3k-2 is the x component of the force applied at k,(AJhk-l is the y component of the applied force, and (AJhk represents a couple in the :: sense applied at the joint. Thus, the vector AJ will take the following form:

AJ = {(AJ)J, (AJ)z, (AJh, ... , (AJb-2' (AJhk-b (AJb, ... ,

(AJhu-2' (AJhu-h (AJhu} (4-73)

Figure 4-30b delineates the actions at the ends of a restrained plane frame member due to loads. End-actions for member i, with respect to member-oriented axes, are defined as follows:

###### ),

y

Fig." 4-29. Joint loads for a plane frame.

![image 357](Matrix Analysis of Framed Structures_images/imageFile357.png)

Chapter 4 Computer-Oriented Direct Stiffness Method

248

Fig. 4-30.

Loads on a plane frame member.

(AML)l,i = force in the XM direction at the j end (AML)2,i = force in the YM direction at the j end (AMLh.i = moment in the ZM sense at the j end (AML)4,i = force in the XM direction at the k end (AMLki = force in the YM direction at the k end (AML)6,i = moment in the ZM sense at the k end

These end-actions may be obtained from Appendix B for particular loading conditions. The matrix AML is an array of order 6 X m, in which each column consists of the elements listed above for a given member. Hence,

(AMdl,l (AMLh,i (AML)l,m1

AML = (A.~L!2'1 (AML)2,i (A~~~2,m

(4-74)

[

(AMLkl (AMLki (AML)6,m

The construction of the equivalent load vector AE may be executed by the method of rotation of axes, as was demonstrated previously for plane trusses in Sec. 4.14 (see Eq. 4-52). Figures 4-30a and c show the equivalent loads atj and k that receive contributions from member i. Fixed-end actions AMS;' in the directions of structural axes, can be computed using the relationship

(4-75) in which Rfi is the transpose ofthe matrix given by Eq. (4-63). The expres-

![image 358](Matrix Analysis of Framed Structures_images/imageFile358.png)

4.17 Analysis of Plane Frames 249

sions resulting from this operation, with their signs reversed, represent the incremental portions of AE contributed by the i-th member. Thus,

(AEb-2 = - ~AMS - Cxi(AMJJLi + CYi(AML)z,i (AEb-1 = - ~AMS - CYi(AMLh,i - Cxi(AML)2,i

(AEJ3j = - ~A.l1s - (A.I1Lhi

(4-76)

(AEhk-2 = - ~AMS - Cxi(AMLki + CYi(AML);,i (AEhk-l = - ~A'l1s - CYi(A.I1L)4,i - CdA.I1Lki

(AEhk = - ~AMS - (A,I1Lki

Addition of the vectors AJ and AE produces the combined load vector Ac, as given by Eq. (4-7). The vector Ac may then be rearranged if necessary into the form of Eq. (4-9).

After the generation of the required matrices is accomplished, substitution into Eqs. (4-3) and (4-4) yields the solution for free joint displacements DF (which is expanded into the vector DJ) and support reactions AR. Member end-actions in the plane frame may then be calculated by the same method as that indicated by Eq, (4-54) in Sec, 4,14 for plane trusses, The equation that corresponds to Eq, (4-54) is the following:

(4-77)

in which RT is again given by Eq, (4-63), Substitution of SMi from Table 4-26 and RTi for a plane frame member into this expression yields

EAxi

(AM)Li = (AML)I,i + L; {[(DJ);I - (DJhl]CXi

+ [(DJb - (DJ)k2]Cyi} 12Elzi

(AM)z,i = (AML)2,i - -----z;r- {[(DJ);I - (DJhl]CYi

- [(DJ);2 - (DJ)k2] CXi} +Lf [(DJ)j3 + (DJ)d

6Elzi

6Elzi

(AMhi = (AMLhi +---v-{-[(DJ)jl- (DJhl]CYi

+ [(DJ)i2 - (DJh2]CXi} +-----r:-, (DJ);3 +2"(DJ)k:l (4-78)

1 4ElZi [ 1 ]

EAxi

(AM)4,i = (AM1J4,i - L; {[(DJ)jl - (DJ)kl] CXi

+ [(DJ);2 - (DJ)k2] CYi}

(AM);,i = (AML);,i + -----z;r- {[(DJ)jl - (DJhl]CYi

12Elzi

- [(DJ)i2 - (DJ)dCXi} - ---v-, [(DJ)j:l + (DJ)d

6Elzi

![image 359](Matrix Analysis of Framed Structures_images/imageFile359.png)

250 Chapter 4 Computer-Oriented Direct Stiffness Method

In Eqs. (4-78) the subscripts j 1, j2, j3, k 1, k2, and k3 carry the meanings defined previously in Eqs. (4-66).

The next section contains an example analysis of a plane frame by the method described above, and a computer program for plane frames appears in Sec. 5.8.

4.18 Example. Figure 4-31a shows a plane frame having two members, three joints, six restraints, and three degrees of freedom. This frame is to be analyzed by the methods given in the previous section. For this purpose, assume that the crosssectional area Ax and the moment of inertia /z are constant throughout the structure. Assume also that the parameters in the problem have the following numerical values:

E = 10,000 ksi L = 100 in. /z = 1000 in.4 P = 10 kips Ax = 10 in.2

For this frame the material is aluminum, and units of kips, inches, and radians are used throughout the analysis.*

A numbering system for members, joints, and displacements is given in Fig. 4-31b, which shows the restrained structure. The sequence for numbering the joints is selected in such a manner that the matrices in the analysis do not require rearrangement.

(0)

###### r

2 ~ CD

###### / 3I

y

###### ,)-x (bJ

Fig. 4-31. Example (plane frame).

*Units for this example are in the United States (US) customary system. However. about half of the problems for Sec. 4.18 (given at the end of the chapter) are in the international (SI) system of units.

![image 360](Matrix Analysis of Framed Structures_images/imageFile360.png)

4.18 Example 251

###### Table 4-28

Joint Information for Frame of Fig. 4-31

Coordinates (in.) Restraint List

joint

-_. x y x y ,.I 100 75 0 0 () 2 0 75 I I I 3 200 0 1 I I

~--- ------- ----~-

Joint information is summarized in Table 4-28, which contains the joint numbers. joint coordinates. and the conditions of restraint. The member information for the frame is presented in Table 4-29. Substitution of the direction cosines for the members into Eq. (4-62) results in the rotation matrices Rl and R2 shown in Table 4-30.

###### Table 4-29

Member Information for Frame of Fig. 4-31

Moment

Area ofInertia Length Direction Cosines Member joint.i joint k (in. 2) (in.') (in.) Cx C l·

I 2 I 10 1000 100 1.0 0 2 I 3 10 1000 125 0.8 -0.6

###### Table 4-30

Rotation Matrices for Members of Frame of Fig. 4-31

-0.6 o1

0

I~]

[ OR

[ 10

Rj = ~ I.() Rz = o.~ 0.8 0

0 0 1.0 J

Table 4-31 Member Stiffness Matrices for Structural Axes

1000.0 0 0 -1000.0 0 0 4 0 120.0 6000.0 0 -120.0 6000.0 5 0 6000.0 400000.0 0 -6000.0 200000.0 6

S.\[SI = -1000.0 0 0 1000.0 0 0

0 -120.0 -6000.0 0 120.0 -6000.0 2 0 6000.0 200000.0 0 -6000.0 400000.0 3 4 5 6 2 3

534.1 -354.5 2304.0 -534.1 354.5 2304.0

-354.5 327.3 3072.0 354.5 -327.3 3072.0 2

2304.0 3072.0 320000.0 -2304.0 -3072.0 160000.0 3 -534.1 354.5 -2304.0 534.1 -354.5 -2304.0 7 354.5 -327.3 - 3072.0 -354.5 327.3 -3072.0 8 2304.0 3072.0 160000.0 -2304.0 -3072.0 320000.0 9

SW;2 =

2 3 7 8 9

![image 361](Matrix Analysis of Framed Structures_images/imageFile361.png)

-rIJ

-=~

###### =;-

###### 3

§i

###### ~::

7o.,;.

o::;.

###### .,.,..~

('j

('j

###### =-Ql

:l=-&.

Q..

'S.

~

'C

::!l

~IOO~O-------O--------O---:--IOO~O------O--------O--------0--------0---------6--

2304.0-2928.0720000.006000.0200000.0-2304.0-3072.0160000.0

-354.5447.3-2928.00-120.0-6000.0354.5-327.33072.0

2304.03072.0160000.0:000-2304.0-3072.0320000.0

1534.1-354.52304.0-1000.000-534.1354.52304.0

354.5-327.3-3072.0:000-354.5327.3-3072.0

-2304.0:000534.1-354.5-2304.0-534.1354.5

IS.J0-120.06000.0:0120.06000.0000=o-6000.0200000.0:06000.0400000.0000

Joint Stiffness Matrix for Frame ofFig. 4-31

Table4-32

I

###### I

I

I

I

![image 362](Matrix Analysis of Framed Structures_images/imageFile362.png)

4.18 Example 253

In preparation for generating the over-all joint stiffness matrix Sj, the member stiffness matrices are calculated. This may be done for each member by first generating the member stiffness matrix SMi for member axes (see Table 4-26, Sec. 4.16) and then calculating the matrix SMSi for structural axes by the rotation transformation of Eq. (4-64). For this purpose the matrix RTi for each member is composed as shown by Eq. (4-63). Alternatively, the matrix SMSi may be calculated directly for each member using Table 4-27. The resulting matrices are given in Table 4-31. The indexes jl through k3 (computed by Eqs. 4-66) are also indicated in Table 4-31 down the right-hand side and across the bottom of each matrix SMSi' These indexes may be used as a guide for the purpose of transferring elements to the matrix Sj. After the transferring process is accomplished, the over-all joint stiffness matrix that results is shown in Table 4-32. This matrix is partitioned in the usual manner, thereby isolating the 3 x 3 stiffness matrix SFF' The inverse of this matrix is given in Table 4-33.

Table 4-33

Inverse of Stiffness Matrix

I 798.0 632.5 0.01877

###### l

632.5 2798.0 9.355 x 10-6

SF}

0.01877 9.355 1.426

Next, the load information is processed, beginning with the joint loads shown in Table 4-34. The actions in this table are placed in the vector Aj , as indicated by Eq. (4-73).

AJ = {O, -10, -1000, 0, 0, 0, 0, 0, O}

Table 4-34

Actions Applied at Joints

Force in Force in Couple in Joint x Direction y Direction z Sense

(kips) (kips) (kip-in.)

I 0 -10 -1000

2 0 0 0 3 0 0 0

In addition, the actions in Table 4-35 are placed in the matrix AML and then transferred to the vector of equivalent joint loads AE in accordance with Eqs. (4-76). The following vector results:

AE = {O, -22, -50,0, -12, -200,0, -10, 250}

Adding the vectors AJ and AE produces the combined load vector Ac as follows:

Ac = {O, -32, -1050,0, -12, -200,0, -10, 250}

![image 363](Matrix Analysis of Framed Structures_images/imageFile363.png)

Table 4-35

Actions at Ends of Restrained Members Due to Loads

(A.ltd•.; (A.wd2.i (A.lII.)".; (A.III)'.; (A.lld•.; Member (kips) (kips) (kip-in.) (kips) (kips)

(A.wd6.i

(kip-in.)

1 0 12 200 0 12 2 -6 8 250 -6 8

- -200
- -250


The first three elements of this vector constitute the vector Apc

AFc = {O, -32, -1050} and the last six elements are the vector ARc,

ARc = {O, -12, -200,0, -10, 250}

Having all of the required matrices on hand, one may complete the solution by calculating the free joint displacements DF by Eq. (4-3) with the following result:

DF = SiJAFC = {-0.02026, -0.09936, -0.001797}

The first two elements in the vector DF are the translations (inches) in the x and y directions at joint 1, and the last element is the rotation (radians) of the joint in the z sense.

The vector DJ for this structure consists of the vector Dp in the first part and zeros in the latter part.

DJ = {-0.02026, -0.09936, -0.001797, 0, 0, 0, 0, 0, O}

In the next step the support reactions are computed, using Eq. (4-4) with the matrix SRP obtained from the lower left-hand portion of Table 4-32.

AR = -ARC + SRpDp = {20.26, 13.14,436.6, -20.26,40.86, -889.5}

Terms in the vector AR consist of the forces (kips) in the x and y directions and the moments (kip-inches) in the z sense at points 2 and 3.

As the final step in the analysis, the member end-actions AM; are calculated, using either Eq. (4-77) or Eqs. (4-78). The results of these calculations are given in Table 4-36, which completes the analysis ofthe plane frame structure.

Table 4-36

Final Member End-Actions

(,4..11),,; (,4..11)2.; (A.vJ3,; (,4..11)4.; (,4.Mh,i (A,\1)6,;

Member (kips) (kips) (kip-in.) (kips) (kips) (kip-in.)

I 20.26 13.14 436.6 -20.26 10.86 -322.9 2 28.72 -4.53 -677.1 -40.73 20.53 -889.5

4.19 Grid Member StitTnesses. A grid structure resembles a plane frame in several respects. All of the members and joints lie in the same plane, and the members are assumed to be rigidly connected at the joints

![image 364](Matrix Analysis of Framed Structures_images/imageFile364.png)

4.19 Grid Member Stiffnesses 255

(see Fig. 4-32a). Flexural effects tend to predominate in the analysis of both types of structures, with the torsional moments often being secondary in the grid analysis and axial strains often being secondary in the plane frame analysis. The most important difference between a plane frame and a grid is that forces applied to the former are assumed to lie in its own plane, whereas the forces applied to the latter are normal to its own plane. In addition, moments applied to a plane frame have their vectors normal to the plane of the structure, whereas moment vectors applied to a grid are assumed to lie in the plane of the structure. Both structures could be called plane frames, and the difference between them could be denoted by stating the nature of the loading system. Furthermore, if the applied loads were to have general orientations in space, the analysis of the structure could be divided into two parts. In the first part, the frame would be analyzed for the components of forces in the plane of the structure and moments normal to the plane; and the second part would consist of analyzing for the components of forces normal to the plane and moments in the plane. Superposition of these two analyses would then produce the total solution of the problem. Such a structure might be considered to be a special case of a space frame in which all of the members and joints lie in a common plane.

In analyzing a grid structure, the coordinate axes will be taken as shown

###### ~/

###### k

( b) (c)

###### Fig. 4-32. Numbering system for a grid member.

![image 365](Matrix Analysis of Framed Structures_images/imageFile365.png)

in Fig. 4-32a. The structure lies in the x-y plane, and all applied forces act parallel to the Z axis. Loads in the form of moments have their vectors in the x-y plane. The figure shows a typical member i framing into joints j and k. The significant displacements of the joints are rotations in the x and y senses and translations in the z direction. The six possible displacements at the ends of member i in the directions of structure axes are shown in Fig. 4-32c. The numbering system for these displacements is in the order mentioned above. The reason for numbering the rotations before the translation at each joint is to maintain a parallelism with the analysis of a plane frame, as can be seen by comparing the computer programs for plane frames and grids (see Secs. 5.8 and 5.9).

Figure 4-32b depicts the member i in conjunction with a set of memberoriented axes XM, YM, and ZM' These axes are rotated from the structural axes about the ZM axis through the angle 'Y. The XM"ZM plane for each member in the grid is assumed to be a plane of symmetry (and hence a principal plane of bending). The possible displacements of the ends of member i in the directions of member axes are also indicated in Fig. 4-32b. The six enddisplacements, shown in their positive senses, consist of rotations in the XM and YM senses and a translation in the ZM (or z) direction at the endsj and k, respectively. Unit displacements of these six types may be induced at the ends of the member one at a time for the purpose of developing the member stiffness matrix SM; for member axes. This matrix is of order 6 x 6, and it may be obtained from cases (3), (4), (5), (9), (10), and (11) of Fig. 4-2 in Sec. 4.3. The matrix which results is shown in Table 4-37.

Transformation of the member stiffness matrix from member axes (Fig. 4-32b) to structural axes (Fig. 4-32c) follows the same pattern as that for a

Table 4-37

Grid Member Stiffness Matrix for Member Axes (Fig. 4-32b)

_ Glx 0 0

Glx 0 0

L L

4Ely _ 6Ely 0

2Ely 6Ely

0

###### L V L V

0 _ 6Ely 12Ely 0 6Ely _ 12Ely

###### P [3 -IF L3

SMi= ------------------------------ -------------------------------

Glx 0 0

_ Glx 0 0

L L

4Ely 6Ely

2Ely _ 6Ely 0

0

L L2 L V

6Ely 12Ely

6Ely 12Ely 0

0

V L3 V VI

![image 366](Matrix Analysis of Framed Structures_images/imageFile366.png)

-(Jl§i

###### 3==

.,c;'}

s:

....~

###### '"'I

-=

to..>

r::r

.,I't

I't

~

~

L2x

-vCr

L2X

L2I'

12Elr

6Elr C

6Elr C

_ 6EI,C

12E1r

L"

L"

6Elr

6El2C2_ Glx2Elrr+yx_(G1x2EII)CCGIC2.4ElC2._(GIl'4E11)C.C,

++CrLL.,LLxCyLLLLx1I'V.11

GIy2EIyrCyI6ElC2C24ElrG1xx(GIl'2EII)-L_C(Gl4El)-T+T'+TnI+rCrCC1LLxCLLxL2YII'I'

+.\"LLI'

.,LL1 GIl'C2C24EII'

T-T-T+T+y+CxC-VCrCxC·LLLLxrI'I'X

yI6ElyyyrC2C2C2G1x4EI_ Gl2ElC2(Gl4EII)(Gl2EII)I'I

CL2I'V,L2L2I'XL"

VCrIL2L2L2xxrL"I

r6E1·12El,1. C_ 6EIrC_ 6EIr6E1r CI

12Ely6El,.yC_ 6ElC6EI_ 6E1r C,l

Grid Member Stiffness Matrix for Structural Axes (Fig. 4-32c)

I--------------------------------------------------~-------------------S"Si=

L2X (GIl'_4EI!:)C.C.

Table4-38

r

I

+LL'I' C_ 6Elr

+LLxI' _GI'C22E1"C2

xCC_(Gl2Ell')

![image 367](Matrix Analysis of Framed Structures_images/imageFile367.png)

plane frame (see Sec. 4.16). The rotation transformation matrix, which involves a rotation about the ZM axis, is exactly the same for both a plane frame member and a grid member because of the choice of numbering system mentioned above. This agreement between the two cases can be seen physically by comparing the orientation of the grid member in Fig. 4-32 with that of the plane frame member in Fig. 4-27. Thus, Eqs. (4-62) through (4-64) in Sec. 4.16 may be applied to a grid member as well as a plane frame member. Substitution of the matrix 8Mi from Table 4-37 into Eq. (4-64) results in the member stiffness matrix 8MSi for structural axes. This matrix

- is given in Table 4-38 and will be used subsequently in the analysis of grid structures.


4.20 Analysis of Grids. The first step in the analysis of a grid is to number the joints and members. This is done in the same manner as for a plane truss or plane frame. As mentioned in the preceding section, there are three possible displacements at each joint. These are the joint rotations in the x and y senses and the joint translation in the Z direction. Thus, the possible displacements at a joint j may be denoted by the following:

3j - 2 = index for rotation in the x sense 3j - 1 = index for rotation in the y sense 3j = index for translation in the Z direction

Note that these indexes are the same as those for the plane frame (see Sec. 4.17) but that the meanings are different in the grid structure. Because there are three possible displacements at each joint in both a grid and a plane frame, the number of degrees of freedom in a grid may be determined using Eq. (4-65) in Sec. 4. 17. Moreover, the indexes for the possible displacements of the two joints associated with member i may be calculated according to Eqs. (4-66) for either type of structure. These indexes are indicated for a grid member in Fig. 4-33. Since several of the steps in the analysis of a grid are symbolically the same as in the analysis of a plane frame, it is sufficient in much of the following discussion merely to refer to the plane frame analysis described in Sec. 4. 17.

The analysis of the restrained grid for joint stiffnesses follows the same

###### L,

z

- Fig. 4-33. End-displacements for grid member.


![image 368](Matrix Analysis of Framed Structures_images/imageFile368.png)

4.20 Analysis of Grids 259

###### L x

z

- Fig. 4-34. Joint loads for a grid.


pattern as in the analysis of a plane frame. The 6 x 6 member stiffness matrix S~IS j for each member is generated (see Table 4-38), and the elements of this array are transferred systematically to the joint stiffness matrix SJ. Equations (4-67) through (4-72) serve this purpose for a grid as well as for a plane frame.

The analysis of the restrained structure subjected to loads is also analogous to the plane frame, except that the types of actions involved are not the same. Consider first the vector of actions AJ applied at joints. Figure

- 4-34 shows the actions which may be imposed at a typical joint k in a grid. The action (AJhk-2 is the x-component of a moment vector applied at k, (AJhk-l is the y-component of the moment vector, and (AJhk represents a force in the z direction applied at the joint. Thus, the vector AJ may be formed in the sequence denoted by Eq. (4-73).


Actions AMLi at the ends of a restrained grid member (due to loads) appear in Fig. 4-35b. The end-actions for the i-th member, with respect to member axes, are defined as follows:

Fig. 4-35. Loads on a grid member.

![image 369](Matrix Analysis of Framed Structures_images/imageFile369.png)

(AML)I,i = moment in the XM sense at thej end (AMLh,i = moment in the Y M sense at the j end (AMLhi = force in the ZM direction at the j end (AMLki = moment in the XM sense at the k end (AML)5,i = moment in the YM sense at the k end (AML)6,i = force in the ZM direction at the k end

The matrix AML may be formulated as a rectangular array of order 6 x m of the type given by Eq. (4-74).

Construction of the equivalent load vector AE from the matrix AML is executed as described in Sec. 4.17 for plane frames. Figures 4-35a and

- 4-35c show the equivalent loads at joints j and k that receive contributions from member i. Equations (4-76) may be used for the purpose of computing these actions.


The calculation of displacements, reactions, and end-actions for a grid structure follows the same steps given previously for a plane frame (see Sec. 4.17). Joint displacements DF are computed, using Eq. (4-3), and then expanded into the vector DJ• Support reactions are calculated, using Eq. (4-4), and member end-actions are determined, using Eq. (4-77). In the latter equation the matrix RTi is given by Eq. (4-63), and the matrix SMi is obtained from Table 4-37. Substitution of these matrices into Eq. (4-77) produces the following expressions for end-actions:

Glxi

(AM)l,i = (AMLh.i + L. {[(DJ)jl - (DJhl]C;n

I

+ [(DJ)j2 - (DJ)k2] CYi}

(AMki = (AMLh,; + 4~y; { - [(DJ)jl +~ (DJhl] CYi

+ [(DJ)j2 +~ (DJh2] Cx} - 6~~Y; [(DJ)j3 - (DJh3]

6Ely;

(AMhi = (AMLh,i +U {[(DJ)jl + (DJ)ktl Cy;

- [(DJ)j2 + (DJh2]CXi} +---v- [(DJ)j3 - (DJ)d

12Ely;

(4-79)

I

Glxi

(AMki = (AMLki - L. {[(DJ)jl - (DJ)kl]CXi

I

+ [(DJ)j2 - (DJ)k2] CYi}

(AM)5,i = (AMLki + 4~Yi { - [~ (DJ)jl + (DJ)kl] Cy;

+ [~(DJ)j2 + (DJ)k2]CXi} - 6~~Yi [(DJ)j3 - (DJ)k3]

6EIYi

(AML)6,i - U {[(DJ)jl + (DJ)kl]CYi

[(DJ)j2 + (DJ)k2]CXi} - -z;r [(DJ)j3 - (DJh3]

12Ely;

![image 370](Matrix Analysis of Framed Structures_images/imageFile370.png)

4.21 Space Truss Member Stiffnesses 261

###### y

Z

Fig. 4-36. Space truss.

A computer program for the analysis of grids by the method described above is presented in Sec. 5.9. Numerical examples of the analysis of grid structures also appear in that section.

4.21 Space Truss Member Stiffnesses. Figure 4-36 shows a portion of a space truss structure in conjunction with a set of structural axes x, y, and z. A typical member i, framing into joints j and k, is indicated in the figure. All joints in the space truss are assumed to be universal hinges. Because of this idealization, rotations of the ends of the members are considered to be immaterial to the analysis. The significant joint displacements are translations, and these translations may be expressed conveniently by their components in the x, y, and z directions.

The possible displacements at the ends of a typical member i are indicated in Fig. 4-37a for member-oriented axes and in Fig. 4-37b for the structural axes. As usual, the member axes in Fig. 4-37a are arranged in such a

y

r----+--------~-----x

###### l

###### z

(0 ) ( b)

###### Fig. 4-37. Numbering system for a space truss member.

![image 371](Matrix Analysis of Framed Structures_images/imageFile371.png)

manner that the XM axis coincides with the axis of the member and has its positive sense from j to k. The YM and ZM axes lie in a plane that is perpendicular to the axis of the member and passes through end j. However, the precise orientation of these axes in the plane is immaterial at this stage of the discussion, because their position has no effect on the stiffness matrix for a truss member. In the next section, a particular choice for the directions of these axes will be made in order to facilitate the handling of load data.

The six end-displacements shown in Fig. 4-37a consist of translations in the XM, YM, and ZM directions at the ends j and k, respectively. The member stiffness matrix with respect to the member axes may be readily deduced from cases (1) and (7) of Fig. 4-2 in Sec. 4.3, and the resulting 6 X 6 matrix

- is given in Table 4-39. It can be seen that the only nonzero elements in this matrix are associated with displacements 1 and 4, which are in the direction of the XM axis (Fig. 4-37a). Thus, as mentioned above, the stiffness matrix for member axes is independent of the directions selected for the YM and ZM axes.


In order to transform the member stiffness matrix from member axes to structural axes, the rotation transformation matrix RT for a space truss member is required. This matrix takes the same form as that given by Eq. (4-63) for plane frames, and the transformation of SM to SMS is shown in Eq. (4-64). The 3 x 3 rotation matrix R required for RT is explained in the following discussion (omitting the subscript i).

The general form of the rotation matrix R is given by Eq. (4-56). The three elements AI), AI2 and AI3 in the first row of R are the direction cosines for the XM axis with respect to the structural axes. Therefore, these three elements are the same as the direction cosines for the member itself (All = Cx, AI2 = Cy, AI3 = Cz) and can be found from the coordinates of the ends of the member.

(4-80)

The length L of the member may also be computed from the coordinates of its end points.

(4-81)

Table 4-39

Space Truss Member Stiffness Matrix for Member Axes (Fig.4-37a)

![image 372](Matrix Analysis of Framed Structures_images/imageFile372.png)

4.22 Selection of Space Truss Member Axes 263

The elements in the last two rows of R (the direction cosines for the YM and Z.lfaxes, respectively) can be left in an indefinite form, so that the rotation matrix becomes

(4-82)

If this rotation matrix is substituted into Eq. (4-63) for RT and then both Rr and S:l1 (see Table 4-39) are substituted into Eq. (4-64), the result will be the 6 x 6 member stiffness matrix SMS for structural axes. This matrix, which contains terms involving only the direction cosines for the member itself, is given in Table 4-40.

Table 4-40

Space Truss Member Stiffness Matrix for Structural Axes (Fig. 4-37b)

n c,.c\ c,£\ - c~ -c}.cx -c;!:x C\.cy n· C,£y -C\.cy -C1' -C,£y

EAx S,IS; --- L

C\.cz C}.cz C~ I -C\Cz -C}.cz -C~

- -n -C}.cy -C'£x: n CyCx C,£y
- -C.\.cj' - C} -C,£ y C\.cy C} C,£y
- -C\CZ -Cy.cz - C~ C\CZ C}.cz C~


---------------------------~---~----------------------

4.22 Selection of Space Truss Member Axes. For the purpose of handling loads acting directly on the members of a space truss, it is necessary to select a specific orientation for all three member axes XM, YM, and ZM' Since the XM axis has already been selected as the axis of the member

- (see Fig. 4-37a), it remains only to establish directions for YM and ZM' For this purpose, the typical member i is shown again in Fig. 4-38, with axes


k

###### I

ILCy

I I /

###### I ic

f3________LjC; +cJ J- '--- ::::J.-1// Z

LCx

###### ~x

p

###### Fig. 4-38. Rotation of axes for a space truss member.

![image 373](Matrix Analysis of Framed Structures_images/imageFile373.png)

Xs, Ys, and Zs taken parallel to the structural axes. While many choices are possible for the directions of the YM and ZM axes, a convenient one is to take the ZM axis as being horizontal (that is, lying in the Xs-Zs plane), as shown in the figure. It follows that the YM axis is located in a vertical plane passing through the XM and Ys axes.

When the member axes are specified in the mannerjust described, there is no ambiguity about their orientations except in the case of a vertical member. When the member is vertical, it follows automatically that ZM will be in a horizontal plane; but its position in that plane is not defined uniquely. To overcome this difficulty, the additional specification will be made that the ZM axis is always taken to be along the Zs axis if the member is vertical. The two possibilities for this occurrence are shown in Figs. 4-39a and 4-39b.

In order to perform axis transformations, the rotation matrix R (see Eq. 4-82) is required. The direction cosines for the Y M and ZM axes (the last two rows of R) can be found directly from Fig. 4-38 by geometrical considerations. However, an alternate approach involves successive rotations of axes. In using the latter method, the transformation from the structural axes

- (see Fig. 4-38) to the member axes may be considered to take place in two steps. The first of these is a rotation through an angle {3 about the Ys axis. This rotation places the x axis in the position denoted as x(3, which is the intersection of the Xs-Zs plane and the XM"Ys plane. Also, this rotation places the ZM axis in its final position at the angle {3 with the Zs axis. The second step in the transformation consists of a rotation through an angle 'Y about the ZM axis. This rotation places the XM and YM axes in their final positions, as shown in the figure.


The rotation matrix R that is used in transforming from the structural to the member axes can be developed following the two steps described above. Consider first the rotation about the Ys axis through the angle {3. The 3 x 3 rotation matrix R(3 for this transformation consists of the direction cosines of the {3-axes (that is, the axes x{3' Y{3' Z(3) with respect to the structural axes (xs, Ys, zs)· Hence,

x'" (b)

###### Fig. 4-39. Rotation of axes for a vertical space truss member.

![image 374](Matrix Analysis of Framed Structures_images/imageFile374.png)

- 4.22 Selection of Space Truss Member Axes 265


COS f3 0

###### Si~f3]

(a)

R/3 = 0 1

[

-sin f3 0

cos f3

The functions cos f3 and sin f3 may be expressed in terms of the direction cosines of the member i by referring to the geometry of Fig. 4-38. Thus, these quantities become

cos f3 = -'CC¥ sm• f3 = -Cz (b)

xz Cxz

in which Cxz = .JC~ + C~. Substitution of these expressions into Eq. (a) gives the matrix R{3 in terms of the direction cosines.

Cx 0

Cz Cxz Cxz

R/3 = 0 0 (4-83)

0 Cx

-Cz

Cxz Cxz

The physical significance of the matrix R{3 is that it can be used to relate two alternative orthogonal sets of components of a vector (action or small displacement) in the directions of the f3-axes and the structural axes. For example, consider an action A that can be represented by either the vector A{3 (consisting of components in the directions of the f3 axes) or the vector As (consisting of components in the directions of the structural axes). The transformation of the latter vector into the former is performed by the method of Sec. 4.15, as follows:

A/3 = R/3As (c) where R/3 is given by Eq. (4-83).

The second rotation about the axis ZM through the angle 'Y may be handled in a similar manner. In this step a rotation matrix Ry again relates two orthogonal sets of components of the same vector for two sets of axes. In the case of an action A, the transformation is

(d)

In this equation the vector AM consists of the components of the action A in the directions of the member axes, and the matrix Ry contains the direction cosines of the member axes with respect to the f3-axes. Writing the matrix Ry in expanded form gives

o ~] (e)

sm 'Y cos 'Y

COS 'Y Ry = -s~ 'Y

[

The functions cos 'Y and sin 'Y may be expressed in terms of the direction cosines of the member as follows (see Fig. 4-38):

![image 375](Matrix Analysis of Framed Structures_images/imageFile375.png)

266 Chapter 4 Computer-Oriented Direct Stiffness Method

cos'Y = Cxz sin'Y = Cy CD

Substitution of these expressions into Eq. (e) yields the matrix Ry in the following form:

Cxz

###### C°xz °1

Ry = -~y Cy OJ

(4-84)

[

Now that the two separate rotations have been written in matrix form, the single transformation matrix R from the structural axes to the member axes can also be obtained. Again considering the case of an action A, it can be seen that the vector AM may be expressed in terms of the vector As by substituting AiJ (see Eq. c) into Eq. (d).

(g)

Comparing Eq. (g) with Eq. (4-57) in Sec. 4.15 shows that the desired rotation matrix R consists of the product of Ry and RiJ. Thus,

(4-85)

If Eqs. (4-83) and (4-84) are substituted into Eq. (4-85), the following matrix results:

C y C y Cz

-CyCZ

-CxCy

(4-86) R= Cxz C yZ

C YZ

-Cz

C y Cxz C yZ

###### °

This is the rotation matrix R for a space truss member. It may be used whenever actions or displacements are to be transformed between the member axes and the structural axes.

The preceding rotation matrix R is valid for all positions of the member i except when it is vertical. In either of the cases shown in Fig. 4-39a or Fig. 4-39b, the direction cosines of the rriember axes with respect to the structural axes can be determined by inspection. Thus, the rotation matrix is seen to be

###### C° °°y OJ1

(4-87)

This expression for R is valid for both cases shown in Figs. 4-39a and b. All that is necessary is to substitute for the direction cosine Cy its appropriate value, which is 1 for the member in Fig. 4-39a and -1 for the member in Fig.4-39b.

Substitution of the appropriate rotation matrix R (either Eq. 4-86 or

![image 376](Matrix Analysis of Framed Structures_images/imageFile376.png)

- 4.23 Analysis of Space Trusses 267


4-87) into Eq. (4-63) produces the desired rotation transfonnation matrix RT for the set of member-oriented axes specified in this section.

4.23 Analysis of Space Trusses. The analysis of space truss structures is presented in this section in a manner analogous to the previous discussions for other types of structures. Loads on a space truss structure usually consist of concentrated forces applied at the joints, but in some instances actions of a more general nature may be applied to the individual members, as indicated in Fig. 4-36. As with previous structures, members are numbered 1 through m, and joints are numbered 1 through nj.

Only axial defonnations are taken into account in the analysis of a space truss, but there exists the possibility of three independent translations at each

- joint j, as signified by the following indexes:


3j - 2 = index for translation in the x direction 3j - 1 = index for translation in the y direction 3j = index for translation in the z direction

The number of degrees of freedom in a space truss may be calculated using Eq. (4-65) in Sec. 4.17. In addition, the indexes for the possible displacements of the ends of member i may be detennined using Eqs. (4-66). These indexes are shown in Fig. 4-40 for a space truss member.

The analysis of space trusses is symbolically similar to the analyses of plane frames (Sec. 4.17) and grids (Sec. 4.20). The reason for the parallelism is that all three of these types of structures have three possible displacements per joint. The similarity begins in the first phase of the analysis, in which the 6 x 6 member stiffness matrix SMSi (see Sec. 4.21 for space truss member stiffnesses) is generated for each member in sequence. The elements of each of these member arrays are transferred systematically to the joint stiffness matrix SJ in the manner represented by Eqs. (4-67) through (4-72).

In the next phase of the analysis of a space truss, loads applied to the structure are processed. Figure 4-41 shows the actions applied at a typical

###### k2

![image 377](Matrix Analysis of Framed Structures_images/imageFile377.png)

###### t

y

;1'1;--k1 k3 I

I

###### I I

###### I

x

l _ I

###### - I

-- -J

Fig. 4·40. End·displacements for space truss member.

![image 378](Matrix Analysis of Framed Structures_images/imageFile378.png)

268 Chapter 4 Computer-Oriented Direct Stiffness Method

![image 379](Matrix Analysis of Framed Structures_images/imageFile379.png)

###### }-.

y

![image 380](Matrix Analysis of Framed Structures_images/imageFile380.png)

r

Fig. 4-41. Joint loads for a space truss.

- joint k in a space truss. The actions (AJb'-2' (AJb'-I, and (A./h" are the x, y. and z components ofthe concentrated force applied at the joint. These


actions are placed in the vector AJ , which takes the form given by Eq.

(4-73).

Consider next the matrix of actions AML at the ends of restrained members due to loads. In a truss structure these actions are determined with the ends of members restrained against translation but not against rotation (see Table B-5 of Appendix B). Figure 4-42b shows such a member i and the six end-actions caused by loading applied along its length. These end-actions are computed as the following;

(AML)l,i = force in the XM direction at the j end (AML)2,i = force in the yMdirection at the j end (AMLhi = force in the ZM direction at the j end (AML)4,i = force in the XM direction at the k end (AMLh.i = force in the YMdirection at the k end (AML)6,i = force in the ZM direction at the k end

![image 381](Matrix Analysis of Framed Structures_images/imageFile381.png)

Fig. 4-42. Loads on a space truss member.

![image 382](Matrix Analysis of Framed Structures_images/imageFile382.png)

4.23 Analysis of Space Trusses 269

The matrix AML is conveniently formulated as a rectangular array of order 6 x m, as represented by Eq. (4-74).

Transfer of elements from the matrix AML to the equivalent load vector AE may be accomplished by the method of rotation of axes, as explained previously. Equation (4-75) in Sec. 4.17 produces fixed-end actions AMSi in the directions of structural axes. For a skew member the rotation matrix given by Eq. (4-86) must be transposed and used in Eq. (4-75). Expressions resulting from that operation, with their signs reversed, become the incremental portions of AE contributed by the i-th member, as follows:

(4-88)

Equivalent joint loads receiving the above contributions appear in Figs. 4-42a and 4-42c.

On the other hand, if the member is vertical, the transpose of the rotation matrix given by Eq. (4-87) must be used instead. In this case Eqs. (4-88) for the incremental portions of AE simplify to

- (AEhj-2 = - IAMs + CYi(AML)2,i (AEb-l = - IAMs - CYi(AMLh,i (A Eb = - IA Ms - (AMLhi
- (AEhk-2 = - IAMs + CYi(AML)5,i (AEhk-l = - IAMs - Cy;(AML)4,i (AEhk = - IAMs - (AML)6,i


(4-89)

In the final phase of the analysis, joint displacements DF (translations in the x, y, and z directions) are computed by Eq. (4-3) and expanded into the vector DJ. Next, Eq. (4-4) provides the solution for support reactions (forces in the x, y, and z directions at supports). For the purpose of computing final end-actions, substitute the member stiffness matrix 8Mi from Table 4-39 and the rotation transformation matrix RTi for a space truss into Eq. (4-77). The equations that result from the matrix multiplications are the following:

EAxi

(AM)!,i = (AMLh,i + ---y;- {[(DJ)j! - (DJ)ktlCXi

+ [(DJ)j2 - (DJ)k2]CYi + [(DJ)j3 - (DJ)dCzi} (AJfh,i = (AML)2,j; (AM)3,i = (A,,,nh,i (4-90)

![image 383](Matrix Analysis of Framed Structures_images/imageFile383.png)

EAxi

(AMki = (AML)4,i - L; {[(DJ)il - (DJ)ktlCxi

+ [(DJ)i2 - (DJ)k2]CYi + [(DJ)i3 - (DJh3]CZi} (AMki = (AMLki; (AM)6,i = (AML)6,i

This set ofequations is valid for a member having any orientation, including a vertical member. In the latter case, the direction cosines CXi and C:i appearing in the equations will have the value zero.

A computer program for the analysis of space trusses is given in Sec. 5.10. Numerical examples may also be found in that section.

4.24 Space Frame Member Stiffnesses. Figure 4-43 shows a portion ofa space frame structure and a set of reference axes x, y, and z. A typical member i having positive direction cosines is indicated in the figure with joints at its ends denoted by j and k. The members of the frame are assumed to be rigidly connected at the joints, and each joint that is not restrained is assumed to translate and rotate in a completely general manner in space. Thus, all possible types of joint displacements must be considered and, for convenience, they are taken to be the translations and rotations in the directions of the x, y, and z axes (six possible displacements per joint).

y

x

1//

###### I / /

1// /

--------l: /

###### "'--",, I/ / /

------------~~

z

Fig. 4-43. Space frame.

The twelve possible displacements of the two ends of a member were discussed previously in Sec. 4.3 (see Fig. 4-1) for member-oriented axes and are indicated again in Fig. 4-44a for the typical member i. In this figure, the XM axis is taken along the axis of the member, in the same manner as for a space truss (compare with Fig. 4-38). The YM and ZM axes are selected as the principal axes of the cross section at end j of the member. The complete 12 x 12 stiffness matrix SMi for the member axes was given earlier in Table 4-1. This matrix must be transformed, by means of a rotation trans-

![image 384](Matrix Analysis of Framed Structures_images/imageFile384.png)

![image 385](Matrix Analysis of Framed Structures_images/imageFile385.png)

###### Z -----.I

ZM

(0 )

###### tl1

![image 386](Matrix Analysis of Framed Structures_images/imageFile386.png)

P 1'Ikt--a7 10

y

~ 91

t2 12 1 ~l i 1 I

;( 3 1 I 6 I 1

r------+------------+---------x

Fig. 4·44. Numbering system for aspace frame member.

formation matrix, into the 12 x 12 matrix SMSi' The latter matrix corresponds to the twelve types of displacements indicated in Fig. 4-44b in the directions of structural axes.

The form of the rotation matrix R depends upon the particular orientation of the member axes. In many instances a space frame member will be oriented so that the principal axes of the cross section lie in horizontal and vertical planes (for example, an I-beam with its web in a vertical plane). Under these conditions the YM and ZM axes can be selected exactly the same as for a space truss member (see Fig. 4-38), and the rotation matrix R given in Eq. (4-86) can be used for the space frame member as well.

There are other instances in which a space frame member has two axes of symmetry in the cross section and the same moment of inertia about each axis (for example, a circular or square member, either tubular or solid). In such cases the YM and ZM axes can again be selected as described in the preceding paragraph. This choice can be made because all axes in the cross section are principal axes, and any pair of axes can be selected for YM and ZM'

However, a space frame member may have its principal axes YM and ZM in general directions, as indicated in Fig. 4-44a. There are various ways in

![image 387](Matrix Analysis of Framed Structures_images/imageFile387.png)

![image 388](Matrix Analysis of Framed Structures_images/imageFile388.png)

###### )-.

y

z

Fig. 4·45. Rotation of axes for a space frame member.

which the orientation of these axes can be defined, and two methods will be described. The first method involves specifying the orientation of the principal axes by means of an angle of rotation about the XM axis. In order to visualize clearly how such an angle is measured, consider the three successive rotations from the structural axes to the member axes shown in Fig. 4-45. The first two rotations through the angles {3 and 'Y (about the Ys and Z(3 axes, respectively) are exactly the same as shown in Fig. 4-38 for the special case described above. The third transformation consists of a rotation through the angle a about the XM axis, causing the YM and ZM axes to coincide with the principal axes of the cross section. This last rotation is also indicated in Fig. 4-46, which shows a cross sectional view of the mem-

![image 389](Matrix Analysis of Framed Structures_images/imageFile389.png)

Fig. 4-46. Rotation about x Maxis.

![image 390](Matrix Analysis of Framed Structures_images/imageFile390.png)

ber looking in the negative X.u sense. The X,w),y plane is a vertical plane through the axis of the member, and the angle a is measured (in the positive sense) from that plane to one of the principal axes of the cross section.

The rotation of axes through the angle a requires the introduction of a rotation matrix R" in which the elements are the direction cosines of the member axes (XM' YM, ZM) with respect to the 'Yaxes.

R,=[001 co~a Sl~a] (4-91)

-sin a cos a

Premultiplication of RyR{3 (see Eq. 4-85 and accompanying discussion) by R" yields the rotation matrix R for the three successive rotations shown in Fig. 4-45.

(4-92)

When the three rotation matrices R" Ry , and R{3 (see Eqs. 4-91, 4-84, and 4-83) for a skew member are substituted into Eq. (4-92) and multiplied as indicated, the rotation matrix R becomes (omitting the subscript i)

Cz

_ -c.,Cy cosaCx- Cz sin a

###### r

-Cj,Cz cos a + Cx sin a Cxz

Cxzcos a

(4-93)

R - Cxz

CyCz sin a + Cx cos a Cxz

CxC y sin a - Cz cos a

-Cxzsin a

1.. Cxz

This rotation matrix is expressed in terms of the direction cosines of the member (which are readily computed from the coordinates of the joints) and the angle a, which must be given as part of the description of the structure itself. Note that if a is equal to zero, the matrix R reduces to the form given previously for a space truss member (Eq. 4-86). The special case of a vertical member will be discussed later.

The rotation transformation matrix RT for a space frame member can be shown to take the following form:

RT=[g ~ ~ g]

(4-94)

000 R

which is analogous to the matrix given in Eg. (4-63). Finally, the member stiffness matrix SMS for structural axes may be computed by the usual matrix multiplications.

SMS = R:j:SMRT (4-95)

The resulting matrix is quite complicated when expressed in literal form, and for that reason it is not expanded in the text. The fact that such a

![image 391](Matrix Analysis of Framed Structures_images/imageFile391.png)

lengthy set of relationships can be represented so concisely by Eq. (4-95) is one of the principal advantages of matrix methods in the analysis of structures.

In some structures the orientation of a particular member may be such that the angle a specifying the location of the principal axes for that member may not be readily available. In that event, a different technique for describing their location can be used. A suitable method is to give the coordinates of a point that lies in one of the principal planes of the member but is not on the axis of the member itself. This point and the XM axis will define without ambiguity a plane in space, and that plane can be taken as the XWYM plane. All that is necessary is to obtain expressions for the angle of rotation a, which appears in the rotation matrix R (Eq. 4-93), in terms of the coordinates of the given point and the coordinates of the ends of the member itself. Once this is accomplished, it becomes possible for the structural analyst to describe the position of the principal axes of a member either by giving the angle a directly or by giving the coordinates of a suitable point.

An arbitrary point p in the XWYM plane is shown in Fig. 4-45. The x, y, and z coordinates of this point (denoted as xP' Yp' and zp) are assumed to be given. Since the structural axes xs, Ys, and Zs have their origin at end j of the member, the coordinates of point p with respect to the structural axes (denoted as xps, Yps, and zps) are

(4-96) in which Xh Yh and Z,j are the coordinates of end j of the member.

The point p is also shown in Fig. 4-46 in conjunction with the rotation angle a. The coordinates of p with respect to the axesxy , Yy, andzy can be obtained in terms of those for the axes xs, Ys, and Zs by a rotation of axes through the angles f3 and )I. Let the coordinates ofpoint p with respect to the )I-axes be Xpy, ypy, and Zpy (the latter two coordinates are shown positive in Fig. 4-46). Then the desired transformation of coordinates becomes the following·

(a)

Substitution of RyRIl from Eq. (4-86) into Eq. (a) yields the following expressions:

Xpy = Cxxps + Cyyps + Czzps

ypy = - c-Xps + CxzYps - -CZps

CxCy CyCZ

(4-97) Cz Cx

xz xz

Zpy = --C Xps +-C Zps xz xz

![image 392](Matrix Analysis of Framed Structures_images/imageFile392.png)

4.24 Space Frame Member Stiffnesses 275

These equations give the coordinates of point p with respect to the y axes.

From the geometry of Fig. 4-46 the following expressions for the sine and cosine of the angle 0' are obtained:

ypy

cos 0' = -----r=i=~==;:=

(4-98)

Vy~ + z~

With Eqs. (4-96), (4-97), and (4-98) the quantities sin 0' and cos 0' can be

computed from the coordinates of point p and then substituted into the rotation matrix R (Eq. 4-93). This substitution produces the rotation matrix R in a form that involves only the direction cosines of the member itself and the coordinates of pointp.*

The preceding discussion dealt with a member that was not vertical. As shown in Sec. 4.22 for a space truss member, a vertical member is a special case that must be treated separately. The rotation matrix R given previously for a vertical space truss member (see Eq. 4-87) can also be used for certain types of vertical space frame members. The only requirement is that one of the principal axes of the cross section of the member be in the direction of the Zs axis. In some cases the member will be oriented in such a manner that this requirement is met (for example, an I-beam with its web in the Xs-Ys plane). The requirement is also satisfied by a member having a cross section that is either circular or square (solid or tubular). In these cases all axes of the cross section are principal axes, and hence one of them can arbitrarily be selected in the Zs direction.

In a more general case of a vertical member, the principal axes of the cross section will be rotated about the vertical axis so that they form an angle ex with the directions of the structural axes. The orientation of such a vertical member can best be visualized by considering the successive rotations of axes shown in Fig. 4-47. There is no rotation through the angle {3 (about the Ys axis) in this case. Instead, the first rotation is through the angle 'Y, which may be either 90° or 270° (see Figs. 4-47a and 4-47b, respectively). The second rotation is through the angle ex and about the XM axis. The rotation matrix for either of the cases shown in the figure can be obtained by inspection. It consists of the direction cosines of the XM, YM, and ZM axes with respect to the structural axes:

Rver! = [-Cy°cos0' ~Y si~0'] (4-99)

Cy sin 0' ° cos 0'

This expression is valid for both orientations shown in Figs. 4-47a and b, provided the appropriate value of Cy is substituted (+ 1in the first case and

"The rotation matrix R can also be derived from properties of the vector (or cross) product, as follows: ezM = exM x ejJvd'M + eJp ; eyM = ezM x exM' (In these expressions the symbol e represents a unit vector in the direction indicated by its subscripts.) Such vector operations appear simple because of efficient notation, but their expansions involve the same terms used in the more informative rotation of axes technique described herein.

![image 393](Matrix Analysis of Framed Structures_images/imageFile393.png)

276 Chapter 4 Computer-Oriented Direct Stiffness Method

![image 394](Matrix Analysis of Framed Structures_images/imageFile394.png)

Ys

![image 395](Matrix Analysis of Framed Structures_images/imageFile395.png)

###### T : 270·

(0 )

Fig. 4-47. Rotation of axes for a vertical space frame member.

-1 in the second case). It should be noted also that if a is equal to zero, the rotation matrix given in Eq. (4-99) reduces to the rotation matrix for a vertical space truss member (Eq. 4-87).

In those cases where it is desired to begin with the coordinates of a point p that is known to lie in a principal plane, it is possible to calculate sin a and cos a for use in Eq. (4-99) directly from the coordinates of the point. Figure 4-48a shows a vertical member with the lower end designated as jointj and the upper end designated as joint k. Also shown in the figure is the point p. When this point is located so that its coordinates with respect to the S-axes are positive, the angle a will be between 90° and 180°. The sine and cosine ofthis angle are as follows:

###### cos a =--::======

-XpS

sma• = ---;~======;;=ZpS

(b)

~+z~s

vx~s + z~s

On the other hand, Fig. 4-48b represents a vertical member with the lower end designated as joint k and the upper end designated as joint j. In this case the angle a is between 0° and 90° (when p has positive coordinates), and sin a and cos a are given by the following expressions:

![image 396](Matrix Analysis of Framed Structures_images/imageFile396.png)

![image 397](Matrix Analysis of Framed Structures_images/imageFile397.png)

Ys

(0) (b)

###### Fig. 4-48. Use of point p for a vertical space frame member.

![image 398](Matrix Analysis of Framed Structures_images/imageFile398.png)

sin a. = zps-

XpS

(c)

COS a = - -

.V/-'pS,.2 + '-'pB~2

•V/ xps2 + zps2

Expressions (b) and (c) may be combined into one set by introducing the direction cosine Cy for the member, as follows:

-xpS C

sin a• = ZpS- -

COS a = y

(4-100)

.v·/ \.2ps + ""'ps~2

.V/ XpS2 + ':::pS2

For the cases shown in Fig. 4-48a and 4-48b the direction cosine Cy has the values +1and -1, respectively. Equations (4-100) can be used to calculate sin a and cos a from the coordinates of point p. which must be located in a principal plane of the member. These functions can then be substituted into the rotation matrix R (Eq. 4-99).

In summary, the member stiffness matrix SMi for a space frame member is first obtained for the member axes using Table 4-1 in Sec. 4.3. Next, a rotation matrix R is constructed in a form that depends upon the case under consideration, using either the angle a or the coordinates of a point p to identify a principal plane. The matrix R has the form given in either Eg. (4-93) or Eg. (4-99), depending upon whether the member is inclined or vertical. In both of these cases, the angle a may be zero, which means that R reduces to one of the forms given previously for a space truss member (see Egs. 4-86 and 4-87). In all cases, the rotation transformation matrix RT is formed according to Eg. (4-94), and the member stiffness matrix for structural axes is computed by Eg. (4-95).

4.25 Analysis of Space Frames. The space frame shown in Fig. 4-43 contains rigidly connected members oriented in a general manner in space. The loads on the structure may be of any type and orientation. The numbering system to be adopted for members and joints is the same as for structures discussed previously.

Axial, flexural, and torsional deformations will be considered in the analysis of space frames. ", The unknown displacements at the joints consist of six types, namely, the x, y. and z components of the joint translations and the x, y. and z components of the joint rotations. The six possible displacements at a particular joint j are denoted by the following indexes:

6j - 5 = index for translation in the x direction 6j - 4 = index for translation in the y direction 6j - 3 = index for translation in the z direction 6j - 2 = index for rotation in the x sense 6j - 1 = index for rotation in the y sense 6j = index for rotation in the z sense

Also, the number of degrees of freedom 11 in a space frame may be deter-

*To omit axial deformations. constraints against length changes of members must be introduced (see Sec. 6.19).

![image 399](Matrix Analysis of Framed Structures_images/imageFile399.png)

278 Chapter 4 Computer-Oriented Direct Stiffness Method

mined from the number ofjoints nj and the number of restraints nr by the following expression:

n = 6nj - nr (4-101)

A member i in a space frame will have joint numbers j and k at its ends, as shown in Fig. 4-49. The twelve possible displacements of the joints associated with this member are also indicated in Fig. 4-49 and are indexed as follows:

- j3 = 6j - 3 j6 = 6j
- k3 = 6k - 3 k6 = 6k


jI = 6j - 5 j4 = 6j - 2

j2 = 6j - 4

- j5 = 6j - 1 k2 = 6k - 4
- k5 = 6k - 1


(4-102)

kl = 6k- 5 k4 = 6k - 2

Construction of the joint stiffness matrix follows the same general pattern as with plane frames (see Sec. 4.17), except that the process is complicated by the fact that more terms are involved. The 12 X 12 stiffness matrix SMSi is generated for each member in the frame (see Sec. 4.24), and its contributions to the stiffnesses ofjoints j and k are assessed. For example, the first column in the matrix SMSi contributes to the joint stiffness matrix Sj as follows:

(SJ)jl,jl = ISMs + (SMSl,l)i (SJ)j2,jl = ISMs + (SMS2,1)i (SJ)j3Jl = ISMs + (SMS3,1)i

(SJ)klJl = (SMS7,1)i (SJ)k2Jl = (SMS8,1)i (SJh3Jl = (SMS9,1)i

(4-103)

- (SJ)j4,jl = ISMs + (SMS4,1)i
- (SJ)j5,il = ISMs + (SMS5,1)i
- (SJ)j6,jl = ISMs + (SMS6,1)i


(SJ)k4,ji = (SMSIO,l)i (SJ)k5,il = (SMSll,l)i (SJ)k6,jl = (SMS12,1)i

Eleven other sets of expressions similar to Eqs. (4-103) may be written to make a total of twelve sets of equations. Each set involves transferring

tk5

###### tk2

y

If ----.. ----.... x

###### 1'1 kl k4

/ k31

k6 1

}1}4 I

###### I I

r-~---r------------r------X

###### Fig. 4-49. End-displacements for space frame member.

![image 400](Matrix Analysis of Framed Structures_images/imageFile400.png)

z

- Fig. 4-50. Joint loads for a space frame.


elements from a given column in the matrix SMS i to the appropriate locations in the matrix S.J'

Actions applied at a typical joint k are shown in Fig. 4-50. In the figure, the actions (A j)6k-5, (A j)6k-4, and (A j)6k-3 are the x. y. and 2 components of the concentrated force applied at the joint. In addition, the actions (Aj)6k-2, (A j)6k-1o and (Aj)6k are the x. y. and 2 components of the moment vector acting at the joint. These actions are placed in the vector of applied actions AJ , which assumes the following form:

AJ = {(Ajh, (AJ)z. (Ajh, (A j)4, (Ajh, (A j)6,

... , (A j )6h'-5, (A j )6k-4, (A j )6k-3, (A j)6k-2, (A j)6k-1o (Aj)6ko (4-104)

...• (A j )6IU-5. (A j )6nj-4, (A j )6nj-3, (A j )6Ilj-2, (A j )6nj-l, (A j )6nj}

Figure 4-51b shows the actions at the ends of a restrained space frame member i due to loads on the member itself. The end-actions AML for member-oriented axes are defined as follows:

(A JfLh,i = force in the XM direction at thej end (A.HLh,i = force in the YM direction at the j end (A'\fLhi = force in the ZM direction at the j end (A JflJ4,i = moment in the XM sense at the j end (A MLh,i = moment in the YM sense at the j end (A.uIJ6,i = moment in the ZM sense at the j end (AMLh.i = force in the XM direction at the k end (A;HIJ8,i = force in the YM direction at the k end (A ;\fL)9,i = force in the ZM direction at the k end

(AJfL)IO,i = moment in the XM sense at the k end (A AfLhl,i = moment in the YM sense at the k end (A.~fL)12,i = moment in the 2M sense at the k end

The matrix A~IL may be treated as a rectangular array of order 12 x m. in which each column is made up of the twelve elements enumerated above for a given member. Thus,

l(AML)I,I

(AMLh,m1

(AM/Ju

###### (AML)2,m

(AMLki

(4-105)

A ML = (A,lfLk.l•.•

(A ML)12,m

(AML)12.1

![image 401](Matrix Analysis of Framed Structures_images/imageFile401.png)

...=

###### a

::

###### §i

###### :r

:r

6

j;'

"'"

Q.

###### Q.

("l

("l

~....

~

...~

~

'S.

o

3

'CI

"'I

"'I

"'I

~

~

~

~

~

~

Q

Q

![image 402](Matrix Analysis of Framed Structures_images/imageFile402.png)

fA~f"..)~1\(---'0,'"MLA£)6"2fAY,

"'"f"fA"f...{/''/fA",...,

~I,.,II'.'Ifo(A(AMi)

1(A£)u_.

t(A£)6.-4

###### A"~)";fA,I~.,/VfA:';:"',"'"

I/--/!fA.,I,..___Xs

"//)j3'/j'i-..........................ML(A).Z,,-77,.-------)4

7:'~fA~I,.CDfA"I,.•

I,~-----............:::J//LS

(b)

ML(AIM/)6"-

sY

Fig.4-51.Loadsona spaceframemember.

(A£)6/-Z

ML

--

(A

(a)

/.(A£156r

}-,

/(A£16 r3

(A£1/6

J

Y

L

![image 403](Matrix Analysis of Framed Structures_images/imageFile403.png)

Problems 281

The construction ofthe equivalent load vector AE is accomplished through the rotation of axes procedure used previously. Figures 4-5la and 4-5lc show the equivalent loads at joints j and k that receive contributions from member i. For this purpose, the fixed-end actions AMSi (in the directions of structural axes) can be obtained from

AMSi = RfA~ILi (4-106)

in which Rii is the transpose of the matrix given by Eq. (4-94). The form of the rotation matrix R used in RTi is dictated by the category into which the particular member falls. These categories were discussed in Sec. 4.24. Following the calculation of AE, this vector is added to the vector AJ to form the combined load vector Ac.

The analysis is completed by calculating free joint displacements DF (translations and rotations in the x. y. and z directions), using Eq. (4-3) and then expanding them into the vector DJ• Support reactions AR (forces and moments in the x. y. and z directions) are computed next using Eq. (4-4). Finally, member end-actions for each member are computed by substituting the member stiffness matrix SMi for member axes (Table 4-1) and the appropriate form of the rotation transformation matrix RT i into the following equation:

(4-107)

This equation is of the same form as Eq. (4-77) given previously for plane frames.

A computer program for the analysis of space frames is given in Sec.

- 5. 11, and numerical examples are also included in that section.


Problems

The problems for Sec. 4.9 are to be solved in the manner described in Secs. 4.8 and 4.9. In each problem aU ofthe joint displacements. support reactions. and member end-actions are to be obtained. unless stated otherwise. Use the arbitrary numbering system shown in Fig. 4-7b when obtaining the over-aU joint stiffness matrix.

- 4.9-1. Analyze the continuous beam in Fig. 3-4a, assuming that the flexural

rigidity E1 is constant for all spans. Assume also that I1'L = P and M = PL.

- 4.9-2. Make an analysis of the continuous beam in Fig. 3-5a if the flexural rig-

idity E1 is the same for both spans and PI = 2P. P2 = P.

- 4.9-3. Analyze the three-span beam shown in the figure for Prob. 3.3-7 if Ll


= L3 = L. L2 = 2L. PI = P2= P'l = P. M = PL. and II'L = P. The flexural rigidity for members AB and CD is E1 and for member BC is 2E1.

4.9-4. Analyze the beam shown in the figure for Prob. 3.3-14 assuming that Ell

###### = 2EI and El2 = E1.

![image 404](Matrix Analysis of Framed Structures_images/imageFile404.png)

282 Chapter 4 Computer-Oriented Direct Stiffness Method

- 4.9-5. Analyze the overhanging beam shown in the figure, taking points A, B,

and C as joints. The beam has constant flexural rigidity EI.

W !WLI.

11111111111111111tR~lIIli'jc'

I. L '" L/2

Prob. 4.9-5.

- 4.9-6. Analyze the three-span beam having constant flexural rigidity EI (see

figure).

P 2P P 2P

PG.> 1ilk1o~

~L L/2:1:L/2 L L/2:1:L/2 L~

Prob. 4.9-6.

- 4.9-7. Analyze the beam shown in the figure, taking points A, B, C. and D as


joints. The segment AB has a flexural rigidity of 2EI, and the portion from B to D has a constant flexural rigidity of EI.

###### ~ ,llj) ±I"1) I" I

A 2PL Pie 2Pt P; i2P 0

###### ~-:-L/2 L/2-:-L/2±L/2~~

Prob. 4.9-7.

- 4.9-8. Obtain the joint stiffness matrix SJ for the beam shown in Prob. 3.3-8; also, rearrange and partition S.r into the form given by Eq. (4-8). Assume that the beam has constant EI.
- 4.9-9. Obtain the joint stiffness matrix SJ for the beam shown in Prob. 3.3-11, assuming that EI is constant. Also, rearrange and partition the matrix into the form given by Eq. (4-8).
- 4.9-10. Find the joint stiffness matrix SJ for the beam ofProb. 3.3-12, assuming that the flexural rigidity of the middle span is twice that of the end spans. Also, rearrange and partition the matrix into the form given by Eq. (4-8).
- 4.9-11. Find the joint stiffness matrix SJ for a continuous beam on five simple supports having four identical spans, each of length L. Also, rearrange and partition the matrix into the form given by Eq. (4-8). Assume that EI is constant for all spans.
- 4.9-12. Obtain the joint stiffness matrix SJ for the beam shown in the figure.


###### A e c 0 E

###### ~ 2EI "J&

i

~L ~·1, 2~1 E:-J

###### L L ·1,

Prob. 4.9-12.

![image 405](Matrix Analysis of Framed Structures_images/imageFile405.png)

Problems 283

Also, rearrange and partition the matrix into the form given by Eq. (4-8). The beam has a flexural rigidity of 2EI from A to C and EI from C to E.

The problems for Sec. 4.12 are to be solved in the manner described in Secs. 4.11 and 4.12. 1n each problem all of the joint di5placements, support reactions, and member end-actions are to be obtained unless otherwise stated. Use the arbitrary numbering systems shown in the figures which accompany the problems.

- 4.12-1. Analyze the plane truss structure in the figure for Prob. 3.3-19 under the effect of the vertical load P shown in the figure plus a horizontal load of 2P applied at the mid-height of member AC and directed to the right. Each member of the truss has the same axial rigidity EAx. Number the members as shown in the figure, and number the joints in the same sequence as the letters in the figure.
- 4.12-2. Analyze the plane truss shown in Fig. 4-23 for the loads shown, but with a hinge sUpp0I1 which prevents translation at point B (joint 2). Otherwise, the data are the same as in the example problem.
- 4.12-3. Analyze the plane truss shown in the figure for Prob. 3.3-23 due to the weights of the members. Each member has the same axial rigidity EAx and the same weight w per unit length. Number the joints in the following sequence: D, C. A, and B. Number the members in the following order: DC, AB, AD, BC, DB, and


###### AC.

4.12-4. Analyze the plane truss shown in Fig. 4-23 for the effect of its own weight, assuming a roller support exists at joint B which prevents translation in the .r direction. Assume that the weight of each member is 1\' per unit length. Otherwise, the structural data are the same as in the example problem.

- 4.12-5. Analyze the plane truss for the loads shown (see figure). All members

have the same axial rigidity EAr.

Prob. 4.12-5.

- 4.12-6. Analyze the plane truss shown in the figure for the effect of its own


weight. Assume that the axial rigidity of each member is EAx, and that each has the same weight w per unit length. (Hint: Take advantage of the symmetry of the structure and loading by working with half the structure, as indicated in the second part

![image 406](Matrix Analysis of Framed Structures_images/imageFile406.png)

284 Chapter 4 Computer-Oriented Direct Stiffness Method

of the figure. Note that both the area and the weight of the middle bar must be halved.)

Prob. 4.12-6.

- 4.12-7. Obtain the joint stiffness matrix SJ for the plane truss shown in the fig-

ure. Assume that all members have the same axial rigidity EAx.

y

~~--~--~~~--------x

1---- L ----I

Prob. 4.12-7.

- 4.12-8. Determine the joint stiffness matrix SJ for the plane truss shown in the

figure. Assume that all members have the same axial rigidity EA.\:.

Prob. 4.12-8.

- 4.12-9. Obtain the joint stiffness matrix SJ for the plane truss structure shown


in the figure. Rearrange and partition the matrix into the form given by Eq. (4-8). Assume that the horizontal and vertical members have cross-sectional areas Ax, and that the diagonal members have cross-sectional areas 2Ax.

![image 407](Matrix Analysis of Framed Structures_images/imageFile407.png)

Problems 285

y

~L--+<----

Prob. 4.12-9.

4.12-10. Determine the joint stiffness matrix SJ for the plane truss structure given in the figure. Assume that the cross-sectional areas of members numbered one through five are Ax, and that the cross-sectional areas of members numbered six through ten are 2Ax.

Prob. 4.12-10.

The problems for Sec. 4.18 are to be solved in the manner described in Secs. 4.17 and 4.18. In each problem all of the joint displacements, support reactions, and member end-actions are to be obtained unless otherwise stated. Use the numbering systems shown in the figures which accompany the problems. In the problems with US units, convert to kips and inches where necessary.

- 4.18-1. Analyze the plane frame shown in Fig. 3-lOa, assuming that both members have the same cross-sectional properties. Use the following numerical data: P = 10 kips, L = H = 12 ft, E = 30,000 ksi, lz = 200 in.4, and Ax = 10 in.2 Number the joints in the sequence B, A, e, and number the members in the sequence AB, Be. The material is steel, and units are US.
- 4.18-2. Analyze the plane frame shown in the figure for Prob. 3.3-32 if P =

- 6 kips, L = 24 ft, H = 16 ft, E = 30,000 ksi, lz = 350 in.\ and Ax = 16 in.2 Number the joints in the sequence B, A, e, D, and number the members in the sequence AB, Be, DB. The material is steel, and units are US.


- 4.18-3. Analyze the plane frame shown in the figure, assuming that both members have the same cross-sectional properties. Use the following data: P = 50 kN, L = 6 m, E = 200 X 106 kN/m2, lz = 1 X 10-3 m4, and Ax = 0.02 m2• The material is steel, and units are SI.


![image 408](Matrix Analysis of Framed Structures_images/imageFile408.png)

###### 286 Chapter 4 Computer-Oriented Direct Stiffness Method

----x

Prob. 4.18-3.

4.18-4. Analyze the plane frame shown in the figure, assuming that P = 40 kN, L = 2 m, and E = 70 X 106 kN/m2. The moment of inertia and cross-sectional area of members 1 and 3 are 0.5 x 10-3 m4 and 0.02 m2, respectively, and for member 2 are 1 x 10-3 m4 and 0.03 m2, respectively. The material is aluminum, and units are SI.

Prob. 4.18-4.

4.18-5. Analyze the plane frame shown in figure (a) for the effect of the loads shown. Assume that all members have E = 10,500 ksi, /z = 26 in.4, Ax = 8 in.2, and also assume that L = 60 in. and P = 2000 lb. Take advantage of the symmetry of the structure and loading by analyzing the structure shown in figure (b). Note that the area and moment of inertia of member 1 must be halved. The imaginary restraint

...L..--x 3

.....1.---'---x

###### /

z

(b)

(a)

Prob. 4.18-5.

![image 409](Matrix Analysis of Framed Structures_images/imageFile409.png)

at joint I prevents both x translation and z rotation. The material is aluminum, and units are US.

4.18-6. Analyze the plane frame shown in the figure, assuming that (for both members) E = 200 X 106 kN/m2, /z = 2 X 10-3 m4, and Ax = 0.04 m2. Also, assume L = 3 m and P = 30 kN. The material is steel, and units are SI. y ..j2p 2PL

45"61

)-+-:---""......+.

x

###### z

Prob. 4.18-6.

4.18-7. The plane frame shown in the figure is to be analyzed on the basis of the following numerical data: E = 200 X 106 kN/m2, P = 10 kN, L = 2 m; for members I and 2, /z = 1.5 X 10-3 m4, Ax = 0.01 m2; for member 3, /z = 1.8 X 10-3 m4, Ax = 0.03 m2. The material is steel, and units are SI.

z

Prob. 4.18-7.

4.18-8. Determine the joint stiffness matrix Sj for the plane frame shown in the figure if all members have the same cross-sectional properties. Assume the following data: E = 30,000 ksi, L = 20 ft, /z = 1600 in.4, Ax = 24 in.2 The material is steel, and units are US.

l G) 2

###### lr-------:=~"--------"{J

###### /1---1.-2L-~.1

###### z

Prob. 4.18-8.

![image 410](Matrix Analysis of Framed Structures_images/imageFile410.png)

288 Chapter 4 Computer-Oriented Direct Stiffness Method

4.18-9. Repeat the preceding problem for the plane frame shown in the figure. Also, rearrange and partition the matrix into the form given by Eq. (4-8).

Prob. 4.18-9.

4.19-1. Assume that a grid structure lies in the x-z plane and that a typical member i has local axes as shown in the figure. Determine the member stiffness matrix 8M for the local axes. Give the rotation matrix R in terms of the angle 'Y and also in terms of the direction cosines Cx and Cz.

y

###### z

Probs. 4.19-1 through 4.20-4.

- 4.19-2. For the grid member shown in the figure, derive the member stiffness

matrix 8MS for structural axes, using the results from Prob. 4.19-1.

- 4.20-1. Refer again to the grid member in the figure; and find the incremental


contributions to the vector AE from the j end (see Eq. 4-75), using the results from Prob.4.19-1.

4.20-2. Repeat Prob. 4.20-1 for the k end of the member. 4.20-3. For the grid member in the figure, determine formulas for the final

member end-actions AMi at the j end (see Eq. 4-77), using the results from Prob. 4.19-1.

4.20-4. Repeat Prob. 4.20-3 for the k end of the member.

![image 411](Matrix Analysis of Framed Structures_images/imageFile411.png)

4.22-1. The figure shows an alternative approach to rotation of axes for a space truss member. Let CyZ = .JC~ + C~, and do the following: (a) Determine Re for the first rotation about the Xs axis. (b) Find R" for the second rotation about the ZM axis. (c) Calculate the rotation matrix R by matrix multiplication. (d) Write the appropriate rotation matrix to be used instead of R for a member parallel to the Xs axis.

Ys

~~--~-------------~

Prob. 4.22-1.

- 4.22-2. An alternative approach to rotation of axes for a space truss member appears in the figure. Let CXY = .Jci + C~, and do the following: (a) Find R" for the first rotation about the Zs axis. (b) For the second rotation about the YM axis, determine R{J' (c) By matrix multiplication, calculate the rotation matrix R. (d) If a member is parallel to the Zs axis, what rotation matrix should be used instead of R?
- 4.23-1. For the space truss member in the figure, determine the incremental contributions to the vector AE from thej end (see Eq. 4-75), using the results from Prob. 4.22-2.


- 4.23-2. Repeat Prob. 4.23-1 for the k end of the member.
- 4.23-3. Derive formulas for the final member end-actions AMi at the j end of


the space truss member in the figure (see Eq. 4-77), using the results from Prob.

- 4.22-2.


![image 412](Matrix Analysis of Framed Structures_images/imageFile412.png)

290 Chapter 4 Computer-Oriented Direct Stiffness Method 4.23-4. Repeat Prob. 4.23-3 for the k end of the member. 4.24-1. The figure shows coordinates of points j, k, and p for a space frame

member. Find the rotation matrix R for principal axes of member i by the method described in Sec. 4.24.

y

°r-----~~------~~--~--x

1/ //

###### __________-----~---..:-:....~~."J/1//

Prob. 4.24-1.

![image 413](Matrix Analysis of Framed Structures_images/imageFile413.png)

###### 5Computer Programs forFramed Structures

5.1 Introduction. This chapter contains flow charts of computer programs for analyzing the six basic types of framed structures by the direct stiffness method. The flow charts are sufficiently detailed so that persons who are familiar with the elements of computer programming could write their own programs for structural analysis if desired.

All of the structures to be analyzed by the programs of this chapter are assumed to consist of straight, prismatic members. The material properties for a given structure are taken to be constant throughout the structure. Only the effects of loads are considered, and no other influences, such as temperature changes, are taken directly into account. However, such influences can usually be handled by converting them into equivalent joint loads, as described in Chapter 6. The programs are designed to handle in a single computer run any number of structures as well as any number of loading systems for the same structure.

Section 5.2 contains a brief description of the essential features of computer languages, with emphasis on FORTRAN and flow chart symbols. Program notation, preparation of data, and a description of program organization are given in Secs. 5.3 through 5.5. Flow charts of the programs for the six types of framed structures are presented in Secs. 5.6 through 5.11. Each of these sections also contains examples to demonstrate the preparation of input data and the form of output results from a digital computer (for both customary US units and SI units). Finally, a combined program for analyzing all types of framed structures is discussed in Sec. 5.12.

5.2 FORTRAN Programming and Flow Charts. It is assumed that the reader is already acquainted with FORTRAN or some other algorithmic programming language. Some programming experience with elementary problems, not necessarily related to structural engineering, is also desirable. If the reader has this rudimentary programming ability as well as a fundamental understanding of the material in Chapter 4, there should be no great difficulty in implementing the programs in this chapter. The programs are presented as annotated flow charts that are oriented toward the features of FORTRAN [1-3] for either a personal or main-frame computer. These FORTRAN-oriented charts are sufficiently detailed so that every step in the calculations is covered. Furthermore, a person who wishes to write these programs in some computer language other than FORTRAN should be able to do so quite easily by going step-by-step through the flow charts.

291

![image 414](Matrix Analysis of Framed Structures_images/imageFile414.png)

292 Chapter 5 Computer Programs for Framed Structures

Some of the essential features of an algorithmic language (such as FORTRAN), as well as the symbols used in the flow charts, are summarized in this section. The discussion is not intended to be complete, and it covers only those features that are required for the structural programs.

Numbers in a computer program may be either decimal numbers or integer numbers. The decimal numbers are also referred to as real numbers or floating-point numbers. Integer numbers are whole numbers that do not include a decimal point. Both types will be used in the programs, but they must be distinguished from one another because arithmetic operations are not always the same for the two types ofnumbers. Most ofthe calculations in the programs are made with decimal numbers. Integer numbers are used primarily as indexes (or subscripts).

Identifiers are names for variables, constants, or other entities used in a program. For example, the symbol E is used as an identifier for the modulus ofelasticity ofthe material. In general, the symbols used previously in Chapter 4 are adopted in the programs as identifiers, although some minor modifications are required. All alphabetical characters will be written as capital letters, and all symbols must be on the same line. For example, the symbol for the number ofjoints nj becomes the identifier NJ in a computer program. Identifiers of this type require only one storage location in the memory of a computer and are said to represent simpLe variables.

There are other variables, called subscripted variables, that require more than one storage location. Thus, an identifier for a subscripted variable represents an array of numbers, as in the case of a vector or a matrix. The location of a particular element in the array is determined by the subscripts following the symbol. These subscripts are enclosed in parentheses; for example, an element of the vector AE, such as AE4, becomes AE(4) in a computer program. Similarly, an element of the matrix AML, such as AML23, becomes AML(2,3). It is necessary to reserve in advance a block of storage locations in the computer memory for each subscripted variable, as explained later.

Operators used in computer programming are of several types, and those used in the structural programs are summarized in Table 5-1. Arithmetic operators are used to signify the operations of addition, subtraction, multiplication, division, and exponentiation. Note that multiplication is indicated by an asterisk, as in FORTRAN; thus, the product of B times C is represented in a program as B*C. Since all symbols must be on the same line, exponentiation is denoted by two asterisks followed by the exponent. For example, A4 is represented in a program by A**4.

The repLacement operator is an equal sign, as in FORTRAN, which represents the operation of replacing an existing number in a storage location with a new number. The new number is then said to be the current value ofthe variable.

The reLational operators are also listed in Table 5-1. These consist of the relations less than, less or equal, equal, greater or equal, greater than,

![image 415](Matrix Analysis of Framed Structures_images/imageFile415.png)

5.2 FORTRAN Programming and Flow Charts 293

Table 5-1

Operators Used in Computer Programs

Operator Symbol

Arithmetic Operators: Addition + Subtraction -

MultiplicationDivision *I Exponentiation **

Replacement Operator =

Relational Operators:

Less than < Less or equal ~ Equal = Greater or equal ~ Greater than > Not equal of=

and not equal. All of the relational operators are represented in the table by the usual algebraic symbols. These symbols are not the same as their counterparts in FORTRAN, which are .LT., .LE., .EQ., .GE., .GT., and .NE. However, the former are preferred to the latter for use in flow charts because they are more general.

Computer programs consist of declarations and statements. The purpose of a declaration may be to define the properties of one or more identifiers used in a program. For example, declarations are used to specify which identifiers represent integer numbers and which represent decimal numbers (type declarations). The former are declared to be identifiers of integer type, and the latter are declared to be identifiers of floating (or real) type. In FORTRAN identifiers beginning with the letters I, J, K, L, M, and N are implied to be of type integer unless otherwise specified. Another important kind of declaration specifies the amounts of storage to be reserved for arrays in the program (array declarations). Declarations are also used to specify the items in sets of input or output data, as well as the details of format for the output of information (format declarations). The reader will find that no declarations appear in the flow charts of this chapter because they do not represent logical steps in the programs.

Statements, on the other hand, define operations to be performed by the computer. The order in which statements are written is an important feature in computer programming because instructions are executed one-by-one in the sequence in which they appear in the program, unless a specific command causes control to pass to another statement that is not in sequence. A state-

![image 416](Matrix Analysis of Framed Structures_images/imageFile416.png)

ment may be preceded by a label, which must be an integer number in FORTRAN. Statement labels are useful for proceeding from one statement to another in a sequence other than that in which they are listed.

The types of statements used in the programs in this book are summarized in Table 5-2. Flow chart symbols denoting these statements also appear in the table. Each of the statements listed in Table 5-2 is described briefly in the following discussion.

The input statement causes information to be transferred into the memory unit of the computer from some external source, such as a terminal, data cards, or magnetic disk. An input statement is represented in a flow chart by a box in the shape of a data card (see Table 5-2), which is an outdated mode of storing data. As an example, suppose that the numbers A, B, and C are to be brought into the computer as input data. This may be represented

Table 5-2

Statements Used in Computer Programs

Type of Statement Flow Chart Symbol

- (a)Input ¢
- (b) Output

~

- (c) Assignment

Q

- (d)Unconditionalcontrol 6
- (e)Conditionalcontrol ¢rT
- (f)Continue ¢
- (g)Iterativecontrol r¢


![image 417](Matrix Analysis of Framed Structures_images/imageFile417.png)

5.2 FORTRAN Programming and Flow Charts

295

###### $

###### $

(a)

(b)

###### $A=B*C

~

(e)

(d)

I

I

I

- (e)
- (f)


Statements

###### I

###### I

9

L

CONTINUE

(g)

Fig. 5·1. Flow chart symbols for statements: (a) input, (b) output, (c) assignment, (d) unconditional control, (e) conditional control, (f) continue, and (g) iterative control.

in the flow chart as shown in Fig. 5-la. (The arrows denote the flow of steps in a chart.)

The output statement causes information in the computer to be transferred outside and communicated to the programmer by means of a printer, a cathode ray tube (CRT), or other device. An output statement appears in a flow chart as a box with a diagonal line at the base, as shown in Table 5-2. Figure 5-lb demonstrates the appearance in a flow chart of an output statement that causes the numbers A, B, and C to be printed (or otherwise communicated to the programmer).

The assignment statement replaces the current value of a variable with a new value. For example, the statement

A = B*C

means that B*C is to be evaluated and put into the storage location for the variable A. Thus, the current value of A is replaced by the product of B times C. The replacement operator (an equal sign) is an integral part of the assignment statement. In a flow chart the assignment statement is enclosed in a rectangle (see Table 5-2). The statement described above is shown in

![image 418](Matrix Analysis of Framed Structures_images/imageFile418.png)

Fig. 5-1c as it would appear in a flow chart. The manner of showing a statement label in a flow chart is also illustrated in Fig. 5-1c. The label is written at the upper left-hand comer of the rectangle, and in this example the label is assumed to be the number 12.

The unconditional control statement changes the order of execution of statements in a program. This instruction is commonly known as the GO TO statement. By means of this command, control may be transferred to any other statement in the program by referring to its statement label. The unconditional control statement is represented in a flow chart by a circle, as shown in Table 5-2. The label of the statement to which control is transferred is indicated inside the circle. For example, in Fig. 5-1d the statement label 12 in the circle indicates that control is to be transferred to the statement in the program having the label 12.

The conditional control statement provides the ability to make decisions based upon a test, which may be a relational expression. In FORTRAN this type of command is called the logical IF statement. Control is transferred to one statement or another in the program depending upon whether the expression is true or false. The flow chart symbol for a conditional control statement is shown in Table 5-2 with the true and false branches indicated by a T and an F. These letters are not required if the true and false branches are always arranged in the manner shown. Figure 5-1e shows a conditional control statement which tests to determine whether A is less than B, using the relational operator <. If the condition is true, the branch at the right is followed; if the condition is false, the program continues along the branch indicated by the lower arrow. In FORTRAN there can only be one other statement on the true branch ofa logical IF statement. Therefore, an unconditional control (or GO TO) statement appears on the right-hand branch in Fig. 5-1e, representing typical FORTRAN construction.

The CONTINUE statement serves as a spacer in a FORTRAN program. It is not executable, except that it means "go on to" (or continue with) the next statement. When labeled, it is frequently used as the object of a GO TO statement, as indicated in Fig. 5-lf.

The iterative control statement is a useful device for executing the same statement or set of statements a specific number of times. In FORTRAN this type of command is known as a DO statement (or "DO-loop"). It causes an index, such as J, to be set to a specified initial value for the first cycle ofcalculations. Then the index is incremented a specified amount for subsequent cycles until it reaches or exceeds a final value, which is also specified. The increment for a DO-loop in FORTRAN is implied to be unity, unless otherwise stated. In a flow chart the list of specified parameters is enclosed in a hexagonal figure of the type shown in Table 5-2. The dashed line and arrowhead at the left of the symbol indicate that control is returned to this statement in cyclic fashion.

![image 419](Matrix Analysis of Framed Structures_images/imageFile419.png)

5.2 FORTRAN Programming and Flow Charts 197

Figure 5-lg shows an iterative control statement that causes other statements within the rectangular box to be executed N times. The iterative control statement contains the following indexes:

J = I,N

This expression means that the quantity J takes the value I for the first execution and then is incremented by an implied value of I for subsequent executions until it is finally set equal to N, and the statements are executed for the last time. If the increment is not equal to 1, its value must be specified as a third parameter (following N) in the list. Note the use of the CONTINUE statement in Fig. 5-lg to delineate the scope of the DO-loop.

As an example, suppose that A, B, and C are all subscripted variables of N elements each. If the corresponding elements of Band C are to be multiplied and assigned to A, the statement in the rectangular box would be

After N repetitions of the calculation, all elements of the arrays have been processed, and control is transferred to the next statement in the program.

It is often necessary to evaluate afunction in the course of executing a given statement. For example, the assignment statement

involves the evaluation of the cosine of C. In this example COS is the function designator, and its use in a program implies that a specific set of operations is to be performed automatically, resulting in the evaluation of the cosine of C. Certain frequently used functions such as sine, cosine, square root, logarithm, absolute value, etc. (designated as SIN, COS, SQRT, LOG, ABS, etc.) are incorporated into algorithmic languages such as FORTRAN for the convenience of the programmer.

Another important feature of algorithmic languages enables the programmer to use a series of statements as a subprogram (or subroutine in FORTRAN). A subprogram is a block of statements that may be used at several points in the same program or in different programs without alteration. If a program is constructed using subprograms as building blocks, it is said to be modular. The programs for structural analysis presented in this chapter are constructed in this manner.

The block of FORTRAN coding constituting a subroutine is treated as a declaration (called a subroutine declaration) that contains both a heading and a body. The heading includes the suhroutill£' II(//II£', to which may be appended a list ofji)l'1I/(/! p(/rllll/l'II'rs. or I/rgulI/I'lIls, enclosed in parentheses. These parameters represcnt qllantitic' fl'llOl the main program that are

![image 420](Matrix Analysis of Framed Structures_images/imageFile420.png)

298 Chapter 5 Computer Programs for Framed Structures

used in the subroutine. As an example of a subroutine name, consider the operation of multiplying a vector A (of M elements) by a scalar B to produce the vector C. A possible name for this subroutine would be:

SUBROUTINE VSCALE(M,A,B,C)

An important characteristic of a subroutine is that notation in the subroutine declaration has no connection with notation in the main program. When a program makes use of a subroutine, the formal parameters are replaced by actual parameters being used in the main program. Insertion of a subroutine statement (or subroutine call) into the program causes the steps in the subroutine to be executed. A subroutine call has the same format as a subroutine declaration, but in this case the list of actual parameters is used. For example, if a vector D (ofN elements) in the program is to be multiplied by a scalar E to produce the vector F, the subroutine call becomes:

CALL VSCALE(N,D,E,F)

Note that the list of actual parameters must contain all of the identifiers to be substituted for the corresponding items in the list of formal parameters found in the subroutine declaration. Both the number and the sequence of actual parameters must agree with the list offormal parameters.

If the parameters are numerous, it is more convenient to list them in a COMMON declaration in both the subroutine and the main program. In this case the parameters are omitted from the subroutine name and the subroutine call, which would both become simply VSCALE for the example. If the main program calls various subroutines of this nature, all COMMON statements must have the same number and sequence of parameters.

Although the foregoing discussion of some of the features of an algorithmic language is brief and incomplete, its purpose has been to explain the conventions used in the FORTRAN-oriented flow charts of this book. With these features in mind, the programmer can follow the charts and write programs for structural analysis.

5.3 Program Notation. The notation used in the computer programs for framed structures is summarized in this section. For convenience, items are listed in alphabetical order. A symbol in the list followed by parentheses ( ) denotes a subscripted variable with a single subscript (or a vector). A symbol followed by parentheses enclosing a comma (,) denotes a subscripted variable with two subscripts (or a matrix). The type of each variable (integer or decimal) is implied by the default rule of FORTRAN. That is, variables having names that begin with the letters I, J, K, L, M, and N are taken to be integers, while all others are assumed to be decimals.

In conjunction with a computer program, symbols such as AML and AML may be used interchangeably. It is understood that the symbol AML

![image 421](Matrix Analysis of Framed Structures_images/imageFile421.png)

5.3 Program Notation 299

represents a matrix and that the identifier AML stands for its counterpart in the program.

Identifiers Used in Computer Programs

Definition

Identifier

Combined joint loads Ac (in directions of structural axes) Equivalent joint loads AE (in directions of structural axes) Actions AJ (loads) applied at joints (in directions of

AC( )

AE( ) AJ( )

structural axes) Final member end-actions AM Actions AMD at ends of member (in directions of member

AM( ) AMD( )

axes) due to joint displacements Actions AML at ends of restrained members (in directions

AML( , )

of member axes) due to loads Support reactions AR (in directions of structural axes) Cross-sectional area Ax of member x, y, and z direction cosines of member (Cx, Cy, Cz) Identifier for expression CXZ = SQRT(CX*CX +

AR( ) AX( ) CX,CY,CZ CXZ

CZ*CZ)

Free joint displacements DF (in directions of structural

DF( ) DJ( )

axes) Joint displacements DJ for all joints (in directions of

structural axes) Modulus of elasticity E for tension or compression Length L of element (member) Modulus of elasticity G for shear Member index i Identifier used to indicate whether or not the angle ex is

E

EL( )

G

- I IA ID( )

- IM( ) IR,IC ISN ITS

J, K

Jl, . , J6 JE, KE

JJ( ) JK( )

JRL( ) KI, ... ,K6

- LML( ) LN M MD




zero Displacement indexes for joints Displacement indexes for a member Rowand column indexes Structure number Type of structure Joint indexes

- Indexes for displacements at j end of member Indexes for expanded vectors

- Designation for j end of member (joint j)
- Designation for k end of member (joint k) Joint restraint list


- Indexes for displacements at k end of member Loaded member list Loading number Number of members Number of displacement coordinates for a member (MD


= 2*NDJ) Number of degrees of freedom Semi-band width of stiffness matrix Number of displacement coordinates for all joints (ND =

N

NB

ND NDJ NJ

NDJ*NJ) Number of displacements per joint Number of joints Number of loaded joints Number of loaded members

NLJ

NLM

![image 422](Matrix Analysis of Framed Structures_images/imageFile422.png)

Chapter 5 Computer Programs for Framed Structures

300

Identifier

Definition

NLS NR NRJ

Number of loading systems Number of support restraints Number of restrained joints Rotation matrix Stiffness constant of member Stiffness matrix SFF for free joint displacements Sine and cosine of the angle a (sin a, cos a) Member stiffness matrix SM for member-oriented axes Identifier used for temporary storage of the product

R( , )

SCM SFF( ,)

SINA, COSA SM(, ) SMRT(, )

SMRT Member stiffness matrix SMS for structure-oriented

SMS( ,)

axes x, y, and z coordinates ofjoints x. y. and z components of length of member Torsion constant of member (lx)

X(), Y(), Z()

XCL, YCL, ZCL

XI()

- x. y. and z coordinates ofpoint p x s. Ys. and Zs coordinates of point p Moment of inertia about the YM axis (ly)
- y.y and Zy coordinates of point p Moment of inertia about the ZM axis (lz)


XP,YP,ZP XPS, YPS, ZPS

###### YI()

YPG,ZPG

ZI()

5.4 Preparation of Data. The manner in which a program is written depends to some extent upon the form in which the data are supplied. As a preliminary matter, the required input data for all of the programs in this chapter are described in this section. It is assumed that the data are given either as a group of lines typed on a terminal or as a collection of lines stored as a file in the computer.

The data lines for a particular structure are divided into the three categories of control data, structural data, and load data. Only one set of control and structural data is required for each structure, but there may be any number of sets of load data. The control data consist of three parameters that are most useful when the six special-purpose programs are assembled into a combined program for all types of framed structures. These parameters are the structure number ISN, the type of structure ITS, and the number of loading systems NLS. The structure number ISN will be 1 for the first structure, 2 for the second structure, etc. On the other hand, the type of structure ITS is represented by one of the numbers 1 through 6, as follows:

- ITS = 1: Continuous beam
- ITS = 2: Plane truss
- ITS = 3: Plane frame


- ITS = 4: Grid
- ITS = 5: Space truss
- ITS = 6: Space frame


The number of loading systems NLS indicates the number of sets of load data that accompany a given set of structural data.

The input data required for continuous beams are given in Table 5-3. This table specifies the number of data lines required for each category of information as well as the items to be included on the lines. The

![image 423](Matrix Analysis of Framed Structures_images/imageFile423.png)

Table 5-3

Preparation of Data for Continuous Beams

---~---- -.--

###### Number Data ofLines Items on Data Lines

--

Control Data I ISN ITS NLS

-~---

(;i-::l.... .._ a. Structuralparameters I M NR NRJ E

u:::20 c.b. JointMemberrestraintinformationlist NRJM IK JRU2K-llEUn Zl(l)JRU2K)

###### ell

-_. - 1--------------- -- ------ ._---C-------

i3 a. Load parameters I NLJ NLM Ci'" b. Actions at joints NLJ K AJ(2K-1l AJ(2K)

~ c. Actions at ends of NLM I AMUI.I) AMU2,ll .....lQ restrained members AML(3,1) AMU4,l)

due to loads

first line in the table under the category of structural data contains the number of members M, the number of restraints NR, the number of restrained joints NRJ, and the elastic modulus E of the material. The reason for including NRJ is that the number of data lines required to fill the joint restraint list (see line 4 of the table) is minimized if the number of restrained joints is known.

Each data line containing member information (line 3 of Table 5-3) includes for one member the member number I, the length EL(I), and the moment of inertia ZI(I) about the z axis. A total of M lines is required for the member data.

Each of the lines in the next series (a total of NRJ lines) contains a joint number K and two code numbers indicating the conditions of restraint at that joint. The term JRL(2K-1) denotes the restraint against translation in the y direction at joint k, and the term JRL(2K) denotes the restraint against rotation in the z sense at joint k. The convention adopted in this program is the following: If the restraint exists, the integer 1 is assigned as the value of JRL; and if there is no restraint, a value of zero is assigned.

The first line in the load data contains two items. These are the number ofloaded joints NLJ and the number of loaded members NLM. One reason for introducing these numbers is that they serve to minimize the amount of subsequent load data required. Another reason is that certain calculations in the program can be bypassed if either NLJ or NLM is equal to zero; for example, if NLM is equal to zero, the calculation of the vector AE can be omitted.

Each line ofjoint load data (a total ofNLJ lines) contains ajoint number K and the two actions AJ(2K-l) and AJ(2K) applied at that joint. These actions are a force in the y direction and a moment in the z sense. Finally,

![image 424](Matrix Analysis of Framed Structures_images/imageFile424.png)

302 Chapter 5 Computer Programs for Framed Structures

each line for member loads (NLM lines total) contains a member number I and the four fixed-end actions AML for that member. The fixed-end actions consist of a force in the y direction and a moment in the z sense at each end of the member.

Table 5-4 shows the input data required for plane trusses. Since both beams and plane trusses have two possible displacements at each joint, Tables 5-3 and 5-4 are very similar. The structural parameters required for plane trusses are similar to those for beams, except that the number of joints NJ must be specified in addition to the other items. Moreover, a set of data (NJ lines total) is required to specify the coordinates of the joints of a truss. Each line in this set contains a joint number J, the x coordinate X(J) of the joint, and the y coordinate Y(J) of the joint.

On each of the lines containing member information the member number 1 is listed first, followed by the joint j number JJ(I) and the joint k number JK(I) for the two ends of the member. The choice of which end of the member is to be the j end and which is to be the k end is made arbitrarily by the programmer. The last item on each line is the cross-sectional area AX(I) of the member.

The data for the joint restraint list are similar to those for continuous beams, except that the types of restraints differ. For the plane truss, the terms JRL(2K-l) and JRL(2K) denote the restraints against translations in the x and y directions, respectively, at joint k. Similarly, the load data are symbolically the same as for continuous beams, but the applied actions AJ consist offorces in the x and y directions, and the hinged-end actions AML consist of forces in the XM and YM directions at the ends of the members.

Table 5-5 lists the input data required for plane frames. This table contains information similar to that in Table 5-4 for plane trusses, but there are certain differences caused by the fact that plane frames have three possible

Table 5-4

Preparation of Data for Plane Trusses

Number Data ofLines Items on Data Lines

Control Data I ISN ITS NLS ""§ a. Structural parameters 1 M NJ NR NRJ E o~::l «S b. Joint coordinates NJ J X(J) Y(J)

...20 c . Memberinformation M I JJ(I) JK(J) AX(I)

r/) d. Joint restraint list NRJ K JRL(2K-l) JRL(2K)

«S a. Load parameters 1 NLJ NLM 0~ b. Actions at joints NLJ K AJ(2K-l) AJ(2K) "0«S c. Actions at ends of NLM I AML(l,I) AML(2,I)

0 restrained members AML(3,I) AML(4,I)

....l due to loads

![image 425](Matrix Analysis of Framed Structures_images/imageFile425.png)

Table 5-5

Preparation of Data for Plane Frames

Number Data ofLines Items on Data Lines

Control Data I ISN ITS NLS

Cll3'"

- a. Structural parameters 1 M NJ NR NRJ E
- b. Joint coordinates NJ J X(J) Y(J)
- c. Member information M I 11(0 JK<O AX(I) ZI(i)
- d. Joint restraint list NRJ K JRl..(3K-2) JRL(3K-1) JRl..(3KJ


"§

Bu

2

r/l

- a. Load parameters I NU NLM
- b. Actions at joints NU K AJ(3K-2) AJ(3K-1) AJ(3K)
- c. Actions at ends of NLM I AMl..(l,l) AML(2,1) AMl..(3,I)


Cl"''"

"0

'"0

restrained members AMl..(4,1) AMl..(5,I) AMl..(6,I) due to loads

.....J

displacements at each joint. One dissimilarity is that an additional member property ZI (moment of inertia of the cross section) is required on each of the lines containing member information. Another distinction is that each of the lines in the joint restraint series contains (in addition to the joint number K) three code numbers instead of two. The terms JRL(3K-2), JRL(3K-I), and JRL(3K) denote the restraints atjoint k against translations in the x and y directions and rotation in the z sense, respectively.

Each line of joint-load data contains a joint number K and the three actions AJ applied at that joint. These actions are applied forces in the x and Y directions and a moment in the z sense. In addition, each line of member loads contains a member number I and the six actions AML at the ends of the restrained member. These actions consist of forces in the XM and YM directions and a moment in the ZM (or z) sense at the ends j and k, respectively.

The input data required for grids, shown in Table 5-6, are nearly the same as for plane frames (see Table 5-5). However, an additional material property (the shear modulus of elasticity G) is required on the first line of structural data in Table 5-6. Also, the torsion constant XI and moment of inertia YI appear on the lines containing member properties instead of the cross-sectional area AX and moment of inertia ZI.

Data for the joint restraint list are similar to those for plane frames, except that the nature of the restraints is different. For grids, the terms JRL(3K-2), JRL(3K-I), and JRL(3K) denote the restraints against rotations in the x and y senses and translation in the z direction, respectively, at joint k.

Similarly, the load data are symbolically the same as for plane frames, but the meanings are different. For a grid structure, the actions AJ applied at joints consist of moments in the x and y senses and a force in the z

![image 426](Matrix Analysis of Framed Structures_images/imageFile426.png)

Chapter 5 Computer Programs for Framed Structures

304

Table 5-6

Preparation of Data for Grids

Number ofLines Items on Data Lines

Dam

I ISN ITS NLS

Control Data

~

Structural parameters I M NJ NR NRJ E Joint coordinates NJ J X(J) Y(J) Member information M I JJ(I) JK(I) XI(I) Joint restraint list NRJ K JRL(3K-2) JRL(3K-1)

G

Q a. "§ b. Eu c. en2 d.

YI(I) JRL(3K)

Load parameters I NLJ NLM Actions at joints NLJ K AJ(3K-21 AJ(3K-1) Actions at ends of NLM I AML(I,I) AML(2,1) restrained members AML(4,1) AML(5,11 due to loads

Ol a.

AJ(3K) AML(3,1) AML(6.1l

b.

~

Q

c.

~

-l0

direction. Finally, the actions AML at the ends of restrained members due to loads are moments in the XM and YM senses and a force in the ZM (or z) direction at the ends j and k. respectively.

Table 5-7 shows the input data required for space trusses. This table is similar to Table 5-5 for plane frames, with some exceptions. For example, each of the lines in Table 5-7 containing joint coordinates provides not only the x and Y coordinates but also the Z coordinate for a joint. On the lines containing member properties, only the cross-sectional area AX is required.

Table 5-7

Preparation of Data for Space Trusses

Number Data ofLines Items on Data Lines

Control Data I ISN ITS NLS OJOl a. Structural parameters 1 M NJ NR NRJ E Q"§:::I c.b. MemberJoint coordinatesinformation NJM JI 11(1)X(J) Y(l)JK(I) Z(J)AX(l) t):::I d. Joint restraint list NRJ K JRL(3K-2) JRL(3K-1) JRL(3K)

###### en....

Ol a. Load parameters 1 NLJ NLM

Q~ b. Actions at joints NU K AJ(3K-2) AJ(3K-1) AJ(3K)

~ c. Actions at ends of NLM I AML(I,I) AML(2,1) AML(3,1) -l0 restrained members AML(4,1) AML(5,1) AML(6,1)

due to loads

![image 427](Matrix Analysis of Framed Structures_images/imageFile427.png)

5.4 Preparation of Data 305

Data for the joint restraint list are similar to those for plane frames, except that the types ofrestraints are different. For space trusses, the terms JRL(3K-2), JRL(3K-l), and JRL(3K) denote the restraints at joint k against translations in the x, y, and z directions, respectively.

Similarly, the load data are symbolically the same as for plane frames, but the meanings are different. Actions AJ applied atjoints consist offorces in the x, y, and z directions, and end-actions AML consist of forces in the XM, YM, and ZM directions at each end of a loaded member.

The input data required for space frames are summarized in Table 5-8, which is also similar to Table 5-5 for plane frames. However, since the space frame is three-dimensional and has six possible displacements per joint, there are more items of data for this type of structure than for plane frames. The first line of structural data in Table 5-8 includes the shear modulus G as well as the modulus E, and each of the lines containing joint coordinates must provide the z coordinate as well as the x and Y coordinates of a joint.

Member information must include the cross-sectional properties AX, XI, YI, and ZI. In addition, an identifier IA is provided in order to indicate whether the rotation angle ex is zero or not (see Sec. 4.24 for the meaning of the angle ex:). If the angle ex is zero for a given member, the value of zero is assigned to IA. If the angle ex: is not zero, the integer 1 is assigned. This is an arbitrary convention indicating that the member has its principal axes in skew directions. Under these conditions the principal axes are located by

Table 5-8

Preparation of Data for Space Frames

Number

Data ofLines Items on Data Lines Control Data 1 ISN ITS NLS

- a. Structural parameters 1 M NJ NR NRJ E G
- b. Joint coordinates NJ J X(J) Y(J) Z(J)
- c. Member information M I 11(1) JK(I) AX(I) XI(I) YI(I) ZI(I) IA

Coordinates of point p I XP YP ZP (required when IA = 1)

- d. Joint restraint list NRJ K JRL(6K-5) JRL(6K-4) JRL(6K-3) JRL(6K-2) JRL(6K-1) JRL(6K)


<;;Ol

Cl

~::>

- 1:)
- 2


- cil

<;;Ol

- Cl


- a. Load parameters 1 NLJ NLM
- b. Actions at joints NLJ K AJ(6K-5) AJ(6K-4) AJ(6K-3) AJ(6K-2) AJ(6K-1) AJ(6K)
- c. Actions at ends of 2NLM I AMUI,I) AML(2,1) AML(3.1) restrained members AMU4,l) AML(5,i) AML(6,1) due to loads AMU7,1) AML(8,I) AML(9,1)


"0

Ol

0

-l

AMU 10.1) AML(ll,l) AML(12,1)

![image 428](Matrix Analysis of Framed Structures_images/imageFile428.png)

306 Chapter 5 Computer Programs for Framed Structures

means of the coordinates of a point p in the X~YM plane (see Figs. 4-45 and 4-46) but not on the axis of the member. Therefore, each data line where IA is equal to 1 must be followed by an additional line on which the member index I and the three coordinates XP, YP, and ZP are given. These coordinates are used to obtain the rotation matrix, as described in Sec. 4.24.

An alternate method of programming would be to provide for the contingency that the angle a is known, in which case it would not be necessary to give the coordinates of a point p. The actual value of a could be assigned to an identifier named AA, after which the rotation matrix can be calculated directly from either Eq. (4-93) or Eq. (4-99).

Each of the lines in the joint restraint series contains a joint number K and six code numbers indicating the conditions of restraint at that joint. The terms JRL(6K-5) through JRL(6K) denote the restraints against translations and rotations in the x, y, and z directions at joint k.

Each line ofjoint load data contains ajoint number K and the six actions applied at that point. These actions are the components ofthe applied force vector and the applied moment vector in the x, y, and z directions.

In the last group of data, two lines must be provided for each member to which loads are applied because the information may not fit on one line. The first line contains a member number I and the six actions at the j end of the restrained member, and the second line provides the six actions at the k end of the member. The actions at each end are the forces and moments in the XM, YM, and ZM directions.

Units. A consistent system of units must be used for the input data, which involve units offorce and length only. The results ofthe calculations will have the same units as the input data, with the addition that all angles will automatically be in radians. One example ofa consistent US system of units is to give loads in kips, lengths in inches, areas in square inches, modulus of elasticity in kips per square inch, etc. In such a case all of the final results will be in units of kips, inches, and radians. On the other hand, if SI units of kilonewtons and meters are used for the input data, the final results will be in terms of kilonewtons, meters, and radians.

5.5 Description ofPrograms. The primary objective ofthis chapter is to present computer programs for individual types offramed structures. Each of these special-purpose programs consists of a main program that uses a series ofsubprograms to perform the detailed calculations. The main program is designed to handle any number of structures in one run and any number of loading systems for each structure. It calls upon subprograms that accomplish the following steps for a given type of structure:

1. Read and write structural data

- a. Problem identification
- b. Structural parameters
- c. Joint coordinates (except continuous beams)
- d. Member information


![image 429](Matrix Analysis of Framed Structures_images/imageFile429.png)

5.5 Description of Programs 307

- e. Joint restraint list
- f. Joint displacement indexes (computed internally)


- 2. Construct stiffness matrix a. Member stiffnesses b. Transfer to joint stiffness matrix
- 3. Read and write load data a. Load parameters b. Joint loads c. Member loads
- 4. Construct load vector a. Equivalent joint loads b. Combined joint loads
- 5. Calculate and write results


- a. Joint displacements
- b. Member end-actions
- c. Support reactions


To conserve computer time and storage, only the upper band of the stiffness matrix SFF (for free joint displacements) is constructed. This matrix is generated as a rectangular array of size N x NB, where N is the number of degrees of freedom and NB is the semi-band width. Figure 5-2a shows the banded form of SFf', and Fig. 5-2b depicts storage of the upper band as a rectangular matrix. The semi-band width NB for a particular structure is determined by the system for numbering joints. The value of this parameter may be calculated from the formula

NB = [NDJ*ABS(JK(I) - 11(1) + 1) - NSR]max (5-1)

In this FORTRAN expression the identifiers 11(1) and JK(I) denote the joint numbers at the two ends of a member I, and NDJ is the number ofdisplacements per joint. The symbol NSR represents the number of support restraints having displacement indexes within the range of indexes spanned by the term NDJ*ABS(JK(I) - 11(1) + 1). The member for which the righthand side of Eq. (5-1) is a maximum determines the semi-band width NB. Since the magnitude of NB dictates the amount of storage required for the upper band portion of SH" the joints of a structure should be numbered in a sequence which minimizes that parameter. If the term NSR is equal to zero, minimization of the difference JK(I) - 11(1) serves to minimize NB also.

Generation of the upper band of the stiffness matrix SFF in the form shown by Fig. 5-2b requires modification of the subscripts calculated for the form in Fig. 5-2a, which are

- (5-2a)
- (5-2b)


- ID(J) = J - Nl
- ID(K) = K - N2


These FORTRAN expressions for row and column indexes of a typical

![image 430](Matrix Analysis of Framed Structures_images/imageFile430.png)

308 Chapter 5 Computer Programs for Framed Structures

![image 431](Matrix Analysis of Framed Structures_images/imageFile431.png)

_ NB1

• N •

![image 432](Matrix Analysis of Framed Structures_images/imageFile432.png)

ID(K)

I I I

0

###### ID(J) ------

N

0

o

( 0) (b)

Fig. 5-2. Stiffness matrix SFF: (a) usual form of storage and (b) storage of upper band as a rectangular matrix.

element in Spp are drawn from Eq. (a) in Sec. 4.6. They produce revised displacement indexes ID(J) and ID(K) from the original indexes J and K by subtracting cumulative numbers of restraints Nl and N2, corresponding to J and K. Then the row and column indexes of the same element appearing in Fig. 5-2b are obtained as

IR = ID(J) IC = ID(K) - IR + 1

(5-3a) (5-3b)

The stiffness matrix generated in the form of Fig. 5-2b is factored using the subprogram named BANFAC given in Appendix D. This factorization need be done only once for a given structure. Subsequently, the free joint displacements DF are found using the subprogram BANSOL, which is also given in Appendix D. This subprogram must be applied a number of times equal to the number of loading systems NLS. For each loading system the matrix equation to be solved is

(5-4)

After the free joint displacements DF have been calculated, the member end-actions AMi and the support reactions AR are also obtained. Because the stiffness submatrix SRF is not generated, support reactions due to displacements DF cannot be calculated by matrix multiplication, as indicated in Eq. (4-4). Instead, the member end-actions AMi are first obtained from Eq. (4-5) as

![image 433](Matrix Analysis of Framed Structures_images/imageFile433.png)

5.6 Continuous Beam Program 309

- (5-5a) where
- (5-5b)


Then the support reactions are computed using the results from the member end-actions, as follows:

- (5-6a)
- (5-6b)


where

III

ARD = L RtiAMDi

i = 1

Only those members framing into the supports will contribute terms in Eq. (5-6b). The results of summing such terms are the same as the product SRFDFin Eq. (4-4). Of course, if the structure is a beam, the rotation transformation matrix RTi in Eqs. (5-5b) and (5-6b) is not needed.

The techniques described above are applied in programs for the six types of framed structures in Secs. 5.6 through 5. 11. The subprograms from these six programs may also be used to form a single combined program for all types of framed structures, as shown in Sec. 5.12.

5.6 Continuous Beam Program. This section contains flow charts for the main program and subprograms for analyzing continuous beams, as described in Sec. 4.8. In addition, numerical examples are given to demonstrate the form of the data and the results obtained from a computer program.

The first part of Flow Chart 5-1 shows the logic of the main program, called CB, for analyzing continuous beams. Comments on the right side of the flow chart are intended to help the reader understand what is meant by the symbols in the boxes. (Double boxes indicate subprograms that are called by the main program.) More than half of the statements in the main program are independent of the type of structure. These items include reading the control data, factoring the stiffness matrix, processing multiple loading systems, and solving joint equilibrium equations for each load set. Note that the layout of the program allows any number of structures to be processed in one run, and each structure may be analyzed for a number of loading systems equal to NLS. The upper band of the stiffness matrix SFF is generated and factored only once for a given structure, but the solution for DF (and other results) is obtained NLS times (for a series of loading systems).

The other items in the main program consist of the five subprogram statements numbered 1 through 5 in the chart. These subprograms pertain specifically to continuous beams and do the following blocks of operations:

![image 434](Matrix Analysis of Framed Structures_images/imageFile434.png)

- 1. SDATAl: Reads and writes the structural data
- 2. STIFF1: Constructs the stiffness matrix
- 3. LDATAl: Reads and writes the load data
- 4. LOADSl: Constructs the load vector
- 5. RESUL1: Calculates and writes the results


Statements in these five subprograms are given in Sections 1.1 through 1.5 of the flow chart.

Example 1. The continuous beam structure analyzed in Sec. 4.9 (see Fig. 4-13a) is presented as the first example to demonstrate the computer program. For this purpose the following numerical values (in US units) are assumed:

E = 10,000 ksi L = 100 in. Iz = 1000 in."' P = 10 kips The input data required by the computer program are summarized in Table 5-9,

Table 5-9

Data for Continuous Beam Example I

Type ofData Numerical Values

Control Data 1 1 1 ro (a) 3 5 3 10000.0

- (;j (b) 1 100.0 1000.0

(;!Cl... 23 200.0100.0 2000.02000.0

;:s

U...2 (c) 3I 1I 0I

r/)

4 1 I (a) 2 3

ro

- (;j (b) 2 -10.0 1000.0 Cl 3 -10.0 0.0


~0 (c) I 10.0 250.0 10.0 -250.0 ....l 2 10.0 250.0 10.0 -250.0

3 10.0 333.333 10.0 -333.333

which conforms to the specifications for continuous beams given previously (see Table 5-3). Results from the computer program for this data are listed in Table 5-10.

Example 2. The continuous beam in Fig. 5-3a has constant flexural rigidity and is to be analyzed for the given loads in three stages. as follows: (I) concentrated loads, (2) distributed loads, and (3) total loads. Numerical values (in SI units) for this problem are

![image 435](Matrix Analysis of Framed Structures_images/imageFile435.png)

###### 5.6 Continuous Beam Program

311

Iz = 3.6 x 10-:) m-l

Ll = 6 m L2 = 5 m

E = 200 X 106 kN/m2 P = 50 kN

w = 30 kN/m

M = 150 kN-m

Figure 5-3b shows the numbering system for the restrained structure. Input data for this example are given in Table 5-11; and the results appear in Table 5-12.

Table 5-10

Results for Continuous Beam Example 1

STRUCTURE NO. 1 CONTINUOUS BEAM NUMBER OF LOADING SYSTEMS 1

STRUCTURAL PARAMETERS M N NJ NR NRJ

E

10000.0

4

5 3

MEMBER INFORMATION MEMBER EL 1 100.000 2 100.000

ZI 1000.00000 2000.00000 2000.00000

200.000

JOINT RESTRAINTS JOINT JR1 JR2

1 1 1 1 0

4 1 1 LOADING NO. 1

NLJ NLM

3

ACTIONS AT JOINTS JOINT AJ1

AJ2 1000.000 .000

2 -10.000 -10.000

ACTIONS AT ENDS OF MEMBER AML1

TO LOADS AML4

RESTRAINED

MEMBERS DUE

AML2 250.000 250.000 333.333

AML3 10.000 10.000 10.000

- 1 10.000
- 2 10.000 10.000


- -250.000
- -250.000
- -333.333 AM4 1023.809
- -670.635
- -164.682


JOINT DISPLACEMENTS JOINT DJ1

DJ2 .OOOOOE+OO .12103E-02 .84325E-03 .OOOOOE+OO

- 1 .OOOOOE+OO
- 2 -.13161E+00
- 3 .OOOOOE+OO
- 4 .OOOOOE+OO


MEMBER END-ACTIONS MEMBER AM1

AM2

AM3 -13.056 16.944 7.470

33.056 2 3.056 12.530

1281. 746 -23.810 670.635

SUPPORT REACTIONS JOINT AR1

AR2 1281. 746 .000 -164.682

1 33.056

- 3 39.474
- 4 7.470


![image 436](Matrix Analysis of Framed Structures_images/imageFile436.png)

###### y

(a)

###### IY

###### 1t 3t 5t

###### 2 j-l__G)~1--/~~-2---.--:0:::::...-2 -6--:-t:/~3-x

/ 4

z (b)

Fig. 5-3. Continuous beam Example 2.

Table 5-11

Data for Continuous Beam Example 2

Type ofData Numerical Values

Control Data 2 1 3

CIl (a) 2 4 3 200000000.0

- 8 (b) 1 6.00 0.0036

c; 2 5.00 0.0036

\.0

:::l (c) 1 1 1 U:::l

2 1 0

\.0

.....

r/"J 3 0 1

1 (a) 1 1

(b) 2 -50.0 150.0

v'" (c) 1 300.0 400.0 300.0 -400.0

r/"J

CIl 2 (a) 0 1

- 8 (c) 2 75.0 62.5 75.0 -62.5


"'g

0 3 (a) 1 2

.....l (b) 2 -50.0 150.0

(c) 1 300.0 400.0 300.0 -400.0 2 75.0 62.5 75.0 -62.5

![image 437](Matrix Analysis of Framed Structures_images/imageFile437.png)

5.6 Continuous Beam Program

###### 313

Table 5-12

Results for Continuous Beam Example 2

STRUCTURE NO. 2 CONTINUOUS BEAM NUMBER OF LOADING SYSTEMS 3

STRUCTURAL PARAMETERS

M N NJ NR NRJ E

MEMBER INFORMATION MEMBER EL

1 6.000 5.000

JOINT RESTRAINTS JOINT JRl JR2 1 1 1 0 0

LOADING NO.

NLJ NLM 1 1

ACTIONS AT JOINTS JOINT AJl

2 -50.000

ACTIONS AT ENDS OF MEMBER AMLl

TO LOADS AML4

- -400.000

AM4 23.077

- -126.923


1 300.000

JOINT DISPLACEMENTS JOINT DJ1

.OOOOOE+OO 2 .OOOOOE+OO 3 .22035E-02

MEMBER END-ACTIONS MEMBER AM1 1 405.769 2 .000

SUPPORT REACTIONS JOINT AR1

- 1 405.769
- 2 244.231
- 3 .000


LOADING NO. 2

NLJ NLM 0 1

ACTIONS AT ENDS OF MEMBER AML1

TO LOADS AML4

2 75.000

- -62.500

AM4

- -192.308 182.692


JOINT DISPLACEMENTS JOINT DJ1

- 1 .OOOOOE+OO

4 3 200000000.0

ZI

.00360 .00360

AJ2 150.000

RESTRAINED AML2 400.000

DJ2 .OOOOOE+OO .88141E-03 .OOOOOE+OO

AM2 611.538 126.923

AR2 611. 538 .000 -126.923

RESTRAINED AML2 62.500

DJ2 .OOOOOE+OO

MEMBERS DUE AML3 300.000

AM3 194.231 .000

MEMBERS DUE AML3 75.000

- 2 .OOOOOE+OO -.40064E-03
- 3 -.20867E-02 .OOOOOE+OO


MEMBER END-ACTIONS MEMBER AM1 AM2 AM3

- 1 -48.077 -96.154 48.077
- 2 150.000 192.308 .000


SUPPORT REACTIONS JOINT AR1 AR2

-48.077 -96.154 2 198.077 .000 .000 182.692

![image 438](Matrix Analysis of Framed Structures_images/imageFile438.png)

###### 314 Chapter 5 Computer Programs for Framed Structures

###### Table 5-12

###### (Continued)

###### LOADING NO. 3 NLJ NLM

1 2

ACTIONS AT JOINTS JOINT AJI

AJ2 150.000

2 -50.000

ACTIONS AT ENDS OF MEMBER AML1

RESTRAINED MEMBERS DUE AML2 AML3 400.000 300.000 62.500 75.000

TO LOADS AML4

- -400.000
- -62.500

AM4

- -169.231 55.769


1 300.000 75.000

JOINT DISPLACEMENTS JOINT DJI

DJ2 .OOOOOE+OO .48077E-03 .OOOOOE+OO

- 1 .OOOOOE+OO
- 2 .OOOOOE+OO
- 3 .11685E-03


MEMBER END-ACTIONS MEMBER AMI

AM2 AM3 515.385 242.308 319.231 .000

1 357.692 150.000

SUPPORT REACTIONS JOINT ARI

AR2 515.385

1 357.692 442.308 .000

.000 55.769

![image 439](Matrix Analysis of Framed Structures_images/imageFile439.png)

5.6 Continuous Beam Program 315

Flow Chart 5-1

Main Program CB for Continuous Beams

###### Comments

Read structure number ISN, type of structure ITS, and number of loading systems NLS.

Read and write structural data (for continuous beam).

- 1.
- 2.

BANFAC(N, NB, SFF, *103)

- 3. i.!::====;::=:::::!..1
- 4.

BANSOL(N, NB, SFF, AC, OF)

- 5.


Construct upper band of stiffness matrix SFF (for continuous beam), stored as a rectangular array of size

###### N X NB.

Factor the upper band of matrix SFF. If SFF is not positive definite, transfer control to 103.

###### I

I I

Initialize loading number LN to zero.

t

Increment loading number by one for each new loading system.

###### I I

Rcad and write load data (for continuous beam).

I

###### I

Construct load vector AC (for continuous beam).

###### I

Solve for free joint displacements OF, using the factored stiffness matrix SFF and the first N elements in vector AC.

I

###### t

Calculate and write rcsults (for continuous beam).

###### I

If NLS is greater than LN, go to 102 and process another set of loads.

###### I

I

Otherwise, go to 101 and process another structure.

I

L

103

Discontinue calculations and write message when matrix SFF is not positive definite.

Message: SFF NOT POS. DEF.

999 STOP END

![image 440](Matrix Analysis of Framed Structures_images/imageFile440.png)

1.1 Subprogram SDATAl for Program CB

- a. Problem identification

Title: STRUCTURE NO. (ISN) CONTINUOUS BEAM NUMBER OF LOADING SYSTEMS = (NLS)

- b. Structural parameters


Write descriptive title.

Heading: STRUCTURAL PARAMETERS Subhead: M N NJ NR NRJ E

Write heading and subheading for structuml pammeters.

Read structural parameters.

Calculate number of joints NJ, number of displacement coordinates ND, and number of degrees of freedom N.

NJ = M + 1; ND = 2.NJ; N = ND - NR

Write structural parameters, including Nand NJ.

c. Member information

Heading: MEMBER INFORMATION Subhead: MEMBER EL ZI

Write heading and subheading for member information.

Set both MD and NB equal to four for a beam.

(Index on members)

1

I

###### I

Read and write M lines containing member numbers and properties.

###### I

I

L

![image 441](Matrix Analysis of Framed Structures_images/imageFile441.png)

###### 5.6 Continuous Beam Program

###### 317

d. Joint restraints

Write heading and subheading for joint restraints.

Heading: Subhead:

(Same for all programs)

Clear joint restraint list.

Read and write NRJ lines containing joint numbers and restraint list.

e. Joint displacement indexes

Initialize accumulator NI to zero.

5 J = 1, ND

(Index on joint displacement coordinates)

###### I

Determine cumulative number of restraints.

I I I I

4 Check for a restraint. If one exists, go to 4.

For case of no restraint, set joint displacement index among degrees of freedom.

###### t

Go to 5.

I

Where a restraint exists, set joint displacement index among support restraints.

I

###### L

RETURN END

![image 442](Matrix Analysis of Framed Structures_images/imageFile442.png)

1.2 Subprogram STIFFI for Program CB

- a. Member stiffnesses

I

II-

L

J = 1, N

5 1= 1, M

SCM1 = 4.0-E-ZI(I)/EL(I) SCM2 = 1.5-SCM1/EL(1) SCM3 = 2.0-SCM2/EL(I)

- SM(1, 1) = SCM3; SM(1, 2) = SCM2 SM(1, 3) = -SCM3; SM(1, 4) = SCM2 SM(2, 2) = SCM1; SM(2, 3) = -SCM2
- SM(2, 4) = SCM1/2.0; SM(3, 3) = SCM3
- SM(3, 4) = -SCM2; SM(4, 4) = SCM1


- b. Transfer to joint stiffness matrix


(Index on rows of SFF)

(Index on columns of SFF)

Clear stiffness matrix SFF.

###### I-

(Index on members)

I

Calculate three stiffness constants for member 1.

###### t

I

Fill upper triangular part of member stiffness matrix SM, using pre-calculated stiffness constants (see Table 4-2).

###### I

###### I

###### I

t

I

IM(1) =2.1-1; IM(3) = 2-1 + 1;

Fill vector of member displacement indexes 1M (see Eqs. 4-12).

IM(2) = 2-1 IM(4) = 2-1 + 2

###### I

,-

###### I

(Index on rows of SM)

4 J = 1, MD

I

I

Set temporary row index I I for matrix SFF equal to IM(J).

###### I

I

t

###### t

Check for restraint corresponding to index 11. If so, go to 4, skipping transfer.

I

I

![image 443](Matrix Analysis of Framed Structures_images/imageFile443.png)

5.6 Continuous Beam Program

319

1.2b (con!.)

###### t t

(Index on columns of SM)

3 K =J. MD

I I

I

###### I I

###### I

Set temporary column index 12 for matrix SFF equal to IM(K).

I !

I

Check for restraint corresponding to index 12. If so, go to 3, skipping transfer.

t I I t

###### I

Obtain actual row and column indexes (lR and IC) from vector !D.

I

###### I I I

Check for upper triangular position. If so, go to 2, keeping subscripts as they are.

I I t

###### I I I

For lower triangular position, switch subscripts, thereby changing to upper triangular position.

I I I I t I

Reset column index for storing upper band of matrix SFF as a rectangular array.

I I I

Transfer an element of SM to the appropriate position in matrix SFF, given by IR and Ie.

###### t I I

SFF(IR, IC) = SFF(IR, IC) + SM(J, K)

L_

3

I I

I t

###### CONTINUE

4

I L__ _ CONTINUE

###### L___ 5

CONTINUE

RETURN END

![image 444](Matrix Analysis of Framed Structures_images/imageFile444.png)

- 1.3 Subprogram LDATAI for Program CB a. Load parameters


Heading: LOADING NO. (LN) Subhead: NLJ NLM

Write heading and subheading for load parameters.

Read and write number of loaded joints and number of loaded members.

b. Joint loads

J

Check to determine whether joint loads exist. If not, ski p this part.

Heading: ACTIONS AT JOINTS Subhead: JOINT AJl AJ2

Write heading and subheading for joint loads.

,-

J=l,NLJ

I

I

Read and write NLJ lines containing joint numbers and joint loads.

###### I

L

![image 445](Matrix Analysis of Framed Structures_images/imageFile445.png)

321

###### 5.6 Continuous Beam Program

c. Member loads

###### ]

Check to determine whether member loads exist. If not, skip this part.

4

Write heading and subheading for member loads.

Heading: ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS

Subhead: MEMBER AML1 AML2 AML3 AML4

i--

I I I, AML(l, I),AML(2, I), AML(3, I),AML(4, I)

Read and write NLM lines containing member numbers and actions at ends of restrained members due to loads.

###### I

I I, AML(l, I),AML(2, I), AML(3, I),AML(4, I)

###### I

###### L __

Put I into the loaded member list to indicate presence of load on member I.

RETURN END

![image 446](Matrix Analysis of Framed Structures_images/imageFile446.png)

###### 322 Chapter 5 Computer Programs for Framed Structures

- 1.4 Subprogram LOADSI for Program CB


- a. Equivalent joint loads

AE(2. 1-1) =AE(2 .1-11-AML(1, I) AE(2. I) = AE(2. I) -AML(2, I) AE(2. I + 1) = AE(2 • I + 1) - AML(3, I) AE(2 • I + 2) = AE(2 • I + 2) - AML(4, I)

- b. Combined joint loads


If no members are loaded, skip this part.

(Index on members)

I

###### I

If member I is not loaded. skip transfer of AML to AE.

I

I

###### I

I I

Transfer negatives of fixed-end actions AML to appropriate locations in equivalent joint load vector AE (see Eqs. 4-20).

###### I

L

(Index on joint loads)

Obtain index JR for rearrangement from vector ID.

Add actual joint loads AJ and equivalent joint loads AE to obtain combined joint loads AC in rearranged form (see Eq. 4-7).

RETURN END

![image 447](Matrix Analysis of Framed Structures_images/imageFile447.png)

###### 5.6 Continuous Beam Program

323

- 1.5 Subprogram RESULI for Program CB a. Joint displacements


Initialize J to N + 1 in preparation for expanding the displacement vector.

(Index on joint displacements)

I

I

###### I

Calculate descending values of indcx JE for expansion of displacement vector.

I

I I

If no restraint exists, go to I.

I I

For restrained case, put a zero into the expanded displacement vector OJ.

I

###### t

Go to 2.

I I

For unrestrained case, decrease value of J by I to locate element of OF.

###### I

###### I

Transfer an element of OF to the appropriate position in OJ.

###### I

###### L

Heading: JOI NT DISPLACEMENTS Subhead: JOINT DJl DJ2

Write heading and subheading for joint displacements.

(Index on joints)

Write joint numbers and joint displacements.

![image 448](Matrix Analysis of Framed Structures_images/imageFile448.png)

###### 324 Chapter 5 Computer Programs for Framed Structures

- b. Member end-actions


Heading: MEMBER END-ACTIONS Subhead: MEMBER AM1 AM2 AM3 AM4

I---------r-------~Write heading and subheading for mem-

ber end-actions.

1--- 6 1=1,M (Indexonmembers)

I ~----~--~

Fill arrays SM and 1M for member I

Similar to Sec. 1.2, but fill whole array SM

###### I

i--

(Index on rows of SM)

5 J = 1, MD

I

I

I

Initialize AMO(J) to zero in preparation for accumulating results.

I

###### t

I-

I

(Index on columns of SM)

4 K = 1, MD

I I

###### I

I I

Obtain displacement index II from vector 1M, and place element of OJ into OM.

I

L~4____L-___~

I

###### t

Calculate AMO(J) by matrix-vector multiplication of SM and OM (see Eq. 5-5b).

AMD(J) = AMD(J) + SM(J, K) • DM(K)

###### I

###### I

###### I

Add AML(J, I) and AMO(J) to produce final end-action AM(J) (see Eq. 5-5a).

I

I I

Obtain displacement index 12 from vector

I

1M.

t

###### I

If no restraint exists, go to 5.

###### I

I

I

For restrained case, transfer AMO(J) to appropriate position in reaction vector AR (see Eq. 5-6b).

I

###### I

###### L___

I

###### I

6

L

Write member number I and final member end-actions.

I, AM(l), AM(2), AM(3), AM(4)

![image 449](Matrix Analysis of Framed Structures_images/imageFile449.png)

325

5.7 Plane Truss Program

- c. Support reactions


i--

(Index on support reactions)

I I

If no restraint exists, go to 7.

###### I

I

For restrained case, augment reaction AR(J) with negatives of AJ(J) and AE(J) (see Eq. 5-6a).

AR(J) = AR(J) - AJ(J) - AE(J)

###### I

I

###### L

Write heading and subheading for support reactions.

Heading: SUPPORT REACTIONS Subhead: JOINT ARl AR2

,--

(Index on joints)

I

Set up indexes 11 and J2. Also, add the corresponding items in JRL to obtain Nl.

###### I

I

I

If NI is zero, no restraint exists at joint J; so printing of reactions is skipped.

I I

Write joint number J and support reactions at a joint where at least one restraint exists.

###### I

###### I

L __

RETURN END

5.7 Plane Truss Program. The program presented in this section executes the analysis of plane trusses by the method given in Sec. 4.11. Details of this program are very similar to those in the continuous beam program (see Sec. 5.6) because both of these types of structures have two possible displacements at each joint. Therefore, in order to avoid repetition, the emphasis in this article is upon those parts ofthe program that are different from the continuous beam program.

The main program for Program PT (plane trusses) is similar to that for Program CB (see Flow Chart 5-1). However, the five subprograms pertaining specifically to plane trusses are named SDATA2, STIFF2, LDATA2,

![image 450](Matrix Analysis of Framed Structures_images/imageFile450.png)

326 Chapter 5 Computer Programs for Framed Structures

LOADS2, and RESUL2. Statements in these subprograms that are different from their counterparts for continuous beams appear in Flow Chart

5-2.

Flow Chart 5-2

- 2.1 Subprogram SDATA2 for Program PT


- a. Problem idenlification

Title: STRUCTURE NO. (lSN) PLANE TRUSS NUMBER OF LOADING SYSTEMS = (NLS)

- b. Structural parameters


Write descriptive title.

Write heading and subheading for structural parameters.

Heading: STRUCTURAL PARAMETERS Subhead: M N NJ NR NRJ E

Read structural parameters.

Set NDJ for a plane truss. Then calculate number of displacement coordinates ND and number of degrees of freedom N.

NDJ = 2; NO = NDJ * NJ; N = NO - NR

Write structural parameters. including N.

c. Joint coordinates

Heading: JOINT COORDINATES Subhead: JOINT X Y

Write heading and subheading for joint coordinates.

###### I-

(Index on joints)

###### I

Read and write NJ lines containing joint numbers and x and y coordinates.

###### I

###### I

L_

![image 451](Matrix Analysis of Framed Structures_images/imageFile451.png)

327

###### 5.7 Plane Truss Program

d. Member information

Write heading and subheading for member information.

Heading: MEMBER INFORMATION Subhead: MEMBER JJ JK AX El CX CY

Determine MD for a plane truss member, and initialize the semi-band width NB to zero.

I

###### I I

Read information for member I.

Calculate semi-band width NBI determined by member I (see Eq. 5-1).

NBI = NDJ.(ABS(JK(I) - JJ(II' + 1,

I

t

I

XCl = X(JK(I)) - X(JJ(I)) YCl = Y(JK(I)) - Y(JJ(I))

Compute x and y components of member length (XCl and YCL), the length EL, and the direction cosines CX and CY.

El(l) = SQRT(XCl·XCl + YCl.YCL) CX(I) = XCLlEL(I); CY(I) = YCLlEl(l)

Write information for member l.

I, JJ(I), JK(I), AX(I), El(I), CX(I), CY(I)

- e. Joint restraints (same as Sec. l.1 d in Program CB)
- f. Displacement indexes (same as Sec. l.le in Program CB)


![image 452](Matrix Analysis of Framed Structures_images/imageFile452.png)

###### 328 Chapter 5 Computer Programs for Framed Structures

- 2.2 Subprogram STIFF2 for Program PT

I

I

I

I I

I I

I

t

I

I I

- a. Member stiffnesses

After clearing SFF, do the following:

SCM = E • AX(I)/EL(I)

- SMS(l, 1) = SCM. CX(I). CX(I)
- SMS(l, 2) = SCM. CX(I) • CY(I)
- SMS(l, 3) = -SMS(l, 1)
- SMS(l, 4) = -SMS(l, 2)


- SMS(2, 2) = SCM. CY(I) • CY(I)
- SMS(2, 3) = -SMS(l, 2)
- SMS(2, 4) = -SMS(2, 2) SMS(3, 3) = SMS(l, 1) SMS(3, 4) = SMS(l, 2) SMS(4, 4) = SMS(2, 2)


- b. Transfer to joint stiffness matrix


IM(l) = 2. JJ(I) -1; IM(3) = 2. JK(I) -1;

IM(2) = 2 • JJ(I) IM(4) = 2 • JK(I)

The remainder of this section is the same as Sec. 1.2b of Program CB, except that SMS replaces SM.

Fill upper triangular part of member stiffness matrix SMS for a plane truss member (see Table 4-15).

Fill vector of member displacemen t indexes 1M (see Eqs. 4-27).

- 2.3 Subprogram LDATA2 for Program PT
- 2.4


This subprogram is the same as LDATAI for Program CB.

Subprogram LOADS2 for Program PT This subprogram is similar to LOADSI for Program CB, but in Sec. 2.4a the equivalent joint loads AE are computed as follows:

Transfer contributions of pinned-end actions AML to appropriate locations in equivalent load vector AE (see Eqs. 4-33).

I

I

t

- J1 = 2. JJ(I) -1; J2 = 2. JJ(I)
- K1 =2oJK(I)-1; K2=2.JK(l1


I

AE(Jl) = AE(J1) - CX(I)' AML(l, I) + CY(I). AML(2, I) AE(J2) = AE(J2) - CY(I) • AML(l, I) - CX(I) • AML(2, I)

###### I

- AE(K1) = AE(Kl) - CX(I) • AML(3, I) + CY(I) • AML(4, I)
- AE(K2) = AE(K2) - Cy(I) • AML(3, I) - CX(I) • AML(4, I)


I

I

![image 453](Matrix Analysis of Framed Structures_images/imageFile453.png)

329

###### 5.7 Plane Truss Program

2.5 Subprogram RESUL2 for Program PT

Sections 2.5a and 2.5c in this subprogram are the same as in RESULI for Program CB. However, Sec. 2.5b is as follows:

b. Member end-actions

Heading: MEMBER END-ACTIONS Subhead: MEMBER AM1 AM2 AM3 AM4

Write heading and subheading for member end-actions.

###### I

6 1= 1,M

###### I

Set up joint displacement indexes, calculate axial stiffness constant, and determine values of AMD (see Eqs. 4-34).

- J1 = 2 <JJ(I) -1; J2 = 2 <JJ(I)
- K1 = 2. JK(I) -1; K2 = 2. JK(I) SCM = E • AX(I)fEL(!) AMD(l) = SCM. ((DJ(J1) - DJ(K1)). CX(I)

+ (DJ(J2) - DJ(K2)) • CY(I)) AMD(3) =-AMD(1) AMD(2) =U.O; AMD(4) =0.0

I-

I

- L


###### I I I

I

t

###### I

Add AML(J, I) and AMD(J) to produce final end-action AM(J).

AM(J) = AML(J, I) + AMD(J)

I

###### I

AR(J1) =AR(J1) + CX(!) • AMD(1)

###### I

If restrained, augment AR(JI )(see Eq. 5-6b)

I

###### I

If restrained, augment AR(J2).

t

I I I

If restrained, augment AR(Kl).

###### AR(K2) =AR(K2) + CY(I) • AMD(3)

###### I

If restrained, augment AR(K2).

###### I

6

L_

Write member number I and final member end-actions.

I, AM(l), AM(2), AM(3), AM(4)

![image 454](Matrix Analysis of Framed Structures_images/imageFile454.png)

330 Chapter 5 Computer Programs for Framed Structures

Example. To demonstrate the use of Program PT, the plane truss structure in Sec. 4.12 (see Fig. 4-23) will be analyzed again. The following numerical values (in US units) are assumed for this problem:

E = 10,000 ksi L = 100 in. Ax = 10 in.2 P = 10 kips

Table 5-13 shows the input data required by the program (see Table 5-4 for data specifications), and the output results are listed in Table 5-14.

5.S Plane Frame Program. This section contains a program for the analysis of plane frames using the concepts described in Sec. 4.17. Because this type of structure has three possible displacements at each joint, the detailed steps in the program will be somewhat different from the programs for continuous beams and plane trusses. However, the methodology is the same, and the only change in certain statements is that the integer 2 (representing number of displacements per joint) is replaced by the integer 3.

Logic in the main program for Program PF (plane frames) is the same as in Programs CB and PT. However, the five subprograms dealing with plane frames are called SDATA3, STIFF3, LDATA3, LOADS3, and RESUL3. Flow Chart 5-3 shows the statements in these subprograms that are different from those in Programs CB and PT.

Table 5-13

Data for Plane Truss Example

Type ofData Numerical Values Control Data 1 2 1

- (a) 6 4 4 2 10000.0
- (b) 1 0.0 80.0 2 60.0 80.0


###### ...

«S 3 0.0 0.0

0«S (c) 41 60.01 0.02 6.0

ta...:s... 2 3 4 6.0

0 3 3 1 8.0

...2 4 4 2 8.0

til 5 1 4 10.0

6 3 2 10.0 (d) 3 1 1

4 1 1 (a) 1 4

~«S (b) 2 20.0 10.0

0 (c) 1 0.0 -20.0 0.0 20.0 "0«S 2 0.0 10.0 0.0 10.0 ...l0 3 0.0 10.0 0.0 10.0

4 5.0 5.0 5.0 5.0

![image 455](Matrix Analysis of Framed Structures_images/imageFile455.png)

Table 5-14

Results for Plane Truss Example

STRUCTURE NO. 1 PLANE TRUSS NUMBER OF LOADING SYSTEMS 1

STRUCTURAL PARAMETERS

M N NJ NR NRJ E 6 4 4 4 2 10000.0

JOINT COORDINATES JOINT X Y

- 1 .000 80.000
- 2 60.000 80.000
- 3 .000 .000
- 4 60.000 .000


MEMBER INFORMATION MEMBER JJ JK AX EL CX CY

- 1 1 2 6.000 60.000 1.000 .000
- 2 3 4 6.000 60.000 1. 000 .000
- 3 3 1 8.000 80.000 .000 1.000
- 4 4 2 8.000 80.000 .000 1. 000
- 5 1 4 10.000 100.000 .600 -.800
- 6 3 2 10.000 100.000 .600 .800


JOINT RESTRAINTS JOINT JR1 JR2 3 1 1 4 1 1

LOADING NO. 1

NLJ NLM 1 4

ACTIONS AT JOINTS JOINT AJ1 AJ2

2 20.000 10.000

ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS MEMBER AML1 AML2 AML3 AML4

- 1 .000 -20.000 .000 20.000
- 2 .000 10.000 .000 10.000
- 3 .000 10.000 .000 10.000
- 4 5.000 5.000 5.000 5.000


JOINT DISPLACEMENTS JOINT OJ1 OJ2

- 1 .10001E+00 .41465E-01
- 2 .10611E+00 -.40201E-01
- 3 .OOOOOE+OO .OOOOOE+OO
- 4 .OOOOOE+OO .OOOOOE+OO


MEMBER END-ACTIONS MEMBER AM1 AM2 AM3 AM4

- 1 -6.099 -20.000 6.099 20.000
- 2 .000 10.000 .000 10.000
- 3 -41. 465 10.000 41. 465 10.000
- 4 45.201 5.000 -35.201 5.000
- 5 26.832 .000 -26.832 .000
- 6 -31. 502 .000 31. 502 .000


SUPPORT REACTIONS JOINT AR1 AR2 3 -28.901 -56.667 4 -21. 099 76.667

331

![image 456](Matrix Analysis of Framed Structures_images/imageFile456.png)

332 Chapter 5 Computer Programs for Framed Structures

Flow Chart 5-3

- 3.1 Subprogram SDATA3 for Program PF


- a. Problem identification

Title: STRUCTURE NO. (tSN) PLANE FRAME NUMBER OF LOADING SYSTEMS = (NLS)

- b. Structural parameters (same as Sec. 2.1 b in Program PT, except that NDJ = 3)
- c. Joint coordinates (same as Sec. 2.lc in Program PT)
- d. Member information (same as Sec. 2.ld in Program PT, except that ZI is also read and written)
- e. Joint restraints

Heading: JOINT RESTRAINTS Subhead: JOINT JR1 JR2 JR3

3 J=l,NRJ

K, JRL(3 * K - 2), JRL(3 * K -1), JRL(3 * K)

3

K,JRL(3 * K-21.JRL(3 * K-1),JRL(3 * K)

- f. Displacement indexe3 (same as Sec. Lie in Program CB)


Write descriptive title.

Write heading and subheading for joint restraints.

Clear joint restraint list.

Read and write NRJ lines containing joint numbers and restraint list.

![image 457](Matrix Analysis of Framed Structures_images/imageFile457.png)

###### 5.8 Plane Frame Program

333

- 3.2 Subprogram STlFF3 for Program PF


a. Member stiffnesses After clearing SFF, do the following:

###### I-- +

5 I =l,M

I

Calculate four stiffness constants for member!.

SCMl = E • AX(I)/EL(I) SCM2 =4.0. E. ZI(I)/EL(I) SCM3 = 1.5. SCM2/EL(1)

I SCM4 =2.0•SCM3/EL(I)

###### I

Fill upper triangular part of member stiffness matrix SMS for a plane frame member (see Table 4-27).

I

- SMS(l, 1) =SCMl .CX(I). CX(I)

+SCM4 • CY(I) • CY(I)

- SMS(l, 2) = (SCMl - SCM4) • CX(I) • CY(I)


###### I I

- SMS(1,3) = -SCM3. CY(I) SMS(l, 4) = -SMS(l, 1) SMS(1,5) = -SMS(1, 2) SMS(1,6) = SMS(l, 3)
- SMS(2, 2) =SCMl • CY(I) • CY(I)


t

+SCM4. CX(I) • CX(I)

- SMS(2, 3) = SCM3. CX(I)

- SMS(2,4) =-SMS(l, 2) SMS(2. 5) = -SMS(2, 2) SMS(2. 6) = SMS(2. 3) SMS(3. 3) = SCM2
- SMS(3, 4) = -SMS(l. 3)

- SMS(3. 5) =-SMS(2, 3)

SMS(3, 6) = SCM2/2.0 SMS(4, 4) = SMS(l, 1) SMS(4, 5) = SMS(l, 2)

- SMS(4. 6) = SMS(3. 4)

SMS(5, 5) = SMS(2, 2)

- SMS(5. 6) = SMS(3. 5)


- SMS(6, 6) = SCM2




###### I

###### I

I

I I I

###### I

###### I

b. Transfer to joint stiffness matrix

t

Fill vector of member displacement indexes 1M (see Eqs. 4-66).

I

IM(1) = 3. JJ(I) - 2; IM(3) = 3. JJ(I); IM(5) = 3. JK(I) -1;

IM(2) = 3. JJ(I) -1 IM(4) = 3 • JK(I) - 2 IM(6) = 3 • JK(I)

I

I

The remainder of this section is the same as Sec. 1.2b of Program CB, except that SMS replaces SM.

![image 458](Matrix Analysis of Framed Structures_images/imageFile458.png)

334 Chapter 5 Computer Programs for Framed Structures

3.3 Subprogram LDATA3 for Program PF

- a. Load parameters (same as Sec. 1.3a in Program CB)
- b. Joint loads


IfNU*0, dothefollowing:

Write heading and subheading for joint loads.

Heading: ACTIONS AT JOI NTS Subhead: JOINT AJ1 AJ2 AJ3

,---

I

I

Read and write NU lines containing joint numbers and joint loads.

K, AJ(3. K - 2), AJ(3. K -1), AJ(3. K)

###### I

L

K, AJ(3 • K - 2), AJ(3 • K - 1), AJ(3 • K)

c. Member loads

After clearing LML and AML, do the following:

Heading: ACTIONS AT ENDS OF RESTRAINED

MEMBERS DUE TO LOADS Subhead: MEMBER AMLl AML2 ... AML6

Write heading and subheading for member loads.

,---

I

Read and write NLM lines containing member numbers and actions at ends of restrained members due to loads.

###### I

I, AML(l,I), AML(2, I ), ... , AML(6, I)

I

###### I

I, AML(1, I), AMl(2, I), ... ,AML(6, I)

I

L __ _

![image 459](Matrix Analysis of Framed Structures_images/imageFile459.png)

###### 5.8 Plane Frame Program 335

- 3.4 Subprogram LOADS3 for Program PF

I I

I

I

t

I

I

This subprogram is similar to LOADS I for Program CB. but in Sec. 3.4a the equilvalent joint loads are computed as follows:

- J1 = 3. JJ(I) -2; J2 = 3 * JJ(I) -1; J3 = 3. JJ(I)
- K1=3dK(I)-2; K2=3dK(I)-1; K3=3dK(1) AE(J1) = AE(J1) - CX(I). AML(l, I) + CY(I)· AML(2, I) AE(J2) = AE(J2) - CY(I) • AML(l, I) - CX(I) * AML(2, I) AE(J3) = AE(J3) - AML(3. I) AE(K1) = AE(K1) - CX(I) • AML(4, I) + CY(I) • AML(5, I) AE(K2) = AE(K2) - CY(I) * AML(4, I) - CX(I) * AML(5, I) AE(K3) = AE(K3) -AML(6, I)


Transfer contributions of fixedend actions AML to appropriate locations in equivalent load vector AE (see Eqs. 4-76).

- 3.5 Subprogram RESUL3 for Program PF a. Joint displacemen ts


After expanding the joint displacement vector. do the following:

Write heading and subheading for joint displacements.

Heading: JOINT DISPLACEMENTS Subhead: JOINT DJ1 DJ2 DJ3

###### 1--

L ~3______~~______~

Write joint numbers and joint displacements.

J, DJ(3 * J - 2), DJ(3. J - 1), DJ(3 * J)

b. Member end-actions

Write heading and subheading for member end-actions.

Heading: MEMBER END-ACTIONS Subhead: MEMBER AM1 AM2 ... AM6

![image 460](Matrix Analysis of Framed Structures_images/imageFile460.png)

336 Chapter 5 Computer Programs for Framed Structures

i--

I

Jl =3.JJ(I)-2; J2=3.JJ(I}-1; J3=3oJJ(I) Kl =3.JK(I),-2; K2=3.JK(I)-1; K3=3.JK(I) SCMl = E • AX(I}/EL(I}; SCM2 = 4.0. E • ZI(I)/EL(I) SCM3 = 1.5. SCM2/EL(I}; SCM4 = 2.0 • SCM3/EL(1} AMD(l) = SCMl • ((DJ(Jl) - DJ(Kl)) • CX(I)

###### I

I I I

Set up joint displacement indexes, calculate four stiffness constants, and determine values of AMD (see Eqs. 4-78).

+ (DJ(J2) - DJ(K2)) • CY(I))

- AMD(2) = SCM4 • (-(DJ(Jl) - DJ(Kl)) • CY(I}

+ (DJ(J2) - DJ(K2)) • CX(Il) +SCM3. (DJ(J3) + DJ(K3))

- AMD(3) = SCM3 • (-(DJ(Jl) - DJ(Kl)) • CY(I)

+ (DJ(J2) - DJ(K2)) • CX(I)) + SCM2 • (DJ(J3) + 0.5. DJ(K3))

- AMD(4) = - AMD(l); AMD(5) = - AMD(2) AMD(6) = SCM3 • (-(DJ(Jl) - DJ(Kl)) • Cy(1}


###### I

###### I

+ (DJ(J2) - DJ(K2)) • CX(I)) + SCM2 • (0.5. DJ(J3) + DJ(K3))

t

###### I

I

I

Add AML(J, I) and AMD(J) to produce final end-action AM(J).

###### I

I I

I

###### I

###### I

###### I I

Augment reactions at j end (see Eq. 5-6b).

t

###### I

###### I

I

###### I I

I I

Augment reactions at k end.

###### I

L_

Write member number I and final member end-actions.

![image 461](Matrix Analysis of Framed Structures_images/imageFile461.png)

###### 337

5.8 Plane Frame Program

c. Support reactions After obtaining reactions, do the following:

Write heading and subheading for suppOt1 reactions.

Heading: SUPPORT REACTIONS Subhead: JOINT ARl AR2 AR3

,--

###### I

I

Set up indexes 11, J2, and J3. Also, add the corresponding items in J RL to obtain N1.

Jl =3.J-2;J2=3.J-l;J3=3.J Nl = JRL(Jl) + JRL(J2) + JRL(J3)

I

###### I

If Nl is zero, skip printing of reactions.

I

###### I

Write joint number and suppOt1 reactions at a joint where at least one restraint exists.

###### I

I

###### L __

RETURN END

Table 5·15

Data for Plane Frame Example

Type ofData Numerical Values

Control Data 1 3 1

(a) 3 4 5 2 70000000.0 (b) 1 0.0 0.0

;3 2 3.0 4.0

C<l

Cl 3 9.0 5.0 ~... 4 11.0 1.0

U::l (c) 1 1 2 0.02 0.003 ::l.... 2 2 3 0.02 0.003

r/5 3 3 4 0.02 0.003

(d) 1 1 1 1

4 1 1 0 (;iC<l (a) 2 1

Cl (b) 2 0.0 -100.0 0.0 "0C<l 3 100.0 200.0 -150.0

0

.....l (c) 1 0.0 120.0 100.0 0.0 120.0 -100.0

![image 462](Matrix Analysis of Framed Structures_images/imageFile462.png)

338 Chapter 5 Computer Programs for Framed Structures

~-------1------L-----------------t-------+----L------X

###### / ~3L~ofE----6L----+-e--

###### z

(0)

1 -------x

###### / A

(b)

z

Fig. 5-4. Plane frame example.

Example. Figure 5-4a shows a plane frame consisting of prismatic members that all have the same cross-sectional properties. A numbering system for the restrained structure is given in Fig. 5-4b. Numerical values (in SI units) for this problem are

E = 70 X 106 kN/m2 Iz = 3 X 10-3 m4

L = 1 m Ax = 0.02 m2 P = 100 kN

Table 5-15 contains the input data required by the computer program (see Table 5-5 for the form of plane frame data), and results from the program are given in Table 5-16.

![image 463](Matrix Analysis of Framed Structures_images/imageFile463.png)

5.S Plane Frame Program 339

###### Table 5-16 Results for Plane Frame Example

STRUCTURE NO. 1 PLANE FRAME NUMBER OF LOADING SYSTEMS

STRUCTURAL PARAMETERS

M N NJ NR NRJ E 7 4 5 2 70000000.0

JOINT COORDINATES JOINT X Y

- 1 .000 .000
- 2 3.000 4.000
- 3 9.000 5.000
- 4 11. 000 1. 000


MEMBER INFORMATION MEMBER JJ JK AX ZI EL CX CY

- 1 1 2 .020 .003 5.000 .600 .800
- 2 2 3 .020 .003 6.083 .986 .164
- 3 3 4 .020 .003 4.472 .447 -.894


JOINT RESTRAINTS JOINT JRl JR2 JR3

1 1 1 1

1 1 0 LOADING NO. 1

NLJ NLM 2 1

ACTIONS AT JOINTS JOINT AJ1 AJ2 AJ3 2 .000 -100.000 .000 3 100.000 200.000 -150.000

ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS MEMBER AML1 AML2 AML3 AML4 AML5 AML6

1 .000 120.000 100.000 .000 120.000 -100.000

JOINT DISPLACEMENTS JOINT OJ1 DJ2 OJ3

- 1 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 2 .73679E-02 -.51920E-02 -.13 353E-03
- 3 .64102E-02 .34207E-02 -.26851E-03
- 4 .OOOOOE+OO .OOOOOE+OO -.23019E-02


MEMBER END-ACTIONS MEMBER AMI AM2 AM3 AM4 AM5 AM6

- 1 -74.807 294.903 542.865 74.807 -54.903 331.648
- 2 -108.461 -110.577 -331. 648 108.461 110.577 -340.968
- 3 -60.373 42.702 190.968 60.373 -42.702 .000


SUPPORT REACTIONS JOINT AR1 AR2 AR3 1 -280.806 117.096 542.865 4 -11.194 -73.096 .000

![image 464](Matrix Analysis of Framed Structures_images/imageFile464.png)

5.9 Grid Program. A program for the analysis of grid structures is given in this section, using the method described earlier in Sec. 4.20. Because the analytical procedure for grids is symbolically similar to that for plane frames, Program GR (for grids) is not much different from Program PF in the preceding section. The five subprograms pertaining to grids are named SDATA4, STIFF4, LDATA4, LOADS4, and RESUL4. Statements in these subprograms that differ from those in Program PF are indicated in Flow Chart 5-4.

Example 1. Figure 5-5a shows a grid structure having geometrical properties and loads similar to the plane frame problem in Sec. 4.18 (see Fig. 4-31a). Assume that the cross-sectional properties of both members of the grid are the same and that the following numerical values (in US units) apply:

E = 10,000 ksi Ix = 1000 in."

L = IODin. P = 10 kips

G = 4,000 ksi h = 1000 in.1

A numbering system is given in Fig. 5-5b, which shows the restrained structure. Numerical values to be supplied as data are shown in Table 5-17 (see Table 5-6 for data specifications), and the output of the computer program is given in Table 5-18.

y

z

w=2.4f P

(0)

( b)

###### Fig. 5-5. Grid Example 1.

![image 465](Matrix Analysis of Framed Structures_images/imageFile465.png)

5.9 Grid Program

###### 341

Flow Chart 5-4

- 4.1 Subprogram SDATA4 for Program GR a. Problem identification

Title: STRUCTURE NO. (ISN) GRID NUMBER OF LOADING SYSTEMS = (NLS)

The remainder of this subprogram is similar to Subprogram SDATA3 in Program PF; but the shear modulus G is added, and the member properties AX and ZI are replaced by XI and VI.

- 4.2 Subprogram STIFF4 for Program GR


Write title.

a. Member stiffnesses After clearing SFF, do the following:

,-----

5 1= l,M

I

I

SCMl = G • XI(I)/EL(I) SCM2 = 4.0. E • YI(I)/EL(I) SCM3 = 1.5 • SCM2/E L( I) SCM4 = 2.0. SCM3/EL(I)

I I

Calculate four stiffness constants for member I.

###### I

Fill upper triangular part of member stiffness matrix SMS for a grid member (see Table 4-38).

SMS(l, 1) = SCMl * CX(I) • CX(I) + SCM2 • CY(I) * CY(I) SMS(l, 2) = (SCMI-SCM2) * CX(I). CY(I) SMS{l, 3) = SCM3 • CY(1) SMS(l, 4) = -SCMl • CX(I) • CX(I) + 0.5. SCM2 • CY(I) • CY(I) SMS(l, 5) = -(SCMl + 0.5. SCM2) * CX(I). CY(I) SMS(l, 6) =-SMS(l, 3) SMS(2, 2) = SCMl • CY(I) • CY(I) + SCM2 • CX(I) * CX(I) SMS(2, 3) = -SCM3. CX(I); SMS(2, 4) = SMS(l, 5) SMS(2, 5) = -SCMl * CY(I) * CY(I) + 0.5 * SCM2 * CX(I) • CX(I) SMS(2, 6) =-SMS(2, 3); SMS(3, 3) =SCM4

I

I I

###### I

I

###### I

- SMS(3, 4) =SMS(l, 3); SMS(3, 5) =SMS(2, 3)

.'SMS(3, 6) =-SCM4; SMS(4, 4) = SMS(l,l)

- SMS(4, 5) =SMS(l, 2); SMS(4, 6) =SMS(l, 6)
- SMS(5, 5) =SMS(2, 2); SMS(5, 6) =SMS(2, 6)
- SMS(6, 6) = SCM4


###### t

I

I

b. Transfer to joint stiffness matrix (same as Sec. 3.2b in Program PF)

- 4.3 Subprogram LDATA4 for Program GR This subprogram is the same as LDA TA3 for Program PF.
- 4.4 Subprogram LOADS4 for Program GR This subprogram is the same as LOADS3 for Program PF.
- 4.5 Subprogram RESUL4 for Program GR This subprogram is similar to RESUL3 for Program PF,


but in Sec. 4.5b the member end-actions AMD are computed as follows:

![image 466](Matrix Analysis of Framed Structures_images/imageFile466.png)

1-----

6 1= 1, M

I

I

Set up joint displacement indexes, calculate four stiffness constants, and determine values of AMD (see Eqs. 4-79).

Jl =3.JJ(I)-2; J2=3.JJ(I)-1; J3=3.JJ(I) K1 =3.JK(I)-2; K2=3.JK(I)-1; K3=3.JK(1) SCM1 = G • XI(I)/EL(I); SCM2 = 4.0. E • YI(I)/EL(I) SCM3 = 1.5. SCM7/EL/I); SCM4 = 2.0. SCM3/EL(I)

###### I

I

I

- AMD(1) = SCMl • «DJ(J1) - DJ(Kl)) • CX(I)

+(DJ(J2) - DJ(K2)) • CY(I))

- AMD(2) = SCM2. (-(DJ(J1) +0.5. DJ(K1)) • CY(I)

+ (DJ(J2) + 0.5. DJ(K2)) • CX(I)) - SCM3 • (DJ(J3) - DJ(K3))

- AMD(3) = SCM3 • «DJ(J1) + DJ(K1)) • CY(I)

- (DJ(J2) + DJ(K2)) • CX(I)) + SCM4 • (DJ(J3) - DJ(K3))

- AMD(4) = -AMD(l); AMD(6) = -AMD(3)
- AMD(5) = SCM2 * (-(0.5 * DJ(J1) + DJ(K1)) * Cy(I)


I

###### I

###### I I

+ (0.5 • DJ(J2) + DJ(K2)) * CX(I)) - SCM3 * (DJ(J3) - DJ(K3))

###### t

I

Example 2. A second problem consisting of a rectangular grid is shown in Fig. 5-6a. This structure has five members, six joints, twelve restraints, and six degrees of freedom. The cross-sectional properties of all of the members are assumed to be the same, and the numerical constants (in SI units) for the problem are the following:

E = 200 X 106 kN/m2 Ix = 2 x 1O-:l m4

G = 80 X 106 kN/m2 Iy = 1 x 1O-~ m'

L=2m P = 50 kN

Figure 5-6b shows a numbering system for the restrained structure. Table 5-19 contains the input data for this problem, and the solution is given in Table 5-20, whic~ shows only the final results from the computer program.

Table 5-17

Data for Grid Example 1

Type ofData Numerical Values Control Data 1 4 1

(a) 2 3 6 2 10000.0 4000.0

'iii (b) 1 100.0 75.0 Ci 2 0.0 75.0

~

Oil.... 3 200.0 0.0

....;:l (c) 1 2 1 1000.0 1000.0

0

2 2 1 3 1000.0 1000.0 ~ (d) 2 1 1 1

3 1 1 1

.... (a) 1 2

~

~

Ci (b) 1 0.0 1000.0 -10.0

"0....l0~ (c) 21 0.00.0 -200.0-312.5 12.010.0 0.00.0 312.5200.0 12.010.0

![image 467](Matrix Analysis of Framed Structures_images/imageFile467.png)

5.9 Grid Program 343

###### Table 5-18 Results for Grid Example 1

STRUCTURE NO. 1 GRID NUMBER OF LOADING SYSTEMS 1

STRUCTURAL PARAMETERS

M N NJ NR NRJ E G 2 3 3 6 2 10000.0 4000.0

JOINT COORDINATES JOINT X Y

- 1 100.000 75.000
- 2 .000 75.000
- 3 200.000 .000


MEMBER INFORMATION

MEMBER JJ JK XI YI EL ex CY 1 2 1 1000.000 1000.000 100.000 1.000 .000 2 1 3 1000.000 1000.000 125.000 .800 -.600

JOINT RESTRAINTS JOINT JR1 JR2 JR3 2 1 1 1 3 1 1 1

LOADING NO. 1

NLJ NLM 1 2

ACTIONS AT JOINTS JOINT AJ1 AJ2 AJ3

1 .000 1000.000 -10.000

ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS MEMBER AML1 AML2 AML3 AML4 AML5 AML6 1 .000 -200.000 12.000 .000 200.000 12.000 2 .000 -312.500 10.000 .000 312.500 10.000

JOINT DISPLACEMENTS JOINT OJ1 OJ2 OJ3 1 -.75985E-02 .50949E-02 -.35508E+00 2 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO 3 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

MEMBER END-ACTIONS MEMBER AM1 AM2 AM3 AM4 AM5 AM6 1 303.941 -1311.474 24.040 -303.941 107.504 -.040 2 -292.344 896.362 -9.960 292.344 1598.675 29.960

SUPPORT REACTIONS JOINT AR1 AR2 AR3 2 303.941 -1311.474 24.040 3 1193.081 1103.534 29.960

![image 468](Matrix Analysis of Framed Structures_images/imageFile468.png)

y

###### z

18 17

(o )

t/___16

###### y

###### z

15 14

###### t~13

5

3

1

(b)

Fig. 5-6. Grid Example 2.

Table 5-19

Data for Grid Example 2

Type ofData Numerical Values

Control Data 2 4 1 (a) 5 6 12 4 200000000.0

80000000.0

(b) 1 6.0 0.0 2 6.0 4.0 3 0.0 0.0 4 10.0 0.0

....~ 5 2.0 4.0

~

Cl 6 6.0 8.0

] (c) 1 3 1 0.002 0.001 ....u;::l 2 1 4 0.002 0.(0) .....2 3 1 2 0.002 0.001 en 4 5 2 0.002 0.001

5 2 6 0.002 0.00)

(d) 3 1 1 1 4 1 1 1 5 1 1 1 6 1 1 1

'Cd (a) 1 2 Cl (b) 1 0.0 100.0 50.0

~

"0....:I0~ (c) 41 0.00.0 -112.5-100.0 150.075.0 0.00.0

112.5 75.0 100.0 150.0

![image 469](Matrix Analysis of Framed Structures_images/imageFile469.png)

5.10 Space Truss Program 345

Table 5-20

Final Results for Grid Example 2

JOINT DISPLACEMENTS JOINT DJl DJ2 DJ3

- 1 -.35599E-03 -.14976E-03 -.12182E-02
- 2 .28856E-03 .18376E-03 -.20993E-02
- 3 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 4 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 5 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 6 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO


MEMBER END-ACTIONS MEMBER AMl AM2 AM3 AM4 AM5 AM6

- 1 9.493 -163.092 93.528 -9.493 51.924 56.472
- 2 -14.240 61. 417 -34.452 14.240 76.393 34.452
- 3 -13.341 -23.733 27.980 13.341 -88.189 -27.980
- 4 -11. 543 -239.068 214.940 11.543 -20.691 85.060
- 5 7.351 99.731 -57.080 -7.351 128.588 57.080


SUPPORT REACTIONS JOINT ARl AR2 AR3

- 3 9.493 -163.092 93.528
- 4 14.240 76.393 34.452
- 5 -11.543 -239.068 214.940
- 6 -128.588 -7.351 57.080


5.10 Space Truss Program. The program in this section perfonns the analysis of space trusses by the method explained in Sec. 4.23. The steps in this program are similar to those in the plane frame and grid programs (Secs. 5.8 and 5.9) because all three types of structures have three possible displacements at each joint. The space truss program also bears a great similarity to the plane truss program, but the three-dimensional nature of space trusses causes some additional complications.

The main program ST for space trusses is similar to that for other types of structures, but in this case the five structure-oriented subprograms are called SDATA5, STIFF5, LDATA5, LOADS5, and RESUL5. Flow Chart 5-5 shows how statements in these subprograms differ from those for the other types of structures considered previously.

Example 1. Figure 5-7a shows a space truss having seven members, five joints, nine restraints (at three pinned supports), and six degrees of freedom. The cross-sectional areas of all members are assumed to be the same, and the following numerical values (in US units) apply:

E = 30,000 ksi L = 120 in. Ax= 10 in.2 P = 20 kips

Figure 5-7b shows the restrained structure and an appropriate numbering system. The input data required for this problem are listed in Table 5-21 (see Table 5-7 for the form of data), and the results from the computer program are given in Table 5-22.

![image 470](Matrix Analysis of Framed Structures_images/imageFile470.png)

###### 346 Chapter 5 Computer Programs for Framed Structures

z (0)

Fig. 5-7. Space truss Example 1.

Table 5-21

Data for Space Truss Example 1

Type of Data Numerical Values

Control Data I 5 I

(a) 7 5 9 3 30000.0 (b) 1 120.0 0.0 0.0

- 2 0.0 240.0 240.0
- 3 240.0 240.0 240.0
- 4 240.0 240.0 0.0


ell 5 0.0 240.0 0.0

(;l

Cl (e) I 1 2 10.0 '"§ 2 I 3 10.0 t)::l 3 2 3 10.0 ::l.... 4 2 5 10.0 U5 5 3 4 10.0

6 2 4 10.0 7 3 5 10.0

(d) 1 1 1 1 4 1 1 1

###### 5 I I I

###### ell (a) 2 2

(;l

Cl (b) 2 0.0 -20.0 0.0 -g 3 0.0 0.0 -20.0

...J0 (e) 4 -10.0 0.0 -10.0 -10.0 0.0 -10.0

I 5 0.0 10.0 0.0 0.0 10.0 0.0

![image 471](Matrix Analysis of Framed Structures_images/imageFile471.png)

5.10 Space Truss Program 347

Table 5-22

Results for Space Truss Example 1

STRUCTURE NO. 1 SPACE TRUSS NUMBER OF LOADING SYSTEMS 1

STRUCTURAL PARAMETERS

M N NJ NR NRJ E 7 6 5 9 3 30000.0

JOINT COORDINATES JOINT X Y Z

- 1 120.000 .000 .000
- 2 .000 240.000 240.000
- 3 240.000 240.000 240.000
- 4 240.000 240.000 .000
- 5 .000 240.000 .000


MEMBER INFORMATION MEMBER JJ JK AX EL CX CY CZ 1 1 2 10.000 360.000 -.333 .667 .667 2 1 3 10.000 360.000 .333 .667 .667 3 2 3 10.000 240.000 1. 000 .000 .000 4 2 5 10.000 240.000 .000 .000 -1. 000 5 3 4 10.000 240.000 .000 .000 -1. 000 6 2 4 10.000 339.411 .707 .000 -.707 7 3 5 10.000 339.411 -.707 .000 -.707

JOINT RESTRAINTS JOINT JR1 JR2 JR3 1 1 1 1 4 1 1 1 5 1 1 1

LOADING NO. 1

NLJ NLM 2 2

ACTIONS AT JOINTS JOINT AJ1 AJ2 AJ3 2 .000 -20.000 .000 3 .000 .000 -20.000

ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS MEMBER AML1 AML2 AML3 AML4 AML5 AML6 4 -10.000 .000 -10.000 -10.000 .000 -10.000 5 .000 10.000 .000 .000 10.000 .000

JOINT DISPLACEMENTS JOINT OJ1 OJ2 OJ3

- 1 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 2 • 14772E-01 -.56383E-01 .97690E-02
- 3 .1654IE-01 -.25040E-01 -.10231E-01
- 4 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 5 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO


MEMBER END-ACTIONS MEMBER AM1 AM2 AM3 AM4 AM5 AM6

- 1 30.000 .000 .000 -30.000 .000 .000
- 2 15.000 .000 .000 -15.000 .000 .000
- 3 -2.211 .000 .000 2.211 .000 .000
- 4 -22.211 .000 -10.000 2.211 .000 -10.000
- 5 12.789 10.000 .000 -12.789 10.000 .000
- 6 3.127 .000 .000 -3.127 .000 .000
- 7 -3.944 .000 .000 3.944 .000 .000


SUPPORT REACTIONS JOINT AR1 AR2 AR3

1 -5.000 30.000 30.000

- 4 -2.211 10.000 15.000
- 5 -12.789 .000 -5.000


![image 472](Matrix Analysis of Framed Structures_images/imageFile472.png)

348 Chapter 5 Computer Programs for Framed Structures

Flow Chart 5-5

5.1 Subprogram SOATA5 for Program ST

- a. Problem identification

Title: STRUCTURE NO. (lSN) SPACE TRUSS NUMBER OF lOADING SYSTEMS = (NlS)

- b. Structural parameters (same as Sec. 2.1 b in Program PT, except that NOJ = 3)
- c. Joint coordinates (similar to Sec. 2.1 c in Program PT, but z coordinates are also required)
- d. Member information (similar to Sec. 2.1 d in Program PT)


Write title.

For each member the direction cosines are computed and written, as follows:

###### t

I

###### I

Compute x, y, and z components of the member length (XCL, YCL, and ZCL), the length EL, and the direction cosines CX, CY, and CZ.

XCl = X(JK(I)) - X(JJ(I)) YCl = Y(JK(I)) - Y(JJ(I)) ZCl = Z(JK(I)) -Z(JJ(I))

###### I

El(l) = SQRT(XCl. XCl + YCl • YCl + ZCl. ZCL) CX(I) = XCL/El(l); CY(I) = YCL/El(l); CZ(I) = ZCL/El(l)

t

###### I

I,JJ(I),JK(I),AX(I),El(l),CX(I),CY(I),CZ(I) J

L_

Write information for member I.

###### t

- e. Joint restraints (same as Sec. 3.le in Program PF)
- f. Oisplacement indexes (same as Sec. I. I e in Program CB)


![image 473](Matrix Analysis of Framed Structures_images/imageFile473.png)

###### 5.10 Space Truss Program

- 5.2 Subprogram STIFFS for Program ST

a. Member stiffnesses After clearing SFF, do the following:

i--

I

5

t

1= 1, M

349

I

I

I I

I

I

I

I

I

t

I

I I

SCM = E • AX(I)/EL(I)

- SMS(1, 1) = SCM. CX(I) • CX(I)
- SMS(1, 2) = SCM. CX(I) • CY(I)
- SMS(1, 3) = SCM. CX(!) • CZ(I)
- SMS(1,4) =-SMS(1, 1)


Fill upper triangular part of member stiffness matrix SMS for a space truss member (see Table 4-40).

I

- SMS(1, 5) = -SMS(1, 2)

- SMS(1,6) =-SMS(1.3)
- SMS(2, 2) = SCM. <:Y(I) • CY(I)

- SMS(2, 3) = SCM. CY(I) • CZ(I)

- SMS(2, 4) = SMS(1, 5)
- SMS(2, 5) = -SMS(2, 2)
- SMS(2, 6) = -SMS(2, 3)


- SMS(3, 3) = SCM. CZ(I) • CZ(I)


- SMS(3, 4) = -SMS(1, 3) SMS(3, 5) = -SMS(2, 3) SMS(3, 6) = -SMS(3, 3)
- SMS(4, 4) = SMS(1, 1)


- SMS(4, 5) = SMS(1, 2)

- SMS(4, 6) = SMS(1, 3)
- SMS(5, 5) = SMS(2, 2)


- SMS(5, 6) = SMS(2, 3)
- SMS(6, 6) = SMS(3, 3)


b. Transfer tojoint stiffness matrix (same as Sec. 3.2b in Program PF)

- 5.3 Subprogram LDATAS This subprogram is the same as LDATA3 for Program PF.


![image 474](Matrix Analysis of Framed Structures_images/imageFile474.png)

- 5.4 Subprogram LOADS5 for Program ST a. Equivalent joint loads


,-

If no members are loaded, skip this part.

###### I

If member I is not loaded, skip transfer of AML to AE.

I

###### I

CXZ = SQRT(CXII) * CX(I) +CZII) * CZII» Jl =3*JJ(I)-2: J2=3*JJ(I)-1; J3=3*JJ(I) Kl =3*JK(I)-2; K2=3*JK(I)-1; K3=3dK(1)

Compute CXZ and J\ through K3.

###### I

t

If the member is vertical, go to 4.

###### I

###### I

Transfer contributions of AML to AE for an inclined member (see Eqs. 4-88).

- AE(J1) = AE(J1) - CXII) * AML(l, I)

+ (CXII) * CYII) * AML(2, I) + CZ(I) * AML(3, I)/CXZ

- AE(J2) = AE(J2) - CYII) • AML(l, I) - CXZ * AML(2, I)
- AE(J3) = AE(J3) - CZ(I) * AML(l, I)


###### I I I

+ (CY(I) • CZII) • AML(2, I) - CXII) • AML(3, I»/CXZ AE(Kl) = AE(Kl) - CXII) • AML(4, I)

+ (CX(I) • CY(I) • AML(5, I) + CZII) • AML(6, I»/CXZ AE(K2) = AE(K2) - CYII) • AML(4, I) - CXZ • AML(5, I) AE(K3) = AE(K3) - CZ(I) * AML(4, I)

###### I

+ (CYII) • CZII) * AML(5, I) - CXII) * AML(6, I)/CXZ

###### I

I

I I

4

###### I

Transfer contributions of AML to AE for a vertical member (see Eqs. 4-89).

AE(Jl) = AE(Jl) + CY(I) • AML(2, I) AE(J2) = AE(J2) - CY(I) • AML(l, I) AE(J3) = AE(J3) - AML(3, I)

+

AE(Kl) = AE(K1) + eYII) • AML(5, I) AE(K2) = AE(K2) - CY(I) • AML(4, I) AE(K3) = AE(K3) -AML(6, I)

###### I

###### I

I

###### L ____ _

b. Combined joint loads (same ·as Sec. l.4b in Program CB)

![image 475](Matrix Analysis of Framed Structures_images/imageFile475.png)

5.10 Space Truss Program

351

5.5 Subprogram RESUL5 for Program ST

Sections 5.5a and 5.5c in this subprogram are the same as in RESUL3 for Program PF. However, in Sec. 5.5b the member end-actions are cOlaputed as follows:

,--

I

Set up joint displacement indexes, calculate axial stiffness constant, and determine values of AMD (see Eqs. 4-90).

###### I

J1 =3*JJ(I)-2; J2=3*JJ(I)-1 J3 = 3 * JJ(I); K1 = 3 * JK(I) - 2 K2 = 3 * JK(I) -1; K3 = 3 * JK(I) SCM = E * AX(I)/EL(I) AMD(l) = SCM * ((DJ(J1) - DJ(K1» * CX(I) + (DJ(J2) - DJ(K2» * CY(I) + (DJ(J3) - DJ(K3» * CZ(I)

I

I I I

AMD(4) = -AMD(l); AMD(2) = 0.0 AMD(3) = 0.0; AMD(5) =0.0; AMD(6) = 0.0

###### I

###### t

###### I

###### I

I

###### I

###### I

I

I

###### I

I I

I

###### t

###### I I I

###### I

L_

![image 476](Matrix Analysis of Framed Structures_images/imageFile476.png)

![image 477](Matrix Analysis of Framed Structures_images/imageFile477.png)

y

###### r

###### 3~3//

###### / /'----

----~--~~~f----.~--._------- x

~L~~~______~________~~ 3L

/-'5' p

(a)

![image 478](Matrix Analysis of Framed Structures_images/imageFile478.png)

-4

(b)

Fig. 5-8. S pace truss Example 2.

Example 2. The space truss in Fig. 5-8a has nine members, six joints, nine restraints (at three pinned supports), and nine degrees of freedom. The members numbered I, 2, and 3 in Fig. 5-8b (the restrained structure) have cross-sectional areas equal to Ax, but the other six members have areas equal to 2Ax. For this problem the following numerical values (in SI units) are assumed:

E = 80 X 106 kN/m2 L = I m Ax = 0.01 m2 P = 240 kN

![image 479](Matrix Analysis of Framed Structures_images/imageFile479.png)

5.11 Space Frame Program 353

Table 5-23

Data for Space Truss Example 2

Type ofData Numerical Values

Control Data 1 5 1

(a) 9 6 9 3 80000000.0 (b) 1 5.0 0.0 3.0

- 2 5.0 0.0 -3.0
- 3 5.0 -3.0 0.0
- 4 0.0 0.0 3.0
- 5 0.0 3.0 0.0


(oj 6 0.0 0.0 -3.0

Q~ (c) 1 1 2 0.01 ] 2 1 3 0.01 ::l 3 3 2 0.01

....U2 54 44 31 0.020.02

CI)

6 5 I 0.02 7 5 2 0.02 8 6 2 0.02 9 6 3 0.02

(d) 4 1 1 1 5 1 1 1 6 I 1 1

~ (a) I 2

(oj

Q (b) 3 240.0 -240.0 480.0 "0 (c) 1 0.0 -720.0 0.0 0.0 -720.0 0.0

(oj

....:I0 4 0.0 120.0 0.0 0.0 120.0 0.0

Table 5-23 contains the required input data, and the final results from the computer program appear in Table 5-24.

5.11 Space Frame Program. This section contains a program for the analysis of space frames by the method given in Sec. 4.25. The steps in this program are considerably different from those in the previous programs for two principal reasons. First, the analysis is complicated by the fact that each joint has six possible displacements instead of three; second, the program incorporates the use of rotation matrices. It was not necessary to use rotation matrices in the previous programs, but the complex nature of space frames makes their use almost essential.

For Program SF (space frames) the logic in the main program is again similar to that for the other types of structures already considered. However, the five subprograms pertaining to space frames are named SDATA6, STIFF6, LDATA6, LOADS6, and RESUL6. Flow Chart 5-6 gives the

![image 480](Matrix Analysis of Framed Structures_images/imageFile480.png)

Table 5-24

Final Results for Space Truss Example 2

JOINT JOINT

DISPLACEMENTS

OJ1

OJ2

OJ3

.30312E-02 .33437E-02 • 13456E-01

.20884E-01 .17938E-01 .21017E-01

1 2

.44359E-02 .20586E-03 .41121E-02

- 3
- 4
- 5
- 6


.OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

.OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

.OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

MEMBER END-ACTIONS MEMBER AMI

AM2

AM3 .000 .000 .000 .000 .000 .000 .000 .000 .000

AM4 AM5 AM6 564.000 -720.000 .000

- 1 -564.000
- 2 -25.456
- 3 -110.309
- 4 -970.000
- 5 301. 642
- 6 1272.142
- 7 1403.291
- 8 -1070.000
- 9 -616.399


- -720.000

.000 .000

120.000 .000 .000 .000 .000 .000

AR2 -18.000

- -1224.000 282.000


25.456 .000 .000 110.309 .000 .000 970.000 120.000 .000

- -301. 642 .000 .000
- -1272.142 .000 .000
- -1403.291 .000 .000 1070.000 .000 .000


616.399 .000 .000

SUPPORT REACTIONS JOINT AR1

AR3

- 4 -739.999
- 5 2039.999
- 6 -1540.000


- -138.000
- -60.000
- -282.000


statements in these subprograms that are different from those for the other types of structures.

Example 1. A space frame having three members and four joints is shown in Fig. 5-9a. Inspection ofthe figure shows that there are twelve degrees offreedom (six at each of the joints B and C) and twelve restraints (six at each of the support

- points A and D). The joint loads on the frame consist of a force 2P in the positive x direction at point B, a force P in the negative y direction at point C, and a moment PL in the negative z sense at C. Member BC is subjected to force 4P in the positive z direction applied at the midlength of the member.

The x-y plane is a principal plane for members AB and BC, and member CD has a principal plane parallel to the y axis. Therefore, all members have the angle ex equal to zero. It is assumed that all members have the same cross-sectional properties and that the numerical values (in SI units) for this problem are the following:

E = 200 X 106 kN/m2 G = 80 X 106 kN/m2 L = 3 m Ax = 0.01 m2 Ix = 2 X 10-3 m4 Iy = Iz = 1 X 10-3 m4 P = 60 kN

Figure 5-9b shows the restrained structure with an appropriate numbering system. The data required as input to the computer program are given in Table 5-25 (see Table 5-8 for data specifications). Note that the identifier IA is zero on each of the lines containing member information. Table 5-26 shows the output of the computer program. (Tables on pp. 365-366.)

Example 2. Figure 5-lOa shows a space frame having three members, four joints, six degrees offreedom (at joint A), and eighteen restraints (six at each of the

- points B, C, and D). The frame is loaded at joint A with a force P in the negative z direction and a moment PLl4 in the negative x sense. In addition, a force of magnitude P acting in the negative z direction is applied at the middle of member AB, and a force P acting in the negative y direction is applied at the middle of member AD. All members in the frame have a principal plane XM-YM that contains


![image 481](Matrix Analysis of Framed Structures_images/imageFile481.png)

5.11 Space Frame Program 355

the point p indicated in Fig. 5-lOa. Point p is located in the plane containing joints B, C, and D (that is, the x-y plane). Any point on the line pA (except point A) would suffice to define the principal planes in this problem. Since a principal plane for member AB is parallel to the y axis, the angle a is taken to be zero for this member. However, for members AC and AD the principal planes are located by giving the coordinates of point p. (Example 2 continued on p. 364.)

Flow Chart 5-6

6.1 Subprogram SDATA6 for Program SF

- a. Problem identification

Title: STRUCTURE NO. (ISN) SPACE FRAME NUMBER OF LOADING SYSTEMS = (NLS) Write title.

- b. Structural parameters (same as Sec. 2.1 b in Program PT, except that the shear modulus G is added and NDJ = 6)
- c. Joint coordinates (similar to Sec. 2.lc in Program PT, but z coordinates are also required)
- d. Member information


Heading: MEMBER INFORMATION Subhead: MEMBER JJ JK AX XI YI ZI IA

Determine MD for a space frame member, and initialize NB to zero.

,---

I I

I, JJ(I), JK(I), AX(I), XI(I), YI(I), ZI(I), IA Read member information.

###### I

###### I

NBI = NDJ * (ABS(JK(I) - JJ(I)) + 1)

I

I I I

XCL = X(JK(I)) - X(JJ(I)); YCL = Y(JK(I)) - Y(JJ(I)); ZCL = Z(JK(I)) - Z(JJ(I)) EL(I) = SQRT(XCL * XCL + YCL * YCL + ZCL * ZCL); CX = XCL/EL(I) CY = YCL/EL(I); CZ = ZCL/EL(I); CXZ = SQRT(CX * CX + CZ * CZ)

###### t

###### I

I

I, JJ(I), JK(I), AX(I), XI(I), YI(I), ZI(I), IA Write member information.

I

![image 482](Matrix Analysis of Framed Structures_images/imageFile482.png)

Chapter 5 Computer Programs for Framed Structures

356

I

Form rotation matrix R for member I:

###### t

I

If angle ex is nonzero, read coordinates of point p.

I

###### I

XPS=XP-X(JJ(I)); YPS=YP-Y(JJ(I)); ZPS= ZP-Z(JJ(I)) (Eqs.4-96)

###### I

7

###### I

I

- R12(1) =CY; R21(1) =-CY; R33,(I) = 1.0; Rl1(l) =0.0

For a vertical member, fill R using Eq. (4-87).

- R13(1) = 0.0; R22(1) = 0.0; R23(1) = 0.0; R31 (I) = 0.0; R32(1) = 0.0


I

I

If angle ex is nonzero, fill R using Eq. (4-99).

###### t

so = SORT(XPS. XPS +ZPS. ZPS); COSA = -XPS • CY/SO; SINA = ZPS/SO R21(1) = -CY • COSA; R23(1) = SINA; R31(1) = CY • SINA; R33(1) = COSA

I I

###### ,I

For an inclined member, 7 fill R using Eq. (4-86).

Rl1(l)= CX; R12(1)= CY; R13(1)=CZ;R2l(l)=-CX. CY/CXZ; R22(1)=cxzI

,

R23(1) = -CY • CZ/CXZ; R3l (I) = -CZ/CXZ; R32(1) = 0.0; R33(1) = CX/CXZ

I IA=O+

###### I

I f angle ex is nonzero, fill R using Eq. (4-93).

###### t

###### I

YPG = R2l (I) • XPS + R22(1) • YPS + R23(1) • ZPS ZPG = R3l (I) • XPS + R32(1) • YPS + R33(1) • ZPS

SO = SORT(YPG • YPG + ZPG • ZPG); COSA = YPG/SO: SINA = ZPG/SO R21(1) = (-CX • CY * COSA - CZ * SINA)/CXZ; R22(!) = cxz • COSA R23(1) = (-CY * CZ • COSA + CX * SINA)/CXZ R31(1) = (CX • CY • SINA -CZ • COSA)/CXZ; R32(1) = -CXZ • SINA R33(1) = (CY • CZ • SINA + CX • COSA)/CXZ

###### I

I

I

----

L_

CONTINUE

![image 483](Matrix Analysis of Framed Structures_images/imageFile483.png)

- 5.11 Space Frame Program


357

Heading: MEMBER LENGTHS AND ROTATION MATRICES Subhead: MEMBER EL R11 R12 ...

Write heading anu suhheauing.

Write M lines contain-

9

ing the member number.

the length. and elements

###### I, ELII), R1111), R12 II),.

of the 3 x 3 rotation ma-

trix.

e. Joint restraints

Heading: JOINT RESTRAINTS Subhead: JOINT JR1 JR2 ... JR6

Write heading and subheading.

Clear joint restraint list.

I

I I

K, JRL(6 * K - 5), JRL(6 * K - 4), .. " JRL(6 * K)

###### I

Read and Write NRJ lines containing joint numbers and restraint list.

L

- K, JRL(6 * K - 5), JRL(6 * K -4)" .. , JRL(6 * K)


f. Displacement indexes (same as Sec. 1.1 e in Program CB)

![image 484](Matrix Analysis of Framed Structures_images/imageFile484.png)

###### 358 Chapter 5 Computer Programs for Framed Structures

- 6.2 Subprogram STIFF6 for Program SF a. Member stiffnesses


r--

###### I

###### I

Calculate eight member stiffness constants.

SCM1A = E * AX(I)/EL(I); SCM1B = G * XI(I)/EL(I)

SCM2Y = 4.0 * E * YI(I)/EL(I); SCM3Y = 1.5 * SCM2Y/EL(I) SCM4Y = 2.0 * SCM3Y/EL(I); SCM2Z = 4.0 * E * ZI(I)/EL(I) SCM3Z = 1.5 * SCM2Z/EL(I); SCM4Z = 2.0 * SCM3Z/EL(I)

I

I

###### I

Generate nonzero terms in the upper triangular portion of SM (see Table 4-1).

SM(l, 1) =SCM1A; SM(l, 7) =-SCM1A

- SM(2, 2) = SCM4Z; SM(2, 6) = SCM3Z SM(2, B) = -SCM4Z; SM(2, 12) = SCM3Z SM(3,3) = SCM4Y; SM(3, 5) = -SCM3Y
- SM(3, 9) = -SCM4Y; SM(3, 11) = -SCM3Y
- SM(4,4) = SCMl B; SM(4, 10) = -SCMl B
- SM(5, 5) = SCM2Y; SM(5, 9) = SCM3Y


I

I

I

###### t

- SM(5, 11) = SCM2Y/2.0; SM(6, 6) = SCM2Z
- SM(6, B) = -SCM3Z; SM(6, 12) = SCM2Z/2.0
- SM(7, 7) = SCM1A; SM(8, 8) = SCM4Z
- SM(8, 12) = -3CM3Z; SM(9, 9) = SCM4Y SM(9. 11) =SCM3Y; SM(10,10)=SCM1B


###### I

I

SM(ll, 11) =SCM2Y; SM(12, 12) =SCM2Z

I

I

###### I

###### I

I I

Generate terms in the lower triangular portion of SM.

t

![image 485](Matrix Analysis of Framed Structures_images/imageFile485.png)

5.11 Space Frame Program 359

###### I

t

1----

(Index for blocks of columns in matrix SM)

I

I

###### I

Determine column indexes in SM.

K1=3.K-2; K2=3.K-1; K3=3.K

I

t

###### I

f- ----

(Index for rows of SM)

I

###### I

I

SMRT(J, K1) = SM(J, K1) • R11 (I) + SM(J, K2) • R21 (I) + SM(J, K3) • R31 (I) SMRT(J, K2) = SM(J, K1) • R12(1) + SM(J, K2) • R22(1) + SM(J, K3) • R32(1) SMRT(J, K3) = SM(J, K1) • R13(1) + SM(J, K2) • R23(1) + SM(J, K3) • R33(1)

I

I I

###### I

###### L ____ -

I

Calculate matrix SMRT as the product SM RT (see

###### t

Eq.4-95).

1----

(Index for blocks of rows in matrix SMRT)

I

Determine row indexes in SMRT.

###### I

J1 = 3 • J - 2; J2 = 3 • J - 1; J3 = 3 • J

###### +

(Index for columns of SMRT)

~----

I

###### I

- SMS(J1, K) = R11(1). SMRT(J1, K) + R21(1). SMRT(J2, K) + R31(1). SMRT(J3, K)
- SMS(J2, K) = R12(1) • SMRT(J1, K) + R22(1) • SMRT(J2, K) + R32(1) • SMRT(J3, K)
- SMS(J3, K) = R13(1) • SMRT(J1, K) + R23(1) • SMRT(J2, K) + R33(1) • SMRT(J3, K)


I

I

###### L ____ -

Calculate matrix SMS by premuitiplying SM RT with

Rf (see Eq. 4-95).

b. Transfer to joint stiffness matrix

t

I

Fill vector of member displacement indexes 1M (see

IM(2) = 6 • JJ(I) - 4 IM(4) =6 .JJ(I)-2 IM(6) = 6. JJ(I) IM(8) = 6. JK(I) - 4

IM(1)=6.JJ(I)-5; IM(3) = 6. JJ(I) - 3; IM(5) = 6 • JJ(I) - 1; IM(7) = 6 • JK(I) - 5; IM(9) = 6. JK(I) -3;

I

Eqs.4-102).

###### I I

IM(10) = 6. JK(I)-2 IM(12) = 6. JK(I)

IM(11) = 6. JK(I) -1;

I

The remainder of this section is the same as Sec. 1.2b of Program CB, except that SMS replaces SM.

![image 486](Matrix Analysis of Framed Structures_images/imageFile486.png)

360 Chapter 5 Computer Programs for Framed Structures

6.3 Subprogram LDATA6 for Program SF a. Load parameters (same as Sec. 1.3a in Program CB) b. Joint loads

IfNU *- 0, do the following:

Write heading and subheading for joint loads.

Heading: ACTIONS AT JOINTS Subhead: JOINT AJ1 AJ2 ••. AJ6

,---

I

I

Read and write NLJ lines containing joint numbers and joint loads.

K. AJ(6 • K - 51. AJ(6 * K - 41 •...• AJ(6 * KI

I

- L


- K. AJ(6 • K - 51. AJ(6 * K - 41 •...• AJ(6 • KI

c. Member loads After clearing LML and AML, do the following:

Heading: ACTIONS AT ENDS OF RESTRAINED

MEMBERS DUE TO LOADS Subhead: MEMBER AML1 AML2 AML6

AML7 AML8 ... AML12

i--

I

I

I

I

I

I

- I. AML(1. I). AML(2. II•...• AML(6. I) AML(7. I). AML(8. I)•...• AML(12. II
- I. AML(1. II. AML(2. I)•...• AML(6. I) AML(7. I). AML(8. II•..•• AML(12. II


- L __


Write heading and subheadings for member loads.

Read and write 2 (NLM) lines contain ing member numbers and actions at ends of restrained members due to loads.

![image 487](Matrix Analysis of Framed Structures_images/imageFile487.png)

- 5.11 Space Frame Program
- 6.4 Subprogram LOADS6 for Program SF


361

This subprogram is similar to LOADS I for Program CB, but in Sec. 6.4a the equivalent joint loads are computed as follows:

+

Fill vector of member displacement indexes 1M (as in Sec. 6.2b).

I

IM(2)=IM(1)+1; etc. IM(8) = IM(7) + 1; etc.

IM(l) = 6 * JJ(I) - 5; IM(7) = 6 * JK(I) - 5;

I I

i--

(Index for blocks of terms in AML)

I

I

Determine indexes for individual terms in AMLandAE.

###### I

Jl =3*J-2; J2=3.J-l; J3=3*J 11 = IM(Jl); 12 = IM(J2); 13 = IM(J3)

I

tI

I

AE(ll) = AE(ll) - Rll(1). AML(Jl, I) - R21(1) * AML(J2, I) - R31(1) * AML(J3, I) AE(12) = AE(l2) - R12(1) * AML(Jl, I) - R22(1) • AML(J2, I) - R32(1) * AML(J3, I) AE(13) = AE(13) - R13(1) • AML(Jl, I) - R23(1) • AML(J2, I) - R33(1) * AML(J3, I)

###### I

###### I

I

###### L__

I

Obtain contributions to AE as - R~iAMLi

###### I

I

6.5 Subprogram RESUL6 for Program SF

- a. Joint displacements


After expanding the joint displacement vector, do the following:

Write heading and subheading for joint dis"lacements.

Heading: JOINT DISPLACEMENTS Subhead: JOINT DJl DJ2 ... DJ6

###### 1--

L r3~______~________~

Write joint numbers and joint displacements.

J, DJ(6 * J - 5), DJ(6 * J - 4), ... , DJ(6 * J)

![image 488](Matrix Analysis of Framed Structures_images/imageFile488.png)

- b. Member end-actions


Heading: MEMBER END-ACTIONS Subhead: MEMBER AMl AM2 AM6 AM7 AM8 ... AM12

,---

Write heading and subheadings for member end-actions.

I I

Fill arrays SMRT and 1M for member I

Similar to Sec. 6.2.

I

,---

(Index for rows of SMRT)

###### I

###### I

tI

I

Initialize AMD(J) to zero.

,-

###### I

###### I

I I

(Index for columns of SMRT)

###### I I I I

###### I

I

Obtain displacement index I I from vector 1M.

t

I

I

4

L

Calculate AMD by matrix-vector multiplication of SMRT and OJ (see Eq. 5-5b).

AMD(J) = AMD(J) + SMRT(J, K) • DJ(l1)

###### I

I

L_

Add AML(J,I) and AMD(J) to produce final end-action AM(J) (see Eq. 5-5a).

###### I

I

Write member number I and final member end-actions.

###### I

I,AM(1), AM(2), ... , AM(6) AM(7), AM(8), ... , AM(12)

I

###### t

(Index for blocks of terms in AMD)

I

I

I

###### I

J1 =3. J - 2; J2 =3 * J -1; J3 =3 * J 11 =IM(J1); 12 = IM(J2); 13 =IM(J3)

Determine indexes for individual terms in AMD and AR.

###### t

I

I

![image 489](Matrix Analysis of Framed Structures_images/imageFile489.png)

t

t

I

AR(l1) = AR(ll) + Rll(1). AMD(J1)

###### I

- + R21(1) * AMD(J2) + R31 (I) • AMD(J3)

AR(12) = AR(12) + R12(1) * AMD(Jl)

- + R22(1) * AMD(J2) + R32(1) * AMD(J3)

AR(l3) = AR(13) + R13(1) * AMD(Jl)

- + R23(1) * AMD(J2) + R33(1) * AMD(J3)


###### I

I

###### I I I

###### I

I

I

I

###### t

###### I

###### I

###### I

I

+ I L Forrestrainedcases, transfer contributions

- IL_ ofAMDtoreactions AR(seeEq. 5-6b).

c. Support reactions After obtaining reactions, do the following:

Heading: SUPPORT REACTIONS Subhead: JOINT ARl AR2 ... AR6

,--

I

I

I

I I

t

I

I

Jl=6.J-5; J2=6*J-4; ... ; J6=6*J Nl = JRL(Jl) + JRL(J2) + ... + JRL(J6)

J, AR(J1), AR(J2), "', AR(J6)

- L __ _


Write heading and subheading for joint reactions.

Set up indexes J I, 12, ... , J6. Also, add the corresponding items in JRL to obtain

###### NI.

If Nl is zero, skip printing of reactions.

Write joint number and suppon reactions at a joint where at least one restraint exists.

RETURN END

![image 490](Matrix Analysis of Framed Structures_images/imageFile490.png)

y

4P P

------+-------~-\----,_--~---x

z y (0)

###### t5 tIl

t21 4 CD ta

7 10 ~-- 2

###### 91

12/

x

###### 121-----

}~"~a 4 19 22

###### 124

z (b)

Fig. 5-9. Space frame Example 1.

The cross-sectional properties of all members are assumed to be the same, and

the numerical constants in the problem are as follows: E = 10,000 ksi G = 4,000 ksi L = 96 in. Ix = 64 in.' Iy = 28 in.' Iz = 80 in."

Ax = 9 in.2 P = 5 kips

Figure 5-lOb shows a numbering system for the restrained structure. Input data required for this problem are listed in Table 5-27. Note that the lines containing member information for members 2 and 3 are each followed by a line that gives the coordinates of point p.

The calculation of actions AML at the ends of the restrained members due to loads (the last four data cards) requires further explanation in this example. The end-actions AMLl for member 1are obtained easily because the load P applied at the middle lies in a principal plane for the member. Figure 5-11 shows all of the endactions for this member. Note that the orientation of the member axes in the figure results from the sequence of {3 and 'Y rotations depicted in Fig. 4-38 (see Sec. 4.22).

On the other hand, the load P applied to member 3 does not lie in a principal plane of the member. In order to calculate the end-actions AML3 for this member, the components ofthe load P in the directions of member axes must be ascertained.

![image 491](Matrix Analysis of Framed Structures_images/imageFile491.png)

Table 5-25

Data for Space Frame Example 1

Type o/Data Numerical Values Control Data I 6 I

(a) 3 4 12 2 200000000.0 80000000.0 (b) I 0.0 3.0 0.0

0-ais....o:l 432 0.09.06.0 0.00.03.0 0.03.00.0

:::l

U2 (c) 2I 3I 2I 0.010.01 0.0020.002 0.0010.001 0.0010.001 00

###### r/l

- 3 2 4 0.01 0.002 0.001 0.001 0 (d) 3 I 1 1 1 I 1
- 4 1 I I 1 I I


(a) 2 I

is

o:l (b) I 120.0 0.0 0.0 0.0 0.0 0.0

0

"0 2 0.0 -60.0 0.0 0.0 0.0 -180.0

o:l

(c) I 0.0 0.0 -120.0 0.0 180.0 0.0 0.0 -120.0 0.0 -180.0

0.0 0.0

0

...J

One method for doing this is to use the rotation of axes technique represented by Eq. (4-57) in Sec. 4.15. Thus,

A),! = RAs (4-57)

repeated

Figure 5-12 shows the member axes for member 3 as well as the load P applied in the negative y direction. The rotation matrix R for the member axes may be obtained either from the geometry of the figure or from Eq. (4-93) in Sec. 4.24 (using the coordinates of point p if desired). This rotation matrix is the following:

16 12 9 V481 - V481 - V481

36 27 20 R = - 5V481 5V481 - V481

- (a)
- (b)


3 4 5 5 o

Because the applied load P is 5 kips, the vector As becomes

As= {O, -5, O}

Substitution of expressions (a) and (b) into Eq. (4-57) produces the vector AM, as follows:

A~! = {60, -27, -4V 481}/V481 = {2.736, -1.231, -4.000} (c) The elements in this vector are the components of the applied load in the directions of member axes. End-actions AM!.3 caused by these forces acting on member 3 are listed in the last two lines of Table 5-27. When the data in Table 5-27 are analyzed by Program SF, the final results obtained are as shown in Table 5-28.

![image 492](Matrix Analysis of Framed Structures_images/imageFile492.png)

366 Chapter 5 Computer Programs for Framed Structures

Table 5-26

Results for Space Frame Example 1

STRUCTURE NO. 1 SPACE FRAME NUMBER OF LOADING SYSTEMS 1

STRUCTURAL PARAMETERS

M N NJ NR NRJ E G 3 12 4 12 2 200000000.0 80000000.0

JOINT COORDINATES

JOINT X Y Z 1 .000 3.000 .000 2 6.000 3.000 .000 3 .000 .000 .000 4 9.000 .000 3.000

MEMBER INFORMATION

MEMBER JJ JK AX XI YI 1 1 2 .0100 .0020 .0010 2 3 1 .0100 .0020 .0010 3 2 4 .0100 .0020 .0010

ZI .0010 .0010 .0010

IA 0

- 0

- 0

R33

- 1. 000


- 1. 000


MEMBER LENGTHS AND ROTATION MATRICES MEMBER EL Rll R12 R13 R21 R22 R23 1 6.000 1.000 .000 .000 .000 1. 000 .000 2 3.000 .000 1.000 .000-1.000 .000 .000 3 5.196 .577 -.577 .577 .408 .816 .408

R31 R32 .000 .000 .000 .000

.707

- -.707 .000

AJ5 .000 .000

AML5 AML11 180.000 -180.000

OJ5

- -.16232E-02


JOINT RESTRAINTS JOINT JRl JR2 JR3 JR4 JR5 JR6 3 1 1 1 1 1 1 4 1 1 1 1 1 1

LOADING NO. 1

NLJ NLM 2 1

ACTIONS AT JOINTS JOINT AJI AJ2 AJ3 AJ4 1 120.000 .000 .000 .000 2 .000 -60.000 .000 .000

AJ6 .000 -180.000

ACTIONS AT ENDS OF RESTRAINED MEMBERS DUE TO LOADS MEMBER AMLl AML2 AML3 AML4

AML6

AML7 AMLB AML9 AMLI0 1 .000 .000 -120.000 .000 .000 .000 -120.000 .000

AML12 .000 .000

JOINT DISPLACEMENTS JOINT OJI OJ2 OJ3 OJ4

DJ6 .68133E-03

- 1 -.85941E-03 .57764E-04 .50076E-02 .23933E-02
- 2 -.11761E-02 .32532E-02 • 52555E-02 . 12884E-02
- 3 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO
- 4 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO


. 17209E-02 .OOOOOE+OO .OOOOOE+OO

-.77147E-03 .OOOOOE+OO .OOOOOE+OO

MEMBER END-ACTIONS MEMBER AMI AM2 AM3 AM4

AM5

AM6 AM12

AM7 AM8 AM9 AMI0

AM 11 86.569

- 1 105.548 -38.509 -126.013 29.464

-105.548 38.509 -113.987 -29.464

- 2 -38.509 14.452 -126.013 86.569 38.509 -14.452 126.013 -86.569


- -67.100
- -163.954
- -23.744 67.100
- -32.181 79.946

AR6

- -23.744 37.163


- -50.491 348.575

29.464 46.703

- -77.711

AR5 86.569

- -75.808


183.623 9.192 5.967 -21. 404 -183.623 -9.192 -5.967 21. 404

SUPPORT REACTIONS JOINT ARl AR2 AR3 AR4

- 3 -14.452 -38.509 -126.013 -348.575
- 4 -105.548 98.509 -113.987 -75.898


![image 493](Matrix Analysis of Framed Structures_images/imageFile493.png)

5.11 Space Frame Program 367

Table 5-27

Data for Space Frame Example 2

Type of Dala Numerical Values

Control Data 2 6 1

(a) 3 4 18 3 10000.0 4000.0 (b) 1 128.0 96.0 72.0

2 128.0 192.0 0.0 .....c<l 3 0.0 0.0 0.0 0c<l 4 256.0 0.0 0.0

«i.... (c) I 1 2 9.0 64.0 28.0 80.0 0 ....u;::l 2 3 1 9.0 64.0 28.0 80.0 1 .....2 2 128.0 96.0 0.0

VJ 3 1 4 9.0 64.0 28.0 80.0 1

3 128.0 96.0 0.0 (d) 2 1 1 I I I 1 3 1 1 I I 1 1 4 1 1 1 I 1 1

(a) 1 2

.....c<l (b) 1 0.0 0.0 -5.0 -120.0 0.0 0.0 0c<l (c) 1 -1.5 2.0 0.0 0.0 0.0 60.0 "0c<l -1.5 2.0 0.0 0.0 0.0 -60.0 0

....l 3 -1.368 0.616 2.0 0.0 -87.727 27.0 -1.368 0.616 2.0 0.0 87.727 -27.0

Table 5-28

Final Results for Space Frame Example 2

JOINT DISPLACEMENTS JOINT DJI DJ2 OJ3 DJ4 DJ5 DJ6 1 -.21764E-03 -.40619E-02 -.16736E-Ol -.52022E-02 .18704E-03 -.44953E-02 2 .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

.OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO .OOOOOE+OO

MEMBER END-ACTIONS MEMBER AMI AM2 AM3 AM4 AM5 AM6

AM7 AM8 AM9 AMI0 AM 11 AM12 3.594 .178 .406 6.073 -32.492 -84.001 -6.594 3.822 -.406 -6.073 -16.233 -134.638 2 4.744 .485 -.131 8.080 7.610 27.616

- -4.744 -.485 .131 -8.080 15.390 57.444 3.214 .178 1. 678 -2.995 -50.178 -24.964
- -5.950 1.054 2.322 2.995 106.594 -51.865


SUPPORT REACTIONS JOINT ARI AR2 AR3 AR4 AR5 AR6

- 2 -.406 -2.982 7.014 -134.638 -14.599 -9.343
- 3 3.699 2.610 1. 505 -8.177 28.387 -3.624
- 4 -3.293 5.372 1. 480 -63.927 -16.885 -98.434


![image 494](Matrix Analysis of Framed Structures_images/imageFile494.png)

368 Chapter 5 Computer Programs for Framed Structures

###### ~L _ _.,j..__ ¥

y

![image 495](Matrix Analysis of Framed Structures_images/imageFile495.png)

###### L

(ol

![image 496](Matrix Analysis of Framed Structures_images/imageFile496.png)

###### t23 t20

19 22 18 1~ If----=:;----'=---------::;~ - .....

'~ ......-"'---4

Z~ 24 21

(bl

Fig. 5·10. Space frame Example 2.

5.12 Combined Program for Framed Structures. Although the primary objective in this chapter is to present programs for individual types of structures, it is also of interest to combine the work into a larger program for analyzing all types of framed structures. This secondary objective can be fulfilled using the subprograms already discussed for the various types of structures.

Flow Chart 5-7 shows the main program (called FS) for analyzing all types offramed structures. It has the same attributes as the main programs CB, PT, PF, etc., for analyzing continuous beams, plane trusses, plane frames, etc. However, in this case the program must branch in accordance with the type of structure being processed. For this purpose, the five subprograms named SDATA, STIFF, LDATA, LOADS, and RESUL are

![image 497](Matrix Analysis of Framed Structures_images/imageFile497.png)

- 5.12 Combined Program for Framed Structures 369


![image 498](Matrix Analysis of Framed Structures_images/imageFile498.png)

###### " I"

,jl.5K

###### '!w-r

y.~"-___~______!J-

I ,t\~ \

'\, \. 72"~

ZM

Fig. 5·11. Restraint actions at ends of member 1.

![image 499](Matrix Analysis of Framed Structures_images/imageFile499.png)

Fig. 5·12. Member axes for member 3.

![image 500](Matrix Analysis of Framed Structures_images/imageFile500.png)

Chapter 5 Computer Programs for Framed Structures

370

Flow Chart 5-7

Main Program FS for Framed Structures

###### Comments

Read structure number ISN, type of structure ITS, and number of loading systems NLS.

Use subprogram SDATA for branching to SDATAI, SDATA2, ... ,SDATA6.

Use subprogram STIFF for branching to STiFFI, STIFF2, ... , STlFF6.

###### r

Factor the upper band of the stiffness matrix SFF, stored as a rectangular array ofsize N x NB. If SFF is not positive definite, go to 103.

I I

Initialize loading number LN to zero.

###### I

Increment loading number by one for each new loading system.

~

I

Use subprogram LDATA for branching to LDATAI, LDATA2, ... , LDATA6.

I

###### I I

Use subprogram LOADS for branching to LOADSI, LOADS2, ... , LOADS6.

###### I I

Solve for free joint displacements DF, using the factored stiffness matrix SFF and the first N elements in vector

AC.

###### I I

Use subprogram RESUL for branching to RESULl, RESUL2, ... RESUL6.

###### +

If NLS is greater than LN, go to 102 and process another set of loads.

###### I I

I

Otherwise, go to 101 and process another structure.

I

L

Discontinue calculations and write message when matrix SFF is not positive definite.

999 STOP

END

written as six-way branching routines that call upon other subprograms to do the actual calculations.

For example, subprogram SDATA branches as shown in Flow Chart

- 5-8 and uses subprogram SDATAI to read and write structural data for a continuous beam. It uses subprogram SDATA2 to read and write structural


![image 501](Matrix Analysis of Framed Structures_images/imageFile501.png)

5.12 Combined Program for Framed Structures 371

Flow Chart 5-8

Subprogram SDAT A for Program FS

###### Comments

If ITS = I, use subprogram SDATAI for a continuous beam.

- If ITS = 2, use subprogram SDATA2 for a plane truss.
- If ITS = 3, use subprogram SDATA3 for a plane frame.
- If ITS = 4, use subprogram SDATA4 for a grid.
- If ITS = 5, use subprogram SDATA5 for a space truss.
- If ITS = 6, use subprogram SDATA6 for a space frame.


RETURN END

data for a plane truss, and so on. The layouts for the other four branching subprograms are the same as that for SDAT A and need not be shown here.

Alternatively, the main programs CB, PT, PF, etc., for each type of structure could be converted to subprograms that are used by the new main program FS. This arrangement would require only one six-way branching routine in the main program to distinguish one type of framed structure from another. Flow Chart 5-9 shows the alternative main program devised for this purpose.

While such combined programs are rather elegant, they are not very suitable for small machines where core storage is limited. The computer code requires space that could otherwise be occupied by data for problems with large numbers of degrees of freedom. In addition, a COMMON declaration designed for the most complicated type of structure (the space frame) must be used in the main program FS and all of the structure-oriented subprograms, regardless of the type of structure involved. In spite of these drawbacks, readers may wish to code combined programs after they have written all ofthe subprograms required for the various types offramed structures.

![image 502](Matrix Analysis of Framed Structures_images/imageFile502.png)

Chapter 5 Computer Programs for Framed Structures

372

Flow Chart 5-9

Alternative Main Program FS for Framed Structures

Comments

Read control data.

If ITS = I, use subprogram CB for a continuous beam. If SFF is not positive definite, go to 202.

###### l

I I

###### --i

Similar, but for a plane truss.

I

I

###### -.J

Similar, but for a plane frame.

I

I

###### -rI

Similar, but for a grid.

I I

J

Similar, but for a space truss.

I

I

I

~==;::===:::::JI -1

Similar, but for a space frame.

I

###### •I

Go to 20I and process another structure.

I

202

____ -.J Discontinue calculations and

Message: SFF NOT POS. DEF.

write message when matrix SFF is not positive definite.

###### 999 STOP END

References

###### I. Davis, G. B., and Hoffman, T. R., FORTRAN 77: A Structured, Disciplined Style, 3rd

ed., McGraw-Hill, New York, 1988.

- 2. Hammond, R. H., Rogers, W. B., and Crittendon, J., Introduction to FORTRAN 77 and the Personal Computer, McGraw-Hill, New York, 1987.
- 3. Koffman, E. B., Problem Solving and Structured Programming in FORTRAN 77, 3rd ed., Addison-Wesley, Reading, Mass., 1987.


![image 503](Matrix Analysis of Framed Structures_images/imageFile503.png)

###### 6

###### Additional Topics for the Stiffness Method

6.1 Introduction. The computer programs given in the preceding chapter apply to the analysis of linearly elastic framed structures of arbitrary configuration but consisting of prismatic members of only one material. These structures are assumed to undergo small displacements when subjected to applied loads, and the principle of superposition is used throughout the analyses. Only actions applied at joints and fixed-end actions due to loads on members are acceptable as input load data for the programs.

Many useful extensions and alternatives are feasible, some of which are discussed briefly in this chapter. The material is intended to be supplementary to the subject matter of previous chapters, and there is no attempt to give complete and detailed explanations. Instead, the objective is to present additional topics that the interested reader may wish to develop and program.

In computer analysis there is usually more than one method for obtaining the desired results. As an illustration of the possibilities, consider a structure composed of members that are not all of the same material. Such a structure can be analyzed using the programs in this book if the crosssectional properties of members are first transformed to the equivalent properties for a structure of only one material. A second approach would be to provide the elastic moduli for each member as a part of the input data. The latter method is more appropriate, but it requires new programming and more data. On the other hand, the first method is representative of contrivances that can be used by the analyst to extend the scope ofexisting programs merely by manipulating the input data.

The first topics discussed in this chapter (Secs. 6.2 and 6.3) are the geometric specializations of rectangular framing and symmetric and repeated structures. The next three sections (6.4 through 6.6) deal with load considerations not covered by the documented programs. Then several topics relating to support conditions are discussed (Secs. 6.7 through 6.9). These topics include support displacements, oblique supports, and elastic supports. Most of the remaining sections in the chapter are devoted to member characteristics that alter the stiffnesses and fixed-end actions for individual members. Covered under this category are nonprismatic members, curved members, releases in members, elastic connections, shearing deformations, offset connections, and axial-flexural interactions. Finally, the formal method

373

![image 504](Matrix Analysis of Framed Structures_images/imageFile504.png)

374 Chapter 6 Additional Topics for the Stiffness Method

for imposing axial constraints in plane and space frames is presented in the last section of this chapter.

6.2 Rectangular Framing. Many framed structures have geometric properties that allow simplifications in their analyses. For example, continuous beams consist of collinear members, and advantage of this fact is taken in the analysis of such structures. Similarly, plane and space structures with rectangular framing are much easier to analyze than those of skew geometry. The joint coordinates, member orientations, and loads may be specified with a minimum of input data, and no rotation-of-axes transformations are required.

The programs in this book will, ofcourse, accommodate structures with rectangular framing, but the computations will not be particularly efficient. Special-purpose programs should be used for the analysis of structures with special geometry in order to take advantage of the simplifications inherent in such problems.

Figures 6-1 through 6-3 show examples of structures with rectangular framing. These are a plane frame, a grid, and a space frame. Each member in a structure of this type has its axis parallel to one of the coordinate axes for the system. Therefore, the member axes should always be taken parallel to the structural axes, and member stiffness matrices should be generated in a form that permits a direct transfer of terms to the joint stiffness matrix without rotation of axes. For example, both the horizontal and the vertical members in the rectangular plane frame (see Figs. 6-1b and 6-1c) have their member axes XM, YM, and ZM parallel to the structural axes x, y, and z. Such axes are also indicated for typical members of the rectangular grid (see Figs.

- 6-2b and 6-2c) and the rectangular space frame (see Figs. 6-3b, 6-3c, and 6-3d). In the latter type of structure, principal axes of members are usually parallel to the structural axes. However, if this is not the case, a single rotation transformation will be required for each member.


Rectangular frames are most commonly used for multi-story buildings [1], in which the horizontal displacements of floor and roof diaphragms are of primary interest. Figure 6-3a shows such diaphragms (or laminae) for a three-story example treated as a space frame. Each lamina is assumed to have infinite rigidity in its own plane, but zero rigidity normal to the plane. Consequently, the joints at a particular framing level are constrained to displace in accordance with the rigid-body motions of the diaphragm at that level. These motions consist of the x and Y translations and the Z rotation indicated by the numbered arrows at arbitrarily selected reference points PI, P2, and P3, which are considered to be rigidly attached to the laminae in Fig. 6-3a. At each joint there remain three independent displacements, which are the x and Y rotations and the ztranslation. These displacements are indicated by the numbered arrows at the typical joint j at the right-hand side of Fig. 6-3a. Thus, the independent joint translations are the same as those for a grid (see also Fig. 6-2a). If nj is the number of joints at a given level, the

![image 505](Matrix Analysis of Framed Structures_images/imageFile505.png)

###### 6.2 Rectangular Framing 375

- 1 ____
- 2___
- 3 ------

r

2/

j

- 4 ____


- 6 ______
- 7 ----


om om ~ /7/7? ~

###### (a) r

Sym .

IYM

IYM

. t~5

1t 0) 3t //

xM ZM/

2/j /*

###### 4 0

###### (b)

(c)

Fig. 6-1. Rectangular plane frame: (a) structure, (b) member parallel to x axis, and (c) member parallel to yaxis.

number of independent displacements for that level is 3nj + 3 (instead of 6n) due to the presence of the lamina.

Similarly, if axial strains are omitted in the horizontal members (beams) of the plane building frame in Fig. 6-la, the beams are implied to be infinitely rigid in their axial directions. Consequently, all points at a

![image 506](Matrix Analysis of Framed Structures_images/imageFile506.png)

Chapter 6 Additional Topics for the Stiffness Method

376

z

###### L x

/,"--svm.

/

(al

/

(b)

(e)

- Fig. 6-2. Rectangular grid: (a) structure, (b) member parallel to x axis, and (c) member parallel to yaxis.


given level are inherently constrained to translate the same amount in the x direction. That is, each horizontal line of beams in Fig. 6-1a may be considered to be the one-dimensional counterpart of a two-dimensional lamina in Fig. 6-3a. Thus, there is only one independent translation in the x direction at each framing level, as indicated by the numbered arrows at the left side of Fig. 6-1a. In addition, there are two independent displacements at each joint, shown as the y translation and the z rotation at a typical joint j. These joint displacements are the same as those for a beam, so the displacement vectors indicated in Fig. 6-1b imply the generation of only a 4 x 4 member stiffness matrix for a horizontal member. On the other hand, the vertical member (column) in Fig. 6-lc provides finite terms for a 6 x 6 member stiffness matrix. Note that the displacement indexes at the ends of the members are numbered in a sequence that takes independent joint displacements before story displacements and proceeds from top-tobottom and left-to-right in the structure. Similar numbering sequences are also indicated at the ends of the members in Figs. 6-3b, c, and d for the space frame.

![image 507](Matrix Analysis of Framed Structures_images/imageFile507.png)

- 6.2 Rectangular Framing 377


![image 508](Matrix Analysis of Framed Structures_images/imageFile508.png)

Diaphragm

2

![image 509](Matrix Analysis of Framed Structures_images/imageFile509.png)

(0)

![image 510](Matrix Analysis of Framed Structures_images/imageFile510.png)

- (b)

0

11

/YM

5/

;t 4-10 xM

,J

- (c) (d)


![image 511](Matrix Analysis of Framed Structures_images/imageFile511.png)

- Fig. 6-3. Rectangular space frame: (a) structure, (b), (c), and (d) members parallel to x, y, and z axes, respectively.


The omission of axial strains in the columns of a building frame would produce constraints against vertical translations at every joint (assuming that column lines are continuous). These constraints would serve to further reduce the number of degrees of freedom and allow additional simplifica-

![image 512](Matrix Analysis of Framed Structures_images/imageFile512.png)

378 Chapter 6 Additional Topics for the Stiffness Method

tions in the analysis. However, axial strains in columns can be a significant factor in the analysis of tall buildings, and their omission may cause serious discrepancies.

6.3 Symmetric and Repeated Structures. When a structure is symmetric with respect to one or more planes, the problem may be reduced to a fraction of its original size [2]. This statement applies even when the loading pattern is not symmetric, because any unsymmetric loading can be decomposed into a symmetric and an antisymmetric loading. The reduction may be accomplished by providing data for only a portion of the structure and by introducing artificial restraints at joints located on planes of symmetry. In addition, the properties of members that lie in those planes must be altered. These changes may be incorporated into the structural data and do not necessitate any additional programming. If there is one plane of symmetry (as in the plane frame in Fig. 6-1a), only half of the structure need be analyzed. If two planes of symmetry exist (as in the grid in Fig. 6-2a), only a quarter need be analyzed, and so on.

Ifthe loading is symmetric with respect to a plane of structural symmetry, the deformations, reactions, and member actions will also be symmetric with respect to the same plane. Therefore, joints on a plane of symmetry must be restrained in such a manner that the structure deforms symmetrically with respect to that plane. Figure 6-4a portrays schematically a typical joint j located on a plane of symmetry that is normal to the x axis. The loading on the structure is assumed to be symmetric with respect to the same plane. The figure also shows joints k and k' that are symmetrically located on opposite sides of the plane. Displacement vectors at each of these joints indicate a symmetric pattern ofdeformation. Note that translations in the y and zdirections and rotations in the x sense are all in positive directions at both points k and k'. Therefore, we conclude that the same displacements on the plane of symmetry must be free to occur. These displacement vectors at point j are labeledj2,j3, andj4. On the other hand, the translations in the x direction and the rotations in the y and z senses are in opposite directions at points k and k'. Thus, the same displacements on the plane of symmetry must be set equal to zero. Hence, the vectors labeled jl, j5, and j6 at point j need to be restrained, as indicated by the small slashes on their arrows. In general, the component of joint translation normal to a plane of symmetry and the components of rotation in the plane must be prevented in order to enforce a symmetric pattern of distortion.

If the loading is antisymmetric with respect to a plane of structural symmetry, the deformations, reactions, and member actions will also be antisymmetric with respect to the same plane. Therefore, joints on a plane of symmetry must be compelled to displace in an antisymmetric manner. For this purpose, Fig. 6-4b depicts displacements at points k and k' that represent an antisymmetric pattern of deformation. That is, the translations

![image 513](Matrix Analysis of Framed Structures_images/imageFile513.png)

###### 6.3 Symmetric and Repeated Structures

379

Y Planeof symmetry t t )1 t

###### ---.- /li5 I IT--

k' /' l/ I

/~ // ti2 iill' 1I11k

IY'k' Y

)-----iI-;-r-------7-----';~· I ---;...1--r--- x

I /;3~ Jj:"" : /

I/zv ;k'

Jl~ ~//

v/Z;k

Z

~ Xik

LXik'

I //

I /

1/

###### V-

(0)

Plane of symmetry t

y

###### t/ /)1I t

###### -!'.-- A/5: kT--

###### /. / t lill'/:Yk

I / i2 }, I j

Y'k' (

~----iI-;-r_----7-~;~·_ ~---;...I--r---x Ix i1 ) i4 I /7 I , i3 / ~/ Zik

Iiii' /

Z

~'i6 .// /

.,LlI /X;k~

v/I /

( b)

- Fig. 6-4. Joint restraints on planes of symmetry: la) symmetric loading and Ib) antisymmetric loading.


- in the x direction and the rotations in the y and z senses are all in positive directions at both points k and k'. From this we conclude that the same displacements on the plane of symmetry must be allowed to occur freely. They are the displacements labeled j1, j5, and j6 at point j. On the other hand, the translations in the y and zdirections and the rotations in the x sense are in opposite directions at points k and k'. Therefore, the same displacements on the plane of symmetry need to be set equal to zero. This may be accomplished by introducing restraints corresponding to j2, j3, and j4, as indicated by the slashes on their vectors. In summary, the components of joint translation in a plane of symmetry and the component of rotation normal to the plane must be prevented to give a pattern of distortion that is antisymmetric with respect to the plane.


![image 514](Matrix Analysis of Framed Structures_images/imageFile514.png)

380 Chapter 6 Additional Topics for the Stiffness Method

The rigidities of members lying in a plane of symmetry (as in Fig. 6-1a) must be halved in order to divide the structure into two equal parts. In the event that a member lies in two planes of symmetry, its rigidities must be divided by four, and so on. If a member is normal to and bisected by a plane of symmetry (see Fig. 6-2a), a new joint is introduced at midlength and restrained as described above.

As an example, consider the plane frame in Fig. 6-5a, which is symmetric with respect to the y-z plane. The applied force P represents an unsymmetric loading that can be decomposed into the symmetric and antisymmetric patterns shown in Figs. 6-5b and 6-5e, respectively. An analysis for the symmetric pattern may be carried out using either the left-hand half of

I~Sym.

C 0

###### I

H

A /-~

E

~I

(a)

###### A E A E

(b) (e) (d)

A E

(e) (f) (g)

###### Fig. 6-5. Symmetric plane frame example.

![image 515](Matrix Analysis of Framed Structures_images/imageFile515.png)

- 6.3 Symmetric and Repeated Structures 381


the structure (Fig. 6-5c) or the right-hand half (Fig. 6-5d). The left-hand set of structural axes x', Y, and z pertain to the former case, and the right-hand set x, y, and z pertain to the latter case. Since the use of right-hand axes is always preferred, the latter case represents the better choice. The artificial restraint conditions at point C preclude translation in the x direction (across the plane of symmetry) and rotation in the z sense (in the plane of symmetry). However, there is no restraint at C against translation in the y direction (in the plane of symmetry). Therefore, the corresponding reaction

- in the y direction at point C will be zero in the symmetric analysis. Similarly, an analysis for the antisymmetric pattern of loading (Fig. 6-Se)


could be performed using either half of the structure, as indicated in Figs. 6-Sf and 6-Sg. Again, the right-hand half (Fig. 6-Sg) would be preferred because of the orientation of structural axes. In this case the artificial restraint conditions at point C allow the x translation and the z rotation to occur, but not the y translation. Hence, the corresponding reactive force in the x direction and moment in the z sense at point C will be zero in the antisymmetric analysis.

To obtain the solution for the right-hand half of the original problem, results from the antisymmetric analysis must be added to those from the symmetric analysis. However, the total solution for the left-hand half of the structure is obtained by subtracting the antisymmetric results from the symmetric results (for the right-hand half) and reflecting them across the plane of symmetry.

Because the subject of repeatability [3] is closely related to symmetry and antisymmetry, it also will be included in this section. Figure 6-6 illustrates two categories of repeated substructures that are characterized as rotational and translational repeatability. Part (a) of the figure shows a portion of a circular grid that is repeated n times in the () direction. In order that this substructure may deform in the same manner as the other n - 1 substructures, it must sustain the same pattern ofloading. Then for analytical purposes it must be subjected to the typical constraint equations

Drj = Drk DOj = DOk Dzj = Dzk (a)

where the joints j and k have corresponding locations on adjacent substructures. In Eqs. (a) the first two expressions impose equality of rotations in the rand () senses at points j and k. The third expression states that translations in the z direction at the two points must be equal. These constraint equations will be combined with equations of equilibrium for all of the free displacements in the substructure.

Figure 6-6b shows a substructure of a plane frame that is repeated n times in the x direction. In this case the points j and k again have corresponding locations on two adjacent substructures. Now the following types of constraint equations must be imposed:

(b)

![image 516](Matrix Analysis of Framed Structures_images/imageFile516.png)

###### 382 Chapter 6 Additional Topics for the Stiffness Method

![image 517](Matrix Analysis of Framed Structures_images/imageFile517.png)

(0 )

![image 518](Matrix Analysis of Framed Structures_images/imageFile518.png)

y

A 8

z

(b)

Fig. 6-6. Repeated substructures: (a) rotational and (b) translational.

The first two equations give equality of translations in the x and y directions at pointsj and k, while the third implies that the rotations in the zsense must be equal. This case of a long series of connected subframes is an approximation, because there can be only a finite number n of such substructures. The first and last subframes in the series must be analyzed separately, using previously computed constrained displacements at connections to interior subframes.

Appearing in Figs. 6-6a and b are the letters A, B, and C, which denote the following locations of displacements in the substructures: (A) joints at the first boundary, (B) interior joints, and (C) joints at the second boundary. Now let all of the displacements of type A be equal to the corresponding displacements of type C. Thus,

(c)

This expression represents the constraint conditions for the whole substructure. Also, equilibrium equations for all joints in the substructure may be written in the partitioned matrix format

[::: ::::::][~:] [::]

(d)

SeA SeB See De Ae

Expanding these equations gives

![image 519](Matrix Analysis of Framed Structures_images/imageFile519.png)

- 6.4 Loads Between Joints


383

SAADA + SABDB + SACDC = AA SBADA + SBBDB + SBCDC = AB SCADA + ScBDB + SCCDC = Ac

- (e)
- (f)
- (g)


From Eq. (c) substitute DA for Dc, and add Eqs. (e) and (g) to obtain

(6-1 )

in which

SAA + SAC + SCA + Scc SAB + SCB = S~A

(6-2a) (6-2b) (6-2c)

Equations (6-1) and (6-2) formalize the process of analyzing either rotational or translational repeated substructures.

6.4 Loads Between Joints. In Chapters 4 and 5 the effects of loads acting on members were handled indirectly by making use of the fixed-end actions caused by such loads. It is also possible to extend the computer programs of Chapter 5 to accept these loads directly as input data, and some of the feasible techniques for doing so are covered in the following discussion (for prismatic members).

From the previous descriptions of member-oriented and structure-oriented axes, it is apparent that loads acting on members may be resolved into components parallel to either set of axes. In general, it is desirable to resolve the member loads into components parallel to the member axes (XM, YM, and ZM)' The loads on beam and grid structures are usually aligned with the member axes by their very nature, but the orientations of loads on plane and space frames may be quite general. Therefore, some preliminary effort may be required to resolve the loads into components parallel to member axes, as demonstrated for a space frame member in Example 2 of Sec. 5. 11 .

It frequently happens that the loads on truss members are expressed with respect to structure-oriented axes, and it may be more convenient to handle them in that form than to resolve them into components parallel to member axes. The reason for this conclusion is that the pinned-end actions in a restrained truss structure are easily calculated, regardless of the orientations of the members (see Table B-5 of Appendix B). In such a case the negatives of the pinned-end actions may be taken as equivalent joint loads acting in the directions of structural axes, and the analysis may be carried out as usual from this point on. The drawback to this approach is the fact that the final member end-actions will not include the initial pinned-end actions AML in the directions of member axes. Thus, the only member end-actions AM that

![image 520](Matrix Analysis of Framed Structures_images/imageFile520.png)

are calculated are the axial forces in the members due to the equivalent joint loads. This limitation is not a serious disadvantage in the analysis of trusses, because their principal features relate to the effects of loads (actual or equivalent) at the joints.

Now consider again those structures for which the member loads have been resolved into components parallel to member axes. The task of incorporating the loads directly into the stiffness method ofanalysis will be facilitated if they are expressed in discrete form (that is, as concentrated forces and moments). Any distributed loadings also can be accommodated by integrating the formulas for AML due to concentrated forces. If this approach is followed, only a certain number of concentrated loads will be possible at any point on a member. For example, at a point t on a beam there may exist either a concentrated force An in the YM direction or a moment AI'2 in the ZM sense, as shown in Fig. 6-7a. Each of these loads will cause four fixed-end actions of the types indicated in the figure. 'Similarly, there are three possible concentrated loads at any point on a plane truss member (see Fig. 6-7b), and four possible pinned-end actions. The most general category of member (a space frame member) is illustrated in Fig. 6-7c. Six load components may exist at any point on such a member, causing twelve types of fixed-end actions, as shown in the figure.

If the loads on a member consist only of concentrated forces and moments as described above, there are several methods by which they may be incorporated directly into the analysis of a structure. The simplest approach is to assume that a joint exists at every point of loading on the member, and then to analyze the structure as if it were subjected to joint loads only. This method is suitable for structures with rigid joints but cannot be adapted easily to trusses; moreover, the loads must be structureoriented instead of member-oriented in this approach. The principal disadvantage of this method is that the number of joints in the structure may become excessive if there are loads on many members.

A second method consists of analyzing each loaded member as a separate structure, using the stiffness method of analysis, and then incorporating the results of each such subanalysis into the over-all analysis of the structure. For example, the restrained beam in Fig. 6-7a could be analyzed

- as a structure consisting of two members of lengths a and b, respectively, and having two degrees of freedom at the point of application of the loads. The fixed-end actions AML for the member i will be the reactions determined in the subanalysis of the beam considered as two members. This line of reasoning may be generalized to include any type of framed structure and any number of load points on a member.


A third approach to the problem involves the use of transfer matrices for fixed-end actions due to unit loads on the members. The relationships between end-actions and loads acting at one point on a member may be expressed by the following equation:

(6-3)

![image 521](Matrix Analysis of Framed Structures_images/imageFile521.png)

6.4 Loads Between Joints 385

(0)

(b)

In Eq. (6-3), ACi is a column vector of concentrated loads that may exist at any point f on the member i. For example, the beam pictured in Fig. 6-7a has the concentrated loads AI'J and AC2 associated with an arbitrary point f on the member. Thus, for this type of structure

(a)

The matrix AMLi in Eq. (6-3) consists of a column vector of fixed-end actions caused by the loads Al'i. For a beam, this vector is the following (see Fig. 6-7a):

(b)

The matrix TMLi is a transfer matrix for the actions AMLi at the ends of the restrained member i due to unit values of the actions At;. The elements of such a transfer matrix may be obtained from the formulas given in Table

![image 522](Matrix Analysis of Framed Structures_images/imageFile522.png)

B-1 of Appendix B, and for a beam the matrix will be the following 4 x 2 array (omitting the subscript i):

b2 6ab - -L:! (3a + b) La

ab2 b

- (2a - b) TML =

###### L2

U

(6-4) (/2 6ab

--(aL3 + 3b) L:! a2b a

L2 -(2bL2 - a)

The vector of member end-actions AML for a member with loads acting

- at several load points can be obtained by applying Eq. (6-4) for every such point and then summing the results. In addition, formulas for fixed-end actions AML due to distributed forces can be derived from the terms in the first column (TMLl) of TML' This is accomplished by replacing a and b with x and L - x and integrating the product of TMLi and the distributed-load functionj(x) over the length to which it is applied. That is,


AML =fTMLlf(x)dx (6-5)

Alternatively, these formulas can be drawn from sources such as Table B-1 in Appendix B.

Transfer matrices similar to Eq. (6-4) may be developed for all types of

framed structures. For a plane truss member subjected to loads as indicated in Fig. 6-7b, the transfer matrix TML for pinned-end actions will be of order

- 4 x 3, as follows:


b L 0 0

b

0

TML = L L (6-6)

a

L 0 0 0

a L L

Similarly, the transfer matrices for the other types of framed structures may be easily derived. Such transfer matrices may be incorporated into a computer program for the purpose of automatically calculating the actions AML at the ends of restrained members due to loads at a discrete number of points. Mter this is done, the calculation of equivalent joint loads and the remaining parts of the analysis proceed as before.

6.5 Automatic Dead Load Analysis. Because structures must carry their own weight, dead load analyses are of great interest to structural

![image 523](Matrix Analysis of Framed Structures_images/imageFile523.png)

6.6 Temperature Changes and Prestrains 387

engineers. Of course, the programs in this book will produce dead load analyses if the input data includes fixed-end actions due to the weights of individual members. Such load data becomes unwieldy for structures with many members, however, and a less tedious approach is desired. The programs can easily be modified to perform dead load analyses automatically for any type of framed structure. Moreover, the weight of the structure may be handled either separately or in combination with other loading systems.

If cross-sectional areas of members and unit weights of materials are included among the input data, the weights of individual members may be calculated by the computer. This task is especially straightforward for prismatic members. Next, the fixed-end actions AML are computed by predetermined formulas. For example, the actions at the ends of a prismatic member in a plane frame (see Fig. 4-30) due to its own weight w (per unit of length) are

wL

wL

AJJLl = T Cy

AJJU = TCi'

II'L

wL

(6-7)

AML5 = TCx

AML2 = TCx

lI'L2

IIL2

###### AJJL6 = - 12Cx

###### A.lfL3 = 12CX

Expressions similar to Eqs. (6-7) may be programmed for each type of framed structure. After these terms are generated and placed into the matrix AML, the calculation ofequivalentjoint loads and the remaining parts of the analysis proceed as before.

Uniformly distributed live loads applied to members may be treated in a manner similar to that for dead loading. For this purpose, an alternative form of input data is required for loads on members. Each data line must specify the member number, the direction of loading, the intensity of loading, and a code number indicating whether the intensity is for a unit of length along the member or along its projection on a reference plane. Formulas for fixedend actions due to the former type of loading are analogous to those for dead weight calculations. Fixed-end actions due to loads of the latter type are also easily determined. For example, if the loading on the plane frame member is defined to be of intensity w per unit of length along the x axis, the fixedend actions are obtained simply by multiplying the formulas in Eqs. (6-7) by the direction cosine ex of the member.

6.6 Temperature Changes and Prestrains. The effects of temperature changes and prestrains were considered in the hand solutions of Chapters 2 and 3. These effects may be readily incorporated into a computeroriented analysis by treating them in a manner analogous to the procedure

![image 524](Matrix Analysis of Framed Structures_images/imageFile524.png)

described in Chapter 4 (Sec. 4.5) for loads on members, that is, by replacing them with equivalent joint loads. Both temperature changes and prestrain effects will cause fixed-end actions in the members of a restrained structure. Formulas for fixed-end actions of this nature are listed in Tables B-2 and B-3 of Appendix B. Such end-actions may be handled in the same manner as those due to loads on members; in other words, they may be listed in matrices AMT and AMP, respectively, analogous to the listing of fixed-end actions due to loads in the matrix AML• Then the sum of all three effects can be combined into a single matrix AMC• Of course, in computer programming it may be desirable to place all terms directly into the matrix A MC, without the necessity of forming separately the matrices A ML, A MT, and AMP. Following this step, the fixed-end actions in the matrix A MC are converted to equivalent joint loads, and the analysis proceeds as described in Chapters 4 and 5 from then on. All free joint displacements DF, reactions A R, and member end-actions AM are calculated in exactly the same manner as for the case of loads only.

6.7 Support Displacements. Support displacements consist of known translations or rotations of support restraints. Two alternative methods will be described for including the effects of support displacements in the stiffness method of analysis.

The first approach requires the calculation of the actions at the ends of members in the restrained structure due to the displacements of the supports. (This technique was used in Chapter 3 for support displacements and discussed in Sec. 6.6 for temperature and prestrain effects.) These fixedend actions are then placed into the matrix AMR (or AMd and treated in the same manner as those due to loads. The conversion of these quantities to equivalent joint loads and the subsequent analysis then proceed as described in Chapter 4. The advantage of treating support displacements in this member-oriented fashion is that the analysis is cast into the same format as that for other secondary effects.

The second approach involves the generation of the over-all stiffness matrix 8) appearing in Eq. (3-31) of Chapter 3, which is repeated below.

AJ = SJDJ

(3-31) repeated

The expanded form of this equation is

- (3-33)

repeated

- (3-34a)


Writing Eq. (3-33) as two matrix equations produces

AF = SFFDF + SFRDR

repeated

and

(3-34b) repeated

![image 525](Matrix Analysis of Framed Structures_images/imageFile525.png)

6.8 Oblique Supports 389

Equation (3-34a) may be solved (symbolically) for the free joint displacements

(3-35) repeated

In this expression it is clearly seen that the second term in the parentheses represents equivalent joint loads corresponding to DF due to the support displacements DR' Furthermore, the last term in Eq. (3-34b) produces the influence of support displacements upon support reactions.

Both of the methods described above for calculating the effects of support displacements may be readily incorporated into a computer program. However, the member end-actions must be computed differently for these two approaches. In the former method the initial member end-actions AMR contain the effects of support displacements. Therefore, only the influence of free joint displacements is utilized in the augmenting terms AMD (see Eq.

- 5-5b). In the latter method the initial member end-actions are zero, and the effects of both free displacements and support displacements must be included in the augmenting terms.


6.8 Oblique Supports. The restraint list code used in the computer programs of Chapter 5 will account for the presence or absence of restraints in directions parallel to the structural axes x, y, and z. Thus, for example, a roller support parallel to one of the structural axes can be taken into account. The code, however, will not accommodate oblique roller supports such as those indicated in Fig. 6-8a for a plane truss and Fig. 6-8c for a plane frame. There are several methods by which such support conditions may be included in the analysis of structures by the stiffness method. One possible approach is to rotate the structural axes so that the reference planes are either parallel or perpendicular to the inclined planes. This technique is limited to those cases in which there is only one oblique support or in which all inclines are mutually orthogonal. In those cases where this method is applicable, however, it is likely that the joint coordinates and the orientations of members and loads with respect to the structural axes will become more complicated.

Another method of handling the problem is to replace the actual support by a member having a large cross-sectional area Ax and having its longitudinal axis in the direction normal to the inclined support. Such a substitution is indicated in Fig. 6-8b for the support shown in Fig. 6-8a. A similar substitution is also indicated in Fig. 6-8d for the frame support of Fig. 6-8c. In this latter case the cross-sectional area Ax must be made large and the moment of inertia lz must be set equal to zero. Since the cross-sectional areas of the substitute members are large compared to those of the other members of the structure, their axial changes of length will be negligible in the over-all analysis. Therefore, such members will create essentially the same effects as the rollers on the inclined planes. Also, the axial forces in the substitute members will be approximately the same as the reactions of the roller supports. The length of a substitute member should be at least

![image 526](Matrix Analysis of Framed Structures_images/imageFile526.png)

(0 )

###### z

(d)

- Fig. 6-8. Oblique supports.


the same order of magnitude as the other members in the structure in order to insure that the angle of rotation of the member is small. The advantage of this method of handling supports is that the addition of one or two extra members and joints does not require any changes in the programs of Chapter 5.

A third approach to the problem of oblique supports requires a modification of the method for writing action equations in the stiffness method. These equations represent summations of forces and moments in the directions of the structural axes. However, at an oblique support the suitable directions are parallel and perpendicular to the inclined plane. Therefore, the over-all formulation of the action equations for the structure should include some equations that are written for restraint-oriented axes instead of structure-oriented axes. A set of restraint-oriented axes XR, YR, and ZR is shown in Fig. 6-8c in conjunction with the oblique support. Actions and displacements at an oblique support may be transformed from structural axes to restraint axes (or vice versa) using the type of rotation matrix R described

![image 527](Matrix Analysis of Framed Structures_images/imageFile527.png)

6.9 Elastic Supports 391

in Chapter 4. In this case the matrix R will consist of the direction cosines of the restraint axes with respect to the structural axes. Moreover, the overall joint stiffness matrix SJ may be generated with respect to structural axes as before, and then the rows and columns associated with the oblique supports may be altered by operations on the matrix using an appropriate rotation transformation matrix RR' The matrix RR contains as submatrices on the principal diagonal either the identity matrix or the rotation matrix R, the latter appearing in those positions that correspond to the oblique supports. The required operations may be represented symbolically by premultiplying the over-all action equation (Eq. 3-31 before rearrangement) by the matrix RR and inserting I = R;'RR = R~RR before DJ, as follows:

(6-8)

Equation (6-8) represents in general a change ofcoordinates, and quantities in the new coordinate system may be identified with an asterisk and defined as follows:

RRAJ = Af RRSJR~ = sf

- (6-9a) (6-9b) (6-9c)
- (6-10)


RRDJ = Df

When Eq. (6-8) is rewritten in these terms, it becomes

Af = SfDf

which has the same form as Eq. (3-31). The solution for displacements and reactions in the new coordinate system may now be carried out as before, but the computation of member end-actions requires that Df be transformed back to the original coordinates, using Eq. (6-9c). Thus,

(6-11)

Among the three methods described above for handling oblique supports, the approach using substitute members is the most convenient because it requires no changes in the programs of Chapter 5. Although the method involving rotation of axes is mathematically more elegant, its application requires an increase in the amount of programming effort.

6.9 Elastic Supports. Cases of support restraint conditions may exist that are intermediate between the extremes of zero restraint and full restraint. If such restraints against either translations or rotations are linearly elastic, they may be included easily within the scope of the stiffness method of analysis.

In order to illustrate conditions of elastic support, consider the continuous beam shown in Fig. 6-9. A comparison of this figure with Fig. 4-7a in

![image 528](Matrix Analysis of Framed Structures_images/imageFile528.png)

392 Chapter 6 Additional Topics for the Stiffness Method

z

- Fig. 6-9. Beam with elastic supports.


Sec. 4.8 shows that full restraints and zero restraints at every joint have been replaced by elastic springs having stiffness constants denoted by the symbol SR' The odd-numbered stiffnesses are restraints against translations in the y direction, and the even-numbered stiffnesses are restraints against rotations

- in the z sense. Iftwo springs exist at every joint, and if there are mmembers in the beam, there will be 2(m + 1) elastic restraints, and the analysis of the structure by the stiffness method will involve that number of degrees of freedom. The restrained structure for the beam in Fig. 6-9 will be the same as before (see Fig. 4-7b), but the joint stiffness matrix will be altered because of the restraint stiffnesses SR' If these restraint stiffnesses are added to the diagonal elements of the over-all joint stiffness matrix SJ' the resulting matrix can then be used in the solution for joint displacements as in Sec. 4.8. Member end-actions may also be computed as described in that section. On the other hand, the reactions at the elastic supports will be equal to the actions in the elastic springs and may be calculated as the negatives of the products ofthe spring constants times the joint displacements. Thus,


(6-12)

Although a beam serves as an example in the preceding discussion, this method of handling elastic supports is applicable to all types of framed structures.

An alternative approach to the problem of elastic supports is to substitute equivalent structural members for the restraints. As an example ofthis technique, consider the problem of handling the joint j of the plane truss shown in Fig. 6-lOa. The joint is restrained by two translational springs having stiffnesses (SR)2j-l and (SRhj. The two springs can be replaced by the two additional truss members 1 and 2 shown in Fig. 6-lOb. These members can be assigned arbitrary lengths Ll and L2 (comparable to the lengths of the other members in the truss) and cross-sectional areas AX! and A X2, computed as follows:

![image 529](Matrix Analysis of Framed Structures_images/imageFile529.png)

6.9 Elastic Supports 393

![image 530](Matrix Analysis of Framed Structures_images/imageFile530.png)

![image 531](Matrix Analysis of Framed Structures_images/imageFile531.png)

###### }--.

y

(a) (b)

z

![image 532](Matrix Analysis of Framed Structures_images/imageFile532.png)

![image 533](Matrix Analysis of Framed Structures_images/imageFile533.png)

Fig. 6-10. Substitution of members.

The assignment of these cross-sectional areas gives the substitute members axial stiffnesses equal to those of the elastic restraints they replace.

A similar example is illustrated in Figs. 6-lOc and 6-lOd, which show a jointj in a plane frame. The substitution of members 1 and 2 for the translational restraints (see Fig. 6-lOd) is similar to that for the plane truss example, except that the moments of inertia of these members must be set equal to zero. A suitable substitution for the rotational restraint of stiffness (S R)aj consists ofa torsion bar, denoted as member 3 in Fig. 6-lOd, parallel to the z axis (and hence perpendicular to the plane of the frame). This member would be assigned an arbitrary length L3 and a torsion constant I X3, computed as follows:

The difficulty arising in this example is that the plane frame is converted into a space frame by the addition of member 3, and the analysis of the structure must proceed on that basis. Thus, it is seen that there will be some cases in which the replacement method is disadvantageous compared to the first method discussed above, which involves augmenting the joint stiffness matrix directly.

![image 534](Matrix Analysis of Framed Structures_images/imageFile534.png)

394 Chapter 6 Additional Topics for the Stiffness Method

6.10 Translation of Axes. In Chapter 4 the concept of rotation of axes was found to be of great practical value for handling actions and displacements in members that are skewed in space. Similarly, the concept of translation of axes will be useful in later sections of this chapter. By this technique it will be possible to transform a set of actions or displacements from one point to another for parallel sets of axes.

Figure 6-11a shows a force vector Pq and a moment Mq at point q and their static equivalents (Pp and Mp) at point p. The actions at p may be computed from those at q by the following expressions:

Pp = Pq (a) Mp = rpq x Pq + Mq (b)

![image 535](Matrix Analysis of Framed Structures_images/imageFile535.png)

Yp Yq

~~----------- Xq

101

1 1

Zq IYPII

1

~~----------------------~I~---------------~

1 //

1 /ZplI

1/

----------- ----- -~

XplI

(0)

![image 536](Matrix Analysis of Framed Structures_images/imageFile536.png)

###### Yp Yq

Rigid bOdY~ ____ - -

./ ./ 88q

./

###### \

~~--~l------- xll

,,01

###### I

###### I YPII /

1 /

~~----------------------+,~r-~-----------~

###### \ _ - - _ _ _ -r "Z

p /

__ -- - 1// PI/

###### ___ ________ ____ _ --Y

(b)

###### Fig. 6-11 . Translation of axes: (a) actions and (b) displacements.

![image 537](Matrix Analysis of Framed Structures_images/imageFile537.png)

6.10 Translation of Axes 395

As seen in the figure, rpq is the location vector from p to q, and its components in the x, y, and z directions are xpq' Ypq' and ZfJQ' The matrix operation that is equivalent to Eqs. (a) and (b) takes the form

###### Ap=TpqAq=[~3pq ~J[~:] (6-13)

In this equation the operator Tpq contains a 3 x 3 submatrix Cpq in the lower left-hand position, which consists of the components of r pq arranged in a pattern for generating the vector product (or cross product) in Eq. (b). For this purpose, the following skew-symmetric submatrix is required:

###### 0 Zpq Y1'q]

[

(6-14)

CjJQ = Zpq 0 - Xpq

-Ypq Xpq 0

The other submatrices in TJUI are a 3 x 3 identity matrix 13 (appearing twice) and a 3 x 3 null matrix. Furthermore, the action vectors Ap and Aq in Eq. (6-13) contain the six components of actions in the x, y, and z directions at points p and q, as follows:

Ap = {Api, A p2 , ... , Aps} A'I = {A'ilo A q2 • •••• A q6}

- (c)
- (d)


The first three terms in Ap are the x, y, and z components of the force Pp; the next three terms in Ap are the x, y, and z components of the moment Mp; and similarly for AQ•

Equation (6-13) may be used in analysis whenever static equivalents are required. The operator T})q transforms a set of component actions Aq at point q into a parallel set Ap at point p, and it is called a translation-ofaxes transformation matrix. The reverse tfansformation (from p to q) is

A - T-'A - [13 0] [ Pp ] (6-15)

q - pQ P - Cqp 13 Mp

in which

C(lJJ = -Cj}q (6-16)

Thus, the inverse of T IJ(I is easily obtained by merely reversing the signs in the submatrix CIJ(I'

Kinematic relationships between the displacements of two different points on a rigid body can also be expressed in operator form. Figure 6-11 b shows points p and q on the same rigid body, which is subjected to a set of small displacements. These rigid-body displacements are represented at point p by the translation vector Sup and the rotation vector 881" while their kinematic equivalents at point q are labeled Su" and 88 q. The displacements at q may be computed from those at p by the relationships

5uq = 5up + 59p x rpq 59q = 59p

(e)

###### (D

![image 538](Matrix Analysis of Framed Structures_images/imageFile538.png)

396 Chapter 6 Additional Topics for the Stiffness Method

In Eq. (e) the cross product can be rewritten as

###### bOp X rpq = -rpq X 09p = rqp X bOp (g)

Then the matrix operation that is equivalent to Eqs. (e) and (f) becomes

Dq= TJqDp=[~ ctqJ [~::J (6-17)

in which

0,.~ -OM~Ow~[

0 Zpq

###### -y ]

"pq 0 X~: (6-18)

ypq -Xpq

Here it is seen that transposition of cpq changes its sign, which is an inherent property of a skew-symmetric matrix.

The kinematically equivalent displacement vectors Dp and Dq in Eq. (6-17) each contain three components oftranslation and three of rotation in the x, y, and z directions at points p and q, respectively. In this case the transposed operator TEq converts a set of component displacements Dp at point p into a parallel set Dq at point q, assuming that there is no relative displacement of the points. The reverse transformation is

Dp=T;JDq=[~ tJ U::J (6-19)

Thus, the calculation of displacements at p in terms of those at q involves the transposed inverse of the operator used for obtaining actions at p from those at q (see Eq. 6-13).

6.11 Member Stiffnesses and Fixed-End Actions from Flexibilities.

Most of the remaining sections in this chapter deal with member characteristics that alter the stiffnesses and fixed-end actions for individual members. Ifthe two matrices SM i (see Sec. 4.3) and TMLi (see Sec. 6.4) are revised to account for nonprismatic shapes, shearing deformations, etc., the stiffness method ofanalysis will be otherwise unchanged. In many instances it is easier to derive these matrices from flexibility considerations than to use the direct stiffness approach. For this reason a technique that requires inversion of member flexibilities and translation-of-axes transformations will be described in this section. Such a procedure can then be applied as desired in subsequent sections to find SMi and TMLi for members with various characteristics.

Figure 6-12a shows a prismatic space frame member that is fixed at its

- j end and free at its k end. The 6 x 6 flexibility matrix F\I1'~' for this type of member was derived previously in Chapter 2 (see Eq. 2-23). Inversion of F\lkk produces the stiffness submatrix S.If~·h·' Thus,


###### (6-20)

![image 539](Matrix Analysis of Framed Structures_images/imageFile539.png)

(0)

(b)

###### YM

(c)

- Fig. 6-12. Space frame member.


As discussed in Sec. 4.3, the complete member stiffness matrix SM (omitting the sUbscript i) has the form

SMjk J

S _ [ S).'ljj :VI - S

(6-21)

SMkk _

:vI kj

After the 6 x 6 submatrix SilHk has been obtained by inversion, the other three 6 x 6 submatrices of S),] can be found by the type of axis transformations described in the preceding article.

Terms in the submatrices ofSM are restraint actions due to unit displace-

![image 540](Matrix Analysis of Framed Structures_images/imageFile540.png)

398 Chapter 6 Additional Topics for the Stiffness Method

ments, and in particular the terms in submatrix SMkk are defined as the restraint actions at the k end of the member due to unit displacements at the same end. Statically equivalent actions at the j end may be computed using the transformation matrix

o1 0 Ofo0:0 00 00

001:000

(6-22)

----------~---------

000:100

###### 00 -L:O 0

o L 0:00

I

This operator is obtained from Eq. (6-13) by replacing points p and q with points j and k and using member-oriented axes. Then terms in the submatrix SMJk can be computed as the static equilibrants (equal and opposite to equivalents) of those in SMkk, as follows:

(6-23) The terms in SMJk are the restraint actions at j due to unit displacements at

- k, and they are in equilibrium with the terms in SMkk' Because the member stiffness matrix SM is symmetric, the submatrix


SMkj must be equal to the transpose of SMJk. Thus,

(6-24) Terms in SMkJ consist of restraint actions at k due to unit displacements at

j.

The remaining submatrix SMJJ can be found from SMkJ by using an expression analogous to Eq. (6-23). That is,

(6-25)

The terms in SM» are restraint actions at j due to unit displacements at j, and they are in equilibrium with the terms in SMkJ'

In summary, Eqs. (6-23), (6-24), and (6-25) constitute the relationships for finding the other submatrices of SM after the submatrix SMkk has been found by inversion of FMkk• A formulation similar to the above may also be carried out by starting with the j end free and the k end fixed. In this approach the submatrix SMJJ is determined as the inverse of FMjjo and a transformation matrix TkJ is used to find the other submatrices of SM. The operator TkJ required for this purpose is the inverse of matrix Tjk and is obtained by merely changing the signs of the nonzero terms in the lower left-hand portion of Tjk•

Furthermore, the expressions developed above for a space frame member can be specialized to any other type of framed structure by removing appropriate rows and columns from the transformation operator. For example, a beam member involves only forces in the YM direction and

![image 541](Matrix Analysis of Framed Structures_images/imageFile541.png)

moments in the ZM sense. Therefore, only the second and sixth rows and columns of Tjk need be retained, as follows:

Tik =[i ~] (6-26)

Of course, the submatrices of SM for a beam member will all be of size 2 x 2 instead of 6 x 6.

It is also possible to develop expressions for the fixed-end actions in matrix TML (see Sec. 6.4) from member flexibilities and axis transformations. For this purpose, consider the fixed-end space frame member in Fig.

- 6-12b, which has six components of actions applied at an intermediate point C. They are


(a)

Due to these applied actions, six fixed-end actions will occur at each end of the member. At the j end the fixed-end actions are

(b)

and at the k end they are

AMLk = {AMLkt. A MLk2, •.. , A MLk6} (c)

When the fixed-end actions at j and k are distinguished in this manner, the matrix TML can be partitioned as follows:

TML = [ TMLi] (6-27)

TMLk

Formulas for the submatrices TMLj and TMLk will be derived separately in the ensuing discussion.

The fixed-end member in Fig. 6-12b is statically indeterminate to the sixth degree, and the flexibility method of Chapter 2 can be used to find six of the unknown actions. If the fixed-end actions AMLk at the k end are chosen as redundants, the released structure is as shown in Fig. 6-12c. Due to the applied loads on the released structure, the displacements at the load point are

(6-28)

In this expression the symbol Fat! represents a 6 x 6 flexibility matrix for the t end of the beam segment of length a. Whereas this segment deforms due to the loads, the other segment (of length b) displaces as a rigid body. Therefore, the displacements at k can be computed as

(6-29)

which is drawn from Eq. (6-17) in the preceding section. Substitution of Eq. (6-28) into Eq. (6-29) yields

(6-30)

![image 542](Matrix Analysis of Framed Structures_images/imageFile542.png)

400 Chapter 6 Additional Topics for the Stiffness Method

This vector of displacements corresponds to the redundants and is due to the loads on the released structure. Therefore, it is recognized to be DQL in the flexibility equation, which is

(2-9) repeated

Since the final displacements DQcorresponding to the redundants are zero, the solution for the fixed-end actions AMLk becomes

(6-31)

This formula is obtained from Eq. (2-9) by replacing Q, F-I, and DQ!_ with AMLk• S~Ikk' and Dk (from Eq. 6-30).

Similarly, a matrix formula for AMLj can be derived with the flexibility method by choosing the fixed-end actions atj as the redundants and releasing the j end instead of the k end. The resulting expression is

(6-32)

In this formula the symbol Fbtl represents a 6 x 6 flexibility matrix for the t end of the beam segment of length h; and the operator T;~ transforms displacements from t to j. Since the coefficients of At in Eqs. (6-31) and

- (6-32) are TMLk and TMLh they can be placed into Eq. (6-27) to produce (6-33)

From principles of static equilibrium, the following relationships can also be written:

- (6-34a) and
- (6-34b)


The coefficients of At in the latter form of these expressions are seen to be TMU and TMLk' Thus,

- (6-35a) and
- (6-35b) which give TMLj and TMLk in terms of each other.


In summary, terms in the matrix TML can be obtained from member flexibilities and axis transformations by evaluating the formulas in Eq.

- (6-33). However, only one of the submatrices in Eq. (6-33) need be evaluated because the other can be found from equilibrium principles using either Eq. (6-35a) or Eq. (6-35b). This procedure can be applied to the members ofany type offramed structure and is illustrated by the following beam example.


![image 543](Matrix Analysis of Framed Structures_images/imageFile543.png)

6.11 Member Stiffnesses and Fixed-End Actions from Flexibilities 401

Example. Figure 6-13a shows a restrained prismatic beam member with actions All (y force) and AI2 (z moment) applied at point f. The submatrices of SM and TML for this example will be found using member f1exibilities and axis transformations. For the released structure in Fig. 6-13b, the f1exibilities are

###### L [2U

###### FMkk = 6El 3L

Inversion of this matrix in accordance with Eq. (6-20) gives

###### _ -1 _ 2El[ 6

S'lkk - FMkk - U -3L -3L]

###### 2U

From Eq. (6-23) the static equilibrants at} are

###### 0] 2El[ -6 1 SMkk = U -3L

By transposition (see Eq. 6-24),

###### S -- Sr __ 2El[ -6

###### -3L]u

'lkj - 'Uk - U 3L

(a)

(b)

- Fig. 6-13. Beam example.


![image 544](Matrix Analysis of Framed Structures_images/imageFile544.png)

402 Chapter 6 Additional Topics for the Stiffness Method Then Eq. (6-25) produces the equilibrants at} as

SMii= -TikSMki= - [1 ~J SMki = 2ft[3~ 2L23LJ

All of the terms in these stiffness submatrices are familiar expressions.

The less familiar submatrices of TML will be obtained by working with the released structure in Fig. 6-13b. For unit values of A/I and A12, the flexibility matrix of the segment jl is

###### a [2a2 3a]

###### Fatt= 6EI 3a 6

and the transfonnation matrix for displacements at k due to unit displacements at t is

Tlk = [~ ~]

Therefore, the submatrix TMLk in Eq. (6-33) becomes

_ T _J...[-a2(a+3b) TMLk - -SMkkT{kFatt- VI a2bL

-6ab ] aL(2b - a)

Then the submatrix TMLi can be determined from equilibrium considerations (Eq. 6-35a), as follows:

TMLj = -TjkTMLk- Tjt= - [1 ~] TMLk - [~ ~]

1 [-b2(3a + b) 6ab]

= V -ab2L bL(2a - b)

The submatrices of TML found above are the same as those given previously in Eq.

(6-4).

6.12 Nonprismatic Members. Members that do not have the same cross-sectional properties from one end to the other are called nonprismatic members. Examples are tapered members and members having reinforcements over parts of their lengths. In addition, any member that does not have a straight axis is nonprismatic. The topic of curved members is covered in Sec. 6.13, and only nonprismatic members with straight axes are discussed in this section.

One feasible approach for analyzing a structure with nonprismatic members consists of assuming joints at intermediate points along the length of each nonprismatic member. A segment between two such joints may be approximated as a prismatic member (if it is not already prismatic) having section properties obtained by averaging those at the two ends of the segment. This approach will cause the joint stiffness matrix to become very large, but it does not require any changes in the computer programs of Chapter 5.

However, a more desirable approach consists of evaluating flexibilities for the nonprismatic member and then obtaining stiffnesses and fixed-end

![image 545](Matrix Analysis of Framed Structures_images/imageFile545.png)

6.12 Nonprismatic Members 403

actions by the method described in the preceding section. The unit-load method in Appendix A provides a means of calculating ftexibilities by direct integration, assuming that the variations in cross-sectional properties are expressed as continuous functions. Otherwise, the ftexibilities can be obtained through an appropriate numerical integration procedure.

As an example, consider the tapered beam member shown in Fig. 6-14a. It will be assumed that this beam has a rectangular cross section of constant thickness t and that its height varies linearly from hi at the j end to hk at the k end. The j end of the member is fixed in preparation for calculating flexibilities at the k end. Also shown in the figure is an origin at point O. where the depth of the imaginary portion of the beam (shown by dashed lines) is zero. From this origin the auxiliary variable Xl is measured and will be used for convenient integration. Figures 6-14b and 6-14c consist of moment diagrams MU1 and M(72 due to unit values of the actions Ak1 and A k2, respectively. These diagrams may be used to obtain the member flexibilities at the k end by the unit-load method. Thus, Eq. (A-31) in Appendix A-2 gives (for flexural deformations only)

(a)

In this equation the terms are

hkL

L1 = --"--

(b)

hi - 17k

(a)

###### L~~-

(+)

###### j k j k

(b) (c)

###### Fig. 6·14. Tapered beam member.

![image 546](Matrix Analysis of Framed Structures_images/imageFile546.png)

404 Chapter 6 Additional Topics for the Stiffness Method

If hj = 2hk , the terms in expressions (b) simplify to

(c)

Substitution of expressions (c) into (a) produces

12V J2L (Xl - L)2

- (d)
- (e)
- (f)
- (g)


(FMkk)11 = th'kE L xt dXI

Intregration yields

12V( 5)

(FMkk)n = th'kE ,In 2 - "8 Similarly,

and

2LMt2 9L

J

(FMkkb = L Elz dXI = 2th'kE

From this point the member stiffness matrix SM and the transfer matrix TML can be obtained as described in the preceding section.

Consider now a nonprismatic member composed of segments, each of which may be either prismatic or nonprismatic, as indicated in Figs. 6-15a and b. Assume that flexibilities, stiffnesses, and fixed-end actions for each segment have already been calculated in the manner described above. Two methods will be discussed for obtaining the matrices SM and TML for this type of member. The first approach utilizes segment flexibilities and translation-of-axes transformations, whereas the second approach involves segment stiffnesses.

In the flexibility approach, let the j end of the segmented member be fixed (see Fig. 6-15a) and examine the influence of loads at the k end. Actions At at point t that are statically equivalent to actions Ak at k are (from Eq. 6-13):

(6-36)

Due to these actions, incremental displacements ADt at pointt. relative to those at point t - 1, become

(6-37)

where Fs{( represents the flexibility matrix of the t end of the segment of length s. Substitute Eq. (6-36) into Eq. (6-37) to obtain

(6-38)

![image 547](Matrix Analysis of Framed Structures_images/imageFile547.png)

6.12 Nonprismatic Members 405

/ tt--E_::::_~_:;:;E_=_="~~-1EL~®~~'l::;;;;,;E;;1:~~=b:::::Q~~]:::I~k-)(M

## ZMIf----:-L----.j:1

(a)

YM

if!

Restrained joints

~~,

I Free joints

###### t ® t t

i 1 )(M

###### /1. LSQ-JL .1

(b)

Fig. 6-15. Segmented member: (a) flexibility approach and (b) stiffness approach.

Then calculate the incremental displacements at point k as (see Eq. 6-17)

- (6-39)
- (6-40)


LlDk = TlkLlD{

Substitution of Eq. (6-38) into Eq. (6-39) gives

LlDk = TlkFsaTtkAk

This expression represents incremental displacements at k caused by actions Ak associated with the flexibilities of segment t only. By superposition of the contributions of all segments, the total effect 'It k is

###### II,

(6-41) in which n, is the number of segments. Hence,

ns

(6-42)

![image 548](Matrix Analysis of Framed Structures_images/imageFile548.png)

406 Chapter 6 Additional Topics for the Stiffness Method

From this point the inversion of FMkk to obtain SMkb and so on, is the same

- as in the preceding section. Similarly, expressions for the transfer matrix TML can also be derived

by the flexibility approach, as demonstrated previously for a prismatic member. Equation (6-33) provides the necessary formulas, but in this case the flexibility matrices Faft and Fbtl must be obtained by summation of terms from contributing segments to the left and to the right of point t (see Fig. 6-15a). Furthermore, there is a different matrix TMLtfor each point of interest, such that

(t = 1,2, ... , ns - 1) (6-43)

Thus, the transfer matrix TML for a point where two segments are joined is somewhat different from the one discussed in Sec. 6.4, which was for fixedend actions due to unit actions applied at any point on the axis of a member.

The stiffness approach will be developed using Fig. 6-15b, which shows the segmented member fixed at both ends. At each point where segments are joined there will be free displacements DF/(t= 1,2, ... , ns - 1), and

- at ends j and k there will be restrained displacements DR. The action-displacement relationships for this structure (see Eq. 3-33) can be written in rearranged and partitioned form, as follows:


- (3-33)

repeated

- (3-34a)


Performing the indicated multiplications gives

repeated

and

(3-34b) repeated

Solving for DF in the first equation results in

(3-35) repeated

Then substituting this expression for DF into Eq. (3-34b) and rearranging terms yields

(6-44)

The right-hand side of Eq. (6-44) contains the actions of type R minus a term involving the effect ofactions oftype F. If the displacements DR are

![image 549](Matrix Analysis of Framed Structures_images/imageFile549.png)

6.12 Nonprismatic Members 407 all equal to zero (fixed-end member), Eq. (6-44) gives the following relation between the actions of types Rand F:

(6-45)

Therefore, the transfer matrix TML for fixed-end actions of type R due to unit actions of type F is

(6-46)

On the other hand, if all actions of type F are set equal to zero, Eq. (6-44) becomes

(6-47)

Because actions AR and displacements DR are corresponding, the expression in the parentheses in Eq. (6-47) is seen to be the stiffness matrix for unit displacements of the ends of the segmented member. Thus,

- (6-48) Substitution of Eq. (6-46) into the last term of Eq. (6-48) yields
- (6-49)


In summary, the member stiffness matrix SM and the transfer matrix TML for a segmented member may be obtained using previous concepts applied to a single member. By this approach the over-all joint stiffness matrix is formed as shown in Eq. (3-33), giving the matrices SFF, SFR, SRF, and SRR' Inversion of SFF and substitution of the appropriate matrices into Eqs. (6-46) and (6-49) produce the transfer matrix TML and the stiffness matrix SM for the segmented member.

The process of eliminating one or more matrices by partial solution of

the problem (as was done in deriving Eq. 6-44) is sometimes referred to as matrix condensation. Thus, the matrices SM and T~IL for the segmented nonprismatic member represent combinations of other matrices obtained by a condensation procedure. In this case the matrix T~IL pertains to all the points where segments are joined. It is also possible to make a more refined analysis, in which the displacements DF{are eliminated one joint at a time.

Example. Assume that the two-segment beam member in Figs. 6-16a and b has the following properties:

Determine stiffnesses and fixed-end actions for this segmented member by the flexibility and stiffness approaches described above.

###### FSl1=6~1[~f ~L]=2Fs22 Tlk=[l ~] T2k=[6 n

For the flexibility approach, the following matrices are needed:

![image 550](Matrix Analysis of Framed Structures_images/imageFile550.png)

408 Chapter 6 Additional Topics for the Stiffness Method

###### YM

£tA21 @ fkl

CD

~

.1 elk xM

7 ElZ2 7

E/z,

A22 An

###### "' L, .. E L2 ~

(a)

tAR3

tAR1

®

£tAF1

CD

###### ;I .1 ~~k XM

7 7

###### /. AR2 AF2 AR4

###### zM

(b)

- Fig. 6-16. Nonprismatic beam: (a) flexibility approach and (b) stiffness approach. From Eq. (6-42), the f1exibilities ofthe k end are


n., L [14L2 9 6

LJ

L [2L2 3L]

FMkk = I; (TXFS/'fT11<) = 6£1

+ 12EI 3L 6

1=1 9L

###### = ~ [IOL2 76LJ

###### 4EI 7L

Inversion of this matrix yields

###### -7LJ

SF-I 4EI [ 6

Mkk = Mkk = lIL3 -7L

###### IOU

From Eq. (6-33) the fixed-end actions TMLkI at the k end due to unit actions at point f become

TMUI' = -SMkkTIF,,~,

###### -12J

= -SMkk[ ~ LJ[2U 3LJ L 2 [-9L

1 3L 6 6EI = 33L 5U

3L

![image 551](Matrix Analysis of Framed Structures_images/imageFile551.png)

6.13 Curved Members 409

For the stiffness approach, the segment stiffnesses needed are drawn from Table 4-2. From these terms the rearranged and partitioned stiffness matrix for the segmented beam is formed. Thus,

36 6L :-12 -6L -24 IlL 6L 12U: 6L 2U -12L 4U

EJ ='-12------"6£--+--12----6£-----0------6--

[~::. ~;;:] L" -6L 2£2 6L 4L2 0 0

- 24 - 12L 0 0 24 - 12L

###### IlL 4U 0 0 -IlL 8£2

Substitution of the appropriate submatrices from this matrix into Eqs. (6-46) and (6-49) produces the transfer matrix TML and the member stiffness matrix SM for the nonprismatic member. as follows:

-15L 24]

T - _1_ _~]J,.2___JJ, _ TMU{

ML-33L -18L -24 -[T~ILh'{]

[

###### IOU 6L

6 5L i -6 7L ]

S = 4EI _21-____§£-:L-=:2£,____'!£-: = [SMjj M lIL3 -6 -5L: 6 -7L S~lkj

[

###### 7L 4U I -7L IOU

###### I

Observe that TMLkl' and SMkk are the same as those obtained by the flexibility approach.

6.13 Curved Members. In plane frames, grids, and space frames certain members may have axes that are curved in a plane or curved in space. Such members can always be divided into straight segments and treated in a manner similar to that for a straight segmented member, as described in the preceding section. However, for this purpose rotation-of-axes as well as translation-of-axes transformation matrices are required. In the present section flexibilities, stiffnesses, and fixed-end actions are discussed for circular members in plane frames and grids. These cases occur rather commonly, and the exact integrations are not difficult to perform.

Figure 6-17 shows a plane frame member i in the shape of a circular arc with its center at point C. The member lies in the x-y plane, and its crosssectional properties are assumed to be constant throughout its length. The j end is fixed, but the k end is free (in preparation for calculating flexibilities). Due to unit values of the actions Aklo A k2 , and Ak3 (two forces and a moment) the following bending moments exist in the member:

###### M('1 = -r(l - cos (J) MU2 = r sin (J MU3 = (al

In these expressions r is the radius of the member, and (J is the central angle measured from end k (see Fig. 6-17). The moments in expressions (a) can be used to determine the member flexibilities at the k end by the unitload method. Thus, Eq. (A-31) in Appendix A-2 gives (for flexural deformations only)

![image 552](Matrix Analysis of Framed Structures_images/imageFile552.png)

410 Chapter 6 Additional Topics for the Stiffness Method

![image 553](Matrix Analysis of Framed Structures_images/imageFile553.png)

/"------J{

/

.r

- Fig. 6-17. Circular member in a plane frame.


JMbl JeI> r2(1 - cos(j)2

###### (FMkk)U = -- ds = r de

###### E1z 0 E1z

= --r:l (3cp - 4 sin cp + sin cp cos cp)

(b)

2E1z

After other flexibilities of this nature are developed at the k end, the member flexibility matrix is found to be

r [r2(3CP - 4 sin cp + sin cp cos cp) - r2(2 - 2 cos cp - sin2 cp) FMkk = 2E1, r2(cp - sin cp cos cp)

Z Sym.

-2r(cp - sin CP)] 2r(1 - cos cp)

(6-50)

2cp

![image 554](Matrix Analysis of Framed Structures_images/imageFile554.png)

6.13 Curved Members 411

This matrix consists of displacements in the directions xMk. YMk. and ZMk due to unit values of Akb A k2, and A k3.

From the flexibilities listed above, the stiffnesses at the k end (in member directions) may be obtained through inversion as follows:

(6-20)

repeated

These stiffnesses can be transformed to structural directions by a rotationof-axes congruence transformation using the angle 'Yk' Thus,

(6-51)

in which

~] (6-52)

COS 'Yk sin 'Yk

Rk = - sino 'Yk cos0'Yk

[

Then the other parts of the member stiffness matrix (for structural axes) are obtained by the method of Sec. 6.11. That is,

(6-53)

where

###### Tik= [ ~ ~ ~]

(6-54)

-Yik Xjk 1

This translation-of-axes transformation matrix is found by taking the first, second, and sixth rows and columns of matrix Tpq in Eq. (6-13) and replacing p and q withj and k. Next, transposition gives

(6-55)

Finally,

(6-56)

These stiffness submatrices can be transformed to member directions, as follows:

(6-57)

in which

RT = [~j ~k ] (6-58)

In this operator the submatrix Rj is similar to Rk (see Eq. 6-52), but the angle 'Yj replaces 'Yk'

To determine expressions for fixed-end actions, the concepts in Sec.

![image 555](Matrix Analysis of Framed Structures_images/imageFile555.png)

412 Chapter 6 Additional Topics for the Stiffness Method

6.11 can again be used. However, in the present case it is also necessary to transfonn certain actions and displacements by rotation-of-axes techniques. Consider the actions Afl , An, and A('3 applied at point f in the directions XMf, YMf, and ZMf (see Fig. 6-17). When these actions are premultiplied by a flexibility matrix Fall" the displacements at f in the member directions are

(c)

The matrix Fallin this expression is similar to FMkk in Eq. (6-50), but the central angle cf> is replaced by cf>a (see Fig. 6-17). Rotation of axes to structural directions and translation of the results to point k gives

DSk = T~R;Dr = T~R;Fall'Ae (d)

In this expression the rotation matrix Rt is similar to Rk (see Eq. 6-52), but 'Y(replaces 'Yk. Also, the translational operator Ttk is similar to Tjk(see Eq. 6-54), but Xtk and Ytk replace Xjk and Yik. Then the flexibility equation (Eq. 2-9) can be applied to find the fixed-end actions at k, which are also transformed to member directions, as follows:

AMLk = - RkSMSkkDsk = - RkSMSkkT~R;FanAt (e) In this formulation the coefficient of Atis seen to be TMLk.

Similarly, a matrix formula for AMLi can be obtained from the flexibility method by choosing the fixed-end actions atj as the redundants and releasing the j end instead of the k end. This approach leads to

(f)

The matrix Fbll'in this expression is similar to FMkk in Eq. (6-50), but the central angle 1> is replaced by 1>b (see Fig. 6-17) and the signs for elements 1,2 and 2,3 are reversed. Also, the translational operator Tfj is similar to Tjh but Xfj and Yfj replace Xjk and Yjk. Because the coefficients of Ar in Eqs. (e) and (f) are TMLk and TMLj, they can be used in Eq. (6-27) to give

TML = [TMLi] = [-R,-SMSiiTliRiFbtt ] TMLk -RkSMskkTlrcRIFa({

(6-59)

Furthermore, principles of static equilibrium can be used to show that

- (6-60a) and
- (6-60b) which give TMLi and TMLk in terms of each other.


Consider now the grid type of structure, for which Fig. 6-18 shows a member i in the shape of a circular arc. Again, the member lies in the X-Y plane and has constant section properties. In this case, however, the

![image 556](Matrix Analysis of Framed Structures_images/imageFile556.png)

6.13 Curved Members 413

![image 557](Matrix Analysis of Framed Structures_images/imageFile557.png)

;-- --x

z

Fig. 6-18. Circular member in a grid.

actions Akl , A k2 , and Ak3 at the k end are two moments and a force. Due to unit values of these actions, the following bending moments and torques exist in the member:

MU2 = -cos 8 TU2 = sin 8

MUI = sin 8 Tu! = cos 8

###### MU3 = r sin 8 TU3 = -r(1 - cos 8) (g)

In this case Eq. (A-3l) in Appendix A-2 gives (due to flexural and torsional deformations):

(F fMh f nl f<l>sin28 f<l>cos28

###### Mkk)1I = -- ds + _. ds = -- r d8 + -- rd8

Ely Glx 0 Elv 0 Glx

= 2Elr.y (cf> - SIn cf> cos cf» + 2Glr.x (cf> + SIn cf> cos cf» (h)

![image 558](Matrix Analysis of Framed Structures_images/imageFile558.png)

414 Chapter 6 Additional Topics for the Stiffness Method

After other ftexibilities in FMkk are found, the matrix can be written as the sum offtexural and torsional terms, as follows:

(6-61) where

f/J - sin f/J cos f/J - sin2 f/J r(f/J - sin f/J cos f/J)J (FMkklflex = 2El f/J + sm f/J cos f/J -r sm f/J

\ r [ . . 2

Y Sym. y2(f/J - sin f/J cos f/J)

and (6-62a)

r [f/J + sin f/J cos f/J sin2 f/J r(f/J - 2 sin f/J + sin f/J cos f/J) ] (FMkk)tors = 2Gl f/J - sin f/J cos f/J - r(2 - 2 cos f/J - sin2 f/J)

x Sym. r2(3f/J - 4 sin f/J + sin f/J cos f/J

(6-62b)

Each of these arrays contains formulas for displacements in the directions XMk, YMk, and ZMk due to unit values of Akt. Ak2, and Aka.

The determination of stiffnesses for the circular grid member is accomplished in the same manner as that described earlier for the plane frame member. However, for the grid member the translation-of-axes transformation matrix TJk in Eq. (6-54) must be replaced by the following:

###### 1 0 Yjk] TJk = 01 -Xjk

(6-63)

[

o 0 1

This matrix may be obtained from Tpq in Eq. (6-13) by taking the fourth, fifth, and third rows and columns (corresponding to x moment, Ymoment, and Z force) in that order.

In addition, the matrix formulation of the fixed-end actions in TML for the circular grid member is symbolically the same as that for a plane frame member. In the case of the grid, however, the translational operators Tlk and TtJ are in the form of Eq. (6-63) instead of Eq. (6-54). Other comments made about the plane frame member apply also to the grid member, including the sign differences for terms in FaUand Fbtl.

6.14 Releases in Members. Figure 6-19 shows the types of partial discontinuities (or releases) that can exist in the members of framed structures. The symbols in Figs. 6-19a, b, c, and d denote the inability to transmit

----<o~--

(0) (b) (e) (d)

###### Fig. 6-19. Partial discontinuities.

![image 559](Matrix Analysis of Framed Structures_images/imageFile559.png)

6.14 Releases in Members 415

shear, moment, thrust, and torque, respectively. These inabilities to transmit actions result in translational or rotational displacement discontinuities. Combinations of these releases are also possible, and complete release takes the form of a free end. The general nature of a framed structure determines the types of releases that are important. In beams, for example, only shear and moment releases have significance. The member stiffness matrices and end-action transfer matrices for beams having such releases are presented in this section, and the concepts may be extended to the members of other types of structures as well.

Consider first the possibility of a shear or moment release at one end of a prismatic beam. Figures 6-20a and 6-20b show such conditions at a small distance from the j end of a restrained member, and Figs. 6-20c and 6-20d indicate the same conditions at the k end. The member stiffness matrices SM for these cases are easily obtained by analysis of the beams

YM

###### I 0 ('

/'~

---------,-+--------;;~ -XM

I

###### a A2(1.

---'-----l---b~ k

ZM : L

(0 )

###### tAl

###### ~ A2/

###### I

( b)

###### tAl

###### ~~--:+----~A2/I

(c)

###### tAl

~--------7_-----~

###### ~ A2/I

(d)

###### CD ('

###### ~I: A/;

a 2 , I.,

L

(e)

###### CD tAl

~

0

###### A2/

(tl

- Fig. 6-20. Discontinuities in a beam member.


![image 560](Matrix Analysis of Framed Structures_images/imageFile560.png)

416 Chapter 6 Additional Topics for the Stiffness Method

shown in the figure, and they are listed in Table 6-1 as matrices (a) through (d). Figures 6-20a through 6-20d also show actions Al and Az at the distance a from the j end of the member, and the transfer matrices TML for the resulting fixed-end actions are given in Table 6-2 as matrices (a) through (d). If the matrices 8M and TML shown in Tables 6-1 and 6-2 are used for a beam member having a shear or moment release at either end, the analysis may then proceed as before with no further modifications required.

Consider next the determination of the stiffness matrix 8M for a beam having a shear or moment release at an intermediate point. Figures 6-20e and 6-20f show such beams with the releases at the distance a from the j end of the member. One method of analyzing these beams consists oftreating them as two members by assuming a joint just to the left or right of the release. Then one of the submembers will have a release at one end (as in Figs. 6-20a through 6-20d), but the other submember will have no releases. This approach has the advantage that no new matrices are required other than those discussed above. Alternatively, the stiffness matrices for beams having releases at intermediate points always can be obtained directly from an elementary beam analysis. The results of such analyses for the beams in Figs. 6-20e and 6-20f are given in Table 6-1 as matrices (e) and (f).

Transfer matrices TML for fixed-end actions for beams with releases at intermediate points may also be found by the procedures mentioned above. If actions Al and Az are applied just to the left of the releases (see Figs. 6-20e and 6-20f), the transfer matrices have the form given in Table 6-2 as matrices (e) and (f). If the actions Al and Az are applied just to the right of the releases, the matrices are as given in Table 6-2 as matrices (g) and (h).

Table 6-1

Member Stiffness Matrices for Beams of Fig. 6-20

- 0 0

-f] 3E1,[ ~

0 -1

- 1 0 0 0 J]


El, [~

L 0 0 0 Vl -1 0 1

###### 0 -1 0 L 0 -L L2

1 0 U -Ln

(a) (b)

-fl 3EI,[ 1

L -1

###### EI, [~

0 0

L 0 0 0 VI -1 -L 1 0 -1 0 0 0 0

(c) (d)

###### EJ,[~

- 0 0

-~] [ I

a -1

- 1 0 3Elz a a2 -[J :b]


L 0 0 0 a3+ h'l -! -a 1 -h

###### 0 -1 0 ah -h h2

(e) (0

![image 561](Matrix Analysis of Framed Structures_images/imageFile561.png)

6.14 Releases in Members 417

Table 6-2

Transfer Matrices for Beams of Fig. 6-20

###### 0] [-b'(2L+al 3b(L+al]

2~[

0

b2 -2b I 0 0

2 - a2) -3b(L + a) beL + a) abL(L + a) L(P - 3(2)

-2L -2~1 2L'l -a(3L

(a) (b)

--..L -({(L + h) -2b 1 [--ahL(Lb(3L' -+b'lb) L(U3a(L+b)~- 3b2) 2L 0 -~({ 2£'1 - a

[ -2L OJ

2(2L 0+ b) -3a(L + b)

-a 2 0

(c) (d)

--..L -a(L + h) -2b 1 [ -2ab:-2b' l (/33a'_ 2b"] 2L 0 -~a 2(a" + b:l) -2a

[ -2L o1

3 - 3a2 -a2 2a:lb 3a2b

(e) (f)

###### 2~[

0

b2 -2ho ] 1 [ -2ab:-2b' l 3b'3ab2 ]

l + b3) -2a:l -3h 2 beL + a) 2a 3h -2a 3 + h"

-2L -~a 2(a:

(g) (h)

To understand how terms in Tables 6-1 and 6-2 can be derived, consider the member in Fig. 6-20f with a hinge at an intermediate location. The method of matrix condensation (see Sec. 6.12) may be applied to this problem to determine SM and TML' For that purpose, the joint stiffness matrix S) is formed, using individual stiffness matrices for submembers I and 2 (see Fig. 6-20f), as follows:

###### S.J = EI"

(a)

![image 562](Matrix Analysis of Framed Structures_images/imageFile562.png)

418 Chapter 6 Additional Topics for the Stiffness Method

In this matrix the contributions from member 1 are drawn from Table 4-2, but those for member 2 are given by matrix (b) in Table 6-1. Rearrangement and partitioning of Eq. (a) yields

I

12 3 6

I 12 6 3 3

###### -+-

I

a3 b3 a2 II a3 a2 b:l b2

###### I

6

6 2

4

I

###### I

---------------+------------------------ a2 -;;: a2 -;; 0 0

12 6

I I 12 6 I 0 0

a:l a2 I a:! a2

= [SFF SFR ]

I (b)

S,l = Ell:

I I 6 4 I 0 0

SRF SRR_ 6 2

###### a2 a II a2 a

I

3

I 3 3

0 0

0

I

b3 II b3 b2

I

3 I 3 3

0 0

I

0

I

###### b2

I b2 b

I

From this form the matrices TML and SM can be computed, using Eqs. (6-46) and (6-49) in Sec. 6.12, to produce the arrays labeled (f) in Tables 6-1 and 6-2.

Note that the transfer matrices (e) through (h) in Table 6-2 are for endactions at j and k due to unit actions applied adjacent to the releases. If actions are applied at other points along the length, suitable transfer matrices can be developed for cases in which XMI ~ a and XM2 ~ a. One way of obtaining these transfer matrices is to make use of the matrices given in Tables 6-2. For this purpose, a temporary restraint is imposed at a point adjacent to the release, and matrices (a) through (d) are used to compute the restraint actions at that point. The negatives of these restraint actions constitute equivalent loads adjacent to the release, and matrices (e) through (h) may be used to transfer the effects to the ends of the member.

Matrices similar to those in Tables 6-1 and 6-2 can be developed for the members of other types of framed structures, such as frames and grids. However, the topic is of lesser importance in trusses, because the ends of all members are assumed to be pinned; and any additional releases are unlikely.

It is interesting to note that certain releases in members may be taken into account by trivial changes in the analysis. For example, if a plane frame member has hinges at both ends, its member stiffness matrix will be the same

- as that for a plane truss member (expanded to size 6 X 6). Such a member may be handled in the computer program for a plane frame (Sec. 5.8) simply by setting its cross-sectional moment of inertia lz equal to zero. Such "tricks" can often be used to good advantage without resorting to additional programming.


![image 563](Matrix Analysis of Framed Structures_images/imageFile563.png)

6.15 Elastic Connections 419

6.15 Elastic Connections. Joints of framed structures are usually idealized to be either pinned or completely rigid. However, the connections themselves may have a significant degree of flexibility that could be important in the analysis. If such connections are assumed to be linearly elastic, they can be incorporated into the stiffness properties of the individual members as modifications of the idealized cases.

Several types of elastic connections are theoretically possible, according to the relative translations and rotations that can occur at the joints of a structure. Connections for shearing force, bending moment, thrust, and torque may all possess a certain amount offlexibility, but the most important of these is the rotational type that transmits bending moment. Such a connection is discussed in this section in conjunction with the analysis of beams. The ideas may, of course, be extended to other types of elastic connections and other types of framed structures.

Figure 6-21a shows a prismatic beam with a rotational elastic connection at a small distance from each end. Let SE be the stiffness constant for the elastic connection at each end of the member. A constant of this type is defined as the moment per unit relative rotation at the elastic connection. The stiffness constant SE will be incorporated into the stiffness matrix SM and the transfer matrix TML for the member. For convenience in writing these matrices, the following nondimensional parameters are defined:

Elz

(6-64)

e =--LSE

('1 = (' + 1 e4 = 4e + 1

e3 = 3e + 1

e2 = 2e + 1 e6 = 6e + 1

Terms in the modified member stiffness matrix SM can be obtained using the flexibility approach explained in Sec. 6.11. For this purpose the member is fixed at thej end and free at the k end, as shown in Figs. 6-21b through e. When a unit force is applied in the YM direction at the k end (Fig. 6-21b), the flexibilities at that end become

and

Similarly, a unit moment in the YM sense at the k end (Fig. 6-21c) produces

(c)

![image 564](Matrix Analysis of Framed Structures_images/imageFile564.png)

![image 565](Matrix Analysis of Framed Structures_images/imageFile565.png)

![image 566](Matrix Analysis of Framed Structures_images/imageFile566.png)

- (a)
- (b)


![image 567](Matrix Analysis of Framed Structures_images/imageFile567.png)

(el

![image 568](Matrix Analysis of Framed Structures_images/imageFile568.png)

(d)

![image 569](Matrix Analysis of Framed Structures_images/imageFile569.png)

SE'

~{! k

j ~~E'--=======-=1::";;-IL-------'---t-_-_-_-_----1

s£

(e)

Fig. 6-21. Beam with elastic connections.

and

L 2 L 2Le L L

F22 =- +- =- +-- =- (l + 2e) =- e2 (d)

Elz SE Elz Elz Elz E/z

![image 570](Matrix Analysis of Framed Structures_images/imageFile570.png)

- 6.15 Elastic Connections 421 Putting these terms into the flexibility matrix for the k end gives


###### F _ L [2L2e3

(6-65)

Mkk - 6EIz 3Le2

Inversion of this matrix yields

###### 2Elz [ 6e2

###### SMkk = L3e2ea - 3Le2 (6-66)

Then other submatrices of SM can be found using the translation-of-axes technique given in Sec. 6.11. Table 6-3 contains the resulting matrix, and the reader should compare this table with Table 4-2 in Chapter 4. Note that when SE is allowed to approach infinity (for a rigid connection), the constant e approaches zero, and the matrix in Table 6-3 becomes the same as the one in Table 4-2.

Formulas for the transfer matrix TML can also be derived in literal form. For this purpose, Fig. 6-21d shows a unit force (of type Af ,) applied in the YM direction at the intermediate point f. Similarly, Fig. 6-21e shows a unit moment (of type An) applied in the ZM sense at the same point. From these unit loads the flexibility matrix Fal'l', for the f end of the segment of length a, is found to be:

(6-67)

Comparison of these terms with those in Eq. (6-65) shows that L is replaced by a, and e2 is replaced bye, in position 2,2. (Thus, this matrix is of the same form as that for a beam with an elastic connection at the j end only.) From this point the parts of matrix TML can be obtained from the formulas in Eq. (6-33) of Sec. 6.11. Thus,

TML = [ TMLj ] = [ -=-SMjjTt~Fbtt]

(6-33)

TMLk SMkkT{kFutt

repeated In this expression the matrix FMe is similar to Fat(, but a is replaced by b and off-diagonal terms are negative. The resulting matrix T~'L appears in

Table 6-3 Member Stiffness Matrix for Beam with Elastic Connections

12 6: 12 6

L'l e2 L2 e2 : - L3 e2 L2 e2

6 4: 6 2

V e2 L e3 : - V e2 L

--------------+--------------12 6 I 12 6

- L3 e2 - L2 e2: L3 e2 - L2 e 2

I

6 2: 6 4

V e2 L : - V e2 L e3

![image 571](Matrix Analysis of Framed Structures_images/imageFile571.png)

Table 6-4, the parts of which are also related by equilibrium principles (see Eqs. 6-35a and b). When e is set equal to zero, elements in the table become the same as those in Eq. (6-4) for a beam with rigid joints (see Sec.

6.4).

Matrices similar to those in Tables 6-3 and 6-4 may also be derived for the case of unequal elastic connections at ends j and k of the beam and for the case of an elastic connection at only one end of the beam. In addition, other types of elastic connections and other types of structural members may be considered.

6.16 Shearing Deformations. In beams, frames, and grids the deformations of members due to shearing forces may be of significant magnitudes. If this is true, the effects of shearing deformations should be included in the analyses of such structures by making the appropriate modifications of the matrices SM and TML' The modified matrices for prismatic beams are presented in this section, and the changes made in the beam matrices may be easily extended to obtain the required changes in the matrices for frames and grids.

Elements of the modified stiffness matrix SM for a beam member with shearing deformations can be derived in the same manner as that used in the preceding section for a beam member with elastic connections. Toward this end, Fig. 6-22a shows a cantilevered member with a unit force in the YM direction applied at the k end. This force causes both flexural and shearing deformations in the member, as indicated in the figure. Thus, the translation

- at the k end may be written as


U fL

###### F =--+--

11 3Elz GAx (a)

where the first part is due to flexure and the second part is due to shear (see Appendix A). It is convenient to introduce a dimensionless shear constant g for the purpose of simplifying Eq. (a), as follows:

6fElz

(6-68)

###### g = GAxU

Table 6-4

Transfer Matrix for Beam with Elastic Connections

1

TMI.= 12('2(/b + (',L"-

![image 572](Matrix Analysis of Framed Structures_images/imageFile572.png)

- 6.16 Shearing Deformations


423

![image 573](Matrix Analysis of Framed Structures_images/imageFile573.png)

![image 574](Matrix Analysis of Framed Structures_images/imageFile574.png)

###### j~ pi

###### 1-. a~

(b)

- Fig. 6-22. Beam with shearing deformations.


Substitution of the form factor f(expressed in terms of g) into Eq. (a) gives

VI VI Ll ( g)

###### F11 = -- + --g = -- 1 + -

(b)

3EIz 6EIz 3EIz \ 2

Due to shearing deformations, there is no rotation of the cross section at k (only translation). Therefore, the flexibility F21 (see Fig. 6-22a) is caused only by flexure and has the value

###### U

(c)

F21 =--2EIz

By similar reasoning, a unit moment applied at k produces only flexural deformations; so the flexibility matrix becomes

###### L [2U(I +~)

(6-69)

FMkk =-- 2

6EIz 3L

Inversion of FMkk yields

###### s = 2EIz [6

(6-70)

Mkk L3(l + 2g) -3L

![image 575](Matrix Analysis of Framed Structures_images/imageFile575.png)

424 Chapter 6 Additional Topics for the Stiffness Method

Table 6-5

Member Stiffness Matrix for Beam with Shearing Deformations

12 6: 12 6

L3 L2 : - L:l L2

6 4 ( g): 6 2

###### U L 1 + 2" : - L2 L (l - g)

----------------+----------------12 6 12 6

###### -L2

###### L3

-2 (l - g)

6

###### U

L

Other parts of 8M are obtained as before, and the results are summarized in Table 6-5. Note that if the shear constant g is set equal to zero, the matrix in Table 6-5 becomes the same as that in Table 4-2.

The transfer matrix TML for a beam must also be modified for the effects of shearing deformations. This matrix can be developed using Fig. 6-22b, which shows the effect of a unit force (of type AI,) applied in the YM direction at an intermediate point t. Due to this force the translation at point tis the same as that given by Eq. (b), except that L is replaced by G. In fact, the flexibility matrix for the t end of the segment of length {/ is

###### Fa{(= 6;/ [2(/2 (1+~) 3(/]

(6-71)

z 3(1 6

which is analogous to Eq. (6-69). From this point the matrix TML can be obtained using Eq. (6-33), and the results are listed in Table 6-6. If the constant g is set equal to zero, the elements in Table 6-6 become equal to those in Eq. (6-4).

Thus, the effects of shearing deformations in beams may be taken into account in convenient fashion by using the modified matrices 8M and TML described in this section.

6.17 Offset Connections. In structures with rigid joints, the framing connections are often rather large in comparison with the lengths of the

Table 6-6

Transfer Matrix for Beam with Shearing Deformations

###### - U~ [3a + b + 2b(Llb)2g] ~b['l

a~ b

1 -""[;2 [I + (Llb)g] L2 (2a - b - 2gL)

###### TML =-- -----------------------------------------

1 + 2g a2 6,,/J

- V [a + 3b + 2a(Lla)2g] L'l

Va2b [l + (Lla)g] Ua (2b - II - 2gL)

![image 576](Matrix Analysis of Framed Structures_images/imageFile576.png)

members. Steel building frames designed against lateral loads tend to have large moment-resisting connections, and reinforced concrete frames with deep members usually contain joints that are correspondingly bulky. If the finite dimensions of joints are ignored, significant errors can arise in the analysis and design of framed structures. Therefore, a method for including their effects is given in this section under the heading of offset connections.

Another type of offset connection is encountered when the cross section of a member is not doubly symmetric. In such a case flexural and torsional deflections may be coupled because the shear-center axis [4] of the member does not coincide with the centroidal axis. Figure 6-23a shows a beam member with a channel-shaped cross section. Its shear-center axis through point 0 is eccentric with respect to its centroidal axis through point C. If the XM axis of the member is taken to be the shear-center axis, forces in the XMYM plane will cause the member to translate in the YM direction without twisting. However, if applied forces are eccentric with respect to the shearcenter axis, the cross section will deflect as indicated in Fig. 6-23b. In this figure it is assumed that the point 0 has translated in the negative YM direction an amount D" and the cross section has also rotated about the XM axis (shear-center axis) an amount D2• This type of coupling can be avoided if the joints between members are located at the intersections of shear-center axes and if applied forces intersect those axes. Otherwise, the problem of shear-center eccentricities may be handled under the heading of offset connections.

When joints of finite size or other types of offset connections are taken to be infinitely stiff, they may be treated as rigid bodies within the structure [5]. Under this assumption the actions, displacements, and stiffnesses at the ends of members framing into such joints must be transformed to specified working points on the rigid bodies. Figure 6-24 shows a space frame member with such offset connections at both ends. Points p and q on the rigid bodies are taken as working points to which information about joints j and k will be referred. First, any actions Aj and Ak at the ends of the member may be

C

ZM ----+-+1--' 0

(0 )

(b)

###### Fig. 6-23. Beam member with channel cross section.

![image 577](Matrix Analysis of Framed Structures_images/imageFile577.png)

426 Chapter 6 Additional Topics for the Stiffness Method

transfonned into statically equivalent actions AI' and Aq at the working points by the following generalized fonn of Eq. (6-13):

(6-72)

In the case of a space frame member, the vector Ai contains Ai), Aj2' ... , Aj6' as indicated by the joint displacement indexes at joint j in Fig. 6-24. In addition, the vectors Ab AI" and Aq consist of similar actions for the points k, p, and q in the figure. The translation-of-axes transfonnation matrices Tl'i and Tqk are both of the type given by Eq. (6-13) in Sec. 6.10. Equation (6-72) may be expressed more concisely as

- (6-73)
- (6-74)


in which

r5

tq2

,Iq --ql q4

/' q3 !k5

q6 T

k k2___

y

/1 kl k4

~k31

k6 1

###### I I

1

###### I

###### I

1

pI p4

1

I

I

r---~~r---------------------~~---.r------X

###### -----k::. I /

###### -------------~~~~~~------- 1 / /

- Fig. 6-24. Space frame member with offset connections.


![image 578](Matrix Analysis of Framed Structures_images/imageFile578.png)

and

###### T = [~j T~k ] (6-75)

The transformation matrix T is a combined operator that converts the actions in AMS into the statically equivalent actions in AMB for the rigid bodies. These actions are all in the directions of structural axes.

Displacements at joints j and k can also be expressed in terms of those at points p and q by an extended form of Eq. (6-17), as follows:

[ Dj ] - [T;~j 0 ] [ DpJ

(6-76)

D,.. - 0 TJk Dq

The displacement vectors in this equation correspond to the action vectors in Eq. (6-72). Equation (6-76) is expressed more succinctly as

- (6-77) in which,
- (6-78) and


TT = [~j T~J (6-79)

In addition, the member stiffness matrix S~IS can be transformed to the reference points p and q. For this purpose, consider the action-displacement relationships

AMS = SMsDMS Substitution ofEq. (6-77) for DMS gives

- (a)
- (b)
- (c)


Use of this expression in Eq. (6-73) produces

AMB = T SMS TTDMB Hence, the matrix relating AMB to DMB is

5MB = T SMsTT

(6-80)

In this expression 5MB is the member stiffness matrix for actions at points p and q due to unit displacements of those points.

The transformations represented by Eqs. (6-73), (6-77), and (6-80) apply equally well to all types of framed structures having offset connections. These expressions may be readily incorporated into the computer programs of Chapter 5 if desired. Of course, the transformations would be bypassed in cases where the dimensions of connections are small enough to be neglected.

![image 579](Matrix Analysis of Framed Structures_images/imageFile579.png)

428 Chapter 6 Additional Topics for the Stiffness Method

Example. A horizontal beam member within a rectangular plane frame (see Fig. 6-25) has offset connections at both ends. At the j end the offset distance is c. and at the k end the offset is d. For this example the translational operators are

###### T"j= [~, ~] Tqh' = [ld ~] (d)

Using these matrices in Eqs. (6-73), (6-77), and (6-80) produces

AXIll = TAMs = {A.l1st • cAJ/st + A J1s2• A ,usa. -dAMs:l + AMS'} DMS = TTDMB = {D.UBt + CDJfB2 • D,uB2. DMH3 - dDJ1B4• DMH4} 5MB = TSMSTT

- (e)
- (f)


6 3L + 6(' -6

3L + 6d ] V + 3Lc + 3Ld + 6cd

-V_ 2Elz 2V+ 6Lc + 6c2 -3L6-6c

[

-3L - 6£1 (g)

Sym. 2V + 6Ld + 6d2

6.18 Axial-Flexural Interactions. Throughout the earlier discussions in this book it was always assumed that there was no interaction between axial forces and bending moments in a structural member. This assumption is satisfactory in many ordinary situations; however, if the axial forces are large or if the member is slender, it may be necessary to make a more accurate analysis. Such an analysis must take into account the additional bending moments that are produced in a member by the axial forces when the member deflects laterally. This axial-flexural interaction, which is sometimes referred to as the beam-column effect or the P-!l. effect, results in changes in the member stiffness matrix SM and the transfer matrix TML'

Let us consider first the changes that are required in the member stiffness matrix SM for a beam member. Figure 6-26 shows a restrained beam that carries an axial compressive force P and is subjected to a unit translation and a unit rotation at the j end (figures showing similar displacements at the k end are omitted). The axial force may be either tension or compression, but compression is usually of greater interest than tension due to the possibility ofbuckling. Because ofthe lateral deflections ofthe beam, the bending

###### o

- Fig. 6-25. Beam member with finite joint sizes.


![image 580](Matrix Analysis of Framed Structures_images/imageFile580.png)

p ~--__ 0 t ~=1~~j__________~~=-__~ P

+SM31

5

/ ;- ---XM 5M41

M21

(0 )

(b)

- Fig. 6-26. Member stiffnesses for a beam subjected to an axial force.


moments are modified by the presence of the axial force. The corresponding modified terms in the member stiffness matrix SM are given in Table 6-7. Each term is expressed as the product of the stiffness without axial-flexural interaction (see Table 4-2) and a stiffness function s. The four stiffness functions are defined in Table 6-8 for axial forces that are compression, tension, and zero. All of the formulas given in this table can be derived by elementary beam analysis, considering the presence of the axial force.

To understand how the functions in Table 6-8 are obtained, consider the translation d = 1 at end j of the beam in Fig. 6-26a. At the distance x from that end, the moment in the beam is

###### d2v

###### M = Elz dx2 = P(d - v) + SMIIX - SM21 (a)

In this expression the symbol v denotes translation of the beam in the y direction, and d is retained to preserve units. Rearrangement ofEq. (a) gives

Table 6-7

Member Stiffness Matrix for a Beam Subjected to Axial Force

3Ls2

2L2s:1

###### -3Ls2 L 2.\"

![image 581](Matrix Analysis of Framed Structures_images/imageFile581.png)

430 Chapter 6 Additional Topics for the Stiffness Method

Table 6-8

Stiffness Functions for a Beam Subjected to Axial Force

Condition ofAxial Force Function

Compression Zero Tension

- S1

(kL)3sin kL

1

(kL)3sinh kL

12$, 12$r (kL)2(1 - cos kL)

1

- S2 (kL)2 (cosh kL - 1) 6$c 6$r

kL(sin kL - kL cos kL)

1

kL(kL cosh kL - sinh kL)

- S3 4$c 4$r

._-----

kL(kL - sin kL)

1

kL(sinh kL - kL)

- S4 24>c 2$r


$c = 2 - 2 cos kL - kL sin kL $r = 2 - 2 cosh kL + kL sinh kL k=ff

Ell:

(b)

in which

###### k- Hi-

(c)

Elz

For Eq. (b) the general solution is

v = A sin kx + B cos kx + .::l + (SMIIX - SM21)lk2Elz (d)

The constants A and B in this result depend upon boundary conditions at the ends, as follows:

x = 0, v =.::l: B = SM2Ilk2Elz (e) x = 0, dvdx = o.. A = -SMll/k3Elz (f) x = L, v = 0: A sin kL + B cos kL + .::l

+ (SM11L - SM21)lk2EIz = 0 (g) x = L, dvdx = o.. Ak cos kL - Bk sin kL

+ SMll/k2Elz = 0 (h)

![image 582](Matrix Analysis of Framed Structures_images/imageFile582.png)

Now substitute the constants A and B from Eqs. (e) and (f) into Eqs. (g) and (h) to produce

SMII. SM21 1

--3- sm kL + k---Y-- cos kL + Ll + -2- (SMIIL - SM21) = 0 (i)

k Elz Elz k Elz

- -2SMII- SM21 . SMII

cos kL - - sm kL + -2- = 0 (j) k Elz kElz k Elz

Then rearrange and simplify Eqs. (i) and (j), as follows:

SMII(kL - sin kL) + SM2Ik(cos kL - 1) = -k3E/zLl (k)

SMII(l - cos kL) - SM21k sin kL = 0 (1) Solve Eqs. (k) and (1) to find

(6-81 )

for which Ll = 1 and the functions SI and S2 are

(kL)3 sin kL

(6-82a)

SI = 12<pc

and

<Pc = 2 - 2 cos kL - kL sin kL (6-82b)

These results appear in Tables 6-7 and 6-8. Formulas for SM31 and SM41 may be found by equHibrium of forces and moments in Fig. 6-26a.

The elements of the transfer matrix TML are pictured in Fig. 6-27 for a beam subjected to an axial compressive force P. These elements may also be obtained by beam analysis, taking into account the axial-flexural interaction; and the results are shown in Table 6-9. When the axial force is equal to zero, the matrix TML reduces to that shown by Eq. (6-4).

If axial-flexural interactions are to be taken into account in the analysis of plane or space frames, it is necessary to make further modifications of the stiffness method beyond those already described for SM and TML' The analysis is complicated by the fact that the axial forces in the members are related to the joint displacements and must be calculated in a cyclic fashion. In the first cycle of analysis the stiffness method is applied as explained in Chapter 4. In the second cycle the axial forces in the members, as obtained from the first cycle, are used to determine the modified member stiffnesses (see Tables 6-7 and 6-8) and also to find the modified fixed-end actions (see Table 6-9). The second cycle is then completed, using the modified stiffnesses and fixed-end actions; and new values for the axial forces are obtained. This process is repeated until two successive analyses yield approximately the same results.

![image 583](Matrix Analysis of Framed Structures_images/imageFile583.png)

t1ML31

t1MLll

2tA.l=1

CD

k~~ Xu

~~rJ_'________~~______~------------~I

###### 0 ~IE T"'''/I

/. =:=--

TUL2~ I

b :

L

(0)

Fig. 6-27. Elements of transfer matrix TML for a beam subjected to an axial force.

The cyclic method of analysis described above may be used to determine the buckling load for a frame. The loads on the frame may be gradually increased until the stiffness matrix SFF becomes singular. This singularity is the criterion for obtaining the magnitude ofloading that causes elastic instability in the fundamental buckling mode.

6_19 Axial Constraints in Frames. If members of a plane or space frame are perpendicular to each other, the influences of axial strains may be omitted without difficulty (see Example 3 in Secs. 2.7 and 3.6). However, this matter is not simple for frames with straight members that are oriented arbitrarily in a plane or in space. When axial constraints are imposed for m members of a frame, the number of translational degrees of freedom is reduced by m (see Sec. 1.7). A method can be devised for reducing the number of joint equilibrium equations by automatically selecting m of the joint translations to be dependent upon the others. This reduction procedure may be combined with matrix condensation (see Sec. 6.12) to eliminate joint rotations while retaining joint translations. It is assumed that the frame to

![image 584](Matrix Analysis of Framed Structures_images/imageFile584.png)

6.19 Axial Constraints in Frames 433

Table 6-9

Elements of Transfer Matrix TML for a Beam Subjected to Axial Force

Condition ofAxial Force Element

Compression Zero Tension

J... (cos kL - cos ka + cos kh h'(3a + h) J... (cosh kL - cosh ka + cosh kh

<1>1' -

+ kh sin kL - I) L" <l>rkh sinh kL - 1) _1_ (sin kL - sin ka - sin kh ah2 ~ (sinh kL - sinh ka - sinh kh

T.ULlI

T.UL21 k<l>c -- k<l>r

- kh cos kL + kL cos kh - ha) L' - kh cosh hL + kL cosh kh - ka)

J... (cos kL - cos kh + cos ka a'(a + 3h) J... (cosh kL - cosh kb + cosh ka

<l>r - L" <l>r

T.UI':l1

+ ka sin kL - 1) - ka sinh kL - 1)

_1_ (-sin kL + sin kh + sin ka

{f2b _1_ (-sinh kL + sinh kh + sinh ka TUfAl k<l>c - k<l>r

+ ka cos kL - kL cos ka + kh) L' + ka cosh kL - kL cosh ka + kh) !..- (sin ka + sin kh - sin kL)

T.Vl,l2 -6ah !-. (-sinh ka - sinh kh + sinh kL)

<l>c L" <l>r

J... (cos kL + cos kh - cos ka h(Za - h) J... (cosh kL + cosh kh - cosh ka rUL2'/. <l>c L' <l>r

+ kL sin kh - 1) - kL sinh kb - 1) !-. (-sin ka - sin kb + sin kL)

TJ/L;\2 --6ab !-. (sinh ka + sinh kh - sinh kL)

<1>1' L" <l>T

J... (cos kL + cos ka - cos kh a(2h - a) J... (cosh kL + cosh ka - cosh kh <l>c+ kL sin ka - I) L' -<l>rkL sinh ka - 1)

Tj\IfA2

<l>c= 2 - 2 cos kL - kL sinkL <l>r= 2 - 2 coshkL +kL sinhkL k - {,f

Ely.

L---.

be analyzed is underconstrained, so that no complications will arise from redundant constraints (or superfluous members) [6, 7].

The axial constraint condition for zero elongation of a typical member i in a plane frame (see Fig. 6-28a) may be stated as

(Djl - Dkl)CX + (Dj2 - DdCy = 0 In this equation the symbols Djl and Dj2 represent the x and y translations ofjointj, and Dkl and Dk2 are those at joint k. As before, the x and y direction cosines of the axis of the member are denoted by Cx and Cy.

Similarly, the axial constraint condition for zero elongation of a space frame member (see Fig. 6-28b) becomes

(Djl - Dkl)CX + (Dj2 - DdCy + (Dj3 - Dk3)CZ = 0

Here Dj3 and Dk3 are translations of joints j and k in the z direction, and Cz is the z direction cosine of the member axis.

![image 585](Matrix Analysis of Framed Structures_images/imageFile585.png)

###### "tk2__

y

,/1111 113

I I I

###### I I I

x

z

(0)

y t115

t"2

###### O " __

ti2Jt' 113:

i It 1 114

###### . i ...-_Jk6 I Iy i1 i4 I

. I I

Iy I I

/-~--~~---------+------,--x

- -----k.I /---.. / //

_____________---_..... ::::"J/1//

z

( b)

Fig. 6-28. Frame members: (a) plane and (b) space.

Assembling these constraint conditions into a matrix format for either a plane or a space frame gives

(6-83)

The matrix C in this expression is called the constraint matrix, which contains only positive and negative values of direction cosines for the constrained members. This array is of size m X nt, where nt is the number of joint translations. The vector D, in Eq. (6-83) consists of only free joint translations, because no joint rotations are involved at this stage.

Due to the constraint conditions, some of the joint translations in the vector D, will be linearly dependent upon others. In order to determine which translations are dependent and which are independent, it is necessary to investigate the rank of matrix C in a systematic fashion. The rank r and the basis (or vector space) of C are found using Gauss-Jordan elimination with pivoting. Although the rank of a matrix is unique, the basis is not. Therefore, the choice of dependent translations is arbitrary, and pivoting automatically produces the best selection. Thus, it becomes possible (in retrospect) to partition the matrices in Eq. (6-83) as follows:

![image 586](Matrix Analysis of Framed Structures_images/imageFile586.png)

6.19 Axial Constraints in Frames 435

(6-84)

In this expanded form the vector 0 1 represents r dependent translations, and O2 contains the remaining ni independent translations. Because no redundant constraints are included, the rank r of matrix C will always be equal to the number of members m. Therefore, submatrix CII in Eq. (6-84) is a square array of size m x m, and submatrix CI2 is of size m X ni'

Multiplying the matrices on the left-hand side of Eq. (6-84) produces (6-85)

Because matrix CII is square and nonsingular, Eq. (6-85) can be solved for vector 0 1 in terms of vector O2, Thus,

- (6-86) in which the operator TI2 is
- (6-87)


During the Gauss-Jordan elimination process, the matrix C II is replaced by an identity matrix; and C I2 is replaced by -TI2• If the operations are also applied to an identity matrix 1m of order m, it will be replaced by C III . Define this inverse to be the operator

Til = CIII (6-88) Then the original augmented constraint matrix is

(6-89)

To confirm ideas regarding the constraint matrix, consider the plane frame in Fig. 6-29, for which the member information is given in Table 6-10. The augmented constraint matrix [see Eq. (6-89)] for this case is

1 2 4 5

lO707 0.707 -0.707 -0.707 1.000 0

,Ll

C1 = 0 -1.000 0 0 0 1.000 (a) 0 0 0.447 -0.894 0 0

The numbers above the columns of C indicate the translational displacements shown in Fig. 6-29. After the Gauss-Jordan procedure is applied, the matrix in Eq. (a) becomes

I 2 4 5

l'~

###### -1~1l8l

0 -1.500 0 1.414 1.000

C{ = 0 1.000 0 0 0 -1.000 (b)

0 0 -0.500 1.000 0 0 -1.118

![image 587](Matrix Analysis of Framed Structures_images/imageFile587.png)

y

###### 1

L

L

3 _____-+__x 4~

L-J

Fig. 6-29. Three-member plane frame.

Therefore,

###### -1~1l8l

1.000

ll.t

Til = CI,' -1.000 0 -1.118

(c)

And

4

ll.~l

TI2 -CI,'C'2 =

(d)

0.500

Thus, the dependent translations are found to be 1, 2, and 5; whereas, the independent translation is automatically chosen to be 4. Note that there is no need to rearrange the augmented constraint matrix during this procedure.

In preparation for a coordinate transformation associated with axial constraints, define a generalized displacement vector i), as follows:

![image 588](Matrix Analysis of Framed Structures_images/imageFile588.png)

6.19 Axial Constraints in Frames 437

Table 6-10

Member Information for Plane Frame

Member Jointj Joint k Cx Cy I I 2 0.7071 0.7071 2 3 I 0 1.000 3 2 4 0.4472 -0.8944

###### I

(6-90)

The first part of D consists of a null vector, representing member elongations (which are zero); and the second part contains the independent translations D2. To relate the vector D to Dt, let

(6-9Ia) Or

10 l ICII C12llDll

LD2J L0 12 JLD2J (6-91b) In Eq. (6-91b) the upper part represents the constraint conditions, and the lower part merely reproduces D2• Because the generalized displacements are independent and constitute a complete set, there is also an inverse relationship in the form

- (6-92)

where

- (6-93)


Matrix T c is an operator that can be used to transform action equations from the original displacement coordinates to the generalized displacement coordinates for axial constraints. Notice that submatrices TII and T12 are generated automatically in the Gauss-Jordan procedure described previously.

Now restate (without subscripts) the equations of equilibrium for free displacements at the joints of a plane or space frame as

SD = A (6-94a)

If rotations are separated from translations, this equation can be written in the expanded form

(6-94b)

![image 589](Matrix Analysis of Framed Structures_images/imageFile589.png)

in which the subscripts rand t denote rotations and translations, respectively. Then use matrix condensation to eliminate the rotations and retain the translations in Eq. (6-94b), yielding

S~Ot = A~ (6-95) where

S~ = Sit + T~Srt (6-96) A~ = At + T~Ar (6-97)

The transfonnation operator Trt in these expressions relates the rotations Or to the translations Ot, as follows:

- (6-98) where
- (6-99)


The operator Tc [see Eq. (6-93)] can now be used to transfonn the reduced equations in Eq. (6-95) to the generalized displacement coordinates D in Eq. (6-90). Because axial constraints are to be imposed, axial stiffnesses of members must be omitted from the structural stiffness matrix. Then to satisfy equilibrium at the joints, Eq. (6-95) is revised to become

(6-100)

in which the symbol Q denotes a vector of axial forces in the constrained members. Here the transposed constraint matrix is required to convert the axial forces to structural directions.

To perfonn the transfonnation, substitute Eq. (6-92) into Eq. (6-100) and premultiply by T~ to obtain

###### 8D = A + CQ

- (6-101)
- (6-102)
- (6-103)
- (6-104)
- (6-105)
- (6-106)


Writing this equation in expanded fonn yields

I~\l ~12JI 0 J= I~IJ + PIJQ

###### LS2I S22 L02 LA2 L0

Multiplying tenns and rearranging the results produces

8220 2 = A2 and

###### Q = 81202 - AI

The barred matrices in these equations have the definitions 812 = Ti,S~\T'2 + Ti,si2 822 = Ti2Si,TI2 + Ti2Si2 + Si,T'2 + Si2

![image 590](Matrix Analysis of Framed Structures_images/imageFile590.png)

6.19 Axial Constraints in Frames

439

A, = TT,A;" A2 = TTzA;" + Ai

(6-107) (6-108)

Equation (6-103) represents a doubly reduced set of equilibrium equations that can be solved for the independent translations D2. Then the vector D2 may be substituted into Eq. (6-104) to determine the vector of axial forces Q in the members. Next, dependent translations D, can be obtained from Eq. (6-86); and the rotations Dr are found using Eq. (6-98). Finally, other internal actions and support reactions may be calculated from known relationships.

Whenever axial strains are omitted from analyses of plane or space frames, a loss of accuracy is bound to occur. The significance of such discrepancies will vary from one problem to another. However, for most practical underconstrained frames, the loss of accuracy due to introducing axial constraints is likely to be negligible, except in the columns of tall buildings [I] and similar structures. Moreover, the numerical problem of ill conditioning due to combining large axial stiffnesses with small flexural and torsional stiffnesses is completely avoided. Of course, when the members in a frame are perpendicular to each other, omission of axial strains is easily accomplished without the formal procedure of this section.

Example. For the three-member plane frame in Fig. 6-29, do the following. First, set up the stiffness and load matrices for the six degrees of freedom shown. Second, use matrix condensation to eliminate the two joint rotations and retain the four translations. Third, by imposing axial constraints, eliminate three dependent translations and keep the best single independent translation, which was previously found to be displacement number 4. As the last step, analyze the reduced system for the loads shown in the figure.

From Table 4-27, determine member stiffnesses (without axial terms), assemble them, and rearrange the results to produce the following submatrices of the structural stiffness matrix:

3 6 S = E/z l6.828

1.414J3

(e)

rr L 1.414

4.617 6

2 4 5

S - Elz l3.879 2.121 2.121 -2.121

###### J~

(f)

rt - L2 -2.121 2.121 3.195 -1.585

2 4 5

###### s [ 1412 SYffiT

###### = Elz -2.121 2.121

(g)

" L' -2.121 2.121 2.980

2.121 -2.121 -1.692

2.336 :

![image 591](Matrix Analysis of Framed Structures_images/imageFile591.png)

440 Chapter 6 Additional Topics for the Stiffness Method

Also, Fig. 6-29 shows that the parts of the rearranged load vector are

Ar = {O, O} A, = {I, 1,0.5, O}P (h)

For the purpose of applying matrix condensation, calculate the inverse of submatrix Srr as

1 L I 0.1564 -0.04790l Sr-;: = Elz L-0.04790 0.2313.

- (i)
- (j)
- (k)


Then from Eg. (6-99), the operator Tr, becomes

2 4 5

= ~ l-0.7083 -0.2301 -0.1787 0.2558l3 L 0.6764 -0.3890 -0.6374 0.2650 6

In accordance with Eg. (6-96), the reduced stiffness matrix S~ is 2 4 5

~:: 0.565 Syml:

###### r

9.940

###### S* = EIz -2.189 It L3 -1.463

-1.017 -0.303 1.374 5 In addition, Eg. (6-97) yields

2.552

A~ = {l, 1,0.5, O}P

###### (I)

Next, reduce further the stiffness and load matrices to account for axial constraints on the members. Rearranging and partitioning the stiffness matrix in Eg. (k) produces

2 5

sil = ~: [~~~~~9 0.808 sym.] ~ 2.552 -1.017 1.374 5 125

- (m)
- (n)


###### Elz T

sil = L3 [1.463 0.391 0.303] 4 = Si2

4

S22* = -jElz [0.565] 4

###### (0)

L"

the last of which is just a single term. Similarly, the load vector in Eg. (I) gives

###### Ai = {l, 1, O}P Ai = O.5P (p)

Then the barred matrices in Egs. (6-105) through (6-108) become

![image 592](Matrix Analysis of Framed Structures_images/imageFile592.png)

###### References 441

4

20.82 ] I = ElL1z 18.12 2 -21.17 3

[

(q)

###### AI = p[ 1.~14 J~

A2 = P[2.0] 4 (r)

-1.118 3

For these arrays the indexes I, 2, and 3 denote member numbers; whereas, index 4 represents the independent joint translation.

Now all of the matrices are available for solving Eq. (6-103) and finding the axial forces in Eq. (6-104) due to the applied loads. Thus,

--..".,22.4IEIz----= D4 = 2.0P

- (s)
- (t)
- (u)


L

Solving for the independent displacement D4 yields

PL'

D4 = 0.08925 -

Elz

Substitution of D4 and the appropriate barred matrices into Eq. (6-104) produces

0.4442 ]

Q [

1.617 P

-0.7714

which are the axial forces in the members. Completion of this example includes computing the dependent joint translations, the joint rotations, other internal member actions, and support reactions. However, these tasks are straightforward and will be left as exercises for the reader.

###### References

I. Weaver, W., Jr., and Nelson, M. F., "Three-Dimensional Analysis of Tier Buildings," ASCE 1. Stmc. Dil'., Vol. 92, No. ST6, 1966, pp. 385-404.

- 2. Glockner, P. G" "Symmetry in Structural Mechanics," ASCE 1. Struc. Dil'.. Vol. 99, No. STI, 1973, pp. 71-89.
- 3. Zienkiewicz, O. C., and Scott, F. C., "On the Principle of Repeatability and Its Application in Analysis of Turbine and Pump Impellers," /111. 1. NUlIler. Meth. Ell/V., Vol. 4, No.3, 1972, pp. 445-448.
- 4. Gere, 1. M., and Timoshenko, S. P., Mechanics afMaterials, 3rd ed., PWS-Kent. Boston, MA,1990.
- 5. Weaver, W., Jr., "Dynamics of Elastically Connected Rigid Bodies," Dew,l. Theor. Appl. Mech., Vol. 3, Pergamon, New York, 1967, pp. 543-562.
- 6. Weaver, W., Jr., "Constraints for Axial Strains in Frames," ASCE 1. Struc. Dil'., Vol. 106, No. I, 1980, pp. 199-209.
- 7. Weaver, W.. Jr., and Eisenberger. M.. "Dynamics of Frames with Axial Constraints," ASCE 1. Struc. Dil'., Vol. 109, No.3, 1983, pp. 773-784.


![image 593](Matrix Analysis of Framed Structures_images/imageFile593.png)

442 Chapter 6 Additional Topics for the Stiffness Method

Problems

- 6.4-1. Write the transfer matrix TML for a prismatic member in a plane frame.
- 6.4-2. For a prismatic member of a grid structure, write the transfer matrix

TML·

- 6.4-3. Write the transfer matrix TML for a prismatic member in a space truss.
- 6.4-4. For a prismatic member of a space frame, write the transfer matrix TML.


- 6.5-1. Determine the vector AML of pinned end actions for a prismatic plane

truss member caused by its own weight.

- 6.5-2. For a prismatic member in a grid, find the vector AMl. of fixed-end

actions due to its own weight.

- 6.5-3. For a prismatic member in a space truss, determine the vector AML of

pinned-end actions caused by its own weight.

- 6.5-4. Find the vector AML of fixed-end actions for a prismatic space frame


member due to its own weight.

- 6.11-1. Using ftexibilities with end k free, derive the matrices 8M and T ML for

a prismatic member in a plane frame.

- 6.11-2. For a prismatic member in a grid, find the matrices 8Mand T ML, using

ftexibilities with end k free.

- 6.11-3. With endj free, use ftexibilities to derive the matrices 8M and TML for

a prismatic member in a plane frame.

- 6.11-4. For a prismatic grid member, use ftexibilities with end j free to deter-


mine the matrices 8M and T ML.

- 6.12-1. Repeat the example in Sec. 6.12, but with LI = L, L2 = 2L, IZI = I,

and In = 3/.

- 6.12-2. Repeat the example in Sec. 6.12, but with LI = 3L, L2 = 2L, IZI

- 2/, and 121 = I.


- 6.12-3. Repeat Prob. 6.12-1, but with the j end free and the k end fixed.
- 6.12-4. Repeat Prob. 6.12-2, but with the j end free and the k end fixed.
- 6.12-5. For the nonprismatic beam in the figure, assemble the flexibility matrix


FMjj at the j end of the member with the k end fixed.

![image 594](Matrix Analysis of Framed Structures_images/imageFile594.png)

Problems 443

###### I:M 0) 2 CD 3 0 I-kXM

###### :

###### :

/.1:

Iz~

2IZ~

JE JE 3Iz~ ::

i i L

L

Prob. 6.12-5.

6.12-6. Extend the example in Sec. 6.12 to the case of a plane frame member (see figure), and derive matrices SM amI TML'

###### IYM

j ~~~~~::::::::::;=;;~~~====*-k--XM

###### ZM 1-01EOE---- ---~<----L---~I

/

Prob. 6.12-6.

- 6.14-1. By the method of matrix condensation, derive matrix (b) in Tables 6-

I and 6-2.

- 6.14-2. Repeat Prob. 6.14-1 for matrix (d).
- 6.14-3. Repeat Prob. 6.14-1 for matrix (e).
- 6.14-4. By the method of matrix condensation, derive matrix (g) in Table

6-2.

- 6.14-5. Repeat Prob. 6.14-4 for matrix (h).


- 6.15-1. By the flexibility approach, derive again the matrix SM in Table 6-3;

but with end j free and end k fi xed.

- 6.15-2. Using Eg. (6-33), develop the tenns for the transfer matrix TML In

Table 6-4.

- 6.15-3. For a prismatic beam with a rotational elastic connection at the k end


only (see figure), detennine FMji, SMI/' SMki' SMik, and SMH, using the transformation operator Tki'

![image 595](Matrix Analysis of Framed Structures_images/imageFile595.png)

###### 444 Chapter 6 Additional Topics for the Stiffness Method

Prob. 6.15-3.

- 6.15-4. Repeat Prob. 6.15-3, but with the elastic connection at thej end only.
- 6.15-5. Derive matrix SM for a prismatic beam with a rotational elastic connection at an intermediate point, as shown in the figure. Use the flexibility approach with the k end free to find FMkb SMkk' and so on. For simplification, introduce the notation el = I + e, e2 = 1 + 2eblL, e} = 1 + 3eb21L2, and so on.


Prob. 6.15-5.

- 6.15-6. For the beam in Prob. 6.15-5, develop the terms In matrix TMLko assuming that loads are applied just to the right of point f.
- 6.15-7. The prismatic beam in the figure has unequal rotational elastic connections at ends j and k. Using the flexibility approach, determine matrix SM' starting with the j end free. Introduce new notation, as follows: ej = Elz1LSf.j' ek = ElziLSu , ejl = I + ej' ej2 = 1 + 2ej' ej.l = 1 + 3ej' eo = I + eb ek2 = I + 2eko ek3 = 1 + 3eb ejk = I + ej + eko and so on.


Prob. 6.15-7.

![image 596](Matrix Analysis of Framed Structures_images/imageFile596.png)

Problems 445

6.15-8. The figure shows a circularly curved member of a plane frame (see also Fig. 6-17) with equal rotational elastic connections at both ends. In terms of r, <1>, and Sf., what additional formulas are required for the elements in matrix FMH ?

It

Prob. 6.15-8.

- 6.16-1. For the nonprismatic member in Fig. 6-16a, derive matrices SMH and

TMLk for the k end, including shearing deformations.

- 6.16-2. For the prismatic beam with elastic connections in Fig. 6-2Ia, deter-


mine again the member stiffness matrix SM, including terms for shearing deformations.

- 6.16-3. Repeat Prob. 6.16-2 for unequal elastic connections.
- 6.16-4. Assuming that the form factor fis constant, what terms due to shearing

deformation must be added to FMJi for the nonprismatic beam in Prob. 6.12-5?

- 6.16-5. What terms due to shearing deformations must be added to FMkk for


the nonprismatic beam in the figure? Assume that the form factorf is constant, and leave results from the unit-load method in integral form.

Prob. 6.16-5.

- 6.17-1. The plane frame member i in the figure lies in the x-y plane and has


the stiffness matrix SMS for structural axes. Find element (SMBh.6 for points p and q in terms of elements in SMS (call them SII' S12' etc.) and the offsets a, b, c, and d at ends j and k.

![image 597](Matrix Analysis of Framed Structures_images/imageFile597.png)

446 Chapter 6 Additional Topics for the Stiffness Method

y

~----------------x

###### z

Probs. 6.17-1 through 6.17-4.

- 6.17-2. Repeat Prob. 6.17-1, but for element (SMB)2.4'
- 6.17-3. If the figure represents a member in a grid instead of a plane frame,

repeat Prob. 6.17-1; but find element (SMB) 1.5'

- 6.17-4. Repeat Prob. 6.17-3, but for element (SMBh.6'


![image 598](Matrix Analysis of Framed Structures_images/imageFile598.png)

###### 7Finite·Element Method forFramed Structures

7.1 Introduction. Matrix analysis of framed structures may be considered as a subset of the more general method of finite elements [1-4]. Any continuum can be partitioned into subregions called finite elements. These subregions are of finite size and usually have simpler geometries than the boundaries of the original continuum. Such a partitioning serves to convert a problem involving an infinite number of degrees of freedom to one with a finite number in order to simplify the solution process. Applications in solid mechanics consist of framed structures, two- and three-dimensional solids, plates, shells, and so on. One-, two-, and three-dimensional finite elements may be required for such analyses. However, the members of framed structures are relatively long compared to their cross-sectional dimensions, so only one-dimensional finite elements are needed to model them.

Finite-element theory of structures yields an approximate analysis based upon assumed displacement functions, stress functions, or a mixture of these within each element. Because the assumption of displacement functions is the technique most commonly used, the following steps suffice to describe this approach for static analysis of framed structures:

- 1. Divide the structure into a finite number of elements (members or segments of members).
- 2. Select key points on the elements to serve as nodes (or joints), where conditions of equilibrium and compatibility are to be enforced.
- 3. Assume displacement functions within each element so that the displacements at every point are dependent upon those at the nodes.
- 4. Satisfy strain-displacement and stress-strain relationships within every element.
- 5. Determine stiffnesses and equivalent nodal loads for a typical element, using work or energy principles.
- 6. Develop equilibrium equations for the nodes of the structure by assembling element contributions.
- 7. Solve these equilibrium equations for the displacements at unrestrained nodes.
- 8. Using the nodal displacements, calculate internal actions at the ends of each element.
- 9. Determine support reactions at restrained nodes if desired.


447

![image 599](Matrix Analysis of Framed Structures_images/imageFile599.png)

448 Chapter 7 Finite-Element Method for Framed Structures

The reader should notice that steps 1, 2, and 6 through 9 correspond to the direct stiffness method described earlier in Chapter 4. Hence, only steps

- 3, 4, and 5 require detailed explanations in this chapter. In the next section, strain-stress and stress-strain relationships will be


discussed for linearly elastic continua. Then the finite-element theory is presented in Sec. 7.3, based on the principle of virtual work. That section displays formulas for stiffnesses and equivalent nodal loads for any type of finite element. Section 7.4 concentrates upon one-dimensional elements that are needed for matrix analysis of framed structures, as described in Sec. 7.'5.

7.2 Stresses and Strains in Continua. Recall that in Sec. 1. 13 the six independent stresses and the corresponding strains in a three-dimensional continuum were represented as column matrices (or vectors). Thus,

al ax EI Ex

- a2 ay E2 Ey
- a3 az E3 Ez

cr= E = (7-1)

- a4 Txy E4 'Yxy
- a5 TyZ ES 'Y,vz
- a6 Tzx E6 'Yzx


where the bold-faced Greek letters cr and E denote the vectors shown.

Strain-stress relationships for an isotropic material are drawn from the theory of elasticity [5], as follows:

1

Ex = E(ax - vay - vaz)

'Yxy = TnG

- (7-2)
- (7-3)


where

###### E G=---

2(1 + v)

In these expressions E = Young's modulus of elasticity, G = shearing modulus of elasticity. and v = Poisson's ratio. With matrix format, the relationships in Eqs. (7-2) may be written as

E = Ccr (7-4) in which

![image 600](Matrix Analysis of Framed Structures_images/imageFile600.png)

7.3 Virtual-Work Basis of Finite-Element Method 449

-/I -/I 0 0 0 -/I -/I 0 0 0

-/I -/I 0 0 0

C=~

(7-5)

E 0 0 0 2(1 + /I) 0 0 0 0 0 0 2(1 + /I) 0 0 0 0 0 0 2(1 + /I)

Matrix C is an array that relates the strain vector E to the stress vector (J. By the process of inversion (or simultaneous solution), we can also obtain stressstrain relationships from Eq. (7-4), as follows:

(J = EE (7-6) where

###### E = C-I

- /I /I /I 0 0 0 /I - /I /I 0 0 0 /I /I - /I 0 0 0

- 2/1

E 0 0 0

0 0

(1 + /1)(1 - 2/1) 2

- 2/1

0 0 0 0

0

2

- 2/1

0 0 0 0 0

2

(7-7) Matrix E relates the stress vector (J to the strain vector E.

For the elements discussed in Sec. 7.4, we will not need the 6 x 6 stressstrain matrix given by Eq. (7-7). With one-dimensional elements, only one term, such as E or G, is required. If we were to deal with two- and threedimensional elements, larger matrices [up to the size of that in Eq. (7-7)] would be needed.

7.3 Virtual-Work Basis of Finite-Element Method. To begin, some new definitions and notations are introduced that pertain to all types of finite elements for elastic continua. From the principle of virtual work, equilibrium equations can be developed that include formulas for stiffnesses and

![image 601](Matrix Analysis of Framed Structures_images/imageFile601.png)

450 Chapter 7 Finite-Element Method for Framed Structures

equivalent nodal loads for a typical element. These terms are treated in detail for one-dimensional elements in the next section.

Let the displacements at any point within a three-dimensional element be expressed as the column vector

u = {u, v, w} (7-8)

where u, v, and ware translations in the x, y, and z directions, respectively.

If the element is subjected to body forces, such forces may be placed into a vector b, as follows:

(7-9)

Here the symbols bX' by, and bz represent components of force (per unit of volume, area, or length) acting in the reference directions at any point.

Nodal displacements q will at first be considered as only translations in the x, y, and z directions. Thus, if ncn = number of element nodes,

q = {q;} (i = 1, 2, ... , nen) (7-lO) where

(7-11)

However, other types of displacements, such as small rotations (av/ax, and so on) and curvatures (a2v/ax 2, and so on) could also be used.

Similarly, nodal actions p will temporarily be taken as only forces in the x, y, and z directions at the nodes. That is,

(i = 1, 2, ... , ncn) (7-12)

in which

(7-13)

Other types of nodal actions, such as moments, rates of changes of moments, and so on, could be used as well.

For the type of finite-element method discussed in this chapter, certain assumed displacement shape functions relate displacements at any point to nodal displacements, as follows:

u = fq (7-14)

In this expression the symbol f denotes a rectangular matrix containing geometric functions that make u completely dependent upon q.

Strain-displacement relationships are obtained by differentiation of the displacements. This process may be expressed by forming a matrix d, called a linear differential operator, and applying it with the rules of matrix multiplication. Thus,

###### E = du (7-15)

![image 602](Matrix Analysis of Framed Structures_images/imageFile602.png)

7.3 Virtual-Work Basis of Finite-Element Method 451

In this equation the operator d expresses the strain vector E in terms of displacements in the vector u [see Eqs. (b) and (c) in Sec. 1.13)]. Substitution of Eq. (7-14) into Eq. (7-15) yields

E = Bq (7-16) where

B = df (7-17)

Matrix B gives strains at any point within the element due to unit values of nodal displacements.

Stress-strain relationships between the vectors (J and E are given by Eq. (7-6) in the preceding section. Substitution of Eq. (7-16) into Eq. (7-6) produces

(J = EBq (7-18)

in which the matrix product EB gives stresses at any point due to unit values of nodal displacements.

Application of the principle of virtual work (see Sec. 1.14) to a finite element yields

###### oUe = oWe (7-19)

where oUe is the virtual strain energy of internal stresses and oWe is the virtual work of external actions on the element. To develop both of these quantities in detail, assume a vector oq of small virtual nodal displacements. Thus,

oq = {oq;} (i = 1, 2, . . . , nen) (7-20)

Then the resulting virtual displacements at any point in the element become [see Eq. (7-14)]

ou = foq

- (7-21)
- (7-22)
- (7-23)


Using the strain-displacement relationships in Eq. (7-16) produces

bE = Boq

Now the internal virtual strain energy can be written as

where integration is over the volume of the element. In addition, the external virtual work of nodal and body forces becomes

###### oWe= oqTp+ LouTbdV (7-24)

Substitution of Eqs. (7-23) and (7-24) into Eq. (7-19) gives

![image 603](Matrix Analysis of Framed Structures_images/imageFile603.png)

452 Chapter 7 Finite-Element Method for Framed Structures

###### LfJETCJdV= OqTp+LouTbdV (7-25)

Then substitute Eq. (7-18) into Eq. (7-25) and use the transposes of Eqs. (7-21) and (7-22) to obtain

oqTLBTEBdVq = oqTp+oqTLfTbdV

- (7-26)
- (7-27)
- (7-28)
- (7-29)


Cancellation of oqT from both sides of Eq. (7-26) produces

###### Kq = P + Ph

where

and

Matrix K in Eq. (7-28) is the element stiffness matrix, which contains stiffness coefficients that are actions at nodes due to unit values of nodal displacements. Also, the vector Ph in Eq. (7-29) consists of equivalent nodal loads due to body forces in the vector b.

The stresses and strains considered in the above derivation are due only to nodal displacements. If initial strains Eo exist, the total strains may be expressed as

E = EO + CCJ (7-30)

in which C is the matrix of strain-stress relationships discussed in Sec. 7.2. Thus, Eq. (7-7) gives

- (7-31)
- (7-32)


Solving for the stress vector in Eq. (7-30) yields

CJ = E(E - EO)

When this expression is used in place of CJ in Eq. (7-25), the formulation leads to

Kq = P + Ph + Po (7-33) where

(7-34)

![image 604](Matrix Analysis of Framed Structures_images/imageFile604.png)

(0)

###### 1~

( b)

###### ~,

(c)

Fig. 7-1. Axial element.

The vector Po may be considered to consist of equivalent nodal loads due to initial strains or temperature changes.

7.4 One-Dimensional Elements. In this section properties are developed for one-dimensional elements subjected to axial, torsional, and flexural deformations, starting with the axial element in Fig. 7-1 a. The figure indicates a single translation u in the x direction at any point. Thus, Eq. (7-8) from the preceding section yields

u = u

The corresponding body force is a single component h, (force per unit length), acting in the x direction. Therefore, Eq. (7-9) gives

###### b = bx

Nodal displacements q, and q2 consist of translations in the x direction at nodes 1 and 2 (see Fig. 7-1a). Hence, Eq. (7-10) becomes

###### q = {q" q2} = {u" U2}

Corresponding nodal forces at points 1 and 2 are given by Eq. (7-12) as

###### p = {Ph P2} = {Pd, Px2}

Assume that the displacement u at any point within the element varies linearly with x, as follows:

(a)

This expression is called a displacement function. It may be put into the form of a displacement shape function [see Eq. (7-14)] by evaluating the two undetermined constants c, and C2. That is, for x = 0, c, = q,; and for x = L, q2 = C, + c2L. Therefore, C2 = (q2 - q,)IL. Substituting these constants into Eq. (a) produces

![image 605](Matrix Analysis of Framed Structures_images/imageFile605.png)

454 Chapter 7 Finite-Element Method for Framed Structures

###### u = q, + (q2 ~ q,) X (b)

which is now in tenns of the two nodal displacements instead of the two constants. Equation (b) matches the fonn of Eq. (7-14) and can be rewritten as

###### II x

u= ~l[::]

(c)

L

or,

u = fq (d)

where

f=[f, 12]=II x

L iJ (7-35)

Figures 7-1band c show the resulting linear displacement shape functions it and12 derived for this element. These functions give the variations of u along the length due to unit values ofthe nodal translations q, and q2. They are exact for a prismatic element but are only approximate if the element is nonprismatic.

From Fig. 7-2 it is evident that the single strain-displacement relationship du/dx for the axial element is constant on the cross section. Thus, Eqs. (7-15), (7-16), and (7-17) yield

du df

E = Ex = - = - q = Bq (7-36a)

dx dx where

df 1

B = df = - = - [-1 1]

(7-36b)

dx L

y

"7""-;;-""-+--+--- K, U

z

Fig. 7-2. Axial deformations.

![image 606](Matrix Analysis of Framed Structures_images/imageFile606.png)

Here the linear differential operator d is simply d/dx. As shown in Eq. (7-36a), matrix B expresses the strain Ex in tenns of the nodal displacements

- q. Similarly, the single stress-strain relationship [see Eq. (7-18)] becomes merely


(7-37a) Hence,

###### E

###### E=E and EB = L[-I I] (7-37b)

Equation (7-37a) shows that the product EB gives the stress ax in tenns of the nodal displacements.

From Eq. (7-28) the element stiffness matrix K may now be evaluated, as follows:

###### K~ LBTEBdV~:;[~}-1 I) J: l,dAdx

Multiplication and integration over the cross section and the length give

###### K~E:[~1 ~1]

(7-38)

assuming that the cross-sectional area A is constant. In addition, equivalent nodal loads due to body forces [see Eq. (7-29)] are simply

(7-39)

in which the force intensity bx varies along the length L.

The stiffness matrix K is unique and exact for the prismatic axial element; but it is only approximate if the cross-sectional area is not constant along the length. On the other hand, an infinite number of equivalent nodal load vectors Ph can be derived, depending upon the distribution of body forces. For example, suppose that a linearly varying load bx = b2x/L (force per unit length) is applied to an axial element. Then Eq. (7-39) produces

###### rL brL[L-x] b L[I]

Ph = Jo fT(bzX/L)dx =L; Jo x xdx =1- 2 (e)

which shows that the equivalent force at node I is half that at node 2 for this load.

For the torsional element in Fig. 7-3a, the single displacement at any point is a small rotation Ox about the x axis (indicated by a double-headed arrow). Thus,

![image 607](Matrix Analysis of Framed Structures_images/imageFile607.png)

###### 456 Chapter 7 Finite-Element Method for Framed Structures

(0)

(b)

###### ~1

( c)

Fig. 7-3. Torsional element.

Corresponding to this displacement is a single body action

###### b = mx

which is a moment per unit length acting in the positive x sense. Nodal displacements in the figure consist of small axial rotations at nodes 1 and 2. Hence,

In addition, the corresponding nodal actions at points 1 and 2 are

which are moments (or torques) acting in the x direction. As for the axial element, we use the linear displacement shape functions II andh shown in Figs. 7-3b and c. Therefore,

(f)

in which the matrix f is again given by Eq. (7-35). However, in this case the functions mean that variations of ()x along the length are caused by unit values of the nodal rotations q) and q2.

Strain-displacement relationships can be inferred for a torsional element with a circular cross section by examining Fig. 7-4. If radii remain straight during torsional deformation, the shearing strain l' will vary linearly with the radial distance r, as follows:

###### 'Y=r-=rtj;d()x

(7-40)

dx

where tj; is the twist, or rate of change of angular displacement. Thus,

![image 608](Matrix Analysis of Framed Structures_images/imageFile608.png)

###### 7.4 One-Dimensional Elements 457

![image 609](Matrix Analysis of Framed Structures_images/imageFile609.png)

###### y

###### Mx

~--+~_~---x

T

Fig. 7-4 . Torsional deformations.

(7-41 )

Equation (7-40) shows that the maximum value of the shearing strain occurs at the surface. That is,

I'max = Rl/; (g)

where R is the radius of the cross section (see Fig. 7-4). Also, from Eq. (7-40) the linear differential operator d relating l' to Ox is

d

d = r-

- (7-42)
- (7-43)


dx

Thus, the strain-displacement matrix B becomes

r

B = df = L[-1 1]

which is the same as for the axial element, except for the presence of r.

Shearing stress T (see Fig. 7-4) is related to shearing strain in a torsional element by

T = cry (7-44a) where the symbol G denotes the shearing modulus of the material. Hence,

Gr

GB = L [-1 1] (7-44b)

E=G and

These relationships are analogous to Eqs. (7-37) for the axial element.

Now find the torsional stiffness matrix K by applying Eq. (7-28), as follows:

![image 610](Matrix Analysis of Framed Structures_images/imageFile610.png)

458 Chapter 7 Finite-Element Method for Framed Structures

###### G[-1]

= L2 1 [-1 rL r27r rR

1] Jo Jo Jo (r2)r dr dO dx

~1] (7-45)

= GJ [ 1

L -1

where GJ is constant. If the cross section of the element is not circular, the polar moment of inertia J must be replaced by an appropriate torsion constant. Also, Eq. (7-29) gives the equivalent nodal loads due to body forces as

###### Ph= tfTmxdx (7-46)

where the moment intensity mx varies along the length L.

Again, the stiffness matrix K is exact for a torsional element of constant cross section, but the equivalent nodal load vector Ph changes with the type

ofloading. Ifa linearly varying moment mx = ml(L - x)/L (per unit length)

is applied to a torsional element, Eq. (7-46) yields

(h)

showing that the equivalent moment at node 1 is twice that at node 2 for this case.

Figure 7-5a shows a flexural element, for which the x-y plane is a principal plane of bending. Indicated in the figure is the single displacement vat any point, which is a translation in the y direction. Thus,

###### u = v

The corresponding body force is a single component b" (force per unit length), acting in the y direction. Hence,

b = bl'

At node 1 (see Fig. 7-5a) the two nodal displacements ql and q2 are a small translation in the y direction and a small rotation in the z sense. The fonner is indicated by a single-headed arrow, while the latter is shown as a doubleheaded arrow. Similarly, at node 2 the displacements numbered 3 and 4 are a translation and a rotation, respectively. Therefore, the vector of nodal displacements becomes

###### q = {qb q2, q3, q4} = {Vb Ozb V2, Od

![image 611](Matrix Analysis of Framed Structures_images/imageFile611.png)

- 7.4 One-Dimensional Elements


459

###### Y,V

+-~r--__

C f1

###### ~

t

(bl

C f2

###### -. ~

f3:J--_--..~-+

###### t

(dl

###### J.1/----

###### ~- ......;--~

(el

Fig. 7-5. Flexural element.

in which

###### () = (dV)

zl d.x

I

These derivatives (or slopes) may be considered to be small rotations even though they are actually rates of changes of translations at the nodes. Corresponding nodal actions at points 1 and 2 are

###### p = {p), P2, P3, P4} = {p\,), Mz), Py2' Md

The terms Pyl and Py2 denote forces in the y direction at nodes 1 and 2, and the symbols Mzl and Mz2 represent moments in the z sense at those points.

For the flexural element, assume that the displacement v at any point varies cubically with x. Then the number of undetermined constants in the displacement function will be equal to the number of nodal displacements. Thus,

(i)

![image 612](Matrix Analysis of Framed Structures_images/imageFile612.png)

460 Chapter 7 Finite-Element Method for Framed Structures

In this case the second displacement at each node bears a differential relationship to the first. Therefore, the derivative of Eq. (i) with respect to x is also needed, as follows:

dvdx = C2 + 2C3X + 3C3X2 (j)

Now the four undetermined constants CI through C4 can be evaluated from the boundary conditions.

At x = 0, VI = ql = CI

###### (:)1 = q2 = C2

(k)

At x = L, V3 = q3 = CI + C2L + C3L2 + C4L3

Solve for CI through C4 in terms of ql through q4 and substitute the results into Eq. (i) to produce

I I

V = L3 (2x3 - 3Lx2 + L3)ql + L2 (x3 - 2Lx2 + L2x)q2

(I)

This expression is the displacement shape function for the flexural element and can be written as

###### v = fq

(m)

in which

- (7-47a)
- (7-47b)


and

I

11 = 3 (2x3 - 3Lx2 + L3)

L

13 = L3I (-2x3 + 3Lx2)

These four shape functions appear in Figs. 7-5b, c, d, and e. They represent the variations of v along the length due to unit values of the four nodal displacements ql through q4' The functions are exact for a prismatic element in which shearing defomiations are omitted.

Strain-displacement relationships can be developed for a flexural element

![image 613](Matrix Analysis of Framed Structures_images/imageFile613.png)

![image 614](Matrix Analysis of Framed Structures_images/imageFile614.png)

Y,V

7"""'-----f--- Jf, U

Fig. 7-6. Flexural deformations.

by assuming that plane sections remain plane during deformation, as illustrated in Fig. 7-6. The translation u in the x direction at any point on the cross section is

###### dv

u = -y-

(7-48)

dx

From this relationship, the following expression for flexural strain is obtained:

###### du d2v

Ex -- -dx -- - Y dx 2 = - y¢ (7-49) in which ¢ represents the curvature

(7-50)

From Eq. (7-49) it is apparent that the linear differential operator d relating Ex to v is

(7-51)

Then Eq. (7-17) gives the strain-displacement matrix B as

###### B = df = - I3 [12x - 6L 6Lx - 4L2 -12x + 6L

(7-52)

In addition, flexural stress ax in Fig. 7-6 is related to flexural strain Ex simply by

(7-53a)

![image 615](Matrix Analysis of Framed Structures_images/imageFile615.png)

462 Chapter 7 Finite-Element Method for Framed Structures

Hence,

E = E and E B = EB (7-53b) Element stiffnesses now may be obtained from Eq. (7-28), as follows:

K = LBTEBdV

12x - 6L 6Lx - 4L2 -12x + 6L 6Lx - 2L2

###### rL r E~2

[12x - 6L ... 6Lx - 2L2]dAdx

Jo JA L

Multiplication and integration (with EI constant) yield

###### 6 3L -6 3L K = 2EI 3L 2L2 -3L L2

(7-54)

L3 -6 -3L 6 -3L

3L L2 -3L 2L2

Furthennore, equivalent nodal loads due to body forces [see Eq. (7-29)] become

(7-55)

in which the force intensity bl' varies along the length L.

As before, the stiffness matrix K is exact for a prismatic flexural element, but the type of loading dictates the fonn of vector Ph' For instance, if a linearly varying force by = bJ(L - x)IL + b2xlL (per unit length) acts on the element, Eq. (7-55) gives

###### Ph = -1 lL fT[bJ(L - x) + b2x] dx

L 0 (n)

For this multiplication and integration, the four displacement shape functions were drawn from Eqs. (7-47b).

Repetitious integrations over the cross sections of one-dimensional elements can be avoided by using generalized stresses and strains. While this concept is rather trivial for an axial element, it can be more useful for torsional and flexural elements. To appreciate this idea, reconsider the torsional element in Fig. 7-4, and integrate the moment ofthe shearing stress 7 about the x axis. Thus, the torque Mx is generated, as follows:

![image 616](Matrix Analysis of Framed Structures_images/imageFile616.png)

(7-56)

Substitution of the stress-strain and strain-displacement relationships from Eqs. (7-44a) and (7-40) produces

(7-57)

Now take Mr as generalized (or integrated) stress and 1/; as generalized strain.

Then the generalized stress-strain (ortorque-twist) operatorabecomes

G = GJ (7-58)

which is the torsional rigidity of the cross section. Hence, Eq. (7-57) may be rewritten as

(7-59) By this method the operator d in Eq. (7-42) does not include the multiplier

- r. Furthermore, the generalized matrix B [Eq. (7-43) devoid of r] is used instead of matrix B. That is,


B = rB (7-60)

From this point it is evident that evaluations of the terms in the stiffness matrix K do not require integrations over the cross section. Therefore,

###### K= tBTaBdx (7-61)

This expression for K is equivalent to Eq. (7-28) used previously. Also, for any initial twist 1/;0, the equivalent load vector becomes

###### Po= tjjTa1/;odx (7-62)

which replaces Eq. (7-34).

Turning now to the flexural element in Fig. 7-6, integrate the moment of the normal stress (Jx about the neutral axis to obtain Mz, as follows:

Mz=t-(JxydA (7-63)

Then substitute the stress-strain and strain-displacement relationships from Eqs. (7-53a) and (7-49) to find

Mz=E¢tldA=EI¢ (7-64)

For this element take Mz as generalized (or integrated) stress and ¢ as generalized strain. Then the generalized stress-strain (or moment-curvature)

![image 617](Matrix Analysis of Framed Structures_images/imageFile617.png)

464 Chapter 7 Finite-Element Method for Framed Structures

operator E is

E = EI (7-65)

which is the flexural rigidity of the cross section. Thus, Eq. (7-64) may be restated as

(7-66)

With this approach the operator d in Eq. (7-51) is devoid of the multiplier -yo In addition, the generalized matrix B [Eq. (7-52) without the factor -y] may be used in place of matrix B. That is,

B = -yB (7-67)

Then integration over the cross section for terms In matrix K becomes unnecessary. Hence,

(7-68)

which is analogous to Eq. (7-61). Furthermore, due to initial curvature ¢o, the equivalent load vector is

Po= LBTE¢odx (7-69)

which can be used in place of Eq. (7-34).

To confirm the use of generalized stresses and strains, recall the prismatic beam member in Prob. 2.4-3 having the following values of initial curvatures:

###### L

¢o = ¢1 for O~x ~ 2 ¢o = -¢1 for

###### L

-

2 ~x ~L

For this example, Eq. (7-69) produces

Po = LI2 BTE¢1 dx - LI2 BTE¢, dx

###### {-2, -L, 2, -L}3EI¢,/2L (0)

These results show that the forces are equal and opposite, while the moments are the same at the two ends.

7.5 Application to Framed Structures. Properties of the one-dimensional elements described in the preceding section may be combined to form stiffnesses and equivalent nodal loads for the members of framed structures. For example, the axial element provides the necessary characteristics to model a member in a plane or space truss. If the stiffness matrix Kin Eq. (7-38) for the axial element is expanded to become Ke by adding two rows

![image 618](Matrix Analysis of Framed Structures_images/imageFile618.png)

###### 7.5 Application to Framed Structuresand columns of zeros, the result is

465

o -1 0 o 0 : 0 0

EA

,

-------------:------------

(7-70)

,

L

o o 0

-1 0

o 0

which is partitioned in accordance with joints j and k. This 4 X 4 array is the same as the plane truss member stiffness matrix SM for member axes in Table 4-14, except that the symbol Ax replaces A. Furthermore, if four rows and columns of zeros are added, the matrix becomes

,

-1 0 0 0 0 0 0 0 0 0 0 0 ,,, 0 0 0

0 0

EA ,,

Ke - ---------------~--------- ---- -- (7-71)

L

-1 0 0 , 0 0 0 0 0 0 0 0 0 0 0 0 0 0

This 6 x 6 matrix pertains to a space truss member (see Table 4-39).

The flexural element coincides with the beam member described previously in Chapter 4. Thus, the 4 x 4 stiffness matrix K in Eq. (7-54) is the same as the prismatic beam member stiffness matrix SM appearing in Table 4-2, except that the symbol Iz replaces I.

To model a plane frame member, both the axial and the flexural elements are required. Thus, expansion and combination of the stiffness matrices for the axial and flexural elements produces

, rl ,, -rl 0 0 0 12 6L , 0 -12 6L ,

0 0

0 6L 4L2 0 -6L 2L2 EI ,,

---- - - - - - - - - ------- - - - - --:-- - ---- ------ - - - - - - - ------ (7-72)

Ke L3

,

, r

-rl 0 0

: l 0 0 0 -12 -6L

,

, 0 12 -6L 2L2

:

,

,, 0 -6L

0 6L 4L2

where the dimensionless ratio rl represents the term AL2/I = AxL2/Iz. This

###### 6 x 6 array corresponds to the plane frame member stiffness matrix SM formember axes given in Table 4-26.

![image 619](Matrix Analysis of Framed Structures_images/imageFile619.png)

466 Chapter 7 Finite-Element Method for Framed Structures

Similarly, a grid member may be modeled using the torsional and the flexural elements. When the stiffness matrices from those two elements are expanded, rearranged, and combined, the results are

r2L2 0 0 -r2L2 0 0

,

,

,, ,, ,

0 4L2 -6L

0 2L2 6L

###### 0 -6L 12 ,,, 0 -6L -12 EI

,,

K=-e L3 ----------------------------,-------------------------, -- (7-73) -r2L2 0 0 r2L2 0 0

###### 0 2L2 -6L 0 4L2 6L 0 6L -12 0 6L 12

in which the dimensionless ratio r2 is GJ EI = GlxlEly. To form this 6 X 6 matrix, sign changes are required because the second nodal rotation (about the YM axis) is in the opposite sense from that for the flexural element (compare Figs. 4-32b and 7-5a). The array in Eq. (7-73) is the same as that for the grid member stiffness matrix for member axes (see Table 4-37), except that the symbols J and I are replaced by Ix and Iy.

Finally, the stiffness matrix for a space frame member may be duplicated by expanding, rearranging, and combining those for an axial element, a torsional element, and two cases of flexural elements (in two orthogonal principal planes of bending). By this approach, the following 6 X 6 stiffness submatrices are obtained:

rt/Z 0 0 0 0 0

0 12/z 0 0 0 6LIz E 0 0 121y 0 -6LIy 0

KeJJ.. =-L3 0 0 0 r2L21y 0 0 (7-74a) 0 0 -6LIy 0 4L21y 0 0 6LIz 0 0 0 4L2/z

and

-rt/Z 0 0 0 0 0

0 -12/z 0 0 0 6LIz T E 0 0 -I21y 0 -6Lly 0

Kejk = Kekj = L3

0 0 0 -r2L21y 0 0 0 0 6LIy 0 2L2/y 0 0 -6LIz 0 0 0 2L2/z

(7-74b)

![image 620](Matrix Analysis of Framed Structures_images/imageFile620.png)

References 467 and

rJ/z 0 0 0 0 0

0 12/z 0 0 0 -6Llz E 0 0 12Iy 0 6Lly

0 0

(7-74c)

Kekk = L3

0 0 0 r2L21y 0

###### 0 0 6Lly 0 4L21y 0 0 -6Llz 0 0 0 4L2/z

These submatrices are the same as those in Table 4-1, except that Iz and 1y replace 1 to denote the two orthogonal directions. Again, sign changes are needed when forming the submatrices in Eqs. (7-74), as stated previously for the grid member.

From the preceding discussion of member stiffness matrices, the reader should see how the analysis of framed structures fits into the finite-element approach. Formulations of equivalent nodal loads using displacement shape functions appear in Ref. [2] and need not be repeated here. Once the stiffness and load matrices for members are formed, the analysis proceeds as described previously in Chapter 4.

References

- 1. Weaver, W., Jr., and Johnston, P. R., Finite Elements for Structural Analysis, PrenticeHall, Englewood Cliffs, New Jersey, 1984.
- 2. Weaver, W., Jr., and Johnston, P. R., Structural Dynamics by Finite Elements, PrenticeHall, Englewood Cliffs, New Jersey, 1987.
- 3. Zienkiewicz, O. C., and Taylor, R., The Finite Element Method, 4th ed., McGraw-Hili, New York, 1989.
- 4. Cook, R. D., Concepts and Applications ofFinite Element Analysis, 2nd ed., Wiley, New York, 1981.
- 5. Timoshenko, S. P., and Goodier, J. N., Theory ofElasticity, 3rd ed., McGraw-Hill, New York, 1970.


![image 621](Matrix Analysis of Framed Structures_images/imageFile621.png)

###### General References

###### Textbooks on Matrix Analysis of Structures (Chronological Order)

- I. Beaufait, F. W., Rowan, W. H., Jr., Hoadley, P. G., and Hackett, R. M., Computer Methods of Structural Analysis, Prentice-Hall, Englewood Cliffs, New Jersey, 1970.

- 2. Rubinstein, M. F., Structural Systems-Statics, Dynamics, and Stability, Prentice-Hall, Englewood Cliffs, New Jersey, 1970.
- 3. Wang, C. K., Matrix Methods of Structural Analysis, 2nd ed., International, Scranton, Pennsylvania, 1970.
- 4. Meek, J. L., Matrix Structural Analysis, McGraw-Hill, New York, 1971.
- 5. Kardestuncer, H., Elementary Matrix Analysis of Structures, McGraw-Hill, New York, 1974.
- 6. Vanderbilt, M. D., Matrix Structural Analysis, Quantum, New York, 1974.
- 7. McGuire, W., and Gallagher, R. H., Matrix Structural Analysis, Wiley, New York, 1979.
- 8. Meyers, V. J., Matrix Analysis ofStructures, Harper and Row, New York, 1983.
- 9. Holzer, S. H., Computer Analysis of Structures, Elsevier, New York, 1985.
- 10. Bhatt, P., Programming the Matrix Analysis of Skeletal Structures, Wiley, New York, 1986.


- II. Fleming, J. F., Computer Analysis ofStructural Systems, McGraw-Hill, New York, 1989.


###### Textbooks on Finite Elements (Chronological Order)

- I. Gallagher, R. H., Finite Element Analysis Fundamentals, Prentice-Hall, Englewood Cliffs, New Jersey, 1975.


- 2. Bathe, K. J., and Wilson, E. L., Numerical Methods in Finite Element Analysis, PrenticeHall, Englewood Cliffs, New Jersey, 1976.
- 3. Hinton, E., and Owen, D. R. J., Finite Element Programming, Academic Press, London, 1977.
- 4. Desai, C. S., Elementary Finite Element Method, Prentice-Hall, Englewood Cliffs, New Jersey, 1979.
- 5. Cheung, Y. K., and Yeo, M. F., A Practical Introduction to Finite Element Analysis, Pitman, London, 1979.
- 6. Hinton, E., and Owen, D. R. J., An Introduction to Finite Element Computations, Pineridge Press, Swansea (UK), 1979.
- 7. Owen, D. R. J., and Hinton, E., Finite Elements in Plasticity, Pineridge Press, Swansea (UK), 1980.
- 8. Cook, R. D. Concepts and Applications ofFinite Element Analysis, 2nd ed., Wiley, New York, 1981.


468

![image 622](Matrix Analysis of Framed Structures_images/imageFile622.png)

###### General References 469

9. Becker, E. B., et aI., Finite Elements, (five volumes) Prentice-Hall, Englewood Cliffs, New Jersey, 1981 to 1984.

10. Bathe, K. J., Finite Element Procedures in Engineering Analysis, Prentice-Hall, Englewood Cliffs, New Jersey, 1982.

- II. Huebner, K. H., The Finite Element Method for Engineers, 2nd ed., Wiley, New York, 1983.


- 12. Weaver, W., Jr., and Johnston, P. R., Finite Elements for Structural Analysis, PrenticcHall, Englewood Cliffs, New Jersey, 1984.
- 13. Reddy, 1. N., An Introduction to the Finite Element Method, McGraw-Hill, New York, 1984.
- 14. Segerlind, L. J., Applied Finite Element Analysis, 2nd ed., Wiley, New York, 1985.
- 15. Yang, T. Y., Finite Element Structural Analysis, Prentice-Hall, Englewood Cliffs, New Jersey, 1986.
- 16. Hughes, T. 1. R., The Finite Element Method, Prentice-Hall, Englewood Cliffs, New Jersey, 1987.
- 17. Weaver, W., Jr., and Johnston, P. R., Structural Dynamics by Finite Elements, PrenticeHall, Englewood Cliffs, New Jersey, 1987.
- 18. Zienkiewicz, O. C., and Taylor, R., The Finite Element Method, 4th ed., McGraw-Hill, New York, 1989.


![image 623](Matrix Analysis of Framed Structures_images/imageFile623.png)

###### Notation

###### Table N-J

Matrices Used in the Flexibility Method (Sees. 2.1-2.5)

Matrix Order

Definition

Q q x q x q x

Unknown redundant actions (q = number of redundants) Displacements in the actual structure corresponding to the redundants

Displacements in the released structure corresponding to the redundants and due to loads

F q X q

Displacements in the released structure corresponding to the redundants and due to unit values of the redundants (flexibility coefficients)

q x 1

Displacements in the released structure corresponding to the redundants and due to temperature, prestrain, and restraint displacements (other than those in DQ)

DQC = DQL + DQT + DQP + DQR

qX jX jX jXq

Joint displacements in the actual structure (j = number ofjoint displacements) Joint displacements in the released structure

due to loads Joint displacements in the released structure due to unit values of the redundants

j x 1

Joint displacements in the released structure due to temperature, prestrain, and restraint displacements (other than those in DQ)

DJC = DJL + DJT + DJp + DJR

jx

Member end-actions in the actual structure

mX mX

(m = number of end-actions)

Member end-actions in the released structure due to loads Member end-actions in the released structure due to unit values of the redundants

mXq

r x r x

Reactions in the actual structure (r = number ofreactions) Reactions in the released structure due to loads Reactions in the released structure due to unit values of the redundants

r x q

470

![image 624](Matrix Analysis of Framed Structures_images/imageFile624.png)

Table N-2

Matrices Used in the Fonnalized Flexibility Method (Sees. 2.6-2.7)

Matrix

Definition

Flexibilities at k end of member i (in member directions) Actions at k end of member i (in member directions) Displacements at k end of member i relative to j end (in member

F~1i

- A~li D~li

As

A,j

A(l

- B~ls B~!'j B:w, Ds D,J


di rections) Unassembled flexibility matrix (in member directions) Actions at k ends of all members (in member directions) Displacements at k ends of all members relative to j ends (in

member directions) Actions in structural directions Actions at joints Redundant actions Actions A~I due to unit actions As Actions A~I due to unit actions AJ Actions AM due to unit actions A(l Displacements in structural directions Displacements at joints Displacements corresponding to redundants Assembled flexibility matrix

###### D"

Fs F,J,J

Displacements DJ due to unit actions AJ Displacements DJ due to unit actions A" Displacements D(l due to unit actions A,J Displacements D" due to unit actions A" Fixed-end actions (in member directions) Reactions AR due to unit actions As Reactions AR due to unit actions A.I Reactions AR due to unit actions A(l Combined loads applied at supports

###### FJ"

F(l,J F',(l

AMF

BRS

BRJ BR(l ARc

![image 625](Matrix Analysis of Framed Structures_images/imageFile625.png)

###### 472 Notation

###### Table N-3

Matrices Used in the Stiffness Method (Sees. 3.1-3.4)

Matrix D

Order

Definition Unknown joint displacements (d = number of

d x 1 d x 1 d x 1

displacements) Actions in the actual structure corresponding to the unknown displacements

All

Actions in the restrained structure corresponding to the unknown displacements and due to all loads except those that correspond to the unknown displacements

AIlL

d x d

Actions in the restrained structure corresponding to the unknown displacements and due to unit values of the displacements (stiffness coefficients)

S

d x 1

Actions in the restrained structure corresponding to the unknown displacements and due to temperature, prestrain, and restraint displacement

Aoc = AOL + AOT + AIlP + AOR Member end-actions in the actual structure

d x 1 m x 1 m x 1

(/11 = number of end-actions)

Member end-actions in the restrained structure due to all loads except those that correspond to the unknown displacements Member end-actions in the restrained struc-

A'IL

mxd

ture due to unit values of the displacements

m x 1

Member end-actions in the restrained structure due to temperature, prestrain, and restraint displacement

A'ic = A'IL + A'IT + A'IP + A'IR Reactions in the actual structure (r = number

mX

r x

of reactions)

r x

Reactions in the restrained structure due to all loads except those that correspond to the unknown displacements

r x d r x 1

Reactions in the restrained structure due to unit values of the displacements

Reactions in the restrained structure due to temperature, prestrain, and restraint displacement

r x 1

An!' = ARL + AnT + AnI' + ARn

![image 626](Matrix Analysis of Framed Structures_images/imageFile626.png)

###### Table N-4

Matrices Used in the Formalized Stiffness Method (Sees. 3.5-3.6)

Matrix

Definition

Stiffnesses at k end of member i (in member directions) Actions at k end of member i (in member directions) Displacements at k end of member i relative to j end (in member

directions) Unassembled stiffness matrix (in member directions) Actions at k ends of all members (in member directions) Displacements at k ends of all members relative to.i ends (in

member directions) Displacements at all joints Free joint displacements Restrained joint displacements Displacements DM due to unit displacements DJ Displacements DM due to unit displacements DF Displacements DM due to unit displacements DR Actions at all joints Actions at free joints Reactions at restrained joints Assembled joint stiffness matrix Actions AF due to unit displacements DF Actions AF due to unit displacements DR Reactions AR due to unit displacements DF Reactions AR due to unit displacements DR Member end-actions due to loads (in member directions) Combined loads applied at supports

DJ

DF DR

CM.) CMF

C~!H

AJ

###### A,

AR

SJ

SFF SFR SRF SRR

AMI,

ARC

![image 627](Matrix Analysis of Framed Structures_images/imageFile627.png)

474 Notation

Table N-S

Matrices Used in the Computer-Oriented Direct Stiffness Method (Chapters 4, 5, and 6)

Matrix Definition

Member stiffnesses (for both ends of member i) in directions of

member axes Submatrix jj of SMi Submatrix jk of SM i Submatrix kj of SMi Submatrix kk of SMi Member stiffnesses (for both ends of member i) in directions of

SM;;

SM;k SMk; SMkk

SMSi

structural axes Fixed-end actions (for both ends of member i) in directions of structural axes Displacements (for both ends of member i) in directions of

structural axes Equivalent joint loads Combined joint loads Combined joint loads corresponding to DF Combined joint loads corresponding to DR Rotation matrix for member i Rotation transformation matrix for member i Joint displacements at ends of member i End-actions (for both ends of member i) in member directions, due

###### AE

Ac

AFC

ARC

###### Ri RTi

DJi

AMDi

to joint displacements Support reactions due to joint displacements Transfer matrix for fixed-end actions due to unit values of

concentrated loads Concentrated loads at point I between the ends of member i Rotation transformation matrix for structure

At;

RR

- Actions at point p
- Actions at point q Translation-of-axes transformation matrix


Ap

Aq

Tpq

- Displacements at point p
- Displacements at point q Specialization of Tpq to points j and k


###### Dp Dq

T;k

- Flexibilities for j end of member i (in member directions)
- Flexibilities for k end of member i (in member directions) Flexibilities for tend of segmentj{(in member directions) Flexibilities for t end of segmentlk (in member directions) Actions {Ap, Aq} for rigid bodies Displacements {Dp, Dq} for rigid bodies Combined translation-of-axes operator Constraint matrix for frames Vector of axial forces in frames


FM;;

FMkk

Falt

FbU

AMB DMB

T

C

Q

![image 628](Matrix Analysis of Framed Structures_images/imageFile628.png)

Table N-6

Matrices used in Chapter 7 and Appendix D

Definition

Matrix

- o

- A
- B
- C
- D
- E K S T U


- X
- Y
- Z b d r


- p
- q u


Null matrix Action vector (also coefficient matrix) Strain-displacement matrix (and vector of constants) Strain-stress matrix Displacement vector Stress-strain matrix Element stiffness matrix Stiffness matrix Transformation matrix Upper triangular matrix Vector of unknowns Vector of unknowns Vector of unknowns Vector of body forces for element Linear differential operator for strain-displacement relationships Matrix of displacement shape functions Nodal load vector for element Nodal displacement vector for element Displacement vector for any point on an element

![image 629](Matrix Analysis of Framed Structures_images/imageFile629.png)

A

###### Displacements of Framed Structures

A.I Stresses and Deformations in Slender Members. Whenever a load is applied to a structure, stresses will be developed within the material, and defonnations will occur. Defonnation means any change in the shape of some part of the structure, such as a change in shape of an infinitesimal element cut from a member, while stresses refer to the distributed actions that occur internally between such adjoining elements. It is assumed in subsequent analyses that the defonnations are very small and that the material is linearly elastic (Hooke's law). Under these conditions the stresses are proportional to the corresponding strains in the material, and the principle of superposition may be used for combining stresses, strains, and defonnations due to various load systems.

The principal types of defonnations to be considered are axial, flexural, torsional, and shearing defonnations. These are caused by the corresponding stress resultants, which are axial forces, bending moments, torsional moments, and shearing forces, respectively. In each of these four cases the expressions for the stresses acting on the cross section, the strains in an element, and the defonnation of an element are summarized in this section. In addition, defonnations caused by temperature effects are described.

The calculation of displacements in structures is described in Sections A.2 and A.3. This subject is an important part of the flexibility method of analysis (see Chapter 2), and is presented in this Appendix for review purposes. Further infonnation on the subject may be found in textbooks on mechanics of materials and elementary theory of structures.

Axial Deformations. The slender member shown in Fig. A-la is assumed to be acted upon by a tensile force P at each end. The member will be in pure tension due to these forces, provided each force acts at the centroid of the cross-sectional area. At any distance x from the left end the tensile stress ax on the cross section is

P

x A (A-I)

a =-

in which A is the cross-sectional area. The axial strain Ex in the member is equal to the stress divided by the modulus of elasticity E of the material. Hence,

476

![image 630](Matrix Analysis of Framed Structures_images/imageFile630.png)

477

A.I Stresses and Deformations in Slender Members

![image 631](Matrix Analysis of Framed Structures_images/imageFile631.png)

![image 632](Matrix Analysis of Framed Structures_images/imageFile632.png)

k----- L ----~ 6

(0 )

Fig. A-1. Axial deformations.

P EA

(A-2)

E

The quantity EA is called the axial rigidity of the member.

The change in length dt1 of an element of initial length dx is indicated in Fig. A-I b and is given by the formula

P

dt1 = E.I' dx = EA dx (A-3)

The total elongation t1 of the member shown in Fig. A-la is obtained by integration of dt1 over the length L, as follows:

###### t1 = Jdt1 = lL.!:....dx

(A-4)

o EA

If the member is prismatic and E is constant, the integration of Eq. (A-4) gives

t1 = PL

(A-5)

EA

This equation can be used to calculate the change in length of a prismatic member subjected to a constant axial force.

If the axial force P varies along the length of the member, Eq. (A-4) can still be used. All that is necessary is to express P as a function of x and then perform the integration. If the member is tapered slightly, then A must be expressed as a function of x, after which the integration can be carried out.

Flexural Deformations. A member subjected to pure bending moment produced by couples M acting at each end is shown in Fig. A-2a. It is assumed that the plane of bending (the x-y plane) is a plane of symmetry of the beam, and hence the y axis is an axis ofsymmetry of the cross-sectional area (see Fig. A-2b). This requirement also means that the y and z axes are principal axes through point 0, which is selected at the centroid of the cross section. With the bending moments M acting as shown in Fig. A-2, it

![image 633](Matrix Analysis of Framed Structures_images/imageFile633.png)

478 Appendix A: Displacements of Framed Structures

![image 634](Matrix Analysis of Framed Structures_images/imageFile634.png)

y~zTJ

![image 635](Matrix Analysis of Framed Structures_images/imageFile635.png)

Ib)

(0)

![image 636](Matrix Analysis of Framed Structures_images/imageFile636.png)

![image 637](Matrix Analysis of Framed Structures_images/imageFile637.png)

~------- L --------~

Ie) Id)

Fig. A-2. Flexural deformations.

follows that all displacements of the beam will be in the x-y plane. If the cross section of the beam is not symmetric about the y axis, the bending analysis becomes more complicated because bending will no longer occur in a single plane. It then becomes necessary to take the origin 0 at the shear center ofthe cross section and to take the y and zaxes parallel to the principal centroidal axes. Then the beam is analyzed for bending in both principal planes, as well as for torsion; and the results are combined to give the final stresses and displacements.

At any cross section of the beam the flexural stress (Jx is given by the formula

My

###### (A-6)

(Jx =

###### Iz

in which y is the distance from the neutral axis (the z axis) to any point A in the cross section (see Fig. A-2b), and Iz is the moment of inertia (or second moment) of the cross-sectional area with respect to the z axis. The flexural strain Ex at the same point is equal to the flexural stress divided by the modulus of elasticity; therefore,

(Jx My

Ex = E = Elz (A-7)

The minus sign appears in Eqs. (A-6) and (A-7) because positive bending moment M produces negative stresses (compression) in the region where y is positive.

The relative angle of rotation de between two cross sections is shown

![image 638](Matrix Analysis of Framed Structures_images/imageFile638.png)

A.I Stresses and Deformations in Slender Members 479

in Fig. A-2c. For small angles of rotation this angle can be found by dividing the shortening ab of a fiber at distance y from the neutral axis by the distance y itself. Since the distance ab is equal to -E,r dx, the expression for de becomes

Substitution of Eq. (A-7) into this equation results in

M

de = Elz dx (A-8)

The quantity Elz in the denominator is called the flexural rigidity of the beam.

Expression (A-8) can sometimes be used to calculate angles of rotation and displacements of beams. An example of this kind is shown in Fig. A-2d, where it is assumed that the left end A of the beam in pure bending is fixed to a support and does not rotate. The angle of rotation eof end B may be determined by integration of de (see Eq. A-8) along the length of the member. The expression for eis

###### e= Jdfl = JL~dx

(A-9)

o Elz

in which dx is the length ofthe small element mn of the beam. Ifthe member is prismatic and E is constant, integration ofEq. (A-9) gives the following expression for the angle at B for pure bending:

###### e=-MLElz (A-to)

However, Eq. (A-9) may also be used with good accuracy for cases in which the bending moment varies along the beam or in which the member is slightly tapered. The procedure is to substitute the appropriate expressions for M and lz into Eq. (A-9) before performing the integration.

The deflection Il at end B of the beam (Fig. A-2d) is seen to consist of the summation of the small distances dll, each of which is an intercept on the vertical through B of the tangent lines from points m and n. Thus, for small angles of rotation the intercept dIl is

dll = (L - x)de

or, using Eq. (A-8),

M

(A-II)

dll = (L - x) - dx

Elz

![image 639](Matrix Analysis of Framed Structures_images/imageFile639.png)

480 Appendix A: Displacements of Framed Structures

Integration over the length of the member gives the total displacement ~ for a prismatic beam, as follows:

~ =Jd~ = fl> (L - x) M dx =_MP

(A-12)

o EIz 2EIz

This example for a beam in pure bending requires only very simple calculations in order to find the displacement. The same technique can be used if either M or the flexural rigidity EIz varies along the length. Under more general conditions it is necessary to use other methods for determining displacements of beams, such as the unit-load method described in Art. A.2.

Torsional Deformations. The deformations caused by pure torsion of a member having a circular cross section are illustrated in Fig. A-3. The member has a length L and is subjected to twisting moments T at its ends, as indicated by the double-headed arrows in Fig. A-3a. The deformation of an element located at distance x from one end of the member (Fig. A-3b) consists of a relative rotation about the x axis of one cross section with respect to another. The relative angle of rotation is denoted by dcj> in the figure.

Associated with the deformation are shearing stresses T and shearing strains y. The torsional shearing stresses are directly proportional to the distance from the longitudinal axis; and, at a distance r from the axis (see Fig. A-3b), the stress intensity is given by the formula

Tr

(A-13)

T=-

J

The term J is the polar moment of inertia of the circular cross section; thus, J is equal to 7rR4/2, where R is the radius of the member. The maximum shearing stress occurs at the outer surface of the member and is obtained from the formula

###### TR

###### Tmax = J (A-14)

The shearing stresses acting on the circular cross sections are always in a

![image 640](Matrix Analysis of Framed Structures_images/imageFile640.png)

![image 641](Matrix Analysis of Framed Structures_images/imageFile641.png)

T T T

z

(0 ) (b)

###### Fig. A-3. Torsional deformations.

![image 642](Matrix Analysis of Framed Structures_images/imageFile642.png)

A.I Stresses and Deformations in Slender Members 481

tangential direction (normal to the radius) and in the same sense as the torque T.

The shearing strain 'Y at the radius r is equal to the shearing stress divided by the shearing modulus of elasticity G of the material; therefore,

T Tr

(A-IS)

y=--=-

###### G GJ

The expression for the maximum shearing strain (see Fig. A-3b) is

###### TR

(A-I6)

Ymax = GJ

The quantity GJ appearing in this formula is called the torsiol1ul rigidity of the member.

The relative angle of rotation d¢ between the cross sections of the ele· ment in Fig. A-3b is

d¢ = YmaxR dl.

as can be seen from the geometry of the figure. This expression takes the following form when Eq. (A-I6) is substituted:

T

d¢ = - dx

(A-17)

GJ

From Eq. (A-I7) the total angle of twist ¢ (see Fig. A-3a) can be found by integration of d¢ over the length of the member. The result is

###### J fl. T

(A-IS)

###### ¢= d¢= -dx

o GJ

which for a cylindrical member with constant torque T becomes

(A-I9)

All of the formulas given above may be used for either a solid or a tubular circular member. Of course, in the latter case J must be taken equal to the polar moment of inertia of the annular cross section.

It should be noted that Eq. (A-IS) may be used for a member that is subjected to a torque Tthat varies along its length. It may also be used when J varies, provided the variation is gradual over the range of integration. In either of these cases the expression for Tor J as a function ofx is substituted into Eq. (A-IS) before the integration is performed.

If the cross section of the member is not circular or annular, the torsional analysis is more complicated than the one described above. However, for

![image 643](Matrix Analysis of Framed Structures_images/imageFile643.png)

482 Appendix A: Displacements of Framed Structures

pure torsion, for which the twisting moment T is constant along the length, the formula for the angle of twist (see Eq. A-19) can still be used with good accuracy, provided that J is taken as the appropriate torsion constant for the particular cross section. Torsion constants for several shapes ofcross sections are tabulated in Appendix C.

Ifthe cross section of the bar is not circular, there will be warping of the cross sections. Warping refers to the longitudinal displacement of points in the cross section, so that it is no longer planar. Warping occurs in the case of I beams and channel beams, as well as most other sections, and a more complicated analysis can be made. However, in such cases it is usually found that the analysis based upon pure torsion alone, with the warping effects neglected, gives acceptable results. Torsion in which warping occurs is called nonuniform torsion [1].

Shearing Deformations. There are usually shearing forces as well as bending moments acting on the cross sections of a beam. For example, at distance x from the fixed support of the cantilever beam shown in Fig. A-4a, there will be a bending moment M (assumed positive when the top of the beam is in compression) given by the equation

M = -P(L - x) (A-20)

The positive direction for M is shown in Fig. A-4b, which shows an element of length dx from the beam. The shearing force V is constant throughout the length of the beam and is

###### V=P (A-21)

It is assumed that a positive shearing force is downward on the right-hand side of the element and upward on the left-hand side (see Fig. A-4b). In a more general case, the shearing force Vas well as the bending moment M will vary along the length of the beam.

The shearing stresses on the cross section of a beam with rectangular cross section, due to a shearing force V, can be found from the formula

###### VQ

###### 7 = Izh (A-22)

in which Q is the first moment about the neutral axis of the portion of the

# laG,

###### I T tv

l I

###### ~dX~ .

(0 ) (b) (e)

Fig. A-4. Shearing deformations.

![image 644](Matrix Analysis of Framed Structures_images/imageFile644.png)

A.I Stresses and Deformations in Slender Members 483

cross-sectional area that is outside of the section where the shearing stress is to be detennined; /z is the moment of inertia of the cross-sectional area about the neutral axis; and b is the width of the rectangular beam. Equation (A-22) can be used to find shearing stresses in a few other shapes of beams; for example, it can be used to calculate the shearing stresses in the web of an / beam, provided that b is taken as the thickness of the web of the beam. On the other hand, it cannot be used to calculate stresses in a beam of circular cross section. The shearing strain 'Y can be found by dividing the shearing stress 7 by the shearing modulus of elasticity G.

Previously, the defonnation of an element of a beam due solely to the action of bending moments was considered (see Fig. A-2c). In the present discussion, only the defonnations caused by the shearing forces V will be taken into account. These defonnations consist of a relative displacement d"A of one face of the element with respect to the other (see Fig. A-4c). The displacement d"A is given by the expression

Vdx

###### d"A =f-GA (A-23)

in which A is the area of the cross section andf is a fonn factor [2] that is dependent upon the shape of the cross section. Values of the fonn factor for several shapes of cross section are given in Appendix C. The quantity GA /f is called the shearing rigidity of the bar.

The presence of shearing defonnations d"A in the elements of a beam means that the total displacement at any other point along the beam will be influenced by both flexural and shearing defonnations. Usually, the effects of shear are small compared to the effects of bending and can be neglected; however, if it is desired to include the shearing defonnations in the calculations ofdisplacements, it is possible to do so by using the unit-load method, as described in Sec. A.2.

In a few elementary cases the deflections due to shearing defonnations can be calculated by a direct application of Eq. (A-23). This equation can be used, for example, to calculate the deflection d at the end of the cantilever beam in Fig. A-4a. The portion d s of the total deflection that is due solely to the effect of shearing deformations is equal to (see Eqs. A-21 and A-23)

f fP [L fPL

ds = d'A = GA Jo dx = GA (A-24)

The remaining part db of the deflection is due to bending and can be found by integrating Eq. (A-ll). However, Eq. (A-ll) was derived on the basis that upward deflection d was positive, whereas in Fig. A-4a the deflection d is downward. Thus, it is necessary to change the sign of the expression appearing in Eq. (A-ll); the result is

![image 645](Matrix Analysis of Framed Structures_images/imageFile645.png)

484 Appendix A: Displacements of Framed Structures

a" = JL - (L - x) M dx

###### o Elz

The bending moment M for the beam is given by Eq. (A-20) and, when this expression is substituted into the above equation, the following result is obtained:

###### a" -_ JL0 (L -ElX)2z P dx -_ 3ElPVz

(A-25)

Summing the deflections due to both bending and shearing deformations gives the total deflection a, as follows:

###### PV fPL

###### a = a" + as = 3Elz + GA (A-26)

From this equation it is found that the ratio of the shearing deflection to the bending deflection is 3fElzIGAL2. This ratio is very small compared to unity except in the case of short, deep beams; hence, in most cases it can be omitted.

Temperature Deformations. When the temperature of a structure varies, there is a tendency to produce changes in the shape of the structure. The resulting deformations and displacements may be of considerable importance in the analysis of the structure. In order to obtain formulas for the deformation due to temperature changes, consider the member shown in Fig. A-5a. A uniform temperature change throughout the member results in an increase in its length by the amount

a = cv.LI:!.T (A-27)

in which I:!. is the change in length (positive sign denotes elongation); cv. is the coefficient of thermal expansion; L is the length of the member; and I:!. T is the change in temperature (positive sign means increase in temperature). In addition, all other dimensions of the member will be changed proportionately, but only the change in length will be of importance for the analysis of framed structures.

(0 ) (b) (c)

###### Fig. A-5. Temperature deformations.

![image 646](Matrix Analysis of Framed Structures_images/imageFile646.png)

A.2 Displacements by the Unit-Load Method 485

The deformation of an element of the member of length dx (Fig. A-5a) will be analogous to that for the entire member. The longitudinal deformation of the element is shown in Fig. A-5b and is seen to be of the same type

- as that caused by an axial force (see Fig. A-lb). This deformation is given by the expression


###### dfl = afl T dx (A-28)

Equation (A-28) can be used when calculating displacements of structures due to uniform temperature changes, as described in the next section.

A temperature differential between two surfaces of a beam causes each element of the member to deform as shown in Fig. A-5c. If the temperature change varies linearly between fl T2 at the top of the beam and a higher value fl TI at the bottom of the beam, the cross sections of the member will remain plane, as illustrated in the figure. The relative angle of rotation d() between the sides of the element is

d() = _a--,--(fl_T---,I_-_fl_T--=2,,---)dx_

(A-29)

d

in which d is the depth of the beam. The deformation represented by the angle d() in Eq. (A-29) is similar to that caused by bending moments acting on the member (see Fig. A-2c). The use of Eq. (A-29) for finding beam displacements will be shown also in Sec. A.2.

The formulas in the preceding paragraphs have been presented for reference use in the solution of problems and examples throughout this book. For a more complete treatment of stresses and deformations, a textbook on mechanics of materials should be consulted.

A.2 Displacements by the Unit-Load Method. The unit-load method derived in Sec. 1.14 is a very general and versatile technique for calculating displacements of structures. It may be used (in theory) for either determinate or indeterminate structures, although for practical calculations it is applied almost exclusively to statically determinate structures because its use requires that the stress resultants be known throughout the structure. The method may be used to determine displacements caused by loads on a structure, as well as displacements caused by temperature changes, misfit of parts, and other influences. The effects of axial, flexural, shearing, and torsional deformations may be included in the calculations.

In this section the unit-load method is applied to framed structures, and several numerical examples are solved. It is assumed throughout the discussion that the displacements of the structures are small and that the material is linearly elastic.

Two systems of loading must be considered when using the unit-load method. The first system consists of the structure in its actual condition; that is, subjected to the actual loads, temperature changes, or other effects. The second system consists of the same structure subjected to a unit load

![image 647](Matrix Analysis of Framed Structures_images/imageFile647.png)

corresponding to the desired displacement in the actual structure. The unit load is a fictitious or dummy load and is introduced solely for purpose~ of analysis. By a unit load corresponding to the displacement is meant a load

- at the particular point of the structure where the displacement is to be determined and acting in the positive direction of that displacement. The term "displacement" is used here in the generalized sense, as discussed in Sec. 1.4. That is, a displacement may be the translation of a point on the structure, the angle of rotation of the axis of a member, or a combination of translations and rotations. If the displacement to be calculated is a translation, then the unit load is a concentrated force at the point where the displacement occurs. In addition, the unit load must be in the same direction as the displacement and have the same positive sense. If the displacement to be calculated is a rotation, then the unit load is a moment at the point where the rotation occurs and is assumed positive in the same sense as a positive rotation. Similarly, if the displacement is the relative translation of two points along the line joining them, the unit load consists of two collinear and oppositely directed forces acting at the two points; and if the displacement is a relative rotation between two points, the unit load consists of two equal and oppositely directed moments at the points.


In Sec. 1.14 the principle of complementary virtual work was specialized to the unit-load method [see Eq. (1-43)], which may be stated in words as

(unit virtualload)(unknown displacement)

=Iv(virtualstresses)(realstrains)dV

where the left-hand side is external work and the right-hand side is internal work. For the slender members of framed structures, however, integration over volume may be replaced by integration over length by working with virtual stress resultants and the corresponding internal displacements. The virtual stress resultants caused by the unit load will be represented by the symbols N u, M u, Tu, and V u, denoting the axial force, bending moment, twisting moment, and shearing force, respectively, at any cross section in the members of the structure.

The corresponding incremental displacements will be denoted as dfl for axial deformation (see Fig. A-1b), de for flexural deformation (Fig. A-2c), de/> for torsional deformation (Fig. A-3b), and d>--.. for shearing deformation (Fig. A-4c). Thus, the internal work of the virtual stress resultants and the corresponding incremental displacements for an infinitesimal element may be written as

N ud6. + M "de+ T ude/> + V ud>--..

The first term in this expression is the work done by the axial force N u (produced by the unit load) when the displacement dfl (due to the actual loads or other effects) is imposed on the element. A similar statement can

![image 648](Matrix Analysis of Framed Structures_images/imageFile648.png)

A.2 Displacements by the Unit-Load Method 487

be made about each of the other terms. Then the total work of the virtual internal actions is

.~ (I Nud!:. + rMudO + r Tud¢> + r vud'A.)

###### I= I L JL JL JL i

in which m = number of members. Integrations are carried out over the lengths of all members of the structure.

The external work done by the unit load is

(l)/:,.

in which /:,. represents the desired unknown displacement. Equating the work of the external and internal actions gives the equation of the unit-load method for framed structures as

Because the unit load has been divided from the left-hand side of Eq. (A-30), leaving only the term /:,., it is necessary to consider the quantities N[:, Me, Te, and Vc as having the dimensions of force or moment per unit of the applied unit load.

The quantities d/:,., de, d¢>, and d1l. appearing in Eq. (A-30) can be expressed in terms of the properties of the structure. The expression for d/:" when the axial deformations are caused by loads only is (compare with Eq. A-3)

d/:" = NLdx EA

in which N L represents the axial force in the member due to the actual loads on the structure. Similarly, if the deformations are caused by a uniform temperature increase, the expression for d/:" is (see Eq. A-28)

d!:. = ex.!:.T dx

in which ex. is the coefficient of thermal expansion and!:. T is the temperature change. The expressions for the remaining deformation quantities due to loads (compare with Eqs. A-8, A-17, and A-23) are

d _ hdx

d1l. = IVLdx

cP - GJ

GA

The quantIties ML, TL, and VL represent the bending moment, twisting moment, and shearing force caused by the loads. If there is a temperature

![image 649](Matrix Analysis of Framed Structures_images/imageFile649.png)

differential across the beam, Eq. (A-29) can be used for the deformation

###### dO.

When the relations given above for the deformations due to loads only are substituted into Eq. (A-30), the equation for the displacement takes the form

###### i: (r NuNLdx + r MUMLdx + r TuTLdx + rJVuVLdx)

i= \ JL EA JL EI JL GJ JL GA i

(A-31)

Each term in this equation represents the effect ofone type ofdeformation on the total displacement ~ that is to be found. In other words, the first term represents the displacement caused by axial deformations; the second term represents the displacement caused by bending deformations; and so forth for the remaining terms. The sign conventions used for the quantities appearing in Eq. (A-31) must be consistent with one another. Thus, the axial forces N u and N L must be obtained according to the same convention; for example, tension is positive. Similarly, the bending moments Mu and ML must have the same sign convention, as also must T u and Tv and Vu

and VL• Only ifthe sign conventions are consistent will the displacement ~ have the same positive sense as the unit loa~.

The procedure for calculating a displacement by means of Eq. (A-31) is as follows: (1) determine forces and moments in the structure due to the loads (that is, obtain Nv Mv Tv and VL); (2) place a unit load on the structure corresponding to the displacement ~ that is to be found; (3) determine forces and moments in the structure due to the unit load (that is, find N u. Mu. Tu, and Vu); (4) form the products shown in Eq. (A-31) and integrate each term for the entire structure; and (5) sum the results to obtain the total displacement.

Usually, not all of the terms given in Eq. (A-31) are required for the calculation of displacements. In a truss with hinged joints and with loads acting only at the joints, there will be no bending, torsional, or shearing deformations. Furthermore, if each member of the truss is prismatic, the cross-sectional area A will be a constant for each member. In such a case the equation for A can be written as

###### A = .i: (NUNLL)

(A-32)

1=\ EA i

in which L represents the length of a member. The summation is carried out for all members of the truss.

In a beam it is quite likely that only bending deformations are important. Therefore, the equation for the displacement simplifies to

###### A= i: (r MUMLdx)

(A-33)

i= \ JL EI i

![image 650](Matrix Analysis of Framed Structures_images/imageFile650.png)

In an analogous manner it is possible to calculate displacements by using any appropriate combination ofterms from Eq. (A-31), depending upon the nature of the structure and the degree of refinement required for the analysis. Other terms can be used when displacements due to temperature changes, prestrains, etc., are to be found. All that is necessary is to substitute into Eq. (A-30) the appropriate expressions for the deformations. Some examples of the use of the unit-load method will now be given.

Example 1. The truss shown in Fig. A-6a is subjected to loads P and 2P at

- joint A. All members of the truss are assumed to have the same axial rigidity EA. The horizontal displacement .::11 of joint B (positive to the right) is to be found.


The calculations for the displacement .::11 by the unit-load method are given in Table A-I. The first two columns in the table identify the members of the truss and their lengths. The axial forces NL, which are determined by static equilibrium for the truss shown in Fig. A-6a, are listed in column (3) of the table. The unit load corresponding (0 the displacement .::11 is shown in Fig. A-6b, and the resulting axial forces NUl are given in column (4). Finally, the products NUINLL are obtained for each member (column 5), summed, and divided by EA. Thus, the displacement .::11 is (see Eq. A-32)

###### PL

Ll, = -3.828 EA

The negative sign in this result means that Ll, is in the direction opposite to the unit load (i.e., to the left).

A similar procedure can be used to find any other displacement of the truss. For example, suppose that it is desired to determine the relative displacement Ll2 of joints A and D (see Fig. A-6a) along the line joining them. The corresponding unit load consists of two unit forces, as shown in Fig. A-6c. The resulting axial forces N['2 in the truss are listed in column (6) ofTable A-I, and the products N['2NLL are given in column (7). Thus, the relative displacement ofjoints A and Dis

Ll PL

2 =-2 EA

in which the minus sign indicates that the distance between points A and D has increased (that is, it is opposite to the sense of the unit loads).

###### 2P

A B A

P._+-'---------j(

(a) (b) (c)

###### Fig. A-S. Examples 1 and 2.

![image 651](Matrix Analysis of Framed Structures_images/imageFile651.png)

###### Table A-I

Member Length NI. NL'I Nl'INL L NL'2 NC2NI. L

(1) (2) (3) (4) (5) (6) (7)

AB L P 0 0 -lIV2 -PLlV2 AC L -2P 0 0 -lIV2 2PLlV2 BD L P -1 -PL -lIV2 -PLlV2 CD L 0 0 0 -lIV2 0 CB V2L -V2P V2 -2V2PL 1 -2PL

-3.828PL -2PL

Example 2. Consider again the truss shown in Fig. A-6a, and assume now that member BD has been fabricated with a length that is greater by an amount e than the theoretical length L. The horizontal displacement ~, of joint B and the relative displacement ~2 between points A and D are to be determined (see Figs. A-6b and A-6c for the corresponding unit loads).

Any displacement of the truss caused by the increased length of member BD can be found by using Eq. (A-30) and retaining only the first term on the right-hand side. For a truss the equation may be expressed in the form

m

~ = I; [Nu(M)];

i=1

in which the summation is carried out for all members of the truss and M represents the change in length of any member. In this example the only member in the truss of Fig. A-6a that has a change in length is member BD itself; hence, there is only one term in the summation. For member BD, the term ~L is

AL = e

When finding the horizontal displacement ofjoint B. the force in member BD due to the unit load shown in Fig. A-6b is

Nn=-I

as given in the third line of column (4) in Table A-I. Therefore, the displacement of

- joint B is A, = -e


and is to the left.

When the decrease in distance between joints A and D due to the lengthening of member BD is to be found, the value for N U2 becomes

1

###### NU2 =-v'2

as given in column (6) ofTable A-I; therefore,

A,.=-~- v'2

The negative sign for ~2 shows that joints A and D move apart from one another.

![image 652](Matrix Analysis of Framed Structures_images/imageFile652.png)

A unifonn temperature change in one or more members of the truss is handled in the same manner as a change in length. The only difference is that the change in length M now is given by Eg. (A-27). Thus, the horizontal displacement of joint

- B due to a temperature increase of ~ T degrees in member BD becomes ~I = -c;L~T


and the change in distance between points A and D becomes

c;L~T

###### ~2 = - J2

Example 3. The cantilever beam AE shown in Fig. A-7a is subjected to loads at points B. C. D and E. The translational displacements Al and A2 of the beam (positive upward) at points C and E. respectively, are to be determined.

The displacements Al and A2 can be found from Eq. (A-33), which is expressed in terms of the bending moments MLand M [. The former moments are due to the actual loads on the beam, and the latter are due to unit loads corresponding to the desired displacements. Expressions for ML and Me must be obtained for each segment ofthe beam between applied loads, and then these expressions are substituted into Eq. (A-33) to obtain the displacements.

The required calculations are shown in Table A-2. The first two columns of the table list the segments of the beam and the limits for the distance x. which is measured from the fixed support. Column (3) gives the expressions for the bending moments in the beam due to the actual loads, assuming that compression on top of the beam corresponds to positive bending moment. The moments Mn in column (4) are those caused by a unit load at point C (Fig. A-7b). These moments are evaluated according to the same sign convention that was used in determining the moments ML• Next, column (5) shows the results ofevaluating the integral given in Eq. (A-33), except that the factor El has been omitted, since it is assumed to be the same for all segments ofthe beam. When the expressions in column (5) are summed, and the total is divided by El, the result is the displacement corresponding to the unit load. Therefore, the displacement at point C in the y direction is

(a)

###### ____________-r__________~E

~A C

###### tl

( b)

~A E

(c)

###### Fig. A-7. Example 3.

![image 653](Matrix Analysis of Framed Structures_images/imageFile653.png)

492 Appendix A: Displacements of Framed Structures

###### Table A-2

Unit Load at C Unit Load at E Seg- Limits

ment forx ML Ml'l fMn MLdx M("2 fM1'2 MLdx

-

(1) (2)

(4)

(5)

(6) (7)

(3)

###### 17PL:1

L

"'2P (4x +L)

41PV

AB 0

--

to -

--

L -x

2L -x

48

48

2

--3PL'1

Be -L to L 2

15PL" 2L -x --

3PL

--

L -x

16

16

2

3L

###### -PL

3PL"

--

to -

CD L

2L -x

0

0

16

2

2

PL'1 2L -x --

23L to 2L

DE

P(2L - x)

0

0

24

###### 97PV

###### 13PL"

--

---

48

24

13PV

.:l, = 24EI

and is in the positive direction of the y axis (upward).

The calculations for the translation at point E are also shown in Table A-2 (see columns 6 and 7). The unit load used in ascertaining the moments MU2 is shown in Fig. A-7c. The result of the calculations is

97PL3

.:l2 = 48EI

which, being positive, shows that the translation is in the direction of the y axis.

Example 4. In this example it is assumed that the beam shown in Fig. A-7a is now subjected to a linear temperature gradient such that the bottom of the beam has a temperature change ~ T" while the top of the beam has a change ~ T2 (see

- Fig. A-8). The formula for the displacements is obtained by using only the second term on the right-hand side of Eq. (A-30) and substituting for dO the expression given in Eq. (A-29). Thus,


_ rM a(~T, - ~T2)d.x

###### ~ - J U d

The expressions for Mu that are to be substituted into this equation are given in columns (4) and (6) of Table A-2, assuming that the vertical translations ~, and ~2 at points C and E are to be found. The calculations become as follows:

_ a(~T, - ~T2) rL d.x _ _a..:...(~_T.....:,_-_~_T.....:2:.:..)L_2

~, - d Jo (L - x) - 2d

These results show that if ~ T, is greater than ~ T2, the beam deflects upward.

![image 654](Matrix Analysis of Framed Structures_images/imageFile654.png)

A.4 Integrals of Products for Computing Displacements 493

!1T, !1T, !1 T,

~A

I- L .i~ !1:~E

Fig. A-S. Example 4.

The preceding examples illustrate the determination of translational displacements in trusses and beams due to various causes. Other types of structures can be analyzed in an analogous manner. Also, techniques that are similar to those illustrated can be used to find rotations at a point (the unit load corresponding to a rotation is a unit moment), as well as to obtain displacements due to shearing and torsional deformations, all of which are included in Eq. (A-30).

A.3 Displacements of Beams. In many of the problems and examples given in Chapters 1 and 2, it is necessary to determine displacements of beams. Such displacements can be found in all cases by the unit-load method, although other standard methods (including integration of the differential equation for displacements of a beam, and the moment-area method) may be suitable also. In most of the examples, however, the desired displacements can be obtained with the aid of the formulas given in Table A-3 for prismatic beams.

As an illustration of the use of the formulas, consider a cantilever beam with constant E1 that is subjected to a concentrated load P at its midpoint

(Fig. A-9). The displacement a at the end of the beam can be obtained readily by making the following observation: the displacement a is equal to the displacement at B plus the rotation at B times the distance from B to

- C. Thus, from Case 7 in Table A-3, the following expression is obtained:


###### a L (L):l 1 (L)2 1 L 5PV

###### = aB + 8n 2 = P 2 3E1 + P 2 2E12 = 48E1

Techniques of this kind can be very useful for finding displacements III beams and plane frames.

A.4 Integrals of Products for Computing Displacements. Equation (A-31) in Sec. A.2 provides a useful tool for calculating displacements in framed structures by the unit-load method. Evaluation of the integrals of products in that equation can become repetitious, however (see Example 3 in Sec. A.2), and it is possible to avoid much of the work by using a table of product integrals.

The members of framed structures are usually prismatic and have constant material properties along their lengths. In all such cases the rigidities may be taken outside of the integral signs, as follows:

###### a = ~fIl (1- ~ NuNLdx + -I ~ MUMLdx

i= I EA L EI L

+ _1 r TUTL dx + Gf" r VUVL dx) (A-34)

###### GJ JL /:I JL i

![image 655](Matrix Analysis of Framed Structures_images/imageFile655.png)

Table A-3

Displacements of Prismatic Beams

,-----------------------------

I Translations I

i (positive I Rotations

Beam I downward) 1 (positiye clockwise)

1-------------1

- 1 ACTJ ~jeWi I IJB I 5wL4 w£3

~ ~ I Ac = 384EI OA = -OB = 24EI

~L12 -I· L12~ I

- 2


r P£3 PU

A B Ac = 48EI OA = -OB = 16HI

###### e

1---------------1------1----------1

###### A _ 23P£3

###### c - 648EI

4 M

A .(\ B I Ac = 0 OA = OB = ::A~l I

###### 1__A_____~_____~____i______________1

- 5

A MQ

~~---~~----~~

- 6


! ML!

l ML2 OA = 6EI

I Ac = 16EI

o _ _AIL

I

1----

B - 3EI

II A--wf..4

1 B - 8EI

I-------------il------I----------I

I------r

- 7
- 8


###### ~A B

M

o _ "'IL

~-----CjB~A

B - EI

I

494

![image 656](Matrix Analysis of Framed Structures_images/imageFile656.png)

A.4 Integrals of Products for Computing Displacements 495

Fig. A-9.

The product integrals in this expression must be evaluated over the length of each member and then added for all members. For a structure in which only flexural deformations are considered, Eq. (A-34) reduces to

###### .1 =~ (.l rMUMLdx)

(A-35)

/=1 EI JL i

Table A-4 contains product integrals for the most commonly encountered functions (constant, linear, and quadratic). Although the results in the table are in terms of Mu and ML (see Eq. A-35), these functions can be replaced by any others, such as Nu and NL (see Eq. A-34).

To demonstrate the use of Table A-4, consider the simple beam in Fig. A-lOa, subjected to a uniformly distributed load of intensity w. The rotation (1B (taken as positive clockwise) at end B will be determined, assuming that EI is constant over the length. For this purpose, a unit load in the form of a moment is applied at point B (see Fig. A-IOc). It is seen from Figs. A-lOb and A-IOd that the functions ML and Me are quadratic and linear, respectively. For this example, Table A-4 yields

###### OB= ~IfMI'MLdx = ~I[~M(M:l]= ~I[~(-1)(W~2)] = - 2:~~

The result is the same as that given in Case I of Table A-3.

###### References

I. Oden, J. T., Mechanics ofElastic Structures, McGraw-Hill, New York, 1967.

2. Gere, J. M., and Timoshenko, S. P., Mechanics afMaterials, 3rd ed., PWS-Kent, Boston, MA.1990.

![image 657](Matrix Analysis of Framed Structures_images/imageFile657.png)

###### f

###### I

###### f

###### i

~

~.

~

So

~

L(Cd)'3+3L2M.M1

+3"M,(M3M..)

I-'-l.~

~

M,

2L3'M1MJ

8L15MIM3

L'3MM3•

L'3MIM3

L5MIM3

L

L+121 +V3M.M

~(1++i)MIM4

- -C)2L(a
- -6adM!M3


3L(ab)1 +3L2M.M

~(l+~)M.MJ

~(1+~)MIMJ

~(1+~)M.M3

(Laa2)

~-->4cb.lL--I

A

Forc~a:

L2"M1MJ

L3MIMJ

fOLMCMLdxProductIntegrals

LI+-l.-I6"++)M2(MJ2M4

+~(1+i)M2M3

###### 12+4"MM3J(M.)M3M21

###### +J6"(2M!M)MJ26"M.M

cJM4+6"M.(2MJM..)L

~c::r'

###### +'36"(M.2M2)MMMJ•Jf--l.-J

TableA·4

AI]LL'3~'3MM3•(M.+M)M32

###### 2"(M12"+M2)MJM1MJ

~(1+~)MIM3~j

t--l.--..l~l.ML

~MlAI.

LL~AI'

###### gM'LL

LL~M]

LLMl~

L

+M.(M32M..)

~(I+i)M'M3~~

M,6"

t-l.--j

I+-l.--:

I--I.~

~l.

![image 658](Matrix Analysis of Framed Structures_images/imageFile658.png)

- A.4 Integrals of Products for Computing Displacements 497


AliII11tTlIII!1!J;

IE L ~I

(a)

( b)

~~_______________~1

(e)

(d)

###### Fig. A-10.

![image 659](Matrix Analysis of Framed Structures_images/imageFile659.png)

###### B

###### End·Actions for Restrained Members

A restrained member is one whose ends are restrained against displacements (translation and rotation), as in the case of a fixed-end beam. The end-actions for a restrained member are the reactive actions (forces and moments) developed at the ends when the member is subjected to loads, temperature changes, or other effects. Restrained members are encountered in the stiffness method of analysis and also in the determination of equivalent joint loads (see Chapters 3 and 4). In this appendix, formulas are given for end-actions in restrained members due to various causes. It is assumed in each case that the member is prismatic.

Table B-1 gives end-actions in fixed-end beams that are subjected to various conditions ofloading. As shown in the figure at the top of the table, the length of the beam is L, the reactive moments at the left and right-hand ends are denoted MA and Ms, respectively, and the reactive forces are denoted RA and Rs, respectively. The moments are positive when counterclockwise, and the forces are positive when upward. Formulas for these quantities are given in Cases 1, 2, 5, 6, 7, and 8. However, Cases 3 and 4 differ slightly because of the special nature of the loads. In Case 3 the load is an axial force P, and therefore the only reactions are the two axial forces shown in the figure. In Case 4 the load is a twisting moment T, which produces reactions in the form of twisting moments only.

All of the formulas given in Table B-1 can be derived by standard methods of mechanics of materials. For instance, many of the formulas for beams can be obtained by integration of the differential equation for bending of a beam. The flexibility method, as described in Chapter 2, can also be used to obtain the formulas. Furthermore, the more complicated cases of loading frequently can be obtained from the simpler cases by using the principle of superposition.

Fixed-end actions due to temperature changes are listed in Table B-2. Case 1 of this table is for a beam subjected to a uniform temperature increase of AT. The resulting end-actions consist of axial compressive forces that are independent of the length of the member. The second case is a beam subjected to a linear temperature gradient such that the top of the beam has a temperature change AT2, while the bottom has a change AT1• If the temperature at the centroidal axis remains unchanged, there is no tendency for the beam to change in length; and the end-actions consist of moments only. On the other hand, a nonzero change of temperature at the centroidal axis is covered by Case 1.

498

![image 660](Matrix Analysis of Framed Structures_images/imageFile660.png)

Table H-I Fixed-End Actions Caused by Loads

Pa

M, = -J[B = L (L - a)

R, = V (3a+b) RB= La(a+3b)-61

Pb2 Pa2 RA = RB = P

###### --=J

M, = -iVfB =-WL212

wL

R,., = RB =-2

Mb

M A = V (2a - b)

2..1

J[a

###### Mil = V (2b - a)

RA = -Ril = 6Jfab

###### V

wa2

MA = 12V (6V - 8aL + 3a2)

~I

wa3

p

MB = -12V (4L - 3a)

~~ ~ ~~

RA I-0--+-b------I R8

wa3

R _ Pa

I RB = 2V (2L - a)

B- L

wV

WL2

}vfB = -20

###### MA =30

###### R _ 3wL

R _ 7wL

TB = Ta

A - 20

B - 20

L

![image 661](Matrix Analysis of Framed Structures_images/imageFile661.png)

500 Appendix B: End-Actions for Restrained Members

Table B-2

Fixed-End Actions Caused by Temperature Changes

WLineartemperaturegradient

~Uniform increase in temperature

###### R = EAex flT

I = moment of inertia fl T\ = temperature change at bottom of

E = modulus of elasticity A = cross-sectional area ex = coefficient of thennal expansion

beam

fl T2 = temperature change at top of beam d = depth of beam

fl T = temperature increase

- Table B-3 gives fixed-end actions due to prestrains in the members. A prestrain is an initial deformation of a member, causing end-actions to be developed when the ends of the member are held in the restrained positions. The simplest example of a prestrain is shown in Case 1, where member AB is assumed to have an initial length that is greater than the distance between supports by a small amount e. When the ends of the member are held in their final positions, the member will have been shortened by the distance e. The resulting fixed-end actions are the axial compressive forces shown in the table. Case 2 is a member with an initial bend in it, and the last case is a member having an initial circular curvature such that the deflection at the middle of the beam is equal to the small distance e.
- Table B-4 lists formulas for fixed-end actions caused by displacements of one end of the member. Cases 1 and 2 are for axial and lateral translations of the end B of the member through the small distance 11, while Cases 3 and 4 are for rotations. The rotation tbrough the angle (J shown in Case 3 produces bending of the member, while the rotation through the angle 1> in Case 4 produces torsion. Formulas for the torsion constant J, which appears in the formulas of Case 4, are given in Appendix C for several cross-sectional shapes.


End-actions for truss members are listed in Table B-5 for three cases of loading: a uniform load, a concentrated load, and a moment. The members shown in the figures have pinned ends that are restrained against translation but not rotation, because only joint translations are of interest in a truss analysis. The members are shown inclined at an angle 'Y to the horizontal, in order to have a general orientation. However, the end-actions are independent of the angle of inclination, which may have any value (including 0 and 90 degrees). For both the uniform load and the concentrated load

![image 662](Matrix Analysis of Framed Structures_images/imageFile662.png)

Appendix B: End-Actions for Restrained Members

###### 501

###### Table B-3 Fixed-End Actions Caused by Prestrains

Bar with excess length

Bar with a bend

A 8

~L+e~

~~::1-A_____8--t:~___

###### f-I.--L------+1.1 R

2EIO lIfA = -- (2£ - 3a)

R = EAe

L

1.2

E = modulus of elasticity A = cross-sectional area

JIB = 2~:O (L - 3a)

6EIO

R.1 = - RB = La (L - 2a)

e = excess length

I = moment of inertia

o= angle of bend ~I Initial circular curvature

11 -11 = 8Ele

###### 1 A = • B L2

e = initial deflection at middle of bar

,----------.---------------~

![image 663](Matrix Analysis of Framed Structures_images/imageFile663.png)

502 Appendix B: End-Actions for Restrained Members

Table B-4

Fixed-End Actions Caused by End-Displacements

_11

I

;--~A B~ ~~

I~ L ·16 ~

R=-EA~

L

21

###### M,c~tJM't. L 1

R = 12EI~

MA = MB = 6EI~

###### V

£2

###### ~

C~A _/ ~)

M, t--? .{ M,

R L R

R = 6EI()

1[ = 2EI()

B = 4EI()

• A L J1[

/.,2

L

###### -=-1

~~A B~~ -r---T

###### I. L ·1

T = GJtjJ

L

G = shear modulus of elasticity

###### J = torsion constant

![image 664](Matrix Analysis of Framed Structures_images/imageFile664.png)

Appendix B: End-Actions for Restrained Members

503

Table B-S

End-Actions for Truss Members

R = wL

2

~I

B

R=M

L

![image 665](Matrix Analysis of Framed Structures_images/imageFile665.png)

504 Appendix B: End-Actions for Restrained Members

(Cases 1 and 2) the reactions are parallel to the lines of action of the loads, while in Case 3 the reactions are perpendicular to the axis of the member.

If a truss member is subjected to a uniform increase in temperature, Case 1 ofTable B-2 can be used; if subjected to a prestrain consisting of an increase in length, Case 1 of Table B-3 can be used; and if subjected to a displacement in the axial direction, Case 1 ofTable B-4 can be used.

![image 666](Matrix Analysis of Framed Structures_images/imageFile666.png)

###### C Properties of Sections

y

z

###### 1= ht",~

------ -- ---

.-1 = 2(btj + htll.)

J ~ 2b2h2 tjtu'

btu' + Iztj

A

1 = 2htw

--- _._._- --------.-----.--~--- ------

1=2

z

y bh3

J = {3 hb3

/z = 12

For II ;;. b,

I"

hb3

{3 ~"31 - 0.21 hb( 1 - 12114b4 )

h /y = 12

Z

~

6

..l=bh

1=-

5

~b-~

1 = 10

9

lz = moment ofinertia ofcross section about z axis / y = moment of inertia of cross section about y axis A = area of cross section

J = torsion constant f = form factor for shear

![image 667](Matrix Analysis of Framed Structures_images/imageFile667.png)

###### DComputer Routines forSolving Equations

0.1 Factorization Method for Symmetric Matrices. The primary mathematical task associated with matrix analysis of framed structures consists of solving a set of n simultaneous linear algebraic equations for n unknowns. There are many methods for computing the unknowns in such equations [1], one of which is called the Jactorization method (also referred to as the method ojdecomposition). This approach is particularly well suited for matrix analysis of structures because it provides the efficiency of the well-known Gaussian elimination process within a matrix format. Since the stiffness and flexibility matrices of linearly elastic structures are always symmetric, a specialized type of factorization known as the Cholesky method will be developed for symmetric matrices. Recurrence equations derived in this section will be extended to banded matrices and applied as computer subprograms in later sections.

To begin the discussion, let the symbol A represent a symmetric matrix of size n x n. If this matrix is positive definite as well as symmetric, it can be factored into the product of a lower triangular matrix and an upper triangular matrix, each of which is the transpose of the other. Thus, the factorization of A may be stated as

(0-1)

The symbol U in this expression denotes the upper triangular matrix, and UT is its transpose. Equation (0-1) in expanded form becomes

Au Al2 Al3 A ln A21 A22 A 23 A 2n A31 A32 A33 A 3n

Ani An2 An3 Ann

Vu 0 0 0 Vu Vl2 Vl3 V ln Vl2 V 22 0 0 0 V 22 V 23 V 2n Vl3 V 23 V33 0 0 0 V33 V 3n (0-2)

V ln V 2n V 3n Vnn 0 0 0 Vnn

It can be seen from Eq. (0-2) that elements ofthe matrix A consist of inner products of the rows of UT and the columns of U, which is equivalent to

506

![image 668](Matrix Analysis of Framed Structures_images/imageFile668.png)

D.I Factorization Method for Symmetric Matrices 507

calculating the elements of A as inner products among the columns of U. Thus, the inner products of the first column of U with itselfand subsequent columns produce

Similarly, the inner products of the second column of U with itself and subsequent columns are

and for the third column of U the inner products are

In general, a diagonal term Aii in matrix A can be written as

or

###### Aii = ~ V~i (i =j) (a)

k=l

In a similar manner, the off-diagonal term Au in an upper triangular position is seen to be

or

i

###### Au = ~ VkiVki

(i <j) (b)

k=l

Then the elements ofU may be determined by rearranging Eqs. (a) and (b) as follows:

(1<i=j) (0-3)

(1 < i <j) (0-4) Vu = 0 (i > j) (0-5)

Equations (0-3), (0-4), and (0-5) constitute recurrence formulas in an algorithm for factoring the matrix A into the form given by Eq. (0-1). Because it was developed by Cholesky and a square root term appears in Eq. (0-3), this technique is known as the Cholesky square root method. It applies only to symmetric, positive definite matrices, for which the term within the square root sign in Eq. (0-3) is always a positive number.

![image 669](Matrix Analysis of Framed Structures_images/imageFile669.png)

508 Appendix D: Computer Routines for Solving Equations

If the symmetric matrix A were not positive definite, it could still be factored into the following triple product:

###### A = UTDU (0-6)

In this expression the symbol D represents a diagonal matrix containing the squares of terms factored from the rows of U. If such factored terms are chosen to be U ii. then the typical diagonal term in D is

###### (i = 1,2, ... , n) (0-7)

Since this term is the square of that in Eq. (0-3), it becomes possible to avoid taking square roots by factoring A as indicated by Eq. (0-6) instead of Eq. (0-1). For this purpose the recurrence formulas given by Eqs. (0-3) and (0-4) must be modified, and the resulting technique is known as the modified Cholesky method. In expanded form, the factorization represented by Eq. (0-6) is

###### o

0 0 U l2 1 0

o

###### o x

A= Ul3 U23 1

U 1n U 2n U 3n

(0-8)

Du 0 0 0 D22 0 0 0 D33

0 0 0

1

U l2

U l3 U 1n U 23 U2n

0 0

1

0 0

1 U3n 0 1

0 0 0

0

Dnn

From this form it is seen that Au = Du and that other diagonal terms in A can be written as

or

i-I

###### Aii = Dii + ~ Dkkmi

(1<i=j) (c)

k=l

Similarly, off-diagonal terms in the first row of A are Ali = D l1U Ii and in other rows are

Aii = DUUliU1i + D22U2iU2i + D33U3iU3i + ... + DiiUij

or

;-1

Au = D;;Uu + ~ DkkUk;Uki (1 < i <j) (d)

k=1

![image 670](Matrix Analysis of Framed Structures_images/imageFile670.png)

D.I Factorization Method for Symmetric Matrices 509

Then the elements ofD and U can be found by rearranging Eqs. (c) and (d), as follows:

i-J

###### Dii = Aii - ~ Dkk VTe; (1 < i = j) (0-9)

k=l

###### (l < i <j) (0-10)

###### Vij = 0 (i > j) (0-11)

These recurrence formulas imply twice as many multiplications as those in Eqs. (0-3) and (0-4). However, this increase in the number of operations can be avoided, as shown in the subsequent discussion.

The recurrence equations (0-9) and (0-10) indicate that the diagonal term Dii is computed first, followed by the calculation of the terms in the i-th row of U. This row-wise generation of tem1S can be changed to the column-wise sequence:

Vij = _1_(Au - ~ DkkVkiVkj)

(1 < i <j) (e)

Dii k=l

(l<i=j) (f)

Note that the product Dkk V kj appears in both Eq. (e) and Eq. (f). Let this product be

V'0 = DkkVkj (g) and perform the calculations for Vu and Djj in the following manner (for j

= 2, 3, ... , n):

- i-I

Vi; = Au - ~ - -* ( 1 < j) (0-12)

UkiUkj <

k=1

- j-I


Djj = Ajj - ~ - -* ( 1 < = j) (0-13)

UkjUki k=1

where

###### U 1 -*

###### kj = -D Ukj (0-14)

kk

Thus, for column j the intermediate product Vi; is obtained for each offdiagonal term after the first (see Eq. 0-12). Then the diagonal term Djj is computed (Eq. 0-13), during which calculation the final value of each offdiagonal term is also found (Eq. 0-14). By this sequence of operations, the number of multiplications is reduced to that for the Cholesky square root method, and the calculation of square roots is avoided.

![image 671](Matrix Analysis of Framed Structures_images/imageFile671.png)

Assume that the following system of linear algebraic equations is to be solved:

AX = B (D-I5)

in which X is a column vector of n unknowns and B is a column vector of constant terms. As a preliminary step, substitute Eq. (D-6) into Eq. (D-I5) to obtain

tFDUX = B (D-I6) Then define the vector Y to be

UX = Y (D-I7) In expanded form this expression is

###### 1 VI2 VI:l VIn XI YI 0 1 Vn V21l X2 Y2 0 0 1 V31l X~ Y~ (D-I8)

0 0 0 X" YII In addition, define the vector Z to be

DY = Z (D-I9) for which the expanded form is

Dl1 0 0 0 YI ZI 0 D22 0 0 Y2 Z2 0 0 D33 0 Y3 Z3 (D-20)

0 0 0 Dnn Yn Zn

Substitution of Eq. (D-I7) into Eq. (D-I9) and then the latter into Eq. (D-I6) yields

UTz = B (D-21) Or, in expanded form:

0 0 0 ZI BI VI2 1 0 0 Z2 B2 Ul3 V2~ 1 0 Z3 B3 (D-22)

###### Vln V2n V3n Zn Bn

The original vector of unknowns X may now be obtained in three steps using Eqs. (D-2I), (D-I9), and (D-I7). In the first step Eq. (D-2I) is solved for the vector Z. Since UT is a lower triangular matrix (see Eq. D-22), the elements of Z can be calculated in a series of forward substitutions. For

![image 672](Matrix Analysis of Framed Structures_images/imageFile672.png)

511

D.I Factorization Method for Symmetric Matrices

example, the first term in Z is

ZI = BI The second term in Z is found to be

- (h)
- (i)
- (j)


and the third term is

In general, the recurrence formula for elements of Z becomes

i-I

###### Zi = Bi - L UkiZk (1 < i)

(D-23)

k=1

The second step consists of solving for the vector Y in Eq. (D-I9). Since D is a diagonal matrix (see Eq. D-20), the elements of Y can be found by dividing terms in Z by corresponding diagonals of D, as follows:

###### Z

(i = I, 2, ... , n) (D-24)

Yi =-'

Dii

This recurrence formula can be applied in either a forward or a backward sequence.

In the third step the vector X is found from Eq. CD-I7). SinceTI is an upper triangular matrix (see Eq. D-I8), the elements of X are determined in a backward substitution procedure. The last term in X is

###### XII = YII

(k)

The next-to-Iast term is

(1)

and so on. In general, the elements of X (other than the last) may be calculated from the recurrence formula:

II

Xi = Yi- L UikXk

(i < n) (D-25)

k=i+1

This step completes the solution ofthe original equations (Eq. D-I5) for the unknown quantities.

Numbers of arithmetic operations for the modified Cholesky method are summarized in Table D-I for factoring an n x n symmetric coefficient matrix and solving for n unknowns. Also shown in the table are the corresponding numbers for the method of compact Gaussian elimination [2], which is known to require the least number of operations. It is seen that the

![image 673](Matrix Analysis of Framed Structures_images/imageFile673.png)

Table D-l

Numbers of Arithmetic Operations

Method Multiplications Divisions Additions

n n n --- ---

###### 3 n n2 n3

Factor

6 6 2 2 6 6

Modified Cholesky Solve n2 n n2 - n

n3 n n2 n n3 7n Totals -6 + n2 --6 -+-2 2 -6 + n2 --6 Compact Gaussian n3 3n2 2n n3 7n elimination -+---6 2 3 n -6 + n2 --6

sum of the number of multiplications and divisions is the same for both methods, as is the number of additions.

The factorization and solution procedures described above apply also to banded symmetric matrices. For a banded matrix the upper triangular component U (and hence U) has the same semi-band width as the original matrix A. Therefore, fewer calculations are required in the recurrence formulas for both factorization and solution.

D.2 Subprogram FACTOR. In this section the factorization of a symmetric matrix by the modified Cholesky approach, as described in the preceding section, is cast into the form of a computer subprogram. The name of this subprogram is

FACTOR(N,A,*)

The first argument in the parentheses is the integer number N, which denotes the size of the matrix to be factored. The second identifier represents a symmetric matrix A ofreal numbers, and the third symbol (an asterisk) signifies a nonstandard RETURN to an error message in the main program if A is found not to be positive definite. In addition to this notation, the integer numbers I, J, K, 11, and 11 serve as local indexes in the body of the subprogram; and the real variables SUM and TEMP are used for temporary storage.

Subprogram FACTOR appears in Flow Chart 0-1, which implements Eqs. (0-12), (0-13), and (0-14) from the preceding section. Elements ofthe upper triangular matrix U are generated column-wise in the storage locations originally occupied by the upper triangular part of the matrix A. Thus, the identifier A remains in use throughout the flow chart. In addition, the diagonal elements Dii are stored in the diagonal positions Aii of matrix A. If a zero or negative value of Dii is detected, control is transferred (by means of the nonstandard RETURN) to an error message in the main pro-

![image 674](Matrix Analysis of Framed Structures_images/imageFile674.png)

D.2 Subprogram FACTOR

513

Flow Chart D-l: Subprogram FACTOR (N, A, *)

1---

I

###### I

###### t

,--

I

###### I

###### I

I

I

SUM = A(I, J) 11 = 1-1

I

###### I

###### I

###### +

I-

I

I

I

###### I

I I

L SUM = SUM - A(K, I) * A(K, J)

I

- Eg. (0-12)
- Eg. (0-13)
- Eg. (0-14)


###### t

###### L __

I

###### I

###### I

I

###### I

###### I

TEMP = AtK, J) / A(K, K) SUM = SUM - TEMP * A(K, J)

I I

###### +

I

###### I

I

###### L __ _

RETURN END

![image 675](Matrix Analysis of Framed Structures_images/imageFile675.png)

gram. Elements of A below the main diagonal are left undisturbed by this subprogram.

Neither Subprogram FACTOR nor Subprogram SOLVER (described in the next section) is needed by the structural analysis programs in this book. However, they are included in the series of subprograms because of their general usefulness. In addition, they serve as guides to understanding the more complicated subprograms called BANFAC and BANSOL, which are given in later sections and used in the structural analysis programs.

D.3 Subprogram SOLVER. The second subprogram in this series accepts the factored matrix from Subprogram FACTOR and solves for the unknowns in the original system ofequations. The name ofthis subprogram is

SOLVER(N,U,B,X)

The argument N has the same meaning as previously, and the symbol U denotes the matrix from Subprogram FACTOR. The identifiers B and X represent real vectors of constant terms and unknowns, respectively (see Eq.0-15).

Flow Chart 0-2 shows the logic for Subprogram SOLVER. In the first portion of the flow chart the intermediate vector Z is computed by forward substitutions, according to Eq. (0-23). Note that the vector X is used as temporary storage for Z in this part of the subprogram.

The second portion of the chart involves finding the vector Y by dividing each value of Zi by the corresponding diagonal term Dii (see Eq. 0-24). In this instance the vector X is used as temporary storage for Y, and the terms Dii are known to be in the diagonal positions Vii (see Subprogram FACTOR).

In the last portion of the chart, the final values of the elements in the vector X are calculated by Eq. (0-25). This backward sweep completes the solution of the original equations.

D.4 Subprogram BANFAC. The factorization method is more efficient for a banded matrix than for a filled array because no calculations need be made for elements outside of the band. Figure 0-la illustrates the general appearance of a banded symmetric matrix. The symbol NB shown in the figure denotes the semi-band width, and N is the size of the matrix. Only the upper portion ofthe band (including the diagonal elements) has to be stored, as indicated by the small squares in Fig. 0-la. A more efficient pattern for storing the upper band portion of the matrix appears in Fig. 0-lb. In this arrangement the required elements are stored as a rectangular array with the diagonal elements (shown shaded) in the first column. Comparison of Fig. 0-la with Fig. 0-lb shows that the rows of the matrix have been shifted to the left, and most of the excess terms have been removed.

Flow Chart 0-3 contains the steps for a subprogram that factors the upper band of a symmetric matrix stored as a rectangular array. The name

![image 676](Matrix Analysis of Framed Structures_images/imageFile676.png)

D.4 Subprogram BANFAC

515

Flow Chart D-2: Subprogram SOLVER (N, U, B, X)

1---

I I

SUM = 8(1)

###### I I I

- K1 = 1-1

I=N-11+1 SUM = X(I)

- K2 = 1 + 1


I

###### I

~

I

###### I

- Eq. (0-23)
- Eq. (0-24)


I

###### L __ _

1---

I I

###### I I I I

I

+

I I-

I I 4

I L I

Eq. (0--25)

L __

RETURN END

![image 677](Matrix Analysis of Framed Structures_images/imageFile677.png)

516 Appendix D: Computer Routines for Solving Equations

###### F-NB---I'--~I

![image 678](Matrix Analysis of Framed Structures_images/imageFile678.png)

![image 679](Matrix Analysis of Framed Structures_images/imageFile679.png)

###### 1

J 1

###### j

###### r -- -------- -- -

N

N

J ---------- --------- --- ----

J

o

o

(oj (b)

Fig. 0-1. Banded matrix: (a) usual form of storage and (b) upper band stored as a rectangular array.

of this subprogram is

BANFAC(N,NB,A,*)

Arguments in the parentheses have all been defined, and most of the other identifiers in the body of this subprogram were used before. However, a new index J2 is introduced for the purpose of limiting calculations to nonzero elements. When the column number J exceeds the semi-band width NB in Fig. D-la, the first nonzero term in that column has the row index

J2 = J - NB + 1 (NB < J ~ N) (a) Otherwise, for the first NB columns (except column 1),

###### J2 = 1 (1 < J ~ NB) (b)

The sequence of operations in Subprogram BANFAC follows that in Subprogram FACTOR (see Flow Chart D-l), except that additional statements are required to determine the index J2. Furthermore, the column SUbscripts of terms in Eqs. (D-12), (D-13), and (D-14) are modified due to the fact that the upper-band portion of matrix A is stored as a rectangular array. Whereas the recurrence equations pertain to columns I and J in Fig. D-la, they involve staircase patterns of elements in the mMrix of Fig. D-lb.

As in the earlier subprogram for factorization, the matrixU is generated and placed in the storage locations originally occupied by the matrix A, but

![image 680](Matrix Analysis of Framed Structures_images/imageFile680.png)

D.4 Subprogram BANFAC

517

Flow Chart D-3: Subprogram BANFAC (N, NB, A, *)

###### ----l

I

###### I

TEMP = A(K, J - K + 1)/A(K, 1\ SUM = SUM - TEMP * A(K, J - K + 1)

- J1 =J-1
- J2 = J - NB + 1


###### I

I

###### +

I

###### I I

I

###### L ___ _

---,

2 1= 2, J1

I

###### RETURN END

###### I

I

###### I

2

I

###### I I

+

I I

----1

###### I

###### I

SUM = SUM - A(K, 1-K + 1) * A(K, J - K + 1) J

I

###### I

###### I I

~

the identifier A remains in use. In addition, the diagonal elements D ii are stored in the first column of A for convenience in later calculations. If Dr; is found to be zero or negative, control is transferred (by means of the nonstandard RETURN) to an error message in the main program.

Subprogram BANSOL, given in the next section, is intended to be used

![image 681](Matrix Analysis of Framed Structures_images/imageFile681.png)

518 Appendix D: Computer Routines for Solving Equations

in conjunction with Subprogram BANFAC. They are both applied in the structural analysis programs in Chapter 5, which take advantage of the band widths of the stiffness matrices.

D.S Subprogram BANSOL. The last subprogram in the series is analogous to Subprogram SOLVER (see Flow Chart D-2), except that it applies to a banded matrix. This subprogram accepts the upper band of the matrix U from Subprogram BANFAC and solves for the unknowns in the original system of equations. The name of the subprogram is

BANSOL(N,NB,U,B,X)

All identifiers in the parentheses are familiar terms that have been used before.

Flow Chart D-4 for Subprogram BANSaL bears much similarity to that for Subprogram SOLVER in Flow Chart D-2. However, it is complicated by the fact that the upper band ofU is stored in rectangular form. In both the forward and backward substitutions (see Eqs. D-23 and D-25) the index J is used to delineate nonzero terms to be included in the calculations. In the forward sweep, the row index for the first nonzero item in column I is

J = 1- NB + 1 (NB < I ~ N) (a) Otherwise, for the first NB columns (except column 1),

J = 1 (1 < I ~ NB) (b)

Similarly, in the backward sweep, the column index for the last nonzero element in row I of matrix U is

J=I+NB-l [1 ~ I ~ (N - NB)] (c) Otherwise, for the last NB rows (except row N),

J=N [(N - NB) < I < N] (d)

In addition, the column indexes ofthe elements in Uare modified according to their actual locations in the rectangular array.

As in the earlier solution subprogram, the intermediate vectors Z and Y are generated in the vector X, and final values of X are calculated in the backward sweep. The elements of U and B are left unaltered by this solution routine; so it can be used repeatedly for the same matrix U but for different vectors of constant terms.

References

###### I. Bathe, K. J. Finite Element Procedures in Engineering Analysis, Prentice-Hall, Engle-

wood Cliffs, New Jersey, 1982.

###### 2. Fox, L., An Introduction to Numerical Linear Algebra, Oxford Univ. Press, New York,

1965.

![image 682](Matrix Analysis of Framed Structures_images/imageFile682.png)

D.5 Subprogram BANSOL 519

,---

Flow Chart D-4: Subprogram BANSOL (N, NB, U, B, X)

1----

I

I

I I I

1 = N-11 + 1 J = 1 + NB-1

###### I

I

I

###### I

###### I I

I

###### I I

I

SUM = B(I) K1 =1-1

SUM = X(I)

K2 = 1+ 1

I

###### I

###### I

+ I

+

###### I ,---

,---

###### I

###### I I I I

I

I

I 4

###### I

r---------~--------~

L SUM = SUM - U(K, 1 - K + 1) * X(K)

L SUM=SUM-U(I,K-I+1)*X(K)

I

###### L __ _

L __ _

,

RETURN END

I

L

![image 683](Matrix Analysis of Framed Structures_images/imageFile683.png)

E

###### Solution Without Rearrangement

In the stiffness method of analysis it is possible to solve the joint equilibrium equations in place (without rearrangement). This can be accomplished by modifying the stiffness and load matrices to convert the equations for support reactions into trivial displacement equations embedded within the complete set of equations. Then the whole set can be solved for the unknown joint displacements as well as the known support displacements without having to rearrange and partition the matrices.

To show the technique, a small example will suffice. Suppose that a hypothetical structure has only four possible joint displacements, as indicated by the following joint equilibrium equations:

[~~~: ~~~: ~~~: ~~~:] [~~~]-[~~~] (E-l)

SJ31 SJ32 SJ33 SJ34 DJ3 - AJ3 SJ41 SJ42 SJ43 SJ44 DJ4 AJ4

In addition, suppose that the third displacement is specified to be a nonzero

support displacement DJ3 =1= o. Then the terms involving DJ:l can be subtracted from both sides of Eq. (E-l), and the third equation can be replaced by the trivial expression DJ3 = DJ3 to obtain:

SJll SJ12 0 SJ14] [DJI] [AJ! - SJl3DJ3]

SJ21o SJ220 01 SJ240 DJ2DJ3 = AJ2 -DJ3SJ23DJ3 (E-2)

[

SJ41 SJ42 0 SJ44 DJ4 AJ4 - SJ43DJ3

These equations may now be solved for the four joint displacements, including D J3.

Negative terms on the right-hand side of Eq. (E-2) represent equivalent joint loads due to the specified support displacement DJ3• Of course, if DJ3 = 0 these equivalent joint loads are also zero. Any number of specified support displacements can be handled in this manner. This technique precludes the calculation of support reactions by the matrix multiplication approach described in Sec. 6.7. Instead, it is necessary to obtain the reactions from end-actions of members framing into the supports, as in the programs of Chapter 5.

To apply the technique described above, it is necessary to revise the flow charts in Chapter 5. Flow Chart E-l shows the changes required in gener-

520

![image 684](Matrix Analysis of Framed Structures_images/imageFile684.png)

Appendix E: Solution Without Rearrangement 521 Flow Chart E-l: Alternative Method

###### t

Sec. 2b

###### I r---

(Index on rows of SM)

###### I I

(Index on columns of SM)

i--

I I

I

###### I I

I

Set row index J R for matrix S1 equal to IM(1).

I t

I I

I I

Check for restraint corresponding to index JR. If so, go to 3, skipping transfer.

###### I

###### I I

I

Set column index Ie for matrix S1 equal to IM(K).

t I I I

t

I

Check for restraint corresponding to index Ie.

###### I I

If so, go to 3, skipping transfer.

###### I I

###### I I

Check for upper triangular position. If so, go to 2, keeping subscripts as they are.

I

I I I I

I

For lower triangular position, switch subscripts,

thereby changing to upper triangular position.

I I I +

I I

Reset column index for storing upper band of

i t

matrix SJ as a rectangular array.

I I I I

Transfer an element of SM to the position in matrix S1 given by subscripts IR and IC.

I SJ(IR, IC) = SJ(IR, IC) +SM(J, K)

I

###### t I

L_•

I I

I L __ _ I

L__

###### r

(Index on joint displacements)

I

Check for restraint corresponding to index 1.

###### I

If none, go to 9, skipping next statement.

I

I

Set S1(1, I) equal to unity in preparation for

solving in place without rearrangement.

I

L

RETURN END

![image 685](Matrix Analysis of Framed Structures_images/imageFile685.png)

522 Appendix E: Solution Without Rearrangement

ating the stiffness matrix for any type of framed structure. By this routine no transfers of stiffness terms are made to rows or columns corresponding to support restraints. In addition, the value 1.0 is placed in the diagonal position (first column of SJ) wherever a support restraint exists.

Other less important changes must also be made at various places in all of the programs of Chapter 5, as follows:

- 1. Because there is no rearrangement, the identifiers SFF and DF may be replaced by SJ and DJ, respectively.
- 2. Section Ie on joint displacement indexes may be omitted.
- 3. When calling Subprograms BANFAC and BANSOL, use ND instead of N.
- 4. In Sec. 4b no rearrangement of the load vector is required.
- 5. Before calling BANSOL, set the loads at supports equal to zero.
- 6. In Sec. 5a omit the expansion of the displacement vector.


Although the coded programs are somewhat simplified by avoiding rearrangement, they can be wasteful of computer time and storage if there are numerous restraints. Therefore, the method involving rearrangement was chosen for the programs in this book because of its greater efficiency.

![image 686](Matrix Analysis of Framed Structures_images/imageFile686.png)

###### Answers to Problems

Chapter I

- 1.4-1 The increase in length of the bar.
- 1.4-2 A horizontal force acting to the right at joint C, and a clockwise couple acting at joint C.
- 1.4-3
- 1.4-4
- 1.4-5


1.7-1 1.7-3 1.7-6 1.7-8

- 1.7-10

- 1.7-12

- 1.7-14

- 1.7-16

- 1.14-1
- 1.14-2
- 1.14-3
- 1.14-4
- 1.14-5
- 1.14-6


A,L A"L" A:lL"

Dll = 3El D2" = - 32El D,,:; = SEl (a) 3 (b) 2 (c) 3 (d) 2 1.7-2 (a) 2 (b) 7 (c) 4 (a) I (b) 5 1.7-4 10 1.7-5 (a) 3 (b) 9 (a) 3 (b) 6 (c) 3 1.7-7 (a) I (b) S (c) 5 (a) 4 (b) 14 (c) S 1.7-9 (a) S (b) 16 (c) S (a) 9 (b) 27 (c) 15 1.7-11 (a) 0 (b) 9 (a)3(b)6 1.7-13 (a)21 (b) 12 (a) 15 (b) 21 (c) 15 1.7-15 (a) 42 (b) 54 (c) 3S (a) 30 (b) 36 (c) 25 1.7-17 (a) 60 (b) S4 (c) 60 (a) 8, = (SA, - A z)Ll24El (c) 8(' = (-A, + 2Az)Ll24El

(b) ~(' = A,UI16El

F" = LIEl F'2 = F21 = - V/SEl F22 = L3/24El Fll = V/SEl F,z = Fz, = UI4SEl Fzz = Ll12El D, = (4.S3A, + 3.41Az)LlEA Dz = 3.4l(A, + Az)LlEA

F" = 2(1 + V2)LlEA F12 = F2, = -LiEA F22 = LlEA F,z = 125L11SEA FZ2 = 42L1EA FZ:l = 32L13EA

Chapter 2

- 2.3-1


- 2.3-2


__ 96sEl Q = 30sEl Ql - 7V 2 7L3

- 2.3-4 Q _ 3PL


1 - 2S

Q - 17P 235

2 - 14 . -

5wU Q = _33wU Ql = - 60S 2 152

- 2.3-6


WL2

Q, =-"24 2.3-7 Q, = -0.243P

523

![image 687](Matrix Analysis of Framed Structures_images/imageFile687.png)

Answers to Problems

524

- 2.3-8
- 2.3-9
- 2.3-10
- 2.3-11
- 2.3-12
- 2.3-13
- 2.3-14
- 2.3-15
- 2.3-16
- 2.3-17
- 2.3-18
- 2.3-19
- 2.3-20
- 2.3-21
- 2.3-22
- 2.3-23
- 2.3-24
- 2.3-25
- 2.3-26


Q, = -0.243P Q2 = O.I72P Q, = 0.348P Q2 = -0.699P Q, = 0.0267P Q2 = 0.4698P Q, = 2.628 P Q2 = 0.586 P Q, = - wLl28 Q2 = 3wL17 Q, = - 3PLl28 Q2 = 3PLl56 Q, = -23P111 Q2 = 3PI22 Q, = -wLl16 Q2 = 7wLll6 Q3 = -wL2/24

L H3 JH V fL H

Fn = EA + 3EI + GA F22 = 3EI + GA + EA

Other tenns in F are the same as in Eg. (a) of Example 4, Sec. 2.3.

L2 F12 = F 23 = 0 F 13 = - EI

2V

(a) Fn = 3EI

###### , 4L

2V 2L 2JL

(b) Fl1 = 3EI + EA + GA L2

r33 = EI

F =-- 8V 2L 2fL

4L

13 EI F22 = 3EI + EA + GA

F33 = EI

8V

Fl1 = 3EI

4L

F33 = EI

P liP Q, = - 16 Q2 = 16

Ql = -0.156P Q2 = O.290P

F22 = F33 = ~I + ~J F23 = 0 3P 1 E1 QI = 162+3p P = GJ Q = {-77, 9}PLl336 Q, = 55wLl96 Q2 = - 35wLl96 2V 2L Fn = F33 = 3EI + EA FI2 = 0

4V 2L

F22 = 3EI + EA

PL'l

DQL3 = 0

DQLI = - 'lEI

L:l

###### F12 = -F13 = 2EI

5L'l L'l

F33 = 3EI + GJ

![image 688](Matrix Analysis of Framed Structures_images/imageFile688.png)

Answers to Problems

525

- 2.4-1 2.4-2 2.4-3 QI = -3EI<I>IIL Q2 = 3EI<I>I/2 2.4-4 Don = DiLL:.T Don = 0 2.4-5

- 2.4-7
- 2.4-8
- 2.4-9
- 2.4-10
- 2.4-11
- 2.4-12


- 2.5-1


2.4-6

DOPI = O.8e DOP2 = 1.6e Q _ 12EIo5 6Elf3

I - - ------v- +-----v- Q __ 6EIs 2Elf3

2 - U + L

DQR! = -05 DQR2 = °

D 2s1 S2

QRI = -I: + L D _ ~ _ 2s

QR2 - L L 2 Q2 = 18EI(j()BI7L2

QI = -12EI(j()BI7L2 Doci = DiLL:. T - (3H DQC2 = --- - DiHL:.T - s

5PL>

48EI

###### PV [-16]2

DJ = 720EI ~~

###### [-0.1716]

D = PL [-1.172] .J EA -1.828

- 2.5-2
- 2.5-3


AR= P

1.828

DJ = {a, 0, I}PL%4EI An = {-3, 13, L}P132

Chapter 3

- 3.3-1 A _ 5wL

R! - 8

WL2 A R2 =-

8

A _ 3wL R3 - 8

- 3.3-2

llP

A.If! = ""'i6 AM2=~3PL

5P AM3 = 16

- 3.3-3 AR! = 2P

A _ 13PL R2 - 18

A _ 5PL R3 - 18

- 3.3-4 AM! -_ 13P8 A M2 =-PL A.lf3 =-P A _ 3PL 2 4 M4 - 8

3P P ARI = --8 AR2 = --

4

- 3.3-5

P 5PL

AR! = P

A _ 7PL

All! ='3 A.uz = 7z R2 - 72

- 3.3-6


23P

37P AM! =60

59PL A.lf2 = 360

###### 17PL

A.lf3 = 60 AM4 = 49P

360

23P AR2 = 60

ARI = 120

![image 689](Matrix Analysis of Framed Structures_images/imageFile689.png)

Answers to Problems

526

PL

Am = -AM3 = _ 25PL

AMI =72

- 3.3·7


72

A _ 13PL M5 - 18

A _ 17PL

A _ 127P

A _ 79P

M6 - 72

RI - 48

R2 - 48

4El

2El

6El 522 = 533 = - L

5 11 = 5•• =-

- 3.3·8


5 12 = 53. =-

L

L

El

- 523 =L

8El

522 =2511 =-

L

2El

512 = 523 =-

L

20El

533 = 5534 = --

3L 8El

5.. = 3L

4El 511 = 566 =-L

8El

522 = 533 = 5•• = 555 = -

L

4EI

524 = 25[2 = L

5 _ 96El

'1'1 - L'1

12EI

522 = 5aa = ~

511 = 555 = 2512 = 2545 = 4EIIL 5:1'1 = 452:1 = 45H = 32EII3L

522 = 5 •• = 28EII3L

19P A _ 79PL ARl = 22 R2 - 264

DI = 4.00wL2/EA D2 = -J5.8wL2/EA DI = 3PLlEA D2 = -4PLlEA DI = -3.11wL2/EA D2 = -20.6wL2/EA

AM2 = 0.433P

AMI = AM;j = 0.293P AM2 = 2AMI

19PL

264

AMI = AM;j = 0.293P - 0.060wL AM2 = 0.586P - 0.621wL AMI = P Am = 0.586P AM3 = -0.414P AMI = -AM5 = 0.236P AM2 = 5AM4 = 0.417P AM:) = 0.354P A R[ = 0.446wL AR2 = 2.153wL A R3 = 2.968wL AR4 = -O.446wL AR5 = 0 A R6 = 1.707wL

EA

511 = 522 = 53:1 = 5H = 1.354 L

- 524 =--EAL


- 3.3·9


- 3.3·10
- 3.3·11
- 3.3·12
- 3.3·13
- 3.3·14
- 3.3·15
- 3.3·16
- 3.3·17 3.3-18


3.3-19 3.3-20 3.3·21 3.3·22 3.3-23

EA

512 = -534 = -0.354 L

3.3-24

EA

511 = 522 = 53:) = 544 = 1.354 L

3.3·25

![image 690](Matrix Analysis of Framed Structures_images/imageFile690.png)

Answers to Problems 527

233 EA S'2- = S77 =--375 L EA 4L

- 3.3-26
- 3.3-27


###### 179 EA S55 = S99 = 375 L

###### EA S27 = --3L

wLJl 4j D = 66EI -1 D = PL2l-639]

D---PL2 l 7J

3.3-28

D=-PL2l 253J x

- 176EI -9

10-4 3.3-30

- 3.3-29


X 10-4

A"~~p ]-2L

EI -389

EI 472

A"~~[=U

- 3.3-31
- 3.3-32
- 3.3-33
- 3.3-34
- 3.3-35
- 3.3-36
- 3.3-37


27P 31P PL

27P

ARl =- AR2 = 56 AR3 =-

AR4 = 224

4'.. 7

3P 3PL

AR5 =-2 AR6 =ill

###### wL [-:g] - JwL [15]

A\I = 28 AH - 28

26L -4

###### 24E1

- (a)Su=V

6E1 S22 = S33 =-

L

E1 S23 =-L

12E1 EA

- (b) Su = S44 = V + 2L


3E1 EA

S22 = S55 = 2V + L

3E1 S25 = - 2U

3E1 S23 = S26 = -S35 = -S56 = 2L2

6E1

S33 = S66 = 6S36 = L

12E1

S22 = L

2E12

S34 = S56 = L

![image 691](Matrix Analysis of Framed Structures_images/imageFile691.png)

Answers to Problems

528

PL (2 + 71)(5 + 271) AM2 = -16 (1 + 71)(4 + 71)

P 5 + 271 AMI ="8 4 + 71

- 3.3-38
- 3.3-39
- 3.3-40
- 3.3-41
- 3.3-42


3PL 71 AM3 = 16(1 + 71)(4 + 71) D= wL3 [-LC_3

44+ TJ)] 24E/(l + 71)

P 11 + 271 ARI ="4 4 + 71

4EI 511 = 577 =-L

2EI 513 = 546 = 557 = ~L

511 = -514 = -546 = 566 = L 522 = 577 = -4EI

GJ

L

6EI 2EI 523 = -534 = -537 = - P 525 = 557 = L 5 - 4EI + 2GJ 555 = 8EI + GJ 44- L L L L

AR=301E/(t!..T7dLI-t!..T2)l-13il3.4-2

- 3.4-1


-1

Elf3

Elf3 4Elf3

- 3.4-3
- 3.4-4
- 3.4-5
- 3.4-6
- 3.4-7
- 3.4-8
- 3.4-9
- 3.4-10


AM2 = I2L A M3 = 9V

AMI = 4L2

7Elf3

61Elf3

ARI = 36L2

AR2 = - 36V

OIEI(t!..TI - t!..T2)

d ARI = AR3 = 0 AR2 = -AR4 = -AM2

AMI = {-2, 5L, 2, -7L}4/3I1IL where /3 = OIE/(t!..TI - t!..T2)/d

D = - 66EI/3L lL]6

D -- P:...[L52EI -4J

AM2 = {-2, 7L, 2. -9L}9/3/26L where /3 = OIE/(t!..TI - t!..T2)/d

D=-3t!..B8L AR = {-II, -lOL, 37, -26, I4L}3Elt!..B/8L3

A __ PL _ 6EIs DCI- 8 L2

P 6Elf3

###### ARC2 = 2" + -----v-

AMI = AM4 = -O.I745EAOIt!..T AM2 = AM3 = O.1277EAOIt!..T

![image 692](Matrix Analysis of Framed Structures_images/imageFile692.png)

529

Answers to Problems

###### V3EAe Am = 2Au3 = 4L

- 3.4-11
- 3.4-12
- 3.4-13
- 3.4-14


ADC= -EAU+../2exD.T)

###### EAs

###### A.lIC2 = - L ADel = EA(£ - 1.707exD.T) ADO = EA(£ + L707exD.T)

ADO = EA 0.354i - L707exD.T ADC4 = ADO - L

5 ) EAe

(

ADCI = AMCI = -EAexD.T

Chapter 4

###### PL2 P

- 4.9-1 DF = 384EI {7, -53} AR = 576 {351, 93L, 1049,427,765, -207L}

P P

AMI = 192 {117, 31L, 75, -IOL} AM2 = 288 {124, 15L, 308, -153L}

P

A:\!3 = 192 {-63, -90L, 255, -69L}

PL2 P

- 4.9-2 DF = - 240EI {6, 13L} AR = 240 {204, 48L, 516, 36L}

P P

AMI = 240 {204, 48L, 276, -84L} AM2 = 240 {240, 84L, 0, 36L}

PL2 P

- 4.9-3 DF = 144EI { -8,23} AR = 144 {24, 2L, 381, 237, -66, 34L}

P P

AMI = 72 {12, L, 60, -25L} AM2 = 144 {117, 50L, 27, 40L}

P

AM3 = 72 {lOS, 52L, -33, 17L}

- 4.9-4

PL2 P

DF = 528EI { -7L, 2} AR = 264 {228, 79L, 36, -19L}

P P

AMI = 264 {228, 79L, 36, 17L} AM2 = 264 {-36, -I7L, 36, -I9L}

- 4.9-5

wL3 wL DF = - 384EI {16, 15L, 36} AR = 4"" {I, 0, 6}

wL wL

AMI = 4"" {I, 0,3, -L} AM2 = 4""{3, L, -1, O}

- 4.9-6


###### PL2 P

DF = 416EI { 109, -36,9} AR = 416 {646, 24,1464,362, -86L}

![image 693](Matrix Analysis of Framed Structures_images/imageFile693.png)

530 Answers to Problems

###### P

AMI = 416 {646, 416L, -230, 22L}

p

AM2 = 416 {254, -22L, 578, -140L}

P

AM3 = 416 {470, 140L, 362, -86L}

###### PL2

- 4.9-7 DF = 272£1 {43L, 31, -91}

P

AR = - {78, -128L, -351,409, -125L} 136

P

AMI = 68 {39, -64L, -39, -33L}

P

AM2 = 68 {-29, 33L, -107, 6L}

P

AM3 = 136 { -137, -148L, 409, -125L}

- 4.9-8 Nonzero elements of rearranged SJ after factoring 2e:3:

SJ11 = 2SJ12 = 2/aSJ22 = 4SJ23 = 2/aSJ33 = 2SJ34 = SJ44 = 8V SJl5 = -SJI6 = SJ25 = -4jaSJ26

= -4Sm = 4SJ36 = 4jaSJ37 = -SJ38 = SJ47 = -SJ48 = 12L SJ55 = -SJ56 = %SJ66 = -8SJ67 = 8fgSJ77 = -SJ78 = SJ88 = 24

- 4.9-9 Nonzero elements of rearranged SJ after factoring ~!:
- 4.9-10
- 4.9-11


SJIl = 4SJI2 = 4SJ16 = 2/3SJ22 = 2SJ24 = SJ44 = 2SJ66 = 8L2 SJl5 = -SJl8 = -%SJ23 = Sm = lj3SJ28

= -%SJ34 = lj4SJ48 = SJ56 = -SJ67 = 6L 1fsSJ33 = -lj8SJ38 = SJ55 = -SJ57 = lj2Sm = -SJ78 = IfgSJ88 = 12

Nonzero elements ofrearranged SJ after factoring ~!: Sm = -SJI6 = SJ44 = -SJ47 = lj3SJ66 = -ifzSJ67 = 1faSJ77 = 12 SJl2 = SJl5 = SJ26

###### = _1h,SJ27 = - SJ34 = Ih,SJ36 = - SJ37 = - SJ48 = - SJ56 = SJ78 = 6L SJ22 = 3SJ23 = 6SJ25 = SJ33 = 6SJ38 = 3SJ55 = 3SJ88 = 12V

Nonzero elements ofrearranged SJ after factoring ~!:

SJ11 = 2SJ12 = Ih,SJ22 = 2SJ23 = Ih,SJ33 = 2SJ34 = Ih,SJ44 = 2SJ45 = SJ55

=4L2 SJl6 = - SJl7 = SJ26

= - SJ28 = SJ37 = - SJ39 = SJ48

= -SJ410 = SJ59 = -SJ510 = 6L SJ66 = -SJ67 = !h,SJ77 = -SJ78

= Ih,SJ88 = -SJ89 = Ih,SJ99

= - SJ910 = SJIOIO = 12

![image 694](Matrix Analysis of Framed Structures_images/imageFile694.png)

Answers to Problems 531

f . 2B

Nonzero elements 0 rearranged SJ after factonngV:

- 4.9-12


SJl1 = 4SJ13 = 4SJ18 = 4(3SJ33

= 8SJ34 = 2SJ44 = 8SJ46 = 4SJ66 = 2SJ88 = 8L2

-SJI2 = SJ17 = -2SJ23

- = 2SJ24 = SJ39 = -2SJ310 = -2SJ45 = -2SJ56 = 2SJ610 = SJ78 = -SJ89

= 6L SJ22 = -%SJ29 = -3SJ21o

- = 3SJ55 = -3SJ510 = 3h.Sm = -%SJ79 = 3/.SJ99 = 3h.SJ10l0 = 18


JiPL OF = Ji {I + Ji, \}

- 4.12-1
- 4.12-2
- 4.12-3
- 4.12-4
- 4.12-5


(1 + 2)EAx

###### AR = P0 {-(2 + 0). -(2 +0). - 2(1 +0), - 2V2,

2(1 + 2)

-0,0} AMI = P{ -1,0,1, O} AM2 = 1:vIz {-V2, -(1 +vIz), viz, - (1 +V2)}

P

AM3 = ------:-r= {I, 0, -1, O} l+v2 PL

OF = -EAx {1.30, 1.60} AR = P{ - 3.80, 1.50, -1.00, -0.600, -0.200, 1.10} AMI = P{ 1.30, - 2.00, -1.30, 2.oo} AM2 = P{O, 1.00, 0, 1.00}

- A~13 = P{ -1.60, 1.00, 1.60, l.oo} AM4 = P{0.5OO, 0.500, 0.500, 0.5OO} AM5 = P{ -0.500,0, 0.500, O} AM6 = P{O, 0, 0, O}

wL2 OF = -EAx {-1.26, O} AR = wL{O, 1.71, -0.446,0.446,2.15, 2.97} AMI = wL{O, 0.500, 0, 0.5OO} AM2 = wL{O, 0.500, 0, 0.5OO} AM:) = wL{0.500, 0, 0.500, O} AM4 = wL{1.76, 0, -0.762, O} AM5 = wL{-0.500,0.500, -0.500, 0.500} AM6 = wL{1.131, 0.500,0.13\, 0.500}

wL2 OF = -EAx {-0.288, -0.815, -0.73!} AR = wL{-0.0630,0.351,2.48, -0.288, 2.32} A~ll = wL{ -0.288,0.300,0.288, 0.300} AM2 = wL{O, 0.300, 0, 0.300} AM3 = wL{1.22, 0, -0.416, O}

- A~14 = wL{1.l3, 0, -0.332, O}
- A~15 = wL{0.080, 0.300, -0.880, 0.300} A"6 = wL{0.985, 0.300, -0.185, 0.300}


###### PL

OF = -EAx {0.667, -2.00, -4.00} AR = P{ -2.40, 0.700, 0.211, 0.700, 4.79}

A,ll = P{0.667, 1.00, -0.667, 2.00} A,12 = P{O, -1.00,0, -1.00} A,I:) = P{1.40, 0, -1.40, O} A,14 = P{2.07, 0, -2.07, O} A,lc, = P{4.33, 0.500, -2.60, 0.500}

![image 695](Matrix Analysis of Framed Structures_images/imageFile695.png)

Answers to Problems

532

###### WL2

DF = -EAx {-2.92, -2.92} AR = wL{ -1.40,1.40, -1.40,2.25,1.40, 2.25}

- 4.12-6
- 4.12-7
- 4.12-8
- 4.12-9
- 4.12-10


A~H = wL{O, 0.400, 0, 0.400} A~12 = wL{O, 0.400, 0, 0.400} Am = wL{0.300, 0, 0.300, O} A"4 = wL{0.150, 0, 0.150, O}

A~15 = wL{ -2.05,0.400, 1.45, 0.400} A~16 = wL{2.05, 0.400, -1.45, 0.400}

NonzeroelementsofSJafterfactoringE:x:

SJIl = -2SJ15 = -2SJ17 = _2/3SJ26 = -2(3S.l28 = _2/3SJ36 = 2/3S J38

= -2(35,,·> = z/3SJ47 = 0.500 SJ16 = -SJ18 = SJ25 = -S'/27 = SJ46 = S.148 = -0.433 SJ22 = 3.23 S.l24 = -1.73 SJ:l3 = -2SJ35 = -2S./37 = SJ44 = 2.60 S./55 = Sm = 2.55 SJ56 = SJ66 = - SJ78 = SJ88 = 1.18 S.l57 = -1.00

Nonzero elementsofSJ afterfactoring L:EA,

SJ11 = S.I:13 = 1.38 SJI2 = _1/2SJI6 = SJ18 = _1/ZS./25 = SJ27 = -S.l34 = I/2SJ36 = -S.l310

= I/2SJ45 = -SJ49 = I/2SJ57 = 1/2S J59 = 3/ZSJ68 = 3/2SJ610 = -0.217 SJI3 = 4S.l15 = 8SJI7 = -0/9SJ22 = 4/3S./26 = %S.I28 = 4S.I35 = 8S.m = -S/9SJH = 4(3SJ46 = 8hSJ410 = 4S.l58 = -45J510 = 4SJ6,

= -4S./69 = -1.00 S./55 = 1.368 S./66 = 1.79 SJ77 = SJ99 = 0.559 SJ78 = -S./910 = 0.467 SJ88 = SJIOIO = 0.520

###### EAy

Nonzero elements of rearranged S,l after factoring T:

SJll = SJ33 = SJ77 = SJ99 = 1.71 SJI2 = SJ27 = SJ35 = SJ49 = -1.00 SJ22 = 2.71 SJI4 = SJI5 = - SJ16 = - SJ23 = S./29 = SJ210 = SJ:J9 = SJ310 = SJ46

= SJ47 = - SJ48 = SJ56 = - SJ57 = S./58 = - SJ66 = SJ78

= - SJ88 = - SJ910 = - S./IOIO = -0.707 SJ44 = SJ55 = 2.41

###### EA,

Nonzero elements of SJ after factoring T:

SJ11 = SJ33 = I/3S.l55 = Ij3SJ77 = Ij2SJ99 = Ij2SJ1111 = 2.03 SJ12 = 4(3SJ17 = - SJ18 = - SJ27 = 3/4S.l28 = - SJ:J4 = 4/3SJ35 = SJ36

= SJ45 = 3/4S J46 = 2/3SJ511 = _1/2SJ512 = _1/2S./611 = 3/8SJ612

= 2/3SJ79 = Ij2SJ710 = Ij2SJ89 = 3/sSJ810 = - Ij2SJ910 = _3/sSJ10l0

= I/2SJ1112 = _3/SS./1212 = -0.480 S./15 = SJ37 = Ij2S./59 = Ij2SJ711 = -1.67 SJ22 = SJ44 = 1.89 SJ24 = I/2SJ68 = -1.25 SJ56 = -S}78 = -0.480 SJ66 = S./88 = 4.42

###### Answers to problems for Sec. 4.18 in US units are kips, inches, and radians; those in SI units are kilonewtons, meters, and radians.

- 4.18-1 DF = {-4.38, -19.3, 5.32} X 10-4 AR = {0.913, 5.97, 227.7, - 0.913,4.03, 43.59}


![image 696](Matrix Analysis of Framed Structures_images/imageFile696.png)

- Answers to Problems 533
- 4.18-2
- 4.18-3
- 4.18-4
- 4.18-5
- 4.18-6
- 4.18-7
- 4.18-8
- 4.18-9


AMI = {0.913, 5.97, 227.7, -0.913,4.03, -87.94} AM2 = {4.03, 0.913, 87.94, -4.03, -0.913, 43.59} DF = {-2.16, -35.8, 4.24} X 10-4

AR = {0.360, 3.34, 249.6, 0.360, -0.303,28.19, -0.720,8.96, 46.00} AMI = {0.360, 3.34, 249.6, -0.360,2.66, -151.5} AM2 = {-0.360, 0.303, 59.09,0.360, -0.303, 28.19} AM3 = {8.96, 0.721, 92.36, -8.96, -0.721, 46.0} DF = {0.7491, -0.1650, 1.980} X 10-4 AR = {-24.97, 39.00, -62.29, -25.03, 11.00, 44.49}

A~11 = {24.97, 11.00,44.31, -24.97,39.00, -62.29} AM2 = {I 1.00, 25.03, 44.49, -11.00,24.97, -14.31} DF = {0.5934, -2.225, -1.466} X 10-4

AR = {-20.77, 19.54, 20.36, -20.77, 62.58, -66.02, -38.47, 77.89, 38.21}

A~11 = {-20.77, 19.54,20.36,20.77,20.46, -22.21} A~12 = {20.77, 57.42, 50.56, -20.77,62.58, -66.02} AM3 = {77.89, 38.47, 38.21, -77.89,41.54, -44.35} DF = {O, -0.000620, O}

AR = {-0.323, -8.55,0,0.434,0,0.323, 1.57, 8.77} Am = {-0.434, 0, 0, 0.434, 0, O} A\I~ = {1.52, 0.503, 8.77, 0.215, 0.497, -8.55} DF = {0.5302, -1.457, -0.02613} X 10-4 AR = { -141.40, -63.40, 5.444, 51.40, 93.40, 40.75}

A~11 = {141.40, 63.40, 4.747, -141.40, -63.40, 5.444} A~12 = {102.39, 29.70, 40.75, -144.81, 12.73, -4.747} DF = {0.4160, -0.9615, 0.1880} X 10-4

AR = {-13.87, 24.77, 33.35, -20.80, 13.29, -18.00,34.66,61.94, 17.23}

AMI = {-13.87, 24.77, 33.35,13.87,5.235, -4.765} AM2 = {20.80, 6.707, 4.824, -20.80, 13.29, -18.oo} AM3 = {70.35, 9.435, 17.23, -46.35,8.565, -0.059} Nonzero elements of SJ:

SJII = S.l44 = 1541.7 SJi3 = S.l19 = - S.l37 = SJ46 = SJ412 = - SJ610 = - S.l79

= - SJ1012 = 5000.0 S.l14 = Ij2S.J28 = I/2S.l511 = - Ij2SJ88 = - Ij2SJi111 = -1500.0 SJ17 = SJ410 = -SJ77 = -SJIOIO = -41.7 S.l22 = SJ55 = 3005.2 SJ23 = SJ26 = -SJ35 = -SJ56 = 1250.0 SJ25 = -5.22

- 1/3S J33 = 2SJ36 = S.l39 = 1(3SJ66 = S'612 = I/2SJ99 = 1(2SJ1212 = 4.0 X 105 Nonzero elements of rearranged SJ: SJ\l = Sm = 3041.7 SJi3 = S'19 = SJ23 = SJ26 = - SJ35 = - S'37 = - SJ79 = 5000.0 S'14 = Sm = - S'88 = - 3000.0 S'17 = SJ25 = - SJ77 = -41.7
- 1/4SJ!'.o = SJ36 = SJ39 = 5/18S.l66 = 5/4S'612 = lj2S'99 = 5/sSJ1212 = 4.0 X 105 SJ44 = 3877.7 SJ45 = -S'4l1 = -S'510 = S'I011 = -1143.0 S.l46 = SJ412 = -S'61O = -S.l1012 = 2560.0 S.l410 = -SJIOIO = -877.7 SJ55 = 1585.0 S'56 = -3080.0 S.l511 = -SJl111 = -1543.7 SJ512 = -S.l611 = -S.l11I2 = 1920.0


![image 697](Matrix Analysis of Framed Structures_images/imageFile697.png)

Answers to Problems

534

- 4.19-1
- 4.19-2


Nonzero elements of SM:

SMII = -SMI4 = SM44 = -L SM22 = -SM25 = SM55 = -3-12ElL z

Glx

Cx 0 cz]

R = [ 0 1 0

###### 4Elz SM33 = 2SM36 = SM66 = --L

Elements of SMS:

SMSII = SMS44 = (Glx ci + 4Elz C~)IL

- SMS22 = SMS55 = -SMS25 = 12ElzIL3 SMS33 = SMS66 = (GIx C~ + 4Elz Ci)IL

-CZ 0 Cx

SMSI2 = -SMSI5 = SMS24 = -SMS45 = -6Elz CzIL2 SMSI3 = SMS46 = (Glx - 4EIz) Cx CzIL

- SMS23 = SMS26 = -SMS35 = -SMS56 = 6Elz CxlL2 SMSI4 = -(Glx ci - 2EIz C~)IL SMS36 = -(Glx C~ - 2Elz Ci)/L SMSI6 = SMS34 = -(Glx + 2Elz) CxCzIL


- -(AMSki = -CX(AMdl.i + CZ(AMLh.i
- -(AMSh.i = -(AMLh.i
- -(AMSh.i = -CZ(AML)l.i - CX(AMLh.i
- -(AMSki = -CX(AMLki + CZ(AML)6.i
- -(AMSh.i = -(AMLh.i
- -(AMS)6.i = -CZ(AMLki - CX(AML)6.i


- 4.20-1
- 4.20-2
- 4.20-3
- 4.20-4


(AM)l,i = (AMLki + Glx {[(Dj)jl - (Dj)kll Cx

+ [(Dj )j3 - (Dj )k31 Cz}/L

(AMh.i = (AMLh.i - 6EIz {[(Dj)jl + (Djhll CzL - 2 [(Dj)j2

- (Djh21 - [(Dj )j3 + (Djh31 CxL}/L3

(AMh.i = (AMLh.i - 2EIz {[2(Dj)jl + (Dj)kll CzL - 3 [(Dj )j2

-(Dj)d - [2(Dj )j3 + (Dj h31 CxL}/L2

(AMki = (AMLki - Glx {[(Dj)jl - (Dj)kll Cx

+ [(Dj )j3 - (Dj )k31 Cz}/L

(AMh.i = (AMLh.i + 6Elz {[(Dj)jl + (Dj)kd CzL - 2[(Dj )j2

-(Dj h21 - [(Dj )j3 + (Dj>t31 CxL}/L3

(AM)6.i = (AMLki - 2EIz {[(Dj)jl + 2(Dj )kd CzL - 3 [(Dj )j2 - (Dj h21 - [(Dj )j3 + 2(Dj h31 CxL}/L2

4.22-1

![image 698](Matrix Analysis of Framed Structures_images/imageFile698.png)

###### 535

Answers to Problems

Cy

4.22-2

CxlCxy -CyCZICxy

- 4.23-1
- 4.23-2
- 4.23-3
- 4.23-4


- -(AMS)U = -(Cx CXy AMI.1 - Cy AMI.2 - Cx Cz AMU)/Cxy
- -(AMSh.i = -(Cy CXy AMLI + Cx AML2 - Cy Cz AMU)/Cxy
- -(AMShi = -(Cz AMI.1 + CXy AMu)
- -(AMSki = -(Cx CXyAMIA - CyAMI.S - Cx CZAML6)/Cxy
- -(AMSki = -(Cy CXY AMIA + Cx AMLS - Cy Cz AM/6)/CXY
- -(AMSki = -(Cz AMIA + CXy AMU,)


(AM)I., = (AML)!., + {[(Dj)jl - (Dj)kI] Cx + [(D}),"

- (Dj)d C y + [(D})" - (Dj)o] Cz} EAxlL (AMh.i = (AMLh.i (AMhi = (AM/h)

(AM)4.i = (AMIki - {[(Dj)jl - (Dj),I] Cx + [(Dj )j2

- (Dj)d Cy + [(Dj)j, - (Dj ),,] Cz} EAxlL (AM)s.i = (AML)S.i (AM)6.i = (AMd6.i

[fflv'J4

R= ~ -3~ ~]

4.24-1

5

###### .J3 2.J3

Chapter 6

- 6.4-1 -bL2

0 0

0 -b2(3a + b) 6ab

I 0 -ab2L b(2a - b)L

TML =-L} -aL2 0 0 0 -a2(a + 3b) -6ab 0 a"bL a(2b - a)L

- 6.4-2 -bL2


0 0 0 b(2a - b)L ab2L

I 0 -6ab -b2(3a + b) TML =-

L3 -aL2 0 0 0 a(2b - a)L -a2bL 0 6ab -a2(a + 3b)

![image 699](Matrix Analysis of Framed Structures_images/imageFile699.png)

###### 536 Answers to Problems

- 6.4-3 TMLII = TML22 = TML33 = -biL TMIAI = TML52 = TML62 = -aiL TML25 = -TML34 = -TML55 = TML64 = ilL
- 6.4-4 TMLI.I = TML4.4 = -biL TMU,I = TML10.4 = -aiL TML2,2 = TML3,3 = -b2(3a + b)IL3 TML8,2 = TML9,3 = -a2(a + 3b)IL3 TML5,3 = -TML6,2 = ab21L2 TMI,12,2 = -TML1 1.3 = a2blL2 TML2,6 = -TML3,5 = -TML8,6 = TML9,5 = 6ablLJ TML5,5 = TML6,6 = b(2a - b)IL2 TML1 1.5 = TMLI2,6 = a(2b - a)IL2


- 6.5-1
- 6.5-2

wL

AML = 12 {a, -L, 6,0, L, 6}

- 6.5-3

wL

AMI, = 2 {Cy, Cxz, 0, Cy, Cxz, o}

- 6.5-4


wL

AML = 12 {6Cy, 6Cxz cos ex, -6Cxz sin ex, 0, LCxz sin ex, LCxz cos ex,

6Cy, 6Cxz cos ex, -6Cxz sin ex, 0, -LCxz sin ex, -LCxz cos ex}

###### 6.11-1

[-,L' ° °

###### 6.11-2 TMLk = ~3 ~ aL(2b - a) -a'bL ]

6ab -a2(a + 3b)

[ -bL' ° °

= ~3 ~ -b2(3a + b) oob ]

###### 6.11-3 T MLj

-ab2L bL(2a - b)

[-bL' ° °

= ~3 ~ bL(2a - b) ,b'L ]

###### 6.11-4 T MLj

-6ab -b2(3a + b)

6EI l30

- 6.12-1 a) Flexibility Approach:


l

###### l

3 l-23L

TMLkI = 217L 22L2 - 36

57L

-

SMkk = 217L3 -57L

130L2

25L

![image 700](Matrix Analysis of Framed Structures_images/imageFile700.png)

Answers to Problems 537

l-148L

b) Stiffness Approach:

32L108l

1 -76L2

T --

- -108

75L

58L2

- -33L 30 41L2 -57L


l30

ML - 217L -69L 66L2

svm'l

6EI 33L

S ---

M - 217L3 -30 57L

###### 130L2

- 6.12-2
- 6.12-3
- 6.12-4
- 6.12-5
- 6.12-6


- a) Flexibility Approach:

4EI 142

SMkk = 1201L3 L-87L

-87L l

266L2

3 1-243L - 1201

TMLkI = 1201L L 246L2 77d

- b) Stiffness Approach:


1 l-47U-696L2 3W368Ll

'yml

TML = 1201L -729L -360

738L2 231L

42

4£1 l123L

446L2

SM = 1201L3 -42 -123L 42

87L

169L2 -87L 266L2

- (Similar to Prob. 6.12-1)

6EI 130 33Ll

SMii = 217L3 L33L 58L2

- (Similar to Prob. 6.12-2)


1 1-148L 108l

TMLil = 217L L-76L2 32L

(etc.)

4EI 142 123Ll

1 1-472L 360l

TMLil = 1201L L-696L2 368L

(etc.)

SMii = 1201L3 L123L 446L2

l 1130P -751l

FMii = 36Elz L-751 66

(Axial influences not coupled with flexural) a) Flexibility Approach:

2EA 2 SMkk = 3L T MW = 3

![image 701](Matrix Analysis of Framed Structures_images/imageFile701.png)

Answers to Problems

538

S = 2EAII

b) Stiffness Approach:

###### -IJ 1

TML = -~ llJ = lTMLllJ

M 3L -I

3 2 TMLAI

1 4

- 6.15-4
- 6.15-5
- 6.15-6
- 6.15-7
- 6.15-8


a l-a(ae4 + 3b) TMLk = L3e ab(ae4 + b)

L l2L2ek3 -3Lek2J 2Elzl6ejk 3Lek2J

T 2Elzl-6ejk 3Lej2J S = 2Elzl6ejk -3Lej2J

~=-- ~=-3- 2

6Elz - 3Lekl 6ejk L eJ 3Lek2 2L ek3

SMjk = SMkj = -3- Mkk 3

LeJ -3Lek2 L2 .. Lejt -3Lej2 2L2ej3 where ejt = I + 4ej + 4ek + 12ejek

AFll = r2(1 - cos ¢)2/SE AF21 = _r2(1 - cos ¢) sin ¢/SE = AF12 AF31 = -r(1 - cos ¢)/SE = AFI3 AF22 = r2 sin2 ¢/SE AF32 = r sin ¢/SE = AF23 AF33 = 2/SE

4EI l6 -7L J

- 6.16-1


SMkk = (II + 6g)L3 -7L (10 + g)L2

2 l-3(3 + 2g)L -12 J

TMLk = 3(11 + 6g)L (5 + 4g)L2 3(1 - 2g)L

![image 702](Matrix Analysis of Framed Structures_images/imageFile702.png)

Answers to Problems

539

- 6.16-2
- 6.16-3
- 6.16-4
- 6.16-5 6.17-1


11gP

A(FMjj)I I = 36Elz (others unchanged)

fL (1 rU4 dx' ) A(FMkk)1I = GAx :2 + 2 Jo L + 4x' (others unchanged) (SMBh.6 = -b(SI4d- SISC + S16) + a(S24d - S2SC + S26)

+ S34d - S3SC + S36

- 6.17-2
- 6.17-3
- 6.17-4


![image 703](Matrix Analysis of Framed Structures_images/imageFile703.png)

###### Index

Action equations 25, 33 Actions, corresponding 10

Bending moment 4,477 Bending plane 2 Body forces 450 Buckling of frames 432

definition of 7 generalized 7 internal 8 nodal 450 notation for 12 virtual 46

Castigliano's first theorem 43 Castigliano's second theorem 43 Cholesky method 506

Answers to problems 523 Antisymmetric loads 378 Arbitrary numbering systems 190 Arithmetic operations 292

modified 508 square root 507

Combined joint loads 36, 124, 195 Combined program for framed structures 368 Compatibility 14, 57 Compatibility matrix 159 Complementary strain energy 41 Complementary virtual strain energy 47 Complementary virtual work 47 Complementary work of loads 42 Complete member stiffness matrices 184 Computer programs, Chapter 5 and Appendix

numbers of (table) 512 Assembled flexibility matrix 94 Assembled stiffness matrix 160 Automatic dead load analysis 386 Axes, member-oriented 86 restraint-oriented 390 structure-oriented 86

Axial constraints in frames 432 Axial deformations 5,70, 141,476 Axial element 453 Axial-flexural interactions 428 Axial force 4, 476 Axial rigidity 477 Axial strains, constraints against 432 Axis transfromations, rotational 233, 239

D

combined, for framed structures 368 data for 300 for beams 309 for grids 340 for plane frames 330 for plane trusses 325 for space frames 355 for space trusses 345 identifiers used in (table) 299 outline of 306

translational 394

Banded matrices 307, 514 Beam-column effect 428 Beam sign convention 6 Beams, analysis by flexibility method of 56,

Computer routines for solving equations,

Appendix D Condensation, matrix 407,432 Connections, elastic 419 Connections, offset 424 Conservation of energy 42 Conservative systems 38 Constraint matrix 434 Constraints, redundant 433 Constraints for repeatability 381 Constraints in frames, axial 432 Coordinates, global 86

63, 80, 101 analysis by stiffness method 118, 129, 162,

199 computer program for 309 definition of 2 deformations in 6 joint displacements in 80 member flexibilities of 88 member stiffnesses of 125, 134, 153, 190 nonprismatic 402 table of displacements for 494

local 86

541

![image 704](Matrix Analysis of Framed Structures_images/imageFile704.png)

###### Index

###### 542

Corrsponding actions and displacements 10 Crotti-Engesser theorem 43 Cumulative restraint list 210 Curvature 461 Curved members 409

Factorization of symmetric matrices 506 Finite-element method 447

virtual-work basis of 449

Fixed-end actions, Appendix B due to end-displacements 502 due to loads 499 due to prestrains 501 due to temperature changes 500 for truss members 503 from flexibilities 396 matrices of 195

Data for programs 300 Dead load analysis, automatic 386 Decomposition of symmetric matrices 506 Deflections (see Displacements) Deformations, virtual 45 Deformations of members 4,476 Degrees of freedom 18 Degrees of kinematic indeterminacy 18 Degrees of static indeterminacy 15 Differential operator, linear 450 Direct stiffness method (see Stiffness method) Direction cosines 216, 233, 240 Dicontinuities in members 414 Displacement equations 25, 32 Displacement method (see Stiffness method) Displacement shape functions 450 Displacements 6, Appendix A

Flexibilities, definition of 25, 28 of beam member 88 of grid member 90 of plane frame member 89 of prismatic members 86 of space frame member 91 of truss member 88

Flexibility coefficients 28, 33, 60 cross 33 direct 33 reciprocal theorem for 44

Flexibility matrix 31, 61, 93 inverse of 33 member 86 of assembled structure 94 of unassembled structure 93 symmetry of 44

corresponding 10 definition of 9 due to shear 483 generalized 10 nodal 450 notation for 12, 28 relative 92 table of (for beams) 494 unit-load method for 47,485 virtual 45 (see also Joint displacements and Support

Flexibility method, Chapter 2 formalization of 92 joint displacements by 80 prestrain effects in 75, 84 reactions by 80 support displacements in 60, 75, 84 temperature changes in 75, 84

displacements) Dummy-load method (see Unit-load method)

Flexible connections 419 Flexible supports 391 Flexural deformations 5, 477 Flexural element 458 Flexural rigidity 464, 479 Flow charts, 291

Eccentric connections 424 Elastic connections 419 Elastic structures 5, 25, 476 Elastic supports 391 Element stiffness matrix 452 Elimination, Gaussian 511

for beams, 315 for combined program 370 for grids 341 for plane frames 332 for plane trusses 326 for space frames 355 for space trusses 348 symbols for statements in 294

Gauss-Jordan 434 End-actions for restrained members, Appendix

B (see also Member end-actions) Energy concepts 38 Equations, solution of 506 Equilibrium 13

Force method (see Flexibility method) Forces, body 450 Formalization of the flexibility method 92 Formalization of the stiffness method 157 FORTRAN programming 291 Framed structures, types of 1

equations of 13, 120 Equilibrium matrix 93 Equivalent joint loads 36, 93, 124, 150, 182,

193 Equivalent nodal loads 452

![image 705](Matrix Analysis of Framed Structures_images/imageFile705.png)

###### 543

###### Index

Kinematic equivalents 395 Kinematic indeterminacy 14, 18 Kinematic instability 21 Kinematic redundants 18 Kinematics matrix 159

Frames axial constraints in 432 deformations in 6, 7 plane, definition of 2 space, definition of 3 (see also Plane frames and Space frames)

Linear differential operator 450 Linearly elastic structures 5, 25, 476 Loads, antisymmetric 378

Gaussian elimination 511 Gauss-Jordan elimination 434 Generalized displacement 10 Generalized force 7 Generalized stresses and strains 462 Geometry, equation of 57 Global coordinates 86 Grids, analysis by flexibility method of 73

combined joint 36, 124, 195

equivalent joint 36,93, 124, 150, 182, 193 equivalent nodal 452 fixed-end actions due to (table) 499 joint (actual) 36, 193 nodal (actual) 450 rearranged 197 symmetric 378 virtual 46 work done by 41 (see also Joint loads)

analysis by stiffness method of 146, 258 computer program for 340 definition of 2 deformations in 7 member flexibilities of 90 member stiffnesses of 155, 254

Loads between joints 383 Local coordinates 86

Material, isotropic 448 Matrix condensation 407, 432 Maxwell-Mohr method 55 Maxwell's theorem 44 Member discontinuities 414 Member end-actions 80, 92, 126, 183

Hinges in members 414 Hooke's law 5, 24, 476

Identifiers used in computer programs (table)

299 Inclined supports 389 Indeterminacy, kinematic 14, 18

for beams 198, 208 for grids 260 for plane frames 249 for space frames 281 for trusses 227, 238, 269 tables of, Appendix B

static 14 Initial strains 452 (see also Prestrains) Integrals of products (table) 496 Isotropic material 448

Member flexibilities (see Flexibilities) Member flexibility matrices 86 Member-oriented axes 86 Member stiffness matrices 153 Member stiffnesses, from flexibilities 396 (see

Joint displacement indexes 192 Joint displacements 80

fixed-end actions due to (table) 502 numbering of 192,201,221

also Stiffnesses)

Joint loads, for beams 36, 193, 205 for grids 259 for plane frames 247 for plane trusses 225 for space frames 279 for space trusses 268 (see also Loads)

Members, curved 409

numbering of 199, 219 Mobile structures 21 Multi-story buildings 374

Nodal displacements 450 Nodal loads, actual 450

Joint restraint list 210 Joint stiffnesses, for beams 125, 202

equivalent 452 Nodes of finite elements 447 Nonprismatic members 402 Nonrigid connections 419 Normal strains 39 Normal stresses 38 Notation, explanation of 12, 58, 121 Notation (tables) 470

for grids 254 for plane frames 241 for plane trusses 215 for space frames 270 for space trusses 261 (see also Stiffnesses)

Joints, types of I numbering of 199, 219

![image 706](Matrix Analysis of Framed Structures_images/imageFile706.png)

###### 544

###### Index

Numbering systems, arbitrary 190 Numbers of arithmetic operations (table) 512

Relative displacements 92 Released structure 56 Releases in members 414 Repeatability, rotational 381

Oblique supports 389 Offset connections 424 One-dimensional elements

translational 381 Repeated structures 378, 381 Restrained members, end-actions for,

axial 453 flexural 458 torsional 455

Appendix B Restrained structure 118

Over-all joint stiffness matrix 184

Restraint displacements (see Support displace-

ments) Restraint-oriented axes 390 Rigidity, axial 477

P-.:l effect 428 Plane frames, analysis by flexibility method of

70, 104 analysis by stiffness method of 141, 167,

flexural 464, 479 torsional 463, 481

Rotational repeatability 381 Rotation of axes, for grids 258

245 computer program for 330 definition of 2 deformations in 6 effect of axial deformations in 70, 141,432 member flexibilities 89 member stiffnesses of 154, 241

for oblique supports 390 for plane frames 243 for plane trusses 236 for space frames 271 for space trusses 262, 264 three-dimensional 239 two-dimensional 233

Plane of bending 2 Plane trusses, analysis by flexibility method of

67,78,97 analysis by stiffness method of 135, 165,

Rotations 9

Section properties (table) 505 Shape functions, displacement 450 Shear-center axis 425 Shearing deformations 5, 7, 422, 482 Shearing force 4, 482 Shearing rigidity 483 Shearing strains 39 Shearing stresses 38 Sign convention, beam 6

219 computer program for 325 definition of 2 deformations in 6 member flexibilities of 88 member stiffnesses of 138, 154,215,236

Prestrains, in flexibility method 75, 84 in stiffness method 149, 387 table of fixed-end actions due to 501

Principle of complementary virtual work 47 Principle of conservation, of energy 42

statics 6 Solution of equations 506 Solution without rearrangement 520 Space frames, analysis by stiffness method of

of complementary energy 42 Principle of superposition 13, 22 Principle of virtual work 45 Product integrals (table) 496 Programs, computer (see Computer programs) Properties of sections (table) 505

277 computer program for 355 definition of 3 deformations in 7 member flexibilities of 91 member stiffnesses of 156, 185,270 principal axes for members in 271 vertical members in 275

Reactions 80, 95, 126, 160, 183, 198 Rearranged load vector 193, 196 Rearranged stiffness matrix 193, 196 Reciprocal relations 44 Rectangular framing 374 Redundancy (see Indeterminacy) Redundant constraints 433 Redundants, kinematic 18

Space tmsses, analysis by stiffness method of

267 computer program for 345 definition of 2 deformations in 6 member flexibilities of 88 member stiffnesses of 154. 261

static 15 References 468

![image 707](Matrix Analysis of Framed Structures_images/imageFile707.png)

###### 545

###### Index

selection of member axes for 263 vertical members in 264

Strain-stress relationships 448 Strains, initial 452 (see also Prestrains) Strains, normal 39

Static equilibrants 398 Static equilibrium 13 Static equivalents 394 Static indeterminacy 14 Static redundants 15 Statics matrix 93 Statics sign convention 6 Stiffness coefficients 29,33, 119, 122

shearing 39 virtual 45

Stress resultants, 2, 4, 8, 476 Stress-strain relationships 449, 451 Stresses, in members 476

normal 38 shearing 38 virtual 46

cross 33 direct 33 reciprocal theorem for 44

Stresses and strains, generalized 462 Stresses and strains in continua 448 Structural mobilities 21 Structure-oriented axes 86 Subprogram BANFAC 514

Stiffness matrix 31,33, 123 element 452 inverse of 34 member 153 of assembled structure 160 of unassembled structure 158 over-all joint 184 rearranged 196 symmetry of 44

BANSOL 518 FACTOR 512 SOLVER 514

Superposition, conditions for 24 equationsof23, 57, 61, 83,120,122,127, 149

Stiffness method, Chapters 3-6 computer programs for, Chapter 5 direct 181 formalization of 157 member end-actions in 126, 160 outline of 183 prestrain effects in 149, 387 reactions by 126, 160 results for 197 steps in the 183 support displacements in 149, 388 temperature effects in 149, 387

principle of 13, 22 Support displacements 60, 75, 84, 149, 388 Support reactions (see Reactions) Supports, elastic 391

oblique 389 types of 1

Symmetric loads 378 Symmetric matrices, factorization of 506 Symmetric structures 378

Temperature changes 75, 84, 149, 387

fixed-end actions due to (table) 500 Temperature deformations 484 Torsion constant 482

Stiffnesses, definition of 26, 29 for beam member 125, 134, 153, 190 for grid member 147, 155,254 for members with axial forces 428 for members with releases 414 for members with elastic connections 419 for members with shearing deformations

table 505 Torsional deformations 5,480 Torsional element 455 Torsional rigidity 463, 481 Transfer matrices for fixed-end actions 384,

422 for nonprismatic members 402 for plane frame member 154, 241 for plane truss member 138, 154,215,236 for prismatic members 153, 184 for space frame member 156, 185, 270 for space truss member 154, 261 joint 125, 192 (see also Joint stiffnesses)

399 in curved members 412 in members with axial-flexural interaction

431 in members with elastic connections 421 in members with releases 416 in members with shearing deformations 424 in nonprismatic members 406

Strain-displacement relationships 450 Strain energy 40

Translation of axes 394 Translational repeatability 381 Translations 9 Truss members, end-actions for (table) 504

complementary 41 complementary virtual 47 virtual 45

![image 708](Matrix Analysis of Framed Structures_images/imageFile708.png)

###### Index

###### 546

Trusses, defonnations in 6 plane, definition of 2 space, definition of 2 (see also Plane trusses and Space trusses)

Virtual actions 46 Virtual defonnations 45 Virtual displacements 45 Virtual loads 46 Virtual strain energy 45 Virtual strains 45 Virtual stresses 46 Virtual work 44

Twist 456 Twisting moment 5, 480

Unassembled flexibility matrix 93 Unassembled stiffness matrix 158 Unit-displacement method 46 Unit-load method 47, 485 Units, US and SI 306 Unstable structures 21, 432

Virtual-work basis of finite-element method 449

Work of loads 41

Vertical members, in space frames 275 in space trusses 264

complementary 42 Working points 425

![image 709](Matrix Analysis of Framed Structures_images/imageFile709.png)

###### ORDER FORM

Computer Programs for Matrix Analysis ofFramed Structures, Third Edition, by William Weaver, Jr. and James M. Gere, Van Nostrand Reinhold, 1990.

Please send me a diskette contammg the FORTRAN source code and example data sets for the programs CB, PT, PF, GR, ST, and SF that are described in Chapter 5.

I would like to receive a (check one) o S±" diskette for an IBM PC. o 3~" diskette for a Macintosh II PC.

I enclose a check for $50.00 payable to Dr. Paul R. Johnston. Residents of the State of California should add $3.50 sales tax.

Send orders to:

Dr. Paul R. Johnston 838 Mesa Court Palo Alto, California 94306

Name and address:

