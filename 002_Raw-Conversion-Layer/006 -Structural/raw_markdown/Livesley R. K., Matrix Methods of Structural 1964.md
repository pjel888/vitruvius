![image 1](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile1.png)

THE COMMONWEALTH AND INTERNATIONAL LIBRARY OF SCIENCE, TECHNOLOGY, ENGINEERING AND LIBERAL STUDIES

Joint Chairmen of the Honorary Editorial Advisory Board SIR ROBERT ROBINSON, o.M., F.R.S., London DEAN ATHELSTAN SPILHAUS, Minnesota

Publisher ROBERT MAXWELL, M.c. STRUCTURES AND SOLID BODY MECHANICS DIVISION

VOLUME THREE

General Editor: B. G. NEAL

###### MATRIX METHODS OF STRUCTURAL ANALYSIS

![image 2](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile2.png)

##### Matrix Methods of Structural Analysis

###### R. K. LIVESLEY

###### M.A., Ph.D. University Lecturer in Engineering Fellow of Churchill College Cambridge

yjgff

PERGAMON PRESS

OXFORD · LONDON · EDINBURGH · NEW YORK TORONTO · SYDNEY · PARIS · BRAUNSCHWEIG

![image 3](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile3.png)

Pergamon Press Ltd., Headington Hill Hall, Oxford 4 & 5 Fitzroy Square, London W.l Pergamon Press (Scotland) Ltd., 2 & 3 Teviot Place, Edinburgh 1 Pergamon Press Inc., Maxwell House, Fairview Park, Elmsford,

New York 10523 Pergamon of Canada Ltd., 207 Queen's Quay West, Toronto 1

Pergamon Press (Aust.) Pty. Ltd., 19a Boundary Street, Rushcutters Bay, Sydney, N.S.W. 2011, Australia Pergamon Press S.A.R.L., 24 rue des Écoles, Paris 5e Vieweg & Sohn GmbH, Burgplatz 1, Braunschweig Copyright © 1964 Pergamon Press Ltd. All Rights Reserved. No part of this publication may be reproduced, stored in a retrieval system, or transmitted, in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior permission of Pergamon Press Ltd. First edition 1964 Reprinted with corrections 1969 Library of Congress Catalog Card No. 63-19535

Printed in Great Britain by A. Wheaton & Co., Exeter

This book is sold subject to the condition that it shall not, by way of trade, be lent, resold, hired out, or otherwise disposed of without the publisher's consent, in any form of binding or cover other than that in which

it is published.

- 08 010355 3 (flexicover)
- 08 010356 1 (hard cover)


![image 4](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile4.png)

###### PREFACE

THE concepts and notation of matrix algebra have for a long time been part of the normal stock-in-trade of the applied mathematician. This book shows how these concepts can be used to provide a general systematic approach to the analysis of structures.

An approach which uses the techniques of matrix algebra has two quite distinct virtues in structural analysis. In the first place the notation provides a precise yet compact symbolism for the discussion of basic structural principles. It encourages the development of systems of analysis which are applicable to a wide range of structures, and reveals connections between methods which at first sight might appear to be unrelated. Because of this feature, the book is arranged in a way which distinguishes between differences of method rather than differences of structural form. Thus the divisions are between the "equilibrium" and "compatibility" approaches, between linear and non-linear behaviour, rather than between portal frames, trusses and continuous beams.

In the second place the use of matrix theory makes it possible to reduce the detailed numerical operations required in the analysis of a given structure to systematic processes of matrix manipulation. In terms of human computational effort these processes are tedious, and often involve more labour than is required by conventional methods of analysis. For this reason matrix methods are rarely advantageous if all the arithmetic has to be done by hand. However, numerical operations on matrices can be carried out very easily on digital computers, and it is the development of these machines during the last decade which has

ix

###### A ·

![image 5](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile5.png)

###### X MATRIX METHODS OF STRUCTURAL ANALYSIS

made the analysis of structures by matrix methods a practical proposition. Many of the general-purpose computer programs now available for routine structural analysis are based on matrix methods similar to those described in this book.

It follows that the book has two purposes. The first is to use matrix notation to present the basic principles of structural analysis in a way which is general yet at the same time compact and precise. The second is to provide practising engineers with an account of the analytical techniques which experience has shown to be useful when programming structural problems for digital computers. It may be argued that relatively few engineers will ever be actively engaged in computer programming and that one can obtain correct results from an existing program without understanding the method on which it is based. Nevertheless, most structural engineers will have more confidence in results obtained from computers if they know something of the way in which the results are produced.

Since I feel that the case for matrix methods rests largely on the availability of automatic computers, I have restricted the discussion of numerical techniques to a brief account of the more elementary methods of solving systems of linear equations, inverting matrices, and finding eigenvalues and eigenvectors. All present-day computers have "library routines" for carrying out these standard matrix processes—they are in fact permanently built into many machines. The construction of such routines is a job for the computer speciahst, and the average machine user is normally quite happy to remain in ignorance of the methods which they employ.

This does not mean that matrix methods can be fully understood without a certain amount of practice in the manipulation of numerical matrices on, say, a desk calculating machine. However, the aim of such practice should be a better understanding of the real meaning of symbolic expressions containing vectors and matrices, rather than the mere acquisition of manual dexterity in handling numbers. It seems unnecessary nowadays for the

![image 6](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile6.png)

###### PREFACE XI

average engineer to learn the systematic tabular methods and checking procedures which have been developed for the manual solution of large systems of equations.

In general I have assumed that the reader has a fair working knowledge of the more important techniques of structural analysis, and although all the matrix theory used in the book is covered in the chapter on matrices, a general mathematical background is also assumed. In both cases the level is about that which a student taking a degree course in civil engineering might be expected to have reached at the start of his final undergraduate year.

Matrix methods are at their best when applied to complex structures which are difficult to solve by traditional means. When used to solve the relatively trivial problems so often used as examples in structural textbooks they tend to look cumbersome and rather absurd. It should be understood, therefore, that the examples in the text have been introduced to illustrate particular points in the general theory—it is not suggested that they are problems for which a matrix solution is most appropriate in practice.

This feature of matrix methods also explains the absence of the usual problems for detailed solution by the reader. In general I have considered the process of analysing a structure to be complete when it has been reduced to a series of numerical operations which can be carried out by standard methods on a computer. It is this reduction which is the real responsibility of the structural analyst—the production of correct numerical answers in particular cases follows automatically (unless a fault occurs in the computer) provided that the matrix operations have been specified correctly.

For the sake of brevity and simplicity I have restricted the analysis to skeletal structures. Matrix methods have, of course, been applied successfully to both stressed-skin aircraft structures and shell roofs, but a satisfactory treatment of such structures would have made the book considerably longer. This restriction

![image 7](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile7.png)

###### XÜ MATRIX METHODS OF STRUCTURAL ANALYSIS

must be borne in mind when making comparisons between the "equilibrium" and "compatibility" methods. When dealing with skeletal structures the equilibrium method has an advantage, since it works in terms of physically obvious variables—the joint displacements. The compatibility method, in contrast, requires a study of the degree of indeterminacy of a structure before the corresponding basic variables— the self-equilibrating "redundant" load-pairs, can be defined. In more general structures, however, the definition of suitable displacement variables may require as much thought as the definition of suitable redundant loadpairs.

Although matrix methods have only become popular during the last decade or so there is already a considerable body of literature on the subject. Five recent books are given in the list of references,! and the reader will find an excellent bibliography and historical survey in a paper by Argyris (Argyris, 1958). It is difficult to say who first introduced matrix methods into structural analysis. Certainly no one name springs to mind with the inevitability of a Southwell or a Hardy Cross. As with other innovations, the same ideas seem to have occurred to a number of different research workers at about the same time. The form of presentation adopted in this book owes a great deal to the classic paper by Kron (Kron, 1944), and to a paper on the related subject of network topology by Synge (Synge, 1951).

It is a pleasure to be able to record my gratitude to those who have assisted, directly or indirectly, in the writing of this book. In particular I have to thank Professor J. A. L. Matheson for suggesting to me that the application of computers to structural analysis was a worthwhile subject for research, and for encouraging my early work in this field. I am indebted to Professor T. M. Charlton and Dr. F. Leckie for fruitful discussions on points of structural theory, and to the many friends, first in the Computing Machine Laboratory at Manchester, and later in the Mathematical

t A list of references will be found at the end of the book.

![image 8](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile8.png)

###### PREFACE xiii

Laboratory at Cambridge, who have helped me in the development of practical computer programs for structural analysis. Finally I must thank the general Editor of this series, Professor

- B. G. Neal, for his suggestions and comments during the preparation of this book.


R. K. LIVESLEY

Cambridge

![image 9](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile9.png)

###### CHAPTER 1

###### Introduction

THE development of automatic computers during the last decade or so has stimulated a great deal of research work in many branches of applied mathematics. Much of this activity has naturally been concerned with the development of numerical techniques suitable for use with automatic computers, and in the field of structural analysis it has led to the development of methods which use the ideas of matrix algebra.

The use of matrix notation has two advantages in structural analysis. From the theoretical point of view it allows one to discuss methods of analysis in a manner which is compact and precise, but at the same time quite general. Thus it facilitates the treatment of structural theory as a unified whole, without the fundamental principles being obscured by computational devices on the one hand or physical differences between structures on the other. From the practical point of view it provides a systematic approach to the analysis of structures which forms a very suitable basis for the development of computer programs.

In contrast to these advantages it must be admitted that matrix methods are characterized by a large amount of systematic calculation, and their value in practical structural analysis depends on the availability of automatic computers to carry out the numerical work. It follows that their main field of application is the analysis of large and complex structures, where the traditional manual methods require an excessive amount of human effort. In simple problems where existing techniques are quite satisfactory little is to be gained from a matrix approach.

1

![image 10](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile10.png)

###### 2 MATRIX METHODS OF STRUCTURAL ANALYSIS

Although matrix methods are general in application their essential features are most easily demonstrated by applying them to particular types of engineering structure. For the sake of simplicity this book is restricted to a consideration of skeletal structures. By a skeletal structure we mean one which can be represented diagrammatically by a series of lines (corresponding to the members) meeting at points (corresponding to the joints). Thus we shall consider structures formed from elements such as beams, columns, struts and ties, but not structures whose elements include flat plates or curved shells. Within this limitation the aim of the book is to present an account of structural theory which is

- as general as possible. The purpose of the book is to emphasize general principles

rather than to provide a handbook of practical structural computing. Detail not essential to the main line of argument has therefore been kept to a minimum, and material of interest only to the specialist computer programmer has been omitted. For the sake of brevity it is assumed that the reader has some familiarity with the traditional methods of structural analysis.

Although one may argue that the complete analysis of a structure implies the determination of the stress and displacement

- at every point, in the case of a skeletal structure interest is largely centred on the displacements of the joints and on the internal forces and moments which act there. The reason for this is that the complete pattern of stress and deformation in each member of a skeletal structure can be determined if the forces and moments acting on its ends are known. Once these forces and moments have been found, the detailed calculation of the conditions at internal points depends only on the characteristics of the member and not on the position which it occupies in the structure. In general we shall regard an analysis as complete when the displacements of the joints of a structure and the forces and moments acting on the ends of its members have been found.


![image 11](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile11.png)

INTRODUCTION 3

###### 1.1. The Aim of Matrix Methods

In all but the simplest structures numerical values of stresses and displacements cannot be found merely by substituting numbers into known algebraic formulae. More complicated calculations are required, and in many cases the structural engineer is faced with a wide range of alternative methods. His choice of method is normally governed partly by the degree of accuracy which he requires and partly by his training and inclinations. When comparing methods which are equally accurate he is likely to base his choice on two considerations—the amount of numerical effort involved, and the ease with which mistakes in the calculation can be detected and rectified. In general he will probably favour a method in which he can make use of experience gained in the analysis of similar structures, particularly if the method is one which allows him to use his engineering judgement

to make approximations and take short cuts. Another - factor which may affect his choice is the preference of most engineers for numbers which have a direct physical significance. This is one of the attractions of methods such as moment distributionthroughout the calculation the engineer feels that he is carrying out a process which is physically meaningful. In such methods errors can often be detected by applying common sense rather than by strict mathematics, since the numbers in the calculation represent quantities whose magnitudes are known, at least approximately, by the engineer.

All these considerations are based on the assumption that the whole of the analysis, including the numerical work, will be done by the engineer himself—usually a person with considerable knowledge of structural behaviour, but with no great liking for formal mathematics or computation. However, if an automatic computer is available to carry out the numerical work the criteria by which a method is judged to be "good" or "bad" need to be re-examined. The question is not now whether a human being would find the calculation tedious, but whether the method is one

![image 12](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile12.png)

###### 4 MATRIX METHODS OF STRUCTURAL ANALYSIS

which can easily be organized for a machine. If it can, then the method is a "good" one, even though the total number of numerical operations carried out may be considerably greater than in some other method which is less easily mechanized.

An automatic computer is essentially a calculating machine which is controlled by a pre-arranged sequence of instructions, which cause it to carry out the successive steps of a calculation in the correct order. The complete set of instructions is called a program, and the task of preparing the instructions is known as programming. It is important to realize that a program is not restricted to operate on one particular set of numbers. It will cause the computer to carry out the same operations each time it is used, but the numbers forming the raw material of the calculation may be different on each occasion. It follows that if a program exists for a certain type of calculation then all problems for which the calculation provides a means of solution can be regarded as "solved". To say that a solution exists in this sense implies considerably more than the mere existence of a mathematical theory or a numerical technique. It means, in fact, that any problem covered by the program can be solved completely in numerical terms merely by feeding the data of the problem, with the program, into a computer. The results of the calculation will still be correct even if the originator of the problem is ignorant of the mathematical method used by the program, so that the whole process of analysis can be reduced to one of routine dataprocessing.

The simplest problems to program are those in which the numerical data is treated in a systematic manner. The operations of linear algebra, for example, are easily carried out on a computer because they consist of sequences of relatively simple steps repeated many times. All present-day computers are in fact provided with sequences of instructions, known as routines, for carrying out the standard operations of numerical analysis, including those of linear algebra, so that if a structural calculation can be put in the form of a series of these operations the

![image 13](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile13.png)

construction of the complete program merely involves the connecting together of the appropriate routines in the correct order.

It follows that the development of methods of structural analysis in which the numerical work can conveniently be done on an automatic computer calls for an approach which is both systematic and general. The aim is not to minimize the total number of arithmetical operations, but to produce methods which can be applied to many different types of structure, and which make the maximum possible use of standard numerical processes for which computer routines already exist. In achieving these aims it is found that the concepts of matrix algebra are extremely useful.

The fact that matrix methods are linked with automatic computers and use a notation which is unfamiliar to some engineers has led to the belief that they involve new and difficult mathematical and structural concepts. This is not true. A knowledge of the basic operations of matrix algebra is all that is required, while the only structural principles involved are the elementary ones appearing in all structural textbooks. In fact matrix methods such as those which are described in this book are much more closely related to the ideas of men such as Maxwell, Mohr and Müller-Breslau than are many of the methods at present used in hand calculations.

The classical methods of structural analysis developed in the late nineteenth century have the qualities of generality, logical simplicity and mathematical elegance. Unfortunately they often led to tedious calculations when applied to the analysis of practical structures, and in an age when even the desk calculating machine was a rarity this was a serious defect. Succeeding generations of engineers accordingly devoted a great deal of effort to reducing the amount of computation involved. Many ingenious techniques of great practical value appeared, but most of these were only applicable to certain types of structure, and inevitably the increasing number of superficially different methods

![image 14](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile14.png)

tended to obscure the simplicity of the fundamental ideas from which they all originally came. It is also arguable that the need to produce practical analytical techniques for linear structures diverted many research workers who might otherwise have contributed to a better understanding of real structural behaviour, with the result that the investigation of phenomena such as plasticity and instability was delayed.

The main objection to the earlier methods of analysis was that they led to large systems of linear equations, which were difficult to solve by hand. With computers to do the numerical work this objection no longer has the same force, while the advantages of a general approach remain. This explains why matrix methods draw their basic structural approach from the nineteenth rather than the twentieth century.

###### 1.2. Linearity

A linear structure is one in which all displacements and internal loads are linear functions of the applied loads. Most practical structures behave in an approximately linear manner under working loads, so that methods of analysis which assume linearity are the most important ones from the practising engineer's point of view. The assumption of linearity has two important advantages. In the first place it makes the actual job of analysing a structure under a particular loading system a great deal easier. In the second place it allows the superposition of solutions, with a consequent saving of effort when many different loading systems have to be considered.

There are three important causes of non-linear behaviour in structures. The first is non-linear behaviour of the material from which the structure is made. This normally only affects the behaviour of the structure at loads outside the working range, but must obviously be considered in any theory which attempts to predict collapse loads. Mild steel, for example, can undergo considerable plastic deformation before fracture, and this

![image 15](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile15.png)

phenomenon provides a rigid-jointed structure with a reserve of strength which is made use of in the method of plastic limit design.

The second cause is usually known as "gross deformation". In linear analysis it is necessary to assume that the deformations of a structure are small compared with its dimensions, so that the overall shape of the structure is not significantly altered by the process of loading it. More specifically, it is assumed that it is legitimate to write down the equilibrium equations using the lengths, angles, etc., appropriate to the wulistorted structure, whereas strictly these equations must hold in the distorted structure. There are certain types of structure where this approximation cannot be made. One important example is the suspension bridge, where changes in the shape of the supporting cables must be taken into account during the analysis.

The third cause of non-linear behaviour is really a particular case of the second, but is of sufficient practical importance to be mentioned separately. This is the effect which axial forces have on the bending stiffness of members in rigid-jointed frames and trusses. If the axial force in a member is compressive the bending stiffness is reduced, while if it is tensile the stiffness is increased. This effect may in extreme cases cause a structure to become unstable while still remaining elastic.

The most complex structural problems are of course those in which the various causes of non-linearity interact, and in chapter 10 we describe a general technique for dealing with these problems. In most of the remainder of the book, however, it will be assumed that the approximations inherent in the normal linear small-deflexion theory of structures are valid.

1.3. Superposition

As mentioned in the last section, one advantage of a linear theory of structures is that it allows one to apply the principle of superposition. This principle, which holds for any linear structure,

![image 16](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile16.png)

states that the stresses and deformations produced in a structure by a set of loads acting in combination can be obtained by adding up the stresses and deformations produced by each load acting separately. Thus we may analyse the behaviour of a structure under a series of unit loads applied at different points, and then calculate the effects of more complex loading patterns by combining these basic solutions.

An important application of the principle of superposition occurs in the analysis of rigid-jointed structures under distributed loads and concentrated loads applied at points other than the joints. In such circumstances it is advantageous to think of the actual system of applied loads as the sum of two systems and carry out two separate analyses of the structure, the final set of stresses and displacements being obtained by adding the two sets of results.

The first system, which we shall call load system (a), consists of the actual applied loads, including any distributed and mid-span concentrated loads, together with a system of concentrated forces and moments which act at the joints, these forces and moments being of such magnitudes as will prevent any translation or rotation of the joints. The analysis of a structure under a load system of this sort is very simple, since each member is completely fixed at its ends and can therefore be treated quite separately from the rest of the structure. Since this aspect of structural analysis is already fully covered in many standard textbooks it will not be considered here in any detail.

As a result of the analysis for load system (a) we obtain the values of the concentrated forces and moments which must be applied to prevent the joints from displacing. If we reverse the signs of all these forces and moments we obtain a system which we shall call load system (b). It is clear that the sum of load systems (a) and (b) is equal to the actual system of applied loading.

Load system (b) is essentially a system of concentrated loads applied at the joints of the structure, and it is with this type of loading that we shall be concerned in this book. Thus we imagine

![image 17](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile17.png)

###### INTRODUCTION 9

that, where necessary, the analysis of a structure under load system (a) has been completed, so that load system (b) is known. The latter load system is sometimes known as the system of "equivalent fixed-end forces and moments". It should be remembered that the process of replacing a system of distributed loads by the "equivalent" concentrated joint loads is dependent for its validity on the principle of superposition, and that this in turn is only valid for linear structures.

FIG. 1.1.t A load system expressed as the sum of two load systems (a) and (b).

fThe sign convention used in Figs. 1.1 and 1.2 is that used elsewhere in this book. A description of this convention is given in section 3.1.

An example of this transformation is shown in Fig. 1.1. It should be noted that in general both forces and moments must be introduced at the joints of a structure in order to satisfy conditions of equilibrium while at the same time preventing the occurrence of any displacements. It is not necessary, of course,

![image 18](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile18.png)

###### 10 MATRIX METHODS OF STRUCTURAL ANALYSIS

for each "joint" to be an actual physical joint in the structure. If a concentrated load acts at some point along the length of a member it may be convenient to consider its point of application as a joint, and treat the member as two separate members. An example of this technique is shown in Fig. 1.2.

FIG. 1.2. An alternative way of expressing the load system shown in Fig. 1.1.

###### 1.4. Methods of Structural Analysis

As discussed in the previous section, the loading on a linear skeletal structure may always be transformed into a system of "equivalent" concentrated loads applied at the joints. By the analysis of such a structure we mean the determination of the

loads acting on the ends of all the members and the displacements of all the joints, for this equivalent loading. (We use the terms "loads" and "displacements" in a general sense here, to include moments and rotations as well as forces and translations. More precise definitions of these terms are given in section 3.1.)

![image 19](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile19.png)

INTRODUCTION 11 There are three sets of conditions which these loads and dis-

placements must satisfy. These conditions are:

(1) The loads acting on the ends of each member and the displacements of those ends must satisfy equations derived from the stress-strain relationship of the material of the member.

- (2) The displacements of the ends of each member must be com-

patible with the displacements of the joints to which the member is attached. These are termed the conditions of compatibility.

- (3) The loads acting on the ends of each member must be such


- as will keep the member in equilibrium. Furthermore, the sum of the loads acting on the ends of the members meeting at any joint must equal the external load applied at the joint. These are termed the conditions of equilibrium.


If the conditions of member and joint equilibrium specified in (3) provide sufficient equations to determine all the internal forces and moments in a structure the structure is said to be statically determinate. If not, it is said to be statically indeterminate or hyperstatic. Most of this book is concerned with the analysis of hyperstatic structures.

The analysis of a determinate structure is relatively straightforward, since conditions (3) are sufficient to give all the internal forces and moments. Conditions (1) and (2) may be applied afterwards if the displacements of the structure are required. In analysing a hyperstatic structure, on the other hand, it is necessary to use all three conditions in order to obtain either stresses or displacements. Broadly speaking, one may classify methods of structural analysis according to the order in which the conditions of equilibrium and compatibility are applied. Methods in which the compatibility conditions are used first give rise to equations of joint equilibrium, and are called equilibrium or displacement methods. Methods in which the equilibrium conditions are satisfied first lead to equations of displacement compatibility and are called compatibility ox force methods.

The essence of the equilibrium approach, as far as skeletal

###### B

![image 20](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile20.png)

structures are concerned, is that the displacements of the joints are considered to be the basic unknowns. In any application of the method the first step is the expression of the member endloads in terms of the corresponding end-displacements. These expressions for the member end-loads are, in general, integrals of the appropriate differential equations of extension, flexure or torsion associated with the member. They may be found either by direct integration of those equations or by differentiating the appropriate strain energy expressions with respect to the end-displacements. If the structure is linear then the member end-loads will be linear functions of the end-displacements, the coefficients of the end-displacements being functions of the dimensions and material properties of the members.

The next step uses the conditions of compatibility to express the member end-displacements in terms of the joint displacements. Thus we obtain expressions for the loads acting on the ends of the members in terms of the unknown joint displacements, which satisfy the stress-strain equations (1) and the compatibility conditions (2). These expressions for the member end-loads are now substituted into the equations of joint equilibrium. The result is a set of equations—the load-displacement equations of the structure, which relates the known joint loads to the unknown joint displacements. There will be one equation for each component of joint displacement, the constant term being the corresponding component of the applied loading. An alternative approach is to write the strain energy of the structure in terms of the joint displacements and then to differentiate with respect to each component of displacement in turn, equating the result to the corresponding external force or moment. However, this is merely an alternative way of deriving exactly the same set of equations.

The equations may now be solved for the unknown joint displacements. When this has been done, the expressions already used in setting up the equilibrium equations may be employed to find the member end-loads.

![image 21](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile21.png)

###### INTRODUCTION 13

It is apparent that in an application of the equilibrium approach it is always the displacements which are computed first. The number of equations which have to be solved is equal to the total number of independent displacement variables—the number of degrees of freedom of the structure, as it is often called, and is not

affected by whether the structure is statically determinate or not.

In the compatibility approach, on the other hand, use is made of the fact that it is relatively easy to analyse a determinate structure. Even when a structure is hyperstatic the equations of joint and member equilibrium must still hold, and these equations may be used to express the complete set of member end-loads in terms of a smaller number of unknown forces and moments. Subject to certain restrictions these unknowns may be chosen arbitrarily. They are often termed the redundant forces and moments.

While the equilibrium approach uses the stress-strain relations for the members to express end-loads in terms of end-displacements, the compatibility approach uses these relationships in the inverted form, deformations being expressed in terms of member end-loads. These end-loads are then expressed in terms of the redundant forces and moments and the known external loads by means of the conditions of equilibrium. Thus we obtain all the member deformations as functions of the external loads and the unknown redundants.

The next step involves the application of the compatibility conditions to these deformations. The result is a set of equations which in effect states that the structure is continuous at the points

- at which the redundant forces and moments act. As in the equilibrium approach, strain energy (or, more strictly, complementary energy) provides an alternative means of deriving exactly the same set of equations. Solution of these equations gives the values of the redundant forces and moments, and hence all the member end-loads. The expressions for the member deformations in terms of the applied loads and the redundants may then be used to find the displacements of the joints.


![image 22](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile22.png)

In comparing the equilibrium and compatibility approaches the most obvious test is to consider the number of equations which have to be solved. In an equilibrium analysis of a structure the number of equations is equal to the number of degrees of freedom, while in a compatibility analysis it is equal to the number of redundants. However, a comparison on these grounds may well be misleading, since the ease with which large systems of equations can be solved on a modern computer makes the actual solution process a relatively trivial part of the complete analysis. It is more sensible to base a comparison on the amount of work which has to be done in setting up the equations, and the ease with which this work can be systematized. In this connection it is worth noting that in a skeletal structure the basic unknowns of the equilibrium approach—the joint displacements, are obvious physical quantities associated with the structure. The basic unknowns of the compatibility approach, on the other hand, are a certain number of forces and moments which must be chosen according to certain rules. Any general computer program based on the compatibility approach to structural analysis must include a systematic process for determining the number and location of these forces and moments.

A skeletal structure is normally described on paper by a set of points (representing the joints) joined by lines (representing the members). Such a diagram is very similar to the way in which one describes an electrical network, and it is not surprising that there are many points of similarity between the methods used in analysing the two types of system. In network theory what we have termed "equilibrium" and "compatibility" methods appear as "node" and "mesh" methods respectively, loads being replaced by currents and displacements by voltages. The analogue is not complete, however, since the behaviour of an electrical network depends only on the way in which the elements are connected together, and not on their orientation in space.

![image 23](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile23.png)

###### CHAPTER 2

###### Vectors and Matrices

IN this chapter we give a brief account of those aspects of matrix algebra used in later chapters. Sections 2.1-2.4 and section 2.6 contain those basic ideas and techniques which are of general importance in the matrix analysis of structures, and which are used throughout the rest of the book. Section 2.5 contains material relevant to the discussion of vibration problems in sections 4.9 and 8.6, while the account of linear programming in section 2.7 is introduced in preparation for the discussion of rigid-plastic collapse analysis in section 7.7. Further information on the algebraic properties of matrices and the computational problems associated with matrix operations will be found in the references listed at the end of the book.

###### 2.1. Vectors

An ordinary three-dimensional vector is often defined as a quantity "possessing both magnitude and direction". Although such a quantity may be thought of as having an existence which is independent of any coordinate system, its direction can only be specified by relating it to some arbitrarily chosen set of axes. Thus a vector might be defined in a particular coordinate system by its components x, y and z. Such a representation would not be unique, since it would depend on the choice of coordinate system—referred to another set of axes the same vector would have a different set of components x\ y\ ~'. When a vector is specified in this way the order in which the components are given

15

![image 24](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile24.png)

###### 16 MATRIX METHODS OF STRUCTURAL ANALYSIS

is important: for example, the vectors whose components are [1, 2, 3] and [3, 1, 2] are different vectors.

Conversely, any set of three numbers or variables arranged in a particular order may be regarded as defining a vector in the threedimensional space formed by an appropriate set of coordinate axes. More generally, a set of n scalar quantities may be regarded as defining a vector in an «-dimensional space. This does not mean that the reader must attempt to visualize an «-dimensional space. It is merely that many of the results which can be proved by geometrical argument in the case of three-dimensional vectors can be extended formally to n dimensions, and can be discussed in the same sort of geometrical language.

In this book we shall call a set of scalar quantities xu x2, ..., xn a vector, and write it for the sake of conciseness as xt (where i is assumed to take all values from 1 to «), or JC. The individual scalar x's will be referred to as the components of the vector. Where a physical quantity such as a load or a displacement is written as a vector the values of the components will depend on the coordinate system in which these components are measured, so that essentially the same physical quantity will be represented by different vectors when viewed from different coordinate systems. As we shall see, matrix notation makes it very easy to change from one coordinate system to another.

We shall normally write vectors as columns of numbers or symbols, enclosed in square brackets. The rules for the manipulation of general «-dimensional vectors are very similar to those used in dealing with ordinary three-dimensional ones. Thus two vectors are equal only if all their components are equal, while the sum of two vectors is formed by adding corresponding components. Extending the normal three-dimensional idea of length we say that the length of a vector x is equal to

## M*)

Multiplication of a vector by a scalar merely increases each

![image 25](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile25.png)

###### VECTORS AND MATRICES 17

component in the same proportion, or, in geometrical terms, changes the "length" of the vector without altering its "direction". Thus we write

= /CA^I

Γ*1~

x2

KX2

###### L*„_

###### -fe*iJ

If two vectors ai9a2,-..9an and bi9b2, ..*,bn have the same number of components their scalar product is defined to be the scalar quantity c = αφγ + a2b2 + ... anbn9 which may be written more concisely as

n

###### c = Σ * A

It is common practice to drop the summation symbol in such expressions and write simply c = apiy the repetition of the suffix 1 being regarded as implying summation over all its possible values. We shall make occasional use of this convention: it should be noted that summation is only implied when the repetition of the suffix occurs within a product—the equation a{ = xh for example, does not imply any summation. In ordinary three-dimensional vector algebra it can easily be shown that two vectors whose scalar product is zero must be at right-angles to each other. In the general case two vectors whose scalar product is zero are said to be orthogonal.

The equation

a^x^ + a2x2 + a3x3 = 0 (2.1) represents a plane through the origin (i.e. a two-dimensional space) lying in the three-dimensional space defined by the axes *i, x2, X3, and all vectors whose components xl9 x2y x3 have to satisfy (2.1) must lie in this plane. Although such vectors have three components only two can be specified arbitrarily, since the third is then determined by (2.1). In such a case the three components are said to be linearly dependent. This idea may be

![image 26](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile26.png)

###### 18 MATRIX METHODS OF STRUCTURAL ANALYSIS

extended to «-dimensional vectors. If the components of an «-dimensional vector x have to satisfy an equation of the form

alxl -h a2x2 + ··· 0/Λι = 0 (2.2) then the components are said to be linearly dependent, since only n — 1 of them can be specified arbitrarily. Equation (2.2) restricts the vector x to a space of « — 1 dimensions, sometimes called a hyperplane, lying in the «-dimensional space formed by the axes xu x2, ..., xn.

###### 2.2. Matrices

In the analysis of linear systems there are many occasions when one vector is expressed as a linear function of another. That is to say, a set of variables xl9 ..., xn is related to another set of variables >'i» ···> y m by a system of linear equations

.v2 = a2ly{ + a22y2 4- ...a2mym\

###### (2.3)

x« = <*myi + an2y2 + ...flnm^m/

where the coefficients αη, Λ124 etc. are constant. It should be noted that in these equations the first suffix of each coefficient defines the row in which it stands, while the second defines the column. Equations (2.3) may be written in condensed form as

m

*i= Σ auyj 0' = ^ · ·> ")

or, using the summation convention mentioned in section 2.1, simply as

Xi = WJ 12.4) We now give (2.4) a rather different interpretation. We

regard the symbols ΛΓ, and ;>. as denoting the complete vectors JC

![image 27](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile27.png)

VECTORS AND MATRICES 19

and y rather than particular individual components, and the symbol au as denoting the whole set of n x m coefficients appearing in (2.3). We call this set a matrix and write it in square brackets. Thus (2.3) becomes

- (2.5)
- (2.6)


011 ^12

>'l

a2l a22

y2

<*2m

* 2

or, more briefly,

x = Ay

Equation (2.6) may be interpreted as stating that the vector JC is equal to the vector y "multiplied" by the matrix A. Since these symbols do not now represent simple algebraic quantities, it is necessary to define the meaning of the word "multiplication" in this context. We do this by saying that equations (2.3)-(2.6) are all identical in meaning. In other words we multiply a vector by a matrix by taking the scalar product of each row of the matrix with the vector. It is obvious that for such a multiplication to be possible the number of columns in the matrix must be equal to the number of components in the vector: the result of the multiplication is a vector with as many components as there are rows in the matrix. For example, the linear relation

*i = 3>Ί - 2y2 + 4y3 x2 = 2yt 4- 3y2 - y3

appears in matrix form as

3 - 2 4 2 3 - 1

*i

L*2

LB

![image 28](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile28.png)

20 MATRIX METHODS OF STRUCTURAL ANALYSIS

In this book vectors will be denoted by lower case letters and matrices by capitals. A matrix with an equal number of rows and columns is termed a square matrix, and the coefficients an, a22, ...,ann are referred to collectively as the leading diagonal. A square matrix in which the only non-zero terms are on the leading diagonal is called a diagonal matrix, and if all these coefficients are equal to unity it is then called a unit matrix, normally denoted by the symbol J. A unit matrix clearly satisfies the equation x = Ix for an arbitrary vector JC. A matrix entirely composed of zero coefficients is termed a null matrix, and is written as 0.

The next step is to consider what is meant by the "multiplication" of two matrices. Consider the two sets of equations

yx = bilZi + bl2Z2

(2.7)

xl = ailyl + al2y2 + ai3y3

- y2 = b21zx + b22z2
- y3 = b3lzl 4- b32z2


*2 = «2iJ>i + a22y2 + a23y3

In matrix notation these become ϊαίί αί2 αί3

###### 5 >r

###### ipr

###### = 1*11

b12 bn

b2l L*3i

yi

v 2 j L«21 #22 «23J

^2

1 J's.

.y*.

*32.

and eliminating the vector y we obtain the formal result

(2.8)

bit bi2 b2i b22

«n

Zl

«13

'12

«21

«23j

L*2

'22

L*2

*3i b32J

Alternatively we may eliminate yu y2, y3 from equations (2.7) by the ordinary rules of algebra to give

- *i - («n*7i + «12*21 + al3b3x)zx


+ («11*12 + «12*22 + «13*32^2

![image 29](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile29.png)

###### VECTORS AND MATRICES 21

- *2 = («21*11 + «22*21 + «23*3l)*l


+ («21*12 + «22*22 + «23*32^2

which may be written in matrix form as

###### ^2J

«11*11 + «12*21 + «13*31 «11*12 + «12*22 + «13*32 «21*11 + «22*21 + «23*31 «21*12 + «22*22 + «23*32

ώ2ϋ

(2.9)

Comparing (2.8) and (2.9) gives immediately

###### «11 «12 «13]Γ*11 *12 '22 *21 *2

.*31 *32

= [«11*11 + «12*21 + «13*31 «11*12 + «12*22 + «13*321 L«21*ll + «22*21 + «23*31 «21*12 + «22*22 + «23*32

Thus the product of two matrices A and B is formed by taking the scalar product of each row of A with each column of B, More explicitly, if C = AB then the element in the /'th row and the/th column of C is obtained by taking the scalar product of the /'th row of A and the / t h column of B. It follows that for such a multiplication to be possible the number of columns in A must equal the number of rows in B. It is always the rows of the first matrix which multiply the columns of the second, so that the product BA is not necessarily equal to AB, and indeed may not exist at all. When referring to a matrix product such as AB we may specify the order of multiplication by saying that A "premultiplies" B, or that B "post-multiplies" A.

Every matrix A has associated with it another matrix called the transpose, written as A\ which is formed by interchanging corresponding rows and columns. A matrix for which A* — A is

![image 30](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile30.png)

###### 22 MATRIX METHODS OF STRUCTURAL ANALYSIS

called a symmetric matrix. Such a matrix is necessarily square, and the elements satisfy the condition atj = ayv The reader may easily verify that the product of two symmetric matrices is not necessarily symmetric.

A vector may be regarded as a matrix containing only one row or column. The scalar product of two vectors at and b{ may therefore be written in the form

(2.10)

Ol <*2 - a„]

b2

lA_l

where the vector a is written as a row rather than a column in order to agree with the general rule for matrix multiplication. It is important to realize that such a "row vector" is not essentially different from the same symbols written as a column. It is simply a matter of arranging the components on paper in such a way that they conform to the rule for multiplication. Since a row vector is the transpose of the corresponding column vector (2.10) may be written as axb = <?, and it is obvious that alb — Va. More generally it is easy to show that for matrices A*B = ffiA)*.

Other properties of matrices can be derived by considering operations carried out on linear systems of equations. For example, if

- *i = 4yx + 2y2 ζγ = 2yY + 6y2 (2.11)
- *2 = 3j>i + 5y2


*2 = 4>Ί - y2

then it follows that

(2.12)

x, + z, =(4 + 2)^ + (2 + 6)>^2 x2 + z2 = (3 + A)yx + (5 - l).y2

![image 31](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile31.png)

###### VECTORS AND MATRICES 23

In matrix notation (2.11) might be written as x = Ay, z = By, and (2.12) as x + z = (A + B)y = C>, where C, the swm of A and ß, is formed by adding corresponding elements of the two matrices. It follows that one cannot add two matrices unless they have the same number of rows and the same number of columns. In the same way it is possible to show that the normal associative laws of algebra

A(B + C) = AB + AC, (AB)C = A(BC)

hold for matrices, provided that the order of the multiplications is maintained.

In structural analysis it is often convenient to use matrices in which the elements are themselves smaller matrices. Thus one might write the equations Ax + By = a, Cx + Dy = b in the form

\A Bl

— a]

- [x
- [y.


###### [c D\

###### _b[

A matrix which is divided into blocks of coefficients in this way is said to be partitioned, and the elements A, B, etc. are called submatrices.

An important quantity associated with a symmetric matrix is its quadratic form. The quadratic form associated with the matrix A is simply the scalar function x*Ax, where JC is an arbitrary vector. Written out in suffix notation this takes the form aijXiXj, summation being implied over both i and j . A matrix whose quadratic form is always strictly positive for an arbitrary non-zero vector x is called positive definite. The quadratic form associated with a symmetric matrix often has a direct physical significance. For example, if the displacements d of a structure are related to the external loads p by the linear equation p = Kd, then the work done on the structure during the application of the loads is dxp\2 = dfKd/2. Thus the quadratic form associated with the matrix K is proportional to the strain energy of the structure. If K is positive definite then the strain energy is always

![image 32](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile32.png)

positive and the structure is therefore stable. Just as the method of moment distribution only converges for stable structures, so many of the iterative methods for solving systems of linear equations only converge if the matrix of the coefficients is positive definite.

2.3. Matrix Inversion The equation

Ax (2.13) may be regarded as having the efFect of transforming an arbitrary

- vector x into another vector y, and is often described as a linear transformation. As an illustration of a two-dimensional linear transformation we may imagine the vector x to be a line drawn on a rubber sheet, and think of the multiplication of x by A as a stretching of the sheet in some uniform manner. The following are examples of simple two-dimensional transformations :

- (1) A = Γΐ 0] A is a unit matrix: this transformation [0 1J leaves every vector unchanged.
- (2) A = fa 01 A is a diagonal matrix: this transformation [0 b\ multiplies the xt component of any vector

by a factor a, and the x2 component by a factor b.

[

cos a —sin a] sin a cos aj

- (3) A = [cos a — sin a] This produces a rotation of any vector through an angle a, as shown in Fig. 2.1.


In these three examples any particular vector x gives a unique

- vector y, and conversely one may choose an arbitrary y and determine a corresponding unique vector JC. This implies that an inverse transformation exists* of the form


x = By (2.14) where B is some function of A. The matrix B is called the inverse

![image 33](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile33.png)

###### VECTORS AND MATRICES 25

of A and is written A ~\ Methods of computing the inverse of a matrix will be found in any standard textbook on matrix algebraan elementary method is described in section 2.6.

If we eliminate j; from equations (2.13) and (2.14) we obtain JC = A'1 Ax. Since the only matrix which leaves all vectors x unchanged is the unit matrix /, it follows that A'1 A = /, just as a~1a = 1 for ordinary scalars. This result is useful in checking the

computed value of an inverse matrix.

Fio. 2.1. Rotation of a two-dimensional vector through an angle a.

For a matrix to possess an inverse it must necessarily be square, but this alone is not sufficient. Consider, for example, the transformation

)>1 (2.15)

= cot a

1 1 tan aj

###### Γ*Γ

1

###### L"^2

yi.

where a is constant. It is apparent that, irrespective of the values of xx and x2, the components of the vector y are not independent, but must satisfy the equation

###### y2 = yt tan a (2.16)

Thus (2.15) transforms any vector x into a vector lying in a certain direction, as shown in Fig. 2.2. In fact all vectors x for which the

![image 34](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile34.png)

function jq + x2 tan a is constant transform into the same vector y. In such a case it is clearly impossible, given a particular vector y9 to find a unique corresponding vector JC, so that the inverse transformation (2.14) does not exist. A transformation or a matrix which has no inverse is said to be singular.

FIG. 2.2. A singular transformation: all the vectors ΟΑι, ΟΑι> ..., transform into the same vector OB.

In the general case we may regard a singular transformation as one in which the resulting vector y has a smaller number of independent components than the original vector JC. In geometrical language this is equivalent to saying that the vector y lies in a space with a smaller number of dimensions than that of the space required for the general vector JC. This may be because the matrix A is a rectangular matrix with fewer rows than columns, so that the vector y necessarily has fewer components than jr. It may, on the other hand, be due to the fact that, although x and y have the same number of components, the square matrix A is such that the components of y have to satisfy one or more

![image 35](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile35.png)

###### VECTORS AND MATRICES 27

conditions such as (2.16). As we saw in section 2.1, if the components of y satisfy (independently of the choice of x) one or more conditions of the form

Wi + Wi + ··· cnyn = 0 (2.17) then it is impossible to give arbitrary values to all the components, so that the vector y does not, in fact, occupy a space of the same number of dimensions as JC. In these circumstances the inverse transformation (2.14) does not exist.

What property of a matrix determines whether it is singular or not ? We may answer this question by writing (2.13) in the form

where a\9 ..., aj, are the successive rows of the matrix A. Substituting these expressions in (2.17) gives {ο^α\ + ο2α\ -l· ... £ηαί,)χ = 0, and since JC may be any vector it follows that

(2.18)

Thus a square matrix is singular if its rows satisfy one or more equations such as (2.18), i.e. if one or more of the rows are merely linear combinations of the others. If no such relationship exists the rows of the matrix are said to be linearly independent and the matrix is then non-singular. The reader familiar with the theory of determinants will recognize that a matrix is singular if and only if its determinant is zero.

It is instructive to arrive at the same result by a slightly different line of reasoning. Consider the set of three simultaneous equations

![image 36](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile36.png)

###### 28 MATRIX METHODS OF STRUCTURAL ANALYSIS

which in matrix form is equivalent to

Ax = b (2.19) Equation (2.19) may be written

a\x = 6Λ ' a2x = b2 (2.20)

###### a\x = bj

where a\, a29 a3 are the rows of the matrix A. We may make each of these vectors of unit length by dividing the original equations by the appropriate factors. If this is done, then (2.20) states that bu Z>2, b3 are the components of the vector x in the directions of the unit vectors au a2, a3. This information will be sufficient to determine JC, provided that these three unit vectors constitute a set of axes in which it is possible to define a general three-dimensional vector. This will be so provided that the vectors αί9 a2, a3 are not coplanar, which is equivalent to saying that they do not satisfy an equation of the form

c1a1 + c2a2 + c3a3 = 0 This is essentially the same condition as before.

This analysis allows us to introduce the idea of ill-conditioned systems of equations. If the vectors αί9 α2, a3 are not coplanar, then theoretically the inverse matrix A ~1 exists, and it is possible to solve (2.19) for the vector x. However, if the vector ax, say, lies very nearly in the plane defined by a2 and a3 then the three unit vectors obviously form a "bad" set of axes for describing a three-dimensional space, and considerable numerical difficulty may be experienced in obtaining an accurate solution of the equations. In such a case the matrix A is said to be ill-conditioned.

In contrast, the "best" sets of axes for describing a threedimensional space are rectangular cartesian ones, in which the base vectors ai9 a2, a3 are mutually perpendicular. This condition may be written in the form a\aj = 0, (/ Φ j). In general a

![image 37](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile37.png)

###### VECTORS AND MATRICES. 29

matrix in which the rows form a system of mutually orthogonal unit vectors is termed an orthogonal matrix. Since for an orthogonal matrix

α1α, = 0 {ίΦ))

a\aj = l (i=j)

it follows that AXA = /, so that the inverse of an orthogonal matrix is equal to its transpose.

In structural applications of matrix algebra it is occasionally necessary to find the inverse of a matrix product such as ABC. It is easy to show that if all the matrices A, B, and C are nonsingular then {ABC)"1 = C~1B~1A~1. This result may be proved by pre-multiplying both sides of the equation by ABC, giving (ABC)(ABCyl = ABCC^B^AK Both sides of the latter equation are clearly equal to the unit matrix.

The solution of a set of simultaneous equations or the inversion of a matrix forms the central computational problem in what may be called "linear equilibrium problems". In structural analysis the equations to be solved may be those of equilibrium or compatibility, while in electric network theory they arise through the application of Kirchhoff's laws. Some simple methods of carrying out these processes numerically are discussed in section 2.6.

###### 2.4. Coordinate Transformations

As mentioned in section 2.1, our definition of a vector as a set of components implies the existence of a coordinate system in which these components are measured. If in the equation

y = Ax (2.21)

the symbols x and y stand for physical quantities such as loads and displacements, then this equation represents a linear relationship between these quantities as seen from the standpoint of one particular frame of reference. If we had chosen a different reference frame the same relationship would have appeared in a

![image 38](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile38.png)

###### 30 MATRIX METHODS OF STRUCTURAL ANALYSIS

different form as y' = A'x . In other words the matrix A is not an invariant mathematical description of the relationship between the physical quantities, but depends on the coordinate system used to define their components. We now consider the form taken by a relationship such as (2.21) when the coordinate axes are changed.

For the sake of simplicity we shall imagine that we are dealing with ordinary three-dimensional vectors x and y, whose components are initially defined in a given set of rectangular cartesian coordinates. Let ul9 u2i u3 be three mutually perpendicular unit vectors whose components (often termed direction cosines) are defined relative to this set of axes. Then these three unit vectors may be thought of as defining a new system of coordinates, and in this new system the vector x has components u\x, u2x, u\x. If we write

x[ = u\x\ x2 = u2x \ (2.22)

then the vector xf represents the vector JC as it appears in the new coordinate system. Equations (2.22) may be written

x = U'x (2.23)

where Vx is the orthogonal matrix whose rows are u\, u2, u*3. Since U* is orthogonal, its inverse is equal to its transpose, so that

x = Vx' (2.24)

Equation (2.23) may also be used to find the vector y' corresponding to the vector y, i.e. y' = £/fy. Combining this equation with (2.21) and (2.24) we obtain

y' = Uty=UtAx = (UtAU)x'

Thus the relationship which was defined by the matrix A in the old coordinate system is defined by the matrix A' = U%A\J in the

![image 39](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile39.png)

###### VECTORS AND MATRICES 31

new one. The matrices A and A' are said to be congruent. It is easy to show that if A is symmetric then so is A'.

This treatment may be extended to «-dimensional vectors. More general transformations also exist, in which the matrix U is not necessarily an orthogonal matrix and may even be singular. Examples of such transformations will appear in following chapters.

###### 2.5. The Principal Axes Problemf

Transformations of the type described in the previous section may be carried out on any square matrix, whether symmetric or not. However, many of the matrices which occur in the study of linear structures are symmetric, and as such possess a number of special properties.

If we have a linear relationship defined in a certain coordinate system by the equation y = Ax, where A is symmetric, then from the analysis given in the previous section we know that the same relationship will appear in another coordinate system as y' = A'x\ where A' is derived from A by the congruent transformation Α' = U'AU. An important property of symmetric matrices is that by a suitable change of coordinate system any linear relationship defined by a symmetric matrix A can be transformed into a relationship in which A' is purely diagonal, i.e.

0

0

y'i

0 0 L·

yn.

all the A's being real. (This transformation is also possible if A is

t This section is only relevant to sections 4.9 and 8.6 and may be omitted at a first reading.

![image 40](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile40.png)

###### 32 MATRIX METHODS OF STRUCTURAL ANALYSIS

not symmetric, but the A's may be complex.) This equation may be written

y2 = λ1χ,1

In other words, any linear relation between vectors for which the matrix is symmetric is essentially one in which (in the appropriate coordinate system) individual components are simply multiplied by the appropriate λ% so that y\ depends only on x[, y'2 only on x2, etc. The unit vectors uu u2, .., un which form the axes of the new system of coordinates are called the principal axes, characteristic vectors, eigenvectors, or latent vectors of the matrix A. The

- A's which form the diagonal elements of A' are called the eigenvalues or latent roots of A.


We can construct a general method for finding the eigenvalues and eigenvectors of a matrix as follows. Consider the application of the linear transformation (2.21) to the vector x = w, where u is one of the eigenvectors wf. By definition the effect of the transformation on such a vector is merely to multiply it by some unknown scalar factor λ, so that Au = Xu, which may be written as

{A - Xl)u = 0 (2.25)

If a particular vector u satisfies (2.25) then clearly any scalar multiple of u also satisfies the equation. Since the solution is not unique it follows that the matrix (A — λΐ) must be singular, and hence that the determinant of this matrix must be zero. Expansion of this determinant gives a polynomial of degree n in X, and it can be shown that if A is symmetric then all the n roots of this polynomial are real. These n roots are the n eigenvalues λΐ9 A2, ..·, λη. If we consider only the simple case where the n roots are distinct, we may find the eigenvector associated with any

![image 41](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile41.png)

particular eigenvalue Xt by substituting this value into (2.25). This gives a set of n simultaneous equations of the form

B,u = 0 (2.26)

whereof — A — XtL No w although B fis singular it can be shown that if Af is a simple root then n — 1 of the simultaneous equations

(2.26) are linearly independent. It is possible, therefore, to specify one component of the solution arbitrarily and then solve the equations for the remainder. This arbitrary specification of one component is equivalent to assigning the length of the vector, which we have chosen to be unity. Thus we can obtain the vector if; associated with each value of λν

It is easy to show that the eigenvectors must be mutually

orthogonal. Let nr, us be two different eigenvectors and λη Xs be the corresponding eigenvalues. Then we have

- Aur = Xrur (2.27)
- Aus = Xsus (2.28)


Multiplying (2.27) by u[ and (2.28) by u*r gives

u\Aur = Xru[ur (2.29) ulAus = X5ulus (2.30)

and since A is symmetric the left-hand sides of (2.29) and (2.30) are identical. It follows that Xruxsur — J.5u'ifs, and since by hypothesis ΛΓ Φ Xs we must have u\ur = 0.

While the eigenvalues of a symmetric matrix are always real, it can be shown that the eigenvalues of a positive definite symmetric matrix are in addition always positive. If we take a general vector JC and express it in the coordinate system defined by the eigenvectors we have x = Ux' from (2.24). It follows that the quadratic form x*Ax becomes x^WAUx' when transformed into this coordinate system. Since the matrix \]ΧΑ\] is equal to the

![image 42](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile42.png)

###### 34 MATRIX METHODS OF STRUCTURAL ANALYSIS

diagonal matrix A' whose leading diagonal coefficients are the eigenvalues λ,, the quadratic form reduces to

n

###### Σ λιχΐ2

Hence the change of coordinates which reduces A to a purely diagonal matrix reduces the associated quadratic form to a sum of squares. If this quadratic form is always positive for any arbitrary non-zero vector x it follows that all the A's must be positive.

There are a number of other methods for obtaining the complete set of eigenvalues and eigenvectors of a given matrix which are more efficient from a computational point of view than the simple process outlined above. These are described in standard textbooks on numerical analysis and will not be dealt with here. However, there are also a number of processes for finding single eigenvalues. Two of these are of sufficient importance in engineering problems to justify a brief account here.

The first method is essentially one for finding the eigenvalue of largest modulus, this being also the algebraically largest eigenvalue in the case of a positive definite matrix. It will be recalled that for any matrix A the effect of multiplying an eigenvector u by A is to multiply its "length" by the corresponding λ without changing its "direction". Now any arbitrary vector JC(0) may be expressed in the coordinate system defined by the eigenvectors as

JC(0) = x\ux + x'2u2 + ... + x'„un

x[, x'2, ..., x'n being the components of x in the directions of the various eigenvectors. If now we multiply x(0) by A we obtain

X(1) = Λχ(0) = X1X\U1 + λ2χ'2η2 + ... K*'n*n

each component being magnified by the appropriate eigenvalue. Suppose now that λ1 < λ2 < ... < λη. Then the component of JC(0) in the direction of un has been multiplied by a larger factor than any of the other components—in other words the direction of x(l) is closer to the direction of u„ than was the direction of

![image 43](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile43.png)

###### x(0). If we repeat the process we obtainχ(2) β ^2χ<0> = X2x,iUi + _λ2^ηΜη

and with each successive multiplication the magnitude of the component of the vector x in the direction of un increases relative to the magnitudes of the other components.! Eventually we reach a stage where jc(r) is in approximately the same direction as un9 the components associated with the other eigenvectors being negligible in comparison. Thus we have jc(r+1) = Ax{r) « k„xir\ λη being obtained as the ratio of jc(r+1) to x(r).

The speed of convergence of this process clearly depends on the ratio of λη to the other A's. It also depends on the choice of initial x(°)—it is a considerable advantage if a vector is chosen which is already more or less "in the right direction". In vibration problems the process corresponds to assuming a mode of vibration which is then corrected, and it is usually possible to make an initial guess at this mode using physical intuition or model tests.

In the form in which we have described it the process will always converge to the largest eigenvalue, while in vibration problems it is usually the smallest which is required. (The smallest eigenvalue corresponds to the lowest natural frequency of vibration, the eigenvector associated with this eigenvalue usually being called the "fundamental mode".) However, this difficulty is easily overcome. If a matrix A has eigenvalues kt and eigenvectors if; then these satisfy the equation {A — Xl)u = 0. If we multiply this equationby —(1/λ)Α~l we obtain (A~l — {\jX)l)u = 0. It follows that the eigenvalues of A'1 are the reciprocals of those of A, while the eigenvectors are the same. Thus the smallest eigenvalue of A can be found by taking the reciprocal of the largest eigenvalue of A"1. (We are of course assuming here that A is non-singular, so that λ = 0 is not an eigenvalue.)

t We are not here concerned with the absolute lengths of the vectors x<°>,

###### x(1)t ..., x(r), ..., but merely with the relative proportions of their components.In a numerical application of the method it may be desirable to make theselengths approximately equal by applying a suitable scalar multiplier aftereach matrix multiplication.

![image 44](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile44.png)

###### 36 MATRIX METHODS OF STRUCTURAL ANALYSIS

The second method we shall describe is known as "Rayleigh's principle". This may be used to obtain an approximate value for an eigenvalue from an approximation for the corresponding eigenvector. As mentioned earlier, in the case of a vibration problem it is usually possible to make a reasonable guess at the form of a mode of oscillation, particularly when the mode in question is the fundamental, and in fact Rayleigh's principle is often used for estimating the lowest natural frequency of a system.

The method is extremely simple. If ur is an eigenvector of A, then by definition Aur — Xrur. Pre-multiplying both sides of this equation by u\ we obtain u\Aur = Xru\u„ or Xr = uxrAur\u\ur. If the vector ur is only an approximation to the eigenvector then this equation will not be exact, but it can be shown that the error in the computed value of Xr will be of second order compared with the error in i#r. Thus a relatively crude approximation to the eigenvector will often yield a satisfactory approximation to the corresponding eigenvalue. It can also be shown that if ur is not an exact eigenvector then the calculated Xr will lie between the greatest and the least of the A's. It follows that when used to estimate the lowest natural frequency of a system Rayleigh's principle always gives a value which is somewhat greater than the true frequency.

In many vibration problems the equation which has to be solved is not Au = Xu but the more general one

Au = XBu (2.31)

- where A and B are known symmetric matrices. It is possible to reduce (2.31) to the simpler form by pre-multiplying both sides by


- B'1, but this has the drawback that in general B~XA will not be symmetric. The symmetry may be retained by splitting B into two triangular matrices. It can be shown that if B is a positive definite matrix then it is possible to express B in the form 11L, where L is a lower triangular matrix (i.e. a matrix which has all its elements above the leading diagonal equal to zero). Thus we may


![image 45](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile45.png)

###### VECTORS AND MATRICES 37

write (2.31) as Au = XllLu, and if we put v = Lu this may be written as AL~lv = Xllv, or as

(L)~lAL-lv = λν (2.32)

The matrix (Ü)~{AL~l is symmetric if A is symmetric, but it should be noted that its eigenvectors vt are not the same as those of A. The H'S must be obtained from the »'s by applying the relationship iif = L~lvi.

When using Rayleigh's principle the more general form (2.31) gives no trouble. One merely pre-multiplies both sides of (2.31) by u\ in the same way as before, obtaining Xr = u^Au^u^Bu^

2.6. The Solution of Simultaneous Equations and the Inversion of Matrices

Throughout this book we shall assume that the structural analyst who wants to use matrix methods has an automatic computer available, and that this computer is already provided with routines for carrying out the standard operations of adding, multiplying, and inverting matrices when these matrices are expressed in numerical form. We regard the development of these routines as the province of the professional numerical analyst, not the structural engineer. However, there are occasions when it is desirable to solve a simple set of equations or find the inverse of a matrix in algebraic rather than numerical form. We therefore describe here a few of the methods which are available for solving systems of linear equations and inverting matrices.

Methods of solving sets of simultaneous equations may be divided into those which obtain an exact solution (except for numerical rounding-off errors), and those which produce a sequence of approximations to the true solution, starting from arbitrary initial values of the variables.

One of the earliest approximate methods to be developed is the systematic process known as the Gauss-Seidel method, in which the equations are scanned repeatedly in a fixed order. Each

![image 46](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile46.png)

###### 38 MATRIX METHODS OF STRUCTURAL ANALYSIS

equation is used to obtain a new value of the variable associated with it in terms of the current values of the other variables, the cycle being repeated until a sufficiently accurate answer has been obtained. The process converges provided that the matrix of the coefficients appearing in the equations is positive definite, but in many structural applications even the speed of a modern computer is not sufficient to make the rate of convergence acceptable.

More recently a whole class of approximating procedures have been developed which are known generally as "relaxation methods". These also operate by making repeated adjustments to arbitrary initial values of the variables, but the adjustments are not made in any set order, the pattern of the calculation being determined by the intuition and experience of the human computer rather than by a rigid set of rules. Although relaxation methods are a useful aid in solving certain types of linear system,

- as far as structural analysis is concerned it seems preferable to apply them in a semi-physical manner, without formally writing down the linear equations. The method of moment distribution is a well-known example of this approach.


While computer routines based on iterative methods have been used successfully for solving certain types of linear system, the standard routines for general-purpose equation solving and matrix inversion almost all use exact procedures. The reason is that the convergence of the simpler iterative methods depends on the equations satisfying some analytical condition, such as the positive-definiteness of the coefficient matrix. Even when this condition is formally satisfied the rate of convergence may be unsatisfactory if the equations are ill-conditioned. The various devices which the human computer uses to accelerate the convergence of the relaxation process are almost all non-systematic, so that although when incorporated in a computer program they may improve the degree of convergence per cycle, the overall saving in time may not be very great.

One of the most widely used of the "exact" methods of solving linear systems of equations is the method of successive elimination

![image 47](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile47.png)

###### VECTORS AND MATRICES 39

of variables. This method is capable of handling ill-conditioned systems of equations, and there is no need for the coefficient matrix to be either symmetric or positive definite. We describe the method here in its simplest form—there are many variations of it, most of them designed to facilitate the arrangement of the calculation in a compact tabular form when they are done by hand.

If we have a set of n linear equations

" 1

~ l

"'in

a2l a22

• «2n

*2

###### 6.

then the variable xx may be eliminated from the last n — 1 equations by subtracting suitable multiples of the first equation from the others. In terms of matrix coefficients this may be done by adding —ail/aii times the first row of coefficients to the coefficients of row /, where / takes the values 2, 3, ..., n, and multiplying the constant bi by the same factor and adding it to the corresponding constant br This leaves the actual solution of the equations unchanged, and results in the original equations being replaced by

###### = Γ*ι1

al2 .

Γ*11

- • «In"
- • «in
- • a'm_


~*1~

0

x2

«22 ·

b'2\

###### L °

###### M

-*»-

<2 ·

where primes indicate altered coefficients. In the same way we may subtract multiples of the second equation from the third and following rows in such a way as will make the coefficients «32» ···>an2a^ zero» a nd ^ e process may be continued until all the coefficients below the leading diagonal have been reduced to zero. During this process the row used to alter the coefficients in the other rows is called the pivotal row, and its leading diagonal element is termed the pivotal element.

![image 48](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile48.png)

###### 40 MATRIX METHODS OF STRUCTURAL ANALYSIS

Having reduced the equations to the form

###### ~V

###### = ~M

a12 a'22 -

f«ll 0

01» «2»

*2

###### ■^2

###### .Kl

###### L °

0

_*»_

α'ππ.

we may now find xn from the last equation, which gives xn = ^ή/tf,',,,. Substituting this value into the (n — l)'th equation gives xn-u and the process can be continued until we finally determine xx.

So far we have assumed that the coefficients in the equations are single numbers. Exactly the same process may be employed if they are sub-matrices. The only difference is the notational one associated with the row multipliers —ail/all, etc., which now have to be written in the form —aixa^l, etc.

The total number of operations involved in this process is theoretically of order n3/3. However, we shall see in section 9.4 that for structural applications this is usually a very pessimistic estimate, since the matrices which arise in structural calculations are generally both sparse and banded, i.e. they have a large number of zero elements, and the non-zero elements tend to lie near the leading diagonal. In these circumstances the number of operations can be made very much less than «3/3.

If the initial matrix is symmetric then it is easy to show that after the unknown *χ has been eliminated from equations 2 to n these n — 1 equations are still symmetric. Similarly when the second column of zeros has been introduced the last n — 2 equations are symmetric, and so on. Thus the process may be carried out entirely in terms of the coefficients on the leading diagonal and above it, or alternatively the symmetry may be used to provide a check on the calculation.

The systematic process described above assumes that at each stage the relevant leading diagonal element is non-zero (or, if the element is a sub-matrix, that it is non-singular). The process fails if this is not the case, while if the element is small compared

![image 49](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile49.png)

###### VECTORS AND MATRICES 41

with the other coefficients in the column then the calculation is likely to become inaccurate. This defect may be overcome by the process known as exchange of pivots. We first of all scan the first column of the matrix to find the element in the column with the numerically largest value. The equations are then rearranged in order so that this element becomes αίί: it follows that all the multipliers — flu/flu are made less than unity, so that the process of modifying the rows of the matrix does not give rise to large numbers. The same operation is repeated with the second column during the next stage of the process, the equations 2, ..., n being rearranged so that a'22 becomes the largest in the column a'12, ···> a'nl. Thus throughout the reduction process the factors by which rows are multiplied before being added to other rows are always less than unity. This refinement is commonly found in generalpurpose computer routines, since it minimizes the eifects of rounding errors. However, most of the systems of equations which have to be solved in structural analysis involve matrices which are symmetric and have non-zero leading diagonal elements —these elements are often direct stiffness or flexibility coefficients, which must be non-zero on physical grounds. Thus the purely sequential process is usually satisfactory for structural problems.

The elimination method also provides a convenient way of checking on the stability or otherwise of a structural system. As we saw in section 2.2, the stability of a structure depends on the coefficients appearing in the load-displacement equations forming a positive definite matrix. It may be shown that if all the leading diagonal elements aiX, a22, ··,#«„ of the triangular matrix formed by the elimination process are strictly positive then the original matrix is positive definite. The product of these leading diagonal elements is in fact equal to the value of the determinant of the original matrix, and the elimination method is probably the easiest way of computing this quantity if it is required.

The inversion of a matrix may be regarded as the solution of a set of linear equations with a succession of right-nand sides, and it may be carried out by the following process, which is very similar

![image 50](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile50.png)

###### 42 MATRIX METHODS OF STRUCTURAL ANALYSIS

to the elimination method described above. If we have a linear relation Ax = y we write it as Ax = ly. We now proceed to eliminate all the off-diagonal elements of A by combining suitable multiples of equations. In this manipulation we combine the rows of the unit matrix / in exactly the same way as the rows of A, so that eventually we transform the equations into the form Ix = By,

- where B is equal to A~l. Since the process only involves the elements of the matrices the vectors JC and y are not really necessary and may be omitted in an actual calculation.


The following example may help to make the process clear. We wish to invert the matrix

- 0 3
- 1


Γ6 0

31

- 1
- 2j


###### b

We write this matrix and a unit matrix side by side and carry out the same operations on each. The operations are,

Initial matrices.

0

1 0

- 0
- 1 0


Γ6 0 311

###### p[3 31 2] 1Ί

- 0
- 1 0


- 0
- 1


Subtract half first row from last.

- 0
- 1 0


###### Γ6 0 3 ]| 0 3 1

- 0
- 1 0


- 0

- - i

1

- 0

-i

- 1 0


- - 3

10 3

- - 3




Lo 1 ill

Subtract third of second row from last.

- 0
- 1


###### Γ6 0 3]

P 3 M Lo 0 iji

- 0
- 1


- -h

- 0
- 1


- - 2

6 3

- - 2


Multiply last row by 6.

0 0 6

Γ6 0 311 0 3 1

###### Lo 0 ij

Subtract last row from second and three times last row from first.

18 3 - 6

Γ6 0 0ΊΙ 0 3 0

Lo 0 ij

6

![image 51](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile51.png)

VECTORS AND MATRICES 43

- - 3
- - 2 6


Divide first row by 6 and second row by 3.

Ί 0 01 0 1 0 0 0 ll

1 1

Γ 5

TI

- 2

###### L-3

As a result of these operations A has been reduced to / and / has been replaced by A'1. The reader may easily verify by direct multiplication that

- -3"
- - 2 6


1 1

= "1 0 01 0 1 0 0 0 lj

6 0 3 0 3 1 3 1 2

5

T1 3

- 2

It may be noted that the inversion of a matrix by a process of this type takes about n3 operations, i.e. about three times as much work as the solution of the corresponding system of equations.

2.7. The Linear Programming Problemf

The solution of systems of simultaneous equations, the inversion of matrices and the determination of eigenvalues and eigenvectors are usually regarded as the classical numerical problems of matrix algebra. In recent years, however, another type of problem has appeared which has given rise to what is now known as "linear programming". In view of the association of the word "programming" with digital computers this name is perhaps rather misleading. The word is used here in its normal sense of "planning", and in fact much of the early work on linear programming was done during theoretical studies of problems connected with military supplies.

The basic mathematical problem is to maximize (or minimize) a linear function of a set of variables when these variables have to satisfy a system of linear inequalities, i.e. to find a set of numbers JC satisfying the conditions Ax ^ b which maximizes (or minimizes) a function y = c'jt, where the matrix A and the vectors b and c are known. (The symbol < appearing in a vector equation is

t This section is only relevant to section 7.7 and may be omitted at a first reading.

![image 52](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile52.png)

###### 44 MATRIX METHODS OF STRUCTURAL ANALYSIS

here taken to mean that every component on the right-hand side is greater than or equal to the corresponding component on the left.) In practice the inequalities represent limitations (such as maximum allowable stresses in a structure) imposed by the physical nature of the system, while the function y which is to be maximized is a measure of how "good" the solution is. In most cases there will be a large range of possible solutions, all satisfying the required conditions, and the problem is to find the solution which is in some sense the "best".

As with the other standard matrix operations, most modern computers have routines available for solving the linear programming problem in the general form in which we have stated it. The design of such routines is the province of the numerical analyst, and it would be out of place to give an account of the general theory here. We shall merely give a very simple example of a linear programming problem to illustrate the general form which the solution takes.

We consider the problem of finding the values of the variables xi9 x2 which maximize the function y = xt + 2x2, subject to the conditions

xt < 1 x2 < 2 2xl + 5x2 ^ 10 4*! + x2 < 4 Since there are only two variables the problem can be solved graphically. The inequalities divide the xlx2 plane into a "permissible" and a "nonpermissible" region, points satisfying all four inequalities lying within the shaded region shown in Fig. 2.3. If we superpose on this region contours of constant y it becomes obvious that the maximum will be attained at one of the vertices of the permissible region, where two of the four inequalities are satisfied as equalities. In this example the solution is at the point S in Fig. 2.3, i.e. at the point xx = 5/9, x2 = 16/9. It is apparent that it is possible to have a system of inequalities for which no permissible solutions exist, and functions (such as y = xx — 2x2 in the present example) for which no finite maximum exists.

All these features may be generalized to the problem of n

![image 53](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile53.png)

###### VECTORS AND MATRICES 45

variables satisfying m inequalities. The "permissible region" becomes a region in w-dimensional space, and the solution (whose existence is normally arguable on physical grounds) is a vertex of this region, where n out of the m inequalities are satisfied as equalities. The whole difficulty of the linear programming problem from a computational point of view lies in devising a general scheme for finding the correct set of inequalities to be solved as equalities which does not involve considering all the possible combinations.

FIG. 2.3. Graphical solution of a simple linear programming problem.

In structural theory the linear programming problem arises in both plastic collapse analysis and plastic limit design. The first of these subjects is discussed in section 7.7.

![image 54](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile54.png)

CHAPTER 3

###### Basic Relationships and Definitions

As mentioned in section 1.4, all methods of analysing skeletal structures make use of three basic sets of equations—the stressstrain relationships of the members, the compatibility conditions satisfied by the member end-displacements, and the equilibrium conditions satisfied by the member end-loads. The purpose of the present chapter is to express these equations in general matrix form suitable for use in the development of analytical methods in later chapters. Before this can be done, however, it is necessary to define a notation which is precise yet sufficiently general to apply to all the structures which we wish to discuss.

A diagram of a skeletal structure consists essentially of a series of lines representing the members, connecting points representing the joints. When considering a general structure we shall denote the joints by capital letters A, B, ..., N9 (or numbers 1,2, ...,) the actual assignment of letters or numbers to specific joints being done in an arbitrary manner. The term "joint" refers here to points in the structure which can displace under the action of applied loads—points at which the structure is attached to a rigid foundation will be referred to collectively as joint O (or 0). In the same way we identify the members by lower case letters a,b9...,n. In considering the properties of individual members we shall use the suffixes 1 and 2 to refer to the two ends. It would be possible to assign these suffixes arbitrarily, but we shall find it convenient to adopt the convention that the end of the member

- at the joint whose identifying letter comes nearest the beginning of the alphabet is referred to as end It. Thus a member connecting joints B and K has end 1 at joint B.


t The letter O (denoting a foundation attachment) is here regarded as coming before A.

46

![image 55](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile55.png)

###### BASIC RELATIONSHIPS AND DEFINITIONS 47

To define the orientation of a member in space it is necessary to specify the angles which it makes with the coordinate axes in an unambiguous manner. We shall find it convenient for this purpose to introduce the idea of the direction of a member, defined as the line running from end 1 to end 2. Directions may be indicated on line diagrams by arrows placed on the members, in the same way that the directions of currents are indicated in electric networks.

This systematic method of labelling the joints and members of a structure makes it easy to specify any structure, however complex, in the form of a list of members and joint connections. This form of specification is necessary if the structure is to be analysed by a general computer program, since a computer cannot read diagrams, and requires all its information in numerical form. Figure 4.1 shows how this system of labelling appears when applied to a simple structure.

###### 3.1. Notation for Loads and Displacements

Throughout the remainder of this book the term "joint displacement" will be used to refer to the vector formed by the group of variables which together define the translation and rotation of a joint, and the term "member end-displacement" will be used to refer to the corresponding group of quantities associated with the end of a member. Displacement vectors of this sort will be denoted by the symbol d, with appropriate suffixes to indicate the joint or member referred to. The number of variables in a displacement vector will of course depend on the type of structure considered. In a general three-dimensional space frame each displacement will have six components—three translations and three rotations, while in a plane pin-jointed truss there will merely be the two components of translation.

In the same manner the terms "joint load" and "member endload" will be used to refer to the vectors formed from all the force and moment components acting on a joint or on the end of a member. For each component in a displacement vector there will

![image 56](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile56.png)

###### 48 MATRIX METHODS OF STRUCTURAL ANALYSIS

be a component in the corresponding load vector, forces being associated with translations and moments with rotations. The symbol p will be used to denote such load vectors, the number of components depending, as before, on the type of structure

###### *,.*,

$r , P*

FIG. 3.1. Convention for three-dimensional space structures, showing senses in which displacement and load components are considered positive.

considered. Thus in a general space frame with coordinate axes x, y, z the displacement and load vectors will have the general form

d = p,lk

###### P = ~Px

- Py
- Pz m,


###### k \ekx k.

m} _m,

where δ, θ, ρ and m indicate translation, rotation, force and moment components respectively. Throughout the book we shall use the right-handed system of coordinate axes shown in Fig. 3.1,

![image 57](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile57.png)

###### BASIC RELATIONSHIPS AND DEFINITIONS 49

the sign convention for the various components being as shown in that figure.

Since a plane structure may be regarded as a special case of a space structure it is natural to use a right-handed system also when discussing plane structures. Two alternative right-handed coordinate systems are shown in Fig. 3.2—it is apparent from

(o) (b)

FIG. 3.2. Alternative right-handed coordinate systems for plane structures.

- Fig. 3.1 that these are merely two views of the xy plane, one seen from the positive z axis and the other seen from the negative z axis. It follows that any system of equations which is true in the coordinate system of Fig. 3.2a is automatically true in the system of Fig. 3.2b. We shall write the displacement and load vectors for a plane structure in the form


P*l

###### P = >*1

###### \?kJ

Py\

_m\

Where a number of p's or <Fs are combined to form vectors (representing, say, the complete set of joint loads or joint displacements of a structure) we shall denote such vectors by the symbols p and d.

When deriving the load-displacement relations for a particular member of a structure it is natural to choose a coordinate system which makes the form of the equations as simple as possible.

![image 58](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile58.png)

Such a system belongs, as it were, to the member, and is not concerned with the spatial orientation of the member in the structure. For example, when analysing an initially straight beam one would naturally choose the direction of the unloaded beam as the x axis, and make the y and z axes coincide with the principle axes of the cross-section. Such a set of coordinates will be called a member coordinate system.

When the members are connected together to form a structure, on the other hand, it is necessary to have a common coordinate system for all the member end-loads and end-displacements. It is clearly impossible to write down conditions of equilibrium and compatibility involving p's and <f s unless all these vectors are expressed in the same coordinate system. A set of coordinates used for defining the joint displacements of a structure or the loading applied to it will be called a set of frame or system coordinates.

There are some types of structure, such as continuous beams, where all the member coordinate systems coincide naturally with the frame coordinate system. In most cases, however, the two types of system are different, and it is necessary at some stage of the analysis to change from one to the other. One advantage of matrix notation is the ease with which transformations of this sort may be made. In general we shall adopt the practice of developing the equations for various types of structural element in their own appropriate coordinate systems, and then use the transformation rule developed in section 2.4 to convert these equations into system coordinates. In dealing with quantities associated with members it is sometimes necessary to have an indication of whether they are expressed in member or system coordinates. Where this distinction is required we shall indicate quantities expressed in system coordinates by primes. This convention only applies to variables associated with membersjoint loads and displacements must obviously be measured in system coordinates, but since there is no possible ambiguity in such cases the primes will be omitted.

![image 59](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile59.png)

###### 3.2. A Note on Sign Conventions

The sign convention for loads introduced in the previous section is a convenient one for expressing forces and moments applied to joints and to the ends of members. In analysing the stresses at internal points of members, however, it is more convenient to choose a convention based on the sign of the induced strain. In analysing a beam, for example, one might sensibly adopt the convention that a bending moment associated with a positive curvature of the neutral axis is treated as a positive bending moment, while a shear force which acts in a clockwise sense is a positive shear.

It is important to realize that these two sign conventions are fundamentally incompatible. The simplest example is to be found in the analysis of pin-jointed frames. When considering the loads acting on the joints it is reasonable to consider a component of applied force to be positive when it acts in the positive x or y direction, as shown in Fig. 3.3a. When calculating stresses,

FIG. 3.3. An example of the two types of sign convention. (a) Externally applied force components in a pin-jointed frame. ib) Internal self-equilibrating force pair in a pin-jointed frame.

LC

![image 60](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile60.png)

on the other hand, it is equally reasonable to call a tensile force positive and a compressive force negative, as shown in Fig. 3.3b. It is obvious that the two conventions cannot be made to agree at both ends of a member at once.

The same incompatibility appears in devising a convention for bending moments. A "sagging" moment at the left-hand end of a beam acts in a clockwise sense, while at the right-hand end its sense is anticlockwise. This change is illustrated in Fig. 1.2. In load system (a) the moments mCB and mBC both produce curvature in the same sense, and if they were obtained from the differential equation of bending they would both be computed with the same sign. When constructing load system (b), however, these two moments must be given opposite signs in order to make the convention for applied moments consistent at the two joints.

Once the existence of the two types of convention has been explicitly recognized there is little risk of confusion. In this book we shall work consistently with the convention introduced in the previous section—that is to say, with a convention of the type

- shown in Fig. 3.3a rather than Fig. 3.3b.


###### 3.3. Stiffness and Flexibility Matrices

The equations connecting the end-loads and the end-displacements of a structural member can be written in a number of ways. In the equilibrium method the appropriate form consists of expressions giving the end-loads pu Vi ifl terms of the enddisplacements du d2. For members which behave in a linear manner these expressions have the general form

Pi = #ιι<*ι +K12d2>|

(3.1) p2 = K2ldl + K22d2)

where the size of the matrices Κίί9 etc. depends on the number of components in the load and displacement vectors.

The equilibrium method described in chapter 4 uses the conditions of displacement compatibility and joint equilibrium

![image 61](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile61.png)

to construct the set of load-displacement equations for a complete structure out of the load-displacement equations (3.1) of the individual members. This set of equations may be written

p = Kd (3.2)

where p indicates the complete set of applied joint loads and d indicates the corresponding set of unknown joint displacements.

In discussing the elementary problem of the extension of a spring it is usual to introduce the concept of "stiffness" through the equation

force = stiffness x displacement

It is natural to use this concept in a rather more general sense when referring to equations such as (3.1) and (3.2). Thus we shall call K1U K12, etc. member stiffness matrices, and refer to K in (3.2) as the stiffness matrix of a structure.

Returning to the case of the simple spring we may also write the relationship between force and displacement in the form

displacement = flexibility x force

thus defining "flexibility" as the reciprocal of stiffness. At first sight it might seem that (3.1) could also be written in an analogous form, the displacements di9 d2 being expressed in terms of the loads pl5 p2- However, it is easy to see that this is not possible. While the end-loads are defined for any pair of end-displacements, the converse is not true, since the member may be given an arbitrary rigid-body displacement without affecting the forces acting on its ends. Mathematically this corresponds to saying that the equations (3.1) are necessarily singular and therefore cannot be written in inverse form.

Although equations (3.1) are in a form suitable for use with the equilibrium method, in other methods it is often desirable to work in terms of member deformations rather than member enddisplacements. For while the end-displacements of a member under given end-loads are indeterminate due to the possibility of

![image 62](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile62.png)

###### 54 MATRIX METHODS OF STRUCTURAL ANALYSIS

rigid-body movement, the deformation of the member is unique. We define the deformation vector of a member as the displacement of end 2 relative to end 1, i.e. the displacement which end 2 would have under the given loading if end 1 were rigidly fixed, and denote it by e. Thus we may write the second of equations (3.1) in the form

Pi = K21e (3.3)

obtaining pt from p2 simply by considering the equilibrium of the member. Since e is defined uniquely for any given value of p2 we may invert (3.3) and obtain

e = F22p2 (3.4)

where F22 is the inverse of K22. By analogy with the simple concept of flexibility we may term F22 a, flexibility matrix.

In this approach the general displacement of a member is regarded as being the sum of a deformation, defined uniquely by the loading and the elastic properties of the member, and a rigid-body movement which is independent of these elastic properties. This form of the load-displacement equations is developed in chapter 5 and used in subsequent chapters.

Although the equations (3.1) for a single member are singular and therefore cannot be inverted, the complete load-displacement

- equations (3.2) will always have a unique solution, provided that the members form a structure and not a mechanism. In other words we may argue on physical grounds that the matrix K will always be non-singular, so that (3.2) may be inverted and written in the form


d = K 1 p = F p (3.5) where F is termed the flexibility matrix of a structure.

The matrices K and F represent alternative mathematical statements of the complete load-displacement characteristics of a structure. If we consider a load system p in which a certain

![image 63](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile63.png)

###### BASIC RELATIONSHIPS AND DEFINITIONS 55

component^· is equal to unity and all other components are zero, then it follows from (3.5) that the displacement component d{ is equal to the element Ftj of the flexibility matrix F. Now we know from the reciprocal theorem that F^ = FJi9 so that the matrix F is symmetric. It follows that K is also symmetric. We shall find that this characteristic of symmetry runs through a great deal of our analysis. It provides a useful check in both the algebraic and the computational stages of the work.

3.4. Equilibrium and Compatibility Conditions: Virtual Work

The systematic notation for loads and displacements described in section 3.1 makes the writing down of equilibrium and compatibility conditions a very simple matter. As an example, consider the conditions associated with the joint X in Fig. 3.4.

FIG. 3.4.f A typical joint of a structure.

t Throughout this book general load and displacement vectors will be represented in diagrams by single arrows, the existence of moments and rotations being implied where appropriate.

In our notation the equilibrium conditions are simply

Pia + Pit + Pu = Px (3.6) while the compatibility conditions are

à'ia = à'ib = à\c = Ax (3.7)

![image 64](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile64.png)

###### 56 MATRIX METHODS OF STRUCTURAL ANALYSIS

It might appear at first sight that there is no particular connection between equations (3.6) and (3.7). However, there is in fact an extremely important relationship between these equations, which we shall find wherever equilibrium and compatibility conditions have to be satisfied.

Let us write the relevant member end-loads and end-displacements in the form

d' = à'ia à'ib

Pm = Pia Pib

###### Ldic

.Pu.

where the suffix m is used to indicate "members". Equations (3.6) and (3.7) may now be written

(3.8) (3.9)

PX = U I i]Pm

7 / I

from which we see that the matrix (in this case merely a single row of unit matrices) which connects the joint and member load vectors is the transpose of the matrix which connects the corresponding displacement vectors.

We may show that this result is not fortuitous as follows. We first write (3.8) in the form

###### PX = CPm (3.10)

We now impose a virtual displacement 5dx on the joint X, keeping the load vectors constant during the displacement in the usual way. Since the joint is in equilibrium throughout the virtual displacement, the work done by the applied load px must equal the work done by the member end-loads p^. Thus we have

P Ä = P X (3.11) and since (3.10) may be written as px = p'^C*, (3.11) becomes

![image 65](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile65.png)

###### BASIC RELATIONSHIPS AND DEFINITIONS 57

p^C<5rfx = Pm^^in· Since the virtual displacement is quite arbitrary it follows that

ôâ'm = Côdx (3.12)

So far our argument has made no assumption of linearity. If now we make the usual assumption of the displacements of the structure being small we may replace the virtual displacements in

- (3.12) by the real displacements d^ and dx, thus obtaining the equation


d'm = Cdx (3.13) which corresponds to (3.9).

This analysis is important in that it shows that conditions of compatibility and equilibrium are not independent, but are very closely related. We shall use reasoning similar to that given above in a number of places in later chapters. The relation between force and displacement transformations typified by equations

- (3.10) and (3.13) is known in general as contragredience.


![image 66](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile66.png)

###### CHAPTER 4

###### The Equilibrium Method

IN this chapter we give a more detailed account of the equilibrium method, which we have already described in general terms in section 1.4. As stated in section 3.3, the equilibrium approach uses the load-displacement equations of a member in the general "stiffness" form (3.1), combining similar equations for all the members into a set of load-displacement equations for a structure.

Before conditions of equilibrium and compatibility can be applied to the various member equations (3.1) these equations must be expressed in system coordinates in the form

Pi =Κ'ΐ1<Ί +K'l2<*21 /4 j)

Vl = ^21^2 + #22^2)

One of the most important features of the equilibrium method presented in this chapter is the way in which the elastic properties of the members and their orientation within the structure are introduced into the analysis before any consideration of joint equilibrium or compatibility takes place. The equations (4.1) for the individual members contain a complete description of the load-displacement characteristics and orientation of the members, while the equilibrium and compatibility conditions merely supply information about the external loading and describe the way in which the various members are connected together.

The advantage of this approach is that it splits the analytical work into two quite separate parts. In developing equations

- (4.1) we are only concerned with single members and their 58


![image 67](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile67.png)

###### THE EQUILIBRIUM METHOD 59

elastic properties, and need not worry about the complexity of the structure of which these members may form a part. In applying the conditions of equilibrium and compatibility, on the other hand, we need only consider the topology of the structure, i.e. the way in which the members are connected together. By working with load and displacement vectors which are represented by single symbols we can make this part of the analysis quite independent of whether the structure is a plane frame, a space frame, or a pin-jointed truss.

Another important feature of the method, at least as we shall describe it, is the systematic way in which the displacement variables are assigned to the joints. We shall assume that in any particular structure each joint displacement vector has the same number of components—six for a rigid-jointed space frame, three for a rigid-jointed plane frame or a pin-jointed space truss, and two for a pin-jointed plane truss. It follows from this assumption that the methods developed for rigid-jointed structures always take account of axial strains in members, whether the structures are rectangular frames (in which axial strains are normally ignored) or braced trusses. This may lead to a considerable increase in the numerical work involved in analysing a particular structure, but it makes the analysis systematic and general in application. As stated in section 1.1, these are qualities which are sufficiently desirable from a computer point of view to justify the increased amount of calculation.

As with other methods of analysis in which the basic ideas are simple it is difficult to know who may be said to have "discovered" the equilibrium method. Credit for this seems usually to be given to Bendixen and Ostenfeld (Ostenfeld, 1926). The notation used in the present chapter is derived from that employed by Kron (Kron, 1944).

We introduce the method by considering two simple examples. These are of course only discussed as illustrations—it is not suggested that one should use matrix methods to analyse such structures in practice. Throughout the chapter we assume the

![image 68](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile68.png)

60 MATRIX METHODS OF STRUCTURAL ANALYSIS validity of the approximations of linear small-deflexion theory discussed in section 1.2.

###### 4.1. The Analysis of a Plane Pin-Jointed Truss

For the first example we consider the plane pin-jointed truss

- shown in Fig. 4.1. For the sake of simplicity we consider the case


FIG. 4.1. Example of a pin-jointed truss, showing directions of system coordinate axes xf and y\

where all the members are straight and of uniform cross-section, and assume that the material of which the members are made obeys Hooke's law.

The first part of our analysis is quite general and is concerned with finding the form taken by equations (4.1) in the case of a member of a plane pin-jointed structure. We consider a member of length L and cross-sectional area A. Since a pin-ended member can only carry forces acting in the direction of its length the member coordinate system is purely one-dimensional, as shown in

- Fig. 4.2. In this figure the displacements dl9 d2 are assumed to be measured from the initial unstressed position of the member. The load-displacement equations in this coordinate system are simply Pi = — p2 = (EA/L)(dl — d2), which we may write in the form


pt = Kdi — Kd2 p2 = -Kdx + Kd2

###### (4.2)

![image 69](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile69.png)

###### THE EQUILIBRIUM METHOD 61

where K = EA/L. (It is not necessary to write down an equation for forces normal to the bar, since we know that these must be zero.) These equations are in a form similar to equations (3.1), although in this simple case the vectors p and d have only one component and K is merely a single coefficient.

Equations (4.2) define the end-loads pl9 p2 for any given pair of displacements du d2. It will be noticed that the equations are

FIG. 4.2. Member coordinate system for a pin-ended bar.

symmetric, as we should expect from the reciprocal theorem. It is not possible, however, to "solve" these equations and obtain the d's in terms of the p's, since the matrix

Γ K -K~\

is singular. This is a reflection of the fact that the member may be given an arbitrary rigid-body displacement without affecting the forces acting on its ends. (The quantity (d2 — dx), on the other hand, represents the deformation of the member, and is defined uniquely by (4.2) for any given pair of end-loads.)

Equations similar to (4.2) hold (in the appropriate individual member coordinate systems) for each member of the truss under consideration. Before we can apply conditions of joint equilibrium and displacement compatibility, however, it is necessary

![image 70](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile70.png)

###### 62 MATRIX METHODS OF STRUCTURAL ANALYSIS

to transform the loads and displacements appearing in (4.2) into the overall frame coordinate system x'y' shown in Fig. 4.1. In making this transformation we shall assume that the displacements of the joints of the structure are small enough in comparison with the lengths of the members for us to neglect the change in the orientation of a member to the frame coordinate axes. This is the usual approximation of linear structural theory, and corresponds to the writing of the equilibrium equations for the undistorted structure, rather than for the distorted structure in which they must actually hold. Thus in Fig. 4.3 we shall assume that the change in the angle a due to the loading of the structure may be neglected, and take the value of a appropriate to the undistorted structure.

y k

FIG. 4.3. Change from member to system coordinates for a pinended member inclined at an angle a to the x' axis.

From Fig. 4.3 we see that in frame coordinates the two components of an end-load vector are given by

p'x = p cos a Py = p sin a

which we may write in the form

V' = Tp (4.3) where

[

cosal sinaj

T =

![image 71](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile71.png)

###### THE EQUILIBRIUM METHOD 63

(It may be noted that although T is not a square matrix and therefore has no inverse, equation (4.3) may be written in the "inverse" form p = T*p'.) In the same way an end-displacement d may be expressed in terms of the components of displacement in system coordinates as d = δ'χ cos a + δν sin a, which may be written in the form

d = [cos a sin a] Γ<5^1

###### U;J

or

d = Ta' (4.4) It will be noticed from the figure that the end of a member may also have a displacement component perpendicular to the member, and this could be expressed in terms of the quantities δχ and ô'r Such displacements, however, have no effect on the end-loads, and therefore need not be included in the analysis.

In this case it is easy to derive equation (4.4) by direct geometrical considerations. It is also possible to derive the same equation by using the principle of virtual work. The reasoning follows very similar lines to that given in section 3.4. It is clear that the work done by a force in moving through a given distance must be the same whatever coordinate system is used to measure the force and distance. Thus the work done by the force p moving through a distance d in Fig. 4.3 is equal to pd, and it is also equal to ρχδχ + p'yôfy = pnd'. Thus we have pd = pftd\ and if p = Tp it follows that pn = pV. Hence we have pd = pVd\ and, sincep is a general load, equation (4.4) follows.

We now multiply equations (4.2) by T and use equation (4.3) to give

p[ = TPl = TKdx - TKd2 p'2 = Tp2= -TKd1 + TKd2

Substituting for dY and d2 from equation (4.4) gives p\ = {TKT)d[ - (JKT)d'2 p>2 = _( TKT)d\ + ( TKTf)d2

![image 72](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile72.png)

If we now write K' = TKT\ we obtain

Pi= K'i[-K'd'2\ p^-K'd^+K'd'ij K*'D)

The reader may easily verify that K' = (EA/L) Γ cos2 a sin a cos a [sin a cos a sin2 a

It will be noted that the symmetry of (4.2) is preserved by the transformation. The change of coordinates does not, of course, alter the fact that the load-displacement equations are still singular.

Having obtained general expressions for the member end-loads in frame coordinates we now proceed to the next stage of the analysis, which is the assembly of the matrix K. Applying the condition that the displacements of the ends of members must be equal to the displacements of the appropriate joints we have the following equations

- Member a
- Member b
- Member c
- Member d
- Member e


i/; = o <f; = o

d'i = dA d2 = dB d'i = dB d'2 = dA d'2 = dBi

(4.6)

- d[=0
- di=0


d\ = dA

Substituting these expressions for the member end-displacements into equations (4.5) for each member gives

- Member a
- Member b
- Member c
- Member d
- Member e


Pia = KdA

Pib = KbdB Pic = K'cdß P'id = KddA Pie = K'edA - KedB

(4.7)

Pie = -K'edA + KedB)

The expressions for p[ have been omitted in the case of members a, b, c and d, since they are merely foundation reactions and do

![image 73](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile73.png)

###### THE EQUILIBRIUM METHOD 65

not enter into the joint equilibrium equations. The primes are omitted from dA and dB since these must obviously be in system coordinates.

The conditions of joint equilibrium in this example are simply

- PA = Pia + Pid + Pie
- PB = Plb + Pic + Pie


where once again the primes are omitted from pA and pB. Substituting into these equations from (4.7) gives

ρΛ = \Κ'Λ + Κ'Λ + Κ'9 -K'e ]\dA] (4.8)

###### pB\ = l - x ; K'b + K'e + K'e\[dB\

which is the form of equation (3.2) in this particular example. The stiffness matrix K in equation (4.8) is an example of a partitioned matrix, the elements in this case being 2 x 2 matrices. This is a general characteristic of the equilibrium method—we shall find that in most cases these elements may be treated as though they were ordinary scalar coefficients. It will be noted that the matrix in (4.8) is symmetric, this being a consequence of the reciprocal theorem, as mentioned earlier.

Although the load-displacement equations for the individual members are singular, we may argue on physical grounds that the

- equations (4.8) must have a unique solution for a given loading, and that therefore the complete stiffness matrix of the structure must be non-singular. All that remains, therefore, is the solution of (4.8) for the displacements dA, dB and the subsequent use of


- (4.7) to find the internal forces in the members. It may be mentioned here that if a structure has to be analysed for a large number of different loadings it may be better to invert the stiffness matrix K to give what we have called the flexibility matrix F, and then to find the displacements for each loading from the equation d = Fp. By this procedure the matrix inversion only has to be carried out once; the subsequent analysis for any particular loading merely requires multiplication of the load vector p by the matrix F. This point is discussed in section 9.4.


![image 74](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile74.png)

It is interesting to note the way in which the stiffness matrix reflects the arrangement of bars in the structure. The bars a and d merely contribute to the direct stiffness of joint A, and consequently their K' matrices only appear in the first leading diagonal element, which relates the displacement of joint A to the load applied there. Similarly the bars b and c merely contribute to the stiffness of joint B, and their K' matrices consequently appear only in the second leading diagonal element. The bar e, on the other hand, connects joints A and B, and contributes to both the leading diagonal elements. It also provides the offdiagonal elements — K'e which constitute the mathematical link

###### /*P*

FIG. 4.4. Simple pin-jointed structure with one joint and two degrees of freedom.

between the displacements dA and dB, thus reflecting the physical link between the two joints which the bar provides in the structure.

This close relationship between the form of the stiffness matrix and the geometrical arrangement of the structure makes it possible to write down the complete matrix in terms of the member stiffness matrices merely by inspection, without formally writing out the conditions of equilibrium and compatibility. The general rule is that if a member r connects joints /and J then K'r is added to the J'th and J'th leading diagonal elements, and — K'r is placed in the corresponding off-diagonal positions (i.e. row /, column J, and row J, column I). If we wish to modify a design and remove a member from a frame, we merely remove its K' matrices from the

![image 75](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile75.png)

###### THE EQUILIBRIUM METHOD 67

appropriate places in the complete stiffness matrix, without having to alter the remaining elements. (However, this will in general have the effect of altering all the elements of the flexibility matrix F.)

One of the most important features of the stiffness matrix of a structure is the fact that it is formed by adding up the stiffness matrices of the structure's component parts. If in Fig. 4.1 we prevent joint A from displacing we have the structure shown in Fig. 4.4, and equation (4.8) reduces to pB = (K'b + K'c + K'e)dB. This equation may be regarded as a generalization of the scalar

^N nrmwrrmrrrrr Π

###### ^ *3

• \ j — ormrnTinnnrrnp

FIG. 4.5. Simple system with one degree of freedom consisting of three springs in parallel.

equation p = (ki + k2 + k3)d for the force-displacement relationship of three springs of stiffness kl9 k2, k3 arranged in parallel as shown in Fig. 4.5.

###### 4.2. The Analysis of a Plane Rigid-Jointed Truss

In the analysis of plane structures by traditional methods it is usual to make a sharp distinction between trusses and frames, and to use different methods of analysis in the two cases. A truss is essentially a triangulated structure which would still be a structure if its joints were pinned. The bending moments induced by joint rigidity are usually small and indeed are often referred to as "secondary stresses". A frame on the other hand is essentially a structure which carries loads primarily by bending action, the

![image 76](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile76.png)

rigidity of its joints being essential to its function as a structure. In the conventional analysis of frames the axial strains are usually ignored.

The method described in this section, however, is equally applicable to frames and trusses. We shall illustrate it by considering the analysis of the truss shown in Fig. 4.1 when all the joints are treated as rigid. We shall find that the analysis has many features in common with the method described in the previous section.

In analysing a pin-jointed truss it is in fact unnecessary to place arrows on members to indicate their directions since the elements of the K' matrix appearing in equations (4.5) are unchanged if the angle a in Fig. 4.3 is increased by 180 degrees. In analysing rigid-jointed frames, however, the direction convention is important. Since moments and shear forces now have to be considered, the load and displacement vectors will have three components in both member and frame coordinates. We begin, as before, by considering the load-displacement equations for a single member. The coordinate system used is shown in Fig. 4.6,

y i

FIG. 4.6. Coordinate system for a uniform member in plane bending.

and we shall restrict our analysis to linear small-deflexion theory. Thus we shall ignore changes in the distance between the ends of a

![image 77](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile77.png)

###### THE EQUILIBRIUM METHOD 69

member due to curvature of the member, and retain the simple linear equations

Pxi = -Pxi = (EA;L)(ôxi - δχ2) (4.9)

for the load-displacement relations in the direction of the x axis. The curvature terms are omitted from equations (4.9) because they are non-linear rather than because they are small, but in most practical structures the effect of curvature on the length of a member is negligible at working loads. While it is true that in certain cases the effect of the linear axial strain terms may be equally small, this does not invalidate the use of (4.9) in a scheme of linear analysis.

If we restrict our attention to an initially straight member of uniform cross-section then provided that the axial force is small compared with the Euler load the moments on the ends are given by the slope-deflexion equations

mt = (6EI/L2)ôyl + (4EI/LM - (6EI/L2)ôy2 + (2£J/L)02) m2 = (6EIlL2)5yl + (lEI/QO, - (6EI/L2)ôy2 + (4£//L)02/ ^ , l u ; These equations may be found in any standard textbook on structural analysis, and we shall not, therefore, give their derivation here. As mentioned in section 3.1, these equations also hold in the alternative right-handed set of axes (Fig. 3.2b) in which y is measured downwards and the senses of 0 and m are reversed. In fact, as we showed in section 3.1, any set of equations which hold in the coordinate system shown in Fig. 3.2a must also hold in the coordinate system of Fig. 3.2b. The latter coordinate system is the one most commonly used in the analysis of continuous beams, but we have used the one shown in Fig. 3.2a in order to be consistent with the coordinate system used in the analysis of pin-ended members in section 4.1.

Adding the two equations (4.10) we obtain (m1 + m2)IL = pyl = -py2

= (12EÏ/L3)ôsl + (6EIIL2)et - (l2EIJL2)Ôv2 + (6ΕΙ]ΐ})θ2 (4.11)

![image 78](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile78.png)

The equations (4.9), (4.10) and (4.11) may now be combined to give the matrix equations

= 1

0 ]

piil

0 12E//L3

EA/L 0 0

###### ÏPxl

6EI/L2

###### r^kJ1

\Pyi

###### 6EI/L2

###### 4EI/L J 0 ]

lmi.

###### +

0

'-EAjL 0 0

\δχ2\

6E//L2

- -12EIIÛ
- -6EIIL2 0
- -12E//L3 6EI/L2

0 12EJ/L3

- -6EI/L2


<5y2

###### kJ

###### 2EI/L J

_ 1

pxil

0 "1 6EI/L2

-EAjL 0 0

\Pxl \Py2

###### P,ikJ

###### 2EI/L J 0 ]

Lm2_

###### Ρχ21

+ 1

EAjL 0 0

6EI/L2

rj·2

###### kJ

4EI/L J

These equations may now be written in the form

Pi = £ ΐ 1 < Ί +#12^21 Pi = -^21^1 + #22^2/

(4.12)

It will be noted that these equations are symmetric, since the matrices Ku and K22 are symmetric and K2\ is the transpose of X12. They are also singular, since the end-loads pl9 p2 have to satisfy the three equations of member equilibrium, and the member can suffer a (small) arbitrary rigid-body displacement without affecting the end-loads.

As in the previous section, the next step is to transform these equations into system coordinates. If the direction of the member is inclined at an angle a to the x' axis, as shown in Fig. 4.7, the equations relating the components of a load vector in member and system coordinates are

"cos a

— sin a cos a

0*

= = =

'Px

- P'x
- P'y m'


sin a 0

- 0
- 1


Py

0

###### m

![image 79](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile79.png)

###### THE EQUILIBRIUM METHOD 71

which may be written as/?' = Tp in the same manner as before. In contrast to the case of a pin-ended member Γ is now a square orthogonal matrix with an inverse equal to its transpose, so that p = Tp'. As before, the relationship between the end-displacement vectors may be shown to be d = Vd'. This may be done directly from geometrical considerations, or by the method described in section 3.4.

Fio. 4.7. End-loads and end-displacements as they appear in member and system coordinates. (Moments and rotations are unchanged.)

Using these relationships we may eliminate the p and d vectors from equations (4.12) to give

P\ = K'u<*i + Κ'ΐ2<*2 pf2 = Kf2Xdfl +K22d2 (4.13)

where Kij= 7K0T', (/,y = 1,2). Equations (4.13), like equations (4.12), are symmetric and singular. The matrix Κ[γ has the form

SC(EAIL - 12EI/L3) - S 6EI/L2' S2EA/L + C2 12EI/Ü C 6EI/L2

VC2EA\L + S2 12EI/Û SC(EA/L - 12£//L3)

-S6EI/Û C 6EI/L2 4EI/L where S = sin a, C = cos a. The other matrices are similar.

![image 80](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile80.png)

###### 72 MATRIX METHODS OF STRUCTURAL ANALYSIS

The assembly of the complete equations for the truss follows very much the same pattern as has already been described in the pin-jointed case. The equations of joint compatibility (4.6) are unchanged, although the displacement vectors in those equations now have rotations included in their components. Substituting these expressions for the end-displacements of the members into equations (4.13) for the individual members gives

- Member a p2a = (K22)adA \
- Member b p2b = (K22)bdB
- Member c p2c = (K22)cdB
- Member d p'2d = (K22)ddA
- Member e p'le = (K^)^ + (K[2)edB Pie = Wide* A + {K'll)edB^


(4.14)

where, as before, primes are omitted from the displacement vectors since these must obviously be defined in the frame coordinate system. These equations are identical with (4.7), except for the suffixes which now have to be attached to the K' matrices, and the fact that the end-loads now have moment components. As before, the expressions for p[ have been omitted in the case of members <z, b, c and d.

The conditions of joint equilibrium are also exactly the same as before,

- PA = Pia + Pià + Pie\ /4 |5)
- PB = Plb + Pic + Plej


Substituting the equations (4.14) into these equations gives

PA] = \(K'22)a + {K'22)d + (K\x\ ^ (K'12)e ! Γ^PßJ L (K'll)e (K'll)b + (K2l)c + (K'll)e\ \_dB.

(4.16)

It will be seen that these equations are very similar to the equations (4.8) derived for the pin-jointed truss. As before, the form of the complete stiffness matrix reflects the arrangement of bars in the

![image 81](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile81.png)

###### THE EQUILIBRIUM METHOD 73

structure. The addition of the two joint rotations as extra degrees of freedom means that the equation (4.16) represents six linear simultaneous equations for the six components of joint displacement. As before, once these equations have been solved, the internal forces and moments in the truss may be found from (4.14).

In this particular problem the equilibrium method has given us a complete secondary stress analysis of a rigid-jointed truss. If now we remove the members c and d from the structure we obtain an unbraced portal frame, which would normally be analysed in quite a different manner. However, all we need to do to obtain a complete solution of the new problem (including axial strain effects) is to drop the matrices {Κ'22)€ and {K'22)d from equations (4.16), solve the resulting equations, and use the relevant equations from the set (4.14) to find the forces and moments acting on the ends of the remaining members a, b ande.

###### 4.3. The Assembly of the Stiffness Matrix of a Structure

It should now be clear that the assembly of the complete stiffness matrix of a structure from the individual member stiffness matrices depends only on the way the members are connected together, and not on the geometry of the system. Once the load-displacement équations (3.1) have been found for all the members of a structure and have been translated into frame coordinates, the application of the conditions of equilibrium and compatibility involves no further reference to the detailed characteristics of the elements, and may be carried out formally in terms of the p and d vectors and the K' matrices of the members. It is true, of course, that these vectors will have different numbers of components in different cases, and that the coefficients of the K' matrices will depend on the type of element involved, but as long as the equations are written in terms of vectors and matrices this does not affect their general form.

![image 82](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile82.png)

###### 74 MATRIX METHODS OF STRUCTURAL ANALYSIS

We now consider the problem of assembling the complete K matrix for a general structure. We imagine that the joints of the structure are denoted by A, B, ..., N, points of attachment to foundations being regarded as joint O. We shall assume that the rule for assigning directions mentioned earlier has been followed, so that they always run from the "lower" to the "higher" lettered joint. Consider now the contribution which a member r running from joint / to joint J {I < J) makes to the final set of loaddisplacement equations. The equations for the member are

Pi, = (* U)rdir + (* i2)^r

Pir = (K'lUA'lr + (K'llXd'lr

or, substituting the compatibility conditions d\r = dIf d2r = dj9 P'lr = (K'n)rdI + (K'12)rdJ

The equilibrium equations for joints / and / are

Pi = Pir + contributions from other members meeting at joint / PJ = Pir + contributions from other members meeting at joint J

where the contributions from the other members will be p\ vectors for those members with end 1 at the joint considered, and p'2 vectors for members with end 2 at the joint considered. Thus the load-displacement equations for joints / and J have the form

PJ — (#Ίι)Γέ// + {Kfl2)rdj + contributions from other members PJ = (^2i)r^/ + i^2i)Aj + contributions from other members Thus it follows that the presence of a member between joints /and

- J has the effect of adding its K' matrices to the stiffness matrix of the complete structure according to the following scheme,


![image 83](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile83.png)

75

###### THE EQUILIBRIUM METHOD

Column / Column J

row /

11

12

row J

. K

K

Since there is no load-displacement equation for the equilibrium of joint 0, the final stiffness matrix K has no row or column corresponding to joint O. Thus a member whose end 1 is a point of foundation attachment merely contributes its K22 matrix to the leading diagonal element of row J. Since Κ'2γ is the transpose of K[2 the contributions of the individual members to the final matrix are always such as to maintain its symmetry, so that in practice we need only consider the assembly of the leading diagonal elements and those above them—the "upper triangle",

- as it is usually called. The rules for the assembly of this upper triangle may be stated as follows :


- (1) The leading diagonal element of row / is the sum of the matrices Κ[χ or K22 of all the members meeting at joint /, the matrix K'Yl being selected if the member has end 1 at the joint, and the matrix K22 being chosen if the end at the joint is end 2.
- (2) The off-diagonal elements of row /, corresponding to columns J,K,L, ... > I, are the K'l2 matrices of the members connecting joint / to joints /, K, L, ... . If a joint is not directly connected to / by a member, then the associated element is zero. (Due to the symmetry of the complete matrix it is only necessary to consider members which have end 1 at joint /.)


The reader will find that applying these rules to the frame shown in Fig. 4.1 leads to equations (4.16), as we should expect.

###### D

![image 84](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile84.png)

76 MATRIX METHODS OF STRUCTURAL ANALYSIS As a further example, applying the rules to the frame shown in Fig. 4.8 gives the equations

(K'22)a (K'l2)c (K'12)d 0

- PA
- PB


###### + (K'„)C

+ (K'11)d

(K'22)„ 0 (K'i2)e

+ (K'22\.

###### + (*'u),

Pc

dD

* * * \**-22Je

PD

+ (K'22)f.

c

f

D

###### * -

d '

>e

r

A

B

'

^b

0 '

~77~n77

o

FIG. 4.8. Example of a rigid-jointed frame.

where only elements in the upper triangle of the stiffness matrix have been shown.

A term on the leading diagonal of the final stiffness matrix represents the "direct" stiffness of a joint, i.e. the load required

- at the joint to produce unit displacement of that joint, all the other joints being held fixed. The off-diagonal elements correspond to connections between joints, and since there will usually be one member, at most, connecting any given pair of joints, the


![image 85](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile85.png)

###### THE EQUILIBRIUM MITTIOD 77

off-diagonal elements will normally be either single K\2 or K'2i matrices or zero.

In most structures joints are only connected to their nearer neighbours, and there are rarely more than six members meeting at any one joint. This means that, provided a systematic method of lettering or numbering the joints is adopted, the difference in the joint numbers at the ends of members will be small compared with the total number of joints, and as a result most of the elements of the stiffness matrix of the structure will lie near the leading diagonal. Such a matrix is called a "banded matrix". This characteristic is important in considering the numerical solution of the load-displacement equations on a digital computer, and we shall discuss its implications in section 9.4.

4.4. Stiffness Matrices for a Straight Uniform Member in a Space Structure

In sections 4.1 and 4.2 we considered the analysis of a simple plane structure, first with pinned joints and then with rigid joints. We now consider the more general case of a member in a rigidjointed space structure. We shall limit our analysis to the derivation of the appropriate K' matrices, since the technique for assembling the complete stiffness matrix of a structure described in sections 4.3 is formally the same whether the structure is plane or not.

The derivation of the stiffness matrices of a general threedimensional non-uniform member will be given in the following chapter. For the present we shall merely consider the case of a straight member of uniform cross-section. As in the previous sections, we shall assume that the material of the member obeys Hooke's law, and that the deformations are sufficiently small for ordinary linear theory to apply. The coordinate system which we shall use is shown in Fig. 4.9. We shall assume that the y and z axes are the principal axes of the cross-section, and denote the flexural rigidity of the beam in the xz and xy planes by EIy and

![image 86](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile86.png)

EIZ respectively. Since the y and z directions correspond to the principal axes, the flexural behaviour of the member in the xy and xz planes may be considered quite independently, the analysis given in section 4.2 being applied to each plane in turn. The equation (4.9) for axial strain will also be unchanged, so that the only new factor to be considered is the torsional stiffness of the

End I

End 2

FIG. 4.9. Member coordinate system for a member of a threedimensional frame.

member about its axis. If we consider the simple case in which warping effects are ignored, and assume the torsion axis of the member to coincide with the centre-line (i.e. the x axis), then the equation for twisting of the beam is simply mxi = —mx2 = (GJ/L)(ßxl - θχ2), where GJ/L is the torsional stiffness of the member. Thus the load-displacement equations of the member may be written in the usual form

Pi = filial +Kl2<*2 Pi = ^21<*1 + #22<*2

(4.17)

![image 87](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile87.png)

###### 79

###### THE EQUILIBRIUM METHOD

where

d = M δδ>\Ί

###### [>*"

\Py

Pz

###### ™x

θ,\

Θ,\

my

###### L™2_

###### ßA

and

###### κη =

0 0 0

' EA/L

0 0 0 6EIJÛ

12EIJL3 0 0 0 \2EIJL3 0 · 0 0 GJ/L 0 -6E1JÛ 0

0 0 0 0 0

- -6EIJL2 0 0 0

4£/,/L 0 0 4EIJL

0 0 0 6EIJL2

- -6EIy/Û 0 0 0


6EIJL2 0 0

###### κ12 = κ2ί=

0 0 0

'-EA/L 0 0 0 0 ο ■

12EIJÜ 0 0 0 -12£7„/L3 0 · 0 0 -GJ/L 0 6EIyIL2 0

lEîylL 0 0 2EIJL

-6EIJL2 0 0

and K22 is equal to Klt with the signs of the off-diagonal elements

-6EIy/L2 and 6EIJL2 reversed.

We now apply the usual technique for transforming (4.17) into frame coordinates. It is a matter of simple coordinate geometry to show that

![image 88](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile88.png)

(4.18)

0 0 0

0 0 0

0 0 0 x'z

x'z y'z

= x'x

x'y y'y

- Px
- Py
- Pz


- Px
- Py
- Pz m:


- y'x
- z'x 0 0


###### 7y

###### 7z

0 0 0

0 0 0

- m'x
- m'y
- m'z_


- x'x
- y'x
- z'x


- x'y
- y'y
- z'y


###### 7z

m j

_ 0

jn

7z_

where x'x, x'y, etc. are the cosines of the angles between the appropriate member and system axes. This may be written in the usual way as p' = Tp, and since Tis orthogonal it follows that p = Tp'. The vector d transforms in a similar manner, so that

we have d' = Td, d = Vd'. Thus we obtain the usual expression for the member stiffness matrices

x;,= TKur a i = i,2) (4.19)

The actual process of computing the K' matrices in a given case may be simplified somewhat by using the idea of partitioned matrices. We split each of the matrices K and T into four 3 x 3 matrices, writing them in the form

T0 0

###### r=

*.·,·=

\K'

###### o r0

###### [K

K.<sj

It is easy to show that

###### Ä:J= TKur

0

'Τ» 0 1

\K°

###### k

###### .o rj

L τ0κγ τ0 Τ0Κδ Τ0 Thus the triple matrix products in (4.19) involving 6 x 6 matrices can each be replaced by four triple matrix products involving 3 x 3 matrices. In view of the simple form of the matrices Ka,

nrt i 0 .

0

![image 89](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile89.png)

###### THE EQUILIBRIUM METHOD 81

etc., the labour involved in forming these triple products is not nearly as much as it would be if the matrices Ktj and T were all general 6 x 6 matrices.

###### 4.5. The Analysis of Plane Grillages

One special case of the general three-dimensional space frame with rigid joints is the plane frame loaded in its own plane, which we considered in section 4.2. Another important type of structure is the plane grillage. In practice this is often a highly

FIG. 4.10. Member coordinate system for an element of a plane grillage.

redundant structure which it is difficult to analyse by conventional means, and in such cases matrix methods provide a useful way of obtaining a solution. The analysis presented here follows that given by Lightfoot (Lightfoot and Sawko, 1959).

In this analysis we consider a plane horizontal grillage composed of straight uniform beams rigidly joined together at their ends, loaded by vertical forces acting at the joints. As in the previous section, we assume the beams to have torsional stiffness but neglect warping effects. The analysis allows the inclusion in the loading of couples about horizontal axes, but there are

![image 90](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile90.png)

###### 82 MATRIX METHODS OF STRUCTURAL ANALYSIS

assumed to be no applied forces in the plane of the grillage, and no moments applied about vertical axes. In view of these restrictions on the loading we may neglect translations of the joints in the horizontal plane, and rotations of the joints about the vertical. Thus at each joint the displacement vector merely consists of the vertical displacement and the rotations about the two horizontal axes.

As usual we consider first of all the equations of a single member, using the coordinate system shown in Fig. 4.10. It will be noted that this is essentially a similar coordinate system to that used in the previous section for a general three-dimensional member, and we may obtain the equations we require simply by dropping the appropriate terms from the equations (4.17) given in that section. The relevant equations are

0 12EI/Û

'GJIL

0 1 6EI/Û

0 0

^ 1

###### 4EI/L J

6EI/L2 0

[Ai.

\0x2'

###### +

0 "1 6£J/L2

'-GJIL

0 0

- -Î2EIIÛ
- -6EI/L2 0
- -12EIIL3 6EIIL2

0 12£//L3

- -6EIJL2


^3-2

###### k2.

###### 2EI/L J

(4.20)

-GJIL

0 1

=

- [0*1
- [0*2 k-2


- -6£//L2 2EI/L J

0 ]

- -6£//L2 4£//L J


0 0

\Py2

+

'GJjL 0 0

/

###### k2_

where the order of the variables has been altered to make the form of the K matrices as similar as possible to those obtained in section 4.2 for a member of a plane rigid-jointed frame. These equations may be written in the usual form (3.1).

The relation between the member coordinates and the system coordinates is shown in Fig. 4.11. The axes x and z are assumed

![image 91](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile91.png)

###### THE EQUILIBRIUM METHOD 83

to remain in the horizontal plane x'z\ so that the y and y' axes are coincident. From Fig. 4.11 we have

- 0
- 1 0


###### Tm,

»»*"

= "cos a 0

— sin a"|

0

V'y

\Py

sin a

cos al

###### mi

###### [m,

which we write in the normal way as p' = Tp. Transforming equations (4.20) into system coordinates we obtain the member

FIG. 4.11. Member and system coordinates for an element of a plane grillage.

stiffness matrices K'ip which are defined formally by equation

- (4.19). The reader may easily verify that


- K\ ! = \C2 GJ/'L + S2 4EI/L - SÔEI/L2 SC{GJjL - 4E//L)


-S6EIIÛ 12EI/L3 C6EI/L2

[SC(GJIL - 4EI/L) C6EI/L2 S2 GJjL + C2 4£//Lj where S = sin a, C = cos a. The other K' matrices are similar. The process of assembling the stiffness matrix of a complete grillage follows the pattern described in section 4.3.

###### 4.6. The Analysis of Pin-Jointed Space Trusses

As a final example we consider the determination of the K' matrices for a member of a pin-jointed space truss. The force in such a member is dependent only on the axial components of its

###### LD

![image 92](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile92.png)

###### 84 MATRIX METHODS OF STRUCTURAL ANALYSIS

end-translations, so that the member coordinate system only needs to be one-dimensional. Thus the equations relating the end-loads and end-displacements in member coordinates are identical with equations (4.2), which were derived for a pinjointed member of a plane truss. It is only necessary to transform these equations into the appropriate system coordinates.

In system coordinates a load vector p' will have three components p'x, p'y, p'z. In the case of a member whose direction cosines with respect to the x\ y\ z' axes are /, w, n, the axial force p has components

Px = lp p'y = mp P'z = np

which may be written in the usual way as p' = 7>, where Γ =

It follows that the corresponding displacement relationship is d = Vd\ and that equations (4.2) transform into

P\ =- K'd[ -K'd'2 p'2 = —K'd'i -f Krd'2

where

TKV=(EA/L) Ί2 lm ml m2 nl nm

In mn n2

K

4.7. Pin-Joints in Rigid-Jointed Structures

So far we have assumed that the joints of a structure are all pinned or all rigid. We now consider the case where an otherwise

![image 93](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile93.png)

###### THE EQUILIBRIUM METHOD 85

rigid-jointed frame has pin-joints in certain places. The technique which we shall develop is one which can easily be incorporated in a general computer program for analysing rigid-jointed structures, without upsetting the overall arrangement of the calculation. We shall describe it in the form which it takes when applied to plane structures—the ideas may easily be generalized to space frames.

FIG. 4.12. Two rigid joints connected by a pin.

We shall see in section 5.7 that when a single member is pinned to an otherwise rigid joint it is possible to treat the connection as rigid by using modified member stiffness matrices. This is a generalization of the modified stiffness factor used in moment distribution when a member has a pin-joint at one end. However, this technique can only be used for single members—it is not adaptable to the case where several members have their ends rigidly joined together and the rigid joint is then pin-connected either to another rigid joint or to a foundation.

A systematic technique which deals with this problem is the following. Let the two joints which are connected together be denoted by R and S, as shown in Fig. 4.12. We first of all set up

![image 94](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile94.png)

###### 86 MATRIX METHODS OF STRUCTURAL ANALYSIS

the stiffness matrix K of the complete structure as though the two joints were quite distinct. This is legitimate provided that we include the unknown forces qx and qy shown in Fig. 4.12b in the vector of external loads. The relevant part of the load-displacement equations of the structure is thus

###### =

row 3R

PxR + <lx PyR + <ly

uxR ÖyR

3 R + 1 3Λ + 2

- * * ÇLK)RR 0 * *
- * * 0 (ZK)SS * *


###### mR

OR

row 35

"Qx

3 5 + 1 35 + 2

-«,

uyS

###### ms

Os

Here the association of the external forces with joint R rather than joint 5 is quite arbitrary, but the external moments must be assigned to the joints on which they act. The expression (ΣΚ) indicates the sum of the direct stiffness matrices (i.e. Κ[χ or Kf22) at a joint, and the asterisks indicate other coefficients in the equations (due to the members which connect R and 5 to other joints). The two null matrices appear because there is no member connecting R to 5.

We now eliminate the unknown forces qx and qy from equations 3R and 3R + 1 by adding equations 35 and 35 + 1 respectively to them, and introduce the displacement compatibility conditions ôxR = ôxS, ôyR = ôyS by replacing equations 35 and 35 + 1 by the equations

0 = -oxR + ôxS 0 = -ôyR + ôyS

respectively. The equations may now be solved in the usual way. In the subsequent calculation of member end-loads the normal K' matrices of the members should be used.

The only defects of this technique are that it is somewhat wasteful of computer storage space and that it makes the matrix

![image 95](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile95.png)

###### THE EQUILIBRIUM METHOD 87

K unsymrnetric. The waste of storage is usually not importantfrom the programming point of view the elimination of the unnecessary rows and columns of K would be an awkward operation, involving re-packing most of the matrix. The lack of symmetry can easily be removed by transferring appropriate coefficients from columns 35 and 3 5 + 1 to columns 3R and 3R + 1. (Since elements in columns 35 and 3 5 + 1 multiply ôxS and ôyS, which by hypothesis are equal to SxR and SyR respectively, it does not matter which columns these elements appear in.) The only elements which must be left in the columns 35 and 35 + 1 are the l's on the leading diagonal—this is merely to allow the equation-solving routine of the computer to function without being upset by encountering a complete row of zeros.

If a joint is pinned to a rigid foundation the process is somewhat simpler. If, for example, we have the conditions SxS =

SyS = 0, we merely construct the complete matrix K as though 5 were an ordinary joint, and then alter rows 35 and 35 + 1 to give

the required solution. This is done simply by inserting Fs in the leading diagonal positions of K corresponding to these variables, and replacing all other coefficients in the rows by zeros. The appropriate components in the external load vector are also made equal to zero, and if symmetry is to be retained then columns 35 and 3 5 + 1 should also be replaced by zeros, except for the l's on the leading diagonal.

The same technique may be used in the case of sliding joints, and supports mounted on rollers. One merely alters the equations associated with the appropriate degrees of freedom. Somewhat similar methods may be employed in cases where it is possible to reduce the number of displacement variables appearing in an analysis by making use of symmetry.

###### 4.8. Temperature Stresses and Lack of Fit

So far we have assumed that all the members of a structure are unstressed before the application of the external loads. If

![image 96](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile96.png)

###### 88 MATRIX METHODS OF STRUCTURAL ANALYSIS

a structure is hyperstatic, however, there will almost certainly be stresses in the structure before it is loaded, due to lack of fit of members during erection.

The calculation of erection stresses is usually merely an academic exercise, since it is generally impracticable to measure errors in lengths, etc. during erection. These stresses are essentially self-equilibrating, and in a ductile structure they do not affect the collapse load appreciably, since they are "ironed out" by plastic deformation. It is reasonable, therefore, to carry out the elastic analysis of structures as though they are initially unstressed, bearing in mind that what is really computed is the change in stress produced by the application of the external loads.

Temperature changes may also produce stresses in a hyperstatic structure, and since (in contrast to erection errors) the changes of length, etc. produced by temperature can be calculated with reasonable accuracy, it is sensible to attempt to calculate the stresses which are induced. These stresses may be due to different members of the structure being formed from different materials, or they may be due to the existence of temperature gradients within the structure.

Both lack of fit and temperature effects may be dealt with in very much the same way. For example, if we consider the case of a straight uniform member whose temperature rises by an amount /, the unstressed length of the member will increase by an amount ocLt, where a is the coefficient of linear expansion of the material. If the ends of the member are prevented from displacing then this will require the application of an axial compressive force AEoct. Such forces may be included in the load-displacement equations of any member by writing the equations in the more general form

ρι = Κ1ίαι + Κί2ά2^ρη)

(4.21) p2 = K2ldl + K22d2 + pt2)

where ptU pt2 are vectors representing the end-loads on the member when end-displacements are prevented. In our simple

![image 97](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile97.png)

###### IHK EQUILIBRIUM METHOD 89

example the components (px)ti and (px)t2 are equal to AEoct and —AEoct respectively and all the other components are zero. In

other cases the vectors ptl, pt2 may be more complex—a transverse temperature gradient, for example, would give rise to nonzero bending moment components.

Equations (4.21) may be used in the assembly of the loaddisplacement equations of a structure in the normal way. Transformed into system coordinates they appear as

Pi = K\\à\ + K'l2<*2 + P'tl

Pi = #21^1 + #22<*2 + Ptl

where p'tl = Tpn, etc. If we consider the case of an unloaded structure and substitute these expressions for the member endloads into the joint equilibrium equations we obtain a system of equations 0 = Kd + p„ where K is the normal stiffness matrix of the structure and p, is the vector formed from all the individual vectors p'n, p'tl associated with the members. After these equations have been solved for the joint displacements the internal forces and moments in the structure may be found from equations

- (4.21).


4.9. Dynamic Problems

So far we have considered the behaviour of structures under known static loading. There are many instances, however, where the response of a structure to time-dependent forces is required. For example, in designing a structure to resist earthquake or blast loading it is important to know the behaviour of the structure under transient loading conditions, while in the case of a structure supporting rotating machinery the natural frequencies of vibration of the structure are obviously of considerable importance. Problems of dynamic loading are particularly common in the field of aeronautics, and it is the complexity of these problems which has been largely responsible for the widespread adoption of matrix methods in the analysis of aircraft structures.

![image 98](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile98.png)

90 MATRIX METHODS OF STRUCTURAL ANALYSIS

In many problems of structural vibration it is permissible to replace the continuous mass distribution of the real structure by an "equivalent" set of concentrated masses and inertias situated at the joints. This transformation necessarily introduces errors into the computed response of the structure, but these errors are usually small—at least as far as the lower modes of vibration are concerned. If this transformation is carried out then what we have so far referred to as the "equilibrium method" can be used to obtain the general equations of motion of the structure under any type of time-dependent loading.

If a structure has displacements d under a set of static loads p the methods outlined in this chapter provide a systematic means of setting up the equilibrium equations p = Kd. If now the loading vector p is a function of time and the mass of the structure can be treated as a series of masses and rotational inertias concentrated at the joints then these equilibrium equations are replaced by the equations of motion

###### p(0 - Kd = Md (4.22)

where the matrix M is a diagonal matrix whose elements are the massesand inertias associated with the various degrees of freedom.!

In general equation (4.22) represents a set of linear differential equations, and if a computer is available these can easily be integrated numerically from known initial conditions. A common case is the one in which there are no external applied loads and the natural frequencies and normal modes of oscillation are required. If we write p(/) = 0 and d = d0 sin cot equation

- (4.22) becomes Kd0 = a>2Md0 (4.23)


t A more exact equivalence to the distributed mass of a structure may be obtained by using a mass matrix M which is not purely diagonal. This matrix is built up from the mass matrices of the individual structural elements in the same way as the stiffness matrix K. The technique was developed by Archer (Archer, 1963) and independently by Leckie and Lindberg (Leckie and Lindberg, 1963). For further details the reader is referred to these papers and to the book by Przemieniecki (Przemieniecki, 1968), chapter 11.

![image 99](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile99.png)

###### THE EQUILIBRIUM METHOD 91

and putting λ = ω2 gives the general eigenvalue problem discussed in section 2.5. It should be noted here that in general it is advisable to make the matrix M non-singular by associating a non-zero mass or inertia with each degree of freedom. A joint without mass gives rise to an infinite natural frequency, and although this is not physically significant it may lead to computational trouble with certain types of numerical method.

If it is only required to find the lowest natural frequency of a

system (4.23) may be written in the form (M — λΚ)ά0 = 0, where λ = l/ω2, and this may be transformed into (A — λ\)χ = 0

by the method outlined in section 2.5, provided that K is positive definite. The smallest value of ω now corresponds to the largest value of A, and may be found by the iterative method described in that section. In most structural problems the frequency of the first harmonic is considerably greater than the frequency of the fundamental mode, so that the iterative process usually converges with satisfactory rapidity. Alternatively Rayleigh's principle may be used—it is often convenient to use the deflected form of the structure under suitable static loading as the approximate mode of vibration.

While the use of stiffness matrices makes it easy to formulate a structural vibration problem in classical eigenvalue terms the heavily banded nature of the K and M matrices may make it practicable to find the solutions of equation (4.23) by actually evaluating the determinant |K — Μω2| numerically for a series of values of ω, and finding the zeros by a standard root-finding process. This approach is particularly useful if it is required to investigate the vibration characteristics of a structure in a given frequency range. It is often applied in conjunction with the use of transfer matrices and is discussed further in section 8.6.

![image 100](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile100.png)

###### CHAPTER 5

###### Stiffness, Flexibility and Equilibrium Matrices for Single Members

IN describing the general features of the equilibrium method in the previous chapter it was natural to choose examples involving relatively simple structural elements. By restricting the analysis to structures formed from straight uniform members it was possible to obtain the coefficients of the member stiffness matrices direct from the known solutions of the differential equations of bending, torsion, etc., without actually having to consider the differential equations themselves. We now consider the problem of finding member stiffness matrices in the more general case, where the member may be both curved and non-uniform in cross-section.

In discussing the equilibrium method we wrote the loaddisplacement equations for a single member in the form

Pi =Klldi + K12d2

(5.1)

Pi = #2i<*i + K22d2

and referred to the matrices K1U etc., as the "stiffness matrices" of the member. Although this is the form most suited to the equilibrium method it is not the only way in which the relationships between end-forces and end-displacements may be written, and it is not in fact the form in which they are most conveniently derived. In the present chapter we develop an alternative

92

![image 101](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile101.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 93

formulation of the equations in terms of the deformation vector e introduced in section 3.3.

This formulation has two advantages. In the first place it provides a convenient way of obtaining the member stiffness matrices used in the equilibrium approach, and we shall see that the four matrices Kn, K12, etc. can all be derived from a single flexibility matrix F and an equilibrium matrix H. The latter matrix is of very simple form and is independent of the elastic properties of the member. In the second place it forms a natural starting point for the development of the compatibility approach described in chapter 7 and the method of transfer matrices described in chapter 8.

5.1. Equilibrium Equations and Rigid-Body Displacements

The reader will recall that it was stated in section 3.3 that load-displacement equations such as (5.1) are inevitably singular, since an isolated member may be given an arbitrary small rigidbody displacement without affecting the forces and moments applied to its ends. (The rigid-body movement is required to be small merely because all our analysis is subject to the restrictions of linear small-displacement theory.) Alternatively we may say that equations (5.1) are singular because the displacements du d2 may be specified arbitrarily (provided they are small) while the end-loads pl9 p2 may not, since the latter quantities must always satisfy equations of member equilibrium. In fact only one of the two equations (5.1) is really necessary for the purpose of obtaining the end-loads associated with a particular pair of end-displacements, since one end-load can always be found in terms of the other from statical considerations alone.

We now introduce the concept of an equilibrium matrix. The equilibrium equations connecting pt and p2 may be written in matrix formas ργ + Ηί2ρ2 = 0> or alternatively as H2ip1 + p2 = 0, where H2i = //Γ21· For the sake of simplicity in notation we

![image 102](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile102.png)

shall write Hl2 merely as H, and denote H2i by H *, so that the equations become

(5.2a) (5.2b)

Pi +Hp2 = 0 Hipi + p2 = 0

We call H the equilibrium matrix associated with the member. There is a certain arbitrariness here in that H is associated with

FIG. 5.1. End-loads for a general member in space.

p2 rather than pu but the lack of symmetry has few practical disadvantages. In practice it is quite natural to think of the load

on a member as being specified by Pi, the quantity px being regarded merely as a support reaction whose value is determined by equation (5.2a).

As we are still only concerned with the linear small-deflexion theory of structures we shall continue the practice adopted in the previous chapter and write all equations of equilibrium in the

![image 103](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile103.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 95

form which they would take in the undistorted structure. By doing this we make H independent of the elastic properties of the member, and merely a function of the relative positions of its ends in space. The coefficients of H depend, of course, on the particular coordinate system used to express the components of the loads pt and p2- We shall continue to follow the convention introduced in chapter 3, attaching primes to vectors and matrices whose components are referred to system coordinates.

When we considered the derivation of stiffness matrices in chapter 4 our practice was to derive these first in member coordinates and then to change to general system coordinates afterwards. We could follow the same procedure here, but in fact it is quite easy to write down the coefficients of a general equilibrium matrix in system coordinates. If we consider a general three-dimensional member in which end 2 has coordinates Lx, Lr Lz with respect to end 1, as shown in Fig. 5.1, the equations of equilibrium for the member are

Pxi + Px2 = 0 < i + < 2 + Lyp'z2 - Lzp'y2 = 0 P'yi + Pyz = 0 m'yl + m'y2 + Lzp'xl - Lxpz2 = 0 Pzi + Pz2 = 0 m'zi + mz2 + Lxp'y2 - Lypx2 = 0

which may be written ΓΡχΐ"

+ " 1 0 0 0 Lz

0 0 0 0

0

0 0 0 1 0 0

0 0 0

- 0
- 1 0


= 0 (5.3)

Pxl P'yl P'Z2

- 0
- 1 Ly


Pyi Pzl m'xi

- 0
- 1 0


###### -K

- ™'x2
- ™'y2


- 0
- 1


0 Lx

m'yi

-Lx 0

###### L-L,

L<i.

L < 2 J

Equation (5.3) defines the matrix W in the most general case, the primes being attached because the axes we have chosen resemble system coordinates rather than member coordinates. If coordinates are chosen in which the axis of x coincides with the line

![image 104](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile104.png)

joining the two ends of the member, then the corresponding equations are

0 (5.4)

0 0 0

0" 0 0 0 0 I_

+ 01 0 0

0 0 1 0

0 0 0 1 0 0

~Px2~\ Py2 Pzl

Pxl Pyl Pzl

- 0
- 1 0


###### ™x2

mxl myi

0 -L L 0

my2

.^ι2\

where L is the distance between the ends of the member. If the loads and the member lie entirely in the x'y' plane then equations

- (5.3) and (5.4) reduce to


- = 0 (5.5)
- = 0 (5.6)


0 1 Lx

(Γ 0 1_

###### +

" 1 0

Px2

Pxl

P'yl

\Py2

m\.

_m'2

--L,

and

###### +

- 0
- 1 L


0" 0 1_

' 1 0 0

Pxl Pyl

Pxl Pyl

_m2 respectively.

« 1 .

These equations are useful in finding the load transmitted to a joint by a member which carries a load at its far end. Thus if a load p2 acts at end 2 of a member then the load transmitted to the joint atend 1 is —puand this is equal to Hp2 from equation (5.2a). Similarly if a load pl acts at end 1 then the load transmitted to the joint at end 2 is H~1pl. Although it is straightforward to find the inverse of an H matrix by direct application of the rules for matrix inversion, it is simpler to obtain the result by returning to Fig. 5.1. If we interchange ends 1 and 2 in that figure the only difference is that the coordinates of end 2 relative to end 1 reverse their signs. It follows that the inverse of an H or H' matrix is obtained merely

![image 105](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile105.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 97

by reversing the signs of the off-diagonal elements—a result which the reader may easily verify algebraically.

Although the matrix H has been derived entirely from equilibrium considerations, it has another important function in relating the end-displacements of a member during a rigid-body movement. Once again we follow the reasoning of section 3.4. We imagine a virtual rigid-body movement of a member, during which it is acted on by end-loads pu p2, these end-loads being constant and

FIG. 5.2. Member formed from two elements joined together.

satisfying the equilibrium condition (5.2). We denote the rigidbody end-displacements by d*, d%. Since the member is in equilibrium throughout the movement the total work done by the applied forces must be zero, so that p[d* + p2d* = 0. Substituting for pt from equation (5.2) we obtain —p^H'df + p2d* = 0, and since p2 may be chosen arbitrarily it follows that we must have

d\ = Hfd* (5.7)

###### 5.2. Products of Equilibrium Matrices

Consider now the case of a member c formed from members a and b, end 2 of member a being rigidly attached to end 1 of member b, as shown in Fig. 5.2. The equilibrium equations for the

![image 106](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile106.png)

98 MATRIX METHODS OF STRUCTURAL ANALYSIS

two individual components of c may be written P\a + H'oP'2a = 0\ P'ib + H'bp'2b = OJ

(5.8)

where the matrices H'a, Hb are defined by equations similar to (5.3). For equilibrium at the junction of the two components we have

Pia + P\b = ° (5.9)

(System coordinates must be used in equations (5.8) and (5.9) since the individual member coordinate axes may not be the same.) Combining these equations we obtain p\a + H'aH'bp'2b = 0, which may be written as p'lc + H'cp'2c = 0, where H'c, the equilibrium matrix for the complete member, is equal to H'aH'b. This result may be checked by direct multiplication. It is easy to verify that

0 0

01 0 0

0 0 0

0 0 1

1 0 0 0

- 0
- 1 0 Lz, 0


0 0 1 Lya

1 0 0

- 0 0 0

- 0 0 0

- 0 0 0
- 1 0 0


- 0 1 0


- 0 0 1


- 0
- 1 0


- 0
- 1 0 0


###### °l

- 0
- 1 0


###### o -u

0

-Lxa 0

~Lxb 0

###### K

'zb

lj 1

-Lv.

■Lyb

xb

1 0 0

0

- 0
- 1 0


- 0 0 0

- 0 0 0

- 0 0 0
- 1 0 0


- 0 1 0


- 0 0 1


- 0
- 1


###### o ,

— L,a — Lzb 0

Lya + Lv

'yb

Lia + Lz ~Lya — Lyb

~~ Lxa — Lxh 0

![image 107](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile107.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 99

as we should expect by a direct consideration of the equilibrium of the complete member c. This result may be generalized to the case of any number of members connected end-to-end. Thus if we have a composite member formed from sections a, b, ..., n the equilibrium equations connecting the end-loads p[, p'2 are p\ + (H'aH'b H'n)pf2 = 0. Similarly if the member undergoes a

rigid-body movement the end-displacements d*', d*f are related by the equation A%' = {HaHb Hffd?.

5.3. Flexibility and Stiffness Matrices for a Gênerai Linear Member

We now develop the idea of a deformation vector introduced in section 3.3. We think of the end-displacements du d2 of a structural element as the sum of two separate sets of displacements, one due to the elastic strains and the other due to rigidbody movement. We deduce expressions for the general loaddisplacement characteristics of a linear element by considering the two sets of displacements separately and then combining the results.

We consider the general member shown in Fig. 5.3, and deal first with the case where end 1 of the member is completely restrained against displacement. The displacement at end 2 due to the load p2 under these conditions is equal to the deformation e, the load and deformation vectors being measured in member coordinates. One way of determining e is to use strain energy. It is simply a matter of statics to express the moment and force components at any point P of the member in terms of the coordinate s and the components of p2- (Note that these equations will also involve the linearizing approximation discussed in the derivation of the matrix H since they will normally be based on the geometry of the undistorted member.) By integrating along the member the strain energy may be expressed in terms of these components, and since the member is assumed to behave in a linear manner we may apply Castigliano's theorem, Part II,

![image 108](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile108.png)

###### 100 MATRIX METHODS OF STRUCTURAL ANALYSIS

differentiating tne strain energy U with respect to each component of p2 in turn. If the member is a general member of a space structure this gives the six components of e in the form

###### δχ2 - duidPx2 sy2 » du/dPy2 δζ2 - du/dpz2

θχ2 = dUldmx2 0y2 = dU/dmy2 θζ2 = dU/dmz2

(b)

FIG. 5.3. General member with (a) end 1 rigidly fixed and load P2 applied to end 2. (b) rigid-body displacement under constant end-loads.

These differential coefficients will be linear functions of the components of p2, so that we may write the expressions for the displacement components in the form

e = Fp2 (5.10)

We shall call F the flexibility matrix of the member. We may argue on physical grounds that F must be non-singular, since the member is sufficiently restrained to constitute a structure, and

![image 109](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile109.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 101

from the reciprocal theorem F must also be symmetric. We may therefore invert F and write (5.10) in the form

p2 = Ke (5.11)

where K is also symmetric. We shall call K the stiffness matrix of the member. As with the matrix H and the vector e there is a certain lack of symmetry in associating F and K with end 2. It is clear that K is equal to the matrix which we previously defined as K22, and it would be more precise to write F as F22, but the omission of the suffixes makes the analysis somewhat simpler to follow and has few practical disadvantages. We shall see later that the corresponding matrices associated with end 1 can easily be obtained in terms of F and H if required. Equation (5.2) now gives the corresponding load at end 1,

Pi= -Hp2= -HKe (5.12)

We now consider the effect of superposing a rigid-body displacement of the member on the displacements dx = 0, d2 = e. Let these rigid-body displacements be denoted by d\ and d*> where

d*2 = WdX (5.13) from equation (5.7). Adding the two sets of displacements we have

(5.14)

- d2 = d*2 + ej

Eliminating the rigid-body displacements d* and d\ from (5.13) and (5.14) we obtain

- e = d2-Htdl (5.15)


This expression for e provides a measure of the amount of elastic strain associated with any arbitrary end-displacements dl9 d2. If e is zero then dl and d2 satisfy equation (5.13) and correspond to a purely rigid-body displacement.

![image 110](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile110.png)

###### 102 MATRIX METHODS OF STRUCTURAL ANALYSIS

Combining equations (5.10) and (5.15) gives the equation d2 = Htdi + Fp2 (5.16)

which we shall use in chapter 3 when discussing transfer matrices. Substituting the expression for e given in (5.15) into (5.11) and (5.12) gives

###### p^iHKH'^-iHK^] ( 5 1 7)

p2=-{Küt)dl+Kd2 )

Comparing equations (5.17) and (5.1) we obtain the important general expressions for the member stiffness matrices

Κ1 1=ΗΚΗί Κί2=-ΗΚ Κ21=-ΚΗ* Κ22 = Κ (5.18) where K = F"1. Since F and K are symmetric it follows that Kll and K22 are symmetric, and that K21 = K\2. It also follows that if end 2 is prevented from displacing then the flexibility matrix associated with end 1 is

ΚΓι1 = (ΗΚΗ')1 = (H-^FH^

The temperature effects discussed in section 4.8 may easily be included in this analysis. If there is an additional deformation of the member et due to temperature changes (5.11) becomes p2 = K(e — et)y and equations (5.17) become

pY = (HKH')<*i - (HK)d2 + (HK)et p2= -(KHt)dl+Kd2-Ket

Comparing these equations with equations (4.21) in section 4.8 we see that the load vectors pn, pt2 defined in that section are equal to HKet and — Ket respectively.

The reader will notice the similarity between the matrix product HKH* appearing in equation (5.18) and the products of the form ΊΚΊ* which appeared during coordinate transformations in chapter 4. There is, however, an important difference between

t It is easy to show that if A is a non-singular matrix then (A1)"1 = (Α~ιΥ.

![image 111](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile111.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 103

the matrices H and Γ. The matrix T is, in general, an orthogonal matrix, which relates the components of a particular load or displacement vector to the components of the same load or displacement vector when expressed in a different coordinate system. The matrix //, on the other hand, is not normally an orthogonal matrix, and relates the load or displacement vectors at two different points, both vectors being measured in the same coordinate system.

End I End 2

FIG. 5.4. Coordinate system for the analysis of an initially straight member of non-uniform cross-section.

As an example of the application of this analysis we shall consider the derivation of the flexibility and stiffness matrices for a straight non-uniform beam of length L under the action of forces and moments in a plane, as shown in Fig. 5.4. The x axis of the coordinate system is assumed to coincide with the unstrained axis of the beam.

We first consider the displacement d2 of end 2 due to the load p2, the displacement of end 1 being kept equal to zero, as shown in the figure. At the point P the direct force is equal to px2 and the moment is m2 + py2s. (Note that, as usual, the expression for the moment is derived for the undistorted member.) The strain energy U is given by

U = I (p2x2/2EA)ds + I ((m2 + py2s)2/2EI)ds

Jo Jo and the displacement components at end 2 are given by the expressions

![image 112](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile112.png)

104 MATRIX MITHODS OF STRUCTURAL ANALYSIS

###### [Î:

(\IEA)ds\

<5.r2 = dUjdpx2

Px2

x

(s2/EI)ds

(slEI)ds

<\z = dU/dPy2 =

m2

Py2 +

Pyl + I

(\/EI)ds

02 = euidm2

(slEI)ds

nu

Writing J\,f2, fs, f* for the four different integrals appearing in these equations we obtain

5,2 = flPxl àyl = f2Py2 + / > l 2

#2 = /3Py2 + . / > 2

or in matrix form

= ~fi 0 0 ■

Ά 2 "

Px2

0 Λ Λ _o /3 /4_

P>'2

^y2

A _

m2 that is, rf2 = e = *P2·

It will be recalled that in section 2.5 we stated that any symmetric linear relation y = Ax can be transformed, by a suitable choice of axes, into a relationship y' = A'x\ in which A' is a purely diagonal matrix. It follows that in a certain coordinate system the matrix F which we have derived will appear as a diagonal matrix. In the case of a general curved member whose deformation is entirely due to bending, the coordinate axes of this system have a physical interpretation, being the principal axes of inertia of a line distribution of mass whose line density is proportional to I/EL The origin of this coordinate system corresponds to the centre of gravity of the line distribution and is termed the elastic centre.

If the beam is of unifonn cross-section the evaluation of the

![image 113](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile113.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 105

integrals is elementary and the matrix F takes the form ~L\EA 0 0 "

###### 0 ÜßEl ÜßEl 0 ÜßEl L/EI J

The inverse of F may now be computed to give the matrix which we denoted by K in equation (5.11). For the case of a uniform beam we obtain

EA/L 0 0 0 12£//L3 -6EI/L2 0 -6EI/L2 4EI/L

which agrees with the value of K22 given in section 4.2.

In the general case the evaluation of the member stiffness matrices Klu etc. follows from equations (5.18), using the expression for H given in equation (5.6). The reader may easily verify that in the case of a uniform beam these equations give matrices which are identical with those derived in chapter 4.

5.4. Coordinate Transformations of Flexibility and Equilibrium Matrices

In section 5.3 we were concerned with calculating the matrix F in member coordinates. If we wish to find the form taken by F in some other system of coordinates we may employ the same method as we used in chapter 4 when dealing with stiffness matrices. Using primes to denote vectors expressed in system coordinates we may relate end-loads and deformations in the two coordinate systems by the equations

p' = Tp e' ~ Te p = Vp' e = Te'

where in general the matrix T is orthogonal. Using these expressions we may write equation (5.10) in system coordinates,

![image 114](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile114.png)

###### 106 MATRIX METHODS OF STRUCTURAL ANALYSIS

obtaining e = (TFF)p'2, so that the form of the matrix F in system coordinates is given by F' = TFF. Thus the transformation rules for flexibility matrices are identical with those derived for stiffness matrices in chapter 4.

(a) £ t

Jo

777)777 (b)

FIG. 5.5. (a) Springs in parallel, (b) Springs in series.

It is easy to show that H matrices transform in exactly the same way. Multiplying (5.2a) by T and substituting for pt and p2 we obtain p\ + (THT')p'2 = 0, so that we have H' = THF. However, as we saw in section 5.1, it is quite easy to derive the matrix H' by direct means, so that this formal result is not of great practical value.

###### 5.5. Members Formed from Elements Connected in Series

If a number of springs are connected together in parallel, as shown in Fig. 5.5a, then the extensions of all the springs are the same. We accordingly write the load-extension equation of each spring in the form

force = stiffness x extension,

![image 115](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile115.png)

and add up all the individual forces to give total force = sum of stiffnesses x extension.

By working in this way we avoid bringing in the individual spring forces as variables and have only the one equation to solve for the extension. If on the other hand the springs are connected in series, as shown in Fig. 5.5b, the force in each spring is the same. Thus we write for each spring

extension = flexibility x force, and add up all the individual extensions to give

total extension = sum of flexibilities x force.

Here the use of flexibilities rather than stiffnesses enables us to avoid introducing the intermediate displacements at the spring connections as variables.

In an analogous way, the use of stiffness matrices is advantageous when analysing structures which have a large number of members "in parallel", while the use of flexibility matrices enables intermediate displacements to be eliminated when a number of members are connected together "in series". Even when the overall analysis of the structure is to be done by the equilibrium method there may be parts of the structure where several members are connected end-to-end, and in such cases the size of the final stiffness matrix may be considerably reduced by the elimination of intermediate displacements prior to the assembly process.

We shall demonstrate these ideas by considering the analysis of the composite member shown in Fig. 5.6a. This member is assumed to consist of a number of sections whose F matrices are known. The problem is to find the flexibility and stiffness matrices of the complete member in terms of the F's of the components, so that only the displacements of the ends A and X need enter into the subsequent analysis of any frame of which the member may be a part. In the following analysis we shall assume that the

![image 116](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile116.png)

###### 108 MATRIX METHODS OF STRUCTURAL ANALYSIS

H and F matrices of the individual sections are expressed in some overall coordinate system associated with the member AX. If necessary the transformation rules given in section 5.4 may be used to achieve this.

We approach the problem by considering the separate contribution which each section of the member makes to the displacement of end X relative to end A. If we consider the case

End 2

FIG. 5.6. (a) Member composed of a series of elements. (b) Deformation of member associated with strains in section k.

where end A is fixed and a load px is applied to end X, then by definition the displacement at X is given by

άχ = eAX = FAXPX (5.19) This displacement is the sum of the displacements due to the strains in the individual sections. Consider, for example, the displacement at end X due to the deformation of section k. For this purpose we regard the remainder of the member as being merely rigid extensions AJ, KX of section k9 as shown in Fig. 5.6b.

![image 117](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile117.png)

If we consider the part KX of the member, lying between end 2 of section k and X, we may apply equation (5.2) to the loads acting on its ends. Thus the load acting on the end of KX attached to section k is equal to — HKxpx, and the load acting on end 2 of section k is HKXpx. (It follows from the result proved in section 5.2 that HKX is equal to the product of the H matrices of all the sections comprising KX.) Since A is fixed and AJ is considered rigid, end 1 of member k is effectively fixed, and the displacement of its end 2 is given by dK = ek = Fkplh = FkHKXpx. Now KX is a rigid member, and the displacements of its ends therefore satisfy the equation for rigid-body movement (5.7). Thus the displacement of X due to the strain induced in section k by the load px at X is dXk = Ηκχ^κ — ^κχ^^κχΡχ- Thus the flexibility matrix Fk of section k appears as Η*κχΡιΗκχ when viewed from the point X. Similar analysis may be applied to each section of AX, and adding up all the displacement contributions we obtain the complete flexibility matrix of AX in the form

FAX = Σ^χ^κχ (5.20)

where the summation extends over all the sections making up the member AX. Inversion of FAX gives the matrix KAX, and since the matrix HAX may be obtained either from the overall equilibrium of the member or by multiplying together all the H matrices of the sections the other stiffness matrices follow immediately from equations (5.18).

From this analysis we see that the behaviour of a set of structural members differs slightly from the behaviour of a simple onedimensional spring system. For members connected "in parallel" the stiffness matrices are simply added together, in the same way as the stiffnesses of springs in parallel are added together. For members connected "in series", on the other hand, the flexibility matrices have to be modified in accordance with equation (5.20) before they are added together. The following two sections show how the analysis is applied to some practical problems.

![image 118](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile118.png)

1 10 MATRIX METHODS OF STRUCTURAL ANALYSIS

###### 5.6. The Effect of Joints of Finite Size

A simple application of the analysis contained in the previous section occurs when we consider the effect of joint size in a plane rigid-jointed structure. We imagine that the member BC in

- Fig. 5.7 is connected to the joints A and D by rigid gusset plates


End I Endl

FIG. 5.7. Member with end-connections of finite size.

AB and CD. (The points A and D are merely the arbitrary points at which we choose to measure the joint loads and displacements.) We wish to find the stiffness matrices of the composite member AD in terms of the known stiffness matrices of the flexible section BC and the geometry of the rigid end-plates. We assume that the stiffness matrices of the flexible section are known in the member coordinate system shown, this system being such that the x axis lies in the direction BC.

Since BC is the only section of the composite member which has any flexibility, equation (5.20) gives the simple expression FAD = HcDFBCHCD for the flexibility matrix of AD. Inverting

###### this we obtain KAD = H^F^H^)' = U^K^H^)*. This

gives us immediately the matrix K22 of the composite member AD. To find the other stiffness matrices we apply equations (5.18), noting that the H matrix for the complete member is equal to the product of the H matrices for the three individual sections. Thus we have

![image 119](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile119.png)

STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 111 (KU)AD = HADKADHAD (5.21)

= HABH BCHCDHCDK BC{HCD) HCDHBCHAB

= HABH BCKBCHBCHAB

= HAB(Kll)BCHAB

(KII)AD = (K 21) AD = —HADKAD (5.22)

= ~HABHBCHCDHCDKBC(HCD)

— ^HABHBCKBC(HCD)

= HA B(KI I)BC(HCD )

(^22)AD = KAD = HcD(K22)Bc(HcDy (5.23) Equations (5.21) to (5.23) give the stiffness matrices of the composite member in terms of the corresponding stiffness matrices of the section BC. These equations are of course quite general, and hold whether the member is part of a space or plane structure. In the case of a plane structure, where the coordinates of B relative to A and D relative to C are (xl9 yj and (x2, y2) respectively, as shown in Fig. 5.7, we have

1 0 01 0 1 0 y2 -*2 iJ

- 0
- 1


0

HAB = Γ 1

HCD —

- 0
- 1_


0

L-.Fi

*1

from equation (5.5). As mentioned earlier, the inverse of an H matrix is obtained merely by reversing the signs of the off-diagonal elements. It should be noted that the stiffness matrices for the member AD given by equations (5.21) to (5.23) are still in the member coordinate system associated with the flexible section BC.

###### 5.7. Semi-Rigid Joint Connections

We have so far assumed, both in chapter 4 and in the previous section, that the displacement vectors at the ends of any member

![image 120](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile120.png)

###### 112 MATRIX METHODS OF STRUCTURAL ANALYSIS

are always equal to the displacement vectors associated with the joints to which the member is attached. We now consider the case where a member is attached to the joints at its ends by flexible connections, each of which transmits a moment proportional to the difference between the rotation of the end of the member and the rotation of the joint to which it is attached. Such joints occur in bolted frames, and in welded frames after the onset of plasticity. It is true that in both these cases the moment-rotation

FIG. 5.8. Flexibility of a semi-rigid joint connection. (Note: the load * is applied to end 2 of the connection).

relation is unlikely to be linear, but we shall show in chapter 10 that such problems may be solved by iterative means, the structure being treated as a linear system during each iteration. As in the previous section, our aim is to find the stiffness matrices of the complete system of member plus connections, so that in a subsequent equilibrium analysis we need not consider the rotation which occurs on the member side of each connection.

We consider a straight uniform member of a plane frame, of length L and flexural rigidity El, whose ends 1 and 2 are attached to the rest of the frame by connections which exert moments 4EIk1/L and 4EIk2/L respectively per unit difference in rotation. We ignore the length of each connection, so that although the rotations may differ the translations of the ends of the member are the same as those of the corresponding joints. If now we imagine the joint at end 1 of the member to be prevented from

![image 121](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile121.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 113

displacing, the displacement vector on the member side of the connection is given by the equation

###### P*l

0 0 "1 0 0

###### r[m*\

LöT*

0 L/4£/fcJ

where the starred forces and moment are shown in Fig. 5.8. Thus the flexibility matrix of the connection is

0 0 0 0

0 0 0

0 L/4£//cj

In the same way the flexibility matrix of the connection at end 2 of the member is

0 0 0 0 0 L/4EIk2

0 0 0

The flexibility matrix of the member itself is given in section 5.3, and is

Fm = \L\EA 0 0 0 ÜßEI Ü/2EI 0 ÜjlEI LjEI

We may now find the flexibility matrix of the member plus the connections by applying the analysis given in section 5.5. Assuming that the lengths of the connections are negligible we have from equation (5.20) F = iffFclH + Fm + Fc2, where H is the equilibrium matrix of the member. The first term on the right-hand side of this equation represents the flexibility

![image 122](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile122.png)

###### 114 MATRIX METHODS OF STRUCTURAL ANALYSIS

of the connection at end 1 as viewed from end 2. Written out in full it is

0 0 0 0 0 0

"1 0 01 0 1 0

0 0 0

0] 1 L

Γ1 0

Lo

lj |

_0 L lj

.0 0 L/4£/fcJ

"0 0 0 '

0 L3/4£/fc! L2/4£/fc! _0 L2/4£/A'! L/4£ifei

Adding the other flexibility matrices we obtain F =

###### n °

0

L3/l 1 \

L2 /l 1 \ £/\2 + 4fc1/ L / 1 1 \ £/\ +4k1"+ 4/c2/_

###### El \3+ 4kJ

L2/l 1 \

###### EI\2+ 4kJ

7 we obtain

Inverting i

K = ](■>■, =

0

###### T

12£/4fc1fc2 + /c1 L3 2k

+ fc2 6£7 k2 + 2fcifc2

###### "IF it

6EIk2 + 2ktk2 4£/3/c2 + 4kik2 2k

where A: = 2(1 + £0(1 + &2) - \. It will be noted that this expression reduces to the known form for K when both &t and k2 are infinite. The other stiffness matrices now follow from equations (5.18)

![image 123](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile123.png)

###### STIFFNESS, FLEXIBILITY AND EQUILIBRIUM MATRICES 115

Kn = HKiV = YEA L

12EI 4ktk2 + k1+k2 6EI kx + 2k2kx Ί} 2k

0

L2 k AEl^+Aktki

6EIkt +2k2k!

0

2k

A i2 = **21 = —HK

-EA L

12EI 4ktk2 + kt + k2 6EIk2 + 2ktk2 Ü 2k

0

L2 k 2EI 2kxk2

6EI fcj + 2fc2fct

0

An interesting special case of these results occurs when one k value is equal to zero and the other is equal to infinity. This corresponds to the case of a member with a pin joint at one end and a rigid joint at the other. The two cases are :

(a) kx = 0, k2 = oo. (Pin joint at end 1, rigid joint at end 2.)

EA\L 0 0"

0 3EI/Ü 0 0 0 0

-EAjL 0 0 -3E//L3 0 0

0 Ί 3EI/L2

###### K{2 — #21 —

###### o J

EAjL 0

0 1

K22

-3EJIL2 3EI/L J

0 3EI/Û 0 -3EI/L2

LE

![image 124](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile124.png)

###### 116 MATRIX METHODS OF STRUCTURAL ANALYSIS

(b) k1 = oo, k2 = 0. (Rigid joint at end 1, pin joint at end 2.)

* H = EA/L 0 0 0 3EI/L3 3EI/L2 0 3£//L2 3£//Lj

0 0 -3EI/L3 0 -3EI/L2 0

1 — -EA/L

0 0

0 0] 3E//L3 0

^22 = 'EA/L

0 0

###### o oj

The reader may notice that the last term of the matrix K22 in case (a), (or Xu in case (b)), has been reduced from 4EI/L to 3EI/L by the presence of the pin joint. This corresponds to the modification of rotational stiffness normally made in the moment distribution process when a member has a pin joint at one end. Finally it may be noted that if kx and k2 are both zero then all the flexural terms in the stiffness matrices become zero, which corresponds to the fact that a member which is pinned at both ends may be treated simply as a member of zero flexural rigidity rigidly attached to the joints at its ends.

![image 125](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile125.png)

###### CHAPTER 6

###### Connection Matrices and Determinate Systems

ONE of the most noticeable features of the equilibrium method of analysis described in chapter 4 is the way in which it completely ignores the question of whether the structure being analysed is statically determinate or not. In one sense this is an advantage, since it means that the method can be applied to many different types of structure, but it also implies that the method is inefficient when it is used to analyse determinate structures, or structures with only a few redundancies.

The analysis of determinate structures is important for two reasons. The most obvious one is that a great many engineering structures are in fact determinate, or at least are analysed as such during design. Although the analysis of a determinate structure is usually regarded as elementary from a theoretical point of view, the practical problem of stressing a complicated threedimensional structure with several hundred members can hardly be called trivial, even when the members are arranged in such a way as to make the system determinate. For such problems it is worth developing systematic techniques which can be programmed for a computer. The second reason is that the analysis of a hyperstatic structure by the compatibility method involves the consideration of an auxiliary statically determinate structure, so that the techniques which we shall discuss in the later sections of this chapter are an essential preliminary to the account of the compatibility method given in chapter 7.

In the first part of this chapter we consider the equilibrium

117

![image 126](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile126.png)

###### 118 MATRIX METHODS OF STRUCTURAL ANALYSIS

method of analysis from a slightly different standpoint, introducing the concept of connection matrices. Although this formulation of the method is not often used in solving problems it is of considerable theoretical interest, since it provides a link between the equilibrium method and the much simpler methods which are available for dealing with determinate systems. In the second part of the chapter we consider systematic methods for analysing determinate structures.

Matrix notation makes it very easy to discuss techniques of analysis in a way which is precise yet applicable to a wide range of structures. In this chapter we shall regard a "structure" simply as a set of members connected together in a specified way and acted on by known loads applied at the joints. We shall imagine that for each member the F and H matrices are known in member coordinates, together with the matrix T which defines the orientation of the member with respect to the system coordinate axes. We shall not in general concern ourselves with the detailed characteristics of these matrices—we merely imagine that they have been determined by the methods described in the previous chapters. Thus our analysis will apply equally well to plane and space structures—we merely assume that the various vectors and matrices are defined appropriately.

6.1. Formulation of the Equilibrium Method Using Connection Matrices

In discussing the assembly of the complete stiffness matrix of a structure in section 4.3 we were in fact concerned merely with the topological properties of a set of lines drawn on a sheet of paper. The fact that these lines represented the members of a structure was in one sense irrelevant: we could have adopted exactly the same procedure in analysing an electric network, displacements being replaced by voltages and loads by currents. The equilibrium approach to structural analysis, in which displacements are considered as the basic unknowns, is in fact

![image 127](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile127.png)

directly analogous to the nodal method of analysing electric networks, in which the basic unknowns are considered to be the node voltages. It is therefore worth investigating the methods which have been developed for the analysis of electric networks to see if they contain anything of value to the structural analyst.

One concept which was originally developed in an electrical context but which has direct application to structural theory is the connection matrix. We shall illustrate this idea by considering the analysis of the rigid-jointed frame shown in Fig. 6.1. This

FIG. 6.1. Example of a rigid-jointed structure.

frame may be a plane frame or a space frame—as mentioned earlier, our analysis will hold for either, provided that the various vectors and matrices are suitably defined.

By applying the rules laid down in section 4.3 we can immediately write down the load-displacement equations for this structure in the form

PA] = \(Kf22)a + (K'22)b + (tf'n), (K[2)d ψΑ1 (6.1) PB\ [ (K2i)d (K22)c + (K'22)d\[dB\

The direct construction of these equations is a straightforward matter, but the equations may also be derived by a rather different approach which we now describe.

We first of all write down the load-displacement equations of the individual elements of the structure in system coordinates, arranging them as a large banded matrix in the form

![image 128](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile128.png)

=

0 0 0 0

(JTi2)« 0 0 (K'22)a 0 0

###### Γρ'ΐα

###### d'\a~\

(AT'll)a

- d\a d'lb
- d\b


p'la p'lb p\b

(Ä"'2l)u

0 0

0 (Ä"ll)* (K'l2)b 0 0 (JT'2i)* (K'2z)b 0

0 0

d\d

0 (K'u)d (K'i2)a 0 (K'2l)d (K'22)d_

p'ld

_d'2d J

|_/?'2ci_

write as

vhich

we

Pm = Kmdin (6.2) the suffix m standing for "members". Although equation (6.2) resembles equation (3.2) it is not of course a description of the behaviour of the structure. It merely describes the elastic properties of the separate components when they are correctly oriented with respect to the system axes but not connected to the joints. It may be noted that the matrix K'm is singular, since there is, as yet, nothing to prevent the individual members being given rigid-body displacements.

We now describe in mathematical terms the process of connecting up the components, in a manner very similar to that used in section 3.4. First of all we note that the member end-loads which make up the vector p'm in equation (6.2) must satisfy the equations of equilibrium

PA = Pia + P'ib + P\d PB = Pic + P'ld

which we may write in the form

0 / 0 0

0 / 0 0

0 0 0 /

0 /

I 0

- PA
- PB.


Pia Pia

P'n

P2b

Pu

P'lc

Pu Ρ'ζαΔ

![image 129](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile129.png)

where / and 0 are matrices of a size appropriate to the number of components in the load vectors. This may be written as

P = C0p^ (6.3)

the matrix C0 being termed a connection matrix^.

Secondly we note that the components of the vector d^ appearing in equation (6.2) must satisfy the compatibility conditions

à\a = à\b = d'lc = 0 d'2ü = d'2b = d'u = dA d'2c = d'2d = dB which we may write as

01 0 0 0 0 / 0 l\

= "0 / 0 / 0 0 /

\d'ia~\ a'la

d'ib

a'lb

###### \d'u

d2c

à\à Ld2d.

###### _o

or as

dm = Cod (6.4)

Equations (6.3) and (6.4) provide another example of the contragredient nature of load and displacement transformations which we discussed in section 3.4. It is easy to show that this relationship must hold for any linear structure. If in a general structure we consider a small virtual displacement of the joints of the connected structure <5d, then the work done by the applied loads is equal to pf<5d, and this must equal the change in the strain energy stored in the members pm<5dm. Thus we have pf<5d = pm(5dm,

t This matrix is written as Co merely to distinguish it from the matrix C introduced in the next section.

![image 130](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile130.png)

so that if p and p^ are related by equation (6.3) we have p^,C0<5d = Pm<5d^. Since δό and p'm may be chosen quite independently this equation implies that Ο0δό = ôd'm and since we are assuming that the displacements of the structure are small enough for the geometrical relations between displacements to be linear equation (6.4) follows. A similar argument based on the invariance of electrical power leads to a similar result for voltage and current transformations in electrical network theory.

We now use equations (6.3) and (6.4) to eliminate the vectors p'm and d^, from equation (6.2), giving

###### p = (C0K^C0)d (6.5)

Comparing this equation with equation (3.2) it follows that the stiffness matrix of the assembled structure K is equal to CQK^CO. The reader may easily verify that for the simple example shown in

- Fig. 6.1 the stiffness matrix derived in this way agrees with that appearing in equation (6.1). We may argue on physical grounds


that although K'm is singular the matrix product 00Κ^Ο0 is not, so that equation (6.5) maybe inverted to gived = ( C O K ^ C Q ) " ^. Substituting this expression into equation (6.4) gives

###### d^ = C'oCCoK^C^-'p

while equation (6.2) gives the corresponding expression for the member end-loads

###### p^ = K ^ = K^COiCoK^q,)-1? (6.6)

Although equation (6.6) provides an explicit formal expression for the internal forces and moments in a structure under a given load, practical computer programs based on the equilibrium approach usually employ the general rules given in section 4.3 for the construction of the complete stiffness matrix K. This is partly because the large number of zero elements in the C0 and K^ matrices make the formal matrix multiplications of equation (6.6) rather an inefficient way of carrying out an essentially simple process. The relatively large size of the K'm matrix compared with

![image 131](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile131.png)

###### CONNECTION MATRICES AND DETERMINATE SYSTEMS 123

the final matrix K may also introduce storage problems, unless advantage is taken of the large number of zero elements.

6.2. An Alternative Formulation of the Equilibrium Method

The matrix C0 defined in the previous section is simply a matrix composed of O's and l's which describes the topology of a structure—that is, the way in which the various members are connected together. The information about the elastic characteristics of the members and their orientations with respect to the system axes is contained entirely in the matrix K'm. We now consider an alternative formulation of the equations in which the orientation of the members is included in the connection matrix, and the matrix K'm is replaced by a matrix which is nonsingular.

In the previous section we used the symbols p^ and à'm to denote the complete vectors of member end-loads and enddisplacements in a structure, relating these vectors by equation (6.2). This statement of the properties of the members contains a considerable amount of redundant information, however, which results in the matrix K^ being twice as large as is really necessary. We know that a load pt acting on the end of a member can always be expressed in terms of the corresponding load p2 by means of an equilibrium equation of the form pt + Hp2 = 0, which does not involve the elastic properties of the member. Thus a vector whose components are simply the loads acting on end 2 of the members provides a more compact and equally unambiguous way of defining the complete set of internal forces and moments in a structure. We shall retain the symbol pm for this vector, but in contrast with the previous section we shall imagine each component p2 to be expressed in the member coordinate system of its associated member. (Our choice of end 2 for each member here is arbitrary, but corresponds to the practice adopted in chapter 5 of regarding the load on a

![image 132](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile132.png)

member as being specified by p2- the end-load pt being considered merely as a support reaction whose function is to maintain the member in equilibrium.)

In a similar manner we may halve the size of the vector describing the member end-displacements by working in terms of the member deformations, i.e. the relative displacements of the two ends of members, rather than with the absolute displacements dl9 d2. It will be recalled that in chapter 5 we introduced the quantity e9 defined by (5.10) or (5.15), to represent the displacement which end 2 of a member would have if end 1 were fixed. This quantity defines the member deformation, and has the advantage of being uniquely defined for any given loading, irrespective of any rigid-body displacement which the member may have. We shall write the vector formed from all the relative displacements e of the individual members as em; as in the case of the vector pm we shall measure these displacements in the various individual member coordinate systems. Provided a structure is sufficiently anchored to prevent overall rigid-body movement there will be a unique set of joint displacements d corresponding to any particular set of member deformations em.

For each member of a structure we have an expression (5.11) relating the load p2 and the deformation vector e, and all these expressions may be collected together into a single matrix equation. For the example shown in Fig. 6.1 this equation has the form

###### >2«Ί = f X 0 0 0

0 Kb 0 0 0 0 Kc 0 0 0 0 KdJ

Pib Pic \-PidA

- *b
- *c


or more briefly

Kme„ (6.7) Equation (6.7) differs from equation (6.2) in three ways. In the

![image 133](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile133.png)

first place, the component load and displacement vectors are in member coordinates, so that the diagonal matrix Km represents the elastic properties of the completely unconnected members, without containing any information about their orientation. Since the component K matrices are in member coordinates they will usually be relatively simple in form. In the second place the vectors pm and em have only half the number of components appearing in the vectors p'm and d^ defined in the last section. In the third place, and most important of ail for our purpose, the vector em is uniquely defined for any given pm, so that the matrix Km is always non-singular. It follows that equation (6.7) may be written in the inverse form

em = Fm Pm (6.8)

where Fm is simply the diagonal matrix formed from the member flexibility matrices, and in our example has the form

[Fa 0 0 0 1 0 Fb 0 0 0 0 Fc 0

###### L° ° 0 Fj

As mentioned in chapter 5, it will often be in the flexibility form

- (5.10) that the relations between the loads and deformations for the individual members are first derived. If deformations due to


temperature are present, equation (6.8) becomes em = Fmpm -f emt. The completion of the analysis for the latter case is left to the reader.

Following the procedure of the previous section, we now consider the assembly of the members into a connected structure. In our illustrative example the equations of joint equilibrium are

- PA = Pia + Pib + P\d
- PB = Pic + Pid


![image 134](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile134.png)

Now for each member we may combine the equations of equilibrium (5.2) with the equations describing the change to system coordinates, writing them in the form

Pi = Tp2 Pi = Tp\ -THp2

Substituting these expressions into the joint equilibrium equations we obtain

PA = Tap2a + Tbp2b - TdHdp2d PB = TcP2c + Tdp2d

which we may write in the form T o 0

0 — TdHd Pia Pib Pic

- PA
- PB


###### LPuA

or simply as

###### P= Cpn (6.9)

The general rule for the construction of the connection matrix C should be clear from the example. The element in row i and column j of C refers to joint / and memberj . If member j has end 1 at joint / then the element is the matrix product — TH, where T and H are the matrices associated with the member. If the member has end 2 at the joint then the element is simply Γ, while if neither end is connected to the joint the element is zero, or, more precisely, a null matrix of the appropriate size.

It will hardly surprise the reader to find that the deformation vector em is related to the joint displacement vector d by the equation

e m = C ' d (6.10)

![image 135](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile135.png)

The proof follows very much the same lines as before. The work done on the structure by the applied loads during a virtual displacement <5d is p'(5d, while the increase in the strain energy stored in the members is pfm<5em. (Note that although any particular load p2 does not actually displace by be the increase in strain energy stored in the member is always p2be, since the general pair of virtual displacements bdu bd2 of the ends of a member may be split up into a pair bdt = 0, bd2 = Se, and another pair corresponding to a rigid-body displacement of the member. The endloads pl9 p2 do no work during the rigid-body displacement.) Hence we have p'(5d = p'm(5em, and if p and pm are related by equation (6.9) then equation (6.10) follows by the same argument as before.

Combining equations (6.7), (6.9) and (6.10) we obtain

###### p = (CKmC)d (6.11)

As in the previous section, the reader may easily verify that for our particular example equation (6.11) is identical with equation

- (6.1), the member stiffness matrices Kli9 etc., being determined from the member K and H matrices in accordance with equations


- (5.18). Inverting equation (6.11) we obtain


d = (CKmC)-Ip (6.12) and from equations (6.10) and (6.7) we have

em=C'(CKmC)-1p and

Pm = Kmem = KnCXCKnC'yip (6.13) Equation (6.13) is merely an equivalent form of equation (6.6). The main difference between the two forms is that the H and T matrices which were contained implicitly in K'm have been transferred to C, with the result that the matrix Km is non-singular, and much simpler in form than K^.

![image 136](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile136.png)

###### 6.3. The Analysis of Determinate Structures

Although equations (6.12) and (6.13) have not been used extensively as the basis of practical methods of structural analysis, they provide a quite general formulation of the equilibrium method in a way which allows us to consider the special case of determinate structures. By definition a determinate structure is one in which the equations of equilibrium are sufficient to determine all the internal forces and moments. As we have seen in the previous section, the individual conditions of member equilibrium will always give us the load at one end of a member in terms of the load at the other. This implies that if the conditions of joint equilibrium are sufficient to determine the vector pm defined in the previous section, then all the other forces and moments in the structure may be found from the individual equations of member equilibrium.

It follows, therefore, that the determinacy or otherwise of any structure of the skeletal form considered in this book depends entirely on whether equation (6.9) can be solved for the vector pm. If the matrix C appearing in that equation is rectangular then it is impossible to obtain a unique solution and the structure is consequently hyperstatic.| But if the inverse matrix C"1 exists then the internal forces and moments in the structure can be obtained immediately by writing equation (6.9) in the form

P m = C " 1 p (6.14)

This gives us a simple expression for the displacements of a determinate structure, since if C is non-singular we may write equation (6.12) in the form d = ( C ^ ' K ^ C ^ p . This follows from the rule given in section 2.3 for the inverse of the product of a number of non-singular matrices. As mentioned in the previous

t It may be noted that in the case where the structure is in fact a mechanism the matrix C will also be singular. The difference between the two situations is reflected in the form of the equations. For a hyperstatic structure there will be a whole range of different vectors pm which will satisfy equation (6.9). In the case of a mechanism there will in general be no solutions at all.

![image 137](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile137.png)

section, the matrix Km is always non-singular. Since we have Km1 = Fui fr°m equations (6.7) and (6.8) it follows that

d = (C-7FmC-1p (6.15) We may also note that if C is non-singular then equation (6.13) becomes pm = K ^ ^ C ^ K ^ C " " ^ which reduces, as we should expect, to equation (6.14).

An unfamiliar symbolism should not conceal the fact that equation (6.15) is merely a description in very general mathematical terms of the way in which we normally analyse a determinate structure. The process may be split up into three steps:

- (1) The internal forces and moments are found in terms of the known external loads by solving the equations of joint equilibrium (pm « C ^ p ) .
- (2) The member deformations are found from the internal forces and moments and the elastic characteristics of the members


(em = FmPm).

(3) The joint displacements are computed from the member deformations (d = (C"1)^). It will be noted that the matrix C~ * has already been found in the first step, so that the last operation requires no new information about the structure.

Applying these ideas to the simple example which we have been considering, we see that our physical knowledge that the frame is hyperstatic can be put into mathematical form by saying that the matrix

C = Ta Tb 0 -Γ,Η,, (6.16)

0 0 Tc Td

appearing in equation (6.9) is singular. This is immediately apparent from the form of the matrix, since the T matrix of a member of rigid-jointed frame is square and the matrix C is therefore rectangular.

Consider now the case where the structure has pinned instead of

![image 138](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile138.png)

rigid joints, the members forming a plane truss as shown in Fig. 6.2. This has the same topological arrangement as the frame shown in Fig. 6.1, and its C matrix is still given by equation

- (6.16). However, the structure is now quite clearly determinate, so that in this case (6.16) ought to define a square non-singular matrix. It is easy to show that C is in fact now square and nonsingular.


PyB . ByB

PyA » $yA

FIG. 6.2. Example of a plane pin-jointed truss.

For a member of a plane pin-jointed frame inclined at an angle a to the x' axis the T matrix was shown in section 4.1 to be given by

cos a sin a

Thus the T matrices for the members appearing in Fig. 6.2 are

T = T T„ = i/V2' •i/V'2

###### r,=

It will also be remembered that the member end-load vectors for a pin-ended member in member coordinates have only a single

![image 139](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile139.png)

###### CONNECTION MATRICES AND DETERMINATE SYSTEMS 131

component each, the equation of member equilibrium being simply Pi + Pi = 0· It follows that the matrix H for a pin-ended member is merely a single element whose value is 1. Thus any term in C of the general form — TH may be replaced by — T when the member is pin-ended. This result holds irrespective of whether the member is part of a plane or a space frame.

Substituting these values for the elements Tand — TH in equation (6.16) we obtain

C = 1 l/yj'2 0 0*

0 -1A/2 0 - 1 0 0 1 0 0 0 0

Written out in full equation (6.9) is

(6.17)

1 0 0

0"

l/>/2 0

'Plal

PxA PyA PxB

###### -1/V2 0

- 1

Pib Pic -PidJ

0 1_

0 1 0 0 0

.PyB.

It should be noted that in the case of a pin-ended member our sign convention is such that p2 is equal to the tension in the member. The reader may easily verify that this statement of the joint equilibrium conditions is identical with the equations derived by a direct consideration of the forces in the truss. It will be seen that C is non-singular, as expected, and equations (6.17) may be inverted to give

Pia' (6.18) Plb Pic Pip-

— "1 0 0

1

0

i -

PxA PyA PxB

- 0
- 1 0


###### -V2

###### -V2

0 0

0 1

_0

-PyB

![image 140](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile140.png)

###### 132 MATRIX METHODS OF STRUCTURAL ANALYSIS

The triangular form of C makes the inversion process extremely easy, and produces a matrix C~ * which is also an upper triangular matrix. We shall see later that this is a common feature of C matrices. In this example equation (6.18) may easily be checked by statics.

As we showed in chapter 4, the K matrix of a straight uniform pin-ended member is simply the single coefficient EA/L. The F matrix is therefore simply LjEA. If the members of our truss are straight and of uniform cross-section then equation (6.8) has the form

0 "1 0 0 (L/EA)d\

\e°~ (6.19) eb

= '(LjEA). 0 0 0 (LIEA)b 0 0 0 (LfEA)c 0 0 0

[P2a Pu

Pic

€c

YPid The quantity e for a pin-ended member is simply the relative displacement of the ends and is equal to d2 — dl9 i.e. it is merely the extension of the member.

ltd.

Having now obtained the matrices C - 1 and Fm we may complete the analysis by obtaining the displacements of the joints of the structure from equation (6.15),

###### = 0

0 0

0 0 0

0 F„ 0 0

###### [àxA~

àyA

0

###### àXB

Fc

0

###### F,

- Λ / 2

L<>yB^

1 0

1 1

\ΡχΛ

###### V2 o

PyA PxB

" V 2 0

0 1 0 0

###### 1 J

LPyB-

where F = LjEA.

![image 141](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile141.png)

CONNECTION MATRICES AND DETERMINATE SYSTEMS 133

While the simple truss which we have considered is determinate if its deformation is restricted to a plane it becomes a mechanism when considered as a three-dimensional structure. (The pinjoints at the ends of the members are assumed to be replaced by ball-joints.) This is reflected in the form of the C matrix, which becomes rectangular when the Γ matrices appearing in it are those associated with a general pin-ended member in three dimensions. Each of these matrices consists of a column of three components —the general form is defined in section 4.6. The matrix C has therefore more rows than columns, so that equation (6.9) has no general solution. There may of course be a solution for particular values of the external load vector p, but this is not sufficient to make the assembly of members a "structure" in the usual sense.

Finally, it should be realized that the analysis described in this and the previous sections is not restricted to structures whose members are all of the same type. For example, one can apply it to the case where the members a, c and d in Fig. 6.2 are rigidly joined together at their ends, but the member b is still pin-ended. In these circumstances, the matrices Ta, Tc Td9 Hd appearing in equation (6.9) are the appropriate square matrices associated with members whose ends can carry bending moments, while the matrix Tb consists of a single column. It is necessary to add zeros to this column in the rows corresponding to the moment components of pA—it is clear that the force in member b can make no contribution to these components. Similarly the members a, c and d each contribute a displacement and end-load vector containing six components (or three if the frame is plane) to the vectors em and pm, while the member b only contributes a single term to each. The matrix Km also contains the appropriate square matrices for members a, c and d, and a single element for the member b. With the various vectors and matrices defined in this way the formal solution provided by equations (6.12) and (6.13) still holds.

![image 142](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile142.png)

6.4. Determinate Structures with Rigid Joints: Tree Structures

If one were constructing a computer program it might be sensible to use the singularity or otherwise of the matrix C as a test for the determinacy of a given structure. Human beings, however, usually prefer to make this test by visual inspection of the line diagram of the structure. In the case of a structure in which all the joints are rigid this test is very simple—simpler, in some ways, than the corresponding test for a pin-jointed frame.

If we consider again the simple frame shown in Fig. 6.1 it is clear that any load such as pA must eventually be transmitted to the foundations of the structure. Now in this particular example there are three alternative paths for the transmission of the load pA to the foundations—the member a, the member b, and the pair of members c and d. Without information about the relative stiffness of these members we cannot tell what proportion of pA will follow each path. We cannot therefore determine the internal forces and moments from statics alone, so that the structure is hyperstatic. From this argument it follows that for a rigid-jointed structure to be determinate there must be only one path to the foundations from any given loading point. This implies that the structure must only be attached to a rigid foundation at a single point, and that the members must be arranged in such a way that they do not form any closed rings. Such a structure we shall term a tree structure. At first sight the analysis of tree structures might appear to be merely an academic exercise, since few engineering structures are of this form. However, as we shall see in chapter 7, the application of the compatibility method to a rigid-jointed structure involves the reduction of the structure to determinate form by the introduction of suitable "releases". If these releases take the form of complete discontinuities in the structure the result is a tree structure. It is for this reason that the problem is discussed here.

The simplest type of tree structure is one consisting merely of a

![image 143](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile143.png)

###### CONNECTION MATRICES AND DETERMINATE SYSTEMS 135

single branch, as shown in Fig. 6.3, If we apply the rules given in section 6.2 for the construction of the matrix C we find that the matrix for this structure is given by

C=rrfl -TbHb 0 . . . . 0 ](6.20)

0 0

Tb -TCHC 0 0 Tc -TdHd 0

0 0 0

TkHk

This may easily be verified by deriving equation (6.9) from first principles. The simple regular form of this matrix makes its inversion a straightforward matter. It is convenient to commence

FIG. 6.3. A tree structure with one branch.

the inversion by writing all the H matrices appearing in equation

- (6.20) in the overall system coordinates used to describe the applied loads. It will be recalled that in section 5.4 we showed that an H matrix transforms into system coordinates in the same way as an F or K matrix. Thus we have //' = THT\ and post-multiplying


![image 144](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile144.png)

both sides of this equation by T we obtain H'T = TH. Thus equation (6.20) may be written in the alternative form

0 0 0

Γ„ -HLTh 0

0 0

Tb -H'X 0 0 Tc -HJd 0

0

We can now carry out the inversion process described in section 2.6. It is necessary to exercise a certain amount of care in maintaining the order of multiplication in the products of the T and H' matrices, but otherwise the manipulations may be carried out as though these matrices were single elements. Since there is only one oif-diagonal element to be eliminated in each row of C the process merely consists of the following operations applied to the rows of both C and a unit matrix of the same size:

- (1) The last row is pre-multiplied by H'k and added to the

previous row.

- (2) The last row is multiplied by Γ£. (Note that the T's are

orthogonal matrices, so that Γ""1 = T'.)

- (3) Operations (1) and (2) are repeated for the last row but one,


and then for all the preceding rows, the appropriate H and T matrices being used at each stage.

This process results in the matrix C being reduced to a unit matrix, and the original unit matrix being transformed into C'1.

The reader will find that the off-diagonal terms of C"1 involve products of H' matrices, and the form of the inverse is considerably simplified if we use the result of section 5.2. For example, it

![image 145](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile145.png)

###### CONNECTION MATRICES AND DETERMINATE SYSTEMS 137

follows from the analysis in that section that the matrix product H'bH'cH'd is simply the H' matrix of the composite member formed

from b, c and d, which we shall write as H'AD. With this notation we have

###### c-1- V 0 0

ΤαΗΛΚ

TaHÂc

T'OHAB

###### Ά

T'bH'BK T'cH'CK

TÎH'BC

###### rc

0

###### 0 τ·

0 0

T}H'jK

###### n

0

Once C"1 has been found the determination of the forces and moments in the structure and the displacements of the joints follows from equations (6.14) and (6.15).

If we take the special case where the only non-zero load vector is pK we find from equations (6.14) and (6.15) that the vector pm is given by

###### ΤΉ'AK

PK

T'JH'JK

V

and the displacement dK is given by

![image 146](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile146.png)

###### 138 MATRIX METHODS OF STRUCTURAL ANALYSIS

<lK = IMAKJO H'BK ?b HJKTJ TJ x

0 ΤαΗΆκ

Fa 0 . 0 Fb 0

Ρκ (6.21)

ΤΟΗ'ΒΚ

0

###### 0 . . 0 F J L Ti

Since TaFaTj = Γ^ etc. this may be written

dK = (HAKFÜHAK + H'BKFÎBBK + ··· ^K)PA:

which agrees with the expression previously obtained in section 5.5 for the flexibility matrix of a member comprising a number of elements joined end-to-end.

FIG. 6.4. A tree structure containing two branches.

The same approach may be used in dealing with a tree structure which has several branches. Consider, for example, the structure

- shown in Fig. 6.4, where loads may be applied at any of the joints A, B, ..., F. Applying the rules given in section 6.2 we obtain


![image 147](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile147.png)

CONNECTION MATRICES AND DETERMINATE SYSTEMS 139

###### c = TbHb

0

0

0 0

0 0 0 0

###### T„

###### - TeHe

-TCHC

0

0 0

— TdHd

Te 0

Td 0

T 0

-TfH, 0 Tf

As before, this result may easily be checked by deriving equation

- (6.9) directly. By the same method as we used in the previous example we find that


###### Tan\E

T'H'AC TbH'BC

T'H'AO

H'AB

TOH'AF

###### V

Τ£Η'Βϋ TcH'co

TbH'BF

Tb^BE

###### V

0 0

0

0 0

0

Jt

0

Λ e

0 V If we have a general tree structure, and label it in the way indicated in Fig. 6.4 (that is, joint Q is the joint at end 2 of member q)y then the element in row r and column s of C"1 gives the load vector p2 acting on the end of member r due to a unit load vector acting at joint S. We may state the following general rule for the construction of the matrix C"x :

0

"If s < r, then the element is zero. If s — r the element is Tr. If s > r then the element is Τ[Η'Κ8 if the path from joint S to the foundation passes through member r and zero otherwise."

The formal rules developed in this chapter for the construction of the C and C"1 matrices may seem at first sight to be an unnecessarily complicated way of deriving equations which can perfectly easily be written down by applying simple physical reasoning

![image 148](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile148.png)

###### 140 MATRIX METHODS OF STRUCTURAL ANALYSIS

to the line diagram of a structure. The reduction of geometrical arguments to formal algebraic statements is, however, a necessary part of the development of methods suitable for use with computers.

![image 149](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile149.png)

###### CHAPTER 7

###### The Compatibility Method

IN this chapter we describe the compatibility method, an outline of which was given in section 1.4. Following the practice of previous chapters the method is presented as a systematic process which can conveniently be carried out on a computer. We also discuss the way in which the compatibility method is related to the equilibrium method.

In the preceding chapter we showed that the load-displacement equations of a structure can be written in the form

p = (CKmC)d (7.1)

where Km is the non-singular stiffness matrix of the individual disconnected elements and C is a matrix which relates the applied loads to the internal forces and moments. The matrix C is independent of the elasticity of the structure and is derived simply from the conditions of joint equilibrium. The normal process of analysing a structure by the equilibrium method involves the inversion of the matrix CKmC (or the solution of the corresponding linear equations) to give an expression for the joint displacements in terms of the known applied loads. Since the order of this matrix is equal to the total number of degrees of freedom of the structure the inversion process (or the solution of the equations

- (7.1) for a particular load vector) may be regarded as the central computational problem of the method.


In the case of a determinate structure, however, the matrix C is

non-singular, so that the inverse of the matrix CKmC may be written in the simpler form (C"1)^^"1. As we saw in the

141

![image 150](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile150.png)

###### 142 MATRIX METHODS OF STRUCTURAL ANALYSIS

previous chapter, the matrix C is usually of simple form and therefore easy to invert, it being possible to write down C""1 directly in a number of cases. If only the forces and moments in the structure are required then it is unnecessary to compute the displacements, since the member end-loads can be found immediately from the equilibrium equations pm = C_ 1p.

FIG. 7.1. A pin-jointed truss with a "redundant" member.

The relative simplicity of the analysis in the case of determinate structures suggests the possibility of finding a method which retains at least some of this simplicity when applied to structures whose degree of indeterminacy is small. This is the idea behind the method which we describe in this chapter. The basis of the method is very simple. A hyperstatic structure is made statically determinate by relaxing the conditions of compatibility at sufficient points. This structure is then analysed by means such

- as those described in section 6.3, and finally the forces and moments which must be apphed at the points of discontinuity to produce displacement compatibility are calculated.


As in chapter 4, we introduce the method by applying it to some simple examples. The first of these is a plane pin-jointed truss.

![image 151](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile151.png)

THE COMPATIBILITY METHOD 143

###### 7.1. The Analysis of a Pin-Jointed Truss

We consider the pin-jointed truss shown in Fig. 7.1. This is identical with the truss discussed in section 6.3, except for the presence of the "redundant" member r.

Applying the rules for the assembly of the matrix C given in section 6.2 (or by direct equilibrium considerations) we obtain joint equilibrium equations (6.9) in the form

- A (7.2)
- B.


0]

0 T

= " T

Tb 0

- TdHd Td

[Pia

.0

Tr\

Pib Pic Pid

LPlr

This equation holds whether the structure is pinned or rigid at the joints. For pin-ended members in a plane the T matrices for the various members are

T =

T = "1/V2]

Γ1"

T„ = "0" .1.

T„ =' 1/V2' .-1/V2.

###### k

.1/V2J

Remembering that for a pin-ended member H = 1, equations

- (7.2) may be written out in full as


PxA (7.3)

0 Ί

0 - 1

= "1 0 0

1/V2 0

\Pla

- 0

l/V'2

- 1/V2J


-i/V2 o

Pib Pic

- PyA PxB
- PyB.


- 0
- 1


0 1 0 0

_0

Pid

LPlr

The reader will notice that this equation is identical with (6.17), except for the extra column of C associated with member r and

![image 152](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile152.png)

###### 144 MATRIX METHODS OF STRUCTURAL ANALYSIS

the extra component plr in the vector of member end-loads. Since C is now rectangular we cannot invert it as we did when the structure was determinate. We overcome this difficulty by temporarily relaxing one of the displacement compatibility conditions which have to be satisfied by the members of the structure. We shall choose the condition imposed on end 2 of member r as the one which we shall relax, this choice being quite arbitrary.

PyP L

###### I c \/q

###### "Γ . y

j

/ N. b

Δ. » i

■ τ *P*A k

###### §f ° t

PyA

FIG. 7.2. A pin-jointed truss made determinate by the insertion of a release.

In other words we imagine the structure to be broken at this point, as shown in Fig. 7.2, and introduce a pair of forces which we treat as external loads acting on the structure. This process is sometimes described as inserting a "release" in the structure. It will be noted that it is not merely a matter of adding a single load to the applied loading, but a pair of loads which are necessarily in statical equilibrium. In general we shall use the symbol q to denote a self-equilibrating load-pair of this sort, and in this example we shall find it convenient to put p2r = — q> as shown in the figure.

![image 153](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile153.png)

THE COMPATIBILITY METHOD 145 If we now include q in the vector of the applied loads equation

(7.3) becomes

1/V2 0 -1/V2 0

= "1 0 0 0

0 0 1

(7.4)

PxA

[Pla~

- 1 0

###### Pu

- PyA PxB
- PyB


0 1/V2 i i/V2

0 1 0 0 0 0

Pic Pit

###### 0 -1 J

.0

LPlr.

Q .

Thus we have replaced C by an augmented matrix C+ which is square and non-singular. Inverting (7.4) we obtain

= "1 0 0 0

1

1 0

'Pia' (7.5)

1/V2]

[PxA

###### -V2

. - 1

-y/2 0 0 1 0 0 0 0

Plb Pic Piâ _P2r.

- PyA PxB
- PyB


0 1 0

' 1/V2 1/V2

###### - i J

_0

L <5f

These equations are very similar to (6.18) and may easily be checked by statics.

We now split up the square matrix C+1 appearing in equation (7.5) into two rectangular matrices, which we shall call B0 and B. The matrix B0 consists of the first four columns of C+1, which are associated with the known applied loads ρΛ and pB. The

- matrix B consists of the last column, which is associated with the unknown load-pair q. Thus we write (7.5) in the form


Pm = B0p + Bq (7.6)

Having expressed all the internal forces in terms of the external loads and the unknown q we can now compute the vector of member deformations em from the individual member flexibilities in

![image 154](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile154.png)

###### 146 MATRIX METHODS OF STRUCTURAL ANALYSIS

the form

(7.7)

em=FmPm=Fm(B0p+ Bq)

where

(LjEA)a 0 0 (L/EA)b .

(L/EA)d 0

###### 0 (L/EAXJ

0

We now use the relationship between load and displacement transformations to obtain the joint displacement vector d from the member deformation vector em. To this vector we must add a term corresponding to the displacement associated with q, and before proceeding further it is necessary to consider how we should define the displacement associated with a self-equilibrating force-pair of this type. It will be recalled that the derivation of the relationship (6.10) between joint displacements and member deformations was based on the equating of the work done by the applied loads to the change of strain energy stored in the members during a virtual displacement. It follows that the displacement associated with any particular load must be such that the scalar product of the load and the change in displacement is equal to the work done by the load. Hence the displacement which must be associated with the force-pair q, — q is the relative displacement of the two points of application, i.e. the quantity u

- shown in Fig. 7.2. We use the symbol u here rather than d since we are concerned with a relative rather than an absolute displacement.


Since (7.6) may be written in the form

###### Pm = [BoB][p]

A\

![image 155](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile155.png)

THE COMPATIBILITY METHOD 147 it follows from (6.10) that

- (7.8)
- (7.9)


B' Combining (7.7) and (7.8) we obtain

Fm[B0P+ B<j]

BO B'

While this equation is formally similar to (6.15) it must be remembered that q is not really a known external force, but an unknown which has to be determined from the condition u = 0. Equation (7.9) may be written as

d=B'0FmBop+B'oFmBg «=B'FmB0p+B'FmBg

(7.10)

Since we know that in the real structure u must be zero the second of these equations gives us

BiFmB0p=-BiFmB^ from which we obtain

###### ^-(B'F^r'B'F^oP (7.11)

This equation for the unknown q may be given physical meaning

- as follows. We imagine first of all that the loads p are applied* to the structure with member r not connected to B and carrying no


load. Thus q is zero and the gap u is given by u = B*FmB0p. This is a straightforward application of equation (6.15), the

matrices B0 and B being, as we have seen, merely the appropriate columns of the square matrix C+1. We now consider the value

of the pair of forces q9 — q which must be applied to make the gap zero. Once again we are dealing with a determinate system, and we find that the flexibility of this system, as measured at the gap, is BfFmB. Thus the force-pair necessary to bring the two

LF

![image 156](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile156.png)

###### 148 MATRIX METHODS OF STRUCTURAL ANALYSIS

sides of the gap together (i.e. produce a relative movement — w) is given by the equation — u — BfFmB#, from which (7.11) follows. It should be noted that although written in matrix form the product B'FmB is in this example a single number, so that its "inversion" is trivial.

###### B/PB

^\\\vS\\S\\\V

FIG. 7.3. An example of a portal frame.

Having determined q we may return to equation (7.6) for the other internal forces in the structure. Substituting for q from (7.11) we obtain a formal expression for the forces in the bars

Pm = (I - B(B'FmB)-1B'Fm)B0p (7.12)

It will be noticed that in this expression the matrix B0 only appears in the product B0p. It follows immediately from (7.6) that this product represents the values of the forces in the bars when the unknown q is zero. The displacements of the joints may be obtained from the equation

d = B'0FmPm (7.13)

while as a check on the analysis we may evaluate the product B'Fmpm, which should be zero from (7.10).

One feature of the above analysis which is characteristic of the compatibility method is the arbitrary choice of redundant. It is clear that in this example we could have chosen the force in any of

![image 157](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile157.png)

###### THE COMPATIBILITY METHOD 149

the other bars as our q. In each case we should have obtained different matrices B0 and B, but the final numerical values for the forces and displacements would have been the same.

7.2. The Analysis of a Rigid-Jointed Frame

For our second illustration of the method we consider the simple portal frame with rigid joints shown in Fig. 7.3. The loads

- at the joints A and B are assumed to include any fixed-end forces and moments which may arise from mid-span loading on the beam. As in the previous chapter, we shall work in terms of the H, F and T matrices of the members, so that provided these matrices and the load and displacement vectors are suitably defined our analysis will apply equally well to a plane or a space structure.


The starting point for both the equilibrium and the compatibility methods is the same—the equations of joint equilibrium. From the rules given in the last chapter for the assembly of the

- matrix C we may write these equations as


Ta — TbHb 0 Tb

(7.14)

0

Pia Pib

PA PB

— TCHC

PlcA

For comparison with the analysis involved in the compatibility method we note that the load-displacement equations derived by the equilibrium approach are

- PA
- PB


###### °Ί

0

0

X

TbHb 0 Tb — TCHC

Ka

###### n

o

0 0

0

###### K„

###### -WV d„

xJI

0 -HX'

0

![image 158](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile158.png)

###### 150 MATRIX METHODS OF STRUCTURAL ANALYSIS

or

###### '(*ί2). + (*ίι)> (K[2)b

PA

###### (ill)» (*«)* + (*ll)c l A j

IPB.

As in the previous example, we see that the matrix C appearing in (7.14) is rectangular and therefore singular. To make it square we consider the related structure shown in Fig. 7.4, in

C^^r q

FIG. 7.4. The portal frame of Fig. 7.3. with joint C allowed to move.

which the joint C is allowed to displace and the foundation reaction at C is thought of as an external load q. As in the previous example, this load should be regarded as a self-equilibrating pair of loads, although since one half acts on a rigid foundation whose displacement is always zero the displacement vector u associated with q is in fact equal to the absolute displacement of end 2 of member c. If the frame is a plane one the relaxation of the compatibility condition at C introduces three extra displacement and load components, while if it is a space frame the number is six. We may therefore refer to the imaginary cutting of the frame at C as introducing a three-fold or a six-fold release.

Augmenting the matrix C appearing in (7.14) with an extra row for the load q gives

![image 159](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile159.png)

THE COMPATIBILITY METHOD 151

0 1

= T 0

-TbHb

[Pia

- PA'
- PB «_


###### T„

-TCHC\

Pzb {.Pic

Tc J

0

. 0

The matrix Tc appears in the last row of the augmented matrix merely because q has been thought of as an external load, and has therefore been expressed in system coordinates. It might equally well have been defined in the coordinates associated with member c, in which case Tc would have been replaced by a unit matrix of appropriate size.

We may now use the rule developed in section 6.4 for the in-

version of the matrix C of a tree structure. This gives Pia' (7.15) Pu

###### = ~r.

Τ·Η'ΛΒ

- PA
- PB


VA'AC

###### n

0 _0

T'bH'BC

###### n -

0

. 9

Pic.

As before, we write the matrix appearing in (7.15) as C+1, and split it up into two matrices B0 and B. The matrix B0 consists of the first two columns of sub-matrices and is associated with the known applied loads pA, pB. The matrix B consists of the last column of sub-matrices (i.e. three or six columns of scalar coefficients, depending on whether the frame is a plane or a space structure), and is associated with the unknown load q. The division is indicated by the dotted line in (7.15).

The analysis is now almost identical with that given in the previous section. Equation (7.15) is written as

Pm= B0p+ Bq (7.16)

and the corresponding relation between the joint displacements and the member deformations is

B' (7.17) B

![image 160](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile160.png)

The reader will note that the displacement u is defined in such a way that the load-pair ±q does work q'öu in a virtual displacement ou. The member deformations may be expressed in terms of the member end-loads in the usual way as

em "mrn (7.18) where in this example

Fm = [Fa 0 0 0 Fb 0 0 0 Fc

and eliminating pm and em from (7.16), (7.17) and (7.18) we obtain

d=Bi0Fm(B0p+Bi) u= B'Fm(B0p + Bq)

which are identical in form with (7.10) except thai q and u are now vectors.

We now apply the condition u = 0 to the second of these equations. It must be remembered that this is a vector equation, corresponding to three or six scalar equations, according to the number of components in u. Thus we obtain the unknown load q>

###### ^ - ( Β ' Ρ , , , Β Γ ' Β ^ Β ο ρ

This part of the calculation involves the inversion of the matrix BfFmB, whose order is equal to the number of components in the load vector q, while the equilibrium method requires the inversion of a matrix twice this size. The final expressions for the member end-loads pm and the joint displacements d are formally the same as those given in equations (7.12) and (7.13).

As in the previous example, it may make the analysis easier to follow if the release of joint C is thought of as an actual physical

![image 161](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile161.png)

###### THE COMPATIBILITY METHOD 153

occurrence, rather than a mere mathematical fiction. Thus we may imagine that we start with the determinate structure OABC and load it at A and B, leaving C entirely free. Since this structure is determinate its displacements are given by equation (6.15), C being replaced by C+. Since we know that the load q is zero we may drop the column of the matrix C+1 which multiplies q in that equation. This has the effect of replacing C+1 by the matrix which we have defined as B0. In the same way, to find the displacement u of joint C we need only take the appropriate row of (C+1)', which is the matrix Bf. Hence we have the displacement of C due to the loads at A and B as u = BTmB0p.

We now consider the load q required to close the gap, i.e. to produce a displacement at C of — u. To find this we need the flexibility matrix of the structure as measured at C, and in calculating this matrix we need not consider the loads at A and B. In (5.20) we already have a general expression for the flexibility matrix of a series of members connected end-to-end, which in the notation of this chapter is equivalent to the product B'FmB. Written out in full this product is H^cF'aHAC + H'j}cF'bH'BC + F'c, which agrees with the analysis of section 5.5. It follows that the stiffness matrix of the system OABC as measured at C is (B*FmB)-1, and hence that the load required to produce a displacement —u is — (BtFmB)~1u. This gives the same result for q as before.

Our decision to introduce the releases at C was of course quite arbitrary. We might have chosen to introduce them at joint B, as shown in Fig. 7.5. The corresponding "external'* loads would then be the self-equilibrating load-pair q, —q shown in that figure, and the augmented equilibrium equations would be

###### = >2«Ί

\PA" PB

Pib

###### L?_

-Plcl

![image 162](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile162.png)

- As before, the expression of q in system coordinates is quite arbitrary.


0/ \C

FIG. 7.5. An alternative release system for the portal frame of Fig. 7.3.

The inverse equations are

###### ~τα o o o rb

ΤαΗΉ PA

Pia Pib Pic.

PB

which may be written in the same way as before as

Pm= BSp+ B*0

The analysis now proceeds in exactly the same way as before. Although the matrices B0 and B have been replaced by the matrices B* and B* the final values for the internal forces and moments in the members and the joint displacements should clearly be the same, whatever system of releases is chosen.

So far we have introduced all the necessary releases at one particular point in the structure, allowing complete discontinuity

![image 163](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile163.png)

###### THE COMPATIBILITY METHOD 155

- at that point. This is perhaps the simplest way of making a rigidjointed structure determinate, but it is by no means the only way. Assuming our example to be a plane frame, we may achieve the same result by introducing three hinges, say at A, B and C.


iPyA

me ^ B

\

P..; Γ *

###### A i

###### ' b

h

a ■

' C

i

1 - *.

'

###### C

0

}

(a)

FIG. 7.6. A plane rectangular frame showing the positions of the releases.

- At a hinge translations are continuous but rotations are not, so that this system of releases corresponds to the introduction of three unknown self-equilibrating moment-pairs into the external loading vector, and the addition of three relative rotations to the displacement vector. If the members of the frame are horizontal and vertical, as shown in Fig. 7.6, then the equilibrium equations (7.14) may be written out in full as


![image 164](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile164.png)

- 0
- 1 0 0 0 0


- 1 0 0 0 0 1 0 0 0 0 0 0

- 1 0 0 0 - 1 0 0 - / - 1 1 0 0 0 1 0 0 0 1

0 0 0 0 1 0

0 0 0 0 0 0

(Pxl)a

###### PxA

(PylX

- PyA

MA

PxB

- PyB


(W2)a

- - 1 0 0 0
- - Λ - 1


(PxlX

- (Pyl)b (™l)b (Pxl)c
- (Pyl)c


###### L(w2)c.

These equations may be derived from the expressions for the matrices T and H given in sections 4.2 and 5.1, or may be obtained directly from statics. If we now denote the self-equilibrating moment pairs at A, B and C by ±qA, ±qB and ±qc the equilibrium equations may be augmented and written as

= [ " 0 - 1 0 10 0 0 0 0

'(Px2)a

0 0 0 0

0 0 0 0

0 1 0 0

0 0 0 0

0 0 0 0

1

0 - / 1 - 1 0 0 0 0 0 0 0 0 1

mB

- 0
- 1 0


<1A

QB

> 2 ) i .

These equations may now be inverted and written as

![image 165](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile165.png)

###### THE COMPATIBILITY METHOD 157

Ml

- -Ml
- -1/A 0 1/A
- -Ml 1 i// 1/A 0


0 0 0 - 1 0 1/A 0 0 0 1 0 -1/A 0 0 0 0 0 0 0 1 0 0 0 -1/A 0 0 0

- 0 "I
- 1/A


1//

[7ΆΛ~]

KPx2)a

0 0

0 1 0

0

0 i// 0 i// 0

- -1/A 0 0

- 0

-1/A

- 1 J




Ml

0

rriB

-Ml

\qA

0 0

\QB

0

(mac

Lqc j

These equations may easily be checked by statics. The coefficient matrix may now be divided into the matrices B0 and B, the division being indicated by the dotted line. The remainder of the analysis proceeds as before, the compatibility conditions being the continuity of rotation at the releases.

The use of hinges rather than complete cuts in members has certain numerical advantages in the manual analysis of hyperstatic rigid-jointed frames. The matrix B'FmB is often better conditioned, and the effect of inaccuracies in the calculated values of the release moments is less. These advantages, however, are obtained at the cost of additional complication in the inversion of the augmented equilibrium equations. As we have seen in this example, the inversion of the augmented matrix C+ has to be done in terms of individual scalar coefficients, whereas when complete cuts are used it is possible to work entirely in terms of the member T and H matrices. The known form of the matrix

- C+ * in the case of tree structures simplifies the work considerably, and although this may be at the cost of less well conditioned matrices a digital computer usually works with sufficient significant figures for conditioning problems not to be serious. The problem of ill-conditioning is discussed further in section 9.2.


###### 7.3. General Features of the Compatibility Method

We now consider the compatibility method in more general terms, and discuss its relation to the equilibrium method described in chapter 4.

![image 166](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile166.png)

###### 158 MATRIX METHODS OF STRUCTURAL ANALYSIS

As we have seen from the examples, both the equilibrium and the compatibility methods use the equations of joint equilibrium, which we have written in the form

P = Cpm (7.19) The equilibrium method merely uses the matrix C to transform the matrix Km, and is not concerned with whether C is singular or not. The compatibility method, on the other hand, transforms C into a non-singular matrix C+, which it then inverts. This transformation is effected by introducing sufficient discontinuities (i.e. releases) into the structure to make it determinate, and considering the self-equilibrating force systems which act at these discontinuities as external loads. The first problem which faces the analyst when using the compatibility method, therefore, is to decide on the number and positions of the releases.

The number of releases required to make a structure determinate is often known as the degree of indeterminacy of the structure. In most civil engineering structures this can be found by inspection, and for plane and space trusses with pin-joints there are well-known rules which give the degree of indeterminacy in terms of the number of members and the number of joints. For a general account of the problem of finding the degree of indeterminacy of a structure the reader is referred to Morice (Morice, 1959), and Henderson and Bickley (Henderson and Bickley, 1955).

It is relatively easy to calculate the degree of indeterminacy for frames in which all the joints are rigid. We merely introduce sufficient cuts in the members to convert the frame into a tree structure, which we know to be determinate. Each cut introduces six releases into a space structure or three into a plane structure, so that the degree of indeterminacy is simply six (or three) times the number of cuts. Alternatively we may argue that in the line diagram of a tree structure there are no closed paths or rings. A hyperstatic structure, on the other hand, always has a number of rings, each of which must be cut somewhere to make it into a

![image 167](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile167.png)

THE COMPATIBILITY METHOD 159

tree structure. Hence the degree of indeterminacy is equal to six (or three) times the number of independent rings in the original structure. It may be noted here that the foundations must be included in the structure—if a rigid-jointed structure has two points of foundation attachment, then this constitutes a ring. The frame shown in Fig. 7.7a, for example, has four independent

iininnuumiihi

Trr

7777777777

777777777777777777Γ (b)

(0

(a)

FIG. 7.7. A rigid-jointed frame showing two alternative release systems.

rings, and has therefore 12 or 24 degrees of indeterminacy, according as to whether it is treated as a plane or a space frame. It may be converted into a tree structure by the introduction of four cuts, whose positions may (with some restrictions*)·) be chosen arbitrarily. Two possible systems of releases are shown in Figs. 7.7b and 7.7c.

A more difficult type of structure to deal with is one with some joints rigid and some joints pinned. One way of tackling such a structure is to temporarily make all the pin-joints rigid, and find thé degree of indeterminacy of the resulting structure by counting the number of independent rings in the manner described above. If we subtract from this number the number of

- t The restriction on the positions of the cuts is that they must break all the


rings—otherwise they would reduce the structure to a combination of a hyperstatic structure and a mechanism.

![image 168](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile168.png)

###### 160 MATRIX METHODS OF STRUCTURAL ANALYSIS

additional constraints introduced by making the pin-joints rigid we obtain the degree of indeterminacy of the original structure.

While it is relatively easy to determine the number of releases required to make a given structure determinate, it is difficult to give rigid rules for choosing the positions of the releases. The characteristics of a good set of releases are :

(a) The numerical work should be as simple as possible. In other words it should be easy to find the matrices B0 and B, and these matrices should if possible contain a large number of zeros.

- (b) The matrix B'FmB should be well-conditioned, in order to

avoid trouble during the inversion process.

- (c) The system of internal forces and moments induced by the


release loads q (the system Bq in (7.21)) should be small compared with the forces and moments induced in the released structure by the applied loads (the system B0p). This reduces the effects of inaccuracies in the calculation of q.

Having decided on the release system to be used we add the selfequilibrating load-pairs ±ql9 ±q2, ···> associated with the releases to the applied load vector, at the same time adding appropriate rows to the matrix C appearing in (7.19). Thus we obtain an equation which we write

p] = C+ Pm (7.20) qj

Inverting C+ we obtain the expression P qj

Pm=C +

which we write as

pm = B0p + Bq (7.21) Equation (7.21) is merely an alternative form of the equilibrium conditions (7.19), the internal forces and moments pm being

![image 169](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile169.png)

###### THE COMPATIBILITY METHOD 161

expressed in terms of the applied loads p and certain arbitrarily chosen internal forces and moments q. In many problems, of course, it is straightforward to write down the equations in this form directly, without formally constructing the matrices C or C+. The matrices B0 and B have as many rows as pm has components. B0 has a column for each component of the external

- load vector p, and B has a column for each component of q.


The product B0p gives the internal load system produced in the structure when all the release load-pairs are zero, while the product Bq represents the self-equilibrating internal load system corresponding to the release load-pairs alone.

Corresponding to (7.21) we have the relationship between displacements and deformations, which we write as

rd" —"B'ol

###### _B'J

or as d = Bf0em; u = Bfem. The displacement vector d represents the displacements of the points of application of the known external loads, while u represents the relative displacements at the releases.

If we consider a load system in which q is zero then we may find

the corresponding member deformations e^} = Fmp^) = FmB0p, and hence the corresponding relative displacements at the releases

u(0) _ B'FmB0p. We now find the value of q which will produce displacements at the releases which are equal and opposite to those produced by the applied loads. The displacements produced at the releases by the loads q acting alone are u(1) = B'FmBq, so that if u(0) + u(1) = 0 it follows that

q=-(BTmB)-1B'FmB0p (7.22)

Substituting for q in (7.21) we find the true internal loads pm, and the displacements follow from the equation d = Boem = BOFmpm. It will be noticed that in calculating the displacements d from the internal loads we only need the matrix B0,

![image 170](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile170.png)

###### 162 MATRIX METHODS OF STRUCTURAL ANALYSIS

which relates the internal loads to the known external loads in the determinate structure.

One of the most interesting things about the compatibility method is the way in which the matrix B'FmB, which is the flexibility matrix of the structure as measured at the releases, resembles the matrix C KmC, which is the stiffness matrix of the structure as measured at the joints. Consider, for example, the release system shown in Fig. 7.7b. Here we have four independent rings, with release displacements ui9 u2, w3, »4 and self-equilibrating release load-pairs ±qu ±q2> ±^3, ±£4 as shown in Fig. 7.8.

###### r

###### Φ -?,A <nA

D

.F

~^ E

###### J\

UllllUJHIIUIilll III llliljll III

FIG. 7.8. The release load-pairs associated with Fig. 7.7b.

The »'s are expressed in terms of the <fs by the linear equation

- u = BfFmBq, which in this case may be written as


"1 (7.23)

###### = f n

9l 92

Fl3 F23 F33

F14' F24 F34

*12

###### F 22 F32

- «2
- «3 M4


^21

F3, F*.

- 03
- 4U


F*s

^44

^42

![image 171](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile171.png)

THE COMPATIBILITY METHOD 163

We now consider the detailed structure of the matrix appearing in (7.23). In particular we shall direct our attention to the third row, whose coefficients give us the relative displacement w3 of the points C and F due to the various q's. The leading diagonal sub-matrix F33 gives us the displacement due to the load-pair qz applied at C and F. The only members affected by this load-pair are the members comprising the ring FEABC, and the flexibility matrix of this ring may easily be found from the analysis in section 5.5. From equation (5.20) we obtain

^33 = H'BCF'ABH'BC + F'BC + H'EFF'AEH'EF + F'EF

Applying the same process to the other rings we see that in general each leading diagonal element of the flexibility matrix BfFmB is equal to the sum of the flexibilities of the members making up the corresponding ring. This may be compared with the fact that in the stiffness matrix CKmC of a structure each leading diagonal element is the sum of the direct stiffnesses of the members meeting at the corresponding joint.

If we now look at the off-diagonal elements of the third row, we see that the relative displacement of the points C and F due to the load-pair q2 is caused entirely by the strain induced in the member BC, this member being the only one common to rings 2 and 3. Applying the analysis given in section 5.5 to the composite member BCD we find that this displacement is equal to-FBCH'CDq2> so that we have-F32= F'BCH'CD. Similarly the contribution to u3 from the load-pair q4 is caused entirely by the strain in member AE, this being the only member common to rings 3 and 4. It is easy to show that F34 =-HEFF'AE. Finally we see that F31 must be zero. For rings 1 and 3 have no common member, and therefore no strains are caused in the members of ring 3 by any system of loads in ring 1. Applying the same analysis to the other rings we see that in general an off-diagonal element in the flexibility matrix depends on the flexibility of the member (or members) common to the two corresponding rings. If the rings have no

![image 172](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile172.png)

###### 164 MATRIX METHODS OF STRUCTURAL ANALYSIS

members in common then the element is zero. This may be compared with the fact that in the stiffness matrix of a structure an off-diagonal element is a function of the stiffness of the member connecting the two corresponding joints, and is zero if the joints are not directly connected by a member.

It follows that for the release system shown in Fig. 7.7b equation (7.23) is actually of the form

= F n F12 0 0

###### Γ«ι"

- 01
- 02


^21 f 2 2 ^23 0 0 ^32 ^33 ^34

« 2

" 3

0 0 F43 F.4 4J

L«4_

$4.

Like the stiffness matrix of a structure, the flexibility matrix tends to be "banded" in form, having its elements grouped round the leading diagonal. As we shall see in section 9.4, this feature has considerable computational advantages. The banded nature of the flexibility matrix depends on the arrangement of the rings, and this in turn depends on the positions chosen for the releases. For example, if we had chosen the system of releases shown in Fig. 7.7c the four rings would be as shown in Fig. 7.9. A load applied at one release point would produce displacements at all the others, so that there would be no zeros at all in the flexibility matrix. It follows that it is desirable to choose release systems in such a way that the rings are as independent of each other as possible.

###### 7.4. Axial Forces in Rigid-Jointed Frames

Because of its systematic nature the equilibrium method described in chapter 4 is easily programmed for a computer. The systematic nature of the analysis is due largely to the fact that all the joints in a given structure are treated as having the same number of degrees of freedom—two per joint in a pin-jointed

![image 173](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile173.png)

plane truss, three per joint in a rigid-jointed plane frame, etc. This allows the same method of analysis (and, by implication, the same computer program) to be applied to many different types of structure. As a result of this approach the equilibrium method always includes the effects of axial strains in members, making no distinction between frames and trusses.

FIG. 7.9. The system of rings associated with the releases shown in Fig. 7.7c.

While it is useful to have a general method of analysis which is "exact" in the sense of including the axial strain effects, it would also be desirable to have an equally systematic technique which neglected these effects, and was therefore simpler and involved less computation. Unfortunately it is difficult to do this in the matrix equilibrium method without destroying the systematic nature of the method. It is computationally impossible to make the axial stiffness of a member infinite, and merely making it large achieves nothing in the way of simplification. In fact, as we shall see in section 9.2, this may lead to ill-conditioning of the load-displacement equations.

![image 174](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile174.png)

###### 166 MATRIX METHODS OF STRUCTURAL ANALYSIS

In the compatibility method, however, some simplification is possible. We cannot neglect axial forces entirely, since an axial force in one member may cause a shear force to appear in another. Thus in writing the equations of joint equilibrium p = Cpm, we must include axial forces in the vector of member end-loads pm. However, when the matrix C has been augmented and inverted we may drop the axial force components from pm, keeping the values of the other components unchanged. Hence we may write

pm = B0p + Bq (7.24)

where pm has no axial force components, and the corresponding rows have been omitted from the two matrices B0 and B.

While an infinite stiffness is a computational embarrassment, a zero flexibility is easily handled. Having dropped the axial force component from each member end-load appearing in pm it is natural to drop the axial strain component from each member deformation appearing in em. Thus each member flexibility matrix becomes a 2 x 2 matrix in the case of a plane frame, or a 5 x 5 matrix in the case of a space frame. It is clear that this procedure does not affect the expressions for the other components of em—it merely eliminates the calculations associated with the axial strain components, which we are assuming to be zero.

The expressions for the displacements at the joints and the releases are still d = BOem, u = B'em, where B0 and B are the reduced matrices appearing in equation (7.24). Dropping the rows from B0 and B which are associated with axial forces eliminates the corresponding columns from Bf0 and Bf, and it is precisely these columns which correspond to the zero axial strains which we have omitted from em. The remainder of the analysis is formally the same as that given in the previous section. In the case of a plane frame the overall result is a reduction of a third in the number of rows in the matrices B0 and B, and a reduction of over 50 per cent in the number of coefficients in the member

![image 175](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile175.png)

flexibility matrices. A similar technique may be employed in cases where a member can be regarded as infinitely rigid in bending.

7.5. A Derivation of the Compatibility Equations by Virtual Work

In the preceding sections the equations of the compatibility method were developed by considering an imaginary physical process in which a structure is cut at certain points and the gaps then closed by the application of suitable forces. Although this approach is valuable in providing a physical background to the analysis it is not necessary, and the method may be made more general by arguing in the following manner.

In the presentation of the method given in previous sections the first part of the analysis is concerned with the inversion of the matrix C appearing in (7.19). This is done by the addition of extra rows of coefficients to C, and the addition of a corresponding vector q to the vector of applied loads. Now from a mathematical point of view all that matters about these extra rows is that they should make the augmented matrix C+ non-singular. In other words they must be linearly independent of the existing rows of C and of each other, but otherwise they may be chosen arbitrarily. In practice it is natural to make these extra rows as simple as possible, striving at the same time to make the matrix C+ reasonably well conditioned.

If the extra rows are added to C in this manner then the unknown vector q becomes purely a mathematical convenience, and its components do not in general correspond to any particular forces and moments in the structure. However, this does not affect the inversion of equation (7.19), and we may still express the member end-loads pm in terms of the applied loads p and the vector q in the form

###### Pm = B0p + Bq (7.25)

![image 176](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile176.png)

###### 168 MATRIX METHODS OF STRUCTURAL ANALYSIS

Equation (7.25) defines all possible systems of internal loads pm which satisfy the equilibrium conditions (7.19). In particular, if we put q = 0 the system p^} = B0p is statically equivalent to the applied loading. It follows that if we give q an arbitrary value, say qu then the load system Pm} = Bfli *s essentially self-equilibrating.

We now consider the effect of a virtual displacement of the joints of the structure. In contrast to our previous approach we introduce no releases, and require the virtual displacements to satisfy all the compatibility conditions. Since we are concerned with linear small-displacement theory we may choose our virtual displacements to be the actual displacements of the joints under the load system p. Let the vector of member deformations associated with these displacements be em. Then since the system ρ^} is self-equilibrating it follows that the work done by it during a virtual displacement is zero, so that we have (p^/e^, = qi1Bfem = 0. Since this equation holds for any arbitrary value of qx it follows that

Bfem = 0 (7.26)

Now we know that the vector em is given by em = Fmpm = Fm(B0p + Bq), where the symbol q in this equation represents the value associated with the actual system of internal loads. Hence we obtain BiFm(B0p + Bq) = 0, which agrees with (7.22).

This analysis shows that while the introduction of an unknown

- load vector q is essential to the compatibility method, it is not necessary for the components of q to represent particular forces and moments in the structure, nor is it necessary to relax the conditions of displacement compatibility by introducing releases at specific points.


![image 177](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile177.png)

###### 7.6. Combinations of Release Systems

In the last section we derived equation (7.26) by evaluating the work done by an arbitrary self-equilibrating load system during the deformation of the structure and equating it to zero. From this equation it follows that the internal forces and moments in the structure must satisfy the condition BfFmpm = 0, and we may, if we wish, give this equation physical significance by regarding it

- as the condition of continuity at the releases. It is natural to


proceed from this equation by substituting for pm from equation (7.25), but it is equally valid to use an expression derived from a quite different release system. If we have two alternative release systems for a structure, as in Fig. 7.7, we can obtain two alternative expressions for pm, which we may write as

pm = B(0fl)p + B«VÛ) (7.27) pm = B<0*>p + B<»q(» (7.28)

Either of these expressions may be used to define the complete set of load vectors pm which satisfy the equilibrium equations. We may apply the analysis of the previous section to (7.27) and obtain the condition (B(a))iFmpm = 0, and then, if we wish, substitute for pm from (7.28). Thus we obtain (B(a))'Fm (B<>b)p + B(b)q(f,)) = 0, which we may solve for q(b), finally obtaining the internal forces and moments from (7.28).

The above analysis is an example of what is known as a mixed system analysis. The following technique, which is based on very much the same kind of idea, has some practical value when the calculations are carried out by hand. Referring to equations (7.27) and (7.28) we first of all note that the two systems Bft°p and B(0d)p are both statically equivalent to the applied loading. Their difference is therefore a self-equilibrating system. But we know that any self-equilibrating set of internal forces and moments can be expressed in the form B(fl)q(e) by a suitable choice

![image 178](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile178.png)

###### 170 MATRIX METHODS OF STRUCTURAL ANALYSIS

of q(a). Thus we may write (7.27) in the form

###### Pm = B(o6)p + (B<0"> - B{f>)p + B<-)q<"

and by a suitable "change of origin" we may include the term (B(0a) - B(0fe))p in the term B(e)q(fl). Thus we may write

Pn, = B<0*>p + B<*>q (7.29)

and still obtain a correct analysis. For the internal load vector pm defined by (7.29) satisfies the equations of equilibrium, and by a suitable choice of q may be made to take any value consistent with those equations.

From this analysis we see that we may obtain the correct set of internal forces and moments in a structure by using the selfequilibrating system B(a)q in conjunction with any system of internal forces and moments B^b)p, the only condition on this system being that it is statically equivalent to the applied loads. Thus one may choose the simplest possible system equivalent to the applied loading, and then use any convenient self-equilibrating system for the remainder of the analysis.

Corresponding to the equilibrium equations (7.27) and (7.28) we have the compatibility equations

###### d==(B<?>)<em d = (B?>)'em

It is clear that the joint displacements of a structure can be found from any B0 matrix once the member deformations are known. All that matters is that the system B0p should be statically equivalent to the applied loads.

The mixed system methods described in this section have certain advantages when the calculations have to be done by hand, but when a computer is available the more straightforward approach involving only a single release system is probably the best. For some examples of mixed system analyses the reader is referred to the book by Hall and Woodhead (Hall and Woodhead, 1967, Second Edition).

![image 179](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile179.png)

###### 7.7. The Collapse Load of a Rigid-Plastic Structure

We now consider a problem which at first sight appears to have little connection with the other sections of this chapter—the calculation of the collapse load of a structure under ideal rigidplastic conditions. We shall show that this problem can be attacked very conveniently by the compatibility approach, and that it can be reduced to a standard problem of matrix theorythe so-called "linear programming problem" discussed in section 2.7. This reduction was first demonstrated by Foulkes (Foulkes, 1954) for the related problem of plastic minimum weight design.

In calculating the rigid-plastic collapse load of a structure we assume that the elastic deformations of the structure are insignificant compared with the deformations caused by plasticity.f In other words we imagine that the structure does not distort

- at all until sufficient plastic regions have formed to allow it to behave as a mechanism. We also make the following simplifying assumptions about the plastic behaviour of the materials forming the structure.


- (a) In the case of a member which yields in tension or compression we imagine that the member behaves elastically for axial forces p in a range — pc to +pt, and that further plastic deformations occur at constant tensile or compressive load. In practice, of course, the compressive limit — pc maybe a buckling load rather than one causing plastic yielding, but this does not affect the behaviour of the structure as a whole. The general form of the relationship is shown in Fig. 7.10a.
- (b) In the case of a member of a rigid-jointed frame in which yield occurs in bending we imagine that the member behaves elastically until the moment m at some point reaches a value ±mp, where mp is termed the plastic moment of resistance of the member. At this point a plastic hinge appears, the parts of the structure on either side of the hinge being able to rotate relative


t For a full account of the rigid-plastic theory of structures the reader is referred to Neal (Neal, 1963, Second Edition).

G

![image 180](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile180.png)

to each other without change in the resisting moment. The plastic moment of resistance of a member may depend on the axial force which the member carries, but we shall assume here that it is a known quantity. If a member of a structure carries no lateral loading at points along its length then the largest moment in the member will always appear at one or other of the ends, so that in these circumstances the plastic hinges will also occur at the ends.

Axial force p E nd moment m{ or mz

###### ,

P,

Compression

Extension

"Pc

(o) (b)

FIG. 7.10. Ideal rigid-plastic behaviour of (a) a bar under axial force, (b) a beam under end-moments.

If it is suspected that due to lateral loading a plastic hinge may appear at some point along the length of a member then we treat this point as a "joint" and consider the member as two separate members. Thus the relationship between the end-moments and the end-rotations of a member has the general form shown in

- Fig. 7.10b. The problem which we want to solve may now be stated ex-


plicitly as follows. Given a structure under known applied joint loads p, what is the factor λ by which these loads should be multiplied in order to convert the structure into a mechanism and thus cause collapse? In the case of a determinate structure the problem is trivial, since the internal forces and moments will increase in proportion to A, and collapse will take place as soon

- as the yield condition is reached at some point. In the case of a


![image 181](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile181.png)

###### THE COMPATIBILITY METHOD 173

hyperstatic structure, on the other hand, the appearance of plasticity has exactly the same effect as the insertion of a release, and it is not until sufficient releases have been inserted to convert the structure into a mechanism that collapse occurs. On the point of collapse the structure is determinate.

By definition we have, at the point of collapse, a system of internal forces and moments which can just remain in equilibrium with the external loads λρ without violating the yield conditions (—pc < p < pt or — mp < m < mp, as appropriate) at any point in the structure. For larger values of λ no such system exists. The problem is therefore to find the largest value of λ for which a system of internal forces and moments exists which satisfies both the equilibrium equations and the yield inequalities.

The general features of the analysis may be illustrated by considering the simple pin-jointed truss discussed in section 7.1. It will be recalled that in that section we took the equations of joint equilibrium (7.3) and transformed them into equations (7.5), expressing the internal forces in the bars in terms of the known external joint loads and the unknown "redundant" force q. If we consider the case where the load system p is given by

PxA = 1 PyA = 2 PxB = PyB = Q

then for a loading λρ equation (7.5) becomes

i i/V2]

= " 3 1/V21

rii

###### ΓΑ" 2/1

= "1 0 0 0

(7.30)

Pia Plb Pic Pia Plr.

###### U\

###### - V 2 - 1 0 l/V'2 1

-V2 - 1

o 1/72 0 1/V2 0 -1 J

Lg.

0 1/721 0 - l j

_0

If each bar yields at a compressive load pc = 2 and a tensile load pt = 4 then the yield conditions — 2 ^ p2i\ ^ 4 (/ = a, b, etc.)

![image 182](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile182.png)

may be combined with equation (7.30) to give

###### 3 1/V21 m ^ Γ4Ί (7.31)

###### «; "4]

###### i/V2"

Γ1"

###### u.

- - 1 VN/2

!/v'2

- - 1


4 4 4 4 2 2 21

0 0 0

- 3

l/V'2

1

0 0 0

1/V2

###### i/V2

12

1

###### J-\

Thus the problem is reduced to maximizing a linear function of a set of variables (in this case simply the function y = λ) subject to the linear inequalities (7.31), and this is precisely the linear programming problem discussed in section 2.7, for which standard computer techniques (and programs) are available. In this example graphical solution is possible and gives λ = 1 + yjl.

Exactly the same procedure may be followed in the case of members for which yield occurs in bending. For a plane rigidjointed frame we may follow the analysis given in section 7.3 and define a suitable set of release load-pairs q. Thus we obtain the joint equilibrium equations (7.20) in the form

which on inversion gives

Pm = c;1fAp

q

![image 183](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile183.png)

###### THE COMPATIBILITY METHOD 175

Since p is assumed to be known we may combine the appropriate multiples of the columns of C+1, as we did in (7.30), and write the result in the form

(7.32)

We now write down the yield conditions for each member. Although the vector pm consists merely of the load vectors at end 2 of each member, the other end-moments may easily be obtained by statics, the relationship for each member being

(7.33)

mt"

###### -1]

- "0 .0

- L 0

\Px2 Py2

lj

m2_

Lm2

If we denote the complete set of end-moments for the structure by mm we may write equations (7.33) for all the members in the symbolic form

m, = Apm = AD[A (7.34)

The yield conditions — mp ^ m m2 < mp for all the members may be written symbolically as — mp ^ mm < mp, and combining these conditions with (7.34) gives the system of linear inequalities

AD AD mr

Once again the problem is to maximize the function y = λ subject to a set of linear inequalities. The standard computational process for solving the linear programming problem will also give the components of the vector q associated with the solution, so that the internal loads and the positions of the plastic hinges can be

![image 184](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile184.png)

determined. The method may also be applied to structures in which some members yield in bending and some in tension or compression.

The collapse analysis of a structure may also be reduced to a linear programming problem by considering the alternative mechanisms of collapse. This procedure obtains the final value of λ as a lower bound, while the process which we have described obtains it as an upper bound. In cases where the elastic and plastic deformations of the structure prior to collapse affect the collapse load the problem must be treated by considering the gradual development of the collapse mechanism. A general iterative technique for dealing with such problems is described in section 10.5.

![image 185](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile185.png)

###### CHAPTER 8

###### Transfer Matrices

So far in this book we have been concerned with general methods of structural analysis which can be applied to a wide range of structural forms. As we have seen, these methods involve the manipulation of matrices whose size depends on the number of members or the number of joints in a structure. In the present chapter we discuss a method of analysing a particular type of structure which avoids the necessity of handling large matrices. Instead it proceeds by means of a series of matrix multiplications involving smaller matrices known as transfer matrices.

The type of structure which can be analysed by means of transfer matrices is one in which the joints are connected by a single chain of members. Examples of such structures are shown in Figs. 8.1 and 8.2—their essential characteristic is that if the joints are numbered sequentially then joint / is connected directly to joints J + 1 and / — 1, and possibly to a rigid foundation, but to no other joints. For a fuller account of the applications of transfer matrices the reader is referred to papers by Targoif (Targoff, 1947) and Leckie and Pestel (Leckie and Pestel, 1960).

###### 8.1. The Transfer Matrix of a Single Member

As in previous chapters, we shall use the symbols p and d to denote the load and displacement vectors associated with joints and with the ends of members. Thus our analysis applies equally well to plane and space structures, provided that the vectors and matrices involved are defined appropriately.

177

![image 186](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile186.png)

In section 5.1 we wrote the equilibrium equations of a single member in the form

Pl + Hp2 = 0 (5.2a) and in section 5.3 we derived the expression

d2 = Htdi+Fp2 (5.16) The latter equation gives the displacement d2 of end 2 of a member in terms of the displacement associated with end 1 and the deformation induced by the applied load p2. In section 5.3 we used these equations to derive expressions for the end-loads pu p2 in terms of the end-displacements dl9 d2, these expressions being the ones appropriate to the equilibrium method of analysis. We now write them in an alternative form, in which the displacement and load at end 2 are expressed in terms of the corresponding quantities at end 1.

From equations (5.2a) and (5.16) we obtain p2 = —H~ipi and d2 = Htdl — FH~1pl9 which may be written in the form

(8.1)

###### Pi 0 -tf-'JLPiJ

The combinations of displacements and loads A

d2

and

are

Pi

Pi

referred to as the state vectors of the two ends of the member, while the matrix which relates them is called the transfer matrix of the member. We shall write (8.1) as

s2 = Gsx (8.2) It may be noted that there is the same lack of symmetry here as occurred in our definition of the equilibrium matrix H in section 5.1. Our definition of G in the form which gives s2 in terms of st is purely arbitrary. If we wish to express st in terms of s2 we have sx = G~1s2, where it is easy to show that

G-1 = r(H')"1 -(Hr)_ 1Fl

0 -H

![image 187](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile187.png)

TRANSFER MATRICES 179

In the case of a straight uniform member whose end-loads and end-displacements lie in a plane the detailed coefficients of the transfer matrix G may be derived by substituting the appropriate expressions for the H and F matrices given in sections 5.1 and 5.3 into equation (8.1). Thus we obtain

0 Û/6EI L2\2E\ 0

0

- -L/EA 0 0
- - 1 0 0


1 0 0 0 1 L 0 0 1 0 0 0 0 0 0 0 0 0

<5*i]

dx2

- -L2I2EI
- -LI El 0 0
- - 1


*,t 0i

02

Pxl Pyl

Px2 Pyl

- 1 L

_ ^ l J

m2J

the inverse form being

0 L3/6£7 ■L2I2EI 0 - 1 - L

0 1 0 0 0 0

- 0

-L

- 1 0 0 0


= "1 0 0 0 0

- -L/EA 0 0
- - 1 0 0


ôxl~

L2j2El

###### <V

- -LI El 0 0
- - I


θ2

öl

Vx\

Vx2 Pyl

Pyl

.0

.™2.

« 1 .

To transform equation (8.1) into system coordinates we merely apply the rules given in section 5.4 for the transformation of H and F matrices. Thus we obtain equation (8.1) in the form

ÏH" - F A ' - 1 1 (8.3)

d'2 Pii / i J

0 -f/'_1 where H' = THT'andF' = TFT'. This equation maybe written as

si = G's'i (8.4)

![image 188](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile188.png)

180 MATRIX METHODS OF STRUCTURAL ANALYSIS

###### 8.2. An Example of the Use of Transfer Matrices

For our first example of the use of transfer matrices we consider the built-in arch shown in Fig. 8.1. We imagine that the transfer matrix for each section of the arch is known in system coordinates—as we have seen, this merely implies that we know the F, H and T matrices of the sections. As usual, the quantities PA> PB, ..·, denote known external loads, which may include moment components as well as forces.

FIG. 8.1. Example of a built-in arch.

At the left-hand end of section a we have the state vector

01 r0\

[fia.

where r0 is the as yet unknown reaction at the support O. Multiplying s\a by the transfer matrix for member a we obtain

*2. = G>'i« (8.5)

We now have to move from end 2 of section a to end 1 of section b. The compatibility and equilibrium equations

- at joint A are simply d[b = d'2a9 p'lb 4- p'2a = PA- In transfer


![image 189](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile189.png)

###### TRANSFER MATRICES 181

matrix form this becomes \i\b IPit.

###### + "°1

= 7

01

\à'ià

###### -'J

.0

[Pia.

###### .PA\

which may be written as s'ib = Us'2a + sA. Substituting for s2a from (8.5) this becomes s[b — UG'as[a + sA. (It may be noted that pre-multiplying a G matrix by U merely reverses the sign of the sub-matrix — H'"1 which appears in the second row.)

In the same way we have s\c = VGbs\b + sB

= UG'hVG'as\a + UG'bsA + sB

Progressing in this manner along the whole length of the arch we finally obtain

8'2x = {G'xUG'w...G'bUGWlM

+ (G'XUG'W ... G'b)sA + ... + G'xsw (8.6)

Since all the state vectors sA9 ...,sw are known we may add up all the terms in equation (8.6) associated with these vectors to form a single known vector which we shall write simply as c. Thus equation (8.6) may be written as

###### Gs'i. + c (8.7)

It should be realized that although the matrix G and the vector c relate to the whole arch they are no larger than the individual transfer matrices and state vectors associated with the separate sections.

We have already introduced the boundary conditions at end O by writing

*Ί„=Γ01

r o j

![image 190](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile190.png)

###### 182 MATRIX METHODS OF STRUCTURAL ANALYSIS

We now introduce the boundary conditions at end X by writing

###### 0

If we split the matrix G into sub-matrices G n , G12 etc., we may write equation (8.7) in the form

###### Ol = rGn Gi3 0

###### +

###### G22jl/r>

or as

0 = G12ro + C! rx = G22r0 + c2

(8.8) (8.9)

Equation (8.8) may now be solved for the unknown support reaction r0, after which equation (8.9) (which is merely the overall equation of equilibrium for the arch) gives the other reaction rx. Once r0 is known, equation (8.5) and the equations that follow it may be used to find the state vector (i.e. the displacement and the internal forces and moments) at any point in the arch. If the arch is a member of a larger structure then the method which we have described provides a convenient systematic way of finding the equivalent fixed-end forces and moments needed in the analysis of the complete structure.

In this particular example equation (8.8) might have been derived by the use of the compatibility method described in the previous chapter. Our present analysis corresponds, in fact, to an application of the compatibility method in which r0 is chosen

- as the unknown load vector q, and the releases are introduced in the form of a cut at joint X. Equation (8.8) is merely the compatibility condition which states that the displacements at these releases must be zero. However, the method of transfer matrices is not in general just a restatement of the compatibility method in a different notation. As we shall see in the next section, it can be applied to cases where intermediate supports give a structure a


![image 191](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile191.png)

###### TRANSFER MATRICES 183

high degree of redundancy, without any increase in the number of equations which have to be solved.

Although our analysis was developed for an arch with built-in ends equation (8.7) is quite general ^nd may be used to obtain solutions for any other type of support. For example, a foundation settlement at X or an initial "lack of fit" due to temperature would merely result in s'2x having a non-zero displacement component, and equation (8.8) having a corresponding non-zero term on the left-hand side. If the arch were a plane one and the joints

- at O and X were pinned instead of being rigid then the state vector


s\a would still have three known components (two zero translation components and a zero moment) and three unknown components (two forces and a rotation). Similarly the state vector s2x would also have three known components, so that we should have

###### s2x ~ ' °1

Γ 0"

0

0

Ox

00

rxX\

rxO

ryO

ryx\

###### L °.

###### _ 0 J

Thus the unknowns 0O, rx0, ry0 could be obtained by abstracting the first, second and last scalar equations (corresponding to the zero components in s2x) from the vector equation (8.7). The remaining equations could then be used afterwards to find the corresponding unknowns Θχ, rxX, rfyX. A similar procedure could be adopted in the case of a joint mounted on rollers.

###### 8.3. The Effect of Intermediate Supports

We now consider the structure shown diagrammatically in

- Fig. 8.2, in which each joint has a direct connection to a rigid


![image 192](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile192.png)

###### 184 MATRIX METHODS OF STRUCTURAL ANALYSIS

foundation as well as connections to adjacent joints. As before, we assume that the transfer matrices of the members b, c, ..., n are known in system coordinates, and that a known set of loads PA> PB> ···> PN (incorporating equivalent fixed-end forces and

moments where necessary) are applied at the joints A, B, ..., N. We denote the stiffness matrix of the stanchion supporting joint

- J by Kj. In other words, if joint / has a displacement dj then the load which the joint exerts on the end of the stanchion is given by K'jdj.


77777777777/77777777777777/ ΊΜΠΙΗΜΠΙ!;

FIG. 8.2. A structure consisting of a chain of members with intermediate supports.

As before, we start our analysis at the extreme left-hand end of the structure. Since there is no member to the left of the joint A we may write the state vector for the left-hand side of joint

A as sA__ = , where it is now the displacement components

###### L o J

of 5 which are unknown. The compatibility condition at joint A is simply d\b = dÄ9 while the equilibrium condition is p'ib + K'AdA = pAi K'AdA being the load applied by the joint to the stanchion supporting it due to the displacement dA. These two equations may be written in transfer matrix form as

I 0

###### + 0

d\lb

- J 0

Pit.

VPA\

or more briefly as s'lb = G'AsA^ + sA. It will be seen that the effect of the flexible support at A is to introduce the sub-matrix — KA into the matrix we previously denoted by U. While a joint which has no direct support can easily be dealt with simply by

![image 193](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile193.png)

making K' zero, the present analysis does not cover the case where one or more displacement degrees of freedom are completely restrained, since this would correspond to some of the elements of

- K' being infinite. This problem is discussed in section 8.5. We may now use the transfer matrix of member b to obtain


s2b> i.e. s2b = Gbs[b — GbG'AsA- + G'bsA. The compatibility and

equilibrium conditions at joint B are d\c = d'2b, p[c + p'2b + K'BdB = pB, which may be written in the same way as before as

###### ά\Λ = 0 <*;lb + 0

iP'ici L~K'B -!\lP2bi iPei

or as s'lc = GBs2b + sB. Thus we obtain s'lc = GBGbGAsA_ + GBGbsA + sB, and proceeding along the structure we finally obtain an expression for the state vector associated with the righthand side of joint N9 which we shall write as sN+. This expression is

s*+ = (G'NG'nG'M...G'BG'bG'A)sA_ +

+ (G'NG'HGM...G'b)sA+...+sN (8.10) As before, we may add up the terms containing the known vectors sA, ..., sN and write equation (8.10) in the form

###### - G 5 ._ + C (8.11)

We now apply the boundary condition at the right-hand end of the structure, which is simply that the load components of sN+ are zero. Splitting the matrix G into sub-matrices G11, G12 etc. in the same way as before we obtain equation (8.11) in the form

###### + «I

dN~ 0.

= "Gn G2l

G12l

\dA

###### G22J

###### Lo.

.«2

###### that is

*N= GlidA + Cl (8.12) 0 = G21dA + c2 (8.13)

![image 194](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile194.png)

###### 186 MATRIX METHODS OF STRUCTURAL ANALYSIS

It is now equation (8.13) which has to be solved for the unknown displacement dA. This is an "equilibrium" rather than a "compatibility" equation. Once dA has been found the state vectors at intermediate points may easily be derived by working along the chain.

8.4. A Comparison of the Transfer Matrix Method and the Equilibrium Method

The examples discussed in the two previous sections show that the method of transfer matrices has some of the characteristics of both the equilibrium and the compatibility methods. The final set of equations which have to be solved may be compatibility equations (as in (8.8)), or equilibrium equations (as in (8.13)). In the last example the matrix G was seen to be a product of both flexibility and stiffness matrices—flexibility sub-matrices appearing in the transfer matrices of the members and stiffness sub-matrices appearing in the transfer matrices of the joints.

The appeal of the transfer matrix method lies in the fact that the final matrix G is no larger than the individual transfer matrices associated with particular members or joints. It is therefore an attractive method for the structural analyst using a computer with a relatively small working store. It must be remembered, however, that equations such as (8.8) or (8.13) merely give the unknown components of the state-vector at the extreme left-hand end of the structure. To find the state-vectors at intermediate points one must either repeat the formation of the partial matrix products G'bG'A, G'BG'hGA, etc., or record them separately during the formation of the matrix G.

At the end of the previous section we stated that equation (8.13) was essentially an "equilibrium" equation, since it can be written

G2idA = pN+-c2 (8.14) where pN+ is known to be zero since there are no members to the

![image 195](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile195.png)

right of joint N. An equivalent (though not identical) equation for dA appears during the solution of the load-displacement equations derived by the equilibrium method, and it is interesting to make a rough comparison between the amount of numerical effort required by the two methods for the example of section 8.3.

In making this comparison we shall restrict our attention to the computation of the matrix G21, and the equivalent matrix which arises in the equilibrium method. These matrices are of the same size as the H' and F' matrices of the individual members—i.e. 3 x 3 for a plane structure and 6 x 6 for a space structure. The number of simple numerical operations involved in both the inversion of an n x n matrix and the multiplication of two n x n matrices is of order «3, while the addition of two such matrices requires only n2 operations. In comparing the two methods we shall therefore ignore matrix additions and regard matrix inversion and multiplication as involving roughly the same amount of numerical effort. We shall think of either of these processes as one "basic operation" when applied to the JFT, F' or K' matrices of the individual members. We shall assume that all the individual G' matrices required by the transfer matrix method and the K' matrices used in the equilibrium method are already available, and we shall not consider the numerical work involved in their formation.

Since we only need to compute the element G21 of the repeated product G = G^G^G^G^ GiGbG^ the most efficient procedure is to start at the right-hand end and compute only the first column of each matrix product. Thus we begin by evaluating the first column of the product G'hG'A, and if we do not count multiplication by 0 or / this requires two basic operations. We next compute the first column of the product G^G^G^ by pre-multiplying the result of the previous step by G> Again ignoring multiplication by 0 or / this requires only one basic operation. Multiplication by G'c now requires three basic operations and multiplication by Gi one basic operation, and these numbers are

![image 196](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile196.png)

188

MATRIX METHODS OF STRUCTURAL ANALYSIS

od

ξ •β

^ OQ O

^3 ^3 13

o o o

###### .- * * H

fc< w fc<

o o

^ cq υ ft« «^ ft,

![image 197](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile197.png)

###### TRANSFER MATRICES 189

repeated for each succeeding pair of member and joint transfer matrices. Thus the total number of operations required to compute G21 in this example is 12(1 + 3) + 1 + 2 = 51.

Turning now to the equilibrium method of analysis, we may use the rules given in section 4.3 to write the load-displacement equations of the structure in the form portrayed on p. 188, where (ΣΚ') indicates the sum of the direct stiffness matrices of the members meeting at a joint. These equations are symmetric, and may be solved very easily by the elimination process described in section 2.6.

We may start the process with the last equation, adding such multiples of it to the previous equations as will make all the elements in the last column apart from (ΣΚ')Ν equal to zero. Since all but one of these elements are zero already all we need to do is multiply the elements in the last row by —(Κ'^ηΦΚ')^1 and add them to the corresponding elements in the last row but one. Thus we take (K2i)n9 form -{Κ\2)η{ΣΚ%\K'2l)n, and add it to the sub-matrix (ΣΚ')Μ—it will be noted that the resulting submatrix is still symmetric. This involves three basic operations —an inversion and two multiplications. In practice we need not carry out the same operations on the sub-matrix (ΣΚ')Ν since we know that the expression (K'12)n - (Κ^^ΣΚ')^1 (ΣΚ')Ν is identically zero—we merely replace (K'12)n by a null matrix.

The same process may be repeated on the equation associated with joint M, and so on until (K'i2)b is eliminated from the first equation, three basic operations being required for each matrix equation. Thus the total number of operations required is 3 x 13 = 39—approximately 80 per cent of the number required in the transfer matrix method. It must be admitted that this comparison is an extremely rough one. We have equated matrix inversion with matrix multiplication from the point of view of effort involved, and ignored the operations which have to be carried out on the loading terms. However, the difference is sufficient to justify the statement that the equilibrium method is at least as efficient as the method of transfer matrices.

![image 198](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile198.png)

190 MATRIX METHODS OF STRUCTURAL ANALYSIS

At the beginning of this section we mentioned that the equations derived by the two methods, though equivalent, are not identical. The elimination process which we have described eventually reduces the first equation of (8.15) to a modified equilibrium equation for joint A9

K*AdA = pA+f(pB,...,pN) (8-16)

where K* is the sub-matrix which was initially (ΣΚ')Λ, and APB> ···> PN) represents the linear function of the applied loads which is added to pA during the elimination process. The matrix K* is symmetric, and represents the direct stiffness of the complete structure as measured at joint A. If the structure is a physically sensible one then K* is likely to be well-conditioned. Equation (8.14), on the other hand, is essentially an equilibrium equation for joint N, even though it is solved for the displacement dA. The matrix G21 is unsymmetric and represents the cross-stiffness between joints A and N, while the vector c2 represents a loading system equivalent to the actual applied loads as far as joint N is concerned. Such an equation may not be a "good" equation for determining the displacement dA, since if there is a very stiff support or a very flexible member at some intermediate point in the structure the equilibrium of joint N may be only very slightly affected by changes in the displacement of joint A. This point is discussed further in section 9.2.

The method of transfer matrices is very similar to the method often used in the numerical integration of ordinary differential equations when some of the boundary conditions are specified at one end of an interval and some at the other—the so-called "twopoint boundary-value" problem. In dealing with such a problem it is common practice to give arbitrary values to the boundary conditions which are unknown at one end of the interval. The numerical integration is then carried out using these values (along with the other known boundary conditions at that end) as starting values, and it is repeated with corrected values of the unknowns until the boundary conditions at the other end of the interval are

![image 199](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile199.png)

###### TRANSFER MATRICES 191

also satisfied. Here again one is determining the values of parameters associated with the solution at one end of an interval by applying conditions at the other. It is clear that serious numerical difficulties will arise if some of the solutions die away very rapidly, since whatever boundary conditions are assumed at one end these solutions will have become effectively zero by the time the other end is reached.

###### 8.5. Rigid Supports and Flexible Joints

As stated in section 8.3, the account of the transfer matrix method which we have given so far does not cover the case where a structure has a rigid support at some point along its length, since this corresponds to an infinite coefficient in one of the K' matrices. As mentioned in the last section, even a large finite stiffness may cause trouble by making the final matrix G illconditioned. In the same way a pin-joint at the end of a member represents an infinite flexibility and gives rise to an infinite coefficient in the corresponding F' matrix. We now describe a technique which may be used to overcome both these defects.

FIG. 8.3. Continuous beam with pin-joint at B and rigid supports at C and D.

We illustrate the idea by considering the continuous beam shown in Fig. 8.3, which is built-in to a rigid support at A and simplysupported at C and D. The latter supports are assumed to offer no rotational restraint, but to be infinitely stiff as far as vertical movement is concerned, while the pin at B is assumed to be incapable of transmitting a moment. The loading on the beam is taken to be equivalent to a vertical force pyB at B and moments mc, mD at C and D.

![image 200](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile200.png)

In considering this example we shall ignore longitudinal forces and displacements, so that each state-vector has only four components, being of the general form

Py

m

The appropriate member transfer matrices may be obtained from the expression given in section 8.1 for the transfer matrix of a straight uniform member by dropping the rows and columns associated with the axial force and displacement.

As usual we start the process at the left-hand end of the beam, where we have known (zero) displacement components and an unknown force and moment. Thus we write

- -L2I2EI~\
- -LI El 0
- -1 J


###### Γ °

###### Sin = (M/

= "1 L ÜI6EI 0 1 L2/2EI 0 0 - 1

(8.17)

- 0

PyA

- 1™A


###### (02). (Py2)a

_0 0 L

( « 2 ) . .

where pyA and mA are the unknown reactions at the support A. We now have to cross the pin at B, expressing slb in terms of sla. This presents no difficulty as far as vertical movement and vertical loading are concerned, since we have (ôyl)b — (ôy2)a9 and (PyiX + (Pyi)a = PB-> D ut w e ha ve no equation which will give us

( 0 ^ from (02)a. However, this lack of information about rotations is compensated by the fact that we have a known (zero) value for the moment at B, so that (m2)a = (mj,, = 0, and if we put this into equation (8.17) we see that it implies LpyA — mA = 0, as indeed is obvious from elementary statical considerations. In other words, the unknowns pyA and mA are not linearly independent, and it is therefore unnecessary to keep them as separate

![image 201](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile201.png)

###### TRANSFER MATRICES 193

variables during the remainder of the analysis. Thus we may combine the columns multiplying pyA and mA in equation (8.17) and write that equation as

- -L2/3£7]
- -L/2EI
- -1/L


###### Γ °"

= "1 L 0 1 0 0

v,i): (8.18) (ßl).

0

L.mA.

(Py2)a

o J

_0 0

(™2)α_

We have still not overcome the difficulty of defining (0^. We do this simply by introducing the discontinuity in rotation ΘΒ = (0^ - (02)β as an extra unknown into equation (8.18), in place of the quantity pyA which we have eliminated. Thus

- equation (8.18) becomes VyzV


- -L2/3£J 0]
- -LI2EI 0
- -1/L 0 0 Oj


Γ0 0 mA

= "1 L 0 1 0 0

(β2). (Pylia (m2)a.

###### UB

_0 0

We may now write the state-vector slb associated with the righthand side of the hinge as

+ " 0 "

###### Γ V,l\ ]

Γ(«,ι)»Ί

0

(Θ2\+ΘΒ

(Öl)» (Pyl)b

PyB

-(.Pylia

_ 0 .

L(mi)J

L (m2)a J

###### + ' ° Ί

-L2/3L7 0 -LI2EI 1

" 0 " 0 mA

Γ1 L 0 1 0 0

=

0

1/L 0 0 0

PyB

###### _ o J

lo 0

.0,.

![image 202](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile202.png)

We now multiply this equation by the transfer matrix of member b to obtain the state-vector s2b associated with the left-hand side of the support C. Having done this we are faced with very much the same kind of difficulty as we encountered at B. We have continuity of rotation (θ^ = (62)b and a straightforward moment equilibrium equation (m2)b + (^i)c = mc, but we have no equation giving the vertical reaction rc. We deal with this difficulty in the same way as before. We apply the condition (ôy2)b = 0 to obtain a relationship between mA and 0B, and we use this equation to eliminate one of these variables (say mA) from the expression for s2b. In place of this variable we put the unknown rc and then express the state-vector slc associated with the right-hand side of joint C in terms of the unknowns ΘΒ, rc and the known applied loads at B and C. Finally we multiply this expression for slc by the transfer matrix for member c, and derive equations for the unknowns θΒ and rc by applying the conditions of zero vertical translation and known moment associated with the joint D.

8.6. The Application of Transfer Matrices to Vibration Problems

In section 4.9 we saw that the application of the "equilibrium" method to problems of free undamped vibration leads naturally to the classical problem of finding the eigenvalues and eigenvectors of a matrix. We now describe an alternative method of finding natural frequencies of vibration which is applicable to those structures which can be analysed conveniently by transfer matrices. We illustrate the process by considering the problem of finding the natural frequencies and normal modes of transverse vibration of a straight continuous beam. An important practical application of this analysis is in the determination of the critical speeds of a turbine rotor.

Whatever the method used, the first step in the analysis is the replacement of the continuous distribution of mass by

![image 203](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile203.png)

TRANSFER MATRICES 195

"equivalent" concentrated masses and (possibly) rotational inertias (i.e. moments of inertia about a transverse axis).f It is obviously convenient if this is done in such a way that each section of shaft is uniform between mass points—the process is illustrated in Fig. 8.4.

### b-r-p-i

###### a-D

0

###### —*l i —k

s

.-77777 I ' ■ ιΎ7^77 ////,/

FIG. 8.4. An example of a vibrating system in which a continuous mass distribution is replaced by a series of concentrated masses and

inertias.

It may be noted in passing that the replacement of a continuous mass distribution by a series of concentrated masses necessarily results in the computed frequencies and vibration modes being somewhat in error. The size of the error is reduced by taking a larger number of mass points and increases with the number of the harmonic—the discrete system, of course, has only a finite number of natural frequencies, while the continuous system has an infinite number. A discussion of this problem has been given by Duncan (Duncan, 1952).

The method we adopt is essentially one of finding the harmonic exciting force necessary to maintain the system in vibration at an arbitrary frequency ω. While the basic idea of the method is similar to that introduced by Myklestad (Myklestad, 1944), the

|The more sophisticated technique mentioned in the footnote on p. 90 may also be used with transfer matrices.

![image 204](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile204.png)

use of transfer matrix notation makes the presentation considerably simpler. We assume that all loads and displacements vary sinusoidally with time, and since we are ignoring damping there are no differences in phase. Thus all state vectors have the general form

sin cot

and since the sin oot term multiplies all state vectors equally we shall adopt the practice common in vibration analysis of omitting it when writing down equations. Thus our state vectors represent amplitudes, not instantaneous values.

Having concentrated the mass of the system at certain points it is logical to treat the sections of beam between these points as weightless. Thus their transfer matrices are exactly the same as in the static case. The transfer matrices of the mass points, on the other hand, depend on the frequency ω. Consider the mass point / in Fig. 8.4, which has a support whose translational stiffness is kyJ and whose rotational stiffness is kBJ. Let the mass associated with J be M3 and the rotational inertia be /,. Then the compatibility equations at the mass point are simply

(ày2)j = (Öyl)k

while the assumption of harmonic time-dependence reduces the equations of motion to

(Pyl)j + (Pyl)* + kyJ(ôy2)j = MjCÛ2(ôy2)j

(m2)j + (mx)k + kej(02)j = Ijw2(e2)j

![image 205](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile205.png)

TRANSFER MATRICES 197 These equations may be written in transfer matrix form as

###### [(Μ,Ί

= 1 0

0 0

01 0 0

(Öyl)k

0 1 Mjco2 - ky] 0

###### (0Λ

(»2)>

- 1

(Pyl)k

(Py2)j

###### L(w2)J

-1J

0 Ij(û2 - k9J

0

(»>ΐ)ϋ.

or as slk = GjS2y

As in the case of a statical analysis we start with the statevector at the left-hand side of point A, which we write as

uyA

ΘΑ 0 0

where the displacement ôyA and the rotation ΘΑ at point A are unknown. We then progress along the chain in exactly the same manner as before. Eventually we obtain the state-vector at the right-hand side of point N in the form sN+ = GNGn GkGjGj

GAsA_, which may be written

%+ = G ^ (8.19) where the matrix product G is a function of ω. We now split up

- equation (8.19) into the form


P12 dA 0

PN+ LG21

and from this abstract the equation ρχ+ = G21dA. The quantity pN+ given by this equation represents the force and moment which are required at point TV to maintain the system in vibration

- at the chosen frequency ω, the amplitude of the vibration being


![image 206](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile206.png)

defined by the vector dA. At the natural frequencies pN+ is zero, so that we have C2idA = 0. Thus we have to find the values of ω which make G21 singular. It must be remembered that although this is basically an eigenvalue problem we shall not normally obtain G21 as an algebraic function of ω, but as a numerical matrix computed for a definite numerical value of . We shall, therefore, have to find the natural frequencies by evaluating |G21| for a series of values of ω and finding the zeros by a numerical root-finding process. Although this is mathematically a rather inefficient process compared with the classical eigenvalue approach, it is very suitable for the situation which often occurs in practice, where it is required to find out whether a system has any resonant frequencies within a particular frequency range. The method is also very convenient if it is required to find the response to a harmonic forcing term of known frequency.

The analysis can be extended to cases involving longitudinal and torsional vibrations merely by defining the transfer matrices in the appropriate way. It should be remembered, however, that the remarks made in section 8.3 about the possibility of the matrix G21 being ill-conditioned still apply. In cases where a support stiffness or a member flexibility is infinite the device described in section 8.4 may be applied in exactly the same way as for the static case.

![image 207](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile207.png)

###### CHAPTER 9

###### Computational Problems

As we have already stated, the systematic nature of matrix methods makes them ideal for use in conjunction with automatic computers. While this is not a textbook on computer programming it seems appropriate to describe here some of the problems which arise when analysing structures on a computer. Further information about the practical aspects of applying computers to structural work will be found in a recent report published by the Institution of Structural Engineers (1967, Second Edition).

The first part of this chapter discusses some of the general strategical decisions which must be taken before any detailed programming can begin. The second part is concerned with the problem of accuracy, and discusses the type of checks which are desirable when using matrix methods. The last part is concerned with the efficient handling of large matrices. As we have seen, the matrices which arise in structural analysis often have a high proportion of zero elements, and the non-zero terms are usually located near the leading diagonal. By taking advantage of these features it is possible to achieve considerable economies both in computing time and computer storage space. This is extremely important in the analysis of really large and complex structures.

###### 9.1· Single and Repetitive Problems

There are occasional problems in engineering which are so complicated that an "exact" solution can only be found by using an automatic computer. In such cases it is not a question of

199

![image 208](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile208.png)

making an economic comparison with methods of manual calculation, but of deciding whether the exact solution is really necessary. In most cases, however, the engineer has a choice between a traditional manual method and a solution by computer which, in a problem of structural analysis, will probably be based on one or other of the methods described in this book. Which alternative is the "best" depends to a large extent on whether the problem is single or repetitive.

We use the term single to denote a problem in which the production of numerical results means that the problem has been "solved" in the sense that no similar calculations will ever be required. A certain amount of repetition may be involved, but the number of repetitions is known in advance. This type of problem is characteristic of research work. The end-product of the calculation is usually a table of numbers, which may represent the values of a mathematical function, the solution of a differential equation, or standard solutions covering all practical parameter values of a particular engineering product.

If a computer program is prepared for such a calculation it will be of no further use once the results have been obtained. It must therefore pay for its creation during a relatively short working life. In these circumstances the comparison between automatic and manual methods is a straightforward one of total time and cost. In many cases the time spent actually running the program on the computer is so short that the question of computational efficiency is almost irrelevant—the time and cost of the computer solution are effectively the time and cost of developing and testing the program.

To construct a working computer program in the shortest possible time one naturally chooses a method which is based on standard mathematical processes for which routines already exist. Even if the method is "inefficient" in a mathematical sense the small amount of computer time needed to test the program may well mean that the total cost of the computation is less than in the case of a "better" method for which special routines would

![image 209](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile209.png)

###### COMPUTATIONAL PROBLEMS 201

have to be written. Thus in solving a structural analysis problem one would tend to use existing routines for all matrix processes, ignoring the fact that in some cases the simple form of a particular matrix could have been used to reduce the number of numerical operations carried out by the computer.

In solving single problems in structural analysis with the aid of a computer it is probably best to regard the computer merely as a machine which will manipulate matrices and solve equations. Thus the analyst himself transforms the problem into a series of matrix operations, and presents the data to the computer in the form of a series of vectors and matrices. In these circumstances the "program" is nothing more than a series of standard matrix routines arranged in the appropriate order, and as such is very easy to construct. The disadvantage of this approach is that the translation of the problem into matrix form has to be done by hand, and the analyst may in fact have to do a considerable amount of work in calculating coefficients before the problem is ready for the computer.

A repetitive problem, on the other hand, is one where essentially the same calculation has to be carried out periodically, only the numerical data being different each time. This type of problem is common in structural engineering practice, especially in any organization which specializes in the design of particular types of structure.

The economic considerations involved in choosing between automatic and manual methods of analysis are completely different in the case of repetitive problems. No longer is the computer program something to be thrown away once the calculation has been completed. It now represents a capital asset of considerable value, since it can be used for similar calculations in the future without any further programming being required. If such a program has been written for analysing a particular type of structure then each individual analysis merely involves the transcription of the relevant data from the designer's drawing board into the computer input medium.

![image 210](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile210.png)

###### 202 MATRIX METHODS OF STRUCTURAL ANALYSIS

Since a computer program for a repetitive problem is of permanent value it is worth while spending a considerable amount of time and effort on making it as efficient as possible. There are a number of features which such a program should possess.

The first and perhaps the most obvious feature is numerical efficiency. Even if the running time of the program is only a few minutes, a saving of a few per cent every time the program is used may represent a considerable gain over a long period. It may now be worth writing special routines for dealing with certain types of matrix, and developing compact methods of storing matrices with large numbers of zeros.

The second feature is generality of application, and it is this characteristic which makes matrix methods so valuable in structural analysis. In designing a program for a certain type of structure the restrictions on structural form should be as liberal as possible. It must be remembered, however, that generality must always be paid for. It must be paid for in computing timefor example, the analysis of a simple portal frame on a given computer will always take longer when carried out by a general three-dimensional space-frame program than it will when done by a simple program restricted to portal frames. Equally important, it must be paid for in program development time. To include facilities in a program which are very rarely used may involve a considerable amount of development time without adding materially to the value of the program. In extreme cases a program may be conceived in such general terme that its detailed construction becomes too complicated for its designer.

Thirdly, a program for a repetitive calculation should fit naturally into the overall design process, of which the computing work is probably only a small part. In the case of programs for structural analysis the program should take in the data describing a particular structure in a form as close as possible to the engineer's normal specification, and should produce answers in the form of the actual displacements and stresses which he requires. The transcription from the drawing-board to the computer input

![image 211](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile211.png)

###### COMPUTATIONAL PROBLEMS 203

medium should not involve any manual calculations, and should be systematized in such a way that it can be carried out by a person who does not know the method on which the analysis is based. The actual writer of the program may use matrix methods, but the matrix operations, if they exist, should take place "behind the scenes" and not be the concern of the user of the program. In this way the whole process of analysis becomes something which can be carried out by semi-skilled labour.

###### 9.2. Ill-Conditioning in Matrix Processes

In section 2.3 we considered a set of linear equations Ax = b (9.1)

as a series of statements about the vector x. By writing the equation in the form

a\x = bx a2x = b2

we showed that these statements are really specifications of the components of the vector x in various directions au a2, ..., an. We deduced that the value of equation (9.1) as an expression for determining x depends on whether the set of vectors au a2, ..., a„ forms a "good" system of axes for defining a vector of n dimensions.

In analysing a structure by the equilibrium method we have to solve the set of equations

p = Kd (9.2)

and it is natural to consider in what circumstances, if any, there is likely to be computational difficulty due to ill-conditioning of

###### H

![image 212](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile212.png)

###### 204 MATRIX METHODS OF STRUCTURAL ANALYSIS

the matrix K. Similarly in the compatibility method it is necessary to invert the matrix B ^ B , and it is desirable to choose a release system which makes this matrix as well-conditioned as possible. We consider the equilibrium method first.

To illustrate both the cause and the effect of ill-conditioning in the equilibrium method we consider the simple one-dimensional system shown in Fig. 9.1, in which three springs of stiffnesses k,

$1 B C ^ x] k + K ^ k l·

P\ ,*\ P?>*2 x

FIG. 9.1. Simple one-dimensional system illustrating ill-conditioning.

K and k support two points B and C at which known loads Pu Pi a re applied. In this example it is very simple to set up the equilibrium equations

pl = (/c + K)xl — Kx2 p2 = -Kxv +(k + K)x2

which may be written

(9.3)

\k + K - K |[*i

-K k + K\[x2

iPi.

We see that in this case the vector x = |Λι I is specified by its scalar products with the two vectors a[ = [k + K —K], a2 = [ — K k + K\. Whether these are "good" axes for defining

a general two-dimensional vector depends on the relative magnitudes of the stiffnesses K and k. The directions of the vectors

- au a 2 and the lines corresponding to the scalar equations defined by (9.3) are shown in Fig. 9.2 for the two cases k/K = 0-1 and k/K = 10.


It will be seen that when k is small relative to K the vector x is ill-defined, in the sense that small changes in the loads or the

![image 213](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile213.png)

###### COMPUTATIONAL PROBLEMS 205

stiffness coefficients may produce large changes in xx and x2. If we solve equations (9.3) by the elimination process we have to multiply the first equation by K/(k + K) and add it to the second.

FIG. 9.2. (a) An ill-conditioned system: k\K = 0-1. (b) A well-conditioned system: k/K = 10.

This gives

k + K -K

Pi

0 (k + K) - K2j(k + K) *2J and the last equation, which gives x2, may be written

Pi + KpJik + K)\

f(fc + K)2 - K2)

###### p2 + KPl/(k + X) = p ^ ^ J*2

If we consider the evaluation or the coefficient of x2 in this equation as an algebraic process then there is of course no difficulty, but if the coefficients k + K and K are only available in numerical form then we have to find the difference of two squares, which will be very nearly equal if k < K. Thus the coefficient of x2 will have fewer significant figures than the

![image 214](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile214.png)

###### 206 MATRIX METHODS OF STRUCTURAL ANALYSIS

original coefficients k -f K and K, and this inaccuracy will in general lead to both xt and x2 being in error.

It is apparent that in this simple example ill-conditioning arises when the stiffness K of the spring which connects the two points B and C is large compared with the stiffness of the springs which connect these points separately to the fixed supports A and D, so that the displacements χγ and x2 are physically very closely linked together. In fact we may argue that the real cause of the ill-conditioning is not that the equilibrium equations are a

"bad" way of defining the vector l but that this vector is a "bad" way of defining the displaced form of the system when K is large. For example, if we define the displacements of the points B and C by means of the extensions of the springs AB and BC then the equations giving these extensions are quite well conditioned.

The same phenomenon occurs in the analysis of rigid-jointed frames by the matrix equilibrium method, particularly in frames of unbraced form. If we consider the simple portal frame shown in Fig. 9.3a then the formal application of the equilibrium method involves defining the displacement of the structure by means of the two displacement vectors

###### [δΧΑ-

dB = ~δχΒ~\

SyB

δ>Λ

###### .o,\

[ θΑ.

If we write down the equilibrium equations in the manner described in chapter 4 and extract the scalar equations concerned with horizontal equilibrium we find that these have the form

pxA = {(EA/L)b + (12EI/L\}ÔXA - (EA/L)bôxB }

(9.4) pxB = ~(EAIL)bôxA + {(EA/L)b + (12L7/L3)CR J

![image 215](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile215.png)

###### COMPUTATIONAL PROBLEMS 207

In most practical frames the direct compressive stiffness terms EA/L are considerably greater than the shear stiffness terms 12EI/L3, so that equations (9.4) are ill-conditioned in exactly the same way as equations (9.3).

This type of ill-conditioning only appears in frames which are unbraced. If we add a diagonal bracing d to the frame shown in Fig. 9.3a, so that we obtain the frame shown in Fig. 9.3b, it will

B

A

0

c

< ^X\\\\\\ \\ Λ;\V,\

\\x\

(a) (b)

FIG. 9.3. (a) A frame with ill-conditioned sway equations. (b) A frame with well-conditioned sway equations.

be found that the equations are quite well-behaved. This is because the diagonal bracing gives joint B a direct stiffness with respect to horizontal displacements which is comparable in magnitude to the axial stiffness of the member b connecting A and B. It should be noted that the ill-conditioning depends on the stiffness matrix K and not on the loading vector p. Thus it is a function of the structure, and the choice of variables used to define its deformation, rather than the particular load system applied.

The degree of ill-conditioning which appears in the formal application of the equilibrium method described in chapter 4 to rectangular rigid-jointed frames is sufficient to cause a certain amount of trouble if the calculations have to be done by hand. In practice, of course, this difficulty is avoided by ignoring axial compressibility altogether and as a consequence representing the sideways displacement of all points at a particular floor-level by a single component of displacement. However, this to some extent destroys the systematic nature of the matrix equilibrium method,

![image 216](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile216.png)

208 MATRIX METHODS OF STRUCTURAL ANALYSIS

which is its chief attraction from the point of view of an automatic computer.

Most automatic computers store numbers to a precision of about 10 decimal places, and experience seems to show that this is sufficient to avoid any serious trouble due to ill-conditioning when using the equilibrium method for the analysis of practical structures, whether they are braced or not. This statement is based on the assumption that the equilibrium equations are solved by the elimination method—the ill-conditioning is certainly sufficiently severe to make the simple Gauss-Seidel iteration process converge extremely slowly when applied to unbraced rigidjointed frames. Some experiments carried out by the author suggest that in an unbraced frame formed from ordinary rolled steel sections the axial stiffnesses can be increased by a factor of about 103 before the effects of ill-conditioning become serious.f

Similar arguments may be applied to the matrix BrFmB, which has to be inverted when the compatibility method is used. In section 7.3 we showed that this matrix, which expresses the displacements u at the releases in terms of the release load-pairs q, has the general form

^ 2 1 ^ 2 2 * In

\Jn\ $nl FnnJ

where the leading diagonal elements F11? F22> etc» represent the direct flexibilities at the various releases and the off-diagonal elements represent the cross-flexibilities. We also showed that in the case of a rigid-jointed structure each release load-pair can be associated with a "ring". Each leading diagonal element is formed

jThese experiments were carried out on simple frames with about 12 joints. In structures with several hundred joints it may be necessary to use double precision arithmetic during the solution in order to restrict the build up of rounding errors.

![image 217](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile217.png)

COMPUTATIONAL PROBLEMS 209 by adding up the flexibilities of the members making up the corresponding ring, while the off-diagonal elements consist of the flexibilities of elements common to two rings. It follows that if we have two rings coupled by a very flexible member then the matrix Bf FmB will be ill-conditioned in exactly the same way that the stiffness matrix K is ill-conditioned when two joints are coupled by a very stiff member.

We may illustrate this by considering the simple example shown in Fig. 9.4. Here we have two rings Ru R2 in which are

FIG. 9.4. Two rings with a very flexible common member.

inserted releases. The gaps produced at the releases by the external loads are ui9 u2 and we wish to find the load pairs qu q2 which will reduce these gaps to zero. The equations for ql and q2 will be of the general form

Γ«ι" (9.5)

= F'AB + F AC . -F'AC

hi

-F'AC 1

###### Uz

L«2.

F AD + F'ACI

If now the member AC is very flexible compared with members AB and AD then F'AC will be very much greater than FAB or F'AD

![image 218](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile218.png)

###### 210 MATRIX METHODS OF STRUCTURAL ANALYSIS

and equation (9.5) will be ill-conditioned in exactly the same way as equations (9.3) or (9.4).

Since the choice of the releases in the compatibility method is under the control of the analyst it is desirable to have a general criterion as to what constitutes a "good" system of releases. As far as the conditioning of the flexibility matrix is concerned the main aim should be to make the leading diagonal elements as large as possible in comparison with the off-diagonal elements. Physically this corresponds to choosing a system of releases in which the direct flexibilities of the rings are large compared with the flexibilities of the members which couple the rings together. An alternative statement of this criterion is that the displacement which a release load-pair induces at its own release point should be as large as possible compared with the displacements which it induces at other release points.

An interesting contrast arises when we consider conditioning problems in the method of transfer matrices. As we showed in the previous chapter, the method of transfer matrices uses an equilibrium or compatibility condition applied at one end of a chain of members to find unknowns associated with the other. Its success depends, therefore, on a disturbance applied at one end of the chain propagating to the other without undue attenuation. For example, to solve the simple system shown in Fig. 9.1 by the method of transfer matrices we define a state-vector at the extreme left-hand end of the system, consisting of an unknown force and a known (zero) displacement. We then proceed along the chain, finally applying a condition of zero displacement to the displacement component of the state-vector at the extreme right-hand end. If now the stiffness K of the centre spring is very small compared with the stiffness k of the other springs we shall expect this condition of zero displacement to be very little affected by anything which happens at the left-hand end of the system. In the extreme case where K is zero the transfer matrix method fails completely, since a disturbance can never propagate from one end of the system to the other. It follows, therefore,

![image 219](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile219.png)

that the transfer matrix method encounters conditioning trouble in precisely the situation where the equilibrium method leads to well-conditioned equations. Conversely it is satisfactory in situations where the application of the equilibrium method leads to ill-conditioned equations.

###### 9.3. Numerical Checks in Matrix Processes

In designing any numerical process it is always desirable to include some kind of checking system. Such checks have two main functions. The first function is to detect actual mistakes, and in manual work in particular it is important that a mistake should be detected as soon after it is made as possible, so that useless work is avoided. The second function is to provide an estimate of the overall accuracy of the calculation, and to detect cases where errors due to ill-conditioning, rounding-oif, etc. are serious.

The type of running check which it is desirable to include in a calculation for the purpose of error-detection naturally depends on the frequency with which the human or automatic computer is likely to make mistakes, and most textbooks on numerical methods describe checking systems which are appropriate for matrix calculations when these are carried out by hand. However, modern automatic computers usually have their own built-in error-detecting circuits, and in general these are sufficiently reliable for an overall check on the complete calculation to be all that is required. The main purpose of this check is to detect numerical inaccuracies due to ill-conditioning rather than to indicate machine faults.

In programming structural problems for a computer, therefore, it is common practice not to include any programmed checks on the individual matrix operations, but to provide an overall check on the final results. If the analysis is based on the equilibrium method then the final stage consists of the calculation of the member end-loads from the member stiffness matrices and the computed displacements. The simplest way of checking these

###### LH

![image 220](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile220.png)

212 MATRIX METHODS OF STRUCTURAL ANALYSIS

loads is to verify that they are in equilibrium with the external loads applied at the joints. In essence this is simply a substitution of the computed joint displacements d into the original equations p = Kd to verify that they do in fact satisfy the equations.

In practice, of course, the conditions of equilibrium will never be satisfied exactly. Instead of the true displacements d we inevitably calculate some approximation to this set, which we may call d*, and when this is multiplied by K we obtain a load vector p* which differs from p by some amount <5p = p — p*. The vector <5p is termed the "residual vector". Having calculated <5p we may if necessary improve the accuracy! of the solution by solving the equation

δρ = K<5d (9.6)

thus obtaining the correction <5d which has to be added to d*. Of course this correction itself is only approximate, but if necessary the process may be repeated until sufficient accuracy has been achieved.

It will be noted that the simplest check to apply is a check on the degree to which the internal loads satisfy the equilibrium equations, and not a check on the accuracy of the displacements. It is true that we may obtain an estimate of the error in the displacements by solving equation (9.6), but this will involve just as much work as the solution of the original equations. It is also true that if the matrix K is ill-conditioned then the error-vector δό may be considerably larger than the residual vector <5p. However, we must not overlook the fact that in any real problem of structural analysis the load vector p is only known approximately. If from the computed displacements d* we calculate a load vector p*, the first question we should ask is whether we really know p so precisely that the difference <5p is significant. If <5p is less than the inevitable uncertainty in our knowledge of the

t This process merely corrects errors due to rounding-off during the solution of the equations. It does not, of course, correct rounding errors made during the calculation of K itself.

![image 221](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile221.png)

applied loads any attempts to improve the "accuracy" of our solution are bound to be useless. Looking at the problem from a slightly different point of view, we may say that our solution d* and the internal loads derived from it are exact for a system of applied loads p*. Thus we have an exact solution, not of the loading case p which we set out to analyse, but of a loading case p* which differs from the original by a certain amount. If the difference is insignificant then the solution we have found is clearly an acceptable one.

The same type of overall check may be applied in the compatibility method. Having calculated an approximate set of member end-loads p£ the obvious thing to do is to see whether these really do produce continuity at the releases. Thus we evaluate B'^mPm and see whether it is zero. As in the case of the equilibrium method, we shall find that due to rounding errors during the calculation the result will not be quite zero. Before any attempts to improve the "accuracy" of the calculation are made it is necessary to consider whether the error is significant. Now the error here is an error in the satisfying of compatibility conditions at the releases, just as before it was an error in satisfying equilibrium conditions at the joints. We must accordingly ask whether we know that during the erection of the structure the compatibility conditions were satisfied to this degree of accuracy. In other words we say that our solution is "exact" for a structure in which there is a certain amount of lack of fit when unloaded, and consider whether or not this degree of incompatibility is likely to arise in practice.

Although the checks we have described have been thought of as overall checks they are really only a test that the equilibrium equations have been solved or the flexibility matrix inverted correctly. In the equilibrium method, for example, each member K' matrix is used twice during the calculation—first in the formation of the stiffness matrix of the structure K and afterwards in the calculation of the member end-loads. A computing error in the calculation of a K' matrix will lead to the final solution being

![image 222](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile222.png)

###### 214 MATRIX METHODS OF STRUCTURAL ANALYSIS

incorrect, but if the faulty K' matrix is used consistently the resulting internal loads may still satisfy the equilibrium equations, so that the check we have described may not detect the error. In fact we shall have obtained a correct analysis of the wrong structure. In present-day computers, however, such errors are extremely rare—certainly a great deal rarer than the occasions when the same effect is produced by a human error in the preparation of the computer input data.

Finally it must be stated that while an equilibrium check is a valuable aid to confidence in the results produced by a computer, in practice the degree of accuracy provided by an automatic computer is usually considerably more than that thought necessary in structural calculations. If a check fails, then the possibility that the failure was due to a transient machine error may be tested by running the program through the computer again. If the failure is repeated, indicating a genuine numerical difficulty, it probably implies the existence of something very unusual in the structure whose data has been fed into the computer—or, of course, an error in the data.

###### 9.4. Operations on Banded Matrices

As mentioned earlier, the user of an automatic computer may expect to be provided with general purpose routines for carrying out standard matrix processes. If the problem to be solved is a single one (according to the definition given in section 9.1) then he will naturally use these routines, if possible, in order to minimize the programming effort required. However, the matrices which appear in structural analysis are often of very simple form, so that if the program is to be used a large number of times it may be desirable to write special routines which are tailored to fit the particular type of matrix involved.

The need for special-purpose routines is particularly apparent when dealing with really complex structures. For example, consider the problem of analysing a space frame of 100 joints—

![image 223](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile223.png)

###### COMPUTATIONAL PROBLEMS 215

not an unduly complicated structure by modern standards. The equilibrium method described in chapter 4 provides an admirably systematic technique for setting up the load-displacement equations of such a structure, and there is no particular difficulty in programming this technique for a computer. However, in order to decide whether the method is practicable we need to know how long it will take a computer to solve the resulting 600 simultaneous equations. The following analysis is very approximate, but shows the order of magnitude of the times which are involved. We shall take the elimination method and consider the problem of reducing the equations to triangular form—the subsequent back-substitution takes a relatively short time.

In estimating how long it will take a particular computer to carry out a given piece of numerical work two factors have to be considered. The first and most obvious is the time taken by the actual arithmetical operations which have to be performed. This of course varies with the type of computer, and the time per operation may vary from less than 1 /xsec in the fastest (and most expensive) scientific machines to 1 msec or so in computers with less sophisticated arithmetical hardware. The second factor, which may be equally important, is the time taken to transfer numbers from one part of the computer to another. Most computers have two forms of number storage, which may be referred to as the "working store" and the "auxiliary store". The working store holds the instructions which the computer is actually in process of obeying and the numbers on which these instructions operate. Its capacity may vary from 100 to 200,000 numbers, according to the size and cost of the computer. The auxiliary store, which often takes the form of magnetic tape or a magnetic disc, is of much larger storage capacity. However, a computer cannot do arithmetic on numbers while they are held in the auxiliary store—it is necessary to transfer the numbers to the working store for processing, and then return them to the auxiliary store afterwards. Since the transfer is usually an electromechanical operation its speed is limited by the rate at which

![image 224](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile224.png)

216 MATRIX METHODS OF STRUCTURAL ANALYSIS

information can be written on and read from magnetic materialas far as magnetic tape is concerned the transfer rate is likely to be between 5000 and 50,000 numbers per second.

Returning now to our problem of solving a set of 600 simultaneous equations, it is obvious that in the general case we shall require storage for 6002 = 360,000 numbers. There are many computers which have this storage capacity, although there are none, as yet, with a working store of this size. Let us imagine that we have a computer whose auxiliary store is of adequate size for our purpose, and that we have set up the coefficients of the 600 equations in this store. If we are solving the equations by the elimination process it will be necessary to take each equation in turn and add suitable multiples of it to all subsequent equations. The reader may easily verify that the total number of arithmetic operations involved is approximately 6003/3. If now our computer has a fairly small working store—say 8000 numbers —it will be necessary to keep all the coefficients of the equations in the auxiliary store and bring them to the working store each time they are altered by the elimination process. Thus to the 6003/3 arithmetic operations we must add a total of 2 x 6003/3 transfers between the stores. If our computer has an operation rate of 100 /isec per arithmetical operation and a transfer rate of 10,000 numbers per second (figures representative of a mediumsized modern computer) then the arithmetic will take approximately 2 hrs of machine time, while the transfers between auxiliary and working stores will take about 4 hrs. More sophisticated programming techniques would certainly reduce this figure, but it would probably be difficult to cut the total time required for the calculation to less than, say, 2 or 3 hrs. This might be regarded as reasonable in an important single research calculation, but it certainly cannot be regarded as satisfactory in the case of a routine engineering calculation which one might want to repeat several times.

In fact we have grossly over-estimated the number of operations which would be required in analysing a practical space structure

![image 225](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile225.png)

COMPUTATIONAL PROBLEMS 217

of 100 joints. Not only have we ignored the symmetry which we know is possessed by the stiffness matrix of a structure, but we have taken no account of the large numbers of zeros which are

FIG. 9.5. A three-dimensional frame with 100 joints.

present in this matrix. To obtain a more realistic estimate of the amount of work likely to be involved we introduce the idea of the "band-width" of a matrix, which we illustrate by considering the structure shown in Fig. 9.5.

In section 4.3 we derived rules for constructing the complete stiffness matrix of a general structure. If we apply these rules

![image 226](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile226.png)

218 MATRIX METHODS OF STRUCTURAL ANALYSIS

to the structure under consideration we find that the stiffness matrix has the general form, In this arrangement an asterisk indicates a non-zero element and a dot a null element, the elements being 6 x 6 sub-matrices since the structure is a space frame. Since the matrix is symmetric

Joint numbers

- 1
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
- 15
- 16
- 17


- * * · · · * · · · · # I
- * * · · · * · · · · * I
- * * · · · * · · · · * I
- * * · · · * · · · · * I
- * · · · · * · · · · * ' ·
- * * *
- * * * I
- ** * I


###### ** * I

- * * I
- * * · · · * · · · · * I
- * * · · · * · · · * I
- * * · · · * · · · · * I
- * * · · · * · · · · * I
- ** * I


###### * * * · · · · !

only the section above and including the leading diagonal has been shown. It will be recalled from section 4.3 that the leading diagonal elements correspond to the direct stiffnesses of the joints, while a non-zero element in an off-diagonal position corresponds to a direct connection between joints. Thus an asterisk in position i, j indicates the presence of a member con-

![image 227](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile227.png)

COMPUTATIONAL PROBLEMS 219

necting joints i andj . It follows that in the upper triangle of the stiffness matrix there will be one leading diagonal element for each joint and one off-diagonal element for each member connecting two joints, giving in the example considered a total of 100 + 220 = 320 elements. Since each element is a 6 x 6 submatrix this gives a total of 11,520 non-zero coefficients. This might be further reduced if we considered the symmetry of the leading diagonal sub-matrices. Comparing this figure with the total number of 360,000 coefficients we see that only about 3 per cent of these coefficients really need to be stored in the computer in order to define the stiffness matrix.

In view of the small number of non-zero coefficients it is natural to consider methods of solving the load-displacement equations in which only the non-zero elements of the stiffness matrix need be stored. There are a number of such methods, in which the coefficient matrix is not altered during the solution process. Of these the most satisfactory from a programming point of view are the Gauss-Seidel method described in section 2.6 and the method of conjugate gradients developed by Hestenes and Stiefel (Hestenes and Stiefel, 1952). However, neither of these methods are very satisfactory if the equations are ill-conditioned, and experience suggests that the storage economies which they make possible do not in fact lead to a significant saving in computing time.|

Since the elimination method alters the coefficient matrix it might seem at first sight that the zero coefficients must be retained, since they may become non-zero during the elimination process. However, it is easy to see that only certain of the zero coefficients are affected in this way. Returning to our example it is apparent that all the coefficients outside the diagonal band of non-zero elements furthest from the leading diagonal will always remain zero during the solution process, while the zeros inside this band will in general be altered. It follows that although in the

t A comparison between elimination and iteration technique has been made by Clough, Wilson and King (Clough, Wilson and King, 1963).

L H·

![image 228](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile228.png)

220 MATRIX METHODS OF STRUCTURAL ANALYSIS

elimination method it is necessary to store a certain number of zeros it is still possible to achieve a considerable economy in storage.

In general we can say that all the non-zero elements in the stiffness matrix of a structure will lie within the region formed by two diagonals which are equidistant from the leading diagonal, the distance depending on the maximum difference betwpen the pairs of joint numbers at the ends of the members of the structure. This maximum difference we call the "band-width" of the stiffness matrix—in our example the band-width is 10. (The band-width is not, of course, an invariant of the structure, since it depends on the way the joints are numbered. In fact it is an interesting problem to find a general method of numbering the joints of a structure in such a way as will make the band-width as small as possible.) If the band-width in a particular case is n then only n + 1 elements in each row of the stiffness matrix need be stored for a solution by elimination. In our example we need to store 11 elements in each row, these elements consisting of the leading diagonal element and the 10 consecutive elements to the right of it. Thus we have to store approximately 1100 elements, or 40,000 coefficients.

The banded nature of the stiffness matrix not only reduces the amount of computer storage required. It also has a considerable effect on the number of numerical operations required. If we operate entirely with the section of the matrix on and to the right of the leading diagonal then a band-width of 10 implies that each scalar equation contains at most 66 non-zero coefficients. It is only necessary, therefore, to add multiples of it to each of the 65 scalar equations following, the number of operations being at most 662/2. The region of the matrix affected by a particular equation during the elimination process is shown diagrammatically in Fig. 9.6. It follows that the total number of operations needed for the solution of the 600 equations associated with the frame shown in Fig. 9.5 is now only 600 x 662/2, and at the rate of 100 /isec per operation used previously this would take about

![image 229](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile229.png)

COMPUTATIONAL PROBLEMS 221

2 min.—an improvement by a factor of 60 on the previous estimate.

An even more spectacular improvement occurs in the case of transfer times. For at each stage of the ehmination process we have one equation of 66 coefficients being used to modify the next 65 equations, each one of which also has 66 coefficients.

FIG. 9.6. Region of a banded matrix modified by a given pivotal equation. Region (a)—coefficients which are actually altered. Region (b)—unaltered coefficients in modified equations.

Now the total number of coefficients involved in this process is only 662, and if the working store of our computer will hold 8000 numbers we may hold all the 66 equations in this store at the same time and still leave space for the load vector and the program. Thus we may arrange the computation in the following way. The first 66 equations are transferred from the auxiliary store to the main store of the computer, and the first equation is used to modify the remaining 65 in the usual way. When this modification has been completed the first equation is transferred back to the auxiliary store and is replaced by the 67th equation. Since the second equation and all the other equations on which it has to operate are now in the working store the process can be repeated using the second equation without any further transfers. When the operations with the second equation are complete

![image 230](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile230.png)

222 MATRIX METHODS OF STRUCTURAL ANALYSIS

it too is returned to the auxiliary store and replaced by the 68th equation, and so on. In this scheme each equation is brought from the auxiliary store to the working store and takes its place, as it were, "at the end of the queue". While in the working store it is modified by all the equations which have higher positions in the queue, until eventually it reaches the position where it is used as the pivotal equation. After it in its turn has been used to modify the equations which follow, it is returned to the auxiliary store. Thus each equation is only transferred between the auxiliary and the working stores once in each direction. The total transfer time involved is thus the time required to transfer about 2 x 40,000 numbers, which at the rate quoted previously would only take about 8 sec.

It must be stressed that the figures which we have derived are extremely approximate. Their main purpose is to show that the analysis of a space frame of 100 joints by the equilibrium method is a practical proposition on quite a small computer. Another important conclusion we may draw is that for a given bandwidth the solution time is linear in the number of joints. Thus if the frame shown in Fig. 9.5 were extended upwards for another ten floors then the solution time for the resulting frame of 200 joints would be approximately doubled. It also follows that it is the band-width rather than the number of joints which determines the ease with which a structure can be analysed. Not only is the total amount of calculation proportional to the square of the band-width. For any given computer there is a certain bandwidth for which the scheme of transfers described above becomes impossible. For matrices with band-widths larger than this figure the computing time is likely to rise considerably.

Similar considerations apply to the equations which have to be solved in the compatibility method. Here the band-width depends on the degree of interaction between the various release load-pairs, which depends in turn on the positions chosen for the releases.

While the stiffness matrix of a structure is often of banded form, the inverse matrix is unlikely to have many non-zero

![image 231](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile231.png)

###### COMPUTATIONAL PROBLEMS 223

coefficients. For the inverse equations are of the form d = Fp, and in general any component of p is likely to produce displacements at all the joints of the structure. In the case of very large and heavily banded matrices one must therefore qualify the general principle that if several loadings have to be considered it is better to compute the inverse matrix F and then multiply the successive loading vectors by it. Such an approach may well involve a great deal of unnecessary computing, and use a great deal of storage space. Thus it may often be better to solve the equations separately for each loading than to try and compute the matrix F explicitly. For more detailed accounts of methods of dealing with banded matrices the reader is referred to papers by Wilson (Wilson, 1959), the present author (Livesley, 1960) and Jennings (Jennings, 1966).

9.5. The Use of Sub-Structures

The technique described in the previous section is well adapted to the analysis of structures which are in some sense "long and thin"—a tall building, for example, or a multi-span bridge. In such cases the band-width is small compared with the total number of joints and, as we have seen, it is the band-width which is the main factor in determining the amount of computing work which has to be done. Another way of dealing with the same kind of problem involves the idea of sub-structures.

Consider, for example, the structure shown in Fig. 9.7a. We imagine that this structure consists of two simpler structures connected together at certain points. (While the division between the two structures is to some extent arbitrary one would in practice naturally try to make it in such a way that the connections between the two are as few as possible.) In our example we shall assume the connection to consist merely of two common joints M and N.

We now adopt the procedure used in the compatibility method, inserting releases at the points connecting the two systems and

![image 232](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile232.png)

224 MATRIX METHODS OF STRUCTURAL ANALYSIS

applying self-equilibrating load-pairs at these points. By doing this we reduce the structure to two simpler structures, as shown

- in Fig. 9.7b, which can be considered quite separately. We may


M

Sub-strive I

Sub-structure

###### 2

N

Joints A...L

Joints P...Z

//////////////////////////////////j^/j///?;////;////////^/,

la)

#### f L•M M+

CD

(b)

FIG. 9.7. A structure split up into two simpler sub-structures.

###### begin the analysis by writing down the load-displacement equations of sub-structure 1 in the form

###### dA

(9.7)

###### PA =

K4

dL dM

PL

Ids.

UATJ

Since qM and qN are unknown we cannot solve these equations completely, but we can commence the elimination process in the

![image 233](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile233.png)

COMPUTATIONAL PROBLEMS 225

usual way, subtracting suitable multiples of the first equation from the others, etc. until we have eliminated all coefficients of the joint displacements dA, ..., dL from the equilibrium equations for joints M and N. Thus we reduce the last two equations of

- (9.7) to


9Ν + ΦΝ(ΡΛ^'^ΡΟ\ C

(9.8)

Here K* indicates the altered coefficients produced by the elimination process, and φΜ, φΝ are the linear combinations of the known applied loads at joints A, ...,L which are added to the unknowns qM and qN. We may write equation (9.8) in the form

- ■"

"ΦΜΙ\ .ΦΝΙ\

Kf]k. "

L A *.

These equations have a direct physical interpretation. The reduced stiffness matrix K* represents the stiffness of sub-structure 1 as viewed from joints M and N, while the loads φΜί and φΝί are the loads which the structure would exert on the joints M and N if these joints were prevented from displacing.

In exactly the same way we may write down load-displacement equations for sub-structure 2 in the form

(9.9)

- 4 T JV

L Pz J Ldzj

If we now add equations (9.8) to the first two equations of (9.9)

![image 234](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile234.png)

we eliminate the unknowns qM, qN and obtain

(9.10)

dM dN

ΦΜΙ ΦΝΙ

LPz

J Luz

where K is the matrix formed by adding K* to the appropriate elements of K2. Since the 0's are known these equations may be solved for the displacements of sub-structure 2 without difficulty. Once the displacements of joints M and N are known we may drop the last two of the equilibrium equations (9.7) and solve the remaining equations for the displacements of sub-structure 1.

An alternative approach is to take the equilibrium equations for sub-structure 2 and eliminate the displacements of joints O, ..., Z in the same way as we did for sub-structure 1. This gives

# QN +ΦΝ2 «E

(9.11)

1Μ + ΦΜ2

where φΜ2 and φΝ2 are linear functions of the loads applied to the joints of sub-structure 2. Equation (9.11) now defines the behaviour of sub-structure 2 as viewed from the joints M and N. If we simply add equations (9.8) and (9.11) our analysis is effectively the same as before. If on the other hand we write equations

- (9.8) and (9.11) in the form


ΪΙ^Ν + ΦΝΙ J

dM dN\

###### ΚΓ1Ϊ",Μ +

ΦΜ2 ΦΝ2

JL-ÏN +

![image 235](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile235.png)

COMPUTATIONAL PROBLEMS 227

we may obtain the unknowns qM, qN by equating the displacements of the joints M and N in the two sub-structures, writing the equations in the form

K** - i \ΦΜΙ\ ΙΦΝΙΙ

###### κΐ^ + κ*-1

"M2

###### κ;*-l

Kl

L«JVJ

This equation may be solved for qM and qN, after which we may obtain the detailed solution for each sub-structure by solving

- equations (9.7) and (9.9). The first approach which we described (i.e. the addition of
- equations (9.8) and (9.9)) is merely a computational device to allow the elimination solution of the equilibrium equations of the complete structure to be done in two parts. The second approach, in which we apply compatibility conditions at joints M and N to


determine the unknown internal loads qM and qN, is an application of the compatibility method described in chapter 7. There is, however, one important difference between the analysis developed here and the analysis given in that chapter. In our previous account of the compatibility method we introduced sufficient releases into a structure to make it determinate. It was therefore possible to determine the flexibility matrix of the resulting structure merely from the equations of joint equilibrium and the individual flexibilities of the members. In the analysis presented in this section both sub-structures may well be hyperstatic, so that it is necessary to find their flexibility matrices by inverting their stiffness matrices.

The idea of a sub-structure is nothing more than a generalization of the concept of a structural member, and all we are really doing is regarding the sub-structure as our basic "building brick", rather than the individual member. As in the case of a simple member, our main interest is in the displacements of the joints which connect the various sub-structures together, and the loads which act at these joints. Thus we replace loads acting at internal points of the sub-structures by "equivalent" loads at the connecting joints—the ^'s which we introduced in equations (9.8)

![image 236](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile236.png)

- and (9.11) are exactly analogous to the "equivalent fixed-end forces and moments" which we introduced when dealing with a member with loads acting at points along its length. The equations


- (9.8) are exactly analogous to the load-displacement equations of a simple structural member, expressed in "stiffness" form, and may be used to build up the load-displacement equations of a more complicated structure in exactly the same way as described in chapter 4. For example, consider the arrangement of three sub-structures shown in Fig. 9.8. Following the notation used in


ΓΠΤΠ

Fio. 9.8. A structure formed from three sub-structures.

dealing with single members we have used the suffixes 1 and 2 to denote the points at which sub-structures are connected to other sub-structures (in general, of course, a sub-structure may be connected to more than two other sub-structures). The number of degrees of freedom at the various connections may be different, although the number on either side of a particular connection must necessarily be the same. If we take the equilibrium equations for each sub-structure and eliminate all the "internal" displacements and loads we obtain equations which we can write in the form

Pi« + Φΐα = (* ΙΐλΑα + {^XliAla

Via + Φΐα = (^2ΐλΑα +!(*22)α<*2α

![image 237](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile237.png)

COMPUTATIONAL PROBLEMS 229

etc., the equations being similar for the other sub-structures. Although primes have been omitted from these equations they are of course in overall system coordinates. It will be found that they have the same characteristics of symmetry as the corresponding equations for single members. If we now apply compatibility and equilibrium conditions at the connections A, B and C we obtain the equations

Φΐα + Φlb Φη + Φ\

L02c + Φΐα J

■(*ai). + (*n)i Via)»

###### (*ai).

###### (K21\ (K22\ + (Kn)e

###### dB

(*12)e

(Kl212 Ja\ (*2l)c (ffll)a + (#22)cJ L^cJ

Once these equations have been solved for the connecting displacements dÄ9 dB and dc we may return to a detailed analysis of each individual sub-structure if necessary. The reader is referred to a paper by Eisemann, Woo and Namyet (Eisemann, Woo and Namyet, 1962) for an account of a general computer program for space-frame analysis which incorporates these ideas.

This replacement of an assembly of members by an "equivalent" system, in which only the joints which connect the assembly to the remainder of the structure are considered, is an extremely useful idea, since it enables one to separate out the small-scale detail from the overall pattern of stress and deformation. It is particularly useful when a structure contains a pre-fabricated member made up from a large number of smaller parts—a braced girder is an obvious example. The reader familiar with electric network analysis will realize that what we have been discussing is nothing more than a structural equivalent of Thevenin's theorem.

![image 238](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile238.png)

###### CHAPTER 10

###### The Analysis of Non-linear Structures

THERE are a number of occasions when it is necessary to consider structures which behave in a non-linear manner. Certain types of structure, particularly those formed partly from flexible cables, behave in a non-linear manner under working loads, while almost all structures have a non-linear load-displacement relationship as the collapse load is approached. In this chapter we consider ways in which the matrix methods developed in previous chapters can be extended to cover structures in the non-linear range.

Before discussing techniques for analysing non-linear systems it is worth while emphasizing again the points in our previous analysis at which we have made use of the concept of linearity. For this purpose it is convenient to use the statement of the equilibrium method of analysis given in section 6.2.

Our first assumption is that the individual components of a structure behave in a linear way. That is to say, we assume that the equations (6.7)

P„, = Kmem (10.1)

which relate the end-loads to the deformations for the disconnected members, are linear. It is obvious that if this is not so then the structure will in general behave in a non-linear manner.

Our second assumption is that the equations of joint equilibrium (6.9)

P = Cpm (10.2)

230

![image 239](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile239.png)

ANALYSIS OF NON-LINEAR STRUCTURES 231

may be written down for the undistorted structure, rather than for the distorted structure in which they must actually be satisfied. By doing this we make C a constant matrix, independent of the loading on the structure. Strictly speaking this procedure is always an approximation, and is justified by the fact that in most structures the displacements under working loads are small compared with the dimensions of the structure.

This assumption is repeated when we deduce the equations of displacement compatibility (6.10)

em = Cd (10.3) This relationship was proved by considering a virtual displacement <5d from the equilibrium state, and arguing that the work done by the applied loads during this deformation must be equal to the gain in strain energy of the members. This leads to the equation pf<5d = pÎ„<5em, where p and pm are the equilibrium external and internal load vectors, which are kept constant during the virtual displacement. Thus, provided that C is defined for the deformed equilibrium state, the equation

<5em = C M (10.4) holds, irrespective of linearity. If now the deformations of the structure are sufficiently small to justify our assumption that C does not change during the loading, then we may replace the virtual displacements and deformations <5d and <5em by the actual

displacements and deformations d and em. However, if the changes in geometry are significant then C is a function of the displacements, and in equations (10.2) and (10.4) it takes the value associated with the particular system of applied loading considered. In these circumstances it is only legitimate to replace the virtual displacements in equation (10.4) by small (strictly infinitesimal) real displacements from the equilibrium state.

When either or both of the above assumptions cannot be made it is usually necessary to employ an iterative type of solution, and a general iterative technique is discussed in section 10.3. First,

![image 240](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile240.png)

however, we consider a problem of practical importance which is non-linear in a very limited sense and whose solution is relatively simple. This is the problem of analysing a rigid-jointed structure in which the axial forces in members affect their bending stiffness. For the sake of simplicity the analysis is presented in the form which it takes when applied to plane structures—although complicated by the possibility of torsional-flexural buckling, a similar treatment may be developed for space structures.

10.1. Stiffness Matrices for a Uniform Member with Axial Thrust

In section 4.2 we developed the stiffness matrices for a uniform member in plane bending, assuming that the only effect of the axial component of load was to produce axial strains. If we consider the contribution which the axial thrust makes to the bending moment distribution in the member then these matrices must be modified.

We consider again the uniform member (Fig. 4.6) which we considered in section 4.2. We denote the compressive force in the member by P, and we regard this force as a known parameter of the member, just like E9 I and L. In fact, of course, the force P is equal to pxU and when the member is part of a structure it must satisfy conditions of joint equilibrium just like any other internal force or moment. For the present, however, we imagine that P is known—as we shall see, by doing this we make the analysis of a structure with axial forces in its members a purely linear problem.

As in section 4.2, we assume that the lateral displacement of the member is sufficiently small for the elementary theory of bending to apply. The governing differential equation is therefore

El t-\ = pylx - P(y - <5yl) - mx (10.5)

![image 241](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile241.png)

ANALYSIS OF NON-LINEAR STRUCTURES 233

where x is measured from end 1 of the member. Integrating this differential equation and inserting the appropriate end-conditions we obtain the slope-deflexion equations (4.10) in the modified form

El El El El , mi = 77 5(* + c)àyi + — soi - 7J ·*(! + Φγ2 + y sc92

Li Li Li Lé I

, (10.6) EI El EI El

m2 = JJ s(l + c)6yX + — sc6i - JY s(l + c)Sy2 + — s02 |

where .s and c are the non-dimensional stability functions originally defined by Lundquist and Kroll (Lundquist and Kroll, 1944) and developed more recently by Merchant (Merchant, 1954, 1955). The end-shears p y i and/?y2 may be found by applying the condition of moment equilibrium

mi + m2 + py2L + P(Sy2 - δη) = 0 (10.7)

where the end-thrust is written as P rather than as pxl or — px2 in order to keep the analysis linear. Thus we obtain equation (4.11) for the end-shears in the modified form

Î2EI P\ El Pyi = -Pyi = (-£Γ *tt + <0 ~ I)Syi + JT5(* + Wi (»0.8)

[2EI ,Λ N PL El /4

" \ΊΓ5( c) - IF2+IFs( c) 2

It will be noted that although the coefiicients in equations (10.6) are still linear in the displacement components Syl9 6U etc.

- and (10.8) are now functions of the axial thrust P these equations


Equations (10.6) and (10.8) may be put in a form more closely identifiable with equations (4.10) and (4.11) by introducing the functions

s(l + c) PI} ^ s(l + c) ^ s ^ sc

![image 242](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile242.png)

FIG. 10.1. The functions Φι Φί.

Using these functions we may write the equations for the endmoments and the end-shears in the form

m, = (6ΕΙΦ2Ιΰ)δγί + (4£/*3/L)Ö! - (6ΕΙΦ2/ΰ)δ,2 (10.9a)

+ (2Ε/Φ4/ί.)02 m2 = (6ΕΙΦ2Ιϋ)δη + (2£/Φ4/£)0! - {6ΕΙΦ2ΙΙ})δη (10.9b)

+ (4£/<P3/L)02

![image 243](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile243.png)

ANALYSIS OF NON-LINEAR STRUCTURES 235

-Py2 = {\2EWJU)èn + {βΕΙΦ^Θ,

(10.9c)

- (\2EWjL3)ôy2 + (6ΕΙΦ2/ΰ)θ2

Comparing these equations with equations (4.10) and (4.11) it is apparent that the Φ-functions are merely multiplying factors for the stiffness coefficients of a beam without end-thrust. They are conveniently expressed as functions of the ratio of the end-thrust P to the Euler load Pe = n2EI/L2, and are shown in Fig. 10.1.

In order to complete the load-displacement equations for the member it is necessary to obtain expressions for the axial forces Pxu Pxi in terms of the end displacements. As in section 4.2, we shall use the simple relationship

###### Pxi = -Pxi = (EAIQÖxl - (EAIQÔx2 (10.10)

neglecting the axial shortening terms due to curvature. In this way we keep the load-displacement equations linear, although the omission of the curvature terms is, of course, an approximation which must be borne in mind when assessing the results of any analysis.

Combining equations (10.9) and (10.10) we obtain the loaddisplacement equations for the member in the familiar form

###### Pi = £ιι<Ί + K12d2

(10.11)

Pi = #21^1 + #22^2

where

EA/L 0 0

* u

0 12EWJL3 6ΕΙΦ2/ΰ 0 6ΕΙΦ2ΙΙ} 4EW3/L

Kl2 — Κ2ι — -EA\L 0 0

0 -llEWJL3 6ΕΙΦ2Ιΰ 0 -6ΕΙΦ2/ύ 2EI<PJL

LI

![image 244](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile244.png)

K22 = rEA/L 0 0 0 12EI<PJL3 -6ΕΙΦ2Ιΰ 0 -6EI<P2/L2 4£/Φ3/£.

It may be noted that the loads pl9 p2 defined by equation (10.11) automatically satisfy the conditions of translational equilibrium Pxi — —PxiiPyi = —Ζ^2>a nd the moment condition (10.7).

It is apparent that if we think of the axial force P in a member

- as a known quantity then the equations (10.11) still provide a linear relationship between the end-loads and the end-displacements. They may therefore be transformed into system coordinates in the manner described in section 4.2 and combined with similar equations to form the complete set of load-displacement equations for a structure


p = Kd (10.12)

As before, the loading vector p may include fixed-end forces and moments equivalent to loads applied at points other than the joints of the structure, but it should be noted that the calculation of these fixed-end forces and moments may be affected by the existence of axial forces in the members. For example, if a beam carrying a uniform transverse load w per unit length is subjected to an axial thrust P then it can be shown that the fixed-end moments wL2/12 must be multiplied by the factor 1/Φ2· However, since we are assuming that the values of the axial forces in the members are known this does not materially complicate the analysis.

By solving the equations (10.12) we obtain the displacements of the joints of the structure, and substituting these displacements into equations (10.11) for the various members we obtain a set of internal forces and moments. These forces and moments necessarily satisfy the equations of joint equilibrium, and to that extent are a correct analysis of the structure. It must be remembered, however, that equations (10.7) and (10.11), which the forces and

![image 245](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile245.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 237

moments also satisfy, contain the assumed values of the axial thrusts, so that the analysis is only correct (in the sense of being self-consistent) if the axial thrusts obtained as part of the computed internal forces and moments agree in value with those originally assumed.

Fortunately there are many practical problems in which it is easy to make a reasonably accurate estimate of the axial forces in the members of a structure. In a triangulated rigid-jointed frame, for example, the axial forces are unlikely to differ significantly from those calculated in an analysis which treats all the joints as pinned. In rectangular frames, too, the axial forces in the stanchions may usually be estimated by treating the beams as simplysupported at their ends.

###### 10.2. The Determination of Elastic Critical Loads

While a designer may well be interested in knowing the value of the load factor which would cause a structure to collapse, he is unlikely to require detailed information about the behaviour of the structure as the collapse load is approached. This is fortunate, since a rigorous analysis of a structure under these conditions must inevitably include a consideration of the effects of gross deformation and partial plasticity. Such an analysis is complicated even when carried out on a computer, and certainly cannot be justified as part of normal design procedure.

In practice a reasonable estimate of the collapse load of a rigid-jointed structure can usually be obtained from two quantities which are more easily calculated—the rigid-plastic collapse load and the elastic critical load. The calculation of the first of these has already been discussed in section 7.7. The second may conveniently be obtained by using the modified equilibrium method described in the previous section. For an account of the use of these two quantities in estimating the collapse load of a structure the reader is referred to papers by Merchant (Merchant, 1954) and Home (Home, 1961).

![image 246](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile246.png)

###### 238 MATRIX METHODS OF STRUCTURAL ANALYSIS

The concept of the elastic critical load of a structure is essentially a generalization of the Euler buckling load of a pin-ended strut. We imagine a structure acted on by a given load system p such that the only internal forces are the axial thrusts Pt. We assume that the axial thrusts are proportional to the applied loading, so that a load system λρ produces axial thrusts XPr Then the elastic critical load is defined as the value of λ for which the equilibrium configuration of the structure is not unique, it being possible to maintain the structure in a displaced position involving bending of the members without any additional loading, as shown

- in Fig. 10.2. This corresponds exactly to the definition normally


λρ *P

FIG. 10.2. Alternative deformation states at the critical load.

given for the critical load of a pin-ended strut. It is assumed that the deformation of the structure from the condition in which all the members are straight is sufficiently small for the linear theory developed in the previous section to apply. It is further assumed that during this deformation the axial forces do not alter in value.

In general a small disturbing load δρ applied to the structure will produce a corresponding small change in displacements <5d, the two quantities being related by equation (10.12). Since we are assuming that this additional deformation does not alter the values of the axial forces in the structure, these forces remain

![image 247](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile247.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 239

equal to XPt, so that the stiffness matrix of the structure can be regarded as a function of λ only. Thus we may write equation

- (10.12) in the form δρ= Κ(λ)δά (10.13)


where K(A) is independent of (5d. At the critical load we have by definition <5p = 0 for some non-zero δά, so that equation (10.13) becomes

###### K(Acrlt)*d = 0 (10.14)

It follows that the stiffness matrix K(Acrit) must be singular, so that Xcrii is a root of the equation

|K(/l)|=0 (10.15)

Since |K(A)| is a transcendental function of λ it is usually necessary to find the roots numerically, evaluating the determinant for a series of values of λ and using one of the standard processes for inverse interpolation. It is very easy to carry out this type of numerical work on an automatic computer.

Although Κ(λ) is a more complicated function of λ than the linear expression A — λΐ which we considered in section 2.5, the calculation of critical loads is in essence an eigenvalue problem. While in practice interest is usually confined to the lowest positive root, equation (10.15) has in general an infinite number of roots, corresponding to an infinite number of critical loads. For each value of Xcrit equation (10.14) defines an associated "critical mode" of arbitrary magnitude but definite proportions, and the modes may be used as coordinates for defining the deformation of the structure under any arbitrary loading, in very much the same way as normal modes are used in problems of dynamic response.

An alternative way of determining the lowest critical load is to investigate the effect of a constant disturbance as λ is increased. Besides giving the value of the critical load this method also gives a picture of the behaviour of the structure as the critical condition

![image 248](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile248.png)

###### 240 MATRIX METHODS OF STRUCTURAL ANALYSIS

is approached. The disturbance should be one which excites the buckling mode associated with the lowest critical loadfortunately in most structures it is possible to make a reasonable guess at the form which this mode takes.

For example, if we consider the frame shown in Fig. 10.2 it is reasonable to assume that this frame will buckle in sidesway, as shown in the figure. An appropriate disturbance is therefore a constant horizontal load q applied to the top of the structure, as shown in Fig. 10.3a. If <5 is the horizontal displacement produced

###### Φ*\

77777777777777777Π77Γ

(a) (b)

FIG. 10.3. Determination of the critical load of a structure by a consideration of the reduction of stiffness.

by this disturbance the ratio q/δ represents the stiffness of the structure with respect to the disturbance, and as λ is increased this stiffness will diminish. Since at the critical load a displacement δ can exist without the presence of a disturbing force, it follows that at the critical load the stiffness of the structure with respect to the disturbance must be zero. Thus the critical load may be found by carrying out a series of analyses at various values of λ, and extrapolating the graph of q/δ against λ until it cuts the λ axis, as shown in Fig. 10.3b.

In applying this method it must be remembered that the use of a disturbance which does not excite the lowest mode will give an

![image 249](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile249.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 241

incorrect result. Thus the application of a symmetrical disturbance to the frame shown in Fig. 10.2 would lead to a value of Acrit corresponding to the lowest symmetric buckling mode, and this might well be considerably higher than the value associated with sidesway buckling.

10.3. A General Metiiod for Analysing Non-Linear Structures

So far we have avoided the real issue of non-linearity by imagining that we know part of the results of our analysis (the axial forces in a structure) before the analysis is commenced. We iiow describe a general technique which can be applied in situations where the non-linear effects cannot be dealt with in this way.

Before describing the method in its most general form we illustrate its essential characteristics by considering a simple example with one degree of freedom. We imagine that we have a bar whose load-extension relation is non-linear, being of the form p — /(<5), as shown in Fig. 10.4. We wish to find the extension S associated with a given load p, so that our problem is to solve the non-linear equation

p = f(5)=p (10.16)

We shall solve this equation by the Newton-Raphson method, the successive steps of the solution being illustrated graphically in Fig. 10.4. in this method we start at some assumed value of displacement, here taken to be the origin, and replace the nonlinear bar by a bar with linear characteristics whose stiffness is the same at the assumed displacement. (By the term "stiffness" we mean here the slope of the load-displacement curve, i.e. dp/do = /'(<?). This is sometimes known as the "incremental stiffness".) In graphical terms this means that we approximate to the curve by the tangent. Thus we replace (10.16) by the equation δ x/'(0) = p, where /'(0) is the derivative of the

![image 250](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile250.png)

###### 242 MATRIX METHODS OF STRUCTURAL ANALYSIS

function f{S) at the origin, and obtain an approximate solution <5i = Plf'(0). This corresponds to the point P[ in Fig. 10.4. If we now substitute δχ into equation (10.16) we find that this displacement really corresponds to a load px = f(ôx\ so that in fact we have only reached the point Px on the curve.

We now replace the non-linear bar by a bar with a linear loadextension law corresponding to the tangent to the curve at the point Pi9 i.e. to the straight line p = px + /'(δ1)(δ - ôt).

p= f(S)

FIG. 10.4. Illustration of the Newton-Raphson method.

Solving the equation/^ + f\b^){b - δχ) = p we obtain a second approximation <52 = (p - Pi)lf\ôx) + δχ. This gives us the point P2 in Fig. 10.4, and the process maybe repeated until the difference p - pn is less than some appropriate allowable error. As in the case of linear problems discussed in section 9.2, ill-conditioning may arise if the curve is nearly horizontal in the neighbourhood of the solution, since in such a case a small difference p — pn corresponds to a much larger change in the displacement. However, if p - pn is less in magnitude than the possible error in the

![image 251](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile251.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 243

specified value of p (which will only be known approximately in practice) the corresponding solution δη is obviously a valid solution of the problem.

The process which we have described will not converge if the starting point is too far away from the solution, and is likely to give trouble if the curve has discontinuities. For a smooth curve, however, the convergence in the neighbourhood of the solution is of second order.t In other words the approximation of the straight line to the curve becomes proportionately more accurate the nearer we get to the true solution.

The Newton-Raphson process as we have described it requires a re-calculation of the derivative at each approximate solution. If this calculation requires a considerable amount of labour, or if the value of the derivative is known not to change a great deal, then one may use the value of the derivative calculated at the origin at each stage. The resulting process is of course much less efficient in terms of the number of steps required to produce a given degree of convergence, but the effort required per step is also reduced. The process has only first order convergence, and is shown graphically in Fig. 10.5. As a further alternative, one might re-calculate the derivative periodically—say after every three or four steps of the iterative process. If the function f(x) is such that it is difficult to obtain the derivative /'(*) in algebraic form one may approximate to the derivative numerically, taking two points on the curve which are close together and finding the slope of the line joining them.

Both the normal Newton-Raphson process and the variations mentioned above may be generalized to systems which have several degrees of freedom. Returning to the general statement of the equilibrium method given in section 6.2 and discussed

- at the beginning of this chapter, we may combine it with the


t The order of convergence of an iterative process is defined as follows. Let x be the true solution, xn the approximation obtained after n steps and let 8xn = |x—*„|. Then if 8xn + 1 & a hxn, where \a\< 1, the convergence is first order. If 8xn+1 ^ a(8x„)2 the convergence is second order.

![image 252](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile252.png)

###### 244 MATRIX METHODS OF STRUCTURAL ANALYSIS

Newton-Raphson method to form a systematic approach to the analysis of non-linear structures.

Fio. 10.5. Modified Newton-Raphson process using lines of slope /'(0).

We consider a structure in which the member end-loads pm are related to the member deformations em by known equations (in general non-linear) which have the form

Pm =/(em) (10.17)

We begin the analysis by assuming a certain arbitrary set of deformations, and in this description of the method we choose these deformations to be all zero. Thus we replace (10.17) by the linear approximation

Pm = Km0em (10.18)

where Km0 represents the set of member stiffness matrices derived by ordinary linear small-displacement analysis of the individual members. This corresponds to the tangent at the origin in Fig. 10.4.

![image 253](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile253.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 245

The joint equilibrium equations are now written in the linearized form

P = Co Pm (10.19)

where the matrix C0 is based on the geometry of the undistorted structure, and the displacement compatibility equations are written in the corresponding form

em = C< d (10.20) Combining (10.18), (10.19) and (10.20) we obtain the normal load-displacement equations of linear analysis p = C0Km0COd, which we solve for the joint displacements of the structure in the usual way. These displacements constitute our first approximation to the true solution, and we denote them by d^ Substituting these displacements into (10.20) we obtain the corresponding member deformations em l, and the associated member end-loads pml follow from (10.17). (It is important at this point to use (10.17) rather than the linear approximation (10.18).) We may now correct the equilibrium equations (10.19) to take account of the change in geometry, obtaining a modified set of equations

p = C l P m (10.21)

the matrix Ct being a function of the displacements d1# In general, of course, the member end-loads pml will not satisfy the equilibrium conditions (10.21), indicating that the solution which we have obtained requires adjustment.

The next step is to obtain a linear approximation to equations (10.17) which is valid in the neighbourhood of the deformations em l. We write this in the form

Pm = Pmi + Kml(em - eml) (10.22)

where Kml represents the set of member stiffness matrices associated with small changes in the deformation vector em l. The matrix Kml corresponds to the slope of the load-extension curve at the point Pt in Fig. 10.4. Corresponding to (10.21) we

![image 254](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile254.png)

###### 246 MATRIX METHODS OF STRUCTURAL ANALYSIS

write the compatibility conditions in the modified form

###### em - eml = CUd - d,) (10.23)

—as mentioned at the beginning of this chapter, in the non-linear case the contragredient nature of force and displacement transformations only holds for small (strictly infinitesimal) displacements. Combining equations (10.21), (10.22) and (10.23) we obtain p = Cx(pml + KmlCf1(d — dx)), which may be written as

###### p - d pml = Cx Kml Ctfd - d,) (10.24)

Equation (10.24) may now be solved for the vector d — a\, which is essentially a correction to the first approximate set of displacements dx. Adding this correction to dt gives a new set of displacements d2, the corresponding member deformations em2 and member end-loads pm2 being found from equations (10.23) and (10.17) respectively.

The process may be repeated until a sufficient degree of convergence has been achieved. As in the single-variable example of the Newton-Raphson process we may measure the convergence by comparing successive displacement vectors, or alternatively we may consider successive member end-load vectors. In deciding on a suitable convergence criterion it should be remembered that in a numerical application of the method there will normally be random fluctuations in successive solutions due to rounding errors in the computation, so that "exact" mathematical convergence will never be achieved.

The method as we have described it calculates successive corrections which are added to the initial approximate solution dt. It is also possible to compute successive approximations rather than successive corrections by writing equation (10.24) in the form p - Cxpml + C1KmlC1d1 = C^K^C^d. The choice between the two approaches is merely a matter of computational convenience.

Although we have described an iterative method of analysing non-linear structures in terms of the equilibrium approach the

![image 255](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile255.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 247

compatibility method described in chapter 7 may equally well be used for the individual linear analyses. The use of the compatibility method may be particularly advantageous if it is desired to trace the development of a collapse mechanism in a rigid-jointed frame. As far as the equilibrium approach is concerned the appearance of plastic hinges merely makes the equations more illconditioned, but from a compatibility viewpoint each hinge reduces the degree of redundancy, the structure being determinate when the last hinge is about to form.

###### 10.4. The Analysis of Guyed Masts

As a simple example of the general technique described in the previous section we now consider the analysis of a transmission mast, supported by guys at a number of levels, under the action of vertical and wind loading. In this analysis we shall only consider non-linear effects due to the axial force in the mast and the load-extension characteristics of the guys—we shall ignore the effects of changes in overall geometry, although the analysis could readily be extended to cover these changes if necessary.

An example of a typical mast is shown in Fig. 10.6. As usual we shall imagine that the distributed loads on the mast due to wind pressure and dead weight have been replaced by concentrated loads applied at the joints, the term "joints" being used here to describe the points on the mast at which the guys are attached. Although a transmission mast is essentially a space structure, in practice it is legitimate to ignore torsional effects and vertical movements of the joints due to axial strains. Thus there are four degrees of freedom at each joint—one translation and one rotation in each of the two principal planes of bending. As far as the mast sections are concerned the deformations in these two planes are quite independent, although they may be coupled as far as the complete structure is concerned by guys which do not lie in either plane. Thus the stiffness matrices for the mast sections are identical with those developed in section 10.1, apart

![image 256](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile256.png)

###### 248

MATRIX METHODS OF STRUCTURAL ANALYSIS

FIG. 10.6. Example of a guyed mast.

P

###### X/// //

jr /

P\

^ ^ ^ I /7 ^" Limiting f/ j slope EA/L

Po I st approximation ^ * ί

2 nd approximation

###### ! ^

FIG. 10.7. Relation between the axial tension/? and the axial extension δ for a typical guy.

![image 257](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile257.png)

from the omission of the rows and columns associated with axial strains. If the moments of inertia about the two principal axes are different then there will of course be two different sets of matrices—one for each plane.

The axial tension in any guy, which we shall denote by p, is related to the axial extension δ by a curve which has the general form shown in Fig. 10.7. In the figure the condition (5 = 0 corresponds to the case where the upper end of the guy is attached to a joint whose displacement is zero. The corresponding tension pQ is a function of the erection tension (the erection being assumed to take place in still air conditions) and the wind pressure on the guy.

In practice each guy hangs in a catenary which is comparatively flat, and it is normal to use a parabolic approximation to the catenary when deriving the force-extension equations. This results in a cubic equation

p3 + p\a\2p\ - p0 - ΕΑδ/L) = a/2 (10.25)

where a is equal to EAWf/12, Wn being the total transverse loading on the cable due to wind and gravity forces. It will be noted that this is an implicit relation between p and δ, while equation (10.16) is essentially an explicit expression for/? in terms of <5. However, it is easy to solve equation (10.25) for any particular value of δ. From that equation it is also easy to show that the slope k of the ρ/δ curve (the stiffness of the guy at a particular load) is given by

dp EA p3

###### k-jr~7Ti <10·26>

As might be expected, this tends to the constant value EA/L when p is large, since in this condition the guy becomes almost straight.

We begin the analysis of a mast by treating it as a linear system, using the guy stiffnesses appropriate to the assumed initial

![image 258](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile258.png)

###### 250 MATRIX METHODS OF STRUCTURAL ANALYSIS

condition of zero joint displacements. Thus we imagine that each guy obeys the linear force-extension equation

P =>o + M (10.27)

which is transformed into system coordinates in the manner described in section 4.6. If p' = Tp and δ = Vd\ where p' and d' are the end-load and end-displacement vectors in system coordinates,! then equation (10.27) takes the form

p' = Tp0 + (Tk0T)d' (10.28) The stiffness matrices for each mast section may also be computed, using the value of axial thrust corresponding to the initial tensions p0 in the guys. Thus the load-displacement equations of the linearized structure may be set up in the form

p - p0 = K0d (10.29)

where p0 represents the vector formed from the various terms Tp0 which appear in the guy equations (10.28).

Equation (10.29) can now be solved to give an approximate set of displacements d1? and from these we can find the corresponding extension δί of each guy. Solving the cubic (10.25) for each guy with the appropriate value of δχ we obtain the corresponding force px. (As mentioned in the previous section it is not permissible to use the linear approximation (10.27) at this point, since this introduces an error into the analysis which is not corrected during later iterations.)

Having found the forces in the guys corresponding to the displacements dl9 we construct a new linearized force-extension equation for each guy p = py + kt(o — ÔJ, where the stiffness

kl is found by substituting pt into equation (10.26). If we put P* —Pi — fci^i this equation may be written as

p = p* + kxS (10.30)

t In this analysis system coordinates may conveniently be defined by taking the axis of the mast as the z axis, and making the xz and yz planes correspond to the principal planes of bending.

![image 259](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile259.png)

which is similar in form to equation (10.27). These equations for the guy forces may be transformed into system coordinates in the same way as before, giving

ρ'^Τρ*χ+(Τ^Ρ)ά' (10.31)

We also use the new guy tensions pt to compute corrected values for the thrusts in the various sections of the mast, and calculate new stiffness matrices for these sections based on the corrected thrusts.

Assembling the joint equilibrium equations in the usual way we obtain the load-displacement equations

p - p ^ M (10.32)

where pt represents the vector formed from the various terms Ίρ* which appear in the guy equations (10.31). Solving these

equations we obtain a second approximate solution d2, repeating the process until a satisfactory degree of convergence has been achieved. In practice the degree of non-linearity in the behaviour of a transmission mast is not great, and experience suggests that after four iterations the displacements and internal forces and moments are usually within 1 per cent of their final values.

It will be noted that the process has been described here in terms of successive approximations rather than as a series of corrections to a first approximation. This makes the assembly of equations (10.29) and (10.32) identical, which is convenient from a computer programming point of view, since it means that one cycle of machine instructions can be used for all iterations including the first.

If the joints of the structure are numbered in order 1, 2, ..., n then it is apparent that joint J is connected to earth by guys and to joints / + 1 and J — 1 by the adjacent mast sections. Thus the

successive stiffness matrices K0, Kl9 ..., of the linearized structure all have a very simple form, consisting of a leading diagonal of sub-matrices and two diagonals of sub-matrices on either side. Since all the guys have their lower ends anchored they merely

![image 260](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile260.png)

###### 252 MATRIX METHODS OF STRUCTURAL ANALYSIS

contribute direct stiffness coefficients to the leading diagonal terms. Thus the simultaneous equations (10.29) and (10.32) may be solved very rapidly. A computer program based on the analysis outlined in this section has been developed at Cambridge (Poskitt and Livesley, 1963). This will carry out a complete analysis involving 4 cycles of iteration for a mast stayed at 6 levels in less than a minute of total computing time.

###### 10.5. Some Problems of Collapse Analysis

As mentioned in section 10.2, it is common practice to estimate the actual collapse load of a structure from the rigid-plastic collapse load and the elastic critical load. As we have seen, both the latter parameters can be found relatively easily. However, it is natural to consider whether it is practicable to develop an analytical approach which determines the collapse load in a more direct manner.

There are two ways of tackling this problem. The first alternative is to take the rigid-plastic analysis presented in section 7.7 and modify it to include the effects of elastic deformations. The second is to take the method of finding critical loads described in section 10.2 and modify it to include the effects of plasticity. In this section we discuss some of the problems which arise in applying the second of these approaches to the collapse analysis of plane rigid-jointed frames. The general procedure is similar to that adopted in section 10.2. We imagine a structure to be acted on by a certain load system p, and carry out analyses for gradually increasing loadings λρ until λ reaches a value for which the load-displacement equations have either no solution or a solution which is unstable.

The methods of rigid-plastic analysis and elastic critical load analysis which we have described are both based on small-displacement theory, and the analysis given in this section is subject to the same restrictions. While the use of small-displacement theory in analysing a structure near to collapse is difficult to justify from

![image 261](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile261.png)

a purist point of view, it has the advantage of simplicity and makes it possible to retain the generality which is the virtue of the matrix equilibrium method. A more exact treatment makes the analysis a great deal more complicated, and so far it has only been attempted for single members and very simple frames.

The assumptions we shall make are as follows:

- (a) The deformations of the structure will be treated as "small" in the manner adopted in section 10.1. In particular we continue to neglect the axial shortening of a member due to curvature. This is reasonable in dealing with rigid-jointed frames, even under conditions near to collapse, since axial strains usually have little effect on the collapse load. In the case of hyperstatic trusses, however, axial shortening due to bending may cause considerable redistribution of the axial forces as collapse is approached, and thus affect the value of the collapse load. The method should therefore be applied with caution in such cases.
- (b) As in section 7.7, the position of the maximum moment in a member will be assumed to be at one or other of the ends. This may not be true in problems of local stanchion collapse, but it is a reasonable assumption in problems of overall collapse involving sidesway. If it is suspected that plasticity might develop at some point along the length of a member then an extra "joint" must be introduced at that point.
- (c) Plasticity is assumed to occur only at the positions of maximum moment, being localized in the form of plastic hinges. The shape factor is taken to be unity—i.e. the state at each end of a member is assumed to be one of purely elastic or purely plastic behaviour. If the condition is one of plasticity then the moment is assumed to be equal in magnitude to the fully plastic moment. The actual value of the fully plastic moment may be reduced by the presence of an axial force, but it is assumed to be independent of the amount of rotation at the hinge.


With these assumptions it is possible to extend the analysis given in section 10.1 to the case of a member with plastic hinges at either or both of its ends. The analysis is very similar to that

![image 262](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile262.png)

###### 254 MATRIX METHODS OF STRUCTURAL ANALYSIS

already given in section 5.7, where the stiffness matrices for a member with semi-rigid joints were derived. The load-displacement equations take the general form

###### * - * ι Λ + *„<, + *,* | (io33)

P2 = K21dl + #22^2 + mpC2 J

If the member is completely elastic then the vectors cl5 c2 are both zero and the equations are identical with equations (10.11). Otherwise the coefficients depend on the positions and signs of the plastic hinges. For example, if we have a member with a plastic hinge at end 1, so that rax = ±mp, then the stiffness matrices and the vectors cl9 c2 can be shown to be

'EAjL 0 0" 0 6£/Φ5/ί? - P/L 0 0 ~-EA\L

###### * 1 1 =

0 0_ 0 0 Ί

K'2i =

-6EI<PSIL3 + P/L 6ΕΙΦ5Ιΰ

0 0

###### 0 0 J

'EAjL

K22 =

0 0 Ί 0 6£/$5/L2-P/L -6ΕΙΦ5/ΰ 0

-6EI<P5/L2 6£/Φ5/Ζ._

###### cx = ± " 0 "

###### c 2 = ± " 0 "

###### -ΦΊ\Ε

Φι/L 1

. Φβ

where the sign of the vectors cu c2 is the same as the sign of mu and the functions Φ5, Φ6, and ΦΊ are given in terms of the Φ-functions defined in section 10.1 by Φ5 = Φ^ΙΦ^ Φ6 = Φ4/2Φ3, Φη = 1 + Φ6. Similar expressions may be obtained for other hinge conditions.

The analysis of a general structure may now be carried out by an

![image 263](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile263.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 255

iterative technique very similar to that described in section 10.3. We begin by assuming a set of axial forces Pt and compute stiffness matrices for the members on the assumption (say) that the structure is entirely elastic. This leads to a set of load-displacement equations p = K0d which are solved in the usual way to give a set of joint displacements d1# From these displacements we compute the internal forces and moments in the structure, obtaining as part of our results the end-moments and the axial thrust in each member. If now either of the calculated endmoments exceeds the fully plastic moment of the member we assume that a plastic hinge has formed at the corresponding end, and we construct the new load-displacement equations of the member in the appropriate form (10.33). In constructing these equations we use, of course, the new value of the axial thrust.

In this way we set up a new system of load-displacement equations for the structure

P - Pi = Κ^ (10.34)

where pt is the vector formed from the various terms mpcls etc. appearing in equations (10.33). From equation (10.34) we obtain

a new set of displacements d2, and the iterative process proceeds in the same way as before.

Although superficially the analysis presented in this section appears to be just a simple application of the general iterative method developed in section 10.3, it has one very important feature which is the main reason for including it in this chapter. In the transmission mast analysis discussed in the previous section we dealt with structural elements whose stiffness varied with displacement in a continuous manner. Our assumption of a unit shape factor in the present analysis means that a member is assumed to stay completely elastic until the full plastic moment is reached and then become completely plastic. Although this assumption simplifies the calculation of the individual member stiffness matrices, it implies a discontinuity in stiffness which may have a disastrous effect on the convergence of the iterative process. The process may in certain circumstances oscillate

![image 264](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile264.png)

###### 256 MATRIX METHODS OF STRUCTURAL ANALYSIS

indefinitely, while in others it may converge to an incorrect solution. For example, it may well happen that in the first iteration, in which the structure is treated as entirely elastic, the resulting internal load system violates the yield condition at some points which are not plastic hinges in the actual structure. Now any point at which the calculated elastic moment is greater than the appropriate fully plastic moment is treated as a plastic hinge during the second iteration, and if sufficient of these fictitious hinges appear then the load-displacement equations of the structure for the second iteration (10.34) will become singular, giving a false indication of collapse. It seems that these difficulties can be avoided, at the cost of some complication in the calculation of the member stiffness matrices, by making the stiffness coefficients vary in a more continuous way, and by giving the plastic hinges some small positive rotational stiffness —such a positive stiffness appears when a real member becomes plastic due to the presence of strain-hardening. In fact one may argue that the convergence troubles which have occurred in certain practical applications of the method are entirely due to the approximations which were initially introduced to "simplify" the analysis.

The process which we have described allows us to trace the gradual development of a collapse mechanism in a structure. This may easily be done on a computer by carrying out a series of analyses at gradually increasing load-factors, commencing at a loading at which the structure is purely elastic. Although this involves carrying out a whole series of non-linear analyses, the amount of work involved is considerably reduced by the fact that the solution varies with the load-factor in a continuous way. Thus one may extrapolate from the results of previous analyses and obtain a good approximation from which to start the analysis for the next load-factor. If at any point the process shows convergence troubles these may usually be cured by proceeding with smaller increments of loading. As the loading is increased plastic hinges will appear at various points in the structure, the load-

![image 265](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile265.png)

###### ANALYSIS OF NON-LINEAR STRUCTURES 257

displacement curve of the structure showing a discontinuity of slope each time a hinge appears. Eventually one of two things will happen. Either enough hinges will form to create a mechanism, or the remaining elastic structure will become unstable under the gradually increasing load, and collapse will occur before the full complement of hinges has formed. The latter phenomenon, known as the "deterioration of stability", has been discussed by Wood (Wood, 1957-8). In either case the structure remains stable as long as its stiffness matrix is positive definite, and it is easy to insert a test for this during the solution of the load-displacement equations. In the case of multi-storey singlebay rectangular frames the collapse loads predicted by a computer program based on this analysis are in good agreement with those obtained from model tests.

There is one important defect of the simple iterative procedure described in section 10.3. This approach proceeds to the true solution of a non-linear problem by means of a series of approximate solutions, and these solutions do not normally have any particular physical significance—they are merely part of a numerical process. Since in general the approximate solutions do not correspond to actual states of the real structure under load, the process cannot be used to analyse a non-conservative structure, where the solution depends not only on the loading but also on the loading history.

This means that we encounter difficulties if we use the method to analyse a non-linear structure in which a stress reversal occurs in material which has been deformed plastically. The difficulty may be illustrated by considering a structure which contains a bar whose elastic-plastic load-extension curve is shown in Fig. 10.8. Imagine that in two successive iterations we obtain two values of extension δ„ and δΒ+1, where δη+1 < δ,„ as shown in the figure. Now this may correspond to a true unloading of the bar, in which case we ought to follow the unloading curve XX' shown in the figure, using the slope of this line at X in the iteration which produces δη+1. On the other hand, the apparent reduction in dis-

![image 266](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile266.png)

placement may be merely a chance incident in the iteration process, without there being any unloading of the real bar at all. If this is so we clearly ought to follow the loading curve XX", and use the slope of this line at X in the iteration process.

###### x

/ * r / |

i / i / i /

' / i

###### xl * !

4, + i S„ Fxtension

FIG. 10.8. The effect of unloading in the plastic region.

To solve history-dependent problems of this sort it is necessary to trace the true behaviour of the structure as the actual loading program is carried out. This may be done by a sequence of nonlinear analyses, the procedure being similar to that described earlier for the elastic-plastic collapse analysis. After each increment δ p a check is made to see that the loading and unloading stiffnesses used are consistent with the signs of the computed changes in deformations.

This process is open to objection in that it does not follow the actual changes in deformation as Sp is applied. In fact it assumes that although the behaviour up to loading/» depends on how the loads are applied, this dependence may be ignored when considering the change in loading p. This seems to be reasonable provided that h p is sufficiently small, and is obviously a necessary assumption in any method which works with finite increments of loading.

![image 267](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile267.png)

###### References

###### (a) General Books on Matrix Methods of Structural Analysis

ARGYRIS, J. H. and KELSEY, S. (1960) Energy Theorems and Structural Analysis. Butterworths, London. BROTTON, D. M. (1962) The Application of Digital Computers to Structural Engineering Problems. Spon, London. HALL, A. S. and WOODHEAD, R. W. (2nd. ed., 1967) Frame Analysis. Wiley,

New York. MCMINN, S. J. (1962) Matrices for Structural Analysis. Spon, London. MORICE, P. B. (1959) Linear Structural Analysis. Thames and Hudson,

London.

PRZEMIENIECKI, J. S. (1968) Theory of Matrix Structural Analysis. McGrawHill, New York. An account of the historical development of matrix methods and a biblio-

graphy of the early literature will be found in the paper: ARGYRIS, J. H. (1958) Appl. Mech Rev. 11, 7, 331.

A bibliography which includes more recent work will be found in the book by Przemieinecki listed above.

###### (b) Books on Matrix Algebra and the Associated ComputingTechniques

AITKEN, A. C. (9th ed., 1958) Determinants and Matrices. Oliverand Boyd, Edinburgh. PIPES, L. A. (1958) Mathematics for Engineers and Physicists. McGraw-Hill, New York. RALSTON, A. and WILF, H. S. (1960) Mathematical Methods for Digital Computers. Wiley, New York. The Staff of the National Physical Laboratory (1961) Modern Computing Methods. H.M.S.O., London.

###### (c) References Quoted in the Text of this Book

ARCHER, J. S. (1963) Proc. Amer. Soc. Civil Engineers, 89, ST4, 161. CLOUGH, R. W., WILSON, E. L. and KING, I. P. (1963) Proc. Amer. Soc. Civil

Engineers, Z9, ST4, 179. DUNCAN, W. J. (1952) Quart. J. Mech. 5, 97. EISEMANN, K., Woo, L. and NAMYET, S. (1962) Proc. Amer. Soc. Civil

Engineers, 88, ST6, 245. FOULKES, J. (1954) Proc. Roy. Soc. Ser. A, 223, 482.

HALL, A. S. and WOODHEAD, R. W. (2nd ed., 1967) Frame Analysis, Ch. 9.

###### Wiley, New York. HENDERSON, J. C. DE C. and BICKLEY, W. G. (1955) Aircraft Engineering, 27, 400.

HESTENES, M. R. and STIEFEL, E. (1952) / . Res. Nat. Bur. Stand. 49, 409.

###### 259

![image 268](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile268.png)

HORNE, M. R. (1961) Progress in Solid Mechanics, Vol. 2, Ch. 7. NorthHolland, Amsterdam.

INSTITUTION OF STRUCTURAL ENGINEERS (1967) Report of a Committee on

Structural Computing, London. JENNINGS, A. (1966) The Computer J. 9, 281 KRÖN, G. (1944) /. Franklin Inst. 238, 6, 400. LECKIE, F. L. and LINDBERG, G. M. (1963) The Aeronautical Quart. 14, 224.

LECKIE, F. and PESTEL, E. (1960) Int. J. Mech. Sei. 2, 137. LIGHTFOOT, E. and SAWKO, F. (1959) Engineering, 187, 18.

LIVESLEY, R. K. (1960) The Computer J. 3, 34. LUNDQUIST, E. E. and KROLL, W. D. (1944) N.A.C.A. Report ARR No.

4B24. MERCHANT, W. (1954) The Struct. Engineer, 32, 185. MERCHANT, W. (1955) The Struct. Engineer, 33, 84. MORICE, P. B. (1959) Linear Structural Analysis, Ch 3. Thames and Hudson,

London. MYKLESTAD, N. O. (1944) /. Aero. Sei. 11, 153. NEAL, B. G. (2nd ed., 1963) The Plastic of Structural Analysis. Chapman

and Hall, London. OSTENFELD, A. (1926) Die Deformations Methode. Springer, Berlin. POSKITT, T. J. and LIVESLEY, R. K. (1963) Proc. Inst. Civil Engineers, 24, 373. PRZEMIENIECKI, J. S. (1968) Theory of Matrix Structural Analysis, Ch. 11.

McGraw-Hill, New York. SYNGE, J. L. (1951) Quart. Appl. Math. 9, 113. TARGOFF, W. P. (1947) J. Aero. Sei. 14, 579. WILSON, L. B. (1959) The Computer J. 2, 130. WOOD, R. H. (1957-8) Proc. Inst. Civil Engineers, 11, 69.

![image 269](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile269.png)

###### Index

Accuracy in linear analysis 203-214 in non-linear analysis 246

of a rigid-plastic rigid-jointed frame 171, 174-176

Compatibility equations 11,12, 5557, 64, 72, 121, 144, 213, 231, 246

Arches 106-109, 180-183 Automatic computers 3-5

auxiliary storage in 215-222 error detection in 211 operation times in 215, 252 programs for 4, 122-123, 164-

Compatibility method 11, 13, 134, 141-176, 208-210, 213, 226227, 247

Complementary energy 13 Connection matrices 121-140, 141145,166,230-231,245

165,174,199-203,211,252 routines for 4, 37, 41, 44, 200201, 214 storage of zero elements in 122123, 217-223 Axial forces 60,69, 83-84,164-167, 171, 232, 253 changes in bending stiffness due to 7, 232-235, 254 Axial shortening due to curvature 69, 235, 253 Axial strains in rigid-jointed frames 59, 68, 73, 164-167, 206-208

augmented 145, 150-151, 160, 167, 174 inversion of 128-129, 131-132,

135-140 Contragredience 57,121,246 Convergence of iterative processes

for solving non-linear systems 243,246,251,256-257 for solving sets of linear equations

24, 38, 208 Coordinate axes 15,16 frame or system 50 member 50 plane 49 space 47-48

Banded matrices 40, 77, 164, 214-

223, 251 Band-width 220 Branched tree structures 138

Coordinate transformations 16, 2931,50, 104 Coordinate transformation matrices

24-25 plane 62-63, 70-71, 130 space 79-80, 83, 84

Checking of computer output 211-

214 Collapse

Critical load, elastic 237-241 Curvature effects in initially straight members 69, 235, 253

of an elastic-plastic structure 247, 252-258 of a rigid-plastic pin-iointed truss 171, 173-174

261

![image 270](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile270.png)

262 INDEX

Deformation of a member 53-54, 61 Deformation vector

for joints 55-56, 74, 120-121, 125-126, 128-129, 141-145, 158,212,230-231,245

of a member 54,99-109,124,132 due to temperature changes

for members 54, 93-99, 123, 128, 175, 178

102

Equilibrium method 11-13, 58-91, 118-140, 149-150, 189-190, 203-208, 211-213, 214-229, 243-247

of a set of members 124-129, 145-147, 152, 166, 168, 230231,244-246

Degree of indeterminacy of a structure 142, 158-160

Equilibrium matrices, member 93-

103,106,111,126,131,178 Exchange of pivots 41

Degrees of freedom of a joint 47, 59 of a structure 13, 14, 141 Deterioration of stability 257 Determinacy, conditions for 11,

Fixed-end forces and moments 8-

10, 182, 227-228, 236 Flexibility 53, 107 Flexibility matrix

128-129, 134 Determinants 27, 32, 91, 198, 239 evaluation of 41 Determinate structures 11,117-118,

of a member 54, 99-114 of members connected in series

128-140, 172 Direction of a member 47, 68 Displacement method, see Equili-

106-114, 138, 153 of a set of members 125, 129, 132, 146-148

brium method Displacements 10,47-50

of a structure 54, 65, 67, 223 Flexible cables 7

associated with self-equilibrating load-pairs 146, 161-162 Distributed loads 8, 236 Distributed self-weight in vibrating

load-displacement equations of 248-251 Force method, see Compatibility method Frames, see Rigid-jointed structures

systems 90, 194-195 Dynamic loading problems 89-90

Grillages 81-83 Gross deformation 7, 231, 244-247 Guyed masts 247-252

Eigenvalues 31-37, 90-91 determination of by finding zeros of determinant 32, 91, 198 by Rayleigh's method 36, 37, 91 by repeated multiplication 3435,91 Eigenvectors 32-33, 37

Hyperstatic structures 11, 13, 88, 117, 128-129, 134, 142-176, 227

orthogonality of 33 Elastic centre 104 Electric network analysis 14, 29,47,

Ill-conditioned equations 28, 38, 39, 157, 160, 190-191, 198, 203-212, 242, 247

118-119,122,229 Equilibrium equations 7, 11

Instability 7, 24, 41, 237-241, 257

![image 271](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile271.png)

INDEX 263 Iterative methods

leading diagonal of 20, 41 inversion of 24-29, 41-43 multiplication of 20-21 multiplication of vectors by 19 null 20 orthogonal 28-29, 30-31 partitioned 23, 40, 65, 80-81 positive-definite 23, 33, 38, 41 singular 25-28 square 20 sum of 23 symmetric 21-22, 31-33, 40 transposition of 21, 29 unit 20, 24, 25, 42

for solving non-linear systems 241-258 for solving sets of linear equations 24, 37-38, 208

Joints 2, 46-47 fictitious 10, 172, 253 of finite size 110-111

Labelling conventions for joints and

members 46, 74 Lack of fit 87-89, 183 Linear theory of structures, approximations necessary for a 6-7, 57, 62, 68-69, 93-95, 99, 103, 122, 230-232, 252-253 Linear dependence 17, 27, 33, 192 Linear equations 6, 18, 37-41

Mechanisms 54, 128, 133, 159 of collapse 172-173, 176, 247,

256-257 Member coordinates 50 Member deformations 53-54, 61,

124 Member equilibrium equations 54, 93-99, 123, 128, 175, 178 Members in series 106-116, 138,

solution by elimination method 38-41,208, 215-223,224-225 Gauss-Seidel method 37-38, 208, 219 method of conjugate gradients, 219 relaxation methods 38 Linear programming 43-45, 171-

153, 163, 177-198 Mixed system analysis 169-170 Moment distribution 3, 24, 38, 85,

116

Natural frequencies of vibration 35, 90-91, 194-198 Newton-Raphson method

176 Loads 8-10, 47-49, 89-90 Load-displacement equations

for a single variable 241-243 for several variables 243-252 convergence of 243, 246, 251,

of a member 52, 74,102,119-120 with temperature stresses or

256-258 Non-conservative systems 257-258 Non-linear behaviour 6-7, 230-258

lack of fit 88-89, 102 of a set of members 11,12,120 of a structure 12, 23, 53, 54, 73-

due to non-linear elements 6, 230, 241-252 due to gross deformations 7,

77, 86-87, 90, 119-127, 245246

Lumped mass and inertia in vibration analysis 90, 194-195

230-231, 245-247 Non-uniform members 99-104

Partially rigid-jointed structures pin joints in 84-87, 159-160, 191-194

Matrices 18-45 congruent 31 diagonal 20,24,31,104

![image 272](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile272.png)

264 IMDEX

Secondary stresses in rigid-jointed trusses 67, 73

pinned foundation attachments in

87, 183, 194 Pin-jointed trusses, see Trusses Pivotal element 39-41 Pivotal row 39, 221-222 Plastic collapse, see Collapse Plastic hinges 112, 171-172, 174-

Self-equilibrating load pairs 51, 85, 144, 150-154, 173 Self-equilibrating load systems 88, 155-157, 160-164, 167-170, 174, 224-227

Semi-rigid joint connections 84-87, 111-116

176, 253-257 Plastic limit design 7, 45,171 Plasticity 6, 171-176, 252-258 Principal axes

Sign conventions for loads 48-^9,51-52 for displacements 47-49

of bending 77,247-249 of a matrix 31-37, 104

Slope-deflexion equations 69-70, 82

Programming 4, 215-223, 251 for repetitive problems 201-203 for single problems 199-201

with stability effects 232-236, 254 Stability functions 233-234, 254-

255 State vector 178 Stiffness 53, 241 Stiffness matrices

Quadratic form 23, 33-34

of a straight uniform member, in a plane grillage 81 -83 in a plane pin-jointed truss 60-

Rayleigh's principle 36, 37, 91 Reciprocal theorem 55, 61, 65,

64

101 Redundants 13, 14, 143-149 Relaxation methods 38 Release systems 134, 144-164,169-

in a plane rigid-jointed frame 68-71, 104-105 with stability effects 232-236 with plastic hinges 254

170, 210

in a space pin-jointed truss 83-84 in a space rigid-jointed frame 77-81 with a pin-joint at one end 115116 with semi-rigid joint connections 111-116 of a straight non-uniform member in a plane 103-104 of a general member 52-53, 99-103, 110-111

in the form of complete cuts 134, 144-154, 158-159, 162-164, 182

in the form of hinges 155-157, 247

Rigid-body displacements of a member 53-54, 61, 93, 97, 99101, 109

Rigid-jointed structures 73-77, 119129, 134-140, 149-154, 158159

plane 67-73, 85-87,155-157, 183, 232-237 space 77-83,214-223

of a flexible cable 249-251 Stiffness matrix

of a set of members 120,122-129, 133, 230, 244-246

Rings in rigid-jointed structures 134, 158-159, 162-164, 208209

of a structure 53, 65-67, 72-77, 85-87, 119-127,162-164,203208, 211-214,218-223,239

Rounding errors 41, 212-213, 246

![image 273](Livesley R. K., Matrix Methods of Structural 1964_images/imageFile273.png)

INDEX 265 Strain energy 12, 13, 23, 99-100,

Trusses plane pin-jointed 60-67, 129-

103-104 Sub-structures 223-229 Summation convention 17,18 Superposition 6, 7-10, 54, 99-101 System coordinates 50 Symmetry of stiffness and flexibility

133, 143-149 space pin-jointed 83-84, 133 secondary stresses in 67, 73 rigid-jointed, see Rigid-jointed

structures

matrices 55, 61, 64, 65, 75,

87, 101-102, 218

Vectors 15-18 length of 16 multiplication by scalar 16-17 orthogonal 17 scalar product of 17, 22 sum of 16 components of 16

Temperature stresses 87-89, 102,

125, 183 Torsional rigidity 78, 81-82 Transfer matrices 177-198

of a uniform member in a plane 179 of a loaded joint in a plane 180181, 184-185 of a joint in a plane vibrating system 196-197 Transfer matrix method, efficiency of 186-191,210-211 Tree structures 134-140, 151, 157, 158-159 with a single branch, 134-138 Triangular matrices 36-37,40,135140

Vibration analysis 89-91, 194-198 Virtual work 55-57, 63, 97, 121-

122, 127, 146, 152, 167-168, 231

Warping stiffness 78, 81

Zero elements, storage of 122-123, 2Î7-223.

