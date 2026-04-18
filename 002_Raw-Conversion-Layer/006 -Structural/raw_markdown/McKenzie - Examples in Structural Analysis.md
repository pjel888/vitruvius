![image 1](McKenzie - Examples in Structural Analysis_images/imageFile1.png)

###### Examples in Structural Analysis

### Also available from Taylor & Francis

Structures: From Theory to Practice A.Jennings Hb: 0-415-26842-7 Pb: 0-415-26843-5

Structural Analysis, 5th Edition A.Ghali, A.Neville & T.G.Brown Hb: 0-415-28091-5 Pb: 0-415-28092-3

Free-standing Tension Structures B.B.Wang Hb: 0-415-33595-7

Reinforced Concrete Designer’s Handbook, 11th edition T.Threlfall & J.C.Steedman Hb: 0-419-25820-5 Pb: 0-419-25830-2

Reinforced and Prestressed Concrete, 4th edition S.Teng & F.K.Kong Hb: 0-415-31627-8 Pb: 0-415-31626-X

Wind Loading of Structures, 2nd edition J.Holmes Hb: 0-415-40946-2

Information and ordering details For price availability and ordering visit our website www.tandfbuiltenvironment.com Alternatively our books are available from all good bookshops.

# Examples in Structural Analysis W.M.C.McKenzie

![image 2](McKenzie - Examples in Structural Analysis_images/imageFile2.png)

LONDON AND NEW YORK

First published 2006 by Taylor & Francis 2 Park Square, Milton Park, Abingdon, Oxon OX14 4RN

Simultaneously published in the USA and Canada by Taylor & Francis 270 Madison Ave, New York, NY 10016, USA

Taylor & Francis is an imprint of the Taylor & Francis Group, an informa business This edition published in the Taylor & Francis e-Library, 2006.

“To purchase your own copy of this or any of Taylor & Francis or Routledge’s collection of thousands of eBooks please go to http://www.ebookstore.tandf.co.uk/.”

© 2006 William M.C.McKenzie Publisher’s Note This book has been prepared from camera-ready copy supplied by the author. All rights reserved. No part of this book may be reprinted or reproduced or utilised in any form or by any electronic, mechanical, or other means, now known or hereafter invented, including photocopying and recording, or in any information storage or retrieval system, without permission in writing from the publishers. The publisher makes no representation, express or implied, with regard to the accuracy of the information contained in this book and cannot accept any legal responsibility or liability for any efforts or omissions that may be made. The author has asserted his right to be indentified as the author of this work in accordance with the Copyright, Designs and Patents Act 1988 British Library Cataloguing in Publication Data A catalogue record for this book is available from the British Library Library of Congress Cataloging in Publication Data McKenzie, W.M.C. (William M.C). Examples in structural analysis/William M.C.McKenzie. p. cm. ISBN 0-415-37053-1 (hardback: alk. paper)ISBN 0-415-37054-X (pbk.: alk. paper) 1. Structural analysis (Engineering) I. Title. TA645.M385 2006 624.1′71–dc22 2006005678

ISBN 0-203-03037-0 Master e-book ISBN

- ISBN10: 0-415-37053-1 (hbk)
- ISBN10: 0-415-37054-X (pbk) ISBN10: 0-203-03037-0 (ebk)


- ISBN13: 978-0-415-37053-0 (hbk)
- ISBN13: 978-0-415-37054-7 (pbk) ISBN13: 978-0-203-03037-0 (ebk)


## Contents

Preface vi Acknowledgements viii

- 1. Structural Analysis and Design 1
- 2. Material and Section Properties 28
- 3. Pin-Jointed Frames 76
- 4. Beams 178
- 5. Rigid-Jointed Frames 354
- 6. Buckling Instability 481
- 7. Direct Stiffness Method 534
- 8. Plastic Analysis 619


###### Appendices

- Appendix 1 Elastic Section Properties of Geometric Figures 764
- Appendix 2 Beam Reactions, Bending Moments and Deflections 769
- Appendix 3 Matrix Algebra 776 Index 781


## Preface

Prior to the development of quantitative structural theories in the mid-18th century and since, builders relied on an intuitive and highly developed sense of structural behaviour. The advent of modern mathematical modelling and numerical methods has to a large extent replaced this skill with a reliance on computer generated solutions to structural problems. Professor Hardy Cross1 aptly expressed his concern regarding this in the following quote:

|‘There is sometimes cause to fear that the scientific technique, the proud servant of the engineering arts, is trying to swallow its master.’<br><br>|
|---|


It is inevitable and unavoidable that designers will utilize continually improving computer software for analyses. However, it is essential that the use of such software should only be undertaken by those with the appropriate knowledge and understanding of the mathematical modelling, assumptions and limitations inherent in the programs they use.

Students adopt a variety of strategies to develop their knowledge and understanding of structural behaviour, e.g. the use of:

|• computers to carry out sensitivity analyses,<br><br>• physical models to demonstrate physical effects such as buckling, bending, the<br><br><br>development of tension and compression and deformation characteristics,<br><br>• the study of worked examples and carrying out analyses using ‘hand’ methods.<br><br>|
|---|


This textbook focuses on the provision of numerous fully detailed and comprehensive worked examples for a wide variety of structural problems. In each chapter a résumé of the concepts and principles involved in the method being considered is given and illustrated by several examples. A selection of problems is then presented which students should undertake on their own prior to studying the given solutions.

Students are strongly encouraged to attempt to visualise/sketch the deflected shape of a loaded structure and predict the type of force in the members prior to carrying out the analysis; i.e.

|(i) in the case of pin-jointed frames identify the location of the tension and<br><br>compression members,<br><br>(ii) in the case of beams/rigid-jointed frames, sketch the shape of the bending moment<br><br><br>diagram and locate points of contra-flexure indicating areas of tension and compression.<br><br>|
|---|


A knowledge of the location of tension zones is vital when placing reinforcement in reinforced concrete design and similarly with compression zones when assessing the effective buckling lengths of steel members.

When developing their understanding and confirming their own answers by studying the solutions provided, students should also analyse the structures using a computer analysis, and identify any differences and the reasons for them.

The methods of analysis adopted in this text represent the most commonly used ‘hand’ techniques with the exception of the direct stiffness method in Chapter 7. This matrix based method is included to develop an understanding of the concepts and procedures adopted in most computer software analysis programs. A method for inverting matrices is given in Appendix 3 and used in the solutions for this chapter—it is not necessary for students to undertake this procedure. It is included to demonstrate the process involved when solving the simultaneous equations as generated in the direct stiffness method.

Whichever analysis method is adopted during design, it must always be controlled by the designer, i.e. not a computer! This can only be the case if a designer has a highly developed knowledge and understanding of the concepts and principles involved in structural behaviour. The use of worked examples is one of a number of strategies adopted by students to achieve this.

|1 Cross, H. Engineers and Ivory Towers. New York: McGraw Hill, 1952|
|---|


W.M.C.McKenzie To the many students who, during the last twenty five years, have made teaching a

very satisfying and rewarding experience.

### Acknowledgements

I wish to thank Caroline, Karen and Gordon for their endless support and encouragement.

### 1. Structural Analysis and Design

#### 1.1 Introduction

The design of structures, of which analysis is an integral part, is frequently undertaken using computer software. This can only be done safely and effectively if those undertaking the design fully understand the concepts, principles and assumptions on which the computer software is based. It is vitally important therefore that design engineers develop this knowledge and understanding by studying and using handmethods of analysis based on the same concepts and principles, e.g. equilibrium, energy theorems, elastic, elasto-plastic and plastic behaviour and mathematical modelling.

In addition to providing a mechanism for developing knowledge and understanding, hand-methods also provide a useful tool for readily obtaining approximate solutions during preliminary design and an independent check on the answers obtained from computer analyses.

The methods explained and illustrated in this text, whilst not exhaustive, include those most widely used in typical design offices, e.g. method-of-sections/joint resolution/unit load/McCaulay’s method/moment distribution/plastic analysis.

In Chapter 7 a résumé is given of the direct stiffness method; the technique used in developing most computer software analysis packages. The examples and problems in this case have been restricted and used to illustrate the processes undertaken when using matrix analysis; this is not regarded as a hand-method of analysis.

#### 1.2 Equilibrium

All structural analyses are based on satisfying one of the fundamental laws of physics, i.e.

|![image 3](McKenzie - Examples in Structural Analysis_images/imageFile3.png)<br><br>Equation<br><br>(1)|
|---|


where

F is the force system acting on a body

m is the mass of the body a is the acceleration of the body

Structural analyses carried out on the basis of a force system inducing a dynamic response, for example structural vibration induced by wind loading, earthquake loading, moving machinery, vehicular traffic etc., have a non-zero value for ‘a’ the acceleration. In the case of analyses carried out on the basis of a static response, for example stresses/deflections induced by the self-weights of materials, imposed loads which do not induce vibration etc., the acceleration ‘a’ is equal to zero.

Static analysis can be regarded as a special case of the more general dynamic analysis in which:

|![image 4](McKenzie - Examples in Structural Analysis_images/imageFile4.png)<br><br>Equation<br><br>(2)|
|---|


F can represent the applied force system in any direction; for convenience this is normally considered in either two or three mutually perpendicular directions as shown in

- Figure 1.1.


![image 5](McKenzie - Examples in Structural Analysis_images/imageFile5.png)

- Figure 1.1 The application of Equation 2 to the force system indicated in Figure 1.1 is:


|Sum of the forces in the direction of the X-axis ΣFx=0 Equation 3<br><br>Sum of the forces in the direction of the Y-axis ΣFy=0 Equation 4<br><br>Sum of the forces in the direction of the Z-axis ΣFz=0 Equation 5<br><br><br>|
|---|


Since the structure is neither moving in a linear direction, nor in a rotational direction a further three equations can be written down to satisfy Equation 2:

|Sum of the moments of the forces about the X-axis ΣMx=0 Equation 6<br><br>Sum of the moments of the forces about the Y-axis SMy=0 Equation 7<br><br>Sum of the moments of the forces about the Z-axis ΣMz=0 Equation 8<br><br><br>|
|---|


Equations 3 to 8 represent the static equilibrium of a body (structure) subject to a three-dimensional force system. Many analyses are carried out for design purposes assuming two-dimensional force systems and hence only two linear equations (e.g. equations 3 and 4 representing the x and y axes) and one rotational equation (e.g. equation 8 representing the z-axis) are required. The x, y and z axes must be mutually perpendicular and can be in any orientation, however for convenience two of the axes are usually regarded as horizontal and vertical, (e.g. gravity loads are vertical and wind loads frequently regarded as horizontal). It is usual practice, when considering equilibrium, to assume that clockwise rotation is positive and anti-clockwise rotation is negative. The following conventions have been adopted in this text:

![image 6](McKenzie - Examples in Structural Analysis_images/imageFile6.png)

###### Figure 1.2

Structures in which all the member forces and external support reactions can be determined using only the equations of equilibrium are ‘statically determinate’ otherwise they are ‘indeterminate structures’. The degree-of-indeterminacy is equal to the number of unknown variables (i.e. member forces/external reactions) which are in excess of the equations of equilibrium available to solve for them, see Section 1.5

The availability of current computer software enables full three-dimensional analyses of structures to be carried out for a wide variety of applied loads. An alternative, more traditional, and frequently used method of analysis when designing is to consider the stability and forces on a structure separately in two mutually perpendicular planes, i.e. a series of plane frames and ensure lateral and rotational stability and equilibrium in each

plane. Consider a typical industrial frame comprising a series of parallel portal frames as shown in Figure 1.3. The frame can be designed considering the X-Y and the Y-Z planes as shown.

![image 7](McKenzie - Examples in Structural Analysis_images/imageFile7.png)

- Figure 1.3


#### 1.3 Mathematical Modelling

The purpose of mathematical modelling is to predict structural behaviour in terms of loads, stresses and deformations under any specified, externally applied force system. Since actual structures are physical, three-dimensional entities it is necessary to create an idealized model which is representative of the materials used, the geometry of the structure and the physical constraints e.g. the support conditions and the externally applied force system.

The precise idealisation adopted in a particular case is dependent on the complexity of the structure and the level of the required accuracy of the final results. The idealization can range from simple 2-dimensional ‘beam-type’ and ‘plate’ elements for pin-jointed or

rigid jointed plane frames and space frames to more sophisticated 3-dimensional elements such as those used in grillages or finite element analyses adopted when analysing for example bridge decks, floor-plates or shell roofs.

It is essential to recognise that irrespective of how advanced the analysis method is, it is always an approximate solution to the real behaviour of a structure.

In some cases the approximation reflects very closely the actual behaviour in terms of both stresses and deformations whilst in others, only one of these parameters may be accurately modelled or indeed the model may be inadequate in both respects resulting in the need for the physical testing of scaled models.

###### 1.3.1 Line Diagrams

When modelling it is necessary to represent the form of an actual structure in terms of idealized structural members, e.g. in the case of plane frames as beam elements, in which the beams, columns, slabs etc. are indicated by line diagrams. The lines normally coincide with the centre-lines of the members. A number of such line diagrams for a variety of typical plane structures is shown in Figures 1.4 to 1.9. In some cases it is sufficient to consider a section of the structure and carry out an approximate analysis on a sub-frame as indicated in Figure 1.8.

![image 8](McKenzie - Examples in Structural Analysis_images/imageFile8.png)

###### Figure 1.4

![image 9](McKenzie - Examples in Structural Analysis_images/imageFile9.png)

###### Figure 1.5

![image 10](McKenzie - Examples in Structural Analysis_images/imageFile10.png)

###### Figure 1.6

![image 11](McKenzie - Examples in Structural Analysis_images/imageFile11.png)

###### Figure 1.7

![image 12](McKenzie - Examples in Structural Analysis_images/imageFile12.png)

###### Figure 1.8

![image 13](McKenzie - Examples in Structural Analysis_images/imageFile13.png)

###### Figure 1.9

1.3.2 Load Path

The support reactions for structures relate to the restraint conditions against linear and rotational movement. Every structural element and structure must be supported in order to transfer the applied loading to the foundations where it is dissipated through the ground. For example beams and floor slabs may be supported by other beams, columns or walls which are supported on foundations which subsequently transfer the loads to the ground. It is important to trace the load path of any applied loading on a structure to ensure that there is no interruption in the flow as shown in Figure 1.10.

![image 14](McKenzie - Examples in Structural Analysis_images/imageFile14.png)

###### Figure 1.10

The loads are transferred between structural members at the joints using either simple or rigid connections (i.e. moment connections). In the case of simple connections axial and/or shear forces are transmitted whilst in the case of rigid connections in addition to axial and shear effects, moments are also transferred.

The type of connections used will influence the degree-of-indeterminacy and the method of analysis required (e.g. determinate, indeterminate, pinjointed frame, rigid-jointed frame). Connection design, reflecting the assumptions made in the analysis, is an essential element in achieving an effective load path.

###### 1.3.3 Foundations

The primary function of all structural members/frames is to transfer the applied dead and imposed loading, from whichever source, to the foundations and subsequently to the ground. The type of foundation required in any particular circumstance is dependent on a number of factors such as the magnitude and type of applied loading, the pressure which the ground can safely support, the acceptable levels of settlement and the location and proximity of adjacent structures.

In addition to purpose made pinned and roller supports the most common types of foundation currently used are indicated Figure 1.11. The support reactions in a structure depend on the types of foundation provided and the resistance to lateral and rotational movement.

![image 15](McKenzie - Examples in Structural Analysis_images/imageFile15.png)

#### 1.4 Structural Loading

All structures are subjected to loading from various sources. The main categories of loading are: dead, imposed and wind loads. In some circumstances there may be other loading types which should be considered, such as settlement, fatigue, temperature effects, dynamic loading, or impact effects (e.g. when designing bridge decks, cranegantry girders or maritime structures). In the majority of cases design considering combinations of dead, imposed and wind loads is the most appropriate.

Most floor systems are capable of lateral distribution of loading. In situations where lateral distribution is not possible, the effects of the concentrated loads should be considered with the load applied at locations which will induce the most adverse effect, e.g. maximum bending moment, shear and deflection. In addition, local effects such as crushing and punching should be considered where appropriate.

In multi-storey structures it is very unlikely that all floors will be required to carry the full imposed load at the same time. Statistically it is acceptable to reduce the total floor loads carried by a supporting member by varying amounts depending on the number of floors or floor area carried. Dynamic loading is often represented by a system of equivalent static forces which can be used in the analysis and design of a structure.

The primary objective of structural analysis is to determine the distribution of internal moments and forces throughout a structure such that they are in equilibrium with the applied design loads.

Mathematical models which can be used to idealise structural behaviour include: twoand three-dimensional elastic behaviour, elastic behaviour considering a redistribution of moments, plastic behaviour and non-linear behaviour. The following chapters illustrate most of the hand-based techniques commonly used to predict structural member forces and behaviour.

In braced structures (i.e. those in which structural elements have been provided specifically to transfer lateral loading) where floor slabs and beams are considered to be simply supported, vertical loads give rise to different types of beam loading. Floor slabs can be designed as either one-way spanning or two-way spanning as shown in Figures 1.12(a) and (b).

![image 16](McKenzie - Examples in Structural Analysis_images/imageFile16.png)

###### Figure 1.12

In the case of one-way spanning slabs the entire load is distributed to the two main beams. Two-way spanning slabs distribute load to main beams along all edges. These

###### differences give rise to a number of typical beam loadings in floor slabs as shown in Figures 1.13.

![image 17](McKenzie - Examples in Structural Analysis_images/imageFile17.png)

#### 1.5 Statical Indeterminacy

Any plane-frame structure which is in a state of equilibrium under the action of an externally applied force system must satisfy the following three conditions:

|• the sum of the horizontal components of all applied forces must equal zero,<br><br>• the sum of the vertical components of all applied forces must equal zero,<br><br>• the sum of the moments (about any point in the plane of the frame) of all applied<br><br><br>forces must equal zero.<br><br>|
|---|


This is represented by the following ‘three equations of static equilibrium’

|Sum of the horizontal forces equals zero +ve<br><br>ΣFx=0<br><br>![image 18](McKenzie - Examples in Structural Analysis_images/imageFile18.png)<br><br>Sum of the vertical forces equals zero +ve<br><br>ΣFy=0<br><br><br>![image 19](McKenzie - Examples in Structural Analysis_images/imageFile19.png)<br><br>Sum of the moments about a point in the plane of the forces equals zero<br><br>+ve ΣM=0<br><br>![image 20](McKenzie - Examples in Structural Analysis_images/imageFile20.png)<br><br>|
|---|


In statically determinate structures, all internal member forces and external reactant forces can be evaluated using the three equations of static equilibrium. When there are more unknown member forces and external reactant forces than there are available equations of equilibrium a structure is statically indeterminate and it is necessary to consider the compatibility of structural deformations to fully analyse the structure.

A structure may be indeterminate due to redundant components of reaction and/or redundant members. i.e. a redundant reaction or member is one which is not essential to satisfy the minimum requirements of stability and static equilibrium, (Note: it is not necessarily a member with zero force).

The degree-of-indeterminacy (referred to as ID in this text) is equal to the number of unknown variables (i.e. member forces/external reactions) which are in excess of the equations of equilibrium available to solve for them.

1.5.1 Indeterminacy of Two-Dimensional Pin-Jointed Frames

The external components of reaction (r) in pin-jointed frames are normally one of two types:

|i) a roller support providing one degree-of-restraint, i.e. perpendicular to the roller,<br><br>ii) a pinned support providing two degrees-of-restraint, e.g. in the horizontal and<br><br><br>vertical directions.<br><br>|
|---|


as shown in Figure 1.14

![image 21](McKenzie - Examples in Structural Analysis_images/imageFile21.png)

- Figure 1.14

It is necessary to provide three non-parallel, non-concentric, components of reaction to satisfy the three equations of static equilibrium. Consider the frames indicated in Figures 1.15 and 1.16

![image 22](McKenzie - Examples in Structural Analysis_images/imageFile22.png)

- Figure 1.15


![image 23](McKenzie - Examples in Structural Analysis_images/imageFile23.png)

Figures 1.16

In Figures 1.15 and 1.16 the applied forces and the external components of reaction represent co-planar force systems which are in static equilibrium. In Figure 1.15 there are three unknowns, (HA, VA and VC), and three equations of equilibrium which can be used to determine their values: there are no redundant components of reaction.

In Figure 1.16 there are five unknowns components of reaction, (HA, VA, VF, HE and VE), and only three equations of equilibrium; there are two redundant reactions in this case.

The internal members of pin-jointed frames transfer either tensile or compressive axial loads through the nodes to the supports and hence reactions. A simple pin-jointed frame is one in which the minimum number of members is present to ensure stability and static equilibrium.

Consider the basic three member pinned-frame indicated in Figure 1.15. There are three nodes and three members. A triangle is the basis for the development of all pinjointed frames since it is an inherently stable system, i.e. only one configuration is possible for any given three lengths of the members.

Consider the development of the frame shown in Figure 1.17:

![image 24](McKenzie - Examples in Structural Analysis_images/imageFile24.png)

###### Figure 1.17

Initially there are three nodes and three members. If the number of members in the frame is to be increased then for each node added, two members are required to maintain the triangulation. The minimum number of members required to create a simple frame can be determined as follows:

|![image 25](McKenzie - Examples in Structural Analysis_images/imageFile25.png)|
|---|


Any members which are added to the frame in addition to this number are redundant members and make the frame statically indeterminate; e.g.

![image 26](McKenzie - Examples in Structural Analysis_images/imageFile26.png)

###### Figure 1.18

It is also essential to consider the configuration of the members in a frame to ensure that it is triangulated. The simple frames indicated in Figure 1.19 are unstable.

![image 27](McKenzie - Examples in Structural Analysis_images/imageFile27.png)

###### Figure 1.19

As indicated previously, the minimum number of reactant forces to maintain static equilibrium is three and consequently when considering a simple, pin-jointed plane-frame and its support reactions the combined total of members and components of reaction is equal to:

|Σ (number of members+support reactions)=(m+r)=(2n−3)+3=2n|
|---|


Consider the frames shown in Figure 1.20 with pinned and roller supports as indicated.

![image 28](McKenzie - Examples in Structural Analysis_images/imageFile28.png)

###### Figure 1.20

The degree of indeterminacy ID=(m+r)−2n Compound trusses which are fabricated from two or more simple trusses by a structural system involving no more than three, non-parallel, non-concurrent, unknown forces can also be stable and determinate. Consider the truss shown in Figure 1.21(a) which is a simple truss and satisfies the relationships m=(2n−3) and ID=0.

![image 29](McKenzie - Examples in Structural Analysis_images/imageFile29.png)

- Figure 1.21 This truss can be connected to a similar one by a pin and an additional member as

- shown in Figure 1.21(b) to create a compound truss comprising two statically determinate trusses. Since only an additional three unknown forces have been generated the three equations of equilibrium can be used to solve these by considering a section A–A as shown (see Chapter 3—Section 3.2.—Method of Sections for Pin-Jointed Frames: Problem 3.4).


1.5.2 Indeterminacy of Two-Dimensional Rigid-Jointed Frames

The external components of reaction (r) in rigid-jointed frames are normally one of three types:

|i) a roller support providing one degree-of-restraint, i.e. perpendicular to the roller,<br><br>ii) a pinned support providing two degrees-of-restraint, e.g. in the horizontal and<br><br>vertical directions,<br><br>iii) a fixed (encastre) support providing three degrees-of-restraint, i.e. in the horizontal<br><br><br>and vertical directions and a moment restraint,<br><br>|
|---|


- as shown in Figure 1.22


![image 30](McKenzie - Examples in Structural Analysis_images/imageFile30.png)

- Figure 1.22


In rigid-jointed frames, the applied load system is transferred to the supports by inducing axial loads, shear forces and bending moments in the members. Since three

components of reaction are required for static equilibrium the total number of unknowns is equal to: [(3×m)+r]. At each node there are three equations of equilibrium, i.e.

|Σ the vertical forces Fy=0; Σ the horizontal forces<br><br>Fx=0;<br><br>Σ the moments M=0, providing (3×n) equations.<br><br>The degree of indeterminacy ID=[(3m)+r]−3n<br><br>|
|---|


Consider the frames shown in Figure 1.23

![image 31](McKenzie - Examples in Structural Analysis_images/imageFile31.png)

###### Figure 1.23

The existence of an internal pin in a member in a rigid-frame results in only shear and axial loads being transferred through the frame at its location. This reduces the number of unknowns and hence redundancies, since an additional equation is available for solution, i.e. Sum of the moments about the pin equals zero, i.e. Σ Mpin=0

Consider the effect of introducing pins in the frames shown in Figure 1.24

![image 32](McKenzie - Examples in Structural Analysis_images/imageFile32.png)

###### Figure 1.24

The existence of an internal pin at a node with two members in a rigid-frame results in the release of the moment capacity and hence one additional equation as shown in Figure 1.25(a). When there are three members meeting at the node then there are effectively two values of moment, i.e. M1 and M2 and in the third member M3=(M1+M2) The introduction of a pin in one of the members produces a single release and in two members (effectively all three members) produces two releases as shown in Figure 1.25(b).

In general terms the introduction of ‘p’ pins at a joint introduces ‘p’ additional equations. When pins are introduced to all members at the joint the number of additional equations produced equals (number of members at the joint—1).

![image 33](McKenzie - Examples in Structural Analysis_images/imageFile33.png)

###### Figure 1.25

Consider the frame shown in Figure 1.26.

![image 34](McKenzie - Examples in Structural Analysis_images/imageFile34.png)

###### Figure 1.26

The inclusion of an internal roller within a member results in the release of the moment capacity and in addition the force parallel to the roller and hence provides two additional equations. Consider the continuous beam ABC shown in Figure 1.27. in which a roller has been inserted in member AB

![image 35](McKenzie - Examples in Structural Analysis_images/imageFile35.png)

###### Figure 1.27

ID={[(3m)+r]−3n}−2 due to the release of the moment and axial load capacity at the roller ∴ ID={[(3×2)+6]−(3×3)−2=1

Consider the same beam AB with a pin added in addition to the roller.

![image 36](McKenzie - Examples in Structural Analysis_images/imageFile36.png)

###### Figure 1.28

ID={[(3m)+r]−3n}−3 due to the release of the moment capacity at the position of the

pin and the release of the moment and axial load capacity at the roller ID={[(3×2)+6]−(3×3)−3=0 The structure is statically determinate. A similar approach can be taken for three-dimensional structures; this is not

considered in this text.

#### 1.6 Structural Degrees-of-Freedom

The degrees-of-freedom in a structure can be regarded as the possible components of displacements of the nodes including those at which some support conditions are provided. In pin-jointed, plane-frames each node, unless restrained, can displace a small amount δ which can be resolved in to horizontal and vertical components δH and δV as

- shown in Figure 1.29.


![image 37](McKenzie - Examples in Structural Analysis_images/imageFile37.png)

###### Figure 1.29

Each component of displacement can be regarded as a separate degree-of-freedom and in this frame there is a total of three degrees-of-freedom:

The vertical and horizontal displacement of node B and the horizontal displacement of node C as indicated.

In a pin-jointed frame there are effectively two possible components of displacement for each node which does not constitute a support. At each roller support there is an additional degree-of-freedom due to the release of one restraint. In a simple, i.e. statically determinate frame, the number of degrees-of-freedom is equal to the number of members. Consider the two frames indicated in Figures 1.20(a) and (b):

|In Figure 1.20(a):<br><br>the number of members m=3<br><br>possible components of displacements at node B =2 possible components of displacements at node support C<br><br>=1<br><br>Total number of degrees-of-freedom (=m)=3<br><br>|
|---|


In Figure

- 1.20(b):


the number of members m=11

possible components of displacements at nodes =10 possible components of displacements at support E

=1

###### Total number of degrees-of-freedom (=m)=11

In the case of indeterminate frames, the number of degrees-of-freedom is equal to the (number of members—ID); consider the two frames indicated in Figures 1.20(c) and (d):

|In Figure 1.20(c):<br><br>the number of members m=14<br><br>possible components of displacements at nodes<br><br>=12<br><br>possible components of displacements at support G<br><br>=1<br><br>degree-of-indeterminacy ID=1 Total number of degrees-of-freedom (m−ID)=13<br><br>|
|---|


In Figure

- 1.20(d):


the number of members m=15

possible components of displacements at nodes

=10

degree-of-indeterminacy ID=5 Total number of degrees-of-freedom (m−ID)=10

In rigid-jointed frames there are effectively three possible components of displacement for each node which does not constitute a support; they are rotation and two components of translation e.g. θ, δH and δV. At each pinned support there is an additional degree-offreedom due to the release of the rotational restraint and in the case of a roller, two additional degrees-of-freedom due to the release of the rotational restraint and a translational restraint. Consider the frames shown in Figure 1.23.

|In Figure 1.23(a): the number of nodes (excluding supports) =2 possible components of displacements at nodes =6 possible components of displacements at support D =1 Total number of degrees-of-freedom =7<br><br>|
|---|


In Figure

- 1.23(b):


the number of nodes (excluding supports) =4

possible components of displacements at nodes =12 possible components of displacements at support G

=1

possible components of displacements at support F =1 Total number of degrees-of-freedom =14

|In Figure 1.23(c): the number of nodes (excluding supports) =3 possible components of displacements at nodes =9 possible components of displacements at support A =1 Total number of degrees-of-freedom =10<br><br>|
|---|


###### In Figure 1.23(d): the number of nodes (excluding supports) =1 possible components of displacements at nodes =3 possible components of displacements at support C =2 possible components of displacements at support D =1 Total number of degrees-of-freedom =6

The introduction of a pin in a member at a node produces an additional degree-offreedom. Consider the typical node with four members as shown in Figure 1.30. In (a) the node is a rigid connection with no pins in any of the members and has the three degreesof-freedom indicated. In (b) a pin is present in one member, this produces an additional degrees-of-freedom since the rotation of this member can be different from the remaining three, similarly with the other members as shown in (c) and (d).

![image 38](McKenzie - Examples in Structural Analysis_images/imageFile38.png)

- Figure 1.30 Degrees-of-freedom:


![image 39](McKenzie - Examples in Structural Analysis_images/imageFile39.png)

In many cases the effects due to axial deformations is significantly smaller than those due to the bending effect and consequently an analysis assuming axial rigidity of members is acceptable. Assuming axial rigidity reduces the degrees-of-freedom which are considered; consider the frame shown in Figure 1.31.

![image 40](McKenzie - Examples in Structural Analysis_images/imageFile40.png)

- Figure 1.31


###### 1.6.1 Problems: Indeterminacy and Degrees-of-Freedom

Determine the degree of indeterminacy and the number of degrees-of-freedom for the pin-jointed and rigid-jointed frames indicated in Problems 1.1 to 1.3. and 1.4 to 1.6 respectively.

- Problem 1.1


![image 41](McKenzie - Examples in Structural Analysis_images/imageFile41.png)

![image 42](McKenzie - Examples in Structural Analysis_images/imageFile42.png)

###### Problem 1.2

###### Problem 1.3

![image 43](McKenzie - Examples in Structural Analysis_images/imageFile43.png)

![image 44](McKenzie - Examples in Structural Analysis_images/imageFile44.png)

###### Problem 1.4

###### Problem 1.5

![image 45](McKenzie - Examples in Structural Analysis_images/imageFile45.png)

![image 46](McKenzie - Examples in Structural Analysis_images/imageFile46.png)

###### Problem 1.6

###### 1.6.2 Solutions: Indeterminacy and Degrees-of-freedom

![image 47](McKenzie - Examples in Structural Analysis_images/imageFile47.png)

### 2. Material and Section Properties

#### 2.1 Introduction

Structural behaviour is dependent upon material characteristics such as elastic constants which describe the stress/strain relationships and the geometry of the crosssection of individual members. This section describes the principal characteristics and properties which must be considered and evaluated to enable mathematical modelling to be undertaken.

2.1.1 Simple Stress and Strain

The application of loads to structural members induce deformations and internal resisting forces within the materials. The intensity of these forces is known as the stress in the material and is measured as the force per unit area of the cross-sections which is normally given the symbol σ when it acts perpendicular to the surface of a cross-section and τ when it acts parallel to the surface. Different types of force cause different types and distributions of stress for example: axial stress, bending stress, shear stress, torsional stress and combined stress.

Consider the case of simple stress due to an axial load P which is supported by a column of cross-sectional area A and original length L as shown in Figure 2.1. The applied force induces an internal stress σ such that:

![image 48](McKenzie - Examples in Structural Analysis_images/imageFile48.png)

###### Figure 2.1

The deformation induced by the stress is quantified by relating the change in length to the original length and is known as the strain in the material normally given the symbol ε where:

|δ=(change in length/original length)=(δ/L)|
|---|


Note: the strain is dimensionless since the units of δ and L are the same.

The relationship between stress and strain was first established by Robert Hook in 1676 who determined that in an elastic material the strain is proportional to the stress. The general form of a stress/strain graph is as

- shown in Figure 2.2.


![image 49](McKenzie - Examples in Structural Analysis_images/imageFile49.png)

- Figure 2.2


The point at which this graph ceases to obey Hook’s Law and becomes non-linear is the ‘elastic limit’ or ‘proportional limit’.

A typical stress-strain curve for concrete is shown in Figure 2.3(a). This is a non-linear curve in which the peak stress is developed at a compressive strain of approximately 0.002 (depending upon the strength of the concrete) with an ultimate strain of approximately 0.0035. There is no clearly defined elastic range over which the stress varies linearly with the strain. Such stress/strain curves are typical of brittle materials.

A typical stress-strain curve for hot-rolled mild steel is shown in Figure 2.3(b). When a test specimen of mild steel reinforcing bar is subjected to an axial tension in a testing machine, the stress/strain relationship is linearly elastic until the value of stress reaches a yield value, e.g. 250 N/mm2.

At this point an appreciable increase in the stretching of the sample occurs at constant load: this is known as yielding. During the process of yielding a molecular change takes place in the material which has the effect of hardening the steel. After approximately 5% strain has occurred sufficient strain-hardening will have developed to enable the steel to carry a further increase in load until a maximum load is reached.

The stress-strain curve falls after this point due to a local reduction in the diameter of the sample (known as necking) with a consequent smaller cross-sectional area and load carrying capacity. Eventually the sample fractures at approximately 35% strain.

![image 50](McKenzie - Examples in Structural Analysis_images/imageFile50.png)

###### Figure 2.3

The characteristics of the stress/strain curves are fundamental to the development and use of structural analysis techniques. A number of frequently used material properties relating to these characteristics are defined in Sections 2.1.2 to 2.1.6.

###### 2.1.2 Young’s Modulus (Modulus of Elasticity)—E

From Hooke’s Law (in the elastic region): stress strain ∴ stress=(constant×strain). The value of the constant is known as ‘Young’s Modulus’ and usually given the symbol ‘E’. Since strain is dimensionless, the units of E are the same as those for stress. It represents a measure of material resistance to axial deformation. For some materials the value of Young’s Modulus is different in tension than it is in compression. The numerical value of E is equal to the slope of the stress/strain curve in the elastic region, i.e. tanθ in

![image 51](McKenzie - Examples in Structural Analysis_images/imageFile51.png)

- Figure 2.2.


###### 2.1.3 Secant Modulus—Es

The ‘secant modulus’ is equal to the slope of a line drawn from the origin of the stressstrain graph to a point of interest beyond the elastic limit as shown in Figure 2.4.

![image 52](McKenzie - Examples in Structural Analysis_images/imageFile52.png)

###### Figure 2.4

The secant modulus is used to describe the material resistance to deformation in the inelastic region of a stress/strain curve and is often expressed as a percentage of Young’s Modulus, e.g. 75%–0.75E.

2.1.4 Tangent Modulus—Et

The ‘tangent modulus’ is equal to the slope of a tangent line to the stress-strain graph

- at a point of interest beyond the elastic limit as shown in Figure 2.5.


![image 53](McKenzie - Examples in Structural Analysis_images/imageFile53.png)

###### Figure 2.5

The tangent modulus can be used in inelastic buckling analysis of columns as shown in Section 6.3.6 of Chapter 6.

###### 2.1.5 Shear Rigidity (Modulus of Rigidity)—G

The shear rigidity is used to describe the material resistance against shear deformation. similar to Young’s Modulus for axial or normal stress/strain. The numerical value of G is equal to the slope of the shear stress/strain curve in the elastic region, where the shear strain is the change angle induced between two perpendicular surfaces subject to a shear stress.

###### 2.1.6 Yield Strength

The yield strength corresponds with the point on the stress/strain graph where permanent deformation begins in the material. In some cases, e.g. in Figure 2.3(a) there is no distinct yield point whilst in others, such as in Figure 2.3(b) there is a well-defined yield region. In the former case a percentage offset is often used to obtain an approximate yield point, e.g. a 0.2% offset point can be determined by drawing a line parallel to the elastic linear line of the graph starting at a point 0.2% (0.002) along the strain axes as

- shown in Figure 2.6. The intersection of this line with the stress-strain curve defines the 0.2% yield point.


![image 54](McKenzie - Examples in Structural Analysis_images/imageFile54.png)

- Figure 2.6


###### 2.1.7 Ultimate Tensile Strength

The ‘ultimate strength’ is the maximum stress which a material is capable of sustaining and corresponds to the highest point on the stress/strain curve; see Figure

- 2.3(b). In engineering terms this is normally the value adopted, however if a specimen undergoes considerable necking prior to fracture the true value will differ from this.


###### 2.1.8 Modulus of Rupture in Bending

The ‘modulus of rupture’ represents the ultimate strength in bending obtained during a bending test. It is determined by calculating the maximum bending stress in the extreme fibres in a member at failure.

###### 2.1.9 Modulus of Rupture in Torsion

The ‘modulus of rupture’ represents the ultimate strength in torsion obtained during torsion test. It is determined by calculating the maximum shear stress in the extreme fibres of a circular member at failure.

###### 2.1.10 Poisson’s Ratio—υ

The ‘Poisson’s Ratio’ for a material is a dimensionless constant representing the ratio of the lateral strain to the axial strain as shown in Figure 2.7.

![image 55](McKenzie - Examples in Structural Analysis_images/imageFile55.png)

- Figure 2.7


###### 2.1.11 Coefficient of Thermal Expansion—a

The linear coefficient of thermal expansion describes by how much a material will expand for each degree of temperature increase/decrease, e.g. the change in the length of a bar made from a particular material is given by:

δL=αLΔT where a is the coefficient of thermal expansion for the material, L is the original length, ∆T is the change in temperature—a reduction being considered negative and an

increase being positive. The unit for coefficient of thermal expansion is typically °C−1.

###### 2.1.12 Elastic Assumptions

The laws of structural mechanics are well established in recognised elastic theory using the following assumptions:

|• the material is homogeneous which implies its constituent parts have the same physical properties throughout its entire volume.<br><br>• the material is isotropic which implies that the elastic properties are the same in all directions.<br><br>• the material obeys Hooke’s Law, i.e. when subjected to an external force system the deformations induced will be directly proportional to the magnitude of the applied force. (P δ)<br><br>![image 56](McKenzie - Examples in Structural Analysis_images/imageFile56.png)<br><br>• the material is elastic, which implies that it will recover completely from any deformation after the removal of load.<br><br>• the modulus of elasticity is the same in tension and compression.<br><br><br>|
|---|


|• plane sections remain plane during deformation. During bending this assumption is violated and is reflected in a non-linear bending stress diagram throughout cross-sections subject to a moment; in most cases this can be neglected.<br><br>|
|---|


#### 2.2 Elastic Cross-Section Properties

An evaluation of the elastic section properties of a cross-section is fundamental to all structural analyses. These encompass a wide range of parameters such as; cross-sectional area, position of the centroid and the elastic neutral axes, the second moment of area about the centroidal axes and any parallel axes and the elastic section modulus, (Note: not the Elastic Modulus of Elasticity which is discussed in Section 2.1). Each of these is discussed separately in Sections 2.2.1 to 2.2.8.

Most structural elements have a cross-section for which standard properties are known, e.g. square, rectangle, triangle, trapezium, circle etc., or comprise a combination of one or more such shapes. If the properties of each shape which makes up a complete cross-section are known, this information can be used to determine the corresponding properties of the composite shape. A number of examples are given to illustrate this in the following sections.

In structural steelwork a variety of hot-rolled standard sections are available, the crosssectional properties of which are given in published tables. A selection of the most common ones are shown in Figure 2.8.

![image 57](McKenzie - Examples in Structural Analysis_images/imageFile57.png)

###### Figure 2.8

###### 2.2.1 Cross-sectional Area

The cross-sectional area of a composite shape can be expressed as:

|![image 58](McKenzie - Examples in Structural Analysis_images/imageFile58.png)|
|---|


where:

|Atotal is the total area of the composite cross-section Ai is the cross-sectional area of each component part<br><br>|
|---|


Consider the composite shapes indicated in (i) to (ix) and determine the value of Atotal

![image 59](McKenzie - Examples in Structural Analysis_images/imageFile59.png)

###### Figure 2.9

|![image 60](McKenzie - Examples in Structural Analysis_images/imageFile60.png)|
|---|


![image 61](McKenzie - Examples in Structural Analysis_images/imageFile61.png)

###### Figure 2.10

|![image 62](McKenzie - Examples in Structural Analysis_images/imageFile62.png)|
|---|


![image 63](McKenzie - Examples in Structural Analysis_images/imageFile63.png)

###### Figure 2.11

|![image 64](McKenzie - Examples in Structural Analysis_images/imageFile64.png)|
|---|


![image 65](McKenzie - Examples in Structural Analysis_images/imageFile65.png)

###### Figure 2.12

|![image 66](McKenzie - Examples in Structural Analysis_images/imageFile66.png)|
|---|


![image 67](McKenzie - Examples in Structural Analysis_images/imageFile67.png)

###### Figure 2.13

|![image 68](McKenzie - Examples in Structural Analysis_images/imageFile68.png)|
|---|


![image 69](McKenzie - Examples in Structural Analysis_images/imageFile69.png)

###### Figure 2.14

|![image 70](McKenzie - Examples in Structural Analysis_images/imageFile70.png)|
|---|


![image 71](McKenzie - Examples in Structural Analysis_images/imageFile71.png)

###### Figure 2.15

|![image 72](McKenzie - Examples in Structural Analysis_images/imageFile72.png)|
|---|


Check the area of the trapezium in (vi): Atotal=[0.5×(70+150)×(50)]=5500 mm2 In a similar manner to adding the individual areas of component parts to obtain the

total area, section properties can be evaluated by subtracting areas which do not exist, e.g. in hollow sections. Consider examples (vii) to (ix).

![image 73](McKenzie - Examples in Structural Analysis_images/imageFile73.png)

###### Figure 2.16

|![image 74](McKenzie - Examples in Structural Analysis_images/imageFile74.png)|
|---|


![image 75](McKenzie - Examples in Structural Analysis_images/imageFile75.png)

###### Figure 2.17

|![image 76](McKenzie - Examples in Structural Analysis_images/imageFile76.png)|
|---|


![image 77](McKenzie - Examples in Structural Analysis_images/imageFile77.png)

###### Figure 2.18

|![image 78](McKenzie - Examples in Structural Analysis_images/imageFile78.png)|
|---|


2.2.2 Centre of Gravity and Centroid

The centre of gravity of an object is the point through which the force due to gravity on the total mass of the object is considered to act. The corresponding position on a plane surface (i.e. relating to the cross-sectional area) is known as the centroid; both are

- indicated in Figure 2.19


![image 79](McKenzie - Examples in Structural Analysis_images/imageFile79.png)

###### Figure 2.19

Consider the cross-section A shown in Figures 2.20(a) and (b) which can be considered to be an infinite number of elemental areas each equal to δA. The 1st moment

of area (i.e. area×perpendicular lever arm) of the total area about any axis is equal to the sum of the 1st moments of area of each individual area about the same axis, i.e.

|![image 80](McKenzie - Examples in Structural Analysis_images/imageFile80.png)|
|---|


where:

|A is the total area of the cross section<br><br>![image 81](McKenzie - Examples in Structural Analysis_images/imageFile81.png)<br><br>is the distance in the x direction to the centroid for the total area<br><br>![image 82](McKenzie - Examples in Structural Analysis_images/imageFile82.png)<br><br>is the distance in the y direction to the centroid for the total area<br><br><br>x is the distance in the x direction to the centroid of the elemental area<br><br>y is the distance in the y direction to the centroid of the elemental area<br><br><br>|
|---|


![image 83](McKenzie - Examples in Structural Analysis_images/imageFile83.png)

###### Figure 2.20

In precise terms, ΣδAx/A and ΣδAy/A are the integrals for the shape being considered, however in most practical cases the cross-sectional area comprises a number of standard shapes (instead of the elemental area) i.e. rectangles, triangles, circles etc. in which the position of the centroid is known as shown in Figure 2.21

![image 84](McKenzie - Examples in Structural Analysis_images/imageFile84.png)

###### Figure 2.21

Consider the composite shapes (i) to (ix) indicated previously to determine the co-ordinates of their centroids.

![image 85](McKenzie - Examples in Structural Analysis_images/imageFile85.png)

###### Figure 2.22

![image 86](McKenzie - Examples in Structural Analysis_images/imageFile86.png)

###### Figure 2.23

![image 87](McKenzie - Examples in Structural Analysis_images/imageFile87.png)

###### Figure 2.24

Note: If there are axes of symmetry then the centroid lies at the intersection point of the axes.

![image 88](McKenzie - Examples in Structural Analysis_images/imageFile88.png)

###### Figure 2.25

![image 89](McKenzie - Examples in Structural Analysis_images/imageFile89.png)

###### Figure 2.26

![image 90](McKenzie - Examples in Structural Analysis_images/imageFile90.png)

###### Figure 2.27

![image 91](McKenzie - Examples in Structural Analysis_images/imageFile91.png)

###### Figure 2.28

![image 92](McKenzie - Examples in Structural Analysis_images/imageFile92.png)

###### Figure 2.29

![image 93](McKenzie - Examples in Structural Analysis_images/imageFile93.png)

###### Figure 2.30

|![image 94](McKenzie - Examples in Structural Analysis_images/imageFile94.png)|
|---|


###### 2.2.3 Problems: Cross-sectional Area and Position of Centroid

![image 95](McKenzie - Examples in Structural Analysis_images/imageFile95.png)

![image 96](McKenzie - Examples in Structural Analysis_images/imageFile96.png)

Determine the cross-sectional area and the values of and to locate the position of the centroid for the sections shown in Problems 2.1 to 2.6. Assume the origin of the coordinate system to be at the bottom left-hand corner for each section.

###### Problem 2.1

###### Problem 2.2

![image 97](McKenzie - Examples in Structural Analysis_images/imageFile97.png)

![image 98](McKenzie - Examples in Structural Analysis_images/imageFile98.png)

###### Problem 2.3

###### Problem 2.4

![image 99](McKenzie - Examples in Structural Analysis_images/imageFile99.png)

![image 100](McKenzie - Examples in Structural Analysis_images/imageFile100.png)

![image 101](McKenzie - Examples in Structural Analysis_images/imageFile101.png)

###### Problem 2.5

![image 102](McKenzie - Examples in Structural Analysis_images/imageFile102.png)

###### Problem 2.6

2.2.4 Solutions: Cross-sectional Area and Position of Centroid

![image 103](McKenzie - Examples in Structural Analysis_images/imageFile103.png)

2.2.5 Elastic Neutral Axes

Consider a beam of rectangular cross-section which is simply supported at the ends and carries a distributed load, as shown in Figure 2.31.

![image 104](McKenzie - Examples in Structural Analysis_images/imageFile104.png)

- Figure 2.31

The beam will deflect due to the bending moments and shear forces induced by the applied loading, resulting in a curved shape as indicated in Figure 2.32.

![image 105](McKenzie - Examples in Structural Analysis_images/imageFile105.png)

- Figure 2.32

Clearly if the ends of the beam are assumed to remain perpendicular to the longitudinal axis, then the material above this axis must be in compression, whilst that below it must be in tension. At a point between the top and the bottom of the beam a layer of fibres exist which remain at their original length and consequently do not have any bending stress in them. This layer of fibres forms the ‘neutral surface’ and on a crosssection is indicated by the ‘neutral axis’ as shown in Figure 2.33.

![image 106](McKenzie - Examples in Structural Analysis_images/imageFile106.png)

- Figure 2.33


###### 2.2.6 Second Moment of Area—I and Radius of Gyration—r

Two of the most important properties of a cross-section are the ‘second moment of area’ and the ‘radius of gyration’. Consider the area shown in Figure 2.20(b). If the elemental area δA has its centroid at a perpendicular distance ‘r’ from a given axis, the

second moment of area of the element about the given axis is the product of the area of the element and the square of the distance of the centroid from the axis, i.e.

|![image 107](McKenzie - Examples in Structural Analysis_images/imageFile107.png)|
|---|


The second moment of area of the total area A is equal to Σ(δAr2) over the whole area. It is convenient to consider two mutually perpendicular axes which intersect at the centroid of a cross-section and hence:

|![image 108](McKenzie - Examples in Structural Analysis_images/imageFile108.png)|
|---|


Alternatively:

|![image 109](McKenzie - Examples in Structural Analysis_images/imageFile109.png)|
|---|


where rxx and ryy are known as the ‘radii of gyration’ about the x-x and y-y axes respectively.

Consider the rectangular cross-section shown in Figure 2.34.

![image 110](McKenzie - Examples in Structural Analysis_images/imageFile110.png)

###### Figure 2.34

|![image 111](McKenzie - Examples in Structural Analysis_images/imageFile111.png)|
|---|


2.2.6.1 The Parallel Axis Theorem

It can also be shown that the second moment of area of a cross-sectional area A about an axis parallel to any other axis is equal to the second moment of area of A about that other axis plus the area multiplied by the square of the perpendicular distance between the axes. Consider the rectangular areas shown in Figure 2.35:

![image 112](McKenzie - Examples in Structural Analysis_images/imageFile112.png)

- Figure 2.35

These relationships are used extensively to determine the values of the second moment of area and radius of gyration of compound sections comprising defined areas such as rectangles, triangles circles etc.

Consider the cross-sectional area shown in Figures 2.24 and determine the values of the second moment of area and radius of gyration about the centroidal axes. Data from

- Figure 2.24 is indicated in Figure 2.36:


![image 113](McKenzie - Examples in Structural Analysis_images/imageFile113.png)

- Figure 2.36


IQQ=(Iyy+Ax2) for each rectangle in which QQ is the y-y axis for the whole section. In this case the second term for each rectangle is equal to zero since the y-y axis coincides with their centroidal axes.

|![image 114](McKenzie - Examples in Structural Analysis_images/imageFile114.png)|
|---|


###### 2.2.7 Elastic Section Modulus—Z

The bending moments induced in a beam by an applied load system generate bending stresses in the material fibres which vary from a maximum in the extreme fibres to zero at the level of the neutral axis as shown in Figures 2.33 and 2.37.

The magnitude of the bending stresses at any vertical cross-section can be determined using the simple theory of bending from which the following equation is derived:

|![image 115](McKenzie - Examples in Structural Analysis_images/imageFile115.png)|
|---|


![image 116](McKenzie - Examples in Structural Analysis_images/imageFile116.png)

###### Figure 2.37where:

M the applied bending moment at the section being considered, E the value of Young’s modulus of elasticity, R the radius of curvature of the beam,

σ the bending stress, y the distance measured from the elastic neutral axis to the level on the cross-

section at which the stress is being evaluated, I the second moment of area of the full cross-section about the elastic neutral axis.

It is evident from the equation given above that for any specified cross-section in a beam subject to a known value of bending moment (i.e. M and I constant), the bending stress is directly proportional to the distance from the neutral axis; i.e.

|![image 117](McKenzie - Examples in Structural Analysis_images/imageFile117.png)|
|---|


This is shown in Figure 2.37, in which the maximum bending stress occurs at the extreme fibres.

In design it is usually the extreme fibre stresses relating to the ymaximum values at the top and bottom which are critical. These can be determined using:

|![image 118](McKenzie - Examples in Structural Analysis_images/imageFile118.png)|
|---|


where σ and M are as before,

Ztop is the elastic section modulus relating to the top fibres and defined as

![image 119](McKenzie - Examples in Structural Analysis_images/imageFile119.png)

Zbottom is the elastic section modulus relating to the bottom fibres and defined as

![image 120](McKenzie - Examples in Structural Analysis_images/imageFile120.png)

If a cross-section is symmetrical about the x-x axis then Ztop=Zbottom. In asymmetric sections the maximum stress occurs in the fibres corresponding to the smallest Z value. For a rectangular cross-section of breadth B and depth D subject to a bending moment M about the major x-x axis, the appropriate values of I, y and Z are:

![image 121](McKenzie - Examples in Structural Analysis_images/imageFile121.png)

In the case of bending about the minor y-y axis:

![image 122](McKenzie - Examples in Structural Analysis_images/imageFile122.png)

Consider the cross-sectional area shown in Figures 2.29/2.38 and determine the values of the maximum and minimum elastic section modulii about the centroidal axes.

![image 123](McKenzie - Examples in Structural Analysis_images/imageFile123.png)

###### Figure 2.38

|![image 124](McKenzie - Examples in Structural Analysis_images/imageFile124.png)|
|---|


- 2.2.8 Problems: Second Moments of Area and Elastic Section Modulii

Determine the following values for the sections indicated in Problems 2.1 to 2.6.

|(i) the second moment of areas Ixx and Iyy and<br><br>(ii) the elastic section modulii Zxx and Zyy.<br><br><br>|
|---|


- 2.2.9 Solutions: Second Moments of Area and Elastic Section


##### Modulii

![image 125](McKenzie - Examples in Structural Analysis_images/imageFile125.png)

![image 126](McKenzie - Examples in Structural Analysis_images/imageFile126.png)

![image 127](McKenzie - Examples in Structural Analysis_images/imageFile127.png)

![image 128](McKenzie - Examples in Structural Analysis_images/imageFile128.png)

![image 129](McKenzie - Examples in Structural Analysis_images/imageFile129.png)

![image 130](McKenzie - Examples in Structural Analysis_images/imageFile130.png)

#### 2.3 Plastic Cross-Section Properties

When using elastic theory in design, the acceptance criterion are based on “permissible” or “working” stresses. These are obtained by dividing the “yield stress” py of the material by a suitable Factor of Safety. The loads adopted to evaluate an actual working stress are “working loads”.

In a structure fabricated from linearly elastic material, the Factor of Safety (F. of S.) can also be expressed in terms of the load required to produce yield stress and the working load. This is known as the Load Factor (λ).

|![image 131](McKenzie - Examples in Structural Analysis_images/imageFile131.png)|
|---|


2.3.1 Stress/Strain Relationship

The plastic analysis and design of structures is based on collapse loads. A typical stress-strain curve for a ductile material having the characteristic of providing a large increase in strain beyond the yield point without any increase in stress, (e.g. steel) is given in Figure 2.39.

![image 132](McKenzie - Examples in Structural Analysis_images/imageFile132.png)

- Figure 2.39 When adopting this curve for the theory of plasticity (see Chapter 8) it is idealised as


- indicated in Figure 2.40


![image 133](McKenzie - Examples in Structural Analysis_images/imageFile133.png)

###### Figure 2.40If a beam manufactured from material with a characteristic stress/strain curve as

- shown in Figure 2.39 has a rectangular cross section and is subjected to an increasing bending moment only, then the progression from elastic stress/strain distributions to plastic stress/strain distributions are as indicated in Figure 2.41.


![image 134](McKenzie - Examples in Structural Analysis_images/imageFile134.png)

###### Figure 2.41

Initially at low values of applied moment (a) the maximum stress and strain values are less than the permissible working values as indicated in Figure 2.41 (i.e. between points A and B in Figure 2.40).

As the applied moment increases, then the stress and strain values increase until at stage (b), both attain the yield values εy and py. This corresponds to point C in Figure

- 2.40. A further increase in the applied moment induces yield in some of the inner fibres of


the material. Whilst the extreme fibre strains must now exceed εy, the stress must obviously remain at py. This corresponds to point D in Figure 2.40 and (c) in Figure 2.41.

As the applied moment increases still further, so the whole section eventually reaches the yield stress. (As indicated in (d) there is a very small region around the neutral axis which has not reached yield, but this can be ignored without any appreciable error). When the whole section has attained yield stress then the section cannot provide any further moment resistance and a plastic hinge is formed allowing the beam to rotate at the location of the beam. The value of the applied moment at which this occurs is known as the Plastic Moment of Resistance (Mp).

###### 2.3.2 Plastic Neutral Axis

Obviously at all stages of loading, the compression force (FC) induced by the applied moment must equal the tension force (FT). This being so, then at the formation of the plastic hinge where all the material is subjected to the same stress i.e. py, the plastic neutral axis must be that axis which equally divides the area into two separate parts, i.e.

|![image 135](McKenzie - Examples in Structural Analysis_images/imageFile135.png)|
|---|


and Force in compression=Force in tension

|![image 136](McKenzie - Examples in Structural Analysis_images/imageFile136.png)|
|---|


i.e. Area in compression=Area in tension In plastic analysis the neutral axis is the equal area axis.

##### 2.3.3 Evaluation of Plastic Moment of Resistance (Mp) and Plastic Section Modulus

In elastic analysis the limiting elastic moment can be expressed in terms of the yield stress and the elastic section modulus, at the limit of elasticity;

|![image 137](McKenzie - Examples in Structural Analysis_images/imageFile137.png)|
|---|


Similarly in plastic analysis, the plastic moment of resistance can be expressed in terms of the yield stress and the plastic section modulus.

|![image 138](McKenzie - Examples in Structural Analysis_images/imageFile138.png)|
|---|


Consider the section shown in Figure 2.42.

![image 139](McKenzie - Examples in Structural Analysis_images/imageFile139.png)

###### Figure 2.42

If the rectangular section is subjected to a moment equal to the plastic moment of resistance Mp of the section then we can determine a value for the plastic section modulus.

|![image 140](McKenzie - Examples in Structural Analysis_images/imageFile140.png)|
|---|


![image 141](McKenzie - Examples in Structural Analysis_images/imageFile141.png)

Hence for a rectangular section the Plastic Section Modulus

The Plastic Section Modulus Sxx=1st moment of area about the equal area axis

###### 2.3.4 Shape Factor

The ratio of the plastic modulus to the elastic modulus (or plastic moment to limiting elastic moment) is known as the shape factor given by the symbol ν.

|![image 142](McKenzie - Examples in Structural Analysis_images/imageFile142.png)|
|---|


###### 2.3.5 Section Classification

In design codes the compression elements of structural members are classified into four categories depending upon their resistance to local buckling effects which may influence their load carrying capacity. The compression may be due to direct axial forces, bending moments, or a combination of both. There are two distinct types of element in a cross-section identified in the code:

|1. Outstand elements—elements which are attached to an adjacent element at one edge<br><br>only, the other edge being free, e.g. the flange of an I-section.<br><br>2. Internal elements—elements which are attached to other elements on both<br><br><br>longitudinal edges, including:<br><br>|
|---|


|— webs comprising the internal elements perpendicular to the axis of bending<br><br>— flanges comprising the internal elements parallel to the axis of bending<br><br>|
|---|


e.g. the webs and flanges of a rectangular hollow section. The classifications specified in the code are:

|• Class 1 Plastic Sections<br><br>• Class 2 Compact Sections<br><br>• Class 3 Semi-compact Sections<br><br>• Class 4 Slender Sections<br><br><br>|
|---|


and are determined by consideration of the limiting values given in Tables of the code. The classifications are based on a number of criteria.

2.3.5.1 Aspect Ratio

The aspect ratio for various types of element can be determined using the variables indicated in the code for a wide range of cross-sections. A typical example is the hotrolled I-section indicated in Figure 2.43.

![image 143](McKenzie - Examples in Structural Analysis_images/imageFile143.png)

- Figure 2.43

The limiting aspect ratios given must be modified to allow for the design strength py. This is done by multiplying each limiting ratio by ε which is defined as:

![image 144](McKenzie - Examples in Structural Analysis_images/imageFile144.png)

. In the case of the web of a hybrid section ε should be based on the design strength pyf of the flanges.

In addition to ε, some limiting values also include parameters r1 and r2 which are stress ratios, these are not considered further here.

2.3.5.2 Type of Section

The type of section e.g. universal beam, universal column, circular hollow sections, welded tubes, hot finished rectangular hollow sections, cold formed rectangular hollow sections etc. also influences the classification.

The classifications given in codes indicate the moment/rotation characteristics of a section, as shown in Figure 2.44.

![image 145](McKenzie - Examples in Structural Analysis_images/imageFile145.png)

- Figure 2.44


where:

|Mp = plastic moment of resistance Me = limiting elastic moment of resistance M = elastic moment of resistance<br><br>|
|---|


These characteristics determine whether or not a fully plastic moment can develop within a section and whether or not the section possesses sufficient rotational capacity to permit the section to be used in plastic design.

Consider a section subject to an increasing bending moment; the bending stress diagram changes from a linearly elastic condition with extreme fibre stresses less than the design strength (py), to one in which all of the fibres can be considered to have reached the design strength, as shown in Figure 2.45.

![image 146](McKenzie - Examples in Structural Analysis_images/imageFile146.png)

- Figure 2.45


#### 2.4 Example 2.1: Plastic Cross-section Properties—Section 1

![image 147](McKenzie - Examples in Structural Analysis_images/imageFile147.png)

Determine the position of the plastic neutral axis plastic, the plastic section modulus Sxx and the shape factor υ for the welded section indicated in Figure 2.46.

![image 148](McKenzie - Examples in Structural Analysis_images/imageFile148.png)

###### Figure 2.46

|(i) Position of plastic neutral axis ( plastic)<br><br>![image 149](McKenzie - Examples in Structural Analysis_images/imageFile149.png)<br><br>|
|---|
|A=[(90×10)+(90×15)]=2250 mm2 A/2=(2250/2)=1125 mm2|
|For equal area axis:<br><br>|
|![image 150](McKenzie - Examples in Structural Analysis_images/imageFile150.png)<br><br>plastic=1125/15=75 mm|
|(ii) Plastic section modulus (Sxx): (1st moment of area about the plastic neutral axis)<br><br>|
|Sxx=[(90×10)×20]+[(15×15)×7.5)]+[(75×15)×37.5)]=61.875×103 mm3|
|(iii)<br><br>![image 151](McKenzie - Examples in Structural Analysis_images/imageFile151.png)<br><br>|


#### 2.5 Problems: Plastic Cross-section Properties

Determine the following values for the welded sections indicated in Problems 2.13 to

- 2.16,


|(i) position of the plastic neutral axis plastic,<br><br>![image 152](McKenzie - Examples in Structural Analysis_images/imageFile152.png)<br><br>(ii) the plastic section modulus Sxx and<br><br>(iii) the shape factor υ.<br><br><br>|
|---|


![image 153](McKenzie - Examples in Structural Analysis_images/imageFile153.png)

###### Problem 2.13

![image 154](McKenzie - Examples in Structural Analysis_images/imageFile154.png)

###### Problem 2.14

###### Problem 2.15

###### Problem 2.16

![image 155](McKenzie - Examples in Structural Analysis_images/imageFile155.png)

![image 156](McKenzie - Examples in Structural Analysis_images/imageFile156.png)

#### 2.6 Solutions: Plastic Cross-section Properties

![image 157](McKenzie - Examples in Structural Analysis_images/imageFile157.png)

![image 158](McKenzie - Examples in Structural Analysis_images/imageFile158.png)

![image 159](McKenzie - Examples in Structural Analysis_images/imageFile159.png)

![image 160](McKenzie - Examples in Structural Analysis_images/imageFile160.png)

### 3. Pin-Jointed Frames

#### 3.1 Introduction

The use of beams/plate-girders does not always provide the most economic or suitable structural solution when spanning large openings. In buildings which have lightly loaded, long span roofs, when large voids are required within the depth of roof structures for services, when plated structures are impractical, or for aesthetic/architectural reasons, the use of roof trusses, lattice girders or space-frames may be more appropriate.

Such trusses/girders/frames, generally, transfer their loads by inducing axial tension or compressive forces in the individual members. The magnitude and sense of these forces can be determined using standard methods of analysis such as ‘the method of sections’, ‘the method of joint-resolution’, ‘the method of tension coefficients’ or the use of ‘computer software’. The first three methods indicated are summarized and illustrated in this Chapter.

#### 3.2 Method of Sections

The method of sections involves the application of the three equations of static equilibrium to two-dimensional plane frames. The sign convention adopted to indicate ties (i.e. tension members) and struts (i.e. compression members) in frames is as shown in

- Figure 3.1.


![image 161](McKenzie - Examples in Structural Analysis_images/imageFile161.png)

###### Figure 3.1

The method involves considering an imaginary section line which cuts the frame under consideration into two parts A and B as shown in Figure 3.4.

Since only three independent equations of equilibrium are available any section taken through a frame must not include more than three members for which the internal force is unknown.

Consideration of the equilibrium of the resulting force system enables the magnitude and sense (i.e. compression or tension) of the forces in the cut members to be determined.

###### 3.2.1 Example 3.1: Pin-Jointed Truss

A pin-jointed truss supported by a pinned support at A and a roller support at G carries three loads at joints C, D and E as shown in Figure 3.2. Determine the magnitude and sense of the forces induced in members X, Y and Z as indicated.

![image 162](McKenzie - Examples in Structural Analysis_images/imageFile162.png)

###### Figure 3.2

Step 1: Evaluate the support reactions. It is not necessary to know any information regarding the frame members at this stage other than dimensions as shown in Figure 3.3, since only externally applied loads and reactions are involved.

![image 163](McKenzie - Examples in Structural Analysis_images/imageFile163.png)

###### Figure 3.3

Apply the three equations of static equilibrium to the force system:

|![image 164](McKenzie - Examples in Structural Analysis_images/imageFile164.png)|
|---|


Step 2: Select a section through which the frame can be considered to be cut and using the same three equations of equilibrium determine the magnitude and sense of the unknown forces (i.e. the internal forces in the cut members).

![image 165](McKenzie - Examples in Structural Analysis_images/imageFile165.png)

###### Figure 3.4

It is convenient to assume all unknown forces to be tensile and hence at the cut section their direction and lines of action are considered to be pointing away from the joints (refer to Figure 3.4). If the answer results in a negative force this means that the assumption of a tie was incorrect and the member is actually in compression, i.e. a strut.

The application of the equations of equilibrium to either part of the cut frame will enable the forces X(FDE), Y(FEI) and Z(FHI) to be evaluated.

Note: The section considered must not cut through more than three members with unknown internal forces since only three equations of equilibrium are applicable.

Consider part A:

![image 166](McKenzie - Examples in Structural Analysis_images/imageFile166.png)

###### Figure 3.5

|![image 167](McKenzie - Examples in Structural Analysis_images/imageFile167.png)|
|---|


![image 168](McKenzie - Examples in Structural Analysis_images/imageFile168.png)

![image 169](McKenzie - Examples in Structural Analysis_images/imageFile169.png)

These answers can be confirmed by considering Part B of the structure and applying the equations as above.

#### 3.3 Method of Joint Resolution

Considering the same frame using joint resolution highlights the advantage of the method of sections when only a few member forces are required.

In this technique (which can be considered as a special case of the method of sections), sections are taken which isolate each individual joint in turn in the frame, e.g.

![image 170](McKenzie - Examples in Structural Analysis_images/imageFile170.png)

###### Figure 3.6

In Figure 3.6 four sections are shown, each of which isolates a joint in the structure as indicated in Figure 3.7.

![image 171](McKenzie - Examples in Structural Analysis_images/imageFile171.png)

###### Figure 3.7

Since in each case the forces are coincident, the moment equation is of no value, hence only two independent equations are available. It is necessary when considering the equilibrium of each joint to do so in a sequence which ensures that there are no more than two unknown member forces in the joint under consideration. This can be carried out until all member forces in the structure have been determined.

Consider Joint G:

![image 172](McKenzie - Examples in Structural Analysis_images/imageFile172.png)

Consider Joint F: substitute for calculated values, i.e. FFG (direction of force is into the joint)

![image 173](McKenzie - Examples in Structural Analysis_images/imageFile173.png)

Consider Joint H: substitute for calculated values, i.e. FGH and FFH

![image 174](McKenzie - Examples in Structural Analysis_images/imageFile174.png)

Consider Joint E: substitute for calculated values, i.e. FEF and FEH

![image 175](McKenzie - Examples in Structural Analysis_images/imageFile175.png)

###### 3.3.1 Problems: Method of Sections and Joint Resolution

Determine the support reactions and the forces in the members of the pin-jointed frames indicated by the ‘*’ in Problems 3.1 to 3.4 using the method of sections.

![image 176](McKenzie - Examples in Structural Analysis_images/imageFile176.png)

###### Problem 3.1

![image 177](McKenzie - Examples in Structural Analysis_images/imageFile177.png)

###### Problem 3.2

![image 178](McKenzie - Examples in Structural Analysis_images/imageFile178.png)

###### Problem 3.3

![image 179](McKenzie - Examples in Structural Analysis_images/imageFile179.png)

###### Problem 3.4

Determine the support reactions and the forces in the members of the pin-jointed frames indicated in Problems 3.5 to 3.10 using the method of joint resolution.

###### Problem 3.5

###### Problem 3.6

###### Problem 3.7

![image 180](McKenzie - Examples in Structural Analysis_images/imageFile180.png)

![image 181](McKenzie - Examples in Structural Analysis_images/imageFile181.png)

![image 182](McKenzie - Examples in Structural Analysis_images/imageFile182.png)

![image 183](McKenzie - Examples in Structural Analysis_images/imageFile183.png)

###### Problem 3.8

![image 184](McKenzie - Examples in Structural Analysis_images/imageFile184.png)

###### Problem 3.9

![image 185](McKenzie - Examples in Structural Analysis_images/imageFile185.png)

###### Problem 3.10

###### 3.3.2 Solutions: Method of Sections and Joint Resolution

![image 186](McKenzie - Examples in Structural Analysis_images/imageFile186.png)

![image 187](McKenzie - Examples in Structural Analysis_images/imageFile187.png)

![image 188](McKenzie - Examples in Structural Analysis_images/imageFile188.png)

![image 189](McKenzie - Examples in Structural Analysis_images/imageFile189.png)

![image 190](McKenzie - Examples in Structural Analysis_images/imageFile190.png)

![image 191](McKenzie - Examples in Structural Analysis_images/imageFile191.png)

![image 192](McKenzie - Examples in Structural Analysis_images/imageFile192.png)

![image 193](McKenzie - Examples in Structural Analysis_images/imageFile193.png)

![image 194](McKenzie - Examples in Structural Analysis_images/imageFile194.png)

![image 195](McKenzie - Examples in Structural Analysis_images/imageFile195.png)

![image 196](McKenzie - Examples in Structural Analysis_images/imageFile196.png)

![image 197](McKenzie - Examples in Structural Analysis_images/imageFile197.png)

![image 198](McKenzie - Examples in Structural Analysis_images/imageFile198.png)

![image 199](McKenzie - Examples in Structural Analysis_images/imageFile199.png)

![image 200](McKenzie - Examples in Structural Analysis_images/imageFile200.png)

![image 201](McKenzie - Examples in Structural Analysis_images/imageFile201.png)

![image 202](McKenzie - Examples in Structural Analysis_images/imageFile202.png)

![image 203](McKenzie - Examples in Structural Analysis_images/imageFile203.png)

![image 204](McKenzie - Examples in Structural Analysis_images/imageFile204.png)

![image 205](McKenzie - Examples in Structural Analysis_images/imageFile205.png)

![image 206](McKenzie - Examples in Structural Analysis_images/imageFile206.png)

![image 207](McKenzie - Examples in Structural Analysis_images/imageFile207.png)

![image 208](McKenzie - Examples in Structural Analysis_images/imageFile208.png)

#### 3.4 Method of Tension Coefficients

The method of tension coefficients is a tabular technique of carrying out joint resolution in either two or three dimensions. It is ideally suited to the analysis of pinjointed space-frames.

Consider an individual member from a pin-jointed plane-frame, e.g. member AB

- shown in Figure 3.8 with reference to a particular X-Y co-ordinate system. If AB is a member of length LAB having a tensile force in it of TAB, then the


components of this force in the X and Y directions are TAB Cosθ and TAB Sinθ respectively.

If the co-ordinates of A and B are (XA, YA) and (XB, YB), then the component of TAB in the x-direction is given by :

|![image 209](McKenzie - Examples in Structural Analysis_images/imageFile209.png)|
|---|


![image 210](McKenzie - Examples in Structural Analysis_images/imageFile210.png)

###### Figure 3.8where

![image 211](McKenzie - Examples in Structural Analysis_images/imageFile211.png)

and is known as the tension coefficient of the bar. Similarly, the component of TAB in the y-direction is given by:

|![image 212](McKenzie - Examples in Structural Analysis_images/imageFile212.png)|
|---|


If at joint A in the frame there are a number of bars, i.e. AB, AC … AN, and external

loads XA and YA acting in the X and Y directions, then since the joint is in equilibrium the sum of the components of the external and internal forces must equal zero in each of those directions.

Expressing these conditions in terms of the components of each of the forces then gives:

|![image 213](McKenzie - Examples in Structural Analysis_images/imageFile213.png)<br><br>(1)|
|---|


![image 214](McKenzie - Examples in Structural Analysis_images/imageFile214.png)

(2)

A similar pair of equations can be developed for each joint in the frame giving a total number of equation equal to (2×number of joints)

In a statically determinate triangulated plane-frame the number of unknown member forces is equal to [(2×number of joints)−3], hence there are three additional equations which can be used to determine the reactions or check the values of the tension coefficients.

Once a tension coefficient (e.g. tAB) has been determined, the unknown member force is given by the product:

|![image 215](McKenzie - Examples in Structural Analysis_images/imageFile215.png)|
|---|


Note: A member which has a −ve tension coefficient is in compression and is a strut.

###### 3.4.1 Example 3.2: Two-Dimensional Plane Truss

Consider the pin-jointed, plane-frame ABC loaded as shown in Figure 3.9.

![image 216](McKenzie - Examples in Structural Analysis_images/imageFile216.png)

Construct a table in terms of tension coefficients and an X/Y co-ordinate system as shown in Table 3.1.

The equilibrium equations are solved in terms of the ‘t’ values and hence the member

forces and support reactions are evaluated and entered in the table as shown in Table 3.1. Consider joint B: There are only two unknowns and two equations, hence: Adding both equations

|![image 217](McKenzie - Examples in Structural Analysis_images/imageFile217.png)|
|---|


![image 218](McKenzie - Examples in Structural Analysis_images/imageFile218.png)

Joints A and C can be considered in a similar manner until all unknown values, including reactions, have been determined.

The reader should complete this solution to obtain the following values: FAC=+14.28 kN Ax=+20 kN Ay=−4.29 kN Cy=+14.28 kN

|![image 219](McKenzie - Examples in Structural Analysis_images/imageFile219.png)<br><br>Table 3.1<br><br>|
|---|


In the case of a space frame, each joint has three co-ordinates and the forces have components in the three orthogonal X, Y and Z directions. This leads to (3×Number. of joints) equations which can be solved as above to determine the ‘t’ values and subsequently the member forces and support reactions.

###### 3.4.2 Example 3.3: Three-Dimensional Space Truss

The space frame shown in Figure 3.10 has three pinned supports at A, B and C, all of which lie on the same level as indicated. Member DE is horizontal and at a height of 10

m above the plane of the supports. The planar dimensions (z-x, x-y and z-y) of the frame are indicated in Figure 3.11.

Determine the forces in the members when the frame carries loads of 80 kN and 40 kN acting in a horizontal plane at joints E and D respectively as shown.

![image 220](McKenzie - Examples in Structural Analysis_images/imageFile220.png)

###### Figure 3.10

![image 221](McKenzie - Examples in Structural Analysis_images/imageFile221.png)

Solution:

|![image 222](McKenzie - Examples in Structural Analysis_images/imageFile222.png)|
|---|


The equations from the Tension Coefficient Table are used to determine the ‘t’ values. Since only three equations are available at any joint, only three unknowns can be determined at any one time, i.e. identify a joint with no more that three unknown member forces to begin the calculation; in this case the only suitable joint is D.

Solve the three simultaneous equations at joint D to determine the tension coefficients tAD, tDE and tCD; i.e.

- Consider Joint D: Equations (10), (11) and (12)

|![image 223](McKenzie - Examples in Structural Analysis_images/imageFile223.png)|
|---|


Similarly for the next joint in which there are no more than three unknowns, i.e. Joint E

- Consider Joint E: Equations (13), (14) and (15)


|![image 224](McKenzie - Examples in Structural Analysis_images/imageFile224.png)|
|---|


The support reactions can be determined after the tension coefficient values have been determined using Equations (1) to (9).

The sum of the reactions in the x, y and z directions should be checked by ensuring that they are equal and opposite to the applied load system.

|![image 225](McKenzie - Examples in Structural Analysis_images/imageFile225.png)<br><br>Table 3.2<br><br>|
|---|


###### 3.4.3 Problems: Method of Tension Coefficients

The pin-jointed space-frames shown in Problems 3.11 to 3.16 have three pinned supports at A, B and C as indicated. In each case the supports A, B and C are in the same plane. Using the data given determine:

|(i) the member forces and<br><br>(ii) the support reactions,<br><br><br>|
|---|


when the frames are subjected to the loading indicated.

![image 226](McKenzie - Examples in Structural Analysis_images/imageFile226.png)

###### Problem 3.11

![image 227](McKenzie - Examples in Structural Analysis_images/imageFile227.png)

###### Problem 3.12

![image 228](McKenzie - Examples in Structural Analysis_images/imageFile228.png)

###### Problem 3.13

![image 229](McKenzie - Examples in Structural Analysis_images/imageFile229.png)

###### Problem 3.14

![image 230](McKenzie - Examples in Structural Analysis_images/imageFile230.png)

###### Problem 3.15

![image 231](McKenzie - Examples in Structural Analysis_images/imageFile231.png)

###### Problem 3.16

###### 3.4.4 Solutions: Method of Tension Coefficients

![image 232](McKenzie - Examples in Structural Analysis_images/imageFile232.png)

![image 233](McKenzie - Examples in Structural Analysis_images/imageFile233.png)

![image 234](McKenzie - Examples in Structural Analysis_images/imageFile234.png)

![image 235](McKenzie - Examples in Structural Analysis_images/imageFile235.png)

![image 236](McKenzie - Examples in Structural Analysis_images/imageFile236.png)

![image 237](McKenzie - Examples in Structural Analysis_images/imageFile237.png)

![image 238](McKenzie - Examples in Structural Analysis_images/imageFile238.png)

![image 239](McKenzie - Examples in Structural Analysis_images/imageFile239.png)

![image 240](McKenzie - Examples in Structural Analysis_images/imageFile240.png)

![image 241](McKenzie - Examples in Structural Analysis_images/imageFile241.png)

![image 242](McKenzie - Examples in Structural Analysis_images/imageFile242.png)

![image 243](McKenzie - Examples in Structural Analysis_images/imageFile243.png)

#### 3.5 Unit Load Method for Deflection

The Unit Load Method of analysis is based on the principles of strain energy and Castigliano’s 1st Theorem. When structures deflect under load the work-done by the displacement of the applied loads is stored in the members of the structure in the form of strain energy.

3.5.1 Strain Energy (Axial Load Effects)

Consider an axially loaded structural member of length ‘L’, cross-sectional area ‘A’, and of material with modulus of elasticity ‘E’ as shown in Figure 3.12(a)

![image 244](McKenzie - Examples in Structural Analysis_images/imageFile244.png)

###### Figure 3.12

When an axial load ‘P’ is applied as indicated, the member will increase in length by ‘δL’ as shown in Figure 3.12(b). Assuming linear elastic behaviour δL P, this relationship is represented graphically in Figure 3.13.

![image 245](McKenzie - Examples in Structural Analysis_images/imageFile245.png)

![image 246](McKenzie - Examples in Structural Analysis_images/imageFile246.png)

###### Figure 3.13

The work-done by the externally applied load ‘P’ is equal to: (average value of the force×distance through which the force moves in its line of

action)

|![image 247](McKenzie - Examples in Structural Analysis_images/imageFile247.png)|
|---|


For linearly elastic materials the relationship between the applied axial load and the change in length is:

|![image 248](McKenzie - Examples in Structural Analysis_images/imageFile248.png)|
|---|


This work-done by the externally applied load is equal to the ‘energy’ stored by the member when it changes length and is known as the strain energy, usually given the symbol ‘U’. It is this energy which causes structural members to return to their original length when an applied load system is removed; (Note: assuming that the strains are within the elastic limits of the material).

∴ Strain energy=Work-done by the applied load system

|![image 249](McKenzie - Examples in Structural Analysis_images/imageFile249.png)|
|---|


(Note: the principles of strain energy also apply to members subject to shear, bending, torsion etc.).

###### 3.5.2 Castigliano’s 1st Theorem

Castigliano’s 1st Theorem relating to strain energy and structural deformation can be expressed as follows:

‘If the total strain energy in a structure is partially differentiated with respect to an applied load the result is equal to the displacement of that load in its line of action.’

In mathematical terms this is:

|![image 250](McKenzie - Examples in Structural Analysis_images/imageFile250.png)|
|---|


where:

|U is the total strain energy of the structure due to the applied load system, W is the force acting at the point where the displacement is required, ∆ is the linear displacement in the direction of the line of action of W.<br><br>|
|---|


This form of the theorem is very useful in obtaining the deflection at joints in pinjointed structures. Consider the pin-jointed frame shown in Figure 3.14 in which it is required to determine the vertical deflection of joint B.

![image 251](McKenzie - Examples in Structural Analysis_images/imageFile251.png)

###### Figure 3.14

- Step 1: The member forces induced by the applied load system are calculated, in this case


referred to as the ‘P’ forces, as shown in Figure 3.15.

![image 252](McKenzie - Examples in Structural Analysis_images/imageFile252.png)

###### Figure 3.15

- Step 2: The applied load system is removed from the structure and an imaginary Unit load is


applied at the joint and in the direction of the required deflection, i.e. a vertical load equal to 1.0 at joint B. The resulting member forces due to the unit load are calculated and referred to as the ‘u’ forces, as shown in Figure 3.16.

![image 253](McKenzie - Examples in Structural Analysis_images/imageFile253.png)

###### Figure 3.16

If both the Step 1 and the Step 2 load systems are considered to act simultaneously, then by superposition the total force in each member is given by:

|![image 254](McKenzie - Examples in Structural Analysis_images/imageFile254.png)|
|---|


where:

|P is the force due to the applied load system u is the force due to the applied imaginary Unit load applied at B β is a multiplying factor to reflect the value of the load applied at B (since the unit<br><br>load is an imaginary force the value of β=zero and is used here as a mathematical convenience.)<br><br>|
|---|


The total strain energy in the structure is equal to the sum of the energy stored in all the members:

|![image 255](McKenzie - Examples in Structural Analysis_images/imageFile255.png)|
|---|


Using Castigliano’s 1st Theorem the deflection of joint B is given by:

|![image 256](McKenzie - Examples in Structural Analysis_images/imageFile256.png)|
|---|


and

|![image 257](McKenzie - Examples in Structural Analysis_images/imageFile257.png)|
|---|


Since β=zero the vertical deflection at B (Δβ) is given by:

|![image 258](McKenzie - Examples in Structural Analysis_images/imageFile258.png)|
|---|


i.e. the deflection at any joint in a pin-jointed frame can be determined from:

|![image 259](McKenzie - Examples in Structural Analysis_images/imageFile259.png)|
|---|


where:

|δ is the displacement of the point of application of any load, along the line of<br><br>action of that load, P is the force in a member due to the externally applied loading system, u is the force in a member due to a unit load acting at the position of, and in the<br><br>direction of the desired displacement, L/A is the ratio of the length to the cross-sectional area of the members, E is the modulus of elasticity of the material for each member (i.e. Young’s<br><br>modulus).<br><br>|
|---|


###### 3.5.3 Example 3.4: Deflection of a Pin-Jointed Truss

A pin-jointed truss ABCD is shown in Figure 3.17 in which both a vertical and a horizontal load are applied at joint B as indicated. Determine the magnitude and direction of the resultant deflection at joint B and the vertical deflection at joint D.

![image 260](McKenzie - Examples in Structural Analysis_images/imageFile260.png)

###### Figure 3.17

Step 1: Evaluate the member forces. The reader should follow the procedure given in Example 3.1 to determine the following results:

|Horizontal component of reaction at support A HA=−20.0 kN Vertical component of reaction at support A VA=−4.29 kN<br><br>![image 261](McKenzie - Examples in Structural Analysis_images/imageFile261.png)<br><br>![image 262](McKenzie - Examples in Structural Analysis_images/imageFile262.png)<br><br>Vertical component of reaction at support C VC=+14.29 kN<br><br>![image 263](McKenzie - Examples in Structural Analysis_images/imageFile263.png)<br><br>|
|---|


Use the method of sections or joint resolution as indicated in Sections 3.2 and 3.3 respectively to determine the magnitude and sense of the unknown member forces (i.e. the P forces).

The reader should complete this calculation to determine the member forces as indicated in Figure 3.18.

![image 264](McKenzie - Examples in Structural Analysis_images/imageFile264.png)

###### Figure 3.18

Step 2: To determine uhe vertical deflection at joint B remove the externally applied load system and apply a unit load only in a vertical direction at joint B as shown in Figure

- 3.19. Use the method of sections or joint resolution as before to determine the magnitude and sense of the unknown member forces (i.e. the u forces).


The reader should complete this calculation to determine the member forces as

- indicated in Figure 3.19.


![image 265](McKenzie - Examples in Structural Analysis_images/imageFile265.png)

- Figure 3.19


![image 266](McKenzie - Examples in Structural Analysis_images/imageFile266.png)

The vertical deflection

This is better calculated in tabular form as shown in Table 3.3.

PL×u (kNm) AB 5.0 m A E +7.15 −0.71 −25.38 BC 4.24 m A E −20.20 −0.81 +69.37 AD 4.0 m A E +14.29 +0.57 +32.58 CD 3.0 m A E +14.29 +0.57 +24.44 BD 3.0 m A E 0.0 0.0 0.0

P forces (kN)

u forces

Modulus (E)

|Member|
|---|


|Length (L)<br><br>|
|---|


|Crosssection (A)<br><br>|
|---|


Σ +101.01

- Table 3.3


| |
|---|


The +ve sign indicates that the deflection is in the same direction as the applied unit load.

![image 267](McKenzie - Examples in Structural Analysis_images/imageFile267.png)

Hence the vertical deflection Note: Where the members have different cross-sectional areas and/or modulii of

elasticity each entry in the last column of the table should be based on (PL×u)/AE and not only (PL×u).

- A similar calculation can be carried out to determine the horizontal deflection at joint
- B. The reader should complete this calculation to determine the member forces as


- indicated in Figure 3.20.


![image 268](McKenzie - Examples in Structural Analysis_images/imageFile268.png)

###### Figure 3.20

![image 269](McKenzie - Examples in Structural Analysis_images/imageFile269.png)

The horizontal deflection

| | | | | | | |
|---|---|---|---|---|---|---|
||Member|
|---|
||Length (L)<br><br>|
|---|
| | ||P forces (kN)<br><br>|
|---|
| | |
| | |Crosssection (A)<br><br>|Modulus (E)<br><br>| |u forces<br><br>|PL×u (kNm)<br><br>|
| | | | | | | |
|AB|5.0 m|A|E|+7.15|+0.71|+25.74|
|BC|4.24 m|A|E|−20.20|−0.61|+52.25|
|AD|4.0 m|A|E|+14.29|+0.43|+24.58|


CD 3.0 m A E +14.29 +0.43 +18.43 BD 3.0 m A E 0.0 0.0 0.0

###### Σ +121.00

###### Table 3.4

![image 270](McKenzie - Examples in Structural Analysis_images/imageFile270.png)

Hence the horizontal deflection The resultant deflection at joint B can be determined from the horizontal and vertical

components evaluated above, i.e.

|![image 271](McKenzie - Examples in Structural Analysis_images/imageFile271.png)|
|---|


A similar calculation can be carried out to determine the vertical deflection at joint D. The reader should complete this calculation to determine the member forces as

- indicated in Figure 3.21.


![image 272](McKenzie - Examples in Structural Analysis_images/imageFile272.png)

###### Figure 3.21

![image 273](McKenzie - Examples in Structural Analysis_images/imageFile273.png)

The vertical deflection

PL×u (kNm) AB 5.0 m A E +7.15 −0.71 −25.38 BC 4.24 m A E −20.20 −0.81 +69.37 AD 4.0 m A E +14.29 +0.57 +32.58 CD 3.0 m A E +14.29 +0.57 +24.44 BD 3.0 m A E 0.0 +1.0 0.0

P forces (kN)

u forces

Modulus (E)

|Member|
|---|


|Length (L)<br><br>|
|---|


|Crosssection (A)<br><br>|
|---|


Σ +101.01

- Table 3.5


![image 274](McKenzie - Examples in Structural Analysis_images/imageFile274.png)

Hence the vertical deflection

3.5.3.1 Fabrication Errors—(Lack-of-fit)

During fabrication it is not unusual for a member length to be slightly too short or too long and assembly is achieved by forcing members in to place. The effect of this can be accommodated very easily in this method of analysis by adding additional terms relating to each member for which lack-of-fit applies. The δL term for the relevant members is equal to the magnitude of the error in length, i.e. ΔL where negative values relate to members which are too short and positive values to members which are too long.

![image 275](McKenzie - Examples in Structural Analysis_images/imageFile275.png)

(Note: under normal applied loading the )

###### 3.5.3.2 Changes in Temperature

The effects of temperature change in members can also be accommodated in a similar manner; in this case the δL term is related to the coefficient of thermal expansion for the material, the change in temperature and the original length,

|i.e. δL=αLΔT|
|---|


where

|a is the coefficient of thermal expansion, L is the original length, ΔT is the change in temperature—a reduction being considered negative and an<br><br>increase being positive.<br><br>|
|---|


Since this is an elastic analysis the principle of superposition can be used to obtain results when a combination of applied load, lack-of-fit and/or temperature difference occurs. This is illustrated in Example 3.5.

###### 3.5.4 Example 3.5: Lack-of-fit and Temperature Difference

Consider the frame indicated in Example 3.4 and determine the vertical deflection at joint D assuming the existing loading and that member BC is too short by 2.0 mm, member CD is too long by 1.5 mm and that members AD and CD are both subject to an increase in temperature of 5ºC. Assume α=12.0×10−6/°C and AE=100×103 kN.

![image 276](McKenzie - Examples in Structural Analysis_images/imageFile276.png)

###### Figure 3.22

The δL value for member BC due to lack-of-fit ∆L=−2.0 mm The δL value for member CD due to lack-of-fit ∆L=+1.5 mm

|![image 277](McKenzie - Examples in Structural Analysis_images/imageFile277.png)|
|---|


![image 278](McKenzie - Examples in Structural Analysis_images/imageFile278.png)

AE (kN) P-

(PL/AE+ΔL+ΔT)×u (mm)

PL/AE (mm)

Length (mm)

|Member|
|---|


|ΔT (mm)<br><br>|
|---|


|u|
|---|


ΔL (mm)

force (kN)

AB 5000 100×103 +7.15 +0.36 0 0 −0.71 −0.26 BC 4243 100×103 −20.20 −0.86 −2.0 0 −0.81 +2.32 AD 4000 100×103 +14.29 +0.57 0 +0.24 +0.57 +0.46 CD 3000 100×103 +14.29 +0.43 +1.5 +0.18 +0.57 +1.20 BD 3000 100×103 0 0 0 0 1.0 0

Σ=+3.72

- Table 3.6


The vertical deflection at joint D due to combined loading, lack-of-fit and temperature change is given by:

|![image 279](McKenzie - Examples in Structural Analysis_images/imageFile279.png)|
|---|


Note: Statically determinate, pin-jointed frames can accommodate small changes in geometry without any significant effect on the member forces induced by the applied load system, i.e. the member forces in Example 3.5 are the same as those in Example 3.4.

###### 3.5.5 Problems: Unit Load Method for Deflection of Pin-Jointed Frames

A series of pin-jointed frames are shown in Problems 3.17 to 3.20. Using the applied load systems and data given in each case, determine the value of the deflections indicated. Assume E=205 kN/mm2 and α=12×10−6/ºC where required.

![image 280](McKenzie - Examples in Structural Analysis_images/imageFile280.png)

###### Problem 3.17

![image 281](McKenzie - Examples in Structural Analysis_images/imageFile281.png)

###### Problem 3.18

![image 282](McKenzie - Examples in Structural Analysis_images/imageFile282.png)

###### Problem 3.19

![image 283](McKenzie - Examples in Structural Analysis_images/imageFile283.png)

###### Problem 3.20

###### 3.5.6 Solutions: Unit Load Method for Deflection of Pin-Jointed Frames

![image 284](McKenzie - Examples in Structural Analysis_images/imageFile284.png)

![image 285](McKenzie - Examples in Structural Analysis_images/imageFile285.png)

![image 286](McKenzie - Examples in Structural Analysis_images/imageFile286.png)

![image 287](McKenzie - Examples in Structural Analysis_images/imageFile287.png)

![image 288](McKenzie - Examples in Structural Analysis_images/imageFile288.png)

![image 289](McKenzie - Examples in Structural Analysis_images/imageFile289.png)

![image 290](McKenzie - Examples in Structural Analysis_images/imageFile290.png)

![image 291](McKenzie - Examples in Structural Analysis_images/imageFile291.png)

![image 292](McKenzie - Examples in Structural Analysis_images/imageFile292.png)

![image 293](McKenzie - Examples in Structural Analysis_images/imageFile293.png)

![image 294](McKenzie - Examples in Structural Analysis_images/imageFile294.png)

![image 295](McKenzie - Examples in Structural Analysis_images/imageFile295.png)

#### 3.6 Unit Load Method for Singly-Redundant Pin-Jointed Frames

The method of analysis illustrated in Section 3.5 can also be adopted to determine the member forces in singly-redundant frames. Consider the frame shown in Example 3.6.

3.6.1 Example 3.6: Singly-Redundant Pin-Jointed Frame 1

Using the data given, determine the member forces and support reactions for the pinjointed frame shown in Figure 3.23.

![image 296](McKenzie - Examples in Structural Analysis_images/imageFile296.png)

- Figure 3.23

The degree-of-indeterminacy ID=(m+r)−2n=(5+4)−(2×4)=1 Assume that member BD is a redundant member and consider the original frame to be

the superposition of two structures as indicated in Figures 3.24(a) and (b). The frame in

- Figure 3.24(b) can be represented as shown in Figure 3.25.


![image 297](McKenzie - Examples in Structural Analysis_images/imageFile297.png)

- Figure 3.24


![image 298](McKenzie - Examples in Structural Analysis_images/imageFile298.png)

###### Figure 3.25

To maintain compatibility in the length of member BD in the original frame the change in length of the diagonal BD in Figure 3.24(a) must be equal and opposite to that in Figure 3.24(b) as shown in Figure 3.26.

![image 299](McKenzie - Examples in Structural Analysis_images/imageFile299.png)

###### Figure 3.26

(δ′BD due to P-forces)+(δ″BD due to unit load forces)×FBD=0

|![image 300](McKenzie - Examples in Structural Analysis_images/imageFile300.png)|
|---|


Using joint resolution the P-forces and the u-forces can be determined as indicated in

###### Figure 3.27.

![image 301](McKenzie - Examples in Structural Analysis_images/imageFile301.png)

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
||Member|
|---|
||Length (mm)<br><br>|
|---|
| ||Pforce (kN)<br><br>|
|---|
| | | | | |
| | |AE (kN)| |PL/AE (mm)<br><br>|u|(PL/AE)×u (mm)<br><br>|(uL/AE)×u (mm)<br><br>|Memb force<br><br>|
| | | | | | | | | |
| | | | | | | | | |
|BC|3000|35.88×103|+10.00|+0.84|−0.71|−0.59|0.04|+4.38|
|CD|3000|35.88×103|+10.00|+0.84|−0.71|−0.59|0.04|+4.38|
|DA|3000|35.88×103|0|0|−0.71|0|0.04|−5.62|
|AC|4243|35.88×103|−14.14|−1.67|+1.00|−1.67|0.12|−6.23|
|BD|4243|35.88×103|0|0|+1.00|0|0.12|+7.91|
| | | | | | |Σ=−2.85|Σ=+0.36| |
| | | | | | | | | |


![image 302](McKenzie - Examples in Structural Analysis_images/imageFile302.png)

###### The final member forces=[P-forces+(u-forces×7.91)] and are given in the last column of the table

![image 303](McKenzie - Examples in Structural Analysis_images/imageFile303.png)

###### 3.6.2 Example 3.7: Singly-Redundant Pin-Jointed Frame 2

Using the data given, determine the member forces and support reactions for the pinjointed frame shown in Figure 3.29.

The cross-sectional area of all members is equal to 140 mm2. Assume E=205 kN/mm2

![image 304](McKenzie - Examples in Structural Analysis_images/imageFile304.png)

- Figure 3.29


|All member lengths L=3.0 m AE=(140×205)=28.7×103 kN Sin60º=0.866 Cos60º=0.5|
|---|


![image 305](McKenzie - Examples in Structural Analysis_images/imageFile305.png)

The degree of indeterminacy ID=(m+r)−2n=(8+7)−(2×7)=1

Consider the vertical reaction at support F to be redundant. The equivalent system is the superposition of the statically determinate frame and the (unit load frame×VF) as shown in Figures 3.30 and 3.31.

![image 306](McKenzie - Examples in Structural Analysis_images/imageFile306.png)

###### Figure 3.30

![image 307](McKenzie - Examples in Structural Analysis_images/imageFile307.png)

###### Figure 3.31

Using joint resolution the P-forces and the u-forces can be determined as indicated in Figures 3.32 and 3.33.

![image 308](McKenzie - Examples in Structural Analysis_images/imageFile308.png)

###### Figure 3.32

![image 309](McKenzie - Examples in Structural Analysis_images/imageFile309.png)

- Figure 3.33


(uL/AE)×u (mm)

PL/AE (mm)

u (PL/AE)

Length (mm)

Member forces

Mem ber

|AE (kN)|
|---|


|Pforce (kN)<br><br>|
|---|


×u (mm)

AB 3000 28.7×103 0 0 0 0 0 0 BC 3000 28.7×103 0 0 0 0 0 0 CD 3000 28.7×103 0 0 +0.58 0 0.035 0 DE 3000 28.7×103 0 0 +0.58 0 0.035 0 DF 3000 28.7×103 0 0 −0.58 0 0.035 0 CF 3000 28.7×103 0 0 −0.58 0 0.035 0 CG 3000 28.7×103 0 0 +0.58 0 0.035 0 BG 3000 28.7×103 −30.00 −3.14 0 0 0 −30.00

Σ=zero Σ=+0.18

![image 310](McKenzie - Examples in Structural Analysis_images/imageFile310.png)

The final member forces=[P-forces+(u-forces×0)] and are given in the last column of the table.

|VG=+25.98 kN HG=−15.0 kN<br><br>![image 311](McKenzie - Examples in Structural Analysis_images/imageFile311.png)<br><br>![image 312](McKenzie - Examples in Structural Analysis_images/imageFile312.png)|
|---|


All other reactions are equal to zero.

![image 313](McKenzie - Examples in Structural Analysis_images/imageFile313.png)

- Figure 3.34


###### 3.6.3 Problems: Unit Load Method for Singly-Redundant PinJointed Frames

Using the data given in the singly-redundant, pin-jointed frames shown in Problems

- 3.21 to 3.24, determine the support reactions and the member forces due to the applied loads. Assume E=205 kN/mm2 and α=12×10−6/°C where required.


![image 314](McKenzie - Examples in Structural Analysis_images/imageFile314.png)

###### Problem 3.21

![image 315](McKenzie - Examples in Structural Analysis_images/imageFile315.png)

###### Problem 3.22

![image 316](McKenzie - Examples in Structural Analysis_images/imageFile316.png)

###### Problem 3.23

![image 317](McKenzie - Examples in Structural Analysis_images/imageFile317.png)

###### Problem 3.24

###### 3.6.4 Solutions: Unit Load Method for Singly-Redundant PinJointed Frames

![image 318](McKenzie - Examples in Structural Analysis_images/imageFile318.png)

![image 319](McKenzie - Examples in Structural Analysis_images/imageFile319.png)

![image 320](McKenzie - Examples in Structural Analysis_images/imageFile320.png)

![image 321](McKenzie - Examples in Structural Analysis_images/imageFile321.png)

![image 322](McKenzie - Examples in Structural Analysis_images/imageFile322.png)

![image 323](McKenzie - Examples in Structural Analysis_images/imageFile323.png)

![image 324](McKenzie - Examples in Structural Analysis_images/imageFile324.png)

![image 325](McKenzie - Examples in Structural Analysis_images/imageFile325.png)

![image 326](McKenzie - Examples in Structural Analysis_images/imageFile326.png)

![image 327](McKenzie - Examples in Structural Analysis_images/imageFile327.png)

![image 328](McKenzie - Examples in Structural Analysis_images/imageFile328.png)

![image 329](McKenzie - Examples in Structural Analysis_images/imageFile329.png)

![image 330](McKenzie - Examples in Structural Analysis_images/imageFile330.png)

![image 331](McKenzie - Examples in Structural Analysis_images/imageFile331.png)

![image 332](McKenzie - Examples in Structural Analysis_images/imageFile332.png)

![image 333](McKenzie - Examples in Structural Analysis_images/imageFile333.png)

### 4. Beams

#### 4.1 Statically Determinate Beams

Two parameters which are fundamentally important to the design of beams are shear force and bending moment. These quantities are the result of internal forces acting on the material of a beam in response to an externally applied load system.

4.1.1 Example 4.1: Beam with Point Loads

Consider a simply supported beam as shown in Figure 4.1 carrying a series of secondary beams each imposing a point load of 4 kN.

![image 334](McKenzie - Examples in Structural Analysis_images/imageFile334.png)

- Figure 4.1 This structure can be represented as a line diagram as shown in Figure 4.2:


![image 335](McKenzie - Examples in Structural Analysis_images/imageFile335.png)

###### Figure 4.2

Since the externally applied force system is in equilibrium, the three equations of static equilibrium must be satisfied, i.e.

|+ve ↑ ΣFy=0 The sum of the vertical forces must equal zero.<br><br>![image 336](McKenzie - Examples in Structural Analysis_images/imageFile336.png)<br><br>The sum of the moments of all forces about any point on the plane of the forces must equal zero.<br><br>+ve→ ΣFx=0 The sum of the horizontal forces must equal zero.<br><br>|
|---|


The assumed positive directions are as indicated. In this particular problem there are no externally applied horizontal forces and consequently the third equation is not required.

(Note: It is still necessary to provide horizontal restraint to a structure since it can be subject to a variety of load cases, some of which may have a horizontal component.)

Consider the vertical equilibrium of the beam:

|![image 337](McKenzie - Examples in Structural Analysis_images/imageFile337.png)<br><br>Equation<br><br>(1)|
|---|


Note: The sum of the moments is taken about one end of the beam (end A) for convenience. Since one of the forces (VA) passes through this point it does not produce a moment about A and hence does not appear in the equation. It should be recognised that the sum of the moments could have been considered about any known point in the same plane.

|![image 338](McKenzie - Examples in Structural Analysis_images/imageFile338.png)<br><br>Equation<br><br>(2)|
|---|


This calculation was carried out considering only the externally applied forces, i.e.

![image 339](McKenzie - Examples in Structural Analysis_images/imageFile339.png)

- Figure 4.3


The structure itself was ignored, however the applied loads are transferred to the end supports through the material fibres of the beam. Consider the beam to be cut at section X–X producing two sections each of which is in equilibrium as shown in Figure 4.4.

![image 340](McKenzie - Examples in Structural Analysis_images/imageFile340.png)

- Figure 4.4

Clearly if the two sections are in equilibrium there must be internal forces acting on the cut surfaces to maintain this; these forces are known as the shear force and the bending moment, and are illustrated in Figure 4.5

![image 341](McKenzie - Examples in Structural Analysis_images/imageFile341.png)

- Figure 4.5


The force V and moment M are equal and opposite on each surface. The magnitude and direction of V and M can be determined by considering two equations of static equilibrium for either of the cut sections; both will give the same answer.

Consider the left-hand section with the ‘assumed’ directions of the internal forces V and M as shown in Figure 4.6.

![image 342](McKenzie - Examples in Structural Analysis_images/imageFile342.png)

- Figure 4.6

4.1.2 Shear Force Diagrams

In a statically determinate beam, the numerical value of the shear force can be obtained by evaluating the algebraic sum of the vertical forces to one side of the section being considered. The convention adopted in this text to indicate positive and negative shear forces is shown in Figure 4.7.

![image 343](McKenzie - Examples in Structural Analysis_images/imageFile343.png)

- Figure 4.7


The calculation carried out to determine the shear force can be repeated at various locations along a beam and the values obtained plotted as a graph; this graph is known as the shear force diagram. The shear force diagram indicates the variation of the shear force along a structural member.

Consider any section of the beam between A and B:

![image 344](McKenzie - Examples in Structural Analysis_images/imageFile344.png)

Note: The value immediately under the point load at the cut section is not being considered.

|![image 345](McKenzie - Examples in Structural Analysis_images/imageFile345.png)|
|---|


This value is a constant for all values of x between zero and 600 mm, the graph will therefore be a horizontal line equal to 10.0 kN. This force produces a +ve shear effect, i.e.

![image 346](McKenzie - Examples in Structural Analysis_images/imageFile346.png)

Consider any section of the beam between B and C:

![image 347](McKenzie - Examples in Structural Analysis_images/imageFile347.png)

|![image 348](McKenzie - Examples in Structural Analysis_images/imageFile348.png)|
|---|


This value is a constant for all values of x between 600 mm and 1200 mm, the graph will therefore be a horizontal line equal to 6.0 kN. This force produces a +ve effect shear effect.

###### Similarly for any section between C and D:

![image 349](McKenzie - Examples in Structural Analysis_images/imageFile349.png)

|![image 350](McKenzie - Examples in Structural Analysis_images/imageFile350.png)|
|---|


Consider any section of the beam between D and E:

|![image 351](McKenzie - Examples in Structural Analysis_images/imageFile351.png)|
|---|


![image 352](McKenzie - Examples in Structural Analysis_images/imageFile352.png)

|![image 353](McKenzie - Examples in Structural Analysis_images/imageFile353.png)|
|---|


![image 354](McKenzie - Examples in Structural Analysis_images/imageFile354.png)

and

|![image 355](McKenzie - Examples in Structural Analysis_images/imageFile355.png)|
|---|


In each of the cases above the value has not been considered at the point of application of the load.

Consider the location of the applied load at B shown in Figure 4.8.

![image 356](McKenzie - Examples in Structural Analysis_images/imageFile356.png)

- Figure 4.8


The 4.0 kN is not instantly transferred through the beam fibres at B but instead over the width of the actual secondary beam. The change in value of the shear force between x<600 mm and x>600 mm occurs over this width, as shown in Figure 4.9.

![image 357](McKenzie - Examples in Structural Analysis_images/imageFile357.png)

###### Figure 4.9

The width of the secondary beam is insignificant when compared with the overall span, and the shear force is assumed to change instantly at this point, producing a vertical line on the shear force diagram as shown in Figure 4.10.

![image 358](McKenzie - Examples in Structural Analysis_images/imageFile358.png)

###### Figure 4.10The full shear force diagram can therefore be drawn as shown in Figure 4.11.

![image 359](McKenzie - Examples in Structural Analysis_images/imageFile359.png)

###### Figure 4.11

The same result can be obtained by considering sections from the right-hand side of the beam.

4.1.3 Bending Moment Diagrams

In a statically determinate beam the numerical value of the bending moment (i.e. moments caused by forces which tend to bend the beam) can be obtained by evaluating the algebraic sum of the moments of the forces to one side of a section. In the same manner as with shear forces either the left-hand or the right-hand side of the beam can be considered. The convention adopted in this text to indicate positive and negative bending moments is shown in Figures 4.12(a) and (b).

Bending inducing tension on the underside of a beam is considered positive.

![image 360](McKenzie - Examples in Structural Analysis_images/imageFile360.png)

###### Figure 4.12(a)Bending inducing tension on the top of a beam is considered negative.

![image 361](McKenzie - Examples in Structural Analysis_images/imageFile361.png)

- Figure 4.12(b)


Note: Clockwise/anti-clockwise moments do not define +ve or −νe bending moments. The sign of the bending moment is governed by the location of the tension surface at the point being considered.

As with shear forces the calculation for bending moments can be carried out at various locations along a beam and the values plotted on a graph; this graph is known as the ‘bending moment diagram’. The bending moment diagram indicates the variation in the bending moment along a structural member.

- Consider sections between A and B of the beam as before:


![image 362](McKenzie - Examples in Structural Analysis_images/imageFile362.png)

In this case when x=600 mm the 4.0 kN load passes through the section being considered and does not produce a bending moment, and can therefore be ignored.

|![image 363](McKenzie - Examples in Structural Analysis_images/imageFile363.png)|
|---|


Unlike the shear force, this expression is not a constant and depends on the value of ‘x’ which varies between the limits given. This is a linear expression which should be reflected in the calculated values of the bending moment.

x=0 Mx= 10.0×0=zero x=200 mm Mx=10.0×0.2=2.0 kNm

x=400 mm Mx=10.0×0.4=4.0 kNm x=600 mm Mx=10.0×0.6–6.0 kNm

Clearly the bending moment increases linearly from zero at the simply supported end to a value of 6.0 kNm at point B.

- Consider sections between B and C of the beam:


|![image 364](McKenzie - Examples in Structural Analysis_images/imageFile364.png)|
|---|


![image 365](McKenzie - Examples in Structural Analysis_images/imageFile365.png)

![image 366](McKenzie - Examples in Structural Analysis_images/imageFile366.png)

|x=800 mm Mx =+(10.0×0.8)−(4.0×0.2)=7.2 kNm x=1000 mm Mx=+(10.0×1.0)−(4.0×0.4)−8.4 kNm x=1200 mm Mx =+(10.0×1.2)−(4.0×0.6)=9.6 kNm<br><br>|
|---|


As before the bending moment increases linearly, i.e. from 7.2 kNm at x=800 mm to a value of 9.6 kNm at point C.

Since the variation is linear it is only necessary to evaluate the magnitude and sign of the bending moment at locations where the slope of the line changes, i.e. each of the point load locations.

###### Consider point D:

![image 367](McKenzie - Examples in Structural Analysis_images/imageFile367.png)

|![image 368](McKenzie - Examples in Structural Analysis_images/imageFile368.png)|
|---|


Consider point E:

![image 369](McKenzie - Examples in Structural Analysis_images/imageFile369.png)

|![image 370](McKenzie - Examples in Structural Analysis_images/imageFile370.png)|
|---|


Similarly at point F:

|![image 371](McKenzie - Examples in Structural Analysis_images/imageFile371.png)|
|---|


The full bending moment diagram can therefore be drawn as shown in Figure 4.13.

![image 372](McKenzie - Examples in Structural Analysis_images/imageFile372.png)

###### Figure 4.13

The same result can be obtained by considering sections from the right-hand side of the beam. The value of the bending moment at any location can also be determined by evaluating the area under the shear force diagram.

Consider point B:

![image 373](McKenzie - Examples in Structural Analysis_images/imageFile373.png)

|Bending moment at B=shaded area on the shear force diagram MB=(10.0×0.6)=6.0 kNm as before|
|---|


Consider a section at a distance of x=900 mm along the beam between D and E:

![image 374](McKenzie - Examples in Structural Analysis_images/imageFile374.png)

|Bending moment at x=shaded area on the shear force diagram Mx=(10.0×0.6)+(6.0×0.3)=7.8 kNm as before Consider a section at a distance of x=2100 mm along the beam|
|---|


|between D and E:|
|---|


![image 375](McKenzie - Examples in Structural Analysis_images/imageFile375.png)

Bending moment at x=shaded area on the shear force diagram

|![image 376](McKenzie - Examples in Structural Analysis_images/imageFile376.png)|
|---|


(Note: A maximum bending moment occurs at the same position as a zero shear force.)

###### 4.1.4 Example 4.2: Beam with a Uniformly Distributed Load (UDL)

Consider a simply-supported beam carrying a uniformly distributed load of 5 kN/m, as shown in Figure 4.14

![image 377](McKenzie - Examples in Structural Analysis_images/imageFile377.png)

###### Figure 4.14

The shear force at any section a distance x from the support at A is given by: Vx=algebraic sum of the vertical forces

![image 378](McKenzie - Examples in Structural Analysis_images/imageFile378.png)

This is a linear equation in which Vx decreases as x increases. The points of interest are at the supports where the maximum shear forces occur, and at the locations where the maximum bending moment occurs, i.e. the point of zero shear.

|Vx=0 when +9.0−5.0x=0 ∴ x=1.8 m|
|---|


Any intermediate value can be found by substituting the appropriate value of ‘x’ in the equation for the shear force; e.g.

|x=600 mm Vx =+9.0−(5.0×0.6)=+6.0 kN x=2100 mm Vx =+9.0−(5.0×2.1) =−1.5 kN<br><br>|
|---|


The shear force can be drawn as shown in Figure 4.15.

![image 379](McKenzie - Examples in Structural Analysis_images/imageFile379.png)

###### Figure 4.15

The bending moment can be determined as before, either using an equation or evaluating the area under the shear force diagram.

###### Using an equation:

![image 380](McKenzie - Examples in Structural Analysis_images/imageFile380.png)

Bending moment at x: Mx =+(9.0×x)−[(5.0×x)×(x/2)]=(9.0x−2.5x2)

In this case the equation is not linear, and the bending moment diagram will therefore be curved. Consider several values:

|x=0 Mx=zero x=600 mm Mx =+(9.0×0.6)−(2.5×0.62)=4.5 kNm x=1800 mm Mx =+(9.0×1.8)−(2.5×1.82)=8.1 kNm x=2100 mm Mx =+(9.0×2.1)−(2.5×2.12)=7.88 kNm<br><br>|
|---|


Using the shear force diagram:

|![image 381](McKenzie - Examples in Structural Analysis_images/imageFile381.png)|
|---|


Mx=shaded area =+[0.5×(9.0+6.0)×0.6]=4.5 kNm

|![image 382](McKenzie - Examples in Structural Analysis_images/imageFile382.png)|
|---|


###### x=2100 mm

Mx=shaded area =+[0.5×9.0×1.8]=8.1 kNm

|![image 383](McKenzie - Examples in Structural Analysis_images/imageFile383.png)|
|---|


Mx=shaded area =+[8.1−(0.5×0.3×1.5)]=7.88 kNm

The bending moment diagram is shown in Figure 4.16.

![image 384](McKenzie - Examples in Structural Analysis_images/imageFile384.png)

- Figure 4.16

The UDL loading is a ‘standard’ load case which occurs in numerous beam designs and can be expressed in general terms using L for the span and w for the applied load/metre or Wtotal(= wL) for the total applied load, as shown in Figure 4.17.

![image 385](McKenzie - Examples in Structural Analysis_images/imageFile385.png)

- Figure 4.17


Clearly both give the same magnitude of support reactions, shear forces and bending moments.

In cantilever beams, all support restraints are provided at one location, i.e. an ‘encastre’ or ‘fixed’ support as shown in Example 4.3.

###### 4.1.5 Example 4.3: Cantilever Beam

Consider the cantilever beam shown in Figure 4.18 which is required to support a uniformly distributed load in addition to a mid-span point load as indicated.

![image 386](McKenzie - Examples in Structural Analysis_images/imageFile386.png)

###### Figure 4.18Support Reactions

|![image 387](McKenzie - Examples in Structural Analysis_images/imageFile387.png)|
|---|


Shear force at B:

###### VB=[51.0−(6.0×3.0)]=33.0 kN and=(33.0–15.0)=18.0 kN

![image 388](McKenzie - Examples in Structural Analysis_images/imageFile388.png)

###### 4.1.6 Problems: Statically Determinate Beams—Shear Force and Bending Moment

A series of simply supported beams are indicated in Problems 4.1 to 4.10. Using the applied loading given in each case:

|i) determine the support reactions,<br><br>ii) sketch the shear force diagram and<br><br>iii) sketch the bending moment diagram indicating the maximum value(s).<br><br><br>|
|---|


![image 389](McKenzie - Examples in Structural Analysis_images/imageFile389.png)

###### Problem 4.1

![image 390](McKenzie - Examples in Structural Analysis_images/imageFile390.png)

###### Problem 4.2

![image 391](McKenzie - Examples in Structural Analysis_images/imageFile391.png)

###### Problem 4.3

![image 392](McKenzie - Examples in Structural Analysis_images/imageFile392.png)

###### Problem 4.4

![image 393](McKenzie - Examples in Structural Analysis_images/imageFile393.png)

###### Problem 4.5

![image 394](McKenzie - Examples in Structural Analysis_images/imageFile394.png)

###### Problem 4.6

![image 395](McKenzie - Examples in Structural Analysis_images/imageFile395.png)

###### Problem 4.7

![image 396](McKenzie - Examples in Structural Analysis_images/imageFile396.png)

###### Problem 4.8

![image 397](McKenzie - Examples in Structural Analysis_images/imageFile397.png)

###### Problem 4.9

![image 398](McKenzie - Examples in Structural Analysis_images/imageFile398.png)

###### Problem 4.10

###### 4.1.7 Solutions: Statically Determinate Beams—Shear Force and Bending Moment

![image 399](McKenzie - Examples in Structural Analysis_images/imageFile399.png)

![image 400](McKenzie - Examples in Structural Analysis_images/imageFile400.png)

![image 401](McKenzie - Examples in Structural Analysis_images/imageFile401.png)

![image 402](McKenzie - Examples in Structural Analysis_images/imageFile402.png)

![image 403](McKenzie - Examples in Structural Analysis_images/imageFile403.png)

![image 404](McKenzie - Examples in Structural Analysis_images/imageFile404.png)

![image 405](McKenzie - Examples in Structural Analysis_images/imageFile405.png)

![image 406](McKenzie - Examples in Structural Analysis_images/imageFile406.png)

![image 407](McKenzie - Examples in Structural Analysis_images/imageFile407.png)

![image 408](McKenzie - Examples in Structural Analysis_images/imageFile408.png)

#### 4.2 McCaulay’s Method for the Deflection of Beams

In elastic analysis the deflected shape of a simply supported beam is normally assumed to be a circular arc of radius R (R is known as the radius of curvature), as shown in Figure 4.19.

![image 409](McKenzie - Examples in Structural Analysis_images/imageFile409.png)

- Figure 4.19


Consider the beam AB to be subject to a variable bending moment along its length. The beam is assumed to deflect as indicated.

R is the radius of curvature, L is the span, I is the second moment of area about the axis of bending, E is the modulus of elasticity, ds is an elemental length of beam measured a distance of x from the left-

hand end

###### M is the value of the bending moment at position x.

The slope of the beam at position x is given by:

|![image 410](McKenzie - Examples in Structural Analysis_images/imageFile410.png)|
|---|


Differentiating the slope with respect to x gives:

|![image 411](McKenzie - Examples in Structural Analysis_images/imageFile411.png)<br><br>Equation<br><br>(1)bending moment (Mx)|
|---|


- Integrating Equation (1) with respect to x gives

|![image 412](McKenzie - Examples in Structural Analysis_images/imageFile412.png)<br><br>Equation<br><br>(2)EI×slop e (EIθ)|
|---|


- Integrating Equation (2) with respect to x gives


|![image 413](McKenzie - Examples in Structural Analysis_images/imageFile413.png)<br><br>Equation<br><br>(3)EI×deflectio n (EIδ)|
|---|


Equations (1) and (2) result in two constants of integration A and B; these are determined by considering boundary conditions such as known values of slope and/or deflection at positions on the beam.

###### 4.2.1 Example 4.4: Beam with Point Loads

Consider a beam supporting three point loads as shown in Figure 4.20.

![image 414](McKenzie - Examples in Structural Analysis_images/imageFile414.png)

- Figure 4.20

Step 1: Formulate an equation which represents the value of the bending moment at a position measured x from the left-hand end of the beam. This expression must include all of the loads and x should therefore be considered between points D and E.

![image 415](McKenzie - Examples in Structural Analysis_images/imageFile415.png)

- Figure 4.21 Consider the vertical equilibrium of the beam:


|![image 416](McKenzie - Examples in Structural Analysis_images/imageFile416.png)<br><br>(i)|
|---|


Consider the rotational equilibrium of the beam:

|![image 417](McKenzie - Examples in Structural Analysis_images/imageFile417.png)<br><br>(ii)|
|---|


Substituting into equation (i) gives ∴ VA=8.8 kN

###### The equation for the bending moment at x:

|![image 418](McKenzie - Examples in Structural Analysis_images/imageFile418.png)<br><br>Equation<br><br>(1)|
|---|


The equation for the slope (θ) at x:

|![image 419](McKenzie - Examples in Structural Analysis_images/imageFile419.png)<br><br>Equation<br><br>(2)|
|---|


The equation for the deflection (δ) at x:

|![image 420](McKenzie - Examples in Structural Analysis_images/imageFile420.png)<br><br>Equation<br><br>(3)|
|---|


where A and B are constants of integration related to the boundary conditions.

Note: It is common practice to use square brackets, i.e. [], to enclose the lever arms for the forces as shown. These brackets are integrated as a unit and during the calculation for slope and deflection; they are ignored if the contents are −ve, i.e. the position x being considered is to the left of the load associated with the bracket.

Boundary Conditions The boundary conditions are known values associated with the slope and/or deflection. In this problem, assuming no settlement occurs at the supports then the deflection is equal to zero at these positions, i.e.

|![image 421](McKenzie - Examples in Structural Analysis_images/imageFile421.png)|
|---|


Substituting for x and y in equation (3) ∴ B=0

|![image 422](McKenzie - Examples in Structural Analysis_images/imageFile422.png)|
|---|


The general equations for the slope and deflection at any point along the length of the beam are given by:

###### The equation for the slope at x:

|![image 423](McKenzie - Examples in Structural Analysis_images/imageFile423.png)<br><br>Equation<br><br>(4)|
|---|


The equation for the deflection at x:

|![image 424](McKenzie - Examples in Structural Analysis_images/imageFile424.png)<br><br>Equation<br><br>(5)|
|---|


e.g. the deflection at the mid-span point can be determined from equation (5) by substituting the value of x=5.0 and ignoring the [] when their contents are −ve, i.e.

|![image 425](McKenzie - Examples in Structural Analysis_images/imageFile425.png)|
|---|


![image 426](McKenzie - Examples in Structural Analysis_images/imageFile426.png)

The maximum deflection can be determined by calculating the value of x when the slope, i.e. equation (4) is equal to zero and substituting the calculated value of x into equation (5) as above.

In most simply supported spans the maximum deflection occurs near the mid-span point this can be used to estimate the value of x in equation (4) and hence eliminate some of the [] brackets, e.g. if the maximum deflection is assumed to occur at a position less than 6.0 m from the lefthand end the last two terms in the [] brackets need not be used to determine the position of zero slope. This assumption can be checked and if incorrect a subsequent calculation carried out including an additional bracket until the correct answer is found.

Assume ymaximum occurs between 5.0 m and 6.0 m from the left-hand end of the beam, then:

The equation for the slope at x is:

|![image 427](McKenzie - Examples in Structural Analysis_images/imageFile427.png)|
|---|


This equation reduces to:

|![image 428](McKenzie - Examples in Structural Analysis_images/imageFile428.png)|
|---|


since x was assumed to lie between 5.0 m and 6.0 m ignoring the two [] terms was correct. The maximum deflection can be found by substituting the value of x=5.2 m in equation (5) and ignoring the [] when their contents are −ve, i.e.

|![image 429](McKenzie - Examples in Structural Analysis_images/imageFile429.png)|
|---|


Note: There is no significant difference from the value calculated at mid-span.

###### 4.2.2 Example 4.5: Beam with Combined Point Loads and UDLs

A simply supported beam ABCD carries a uniformly distributed load of 3.0 kN/m between A and B, point loads of 4 kN and 6 kN at B and C respectively, and a uniformly distributed load of 5.0 kN/m between B and D as shown in Figure 4.22. Determine the position and magnitude of the maximum deflection.

![image 430](McKenzie - Examples in Structural Analysis_images/imageFile430.png)

- Figure 4.22 Consider the vertical equilibrium of the beam:

|![image 431](McKenzie - Examples in Structural Analysis_images/imageFile431.png)<br><br>(i)|
|---|


Consider the rotational equilibrium of the beam:

|![image 432](McKenzie - Examples in Structural Analysis_images/imageFile432.png)<br><br>(ii)|
|---|


Substituting into equation (i) gives ∴ VA= 16.33 kN

![image 433](McKenzie - Examples in Structural Analysis_images/imageFile433.png)

- Figure 4.23


In the case of a UDL when a term is written in the moment equation in square brackets, [], this effectively applies the load for the full length of the beam. For example, in Figure 4.23 the 3.0 kN/m load is assumed to apply from A to D and consequently only an additional 2.0 kN/m need be applied from position B onwards as shown in Figure 4.24.

![image 434](McKenzie - Examples in Structural Analysis_images/imageFile434.png)

###### Figure 4.24The equation for the bending moment at x is:

|![image 435](McKenzie - Examples in Structural Analysis_images/imageFile435.png)<br><br>Equation<br><br>(1)|
|---|


The equation for the slope at x is:

|![image 436](McKenzie - Examples in Structural Analysis_images/imageFile436.png)<br><br>Equation<br><br>(2)|
|---|


The equation for the deflection at x is:

|![image 437](McKenzie - Examples in Structural Analysis_images/imageFile437.png)<br><br>Equation<br><br>(3)|
|---|


where A and B are constants of integration related to the boundary conditions.

###### Boundary Conditions

In this problem, assuming no settlement occurs at the supports then the deflection is equal to zero at these positions, i.e.

|![image 438](McKenzie - Examples in Structural Analysis_images/imageFile438.png)|
|---|


Substituting for x and y in equation (3) ∴ B=0

|![image 439](McKenzie - Examples in Structural Analysis_images/imageFile439.png)|
|---|


The general equations for the slope and bending moment at any point along the length of the beam are given by:

###### The equation for the slope at x:

|![image 440](McKenzie - Examples in Structural Analysis_images/imageFile440.png)<br><br>Equation<br><br>(4)|
|---|


The equation for the deflection at x:

|![image 441](McKenzie - Examples in Structural Analysis_images/imageFile441.png)<br><br>Equation<br><br>(5)|
|---|


Assume ymaximum occurs between 2.0 m and 4.0 m from the left-hand end of the beam, then:

###### The equation for the slope at ‘x’ is:

|![image 442](McKenzie - Examples in Structural Analysis_images/imageFile442.png)|
|---|


This cubic can be solved by iteration.

Guess a value for x, e.g. 3.1 m

|(16.33×3.12)/2−(3.0×3.13)/6−(4.0×1.12)/2−(2.0×1.13)/6−58.98=1.73|
|---|


|>0|
|---|


The assumed value of 3.1 is slightly high, try x=3.05 m

|(16.33×3.052)/2−(3.0×3.053)/6−(4.0×1.052)/2−(2.0×1.053)/6– 58.98=0.20|
|---|


This value is close enough. x=3.05 m and since x was assumed to lie between 2.0 m and 4.0 m, ignoring the [x−4] term was correct.

The maximum deflection can be found by substituting the value of x=3.05 m in equation (5) and ignoring the [] when their contents are −ve, i.e.

|![image 443](McKenzie - Examples in Structural Analysis_images/imageFile443.png)|
|---|


#### 4.3 Equivalent Uniformly Distributed Load Method for the Deflection of Beams

In a simply supported beam, the maximum deflection induced by the applied loading always approximates the mid-span value if it is not equal to it. A number of standard frequently used load cases for which the elastic deformation is required are given in Appendix 2 in this text.

In many cases beams support complex load arrangements which do not lend themselves either to an individual load case or to a combination of the load cases given in Appendix 2. Provided that deflection is not the governing design criterion, a calculation which gives an approximate answer is usually adequate. The equivalent UDL method is a useful tool for estimating the deflection in a simply supported beam with a complex loading.

Consider a single-span, simply supported beam carrying a non-uniform loading which induces a maximum bending moment of M as shown in

- Figure 4.25.


![image 444](McKenzie - Examples in Structural Analysis_images/imageFile444.png)

- Figure 4.25


The equivalent UDL (we) which would induce the same magnitude of maximum bending moment (Note: the position may be different) on a simply supported span carrying a uniform loading can be determined from:

|![image 445](McKenzie - Examples in Structural Analysis_images/imageFile445.png)|
|---|


where we is the equivalent uniform distributed load.

The maximum deflection of the beam carrying the uniform loading will occur at the mid

|![image 446](McKenzie - Examples in Structural Analysis_images/imageFile446.png)|
|---|


Using this expression, the maximum deflection of the beam carrying the non-uniform loading can be estimated by substituting for the we term, i.e.

|![image 447](McKenzie - Examples in Structural Analysis_images/imageFile447.png)|
|---|


The maximum bending moments in Examples 5.4 and 5.5 are 32.8 kNm and 30.67 kNm respectively (the reader should check these answers).

###### Using the equivalent UDL method to estimate the maximum deflection in each case gives:

|![image 448](McKenzie - Examples in Structural Analysis_images/imageFile448.png)|
|---|


Note: The estimated deflection is more accurate for beams which are predominantly loaded with distributed loads.

###### 4.3.1 Problems: McCaulay’s and Equivalent UDL Methods for Deflection of Beams

A series of simply supported beams are indicated in Problems 4.11 to 4.15. Using the applied loading given in each case determine the maximum deflection. Assume all beams are uniform with Young’s Modulus of Elasticity=E and Second Moment of Area=I

![image 449](McKenzie - Examples in Structural Analysis_images/imageFile449.png)

###### Problem 4.11

![image 450](McKenzie - Examples in Structural Analysis_images/imageFile450.png)

###### Problem 4.12

![image 451](McKenzie - Examples in Structural Analysis_images/imageFile451.png)

###### Problem 4.13

![image 452](McKenzie - Examples in Structural Analysis_images/imageFile452.png)

###### Problem 4.14

![image 453](McKenzie - Examples in Structural Analysis_images/imageFile453.png)

###### Problem 4.15

###### 4.3.2 Solutions: McCaulay’s and Equivalent UDL Methods for Deflection of Beams

![image 454](McKenzie - Examples in Structural Analysis_images/imageFile454.png)

![image 455](McKenzie - Examples in Structural Analysis_images/imageFile455.png)

![image 456](McKenzie - Examples in Structural Analysis_images/imageFile456.png)

![image 457](McKenzie - Examples in Structural Analysis_images/imageFile457.png)

![image 458](McKenzie - Examples in Structural Analysis_images/imageFile458.png)

![image 459](McKenzie - Examples in Structural Analysis_images/imageFile459.png)

![image 460](McKenzie - Examples in Structural Analysis_images/imageFile460.png)

![image 461](McKenzie - Examples in Structural Analysis_images/imageFile461.png)

![image 462](McKenzie - Examples in Structural Analysis_images/imageFile462.png)

![image 463](McKenzie - Examples in Structural Analysis_images/imageFile463.png)

#### 4.4 The Principle of Superposition

The Principle of Superposition can be stated as follows:

‘If the displacements at all points in a structure are proportional to the forces causing them, the effect produced on that structure by a number of forces applied simultaneously, is the same as the sum of the effects when each of the forces is applied individually.’

This applies to any structure made from a material which has a linear loaddisplacement relationship. Consider the simply-supported beam ABCD shown in Figure 4.26 which carries two point loads at B and C as indicated.

![image 464](McKenzie - Examples in Structural Analysis_images/imageFile464.png)

- Figure 4.26

![image 465](McKenzie - Examples in Structural Analysis_images/imageFile465.png)

- Figure 4.27


Note: the maximum deflection does not necessarily occur at the mid-span point.

###### When the loads are considered individually the corresponding functions are as indicated in Figure 4.28.

![image 466](McKenzie - Examples in Structural Analysis_images/imageFile466.png)

- Figure 4.28 It is evident from Figure 4.28 that:


|VA=(12.0+7.5)=19.5 kN; VD=(4.0+12.5)=16.5 kN|
|---|


![image 467](McKenzie - Examples in Structural Analysis_images/imageFile467.png)

|![image 468](McKenzie - Examples in Structural Analysis_images/imageFile468.png)|
|---|


This Principle can be used very effectively when calculating the deflection of beams, (particularly non-uniform beams), as used in the Examples and Problems given in Section 4.5. Examples 5.6 to 5.10 illustrate the application of the Principle.

###### 4.4.1 Example 4.6: Superposition—Beam 1

![image 469](McKenzie - Examples in Structural Analysis_images/imageFile469.png)

- Figure 4.29

Using superposition this beam can be represented as the sum of the two load cases shown in Figure 4.30.

![image 470](McKenzie - Examples in Structural Analysis_images/imageFile470.png)

- Figure 4.30


|![image 471](McKenzie - Examples in Structural Analysis_images/imageFile471.png)|
|---|


###### 4.4.2 Example 4.7: Superposition—Beam 2

![image 472](McKenzie - Examples in Structural Analysis_images/imageFile472.png)

- Figure 4.31 Using superposition this beam can be represented as the sum of:

![image 473](McKenzie - Examples in Structural Analysis_images/imageFile473.png)

- Figure 4.32


![image 474](McKenzie - Examples in Structural Analysis_images/imageFile474.png)

###### 4.4.3 Example 4.8: Superposition—Beam 3

![image 475](McKenzie - Examples in Structural Analysis_images/imageFile475.png)

- Figure 4.33 Using superposition this beam can be represented as the sum of:

![image 476](McKenzie - Examples in Structural Analysis_images/imageFile476.png)

- Figure 4.34


VA=(24.0+12.0+5.0–2.5)=38.5 kN;

|![image 477](McKenzie - Examples in Structural Analysis_images/imageFile477.png)|
|---|


###### 4.4.4 Example 4.9: Superposition-Beam 4

![image 478](McKenzie - Examples in Structural Analysis_images/imageFile478.png)

- Figure 4.35 Using superposition this beam can be represented as the sum of:

![image 479](McKenzie - Examples in Structural Analysis_images/imageFile479.png)

- Figure 4.36


![image 480](McKenzie - Examples in Structural Analysis_images/imageFile480.png)

###### 4.4.5 Example 4.10: Superposition -Beam 5

![image 481](McKenzie - Examples in Structural Analysis_images/imageFile481.png)

- Figure 4.37 Using superposition this beam can be represented as the sum of:

![image 482](McKenzie - Examples in Structural Analysis_images/imageFile482.png)

- Figure 4.38


|![image 483](McKenzie - Examples in Structural Analysis_images/imageFile483.png)|
|---|


#### 4.5 Unit Load Method for Deflection of Beams

In Chapter 3, Section 3.5 the deflection of pin-jointed frames was calculated using the concept of strain energy and Castigliano’s 1st Theorem. This approach can also be applied to structures such as beams and rigid-jointed frames in which the members are primarily subject to bending effects.

In the case of pin-jointed frames the applied loads induce axial load effects and subsequent changes in the lengths of the members. In the case of beams and rigid-jointed frames, the corresponding applied loads induce bending moments and subsequent changes in the slope of the member.

Pin-jointed frames comprise discrete members with individual axial loads which are constant along the length of the member. In beams the bending moment generally varies along the length and consequently the summation of the bending effect for the entire beam is the integral of a function involving the bending moment.

4.5.1 Strain Energy (Bending Load Effects)

A simply-supported beam subjected to a single point load is shown in Figure 4.39. An incremental length of beam dx, over which the bending moment can be considered to be constant, is indicated a distance ‘x’ from the left-hand support.

![image 484](McKenzie - Examples in Structural Analysis_images/imageFile484.png)

###### Figure 4.39

![image 485](McKenzie - Examples in Structural Analysis_images/imageFile485.png)

From ‘simple bending theory’

where R is the radius of curvature and 1/R is the curvature of the beam, i.e. the rate of

![image 486](McKenzie - Examples in Structural Analysis_images/imageFile486.png)

change of slope.

Assuming the moment is applied to the beam gradually, the relationship between the moment and the change in slope is as shown in Figure 4.40.

![image 487](McKenzie - Examples in Structural Analysis_images/imageFile487.png)

###### Figure 4.40Differentiating the expression for strain energy with respect to x gives:

|![image 488](McKenzie - Examples in Structural Analysis_images/imageFile488.png)|
|---|


Using Castigliano’s 1st Theorem relating to strain energy and structural deformation:

|![image 489](McKenzie - Examples in Structural Analysis_images/imageFile489.png)|
|---|


where:

|U is the total strain energy of the structure due to the applied load system, W is the force or moment acting at the point where the displacement or<br><br>rotation is required, Δ is the linear displacement or rotation in the direction of the line of action of W.<br><br>|
|---|


Consider the simply-supported beam ABCD shown in Figure 4.41 in which it is required to determine the mid-span deflection at C due to an applied load P at position B.

![image 490](McKenzie - Examples in Structural Analysis_images/imageFile490.png)

###### Figure 4.41

Step 1:

The applied load bending moment diagram is determined as shown in Figure 4.42

![image 491](McKenzie - Examples in Structural Analysis_images/imageFile491.png)

- Figure 4.42

Step 2:

The applied load system is removed from the structure and an imaginary Unit load is applied at the position and in the direction of the required deflection, i.e. a vertical load equal to 1.0 at point C. The resulting bending moment diagram due to the unit load is indicated in Figure 4.43

![image 492](McKenzie - Examples in Structural Analysis_images/imageFile492.png)

- Figure 4.43


If both the Step 1 and the Step 2 load systems are considered to act simultaneously, then by superposition the bending moment in the beam is given by:

|![image 493](McKenzie - Examples in Structural Analysis_images/imageFile493.png)|
|---|


where:

|M is the bending moment due to the applied load system m is the bending moment due to the applied imaginary Unit load applied<br><br>at C β is a multiplying factor to reflect the value of the load applied at C, (since the unit load is an imaginary force the value of β=zero and is<br><br>|
|---|


###### used here as a mathematical convenience.)

The strain energy in the structure is equal to the total energy stored along the full length of the beam:

|![image 494](McKenzie - Examples in Structural Analysis_images/imageFile494.png)|
|---|


Using Castigliano’s 1st Theorem the deflection of point C is given by:

|![image 495](McKenzie - Examples in Structural Analysis_images/imageFile495.png)|
|---|


Since β=zero the vertical deflection at B (Δβ) is given by:

|![image 496](McKenzie - Examples in Structural Analysis_images/imageFile496.png)|
|---|


i.e. the deflection at any point in a beam can be determined from:

|![image 497](McKenzie - Examples in Structural Analysis_images/imageFile497.png)|
|---|


where:

###### δ is the displacement of the point of application of any load, along the line of action of that load,

M is the bending in the member due to the externally applied load system, m is the bending moment in member due to a unit load acting at the

position of, and in the direction of the desired displacement, I is the second-moment of area of the member, E is the modulus of elasticity of the material for the member.

###### 4.5.2 Example 4.11: Deflection and Slope of a Uniform Cantilever

A uniform cantilever beam is shown in Figure 4.44 in which a 20 kN is applied at B as indicated. Determine the magnitude and direction of the deflection and slope at B.

![image 498](McKenzie - Examples in Structural Analysis_images/imageFile498.png)

- Figure 4.44

The bending moment diagrams for the applied load, a unit point load at B and a unit moment at B are shown in Figure 4.45.

![image 499](McKenzie - Examples in Structural Analysis_images/imageFile499.png)

- Figure 4.45


Solution:

|![image 500](McKenzie - Examples in Structural Analysis_images/imageFile500.png)|
|---|


The bending moment at position ‘x’ due to the applied vertical load M=−20.0x

###### The bending moment at position ‘x’ due to the applied unit vertical load m=−x

|![image 501](McKenzie - Examples in Structural Analysis_images/imageFile501.png)|
|---|


The bending moment at position ‘x’ due to the applied unit moment at B m=−1.0

|![image 502](McKenzie - Examples in Structural Analysis_images/imageFile502.png)|
|---|


![image 503](McKenzie - Examples in Structural Analysis_images/imageFile503.png)

The product integral can be also be calculated as:

(Area of the applied load bending moment diagram×the ordinate on the unit load bending moment diagram corresponding to the position of the centroid of the applied load bending moment diagram), e.g.

To determine the vertical deflection: Area of the applied load bending moment diagram A=(0.5×4.0×80.0)=160 kNm2

- Ordinate at the position of the centroid y1=2.67 m


|![image 504](McKenzie - Examples in Structural Analysis_images/imageFile504.png)|
|---|


To determine the slope:

Area of the applied load bending moment diagram A=(0.5×4.0×80.0)=160 kNm2

- Ordinate at the position of the centroid y2=1.0


|![image 505](McKenzie - Examples in Structural Analysis_images/imageFile505.png)|
|---|


###### 4.5.3 Example 4.12: Deflection and Slope of a Non-Uniform Cantilever

Consider the same problem as in Example 4.11 in which the cross-section of the cantilever has a variable EI value as indicated in Figure 4.46.

![image 506](McKenzie - Examples in Structural Analysis_images/imageFile506.png)

###### Figure 4.46

The bending moment diagrams for the applied load, a unit point load at C and a unit moment at C are shown in Figure 4.47.

![image 507](McKenzie - Examples in Structural Analysis_images/imageFile507.png)

###### Figure 4.47Solution:

|![image 508](McKenzie - Examples in Structural Analysis_images/imageFile508.png)|
|---|


In this case since (Mm/EI) is not a continuous function the product integral must be evaluated between each of the discontinuities, i.e. C to B and B to A.

|![image 509](McKenzie - Examples in Structural Analysis_images/imageFile509.png)|
|---|


![image 510](McKenzie - Examples in Structural Analysis_images/imageFile510.png)

Consider the section from C to B:

|![image 511](McKenzie - Examples in Structural Analysis_images/imageFile511.png)|
|---|


- Consider the section from B to A:

![image 512](McKenzie - Examples in Structural Analysis_images/imageFile512.png)

|![image 513](McKenzie - Examples in Structural Analysis_images/imageFile513.png)|
|---|


Similarly to determine the slope:

|![image 514](McKenzie - Examples in Structural Analysis_images/imageFile514.png)|
|---|


- Consider the section from C to B:


![image 515](McKenzie - Examples in Structural Analysis_images/imageFile515.png)

|![image 516](McKenzie - Examples in Structural Analysis_images/imageFile516.png)|
|---|


![image 517](McKenzie - Examples in Structural Analysis_images/imageFile517.png)

Consider the section from B to A:

|![image 518](McKenzie - Examples in Structural Analysis_images/imageFile518.png)|
|---|


Alternatively, the applied bending moment diagram can be considered as a the sum of the areas created by the discontinuity. (In most cases this will result in a number of recognised shapes e.g. triangular, rectangular or parabolic, in which the areas and the position of the centroid can be easily calculated).

###### The deflection can then be determined by summing the products (area×ordinate) for each of the shapes.

|![image 519](McKenzie - Examples in Structural Analysis_images/imageFile519.png)|
|---|


The slope can then be determined by summing the products (area×ordinate) for each of the shapes.

|![image 520](McKenzie - Examples in Structural Analysis_images/imageFile520.png)|
|---|


###### 4.5.4 Example 4.13: Deflection and Slope of a Linearly VaryingCantilever

Consider the same problem as in Example 4.11 in which the cross-section of the cantilever has an I which varies linearly from I at the free end to 2I at the fixed support at A as indicated in Figure 4.48. Determine the vertical displacement and the slope at point B for the loading indicated.

![image 521](McKenzie - Examples in Structural Analysis_images/imageFile521.png)

The value of I at position ‘x’ along the beam is given by: I+I(x/L)=I(L+x)/L.

In this case since the I term is dependent on x it cannot be considered outside the integral as a constant. The displacement must be determined using integration and cannot be calculated using the sum of the (area×ordinate) as in Examples 5.11 and 5.12.

![image 522](McKenzie - Examples in Structural Analysis_images/imageFile522.png)

- Figure 4.49 Solution:


The bending moment at position ‘x’ due to the applied vertical load M=−20.0x

The bending moment at position ‘x’ due to the applied unit vertical load m=−x

|![image 523](McKenzie - Examples in Structural Analysis_images/imageFile523.png)|
|---|


The bending moment at position ‘x’ due to the applied unit moment at B m=−1.0

|![image 524](McKenzie - Examples in Structural Analysis_images/imageFile524.png)|
|---|


###### 4.5.5 Example 4.14: Deflection of a Non-Uniform, Simply-SupportedBeam

A non-uniform, single-span beam ABCD is simply-supported at A and D and carries loading as indicated in Figure 4.50. Determine the vertical displacement at point B.

![image 525](McKenzie - Examples in Structural Analysis_images/imageFile525.png)

The bending moment diagrams for the applied load, a unit point load at B are shown in Figure 4.51.

The beam loading can be considered as the superposition of a number of load cases each of which produces a bending moment diagram with a standard shape. Since there are discontinuities in the bending moment diagrams the product integrals should be carried out for the three regions A to B, D to C and C to B.

![image 526](McKenzie - Examples in Structural Analysis_images/imageFile526.png)

- Figure 4.51 Solution:


It is convenient in this problem to change the position of the origin from which ‘x’ is measured for the different regions A–B, D–C and C–B as shown in Figure 4.51.

|![image 527](McKenzie - Examples in Structural Analysis_images/imageFile527.png)|
|---|


![image 528](McKenzie - Examples in Structural Analysis_images/imageFile528.png)

Consider the section from A to B:

|![image 529](McKenzie - Examples in Structural Analysis_images/imageFile529.png)|
|---|


![image 530](McKenzie - Examples in Structural Analysis_images/imageFile530.png)

Consider the section from D to C:

|![image 531](McKenzie - Examples in Structural Analysis_images/imageFile531.png)|
|---|


![image 532](McKenzie - Examples in Structural Analysis_images/imageFile532.png)

Consider the section from C to B:

|![image 533](McKenzie - Examples in Structural Analysis_images/imageFile533.png)|
|---|


Alternatively: considering Σ (areas×ordinates)

![image 534](McKenzie - Examples in Structural Analysis_images/imageFile534.png)

###### Figure 5.52

|![image 535](McKenzie - Examples in Structural Analysis_images/imageFile535.png)|
|---|


###### 4.5.6 Example 4.15: Deflection of a Frame and Beam Structure

A uniform beam BCD is tied at B, supported on a roller at C and carries a vertical load at D as indicated in Figure 4.53. Using the data given determine the vertical displacement at point D.

![image 536](McKenzie - Examples in Structural Analysis_images/imageFile536.png)

- Figure 4.53 Solution:


Consider the rotational equilibrium of the beam:

|![image 537](McKenzie - Examples in Structural Analysis_images/imageFile537.png)|
|---|


Consider the vertical equilibrium of the structure:

|![image 538](McKenzie - Examples in Structural Analysis_images/imageFile538.png)|
|---|


Since the structure comprises both an axially loaded member and a flexural member the deflection at D is given by:

|![image 539](McKenzie - Examples in Structural Analysis_images/imageFile539.png)|
|---|


![image 540](McKenzie - Examples in Structural Analysis_images/imageFile540.png)

###### Figure 4.54

|![image 541](McKenzie - Examples in Structural Analysis_images/imageFile541.png)|
|---|


![image 542](McKenzie - Examples in Structural Analysis_images/imageFile542.png)

Consider the section from B to C:

|![image 543](McKenzie - Examples in Structural Analysis_images/imageFile543.png)|
|---|


![image 544](McKenzie - Examples in Structural Analysis_images/imageFile544.png)

Consider the section from D to C:

|![image 545](McKenzie - Examples in Structural Analysis_images/imageFile545.png)|
|---|


In the previous examples the product integrals were also determined using:

(the area of the applied bending moment diagram×ordinate on the unit load bending moment diagram).

In Table 4.1 coefficients are given to enable the rapid evaluation of product integrals for standard cases along lengths of beam where the EI value is constant.

|![image 546](McKenzie - Examples in Structural Analysis_images/imageFile546.png)<br><br>Table 4.1<br><br>|
|---|


Consider the contribution from the beam BCD to the vertical deflection at D in Example 4.15.

|![image 547](McKenzie - Examples in Structural Analysis_images/imageFile547.png)|
|---|


###### 4.5.7 Example 4.16: Deflection of a Uniform Cantilever usingCoefficients

A uniform cantilever beam is shown in Figure 4.55 in which a uniformly distributed load and a vertical load is applied as indicated. Using the coefficients in Table 4.1 determine the magnitude and direction of the deflection at D.

![image 548](McKenzie - Examples in Structural Analysis_images/imageFile548.png)

- Figure 4.55

The bending moment diagrams for the applied loads and a unit point load at B are shown in Figure 4.56.

![image 549](McKenzie - Examples in Structural Analysis_images/imageFile549.png)

- Figure 4.56 Solution:


Consider the unit load bending moment diagrams for both applied loads as the sum of rectangular and a triangular area as shown.

![image 550](McKenzie - Examples in Structural Analysis_images/imageFile550.png)

###### 4.5.8 Problems: Unit Load Method for Deflection of Beams/Frames

A series of statically-determinate beams/frames are indicated in Problems 4.16 to 4.23. Using the applied loading given in each case determine the deflections indicated. The relative values of Young’s Modulus of Elasticity (E), Second Moment of Area (I) and Cross-sectional area (A) are given in each case.

![image 551](McKenzie - Examples in Structural Analysis_images/imageFile551.png)

###### Problem 4.16

![image 552](McKenzie - Examples in Structural Analysis_images/imageFile552.png)

###### Problem 4.17

![image 553](McKenzie - Examples in Structural Analysis_images/imageFile553.png)

###### Problem 4.18

![image 554](McKenzie - Examples in Structural Analysis_images/imageFile554.png)

###### Problem 4.19

![image 555](McKenzie - Examples in Structural Analysis_images/imageFile555.png)

###### Problem 4.20

![image 556](McKenzie - Examples in Structural Analysis_images/imageFile556.png)

###### Problem 4.21

![image 557](McKenzie - Examples in Structural Analysis_images/imageFile557.png)

###### Problem 4.22

![image 558](McKenzie - Examples in Structural Analysis_images/imageFile558.png)

###### Problem 4.23

###### 4.5.9 Solutions: Unit Load Method for Deflection of Beams/Frames

![image 559](McKenzie - Examples in Structural Analysis_images/imageFile559.png)

![image 560](McKenzie - Examples in Structural Analysis_images/imageFile560.png)

![image 561](McKenzie - Examples in Structural Analysis_images/imageFile561.png)

![image 562](McKenzie - Examples in Structural Analysis_images/imageFile562.png)

![image 563](McKenzie - Examples in Structural Analysis_images/imageFile563.png)

![image 564](McKenzie - Examples in Structural Analysis_images/imageFile564.png)

![image 565](McKenzie - Examples in Structural Analysis_images/imageFile565.png)

![image 566](McKenzie - Examples in Structural Analysis_images/imageFile566.png)

![image 567](McKenzie - Examples in Structural Analysis_images/imageFile567.png)

![image 568](McKenzie - Examples in Structural Analysis_images/imageFile568.png)

![image 569](McKenzie - Examples in Structural Analysis_images/imageFile569.png)

![image 570](McKenzie - Examples in Structural Analysis_images/imageFile570.png)

![image 571](McKenzie - Examples in Structural Analysis_images/imageFile571.png)

![image 572](McKenzie - Examples in Structural Analysis_images/imageFile572.png)

![image 573](McKenzie - Examples in Structural Analysis_images/imageFile573.png)

![image 574](McKenzie - Examples in Structural Analysis_images/imageFile574.png)

![image 575](McKenzie - Examples in Structural Analysis_images/imageFile575.png)

![image 576](McKenzie - Examples in Structural Analysis_images/imageFile576.png)

![image 577](McKenzie - Examples in Structural Analysis_images/imageFile577.png)

![image 578](McKenzie - Examples in Structural Analysis_images/imageFile578.png)

![image 579](McKenzie - Examples in Structural Analysis_images/imageFile579.png)

![image 580](McKenzie - Examples in Structural Analysis_images/imageFile580.png)

![image 581](McKenzie - Examples in Structural Analysis_images/imageFile581.png)

![image 582](McKenzie - Examples in Structural Analysis_images/imageFile582.png)

![image 583](McKenzie - Examples in Structural Analysis_images/imageFile583.png)

![image 584](McKenzie - Examples in Structural Analysis_images/imageFile584.png)

![image 585](McKenzie - Examples in Structural Analysis_images/imageFile585.png)

#### 4.6 Statically Indeterminate Beams

In many instances multi-span beams are used in design, and consequently it is necessary to consider the effects of the continuity on the support reactions and member forces. Such structures are indeterminate (see Chapter 1) and there are more unknown variables than

can be solved using only the three equations of equilibrium. A few examples of such beams are shown in Figure 4.57(a) to (d).

![image 586](McKenzie - Examples in Structural Analysis_images/imageFile586.png)

- Figure 4.57(a)


![image 587](McKenzie - Examples in Structural Analysis_images/imageFile587.png)

- Figure 4.57(b)

![image 588](McKenzie - Examples in Structural Analysis_images/imageFile588.png)

- Figure 4.57(c)

![image 589](McKenzie - Examples in Structural Analysis_images/imageFile589.png)

- Figure 4.57(d)


A number of analysis methods are available for determining the support reactions, and member forces in indeterminate beams. In the case of singly-redundant beams the ‘unitload method’ can be conveniently used to analyse the structure. In multi-redundant structures the method of ‘moment distribution’ is a particularly useful hand-method of analysis. These methods are considered in Sections 4.6.1 and 4.6.2 respectively.

###### 4.6.1 Unit Load Method for Singly-Redundant Beams

Using the method of analysis illustrated in Section 4.5 and considering the compatibility of displacements, member forces in singly-redundant beams can be determined as shown in Examples 4.17 and 4.18 and in Problems 4.24 to 4.27.

###### 4.6.2 Example 4.17: Singly-Redundant Beam 1

A propped cantilever ABC is fixed at A, supported on a roller at C and carries a mid-span point load of 15 kN as shown in Figure 4.58,

|(i) determine the value of the support reactions and<br><br>(ii) sketch the shear force and bending moment diagram.<br><br><br>|
|---|


![image 590](McKenzie - Examples in Structural Analysis_images/imageFile590.png)

###### Figure 4.58

The degree-of-indeterminacy ID=[(3m+r)]−3n=[(3×1)+4]−(3×2)=1

Assume that the reaction at C is the redundant reaction and consider the original beam to be the superposition of two beams as indicated in Figures 4.59(a) and (b). The beam in Figure 4.59(b) can be represented as shown in Figure 4.60. (Note: HA=zero)

![image 591](McKenzie - Examples in Structural Analysis_images/imageFile591.png)

###### Figure 4.59

![image 592](McKenzie - Examples in Structural Analysis_images/imageFile592.png)

###### Figure 4.60

To maintain compatibility at the roller support, i.e. no resultant vertical displacement, the deformation of point C in Figure 4.59(a) must be equal and opposite to that in Figure 4.59(b) as shown in Figure 4.61.

![image 593](McKenzie - Examples in Structural Analysis_images/imageFile593.png)

###### Figure 4.61

(δ′ due to the applied load)+(δ″ due to the unit load)×VC=0

|![image 594](McKenzie - Examples in Structural Analysis_images/imageFile594.png)|
|---|


The product integrals can be evaluated as before in Section 4.5, e.g. using the coefficients in Table 4.1.

Solution: The bending moment diagrams for the applied loads and a unit point load at B are shown in Figure 4.62.

![image 595](McKenzie - Examples in Structural Analysis_images/imageFile595.png)

###### Figure 4.62

Using the coefficients given in Table 4.1:

|![image 596](McKenzie - Examples in Structural Analysis_images/imageFile596.png)|
|---|


![image 597](McKenzie - Examples in Structural Analysis_images/imageFile597.png)

- Figure 4.63

4.6.3 Example 4.18: Singly-Redundant Beam 2

A non-uniform, two-span beam ABCD is simply supported at A, B and D as shown in

- Figure 4.64. The beam carries a uniformly distributed load on span AB and a point at the mid-span point of BCD. Using the data given:


| |
|---|


|(i) determine the value of the support reactions,<br><br>(ii) sketch the shear force and bending moment diagrams.<br><br>|
|---|


![image 598](McKenzie - Examples in Structural Analysis_images/imageFile598.png)

- Figure 4.64 Solution:


Assume that the reaction at B is the redundant reaction. The bending moment diagrams for the applied loads and a unit point load at B are shown in Figure 4.65.

![image 599](McKenzie - Examples in Structural Analysis_images/imageFile599.png)

|![image 600](McKenzie - Examples in Structural Analysis_images/imageFile600.png)|
|---|


![image 601](McKenzie - Examples in Structural Analysis_images/imageFile601.png)

###### 4.6.4 Problems: Unit Load Method for Singly-Redundant Beams

A series of singly-redundant beams are indicated in Problems 4.24 to 4.27. Using the applied loading given in each case:

|i) determine the support reactions,<br><br>ii) sketch the shear force diagram and<br><br>iii) sketch the bending moment diagram.<br><br><br>|
|---|


![image 602](McKenzie - Examples in Structural Analysis_images/imageFile602.png)

###### Problem 4.24

![image 603](McKenzie - Examples in Structural Analysis_images/imageFile603.png)

###### Problem 4.25

![image 604](McKenzie - Examples in Structural Analysis_images/imageFile604.png)

###### Problem 4.26

![image 605](McKenzie - Examples in Structural Analysis_images/imageFile605.png)

- Problem 4.27


###### 4.6.5 Solutions: Unit Load Method for Singly-Redundant Beams

![image 606](McKenzie - Examples in Structural Analysis_images/imageFile606.png)

![image 607](McKenzie - Examples in Structural Analysis_images/imageFile607.png)

![image 608](McKenzie - Examples in Structural Analysis_images/imageFile608.png)

![image 609](McKenzie - Examples in Structural Analysis_images/imageFile609.png)

![image 610](McKenzie - Examples in Structural Analysis_images/imageFile610.png)

![image 611](McKenzie - Examples in Structural Analysis_images/imageFile611.png)

![image 612](McKenzie - Examples in Structural Analysis_images/imageFile612.png)

![image 613](McKenzie - Examples in Structural Analysis_images/imageFile613.png)

![image 614](McKenzie - Examples in Structural Analysis_images/imageFile614.png)

![image 615](McKenzie - Examples in Structural Analysis_images/imageFile615.png)

#### 4.7 Moment Distribution Method for Multi-Redundant Beams

This section deals with continuous beams and propped cantilevers. An American engineer, Professor Hardy Cross, developed a very simple, elegant and practical method of analysis for such structures called Moment Distribution. This technique is one of developing successive approximations and is based on several basic concepts of structural behaviour which are illustrated in Sections 4.6.1 to 4.6.10.

4.7.1 Bending (Rotational) Stiffness

A fundamental relationship which exists in the elastic behaviour of structures and structural elements is that between an applied force system and the displacements which are induced by that system, i.e.

|![image 616](McKenzie - Examples in Structural Analysis_images/imageFile616.png)|
|---|


where:

|P is the applied force, k is the stiffness, δ is the displacement.<br><br>|
|---|


A definition of stiffness can be derived from this equation by rearranging it such that:

k=P/δ when δ=1.0 (i.e. unit displacement) the stiffness is: ‘the force necessary to maintain a UNIT displacement, all other displacements being equal to zero.’

The displacement can be a shear displacement, an axial displacement, a bending (rotational) displacement or a torsional displacement, each in turn producing the shear, axial, bending or torsional stiffness.

When considering beam elements in continuous structures using the moment distribution method of analysis, the bending stiffness is the principal characteristic which influences behaviour.

Consider the beam element AB shown in Figure 4.67 which is subject to a UNIT rotation at end A and is fixed at end B as indicated.

![image 617](McKenzie - Examples in Structural Analysis_images/imageFile617.png)

- Figure 4.67

The force (MA) necessary to maintain this displacement can be shown to be equal to (4EI)/L (see Chapter 7, Section 7.2.2). From the definition of stiffness given previously, the bending stiffness of the beam is equal to (Force/1.0), therefore k=(4EI)/L. This is known as the absolute bending stiffness of the element. Since most elements in continuous structures are made from the same material, the value of Young’s Modulus (E) is constant throughout and 4E in the stiffness term is also a constant. This constant is normally ignored, to give k=I/L which is known as the relative bending stiffness of the element. It is this value of stiffness which is normally used in the method of Moment Distribution. It is evident from Figure 4.67 that when the beam element deforms due to the applied rotation at end A, an additional moment (MB) is also transferred by the element to the remote end if it has zero slope (i.e. is fixed) The moment MB is known as the carry-over moment.

4.7.2 Carry-Over Moment

Using the same analysis as that to determine MA, it can be shown that MB=(2EI)/L, i.e. (½×MA). It can therefore be stated that ‘if a moment is applied to one end of a beam then a moment of the same sense and equal to half of its value will be transferred to the remote end provided that it is fixed.’

If the remote end is ‘pinned’, then the beam is less stiff and there is no carry-over moment.

4.7.3 Pinned End

Consider the beam shown in Figure 4.68 in which a unit rotation is imposed at end A as before but the remote end B is pinned.

![image 618](McKenzie - Examples in Structural Analysis_images/imageFile618.png)

- Figure 4.68


The force (MA) necessary to maintain this displacement can be shown (e.g. using McCaulay’s Method) to be equal to (3EI)/L, which represents the reduced absolute stiffness of a pin-ended beam. It can therefore be stated that ‘the stiffness of a pin-ended beam is equal to ¾×the stiffness of a fixed-end beam.’ In addition it can be shown that there is no carry-over moment to the remote end. These two cases are summarised in Figure 4.69.

![image 619](McKenzie - Examples in Structural Analysis_images/imageFile619.png)

###### Figure 4.69

4.7.4 Free and Fixed Bending Moments

When a beam is free to rotate at both ends as shown in Figures 4.70(a) and (b) such that no bending moment can develop at the supports, then the bending moment diagram resulting from the applied loads on the beam is known as the Free Bending Moment Diagram.

![image 620](McKenzie - Examples in Structural Analysis_images/imageFile620.png)

###### Figure 4.70—Free Bending Moment Diagrams

When a beam is fixed at the ends (encastre) such that it cannot rotate, i.e. zero slope at the supports, as shown in Figure 4.71, then bending moments are induced at the supports and are called Fixed-End Moments. The bending moment diagram associated only with the fixed-end moments is called the Fixed Bending Moment Diagram.

![image 621](McKenzie - Examples in Structural Analysis_images/imageFile621.png)

###### Figure 4.71—Fixed Bending Moment Diagram

Using the principle of superposition, this beam can be considered in two parts in order to evaluate the support reactions and the Final bending moment diagram:

|(i) The fixed-reactions (moments and forces) at the supports|
|---|


###### Figure 4.72

![image 622](McKenzie - Examples in Structural Analysis_images/imageFile622.png)

(ii) The free reactions at the supports and the bending moments throughout the length due to the applied load, assuming the supports to be pinned

![image 623](McKenzie - Examples in Structural Analysis_images/imageFile623.png)

###### Figure 4.73Combining (i)+(ii) gives the final bending moment diagram as shown in Figure 4.74:

![image 624](McKenzie - Examples in Structural Analysis_images/imageFile624.png)

|![image 625](McKenzie - Examples in Structural Analysis_images/imageFile625.png)<br><br>Figure 4.74<br><br>The values of MA and MB for the most commonly applied load cases are given in Appendix 2. These are standard Fixed-End Moments relating to single-span encastre beams and are used extensively in structural analysis.<br><br>4.7.5 Example 4.19: Single-span Encastre Beam<br><br>Determine the support reactions and draw the bending moment diagram for the encastre beam loaded as shown in Figure 4.75.<br><br>![image 626](McKenzie - Examples in Structural Analysis_images/imageFile626.png)<br><br>Figure 4.75 Solution:<br><br><br>Consider the beam in two parts. (i) Fixed Support Reactions The values of the fixed-end moments are given in Appendix 2.<br><br>|
|---|


![image 627](McKenzie - Examples in Structural Analysis_images/imageFile627.png)

![image 628](McKenzie - Examples in Structural Analysis_images/imageFile628.png)

Consider the rotational equilibrium of the beam:

![image 629](McKenzie - Examples in Structural Analysis_images/imageFile629.png)

Equation

(1)

Consider the vertical equilibrium of the beam:

![image 630](McKenzie - Examples in Structural Analysis_images/imageFile630.png)

Equation

(2)

![image 631](McKenzie - Examples in Structural Analysis_images/imageFile631.png)

|Consider the rotational equilibrium of the beam:<br><br>|
|---|
|![image 632](McKenzie - Examples in Structural Analysis_images/imageFile632.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 633](McKenzie - Examples in Structural Analysis_images/imageFile633.png)<br><br>Equation<br><br>(2)|
|Bending Moment under the point load =(+13.33×2.0)=+26.67 kNm (This induces tension in the bottom of the beam)<br><br>The final vertical support reactions are given by (i)+(ii):<br><br>![image 634](McKenzie - Examples in Structural Analysis_images/imageFile634.png)<br><br>Check the vertical equilibrium: Total vertical force =+14.81+5.19=+20 kN<br><br>![image 635](McKenzie - Examples in Structural Analysis_images/imageFile635.png)<br><br>![image 636](McKenzie - Examples in Structural Analysis_images/imageFile636.png)<br><br>Figure 4.76<br><br>|


Note the similarity between the shape of the bending moment diagram and the final deflected shape as shown in Figure 4.77.

![image 637](McKenzie - Examples in Structural Analysis_images/imageFile637.png)

###### Figure 4.77

4.7.6 Propped Cantilevers

The fixed-end moment for propped cantilevers (i.e. one end fixed and the other end simply supported) can be derived from the standard values given for encastre beams as follows. Consider the propped cantilever shown in Figure 4.78, which supports a uniformly distributed load as indicated.

![image 638](McKenzie - Examples in Structural Analysis_images/imageFile638.png)

###### Figure 4.78The structure can be considered to be the superposition of an encastre beam with theaddition of an equal and opposite moment to MB applied at B to ensure that the final

moment at this support is equal to zero, as indicated in Figure 4.79.

![image 639](McKenzie - Examples in Structural Analysis_images/imageFile639.png)

###### Figure 4.79

###### 4.7.7 Example 4.20: Propped Cantilever

Determine the support reactions and draw the bending moment diagram for the propped cantilever shown in Figure 4.80.

![image 640](McKenzie - Examples in Structural Analysis_images/imageFile640.png)

- Figure 4.80 Solution


Fixed-End Moment for Propped Cantilever: Consider the beam fixed at both supports. The values of the fixed-end moments for encastre beams are given in Appendix 2.

![image 641](McKenzie - Examples in Structural Analysis_images/imageFile641.png)

The moment MB must be cancelled out by applying an equal and opposite moment at B which in turn produces a carry-over moment equal to-(0.5×MB) at support A.

![image 642](McKenzie - Examples in Structural Analysis_images/imageFile642.png)

(i) Fixed Support Reactions

![image 643](McKenzie - Examples in Structural Analysis_images/imageFile643.png)

Consider the rotational equilibrium of the beam:

![image 644](McKenzie - Examples in Structural Analysis_images/imageFile644.png)

Equation

(1)

Consider the vertical equilibrium of the beam:

![image 645](McKenzie - Examples in Structural Analysis_images/imageFile645.png)

Equation

(2)

![image 646](McKenzie - Examples in Structural Analysis_images/imageFile646.png)

Consider the rotational equilibrium of the beam:

![image 647](McKenzie - Examples in Structural Analysis_images/imageFile647.png)

Equation

- (1)


Consider the vertical equilibrium of the beam:

![image 648](McKenzie - Examples in Structural Analysis_images/imageFile648.png)

Equation

- (2)


The final vertical support reactions are given by (i)+(ii):

![image 649](McKenzie - Examples in Structural Analysis_images/imageFile649.png)

![image 650](McKenzie - Examples in Structural Analysis_images/imageFile650.png)

Check the vertical equilibrium: Total vertical force =+50.0+30.0 =+80 kN

![image 651](McKenzie - Examples in Structural Analysis_images/imageFile651.png)

###### Figure 4.81

|Note the similarity between the shape of the bending moment diagram and the final deflected shape as shown in Figure 4.82.<br><br>![image 652](McKenzie - Examples in Structural Analysis_images/imageFile652.png)<br><br>Figure 4.82 The position of the maximum bending moment can be determined by finding the point of<br><br>zero shear force as shown in Figure 4.83.<br><br>![image 653](McKenzie - Examples in Structural Analysis_images/imageFile653.png)<br><br>Figure 4.83<br><br>4.7.8 Distribution Factors<br><br>Consider a uniform two-span continuous beam, as shown in Figure 4.84.<br><br>![image 654](McKenzie - Examples in Structural Analysis_images/imageFile654.png)<br><br>Figure 4.84<br><br><br>If an external moment M is applied to this structure at support B it will produce a rotation of the beam at the support; part of this moment is absorbed by each of the two spans BA and BC, as indicated in Figure 4.85.<br><br>|
|---|


![image 655](McKenzie - Examples in Structural Analysis_images/imageFile655.png)

###### Figure 4.85The proportion of each moment induced in each span is directly proportional to the

relative stiffnesses, e.g.

![image 656](McKenzie - Examples in Structural Analysis_images/imageFile656.png)

![image 657](McKenzie - Examples in Structural Analysis_images/imageFile657.png)

The ratio is known as the Distribution Factor for the member at the joint where the moment is applied.

As indicated in Section 4.7.2, when a moment (M) is applied to one end of a beam in which the other end is fixed, a carry-over moment equal to 50% of M is induced at the remote fixed-end and consequently moments equal

to ½ M1 and ½ M2 will develop at supports A and C respectively, as shown in Figure 4.86.

![image 658](McKenzie - Examples in Structural Analysis_images/imageFile658.png)

###### Figure 4.86

|4.7.9 Application of the Method<br><br>All of the concepts outlined in Sections 4.7.1 to 4.7.8 are used when analysing indeterminate structures using the method of moment distribution. Consider the two separate beam spans indicated in Figure 4.87.<br><br>![image 659](McKenzie - Examples in Structural Analysis_images/imageFile659.png)<br><br>Figure 4.87 Since the beams are not connected at the support B they behave independently as simply<br><br>supported beams with separate reactions and bending moment diagrams, as shown in Figure 4.88.<br><br>![image 660](McKenzie - Examples in Structural Analysis_images/imageFile660.png)<br><br>Figure 4.88<br><br><br>When the beams are continuous over support B as shown in Figure 4.89(a), a continuity moment develops for the continuous structure as shown in Figures 4.89(b) and (c). Note the similarity of the bending moment diagram for member AB to the propped cantilever in Figure 4.81. Both members AB and BD are similar to propped cantilevers in this structure.<br><br>|
|---|


|![image 661](McKenzie - Examples in Structural Analysis_images/imageFile661.png)<br><br>Figure 4.89 Moment distribution enables the evaluation of the continuity moments. The method is<br><br>ideally suited to tabular representation and is illustrated in Example 4.21.<br><br>4.7.10 Example 4.21: Three-span Continuous Beam<br><br>A non-uniform, three span beam ABCDEF is fixed at support A and pinned at support F, as illustrated in Figure 4.90. Determine the support reactions and sketch the bending moment diagram for the applied loading indicated.<br><br>![image 662](McKenzie - Examples in Structural Analysis_images/imageFile662.png)<br><br>Figure 4.90<br><br><br>Solution:<br><br>Step 1<br><br>The first step is to assume that all supports are fixed against rotation and evaluate the ‘fixed-end moments’.<br><br>![image 663](McKenzie - Examples in Structural Analysis_images/imageFile663.png)<br><br>The values of the fixed-end moments for encastre beams are given in Appendix 2.<br><br>|
|---|


![image 664](McKenzie - Examples in Structural Analysis_images/imageFile664.png)

* Since support F is pinned, the fixed-end moments are (MDF−0.5MFD) at D and zero at F (see Figure 4.79):

![image 665](McKenzie - Examples in Structural Analysis_images/imageFile665.png)

- Step 2 The second step is to evaluate the member and total stiffness at each internal joint/support


and determine the distribution factors at each support. Note that the applied force system is not required to do this.

![image 666](McKenzie - Examples in Structural Analysis_images/imageFile666.png)

Support C

![image 667](McKenzie - Examples in Structural Analysis_images/imageFile667.png)

Support D

![image 668](McKenzie - Examples in Structural Analysis_images/imageFile668.png)

![image 669](McKenzie - Examples in Structural Analysis_images/imageFile669.png)

The structure and the distribution factors can be represented in tabular form, as shown in Figure 4.91.

![image 670](McKenzie - Examples in Structural Analysis_images/imageFile670.png)

###### Figure 4.91

The distribution factor for fixed supports is equal to zero since any moment is resisted by an equal and opposite moment within the support and no balancing is required. In the case of pinned supports the distribution factor is equal to 1.0 since 100% of any applied moment, e.g. by a cantilever overhang, must be balanced and a carry-over of ½×the balancing moment transferred to the remote end at the internal support.

- Step 3 The fixed-end moments are now entered into the table at the appropriate locations, taking


care to ensure that the signs are correct.

![image 671](McKenzie - Examples in Structural Analysis_images/imageFile671.png)

- Step 4 When the structure is restrained against rotation there is normally a resultant moment at a


typical internal support. For example, consider the moments C:

![image 672](McKenzie - Examples in Structural Analysis_images/imageFile672.png)

If the imposed fixity at one support (all others remaining fixed), e.g. support C, is released, the beam will rotate sufficiently to induce a balancing moment such that equilibrium is achieved and the moments MCA and MCD are equal and opposite. The application of the balancing moment is distributed between CA and CD in proportion to the distribution factors calculated previously.

![image 673](McKenzie - Examples in Structural Analysis_images/imageFile673.png)

- As indicated in Section 4.7.2, when a moment is applied to one end of a beam whilst


the remote end is fixed, a carry-over moment equal to (½×applied moment) and of the same sign is induced at the remote end. This is entered into the table as shown.

![image 674](McKenzie - Examples in Structural Analysis_images/imageFile674.png)

- Step 5 The procedure outline above is then carried out for each restrained support in turn. The


reader should confirm the values given in the table for support D.

![image 675](McKenzie - Examples in Structural Analysis_images/imageFile675.png)

If the total moments at each internal support are now calculated they are:

![image 676](McKenzie - Examples in Structural Analysis_images/imageFile676.png)

It is evident that after one iteration of each support moment the true values are nearer to 23.8 kNm and 69.0 kNm for C and D respectively. The existing out-of-balance moments which still exist, 0.64 kNm, can be distributed in the same manner as during the first iteration. This process is carried out until the desired level of accuracy has been achieved, normally after three or four iterations.

A slight modification to carrying out the distribution process which still results in the same answers is to carry out the balancing operation for all supports simultaneously and the carry-over operation likewise. This is quicker and requires less work. The reader should complete a further three/four iterations to the solution given above and compare the results with those shown in Figure 4.92.

![image 677](McKenzie - Examples in Structural Analysis_images/imageFile677.png)

- Figure 4.92 The continuity moments are shown in Figure 4.93.

![image 678](McKenzie - Examples in Structural Analysis_images/imageFile678.png)

- Figure 4.93


The support reactions and the bending moment diagrams for each span can be calculated using superposition as before by considering each span separately.

|(i) Fixed Support Reactions<br><br>![image 679](McKenzie - Examples in Structural Analysis_images/imageFile679.png)<br><br>Consider span AC:<br><br>|
|---|
|![image 680](McKenzie - Examples in Structural Analysis_images/imageFile680.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 681](McKenzie - Examples in Structural Analysis_images/imageFile681.png)<br><br>Equation<br><br>(2)|
|Consider span CD:<br><br>|
|![image 682](McKenzie - Examples in Structural Analysis_images/imageFile682.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 683](McKenzie - Examples in Structural Analysis_images/imageFile683.png)<br><br>Equation|


###### (2)

|Consider span DF:<br><br>|
|---|
|![image 684](McKenzie - Examples in Structural Analysis_images/imageFile684.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 685](McKenzie - Examples in Structural Analysis_images/imageFile685.png)<br><br>Equation<br><br>(2)|
|Fixed vertical reactions<br><br>The total vertical reaction at each support due to the continuity moments is equal to the algebraic sum of the contributions from each beam at the support.<br><br>|
|![image 686](McKenzie - Examples in Structural Analysis_images/imageFile686.png)|
|![image 687](McKenzie - Examples in Structural Analysis_images/imageFile687.png)|


|Free bending moments<br><br>![image 688](McKenzie - Examples in Structural Analysis_images/imageFile688.png)<br><br>Consider span AC:<br><br>|
|---|
|![image 689](McKenzie - Examples in Structural Analysis_images/imageFile689.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 690](McKenzie - Examples in Structural Analysis_images/imageFile690.png)<br><br>Equation<br><br>(2)|
|Consider span CD:<br><br>|
|![image 691](McKenzie - Examples in Structural Analysis_images/imageFile691.png)<br><br>Equation<br><br>(1)|
|Consider the vertical equilibrium of the beam:<br><br>|
|![image 692](McKenzie - Examples in Structural Analysis_images/imageFile692.png)<br><br>Equation<br><br>(2)|
|Consider span DF:<br><br>|


![image 693](McKenzie - Examples in Structural Analysis_images/imageFile693.png)

Equation

- (1)

Consider the vertical equilibrium of the beam:

![image 694](McKenzie - Examples in Structural Analysis_images/imageFile694.png)

Equation

- (2)


![image 695](McKenzie - Examples in Structural Analysis_images/imageFile695.png)

![image 696](McKenzie - Examples in Structural Analysis_images/imageFile696.png)

The final bending moment diagram is shown in Figure 4.94.

![image 697](McKenzie - Examples in Structural Analysis_images/imageFile697.png)

- Figure 4.94


|4.7.11 Problems: Moment Distribution—Continuous Beams<br><br>A series of continuous beams are indicated in Problems 4.28 to 4.32 in which the relative EI values and the applied loading are given. In each case:<br><br>|
|---|
|i) determine the support reactions,<br><br>ii) sketch the shear force diagram and<br><br>iii) sketch the bending moment diagram.<br><br><br>|
|![image 698](McKenzie - Examples in Structural Analysis_images/imageFile698.png)<br><br>Problem 4.28<br><br>![image 699](McKenzie - Examples in Structural Analysis_images/imageFile699.png)<br><br>Problem 4.29<br><br>![image 700](McKenzie - Examples in Structural Analysis_images/imageFile700.png)<br><br>Problem 4.30<br><br><br>![image 701](McKenzie - Examples in Structural Analysis_images/imageFile701.png)<br><br>|


|Problem 4.31<br><br>![image 702](McKenzie - Examples in Structural Analysis_images/imageFile702.png)<br><br>Problem 4.32<br><br><br>4.7.12 Solutions: Moment Distribution—Continuous Beams<br><br>![image 703](McKenzie - Examples in Structural Analysis_images/imageFile703.png)<br><br>|
|---|


|![image 704](McKenzie - Examples in Structural Analysis_images/imageFile704.png)|
|---|


|![image 705](McKenzie - Examples in Structural Analysis_images/imageFile705.png)|
|---|


|![image 706](McKenzie - Examples in Structural Analysis_images/imageFile706.png)|
|---|


|![image 707](McKenzie - Examples in Structural Analysis_images/imageFile707.png)|
|---|


|![image 708](McKenzie - Examples in Structural Analysis_images/imageFile708.png)|
|---|


|![image 709](McKenzie - Examples in Structural Analysis_images/imageFile709.png)|
|---|


|![image 710](McKenzie - Examples in Structural Analysis_images/imageFile710.png)|
|---|


|![image 711](McKenzie - Examples in Structural Analysis_images/imageFile711.png)|
|---|


|![image 712](McKenzie - Examples in Structural Analysis_images/imageFile712.png)|
|---|


|![image 713](McKenzie - Examples in Structural Analysis_images/imageFile713.png)|
|---|


|![image 714](McKenzie - Examples in Structural Analysis_images/imageFile714.png)|
|---|


|![image 715](McKenzie - Examples in Structural Analysis_images/imageFile715.png)|
|---|


|![image 716](McKenzie - Examples in Structural Analysis_images/imageFile716.png)|
|---|


|![image 717](McKenzie - Examples in Structural Analysis_images/imageFile717.png)|
|---|


|![image 718](McKenzie - Examples in Structural Analysis_images/imageFile718.png)|
|---|


|![image 719](McKenzie - Examples in Structural Analysis_images/imageFile719.png)|
|---|


|![image 720](McKenzie - Examples in Structural Analysis_images/imageFile720.png)|
|---|


|![image 721](McKenzie - Examples in Structural Analysis_images/imageFile721.png)|
|---|


|![image 722](McKenzie - Examples in Structural Analysis_images/imageFile722.png)|
|---|


|![image 723](McKenzie - Examples in Structural Analysis_images/imageFile723.png)|
|---|


|![image 724](McKenzie - Examples in Structural Analysis_images/imageFile724.png)|
|---|


|![image 725](McKenzie - Examples in Structural Analysis_images/imageFile725.png)|
|---|


![image 726](McKenzie - Examples in Structural Analysis_images/imageFile726.png)

### 5. Rigid-Jointed Frames

#### 5.1 Rigid-Jointed Frames

Rigid-jointed frames are framed structures in which the members transmit applied loads by axial, shear, and bending effects. There are basically two types of frame to consider;

- (i) statically determinate frames; see Figure 5.1(a) and

- (ii) statically indeterminate frames; see Figure 5.1(b).


![image 727](McKenzie - Examples in Structural Analysis_images/imageFile727.png)

- Figure 5.1


Rigid-joints (moment connections) are designed to transfer axial and shear forces in addition to bending moments between the connected members whilst pinned joints (simple connections) are designed to transfer axial and shear forces only. Typical moment and simple connections between steel members is illustrated in Figure 5.2.

In the case of statically determinate frames, only the equations of equilibrium are required to determine the member forces. They are often used where there is a possibility of support settlement since statically determinate frames can accommodate small changes of geometry without inducing significant secondary stresses. Analysis of such frames is illustrated in this Examples 5.1 and 5.2 and Problems 5.1 to 5.4.

![image 728](McKenzie - Examples in Structural Analysis_images/imageFile728.png)

- Figure 5.2


Statically indeterminate frames require consideration of compatibility when determining the member forces. One of the most convenient and most versatile methods of analysis for such frames is moment distribution. When using this method there are two cases to consider; no-sway frames and sway frames. Analysis of the former is illustrated in Example 5.2 and Problems 5.5 to 5.12 and in the latter in Example 5.4 and Problems

- 5.13 to 5.18.


###### 5.1.1 Example 5.1 Statically Determinate Rigid–Jointed Frame 1

A asymmetric portal frame is supported on a roller at A and pinned at support D as shown in Figure 5.3. For the loading indicated:

i) determine the support reactions and

ii) sketch the axial load, shear force and bending moment diagrams.

![image 729](McKenzie - Examples in Structural Analysis_images/imageFile729.png)

Figure 5.3

Solution:

Apply the three equations of static equilibrium to the force system

![image 730](McKenzie - Examples in Structural Analysis_images/imageFile730.png)

Equation

- (1)


![image 731](McKenzie - Examples in Structural Analysis_images/imageFile731.png)

Equation

###### (2)

|![image 732](McKenzie - Examples in Structural Analysis_images/imageFile732.png)<br><br>Equation<br><br>(3)|
|---|
|![image 733](McKenzie - Examples in Structural Analysis_images/imageFile733.png)<br><br>Assuming positive bending moments induce tension inside the frame:<br><br>|
|MB=−(6.0×4.0ĩ(2.0)=−48.0 kNm MC=+(46.5×3.0)−(40.0×4.0)=−20.50 kNm|
|![image 734](McKenzie - Examples in Structural Analysis_images/imageFile734.png)<br><br>Figure 5.4<br><br>The values of the end-forces F1 to F8 can be determined by considering the equilibrium of each member and joint in turn.<br><br>Consider member AB:<br><br>|
|![image 735](McKenzie - Examples in Structural Analysis_images/imageFile735.png)|
|Consider joint B:<br><br>|


![image 736](McKenzie - Examples in Structural Analysis_images/imageFile736.png)

Consider member BC:

![image 737](McKenzie - Examples in Structural Analysis_images/imageFile737.png)

Consider member CD:

![image 738](McKenzie - Examples in Structural Analysis_images/imageFile738.png)

Check joint C:

![image 739](McKenzie - Examples in Structural Analysis_images/imageFile739.png)

The axial force and shear force in member CD can be found from:

###### Axial load=+/−(Horizontal force×Cosα)+/−(Vertical force×Sinα) Shear force=+/−(Horizontal force×Sinα)+/−(Vertical force×Cosα) The signs are dependent on the directions of the respective forces. Member CD:

![image 740](McKenzie - Examples in Structural Analysis_images/imageFile740.png)

![image 741](McKenzie - Examples in Structural Analysis_images/imageFile741.png)

###### Figure 5.5

###### 5.1.2 Example 5.2 Statically Determinate Rigid-Jointed Frame 2

A pitched-roof portal frame is pinned at supports A and H and members CD and DEF are pinned at the ridge as shown in Figure 5.6. For the loading indicated:

i) determine the support reactions and

ii) sketch the axial load, shear force and bending moment diagrams.

![image 742](McKenzie - Examples in Structural Analysis_images/imageFile742.png)

- Figure 5.6


Apply the three equations of static equilibrium to the force system in addition to the Σ moments at the pin=0:

![image 743](McKenzie - Examples in Structural Analysis_images/imageFile743.png)

Equation

(1)

![image 744](McKenzie - Examples in Structural Analysis_images/imageFile744.png)

Equation

###### (2)

|![image 745](McKenzie - Examples in Structural Analysis_images/imageFile745.png)<br><br>Equation<br><br>(3)|
|---|
|![image 746](McKenzie - Examples in Structural Analysis_images/imageFile746.png)<br><br>Equation<br><br>(4)<br><br>|
|![image 747](McKenzie - Examples in Structural Analysis_images/imageFile747.png)<br><br>Equation (3a)|
|![image 748](McKenzie - Examples in Structural Analysis_images/imageFile748.png)<br><br>Equation (3b)<br><br>![image 749](McKenzie - Examples in Structural Analysis_images/imageFile749.png)<br><br>![image 750](McKenzie - Examples in Structural Analysis_images/imageFile750.png)<br><br>Figure 5.7<br><br>|


|Assuming positive bending moments induce tension inside the frame:<br><br>|
|---|
|![image 751](McKenzie - Examples in Structural Analysis_images/imageFile751.png)|
|![image 752](McKenzie - Examples in Structural Analysis_images/imageFile752.png)<br><br>Figure 5.8<br><br>The values of the end-forces F1 to F12 can be determined by considering the equilibrium of each member and joint in turn.<br><br>Consider member ABC:<br><br>|
|![image 753](McKenzie - Examples in Structural Analysis_images/imageFile753.png)|
|Consider joint C:<br><br>|


![image 754](McKenzie - Examples in Structural Analysis_images/imageFile754.png)

Consider member CD:

![image 755](McKenzie - Examples in Structural Analysis_images/imageFile755.png)

Consider member FGH:

![image 756](McKenzie - Examples in Structural Analysis_images/imageFile756.png)

Consider joint F:

![image 757](McKenzie - Examples in Structural Analysis_images/imageFile757.png)

![image 758](McKenzie - Examples in Structural Analysis_images/imageFile758.png)

Consider member DF:

![image 759](McKenzie - Examples in Structural Analysis_images/imageFile759.png)

The calculated values can be checked by considering the equilibrium at joint D.

![image 760](McKenzie - Examples in Structural Analysis_images/imageFile760.png)

###### Figure 5.9

![image 761](McKenzie - Examples in Structural Analysis_images/imageFile761.png)

|The axial force and shear force in member CD can be found from:<br><br>|
|---|
|Axial load=+/−(Horizontal force×Cosα)+/−(Vertical force×Sinα) Shear force=+/−(Horizontal force×Sinα)+/−(Vertical force×Cosα)|
|The signs are dependent on the directions of the respective forces.<br><br>Similarly with θ for member DEF. Member CD:<br><br>![image 762](McKenzie - Examples in Structural Analysis_images/imageFile762.png)<br><br>Member DEF:<br><br>![image 763](McKenzie - Examples in Structural Analysis_images/imageFile763.png)<br><br>|


|![image 764](McKenzie - Examples in Structural Analysis_images/imageFile764.png)<br><br>Figure 5.10<br><br>|
|---|


|5.1.3 Problems: Statically Determinate Rigid-Jointed Frames<br><br>A series of statically determinate, rigid-jointed frames are indicated in Problems 5.1 to 5.4. In each case, for the loading given:<br><br>|
|---|
|i) determine the support reactions and<br><br>ii) sketch the axial load, shear force and bending moment diagrams.<br><br>|
|![image 765](McKenzie - Examples in Structural Analysis_images/imageFile765.png)<br><br>Problem 5.1<br><br>![image 766](McKenzie - Examples in Structural Analysis_images/imageFile766.png)<br><br>Problem 5.2<br><br><br>|


![image 767](McKenzie - Examples in Structural Analysis_images/imageFile767.png)

###### Problem 5.3

![image 768](McKenzie - Examples in Structural Analysis_images/imageFile768.png)

###### Problem 5.4

|5.1.4 Solutions: Statically Determinate Rigid-Jointed Frames<br><br>![image 769](McKenzie - Examples in Structural Analysis_images/imageFile769.png)|
|---|


|![image 770](McKenzie - Examples in Structural Analysis_images/imageFile770.png)|
|---|


|![image 771](McKenzie - Examples in Structural Analysis_images/imageFile771.png)|
|---|


|![image 772](McKenzie - Examples in Structural Analysis_images/imageFile772.png)|
|---|


|![image 773](McKenzie - Examples in Structural Analysis_images/imageFile773.png)|
|---|


|![image 774](McKenzie - Examples in Structural Analysis_images/imageFile774.png)|
|---|


|![image 775](McKenzie - Examples in Structural Analysis_images/imageFile775.png)|
|---|


|![image 776](McKenzie - Examples in Structural Analysis_images/imageFile776.png)|
|---|


|![image 777](McKenzie - Examples in Structural Analysis_images/imageFile777.png)|
|---|


|![image 778](McKenzie - Examples in Structural Analysis_images/imageFile778.png)|
|---|


|![image 779](McKenzie - Examples in Structural Analysis_images/imageFile779.png)|
|---|


![image 780](McKenzie - Examples in Structural Analysis_images/imageFile780.png)

#### 5.2 Moment Distribution for No-Sway Rigid-Jointed Frames

The principles of moment distribution are explained in Chapter 4 in relation to the analysis of multi-span beams. In the case of rigid-jointed frames there are many instances where there more than two members meeting at a joint. This results in the out-of-balance

moment induced by the fixed-end moments being distributed among several members. Consider the frame shown in Figure 5.11:

![image 781](McKenzie - Examples in Structural Analysis_images/imageFile781.png)

- Figure 5.11 Fixed-End Moments:

![image 782](McKenzie - Examples in Structural Analysis_images/imageFile782.png)

![image 783](McKenzie - Examples in Structural Analysis_images/imageFile783.png)

- Figure 5.12


Distribution Factors:

At joint B there are four members contributing to the overall stiffness of the joint.

![image 784](McKenzie - Examples in Structural Analysis_images/imageFile784.png)

The sum of the distribution factors is equal 1.0 since 100% of the out-of-balance moment must be distributed between the members.

- At joint C there are three members contributing to the overall stiffness of the joint.


![image 785](McKenzie - Examples in Structural Analysis_images/imageFile785.png)

![image 786](McKenzie - Examples in Structural Analysis_images/imageFile786.png)

- Figure 5.13


|The carry-over moments equal to 50% of the balancing moments are applied to joints A, B, E, F and C.<br><br>![image 787](McKenzie - Examples in Structural Analysis_images/imageFile787.png)<br><br>Figure 5.14<br><br>As before with beams, the above process is carried out until the required accuracy is obtained. This is illustrated in Example 5.3 and the solutions to Problems 5.5 to 5.12.<br><br>5.2.1 Example 5.3 No-Sway Rigid–Jointed Frame 1<br><br>A rigid-jointed, two-bay rectangular frame is pinned at supports A, D and E and carries loading as indicated in Figure 5.15 Given that supports D and E settle by 3 mm and 2 mm respectively and that EI=102.5×103 kNm2;<br><br>|
|---|
|i) sketch the bending moment diagram and determine the support reactions,<br><br>ii) sketch the deflected shape (assuming axially rigid members) and compare with the<br><br><br>shape of the bending moment diagram (the reader should check the answer using a computer analysi`s solution).<br><br>|
|![image 788](McKenzie - Examples in Structural Analysis_images/imageFile788.png)|


|Figure 5.15|
|---|
|Fixed-end Moments:<br><br>The final fixed-end moments are due to the combined effects of the applied member loads and the settlement; consider the member loads,<br><br>![image 789](McKenzie - Examples in Structural Analysis_images/imageFile789.png)<br><br>Figure 5.16 Member AB *<br><br>|
|![image 790](McKenzie - Examples in Structural Analysis_images/imageFile790.png)|
|* Since support A is pinned, the fixed-end moments are (MBA−0.5MAB) at B and zero at A.<br><br>|


![image 791](McKenzie - Examples in Structural Analysis_images/imageFile791.png)

Member CE *

![image 792](McKenzie - Examples in Structural Analysis_images/imageFile792.png)

|* Since support E is pinned, the fixed-end moments are (MCE−0.5MEC) at C and zero at E.|
|---|


![image 793](McKenzie - Examples in Structural Analysis_images/imageFile793.png)

|Consider the settlement of supports D and E: δAB=3.0 mm and δBC=1.0 mm|
|---|


![image 794](McKenzie - Examples in Structural Analysis_images/imageFile794.png)

|Figure 5.17|
|---|


![image 795](McKenzie - Examples in Structural Analysis_images/imageFile795.png)

|Note: the relative displacement between B and C i.e. δBC=(3.0–2.0)=1.0 mm<br><br>|
|---|


![image 796](McKenzie - Examples in Structural Analysis_images/imageFile796.png)

|Final Fixed-end Moments:|
|---|


![image 797](McKenzie - Examples in Structural Analysis_images/imageFile797.png)

|Distribution Factors: Joint B|
|---|


![image 798](McKenzie - Examples in Structural Analysis_images/imageFile798.png)

|Distribution Factors: Joint C|
|---|


![image 799](McKenzie - Examples in Structural Analysis_images/imageFile799.png)

|Moment Distribution Table:|
|---|


![image 800](McKenzie - Examples in Structural Analysis_images/imageFile800.png)

|Continuity Moments:|
|---|


![image 801](McKenzie - Examples in Structural Analysis_images/imageFile801.png)

![image 802](McKenzie - Examples in Structural Analysis_images/imageFile802.png)

|Free bending moments:|
|---|


![image 803](McKenzie - Examples in Structural Analysis_images/imageFile803.png)

|Member CE:|
|---|


![image 804](McKenzie - Examples in Structural Analysis_images/imageFile804.png)

|The maximum value along the length of member CE can be found by identifying the point of zero shear as follows:<br><br>|
|---|


![image 805](McKenzie - Examples in Structural Analysis_images/imageFile805.png)

![image 806](McKenzie - Examples in Structural Analysis_images/imageFile806.png)

|Consider Member AB:|
|---|


![image 807](McKenzie - Examples in Structural Analysis_images/imageFile807.png)

|For the complete frame:|
|---|


![image 808](McKenzie - Examples in Structural Analysis_images/imageFile808.png)

###### 5.2.2 Problems: Moment Distribution—No-Sway Rigid-Jointed Frames

|A series of rigid-jointed frames are indicated in Problems 5.5 to 5.12 in which the relative EI values and the applied loading are given. In each case:<br><br>|
|---|


- i) sketch the bending moment diagram and determine the support reactions,
- ii) sketch the deflected shape (assuming axially rigid members) and compare with the


shape of the bending moment diagram, (check the answer using a computer analysis solution).

![image 809](McKenzie - Examples in Structural Analysis_images/imageFile809.png)

|Problem 5.5|
|---|


![image 810](McKenzie - Examples in Structural Analysis_images/imageFile810.png)

|Problem 5.6|
|---|


![image 811](McKenzie - Examples in Structural Analysis_images/imageFile811.png)

|Problem 5.7|
|---|


![image 812](McKenzie - Examples in Structural Analysis_images/imageFile812.png)

|Problem 5.8|
|---|


![image 813](McKenzie - Examples in Structural Analysis_images/imageFile813.png)

|Problem 5.9|
|---|


![image 814](McKenzie - Examples in Structural Analysis_images/imageFile814.png)

|Problem 5.10|
|---|


![image 815](McKenzie - Examples in Structural Analysis_images/imageFile815.png)

|Problem 5.11|
|---|


![image 816](McKenzie - Examples in Structural Analysis_images/imageFile816.png)

|Problem 5.12|
|---|


###### 5.2.3 Solutions: Moment Distribution—No-Sway Rigid-Jointed Frames

![image 817](McKenzie - Examples in Structural Analysis_images/imageFile817.png)

![image 818](McKenzie - Examples in Structural Analysis_images/imageFile818.png)

![image 819](McKenzie - Examples in Structural Analysis_images/imageFile819.png)

![image 820](McKenzie - Examples in Structural Analysis_images/imageFile820.png)

![image 821](McKenzie - Examples in Structural Analysis_images/imageFile821.png)

![image 822](McKenzie - Examples in Structural Analysis_images/imageFile822.png)

![image 823](McKenzie - Examples in Structural Analysis_images/imageFile823.png)

![image 824](McKenzie - Examples in Structural Analysis_images/imageFile824.png)

![image 825](McKenzie - Examples in Structural Analysis_images/imageFile825.png)

![image 826](McKenzie - Examples in Structural Analysis_images/imageFile826.png)

![image 827](McKenzie - Examples in Structural Analysis_images/imageFile827.png)

![image 828](McKenzie - Examples in Structural Analysis_images/imageFile828.png)

![image 829](McKenzie - Examples in Structural Analysis_images/imageFile829.png)

![image 830](McKenzie - Examples in Structural Analysis_images/imageFile830.png)

![image 831](McKenzie - Examples in Structural Analysis_images/imageFile831.png)

![image 832](McKenzie - Examples in Structural Analysis_images/imageFile832.png)

![image 833](McKenzie - Examples in Structural Analysis_images/imageFile833.png)

![image 834](McKenzie - Examples in Structural Analysis_images/imageFile834.png)

![image 835](McKenzie - Examples in Structural Analysis_images/imageFile835.png)

![image 836](McKenzie - Examples in Structural Analysis_images/imageFile836.png)

![image 837](McKenzie - Examples in Structural Analysis_images/imageFile837.png)

![image 838](McKenzie - Examples in Structural Analysis_images/imageFile838.png)

![image 839](McKenzie - Examples in Structural Analysis_images/imageFile839.png)

![image 840](McKenzie - Examples in Structural Analysis_images/imageFile840.png)

![image 841](McKenzie - Examples in Structural Analysis_images/imageFile841.png)

![image 842](McKenzie - Examples in Structural Analysis_images/imageFile842.png)

![image 843](McKenzie - Examples in Structural Analysis_images/imageFile843.png)

![image 844](McKenzie - Examples in Structural Analysis_images/imageFile844.png)

![image 845](McKenzie - Examples in Structural Analysis_images/imageFile845.png)

![image 846](McKenzie - Examples in Structural Analysis_images/imageFile846.png)

![image 847](McKenzie - Examples in Structural Analysis_images/imageFile847.png)

![image 848](McKenzie - Examples in Structural Analysis_images/imageFile848.png)

![image 849](McKenzie - Examples in Structural Analysis_images/imageFile849.png)

![image 850](McKenzie - Examples in Structural Analysis_images/imageFile850.png)

![image 851](McKenzie - Examples in Structural Analysis_images/imageFile851.png)

![image 852](McKenzie - Examples in Structural Analysis_images/imageFile852.png)

![image 853](McKenzie - Examples in Structural Analysis_images/imageFile853.png)

#### 5.3 Moment Distribution for Rigid-Jointed Frames with Sway

|The frames in Section 5.2 are prevented from any lateral movement by the support conditions. In frames where restraint against lateral movement is not provided at each level, unless the frame, the supports and the loading are symmetrical it will sway and consequently induce additional forces in the frame members.<br><br>Consider the frame indicated in Figure 5.18(a) in which the frame, supports and applied load are symmetrical.<br><br>|
|---|


![image 854](McKenzie - Examples in Structural Analysis_images/imageFile854.png)

|Figure 5.18<br><br>Consider the same frame in which the load has been moved such that is now asymmetric as indicated in Figure 5.19(a)<br><br>|
|---|


![image 855](McKenzie - Examples in Structural Analysis_images/imageFile855.png)

|Figure 5.19|
|---|


It is evident from Figure 5.19(b) that the solution to this problem is incomplete. Inspection of the deflected shapes of each of the frames in Figure 5.18(a) and 5.19(a) indicates the reason for the inconsistency in the asymmetric frame.

Consider the deflected shapes shown in Figures 5.20 (a) and (b):

![image 856](McKenzie - Examples in Structural Analysis_images/imageFile856.png)

|Figure 5.20<br><br>In case (a) the deflected shape indicates the equal rotations of the joints at B and C due to the balancing of the fixed-end moments induced by the load; note that there is no lateral<br><br>movement at B and C.<br><br>In case (b) in addition to rotation due to the applied load there is also rotation of the joints due to the lateral movement ‘δ’ of B and C. The sway of the frame also induces forces in the members and this effect was not included in the results given in Figure 5.19(b). It is ignoring the ‘sway’ of the frame which has resulted in the inconsistency. In effect, the frame which has been analysed is the one shown in Figure 5.21, i.e. including a prop force preventing sway. The value of the prop force ‘P’ is equal to the resultant horizontal force in Figure 5.19.<br><br><br>|
|---|


![image 857](McKenzie - Examples in Structural Analysis_images/imageFile857.png)

Figure 5.21

The complete analysis should include the effects of the sway and consequently an additional distribution must be carried out for sway-only and the effects added to the no-

sway results, i.e. to cancel out the non-existent ‘prop force’ assumed in the no-sway frame.

![image 858](McKenzie - Examples in Structural Analysis_images/imageFile858.png)

|Figure 5.22<br><br>The technique for completing this calculation including the sway effects is illustrated in Example 5.4 and the solutions to Problems 5.13 to 5.18.<br><br>|
|---|


#### 5.3.1 Example 5.4 Rigid-Jointed Frame with Sway- Frame 1

|A rigid-jointed frame is fixed at support A, pinned at support H and supported on a roller at F as shown in Figure 5.23. For the relative EI values and loading given:<br><br>|
|---|


- i) sketch the bending moment diagram,
- ii) determine the support reactions and
- iii) sketch the deflected shape (assuming axially rigid members) and compare with the


shape of the bending moment diagram, (the reader should check the answer using a computer analysis solution). EI=10×103 kNm2

![image 859](McKenzie - Examples in Structural Analysis_images/imageFile859.png)

###### Figure 5.23

|Consider the frame analysis as the superposition of two effects:|
|---|


![image 860](McKenzie - Examples in Structural Analysis_images/imageFile860.png)

|Figure 5.24|
|---|


![image 861](McKenzie - Examples in Structural Analysis_images/imageFile861.png)

|Figure 25.5 Consider the No-Sway Frame: Fixed-end Moments Member BCD<br><br>|
|---|


![image 862](McKenzie - Examples in Structural Analysis_images/imageFile862.png)

|Fixed-end Moments Member DEF|
|---|


![image 863](McKenzie - Examples in Structural Analysis_images/imageFile863.png)

|Fixed-end Moments Member DGH<br><br>Since support H pinned, the fixed-end moments are (MDH—0.5MHD) at D and zero at H.<br><br>|
|---|


![image 864](McKenzie - Examples in Structural Analysis_images/imageFile864.png)

|Distribution Factors : Joint B|
|---|


![image 865](McKenzie - Examples in Structural Analysis_images/imageFile865.png)

|Distribution Factors : Joint D|
|---|


![image 866](McKenzie - Examples in Structural Analysis_images/imageFile866.png)

|No-Sway Moment Distribution Table:|
|---|


![image 867](McKenzie - Examples in Structural Analysis_images/imageFile867.png)

|Determine the value of the reactions and prop force P:|
|---|


![image 868](McKenzie - Examples in Structural Analysis_images/imageFile868.png)

|Consider member DEF:|
|---|


![image 869](McKenzie - Examples in Structural Analysis_images/imageFile869.png)

|Consider member DGH:|
|---|


![image 870](McKenzie - Examples in Structural Analysis_images/imageFile870.png)

|Consider member BA and a section to the left of D:|
|---|


![image 871](McKenzie - Examples in Structural Analysis_images/imageFile871.png)

![image 872](McKenzie - Examples in Structural Analysis_images/imageFile872.png)

Equation

(1)

|![image 873](McKenzie - Examples in Structural Analysis_images/imageFile873.png)<br><br>Equation<br><br>(2)<br><br>Solve equations (1) and (2) simultaneously:<br><br>|
|---|


![image 874](McKenzie - Examples in Structural Analysis_images/imageFile874.png)

|Consider the equilibrium of the complete frame:|
|---|


![image 875](McKenzie - Examples in Structural Analysis_images/imageFile875.png)

|![image 876](McKenzie - Examples in Structural Analysis_images/imageFile876.png)<br><br>Since the direction of the prop force is right-to-left the sway of the frame is from lefttoright as shown.<br><br>|
|---|


![image 877](McKenzie - Examples in Structural Analysis_images/imageFile877.png)

|Apply an arbitrary sway force P′ to determine the ratio of the fixed-end moments.|
|---|


![image 878](McKenzie - Examples in Structural Analysis_images/imageFile878.png)

|The fixed-end moments in each member are related to the end-displacements (δ) in each case. The relationship between δAB, δAD and δDH can be determined by considering the displacement triangle at joint B and the geometry of the frame.<br><br>Displacement triangle:<br><br>|
|---|


![image 879](McKenzie - Examples in Structural Analysis_images/imageFile879.png)

![image 880](McKenzie - Examples in Structural Analysis_images/imageFile880.png)

|Assume arbitrary fixed-end moments equal to:|
|---|


![image 881](McKenzie - Examples in Structural Analysis_images/imageFile881.png)

|Sway-Qnly Moment Distribution Table:|
|---|


![image 882](McKenzie - Examples in Structural Analysis_images/imageFile882.png)

|Determine the value of the arbitrary sway force P′:|
|---|


![image 883](McKenzie - Examples in Structural Analysis_images/imageFile883.png)

|Consider member DEF:|
|---|


![image 884](McKenzie - Examples in Structural Analysis_images/imageFile884.png)

|Consider member DGH:|
|---|


![image 885](McKenzie - Examples in Structural Analysis_images/imageFile885.png)

|Consider member AB and a section to the left of D:|
|---|


![image 886](McKenzie - Examples in Structural Analysis_images/imageFile886.png)

![image 887](McKenzie - Examples in Structural Analysis_images/imageFile887.png)

Equation

(3)

|![image 888](McKenzie - Examples in Structural Analysis_images/imageFile888.png)<br><br>Equation<br><br>(4)<br><br>Solve equations (3) and (4) simultaneously:<br><br>|
|---|


![image 889](McKenzie - Examples in Structural Analysis_images/imageFile889.png)

|Consider the equilibrium of the complete frame:|
|---|


![image 890](McKenzie - Examples in Structural Analysis_images/imageFile890.png)

|![image 891](McKenzie - Examples in Structural Analysis_images/imageFile891.png)|
|---|


![image 892](McKenzie - Examples in Structural Analysis_images/imageFile892.png)

![image 893](McKenzie - Examples in Structural Analysis_images/imageFile893.png)

|The multiplying factor for the sway moments=+2.02<br><br>Final Moments Distribution Table:<br><br>|
|---|


||Joint|
|---|
||A|
|---|
| | | | | | | | | ||H|
|---|
|
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | |B| | |D| | | |F| |
| | | | | | | | | | | | |
| ||AB|
|---|
| | ||BD|
|---|
| | | ||DF|
|---|
| | ||HD|
|---|
|
| | | |BA| | |DB|DH| | |FD| |
| | | | | | | | | | | | |
|No-Sway Moments|+9.93| |+19.87|−19.87| |+20.06|−6.66|−13.40| |0|0|
|Sway Moments×2.02|−46.36| |−44.24|+44.24| |+37.57|−33.93|−3.64| |0|0|
|Final Moments (kNm)|−36.43| |−24.37|+24.37| |+57.63|−40.59|−17.04| |0|0|


|![image 894](McKenzie - Examples in Structural Analysis_images/imageFile894.png)<br><br>The horizontal deflection at the rafter level=δDH=0.8δAB=(0.8×20)=16 mm<br><br>Final values of support reactions:<br><br>|
|---|


![image 895](McKenzie - Examples in Structural Analysis_images/imageFile895.png)

|Continuity Moments:|
|---|


![image 896](McKenzie - Examples in Structural Analysis_images/imageFile896.png)

|Free bending moment member BCD:|
|---|


![image 897](McKenzie - Examples in Structural Analysis_images/imageFile897.png)

|Free bending moment member DEF:|
|---|


![image 898](McKenzie - Examples in Structural Analysis_images/imageFile898.png)

|Free bending moment member DGH:|
|---|


![image 899](McKenzie - Examples in Structural Analysis_images/imageFile899.png)

![image 900](McKenzie - Examples in Structural Analysis_images/imageFile900.png)

|* The maximum value along the length of members BCD can be found by identifying the point of zero shear as follows:<br><br>|
|---|


![image 901](McKenzie - Examples in Structural Analysis_images/imageFile901.png)

![image 902](McKenzie - Examples in Structural Analysis_images/imageFile902.png)

![image 903](McKenzie - Examples in Structural Analysis_images/imageFile903.png)

###### 5.3.2 Problems: Moment Distribution - Rigid-Jointed Frames with Sway

|A series of rigid-jointed frames are indicated in Problems 5.13 to 5.18 in which the relative EI values and the applied loading are given. In each case:<br><br>|
|---|


i) sketch the bending moment diagram and ii) sketch the deflected shape (assuming axially rigid members) and compare the shape

of the bending moment diagram with a computer analysis solution of the deflected shape.

![image 904](McKenzie - Examples in Structural Analysis_images/imageFile904.png)

|Problem 5.13|
|---|


![image 905](McKenzie - Examples in Structural Analysis_images/imageFile905.png)

|Problem 5.14|
|---|


![image 906](McKenzie - Examples in Structural Analysis_images/imageFile906.png)

|Problem 5.15|
|---|


![image 907](McKenzie - Examples in Structural Analysis_images/imageFile907.png)

|Problem 5.16|
|---|


![image 908](McKenzie - Examples in Structural Analysis_images/imageFile908.png)

|Problem 5.17|
|---|


![image 909](McKenzie - Examples in Structural Analysis_images/imageFile909.png)

|Problem 5.18|
|---|


###### 5.3.3 Solutions: Moment Distribution—Rigid-Jointed Frames withSway

![image 910](McKenzie - Examples in Structural Analysis_images/imageFile910.png)

![image 911](McKenzie - Examples in Structural Analysis_images/imageFile911.png)

![image 912](McKenzie - Examples in Structural Analysis_images/imageFile912.png)

![image 913](McKenzie - Examples in Structural Analysis_images/imageFile913.png)

![image 914](McKenzie - Examples in Structural Analysis_images/imageFile914.png)

![image 915](McKenzie - Examples in Structural Analysis_images/imageFile915.png)

![image 916](McKenzie - Examples in Structural Analysis_images/imageFile916.png)

![image 917](McKenzie - Examples in Structural Analysis_images/imageFile917.png)

![image 918](McKenzie - Examples in Structural Analysis_images/imageFile918.png)

![image 919](McKenzie - Examples in Structural Analysis_images/imageFile919.png)

![image 920](McKenzie - Examples in Structural Analysis_images/imageFile920.png)

![image 921](McKenzie - Examples in Structural Analysis_images/imageFile921.png)

![image 922](McKenzie - Examples in Structural Analysis_images/imageFile922.png)

![image 923](McKenzie - Examples in Structural Analysis_images/imageFile923.png)

![image 924](McKenzie - Examples in Structural Analysis_images/imageFile924.png)

![image 925](McKenzie - Examples in Structural Analysis_images/imageFile925.png)

![image 926](McKenzie - Examples in Structural Analysis_images/imageFile926.png)

![image 927](McKenzie - Examples in Structural Analysis_images/imageFile927.png)

![image 928](McKenzie - Examples in Structural Analysis_images/imageFile928.png)

![image 929](McKenzie - Examples in Structural Analysis_images/imageFile929.png)

![image 930](McKenzie - Examples in Structural Analysis_images/imageFile930.png)

![image 931](McKenzie - Examples in Structural Analysis_images/imageFile931.png)

![image 932](McKenzie - Examples in Structural Analysis_images/imageFile932.png)

![image 933](McKenzie - Examples in Structural Analysis_images/imageFile933.png)

![image 934](McKenzie - Examples in Structural Analysis_images/imageFile934.png)

![image 935](McKenzie - Examples in Structural Analysis_images/imageFile935.png)

![image 936](McKenzie - Examples in Structural Analysis_images/imageFile936.png)

![image 937](McKenzie - Examples in Structural Analysis_images/imageFile937.png)

![image 938](McKenzie - Examples in Structural Analysis_images/imageFile938.png)

![image 939](McKenzie - Examples in Structural Analysis_images/imageFile939.png)

![image 940](McKenzie - Examples in Structural Analysis_images/imageFile940.png)

![image 941](McKenzie - Examples in Structural Analysis_images/imageFile941.png)

![image 942](McKenzie - Examples in Structural Analysis_images/imageFile942.png)

|6. Buckling Instability<br><br>6.1 Introduction<br><br>|
|---|


Structural elements which are subjected to tensile forces are inherently stable and will generally fail when the stress in the cross-section exceeds the ultimate strength of the material. In the case of elements subjected to compressive forces, secondary bending effects caused by, for example, imperfections within materials and/or fabrication processes, inaccurate positioning of loads or asymmetry of the cross-section, can induce premature failure either in a part of the cross-section, such as the outstand flange of an I section, or of the element as a whole. In such cases the failure mode is normally buckling (i.e. lateral movement), of which there are three main types:

![image 943](McKenzie - Examples in Structural Analysis_images/imageFile943.png)

The design of most compressive members is governed by their overall buckling capacity, i.e. the maximum compressive load which can be carried before failure occurs by excessive deflection in the plane of greatest slenderness.

Typically this occurs in columns in building frames and in trussed frameworks as shown in Figure 6.1.

|![image 944](McKenzie - Examples in Structural Analysis_images/imageFile944.png)<br><br>Figure 6.1<br><br>|
|---|


Compression elements can be considered to be sub-divided into three groups: short elements, slender elements and intermediate elements. Each group is described separately, in Sections 6.1.1, 6.1.2 and 6.1.3 respectively.

|6.1.1 Short Elements|
|---|


Provided that the slenderness of an element is low, e.g. the length is not greater than (10×the least horizontal length), the element will fail by crushing of the material induced by predominantly axial compressive stresses as indicated in Figure 6.2(a). Failure occurs when the stress over the cross-section reaches a yield or crushing value for the material.

###### The failure of such a column can be represented on a stress/slenderness curve as shown in Figure 6.2(b).

|![image 945](McKenzie - Examples in Structural Analysis_images/imageFile945.png)<br><br>Figure 6.2<br><br>6.1.2 Slender Elements<br><br>|
|---|


When the slenderness of an element is high, the element fails by excessive lateral deflection (i.e. buckling) at a value of stress considerably less than the yield or crushing values as shown in Figures 6.3(a) and (b).

|![image 946](McKenzie - Examples in Structural Analysis_images/imageFile946.png)<br><br>Figure 6.3<br><br>6.1.3 Intermediate Elements<br><br>|
|---|


###### The failure of an element which is neither short nor slender occurs by a combination of buckling and yielding/crushing as shown in Figures 6.4(a) and (b).

|![image 947](McKenzie - Examples in Structural Analysis_images/imageFile947.png)<br><br>Figure 6.4<br><br>6.2 Secondary Stresses<br><br>|
|---|


- As mentioned in Section 6.1, buckling is due to small imperfections within materials,

application of load etc., which induce secondary bending stresses which may or may not be significant depending on the type of compression element. Consider a typical column as shown in Figure 6.5 in which there is an actual centre-line, reflecting the variations within the element, and an assumed centre-line along which acts an applied compressive load, assumed to be concentric.

|![image 948](McKenzie - Examples in Structural Analysis_images/imageFile948.png)<br><br>Figure 6.5<br><br>|
|---|


- At any given cross-section the point of application of the load P will be eccentric to the actual centre-line of the cross-section at that point, as shown in Figure 6.6.


|![image 949](McKenzie - Examples in Structural Analysis_images/imageFile949.png)<br><br>Figure 6.6<br><br>|
|---|


The resultant eccentric load produces a secondary bending moment in the crosssection. The cross-section is therefore subject to a combination of an axial stress due to P and a bending stress due to (Pe) where e is the eccentricity from the assumed centre-line as indicated in Figure 6.7.

|![image 950](McKenzie - Examples in Structural Analysis_images/imageFile950.png)<br><br>Figure 6.7<br><br>|
|---|


![image 951](McKenzie - Examples in Structural Analysis_images/imageFile951.png)

The combined axial and bending stress is given by:

where: σ is the combined stress, P is the applied load, e is the eccentricity from the assumed centre-line, A is the cross-sectional area of the section, and Z is the elastic section modulus about the axis of bending.

This equation, which includes the effect of secondary bending, can be considered in terms of each of the types of element

|6.2.1 Effect on Short Elements|
|---|


In short elements the value of the bending stress in the equation is insignificant when

![image 952](McKenzie - Examples in Structural Analysis_images/imageFile952.png)

compared to the axial stress i.e. and consequently the lateral movement and buckling effects can be ignored.

|6.2.2 Effect on Slender Elements|
|---|


In slender elements the value of the axial stress in the equation is insignificant when

![image 953](McKenzie - Examples in Structural Analysis_images/imageFile953.png)

compared to the bending stress i.e. particularly since the eccentricity during buckling is increased considerably due to the lateral deflection; consequently the lateral movement and bending effects determine the structural behaviour.

|6.2.3 Effect on Intermediate Elements|
|---|


Most practical columns are considered to be in the intermediate group and consequently both the axial and bending effects are significant in the column behaviour, i.e. both terms

![image 954](McKenzie - Examples in Structural Analysis_images/imageFile954.png)

in the equation are important.

|6.3 Critical Stress (σcritical)|
|---|


In each case described in Sections 6.2.1 to 6.2.3 the critical load Pc (i.e. critical stress× cross-sectional area) must be estimated for design purposes. Since the critical stress depends on the slenderness it is convenient to quantify slenderness in mathematical terms as:

![image 955](McKenzie - Examples in Structural Analysis_images/imageFile955.png)

where:

LE is the effective buckling length,

![image 956](McKenzie - Examples in Structural Analysis_images/imageFile956.png)

r is the radius of gyration= and I and A are the second moment of area about the axis of bending and the cross-sectional area of the section as before.

|6.3.1 Critical Stress for Short Columns|
|---|


Short columns fail by yielding/crushing of the material and σcritical=Py, the yield stress of the material. If, as stated before, columns can be assumed short when the length is not greater than (10×the least horizontal length) then for a typical rectangular column of

cross-section (b×d) and length L≈10b, a limit of slenderness can be determined as follows:

![image 957](McKenzie - Examples in Structural Analysis_images/imageFile957.png)

From this we can consider that short columns correspond with a value of slenderness less than or equal to approximately 30 to 35.

|6.3.2 Critical Stress for Slender Columns|
|---|


Slender columns fail by buckling and the applied compressive stress σcritical<<Py.

The critical load in this case is governed by the bending effects induced by the lateral deformation.

|6.3.3 Euler Equation|
|---|


In 1757 the Swiss engineer/mathematician Leonhard Euler developed a theoretical analysis of premature failure due to buckling. The theory is based on the differential equation of the elastic bending of a pin-ended column which relates the applied bending moment to the curvature along the length of the column, i.e.

![image 958](McKenzie - Examples in Structural Analysis_images/imageFile958.png)

![image 959](McKenzie - Examples in Structural Analysis_images/imageFile959.png)

where approximates to the curvature of the deformed column.

Since this expression for bending moments only applies to linearly elastic materials, it is only valid for stress levels equal to and below the elastic limit of proportionality. This therefore defines an upper limit of stress for which the Euler analysis is applicable. Consider the deformed shape of the assumed centre-line of a column in equilibrium under the action of its critical load Pc as shown in Figure 6.8.

|![image 960](McKenzie - Examples in Structural Analysis_images/imageFile960.png)<br><br>Figure 6.8<br><br>|
|---|


![image 961](McKenzie - Examples in Structural Analysis_images/imageFile961.png)

The bending moment at position x along the column is equal to and hence Bending Moment

![image 962](McKenzie - Examples in Structural Analysis_images/imageFile962.png)

![image 963](McKenzie - Examples in Structural Analysis_images/imageFile963.png)

This is a 2nd Order Differential Equation of the form:

![image 964](McKenzie - Examples in Structural Analysis_images/imageFile964.png)

The solution of this equation can be shown to be: where: n is 0,1,2,3…etc. EI and L are as before. This expression for Pc defines the Euler Critical Load (PE) for a pin-ended column. The value of n=0 is meaningless since it corresponds to a value of Pc=0. All other values of n correspond to the 1st, 2nd, 3rd…etc. harmonics (i.e. buckling mode shapes) for the sinusoidal curve represented by the differential equation. The first three harmonics are indicated in Figure 6.9.

|![image 965](McKenzie - Examples in Structural Analysis_images/imageFile965.png)<br><br>Figure 6.9—Buckling mode-shapes for pin-ended columns<br><br>|
|---|


The higher level harmonics are only possible if columns are restrained at the appropriate levels, e.g. mid-height point in the case of the 2nd harmonic and the third-height points in the case of the 3rd harmonic.

###### The fundamental critical load (i.e. n=1) for a pin-ended column is therefore given by:

![image 966](McKenzie - Examples in Structural Analysis_images/imageFile966.png)

This fundamental case can be modified to determine the critical load for a column with different end-support conditions by defining an effective buckling length equivalent to that of a pin-ended column.

|6.3.4 Effective Buckling Length (LE)|
|---|


The Euler Critical Load for the fundamental buckling mode is dependent on the buckling length between pins and/or points of contra-flexure as indicated in Figure 6.9. In the case of columns which are not pin-ended, a modification to the boundary conditions when solving the differential equation of bending given previously yields different mode shapes and critical loads as shown in Figure 6.10.

|![image 967](McKenzie - Examples in Structural Analysis_images/imageFile967.png)<br><br>Figure 6.10—Effective Buckling Lengths for Different End Conditions<br><br>|
|---|


The Euler stress corresponding to the Euler Buckling Load for a pin-ended column is given by:

![image 968](McKenzie - Examples in Structural Analysis_images/imageFile968.png)

where (L/r) is the slenderness λ as before.

Note: In practical design it is very difficult to achieve full fixity as assumed for the end conditions. This is allowed for by modifying the effective length coefficients e.g. increasing the value of 0.5L to 0.7L and 0.7L to 0.85L.

A lower limit to the slenderness for which the Euler Equation is applicable can be found by substituting the stress at the proportional limit σ e for σ Euler as shown in the following example with a steel column.

Assume that σ e=200 N/mm2 and that E=205 kN/mm2

![image 969](McKenzie - Examples in Structural Analysis_images/imageFile969.png)

In this case the Euler load is only applicable for values of slenderness≥≈100 and can be represented on a stress/slenderness curve in addition to that determined in Section 6.3.1 for short columns as shown in Figure 6.11.

###### The Euler Buckling Load has very limited direct application in terms of practical design because of the following assumptions and limiting conditions:

- • the column is subjected to a perfectly concentric axial load only,
- • the column is pin-jointed at each end and restrained against lateral loading,
- • the material is perfectly elastic,
- • the maximum stress does not exceed the elastic limit of the material,
- • there is no initial curvature and the column is of uniform cross-section along its


length,

- • lateral deflections of the column are small when compared to the overall length,
- • there are no residual stresses in the column,
- • there is no strain hardening of the material in the case of steel columns,
- • the material is assumed to be homogeneous.


|![image 970](McKenzie - Examples in Structural Analysis_images/imageFile970.png)<br><br>Figure 6.11<br><br>|
|---|


Practical columns do not satisfy these criteria, and in addition in most cases are considered to be intermediate in terms of slenderness.

|6.3.5 Critical Stress for Intermediate Columns<br><br>![image 971](McKenzie - Examples in Structural Analysis_images/imageFile971.png)<br><br>Figure 6.12<br><br>|
|---|


Since the Euler Curve is unsuitable for values of stress greater than the elastic limit it is necessary to develop an analysis which overcomes the limitations outlined above and which can be applied between the previously established slenderness limits (see Figure 6.11) as shown in Figure 6.12.

|6.3.6 Tangent Modulus Theorem|
|---|


Early attempts to develop a relationship for intermediate columns included the Tangent Modulus Theorem. Using this method a modified version of the Euler Equation is adopted to determine the stress/slenderness relationship in which the value of the modulus of elasticity at any given level of stress is obtained from the stress/strain curve for the material and used to evaluate the corresponding slenderness. Consider a column manufactured from a material which has a stress/strain curve as shown in Figure 6.13(a).

|![image 972](McKenzie - Examples in Structural Analysis_images/imageFile972.png)<br><br>Figure 6.13<br><br>|
|---|


The slope of the tangent to the stress/strain curve at a value of stress equal to σ is equal to the value of the tangent modulus of elasticity Et (Note: this is different from the value of

E at the elastic limit). The value of Et can be used in the Euler Equation to obtain a modified slenderness corresponding to the value of stress σ as shown at position ‘x’ in Figure 6.13(b):

![image 973](McKenzie - Examples in Structural Analysis_images/imageFile973.png)

If successive values of λ for values of stress between σ e and σ y are calculated and plotted as shown, then a curve representing the intermediate elements can be developed. This solution still has many of the deficiencies of the original Euler equation.

|6.4 Perry-Robertson Formula|
|---|


The Perry-Robertson Formula was developed to take into account the deficiencies of the Euler equation and other techniques such as the Tangent Modulus Method. This formula evolved from the assumption that all practical imperfections could be represented by a hypothetical initial curvature of the column.

As with the Euler analysis a 2nd Order Differential Equation is established and solved using known boundary conditions, and the extreme fibre stress in the cross-section at mid-height (the assumed critical location) is evaluated. The extreme fibre stress, which includes both axial and bending effects, is then equated to the yield value. Clearly the final result is dependent on the initial hypothetical curvature.

Consider the deformed shape of the assumed centre-line of a column in equilibrium under the action of its critical load Pc and an assumed initial curvature as shown in Figure 6.14.

|![image 974](McKenzie - Examples in Structural Analysis_images/imageFile974.png)<br><br>Figure 6.14<br><br>|
|---|


The bending moment at position x along the column is equal to=−Pc(y+yo)

![image 975](McKenzie - Examples in Structural Analysis_images/imageFile975.png)

![image 976](McKenzie - Examples in Structural Analysis_images/imageFile976.png)

If the initial curvature is assumed to be sinusoidal, then where a is the amplitude of the initial displacement and the equation becomes:

![image 977](McKenzie - Examples in Structural Analysis_images/imageFile977.png)

The solution to this differential equation is:

![image 978](McKenzie - Examples in Structural Analysis_images/imageFile978.png)

The constants A and B are determined by considering the boundary values at the pinned ends, i.e. when x=0 y=0 and when x=L y=0.

###### Substitution of the boundary conditions in the equation gives:

![image 979](McKenzie - Examples in Structural Analysis_images/imageFile979.png)

The value of the stress at mid-height is the critical value since the maximum eccentricity of the load (and hence maximum bending moment) occurs at this position;

![image 980](McKenzie - Examples in Structural Analysis_images/imageFile980.png)

(Note: yo at mid-height is equal to the amplitude a of the assumed initial curvature).

The maximum bending moment

![image 981](McKenzie - Examples in Structural Analysis_images/imageFile981.png)

The maximum combined stress at this point is given by:

![image 982](McKenzie - Examples in Structural Analysis_images/imageFile982.png)

where c is the distance from the neutral axis of the cross-section to the extreme fibres. The maximum stress is equal to the yield value, i.e. σmaximum=σy

![image 983](McKenzie - Examples in Structural Analysis_images/imageFile983.png)

The average stress over the cross-section is the load divided by the area, i.e. (Pc/A)

![image 984](McKenzie - Examples in Structural Analysis_images/imageFile984.png)

![image 985](McKenzie - Examples in Structural Analysis_images/imageFile985.png)

The (ac/r2) term is dependent upon the assumed initial curvature and is normally given the symbol η.

![image 986](McKenzie - Examples in Structural Analysis_images/imageFile986.png)

This equation can be rewritten as a quadratic equation in terms of the average stress:

![image 987](McKenzie - Examples in Structural Analysis_images/imageFile987.png)

The solution of this equation in terms of σaverage is:

![image 988](McKenzie - Examples in Structural Analysis_images/imageFile988.png)

This equation represents the average value of stress in the cross-section which will induce the yield stress at mid-height of the column for any given value of η. Experimental evidence obtained by Perry and Robertson indicated that the hypothetical initial curvature of the column could be represented by;

|![image 989](McKenzie - Examples in Structural Analysis_images/imageFile989.png)|
|---|


which was combined with a load factor of 1.7 and used for many years in design codes to determine the critical value of average compressive stress below which overall buckling would not occur. The curve of stress/slenderness for this curve is indicated in Figure 6.15 for comparison with the Euler and Tangent Modulus solutions.

![image 990](McKenzie - Examples in Structural Analysis_images/imageFile990.png)

###### Figure 6.15

|6.5 European Column Curves|
|---|


Whilst the Perry-Robertson formula does take into account many of the deficiencies of the Euler and Tangent Modulus approaches, it does not consider all of the factors which influence the failure of columns subjected to compressive stress. In the case of steel columns for example, the effects of residual stresses induced during fabrication, the type of section being considered (i.e. the cross-section shape), the material thickness, the axis of buckling, the method of fabrication (i.e. rolled or welded), etc. are not allowed for.

A more realistic formula of the critical load capacity of columns has been established following extensive full-scale testing both in the UK and in other European countries. The Perry-Robertson formula has in effect been modified and is referred to in design codes as the Perry strut formula and is given in the following form:

![image 991](McKenzie - Examples in Structural Analysis_images/imageFile991.png)

from which the value of pc may be obtained using:

|![image 992](McKenzie - Examples in Structural Analysis_images/imageFile992.png)|
|---|


where:

py is the design strength λ is the slenderness The Perry factor η for flexural buckling under axial force should be taken as:

|![image 993](McKenzie - Examples in Structural Analysis_images/imageFile993.png)|
|---|


λ0 is the limiting slenderness below which it can be assumed that buckling will not occur.

The European Column curves are indicated in graphical form in Figure

- 6.16.


The Robertson constant a should be taken as 2.0, 3.5, 5.5 or 8.0 as indicated in design codes depending on the cross-section, thickness of material, axis of buckling and method of fabrication.

|![image 994](McKenzie - Examples in Structural Analysis_images/imageFile994.png)<br><br>Figure 6.16<br><br>|
|---|


Typically, the values of ‘a’ are allocated to various cross-sections as indicated in Table 6.1.

||Type of section|
|---|
||Maximum thickness (see Note 1)<br><br>|
|---|
<br><br>||Robertson’s constant ‘a’<br><br>|
|---|
| |
|---|---|---|---|
| | ||Axis of buckling|
|---|
| |
| | | | |
| | |x-x|y-y|
| | | | |
|Hot finished structural hollow section| |2.0|2.0|
|Cold-formed structural section| |5.5|5.5|
|Rolled I-section|≤40mm >40mm|2.0 3.5|3.5 5.5|


|Rolled H-section|≤40mm >40mm|3.5 5.5|5.5 8.0|
|---|---|---|---|
|Welded I or H-section (see Notes 2 and 4)|≤40mm >40mm|3.5 3.5|5.5 8.0|
|Rolled I-section with welded flange cover plates 0.25<U/B<0.8 (see Figure 6.17a)|≤40mm >40mm|2.0 3.5|3.5 5.5|
|Rolled H-section with welded flange cover plates 0.25<U/B<0.8 (see Figure 6.17a)|≤40 mm >40mm|3.5 5.5|5.5 8.0|
|Rolled I or H-section with welded flange cover plates U/B≥0.8 (see Figure 6.17b)|≤40 mm >40mm|3.5 5.5|2.0 3.5|
|Rolled I or H-section with welded flange cover plates U/B≤0.25 (see Figure 6.17c)|≤40 mm >40mm|3.5 3.5|5.5 8.0|
|Welded box section (see Notes 3 and 4)|≤40 mm >40 mm|3.5 5.5|3.5 5.5|
|Round, square or flat bar|≤40 mm >40mm|3.5 5.5|3.5 5.5|
|Rolled angle, channel or T-section Two rolled sections laced, battened or back-to-back Compound rolled sections| |Any axis: a=5.5| |


- Note 1 : For thicknesses between 40 mm and 50 mm the value of pc may

be taken as the average of the values for thicknesses up to 40 mm and over 40 mm for the relevant value of py.

- Note 2 For welded I or H-sections with their flanges thermally cut by machine without subsequent edge grinding or machining, for buckling


about the y-y axis, a=3.5 for flanges up to 40 mm thick and a=5.5 for flanges over 40 mm thick.

Note 3 The category ‘welded box section’ includes any box section fabricated from plates or rolled sections, provided that all of the longitudinal welds are near the corners of the cross-section. (This is to avoid areas in the cross-section which have locked in residual compressive stresses which induce premature failure at a reduced buckling strength). Box sections with longitudinal stiffeners are NOT included in this category.

Note 4 For welded I, H or box sections pc should be obtained from the Perry strut formula using a py value 20 N/mm2 below the normally assigned value. (This is a simplification to avoid the use of a different set of curves which are required for fabricated sections).

|Table 6.1<br><br>![image 995](McKenzie - Examples in Structural Analysis_images/imageFile995.png)<br><br>Figure 6.17<br><br>|
|---|


The design of the majority of concrete and timber column members is usually based on square, rectangular or circular cross-sections, similarly with masonry columns square or rectangular sections are normally used. In the case of structural steelwork there is a wide variety of cross-sections which are adopted, the most common of which are shown in Figure 6.18.

|![image 996](McKenzie - Examples in Structural Analysis_images/imageFile996.png)<br><br>Figure 6.18<br><br>|
|---|


In all cases, irrespective of the material or member cross-section, an assessment of end and intermediate restraint conditions must be made in order to estimate effective buckling lengths (LE) and hence slenderness λ. It is important to recognise that the effective buckling length is not necessarily the same about all axes. Typically, it is required to determine two LE and λ values (e.g. LEy, λy and LEx, λx), and subsequently determine the critical compressive stress relating to each one; the lower value being used to calculate the compressive resistance of a member. In the case of angle sections other axes are also

considered. The application of the Perry strut formula to various steel columns is illustrated in Examples 6.1 to 6.4 and Problems 6.1 to 6.5.

|6.6 Example 6.1 Slenderness|
|---|


The square column section shown in Figure 6.19 is pinned about both the x-x, and y-y axes at the top and fixed about both axis at the bottom. An additional restraint is to be provided to both axes at a height of L1 above the base. Determine the required value of L1 to optimize the compression resistance of the section.

|![image 997](McKenzie - Examples in Structural Analysis_images/imageFile997.png)<br><br>Figure 6.19<br><br>6.7 Example 6.2 Rolled UC Section<br><br>|
|---|


A column, which is subjected to a concentric axial load ‘P’, is shown in Figure 6.20. Restraint against lateral movement, but not rotation, is provided about both axes at the top and the bottom of the column. Additional lateral restraint is also provided about the yy axis at mid-height as shown.

###### Using the data provided determine the compression resistance of the column using the Perry strut formula.

|![image 998](McKenzie - Examples in Structural Analysis_images/imageFile998.png)<br><br>Figure 6.20<br><br>|
|---|


Data:

|![image 999](McKenzie - Examples in Structural Analysis_images/imageFile999.png)|
|---|


###### Perry strut formula:

Solution:

|![image 1000](McKenzie - Examples in Structural Analysis_images/imageFile1000.png)|
|---|


![image 1001](McKenzie - Examples in Structural Analysis_images/imageFile1001.png)

|![image 1002](McKenzie - Examples in Structural Analysis_images/imageFile1002.png)|
|---|
|6.8 Example 6.3 Laced Section<br><br>|


A column comprising two Universal Beam sections laced together to act compositely is shown in Figure 6.21. The restraints to lateral movement about both the A-A and B-B axes are as indicated. Using the data given determine the compressive resistance of the section using the Perry strut formula.

Data:

| | |
|---|---|
|Section Property|Section|
| | |
| | |
| |533×210×82 UB Universal Beam<br><br>|
| | |
|Cross-sectional Area (A)|105 cm2|
|Radius of Gyration (ryy)|4.38 cm|
|Radius of Gyration (rxx)|21.3 cm|
|2nd Moment of Area (Ixx)|47500 cm4|
|2nd Moment of Area (Iyy)|2010 cm4|


|Yeild Stress Py=275 N/mm2|
|---|


Young’s Modulus E=205 kN/mm2

Robertson Constants:

- x-x axis a=5.5
- y-y axis a=5.5


Solution:

|![image 1003](McKenzie - Examples in Structural Analysis_images/imageFile1003.png)<br><br>Figure 6.21<br><br>|
|---|


###### Composite Section Properties:

|![image 1004](McKenzie - Examples in Structural Analysis_images/imageFile1004.png)|
|---|


The possibility of buckling of the individual UB sections and the composite section must be considered in this problem as follows:

(Extract from to BS 5950–1:2000 Structural Use of Steelwork in Building) “The slenderness λc of the main components (based on their minimum radius of gyration) between consecutive points where the lacing is attached should not exceed 50. If the overall slenderness of the member is less than 1.4λc the design should be based on a slenderness of 1.4λc.” Perry strut formula:

|![image 1005](McKenzie - Examples in Structural Analysis_images/imageFile1005.png)|
|---|


Note: Since the same curve is used for both the A-A and the B-B axes in this case (i.e. a=5.5), the compression resistance will correspond to the axis with the highest slenderness value, i.e. the one which produces the lowest pc value.

|![image 1006](McKenzie - Examples in Structural Analysis_images/imageFile1006.png)|
|---|


Consider an individual UB section:

|![image 1007](McKenzie - Examples in Structural Analysis_images/imageFile1007.png)|
|---|


Consider the composite section:

![image 1008](McKenzie - Examples in Structural Analysis_images/imageFile1008.png)

|![image 1009](McKenzie - Examples in Structural Analysis_images/imageFile1009.png)|
|---|


Consider the B-B axis:

|![image 1010](McKenzie - Examples in Structural Analysis_images/imageFile1010.png)|
|---|


Since 1.4λc is the largest value this should be used to determine the value of pc using the Perry strut formula.

|![image 1011](McKenzie - Examples in Structural Analysis_images/imageFile1011.png)|
|---|


![image 1012](McKenzie - Examples in Structural Analysis_images/imageFile1012.png)

![image 1013](McKenzie - Examples in Structural Analysis_images/imageFile1013.png)

Compression resistance

A similar approach is taken when designing battened struts, the corresponding Clause in BS 5950–1:2000 Structural Use of Steelwork in Building is as follows:

“The slenderness λc of a main component (based on its minimum radius of gyration) between end welds or end bolts of adjacent battens should not exceed 50. The slenderness λb of the battened strut about the axis perpendicular to the plane of the battens should be calculated from:

|![image 1014](McKenzie - Examples in Structural Analysis_images/imageFile1014.png)|
|---|


where λm is the ratio LE/r of the whole member about that axis. If λb is less than 1.4λc the design should be based on λb=1.4λc. ”

The application of this is illustrated in the solution to Problem 7.5.

|6.9 Example 6.4 Compound Section|
|---|


A column ABCE of a structure is shown in Figure 6.22. The column is 15.0 m long and supports a roof beam DEF at E. The beam carries a load of w kN/m length along its full length DEF. The column is fabricated from a 152×152×23 UC with plates welded continuously to the flanges as shown. Using the data given determine:

|(i) the compression resistance of the column, and<br><br>(ii) the maximum value of w which can be supported.<br><br><br>|
|---|


Data:

| | | |
|---|---|---|
|Section Property|Section| |
| | | |
| |152×152×23 UB Universal Beam<br><br>|Yield Stress py=275 N/mm2<br><br>|
| | |Young’s Modulus E=205 kN/mm2<br><br>Robertson Constants:<br><br>x-x axis a=5.5<br>y-y axis a=5.5<br>|
|Cross-sectional Area (A)|29.2 cm2| |
|Radius of Gyration (ryy)|3.70 cm| |
|Radius of Gyration (rxx)|6.54 cm| |
|2nd Moment of Area (Ixx)|1250 cm4| |
|2nd Moment of Area (Iyy)|400 cm4| |


|![image 1015](McKenzie - Examples in Structural Analysis_images/imageFile1015.png)<br><br>Figure 6.22<br><br>|
|---|


Solution:

(i)

|![image 1016](McKenzie - Examples in Structural Analysis_images/imageFile1016.png)|
|---|


Perry strut formula:

|![image 1017](McKenzie - Examples in Structural Analysis_images/imageFile1017.png)|
|---|


Note: Since the same curve is used for both the A-A and the B-B axes in this case (i.e. a=5.5), the compression resistance will correspond to the axis with the highest slenderness value, i.e. the one which produces the lowest pc value.

###### Consider the A-A axis:

|![image 1018](McKenzie - Examples in Structural Analysis_images/imageFile1018.png)|
|---|


###### Consider the B-B axis:

|![image 1019](McKenzie - Examples in Structural Analysis_images/imageFile1019.png)|
|---|


Since λA-A is the largest value this should be used to determine the value of pc using the Perry strut formula.

|![image 1020](McKenzie - Examples in Structural Analysis_images/imageFile1020.png)|
|---|


Critical value of pc=80.28 N/mm2

Compression resistance Pc=(pc×Ag)=(80.28×6.92×103)/103=555.5 kN (ii)

|![image 1021](McKenzie - Examples in Structural Analysis_images/imageFile1021.png)<br><br>Figure 6.23<br><br>|
|---|


The maximum value of the vertical reaction at E=555.5 kN

|![image 1022](McKenzie - Examples in Structural Analysis_images/imageFile1022.png)|
|---|
|6.10 Problems: Buckling Instability<br><br>|


A selection of column cross-sections is indicated in Problems 6.1 to 6.7 in addition to the position of the restraints about the x-x and y-y axes. Using the data given and the equation for the European Column Curves, (the Perry strut formula) determine the value of the compressive strength pc and hence the compression resistance, for each section.

Data:

|Table 6.2- Section Property Data|
|---|


| | | | | |
|---|---|---|---|---|
|Problem No.|py (N/mm2)|E (kN/mm2)|Robertson Constant| |
| | | | | |
| | | | ||y-y|
|---|
|
| | | |x-x| |
| | | | | |
|6.1|275|205|3.5|2.0|
|6.2|255|205|3.5|3.5|
|6.3|275|205|5.5|5.5|
|6.4|255|205|3.5|3.5|
|6.5|275|205|5.5|5.5|
|6.6|275|205|5.5|5.5|
|6.7|255|205|5.5|5.5|


|Table 6.3- Section Pro perty Data|
|---|


||Section Property<br><br>|
|---|
| | | | |
|---|---|---|---|---|
| |Section| | | |
| | | | | |
| | | | ||150×100×10 Hollow Section<br><br>|
|---|
|
| |533×210×82 UB<br><br>|457×152×52 UB<br><br>|200×90×30 Channel<br><br>| |
| | | | | |
|Overall Depth (D)|528.3 mm|449.8 mm|200.0 mm|100.0 mm|
|Overall Breadth (B)|208.8 mm|152.4 mm|90.0 mm|50.0 mm|
|Crosssectional Area (A)|105 cm2|66.6 cm2|37.9 cm2|42.6 cm2|
|Radius of Gyration (ryy)|–|–|2.88 cm|3.01 cm|
|2ndMoment of Area (Ixx)|47500 cm4|21400 cm4|2520 cm4|1160.0 cm4|
|2nd Moment of Area (Iyy)|2010 cm4|645 cm4|314 cm4|614.0 cm4|


|![image 1023](McKenzie - Examples in Structural Analysis_images/imageFile1023.png)<br><br>Problem 6.1<br><br>![image 1024](McKenzie - Examples in Structural Analysis_images/imageFile1024.png)<br><br>Problem 6.2<br><br>![image 1025](McKenzie - Examples in Structural Analysis_images/imageFile1025.png)<br><br>Problem 6.3<br><br><br>|
|---|


![image 1026](McKenzie - Examples in Structural Analysis_images/imageFile1026.png)

###### Problem 6.4

![image 1027](McKenzie - Examples in Structural Analysis_images/imageFile1027.png)

###### Problem 6.5

![image 1028](McKenzie - Examples in Structural Analysis_images/imageFile1028.png)

###### Problem 6.6

![image 1029](McKenzie - Examples in Structural Analysis_images/imageFile1029.png)

- Problem 6.7


#### 6.11 Solutions: Buckling Instability

![image 1030](McKenzie - Examples in Structural Analysis_images/imageFile1030.png)

|![image 1031](McKenzie - Examples in Structural Analysis_images/imageFile1031.png)|
|---|


|![image 1032](McKenzie - Examples in Structural Analysis_images/imageFile1032.png)|
|---|


|![image 1033](McKenzie - Examples in Structural Analysis_images/imageFile1033.png)|
|---|


|![image 1034](McKenzie - Examples in Structural Analysis_images/imageFile1034.png)|
|---|


|![image 1035](McKenzie - Examples in Structural Analysis_images/imageFile1035.png)|
|---|


|![image 1036](McKenzie - Examples in Structural Analysis_images/imageFile1036.png)|
|---|


|![image 1037](McKenzie - Examples in Structural Analysis_images/imageFile1037.png)|
|---|


|![image 1038](McKenzie - Examples in Structural Analysis_images/imageFile1038.png)|
|---|


|![image 1039](McKenzie - Examples in Structural Analysis_images/imageFile1039.png)|
|---|


|![image 1040](McKenzie - Examples in Structural Analysis_images/imageFile1040.png)|
|---|


|![image 1041](McKenzie - Examples in Structural Analysis_images/imageFile1041.png)|
|---|


|![image 1042](McKenzie - Examples in Structural Analysis_images/imageFile1042.png)|
|---|


|![image 1043](McKenzie - Examples in Structural Analysis_images/imageFile1043.png)|
|---|


|![image 1044](McKenzie - Examples in Structural Analysis_images/imageFile1044.png)|
|---|


![image 1045](McKenzie - Examples in Structural Analysis_images/imageFile1045.png)

### 7. Direct Stiffness Method

#### 7.1 Direct Stiffness Method of Analysis

The ‘stiffness’ method of analysis is a matrix technique on which most structural computer analysis programs are based. There are two approaches; the indirect and the direct methods. The direct method as illustrated in this chapter requires the visual recognition of the relationship between structural forces/displacements and the consequent element forces/displacements induced by the applied load system. The indirect method is primarily for use in the development of computer programs to enable the automatic correlation between these displacements.

Neither method is regarded as a hand-analysis. The direct method is included here to enable the reader to understand the concepts involved and the procedure which is undertaken during a computer analysis. The examples and problems used to illustrate these concepts have been restricted to rigid-jointed structures assuming axially-rigid elements. In addition, the structures have been limited to having no more than three degrees-of-freedom and do not have any sloping members. In both methods it is necessary to develop element stiffness matrices, related to an element (local) co-ordinate system and a structural stiffness matrix related to a global co-ordinate system. The development of these matrices and coordinate systems is explained in Sections 7.2 and 7.3.

#### 7.2 Element Stiffness Matrix [k]

One of the fundamental characteristics governing the behaviour of elastic structures is the relationship between the applied loads and the displacements which these induce. This can be expressed as:

![image 1046](McKenzie - Examples in Structural Analysis_images/imageFile1046.png)

where:

[F] is a vector representing the forces acting on an element at its nodes i.e. the (element end forces vector),

[k] is the element stiffness matrix relating to the degrees-of-freedom at the nodes relative to the local co-ordinate system,

[δ] is a vector representing the displacements (both translational and rotational) of the element at its nodes relative to the local axes co-ordinate system (element displacement vector).

Considering an element with only one degree-of-freedom, the matrix and vectors can be re-written as leading to a definition of stiffness as: "The force necessary to maintain a ‘unit’ displacement.”

![image 1047](McKenzie - Examples in Structural Analysis_images/imageFile1047.png)

The ‘axial’ stiffness of a column as shown in Figure 7.1, can be derived from the standard relationship between the elastic modulus, stress and strain as follows:

![image 1048](McKenzie - Examples in Structural Analysis_images/imageFile1048.png)

Elastic Modulus. This equation can be re-arranged to give:

![image 1049](McKenzie - Examples in Structural Analysis_images/imageFile1049.png)

![image 1050](McKenzie - Examples in Structural Analysis_images/imageFile1050.png)

- Figure 7.1


|hence when δ=1.0 (i.e. unit displacement) then the force stiffness<br><br>![image 1051](McKenzie - Examples in Structural Analysis_images/imageFile1051.png)<br><br>7.2.1 Beam Elements with Two Degrees-of-Freedom<br><br>Consider a ‘beam element’ of length L, Young’s Modulus E and cross-sectional area A which is subject to axial forces F1 and F2 at the end nodes A and B as shown in Figure 7.2.<br><br>![image 1052](McKenzie - Examples in Structural Analysis_images/imageFile1052.png)<br><br>Figure 7.2<br><br>Assume that node A is displaced a distance of δ1 in the direction of the longitudinal axis (i.e. the x-direction) and similarly node B is displaced a distance of δ2 as shown in Figure 7.3.<br><br>![image 1053](McKenzie - Examples in Structural Analysis_images/imageFile1053.png)<br><br>Figure 7.3The force/displacement relationships for this element are:<br><br>|
|---|
|![image 1054](McKenzie - Examples in Structural Analysis_images/imageFile1054.png)|
|Considering equilibrium in the x direction:<br><br>|
|![image 1055](McKenzie - Examples in Structural Analysis_images/imageFile1055.png)|
|These two equations can be expanded and written in the form:<br><br>|
|![image 1056](McKenzie - Examples in Structural Analysis_images/imageFile1056.png)<br><br>Equation|


(1)

![image 1057](McKenzie - Examples in Structural Analysis_images/imageFile1057.png)

Equation

(2)

![image 1058](McKenzie - Examples in Structural Analysis_images/imageFile1058.png)

where [k] is the element stiffness matrix.

This element stiffness matrix [k] representing two-degrees-of-freedom is adequate for pinjointed structures in which it is assumed that elements are subject to purely axial loading.

###### 7.2.2 Beam Elements with Four Degrees-of-Freedom

In the case of rigid-jointed plane-frame structures, the loading generally consists of axial, shear and bending forces, the effects of which must be determined by the axial, shear and bending effects on the elements. Consider a beam element with the following properties:

![image 1059](McKenzie - Examples in Structural Analysis_images/imageFile1059.png)

which is assumed to be axially rigid, (i.e. neglect axial deformations), and has fourdegrees-of-freedom as indicated in Figure 7.4.

![image 1060](McKenzie - Examples in Structural Analysis_images/imageFile1060.png)

- Figure 7.4


When this element is displaced within a structure each node will displace in a vertical direction and rotate as indicated in Figure 7.5, where δ1 to δ4 are the nodal displacements.

![image 1061](McKenzie - Examples in Structural Analysis_images/imageFile1061.png)

- Figure 7.5 The forces induced in this element by the loaded structure, and which maintain its’

displaced form can be represented by the element end forces F1 to F4 as shown in Figure 7.6.

![image 1062](McKenzie - Examples in Structural Analysis_images/imageFile1062.png)

- Figure 7.6


The element end-forces can be related to the element end-displacements as in the previous case giving;

![image 1063](McKenzie - Examples in Structural Analysis_images/imageFile1063.png)

|where k11, k12, k13 etc. are the stiffness coefficients for the element.<br><br>The displacement configuration in Figure 7.5 can be considered as consisting of the superposition of four independent displacements each having only one degree-of-freedom as shown in Figure 7.8.<br><br>Similarly the element end-forces can be represented as the superposition of four sets of forces, each of which is required to maintain a displaced form as indicated in Figure 7.9<br><br>The values of k1,1, k2,1, k3,1 and k4,1 (which represent the forces necessary to maintain a unit displacement) can be evaluated using an elastic method of analysis such as McCaulay’s Method, (see Chapter 4, Section 4.2).<br><br>Consider the case in which a unit displacement is applied in direction δ1, (i.e. the slope at A=−1.0) as shown in Figure 7.7.<br><br>![image 1064](McKenzie - Examples in Structural Analysis_images/imageFile1064.png)<br><br>Figure 7.7<br><br>|
|---|


![image 1065](McKenzie - Examples in Structural Analysis_images/imageFile1065.png)

![image 1066](McKenzie - Examples in Structural Analysis_images/imageFile1066.png)

e.g. F1={(k1,1 δ1)+(k1,2 δ2)+(k1,3 δ3)+(k1,4 δ4)}

|The bending moment at any position ‘x’ along the element can be expressed as:|
|---|


![image 1067](McKenzie - Examples in Structural Analysis_images/imageFile1067.png)

Equation

- (1)

|![image 1068](McKenzie - Examples in Structural Analysis_images/imageFile1068.png)<br><br>Equation<br><br>(2)|
|---|


![image 1069](McKenzie - Examples in Structural Analysis_images/imageFile1069.png)

Equation

(3)

|![image 1070](McKenzie - Examples in Structural Analysis_images/imageFile1070.png)<br><br>Substitute for x and θ in equation (2): (x=0, θ=−1.0)<br><br>|
|---|


![image 1071](McKenzie - Examples in Structural Analysis_images/imageFile1071.png)

Equation

- (2a)

|Substitute for x and δ in equation (3): (x=0, δ=0)|
|---|


![image 1072](McKenzie - Examples in Structural Analysis_images/imageFile1072.png)

Equation

- (3a)

|Re-write equations (2a) and (3a):|
|---|


![image 1073](McKenzie - Examples in Structural Analysis_images/imageFile1073.png)

Equation

- (4)


|![image 1074](McKenzie - Examples in Structural Analysis_images/imageFile1074.png)<br><br>Equation<br><br>(5)<br><br>Substitute for x and θ in equation (4): (x=L, θ=0)<br><br>|
|---|


![image 1075](McKenzie - Examples in Structural Analysis_images/imageFile1075.png)

Equation

- (6)

|Substitute for x and δ in equation (5): (x=L, δ=0)|
|---|


![image 1076](McKenzie - Examples in Structural Analysis_images/imageFile1076.png)

Equation

- (7)


|Solving equations (6) and (7) simultaneously and evaluating ΣM=0, ΣFy=0 gives:|
|---|


![image 1077](McKenzie - Examples in Structural Analysis_images/imageFile1077.png)

|A similar analysis considering the other three unit displacement diagrams produces the following values for the element stiffness matrix coefficients:<br><br>|
|---|


![image 1078](McKenzie - Examples in Structural Analysis_images/imageFile1078.png)

|where:<br><br>E is Young’s Modulus, I is the Second Moment of area of the cross-section and L is the length of the member.<br><br>|
|---|


|This is the ‘element stiffness matrix’ for a beam element with four degrees-of-freedom as indicated in Figure 7.10<br><br>![image 1079](McKenzie - Examples in Structural Analysis_images/imageFile1079.png)<br><br>Figure 7.10<br><br>7.2.3 Local Co-ordinate System<br><br>The co-ordinate system defining the positive directions for the element end displacements and the corresponding end forces is known as the ‘local co-ordinate system.’ A typical local co-ordinate system for axially rigid elements in a frame is shown in Figure 7.11.<br><br>![image 1080](McKenzie - Examples in Structural Analysis_images/imageFile1080.png)<br><br>Figure 7.11<br><br>7.2.4 Beam Elements with Six Degrees-of-Freedom<br><br>A typical computer analysis program for plain frame elements in rigid-jointed frames uses beam elements with six degrees-of-freedom as shown in Figure 7.12.<br><br>![image 1081](McKenzie - Examples in Structural Analysis_images/imageFile1081.png)<br><br>Figure 7.12 The resulting stiffness matrix for such elements is:<br><br><br>|
|---|


![image 1082](McKenzie - Examples in Structural Analysis_images/imageFile1082.png)

|The values of the stiffness coefficients are as determined in Sections 7.2.1 and 7.2.2, combining the effects of both the two and four degree-of-freedom cases. The order in which the values appear in the matrix is dependent on the numerical order defined in the local co-ordinate system, see Figure 7.12.<br><br>|
|---|


![image 1083](McKenzie - Examples in Structural Analysis_images/imageFile1083.png)

|It is evident from the stiffness matrices developed in each case that they are symmetrical about the main diagonal. (this is a consequence of Maxwell’s Reciprocal Theorem). The elements in matrices represent the force systems necessary to maintain unit displacements as indicated in Figure 7.9.<br><br>The element stiffness matrices must be modified to accommodate the orientation of any elements which are not parallel to the ‘global coordinate system’, see Section 7.3. This is achieved by applying ‘transformation matrices’ such that:<br><br>|
|---|


![image 1084](McKenzie - Examples in Structural Analysis_images/imageFile1084.png)

|where [T] is the transformation matrix relating the rotation of the element to the global axis system. This is not considered further in this text.<br><br>7.3 Structural Stiffness Matrix [K]<br><br>The stiffness matrix for an entire structure is dependent on the number of structural degrees-of-freedom which corresponds with the nodal (i.e. joint) displacements, e.g. consider the structures indicated in Figure 7.13, (Note: assuming axial rigidity).<br><br>![image 1085](McKenzie - Examples in Structural Analysis_images/imageFile1085.png)<br><br>Figure 7.13<br><br>|
|---|


|Each level of the frame can sway independently of the others and consequently there are three degrees-of-freedom due to sway (i.e. translation). In addition all of the internal joints can rotate producing nine degrees-of-freedom due to rotation.<br><br>Three of the supports can rotate whilst one i.e. the roller can also move horizontally. The total number of degrees-of-freedom when the frame is assumed to be axially rigid is equal to SIXTEEN.<br><br>When the axial deformations of the members is also included the number of degrees-offreedom increases to THIRTY ONE.<br><br>In order to generate a structural stiffness matrix and complete the subsequent analysis it is necessary to establish a global co-ordinate system which defines the positions of the nodes and their displacements. The global co-ordinate system is also used to define the positive directions of the applied load system.<br><br>Consider a portal frame having three degrees-of-freedom as indicated in Figure 7.14.<br><br>![image 1086](McKenzie - Examples in Structural Analysis_images/imageFile1086.png)<br><br>Figure 7.14<br><br>The nodal displacements in the structure can be related to the applied structural loads in the same way as those for the elements, i.e.<br><br>|
|---|


![image 1087](McKenzie - Examples in Structural Analysis_images/imageFile1087.png)

|where:<br><br>[P] is a vector representing the equivalent nodal loads applied to the structure (see Section 7.3) relative to the global axes—(structural load vector),<br><br>[K] is the structural stiffness matrix relating to the degrees-of-freedom at the nodes relative to the global axes,<br><br>[∆] is a vector representing the displacements (both translational and rotational) of the structure at its nodes relative to the global axes,(structural displacement vector).<br><br>The coefficients for the structural stiffness matrix (i.e. K1,1, K1,2, K1,3 etc.) can be determined by evaluating the forces necessary to maintain unit displacements for each of the degrees-of-freedom in turn; in a similar manner to the element stiffness matrices.<br><br>Consider the uniform rectangular portal frame shown in Figure 7.15 which supports a number of loads as indicated.<br><br>![image 1088](McKenzie - Examples in Structural Analysis_images/imageFile1088.png)<br><br>Figure 7.15<br><br>The structural displacements are as indicated in Figure 7.16 (assuming axially rigid members).<br><br>|
|---|


![image 1089](McKenzie - Examples in Structural Analysis_images/imageFile1089.png)

###### Figure 7.16

![image 1090](McKenzie - Examples in Structural Analysis_images/imageFile1090.png)

|Consider Δ3=1.0 ∆1=Δ2=Δ4=0|
|---|


![image 1091](McKenzie - Examples in Structural Analysis_images/imageFile1091.png)

|Consider Δ4=1.0 Δ1=Δ2=Δ3=0|
|---|


![image 1092](McKenzie - Examples in Structural Analysis_images/imageFile1092.png)

|![image 1093](McKenzie - Examples in Structural Analysis_images/imageFile1093.png)<br><br>In each case the size of the structural stiffness matrix is the same as the number of degree-of-freedom.<br><br>7.4 Structural Load Vector [P]<br><br>In most cases the loading applied to a structure occurs within, or along the length of the elements. Since only nodal loads are used in this analysis, the applied loading must be represented as ‘equivalent nodal loads’ corresponding to the degrees-of-freedom of the structure. This is easily carried out by replacing the actual load system by a set of forces equal in magnitude and opposite in direction to the ‘fixed-end forces.’<br><br>The Tixed-end forces’ due to the applied loads are calculated for each applied load case and only those which correspond to structural degreesof-freedom are subsequently used to develop the structural load vector as shown in Figures 7.17. to 7.19.<br><br>![image 1094](McKenzie - Examples in Structural Analysis_images/imageFile1094.png)<br><br>Figure 7.17<br><br>|
|---|


|The structural displacements and equivalent nodal load system are as indicated in Figure 7.18, (assuming axially rigid members).<br><br>![image 1095](McKenzie - Examples in Structural Analysis_images/imageFile1095.png)<br><br>Figure 7.18 The equivalent nodal loads can be determined as follows:<br><br>![image 1096](McKenzie - Examples in Structural Analysis_images/imageFile1096.png)<br><br>Figure 7.19<br><br><br>|
|---|
|![image 1097](McKenzie - Examples in Structural Analysis_images/imageFile1097.png)|
|7.5 Structural Displacement Vector [A]<br><br>The structural displacement vector can be determined from the product of the inverse of the structural stiffness matrix and the structural load vector, i.e.<br><br>|


![image 1098](McKenzie - Examples in Structural Analysis_images/imageFile1098.png)

#### 7.6 Element Displacement Vector [δ]

An element displacement vector is required for each element and is dependent on the relationship between the structural displacements and the element nodal displacements in each case. The structural displacements in terms of the global co-ordinate system and the individual element displacements in terms of their local co-ordinate systems are shown in Figure 7.20.

![image 1099](McKenzie - Examples in Structural Analysis_images/imageFile1099.png)

###### Figure 7.20

![image 1100](McKenzie - Examples in Structural Analysis_images/imageFile1100.png)

In the direct stiffness method the correlation between the structural displacements and the element displacements is carried out visually by inspection as indicated above.

|7.7 Element Force Vector [F]Total<br><br>The element end-forces due to the structural displacements can be related to the element end-displacements as indicated in Section 7.2.2.<br><br>|
|---|
|![image 1101](McKenzie - Examples in Structural Analysis_images/imageFile1101.png)|
|The total nodal forces developed at the nodes are given by:<br><br>|
|[F]Total=[F]+[Fixed-End Forces]|
|![image 1102](McKenzie - Examples in Structural Analysis_images/imageFile1102.png)<br><br>7.8 Example 7.1: Two-span Beam<br><br>Consider a uniform two-span beam ABC which is fully-fixed at supports A and C and<br><br>simply supported at B as indicated in Figure 7.21. A uniformly distributed load of 24 kN/m is applied to span AB and a central point load of 24 kN is applied to span BC as shown.<br><br>Using the data given, the degrees-of-freedom indicated and assuming both members to be axially rigid,<br><br>|
|(i) generate the structural stiffness matrix [K] and the applied load vector [P],<br><br>(ii) determine the structural displacements,<br><br>(iii) determine the member end forces and the support reactions,<br><br>(iv) sketch the shear force and bending moment diagrams,<br><br><br>|


|(v) sketch the deflected shape.|
|---|
|![image 1103](McKenzie - Examples in Structural Analysis_images/imageFile1103.png)<br><br>Figure 7.21 Solution:<br><br>To develop the structural stiffness matrix each degree-of-freedom is given a unit displacement in turn and the forces (corresponding to all degrees-of-freedom) necessary to maintain the displaced shape are determined. In this case there is only one degree-offreedom and hence the stiffness matrix comprises one element.<br><br>![image 1104](McKenzie - Examples in Structural Analysis_images/imageFile1104.png)<br><br>![image 1105](McKenzie - Examples in Structural Analysis_images/imageFile1105.png)<br><br>The stiffness matrix [K]=[k11]=[1.34EI]<br><br>The inverse of the stiffness matrix Structural Load Vector [P]:<br><br>![image 1106](McKenzie - Examples in Structural Analysis_images/imageFile1106.png)<br><br>The structural load vector comprises coefficients equal in magnitude and opposite in direction to the fixed-end forces which correspond to the structural degrees-of-freedom. In this case, only the moment at joint B is required.<br><br>|


![image 1107](McKenzie - Examples in Structural Analysis_images/imageFile1107.png)

![image 1108](McKenzie - Examples in Structural Analysis_images/imageFile1108.png)

|![image 1109](McKenzie - Examples in Structural Analysis_images/imageFile1109.png)|
|---|


|![image 1110](McKenzie - Examples in Structural Analysis_images/imageFile1110.png)|
|---|


![image 1111](McKenzie - Examples in Structural Analysis_images/imageFile1111.png)

![image 1112](McKenzie - Examples in Structural Analysis_images/imageFile1112.png)

###### Figure 7.22

|7.9 Example 7.2: Rigid–Jointed Frame<br><br>A non-uniform, rigid-jointed frame ABCD is fully-fixed at supports A and D as indicated in Figure 7.23. A uniformly distributed load of 3 kN/m is applied to element BC a central point load of 5 kN is applied to element AB and a point load at node C as shown. Using the data given, the degrees-of-freedom indicated and assuming all members to be axially rigid,<br><br>|
|---|
|(i) generate the structural stiffness matrix [K] and the applied load vector [P],<br><br>(ii) determine the structural displacements,<br><br>(iii) determine the member end forces and the support reactions,<br><br>(iv) sketch the shear force and bending moment diagrams, (vi) sketch the deflected shape.<br><br><br>|
|![image 1113](McKenzie - Examples in Structural Analysis_images/imageFile1113.png)<br><br>Figure 7.23 Solution:<br><br>Each degree-of-freedom is given a unit displacement in turn and the forces necessary to maintain the displacements is calculated in each case.<br><br>|


![image 1114](McKenzie - Examples in Structural Analysis_images/imageFile1114.png)

![image 1115](McKenzie - Examples in Structural Analysis_images/imageFile1115.png)

###### There are several methods for inverting matrices, the technique used here is given in Appendix 3.

![image 1116](McKenzie - Examples in Structural Analysis_images/imageFile1116.png)

![image 1117](McKenzie - Examples in Structural Analysis_images/imageFile1117.png)

###### The equivalent nodal loads required are those which correspond with the nodal degree-offreedom as follows:

![image 1118](McKenzie - Examples in Structural Analysis_images/imageFile1118.png)

![image 1119](McKenzie - Examples in Structural Analysis_images/imageFile1119.png)

![image 1120](McKenzie - Examples in Structural Analysis_images/imageFile1120.png)

![image 1121](McKenzie - Examples in Structural Analysis_images/imageFile1121.png)

![image 1122](McKenzie - Examples in Structural Analysis_images/imageFile1122.png)

|![image 1123](McKenzie - Examples in Structural Analysis_images/imageFile1123.png)<br><br>Figure 7.24<br><br>7.10 Problems: Direct Stiffness Method<br><br>|
|---|


A series of indeterminate structures are indicated in Problems 7.1 to 7.6 in which the assumed degrees-of-freedom at the nodes and the relative EI values for the members are given. In each case for the data indicated:

- (i) generate the structural stiffness matrix [K] and the applied load vector [P],

- (ii) determine the structural displacements [Δ],

- (iii) determine the member end forces [F],

- (iv) determine the support reactions,


(v) sketch the axial load, shear force, and bending moment diagrams and the deflected shape for each structure.

![image 1124](McKenzie - Examples in Structural Analysis_images/imageFile1124.png)

- Problem 7.1

![image 1125](McKenzie - Examples in Structural Analysis_images/imageFile1125.png)

- Problem 7.2


![image 1126](McKenzie - Examples in Structural Analysis_images/imageFile1126.png)

###### Problem 7.3

![image 1127](McKenzie - Examples in Structural Analysis_images/imageFile1127.png)

###### Problem 7.4

![image 1128](McKenzie - Examples in Structural Analysis_images/imageFile1128.png)

###### Problem 7.5

![image 1129](McKenzie - Examples in Structural Analysis_images/imageFile1129.png)

###### Problem 7.6

|7.11 Solutions: Direct Stiffness Method<br><br>![image 1130](McKenzie - Examples in Structural Analysis_images/imageFile1130.png)|
|---|


|![image 1131](McKenzie - Examples in Structural Analysis_images/imageFile1131.png)|
|---|


|![image 1132](McKenzie - Examples in Structural Analysis_images/imageFile1132.png)|
|---|


|![image 1133](McKenzie - Examples in Structural Analysis_images/imageFile1133.png)|
|---|


|![image 1134](McKenzie - Examples in Structural Analysis_images/imageFile1134.png)|
|---|


|![image 1135](McKenzie - Examples in Structural Analysis_images/imageFile1135.png)|
|---|


|![image 1136](McKenzie - Examples in Structural Analysis_images/imageFile1136.png)|
|---|


|![image 1137](McKenzie - Examples in Structural Analysis_images/imageFile1137.png)|
|---|


|![image 1138](McKenzie - Examples in Structural Analysis_images/imageFile1138.png)|
|---|


|![image 1139](McKenzie - Examples in Structural Analysis_images/imageFile1139.png)|
|---|


|![image 1140](McKenzie - Examples in Structural Analysis_images/imageFile1140.png)|
|---|


|![image 1141](McKenzie - Examples in Structural Analysis_images/imageFile1141.png)|
|---|


|![image 1142](McKenzie - Examples in Structural Analysis_images/imageFile1142.png)|
|---|


|![image 1143](McKenzie - Examples in Structural Analysis_images/imageFile1143.png)|
|---|


|![image 1144](McKenzie - Examples in Structural Analysis_images/imageFile1144.png)|
|---|


|![image 1145](McKenzie - Examples in Structural Analysis_images/imageFile1145.png)|
|---|


|![image 1146](McKenzie - Examples in Structural Analysis_images/imageFile1146.png)|
|---|


|![image 1147](McKenzie - Examples in Structural Analysis_images/imageFile1147.png)|
|---|


|![image 1148](McKenzie - Examples in Structural Analysis_images/imageFile1148.png)|
|---|


|![image 1149](McKenzie - Examples in Structural Analysis_images/imageFile1149.png)|
|---|


|![image 1150](McKenzie - Examples in Structural Analysis_images/imageFile1150.png)|
|---|


|![image 1151](McKenzie - Examples in Structural Analysis_images/imageFile1151.png)|
|---|


|![image 1152](McKenzie - Examples in Structural Analysis_images/imageFile1152.png)|
|---|


|![image 1153](McKenzie - Examples in Structural Analysis_images/imageFile1153.png)|
|---|


|![image 1154](McKenzie - Examples in Structural Analysis_images/imageFile1154.png)|
|---|


|![image 1155](McKenzie - Examples in Structural Analysis_images/imageFile1155.png)|
|---|


|![image 1156](McKenzie - Examples in Structural Analysis_images/imageFile1156.png)|
|---|


|![image 1157](McKenzie - Examples in Structural Analysis_images/imageFile1157.png)|
|---|


|![image 1158](McKenzie - Examples in Structural Analysis_images/imageFile1158.png)|
|---|


|![image 1159](McKenzie - Examples in Structural Analysis_images/imageFile1159.png)|
|---|


|![image 1160](McKenzie - Examples in Structural Analysis_images/imageFile1160.png)|
|---|


|![image 1161](McKenzie - Examples in Structural Analysis_images/imageFile1161.png)|
|---|


|![image 1162](McKenzie - Examples in Structural Analysis_images/imageFile1162.png)|
|---|


|![image 1163](McKenzie - Examples in Structural Analysis_images/imageFile1163.png)|
|---|


|![image 1164](McKenzie - Examples in Structural Analysis_images/imageFile1164.png)|
|---|


|![image 1165](McKenzie - Examples in Structural Analysis_images/imageFile1165.png)|
|---|


|![image 1166](McKenzie - Examples in Structural Analysis_images/imageFile1166.png)|
|---|


|![image 1167](McKenzie - Examples in Structural Analysis_images/imageFile1167.png)|
|---|


|![image 1168](McKenzie - Examples in Structural Analysis_images/imageFile1168.png)|
|---|


|![image 1169](McKenzie - Examples in Structural Analysis_images/imageFile1169.png)|
|---|


|![image 1170](McKenzie - Examples in Structural Analysis_images/imageFile1170.png)|
|---|


|![image 1171](McKenzie - Examples in Structural Analysis_images/imageFile1171.png)|
|---|


|![image 1172](McKenzie - Examples in Structural Analysis_images/imageFile1172.png)|
|---|


|![image 1173](McKenzie - Examples in Structural Analysis_images/imageFile1173.png)|
|---|


|![image 1174](McKenzie - Examples in Structural Analysis_images/imageFile1174.png)|
|---|


|![image 1175](McKenzie - Examples in Structural Analysis_images/imageFile1175.png)|
|---|


|![image 1176](McKenzie - Examples in Structural Analysis_images/imageFile1176.png)|
|---|


|![image 1177](McKenzie - Examples in Structural Analysis_images/imageFile1177.png)|
|---|


![image 1178](McKenzie - Examples in Structural Analysis_images/imageFile1178.png)

### 8. Plastic Analysis

#### 8.1 Introduction

The Plastic Moment of Resistance (Mp) of individual member sections can be derived as indicated in Section 2.3 of Chapter 2. The value of Mp is the maximum value of moment which can be applied to a cross-section before a plastic hinge develops. Consider structural collapse in which either individual members may fail or the entire structure may fail as a whole due to the development of plastic hinges.

According to the theory of plasticity, a structure is deemed to have reached the limit of its load carrying capacity when it forms sufficient hinges to convert it into a mechanism with consequent collapse. This is normally one hinge more than the number of degreesof-indeterminacy (ID) in the structure as indicated in Figure 8.1.

|![image 1179](McKenzie - Examples in Structural Analysis_images/imageFile1179.png)<br><br>Figure 8.1<br><br>|
|---|


|8.1.1 Partial Collapse|
|---|


It is possible for part of a structure to collapse whilst the rest remains stable. In this instance full collapse does not occur and the number of hinges required to cause partial collapse is less than the (ID+1.0). This is illustrated in the multi-span beam shown in Figure 8.2. Ignoring horizontal forces ID=[(2m+r)−2n]=[(2×4)+5−(2×5)]=3

|![image 1180](McKenzie - Examples in Structural Analysis_images/imageFile1180.png)<br><br>Figure 8.2<br><br>|
|---|


For any given design load applied to a redundant structure, more than one collapse mechanism may be possible. The correct mechanism is the one which requires the least amount of ‘work done’ for it's inception.

|8.1.2 Conditions for Full Collapse|
|---|


There are three conditions which must be satisfied to ensure full collapse of a structure and the identification of the true collapse load, they are:

|(i) the mechanism condition in which there must be sufficient plastic hinges to develop<br><br>a mechanism, (i.e. number of plastic hinges ≥[ID+1]),<br><br>(ii) the equilibrium condition in which the bending moments for any collapse<br><br>mechanism must be in equilibrium with the applied collapse loads,<br><br>(iii) the yield condition in which the magnitude of the bending moment anywhere on<br><br><br>the structure cannot exceed the plastic moment of resistance of the member in which it occurs.<br><br>|
|---|


Provided that these three conditions can be satisfied then the true collapse load can be identified.

If only the mechanism and equilibrium conditions are satisfied then an upper-bound (unsafe) solution is obtained in which the collapse load determined is either greater than or equal to the true value.

If only the yield and equilibrium conditions are satisfied then a lower-bound (safe) solution is obtained in which the collapse load determined is either less than or equal to the true value.

Since the bending moment cannot exceed the Mp value for a given cross-section it is evident that when hinges develop they will occur at the positions of maximum bending moment, i.e. at fixed supports, rigid-joints, under point loads and within the region of distributed loads.

The analysis of beams and frames involves determining:

|(i) the collapse loads,<br><br>(ii) the number of hinges required to induce collapse,<br><br>(iii) the possible hinge positions,<br><br>(iv) the independent collapse mechanisms and their associated Mp values,<br><br>(v) the possible combinations of independent mechanisms to obtain the highest<br><br>required Mp value,<br><br>(vi) checking the validity of the calculated value with respect to mechanism,<br><br><br>equilibrium and yield conditions.<br><br>|
|---|


There are two methods of analysis which are frequently used to determine the values of plastic moment of resistance for sections required for a structure to collapse at specified factored loads; they are the Static Method and the Kinematic Method. These are illustrated with respect to continuous beams in Sections 8.2 to 8.4. and with respect to frames in Sections 8.5 to 8.12.

|8.2 Static Method for Continuous Beams|
|---|


In the static method of analysis the ‘Free Bending Moment’ diagrams for the structure are drawn and the ‘Fixed Bending Moment’ diagrams are then added algebraically. The magnitude and ‘sense’ +ve or −ve of the moments must be such that sufficient plastic hinges occur to cause the collapse of the whole or a part of the structure.

In addition, for collapse to occur, adjacent plastic hinges must be alternatively ‘opening’ and ‘closing’. For uniform beams the plastic moment of resistance of each hinge will be the same i.e. Mp.

|8.2.1 Example 8.1: Encastre Beam|
|---|


An encastre beam is 8.0 m long and supports an unfactored load of 40 kN/m as shown in Figure 8.3. Assuming that the yield stress py=460 N/mm2 and a load factor λ=1.7, determine the required plastic moment of resistance and plastic section modulus.

|![image 1181](McKenzie - Examples in Structural Analysis_images/imageFile1181.png)<br><br>Figure 8.3<br><br>|
|---|


Solution:

The collapse load=(40.0×1.7)=68.0 kN/m

The number of hinges required to induce collapse=(ID+1)=3 (see Figure

- 8.1)


The possible hinge positions are at the supports A and B and within the region of a distributed load since these are the positions where the maximum bending moments occur. Superimpose the fixed and free bending moment diagrams:

|![image 1182](McKenzie - Examples in Structural Analysis_images/imageFile1182.png)<br><br>Figure 8.4<br><br>|
|---|


The beam has two redundancies (ignoring horizontal components of reaction) therefore a minimum of three hinges must develop to create a mechanism. Since the beam is uniform, at failure all values of the bending moment at the hinge positions must be equal to the plastic moment of resistance and cannot be exceeded anywhere:

|![image 1183](McKenzie - Examples in Structural Analysis_images/imageFile1183.png)|
|---|


It is evident from the above that all three conditions in Section 8.1.2 are satisfied and consequently the Mp value calculated for the required collapse load is true to achieve a load factor of 1.7

|8.2.2 Example 8.2: Propped Cantilever 1|
|---|


A propped cantilever is 6.0 m long and supports a collapse load of 24 kN as shown in Figure 8.5. Determine the required plastic moment of resistance Mp.

|![image 1184](McKenzie - Examples in Structural Analysis_images/imageFile1184.png)<br><br>Figure 8.5<br><br>|
|---|


Solution:

The collapse load=24.0 kN

The number of hinges required to induce collapse=(ID+1)=2 (see Figure

- 8.1)


The possible hinge positions are at the support A and under the point load since these are the positions where the maximum bending moments occur.

The support reactions for the free bending diagram are: VA=8.0 kN and VC=16.0 kN

The maximum free bending moment at Mfree,C,=(8.0×4.0)=32.0 kNm The bending moment at B due to the fixed moment= −[M1×(2.0×6.0)]

=−0.333M1 kNm

|![image 1185](McKenzie - Examples in Structural Analysis_images/imageFile1185.png)<br><br>Figure 8.6<br><br>|
|---|


The beam has one redundancy (ignoring horizontal components of reaction) therefore a minimum of two hinges must develop to create a mechanism. Since the beam is uniform, at failure all values of the bending moment at the hinge positions must be equal to the plastic moment of resistance and cannot be exceeded anywhere:

|![image 1186](McKenzie - Examples in Structural Analysis_images/imageFile1186.png)|
|---|


As in Example 8.1 all three conditions in Section 8.1.2 are satisfied and consequently the true value of Mp has been calculated for the given collapse load.

|8.2.3 Example 8.3: Propped Cantilever 2|
|---|


A propped cantilever is L m long and supports a collapse load of w kN/m as shown in Figure 8.7. Determine the position of the plastic hinges and the required plastic moment of resistance Mp.

|![image 1187](McKenzie - Examples in Structural Analysis_images/imageFile1187.png)<br><br>Figure 8.7<br><br>|
|---|


Solution:

The collapse load=w kN/m

The number of hinges required to induce collapse=(ID+1)=2 (see Figure

- 8.1)


The possible hinge positions are at the support A and within the region of a distributed load since these are the positions where the maximum bending moments occur. In this case the maximum moment under the distributed load does not occur at mid-span since the bending moment diagram is not symmetrical. Consider the final bending moment diagram:

|![image 1188](McKenzie - Examples in Structural Analysis_images/imageFile1188.png)<br><br>Figure 8.8<br><br>|
|---|


The maximum bending moment (i.e. Mp) occurs at a distance ‘x’ from the roller support and can be determined as follows;

Since the moment is a maximum at position ‘x’ the shear force at ‘x’ is equal to zero.

|![image 1189](McKenzie - Examples in Structural Analysis_images/imageFile1189.png)|
|---|


Equate the Mp values to determine x:

|![image 1190](McKenzie - Examples in Structural Analysis_images/imageFile1190.png)|
|---|


This is a standard value, i.e. for a propped cantilever the plastic hinge in the span occurs at a distance x=0.414L from the simply supported end and the value of the plastic moment Mp=0.0858wL2

|8.3 Kinematic Method for Continuous Beams|
|---|


In this method, a displacement is imposed upon each possible collapse mechanism and an equation between external work done and internal work absorbed in forming the hinges is developed. The collapse mechanism involving the greatest plastic moment, Mp, is the critical one.

Consider the previous Example 8.1 of an encastre beam with a uniformly distributed load. The hinge positions were identified as occurring at A, B and the mid-span point (since the beam and loading are symmetrical). Assuming rigid links between the hinges, the collapse mechanism of the beam when the hinges develop can be drawn as shown in Figure 8.9(c). The deformed shape is drawn grossly magnified to enable the relationship between the rotations at the hinges and the displacements of the loads to be easily identified.

A virtual work equation can be developed by equating the external work done by the applied loads to the internal work done by the formation of the hinges where: Internal work done during the formation of a hinge=(moment×rotation) External work done by a load during displacement=(load×displacement) (In the case of distributed loads the average displacement is used). The sign convention adopted is: Tension on the Bottom of the beam induces a ‘positive’ rotation (i.e. +ve bending) Tension on the Top of the beam induces a ‘negative’ rotation (i.e. −ve bending)

Note: the development of both −ve and +ve hinges involves +ve internal work

|![image 1191](McKenzie - Examples in Structural Analysis_images/imageFile1191.png)<br><br>Figure 8.9<br><br>|
|---|


From the deformed shape in Figure 8.9:

![image 1192](McKenzie - Examples in Structural Analysis_images/imageFile1192.png)

For small values of θ and β The load deflects zero at the supports and δ at the centre

![image 1193](McKenzie - Examples in Structural Analysis_images/imageFile1193.png)

Average displacement of the load The Internal Work Done in developing the hinges is found from the product of the moment induced (i.e. Mp) and the amount of rotation (e.g. θ) for each hinge.

|![image 1194](McKenzie - Examples in Structural Analysis_images/imageFile1194.png)|
|---|


The External Work Done by the applied load system is found from the product of the load and the displacement for each load.

|![image 1195](McKenzie - Examples in Structural Analysis_images/imageFile1195.png)|
|---|


- Consider the previous Example 8.2 of propped cantilever with a single point load. The


hinge positions were identified as occurring at support A, and under the point load at B. Assuming rigid links between the hinges, the collapse mechanism of the beam when the hinges develop can be drawn as shown in Figure 8.10(c).

|![image 1196](McKenzie - Examples in Structural Analysis_images/imageFile1196.png)<br><br>Figure 8.10<br><br>|
|---|


From the deformed shape in Figure 8.10:

|![image 1197](McKenzie - Examples in Structural Analysis_images/imageFile1197.png)|
|---|


- Consider the previous Example 8.3 of a propped cantilever with a uniformly


distributed load. The hinge positions were identified as occurring at support A, and at a point load 0.4142L from the simple support. Assuming rigid links between the hinges, the deformed shape of the beam when the hinges develop can be drawn as shown in Figure 8.11(c).

|![image 1198](McKenzie - Examples in Structural Analysis_images/imageFile1198.png)<br><br>Figure 8.11<br><br>|
|---|


From the deformed shape in Figure 8.11:

For small values of θ and/β δ=0.586Lθ=0.414Lβ :. β=1.415θ The load deflects zero at the supports and δ at a distance 0.414L from support B.

![image 1199](McKenzie - Examples in Structural Analysis_images/imageFile1199.png)

Average displacement of the load Internal Work Done=External Work Done

Mpθ+Mp(θ+β)=(w×L)×0.293Lθ 3.415Mpθ=0.293wLθ Mp=0.0858wL2 (as before)

|8.3.1 Example 8.4: Continuous Beam|
|---|


A non-uniform, three-span beam is fixed at support A, simply supported on rollers at D, F and G and carries unfactored loads as shown in Figure 8.12. Determine the minimum Mp value required to ensure a minimum load factor equal to 1.7 for any span.

|![image 1200](McKenzie - Examples in Structural Analysis_images/imageFile1200.png)<br><br>Figure 8.12<br><br>|
|---|


There are a number of possible elementary beam mechanisms and it is necessary to ensure all possibilities have been considered. It is convenient in multi-span beams to consider each span separately and identify the collapse mechanism involving the greatest plastic moment Mp; this is the critical one and results in partial collapse.

The number of elementary independent mechanisms can be determined from evaluating (the number of possible hinge positions—the degree-ofindeterminacy).

|![image 1201](McKenzie - Examples in Structural Analysis_images/imageFile1201.png)|
|---|


Number of independent mechanisms =(7−3)=4

(Note: In framed structures combinations of independent mechanisms must also be considered see Section 8.5).

λ=1.7

|![image 1202](McKenzie - Examples in Structural Analysis_images/imageFile1202.png)|
|---|


Consider span ABCD:

In this span there are four possible hinge positions, however only three are required to induce collapse in the beam. There are two independent collapse mechanisms to consider, they are:

- (i) hinges developing at A (moment=2Mp), B (moment=2Mp) and D (moment=Mp)
- (ii) hinges developing at A (moment=2Mp), C (moment=2Mp) and D (moment=Mp)


Static Method:

The free bendng moment at B=119.0 kNm

The free bendng moment at C=68.0 kNm.

|![image 1203](McKenzie - Examples in Structural Analysis_images/imageFile1203.png)|
|---|


In this span the critical value of Mp=33.06 kNm with hinges developing at A, B and D.

Kinematic Method:

|![image 1204](McKenzie - Examples in Structural Analysis_images/imageFile1204.png)|
|---|


Consider span DEF:

###### In this span only three hinges are required to induce collapse in the beam. Hinges develop at D (moment=Mp), E (moment=Mp) and F (moment=Mp)

|![image 1205](McKenzie - Examples in Structural Analysis_images/imageFile1205.png)|
|---|


|![image 1206](McKenzie - Examples in Structural Analysis_images/imageFile1206.png)|
|---|


Consider span FG:

###### In this span only two hinges are required to induce collapse in the beam. Hinges develop at F (moment=Mp), and between F and G (moment=1.5Mp)

|![image 1207](McKenzie - Examples in Structural Analysis_images/imageFile1207.png)|
|---|


Span FG is effectively a propped cantilever and consequently the position of the hinge under the uniformly distributed load must be calculated. (Note: it is different from Example 8.3 since the plastic moment at each hinge position is not the same).

|![image 1208](McKenzie - Examples in Structural Analysis_images/imageFile1208.png)|
|---|


Equate the Mp values to determine x:

|![image 1209](McKenzie - Examples in Structural Analysis_images/imageFile1209.png)<br><br>8.4 Problems: Plastic Analysis—Continuous Beams<br><br>|
|---|


A series of continuous beams are indicated in which the relative Mp values and the applied collapse loadings are given in Problems 8.1 to 8.5. Determine the required value of Mp to ensure a minimum load factor λ=1.7.

|![image 1210](McKenzie - Examples in Structural Analysis_images/imageFile1210.png)<br><br>Problem 8.1<br><br>![image 1211](McKenzie - Examples in Structural Analysis_images/imageFile1211.png)<br><br>Problem 8.2<br><br><br>|
|---|


![image 1212](McKenzie - Examples in Structural Analysis_images/imageFile1212.png)

- Problem 8.3

![image 1213](McKenzie - Examples in Structural Analysis_images/imageFile1213.png)

- Problem 8.4

![image 1214](McKenzie - Examples in Structural Analysis_images/imageFile1214.png)

- Problem 8.5


#### 8.5 Solutions: Plastic Analysis—Continuous Beams

|![image 1215](McKenzie - Examples in Structural Analysis_images/imageFile1215.png)|
|---|


|![image 1216](McKenzie - Examples in Structural Analysis_images/imageFile1216.png)|
|---|


|![image 1217](McKenzie - Examples in Structural Analysis_images/imageFile1217.png)|
|---|


|![image 1218](McKenzie - Examples in Structural Analysis_images/imageFile1218.png)|
|---|


|![image 1219](McKenzie - Examples in Structural Analysis_images/imageFile1219.png)|
|---|


|![image 1220](McKenzie - Examples in Structural Analysis_images/imageFile1220.png)|
|---|


|![image 1221](McKenzie - Examples in Structural Analysis_images/imageFile1221.png)|
|---|


|![image 1222](McKenzie - Examples in Structural Analysis_images/imageFile1222.png)|
|---|


|![image 1223](McKenzie - Examples in Structural Analysis_images/imageFile1223.png)|
|---|


|![image 1224](McKenzie - Examples in Structural Analysis_images/imageFile1224.png)|
|---|


|![image 1225](McKenzie - Examples in Structural Analysis_images/imageFile1225.png)|
|---|


|![image 1226](McKenzie - Examples in Structural Analysis_images/imageFile1226.png)|
|---|


|![image 1227](McKenzie - Examples in Structural Analysis_images/imageFile1227.png)|
|---|


|![image 1228](McKenzie - Examples in Structural Analysis_images/imageFile1228.png)|
|---|


|![image 1229](McKenzie - Examples in Structural Analysis_images/imageFile1229.png)|
|---|


|![image 1230](McKenzie - Examples in Structural Analysis_images/imageFile1230.png)|
|---|


|![image 1231](McKenzie - Examples in Structural Analysis_images/imageFile1231.png)|
|---|


![image 1232](McKenzie - Examples in Structural Analysis_images/imageFile1232.png)

#### 8.6 Rigid-Jointed Frames

In the case of beams identification of the critical spans (i.e. in terms of Mp or λ) can usually be solved quite readily by using either the static or the kinematic method and considering simple beam mechanisms. In the case of frames other types of mechanisms,

such as sway, joint and gable mechanisms are also considered. Whilst both techniques can be used the static method often proves laborious when applied to rigid frames, particularly for complex load conditions. It can be easier than the kinematic method in the case of determinate or singly redundant frames. Both methods are illustrated in this section and in the solutions to the given problems.

###### As mentioned previously the kinematic solution gives a lower bound to the true solution whilst the static solution gives an upper bound.

|![image 1233](McKenzie - Examples in Structural Analysis_images/imageFile1233.png)|
|---|


Two basic types of independent mechanism are shown in Figure 8.13:

|![image 1234](McKenzie - Examples in Structural Analysis_images/imageFile1234.png)<br><br>Figure 8.13<br><br>|
|---|


Each of these collapse mechanisms can occur independently of each other. It is also possible for a critical collapse mechanism to develop which is a combination of the independent ones such as indicated in Figure 8.14.

|![image 1235](McKenzie - Examples in Structural Analysis_images/imageFile1235.png)<br><br>Figure 8.14<br><br>|
|---|


It is necessary to consider all possible combinations to identify the critical collapse mode. The Mp value is determined for each independent mechanism and then combined mechanisms are evaluated to establish a maximum value of Mp (i.e. minimum λ). The purpose of combining mechanisms is to eliminate sufficient hinges which exist in the independent mechanisms, leaving only the minimum number required in the resulting combination to induce collapse.

###### It is necessary when carrying out a kinematic solution, to draw the bending moment diagram to ensure that at no point the Mp value determined, is exceeded.

|8.6.1 Example 8.5: Frame 1|
|---|


An asymmetric uniform, frame is pinned at supports A and G and is subjected to a system of factored loads as shown in Figure 8.15. Assuming the λvertical.load=1.7 and λhorizontal loads=1.4 determine the required plastic moment of resistance Mp of the section.

|![image 1236](McKenzie - Examples in Structural Analysis_images/imageFile1236.png)<br><br>Figure 8.15<br><br>|
|---|
|![image 1237](McKenzie - Examples in Structural Analysis_images/imageFile1237.png)|


###### Kinematic Method:

Consider each independent mechanism separately.

###### Mechanism (i): Beam ABC

|![image 1238](McKenzie - Examples in Structural Analysis_images/imageFile1238.png)<br><br>![image 1239](McKenzie - Examples in Structural Analysis_images/imageFile1239.png)<br><br>|
|---|


###### Combinations:

Consider the independent mechanisms, their associated work equations and Mp values as shown in Figure 8.16:

|![image 1240](McKenzie - Examples in Structural Analysis_images/imageFile1240.png)<br><br>Figure 8.16<br><br>|
|---|


It is evident from inspection of the collapse mechanisms that the hinges located at C and E can be eliminated since in some cases the rotation is negative whilst in others it is positive. The minimum number of hinges to induce total collapse is one more than the number of redundancies, i.e. (ID+1)=2 and therefore the independent mechanisms should be combined to try and achieve this and at the same time maximize the associated Mp value. It is unlikely that mechanism (i) will be included in the failure mechanism since its associated Mp value is relatively small compared to the others. It is necessary to investigate several possibilities and confirm the resulting solution by checking that the bending moments do not exceed the plastic moment of resistance at any section.

Combination 1: Mechanism (v)=[(ii)+(iv)] When combining these mechanisms the hinge at C will be eliminated and the resulting Mp value can be determined by adding the work equations. It is necessary to allow for the removal of the hinge at C in the internal work done since in each equation an (Mpθ) term has been included, but the hinge no longer exists. A total of 2Mp must therefore be subtracted from the resulting internal work, i.e.

|![image 1241](McKenzie - Examples in Structural Analysis_images/imageFile1241.png)|
|---|


![image 1242](McKenzie - Examples in Structural Analysis_images/imageFile1242.png)

It is possible that this is the true collapse mechanism, however this would have to be confirmed as indicated above by satisfying conditions (ii) and (iii) in Section 8.1.2.

An alternative solution is also possible where the hinges at C and E are eliminated, this can be a achieved if mechanism (v) is combined with mechanism (iii).

In mechanism (v) β=0.5θ (see the sway calculation above) and hence the total rotation at joint E=−(θ+β)=−1.5θ. If this hinge is to be eliminated then the combinations of mechanisms (iii) and (v) must be in the proportions of 1.5:1.0. (Note: when developing mechanism (v) the proportions were 1:1).

The total value of the internal work for the eliminated hinge=(2×1.5Mp)=3.0Mp, i.e.

|![image 1243](McKenzie - Examples in Structural Analysis_images/imageFile1243.png)|
|---|


![image 1244](McKenzie - Examples in Structural Analysis_images/imageFile1244.png)

The +ve rotation indicates tension inside the frame at point D and the −ve rotation indicates tension outside the frame at point F.

This is marginally higher than the previous value and since there does not appear to be any other obvious collapse mechanism, this result should be checked as follows:

![image 1245](McKenzie - Examples in Structural Analysis_images/imageFile1245.png)

Figure 8.17

![image 1246](McKenzie - Examples in Structural Analysis_images/imageFile1246.png)

|![image 1247](McKenzie - Examples in Structural Analysis_images/imageFile1247.png)<br><br>Figure 8.18<br><br>|
|---|


The three conditions indicated in Section 8.1.2 have been satisfied: i.e.

Mechanism condition: minimum number of hinges required=(ID+1)=2 hinges,

Equilibrium condition: the internal moments are in equilibrium with the collapse loads,

Yield condition: the bending moment does not exceed Mp anywhere in the frame.

|Mp kinematic=Mpstatic=Mptrue|
|---|


It is often convenient to carry-out the calculation of combinations using a table as shown in Table 8.1; eliminated hinges are indicated by EH in the Table.

|Independent and Combined Mechanisms for Example 8.5|
|---|


Hinge Position

(i) (ii) (iii) (iv) (v)=(ii)+(iv) (vi)=(v)+1.5(iii)

|B(MP)|+2.0θ|−|−|−|−|−|
|---|---|---|---|---|---|---|
|C(Mp)|−θ|−θ|−|+θ|EH (2.0Mpθ)|EH (2.0Mpθ)|
|D (Mp)|−|+2.0θ|−|−|+2.0θ|+2.0θ|
|E (Mp)|−|−θ|+θ|−0.5θ|−1.5θ|EH (3.0Mpθ)|
|F (Mp)|−|−|−2.0θ|−|−|−3.0θ|
|External Work|31.5θ|136.0θ|63.0θ|63.0θ|199.0θ|293.5θ|
|Internal Work|3.0Mpθ|4.0Mpθ|3.0Mpθ|1.5Mpθ|5.5Mpθ|10.0Mpθ|
|Eliminated hinges|−|−|−|−|2.0Mpθ|5.0Mpθ|
|Combined MPθ|−|−|−|−|3.5MPθ|5.0Mpθ|
|Mp (kNm)|10.5|34.0|21.0|42.0|56.86|58.70|


|Table 8.1|
|---|


Static Method:

This frame can also be analysed readily using the static method since it only has one degree-of-indeterminacy. When using this method the frame can be considered as the superposition of two frames; one statically determinate and one involving only the assumed redundant reaction as shown in Figure 8.19. Applying the three equations of equilibrium to the two force systems results in the support reactions indicated.

|![image 1248](McKenzie - Examples in Structural Analysis_images/imageFile1248.png)<br><br>Figure 8.19<br><br>|
|---|
|![image 1249](McKenzie - Examples in Structural Analysis_images/imageFile1249.png)|


Equations can be developed for each of the five possible hinge positions in terms of the two frames as follows:

|![image 1250](McKenzie - Examples in Structural Analysis_images/imageFile1250.png)<br><br>Equation<br><br>(1)|
|---|


![image 1251](McKenzie - Examples in Structural Analysis_images/imageFile1251.png)

Equation

(2)

|![image 1252](McKenzie - Examples in Structural Analysis_images/imageFile1252.png)<br><br>Equation<br><br>(3)|
|---|


![image 1253](McKenzie - Examples in Structural Analysis_images/imageFile1253.png)

Equation

- (4)


![image 1254](McKenzie - Examples in Structural Analysis_images/imageFile1254.png)

- Equation
- (5)


As indicated previously, only two hinges are required to induce total collapse. A collapse mechanism involving two hinge positions can be assumed and the associated equations will each have two unknown values, i.e. HG and Mp and can be solved simultaneously.

The value of the bending moment at all other hinge positions can then be checked to ensure that they do not exceed the calculated Mp value. If any one does exceed the value then the assumed mechanism was incorrect and others can be checked until the true one is identified.

Assume a mechanism inducing hinges at D and E as in (v) above.

|![image 1255](McKenzie - Examples in Structural Analysis_images/imageFile1255.png)|
|---|


![image 1256](McKenzie - Examples in Structural Analysis_images/imageFile1256.png)

Equation

(6)

|![image 1257](McKenzie - Examples in Structural Analysis_images/imageFile1257.png)<br><br>Equation<br><br>(7)|
|---|


Add equations (6) and (7):

|![image 1258](McKenzie - Examples in Structural Analysis_images/imageFile1258.png)|
|---|


Check the value of the moments at all other possible hinge positions.

|![image 1259](McKenzie - Examples in Structural Analysis_images/imageFile1259.png)|
|---|


Since the bending moment at F is greater than Mp this mechanism does not satisfy the ‘yield condition’ and produces an unsafe solution.

The reader should repeat the above calculation assuming hinges develop at positions D and F and confirm that the true solution is when Mp=58.7 kNm as determined previously using the kinematic method.

|8.7 Problems: Plastic Analysis—Rigid-Jointed Frames 1|
|---|


A series of rigid-jointed frames are indicated in Problems 8.6 to 8.9 in which the relative Mp values and the applied collapse loads are given. In each case determine the required Mp value, the value of the support reactions and sketch the bending moment diagram.

|![image 1260](McKenzie - Examples in Structural Analysis_images/imageFile1260.png)<br><br>Problem 8.6<br><br>|
|---|


|![image 1261](McKenzie - Examples in Structural Analysis_images/imageFile1261.png)<br><br>Problem 8.7<br><br>![image 1262](McKenzie - Examples in Structural Analysis_images/imageFile1262.png)<br><br>Problem 8.8<br><br><br>|
|---|


![image 1263](McKenzie - Examples in Structural Analysis_images/imageFile1263.png)

###### Problem 8.9

|8.8 Solutions: Plastic Analysis—Rigid-Jointed Frames 1<br><br>![image 1264](McKenzie - Examples in Structural Analysis_images/imageFile1264.png)|
|---|


|![image 1265](McKenzie - Examples in Structural Analysis_images/imageFile1265.png)|
|---|


|![image 1266](McKenzie - Examples in Structural Analysis_images/imageFile1266.png)|
|---|


|![image 1267](McKenzie - Examples in Structural Analysis_images/imageFile1267.png)|
|---|


|![image 1268](McKenzie - Examples in Structural Analysis_images/imageFile1268.png)|
|---|


|![image 1269](McKenzie - Examples in Structural Analysis_images/imageFile1269.png)|
|---|


|![image 1270](McKenzie - Examples in Structural Analysis_images/imageFile1270.png)|
|---|


|![image 1271](McKenzie - Examples in Structural Analysis_images/imageFile1271.png)|
|---|


|![image 1272](McKenzie - Examples in Structural Analysis_images/imageFile1272.png)|
|---|


|![image 1273](McKenzie - Examples in Structural Analysis_images/imageFile1273.png)|
|---|


|![image 1274](McKenzie - Examples in Structural Analysis_images/imageFile1274.png)|
|---|


|![image 1275](McKenzie - Examples in Structural Analysis_images/imageFile1275.png)|
|---|


|![image 1276](McKenzie - Examples in Structural Analysis_images/imageFile1276.png)|
|---|


|![image 1277](McKenzie - Examples in Structural Analysis_images/imageFile1277.png)|
|---|


|![image 1278](McKenzie - Examples in Structural Analysis_images/imageFile1278.png)|
|---|


|![image 1279](McKenzie - Examples in Structural Analysis_images/imageFile1279.png)|
|---|


![image 1280](McKenzie - Examples in Structural Analysis_images/imageFile1280.png)

#### 8.9 Example 8.6: Joint Mechanism

In framed structures where there are more than two members meeting at a joint there is the possibility of a joint mechanism developing within a collapse mechanism. Consider the frame shown in Figure 8.20 with the collapse loads indicated. At joint C individual

hinges can develop in members CBA, CDE and CFG giving three possible hinge positions at the joint in addition to positions B, D F and G.

|![image 1281](McKenzie - Examples in Structural Analysis_images/imageFile1281.png)<br><br>Figure 8.20<br><br>|
|---|


Factored loads: as given

|![image 1282](McKenzie - Examples in Structural Analysis_images/imageFile1282.png)|
|---|


###### Kinematic Method:

Consider each independent mechanism separately.

###### Mechanism (i): Beam ABC

|![image 1283](McKenzie - Examples in Structural Analysis_images/imageFile1283.png)|
|---|


The hinge at joint C is assumed to develop in member ABC at C1.

|![image 1284](McKenzie - Examples in Structural Analysis_images/imageFile1284.png)|
|---|


Mechanism (ii): Joint

###### The joint at C can rotate either in a clockwise direction or an anticlockwise direction.

|![image 1285](McKenzie - Examples in Structural Analysis_images/imageFile1285.png)|
|---|


The independent mechanisms can be entered into a table as before and the possible combinations investigated.

In this example ID=2 and consequently a minimum of three hinges is required to induce total collapse.

Since mechanisms (i) and (iv) have a significantly higher associated Mp value these have been selected to combine with the joint mechanism to produce a possible combination:

Mechanism (vi): the addition of mechanisms (i)+(iv)+(v)(a)

|Independent and Combined Mechanisms for Example 8.6|
|---|


||Hinge Position<br><br>|
|---|
| | | | | | | |
|---|---|---|---|---|---|---|---|
| |(i)|(ii)|(iii)|(iv)|(v)| |(vi)=(i)+(iv)+(v)(a)|
| | | | | | | | |
|B (MP)|+2.0θ|−|−|−|(a)|(b)|+2.0θ|
|C1 (Mp)|−θ|−|−|−|+θ|−θ|EH (2.0Mpθ)|
|C2 (Mp)| |−θ| |−|−θ|+θ|−θ|
|C3 (Mp)| |−|−θ|+θ|−θ|+θ|EH (2.0Mpθ)|
|D (Mp)|−|+2.0θ|−|−|−| |−|
|F (Mp)|−|−|+2.0θ|−θ|−| |−|
|G (Mp)|−|−|−θ|−|−| |−θ|
|External Work|60.0θ|20.0θ|22.5θ|22.5θ|−| |82.5θ|
|Internal Work|3.0Mpθ|3.0Mpθ|4.0MPθ|2.0Mpθ|3.0Mpθ| |8.0Mpθ|


|Eliminated hinges|−|−|−|−|−|4.0Mpθ|
|---|---|---|---|---|---|---|
|Combined Mpθ|−|−|−|−|−|4.0MPθ|
|Mp (kNm)|20.0|6.67|5.63|11.25|−|20.63|


Table 8.2

![image 1286](McKenzie - Examples in Structural Analysis_images/imageFile1286.png)

- Figure 8.21


![image 1287](McKenzie - Examples in Structural Analysis_images/imageFile1287.png)

|![image 1288](McKenzie - Examples in Structural Analysis_images/imageFile1288.png)<br><br>Figure 8.22<br><br>|
|---|
|![image 1289](McKenzie - Examples in Structural Analysis_images/imageFile1289.png)|
|8.10 Problems: Plastic Analysis—Rigid-Jointed Frames 2<br><br>|


A series of rigid-jointed frames are indicated in Problems 8.10 to 8.15 in which the relative Mp values and the applied collapse loads are given. In each case determine the required Mp value, the value of the support reactions and sketch the bending moment diagram.

|![image 1290](McKenzie - Examples in Structural Analysis_images/imageFile1290.png)<br><br>Problem 8.10<br><br>![image 1291](McKenzie - Examples in Structural Analysis_images/imageFile1291.png)<br><br>Problem 8.11<br><br><br>![image 1292](McKenzie - Examples in Structural Analysis_images/imageFile1292.png)<br><br>|
|---|


###### Problem 8.12

![image 1293](McKenzie - Examples in Structural Analysis_images/imageFile1293.png)

###### Problem 8.13

![image 1294](McKenzie - Examples in Structural Analysis_images/imageFile1294.png)

###### Problem 8.14

![image 1295](McKenzie - Examples in Structural Analysis_images/imageFile1295.png)

###### Problem 8.15

|8.11 Solutions: Plastic Analysis—Rigid-Jointed Frames 2<br><br>![image 1296](McKenzie - Examples in Structural Analysis_images/imageFile1296.png)|
|---|


|![image 1297](McKenzie - Examples in Structural Analysis_images/imageFile1297.png)|
|---|


|![image 1298](McKenzie - Examples in Structural Analysis_images/imageFile1298.png)|
|---|


|![image 1299](McKenzie - Examples in Structural Analysis_images/imageFile1299.png)|
|---|


|![image 1300](McKenzie - Examples in Structural Analysis_images/imageFile1300.png)|
|---|


|![image 1301](McKenzie - Examples in Structural Analysis_images/imageFile1301.png)|
|---|


|![image 1302](McKenzie - Examples in Structural Analysis_images/imageFile1302.png)|
|---|


|![image 1303](McKenzie - Examples in Structural Analysis_images/imageFile1303.png)|
|---|


|![image 1304](McKenzie - Examples in Structural Analysis_images/imageFile1304.png)|
|---|


|![image 1305](McKenzie - Examples in Structural Analysis_images/imageFile1305.png)|
|---|


|![image 1306](McKenzie - Examples in Structural Analysis_images/imageFile1306.png)|
|---|


|![image 1307](McKenzie - Examples in Structural Analysis_images/imageFile1307.png)|
|---|


|![image 1308](McKenzie - Examples in Structural Analysis_images/imageFile1308.png)|
|---|


|![image 1309](McKenzie - Examples in Structural Analysis_images/imageFile1309.png)|
|---|


|![image 1310](McKenzie - Examples in Structural Analysis_images/imageFile1310.png)|
|---|


|![image 1311](McKenzie - Examples in Structural Analysis_images/imageFile1311.png)|
|---|


|![image 1312](McKenzie - Examples in Structural Analysis_images/imageFile1312.png)|
|---|


|![image 1313](McKenzie - Examples in Structural Analysis_images/imageFile1313.png)|
|---|


|![image 1314](McKenzie - Examples in Structural Analysis_images/imageFile1314.png)|
|---|


|![image 1315](McKenzie - Examples in Structural Analysis_images/imageFile1315.png)|
|---|


|![image 1316](McKenzie - Examples in Structural Analysis_images/imageFile1316.png)|
|---|


|![image 1317](McKenzie - Examples in Structural Analysis_images/imageFile1317.png)|
|---|


|![image 1318](McKenzie - Examples in Structural Analysis_images/imageFile1318.png)|
|---|


|![image 1319](McKenzie - Examples in Structural Analysis_images/imageFile1319.png)|
|---|


|![image 1320](McKenzie - Examples in Structural Analysis_images/imageFile1320.png)|
|---|


|![image 1321](McKenzie - Examples in Structural Analysis_images/imageFile1321.png)|
|---|


|![image 1322](McKenzie - Examples in Structural Analysis_images/imageFile1322.png)|
|---|


|![image 1323](McKenzie - Examples in Structural Analysis_images/imageFile1323.png)|
|---|


|![image 1324](McKenzie - Examples in Structural Analysis_images/imageFile1324.png)|
|---|


|![image 1325](McKenzie - Examples in Structural Analysis_images/imageFile1325.png)|
|---|


![image 1326](McKenzie - Examples in Structural Analysis_images/imageFile1326.png)

#### 8.12 Gable Mechanism

Another type of independent mechanism which is characteristic of pitched roof portal frames is the Gable Mechanism, as shown in Figure 8.23 with simple beam and sway mechanisms.

|![image 1327](McKenzie - Examples in Structural Analysis_images/imageFile1327.png)<br><br>Figure 8.23<br><br>|
|---|


In the beam and gable mechanisms the rafter of the frame is sloping and it is necessary to evaluate the displacement in the direction of the load. i.e. not necessarily perpendicular to the member as in previous examples. Consider the typical sloping member ABC shown in Figure 8.24(a) which is subject to a horizontal and a vertical load as indicated.

|![image 1328](McKenzie - Examples in Structural Analysis_images/imageFile1328.png)<br><br>Figure 8.24<br><br>|
|---|


Assume that during the formation of a mechanism the centre-of-rotation of the member is point A and point C displaces in a perpendicular direction to ABC to point C'. For small rotations (α) of member ABC, δC′=LACα

The vertical and horizontal displacements of C are given by δC,vertical=δC Cosθ=LADα and δC,horizontal=δC Sinθ=LCDα as shown in Figure 8.24(b), where θ is the angle of the member ABC to the horizontal. The vertical and horizontal displacements at point B can be determined in a similar manner.

These values can then be used in the calculation of external work for the work equation.

|8.13 Instantaneous Centre of Rotation|
|---|


In more complex frames it is convenient to use the ‘instantaneous centre of rotation method’ when developing a collapse mechanism. The technique is explained below in relation to a simple rectangular portal frame and subsequently in Example 8.7.

Consider the asymmetric rectangular frame shown in Figure 8.25 in which there are two independent mechanisms, one beam and one sway. The frame requires three hinges to cause collapse. Both mechanisms can combine to produce a collapse mechanism with hinges developing at A, C and D. In this mechanism there are three rigid-links, AB′C′, C′D′ and D′E as shown.

|![image 1329](McKenzie - Examples in Structural Analysis_images/imageFile1329.png)<br><br>Figure 8.25<br><br>|
|---|


The centre-of-rotation for link AB′C′ is at A and the remote end C moves in a direction perpendicular to line AC shown. The centre-of-rotation for link D′E is at E and the remote end D moves in a direction perpendicular to line ED shown.

In the case of link C′D′, the centre-of-rotation must be determined by considering the direction of movement of each end. C′ moves in a direction perpendicular to AC and consequently the centre-of-rotation must line on an extension of this line. Similarly, it must also lie on a line perpendicular to the movement of D, i.e. on an extension of ED. This construction is shown in Figure 8.26(a). The position of this centre-ofrotation is known as the instantaneous centre-of-rotation and occurs at the instant of collapse.

|![image 1330](McKenzie - Examples in Structural Analysis_images/imageFile1330.png)|
|---|


###### The work equations can be developed and the required Mp value determined by considering the rotation of the hinges and the displacements of the loads. Consider the geometry shown in Figure 8.26(b) and equate the displacements in terms of θ, β and α as follows:

|![image 1331](McKenzie - Examples in Structural Analysis_images/imageFile1331.png)|
|---|


(Note: equating the horizontal displacement of point C will give the same result, i.e. δC,horizontal=3.0α= 6.0θ) The rotation at the hinge at A=α=2.0θ Note: no internal work is done at support E Internal Work Done=External Work Done

|![image 1332](McKenzie - Examples in Structural Analysis_images/imageFile1332.png)|
|---|


The reader should confirm that this is the critical value by calculating the reactions and checking that the bending moment on the frame does not exceed the appropriate Mp value for any member. (Note: In the case of member BCD this is equal to 2.0Mp=40 kNm).

|8.14 Example 8.7: Pitched Roof Frame|
|---|


A non-uniform, asymmetric frame is pinned at support A, fixed at support F and is required to carry collapse loads as indicated in Figure 8.27. Determine the minimum required value of Mp.

|![image 1333](McKenzie - Examples in Structural Analysis_images/imageFile1333.png)<br><br>Figure 8.27<br><br>|
|---|


Factored loads: as given

|![image 1334](McKenzie - Examples in Structural Analysis_images/imageFile1334.png)|
|---|


Kinematic Method:

Consider each independent mechanism separately.

|![image 1335](McKenzie - Examples in Structural Analysis_images/imageFile1335.png)<br><br>![image 1336](McKenzie - Examples in Structural Analysis_images/imageFile1336.png)<br><br>![image 1337](McKenzie - Examples in Structural Analysis_images/imageFile1337.png)<br><br>|
|---|
|![image 1338](McKenzie - Examples in Structural Analysis_images/imageFile1338.png)|


###### Combined Mechanism (iv): [2×mechanism (i)]+mechanism (iii) which eliminates a hinge at C

|![image 1339](McKenzie - Examples in Structural Analysis_images/imageFile1339.png)|
|---|


The reader should confirm that this is the critical value by calculating the reactions and checking that the bending moment on the frame does not exceed the appropriate Mp value for any member. (Note: In the case of support F this is equal to 2.0Mp=93.70 kNm).

###### Alternatively, adding the virtual work equations:

|![image 1340](McKenzie - Examples in Structural Analysis_images/imageFile1340.png)|
|---|


The combined mechanism can be evaluated in a Table as shown:

|Independent and Combined Mechanisms for Example 8.7|
|---|


||Hinge Position|
|---|
||(i)|
|---|
| | | | |
|---|---|---|---|---|---|
| | |(ii)|(iii)|(iv)|(v)=2(i)+(iii)|
| | | | | | |
|B (Mp)|+2.0θ|–|–|–|+2.0 θ|
|C (Mp)|−θ|−θ|–|+2.0θ|EH (2.0Mpθ)|
|D (Mp)|–|+2.00|–|–|–|


|E (Mp)|–|−θ|+θ|−2.25θ|−2.25θ|
|---|---|---|---|---|---|
|F (2Mp)|–|–|−2.0θ|–|–|
|External Work|60.0θ|60.0θ|63.0θ|290.0θ|410.0θ|
|Internal Work|3.0Mpθ|4.0Mpθ|3.0Mpθ|6.75Mpθ|10.75Mpθ|
|Eliminated hinges|–|–|–|–|2.0Mpθ|
|Combined Mpθ|–|–|–|–|8.75Mpθ|
|Mp (kNm)|20.0|15.0|21.0|42.96|46,86|


|![image 1341](McKenzie - Examples in Structural Analysis_images/imageFile1341.png)<br><br>Figure 8.28<br><br>|
|---|


|8.15 Problems: Plastic Analysis—Rigid-Jointed Frames 3|
|---|


A series of rigid-jointed frames are indicated in Problems 8.16 to 8.21 in which the relative Mp values and the applied collapse loads are given. In each case determine the required Mp value, the value of the support reactions and sketch the bending moment diagram.

|![image 1342](McKenzie - Examples in Structural Analysis_images/imageFile1342.png)<br><br>Problem 8.16<br><br>![image 1343](McKenzie - Examples in Structural Analysis_images/imageFile1343.png)<br><br>Problem 8.17<br><br><br>|
|---|


![image 1344](McKenzie - Examples in Structural Analysis_images/imageFile1344.png)

###### Problem 8.18

![image 1345](McKenzie - Examples in Structural Analysis_images/imageFile1345.png)

###### Problem 8.19

![image 1346](McKenzie - Examples in Structural Analysis_images/imageFile1346.png)

###### Problem 8.20

![image 1347](McKenzie - Examples in Structural Analysis_images/imageFile1347.png)

###### Problem 8.21

|8.16 Solutions: Plastic Analysis—Rigid-Jointed Frames 3<br><br>![image 1348](McKenzie - Examples in Structural Analysis_images/imageFile1348.png)|
|---|


|![image 1349](McKenzie - Examples in Structural Analysis_images/imageFile1349.png)|
|---|


|![image 1350](McKenzie - Examples in Structural Analysis_images/imageFile1350.png)|
|---|


|![image 1351](McKenzie - Examples in Structural Analysis_images/imageFile1351.png)|
|---|


|![image 1352](McKenzie - Examples in Structural Analysis_images/imageFile1352.png)|
|---|


|![image 1353](McKenzie - Examples in Structural Analysis_images/imageFile1353.png)|
|---|


|![image 1354](McKenzie - Examples in Structural Analysis_images/imageFile1354.png)|
|---|


|![image 1355](McKenzie - Examples in Structural Analysis_images/imageFile1355.png)|
|---|


|![image 1356](McKenzie - Examples in Structural Analysis_images/imageFile1356.png)|
|---|


|![image 1357](McKenzie - Examples in Structural Analysis_images/imageFile1357.png)|
|---|


|![image 1358](McKenzie - Examples in Structural Analysis_images/imageFile1358.png)|
|---|


|![image 1359](McKenzie - Examples in Structural Analysis_images/imageFile1359.png)|
|---|


|![image 1360](McKenzie - Examples in Structural Analysis_images/imageFile1360.png)|
|---|


|![image 1361](McKenzie - Examples in Structural Analysis_images/imageFile1361.png)|
|---|


|![image 1362](McKenzie - Examples in Structural Analysis_images/imageFile1362.png)|
|---|


|![image 1363](McKenzie - Examples in Structural Analysis_images/imageFile1363.png)|
|---|


|![image 1364](McKenzie - Examples in Structural Analysis_images/imageFile1364.png)|
|---|


|![image 1365](McKenzie - Examples in Structural Analysis_images/imageFile1365.png)|
|---|


|![image 1366](McKenzie - Examples in Structural Analysis_images/imageFile1366.png)|
|---|


|![image 1367](McKenzie - Examples in Structural Analysis_images/imageFile1367.png)|
|---|


|![image 1368](McKenzie - Examples in Structural Analysis_images/imageFile1368.png)|
|---|


|![image 1369](McKenzie - Examples in Structural Analysis_images/imageFile1369.png)|
|---|


|![image 1370](McKenzie - Examples in Structural Analysis_images/imageFile1370.png)|
|---|


|![image 1371](McKenzie - Examples in Structural Analysis_images/imageFile1371.png)|
|---|


|![image 1372](McKenzie - Examples in Structural Analysis_images/imageFile1372.png)|
|---|


|![image 1373](McKenzie - Examples in Structural Analysis_images/imageFile1373.png)|
|---|


|![image 1374](McKenzie - Examples in Structural Analysis_images/imageFile1374.png)|
|---|


|![image 1375](McKenzie - Examples in Structural Analysis_images/imageFile1375.png)|
|---|


|![image 1376](McKenzie - Examples in Structural Analysis_images/imageFile1376.png)|
|---|


|![image 1377](McKenzie - Examples in Structural Analysis_images/imageFile1377.png)|
|---|


|![image 1378](McKenzie - Examples in Structural Analysis_images/imageFile1378.png)|
|---|


![image 1379](McKenzie - Examples in Structural Analysis_images/imageFile1379.png)

### Appendix 1 Elastic Section Properties of Geometric Figures

A = Cross-sectional area y1 or y2 = Distance to centroid zxx = Elastic Section Modulus about the x-x axis rxx = Radius of Gyration about the x-x axis Ixx = Second Moment of Area about the x-x axis

|![image 1380](McKenzie - Examples in Structural Analysis_images/imageFile1380.png)|
|---|


|![image 1381](McKenzie - Examples in Structural Analysis_images/imageFile1381.png)|
|---|


|![image 1382](McKenzie - Examples in Structural Analysis_images/imageFile1382.png)|
|---|


![image 1383](McKenzie - Examples in Structural Analysis_images/imageFile1383.png)

### Appendix 2 Beam Reactions, Bending Moments and Deflections

Simply Supported Beams Cantilever Beams Propped Cantilevers Fixed-End Beams

|![image 1384](McKenzie - Examples in Structural Analysis_images/imageFile1384.png)|
|---|


|![image 1385](McKenzie - Examples in Structural Analysis_images/imageFile1385.png)|
|---|


|![image 1386](McKenzie - Examples in Structural Analysis_images/imageFile1386.png)|
|---|


|![image 1387](McKenzie - Examples in Structural Analysis_images/imageFile1387.png)|
|---|


|![image 1388](McKenzie - Examples in Structural Analysis_images/imageFile1388.png)|
|---|


![image 1389](McKenzie - Examples in Structural Analysis_images/imageFile1389.png)

### Appendix 3 Matrix Algebra

Product of a Matrix and a Vector:

Consider three variables a1, α2 and α3 which are related to three other variables c1, c2 and c3 by the three equations (1), (2) and (3) as indicated:

![image 1390](McKenzie - Examples in Structural Analysis_images/imageFile1390.png)

Equation

- (1)

![image 1391](McKenzie - Examples in Structural Analysis_images/imageFile1391.png)

Equation

- (2)

![image 1392](McKenzie - Examples in Structural Analysis_images/imageFile1392.png)

Equation

- (3)


these equations can be represented in matrix form as:

i.e.

![image 1393](McKenzie - Examples in Structural Analysis_images/imageFile1393.png)

where b11, b12, b13 etc. are the coefficients for the square matrix [B].

###### Clearly for known values of c1, c2 and c3 the values of a1, α2 and α3 can be determined directly. If however, it is required to determine the ‘c’ values for given ‘a’ values then the relationship must be re-written as:

![image 1394](McKenzie - Examples in Structural Analysis_images/imageFile1394.png)

and the INVERT of matrix [B] must be obtained.

###### The invert of a matrix can be defined as:

![image 1395](McKenzie - Examples in Structural Analysis_images/imageFile1395.png)

where adj B is the adjoint of matrix [B] and is equal to the transpose of the co-factor matrix [Bc] of matrix [B], i.e.

![image 1396](McKenzie - Examples in Structural Analysis_images/imageFile1396.png)

The co-factor matrix is given by replacing each element in the matrix by its’ co-factor, i.e.

![image 1397](McKenzie - Examples in Structural Analysis_images/imageFile1397.png)

![image 1398](McKenzie - Examples in Structural Analysis_images/imageFile1398.png)

- Example A.1 Determine the values of c1, and c2 given that:


![image 1399](McKenzie - Examples in Structural Analysis_images/imageFile1399.png)

Solution:

![image 1400](McKenzie - Examples in Structural Analysis_images/imageFile1400.png)

###### c1={+(0.8×40.0)−(0.6×45.0)}=+5.0 c2={−(0.2×40.0)+(0.4×45.0)}=+10.0

- Example A.2 Determine the values of c1, c2 and c3 given that:


![image 1401](McKenzie - Examples in Structural Analysis_images/imageFile1401.png)

Solution:

###### Determine the co-factor matrix:

![image 1402](McKenzie - Examples in Structural Analysis_images/imageFile1402.png)

Determinant of [B]:

![image 1403](McKenzie - Examples in Structural Analysis_images/imageFile1403.png)

### Index

###### A

Arbitrary sway force 388 Aspect ratio 54 Axial rigidity 20 Axial stiffness 475 Axial stress 23

###### B

Beam deflection Beam mechanism (plastic) 556, 564 Bending moment 157, 159 diagrams 163, 170 free 271, 287 557 fixed 271, 282 557 sign convention: beams 163 sign convention: frames 316 Bending stiffness (absolute) 269 Bending stiffness (relative) 270 Bending stress 23, 26 27, 40, 43, 53 Brittle materials 23, 26 Buckling 25, 54 432, 455 critical stress 436, 440 effective buckling length 438, 439 448 intermediate elements 433, 436 444 limiting slenderness 445 mode shapes (pinned columns) 438 Perry-Robertson formula 441

Perry strut formula 445, 448 secondary stresses 434 short elements 433, 435 444 slenderness 432, 433 441, 448 slender elements 433, 436 444

###### C

Carry-over moment 270 Castigliano’s 1st Theorem 113, 114 115 Centre-of-gravity 32 Centroid 28, 32, 38 Centroidal axes 28 Coefficient of thermal expansion 27 Collapse (plastic) full 556 partial 556 Collapse load (plastic) 51 Combined mechanism (plastic) 589, 591 Compact section 54, 56 Compound pin-jointed frames 15 Compound section 42, 452 Connections 8 Co-ordinate systems global 474, 484 local 481,482 Critical load Critical stress 436, 440 Cross-sectional area 28, 38

###### D

Deflection beams 183, 208 222 pin-jointed frames 116, 122 222 Degree-of-indeterminacy 8, 11 15, 21

Degrees-of-freedom 1, 18 21, 477, 483 beam elements 475, 476

- 481 pin-jointed frames 18 rigid-jointed frames 18 Direct stiffness method 474, 504 Distribution factors 278 Distribution of load 10


###### E

Effective buckling length 438, 439 448 Elastic cross-section properties Elastic limit 23, 444 Elastic moment of resistance 52 Elastic neutral axis 28, 40 Elastic section modulus 28, 43 45, 53, 56 Elasto-plastic moment 52 Element co-ordinate system 474 Element displacement vector 474, 488 Element end-forces vector 474, 489 Element stiffness matrix 474, 476 Encastre beam 272 Equilibrium 1, 3, 9, 11 Equivalent nodal loads 487 Equivalent UDL 189, 191 Euler load/stress 437, 440 444 European column curves 445 Perry factor 445 Perry-strut formula 445 Robertson constant 445, 446 External work done (plastic) 561, 562

###### F

Factor of safety 51 First moment of area 33, 54 Fixed supports 15 Fixed-end moment 271, 486 Foundations 7, 8 Fracture 24 Frames pin-jointed 4, 8 18, 62, 121, 140 rigid-jointed 4, 8

- 314, 315, 324, 340, 346, 385, 397 plastic analysis 586, 593 615, 654 Free bending moment 271, 557


###### G

Gable mechanism 586, 648 Global co-ordinate system 474, 482 484

###### H

Hooke’s Law 23, 25, 27

###### I

Independent mechanism (plastic) 557, 589 Indeterminacy 3, 8, 21 555 pin-jointed frames 11, 18 rigid-jointed frames 15, 19 Instability (buckling) 455 Instantaneous centre of rotation 649 Internal Work done (plastic) 561, 562

|J<br><br>Joint mechanism (plastic) 586, 611<br><br>K<br><br>Kinematic method (plastic analysis) 557, 560<br><br>L<br><br>Laced section 450 Lack-of-fit 120 Lateral distribution 9 Limiting elastic moment 52 Limiting slenderness 445 Line diagrams 4 Loading 9 collapse 51 Load distribution 10 Load factor 51 Load path 7 Local co-ordinate system 481, 482 Lower bound solution (plastic) 557, 586<br><br>M<br><br>MaCaulay’s Method 183, 191 477 Mathematical modelling 4, 9 Mechanism condition Method of joint-resolution 62, 65 Method of sections 62, 67 Method of tension coefficients 62, 93 Modelling 4, 9 Modulus of elasticity 25, 27 Modulus of rigidity (shear) 26 Modulus of rupture (bending) 26 Modulus of rupture (torsion) 26 Moment connections 314, 315 Moment distribution 269, 289 arbitrary sway force 388<br><br>|
|---|


absolute stiffness 270 carry-over moment 270, 282 338 distribution factors 278, 281 338 effect of pinned end 270, 282 relative stiffness 270, 281 out-of-balance moment 282, 284 338 prop force 386, 387 sway force 386 Moment of area (1st) 33, 54 Moment of area (2nd) 41, 45

###### N

Necking 23 Neutral axis elastic 28, 40

- plastic 52, 53, 57 Neutral surface 40 No-sway frames 340, 346 386 Nodal displacements 476 Nodal forces 489


###### O

One-way spanning slabs 10 Out-of-balance moment 282

###### P

Parallel axis Theorem 28, 41 Perry factor 445 Perry-Robertson Formula 441, 444 Perry strut formula 445, 448 Pin-jointed frames 4, 8, 18 62, 121, 140 Pin-jointed space frame 93 Pinned support 8, 11 Plastic collapse (full) 556

equilibrium condition 556 mechanism condition 556 yield condition 556 Plastic collapse (partial) 556 Plastic cross-section properties 51, 57 Plastic hinge 52, 53 555 Plastic moment of resistance 52, 53 555 Plastic neutral axis 52, 53, 57 Plastic section 52, 54, 56 Plastic section modulus 53, 54 56, 57 Poisson’s ratio 27 Principle of superposition 202 Prop force 386, 387 Proportional limit 23 Propped cantilever 275

###### R

Radius of curvature 183 Radius of gyration 41, 42 436 Reactions 7 Redundancy 16 redundant member 11, 13 135 redundant reaction 11, 12 Rigid connections 8, 314 315 Rigid-jointed Frames 4, 8, 314 324, 340, 346, 385, 397 Robertson constant 445, 446 Roller support 8, 11 Rotational stiffness 269

###### S

Secant modulus 25 Secondary stresses 314, 434 Section modulus elastic 28, 43 45, 53, 56

- plastic 53, 54 56, 57 Second moment of area 28, 41 42, 45 Section classification 54 Semi-compact section 54, 56 Settlement 289, 299 Shape factor 54, 57 Shear force 157, 159 Shear force diagram 159, 170 Shear rigidity 26 Sign conventions bending moments for beams 163 shear forces 161 static equilibrium 2 Simple connections 8, 315 Simple pin-jointed frames 12, 13 Slender section 54, 56 Slenderness ratio 432, 433 441, 448 Strain energy axial load effects 113, 114 bending effects Stability 3 Static equilibrium 2, 63 Static method (plastic analysis) 557 Statical determinacy 3 Statical indeterminacy 3 Statically determinate beams 157 Statically determinate frames 314, 315 324 Statically indeterminate beams 252, 258 Statically indeterminate frames 315 Stiffness 474 absolute 269 axial 475 relative 270, 281 Stiffness coefficients 477 Stiffness matrix element 474, 476


- 482 structural 474, 483 486 Strain 23, 25 Strain energy (axial effects) 113 strain energy (bending effects) 208


Strain-hardening 23, 51 Stress 23 axial 23 bending 26, 27, 40 43, 53 permissible 51 working 51 yield 51, 52 Structural degrees-of-freedom 18 Structural displacement vector 484, 488 Structural load vector 484, 486 Structural loading 9 Struts 32 Sub-frames Superposition 120, 135 202, 285, 387, 477 Support encastre (fixed) 15 pinned 8, 11 14, 15 roller 8, 11 14, 15 Sway force 386 Sway frames 385, 386 397 Sway mechanism 586, 648

###### T

Tangent modulus 25 Tangent Modulus Theorem 441, 444 Temperature change 27 Tension coefficient 93, 94 Thermal effects 27, 120 Ties 62 Transformation matrix 482 simple 12, 13 compound 15 Trusses 94, 95 Two-dimensional force systems 2 Two-way spanning slabs 10

|U<br><br>Ultimate strain 23 Ultimate stress 51 Ultimate tensile strength 26 Unit load Method 113 determinate pin-jointed frames 116, 122 indeterminate pin-jointed frames 135, 140 beams (deflection) 208 indeterminate beams 252, 258 269 Upper bound solution (plastic) 557, 586 Upper yield stress 24<br><br>V<br><br>Virtual work 561<br><br>W<br><br>Work equations (plastic analysis) internal work-done 561, 562 external work-done 561, 562<br><br>Y<br><br>Yield condition 556 Yield point 26, 51 Yield strength 26, 433 Yield stress 23, 51 52, 436, 444 Young’s modulus 23, 27<br><br>|
|---|


