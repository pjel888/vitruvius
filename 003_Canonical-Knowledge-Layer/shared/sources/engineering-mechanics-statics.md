---
id: source-engineering-mechanics-statics-3th-ed-pytel-kiusalaas
title: Engineering Mechanics STATICS
page_type: source
trust_level: unknown
canonical_status: draft
source_relative_markdown_path: 006 -Structural/refined_markdown/Engineering Mechanics Statics 3th Ed Pytel Kiusalaas.md
last_canonicalized_utc: '2026-05-05T11:48:57.469142+00:00'
---

# Engineering Mechanics STATICS

## Overview

Automated summary withheld for Engineering Mechanics STATICS because the refined source includes image-heavy extraction. Review the Coverage headings and authoritative benchmark/reference sources before relying on summary prose.

## Coverage

- PART A: Analysis of Single Bodies
- PART B: Analysis of Composite Bodies
- PART C: Analysis of Plane Trusses
- PART A: Beams
- Part B: Cables

## Key Points

- (automated key points withheld because source-summary trust is low; review operative sections directly)

## Referenced Concepts

- concept-area-method
- concept-approved-budget-for-the-contract
- concept-floor-area-ratio

## Source Text

![image 1](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile1.png>)

### Engineering Mechanics STATICS

Third Edition

###### This page intentionally left blank

## Engineering Mechanics

## Statics

###### Third Edition

###### Andrew Pytel

The Pennsylvania State University

###### Jaan Kiusalaas

###### The Pennsylvania State University

Australia · Brazil · Japan · Korea · Mexico · Singapore · Spain · United Kingdom · United States

Engineering Mechanics: Statics, Third Edition Andrew Pytel and Jaan Kiusalaas

© 2010, 1999 Cengage Learning ALL RIGHTS RESERVED. No part of this work covered by the copyright herein may be reproduced, transmitted, stored or used in any form or by any means—graphic, electronic, or mechanical, including but not limited to photocopying, recording, scanning, digitizing, taping, Web distribution, information networks, information storage and retrieval systems, or in any other manner—except as many be permitted by the license terms herein.

Director, Global Engineering Program: Chris Carson

Senior Developmental Editor: Hilda Gowans

Editorial Assistant: Jennifer Dinsmore Marketing Specialist: Lauren Betsos Production Manager: Patricia Matthews Boies Content Project Manager: Darrell E. Frye Production Service: RPK Editorial Services Copyeditor: Pat Daly Proofreader: Martha McMaster Indexer: Ron Prottsman Compositor: Integra Senior Art Director: Michelle Kunkler Internal Designer: Carmela Periera Cover Designer: Andrew Adams Cover Image: David H. Seymour/ Shutterstock Photo Permissions Researcher: Kristiina Bowering Image Permission Manager: Don Schlotman Senior First Print Buyer: Doug Wilke

|For product information and technology assistance, contact us at Cengage Learning Customer & Sales Support, 1-800-354-9706.<br><br>For permission to use material from this text or product, submit all requests online at www.cengage.com/permissions. Further permissions questions can be emailed to permissionrequest@cengage.com.|
|---|

Library of Congress Control Number: 2009920813 Student Edition: ISBN-13: 978-0-495-24469-1 ISBN-10: 0-495-24469-4

Cengage Learning 200 First Stamford Place, Suite 400 Stamford, CT 06902 USA

Cengage Learning is a leading provider of customized learning solutions with ofﬁce locations around the globe, including Singapore, the United Kingdom, Australia, Mexico, Brazil, and Japan. Locate your local ofﬁce at: international.cengage.com/region.

Cengage Learning products are represented in Canada by Nelson Education Ltd.

For your course and learning solutions, visit www.cengage.com/engineering. Purchase any of our products at your local college store or at our preferred online store www.ichapters.com.

Printed in Canada 1 2 3 4 5 6 7 13 12 11 10 09

###### To Jean, Leslie, Lori, John, Nicholas and To Judy, Nicholas, Jennifer, Timothy

###### This page intentionally left blank

### Contents

Preface xi

- Chapter 1 Introduction to Statics 1

- 1.1 Introduction 1
- 1.2 Newtonian Mechanics 3
- 1.3 Fundamental Properties of Vectors 10
- 1.4 Representation of Vectors Using Rectangular Components 18
- 1.5 Vector Multiplication 27

- Chapter 2 Basic Operations with Force Systems 37

- 2.1 Introduction 37
- 2.2 Equivalence of Vectors 37
- 2.3 Force 38
- 2.4 Reduction of Concurrent Force Systems 39
- 2.5 Moment of a Force about a Point 49
- 2.6 Moment of a Force about an Axis 60
- 2.7 Couples 73
- 2.8 Changing the Line of Action of a Force 86

- Chapter 3 Resultants of Force Systems 97

- 3.1 Introduction 97
- 3.2 Reduction of a Force System to a Force and a Couple 97
- 3.3 Deﬁnition of Resultant 105
- 3.4 Resultants of Coplanar Force Systems 106
- 3.5 Resultants of Three-Dimensional Systems 116
- 3.6 Introduction to Distributed Normal Loads 128

- Chapter 4 Coplanar Equilibrium Analysis 143

- 4.1 Introduction 143
- 4.2 Deﬁnition of Equilibrium 144 Part A: Analysis of Single Bodies 144
- 4.3 Free-Body Diagram of a Body 144
- 4.4 Coplanar Equilibrium Equations 153
- 4.5 Writing and Solving Equilibrium Equations 155
- 4.6 Equilibrium Analysis for Single-Body Problems 166 vii

###### viii Contents

- Part B: Analysis of Composite Bodies 179

- 4.7 Free-Body Diagrams Involving Internal Reactions 179
- 4.8 Equilibrium Analysis of Composite Bodies 190
- 4.9 Special Cases: Two-Force and Three-Force Bodies 200

Part C: Analysis of Plane Trusses 214

- 4.10 Description of a Truss 214
- 4.11 Method of Joints 215
- 4.12 Method of Sections 224

###### Chapter 5 Three-Dimensional Equilibrium 237

- 5.1 Introduction 237
- 5.2 Deﬁnition of Equilibrium 238
- 5.3 Free-Body Diagrams 238
- 5.4 Independent Equilibrium Equations 249
- 5.5 Improper Constraints 252
- 5.6 Writing and Solving Equilibrium Equations 253
- 5.7 Equilibrium Analysis 263

###### Chapter 6 Beams and Cables 281

- *6.1 Introduction 281

- Part A: Beams 282

- *6.2 Internal Force Systems 282
- *6.3 Analysis of Internal Forces 291
- *6.4 Area Method for Drawing V- and M-Diagrams 303

- Part B: Cables 318

- *6.5 Cables under Distributed Loads 318
- *6.6 Cables under Concentrated Loads 330

###### Chapter 7 Dry Friction 341

- 7.1 Introduction 341
- 7.2 Coulomb’s Theory of Dry Friction 342
- 7.3 Problem Classiﬁcation and Analysis 345
- 7.4 Impending Tipping 361
- 7.5 Angle of Friction; Wedges and Screws 369

- *7.6 Ropes and Flat Belts 379
- *7.7 Disk Friction 386
- *7.8 Rolling Resistance 391

###### Chapter 8 Centroids and Distributed Loads 401

- 8.1 Introduction 401
- 8.2 Centroids of Plane Areas and Curves 401
- 8.3 Centroids of Curved Surfaces, Volumes, and Space Curves 419
- 8.4 Theorems of Pappus-Guldinus 438
- 8.5 Center of Gravity and Center of Mass 442
- 8.6 Distributed Normal Loads 450

*Indicates optional articles

Contents ix

###### Chapter 9 Moments and Products of Inertia of Areas 471

- 9.1 Introduction 471
- 9.2 Moments of Inertia of Areas and Polar Moments of Inertia 472
- 9.3 Products of Inertia of Areas 492
- 9.4 Transformation Equations and Principal Moments of Inertia of Areas 500

- *9.5 Mohr’s Circle for Moments and Products of Inertia 508

Chapter 10 Virtual Work and Potential Energy 523

- *10.1 Introduction 523
- *10.2 Virtual Displacements 524
- *10.3 Virtual Work 525
- *10.4 Method of Virtual Work 528
- *10.5 Instant Center of Rotation 539
- *10.6 Equilibrium and Stability of Conservative Systems 548

###### Appendix A Numerical Integration 559

- A.1 Introduction 559
- A.2 Trapezoidal Rule 560
- A.3 Simpson’s Rule 560

###### Appendix B Finding Roots of Functions 563

- B.1 Introduction 563
- B.2 Newton’s Method 563
- B.3 Secant Method 564

###### Appendix C Densities of Common Materials 567 Answers to Even-Numbered Problems 569 Index 576

###### This page intentionally left blank

### Preface

Statics and dynamics are basic subjects in the general ﬁeld known as engineering mechanics. At the risk of oversimplifying, engineering mechanics is that branch of engineering that is concerned with the behavior of bodies under the action of forces. Statics and dynamics form the basis for many of the traditional ﬁelds of engineering, such as automotive engineering, civil engineering, and mechanical engineering. In addition, these subjects often play fundamental roles when the principles of mechanics are applied to such diverse ﬁelds as medicine and biology. Applying the principles of statics and dynamics to such a wide range of applications requires reasoning and practice rather than memorization. Although the principles of statics and dynamics are relatively few, they can only be truly mastered by studying and analyzing problems. Therefore, all modern textbooks, including ours, contain a large number of problems to be solved by the student. Learning the engineering approach to problem solving is one of the more valuable lessons to be learned from the study of statics and dynamics.

We have made every effort to improve our presentation without compromising the following principles that formed the basis of the previous editions.

- • Each sample problem is carefully chosen to help students master the intricacies of engineering problem analysis.
- • The selection of homework problems is balanced between “textbook” problems that illustrate the principles of engineering mechanics in a straight-forward manner, and practical engineering problems that are applicable to engineering design.
- • The number of problems using U.S. Customary Units and SI Units are approximately equal.
- • The importance of correctly drawn free-body diagrams is emphasized throughout.
- • We continue to present equilibrium analysis in three separate articles, each followed by a set of problems. The ﬁrst article teaches the method for drawing free-body diagrams. The second shows how to write and solve the equilibrium equations using a given free-body diagram. The third article combines the two techniques just learned to arrive at a logical plan for the complete analysis of an equilibrium problem.
- • Whenever applicable, the number of independent equations is compared to the number of unknown quantities before the governing equations are written.
- • Review Problems appear at the end of chapters to encourage students to synthesize the individual topics they have been learning.

###### xi

###### xii Preface

We have included several optional topics, which are marked with an asterisk (*). Due to time constraints, topics so indicated can be omitted without jeopardizing the presentation of the subject. An asterisk is also used to indicate problems that require advanced reasoning. Articles, sample problems, and problems associated with numerical methods are preceded by an icon representing a computer disk.

![image 2](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile2.png>)

In this third edition, we have made a number of signiﬁcant improvements based upon the feedback received from students and faculty who have used the previous editions. In addition, we have incorporated many of the suggestions provided by the reviewers of the second edition.

A number of articles have been reorganized, or rewritten, to make the topics easier for the student to understand. For example, our presentation of beam analysis in Chapter 6 has been completely rewritten and includes both revised sample problems and revised problems. Our discussion of beams now more clearly focuses upon the methods and terminology used in the engineering analysis and design of beams. Also, the topic of rolling resistance has been added to Chapter 7. Furthermore, our discussion of virtual displacements in Chapter 10 has been made more concise and therefore will be easier for the students to understand. New to this edition, sections entitled Review of Equations have been added at the end of each chapter as a convenience for students as they solve the problems.

The total numbers of sample problems and problems remain about the same as in the previous edition; however, the introduction of two colors improves the overall readability of the text and artwork. Compared with the previous edition, approximately one-third of the problems is new, or has been modiﬁed.

Ancillary Study Guide to Accompany Pytel and Kiusalaas Engineering Mechanics, Statics, Third Edition, J.L. Pytel and A. Pytel, 2010. The goals of this study guide are two-fold. First, self-tests are included to help the student focus on the salient features of the assigned reading. Second, the study guide uses “guided” problems that give the student an opportunity to work through representative problems, before attempting to solve the problems in the text.

Acknowledgments We are grateful to the following reviewers for their valuable suggestions:

K.L. Devries, University of Utah Kurt Gramoll, University of Oklahoma Scott L. Hendricks, Virginia Tech Laurence Jacobs, Georgia Institute of Technology Chad M. Landis, Rice University Jim G. LoCascio, California Polytechnic State University,

San Luis Obispo Thomas H. Miller, Oregon State University Robert G. Oakberg, Montana State University Scott D. Schiff, Clemson University

ANDREW PYTEL JAAN KIUSALAAS

# 1

### Introduction to Statics

![image 3](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile3.png>)

The Flemish mathematician and engineer Simon Stevinus (1548–1620) was the ﬁrst to demonstrate resolution of forces, thereby establishing the foundation of modern statics. © Bettmann/CORBIS

###### 1.1 Introduction

###### a. What is engineering mechanics?

Statics and dynamics are among the ﬁrst engineering topics encountered by most students. Therefore, it is appropriate that we begin with a brief exposition on the meaning of the term engineering mechanics and on the role that these courses play in engineering education. Before deﬁning engineering mechanics, we must ﬁrst consider the similarities and differences between physics and engineering.

In general terms, physics is the science that relates the properties of matter and energy, excluding biological and chemical effects. Physics includes the study

###### 1

of mechanics,* thermodynamics, electricity and magnetism, and nuclear physics. On the other hand, engineering is the application of the mathematical and physical sciences (physics, chemistry, and biology) to the design and manufacture of items that beneﬁt humanity. Design is the key concept that distinguishes engineers from scientists. According to the Accreditation Board for Engineering and Technology (ABET), engineering design is the process of devising a system, component, or process to meet desired needs.

Mechanics is the branch of physics that considers the action of forces on bodies or ﬂuids that are at rest or in motion. Correspondingly, the primary topics of mechanics are statics and dynamics. The ﬁrst topic that you studied in your initial physics course, in either high school or college, was undoubtedly mechanics. Thus, engineering mechanics is the branch of engineering that applies the principles of mechanics to mechanical design (i.e., any design that must take into account the effect of forces). The primary goal of engineering mechanics courses is to introduce the student to the engineering applications of mechanics. Statics and Dynamics are generally followed by one or more courses that introduce material properties and deformation, usually called Strength of Materials or Mechanics of Materials. This sequence of courses is then followed by formal training in mechanical design.

Of course, engineering mechanics is an integral component of the education of engineers whose disciplines are related to the mechanical sciences, such as aerospace engineering, architectural engineering, civil engineering, and mechanical engineering. However, a knowledge of engineering mechanics is also useful in most other engineering disciplines, because there, too, the mechanical behavior of a body or ﬂuid must often be considered. Because mechanics was the ﬁrst physical science to be applied to everyday life, it follows that engineering mechanics is the oldest branch of engineering. Given the interdisciplinary character of many engineering applications (e.g., robotics and manufacturing), a sound training in engineering mechanics continues to be one of the more important aspects of engineering education.

###### b. Problem formulation and the accuracy of solutions

Your mastery of the principles of engineering mechanics will be reﬂected in your ability to formulate and solve problems. Unfortunately, there is no simple method for teaching problem-solving skills. Nearly all individuals require a considerable amount of practice in solving problems before they begin to develop the analytical skills that are so necessary for success in engineering. For this reason, a relatively large number of sample problems and homework problems are placed at strategic points throughout this text.

To help you develop an “engineering approach” to problem analysis, you will ﬁnd it instructive to divide your solution for each homework problem into the following parts:

- 1. GIVEN: After carefully reading the problem statement, list all the data provided. If a ﬁgure is required, sketch it neatly and approximately to scale.
- 2. FIND: State precisely the information that is to be determined.

*When discussing the topics included in physics, the term mechanics is used without a modiﬁer. Quite naturally, this often leads to confusion between “mechanics” and “engineering mechanics.”

- 3. SOLUTION: Solve the problem, showing all the steps that you used in the analysis. Work neatly so that your work can be easily followed by others.
- 4. VALIDATE: Many times, an invalid solution can be uncovered by simply asking yourself, “Does the answer make sense?”

When reporting your answers, use only as many digits as the least accurate value in the given data. For example, suppose that you are required to convert 12500ft (assumed to be accurate to three signiﬁcant digits) to miles. Using a calculator, you would divide 12500ft by 5280ft/mi and report the answer as 2.37mi (three signiﬁcant digits), although the quotient displayed on the calculator would be 2.3674242. Reporting the answer as 2.3674242 implies that all eight digits are signiﬁcant, which is, of course, untrue. It is your responsibility to round off the answer to the correct number of digits. In this text, you should assume that given data are accurate to three signiﬁcant digits unless stated otherwise. For example, a length that is given as 3ft should be interpreted as 3.00ft.

When performing intermediate calculations, a good rule of thumb is to carry one more digit than will be reported in the ﬁnal answer; for example, use four-digit intermediate values if the answer is to be signiﬁcant to three digits. Furthermore, it is common practice to report four digits if the ﬁrst digit in an answer is 1; for example, use 1.392 rather than 1.39.

###### 1.2 Newtonian Mechanics

###### a. Scope of Newtonian mechanics

In 1687 Sir Isaac Newton (1642–1727) published his celebrated laws of motion in Principia (Mathematical Principles of Natural Philosophy). Without a doubt, this work ranks among the most inﬂuential scientiﬁc books ever published. We should not think, however, that its publication immediately established classical mechanics. Newton’s work on mechanics dealt primarily with celestial mechanics and was thus limited to particle motion. Another two hundred or so years elapsed before rigid-body dynamics, ﬂuid mechanics, and the mechanics of deformable bodies were developed. Each of these areas required new axioms before it could assume a usable form.

Nevertheless, Newton’s work is the foundation of classical, or Newtonian, mechanics. His efforts have even inﬂuenced two other branches of mechanics, born at the beginning of the twentieth century: relativistic and quantum mechanics. Relativistic mechanics addresses phenomena that occur on a cosmic scale (velocities approaching the speed of light, strong gravitational ﬁelds, etc.). It removes two of the most objectionable postulates of Newtonian mechanics: the existence of a ﬁxed or inertial reference frame and the assumption that time is an absolute variable, “running” at the same rate in all parts of the universe. (There is evidence that Newton himself was bothered by these two postulates.) Quantum mechanics is concerned with particles on the atomic or subatomic scale. It also removes two cherished concepts of classical mechanics: determinism and continuity. Quantum mechanics is essentially a probabilistic theory; instead of predicting an event, it determines the likelihood that an event will occur. Moreover, according to this theory, the events occur in discrete steps (called quanta) rather than in a continuous manner.

Relativistic and quantum mechanics, however, have by no means invalidated the principles of Newtonian mechanics. In the analysis of the motion of bodies encountered in our everyday experience, both theories converge on the equations of Newtonian mechanics. Thus the more esoteric theories actually reinforce the validity of Newton’s laws of motion.

###### b. Newton’s laws for particle motion

Using modern terminology, Newton’s laws of particle motion may be stated as follows:

- 1. If a particle is at rest (or moving with constant velocity in a straight line), it will remain at rest (or continue to move with constant velocity in a straight line) unless acted upon by a force.
- 2. A particle acted upon by a force will accelerate in the direction of the force. The magnitude of the acceleration is proportional to the magnitude of the force and inversely proportional to the mass of the particle.
- 3. For every action, there is an equal and opposite reaction; that is, the forces of interaction between two particles are equal in magnitude and oppositely directed along the same line of action.

Although the ﬁrst law is simply a special case of the second law, it is customary to state the ﬁrst law separately because of its importance to the subject of statics.

###### c. Inertial reference frames

When applying Newton’s second law, attention must be paid to the coordinate system in which the accelerations are measured. An inertial reference frame (also known as a Newtonian or Galilean reference frame) is deﬁned to be any rigid coordinate system in which Newton’s laws of particle motion relative to that frame are valid with an acceptable degree of accuracy. In most design applications used on the surface of the earth, an inertial frame can be approximated with sufﬁcient accuracy by attaching the coordinate system to the earth. In the study of earth satellites, a coordinate system attached to the sun usually sufﬁces. For interplanetary travel, it is necessary to use coordinate systems attached to the so-called ﬁxed stars.

It can be shown that any frame that is translating with constant velocity relative to an inertial frame is itself an inertial frame. It is a common practice to omit the word inertial when referring to frames for which Newton’s laws obviously apply.

###### d. Units and dimensions

The standards of measurement are called units. The term dimension refers to the type of measurement, regardless of the units used. For example, kilogram and feet/second are units, whereas mass and length/time are dimensions. Throughout this text we use two standards of measurement: U.S. Customary system and SI system (from Système internationale d’unités). In the U.S. Customary system the base (fundamental) dimensions* are force [F], length [L], and time [T]. The corresponding base units are pound (lb), foot (ft), and second (s). The base dimensions in the SI system are mass [M], length [L], and time [T], and the base units

*We follow the established custom and enclose dimensions in brackets.

are kilogram (kg), meter (m), and second (s). All other dimensions or units are combinations of the base quantities. For example, the dimension of velocity is [L/T], the units being ft/s, m/s, and so on.

A system with the base dimensions [FLT] (such as the U.S. Customary system) is called a gravitational system. If the base dimensions are [MLT] (as in the SI system), the system is known as an absolute system. In each system of measurement, the base units are deﬁned by physically reproducible phenomena or physical objects. For example, the second is deﬁned by the duration of a speciﬁed number of radiation cycles in a certain isotope, the kilogram is deﬁned as the mass of a certain block of metal kept near Paris, France, and so on.

All equations representing physical phenomena must be dimensionally homogeneous; that is, each term of an equation must have the same dimension. Otherwise, the equation will not make physical sense (it would be meaningless, for example, to add a force to a length). Checking equations for dimensional homogeneity is a good habit to learn, as it can reveal mistakes made during algebraic manipulations.

###### e. Mass, force, and weight

If a force F acts on a particle of mass m, Newton’s second law states that

###### F=ma (1.1)

where a is the acceleration vector of the particle. For a gravitational [FLT] system, dimensional homogeneity of Eq. (1.1) requires the dimension of mass to be

FT2 L

(1.2a)

[M]=

In the U.S. Customary system, the derived unit of mass is called a slug. A slug is deﬁned as the mass that is accelerated at the rate of 1.0ft/s2 by a force of 1.0lb. Substituting units for dimensions in Eq. (1.2a), we get for the unit of a slug

1.0slug=1.0lb·s2/ft

For an absolute [MLT] system of units, dimensional homogeneity of Eq. (1.1) yields for the dimension of force

ML T2

(1.2b)

[F]=

The derived unit of force in the SI system is a newton (N), deﬁned as the force that accelerates a 1.0-kg mass at the rate of 1.0 m/s2. From Eq. (1.2b), we obtain

1.0N=1.0kg·m/s2

Weight is the force of gravitation acting on a body. Denoting gravitational acceleration (free-fall acceleration of the body) by g, the weight W of a body of mass m is given by Newton’s second law as

###### W =mg (1.3)

Note that mass is a constant property of a body, whereas weight is a variable that depends on the local value of g. The gravitational acceleration on the surface of the earth is approximately 32.2 ft/s2, or 9.81m/s2. Thus the mass of a body that weighs 1.0 lb on earth is (1.0lb)/(32.2ft/s2)=1/32.2 slug. Similarly, if the mass of a body is 1.0 kg, its weight on earth is (9.81 m/s2)(1.0 kg)=9.81 N.

At one time, the pound was also used as a unit of mass. The pound mass (lbm) was deﬁned as the mass of a body that weighs 1.0lb on the surface of the earth. Although pound mass is an obsolete unit, it is still used occasionally, giving rise to confusion between mass and weight. In this text, we use the pound exclusively as a unit of force.

###### f. Conversion of units

A convenient method for converting a measurement from one set of units to another is to multiply the measurement by appropriate conversion factors. For example, to convert 240mi/h into ft/s, we proceed as follows:

1.0 h 3600s ×

5280ft 1.0 mi = 352 ft/s

mi h ×

240mi/h=240

where the multipliers 1.0h/3600s and 5280ft/1.0mi are conversion factors. Because 1.0h=3600s and 5280ft=1.0mi, we see that each conversion factor is dimensionless and of magnitude 1. Therefore, a measurement is unchanged when it is multiplied by conversion factors—only its units are altered. Note that it is permissible to cancel units during the conversion as if they were algebraic quantities.

Conversion factors applicable to mechanics are listed inside the front cover of the book.

###### g. Law of gravitation

In addition to his many other accomplishments, Newton also proposed the law of universal gravitation. Consider two particles of mass mA and mB that are separated by a distance R, as shown in Fig. 1.1. The law of gravitation states that the

mB

R

two particles are attracted to each other by forces of magnitude F that act along the line connecting the particles, where

F

mA F

mAmB R2

(1.4)

F = G

Fig. 1.1

The universal gravitational constant G is equal to 3.44×10−8 ft4/(lb · s4), or 6.67× 10−11 m3/(kg·s2). Although this law is valid for particles, Newton showed that it is also applicable to spherical bodies, provided that their masses are distributed uniformly. (When attempting to derive this result, Newton was forced to develop calculus.)

If we let mA = Me (the mass of the earth), mB =m (the mass of a body), and R = Re (the mean radius of the earth), then F in Eq. (1.4) will be the weight W of the body. Comparing W = GMem/Re2 with W =mg, we ﬁnd that g = GMe/Re2. Of course, adjustments may be necessary in the value of g for some applications in order to account for local variation of the gravitational attraction.

|Sample Problem 1.1<br><br>Convert 5000lb/in.2 to Pa (1Pa=1N/m2).<br><br>Solution<br><br>Using the conversion factors listed inside the front cover, we obtain<br><br>5000lb/in.2 = 5000<br><br>lb in.2 ×<br><br>4.448N 1.0 lb ×<br><br>39.37 in. 1.0m<br><br>2<br><br>= 34.5 × 106 N/m2 = 34.5MPa Answer<br><br>Sample Problem 1.2<br><br>The acceleration a of a particle is related to its velocity v, its position coordinate x, and time t by the equation<br><br>a = Ax3t + Bvt2 (a)<br><br>where A and B are constants. The dimension of the acceleration is length per unit time squared; that is, [a]=[L/T2]. The dimensions of the other variables are [v]=[L/T], [x]=[L], and [t]=[T]. Derive the dimensions of A and B if Eq. (a) is to be dimensionally homogeneous.<br><br>Solution<br><br>For Eq. (a) to be dimensionally homogeneous, the dimension of each term on the right-hand side of the equation must be [L/T2], the same as the dimension for a. Therefore, the dimension of the ﬁrst term on the right-hand side of Eq. (a) becomes<br><br>[Ax3t]=[A][x3][t]=[A][L3][T]=<br><br>L T2<br><br>(b)<br><br>Solving Eq.(b) for the dimension of A, we ﬁnd<br><br>[A]=<br><br>1 [L3][T]<br><br>L T2 =<br><br>1 [L2T3]<br><br>Answer|
|---|

###### 7

|Performing a similar dimensional analysis on the second term on the righthand side of Eq. (a) gives<br><br>[Bvt2]=[B][v][t2]=[B]<br><br>L T [T2]=<br><br>L T2<br><br>(c)<br><br>Solving Eq. (c) for the dimension of B, we ﬁnd<br><br>[B]=<br><br>L T2<br><br>T L<br><br>1<br><br>T2 =<br><br>1 T3<br><br>Answer<br><br>Sample Problem 1.3<br><br>Find the gravitational force exerted by the earth on a 70-kg man whose elevation above the surface of the earth equals the radius of the earth. The mass and radius of the earth are Me =5.9742 × 1024 kg and Re =6378 km, respectively.<br><br>Solution<br><br>Consider a body of mass m located at the distance 2Re from the center of the earth (of mass Me). The law of universal gravitation, from Eq. (11.4), states that the body is attracted to the earth by the force F given by<br><br>F = G<br><br>mMe (2Re)2<br><br>where G =6.67 × 10−11 m3/(kg·s2) is the universal gravitational constant. Substituting the values for G and the given parameters, the earth’s gravitational force acting on the 70-kg man is<br><br>F =(6.67 × 10−11)<br><br>(70)(5.9742 × 1024) [2(6378 × 103)]2<br><br>=171.4 N Answer|
|---|

###### 8

1.1–1.21 Problems 9

![image 4](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile4.png>)

###### Problems

- 1.1 A person weighs 30lb on the moon, where g = 5.32 ft/s2. Determine (a) the mass of the person and (b) the weight of the person on earth.
- 1.2 The radius and length of a steel cylinder are 60mm and 120 mm, respectively. If the mass density of steel is 7850kg/m3, determine the weight of the cylinder in pounds.
- 1.3 Convert the following: (a) 400lb·ft to kN·m; (b) 6m/s to mi/h; (c) 20lb/in.2 to kPa; and (d) 500slug/in. to kg/m.
- 1.4 The mass moment of inertia of a certain body is I = 20 kg · m2. Express I in terms of the base units of the U.S. Customary system.
- 1.5 The kinetic energy of a car of mass m moving with velocity v is E = mv2/2. If m = 1000kg and v = 6m/s, compute E in (a) kN · m; and (b) lb · ft.
- 1.6 In a certain application, the acceleration a and the position coordinate x of a particle are related by

a =

gkx W

where g is the gravitational acceleration, k is a constant, and W is the weight of the particle. Show that this equation is dimensionally consistent if the dimension of k is [F/L].

- 1.7 When a force F acts on a linear spring, the elongation x of the spring is given by F =kx, where k is called the stiffness of the spring. Determine the dimension of k in terms of the base dimensions of an absolute [MLT] system of units.
- 1.8 In some applications dealing with very high speeds, the velocity is measured in mm/µs. Convert 25mm/µs into (a) m/s; and (b) mi/h.
- 1.9 A geometry textbook gives the equation of a parabola as y = x2, where x and y are measured in inches. How can this equation be dimensionally correct?
- 1.10 The mass moment of inertia I of a homogeneous sphere about its diameter is I =(2/5)mR2, where m and R are its mass and radius, respectively. Find the dimension of I in terms of the base dimensions of (a) a gravitational [FLT] system and (b) an absolute [MLT] system.
- 1.11 The position coordinate x of a particle is determined by its velocity v and the elapsed time t as follows: (a) x = At2−Bvt; and (b) x = Avte−Bt. Determine the dimensions of constants A and B in each case, assuming the expressions to be dimensionally correct.

∗1.12 In a certain vibration problem the differential equation describing the motion of a particle of mass m is

d2x dt2 + c

dx dt + kx = P0 sinωt

m

where x is the displacement of the particle and t is time. What are the dimensions of the constants c, k, P0, and ω in terms of the base dimensions of a gravitational [FLT] system?

- 1.13 Using Eq. (1.4), derive the dimensions of the universal gravitational constant G in terms of the base dimensions of (a) a gravitational [FLT] system; and (b) an absolute [MLT] system.
- 1.14 The typical power output of a compact car engine is 120hp. What is the equivalent power in (a) lb · ft/s; and (b) kW?
- 1.15 Two 10-kg spheres are placed 500mm apart. Express the gravitational attraction acting on one of the spheres as a percentage of its weight on earth.
- 1.16 Two identical spheres of radius 8in. and weighing 2lb on the surface of the earth are placed in contact. Find the gravitational attraction between them.

Use the following data for Problems 1.17–1.21: mass of earth = 5.9742×1024 kg, radius of earth = 6378 km, mass of moon = 0.073483 × 1024 kg, radius of moon = 1737 km.

- 1.17 A man weighs 180lb on the surface of the earth. Compute his weight in an airplane ﬂying at an elevation of 30 000ft.
- 1.18 Use Eq. (1.4) to show that the weight of an object on the moon is approximately 1/6 its weight on earth.
- 1.19 Plot the earth’s gravitational acceleration g (m/s2) against the height h (km) above the surface of the earth.
- 1.20 Find the elevation h (km) where the weight of an object is one-tenth its weight on the surface of the earth.
- 1.21 Calculate the gravitational force between the earth and the moon in newtons. The distance between the earth and the moon is 384 × 103 km.

###### 1.3 Fundamental Properties of Vectors

A knowledge of vectors is a prerequisite for the study of statics. In this article, we describe the fundamental properties of vectors, with subsequent articles discussing some of the more important elements of vector algebra. (The calculus of vectors will be introduced as needed in Dynamics.) We assume that you are already familiar with vector algebra—our discussion is intended only to be a review of the basic concepts.

The differences between scalar and vector quantities must be understood:

A scalar is a quantity that has magnitude only. A vector is a quantity that possesses magnitude and direction and obeys the parallelogram law for addition.

Because scalars possess only magnitudes, they are real numbers that can be positive, negative, or zero. Physical quantities that are scalars include temperature, time, and speed. As shown later, force, velocity, and displacement are examples of physical quantities that are vectors. The magnitude of a vector is always taken to be a nonnegative number. When a vector represents a physical quantity, the units of the vector are taken to be the same as the units of its magnitude (pounds, meters per second, feet, etc.).

The algebraic notation used for a scalar quantity must, of course, be different from that used for a vector quantity. In this text, we adopt the following conventions: (1) scalars are written as italicized English or Greek letters—for example, t for time and θ for angle; (2) vectors are written as boldface letters—for example, F for force; and (3) the magnitude of a vector A is denoted as |A| or simply as A (italic).

There is no universal method for indicating vector quantities when writing by hand. The more common notations are −→A , A

, A, and A. Unless instructed otherwise, you are free to use the convention that you ﬁnd most comfortable. However, it is imperative that you take care to always distinguish between scalars and vectors when you write.

−→

The following summarizes several important properties of vectors.

Vectors as Directed Line Segments Any vector A can be represented geometrically as a directed line segment (an arrow), as shown in Fig. 1.2(a). The magnitude of A is denoted by A, and the direction of A is speciﬁed by the sense of the arrow and the angle θ that it makes with a ﬁxed reference line. When using graphical methods, the length of the arrow is drawn proportional to the magnitude of the vector. Observe that the representation shown in Fig. 1.2(a) is complete because both the magnitude and direction of the vector are indicated. In some instances, it is also convenient to use the representation shown in Fig. 1.2(b), where the vector character of A is given additional emphasis by using boldface. Both of these representations for vectors are used in this text.

###### A

A

θ θ

Fixed reference line

(a) (b)

###### Fig. 1.2

We see that a vector does not possess a unique line of action, because moving a vector to a parallel line of action changes neither its magnitude nor its direction. In some engineering applications, the deﬁnition of a vector is more restrictive to include a line of action or even a point of application—see Art. 2.2.

Equality of Vectors Two vectors A and B are said to be equal, written as A = B, if (1) their magnitudes are equal—that is, A = B, and (2) they have the same direction.

Scalar-Vector Multiplication The multiplication of a scalar m and a vector A, written as mA or as Am, is deﬁned as follows.

- 1. If m is positive, mA is the vector of magnitude mA that has the same direction as A.
- 2. If m is negative, mA is the vector of magnitude |m|A that is oppositely directed to A.
- 3. If m =0, mA (called the null or zero vector) is a vector of zero magnitude and arbitrary direction.

For m = − 1, we see that (−1)A is the vector that has the same magnitude as A but is oppositely directed to A. The vector (−1)A, usually written as −A, is called the negative of A.

Unit Vectors A unit vector is a dimensionless vector with magnitude 1. Therefore, if λ represents a unit vector (|λ| = 1) with the same direction as A, we can write

###### A= Aλ

This representation of a vector often is useful because it separates the magnitude A and the direction λ of the vector.

The Parallelogram Law for Addition and the Triangle Law The addition of two vectors A and B is deﬁned to be the vector C that results from the geometric construction shown in Fig. 1.3(a) . Observe that C is the diagonal of the parallelogram

formed by A and B. The operation depicted in Fig. 1.3(a), written as A + B = C, is called the parallelogram law for addition. The vectors A and B are referred to as components of C, and C is called the resultant of A and B. The process of replacing a resultant with its components is called resolution. For example, C in Fig. 1.3(a) is resolved into its components A and B.

B

###### A + B

=

C

An equivalent statement of the parallelogram law is the triangle law, which is shown in Fig. 1.3(b). Here the tail of B is placed at the tip of A, and C is the vector that completes the triangle, drawn from the tail of A to the tip of B. The result is identical if the tail of A is placed at the tip of B and C is drawn from the tail of B to the tip of A.

A

(a) Parallelogram law

###### B

Letting E, F, and G represent any three vectors, we have the following two important properties (each follows directly from the parallelogram law):

= A + B

C

- • Addition is commutative: E + F = F + E
- • Addition is associative: E + (F + G) = (E + F) + G

A

It is often convenient to ﬁnd the sum E + F + G (no parentheses are needed) by adding the vectors from tip to tail, as shown in Fig. 1.4. The sum of the three vectors is seen to be the vector drawn from the tail of the ﬁrst vector (E) to the tip of the last vector (G). This method, called the polygon rule for addition, can easily be extended to any number of vectors.

(b) Triangle law

Fig. 1.3

F E

E+F

G

E+F+G

###### Fig. 1.4

The subtraction of two vectors A and B, written as A − B, is deﬁned as A − B = A + (−B), as shown in Fig. 1.5.

A

- A

–

- B

B

–B

###### Fig. 1.5

Because of the geometric nature of the parallelogram law and the triangle law, vector addition can be accomplished graphically. A second technique is to determine the relationships between the various magnitudes and angles analytically by applying the laws of sines and cosines to a sketch of the parallelogram (or the triangle)—see Table 1.1. Both the graphical and the analytical methods are illustrated in Sample Problem 1.4.

|Law of sines<br><br>|a<br><br>sinα =<br><br>b<br><br>sinβ =<br><br>c sinγ<br><br>|
|---|---|
| |a2 b2 c2 2bc cos|

γ

b

a

= + − α Law of cosines b2 = c2 + a2 − 2ca cosβ c2 = a2 + b2 − 2ab cosγ

α

β

c

###### Table 1.1

Some words of caution: It is unfortunate that the symbols +, −, and = are commonly used in both scalar algebra and vector algebra, because they have completely different meanings in the two systems. For example, note the different meanings for + and = in the following two equations: A + B = C and 1 + 2 = 3. In computer programming, this is known as operator overloading, where the rules of the operation depend on the operands involved in the process. Unless you are extremely careful, this double meaning for symbols can easily lead to invalid expressions—for example, A + 5 (a vector cannot be added to a scalar!) and A = 1 (a vector cannot equal a scalar!).

|Sample Problem 1.4<br><br>Figure (a) shows two position vectors of magnitudes A =60 ft and B =100 ft. (A position vector is a vector drawn between two points in space.) Determine the resultant R = A + B using the following methods: (1) analytically, using the triangle law; and (2) graphically, using the triangle law.<br><br>70°<br><br>100 ft<br><br>B<br><br>30°<br><br>A 60ft<br><br>(a)<br><br>Solution<br><br>Part 1<br><br>The ﬁrst step in the analytical solution is to draw a sketch (approximately to scale) of the triangle law. The magnitude and direction of the resultant are then found by applying the laws of sines and cosines to the triangle.<br><br>In this problem, the triangle law for the vector addition of A and B is shown in Fig. (b). The magnitude R of the resultant and the angle α are the unknowns to<br><br>30°<br><br>α<br><br>70°<br><br>(b)<br><br>140°<br><br>R<br><br>B<br><br>= 100 ft<br><br>A<br><br>=60ft<br><br>be determined. Applying the law of cosines, we obtain<br><br>R2 =602 + 1002 − 2(60)(100)cos 140◦<br><br>which yields R =151.0 ft. The angle α can now be found from the law of sines:<br><br>100 sinα =<br><br>R sin140◦<br><br>Substituting R =151.0 ft and solving for α, we get α = 25.2◦. Referring to Fig. (b), we see that the angle that R makes with the horizontal is 30◦ +α =30◦ + 25.2◦ =55.2◦. Therefore, the resultant of A and B is<br><br>R = 151.0 ft<br><br>55.2°<br><br>Answer|
|---|

###### 14

|Part 2<br><br>In the graphical solution, Fig. (b) is drawn to scale with the aid of a ruler and a protractor. We ﬁrst draw the vector A at 30◦ to the horizontal and then append vector B at 70◦ to the horizontal. The resultant R is then obtained by drawing a line from the tail of A to the head of B. The magnitude of R and the angle it makes with the horizontal can now be measured directly from the ﬁgure.<br><br>Of course, the results would not be as accurate as those obtained in the analytical solution. If care is taken in making the drawing, two-digit accuracy is the best we can hope for. In this problem we should get R ≈ 150 ft, inclined at 55◦ to the horizontal.<br><br>Sample Problem 1.5<br><br>The vertical force P of magnitude 100kN is applied to the frame shown in Fig. (a). Resolve P into components that are parallel to the members AB and AC of the truss.<br><br>A<br><br>P<br><br>70°<br><br>35°<br><br>B<br>C<br><br><br>(a)<br><br>PAB<br><br>PAC 110°<br><br>70°<br><br>35°<br><br>35°<br><br>(b)<br><br>=100kNP<br><br>Solution<br><br>The force triangle in Fig. (b) represents the vector addition P = PAC + PAB. The angles in the ﬁgure were derived from the inclinations of AC and AB with the vertical: PAC is inclined at 35◦ (parallel to AC), and PAB is inclined at 70◦ (parallel to AB). Applying the law of sines to the triangle, we obtain<br><br>100 sin35◦ =<br><br>PAB<br><br>sin35◦ =<br><br>PAC sin110◦<br><br>which yields for the magnitudes of the components<br><br>PAB =100.0kN PBC =163.8kN Answer|
|---|

###### 15

![image 5](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile5.png>)

###### Problems

v1

Solve the problems in this set analytically, unless a graphical solution is speciﬁed by your instructor.

30°

1.22 The magnitudes of the two velocity vectors are v1 = 3m/s and v2 = 2m/s.

Determine their resultant v = v1 + v2.

60°

v2

- 1.23 Determine the magnitudes of vectors v1 and v2 so that their resultant is a horizontal vector of magnitude 4m/s directed to the right.
- 1.24 The total aerodynamic force F acting on the airplane has a magnitude of

Fig. P1.22, P1.23

6250lb. Resolve this force into vertical and horizontal components (called the lift and the drag, respectively).

6° F

1.25 Resolve the 200-lb force into components along (a) the x- and y-axes and

(b) the x - and y-axes.

Fig. P1.24

- 1.26 The velocity vector of the boat has two components: v1 is the velocity of the water, and v2 is the velocity of the boat relative to the water. If v1 = 3mi/h and v2 = 5mi/h, determine the velocity vector of the boat.

v2

v1

40°

Fig. P1.26

- 1.27 The two tugboats apply the forces P and Q to the barge, where P =76 kN and Q =52 kN. Determine the resultant of P and Q.

y

200 lb

30°

x

20°

x'

Fig. P1.25

16 m

|P| |
|---|---|
| |Q|

32 m

12 m

24 m

###### Fig. P1.27

###### 1.22–1.39 Problems 17

- 1.28 The 500-N weight is supported by two cables, the cable forces being F1 F F1 2

35° 50°

500 N

y

Fig. P1.28

and F2. Knowing that the resultant of F1 and F2 is a force of magnitude 500N acting in the y-direction, determine F1 and F2.

- 1.29 Determine the resultant of the position vectors A and B.

| | |
|---|---|
| | |

3 m 1.0 m

3 m B

A

2 m 3500 ft

2000ft

O C

B

A

65°

Fig. P1.29 Fig. P1.30

- 1.30 Resolve the position vector A of the car (measured from ﬁxed point O) into components parallel to OB and OC.
- 1.31 Resolve the 360-lb force into components along the cables AB and AC. Use

A

B C

α β

360 lb

Fig. P1.31, P1.32

α =55◦ and β =30◦.

- 1.32 The supporting cables AB and AC are oriented so that the components of the 360-lb force along AB and AC are 185lb and 200lb, respectively. Determine the angles α and β.
- 1.33 The two forces shown act on the structural member AB. Determine the magnitude of P such that the resultant of these forces is directed along AB.

70°

60° 40°

B

A

P

5 kN

60°

P

500 lb

| | | |
|---|---|---|
| | | |

T

W

θ

Fig. P1.33 Fig. P1.34 Fig. P1.35

- 1.34 The resultant of the two forces has a magnitude of 650lb. Determine the direction of the resultant and the magnitude of P.
- 1.35 The forces acting on the bob of the pendulum are its weight W (W = 2 lb) and the tension T in the cord. When the pendulum reaches the limit of its swing at θ =30◦, it can be shown that the resultant of W and T is perpendicular to the cord. Determine the magnitude of T in this position.
- 1.36 A surveyor sights a target at C from points A and B, recording the angles

C

North

###### a

b

42.5° 63.8°

East

200 m

A B

shown. Determine the magnitudes of the position vectors a and b. Fig. P1.36

A 1.37 Determine the following resultants of the position vectors given in the

ﬁgure, and show the results in a sketch of the “box”: (a) A + B; and (b) B + C.

C

4 m

∗1.38 To move the oil drum, the resultant of the three forces shown must have a magnitude of 500N. Determine the magnitude and direction of the smallest force F that would cause the drum to move.

m

B

3

5 m

250 N

Fig. P1.37

###### F

25°

OIL

###### R

α

300 N

50 lb

β

30 lb

Fig. P1.38 1.39 The resultant of the 50-lb and 30-lb forces is R. If R = 65lb, determine

the angles α and β.

Fig. P1.39

###### 1.4 Representation of Vectors Using Rectangular Components

The fundamental properties of vectors discussed in the preceding article are independent of coordinate systems. However, in engineering applications, it is customary to describe vectors using their rectangular components and then to perform vector operations, such as addition, in terms of these components.

###### a. Rectangular components and direction cosines

The reference frame we use throughout this book is shown in Fig. 1.6(a). It is a right-handed, rectangular Cartesian coordinate system. To test for right-handedness, curl the ﬁngers of your right hand and extend your thumb, as shown in the ﬁgure. The coordinate axes now should line up with your hand as

z

z

Azk

###### λ

k

###### A

θz

j

y

θx θy Ayj

y

i

Axi

x

x

(a)

(b)

###### Fig. 1.6

follows: the palm is parallel to the x-direction, the ﬁngers point in the y-direction, and the thumb lies in the z-direction. Figure 1.6(a) also shows the base vectors i, j, and k of the coordinate system. They are dimensionless vectors of unit magnitude directed in the positive coordinate directions.

If a vector A is resolved into its rectangular components, as illustrated in Fig. 1.6(b), it can be written as

A = Axi + Ayj + Azk (1.5)

where Axi, Ayj, and Azk are the vector components of A. The scalar components of A are

Ax = A cosθx Ay = A cosθy Az = A cosθz (1.6)

where θx, θy, and θz are the angles between A and the positive coordinate axes. The scalar components can be positive or negative, depending upon whether the corresponding vector component points in the positive or negative coordinate direction. The magnitude of A is related to its scalar components by

###### A = A2x + A2y + A2z (1.7)

The direction of A customarily is speciﬁed by its direction cosines deﬁned as

###### λx = cosθx λy = cosθy λz = cosθz (1.8)

The scalar components of A in Eq. (1.6) now become Ax = Aλx, Ay = Aλy, and Az = Aλz, so Eq. (1.5) takes the form

###### A = A(λxi + λyj + λzk) = Aλ (1.9)

where

###### λ = λxi + λyj + λzk (1.10)

is a unit vector in the direction of A, as shown in Fig. 1.6(b). Because the magnitude of λ is one, its components satisfy the identity

###### λ2x + λ2y + λ2z = 1 (1.11)

###### b. Vector addition using rectangular components

Consider the two vectors A= Axi+ Ayj+ Azk and B= Bxi+ Byj+ Bzk. Letting C be the sum of A and B, we have

C=A + B=(Axi + Ayj + Azk) + (Bxi + Byj + Bzk) which can be written as

C = Cxi + Cyj + Czk

= (Ax + Bx)i + (Ay + By)j + (Az + Bz)k (1.12) Equating like components, we ﬁnd that the rectangular components of C are

###### Cx = Ax + Bx Cy = Ay + By Cz = Az + Bz (1.13)

Equations (1.13) show that each component of the sum equals the sum of the components. This result is depicted in Fig. 1.7, where, for simplicity’s sake, the xy-plane has been chosen as a plane that contains the vectors A and B. Equations (1.12) and (1.13) can, of course, be extended to include the sum of any number of vectors.

y

B

=+CAByyy

+B

By

A

=

C

Ay

A

x

O

Ax

Bx

Cx = Ax+ Bx

###### Fig. 1.7

###### c. Relative position vectors

The vector drawn from the origin O of a coordinate system to point B, denoted by −OB→, is called the position vector of B. The vector −AB→, drawn from point A to point B, is called the position vector of B relative to A. (Note that the position vector of B relative to A is the negative of the position vector of A relative to B; that is, −AB→= −

###### −BA→.)

Figure 1.8 shows the relative position vector −AB→: the vector drawn from A (xA, yA, zA) to B (xB, yB, zB). The rectangular representation of this vector is

−AB→=(xB − xA)i + (yB − yA)j + (zB − zA)k (1.14)

###### λ

B d

–zzBA

z

AB

y

A

–x

A

x

x

B

yB– yA

###### Fig. 1.8

The magnitude of −AB→ (the distance d in Fig. 1.8) is

−AB→|=d = (xB − xA)2 + (yB − yA)2 + (zB − zA)2 (1.15)

|

The unit vector λ in the direction of −AB→ can be found by dividing the vector −AB→ by its magnitude:

−AB→ |

(xB − xA)i + (yB − yA)j + (zB − zA)k d

(1.16)

=

λ=

−AB→|

Therefore, the components of λ are

xB − xA d

yB − yA d

zB − zA d

(1.17)

λx =

λy =

λz =

###### d. How to write a vector in rectangular form

In statics, we frequently encounter the following problem: Given the magnitude of a vector and two points on its line of action, determine the rectangular representation of the vector. Figure 1.9 shows a vector F that acts along the line AB.

###### λ

Suppose that the magnitude of F and the coordinates of A and B are known, and we want to write the vector F in the rectangular form F = Fxi + Fyj + Fzk. The recommended procedure is

B

###### λ

z

F

=

F

- 1. Write the relative position vector −AB→. The rectangular components of −AB→ can be obtained by inspection of a sketch similar to Fig. 1.9 or by substituting the coordinates of points A and B into Eq. (1.14).
- 2. Evaluate the unit vector λ =

−AB→/|

−AB→|.

- 3. Write F in the rectangular form

y

A

x

Fig. 1.9

###### F = Fλ = F λxi + λyj + λzk (1.18)

|Sample Problem 1.6<br><br>The cable attached to the eyebolt in Fig. (a) is pulled with the force F of magnitude 500lb. Determine the rectangular representation of this force.<br><br>(a)<br><br>6 ft<br><br>3 ft<br><br>4ft F<br><br>z<br><br>O B<br><br>A<br><br>x<br><br>y<br><br>Solution<br><br>Because the coordinates of points A and B on the line of action of F are known, the following is a convenient method for obtaining the rectangular representation of F.<br><br>1. Write −AB→, the vector from A to B, in rectangular form.<br><br>The vector −AB→ and its rectangular components are shown in Fig. (b). Two<br><br>x<br><br>y<br><br>z<br><br>4ft<br><br>6 ft<br><br>B<br><br>3 ft<br><br>A<br><br>AB<br><br>(b)<br><br>O<br><br>common errors made by students at this point are choosing the wrong signs and mixing up the scalar components. You can avoid both of these difﬁculties by taking the time to show the vector on a carefully drawn sketch of the appropriate parallelepiped. From Fig. (b) we see that<br><br>−AB→= − 4i + 6j − 3k ft<br><br>2. Evaluate λ, the unit vector from A toward B:<br><br>λ=<br><br>−AB→ |<br><br>−AB→|<br><br>=<br><br>−4i + 6j − 3k (−4)2 + 62 + (−3)2<br><br>= −0.5122i + 0.7682j − 0.3841k<br><br>3. Write F= Fλ:<br><br><br>F = 500(−0.5122i + 0.7682j − 0.3841k)<br><br>= −256i + 384j − 192k lb Answer<br><br>(c) The rectangular components of F are shown in Fig. (c).<br><br><br>x<br><br>y<br><br>z<br><br>256lb<br><br>192 lb<br><br>A<br><br>384 lb O|
|---|

|Sample Problem 1.7<br><br>Referring to Fig. (a), determine (1) the rectangular representation of the position<br><br>30° 12m<br><br>40°<br><br>x<br><br>y<br><br>A<br><br>z<br><br>O<br><br>(a)<br><br>vector A; and (2) the angles between A and each of the positive coordinate axes.<br><br>Solution<br><br>Part 1 We ﬁrst resolve A into two components as shown in Fig. (b): Az along the z-axis<br><br>x<br><br>y<br><br>30°<br><br>40°<br><br>z<br><br>Axy = A sin30° (b)<br><br>A<br><br>°=cos30AAz<br><br>y<br><br>z<br><br>(c)<br><br>Ax = Axy cos40°<br><br>Ay = Axy sin 40°<br><br>Axy<br><br>°=cos30AAz<br><br>x<br><br>40°<br><br>and Axy in the xy-plane. (Once again we see that a carefully drawn sketch is an essential aid in performing vector resolution.) Because A, Az, and Axy lie in the same plane (a diagonal plane of the parallelepiped), we obtain by trigonometry<br><br>Az = A cos30◦ =12cos30◦ =10.392m Axy = A sin30◦ =12sin30◦ =6m<br><br>The next step, illustrated in Fig. (c), is to resolve Axy into the components along the coordinate axes:<br><br>Ax = Axy cos40◦ =6cos40◦ =4.596m<br>Ay = Axy sin40◦ =6sin40◦ =3.857m<br><br><br>Therefore, the rectangular representation of A is<br><br>A= Axi + Ayj + Azk=4.60i + 3.86j + 10.39km Answer<br><br>Part 2 The angles between A and the coordinate axes can be computed from Eqs. (1.6):<br><br><br>θx = cos−1<br><br>Ax A = cos−1<br><br>4.596 12 =67.5◦<br><br>θy = cos−1<br><br>Ay A = cos−1<br><br>3.857 12 =71.3◦ Answer<br><br>θz = cos−1<br><br><br>Az A = cos−1<br><br>10.392 12 =30.0◦<br><br>These angles are shown in Fig. (d). Note that it was not necessary to compute θz, because it was already given in Fig (a).<br><br>θz = 30°<br><br>x<br><br>y<br><br>A<br><br>z<br><br>(d)<br><br>θy = 71.3° θx = 67.5°<br><br>|
|---|

###### 23

|Sample Problem 1.8<br><br>The pulley shown in Fig. (a) is subjected to the belt forces P and Q. Using rectangular components, determine the magnitude and direction of the resultant force.<br><br>(a)<br><br>30°<br><br>P = 120 lb<br><br>Q = 100 lb<br><br>70°<br><br>y<br><br>x<br><br>Solution<br><br>Referring to Fig. (b), the rectangular representations of P and Q are<br><br>P = 120cos30◦i + 120sin30◦j=103.9i + 60.0j lb<br>Q = −100cos70◦i − 100sin70◦j= − 34.2i − 94.0j lb<br><br><br>y<br><br>x (b)<br><br>70°<br><br>30°<br><br>Q = 100 lb<br><br>P<br><br>=120lb<br><br>The resultant of P and Q is found by adding their components:<br><br>R=P + Q = (103.9 − 34.2)i + (60.0 − 94.0)j<br><br>= 69.7i − 34.0jlb<br><br>Calculating the magnitude and direction of R, we obtain<br><br>34.0 lb<br><br>69.7 lb<br><br>R<br><br>θ Answer<br><br>R = 34.02 + 69.72 =77.6lb θ = tan−1<br><br>34.0 69.7 =26.0◦<br><br>|
|---|

1.40–1.56 Problems 25

![image 6](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile6.png>)

###### Problems

- 1.40 Obtain the rectangular representation of the force P, given that its magnitude is 30lb.

50°

30°

y

x

z

P

Fig. P1.40

- 1.41 The length of the position vector r is 240mm. Determine the rectangular

50°

y

x

z

A

O

40°

r

Fig. P1.41

components of (a) r; and (b) the unit vector directed from O toward A.

- 1.42 (a) Compute the angle θz between the force vector F and the z-axis.

50°

60°

F

z

x y

θz

Fig. P1.42

(b) Determine the rectangular representation of F given that F = 240N.

- 1.43 The coordinates of points A and B are (−3,0,2) ft and (4,1,7) ft, respectively. Determine (a) the distance between A and B; and (b) the rectangular representation of the unit vector directed from A towards B.
- 1.44 The slider travels along the guide rod AB with the velocity v = 6m/s. Determine the rectangular representations of (a) the unit vector directed from A toward B; and (b) the velocity vector v.

z

x

8m

10m

16m

B

12 m

y

A

v

Fig. P1.44

- 1.45 Find the rectangular representation of the force F, given its magnitude

z

5m

A

3 m

###### F

O

x

m

4

y

###### Fig. P1.45 240N.

- 1.46 The magnitude of the force F is 120lb. Find its rectangular representation.

|F| | |
|---|---|---|
| | | |
| | | |

x

A

y

15 ft B

z

18ft

25ft

80 ft

210ft

160ft

z

x

A

v

B y

Fig. P1.46 Fig. P1.47

- 1.47 A riﬂe at A is ﬁred at a target at B. If the speed of the bullet is 1800ft/s, determine the rectangular form of the velocity vector v.
- 1.48 Find the angles between the force F = 1200i + 800j − 1500k N and the x-, y-, and z-axes. Show your results on a sketch of the coordinate system.
- 1.49 Find the resultant of the two forces, each of which is of magnitude P.

x

a

a

a B

y P

P

O

z

A

x

y

z

120 lb

100 lb

3ft

4ft

5 ft

Fig. P1.49 Fig. P1.50

- 1.50 Determine the resultant of the two forces shown.

z

F3

65°

y

35°

F2

F1

x 1.51 The magnitudes of the three forces are F1 = 1.6kN, F2 = 1.2kN, and

F3 = 1.0kN. Compute their resultant in the form (a) R = Rxi + Ryj + Rzk; and (b) R = Rλ.

Fig. P1.51

- 1.52 Given that P =120 lb and Q =130 lb, ﬁnd the rectangular representation

4

3

5

12

P

Q

y

x

Fig. P1.52, P1.53

of P + Q.

- 1.53 Knowing that P = 120 lb and that the resultant of P and Q lies in the positive x-direction, determine Q and the magnitude of the resultant.
- 1.54 If R is the resultant of the forces P and Q, ﬁnd P and Q.

y

x

Q

P

R = 360 lb

30°

30°

25°

Q

R = 2 kN

P = 3 kN

x

y

θ

55°

Fig. P1.54 Fig. P1.55

- 1.55 The force R is the resultant of P and Q. Determine Q and the angle θ.
- 1.56 The vertical post is secured by three cables. The cables are pre-tensioned

z

A

F P Q

12 ft

D

8ft

6ft 6ft

C

x

8ft

y B

6ft

so that the resultant of the cable forces F, Q, and P is directed along the z-axis. If F = 120lb, ﬁnd P and Q.

Fig. P1.56

###### 1.5 Vector Multiplication∗

###### a. Dot (scalar) product

Figure 1.10 shows two vectors A and B, with θ being the angle between their B

positive directions. The dot product of A and B is deﬁned as

A

θ

A·B= AB cosθ (0 ≤ θ ≤ 180◦) (1.19)

Because the dot product is a scalar, it is also called the scalar product. Note that the dot product is positive if θ < 90◦, negative if θ > 90◦, and zero if θ = 90◦.

Fig. 1.10

The following two properties of the dot product follow from its deﬁnition in Eq. (1.19).

- • The dot product is commutative: A·B=B·A
- • The dot product is distributive: A·(B + C)=A·B + A·C

*Note that division by a vector, such as 1/A or B/A, is not deﬁned.

From the deﬁnition of the dot product, we also note that the base vectors of a rectangular coordinate system satisfy the following identities:

- i·i = j·j=k·k=1 (1.20)
- i·j = j·k=k·i=0

When A and B are expressed in rectangular form, their dot product becomes

A·B=(Axi + Ayj + Azk)·(Bxi + Byj + Bzk)

which, using the distributive property of the dot product and Eqs. (1.20), reduces to

A·B= Ax Bx + AyBy + AzBz (1.21)

Equation (1.21) is a powerful and relatively simple method for computing the dot product of two vectors that are given in rectangular form.

The following are two of the more important applications of the dot product.

Finding the Angle Between Two Vectors The angle θ between the two vectors A and B in Fig. 1.11 can be found from the deﬁnition of the dot product in

λB

Eq. (1.19), which can be rewritten as

B

A A ·

B B

###### A·B

AB =

cosθ =

λA

A

θ

Letting λA =A/A and λB =B/B be the unit vectors that have the same directions as A and B, as shown in Fig. 1.11, the last equation becomes

Fig. 1.11

cosθ =λA ·λB (1.22)

If the unit vectors are written in rectangular form, this dot product is easily evaluated using Eq. (1.21).

Determining the Orthogonal Component of a Vector in a Given Direction If B we project B onto A as in Fig. 1.12, the projected length B cosθ is called the

orthogonal component of B in the direction of A. Because θ is the angle between A and B, the deﬁnition of the dot product, A·B= AB cosθ, yields

λA

A

θ

A A

###### A·B

cosθ

A =B·

B cosθ =

B

Because A/A =λA (the unit vector in the direction of A), as shown in Fig. 1.12, the last equation becomes

Fig. 1.12

B cosθ =B·λA (1.23) Therefore,

The orthogonal component of B in the direction of A equals B · λA. (1.24)

###### b. Cross (vector) product

The cross product C of two vectors A and B, denoted by

###### C=A × B

has the following characteristics (see Fig. 1.13):

- • The magnitude of C is

C = ABsinθ (1.25)

where θ (0 ≤ θ ≤ 180◦) is the angle between the positive directions of A and B. (Note that C is always a positive number.)

- • C is perpendicular to both A and B.
- • The sense of C is determined by the right-hand rule, which states that when the ﬁngers of your right hand are curled in the direction of the angle θ (directed from A toward B), your thumb points in the direction of C.*

C = A × B

B

θ

A

###### Fig. 1.13

The cross product of two vectors is also called their vector product. It can be shown that the cross product is distributive; that is,

###### A × (B + C)=(A × B) + (A × C)

However, the cross product is neither associative nor commutative. In other words,

###### A × (B × C)  = (A × B) × C A × B  = B × A

In fact, it can be deduced from the right-hand rule that A × B= − B × A.

From the deﬁnition of the cross product C = A × B, we see that (1) if A and B are perpendicular (θ = 90◦), then C = AB; and (2) if A and B are parallel (θ = 0◦ or 180◦), then C = 0.

*An alternative statement of the right-hand rule is this: The direction of C is the direction in which a right-hand screw would advance when turned in the direction of θ (directed from A toward B).

From the properties of the cross product, we deduce that the base vectors of a rectangular coordinate system satisfy the following identities:

i × i = 0 j × j=0 k × k=0

(1.26) i × j = k j × k=i k × i=j

where the equations in the bottom row are valid in a right-handed coordinate system. If the coordinate axes are labeled such that i × j= − k, j × k= − i, and k × i= − j, the system is said to be left-handed. Examples of both right- and left-handed coordinate systems are shown in Fig. 1.14.*

z

z

k

k

###### j

###### i

x j

y i

O

O

y

x

Right-handed coordinate system (i×j = k, etc.)

Left-handed coordinate system (i×j = –k, etc.)

###### Fig. 1.14

When A and B are expressed in rectangular form, their cross product becomes

###### A × B=(Axi + Ayj + Azk) × (Bxi + Byj + Bzk)

Using the distributive property of the cross product and Eqs. (1.26), this equation becomes

A × B = (AyBz − AzBy)i − (Ax Bz − AzBx)j

(1.27)

+ (Ax By − AyBx)k

The identical expression is obtained when the rules for expanding a 3 × 3 determinant are applied to the following array of nine terms (because the terms are not all scalars, the array is not a true determinant):

i j k Ax Ay Az Bx By Bz

A × B=

(1.28)

*In this text, we assume that all rectangular coordinate systems are right-handed.

You may use any method for determinant expansion, but you will ﬁnd that the following technique, called expansion by minors using the ﬁrst row, is very convenient.

a b c d e f g h i

d e g h

d f g i + c

e f h i − b

= a

= a(ei − f h) − b(di − fg) + c(dh − eg)

Expanding Eq. (1.28) by this method, we ﬁnd that the 2 × 2 determinants equal the i, j, and k components of the cross product.

###### c. Scalar triple product

Of the vector products that involve three or more vectors, the one that is most useful in statics is the scalar triple product. The scalar triple product arises when the cross product of two vectors is dotted with a third vector—for example, A × B·C. When writing this product, it is not necessary to show the parentheses, because A × B·C can be interpreted only in one way—the cross product must be done ﬁrst; otherwise the expression is meaningless.

Assuming that A, B, and C are expressed in rectangular form and recalling Eq. (1.27), the scalar triple product becomes

A × B·C = (AyBz − AzBy) i − (Ax Bz − AzBx)j

+ (Ax By − AyBx)k ·(Cxi + Cyj + Czk)

Using Eq. (1.21) and the properties of the dot products of the rectangular base vectors, this expression simpliﬁes to

A × B·C=(AyBz − AzBy)Cx − (Ax Bz − AzBx)Cy

(1.29)

+ (Ax By − AyBx)Cz

Therefore, the scalar triple product can be written in the following determinant form, which is easy to remember:

Ax Ay Az Bx By Bz Cx Cy Cz

A × B·C=

(1.30)

The following identities relating to the scalar triple product are useful:

###### A × B·C=A·B × C=B·C × A=C·A × B (1.31)

Observe that the value of the scalar triple product is not altered if the locations of the dot and cross are interchanged or if the positions of A, B, and C are changedprovided that the cyclic order A–B–C is maintained.

|Sample Problem 1.9<br><br>Given the vectors<br><br>A = 8i + 4j − 2k lb<br>B = 2j + 6k ft<br>C = 3i − 2j + 4k ft<br><br><br>calculate the following: (1) A·B; (2) the orthogonal component of B in the direction of C; (3) the angle between A and C; (4) A × B; (5) a unit vector λ that is perpendicular to both A and B; and (6) A × B·C.<br><br>Solution<br><br>Part 1 From Eq. (1.21), the dot product of A and B is<br><br>A·B= Ax Bx + AyBy + AzBz = 8(0) + 4(2) + (−2)(6)<br><br>= −4lb·ft Answer<br><br>The negative sign indicates that the angle between A and B is greater than 90◦.<br><br>Part 2 Letting θ be the angle between B and C, we obtain from Eq. (1.23)<br><br>B cosθ =B·λC = B·<br><br>C C =(2j + 6k)·<br><br>3i − 2j + 4k 32 + (−2)2 + 42<br><br>=<br><br>(0)(3) + (2)(−2) + (6)(4) √29 =3.71 ft Answer<br><br>Part 3 Letting α be the angle between A and C, we ﬁnd from Eq. (1.22)<br><br><br>cosα =λA ·λC =<br><br>A A ·<br><br>C C<br><br>=<br><br>8i + 4j − 2k 82 + 42 + (−2)2<br><br>·<br><br>3i − 2j + 4k 32 + (−2)2 + 42<br><br>=<br><br>(8)(3) + (4)(−2) + (−2)(4) √84√29 =0.16209<br><br>|
|---|

###### 32

|which yields<br><br>α =80.7◦ Answer<br><br>Part 4 Referring to Eq. (1.28), the cross product of A and B is<br><br>A × B =<br><br>i j k Ax Ay Az Bx By Bz<br><br>=<br><br>i j k 8 4 −2 0 2 6<br><br>= i<br><br>4 −2 2 6 − j<br><br>8 −2 0 6 + k<br><br>8 4 0 2<br><br>= 28i − 48j + 16k lb · ft Answer<br><br>Part 5<br><br>The cross product A×B is perpendicular to both A and B. Therefore, a unit vector in that direction is obtained by dividing A×B, which was evaluated above, by its magnitude<br><br>A × B |A × B|<br><br>=<br><br>28i − 48j + 16k 282 + (−48)2 + 162<br><br>= 0.484i − 0.830j + 0.277k<br><br>Because the negative of this vector is also a unit vector that is perpendicular to both A and B, we obtain<br><br>λ= ± (0.484i − 0.830j + 0.277k) Answer<br><br>Part 6 The scalar triple product A × B·C is evaluated using Eq. (1.30).<br><br><br>A × B·C =<br><br>Ax Ay Az Bx By Bz Cx Cy Cz<br><br>=<br><br>8 4 −2 0 2 6 3 −2 4<br><br>= 8<br><br>2 6<br><br>−2 4 − 4<br><br>0 6 3 4 + (−2)<br><br>0 2 3 −2<br><br>= 160 + 72 + 12=244 lb · ft2 Answer|
|---|

###### 33

![image 7](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile7.png>)

###### Problems

- 1.57 Compute the dot product A·B for each of the following cases. Identify the units of each product.

- (a) A=6j + 9k ft B=7i − 3j + 2k ft
- (b) A=2i − 3j m B=6i − 13k N
- (c) A=5i − 6j − k m B= − 5i + 8j + 6k m

- 1.58 Compute the cross product C=A × B for each of the cases given in Prob. 1.57. Identify the units of each product.
- 1.59 Given

r = 5i + 4j + 3k m (position vector) F = 30i − 20j − 10k N (force vector) λ = 0.6j + 0.8k (dimensionless unit vector)

compute (a) r × F·λ; and (b) λ × r·F.

- 1.60 Compute A × B and C × B for the position vectors shown.
- 1.61 Use the dot product to ﬁnd the angle between the position vectors A and

z

1.5 m

A C B

y

B. Check your results by trigonometry. 1.62 Use the dot product to ﬁnd the angle between the position vectors A and B.

2m

x

1.2m

Fig. P1.60, P1.61

- 1.63 Let A and B be two nonparallel vectors that lie in a common plane S. If C=A×(A×B), which of the following statements are true: (i) C=0; (ii) C lies in plane S; and (iii) C is perpendicular to plane S?
- 1.64 Determine which of the following position vectors B is perpendicular to

- A=3i − 5j + 2k m:

- (a) B=5i + 3j − 2k m
- (b) B=2i + 3j + 4k m
- (c) B=i + j + k m
- (d) B=3i + j − 2k m

1.65 Find a unit vector that is perpendicular to both A=5i − 2j + 2k ft and

- B= − 3i + 2j + 4k ft.

- 1.66 The three points A(0, −2, 2), B (−1, 4, 1), and C (3, 0, 0) deﬁne a plane. The coordinates are in inches. Find a unit vector that is perpendicular to this plane.
- 1.67 Determine the orthogonal component of C = r × F in the direction of the unit vector λ where r = 0.2i + 0.3j − 0.2k m, F = 300i − 100j + 500k N, and λ = (i + j + k)/√3.

z

120mm

###### B

50° A

y

180mm

200 mm

x

Fig. P1.62

###### 1.57–1.76 Problems 35

y

- 1.68 Compute the orthogonal component of F=6i + 20j − 12k lb in the direction of the vector A=2i − 3j + 5k ft.
- 1.69 Using the dot product, ﬁnd the components of the velocity vector v=20i+

'

x

###### v

'

y

12j km/h in the directions of the x - and y -axes.

30° 60°

x

O

∗1.70 Resolve A = 3i + 5j − 4k in. into two vector components—one parallel to and the other perpendicular to B = 6i + 2k in. Express each of your answers as a magnitude multiplied by a unit vector.

Fig. P1.69

- 1.71 Show that the shortest distance between the point P and the line AB is

A

B

P

d

λAB

Fig. P1.71

d = |

−AP→ × λAB| where λAB is a unit vector in the direction of the line.

- 1.72 Determine the value of the scalar a if the following three vectors are to lie in the same plane: A=2i−j+2k m, B=6i+3j+ak m, and C=16i+46j+7k m. ∗1.73 Resolve the force F=20i + 30j + 50k lb into two components—one

perpendicular to plane ABC and the other lying in plane ABC.

z

- 1.74 It can be shown that a plane area may be represented by a vector A= Aλ, where A is the area and λ represents a unit vector normal to the plane of the area. Show that the area vector of the parallelogram formed by the vectors a and b shown in the ﬁgure is A=a × b.

z

b

a

y

x

O

A = Aλ

Area = A

λ

Fig. P1.74

- 1.75 The coordinates of the corners of a triangle ABC are A(3, –1, 0), B (–2, 2, 3), and C (0, 0, 4). The units are inches. Calculate the area of triangle ABC. (Hint: See Prob. 1.74.)
- 1.76 Show that |a × b·c| equals the volume of a parallelepiped that has a, b, and c as its edges. (Hint: See Prob. 1.74.)

B

F

5in.

2in.

O

6in.

A

x

C

y

Fig. P1.73

![image 8](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile8.png>)

###### Review of Equations

###### Universal law of gravitation

- F = GmAmB/R2
- G = 6.67 × 10−11m3/(kg·s2)

= 3.44 × 10−8 ft4/(lb·s4)

###### Rectangular components of vectors

A = Axi + Ayj + Azk A + B = (Ax + Bx)i + (Ay + By)j + (Az + Bz)k

−AB→ = (xB − xA)i + (yB − yA)j + (zB − zA)k

###### Vector multiplication

A·B = Ax Bx + AyBy + AzBz = AB cosθ

i j k Ax Ay Az Bx By Bz

|A × B| = AB sinθ

A × B =

Ax Ay Az Bx By Bz Cx Cy Cz

A × B·C =

θ = angle between A and B

# 2

### Basic Operations with Force Systems

![image 9](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile9.png>)

A fundamental concept of statics is the equivalence of forces. For example, a single force can produce the same effect on the ﬂoating drilling platform as the two forces applied by the tugboats. Equivalence of forces is one of the topics discussed in this chapter. Don Farrall/Photodisc/Getty Images

###### 2.1 Introduction

The usefulness of vector algebra in real-world problems stems from the fact that several commonly encountered physical quantities possess the properties of vectors. One such quantity is force, which was shown to obey the parallelogram law of addition by Stevinus (1548–1620).

In this chapter we begin to study the effects of forces on particles and rigid bodies. In particular, we learn how to use vector algebra to reduce a system of forces to a simpler, equivalent system. If the forces are concurrent (all forces intersect at the same point), we show that the equivalent system is a single force. The reduction of a nonconcurrent force system requires two additional vector concepts: the moment of a force and the couple. Both of these concepts are introduced in this chapter.

###### 2.2 Equivalence of Vectors

We recall that vectors are quantities that have magnitude and direction, and combine according to the parallelogram law for addition. Two vectors that have the same magnitude and direction are said to be equal.

###### 37

In mechanics, the term equivalence implies interchangeability; two vectors are considered to be equivalent if they can be interchanged without changing the outcome of the problem. Equality does not always result in equivalence. For example, a force applied to a certain point in a body does not necessarily produce the same effect on the body as an equal force acting at a different point.

From the viewpoint of equivalence, vectors representing physical quantities are classiﬁed into the following three types:

- • Fixed vectors: Equivalent vectors have the same magnitude, direction, and point of application.
- • Sliding vectors: Equivalent vectors have the same magnitude, direction, and line of action.
- • Free vectors: Equivalent vectors have the same magnitude and direction.

It is possible for a physical quantity to be one type of vector—say, ﬁxed—in one application and another type of vector, such as sliding, in another application. In vector algebra, reviewed in Chapter 1, all vectors were treated as free vectors.

###### 2.3 Force

Force is the term assigned to mechanical interaction between bodies. A force can affect both the motion and the deformation of the body on which it acts. Forces may arise from direct contact between bodies, or they may be applied at a distance (such as gravitational attraction). Contact forces are distributed over a surface area of the body, whereas forces acting at a distance are distributed over the volume of the body.

Sometimes the area over which a contact force is applied is so small that it may be approximated by a point, in which case the force is said to be concentrated at the point of contact. The contact point is also called the point of application of the force. The line of action of a concentrated force is the line that passes through the point of application and is parallel to the force. In this chapter we consider only concentrated forces; the discussion of distributed forces begins in the next chapter.

Force is a ﬁxed vector, because one of its characteristics (in addition to its magnitude and direction) is its point of application. As an informal proof, consider the three identical bars in Fig. 2.1, each loaded by two equal but opposite forces of magnitude P. If the forces are applied as shown Fig. 2.1(a), the bar is under tension, and its deformation is an elongation. By interchanging the forces, as seen in Fig. 2.1(b), the bar is placed in compression, resulting in its shortening. The loading in Fig. 2.1(c), where both forces are acting at point A, produces no deformation. Note that the forces in all three cases have the same line of action and the same zero resultant; only the points of application are different. Therefore, we conclude that the point of application is a characteristic of a force, as far as deformation is concerned.

If the bar is rigid, however (meaning that the deformation is negligible), there will be no observable differences in the behavior of the three bars in Fig. 2.1.

###### 2.4 Reduction of Concurrent Force Systems 39

| | | |
|---|---|---|
|A| |B|

P P (a) P P A B

| |
|---|
| |

- (b)

A B

- (c)

P P

###### Fig. 2.1

In other words, the external effects* of the three loadings are identical. It follows that if we are interested only in the external effects, a force can be treated

- as a sliding vector. The above conclusion is summarized by the principle of transmissibility:

A force may be moved anywhere along its line of action without changing its external effects on a rigid body.

Two force systems that produce the same external effects on a rigid body are said to be equivalent. (Sometimes the term rigid-body equivalent is used.)

In summary, a force is a ﬁxed vector tied to a point of application, but if one is interested only in its external effect on a rigid body, a force may be treated as a sliding vector.

As a further illustration of the principle of transmissibility, consider the rigid block shown in Fig. 2.2. The block is subjected to three forces P, Q, and S,

|20 N<br><br>20 N| |Q = 20|
|---|---|---|
| | | |

P =

N

each with magnitude 20 N. The three forces are equal in the mathematical sense: P=Q=S. However, only P and Q would produce identical external effects because they have the same line of action. Because S has a different line of action, its external effect would be different.

S =

###### 2.4 Reduction of Concurrent Force Systems

Fig. 2.2

In this article, we discuss the method for replacing a system of concurrent forces with a single equivalent force.

Consider the forces F1, F2, F3, . . . acting on the rigid body in Fig. 2.3(a) (for convenience, only three of the forces are shown). All the forces are concurrent at point O. (Their lines of action intersect at O.) These forces can be reduced to a single, equivalent force by the following two steps.

- 1. Move the forces along their lines of action to the point of concurrency O, as indicated in Fig. 2.3(b). According to the principle of transmissibility, this

*The external effects that concern us most are the motion (or state of rest) of the body, and the support reactions.

z

z

z

F2

###### F1

Rz

F1 F2

R

Ry

###### =

###### = O

y

y

y

O

O

Rx

F3

x

x

F3

x

(a) (b) (c)

###### Fig. 2.3

operation does not change the external effects on the body. Therefore, the force systems in Figs. 2.3(a) and (b) are equivalent, which is indicated by the equal sign between the ﬁgures.

2. With the forces now at the common point O, compute their resultant R from

the vector sum

###### R= F=F1 + F2 + F3 + ··· (2.1)

This resultant, which is also equivalent to the original force system, is shown in Fig. 2.3(c) together with its rectangular components. Note that Eq. (2.1) determines only the magnitude and direction of the resultant. The line of action of R must pass through the point of concurrency O in order for the equivalence to be valid.

When evaluating Eq. (2.1), any of the graphical or analytical methods for vector addition discussed in Chapter 1 may be used. If rectangular components are chosen, the equivalent scalar equations for determining the resultant force R are

###### Rx = Fx Ry = Fy Rz = Fz (2.2)

Thus we see that three scalar equations are required to determine the resultant force for a concurrent system of forces. If the original forces lie in a common plane—say, the xy-plane—the equation Rz = Fz yields no independent information and only the following two equations are necessary to determine the resultant force.

Rx = Fx Ry = Fy (2.3)

We emphasize that the method described here for determining the resultant force is valid only for forces that are concurrent. Because a force is tied to its line of action, the reduction of nonconcurrent force systems will require additional concepts, which are discussed later.

|Sample Problem 2.1<br><br>Determine the resultant of the three concurrent forces shown in Fig. (a).<br><br>(a)<br><br>y<br><br>A<br><br>x<br><br>F3 = 60 N<br><br>F2 = 10 N F1 = 50 N<br><br>60°<br><br>4 3<br><br>Solution<br><br>Because the three forces are concurrent at point A, they may be added immediately to obtain the resultant force R.<br><br>The rectangular components of each of the three forces are shown in Fig. (b). y<br><br>x<br><br>|8.66 N<br><br>5 N<br><br>|50 4 = 5<br><br>|
|---|---|
|A|60 N<br><br>50 3 = 5|
<br><br>40 N 10 sin 60° = 8<br><br>10 cos 60° =<br><br>(b)<br><br>30 N<br><br>Using Eqs. (2.3) to determine the components of the resultant, we have<br><br>Rx = Fx −→+ Rx =30 − 5=25 N<br><br>and<br><br>Ry = Fy +  Ry =40 + 8.66 − 60= − 11.34 N<br><br>The signs in these equations indicate that Rx acts to the right and Ry acts downward. The resultant force R is shown in Fig. (c). Note that the magnitude of the resultant is 27.5N and that it acts through point A (the original point of concurrency) at the 24.4◦ angle shown.<br><br>|A|25|
|---|---|
| |θ<br><br>|
<br><br>y<br><br>x<br><br>(c)<br><br>N<br><br>11.34 N<br><br>R = 27.5 N θ = tan–1 11.34 = 24.4° 25<br><br>The foregoing solution could also have been accomplished using vector notation. The forces would ﬁrst be written in vector form as follows,<br><br>F1 = 30i + 40j N<br>F2 = −5i + 8.66j N<br>F3 = −60j N<br>|
|---|

|and the resultant force R would then be determined from the vector equation<br><br>R = F=F1 + F2 + F3 R = (30i + 40j) + (−5i + 8.66j) + (−60j) R = 25i − 11.34j N Answer<br><br>Whether you use scalar or vector notation is a matter of personal preference.<br><br>Sample Problem 2.2<br><br>Three ropes are attached to the post at A in Fig. (a). The forces in the ropes are F1 = 260lb, F2 = 75lb, and F3 = 60lb. Determine (1) the magnitude of the force R that is equivalent to the three forces shown, and (2) the coordinates of the point where the line of action of R intersects the yz-plane.<br><br>z<br><br>y<br><br>x<br><br>B<br><br>3ft<br>4 ft<br><br><br>F3 A<br><br>F1<br><br>F2<br><br>(a)<br><br>C<br><br>12 ft<br><br>Solution<br><br>Part 1<br><br>The forces are concurrent at point A and thus may be added immediately. Because the forces do not lie in a coordinate plane, it is convenient to use vector notation.<br><br>One method for expressing each of the forces in vector notation is to use the form F= Fλ, where λ is the unit vector in the direction of the force F. Thus<br><br>F1 = 260λAB = 260<br><br>−AB→ |<br><br>−AB→|<br><br>=260 −3i − 12j + 4k<br><br>13<br><br>= −60i − 240j + 80k lb<br><br>F2 = 75λAC = 75<br><br>−AC→ |<br><br>−AC→|<br><br>=75 −3i + 4k<br><br>5<br><br>= −45i + 60k lb<br><br>F3 = −60j lb<br>|
|---|

###### 42

|The resultant force is given by<br><br>R = F=F1 + F2 + F3<br><br>= (−60i − 240j + 80k) + (−45i + 60k) + (−60j)<br><br>= −105i − 300j + 140k lb<br><br>The magnitude of R is<br><br>R = (−105)2 + (−300)2 + (140)2 =347.3 lb Answer<br><br>Part 2<br><br>The unit vector λ in the direction of R is<br><br>λ =<br><br>R R =<br><br>−105i − 300j + 140k 347.3<br><br>= −0.3023i − 0.8638j + 0.4031k<br><br>(b)<br><br>12 ft<br><br>zD<br><br>yD D 12 – yD<br><br>z<br><br>x<br><br>A<br><br>y λ<br><br>3ft<br><br>Let D be the point where λ intersects the yz-plane, as shown in Fig. (b). The coordinates of D can be determined by proportions:<br><br>|λx|<br><br>3 =<br><br>λy<br><br>12 − yD =<br><br>|λz| zD Substituting the components of λ, this becomes<br><br>0.3023 3 =<br><br>0.8638 12 − yD =<br><br>0.4031 zD yielding<br><br>yD = 3.43 ft zD = 4.0 ft Answer|
|---|

![image 10](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile10.png>)

###### Problems

###### 2.1 Which of the force systems shown are equivalent to the 500-N force in (a)?

|500 N| |
|---|---|

4 m

250 N 335 N

3 m A 2 m (a)

A (b)

| |500 N|
|---|---|
| | |

250 N 335 N

A (c)

A (d)

559 N

250 N

559 N

250 N

A (f)

A (e)

500 N

500 N

| | |
|---|---|
| | |

250 N

250 N

A (h)

A (g)

###### Fig. P2.1

###### 2.2 Two men are trying to roll the boulder by applying the forces shown. Deter-

70°

mine the magnitude and direction of the force that is equivalent to the two applied forces.

300 lb

150 lb

20°

- 2.3 The magnitudes of the three forces applied to the eye bolt are T1 = 110lb, T2 = 40lb, and T3 = 150lb. Replace these forces with a single equivalent force R. Show the result on a sketch of the eye bolt.

|60°|40°<br><br>|
|---|---|
| | |

x

y

T3

T2 T1

Fig. P2.3

- 2.4 Determine P and θ so that the three forces shown are equivalent to the single force R = 85i + 20j kN.

x 60°

θ

P y

40 kN

30 kN

|120 mm| |
|---|---|
| | |

100 mm

80 mm

y

x

z

40 N

30 N 60 N

Fig. P2.4 Fig. P2.5

- 2.5 Replace the three forces acting on the bracket by a single, equivalent force.
- 2.6 The forces P1 = 110lb, P2 = 200lb, and P3 = 150lb are equivalent to a

y

z

x

P3

P2

P1

40°

25°

2 ft

Fig. P2.6, P2.7

single force R. Determine (a) the magnitude of R; and (b) the coordinates of the point where the line of action of R crosses the yz-plane.

- 2.7 Determine the magnitudes of the three forces P1, P2, and P3, given that they are equivalent to the force R= − 600i + 500j + 300k lb.

Fig. P2.2

z 2.8 The magnitudes of the three forces acting on the plate are T1 =

100kN, T2 = 80kN and T3 = 50kN. Replace these forces with a single equivalent force R. Also, ﬁnd the coordinates of the point where R intersects the plate.

6 m

T1

- 2.9 Determine the three forces acting on the plate that are equivalent to the force R = 210kkN.
- 2.10 The force R is the resultant of the forces P1, P2, and P3 acting on the rectangular plate. Find P1 and P2 if R =40 kN and P3 =20 kN.

P2

R

30°

300

Dimensions in mm

y

P3 x

P1

400600

300

x

y

8 in.

4 in.

x

A

18 lb

24 lb

Fig. P2.10 Fig. P2.11

- 2.11 The two forces are equivalent to a force R that has a line of action passing through point A. Determine R and the distance x.

35°

Q = 30 lb

x

A

y

P 8 in. 5 in.

8.5 in.

Fig. P2.12

- 2.12 Knowing that the forces P and Q are equivalent to a single force R that passes through point A, determine P and R.
- 2.13 The four forces are to be replaced by a single, equivalent force. Determine

- 1.0m

T3

2m

T2

2m

3m

x y

2m

Fig. P2.8, P2.9

z

15 lb

20 lb 20 lb 15 lb

75°

y

10 in.

x

the rectangular components of this force and the point of intersection of its line of action with the plate.

Fig. P2.13

###### 2.14 Find the forces Q1, Q2, and Q3 so that the two force systems are equivalent.

3 ft

3 ft

3ft

3ft

Q3

P2 = 120 lb

P1 = 100 lb

z

4 ft

4 ft

Q1

P3 = 60 lb

Q2

y x

###### Fig. P2.14

###### 2.15 The man exerts a force P of magnitude 50 lb on the handles of the wheelbarrow. Knowing that the resultant of the forces P, Q (the reaction at the wheel), and W (the weight of the wheelbarrow) is the force R = 10ilb, determine W.

30° 45°

P

W

y

x

Q

Fig. P2.15

###### 2.16 The three forces acting on the beam can be replaced with a single equivalent force R. Determine the angle θ and R.

P2 = 60 kN

P3 = 80 kN

P1 = 25 kN

y

θ 50°

40°

| | |
|---|---|
| | |
| | |
|4 m|6 m|

x

###### Fig. P2.16

z

240 N

y

300 N

A

25°

6 ft

A y

1.2 m

x

1.2 m

z

###### Fig. P2.17

4ft

3ft

T3

- 2.17 The trapdoor is held in the horizontal plane by two wires. Replace the forces in the wires with an equivalent force R that passes through point A, and determine the y-coordinate of point A.
- 2.18 Replace the three forces acting on the guy wires by a single, equivalent

O

3ft

2ft

T1

x y

T2

Fig. P2.18 force acting on the ﬂagpole. Use T1 =200 lb, T2 =400 lb, and T3 =350 lb.

2.19 The three forces acting on the pole are equivalent to a single force R.

Determine (a) the magnitude of R; and (b) the coordinates of the point where the line of action of R crosses the xy-plane.

120 lb

2.20 The three forces, each of magnitude F, are applied to the crate. Determine F so that the three forces are equivalent to a single 600-lb force.

30ft60ft

30° 30°

z

80 lb 160 lb

y

180 ft

10 tons

F

35° 20°

y

x

| | | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |

A B

25° 45°

F

8 tons

50°

F

x

8 tons

Fig. P2.19

###### Fig. P2.20 Fig. P2.21

∗2.21 Determine the resultant force R that is equivalent to the forces exerted by the three tugboats as they maneuver the barge. Specify the coordinate of the point on the x-axis through which R passes. (Hint: First determine the resultant force for the two forces at point A, and then combine this result with the force at point B.)

###### 2.5 Moment of a Force about a Point

In general, a force acting on a rigid body tends to rotate, as well as translate, the body. The force itself is the translational effect—the body tends to move in the direction of the force, and the magnitude of the force is proportional to its ability to translate the body. (The formal statement of this relationship is Newton’s second law: Force equals mass times acceleration.) Here we introduce the tendency of a force to rotate a body, called the moment of a force about a point. This rotational effect depends on the magnitude of the force and the distance between the point and the line of action of the force. The tendency of a force to rotate a body about an axis, called the moment of a force about an axis, is discussed in the next article.

###### a. Deﬁnition

Let F be a force and O a point that is not on the line of action of F, as shown in Fig. 2.4. Note that the force F and the point O determine a unique plane. We let A F

MO

be any point on the line of action of F and deﬁne r to be the vector from point O to point A.

A r

The moment of the force F about point O, called the moment center, is deﬁned as

θ

O

d

Plane determined by O and F

MO =r × F (2.4)

Note that moment about a point has the dimension [FL]. In SI units, moment is measured in newton-meters (N · m). In U.S. Customary units, pound-inches (lb · in.) and pound-feet (lb · ft) are commonly used.

Fig. 2.4

The moment of F about point O is a vector by deﬁnition. From the properties of the cross product of two vectors, MO is perpendicular to both r and F, with its sense determined by the right-hand rule, as shown in Fig. 2.4.*

###### b. Geometric interpretation

The moment of a force about a point can always be computed using the cross product in Eq. (2.4). However, a scalar computation of the magnitude of the moment can be obtained from the geometric interpretation of Eq. (2.4).

Observe that the magnitude of MO is given by

MO =|MO|=|r × F|=rF sinθ (2.5) in which θ is the angle between r and F. Returning to Fig. 2.4, we see that

r sinθ =d (2.6)

where d is the perpendicular distance from the moment center to the line of action of the force F called the moment arm of the force. Therefore, the magnitude of MO is

MO = Fd (2.7)

*Moment vectors are drawn as double-headed arrows throughout this text.

Because the magnitude of MO depends only on the magnitude of the force and the perpendicular distance d, a force may be moved anywhere along its line of action without changing its moment about a point. Therefore, in this application, a force may be treated as a sliding vector. This explains why any point A on the line of action of the force may be chosen when determining the vector r in Eq. (2.4).

Equation (2.7) is convenient only when the moment arm can be easily determined. Furthermore, when using Eq. (2.7), the direction of MO must be found by inspection. For example, the magnitude of the moment of the 100-N force about the point O in Fig. 2.5(a) is (100)(2)=200 N · m, and its direction is counterclockwise, as viewed from the positive z-axis. Using the right-hand rule, the vector representation of this moment is MO =200kN · m, as shown in Fig. 2.5(b). The magnitude of the moment about point O for the 100-N force in Fig. 2.5(c) is also 200 N · m, but in this case its direction is clockwise, as viewed from the positive z-axis. For this force, MO = − 200kN · m, as shown in Fig. 2.5(d). Although the vector description for both forces is −100i N, their moments about point O are oppositely directed.

z

z

MO = 200k N.m

100 N

2 m

O

O

y

y

MO = 200 N.m

x

x

(b)

(a)

z

z

100 N

MO = –200k N.m

O

O

y

y

2 m

MO = 200 N.m

x

x

(d)

(c)

###### Fig. 2.5

###### c. Principle of moments

When determining the moment of a force about a point, it is often convenient to use the principle of moments, also known as Varignon’s theorem:

The moment of a force about a point is equal to the sum of the moments of its components about that point.

###### Proof

To prove Varignon’s theorem, consider the three forces F1, F2, and F3 concurrent

- at point A, as shown in Fig. 2.6, where r is the vector from point O to point A. The z

sum of the moments about point O for the three forces is

F1

- F2
- F3

MO = (r × F)=(r × F1) + (r × F2) + (r × F3) (a) Using the properties of the cross product, Eq. (a) may be written as

A

r

O

y

MO =r × (F1 + F2 + F3)=r × R (b)

where R=F1 + F2 + F3 is the resultant force for the three original forces. Equation (b) proves the principle of moments: The moment of R equals the moments of the components of R. (Although the preceding proof has used only three components, it may obviously be extended to any number of components.)

x

Fig. 2.6

###### d. Vector and scalar methods

From the preceding discussion, we observe that the following are equivalent methods for computing the moment of a force F about a point O.

Vector Method The vector method uses MO =r × F, where r is a vector from point O to any point on the line of action of F. The most efﬁcient technique for using the vector method (with rectangular components) is the following: (1) Write F in vector form; (2) choose an r, and write it in vector form; and (3) use the determinant form of r × F to evaluate MO:

i j k x y z Fx Fy Fz

MO =r × F=

(2.8)

z

Fz

where the second and third lines in the determinant are the rectangular components of r and F, respectively. These components are shown in Fig. 2.7. Expansion

z

of the determinant in Eq. (2.8) yields

A r

Fy Fx

MO =(yFz − zFy)i + (zFx − xFz)j + (xFy − yFx)k (2.9)

O

y

x

Scalar Method In the scalar method, the magnitude of the moment of the force F about the point O is found from MO = Fd, where d is the moment arm of the force. In this method, the sense of the moment must be determined by inspection. As mentioned previously, the scalar method is convenient only when the moment arm d can be easily determined.

y

x

Fig. 2.7

|Sample Problem 2.3<br><br>Determine (1) the moment of the force F about point C; and (2) the perpendicular distance between C and the line of action of F.<br><br>z<br><br>y<br><br>x<br><br>B<br><br>2m<br><br>3 m<br><br>A<br><br>F = 500 N<br><br>rCA 4 m C<br><br>Solution<br><br>Part 1<br><br>The moment of a force about point C can be computed by either the scalar method (MC = Fd), or the vector method (MC =r×F). In this problem the scalar method would be inconvenient, because we have no easy means of determining d (the perpendicular distance between C and the line AB). Therefore, we use the vector method, which consists of the following three steps: (1) write F in vector form; (2) choose an r, and write it in vector form; and (3) compute MC =r × F.<br><br>Step 1: Write F in vector form. Referring to the ﬁgure, we obtain<br><br>F=500λAB =500<br><br>−AB→ |<br><br>−AB→|<br><br>=500<br><br>2i − 4j + 3k 5.385<br><br>which yields<br><br>F=185.7i − 371.4j + 278.6k N<br><br>Step 2: Choose an r, and write it in vector form. The vector r is a vector from point C to any point on the line of<br><br><br>action of F. From the ﬁgure we see that there are two convenient choices for r—the vector from point C to either point A or point B. As shown in the ﬁgure, let us choose r to be rC A. (As an exercise, you may wish to solve this problem by choosing r to be the vector from point C to point B.) Now we have<br><br>r=rC A = − 2i m|
|---|

|Step 3: Calculate MC = r × F.<br><br>The easiest method for evaluating the cross product is to use the determinant expansion:<br><br>MC =r × F=rC A × F=<br><br>i j k −2 0 0 185.7 −371.4 278.6 Expanding this determinant gives<br><br>MC =557.2j + 742.8k N · m Answer<br><br>Part 2<br><br>The magnitude of MC is<br><br>MC = (557.2)2 + (742.8)2 =928.6 N · m<br><br>The perpendicular distance d from point C to the line of action of F may be determined by<br><br>d =<br><br>MC F =<br><br>928.6<br><br>500 =1.857 m Answer Observe that, instead of using the perpendicular distance to determine the moment, we have used the moment to determine the perpendicular distance.<br><br>Caution A common mistake is choosing the wrong sense for r in Eq. (2.4). Note that r is directed from the moment center to the line of action of F. If the sense of r is reversed, r × F will yield the correct magnitude of the moment, but the wrong sense. To avoid this pitfall, it is strongly recommended that you draw r on your sketch before attempting to write it in vector form.<br><br>Sample Problem 2.4<br><br>Determine the moment of the force F in Fig. (a) about point A.<br><br>F = 200 lb<br><br>| | | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | |C| | | |
| | | | | | | | |
| | | | | | | | |
| | |x| | | | | |
<br><br>1 in.<br><br>1 in.<br><br>3<br><br>4<br>5<br><br><br>O D<br><br>(a)<br><br>B<br><br>A<br><br>y|
|---|

|Solution<br><br>The force F and point A lie in the xy-plane. Problems of this type may be solved using either the vector method (r × F) or the scalar method (Fd). For illustrative purposes, we use both methods.<br><br>Vector Solution<br><br>Recall that the three steps in the vector method are to write F in vector form, choose r and write it in vector form, and then evaluate the cross product r × F.<br><br>Writing F in vector form, we get<br><br>F = −<br><br>4<br><br>5<br><br><br>200i +<br><br>3 5<br><br>200j<br><br>= −160i + 120j lb<br><br>There are several good choices for r in this problem, three of which are rAB, rAC, and rAD. Choosing<br><br>r=rAB = − 4i + 6j in.<br><br>the moment about point A is<br><br>MA =r × F=rAB × F=<br><br>i j k −4 6 0<br><br>−160 120 0<br><br>Expanding this determinant, we obtain<br><br>MA =k[(120)(−4) + (160)(6)]=480k lb · in. Answer<br><br>The magnitude of MA is 480 lb·in. Note that the direction of MA is the positive z direction, which by the right-hand rule means that the moment about point A is counterclockwise.<br><br>Scalar Solution<br><br>In Fig. (b), we have resolved the force into the rectangular components F1 and F2 at point B. The moment arm of each component about point A (the perpendicular distance between A and the line of action of the force) can be determined by inspection. The moment arms are d1 = 6in. for F1 and d2 = 4in. for F2, as shown in Fig. (b).<br><br>The moment of F about A now can be obtained by the principle of moments. Nothing that the moment of F1 is counterclockwise, whereas the moment of F2 is clockwise, we obtain<br><br>+ MA = F1d1 − F2d2<br><br>= 160(6) − 120(4) = 480 lb · in.|
|---|

|F<br><br>| |2| | | | | | | |
|---|---|---|---|---|---|---|---|---|
|B<br><br>y<br><br>d1| | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | |x| | | | | |
<br><br>= 120 lb 1 in.<br><br>1 in.<br><br>(b)<br><br>A<br><br>F1= 160 lb<br><br>F<br><br>d2<br><br>Note that the sense of MA is counterclockwise. Applying the right-hand rule, the vector representation of the moment is<br><br>MA = 480k lb · in. Answer<br><br>Recall that a force, being a sliding vector, can be moved to any point on its line of action without changing its moment. In Fig. (c) we have moved F to point C. Now the moment arm of F1 about A is d1 = 3in., and the moment arm of F2 is zero. Hence, the moment of F about A is<br><br>+ MA = F1d1 = 160(3) = 480 lb · in.<br><br>counterclockwise, as before.<br><br>1 in.<br><br>1 in.<br><br>(c)<br><br>x<br><br>A<br><br>B<br><br>y C<br><br>D<br><br>F2= 120 lb F1= 160 lb<br><br>F<br><br>d1<br><br>Another convenient location for F would be point D in Fig. (c). Here the moment arm of F1 about A is zero, whereas the moment arm of F2 is 4in., which again yields MA = 480lb · in. counterclockwise.|
|---|

![image 11](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile11.png>)

###### Problems

###### 800 N 2.22 Determine the magnitude and sense of the moment of the 800-N force

about point A.

38°

- 2.23 Find the magnitude and sense of the moment of the 60-lb force about points A and B.

24 in.

12 in. 40 in.

60 lb

A B

| |
|---|
| |

5.5 m 2.5 m

x

P

B

P

y

A

C b

3.5 m

Fig. P2.23 Fig. P2.24

- 2.24 The two forces can be replaced by an equivalent force R acting at point B on the beam. Determine the distance b that locates B. (Hint: The combined moment of the two forces about any point is equal to the moment of R about the same point.)
- 2.25 A force P in the xy-plane acts on the triangular plate. The moments of P

about points O, A, and B are MO =200 N · m clockwise, MA =0, and MB =0. Determine P.

- 2.26 A force P in the xy-plane acts on the triangular plate. The moments of P about points O, A, and B are MO =80 N · m counterclockwise, MA =200 N · m clockwise, and MB =0. Determine P.

y

A

O B

x

500 mm

400 mm

x

y

O

A 5 in.

12 in.

F

Fig. P2.25, P2.26 Fig. P2.27

- 2.27 Determine the moment of the force F=9i + 18j lb about point O by the following methods: (a) vector method using r × F; (b) scalar method using rectangular components of F; and (c) scalar method using components of F that are parallel and perpendicular to the line OA.

0.6 m

A

0.5 m

Fig. P2.22

- 2.28 Given that T =28.3 kN and W =25 kN, determine the magnitude and sense of the moments about point B of the following: (a) the force T; (b) the force W; and (c) forces T and W combined.

36 m

T

20 m 16 m

B

W

Fig. P2.28

- 2.29 A moment of 50 lb · ft about O is required to loosen the nut. Determine the smallest magnitude of the force F and the corresponding angle θ that will turn the nut.

F

θ

O

15in

.

Fig. P2.29

- 2.30 Knowing that the forces P and Q are equivalent to a single force R that passes through point A, determine P. (Hint: The combined moment of P and Q about A is zero.)

35°

Q = 30 lb

x

A

y

P

8.5 in.

8 in. 5 in.

Fig. P2.30

- 2.31 The resultant of the two forces shown has a line of action that passes

y

8 in.

24 lb

18 lb

4 in.

A

x

x

through point A. Recognizing that the moment of the resultant about A is zero, determine the distance x.

Fig. P2.31

- 2.32 The tow truck’s front wheels will be lifted off the ground if the moment of the load W about the rear axle exceeds the moment of the 6200-lb weight of the truck. Determine the largest W that may be safely applied.

W

4 ft

30°

6ft

6200 lb

8 ft 10 ft

Fig. P2.32

- 2.33 The force F acts on the gripper of the robot arm. The moments of F about points A and B are 210 N · m and 90 N · m, respectively—both counterclockwise. Determine F and the angle θ.

150 mm

300 mm

600 mm

A

B

800 mm

30°

F

θ

Fig. P2.33

- 2.34 Compute the moment of the force P about point A.

P = 200 N

70mm 90mm

100 mm

C

B

y

z

x

A

x

y

z B C

O

D

Q P

600 mm A

360mm

500mm

Fig. P2.34 Fig. P2.35, P2.36

- 2.35 The magnitude of the force P is 100N. Determine the moments of P about (a) point O; and (b) point C.
- 2.36 The magnitude of the force Q is 250N. Determine the moments of Q about (a) point O; and (b) point C.

- 2.37 The magnitude of the moment of force P about point O is 200 kN · m. z O

P

25°

B C

x

A

3 m

2m

4 m

y

Fig. P2.37, P2.38

Determine the magnitude of P.

- 2.38 The magnitude of the force P is 50 kN. Determine the moment of P about (a) point A; and (b) point B.
- 2.39 Determine the moments of Q about (a) point O; and (b) point C. The magnitude of Q is 20lb.

Q

z

x

C

y

A

8 ft

3ft

B

OO

4 ft

z A

3ft

2ft 2ft

4.2ft

O

C

y

2 ft

B

x

P

Q

Fig. P2.39 Fig. P2.40

- 2.40 Find the combined moment of the forces P and Q about point O. The magnitudes of the forces are P = 80lb and Q = 60lb.
- 2.41 The wrench is used to tighten a nut on the wheel. Determine the moment of the 120-lb force about the origin O. Express your answer in vector form.

12

i

n

.

4

i

n.

y

z

x

120 lb

12in.

O

Fig. P2.41

- 2.42 The magnitudes of the two forces shown are P =16 lb and Q =22 lb.

P

Q

###### A

z

8 in.

40°

3 in.

y

O

| | | |
|---|---|---|
| | | |

x

Determine the magnitude of the combined moment of P and Q about point O and the direction cosines of this moment vector.

Fig. P2.42

z

2.43 The moment of the force F = 50i − 100j − 70k lb about point O is

MO = 400i + 410j − 300k lb·ft. Determine the coordinates of the point where the line of action of F intersects the xz-plane.

F

x

- 2.44 Determine the magnitude of the moment of the 150-N force about point O and ﬁnd the direction cosines of the moment vector.

150 N z

y

x

60mm

50mm

30°

40

mm

O

A

a

a

P P

a

A

y

x

z

d

Fig. P2.44 Fig. P2.45

- 2.45 The combined moment of the two forces, each of magnitude P, about point A is zero. Determine the distance d that locates A.
- 2.46 The force F = −20i + 4j + 6k lb acts at point A. Determine the coordinates of point B where the line of action of F intersects the xy-plane. (Hint: The moment of F about B is zero.)

z

O

y

x

Fig. P2.43

z

y

B

###### F

A

z

x

2 ft 4ft

y

3ft

###### Fig. P2.46

###### 2.6 Moment of a Force about an Axis

Whereas the preceding article deﬁned the moment of a force about a point, this article discusses the moment of a force about an axis. Because moment about an axis is a measure of the tendency of a force to rotate a body about the axis, it is fundamental to the study of engineering mechanics. We begin with a formal deﬁnition of the moment about an axis, and we then examine its geometric interpretation.

B

###### a. Deﬁnition

The moment of a force about an axis, called the moment axis, is most easily deﬁned in terms of the moment of the force about a point on the axis. Figure 2.8

λ

shows the force F and its moment MO =r × F about point O, where O is any point on the axis AB. We deﬁne the moment about an axis as follows:

MO = r×F

α

MAB = MO cos

α

The moment of F about the axis AB is the orthogonal component of MO along the axis AB, where O is any point on AB.

F

r O

Letting λ be a unit vector directed from A toward B, this deﬁnition gives for the moment of F about the axis AB

Plane determined by O and F

###### MAB = MO cosα (2.10)

A

where α is the angle between MO and λ, as shown in Fig. 2.8.

Fig. 2.8

Because MO cosα =MO ·λ (from the deﬁnition of the dot product), Eq. (2.10) can also be expressed in the form

###### MAB =MO ·λ=r × F·λ (2.11)

Let us review each of the terms appearing in this equation:

- • MAB is the moment (actually, the magnitude of the moment) of the force F about the axis AB.
- • MO represents the moment of F about the point O, where O is any point on the axis AB.*
- • λ is the unit vector directed from A toward B.
- • r is the position vector drawn from O to any point on the line of action of F.

B

Note that the direction of λ determines the positive sense of MAB by the right-hand rule, as illustrated in Fig. 2.9. Paying heed to this sign convention will enable you

to interpret correctly the sign of MAB in Eqs. (2.10) and (2.11).

Sometimes we wish to express the moment of F about the axis AB as a vector. We can do this by multiplying MAB by the unit vector λ that speciﬁes the direction of the moment axis, yielding

- A

λ

+MAB

(a)

A

λ

- B

###### MAB = MABλ=(r × F·λ)λ (2.12)

+MAB

Rectangular components of MO Let MO be the moment of a force F about O, where O is the origin of the xyz-coordinate system shown in Fig. 2.10. The

(b)

*If we let O and C be two points on the moment axis AB, then MO and MC will, in general, be different. However, it can be shown that MO ·λ=MC ·λ, where λ is a unit vector parallel to AB. For this reason, O in Eq. (2.10) can be any point on AB.

Fig. 2.9

z

Mz

MO

My

y

O

Mx

x

###### Fig. 2.10

moments of F about the three coordinate axes can be obtained from Eq. (2.11) by substituting i, j, and k in turn for λ. The results are

Mx =MO ·i My =MO ·j Mz =MO ·k from which we draw the following conclusion:

The rectangular components of the moment of a force about the origin O are equal to the moments of the force about the coordinate axes.

In other words,

MO = Mxi + Myj + Mzk (2.13)

- A by O and F

O

- B

where Mx, My, and Mz, shown in Fig. 2.10, are equal to the moments of the force about the coordinate axes.

λ

Special Case: Moment Axis Perpendicular to F Consider the case where the moment axis is perpendicular to the plane containing the force F and the point O, as shown in Fig. 2.11(a). Because the directions of MO and MAB now coincide, λ

MAB = MO

F

O r

in Eq. (2.11) is in the direction of MO. Consequently, Eq. (2.11) yields

MO = MAB (2.14) That is, the moment of F about point O equals the moment of F about the axis AB.

Plane determined

A two-dimensional representation of Fig. 2.11(a), viewed along the moment axis AB, is shown in Fig. 2.11(b). We will frequently use a similar ﬁgure in the solution of two-dimensional problems (problems where all forces lie in the same plane). In problems of this type, it is customary to use the term moment about a point (MO), rather than moment about an axis (MAB).

- (a)
- (b)

MAB = MO

F

r

###### b. Geometric interpretation

It is instructive to examine the geometric interpretation of the equation MAB = r × F·λ.

Suppose we are given an arbitrary force F and an arbitrary axis AB, as shown in Fig. 2.12. We construct a plane that is perpendicular to the AB axis and let O and C be the points where the axis and the line of action of the force intersect ,

Fig. 2.11

B

F

λ

F1

###### MO = r×F

MAB = F2d

F2 r C

O

d

Plane

A

###### Fig. 2.12

respectively. The vector from O to C is denoted by r, and λ is the unit vector along the axis AB. We then resolve F into two components: F1 and F2, which are parallel and perpendicular to the axis AB, respectively (observe that F2 lies in plane ). In terms of these components, the moment of F about the axis AB is

MAB =r × F · λ = r × (F1 + F2)·λ

###### = r × F1 ·λ + r × F2 ·λ

Because r × F1 is perpendicular to λ, r × F1 ·λ=0, and we get

MAB =r × F2 ·λ

Substitution of r × F2 ·λ= F2d, where d is the perpendicular distance from O to the line of action of F2, yields

MAB = F2d (2.15)

We see that the moment of F about the axis AB equals the product of the component of F that is perpendicular to AB and the perpendicular distance of this component from AB. Observe that Eq. (2.15) gives only the magnitude of the moment about the axis; its sense must be determined by inspection.

Consideration of Eq. (2.15) reveals that the moment of a force about an axis, as deﬁned in Eq. (2.10), possesses the following physical characteristics:

- • A force that is parallel to the moment axis (such as F1) has no moment about that axis.
- • If the line of action of a force intersects the moment axis (d =0), the force has no moment about that axis.
- • The moment of a force is proportional to its component that is perpendicular to the moment axis (such as F2), and the moment arm (d) of that component.
- • The sense of the moment is consistent with the direction in which the force would tend to rotate a body.

z

Direction of rotation

Hinge axis

Pz

y

x Py

Px

###### Fig. 2.13

To illustrate the above characteristics, consider opening the door in Fig. 2.13 by applying a force P to the handle. In the ﬁgure, P is resolved into the following rectangular components: Px intersects the hinge axis, Py is perpendicular to the door, and Pz is parallel to the hinge axis.

To open the door, we must apply a moment about the z-axis (the hinge axis). Experience tells us that Py is the only component of the force that would accomplish this task. The components Px and Pz are ineffective, because their moments about the z-axis are zero. We also know that it is easier to open the door if we increase the distance between the handle and the hinge axis (the moment arm) or if the magnitude of Py is increased. Finally, observe that Py causes the door to rotate in the direction shown in the ﬁgure, which is also the sense of the moment about the z-axis.

###### c. Vector and scalar methods

From the preceding discussion we see that the moment of the force F about an axis AB can be computed by two methods.

Vector Method The moment of F about AB is obtained from the triple scalar product MAB =r×F·λ, where r is a vector drawn from any point on the moment axis AB to any point on the line of action of F and λ represents a unit directed from A toward B. A convenient means of evaluating the scalar triple product is its determinant form

x y z Fx Fy Fz λx λy λz

(2.16)

MAB =

where x, y, and z are the rectangular components of r.

Scalar Method The moment of F about AB is obtained from the scalar expression MAB = F2d. The sense of the moment must be determined by inspection. This method is convenient if AB is parallel to one of the coordinate axes (which is always the case in two-dimensional problems).

|Sample Problem 2.5<br><br>The force F of magnitude 195kN acts along the line AB. (1) Determine the moments Mx, My, and Mz of F about the coordinate axes by the scalar method; and (2) ﬁnd the moment of F about point O by the vector method and verify that MO = Mxi + Myj + Mzk.<br><br>45 kN<br><br>4 m y<br><br>x<br><br>O<br><br>z<br><br>12 m B<br><br>F = 195 kN 60 kN<br><br>3m<br><br>A 180 kN<br><br>(a)<br><br>Solution<br><br>We start by computing the rectangular components of F:<br><br>F = FλAB = F<br><br>−AB→ |<br><br>−AB→|<br><br>=195<br><br>3i + 12j − 4k 32 + 122 + (−4)2<br><br>= 45i + 180j − 60k kN<br><br>When calculating the moment of a force, the force may be placed at any point on its line of action. As shown in Fig. (a), we chose to have the force acting at point A.<br><br>Part 1<br><br>The moment of F about a coordinate axis can be computed by summing the moments of the components of F about that axis (the principle of moments).<br><br>Moment about the x-Axis Figure (b) represents a two-dimensional version of<br><br>z<br><br>y<br><br>A<br><br>4 m<br><br>45 kN<br><br>O<br><br>O<br><br>180 kN<br><br>(b)<br><br>60 kN<br><br>z<br><br>x<br><br>A<br><br>4 m<br><br>45 kN 180 kN<br><br>(c)<br><br>60 kN<br><br>720 kN . m<br><br>180 kN . m<br><br>Fig. (a), showing the yz-plane. We see that the 45-kN and the 60-kN components of the force contribute nothing to the moment about the x-axis (the former is parallel to the axis, and the latter intersects the axis). The perpendicular distance (moment arm) between the 180-kN component and the x-axis is 4 m. Therefore, the moment of this component about the x-axis (which is also the moment of F) is 180(4)=720 kN · m, clockwise. According to the right-hand rule, the positive sense of Mx is counterclockwise, which means that Mx is negative; that is,<br><br>Mx = − 720 kN · m Answer<br><br>Moment about the y-Axis To compute the moment about the y-axis, we refer to Fig. (c), which represents the xz-plane. We note that only the 45-kN force component has a moment about the y-axis, because the 180-kN component is parallel to the y-axis and the 60-kN component intersects the y-axis. Because the<br>|
|---|

|moment arm of the 45-kN component is 4 m, the moment of F about the y-axis is 45(4)=180 kN · m, counterclockwise. Therefore, we have<br><br>My =45(4)=180 kN · m Answer<br><br>The sign of the moment is positive, because the right-hand rule determines positive My to be counterclockwise.<br><br>Moment about the z-Axis The moment of F about the z-axis is zero, because F intersects that axis. Hence<br><br>Mz =0 Answer<br><br>Part 2<br><br>Recognizing that the vector from O to A in Fig. (a) is rO A =4k m, the moment of F about point O can be computed as follows.<br><br>MO =rO A × F =<br><br>i j k 0 0 4 45 180 −60<br><br>= − i(4)(180) + j(4)(45)<br><br>= −720i + 180j kN · m Answer<br><br>Comparing with MO = Mxi + Myj + Mzk, we see that<br><br>Mx = − 720 kN · m My =180 kN · m Mz =0<br><br>which agree with the results obtained in Part 1.<br><br>Sample Problem 2.6<br><br>The force F of Sample Problem 2.5 is shown again in Fig. (a). (1) Determine the moment of F about the axis CE; and (2) express the moment found in Part 1 in vector form.<br><br>(a)<br><br>45 kN<br><br>y<br><br>2 m 4 m<br><br>x<br><br>O<br><br>z<br><br>E 12 m B<br><br>F = 195 kN 60 kN<br><br>3m<br><br>A 180 kN<br><br>C|
|---|

|Solution<br><br>Part 1<br><br>Referring to Fig. (a), we see that it is not practical to calculate the moment about the axis CE by the scalar method. Because the axis CE is not parallel to a coordinate axis, the task of determining the perpendicular distance between F and CE would be tedious. However, if the vector method is used, the calculation of the moment is straightforward.<br><br>To employ the vector method we ﬁrst express the force F in vector form. This was already done in the solution to Sample Problem 2.5:<br><br>F=45i + 180j − 60k kN<br><br>Next we calculate the moment of F about any convenient point on the axis CE. Inspection of Fig. (a) reveals that there are only two convenient points from which to choose—points C and E. Let us choose point C. Because we will use the cross product r × F to compute the moment about C, our next step is to choose the vector r and to write it in vector form (remember that r must be a vector from point C to any point on the line of action of F). From Fig. (a) we see that there are two convenient choices for r: either the vector from C to A or the vector from C to B. Choosing the latter, we have<br><br>r=rCB = − 4k m<br><br>The moment of F about point C then becomes<br><br>MC = rCB × F=<br><br>i j k 0 0 −4 45 180 −60<br><br>= 720i − 180j kN · m<br><br>Note that the z-component of MC is zero. To understand this result, recall that the z-component of MC equals the moment of F about the axis BC (the line parallel to the z-axis passing through C). Because F intersects BC, its moment about BC is expected to be zero.<br><br>Next, we calculate the unit vector λCE directed from point C toward point E:<br><br>λCE =<br><br>−CE→ |<br><br>−CE→|<br><br>=<br><br>−3i + 2j − 4k (−3)2 + 22 + (−4)2<br><br>= − 0.5571i + 0.3714j − 0.7428k<br><br>The moment of MC about the axis CE can now be obtained from Eq. (2.11):<br><br>MCE = MC ·λCE<br><br>= (720i − 180j)·(−0.5571i + 0.3714j − 0.7428k)<br><br>= −468 kN · m Answer|
|---|

|The negative sign indicates that the sense of the moment is as shown in Fig. (b)that is, opposite to the sense associated with λCE.<br><br>y<br><br>x<br><br>z<br><br>E<br><br>(b)<br><br>C 468 kN·m<br><br>λCE<br><br>We could also compute MCE without ﬁrst determining MC by using the scalar triple product:<br><br>MCE = rBC × F·λCE =<br><br>0 0 −4 45 180 −60 −0.5571 0.3714 −0.7428<br><br>= −468 kN · m<br><br>This agrees, of course, with the result determined previously.<br><br>Part 2<br><br>To express the moment of F about the axis CE in vector form, we multiply MCE by the unit vector λCE, which gives<br><br>MCE = MCEλCE = − 468(−0.5571i + 0.3714j − 0.7428k)<br><br>= 261i − 174j + 348k kN · m Answer<br><br>There is no doubt that using the vector method is convenient when one wishes to calculate the moment about an axis such as CE, which is skewed relative to the coordinate system. However, there is a drawback to vector formalism: You can easily lose appreciation for the physical nature of the problem.|
|---|

![image 12](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile12.png>)

###### Problems

- 2.47 Calculate the combined moment of the three forces about each of the coordinate axes. Use (a) the scalar method; and (b) the vector method.

0.85 m

90 kN

75 kN

160 kN

0.5m

O

A

x

y

z

40 kN B

A

C

600 mm

G

H

D E

F

900 mm

800mm

Fig. P2.47 Fig. P2.48

- 2.48 Determine the moment of the 40-kN force about each of the following axes: (a) AB; (b) CD; (c) CG; (d) CH; and (e) EG.
- 2.49 Determine the moment of the 400-lb force about each of the following

F

H

G

C

|E|
|---|

7.5 ft

z

y

x

9ft

|D|
|---|

4 ft

400 lb

B

A

Fig. P2.49

axes: (a) AB; (b) CD; (c) BF; (d) DH; and (e) BD.

- 2.50 The magnitude of the force F is 75lb. Calculate the moment of F about F

6ft

30°

8ft

z

x

y

Fig. P2.50

the x-axis using (a) the scalar method; and (b) the vector method.

- 2.51 The force F=12i − 8j + 6k N is applied to the gripper of the holding device shown. Determine the moment of F about (a) the a-axis; and (b) the z-axis.

400mm

480mm

z

1 160mm60mm

F

120 mm

y a

x

###### Fig. P2.51

- 2.52 The moment of the force F about the x-axis is 1080 N · m. Determine the moment of F about the axis AB.

y

z

x

12 m

4 m

F B

5m

A

30 N

18 N

y

x

F

20 N

d

1.2 m

O

1.0m

Fig. P2.52 Fig. P2.53, P2.54

- 2.53 Compute the combined moment of the four parallel forces about point O (the center of the table) using F =40 N and d =0.4 m. Express your answer in vector form.
- 2.54 To lift the table without tilting, the combined moment of the four parallel forces must be zero about the x-axis and the y-axis (O is the center of the table). Determine the magnitude of the force F and the distance d.
- 2.55 The combined moment of the three forces is zero about the axis a–a and

40 lb

20 lb

|6 ft y0 a<br><br>x<br><br>0| |
|---|---|
| | |

###### y

6ft

b

b

30 lb

4 ft

a

x

Fig. P2.55 the axis b–b. Determine the distances x0 and y0.

- 2.56 The trap door is held open by the rope AB. If the tension in the rope is T = 40lb, determine its moment about the y-axis.

B

y

z

x

A

3 ft

4 ft

T

4ft

Fig. P2.56

- 2.57 The forces P and Q act on the handles of the wrench. If P = 32lb and Q = 36lb, determine the combined moment of the two forces about the z-axis.

z

15in.

###### P

z

30°

15in.

B

25°

###### Q

D

18 in.

C

y

0.54 m

P

0.42m

0.81 m

A x

x y

###### Fig. P2.57 Fig. P2.58

- 2.58 The magnitude of the force P is 480N. Determine the moment of P about the axis CD. Express the result in vector form.
- 2.59 The combined moment of P and the 20-lb force about the axis GB is zero. Determine the magnitude of P.

y

z

x

G

H

D

B

F

E

12 in.

4 in.

O

20 lb

P

A

4in.

Fig. P2.59

- 2.60 Determine the magnitude of the force F given that its moment about the axis BC is 150 lb · ft.

z

4 ft

B

5ft

C

1 ft

A

y

F

2ft

3 ft 3 ft D

x

###### Fig. P2.60

z

∗2.61 Given that F =250 N, determine the moment of F about the axis that is

perpendicular to the plane ABC and passes through point O. Express your answer in vector form.

B

- 2.62 Calculate the moment of the force P about the axis AD using (a) point A as the moment center; and (b) point D as the moment center.

A

y

z

x

3ft

D

O E

B

C

P = 240 lb 2 ft

8 ft

6 ft

5 ft

z

O

x

A

y

P = 1200 lb

Q = 800 lb

4ft

6ft

4ft

Fig. P2.62 Fig. P2.63

- 2.63 Calculate the combined moment of the two forces about the axis OA, using (a) the vector method; and (b) the scalar method (use trigonometry to ﬁnd the moment arm of each force about the axis OA).
- 2.64 The force F= F(0.6i + 0.8j) kN is applied to the frame at the

F

4 m

3 m

y

O A

3m

C

x

Fig. P2.61

z

A 1.6 m

B

1.2 m

D

###### F

point D (0,0, zD). If the moment of F about the axis BC is zero, determine the coordinate zD.

y

O

zD

- 2.65 Determine the combined moment of the four forces acting on the pulleys about the axis AB (points A and B are the centers of the pulleys).

0.8 m

0.5 m

60 kN

40 kN

20 kN

20 kN

3m

z

y

x

4m

A

B

Fig. P2.65

- 2.66 The ﬂexible shaft AB of the wrench is bent into a horizontal arc with a radius of 24 in. The two 20-lb forces, which are parallel to the z-axis, are applied to the handle CD, as shown. Determine the combined moment of the two 20-lb forces about the x-axis (the axis of the socket at point B).

1.2 m

1.0 m C

x

Fig. P2.64

z

z

B

B

y

x

24-in.radius

6 ft

###### F

A 30°

C

O

D

10 ft

40°

6 in. 6 in.

20 lb 20 lb

8ft

A y

x

4ft

Fig. P2.66 2.67 The magnitude of the force F is 120lb. Find the moment of F about the

Fig. P2.67 axis AB using (a) the vector method, and (b) the scalar method.

###### 2.7 Couples

As pointed out before, a force has two effects on a rigid body: translation due to the force itself and rotation due to the moment of the force. A couple, on the other hand, is a purely rotational effect—it has a moment but no resultant force. Couples play an important role in the analysis of force systems.

###### a. Deﬁnition

Two parallel, noncollinear forces that are equal in magnitude and opposite in direction are known as a couple.

A typical couple is shown in Fig. 2.14. The two forces of equal magnitude F F

are oppositely directed along lines of action that are separated by the perpendicular distance d. (In a vector description of the forces, one of the forces would be labeled F and the other −F.) The lines of action of the two forces determine a plane that we call the plane of the couple. The two forces that form a couple have some interesting properties, which will become apparent when we calculate their combined moment about a point.

a d O

F

Plane of the couple

Fig. 2.14

###### b. Moment of a couple about a point

The moment of a couple about a point is the sum of the moments of the two forces that form the couple. When calculating the moment of a couple about a point, either the scalar method (force times perpendicular distance) or the vector method (r × F) may be used. For illustrative purposes, we will calculate the moment of a couple using both methods. Using two methods of analysis to determine the same quantity may appear redundant, but it is instructive because each method emphasizes different characteristics of a couple.

Scalar Calculation Let us calculate the moment of the couple shown in Fig. 2.14 about the point O. Note that O is an arbitrary point in the plane of

the couple and that it is located a distance a from the force on the left. The sum of the moments about point O for the two forces is

+ MO = F(a + d) − F(a)= Fd (2.17)

Observe that the moment of the couple about point O is independent of the location of O, because the result is independent of the distance a.

From the foregoing discussion, we see that a couple possesses two important characteristics: (1) A couple has no resultant force ( F=0), and (2) the moment of a couple is the same about any point in the plane of the couple.

Vector Calculation When the two forces that form the couple are expressed as vectors, they can be denoted by F and −F, as shown in Fig. 2.15. The points labeled in the ﬁgure are A, any point on the line of action of F; B, any point on the line of action of −F; and O, an arbitrary point in space (not necessarily lying in the plane of the couple). The vectors rOA and rOB are drawn from point O to points A and B, respectively. The vector rBA connects points B and A. Using the cross product to evaluate the moment of the couple about point O, we get

MO =[rO A × F] + [rOB × (−F)]=(rOA − rOB) × F

d

rBA A B

–F

F

Plane of the couple

rOA

rOB

O

###### Fig. 2.15

Since rOA − rOB =rBA, the moment of the couple about point O reduces to

MO =rBA × F (2.18)

which conﬁrms that the moment of the couple about point O is independent of the location of O. Although the choice of point O determines rOA and rOB, neither of these vectors appear in Eq. (2.18). Thus we conclude the following:

The moment of a couple is the same about every point.

In other words, the moment of a couple is a free vector. (Recall that, in the scalar calculation, point O was restricted to points in the plane of the couple. We see now that this restriction is unnecessary; that is, O can be any point in space.) In contrast, the moment of a force about a point (the moment center) is a ﬁxed vector, because the moment depends on the location of the moment center.

###### c. Equivalent couples

Because a couple has no resultant force, its only effect on a rigid body is its moment. For this reason, two couples that have the same moment are said to be equivalent (have the same effect on a rigid body). Figure 2.16 illustrates the four operations that may be performed on a couple without changing its moment; all couples shown in the ﬁgure are equivalent. The operations are

- 1. Changing the magnitude F of each force and the perpendicular distance d while keeping the product Fd constant
- 2. Rotating the couple in its plane
- 3. Moving the couple to a parallel position in its plane
- 4. Moving the couple to a parallel plane

y

y

y

200 lb

100 lb

100 lb

x

2 ft

x

x

2 ft

1 ft

100 lb

200 lb

100 lb

(a) Original 200 lb . ft counterclockwise couple

(c) Rotate original couple in its plane

(b) Change F and d, but keep Fd = 200 lb.ft

y

###### y

|2 ft<br><br>100 lb<br><br>100 lb|
|---|

x

100 lb

x 1 ft

2 ft

100 lb

(e) Move original couple to a parallel plane

(d) Move original couple to a parallel position in its plane

###### Fig. 2.16

###### d. Notation and terminology

Consider the couple shown in Fig. 2.17(a). The moment of this couple, shown in Fig. 2.17(b), has a magnitude of C = 1800N·m and is directed counterclockwise in the xy-plane. Because the only rigid-body effect of a couple is its moment, the representations in Figs. 2.17(a) and (b) are equivalent. That is, we can replace

y

y

y

| |C = 1800 N· m|
|---|---|
|O| |

600 N

2 m O

3 m

O x

x

x

C = 1800k N· m

600 N

z

(a) Couple (b) Moment of the couple, commonly called the couple

(c) Vector representation of the couple, known as the couple-vector

###### Fig. 2.17

a couple that acts on a rigid body by its moment without changing the external effect on the body. This equivalence also applies to the terminology—rather than referring to C as the moment of the couple, it usually is called simply the couple.

Figure 2.17(c) shows the same couple (strictly speaking, the moment of the couple) as a vector, which we call the couple-vector. The couple-vector is perpendicular to the plane of the couple, and its direction is determined by the right-hand rule. The choice of point O for the location of the couple-vector was arbitrary. Being a free vector, the couple-vector could be placed anywhere in the ﬁgure.

We will use the scalar and vector representations in Figs. 2.17(b) and (c) interchangeably, choosing the one that is more convenient for the problem at hand.

###### e. The addition and resolution of couples

Because couples are vectors, they may be added by the usual rules of vector addition. Being free vectors, the requirement that the couples to be added must have a common point of application does not apply. This is in contrast to the addition of forces, which can be added only if they are concurrent. Concurrency is also required for the addition of moments of forces about points, because these are ﬁxed to a moment center. It follows that we must be careful when representing moments of forces and couples as vectors—it is easy to confuse these two concepts. To minimize the possibility of confusion, we will use M to denote moments of forces and reserve C for couples.

The resolution of couples is no different than the resolution of moments of forces. For example, the moment of a couple C about an axis AB can be computed from Eq. (2.11) by replacing MO with C:

MAB =C·λ (2.19)

where λ is the unit vector in the direction of the axis. Note that the subscript O, which indicated that the moment must be taken about point O lying on the axis AB, is no longer present in Eq. (2.19). The reason is, of course, that the moment of C is the same about every point. As in the case of moments of forces, MAB is equal to the rectangular component of C in the direction of AB, and is a measure of the tendency of C to rotate a body about the axis AB.

|Sample Problem 2.7<br><br>For the couple shown in Fig. (a), determine (1) the corresponding couple-vector;<br><br>100 kN<br><br>100 kN<br><br>z<br><br>y<br><br>x<br><br>300mm<br><br>E<br><br>D 600mm<br><br>400 mm B<br><br>G<br><br>H A<br><br>(a)<br><br>300 mm<br><br>and (2) the moment of the couple about the axis GH.<br><br>Solution<br><br>Part 1<br><br>One method for determining the couple-vector is to multiply the magnitude of the couple by the unit vector in its direction. The magnitude of the couple is<br><br>Fd =100(0.6)=60 kN · m<br><br>The sense of the couple is shown in Fig. (b)—counterclockwise looking down on the plane of the couple. Letting λ be the unit vector perpendicular to the plane of the couple, as shown in Fig. (c), the couple-vector C may be written as C=60λ kN · m. Because λ is perpendicular to the line AB, it can be seen that λ=(3j + 4k)/5 (recalling that perpendicular lines have negative reciprocal slopes). Therefore, the couple-vector is<br><br>C=60λ=60<br><br>3j + 4k 5 =36j + 48k kN · m Answer<br><br>z<br><br>y<br><br>x<br><br>(b)<br><br>C = 60 kN.m<br><br>z<br><br>y<br><br>x<br><br>(c)<br><br>4<br><br>λ<br><br>3<br><br>C = 60λ kN·m<br><br>Alternative Solution Because the couple-vector is equal to the moment of the couple about any point, it can also be determined by adding the moments of the two forces forming the couple about any convenient point, such as point B. Letting F be the 100-kN force that acts along the line DE, we have<br><br>F = 100λDE =100<br><br>−DE→ |<br><br>−DE→|<br><br>=100 −0.4j + 0.3k<br><br>0.5<br><br>= −80j + 60k kN|
|---|

|Equating C to the moment of F about point B (the other force of the couple passes through B), we obtain<br><br>C = rBD × F=<br><br>i j k −0.6 0 0<br><br>0 −80 60<br><br>= 36j + 48k kN · m<br><br>which agrees with the answer determined previously.<br><br>In this solution, the choice of point B as the moment center was arbitrary. Because the moment of a couple is the same about every point, the same result would have been obtained no matter which point had been chosen as the moment center.<br><br>Part 2<br><br>The most direct method for determining the moment of the couple about the axis GH is MGH =C·λGH. Because C has already been computed, all we need to do is compute the unit vector λGH and evaluate the dot product. Referring to Fig. (a), we have<br><br>λGH =<br><br>−GH→ |<br><br>−GH→|<br><br>=<br><br>−0.3i + 0.3k<br><br>0.3√2 = − 0.7071i + 0.7071k Hence the moment of the couple about axis GH is<br><br>MGH =C·λGH = (36j + 48k)·(−0.7071i + 0.7071k)<br><br>= +33.9 kN · m Answer The result is illustrated in Fig. (d). If you need help in interpreting the positive<br><br>z<br><br>y<br><br>H<br><br>G x<br><br>33.9kN.m<br><br>(d) sign in the answer, you should refer back to Fig. 2.9.<br><br>Sample Problem 2.8<br><br>The ﬂat plate shown in Fig. (a) is acted on by the three couples. Replace the three couples with (1) a couple-vector; (2) two forces, one acting along the line OP<br><br>350 lb·in. 4 in.<br><br>4 in.<br><br>D B E<br><br>G<br><br>H<br><br>P<br><br>1 in.<br><br>3 in.<br><br>2 in.<br><br><br>150 lb<br><br>150 lb<br><br>x<br><br>y<br><br>3 in. 5 in.<br><br>60 lb 60 lb<br><br>O<br><br>(a)<br><br>θ = 30° A|
|---|

|and the other acting at point A; and (3) the smallest pair of forces, with one force acting at point O and the other at point A.<br><br>Solution<br><br>Part 1<br><br>The magnitudes (Fd) and senses of the couples, all of which lie in the xy-plane, are listed below.<br><br>• Couple at H: 350lb · in. clockwise.<br>• Couple acting on GE: (150)(3)=450 lb · in. counterclockwise.<br>• Couple acting on DB: (60)(5)=300 lb · in. clockwise.<br><br><br>Because all three couples lie in the same plane, they can be added algebraically, their sum being the resultant couple CR. Choosing the counterclockwise sense as positive, we get<br><br>+ CR = − 350 + 450 − 300= − 200 lb · in.<br><br>The negative sign shows that the sense of CR is clockwise. Therefore, the corresponding couple-vector CR is, according to the right-hand rule, in the negative z-direction. It follows that<br><br>CR = − 200k lb · in. Answer<br><br>Note that more dimensions are given in Fig. (a) than are needed for the solution. The only relevant dimensions are the distances between the 60-lb forces (5 in.) and the 150-lb forces (3 in.).<br><br>Part 2<br><br>Two forces that are equivalent to the three couples shown in Fig. (a) must, of course, form a couple. The problem states that one of the forces acts along the line OP and the other acts at point A.<br><br>Because the two forces that form a couple must have parallel lines of action, the line of action of the force at point A must also be parallel to OP. From Fig. (b), we see that the perpendicular distance d between the lines of action of the two forces is d =8sin30◦ =4 in. Having already determined that the magnitude of the resultant couple is 200 lb · in., the magnitudes of the forces that form the couple are given by CR/d =200/4=50 lb. The sense of each force must be consistent with the clockwise sense of CR. The ﬁnal result is shown in Fig. (b).<br><br>(b)<br><br>30°<br><br>O<br><br>8 in.<br><br>d<br><br>=4in.<br><br>50 lb<br><br>50 lb<br><br>A θ = 30°<br><br>Answer|
|---|

|Part 3<br><br>Here we are to determine the smallest two forces acting at points O and A that are equivalent to the three couples shown in Fig. (a). Therefore, the two forces to be determined must form a couple that is equivalent to the resultant couple (200 lb · in., clockwise).<br><br>The magnitude of a couple (Fd) equals the product of the magnitude of the forces that form the couple (F) and the perpendicular distance (d) between the forces. For a couple of given magnitude, the smallest forces will be obtained when the perpendicular distance d is as large as possible. From Fig. (b) it can be seen that for forces acting at points O and A, the largest d will correspond to θ =90◦, giving d =8 in. Therefore, the magnitudes of the smallest forces are given by CR/d =200/8=25 lb. These results are shown in Fig. (c), where again note should be taken of the senses of the forces.<br><br>(c)<br><br>O<br><br>8 in.<br><br>25 lb 25 lb<br><br>A<br><br>Answer<br><br>Sample Problem 2.9<br><br>D 0.4 m z A section of a piping system is acted on by the three couples shown in Fig. (a).<br><br>C2<br><br>C3<br><br>0.5 m<br><br>y<br><br>0.6 m<br><br>0.2m<br><br>0.3 m<br><br>x<br><br>B<br><br>A<br><br>O<br><br>(a)<br><br>0.7m<br><br>C1<br><br><br>Determine the magnitude of the resultant couple-vector CR and its direction cosines, given that the magnitudes of the applied couples are C1 =50 N · m, C2 =90 N · m, and C3 =140 N · m.<br><br>Solution<br><br>Applying the right-hand rule to each of the three couples in Fig. (a), we see that the corresponding couple-vectors will be directed as follows: C1, from point D toward point O; C2, from point O toward point B; and C3, from point A toward point B. Because these couple-vectors do not have the same directions, the most practical method of determining their resultant is to use the vector equation<br><br>CR =C1 + C2 + C3<br><br>Using the three unit vectors shown in Fig. (b), the couple-vectors C1, C2, and C3 can be written as<br><br>C1 = C1 λDO =50<br><br>−DO→ |<br><br>−DO→|<br><br>=50<br><br>0.4j − 0.5k 0.6403<br><br>= 31.24j − 39.04k N · m|
|---|

|C2 = C2 λOB =90i N · m<br>C3 = C3 λAB =140<br><br><br>−AB→ |<br><br>−AB→|<br><br>=140 −0.2i − 0.3j + 0.6k<br><br>0.7000<br><br>= −40i − 60j + 120k N · m<br><br>Adding these three couple-vectors gives<br><br>z D<br><br>0.5 m<br><br>y<br><br>0.2 m 0.3 m<br><br>x<br><br>B<br><br>A<br><br>O<br><br>(b)<br><br>0.6 m<br><br>0.4 m<br><br>λDO<br><br>λOB<br><br>λAB<br><br>CR =50i − 28.76j + 80.96k N · m<br><br>The magnitude of CR is<br><br>CR = (50)2 + (−28.76)2 + (80.96)2 =99.41 N · m Answer<br><br>and the direction cosines of CR are the components of the unit vector λ directed along CR:<br><br>λx =<br><br>50 99.41 =0.503 λy = −<br><br>28.76 99.41 = −0.289 λz =<br><br>80.96 99.41 =0.814 Answer<br><br>The resultant couple-vector is shown in Fig. (c). Although CR is shown at point O, it must be remembered that couples are free vectors, so that CR could be shown acting anywhere.<br><br>(c)<br><br>z<br><br>y<br><br>x<br><br>O<br><br>80.96 N· m<br><br>CR<br><br>50 N· m<br><br>28.76 N· m<br><br>The couple-vector CR can be represented as two equal and opposite parallel forces. However, because the two forces will lie in a plane perpendicular to the couple-vector, in this case a skewed plane, this representation is inconvenient here.<br><br>In general, given two forces that form a couple, the corresponding couplevector is easily determined (e.g., by summing the moments of the two forces about any point). However, given a couple-vector, it is not always convenient (or even desirable) to determine two equivalent forces.|
|---|

![image 13](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile13.png>)

###### Problems

###### 2.68 Which of the systems are equivalent to the couple in (a)?

10 N

0.3 m 0.2 m

0.6 m

15 N

0.4 m

6 N.m

15 N

10 N

(a)

(b) (c)

5 N

|N|7.5| |
|---|---|---|
| | | |
| | | |

N

9 N.m 3 N.m

|6 N.m|
|---|

7.5

5 N

(e)

(d)

(f)

5 N

5 N

|0.3 m| |
|---|---|
| | |
| | |

22.5 N

4 N.m

3 N.m

6 N.m

3 N.m

22.5 N

5 N.m

5 N

5 N

(g)

(i)

(h)

###### Fig. P2.68

###### 2.69 Which of the systems are equivalent to the couple in (a)?

60 lb

60 lb

3 ft

5ft

75 lb

75 lb

4 ft

(a) (b)

75 lb

100 lb

75 lb

100 lb

(c)

(d)

50 lb

75 lb

45 lb

45 lb

45 lb

45 lb

75 lb

50 lb

(f)

(e)

Fig. P2.69

###### 2.70 Replace the two couples shown by a single equivalent couple.

45°

75 lb

1.5ft

75 lb

45°

0.6 ft

60 lb·ft

###### Fig. P2.70

45 lb 2.71 Determine the vector representation of the couple shown. A

60° 3 ft

2.72 Determine the magnitude of the single couple that is equivalent to the two

| |
|---|

y

couples shown. 2.73 Calculate the combined moment of the couple C and the force P about the axis AB. Use C =80 N · m and P =400 N.

1.8 ft

x

B

60°

45 lb

z

Fig. P2.71

###### z

C2

3in.

P

z

B

C

60 lb

5 ft

6 in.

3 in.

2ft

D

400 mm

400mm

C3

60 lb

y

3 ft

y

9in.

O y

2 in.

C1

300 mm

A

7 in.

x

30 lb 30 lb

x

x

Fig. P2.72

###### Fig. P2.73 Fig. P2.74

∗2.74 Determine the couple-vector that is equivalent to the three couples acting on the gear box, given that C1 =200 lb·in., C2 =140 lb·in., and C3 =220 lb·in.

z 2.75 The two forces of magnitude F = 24kN form a couple. Determine the

corresponding couple-vector.

0.9m

- 2.76 The couple acts on the handles of a steering mechanism. In the position shown, the moment applied by the couple about the z-axis is zero. Determine the distance b. Use F = 200i − 110j − 80k kN.

z

180mm

b

y B

A

x

F

–F

80 lb

24in.

50 lb

30 lb

500 lb⋅in

16 in.

C

B

A

z

x y

Fig. P2.76 Fig. P2.77

- 2.77 The force-couple system shown can be replaced by a single equivalent couple CR. Determine CR.

F

B

A

–F

1.2 m 0.9m

x y

Fig. P2.75

- 2.78 A couple of magnitude 360 lb · ft is applied about portion AB of the drive shaft (the drive shaft is connected by universal joints at points B and C). Compute the moment of the applied couple about the portion CD when the drive shaft is in the position shown.

x

y

40°

30°

z

D

B

A

Plane of ABC

Plane of BCD 30°

30°

C

360 lb.ft

Fig. P2.78

- 2.79 The arm ABCD of the industrial robot lies in a vertical plane that is inclined at 40◦ to the yz-plane. The arm CD makes an angle of 30◦ with the vertical. A socket wrench attached at point D applies a 52-lb · ft couple about the arm CD, directed as shown. (a) Find the couple-vector that represents the given couple. (b) Determine the moment of the couple about the z-axis.

z

O

x

y

C

D

40°

30°

52 lb .ft

A

B

4.2 ft

2.8ft

Fig. P2.79

- 2.80 The ﬁgure shows one-half of a universal coupling known as the Hooke’s

C0

z

2in.

|P|R|
|---|---|
| |P|

R

6 in

30°

x

y

joint. The coupling is acted on by the three couples shown: (a) the input couple consisting of forces of magnitude P, (b) the output couple C0, and (c) the couple formed by bearing reactions of magnitude R. If the resultant of these couples is zero, compute R and C0 for P =600 lb.

Fig. P2.80

2.81 The steering column of the rack-and-pinion steering mechanism lies in the xz-plane. The tube AB of the steering gear is attached to the automobile chassis at A and B. When the steering wheel is turned, the assembly is subjected to the four couples shown: the 3-N·m couple applied by the driver to the steering wheel, two 1.8-N · m couples (one at each wheel), and the couple formed by the two forces of magnitude F acting at A and B. If the resultant couple acting on the steering mechanism is zero, determine F and the angle θ (the magnitude and direction of the bearing reactions).

z

3 N· m

360 mm

25°

F

θ

A

45°

B

F

1.8 N· m

θ

x y

1.8 N· m

###### Fig. P2.81

###### 2.8 Changing the Line of Action of a Force

In this article we show how to change the line of action of a force without affecting its external effect on a rigid body. This topic lays the foundation for the next chapter, in which we discuss the resultants of force systems.

Referring to Fig. 2.18(a), consider the problem of moving the force of magnitude F from point B to point A. We cannot simply move the force to A, because this would change its line of action, thereby altering the rotational effect (the

Plane of A and F Couple

F

F

F

|A<br><br>F<br><br>B|
|---|

A

A

A

F

F

CT = Fd

F

F

B

B

d B

(a) Original force (c) Identify the couple (d) Equivalent force-couple system

(b) Introduce equal and opposite forces at A

###### Fig. P2.18

###### 2.8 Changing the Line of Action of a Force 87

moment) of the force. We can, however, counteract this change by introducing a couple that restores the rotational effect to its original state. The construction for determining this couple is illustrated in Fig. 2.18. It consists of the following two steps:

- • Introduce two equal and opposite forces of magnitude F at point A, as shown in Fig. 2.18(b). These forces are parallel to the original force at B. Because the forces at A have no net external effect on a rigid body, the force systems in Figs. 2.18(a) and (b) are equivalent.
- • Identify the two forces that form a couple, as has been done in Fig. 2.18(c). The magnitude of this couple is CT = Fd, where d is the distance between the lines of action of the forces at A and B. The third force and CT thus constitute the force-couple system shown in Fig. 2.18(d), which is equivalent to the original force in Fig. 2.18(a).

We refer to the couple CT as the couple of transfer, because it is the couple that must be introduced when a force is transferred from one line of action to another. From the construction in Fig. 2.18 we note the following:

The couple of transfer is equal to the moment of the original force (acting at B) about the transfer point A.

A

F r

In vector terminology, the line of action of a force F can be changed to a parallel line, provided that we introduce the couple of transfer

B

###### CT =r × F (2.20)

(a) Original force

###### CT = r × F F

where r is the vector drawn from the transfer point A to the point of application B of the original force, as illustrated in Fig. 2.19. It is conventional to show CT

A

acting at the transfer point, as in Fig. 2.19(b), but you must not forget that a couple is a free vector that could be placed anywhere.

According to the properties of the cross product in Eq. (2.20), the couplevector CT is perpendicular to F. Thus a force at a given point can always be replaced by a force at a different point and a couple-vector that is perpendicular to the force. The converse is also true: A force and a couple-vector that are mutually perpendicular can always be reduced to a single, equivalent force by reversing the construction outlined in Figs. 2.18 and 2.19.

B

(b) Equivalent force-couple system

Fig. 2.19

|Sample Problem 2.10<br><br>For the machine part shown in Fig. (a), replace the applied load of 150 kN acting at point A by (1) an equivalent force-couple system with the force acting at point B; and (2) two horizontal forces, one acting at point B and the other acting at point C.<br><br>40 mm 40 mm<br><br>80 mm<br><br>80 mm<br><br>A 150 kN<br><br>B<br>C (a)<br><br><br>Solution<br><br>Part 1<br><br>First we move the 150-kN force to point B, and then we introduce the couple of transfer equal to the moment of the 150-kN force in Fig. (a) about point B, given by<br><br>+ CT = MB = − 150(0.080 + 0.040)= − 18 kN · m<br><br>The negative sign indicates that the sense of the couple is clockwise. The equivalent force-couple system is shown in Fig. (b).<br><br>A<br><br>B<br>C<br><br><br>40 mm 40 mm<br><br>150 kN<br><br>18 kN·m (b)<br><br>Answer<br><br>Part 2<br><br>The 18 kN·m clockwise couple in Fig. (b) can be replaced by two 450-kN forces, one acting at point B and the other at point C, as shown in Fig. (c). (The couple represented by these two forces is 450(0.040)= 18 kN·m in the clockwise direction.) The two forces acting at point B can be added to get the system shown in Fig. (d). This is the answer, because we have replaced the original force with two horizontal forces, one at point B and the other at point C, as required.<br><br>A<br><br>B<br>C<br><br><br>40 mm 40 mm<br><br>450 kN<br><br>150 kN<br><br>450 kN (c)<br><br>A<br><br>40 mm<br><br>B<br>C<br><br><br>600 kN<br><br>(d)<br><br>450 kN<br><br>Answer|
|---|

###### 88

|Sample Problem 2.11<br><br>Replace the force-couple system shown in Fig. (a) with an equivalent force-couple<br><br>y 2 in.<br><br>z<br><br>x<br><br>A<br><br>4in.<br><br>D E<br><br>4 in. B<br><br>O<br><br>F<br><br>C<br><br>(a)<br><br>system, with the force acting at point A, given that F =100 lb and C =120 lb·in.<br><br>Solution<br><br>Moving the given force F from point B to point A requires the introduction of a couple of transfer CT. This couple is then added to the given couple-vector C, thereby obtaining the resultant couple-vector, which we label CR. The couplevector CR and the force F located at point A will then be the required force-couple system.<br><br>Owing to the three-dimensional nature of this problem, it is convenient to use vector methods in the solution. Writing F in vector form, we obtain<br><br>F = 100λBE =100<br><br>−BE→ |<br><br>−BE→|<br><br>=100 −4i + 2k<br><br>4.472<br><br>= −89.44i + 44.72k lb<br><br>The position vector from A to B is rAB =4j−2k in. The couple of transfer is equal to the moment of the given force F about point A, so we have<br><br>CT = MA =rAB × F=<br><br>i j k 0 4 −2<br><br>−89.44 0 44.72<br><br>= 178.9i + 178.9j + 357.8k lb · in.<br><br>Expressing the given couple-vector C shown in Fig. (a) in vector form,<br><br>C = 120λDB =120<br><br>−DB→ |<br><br>−DB→|<br><br>=120<br><br>4i + 4j − 2k 6<br><br>= 80i + 80j − 40k lb · in.<br><br>Adding CT and C (remember that couple-vectors are free vectors), the resultant<br><br>y<br><br>z<br><br>x<br><br>A<br><br>O<br><br>(b)<br><br>2 1<br><br>F = 100 lb 318 lb · in. CR = 485 lb · in.<br><br>259 lb · in. 259 lb · in.<br><br>couple-vector is<br><br>CR =CT + C=258.9i + 258.9j + 317.8k lb · in.<br><br>The magnitude of CR is given by<br><br>CR = (258.9)2 + (258.9)2 + (317.8)2 =485 lb · in.<br><br>The equivalent force-couple system is shown in Fig. (b). Note that the force acts at point A. For convenience of representation, CR is shown at point O, but being a free vector, it could be placed anywhere.|
|---|

###### 89

![image 14](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile14.png>)

###### Problems

2.82 Which of the systems are equivalent to the force-couple system in (a)?

100 N

100 N

100 N 700 N · m

3 m 400 N · m

100 N · m

2 m

2 m

(a)

(c)

(b)

100 N 300 N · m

100 N 600 N · m

200 N

(d)

(e)

(f)

###### Fig. P2.82

- 2.83 A 15-lb force acts at point A on the high-pressure water cock. Replace this force with (a) a force-couple system, the force of which acts at point B; and (b) two horizontal forces, one acting at point B and the other acting at point C.

2.2 in.

6 in.

15 lb

A

- B
- C

|mm| |700 mm P C<br><br>|
|---|---|---|
| | |A<br><br>|
|mm|1200 mm<br><br>B| |
| | | |

200

150

Fig. P2.83 Fig. P2.84

- 2.84 The bracket, which is fastened to a wall by anchor bolts at A and B, is loaded by the force P =120 N and the couple C =140 N·m. Replace P and C with

###### 2.82–2.93 Problems 91

(a) an equivalent force-couple system, the force of which acts at A; and (b) two vertical forces, one acting at A and the other at B.

- 2.85 The three forces shown are equivalent to a 50-kN upward force at A and a

|2 m|3 m 2 m| |
|---|---|---|
| | | |
| | | |

P Q 20 kN

A

Fig. P2.85

170-kN·m counterclockwise couple. Determine P and Q.

- 2.86 Replace the two forces shown by a force-couple system with the force acting at O.

|9 in.|12in.<br><br>30°|
|---|---|
|O| |

50 lb

90 lb

B

x A

y

Fig. P2.86

- 2.87 The ﬁgure shows a schematic of a torsion-bar suspension for an automo-

| | |
|---|---|
|Torsion bar<br><br>| |
| | |

10 in.

20 in. H

V

R

D

H

C

B

A

Fig. P2.87

bile (the torsion bar appears in cross section at A). If the three forces and the couple C = 900lb · ft are equivalent to a upward vertical force R = 1200lb acting at D, determine H and V.

- 2.88 The table can be lifted without tilting by applying the 100-N force at

O

A

y 40 lb

2 ft

90 lb⋅ft 5ft

3ft

z

x

Fig. P2.90

point O, the center of the table. Determine the force-couple system with the force acting at corner A that will produce the same result.

- 2.89 The magnitude of the force F acting at point A on the plate is 160 kN. Determine the equivalent force-couple system with the force acting at point O.

A

y

x

1.2 m

O

1.0m

100 N

z

2 m

2.2m

2 m

x

z

y O B

A F

Fig. P2.88 Fig. P2.89

- 2.90 Replace the force-couple system acting on the pipe with an equivalent force-couple system with the force acting at point O.

∗2.91 (a) Replace the force F= −2800i+1600j+3000k lb acting at end A of the crank handle with a force R acting at O and a couple-vector CR. (b) Resolve R into the normal component P (normal to the cross section of the shaft) and the shear component V (in the plane of the cross section). (c) Resolve CR into the twisting component T and the bending component M.

z

10in.

O

y

x

4 in. F

5in.

A

###### Fig. P2.91

C

###### 2.92 Determine the force-couple system, with the force acting at point O, that

B

is equivalent to the force and couple acting on the arm CD of the industrial robot. Note that the arm ABCD lies in a vertical plane that is inclined at 40◦ to the yz-plane; the arm CD makes an angle of 30◦ with the vertical.

D

52 lb·ft

A

z 30° 9.8 lb

2.8 ft

2.93 Replace the force and the couple shown by an equivalent force-couple system with the force acting at (a) point B; and (b) point D.

4.2 ft

O

40°

x

z

y

B

Fig. P2.92

0.9 m

1.8m

1.3m

80 N

D

A y

250 N⋅m

x

###### Fig. P2.93

Review of Equations 93

![image 15](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile15.png>)

###### Review of Equations

###### Principle of transmissibility

A force may be moved anywhere along its line of action without changing its external effect on a rigid body.

###### Moment of a force about point O

###### MO = r × F MO = Fd

r = vector from O to any point on the line of action of F d = perpendicular distance between O and the line of action of F

###### Moment of force F about axis AB

###### MAB = r × F·λ = MO ·λ

r = vector from any point on AB to any point on the line of action of F λ = unit vector directed from A toward B O = any point on AB

###### Changing the line of action of a force

A force F acting at point A is equivalent to F acting at point B plus the couple of transfer

CT = r × F r = vector from A to B

![image 16](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile16.png>)

###### Review Problems

- 2.94 The moment of the force P about the axis AB is 600 lb · ft. Determine the magnitude of P.

x

A

B

O

C

y

z

30° 20°

8ft

P

8ft

8ft

Fig. P2.94

- 2.95 Replace the force and the couple shown with an equivalent force-couple system where the force acts at A.

6 m

6m

8m

D x

A B

32 kN 180 kN⋅m

E

z

y 4m

Fig. P2.95

- 2.96 Three cable tensions T1, T2, and T3 act at the top of the ﬂagpole. Given

z

A

T1

T3

that the resultant force for the three tensions is R= −400k N, ﬁnd the magnitudes of the cable tensions.

T2

12 m

2.97 The force acting at A is F = 10i + 20j − 5kkN. Knowing that the moment of this force about the y-axis is 8jkN·m, determine the distance b and the moment of F about point O.

3 m

D

4 m

B

y

10 m O

z

6m

A

C

O F

x

300mm

Fig. P2.96

x

250mm

y b

###### Fig. P2.97

###### 2.94–2.108 Review Problems 95

- 2.98 The magnitude of the moment of the force P about the axis CD is 50 lb·in.

3in.

3in.

B

5 in. P

2 in. 2 in. A

z

y

x

C

D

Fig. P2.98

Find the magnitude of P.

- 2.99 The three couples in (a) are equivalent to the couple shown in (b), where F = 160i + 120jN. Determine the distance b.

0.5 m

0.5 m

160 N 400 N⋅m

120 N⋅m

| | | | |160|
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

N

(a) (b)

y

x –F

F

|b| | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Fig. P2.99

- 2.100 The magnitudes of the force P and couple C are 500 lb and 1200 lb · ft, respectively. Calculate the combined moment of P and C about (a) the origin O; and (b) the axis OF.

y

x

z

C

P

B E

A

O

F

12 ft

4 ft

3ft

| | |
|---|---|
| | |

y

x

30° 45°

T3 T2

T1

Fig. P2.100 Fig. P2.101

- 2.101 The resultant force of the three cable tensions that support the crate is R=500j lb. Find T1 and T3, given that T2 =300 lb.
- 2.102 A force system consists of the force F=200i+100j+250k lb, acting at the origin of a rectangular coordinate system, and a couple C=−400i + 300j + 200k lb · in. (a) Show that F and C can be reduced to a single force. (b) Find the coordinates of the point in the xy-plane where the combined moment of F and C is zero.
- 2.103 Replace the two forces shown with an equivalent force-couple system

30 kN

50 kN

4m

B

y A

x

z

O

2m

Fig. P2.103

with the force acting at O.

- 2.104 The three forces of magnitude P can be replaced by a single, equiva-

P

|L<br><br>A|L 2<br><br>|
|---|---|
| | |

P

L 2

x

P

lent force R acting at point A. Determine the distance x and the magnitude and direction of R.

Fig. P2.104

- 2.105 Knowing that the two forces shown can be replaced by an equivalent force acting at O (no couple), determine P.

O

P

4

3

5

12

260 lb

30°

60°

5in.

4in.

z

y

C

T1

T2

A

B

x

20°

5ft

2ft

4 ft

3ft

Fig. P2.105 Fig. P2.106

- 2.106 The trapdoor is held in the position shown by two cables. The tensions

z

E

in the cables are T1 =30 lb and T2 =90 lb. Determine the magnitude of the single force that would have the same effect on the door as the cable tensions.

C

- 3ft
- 4 ft

B 2.107 The force system consists of the force P= − 300i + 200j + 150k lb and

P y

the couple C. Determine the magnitude of C if the moment of this force system about the axis DE is 800 lb · ft.

3ft

D A

2.108 The force system shown can be replaced with a single, equivalent couple CR. Determine CR.

x

Fig. P2.107

z

400 N

B

200

400 N

A

300

O

400

x

D

300 N

y

400

500 N

E

200 N

Dimensions in mm

###### Fig. P2.108

# 3

### Resultants of Force Systems

![image 17](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile17.png>)

Strong winds result in signiﬁcant loads on high-rise buildings. If the pressure distribution is known, the resultant force of the wind and the location of the corresponding pressure center can be computed using the principles of statics—see Problem P3.52. Visions of America/Joe Sohm/Digital Vision/Getty Images

###### 3.1 Introduction

In order to investigate the effects of a system of forces on a body, it is often convenient to reduce the force system to its simplest equivalent representation. Some of these simpliﬁcations have been discussed in the preceding chapter. For example, you have learned that a system of concurrent forces can be replaced by a single force and that a system of couples can be replaced by a single couple.

The next article explains how an arbitrary force system can be reduced to a force and a couple. Subsequent articles discuss applications of the force-couple system to the determination of the resultants of force systems.

3.2 Reduction of a Force System to a Force

and a Couple

Here we show how a system of forces can be reduced to an equivalent system consisting of a force acting at an arbitrary point, plus a couple.

###### 97

98 CHAPTER 3 Resultants of Force Systems

F2

F1

F3 r2

R

###### F2

###### F2

###### =

###### =

F1

F3 O

F3 O

r1 r3 O

O C

O

C3T

C3T

CR

###### CT

C1T

C2T

(a) (b)

(c)

Fig. 3.1

Consider the force system shown in Fig. 3.1(a), consisting of the forces F1, F2, F3,.... The position vectors r1, r2, r3,...of the points where the forces act are measured from an arbitrarily chosen base point O. We can reduce this force system to an equivalent force-couple system, with the force acting at O, by the following procedure:

- • Move each force to point O. As explained in Art. 2.8, the force F1 can be

moved to O if we introduce the couple of transfer C1T =r1 × F1 (the moment of F1 about O). The forces F2, F3, ... can be moved in the same manner, their couples of transfer being C2T =r2×F2, C3T =r3×F3, . . . . After all the forces have been moved, we end up with the force system in Fig 3.1(b), which is equivalent to the original system. (The equal signs between the ﬁgures signify equivalence.)

- • Because the forces are now concurrent at point O, they can be added to yield the resultant force R:

###### R=F1 + F2 + F3 + ··· = F (3.1)

The couples of transfer can also be added, their sum being the resultant couple-vector CR:

###### CR =r1 × F1 + r2 × F2 + r3 × F3 + ··· = MO (3.2)

The resultant force-couple system is displayed in Fig. 3.1(c), with both R and CR shown acting at point O. It should be noted, however, that R is a sliding vector (its line of action must pass through O), whereas CR is a free vector. Although C1T is perpendicular to F1, and so on, as pointed out in Art. 2.8, CR is generally not perpendicular to R.

###### 3.2 Reduction of a Force System to a Force and a Couple 99

Using Eqs. (3.1) and (3.2), any force system can be reduced to an equivalent force-couple system, with the force acting at a reference point of your choosing. The resultant force R is simply the vector sum of all the forces—therefore, it is not affected by the location of the reference point. However, the resultant couplevector CR, being the sum of the moments of all the forces about the reference point,* does depend on the choice of the reference point.

If we choose the reference point O be the origin of a rectangular coordinate system, the two vector equations in Eqs. (3.1) and (3.2) are equivalent to the following six scalar equations:

Rx = Fx Ry = Fy Rz = Fz CxR = Mx CyR = My CzR = Mz

(3.3)

If the forces of the original system lie in a plane—say, the xy-plane—the following three scalar equations are necessary to determine the force-couple system.

###### Rx = Fx Ry = Fy CR = MO (3.4)

The couple-vector CR will always be in the z-direction, because the plane of the couple is the xy-plane. Because the resultant force R lies in the xy-plane, R and CR will be mutually perpendicular. The last observation is signiﬁcant—it implies that a coplanar force system can be further reduced to a single force or a single couple. This topic is discussed in more detail in the next article.

*If the original force system contains couples, their moments must be included in the sum.

|Sample Problem 3.1<br><br>The force system acting on a structural member consists of the couple C and the<br><br>6 ft<br><br>3ft<br>4ft<br><br><br>B<br><br>z<br><br>x<br><br>y<br><br>G<br><br>O C<br><br>A<br><br>F1<br><br>F2<br><br>F3<br><br>forces F1, F2, and F3. Determine the equivalent force-couple system with the force acting at point G. Use C =200lb · ft, F1 =100 lb, F2 =90 lb, and F3 =120 lb.<br><br>Solution<br><br>Because of the three-dimensional nature of this problem, we will use vector algebra to solve it. The ﬁrst step is to express the three forces and the couple in vector form:<br><br>F1 = 100λAB =100<br><br>−AB→ |<br><br>−AB→|<br><br>=100 −4i − 6j + 3k (−4)2 + (−6)2 + 32<br><br>= −51.22i − 76.82j + 38.41k lb<br><br>F2 = 90i lb<br>F3 = 120j lb<br><br><br>C = 200λBG =200<br><br>−BG→ |<br><br>−BG→|<br><br>=200<br><br>4i − 3k 42 + (−3)2<br><br>= 160i − 120k lb · ft<br><br>When we move the forces F1 and F2 to point G, they are concurrent with F3. Adding the three forces, we get for the resultant force<br><br>R = F1 + F2 + F3<br><br>= (−51.22i − 76.82j + 38.41k) + 90i + 120j<br><br>= 38.78i + 43.18j + 38.41k lb Answer<br><br>The couple of transfer that arises from moving F1 and F2 is the moment about G of<br><br>F1 + F2 = (−51.22i − 76.82j + 38.41k) + 90i<br><br>= 38.78i − 76.82j + 38.41k lb<br><br>The resultant couple is the sum of the couple of transfer and the couple C, resulting in<br><br>CR = rGB × (F1 + F2) + C<br><br>=<br><br>i j k −4 3 0 38.78 −76.82 38.41<br><br>+ 160i − 120k<br><br>= 275i + 153.6j + 70.9k lb · ft Answer|
|---|

3ft

###### 100

|Sample Problem 3.2<br><br>The coplanar force system in Fig. (a) consists of three forces and one couple.<br><br>4 3<br><br>800 mm<br><br>400 mm<br><br>300 mm<br><br>y<br><br>x<br><br>90 N<br><br>40 N.m<br><br>100 N<br><br>(a)<br><br>O<br><br>40°<br><br>600mm<br><br>A<br><br>50 N<br><br>500mm<br><br>Determine the equivalent force-couple system with the force acting at point O.<br><br>Solution<br><br>We will solve this problem with scalar algebra; however, the use of vector algebra would be almost as convenient.<br><br>The components of the resultant force R are<br><br>Rx = Fx −→+ Rx = 50cos40◦ + 90 −<br><br>3 5<br><br>(100)=68.30 N<br><br>Ry = Fy +  Ry = 50sin40◦ −<br><br><br>4<br><br>5<br><br><br>(100) = −47.86 N<br><br>Thus the resultant force is<br><br>R=68.3i − 47.9j N Answer<br><br>The magnitude of R is<br><br>R = (68.30)2 + (−47.86)2 =83.4 N<br><br>and the angle that R makes with the x-axis is<br><br>θ = tan−1<br><br>47.86 68.30 =35.0◦<br><br>The force R acting at point O is shown in Fig. (b).<br><br>O<br><br>35°<br><br>68.3 N<br><br>CR= 87.4 N.m<br><br>R = 83.4 N<br><br>47.9 N<br><br>y<br><br>x<br><br>(b)<br><br>The magnitude of the resultant couple equals the magnitude of the total moment about point O of the original force system. Referring to Fig. (a), we have<br><br>CR = MO + CR = 50sin40◦(0.800) − 50cos40◦(0.500)<br><br>− 90(0.600) − 40<br><br>= −87.44 N · m<br><br>Therefore,<br><br>CR =87.4 N · m clockwise Answer The resultant force-couple system is shown in Fig. (b).|
|---|

600mm

500mm

###### 101

![image 18](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile18.png>)

###### Problems

###### 3.1 Determine which of the force systems in (b) through (f) are equivalent to the force-couple system in (a).

10 lb

50 lb.ft

10 lb

|8| |
|---|---|
| | |
| | |

4 ft

lb

- 4 ft

3 ft

- 5 ft

|10 lb|
|---|

50 lb.ft

4 lb

(a)

(b)

(c)

24 lb.ft

10 lb

5 lb

6 lb

|8| |
|---|---|
| | |

lb

80 lb.ft

8 lb

8 lb

4 lb 36 lb.ft

(e)

(f)

(d)

###### Fig. P3.1

- 3.2 Two forces and a couple are applied to the beam in an attempt to lift it. Replace this force system by an equivalent force-couple system with the force acting at (a) point A; and (b) point B.

x

y

A

2 m 3 m

36 kN 20 kN

2 m 94 kN.m C B

b

Fig. P3.2, P3.3

- 3.3 The two forces and a couple acting on the beam are equivalent to a single force acting at C. Determine the distance b that locates point C.

3.2

O

9.5

|3.5|4.5|3.5|
|---|---|---|
| | | |

18 lb 30 lb 46 lb 60 lb

Dimensions in inches 3.4 The four forces shown act on the rollers of an in-line skate. Determine the

equivalent force-couple system, with the force acting at O (the ankle joint of the skater).

Fig. P3.4

###### 3.1–3.15 Problems 103

- 3.5 Replace the three forces with an equivalent force-couple system, with the

150

300

Dimensions in mm

200

200

600 N

400 N

300 N

O

y

x

Fig. P3.5

force acting at O.

- 3.6 The force system acting on the machine part is equivalent to the single force R = 95i + 10jlb acting at O. Determine the force P and the distance b.

8 in.

P

300 lb

60 lb

200 lb

4 in.

30°

O

x

b

y

Fig. P3.6

- 3.7 The three forces are perpendicular to the triangular plate. Find the equivalent force-couple system, with the force acting at O.

50 kN

20 kN

40 kN O

x y

z

3m

4m

Fig. P3.7

- 3.8 Replace the three forces acting on the quarter-circular plate with an equivalent force-couple system with the force at point D. Use P =400lb and θ =40◦.

200 lb

240 lb

A

B O

θ

P

x

y

z

6 ft

6

ft

D

Fig. P3.8, P3.9

- 3.9 When the three forces acting on the quarter-circular plate are replaced by an equivalent force-couple system with the force acting at point D, the resultant couple is zero. Determine P and the angle θ.

###### 3.10 Represent each of the force systems with a force-couple system having the force act at point A. Which systems are equivalent to each other?

z

5 in.

4in.

3 lb

6 lb 2 lb

6 lb

6 lb

###### A

###### A

A

y

3 in.

2 lb

4 lb

6 lb.in.

x

(a)

(c)

(b)

9 lb

2 lb

3 lb

13 lb.in.

1 lb

5 lb

3 lb

###### A A

###### A

4 lb

25 lb.in.

16 lb.in.

3 lb

3 lb (e)

3 lb

(d)

(f)

###### Fig. P3.10

- 3.11 A worker applies the forces P = −10i + 8jlb and Q = 10ilb to the handgrips of the electric drill. These forces are equivalent to the force R = 8jlb acting at the tip of the drill and the couple CR = −120j lb · in. Determine the dimensions a and b.

8in.

CR

R

Q

O

z

x

P y

b

a

Fig. P3.11

- 3.12 Two cable tensions and a couple act on the rod OAB. Determine the equivalent force-couple system with the force acting at O.

###### 3.3 Deﬁnition of Resultant 105

D z

3 m

3m 3m

O

50 kN

A

150 kN.m 20 kN

C

x

B

4m

y

2m

###### Fig. P3.12

- 3.13 Replace the two forces and a couple acting on the bent rod ABC with an

100 N

120 N

2 m

A x

z

B

C

D

y

1.5m

2m

180 N.m

Fig. P3.13

equivalent force-couple system with the force acting at C.

- 3.14 The shaft-and-pulley assembly ABCD is driven by the 32-lb · ft torque (couple) supplied by the electric motor at A. The assembly is also subjected to the two belt tensions shown at each of the two pulleys. Determine the force-couple system at D that is equivalent to the torque and the four belt tensions.

12 lb

26 lb

5

z

x

y

D

A

C

B

12

0.75 ft

32 lb

8 lb

1.0 ft

32 lb.ft

2ft

3ft

1.5ft

Fig. P3.14

- 3.15 Replace the two forces and the couple with an equivalent force-couple

z D

20 N

200

E O

6 N.m

35°

300

A

C

y

14 N

x

250

B

Dimensions in mm

system, with the force acting at A. Note that the 6-N · m couple lies in the plane OCED.

Fig. P3.15

###### 3.3 Deﬁnition of Resultant

The resultant of a force system is deﬁned to be the simplest system that can replace the original system without changing its external effect on a rigid body.

The word simplest is used in the sense that one force is simpler than two forces, one couple is simpler than two couples, a force is simpler than a force and a couple, and so on.

The resultant of a force system is generally a force-couple system R and CR. As explained in Art. 2.8, if R and CR are mutually perpendicular, they can be further reduced to a single force. It follows that the resultant of a force system must be one of the following:*

- • A resultant force R (if CR =0 or if R and CR are perpendicular)
- • A resultant couple-vector CR (if R=0)
- • A resultant force-couple system (if R and CR are not mutually perpendicular)

Force systems that have the same resultant are called statically equivalent. The remainder of this chapter discusses the procedures for determining the

resultants of two- and three-dimensional force systems.

###### 3.4 Resultants of Coplanar Force Systems

This article investigates the resultants of force systems in which all the forces lie in a single plane, chosen as the xy-coordinate plane. We begin with a discussion of the resultants of general coplanar force systems and then consider two special cases: concurrent force systems and parallel force systems.

###### a. General coplanar force system

A general coplanar force system is shown in Fig. 3.2(a), with all the forces lying in the xy-plane. The origin O is located at any convenient point in the plane. The reduction of this force system to its resultant (simplest equivalent force system) is accomplished by the following procedure.

y

y

y

F1

###### R = ΣF

F2

R

###### = =

O O

O F3

x x

x

CR = ΣM d

O

(a) General coplanar force system

(b) Equivalent force-couple system

(c) Resultant is a force (or a couple)

###### Fig. 3.2

*It is important that you pay particular attention to the use of the terms resultant, resultant force R, and resultant couple-vector CR.

###### 3.4 Resultants of Coplanar Force Systems 107

Replace the original force system with the equivalent system consisting of the resultant force R= F (or Rx = Fx and Ry = Fy) acting at O and the resultant couple CR = MO, as shown in Fig. 3.2(b). This procedure has three possible outcomes:

- • R=0. The resultant is the couple CR.
- • CR =0. The resultant is the force R acting through O.
- • R  = 0 and CR  = 0. Because R and CR are perpendicular to each other, the system can be reduced to a single force R acting at a point different from O, as illustrated in Fig. 3.2(c). The perpendicular distance d between O and the line of action of R is determined by the requirement that moments about O of the force systems in Figs. 3.2(b) and (c) must be the same; that is, MO = Rd.

In summary, the resultant of the general coplanar force system shown in Fig. 3.2(a) is either a force or a couple. If F  = 0, then the resultant is a force R determined by

###### Rx = Fx Ry = Fy MO = Rd (3.5)

Note that the moment equation locates the line of action of R. If F=0 and MO  = 0, then the resultant is the couple

CR = MO (3.6)

b. Concurrent, coplanar force system

The resultant of a concurrent, coplanar force system is the force R= F (Rx = Fx, Ry = Fy) acting through the point of concurrency O, as indicated in Fig. 3.3. This conclusion follows from Eq. (3.5): Because MO =0 for a force system that is concurrent at O, the moment equation MO = Rd yields d =0.

y y

R = ΣF

R

F1

|y| |
|---|---|
| |O|

- F2
- F3

###### =

x x

O

Rx

(b) Resultant is a force through point of concurrency

(a) Concurrent, coplanar force system

###### Fig. 3.3

###### c. Parallel, coplanar force system

Figure 3.4(a) shows a coplanar force system, where the forces F1, F2, F3, . . . are parallel to the y-axis. The equivalent force-couple system at point O is shown in Fig. 3.4(b), where

R = F1 + F2 + F3 + ··· = F CR = F1x1 + F2x2 + F3x3 + ··· = MO

y y y

R = ΣF CR = ΣMO x O x x x

F2

R F1

F3

###### = =

O

O

x1

x2

x3

(c) Resultant is a force (or a couple)

(b) Equivalent force-couple system

(a) Parallel, coplanar force system

###### Fig. 3.4

If F  = 0, the resultant is a force R located at the distance x from O, as indicated in Fig. 3.4(c). The value of x is obtained by equating the moments about O in Figs. 3.4(b) and (c):

###### MO = Rx (3.7)

If, on the other hand, F =0 and MO  = 0, then the resultant is the couple CR = MO.

|Sample Problem 3.3<br><br>The values of Rx = Fx, Ry = Fy, and MO for ﬁve force systems lying in the xy-plane are listed in the following table. Point O is the origin of the coordinate system, and positive moments are counterclockwise. Determine the resultant for each force system, and show it on a sketch of the coordinate system.<br><br>Part Rx Ry MO<br><br>1 0 200N 400N · m<br>2 0 200N −400N · m<br>3 300lb 400lb 600lb · ft<br>4 400N −600N −900N · m<br>5 0 0 −200lb · ft<br><br><br>Solution<br><br>Part 1 Rx =0 Ry =200 N MO =400 N · m<br><br>The resultant is a 200-N force that is parallel to the y-axis, as shown in Fig. (a).<br><br>x = 2 m<br><br>y<br><br>x O<br><br>200 N<br><br>(a)<br><br>Letting x be the distance from point O to the line of action of the resultant, as shown in Fig. (a), and using Eq. (3.7), we have<br><br>MO = Rx + 400=200x<br><br>which gives<br><br>x =2 m<br><br>Part 2 Rx =0 Ry =200 N MO = − 400 N · m<br><br>The resultant is the same 200-N force as in Part 1, but here the moment equation gives<br><br>MO = Rx + − 400=200x or<br><br>x = − 2 m The negative sign indicates that x lies to the left of point O, as shown in Fig. (b).<br><br>2 m<br><br>y<br><br>x O<br><br>200 N<br><br>(b)<br><br>Part 3 Rx =300 lb Ry =400 lb MO =600 lb · ft<br><br>The resultant is the force R=300i+400j lb. Its magnitude is R = (300)2 +(400)2 =500 lb. The moment equation of Eqs. (3.5) must be used to<br><br>|
|---|

|determine the line of action of R. Letting d be the perpendicular distance from point O to the line of action of R, as shown in Fig. (c), we have<br><br>MO = Rd + 600=500d which yields<br><br>y<br><br>O<br><br>B<br><br>A<br><br>4 3<br><br>x<br><br>R = 500 lb Ry = 400 lb<br><br>Rx = 300 lb<br><br>x = 1.5 ft<br><br>d<br><br>=1.2ft<br><br>(c)<br><br>d =1.2 ft<br><br>The points where R intersects the coordinate axes can then be determined by trigonometry or by using the principle of moments, as follows.<br><br>y<br><br>O<br><br>B<br><br>A<br><br>x<br><br>R = 500 lb<br><br>Ry = 400 lb<br><br>Rx = 300 lb<br><br>y = 2 ft<br><br>(d)<br><br>With R placed at A, as in Fig. (c): With R placed at B, as in Fig. (d):<br><br>MO = Ryx<br><br>+ 600=400x x =1.5 ft<br><br>MO = Rx y<br><br>+ 600= 300y<br><br>y = 2 ft<br><br>Part 4<br><br>Rx =400 N Ry = − 600 N MO = − 900 N · m The resultant is the force R = 400i − 600j N; its magnitude is R =<br><br>(400)2 + (600)2 = 721.1 N. Letting d be the perpendicular distance from point O to the line of action of R, as shown in Fig. (e), we have<br><br>y<br><br>x O<br><br>(e)<br><br>R = 721.1 N<br><br>6<br><br>4<br><br>d = 1.248 m<br><br>MO = Rd + − 900= − 721.1d<br><br>which gives<br><br>d =1.248 m<br><br>Note that the line of action of R must be placed to the right of the origin, so that its moment about point O has the same sense as MO—that is, clockwise.<br><br>Part 5<br><br>Rx =0 Ry =0 MO = − 200 lb · ft<br><br>Because the sum of the forces is zero, the resultant of this force system is a 200-lb · ft clockwise couple, as shown in Fig. (f).<br><br>y<br><br>x O<br><br>(f)<br><br>200 lb·ft|
|---|

|Sample Problem 3.4<br><br>The force R is the resultant of the other three concurrent forces shown. Determine<br><br>30°<br><br>20°<br><br>80 lb<br><br>y<br><br>P<br><br>R<br><br>x<br><br>100 lb<br><br>O<br><br>P and R.<br><br>Solution<br><br>The three applied forces represent a concurrent, coplanar force system. Therefore, the components of the resultant force are determined by two scalar equations:<br><br>Rx = Fx and Ry = Fy. Because the directions of all the forces are known, there are two unknowns in this problem—the magnitudes P and R. The most direct method for determining these two unknowns is to solve the following two scalar equations (comparing the number of unknowns with the number of available equations is often a valuable aid in the solution of problems):<br><br>Rx = Fx −→+ R cos30◦ = P sin20◦ − 80 (1)<br>Ry = Fy +  R sin30◦ = P cos20◦ − 100 (2)<br><br><br>Solving Eqs. (1) and (2) simultaneously gives<br><br>P =72.5 lb and R = − 63.7 lb<br><br>The positive value of P indicates that P is directed as shown in the ﬁgure. The negative sign associated with R means that R acts in the direction opposite to that shown in the ﬁgure.<br><br>Therefore, the forces P and R are<br><br>20°<br><br>P = 72.5 lb<br><br>30°<br><br>R = 63.7 lb<br><br>Answer<br><br>Of course, the lines of action of P and R pass through O, the point of concurrency.<br><br>Sample Problem 3.5<br><br>Determine the resultant of the coplanar force system shown in Fig. (a) that acts on the arm of an excavator. Show your answer on a sketch of the coordinate system.<br><br>Solution<br><br>For a coplanar force system, the resultant is either a force or a couple. If the resultant is a force, then Eqs. (3.5) provide three scalar equations: Rx = Fx,<br><br>Ry = Fy, and MO = Rd. We see that there are no unknown quantities in the original force system.<br><br><br>Therefore, if the resultant is a force, the three unknowns in this problem will|
|---|

|y<br><br>80 kN 40°<br><br>60 kN<br><br>O<br><br>x O 3 m<br><br>50 kN<br><br>(a)<br><br>37.2°<br><br>R = 14.17 kN d = 2.27 m<br><br>x<br><br>y<br><br>(b)<br><br>3.3 m<br><br>350 kN.m<br><br>be Rx, Ry, and d, which could be determined from the three scalar equations. Referring to Fig. (a), the three equations become<br><br>Rx = Fx −→+ Rx =80cos40◦ − 50=11.284 kN<br><br>This equation is sufﬁcient to tell us that the resultant is a force, not a couple; if the resultant were a couple, Fx would be zero.<br><br>Ry = Fy +  Ry =80sin40◦ − 60= − 8.577 kN MO = Rd + MO =350 − (80 cos40◦)(3.3) − 60(3) = −32.24kN · m<br><br>Therefore, the resultant R is<br><br>8.577 kN R=14.174 kN<br><br>11.284 kN<br><br>θ<br><br>θ = tan−1<br><br>8.577 11.284 =37.2◦<br><br>Because MO is negative (i.e., clockwise), the resultant R must also provide a clockwise moment about O, as shown in Fig. (b). Therefore we obtain<br><br>MO = Rd + 32.24 = 14.174d<br><br>which gives<br><br>d =2.27 m<br><br>The ﬁnal result is shown in Fig. (b).|
|---|

|Sample Problem 3.6<br><br>The force system shown consists of the couple C and four forces. If the resultant of this system is a 500-lb · in. counterclockwise couple, determine P, Q, and C.<br><br>12 5<br><br>20 lb<br><br>80<br><br>|lb| | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
<br><br>l<br><br>O B<br><br>1 in.<br><br>4<br><br>3<br><br>1 in.<br><br>C<br><br>P<br><br>Q<br><br>A<br><br>y<br><br>x<br><br>Solution<br><br>This problem contains three unknowns: P, Q, and C. Because the force system is the general coplanar case, three equations are available to determine the resultant. Since the resultant is a couple, the ﬁrst two of Eqs. (3.5) become<br><br>Rx = Fx =0 −→+ −<br><br>12<br><br>13<br><br><br>Q +<br><br>4<br><br>5<br><br><br>P + 80=0 (a)<br><br>Ry = Fy =0 +  −<br><br><br>5 13<br><br>Q +<br><br>3 5<br><br>P − 20=0 (b)<br><br>Solving Eqs. (a) and (b) simultaneously gives<br><br>P =200 lb and Q =260 lb Answer<br><br>The third equation is Eq. (3.6), CR = MO. Because a couple is a free vector, the moment center can be any point. Given that CR =500 lb·in., counterclockwise, and choosing point A as the moment center, we have<br><br>CR = MA + 500= − 20(3) − C + 80(4) +<br><br>3 5<br><br>P(6) +<br><br>4<br><br>5<br><br><br>P(6)<br><br>Substituting P = 200 lb and solving yields<br><br>C =1440 lb · in. Answer<br><br>Because the values for P, Q, and C are positive, each force acts in the direction shown in the ﬁgure.|
|---|

![image 19](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile19.png>)

###### Problems

y 3.16 Determine the resultant force R and its line of action for the following

force-couple systems:

Fy

Fx

- (a) Fx = 300lb, Fy = 0, and C = −900lb · in.
- (b) Fx = 200N, Fy = −200N, and C = 800N · m
- (c) Fx = −600kN, Fy = −400kN, and C = 0
- (d) Fx = −600lb, Fy = 800lb, and C = −24000lb · ft

x C

O

Fig. P3.16

- 3.17 Determine the resultant of the three forces acting on the gusset plate of a truss.

45° 50°

3800 lb

6200 lb 4000 lb

y

x A

Fig. P3.17

- 3.18 The resultant of the three concurrent forces acting on the eyebolt is the force R=800j lb. Determine the magnitude of the force P and the angle θ that speciﬁes the direction of the 900-lb force.

x

y

3 4

P

500 lb

900 lb

O

θ

| | |
|---|---|

2 m 8 m 4 m 3 m

300 kN 120 kN 200 kN

A

C

B

500 kN

x

Fig. P3.18 Fig. P3.19

- 3.19 The overhead electric hoist C rides along a track on the horizontal beam AB. In addition to the 500-kN vertical force carried by the hoist, the beam also supports the three vertical forces shown. (a) If x =5 m, determine the resultant of the four forces carried by the beam. (b) Determine the distance x for which the resultant of the four forces would act at the center of the span AB.
- 3.20 Knowing that the resultant of the couple and the two forces shown is a

P

3ft

4ft

150 lb

y O

60°

875 lb.ft

x

###### Fig. P3.20 force R acting through point O, determine P and R.

###### 3.16–3.29 Problems 115

- 3.21 Determine which of the force systems in (b) through (f) are equivalent to the 21-kN force in (a).

(f)

6 kN

15 kN

12.6 kN·m

8 kN

6 kN

(e)

21 kN

8 kN

8 kN

(d)

17 kN

10 kN 4

3

15

8

(c)

15 kN

6 kN

189 kN·m

(b)

15 kN 6 kN

(a)

2.1 m

1.5 m

1.575 m

A

21 kN

Fig. P3.21

- 3.22 Determine the resultant of the three forces if (a) θ =30◦; and (b) θ =45◦.

O

500 N

500 N

x

y

500 N

300mm

θ θ

Fig. P3.22

- 3.23 Determine the resultant of the force system acting on the beam.

1000 lb 600 lb

1200 lb

1000 lb

4.5 ft

y

A x

8.2 ft 5.5 ft

12

x

y

O

2.4 m

2.8 m

150 N

4 5 3

80 N C

130 N

Fig. P3.23 Fig. P3.24

- 3.24 Determine the resultant of the three forces and the couple C, and show it on a sketch of the coordinate system if (a) C =0; and (b) C =90N · m.

###### 3.25 The resultant of the three forces is a force R that passes through point B. Determine R and F.

30.5 lb

y

3 ft

1.5 ft

x B

O

200 lb 160 lb

5

F

12

15in.

4 ft

36 lb

12in.

O

Fig. P3.25

C

40 lb

80 lb

###### 3.26 The resultant of the four belt tensions and the couple C is a force R acting

through point O. Determine C and R. 3.27 The resultant of the three forces shown is a counterclockwise couple of

Fig. P3.26

magnitude 150 lb · ft. Calculate the magnitudes of the forces.

C

y

1.0 ft

P1

y

A

300 lb

5ft

A

P3 P2

2m

|2| | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

x

B

1.0 ft

5ft

4 3

P1

y

2m

30°

θ

50 lb

A

x

P2

B

x

O B

P3

P2

P1

Fig. P3.27

###### Fig. P3.28 Fig. P3.29

3.28 The resultant of the three forces is the force R = −170j kN acting through point B. Determine P1, P2, and P3.

∗3.29 The bar AB, which is inclined at the angle θ to the horizontal, is subjected to the four forces shown. Knowing that these forces have no resultant (neither a force nor a couple), determine P1, P2, and θ.

###### 3.5 Resultants of Three-Dimensional Systems

In general, a three-dimensional force system cannot be simpliﬁed beyond a forcecouple system. Exceptions are systems in which the forces are either concurrent or parallel. In this article, we discuss these two special cases, together with a special form of the force-couple system called the wrench.

###### a. Concurrent, three-dimensional force system

A concurrent, three-dimensional force system is shown in Fig. 3.5(a). As in the case of concurrent, coplanar forces, this system can be reduced to the resultant force R= F (Rx = Fx, Ry = Fy, Rz = Fz) acting through the point of concurrency O, as indicated in Fig. 3.5(b).

z

z

F1

Rz

F2

###### =

R = ΣF

Ry

###### O

y O

y

F3

Rx

x

x

(a) Concurrent, three-dimensional force system

(b) Resultant is a force through the point of concurrency

###### Fig. 3.5

###### b. Parallel, three-dimensional force system

Consider the force system in Fig. 3.6(a), where the forces F1, F2, F3, . . . are parallel to the z-axis. To ﬁnd the resultant, we begin by replacing the forces with an equivalent force-couple system, with the force acting at the origin O, as shown in Fig. 3.6(b). The magnitude of the resultant force R, which is also parallel to the z-axis, and the resultant couple-vector CR are given by

###### R = F (3.8)

z z

z

R = ΣF

###### = =

F1

- F2
- F3

R

O O

O y

y

y

x1 x2

r x

###### x3

- y1
- y2
- y3

y A

CR = ΣMO

x

x

x

(a) Parallel, three-dimensional force system

(c) Resultant is a force (or a couple)

(b) Equivalent force-couple system

###### Fig. 3.6

and

###### CR = MO (3.9)

where MO is the sum of the moments of F1, F2, F3, . . . about O. The resultant couple-vector CR lies in the xy-plane (CR has no z-component because forces parallel to an axis have no moment about that axis).

Since R and CR are mutually perpendicular, the force system in Fig. 3.6(b) can be further simpliﬁed. If F = 0, then the resultant is the couple CR = MO. If F  = 0, the resultant is the force R acting through the unique point A in the xy-plane, as shown in Fig. 3.6(c). The vector r= xi + yj that locates this point is obtained by equating the moments about point O of the force-couple system in Fig. 3.6(b) and the force R in Fig. 3.6(c):

MO =r × R (3.10) The scalar components of this vector equation are

Mx = F1y1 + F2y2 + F3y3 + ··· = Ry My = −F1x1 − F2x2 − F3x3 − ··· = − Rx

where Mx and My are the moments of the original forces about the x- and y-axes, respectively. Therefore, the coordinates x and y become

###### λ

Plane normal to R

My R

Mx R

(3.11)

y =

x = −

R

###### c. General three-dimensional force system: The wrench

###### CR

O

It was shown in Art. 3.2 that a given force system can always be reduced to a force-couple system consisting of a resultant force R= F, acting at an arbitrary point O, and a resultant couple-vector CR = MO, as shown in Fig. 3.7(a). If R

and CR are mutually perpendicular, they can be reduced to a single force R, acting

(a)

###### R

R

CtR

CtR R

CRt

###### λ

r

CR

d

O

O

Direction of CRn

###### A

A

d

###### O

CRn

(b)

(c)

(d)

###### Fig. 3.7

through a unique point (this property was used in the special cases of coplanar and parallel force systems). In the general case, R and CR will not be perpendicular to each other, and thus they will not be reducible to a single force. However, a general force system can always be represented by a force and a parallel couple-vector by the procedure described next.

- • Resolve CR into the orthogonal components CtR and CnR, which are parallel and perpendicular to R, respectively. The result is shown in Fig. 3.7(b). The parallel component can be computed from Eq. (2.11):

CtR =(CR ·λ)λ (3.12)

where λ is the unit vector in the direction of R. The normal component is then found from

CnR =CR − CtR (3.13)

- • Because CnR and R are mutually perpendicular, they can be replaced by the single force R acting at point A, as illustrated in Fig. 3.7(c). The line of action of this force is determined by the requirement that its moment about O must be equal to CnR. In other words,

r × R=CnR (3.14)

where r is the vector drawn from O to any point on the new line of action of R. The scalar form of Eq. (3.14) is Rd = CnR, where d is the distance between O and A, as indicated in Fig. 3.7(c). This equation yields

d =

CnR R

(3.15)

Note that the line OA is perpendicular to CnR.

- • Move CtR to point A, as shown in Fig. 3.7(d) (we can do this because a couple is a free vector). The result is a collinear force-couple system, called the wrench. The direction of the wrench, also known as the axis of the wrench, is speciﬁed by the vector λ.

A physical example of a wrench is the operation of a screwdriver. You exert a force along the axis of the screwdriver to hold its tip against the screw, while applying a couple about the same axis to turn the screw. Because the force and the couple-vector are parallel, they constitute a wrench.

|Sample Problem 3.7<br><br>The values of Fz, Mx, and My for three force systems that are parallel to the z-axis are as follows:<br><br>Part Fz Mx My<br><br>1 50kN 60kN · m −125kN · m<br>2 −600lb 0 −1200lb · ft<br>3 0 600lb · in. −800lb · in.<br><br><br>Determine the resultant of each force system and show it on a sketch of the coordinate system.<br><br>Solution<br><br>Part 1<br><br>Fz =50 kN Mx =60 kN · m My = − 125 kN · m<br><br>The resultant is the force R=50k kN. With MO = Mxi + Myj and r= xi + yj, Eq. (3.10) can be used to determine the line of action of R:<br><br>MO =r × R<br><br>60i − 125j=<br><br>i j k x y 0 0 0 50<br><br>=50yi − 50xj<br><br>Equating like components gives the following scalar equations: 60=50y and − 125= − 50x<br><br>which gives x =2.5 m and y =1.2 m. The sketch of the resultant is shown in Fig. (a).<br><br>z<br><br>x<br><br>O y<br><br>50 kN<br><br>2.5m<br><br>1.2 m<br><br>(a)<br><br>Identical results for x and y are obtained if one uses Eqs. (3.11):<br><br>x = −<br><br>My R = −<br><br>−125<br><br>50 =2.5 m<br><br>y =<br><br><br>Mx R =<br><br>60 50 =1.2 m<br><br>Part 2<br><br>Fz = − 600 lb Mx =0 My = − 1200 lb · ft<br><br>The resultant is the force R= − 600k lb. In this case, Eq. (3.10) yields<br><br>MO =r × R<br><br>−1200j=<br><br>i j k x y 0 0 0 −600<br><br>= − 600yi + 600xj<br><br>Equating like components gives x = − 2 ft and y =0. The resultant is shown in Fig. (b).<br><br>z<br><br>x<br><br>O y<br><br>600 lb<br><br>2ft<br><br>(b)|
|---|

|Part 3<br><br>Fz =0 Mx =600 lb · in. My = − 800 lb · in.<br><br>Because the sum of the forces is zero and the sum of the moments is not zero, the resultant is the couple-vector CR = Mxi + Myj=600i − 800j lb · in., shown in Fig. (c). The magnitude of this couple-vector is 1000 lb · in.<br><br>O<br><br>(c)<br><br>y<br><br>x<br><br>z<br><br>800 lb.in.<br><br>CR = 1000 lb.in. 600 lb<br><br>.in.<br><br>Sample Problem 3.8<br><br>The parallel force system in Fig. (a) consists of the three forces shown and the 1250-N·m couple. (1) Determine the resultant, and show it on a sketch of the coordinate system. (2) Determine the resultant if the direction of the 100-N force is reversed.<br><br>100 N 1250 N.m<br><br>z<br><br>200 N<br><br>A B<br><br>300 N (a)<br><br>O<br><br>x<br><br>y<br><br>3 m 3 m 4m<br><br>3m<br><br>2m<br><br>Solution<br><br>Part 1<br><br>The resultant of the force system shown in Fig. (a) will be either a force or a couple. We begin by summing the forces.<br><br>+  R = Fz =100 − 200 + 300=200 N Therefore, the resultant is the force R=200k N.<br><br>We must use a moment equation to ﬁnd the line of action of R. Using the origin O as the moment center and assuming that R intersects the xy-plane at the point (x, y,0), Eq. (3.10) becomes<br><br>MO =r × R<br><br>3i × (−200k) + [(2i + 6j) × 300k]<br><br>−<br><br>4<br><br>5<br><br><br>1250i −<br><br>3 5<br><br>1250j = (xi + yj) × 200k|
|---|

|Expanding the cross products and simplifying, we obtain 800i − 750j=200yi − 200xj<br><br>Equating like components yields x =3.75 m and y =4 m. The resultant is shown x in Fig. (b).<br><br>O y R = 200 N<br><br>z<br><br>(b)<br><br>4 m<br><br>3.75m<br><br>Part 2<br><br>If the direction of the 100-N force is reversed, the sum of the forces will be zero, which means that the resultant is not a force. To determine the resultant couple, we must compute the moment about any point. We choose the origin O as the moment center. Because reversing the direction of the 100-N force has no effect on the moment about O, we conclude that the moment is the same as that found in the solution to Part 1. Therefore, the resultant is the couple-vector CR = MO =800i − 750j N · m.<br><br>Sample Problem 3.9<br><br>The plate is acted on by four parallel forces, three of which are shown in Fig. (a).<br><br>3 ft<br><br>2ft<br><br>4 ft<br><br><br>3ft<br><br>O<br><br>x<br><br>y<br><br>z<br><br>200 lb<br><br>400 lb<br><br>300 lb<br><br>(a)<br><br>The fourth force P and its line of action are unknown. The resultant of this force system is the couple-vector CR = −1100i+1500j lb·ft. Determine P and its line of action.<br><br>Solution<br><br>Because the resultant is a couple, the sum of the forces must be zero:<br><br>+  R = Fz = P + 300 + 400 − 200=0 from which P = −500 lb. Therefore, the force P is<br><br>P= − 500k lb Answer As shown in Fig. (b), we let A be the point where P intersects the xy-plane.<br><br>3 ft<br><br>2ft<br><br>yA<br><br>O<br><br>x<br><br>y<br><br>z<br><br>200 lb<br><br>400 lb<br><br>300 lb<br><br>xA<br><br>500 lb<br><br>3ft<br><br>A<br><br>(b)<br><br>To determine the location of A, we equate the sum of the moments of the original forces about any point to the moment of the resultant about that point (in this case, the moment of the resultant about every point is simply CR). Choosing point O as the moment center and noting that xAi + yAj is the vector from point O to point A, the moment equation becomes<br><br>CR = MO = r × F<br><br>− 1100i + 1500j =<br><br>i j k 3 0 0 0 0 −200<br><br>+<br><br>i j k 2 3 0 0 0 300<br><br>+<br><br>i j k xA yA 0<br><br>0 0 −500|
|---|

|Expanding the above determinants and equating like components gives<br><br>−1100 = 900 − 500yA<br><br>1500 = 600 − 600 + 500xA from which<br><br>xA =3 ft and yA =4 ft Answer<br><br>Sample Problem 3.10<br><br>Determine the wrench that is equivalent to the force system described in Sample Problem 3.1. Find the coordinates of the point where the axis of the wrench crosses the xy-plane.<br><br>Solution<br><br>As explained in the solution to Sample Problem 3.1, the original force system can be reduced to the force-couple system shown in Fig. (a): the force R, acting at the<br><br>y<br><br>z<br><br>x<br><br>O<br><br>CR R<br><br>r<br><br>x<br><br>y<br><br>(a)<br><br>A<br><br>λ<br><br>origin O, and the couple CR, where<br><br>R = 38.8i + 43.2j + 38.4k lb (a) CR = 390i + 116j + 360k lb · ft<br><br>The magnitude of R is<br><br>R = (38.8)2 + (43.2)2 + (38.4)2 =69.6 lb<br><br>We begin by determining the axis of the wrench, deﬁned by the unit vector λ in the direction of R:<br><br>λ =<br><br>R R =<br><br>38.8i + 43.2j + 38.4k 69.6<br><br>= 0.557i + 0.621j + 0.552k<br><br>The component of CR in the direction of λ can now be obtained from Eq. (3.12): CtR =(CR ·λ)λ. The magnitude of this vector is<br><br>CtR = CR ·λ<br><br>= (390i + 116j + 360k)·(0.557i + 0.621j + 0.552k)<br><br>= 488 lb · ft which gives<br><br>CtR = CtRλ=488(0.557i + 0.621j + 0.552k)<br><br>= 272i + 303j + 269k lb · ft|
|---|

|Therefore, the wrench consists of the force-couple system<br><br>R = 38.8i + 43.2j + 38.4k lb Answer<br><br>CtR = 272i + 303j + 269k lb · ft Answer To ﬁnd the coordinates of the point where the axis of the wrench intersects<br><br>the xy-plane, we must ﬁnd CnR, the component of CR that is normal to λ. From Eq. (3.13), we obtain<br><br>CnR =CR − CtR = (390i + 116j + 360k) − (272i + 303j + 269k)<br><br>= 118i − 187j + 91k lb · ft<br><br>Referring to Fig. (a), we let r= xi + yj be the vector from the origin O to A, the point where the wrench intersects the xy-plane. Using Eq. (3.14), we have<br><br>r × R=CnR<br><br>i j k x y 0 38.8 43.2 38.4<br><br>=118i − 187j + 91k<br><br>After expanding the determinant, we get<br><br>38.4yi − 38.4xj + (43.2x − 38.8y)k=118i − 187j + 91k Equating the coefﬁcients of i and j yields<br><br>38.4y = 118 y = 3.07 ft Answer −38.4x = −187 x = 4.87 ft Answer<br><br>The third equation, obtained by equating the coefﬁcients of k, is not independent of the preceding two equations, as can be easily veriﬁed.<br><br>The resultant wrench is depicted in Fig. (b), which shows the magnitudes of the force and the couple-vector.<br><br>y<br><br>z<br><br>x<br><br>O<br><br>4.87ft<br><br>3.07 ft<br><br>R = 69.6 lb<br><br>CR= 488 lb.ft<br><br>A<br><br>(b)<br><br>t|
|---|

![image 20](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile20.png>)

###### Problems

- 3.30 The values of Fz, Mx, and My for three force systems that are parallel to the z-axis are

|Case Fz Mx My|
|---|
|a −50lb −250lb · ft 200lb · ft<br><br>b 50kN 0 −250kN · m<br><br>c 40N 320N · m −400N · m<br><br><br>|

Determine the resultant of each force system and show it on a sketch of the coordinate system.

- 3.31 State whether the resultant of each force system shown is a force, a couple, or a wrench. Do not determine the resultant.

O

8 kN 9 kN

6 kN

12 m

9m

(a)

15 m

y

z

x

O

24 kN

(b)

15 kN

15 kN

O

20 kN

(c)

25 kN

20 kN

O

(d)

16 kN

12 kN

12 kN O

300 kN.m

(e)

15 kN

400 kN.m

Fig. P3.31

- 3.32 Determine the resultant of the three cable tensions that act on the x y

z

3ft

4 ft

6 ft

8ft

T3

T1

T2

4ft

O

Fig. P3.32, P3.33

horizontal boom if T1 =900 lb, T2 =500 lb, and T3 =300 lb.

- 3.33 The resultant of the three cable tensions acts along the y-direction. Determine T1 and T3 given that T2 =980 lb.

z

###### 3.34 The resultant of the three forces shown is the force R=200k lb. Deter-

P1

P2

mine P1, P2, and P3.

C

- 3.35 The resultant of the four forces that act on the right-angle bracket is a couple CR. Determine CR and the force P.

120 N

90 N

y

0.2 m

0.5m

80 N x

z

P

O

0.3m

0.3m

0.6m

0.8m

y

z

x

20 kN

60 kN

80 kN

Fig. P3.35 Fig. P3.36

- 3.36 Determine the resultant of the three forces shown.
- 3.37 Find the resultant of the three forces acting on the square plate.

70 lb

x

z

y

10 lb

60 lb

6ft 6ft

0.75ft

0.75ft

Fig. P3.37

- 3.38 The resultant of the forces P1, P2, and the couple C is the force R=12k lb

12 in.

15in.

B

P3

15in.

D

32 in.

20in.

y x

A

Fig. P3.34

z

P1

O

y

P2

C A

15in.

x

5 in. 15 in.

acting at point A (R is not shown in the ﬁgure). Determine P1, P2, and C.

Fig. P3.38, P3.39

- 3.39 Find the resultant of the two forces and the couple shown, given that P1 =20 lb, P2 =30 lb, and C =100lb · in.
- 3.40 Determine the resultant of the force system acting on the semi-circular

300 lb

z

plate.

500 lb.ft

120 lb

3ft

3.41 The streetlight A is attached to the end of the horizontal boom ABO. The light, which weighs 100N, is subjected to a wind load of 20N acting in the negative y-direction. The forces P and Q represent the tensions in the two cables that are attached at point B. The resultant of the four forces shown is a force R acting at point O. Determine the tensions P and Q and the force R.

30°

x y

200 lb

Fig. P3.40

z

1.5 m

C

1.5 m

D

###### P

Q 2 m

O

20 N

B

y

4m

A

x

2m

100 N

###### Fig. P3.41

- 3.42 The transmission tower OA is being hoisted into position by the cables AB and AC. The resultant of the cable tensions P and Q, along with the 2400-lb weight of the tower, is a force R acting at point O. Determine P, Q, and R.

x

z

B

O

C

y

20ft20ft

2400 lb

69 ft

A P

Q

28ft

32ft

36ft

40ft

Fig. P3.42

- 3.43 The force-couple system acting at O is equivalent to the wrench acting at A. If R = 600i + 1400j + 700k lb and |C| = 1200lb · ft, determine CR.

R

A

O

z

y x

R

CR C

2ft

3ft

R

CR O

z

x

y

Fig. P3.43 Fig. P3.44

- 3.44 The force-couple system consists of the force R = 250i +360j − 400k N and the couple-vector CR = 1200i+750j+560k N·m. Determine the equivalent

wrench and ﬁnd the coordinates of the point where the axis of the wrench crosses the xy-plane.

3.45 (a) Replace the force system shown by an equivalent force-couple system with the force acting at point O. (b) Determine the equivalent wrench, and ﬁnd the coordinates of the point where the axis of the wrench crosses the xy-plane.

z

8 kN

6 kN

1.5 m

6 kN

O

y

1.2m 1.2m

x

###### Fig. P3.45

###### 3.6 Introduction to Distributed Normal Loads

All forces considered up to this point have been assumed to be concentrated. Here we consider distributed loads that are directed normal to the surface on which they act, such as pressure. Two examples of distributed normal loads are the wind pressure acting on the side of a building and the water pressure on a dam. The methods for determining the resultants of distributed normal loads are very similar to those used for concentrated loads. The only notable difference is that integration is used in place of summation.

###### a. Surface loads

Consider the load shown in Fig. 3.8, which is parallel to the z-axis and distributed over the plane region lying in the xy-plane.* The distribution of the load is

z

y x

Load surface

p(x,y)

Region

Load area

###### Fig. 3.8

*The more general case of a load distributed over a curved surface is discussed in Chapter 8.

speciﬁed by the function p(x, y), called the load intensity. The units of load intensity are N/m2, lb/ft2, and so on. The plane region is known as the load area, and the surface formed by the plot of the load intensity is called the load surface. The region that lies between the load area and the load surface is labeled .

As shown in Fig. 3.9(a), we let dA represent a differential (inﬁnitesimal) area element of . The force applied to dA is dR= p dA. The distributed surface load can thus be represented mathematically as an inﬁnite number of forces dR that are parallel to the z-axis. Therefore, the resultant can be determined by employing the methods explained previously for parallel forces. However, because the force system here consists of an inﬁnite number of differential forces, the summations must be replaced by an integrations over the load area .

The resultant force is obtained from R = Fz, which becomes

###### R = dR= p dA (3.16)

where the range of integration is the load area .

The coordinates x¯ and y¯ that locate the line of action of R, shown in Fig. 3.9(b), are determined by Eqs. (3.11): x¯ = − My/R and y¯ = Mx/R. After replacing Mx by py dA and My by − px dA, these equations become

px dA p dA

py dA p dA

(3.17)

x¯ =

and y¯ =

Let us now consider Eqs. (3.16) and (3.17) from a geometrical viewpoint. By inspection of Fig. 3.9 we observe that dR= p dA represents a differential volume of the region in Fig. 3.8. This volume has been denoted dV in Fig. 3.9(a). Therefore, the resultant force R in Eq. (3.16) can also be written as

R = dV = V (3.18)

where V is the total volume of the region .

z

z

dR = p dA

R

O

O

y

y

###### =

x

p dV

x

C y

dA

y

x

x

Load area (a) (b)

###### Fig. 3.9

Replacing p dA with dV in Eqs. (3.17), we get

- x¯ =

x dV dV

=

x dV V

(3.19)

- y¯ =

y dV dV

y dV V

=

As will be explained in Chapter 8, Eqs. (3.19) deﬁne the coordinates of a point known as the centroid of the volume that occupies the region . This point is labeled C in Fig. 3.9(b). The z-coordinate of the centroid is of no concern here because x¯ and y¯ are sufﬁcient to deﬁne the line of action of the resultant force.

z

Load diagram w(s)

The determination of the resultant force of a normal loading distributed over a plane area may thus be summarized as follows:

y

s

- • The magnitude of the resultant force is equal to the volume of the region between the load area and the load surface.
- • The line of action of the resultant force passes through the centroid of the volume bounded by the load area and the load surface.

###### x

(a)

Load diagram w(y)

z

###### b. Line loads

y

Whenever the width of the loading area is negligible compared with its length, a distributed load can be represented as a line load. Loadings distributed along a plane curve and along a straight line are shown in Figs. 3.10(a) and (b), respec-

tively. Line loads are characterized by the load intensity w, a function of the distance measured along the line of distribution. The plot of w is called the load diagram. The units of w are N/m, lb/ft, and so on. In this article, we consider only straight-line loads. Loads distributed along plane curves will be discussed in Chapter 8.

- x (b)

Fig. 3.10

As shown in Fig. 3.11(a), a straight-line load is equivalent to an inﬁnite number of differential forces, each of magnitude dR=wdx. Because these forces are parallel, their resultant is R = Fz, or

L

L

###### wdx (3.20)

R =

dR=

x=0

0

directed parallel to the z-axis, as indicated in Fig. 3.11(b).

The line of action of R can be determined by equating the moments about point O for the two systems in Figs. 3.11(a) and (b):

L

L

+ MO =

x dR=

###### wx dx = Rx¯

x=0

0

z Load

dR = w dx

R

diagram

z

###### =

w(x)

dA

C O

x x

O

x

x dx

L

(a) (b)

###### Fig. 3.11

Substituting the expression for R given in Eq. (3.20) and solving for x¯, we obtain

L

0 wx dx

(3.21)

x¯ =

L

0 wdx

Referring to Fig. 3.11(a), we observe that dR=wdx equals the differential area dA under the load diagram. Therefore, Eq. (3.20) represents the total area A under that diagram. Substituting wdx =dA, Eq. (3.21) can be written as

L

L

x=0 x dA

x=0 x dA A

(3.22)

=

x¯ =

L

x=0 dA

It is shown in Chapter 8 that x¯ locates the centroid of the area under the load diagram, labeled C in Fig. 3.11(b) (the z-coordinate of the centroid is not of interest in this case). Therefore, we may conclude the following for straight-line loads:

- • The magnitude of the resultant force is equal to the area under the load diagram.
- • The line of action of the resultant force passes through the centroid of the area under the load diagram.

###### c. Computation of resultants

Examining Eqs. (3.16) through (3.22), we see that the computation of the resultant of distributed loading is essentially an integration problem. A discussion of the associated integration techniques is postponed until Chapter 8. However, if the

load surface or the load diagram has a simple shape, then tables of centroids, such as Table 3.1, can be used to determine the resultant as illustrated in the following sample problems.

|A. Volumes|B. Areas|
|---|---|
|Rectangular solid<br><br>x = 12 b y = 12 L z = 12 h V = bLh<br><br>y<br><br>z<br><br>b<br><br>C<br><br>L<br><br>h<br><br>x<br><br>y<br><br>x<br><br>z<br><br>|Rectangle<br><br>x = 12 b y = 12 h A = bh<br><br>b<br><br>h<br><br>y<br><br>x<br><br>C y<br><br>x|
|Right-triangular solid<br><br>x = 12 b y = 23 L z = 13 h V = 12 bhL<br><br>y<br><br>h<br><br>b<br><br>C<br><br>L x<br><br>y<br><br>z x<br><br>z|Right triangle<br><br>x = 23 b y = 13 h A = 12 bh<br><br>b<br><br>h<br><br>y<br><br>x<br><br>C<br><br>y<br><br>x|

Table 3.1 Centroids of Some Common Geometric Shapes (Additional tables are

found in Chapter 8.)

|Sample Problem 3.11<br><br>Determine the resultant of the line load acting on the beam shown in Fig. (a). y<br><br>O<br><br>15 kN/m<br><br>4 m 6 m<br><br>x<br><br>(a)<br><br>10 kN/m<br><br>Solution<br><br>We note that the load diagram is not one of the common shapes that are listed in Table 3.1. However, as shown in Fig. (b), the load diagram can be represented as the sum of three line loads corresponding to the two triangles, A1 and A2, and the rectangle A3. The resultant of each of these three line loads is equal to the area of the corresponding load diagram. The line of action of each resultant passes through the centroid of the diagram, the location of which can be found in Table 3.1.<br><br>O<br><br>(b)<br><br>4 m 6 m<br><br>y<br><br>P1 = 30 kN<br><br>x1 = 2.67 m<br><br>A1 C1<br><br>x2 = 6 m<br><br>x3 = 7 m<br><br>P2 = 15 kN<br><br>C3<br><br>A2 P3 = 60 kN<br><br>x<br><br>10 kN/m<br><br>15 kN/m<br><br>C2<br><br>A3<br><br><br>Letting P1, P2, and P3 be the resultants of the line loads represented by the areas A1, A2, and A3, respectively, we have<br><br>P1 =<br><br>1<br><br>2<br><br><br>(4)(15)=30 kN<br><br>P2 =<br><br>1<br><br>2<br><br><br>(6)(5)=15 kN<br><br>P3 = 6(10)=60 kN<br><br>The line of action of each of these forces passes through the centroid of the corresponding load diagram, labeled C1, C2, and C3 in Fig. (b). The x-coordinates of the centroids are obtained using Table 3.1:<br><br>x¯1 =<br><br>2<br><br>3<br><br><br>(4)=2.67 m<br><br>x¯2 = 4 +<br><br>1 3<br><br>(6)=6 m<br><br>x¯3 = 4 +<br><br>1<br><br>2<br><br><br>(6)=7 m|
|---|

|It follows that the magnitude of the resultant of the line load in Fig. (a) is given by<br><br>+<br><br><br><br>R = P1 + P2 + P3 =30 + 15 + 60=105 kN Answer<br><br>To determine x¯, the horizontal distance from point O to the line of action of R, we use the moment equation:<br><br>MO = Rx¯ + 30(2.67) + 15(6) + 60(7)=105x¯ which gives<br><br>x¯ =5.62 m Answer The resultant is shown in Fig. (c).<br><br>y<br><br>x = 5.62 m<br><br>R = 105 kN<br><br>O<br><br>(c)<br><br>Sample Problem 3.12<br><br>After a severe rainstorm, the ﬂat roof of the building shown in Fig. (a) is covered by 2.5in. of rainwater. The speciﬁc weight of water is 62.4lb/ft3, so water at a depth of 2.5in. causes a uniform pressure of 62.4(2.5/12)= 13lb/ft2. Determine the resultant force that the water exerts on the roof.<br><br>x<br><br>32ft<br><br>y<br><br>13 lb/ft2 on roof<br><br>(a)<br><br>O<br><br>32ft<br><br>z<br><br>75 ft<br><br>20ft<br><br>20ft<br><br>Solution<br><br>The load diagram in Fig. (b) can be divided into three solid shapes: two righttriangular solids of volume V1 and V3 and a rectangular solid of volume V2. The resultant force corresponding to each of these shapes is equal to the volume of the shape. Letting P1, P2, and P3 be the resultants, we have<br><br>P1 = V1 =13<br><br>1<br><br>2<br><br><br>(12)(75) =5850 lb<br><br>P2 = V2 =13[(40)(75)]=39000 lb<br>P3 = V3 = P1 =5850 lb<br>|
|---|

###### 134

|12ft<br><br>12ft<br><br>40ft<br><br>(b)<br><br>V2<br><br>V3<br><br>V1<br><br>C1<br><br>P1 = 5850 lb<br><br>C2<br><br>P2 = 39000 lb<br><br><br>C3<br><br>P3 = 5850 lb<br><br>y3 = 50 ft<br><br>y2 = 37.5 ft<br><br>y1 = 50 ft<br><br>75 ft<br><br>13 lb/ft2<br><br>The lines of action of these forces pass through the centroids of the corresponding volumes. The points where these forces intersect the roof of the building are labeled C1, C2, and C3 in Fig. (b).<br><br>The magnitude of the resultant force is given by<br><br>+<br><br><br><br>R = P1 + P2 + P3<br><br>= 5850 + 39000 + 5850=50700 lb Answer<br><br>Because the load area (the roof of the building) is symmetrical about the y-axis and the pressure is uniform, the resultant will lie along the y-axis. Therefore, we need only calculate the distance y¯ shown in Fig. (c).<br><br>(c)<br><br>z<br><br>x<br><br>O y<br><br>y = 40.4 ft R = 50 700 lb<br><br>Using Table 3.1, the coordinates of C1, C2, and C3 in Fig. (b) are<br><br>y¯1 = y¯3 =<br><br>2<br><br>3<br><br><br>(75)=50 ft<br><br>y¯2 =<br><br>1<br><br>2<br><br><br>(75)=37.5 ft<br><br>We can now determine y¯ using the moment equation<br><br>Mx = − Ry¯ − 5850(50) − 39000(37.5) − 5850(50)= − 50700 y¯ which yields<br><br>y¯ =40.4 ft Answer The resultant is shown in Fig. (c).|
|---|

![image 21](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile21.png>)

###### Problems

###### 3.46 During a storm, wind exerts a pressure of 2.3lb/ft2, normal to the surface of the stop sign. Determine the resultant force due to the wind.

10 in. 10 in. 12 in.

10 in.

z

STOP 12in.

10 in.

32m

O

y

x

Fig. P3.46

6 m

###### 3.47 Water pressure acting on the vertical wall of the concrete dam varies lin-

early with the depth of the water as shown. Determine the resultant force caused by the water.

58.9 kN/m2

Fig. P3.47

- 3.48 Determine the resultant of the line load acting on the beam ABC.

1700 lb/ft

1200 lb/ft

x A B C

y

6 ft 8 ft

Fig. P3.48

- 3.49 Determine the resultant of the line load acting on the beam.

y

A

B

x L/2

L/2

w0

w0

| | | |
|---|---|---|
| | | |

O L

L/2 L/2

y

x

w0

w0

Fig. P3.49 Fig. P3.50

- 3.50 Determine the resultant of the line loads acting on the frame, and the x-coordinate of the point where the resultant intersects the x-axis.

###### 3.46–3.55 Problems 137

- 3.51 Find the resultant of the distributed load acting on the ﬂat plate.

1.5 m

0.8m

y

x

80 kN/m2

120 kN/m2

z

Fig. P3.51

- 3.52 At a certain time during a hurricane, the wind pressure acting on the wall

120 ft

180 ft

z

x

O y

3.2lb/ft2

1.8lb/ft2

Wind

60 ft

80 ft

Fig. P3.52

of a high-rise building varies linearly as shown. Determine the resultant force caused by the wind.

- 3.53 The ﬁgure shows the water pressure acting on the sides of a dam that is 20-ft long. Determine the resultant force of the water pressure acting on the dam.

|B| |
|---|---|
| | |

y

A

x

312 lb/ft2 499 lb/ft2

5 ft

8 ft

|12ft<br><br>| |
|---|---|
|7.5ft| |

12ft7.5ft

6 ft

12 ft

750 lb/ft2

x 1217 lb/ft2

y

O

Fig. P3.53 Fig. P3.54

- 3.54 The water pressure acting on a masonry dam varies as shown. If the dam is 20ft wide, determine the resultant force of the water pressure acting on the dam.
- 3.55 The concrete pier is subjected to soil pressure that causes the line loads

y

6 MN/m 4 MN/m

| | |
|---|---|
|2.5 m| |

4 m

x

O

8 MN/m

shown. Determine the resultant of the loading and ﬁnd the y-coordinate of the point where the resultant crosses the y-axis.

Fig. P3.55

![image 22](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile22.png>)

###### Review of Equations

###### Resultant force-couple

The forces F1, F2, F3, ...can be reduced to the force R acting at an arbitrary point A and the couple CR:

R = Fi CR = ri × Fi ri = vector from A to any point on the line of action of Fi

###### Resultant of a force system

R = Fi if R  = 0 CR = ri × Fi if R = 0

###### Wrench

R = Fi CtR = (CR ·λ)λ λ = unit vector in the direction of R

###### Resultant of distributed normal load

px dA R y¯ =

py dA R

R = p dA x¯ =

R = volume under load diagram x¯, y¯ = centroidal coordinates of the volume under load diagram

###### Resultant of distributed line load

wx dx R

R = w dx x¯ =

R = area under the load diagram x¯ = centroidal coordinate of the area under the load diagram

![image 23](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile23.png>)

###### Review Problems

- 3.56 Find the resultant of the three forces acting on the eye bolt.

95 lb

360 lb

50°

x

y

20°

220 lb

Fig. P3.56

- 3.57 The resultant of the force system shown is a 50-lb · ft counterclockwise couple. Find P, Q, and C.

3 ft

x

y

- 2 ft 2 ft

4

3

- 3

4

P

Q

C

20 lb

Fig. P3.57

- 3.58 Determine the resultant of the three forces acting on the plate. Also, ﬁnd the coordinates of the point where the resultant crosses the xy-plane.

50 kN

3m

2m

150 kN

200 kN

z

x

O

y

Fig. P3.58

- 3.59 The ﬁve forces act at end A of the boom. Determine T1, T2, and T3 if the resultant of this force system is zero.

z

6m

C

4m

- T2 T1
- T3

B

30°

A 60 kN

y

20 kN D

x

8 m

###### Fig. P3.59

- 3.60 A portion of the square plate is loaded by the uniformly distributed load p =20lb/ft2. Find the coordinates of the point in the xy-plane through which the resultant passes.

6ft

p = 20 lb/ft2

y

z

x 12 ft

6ft

y

x

A a B

100 lb/ft

75 lb/ft

8 ft

Fig. P3.60 Fig. P3.61

- 3.61 The resultant of the line loads acting on the beam AB is a couple CR. Determine the distance a and the couple CR.
- 3.62 (a) Replace the force system shown with a force-couple system with the force acting at point O. (b) Determine the wrench that is equivalent to this force system. Find the coordinates of the point where the axis of the wrench crosses the xy-plane.

300 lb

200 lb 250 lb

300 lb

200 lb

B A

O

5 ft

2ft

z

y

x

Fig. P3.62

- 3.63 The center of gravity of the 30-lb square plate is at G. The plate can be raised slowly without rotating if the resultant of the three cable tensions is a 30-lb

force that passes through G. If T1 =6 lb and T2 =14 lb, ﬁnd T3 and the x- and

- y-coordinates of its point of attachment.

###### z T1

T2

T3

C

6

2 2

G

y A 3 y

x

6

B

6

6

Dimensions in inches

x

###### Fig. P3.63

- 3.64 The resultant of the force-couple system acting on the frame is a force R acting at point A. Determine the forces P and R.

140 kN.m 100 kN

30°

8 m

4 m

50 kN

y

A

x

P

6 m 30°

40°

O

4m

A

B

C

y

z 35 kN

25 kN

40 kN

x

Fig. P3.64 Fig. P3.65

- 3.65 Find the x- and y-coordinates of the point where the resultant of the three forces crosses the plate.
- 3.66 Replace the force system acting on the pipe with an equivalent forcecouple system with the force acting at point D.

z

300 lb

B

A

30 in.

780 lb.in.

x D

80in.

y

50in.

E

260 lb

###### Fig. P3.66

- 3.67 Replace the coplanar force system that acts on the casting with an equivalent force-couple system, with the force acting at (a) point O; and (b) point A.

3 ft

4 ft

2.5ft

150 lb

90 lb

200 lb

800 lb.ft y A

x

O

x

y

60°

30° 200 lb

100 lb

300 lb

O

Fig. P3.67 Fig. P3.68

- 3.68 Determine the magnitude of the resultant of the three concurrent forces acting on the hook.
- 3.69 Determine the wrench that is equivalent to the force-couple system shown and ﬁnd the coordinates of the point where the axis of the wrench crosses the xz-plane.

z

y

x

120 N

180 N.m 2 m

2 m

O

A

B

C 1.5m

T1

T2

T3

8 m

4m

3m

2m

3m

x y

O

z

Fig. P3.69 Fig. P3.70

- 3.70 The resultant of the three cable tensions acting on the ﬂagpole is the force R= Rk. Find T1, T2, and R given that T3 =500 N.

# 4

### Coplanar Equilibrium Analysis

![image 24](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile24.png>)

Principles of statics often enable us to determine quantities that cannot be easily measured directly. For example, measuring the axle loads of a dump truck with the tray in the up and down positions enables us to compute the weight of the chassis and the weight of the tray. This is illustrated in Problem P4.59. Lester Lefkowitz/The Image Bank/Getty Images

###### 4.1 Introduction

The ﬁrst three chapters of this text were devoted to mastering the elements of vector algebra, with emphasis on forces and couples. Proﬁciency in vector algebra is a prerequisite to the study of statics and most other areas of engineering mechanics.

With this chapter, we begin the application of vector methods to the equilibrium analysis of engineering problems. We introduce the free-body diagram, which is perhaps the most important physical concept found in this text. We show how the free-body diagram is used to obtain the equations that relate the forces acting on a body in equilibrium.

For the present, we restrict our attention to the analysis of bodies that are held in equilibrium by coplanar force systems. The subject is divided into three parts: analysis of single bodies, analysis of composite bodies (called frames and machines in some texts), and analysis of plane trusses.

###### 143

###### 4.2 Deﬁnition of Equilibrium

A body is said to be in equilibrium if the resultant of the force system that acts on the body vanishes. Equilibrium means that both the resultant force and the resultant couple are zero.

When a force system acts on a body that is initially at rest, the absence of a resultant means that the body has no tendency to move. The analysis of problems of this type is the focus of statics; dynamics is concerned with the response of bodies to force systems that are not in equilibrium.

We showed in Chapter 3 that a coplanar force system always can be represented as a resultant force R passing through an arbitrary point O and a couple CR that lies in the plane of the forces. Assuming that the forces lie in the xy-plane, R and CR can be determined from Rx = Fx, Ry = Fy, and CR = MO. Therefore, the equations of equilibrium are

###### Fx =0 Fy =0 MO =0 (4.1)

The summations in Eqs. (4.1) must, of course, include all the forces that act on the body—both the applied forces and the reactions (the forces provided by supports).

###### PART A: Analysis of Single Bodies

###### 4.3 Free-Body Diagram of a Body

The ﬁrst step in equilibrium analysis is to identify all the forces that act on the body. This is accomplished by means of a free-body diagram.

The free-body diagram (FBD) of a body is a sketch of the body showing all forces that act on it. The term free implies that all supports have been removed and replaced by the forces (reactions) that they exert on the body.

The importance of mastering the FBD technique cannot be overemphasized. Free-body diagrams are fundamental to all engineering disciplines that are concerned with the effects that forces have on bodies. The construction of an FBD is the key step that translates a physical problem into a form that can be analyzed mathematically.

Forces that act on a body can be divided into two general categories—reactive forces (or, simply, reactions) and applied forces. Reactions are those forces that are exerted on a body by the supports to which it is attached. Forces acting on a body that are not provided by the supports are called applied forces. Of course, all forces, both reactive and applied, must be shown on free-body diagrams.

The following is the general procedure for constructing a free-body diagram.

- 1. A sketch of the body is drawn assuming that all supports (surfaces of contact, supporting cables, etc.) have been removed.
- 2. All applied forces are drawn and labeled on the sketch. The weight of the body is considered to be an applied force acting at the center of gravity. As shown in Chapter 8, the center of gravity of a homogeneous body coincides with the centroid of its volume.
- 3. The support reactions are drawn and labeled on the sketch. If the sense of a reaction is unknown, it should be assumed. The solution will determine the correct sense: A positive result indicates that the assumed sense is correct, whereas a negative result means that the correct sense is opposite to the assumed sense.
- 4. All relevant angles and dimensions are shown on the sketch.

When you have completed this procedure, you will have a drawing (i.e., a freebody diagram) that contains all of the information necessary for writing the equilibrium equations for the body.

The most difﬁcult step to master in the construction of FBDs is the determination of the support reactions. Table 4.1 shows the reactions exerted by various coplanar supports; it also lists the number of unknowns that are introduced on an FBD by the removal of each support. To be successful at drawing FBDs, you must be completely familiar with the contents of Table 4.1. It is also helpful to understand the physical reasoning that determines the reactions at each support, which are described below.

- (a) Flexible Cable (Negligible Weight). A ﬂexible cable exerts a pull, or tensile force, in the direction of the cable. With the weight of the cable neglected, the cable forms a straight line. If its direction is known, removal of the cable introduces one unknown in a free-body diagram—the magnitude of the force exerted by the cable.
- (b) Frictionless Surface: Single Point of Contact. When a body is in contact with a frictionless surface at only one point, the reaction is a force that is perpendicular to the surface, acting at the point of contact. This reaction is often referred to simply as the normal force. (Walking on an icy sidewalk is treacherous because it is difﬁcult to generate a force in any direction except perpendicular to the sidewalk.) Therefore, removing such a surface introduces one unknown in a free-body diagram—the magnitude of the normal force. If contact between the body and the surface occurs across a ﬁnite area, rather than at one point, the line of action of the resultant normal force will also be unknown.
- (c) Roller Support. A roller support is equivalent to a frictionless surface: It can only exert a force that is perpendicular to the supporting surface. The magnitude of the force is thus the only unknown introduced in a free-body diagram when the support is removed.
- (d) Surface with Friction: Single Point of Contact. A friction surface can exert a force that acts at an angle to the surface. The unknowns may be taken to be

|Support|Reaction(s)|Description of reaction(s)|Number of unknowns|
|---|---|---|---|
|(a)<br><br>θ<br><br>Flexible cable of negligible weight|T<br><br>θ<br><br>|Tension of unknown magnitude T in the direction of the cable|One|
|θ<br><br>(b)<br><br>Frictionless surface (single point of contact)|θ<br><br>N|Force of unknown magnitude N directed normal to the surface|One|
|θ<br><br>θ<br><br>(c)<br><br>Roller support|θ<br><br>N|Force of unknown magnitude N normal to the surface supporting the roller|One|
|θ<br><br>(d)<br><br>Surface with friction (single point of contact)|θ<br><br>N<br><br>F|Force of unknown magnitude N normal to the surface and a friction force of unknown magnitude F parallel to the surface|Two|
|(e)<br><br>y<br><br>x Pin support|Rx<br><br>Ry|Unknown force R|Two|
|(f)<br><br>y<br><br>x<br><br>Built-in (cantilever) support|C Rx<br><br>Ry|Unknown force R and a couple of unknown magnitude C|Three|

###### Table 4.1 Reactions of Coplanar Supports

the magnitude and direction of the force. However, it is usually advantageous to represent the unknowns as N and F, the components that are perpendicular and parallel to the surface, respectively. The component N is called the normal force, and F is known as the friction force. If there is an area of contact, the line of action of N will also be unknown.

- (e) Pin Support. A pin is a cylinder that is slightly smaller than the hole into which it is inserted, as shown in Fig. 4.1(a). Neglecting friction, the pin can only exert a force that is normal to the contact surface, shown as R in Fig. 4.1(b). A pin support thus introduces two unknowns: the magnitude of R and the angle α that speciﬁes the direction of R (α is unknown because the point where the pin contacts the surface of the hole is not known). More commonly, the two unknowns are chosen to be perpendicular components of R, such as Rx and Ry shown in Fig. 4.1(c).
- (f) Built-in (Cantilever) Support. A built-in support, also known as a cantilever support, prevents all motion of the body at the support. Translation (horizontal or vertical movement) is prevented by a force, and a couple prohibits rotation. Therefore, a built-in support introduces three unknowns in a free-body diagram: the magnitude and direction of the reactive force R (these unknowns

are commonly chosen to be two components of R, such as Rx and Ry) and the magnitude C of the reactive couple.

Rx

###### R

###### α

Ry

(a) (b)

(c)

###### Fig. 4.1

You should keep the following points in mind when you are drawing free-body diagrams.

- 1. Be neat. Because the equilibrium equations will be derived directly from the free-body diagram, it is essential that the diagram be readable.
- 2. Clearly label all forces, angles, and distances with values (if known) or symbols (if the values are not known).
- 3. The support reactions must be consistent with the information presented in Table 4.1.
- 4. Show only forces that are external to the body (this includes support reactions and the weight). Internal forces occur in equal and opposite pairs and thus will not appear on free-body diagrams.

|Sample Problem 4.1<br><br>The homogeneous 6-m bar AB in Fig. (a) is supported in the vertical plane by rollers at A and B and by a cable at C. The mass of the bar is 50kg. Draw the FBD of bar AB. Determine the number of unknowns on the FBD.<br><br>Solution<br><br>The FBD of bar AB is shown in Fig. (b). The ﬁrst step in the construction of this diagram is to sketch the bar, assuming the supports have been removed. Then the following forces are added to the sketch.<br><br>C<br><br>20°<br><br>40°<br><br>(a)<br><br>A<br><br>B<br><br>y<br><br>x<br><br>4m<br><br>2m<br><br>B<br><br>C<br><br>A<br><br>40°<br><br>T<br><br>G<br><br>NA<br><br>NB W = 491 N<br><br>(b)<br><br>2m<br><br>1m<br><br>3m<br><br>20°<br><br>W: The Weight of the Bar<br><br>The weight W is shown as a vertical force acting at G, the center of gravity of the bar. Because the bar is homogeneous, G is located at the center of the bar. The magnitude of the weight is W = mg =(50)(9.81) = 491 N.<br><br>NA: The Normal Reaction at A<br><br>Removal of the roller support at A dictates that we show the force that this support can exert on the bar. From Table 4.1, we note that a roller support can exert a single force that is normal to the supporting surface. Therefore, on the FBD we show the reaction at A as a vertical force and label its magnitude as NA.<br><br>NB: The Normal Reaction at B<br><br>Following an argument similar to that for NA, we conclude that the removal of the roller support at B means that we must show a horizontal force at that point. On the FBD, we label this reaction as NB.<br><br>T: The Tension in the Cable at C<br><br>From Table 4.1, the force exerted by a cable is a tensile force acting in the direction of the cable. Therefore, the force exerted on the bar by the cable is shown as a force of magnitude T, acting at 20◦ to the horizontal.<br><br>We note that there are three unknowns on the FBD: the magnitudes of the three reactions (NA, NB, and T).|
|---|

|Sample Problem 4.2<br><br>The homogeneous, 250-kg triangular plate in Fig. (a) is supported by a pin at<br><br>y<br><br>B<br><br>x<br><br>0.6 m<br><br>(a)<br><br>0.35m<br><br>A<br><br>C<br><br>30°<br><br>A and a roller at C. Draw the FBD of the plate and determine the number of unknowns.<br><br>Solution<br><br>The FBD of the plate is shown in Fig. (b). The pin and roller supports have been<br><br>B C<br><br>Ax A Ay<br><br>NC<br><br>(b)<br><br>W = 2453 N<br><br>30°<br><br>G<br><br>0.35m<br><br>0.2 m 0.4 m<br><br>removed and replaced by the reactive forces. The forces acting on the plate are described below.<br><br>W: The Weight of the Plate<br><br>The weight of the plate is W =mg =(250)(9.81)=2453 N. It acts at the centroid G of the triangle ABC, the location of which was determined from Table 3.1. Only the horizontal location of G is shown in the ﬁgure, because it is sufﬁcient to determine the line of action of W.<br><br>Ax and Ay: The Components of the Pin Reaction at A<br><br>From Table 4.1, we see that a pin reaction can be shown as two components Ax and Ay, which are equivalent to an unknown force acting at an unknown angle. We have shown Ax acting to the right and Ay acting upward. These directions were chosen arbitrarily; the solution of the equilibrium equations will determine the correct sense for each force. Therefore, the free-body diagram would be correct even if Ax or Ay had been chosen to act in directions opposite to those shown in Fig. (b).<br><br>NC: The Normal Reaction at C<br><br>From Table 4.1, the force exerted by a roller support is normal to the inclined surface. Therefore, on the FBD we show the force NC at C, inclined at 30◦ to the vertical.<br><br>The FBD contains three unknowns: Ax, Ay, and NC.<br><br>Sample Problem 4.3<br><br>A rigid frame is fabricated by joining the three bars with pins at B, C, and D, as shown in Fig. (a). The frame is loaded by the 1000-lb force and the 1200-lb·ft couple. The supports consist of a pin at A and a roller support at E. Draw the FBD<br><br>F<br><br>1000 lb x<br><br>y<br><br>A<br><br>B<br><br>C<br><br>3 ft<br><br>| |D|
|---|---|
|1200<br><br>2 ft|2 ft 2 ft<br><br>E lb.ft|
<br><br>2 ft<br><br>(a)<br><br>1.5 ft 1.5 ft|
|---|

0.35m

###### 149

|of the frame, neglecting the weights of the members. How many unknowns are on the FBD?<br><br>Solution<br><br>The FBD of the entire frame is shown in Fig. (b). In addition to the applied force and couple, the diagram shows the pin reaction at A (Ax and Ay) and the normal force at roller E (NE).<br><br>1200 lb.ft 8 ft<br><br>Ax<br><br>Ay<br><br>A<br><br>F<br><br>E 1000 lb<br><br>1 ft NE<br><br>(b)<br><br>It is important to realize that the forces at pins B, C, and D do not appear on the FBD of the frame. These pin forces, as well as the forces inside the bars themselves, are internal to the frame (recall that only external forces are shown on FBDs).<br><br>We note that there are three unknowns on the FBD: Ax, Ay, and NE.<br><br>Sample Problem 4.4<br><br>The beam ABC, built into the wall at A and supported by a cable at C, carries a 6 ft distributed load over part of its length, as shown in Fig. (a). The weight of the<br><br>3 ft 5 ft<br><br>A B C<br><br>1000 lb/ft<br><br>(a)<br><br>y<br><br>x<br><br>beam is 70lb/ft. Draw the FBD of the beam.<br><br>Solution<br><br>The FBD of the beam is shown in Fig. (b). Because a built-in, or cantilever, sup-<br><br>A C<br><br>(b)<br><br>3<br><br>4<br><br>T<br><br>4 ft 4 ft 560 lb<br><br>3000 lb 1.5 ft<br><br>CA<br><br>Ax<br><br>Ay<br><br>port can exert a force and a couple, the reactions at the wall are shown as the force components Ax and Ay and the couple CA. The tension in the cable is labeled T. Also shown on the FBD are the weight of the beam (70lb/ft × 8ft = 560lb) and the resultant of the distributed load (3000lb, acting at the centroid of the loading diagram).<br><br>Observe that the FBD contains four unknowns whereas the number of equilibrium equations in Eqs. (4.1) is three. Therefore, it would not be possible to calculate all of the unknowns using only equilibrium analysis. The reason for the indeterminacy is that the beam is oversupported; it would be in equilibrium even if the cable at C were removed or if the built-in support were replaced by a pin connection.|
|---|

4.1–4.11 Problems 151

![image 25](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile25.png>)

###### Problems

4.1–4.3 Each of the bodies shown is homogeneous and has a mass of 30kg.

Assume friction at all contact surfaces. Draw the fully dimensioned FBD for each body and determine the number of unknowns.

Cable

A

0.9 m 0.6 m

1.2 m

B

0.1m

Cable

30°

O

800 N/m

1.5 m

A

B

B 30°

30°

A

###### Fig. P4.1 Fig. P4.2

Fig. P4.3

- 4.4 The homogeneous bar weighs 9lb. It is resting on friction surfaces at

B

A

9.5in.

18 in.

30in.

Fig. P4.4

A and B. Draw the FBD of the bar and determine the number of unknowns.

- 4.5 The homogeneous beam AB weighs 400lb. For each support condition shown in (a) through (d), draw the FBD of the beam and determine the number of unknowns.

Cable

8ft

12 ft B

6 ft 6 ft

A B C

A

40°

(a) (b)

Cables

60° 30°

12 ft B

A

A 12 ft B

(c)

(d)

###### Fig. P4.5

###### 4.6 The homogeneous triangular plate has a mass of 12kg. Draw the FBD of the plate for each set of supports shown in (a)–(d) and determine the number of unknowns.

210 mm

Friction

A

120 mm

Friction

Frictionless

60° 30°

B

(b)

(a)

45°

Friction

(c) (d)

Fig. P4.6

12 in.

###### 4.7 The bracket of negligible weight is supported by a pin at A and a frictionless

peg at B, which can slide in the slot in the bracket. Draw the FBD of the bracket if (a) θ =45◦; and (b) θ =90◦. What are the unknowns?

B

θ 56lb. ft

- 4.8 To open the high-pressure water cock, a 12-lb horizontal force must be applied to the handle at A. Draw the FBD of the handle, neglecting its weight. Count the unknowns.

2in.

6in.

12 lb

A

B

C

20°

8 in.

D

Frictionless

Fig. P4.8, P4.9

- 4.9 The high-pressure water cock is rigidly attached to the support at D. Neglecting the weights of the members, draw the FBD of the entire assembly and count the unknowns.
- 4.10 Draw the FBD of the entire frame, assuming that friction and the weights

24 in.

A

Fig. P4.7

4 ft 1 ft

|20 lb/ft| |E|
|---|---|---|
| | | |
|Slot<br><br>D<br><br>A B| | |

3 ft

###### C

3 ft

of the members are negligible. How many unknowns appear on this FBD? 4.11 Draw an FBD of member CE of the frame described in the previous problem. How many unknowns appear on this FBD?

4 ft

Fig. P4.10, P4.11

4.4 Coplanar Equilibrium Equations 153

###### 4.4 Coplanar Equilibrium Equations

###### a. General case

As stated in Art. 4.2, a body is in equilibrium under a coplanar force system if both the resultant force R and the resultant couple CR of the force system are zero. It follows that the following three conditions are necessary for equilibrium:

###### Fx = 0 Fy = 0 MO = 0 (4.1 repeated)

where the moment center O and the orientation of the xy-coordinate system can be chosen arbitrarily. The two force equations are equivalent to R = 0, and the moment equation assures us that CR = 0.

It often is convenient to use a set of three independent equations different from those in Eqs. (4.1). The alternative equations are described next.

- 1. Two force equations and one moment equation The x- and y-directions in Eqs. (4.1) do not have to be mutually perpendicular—as long as they are not parallel. Hence, the equilibrium equations can be restated as

Fx = 0 Fy = 0 MO = 0 (4.2)

where x and y are any two non-parallel directions and O is an arbitrary point.

- 2. Two moment equations and one force equation It is possible to replace one of the force equations in Eqs. (4.2) by a moment equation, obtaining

MA = 0 MB = 0 Fx = 0 (4.3)

Here, A and B are any two distinct points, and x is any direction that is not perpendicular to the line AB. Note that if MA = 0 and MB = 0 are satisﬁed, the resultant only can be a force R that lies along the line AB, as shown in Fig. 4.2. The equation Fx = 0 (x not perpendicular to AB) then

|R<br><br>B<br><br>x'<br><br>C<br><br><br>A|
|---|

Plane of forces

Fig. 4.2

can be satisﬁed only if R = 0.

- 3. Three moment equations We also can replace both force equations in Eqs. (4.2) by two moment equations. The result is

###### MA = 0 MB = 0 MC = 0 (4.4)

where A, B, and C are any three distinct, non-collinear points, as indicated in Fig. 4.2. Again the equations MA = 0 and MB = 0 are satisﬁed only if the resultant is a force R that lies along the line AB. The third equation MC = 0 (C not on the line AB) then guarantees that R = 0.

###### b. Concurrent force system

Recall that the resultant of a concurrent force system is a force R that passes through the point of concurrency, which we label as point O. The moment equation MO = 0 now is satisﬁed trivially, so that the number of independent equilibrium equations is reduced from three to two. Using the arguments in Part a, it is straightforward to verify that the following are valid choices for independent equilibrium equations, each set consisting of two equations.

- 1. Two force equations.

Fx =0 Fy =0 (4.5)

- where x and y are any two non-parallel directions in the xy-plane.

2. Two moment equations.

MA =0 MB =0 (4.6)

where A and B are any two points in the xy-plane (except point O) provided that A, B, and O do not lie on a straight line.

3. One force equation and one moment equation.

Fx =0 MA =0 (4.7)

where A is any point in the xy-plane (except point O) and x is any direction that is not perpendicular to the line OA.

c. Parallel force system

Assume that all the forces lying in the xy-plane are parallel to the y-axis. The equation Fx =0 is automatically satisﬁed, and the number of independent equilibrium equations is again reduced from three to two. Using the reasoning in Part a, it can be shown that there are two choices for independent equilibrium equations, each containing two equations:

- 1. One force equation and one moment equation.

Fy =0 MA =0 (4.8)

where y is any direction in the xy-plane except the x-direction, and A is any point in the xy-plane.

- 2. Two moment equations.

###### MA =0 MB =0 (4.9)

where A and B are any two points in the xy-plane, provided that the line AB is not parallel to the y-axis.

4.5 Writing and Solving Equilibrium Equations 155

###### 4.5 Writing and Solving Equilibrium Equations

The three steps in the equilibrium analysis of a body are:

- Step 1: Draw a free-body diagram (FBD) of the body that shows all of the forces and couples that act on the body.
- Step 2: Write the equilibrium equations in terms of the forces and couples that appear on the free-body diagram.
- Step 3: Solve the equilibrium equations for the unknowns.

In this article, we assume that the correct free-body diagram has already been drawn, so that we can concentrate on Steps 2 and 3—writing and solving the equilibrium equations.

The force system that holds a body in equilibrium is said to be statically determinate if the number of independent equilibrium equations equals the number of unknowns that appear on its free-body diagram. Statically determinate problems can therefore be solved by equilibrium analysis alone. If the number of unknowns exceeds the number of independent equilibrium equations, the problem is called statically indeterminate. The solution of statically indeterminate problems requires the use of additional principles that are beyond the scope of this text.

When analyzing a force system that holds a body in equilibrium, you should ﬁrst determine the number of independent equilibrium equations and count the number of unknowns. If the force system is statically determinate, these two numbers will be equal. It is then best to outline a method of analysis, or plan of attack, which speciﬁes the sequence in which the equations are to be written and lists the unknowns that will appear in each equation. After you have determined a viable method of analysis, you can then proceed to the mathematical details of the solution.

One word of caution—the set of equilibrium equations used in the analysis must be independent. An attempt to solve a dependent set of equations will, at some stage, yield a useless identity, such as 0=0.

By now you should realize that, although the solution of a statically determinate problem is unique, the set of equations used to determine that solution is not unique. For example, there is an inﬁnite number of choices for point O in the equilibrium equation MO =0.

With an inﬁnite number of equilibrium equations from which to choose, how are you to decide which equations to use for a given problem? The answer is to base your choice on mathematical convenience. If you intend to solve the equations by hand, try to select equations that involve as few unknowns as possible, thus simplifying the algebraic manipulations required. However, if you have access to a computer or a programmable calculator with equation-solving capability, the solution of simultaneous equations is not burdensome and the choice of equations is therefore not critical. It cannot be overemphasized that the set of chosen equations must be independent.

|Sample Problem 4.5<br><br>The weight W is attached to one end of a rope that passes over a pulley that is free to rotate about the pin at A. The weight is held at rest by the force T applied to the other end of the rope. Using the given FBD, show that T = W and compute the pin reactions at A.<br><br>A<br><br>T T<br><br>x r<br><br>Ay A<br><br>W<br><br>Ax<br><br>y<br><br>r<br><br>30° 30°<br><br>FBD<br><br>| | |
|---|---|
|W| |
<br><br>Solution<br><br>Method of Analysis<br><br>The forces shown on the FBD are the weight W, the pull T acting at the end of the rope, and the reactive forces applied to the pulley by the pin at A. Because the force system is coplanar, there are three independent equilibrium equations. The number of unknowns is also three (T, Ax, and Ay), which means that the problem is statically determinate.<br><br>The equilibrium equation MA = 0 is a convenient starting point. Since the pin reactions have zero moments about A, the only unknown in this equation is T. Having computed T, we can then determine Ax from Fx = 0 and Ay from<br><br>Fy = 0.<br><br>Mathematical Details<br><br>MA = 0 + Tr − Wr = 0 T = W Q.E.D.<br><br>This result is signiﬁcant because it shows that the tension in a rope does not change when the rope passes over a pulley that is supported by a frictionless pin.<br><br>Fx = 0 −→+ Ax + T sin30◦ = 0<br>Fy = 0 +  Ay − W − T cos30◦ = 0<br><br><br>With T = W, the last two equations yield<br><br>Ax = −0.5W Ay = 1.866W Answer<br><br>The minus sign indicates that Ax acts to the left; that is, in the direction opposite to what is shown on the FED.|
|---|

|Sample Problem 4.6<br><br>The homogeneous 60-kg disk supported by the rope AB rests against a rough vertical wall. Using the given FBD, determine the force in the rope and the reaction at the wall.<br><br>200<br><br>150<br><br>200<br><br>150<br><br>Dimensions in mm FBD<br><br>3<br>4<br><br><br>A<br><br>B<br><br>y<br><br>NC C<br><br>FC<br><br>T<br><br>B<br><br>x<br><br>A<br><br>W = 588.6 N<br><br>Solution<br><br>Method of Analysis<br><br>The FBD contains the weight W =60(9.81)=588.6N, acting at the center of the disk. The other forces shown on the FBD are the force T applied by the rope and the reactive forces NC (the normal reaction) and FC (the friction force) applied by the wall. The result is a general, coplanar force system for which there are three independent equilibrium equations. Since the number of unknown forces is also three, the problem is statically determinate.<br><br>Because NC and T intersect at point B, the moment equation MB = 0 will yield FC. Then the two force equations Fx = 0 and Fy = 0 can be used to calculate NC and T.<br><br>Mathematical Details<br><br>MB = 0 gives FC = 0 Answer Fy = 0 +  4<br><br>5<br><br>T − 588.6 = 0 T = 735.8 N Answer Fx = 0 −→+ NC −<br><br>3 5<br><br>T = 0 NC −<br><br>3 5<br><br>(735.8) = 0 NC = 441 N Answer<br><br>Another Method of Analysis<br><br>MA = 0 + 200NC − 150(588.6) = 0 NC = 441 N<br><br>|
|---|

|Sample Problem 4.7<br><br>The homogeneous, 120-kg wooden beam is suspended from ropes at A and B. A power wrench applies the 500-N · m clockwise couple to tighten a bolt at C. Use the given FBD to determine the tensions in the ropes.<br><br>|4 m 2 m A B| |
|---|---|
| | |
|3 m|500|
<br><br>4 m 2 m A B<br><br>C<br><br>C<br><br>500 N.m<br><br>N.m FBD<br><br>W = 1177.2 N<br><br>TA TB<br><br>y<br><br>x<br><br>Solution<br><br>Method of Analysis<br><br>The FBD of the beam contains the weight W =mg =120(9.81)= 1177.2 N acting at the center of the beam, the 500-N · m couple applied by the wrench, and the unknown tensions TA and TB in the ropes. Because all the forces lie in the xy-plane and are parallel to the y-axis, there are two independent equilibrium equations. There are also two unknowns: TA and TB. Therefore, the problem is statically determinate.<br><br>It is convenient to start the analysis with the equilibrium equation MA =0. Because this equation does not contain TA, we can immediately solve it for TB. We can then use the equation Fy =0 to calculate TA.<br><br>Mathematical Details<br><br>MA =0 + 4TB − 1177.2(3) − 500=0<br><br>TB =1007.9 N Answer Fy =0 +  TA + TB − 1177.2=0<br><br>Substituting TB =1007.9 N and solving for TA, we get<br><br>TA =169.3 N Answer|
|---|

|Other Methods of Analysis<br><br>Another, equally convenient option is to compute TA using MB = 0 as<br><br>MB =0 + − 4TA + 1177.2(1.0) − 500=0<br><br>TA =169.3 N<br><br>Sample Problem 4.8<br><br>The 420-lb homogeneous log is supported by a rope at A and loose-ﬁtting rollers at B and C as it is being fed into a sawmill. Calculate the tension in the rope and the reactions at the rollers, using the given FBD. Which rollers are in contact with the log?<br><br>A<br><br>B<br><br>C<br><br>T<br><br>FBD<br><br>y<br><br>NB<br><br>W = 420 lb<br><br>NC<br><br>x<br><br>30°<br><br>30°<br><br>30° A<br><br>30°<br><br>B<br><br>C<br><br>10ft<br><br>5ft<br><br>7.5ft<br><br>5ft<br><br>2.5ft<br><br>Solution<br><br>Method of Analysis<br><br>The FBD contains the weight W of the log and three unknown forces: the tension T in rope and the roller reactions NB and NC perpendicular to the log. The sense of each roller reaction indicates that we have assumed the upper rollers to be in contact with the lumber.<br><br>The force system in the FBD is the general coplanar case, for which three independent equilibrium equations are available. Because there are also three unknowns, the problem is statically determinate.<br><br>In general, equilibrium analysis would require the solution of three simultaneous equations, with all three unknowns appearing in each equation. With planning, it usually is possible to reduce the number of unknowns that must be solved simultaneously. Referring to the FBD, we could start with Fx =0, which would contain only two unknowns: NB and NC. Then we would look for another equation that contains only these two unknowns. Inspection of the FBD reveals that the equation MA =0 would not contain T, because this force passes through A.|
|---|

|The equations Fx and MA could thus be solved simultaneously for NA and NB. Finally, Fy would be used to compute T.<br><br>Mathematical Details<br><br>Fx =0 −→+ −NB cos30◦ − NC cos30◦ =0 (a) MA =0 + 420(7.5sin30◦) + 10NB + 15NC =0 (b)<br><br>The solution of Eqs. (a) and (b) is<br><br>NB =315.0 lb and NC = − 315.0 lb Answer<br><br>The signs indicate that the sense of NB is as shown on the FBD, whereas the sense of NC is opposite to that shown. Therefore, the upper roller at B and the lower roller at C are in contact with the log.<br><br>Fy =0 +  T − 420 − NB sin30◦ − NC sin30◦ =0<br><br>Because NB = − NC, this equation yields<br><br>T =420 lb Answer<br><br>Other Methods of Analysis<br><br>The above solution used the equations Fx =0, Fy =0, and MA =0. There are other sets of independent equilibrium equations that would serve equally well. For example, we could ﬁnd T from just a single equation—summation of forces parallel to the log equals zero. Because NB and NC are perpendicular to the log, T would be the only unknown in this equation. The reaction NC could also be computed independently from the other unknowns by setting the sum of the moments about the point where T and NB intersect to zero. Similarly, we could ﬁnd NB from a single equation—summation of moments about the point where T and NC intersect equals zero.<br><br>It is important to realize that the equilibrium equations must be independent. Referring to the FBD, you might be tempted to use the three moment equations<br><br>MA =0, MB =0, and MC =0. Although each is a valid equation, they are not independent of each other. Why not? What would happen if you tried to solve these equations for NB, NC, and T?|
|---|

![image 26](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile26.png>)

###### Problems

###### In each of the following problems, the free-body diagram is given. Write the equilibrium equations, and compute the requested unknowns.

- 4.12 The homogeneous cylinder of weight W rests in a frictionless right-angled corner. Determine the contact forces NA and NB in terms of W and θ.

A

B

NA

NB FBD

W

θ

θ

θ

A

B

15°

P

4ft

15°

120 lb

4ft

P

15°

A

N FBD

15°

A

F

Fig. P4.12 Fig. P4.13

- 4.13 Calculate the force P that is required to hold the 120-lb roller at rest on the rough incline.
- 4.14 Solve Prob. 4.13 if the force P pushes rather than pulls.

P

15°

15°

4ft

120 lb

4ft

P

A

N

F

FBD

15°

15°

A

Fig. P4.14

- 4.15 The 480-kg bent bar ABC of uniform cross section is supported by a pin at A and a vertical cable at C. Determine the pin reactions and the force in the cable.

y

Ay

A A

Ax

x

- 2 m

T

WAB=160(9.81) N

B C B C

4 m

2 m 2 m

WBC = 320(9.81) N

FBD

###### Fig. P4.15

###### 4.16 The table lamp consists of two uniform arms, each weighing 0.8lb, and a

2-lb bulb ﬁxture. If θ =16◦, calculate the couple CA that must be supplied by the friction in joint A.

4 in.

θ

20 in.

2 lb 0.8 lb

0 in.

b

l

8

2

0.

A

14 in. 10 in.

0.8 lb

16°

10 in.

2 lb

0.8 lb Ax

10 in.

A

CA

Ay

FBD

Fig. P4.16

###### 4.17 At what angle θ will the lamp in Prob. 4.16 be in equilibrium without the couple CA?

14 in. 10 in.

C

θ

0.8 lb

10 in.

2 lb

1.5 m

A

0.8 lb Ax

10 in.

2 m

- 3 m

B

A

150 kg

Cy

Ay

y

2.5m

Cx

FBD

x

A

Fig. P4.17

3 m 150(9.81) N

- 2 m
- 3 4

B

RB

###### 4.18 The bent beam ABC is attached to a pin at C and rests against a roller

FBD

support at B. Neglecting the weight of the beam, ﬁnd the reactions at B and C caused by the 150-kg load.

Fig. P4.18

###### 4.19 Compute all reactions at the base A of the trafﬁc light standard, given that the tension in the cable BC is (a) T = 544 lb; and (b) T =0. The weight of the standard is negligible compared with the 320-lb weight of the trafﬁc light.

4 ft

- C A

15 ft

320 lb

B

- C 10 ft

10 ft

8 ft

B

###### T

320 lb

15ft

CA

A

Ax

Ay

FBD

###### Fig. P4.19

4.20 The man is holding up the 35-kg ladder ABC by pushing perpendicular to the ladder. If the maximum force that the man can exert is 400N, determine the smallest angle θ at which he can support the ladder.

C

4m

- 2m

- 3m

2m

35(9.81) N

B Ax

B

400 N

θ θ A

A

Ay

FBD

###### Fig. P4.20

###### 4.21 The machine part of negligible weight is supported by a pin at A and a roller at C. Determine the magnitudes of the forces acting on the part at A and C.

C

400

2.4 kN.m

40°

A

B

200 250 300

3 kN

Dimensions in mm

NC

50°

C

400

2.4 kN.m

40°

B

Ax

A

200 250 300

3 kN

Ay

FBD

Fig. P4.21

###### 4.22 The uniform plank ABC weighs 400N. It is supported by a pin at A and a cable that runs around the pulley D. Determine the tension in the cable and the components of the pin reaction at A. Note that the tension in the cable is constant (see Sample Problem 4.5).

D

70°

A

C

B

2.5 m

0.5 m

y

T T

70°

|x<br><br>B| |
|---|---|
|1.5 m|1.0 m 0.5 m|

A Ax

C

400 N FBD

Ay

Fig. P4.22

###### 4.23 The center of gravity of the 850-N man is at G. If the man pulls on the rope with a 388-N force, determine the horizontal distance b between the man’s feet and G.

388 N

0.6m 0.6m

30° 30°

G

G

1.2m 1.2m

850 N

D

FD

D

b

b ND

FBD

###### Fig. P4.23

###### 4.24 The homogeneous 200-lb sign is suspended from three wires. Find the tension in each wire.

T2 T3 4 ft 4 ft

A B T1

A B

4

3

y

3 ft

2 ft

x

200 lb FBD

Fig. P4.24

###### 4.25 When the truck is empty, it weighs 6000lb and its center of gravity is at G. Determine the total weight W of the logs, knowing that the load on the rear axle is twice the load on the front axle.

72 in. 144 in.

96 in. 92 in. 60 in.

|W 5<br><br>|4W<br><br>5<br>|
|---|---|
| | |

45°

6000 lb

G

###### G

A

A B

B 200 in.

120 in. 60 in.

NA = 2NB NB

20 in.

FBD

###### Fig. P4.25

###### 4.6 Equilibrium Analysis for Single-Body

###### Problems

We learned that the three steps in the equilibrium analysis of a body are:

- 1. Draw the free-body diagram (FBD).
- 2. Write the equilibrium equations.
- 3. Solve the equations for the unknowns.

The individual steps were introduced separately in the preceding articles. The purpose of this article is to give you experience in the entire process of equilibrium analysis.

Always begin by drawing the FBD; there are no exceptions. The FBD is the very key to equilibrium analysis, so it should be drawn with great care. We recommend that you use a straightedge and circle template. After the FBD has been drawn, the remainder of the solution, consisting of writing and solving equilibrium equations, will be straight forward.

It must be reiterated that if the number of unknowns on the FBD equals the number of independent equations (statically determinate problem), you will be able to calculate all of the unknowns. Conversely, if the number of unknowns exceeds the number of independent equations (statically indeterminate problem), all of the unknowns cannot be determined by using equilibrium analysis alone.

Although there are many statically indeterminate problems of practical importance, you will ﬁnd that nearly all problems in this text are statically determinate. To solve a statically indeterminate problem, one must consider deformations of the body, as well as equations of equilibrium. The solution of statically indeterminate problems is discussed in texts with such titles as Strength of Materials or Mechanics of Materials, the understanding of which requires a prior knowledge of statics.

|Sample Problem 4.9<br><br>The telephone cable spool in Fig. (a) weighs 300lb and is held at rest on a 40◦<br><br>0.8 ft<br><br>G<br><br>1.5 ft<br><br><br>40°<br><br>(a)<br><br>G<br><br>300 lb 40° A<br><br>F<br><br>N<br><br>T<br><br>1.5ft<br><br>(b)<br><br>0.8 ft G<br><br>F<br><br>N<br><br>T<br><br>1.5ft<br><br>(c)<br><br>0.8 ft<br><br>300 sin 40° 300 cos 40°<br><br>A<br><br>1.5 cos 40° ft<br><br>40°<br><br>40°<br><br>B<br><br>A<br><br>x<br><br>y<br><br>40°<br><br>y x<br><br>x<br><br>y<br><br>40°<br><br>y x<br><br>Friction<br><br>incline by the horizontal cable. The cable is wound around the inner hub of the spool and attached to the support at B. Assume that G, the center of gravity of the spool, is located at the center of the spool. Find all forces acting on the spool.<br><br>Solution<br><br>Method of Analysis<br><br>The ﬁrst step is, of course, to draw the FBD of the spool, which is shown in Fig. (b). In addition to its weight, the spool is acted on by the normal contact force N and friction force F (both acting at the point of contact A) and by the cable tension T. Note that the magnitudes T, N, and F are the only unknowns and that there are three independent equilibrium equations (general coplanar force system). Therefore, the problem is statically determinate. We illustrate one method of solution in detail and then discuss several other methods that could be used.<br><br>We start with the equation<br><br>MA =0<br><br>The tension T can be calculated using this equation because it will be the only unknown (N and F do not have moments about point A). The next equation is<br><br>MG =0<br><br>The unknowns in this equation will be T and F, because N has no moment about G. Because T has already been found, this equation can be solved for F. Finally, we use the equation<br><br>Fy =0<br><br>The unknowns in this equation will be T and N (F is perpendicular to the y -direction). Again, with T already computed, N can be found.<br><br>Mathematical Details<br><br>To help you follow the details of the preceding analysis, the FBD of the spool has been redrawn in Fig. (c). Note that the 300-lb weight of the spool has been replaced by its x - and y -components and that the vertical distance between A and G (1.5cos40◦ ft) has been added. The analysis now proceeds as follows:<br><br>MA =0 + 300sin40◦(1.5) − T(0.8 + 1.5cos40◦)=0<br><br>T =148.4 lb Answer MG =0 + F(1.5) − T(0.8)=0 F =<br><br>148.4(0.8)<br><br>1.5 =79.1 lb Answer Fy =0 + N − 300cos40◦ − T sin40◦ =0<br><br>N =300cos40◦ + 148.4sin40◦ =325.2 lb Answer|
|---|

|The positive signs determined for T, F, and N indicate that the correct sense for each force was assumed on the FBD.<br><br>As a check on this solution, we can verify that the above answers satisfy a fourth equilibrium equation. For example,<br><br>Fx =0 −→+ F cos40◦ − N sin40◦ + T<br><br>=79.1cos40◦ − 325.2sin40◦ + 148.4 ≈ 0 Check<br><br>Other Methods of Analysis<br><br>Two additional methods of analysis are outlined in the table below, with the mathematical details omitted.<br><br>Equation Unknowns Solution<br><br>MG = 0 T and F<br><br>Solve simultaneously for T and F<br><br>Fx = 0 T and F<br>Fy = 0 T and N Knowing T, solve for N MA = 0 T Solve for T<br><br><br>Fx = 0 T and F Knowing T, solve for F<br>Fy = 0 T, N, and F Knowing T and F, solve for N<br><br><br>In this sample problem, we have illustrated only three of the many sets of equations that can be used to analyze this problem. You may ﬁnd it beneﬁcial to outline one or more additional analyses. Outlining the solution will permit you to concentrate on the method of analysis without becoming too involved with the mathematical details of the solution.<br><br>Sample Problem 4.10<br><br>Determine the mass of the heaviest uniform bar that can be supported in the position shown in Fig. (a) if the breaking strength of the horizontal cable attached at C is 15kN. Neglect friction.<br><br>C<br><br>20°<br><br>1.2m<br><br>1.2m<br><br>(a)<br><br>4<br><br>3<br><br>A<br><br>B<br><br>Solution<br><br>Method of Analysis<br><br>We begin by drawing the FBD of the bar as shown in Fig. (b). The weight W of<br><br>A<br><br>C<br><br>20° B<br><br>1.2m<br><br>1.2m<br><br>(b)<br><br>3<br><br>4<br>5 W<br><br><br>NA<br><br>NB<br><br>T = 15 kN<br><br>x<br><br>y<br><br>y<br><br>x<br><br>the heaviest bar that can be supported will be obtained when the tension T is set|
|---|

|equal to 15kN. A heavier bar would result in a cable tension greater than 15kN, and the cable would break.<br><br>There are three unknowns in the FBD: the normal contact forces NA and NB, and W. Note that the directions of all these forces are known. The unknowns can, therefore, be found using the three independent equilibrium equations that are available for a general coplanar force system. However, because we are seeking W only, it may not be necessary to use all three equations.<br><br>In our analysis, we will use the following two equations.<br><br>Fx =0<br><br>The force NA can be found from this equation (W and NB will not appear because they are perpendicular to the x-direction).<br><br>MB =0<br><br>This equation will contain the two unknowns W and NA. Because NA already has been determined, W now can be found.<br><br>Mathematical Details<br><br>Referring to the FBD in Fig. (b), the mathematical details of the preceding analysis are as follows:<br><br>Fx =0 −→+<br><br>4<br><br>5<br><br><br>NA − 15=0<br><br>NA =18.75 kN (a) MB =0 + W(1.2cos 20◦) + 15(1.2sin20◦) −<br><br>3 5<br><br>NA(2.4cos20◦) −<br><br>4<br><br>5<br><br><br>NA(2.4sin20◦)=0 (b)<br><br>Substituting NA =18.75 kN from Eq. (a) into Eq. (b) gives W =28.0 kN. Therefore, the mass of the heaviest bar that can be supported without breaking the cable is<br><br>m =<br><br>W g =<br><br>28.0 × 103 9.81 =2850 kg Answer<br><br>Other Methods of Analysis<br><br>Another method that could be used to calculate W is outlined in the following table.<br><br>Equation Unknowns Solution<br><br>MA= 0 NB and W<br><br>Solve simultaneously for NB and W Fx = 0 NB and W<br><br>There are, of course, many other sets of equations that could be used to compute W. It is even possible to determine W using only one equilibrium equation— a moment equation taken about the point where NA and NB intersect.|
|---|

|Sample Problem 4.11<br><br>Figure (a) shows the distributed loading due to water pressure that is acting on the upstream side of the ﬂood barrier. Determine the support reactions acting on the barrier at A and B. Neglect the weight of the barrier.<br><br>B<br><br>10 ft<br><br>3200 lb/ft<br><br>60°<br><br>8ft<br><br>(a)<br><br>A<br><br>B<br><br><br>A<br><br>60°<br><br>(b)<br><br>y<br><br>x R = 16000 lb<br><br>D 30°<br><br>Ay<br><br>Ax<br><br>NB<br><br>C<br><br>8ft<br><br>y = 103 ft<br><br>Solution<br><br>Method of Analysis<br><br>The FBD of the barrier is shown in Fig. (b), where NB is the reaction at B, acting perpendicular to the inclined surface, and Ax and Ay are the components of the pin reaction at A. Any three independent equilibrium equations can be used to determine these three unknowns. As explained in Art. 3.6, the resultant of a distributed load is equal to the area under the loading diagram, acting at the centroid of that area. Therefore, we obtain<br><br>R =<br><br>1<br><br>2<br><br><br>(10)(3200)=16000 lb<br><br>and from Table 3.1, we ﬁnd<br><br>y¯ =<br><br>10 3<br><br>ft<br><br>Because the unknown forces Ax and Ay intersect at A, a convenient starting point is<br><br>MA =0|
|---|

|This equation will determine NB. We then use<br><br>Fx =0<br><br>Having previously determined NB, this equation will give Ax. The ﬁnal equation is<br><br>Fy =0<br><br>With NB previously computed, Ay can be found from this equation.<br><br>Mathematical Details<br><br>MA =0 + 16000<br><br>10 3 − NB(8)=0<br><br>NB =6670 lb Answer<br><br>Fx =0 −→+ NB cos30◦ + Ax − 16000=0<br><br>Ax =16000 − (6670)cos30◦ =10220 lb Answer<br><br>Fy =0 +  Ay + NB sin30◦ =0<br><br>Ay = − (6670)sin30◦ = − 3340 lb Answer<br><br><br><br><br>The signs indicate that NB and Ax are directed as shown on the FBD, whereas the correct direction of Ay is opposite the direction shown on the FBD. Therefore, the force that acts on the barrier at A is<br><br>3340 lb<br><br>10220 lb<br><br>A<br><br>θ<br><br>|A| = (10220)2 + (3340)2 =10750 lb<br><br>θ = tan−1<br><br>3340<br><br>10220 =18.1◦ Answer and the force at B is<br><br>6670 lb<br><br>30°<br><br>Answer<br><br>Other Methods of Analysis<br><br>There are, of course, many other independent equations that could be used to solve this problem. Referring to the FBD in Fig. (b), the following set of equations has the advantage of determining each unknown independently of the other two.<br><br>Equation Unknowns Solution<br><br>MA=0 NB Solve for NB MC =0 Ax Solve for Ax MD=0 Ay Solve for Ay|
|---|

![image 27](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile27.png>)

###### Problems

- 4.26 The homogeneous bar AB weighs 30lb. Determine the magnitudes of the forces acting on the bar at A and B. Neglect friction.

B

A

60°

12ft

35°

P

0.5m

A

y

9 ft B

120 lb/ft

x

Fig. P4.26 Fig. P4.27 Fig. P4.28

- 4.27 Determine the horizontal force P required to keep the homogeneous 30-kg cylinder in equilibrium on the rough inclined surface.
- 4.28 The homogeneous beam AB weighing 600lb carries the distributed load shown. Find the support reactions at A and B.
- 4.29 The homogeneous 40-kg bar ABC is held in position by a horizontal rope

C

1.25m

2m

B

A 30°

Fig. P4.29 attached to end C. Neglecting friction, determine the tension in the rope.

- 4.30 The horizontal force P is applied to the handle of the puller. Determine the resulting tension T in the chain in terms of P.

P

20°

24 in.

B

40° A

6in.

| | |
|---|---|
|x| |

2 ft

12 ft 9 ft

6 ft

9 ft

A B

C

Fig. P4.30 Fig. P4.31

- 4.31 The thin steel plate, weighing 82lb/ft2, is being lifted slowly by the cables AC and BC. Compute the distance x and ﬁnd the corresponding tension in each of the cables.
- 4.32 Neglecting the mass of the beam, compute the reactions at A and B.

2kN

1 kN/m

A

12 kN · m

B

3m 3m 6 m

###### Fig. P4.32

- 4.33 The 1200-kg car is being lowered slowly onto the dock using the hoist A and winch C. Determine the forces in cables BA and BC for the position shown.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |

2.2 m

5.6 m

2.4 m

A

B

C

5.6 m C

A B

P

30°

60°

Fig. P4.33 Fig. P4.34, P4.35

- 4.34 The crate weighing 400lb is supported by three ropes concurrent at B. Find the forces in ropes AB and BC if P =460 lb.
- 4.35 Find the smallest value of P for which the crate in the Prob. 4.34 will be in equilibrium in the position shown. (Hint: A rope can only support a tensile force.)
- 4.36 Determine the rope tension T for which the pulley will be in equilibrium.

120 mm 75 mm

2 kN

200 N.m

T

Fig. P4.36

- 4.37 The 60-kg homogeneous disk is resting on an inclined friction surface.

- (a) Compute the magnitude of the horizontal force P. (b) Could the disk be in equilibrium if the inclined surface were frictionless?

30°

0.5m

0.3 m P

Fig. P4.37, P4.38

- 4.38 The 60-kg homogeneous disk is placed on a frictionless inclined surface and held in equilibrium by the horizontal force P and a couple C (C is not shown on the ﬁgure). Find P and C.

###### 4.39 The mass of the uniform bar AB is 40kg. Calculate the couple C required for equilibrium if (a) θ = 0; and (b) θ =54◦.

A

2m

C

θ 20°

B

Fig. P4.39

###### 4.40 The mechanism shown is a modiﬁed Geneva drive—a constant velocity input produces a varying velocity output with periods of dwell. The input torque is 120 N·m. For the position shown, compute the contact force at B and the magnitude of the reaction at A. Neglect friction and the weights of the components.

180mm

B

C

A

18° 28° 120 N·m

Input Output

Fig. P4.40

###### 4.41 The center of gravity of the 3000-lb car is at G. The car is parked on an incline with the parking brake engaged, which locks the rear wheels. Find (a) the normal forces (perpendicular to the incline) acting under the front and rear pairs of wheels; and (b) the friction force (parallel to the incline) under the rear pair of wheels.

2.2ft

G

A

3ft

B

12°

6ft

Fig. P4.41

###### 4.42 The 1800-kg boat is suspended from two parallel cables of equal length. The location of the center of gravity of the boat is not known. Calculate the force P required to hold the boat in the position shown.

| | | |
|---|---|---|
| | |A<br><br>20° 20°<br><br>|
| | | |

B

P

###### Fig. P4.42

- 4.43 The bracket contains three slots that engage pins that are attached to a

Dimensions in mm

30 N 30°

B

50 A 30° C

50

150 100

Fig. P4.43 wall. Neglecting friction, determine the force exerted on the bracket by each pin.

- 4.44 The uniform ladder of weight W is raised slowly by applying a vertical

B

32L

P

L_

3

- 2L
- 3

C

A

θ

Fig. P4.44, P4.45

force P to the rope at A. Show that P is independent of the angle θ.

- 4.45 The uniform, 40-lb ladder is raised slowly by pulling on the rope attached at A. Determine the largest angle θ that the ladder can attain if the maximum allowable tension in rope BC is 330lb.
- 4.46 The 90-kg man, whose center of gravity is at G, is climbing a uniform ladder. The length of the ladder is 5m, and its mass is 20kg. Friction may be neglected. (a) Compute the magnitudes of the reactions at A and B for x =1.5 m.

(b) Find the distance x for which the ladder will be ready to fall.

L

=5m

G

x

1.6 m

1.2 m

A

B

165 lb

30°

20°

y

b

x

B

L

=144in.

A

Fig. P4.46 Fig. P4.47

- 4.47 The homogeneous 240-lb bar AB is in equilibrium in the position shown. Determine the distance b that locates the 165-lb force and compute the magnitude of the support reaction at A.
- 4.48 The tensioning mechanism of a magnetic tape drive has a mass of 0.4kg,

T

20 mm 100 mm

B

T

120 mm

G

A

and its center of gravity is at G. The tension T in the tape is maintained by presetting the tensile force in the spring at B to 14N. Calculate T and the magnitude of the pin reaction at A.

80 mm

Fig. P4.48

###### P 4.49 The homogeneous 300-kg cylinder is pulled over the 100-mm step by the

horizontal force P. Find the smallest P that would raise the cylinder off the surface at A. Assume sufﬁcient friction at corner B to prevent slipping.

600mm

- 4.50 The homogeneous 18-kg pulley is attached to the bar ABC with a pin at B. The mass of the bar is negligible. The cable running over the pulley carries a tension of 600N. Determine the magnitudes of the support reactions at A and C.

| | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | |

600 N

18 kg

40°

600 N

C

B

A

120

Dimensions in mm

96

240 240

Fig. P4.50

- 4.51 Each of the sandbags piled on the 250-lb uniform beam weighs 12lb. Determine the support reactions at A and C.

C

x

11 ft 8 ft

B

A

y B 5 C

A

2.5

Dimensions in feet

1.5

1.5 1.5

2

Fig. P4.51 Fig. P4.52

- 4.52 The homogeneous 600-lb plate is suspended from three cables. Determine the force in each cable.
- 4.53 The supporting structure of the billboard is attached to the ground by a pin

B A

100 mm

Fig. P4.49

q lb/ft

10 ft

###### G

at B, and its rear leg rests on the ground at A. Friction may be neglected. Point G is the center of gravity of the billboard and structure, which together weigh 2800 lb. To prevent tipping over in high winds, a 2370-lb weight is placed on the structure near A, as shown. (a) Compute the magnitudes of the reactions at A and B if the wind load on the billboard is q =120 lb/ft. (b) Find the smallest wind load q that would cause the structure to tip over.

1.5 ft

8 ft

2370 lb

A B

1.5 ft

7 ft

4.54 The self-regulating ﬂoodgate ABC, pinned at B, is pressed against the lip of the spillway at C by the action of the 3645-lb weight A. If the gate is to open

Fig. P4.53

x

|A| |
|---|---|
| | |
| | |
|3645 lb| |

B

6 ft

C h

3 ft

320h lb/ft

###### Fig. P4.54

when the water level reaches a height h =6 ft, determine the distance x locating the weight A. Neglect the weight of the gate.

- 4.55 The cantilever beam is built into a wall at O. Neglecting the weight of the

x

360 lb

400 lb

100 lb

200 lb

120 lb

4 ft 4 ft 3 ft

3 ft

y

O

Fig. P4.55 beam, determine the support reactions at O.

- 4.56 Determine the force F required to keep the 200-kg crate in equilibrium in 34°

| | | |
|---|---|---|
| | | |
| | | |

8 m

200 kg

6.5m

B

A C

F

Fig. P4.56

the position shown.

- 4.57 Determine the angle θ for which the 1250-N homogeneous cylinder will be in equilibrium in the position shown. Also, ﬁnd the tension in the rope AB.

500 N

W = 1250 N

- A
- B

θ

375 N C

150 50

A

B

P

T

50

25°

Dimensions in mm

Fig. P4.57 Fig. P4.58

- 4.58 A machine operator produces the tension T in the control rod by applying the force P to the foot pedal. Determine the largest P if the magnitude of the pin reaction at B is limited to 1.8kN. Neglect the mass of the mechanism.

∗4.59 The dump truck consists of a chassis and a tray, with centers of gravity at G1 and G2, respectively. With the tray down, the axle loads (normal forces at A and B) are 41900 lb each. When the tray is in the raised position, the rear axle load increases to 48700 lb. Compute the weight of the chassis, the weight of the tray, and the distance x.

12 ft 7 ft

###### G

G2

G1

A B x

14.5 ft

###### Fig. P4.59

∗4.60 The centers of gravity of the 50-kg lift truck and the 120-kg box are at G1 and G2, respectively. The truck must be able to negotiate the 5-mm step when the pushing force P is 600 N. Find the smallest allowable radius of the wheel at A. Be sure to check whether the truck will tip.

P

G2

1200

G1

A B

375

5

500

1200

Dimensions in mm

###### Fig. P4.60

###### PART B: Analysis of Composite Bodies

4.7 Free-Body Diagrams Involving Internal

Reactions

Up to now, we have been considering “one-body” problems. Because we have been concerned primarily with calculating external reactions, each problem has required the use of only one free-body diagram (FBD) and the solution of one set of equilibrium equations. We now begin a study of the forces that act at connections that are internal to the body, called internal reactions. The calculation of internal reactions often requires the use of more than one FBD.

In this article, attention is focused on the drawing of FBDs of the various parts that together form a composite body. Frames and machines are examples of connected bodies that are commonly used in engineering applications. Frames are rigid structures that are designed to carry load in a ﬁxed position. Machines contain moving parts and are usually designed to convert an input force to an output force.

The construction of FBDs that involve internal forces relies on Newton’s third law: For every action there is an equal and opposite reaction. Strict adherence to this principle is the key to the construction of FBDs.

###### a. Internal forces in members

Consider the beam in Fig. 4.3(a), which carries the load P acting at its center (P and θ are assumed known). In the FBD of the entire beam, Fig. 4.3(b), there are three unknown external reactions (Ax, Ay, and NB) and three independent equilibrium equations. Therefore, the beam is statically determinate, and the three unknowns could be easily calculated, although we will not do so here.

P

P

y

L

θ

|4|D<br><br>θ|
|---|---|
| | |

B

B

A

Ax

A

x

L 2

L 2

L 2

L 2

Ay NB

(a)

(b)

P

Dy CD

CD

θ

A

Dx

Dx

B

Ax

L 4

L 4

L 2 NB

Ay

Dy

(d)

(c)

###### Fig. 4.3

Now suppose that we are asked to determine the force system that acts on the internal cross section at D, located a distance L/4 to the right of end A. We begin by isolating the parts of the beam that lie to the left and right of D. In effect, we imagine that the beam is cut open at the section of interest. Thus the cross section that was initially an internal section now becomes an external section. We then draw the FBDs of both parts of the beam, as shown in Fig. 4.3(c) and (d).

Consider the FBD for the left portion of the beam, Fig. 4.3(c). The right portion of the beam has been removed, and its effect is shown as an unknown force (represented by the independent components Dx and Dy) and an unknown couple (CD), the senses of which are assumed.

On the FBD for the right portion of the beam, Fig. 4.3(d), the effect of the removed left portion is likewise an unknown force and an unknown couple. However, Newton’s third law prescribes that the effect that the right part of the beam has on the left part is equal and opposite to the effect that the left part has on the right. Therefore, on the FBD in Fig. 4.3(d), the force system at D consists of the forces Dx and Dy and the couple CD, each equal in magnitude, but opposite in direction, to its counterpart in Fig. 4.3(c). That is the key to understanding FBDs! When isolating two parts of a body in order to expose the internal reactions, these reactions must be shown as equal and opposite force systems on the FBDs of the respective parts.

Note that we are using scalar representation for the forces and couples in the FBDs in Fig. 4.3. For example, the magnitude of the x-component of the force at D is labeled Dx, and its direction is indicated by an arrow. If a vector representation is used, one force of the pair would be labeled Dx and the other force −Dx. Because there is no advantage to using vector notation here, we continue to use the scalar representation.

B

P

Finally, note that if Ax, Ay, and NB had been previously computed from the FBD for the entire beam, the FBD in either Fig. 4.3(c) or (d) could be used to calculate the three unknowns Dx, Dy, and CD.

L

Q

Observe that internal forces do not appear on the FBD of the entire beam, Fig. 4.3(b). The reason is that there are two internal force systems acting on every section of the beam, each system being equal and opposite to the other. Therefore, internal reactions have no effect on the force or moment equations for the entire beam.

y

A x C

- (a)

θ θ

B

Q

P

- (b)

###### b. Internal forces at connections

Consider the frame shown in Fig. 4.4(a) , which consists of two identical, homo-

L 2

geneous bars AB and BC, each of weight W and length L. The bars are pinned together at B and are attached to the supports with pins at A and C. Two forces P and Q are applied directly to the pin at B. We assume that L, W, P, Q, and θ are known quantities. Furthermore, throughout this text we neglect the weights of pins and other connectors, unless stated otherwise.

L 2

W

W

θ θ

The FBD of the structure shown in Fig. 4.4(b) contains four unknown pin reactions: Ax and Ay (the forces exerted on bar AB by the pin A) and Cx and Cy (the forces exerted on bar BC by the pin C). The senses of these forces have been chosen arbitrarily. Because only three independent equilibrium equations are available from this FBD, you might presume that the problem is statically indeterminate. Indeed, this would be the correct conclusion if ABC were a single rigid unit, rather than two rigid bars joined by a pin. If the system is “taken apart”

Ax Cx

A C

Ay Cy

Fig. 4.4

and an FBD is drawn for each component, it will be seen that the problem is statically determinate. As explained in the following, drawing the FBD of each component increases the number of unknowns, but the number of independent equations also increases.

The FBD of each component of the frame is shown in Fig. 4.5.

By

Bx

P B

Bx By

Q

(c)

By

B Bx

Bx

B

L 2

L 2

By

L 2

L 2

θ W θ

W

C

Ax A

Cx

Ay

Cy

(a)

(b)

###### Fig. 4.5

Figure 4.5 (a) FBD of bar AB with pins at A and B removed.

W is the weight of bar AB acting at the center of the bar.

Ax and Ay are the forces exerted on bar AB by the pin at A. Bx and By are the forces exerted on bar AB by the pin at B.

###### Notes

- 1. The senses of Ax and Ay cannot be chosen arbitrarily here. These senses were already assumed when the FBD of the system, Fig. 4.4(b), was drawn. Initially, the sense of an unknown force may be chosen arbitrarily, but if that force appears on more than one FBD, its sense must be consistent with the original assumption.
- 2. The senses of Bx and By were chosen arbitrarily, because this is the ﬁrst FBD on which these forces appear.
- 3. P and Q are applied directly to the pin at B, so they do not appear on this FBD (recall that the pin at B has been removed).

Figure 4.5 (b) FBD of bar BC with pins at B and C removed.

By

B Bx

W is the weight of bar BC acting at the center of the bar. Cx and Cy are the forces exerted on bar BC by the pin at C.

L 2

B x and B y are the forces exerted on bar BC by the pin at B.

L 2

###### Notes

θ W

- 4. The directions of Cx and Cy must be the same as shown in Fig. 4.4(b). (See Note 1.)
- 5. The forces exerted by the pin B on bar BC are labeled B x and B y. Because this

is the ﬁrst FBD on which B x and B y have appeared, their senses have been chosen arbitrarily.

Figure 4.5 (c) FBD of pin B with bars AB and BC removed.

P and Q are the external forces acting directly on the pin. Bx and By are the forces exerted on the pin by bar AB. B x and B y are the forces exerted on the pin by bar BC.

Notes

- 6. Because P and Q are applied directly to the pin at B, they will appear on every FBD that contains that pin.
- 7. The senses of Bx and By are opposite to the senses chosen for these forces on the FBD of bar AB. This follows from Newton’s third law: The force exerted on bar AB by the pin B is equal and opposite to the force exerted on pin B by bar AB. A similar argument holds for the directions of B x and B y.

Ax A

Ay

(a)

Bx

B

L 2

By

L 2

W

θ

C

Cx

Cy

(b)

By

Bx

P B

Bx By

Q

Let us now count the unknowns and the independent equilibrium equations available from the FBDs in Fig. 4.5. There are eight unknowns: Ax, Ay, Bx, By, B x, B y, Cx, and Cy. The number of equilibrium equations is also eight: three each from the FBDs of bars AB and BC (general coplanar force systems) and two from the FBD of the pin at B (concurrent, coplanar force system). Therefore, we conclude that the problem is statically determinate, and the eight unknowns are solvable from the eight independent equilibrium equations.

(c)

Fig. 4.5 repeated

As mentioned previously, there are also three independent equations for the FBD of the entire body, shown in Fig. 4.4. Does this mean that we have a total of 8 + 3=11 independent equations? The answer is no! The FBD for the entire system is not independent of the FBDs for all of its parts—the FBDs in Fig. 4.5 could be put back together again to form the FBD in Fig. 4.4. In other words, if each part of the body is in equilibrium, then equilibrium of the entire body is guaranteed. This means that of the eleven equations just cited, only eight will be independent.

Let us now change the problem by assuming ABC to be a single rigid unit rather than two bars pinned together at B. In this case, the body would be able to transmit a force and a couple at B. Consequently, the number of unknowns would be increased by one (the magnitude of the couple), but the number of independent equations would remain at eight. Hence, this problem would be statically indeterminate.

So far, we have drawn the FBD for the entire system and the FBDs for each of its parts. There are two other FBDs that could be constructed—the FBDs with the pin B left inside bar AB and those with pin B left inside bar BC. These FBDs are shown in Figs. 4.6 and Fig. 4.7, respectively. As you study each of the FBDs, note that B x and B y do not appear in Fig. 4.6 because they are now internal forces. For the same reason, Bx and By do not appear in Fig. 4.7. It should be noted again that, although we have drawn additional FBDs, the total number of independent equilibrium equations remains eight.

By

Bx

B Bx

B

P

L 2

L 2

By

Q

L 2

L 2

θ W θ

W

C

Ax A

Cx

Ay

Cy

FBDs of AB and BC with pin B left in BC

###### Fig. 4.6

By

B Bx

Bx

B

L 2

L 2

P Q

By

L 2

L 2

W Ax A

W

θ θ

C

Cx

Ay

Cy

FBDs of AB and BC with pin B left in AB

###### Fig. 4.7

The following special case is extensively used in the construction of FBDs of bodies that are joined by pins.

###### Special Case: Equal and Opposite Pin Reactions

If two members are joined by a pin and if there are no external forces applied to the pin, then the forces that the pin exerts on each member are equal in magnitude and oppositely directed.

It is relatively easy to verify this statement by referring again to the FBD of the pin B, Fig. 4.5(c). Note that if there are no forces applied to the pin (i.e.,

if P = Q =0), the equilibrium equations for the pin dictate that Bx = B x and By = B y—the pin reactions are equal in magnitude and oppositely directed.

Using this special case, the FBDs for bars AB and BC, and pin B would be as shown in Fig. 4.8. Here, the total number of unknowns is six, and the total number of independent equations is six—three for each bar. Obviously, two of the original eight equations have been used up in proving that the pin reactions at B are equal and opposite.

By

B Bx

Bx

B

L 2

L 2

By

L 2

L 2

θ W W θ

C

Ax A

Cx

Cy

Ay

FBDs with no external forces applied to pin B

###### Fig. 4.8

In this text we utilize equal and opposite pin reactions wherever applicable. That is, our FBDs of members display equal and opposite reactions at the pins, as shown at B in Fig. 4.8. The FBDs of the pins are not drawn. The two most common situations where the pin reactions are not equal and opposite are

- • External force is applied to the pin
- • More than two members are connected by the pin

|Sample Problem 4.12<br><br>(1) Referring to Fig. (a), draw the FBD for the entire frame and for each of its<br><br>D<br><br>C0<br><br>P<br><br>1.5 m<br><br>1.5 m<br><br>2 m 2 m<br><br>C<br><br>B<br><br>(a)<br><br>y<br><br>x<br><br>A<br><br>A B<br><br>D<br><br>C<br><br>C0<br><br>(b)<br><br>3 m<br><br>Ax 2 m 2 m<br><br>P<br><br>Ay<br><br>Cx<br><br>Cy<br><br>parts, neglecting the weights of the members. (2) Determine the total number of unknowns and the total number of independent equilibrium equations, assuming that the force P and couple C0 are known.<br><br>Solution<br><br>Part 1<br><br>The force system on each of the FBDs is described below. FBD of Entire Frame—Fig. (b)<br><br>P and C0: applied force and applied couple Ax and Ay: components of the force exerted on the frame by pin A (directions are<br><br>assumed)<br><br>Cx and Cy: components of the force exerted on the frame by pin C (directions are<br><br>assumed)<br><br>FBD of Member ABD—Fig. (c)<br><br>P: applied force Ax and Ay: components of the force exerted on member ABD by pin A [must be<br><br>shown acting in the same directions as in Fig. (b)]<br><br>Dx and Dy: components of the force exerted on member ABD by pin D (directions<br><br>are assumed)<br><br>NB: force exerted on member ABD by the roller at B (must be perpendicular to<br><br>member CDB)<br><br>FBD of Member CDB—Fig. (d)<br><br>C0: applied couple Cx and Cy: components of the force exerted on member CDB by pin C [must be<br><br>shown acting in the same directions as in Fig. (a)]<br><br>(c)<br><br>Ay<br><br>Dx<br><br>Dy<br><br>Ax A 2 m 2 m B<br><br>P<br><br>4<br><br>3<br><br>NB<br><br>D<br><br>1.5 m<br><br>(d)<br><br>3 m 1.5 m<br><br>2 m 2 m<br><br>B Dy<br><br>Dx<br><br>C<br><br>C C<br><br>C<br><br>D<br><br>Cx C0<br><br>Cy<br><br>4<br><br>3 NB<br><br>|
|---|

|Dx and Dy: components of the force exerted on member CDB by pin D [must be<br><br>equal and opposite to the corresponding components in Fig. (c)]<br><br>NB: force exerted on the member by the roller at B [must be equal and opposite to<br><br>the corresponding force in Fig. (c)]<br><br>Part 2<br><br>Three independent equilibrium equations are available from the FBD of member ABD, and three from the FBD of member CDB, which gives a total of six independent equilibrium equations (recall that the FBD for the entire frame is not independent of the FBDs for its two composite members). The total number of unknowns is seven: two unknowns each at A, C, and D and one unknown at B.<br><br>Because the number of unknowns exceeds the number of independent equilibrium equations, we conclude that this problem is statically indeterminate; that is, all unknowns cannot be determined from equilibrium analysis alone.<br><br>Sample Problem 4.13<br><br>(1) Draw the FBDs for the entire frame in Fig. (a) and for each of its parts. The weights of the members are negligible. The cable at C is attached directly to the pin. (2) Determine the total number of unknowns and the total number of independent equilibrium equations, assuming that P is known.<br><br>R = 1 ft<br><br>4 ft 4 ft<br><br>y<br><br>E<br><br>A B C<br><br>x<br><br>5 ft<br><br>P<br><br>(a)<br><br>D<br><br>E<br><br>A B<br><br>C<br><br>5 ft<br><br>P<br><br>(b)<br><br>5 ft 3 ft Ay<br><br>Ax<br><br>T1<br><br>NE<br><br>D<br><br>Solution<br><br>Part 1<br><br>The forces on each of the FBDs are described in the following. FBD of Entire Frame—Fig. (b)<br><br>P: applied force Ax and Ay: components of force exerted on the frame by pin A (directions are<br><br>assumed)|
|---|

###### 186

|NE: force exerted on the frame by the roller E (direction is horizontal, assumed<br><br>acting to the right)<br><br>T1: force exerted on the frame by the cable that is attached to pin C<br><br>FBD of Member EDC—Fig. (c)<br><br>NE: force exerted on member EDC by the roller at E [must be shown acting in the<br><br>same direction as in Fig. (b)]<br><br>Dx and Dy: components of the force exerted on member EDC by pin D (directions<br><br>are assumed)<br><br>NE<br><br>Dy<br><br>E<br><br>C Cy<br><br>Cx<br><br>4 ft 4 ft<br><br>5 ft<br><br>(c)<br><br>Dx D<br><br>D<br><br>Dx<br><br>Dy<br><br>T2 P<br><br>R = 1 ft<br><br>(d)<br><br>Ax<br><br>Ay<br><br>A<br><br>T2<br><br>B<br><br>3 ft 5 ft<br><br>(e)<br><br>Cy<br><br>C Cx<br><br>Cx<br><br>C<br><br>|1 x<br><br>|y|
|---|---|
|C| |
<br><br>T<br><br>(f)<br><br>Cx<br><br>Cy<br><br>Cx and Cy: components of the force exerted on member EDC by pin C (directions<br><br>are assumed)<br><br>FBD of the Pulley—Fig. (d)<br><br>P: applied force Dx and Dy: components of the force exerted on the pulley by pin D [must be<br><br>shown equal and opposite to the corresponding components in Fig. (c)]<br><br>T2: tension in the cable on the left side of the pulley<br><br><br>FBD of Member ABC—Fig. (e)<br><br>Ax and Ay: components of the force exerted on member ABC by pin A [must be<br><br>shown acting in the same directions as in Fig. (b)]<br><br>T2: force exerted on member ABC by the cable that is attached at B [must be equal<br><br>and opposite to the corresponding force in Fig. (d)]<br><br>C x and C y: components of the force exerted on member ABC by pin C (directions<br><br>are assumed)<br><br>FBD of Pin C—Fig. (f) This FBD is necessary because a cable is attached directly to pin C.<br><br>T1: force exerted on pin C by the cable [must be shown acting in the same direction<br><br>as in Fig. (b)]<br><br>Cx and Cy: components of the force exerted on pin C by member EDC [must be shown equal and opposite to the corresponding components in Fig. (c)]<br><br>C x and C y: components of the force exerted on pin C by member ABC [must be shown equal and opposite to the corresponding components in Fig. (e)]<br><br>Part 2<br><br>There are a total of eleven independent equilibrium equations: three for each of the two bars, three for the pulley, and two for pin C (the force system acting on the pin is concurrent, coplanar). Recall that the FBD for the entire frame is not independent of the FBDs of its members.<br><br>The problem is statically determinate because the total number of unknowns is also eleven: Ax and Ay, Cx and Cy, C x and C y, Dx and Dy, NE, T1, and T2.|
|---|

![image 28](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile28.png>)

###### Problems

For Probs. 4.61–4.68, (a) draw the free-body diagrams for the entire assembly (or structure) and each of its parts. Neglect friction and the weights of the members unless speciﬁed otherwise. Be sure to indicate all relevant dimensions. For each problem, (b) determine the total number of unknown forces and the total number of independent equilibrium equations.

1 m 1 m

###### F

D

1 m

500 N

500 N

###### E

C

1 m

500 N

A

B

(a)

(b)

(c)

###### Fig. P4.61

1 ft 4 ft

1.8 ft

B

###### A

100 lb

1.8 ft

100 lb 100 lb

(b)

(c)

(a)

###### Fig. P4.62

Force in spring is 100 lb tension

C

D

D

B

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |

12 in.

10 in.

B

F

20°

###### A D

6 in.

A

| | |
|---|---|
|B|0.8 m|

3 in.

A

1.8 m

200 lb

0.4 m

8 in.

25 kN

###### Fig. P4.63 Fig. P4.64 Fig. P4.65

4.61–4.72 Problems 189

Friction

- B

D

- C

###### C B

5 in.

Cable

- 3 ft
- 4 ft

A

85 mm

1 ft 2 ft

150 lb .in.

16in.

A

D

300N.m

| | |
|---|---|
| | |
| | |

200lb.ft

12 in.

8 in.

A

C B D

100 mm

2 ft 3 ft

###### Fig. P4.66 Fig. P4.67 Fig. P4.68

- 4.69 The ﬂuid control valve D is controlled by the ﬂoat A. Draw FBDs for the ﬂoat-arm assembly ABC, the link CE, the support arm BD, and the assembly composed of all three of these components. The upward thrust on the ﬂoat is 2.4lb. Neglect the weights of the components. Assume that all dimensions are known.

C

B

E

D

A

2.4 lb

###### Fig. P4.69

###### 4.70 Draw the FBDs for the following: (a) bar ABC with pin A inside the bar; (b) bar ABC with pin A removed; and (c) pin A. Neglect the weights of the members.

3.6 m

D

30° 45°

A C

B

2.4 kN

###### Fig. P4.70

- 4.71 Tension in the spring connecting the two arms of the lifting tongs is 150lb. Draw the FBDs of (a) the entire assembly; (b) the pin A; (c) the arm ABD with pin A removed; and (d) the 60-lb block. Neglect the weight of the tongs.

A

B

E D

C

|60 lb|
|---|

10 in.

16 in.

16 in.

1200 lb

1.5 ft

2.5 ft

E

B D

A

5 ft

1.5 ft

Fig. P4.71 Fig. P4.72

- 4.72 For the structure shown, draw the following FBDs: (a) the entire structure; (b) the small pulley at D; and (c) the frame ADE.

###### 4.8 Equilibrium Analysis of Composite Bodies

In the equilibrium analysis of a composite body and its various parts, you must be able to construct the appropriate FBDs. As explained in the previous article, this ability depends on the correct application of Newton’s third law. Furthermore, you must be able to write and solve equilibrium equations based on FBDs, a technique that was explained for one-body problems in Art. 4.6. The primary difference between one-body and composite-body problems is that the latter often require that you analyze more than one FBD.

The problems in the preceding article required the construction of FBDs for a composite body and each of its parts. These problems were simply exercises in the drawing of FBDs. Beginning an equilibrium analysis by constructing all possible FBDs is inefﬁcient; in fact, it can lead to confusion. You should begin by drawing the FBD of the entire body and, if possible, calculate the external reactions. Then, and only then, should you consider the analysis of one or more parts of the body. The advantages of this technique are the following: First, because only external reactions appear on the FBD of the entire body, some or all of them can often be calculated without referring to internal forces. A second advantage is that FBDs are drawn only as needed, thereby reducing the amount of labor. Most of the time it will not be necessary to draw all possible FBDs and compute all internal reactions in order to ﬁnd the desired unknowns. Knowing which FBDs to draw and what equations to write are undoubtedly the most difﬁcult parts of equilibrium analysis.

|Sample Problem 4.14<br><br>The structure in Fig. (a) is loaded by the 240-lb·in. counterclockwise couple<br><br>30°<br><br>4<br><br>4<br><br>3<br><br>3<br><br>240 lb . in.<br><br>B<br><br>C<br><br>D<br><br>A<br><br>(a)<br><br>5in.<br><br>5in.<br><br>5in.<br><br>y<br><br>x<br><br>30°<br><br>240 lb . in.<br><br>B<br><br>C<br><br>D<br><br>A<br><br>(b)<br><br>Ay<br><br>Ax<br><br>ND<br><br>4 in.<br><br>4 in.<br><br>4 in.<br><br>TC<br><br>30°<br><br>3 in.<br><br>B<br><br>C<br><br>D<br><br>(c)<br><br>3 in.<br><br>4 in.<br><br>4 in.<br><br>By<br><br>Bx<br><br>TC<br><br>ND<br><br>applied to member AB. Neglecting the weights of the members, determine all forces acting on member BCD.<br><br>Solution<br><br>The solution of a problem involving a composite body such as this must be approached with caution. Unless an efﬁcient method of analysis is planned from the outset, it is easy to be overwhelmed by the number of FBDs that can be drawn and the number of equilibrium equations that can be written.<br><br>Method of Analysis<br><br>Although not absolutely necessary, considering the FBD of the entire structure is often a good starting point. The FBD shown in Fig. (b) contains the four unknowns ND, TC, Ax, and Ay. With four unknowns and three independent equilibrium equations (general coplanar force system), we cannot determine all unknowns on this FBD (one more independent equation is required). Therefore, without writing a single equation from the FBD in Fig. (b), we turn our attention to another FBD.<br><br>Because we are seeking the forces acting on member BCD, let us next consider its FBD, shown in Fig. (c). This FBD contains four unknowns: ND, TC, Bx, and By. Again there are only three independent equations (general coplanar force system), but a study of Fig. (c) reveals that the equation MB =0 will relate the unknowns ND and TC. Additionally, from Fig. (b) we see that ND and TC are also related by the equation MA = 0. Therefore, these two moment equations can be solved simultaneously for ND and TC. After those two unknowns have been found, the calculation of Bx and By, which are the remaining unknown forces acting on BCD, is straightforward.<br><br>Mathematical Details<br><br>Referring to the FBD of the entire structure in Fig. (b),<br><br>MA =0 + TC cos30◦(8) − ND(12) + 240 = 0<br><br>ND =0.5774 TC + 20 (a) From the FBD of member BCD in Fig. (c),<br><br>MB =0 + TC cos30◦(4) + TC sin30◦(3) − 8 ND =0<br><br>ND =0.6205 TC (b) Solving Eqs. (a) and (b) simultaneously yields<br><br>TC =464 lb and ND =288 lb Answer Also from the FBD of member BCD in Fig. (c),<br><br>Fx =0 −→+ ND − TC cos30◦ + Bx =0 Bx =464cos30◦ − 288=114 lb Answer|
|---|

|and<br><br>Fy =0 +  By − TC sin30◦ =0 By =464sin30◦ =232 lb Answer<br><br>Because the solution yields positive numbers for the unknowns, each force is directed as shown on the FBDs.<br><br>The FBD of member AB, although not required in the foregoing analysis, is shown in Fig. (d).<br><br>240 lb . in. 4 in.<br><br>B<br><br>A<br><br>(d)<br><br>3 in. Ay<br><br>Ax<br><br>By<br><br>Bx<br><br>Other Methods of Analysis<br><br>Note that the FBDs for the two members that make up the structure, Figs. (c) and (d), contain a total of six unknowns: Ax, Ay, Bx, By, ND, and TC. There are also six independent equilibrium equations—three for each member. (Thus you see that it is not absolutely necessary to use the FBD of the entire assembly.) There are many combinations of equations that could be used to determine the forces acting on member BCD. It is recommended that you practice your skills by outlining one or more additional methods of analysis.<br><br>Sample Problem 4.15<br><br>An 80-N box is placed on a folding table as shown in Fig. (a). Neglecting friction and the weights of the members, determine all forces acting on member EFG and the tension in the cable connecting points B and D.<br><br>(a)<br><br>400<br><br>400 200 600<br><br>360<br><br>240<br><br>G<br><br>H<br><br>F<br><br>C<br><br>180<br><br>B D E<br><br>80 N A<br><br>Dimensions in mm<br><br>400<br><br>y<br><br>x<br><br>Solution<br><br>Method of Analysis<br><br>We begin by considering the FBD of the entire table, Fig. (b). Because this FBD contains three unknowns (NG, Hx, and Hy), it will be possible to compute all of them from this FBD. In particular, NG can be found using the equation MH =0.|
|---|

|800<br><br>(b)<br><br>600<br><br>NG Hy<br><br>H Hx<br><br>80 N<br><br>G<br><br>(c)<br><br>1200<br><br>Ey<br><br>80 N<br><br>Ay<br><br>400<br><br>Ax A E Ex<br><br>Next, we turn our attention to the FBD of member EFG by skipping ahead to Fig. (d). We note that there are ﬁve unknowns on this FBD (NG, Fx, Fy, Ex, and Ey). Although we have already found a way to ﬁnd NG, four unknowns remainwith only three independent equations.<br><br>Therefore, without writing any equations for the time being, we consider another FBD—the FBD of the tabletop, shown in Fig. (c). Although this FBD also contains four unknown forces, we see that three of them (Ax, Ay, and Ex) pass through point A. Therefore, the fourth force, Ey, which is one of the forces we are seeking, can be determined from the equation MA =0.<br><br>Having computed Ey, only three unknowns remain on the FBD in Fig. (d). These unknowns can now be readily found by using the three available equilibrium equations.<br><br>Thus far, our analysis has explained how to determine the ﬁve forces acting on member EFG. All that remains is to ﬁnd the tension in the cable connected between B and D. This force has not yet appeared on any of the FBDs, so we must draw another FBD.<br><br>Ey<br><br>E Ex<br><br>Ey<br><br>E Ex<br><br>Fy<br><br>Fx<br><br>NG<br><br>F<br><br>G<br><br>(d)<br><br>400 600<br><br>360<br><br>240<br><br>Cy<br><br>C Cx<br><br>TBD D<br><br>600<br><br>(e)<br><br>180<br><br>We choose to draw the FBD of the right half of the tabletop, shown in Fig. (e). The right half is chosen instead of the left because the pin reactions at E have already been determined. With Ex and Ey previously found, the remaining three unknowns (Cx, Cy, and TBD) can be computed. In particular, the tension TBD can be found from the equation MC =0.<br><br>Note that we did not ﬁnd it necessary to draw the FBD for member AFH or for the left half of the tabletop.|
|---|

|Mathematical Details<br><br>From the FBD of the entire table, Fig. (b),<br><br>MH =0 + 80(600) − NG(800)=0 (a)<br><br>NG =60 N Answer From the FBD of the tabletop, Fig. (c),<br><br>MA =0 + − 80(400) + Ey(1200)=0 (b)<br><br>Ey =26.67 N Answer From the FBD of member EFG, Fig. (d),<br><br>MF =0 + Ex(360) − Ey(600) − NG(400)=0 (c)<br><br>Ex(360)=26.67(600) + 60(400)<br><br>Ex =111.12 N Answer<br><br>Fx =0 −→+ Fx − Ex =0 (d)<br><br>Fx = Ex =111.12 N Answer<br><br>Fy =0 +  NG − Fy − Ey =0 (e)<br><br>Fy =60 − 26.67=33.33 N Answer<br><br><br><br><br>From the FBD of the right half of the tabletop, Fig. (e),<br><br>MC =0 + Ey(600) − Ex(180) + TBD(180)=0 (f)<br><br>TBD(180)=111.12(180) − 26.67(600)<br><br>TBD =22.22 N Answer<br><br>Other Methods of Analysis<br><br>Our analysis was based on the six independent equilibrium equations, Eqs. (a)–(f). For a structure as complex as the one shown in Fig. (a), there are many other methods of analysis that could be used. For example, a different set of equations would result if we chose to consider the left side of the tabletop instead of the right, as was done in Fig. (e).|
|---|

![image 29](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile29.png>)

###### Problems

- 4.73 The beam consists of two bars connected by a pin at B. Neglecting the weight of the beam, compute the support reactions at A.

A

B

C 1.8 m 1.2 m

3 kN/m

Fig. P4.73

- 4.74 For the frame shown, determine the magnitude of the pin reaction at B. Neglect the weight of the frame.

A

B

C

3m

1.8m

2m

15kN/m

12kN/m

Fig. P4.74

- 4.75 The structure consists of two identical bars joined by a pin at B. Neglecting the weights of the bars, ﬁnd the magnitude of the pin reaction at C.

B

200mm

200mm

25°

45° 80 kg

45°

A

C

###### Fig. P4.75

4.76 The bars AB and AC are joined by a pin at A and a horizontal cable. The vertical cable carrying the 200-kg mass is attached to the pin at A. Determine the tension in the horizontal cable. Neglect the weights of the bars.

###### A

30°

60°

3m

2m

###### B C

200 kg

###### Fig. P4.76

###### 200 400 4.77 Neglecting the weights of the members, determine the magnitude of the

pin reaction at D when the frame is loaded by the 200-N·m couple.

A B

- 4.78 The bars AB and BC of the structure are each of length L and weigh W and 2W, respectively. Find the tension in cable DE in terms of W, L, and the angle θ.

A C

B

W 2W

D

L

/2

L

/2

L

/2

L

/2

E

θ θ

2 ft

6 ft 6 ft

6 ft

A 6 ft

D

B

P P

Fig. P4.78 Fig. P4.79

- 4.79 Determine the magnitude of the pin reaction at A as a function of P. The weights of the members are negligible.
- 4.80 Neglecting friction and the weights of the members, compute the magni-

300500

200 N . m

D E

200

F

Dimensions in mm

Fig. P4.77

0.6 m

300 N/m

B

A

C

1.2 m

tudes of the pin reactions at A and C for the folding table shown.

D E

4.81 When activated by the force P, the gripper on a robotic arm is able to pick up objects by applying the gripping force F. Given that P =120 N, calculate the gripping force for the position shown.

0.8 m 0.8 m

Fig. P4.80

160 mm 250 mm

52 mm

B

°

65 A

C

D

F

°

35

P

F

###### Fig. P4.81

- 4.82 Determine the axle loads (normal forces at A, B, and C) for the ore hauler when it is parked on a horizontal roadway with its brakes off. The masses of the cab and the trailer are 4000kg and 6000kg, respectively, with centers of gravity at D and E. Assume that the connection at F is equivalent to a smooth pin.

1m

2m

0.6m

E

2.4 m

F

D

A B C

1.5m

7 in.

4 in.

11 in.

13 in.

P

C

B

A

D E

40°

Fig. P4.82 Fig. P4.83

- 4.83 Determine the force P that would produce a tensile force of 25lb in the cable at E. Neglect the weights of the members.
- 4.84 Determine the force P that will keep the pulley system in equilibrium.

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |

P A

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |

| | |
|---|---|
|1800 lb| |

B

Neglect the weights of the pulleys. Fig. P4.84

- 4.85 Determine the contact force between the smooth 200-lb ball B and the horizontal bar, and the magnitude of the pin reaction at A. Neglect the weights of the bar and the pulley.

D

###### C B

A

7 ft 2 ft

###### Fig. P4.85

4.86 Compute the tension in the cable and the contact force at the smooth sur-

###### C B

face B when the 300-N · m couple is applied to the cylinder. Neglect the weights of the members.

85 mm

- 4.87 The weights and lengths of the two homogeneous beams that make up the structure are shown in the ﬁgure. Determine the magnitude of the pin reaction at B.

A

B

C

50°

6ft 300lb

9 ft 540 lb

Fig. P4.87

- 4.88 Determine the tension in the cable at B, given that the uniform cylinder

###### A

D

| | |
|---|---|
| | |
| | |

300 N.m

100 mm

Fig. P4.86

B

3ft

weighs 350lb. Neglect friction and the weight of bar AB.

C

- 4.89 The masses of the frictionless cylinders A and B are 2.0kg and 1.0kg, respectively. The smallest value of the force P that will lift cylinder A off the horizontal surface is 55.5N. Calculate the radius R of the cylinder B.

A B

20mm

R P

9 ft

12 ft

18 ft 12 ft

A B

200 lb/ft

C D

E

9 ft F

Fig. P4.89 Fig. P4.90

- 4.90 Neglecting the weight of the frame, ﬁnd the tension in cable CD.
- 4.91 Determine the clamping force at A due to the 15-lb horizontal force

10.5ft

D

40° A

Fig. P4.88

15 lb

E

24

C

B

D A

3.75

applied to the handle at E.

5.5 12 3

4.92 Compute the tension in the cable BD when the 165-lb man stands 5ft off the ground, as shown. The weight of the stepladder and friction may be neglected.

Dimensions in inches

Fig. P4.91

300 mm

- A
- B
- C

600 N

###### C

300 mm

3 ft

200 mm 400 mm

B D

600 N

5 ft 4.5 ft

400 mm

E

A

2 ft

2 ft

D

###### Fig. P4.92 Fig. P4.93

- 4.93 Calculate the reactions at the built-in support at C, neglecting the weights of the members.
- 4.94 In the angular motion ampliﬁer shown, the oscillatory motion of AC is

30°

60°

120 mm

36 N·m

C0

C

| | |
|---|---|
|B| |

A

B

Fig. P4.94

ampliﬁed by the oscillatory motion of BC. Neglecting friction and the weights of the members, determine the output torque C0, given that the input torque is 36 N · m.

- 4.95 The linkage of the braking system consists of the pedal arm DAB, the connecting rod BC, and the hydraulic cylinder C. At what angle θ will the force Q be four times greater than the force P applied to the pedal? Neglect friction and the weight of the linkage.

100 mm

100 mm

B

C

A

θ

θ

D

250 mm

Q

P

C

170 lb 190 lb

10 ft 4 ft

A B

D

30 lb

2 ft

Fig. P4.95 Fig. P4.96

- 4.96 The window washers A and B support themselves and the 30-lb uniform plank CD by pulling down on the two ropes. Determine (a) the tension in each rope; and (b) the vertical force that each man exerts on the plank.

- 4.97 The ﬁgure shows a wire cutter. Determine the cutting force on the wire at A when the 75-N forces are applied to the handgrips. (Hint: The horizontal components of pin forces at B and D are zero due to symmetry.)

75 N

75 N Dimensions in mm

E D

A B C

27 80 24 72

Fig. P4.97

- 4.98 Find the tension T in the cable when the 180-N force is applied to the pedal at E. Neglect friction and the weights of the parts.

45°

240mm

B 180 N

T

A

C

E

Cable

D

45°

100mm

100mm

|E D| |
|---|---|
|400 kg| |
|1.4 m| |

4 m

A

C

B

1.6 m

1.1 m

1.4 m

Fig. P4.98 Fig. P4.99

- 4.99 The 400-kg drum is held by tongs of negligible mass. Determine the magnitude of the contact force between the drum and the tongs at D.

###### 4.9 Special Cases: Two-Force and Three-Force

###### Bodies

Up to this point, we have been emphasizing a general approach to the solution of equilibrium problems. Special cases, with the exception of equal and opposite pin reactions, have been avoided so as not to interfere with our discussion of the general principles of equilibrium analysis. Here we study two special cases that can simplify the solution of some problems.

###### a. Two-force bodies

The analysis of bodies held in equilibrium by only two forces is greatly simpliﬁed by the application of the following principle.

Two-Force Principle If a body is held in equilibrium by two forces, the forces must be equal in magnitude and oppositely directed along the same line of action.

To prove the two-force principle, consider the body in Fig. 4.9 (a) that is held in equilibrium by the two forces PA and PB (the forces do not have to be coplanar). From the equilibrium equation F=0 we get PA =−PB. That is, the forces must be equal in magnitude and of opposite sense; they must form a couple. Because the second equilibrium equation, MO =0 (O is an arbitrary point), requires the magnitude of the couple to be zero, PA and PB must be collinear. We conclude that a two-force body can be in equilibrium only if the two forces are as shown in

- Fig. 4.9(b).

B

A A

PB

PA

P

P

B

(a) (b)

B

A A

B

Fig. 4.9

To illustrate the use of the two-force principle, consider the frame shown in

- Fig. 4.10(a). Neglecting the weights of the members, the FBDs for the entire frame and each of its parts are as shown in Figs. 4.10(b) through (d). There are

1000 lb

1000 lb

1000 lb

B

B

B

Cy

1.5 ft

1.5 ft

1.5 ft

4 ft

4 ft

C

C Cy

C

C

Cx Cx

y 3 ft

3 ft

3 ft

3 ft

Ax Dx

Ax

Dx

###### A

D

x

D

D

A A

Dy

Dy

4 ft

Ay

Ay

(a)

(b)

(c)

(d)

###### Fig. 4.10

six unknowns (Ax, Ay, Cx, Cy, Dx, and Dy) and six independent equilibrium equations (three each for the two members). Therefore, the problem is statically determinate.

An efﬁcient analysis is obtained if we recognize that member AC is a twoforce body; that is, it is held in equilibrium by two forces—one acting at A (Ax and Ay are its components) and the other acting at C (Cx and Cy are its components). Using the two-force principle, we know—without writing any equilibrium equations—that the resultant forces at A and C are equal in magnitude and oppositely directed along the line joining A and C. The magnitude of these forces is labeled PAC in Fig. 4.11 .

###### PAC

4 ft

Therefore, if we recognize that AC is a two-force body, either of the FBDs in Fig. 4.12 can be used to replace the FBDs in Fig. 4.10. Because each of the FBDs in Fig. 4.12 contains three unknowns (PAC, Dx, and Dy) and provides us with three independent equilibrium equations, either could be solved completely.

###### C

3

3 ft

4

A

1000 lb

1000 lb

B

B

PAC

1.5 ft

1.5 ft

Fig. 4.11

4 ft

C

C

###### PAC

3 4

3 ft

3 ft

3 ft

3 4

Dx A

Dx

D

D

PAC

Dy

Dy

(a)

(b)

###### Fig. 4.12

It is not absolutely necessary to identify two-force bodies when solving equilibrium problems. However, applying the two-force principle always reduces the number of equilibrium equations that must be used (from six to three, in the preceding example). This simpliﬁcation is invariably convenient, particularly in the analysis of complicated problems.

###### b. Three-force bodies

The analysis of a body held in equilibrium by three forces can be facilitated by applying the following principle.

Three-Force Principle Three non-parallel, coplanar forces that hold a body in equilibrium must be concurrent.

The proof of this principle can be obtained by referring to Fig. 4.13, which shows a body subjected to the three non-parallel, coplanar forces PA, PB, and PC. Because the forces are not parallel, two of them—say, PA and PB—must intersect at some point, such as O. For the body to be in equilibrium, we must have

PB

B

PC

C

O

PA A

###### Fig. 4.13

MO =0. Therefore, the third force, PC, must also pass through O, as shown in Fig. 4.13. This completes the proof of the principle.

As an example of the use of the three-force principle, consider once again the frame shown in Fig. 4.10. We have already shown how the analysis is simpliﬁed by recognizing that member AC is a two-force body. A further simpliﬁcation can be made if we utilize the fact that member BCD is a three-force body.

The FBD of member BCD, repeated in Fig. 4.14(a), shows that the member is held in equilibrium by three non-parallel, coplanar forces. Knowing that the three forces must be concurrent, we could draw the FBD of BCD as shown in Fig. 4.14(b). Because the 1000-lb force and PAC intersect at point E, the pin reaction at D must also pass through that point. Therefore, the two components Dx and Dy can be replaced by a force RD with the slope 11/4.

2 ft 2 ft

1000 lb

B 1000 lb

B

E

1.5 ft

1.5 ft

C C

PAC 4 ft

###### PAC 11

4 ft

4

Dx

D

D

RD

Dy

(a)

(b)

###### Fig. 4.14

Observe that the FBD in Fig. 4.14(a) contains three unknowns (PAC, Dx, and Dy) and that there are three independent equilibrium equations (general coplanar force system). The FBD in Fig. 4.14(b) contains two unknowns (PAC and RD), and there are two independent equilibrium equations (concurrent, coplanar force system). By recognizing that BCD is a three-force body, we reduce both the number of unknowns and the number of independent equilibrium equations by one.

The use of the three-force principle can be helpful in the solution of some problems. However, it is not always beneﬁcial, because complicated trigonometry may be required to locate the point where the three forces intersect.

|Sample Problem 4.16<br><br>Determine the pin reactions at A and all forces acting on member DEF of the 2.5 m 2.5 m frame shown in Fig. (a). Neglect the weights of the members and use the two-force<br><br>1 m<br>2 m<br><br><br>1 m<br><br>1 m E<br><br>B 3 m<br>C D<br><br><br>40 kN<br><br>(a)<br><br>0.5 m<br><br>y<br><br>x<br><br>A F<br><br>3 m<br><br>B<br>C D<br><br><br>E<br><br>A F<br><br>40 kN<br><br>(b)<br><br>Ax<br><br>Ay Fy<br><br>Fx<br><br>5 m<br><br>D<br>E<br><br><br>F<br><br>(c)<br><br>Fy<br><br>Fx<br><br>3 m<br><br>1 m<br><br>PCD<br><br>PBE<br><br>5<br><br>2<br><br>29<br><br>principle wherever applicable.<br><br>Solution<br><br>Method of Analysis<br><br>We begin by considering the FBD of the entire frame, Fig. (b). Because there are only three independent equilibrium equations, it will not be possible to ﬁnd all four unknowns (Ax, Ay, Fx, and Fy) from this FBD alone. However it is possible to compute Fy from MA =0, because it is the only unknown force that has a moment about point A. Similarly, MF =0 will give Ay. To calculate Ax and Fx, we must consider the FBD of at least one member of the frame.<br><br>Note that members CD and BE are two-force bodies, because the only forces acting on them are the pin reactions at each end (the weights of the members are neglected). Therefore, the FBD of member DEF is as shown in Fig. (c). The forces PCD and PBE act along the lines CD and BE, respectively, as determined by the two-force principle. With Fy having been previously computed, the remaining three unknowns in the FBD (PCD, PBE, and Fx) can then be calculated. Returning to the FBD of the entire frame, Fig. (b), we can then ﬁnd Ax from Fx =0.<br><br>Mathematical Details<br><br>From the FBD of the entire frame, Fig. (b),<br><br>MA =0 + −40(3) + Fy(5)=0<br><br>Fy =24.0 kN Answer MF =0 + −40(3) + Ay(5)=0<br><br>Ay = − 24.0 kN Answer From the FBD of member DEF, Fig. (c),<br><br>Fy =0 +  Fy −<br><br>2 √29<br><br>PBE =0<br><br>PBE =<br><br>√29 2<br><br>(24.0)=64.6 kN Answer<br><br>MF =0 + PCD(4) +<br><br>5 √29<br><br>PBE(3)=0<br><br>PCD = −<br><br>15 4√29<br><br>(64.6)= − 45.0 kN Answer<br><br>Fx =0 −→+ − PCD −<br><br>5 √29<br><br>PBE + Fx =0<br><br>Fx =<br><br>5 √29<br><br>(64.6) + (−45.0) = 15.0 kN Answer|
|---|

|From the FBD of the entire frame, Fig. (b),<br><br>Fx =0 −→+ Ax + Fx + 40.0=0 Ax = − 15.0 − 40.0= − 55.0 kN Answer<br><br>Other Methods of Analysis<br><br>There are, of course, many other methods of analysis that could be used. For example, we could analyze the FBDs of the members ABC and DEF, without considering the FBD of the entire frame.<br><br>Sample Problem 4.17<br><br>Neglecting the weights of the members in Fig. (a), determine the forces acting on the cylinder at A and B. Apply the two-force and three-force principles where appropriate. Use two methods of solution: utilizing (1) conventional equilibrium equations; and (2) the force triangle.<br><br>20 lb<br><br>3.5 in.<br><br>2 in. 2 in.<br><br>R<br><br>=2.5in. B A<br><br>(a)<br><br>y<br><br>x<br><br>C<br><br>20 lb<br><br>B A<br><br>(b)<br><br>1<br><br>1 2<br><br>2 in. 2.5 in.<br><br><br>θ<br><br>θ<br><br>θ<br><br>RA<br><br>PBC<br><br>a<br><br>O<br><br>C<br><br>2 in.<br><br>3.5in.<br><br>Solution<br><br>We begin by drawing the FBD of the cylinder, Fig. (b). Because bar BC is acted upon only by the pin reactions at its ends, it is a two-force body. Therefore, the force at B, labeled PBC, is directed along the line BC. The point where the line of action of PBC intersects the 20-lb force is labeled O.<br><br>Next, we note that the cylinder is acted on by three forces: PBC, the 20-lb applied force, and the pin reaction RA. From the three-force principle, the line of action of RA must also pass through point O, as shown in Fig. (b).|
|---|

###### 205

|The angles θ1 and θ2, locating the lines of action of PBC and RA, respectively, can be found from trigonometry. Referring to Fig. (b), we obtain<br><br>θ1 = tan−1<br><br>3.5 2 =60.3◦<br><br>a =(2 + 2.5)tanθ1 =4.5tan60.3◦ =7.89 in.<br><br>θ2 = tan−1<br><br><br>a<br><br>2.5 = tan−1<br><br>7.89 2.5 =72.4◦<br><br>Part 1<br><br>The force system acting on the cylinder is concurrent and coplanar, yielding two independent equilibrium equations. Therefore, referring to the FBD in Fig. (b), the unknowns PBC and RA can be determined as follows:<br><br>Fx =0 −→+ −PBC cosθ1 + RA cosθ2 =0<br><br>RA =<br><br>cosθ1<br><br>cosθ2<br><br><br>PBC =<br><br>cos60.3◦ cos72.4◦<br><br>PBC RA =1.639PBC (a)<br><br>Fy =0 +  −PBC sinθ1 + RA sinθ2 − 20=0 −PBC sin60.3◦ + RA sin72.4◦ − 20=0 (b)<br><br><br>Solving Eqs. (a) and (b) simultaneously yields<br><br>RA = 47.2 lb and PBC = 28.8 lb Answer<br><br>Part 2<br><br>Because the three forces acting on the cylinder are concurrent, the unknowns PBC and RA can be found by applying the law of sines to the force triangle in Fig. (c).<br><br>(c)<br><br>θ<br><br>θ<br><br>θ α<br><br>γ<br><br>20 lb<br><br>RA<br><br>PBC<br><br>1 = 60.3°<br><br>2 = 72.4°<br><br>3<br><br>β<br><br>The angles in Fig. (c) are computed as follows:<br><br>α = 72.4◦ − 60.3◦ =12.1◦<br><br>θ3 = 90◦ − 60.3◦ =29.7◦ β = 180◦ − θ3 =180◦ − 29.7◦ =150.3◦ γ = 180◦ − (α + β)=180◦ − (12.1◦ + 150.3◦)=17.6◦<br><br>Applying the law of sines, we obtain 20 sinα =<br><br>RA<br><br>sinβ =<br><br>PBC sinγ<br><br>Substituting the values for α, β, and γ into this equation yields the same values for PBC and RA as given in Part 1.<br><br>The force triangle that results from the application of the three-force principle, Fig. (c), can also be solved graphically. If the triangle is drawn to a suitable scale, the unknown forces and angles can be measured directly.|
|---|

![image 30](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile30.png>)

###### Problems

Problems 4.100–4.120 each contain at least one two-force member. Solve by utilizing the two-force principle, where appropriate. If the weight of a body is not speciﬁcally stated, it can be neglected.

- 4.100 Compute the magnitudes of all forces acting on member CDE of the

9 ft

6 ft

6 ft

4 ft

B

C

D

A E

80 kips

Fig. P4.100

frame.

- 4.101 Calculate all forces acting on member CDB.

B

C D

A

2 ft

4 ft

3 ft 3 ft 3 ft

240 lb

Fig. P4.101

- 4.102 The automatic drilling robot must sustain a thrust of 38 lb at the tip of the C E

48 in.

D

B

CA

50°

38 lb A

70°

54 in. 30 in.

Fig. P4.102

drill bit. Determine the couple CA that must be developed by the electric motor to resist this thrust.

- 4.103 Determine the clamping (vertical) force applied by the tongs at E.

| | | |
|---|---|---|
|A<br><br>70°<br><br>70°| | |
| | | |

3 in.

10 in.

200 lb

F

D

B C

E

3 in.

Fig. P4.103

- 4.104 The two disks are connected by the bar AB and the smooth peg in the slot at D. Compute the magnitude of the pin reaction at A.

A

B

30° D

###### E

C

6 N ·m 150 mm

###### Fig. P4.104

###### 4.105 Neglecting friction, determine the relationship between P and Q, assum-

ing that the mechanism is in equilibrium in the position shown.

18in.

D C

20°

20°

- 4.106 Calculate the magnitudes of the pin reactions acting on the crane at A and C due to the 5000-lb load.

C

E

8 in. D

8 in.

5000 lb

48 in. 8 in.

B

A

106 in.

18 in.

Fig. P4.106

- 4.107 The load in the bucket of a skid steer loader is 600lb with its center of gravity at G. For the position shown, determine the forces in the hydraulic cylinders AC and DE.

C

D

B

E

F

A

G

Dimensions in inches

20

5 5

25

30

15 50

B

C

D G 0.15

0.24

Dimensions in meters

0.25

0.18

A

0.5

Fig. P4.107 Fig. P4.108

- 4.108 The load in the scoop of an excavator weighs 1.5MN, and its center of gravity is at G. For the position shown, determine the forces in the hydraulic cylinders AB and CD.
- 4.109 The tool shown is used to crimp terminals onto electric wires. The wire

6in.

P

B

| | |
|---|---|
| | |
| | |

20°

A

Q

Fig. P4.105

20 lb

2.6in. 0.4in.

0.6in.

###### D

C

15°

|A|
|---|

B

20 lb

and terminal are inserted into the space D and are squeezed together by the motion of slider A. Compute the magnitude of the crimping force.

Fig. P4.109

- 4.110 The 50-N force is applied to the handle of the toggle cutter. Determine

A

D

E

C

B

Dimensions in mm

50 N

120

25°

90

30

Fig. P4.110

the force exerted by the cutting blade CB on the workpiece E.

- 4.111 The blade of the bulldozer is rigidly attached to a linkage consisting of the arm AB, which is controlled by the hydraulic cylinder BC. There is an identical linkage on the other side of the bulldozer. Determine the magnitudes of the pin reactions at A, B, and C.

A B

C

180 mm

600 kN

1000 mm

1280 kN

500 mm 640 mm

Fig. P4.111

- 4.112 Find the magnitudes of the pin reactions at A, C, and E caused by the

2ft

180lb. ft

60°

A

D

C

E F

B

Fig. P4.112

180-lb·ft couple.

- 4.113 The pins at the end of the retaining-ring spreader ﬁt into holes in a retaining ring. When the handgrip is squeezed, the pins spread the retaining ring, allowing its insertion or removal. Determine the spreading force P caused by the 8-lb forces applied to the handgrip.

Dimensions in inches

Pins

P

P

D

C

A

B

E

0.6

8 lb

8 lb

1.2 2 3.8

Fig. P4.113

- 4.114 When the C-shaped member is suspended from the edge of a friction-

60mm

90mm

###### A

120 mm

G

x

60°

less table, it assumes the position shown. Use a graphical construction to ﬁnd the distance x locating the center of gravity G.

Fig. P4.114

###### 4.115 The center of gravity of the eccentric wheel is at point G. Determine the largest slope angle θ for which the wheel will be at rest on a rough inclined surface.

| | |
|---|---|
|R|G|

R 2

θ

Fig. P4.115

###### 4.116 For the pliers shown, determine the relationship between the magnitudes of the applied forces P and the gripping forces at E.

P

1.5 in. 3 in.

1.5 in.

E

B D

A C

1.2 in.

1 in.

P

Fig. P4.116

###### 4.117 The device shown is an overload prevention mechanism. When the force acting on the smooth peg at D reaches 1.0kN, the peg will be sheared, allowing the jaws at C to open and thereby releasing the eye-bolt. Determine the maximum value of the tension P that can be applied without causing the eyebolt to be released. Neglect friction.

400 120

B

25

150

C A

E

P

P

70

D 20°

Dimensions in mm

Fig. P4.117

###### 4.118 The ﬁgure represents the head of a pole-mounted tree pruner. Determine the force applied by the cutting blade ED on the tree branch when the vertical rope attached at A is pulled with the force P.

A

2

D 40°

E

1.2

1.75

5

P

B

Tree branch

1.0

C

Dimensions in inches

###### Fig. P4.118

∗4.119 The hinge shown is the type used on the doors of some automobiles. If a torsion spring at F applies the constant couple C0 =20 lb · ft to member ABF, calculate the force P required to hold the door open in the position shown.

C

A

B

21in.

21in.

30°

P

30°

90°

90° C

27in.

G

D

0

E

12in.

12in.

H

F

12in.

12in.

###### Fig. P4.119

###### 4.120 Determine the force in the hydraulic cylinder EF that would maintain the parallelogram mechanism in the position shown.

0.6 ft 200 lb

B

3.75ft

D

30°

F

A

0.75 ft

C

2ft

0.75 ft

E

###### Fig. P4.120

Solve Probs. 4.121–4.130, using the two-force and three-force principles where appropriate. Neglect weights of members unless speciﬁed otherwise.

4.121 Determine the horizontal force P that would keep the uniform 15-kg

| |B|
|---|---|
| | |

rectangular plate in the position shown. 4.122 Determine the magnitudes of the forces acting on the bracket at B and C.

P A

120 lb

6.5 in. 4.5 in.

0.4 m

A B

6.5 in.

E 0.3 m D

Fig. P4.121

C

###### Fig. P4.122

B 4.123 Determine the angle θ at which the bar AB is in equilibrium. Neglect

friction.

2m

- 4.124 The automobile, with center of gravity at G, is parked on an 18◦ slope with its brakes off. Determine the height h of the smallest curb that will prevent the automobile from rolling down the plane.

0.5mdia

h B

A

2.6m

0.8m

18°

1.2m

G

30 kg

30°

60°

A B P

Fig. P4.124 Fig. P4.125

- 4.125 Determine the horizontal force P that will keep the 30-kg homogeneous bar AB at rest in the position shown.
- 4.126 The center of gravity of the nonhomogeneous bar AB is located at G. Find the angle θ at which the bar will be in equilibrium if it is free to slide on the frictionless cylindrical surface.

###### C

W A

θ

1 m

Fig. P4.123

8 in. dia

A

θ

G

B

4in.

3in.

###### Fig. P4.126

###### 4.127 When suspended from two cables, the rocket assumes the equilibrium position shown. Determine the distance x that locates G, the center of gravity of the rocket.

|2.5 m|6 m|4 m|
|---|---|---|
|A|x|B|

5 m C D

G

Fig. P4.127

###### 4.128 The pump oiler is operated by pressing on the handle at D, causing the plunger to raise and force out the oil. Determine the distance d of link BC so that the horizontal pin reaction at A is zero.

35

B

A

Plunger

35

C

70

d

P

D

C

Dimensions in mm

35°

Fig. P4.128

B

###### 4.129 The uniform 320-lb bar AB is held in the position shown by the cable

18ft

AC. Compute the tension in the cable.

40°

A

###### 4.130 Find the force P required to (a) push; and (b) pull the 80-lb homogeneous roller over the 3-in. curb.

Fig. P4.129

###### P

###### P

24 in.

20°

20°

3 in.

(a) (b)

###### Fig. P4.130

###### PART C: Analysis of Plane Trusses

###### 4.10 Description of a Truss

A truss is a structure that is made of straight, slender bars that are joined together to form a pattern of triangles. Trusses are usually designed to transmit forces over relatively long spans; common examples are bridge trusses and roof trusses. A typical bridge truss is shown in Fig. 4.15(a).

| |
|---|

(a) (b)

###### Fig. 4.15

The analysis of trusses is based on the following three assumptions:

- 1. The weights of the members are negligible. A truss can be classiﬁed as a lightweight structure, meaning that the weights of its members are generally much smaller than the loads that it is designed to carry.
- 2. All joints are pins. In practice, the members at each joint are usually riveted or welded to a plate, called a gusset plate, as shown in Fig. 4.15(b).

However, if the members at a joint are aligned so that their centroidal axes (axes that pass through the centroids of the cross-sectional areas of the members) intersect at a common point, advanced methods of analysis indicate that the assumption of pins is justiﬁed.

- 3. The applied forces act at the joints. Because the members of a truss are slender, they may fail in bending when subjected to loads applied at locations other than the joints. Therefore, trusses are designed so that the major applied loads act at the joints.

| | |
|---|---|
| | |
| | |

P

P

P P

P P

Although these assumptions may appear to oversimplify the real situation, they lead to results that are adequate in most applications.

Tension

Using the assumptions, the free-body diagram for any member of a truss will contain only two forces—the forces exerted on the member by the pin at each end. Therefore, each member of a truss is a two-force body.

| | |
|---|---|
| | |
| | |

P

P

P P

P P

When dealing with the internal force in a two-force body, engineers commonly distinguish between tension and compression. Figure 4.16 shows the

Compression

external and internal forces in tension and compression. Tensile forces elongate (stretch) the member, whereas compressive forces compress (shorten) it. Because

Fig. 4.16

the forces act along the longitudinal axis of the member, they are often called axial forces. Note that internal forces always occur as equal and opposite pairs on the two faces of an internal cross section.

The two common techniques for computing the internal forces in a truss are the method of joints and the method of sections, each of which is discussed in the following articles.

###### 4.11 Method of Joints

When using the method of joints to calculate the forces in the members of a truss, the equilibrium equations are applied to individual joints (or pins) of the truss. Because the members are two-force bodies, the forces in the FBD of a joint are concurrent. Consequently, two independent equilibrium equations are available for each joint.

To illustrate this method of analysis, consider the truss shown in Fig. 4.17(a). The supports consist of a pin at A and a roller at E (one of the supports is usually designed to be equivalent to a roller, in order to permit the elongation and contraction of the truss with temperature changes).

8000 lb 3000 lb

8000 lb 3000 lb

y

C D

C D

B

B

2

x

8 ft

- A

E A H G F

Ax = 0

H G F E

1 6 ft

6 ft 6 ft 6 ft

Ay = 7500 lb NE = 3500 lb

(b)

(a)

###### Fig. 4.17

###### a. Support reactions

It is usually a good idea to start the analysis by determining the reactions at the supports using the FBD of the entire truss. The FBD of the truss in Fig. 14.17(b) contains three unknown reactions: Ax, Ay, and NE, which can be found from the three available equilibrium equations. The results of the computation are shown in Fig. 4.17(b).

Note that Ax, the horizontal reaction at A, is zero. This result indicates that the truss would be in equilibrium under the given loading even if the pin at A were replaced by a roller. However, we would then have an improper constraint, because an incidental horizontal force would cause the truss to move horizontally. Therefore, a pin support at A (or B) is necessary to properly constrain the truss.

Sometimes the number of unknown reactions on the FBD of the entire truss is greater than three. In this case, all the reactions cannot be found at the outset.

###### b. Equilibrium analysis of joints

Let us now determine the forces in the individual members of the truss in Fig. 4.17. Because the force in a member is internal to the truss, it will appear on a FBD only if the FBD “cuts” the member, thereby separating it from the rest of the truss. For example, to determine the force in members AB and AH, we can draw the FBD of joint A—that is, the portion of the truss encircled by the dashed line 1 in Fig. 4.17(b). This FBD, shown in Fig. 4.18(a), contains the external reactions Ax and Ay and the member forces PAB and PAH (the subscripts identify the member). Note that we have assumed the forces in the members to be tensile. If the solution yields a negative value for a force, the force is compressive. By assuming the members to be in tension, we are using an established convention for which positive results indicate tension and negative results indicate compression.

8000 lb

###### B

PBC

y

x

PAB

PBH

PAB

(b) FBD of joint B

3

4

Ax = 0

A

PAH

Ay = 7500 lb

(a) FBD of joint A

###### Fig. 4.18

Having previously computed Ax and Ay, the forces PAB and PAH are the only unknowns in the FBD for joint A. Therefore, they can be determined from the two independent equilibrium equations for the joint, as follows.

- 4

- 5

Fy =0 +  7500 +

PAB =0

5 4

(7500)= − 9375 lb

PAB = −

3 5

Fx =0 −→+

PAB + PAH + Ax =0

3 5

(−9375) + PAH + 0=0

3 5

(−9375)=5625 lb

PAH = −

The negative value for PAB indicates that the force in member AB is compressive; the positive value for PAH means that the force in member AH is tensile.

To compute the forces in members BC and BH, we draw the FBD of joint

- B—the portion of the truss encircled by the dashed line 2 in Fig. 4.17(b). This FBD is shown in Fig. 4.18(b). Note that the force PAB is equal and opposite to the corresponding force in Fig. 4.18(a), and that we again assumed PBC and PBH to be tensile. Knowing that PAB = − 9375 lb, PBC and PBH are the only unknowns in this FBD. The equilibrium equations of the joint yield

3 5

###### Fx =0 −→+ PBC −

PAB =0

3 5

3 5

(−9375)= − 5625 lb

PBC =

PAB =

- 4

- 5

###### Fy =0 +  −

PAB − PBH − 8000=0

- 4

- 5

PBH = − 8000 −

PAB

- 4

- 5

(−9375)= − 500 lb

= − 8000 −

The negative values indicate that both PBC and PBH are compressive.

We could continue the procedure, moving from joint to joint, until the forces in all the members are determined. In order to show that this is feasible, we count the number of unknowns and the number of independent equilibrium equations:

13 member forces + 3 support reactions = 16 unknowns 8 joints, each yielding 2 equilibrium equations = 16 equations

Because the number of equations equals the number of unknowns, the truss is statically determinate. The three equilibrium equations of the entire truss were not counted, because they are not independent of the joint equilibrium equations (recall that a structure is in equilibrium if each of its components is in equilibrium).

8000 lb

###### B

PBC PAB PBH

###### c. Equilibrium analysis of pins

(b) FBD of pin B

In the above example, the FBD of a joint contained a ﬁnite portion of the truss surrounding the joint. This required “cutting” the members attached to the joint, so that the internal forces in the members would appear on the FBD. An alternative approach, preferred by many engineers, is to draw the FBDs of the “pins,” as illustrated in Fig. 4.19 . In this case, the internal forces in the members appear as Ay = 7500 lb

3

PAB

4

5

Ax = 0

A

PAH

forces acting on the pin. For all practical purposes, the FBDs in Figs. 4.18 and 4.19 are identical. The FBD of a pin is easier to draw, but the FBD of a joint is somewhat more meaningful, particularly when it comes to determining whether the member forces are tensile or compressive.

(a) FBD of pin A

Fig. 4.19

###### d. Zero-force members

There is a special case that occurs frequently enough to warrant special attention. Figure 4.20(a) shows the FBD for joint G of the truss in Fig. 4.17. Because no external loads are applied at G, the joint equilibrium equations Fx =0 and

Fy =0 yield PGH = PGF and PGC =0. Because member GC does not carry a force, it is called a zero-force member. It is easily veriﬁed that the results remain unchanged if member GC is inclined to GH and GF, as shown in Fig. 4.20(b). When analyzing a truss, it is often advantageous to begin by identifying zero-force members, thereby simplifying the solution.

PGC

PGH PGF G

(a) FBD of joint G

PGC

PGH PGF

G

(b)

###### Fig. 4.20

You may wonder why a member, such as GC, is included in the truss if it carries no force. The explanation is the same as the one given for providing a pin support—rather than a roller—at A for the truss in Fig. 4.17(a): It is necessary to ensure the proper constraint of joint G. If member GC were removed, the truss would theoretically remain in equilibrium for the loading shown.* However, the slightest vertical load applied to the joint at G would cause the truss to deform excessively, or even collapse. Moreover, it is unlikely that the loads shown in Fig. 4.17(a) will be the only forces acting on the truss during its lifetime. Should a vertical load be suspended from joint G at some future time, member GC would be essential for equilibrium.

*The word theoretically is to be interpreted as “in accordance with the assumptions.” Our mathematical model for a truss assumes that the weights of the members are negligible. In practice, the force in a so-called zero-force member is not exactly zero but is determined by the weights of the members.

|Sample Problem 4.18<br><br>Using the method of joints, determine the force in each member of the truss shown in Fig. (a). Indicate whether the members are in tension or compression.<br><br>B<br><br>10 kN<br><br>6 m<br><br>3 m 3 m<br><br>60 kN<br><br>A C D<br><br>(a)<br><br>y<br><br>x<br><br>Solution<br><br>The FBD of the entire truss is shown in Fig. (b). The three unknowns (NA, Cx, and Cy) can be computed from the three equilibrium equations<br><br>MC = 0 + − NA(6) + 60(3) − 10(6)=0<br><br>NA =20 kN Fy =0 +  NA − 60 + Cy =0<br><br>Cy =60 − NA =60 − 20=40 kN Fx =0 −→+ 10 − Cx =0<br><br>Cx =10 kN<br><br>We now proceed to the computation of the internal forces by analyzing the FBDs of various pins.<br><br>3 m 3 m<br><br>6 m<br><br>60 kN<br><br>D<br><br>A<br><br>NA<br><br>C Cy<br><br>Cx<br><br>B<br><br>10 kN<br><br>(b)|
|---|

|Method of Analysis<br><br>In the following discussion, the external reactions are treated as knowns, because they have already been calculated. It is convenient to assume the force in each member to be tensile. Therefore, positive values of the forces indicate tension, and negative values denote compression.<br><br>The FBD of pin A, shown in Fig. (c), contains two unknowns: PAB and PAD. We can compute these two forces immediately, because two independent equilibrium equations are available from this FBD.<br><br>The FBD of pin D, in Fig. (d), contains the forces PAD, PBD, and PCD. Because PAD has already been found, we have once again two equations that can be solved for the two unknowns.<br><br>Figure (e) shows the FBD of pin C. With PCD previously found, the only remaining unknown is PBC, which can be easily computed.<br><br>(d)<br><br>PAD<br><br>D<br><br>PBD<br><br>PCD<br><br>60 kN<br><br>1<br><br>5 2<br><br>(e)<br><br>PCD<br><br>PBC<br><br>Cx =10 kN<br><br>Cy = 40 kN<br><br>C<br><br>A<br><br>(c)<br><br>1<br><br>1 PAB<br><br>PAD NA = 20 kN<br><br>2<br><br>Mathematical Details<br><br>From the FBD of pin A, Fig. (c),<br><br>Fy =0 +  1 √2<br><br>PAB + NA =0<br><br>PAB = −<br><br>√<br><br>2(20)= − 28.3 kN<br><br>PAB =28.3 kN (compression) Answer Fx =0 −→+<br><br>1 √2<br><br>PAB + PAD =0<br><br>PAD = −<br><br>1 √2<br><br>PAB = −<br><br>1 √2<br><br>(−28.3)<br><br>= 20.0 kN (tension) Answer<br><br>From the FBD of pin D, Fig. (d),<br><br>Fy =0 +  2 √5<br><br>PBD − 60=0<br><br>PBD =<br><br>√5 2<br><br>(60)=67.1 kN (tension) Answer|
|---|

###### 220

|Fx =0 −→+ − PAD +<br><br>1 √5<br><br>PBD + PCD =0<br><br>PCD = PAD −<br><br>1 √5<br><br>PBD<br><br>PCD =20.0 −<br><br>1 √5<br><br>(67.1)= − 10.0 kN<br><br>PCD =10.0 kN (compression) Answer From the FBD of pin C, Fig. (e),<br><br>Fy =0 +  Cy + PBC =0 PBC = − Cy = − 40 kN PBC =40 kN (compression) Answer<br><br>Note that the equation Fx =0 yields PCD = − 10.0 kN, a value that has been found before. Therefore, this equation is not independent of the equations used previously. The reason for the dependence is that the external reactions were determined by analyzing the FBD of the entire truss. However, the equations for the pins and those for the entire truss are not independent of each other.<br><br>Other Methods of Analysis<br><br>In the preceding analysis, the pins were considered in the following order: A, D, and C (the FBD of pin B was not used). Another sequence that could be used is<br><br>1. FBD of pin A: Calculate PAB and PBD (as before).<br>2. FBD of pin B: With PAB already found, calculate PBD and PBC.<br>3. FBD of pin C: Calculate PCD.<br><br><br>In this analysis, the FBD of pin D would not be used.<br><br>Yet another approach would be to compute the three external reactions and the forces in the ﬁve members (a total of eight unknowns) by using the equilibrium equations for all the pins (a total of eight equations, two for each pin).|
|---|

![image 31](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile31.png>)

###### Problems

###### 4.131–4.140 Using the method of joints, calculate the force in each member of the trusses shown. State whether each member is in tension or compression.

B

6ft

A

A

L L L L

70°

10 ft

A B C

P B

| | | | |
|---|---|---|---|
|E|P<br><br>F|P<br><br>G|P|

8ft

50°

P

L

D H

C

C D

20 ft

###### Fig. P4.131 Fig. P4.132 Fig. P4.133

C

P

E

B

1.5P

B

2 m

8 ft

C

55° A D

35° 35°

E D

A

D

A B C

E

2 m 2 m

6 ft 8 ft 6 ft

8 ft 8 ft

2000 lb 1200 lb

160 kN 160 kN

###### Fig. P4.134 Fig. P4.135 Fig. P4.136

8 kN

C

3000 lb

40°

4 ft

8 kN

C

B

C

200 kN

B

L

30° 60°

6 ft

B

6m

45° 45° 60°

30°

A

E L

A D

A D

8 ft

D

6 m

###### Fig. P4.137 Fig. P4.138 Fig. P4.139

###### 4.131–4.147 Problems 223

- 4.141 Identify all the zero-force members in the four trusses shown.

A 50°

D

C

B

3 m

400 kN

500 kN

2 m

4 m

Fig. P4.140

A A

A

B

B

C

C

D

D

P

P

P

P

P

P

A

B

F

D

E

B

C

C

D

P

E E

E

(a) (b)

(c) (d)

Fig. P4.141

- 4.142 The walkway ABC of the footbridge is stiffened by adding the cable ADC

2 m A

B

C

G

F

E

D

2 m

2 m 2 m

2 m

2 m

42 kN

Fig. P4.143

and the short post of length L. If the tension in the cable is not to exceed 500lb, what is the smallest value of L for which the 185-lb person can be supported at B?

| | | |
|---|---|---|
|B| |L|

8 ft 8 ft

A

C

D

185 lb

Fig. P4.142

- 4.143 Find the force in member EF.

3 ft 3 ft 3 ft

6 ft

2 ft

4 ft

B C D

F

E

G

H

A

P P

Fig. P4.144

- 4.144 Find the forces in members HC and HG in terms of P.
- 4.145 Determine the reaction at E and the force in each member of the right half of the truss.

5 kN

4 kN

10m

10 kN

10m

8 kN

10m

10m

C

D

B 30°

30°

90°

90°

A 30°

30°

E

F G

###### Fig. P4.145

4.146 Determine the force in member AD of the truss.

8000 lb 8000 lb

15 ft 15 ft

4.147 Determine the force in member BE of the truss.

C

B

E

300 kN

C

40 ft

3 m

D

A

B

D

E

25 ft

25 ft

5 m

400 kN

Fig. P4.146

A

3 m

3 m

###### Fig. P4.147

###### 4.12 Method of Sections

Truss analysis by the method of joints is based on the FBDs of individual joints. Analyzing the free-body diagram of a part of a truss that contains two or more joints is called the method of sections. The FBD for a single joint results in a concurrent, coplanar force system (two independent equilibrium equations). When applying the method of sections, the force system will generally be nonconcurrent, coplanar (three independent equilibrium equations).

In the method of sections, a part of the truss is isolated on an FBD so that it exposes the forces to be computed. If the FBD for the isolated portion contains three unknowns, all of them can usually be computed from the three available equilibrium equations. If the number of unknowns exceeds three, one or more of the unknowns must be found by analyzing a different part of the truss. If you are skillful in writing and solving equilibrium equations, the only challenge in using the method of sections is selecting a convenient part of the truss for the FBD.

Consider once again the truss discussed in the preceding article [its FBD is repeated in Fig. 4.21(a)]. We now use the method of sections to determine the forces in members BC, HC, HG, and DF—each of these members is identiﬁed by two short parallel lines in Fig. 4.21(a).

Assuming that the external reactions have been previously computed, the ﬁrst and most important step is the selection of the part of the truss to be analyzed. We note that the section labeled 1 in Fig. 4.21(a) passes through members BC, HC, and HG. The forces in these three members are the only unknowns if the FBD is drawn for a part of the truss that is isolated by this section. Note that after the section has been chosen, the portion of the truss on either side of the cut may be used for the FBD. The forces inside the members occur in equal and opposite pairs, so the same results will be obtained regardless of which part is analyzed. Of course, given a choice, one would naturally select the less complicated part.

###### 4.12 Method of Sections 225

8000 lb 3000 lb

1

C D

B

8 ft

- Ax = 0

2

6 ft 6 ft 6 ft

(b)

PBC

8000 lb

B

A H

- Ay = 7500 lb

A H G F E

6 ft

Ay = 7500 lb NE = 3500 lb

(a)

PDC

###### C

D

y

x

PHC

8 ft

5 4

PDF

3

6 ft

Ax = 0

E

PHG

PEF

NE = 3500 lb

(c)

###### Fig. 4.21

For our truss, using either the portion to the left or to the right of section 1 is equally convenient. For no particular reason, we choose to analyze the left portion, with its FBD shown in Fig. 4.21(b) (we have again assumed the members to be in tension). Note that the force system is nonconcurrent and coplanar, so that any set of three independent equations can be used to compute the three unknown forces.

The following is an efﬁcient method of solution.

Fy =0—determines PHC, because PBC and PHG have no y-components MH =0—determines PBC, because PHC and PHG have no moment about

point H

MC =0—determines PHG, because PBC and PHC have no moment about point C The details of this analysis are as follows:

Fy =0 +  4 5

PHC − 8000 + 7500 = 0

5 4

(8000 − 7500)

PHC =

=625 lb (tension) Answer

MH =0 + − 7500(6) − PBC(8)=0

PBC = − 5625 lb

=5625 lb (compression) Answer

MC =0 + 8000(6) − 7500(12) + PHG(8)=0

1 8[7500(12) − 8000(6)]

PHG =

=5250 lb (tension) Answer

To determine the force in member DF by the method of sections, consider once again the FBD of the entire truss in Fig. 4.21(a). Our intention is to isolate a part of the truss by cutting only three members, one of which is the member DF. It can be seen that section 2 accomplishes this task. We choose to analyze the part to the right of this section because it contains fewer forces. The FBD is shown in Fig. 4.21(c), with the unknown forces again assumed to be tensile. Note that PDF can be computed from the equation

Fy =0 +  3500 − PDF =0

PDF =3500 lb (tension) Answer

If desired, PEF could now be calculated using MD =0, and ME =0 would give PDC.

As you see, the forces in the members of a truss can be found by either the method of joints or the method of sections. Selecting the method that results in the most straightforward analysis is usually not difﬁcult. For example, for the truss shown in Fig. 4.21(a), the FBD of joint A is convenient for computing PAB, whereas the method of sections is more advantageous for calculating PBC.

|Sample Problem 4.19<br><br>Using the method of sections, determine the forces in the following members of the truss in Fig. (a): FI and JC. Indicate tension or compression.<br><br>6ft6ft6ft<br><br>3000 lb 1000 lb<br><br>4 ft 4 ft<br><br>A<br>B<br>C<br><br><br>E D<br><br>I H<br><br>F<br><br>G<br><br>J<br>K<br><br><br>4 ft<br><br>y<br><br>(a)<br><br>x<br><br>Solution<br><br>The FBD of the entire truss is shown in Fig. (b). The three external reactions<br><br>3000 lb 1000 lb<br><br>PDE = 2000 lb<br><br>B<br><br>A<br><br>C<br><br><br>D<br><br>F<br><br>G<br><br>I H<br>J<br><br><br>4 ft K<br><br>4 ft 4 ft<br><br>6ft6ft<br><br>6ft<br><br>Ax =<br><br>Ay = 4000 lb<br><br>2000 lb<br><br>(b)<br><br>1<br><br>2<br><br>(Ax, Ay, and PDE) can be calculated using the following equations (mathematical details have been omitted):<br><br>MA = 0 gives PDE = 2000 lb<br><br>Fx = 0 gives Ax = 2000 lb<br>Fy = 0 gives Ay = 4000 lb<br><br><br>These forces are shown in Fig. (b), and from now on we treat them as known quantities.<br><br>Member FI Method of Analysis<br><br>Referring to the FBD in Fig. (b), it can be seen that section 1 cuts through members FD, FI, and HI. Because there are three equilibrium equations available for a portion of the truss separated by this section, we could ﬁnd the forces in all three members.<br><br>Mathematical Details<br><br>Having chosen section 1, we must now decide which portion of the truss to analyze. We select the portion lying to the right of the section, because it is somewhat|
|---|

6ft

###### 227

|less complicated than the portion on the left. Of course, identical results will be obtained regardless of which part of the truss is analyzed.<br><br>The FBD for the part of the truss lying to the right of section 1 is shown in Fig. (c), with the three unknowns being PFD, PFI, and PHI. Any set of three independent equations can be used to solve for these unknowns. A convenient solution that yields PFI directly is the following:<br><br>MG = 0 gives PFI, because PFD and PHI pass through point G.<br><br>+ 3000(4) +<br><br>3 5<br><br>PFI(8)=0 PFI = −2500 lb<br><br>= 2500 lb (compression) Answer<br><br>Note: The moment of PFI about point G was computed by replacing PFI with its x- and y-components acting at point I.<br><br>3<br><br>4<br><br>5<br><br>PFD<br><br>|PFI<br><br>4 ft<br><br>3ft|4 ft|
|---|---|
|PHI<br><br>3000 lb|1000 lb<br><br>H|
<br><br>P<br><br>F<br><br>G<br><br>5<br><br><br>4<br><br>3<br><br>I<br><br>(c)<br><br>Member JC Method of Analysis<br><br>In Fig. (b), section 2 passes through only three members, one of which is member JC. Therefore, we can ﬁnd the force in that member (and the forces in the other two members if desired) from one FBD.<br><br>Mathematical Details<br><br>The FBD for the portion of the truss lying below section 2 is shown in Fig. (d).<br><br>3<br><br>13 2<br><br>Ax = 2000 lb<br><br>Ay = 4000 lb<br><br>A<br>B<br><br><br>PBC PJC PIJ<br><br>(d)<br><br>K<br><br>J<br><br>The three unknowns are PBC, PJC, and PIJ. The force PJC can be obtained from the following equation:<br><br>Fx =0 −→+ Ax −<br><br>2 √13<br><br>PJC =0<br><br>PJC =<br><br>√13 2<br><br>Ax =<br><br>√13 2<br><br>(2000)<br><br>=3610 lb (tension) Answer|
|---|

###### 228

![image 32](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile32.png>)

###### Problems

- 4.148 Show that all diagonal members of the truss carry the same force, and ﬁnd the magnitude of this force.

|A B C D| | | |
|---|---|---|---|
|F|G|H|I|
| | | | |

4 m

4 panels @ 3 m = 12 m

P E

J

Fig. P4.148, P4.149

- 4.149 Determine the forces in members FG and AB in terms of P.
- 4.150 Determine the forces in members BC, BG, and FG.

A

D

C

E F G H

B 8 ft

4000 lb 6000 lb 8000 lb

8 ft 8 ft 8 ft 8 ft

Fig. P4.150

- 4.151 Find the forces in members BC and DE.

6200 lb

- 3 ft
- 4 ft

A

D

B C

E

9 ft 9 ft

Fig. P4.151

- 4.152 Compute the forces in members EF, NF, and NO.

A

B

C D E F G

H

I

300 kN 8 panels @ 5 m = 40 m

K L M N O P Q

J

6.25

6.0

5.5

4.5

3

R

Dimensions in meters

Fig. P4.152, P4.153

- 4.153 Repeat Prob. 4.152 assuming that the 300-kN force is applied atO instead of L.
- 4.154 Determine the forces in members BG, CI, and CD.

| | | | |
|---|---|---|---|
|F G H I| | | |

P

a a a a

a

F J

A

B C D E

Fig. P4.154, P4.155

- 4.155 Assuming that P =48000 lb and that it may be applied at any joint on the line FJ, determine the location of P that would cause (a) maximum tension in

member HI; (b) maximum compression in member CI; and (c) maximum tension in member CI. Also determine the magnitude of the indicated force in each case.

- 4.156 Determine the angle θ that maximizes the tensile force in member BC and calculate the maximum value of this force.

2 m A

B

C

G

F

E

θ

D

2 m

2 m 2 m

2 m

2 m

42 kN

Fig. P4.156

- 4.157 Find the forces in members CD, DH, and HI.

A

B C D E

F

G

H

I

12 ft

720 lb 1440 lb 1440 lb 720 lb

8 ft 8 ft 8 ft 8 ft 6 ft

5 kN 4 kN 3 kN 2 kN

4 m

A B C D E

F

3 m 3 m 3 m 3 m

Fig. P4.157 Fig. P4.158

- 4.158 Determine the forces in members CD and DF.
- 4.159 Compute the forces in members CD and JK, given that P =3000 lb and

P Q

2 ft

2 ft

H

E

|A|F|
|---|---|
|B|G<br><br>|
|C<br><br>D| |

Q

- I

3 ft

- J

3 ft

Q

3 ft

Q =1000 lb. (Hint: Use the section indicated by the dashed line.)

K

- 4.160 If PCD =6000 lb and PGD =1000 lb (both compression), ﬁnd P and Q.
- 4.161 Determine the forces in members BC, CE, and FG.

Fig. P4.159, P4.160

560 lb 560 lb 560 lb 3 ft 3 ft 3 ft

A

B C D

2 ft

4 ft

E

H G

F

###### Fig. P4.161

- 4.162 Determine the forces in members AC, AD, and DE. A

D

C

F

H

J

E

60 kips

G

I

- K
- L

B

4 @ 4m=16m

5@3m=15m

Fig. P4.162, P4.163

- 4.163 Determine the forces in members GI, FH, and GH.
- 4.164 Determine the forces in members CD, IJ, and NJ of the K-truss in terms of P.

H I J K L

A

a

B

M

P

a

C

P

a

D

P

a

E

P

a

F

P

a

N O Q a G

Fig. P4.164

- 4.165 Determine the largest allowable value for the angle θ if the magnitude of

|A<br>B C<br><br><br>θ θ| |
|---|---|
| | |

D

2P P

Fig. P4.165

the force in member BC is not to exceed 5P.

- 4.166 Find the forces in members BC and BG.

| |F<br><br>|H| |
|---|---|---|---|
| | | | |

A

D

C

P P P

G

E

B

L L L L

L/2 L/2

Fig. P4.166

- 4.167 Determine the forces in members BC and BE and the horizontal pin reaction at G.

A C

|D E<br><br>B|
|---|

G F

12000 lb 16000 lb 12000 lb 8 8 8 8

9

5

Dimensions in feet

A B

C

D

- H

E

F

G 45°

M

L

L

K

J

- I

|W|
|---|

5panels@

L

=5L

Fig. P4.167 Fig. P4.168

- 4.168 A couple acting on the winch at G slowly raises the load W by means of a rope that runs around the pulleys attached to the derrick at A and B. Determine the forces in members EF and KL of the derrick, assuming the diameters of the pulleys and the winch are negligible.

![image 33](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile33.png>)

###### Review of Equations

###### Coplanar equilibrium equations

Fx = Fy = MA = 0 (A arbitrary point) Fx = MA = MB = 0 (x-axis not perpendicular to AB) MA = MB = MC = 0 (A, B and C not collinear)

There are three independent (scalar) equilibrium equations for each body.

###### Free-body diagram

A free-body diagram is a sketch of the body that shows all of the forces and couples (including support reactions) that act upon it.

###### Pin reactions

If two members are joined by a pin, the forces exerted by the pin on the members are equal and opposite, provided that no external force is applied to the pin.

###### Two-force members

If a body is held in equilibrium by two forces, the forces must be equal and opposite.

###### Three-force members

Three non-parallel, coplanar forces that hold a body in equilibrium must be concurrent.

###### Trusses

A truss is a structure that consists of two-force members joined by pins. All external loads are applied to the pins.

![image 34](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile34.png>)

###### Review Problems

- 4.169 The uniform, 20-kg bar is placed between two vertical surfaces.

1.3m

A

B

1.2 m

Fig. P4.169

Assuming sufﬁcient friction at A to support the bar, ﬁnd the magnitudes of the reactions at A and B.

- 4.170 The homogeneous cylinder of weight W and radius R rests in a groove of width 2b. Determine the smallest force P required to roll the cylinder out of the groove. Assume that there is enough friction to prevent slipping.

P W

R

2b

25°

2 m

2.5 m

2 m

5 kN

A

B C

y

x

Fig. P4.170 Fig. P4.171

- 4.171 Determine the magnitude of the pin reaction at A, assuming the weight of bar ABC to be negligible.
- 4.172 Determine the couple C that will hold the bar AB in equilibrium in the

A

C

L

|W|
|---|

B

30°

Fig. P4.172

position shown. Neglect the weight of the bar and the diameter of the small pulley at B.

- 4.173 Calculate the magnitudes of the pin reactions at A, B, and C for the frame shown. Neglect the weights of the members.

80 lb/ft

###### B

5 ft 5 ft

60lb/ft

12ft

A C

###### Fig. P4.173

C

###### 4.174 The weight W =6 kN hangs from the cable which passes over the pulley

at F. Neglecting the weights of the bars and the pulley, determine the magnitude of the pin reaction at D.

1.5 m

B

F

D

- 4.175 The 10-kN and 40-kN forces are applied to the pins at B and C, respectively. Calculate the magnitudes of the pin reactions at A and F. Neglect the weights of the members.

4 m

- 1 m
- 2 m
- 3 m

C

B

A

F

E

D

40 kN

10 kN 1 m

3 m 3 m

2 m

2 m

2 m

3 m

20 kN·m

20 kN·m A

B

D

Fig. P4.175 Fig. P4.176

- 4.176 The two couples act at the midpoints of bars AB and BD. Determine the magnitudes of the pin reactions at A and D. Neglect the weights of the members.
- 4.177 Determine the forces in members AC and AD of the truss.

8 ft

12 ft

10 ft

4 kips

- A
- B

C

- D

F

- E 5 ft

4 ft θ

B

A

L

30°

40°

Fig. P4.177 Fig. P4.178

- 4.178 Determine the angle θ for which the uniform bar of length L and weight W will be in equilibrium. Neglect friction.
- 4.179 Determine the magnitudes of the pin reactions at A, C, and E. Neglect

1.5 m

R = 0.4 m

A E

W

2 m 2 m

Fig. P4.174

- A
- B C

6 ft

2 ft

900 lb.ft

3 ft

D

the weight of the frame. 4.180 Calculate the forces in members (a) DE; (b) BE; and (c) BC. Indicate tension or compression.

E

6 ft

Fig. P4.179

C

P Q

2m

B

2 m 2 m

4 m

B C

4m 4m

D E

2 m

A

60° 60° A D

6 m 3 m 200 kN 100 kN

###### Fig. P4.180 Fig. P4.181

- 4.181 Determine the ratio P/Q for which the parallel linkage will be in equilibrium in the position shown. Neglect the weights of the members.
- 4.182 The 50-lb block C rests on the uniform 20-lb bar AB. The cable con-

2 ft 6 ft

A C B

D

30°

Fig. P4.182

necting C to B passes over a pulley at D. Find the magnitude of the force acting between the block and the bar.

- 4.183 The 30-lb homogeneous bar AB supports the 60-lb block. The ends of the bar rest on frictionless inclines. Determine the distance x for which the bar will be in equilibrium in the position shown.

60° 30°

A B

12 ft

30 lb 60 lb

x

Fig. P4.183

- 4.184 Determine the forces in members (a) BF; and (b) EF. Indicate tension or compression.

8000 lb

3 ft 3 ft

C D

4 ft

E

1500 lb

- A
- B

F

4 ft

6 ft 6 ft

###### Fig. P4.184

4.185 The bar ABC of negligible weight is supported by a pin at A and a rope that runs around the small pulley at D and the 20-lb homogeneous disk. Determine the tension in the rope.

W

6 in.

D

C

D

15in. 9 in.

8 in.

8in. A

B

C

4 in.

B

F G

20 lb

4 in.

A E

15in.

45in.

18 in.

###### Fig. P4.185 Fig. P4.186

4 m 4 m 4 m 4 m

- 4.186 The breaking strength of the cable FG that supports the portable camping stool is 400lb. Determine the maximum weight W that can be supported. Neglect friction and the weights of the members.
- 4.187 For the truss shown, determine the forces in members (a) BD; and (b) BF.

A B C

| | | |
|---|---|---|
|E F|G|H|

6 m

D

- 4.188 The 80-N force is applied to the handle of the embosser at E. Determine the resulting normal force exerted on the workpiece at D. Neglect the weights of the members.

80 N E

A C

B

D

15°

130 50

40

Dimensions in mm

Fig. P4.188

- 4.189 The tongs shown are designed for lifting blocks of ice. If the weight of

20 kN 20 kN 20 kN

Fig. P4.187

W

12 in.

A

15 in.

B

7 in.

D C

4 in. 4 in.

the ice block is W, ﬁnd the horizontal force between the tongs and the ice block at C and D.

W

Fig. P4.189

# 5

### Three-Dimensional Equilibrium

![image 35](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile35.png>)

Analysis of three-dimensional structures relies heavily on vector algebra. The determination of forces in even a simple space structure, such as the tripod shown here, requires the use of vector analysis. prism_68/Shutterstock

###### 5.1 Introduction

In this chapter, we discuss the analysis of bodies that are held in equilibrium by three-dimensional force systems. The emphasis on free-body diagrams and the number of independent equations, begun in Chapter 4, is continued here.

In the analysis of coplanar force systems, there was little advantage in using vector notation. This is not true for equilibrium analysis in three dimensions, where vector notation frequently has a decided advantage over scalar notation.

###### 237

###### 5.2 Deﬁnition of Equilibrium

By deﬁnition, a body is in equilibrium if the resultant of the force system acting on the body vanishes. A general force system can always be reduced to an equivalent force-couple system R = F and CR = MO (where O is any point). Therefore, for a body to be in equilibrium, the following two vector equations must be satisﬁed:

###### F = 0 MO = 0 (5.1)

The equivalent six scalar equations are

Fx = 0 Fy = 0 Fz = 0 Mx = 0 My = 0 Mz = 0

(5.2)

where the x-, y-, and z-axes are assumed to intersect at point O. It is important to recall that the summations must be taken over all forces acting on the body, including the support reactions.

###### 5.3 Free-Body Diagrams

Our study of coplanar equilibrium in Chapter 4 demonstrated the importance of correctly drawn free-body diagrams (FBDs) in the solution of equilibrium problems. To extend the free-body diagram concept to problems in which the loads are not coplanar we must again investigate the reactions that are applied by the various connections and supports.

As mentioned in Chapter 4, the reactions that a connection is capable of exerting on the body can be derived from the following rule: A support that prevents translation in a given direction must apply a force in that direction and a support that prevents rotation about an axis must apply a couple about that axis. Some common supports are illustrated in Table 5.1 and are described in the following paragraphs.

- (a) Flexible Cable (Negligible Weight). A ﬂexible cable can exert a tensile force only in the direction of the cable. (With the weight of the cable neglected, the cable can be shown as a straight line.) Assuming that the direction of the cable is known, the removal of a cable introduces one unknown in the free-body diagram—the magnitude of the tension.
- (b) Spherical Roller or Single Point of Contact on Frictionless Surface. A spherical roller, or a frictionless surface with a single point of contact, can exert only a force that acts normal to the surface. Consequently, the magnitude of the force is the only unknown.
- (c) Cylindrical Roller on Friction Surface, or on Guide Rail. A cylindrical roller placed on a friction surface can exert a force that is normal to the surface and

- a friction force that is perpendicular to the plane of the roller. If a cylindrical roller is placed on a guide rail, the force perpendicular to the plane of the roller is provided by the side of the guide rail. In either case, two unknowns are introduced in the FBD.
- (d) Ball-and-Socket Joint. A ball-and-socket joint prevents translational movement but not rotation. Therefore, a connection of this type exerts an unknown force, usually shown as three independent components; it does not apply a couple.
- (e) Friction Surface: Single Point of Contact. A friction surface in contact with a body at one point can exert an unknown force, acting through the point of contact. This force is usually shown as three components—a normal force and two components of the friction force acting parallel to the surface.

Before describing the hinge and bearing supports, shown in Table 5.1 parts

- (f) and (g), it is necessary to discuss how these supports are designed and used in practice.

a

C

R

A hinge and a thrust bearing are illustrated in Fig 5.1(a) and 5.1(b), respec-

a

tively. Each of these can exert both a force and a couple on the body it supports. Because hinges and bearings prevent translation completely, the force R can act in any direction. As these connections are designed to allow rotation about the a-a axis, the reactive couple-vector C is always perpendicular to that axis. However, hinges and bearings are seldom strong enough to exert the couples without failure. Consequently, they must be arranged so that the reactive couples are not needed to support the body. For this reason, we consider all hinges and bearings capable of providing only reactive forces.

(a)

To further illustrate the physical reasoning behind omitting couples at hinges and bearings, consider the door shown in Fig. 5.2. If the door is supported by a single hinge, as shown in Fig. 5.2(a), the reactive couple CA is essential for equilibrium; otherwise the moment equation MA = 0 could not be satisﬁed. However, we know from experience that this is not the way to suspend a door if we expect it to last for any length of time. The screws used to attach the hinge to the door and doorframe would soon pull out as a result of the large forces that are necessary to provide the couple CA. Figure 5.2(b) shows the conventional method for supporting a door. Two hinges are aligned along a common axis with the hinge at B assumed to be free to slide, so that it does not provide an axial thrust—that is, a force along the axis of the hinge. The FBD shows that equilibrium can be

C

a

R

a

(b)

Fig. 5.1

A Ax

A Ax

|CA|y|
|---|---|
| |W<br><br>A|
| | |

| |y|
|---|---|
| |W B<br><br>A|
| | |

| |A|
|---|---|
| | |
| | |

| |A<br>B<br>|
|---|---|
| | |
| | |
| | |
| | |

Bx

FBD

FBD

(b)

(a)

###### Fig. 5.2

|Support|Reaction(s)|Description of reaction(s)|Number of unknowns|
|---|---|---|---|
|(a)<br><br>Flexible cable of negligible weight<br><br>|T|Tension of unknown magnitude T in the direction of cable|One|
|(b)<br><br>Spherical roller on any surface or a single point of contact on frictionless surface<br><br>|N<br><br>|Force of unknown magnitude N directed normal to the surface|One|
|(c)<br><br>Cylindrical roller on friction surface or guide rail<br><br>|N<br><br>F<br><br>|Force of unknown magnitude N normal to the surface and a force of unknown magnitude F in the direction of the axis of the roller|Two|
|(d)<br><br>Ball-and-socket joint<br><br>z<br><br>y x<br><br>|Rz<br><br>Rx<br><br>Ry<br><br>|Unknown force R|Three|
|(e)<br><br>Single point of contact on friction surface<br><br>z<br><br>y x|N<br><br>Fx<br><br>Fy<br><br>|Force of unknown magnitude N normal to the surface and an unknown friction force F in the plane of the surface|Three|

###### Table 5.1 Common Supports for Three-Dimensional Loading (Table continues on p. 241.)

|Support|Reaction(s)|Description of reaction(s)|Number of unknowns|
|---|---|---|---|
|(f)<br><br>Slider (radial) bearing or hinge<br><br>z<br><br>y x<br><br>|Rz<br><br>Ry<br>Rz<br><br><br>Ry<br><br>|Unknown force R directed normal to the axis of the bearing or hinge|Two|
|(g)<br><br>Thrust bearing or hinge<br><br>z<br><br>y x<br><br>|Rz<br><br>Ry Rz<br><br>Ry<br><br>Rx<br><br>Rx<br><br>|Unknown force R|Three|
|(h)<br><br>Universal joint<br><br>z<br><br>y x<br><br>Axis<br><br>|Rz<br><br>Rx<br><br>Ry<br><br>C<br><br>|Unknown force R and a couple-vector of unknown magnitude C directed along the axis of the joint|Four|
|(i)<br><br>Built-in (cantilever) support<br><br>z<br><br>y x|Rx<br><br>Cx Rz<br><br>Ry Cy<br><br>Cz|Unknown force R and an unknown couple-vector C|Six|

###### Table 5.1 (continued)

satisﬁed without developing reactive couples at the hinges. The reactive couple, identiﬁed as CA in Fig. 5.2(a), is now provided by the reactive forces Ax and Bx in Fig. 5.2(b). Any small misalignment between the axes of the hinges, which could also give rise to reactive couples, is usually accommodated by the slack that is present in most hinges and bearings.

- (f) Slider Bearing or Hinge. A slider bearing, or slider hinge, can exert only a force normal to the axis of the shaft passing through it. Therefore, two unknown force components are introduced into the FBD by this support. A slider bearing is also called a radial bearing, because it is designed to carry loads acting in the radial direction only.
- (g) Thrust Bearing or Hinge. In thrust bearings and thrust hinges, the sliding motion of the shaft along its axis is prevented by an end cap or equivalent

- support. Consequently, this type of support results in three unknown force components on an FBD. The force component Rx, acting parallel to the axis of the shaft, is called the axial thrust.
- (h) Universal Joint. A universal joint prevents all translation, and rotation about the axis of the joint. A universal joint can, therefore, apply an unknown force, usually shown as three independent components, and a couple-vector acting along the axis of the joint. Consequently, four unknowns are introduced.
- (i) Built-in (Cantilever) Support. A built-in support, also called a cantilever support, prevents all translational and rotational movement of the body. Therefore, the support can exert an unknown force and an unknown couple-vector, introducing six unknowns in the FBD.

The procedure for constructing a free-body diagram involving a threedimensional force system is identical to that used for a coplanar force system:

- 1. A sketch of the body (or part of a body) is drawn with all supports removed.
- 2. All applied forces are shown on the sketch.
- 3. The reactions are shown for each support that was removed.

When analyzing connected bodies, it is again important that you adhere to Newton’s third law: For every action, there is an equal and opposite reaction.

If a problem contains two-force members, the FBD can be simpliﬁed considerably by recalling the two-force principle: Two forces in equilibrium must be equal, opposite, and collinear. This principle is illustrated in Fig. 5.3. The bar in Fig. 5.3(a) is supported by a ball-and-socket joint at each end and is not subjected to any forces other than the joint reactions (the weight is assumed negligible). The FBD of the bar, Fig. 5.3(b), shows the joint reactions—one force at A with components Ax, Ay, and Az and the other at B with components Bx, By, and Bz. Therefore, we see that the bar is a two-force member. After invoking the two-force principle, the FBD of the bar simpliﬁes to that shown in Fig. 5.3(c)—the forces at A and B are equal, opposite, and collinear.

Bz

P

By

z

B

B

B

Bx

A Ax Ay

A

A x y

P

Az (b)

(a)

(c)

###### Fig. 5.3

|Sample Problem 5.1<br><br>The 2-Mg uniform pole in Fig. (a) is supported by a ball-and-socket joint at O and two cables. Draw the FBD for the pole, and determine the number of unknowns.<br><br>y<br><br>x<br><br>z<br><br>40 kN<br><br>3 m<br><br>3 m<br><br>2 m<br><br>3 m<br><br>3m<br>4m<br><br><br>1 m<br><br>O<br><br>C<br><br>D<br><br>A<br>B<br><br><br>(a)<br><br>y<br><br>x<br><br>z<br><br>40 kN<br><br>3 m<br><br>3 m<br><br>1 m<br><br>3 m<br><br>3m<br>4m<br><br><br>1 m<br><br>O<br><br>C<br><br>D<br><br>A<br>B<br><br><br>(b)<br><br>1 m<br><br>TBD<br><br>TAC<br><br>G<br><br>W = 19.62 kN<br><br>Ox<br><br>Oz<br><br>Oy<br><br>Solution<br><br>The FBD for the pole is shown in Fig. (b). Observe that, in addition to the 40-kN applied load, the pole is subjected to the following forces:<br><br>• The tensions in the two cables: The magnitudes of the tensions are labeled<br><br>TAC and TBD. Because the direction of each cable is known, the force in each cable introduces only one unknown on the FBD—its magnitude.<br><br>• The reaction at O: Because the support at O is a ball-and-socket joint, the reaction at O is an unknown force, which we show as the three independent components: Ox, Oy, and Oz.<br>• The weight of the pole: The center of gravity is at G, the midpoint of the pole. The weight is<br><br><br>W = mg = (2 × 103 kg)(9.81 m/s2) = 19620 N<br><br>Inspection of Fig. (b) reveals that there are ﬁve unknowns on the FBD: the magnitude of the tension in each of the two cables and the three force components at O.|
|---|

|Sample Problem 5.2<br><br>The 20-lb surveyor’s transit in Fig. (a) is supported by a tripod of negligible<br><br>x<br><br>4 ft<br><br>2 ft 1.5 ft<br><br>2ft<br><br>y<br><br>z<br><br>B<br><br>C<br><br>D<br><br>A<br><br>(a)<br><br>2ft<br><br>weight that is resting on a rough horizontal surface. The legs of the tripod are connected by ball-and-socket joints to the platform supporting the transit. Draw the FBD for the entire assembly using two methods: (1) not recognizing two-force bodies; and (2) recognizing two-force bodies. In each case, determine the number of unknowns. What modiﬁcations to these FBDs are necessary if the weights of the legs are not negligible?<br><br>Solution<br><br>Part 1 Not Recognizing Two-Force Bodies<br><br>The FBD of the entire assembly is shown in Fig. (b). In addition to the weight W of the transit, we show three independent components of the ground reactions at B, C, and D—giving a total of nine unknowns.<br><br>y<br><br>B<br><br>C<br><br>D<br><br>A<br><br>(b)<br><br>Dy<br><br>Dz<br><br>Dx By<br><br>Bx<br><br>Bz Cy<br><br>Cz<br><br>Cx<br><br>W = 20 lb<br><br>2ft<br><br>2ft<br><br>4 ft<br><br>2 ft<br><br>1.5 ft<br><br>x<br><br>B y<br><br>C<br><br>D<br><br>A<br><br>(c)<br><br>PD<br><br>W = 20 lb<br><br>2ft<br><br>2ft<br><br>4 ft<br><br>2 ft<br><br>1.5 ft<br><br>PC<br><br>PB<br><br>x<br><br>Part 2 Recognizing Two-Force Bodies<br><br>When each leg of the tripod is recognized to be a two-force body, the FBD of the assembly can be drawn as shown in Fig. (c). The forces at B, C, and D act in the direction of the corresponding leg of the tripod. Therefore, the three leg reactions are the unknowns.<br><br>If the weights of the legs are not negligible, the FBD in Fig. (b) can be modiﬁed by simply including the weight of each leg. However, the FBD in Fig. (c) cannot be corrected in the same manner. Because the legs are no longer two-force bodies, the forces at B, C, and D cannot be assumed to act in the directions of the respective legs.|
|---|

|Sample Problem 5.3<br><br>The structure shown in Fig. (a) is supported by ball-and-socket joints at O and D, and by a slider bearing at C. The two members OABC and AD, connected by a ball-and-socket joint at A, each weigh 20lb/ft. (1) Draw the FBD for the entire structure, and count the unknowns. (2) Draw the FBD for each of the members, and count the total number of unknowns.<br><br>x<br><br>y<br><br>z 3 ft<br><br>3ft<br><br>O<br><br>A<br><br>3 ft<br><br>D<br><br>C<br><br>3 ft<br><br>2 ft<br><br>(a)<br><br>B<br><br>Solution<br><br>Part 1 FBD for the Entire Structure<br><br>The FBD for the entire structure is shown in Fig. (b); the dimensions have been omitted for the sake of clarity.<br><br>Dx<br><br>Dy<br><br>Dz<br><br>C<br><br>y<br><br>z<br><br>D<br><br>Oz<br><br>Ox<br>Oy<br><br><br>A<br><br>B<br><br>Cx<br><br>Cz<br><br>O<br><br>WBC<br><br>WAD<br><br>(b)<br><br>WAD = 93.8 lb WBC = 60 lb WOB = 100 lb<br><br>x<br><br>WOB<br><br>The weight of the structure is represented by the weights of the segments OB, BC, and AD at their respective midpoints. The weights have been computed by|
|---|

|multiplying the weight per unit length (20lb/ft) by the lengths of the respective segments. (Note that the length of AD is √22 + 32 + 32 = 4.69 ft.)<br><br>In Fig. (b) we also show the reactions at the ball-and-socket joints at O and D. Note that member AD is not a two-force body (because its weight is not negligible), and thus we cannot assume that the force at D acts along the line AD. The FBD includes the two force components exerted on the structure by the slider bearing at C. The FBD of the entire structure in Fig. (b) contains eight unknowns: three forces at O, three forces at D, and two forces at C.<br><br>Part 2 FBD for Each of the Members<br><br>The FBDs for the members OABC and AD are shown in Fig. (c); the dimensions are again omitted for clarity.<br><br>Dz<br><br>Dy Dx<br><br>D<br><br>z<br><br>y Ax<br><br>Az<br><br>Ay<br><br>x<br><br>A<br><br>Oz<br><br>Ox<br>Oy<br><br><br>z<br><br>Az<br><br>A Ay Ax<br><br>100 lb<br><br>60 lb<br><br>B C<br><br>Cz<br><br>y<br><br>(c)<br><br>O<br><br>x Cx<br><br>93.8 lb<br><br>The ball-and-socket reactions at O and D are shown in the same directions as assumed in Fig. (b).<br><br>We must also include the force exerted on each member by the ball-and-socket joint at A [because this force is internal to the FBD of the entire structure, it does not appear in Fig. (b)]. Note that Ax, Ay, and Az must be shown to be equal and opposite on the two members.<br><br>Finally, the reactions at C—shown in the same directions as in Fig. (b)—as well as the weights of the segments are included on the FBDs in Fig. (c).<br><br>When the composite structure is subdivided into its two constituent bodies, the total number of unknowns is eleven—three at O, three at D, three at A, and two at C.|
|---|

5.1–5.12 Problems 247

![image 36](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile36.png>)

###### Problems

- 5.1 Bar AB of negligible weight is supported by a ball-and-socket joint at B and two cables attached at A. Draw the FBD for the bar, recognizing that it is a two-force body. Determine the number of unknowns.
- 5.2 Draw the FBD for the bar described in Prob. 5.1 if the bar is homogeneous and weighs 180lb. Count the unknowns.

y

x

z

B

D

A

C

400 lb

2ft

2.4ft

7ft

4ft

4ft

Fig. P5.1, P5.2

- 5.3 The space truss ABCD in the shape of a tetrahedron is suspended from three

| |B 1.2 m|
|---|---|
| |2 m<br><br>D<br><br>|

A

C

40 kN

15 kN

1.2m

Fig. P5.3, P5.4

vertical links. Assuming that all connections are ball-and-socket joints, draw the FBD of the truss and count the unknowns.

- 5.4 Draw the FBD of the portion BCD of the space truss described in Prob. 5.3. How many unknowns appear on this FBD?
- 5.5 The 600-lb uniform log OGA—G being its center of gravity—is held in the position shown by the two cables and the light bar BG. Draw the FBD for the log, assuming friction at all contact surfaces and noting that BG is a two-force body. Count the unknowns.

z

A

18 ft

G

12ft

B

10ft

D

O

14ft

10ft

8ft

y x

C

###### Fig. P5.5

###### 5.6 The bar ABCD of negligible weight is supported by a slider bearing at A, a thrust bearing at D, and the cable BE. Draw the FBD and count the unknowns.

###### z

200200

| | | | |
|---|---|---|---|
| | | | |

O

y

A

- D
- E

###### B

22in.

30°

100

300 N

B

A

100 N

12 in.

28in.

z

Dimensions in mm

C

x y

60 lb

x

###### Fig. P5.6 Fig. P5.7

- 5.7 The shaft-pulley assembly is supported by the universal joint at O and by the slider bearing at A. The pulley, which has a mass of 7kg, is subjected to the belt tensions shown. The mass of the shaft may be neglected. Draw an FBD that consists of the pulley and shaft AO. Determine the number of unknowns on this FBD.
- 5.8 The 30-kg homogeneous door is supported by hinges at A and B, with only

z

the hinge at B being capable of providing axial thrust. The cable CD prevents the door from fully opening when it is pulled by the 200-N force acting perpendicular to the door. Draw the FBD for the door, and count the unknowns.

880

45°

D

360

C

880

B

5.9 Draw the FBD for bar BCD. The connections at A and B are ball-and-socket joints, C is a slider bearing, and D is a thrust bearing. Assume that the weights of members are negligible and recognize that AB is a two-force member. How many unknowns appear on the FBD?

200

900

200 N

A

E

z

360

y

D

770

100

x

1180

A

25

C

40N.m

x

Dimensions in mm

70

y

Fig. P5.8

110

40

B

Dimensions in mm

###### Fig. P5.9

- 5.10 The T-bar AEBF is connected to rod CD, with the joint at F being equivalent to a slider bearing. The supports at A and C are slider bearings, and thrust bearings are found at B and D. The two applied forces, which act at the midpoint of the arm EF, are parallel to the y- and z-axes, respectively. Neglecting

36 in.

z

y

E

B

A

C

30 in. 40 in.

D

60 lb

40 lb

42 in.

x

F

Fig. P5.10

the weights of the members, draw the FBDs for the entire structure, the T-bar, and rod CD. Determine the total number of unknowns.

- 5.11 The L-shaped rod, supported by slider bearings at A and B, passes through a hole in the cantilever beam DE. Draw the FBDs for the entire assembly and for its two parts. Determine the total number of unknowns. Neglect the weights of the components.

| |38 in. 24 in.<br><br>E| |
|---|---|---|
|20in.<br><br>| | |

x

y

z

A 18 in. B 20 in. 80 lb

D

24in.

60 lb

100 lb

Fig. P5.11

- 5.12 Draw the FBD for the space truss assuming all connections to be ball-andsocket joints. How many unknowns are there?

z

E

G

10 kN

F

6m

A 12 kN

6m

6m 6m

C

B

D

x y

###### Fig. P5.12

###### 5.4 Independent Equilibrium Equations

###### a. General case

The equilibrium equations for a body subjected to a three-dimensional force system have been given in Art 5.2:

###### F = 0 MO = 0 (5.1, repeated)

where O is an arbitrary point. If O is the origin of the x, y, and z coordinate axes, the equivalent scalar equations are

Fx = 0 Fy = 0 Fz = 0 Mx = 0 My = 0 Mz = 0

(5.2, repeated)

As was the case for coplanar force systems, alternate sets of independent equilibrium equations can be used in place of the above equations. Regrettably, the restrictions ensuring the independence of the equations for three-dimensional force systems are so numerous (and often fairly complicated) that a complete listing of the restrictions is of little practical value. It is much better to rely on logic rather than a long list of complex rules.

As an example of an alternate set of independent equilibrium equations, consider the six scalar moment equilibrium equations that result from summing the moments about two arbitrary points, say A and B. If these six equations are satisﬁed, there can be no resultant couple. However, there could still be a resultant force R = F with the line of action passing through points A and B. Therefore, only ﬁve of the moment equations are independent. An additional scalar equation (a carefully chosen force or moment equation) must be used to guarantee that R vanishes.

When considering a three-dimensional force system, remember that the number of independent scalar equations is six. Although various combinations of force and moment equations may be used, at least three must be moment equations. The reason is that couples do not appear in force equations, so that the only way to guarantee that the resultant couple vanishes is to satisfy three independent moment equations of equilibrium. However, if properly chosen, the six independent equations could be three force and three moment equations, two force and four moment equations, one force and ﬁve moment equations, or even six moment equations.

Three special cases, occurring frequently enough to warrant special attention, are discussed in the next three sections and summarized in Fig. 5.4.

###### b. Concurrent force system

In Chapter 3 the resultant of a concurrent force system was found to be a force R passing through the point of concurrency. The components of R were given by Rx = Fx, Ry = Fy, and Rz = Fz. It follows that there are only three independent equilibrium equations:

###### Fx = 0 Fy = 0 Fz = 0 (5.3)

The x-, y-, and z-axes do not have to be the coordinate axes; they can represent any three arbitrary directions, not necessarily perpendicular.

Note that the six independent equations for the general case are reduced to three for this special case. Alternate sets of equations are one moment and two force equations, one force and two moment equations, or three moment equations, each with its own restrictions to ensure independence.

|Type of force system| |No. of independent equil. eqs.|A set of independent equations|
|---|---|---|---|
|General|z<br><br>F2<br><br>F3<br><br>y<br><br>x<br><br>F1<br><br>O|Six|Fx = 0 Fy = 0 Fz = 0 Mx = 0 My = 0 Mz = 0<br><br>Σ<br><br>Σ<br><br>Σ Σ<br><br>Σ Σ|
|Concurrent|z<br><br>y<br><br>x<br><br>F1 F2<br><br>O F3|Three|Fx = 0 Fy = 0 Fz = 0<br><br>Σ Σ Σ|
|Parallel|z<br><br>O<br><br>F2<br><br>x<br><br>y<br><br>F3 F1<br><br>|Three|Fz = 0 Mx = 0 My = 0<br><br>Σ Σ Σ|
|All forces intersect an axis|z<br><br>x<br><br>y O<br><br>F2<br><br>F1 F3|Five|Fx = 0 Fy = 0 Fz = 0 Mx = 0 Mz = 0<br><br>Σ Σ Σ Σ Σ|

###### Fig. 5.4

###### c. Parallel force system

It has been shown in Chapter 3 that, if all the forces are parallel to the z-axis, the resultant is either a force parallel to the z-axis or a couple-vector perpendicular to the z-axis. Therefore, the number of independent equilibrium equations is again reduced to three.

###### Fz = 0 Mx = 0 My = 0 (5.4)

The force equation eliminates the possibility of a resultant force, and the two moment equations ensure that there is no resultant couple.

In Eqs. (5.4), the moments can be summed about any two axes that lie in the xy plane. The three equations in Eqs. (5.4) can be replaced by three moment equations, with various restrictions required to guarantee their independence.

###### d. All forces intersect an axis

If all the forces intersect an axis—say, the y-axis, as shown in Fig. 5.4—the moment equation My = 0 is trivially satisﬁed, and we are left with the following ﬁve independent equilibrium equations.

Fx = 0 Fy = 0 Fz = 0 Mx = 0 Mz = 0

(5.5)

Of course, alternate sets of independent equations can be used—two force and three moment equations, one force and four moment equations, or ﬁve moment equations.

###### 5.5 Improper Constraints

Even if the number of equilibrium equations equals the number of unknowns, we cannot always conclude that a solution exists. As we have mentioned several times, this is the predicament when the equilibrium equations are not independent. In such a case, the fault lies with the analyst who chooses the equations, not with the physical problem. But another situation exists in which the problem itself precludes a solution of the equilibrium equations; it is known as the case of improper constraints.

As an example of improper constraints, consider the plate of weight W suspended from six parallel wires and pushed by the horizontal force P, as shown in Fig. 5.5(a). The free-body diagram of the plate shows that there are six unknowns (the forces in the wires). Because the two equations Fy =0 and Mz = 0 are trivially satisﬁed, the number of independent equilibrium equations is reduced to four in this case. Moreover, the equation Fx =0 yields P =0. From all this we conclude that the plate can be in equilibrium in the position shown only if P =0, and then the problem is statically indeterminate (there are three equilibrium equations left with six unknowns).

The trouble with this problem is that the supports are not capable of resisting the applied load P in the given position; that is, they cannot provide the proper constraints that prevent motion. We encounter this situation whenever the support reactions form one of the special cases described in the preceding article: concurrent, parallel (as in the present example), or intersecting a common axis. An example of the latter is shown in Fig. 5.5(b), in which the plate of weight W is supported by three sliding hinges. Again we have six unknown reactions and ostensibly six independent equilibrium equations, but equilibrium is clearly impossible in the position shown, unless P =0.

In summary, the support constraints are said to be improper if they are not capable of supporting an arbitrary load system (this does not preclude equilibrium under certain loads, e.g., when P =0 in the examples shown in Fig. 5.5).

###### 5.6 Writing and Solving Equilibrium Equations 253

z

Cz

Bz

Cy

T1

- Ay
- Az By

C B

C B

T6

W

T2

A

A

T5

P

P

T3

T4

P y

W

P

x

FBD

FBD

(b)

(a)

###### Fig. 5.5

###### 5.6 Writing and Solving Equilibrium Equations

The steps in the analysis of three-dimensional equilibrium problems are identical to those we used in coplanar analysis.

- 1. Draw the free-body diagrams (FBDs).
- 2. Write the equilibrium equations.
- 3. Solve the equations for the unknowns.

The ﬁrst step, the construction of FBDs, was discussed in Art 5.3. In this article we assume that the FBDs are given, permitting us to concentrate on the second and third steps—writing and solving the equilibrium equations.

The solution of three-dimensional problems requires careful planning before any equilibrium equations are written. As recommended in Chapter 4, you should prepare a method of analysis or plan of attack that speciﬁes the equations to be written and identiﬁes the unknowns that appear in the equations. Comparing the number of unknowns with the number of independent equilibrium equations lets you determine if the problem is statically determinate or indeterminate. With a stated plan, you are able to maintain control of the solution; without it, you can easily be overwhelmed with the complexity of the problem. After you adopt a workable method of analysis, you can then proceed to the mathematical details of the solution.

In the solution of coplanar equilibrium problems, the method of analysis frequently centers on a moment equation. The idea is to ﬁnd a moment center A so that the equation MA =0 involves the fewest possible number of unknowns (ideally only one unknown). This strategy is also convenient for analyzing threedimensional problems. In most problems, you should look for moment equations that simplify the solution. A moment equation about an axis is frequently useful because it eliminates forces that pass through the axis. In many problems, it is possible to ﬁnd an axis for which the corresponding moment equation contains only one unknown.

|Sample Problem 5.4<br><br>Calculate the tension in each of the three cables that support the 1500-kN weight, using the given FBD.<br><br>Solution<br><br>Method of Analysis<br><br>z As shown in the FBD, the forces acting on the weight are concurrent (all the<br><br>y<br><br>x<br><br>C<br><br>O D<br><br>B<br><br>A<br><br>W = 1500 kN<br><br>2.5 m<br><br>3m<br><br>1.2 m 1.5 m<br><br>2m<br><br>|3m<br><br>O|C 1.2 m 1.5|
|---|---|
|A<br><br>2.5m<br><br>TAB|D TAC<br><br>TAD|
<br><br>z<br><br>y<br><br>x<br><br>B<br><br>1500 kN<br><br>2m<br><br>2.5m<br><br>T<br><br>FBD<br><br>m<br><br>forces intersect at A). Therefore, there are three independent equilibrium equations. Because there are also three unknowns (the tensions TAB, TAC, and TAD), we conclude that the problem is statically determinate.<br><br>The most straightforward solution is obtained from the three scalar force equations, Fx = 0, Fy = 0, and Fz = 0 (or the equivalent vector equation,<br><br>F = 0).<br><br>Mathematical Details<br><br>The ﬁrst step is to write the forces in vector form, as follows:<br><br>TAB = TABλAB = TAB<br><br>−AB→ |<br><br>−AB→|<br><br>= TAB<br><br>2i + 2.5k 3.202<br><br>= TAB(0.6246i + 0.7808k)<br><br>TAC = TACλAC = TAC<br><br>−AC→ |<br><br>−AC→|<br><br>= TAC −3i − 1.2j + 2.5k<br><br>4.085<br><br>= TAC(−0.7344i − 0.2938j + 0.6120k)<br><br>TAD = TADλAD = TAD<br><br>−AD→ |<br><br>−AD→|<br><br>= TAD<br><br>1.5j + 2.5k<br><br>2.915<br><br><br>= TAD(0.5145j + 0.8575k)<br><br><br>W = −1500k kN<br><br>Summing the x-, y-, and z-components and setting the results equal to zero, we have<br><br>Fx = 0 0.6246TAB − 0.7344TAC = 0<br>Fy = 0 −0.2938TAC + 0.5145TAD = 0<br>Fz = 0 0.7808TAB + 0.6120TAC + 0.8575TAD − 1500 = 0<br><br><br>Solving these equations simultaneously gives<br><br>TAB = 873 kN TAC = 743 kN TAD = 424 kN Answer|
|---|

|As you can see, the use of three force equations results in a straightforward method of analysis for a concurrent force system. However, there are other sets of equilibrium equations that could have been used just as effectively.<br><br>Another Method of Analysis<br><br>Note that the tensions TAC and TAD intersect the line CD and thus have no moment about that line. Therefore, TAB can be calculated from only one equation: MCD = 0. Similar arguments can be used to show that MDB = 0 yields TAC, and MBC = 0 gives TAD.<br><br>Mathematical Details<br><br>MCD = 0 (rCB ×TAB ·λCD) + (rCO × W·λCD) = 0<br><br>From the ﬁgure, we note that rCB = 5i + 1.2j m, rCO = 3i + 1.2j m, and the unit vector λCD is given by<br><br>λCD =<br><br>−CD→ |<br><br>−CD→|<br><br>=<br><br>3i + 2.7j 4.036<br><br>Using the vector expressions for TAB and W determined in the foregoing, and using the determinant form of the scalar triple product, the moment equation<br><br>MCD = 0 becomes<br><br>TAB 4.036<br><br>5 1.2 0 0.6246 0 0.7808 3 2.7 0<br><br>+<br><br>1 4.036<br><br>3 1.2 0 0 0 −1500<br>3 2.7 0<br><br><br>= 0<br><br>Expanding the determinants and solving the resulting equation yields TAB = 873 kN, the same answer determined in the preceding analysis.<br><br>As mentioned, the tensions in the other two cables could be obtained from MDB = 0 and MBC = 0.<br><br>Sample Problem 5.5<br><br>The horizontal boom OC, which is supported by a ball-and-socket joint and two<br><br>3ft<br><br>P = 8000 lb<br><br>z<br><br>y<br><br>x<br><br>2ft<br><br>3 ft<br><br>3.5ft 2.5ft<br><br>D<br><br>E<br><br>A<br><br>B<br><br>C<br><br>O<br><br>1.0 ft<br><br>cables, carries the vertical force P = 8000 lb. Calculate TAD and TCE, the tensions in the cables, and the components of the force exerted on the boom by the joint at O. Use the given FBD (the weight of the boom is negligible).<br><br>Solution<br><br>Method of Analysis<br><br>As shown in the FBD, the force system acting on the boom is the special case in which all forces intersect an axis, namely, the y-axis. Therefore, there are ﬁve independent equilibrium equations. Because there are also ﬁve unknowns in the FBD (TAD, TCE, Ox, Oy, and Oz), the problem is statically determinate.|
|---|

|Consider the moment equations about the x- and z-axes ( My = 0 is trivially satisﬁed):<br><br>Mx = 0—contains the unknowns TAD and TCE Mz = 0—contains the unknowns TAD and TCE<br><br>These two equations can be solved simultaneously for TAD and TCE. After these<br><br>3ft<br><br>O<br><br>z<br><br>y<br><br>x<br><br>2ft<br><br>3 ft<br><br>3.5ft 2.5ft<br><br>D<br><br>E<br><br>A<br><br>B<br><br>C<br><br>Oy<br><br>Ox<br><br>Oz<br><br>TAD<br><br>TCE<br><br>FBD<br><br>P = 8000 lb<br><br>1.0 ft<br><br>tensions have been found, the reactions at O can be determined using the force equations of equilibrium.<br><br>Mathematical Details<br><br>A convenient method of writing Mx = 0 and Mz = 0 is to sum the moments about point O using vector representation (recall that MO = Mxi + Myj + Mzk). Referring to the FBD, we have<br><br>MO = (rOA × TAD) + (rOC × TCE) + (rOB × P) = 0 where<br><br>rOA = 3j ft rOC = 6j ft rOB = 5j ft<br><br>TAD = TADλAD = TAD<br><br>−AD→ |<br><br>−AD→|<br><br>= TAD<br><br>2.5i − 3j + 3k 4.924<br><br>= TAD(0.5077i − 0.6093j + 0.6093k)<br><br>TCE = TCEλCE = TCE<br><br>−CE→ |<br><br>−CE→|<br><br>= TCE −3.5i − 6j + 3k<br><br>7.566<br><br>= TCE(−0.4626i − 0.7930j + 0.3965k) P = −8000k lb<br><br>Using the determinant form for the cross products, we have<br><br>MO = TAD<br><br>i j k 0 3 0 0.5077 −0.6093 0.6093<br><br>+ TCE<br><br>i j k 0 6 0 −0.4626 −0.7930 0.3965<br><br>+<br><br>i j k 0 5 0 0 0 −8000<br><br>= 0<br><br>Expanding the determinants and equating the x- and z-components (the ycomponents are identically zero, as expected), we get<br><br>Mx = 0 1.828TAD + 2.379TCE − 40000 = 0 Mz = 0 −1.523TAD + 2.776TCE = 0|
|---|

|from which we ﬁnd<br><br>TAD = 12770 lb TCE = 7010 lb Answer<br><br>After the tensions have been computed, the reactions at O can be calculated by using the force equation F = 0:<br><br>Fx = 0 Ox + 0.5077TAD − 0.4626TCE = 0<br>Fy = 0 Oy − 0.6093TAD − 0.7930TCE = 0<br>Fz = 0 Oz + 0.6093TAD + 0.3965TCE − 8000 = 0<br><br><br>Substituting the previously found values for TAD and TCE, we obtain<br><br>Ox = −3240 lb Oy = 13340 lb Oz = −2560 lb Answer<br><br>The negative values for Ox and Oz indicate that the directions of these components are opposite to the directions shown in the FBD.<br><br>Sample Problem 5.6<br><br>The nonhomogeneous plate weighing 60kN has its center of gravity at G. It is<br><br>W = 60kN<br><br>C y<br><br>| |B|
|---|---|
| | |
<br><br>O<br><br>A x<br><br>z<br><br>2.2 m<br><br>3.6m<br><br>1.0 m<br><br>1.2m G<br><br>FBD<br><br>0.8 m<br><br>C y<br><br>|B<br><br>|B<br><br>2.2 m|
|---|---|
| | |
<br><br>O<br><br>A x<br><br>z<br><br>1.0 m<br><br>1.2m G<br><br>TA<br><br>T TC 0.8 m<br><br>3.6m<br><br>supported in the horizontal plane by three vertical cables. Compute the tension in each cable using the given FBD.<br><br>Solution<br><br>Method of Analysis<br><br>As shown in the FBD, the forces holding the plate in equilibrium form a parallel system, which has three independent equilibrium equations. Because there are also three unknowns (TA, TB, and TC), the problem is statically determinate.<br><br>One method of analysis considers the moment equations about the x- and y-axes ( Mz = 0 is trivially satisﬁed because the forces are parallel to the z-axis) and the force equation in the z-direction.<br><br>Mx = 0—contains the unknowns TB and TC My = 0—contains the unknown TA<br><br>Fz = 0—contains the unknowns TA, TB, and TC<br><br>First, the equation My = 0 can be used to ﬁnd TA. Then, the other two equations can be solved simultaneously for TB and TC. The details of this analysis, using scalar representation, are shown in the following.|
|---|

|Mathematical Details<br><br>My = 0 + 60(1.2) − 3.6TA = 0 (1) which gives<br><br>TA = 20.0 kN Answer<br><br>Mx = 0 + 0.8TB + 3.0TC − 60(1.0) = 0 (2)<br><br>Fz = 0 +  TA + TB + TC − 60 = 0 (3) Substituting TA = 20.0 kN, and solving Eqs. (2) and (3) yields<br><br>TB = 27.3 kN TC = 12.7 kN Answer<br><br>Another Method of Analysis<br><br>In the above solution, we were able to ﬁnd TA using the equation My = 0 because TB and TC have no moment about the y-axis. By studying the FBD, you will see that it is also possible to calculate TB using one equation, and TC using one equation.<br><br>Sample Problem 5.7<br><br>The bent bar of negligible weight is supported by a ball-and-socket joint at O, a cable connected between A and E, and a slider bearing at D. The bar is acted on by a wrench consisting of the force P and couple C, both parallel to the z-axis. Determine the components of bearing reaction at D and the force in the cable using the given FBD.<br><br>Solution<br><br>Method of Analysis<br><br>The force system in the FBD is the general case. Therefore, there are six independent equilibrium equations available for computing the six unknowns (Ox, Oy, Oz, TAE, Dx, and Dz).<br><br>Referring to the FBD, we consider the moment equation about each of the coordinate axes:<br><br>Mx = 0— contains the unknown Dz My = 0— contains the unknowns TAE, Dx, and Dz Mz = 0— contains the unknowns TAE and Dx<br><br>Therefore, the three unknowns TAE, Dx, and Dz can be computed from these equations according to the following scheme: First ﬁnd Dz from Mx = 0, and then solve the other two equations simultaneously for Dx and TAE.|
|---|

|Mathematical Details<br><br>When utilizing the above analysis, it is convenient to use the vector approach to<br><br>y<br><br>x<br><br>A<br><br>B<br><br>E<br><br>P = 2000 lb<br><br>C = 6000 lb.ft<br><br><br>4 ft<br><br>3 ft<br><br>2 ft 2 ft<br><br>z<br><br>y<br><br>O<br><br>A B<br><br>D<br><br>E<br><br>P = 2000 lb<br><br><br>C = 6000 lb.ft<br><br>4 ft<br><br>3 ft<br><br>2 ft 2 ft<br><br>Ox<br><br>Oz<br><br>Oy<br><br>TAE<br><br>Dx<br><br>Dz<br><br>FBD<br><br>4ft<br><br>4ft<br><br>z<br><br>O<br><br>D<br><br>x<br><br>2ft2ft<br><br>derive the moment equations MO = Mxi + Myj + Mzk = 0. The details are as follows:<br><br>MO = 0 (rOA × TAE) + (rOD × D) + (rOB × P) + C = 0<br><br>Referring to the FBD, the vectors in the above equation are<br><br>rOA = 4i ft rOD = 4i + 7j + 2k ft<br>rOB = 4i + 2j ft P = −2000k lb C = −6000k lb · ft<br><br><br>TAE = TAEλAE = TAE<br><br>−AE→ |<br><br>−AE→|<br><br>= TAE −4i + 7j + 4k<br><br>9 D = Dxi + Dzk<br><br>Therefore, MO = 0 can be written in determinant form as<br><br>TAE 9<br><br>i j k 4 0 0<br><br>−4 7 4<br><br>+<br><br>i j k 4 7 2 Dx 0 Dz<br><br>+<br><br>i j k 4 2 0 0 0 −2000<br><br>− 6000k = 0<br><br>Expanding the determinants and equating the x-, y-, and z-components yields the equations<br><br>(x-component) 7Dz − 4000=0<br>(y-component) −1.778TAE + 2Dx −4Dz + 8000=0<br>(z-component) 3.111TAE − 7Dx −6000=0<br><br><br>The solution of these equations yields<br><br>Dz = 571 lb TAE = 4500 lb Dx = 1140 lb Answer<br><br>If desired, the reactions Ox, Oy, and Oz could now be found from the force equation F = 0.<br><br>It should be noted that TAE could also be obtained from a single scalar equilibrium equation MOD = 0.|
|---|

###### 2ft

![image 37](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile37.png>)

###### Problems

###### In each of the following problems, the free-body diagram is given. Write the equilibrium equations and compute the requested unknowns.

- 5.13 In Sample Problem 5.4, determine the tension TAC using the equation MDB = 0.
- 5.14 In Sample Problem 5.5, compute the tension TAD using one scalar equilibrium equation.
- 5.15 In Sample Problem 5.5, determine Oy with one scalar equilibrium equation.
- 5.16 Determine the tension TB in Sample Problem 5.6 using one scalar equilibrium equation.
- 5.17 Compute the tension TAE in Sample Problem 5.7 using one scalar equilibrium equation.
- 5.18 The 40-kg homogeneous plate is suspended from four wires. Determine the tension in each wire.

40 kg

250

750

500

D

A

B x y

z

C

250

750

500 392.4 N

Dimensions in mm FBD

375

D

A TD

TC

TA

TB

B x y

z

C

550

550

550

550

Fig. P5.18

- 5.19 The bent bar is supported by slider bearings at A, B, and C. Determine the bearing reactions caused by the 1200-lb·in. couple. Express the answers in vector form.

###### 5.13–5.26 Problems 261

z

1200 lb · in.

15in.

x A

C

B

24in.

27in.

z

y

Az

1200 lb · in.

A

Bz

Cz

Ax

B

15in.

C Bx

x

Cy

27in.

24in.

y

FBD

###### Fig. P5.19

- 5.20 The compound bar is supported by a thrust bearing at A, a slider bearing at B, and the cable CD. Determine the tension in the cable and the magnitude of the bearing reaction at A. Neglect the weight of the bar.

z

x y

D

A C

D

z

B

FBD

270 lb

270 lb

2.8 ft

2.8 ft

3.5ft

3.5ft

3.5ft

2ft

3.5ft

2ft

Ax

Ay

Az

Bz

By

B

A

y

C

T

x

Fig. P5.20

- 5.21 The homogeneous door of weight W =60 lb is held in the horizontal plane

|z Ox| |
|---|---|
|lb|2ft|

| |O|
|---|---|
| | |

4 ft

y

1.5ft

x

z

A

- B
- C

4 ft

2.5ft

1.5ft

z

Ay

Az

Oy

O

2 ft

PBC

FBD

x

y 60 l

2.5ft

Fig. P5.21

by a thrust hinge at O, a hinge at A, and the vertical prop BC. Determine all forces acting on the door.

- 5.22 The light boom AB is attached to the vertical wall by a ball-and-socket joint at A and supported by two cables at B. A force P = 12i − 16k kN is applied

at B. Note that RA, the reaction at A, acts along the boom because it is a two-force body. Compute the cable tensions and RA.

z

z

2m

2m

C

C D

D

4m

4m

2m

2m

D z

- 2ft2ft

3ft

- 3ft

6m3m

6m3m

TBD TBC

2 ft

B

6 m 6 m B

O O

y

y

###### x P P

x

C O

A

B

A

A

x

y

###### RA

3 ft

FBD

Fig. P5.22 5.23 The homogeneous 120-lb sign is suspended from a ball-and-socket joint

D z

- 2ft2ft

3ft

- 3ft 2 ft

at O, and cables AD and BC. Determine the forces in the cables.

Oz

TAD

- 5.24 The support for the T-shaped bar consists of a thrust bearing at O and a slider bearing at B. When a weight W is suspended from D, the force P = W/2, parallel to the x-axis, is required to maintain equilibrium. Calculate θ, the angle of inclination of the bearing axis OB.

B1

z

B

a a A

C

D P

y O

x

z

B

a a A

C

D

y

O

x

W

W

O1 O3

O2

B2

a

a

a

a

FBD

P =

2

W

θ

θ

Fig. P5.24

- 5.25 The space truss is supported by ball-and-socket joints at B, D, and F. Determine the forces in members AB, AC, and AD.

Oy

O

A

Ox

C

TBC

B

x

y

W = 120 lb FBD

Fig. P5.23

###### 5.7 Equilibrium Analysis 263

1200 lb

1200 lb 800 lb

###### A

A

PAB

E

B

800 lb

B C

PAC

PAD

3 ft

2.5ft

C

3 ft

2.5ft

1.0 ft

1.0 ft

F z

2.5ft

2.5ft

y x

4 ft FBD

4 ft 4 ft

D D

###### Fig. P5.25

- 5.26 For the truss described in Prob. 5.25, ﬁnd the forces in members BC and CE.

1200 lb

A

E

PAB

800 lb

B C

PBC

3 ft

2.5ft z

PCE

1.0 ft

y

Dz

2.5ft

PDE Dy

x

D

4 ft

4 ft

Dx

FBD

###### Fig. P5.26

###### 5.7 Equilibrium Analysis

The method for analyzing rigid bodies subjected to three-dimensional force systems is the same as used in Chapter 4 for coplanar loadings.

- 1. Draw the free-body diagrams.
- 2. Write the equilibrium equations.
- 3. Solve the equations for the unknowns.

Article 5.3 concentrated on the construction of FBDs. Article 5.6 was devoted to writing and solving the equilibrium equations from given FBDs. The sample problems that follow this article illustrate the complete analysis of threedimensional equilibrium problems, beginning with the construction of the FBDs and ending with the solution. Analyses of both single and connected bodies are considered.

We reiterate that you must be careful when drawing free-body diagrams. Sloppy sketches of three-dimensional problems are notoriously difﬁcult to read; consequently, they are a major source of errors in the derivation of equilibrium equations.

|Sample Problem 5.8<br><br>Determine the forces acting on the bent bar OBD in Fig. (a). The bar is loaded by the wrench consisting of the force P and couple C. Neglect the weights of the members, and assume that all connections are ball-and-socket joints.<br><br>E<br><br>x<br><br>y<br><br>z<br><br>P = 10 kN<br><br>C = 40 kN · m<br><br>A B O<br><br>D<br><br>4 m<br><br>2 m<br><br>(a)<br><br>3 m<br><br>F<br><br>3m<br><br>4m<br><br>1 m<br><br>2 m<br><br>E<br><br>x<br><br>y<br><br>z<br><br>C = 40 kN · m<br><br>A B<br><br>D<br><br>4 m<br><br>(b)<br><br>3 m<br><br>F 1 m<br><br>PBF PAE<br><br>O Ox<br><br>Oz Oy<br><br>3m<br><br>4m<br><br>2 m<br><br>P = 10 kN<br><br>Solution<br><br>Method of Analysis<br><br>The ﬁrst step is to draw the FBD of bar OBD, which is shown in Fig. (b). The reactions at the ball-and-socket at O are labeled Ox, Oy, and Oz. Note that we have used the fact that the struts AE and BF are two-force bodies, each assumed to act in tension.<br><br>We see that the FBD contains ﬁve unknowns (PAE, PBF, Ox, Oy, and Oz). Because there are also ﬁve independent equilibrium equations, the problem is statically determinate.<br><br>Referring to the FBD in Fig. (b), we consider the moment equations about the x- and z-axes ( My = 0 is trivially satisﬁed):<br><br>Mx = 0—contains the unknowns PAE and PBF Mz = 0—contains the unknowns PAE and PBF<br><br>Therefore, these two equations can be solved simultaneously for PAE and PBF. After these two unknowns have been found, the force equation F = 0 can be used to ﬁnd the remaining three unknowns: Ox, Oy, and Oz.<br><br>Mathematical Details<br><br>We choose to write the moments about the x- and z-axes using the vector expression MO = Mxi + Myj + Mzk.<br><br>MO = 0 (rOA × PAE) + (rOB × PBF) + (rOB × P) + C = 0|
|---|

|The vectors that appear in this equation are<br><br>rOA = 4j m rOB = 7j m P = 10k kN C = −40k kN · m<br><br>PAE = PAEλAE = PAE<br><br>−AE→ |<br><br>−AE→|<br><br>= PAE<br><br>3i − 4j + 2k 5.385<br><br>PBF = PBFλBF = PBF<br><br>−BF→ |<br><br>−BF→|<br><br>= PBF −4i − 7j + k<br><br>8.124<br><br>Expressing the cross products in determinant form, the equilibrium equation<br><br>MO = 0 then becomes<br><br>PAE 5.385<br><br>i j k 0 4 0 3 −4 2<br><br>+<br><br>PBF 8.124<br><br>i j k 0 7 0<br><br>−4 −7 1<br><br>+<br><br>i j k 0 7 0 0 0 10<br><br>− 40k = 0<br><br>Expanding the determinants and equating the x- and z-components (there is no y-component, as expected), we obtain<br><br>(x-component) 1.486PAE + 0.862PBF + 70 = 0 (z-component) −2.228PAE + 3.447PBF − 40 = 0<br><br>Solving simultaneously, we obtain<br><br>PAE = −39.16 kN PBF = −13.70 kN Answer<br><br>The minus signs indicate that the sense of each force is opposite to that assumed in the FBD. In vector form, the two forces are<br><br>PAE = PAEλAE = −39.16<br><br>3i − 4j + 2k 5.385<br><br>= −21.82i + 29.09j − 14.54k kN<br><br>PBF = PBFλBF = −13.70 −4i − 7j + k<br><br>8.124<br><br>= 6.75i + 11.80j − 1.69k kN<br><br>Summing forces, we have<br><br>F = 0 PAE + PBF + P + (Oxi + Oyj + Ozk) = 0<br><br>Substituting the expressions for PAE, PBF, and P, and solving, yields<br><br>Ox = 15.1 kN Oy = −40.9 kN Oz = 6.2 kN Answer|
|---|

|Sample Problem 5.9<br><br>The window in Fig. (a) weighs 40lb; its center of gravity G is located at the geometric center. Find all forces acting on the window when it is held open in the position shown by the rope attached to C. Assume that the hinge at A can provide an axial thrust whereas the hinge at B cannot.<br><br>2ft1.8ft<br><br>2.2ft<br><br>x<br><br>y<br><br>0.4ft<br><br>1.5ft<br><br>0.4ft<br><br>1.5ft<br><br>C<br><br>B<br><br>A<br><br>D<br><br>z<br><br>(a)<br><br>G<br><br>x<br><br>G C<br><br>B<br><br>A<br><br>D z<br><br>1.1<br><br>1.1<br><br>1.82<br><br>1.5<br><br>1.9<br><br>1.5<br><br>0.4<br><br>0.4<br><br>Az<br><br>Ax<br><br>Ay<br><br>Bz<br><br>By<br><br>W = 40 lb<br><br>TCD<br><br>y<br><br>(b)<br><br>Dimensions in feet<br><br>Solution<br><br>Method of Analysis<br><br>We begin by drawing the FBD of the window—see Fig. (b). In addition to its 40-lb weight and the tension TCD in the rope, the window is acted on by the hinge reactions at A and B. Note that an axial thrust (force component in the x-direction) is shown only for the hinge at A.<br><br>The FBD contains six unknowns: Ax, Ay, Az, By, Bz, and TCD. Because the force system is the general case, there are also six independent equilibrium equations, which means that the problem is statically determinate.<br><br>Point A plays an important role in the analysis of this problem, because three of the unknowns (Ax, Ay, and Az) pass through A. Referring to the FBD, we examine the following moment equations:<br><br> (MA)x = 0— contains the unknown TCD<br> (MA)y = 0— contains the unknowns TCD and Bz (By is parallel to this axis)<br> (MA)z = 0— contains the unknowns TCD and By (Bz is parallel to this axis)<br>|
|---|

|These three scalar equations can be solved for the unknowns TCD, By, and Bz. Once these values are known, the three force components at A (Ax, Ay, and Az) can be found from the force equation F = 0.<br><br>Mathematical Details<br><br>We will use the vector representation to ﬁnd the moment equations about the axes passing through A; that is, MA = ( MA)xi + ( MA)yj + ( MA)zk = 0.<br><br>MA = 0 (rAD × TCD) + (rAB × B) + (rAG × W) = 0<br><br>Writing the forces and position vectors in rectangular form, we have<br><br>TCD = TCDλCD = TCD<br><br>−CD→ |<br><br>CD−→|<br><br>= TCD<br><br>1.9i − 2.2j + 3.8k 4.784<br><br>B = Byj + Bzk W = −40k lb rAD = −1.5i + 2k ft rAB = −3i ft rAG = −1.5i + 1.1j − 0.9k ft<br><br>Then, the determinant form of the equation MA = 0 is<br><br>TCD 4.784<br><br>i j k −1.5 0 2<br><br>1.9 −2.2 3.8<br><br>+<br><br>i j k −3 0 0<br><br>0 By Bz<br><br>+<br><br>i j k −1.5 1.1 −0.9<br><br>0 0 −40<br><br>= 0<br><br>Expanding the above determinants and equating like components, we get<br><br>(x-component) 0.9197TCD −44.0=0<br>(y-component) 1.9858TCD +3Bz − 60.0=0<br>(z-component) 0.6898TCD − 3By =0<br><br><br>Solving these equations gives<br><br>TCD = 47.84 lb By = 11.00 lb Bz = −11.67 lb Answer<br><br>Omitting the details, the remaining three unknowns are found from the force equation F = 0 to be<br><br>Ax = −19.00 lb Ay = 11.00 lb Az = 13.67 lb Answer|
|---|

|Sample Problem 5.10<br><br>The two bars AC and CD are homogeneous and weigh 200N/m. Joints A, C, and D are ball-and-sockets, and a cable is connected between B and E. Determine all forces that act on bar AC.<br><br>A x<br><br>z<br><br>E<br><br>B<br><br>C y<br><br>D<br><br>3m<br><br>2m<br><br>2m<br><br>3m<br><br>4m<br><br>3m<br><br>(a)<br><br>Solution<br><br>Method of Analysis<br><br>As you know, there are many ways in which one can calculate the unknown forces acting on bodies that are connected together. However, considering the FBD of the entire assembly is usually a good place to begin.<br><br>The FBD of the entire assembly is shown in Fig. (b). The weights of the bars, WAC and WCD, were calculated by multiplying the weight per unit length (200N/m) by the length of each bar. The components of the reaction at A are Ax, Ay, and Az; the components of the reaction at D are Dx, Dy, and Dz; TBE is the tension in the cable.<br><br>We see that the FBD in Fig. (b) contains seven unknowns (three force components each at A and D, and the tension TBE). Because there are only six independent equilibrium equations (the force system represents the general case), we cannot calculate all of the unknowns without taking the assembly apart. However, we see that TBE is the only unknown that does not intersect the axis AD. Therefore, we can ﬁnd TBE from the moment equation MAD = 0.<br><br>z<br><br>E<br><br>2m<br><br>2m<br><br>A<br><br>(b)<br><br>Dz<br><br>Dy<br><br>Dx<br><br>F<br><br>Ay<br><br>Az<br><br>Ax<br><br>TBE<br><br>WCD = 1000 N<br><br>x<br><br>C y<br><br>D<br><br>3m<br><br>3m<br><br>2m<br>3m<br><br><br>B<br><br>WAC = 1200 N<br><br>2m<br><br>|
|---|

###### m

|We next draw the FBDs of bars AC and CD separately—see Figs. (c) and (d). The force components at A in Fig. (c) and the force components at D in Fig. (d) must act in the same directions as in Fig. (b). Furthermore, the components of the reaction at C (Cx, Cy, and Cz) in Fig. (c) must be equal in magnitude, but oppositely directed, to the corresponding components in Fig. (d). We note that there are ten unknowns in this problem: three each at A, C, and D, and the tension TBE. The total number of independent equilibrium equations is also ten: ﬁve each for the two bars (the force system acting on each bar represents the special case in which the forces intersect an axis). This problem is therefore statically determinate.<br><br>C<br><br>(c)<br><br>Cy Cx Cz<br><br>E<br><br>2m<br><br>A<br><br>Ay<br><br>Az<br><br>Ax<br><br>TBE<br><br>3m<br><br>3m<br><br>B<br><br>WAC = 1200 N<br><br>2m<br><br>(d)<br><br>Cz Cy<br><br>Cx<br><br>Dz<br><br>Dy<br><br>Dx<br><br>F<br><br>WCD = 1000 N<br><br>D<br><br>2m<br>3m<br><br><br>2m<br><br>Referring to the FBD in Fig. (d), Cy can be computed using the moment equation  (MD)z = 0. Next, consider the FBD in Fig. (c). Because we have already determined TBE and Cy, only ﬁve unknowns remain: Ax, Ay, Az, Cx, and Cz. Therefore, any of the ﬁve independent equations for this FBD can be used to ﬁnd these unknowns.<br><br>Mathematical Details<br><br>Referring to the FBD of the entire assembly in Fig. (b), and using scalar triple products to evaluate the moments about the axis AD, we obtain<br><br>MAD = 0<br><br>(rAB × TBE ·λAD) + (rAB × WAC ·λAD) + (rAF × WCD ·λAD) = 0 The vectors appearing in this equation are<br><br>rAB = 3j m rAF = −2i + 6j + 1.5k m WAC = −1200k N WCD = −1000k N<br><br>TBE = TBEλBE = TBE<br><br>−BE→ |<br><br>−BE→|<br><br>= TBE −2i − 3j + 2k<br><br>4.123<br><br>λAD =<br><br>−AD→ |<br><br>−AD→|<br><br>=<br><br>−4i + 6j + 3k 7.810<br><br>|
|---|

|The equation MAD = 0 thus becomes<br><br>1 7.810<br><br>TBE 4.123<br><br>0 3 0 −2 −3 2 −4 6 3<br><br>+<br><br>1 7.810<br><br>0 3 0 0 0 −1200<br><br>−4 6 3<br><br>+<br><br>1 7.810<br><br>−2 6 1.5 0 0 −1000 −4 6 3<br><br>= 0<br><br>Expanding the determinants and solving yields<br><br>TBE = 18140 N Answer Using the FBD of bar CD in Fig. (d),<br><br> (MD)z = 0 gives Cy = 0 Answer<br><br>As mentioned, with TBE and Cy already computed, we can use any ﬁve available equations to ﬁnd the ﬁve remaining unknown forces on the FBD of bar AC in Fig. (c). One method for ﬁnding the forces at A and C is outlined in the following; the mathematical details are left as an exercise.<br><br>Fy = 0 gives Ay = 13200 N Answer  (MC)x = 0 gives Az = 3800 N Answer  (MC)z = 0 gives Ax = 4400 N Answer<br><br>Fx = 0 gives Cx = 4400 N Answer Fz = 0 gives Cz = 3800 N Answer|
|---|

![image 38](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile38.png>)

###### Problems

- 5.27 Calculate all forces acting on the bar AB described in Prob. 5.1.
- 5.28 Determine the forces in members AD, BD, and CD of the space truss in Prob. 5.3.
- 5.29 Find the tension in cable BE that supports the bar ABCD described in Prob. 5.6.
- 5.30 For the structure in Prob. 5.9, determine the reactions at C and D.
- 5.31 Calculate the reaction at D for the structure described in Prob. 5.11.

Dimensions in feet

z

B

E

F D

C

A x

y

12

6

6

12

6

3 3

Fig. P5.32

- 5.32 The frame is supported by a ball-and-socket joint at A and a slider bearing at C. The strut EF has a ball-and-socket joint at each end. The cable EBD runs over a small pulley at B and carries a 600-lb weight D. Neglecting the weights of the members, determine the force in EF and the magnitude of the reaction at C.
- 5.33 Determine the tension in each of the three ropes supporting the 600-lb crate.
- 5.34 Using only one equilibrium equation, compute the force in rope AD of

|A| | |
|---|---|---|
| | | |

| | | | | | |
|---|---|---|---|---|---|

y

z

x

B

C

D

O

7 ft

4 ft 4 ft

4 ft4 ft

W = 600 lb

2 ft

1.6 ft

Fig. P5.33, P5.34

Prob. 5.33.

- 5.35 The homogeneous 25-kg bar AB is supported by a ball-and-socket joint

B P

0.8m

1.6 m

25 kg z

x y

1.8m

at A. End B, which leans against a frictionless vertical wall, is kept from sliding by the horizontal force P. Determine P and the force exerted by the wall at B.

A

Fig. P5.35

###### 5.36 The shaft AB is supported by a thrust bearing at A and a slider bearing at B. Determine the force in cable CD, and the bearing reactions at A and B caused by the 90-N vertical force applied at E. Neglect weights.

z

60

30

D

125

65

C A

6 kN

C

B

450

500

2.4 kN•m

B

E

y

D

70

z

9 kN

270

x

90 N

40

x y

A

Dimensions in mm

Dimensions in mm

###### Fig. P5.36 Fig. P5.37

- 5.37 The bar ABCD has a built-in support at A. Calculate the force and the couple exerted by the support on the bar. Neglect the weight of the bar and express the answers in vector form.
- 5.38 The total mass of the L-shaped beam of constant cross section is 1470kg.

The beam is hoisted by three vertical cables attached at O, A, and B. Determine the distances a and b for which the tensions in the cables are equal.

z

- PA PO
- PB

- 5.39 The crank is supported by a thrust bearing at A, a slider bearing at B, and a frictionless surface at D. Calculate the reactions at A, B, and D if P = 200 lb and C = 800 lb · ft. The weight of the crank may be neglected.

| | |
|---|---|
| | |

z

x

y

2 ft 1.5 ft 2 ft

2 ft

4ft

A O B

D E

C

P

1.25 ft

1.5ft

Fig. P5.39

- 5.40 A 120-lb weight is attached to the cable that is wrapped around the 50-lb homogeneous drum. The shaft attached to the drum is supported by a thrust bearing at A and a slider bearing at B. The drum is kept in equilibrium by the vertical

4 m

a

A O

x

b

3m

B

y

Fig. P5.38

###### force P acting on the handle of the crank. Determine P and the reactions at A and B. Neglect the weights of the crank and the shaft.

z

12

32

A

28

15

24

12

P

x

B

50 lb

y

12

120 lb

Dimensions in inches

###### Fig. P5.40

- 5.41 Calculate the force in cable CD and the reaction at O. Assume that O, A,

z

D

O

B

y x

A

3m

4m

2m

C

400 N

2m

and B are ball-and-socket joints, and neglect the weights of the members. Fig. P5.41

- 5.42 The homogeneous 48-lb plate is welded to the vertical shaft AB of negligible weight. The assembly is supported by a slider bearing at A and a thrust bearing at B. Determine the force in cable CD and the magnitude of the bearing reaction at A.

z

A

0.8 ft

4.8ft

60 lb

3.5 ft

E

48 lb

1.8 ft

B D

C

3.6ft

x

y

###### Fig. P5.42

E 5.43 The A-frame is supported by a thrust bearing at A, a slider bearing at B,

z

and the cable CD. Compute the tension in the cable and the components of the bearing reaction at B caused by the 600-lb load.

600 lb

5 ft

x y

C

- 5.44 A hoist is formed by connecting bars BD and BE to member ABC. Neglecting the weights of the members and assuming that all connections are ball-and-socket joints, determine the magnitudes of the forces in bars BD and BE in terms of the applied load P.

A

z

B

D

E

C O

x y

4 m

3m

4m

6m

4m

P

Fig. P5.44

- 5.45 The crank arm OD of the winch is connected by a universal joint at D to the shaft-pulley assembly. The winch is supported by slider bearings at B and E, and by a thrust bearing at G. Determine the force P that will hold the winch at rest, and calculate the magnitudes of the corresponding bearing reactions. Neglect the weights of the members.

A

4ft

3ft

3ft

4ft

B D

3ft

Fig. P5.43

z

100

200

###### P

320

200

320

320

240 O

x

B

D

E

F

y

Dimensions in mm

G

200 360 N

###### Fig. P5.45

- 5.46 The 40-lb homogeneous door is rigidly attached to the bent bar ABC. The assembly is supported by a thrust bearing at A and a slider bearing at C. Determine the vertical force P required to keep the door in equilibrium in the position shown. Neglect the weight of bar ABC.

B

A

C

y

x

z

7.5in.

2.5in.

26in.

16in.

21in. D

P

40 lb

Fig. P5.46

- 5.47 The frame is built into the wall at D and G. The cross-members AE and BF pass through frictionless holes at A, B, E, and F. The weights of the members are negligible. Determine the reactions at D.

x

46in.

30 in.

240 lb

z

y

A

B

D

G

I

F

E

H

64in.

24in.

36in.

z

240

A

D

240

x

320 N

E

F

O

B

C

240

240

240

y

G

320

Dimensions in mm

Fig. P5.47 Fig. P5.48

- 5.48 All connections of the structure are ball-and-socket joints, except for the slider bearings at A and O. The weights of the members may be neglected. Calculate the forces in members BE and CF.

5.49 Determine the reactions at ball-and-socket joints D, E, and F of the space truss shown. Express the answers in vector form.

z F

C

E

1.5 m

D x y

B

1.5m A

2m

90 kN

Fig. P5.49

![image 39](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile39.png>)

###### Review of Equations

###### Equilibrium equations in three dimensions

General case F = MA = 0 (6 eqs.) Concurrent force system F = 0 (3 eqs.)

All forces parallel to z-axis Fz = Mx = My = 0 (3 eqs.) All forces intersect z-axis F = 0 Mx = 0 My = 0 (5 eqs.)

![image 40](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile40.png>)

###### Review Problems

- 5.50 The space truss is supported by vertical cables at A, B, and C. Calculate

D

C

1800 lb

5ft

5ft 3ft

x

z

y

A

B

9ft

12 ft

Fig. P5.50

the forces in members CB and CD of the truss.

- 5.51 The bent rod is supported by a ball-and-socket joint at O, a cable at B, and a slider bearing at D. Neglecting the weight of the rod, calculate the tension in the cable and the magnitude of the bearing reaction at D.

| | | |
|---|---|---|
| | | |

z

x

O

4 ft 4 ft

1000 lb

2000 lb

3ft3ft

D

C

60°

y 40°

A

B

Fig. P5.51

- 5.52 Find the maximum load P that can be supported by the tripod if the force in any leg is limited to 2000lb. Assume that the legs are two-force bodies.

z

x

D

8 ft

- O

y

B

C

A

- P

6 ft

6 ft

3 ft 6 ft

Fig. P5.52

- 5.53 The vertical mast OA, which weighs 1.5kN, is supported by a ball-and-

###### z

4

###### A

Dimensions in meters

C

4

7

20 kN

B

3

2

5

O x

y

socket joint at O and by the cables AB and AC. Calculate the tension in each cable when the 20-kN force is applied.

Fig. P5.53

z

###### 5.54 The homogeneous bar AB weighs 80lb. End B leans against a vertical wall

and end A is supported by a ball-and-socket joint. Determine the tension in the cable BC and the wall reaction at B. Neglect friction.

C

30°

- 5.55 The 500-kg crate is supported by the three cables. Find the tension in cable AD.

|D| | |
|---|---|---|
| | | |

| | | | | | |
|---|---|---|---|---|---|

y

z

x

A

B

C

O 6m

4m

500 kg

4 m

2 m

8 m

10 m

Fig. P5.55

- 5.56 The uniform bars AB and BC each weigh 4lb/ft. Calculate the tension in cable DE, and the magnitudes of the ball-and-socket reactions at A, B, and C.

- B

5 ft

4ft

6ft

x

A y

Fig. P5.54

z

D

9 ft

2.5 ft

z

7.5ft

E

F

C

A

6 ft

4 ft

E

B

y B

6ft

y

7ft

A

6ft

4 ft

D

x

7ft

1200 lb

x

C

###### Fig. P5.56 Fig. P5.57

5.57 The 1200-lb weight is suspended from a cable that runs over a small pulley attached to the boom ABC. The boom is supported by a ball-and-socket joint at C and two cables attached at B. Neglecting the weight of the boom, determine the tension in cable BE.

- 5.58 The homogeneous 860-kg bar AB is supported by a ball-and-socket joint at A and two cables attached to B. Find the tension in cable CB.

z

A

D

y

B

4 m

3m

3m

2.2m

2.6m

C

x

4.5m

2 m 2 m 3m

B C

A

z

y

x

20 kN·m

Fig. P5.58 Fig. P5.59

- 5.59 The triangular plate is supported by three vertical rods, each of which is able to carry a tensile or compressive force. Calculate the force in each rod when the 20-kN · m couple is applied. Neglect the weight of the plate.
- 5.60 The connections at the ends of bars AB and BC are ball-and-socket joints. Neglecting the weights of the bars, determine the force in cable DE and the reaction at A.

z

x y

E

C

D B

A

2m

1m

1m

0.8 m

800 N

O

x

- B

A

D

- C

O

y

z

3m

5m

4m

6m

3m

Fig. P5.60 Fig. P5.61

- 5.61 The 150-kg bar ABO is supported by two cables at A and a slider bearing at B. The end of the bar presses against a frictionless surface at O. Find the tensions in the cables and the contact force at O.

5.62 The shaft is supported by a thrust bearing at A and a slider bearing at B. Rotation of the shaft is prevented by the cable CD. Compute the tension in the cable and the magnitude of the bearing reaction at B caused by the 50-lb·ft couple.

z

A

50 lb.ft

C

B

12 in.

21in.

D

y

x

18in.

16in.

###### Fig. P5.62

# 6

### Beams and Cables

![image 41](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile41.png>)

Cables are the main structural components of a suspension bridge. This chapter shows how to determine the tension in a cable under a variety of load conditions. George Doyle/Stockbyte/Getty Images

###### *6.1 Introduction

In this chapter we introduce the analyses of beams and ﬂexible cables, two important topics of structural mechanics. The analysis of beams that carry transverse loads deals with the computation of internal forces and couples. Because the internal forces and couples may vary in a complicated manner with the distance along the beam, we place considerable emphasis on methods of computation and graphical displays of the results.

The analysis of ﬂexible cables can also become quite involved; the source of the difﬁculty lies in the geometry of the cable. Because a cable can carry only a tensile force, it must adjust its shape so that the internal tension is in equilibrium with the applied loads. Therefore, the geometry of the cable is not always known at the beginning of the analysis. When the shape of the cable is unknown, the solution invariably leads to nonlinear equations, which can only be solved numerically.

###### 281

###### PART A: Beams

###### *6.2 Internal Force Systems

The determination of internal forces is a fundamental step in the design of members that carry loads. Only after this computation has been made can the design engineer select the proper dimensions for a member or choose the material from which the member should be fabricated.

If the external forces that hold a member in equilibrium are known, we can compute the internal forces by straightforward equilibrium analysis. For example, consider the bar in Fig. 6.1(a) that is loaded by the external forces F1, F2, . . . , F5. To determine the internal force system acting on the cross section labeled 1 (perpendicular to the axis of the bar), we must ﬁrst isolate the portions of the bar lying on either side of section 1. The free-body diagram (FBD) of the portion to the left of section 1 is shown in Fig. 6.1(b). In addition to the external forces F1, F2, and F3, this FBD shows the resultant force-couple system of the internal forces that are distributed over the cross section: the resultant force R acting at the centroid C of the cross section and the resultant couple CR. As explained in Chapter 3, we can place the resultant force R at any point, provided that we introduce the proper resultant couple. However, locating R at the centroid of the cross section

F1

1

F2

F3

F5

F4

(a)

F1

F1

My

Vy

R

y

F2

F2

F3

P

C

CR

F3

T

Vz

z

C

Mz

x

(b)

(c)

###### Fig. 6.1

###### 6.2 Internal Force Systems 283

is the standard engineering practice. If F1, F2, and F3 are known, the equilibrium equations F = 0 and MC = 0 can be used to compute R and CR.

It is conventional to introduce the centroidal coordinate system shown in Fig. 6.1(b). The axis that is perpendicular to the cross section and passes through the centroid (x-axis) is called the centroidal axis. The components of R and CR relative to this coordinate system are identiﬁed by the labels shown in Fig. 6.1(c) and are given the following physically meaningful names.

P: The force component that is perpendicular to the cross section, tending to

elongate or shorten the bar, is called the normal force.

Vy and Vz: The force components lying in the plane of the cross section, tending to slide (shear) the parts of the bar lying on either side of the cross section relative to one another, are called shear forces.

T: The component of the resultant couple that tends to twist the bar is called twisting moment, or torque. My and Mz: The components of the resultant couple that tend to bend the bar are

called bending moments.

The deformations produced by these internal forces and couples are illustrated in Fig. 6.2.

V

P

Undeformed Elongation Shear

M

T

Twisting Bending

###### Fig. 6.2

In many applications the external forces are coplanar and lie in a plane that contains the centroidal axis. Figure 6.3(a) illustrates the case in which all the external forces lie in the xy-plane, where the x-axis coincides with the centroidal axis of the bar. In this special case, the only nonzero components of the internal force system acting on any cross section—for example, section 1—are the normal force P, the shear force V, and the bending moment M, as shown in Fig. 6.3(b).

F2 Plane of external loads

F1

y

F3

F4

F5 1

z

###### x

(a)

F1 F2

F3

M

C

P

V

(b)

V

F3 F4

F2

F5 F1

M

M

P

P

V

(c)

###### Fig. 6.3

Thus far, we have concentrated on the internal force system acting on the portion of the bar lying to the left of section 1. Using Newton’s third law, these internal forces occur in equal and opposite pairs on the two sides of the cross section, as shown in Fig. 6.3(c). In the following articles, we conﬁne our attention to calculating the internal forces and couples in members subjected to coplanar forces.

|Sample Problem 6.1<br><br>The bar in Fig. (a), supported by a pin at A and a cable at B, carries a uniformly<br><br>A<br><br>3 m 3 m<br><br>1<br><br>2 m<br><br>y<br><br>x<br><br>30°<br><br>(a)<br><br>800 N/m<br><br>B<br><br>distributed load over its left half. Neglecting the weight of the bar, determine the normal force, shear force, and bending moment acting on the cross section at 1 by analyzing (1) the bar segment on the left of section 1; and (2) the bar segment on the right of section 1.<br><br>Solution<br><br>Preliminary Calculations<br><br>We must calculate the external reactions before we can ﬁnd the internal force system. As shown in the FBD in Fig. (b), the bar is subjected to the following<br><br>Ax<br><br>6 m<br><br>1.5 m<br><br>| | |30°|
|---|---|---|
| | | |
<br><br>(b)<br><br>2400 N<br><br>T<br><br>Ay<br><br>A B<br><br>forces: the components Ax and Ay of the pin reaction at A, the tension T in the cable at B, and the 2400-N resultant of the uniformly distributed load. Equilibrium analysis determines the reactions as follows:<br><br>MA = 0 + T sin30◦(6) − 2400(1.5) = 0<br><br>T = 1200 N<br><br>Fx = 0 −→+ Ax − T cos30◦ = 0 Ax = T cos30◦ = 1200cos 30◦<br><br>Ax = 1039 N<br><br>Fy = 0 +  Ay − 2400 + T sin30◦ = 0<br><br>Ay = 2400 − T sin30◦ = 2400 − 1200sin30◦ Ay = 1800 N<br><br><br><br><br>Because these answers are positive, each of the reactions is directed as assumed in Fig. (b).<br><br>To ﬁnd the internal force system acting on the cross section at 1, we must isolate the segments of the bar lying on either side of section 1. The FBDs of the segments on the left and on the right of section 1 are shown in Figs. (c) and (d),<br><br>1 m<br><br>(c)<br><br>1600 N<br><br>Ay = 1800 N<br><br>Ax = 1039 N C<br><br>M1<br><br>P1<br><br>V1<br><br>A 2 m<br><br>4 m<br><br>30°<br><br>M1<br><br>P1<br><br>V1<br><br>0.5 m<br><br>800 N<br><br>T = 1200 N<br><br>C<br><br>(d)<br><br>B<br><br>respectively. Note that in determining the resultants of distributed loading, we considered only that part of the load that acts on the segment.<br><br>The force system acting on the cross section at 1 consists of the normal force P1, the shear force V1, and the bending moment M1. To be consistent with Newton’s third law (equal and opposite reactions), P1, V1, and M1 in Fig. (c) are shown equal in magnitude but oppositely directed to their counterparts in Fig. (d). We can use either FBD to compute P1, V1, and M1.<br><br>Part 1<br><br>Applying the equilibrium equations to the FBD of the bar segment lying to the left of section 1, Fig. (c), we obtain<br><br>Fx = 0 −→+ P1 + 1039 = 0 P1 = −1039 N Answer|
|---|

|Fy = 0 +  1800 − 1600 − V1 = 0<br><br>V1 = 1800 − 1600 = 200 N Answer MC = 0 + −1800(2) + 1600(1) + M1 = 0<br><br>M1 = 3600 − 1600 = 2000 N · m Answer<br><br>The negative sign in P1 indicates that its sense is opposite to what is shown in the FBD.<br><br>Part 2<br><br>Applying the equilibrium equations to the FBD of the bar segment on the right of section 1, Fig. (d), yields<br><br>Fx = 0 −→+ −P1 − 1200cos30◦ = 0 P1 = −1200cos 30◦ = −1039 N Answer<br>Fy = 0 +  V1 + 1200sin30◦ − 800 = 0 V1 = −1200sin30◦ + 800 = 200 N Answer<br><br><br>MC = 0 + −M1 − 800(0.5) + 1200sin30◦(4) = 0<br><br>M1 = −800(0.5) + 1200sin30◦(4) = 2000 N · m Answer These answers agree, of course, with those obtained in Part 1.<br><br>Sample Problem 6.2<br><br>A pin-connected circular arch supports a 5000-lb vertical load as shown in Fig. (a). Neglecting the weights of the members, determine the normal force, shear force, and bending moment that act on the cross section at 1.<br><br>60°<br><br>4 ft<br><br>10ft<br><br>A<br><br>C<br><br>B<br><br>(a)<br><br>5000 lb<br><br>1<br><br>y<br><br>x|
|---|

###### 286

|Solution<br><br>The FBD of the entire arch is shown in Fig. (b). The forces Ax and Ay are the components of the pin reactions at A, and RC is the pin reaction at C. Recognizing that member BC is a two-force member, we know that RC is directed along the line BC. In general, all the external reactions should be computed before the internal force systems are found. However, in this problem, we need only calculate RC. From the FBD in Fig. (b) we obtain<br><br>MA = 0 + RC sin45◦(20) − 5000(4) = 0 RC = 1414 lb<br><br>We next consider the FBD of the portion CD shown in Fig. (c). The forces Dx and Dy are the horizontal and vertical components of the resultant force acting on the cross section, and M1 is the bending moment. We could compute Dx, Dy, and M1 by recognizing that their resultant is a single force that is equal and opposite to RC. However, it is simpler to compute these unknowns using the following equilibrium equations:<br><br>Fx = 0 −→+ Dx − 1414cos45◦ = 0 Dx = 1000lb<br>Fy = 0 +  −Dy + 1414sin45◦ = 0 Dy = 1000lb<br><br><br>MD = 0 + M1 − 1414cos45◦(8.66) − 1414sin45◦(5.00) = 0<br><br>M1 = 3660 lb · ft Answer<br><br>The FBD in Fig. (d) shows the resultant force acting on the cross section in terms of its normal component P1 and shear component V1. Comparing Figs. (c) and (d), we obtain<br><br>P1 = Dy cos60◦ + Dx sin60◦<br><br>= 1000cos 60◦ + 1000sin60◦ = 1366 lb Answer and<br><br>V1 = Dy sin60◦ − Dx cos60◦<br><br>= 1000sin60◦ − 1000cos60◦ = 366 lb Answer<br><br>Because P1, V1, and M1 turned out to be positive, each of them is directed as shown in Fig. (d).<br><br>45°<br><br>4 ft<br><br>A C<br><br>B<br><br>(b)<br><br>5000 lb<br><br>20 ft<br><br>Ax<br><br>Ay<br><br>RC<br><br>60°<br><br>1 D<br><br>45°<br><br>C<br><br>RC = 1414 lb<br><br>M1<br><br>Dx<br><br>Dy D<br><br>10 sin60° = 8.66 ft<br><br>10 – 10 cos60° = 5.00 ft<br><br>60°<br><br>45°<br><br>M1<br><br>RC = 1414 lb<br><br>P1<br><br>V1<br><br>(c) (d)<br><br>=<br><br>60°<br><br>|
|---|

![image 42](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile42.png>)

###### Problems

In the following problems the internal force system is to be represented as a normal force P, a shear force V, and a bending moment M. Neglect the weights of the members.

6.1–6.3 Determine the internal force system acting on section 1 by analyzing

the FBD of (a) segment AD; and (b) segment DB.

1

400 lb/ft

1.5 m 1

6 kN/m

1

###### .

|180 kN m| |
|---|---|
| | |
| |D|

| | |
|---|---|
|D 3.75 m|1.5 m<br><br>|

###### A B

###### A B

A B

D

3 m

6 ft

3 ft

1.5 m

0.75 m

###### Fig. P6.2 Fig. P6.3

Fig. P6.1

6.4–6.6 Find the internal force systems acting on sections 1 and 2.

240 lb total

720 lb·ft

240 lb

3 ft

3 ft

3 ft

###### A B

1

1

###### A B

B

###### A 1

###### C

###### C

2 C 5 ft 5 ft

2

2

5 ft

5 ft

5 ft

5 ft

###### Fig. P6.4 Fig. P6.5 Fig. P6.6

6.7 The three identical cantilever beams carry vertical loads that are distributed in a different manner. It is known that beam (a) fails because the maximum internal bending moment reaches its critical value when P1 = 360 lb. Compute the values of P2 and P3 that would cause the failure of the other two beams.

Total load = P2

###### P1

Total load = P3

| | |
|---|---|
| | |
| |L|

| | |
|---|---|
| | |
| |L|

| | |
|---|---|
| | |
| |L|

(a)

(b)

(c)

###### Fig. P6.7

6.8 Find the internal force systems acting on sections 1 and 2 for the eyebolt shown.

###### 6.1–6.20 Problems 289

2

- 1 in.
- 2

- 3 in.
- 4

28 lb

30°

1

40 lb

###### Fig. P6.8

- 6.9 For the structural component shown, determine the internal force systems acting on sections 1 and 2.

2.5 kN

235

Dimensions in mm

1.2 kN

235

A B C

D

400 400 400

1

2

Fig. P6.9

- 6.10 The two bars, pinned together at B, are supported by a frictionless surface at A and a built-in support at C. Determine the internal force systems acting on sections 1 and 2.

| | | |
|---|---|---|
| | | |
| |B|C|

50°

0.6 m

900 N/m

0.6 m

A

0.6 m 0.6 m

1 2

Fig. P6.10

- 6.11 Determine the internal force system acting on section 1 (just below D) of

| |D<br><br>2<br><br>0.8|
|---|---|
|m|0.9 m<br>1<br><br><br>600 N<br><br>0.8|

0.9

A

B

C

E

800 N

m

m

Fig. P6.11, P6.12

the pin-connected frame.

- 6.12 Determine the internal force systems acting on section 2 (just to the right of the 600-N load) of the pin-connected frame.

240 N

6.13 Determine the internal force systems acting on sections 1 and 2 for the

pin-connected frame. The sections are located just above and just below pin C.

0.3 m

- 6.14 Find the internal force system acting on section 3 for the pin-connected frame.
- 6.15 Calculate the internal force systems acting on sections 1 and 2, which are adjacent to point C.

100 lb

C B

1.8 ft 2.2 ft

1 2

1 ft A

Fig. P6.15

- 6.16 The 600 lb·in. couple is applied to member DEF of the pin-connected

C

240 N

1

3 2

0.4 m

45°

A B

0.4 m

Fig. P6.13, P6.14

D

frame. Find the internal force systems acting on sections 1 and 2.

- 6.17 A man of weight W climbs a ladder that has been placed on a frictionless horizontal surface. Find the internal force system acting on section 1 as a function of x (the position coordinate of the person).
- 6.18 For the ladder in Prob. 6.17, ﬁnd the internal force system acting on section 2, assuming that x < a/2.

x

A

a a

C

a

a

B

D E

2 1

Fig. P6.17, P6.18

- 6.19 Determine the internal force system acting on section 1 of the circular arch.

C

16 in.

2

7 in.

4 in.

- E
- F

1

B

8 in.

600 lb.in.

A

12 in.

Fig. P6.16

1000 lb

B C

500 lb

20°

1

2ft

30°

A

D

###### Fig. P6.19

###### ∗6.20 The equation of the parabolic arch is y = (36 − x2)/6, where x and y are measured in feet. Compute the internal force system acting on section 1.

y

1

2000 lb

6 ft

A

x

B

4 ft

6 ft 6 ft

###### Fig. P6.20

###### *6.3 Analysis of Internal Forces

###### a. Loading and supports

The term beam is reserved for a slender bar that is subjected to transverse loading (the applied forces are perpendicular to the bar). In this chapter, we consider only loadings that are also coplanar. As explained in Art. 6.2, the internal force system caused by coplanar loads can be represented as a normal force, a shear force, and a bending moment acting on the cross section.

Several examples of coplanar beam supports and loadings encountered in structural design are depicted in Fig. 6.4. Also shown are the free-body diagrams of the beams, which display both the applied loads and the support reactions. The reactions for statically determinate beams, Fig. 6.4(a)–(c), can be found from equilibrium analysis. The computation of the reactions for statically indeterminate beams, Fig. 6.4(d)–(f), requires analyses that are beyond the scope of this text.

|Statically determinate beams|Statically indeterminate beams|
|---|---|
|w0<br><br>A B<br><br>w0<br><br>NA By<br><br>Bx<br><br>(a) Simply supported beam|(d) Continuous beam<br><br>w0<br><br>A B C w0<br><br>Cx<br><br>NA NB Cy|
|P1<br><br>A<br><br>B<br><br>P1<br><br>NA By<br><br>Bx<br><br>(b) Overhanging beam<br><br>|A<br><br>C1<br><br>C1<br><br>B<br><br>NA<br><br>MB<br><br>By<br><br>Bx<br><br>(e) Propped cantilever beam<br><br>|
|A B<br><br>w0<br><br>By<br><br>MB<br><br>Bx<br><br>(c) Cantilever beam<br><br>w0|A B<br><br>P1<br><br>P2<br><br>Bx MB<br><br>By<br><br>MA Ay<br><br>Ax<br><br>P2<br><br>(f) Fixed beam<br><br>P1<br><br>|

Fig. 6.4

b. Sign convention

For the sake of consistency, it is necessary to adopt sign conventions for applied loading, shear forces, and bending moments. We will use the conventions shown in Fig. 6.5 which assume the following to be positive:

- • External forces that are directed downward; external couples that are directed clockwise.
- • Shear forces that tend to rotate a beam element clockwise.
- • Bending moments that tend to bend a beam element concave upward (the beam “smiles”).

| |Positive|Negative|
|---|---|---|
|External loads|P w C<br><br>|P w<br><br>C|
|Shear force|V<br><br>V<br><br>|V<br><br>V<br><br>|
|Bending moment|M M<br><br>|M M|

Fig. 6.5 Sign conventions for external loads, shear force, and bending moment.

The main disadvantage of the above conventions is that they rely on such adjectives as “downward,” “clockwise,” and so on. To eliminate this obstacle, a convention based upon a Cartesian coordinate system is sometimes used.

c. Shear force and bending moment

equations and diagrams

The determination of the internal force system at a given cross section in a member has been discussed in Art. 6.2. The goal of beam analysis is to determine the shear force and bending moment at every cross section of the beam. Particular attention is paid to ﬁnding the values and the locations of the maximum shear force and the maximum bending moment. The results enable the engineer to select a suitable beam that is capable of supporting the applied loads.

The equations that describe the variation of the shear force (V) and the bending moment (M) with the location of the cross section are called the shear force and bending moment equations, or simply, the V- and M-equations. These equations are always dependent on sign conventions, such as shown in Fig. 6.5.

When the V- and M-equations are drawn to scale, the results are called the shear force and bending moment diagrams, or simply, the V- and M-diagrams. After these diagrams have been drawn, the maximum shear force and the maximum bending moment can usually be found by inspection or with minimal computation.

In the following sample problems, we explain the procedures for deriving the V- and M-equations and for plotting the V- and M-diagrams.

|Sample Problem 6.3<br><br>The simply supported beam shown in Fig. (a) carries two concentrated loads. (1) Derive the expressions for the shear force and the bending moment for each segment of the beam. (2) Sketch the shear force and bending moment diagrams. Neglect the weight of the beam. Note that the support reactions at A and D have been computed and are shown in Fig. (a).<br><br>RA = 18 kN<br><br>x<br><br>y<br><br>D<br><br>|A<br><br>|B|C| |
|---|---|---|---|
| | | | |
| | | | |
<br><br>RD = 24 kN<br><br>1 2 3<br><br>(a)<br><br>2 m 3 m 2 m<br><br>14 kN 28 kN<br><br>Solution<br><br>Part 1<br><br>The determination of the expressions for V and M for each of the three beam segments (AB, BC, and CD) is explained below.<br><br>Segment AB (0<x <2m) Figure (b) shows the FBDs for the two parts of the beam that are separated by section 1, located within segment AB. Note that we show V and M acting in their positive directions according to the sign conventions in Fig. 6.5. Because V and M are equal in magnitude and oppositely directed on the two FBDs, they can be computed using either FBD. The analysis of the FBD of the part to the left of section 1 yields<br><br>Fy = 0 +  18 − V = 0 V = +18 kN Answer ME = 0 + − 18x + M = 0 M = +18x kN · m Answer<br><br>3 m 2 m<br><br>14 kN 28 kN<br><br>18 kN 24 kN<br><br>D<br><br>B C<br><br>A<br><br>(b) FBDs<br><br>x<br><br>V<br><br>E<br><br>E<br><br>M M<br><br>V<br><br>|
|---|

|2 m<br><br>28 kN<br><br>24 kN<br><br>C D<br><br>M<br><br>F<br><br>| |
|---|
<br><br>(c) FBDs<br><br>2 m<br><br>14 kN<br><br>18 kN<br><br>A B<br><br>M<br><br>V<br><br>V F<br><br>x<br><br>Segment BC (2m<x <5m) Figure (c) shows the FBDs for the two parts of the beam that are separated by section 2, an arbitrary section within segment BC. Once again, V and M are assumed to be positive according to the sign conventions in Fig. 6.5. The analysis of the part to the left of section 2 gives<br><br>Fy = 0 +  18 − 14 − V = 0<br><br>V = +18 − 14 = +4 kN Answer MF = 0 + − 18x + 14(x − 2) + M = 0 M = +18x − 14(x − 2) = 4x + 28 kN · m Answer<br><br>Segment CD (5m< x <7m) Section 3 is used to ﬁnd the shear force and bending moment in segment CD. The FBDs in Fig. (d) again show V and M acting in their positive directions. Analyzing the portion of the beam to the left of section 3, we obtain<br><br>Fy = 0 +  18 − 14 − 28 − V = 0<br><br>V = +18 − 14 − 28 = −24 kN Answer MG = 0 + − 18x + 14(x − 2) + 28(x − 5) + M = 0<br><br>M = +18x − 14(x − 2) − 28(x − 5) = −24x + 168 kN · m Answer<br><br>24 kN<br><br>D<br><br>M V<br><br>G<br><br>2 m 3 m<br><br>14 kN 28 kN<br><br>18 kN<br><br>A B C<br><br>M<br><br>V<br><br>x<br><br>G<br><br>(d) FBDs<br><br>Part 2<br><br>The shear force and bending moment diagrams in Figs. (f) and (g) are the plots of the expressions for V and M derived in Part 1. By placing these plots directly below the sketch of the beam in Fig. (e), we establish a clear visual relationship between the diagrams and locations on the beam.|
|---|

|(g) Shear force and bending moment diagrams<br><br>x<br><br>(e)<br><br>4<br><br>18<br><br>(f) –24 M (kN·m)<br><br>V (kN)<br><br>x<br><br>+48<br><br>+36<br><br>2 m<br><br>y<br><br>A<br><br>3 m<br><br>14 kN<br><br>18 kN<br><br>28 kN<br><br>24 kN<br><br>B C<br><br>2 m<br><br>D<br><br>x<br><br>An inspection of the V-diagram reveals that the largest shear force in the beam is −24kN and that it occurs at every cross section of the beam in segment CD. From the M-diagram we see that the maximum bending moment is +48kN · m, which occurs under the 28-kN load at C. Note that at each concentrated force the V-diagram “jumps” by an amount equal to the force. Furthermore, there is a discontinuity in the slope of the M-diagram at each concentrated force.<br><br>Sample Problem 6.4<br><br>The simply supported beam shown in Fig. (a) is loaded by the clockwise couple C0 at B. (1) Derive the shear force and bending moment equations; and (2) draw the shear force and bending moment diagrams. Neglect the weight of the beam. The support reactions A and C have been computed, and their values are shown in Fig. (a).<br><br>Solution<br><br>Part 1<br><br>Due to the presence of the couple C0, we must analyze segments AB and BC separately.<br><br>Segment AB (0< x < 3L/4) Figure (b) shows the FBD of the part of the beam to the left of section 1 (we could also use the part to the right). Note that V and M are assumed to act in their positive directions according to the sign conventions in Fig. 6.5. The equilibrium equations for this portion of the beam yield|
|---|

|Fy = 0 +  −<br><br>C0<br><br>L − V = 0 V = −<br><br>C0 L<br><br>Answer<br><br>MD = 0 +<br><br>C0 L<br><br>x + M = 0<br><br>M = −<br><br>C0x L<br><br>Answer<br><br>Segment BC (3L/4<x <L) Figure (c) shows the FBD of the portion of the beam to the left of section 2 (the right portion could also be used). Once again, V and M are assumed to act in their positive directions. Applying the equilibrium equations to the segment, we obtain<br><br>Fy = 0 +  −<br><br>C0<br><br>L − V = 0 V = −<br><br>C0 L<br><br>Answer<br><br>ME = 0 +<br><br>C0 L<br><br>x − C0 + M = 0 M = −<br><br>C0 L<br><br>x + C0 Answer<br><br>Part 2<br><br>The shear force and bending moment diagrams shown in Figs. (d) and (e), are obtained by plotting the expressions for V and M found in Part 1. From the V-diagram, we see that the shear force is the same for all cross sections of the beam. The M-diagram shows a jump of magnitude C0 at the point of application of the couple.<br><br>x<br><br>C<br><br>1 2<br><br>C0 L<br><br>C0<br><br>L<br><br>y<br><br>x<br><br>(b)<br><br>C0 L<br><br>D<br><br>V<br><br>M<br><br>x<br><br>(c)<br><br>C0 L<br><br>E<br><br>V<br><br>M<br><br>3<br><br>4<br><br><br>L<br><br>L C0<br><br>A<br><br>RA =<br><br>C0 L<br><br>B<br><br>RC =<br><br>3<br><br>4<br><br><br>FBDs<br><br>(a)<br><br>x<br><br>C0<br><br>3<br><br>4<br><br><br>L 1 4<br><br>L<br><br>V<br><br>x<br><br>C0 L<br><br>–<br><br>C0 L<br><br>C0 L<br><br>M<br><br>3<br><br>4<br><br><br>C0<br><br>x<br><br>1 4<br><br>C0<br><br>–<br><br>0<br><br>(e)<br><br>(d)<br><br>Shear force and bending moment diagrams<br><br>|
|---|

|Sample Problem 6.5<br><br>The cantilever beam in Fig. (a) carries a triangular load, the intensity of which varies from zero at the left end to 360 lb/ft at the right end. In addition, a 1000-lb upward vertical load acts at the free end of the beam. (1) Derive the shear force and bending moment equations; and (2) draw the shear force and bending moment diagrams. Neglect the weight of the beam.<br><br>A<br><br>y<br><br>x B<br><br>360 lb/ft<br><br>1000 lb<br><br>12 ft<br><br>(a)<br><br>Solution<br><br>The FBD of the beam is shown in Fig. (b). Note that the triangular load has been replaced by its resultant, which is the force 0.5(12)(360) = 2160 lb (area under the loading diagram) acting at the centroid of the loading diagram. The support reactions at B can now be computed from the equilibrium equations; the results are shown in Fig. (b).<br><br>|x 3<br><br>w = 30x lb/ft 15x2 lb<br><br>C x<br><br>M<br><br>(c)<br><br>V<br><br>2°| | |
|---|---|---|
|(d)<br><br>8.165 ft<br><br>3°|5443|–1160<br><br>3360|
<br><br>1<br><br>RB = 1160 lb<br><br>(b)<br><br>A<br><br>A<br><br>B<br><br>V (lb)<br><br>12 ft<br><br>2160 lb<br><br>8 ft<br><br>360 lb/ft<br><br>M(lb.ft)<br><br>MB =3360lb.ft<br><br>y<br><br>1000 lb<br><br>1000 lb<br><br>1000<br><br>x<br><br>x<br><br>x (e)<br><br>|
|---|

|Because the loading is continuous, the beam does not have to be divided into segments. Therefore, only one expression for V and one expression for M apply to the entire beam.<br><br>Part 1<br><br>Figure (c) shows the FBD of the part of the beam that lies to the left of section 1. Letting w be the intensity of the loading at section 1, as shown in Fig. (b), we have from similar triangles, w/x = 360/12, or w = 30x lb/ft. Now the triangular load in Fig. (c) can be replaced by its resultant force 15x2 lb acting at the centroid of the loading diagram, which is located at x/3 ft from section 1. The shear force V and bending moment M acting at section 1 are shown acting in their positive directions according to the sign convention in Fig. 6.5. Equilibrium analysis of the FBD in Fig. (c) yields<br><br>Fy = 0 +  1000 − 15x2 − V = 0<br><br>V = 1000 − 15x2 lb Answer<br><br>MC = 0 + − 1000x + 15x2<br><br>x 3 + M = 0<br><br>M = 1000x − 5x3 lb·ft Answer<br><br>Part 2<br><br>Plotting the expressions for V and M found in Part 1 gives the shear force and bending moment diagrams shown in Figs. (d) and (e). Observe that the shear force diagram is a parabola and the bending moment diagram is a third-degree polynomial in x.<br><br>The location of the section where the shear force is zero is found from<br><br>V = 1000 − 15x2 = 0 which gives<br><br>x = 8.165ft<br><br>The maximum bending moment occurs where the slope of the M-diagram is zero—that is, where dM /dx = 0. Differentiating the expression for M, we obtain<br><br>dM dx = 1000 − 15x2 = 0<br><br>which again yields x = 8.165ft. (In the next article, we will show that the slope of the bending moment diagram is always zero at a section where the shear force vanishes.) Substituting this value of x into the expression for M, we ﬁnd that the maximum bending moment is<br><br>Mmax = 1000(8.165) − 5(8.165)3 = 5443lb·ft|
|---|

![image 43](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile43.png>)

###### Problems

6.21–6.38 For the beam shown, derive the expressions for V and M, and draw the shear force and bending moment diagrams. Neglect the weight of the beam.

y

y

w0

C0

B

A

x

x

A

B

L

L

###### Fig. P6.21 Fig. P6.22

y

y

w0

w0

A

x

x

B

L

A L

B

###### Fig. P6.23 Fig. P6.24

y

y

P

60 lb/ft

C

A B

300lb·ft

x

x

B

a b

9 ft

A

###### Fig. P6.25 Fig. P6.26

y

y

200 kN/m

120 lb/ft

A

x

x

C

B

B C

A

8ft 6ft

2m 2m

###### Fig. P6.27 Fig. P6.28

y

y

120lb/ft

50 kN

75kN·m

C

C

A

x

x A

| |
|---|

B

B

3ft 6ft

2m 3m

###### Fig. P6.29 Fig. P6.30

6.21–6.42 Problems 301

y

y

80kN/m

8 kN/m

12kN⋅m

C B

A C x

A

x

|B|
|---|

2m 2m

5m 3m

###### Fig. P6.31 Fig. P6.32

y

y

4 kN/m

P

P

|B|C|
|---|---|
| | |

2 kN/m

D

A

x

x

A B C

L 3

L 3

L 3

2 m 3 m

###### Fig. P6.33 Fig. P6.34

y

y

12 kips

30 kN 50 kN

48 kip·ft

D x

D

x

A

A

B C

C

B

1 m 3 m 2 m

4 ft 4 ft 4 ft

###### Fig. P6.35 Fig. P6.36

y

y

400 lb

| | |900 lb<br><br>60 lb/ft| | | | | | |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

800 lb/ft

D

A

A

D

x

x

B

B

C

C

4 ft 8 ft 6 ft

2 ft 4 ft 2 ft

###### Fig. P6.37 Fig. P6.38

6.39–6.40 Derive the shear force and the bending moment as functions of the angle θ for the arch shown. Neglect the weight of the arch.

- O

A

- P B

R

θ

R

B Q

| | | |
|---|---|---|
| | | |

A

θ

| | |C|
|---|---|---|
| | | |

P

###### Fig. P6.39 Fig. P6.40

6.41 The 24-ft timber ﬂoor joist is designed to carry a uniformly distributed load. Because only 16-ft timbers are available, the joist is to be fabricated from two pieces connected by a nailed joint D. Determine the distance b for the most advantageous position of the joint D, knowing that nailed joints are strong in shear but weak in bending.

y

y

- 1

1

L

- 2

|x|P|
|---|---|
| | |

w0 lb/ft

A

B

x

- Case 1

- Case 2

A x

| | | | |
|---|---|---|---|

D C

###### L 2

B

b

y

16 ft 8 ft

P

x

A

B

x

| | |
|---|---|
|L<br><br>|L|

![image 44](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile44.png>)

2 2

Detail of joint at D

###### Fig. P6.41 Fig. P6.42

6.42 For the beam AB shown in Cases 1 and 2, derive and plot expressions for the shear force and bending moment acting on section 1 in terms of the distance x (0 < x < L). [Note: Case 1 results in the conventional V- and M-diagrams, in which the loads are ﬁxed and the location of the section varies; the diagrams for Case 2 (called inﬂuence diagrams) show the variation of V and M at a ﬁxed section as the location of the load is varied.]

*6.4 Area Method for Drawing

V- and M-Diagrams

There are useful relationships between the load diagram, the shear force diagram, and the bending moment diagram, which are derivable from the equilibrium equations. Utilizing these relationships, we can plot the shear force diagram directly from the load diagram, and then sketch the bending moment diagram directly from the shear force diagram. This technique, called the area method, enables us to draw the V- and M-diagrams without having to go through the tedium of writing the V- and M-equations. We ﬁrst consider beams subjected to distributed loading and then discuss concentrated forces and couples.

###### a. Distributed loading

Consider the beam in Fig. 6.6(a) that is subjected to a line load of intensity w(x), where w(x) is assumed to be a continuous function. The free-body diagram of an inﬁnitesimal element of the beam, located at the distance x from the left end, is shown in Fig. 6.6(b). In addition to the distributed load w(x), the segment carries a shear force and a bending moment at each end section, which are denoted by V and M at the left end and by V + dV and M + dM at the right end. The inﬁnitesimal differences dV and dM represent the changes that occur over the differential length dx of the element. Observe that all forces and bending moments are assumed to act in the positive directions, as deﬁned in Fig. 6.5.

The force equation of equilibrium for the element is

###### Fy = 0 +  V − w dx − (V + dV) = 0

y

w(x)

x

| | | |
|---|---|---|

x

dx

(a)

wdx

dx V 2

M M+dM

O

x

dx V+dV

(b)

###### Fig. 6.6

from which we get

dV dx

(6.1)

w = −

The moment equation of equilibrium yields

dx

2 = 0 After canceling M and dividing by dx, we get

MO = 0 + − M − V dx + (M + dM) + wdx

dM dx +

wdx

−V +

2 = 0

Because dx is inﬁnitesimal, the last term can be dropped (this is not an approximation), yielding

dM dx

(6.2)

V =

Equations (6.1) and (6.2) are called the differential equations of equilibrium for beams. The following ﬁve theorems relating the load, the shear force, and bending moment diagrams follow from these equations.

- 1. The load intensity at any section of a beam is equal to the negative of the slope of the shear force diagram at that section. Proof—follows directly from Eq. (6.1).
- 2. The shear force at any section is equal to the slope of the bending moment diagram at that section. Proof—follows directly from Eq. (6.2).
- 3. The difference between the shear force at two sections of a beam is equal to the negative of the area under the load diagram between those two sections. Proof—integrating Eq. (6.1) between sections A and B in Fig. 6.7, we obtain

xB

xA

dV dx

dx = VB − VA = −

xB

xA

wdx

Recognizing that the integral on the right-hand side of this equation represents the area under the load diagram between A and B, we get

VB − VA = −area of w-diagram BA Q.E.D.

For computational purposes, a more convenient form of this equation is

VB = VA − area of w-diagram BA (6.3)

Note that the signs in Eq. (6.3) are correct only if xB > xA.

- 4. The difference between the bending moments at two sections of a beam is equal to the area of the shear force diagram between these two sections.

y

###### w(x)

x

| | | |
|---|---|---|

A B

xA

xB

w(x)

VA

MA MB

B

x

A

VB

###### Fig. 6.7

Proof—integrating Eq. (6.2) between sections A and B (see Fig. 6.7), we have

xB

xB

dM dx

dx = MB − MA =

###### V dx

xA

xA

Because the right-hand side of this equation is the area of the shear force diagram between A and B, we obtain

MB − MA = area of V-diagram BA Q.E.D.

We ﬁnd it convenient to use this equation in the form

###### MB = MA + area of V-diagram BA (6.4)

The signs in Eq. (6.4) are correct only if xB > xA.

- 5. If the load diagram is a polynomial of degree n, then the shear force diagram is a polynomial of degree (n + 1), and the bending moment diagram is a polynomial of degree (n + 2). Proof—follows directly from the integration of Eqs. (6.1) and (6.2).

The area method for drawing shear force and bending moment diagrams is a direct application of the foregoing theorems. For example, consider the beam segment shown in Fig. 6.8(a), which is 2m long and is subjected to a uniformly distributed load w=300N/m. Figure 6.8(b) shows the steps required in the construction of the shear force and bending moment diagrams for the segment, given that the shear force and the bending moment at the left end are VA = +1000 N and MA = +3000 N · m.

y

w = +300 N/m

VA = 1000 N

Area = +600 N

MB

MA=3000N·m

B

x

A

2 m

VB

(a)

|w = +300 N/m (const.)|w (N/m)<br><br>A B<br><br>x 2 m<br><br>+600 N<br><br>300|
|---|---|
| | |
|VA= +1000 N (given)|V (N)<br><br>A B<br><br>x<br><br>1000|
|VB = VA − area of w−diagram] AB<br><br>= 1000 − 600 = + 400N|V (N)<br><br>A B<br><br>x<br><br>1000<br><br>400|
|dV/dx = −w = −300 N/m (const.) V−diagram is a straight line<br><br>|+1400N·m<br><br>2 m<br><br>V (N)<br><br>A B<br><br>x<br><br>1000<br><br>400|
| | |
|MA = +3000N·m (given)|M(N·m)<br><br>A B<br><br>x<br><br>3000|
|MB = MA +area of V-diagram]AB<br><br>= 3000 + 1400 = +4400 N · m|4400<br><br>M(N·m)<br><br>A B<br><br>x<br><br>3000|
|(dM/dx)A = VA = +1000 N<br>(dM/dx)B = VB = +400 N<br>|A B<br><br>x<br><br>M(N·m)|
|M-diagram is a parabola|4400<br><br>A B<br><br>x<br><br>3000<br><br>M(N·m)<br><br>|

(b)

###### Fig. 6.8 Constructing shear force and bending moment diagrams for a beam segment.

###### b. Concentrated forces and couples

The area method for constructing shear force and bending moment diagrams described above for distributed loads can be extended to beams that are loaded by concentrated forces and/or couples. Figure 6.9 shows the free-body diagram of a beam element of inﬁnitesimal length dx containing a point A where a concentrated force PA and a concentrated couple CA are applied. The shear force and the bending acting at the left side of the element are denoted by VA− and MA−, whereas the notation VA+ and MA+ is used for the right side of the element. Observe that all forces and moments in Fig. 6.9 are assumed to be positive according to the sign conventions in Fig. 6.5.

PA

dx 2

y

VA–

MA+

–

MA

A

x

CA

VA+

dx

###### Fig. 6.9

The force equation of equilibrium gives

Fy = 0 +  VA− − PA − VA+ = 0

VA+ = VA− − PA (6.5)

Equation (6.5) indicates that a positive concentrated force causes a negative jump discontinuity in the shear force diagram at A (a concentrated couple does not affect the shear force diagram).

The moment equilibrium equation yields

dx

dx

MA = 0 + MA+ − MA− − CA − VA+

2 − VA−

2 = 0

Dropping the last two terms because they are inﬁnitesimals (this is not an approximation), we obtain

###### MA+ = MA− + CA (6.6)

Thus, a positive concentrated couple causes a positive jump in the bending moment diagram.

###### c. Summary

Equations (6.1)–(6.6), which are repeated below, form the basis of the area method for constructing shear force and bending moment diagrams without deriving the expressions for V and M. The area method is useful only if the areas under the load and shear force diagrams can be easily computed.

dV dx

(6.1)

w = −

dM dx

(6.2)

V =

VB = VA − area of w-diagram BA (6.3)

MB = MA + area of V-diagram BA (6.4)

VA+ = VA− − PA (6.5)

MA+ = MA− + CA (6.6)

Procedure for the Area Method The following steps outline the procedure for constructing shear force and bending moment diagrams by the area method:

- • Compute the support reactions from the free-body diagram (FBD) of the entire beam.
- • Draw the load diagram of the beam (which is essentially a FBD) showing the values of the loads, including the support reactions. Use the sign conventions in Fig. 6.5 to determine the correct sign of each load.
- • Working from left to right, construct the V- and M-diagrams for each segment of the beam using Eqs. (6.1)–(6.6).
- • When you reach the right end of the beam, check to see whether the computed values of V and M are consistent with the end conditions. If they are not, you have made an error in the computations.

At ﬁrst glance, using the area method may appear to be more cumbersome than plotting the shear force and bending moment equations. However, with practice you will ﬁnd that the area method is not only much faster but also less susceptible to numerical errors because of the self-checking nature of the computations.

|Sample Problem 6.6<br><br>The simply-supported beam in Fig. (a) supports a 30-kN concentrated force at B and a 40-kN·m couple at D. Sketch the shear force and bending moment diagrams by the area method. Neglect the weight of the beam.<br><br>4 m<br><br>y<br><br>A E<br><br>(a)<br><br>B<br><br>3 m 3 m<br><br>PB = 30 kN<br><br>CD = 40 kN·m<br><br>D<br><br>x<br><br>Solution<br><br>Load Diagram<br><br>The load diagram for the beam is shown in Fig. (b). The reactions at A and E are found from equilibrium analysis. The numerical value of each force and the couple is followed by a plus or minus sign in parentheses, indicating its sign as established by the sign conventions in Fig. 6.5.<br><br>4 m<br><br>y<br><br>A E<br><br>x<br><br>(b)<br><br>B<br><br>3 m 3 m<br><br>|D|
|---|
<br><br>CD =40kN·m(+)<br><br>PB = 30 kN (+)<br><br>RA = 14 kN (–) RE = 16 kN (–)<br><br>0<br><br>14<br><br>–16<br><br>x<br><br>(c)<br><br>56 f<br><br>48 h<br><br>8 e<br><br>0<br><br>i<br><br>x (d)<br><br>M(kN·m)<br><br>V (kN)<br><br>g<br><br>a b<br><br>c d<br><br>+56 kN· m<br><br>–48 kN·m –48 kN·m<br><br>Shear Force Diagram<br><br>We now explain the steps used to construct the shear force diagram in Fig. (c). From the load diagram, we see that there are concentrated forces at A, B, and E|
|---|

|that will cause jumps in the shear force diagram at these points. Therefore, our discussion of shear force must distinguish between sections of the beam immediately to the left and to the right of each of these points.<br><br>We begin by noting that VA− = 0 because no loading is applied to the left of A. We then proceed across the beam from left to right, constructing the diagram as we go:<br><br>VA+ = VA− − RA = 0 − (−14) = +14 kN<br><br>Plot point a.<br><br>VB− = VA+ − area of w-diagram BA = 14 − 0 = −14 kN<br><br>Plot point b.<br><br><br>Because w = −dV/dx = 0 between A and B, the slope of the V-diagram is zero between these points.<br><br>Connect a and b with a horizontal straight line.<br><br>VB+ = VB− − PB = 14 − (+30) = −16 kN<br><br>Plot point c. VE− = VB+ − area of w-diagram EB = −16 − 0 = −16 kN<br>Plot point d.<br><br><br>Noting that w = −dV/dx = 0 between B and E, we conclude that the slope of the V-diagram is zero in segment BE.<br><br>Connect c and d with a horizontal straight line.<br><br>Because there is no loading to the right of E, we should ﬁnd that VE+ = 0.<br><br>VE+ = VE− − RE = −16 − (−16) = 0 Checks!<br><br>Bending Moment Diagram<br><br>We now explain the steps required to construct the bending moment diagram shown in Fig. (d). Because the applied couple is known to cause a jump in the bending moment diagram at D, we must distinguish between the bending moments at sections just to the left and to the right of D. Before proceeding, we compute the areas under the shear force diagram for the different beam segments. The results of these computations are shown in Fig. (c). Observe that the areas are either positive or negative, depending on the sign of the shear force.|
|---|

|We begin our construction of the bending moment diagram by noting that MA = 0 (there is no couple applied at A).<br><br>Plot point e.<br><br>Proceeding across the beam from left to right, we generate the moment diagram in Fig. (d) in the following manner:<br><br>MB = MA + area of V-diagram BA = 0 + (+56) = 56 kN · m Plot point f.<br><br>The V-diagram shows that the shear force between A and B is constant and positive. Therefore, the slope of the M-diagram between these two sections is also constant and positive (recall that dM/dx = V).<br><br>Connect e and f with a straight line.<br><br>MD− = MB + area of V-diagram DB = 56 + (−48) = 8kN · m Plot point g.<br><br>Because the slope of the V-diagram between B and D is negative and constant, the M-diagram has a constant, negative slope in this segment.<br><br>Connect f and g with a straight line.<br><br>MD+ = MD− + CD = 8 + (+40) = 48 kN · m<br><br>Plot point h.<br><br>Next, we note that ME = 0 (there is no couple applied at E). Our computations based on the area of the V-diagram should verify this result.<br><br>ME = MD+ + area of V-diagram ED = 48 + (−48) = 0 Checks! Plot point i.<br><br>The shear force between D and E is negative and constant, which means that the slope of the M-diagram for this segment is also constant and negative.<br><br>Connect h and i with a straight line.|
|---|

|Sample Problem 6.7<br><br>The overhanging beam in Fig. (a) carries two uniformly distributed loads and<br><br>2 ft<br><br>y<br><br>A<br><br>E<br><br>x<br><br>1 ft 4 ft 2 ft<br><br>C<br><br>400 lb/ft<br><br>PC = 400 lb<br><br>200 lb/ft<br><br>(a)<br><br>D<br><br>B<br><br>a concentrated load. Using the area method, draw the shear force and bending moment diagrams for the beam. Neglect the weight of the beam.<br><br>2 ft<br><br>A E<br><br>x<br><br>1 ft 2 ft<br><br>B C D<br><br>400 lb/ft (+) PC = 400 lb (+) 200 lb/ft (+)<br><br>d<br><br>720<br><br>320<br><br>V (lb)<br><br>0<br><br>+720 lb·ft<br><br>4 ft<br><br>RB = 1520 lb (–)<br><br>(b)<br><br>RD = 880 lb (–)<br><br>–800<br><br>–480<br><br>400<br><br>x (ft)<br><br>d = 1.6 4 – d = 2.4<br><br>0<br><br>M (lb·ft)<br><br>–800<br><br>–80<br><br>176<br><br>–400<br><br>x (ft)<br><br>(d)<br><br>F<br><br>–576 lb·ft<br><br>+400 lb·ft<br><br>–800 lb·ft<br><br>c d a<br><br>g<br><br>h<br><br>f b<br><br>i<br><br>j<br><br>l<br><br>m<br><br>n<br><br>e<br><br>k<br><br><br>+256 lb·ft<br><br>(c)<br><br>Solution<br><br>Load Diagram<br><br>The load diagram for the beam is shown in Fig. (b); the reactions at B and D are determined by equilibrium analysis. Each of the numerical values is followed by a plus or minus sign in parentheses, determined by the sign conventions established in Fig. 6.5. The signiﬁcance of the section labeled F will become apparent in the discussion that follows.<br><br>Shear Force Diagram<br><br>The steps required to construct the shear force diagram shown in Fig. (c) are now detailed. From the load diagram, we see that there are concentrated forces at B, C, and D, which means that there will be jumps in the shear diagram at these points. Therefore, we must differentiate between the shear force immediately to the left and to the right of each of these points.|
|---|

|We begin our construction of the V-diagram by observing that VA = 0 because no force is applied at A.<br><br>Plot point a.<br><br>VB− = VA − area of w-diagram BA = 0 − (+400)(2) = −800 lb<br><br>Plot point b.<br><br>We observe from Fig. (b) that the applied loading between A and B is constant and positive, so the slope of the shear diagram between the two cross sections is constant and negative (recall that dV/dx = −w).<br><br>Connect a and b with a straight line.<br><br>VB+ = VB− − RB = −800 − (−1520) = 720 lb<br><br>Plot point c. VC− = VB+ − area of w-diagram CB = 720 − 0 = 720 lb<br>Plot point d.<br><br><br>Because w = −dV/dx = 0 between B and C, the slope of the V-diagram is zero in this segment.<br><br>Connect c and d with a horizontal straight line.<br><br>VC+ = VC− − PC = 720 − (+400) = 320 lb<br><br>Plot point e.<br><br>VD− = VC+ − area of w-diagram C D = 320 − (+200)4 = −480 lb<br><br>Plot point f.<br><br><br>Because the loading between C and D is constant and positive, the slope of the V-diagram between these two sections is constant and negative.<br><br>Connect e and f with a straight line.<br><br>Our computations have identiﬁed an additional point of interest—the point where the shear force is zero, labeled F on the load diagram in Fig. (b). The location of F can be found from<br><br>VF = VC+ − area of w-diagram C F = 320 − (+200)d = 0 which gives d = 1.60 ft, as shown in Fig. (c). Continuing across the beam, we have<br><br>VD+ = VD− − RD = −480 − (−880) = 400 lb<br><br>Plot point g.|
|---|

|Next, we note that VE = 0 (there is no force acting at E). The computation based on the area of the load diagram should verify this result:<br><br>VE = VD+ − area of w-diagram ED = 400 − (+200)2 = 0 Checks! Plot point h.<br><br>From Fig. (b), we see that the applied loading between D and E is constant and positive. Therefore the slope of the V-diagram between these two cross sections is constant and negative.<br><br>Connect g and h with a straight line. This completes the construction of the shear force diagram.<br><br>Bending Moment Diagram<br><br>We now explain the steps required to construct the bending moment diagram shown in Fig. (d). Because there are no applied couples, there will be no jumps in the M-diagram. The areas of the shear force diagram for the different segments of the beam are shown in Fig. (c).<br><br>We begin by noting that MA = 0 because no couple is applied at A.<br><br>Plot point i.<br><br>Proceeding from left to right across the beam, we construct the bending moment diagram as follows:<br><br>MB = MA + area of V-diagram BA = 0 + (−800) = −800 lb · ft Plot point j.<br><br>We note from Fig. (c) that the V-diagram between A and B is a ﬁrst-degree polynomial (inclined straight line). Therefore, the M-diagram between these two cross sections is a second-degree polynomial—that is, a parabola. From dM/dx = V, we see that the slope of the M-diagram is zero at A and −800lb/ft at B.<br><br>Connect i and j with a parabola that has zero slope at i and negative slope at j. The parabola will be concave downward.<br><br>MC = MB + area of V-diagram CB = −800 + (+720) = −80 lb · ft Plot point k.<br><br>Because the V-diagram is constant and positive between B and C, the slope of the M-diagram is constant and positive between those two cross sections.<br><br>Connect j and k with a straight line.<br><br>MF = MC + area of V-diagram C F = −80 + (+256) = +176 lb · ft Plot point l.|
|---|

|Using V = dM/dx, we know that the slope of the M-diagram is +320lb/ft at C and zero at F, and that the curve is a parabola between these two cross sections.<br><br>Connect k and l with a parabola that has positive slope at k and zero slope at l. The parabola will be concave downward.<br><br>MD = MF + area of V-diagram F D = 176 + (−576) = −400 lb · ft Plot point m.<br><br>The M-diagram between F and D is again a parabola, with a slope of zero at F and −480lb/ft at D.<br><br>Connect l and m with a parabola that has zero slope at l and negative slope at m. The parabola will be concave downward.<br><br>Next, we note that ME = 0 because no couple is applied at E. Our computation based on the area of the V-diagram should verify this result.<br><br>ME = MD + area of V-diagram ED = −400 + (+400) = 0 Checks! Plot point n.<br><br>From the familiar arguments, the M-diagram between D and E is a parabola with a slope equal to +400lb/ft at D and zero slope at E.<br><br>Connect m and n with a parabola that has positive slope at m and zero slope at n. The parabola will be concave downward.<br><br>This completes the construction of the bending moment diagram. It is obvious in Fig. (d) that the slope of the M-diagram is discontinuous at j and m. Not so obvious is the slope discontinuity at k: From dM/dx = V, we see that the slope of the M-diagram to the left of k equals +720lb/ft, whereas to the right of k the slope equals +320lb/ft. Observe that the slope of the M-diagram is continuous at l because the shear force has the same value (zero) to the left and to the right of l.|
|---|

![image 45](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile45.png>)

###### Problems

###### 6.43–6.56 Construct the shear force and bending moment diagrams for the beam shown by the area method. Neglect the weight of the beam.

20 kN

40 kN 60 kN

5 kN/m

30kN.m

B C D

A

E

A

30kN.m

B C

3 m 3 m

2 m 2 m 2 m 2 m

###### Fig. P6.43 Fig. P6.44

|120 lb/ft| | | | | | | |900 lb| | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

10 kN/m

25 kN.m

E C

A

A

C

B

B

D

1 m 1 m

8 ft 4 ft

3 m 2 m

###### Fig. P6.45 Fig. P6.46

100 lb

|120 lb/ft| | | |
|---|---|---|---|
| | | | |

120 lb/ft

- 2 ft 2 ft 2 ft

A

B

D

C

|400 lb/ft| | |
|---|---|---|
| | | |

|200 lb/ft| | | | | |
|---|---|---|---|---|---|
| | | | | | |

2000 lb

1000 lb

5 ft 10 ft 10 ft

A

B

D

C

Fig. P6.47 Fig. P6.48

|7 kN/m| | | | | | | | | | | | | |7 kN/m| | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | |

14 kN/m

- 3 m 4 m 3 m

60 kN 40 kN/m

120kN.m

B

C

A E

D C

A

D

B

1m 1m 1m

3 m

###### Fig. P6.49 Fig. P6.50

750 lb

60 kN

|20 kN/m| | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

3000 lb.ft

120kN.m

D C

A

E C

A

B D

B

2 m 2 m 2 m 2 m

2 ft 3 ft 2 ft

###### Fig. P6.51 Fig. P6.52

6.43–6.61 Problems 317

960 lb/ft 440 lb/ft

960 lb/ft

30 kN 40 kN

|10 kN/m| | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

A D

###### A

E

B C D

B C

4 ft 8 ft 2 ft

2 m 2 m 1 m 3 m

###### Fig. P6.53 Fig. P6.54

400 lb/ft

1000 lb

200 lb/ft

B C

A

D

A

C D

Hinge

2 ft 2 ft 4 ft

B

2 ft 4 ft

2 ft

500 lb

###### Fig. P6.55 Fig. P6.56

###### 6.57–6.61 Draw the load and the bending moment diagrams that correspond to the given shear force diagram. Assume no couples are applied to the beam.

V (lb)

2 2400

3 2 2

V (lb)

3700

1000

1700

400

x (ft)

x (ft)

–3100

–4000

–4000

4 4 4 8

###### Fig. P6.57 Fig. P6.58

V (lb)

4 2 4 4 4

900

V (lb)

480

600

300

x (ft)

x (ft)

–360

–900

–780 2

6 3

–1380

###### Fig. P6.59 Fig. P6.60

V (kN)

10 2nd-degree curve

x (m)

–2

–8

2

3 1 1

###### Fig. P6.61

###### Part B: Cables

###### *6.5 Cables under Distributed Loads

###### a. General discussion

Flexible cables are used in numerous engineering applications. Common examples are power transmission lines and suspension bridges. The term ﬂexible means that the cables are incapable of developing internal forces other than tension. In earlier chapters we treated cables as two-force members; that is, the weights of the cables were neglected, and the loading consisted of end forces only. Here we consider the effects of distributed forces, such as the weight of the cable or the weight of a structure that is suspended from the cable. Concentrated loads are covered in the next article.

Figure 6.10(a) shows a cable that is suspended from its endpoints A and B. In order to support the distributed loading of intensity w, the cable must assume a curved shape. It turns out that the equation describing this shape is simpliﬁed if we place the origin of the xy-coordinate system at the lowest point O of the cable. We let s be the distance measured along the cable from O. The shape of the cable and the location of point O are generally unknown at the beginning of the analysis.

T

y

x

###### θ

B

C

s

A

y

T0 O

s

O

x

###### W

w

FBD

(a)

(b)

###### Fig. 6.10

The units of the load intensity w are lb/ft or N/m. The length can be measured in two ways: along the horizontal x-axis (w as a function of x) or along the cable (w as a function of s). Although these two cases must be treated separately, we ﬁrst consider the elements of the analyses that are common to both.

The free-body diagram (FBD) of a segment of the cable, extending from the lowest point O to an arbitrary point C, is shown in Fig. 6.10(b). The tensile forces in the cable at O and C are denoted by T0 and T, respectively; W is the resultant of the distributed loading; and θ represents the slope angle of the cable at C. The force equilibrium equations of the cable segment are

Fx = 0 −→+ T cosθ − T0 = 0 Fy = 0 +  T sinθ − W = 0

from which we obtain

###### T cosθ = T0 T sinθ = W (6.7)

The ﬁrst of Eqs. (6.7) shows that the horizontal component of the cable force, namely T cos θ, is constant throughout the cable. The solution of Eqs. (6.7) for θ and T yields

W T0

T = T02 + W2 (6.8)

tanθ =

###### b. Parabolic cable

Here we analyze the special case in which the loading is distributed uniformly along the horizontal; that is, w(x) = w0, where w0 is the constant load intensity. This case arises, for example, in the main cables of a suspension bridge [see

- Fig. 6.11(a)] where w0 represents the weight of the roadway per unit length. It is assumed that the roadway is connected to the main cables by a large number of vertical cables and that the weights of all cables are negligible compared to the weight of the roadway.

Taking Eqs. (6.8) as the starting point, we now derive several useful equations that describe the geometry of the cable and the variation of the tensile force within the cable.

θ and T as functions of x and T0 Because the resultant of the loading shown in

- Fig. 6.11(b) is W = w0x, Eqs. (6.8) become

w0x T0

T = T02 + (w0x)2 (6.9)

tanθ =

y as a function of x and T0 Substituting tan θ = dy/dx, the ﬁrst of Eqs. (6.9) can be written as dy/dx = w0x/T0. Upon integration, we get

w0x2 2T0

(6.10)

y =

C

Main cable

O

Roadway

w0

(a)

y

T

x

θ

C s

T0 O

w0

W

FBD (b)

###### Fig. 6.11

where the constant of integration was set equal to zero to satisfy the condition y = 0 when x = 0. Equation (6.10), which represents a parabola with its vertex at O, could also be obtained from a moment equilibrium equation using the FBD in Fig. 6.11(b).

s as a function of x and T0 It is often necessary to compute the length s of the cable between points O and C in Fig. 6.11(b). The inﬁnitesimal length of the cable is

2

dy dx

ds = dx2 + dy2 = 1 +

###### dx (a)

Substituting dy/dx = w0x/T0 and integrating, we obtain

2

x

w0x T0

###### dx (6.11)

s(x) =

1 +

0

Therefore, the length of the cable between points O and C is (see a table of integrals)

2

w0x T0

x 2

s(x) =

1 +

ln

###### (6.12)

2

- 1

- 2

 w0x T0 + 1 +

w0x T0

T0 w0

+

###### c. Catenary cable

Consider a homogeneous cable that carries no load except its own weight. In this case, the loading is uniformly distributed along the length of the cable; that is, w(s)=w0, where w0 is the weight of the cable per unit length, and the distance s is measured along the cable. Therefore, the resultant of the loading shown in Fig. 6.10(b) is W =w0s. The following useful relationships can now be derived from Eqs. (6.8).

###### θ and T as functions of s and T0 Substituting W = w0s into Eqs. (6.8) gives

w0s T0

T = T02 + (w0s)2 (6.13)

tanθ =

s as a function of x and T0 We start with Eq. (a), which can be written as (dy/dx)2 = (ds/dx)2 −1. Substituting dy/dx = tanθ = w0s/T0, and solving for dx, yields

ds

###### (b)

dx =

2

w0s T0

1 +

Using a table of integrals, Eq. (b) yields

ln

  (6.14)

2

s

w0s T0 + 1 +

w0s T0

T0 w0

x(s) =

dx =

0

Solving this equation for s gives

w0x T0

T0 w0

(6.15)

s(x) =

sinh

The functions sinhu and coshu, called the hyperbolic sine and hyperbolic cosine, respectively, are deﬁned as

1 2

1 2

eu + e−u It can be seen that the rules for differentiation are

eu − e−u coshu =

sinhu =

d du

d du

sinhu = coshu

coshu = sinhu

y as a function of x and T0 We substitute Eq. (6.15) into the ﬁrst equation of Eqs. (6.13), which yields tanθ = sinh(w0x/T0). Using tanθ = dy/dx, we obtain

w0x T0

dy = tanθ dx = sinh

dx

which gives

x

###### w0x

T0 w0

T0 − 1 (6.16) The curve represented by Eq. (6.16) is called a catenary.

y(x) =

dy =

cosh

0

If the slope of the catenary is small everywhere, then the curve differs very little from a parabola. As a proof of this statement, we note that if θ << 1, then dx = dscosθ ≈ ds. Consequently, w(s) ≈ w(x), which means that the weight of the cable may be approximated by a uniformly distributed loading along the horizontal. This approximation usually simpliﬁes the solution, because parabolic cables are generally easier to analyze than catenary cables.

T as a function of x and T0 According to Eq. (6.7), the tension in the cable is T = T0/cosθ. Utilizing the geometrical relationship cosθ =dx/ds, this becomes T = T0 ds/dx. On substituting for s from Eq. (6.15), we get

w0x T0

(6.17)

T = T0 cosh

###### d. Note on the solution of problems

There is no standard, step-by-step procedure for solving problems involving ﬂexible cables. The reason is that the solution method for every problem is highly dependent on the information that is given in the problem statement. However, here are two guidelines that are applicable in most situations and that may be helpful.

- 1. It is not always wise to depend entirely on Eqs. (6.9)–(6.17). More often than not, a good starting point is the free-body diagram of the entire cable, or a portion of it, similar to Figs. 6.10(b) or 6.11 (b). This FBD, in conjunction with Eqs. (6.9)–(6.17), should be used to formulate a method of analysis before proceeding to the actual computations.
- 2. Observe that point O, the origin of the coordinate system, and T0 appear in all of the cable equations. If the location of point O and/or T0 are not known, they should be determined ﬁrst.

|Sample Problem 6.8<br><br>The 36-m cable shown in Fig. (a) weighs 1.5kN/m. Determine the sag H and the<br><br>A<br><br>H<br><br>30 m<br><br>Length = 36 m O<br><br>B<br><br>(a)<br><br>maximum tension in the cable.<br><br>Solution<br><br>Method of Analysis<br><br>Because the loading is distributed along the cable, the shape of the cable is a catenary. The cable is obviously symmetric about the midpoint of AB, which means that the location of the lowest point O of the cable is known. From the second of Eqs. (6.13), we note that the maximum cable tension occurs at the endpoints, where s is a maximum.<br><br>We now draw the free-body diagram of the right half of the cable, shown in Fig. (b). Although we could use this FBD in the solution of the problem, it is easier to use Eqs. (6.15)–(6.17). However, the FBD is convenient for identifying the various terms that arise in the solution.<br><br>y<br><br>s<br><br>B<br><br>=<br><br>1<br><br>8<br><br>m<br><br>H O<br><br>w0 = 1.5 kN/m<br><br>B<br><br>(b) FBD of segment OB<br><br>x<br><br>15 m<br><br>T0<br><br>TB = Tmax s<br><br>By studying Eqs. (6.15)–(6.17), we conclude that the solution can be obtained by the following three steps.<br><br>Step 1: Equation (6.15)—Substitute w0 = 1.5 kN/m and the coordinates of B (s = 18 m, x = 15 m); solve for T0.<br>Step 2: Equation (6.16)—Substitute w0 = 1.5 kN/m, the coordinates of B (x = 15 m, y = H), and the value found for T0; solve for H.<br>Step 3: Equation (6.17)—Substitute w0 = 1.5 kN/m, x = 15 m, T = Tmax, and the value found for T0; solve for Tmax.<br><br><br>Mathematical Details<br><br>Step 1 Equation (6.15) is<br><br>s =<br><br>T0 w0<br><br>sinh<br><br>w0x T0 18 =<br><br>T0 1.5<br><br>sinh<br><br>1.5(15) T0<br><br>|
|---|

|This equation must be solved numerically. The result, which may be veriﬁed by substitution, is T0 = 21.13 kN.<br><br>Step 2<br><br>Equation (6.16) is<br><br>y =<br><br>T0 w0<br><br>cosh<br><br>w0x<br><br>T0 − 1 H =<br><br>21.13 1.5<br><br>cosh<br><br>1.5(15)<br><br>21.13 − 1 = 8.77 m Answer Step 3<br><br>Equation (6.17) is<br><br><br>T = T0 cosh<br><br>w0x T0 Tmax = 21.13cosh<br><br>1.5(15) 21.13 = 34.3 kN Answer<br><br>Sample Problem 6.9<br><br>Figure (a) shows a cable that carries the uniformly distributed load w0 = 80 lb/ft, where the distance is measured along the horizontal. Determine the shortest cable for which the cable tension does not exceed 10000lb, and ﬁnd the corresponding vertical distance H.<br><br>40 ft<br><br>200 ft<br><br>(a)<br><br>A<br><br>B<br><br>H O<br><br>w0 = 80 lb/ft<br><br>Solution<br><br>Method of Analysis<br><br>Because the loading is distributed uniformly over the horizontal distance, we know that the shape of the cable is parabolic. It is also apparent that the location of the lowest point O of the cable and the cable tension T0 at that point are not known. Therefore, the computation of these unknowns is addressed ﬁrst.<br><br>A good starting point is the free-body diagram of the entire cable, shown in Fig. (b). The forces appearing on this diagram are the cable tensions at the endpoints (TA and TB) and the resultant of the distributed load:|
|---|

|W=(80lb/ft)(200ft)=16000lb. According to the second equation of Eqs. (6.9), the tension in the cable increases with x (x is measured from the vertex of the parabola). It follows that the maximum cable tension occurs at B; that is, TB = 10000 lb, as shown in the ﬁgure. The FBD in Fig. (b) now contains three unknowns: the slope angles θA and θB and the tension TA, all of which could be computed from the three available equilibrium equations. It turns out that we need only θB, which can be obtained from the moment equation MA = 0.<br><br>40 ft<br><br>B<br><br>TB = 10 000 lb 200 ft<br><br>O<br><br>(b) FBD of entire cable<br><br>TA<br><br>100 ft<br><br>LB<br><br>W = 16 000 lb<br><br>sA<br><br>sB<br><br>LA<br><br>A<br><br>θB<br><br>θA<br><br>As the next step, we draw the FBD of the portion of the cable that lies to the right of point O, as shown in Fig. (c). Assuming that θB has already been computed, this FBD contains three unknowns: LB (which locates point O), T0, and H. Because there are also three equilibrium equations available, all the unknowns can now be calculated. The ﬁnal step is to calculate the length of the cable from Eq. (6.12).<br><br>B<br><br>TB = 10 000 lb<br><br>O<br><br>(c) FBD of segment OB<br><br>x W<br><br>|B<br><br>s| |H|
|---|---|---|
|LB<br><br>B = 80LB| | |
<br><br>T0<br><br>y<br><br>1<br>2LB<br><br><br>θB<br><br>Mathematical Details<br><br>From the FBD of the entire cable in Fig. (b), we obtain<br><br>MA = 0 + (10000sinθB)(200) − (10000cos θB)(40)<br><br>− (16000)(100) = 0 which reduces to<br><br>sinθB − 0.2cosθB − 0.8 = 0 The smallest positive root of this equation can be found by numerical methods. The result, which can be veriﬁed by substitution, is θB = 62.98◦.<br><br>From the FBD of segment OB in Fig. (c) we obtain<br><br>Fx = 0 T0 = TB cosθB = 10000cos 62.98◦ = 4543 lb|
|---|

|Note that this equation is identical to the ﬁrst equation of Eqs. (6.7). Using the FBD in Fig. (c), we also get<br><br>Fy = 0 80LB = TB sinθB = 10000sin 62.98◦ = 8908 lb<br><br>Therefore, LB = 8908/80 = 111.35 ft and LA = 200 − 111.35 = 88.65 ft. The FBD in Fig. (c) also gives<br><br>MO = 0 + TB sinθB(LB) − TB cosθB(H) − 80LB<br><br>LB<br><br>2 = 0 which, on substituting the values for TB, θB, and LB, becomes<br><br>10000sin62.98◦(111.35) − 10000cos 62.98◦(H) − 80<br><br>(111.35)2<br><br>2 = 0 Solving for H, we ﬁnd<br><br>H = 109.2 ft Answer<br><br>The length of each of the two cable segments can be computed from Eq. (6.12). For the segment AO, we substitute x = −LA = −88.65 ft, w0 = 80 lb/ft, and T0 = 4543 lb. Therefore, w0x/T0 = 80(−88.65)/4543 = −1.5611, and Eq. (6.12) becomes<br><br>s(−LA) =<br><br>−88.65 2<br><br>1 + (−1.5611)2<br><br>+<br><br>1<br><br>2<br><br><br>4543 80<br><br>ln (−1.5611) + 1 + (−1.5611)2<br><br>= − 117.0 ft<br><br>The negative result is due to the sign convention: The positive direction of s points to the right of O, whereas point A is to the left of O. Therefore, the length of segment OA is sA = 117.0 ft.<br><br>The length of segment OB is obtained by using x = LB = 111.35 ft in Eq. (6.12). Omitting the details of this computation, the result is sB = 163.1 ft. Hence the total length of the cable is<br><br>sA + sB = 117.0 + 163.1 = 280.1 ft Answer<br><br>If the length of the cable were smaller than 280.1ft, the maximum cable tension would exceed the limiting value of 10000lb.|
|---|

![image 46](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile46.png>)

###### Problems

- 6.62 Show that the tension acting at a point in a parabolic cable varies with the xy-coordinates of the point as

T(x, y) = w0x 1 + (x/2y)2 1/2 (x > 0)

- 6.63 The cable of the suspension bridge spans L = 120m with a sag H =

18m. The cable supports a uniformly distributed load of w0 N/m along the horizontal. If the maximum allowable force in the cable is 4MN, determine the largest permissible value of w0.

| | |
|---|---|
| | |

L /2 L /2

y

H

O

A B

x

Fig. P6.63, P6.64

- 6.64 The two main cables of the Akashi Kaikyo suspension bridge in Japan

have a span L = 1990m and a sag H = 233m. The loading on each cable is w0 = 444.7kN/m (without trafﬁc) along the horizontal. Determine the corresponding maximum force in one of the cables.

- 6.65 Cable AB supports the uniformly distributed load of 2kN/m. If the slope of the cable at A is zero, compute (a) the maximum tensile force in the cable; and (b) the length of the cable.

A

B

40m

60 m

2 kN/m

20 ft

80 ft

7.2 ft

A

B

W = 960 lb

O

Fig. P6.65 Fig. P6.66

- 6.66 A uniform 80-ft pipe that weighs 960lb is supported entirely by a cable AB of negligible weight. Determine the length of the cable and the maximum force in the cable. (Hint: First locate the point O where the cable is tangent to the pipe.)

50°

B 6.67 The cable AB supports a uniformly distributed load of 12lb/ft. Determine

the maximum force in the cable and the distance h.

- 6.68 The string attached to the kite weighs 0.4oz/ft. If the tension in the string is 2.8lb at O and 3.2lb at B, determine the length s of the string and the height H of the kite.

H

B

O

L

Fig. P6.68

- 6.69 Show that the tension acting at a point in a catenary cable varies with the y-coordinate of the point as T(y) = T0 + w0y.
- 6.70 A uniform cable weighing 15N/m is suspended from points A and B. The force in the cable at B is known to be 500N. Using the result of Prob. 6.69, calculate (a) the force in the cable at A; and (b) the span L.

L y

x

4 m

8 m

A

B

Fig. P6.70

- 6.71 The span L and the sag H of the cable AB are 100m and 10m, respec-

h

###### A

20°

12 lb/ft

60 ft

Fig. P6.67

L A B

tively. If the cable weighs 50N/m, determine the maximum force in the cable using (a) the equations of the catenary; and (b) the parabolic approximation. (c) Compute the percentage error in the parabolic approximation.

H

Fig. P6.71, P6.72

- 6.72 Determine the ratio H/L that minimizes the maximum force in the uniform cable AB of a given span L. (Hint: Minimize the maximum force with respect to T0.)
- 6.73 The cable of mass 1.8kg/m is attached to a rigid support at A and passes

18 m

over a smooth pulley at B. If the mass M = 40 kg is attached to the free end of the cable, ﬁnd the two values of H for which the cable will be in equilibrium. (Note: The smaller value of H represents stable equilibrium.)

A B

H

6.74 One end of cable AB is ﬁxed, whereas the other end passes over a smooth pulley at B. If the mass of the cable is 1.5kg/m and the sag is H =1.8 m, determine the mass M that is attached to the free end of the cable.

M

Fig. P6.73, P6.74

###### 6.75 The end of a water hose weighing 0.5lb/ft is pulled with a 40-lb force that is inclined at 14◦ to the horizontal. Determine the length s of the hose that is lifted off the ground and the corresponding horizontal distance L.

40 lb

A

14°

s

O

L

Fig. P6.75

###### 6.76 The 50-ft steel tape AB that weighs 2.4lb is used to measure the horizontal 7.5 lb

distance between points A and C. If the spring scale at B reads 7.5lb when the length of tape between A and C is 36ft, calculate the horizontal distance LAC between A and C to four signiﬁcant digits.

B C

A

LAC

###### 6.77 The cable AOB weighs 5.2N/m. When the horizontal 30-N force is applied to the roller support at B, the sag in the cable is 5m. Find the span L of the cable.

Fig. P6.76

L/2 L/2 B 30 N

A

5 m

O

Fig. P6.77

###### 6.78 The chain AB weighs 5lb/ft. If the force in the chain at B is 800lb, determine the length of the chain.

60 ft 60 ft

A C

45°

h

B

| | |
|---|---|
| | |

B

120 lb

A

20 ft

Fig. P6.78 Fig. P6.79

###### 6.79 The 120-lb trafﬁc light is suspended from two identical cables AB and BC, each weighing 0.75lb/ft. If the maximum allowable horizontal force exerted by a cable on a vertical post is 180lb, determine the shortest possible length of each cable and the corresponding vertical distance h.

###### *6.6 Cables under Concentrated Loads

###### a. General discussion

Sometimes a cable is called on to carry a number of concentrated vertical loads, such as in Fig. 6.12(a). If the weight of the cable is negligible compared to the applied loads, then each segment of the cable is a two-force member and the shape of the cable consists of a series of straight lines. The analysis of a cable loaded in this manner is similar to truss analysis, except that with cables the locations of the joints (i.e., points where the loads are applied) are sometimes unknown. As in the case of truss analysis, we can use the method of joints and/or the method of sections to determine the equilibrium equations. However, it is often necessary to include equations of geometric constraints in order to have enough equations to ﬁnd all the unknowns.

L

L1 L2 L3

B h2

s3

θ3

2

h1 h

s2

θ2

1

s1

θ1

W2

A

W1

(a)

y

y

y

T3

Ti+1

θi+1

θ3

T2

θ2

1 2 i

x

x

x

θ1

θ2

θi

T1

W1

W2

Ti Wi

T2

(b) FBDs

###### Fig. 6.12

If a cable has n segments, then there are (n −1) joints. For example, the cable in Fig. 6.12(a) has n = 3 segments, and (n − 1) = 2 joints, labeled 1 and 2. We use the following notation: si is the segment length; Li is the horizontal spacing of the loads; and θi is the angle between a segment and the horizontal, where i = 1, 2, . . . , n is the segment number. The vertical position of the ith joint, measured downward from end B, is denoted by hi, i = 1, 2, . . . , n − 1.

###### 6.6 Cables under Concentrated Loads 331

Figure 6.12(b) shows the FBDs for joints 1, 2, and an arbitrary joint i, i = 1, 2, . . . , n − 1. The equilibrium analysis of a cable with n segments involves calculating the force Ti and slope angle θi of each cable segment. Because the FBD of each joint yields two equilibrium equations, the total number of independent equilibrium equations for a cable with n segments is 2(n − 1). The equilibrium equations for joint i in Fig. 6.12(b) are

- Fx = 0 −→+ Ti+1 cosθi+1 − Ti cosθi = 0 (a)
- Fy = 0 +  Ti+1 sinθi+1 − Ti sinθi − Wi = 0 (b)

where i = 1, 2, . . . , n − 1. From Eq. (a) we see that the horizontal component Ti cosθi is the same for each segment. Labeling this component as T0, we can replace Eq. (a) with

Ti cosθi = T0 i = 1,2, ...,n (6.18) and Eq. (b) can be rewritten as

###### T0(tanθi+1 − tanθi) = Wi i = 1,2, ...,n − 1 (6.19)

Observe that Eqs. (6.19) represent (n − 1) equations that contain the (n +1) unknowns T0, θ1, θ2, . . . , θn. Therefore, we must obtain two additional independent equations before we can calculate all of the unknowns.

The source of the additional equations depends primarily on the nature of the problem. It is convenient to divide problems into two categories depending on whether the horizontal spacings of the loads (Li) or the lengths of the cable segments (si) are given and to discuss each category separately (we assume that the relative position of the supports—the distances h and L in Fig. 6.12(a)—are known).

Because Eqs. (6.18) and (6.19) have been derived from Fig. 6.12, the ﬁgure also deﬁnes the sign conventions that have been used in the derivations: tensile forces and counterclockwise angles measured from the horizontal are positive, and h is the vertical distance measured downward from the right-hand support B. These conventions also apply to the equations that are derived in the remainder of this article.

###### b. Horizontal spacings of the loads are given

Consider a cable with n segments for which the horizontal spacings of the loads (L1, L2, . . . , Ln) are given. For this case, the following geometric relationship can be obtained from Fig. 6.12(a):

n

Li tanθi (6.20)

h =

i=1

However, the problem is still not solvable, unless one additional piece of information is given. This information may take several forms. For example, the horizontal pull T0 or the maximum cable tension may be speciﬁed (both conditions

are relevant from a design viewpoint), the vertical position of one of the joints (e.g., h1) may be prescribed, or the total length of the cable may be known.

We should point out that, in general, the analysis involves the solution of simultaneous equations that are nonlinear in the angles θi. In many problems this difﬁculty can be avoided by considering an appropriate moment equation using the FBD of the entire cable (see Sample Problem 6.10) or the FBD of a section of the cable containing two or more joints. However, these moment equilibrium equations are not independent of Eqs. (6.18)–(6.20).

###### c. Lengths of the segments are given

Consider next a cable with n segments for which the lengths of the segments s1, s2, . . . , sn are known. For this case, Fig. 6.12(a) yields two independent geometric relationships:

n

n

si cosθi (6.21)

h =

si sinθi L =

i=1

i=1

These two equations, coupled with the (n − 1) equilibrium equations given in Eq. (6.19), can be solved for the (n+1) unknowns without the need for additional information. After T0, θ1, θ2, . . . , θn have been computed, the forces in the cables can be found from Eq. (6.18).

Unfortunately, in this case it is not always possible to avoid the solution of simultaneous, nonlinear equations (a very difﬁcult task to perform analytically). Therefore, a computer program capable of solving simultaneous, nonlinear equations may be necessary for solving problems in this category.

|Sample Problem 6.10<br><br>For the cable loaded as shown in Fig. (a), determine the angles β1 and β2, the force in each segment, and the length of the cable.<br><br>(a)<br><br>6 ft<br><br>2000 lb<br><br>1600 lb<br><br>6 ft 11 ft 7 ft<br><br>A<br><br>β1<br><br>β2<br><br>β3<br><br>B<br><br>= 35°<br><br>1<br><br>2<br><br>FBD<br><br>= 35°<br><br>– 1<br><br>3<br><br>s1<br><br>s3<br><br>A β θ<br><br>θ<br><br>θ<br><br>β<br><br>β<br><br>B<br><br>T3<br><br>T1<br><br>(b)<br><br>– 2<br><br>s2 3 =<br><br>=–6fth<br><br>2 =<br><br>1=<br><br>L1= 6 ft L2 =11 ft L3 = 7 ft<br><br>L = 24 ft<br><br>1<br><br>2<br><br>W2 = 2000 lb<br><br>W1 = 1600 lb<br><br>Solution<br><br>Method of Analysis<br><br>The free-body diagram of the entire cable is shown in Fig. (b), where the labeling of the variables is consistent with the notation used in Fig. 6.12 (recall that the positive direction for θ1, θ2, and θ3 is counterclockwise from the horizontal, and positive h is measured downward from end B).<br><br>We note that the information given in Fig. (a) includes the horizontal spacing of the loads and the angle β3. Therefore, according to the discussion in Art. 6.6, the problem is statically determinate, and a solution can be obtained by writing and solving Eqs. (6.18)–(6.20). In this problem, however, the difﬁculty of solving these simultaneous, nonlinear equations can be avoided.<br><br>Examination of the FBD in Fig. (b) reveals that T3 can be calculated from the equation MA = 0. Equilibrium equations for joints 2 and 1 will then determine the other unknowns without having to solve the equations simultaneously.<br><br>Mathematical Details<br><br>From the FBD of the entire cable, Fig. (b), we obtain<br><br>MA = 0 + T3 sin35◦(24) + T3 cos35◦(6) − 1600(6) − 2000(17) = 0 which gives<br><br>T3 = 2334 lb Answer<br><br>The constant horizontal component T0 of the cable tension can now be found by computing the horizontal component of T3.<br><br>T0 = T3 cosθ3 = 2334cos 35◦ = 1912 lb|
|---|

###### –6ft

|Substituting i = 2 into Eqs. (6.19), we obtain the equilibrium equation for joint 2:<br><br>T0(tanθ3 − tanθ2) = W2<br><br>1912(tan35◦ − tanθ2) = 2000<br><br>which gives<br><br>θ2 = −19.08◦ or β2 = 19.08◦ Answer<br><br>With i = 1, Eqs. (6.19) give the equilibrium equation for joint 1:<br><br>T0(tanθ2 − tanθ1) = W1<br><br>1912[tan(−19.08◦) − tanθ1] = 1600<br><br>which gives<br><br>θ1 = −49.78◦ or β1 = 49.78◦ Answer<br><br>The tensions in the ﬁrst and second segments can now be found from Eqs. (6.18):<br><br>T1 =<br><br>T0<br><br>cosθ1 =<br><br>1912 cos(−49.78◦) = 2961 lb Answer<br><br>T2 =<br><br><br>T0<br><br>cosθ2 =<br><br>1912 cos(−19.08◦) = 2023 lb Answer<br><br>The total length s of the cable is<br><br>s = s1 + s2 + s3<br><br>=<br><br>L1<br><br>cosβ1 +<br><br>L2<br><br>cosβ2 +<br><br>L3 cosβ3<br><br>=<br><br>6 cos49.78◦ +<br><br>11 cos19.08◦ +<br><br>7 cos35◦<br><br>= 9.29 + 11.64 + 8.55 = 29.48 ft Answer|
|---|

|Sample Problem 6.11<br><br>For the cable loaded as shown in Fig. (a), calculate the angles β1, β2, and β3 and the force in each segment of the cable.<br><br>6 ft<br><br>2000 lb<br><br>1600 lb<br><br>24 ft<br><br>8ft<br><br>12ft<br><br>10ft<br><br>(a)<br><br>A β<br><br>β<br><br>β<br><br>1 B<br><br>2<br><br>2<br><br>1<br><br>3<br><br>Solution<br><br>Method of Analysis<br><br>The free-body diagram of the entire cable is shown in Fig. (b). Its main function is to identify the variables and to enforce the sign conventions deﬁned in Fig. 6.12 (recall that the positive directions for the θ’s are counterclockwise and that positive h is measured downward from end B).<br><br>s3<br><br>=10ft<br><br>3 = 2<br><br>3<br><br>T3<br><br>(b)<br><br>1<br><br>2 = – 2<br><br>B<br><br>A β θ<br><br>θ<br><br>θ<br><br>β<br><br>β<br><br>T1<br><br>–=6fth<br><br>L = 24 ft<br><br>1= – 1<br><br>s<br><br>1<br><br>=<br><br>8ft<br><br>s<br><br>2<br><br>=<br><br>12ft<br><br>W2 = 2000 lb<br><br>W1 = 1600 lb<br><br>Observe that the length of each cable segment is given. As pointed out in Art. 6.6, in problems of this type (and this problem is no exception) it is seldom possible to obtain a solution without having to solve nonlinear, simultaneous equations. An inspection of Fig. (b) reveals that two or more unknown angles would appear in each equilibrium equation for the entire cable (this would also be the situation if the equilibrium of any portion of the cable is analyzed). Therefore, the most direct method of solution is to write and solve Eqs. (6.19) and (6.21), giving us a total of four equations containing the unknowns T0, θ1, θ2, and θ3. Because the equations are nonlinear, the solution must be obtained numerically by a computer program capable of solving nonlinear, simultaneous equations. After|
|---|

|the solution has been found, the force in each segment can be calculated from Eqs. (6.18).<br><br>Mathematical Details<br><br>On substituting the given values, Eqs. (6.19) yield<br><br>(i = 1) T0(tanθ2 − tanθ1) = W1<br><br>T0(tanθ2 − tanθ1) = 1600 (a) and<br><br>(i = 2) T0(tanθ3 − tanθ2) = W2<br><br>T0(tanθ3 − tanθ2) = 2000 (b) and Eqs. (6.21) become<br><br>s1 sinθ1 + s2 sinθ2 + s3 sinθ3 = h<br><br>8sinθ1 + 12sinθ2 + 10sinθ3 = −6 (c) and<br><br>s1 cosθ1 + s2 cosθ2 + s3 cosθ3 = L<br><br>8cosθ1 + 12cosθ2 + 10cosθ3 = 24 (d) The solution of Eqs. (a)–(d), which can be veriﬁed by substitution, is<br><br>T0 = 1789 lb<br><br>θ1 = −53.62◦(= −β1) Answer<br>θ2 = −24.83◦(= −β2)<br>θ3 = 33.23◦(= β3)<br><br><br>Using Eqs. (6.18), the tensions in the cable segments are<br><br>T1 =<br><br>T0<br><br>cosθ1 =<br><br>1789 cos(−53.62◦) = 3020 lb<br><br>T2 =<br><br>T0<br><br>cosθ2 =<br><br>1789 cos(−24.83◦) = 1971 lb Answer<br><br>T3 =<br><br><br>T0<br><br>cosθ3 =<br><br>1789 cos33.23◦ = 2140 lb<br><br>|
|---|

![image 47](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile47.png>)

###### Problems

- 6.80 The cable carrying 40-lb loads at B and C is held in the position shown

h

D

P A B

C 6ft

6ft

40 lb

40 lb

Fig. P6.80

by the horizontal force P = 60 lb applied at A. Determine h and the forces in segments BC and CD.

- 6.81 The cable ABCD is held in the position shown by the horizontal force P. Determine P, h, and the forces in segments BC and CD of the cable.

h

D

P

A B

C

40 lb

40 lb

6 ft

6 ft

4 ft

D

10 ft

1.2 kips

1.8 kips

B

C

6 ft 8 ft 12 ft A

β1

β2

β3

Fig. P6.81 Fig. P6.82

- 6.82 Determine the angles β2 and β3 and the force in each cable segment if β1 = 40◦.
- 6.83 The cable carrying three 400-lb loads has a sag at C of hC =16 ft. Calculate the force in each segment of the cable.

8 ft 8 ft 12 ft 12 ft

hC

B

C

D 400 lb

400 lb

400 lb

A E

Fig. P6.83, P6.84

- 6.84 The cable supports three 400-lb loads as shown. If the maximum allowable tension in the cable is 900lb, ﬁnd the smallest possible sag hC at C.
- 6.85 Cable ABC of length 5m supports the force W at B. Determine (a) the

4 m

A C

β2

β1

2m

3m

B

W

###### Fig. P6.85

angles β1 and β2; and (b) the force in each cable segment in terms of W.

###### 6.86 When the 12-kN load and the unknown force P are applied, the cable assumes the conﬁguration shown. Determine P and the force in each segment of the cable.

2 m 4 m 4 m

D

A

4 m

C P

B

12 kN

Fig. P6.86

###### 6.87 The cable is subjected to a 150-lb horizontal force at B, and an 80-lb vertical force at C. Determine the force in segment CD of the cable, and the distance b.

A

4 ft 3ft3ft3ft

150 lb

b

B

D

C

80 lb

Fig. P6.87

###### 6.88 The 15-m-long cable supports the loads W1 and W2 as shown. Find the ratio W1/W2 for which the segment BC will be horizontal; that is, β2 = 0.

12 m

A β1 β3 D

4m

6m

β2

C

5m

B

W2

W1

Fig. P6.88, P6.89

###### 6.89 The cable of length 15m supports the forces W1 = W2 = W at B and C. (a) Derive the simultaneous equations for β1, β2, and β3. (b) Show that the solution to these equations is β1 = 41.0◦, β2 = 9.8◦, and β3 = 50.5◦. (c) Compute the force in each segment in terms of W.

###### 6.90 The 12-kN weight is suspended from a small pulley that is free to roll on the cable. The length of the cable ABC is 18m. Determine the horizontal force P that would hold the pulley in equilibrium in the position x = 4 m.

16 m

C

2 m

A

B

P x

12 kN

Fig. P6.90

###### 6.91 The cable ABCD is held in the position shown by the horizontal force P. Determine P and the force in each segment of the cable.

1.0m

2m 3m

D

A

3m

4m

P

B

15kg

C

25kg

###### Fig. P6.91

![image 48](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile48.png>)

###### Review of Equations

###### Beams

A beam is a slender bar carrying loads that are perpendicular to the bar.

###### Sign conventions for loading, shear force, and bending moment

y

|+w|
|---|

|+V|
|---|

|+M|
|---|

x

###### Differential equations of equilibrium

w = −dV/dx V = dM/dx

###### Area method

VB = VA − area of w-diagram]BA MB = MA + area of V-diagram]BA VA+ = VA− − PA MA+ = MA− + CA

###### Parabolic cable

If the loading w0 is distributed uniformly along the horizontal, the shape of the cable is parabolic:

w0x2 2T0

y(x) =

ln

2

2

w0x T0 + 1 +

w0x T0

w0x T0

x 2

T0 2w0

s(x) =

1 +

+

T0 = tension in the cable at x = 0 s(x) = length measured along the cable from x = 0

###### Catenary cable

If the loading w0 is distributed uniformly along the cable, the shape of the cable is a catenary:

w0x

T0 w0

y(x) =

T0 − 1 s(x) =

cosh

T w0

w0x T0

sinh

# 7

### Dry Friction

![image 49](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile49.png>)

The force required to turn the handle of a screw press, such as the antique wine press shown here, depends on the coefﬁcient of friction between the screw threads. This effect is illustrated Sample Problem 7.12. Andrey Kudinov/Shutterstock

###### 7.1 Introduction

In most of the equilibrium problems that we have analyzed up to this point, the surfaces of contact have been frictionless. The reactive forces were, therefore, normal to the contact surfaces. The concept of a frictionless surface is, of course, an idealization. All real surfaces also provide a force component that is tangent to the surface, called the friction force, that resists sliding.

In many situations, friction forces are helpful. For example, friction enables you to walk without slipping, it holds nails and screws in place, and it allows us

###### 341

to transmit power by means of clutches and belts. On the other hand, friction can also be detrimental: It causes wear in machinery and reduces efﬁciency in the transmission of power by converting mechanical energy into heat.

Dry friction refers to the friction force that exists between two unlubricated solid surfaces. Fluid friction acts between moving surfaces that are separated by a layer of ﬂuid. The friction in a lubricated journal bearing is classiﬁed as ﬂuid friction, because the two halves of the bearing are not in direct contact but are separated by a thin layer of liquid lubricant. In this chapter, we consider only dry friction.* A study of ﬂuid friction involves hydrodynamics, which is beyond the scope of this text.

###### 7.2 Coulomb’s Theory of Dry Friction

P3

Dry friction is a complex phenomenon that is not yet completely understood. This article introduces a highly simpliﬁed theory, known as Coulomb’s theory of dry friction, that has been found to give satisfactory results in many practical problems.

P2

Coulomb’s theory is best explained by considering two bodies that are in contact with each other, as shown in Fig. 7.1 (a). Although a single point of contact

P1

Plane of contact

is indicated in this ﬁgure, the following discussion also applies for a ﬁnite contact area. The plane of contact shown in Fig. 7.1(a) is tangent to both bodies at the point of contact. Figure 7.1(b) displays the free-body diagrams of the bodies, where N is the normal contact force and F is the friction force. The force N is perpendicular to the plane of contact, whereas F lies in the plane of contact. Coulomb’s theory consists of several postulates that are explained in the following.

P4

P5

(a)

###### a. Static case

P3

Coulomb proposed the following law: If there is no relative motion between two surfaces that are in contact, the normal force N and the friction force F satisfy the following relationship.

P2

P1

F

F ≤ Fmax = µsN (7.1)

where Fmax is the maximum static friction force that can exist between the contacting surfaces and µs is known as the coefﬁcient of static friction. The coefﬁcient of static friction is an experimental constant that depends on the composition and roughness of the contacting surfaces. Typical values of µs are listed in Table 7.1. Observe that Eq. (7.1) states simply that the friction force F that exists under static conditions (no relative motion) has an upper limit that is proportional to the normal force.

N N

F

P4

P5

(b)

*Dry friction is also known as Coulomb friction, after C.-A. de Coulomb (1736–1806), the ﬁrst investigator to completely state the laws of dry friction.

Fig. 7.1

7.2 Coulomb’s Theory of Dry Friction 343

![image 50](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile50.png>)

Text not available due to copyright restrictions

###### b. Impending sliding

Consider the static case in which the friction force equals its limiting value; that is,

F = Fmax = µsN (7.2)

For this condition, the surfaces are on the verge of sliding, a condition known as impending sliding. When sliding impends, the surfaces are at rest relative to each other. However, any change that would require an increase in the friction force would cause sliding. The direction for Fmax can be determined from the observation that

Fmax always opposes impending sliding

###### c. Dynamic case

If the two contact surfaces are sliding relative to each other, the friction force F is postulated to be

F = Fk = µkN (7.3)

P

where N is the contact normal force; µk is an experimental constant called the coefﬁcient of kinetic friction; and Fk is referred to as the kinetic, or dynamic friction force. As indicated in Table 7.1, the coefﬁcient of kinetic friction is usually smaller than its static counterpart. As in the static case,

(a)

W

Fk always opposes sliding

P

###### d. Further discussion of Coulomb friction

When applying Coulomb’s theory, the difference between Fmax and Fk must be clearly understood: Fmax is the maximum friction force that can exist under static conditions; Fk is the friction force that does exist during sliding.

F

N

To illustrate Coulomb’s laws of friction, consider the situation depicted in Fig. 7.2 (a). The block of weight W is assumed to be at rest on a horizontal surface

(b)

when it is subjected to the horizontal force P. (We limit our attention here to sliding motion; the possibility that the block may tip about its corner is considered

Fig. 7.2

later.) The free-body diagram of the block is shown in Fig. 7.2(b). Because the friction force F resists the tendency of the block to slide, F is directed opposite to P. We now examine the variation of F with P as the latter increases slowly from zero.

If P is relatively small, the block will remain at rest, and the force equations of equilibrium, Fx =0 and Fy =0, yield F = P and N = W.* Therefore, as long as the block remains at rest, the friction force F equals the applied force P. Figure 7.3 shows the plot of F versus P. In the static region, 0≤ F ≤ Fmax; the variation is a straight line with unit slope. When F = Fmax, the block is still in static equilibrium, but sliding impends. However, the slightest increase in P would result in sliding. In Fig. 7.3, the point referring to impending sliding marks the end of the static region. When P exceeds Fmax, the block starts to slide, and the friction force F drops to its kinetic value Fk. If P is further increased, F remains constant at Fk. Consequently, the plot of F versus P is a horizontal line in the dynamic range.

F (friction force)

Static

Dynamic

Impending sliding

Fmax = µsN

1 Fk = k N

µ

1

P (applied force)

###### Fig. 7.3

###### e. Limitations

Because there is no theoretical explanation that accurately describes friction phenomena, engineers must rely on empirical constants, such as the coefﬁcient of friction. Handbook values for the coefﬁcients of friction should be treated as approximate values. Experimental results indicate that the coefﬁcients may vary widely with environmental conditions, such as humidity, the cleanliness of the surfaces, and so on.

The theory of dry friction is applicable only to surfaces that are dry or that contain only a small amount of lubricant. If there is relative motion between the surfaces of contact, the theory is valid for low speeds only. If the surfaces are well lubricated and are moving with high relative speeds, the frictional characteristics are best described by the theories of ﬂuid friction, which are beyond the scope of this text.

*The moment equation of equilibrium would determine the line of action of the normal force N, an important consideration in the analysis of tipping. However, because we are delaying a discussion of tipping, this equation is not of interest at the present time.

###### 7.3 Problem Classiﬁcation and Analysis 345

It is interesting to note that Coulomb’s theory of dry friction does not depend on the area of contact. There are, of course, many situations where this is not the case. For example, the traction (friction force) between an automobile tire and the pavement can be increased under certain conditions by letting a small amount of air out of the tire, thus increasing the contact area. Obviously, Coulomb’s theory of dry friction is not applicable in this situation. The maximum traction in this case is also inﬂuenced by factors, such as surface adhesion, that depend on the area of contact.

###### 7.3 Problem Classiﬁcation and Analysis

The analysis of equilibrium problems that involve friction can be somewhat complicated because Coulomb’s law, Eq. (7.1), is an inequality. It does not tell us the friction force; it tells us only the largest possible friction force. The equality F = Fmax = µsN can be used only if slipping is known to impend. Because F is not necessarily equal to Fmax at a friction surface, it is not possible to develop a single method of analysis that is valid for all friction problems. However, friction problems can be classiﬁed into three types, and a separate method of solution can be outlined for each type.

Type I The problem statement does not specify impending motion. In problems of this type, we do not know whether or not the body is in equilibrium. Therefore, the analysis must begin with an assumption about equilibrium.

###### Method of Analysis

- 1. Assume equilibrium You are strongly advised to write down this assumption as a reminder that the solution will not be complete unless the assumption has been checked. The sense of each friction force can be assumed because the solution of the equilibrium equations will determine the correct sense.
- 2. Solve the equilibrium equations for the friction forces required for equilibrium.*
- 3. Check the assumption If the friction forces required for equilibrium do

not exceed their limits (i.e., if F ≤µsN at each friction surface), then the assumption is correct, and the remaining unknowns can be computed using equilibrium analysis. (Note that if F =µsN at a surface, which would imply impending sliding, then the assumption is still correct.) If equilibrium requires that F >µsN at any friction surface (which is physically impossible), the assumption of equilibrium is incorrect. Therefore, we have a dynamics problem in which the friction forces at the sliding surfaces are F = Fk =µkN.

See Sample Problems 7.1 and 7.4 for examples of Type I problems.

*This analysis presupposes that the friction forces are statically determinate. Statically indeterminate friction forces are omitted from the present discussion. Problems of this type are best solved using the principle of virtual work (see Chapter 10).

- Type II The problem statement implies impending sliding, and the surfaces where sliding impends are known. Friction problems of this type have the most straightforward analyses, because no assumptions and, therefore, no checks are required. It is not necessary to assume equilibrium—a body known to be in a state of impending sliding is in equilibrium by deﬁnition.

Method of Analysis

- 1. Set F = Fmax = µsN at the surfaces where sliding impends. Make sure that the sense of each Fmax is correctly shown on the FBD (opposing impending sliding), because the solution of the equilibrium equations may depend on the assumed directions of the friction forces.
- 2. Solve for the unknowns using the equilibrium equations.

See Sample Problems 7.2, 7.5, and 7.6 for examples of Type II problems.

- Type III The problem statement implies impending sliding, but the surfaces at which sliding impends are not known. Problems of this type are the most tedious to analyze, because the surfaces at which sliding impends must be identiﬁed by trial and error. Once an assumption has been made, the analysis is similar to that for Type II problems. Two methods of analysis can be used here, both of which are described in the following.

###### Method of Analysis 1

- 1. Determine all possible ways in which sliding can impend.
- 2. For each case, set F = Fmax at the surfaces where sliding impends and solve the equilibrium equations. Again, the sense of each Fmax should be correct on the FBD. In general, a different solution is obtained for each mode of impending sliding.
- 3. Choose the correct answer by inspection of the solutions.

###### Method of Analysis 2

- 1. Determine all possible ways in which sliding can impend.
- 2. For one of the cases, set F = Fmax at the surfaces where sliding impends and solve the equilibrium equations.
- 3. Check the solution by comparing the friction force at each of the other surfaces with its limiting value. If all these forces are less than or equal to their maximum permissible values, then the solution is correct. If a friction force

exceeds its limiting value µsN, the solution is invalid and another mode of impending sliding must be analyzed. This procedure must be continued until the correct solution is found.

See Sample Problems 7.3 and 7.7 for examples of Type III problems.

Caution Remember that the equation F = µsN is valid only in the special case of impending sliding. Many difﬁculties encountered by students can be traced to the incorrect assumption that the equation F = µsN is always true.

|Sample Problem 7.1<br><br>The 100-lb block in Fig. (a) is initially at rest on a horizontal plane. Determine the<br><br>W = 100 lb<br><br>P<br><br>s = 0.5 k = 0.2<br><br>(a)<br><br>100 lb<br><br>P = 30 lb<br><br>(b)<br><br><br>N<br><br>F<br><br>y<br><br>x<br><br>µ µ<br><br>friction force between the block and the surface after P was gradually increased from 0 to 30lb.<br><br>Solution<br><br>From the problem statement we conclude that this is a Type I problem (impending motion is not speciﬁed). Furthermore, we do not know if the block will even remain at rest in static equilibrium when P = 30 lb.<br><br>Assume Equilibrium<br><br>Once we have assumed that the body remains at rest, the equilibrium equations for the free-body diagram in Fig. (b) can be used to calculate the two unknowns (N and F), as follows.<br><br>Fy = 0 +  N − 100 = 0<br><br>N = 100 lb Fx = 0 −→+ P − F = 0<br><br>F = P = 30 lb<br><br>Before we can accept this solution, the assumption of equilibrium must be checked.<br><br>Check<br><br>The maximum static friction force is<br><br>Fmax = µsN = 0.5(100) = 50 lb<br><br>Because F < Fmax, we conclude that the block is in static equilibrium, and the correct value of the friction force is<br><br>F = 30 lb Answer<br><br>Comment<br><br>If the coefﬁcient of static friction had been 0.25, instead of 0.5, the block would not be in equilibrium. The 30-lb friction force required for equilibrium would be greater than Fmax = 0.25(100) = 25 lb; therefore, the friction force would be<br><br>F = Fk = µkN = 0.2(100) = 20 lb<br><br>and the block would be sliding to the right.|
|---|

|Sample Problem 7.2<br><br>The 100-lb block in Fig. (a) is at rest on a rough horizontal plane before the force P<br><br>W = 100 lb<br><br>P<br><br>s = 0.5 k = 0.2<br><br>(a)<br><br>µ µ<br><br>is applied. Determine the magnitude of P that would cause impending sliding to the right.<br><br>Solution<br><br>The problem statement clearly speciﬁes that sliding impends. Because we know where it impends (there is only one friction surface), we conclude that this is a Type II problem.<br><br>The free-body diagram of the block is shown in Fig. (b), where the friction<br><br>100 lb<br><br>P<br><br>(b)<br><br>N<br><br>F<br><br>force is shown acting to the left, opposite the direction of impending sliding. There are three unknowns in this FBD: P, N, and F. There are also three independent equations: two equilibrium equations and Coulomb’s law for impending sliding.<br><br>From the FBD we see that the equilibrium equations give N = 100 lb and P = F. Coulomb’s law then yields<br><br>P = F = Fmax = µsN = 0.5(100) = 50 lb Answer<br><br>This completes the solution. Because there were no assumptions, no checks are necessary.<br><br>Comment<br><br>Note that Fig. (a) in both Sample Problems 7.1 and 7.2 is identical. The differences are revealed only in the problem statements. This shows that you must read each problem statement very carefully, because it determines the problem type.<br><br>A problem statement can imply impending sliding. For example, the following are equivalent to the original statement of this problem: They both imply that P is to be calculated for impending sliding.<br><br>1. Determine the largest force P that can be applied without causing the block to slide to the right.<br>2. Determine the smallest force P that will cause the block to slide to the right.<br><br><br>Sample Problem 7.3<br><br>Determine the maximum force P that can be applied to block A in Fig. (a) without<br><br>A<br><br>WA = 100 lb<br>WB = 200 lb<br><br><br>B<br><br>Surface 1 P<br><br>s = 0.2<br><br>Surface 2<br><br>s = 0.1 (a)<br><br>y<br><br>x<br><br>µ<br><br>µ<br><br>causing either block to move.<br><br>Solution<br><br>The problem statement indicates that we are to ﬁnd P that would cause impending motion. However, there are two possible ways in which motion can impend: impending sliding at surface 1, or impending sliding at surface 2. Because impending sliding is speciﬁed but not its location, this is a Type III problem.<br><br>The free-body diagrams of the entire system and each block are shown in Figs. (b) and (c), respectively. Note that the equilibrium of each block yields|
|---|

|A<br><br>WA = 100 lb<br>WB = 200 lb<br><br><br>B<br><br>P<br><br>(b)<br><br>N2 = 300 lb<br><br>F2<br><br>A<br><br>WA = 100 lb<br><br>B WB = 200 lb<br><br>P<br><br>(c)<br><br>N2 = 300 lb<br><br>F2<br><br>N1 = 100 lb<br><br>F1<br><br>N1 = 100 lb<br><br>F1<br><br>1<br><br>1<br><br>2<br><br><br>N1 = 100 lb and N2 = 300 lb, as shown on the FBDs. Attention should be paid to the friction forces. The friction force F2 on the bottom of block B is directed to the left, opposite the direction in which sliding would impend. At surface 1, block A would tend to slide to the right, across the top of block B. Therefore, F1 is directed to the left on block A, and to the right on block B. The tendency of F1 to slide B to the right is resisted by the friction force F2. Note that F1 and N1 do not appear in the FBD in Fig. (b), because they are internal to the system of both blocks.<br><br>Two solutions are presented here to illustrate both methods of analysis described in Art. 7.3.<br><br>Method of Analysis 1<br><br>First, assume impending sliding at surface 1. Under this assumption we have<br><br>F1 = (F1)max = (µs)1N1 = 0.2(100) = 20 lb<br><br>The FBD of block A then gives<br><br>Fx = 0 −→+ P − F1 = 0 P = F1 = 20 lb<br><br>Next, assume impending sliding at surface 2, which gives<br><br>F2 = (F2)max = (µs)2N2 = 0.1(300) = 30 lb<br><br>From the FBD of the entire system, Fig. (b), we then obtain<br><br>Fx = 0 −→+ P − F2 = 0 P = F2 = 30 lb|
|---|

|So far, we have determined that P =20 lb will cause motion to impend at surface 1 and that P =30 lb will cause motion to impend at surface 2. Therefore, the largest force that can be applied without causing either block to move is<br><br>P = 20 lb Answer<br><br>with sliding impending at surface 1.<br><br>Be sure you understand that the largest force that can be applied is the smaller of the two values determined in the preceding calculations. If sliding impends when P =20 lb, then the system would not be at rest when P =30 lb.<br><br>Method of Analysis 2<br><br>Assume impending motion at surface 1. We would then obtain P = (F1)max = 20 lb, as determined in Method of Analysis 1. Next, we check the assumption.<br><br>Check<br><br>The assumption of impending motion at surface 1 is checked by comparing the friction force F2 with (F2)max, its maximum possible value. Using the FBD of block B, we obtain<br><br>Fx = 0 −→+ F1 − F2 = 0 F1 = F2 = 20 lb<br><br>Because (F2)max =(µs)2N2 =0.1(300)=30 lb, we have F2 <(F2)max. Consequently, we conclude that impending motion at surface 1 is the correct assumption, so that the answer is P =20lb.<br><br>Had F2 turned out to be greater than (F2)max, we would know that sliding would ﬁrst impend at surface 2, and the problem would have to be solved again making use of this fact.<br><br>Comment<br><br>There are ﬁve unknowns in this problem: P, N1, F1, N2, and F2. There are four independent equilibrium equations: two for each block. The assumption of impending motion at one surface provides the ﬁfth equation, F = µsN, making the problem statically determinate.<br><br>In our solution, we have considered two possible modes of impending motion—impending sliding at surface 1 and impending sliding at surface 2. Impending sliding at both surfaces at the same time is obviously a third possibility, but it need not be examined independently. Both of the foregoing analyses would determine if simultaneous impending sliding is indeed the case. In Method of Analysis 1 the two computed values of P would be equal. In Method of Analysis 2 the check would reveal that F = Fmax at both surfaces.<br><br>Caution A mistake that is often made in the analysis of Type III problems is to assume that motion impends at the surface with the smallest coefﬁcient of static friction. The solution to this problem illustrates that this need not be the case.|
|---|

|Sample Problem 7.4<br><br>Can the system in Fig. (a) be in static equilibrium in the position shown? The<br><br>50°<br><br>A<br><br>B<br>C<br><br><br>30°<br><br>10ft<br><br>(a)<br><br>y<br><br>x<br><br>30° 500 lb<br><br>40°<br><br>A<br><br>B<br><br>FB NB<br><br>NA<br><br>5ft<br><br>5ft<br><br>(b)<br><br>FC<br><br>C<br><br>NC (c)<br><br>300<br><br>|lb| |
|---|---|
| | |
<br><br>FB<br><br>NB<br><br>uniform bar AB weighs 500lb, and the weight of block C is 300lb. Friction at A is negligible, and the coefﬁcient of static friction is 0.4 at the other two contact surfaces.<br><br>Solution<br><br>Because it is not known whether motion impends, we identify this as a Type I problem. Note that the FBDs of the bar and the block, Figs. (b) and (c), contain ﬁve unknowns: NA, NB, FB, NC, and FC.<br><br>Assume Equilibrium<br><br>Under this assumption, there are ﬁve equilibrium equations: three for the bar AB and two for the block C. The unknowns may be computed by the following procedure.<br><br>FBD of AB [Fig. (b)]<br><br>MB = 0 + NA sin40◦(10cos30◦) + NA cos40◦(10sin30◦)<br><br>−500(5cos 30◦) = 0 NA = 230.4 lb<br><br>Fx = 0 −→+ FB − NA cos40◦ = 0 FB = 230.4cos 40◦ = 176.50 lb<br>Fy = 0 +  NB + NA sin40◦ − 500 = 0 NB = −230.4sin40◦ + 500 = 351.9 lb<br><br><br>FBD of Block C [Fig. (c)]<br><br>Fy = 0 +  NC − NB − 300 = 0<br><br>NC = 351.9 + 300 = 651.9 lb Fx = 0 −→+ FC − FB = 0<br><br>FC = FB = 176.50 lb<br><br>Check<br><br>To check the assumption of equilibrium, we must compare each of the friction forces against its maximum static value.<br><br>(FB)max = 0.4NB = 0.4(351.9) = 140.76 lb< FB = 176.50 lb Answer<br>(FC)max = 0.4NC = 0.4(651.9) = 260.8 lb > FC = 176.50 lb<br><br><br>We conclude that the system cannot be in equilibrium. Although there is sufﬁcient friction beneath B, the friction force under C exceeds its limiting value.|
|---|

|Sample Problem 7.5<br><br>Determine the largest and smallest values of the force P for which the system in Fig. (a) will be in static equilibrium. The homogeneous bars AB and BC are identical, each having a mass of 100 kg. The coefﬁcient of static friction between the bar at C and the horizontal plane is 0.5.<br><br>s = 0.5<br><br>3m<br><br>30° 30°<br><br>1.5m<br><br>1.5m<br><br>(a)<br><br>A<br><br>B<br><br>C<br><br>P<br><br>y<br><br>x<br><br>µ<br><br>Solution<br><br>This is a Type II problem because impending sliding at C is implied. However, ﬁnding the largest and smallest values of P are two separate problems.<br><br>Note that the weights of the bars have a tendency to slide C to the right. Therefore, impending sliding of C to the right corresponds to the smallest P. The largest P occurs when sliding of C impends to the left; in this case, P must overcome both the friction and the tendency of the weights to slide C to the right. Consequently, the only difference between the two problems is the direction of the friction force at C.<br><br>The FBD of the system consisting of both bars is shown in Fig. (b); the two directions of FC are indicated by dashed lines. The weight of each bar, W =mg =100(9.81)=981 N, is also shown on the diagram.<br><br>30°<br><br>1.5m<br><br>1.5m<br><br>(b)<br><br>A<br><br>B<br><br>C<br><br>P<br><br>1.5m<br><br>1.5m<br><br>Ax<br><br>Ay<br><br>981 N 981 N FC FC<br><br>NC<br><br>An equation involving only NC and P is obtained by summing moments about A in Fig. (b):<br><br>MA = 0 + NC(6cos30◦) + P(1.5sin30◦)<br><br>− 981(1.5cos 30◦) − 981(4.5cos 30◦) = 0 (a)<br><br>The FBDs of bar BC corresponding to the largest and smallest values of P are shown in Figs. (c) and (d), respectively. In both cases, FC is set equal to (FC)max|
|---|

|1.5m<br><br>1.5m<br><br>C<br><br>P<br><br>981 N<br><br>NC<br><br>B<br><br>30°<br><br>By<br><br>Bx<br><br>(c) Largest P<br><br>FC = 0.5NC<br><br>1.5m<br><br>1.5m<br><br>C<br><br>P<br><br>981 N FC = 0.5NC<br><br>NC<br><br>B<br><br>(d) Smallest P<br><br>By<br><br>Bx<br><br>30°<br><br>because sliding impends. Summing moments about B yields another equation containing NC and P.<br><br>MB = 0 + NC(3cos30◦) − 981(1.5cos 30◦)<br><br>− P(1.5sin30◦) ± 0.5NC(3sin30◦) = 0 (b)<br><br>where the positive (negative) sign on the last term corresponds to the largest (smallest) value of P.<br><br>Solving Eqs. (a) and (b) gives<br><br>largest P = 1630 N Answer smallest P = 530 N Answer<br><br>Therefore, the system is in static equilibrium for values of P in the range 530 N ≤ P ≤ 1630 N.<br><br>The solution of this sample problem clearly illustrates that the directions of the friction forces must be shown correctly on the free-body diagrams when sliding impends.<br><br>Sample Problem 7.6<br><br>The uniform 100-lb plank in Fig. (a) is resting on friction surfaces at A and B. The coefﬁcients of static friction are shown in the ﬁgure. If a 200-lb man starts walking from A toward B, determine the distance x when the plank will start to slide.<br><br>40°<br><br>x<br><br>A 10 ft<br><br>B<br><br>(a)<br><br>µs = 0.2<br><br>µs = 0.5|
|---|

|Solution<br><br>This is a Type II problem. When the plank is on the verge of moving, sliding must impend at both A and B. Impending sliding at A only, or at B only, would be physically impossible. Because the plank is a rigid body, any movement of end A must be accompanied by a movement of end B.<br><br>The FBD of the plank is shown in Fig. (b). Observe that the friction forces<br><br>x<br><br>40°<br><br>50°<br><br>5 ft 5 ft<br><br>200 lb<br><br>100 lb<br><br>(b)<br><br>A B<br><br>NA<br><br>FA<br><br>NB<br><br>FB<br><br>y<br><br>x<br><br>are shown acting in their correct directions. When the plank is ready to move, the direction of impending sliding of end B is down the inclined plane. Consequently, end A would tend to slide to the left. The directions of FA and FB must oppose these motions. Showing either of the friction forces in the opposite direction would lead to incorrect results.<br><br>Inspection of the FBD in Fig. (b) reveals that there are ﬁve unknowns: NA, FA, NB, FB, and x. There are also ﬁve equations: three equilibrium equations and two friction equations. Therefore, all the unknowns can be computed from the FBD as follows.<br><br>MA = 0 + NB sin50◦(10) + FB sin40◦(10)<br><br>−200x − 100(5) = 0 (a)<br><br>Fx = 0 −→+ FA − NB cos50◦ + FB cos40◦ = 0 (b)<br>Fy = 0 +  NA − 200 − 100 + NB sin50◦ + FB sin40◦ = 0 (c)<br><br><br>Substituting the friction equations, FA = 0.2NA and FB = 0.5NB, and solving Eqs. (a)–(c) give NA = 163.3 lb, NB = 125.7 lb, and<br><br>x = 4.34 ft Answer<br><br>Sample Problem 7.7<br><br>The spool in Fig. (a) weighs 25 N, and its center of gravity is located at the geometric center. The weight of block C is 50 N. The coefﬁcients of static friction at the two points of contact are as shown. Determine the largest horizontal force P that can be applied without disturbing the equilibrium of the system.<br><br>|C|
|---|
<br><br>A<br>B<br><br><br>120<br><br>80<br><br>(a)<br><br>P<br><br>Dimensions in mm<br><br>µs = 0.3<br><br>µs = 0.4<br><br><br>µ<br><br>µ|
|---|

|Solution<br><br>The key to the analysis of this problem is understanding that there are two possibilities for impending motion (both could occur simultaneously): (1) impending<br><br>sliding at A with impending rolling (without sliding) at B, and (2) impending<br>sliding at B with impending rolling (without sliding) at A. Because it is initially not known which of these possibilities represents the actual mode of impending motion, this is a Type III problem.<br><br><br>The free-body diagrams for the block and the spool are shown in Fig. (b).<br><br>C<br><br>A<br>B<br><br><br>120<br><br>80<br><br>(b)<br><br>25 N<br><br>50 N<br><br>NC<br><br>FA NA<br><br>NA<br><br>FA<br>FB<br><br><br>NB<br><br><br>P<br><br>y<br><br>x<br><br>Observe that both friction forces have been shown in their correct directions. The force P tends to slide points A and B on the spool to the right. Therefore, both friction forces are shown acting to the left on the FBD of the spool.<br><br>Inspecting the FBDs in Fig. (b), we conclude from Fy = 0 that NA = 50 N and NB = 75 N. At this stage three unknowns remain in the FBD of the spool: FA, FB, and P. Because only two equilibrium equations are left ( Fy = 0 has already been used), the remainder of the solution depends on the assumption regarding impending motion.<br><br>Assume Impending Sliding at A<br><br>This assumption gives us the additional equation FA = 0.3NA = 0.3(50) = 15 N. The FBD of the spool then yields<br><br>MB = 0 + FA(240) − P(40) = 0 which gives<br><br>P = 6FA = 6(15) = 90.0 N<br><br>Assume Impending Sliding at B<br><br>This assumption gives FB =0.4NB =0.4(75)=30 N. From the FBD of the spool, we now obtain<br><br>MA = 0 + − FB(240) + P(200) = 0 which gives<br><br>P = 1.2FB = 1.2(30) = 36.0 N<br><br>Choose the Correct Answer<br><br>Up to this point, the analysis has determined that sliding impends at A if P =90.0 N and at B if P =36.0 N. Consequently, the largest force P that can be applied without disturbing the static equilibrium of the spool is<br><br>P = 36.0 N Answer<br><br>with sliding impending at B.<br><br>An alternate method for solving this problem is to assume impending sliding at one surface and then to compare the friction force at the other surface with its limiting static value.|
|---|

![image 51](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile51.png>)

###### Problems

###### 7.1 Can the two blocks be in equilibrium in the position shown? Justify your

answer. All surfaces are frictionless except the horizontal surface beneath block B. 7.2 Determine the range of P for which the system of two blocks will be in

A 120 lb

20°

equilibrium. Friction is negligible except for the surface under block B.

B 80 lb

- 7.3 Two identical chairs, each weighing 14lb, are stacked as shown. The center of gravity of each chair is denoted by G. The coefﬁcient of static friction is 0.2 at B (the contact point between the chairs) and 0.35 at A, C, and D. Determine the smallest force P that would cause sliding.

G

A C D

P B G

20 in.

12 in. 12 in.

Fig. P7.3

- 7.4 The two homogeneous bars AB and BC are connected with a pin at B and placed between rough vertical walls. If the coefﬁcient of static friction between each bar and the wall is 0.4, determine the largest angle θ for which the assembly will remain at rest.

µ

µs = 0.2

Fig. P7.1

30°

A 120 lb

P

B 80 lb

µ

µs = 0.2

Fig. P7.2

B 20in.

20in.

6lb

8lb

θ θ

18 in.

A C

20 lb

###### Fig. P7.4

µ

µs = 0.75 µµs = 0.75

36 lb

30° 7.5 The contact surface between the 36-lb block and 20-lb homogenous cylin-

der is frictionless. Can the system be in static equilibrium on the rough inclined plane?

Fig. P7.5

- 7.6 Determine the smallest angle θ at which the uniform triangular plate of 6in.

9in.

A

W B

θ

Fig. P7.6

weight W can remain at rest. The coefﬁcient of static friction at A and B is 0.5.

- 7.7 The center of gravity of the 50-kg spool is at G. A cable wound around the hub of the spool is attached to the 30-kg block B. The coefﬁcients of static friction are 0.15 under the spool and 0.2 under the block. Determine the largest

counterclockwise couple C0 that can be applied to the spool without disturbing the equilibrium of the system.

G

B

C0

0.3 m

0.5 m

1.2 m

0.6 m

Fig. P7.7

- 7.8 The brake pads at C and D are pressed against the cylinder by the spring BF.

B

A

F

E

24 in.

16 in.

10 in.

8 in. 8 in.

C M D

Fig. P7.8

The coefﬁcient of static friction between each pad and the cylinder is 0.2. Find the smallest tension in the spring that would prevent the cylinder from rotating when the clockwise couple M = 3000 lb·in. is applied. Neglect the weights of the members.

- 7.9 Can the three identical cylinders be in equilibrium if they are stacked as

Fig. P7.9

shown? The static coefﬁcient of friction is 0.30 between the cylinders and 0.1 between the cylinders and the ground.

- 7.10 The rear-wheel-drive pickup truck, with its center of gravity at G, is to negotiate a bump from a standing start in the position shown. The static and kinetic coefﬁcients of friction between the tires and the pavement are 0.18 and 0.15, respectively. Determine the largest slope angle θ that can be negotiated, assuming that the drive wheels are (a) spinning; and (b) not spinning.

12 in.

60 in. 40 in.

A B

G

θ

Fig. P7.10, P7.11

- 7.11 Solve Prob. 7.10 assuming that the pick-up truck has front-wheel drive.
- 7.12 The 0.8-kg bar is pinned at A and rests on the 1.6-kg spool at B. Both

300

150

A

B

7575

125125

P

C

bodies are homogenous. If the coefﬁcient of static friction is 0.25 at both B and C, calculate the largest force P that can be applied without disturbing the equilibrium of the system.

Dimensions in mm

Fig. P7.12

P

7.13 The horizontal force P acts on the rim of the homogeneous cylinder of

radius R and weight W. Determine the smallest coefﬁcient of static friction that enables the cylinder to start rolling up the 30◦ incline.

R

30°

- 7.14 The uniform bar and the homogeneous cylinder each have a mass of 24kg. The static coefﬁcient of friction is µs at A, B, and C (the three points of contact).

- (a) Assuming equilibrium, calculate the normal and friction forces at A, B, and C.
- (b) What is the smallest value of µs necessary for equilibrium?

B

1 m

A

1.5m

C

0.333 m

2.6 ft

6.4 ft

C

A B

60° 60°

Fig. P7.14 Fig. P7.15

- 7.15 A stepladder consisting of two legs pinned together at C is resting on a rough ﬂoor. Will a 160-lb worker be able to change the light bulb if he is required to climb to a height of 2.6 ft? The uniform legs AC and BC weigh 22 lb and 14 lb, respectively. The coefﬁcient of static friction at A and B is 0.48.

Fig. P7.13

B 7.16 The mass of the unbalanced disk is m, and its center of gravity is located

at G. If the coefﬁcient of static friction is 0.2 between the cylinder and the inclined surface, determine whether the cylinder can be at rest in the position shown. Note that the string AB is parallel to the incline.

A

30

G

7.17 The two uniform sheets of plywood, each of length L and weight W, are propped as shown. If the coefﬁcient of static friction is 0.5 at all three contact surfaces, determine whether the sheets will remain at rest.

110

20°

Dimensions in mm

Fig. P7.16

L

L

60°

60°

###### Fig. P7.17

- 7.18 Find the smallest coefﬁcient of static friction at B and E that would permit the tongs to lift the 40-kg block. Neglect the mass of the tongs.

Dimensions in mm

200

1200

600

40 kg 240

P

O A

D

C

B E

300

Fig. P7.18

- 7.19 Determine the smallest force P that the worker must apply to the bar CD to prevent the homogeneous 80-kg spool from moving down the hill. The coefﬁcients of static friction are 0.12 at A and 0.36 at B. Neglect the weight of bar CD.

C

90°

15°

D

A

B

0.5 m

80 kg

P

Fig. P7.19, P7.20

- 7.20 Find the smallest force P that the worker must apply to the bar CD in order to initiate uphill motion of the homogeneous 80-kg spool. The coefﬁcients of static friction are 0.12 at A and 0.36 at B. Neglect the weight of bar CD.
- 7.21 The man is trying to push the homogeneous 20-kg ladder AB up a wall by

| | | | | | | | |A<br><br>B<br><br>P 1.5 m<br><br>|
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
|m| | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |

5

applying the horizontal force P. Determine the smallest value of P that would move the ladder. The coefﬁcient of static friction between the ladder and both contact surfaces is 0.3.

2 m

Fig. P7.21

- 7.22 A 2.2-lb disk A is placed on the inclined surface. The coefﬁcient of static friction between the disk and the surface is 0.4. Is the disk in equilibrium if P = 1.2 lb and θ = 30◦?

x

z

y

2 ft

6ft

|P θ|
|---|

A

P

A

G 45°

30°

6.4in.

9in.

Fig. P7.22 Fig. P7.23

- 7.23 The 40-lb spool is suspended from the hanger GA and rests against a vertical wall. The center of gravity of the spool is at G and the weight of the hanger is negligible. The wire wound around the hub of the spool is extracted by pulling its end with the force P. If the coefﬁcient of static friction between the spool and the wall is 0.25, determine the smallest P that will extract the wire.
- 7.24 A uniform plank is supported by a ﬁxed support at A and a drum at B that rotates clockwise. The coefﬁcients of static and kinetic friction for the two points of contact are as shown. Determine whether the plank moves from the position shown if (a) the plank is placed in position before the drum is set in motion; and (b) the plank is ﬁrst placed on the support at A and then lowered onto the drum, which is already rotating.

A

s = 0.18 k = 0.15

s = 0.32 k = 0.28

1 m 3 m 2 m

µ µ µ µ

B

Fig. P7.24

- 7.25 The uniform bar of weight W is supported by a ball-and-socket joint at A and rests against a vertical wall at B. If sliding impends when the bar is in the position shown, determine the static coefﬁcient of friction at B. [Hint: The

###### 7.4 Impending Tipping 361

direction of impending sliding is tangent to the dashed circle (the potential path of motion of point B).]

z

8in.

Path of impending motion of B

B

17in.

=

R

20in.

15 in.

A

x

y

###### Fig. P7.25

- 7.26 The uniform plank is initially at rest on the ﬁxed support at A and the stationary drum at B. If the drum begins rotating slowly counterclockwise, determine how far the plank will travel before it comes to rest again. (Note: Because the drum rotates slowly, the inertia of the plank may be neglected.)

| |
|---|

A

s = 0.36 k = 0.30

s = 0.32 k = 0.28

3 m 3 m

| |
|---|

B

µ µ µ µ

Fig. P7.26

- 7.27 The two homogeneous bars with the weights shown are connected with a

C

2W

b

W

pin at B and suspended from a pin support at C. The coefﬁcient of static friction between bar AB and the vertical wall is µs. Determine the smallest µs required to keep the assembly in equilibrium in the position shown.

A B

b

Fig. P7.27

###### 7.4 Impending Tipping

In the preceding article, we restricted our attention to sliding; the possibility of tipping was neglected. We now discuss problems that include both sliding and tipping as possible motions.

Consider again a homogeneous block on a friction surface being pushed by a force P, as shown in Fig. 7.4 (a). We assume that the weight W of the block, and the dimensions b, h, and d are known. We wish to determine the magnitude of P that will cause impending motion of the block, either impending sliding or impending tipping.

W y

P

b

x

G

###### P

d

h d

G

A

F

x

A

N

(b)

(a)

###### Fig. 7.4

We can gain insight into the solution by comparing the number of unknowns with the number of available equilibrium equations. From the free-body diagram of the block, Fig. 7.4(b), we see that there are four unknowns: the applied force P, the resultant normal force N, the friction force F, and the distance x that locates the line of action of N. Because there are only three independent equilibrium equations, an additional equation must be found before all unknowns can be calculated. If we assume impending sliding, the additional equation is F = Fmax =µsN. On the other hand, if impending tipping about corner A is assumed, the additional equation is x =b/2, because N acts at the corner of the block when tipping impends.

In the preceding article, three classes of friction problems were introduced for impending sliding. This classiﬁcation can be easily reworded to include the possibility of impending tipping.

- Type I The problem statement does not specify impending motion (sliding or tipping).
- Type II The problem statement implies impending motion, and the type of motion (sliding at known surfaces, or tipping) is known.
- Type III The problem statement implies impending motion, but the type of motion (sliding or tipping) and/or the surfaces where sliding impends are not known.

Examples of the three types of problems are given in the sample problems that follow.

|Sample Problem 7.8<br><br>The man in Fig. (a) is trying to move a packing crate across the ﬂoor by applying a horizontal force P. The center of gravity of the 250-N crate is located at its geometric center. Does the crate move if P =60 N? The coefﬁcient of static friction between the crate and the ﬂoor is 0.3.<br><br>0.6 m<br><br>1.8m<br><br>0.9m<br><br>(a)<br><br>P<br><br>Solution<br><br>This is a Type I problem because the problem statement does not specify impending motion. To determine if the crate moves for the conditions stated, we ﬁrst assume equilibrium and then check the assumption. However, the check must answer two questions—(1) does the crate slide and (2) does the crate tip?<br><br>The free-body diagram of the crate is shown in Fig. (b). If the block is assumed to remain in equilibrium, the three equilibrium equations can be used to calculate the three unknowns: the normal force N1, the friction force F1, and the distance x locating the line of action of N1, as shown in the following.<br><br>0.6 m<br><br>P = 60 N<br><br>N1<br><br>F1<br><br>x<br><br>y<br><br>x<br><br>1.8m<br><br>0.9m<br><br>O<br><br>(b)<br><br>250 N<br><br>|
|---|

|Assume Equilibrium<br><br>Fx = 0 −→+ P − F1 = 0 F1 = P = 60 N<br>Fy = 0 +  N1 − 250 = 0 N1 = 250 N<br><br><br>MO = 0 + N1x − P(0.9) = 0<br><br>which gives<br><br>x = P(0.9)/N1 = 60(0.9)/250 = 0.216 m<br><br>Check<br><br>The largest possible value for x is 0.3 m (half the width of the crate). Because x = 0.216 m, as obtained from equilibrium analysis, is smaller than that, we conclude that the block will not tip.<br><br>The limiting static friction force is (F1)max =µsN1 =0.3(250)=75.0 N, which is larger than the force F1 =60 N that is required for equilibrium. We therefore conclude that the crate will not slide.<br><br>Crate will not move when P = 60 N Answer<br><br>Sample Problem 7.9<br><br>Calculate the force P required to cause tipping of the packing crate in Sam-<br><br>P<br><br>FA<br><br>NA<br><br>A<br><br>0.6 m<br><br>y<br><br>x<br><br>1.8m<br><br>0.9m<br><br>250 N<br><br>ple Problem 7.8. Also determine the minimum coefﬁcient of static friction that permits tipping.<br><br>Solution<br><br>This is a Type II problem because impending tipping is speciﬁed. The free-body diagram for the crate is shown in the ﬁgure. Note that when the crate is on the verge of tipping, the normal force NA acts at corner A. There are three equilibrium equations that can be solved for the unknowns P, NA, and FA:<br><br>MA = 0 + 250(0.3) − P(0.9) = 0<br><br>P = 83.3 N Answer<br><br>Fx = 0 −→+ P − FA = 0 FA = P = 83.3 N<br>Fy = 0 +  NA − 250 = 0 NA = 250 N<br>|
|---|

|The minimum coefﬁcient of static friction that permits tipping is<br><br>µs = FA/NA = 83.3/250 = 0.333 Answer<br><br>Note that if the coefﬁcient of static friction were exactly 0.333, then the force P =83.3 N would result in simultaneous impending sliding and impending tipping.<br><br>Sample Problem 7.10<br><br>The winch in Fig. (a) is used to move the 300-lb uniform log AB. Compute the largest tension in the cable for which the log remains at rest. The coefﬁcient of static friction between the log and the plane is 0.4.<br><br>8 ft 60°<br><br>(a)<br><br>A B<br><br>Solution<br><br>Although we are asked to ﬁnd the cable tension that would cause impending motion, we do not know whether sliding or tipping impends. Therefore, this is a Type III problem.<br><br>The free-body diagram of the log in Fig. (b) contains four unknowns: tension T, resultant normal force N, friction force F, and x (the distance from A to the line of action of N). Because there are only three independent equilibrium equations, all unknowns cannot be calculated unless an assumption is made concerning the type of impending motion.<br><br>300 lb<br><br>x<br><br>A<br><br>N<br><br>F<br><br>4 ft 4 ft 60°<br><br>T<br><br>(b)<br><br>B<br><br>y<br><br>x|
|---|

|Assume Impending Sliding<br><br>Under this assumption, we have F = Fmax = 0.4 N, and the force equilibrium equations for the FBD in Fig. (b) are as follows.<br><br>Fx = 0 −→+ 0.4N − T cos60◦ = 0 (a)<br>Fy = 0 +  N − 300 + T sin60◦ = 0 (b)<br><br><br>Solving Eqs. (a) and (b) simultaneously, we obtain T =141.8 lb and N =177.2 lb.<br><br>Assume Impending Tipping<br><br>Under this assumption, N will act at A, as shown in the FBD in Fig. (c). The cable tension T can be computed from the moment equation<br><br>MA = 0 + T sin60◦(8) − 300(4) = 0<br><br>T = 173.2 lb<br><br>300 lb<br><br>A<br><br>N<br><br>F<br><br>4 ft 4 ft<br><br>T<br><br>(c)<br><br>B<br><br>60°<br><br>Choose the Correct Answer<br><br>Because T = 141.8 lb for impending sliding and T = 173.2 lb for impending tipping, the maximum tension that can be applied without moving the log is<br><br>T = 141.8 lb Answer<br><br>Alternate Solutions<br><br>As with most equilibrium problems, there are several equivalent methods of analysis that could be used. Two such methods are<br><br>1. Assume impending sliding, and solve for T. Continue the equilibrium analysis to ﬁnd x. Then check to see if this value of x is physically possible.<br>2. Assume impending tipping, and solve for T. Continue the equilibrium analysis to ﬁnd F. Then check to see if F ≤ Fmax.<br>|
|---|

7.28–7.43 Problems 367

![image 52](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile52.png>)

###### Problems

- 7.28 The man pushes the 120-lb homogeneous crate with the horizontal force P. Determine the largest distance h for which the crate will slide without tipping.

3 ft

6 ft

P

µs = 0.4

h

s= 0.3

0.4 m

P

1 m

1.2 m

0.5 m

G

µ

θ

Fig. P7.28 Fig. P7.29, P7.30

- 7.29 The 60-kg crate has its center of gravity at G. Determine the smallest force P that will initiate motion if θ =30◦.
- 7.30 Solve Prob. 7.29 if θ = 0.
- 7.31 The 120-lb door with its center of gravity at G is hung from a horizontal 54 in. 54 in.

84in.

18 in. 18 in. A B

G

54 in. 54 in.

P

Fig. P7.31

track at A and B. Find the largest coefﬁcient of static friction µs at A and B for which the door will slide without lifting off the track. Also, determine the corresponding force P.

- 7.32 Determine the largest force P for which the 18-kg uniform bar remains in equilibrium.

2 m 1 m

µs = 0.2 50° P

µ

Fig. P7.32

- 7.33 Determine the largest angle θ for which the homogeneous block remains

5ft

2ft

θ

µs =0.4

Fig. P7.33 at rest.

- 7.34 The cylinder and the block are connected by a horizontal cord. Determine

3 in.

3 lb 5 in. 3 lb

C

µs= 0.35

Fig. P7.34

the largest couple C that can be applied to the cylinder without disturbing the equilibrium of the system. Assume that both bodies are homogeneous.

- 7.35 The weight of the cylindrical tank is negligible in comparison to the weight of water it contains (water weighs 62.4 lb/ft3). The coefﬁcient of static friction

between the tank and the horizontal surface is µs. (a) Assuming a full tank, ﬁnd the smallest force P required to tip the tank, and the smallest µs that would allow tipping to take place. (b) If the force P =200 lb initiates tipping, determine the depth of water in the tank.

###### P

30°

1.4 ft

P

θ

B

4 ft

L

µµs= 0.2

A

20°

C

###### Fig. P7.35 Fig. P7.36

20ft

µ

µs = 0.6

- 7.36 Find the smallest angle θ for which a sufﬁciently large force P would cause the uniform log AB of weight W to tip about A.
- 7.37 The 40-lb ladder AC is leaning on a 10-lb block at B and a frictionless

8 ft 3 ft

B

µ

µs = 0.1

A

corner at C. Both bodies are homogeneous. Can the system remain at rest in the position shown? Be sure to consider all possibilities.

2 ft 10 ft

Fig. P7.37

- 7.38 Two concrete blocks weighing 320lb each form part of the retaining wall of a swimming pool. Will the blocks be in equilibrium when the pool is ﬁlled and the water exerts the line loading shown?

10 in.

18 in.

18 in. Plastic

liner

32 lb/in.

µs=0.5

µs=1.0

h

θ

b

µs

Fig. P7.38 Fig. P7.39

- 7.39 Derive the expression for the largest angle θ for which the homogeneous block stays in equilibrium.
- 7.40 Find the weight of the lightest block D that can be used to support the

C

µs= 0.2

B

15ft

D

8 ft

µs= 0.2

A

6 ft 2 ft

###### Fig. P7.40 200-lb uniform pole ABC in the position shown.

- 7.41 The 2000-lb weight of the trailer is distributed equally between its two wheels, one on each side of the trailer. The center of gravity is at G, and the wheels are free to rotate. Determine whether the trailer can be pushed over a 6-in. curb without tipping, and, if so, compute the required horizontal force P.

R = 12 in.

18 in.

20 in.

P G

6 in.

A

µs= 0.4 36 in.

Fig. P7.41

- 7.42 Determine the smallest force P, applied to the plunger D, that will prevent the couple C = 250 N·m from moving the cylinder. Friction may be neglected at all surfaces, except between the plunger and cylinder. The masses of the bodies are negligible.

P

40 mm

30°

A B

C

30°

D µs= 1.6

Fig. P7.42

- 7.43 The weights of the homogeneous roller and the wedge are 100 lb and 40 lb,

2 ft

C 30°

respectively. The coefﬁcient of static friction is 0.2 between all contact surfaces. Fig. P7.43 Find the smallest couple C that will move the cylinder.

###### 7.5 Angle of Friction; Wedges and Screws

###### a. Angle of friction

Figure 7.5 shows a block on a friction surface subjected to the horizontal force P. As seen in the free-body diagram, we let φ be the angle between the contact force R and the normal n to the contact surface. The angle φ is given by tanφ = F/N, where N and F are the normal and friction forces, respectively. The upper limit of φ, denoted by φs, is reached at impending sliding when F = Fmax =µsN. Therefore, we have

###### tanφs = µs (7.4)

P

W

µ

s

W P

O

F

R

φ

N

n FBD

###### Fig. 7.5

The angle φs is called the angle of static friction. Note that φ ≤ φs signiﬁes equilibrium and that φ = φs indicates impending sliding. Therefore, the direction of the contact force R is known at all surfaces where sliding impends. This knowledge can be frequently utilized to gain insight into problems involving two- and three-force bodies.

In Fig. 7.5, the friction force F opposes the tendency of P to slide the block to the right. If the direction of P is reversed, the direction of F would also be reversed. This leads to the conclusion that the block can be in equilibrium only if the line of action of R stays within the sector AOB (bounded by ±φs), as shown in Fig. 7.6. For more general loadings, the line of action of R must lie within the cone, called the cone of static friction, that is formed by rotating sector AOB about the normal n. Observe that the vertex angle of the cone of static friction is 2φs.

O

Equilibrium range of the line of action of R

φs φs

A B n

###### Fig. 7.6

When sliding occurs, the friction force is F = µkN, and the value of φ that speciﬁes the direction of R is given by

###### tanφk = µk (7.5)

The angle φk is called the angle of kinetic friction. For this case, the cone of static friction is replaced by the smaller cone of kinetic friction, for which the vertex angle is 2φk.

###### b. Wedges

A wedge is a simple device that is used for the same purpose as a lever—to create a mechanical advantage. Consider, for example, the wedge shown in Fig. 7.7(a) that is being forced into a crack by the applied force P. The angle formed by the tip of the wedge is 2β, where β is called the wedge angle. Neglecting the weight, the free-body diagram of the wedge at impending sliding is shown in Fig. 7.7(b). As before, we let φ be the angle between the contact force R and the normal n to the contact surface. Because sliding impends, φ =φs, where φs = tan−1 µs is the angle of friction. From the force diagram in Fig. 7.7(c) we see that R = P/[2sin(φs +β)], which is substantially larger than P if the wedge angle β is small and the sides of the wedge are lubricated (giving a small value for φs).

###### P

P

R

2β

β β β β

φ φ

s +

n R

n

s +

R

φ φ φ φ

= s = s

R

P

(c)

(a)

(b)

###### Fig. 7.7

Ideally, a wedge should be slippery enough to be easily driven into the crack, but have enough friction so that it stays in place when the driving force is removed. In the absence of P, the wedge becomes a two-force body. Therefore, the contact forces R must be collinear, as indicated in the free-body diagram in Fig. 7.8, where now φ =β. Recalling that equilibrium can exist only if φ ≤φs, we conclude that the wedge will stay in place provided that β ≤φs.

φ = β φ = β 2β

R

R

n

n

###### Fig. 7.8

###### c. Square-threaded screws

r

| | |
|---|---|
| | |
| | |
| | |

Screws with square threads are employed in jacks, vises, and other devices that produce a large axial force by applying a relatively small couple about the axis of the screw. A square-threaded screw can be viewed as a bar of rectangular cross section wrapped around a cylinder in a helical fashion, as shown in Fig. 7.9. The

p

helix angle θ is called the lead angle, the distance p between the threads is known as the pitch, and the mean radius of the threads is denoted by r. It can be seen that these parameters are related by

θ

p = 2πr tanθ (7.6)

Figure 7.10 (a) shows a screw being employed as a jack. Assuming that the couple C0, called the torque, is large enough, it will cause the screw to advance, thereby elevating the weight W. The analysis of this problem is simpliﬁed if we recall that in Coulomb’s theory the friction force is independent of the contact area. Therefore, we can assume the contact area to be very small, as illustrated in Fig. 7.10(b). Note that the entire weight W is carried by the contact area and that the horizontal force Q = C0/r is supplied by the applied torque C0. We can now see that this problem is identical to the one shown in Fig. 7.11(a)—namely, a block of weight W being pushed up an incline by the horizontal force Q.

Fig. 7.9

###### W

| | |
|---|---|
| | |
| |C0|

W

r

Contact area

Q = C0/r

(a) (b)

###### Fig. 7.10

The smallest torque required to start the weight W moving upward can now be obtained from the FBD in Fig. 7.11(b). Note that at impending sliding the angle between R and the normal n to the contact surface is φ = φs, and that the direction of φs relative to the normal n indicates that the impending motion is directed up the incline. For equilibrium of the block, we have

C0 r − R sin(φs + θ) = 0 (a)

###### Fx = 0 −→+

###### Fy = 0 +  R cos(φs + θ) − W = 0 (b)

W

W

W

y

C0/r

C0/r

Q = C0/r

x

θ

R

φ φ

= s

φ = φs n

θ

R

θ

n

(a)

(b)

(c)

###### Fig. 7.11

Solving Eqs. (a) and (b), we ﬁnd that the smallest torque that will cause the weight W to move upward is

###### (C0)up = Wr tan(φs + θ) (7.7a)

If we reverse the direction of C0 and assume impending motion down the incline, the FBD in Fig. 7.11(c) must be used. It is seen from the equilibrium equations that the torque required to cause the weight W to move downward is

###### (C0)down = Wr tan(φs − θ) (7.7b)

If φs ≥ θ, the torque C0 in Eq. (7.7b) is positive, which means that the weight W remains at rest if C0 is removed. In this case, the screw is said to be self-locking. On the other hand, if φs <θ, the torque C0 in Eq. (7.7b) is negative, indicating that the weight W would come down by itself in the absence of C0.

|Sample Problem 7.11<br><br>Using the angle of friction, determine the smallest angle θ for which the slender<br><br>A<br><br>L<br><br>B<br><br>s = 0.5<br><br>(a)<br><br>θ µ<br><br>bar shown in Fig. (a) can remain at rest. The bar is homogeneous of weight W and length L. Neglect friction between the bar and wall at B.<br><br>Solution<br><br>As shown in the FBD, Fig. (b), the bar is acted on by three forces: the weight W acting at the midpoint of the bar, the horizontal normal force NB, and the reaction RA at the horizontal surface. Because impending motion is speciﬁed, the angle φ between RA and the normal to the contact surface is equal to its limiting value: φ =φs = tan−1 µs = tan−1 0.5 = 26.57◦. Because the bar is a three-force member, the forces intersect at point C.<br><br>A θ<br><br>φ φ<br><br>B<br><br>L<br><br>/2<br><br>W<br><br>E D<br><br>NB<br><br>RA = s = 26.57°<br><br>C<br><br>L<br><br>/2<br><br>26.57°<br><br>(b)<br><br>From triangle ABD we see that<br><br>tanθ =<br><br>BD AD<br><br>(a)<br><br>From triangle ACE we obtain AE = CE tan26.57◦. Because AD = 2AE, this becomes<br><br>AD = 2CE tan26.57◦ (b) Substituting Eq. (b) into Eq. (a) together with BD = CE, we get<br><br>tanθ =<br><br>CE<br><br>2CE tan26.57◦ =<br><br>1 2tan26.57◦ which yields<br><br>θ = 45.0◦ Answer<br><br>By using the angle of friction and by recognizing the bar to be a three-force member, we were able to ﬁnd θ from geometry, without having to write the equilibrium equations.|
|---|

###### 374

|Sample Problem 7.12<br><br>The screw press shown is used in bookbinding. The screw has a mean radius of 10 mm and its pitch is 5 mm. The static coefﬁcient of friction between the threads is 0.18. If a clamping force of 1000 N is applied to the book, determine (1) the torque that was applied to the handle of the press; and (2) the torque required to loosen the press.<br><br>Solution<br><br>The lead angle of the screw is computed from Eq. (7.6).<br><br>θ = tan−1<br><br>p<br><br>2πr = tan−1<br><br>5<br><br>2π(10) = 4.550◦ The friction angle is<br><br>φs = tan−1 µs = tan−1 0.18 = 10.204◦<br><br>Part 1<br><br>The torque required to apply the force W = 1000 N can be calculated from Eq. (7.7a).<br><br>C0 = Wr tan(φs + θ) = 1000(0.01)tan(10.204◦ + 4.550◦) C0 = 2.63 N · m Answer<br><br>Part 2 The torque needed to loosen the press is obtained from Eq. (7.7b).<br><br>C0 = Wr tan(φs − θ) = 1000(0.01)tan(10.204◦ − 4.550◦) C0 = 0.990 N · m Answer|
|---|

###### 375

![image 53](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile53.png>)

###### Problems

###### The following problems are to be solved using the angle of friction. Utilize the characteristics of two-force and/or three-force bodies wherever applicable.

###### L

60° 30°

7.44 The uniform bar of length L and weight W is kept in the horizontal

position by friction. Determine the smallest possible coefﬁcient of static friction between the bar and the inclined surfaces.

7.45 The movable bracket of negligible weight is mounted on a vertical post.

Fig. P7.44

The coefﬁcient of static friction between the bracket and the post is 0.2. Determine the smallest ratio b/a for which the bracket can support the vertical force P. Assume that the diameter of the post is negligible. (Note: Because the result is independent of P, the bracket is said to be self-locking.)

P

b

- A
- B

- 7.46 The 200-lb man walks up the inclined plank of negligible weight. The coefﬁcients of static friction at A and B are 0.3 and 0.2, respectively. Determine the distance x at which the plank would begin to slide.

20ft

x

B

20° A

Fig. P7.46

- 7.47 The four-wheel drive vehicle of weight W attempts to climb a vertical obstruction at A. The center of gravity of the vehicle is at G, and the coefﬁcient

of static friction is µs at A and B. Find the smallest µs necessary to initiate the climb. (Hint: Slipping must impend at A and B simultaneously.)

11 ft

5.6 ft

A 1.5 ft 3.2 ft

G

B

Fig. P7.47

- 7.48 Find the smallest distance d for which the hook will remain at rest when

a

Fig. P7.45

µs=0.6

A

2 in.

d

B

3 in.

P

acted on by the force P. Neglect the weight of the hook, and assume that the vertical wall is frictionless.

Fig. P7.48

###### 7.44–7.58 Problems 377

- 7.49 The ﬁgure shows a locking device that is used in some belt buckles. When the belt is pulled to the right by the force P, the roller A becomes jammed between the belt and the upper surface of the buckle. If the coefﬁcient of static friction between all surfaces is 0.24, determine the largest angle θ for which the buckle is self-locking (motion of the belt in either direction is prevented even after the force P is removed). Neglect the weight of roller A.

P

Flexible belt

θ

A

4000 kg

s = 0.12

s = 0.2

A B

µ

µ

θ

Fig. P7.49 Fig. P7.50

- 7.50 A small wedge is placed beneath corner B of the 4000-kg block of marble. Determine the largest angle θ for which the wedge is self-locking; that is, the wedge will not slide out from under the block. Neglect the mass of the wedge and the small angle between surface AB and the horizontal.
- 7.51 The two 200-lb blocks are pushed apart by the 15◦ wedge of negligible weight. The angle of static friction is 12◦ at all contact surfaces. Determine the the force P required to start the blocks moving.

15° 15° 200 lb 200 lb

P

φ s = 15° φ s = 12° P β P

Fig. P7.51 Fig. P7.52

- 7.52 The wedge with the angle β is squeezed between two blocks as shown. 20 mm 48 mm

O

27 mm

A B

S

C

µ

Fig. P7.53

Determine the largest β for which the wedge will not move regardless of the magnitude of the squeezing force P. Neglect the weight of the wedge.

- 7.53 The device shown is used to measure the kinetic coefﬁcient of friction between the rotating shaft S and the homogeneous stationary collar C. The entire 840-N weight of the collar is supported by the shaft. The spring scale attached to the collar at A measures the tension in AB caused by the counterclockwise rotation of the shaft. What is the coefﬁcient of kinetic friction if the reading on the scale is 150 N?

- 7.54 The single-threaded screw of the ﬂoor jack has a pitch of 0.5in. and a mean radius of 1.75in. The angle of static friction is 8.5◦. (a) Determine the couple C that must be applied to the screw to start lifting a weight of 4000lb. (b) What is the couple required to start lowering the weight?

C

4000 lb

P

7.5° 7.5°

A B

Fig. P7.54 Fig. P7.55

- 7.55 The force P = 900 lb is required to push the wedge into the crack, starting from the position shown. It is also known that a force of 250 lb is required to pull the wedge out of the crack from this position. Determine the coefﬁcient of static friction between the wedge and the corners of the crack. Assume that the horizontal components of the contact forces at A and B are the same for both cases.
- 7.56 The square-threaded screw of the C-clamp has a mean diameter of 9 mm

C

and a pitch of 1.5 mm. The coefﬁcient of static friction between the threads is 0.2. If the torque C = 1.25 N · m is used to tighten the clamp, determine (a) the clamping force; and (b) the torque required to loosen the clamp.

7.57 The square-threaded screw with a pitch of 10 mm and a mean radius of 18 mm drives a gear that has a mean radius of 75 mm. The static and kinetic

Fig. P7.56

C1

75 mm

C0

| | | |
|---|---|---|
| | | |

###### Fig. P7.57

coefﬁcients of friction between the gear and the screw are 0.12 and 0.06, respectively. The input torque applied to the screw is C0 = 10 N·m. Assuming constant speed operation, determine the output torque C1 acting on the gear.

7.58 The screw of the car jack has a pitch of 0.1in. and a mean radius of 0.175 in. Note that the ends of the screw are threaded in opposite directions (rightand left-handed threads). The coefﬁcient of static friction between the threads is 0.08. Calculate the torque C0 that must be applied to the screw in order to start the 1200-lb load moving (a) upward; and (b) downward.

1200 lb

C0

30°

30°

###### Fig. P7.58

###### *7.6 Ropes and Flat Belts

The theory of Coulomb friction can also be used to analyze the forces acting between a ﬂexible body, such as a rope or belt, and a friction surface.

Figure 7.12 shows a weight W that is held in static equilibrium by a rope that passes over a peg. If the peg is frictionless, then P = W; that is, the peg simply reverses the direction of the rope without changing its tension. If the contact surface between the peg and the rope has friction, the friction force will help to keep the weight from falling. In this case, it is possible to have P < W and still

P

W

###### Fig. 7.12

maintain equilibrium. A good example of this principle in action is the capstan—a device for fastening a ship to the dock. Other applications are belt drives and band brakes. In a belt drive, the friction between the belt and the pulleys enables power to be transmitted between rotating shafts. Band brakes use friction between a band (belt) and a cylindrical drum to reduce the speed of rotating machinery.

Figure 7.13 (a) shows a thin, ﬂat belt that passes over a cylinder of radius r.

Assuming that there is friction between the belt and the cylinder, the tensions T1 and T2 are not equal. According to the theory of dry friction, the belt is in one of the following states depending on the values of T1 and T2: equilibrium without impending slipping, equilibrium with impending slipping, or slipping. The analysis that follows determines the relationship between T1 and T2 for the last two cases.

A θ B

r

O

T1 T2

The forces acting on the belt are shown in Fig. 7.13(b), where the weight of the belt is assumed to be negligible. The cylinder exerts normal and friction forces on the belt, both of which are distributed along the contact area between A and B. Because the direction of impending motion (or motion) of the belt is assumed to be clockwise, equilibrium implies that T2 > T1.* Because the contact forces are distributed, it is necessary to perform the equilibrium analysis on an inﬁnitesimal (differential) length of the belt that subtends the differential angle dα.

(a)

Assumeddirection ofimpendingmotion (ormotion)

Distributed friction force

The free-body diagram of the differential element is shown in Fig. 7.13(c), where n and t refer to the directions that are normal and tangent to the cylindrical surface at the center of the element. The belt tension on the left side of the element is denoted by T, and the tension on the right side by (T + dT), where the differential change in the tension is dT =(dT/dα)dα. The angle between each tension and the t-direction is dα/2. The element is also subjected to the normal force dN and to the friction force dF, acting in the n- and t-directions, respectively.

dα

A B

α

O

Distributed normal force

T1 T2

(b)

Equilibrium of forces in the tangential direction yields

n

α

dα d

2

dα

dα

2 t

Ft = 0 + (T + dT)cos

2 − dF = 0 (a) Because the cosine of an inﬁnitesimal angle equals 1, Eq. (a) reduces to

2 − T cos

dT

T+

dF dN

T

dF = dT (b)

dα

The balance of forces in the normal direction gives

dα

dα

O

2 = 0 (c)

2 − T sin

Fn = 0 + dN − (T + dT)sin

(c)

Assuming that α is measured in radians, sin(dα/2) can be replaced by dα/2, an identity that is valid for inﬁnitesimal angles. Making this substitution gives

Fig. 7.13

dα

dα

2 = 0 (d)

dN − (T + dT)

2 − T

*The equilibrium equations are applicable even if the belt is moving. Because the weight of the belt is assumed to be negligible, inertial effects can be omitted except for very high speeds.

Neglecting the product of differentials (dT dα) compared to Tdα (this is not an approximation), we have

###### dN = T dα (e)

If the belt is slipping or if motion impends, we have the additional equation dF = µdN, where µ = µk (slipping), or µ = µs (impending slipping). Substituting this for dF in Eq. (b) and eliminating dN between Eqs. (b) and (e), we obtain

###### dT T = µdα (f)

Integrating both sides of Eq. (f) over the contact angle θ shown in Fig. 7.13(a), we get

dT T = µ

θ

θ

###### dα

0

0

Noting that T = T1 when α =0, and T = T2 when α = θ, integration yields

###### ln(T2/T1) = µθ

which can be written as

###### T2 = T1eµθ (7.8)

where e = 2.718 . . . is the base of natural (Naperian) logarithms. If the tension in one side of the belt is known, Eq. (7.8) can be used to calculate the belt tension in the other side.

The following points should be kept in mind when using Eq. (7.8).

- • T2 is the belt tension that is directed opposite the belt friction. Thus, T2 must always refer to the larger of the two tensions.
- • For impending motion, use µ = µs. If there is relative motion between the belt and cylinder, use µ = µk.
- • The angle of contact θ must be expressed in radians.
- • Because Eq. (7.8) is independent of r, its use is not restricted to circular contact surfaces; it may also be used for a surface of arbitrary shape.

|Sample Problem 7.13<br><br>The block of weight W is supported by a rope that is wrapped one-and-one-half<br><br>W P<br><br>times around the circular peg. Determine the range of values of P for which the block remains at rest. The coefﬁcient of static friction between the rope and the peg is 0.2.<br><br>Solution<br><br>The tension in the portion of the rope that is attached to the block is obviously equal to W. Because motion impends, Eq. (7.8) can be used to relate this tension to P. Because the angle of contact is θ = 1.5(2π) = 3π rad, Eq. (7.8) becomes<br><br>T2 = T1eµsθ = T1e0.2(3π) = 6.59T1<br><br>Recall that in this equation, T2 refers to the larger of the two tensions.<br><br>The largest value of P for equilibrium occurs when the block is on the verge of moving upward. For this case we must substitute T1 = W and T2 = P into the preceding equation. The result is P = 6.59W.<br><br>The smallest value of P corresponds to impending motion of the block downward, when W will be larger than P. Substituting T1 = P and T2 = W, we have W = 6.59P, or P = W/6.59 = 0.152W.<br><br>Therefore, the block is at rest if P is in the range 0.152W ≤ P ≤ 6.59W Answer<br><br>Sample Problem 7.14<br><br>As shown in Fig. (a), a ﬂexible belt placed around a rotating drum of 4-inch radius acts as a brake when the arm ABCD is pulled down by the force P. The coefﬁcient of kinetic friction between the belt and the drum is 0.2. Determine the force P that would result in a braking torque of 400-lb · in., assuming that the drum is rotating counterclockwise. Neglect the weight of the brake arm.<br><br>2 in.<br><br>A B C<br><br>D<br><br>P<br><br>(a)<br><br>4in.<br><br>O<br><br>60° 60°<br><br>2 in. 4 in. 2 in.|
|---|

###### 382

|Solution<br><br>The free-body diagram of the belt is shown in Fig. (b). The distributed contact forces exerted by the drum have been replaced by the equivalent force-couple system at O. The resultant force R is not of interest to us, but the couple CR represents the braking torque; that is, CR = 400 lb·in. Note that CR has the same sense as the rotation of the drum—namely, counterclockwise. The moment equation of equilibrium, with O as the moment center, is<br><br>MO = 0 + (TC − TB)4 − 400 = 0 (a)<br><br>Equation (7.8) provides us with another relationship between the belt tensions. Substituting µ = µk = 0.2, T1 = TB, T2 = TC (note that TC > TB), and θ = 240(π/180) = 1.333π rad, Eq. (7.8) becomes<br><br>TC = TBe0.2(1.333π) = 2.311TB (b) The solution of Eqs. (a) and (b) is TB = 76.3 lb and TC = 176.3 lb.<br><br>The force P can now be found by the balance of moments about A on the FBD of the brake arm, shown in Fig. (c):<br><br>MA = 0 + TB sin60◦(2) + TC sin60◦(6) − P(8) = 0<br><br>O<br><br>60°<br><br>(b)<br><br>60°<br><br>TB TC<br><br>CR<br><br>240°<br><br>120°<br><br>R<br><br>60° 60°<br><br>D<br><br>P<br><br>(c)<br><br>Ax A B C<br><br>TB TC<br><br>Ay<br><br>2 in. 4 in. 2 in.<br><br>Substituting the values for TB and TC, and solving for P, gives<br><br>P = 131.0 lb Answer|
|---|

###### 383

![image 54](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile54.png>)

###### Problems

- 7.59 How many turns of rope around the capstan are needed for the 60-lb force to resist the 9000-lb pull of a docked ship? The static coefﬁcient of friction between the capstan and the rope is 0.2.

9000 lb 60 lb

8 in.

12 in.

6 in.

P

µk= 0.2

Fig. P7.59 Fig. P7.60, P7.61

- 7.60 The force P applied to the brake handle enables the band brake to reduce the angular speed of a rotating drum. If the tensile strength of the band is 3800lb, ﬁnd the maximum safe value of P and the corresponding braking torque acting on the drum. Assume that the drum is rotating clockwise.
- 7.61 Solve Prob. 7.60 if the drum is rotating counterclockwise.
- 7.62 The rope running over two ﬁxed cylinders carries the 4-kg mass at one end. Determine the force P that must be applied to the other end to initiate motion. The coefﬁcient of static friction between the rope and the cylinders is 0.15.

4 kg

150 mm 150 mm

A+ B+

P 400 mm

Fig. P7.62

- 7.63 The leather rein used to fasten the horse to the hitching rail weighs 4 oz

60°

Horizontal

L

per foot. The coefﬁcient of static friction between the rail and the rein is 0.6. If a 30-lb force acting on the bridle is sufﬁcient to restrain the horse, determine the smallest safe length L for the free end of the rein.

Fig. P7.63

###### 7.59–7.68 Problems 385

- 7.64 The 30-lb weight is attached to a rope that runs over a ﬁxed cylinder. The

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |

30 lb P

Fig. P7.64

coefﬁcient of static friction between the rope and the cylinder is 0.3. Determine the range of the force P for which the system will be at rest.

- 7.65 The rail AB of negligible weight is suspended from a rope that runs around

A B

x

10 ft

|W|
|---|

Fig. P7.65

two ﬁxed pegs. The coefﬁcient of static friction between the rope and the pegs is 0.5. As the weight W moves along the rail toward end B, determine its position x when the rope is about to slip on the pegs.

- 7.66 The sling with a sliding hook is used to hoist a homogeneous drum. If the static coefﬁcient of friction between the cable and the eye of the hook is 0.6, determine the smallest possible value for the angle θ.

µs = 0.6 θ θ

| | |
|---|---|
| | |

| | |
|---|---|
| | |

150 lb

4 in.

+

+

4 in.

P

A

B

16 in.

Fig. P7.66 Fig. P7.67

- 7.67 The 150-lb weight is attached to a rope that passes over the ﬁxed cylinders A and B. The coefﬁcient of static friction between the rope and the cylinders is 0.3. Determine the smallest force P that keeps the system at rest.
- 7.68 The 50-lb homogeneous bar AB is suspended from a rope that runs over a small peg at C. The bar is kept in the position shown by the horizontal force P. Determine the smallest coefﬁcient of static friction at C for which the bar will be at rest.

C

|4 ft|6 ft<br><br>8 ft| |
|---|---|---|
| | | |

P B

A

###### Fig. P7.68

###### *7.7 Disk Friction

When a disk or the end of a shaft is pressed against a ﬂat surface, its rotation is resisted by a frictional couple, known as disk friction. Some examples of disk friction are illustrated in Fig. 7.14. The friction clutch consists of two disks that are

C

P P

coated with special high-friction materials. When the disks are pressed together by an axial force P, as shown in Fig. 7.14(a), they are capable of transmitting a large torque C without slipping. Axial loads carried by rotating shafts are sometimes supported by pivot bearings and collar bearings, shown in Fig. 7.14(b) and (c), respectively. In a pivot bearing, the axial force is distributed over the end of the shaft; in a collar bearing, the load is carried by the annular area of the collar. In both cases the torque C is required to overcome the rotational resistance of the bearing.

C

- (a) Friction clutch

P

- (b) Pivot bearing

P

- (c) Collar bearing

| | |
|---|---|
| |C|

In order to analyze the frictional couple, consider the hollow shaft with inner radius Ri and outer radius Ro shown in Fig. 7.15(a). The shaft is pressed against a ﬂat surface by the axial force P, and the torque required to overcome the frictional couple is denoted by C. The objective of our analysis is to determine the relationship between P and C. Following the practice of the preceding article, we denote the coefﬁcient of friction by µ. If the shaft is rotating, then µ is to be interpreted as µk; for impending rotation, µs should be used.

| | |
|---|---|
| | |

Figure 7.15(b) shows the normal force dN and the friction force dF acting on the inﬁnitesimal element of area dA at the end of the shaft. If the shaft is rotating, or about to rotate, then dF = µdN. The equilibrium equations of the shaft are

C

Fig. 7.14

Faxial = 0 P − dN = 0

Maxis = 0 C − r dF = C − µ r dN = 0

Contact region

| | |
|---|---|
| | |

Ri

P

Ro

C

(a)

P

dθ

dF

C dF

dr

r

dA

dN

dA

Ro Ri

(b)

###### Fig. 7.15

###### 7.7 Disk Friction 387

where the integrals are to be computed over the contact region , which is an annular ring of area A = π(R2o − Ri2). Denoting the normal contact pressure by p, we have dN = p dA, and the equilibrium equations become

P = p dA (7.9)

C = µ pr dA (7.10)

In order to perform the integrations, the variation of the normal pressure p over the contact region must be known. This variation depends on whether the contact surfaces are new or worn.

New Surfaces For new, ﬂat contact surfaces, it is reasonable to assume that the pressure p is uniformly distributed. Therefore, Eq. (7.9) becomes P = pA, and the contact pressure is given by

P π Ro2 − Ri2

P A =

p =

Taking p outside the integral in Eq. (7.10) gives C = µp r dA. As shown in

- Fig. 7.15(b), dA can be expressed in terms of polar coordinates as dA = r dθ dr. Therefore, the torque required to overcome the friction couple becomes

2π

Ro

µP π Ro2 − Ri2

###### r2 dθ dr

C =

0

Ri

which, after evaluating the integrals, becomes:

Ro3 − Ri3 Ro2 − Ri2

- 2µP

- 3

(7.11)

C =

If the cross section is a solid circle of radius Ro(Ri = 0), the above expression reduces to

2µPRo 3

(7.12)

C =

Worn Surfaces Although the normal pressure p may be initially uniform between two new, ﬂat surfaces, the wear will not be uniform. The wear at a given point on the cross section will depend on both the pressure and the distance traveled by the point during slipping. Because the distance traveled is proportional to

r (a point at a radial distance r travels the distance 2πr in one revolution of the shaft), greater wear will occur at points farther from the axis of the shaft. Once the contact surfaces have been broken in, it is reasonable to assume that the cross section will have worn to a shape for which the rate of wear is constant. In this situation, we would have pr = K, where K is a constant. For a hollow cross section, Eq. (7.10) then becomes

###### C = µK dA = µKπ Ro2 − Ri2 (7.13)

The constant K can be calculated by substituting p = K/r into Eq. (7.9), resulting in

2π

Ro

K r

P = p dA =

r dθ dr = 2πK (Ro − Ri)

0

Ri

from which

P 2π (Ro − Ri)

K =

Substituting this expression for K into Eq. (7.13), the torque required to overcome the friction couple is

µP 2

(Ro + Ri) (7.14)

C =

For a solid shaft of radius Ro, we have Ri =0 and the torque reduces to

µPRo 2

(7.15)

C =

|Sample Problem 7.15<br><br>Figure (a) shows a disk clutch that transmits torque from the input shaft on the left to the output shaft on the right. The clutch disk is splined to the input shaft, thereby forcing the clutch disk and the shaft to rotate together but allowing the disk to slide along the shaft. The normal force between the two halves of the clutch is provided by the compression spring. The force F applied to the clutch pedal can disengage the clutch by sliding the throw-out bearing to the left. Determine the largest torque that can be transmitted if the value of F necessary to disengage the clutch is 20lb. Solve for both new and worn friction surfaces.<br><br>3 in.<br><br>5 in.<br><br>4.5 in.<br><br>18in.<br><br>(a)<br><br>F<br><br>Compression spring<br><br>Output shaft<br><br>Clutch<br><br>disk Throw-out<br><br>bearing<br><br>Input shaft<br><br>Bearing<br><br>Friction surface,µs = 0.6<br><br>Solution<br><br>Utilizing the free-body diagram of the clutch pedal assembly, Fig. (b), we get<br><br>MA = 0 + 20(18) − P(4.5) = 0<br><br>P = 80 lb<br><br>This is the normal force acting on the friction surface when the clutch is engaged. The largest torque that can be transmitted equals the friction couple for this value of P.<br><br>18in.<br><br>(b)<br><br>F = 20 lb<br><br>4.5 in.<br><br>Ay<br><br>A Ax<br><br>P<br><br>For a new friction surface, Eq. (7.11) gives<br><br>C =<br><br>2µs P<br><br>3<br><br><br>Ro3 − Ri3 Ro2 − Ri2 =<br><br>2(0.6)(80) 3<br><br>53 − 33 52 − 32<br><br>= 196.0 lb · in. Answer<br><br>After the friction surfaces have become worn, we have from Eq. (7.14)<br><br>C =<br><br>µs P 2<br><br>(Ro + Ri) =<br><br>0.6(80) 2<br><br>(5 + 3) = 192.0 lb · in. Answer|
|---|

###### 389

|Sample Problem 7.16<br><br>The normal pressure under a circular industrial glass polisher is axially symmetric and varies linearly from p0 at r =0 to zero at r = R, as shown in the ﬁgure. Derive the expression for the torque required to rotate the polisher in terms of the axial load P. The coefﬁcient of kinetic friction between the polisher and the glass is µk.<br><br>P<br><br>C<br><br>| | |
|---|---|
|p0|r<br><br>R<br><br>p<br><br>|
<br><br>Solution<br><br>The pressure p at the radial distance r is given by p = p0(R − r)/R. Substituting this expression into Eq. (7.10), the torque C required to rotate the polisher is<br><br>C = µk pr dA =<br><br>µk p0 R<br><br>R<br><br>0<br><br>2π<br><br>0<br><br>(R − r)r2 dθ dr<br><br>=<br><br>πµk p0R3 6<br><br>The relationship between p0 and P can be obtained from Eq. (7.9).<br><br>P = p dA =<br><br>p0 R<br><br>R<br><br>0<br><br>2π<br><br>0<br><br>(R − r)r dθ dr =<br><br>πp0R2 3<br><br>Substituting p0 = 3P/π R2 into the expression for C yields<br><br>C =<br><br>µk PR 2<br><br>Answer|
|---|

7.8 Rolling Resistance 391

###### *7.8 Rolling Resistance

Up to this point, our discussion of friction has dealt only with rigid bodies. Deformation (if any) was assumed to be negligible. For example, consider a rigid wheel of weight W and radius R that is rolling on a rigid, horizontal surface with a constant velocity. The FBD of the wheel is shown in Fig. 7.16(a). Because W and the contact force N are perpendicular to the direction of travel, the wheel encounters no resistance and, therefore, will roll forever.

W

###### R W

R

F

φ

a

A

N

N (a)

(b)

###### Fig. 7.16

In the real world, both the wheel and the surface deform in the region of contact. As a consequence, contact occurs over a ﬁnite area rather than at a point,

- as illustrated in Fig. 7.16(b). The deformation in front of the wheel retards the motion, whereas the material behind the wheel is in recovery, thereby assisting the motion. During the deformation–recovery cycle some of the mechanical energy invariably is converted to heat—a phenomena called hysteresis. Consequently, the retarding force due to deformation always is greater than the propulsion force from the recovering material, so that the contact force N has a horizontal component opposing the motion, as indicated in Fig. 7.16(b). To keep the wheel rolling
- at a constant velocity now requires the application of a horizontal force F equal to the horizontal component of N. The magnitude of the force F is known as rolling resistance or rolling friction.

Let A be the point of application of N, and let a represent the horizontal distance between A and the vertical center line of the wheel. Referring to

- Fig. 7.16(b), the moment equation MA =0 yields Wa = FR cosφ, where φ is the angle between N and the vertical. In practice a << R, which allows us to approximate cosφ ≈ 1. Therefore, Wa = FR, or

a R

W = µrW (7.16)

F =

where µr = a/R is called the coefﬁcient of rolling resistance (unfortunately, the distance a also often is referred to as the coefﬁcient of rolling resistance). Note that µr is analogous to the coefﬁcient of kinetic friction µk. Generally, µr is considerably smaller than µk. Typical values of µr are 0.0002 to 0.0005 for railroad car wheels on steel rails, and 0.01 to 0.03 for car tires on paved roads.

|Sample Problem 7.17<br><br>An 80-lb shopping cart with 6-in. diameter wheels rolls down a ramp with constant speed. If the slope angle of the ramp is 1.5◦, what is the coefﬁcient of rolling resistance?<br><br>3 in.<br><br>φ = 1.5°<br><br>1.5°<br><br>a<br><br>N<br><br>W<br><br>Solution<br><br>Consider the FBD of one wheel of the cart shown in the ﬁgure. Since the speed of the wheel is constant, the wheel is in equilibrium. We also note that the wheel is a two-force body, so that the weight W acting on a wheel and the contact force N are collinear. From geometry, we get<br><br>a = 3sin1.5◦ = 0.07853 in.<br><br>Therefore, the coefﬁcient of rolling resistance is<br><br>µr =<br><br>a R =<br><br>0.07853 3 = 0.0262 Answer<br><br>|
|---|

![image 55](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile55.png>)

###### Problems

- 7.69 The collar bearing carries the axial load P =400 N. Assuming uniform P C

µs

40 mm 80 mm

Fig. P7.69

pressure between the collar and the horizontal surface, determine the couple C required to start the shaft turning. Use µs =0.15 for the coefﬁcient of static friction.

- 7.70 Solve Sample Problem 7.16 if the contact pressure under the polisher

F

2.8 ft

2ft

Fig. P7.71

varies parabolically from p0 at r = 0 to zero at r = R; that is, p = p0(1−r2/R2).

- 7.71 The 500-lb cable spool is placed on a frictionless spindle that has been driven into the ground. If the force required to start the spool rotating is F =110 lb, determine the coefﬁcient of friction between the ground and the spool. Neglect the diameter of the spindle compared to the diameter of the spool.
- 7.72 Determine the braking torque acting on the rotating disk when a force P = 200 N is applied to each brake pad. Assume that the brakes are (a) new; and (b) worn.

k = 0.92

Dimensions in mm

Brake pad

30°

P

µ

P

20

12

Brake pads

Fig. P7.72

- 7.73 The normal pressure acting on the disk of the sander is given by p = (4/3)+(r2/6), where p is the pressure in pounds per square inch (psi) and r represents the radial distance in inches. Determine the torque C required to operate the sander at constant speed if the kinetic coefﬁcient of friction for the surface being sanded is 0.86.

P

C

2psi

4psi

2 in.

p

r

8 in.

###### Fig. P7.73

300 N

7.74 The 20-kg stepped shaft is supported by bearings at A and B. The coefﬁ-

cients of kinetic friction are 0.15 at A and 0.06 at B. Assuming that all surfaces are new, determine the couple C that will rotate the shaft at constant speed.

A C

- 7.75 The single-plate clutch transmits the torque C from the input shaft on the left to the output shaft on the right. Compression springs between the clutch housing and the pressure plate provide the necessary pressure on the friction surface. The splines prevent the clutch plate from rotating relative to the output shaft. If

Ri = 4 in. and Ro = 9 in., determine the total force that must be applied to the pressure plate by the springs if the clutch is to transmit a torque of C = 56 lb·ft when it is new.

Friction surface

= 1.6

Clutch housing

Clutch plate

Pressure plate

Splines

C

Ro

Ri

C µs

| | | |
|---|---|---|
| | | |

| | |
|---|---|
| | |

a b

P

C

β

µs

Friction surface

Gear teeth

Thrust bearing Key

Radial bearing

Fig. P7.75, P7.76 Fig. P7.77

- 7.76 The clutch described in Prob. 7.75 is to transmit a torque of 120lb·ft when the total spring force exerted on the pressure plate is 75lb. If Ri = 4 in., calculate the minimum acceptable value for Ro. Assume that the clutch is new.

100 mm

300 mm

B

Fig. P7.74

∗7.77 The cone clutch transmits the torque C through a conical friction surface with cone angle β. The inner and outer radii of the friction surface are a and b, respectively. The left half of the clutch is keyed to the shaft, and the right half drives a machine (not shown) through a gear attached to its outer rim. Assuming uniform pressure on the friction surface, show that the maximum torque that can be transmitted by the clutch is

b3 − a3 b2 − a2

- 2µs P

- 3sinβ

C =

7.78 Determine the force F required to push the 3700-lb car at a constant speed on concrete pavement. The coefﬁcient of rolling resistance of the 11-in. radius tires on concrete is µr = 0.015.

###### F

3700 lb

+

+

11 in.

11 in.

###### Fig. P7.78

- 7.79 The coefﬁcient of rolling resistance between the 30-kg lawn roller and

the ground is µr = 0.1. (a) Determine the force P required to pull the roller at a constant speed. (b) What force P would be needed to push the roller at a constant speed?

150 mm 30°

P

30 kg

Fig. P7.79

- 7.80 The 120-lb concrete slab is placed on steel rollers. Determine the force P required to move the slab with a constant velocity. The coefﬁcients of rolling resistance are 0.05 between the slab and a roller and 0.03 between a roller and the ground.

| |120 lb|
|---|---|
| | |

P

4 in. 4 in.

++ +

Fig. P7.80

- 7.81 Calculate the horizontal force P required to push the 80-lb lawn mower at constant speed. The center of gravity of the mower is at G, and the coefﬁcients of rolling resistance are 0.1 for the front wheels and 0.15 for the rear wheels.

P

12 in. 10 in.

27 in.

G

10 in.

5 in.

A B

###### Fig. P7.81

![image 56](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile56.png>)

###### Review of Equations

###### Friction force

Static case: F ≤ µsN Dynamic case: F = µkN

µs = coefﬁcient of static friction µk = coefﬁcient of kinetic friction N = normal force

###### Angle of friction

Static case: φs = tan−1 µs Dynamic case: φk = tan−1 µk

###### Square-threaded screws

p = 2πr tanθ

p = pitch of the screw θ = lead angle (helix angle) r = mean radius of threads

(C0)up = Wr tan(φs + θ) (C0)down = Wr tan(φs − θ) C0 = smallest couple required to raise/lower weight W

###### Belt friction

T2 = T1eµsθ (impending slipping) T2 = T1eµkθ (slipping) θ = contact angle between the belt and the peg (in rads.)

###### Disk friction

Ro3 − Ri3 Ro2 − Ri2

- 2µP

- 3

C =

(new surfaces)

µP 2

C =

(Ro + Ri) (worn surfaces)

C = transmitted torque µ = µs (impending rotation) or µ = µk (rotating) P = axial force

![image 57](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile57.png>)

###### Review Problems

- 7.82 Determine the smallest force P that will move the wedge to the right if the coefﬁcient of static friction is 0.5 at all contact surfaces. The uniform cylinder weighs W, and the weight of the wedge may be neglected.

P

15°

W

R

Fig. P7.82

- 7.83 The homogeneous bar AB of weight W and length L is lifted by the force P that is perpendicular to the bar. Determine the smallest coefﬁcient of static friction at A that would enable the bar to reach the position β = 30◦.

L

β

B

P

A

Fig. P7.83

- 7.84 Find the smallest angle β for which the uniform crate can be tipped about

5 ft

β

5 ft

200 lb

µS = 0.2

P

A

Fig. P7.84

corner A. Also compute the corresponding value of P.

- 7.85 The belt is placed between two rollers, which are free to rotate about A and B. Determine the smallest coefﬁcient of static friction between the belt and the rollers for which the device is self-locking; that is, the belt cannot be pulled down for any value of P.

Belt

1.5R

0.5R

R

A

35°

B

P

###### Fig. P7.85

- 7.86 Determine the largest angle β for which the uniform box can be in equilibrium.

1.2m

0.5m

s = 0.45

β

µ

Fig. P7.86

- 7.87 Can the uniform bar of weight W remain at rest in the position shown?

60°

µ

30°

s = 0.6

Fig. P7.87

- 7.88 The panel of weight W with its center of gravity at G is placed between vertical guides and released. Determine the largest height h for which the panel will not slide down due to binding at corners A and B. The coefﬁcient of static friction between the panel and the guides is 0.5.

B G

A

h

6 m 2 m

Fig. P7.88

- 7.89 The woman is trying to move the crate of weight W by pulling on the rope at the angle θ to the horizontal. Find the smallest possible tension that would cause the crate to slide and the corresponding angle θ.

| | |θ|
|---|---|---|
| | | |
| | | |
| | | |

µs

###### Fig. P7.89

- 7.90 The screw of the clamp has a square thread of pitch 0.15in. and a mean diameter of 0.5in. The coefﬁcient of static friction between the threads is 0.5.

Determine (a) the torque C0 that must be applied to the screw in order to produce a 30-lb clamping force at A; and (b) the torque required to loosen the clamp.

A

B C

6 in. 4 in.

C0

Fig. P7.90

- 7.91 Find the largest clockwise couple C that can be applied to cylinder A without causing motion. The coefﬁcient of static friction is 0.2 at all three contact surfaces.

0.3 m

40 kg

C

A B

60 kg

Fig. P7.91

- 7.92 The test specimen AB is placed in the grip of a tension-testing machine and secured with a wedge. The coefﬁcient of static friction at both surfaces of

the specimen is µs. If the wedge angle is θ = 18◦, determine the smallest µs for which the grip is self-locking (no slipping takes place regardless of the magnitude of the force P). Neglect the weight of the wedge.

A θ B P

###### Fig. P7.92

- 7.93 Determine the smallest force P necessary to hold the homogeneous 12-kg block in the position shown.

|0.1 m 60°<br><br>| |
|---|---|
|12 kg| |
|0.2 m| |

P

µs= 0.24

0.25m

Fig. P7.93

- 7.94 The uniform bars AB and BC are connected with a pin at B and placed on a horizontal surface. The coefﬁcient of static friction between the bars and the surface is µs = 0.6. Can the bars be in equilibrium in the position shown?

###### B

10ft 20ft

8ft

15lb

6 ft

A C

###### Fig. P7.94

# 8

### Centroids and Distributed Loads

![image 58](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile58.png>)

The water pressure on the upstream side of an arch dam results in very large forces that must be resisted by the abutments. This chapter shows how to calculate the force resulting from hydraulic pressure acting on curved surfaces, such as the upstream face of the dam shown. Michael Busselle/Stone/Getty Images

###### 8.1 Introduction

In this chapter we investigate centroids, centers of gravity, and centers of mass. Centroids were ﬁrst discussed in Art. 3.6 in conjunction with distributed normal loads. The more rigorous treatment of centroids presented here will enable us to analyze normal loads that are distributed in a complex manner. We also discuss the theorems of Pappus-Guldinus, which utilize centroids for calculating areas and volumes of revolution.

y

x

Plane region

###### 8.2 Centroids of Plane Areas and Curves

###### a. Deﬁnitions

dA x C

Consider the plane region shown in Fig. 8.1. Let dA be a differential (inﬁnites-

imal) area element of , located at (x, y). There are certain properties of that occur frequently in various branches of the physical sciences. One of these is, of course, the area

y

y

x

A = dA (8.1)

Fig. 8.1

###### 401

Other important properties are the ﬁrst moments of the area about the x- and y-axes, deﬁned as

###### Qx = y dA Qy = x dA (8.2)

and the second moments of the area, also called the moments of inertia, which are treated separately in Chapter 9.

The importance of the centroid of the area stems from its close association with the ﬁrst moments of areas. The centroid C of a plane area is deﬁned as the point that has the coordinates (see Fig. 8.1)

x dA dA y¯ =

y dA dA

Qy A =

Qx A =

(8.3)

x¯ =

It can be seen that if A and (x¯, y¯) of an area are known, its ﬁrst moments can be computed by Qx = Ay¯ and Qy = Ax¯, thereby avoiding the evaluation of the integrals in Eqs. (8.2).

The centroid is sometimes referred to as the geometric center of the region. The centroid is not to be confused with the mass center, which is a property of the mass distribution within the region. Centroids and mass centers coincide only if the distribution of mass is uniform—that is, if the body is homogeneous.

The following characteristics of centroids and ﬁrst moments of areas should be noted.

- • The dimension of Qx and Qy is [L3]; hence the units are mm3, in.3, and so on.
- • Qx and Qy may be positive, negative, or zero, depending on the location of the coordinate axes relative to the centroid of the region. If the x-axis passes

through the centroid, then Qx = 0. Similarly, Qy = 0 if the centroid lies on the y-axis.

- • If the region is symmetric, then its centroid is located on the axis of symmetry. This can be demonstrated by considering the region in Fig. 8.2, which is symmetric about the y-axis. Clearly, the integral x dA over the left half (where x is negative) cancels the integral x dA over the right half (where x is positive). Consequently, Qy = 0, and it follows that x¯ = 0.

y

dA dA

x

– x x

###### Fig. 8.2

y

x

Plane curve

x C

ds

y

y

x

###### Fig. 8.3

The deﬁnitions of centroids and ﬁrst moments of plane curves are analogous to those of plane areas. Letting ds be the differential length of the plane curve in Fig. 8.3, the length of the curve is

###### L = ds (8.4)

and the ﬁrst moments of the curve about the coordinate axes are deﬁned as

###### Qx = y ds Qy = x ds (8.5)

The dimension of the ﬁrst moment of a curve is [L3]. The coordinates of the centroid of the curve are, by deﬁnition,

x ds ds y¯ =

y ds ds

Qy L =

Qx L =

(8.6)

x¯ =

###### b. Integration techniques

The details of the integration for plane areas in Eqs. (8.1) and (8.2) depend upon the choice of the area element dA. There are two basic choices for dA: the double differential elements shown in Figs. 8.4(a) and (b); and the single differential elements in Figs. 8.4(c)–(e). In the latter case, the coordinates x and y of the differential element must be interpreted as the coordinates of the centroid of the element. These coordinates, denoted by x¯el and y¯el, are shown in Figs. 8.4(c)–(e).

The expressions for dA, x¯el, and y¯el also depend upon the choice of the coordinate system. Figure 8.4 illustrates elements using both rectangular and polar coordinates. The most convenient coordinate system for a given problem is determined primarily by the shape of the region . Obviously, rectangular regions are best handled by rectangular coordinates, whereas polar coordinates should be chosen for circular regions.

dA = (x2– x1) dy

dA = r dr dθ

xel = 12(x1+ x2)

dA = dx dy

y

y

y

x = r cos θ

x2 xel

x

dx

dr

dy

x1

dy

dA

dA

r dθ

θ=sinyr

dA

y

y

θ

x

x

x

(c)

(b)

(a)

dA = (y2– y1) dx

yel = 12(y1+ y2)

y

y

x dx

xel

θ

dA = 12r2d rel = 23r xel = 23 r cos yel = 23 r sin

dA

θ θ

θ

d

y2 y1

rel

r

dA

yel

yel

θ

x

x

(e)

(d)

###### Fig. 8.4

The properties of curves always involve a single integration, carried out along the length of the curve. The expressions for the differential length ds for rectangular and polar coordinates are shown in Fig. 8.5.

In cases where it is not possible to evaluate the integrals analytically, numerical integration must be used. Two such methods, the trapezoidal rule

y

y

dr

ds

ds

r dθ

dy

dx

θ

x

x

ds = (dx)2+ (dy)2

θ

(dr)2+ (rd )2

ds =

###### ( )d

= = ( )dy

( )dx 1+ dy

dy 2

dx 2

r2+ ddr 2

θ θ

=

1+

dx

(a)

(b)

Fig. 8.5

and Simpson’s rule, are discussed in Appendix A. Numerical integration is particularly useful for computing the centroids of curves, because even simple shapes—for example, parabolas—result in integrals that are difﬁcult to evaluate analytically.

###### c. Composite shapes

Consider the plane region shown in Fig. 8.6 that has been divided into subre- y

gions 1, 2, 3, . . . (only three subregions are shown). The centroids of the areas of the subregions are labeled C1, C2, C3, . . . , with coordinates (x¯1, y¯1), (x¯2, y¯2), (x¯3, y¯3), . . . , respectively. Because the integral of a sum is equal to the sum of the integrals (a well-known property of deﬁnite integrals), the area A of the composite region is

2

1

C2

C1

y2

C3

y1

y3

###### A = dA =

###### dA +

###### dA +

dA + ··· =

Ai

i

x

1

2

3

x1

3

where A1, A2, A3, . . . are the areas of the subregions. Similarly, the ﬁrst moment of the area of about the y-axis is

x3 x2

###### Qy = x dA =

###### x dA +

###### x dA +

x dA + ··· =

(Qy)i

Fig. 8.6

i

1

2

3

where (Qy)i refers to the ﬁrst moment of the area of i about the y-axis. A similar analysis may be used to determine Qx, the ﬁrst moment of the area of about the x-axis.

Therefore, the centroidal coordinates of the area of can be written as

(Qy)i i Ai y¯ =

(Qx)i i Ai

Qy A = i

Qx A = i

(8.7)

x¯ =

Determining the centroid of an area by this technique is called the method of composite areas. Substituting (Qy)i = Aix¯i and (Qx)i = Ai y¯i, the preceding equations become

Aix¯i i Ai y¯ =

Ai y¯i i Ai

Qy A = i

Qx A = i

(8.8)

x¯ =

Caution The centroid of the composite area is not equal to the sum of the centroids of its subregions; that is, x¯  = i(Aix¯i/Ai) and y¯  = i(Ai y¯i/Ai).

The method of composite curves is analogous to the method of composite areas. The centroidal coordinates of the curve of length L that has been subdivided into the segments 1, 2, 3, . . . are given by

Lix¯i i Li y¯ =

Li y¯i i Li

Qy L = i

Qx L = i

(8.9)

x¯ =

where Li is the length of the segment i with its centroid located at (x¯i, y¯i).

You will discover that tables that list the properties of common plane ﬁgures, such as Tables 8.1 and 8.2, are very useful when applying the methods of composite areas and composite lines.

|x =1(a+b) 3<br><br>y =1h<br><br>3<br><br>A =1bh<br><br>2<br><br>y<br><br><br>x<br><br>h<br><br>a<br><br>b 2<br><br>x<br><br>y<br><br>C<br><br>b 2<br><br>Triangle|y<br><br>x<br><br>h<br><br>x<br><br>y<br><br>C<br><br>b<br><br>y = h x<br><br><br>(b)<br><br>2<br><br>x =3b<br><br>4<br><br>A =1bh<br><br>3<br><br>y = 3 h<br><br>10<br><br>Half parabolic complement|
|---|---|
|y<br><br>x<br><br>R<br><br>R<br><br>x<br><br>y<br><br>C<br><br>x = 4 R<br><br>3π<br><br>y = 4 R<br><br>3π<br><br>A =π R2 4<br><br>Quarter circle|y<br><br>x<br><br>h<br><br>x<br><br>y<br><br>C<br><br>b<br><br>y = h<br><br><br>x<br><br>(b)<br><br>2<br><br>x = 3 b<br><br>8<br><br>y = 3 h<br><br>5<br><br>A = 2 bh<br><br>3<br><br>Half parabola|
|y<br><br>x<br><br>b<br><br>a<br><br>x<br><br>y<br><br>C<br><br>x2 a2<br><br>y2 b2<br><br>+ = 1<br><br>x = 4 a<br><br>3π<br><br>y = 4 b<br><br>3π<br><br>A = π ab<br><br>4<br><br>Quarter ellipse|y<br><br>x<br><br>R<br><br>C<br><br>x<br><br>α<br><br>α<br><br>x = 2R sin α<br><br>3α<br><br>A = αR2<br><br>Circular sector|

|y<br><br>x<br><br>R<br><br>x C<br><br>y 45°<br><br>R<br><br>x = 2R<br><br>π y = 2R<br><br>π L = R<br><br>2<br><br>π<br><br>Quarter circular arc|
|---|
|y<br><br>x<br><br>R<br><br>C<br><br>x<br><br>α α<br><br>x = R sin α L = 2αR<br><br>1 α<br><br>Circular arc<br><br>|

###### Table 8.1 Centroids of Plane Areas Table 8.2 Centroids of Plane Curves

|Sample Problem 8.1<br><br>Determine the coordinates of the centroid of the area that lies between the straight line x =2y/3 and the parabola x2 =4y, where x and y are measured in inches—see Fig. (a). Use the following methods: (1) double integration; (2) single<br><br>6 in.<br><br>9 in.<br><br>x = 2 3<br><br>y<br><br>x2 = 4y<br><br>x<br><br>y<br><br><br>(a)<br><br>6 in.<br><br>9 in.<br><br>x<br><br>y<br><br>(b)<br><br>dy<br><br>dA = dxdy<br><br>y<br><br>dx x<br><br>integration using a horizontal differential area element; and (3) single integration using a vertical differential area element.<br><br>Solution<br><br>Part 1 Double Integration<br><br>The double differential area element is shown in Fig. (b). Note that dA can be written as dx dy, or dy dx, depending on whether you choose to integrate on x or y ﬁrst. Choosing to integrate over y ﬁrst, the area A of the region is<br><br>A = dA =<br><br>6<br><br>0<br><br>3x/2<br><br>x2/4<br><br>dy dx =<br><br>6<br><br>0<br><br>3x 2 −<br><br>x2 4<br><br>dx<br><br>=<br><br>3x2 4 −<br><br>x3 12<br><br>6<br><br>0<br><br>= 9 in.2<br><br>The ﬁrst moment of the area about the y-axis is<br><br>Qy = x dA =<br><br>6<br><br>0<br><br>3x/2<br><br>x2/4<br><br>x dy dx =<br><br>6<br><br>0<br><br>3x 2 −<br><br>x2 4<br><br>x dx<br><br>=<br><br>3x3 6 −<br><br>x4 16<br><br>6<br><br>0<br><br>= 27 in.3<br><br>The ﬁrst moment of the area about the x-axis is<br><br>Qx = y dA =<br><br>6<br><br>0<br><br>3x/2<br><br>x2/4<br><br>y dy dx =<br><br>6<br><br>0<br>1<br><br>2<br><br><br>9x2 4 −<br><br>x4 16<br><br>dx<br><br>=<br><br>1<br><br>2<br><br><br>9x3 12 −<br><br>x5 80<br><br>6<br><br>0<br><br>= 32.4 in.3<br><br>Therefore, the coordinates of the centroid of the area are<br><br>x¯ =<br><br>Qy A =<br><br>27 9 = 3 in. Answer<br><br>y¯ =<br><br><br>Qx A =<br><br>32.4 9 = 3.6 in. Answer<br><br>|
|---|

|If you choose to integrate over x ﬁrst, the respective integrals are as follows:<br><br>A = dA =<br><br>9<br><br>0<br><br>2√y<br><br>2y/3<br><br>dx dy<br><br>Qy = x dA =<br><br>9<br><br>0<br><br>2√y<br><br>2y/3<br><br>x dx dy<br><br>Qx = y dA =<br><br>9<br><br>0<br><br>2√y<br><br>2y/3<br><br>y dx dy<br><br>You may wish to verify that the evaluation of these integrals yields the same centroidal coordinates as determined previously.<br><br>Part 2 Single Integration: Horizontal Differential Area Element<br><br>The horizontal differential area element is shown in Fig. (c), together with the<br><br>6 in.<br><br>9 in.<br><br>x<br><br>y<br><br>(c)<br><br>dy<br><br>dA=(2 y– 2<br><br>3<br><br>y)dy<br><br>y<br><br>2 y y<br><br>2<br>3<br><br><br>xel = 1<br><br>2<br><br>(2 y+2<br><br>3<br><br>y)<br><br>expressions for dA and x¯el. For the area we have<br><br>A = dA =<br><br>9<br><br>0<br><br>2√y −<br><br>2y<br><br>3<br><br><br>dy =<br><br>4y3/2 3 −<br><br>y2 3<br><br>9<br><br>0<br><br>= 9 in.2<br><br>Using dQy = x¯el dA we obtain<br><br>dQy =<br><br>1<br><br>2<br><br><br>2√y +<br><br>2y<br><br>3<br><br><br>2√y −<br><br>2y<br><br>3<br><br><br>dy = 2y −<br><br>2y2 9<br><br>dy<br><br>The ﬁrst moment of the area about the y-axis becomes<br><br>Qy =<br><br>9<br><br>0<br><br>2y −<br><br>2y2 9<br><br>dy = y2 −<br><br>2y3 27<br><br>9<br><br>0<br><br>= 27 in.3<br><br>Similarly, dQx = y dA gives<br><br>dQx = y 2√y −<br><br>2y<br><br>3<br><br><br>dy = 2y3/2 −<br><br>2y2<br><br>3<br><br><br>dy<br><br>The ﬁrst moment about the x-axis is<br><br>Qx =<br><br>9<br><br>0<br><br>2y3/2 −<br><br>2y2<br><br>3<br><br><br>dy =<br><br>4<br><br>5<br><br><br>y5/2 −<br><br>2y3 9<br><br>9<br><br>0<br><br>= 32.4 in.3<br><br>Note that A, Qx, and Qy are identical to the values computed in Part 1. Therefore, the coordinates of the centroid of the area are also the same.|
|---|

|Part 3 Single Integration: Vertical Differential Area Element<br><br>The vertical differential area element is shown in Fig. (d), which also gives the expressions for dA and y¯el. The area of the region is<br><br>A = dA =<br><br>6<br><br>0<br><br>3x 2 −<br><br>x2 4<br><br>dx =<br><br>3x2 4 −<br><br>x3 12<br><br>6<br><br>0<br><br>= 9 in.2<br><br>Using the information in Fig. (d), we obtain<br><br>dQy = x dA = x<br><br>3x 2 −<br><br>x2 4<br><br>dx<br><br>Therefore, the ﬁrst moment about the y-axis is<br><br>Qy = dQy =<br><br>6<br><br>0<br><br>3x2 2 −<br><br>x3 4<br><br>dx =<br><br>x3<br><br>2 −<br><br>x4 16<br><br>6<br><br>0<br><br>= 27 in.3<br><br>For dQx = y¯el dA, we get<br><br>dQx =<br><br>1<br><br>2<br><br><br>3x 2 +<br><br>x2 4<br><br>3x 2 −<br><br>x2 4<br><br>dx =<br><br>1<br><br>2<br><br><br>9x2 4 −<br><br>x4 16<br><br>dx<br><br>Integration of this expression yields<br><br>Qx = dQx =<br><br>6<br><br>0<br>1<br><br>2<br><br><br>9x2 4 −<br><br>x4 16<br><br>dx =<br><br>1<br><br>2<br><br><br>9x3 12 −<br><br>x5 80<br><br>6<br><br>0<br><br>= 32.4 in.3<br><br>Again, the same values of A, Qx, and Qy have been obtained as in Parts 1 and 2. Thus x¯ and y¯ would also be identical.<br><br>6 in.<br><br>9 in.<br><br>x<br><br>y<br><br>(d)<br><br>dx x<br><br>x2 4<br><br>3 2<br><br>x<br><br>dA = 3 2<br><br>x – x2 4<br><br>dx<br><br>yel = 1<br><br>2<br><br>3 2<br><br>x + x2 4<br><br>dx<br><br>Sample Problem 8.2<br><br>Using the method of composite areas, determine the location of the centroid of the shaded area shown in Fig. (a).<br><br>300<br><br>200 200<br><br>400<br><br>300<br><br>x<br><br>y<br><br>Dimensions in mm (a)<br><br>400<br><br>Solution<br><br>The area can be viewed as a rectangle, from which a semicircle and a triangle have been removed. The areas and centroidal coordinates for each of these shapes can be determined using Table 8.1. The results are shown in Figs. (b)–(d).|
|---|

|700 350<br><br>x<br><br>y<br><br>(b)<br><br>1<br><br>C1<br><br>Area = (700)(800) = 560 × 103 mm2 +<br><br>400 400<br><br>300<br><br>x<br><br>y<br><br>(c)<br><br>400<br><br>= 127.3<br><br>4(300) 3π<br><br>Area = (300)2 = 141.4 × 103 mm2 –<br><br>C2<br><br>2<br><br>2<br><br>400 272.7<br><br>π<br><br>400<br><br>300<br><br>x<br><br>y<br><br>(d)<br><br>566.7<br><br>200 3<br><br>= 66.7<br><br>400 3<br><br>= 133.3<br><br>Area = 1(200)(400) = 40 × 103 mm2 – 2<br><br>3<br><br>C3<br><br>333.3<br><br>200 200<br><br>When applying the method of composite areas, it is convenient to tabulate the data in the following manner.<br><br>Shape Area A x¯ Ax¯ y¯ Ay¯<br><br>(mm2) (mm) (mm3) (mm) (mm3)<br><br>1 (Rectangle) +560.0 × 103 0 0 +350 196.0 × 106<br>2 (Semicircle) −141.4 × 103 −272.7 +38.56 × 106 +400 −56.56 × 106<br>3 (Triangle) −40.0 × 103 +333.3 −13.33 × 106 +566.7 −22.67 × 106<br><br><br>+378.6 × 103 ··· +25.23 × 106 ··· +116.77 × 106<br><br>Be certain that you understand each of the entries in this table, paying attention to signs. For the rectangle, A is positive, Ax¯ is zero, and Ay¯ is positive. The area of the semicircle is assigned a negative value because it must be subtracted from the area of the rectangle. Because x¯ for the semicircle is also negative, its Ax¯ is positive; however, y¯ is positive, so that its Ay¯ is negative. The area of the triangle is also assigned a negative value, but x¯ and y¯ are both positive, resulting in negative values for both Ax¯ and Ay¯.<br><br>According to the tabulated results, the coordinates of the centroid of the composite area are<br><br>x¯ =<br><br>Ax¯ A =<br><br>+25.23 × 106<br><br>+378.6 × 103 = 66.6 mm Answer<br><br>y¯ =<br><br><br>Ay¯ A =<br><br>+116.77 × 106<br><br>+378.6 × 103 = 308 mm Answer<br><br>Because x¯ and y¯ are both positive, the centroid of the composite area lies in the ﬁrst quadrant of the coordinate plane.|
|---|

|Sample Problem 8.3<br><br>Using the method of composite curves, determine the centroidal coordinates of<br><br>R<br><br>=6in.<br><br>| | |
|---|---|
|2 in.<br><br>3|1<br><br>|
<br><br>5 in.<br><br>8 in.<br><br>2<br><br>y<br><br>x<br><br>(a)<br><br>the line in Fig. (a) that consists of the circular arc 1, and the straight lines 2 and 3.<br><br>Solution<br><br>The length and centroidal coordinates of the circular arc can be calculated using Table 8.2; the results are shown in Fig. (b). Figure (c) displays the properties of the two straight line segments; the centroidal coordinates are at the midpoints of the segments.<br><br>2 in.<br><br>1<br><br>y<br><br>x<br><br>α α<br><br>α<br><br>(b)<br><br>2.595 in.<br><br>C1<br><br>R sin = 4.595 in. L1 = 2 R = 14.772 in.<br><br>2 6<br><br>R<br><br>= 6 in.<br><br>α = cos–1 = 1.231 rad<br><br>5 in.<br><br>8 in.<br><br>2<br><br>3<br><br>y<br><br>x<br><br>(c)<br><br>4 in.<br><br>C2<br><br>C3<br><br>L2 = (8)2 + (5.657)2 = 9.798 in. L3 = 5 in.<br><br>Rsinα = 5.657 in. 2.828 in.<br><br>2.5 in.<br><br>It is convenient to organize the analysis in tabular form, as follows:<br><br>Segment Length L x¯ Lx¯ y¯ L y¯ (in.) (in.) (in.2) (in.) (in.2)<br><br>1 14.772 +2.595 +38.33 0 0<br>2 9.798 −4.0 −39.19 +2.828 +27.71<br>3 5.0 −8.0 −40.0 −2.5 −12.50 29.570 ··· −40.86 ··· +15.21<br><br><br>Therefore, the coordinates of the centroid of the composite curve are<br><br>x¯ =<br><br>Lx¯ L =<br><br>−40.86 29.570 = −1.382 in. Answer<br><br>y¯ =<br><br><br>Ly¯ L =<br><br>+15.21 29.570 = +0.514 in. Answer<br><br>Because x¯ is negative and y¯ is positive, the centroid of the composite curve lies in the third quadrant of the coordinate plane.|
|---|

|Sample Problem 8.4<br><br>Using numerical integration (Simpson’s rule), determine the centroidal coordinates of the sine curve shown in the ﬁgure. Use six panels, each of width<br><br>x = 0.5 in.<br><br>2<br><br>x (in.)<br><br>∆x = 0.5<br><br>y (in.)<br><br>y=2 sin<br><br>x 6<br><br>0<br><br>0 0.5 1.0 1.5 2.0 2.5 3.0<br><br>y2<br><br>y3<br><br>π<br><br>y4<br><br>y5 y6 y7<br><br>Solution<br><br>With six panels, Simpson’s rule is (see Appendix A)<br><br>b<br><br>a<br><br>f (x) dx = ( f1 + 4 f2 + 2 f3 + 4 f4 + 2 f5 + 4 f6 + f7)<br><br>x 3<br><br>(a)<br><br>The integrals to be evaluated are given by Eqs. (8.4) and (8.5):<br><br>L = ds Qy = x ds Qx = y ds (b)<br><br>Substituting ds = (ds/dx)dx, the integrals in Eqs. (b) become<br><br>L =<br><br>ds dx<br><br>dx Qy = x<br><br>ds dx<br><br>dx Qx = y<br><br>ds dx<br><br>dx (c)<br><br>For our problem, the integrals in Eqs. (c) are to be computed with Simpson’s rule using n =6 and x =0.5 in. The values of yi and (ds/dx)i can be obtained from the following sequence of computations (see Fig. 8.5).<br><br>yi = 2sin<br><br>πxi 6<br><br>dy dx i =<br><br>π 3<br><br>cos<br><br>πxi 6<br><br>ds dx i = 1 +<br><br>dy dx<br><br>2<br><br>i|
|---|

|The resulting numerical computations are contained in the following table.<br><br>i x y dy/dx ds/dx x(ds/dx) y(ds/dx) (in.) (in.) (in.) (in.)<br><br>1 0.0 0.0000 1.0472 1.4480 0.0000 0.0000<br>2 0.5 0.5176 1.0115 1.4224 0.7112 0.7363<br>3 1.0 1.0000 0.9069 1.3500 1.3500 1.3500<br>4 1.5 1.4142 0.7405 1.2443 1.8665 1.7597<br>5 2.0 1.7321 0.5236 1.1288 2.2576 1.9551<br>6 2.5 1.9319 0.2710 1.0361 2.5902 2.0016<br>7 3.0 2.0000 0.0000 1.0000 3.0000 2.0000<br><br><br>Substituting the values from this table into Eq. (a) yields<br><br>L ≈<br><br>0.5 3 [1(1.4480) + 4(1.4224) + 2(1.3500) + 4(1.2443) + 2(1.1288)<br><br>+ 4(1.0361) + 1(1.0000)] = 3.7028 in.<br><br>Qy ≈<br><br>0.5 3 [1(0) + 4(0.7112) + 2(1.3500) + 4(1.8665) + 2(2.2576)<br><br>+ 4(2.5902) + 1(3.0000)] = 5.1478 in.2<br><br><br>Qx ≈<br><br>0.5 3 [1(0) + 4(0.7363) + 2(1.3500) + 4(1.7597) + 2(1.9551)<br><br>+ 4(2.0016) + 1(2.0000)] = 4.4334 in.2 from which we obtain<br><br>x¯ =<br><br>Qy L =<br><br>5.1478 3.7028 = 1.390 in. Answer<br><br>y¯ =<br><br><br>Qx L =<br><br>4.4334 3.7028 = 1.197 in. Answer<br><br>|
|---|

![image 59](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile59.png>)

###### Problems

8.1–8.6 Use integration to determine the coordinates of the centroid of the plane region shown.

y

y

y

y2=30x

60 mm

h

y = 14 x3/2

y=0.5x

2 ft

x

x

x

120 mm

4 ft

b

###### Fig. P8.1 Fig. P8.2 Fig. P8.3

y

y

y = x1/2

50 mm 50 mm

y

9x = 4y2

0.6 m

100 mm

3 in.

1.5 in.

- x
- y=x2/25

y = 259 x3/2

x

x

0.36 m

1 in. 3 in.

###### Fig. P8.4 Fig. P8.5 Fig. P8.6

- 8.7 (a) Using integration, locate the centroid of the area under the nth order parabola in terms of b, h, and n (n is a positive integer). (b) Check the result of part (a) with Table 8.1 for the case n = 2.
- 8.8 Use integration to compute the coordinates of the centroid of the triangle. Check your results with Table 8.1.
- 8.9 Determine the y-coordinate of the centroid of the semicircular segment, given that a = 18 in. and α = 45◦.

y

y

y

11 in.

y = h(x/b)n

a

h

α

x

x

7 in.

5 in.

b

x

###### Fig. P8.7 Fig. P8.8 Fig. P8.9

- 8.10 (a) Use integration to locate the centroid of the shaded region in terms of

x

y

R t

Fig. P8.10

R and t. (b) Show that when t →0 the result of part (a) agrees with that given in Table 8.2 for a quarter circular arc.

- 8.11 Locate the centroid of the parabola by integration.

y

x

y=x2

1.0 ft 1.0 ft

1.0 ft 1.0 ft

Fig. P8.11

- 8.12 Use integration to locate the centroid of the quarter circular arc shown in Table 8.2. ∗8.13 The parametric equations of the plane curve known as a cycloid are

y

x =a(θ − sinθ) and y =a(1 − cosθ). Use integration to ﬁnd the coordinates of the centroid of the cycloid obtained by varying θ from 0 to 2π rad.

2a

8.14–8.21 Use the method of composite areas to calculate the centroidal

x

0 πa 2πa

coordinates of the plane regions shown.

Fig. P8.13

|in.|5|
|---|---|
|in.| |

in.

3

- 3

4 in.

y

x

Dimensions in mm

50

15

30

40

y

x O

Fig. P8.14 Fig. P8.15

3 in.

- 4.8in.

y

20

7 in.

2 in.

y

80

20

y

8 in.

x

2 in.

20

x

60

2 in.

x

12 in.

Dimensions in mm

###### Fig. P8.16 Fig. P8.17

Fig. P8.18

y

y

80

3 in.

6 in.

30

2 in.

60

y

1 in.

90

7 in.

20

60 mm 80 mm

30

2 in.

x

x

30° 30°

7 in.

Dimensions in mm

x

###### Fig. P8.19 Fig. P8.20 Fig. P8.21

- 8.22 The plane region is bounded by a semicircle of radius R and a parabola of height h. Determine the relationship between R and h for which the centroid of the region is at C. Use the method of composite areas.

y

x

Parabola

R

C

h

Fig. P8.22

- 8.23 The centroid of the plane region shown is at C. Use the method of

y

composite areas to determine the radius R of the semicircular cutout. 8.24 Compute the centroidal coordinates of the L-shaped region in terms of b and t using the method of composite areas.

|C|8in.|
|---|---|
| |R<br><br>|

x

y

t

8 in.

Fig. P8.23

b

t

x

b

###### Fig. P8.24

- 8.25 By the method of composite areas, derive the expression for the centroidal x-coordinate of the circular segment in terms of R and α.

x

α α

y

R

h

4 ft

x

y

1 ft 1 ft 1 ft 1 ft

Fig. P8.25 Fig. P8.26

- 8.26 Using the method of composite areas, ﬁnd the dimension h that maxi-

2 m

R

C

x

y

Fig. P8.27

mizes the centroidal coordinate y¯ of the plane region shown. Also, compute the corresponding value of y¯.

- 8.27 Given that the centroid of the plane region is at C, ﬁnd the radius R. Use the method of composite areas.

8.28–8.33 Using the method of composite curves, locate the centroids of the plane curves shown.

y

y

| |30mm|
|---|---|
| |60|

2 in.

mm

3.5 in.

x

x

###### Fig. P8.28 Fig. P8.29

y

4ft

x

3 ft

###### Fig. P8.30

y

y

y

|42mm| |
|---|---|
| | |

300 mm

3 in.

| |4 in.|
|---|---|
|5 in.| |

x

125 mm

x

400 mm

x

60 mm

###### Fig. P8.31 Fig. P8.32 Fig. P8.33

8.34 Determine the ratio a/b for which the centroid of the composite curve will

y

be located at point O.

b b

- 8.35 Use numerical integration to locate the centroid of the symmetric plane region.

20

77 60

46 35

27

22 20

x

y

Dimensions in mm

y

x

8.5in.

8.0in.

7.2in.

5.4in.

2 in.

Fig. P8.35 Fig. P8.36

- 8.36 Determine the centroidal coordinates of the plane region by numerical integration.
- 8.37 Compute the y-coordinate of the centroid of the parabola shown, the equation of which is y = 40(1− x2/3600), where x and y are in inches. Use numerical integration with x = 15 in.

a

O x

a

Fig. P8.34

y

15 in.

40in.

x

60 in. 60 in.

###### Fig. P8.37

- 8.38 The equation of the catenary shown is y = 100cosh(x/100) where x and y are measured in feet (the catenary is the shape of a cable suspended between two points). Locate the y-coordinate of the centroid of the catenary by numerical integration using x = 25 ft.

y

25 ft

154.3ft

154.3ft

100ft

x 100 ft 100 ft

###### Fig. P8.38

z

8.3 Centroids of Curved Surfaces, Volumes, and

Space Curves

The centroids of curved surfaces, volumes, and space curves are deﬁned by expressions that are analogous to those used for plane regions. The only difference is that three coordinates, instead of two, are required to locate the centroids for three-dimensional shapes. The following table lists the expressions that deﬁne

- y y x

z

dA

Region

(a) z

x

- y y x

z

(b)

Region dV

z

x

- y y x

x

the centroidal coordinates for various three-dimensional shapes.

Curved Surface Occupying a Region

Volume Occupying a Region

Space Curve

Fig. 8.7(a) Fig. 8.7(b) Fig. 8.7(c) Area A = dA Volume V = dV Length L = ds

- x¯ =

x dA A x¯ =

x dV V x¯ =

x ds L

- y¯ =

y dA A y¯ =

y dV V y¯ =

y ds L

(8.10)

- z¯ =

z dA A z¯ =

z dV V z¯ =

z ds L

Space curve ds

z

The term xdA is sometimes labeled Qyz and is referred to as the ﬁrst moment of the area relative to the yz-plane. Similarly, Qxz = ydA and Qxy = zdA are called the ﬁrst moments of the area relative to the xz- and xy-planes, respectively. Extensions of this notation and terminology to volumes and space curves are obvious.

(c)

Fig. 8.7

The deﬁnitions in Eqs. (8.10) assume that the differential element (dA, dV, or ds) is located at the point that has coordinates x, y, and z. For other choices of elements, such as those occurring in single or double integration, it may be necessary to replace x, y, or z in Eqs. (8.10) with the centroidal coordinates of the element: x¯el, y¯el, z¯el. Because this integration procedure is similar to that described in Art. 8.2, it is not repeated here.

Symmetry of a body can play an important role in the determination of its centroid, as explained in the following:

- • If a volume has a plane of symmetry, its centroid lies in that plane. (The analogous statement for plane areas has been proven in Art. 8.2; the proof for volumes is essentially the same.)
- • If a volume has two planes of symmetry that intersect along a line, its centroid lies on that line. (The proof of this statement follows directly from the preceding symmetry argument.)

This symmetry argument is useful when determining the centroids of volumes of revolution. For example, consider the volume shown in Fig. 8.8 that

z

is generated by rotating a plane area about the y-axis. Because any plane that contains the y-axis is a plane of symmetry, the centroid C of the volume must lie on the y-axis; that is, x¯ = 0 and z¯ = 0.

Generating area

• The centroid of the volume of a prismatic body is located at the centroid of the

cross-sectional area that forms the middle plane of the volume.

x

C

To prove this statement, consider Fig. 8.9, which shows a prismatic body of thickness h that occupies the region . The xy-coordinate plane coincides with the middle plane of the body, and the z-axis is the centroidal axis (passes through the centroids of the cross-sectional areas). The foregoing statement will be proven if we can show that the origin of the coordinate system is the centroid C of the body—that is, if we can show that x¯ = y¯ = z¯ =0. There is no question that C lies on the xy-plane (z¯ =0), because it is the plane of symmetry. To show that x¯ = y¯ =0, it is sufﬁcient to demonstrate that y dV = x dV =0. Using the differential volume element dV = h dA shown in Fig. 8.9, we get y dV = y (h dA)= h y dA=0, where is the plane region of the cross section. The last equality follows from the knowledge that y dA=0 if y is measured from the centroid of the cross-sectional area. It can be proven in a similar manner that x dA=0.

y

Fig. 8.8

z

Region

h 2

Plane region (middle plane)

h 2

C

dA

y

x

x y

dV

###### Fig. 8.9

Identical symmetry arguments can be used to locate the centroids of surfaces and space curves. For example, knowing the centroidal coordinates of a semicircular arc, shown in Fig. 8.10(a), we can immediately deduce the centroidal coordinates of the half cylindrical surface in Fig. 8.10(b).

z

h 2

y

C

h 2

|R|C<br><br>π2R<br><br>|
|---|---|
| | |

π2R

x y

x (a)

(b)

###### Fig. 8.10

The method of composite shapes also applies to curved surfaces, volumes, and space curves. The expressions for the centroidal coordinates of composite surfaces and curves can be obtained by extending Eqs. (8.8) and (8.9) to three dimensions. The equations for composite volumes can be written by analogy with composite areas. The results are

Composite Areas

Aix¯i i Ai y¯ = i

Ai y¯i i Ai z¯ = i

Aiz¯i i Ai

x¯ = i

(8.11)

Composite Volumes

Vix¯i iVi y¯ = i

Vi y¯i iVi z¯ = i

Viz¯i iVi

x¯ = i

(8.12)

Composite Curves

Lix¯i i Li y¯ = i

Li y¯i i Li z¯ = i

Liz¯i i Li

x¯ = i

(8.13)

Note that these expressions are identical to Eqs. (8.10) except that the integrations have been replaced by summations.

In order to facilitate the application of Eqs. (8.11) and (8.12), the properties of some basic surfaces and volumes are shown in Tables 8.3 and 8.4.

|Right tetrahedron<br><br>x = 1 4<br><br>aMMy = 1 4<br><br>bMMz = 1 4<br><br>hMMV = 1 6<br><br>abh<br><br>z<br><br>y<br><br>x<br><br>h a<br><br>b x<br><br>y<br><br>z<br><br>C<br><br>|Pyramid<br><br>z = 3 4<br><br>hMMV = 1 3<br><br>abh<br><br>z<br><br>y<br><br>h z<br><br>x<br><br>b a<br><br>C|
|---|---|
|Cone<br><br>z = 3 4<br><br>hMMV =<br><br>3<br><br>R2h<br><br>| | |
|---|---|
| |C|
<br><br>z<br><br>R<br><br>y<br><br>z h<br><br>x<br><br>π<br><br>|Hemisphere<br><br>C<br><br>z<br><br>R<br><br>R z<br><br>x<br><br>y<br><br>z = 5 8<br><br>RMMV = 2 R3<br><br>3<br><br>π|
|Semi-ellipsoid of revolution<br><br>C<br><br>z<br><br>R<br><br>z = 5 8<br><br>hMMV = 2 R2h<br><br>3<br><br>y<br><br>h z<br><br>x<br><br>π|π<br><br>Paraboloid of revolution<br><br>C<br><br>z<br><br>R<br><br>y<br><br>h z<br><br>x<br><br>z = 2 3<br><br>hMMV = R2h<br><br>2|

|z<br><br>y<br><br>h<br><br>R<br><br>Conical surface<br><br>x<br><br>C<br><br>z<br><br>z = 2hMMA = πR R2 + h2<br><br>3<br><br>|
|---|
|z<br><br>R<br><br>x<br><br>y<br><br>R z<br><br>Hemispherical surface<br><br>z = RMMA = 2πR2<br><br>C<br><br>1<br>2<br>|

###### Table 8.3 Centroids of Volumes Table 8.4 Centroids of Surfaces

|Sample Problem 8.5<br><br>Determine the centroidal coordinates of the volume shown in Fig. (a) that is gener-<br><br>y<br><br>8in.<br><br>z<br><br>z2 = 2y Generating<br><br>area<br><br>(a)<br><br>x<br><br>ated by rotating the area under the curve z2 =2y about the y-axis. The coordinates are measured in inches.<br><br>Solution<br><br>By symmetry, x¯ = z¯ =0. Integration must be used to ﬁnd y¯. There are two convenient single-integration techniques for volumes of revolution; the method of thin disks and the method of thin shells.<br><br>Method I: Thin Disks<br><br>In this method, a differential element of the generating area is the vertical strip shown in Fig. (b). When the generating area is rotated about the y-axis to form the volume of revolution, the differential area element generates the thin disk of thickness dy and radius z that is shown in Fig. (c). Thus, the properties of the volume may be determined by integrating the properties of the disk.<br><br>z<br><br>y<br><br>y<br><br>dy<br><br>z<br><br>8 in.<br><br>(b)<br><br>y<br><br>x<br><br>z<br><br>(c)<br><br>The volume of the disk is<br><br>dV = πz2 dy = 2πy dy Integrating to determine the volume V, we obtain<br><br>V = 2π<br><br>8<br><br>0<br><br>y dy = 2π<br><br>y2 2<br><br>8<br><br>0<br><br>= 64π in.3<br><br>Because the distance from the disk to the xz-plane is y, the corresponding ﬁrst moment is dQxz = y dV, which on substituting the expression for dV becomes<br><br>dQxz = y(2πy dy) = 2πy2 dy Integration yields for the ﬁrst moment of the volume<br><br>Qxz = 2π<br><br>8<br><br>0<br><br>y2 dy = 2π<br><br>y3 3<br><br>8<br><br>0<br><br>= 341π in.4|
|---|

|Therefore, the centroidal coordinates of the volume are<br><br>y¯ =<br><br>Qxz V =<br><br>341π 64π = 5.33 in. x¯ = z¯ = 0 Answer<br><br>Method II: Thin Shells<br><br>In this method, a differential element of the generating area is the horizontal strip shown in Fig. (d). Rotation about the y-axis generates a shell of inﬁnitesimal<br><br>z<br><br>y<br><br>y 8 – y<br><br>z<br><br>(d)<br><br>dz<br><br>4 in.<br><br>4 +<br><br>z2 4<br><br>thickness dz, as shown in Fig. (e).<br><br>y<br><br>x<br><br>z<br><br>(e)<br><br>The volume of the thin shell (circumference × thickness × length) is<br><br>dV = 2πz dz(8 − y) = 2πz 8 −<br><br>z2 2<br><br>dz = π(16z − z3)dz<br><br>Noting that the range of z is from 0 to 4in., the volume is given by<br><br>V = π<br><br>4<br><br>0<br><br>(16z − z3)dz = π 8z2 −<br><br>z4 4<br><br>4<br><br>0<br><br>= 64π in.3<br><br>Referring to Fig. (d), we see that the y-coordinate of the centroid of the thin shell is y¯el = y + (8 − y)/2 = 4 + (y/2) = 4 + (z2/4), and its ﬁrst moment with respect to the xz-plane becomes<br><br>dQxz = y¯el dV = 4 +<br><br>z2 4<br><br>π(16z − z3)dz = π 64z −<br><br>z5 4<br><br>dz<br><br>Therefore, we obtain<br><br>Qxz = π<br><br>4<br><br>0<br><br>64z −<br><br>z5 4<br><br>dz = π 32z2 −<br><br>z6 24<br><br>4<br><br>0<br><br>= 341π in.4<br><br>and the centroidal coordinates of the volume become<br><br>y¯ =<br><br>Qxz V =<br><br>341π 64π = 5.33 in. x¯ = z¯ = 0 Answer<br><br>Of course, these answers are identical to those obtained by the method of thin disks.|
|---|

|Sample Problem 8.6<br><br>Locate the centroid of the hyperbolic paraboloid shown in Fig. (a) using (1) single integration with a differential volume element parallel to the xz-plane; and (2) double integration. The equation of the surface that bounds the volume is (y2/b2) − (x2/a2) = z/c.<br><br>x<br><br>b<br><br>z<br><br>y a<br><br>c<br><br>y2 b2<br><br>x2 a2<br><br>– = z<br><br>c<br><br>(a)<br><br>a<br><br>Solution<br><br>Noting that x¯ = 0 by symmetry, we see that integration is required to ﬁnd y¯ and z¯ only.<br><br>Part 1: Single Integration<br><br>The dimensions of a differential volume element dV, parallel to the xz-plane, are shown in Fig. (b). Because the cross section of the element is a parabola, we may use Table 8.1 to determine dV and z¯el (the volume and centroidal coordinate of the element).<br><br>dV =<br><br>2<br><br>3<br><br><br>2<br><br>a<br><br>b<br><br><br>y<br><br>cy2 b2<br><br>dy =<br><br>4 3<br><br>ac b3<br><br>y3 dy<br><br>z¯el =<br><br><br>2 5<br><br>cy2 b2<br><br>x<br><br>y<br>z<br><br><br>y ay b<br><br>(b)<br><br>ay dV b<br><br>dy<br><br>cy2 b2<br><br>zel<br><br>|
|---|

|Because the limits of integration are y = 0 to y = b, the volume becomes<br><br>V = dV =<br><br>4 3<br><br>ac b3<br><br>b<br><br>0<br><br>y3 dy =<br><br>abc 3<br><br>and the ﬁrst moments with respect to the xz- and xy-planes are<br><br>Qxz = y dV =<br><br>4 3<br><br>ac b3<br><br>b<br><br>0<br><br>y4 dy =<br><br>4ab2c 15<br><br>Qxy = z ¯el dV =<br><br>4 3<br><br>ac b3<br><br>2 5<br><br>c b2<br><br>b<br><br>0<br><br>y5 dy =<br><br>4abc2 45<br><br>Therefore, the centroidal coordinates of the hyperbolic paraboloid are<br><br>x¯ = 0<br>y¯ =<br><br>Qxz V =<br><br>4ab2c/15<br><br>abc/3 =<br><br>4b<br><br>5<br><br><br>Answer<br><br>z¯ =<br><br><br>Qxy V =<br><br>4abc2/45<br><br>abc/3 =<br><br>4c 15<br><br>Part 2: Double Integration<br><br>Using the double differential element of volume shown in Fig. (c), we have<br><br>dV = z dx dy z¯el =<br><br>z 2<br><br>x<br><br>y<br>z<br><br><br>y<br><br>(c)<br><br>dV<br><br>dy<br><br>z<br><br>y2 b2<br><br>x2 a2<br><br>z = c –<br><br>dx b<br><br>ay<br><br>x<br><br>Choosing to integrate ﬁrst on x, then on y, and using the fact that the volume is symmetric with respect to the yz-plane, we have<br><br>V = dV = 2<br><br>b<br><br>0<br><br>ay/b<br><br>0<br><br>z dx dy<br><br>Qxz = y dV = 2<br><br>b<br><br>0<br><br>ay/b<br><br>0<br><br>yz dx dy<br><br>Qxy = z ¯el dV = 2<br><br>b<br><br>0<br><br>ay/b<br><br>0<br><br>z 2<br><br>z dx dy<br><br>Substituting z =c[(y2/b2)−(x2/a2)] into the preceding expressions and performing the integrations yield the same results as found in part 1.|
|---|

|Sample Problem 8.7<br><br>Locate the centroid of the conical surface shown in Fig. (a). z<br><br>x<br><br>y<br><br>R<br><br>h<br><br>(a)<br><br>Solution<br><br>By symmetry, we see that x¯ = z¯ = 0. Because the conical surface is a surface of revolution, single integration can be used to calculate y¯.<br><br>As shown in Fig. (b), the differential area element is taken to be the area of the “ring,” technically known as a frustum, that is generated by rotating the line segment of differential length ds about the y-axis. The area of this differential element (circumference × slant height) is<br><br>dA = 2πz ds<br><br>z<br><br>x<br><br>y<br><br>(b)<br><br>z<br><br>y<br><br>h<br><br>R z<br><br>y<br><br>dy<br><br>ds<br><br>α α<br><br>Letting 2α be the cone angle as shown in Fig. (b), we have z = y tanα and ds=dy/cosα. Substituting these identities, together with tanα = R/h and cosα = h/√R2 + h2, into the expressions for the differential area, we obtain<br><br>dA =<br><br>2π R√R2 + h2 h2<br><br>y dy<br><br>Integrating to ﬁnd the area of the conical surface, we obtain<br><br>A =<br><br>2π R√R2 + h2 h2<br><br>h<br><br>0<br><br>y dy =<br><br>2π R√R2 + h2 h2<br><br>y2 2<br><br>h<br><br>0<br><br>= π R R2 + h2<br><br>From Fig. (b), we see that y is the distance from the xz-plane to the differential area element. Therefore, its ﬁrst moment relative to that plane is dQxz = y dA. Substituting the expression previously determined for dA, and integrating, the ﬁrst moment of the conical surface becomes<br><br>Qxz =<br><br>2π R√R2 + h2 h2<br><br>h<br><br>0<br><br>y2 dy =<br><br>2π R√R2 + h2 h2<br><br>y3 3<br><br>h<br><br>0<br><br>=<br><br>2<br><br>3<br><br><br>π Rh R2 + h2<br><br>|
|---|

|Therefore, the centroidal coordinates of the conical surface are<br><br>x¯ = z¯ = 0 Answer<br>y¯ =<br><br><br>Qxz A =<br><br>(2/3)π Rh√R2 + h2 π R√R2 + h2 =<br><br>2h<br><br>3<br><br><br>Observe that these results agree with data given for a conical surface in Table 8.4.<br><br>Sample Problem 8.8<br><br>Use the method of composite volumes to determine the location of the centroid of<br><br>0.8<br><br>0.75<br><br>x y<br><br>z<br><br>O<br><br>1.25 2.5<br><br>(a)<br><br>Dimensions in inches<br><br>4.3<br><br>4<br><br>the volume for the machine part shown in Fig. (a).<br><br>Solution<br><br>We note that x¯ = 0 because the yz-plane is a plane of symmetry of the volume.<br><br>To calculate y¯ and z¯, the machine part can be considered to be composed of the four volumes shown in Fig. (b): the rectangular solid 1, plus the semicylinder 2, plus the rectangular solid 3, minus the cylinder 4. Most centroidal coordinates of these volumes can be determined by symmetry; only z¯ of volume 2 must be found from Table 8.1.<br><br>(b)<br><br>1<br><br>x<br><br>2.5<br><br><br>2.5<br><br>y<br><br>3.25<br><br>0.8<br><br>z<br><br>x<br><br>0.8<br><br>z<br><br>y<br><br>2.5<br><br>2 3.25<br><br>x<br><br>0.8<br><br>z<br><br>y<br><br>2.5<br><br>2.5<br><br>4.3<br><br>0.75<br><br>4<br><br>z<br><br>1.25<br><br>0.8<br><br>y x<br><br>3.25<br><br>3<br>|
|---|

|The computations of the volumes and ﬁrst moments relative to the xy- and xz-planes are shown in the following table.<br><br>Part Volume V y¯ V y¯ z¯ V z¯ (in.3) (in.) (in.4) (in.) (in.4)<br><br>1 5(3.25)(0.8)=13.000 −0.40 −5.20 +<br><br>3.25 2 = +1.625 +21.13<br><br>2<br><br>π(2.5)2 2<br><br>(0.8) = 7.854 −0.40 −3.14 +3.25 +<br><br>4(2.5) 3π = +4.311 +33.86<br><br>3 5(4.30)(0.75) = 16.125 +<br><br>4.30 2 − 0.80 = +1.35 +21.77 −<br><br>0.75 2 = −0.375 −6.05<br><br>4 −π(1.25)2(0.80) = −3.927 −0.40 +1.57 +3.250 −12.76 33.052 ··· +15.00 ··· +36.18<br><br><br>Using the results displayed in the table, the centroidal coordinates of the machine part are<br><br>x¯ = 0<br>y¯ =<br><br>V y¯ V =<br><br>15.00 33.05 = 0.454 in. Answer<br><br>z¯ =<br><br><br>Vz¯ V =<br><br>36.18 33.05 = 1.095 in.<br><br>Sample Problem 8.9<br><br>Calculate the centroidal coordinates of the shaded surface shown in Fig. (a).<br><br>y<br><br>x<br><br>2<br><br>3<br><br>6<br><br>4<br><br>z<br><br>(a)<br><br>1.0<br><br>Dimensionsininches|
|---|

|Solution<br><br>The surface in Fig. (a) can be decomposed into the four plane areas in Fig. (b): the rectangle 1, plus the quarter circle 2, plus the triangle 3, minus the circle 4. The location of the centroid of each composite area can be found by symmetry or from Table 8.1.<br><br>x y<br><br>6<br><br>z<br><br>(b)<br><br>4<br><br>y<br><br>x<br><br>3<br><br>z<br><br>1.0<br><br>4<br><br>y<br><br>x<br><br>6<br><br>z<br><br>4<br><br>y<br><br>x<br><br>z<br><br>2<br><br>1<br><br>3<br><br>2<br><br>4<br><br>The following table lists the computations for the areas and ﬁrst moments of the areas.<br><br>Part Area A x¯ Ax¯ y¯ Ay¯ z¯ Az¯ (in.2) (in.) (in.3) (in.) (in.3) (in.) (in.3)<br><br>1 4(6) = 24 0 0 +3 +72.00 +2 +48.00<br>2<br><br>π(4)2<br><br>4 = 4π +<br><br>4R 3π = +<br><br>4(4) 3π +21.33 0 0 +<br><br>4R 3π = +<br><br>4(4) 3π +21.33<br><br>3<br><br>1<br><br>2<br><br><br>(4)(6) = 12 +<br><br>1 3<br><br>(4) +16.00 +<br><br>1 3<br><br>(6) +24.00 0 0<br><br>4 −π(1)2 = −π 0 0 +3 −3π +2 −2π 45.42 ··· +37.33 ··· +86.58 ··· +63.05<br>|
|---|

|Therefore, the centroidal coordinates of the shaded surface shown in Fig. (a) are<br><br>x¯ =<br><br>37.33<br><br>45.42 = 0.822 in.<br><br>y¯ =<br><br>86.58<br><br>45.42 = 1.906 in. Answer<br><br><br>z¯ =<br><br>63.05 45.42 = 1.388 in.<br><br>You should locate this point on Fig. (a) to verify that it represents a reasonable location of the centroid for the shaded surface.<br><br>Sample Problem 8.10<br><br>Determine the centroidal coordinates for the composite curve made up of three segments: the semicircular arc 1, and the straight lines 2 and 3.<br><br>x y<br><br>z<br><br>400 mm<br><br>300 mm<br><br>600mm 500mm<br><br>1<br><br>2<br><br>3<br><br>Solution<br><br>Segment 1 (semicircular arc) L1 = π R = 400π mm x¯1 = 400 mm, y¯1 = 0 (by inspection)<br><br>z¯1 =<br><br>2R<br><br>π =<br><br>2(400)<br><br>π =<br><br>800 π<br><br>mm (from Table 8.2)<br><br>Segment 2 (straight line)<br><br><br>L2 = 5002 + 6002 = 781.0 mm x¯2 = 300 mm y¯2 = 250 mm z¯2 = 0 (by inspection)<br><br>|
|---|

|Segment 3 (straight line)<br><br>L3 = 6002 + 3002 = 670.8 mm x¯3 = 300 mm y¯3 = 500 mm z¯3 = 150 mm (by inspection)<br><br>The remaining computations are carried out in the following table.<br><br>Segment Length L x¯ Lx¯ y¯ L y¯ z¯ Lz¯ (mm) (mm) (mm2) (mm) (mm2) (mm) (mm2)<br><br>1 400π 400 502.7 × 103 0 0<br><br>800 π<br><br>320.0 × 103<br><br>2 781.0 300 234.3 × 103 250 195.3 × 103 0 0<br>3 670.8 300 201.2 × 103 500 335.4 × 103 150 100.6 × 103 2708.4 ··· 938.2 × 103 ··· 530.7 × 103 ··· 420.6 × 103<br><br><br>Therefore, the centroidal coordinates of the composite curve are<br><br>x¯ =<br><br>Lx¯ L =<br><br>938.2 × 103 2708.4 = 346 mm<br><br>y¯ =<br><br>Ly¯ L =<br><br>530.7 × 103 2708.4 = 196 mm Answer<br><br>z¯ =<br><br><br>Lz¯ L =<br><br>420.6 × 103 2708.4 = 155 mm<br><br>You should locate this point on the ﬁgure to verify that it represents a reasonable location for the centroid of the composite curve.|
|---|

![image 60](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile60.png>)

###### Problems

- 8.39 Use integration to locate the centroid of the volume of the hemisphere. z

y

x

R

Fig. P8.39, P8.40

Compare your results with Table 8.3.

- 8.40 By integration, ﬁnd the centroid of the surface of the hemisphere. Compare your result with Table 8.4.
- 8.41 Locate the centroid of the volume obtained by revolving the triangle about

2 in.

y

x

4 in.

8 in.

Fig. P8.41, P8.42

the x-axis. Use integration.

- 8.42 Solve Prob. 8.41 assuming that the triangle is revolved about the y-axis.

y

h

b

x

y = h(1– x2/b2)

Fig. P8.43, P8.44

- 8.43 Use integration to ﬁnd the centroidal coordinates for the volume obtained by revolving the area shown about the x-axis.
- 8.44 Solve Prob. 8.43 assuming that the area is revolved about the y-axis.
- 8.45 Verify the centroidal z-coordinate of the pyramid shown in Table 8.3 by integration.
- 8.46 Use integration to compute the z-coordinate of the centroid of the half

y

z

x

h

R

Fig. P8.46, P8.47

cone.

- 8.47 Determine the centroidal z-coordinate of the curved surface of the half cone by integration.
- 8.48 By integration, determine the x- and y-centroidal coordinates for the volume shown.

h2

y

x

z

b

a

h1

z = h1– (h1– h2)

xy ab

y

z

x

b b z = h cos

a

π x 2a

π y 2b

a

h

cos

Fig. P8.48 Fig. P8.49

- 8.49 Locate the centroid of the volume between the curved surface and the xy-plane using integration.

B

8.50 Use integration to locate the centroid of the curved surface.

z = h

πθ

h

- 8.51 By integration, determine the centroidal coordinates of the curve connecting points A and B.
- 8.52–8.57 By the method of composite volumes, determine the centroidal coordinates of the volume.

z

y

R

θ

A

z

- x

Fig. P8.50, P8.51

16

z

13

4in.

4in.

19

6.5in.

3.5 in.

y

10 18

17in.

y

x

x

8in.

Dimensions in inches

###### Fig. P8.52 Fig. P8.53

z

60

120

40

z

80

60mm

80mm

20

45

y

65 mm

x

120

y x

120mm

Dimensions in mm

###### Fig. P8.54 Fig. P8.55

z

70

60

z

y

334 in.

80

312 in.

45

10

1 4

1 in. radius

x

160

90

2 in. radius

x

7 in.

10

y

43 in.

Dimensions in mm

###### Fig. P8.56 Fig. P8.57

z

8

###### 8.58 Use the method of composite volumes to ﬁnd the centroidal z-coordinate

40 y

of the split bearing.

###### 8.59 The cylindrical container will have maximum stability against tipping

when its centroid is located at its lowest possible position. Determine the depth h of the cylindrical portion that must be removed to achieve this.

10

56

x

8.60–8.65 Using the method of composite surfaces, locate the centroid of the surface.

78

Dimensions in mm

Fig. P8.58

1.5 in. 2 in.

z

12in.

###### z

1.5 0.75

h

12in.

15 in.

6 in.

25in.

15 in.

3

9in.

Fig. P8.59

x 1.5

3.5

- x y

y

Dimensions in inches

###### Fig. P8.60 Fig. P8.61

z

z

200

400

150

200

360

x

x

200

900

100

150

Dimensions in mm

150

y

Dimensions in mm

100

y

###### Fig. P8.62 Fig. P8.63

z

15

21

z

36

18 in.

y 54

x

x y

22in.

22in.

Dimensions in inches

###### Fig. P8.64 Fig. P8.65

###### 8.66 The picture board and its triangular supporting bracket form a composite surface. Calculate the height h of the support that minimizes the centroidal z-coordinate of the assembly.

z

100

Dimensions 100 in mm

h

250

y

150

x

###### Fig. P8.66

###### 8.67–8.69 By the method of composite curves, locate the centroid of the wire ﬁgure.

z

3 in.

z

120 mm

120 mm

120 mm

100mm

100mm

7 in.

y

6 in.

x y

x

###### Fig. P8.67 Fig. P8.68

y

8in.

60 51

92

12 in.

50

114

z

114

51

x

x y

5 in.

Dimensions in mm

###### Fig. P8.69 Fig. P8.70, P8.71

- 8.70 Use numerical integration to ﬁnd the centroid of the volume generated by

4.90in.

6.93in.

8.49in.

9.80in.

10.95in.

x

y

2 in.

12 in.

O

12.00in.

B

A

Fig. P8.72, P8.73

revolving the area shown about the x-axis.

- 8.71 Solve Prob. 8.70 assuming that the area is revolved about the y-axis.
- 8.72 Locate the centroid of the volume generated by revolving the area shown about the line AB. Use numerical integration.
- 8.73 (a) Solve Prob. 8.72 assuming that the area is revolved about the x-axis. (b) Check your result in part (a) with Table 8.3 knowing that the curve OB is a parabola.

- 8.74 Use numerical integration with x = 1.0 m to locate the centroid of the surface generated by revolving the parabola about the y-axis.

1 m

y

O

4 m

3 m

A y = 3

16

x2

x

Fig. P8.74, P8.75

- 8.75 Solve Prob. 8.74 assuming that the parabola OA is revolved about the xaxis.

###### 8.4 Theorems of Pappus-Guldinus

The theorems of Pappus-Guldinus* provide relatively simple methods for calculating surface areas and volumes of bodies of revolution, utilizing ﬁrst moments of curves and areas.

Theorem I The surface area generated by revolving a plane curve through 360◦ about a nonintersecting axis in the plane of the curve is equal to 2π times the ﬁrst moment of the curve about the axis of revolution.

Proof

Consider the curve with length L, shown in Fig. 8.11, that lies in the xy-plane. When this curve is rotated through 360◦ about the x-axis, the area of the ring generated by the differential curve length ds is dA = 2πyds. Therefore, the surface area generated by the entire curve becomes

###### A = 2π y ds = 2π Qx (8.14)

where Qx = yds is the ﬁrst moment of the curve about the x-axis. This completes the proof.

*Named after the Greek geometrician Pappus (fourth century A.D.) and the Swiss mathematician Paul Guldinus (1577–1643).

###### 8.4 Theorems of Pappus-Guldinus 439

y

dA

z

Curve of length L

- y

ds

y

x

x

###### Fig. 8.11

TheoremII The volume generated by revolving a plane area through 360◦ about a nonintersecting axis in the plane of the area is equal to 2π times the ﬁrst moment of the area about the axis of revolution.

Proof

Consider the region with area A, shown in Fig. 8.12, that lies in the xy-plane. When this area is rotated through 360◦ about the x-axis, the volume generated by the differential area dA is dV = 2πy dA. Therefore, the volume generated by the entire area is

###### V = 2π y dA = 2π Qx (8.15)

where Qx = y dA is the ﬁrst moment of the area about the x-axis. This completes the proof.

Note that if the generating curve or area is revolved through an angle less than 360◦, this angle, measured in radians, should replace 2π in Eqs. (8.14) or (8.15).

y

dV

z

y

Plane region of area A

dA

x

y

x

###### Fig. 8.12

|Sample Problem 8.11<br><br>The area shown in Fig. (a) is revolved around the x-axis to form the body shown<br><br>3in.<br><br>4.5 in.<br><br>1.0 in.<br><br>(a)<br><br>x<br><br>y<br><br>x<br><br>(b)<br><br>in Fig. (b). Using the theorems of Pappus-Guldinus, calculate (1) the volume of the body; and (2) the area of the curved surface of the body.<br><br>Solution<br><br>Part 1<br><br>By Theorem II, the volume of the body is V =2πQx, where Qx is the ﬁrst moment of the area in Fig. (a) about the x-axis. By the method of composite areas, Qx equals the ﬁrst moment of a rectangle minus the ﬁrst moment of a quarter circle, both taken about the x-axis—see Fig. (c). Table 8.1 is used to locate the centroid for the quarter circle, and the centroid for the rectangle has been determined from symmetry. Therefore, we obtain<br><br>Qx = Ay¯ =(3 × 3.5)(2.75) −<br><br>π(3)2 4<br><br>4.5 −<br><br>4 π = 6.066 in.3<br><br>Hence the volume of the body is<br><br>V = 2πQx = 2π(6.066) = 38.1 in.3 Answer<br><br>2.75 in. 1.0 in.<br><br>(c)<br><br>x<br><br>y<br><br>3.0 in.<br><br>3.5in.<br><br>C1 4.5 in.<br><br>x<br><br>y<br><br>R = 3 in.<br><br>4R 4 3π = π in.<br><br>C2<br><br>Part 2<br><br>The curved surface of the body in Fig. (b) is generated by revolving the quarter circular arc shown in Fig. (d) about the x-axis. By Theorem I, this area equals<br><br>(d)<br><br>4.5 in.<br><br>x<br><br>y<br><br>R = 3 in.<br><br>6 in.<br><br>C<br><br>45°<br><br>2R =<br><br>π π<br><br>2πQx, where Qx is the ﬁrst moment of the arc about the x-axis. The location of the centroid for the arc can be found in Table 8.3. Using L = π R/2 for the length of the arc and referring to Fig. (d), we obtain<br><br>Qx = Ly¯ =<br><br>π(3) 2<br><br>4.5 −<br><br>6 π<br><br>sin45◦ = 14.842 in.2<br><br>The area of the curved surface is<br><br>A = 2π Qx = 2π(14.842) = 93.3 in.2 Answer|
|---|

###### 440

8.76–8.88 Problems 441

![image 61](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile61.png>)

###### Problems

- 8.76 A 4-in. diameter hole is drilled in the conical frustum. Calculate the 2 in. 4 in.

8in.

12 in.

Fig. P8.76

volume and the surface area of the resulting body.

- 8.77 A torus is formed by rotating the circle about the axis AB. Compute the volume and the surface area of the torus.

- A a

b

- B

y

x

4 in.

5in.

Fig. P8.77 Fig. P8.78

- 8.78 A solid of revolution is formed by rotating the plane area shown about the

y-axis. Determine the surface area and the volume of the solid.

- 8.79 Compute the volume of the spherical cap that is formed when the circular

B

y

x

4 in.

A

60°

Fig. P8.79, P8.80

segment is revolved about the y-axis.

- 8.80 Calculate the surface area of the truncated sphere that is formed by rotating the circular arc AB about the y-axis.
- 8.81 The rim of a steel V-belt pulley is formed by rotating the plane area shown about the axis AB. Find the mass of the rim, given that the mass density of steel is 7850 kg/m3.

60 10

200

80

10

A B Dimensions in mm

60

2 in. radius

10 in. radius

z

15 in.

10 in.

Fig. P8.81 Fig. P8.82

- 8.82 Determine the volume of the machine part shown.
- 8.83 Determine the surface area of the paraboloid that is generated by rotating

###### y

y = 12(1 – x2/100) in.

12 in.

x

10 in.

the parabola about the y-axis. (Hint: Compute Qy of the parabola by integration.) Fig. P8.83

###### 8.84 The volume of the dome in the shape of a paraboloid is 2000ft3.

Determine the height h of the dome.

- 8.85 Find the surface area of the 90◦ duct elbow.

6 in.

8 in.

2 in. radius at each corner

5 in. radius

36

30

2

60°

Dimensions in meters

9 9

Fig. P8.85 Fig. P8.86

- 8.86 Determine the volume of the concrete arch dam.
- 8.87 (a) Find the volume of liquid contained in the ﬂask when it is ﬁlled to the

h

10 ft radius

Fig. P8.84

radius = 20

Full

142.5

Half full

h

“full” mark. (b) Determine the elevation h of the “half full” mark.

radius = 70

8.88 Determine the ratio b/a for which the volume of the ﬁll equals the volume of the material removed from the conical excavation. Assume that the ﬁll is axisymmetric about the excavation.

Dimensions in mm

Fig. P8.87

Excavation Fill

α

α

a

b

###### Fig. P8.88

###### 8.5 Center of Gravity and Center of Mass

The resultant of the gravity forces acting on a body, which we know as the weight of the body, acts through a point called the center of gravity of the body. The center of gravity is thus determined by the distribution of weight within the body.

The center of mass of a body is a very important concept in dynamics (it is the point through which the resultant inertia force acts); it is a property of the distribution of mass within the body. However, because weight and mass differ only by a constant factor (provided that the gravitational ﬁeld is uniform), we ﬁnd that the centers of mass and gravity coincide in most applications. Differences

###### 8.5 Center of Gravity and Center of Mass 443

arise only in problems in which the gravitational ﬁeld is not uniform. Therefore, it is not surprising that engineers frequently use the terms center of gravity and center of mass interchangeably.

###### a. Center of gravity

The weight of a body is the most common example of a distributed force. For a body occupying the region , as in Fig. 8.13 , the weight of a differential volume z

element dV is dW = γ dV, where γ is the weight density (weight per unit volume). The total weight W of the body is thus the resultant of an inﬁnite number of parallel forces dW; that is,

y x

###### W = dW = γ dV

- y

z

(a)

dVdV

Region

dW = γdV

- z

x

The point G through which the weight W acts is called the center of weight—or, more commonly—the center of gravity of the body—see Fig. 8.13(b).

The coordinates of G can be determined by equating the resultant moment of the distributed weight to the moment of W about the coordinate axes. Referring to Fig. 8.13(a) and (b), we obtain

W

G

###### Mx = −W y¯ = − y dW My = Wx¯ = x dW

z

y x

from which we obtain

y

x

- x¯ =

x dW dW =

xγ dV γ dV

(8.16a)

- y¯ =

(b)

Fig. 8.13

y dW dW =

yγ dV γ dV

(8.16b)

If we imagine that the body and the coordinate axes are rotated so that either the x- or y-axis is vertical, the equality of moments would yield

z dW dW

zγ dV γ dV

(8.16c)

z¯ =

=

The integrals in Eqs. (8.16) can be evaluated by the same techniques that were used to locate the centroids of volumes in Art. 8.3.

For homogeneous bodies, the weight density γ is constant and thus cancels in Eqs. (8.16), giving

x dV dV

y dV dV

z dV dV

x¯ =

y¯ =

z¯ =

Comparing these equations with Eqs. (8.10), we can make the following important observation.

The center of gravity of a homogeneous body coincides with the centroid of its volume.

Therefore, tables listing the centroids of volumes, such as Table 8.3, can be used to determine the location of the centers of gravity of homogeneous bodies.

###### b. Center of mass

The center of mass of a body is deﬁned as the point that has the following coordinates.

- x¯ =

x dm dm

=

xρ dV ρ dV

- y¯ =

y dm dm

=

yρ dV ρ dV

- z¯ =

(8.17)

z dm dm

zρ dV ρ dV

=

In Eqs. (8.17), dm is the mass of the differential element dV in Fig. 8.13(a), given by dm = ρ dV, where ρ is the mass density (mass per unit volume). If the gravitational ﬁeld is constant, which is a valid assumption in most engineering problems, the weight density γ and the mass density ρ are related by γ = ρg, where g is the gravitational acceleration (constant). In this case, the center of gravity and the center of mass for a given body coincide.

###### c. Composite bodies

If a body is composed of several simple shapes, we can use the method of composite bodies to ﬁnd its center of gravity or mass center. By replacing the integrals in Eqs. (8.16) by summations, we obtain for the center of gravity

Wix¯i Wi y¯ =

- Wi y¯i

- Wi z¯ =

Wiz¯i Wi

(8.18)

x¯ =

where Wi is the weight of the ith component of the body and (x¯i, y¯i, z¯i) are the coordinates of its center of gravity.

Similarly, the location of the mass center of a composite body can be obtained from Eqs. (8.17):

mix¯i mi y¯ =

mi y¯i mi z¯ =

miz¯i mi

(8.19)

x¯ =

where mi is the mass of the ith component and (x¯i, y¯i, z¯i) are the coordinates of its mass center.

|Sample Problem 8.12<br><br>The machine part in Fig. (a) consists of a steel hemisphere joined to an aluminum cylinder into which a hole has been drilled. Determine the location of the center of mass. The mass densities for aluminum and steel are 2700kg/m3 and 7850kg/m3, respectively.<br><br>y<br><br>z<br><br>30 20 50<br><br>12.5 30<br><br>Dimensions in mm<br><br>Steel Aluminum<br><br>(a)<br><br>z<br><br>x<br><br>y<br><br>Solution<br><br>By symmetry, we note that x¯ = z¯ = 0. If the machine part were homogeneous, its center of mass would coincide with the centroid of the enclosing volume, and y¯ could be determined using the method of composite volumes described in Art. 8.3. Because the machine part is not homogeneous, y¯ must be determined by the method of composite bodies.<br><br>100<br><br>30<br><br>y<br><br>z<br><br>|1|
|---|
<br><br>50<br><br>12.5<br><br>y<br><br>z<br><br>50<br><br>3<br><br>12.5<br><br>y<br><br>z<br><br>30<br><br>4<br><br>20<br><br>z<br><br>y 30<br><br>Steel<br><br>Aluminum<br><br>Aluminum<br><br>Aluminum<br><br>(b)<br><br>2<br><br>|
|---|

###### 445

|The part is composed of the four bodies shown in Fig. (b): the aluminum cylinder 1, plus the steel hemisphere 2, minus the aluminum cylinder 3, minus the aluminum cone 4. Because each of these bodies is homogeneous, each center of mass coincides with the centroid of the enclosing volume.<br><br>Aluminum Cylinder 1<br><br>m = ρV = ρπ R2h = 2700π(0.030)2(0.100) = 0.7634 kg y¯ =<br><br>100<br><br>2 = 50 mm (by symmetry) my¯ = (0.7634)(50) = 38.17 kg · mm<br><br>Steel Hemisphere 2<br><br>m = ρV = ρ<br><br>2π<br><br>3<br><br><br>R3 = 7850<br><br>2π<br><br>3<br><br><br>(0.030)3 = 0.4439 kg<br><br>y¯ = −<br><br>3 8<br><br>R = −<br><br>3 8<br><br>(30) = −11.25 mm (using Table 8.3) my¯ = (0.4439)(−11.25) = −4.994 kg · mm<br><br>Aluminum Cylinder 3 (to be subtracted)<br><br>m = −ρV = −ρπ R2h = −2700π(0.0125)2(0.050) = −0.06627 kg y¯ = 75 mm (by symmetry) my¯ = (−0.06627)(75) = −4.970 kg · mm<br><br>Aluminum Cone 4 (to be subtracted)<br><br>m = −ρV = −ρ<br><br>π 3<br><br>R2h = −2700<br><br>π 3<br><br>(0.0125)2(0.020) = −0.008836 kg<br><br>y¯ = 30 +<br><br>3<br><br>4<br><br><br>(20) = 45 mm (using Table 8.3) my¯ = (−0.008836)(45) = −0.3976 kg · mm<br><br>Totals<br><br>m = 0.7634 + 0.4439 − 0.06627 − 0.008836 = 1.1322 kg my¯ = 38.17 − 4.994 − 4.970 − 0.3976 = 27.81 kg · mm<br><br>Therefore, the coordinates of the mass center of the machine part are<br><br>x¯ = z¯ = 0 y¯ =<br><br>my¯ m =<br><br>27.81 1.1322 = 24.6 mm Answer<br><br>|
|---|

###### 446

![image 62](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile62.png>)

###### Problems

- 8.89 The steel cylinder with a cylindrical hole is connected to the copper cone. Find the center of gravity of the assembly. The weight densities of steel and copper are 489lb/ft3 and 556lb/ft3, respectively.

Steel

Copper

y

x

z

6in. 8in.

6in.

2 in.

1.5 in.

Fig. P8.89

- 8.90 The rocket casing is a cylindrical shell of mass 80kg. The mass of each

0.5 m

0.36m

1.8 m

x

A

y

z

Fig. P8.90

of the four triangular ﬁns attached to the casing is 12kg. All components are thin and of uniform thickness. Determine the coordinates of the mass center of the casing.

- 8.91 What is the ratio L/R for which the uniform wire ﬁgure can be balanced

R

L

Fig. P8.91

in the position shown?

- 8.92 Small screws are used to fasten a piece of hardwood to the bracket that is formed from 1/20-in.-thick steel sheet metal. For steel, γ =0.283 lb/in.3, and for hardwood, γ =0.029 lb/in.3 Locate the center of gravity of the assembly.
- 8.93 Plywood with two different thicknesses is used to fabricate the partition shown. Find the largest allowable ratio t2/t1 if the partition is not to tip over.

z

z

15

Thickness t2

21

5 in.

2 in.

36

t1

y

y

5 in.

t1

54

2 in. 4 in.

x

Dimensions in inches

x

###### Fig. P8.92 Fig. P8.93

y

###### 8.94 The aluminum cylinder is attached to the steel hemisphere. Find the height

9 in.

h of the cylinder for which the center of gravity of the assembly is at G. Use γ =0.283lb/in.3 for steel and γ =0.096lb/in.3 for aluminum.

Aluminum

| | |
|---|---|
| | |
|G<br><br>| |

h

x

8.95 Two uniform bars of different diameters are joined together as shown.

Bar AB is made of aluminum (ρ =2700 kg/m3) and bar CD is made of copper (ρ =8910 kg/m3). Find the coordinates of the mass center of the assembly.

Steel

- 8.96 The assembly is formed by joining a semicircular steel (γ = 490 lb/ft3) plate to a triangular aluminum (γ =166 lb/ft3) plate. Both plates are homogeneous and of thickness 1/8inch. Find the coordinates of the center of gravity of the assembly.
- 8.97 The steel pin A is inserted partway into the aluminum tube B. Determine the x-coordinate of the mass center of the assembly. Use ρ =2660 kg/m3 for aluminum and ρ =7850kg/m3 for steel.

Fig. P8.94

y

40 mm

160 mm

A C B

6 mm dia 8 mm dia

160 mm

y

130 36

z

27 12 x

27

x D

9in.

6in.

A

B

100

10 Dimensions in mm

Fig. P8.95

x

y

###### Fig. P8.96 Fig. P8.97

###### 8.98 Locate the center of gravity of the hammer if the mass of the steel head is 0.919kg, and the mass of the hardwood handle is 0.0990kg.

z

60 45

30 30

30

y

40

25

Ellipse

x

180

Dimensions in mm

###### Fig. P8.98

- 8.99 The total weight of the car wheel and tire is 24lb. To statically balance the wheel-tire assembly (to move its center of gravity to point O), 2-oz lead weights are attached to the rim at A and B. What was the location of the center of gravity of the assembly before the balancing weights were added?

45°

x

y

O

B

7 in.

A

y

h

G

R

H

x

Fig. P8.99 Fig. P8.100

- 8.100 The cylindrical water tank with R =12 ft and H =18 ft has thin steel walls of uniform thickness and weighs 23000lb when empty. Determine the depth of the water h for which the center of gravity G of the tank plus water will be located at the surface of the water. For water, use γ = 62.4 lb/ft3.
- 8.101 The thin, steel rod is rigidly attached to the plastic sheet. The masses are 4.5kg/m2 for the plastic sheet and 0.098kg/m for the steel rod. Determine the coordinates of the mass center of the assembly.

Steel

z

x

y

120 mm

Plastic

80mm

80mm

60mm

x

θ θ

y

8 in. 10 in.

45° 45°

in.

O

- 3
- 4

Fig. P8.101 Fig. P8.102

- 8.102 Five 34-in. diameter holes are to be drilled in a uniform plate. Determine the angle θ for the circular segment that must also be removed if the center of gravity is to remain at point O.

###### 8.6 Distributed Normal Loads

Our discussion of distributed loads in Art. 3.6 was limited to simple cases because the treatment of centroids was postponed until the present chapter. It is now possible to discuss distributed normal loads in a general context.

###### a. General case

Consider the general case of a distributed normal loading shown in Fig. 8.14(a). The magnitude of the loading is characterized by p(x, y, z), the load intensity (force per unit area). Letting dR be the force acting on the differential area dA, we have dR = np dA, where n is a unit vector normal to dA (in the direction of p). Then the resultant of the distributed load is the force R shown in Fig. 8.14(b), where

R = dR = np dA (8.20)

Moment equations can be used to determine the line of action of R—that is, the coordinates x¯, y¯, and z¯ (of course, if R = 0 and the sum of the moments is

dR = np dA

z

n

p dA

Load area

y

x

(a)

z

###### R

z

y

x y

not zero, the resultant is a couple). In general, n, p, and dA are functions of x, y, and z, and evaluation of the integrals may be complicated. The following special cases occur frequently enough to warrant special attention: ﬂat surfaces, line loads, uniform pressure on curved surfaces, and ﬂuid pressure.

###### b. Normal loads on ﬂat surfaces

The load shown in Fig. 8.15(a) is parallel to the z-axis and is assumed to be distributed across the load area , which lies in the xy-plane. In this case, the load intensity p is a function only of x and y. The resultant force is shown in Fig. 8.15(b). According to Eqs. (3.18) and (3.19) of Art. 3.6, the magnitude of the resultant force and its line of action are determined by

x dV V y¯ =

y dV V

(8.21)

R = dV = V x¯ =

where V is the volume of the region between the load surface and the load area.

z

Load surface

y

###### p(x, y)

x

Region

Load area (a)

z

R

y

x

C y

x

(b)

###### Fig. 8.15

Therefore, we arrive at the conclusions stated in Art. 3.6:

- • The magnitude of the resultant force is equal to the volume under the load surface.
- • The line of action of the resultant force passes through the centroid of the volume under the load surface.

###### c. Line loads

Line loads—that is, distributed loads for which the width of the loading area is negligible compared to its length—were also introduced in Art. 3.6. In that article, emphasis was given to loads distributed along straight lines. Here, we determine the resultants of loadings that are distributed along plane curves.

Fig. 8.16(a) shows a loading, parallel to the z-axis, that acts along a curve lying in the xy-plane. We let s be the length measured along the curve. The loading is characterized by the load intensity w(s) with units lb/ft, N/m, etc. The plot of w(s) is called the load diagram. We let A be the area of the region (curved surface) under the load diagram. The resultant R of the line load is shown in Fig. 8.16(b), with its line of action located by x¯ and y¯. Because the line load may be thought of as an inﬁnite number of parallel, differential forces, integration is used to ﬁnd the magnitude and line of action of R.

z

dR = wds = dA

w

Load diagram

Region

y

x

s

y ds

x

(a)

z

###### R

y

C

x y

As shown in Fig. 8.16(a), we let dR represent the inﬁnitesimal force that acts on the differential line length ds. Because dR = w ds = dA, where dA is the differential area under the loading diagram, we see that the magnitude of the resultant force equals the area of the curved surface ; that is,

###### R = dR = w ds = dA = A (8.22)

Equating moments of the load system in Figs. 8.16(a) and (b) about the coordinate axes yields

###### Mx = Ry¯ = y dR My = −Rx¯ = − x dR

After substituting R = A and dR = dA, we get

###### Ay¯ = y dA Ax¯ = x dA

from which we obtain

x dA A y¯ =

y dA A

(8.23)

x¯ =

Comparing Eqs. (8.23) and (8.10), we conclude that R acts at the centroid of the region under the load diagram. This point is labeled C in Fig. 8.16(b). The

- z-coordinate of the centroid is irrelevant, because R is a sliding vector. In summary, line loads distributed along a plane curve have the following

properties:

- • The magnitude of the resultant force is equal to the area under the load diagram.
- • The line of action of the resultant force passes through the centroid of the area under the load diagram.

These conclusions were made in Art. 3.6 for loads distributed along straight lines; now we see that they are also valid for curved lines.

###### d. Uniform pressure on curved surfaces

Uniform pressure refers to the special case in which the magnitude of the load intensity is constant. If p is constant, Eq. (8.20) becomes

###### R = pndA = p ndA (8.24)

It can be shown by vector analysis that

###### n dA = dAx i + dAy j + dAz k

z

dAy

dAx

n

dA

x

y

dAz

###### Fig. 8.17

where dAx, dAy, and dAz are the projections of dA on the three coordinate planes, as shown in Fig. 8.17. Therefore, Eq. (8.24) can be written as

z

R = p i dAx + j dAy + k dAz = p(Axi + Ayj + Azk) or

x y

(a)

Rx = pAx Ry = pAy Rz = pAz (8.25)

where Ax, Ay, and Az are the projections of the load area on the coordinate planes. In principle, moment equations could be used to determine the line of action of R. However, in many instances the line of action can be determined by symmetry.

L

D

There are many practical applications in which the results of Eqs. (8.25) can be used. For example, consider the cylindrical vessel with inside diameter D, shown in Fig. 8.18(a), that is subjected to a uniform internal pressure p. Half of the vessel

p

and the pressure acting on it are shown in Fig. 8.18(b). It is clear that the pressure p has a resultant force Pb that tends to rupture the vessel (to split it lengthwise). This bursting force can be calculated using integration as indicated in Eq. (8.24). However, from Eq. (8.25), we immediately obtain Pb = pAy = pDL, as shown in Fig. 8.18(c).

(b)

Although the formula “force equals pressure times projected area” is very useful, you must remember that it is valid only for uniform pressure.

L

D

Ay

###### e. Fluid pressure

Pb = pDL

If a surface is submerged in a ﬂuid of weight density γ, the pressure exerted by the ﬂuid is p = γh, where h is the depth measured from the free surface of the ﬂuid. The resultant of this pressure could be obtained by integration, but if the surface is curved, the analysis may become complicated because both the magnitude and direction of p vary. It is usually easier to ﬁnd the resultant by equilibrium analysis of a volume of water that is bounded by the curved surface, as illustrated below.

(c)

Fig. 8.18

Let us ﬁnd the resultant of the water pressure acting on the curved surface AB of the dam in Fig. 8.19(a) by considering equilibrium of the body of water contained in the region ABC shown in Fig. 8.19(b). The FBD of the water in Fig. 8.19(c) contains the following forces:

- R1: resultant of the uniform pressure exerted by the water above the region.
- R2: resultant of the linearly varying pressure due to water lying to the right of the region.

RAB: resultant of the pressure exerted by the dam; it is equal and opposite to the

force of the water acting on portion AB of the dam.

W: weight of the water contained in the region; it acts at the centroid G of region ABC.

p=γ·depth

hA

C

###### A

A

hB

B

B

(a)

(b)

R1

pA= γhA

C G

A

R2

W

RAB

B

pB = γhB

(c)

###### Fig. 8.19

The forces R1, R2, and W can be found by the methods described previously in this article. The horizontal and vertical components of RAB can then be found by force equations of equilibrium. A moment equation would be required to determine the line of action of RAB.

|Sample Problem 8.13<br><br>Determine the resultant of the line load shown in Fig. (a).<br><br>Solution<br><br>As shown in Fig. (b), we represent the original line loading as the sum of the following three components: 1—the parabolic load distributed along a straight line on the x-axis, 2—the uniform load distributed along the quarter circle lying in the xy-plane, and 3—the rectangular load along the y-axis. The resultant force of each load component equals the area under the corresponding load diagram, acting through the centroid of the diagram.<br><br>2.4 N/mm<br><br>rad.=120<br><br>80<br><br>90<br><br>Dimensions in mm<br><br>Parabola<br><br>z<br><br>y<br><br>x (a)<br><br>R3<br><br>R1<br><br>C1<br><br>C3<br><br>C2<br><br>y3<br><br>y2<br><br>x2<br><br>x1<br><br>z y<br><br>x (b)<br><br>R2<br><br>1<br><br>2<br><br>3<br><br>Load Component 1 Using Table 8.1 for the parabola, we have<br><br>R1 = A1 =<br><br>2<br><br>3<br><br><br>(90)(2.4) = 144.0 N<br><br>x¯1 = 120 +<br><br>3 8<br><br>(90) = 153.75 mm y¯1 = 0<br><br>Load Component 2<br><br><br>R2 = A2 =<br><br>π R 2<br><br>(2.4) =<br><br>π(120) 2<br><br>(2.4) = 452.4 N<br><br>Noting that the x- and y-centroidal coordinates for the curved surface are the same as the centroidal coordinates for the quarter circle lying in the xy-plane, Table 8.2 yields<br><br>x¯2 = y¯2 = R −<br><br>2R<br><br>π = 0.3634R = 0.3634(120) = 43.6 mm|
|---|

|Load Component 3<br><br>R3 = A3 = (80)(2.4) = 192.0 N x¯3 = 0 y¯3 = 120.0 + 40.0 = 160.0 mm<br><br>Resultant Load<br><br>From the foregoing data, we ﬁnd that the magnitude of the resultant is<br><br>R = R = 144.0 + 452.4 + 192.0 = 788.4 N Answer The coordinates of the point through which R acts are determined by<br><br>x¯ =<br><br>Rx¯ R =<br><br>(144.0)(153.75) + (452.4)(43.6) + (192.0)(0) 788.4<br><br>= 53.1 mm Answer<br><br>y¯ =<br><br><br>Ry¯ R =<br><br>(144.0)(0) + (452.4)(43.6) + (192.0)(160.0) 788.4<br><br>= 64.0 mm Answer<br><br>You should locate this point on Fig. (a) to conﬁrm that it represents a reasonable location for the line of action of the resultant force.<br><br>Sample Problem 8.14<br><br>The undersides of the 36-in.×24-in. corrugated sheets in Figs. (a) and (b) carry a uniform normal pressure of p0 =0.6 lb/in.2. Calculate the rectangular components of the resultant force acting on the underside of each sheet.<br><br>4 in.<br><br>z<br><br>y p0<br><br>(a)<br><br>4 in.<br><br>x<br><br>36in.<br><br>24in.<br><br>4 in.<br><br>4 in.<br><br>z<br><br>x<br><br>y<br><br>p0<br><br>(b)<br><br>24in.<br><br>36in.<br><br>Solution<br><br>Because each sheet is subjected to uniform normal pressure, it is possible to determine the components of the resultant force by using the pressure times the projected area. Thus Rx = p0Ax, Ry = p0Ay, and Rz = p0Az, where Ax, Ay, and Az are the projected areas of the loading surface on the three coordinate planes.|
|---|

|The construction in Fig. (c) shows that the projected areas are<br><br>36 in.<br><br>8 in.<br><br>Sheet (a)<br>Sheet (b)<br><br><br>(c)<br><br>z<br><br>y<br><br>y<br><br>Az<br><br>Ay Sheet (a)<br><br>Ax = 0 Ay = 8 × 24 = 192 in.2 Az = 36 × 24 = 864 in.2<br><br>Sheet (b)<br><br>Ax = 0 Ay = 0 Az = 36 × 24 = 864 in.2<br><br>Therefore, for sheet (a), the rectangular components of the resultant force are<br><br>Rx = p0Ax = 0 Ry = p0Ay = 0.6(192) = 115.2 lb<br><br>Answer Rz = p0Az = 0.6(864) = 518 lb<br><br>For sheet (b), we have<br><br>Rx = p0Ax = 0 Ry = p0Ay = 0<br><br>Answer Rz = p0Az = 0.6(864) = 518 lb<br><br>Sample Problem 8.15<br><br>A swimming pool is ﬁlled with water to a depth of 3m, as shown in Fig. (a). Determine the magnitude and line of action of the resultant force that acts on the circular portion AB of the wall. The length of the wall (dimension perpendicular to the paper) is 25m, and the mass density of water is 1000kg/m3.<br><br>Solution<br><br>The free-body diagram of the water contained in the region OAB (25m in length) is shown in Fig. (b). The pressures p1 and p2 are equal to the products of the<br><br>radius=1.6 m<br><br>Length of wall = 25 m<br><br>(a)<br><br>3 m<br><br>| | | |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
| | | |
| | | |
| |O A| |
| | | |
<br><br>B<br><br>|
|---|

|weight density of water γ and the depths at A and B, respectively. Letting ρ be the mass density, we have γ = ρg = 1000(9.81) = 9.81 kN/m3.<br><br>0.8 m<br><br>0.8 m<br><br>y<br><br>O<br><br>P1<br><br>A<br><br>x<br><br>p1 = h = (9.81)(1.4) = 13.73 kN/m2<br><br>p2 = h = (9.81)(3) = 29.43 kN/m2<br><br>4(1.6) 3π<br><br>= 0.6791 m<br><br>P2<br><br>p1<br><br>P3<br><br>1.6 3<br><br>= 0.5333 m B<br><br>W<br><br>x0<br><br>R<br><br>(b)<br><br>C<br><br>γ<br><br>γ<br><br>0.8 m 0.8 m<br><br>The resultant forces P1 and P2 are caused by the uniformly distributed loadings shown, and P3 is due to the triangular portion of the loading. Each of these forces equals the product of the pressure (average pressure is used for P3) and the area on which the pressure acts.<br><br>P1 = p1A = (13.73)(1.6)(25) = 549.2 kN<br>P2 = p1A = (13.73)(1.6)(25) = 549.2 kN<br>P3 =<br><br><br>p2 − p1 2<br><br>A =<br><br>29.43 − 13.73 2<br><br>(1.6)(25) = 314.0 kN<br><br>The lines of action of P1, P2, and P3 pass through the centroids of the corresponding load diagrams. The weight W of the water contained in the region OAB is<br><br>W = γ × volume = (9.81)<br><br>π(1.6)2 4<br><br>(25) = 493.1 kN<br><br>Letting R be the resultant force exerted on the water by the curved portion of the wall, we can ﬁnd its components from the force equilibrium equations. Referring to the FBD in Fig. (b), we obtain<br><br>Fx = 0 −→+ P2 + P3 − Rx = 0<br><br>Rx = P2 + P3 = 549.2 + 314.0 = 863.2 kN<br><br>Fy = 0 +  Ry − W − P1 = 0<br><br>Ry = W + P1 = 493.1 + 549.2 = 1042.3 kN<br>|
|---|

|Therefore, the magnitude and direction of R are<br><br>1042.3 kN<br><br>863.2 kN<br><br>θ<br><br>R R = (863.2)2 + (1042.3)2<br><br>= 1353 kN θ = tan−1<br><br>1042.3 863.2 = 50.4◦<br><br>To ﬁnd the line of action of R, we use the moment equation of equilibrium. Choosing point B in Fig. (b) as the moment center and letting x0 be the distance between B and C (the point where R intersects the x-axis), we obtain<br><br>MB = 0 + Ryx0 − P1(0.8) − P2(0.8)<br><br>− P3(0.5333) − W(0.6791) = 0 from which we have<br><br>x0 =<br><br>549.2(0.8) + 549.2(0.8) + 314.0(0.5333) + 493.1(0.6791) 1042.3 = 1.325 m<br><br>The force exerted by the water on the wall is equal and opposite to the force determined above, as shown in Fig. (c).<br><br>B<br><br>O A<br><br>R = 1353 N 50.4°<br><br>1.325 m<br><br>C<br><br>(c)<br><br>Answer|
|---|

![image 63](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile63.png>)

###### Problems

Unless integration is speciﬁed, the following problems are to be analyzed using the information in Tables 8.1–8.3.

- 8.103 Wind pressure acting on a cylinder can be approximated by p = p0 cosθ, where p0 is a constant (note that on the lee side the pressure is negative). Determine the resultant force of the wind pressure on a cylinder of radius R and length L by integration.

|θ|R<br><br>|
|---|---|
| | |

p

Wind

p0 p0

2.5 5 7.5 10 12.5 15

x (ft)

w (lb/ft)

0

42.5

37.5

28.3

32.4

42.3

52.1

58.6

Fig. P8.103 Fig. P8.104

- 8.104 The beam carries the distributed line load shown. Use numerical integration to determine the resultant force and its line of action.
- 8.105 The pressure acting on the square plate varies as

y b b

x

2p0

p0

Fig. P8.105

p = p0

x b +

xy b2

where p0 is a constant. Use integration to ﬁnd the resultant force of the pressure, and the x- and y-coordinates of its line of action.

- 8.106 The intensity of the line loading acting on the rim of the semicircular

plate varies as w = w0y/a, where w0 is a constant and a is the radius of the plate. Use integration to determine the resultant force and to locate its line of action.

y

x

a w0

a

B

θ

A

y

x O

w0

w = w0 cos θ

Fig. P8.106 Fig. P8.107

- 8.107 Use integration to determine the resultant of the normal line loading acting on the circular arch.
- 8.108 If the intensity of the line loading is w = [(40x − x2)/40] lb/in., where x

60 in.

w(x) O x

x

is measured in inches, use integration to ﬁnd the resultant. Fig. P8.108

- 8.109 Determine the resultant force of the line loading and the x- and y-coordinates of its line of action.

Parabola

z

x

y

4 lb/in.

160in.

220in.

0.4m

x y

z

Radius = 0.2 m

180 N/m

Fig. P8.109 Fig. P8.110

- 8.110 Find the resultant of the line load shown.
- 8.111 Determine the resultant force or resultant couple for each of the line loads shown. In each case the loading is normal to the line and has constant intensity w0.

|O|a|
|---|---|
| | |

w0

y

x

(a)

a

w0

y

x (b)

O

| |a|
|---|---|
|O| |

w0

y

x

(c)

2a

|O|a|
|---|---|
| | |

w0

y

x

(d)

a

Fig. P8.111

- 8.112 The inside surface of each thin shell carries a uniform normal pressure of intensity p0. Compute R, the magnitude of the resultant force for each case.

z

z

a

y h

x

a

x y

(a) Cone

(b) Hemisphere

z

z

a

x y h

a

x y

(c) Quarter sphere

(d) Half cone

###### Fig. P8.112

- 8.113 Calculate the resultant force caused by the water acting on the parabolic arch dam. The water levels are 16ft on the upstream side and zero on the downstream side. For water, use γ = 62.4 lb/ft3.

40ft

40ft

16 ft

Downstream side

Upstream side Parabola

16ft

A

B

Diameter = d

Radius=a

Fig. P8.113 Fig. P8.114

- 8.114 Determine the resultant force acting on the elbow of the thin-walled pipe when the pipe carries a uniform internal pressure p0.
- 8.115 The thin plate of area A is submerged in ﬂuid of weight density γ. Show

h

C

A

that the resultant force of the ﬂuid pressure acting on one side of the plate is R = γhA¯ where h¯ is the depth of the centroid C of the area of the plate.

Fig. P8.115

###### 8.116 Each of the three gates has a constant width c (perpendicular to the paper). Calculate the force P required to maintain each gate in the position shown. Express your answers in terms of b, c, h, and γ (the weight density of the ﬂuid).

y

b

b

b

P

P

P

B

B

B

h

h

h

Parabola

Parabola

x

A

A

A

(b)

(b)

(a)

Fig. P8.116

###### 8.117 The concrete dam shown in cross section holds back fresh water (ρ =1000kg/m3). Determine the resultant force R of the water pressure acting on one meter length of the dam. Also, compute the coordinates of a point on the line of action of R.

y

4.3 m 3.9 m 3.3 m

5.8 m

7.5 m

y

x

1.5 m

Fig. P8.117

Parabola

4 m

###### 8.118 A concrete seawater dam is shown in cross section. Is the dam safe

against tipping about edge A? The mass densities are 2400kg/m3 for concrete and 1030kg/m3 for seawater.

x

O A

8.119 Determine the force F required to pull up the 2.5-oz stopper from the drain of a sink if the depth of water is 9in. Use γ =0.036 lb/in.3 for water and neglect the weight of the chain.

2.5 m

- Fig. P8.118

F

z

9 in.

|0.5 in. 2.5|oz|
|---|---|
| | |

115mm

y

90°

2 in. dia

x

###### Fig. P8.119 Fig. P8.120

- 8.120 If the trough is ﬁlled with water (ρ =1000 kg/m3), determine the resultant of the water pressure acting on one of the equilateral triangular end plates.
- 8.121 The pressure acting on the circular plate of radius a varies as

p = p0 [1 + (r/a)cosθ], where p0 is a constant. Use integration to ﬁnd the resultant force and to locate its line of action.

| | |
|---|---|
| | |

x

p

a

r

y

2p0

θ

A

B

8ft

Fig. P8.121 Fig. P8.122

- 8.122 The 10-ft wide quarter-circular gate AB is hinged at A. Determine the contact force between the gate and the smooth surface at B due to water pressure acting on the gate. Use γ = 62.4lb/ft3 for water.

![image 64](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile64.png>)

###### Review of Equations

###### First moments of areas and curves

Plane area: Qx = y dA Qy = x dA Plane curve: Qx = y ds Qy = x ds

###### Composite areas and curves

Qx = i(Qx)i Qy = i(Qy)i

###### Centroidal coordinates of areas and curves

Plane area: x¯ = Qy A y¯ = Qx/A Plane curve: x¯ = Qy L y¯ = Qx/L

###### Theorems of Pappus-Guldinus

A = 2π Qx

A = area of surface generated by rotating a plane curve about x-axis Qx = ﬁrst moment of the generating curve about x-axis

V = 2π Qx

V = volume of the solid generated by rotating a plane area about x-axis Qx = ﬁrst moment of the generating area about x-axis

###### Center of gravity—composite bodies

Wix¯i iWi y¯ = i

Wi y¯i iWi z¯ = i

Wiz¯i iWi

x¯ = i

###### Resultant of normal load on a ﬂat surface

R = volume under the load surface x¯, y¯ = centroidal coordinates of the volume under the load surface

###### Resultant of uniform pressure on a curved surface

Rx = pAx Ry = pAy Rx = pAz

![image 65](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile65.png>)

###### Review Problems

y

###### 8.123 The center of gravity of the plane wire ﬁgure is located at G. Determine

the lengths a and b.

###### 8.124 The 10-m wide gate restrains water at a depth of 6ft. Calculate the magnitude of the hinge reaction at A, and the contact force between the gate and the smooth surface at B. Neglect the weight of the gate.

4in.

G a

x

b

A

Fig. P8.123

- 3 m

- 4 m

2 m

L w

35°

y

B

Fig. P8.124 Fig. P8.125

###### 8.125 The pressure of wind acting on a pole of length L results in the line

loading w=w0 1 − exp(−5y/L) , where w0 is a constant. Use integration to determine the reactive couple at the base of the pole.

###### 8.126 The bin, open at the top and closed at the bottom, is made from sheet metal of uniform thickness. Locate its center of gravity.

z

25

20

40

x

y

Dimensions in inches

###### Fig. P8.126

- 8.127 Find the volume of the solid that is generated by rotating the plane area shown about the y-axis.

| | |
|---|---|
|40| |

20

30 20

y

Dimensions in mm

Fig. P8.127, P8.128

- 8.128 Determine the surface area of the solid that is generated by rotating the plane area shown about the y-axis.
- 8.129 The rectangular plate is subjected to the pressure

p = p0

x a

cos

πy 2b

Determine the resultant force of the pressure and the coordinates of its point of application.

y a

b

b

x

p0

Fig. P8.129

- 8.130 Calculate the tension in each of the three ropes which support the uniform steel plate weighing 0.284lb/in.3

20 in.

C B

34 in.

20 in.

15in.

A

###### Fig. P8.130

- 8.131 Using the method of composite areas, ﬁnd the centroid of the truncated parabolic complement.

b b

h

y

x

Fig. P8.131, P8.132

- 8.132 Find the centroid of the truncated parabolic complement by integration.
- 8.133 The screwdriver has a plastic handle and a 9-in. steel shaft. Find

- the x-coordinate of its mass center. Use γ =0.055lb/in.3 for plastic and γ =0.283lb/in.3 for steel.

1.25 in.

0.4 in.

x

4 in. 7.5 in.

9 in.

Fig. P8.133

- 8.134 Determine the dimension h if the centroid of the homogeneous axisym-

z

r

h

C

O

30 in.

20 in.

10 in.

Fig. P8.134

metric solid is located at C.

- 8.135 Two hemispherical shells of inner diameter 1m are joined together with 12 equally spaced bolts. If the interior pressure is raised to 300kPa above atmospheric pressure, determine the tensile force in each bolt.

1 m dia

Fig. P8.135

- 8.136 Calculate the area of the surface generated when the plane z-curve is

y

2.5 in. 3 in.

4 in.

2 in.

x

###### rotated about (a) the x-axis; and (b) the y-axis. Fig. P8.136

- 8.137 Determine the resultant of the line loading, given that w0 = 36 lb/ft.

3ft

3ft

x y

w0

w0

3ft

Fig. P8.137

- 8.138 Find the coordinates of the centroid of the plane region. The region is symmetric about the y-axis.

###### P

z

3 in. 3 in. 3 in.

y

y

- 5 in. dia

- 6 in. dia

2 in.

x

5 ft

8 in.

1.5ft

6 in.

x

###### Fig. P8.138 Fig. P8.139, P8.140 Fig. P8.141

- 8.139 The sheet metal trough has a uniform wall thickness. Determine the coordinates of its center of gravity.
- 8.140 The trough is ﬁlled with water (γ = 62.4lb/ft3). Determine the resultant force of the water pressure acting on one of the semicircular ends and the coordinates of its point of application.
- 8.141 The thin-walled cylindrical can with a spherical dimple weighs 0.2lb. Determine the force P required to push the can into water to a depth of 8in. Use γ = 0.036 lb/in.3 for water.
- 8.142 Find the location of the centroid of the plane region.

###### y

14

70

x 35

35 Dimensions in mm

###### Fig. P8.142

# 9

### Moments and Products of Inertia of Areas

![image 66](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile66.png>)

The strength and rigidity of a beam is determined by the moment of inertia of its cross-sectional area. The computation of area moments of inertia is the main topic of this chapter. Peter Dazeley/ Photographer’s Choice RF/Getty Images

###### 9.1 Introduction

First moments of areas, as presented in Chapter 8, dealt with the integrals x dA and y dA. In this chapter, we discuss the second moments of plane areas, also known as moments of inertia, x2 dA and y2 dA. We also introduce the product of inertia xy dA.

Moments and products of inertia arise in the analysis of linear load distributions acting on plane areas. Such distributions occur in members subjected to bending (beams), and in circular shafts carrying twisting couples. In addition, moments and products of inertia are encountered in the determination of resultants acting on submerged surfaces.

###### 471

In this chapter we also discuss the dependence of moments and products of inertia on the orientation of the coordinate system. This dependence results in the transformation equations for moments and products of inertia, which are used to determine the maximum and minimum moments of inertia at a point. This chapter concludes with a discussion of Mohr’s circle, a graphical method for representing the transformation equations.

9.2 Moments of Inertia of Areas and Polar

Moments of Inertia

a. Moment of inertia of area

In Art. 8.2, the ﬁrst moments of the area of a plane region about the x- and y-axes were deﬁned as

Qx = y dA Qy = x dA (9.1)

where A is the area of the region and x and y are the coordinates of the differential area element dA, as shown in Fig. 9.1.

Plane region

y

dA

x

r

y

x

O

###### Fig. 9.1

The moments of inertia of the area about the x- and y-axes, respectively, are deﬁned by*

Ix = y2 dA Iy = x2 dA (9.2)

Because the distances x and y are squared, Ix and Iy are sometimes called the second moments of the area.

The dimension for moment of inertia of area is [L4]. Therefore, the units are in.4, mm4, and so forth. Although the ﬁrst moment of an area can be positive, negative, or zero, its moment of inertia is always positive, because both x and y in Eqs. (9.2) are squared.

*The term moment of inertia of an area should not be confused with moment of inertia of a body, which occurs in the study of dynamics. The latter refers to the ability of a body to resist a change in its rotation and is a property of mass. Because an area does not have mass, it does not possess inertia. However, the term moment of inertia is used because the integrals in Eqs. (9.2) are similar to the expression r2 dm that deﬁnes the moment of inertia of a body.

Caution Recall that the ﬁrst moment of an area can be obtained from Qx = Ay¯, where y¯ is the centroidal coordinate of the area. A mistake frequently made is to assume that Ix = Ay¯2. Although the ﬁrst moment of an area equals the area times the centroidal distance, the second moment of an area is not equal to the area times the centroidal distance squared.

###### b. Polar moment of inertia

Referring again to Fig. 9.1, the polar moment of inertia of the area about point O (strictly speaking, about an axis through O, perpendicular to the plane of the area) is deﬁned by

###### JO = r2 dA (9.3)

where r is the distance from O to the differential area element dA. Note that the polar moment of an area is always positive and its dimension is [L4].

From Fig. 9.1, we note that r2 = y2 + x2, which gives the following relationship between polar moment of inertia and moment of inertia:

###### JO = r2 dA = (y2 + x2)dA = y2 dA + x2 dA

or

###### JO = Ix + Iy (9.4)

This relationship states that the polar moment of inertia of an area about a point O equals the sum of the moments of inertia of the area about two perpendicular axes that intersect at O.

###### c. Parallel-axis theorems

There is a simple relationship between the moments of inertia about two parallel axes, provided that one of the axes passes through the centroid of the area. Referring to Fig. 9.2(a), let C be the centroid of the area contained in the plane region

and let the x -axis be the centroidal axis that is parallel to the x-axis. We denote the moment of inertia about the x -axis by I¯x, which is to be read as the “moment of inertia about the centroidal x-axis” (about the axis that is parallel to the x-axis and passes through the centroid of the area). Observe that the y-coordinate of the differential area dA can be written as y = y¯ + y , where y¯ (the centroidal coordinate of the area) is the distance between the two axes. Equations (9.2) yield the following expression for the moment of inertia of the area about the x-axis (note that y¯ is constant).

Ix = y2 dA = (y¯ + y )2 dA

= y¯2 dA + 2y¯ y dA + (y )2dA (a)

y

x

y'

Plane region

dA

x'

y'

C

x

x'

y

r

y

x

O

(a)

###### C

Ia

d

Ia

a

(b)

###### Fig. 9.2

Noting that dA= A (the area of the region), y dA=0 (the ﬁrst moment of the area about a centroidal axis vanishes), and (y )2dA= I¯x (the second moment of the area about the x -axis), Eq. (a) simpliﬁes to

Ix = I¯x + Ay¯2 (9.5a)

This relationship is known as the parallel-axis theorem for moment of inertia of an area. The distance y¯ is sometimes called the transfer distance (the distance through which the moment of inertia is to be “transferred”). It is important to remember that the theorem is valid only if I¯x is the moment of inertia about the centroidal x-axis. If this is not the case, the term y dA in Eq. (a) would not vanish, giving rise to an additional term in Eq. (9.5a).

Because the direction of the x-axis in Fig. 9.2(a) can be chosen arbitrarily, the parallel-axis theorem applies to axes of any orientation. For example, applying the theorem to the y-axis yields

Iy = I¯y + Ax¯2 (9.5b)

where I¯y is the moment of inertia of the area about the centroidal y-axis—that is, the y -axis in Fig. 9.2 (a), and x¯ is the x-coordinate of the centroid.

In general, the parallel-axis theorem can be written as

###### Ia = I¯a + Ad2 (9.6)

As illustrated in Fig. 9.2(b), Ia is the moment of inertia about an arbitrarily oriented a-axis, I¯a represents the moment of inertia about the parallel axis that passes through the centroid C, and d is the distance between the axes (transfer distance).

By inspection of Eq. (9.6), we see that, given the direction of the axis, the moment of inertia of an area is smallest about the axis that passes through the centroid of the area. In other words, I¯a is smaller than the moment of inertia about any other axis that is parallel to the a-axis.

The parallel-axis theorem also applies to the polar moment of inertia. Denoting the polar moment of inertia of the area about the origin O by JO, and about the centroid C by J¯C, we have from Eqs. (9.4) and (9.5)

###### JO = Ix + Iy = (I¯x + Ay¯2) + (I¯y + Ax¯2)

Using I¯x + I¯y = J¯C, this equation becomes

###### JO = J¯C + Ar¯2 (9.7)

where r¯ = x¯2 + y¯2 is the distance between points O and C, as shown in Fig. 9.2(a).

###### d. Radius of gyration

In some structural engineering applications, it is common practice to introduce the radius of gyration of area. The radii of gyration of an area about the x-axis,

- the y-axis, and the origin O are deﬁned as

Iy A

Ix A

JO A

(9.8)

kx =

ky =

kO =

The dimension of the radius of gyration is [L]. However, the radius of gyration is not a distance that has a clear-cut physical meaning, nor can it be determined by direct measurement; its value can be determined only by computation using Eqs. (9.8). The radii of gyration are related by the equation

###### k2O = kx2 + k2y (9.9)

which can be obtained by substituting Eqs. (9.8) into Eq. (9.4).

###### e. Integration techniques

When computing the moment of inertia of an area about a given axis by integration, we must choose a coordinate system and decide whether to use single or double integration. The differential area elements dA associated with various coordinate systems were discussed in Art 8.2 and illustrated in Fig. 8.4.

If double integration is used, the moments of inertia can be calculated from Eqs. (9.2) in a straightforward manner. However, in single integration we must view Eqs. (9.2) in the form

###### Ix = dIx Iy = dIy

where dIx and dIy are the moments of inertia of the area element dA about the x- and y-axes. In general, dIx = y2dA only if all parts of the area element are the same distance y from the x-axis. To satisfy this condition, the area element must be either a double differential element (dA=dx dy), or a strip of width dy that is parallel to the x-axis, as shown in Fig. 8.4(c). A similar argument applies to dIy.

###### f. Method of composite areas

Consider a plane region that has been divided into the subregions 1, 2,

3, . . . . The moment of inertia of the area of about an axis can be computed by summing the moments of inertia of the subregions about the same axis. This technique, known as the method of composite areas, follows directly from the property of deﬁnite integrals: the integral of a sum equals the sum of the integrals. For example, Ix, the moment of inertia about the x-axis, becomes

###### Ix = y2 dA =

###### y2 dA +

###### y2 dA +

###### y2 dA + ···

1

2

3

which can be written as

###### Ix = (Ix)1 + (Ix)2 + (Ix)3 + ··· (9.10a)

where (Ix)i is the moment of the inertia of the area of the subregion i with respect to the x-axis. Obviously, the method of composite areas also applies to the computation of polar moments of areas:

###### JO = (JO)1 + (JO)2 + (JO)3 + ··· (9.10b)

where (JO)i is the polar moment of inertia of the subregion i with respect to point O.

The moments of inertia of the component areas about their centroidal axes can be found in tables, such as Tables 9.1 and 9.2. The parallel-axis theorem must then be used to convert these moments of inertia to the common axis before they can be summed.

|Rectangle<br><br>I¯x<br><br>Ix<br><br>= bh3 12<br><br>I¯y Iy<br><br>= b3h b3h<br><br>12<br><br>I¯xy Ixy<br><br>= 0<br><br>= bh3 3<br><br>=<br><br>3<br><br>= b2h2 4<br><br>h<br><br>b<br><br>b 2<br><br>h 2<br><br>x<br><br>y<br><br>C|Circle<br><br>Ix = Iy =<br><br>πR4 4<br><br>Ixy = 0<br><br>y<br><br>x<br><br>R<br><br>C|
|---|---|
|Right triangle<br><br>I¯x<br><br>Ix<br><br>= bh3 bh3<br><br>36<br><br>I¯y<br><br>Iy<br><br>= b3h b3h<br><br>36<br><br>¯ = −<br><br>72<br><br>=<br><br>12<br><br>=<br><br>12<br><br>Ixy<br><br>Ixy<br><br>= b2h2<br><br>b2h2<br><br>24<br><br>h<br><br>b<br><br>y<br><br>x<br><br>h 3<br><br>b 3<br><br>C|Ix Ix Iy<br><br>Semicircle<br><br>¯ = 0.1098R4 ¯ = 0<br><br>= = πR4 8<br><br>Ixy<br><br>Ixy<br><br>= 0<br><br>y<br><br>x<br><br>R<br><br>3π<br>4 R<br><br><br>C|
|Ix<br><br>Ix<br><br>Iy<br><br>Isosceles triangle<br><br>¯ = bh3 bh3<br><br>36<br><br>¯ = b3h 48<br><br>¯<br><br>= 12<br><br>Ixy = 0<br><br>Ixy = 0<br><br>h<br><br>x<br><br>h 3<br><br>y<br><br>b 2<br><br>b 2<br><br>C| |

###### Table 9.1 Inertial Properties of Plane Areas: Part 1

|Triangle<br><br>I¯x = bh3<br><br>36<br><br>Ix = bh3<br><br>12<br><br>I¯y = bh<br><br>36(a2 − ab + b2) Iy =<br><br>bh 12<br><br>(a2 + ab + b2)<br><br>I¯xy = bh2<br><br>72<br><br>(2a − b) Ixy =<br><br>bh2 24<br><br>(2a + b)<br><br>a<br><br>C<br><br>h<br><br>y<br><br>x b<br><br>|Half parabolic complement<br><br>I¯x = 37bh3<br><br>2100 Ix = bh3<br><br>21<br><br>I¯y = b3h 80<br><br><br>Iy =<br><br>b3h 5 I¯xy = b2h2<br><br>120 Ixy = b2h2<br><br>12<br><br>h<br><br>x<br><br>C<br><br>y<br><br>b<br><br>y=h(<br><br>x<br><br>b)<br><br>2|
|---|---|
|Quarter circle<br><br>I¯x = I¯y = 0.05488R4 Ix = Iy =<br><br>πR4 16<br><br>I¯xy = − 0.01647R4 Ixy =<br><br>R4 8<br><br>y<br><br>x R<br><br>C<br><br>R|Half parabola<br><br>I¯x = 8bh3<br><br>175<br><br>Ix =<br><br>2bh3 7<br><br>I¯y = 19b3h<br><br><br>480<br><br>Iy = 2b3h<br><br>15<br><br>I¯xy = b2h2<br><br>60<br><br>Ixy =<br><br>b2h2 6<br><br>h<br><br>y<br><br>x b<br><br>C<br><br>y=h(<br><br>x<br><br>b)<br><br>2|
|Quarter ellipse<br><br>I¯x = 0.05488ab3 Ix = π ab3<br><br>16<br><br>I¯y = 0.05488a3b Iy =<br><br><br>π a3b 16<br><br>I¯xy = − 0.01647a2b2 Ixy = a2b2<br><br>8<br><br>a<br><br>y<br><br>b<br><br>C<br><br>x<br><br>x2<br><br>+<br><br>y2<br><br>= 1 a2 b2|Circular sector<br><br>Ix = R4<br><br>8<br><br>(2α − sin 2α)<br><br>Iy = R4<br><br>8<br><br>(2α + sin 2α)<br><br>Ixy = 0<br><br>y<br><br>R<br><br>C x<br><br>α α|

###### Table 9.2 Inertial Properties of Plane Areas: Part 2

|Sample Problem 9.1<br><br>The centroid of the plane region is located at C. If the area of the region is 2000mm2 and its moment of inertia about the x-axis is Ix =40 × 106 mm4, determine Iu.<br><br>u<br><br>x<br><br>C<br><br>d2 = 70 mm d1 = 90 mm<br><br>Solution<br><br>Note that we are required to transfer the moment of inertia from the x-axis to the u-axis, neither of which is a centroidal axis. Therefore, we must ﬁrst calculate I¯x, the moment of inertia about the centroidal axis that is parallel to the x-axis. From the parallel-axis theorem we have Ix = I¯x + Ad12, which gives<br><br>I¯x = Ix − Ad12 = (40 × 106) − (2000)(90)2 = 23.8 × 106 mm4<br><br>After I¯x has been found, the parallel-axis theorem enables us to compute the moment of inertia about any axis that is parallel to the centroidal axis. For Iu we have<br><br>Iu = I¯x + Ad22 = (23.8 × 106) + (2000)(70)2<br><br>= 33.6 × 106 mm4 Answer<br><br>A common error is to use the parallel-axis theorem to transfer the moment of inertia between two axes, neither of which is a centroidal axis. In this problem, for example, it is tempting to write Iu = Ix + A(d1 + d2)2, which would result in an incorrect answer for Iu.<br><br>Sample Problem 9.2<br><br>For the rectangle, compute the following: (1) the moment of inertia about the<br><br>y<br><br>dy<br><br>b<br><br>h<br><br>| |
|---|
| |
|dA<br><br>|
<br><br>y<br><br>x O<br><br>x-axis by integration; (2) the moment of inertia about the centroidal axis that is parallel to the x-axis; and (3) the polar moment of inertia about the centroid.<br><br>Solution<br><br>Part 1<br><br>The area of the differential element shown in the ﬁgure is dA = bdy. Because all parts of the element are a distance y from the x-axis, we can use Eq. (9.2):<br><br>Ix = y2 dA = b<br><br>h<br><br>0<br><br>y2 dy =<br><br>by3 3<br><br>h<br><br>0<br><br>=<br><br>bh3 3<br><br>Answer|
|---|

|This result agrees with the information listed for a rectangle in Table 9.1.<br><br>If we had chosen to use double integration with dA=dx dy, the analysis would yield<br><br>Ix = y2 dA=<br><br>h<br><br>0<br><br>b<br><br>0<br><br>y2 dx dy =<br><br>bh3 3 which is identical to the previous result.<br><br>Part 2<br><br>We can calculate I¯x from the parallel-axis theorem and the result of Part 1.<br><br>Substituting Ix =bh3/3 into the parallel-axis theorem, and recognizing that the transfer distance d (the distance between the x-axis and the centroidal x-axis) is h/2, we ﬁnd that<br><br>I¯x = Ix − Ad2 =<br><br>bh3<br><br>3 − bh<br><br>h 2<br><br>2<br><br>=<br><br>bh3 12<br><br>Answer<br><br>This answer also agrees with the results in Table 9.1.<br><br>Part 3<br><br>One method of computing J¯C is to use J¯C = I¯x + I¯y. From the results of Part 2, or Table 9.1, we have<br><br>J¯C = I¯x + I¯y =<br><br>bh3<br><br>12 +<br><br>hb3<br><br>12 =<br><br>bh 12<br><br>(h2 + b2) Answer<br><br>Another method of computing J¯C is to ﬁrst compute JO = Ix + Iy and then transfer this result to the centroid. From the results of Part 1, we have<br><br>JO = Ix + Iy =<br><br>bh3<br><br>3 +<br><br>hb3<br><br>3 =<br><br>bh 3<br><br>(h2 + b2)<br><br>The transfer distance is the distance between point O and the centroid of the rectangle; that is, d = (b/2)2 + (h/2)2. From the parallel-axis theorem, we obtain<br><br>J¯C = JO − Ad2 =<br><br>bh 3<br><br>(h2 + b2) − bh<br><br>b2<br><br>4 +<br><br>h2<br><br>4 or<br><br>J¯C =<br><br>bh 12<br><br>(h2 + b2) Answer<br><br>which agrees with the previous result.|
|---|

|Sample Problem 9.3<br><br>By integration, calculate the moment of inertia about the y-axis of the area shown in Fig. (a) by the following methods: (1) single integration using a vertical differential area element; (2) double integration; and (3) single integration using a horizontal differential area element.<br><br>b<br><br>h<br><br>y<br><br>x<br><br>y = h(x/b)2<br><br>(a)<br><br>Solution<br><br>Part 1<br><br>The vertical differential area element is shown in Fig. (b). Because all parts of the element are the same distance x from the y-axis, we may use Eq. (9.2) directly. With dA = y dx = h(x/b)2 dx, we have<br><br>Iy = x2 dA =<br><br>h b2<br><br>b<br><br>0<br><br>x4 dx =<br><br>h b2<br><br>b5<br><br>5 =<br><br>b3h 5<br><br>Answer<br><br>which agrees with the information in Table 9.2 for the half parabolic complement.<br><br>x<br><br>y<br><br>x<br><br>(b)<br><br>y<br><br>dx<br><br>y = h(x/b)2<br><br>h<br><br>Part 2<br><br>Equation (9.2) can also be used with the double differential area element dA = dy dx. Choosing to integrate on y ﬁrst, we obtain<br><br>Iy = x2 dA =<br><br>b<br><br>0<br><br>h(x/b)2<br><br>0<br><br>x2 dy dx|
|---|

|Integrating over x ﬁrst would yield<br><br>Iy = x2 dA =<br><br>h<br><br>0<br><br>b(y/h)1/2<br><br>0<br><br>x2 dx dy<br><br>Performing either of the foregoing integrations yields the same expression for Iy as found in Part 1.<br><br>Part 3<br><br>The horizontal differential area element is shown in Fig. (c). Because all parts of the differential area element are not the same distance from the y-axis, Eq. (9.2) cannot be applied directly. To ﬁnd Iy for the entire area, we must integrate dIy, the moment of inertia of the differential area element about the y-axis.<br><br>x<br><br>y<br><br>y<br><br>x<br><br>(c)<br><br>b – x<br><br>dy<br><br>Cel<br><br>x + b – x = b + x<br><br>2 2<br><br>Table 9.1 lists I¯y = hb3/12 for a rectangle. Therefore, the moment of inertia of the differential element about its vertical centroidal axis (axis parallel to the y-axis passing through the centroid Cel of the element) is dI¯y =dy (b − x)3/12. According to the parallel-axis theorem, dIy =dI¯y + dA(del2), where del is the distance between the y-axis and the vertical centroidal axis of the element. Using del =(b + x)/2, as shown in Fig. (c), and integrating, we obtain Iy for the entire area:<br><br>Iy = dIy =<br><br>h<br><br>0<br><br>dy (b − x)3<br><br>12 + (b − x) dy<br><br>b + x 2<br><br>2<br><br>Substituting x =b(y/h)1/2 and completing the integration gives the same result as found in Part 1.<br><br>Obviously, the horizontal differential area element is not as convenient as the other choices in this problem.|
|---|

|Sample Problem 9.4<br><br>For the area shown in Fig. (a), calculate the radii of gyration about the x- and<br><br>20<br><br>45<br><br>100<br><br>y<br><br>x (a)<br><br>Dimensions in mm<br><br>y-axes.<br><br>Solution<br><br>We consider the area to be composed of the three parts shown in Figs. (b)–(d): a triangle, plus a semicircle, minus a circle. The moments of inertia of each part are obtained in two steps. First, the moments of inertia about the centroidal axes of the part are found from Table 9.1. The parallel-axis theorem is then used to calculate the moments of inertia about the x- and y-axes.<br><br>y<br><br>x (b)<br><br>100<br><br>90 x = 23 (90) = 60<br><br>y = 23 (100) = 66.7<br><br>C<br><br>45<br><br>100<br><br>y<br><br>x (c)<br><br>y = 100 + = 119.1<br><br>4(45) 3π<br><br>x = 45<br><br>C<br><br>20<br><br>y = 100<br><br>y<br><br>x (d)<br><br>x = 45<br><br>C<br><br>Triangle<br><br>A =<br><br>bh<br><br>2 =<br><br>90(100) 2 = 4500 mm2<br><br>I¯x =<br><br>bh3<br><br>36 =<br><br>90(100)3 36 = 2.50 × 106 mm4<br><br>Ix = I¯x + Ay¯2 = (2.50 × 106) + (4500)(66.7)2 = 22.52 × 106 mm4<br><br>I¯y =<br><br><br>hb3<br><br>36 =<br><br>100(90)3 36 = 2.025 × 106 mm4<br><br>Iy = I¯y + Ax¯2 = (2.025 × 106) + (4500)(60)2 = 18.23 × 106 mm4<br><br>Semicircle<br><br>A =<br><br>π R2<br><br>2 =<br><br>π(45)2<br><br>2 = 3181 mm2<br><br>I¯x = 0.1098R4 = 0.1098(45)4 = 0.450 × 106 mm4 Ix = I¯x + Ay¯2 = (0.450 × 106) + (3181)(119.1)2 = 45.57 × 106 mm4<br>I¯y =<br><br><br>π R4<br><br>8 =<br><br>π(45)4<br><br>8 = 1.61 × 106 mm4<br><br>Iy = I¯y + Ax¯2 = (1.61 × 106) + (3181)(45)2 = 8.05 × 106 mm4|
|---|

|Circle<br><br>A = π R2 = π(20)2 = 1257 mm2<br><br>I¯x =<br><br>π R4<br><br>4 =<br><br>π(20)4<br><br>4 = 0.1257 × 106 mm4<br><br>Ix = I¯x + Ay¯2 = (0.1257 × 106) + (1257)(100)2 = 12.70 × 106 mm4<br><br>I¯y =<br><br><br>π R4<br><br>4 =<br><br>π(20)4<br><br>4 = 0.1257 × 106 mm4<br><br>Iy = I¯y + Ax¯2 = (0.1257 × 106) + (1257)(45)2 = 2.67 × 106 mm4<br><br>Composite Area<br><br>To determine the properties for the composite area, we superimpose the foregoing results (taking care to subtract the quantities for the circle) and obtain<br><br>A = A = 4500 + 3181 − 1257 = 6424 mm2 Ix = Ix = (22.52 + 45.57 − 12.70) × 106 = 55.39 × 106 mm4 Iy = Iy = (18.23 + 8.05 − 2.67) × 106 = 23.61 × 106 mm4<br><br>Therefore, for the radii of gyration we have<br><br>kx =<br><br>Ix A =<br><br>55.39 × 106 6424 = 92.9 mm Answer<br><br>ky =<br><br><br>Iy A =<br><br>23.61 × 106 6424 = 60.6 mm Answer<br><br>Sample Problem 9.5<br><br>Using numerical integration, calculate the moments of inertia about the x- and<br><br>b<br><br>h<br><br>y<br><br>x<br><br>y = h(x/b)2<br><br>b 4<br><br>y-axes for the half parabolic complement. Use Simpson’s rule with four panels. Compare your results with the exact values in Table 9.2.<br><br>Solution<br><br>Dividing the range of integration into four panels, each of width x = b/4, Simpson’s rule becomes (see Appendix A)<br><br>b<br><br>0<br><br>f (x) dx ≈<br><br>b/4 3<br><br>( f1 + 4 f2 + 2 f3 + 4 f4 + f5) (a)<br><br>The integrals to be evaluated are Ix = dIx and Iy = dIy. Choosing a vertical strip of width dx and height y as the differential area element, we have<br><br>dIx = 13 y3dx (moment of inertia of a rectangle about its base) dIy = x2dA = x2y dx (all parts of the area element dA = y dx are at the distance<br><br>x from the y-axis)|
|---|

|Therefore,<br><br>Ix =<br><br>b<br><br>0<br>1<br><br><br>3<br><br>y3 dx ≈<br><br>b 12<br><br>y13 3 + 4<br><br>y23 3 + 2<br><br>y33 3 + 4<br><br>y43 3 +<br><br>y53 3<br><br>(b)<br><br>Iy =<br><br>b<br><br>0<br><br>x2y dx ≈<br><br>b 12<br><br>x12y1 + 4x22y2 + 2x32y3 + 4x42y4 + x52y5 (c)<br><br>where yi = h(xi/b)2. The terms on the right-hand side of Eqs. (b) and (c) are evaluated in the following table.<br><br>i x y y3/3 x2y<br><br>1 0.00 0.0000 0.00000 0.00000<br>2 0.25b 0.0625h 0.00008h3 0.00391b2h<br>3 0.50b 0.2500h 0.00521h3 0.06250b2h<br>4 0.75b 0.5625h 0.05933h3 0.31641b2h<br>5 1.00b 1.0000h 0.33333h3 1.00000b2h<br><br><br>Substituting the values from this table into Eqs. (b) and (c) gives<br><br>Ix =<br><br>bh3<br><br>12 [1(0) + 4(0.00008) + 2(0.00521) + 4(0.05933)]<br><br>+ 1(0.33333)] = 0.0485bh3 Answer<br><br>Iy =<br><br>b3h<br><br>12 [1(0) + 4(0.00391) + 2(0.06250) + 4(0.31641)]<br><br>+ 1(1.00000)] = 0.2005b3h Answer<br><br>According to Table 9.2, the half parabolic complement has Ix = bh3/21 = 0.0476bh3 and Iy = b3h/5 = 0.2000b3h. Therefore, the errors introduced by our numerical integration are 1.9% for Ix and 0.25% for Iy.|
|---|

![image 67](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile67.png>)

###### Problems

y=50 + –4 x 9.1 Compute the moment of inertia of the shaded region about the y-axis by

9 y

integration.

- 9.2 The properties of the plane region are J¯C =50 × 103 mm4, Ix =600 × 103 mm4, and Iy =350 × 103 mm4. Calculate A, I¯x, and I¯y for the region.

y

x

C

30 mm

40 mm

x

Area = A

C

300 mm

u

h

Fig. P9.2 Fig. P9.3, P9.4

- 9.3 The moments of inertia about the x- and u-axes of the plane region are

Ix =14×109 mm4 and Iu =38 × 109 mm4, respectively. If h =200 mm, determine the area of the region, and the radius of gyration about the centroidal axis parallel to the x-axis.

- 9.4 Find the distance h for which the moment of inertia of the plane region

90 mm

50 mm

x

90 mm

Fig. P9.1

about the u-axis equals 120×109 mm4, given that A =90×103 mm2 and Ix =14× 109 mm4.

y 9.5 Using integration, ﬁnd the moment of inertia and the radius of gyration

about the x-axis for the thin ring (t R). 9.6 Use integration to determine the moment of inertia of the shaded region about the x-axis.

t

R

x

Fig. P9.5

y

x=10–2.5y2

2 in.

x

10 in.

###### Fig. P9.6

- 9.7 Compute Ix for the shaded region using integration.

O x

y

4 in.

4 in. 8 in.

y2 = 2x

O

y

x

R

α α

Fig. P9.7 Fig. P9.8

- 9.8 Using integration, compute the polar moment of inertia about point O for the circular sector. Check your result with Table 9.2.
- 9.9 Use integration to compute Ix and Iy for the parabola. Check your answers b

h

x

y = h(x/b)2

y

Fig. P9.9

with the results for the half parabolic complement in Table 9.2.

- 9.10 By integration, determine the moments of inertia about the x- and y-axes

y = x2

y = x

1 m

y

x

Fig. P9.10

for the region shown.

- 9.11 Compute the moment of inertia about the x-axis for the region shown using

y

x 20 in.

12 in.

y = 12 cos

40

πx

Fig. P9.11, P9.12

integration.

- 9.12 By integration, ﬁnd the moment of inertia about the y-axis for the region shown.
- 9.13 Figure (a) shows the cross section of a column that uses a structural shape known as W8 × 67 (wide-ﬂange beam, nominally 8 in. deep, weighing 67lb/ft). The American Institute of Steel Construction Structural Steel Handbook lists the following cross-sectional properties: A =19.7 in.2, I¯x =272 in.4, and I¯y =88.6 in.4 Determine the dimensions of the rectangle in Fig. (b) that has the same I¯x and I¯y as a W8 × 67 section.

y

y

0.933 in.

Web

h C x

9 in. C x

0.575 in.

Flange

b

8.287 in.

(a) (b)

###### Fig. P9.13–P9.15

- 9.14 Compute the dimensions of the rectangle shown in Fig. (b) that has the

same k¯x and k¯y as the W8 × 67 section in Fig. (a). (See Prob. 9.13 for properties of W8 × 67.)

Problems 9.15–9.29 are to be solved using the method of composite areas.

- 9.15 Compute I¯x and I¯y for the W8 × 67 shape dimensioned in the ﬁgure. Assume that the section is composed of rectangles, neglecting the effects due to rounding of the corners. Compare your results with the handbook values listed in Prob. 9.13.
- 9.16 Figure (a) shows the cross-sectional dimensions for the structural steel section known as C10 × 20 (channel with a nominal depth of 10in., weighing 20lb/ft). The American Institute of Steel Construction Structural Steel Handbook lists the following properties for the cross section: A =5.88 in.2, I¯x =78.9 in.4, and I¯y =2.81 in.4 If two of these channels are welded together as shown in Fig. (b), ﬁnd I¯x and I¯y for the resulting cross section.

2.739 in.

0.379 in.

y

y 0.606 in.

C C x x

(a) (b)

10 in.

Fig. P9.16

- 9.17 A W8 × 67 section is joined to a C10 × 20 section to form a struc-

tural member that has the cross section shown. Calculate I¯x and I¯y for this cross section. (See Probs. 9.13 and 9.16 for the properties of the structural sections.)

y

x

###### Fig. P9.17

- 9.18 Compute Ix and Iy for the region shown.

66 mm 66 mm

40 mm 40 mm

x

y

68 mm

Fig. P9.18

- 9.19 Find I¯x and I¯y for the region shown.

y

9 in.

5 in.

2 in.

2 in.

7 in.

x

1 in.

Fig. P9.19

- 9.20 Calculate I¯x for the shaded region, knowing that y¯ =68.54 mm. 60

30

90

20

25

80

Dimensions in mm

y

x

Fig. P9.20, P9.21

- 9.21 Compute I¯y for the region shown, given that x¯ =25.86 mm.
- 9.22 Compute I¯x for the region shown.

2 2

2

2 x

y

Dimensions in inches

8 8

18 5 5

30

30

15

y

x

Dimensions in mm

Fig. P9.22 Fig. P9.23

- 9.23 For the plane region with a circular cutout, (a) ﬁnd Ix; and (b) compute I¯x x

y

3 in.

2 in.

4 in. 4 in.

Fig. P9.24

using the result of part (a) and the parallel-axis theorem.

- 9.24 Determine I¯x for the triangular region shown.

- 9.25 Determine the distance h for which the moment of inertia of the region shown about the x-axis will be as small as possible.

h

x

y

O 4 ft

1 ft 1 ft 1 ft 1 ft

x

y

d

R/2

R

Fig. P9.25 Fig. P9.26

- 9.26 A circular region of radius R/2 is cut out from the circular region of radius

R as shown. For what distance d will kx for the new region be the same as kx for the region before the cutout was removed?

- 9.27 Determine Ix and Iy for the region shown. Note that the region is symmetric about the x-axis.

y

x

68 mm

17 mm

- 17 mm
- 18 mm

27 mm

Fig. P9.27

- 9.28 Determine the ratio a/b for which I¯x = I¯y for the isosceles triangle.

y

a a C

x

b

###### Fig. P9.28

- 9.29 As a round log passes through a sawmill, two slabs are cut off, resulting

h

h

x

R

Fig. P9.29

in the cross section shown. Calculate Ix of the cross section if h = R/2. What is the percentage reduction in Ix caused by the sawing operation?

- 9.30 For the circular sector shown in Table 9.2, determine the angle α, other than α =0 and α =π, for which I¯x = I¯y.
- 9.31 By numerical integration, compute the moments of inertia about the xand y-axes for the region shown. The region is symmetric with respect to each coordinate axis.

24

6

x

y

Dimensions in inches

24.00

22.16

16.97

9.18

Fig. P9.31

- 9.32 Use numerical integration to compute the moments of inertia about the xand y-axes for the symmetric region shown.

120

20

77

y

x

60 46

35 27

22 20

Dimensions in mm

Fig. P9.32

- 9.33 The plane region is submerged in a ﬂuid of weight density γ. The resul-

a a

h

C

tant force of the ﬂuid pressure on the region is R acting at the point C (called the pressure center) located at the distance h below the surface of the ﬂuid. Show that R =γ Qa and h = Ia/Qa, where Qa and Ia are the ﬁrst and second moments of

Region

about the axis a–a.

Fig. P9.33

###### 9.3 Products of Inertia of Areas

###### a. Deﬁnition

The product of inertia of a plane area (also called the product of area) about the x- and y-coordinate axes is deﬁned by

###### Ixy = xy dA (9.11)

Plane region

y where A is the area of the plane region shown in Fig. 9.3, and x and y are the

coordinates of dA.

dA

x

The dimension of product of inertia is [L4], the same as for moment of inertia and polar moment of area. Whereas moment of inertia is always positive, the product of inertia can be positive, negative, or zero, depending on the manner in which the area is distributed in the xy-plane.

y

To further explore the signs for product of inertia, consider the plane region

x

O

shown in Fig. 9.4. The region lies in the ﬁrst quadrant of the xy-coordinate system. Because both x and y are positive for every differential area element dA, Ixy = xy dA is clearly positive. However, relative to the uv-coordinate system, the region lies in the fourth quadrant, so that the u-coordinate of each dA is positive and the v-coordinate is negative. Therefore, Iuv = uv dA is negative.

Fig. 9.3

u Plane region

y

dA

x

y

v θ

x

y

O

###### Fig. 9.4

dA dA

Note that the uv-axes in Fig. 9.4 are rotated counterclockwise through the angle θ relative to the xy-axes. Because Ixy is positive and Iuv is negative, there must be an orientation of the axes for which the product of inertia is zero. As we see in the next article, the axes of zero product of inertia play a fundamental role in the calculation of the maximum and minimum moments of inertia.

x

– x x

Next, consider a region that has an axis of symmetry, such as that shown in Fig. 9.5. Because the y-axis is the axis of symmetry, for every dA with coordinates

###### Fig. 9.5

(x, y), there is a dA with coordinates (−x, y). Therefore, xy dA = 0 when the integration is performed over the entire region. Consequently, we have the following property:

If an area has an axis of symmetry, that axis and the axis perpendicular to it constitute a set of axes for which the product of inertia is zero.

9.3 Products of Inertia of Areas 493

###### b. Parallel-axis theorem

The parallel-axis theorem for products of inertia can be derived by considering the plane region shown in Fig. 9.6. We let x and y be axes through the centroid C and parallel to the x- and y-axes. The coordinates of C relative to the xy-axes are x¯ and y¯. Using x = x + x¯ and y = y + y¯ in Eq. (9.11), we obtain

Ixy = xy dA = (x + x¯)(y + y¯) dA

= x y dA + x¯ y dA + y¯ x dA + x¯y¯ dA

y

x

y'

Plane region

dA

x'

y'

C

x

x'

y

y

x

O

###### Fig. 9.6

The ﬁrst term on the right-hand side is the product of inertia with respect to the centroidal axes, which we denote with I¯xy. The middle two terms are zero, because each integral represents the ﬁrst moment of the area about a centroidal axis. The integral in the last term is simply the area A. Therefore, the parallel-axis theorem for products of inertia can be written as

Ixy = I¯xy + Ax¯y¯ (9.12)

To reiterate, the symbol I¯xy is to be read as “the product of inertia relative to centroidal x- and y-axes” (axes through the centroid and parallel to the x- and y-axes).

It should be evident that the method of composite areas is also valid for products of inertia. Tables 9.1 and 9.2 list the products of inertia for common shapes, which can be utilized in the method of composite areas.

|Sample Problem 9.6<br><br>Calculate the product of inertia of the triangle shown in Fig. (a) about the x- and<br><br>y<br><br>x b<br><br>(b)<br><br>h<br><br>y<br><br>dy<br><br>x<br><br>y<br><br>x b (c)<br><br>h<br><br>x dx<br><br>y<br><br><br>y-axes using (1) single integration; and (2) double integration.<br><br>y<br><br>x b<br><br>(a)<br><br>h<br><br>Solution<br><br>Part 1<br><br>By deﬁnition, Ixy = xy dA, where x and y are the coordinates of the differential area element dA = dy dx. However, this formula does not apply to single integration, where we must integrate dIxy, the product of inertia of the differential area element. To ﬁnd dIxy, the parallel-axis theorem for products of inertia, Ixy = I¯xy + Ax¯y¯, must be interpreted as dIxy = dI¯xy +dA x¯ely¯el, where dI¯xy is the product of inertia of dA about its centroidal axes, and x¯el and y¯el are the centroidal coordinates of the area element.<br><br>The analysis then proceeds as follows:<br><br>Horizontal element shown in Fig. (b) Vertical element shown in Fig. (c)<br><br>dA = x dy dA = y dx<br><br>x¯el =<br><br>x 2 x¯el = x<br><br>y¯el = y y¯el =<br><br><br>y 2<br><br>dI¯xy = 0 (by symmetry) dI¯xy = 0 (by symmetry) dIxy = dA x¯ely¯el dIxy = dA x¯ely¯el<br><br>= (x dy)<br><br>x 2<br><br>(y) = (y dx)(x)<br><br>y 2<br><br>=<br><br>x2y 2<br><br>dy =<br><br>xy2 2<br><br>dx<br><br>Substitute x =<br><br>b h<br><br>(h − y) and integrate Substitute y =<br><br>h b<br><br>(b − x) and integrate<br><br>Ixy =<br><br>b2 2h2<br><br>h<br><br>0<br><br>(h − y)2y dy Ixy =<br><br>h2 2b2<br><br>b<br><br>0<br><br>x(b − x)2 dx<br><br>Ixy =<br><br>b2h2 24<br><br>Answer Ixy =<br><br>b2h2 24<br><br>Answer These results agree with the information listed for the triangle in Table 9.1.|
|---|

|Part 2<br><br>Using double integration with dA = dx dy, we use Ixy = xy dA. Choosing to integrate on y ﬁrst, we have<br><br>Ixy =<br><br>b<br><br>0<br><br>(h/b)(b−x)<br><br>0<br><br>xy dy dx<br><br>Integrating on x ﬁrst would yield<br><br>Ixy =<br><br>h<br><br>0<br><br>(b/h)(h−y)<br><br>0<br><br>xy dx dy<br><br>Evaluating either of the above integrals yields Ixy = b2h2/24, as in Part 1.<br><br>Sample Problem 9.7<br><br>Using the results of Sample Problem 9.6, calculate I¯xy, the product of inertia of the triangle shown about centroidal axes parallel to the x- and y-axes.<br><br>y<br><br>x b<br><br>h<br><br>C<br><br>3<br><br>b<br><br>h 3<br><br>Solution<br><br>From the solution to Sample Problem 9.6, we have Ixy = b2h2/24. The parallelaxis theorem yields<br><br>I¯xy = Ixy − Ax¯y¯ =<br><br>b2h2<br><br>24 −<br><br>bh 2<br><br>b 3<br><br>h 3<br><br>which simpliﬁes to<br><br>I¯xy = −<br><br>b2h2 72<br><br>Answer<br><br>The above result agrees with the information in Table 9.1 for the right triangle.|
|---|

###### 495

|Sample Problem 9.8<br><br>Calculate the product of inertia Ixy for the angle shown in Fig. (a) by the method of composite areas.<br><br>20<br><br>140<br><br>180<br><br>20<br><br>x<br><br>y<br><br>Dimensions in mm<br><br>(a)<br><br>Solution<br><br>We may view the angle as the composite of the two rectangles shown in Fig. (b). For each rectangle, Ixy can be computed using the parallel-axis theorem for products of inertia: Ixy = I¯xy + Ax¯y¯. Note that I¯xy = 0 for each rectangle, by symmetry.<br><br>For the 20mm × 140mm rectangle,<br><br>Ixy = 0 + (140 × 20)(10)(70) = 1.96 × 106 mm4 For the 160mm × 20mm rectangle,<br><br>Ixy = 0 + (160 × 20)(100)(10) = 3.20 × 106 mm4 Therefore, the product of inertia for the angle is<br><br>Ixy = Ixy = (1.96 + 3.20) × 106 = 5.16 × 106 mm4 Answer<br><br>(b)<br><br>140<br><br>x<br><br>y<br><br>20<br><br>x = 10 y = 70 x = 100 y = 10<br><br>x<br><br>20<br><br>20 160<br><br>y<br><br>|
|---|

![image 68](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile68.png>)

###### Problems

- 9.34 Use integration to verify the formula given in Table 9.2 for Ixy of a half parabolic complement.
- 9.35 For the quarter circle in Table 9.2, verify the following formulas: (a) Ixy by integration; and (b) I¯xy using the formula for Ixy and the parallel-axis theorem.
- 9.36 Determine the product of inertia with respect to the x- and y-axes for the quarter circular, thin ring (t R) by integration.

R

t

x

y

Fig. P9.36

- 9.37 The product of inertia of triangle (a) with respect to its centroid is I¯xy = −b2h2/72. What is I¯xy for triangles (b)–(d)? (Hint: Investigate the signs in the expression I¯xy = Ixy − Ax¯y¯.)

b

b b

h

h h

h

y

y y

y

x

x x

x (a)

b (b)

(c) (d)

Fig. P9.37

- 9.38 Calculate Iuv for the region shown, given that x¯ = 30 mm, d = 40 mm,

y

x, u

C

A = 400 mm2

40 mm

v

x

d

Fig. P9.38, P9.39

and Ixy = 520 × 103 mm4.

- 9.39 For the region shown, Ixy = 320 × 103 mm4 and Iuv = 0. Compute the distance d between the y- and v-axes. (Note: The result is independent of x¯.)

###### Problems 9.40–9.47 are to be solved using the method of composite areas.

- 9.40 Compute the product of inertia with respect to the x- and y-axes.

20

Dimensions in mm

x

y

60

60

60 60

30

30

Fig. P9.40

- 9.41 Calculate the product of inertia with respect to the x- and y-axes.

y

9.42 Find I¯xy for the region shown.

R

- 9.43 Determine I¯xy for the plate with parabolic cutouts.

6 in.

10 in.

7 in. 9 in.

6 in.

10 in.

9 in. 7 in.

y

x

Parabola

Parabola

16.5

26.5

80

60

10

10

x

y

Dimensions in mm

C

Fig. P9.43 Fig. P9.44

- 9.44 The ﬁgure shows the cross section of a standard L80 × 60 × 10-mm structural steel, unequal angle section. Neglecting the effects of the small corner ﬁllets, compute Ixy of the cross-sectional area.

R

x

Fig. P9.41

160

40

160

Dimensions 40 in mm

y

40

x

160

Fig. P9.42

- 9.45 Calculate I¯xy for the region shown, knowing that x¯ = 25.86mm and y¯ = 68.54mm.

60

90

20

25

80

Dimensions in mm

y

x

30

Fig. P9.45

- 9.46 Compute I¯xy for the region shown.

x

y

12 in.

6 in.

18 in.

Fig. P9.46

- 9.47 Determine I¯xy for the region shown.

x

y

12 in.

Parabola

6 in.

18 in.

Fig. P9.47

- 9.48 Use numerical integration to compute the product of inertia of the region shown with respect to the x- and y-axes.

185

185

185

185

218

392

420

406

x

y

Dimensions in mm

338

Fig. P9.48

- 9.49 Determine the dimension b of the square cutout so that Ixy = 0 for the

y

5.6 in. 5.6 in.

b b

5.6 in.

x

|in.| |
|---|---|
| |4.2 in.|

5.6 in.

4.2

###### region shown. Fig. P9.49

9.4 Transformation Equations and Principal

Moments of Inertia of Areas

In general, the values of Ix, Iy, and Ixy for a given plane area depend on the location of O (the origin of the coordinate system) and the orientation of the xy-axes. The effect of relocating O, which is equivalent to translating the coordinate axes, has been studied and has resulted in the parallel-axis theorem. Here we investigate the changes in the moments and product of inertia caused by varying the orientation of the coordinate axes. This in turn enables us to determine the maximum and minimum moments of inertia associated with point O and ﬁnd the orientation of the corresponding axes.

a. Transformation equations for moments

and products of inertia

Consider the plane region with area A shown in Fig. 9.7, where the uv-axes at point O are obtained by rotating the xy-axes counterclockwise through the angle θ. We now derive formulas for Iu, Iv, and Iuv in terms of Ix, Iy, Ixy, and θ. These formulas are known as the transformation equations for moments and products of inertia.* We start with the transformation equations of the position coordinates, which can be derived from Fig. 9.7:

- u = y sinθ + x cosθ
- v = y cosθ − x sinθ

(9.13)

y

v

u ysinθ

xcosθ

Plane region

x dA

x sinθ

θ

y

u

y cos

v

θ

θ

x

O

###### Fig. 9.7

Substituting these equations into the deﬁning equation for Iu, we have

Iu = v2 dA = (y cosθ − x sinθ)2 dA

= cos2 θ y2 dA − 2sinθ cosθ xy dA + sin2 θ x2 dA

*Several other physical quantities—for example, stress and strain—obey transformation equations identical to those for moment of inertia.

###### 9.4 Transformation Equations and Principal Moments of Inertia of Areas 501

Identifying the moments and products of inertia, this equation becomes

Iu = Ix cos2 θ − 2Ixy sinθ cosθ + Iy sin2 θ (9.14) The equations for Iv and Iuv may be derived in a similar manner, the results being

###### Iv = Ix sin2 θ + 2Ixy sinθ cosθ + Iy cos2 θ (9.15) Iuv = (Ix − Iy)sinθ cosθ + Ixy(cos2 θ − sin2 θ) (9.16)

The equation for Iv could also be derived by replacing θ with (θ + 90◦) in Eq. (9.14).

Using the trigonometric identities

sin2θ = 2sinθ cosθ cos2θ = cos2 θ − sin2 θ cos2 θ = 12(1 + cos2θ) sin2 θ = 12(1 − cos2θ)

Eqs. (9.14)–(9.16) can also be written in the form

Iu = 12(Ix + Iy) + 12(Ix − Iy)cos2θ − Ixy sin2θ Iv = 12(Ix + Iy) − 12(Ix − Iy)cos2θ + Ixy sin2θ

- (9.17)
- (9.18)
- (9.19)

Iuv = 12(Ix − Iy)sin2θ + Ixy cos2θ

From Eqs. (9.17) and (9.18) we see that Iu+Iv = Ix+Iy, a result that we expected, because both sides of the equation are equal to JO, the polar moment of the area about O.

###### b. Principal moments of inertia

The maximum and minimum moments of inertia at a point are called the principal moments of inertia at that point. The axes about which the moments of inertia are maximum or minimum are called the principal axes, and the corresponding directions are referred to as principal directions. To ﬁnd the maximum and minimum moments of inertia, we set the derivative of Iu in Eq. (9.17) equal to zero:

###### dIu dθ = −(Ix − Iy)sin2θ − 2Ixy cos2θ = 0

Solving for 2θ, we obtain

2Ixy Ix − Iy

(9.20)

tan2θ = −

Note that there are two solutions for the angle 2θ that differ by 180◦ or, equivalently, two solutions for θ that differ by 90◦. We denote these solutions by θ1 and θ2. From the graphical representations shown in Fig. 9.8 we ﬁnd that

Ixy R cos2θ1,2 = ±

sin2θ1,2 = ∓

(9.21)

Ix − Iy 2R

where

2

Ix − Iy 2

###### + Ixy2 (9.22)

R =

The angles θ1 and θ2, measured counterclockwise from the x-axis, deﬁne the principal directions. Substituting Eq. (9.22) into Eq. (9.17) and simplifying, we obtain the principal moments of inertia

Ix + Iy

2 ± R (9.23)

I1,2 =

where I1 and I2 correspond to the axes deﬁned by θ1 and θ2, respectively.* In Eqs. (9.21) and (9.23), the upper sign of either ± or ∓ is to be used with θ1 and the lower sign with θ2 (refer to Fig. 9.8).

R

R

–Ixy

Ixy

2θ1 2θ2

Ix – Iy 2

Ix – Iy 2

–

Solution 1

Solution 2

###### Fig. 9.8

To determine the product of inertia with respect to the principal axes, we substitute Eqs. (9.21) into Eq. (9.19), which yields

Ix − Iy

Ix − Iy

Ixy R + Ixy ±

2R = 0 Therefore, the product of inertia with respect to the principal axes is zero.

2 ∓

=

Iuv θ=θ

1,2

The properties of an area, in general, depend on the location of the origin O of the xy-coordinate system. Therefore, the principal moments of inertia and principal directions vary with the location of point O. However, most practical applications, such as those found in structural engineering, are concerned with moments of inertia with respect to centroidal axes.

*It can be shown that I1 and I2 are the two values of I that are the roots of the following quadratic equation.

Ix − I −Ixy −Ixy Iy − I = 0

|Sample Problem 9.9<br><br>For the region shown in Fig. (a), calculate (1) the centroidal principal moments of inertia and the principal directions; and (2) the moments and product of inertia about the uv-axes through the centroid C.<br><br>50°<br><br>u v<br><br>x<br><br>C<br><br>160<br><br>200<br><br>30<br><br>30<br><br>y<br><br>(a)<br><br>Dimensions in mm<br><br>Solution<br><br>Centroidal Properties<br><br>The table below lists the computations that have been used to determine the cen-<br><br>|1|50°<br><br>u<br><br>C|
|---|---|
| |2|
<br><br>v<br><br>x 130<br><br>200<br><br>30<br><br>y<br><br>(b)<br><br>30<br><br>y = 66.52<br><br>x = 46.52<br><br>troidal coordinates and the inertial properties with respect to the x- and y-axes. The region is considered as a composite of the two rectangles shown in Fig. (b). Their moments of inertia have been calculated using Table 9.1.<br><br>The centroidal coordinates, shown in Fig. (b), are computed from the results in Table 9.1 as follows:<br><br>x¯ =<br><br>Ax¯ A =<br><br>460.5 × 103 9900 = 46.52 mm<br><br>y¯ =<br><br><br>Ay¯ A =<br><br>685.5 × 103 9900 = 66.52 mm<br><br>|Part<br><br>|A (mm2)|x¯ (mm)<br><br>|Ax¯ (mm3)|y¯ (mm)<br><br>|Ay¯ (mm3)<br><br>|Ix (mm4)|Iy (mm4)<br><br>|Ixy = I¯xy + Ax¯ y¯ (mm4)|
|---|---|---|---|---|---|---|---|---|
||1<br><br>|= 6000| |×| |×|3 = 80.00×106|3 = 1.800×106<br><br>|+<br><br>= 9.00×106|
|---|---|---|---|---|---|---|---|---|
| ||2|= 3900<br><br>130(30)<br><br>| |×| |×|3 = 1.17×106<br><br>|12 +3900(95)2<br><br>= 40.69×106|+<br><br>= 5.56×106|
|---|---|---|---|---|---|---|---|---|
| |9900<br><br>|···<br><br>|460.5×103<br><br>|···|658.5×103<br><br>|81.17×106|42.49×106|14.56×106|
|95<br><br>|370.5 103<br><br>|15|58.5 103<br><br>|130(30)3<br><br>|30(130)3<br><br>|0 3900(95)(15)|
|200(30)|15|90 103<br><br>|100|600 103<br><br>|30(200)3<br><br>|200(30)3<br><br>|0 6000(15)(100)|
<br><br>|1<br><br>|= 6000| |×| |×|3 = 80.00×106|3 = 1.800×106<br><br>|+<br><br>= 9.00×106|
|---|---|---|---|---|---|---|---|---|
| ||2|= 3900<br><br>130(30)<br><br>| |×| |×|3 = 1.17×106<br><br>|12 +3900(95)2<br><br>= 40.69×106|+<br><br>= 5.56×106|
|---|---|---|---|---|---|---|---|---|
| |9900<br><br>|···<br><br>|460.5×103<br><br>|···|658.5×103<br><br>|81.17×106|42.49×106|14.56×106|
|95<br><br>|370.5 103<br><br>|15|58.5 103<br><br>|130(30)3<br><br>|30(130)3<br><br>|0 3900(95)(15)|
<br><br>|2|= 3900<br><br>130(30)<br><br>| |×| |×|3 = 1.17×106<br><br>|12 +3900(95)2<br><br>= 40.69×106|+<br><br>= 5.56×106|
|---|---|---|---|---|---|---|---|---|
| |9900<br><br>|···<br><br>|460.5×103<br><br>|···|658.5×103<br><br>|81.17×106|42.49×106|14.56×106|
|
|---|

|The parallel-axis theorem is then used to calculate the inertial properties about the centroidal axes.<br><br>I¯x = Ix − Ay¯2 = (81.17 × 106) − (9900)(66.52)2<br><br>= 37.36 × 106 mm4<br><br>I¯y = Iy − Ax¯2 = (42.49 × 106) − (9900)(46.52)2<br><br>= 21.07 × 106 mm4 I¯xy = Ixy − Ax¯y¯ = (14.56 × 106) − (9900)(46.52)(66.52)<br><br>= −16.08 × 106 mm4<br><br>Part 1<br><br>Substituting the values for I¯x, I¯y, and I¯xy into Eq. (9.22) yields<br><br>R = 106<br><br>37.36 − 21.07 2<br><br>2<br><br>+ (−16.08)2 = 18.03 × 106 mm4<br><br>Therefore Eq. (9.23) becomes<br><br>I1,2 =<br><br>37.36 + 21.07 2 ± 18.03 × 106 = (29.22 ± 18.03) × 106 mm4<br><br>from which we obtain the principal moments of inertia<br><br>I1 = 47.3 × 106 mm4 I2 = 11.2 × 106 mm4 Answer<br><br>For the principal directions, Eqs. (9.21) yield<br><br>sin2θ1,2 = ∓<br><br>I¯xy R = ∓<br><br>(−16.08)<br><br>18.03 = ±0.8919<br><br>Because the upper sign goes with θ1, we have 2θ1 = 63.11◦ or 116.9◦, and 2θ2 = 243.11◦ or −63.11◦. To determine the correct choices, we investigate the sign of cos2θ1. From Eqs. (9.21) we obtain<br><br>cos2θ1 = (I¯x − I¯y)/(2R) = (37.36 − 21.07)/[2(18.03)]<br><br>which is positive. Therefore, 2θ1 = 63.11◦ and 2θ2 = 243.11◦ are the correct choices, which give<br><br>θ1 = 31.6◦ θ2 = 121.6◦ Answer<br><br>The principal axes, labeled 1 and 2 in Fig. (c), correspond to the axes of I1 and I2, respectively.|
|---|

###### 504

|31.6°<br><br>x<br><br>C<br><br>y<br><br>(c)<br><br>1<br><br>2<br><br>Part 2<br><br>To compute the moments and product of inertia relative to the uv-axes in Fig. (a), we need only substitute I¯x = 37.36 × 106 mm4, I¯y = 21.07 × 106 mm4, I¯xy = −16.08 × 106 mm4, and θ = 50◦ into the transformation equations. From Eq. (9.17) we obtain<br><br>Iu × 10−6 =<br><br>37.36 + 21.07 2 +<br><br>37.36 − 21.07 2<br><br>cos100◦ − (−16.08)sin100◦<br><br>Iu = 43.6 × 106 mm4 Answer Equation (9.18) yields<br><br>Iv × 10−6 =<br><br>37.36 + 21.07 2 −<br><br>37.36 − 21.07 2<br><br>cos100◦ + (−16.08)sin100◦<br><br>Iv = 14.8 × 106 mm4 Answer From Eq. (9.19) we have<br><br>Iuv × 10−6 =<br><br>37.36 − 21.07 2<br><br>sin100◦ + (−16.08)cos 100◦<br><br>Iuv = 10.8 × 106 mm4 Answer|
|---|

![image 69](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile69.png>)

###### Problems

y

9.50 For the rectangular region, determine (a) the principal moments of inertia

v

and the principal directions at the centroid C; and (b) the moments and products of inertia about the u-v axes.

u

- 9.51 For the semicircular region, calculate (a) the principal moments of inertia and the principal directions at the centroid C; and (b) the moments and products of inertia about the u-v axes.

x

u

v

y

65°

C 120mm

x

C

O

y

6 in.

8 in.

Fig. P9.51 Fig. P9.52

- 9.52 Find the principal moments of inertia and the principal directions at the centroid C of the triangle.
- 9.53 Using Ix, Iy, and Ixy in Table 9.2, compute Iu, Iv, and Iuv for the parabola shown.

θ

8.5 in.

6.4 in.

O

y

y=cx2

u

x

v

Fig. P9.53

- 9.54 Given that the properties of the region shown are Ix =3000 in.4,

30°

C x

4 in.

3 in.

Fig. P9.50

Iy =2000 in.4, and Ixy = − 500 in.4, determine Iu, Iv, and Iuv for θ =120◦.

y

v

- 9.55 The properties of the region shown are Ix =10 × 106 mm4, Iy =20 × 106 mm4, and Ixy =12 × 106 mm4. Compute Iu, Iv, and Iuv if θ = 33.7◦.
- 9.56 The u- and v-axes are the principal axes of the region shown. Given that Iu =7600 in.4, Iv =5000 in.4, and θ =33.7◦, determine Ix, Iy, and Ixy.
- 9.57 The x- and y-axes are the principal axes for the region shown with Ix = 6 × 106 mm4 and Iy =2 × 106 mm4. (a) Calculate the angle θ for which Iuv is maximum. (b) Determine Iu, Iv, and Iuv for the angle θ found in part (a).

u

θ x

C

Fig. P9.54–P9.58

###### 9.50–9.68 Problems 507

- 9.58 Compute Iv for the region shown, given that Iu =160 × 106 mm4, Ixy = −30 × 106 mm4, and θ =18.44◦. The u- and v-axes are principal axes for the region.
- 9.59 The inertial properties of the region shown with respect to the x- and

y-axes are Ix = Iy = 16.023 × 106 mm4 and Ixy = −1.1310 × 106 mm4. Determine the principal moments of inertia at point O. (Hint: The orientation of the principal axes can be determined by inspection.)

20

Dimensions in mm

O

x

y

30

30

60 60

60

60

u

y

x

80 mm

45° C

20 mm

20 mm

80 mm

Fig. P9.59 Fig. P9.60

- 9.60 Determine I¯u for the inverted T-section shown. Note that the section is symmetric about the y-axis.
- 9.61 Using Ix and Iu from Table 9.2, determine the moment of inertia of the circular sector about the OB-axis. Check your result for α =45◦ with that given for a quarter circle in Table 9.2.

O

R

B

x

y

α α

x

a

a C

y

a

|O<br><br>|2<br><br>u| |
|---|---|---|
| | |2 in.|

in.

y v

x

Fig. P9.61 Fig. P9.62 Fig. P9.63

- 9.62 Show that every axis passing through the centroid of the equilateral triangle is a principal axis.
- 9.63 Calculate Iu, Iv, and Iuv for the region shown.
- 9.64 The L80 × 60 × 10-mm structural angle has the following cross-

10

y

Dimensions in mm

80

###### C

x

26.5

10

16.5

60

sectional properties: Ix =0.808 × 106 mm4, Iy =0.388 × 106 mm4, and Fig. P9.64

I2 =0.213 × 106 mm4, where I2 is a principal centroidal moment of inertia. Assuming Ixy is negative, compute (a) I1 (the other principal centroidal moment of inertia); and (b) the principal directions.

- 9.65 Compute the principal centroidal moments of inertia for the area shown.

2 ft

1.32 ft

x

y

1.32 ft

16 in.

20 in.

|10in.|
|---|

O x

y

Fig. P9.65 Fig. P9.66

- 9.66 Determine the directions of the principal axes of inertia at point O for the area shown.
- 9.67 Determine the principal centroidal moments of inertia and the corresponding principal directions for the region shown.

6 in.

10 in.

7 in. 9 in.

6 in.

10 in.

9 in. 7 in.

y

x

Parabola

Parabola

40

160

160 40

Dimensions in mm

40

y

x

160

Fig. P9.67 Fig. P9.68

- 9.68 Compute the principal centroidal moments of inertia and the corresponding principal directions for the region shown.

###### *9.5 Mohr’s Circle for Moments and Products

###### of Inertia

Mohr’s circle is a graphical representation of the transformation equations for moments and products of inertia. Developed by Otto Mohr, a German engineer in 1882, it is a popular alternative to the transformation equations. There are two advantages to using Mohr’s circle. First, the circle gives a clear visual representation of how the inertial properties vary with the orientation of the axes. Second,

by referring to the circle, you can obtain the numerical values without having to memorize the transformation equations.

###### a. Construction of Mohr’s circle

Consider the plane region shown in Fig. 9.9(a). Let Ix, Iy, and Ixy be the moments and the product of inertia of the region with respect to the x-y axes that intersect at point O. Mohr’s circle associated with point O is shown in Fig. 9.9(b). The circle is constructed as follows:

1. Draw a set of axes, the horizontal axis representing the moment of inertia

(M.I.), and the vertical axis representing the product of inertia (P.I.).

2. Plot the point x with coordinates (Ix, Ixy), and the point y with coordinates

(Iy,−Ixy).

3. Join x and y with a line, and draw a circle with this line as its diameter.

y

O x

- (a)
- (b)

P.I.

x

Ixy

R

Iy

M.I.

Ix

–Ixy

y

b

###### Fig. 9.9

Mohr’s circle is now complete. Note that the radius of the circle is

2

Ix − Iy 2

+ Ixy2

R =

and its center is located at

- 1

- 2

(Ix + Iy)

b =

###### b. Properties of Mohr’s circle

The properties of Mohr’s circle are

- • The end points of every diameter of the circle represent the moments and the product of inertia associated with a set of perpendicular axes passing through point O.
- • Angles between diameters on the circle are twice the angles between axes at point O, and these angles are measured in the same sense (CW or CCW).

The procedure for determining the inertial properties with respect to particular axes, such as the u-v axes shown in Fig. 9.10(a), is as follows:

- 1. Note the magnitude and sense of the angle θ between the x-y and the u-v coordinate axes. (The sense of the θ is the direction in which the x-y axes must be rotated so that they coincide with the u-v axes.)
- 2. Rotate the diameter x-y of Mohr’s circle through the angle 2θ in the same sense as θ. Label the end points of this diameter u and v, as shown in Fig. 9.10(b). The coordinates of u are (Iu, Iuv), and the coordinates of v are (Iv,−Iuv).

Mohr’s circle can also be used to ﬁnd the principal moments of inertia and the principal directions. Referring to Fig. 9.10(b), we see that the maximum and the

v y

2

u O

θ x α

1

- (a)
- (b)

P.I.

u

x

Iuv

θ

2

###### R

α

2

Iv I2 Iu I1

M.I.

–Iuv

y

v

b

###### Fig. 9.10

minimum moments of inertia are I1 = b + R and I2 = b − R, respectively. The orientation of the principal axes, labeled “1” and “2” in Fig. 9.10(a), is obtained by rotating the x-y axes though the angle α. The magnitude and sense of α is determined from the Mohr’s circle. In particular, note that α in Fig. 9.10(a) and 2α in Fig. 9.10(b) must have the same sense.

###### c. Veriﬁcation of Mohr’s circle

Figure 9.11 shows the circle that was constructed following the steps outlined in the preceding section. Because x and u are points located above the abscissa, we have assumed that both Ixy and Iuv are positive.

P.I.

Ix

Iu

u

x

θ

2

###### R

Ixy Iuv

α

2

M.I.

Ix– Iy

2

y

Iy+ Iy

Iy

v

b =

2

b

#### ( ) 2

2

Ix– Iy 2

R = + Ixy

###### Fig. 9.11

In order to prove that Mohr’s circle is a valid representation of the transformation equations, we must show that the coordinates of u agree with Eqs. (9.17) and (9.19).

From Fig. 9.11, we have

###### Iu = b + R cos(2θ + 2α)

Using the identity

cos(2θ + 2α) = cos2θ cos2α − sin2θ sin2α

and substituting b = (Ix + Iy)/2, we get

Ix + Iy

2 + R(cos2θ cos2α − sin2θ sin2α)

Iu =

From Fig. 9.11, we see that sin2α = Ixy/R and cos2α = (Ix − Iy)/(2R). Substituting these relations into the last equation yields

Ix + Iy

Ix − Iy 2R

Ixy R

2 + R

cos2θ −

Iu =

sin2θ

or

Ix + Iy

Ix − Iy 2

cos2θ − Ixy sin2θ (9.24) From Fig. 9.11, we also obtain

2 +

Iu =

###### Iuv = R sin(2θ + 2α)

Using the identity

sin(2θ + 2α) = sin2θ cos2α + cos2θ sin2α

and the previously derived expressions for sin2α and cos2α, we have

Ix − Iy 2R

Ixy R

sin2θ +

Iuv = R

cos2θ

which becomes

Ix − Iy 2

sin2θ + Ixy cos2θ (9.25)

Iuv =

Because Eqs. (9.24) and (9.25) are identical to the transformation equations, Eqs. (9.17) and (9.19), we conclude that Mohr’s circle is a valid representation of the transformation equations.

|Sample Problem 9.10<br><br>For the region shown in Fig. (a), calculate (1) the centroidal principal moments of inertia and principal directions; and (2) the moments and product of inertia about the u-v axes through the centroid C. Note that this is the same region as in Sample Problem 9.9.<br><br>50°<br><br>u v<br><br>x<br><br>C<br><br>160<br><br>200<br><br>30<br><br>30<br><br>y<br><br>(a)<br><br>Dimensions in mm<br><br>Solution<br><br>Construction of Mohr’s Circle<br><br>From the solution to Sample Problem 9.9, we have I¯x =37.36 × 106 mm4, I¯y =21.07×106 mm4, and I¯xy = −16.08×106 mm4. Using these values, Mohr’s circle is plotted as shown in Fig. (b), following the procedure outlined in Art. 9.5.<br><br>2θ2<br><br>2α<br><br>100°<br><br>37.36<br><br>Iu<br><br>16.08<br><br>I2<br><br>Iv<br><br>I1<br><br>16.08<br><br>Iuv<br><br>v<br><br>21.07<br><br>yC<br><br>u<br><br>xC<br><br>P.I. (106 mm4)<br><br>M.I. (106 mm4)<br><br>(b)<br><br>2 1<br><br>b a<br><br>R<br><br>2θ1|
|---|

|Note that<br><br>1. The points on the circle that correspond to the centroidal axes that are parallel to the x- and y-axes are labeled xC and yC, respectively.<br>2. Because I¯xy is negative, xC is plotted below the abscissa and yC is plotted above.<br><br><br>If the circle were drawn to scale, all unknown values could be determined by direct measurements. However, we will compute the requested values by trigonometry. Of course, all results in the analyses should agree with those found previously in the solution to Sample Problem 9.9.<br><br>The following values, computed directly from the circle, are shown in the ﬁgure.<br><br>b =<br><br>37.36 + 21.07<br><br>2 × 106 = 29.22 × 106 mm4 a =<br><br>37.36 − 21.07 2 × 106 = 8.145 × 106 mm4<br><br>R = (8.145)2 + (16.08)2 × 106 = 18.03 × 106 mm4<br><br>Part 1<br><br>In Fig. (b), 1, and 2 correspond to the maximum and minimum moments of inertia, respectively. Therefore, we have I1,2 =b± R =(29.22±18.03)×106 mm4, from which we obtain<br><br>I1 = 47.3 × 106 mm4 I2 = 11.2 × 106 mm4 Answer<br><br>The principal directions are found by calculating the angles θ1 and θ2. From the circle we ﬁnd that 2θ1 = sin−1 (16.08/18.03)= 63.11◦ and 2θ2 =180 + 2θ1 =243.11◦, which gives<br><br>θ1 = 31.6◦ θ2 = 121.6◦ Answer<br><br>Note that on the circle the central angle from xC to 1 is 2θ1, counterclockwise. Therefore, the principal direction corresponding to I1 is θ1 =31.6◦, measured counterclockwise from the centroidal x-axis. (Remember that angles on the circle are twice the angles between axes, measured in the same direction). Therefore, the centroidal principal axes are oriented as shown in Fig. (c).<br><br>31.6°<br><br>x<br><br>C<br><br>y<br><br>(c)<br><br>1<br><br>2<br><br>Part 2<br><br>To determine Iu, Iv, and Iuv, the points u and v—corresponding to the u- and v-axes, respectively—must be identiﬁed on Mohr’s circle. Because the u-axis is located at 50◦ counterclockwise from the centroidal x-axis, u on the circle is 100◦|
|---|

###### 514

|counterclockwise from xC. Of course, v is located at the opposite end of the diameter from u. To facilitate our computations, we have introduced the central angle 2α between points 1 and u, given by 2α = 100◦−2θ1 = 100◦−63.11◦ = 36.89◦. Referring to the circle, we ﬁnd that<br><br>Iu,v = b ± R cos2α<br><br>= (29.22 ± 18.03cos 36.89◦) × 106 mm4<br><br>or<br><br>Iu = 43.6 × 106 mm4 Iv = 14.8 × 106 mm4 Answer<br><br>Additionally, the circle yields |Iuv| = R sin2α = (18.03sin36.89◦) × 106 = 10.8 × 106 mm4. Because u is above the abscissa, Iuv is positive. Therefore, we have<br><br>Iuv = +10.8 × 106 mm4 Answer<br><br>Recall that in the transformation equations, Eqs. (9.17)–(9.19), 2θ represents the angle measured counterclockwise from the x-axis to the u-axis. However, after Mohr’s circle has been drawn, any convenient angle—clockwise or counterclockwise, and measured from any point on the circle—can be used to locate u. For example, on the circle in Fig. (b) we see that u is located at 80◦ in the clockwise direction from yC. This is consistent with Fig. (a), where the u-axis is reached from the centroidal y-axis by a 40◦ clockwise rotation.|
|---|

![image 70](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile70.png>)

###### Problems

###### The following problems are to be solved using Mohr’s circle. 9.69 Find the moments and the product of inertia of the rectangle about the u-v

y

v

axes at the centroid C.

u

- 9.70 Determine the moments and the product of inertia of the semicircle about the u-v axes that pass through the centroid C.

x

y

u

v

C 120mm

65°

Fig. P9.70

- 9.71 Find the principal moments of inertia and the principal directions at the centroid C of the triangle.

y

x

C

O

8 in.

6 in.

Fig. P9.71

- 9.72 Determine the moments and the product of inertia of the parabola about the u-v axes.

30°

4 in. x

C

3 in.

Fig. P9.69

u

y

v

y = cx2

6.4 in.

θ

x

O

8.5 in.

###### Fig. P9.72

###### 9.69–9.78 Problems 517

- 9.73 Given that the properties of the region shown are Ix =3000 in.4, Iy =2000 in.4, and Ixy = − 500 in.4, determine Iu, Iv, and Iuv for θ =120◦.
- 9.74 The properties of the region shown are Ix =10 × 106 mm4, Iy =20 × 106 mm4, and Ixy =12 × 106 mm4. Determine Iu, Iv, and Iuv if θ =33.7◦.
- 9.75 The u- and v-axes are the principal axes of the region shown. Given that Iu =8400 in.4, Iv =5000 in.4, and θ = 25◦, calculate Ix, Iy, and Ixy.

y

C

v

u θ x

Fig. P9.73–P9.77

- 9.76 The x- and y-axes are the principal axes for the region shown, with Ix =8 × 106 mm4 and Iy =2 × 106 mm4. (a) Calculate the angle θ for which Iuv is maximum. (b) Determine Iu, Iv, and Iuv for the angle θ found in part (a).
- 9.77 Compute Iv for the region shown, given that Iu =140 × 106 mm4, Ixy = −30×106 mm4, and θ =18◦. The u- and v-axes are principal axes for the region.
- 9.78 The L80 × 60 × 10-mm structural angle has the following cross-sectional properties: Ix =0.808 × 106 mm4, Iy =0.388 × 106 mm4, and I2 =0.213 × 106 mm4, where I2 is a centroidal principal moment of inertia. Assuming that Ixy is negative, compute (a) I1 (the other centroidal principal moment of inertia); and (b) the principal directions at the centroid.

10

y

Dimensions in mm

80

C x

26.5

10

16.5

60

###### Fig. P9.78

![image 71](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile71.png>)

###### Review of Equations

###### Moments of inertia of plane areas

###### Ix = y2 dA Iy = x2dA Ixy = xy dA

JO = r2 dA = Ix + Iy (polar moment of inertia)

###### Parallel axis theorems

Ix = I¯x + Ay¯2 Iy = I¯y + Ax¯2 Ixy = I¯xy + Ax¯y¯ JO = J¯C + Ar¯2

###### Radius of gyration

kx = Ix/A ky = Iy/A kO = JO/A

###### Composite areas

Ix = i(Ix)i Iy = i(Iy)i Ixy = i(Ixy)i JO = i(JO)i

###### Transformation equations

Ix + Iy

Ix − Iy 2

2 +

cos2θ − Ixy sin2θ

Iu =

Ix + Iy

Ix − Iy 2

2 −

cos2θ + Ixy sin2θ

Iv =

Ix − Iy 2

sin2θ + Ixy cos2θ

Iuv =

θ = angle measured from x-axis to u-axis in counterclockwise direction

###### Principal values and principal directions

2

Ix + Iy

Ix − Iy 2

###### + Ixy2

2 ± R R =

I1,2 =

Ix − Iy 2R

Ixy R

sin2θ1,2 = ∓

cos2θ1,2 = ±

![image 72](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile72.png>)

###### Review Problems

- 9.79 Determine Iu, Iv, and Iuv for the rectangle where C is the centroid of the area.

v y

C

θ

120mm 80mm

x

u

Fig. P9.79

- 9.80 The principal moments of inertia at point O for the shaded region are 60 × 106 mm4 and 30 × 106 mm4. In addition, the product of inertia with respect to the x- and y-axes is 10 × 106 mm4. Find (a) Ix and Iy; and (b) Iu and Iv.

y

O

x

u u

50°

R

x

y

Fig. P9.80 Fig. P9.81

- 9.81 By integration, show that the product of inertia with respect to the x- and y-axes for the quarter circular region is R4/8.
- 9.82 Compute the I¯x and I¯y for the annular region.

40mm

y

x

60mm

Fig. P9.82

- 9.83 Using integration, evaluate the moments of inertia about the x- and y-axes

60 mm

30 mm

90 mm

60 mm

y

x

Fig. P9.83

for the parallelogram.

- 9.84 The inertial properties at point O for a plane region are Ix =200 × 106 mm4, Iy =300 × 106 mm4, and Ixy = − 120 × 106 mm4. Determine the principal moments of inertia and principal directions at point O.

###### 9.85 Compute I¯x and I¯y for the shaded region.

y

6 in.

1 in.

6 in.

1 in.

1 in.

x

3 in.

Fig. P9.85

###### 9.86 The ﬂanged bolt coupling is fabricated by drilling 10 evenly spaced 0.5-in. diameter bolt holes in a steel plate. The radii of the plate and bolt circle are 5in. and 4in., respectively. Determine the percent reduction in the polar moment of the area about point O due to the drilling operation.

y

5in.

x O

4in.

Fig. P9.86

###### 9.87 The ﬁgure shows a structural shape known as an unequal angle (L) section. From a table of structural shapes, the inertial properties of an L150 × 100 × 10-mm are x¯ =23.8 mm, y¯ =48.8 mm, A =2400 mm2, I¯x =5.58 × 106 mm4, I¯y =2.03 × 106 mm4. In addition, the angle α locating the axis of minimum centroidal moment of inertia (labeled as the 2-axis in the ﬁgure) is listed as 24.0◦,

with the corresponding radius of gyration being k¯2 =21.9 mm. Compute (a) the other principal centroidal moment of inertia; and (b) I¯xy.

y x

C

x

###### y

α

2

###### Fig. P9.87

- 9.88 Compute I¯x, I¯y, and I¯xy for the region shown.

12 in.

y

x

5in.

Fig. P9.88

- 9.89 Determine Ix and Ixy for the region shown.

60 mm

90 mm

x

y

90 mm

Fig. P9.89

- 9.90 Calculate I¯x, I¯y, and I¯xy for the plane region shown.

y

40

35

40

x 50

Dimensions in mm

###### Fig. P9.90

- 9.91 For the plane region shown, determine (a) Ix and Iy; and (b) I¯x and I¯y using the parallel axis theorem and the results of part (a).

x

y

20

20

20

10

Dimensions in mm

y

x

4 in.

4 in.

y2=4x

x2=4y

Fig. P9.91 Fig. P9.92

- 9.92 Use integration to ﬁnd Ix, Iy, and Ixy for the region shown.
- 9.93 Determine the principal moments of inertia and the principal directions at

y

2 in.

the centroid of the region shown.

9.94 The inertial properties of the region shown are Ix =140 in.4, Iy =264 in.4, and Ixy = −116 in.4 Determine Iu, Iv, and Iuv. Note that the u-axis passes through point B.

6 in.

2 in.

x

y

6 in.

v

Fig. P9.93

3.5 in.

O

x

B

u

2 in.

7.5 in.

###### Fig. P9.94

# 10

### Virtual Work and Potential Energy

![image 73](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile73.png>)

Methods based on concepts of work and energy are well-suited for the analysis of structures consisting of interconnected links. The scissor lift shown here is a typical example of a multi-link structure. This chapter discusses two work-energy methods of analysis: the method of virtual work and the principle of stationary potential energy. Richard Thornton/Shutterstock

###### *10.1 Introduction

Methods based on the concepts of virtual work and potential energy can be used as alternatives to Newton’s laws in equilibrium analysis. These methods are best suited for the analysis of systems made up of several interconnected rigid bodies. The primary advantage of work and energy methods is that the reactions at certain connections, such as pins or inextensible cables, do not enter into the analysis. Therefore, the number of unknowns (and equations) is often considerably reduced.

The disadvantage of work and energy methods is that they require the use of kinematics (geometry of motion), which is a branch of dynamics. To keep

###### 523

the kinematics relatively simple, we conﬁne our discussion to two-dimensional problems. In addition to kinematics, the concept of work must also be introduced.

###### *10.2 Virtual Displacements

###### a. Deﬁnition and notation

A virtual displacement is deﬁned as a ﬁctitious displacement of inﬁnitesimal magnitude. By “ﬁctitious,” we mean that the displacement is imaginary; it may not actually occur.

The usual practice is to precede an inﬁnitesimal quantity with the letter d. Thus, the inﬁnitesimal displacement vector of point A would be denoted by drA. To draw attention to its ﬁctitious nature, a virtual displacement is preceded by δ (lower case delta). Hence, the virtual displacement of point A would be written as δrA.

Mathematically, drA and δrA are identical. For example, if rA is a function of a parameter θ, we can write δrA =(drA/dθ)δθ, where δθ is the virtual change in θ.

###### b. Virtual motion of a rigid body

Virtual Translation Virtual translation of a rigid body is illustrated in Fig. 10.1. Two important characteristics of translation are

δ rB

B

• Any straight line embedded in the body, such as the line AB, remains parallel

to its original position. That is, embedded lines do not rotate. • All points of the body have the same displacement. Therefore,

δ rA

δrB =δrA (10.1)

A

where A and B are any two points of the body.

###### Fig. 10.1

Virtual Rotation about a Fixed Point Figure 10.2 illustrates virtual rotation δθ of a rigid body about point A. The characteristics of this motion are

δ rB

- • Every line embedded in the body undergoes the same virtual rotation δθ.
- • Any point of the body, such as B, moves along a circular arc centered at A. The magnitude of the virtual displacement of B is

B

δθ rAB

###### δrB =rAB δθ (10.2)

A

where rAB is the magnitude of rAB (the vector drawn from A to B).

###### Fig. 10.2

Sometimes it is convenient to use the vector form of Eq. (10.2), which is

###### δrB =δθ × rAB (10.3)

where δθ is the virtual rotation vector shown in Fig. 10.3. It readily can be veriﬁed that Eq. (10.3) produces the correct magnitude and direction of δrB.

###### δθ

Plane of motion

###### B

δrB

rAB

A

δθ

###### Fig. 10.3

General Plane Virtual Motion Any virtual motion of a rigid body can be obtained by a superposition of translation and rotation about a point, as illustrated in Fig. 10.4. We ﬁrst apply the translation δrA, which moves point A to its ﬁnal position without changing the orientation of the body. This is followed by the rotation δθ about A to give the body is ﬁnal orientation. The resulting virtual displacement of point B is

δrB =δrA + δθ × rAB (10.4)

###### F

δ rB

B

###### δr α

δ θ

(a)

A

δ rA

###### F

###### Fig. 10.4

δr α

F cos α

The reference point A can be chosen arbitrarily. The order in which the two motions (translation and rotation) are carried out is irrelevant.

(b)

###### *10.3 Virtual Work

###### F

δr δr cos α

###### a. Virtual work of a force

α

If the point of application of a force F undergoes a virtual displacement δr, as shown in Fig. 10.5 (a), the virtual work δU done by the force is deﬁned to be

(c)

###### δU =F·δr= F cosα δr (10.5) Fig. 10.5

where α is the angle between F and δr. Note that the virtual work is a scalar that can be positive, negative, or zero, depending upon the angle α. The dimension of virtual work is [FL]; hence the units are lb · ft, N · m, and so forth.

Referring to Figs. 10.5(b) and 10.5(c), we see that the virtual work can be viewed in two ways:

- • δU =(F cosα)δr, where F cosα (the component of F in the direction of δr) is called the working component of the force.
- • δU = F(δr cosα), where δr cosα (the component of δr in the direction of F) is known as the work-absorbing component of the virtual displacement.

###### b. Virtual work of a couple

Figure 10.6(a) shows a couple formed by the forces −F and F acting at points A and B of a rigid body. The corresponding couple-vector C=rAB ×F is perpendicular to the plane of the couple, as indicated in Fig. 10.6(b). If the body undergoes a virtual motion in the plane of the couple, the virtual work of the couple is

###### δU = − F·δrA + F·δrB

δθ

Plane of couple and plane of motion

C = rAB × F

A

rAB F

–F

B

(a) (b)

###### Fig. 10.6

Substituting for δrB from Eq. (10.4), we get

δU = − F·δrA + F·(δrA + δθ × rAB)=F·δθ × rAB =rAB × F·δθ or

δU =C·δθ (10.6)

Because C and δθ are collinear (recall that we consider only two-dimensional problems), the virtual work of the couple can also be written as

δU =C δθ (10.7)

Note that δU is positive if C and δθ have the same sense, and negative if they have opposite sense.

###### c. Virtual work performed on a rigid body

The following theorem is sometimes useful in the computation of virtual work (this theorem is also needed to derive the principle of virtual work):

###### The virtual work of all forces that act on a rigid body is equal to the virtual work of their resultant.

Proof Consider a rigid body that is subjected to the coplanar forces F1, F2, ... , Fi ... ,

- as in Fig. 10.7(a). Figure 10.7(b) shows the resultant of this force system consisting of the force R= iFi acting at A, and the couple CR = irAi × Fi, where rAi is the vector drawn from A to the point of application of Fi. If the body undergoes a virtual displacement, the virtual work of all the forces is

###### Fi ·δri

δU =

i

F3

Fi

F2 R

rAi

CR

A

A

F1

(a)

(b)

###### Fig. 10.7

Using Eq. (10.4), we substitute δri =δrA + δθ × rAi, which results in

Fi ·δrA +

Fi ·δθ × rAi

δU =

i

i

The ﬁrst term in this expression is

Fi ·δrA =

###### Fi ·δrA =R·δrA

i

i

The second term can be written as

rAi × Fi ·δθ=CR ·δθ

Fi ·δθ × rAi =

rAi × Fi ·δθ =

i

i

i

Therefore, the virtual work performed on the body is

###### δU =R·δrA + CR ·δθ (10.8)

which completes the proof.

###### d. Virtual work for a system of rigid bodies

Consider a system of interconnected rigid bodies, where the frictional forces at the connections and the supports are negligible. Virtual work of friction forces would introduce complications that we wish to avoid at this level. The connections that we consider are thus limited to pins, rollers, inextensible and extensible cables, ideal springs, and so forth.

If a system of interconnected rigid bodies is given a virtual displacement, the virtual work done on the system equals the virtual work of the external forces, plus the virtual work of the internal forces. At connections that do not deform, the net work done by the internal forces is zero. For example, if a pin joins two rigid bodies, the positive work of the pin reaction acting on one body cancels the negative work of the pin reaction acting on the other body. The reason for this cancellation is that the pin reactions acting on the two bodies are equal in magnitude, opposite in sense, and undergo identical displacements. The forces provided by a deformable connector may also be equal and opposite; however, because of deformation, they do not necessarily undergo the same displacement. Consequently, a deformable connection is capable of doing virtual work on a system. Springs are the only deformable connections that we consider in this text.

###### *10.4 Method of Virtual Work

###### a. Principle of virtual work

The principle of virtual work for a rigid body states the following:

If a body is in equilibrium, then the virtual work of all forces acting on the body is zero for all kinematically admissible virtual displacements of the body from the equilibrium position.

The term kinematically admissible means that the virtual displacements must be kinematically possible; that is, they must not violate constraints imposed by the supports.

Proof of the principle follows directly from Eq. (10.8). If a body is in equilibrium, the resultant of the forces acting on it vanishes; that is, R=0 and CR =0, and Eq. (10.8) becomes

δU =0 (10.9) The principle of virtual work also applies to systems of connected rigid bodies. Because a system can be in equilibrium only if each of its members

###### 10.4 Method of Virtual Work 529

(constituent bodies) is in equilibrium, we conclude that δU =0 for each member. It follows that the virtual work done on the system also vanishes. In other words:

If a system of rigid bodies is in equilibrium, then the virtual work of all forces acting on the system is zero for all kinematically admissible virtual displacements of the system from the equilibrium position.

###### b. Kinematic constraints and independent coordinates

The following terms are frequently used in kinematics (geometry of motion):

x

O

- • Kinematic constraints are geometric restrictions imposed on the conﬁguration of a system.
- • Kinematically independent coordinates of a system are parameters that deﬁne the conﬁguration of the system and can be varied independently without violating kinematic constraints.
- • Number of degrees of freedom (number of DOF) of a system is the number of kinematically independent coordinates required to completely deﬁne the conﬁguration of the system.
- • Equations of constraint are mathematical relations between position coordinates that describe the kinematic constraints.

L

θ

A

y

###### Fig. 10.8

O

To illustrate these terms, consider the bar shown in Fig. 10.8. This bar has a

x

single DOF, because it takes only one coordinate, such as the angle θ to deﬁne the position of every point in the bar. Because there are no kinematic constraints on θ, it is a kinematically independent coordinate.

L1

θ1

The system of two bars in Fig. 10.9 also has one DOF. For the kinemati-

d

y

cally independent coordinate we may choose either θ1 or θ2. Whichever of the two angles is selected, the other one is determined by the equation of constraint L1 cosθ1+L2 cosθ2 = d. Any conﬁguration of the bars that violates this equation of constraint is kinematically inadmissible.

A

L2

θ2

B

A system with two DOF is shown in Fig. 10.10. This system requires two

kinematically independent coordinates, such as θ1 and θ2, to completely describe its conﬁguration.

Fig. 10.9

###### c. Implementation of the method of virtual work

O

x

When applying the method of virtual work, we must be certain that the virtual displacements of points where the loads are applied (the displacements that contribute to the virtual work) are kinematically admissible. This can be accomplished by the following two steps:

L1

θ1

y

A

L2

θ2

- • First, use geometry to relate the coordinates of the points where loads act to the kinematically independent coordinates.
- • Then obtain the relationships between the virtual changes of these coordinates (the virtual displacements) by differentiation.

B

Fig. 10.10

As an example, consider the bar shown in Fig. 10.11. The weight of the bar is

x yG

W, and its center of gravity is denoted by G. The virtual work done on the bar is

O

L/2

θ

###### δU = W δyG + F δxA

G

L/2

Choosing θ as the kinematically independent coordinate, we obtain from geometry

W

F

xA A

y

L 2

yG =

cosθ xA = L sinθ

Fig. 10.11

By taking the differentials of the coordinates (recall that virtual changes are identical to differentials), we get

L 2

δyG = −

sinθ δθ δxA = L cosθ δθ

Therefore, the virtual work done on the bar is

W 2

sinθ + F cosθ L δθ

δU = −

If θ is an equilibrium position, then δU =0 for any nonzero δθ. Consequently, the condition for equilibrium is

W 2

−

sinθ + F cosθ =0

Consider next a system of bodies with n degrees of freedom with q1, q2, ..., qn being the kinematically independent coordinates. If we follow the procedure outlined above, the virtual work done on the system will take the form

###### δU = Q1 δq1 + Q2 δq2 + ··· + Qn δqn (10.10)

where each Qi is in general a function of q1, q2, ... , qn. If the system is in equilibrium, then δU = 0 for any nonzero combination of δq’s. This condition can be satisﬁed only if

Q1 = Q2 = ··· = Qn =0

The Q’s are known as the generalized forces. If qi has units of distance, then Qi has units of force; if qi is an angle, then Qi has units of moment of a force.

When applying the method of virtual work, it is recommended that you begin by drawing an active-force diagram, which is a sketch of the body that shows only the forces that do work. Figure 10.11 is an example of an active-force diagram. It displays only the work-producing forces W and F. The pin reactions at O were omitted, because they do no work (point O does not move).

|Sample Problem 10.1<br><br>Compute the couple C0 that will support the load W. Neglect the weights of<br><br>x<br><br>a<br><br>C<br><br>yC<br><br>A<br><br>B<br><br>D<br><br>C0<br><br>y<br><br>a<br><br>a<br><br>W<br><br>θ<br><br>the bars.<br><br>Solution<br><br>Note that the system possesses one DOF because its conﬁguration can be speciﬁed by a single coordinate, such as the angle θ.<br><br>The ﬁgure is an active-force diagram because only W and C0 do virtual work when the system is given a virtual displacement consistent with the constraints. The pin reaction at A is workless because its point of application does not move. The roller reaction at D does no work because it is horizontal, whereas the virtual displacement of end D can only be vertical. The internal forces, including the pin reaction at B, are also workless.<br><br>The ﬁgure can also be used for the kinematic analysis. We introduce the xycoordinate system with origin at the ﬁxed point A, and we choose the angle θ as the kinematically independent coordinate. The vertical coordinate of end C is denoted yC.<br><br>Applying the principle of virtual work to the system under consideration, we have<br><br>δU =C0 δθ − W δyC =0 (a)<br><br>where δθ is the virtual rotation of the bar BD and δyC is the vertical virtual displacement of C. The positive directions for δθ and δyC are, of course, the same as for θ and yC, respectively. The sign of the ﬁrst term in Eq. (a) is positive because positive δθ has the same sense as positive C0. The second term has a negative sign because the positive sense of W is opposite to the positive sense of δyC.<br><br>We now relate yC to θ using geometry and then obtain δyC in terms of δθ by differentiation. Referring to the ﬁgure, this procedure yields<br><br>yC = 2a cosθ δyC =<br><br>dyC dθ<br><br>δθ = −2a sinθ δθ (b)<br><br>Substituting Eq. (b) into Eq. (a), we obtain<br><br>δU =C0 δθ − W(−2a sinθ δθ) = 0 or<br><br>(C0 + 2Wa sinθ)δθ = 0 (c)<br><br>Equation (c) can be satisﬁed for a nonzero δθ only if the term in parentheses (which represents the generalized force corresponding to δθ) vanishes, which yields<br><br>C0 = − 2Wa sinθ Answer<br><br>as the condition for equilibrium. The negative sign indicates that the correct sense of C0 is opposite to that shown in the ﬁgure.|
|---|

|Sample Problem 10.2<br><br>The mechanism shown in the ﬁgure consists of two pin-connected, homogeneous x bars of weight W and length L each. The roller at B moves in a horizontal slot,<br><br>y<br><br>O<br><br>L<br><br>A<br><br>L<br><br>xB<br><br>W<br><br>W<br><br>P<br><br>1.5L<br><br>y1<br><br>y2<br><br>B<br><br>θ1=30°<br><br>θ2(50.66°)<br><br>located at the distance 1.5L below the pin at O. Determine the force P that will hold the system in equilibrium for θ1 =30◦.<br><br>Solution<br><br>The system has one DOF because only one position coordinate, for example, θ1 or θ2, is required to specify its conﬁguration. The ﬁgure shown is also an active-force diagram, because it shows only those forces than can perform virtual work on the system. The pin reactions at O and A, and the roller reaction at B, are omitted because their virtual work is zero.<br><br>It is convenient to use the same ﬁgure for kinematic analysis. We introduce the xy-coordinate system shown, the origin of which is located at the ﬁxed point O. The coordinates y1 and y2 locate the centers of gravity of the bars, and xB is the horizontal coordinate of end B.<br><br>If the system is given a virtual displacement consistent with the constraints, the principle of virtual work takes the form<br><br>δU = W δy1 + W δy2 + P δxB =0 (a)<br><br>All the signs in Eq. (a) are positive because the direction of each force is the same as the positive coordinate direction of its point of application.<br><br>The next step is to express δy1, δy2, and δxB as functions of the virtual change in the kinematically independent coordinate. Let us choose θ1 as the independent coordinate. Because the roller at B is constrained to move in the horizontal slot, the equation of constraint is L cosθ1 + L cosθ2 =1.5L, or<br><br>cosθ1 + cosθ2 =1.5 (b)<br><br>which yields θ2 =50.66◦ when θ1 =30◦. The evaluation of δy1, δy2, and δxB in terms of the virtual rotation δθ1 now proceeds as follows.<br><br>Evaluation of δy1<br><br>From the ﬁgure, we see that y1 =(L/2)cosθ1. Forming the differential of both sides and evaluating at θ1 =30◦, we ﬁnd that<br><br>δy1 =<br><br>dy1 dθ1<br><br>δθ1 = −<br><br>L 2<br><br>sinθ1 δθ1 = − 0.2500L δθ1 (c)<br><br>Evaluation of δy2<br><br>From the ﬁgure, y2 = L cosθ1+(L/2)cosθ2. Substituting for θ2 from Eq. (b), and simplifying, gives y2 = (L/2)cosθ1 +0.75L. Taking the differential of each side, and substituting θ1 =30◦, yields<br><br>δy2 =<br><br>dy2 dθ1<br><br>δθ1 = −<br><br>L 2<br><br>sinθ1 δθ1 = − 0.2500L δθ1 (d)|
|---|

|Evaluation of δxB<br><br>From the ﬁgure, xB = L sinθ1 + L sinθ2. In principle, θ2 could be eliminated by using Eq. (b), but this would result in a rather cumbersome expression. It is much easier to form the differentials ﬁrst and then carry out the substitution. From the chain rule for differentiation, we obtain<br><br>δxB =<br><br>∂xB ∂θ1<br><br>δθ1 +<br><br>∂xB ∂θ2<br><br>δθ2<br><br>which gives<br><br>δxB = L cosθ1 δθ1 + L cosθ2 δθ2 (e) From Eq. (b) we obtain the following equation of constraint in terms of δθ1<br><br>and δθ2:<br><br>∂ ∂θ1<br><br>(cosθ1 + cosθ2)δθ1 +<br><br>∂ ∂θ2<br><br>(cosθ1 + cosθ2)δθ2 =0<br><br>or<br><br>−sinθ1 δθ1 − sinθ2 δθ2 =0 which gives<br><br>δθ2 = − (sinθ1/sinθ2) δθ1 (f) Substituting Eq. (f) into Eq. (e), we ﬁnd that<br><br>δxB = L cosθ1 δθ1 + L cosθ2 −<br><br>sinθ1<br><br>sinθ2<br><br><br>δθ1<br><br>which, when evaluated at θ1 =30◦ and θ2 = 50.66◦, yields<br><br>δxB =0.4562L δθ1 (g)<br><br>Virtual Work Equation<br><br>Substituting Eqs. (c), (d), and (g) into Eq. (a) gives<br><br>δU = W(−0.2500L δθ1) + W(−0.2500L δθ1) + P(0.4562L δθ1) = 0<br><br>which simpliﬁes to<br><br>(−0.5W + 0.4562P) δθ1 =0 (h)<br><br>This equation can be satisﬁed for a nonzero δθ1 only if the term in parentheses vanishes, which yields<br><br>P =1.096W Answer Because P is positive, its direction is as shown in the ﬁgure.|
|---|

|Sample Problem 10.3<br><br>The structure shown in Fig. (a) is obtained by ﬁxing point B of the mechanism in Sample Problem 10.2. For θ1 =30◦, determine the pin reactions Bx and By.<br><br>x<br><br>y<br><br>O<br><br>L<br><br>A<br><br>L<br><br>B<br><br>W<br><br>W<br><br>1.5L<br><br>(a)<br><br>θ1=30°<br><br>θ2 = 50.66°<br><br>Solution<br><br>Using θ1 =30◦, we found from geometry in Sample Problem 10.2 that θ2 =50.66◦.<br><br>Because the system in Fig. (a) is a structure rather than a mechanism, it has no DOF. To determine the reactions at B by the method of virtual work, we must turn Bx and By into active forces by removing the support at B.<br><br>Figure (b) shows the system with both Bx and By as active forces. In this case, angles θ1 and θ2 are independent position coordinates; consequently, the system possesses two DOF. The principle of virtual work states that at equilibrium<br><br>δU = W δy1 + W δy2 + Bx δxB + By δyB =0 (a)<br><br>x<br><br>y<br><br>O<br><br>L<br><br>A<br><br>L<br><br>xB<br><br>Bx<br><br>By<br><br>W<br><br>W<br><br>(b)<br><br>y1<br><br>y2<br><br>yB<br><br>θ1= 30°<br><br>θ2 = 50.66°<br><br>|
|---|

|The virtual displacements in Eq. (a) can be related to δθ1 and δθ2 as follows:<br><br>y1 =<br><br>L 2<br><br>cosθ1<br><br>δy1 =<br><br>dy1 dθ1<br><br>δθ1 = −<br><br>L 2<br><br>sinθ1 δθ1 (b)<br><br>y2 = L cosθ1 +<br><br><br>L 2<br><br>cosθ2<br><br>δy2 =<br><br>∂y2 ∂θ1<br><br>δθ1 +<br><br>∂y2 ∂θ2<br><br>δθ2<br><br>δy2 = −L sinθ1 δθ1 −<br><br>L 2<br><br>sinθ2 δθ2 (c)<br><br>xB = L sinθ1 + L sinθ2<br><br>δxB =<br><br>∂xB ∂θ1<br><br>δθ1 +<br><br>∂xB ∂θ2<br><br>δθ2<br><br>δxB = L cosθ1 δθ1 + L cosθ2 δθ2 (d) yB = L cosθ1 + L cosθ2<br><br>δyB =<br><br>∂yB ∂θ1<br><br>δθ1 +<br><br>∂yB ∂θ2<br><br>δθ2<br><br>δyB = −L sinθ1 δθ1 − L sinθ2 δθ2 (e) Substituting Eqs. (b)–(e) into Eq. (a) and regrouping terms, we obtain<br><br>δU = −<br><br>W 2<br><br>sinθ1 − W sinθ1 + Bx cosθ1 − By sinθ1 L δθ1<br><br>+ −<br><br>W 2<br><br>sinθ2 + Bx cosθ2 − By sinθ2 L δθ2 =0<br><br>(f)<br><br>Because δθ1 and δθ2 are independent, Eq. (f) will be satisﬁed only if each of the terms in parentheses is zero; that is,<br><br>−<br><br>3W 2<br><br>sinθ1 + Bx cosθ1 − By sinθ1 =0 (g)<br><br>and<br><br>−<br><br>W 2<br><br>sinθ2 + Bx cosθ2 − By sinθ2 =0 (h)<br><br>Substituting θ1 =30◦ and θ2 =50.66◦, and solving Eqs. (g) and (h) simultaneously, we obtain<br><br>Bx =1.096W and By =0.398W Answer|
|---|

![image 74](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile74.png>)

###### Problems

###### 10.1 Determine the number of DOF for each of the mechanisms shown.

| | |
|---|---|
| | |

(a) (b) (c)

| | |
|---|---|
| | |

| | |
|---|---|
| | |

(d) (e)

(f)

###### Fig. P10.1

###### Neglect friction in the following problems.

- 10.2 The uniform bar of weight W is held in equilibrium by the couple C0. Find C0 in terms of W, L, and θ.

L

B

C0

A

θ

A

L

θ

P

C B

L

Fig. P10.2 Fig. P10.3

- 10.3 Bars AB and AC of the mechanism are homogeneous with each of weight W. Determine the force P required to keep the mechanism in the position shown.

###### 10.1–10.19 Problems 537

- 10.4 The 240-kg uniform block is supported by two bars of negligible mass.

4 m

θ θ

3m

3m

2m

C0

|240 kg|
|---|

Fig. P10.4

Determine the couple C0 that will keep the system in the position θ = 30◦.

| | | |
|---|---|---|
| | |A<br><br>20° 20°<br><br>|
| | | |

P

B

Fig. P10.5

- 10.5 The 1800-kg boat is suspended from two parallel cables of equal length. The location of the center of gravity of the boat is not known. Calculate the force P required to hold the boat in the position shown.

| | |
|---|---|
|2.5in.<br><br>| |
| | |

5in.

5in. 30°

A

C

B

E

D

2.5in.

3 in.

G

C

A

B

P

15 in.

15in. 1.2lb

0.5lb

8in.

θ

A B

b

θ θ

C

a

D

b

P

Fig. P10.6 Fig. P10.7 Fig. P10.8

- 10.6 The 5-lb lamp, with center of gravity located at G, is supported by the parallelogram linkage of negligible weight. Find the tension in the spring AD when the lamp is in equilibrium in the position shown.
- 10.7 Determine the force P that would hold the mechanism in equilibrium in the position θ =40◦.
- 10.8 For the frame shown, ﬁnd the horizontal component of the support reaction at B. Neglect the weights of the members.
- 10.9 The four-bar linkage supports the homogeneous box of weight W.

a

θ a

a

a

b b

|A B W|
|---|

Neglecting the weight of the linkage, determine the horizontal pin reactions at A and B.

Fig. P10.9

###### 10.10 The uniform 320-lb bar AB is held in the position shown by the cable AC. Compute the tension in this cable.

C

Q

35°

B

a

P

θ

18ft

a

40°

A

###### Fig. P10.10 Fig. P10.11

10.11 Determine the ratio P/Q of the forces that are required to maintain equilibrium of the mechanism for an arbitrary angle θ. Neglect the weight of the mechanism.

P 10.12 Neglecting the weights of the members, determine the force P that would B

keep the mechanism in the position shown. The spring DE has a free length of 0.5m and a stiffness of 1.2kN/m.

1.5 m

1.5 m

- 10.13 The linkage of the braking system consists of the pedal arm DAB, the connecting rod BC, and the hydraulic cylinder C. At what angle θ will the force Q be four times greater than the force P that is applied to the pedal? Neglect the weight of the linkage.

100 mm

100 mm

B

C

A D

250 mm

Q

P

θ

θ

C E

48 in.

D

B

CA

50°

38 lb A

54 in. 30 in.

70°

Fig. P10.13 Fig. P10.14

- 10.14 The automatic drilling robot must sustain a thrust of 38 lb at the tip of the

drill bit. Determine the couple CA that must be developed by the electric motor at A to resist this thrust. Neglect the weights of the members.

- 10.15 Determine the couple C for which the mechanism would be in equilibrium in the position θ = 25◦. Neglect the weights of the members.

D E

1.5 m

1.5 m

2 m

A C

Fig. P10.12

B

200mm

200mm

θ

A

80 mm

C

200 N D

###### Fig. P10.15

- 10.16 In the angular motion ampliﬁer, the oscillatory motion of AC is ampli-

30°

60°

120 mm

36 N.m

C0

C

A

| | |
|---|---|
|B| |

B

Fig. P10.16

ﬁed by the oscillatory motion of BC. Neglecting the weights of the members, determine the output torque C0, given that the input torque is 36 N · m.

- 10.17 End B of the 60-lb homogeneous bar is pulled by the 80-lb force inclined

A

L

θ

B

80 lb 45°

60lb

Fig. P10.17

at 45◦ to the horizontal. Find θ, the angle of inclination of the bar.

- 10.18 Calculate the torque C0 that must be applied to the handle of the screw jack in order to lift the load P =3 kN when θ =30◦. The screw has a pitch of 2.5mm. Neglect the weight of the linkage.

C0

P

θ θ

θ θ

A

C

α

B

L

θ

L F

1

θ2

Fig. P10.18 Fig. P10.19

- 10.19 Determine the force F and the angle α required to hold the linkage in

the position θ1 =60◦, θ2 =15◦. Each bar of the linkage is homogeneous and of weight W.

###### *10.5 Instant Center of Rotation

In the previous article, we determined the virtual displacements of points of interest (points of application of forces) by taking the differentials of their position coordinates. Here we introduce a method that does not require differentiation. This approach is based on the concept of instant center of rotation, which is deﬁned as follows:

###### The instant center of rotation of a rigid body is the point in the body that has zero virtual displacement during virtual motion of the body.

To ﬁnd the location of the instant center, consider the virtual motion of the rigid body shown in Fig. 10.12 . Let δrA and δrB be the virtual displacements

Plane of motion

of points A and B in the body. Assume, for the time being, that their directions are not parallel. Now draw a line through point A that is perpendicular to δrA, and another line through B that is perpendicular to δrB. The intersection of these two lines, labeled O in the ﬁgure, is the instant center of rotation of the body. Sometimes O lies outside the body, in which case we imagine that the body is enlarged to include it. The expanded body is called the body extended.

###### B A

δrB

rB

δrA

rA

δθ

We still must show that the virtual displacement of O is zero. Because A, B, and O are points in the same body (or body extended), their virtual displacements satisfy Eq. (10.4):

O

Fig. 10.12

δrA = δrO + δθ × rA (a) δrB = δrO + δθ × rB (b)

where δθ is the virtual rotation of the body, and rA and rB are the position vectors of A and B relative to O. Recalling that δθ is perpendicular to the plane of motion, we deduce from the properties of the vector product that δθ×rA is parallel to δrA. Therefore, Eq. (a) can hold only if δrO is also parallel to δrA. In the same way we can argue that δrO in Eq. (b) must be parallel to δrB. Because a nonzero vector cannot have two different directions, we conclude that δrO = 0.

The term instant center of rotation implies that the body appears to be rotating about O during its virtual displacement. Therefore, once the instant center of rotation has been located, the magnitude of the virtual displacement of any point in the body, such as A, can be obtained from Eq. (10.2):

###### δrA =rAδθ (10.11)

where rA is the distance of A from the instant center of rotation.

In summary, the rules for determining the virtual displacement of a point A in a rigid body are as follows:

- • The magnitude of the virtual displacement is proportional to the distance of A from the instant center of rotation O.
- • The direction of the virtual displacement is perpendicular to the line connecting A and O.
- • The sense of the virtual displacement must be consistent with the sense of the virtual rotation.

The construction shown in Fig. 10.12 for locating the instant center for a rigid body is valid only if the directions of δrA and δrB are not parallel. If the directions are parallel, the instant center can still be located without difﬁculty, as shown in Fig. 10.13. Figure 10.13(a) shows translation, in which the virtual displacements of all points are equal, and the instant center is located at inﬁnity. Figure 10.13(b) depicts the case where δrA and δrB have the same direction but unequal magnitudes, δrA >δrB. In Fig. 10.13(c), δrA and δrB have parallel but opposite directions. (Whether their magnitudes are equal or not is irrelevant.)

δ A

δ

rA

rA

A

δ

rA

δθ

rA

A

O

δ

rB B

δ

rB

rA

B

rB

rB

δ δ

δ

B rB

rA = rB

δθ

O

Point O at ∞

(a)

(b)

(c)

###### Fig. 10.13

We now derive the formulas for the rectangular components of the virtual displacement of a point. These formulas are frequently used in the computation of the virtual work of a force. Let δrA be the virtual displacement of a point A that is located at the distance rA from point O (the instant center of the body containing A). From Fig. 10.14 we see that δxA = −δrA sinθ and δyA =δrA cosθ. Substituting δrA =rA δθ, and noting that rA cosθ = xA and rA sinθ = yA, we obtain

###### δxA = − yA δθ and δyA = xA δθ (10.12)

δrA = rAδθ

δθ

xA

θ

y

A

δθ

yA

yA

rA

θ

x

O

δθ

xA

###### Fig. 10.14

The signs in this equation are consistent with the positive directions of x, y, and δθ shown in Fig. 10.14. However, when solving problems, it is easiest to determine the directions of δxA and δyA by inspection, rather than by adhering to a rigorous sign convention.

|Sample Problem 10.4<br><br>The mechanism in Fig. (a) consists of three homogeneous bars with the weights shown. A clockwise 500-lb·ft couple is applied to bar CD. Using instant centers of rotation, determine the couple C0 that must be applied to bar AB in order to maintain equilibrium.<br><br>500 lb·ft<br><br>6 300 lb 400 lb<br><br>200 lb 4 8<br><br>3 C0<br><br>A<br><br>B<br><br>C<br><br>D<br><br>Dimensions in feet<br><br>(a)<br><br>Solution<br><br>The system possesses one degree of freedom, because only one position coordinate, for example, the angular position of one of the bars, is sufﬁcient to specify its conﬁguration.<br><br>Figure (b) shows a virtual displacement of the system that is consistent with<br><br>(b)<br><br>x<br><br>y<br><br>A<br><br>B<br><br>C<br><br>D<br><br>1<br><br>2<br><br>3<br><br>AB<br><br>BC<br><br>CD<br><br>CD<br><br>BC<br><br>δθAB<br><br>δθ<br><br>δθ θ<br><br>θ<br><br>θ<br><br>(c)<br><br>x<br><br>y<br><br>C<br><br>D<br><br>AB 1<br><br>2<br><br>3<br><br>2 2<br><br>4<br><br>O 3<br><br>3<br><br>3<br><br>8<br><br>3<br><br>A<br><br>B<br><br>rB rC<br><br>CD<br><br>5<br><br>δ δ<br><br>δθ δθ<br><br>(d)<br><br>C 4 2<br><br>O 3<br><br>3 4<br><br>3<br><br>rB<br><br>rC<br><br>4<br><br>10<br><br>3<br>4<br><br><br>B<br><br>BC<br><br>Bar BC extended<br><br>δ<br><br>δ<br><br>δθ<br><br>the constraints, with δθAB, δθBC, and δθCD representing the virtual rotations of the bars. Points 1, 2, and 3 indicate the locations of the centers of gravity of the bars. Note that Fig. (a) is the active-force diagram for the system because only the weights and the two couples are capable of doing work on the system. Applying the principle of virtual work, we obtain<br><br>δU =C0 δθAB − 500 δθCD − 200 δy1 − 300 δy2 − 400 δy3 =0 (a)<br><br>where δy1 is the positive y-component of the virtual displacement of point 1, and so forth. Note the signs in Eq. (a), which follow the rule that virtual work is positive if the force (couple) has the same direction as the displacement (rotation). If these directions are opposite each other, the virtual work is negative.<br><br>The next step in the analysis is to express all of the virtual changes in Eq. (a) in terms of one independent position coordinate, for which we choose θAB. To utilize instant centers, we must ﬁrst locate the instant center for each of the three bars. Referring to Fig. (b), we see that A and D, being ﬁxed points, are obviously the instant centers for bars AB and CD, respectively. Therefore, δrB is perpendicular to AB, and δrC is perpendicular to CD, each directed as shown in Fig. (c). Because B and C also belong to bar BC, the instant center of BC is point O, where the lines that are perpendicular to δrB and δrC intersect. Because point O does not lie on bar BC, it is convenient to think of BC being extended to the triangle BCO, as shown in Fig. (d). From the directions of δrB and δrC, we see that δθBC is clockwise.|
|---|

###### 542

|Figures (c) and (d) show all the dimensions needed for kinematic analysis. We now relate the virtual rotations of BC and CD to δθAB as follows:<br><br>B rotates about A: δrB =5 δθAB ft—see Fig. (c)<br><br>B rotates about O: δrB =10 δθBC ft—see Fig. (d) Equating the right-hand sides of these two equations gives<br><br>δθBC =<br><br>1<br><br>2<br><br><br>δθAB (b)<br><br>C rotates about D: δrC =6 δθCD ft—see Fig. (c)<br><br><br>C rotates about O: δrC =3 δθBC ft—see Fig. (d) Equating the right-hand sides of these two equations, and using Eq. (b), yields<br><br><br>δθCD =<br><br>1 4<br><br>δθAB (c)<br><br>Next, Eq. (10.12) is used to calculate δy1, δy2, and δy3:<br><br>Point 1 rotates about A: from Fig. (c) we ﬁnd<br><br>δy1 =2 δθAB (d)<br><br>Point 2 rotates about O: from Fig. (d), δy2 = 4 δθBC. Substituting for δBC from<br><br><br>Eq. (b), we get<br><br>δy2 =2 δθAB (e)<br><br>Finally, from Fig. (c) we see that<br><br>δy3 =0 (f)<br><br>Substituting Eqs. (b)–(f) into Eq. (a), we obtain<br><br>δU = C0 δθAB − 500<br><br>1 4<br><br>δθAB − 200(2 δθAB) − 300(2 δθAB) − 400(0)=0<br><br>which reduces to<br><br>(C0 − 1125) δθAB =0<br><br>This equation can be satisﬁed for nonzero δθAB only if<br><br>C0 =1125 lb · ft Answer<br><br>Because C0 is positive, it is directed as shown in Fig. (a)—that is, counterclockwise.|
|---|

###### 543

![image 75](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile75.png>)

###### Problems

###### 10.20 Locate the instant center of rotation of bar AB for each case shown.

A

B

###### A B

A

D

D B

(a)

(b)

(c)

D

B

D E

E

A

B A

F

(d)

(e)

###### Fig. P10.20

The following problems are to be solved using instant centers of rotation. Neglect the weights of the members unless otherwise speciﬁed.

2.5 ft

C 10.21 Each of the three uniform bars of the mechanism weighs 12 lb/ft. Deter-

mine the couple C0 that would hold the mechanism in equilibrium in the position shown.

D

2ft

C0

10.22 Determine the force P that will keep the mechanism in equilibrium in the position shown.

B A

1.6 ft

60 lb

Fig. P10.21

14 in.

18 in.

12 in.

P

24 in.

θ

12 in.

18 in.

###### Fig. P10.22

- 10.23 Determine the tension in the cable attached to the linkage at B.

6 ft

3 ft 2 ft 4 ft 4 ft

A

B C E D

F

400 lb

Fig. P10.23, P10.24

- 10.24 Find the couple applied by the built-in support at F to the linkage.
- 10.25 Find the position coordinate x of the sliding weight B for which the scales will be balanced.

x A

25 60 140

40

Dimensions in mm

0.4 kg

0.2 kg B

| |B|
|---|---|
| | |

0.4 m

E 0.3 m D

P A

Fig. P10.25 Fig. P10.26

- 10.26 Compute the force P that will keep the 15-kg uniform plate ABDE in equilibrium in the position shown.
- 10.27 Each bar of the structure is uniform and weighs 50lb. Find the horizontal

C

4ft

4ft

A

60° 60°

B

Fig. P10.27

pin reaction at C.

- 10.28 Determine the force P necessary to keep the mechanism in the position

800

20 kN

400

Dimensions in mm

400

C D

F

P B

E

A

600

300

Fig. P10.28

shown.

- 10.29 If the input force to the compound lever is P = 30 lb, calculate the output force Q.

22 in. 6 in.

P

B D

A Q

4 in.

| | |E|
|---|---|---|
| | | |

6 in.

22 in.

###### Fig. P10.29

- 10.30 Determine the force P required for equilibrium of the compound lever if Q = 4200 N.

B

A

C D

40

Dimensions in mm

P

Q

60

60 80 320

Fig. P10.30

- 10.31 If Q = 200 N, determine the couple C0 required to hold the mechanism in equilibrium in the position θ = 25◦. Neglect friction.

A

B

C

θ Q C0

50mm

40mm

Fig. P10.31

- 10.32 For the automobile suspension shown, ﬁnd the force in the coil spring

210

D

F

E

135

B

C

A

150

BE given that P =2600 N.

Dimensions in mm

- 10.33 The couples C1 and C2 act on the linkage. Find the ratio C1/C2 for which the linkage will be in equilibrium in the position shown.

40 in.

65°

B

A

D

C

C1

C2

60 in.

60in.

7 in.

4 in.

11 in.

13 in.

P

C

B

A

D E

40°

Fig. P10.33 Fig. P10.34

- 10.34 What force P will produce a tensile force of 25lb in the cable at E?
- 10.35 If the force P acting on the piston in the position shown is equal to

135

P

Fig. P10.32

Dimensions in mm

P

###### A

136

B

30° C

58

C0

Fig. P10.35 1600 N, compute C0, the output torque at the crankshaft.

- 10.36 For the pliers shown, determine the relationship between the magnitude of the applied forces P and the magnitude of the gripping forces at E. (Hint: Consider AB to be ﬁxed.)

1.2 in.

P

P

1 in.

1.5 in. 3 in.

E

1.5 in.

A C

B D

Fig. P10.36

- 10.37 When activated by the force P, the gripper on a robot’s arm is able to pick up objects by applying the gripping force F. Given that P =120 N, calculate F in the position shown.

250 mm

160 mm

52 mm

B

65°

C 35°

D

A

F F

P

###### Fig. P10.37

∗10.38 (a) Using a scale drawing, locate graphically the instant center of the connecting rod AB in the position shown. (b) Using the results of part (a) and assuming equilibrium, ﬁnd the couple C0 that acts on the ﬂywheel if the force acting on the piston is P =120 lb.

18.5in.

A

60°

7.5 in. C

P

B

2.5 in.

C0

###### Fig. P10.38

∗10.39 The hinge is of the type used on some automobiles, in which the door DE appears to rotate about point H. Use a graphical construction, drawn to scale, to locate H. (Hint: ABED and BCGF are parallelogram linkages.)

C

A

B

21in.

21in.

30°

P

30°

90°

90°

27in.

G

D

###### C

0

E

12in.

12in.

F

12in.

12in.

H

###### Fig. P10.39

*10.6 Equilibrium and Stability of Conservative

Systems

a. Potential energy

As explained in Art. 10.4, if a frictionless system is given a kinematically admissible virtual displacement, the virtual work has the form [see Eq. (10.10)]

δU = Q1 δq1 + Q2 δq2 + ··· + Qn δqn

where the δq’s are virtual changes in the independent position coordinates and the Q’s are called generalized forces. The system is classiﬁed as conservative if there exists a scalar function V(q1,q2,...,qn) such that

∂V ∂qi

(i =1,2,...,n) (10.13)

Qi = −

The function V is called the potential function, or the potential energy, of the system. Therefore, the generalized forces are said to be derivable from a potential. The minus sign in Eq. (10.13), which is part of the deﬁnition, has its origin in the relationship between work and potential energy.* If each of the forces acting on a system is derivable from a potential, the potential energy of the system is obtained by summing the potential energies of all the forces. For our purposes, we only need to consider gravitational potential energy and elastic potential energy.

*This relationship is treated in Dynamics. Here we discuss only those properties of potential energy that are required for the equilibrium analysis of conservative systems.

10.6 Equilibrium and Stability of Conservative Systems 549

###### b. Gravitational potential energy

y

Figure 10.15 shows a body of weight W whose center of gravity G is a dis-

tance yG above an arbitrary reference line that coincides with the x-axis. The generalized force corresponding to the coordinate yG is −W (the minus sign is necessary because W is directed opposite the positive direction of yG). The potential function of the weight, also called its gravitational potential energy, is Vg = WyG + C, where C is an arbitrary constant. This result is easily veriﬁed by noting that −dVg/dyG = − W, which agrees with Eq. (10.13). Because the weight W is derivable from a potential, it is a conservative force.* Observe that the value of the additive constant C is irrelevant because it does not contribute to the derivative of Vg. Therefore, C is usually taken to be zero, and the gravitational potential energy is written as

G

Arbitrary reference line

yG W

x

Fig. 10.15

Vg = WyG (10.14)

c. Elastic potential energy

Our discussion of elastic potential energy is limited to ideal springs. An ideal spring has the following properties: (1) the weight of the spring is negligible, and (2) the force exerted by the spring is proportional to the elongation of the spring. (The reader should be aware that our consideration of deformable springs represents a radical departure from the analysis of rigid bodies.) The free (unstretched) length of the spring is denoted by L0 and the elongation by s, as shown in Fig. 10.16. If the spring is ideal, the force F applied to the spring is

related to its elongation s by

Unstretched

s

L0

F =ks (10.15)

where k is a constant, called the stiffness of the spring, or the spring constant. The stiffness k has the dimension [F/L]; hence the units are lb/ft, N/m, and so on.

F = ks

Stretched

Letting Qs represent the force exerted by the spring, we have Qs = − ks (the force exerted by the spring is opposite the force exerted on the spring). Note that this expression for Qs is valid for both positive s (tension spring) and negative s (compression spring).

Fig. 10.16

The potential energy of an ideal spring is

- 1

- 2

ks2 (10.16)

Ve =

It can be seen that −dVe/ds = − ks, which is indeed the force Qs exerted by the spring. Because the spring force is derivable from a potential, we conclude that it is a conservative force. The potential energy Ve is called elastic potential energy. When using Eq. (10.16), remember that s is the elongation or contraction of the spring, not the length of the spring.

###### d. Stationary potential energy and stability

In Art. 10.5, we pointed out that a system is in equilibrium only if all the generalized forces vanish—that is, if Q1 = Q2 = ··· = Qn =0. For a conservative

*A similar argument can be used to show that all forces of constant magnitude and direction are conservative.

system with potential energy V(q1,q2,...,qn), the equilibrium conditions thus are

∂V ∂q1 =0,

∂V ∂q2 =0,...,

∂V ∂qn = 0 (10.17)

Equation (10.17) represents the principle of stationary potential energy:

The potential energy of a conservative system is stationary (minimum, maximum, or constant) in an equilibrium position.

Potential energy can also be used to determine whether an equilibrium position is stable, unstable, or neutral. These three classiﬁcations of equilibrium are illustrated in Fig. 10.17. The ball at the bottom of the bowl in (a) is said to be

in stable equilibrium—if the ball is displaced a small amount and then released, it will return to the equilibrium position shown. In (b), the ball is in equilibrium at the top of an inverted bowl. Here the equilibrium is unstable—if the ball is displaced a small amount and then released, it will move away from the original equilibrium position. Neutral equilibrium is shown in (c)—if the ball on a ﬂat surface is displaced a small amount to the left or right and then released, the ball will simply remain at rest in the new position.

- (a) Stable

- (b) Unstable

- (c) Neutral

From the foregoing examples, we can deduce the principle of minimum potential energy:

The potential energy of a conservative system is at its minimum in a stable equilibrium position.

As an illustration of this principle, note that when the ball in Fig. 10.17(a) is displaced, its potential energy is increased. When released, the ball returns to its original position of lower potential energy. However, when the ball in Fig. 10.17(b) is displaced, its potential energy decreases. When released, the ball does not return to its original position of higher potential energy. Instead, the ball seeks a position of lower potential energy—it rolls off the bowl.

Fig. 10.17

We restrict our discussion of stability to systems that possess one degree of freedom—that is, systems for which the potential energy V(q) is a function of a single coordinate q. By the principle of stationary potential energy, the equilibrium positions of the system correspond to the roots of the equation dV/dq = 0. To determine whether the equilibrium positions are stable or unstable, we must investigate the sign of the second derivative, d2V/dq2. If the second derivative is positive at an equilibrium position, the potential energy is a minimum (stable equilibrium); if the second derivative is negative, the potential energy is a maximum (unstable equilibrium).

In summary, if q = q0 is a stable equilibrium position, then dV dq q0 =0

d2V dq2 q0

> 0 (10.18)

and if q = q0 is an unstable equilibrium position, then dV dq q0 =0

d2V dq2 q0

< 0 (10.19)

|Sample Problem 10.5<br><br>A light rod is pin-supported at one end and carries a weight W at the other end, as shown in the ﬁgure. The ideal spring attached to the rod is capable of resisting both tension and compression, and it is unstretched when the rod is vertical. Find the largest value of W for which the vertical equilibrium position of the rod would be stable.<br><br>yG = L cos θ L<br><br>s=bsin θ<br><br>Reference line for Vg<br><br>b<br><br>O<br><br>W<br><br>k<br><br>θ<br><br>Solution<br><br>The potential energy of the system consists of Vg, the gravitational potential energy of the weight, and Ve, the elastic potential energy of the spring. From Eq. (10.14), Vg = WyG, where yG is the vertical distance to W measured from an arbitrary reference line. Choosing the horizontal line passing through O as the reference, we ﬁnd Vg =WLcosθ.<br><br>To determine whether a function evaluated at a point is a minimum or maximum, it is sufﬁcient to investigate the function only in a small neighborhood of that point. Therefore, we can conﬁne our attention to small values of θ. Approximating cosθ with (1 − θ2/2), which is valid for small angles, the gravitational potential energy becomes<br><br>Vg =WL 1 −<br><br>1<br><br>2<br><br><br>θ2 (a)<br><br>From Eq. (10.16), Ve =(1/2)ks2, where s is the elongation (or contraction) of the spring measured from its unstretched position. From the ﬁgure, we see that for sufﬁciently small θ, s =b sinθ. Using the approximation sinθ ≈ θ, the elastic potential energy of the spring becomes<br><br>Ve =<br><br>1<br><br>2<br><br><br>kb2θ2 (b)<br><br>Combining Eqs. (a) and (b), the potential energy of the system is<br><br>V = Vg + Ve =WL 1 −<br><br>1<br><br>2<br><br><br>θ2 +<br><br>1<br><br>2<br><br><br>kb2θ2<br><br>which is valid for small values of θ.<br><br>For the system to be in stable equilibrium, d2V/dθ2 must be positive. After differentiation, we ﬁnd<br><br>dV dθ =(−WL + kb2)θ<br><br>|
|---|

|Observe that dV/dθ =0 when θ =0, conﬁrming that the rod is in equilibrium in the vertical position. Differentiating again, we obtain<br><br>d2V dθ2 = − WL + kb2<br><br>We see that d2V/dθ2 will be positive; that is, the system will be in stable equilibrium, only if kb2 >WL. Therefore, the maximum value of W for which the system will be in stable equilibrium for θ =0 is<br><br>Wmax =kb2/L Answer<br><br>Sample Problem 10.6<br><br>For the system shown, determine (1) all values of θ at equilibrium; and (2) the stability of each equilibrium position. The homogeneous rod AB weighs 80lb, and the ideal spring is unstretched when θ =0. Neglect friction and the weights of the sliders at A and B.<br><br>yG = 6cos θ<br><br>Reference line for Vg<br><br>s = 12sin k = 6 lb/ft<br><br>12 ft<br><br>W = 80 lb<br><br>B<br><br>G<br><br>A<br><br>θ<br><br>θ<br><br>Solution<br><br>The potential energy V of the system consists of the potential energy of the weight Vg and the potential energy of the spring Ve. From Eqs. (10.14) and (10.16), we have<br><br>V = Vg + Ve = WyG +<br><br>1<br><br>2<br><br><br>ks2 (a)<br><br>where yG is the vertical distance of the center of gravity G of bar AB above the chosen reference line, and s is the elongation of the spring. As shown in the ﬁgure, we have yG = 6cosθ ft and s =12sinθ ft (recall that the spring is unstretched|
|---|

###### 552

|when the rod is vertical). Therefore, the potential energy in Eq. (a) becomes<br><br>V = 80(6cosθ) +<br><br>1<br><br>2<br><br><br>(6)(12sinθ)2<br><br>= 480cosθ + 432sin2 θ lb · ft (b) The ﬁrst derivative of the potential energy is<br><br>dV dθ = − 480sinθ + 864sinθ cosθ lb · ft (c)<br><br>Using d(sinθ cosθ)/dθ = cos2 θ − sin2 θ, the second derivative of the potential energy is<br><br>d2V dθ2 = − 480cosθ + 864(cos2 θ − sin2 θ) lb · ft (d)<br><br>Part 1<br><br>According to the principle of minimum potential energy, the values of θ at equilibrium are the roots of the equation dV/dθ =0. Using Eq. (c), we ﬁnd that the equilibrium condition is<br><br>−480sinθ + 864sinθ cosθ =0 or<br><br>sinθ(−480 + 864cosθ)=0<br><br>The roots of this equation are sinθ =0 and cosθ = 480/864. Consequently, the equilibrium positions are<br><br>θ =0 θ = cos−1<br><br>480 864 = 56.25◦ Answer<br><br>Part 2<br><br>Evaluating the second derivative of the potential energy, Eq. (d), at the equilibrium position θ =0, we ﬁnd<br><br>d2V dθ2 = − 480 + 864=384 lb · ft<br><br>Because d2V/dθ2 > 0, we conclude that θ =0 is a stable equilibrium position. For θ =56.25◦, Eq. (d) gives<br><br>d2V dθ2 = −480cos56.25◦ + 864(cos2 56.25◦ − sin2 56.25◦)<br><br>= −597 lb · ft<br><br>Because d2V/dθ2 <0, we deduce that θ =56.25◦ is an unstable equilibrium position.|
|---|

![image 76](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile76.png>)

###### Problems

Neglect friction in the following problems, unless otherwise stated. 10.40 Show that θ =0 represents the only equilibrium position of the uniform

B

bar AB. Is this position stable or unstable?

θ

- 10.41 The weight W is suspended from end B of the weightless bar that is supported by walls at A and C. Determine the equilibrium value of the angle θ and investigate the stability of equilibrium.

B

C

1 m

2m

W A

θ

A

R

L

B

θ

Fig. P10.41 Fig. P10.42

- 10.42 The uniform bar of weight W and length L = 2R rests in a hemispherical cavity of radius R. Calculate the angle θ for equilibrium and investigate the stability of equilibrium.
- 10.43 A slender homogeneous bar is bent into a right angle and placed on a

A

α α

Fig. P10.40

cylindrical surface. Determine the range of b/R for which the equilibrium position shown is stable.

b b

R

- 10.44 The body shown is a composite of a hemisphere and a cylinder, with both of uniform weight density γ. Determine the range of h/R for which the equilibrium position shown is stable.

R

h

2h G

O

R

Fig. P10.44 Fig. P10.45

- 10.45 The uniform block of height 2h is balanced on the rough cylindrical surface of radius R. Show that this equilibrium position is stable only if R > h. Assume that friction prevents the block from sliding.
- 10.46 The uniform bar AB of weight W and length L is pinned to a sliding collar at A and to the sliding rod BD at B. The spring wound around rod BD has

Fig. P10.43

a stiffness k and is undeformed when rod AB is in the position θ = 0. Determine the expression for the angle θ (other than θ = 90◦) at equilibrium and investigate the stability of equilibrium for this position.

D

k

C

A

θ

L

B

###### Fig. P10.46

- 10.47 Uniform rods of weights W1 and W2 are welded to the two pulleys that are connected by a belt. Determine the range of W1/W2 for which the equilibrium position shown is stable.

| | |
|---|---|
|2R|W2<br><br>R|

W1

3R 1.5R

2

L

A B k k

b b

Fig. P10.47 Fig. P10.48

- 10.48 The weight of the uniform bar of length L is W. The base of the bar is supported by a pin and two springs. The springs (each of stiffness k) are undeformed when the base is horizontal. Determine the smallest dimension b of the base for which the bar is stable in the position shown.
- 10.49 The semi-cylinder of radius r is placed on a cylindrical surface of radius

W r

R

Fig. P10.49

R. Assuming no slipping, determine the range of R/r for which the equilibrium position shown is stable.

- 10.50 Find the equilibrium positions of the mechanism shown and investigate

| | |
|---|---|
|6 lb| |

12in.

12in.

θ

k

k = 1.0 lb/in.

their stability. The spring is undeformed in the θ = 0 position. Neglect the weight of the mechanism.

Fig. P10.50

W

10.51 Determine the largest weight W for which the hinged bar ABC will be in

stable equilibrium in the position shown. The ideal spring of stiffness k is capable of carrying tension and compression and is undeformed in the position shown. (Hint: Use sinθ ≈ θ and cosθ ≈ 1 − θ2/2.)

A

- a

k

- b

10.52 The spring is connected to a rope that passes over the cylindrical surface and is attached to corner A of the rocker. The spring has a stiffness k and is undeformed when θ = 0. When the weight W is suspended from A, the equilibrium position of the rocker is θ = 30◦. Determine if this equilibrium position is stable. Neglect the weight of the rocker.

B

k

| | |
|---|---|
| | |
| | |

C

θ A

| | |
|---|---|
|W| |

R

20 lb

Fig. P10.51

6 ft

6ft 40lb

θ

###### Fig. P10.52 Fig. P10.53

∗10.53 Find the equilibrium positions of the 40-lb homogeneous bar and investigate their stability.

- 10.54 The mechanism of negligible weight supports the weight W. Find the value of θ for equilibrium. Is the equilibrium position stable or unstable?

A B

b b

b b

C D

W

θ

Fig. P10.54, P10.55

- 10.55 Solve Prob. 10.54 assuming that A and B are connected by a spring of stiffness k =0.3 W/b and free length b.
- 10.56 The stiffness of the ideal spring that is compressed by the slider C is

A

0.2m

0.2m

θ

k

B

C

0.2m 0.2m

0.2m

0.2m

k =250N/m. The spring is unstretched when θ =20◦. When the mass m is suspended from A, the system is in equilibrium at θ = 60◦. Determine the value of m and whether the equilibrium position is stable or unstable.

| | | |
|---|---|---|
|m| | |

10.57 Find the stable equilibrium position of the system described in Prob. 10.56 if m =2.06 kg.

Fig. P10.56, P10.57

- 10.58 The uniform bar AB of weight W =kL is in equilibrium when θ =65◦. Find the value of θ for which the ideal spring would be unstretched, and investigate the stability of the equilibrium position.
- 10.59 The weight of the uniform bar AB is W. The stiffness of the ideal spring attached to B is k, and the spring is unstretched when θ =80◦. If W =kL, the bar has three equilibrium positions in the range 0<θ <π, only one of which is stable. Determine the angle θ at the stable equilibrium position.

L

A

B k

θ

5in.

5in.

5 in.

5 in.

B

E

D

A F

C

k = 7.5 lb/in.

5 lb

θ

Fig. P10.58, P10.59 Fig. P10.60

- 10.60 The weightless bars AB and CE, together with the 5-lb weight BE, form a parallelogram linkage. The ideal spring attached to D has a free length of 2in. and a stiffness of 7.5 lb/in. Find the two equilibrium positions that are in the range 0<θ <π/2, and determine their stability. Neglect the weight of slider F.
- 10.61 The three ideal springs supporting the two bars that are pinned together

at C are unstretched when θ1 =θ2 =0. Note that the springs are always vertical because the collars to which they are attached are free to slide on the horizontal rail. Compute the angles θ1 and θ2 at equilibrium if W =kL /10.

A

B

k

C

θ

θ

D E

- 1

2

k

k

L

- 2

L 2 L

2 L 2

| | | |
|---|---|---|
|W| | |

| | | |
|---|---|---|
|W| | |

L A 3

B

C

k

k

k

- 2L
- 3

L 2

θ

Fig. P10.61 Fig. P10.62

- 10.62 The bar ABC is supported by three identical, ideal springs. Note that the springs are always vertical because the collars to which they are attached are free to slide on the horizontal rail. Find the angle θ at equilibrium if W =kL. Neglect the weight of the bar.

![image 77](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile77.png>)

###### Review of Equations

###### Virtual displacements

Translation : δrA = δrB Rotation about ﬁxed point : δrB = δθ × rAB

General plane motion : δrB = δrA + δθ × rAB Point O is instant center of AB : δrA = δθ × rOA

δrB = δθ × rOB

###### Virtual work

δU = F·δr= F cosα δr (work of a force) δU = C·δθ= C δθ (work of a couple)

α = angle between F and δr

###### Method of virtual work

If a body is in equilibrium, then the virtual work of all forces acting on the body is zero for all kinematically admissible virtual displacements of the body from the equilibrium position (δU = 0).

###### Potential energy

Vg = WyG (gravitational potential energy) Ve =

1 2

ks2 (elastic energy of a spring)

k = spring stiffness s = elongation of spring

###### Principle of stationary potential energy

The potential energy of a conservative system is minimum in a stable equilibrium position.

# A

### Numerical Integration

###### A.1 Introduction

The purpose of numerical integration, also known as quadrature, is to evaluate deﬁnite integrals of the type

b

f(x) dx (A.1)

A =

a

without using calculus. Quadrature gives only an approximate value for the integral, because calculus is the only method for performing the integration exactly. Numerical integration is useful in the following situations:

- • The integration is difﬁcult or tedious to perform analytically.
- • The integral cannot be expressed in terms of known functions.
- • The function f(x) is unknown, but its values are known at discrete points.

Generally speaking, integral is a mathematical term for the sum of an inﬁnite number of inﬁnitesimal quantities. Consequently, the deﬁnite integral in Eq. (A.1) represents the summation of all the differential (inﬁnitesimal) areas dA= f(x) dx that lie between the limits x =a and x =b, as seen in Fig. A.1. In numerical

y

Area = A y = f(x)

integration, the integral is approximated by adding the areas A1, A2, A3, . . . , An, of n (ﬁnite) panels, each of width x, as shown in Fig. A.2. Because the area of each panel must be estimated (integral calculus would be required to obtain the exact values), quadrature yields only an approximate value of the integral; that is,

dA f(x)

x

a b

n

dx

A ≈

Ai

Fig. A.1

i=1

As a rule, a larger number of panels, with correspondingly smaller x, yields a more accurate result.

There are several methods available for estimating the areas of the panels. We discuss only the trapezoidal rule and Simpson’s rule.

###### 559

###### 560 APPENDIX A Numerical Integration

y

A3

An

A2

A1

f1 f2 f3 f4

fn fn + 1

x

a b

Dx nDx

###### Fig. A.2

###### A.2 Trapezoidal Rule

In the trapezoidal rule, each of the n-panels is approximated by a trapezoid. Recalling that the area of a trapezoid is (base)×(average height), the area of a typical panel in Fig. A.2 is

fi + fi+1 2

x (A.2)

Ai =

Adding the areas of all of the panels, we get

n

x 2

###### (A.3)

A ≈

Ai = ( f1 + 2 f2 + 2 f3 + ··· + 2 fn + fn+1)

i=1

Equation (A.3) is known as the trapezoidal rule. The trapezoidal rule is sometimes written in the following form.

n+1

Wi fi (A.4)

A ≈

i=1

where the Wi are known as the weights and the expression i n=+11Wi fi is called the weighted summation. For the trapezoidal rule, the weights are

x 2

W1 = Wn+1 =

(A.5) Wi = x for 2 ≤ i ≤ n

###### A.3 Simpson’s Rule

In the trapezoidal rule, the function f(x) is approximated by a straight line within each panel of width x; that is, the curvature of f(x) is neglected. This linearization may result in an unacceptably large error in the quadrature, particularly if the curvature of f(x) is large and of the same sign throughout the interval a ≤ x ≤b.

###### A.3 Simpson’s Rule 561

Simpson’s rule overcomes this deﬁciency by replacing the straight lines with parabolas. Because three points—that is, three values of f(x)—are required to deﬁne a parabola, Simpson’s rule approximates the area of a pair of adjacent panels.

Figure A.3 shows two adjacent panels bounded by a parabola that passes through the three panel points. It can be shown that the area under the parabola is

fi + 4 fi+1 + fi+2 3

Ai + Ai+1 =

x

y

Ai+1 Ai

fi+1 fi+2

fi

x

∆x ∆x

###### Fig. A.3

Adding the areas of all the panels yields Simpson’ rule

n−1

A ≈

(Ai + Ai+1)

i=1,3,5,...

###### (A.6)

x 3

= ( f1 + 4 f2 + 2 f3 + 4 f4 + ··· + 2 fn−1 + 4 fn + fn+1)

Note that the number of panels in Simpson’s rule must be even. Introducing the concept of weights Wi, Simpson’s rule can be written as

n+1

Wi fi (A.7)

A ≈

i=1

where the weights are

x 3

W1 = Wn+1 =

4 x 3

Wi =

i even

2 ≤ i ≤ n (A.8)

- 2 x

- 3

Wi =

i odd

Because of its greater accuracy, Simpson’s rule should be chosen over the trapezoidal rule. If the number of panels is odd, the area of one panel should be calculated using the trapezoidal rule, and then Simpson’s rule can be used for the remaining panels.

|Sample Problem A.1<br><br>Evaluate the integral A = 0 π/2 sin x dx (x is measured in radians) with four panels, using (1) the trapezoidal rule; and (2) Simpson’s rule.<br><br>Solution<br><br>Because the range of integration is 0 ≤ x ≤ π/2 rad and the number of panels is four, we get x = (π/2)/4 = π/8 rad. The following table is convenient for carrying out the quadrature.<br><br>i x(rad) f(x) = sin x<br><br>1 0 0<br>2 π/8 0.3827<br>3 π/4 0.7071<br>4 3π/8 0.9239<br>5 π/2 1.0000<br><br><br>Part 1: Trapezoidal Rule Using Eq. (A.3) wih n = 4 and x = π/8 rad, we get<br><br>A ≈ ( f1 + 2 f2 + 2 f3 + 2 f4 + f5)<br><br>x 2<br><br>= [0 + 2(0.3827 + 0.7071 + 0.9239) + 1.0]<br><br>π 16<br><br>= 0.9871 Answer<br><br>Part 2: Simpson’s Rule With n = 4 and x = π/8 rad, Eq. (A.6) becomes<br><br><br>A ≈ ( f1 + 4 f2 + 2 f3 + 4 f4 + f5)<br><br>x 3<br><br>= [0 + 4(0.3827) + 2(0.7071) + 4(0.9239) + 1.0]<br><br>π 24<br><br>= 1.0002 Answer<br><br>Because the exact value of the integral is 1.0000, you can see that Simpson’s rule is considerably more accurate than the trapezoidal rule for this problem. A major source of error in the trapezoidal rule is that the curvature of the function<br><br>f (x) = sin x has the same sign throughout the interval 0 ≤ x ≤ π/2 rad. As mentioned previously, the trapezoidal rule does not perform well in problems of this type.|
|---|

###### 562

# B

### Finding Roots of Functions

###### B.1 Introduction

The solutions of the equation f (x) = 0, where f (x) is a given function, are called the roots of f (x). In many practical applications, f (x) is nonlinear in x, in which case it may be difﬁcult or even impossible to ﬁnd the roots analytically. Examples of such nonlinear functions are f (x) = ex cos x−1 and f (x) = x4−2x3+6x−5. Here we introduce two popular numerical methods for root ﬁnding: Netwon’s method (also known as Newton-Raphson iteration) and the secant method. Both methods work by iteration and require a good starting value (initial guess) of the root. If the starting value is not sufﬁciently close to the root, the procedures may fail. Frequently, the physical principles of a problem suggest a reasonable starting value. Otherwise, a good estimate of the root can be obtained by sketching f (x) versus x. (This involves, of course, evaluating the function at various values of x.) If the initial value is not close enough to the root, two problems may arise:

- • The iterative procedure will not converge to a single value of x.
- • The procedure will converge to a root that is different from the one being sought. (Recall that nonlinear equations may have multiple roots.)

###### B.2 Newton’s Method

Consider the problem of computing the root x0 of the function f (x) that is plotted in Fig. B.1. We begin by estimating the value x1 of the root and computing f (x1); the corresponding point is denoted A in the ﬁgure. The next step is to compute

f (x1) (the prime indicates differentiation with respect to x), which represents the slope of the straight line that is tangent to f (x) at A. The coordinate of the point where the tangent line crosses the x-axis is denoted x2. If x1 is close to x0, then the tangent line is a good approximation of f (x) in the vicinity of the root. Consequently, x2 should be a better approximation of the root than x1.

The value of x2 can be computed from the shaded triangle in Fig. B.1: tanθ = f (x1)/(x1 − x2). Substituting tanθ = f (x1) and solving for x2 yield

f (x1) f (x1)

x2 = x1 −

###### 563

###### 564 APPENDIX B Finding Roots of Functions

f(x)

Tangent line at A

A

f(x)

f(x1) θ

x x0 x2 x1

###### Fig. B.1

This completes one cycle of the iteration process. The procedure is then repeated with the output of each iterative step (e.g., x2) being used as the input for the next step, until the change in x between successive steps is negligible. The algorithm for Newton’s method can thus be summarized as follows:

estimate x do until | x| <

f (x) f (x)

(B.1)

x ← −

x ← x + x end do

where a ← b means “b replaces a” and where is the convergence parameter (a small number that signals that the desired accuracy has been achieved).

The main drawback of Newton’s method is that it requires the derivative of

f (x). If f (x) is a simple expression, then deriving f (x) is only a minor nuisance. However, in cases where f (x) is a complicated function, methods that do not require the derivative are more attractive.

###### B.3 Secant Method

The secant method is based on the same principle as Newton’s method. However, instead of requiring the derivative of f (x), it requires two starting values (initial guesses) of the root. These starting values are denoted x1 and x2 in Fig. B.2, and the corresponding points on the plot of f (x) are labeled A and B, respectively. (In the ﬁgure, we assume that x1 > x2, but this need not be the case.) The role that was played by the tangent line in Newton’s method is now taken over by the chord AB; that is, the chord AB will be a good approximation of f (x) in the vicinity of the root x0 if the starting values are close enough to the root.

###### B.3 Secant Method 565

f(x)

Chord AB

A

B

f(x1) f(x2)

f(x)

x x2 x1

x3

x0

###### Fig. B.2

From similar triangles in Fig. B.2 we get

f (x1) − f (x2) x1 − x2

f (x2) x2 − x3 =

which yields

x1 − x2 f (x1) − f (x2)

x3 = x2 − f (x2)

Repeating this procedure using x2 and x3 as the new input values (x1 is discarded) will further improve the estimation of the root. The computations continue until x3 shows no signiﬁcant change—that is, until the change in x is insigniﬁcant. The summary of the algorithm for the secant method is

estimate x1 and x2 do until | x| <

x1 − x2 f (x1) − f (x2)

x ← − f (x2)

###### (B.2)

x3 ← x2 + x x1 ← x2 x2 ← x3

end do

|Sample Problem B.1<br><br>Find the smallest positive, nonzero root of f (x) = ex cos x − 1 within ﬁve signiﬁcant digits. Use (1) Newton’s method; and (2) the secant method.<br><br>Solution<br><br>To obtain an approximate value of the desired root, we plot f (x) in increments of<br><br>x = 0.5, starting at x = 0 and ending after f (x) reverses its sign. The results<br><br>are shown in the ﬁgure. By inspection we estimate the root to be approximately<br><br>x = 1.3. Part 1: Newton’s Method<br><br><br>0.5 1.0<br><br>1.5 0<br><br>f(x)<br><br>x<br><br>0.447<br><br>0.469<br><br>–0.683<br><br>Newton’s method requires the derivative of f (x), which is<br><br>f (x) =<br><br>d dx<br><br>(ex cos x − 1) = ex(cos x − sin x)<br><br>The following table shows the computations for the root, based on the algorithm given in Eq. (B.1). The starting value was x = 1.3.<br><br>x f(x) f (x) x<br><br>1.3 −0.01847 −2.55405 −0.00723 1.29277 −0.00018 −2.50316 −0.00007 1.29270 0.00000 −2.50264 0.00000<br><br>The ﬁnal result, x = 1.2927, has been obtained in only two iterations because of the accuracy of our initial estimate.<br><br>Part 2: Secant Method<br><br>We chose x1 = 1.2 and x2 = 1.3 as the starting values of the root. The algorithm in Eq. (B.2) leads to the following sequence of computations.<br><br>x1 x2 f(x1) f(x2) x x3=x2+ x<br><br>1.2 1.3 0.203 07 −0.018 47 −0.008 34 1.291 66<br>1.3 1.291 66 −0.018 47 0.002 58 0.001 03 1.292 69<br><br><br>1.291 66 1.292 69 0.002 58 0.000 03 0.000 01 1.292 70<br>1.292 69 1.292 70 0.000 03 0.000 00 0.000 00 1.292 70<br><br><br>Referring to the ﬁrst row in the table, note that x1 and x2 are entered ﬁrst, and then the remaining entries in the row are computed using the algorithm. In the second row, the values for x1, x2, and f (x1) are simply copied from the appropriate columns in the ﬁrst row. This pattern is repeated in subsequent rows.<br><br>Once again, the ﬁnal result (x3) is 1.2927, with only three iterations required. In general, the secant method converges a little more slowly than Newton’s method.|
|---|

###### 566

# C

### Densities of Common Materials

ρ kg/m3

γ lb/ft3

γ lb/in.3

Aluminum 2660 166 0.096 Brass 8300 518 0.300 Brick 2000 125 0.072 Cast iron 7200 449 0.260 Concrete 2400 150 0.087 Copper 8910 556 0.322 Earth (dry) 1280 80 0.046 Earth (wet) 1760 110 0.064 Glass 2590 162 0.094 Ice 900 56 0.032 Lead 11370 710 0.411 Oil 900 56 0.032 Steel 7850 489 0.283 Water (fresh) 1000 62.4 0.036 Water (ocean) 1030 64 0.037 Wood, hard (white oak) 800 50 0.029 Wood, soft (Douglas ﬁr) 480 30 0.017

###### This page intentionally left blank

### Answers to Even-Numbered Problems

1.58 (a) 39i + 63j − 42k ft2; (b) 39i + 26j + 18k N·m;

###### Chapter 1

(c) −28i − 25j + 10k m2 1.60 A × B = C × B = 1.8i − 3j m2 1.62 28.0◦ 1.64 (c) and (d) 1.66 ±(0.422i + 0.211j + 0.844k) 1.68 −17.52 lb 1.70 Parallel: 1.581(0.949i + 0.316k) in., Perpendicular:

- 1.2 23.5 lb

- 1.4 14.75 lb·ft·s2

- 1.6 (No answer)

- 1.8 (a) 25 000 m/s; (b) 5930 mi/h

- 1.10 (a) [FLT2]; (b) [ML2]

- 1.12 [c] = [FTL−1], [k] = [FL−1], [P0] = [F], [ω] = [T−1]

6.89(0.218i + 0.725j − 0.653k) in. 1.72 5 m 1.74 (No answer)

- 1.14 (a) 66 000 lb·ft/s; (b) 89.5 kW

- 1.16 7.46 × 10−11 lb

- 1.18 (No answer)

- 1.76 (No answer)

Chapter 2

- 2.2 413 lb at 53.8◦ 2.4 P = 109.6 kN, θ = 29.9◦ 2.6 (a) 367 lb; (b) (0, 1.314 ft, 0.651 ft) 2.8 R =−24.2i − 24.5j + 205.1k kN, xA = 0.708 m,

- 1.20 13 790 km

![image 78](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile78.png>)

- 1.22 3.61 m/s at 26.3◦

- 1.24 Lift = 6220 lb , Drag = 653 lb →

![image 79](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile79.png>)

- 1.26 7.55 mi/h at 25.2◦

![image 80](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile80.png>)

- 1.28 F1 = 323 N, F2 = 411 N

- 1.30 2210 ft along OB, 2570 ft along OC

- 1.32 α = 21.6◦, β = 19.9◦

![image 81](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile81.png>)

- 1.34 (a) 71.8◦ ; (b) 235 lb

yA = 0.716 m 2.10 P1 = 62.3 kN, P2 = 44.6 kN 2.12 P = 38.9 lb, R = 32.8 lb 2.14 Q1 = 121.7 lb, Q2 = 0, Q3 = 203 lb 2.16 θ = 69.2◦, R = −10.99i + 133.45k N 2.18 −108.4i + 121.8j − 820.4k lb 2.20 234 lb 2.22 132.0 N·m CW 2.24 1.378 m 2.26 −560i + 200j N 2.28 (a) 400 kN·m CCW; (b) 400 kN·m CW; (c) 0 2.30 38.9 lb 2.32 6020 lb

- 1.36 a = 494 m, b = 372 m

![image 82](<Engineering Mechanics Statics 3th Ed Pytel Kiusalaas_images/imageFile82.png>)

- 1.38 222 N, 21.1◦

- 1.40 −9.64i + 16.70j + 22.98k lb

- 1.42 (a) 54.5◦; (b) 154.3i + 120.0j + 139.3k N

- 1.44 (a)−0.269i + 0.875j + 0.404k; (b) −1.61i + 5.24j + 2.42k m/s

- 1.46 63.0i − 52.5j − 87.6k lb

- 1.48 θx = 54.8◦, θy = 67.4◦, θz = 136.1◦

- 1.50 −96.0i + 123.5j − 85.8k lb

- 1.52 146i − 48j lb

- 1.54 P = 717 lb, Q = 590 lb

- 1.56 P = 74.3 lb, Q = 69.9 lb

- 2.34 −14.75i − 11.47j + 10.32k N·m

3.6 P = 222i − 150j lb, b = 3.90 in. 3.8 R = 40k lb, CR = 1046i − 1256j lb·ft

- 2.36 (a) −73.0j N·m; (b) −87.7i − 121.7k N·m

3.10 (a) R = 2i + 6j lb, CR = −6j lb·in.;

- 2.38 (a) 84.5i + 136.0j + 181.3k kN·m; (b) 84.5i + 181.3k kN·m

- (b) R = 4i + 6j + 3k lb, CR = 0;
- (c) R = 2i + 6j lb, CR = −6j lb·in.;
- (d) R = 0, CR = −15i + 8j lb·in.;
- (e) R = 0, CR = −15i + 8j lb·in.;
- (f) R = 0, CR = 0; (a) and (c) are equivalent, (d) and (e) are equivalent

- 2.40 150.5i−190.9j lb·ft

- 2.42 MO = 233 lb·in., cosθx = 0.487, cosθy = 0.133, cosθz = 0.864

- 2.44 MO = 7.94 N·m, cosθx = −0.327, cosθy = 0.818, cosθz = −0.473

3.12 R = −13.7i − 50.3j + 25.7k kN,

###### 2.46 y = 4.60 ft, z = 2.90 ft

CR = 102.9i + 150.0j + 54.9k kN·m 3.14 R = −36i − 30k lb, CR = 15i − 162k lb·ft 3.16 (1) R = 300i lb intersecting y-axis at y = 3 in.;

- 2.48 (a) 36 kN·m; (b) 36 kN·m; (c) 32 kN·m; (d) 0; (e) 0

- 2.50 (a) 432 lb·ft; (b) 432 lb·ft

- (2) R = 200i − 200j N intersecting x-axis at x = −4 m;
- (3) R = −600i − 400j kN passing through O;
- (4) R = −600i + 800j lb intersecting x-axis at x = −30 ft

- 2.52 415 N·m

- 2.54 F = 32.0 N, d = 0.450 m

###### 2.56 −75.0 lb·ft

- 2.58 −74.6i − 96.0k N·m

- 2.60 116.2 lb

3.18 P = 348 lb, θ = 33.7◦ 3.20 P = 45.4 lb, R = 175.3i − 75.0j lb 3.22 (a) CR = 450 N·m CCW; (b) R = 207i N intersecting y-axis at y = −2.17 m 3.24 (a) R = −60i N acting through O;

- 2.62 528 lb·ft

- 2.64 0.327 m

- 2.66 −208 lb·in.

- 2.68 (b), (c), (d), (f), and (g)

- 2.70 19.55 lb·ft CW

(b) R = −60i N intersecting y-axis at y = 1.5 m 3.26 C = 30 lb·ft CCW, R = 80 lb → 3.28 P1 = 103.7 kN, P2 = 49.8 kN, P3 = 82.9 kN 3.30 (a) R = −50k lb passing through point (4 ft, 5 ft, 0);

- 2.72 192.1 lb·ft

- 2.74 −106.2i + 140.7j + 280.7k lb·in.

- 2.76 99.0 mm

- 2.78 339 lb·ft

- (b) R = 50k kN passing through point (5 m, 0, 0);
- (c) R = 40k N passing through point (10 m, 8 m, 0)

- 2.80 R = 900 lb, C0 = 3120 lb·in.

- 2.82 (c) and (e)

, CR = 56 N·m CCW; (b) FA = 253 N , FB = 373 N

3.32 R = 82i − 1411j + 406k lb at the point of

- 2.84 (a) R = 120 N

concurrency 3.34 P1 = 805 lb, P2 = P3 = 338 lb 3.36 CR = 18i − 12j kN·m 3.38 P1 = 28.8 lb, P2 = −16.8 lb, C = 540 lb·in. 3.40 R = −380k lb passing through point

- 2.86 R = 25.0i − 133.3j lb, CR = 210k lb·in.

###### 2.88 R = 100 N , CR = 60i − 50j N ·m 2.90 R = P = −33.3i − 22.2k lb,

CR = −157.3i − 10.6j + 166.4k lb·ft 2.92 R = 3.15i − 3.75j + 8.49k lb,

(−1.474 ft, −1.001 ft, 0) 3.42 P = 1063 lb, Q = 915 lb, R = −1425j − 3660k lb 3.44 R = 250i + 360j − 400k N,

CR = 54.5i + 11.81j + 45.0k lb·ft 2.94 97.9 lb

CtR = 246i + 354j − 393k N·m, passing through point (0.991 m, −2.39 m, 0)

- 2.96 T1 = 79.4 N, T2 = 151.6 N, T3 = 220.3 N

- 2.98 65.8 lb

- 2.100 (a) 1200j + 1200k lb·ft; (b) 1477 lb·ft

3.46 R = 13.2 lb acting at center of sign 3.48 R = 15 200 lb

- 2.102 (a) Show that F·C = 0; (b) (−1.2 in., −1.6 in., 0)

, x¯ = 8.75 ft 3.50 R = (−w0L/4)(i + j), x = 0.833L 3.52 R = −76970j lb passing through point

###### 2.1062.104 107x =.3Llb/2, R = P

- 2.108 −120i − 80j − 80k N·m

- Chapter 3

- 3.2 R = 56 kN , CR = 266 kN·m CCW

(59.1 ft, 0, 135.6 ft)

3.54 R = (−237i − 45.0j) × 103 lb acting through point

(−24.3 ft, 0) 3.56 343i + 201j lb 3.58 R = −400k kN, x = 1.0 m, y = 1.125 m 3.60 (4.67 ft, 5.33 ft, 0)

- 3.4 R = 154 lb , CR = 115.2 lb·in. CW

###### Chapter 4 571

- 3.62 (a) R = −200i + 300j + 150k lb, CR = 1250i + 600j + 1000k lb·ft; (b) R = −200i + 300j + 150k lb, CR = −104.9i + 157.4j + 78.7k lb·ft, passing through point (−2.95 ft, 9.03 ft, 0)

4.66 6 unknowns, 6 independent eqs. 4.68 9 unknowns, 9 independent eqs. 4.70 (No answer) 4.72 (No answer) 4.74 5.03 kN 4.76 1416 N 4.78 1.5W cotθ 4.80 RA = 411 N, RC = 416 N 4.82 NA = 55.6 kN, NB = 10.12 kN, NC = 32.4 kN 4.84 200 lb 4.86 T = 3530 N, NB = 6530 N 4.88 280 lb 4.90 7200 lb 4.92 36.7 lb 4.94 24.0 N·m 4.96 (a) TA = 68.9 lb, TB = 126.1 lb;

- 3.64 P = 38.9 kN, R = 125.5i kN

- 3.66 R = 131.3i + 210j + 221k lb, CR = 6700i − 630j − 10 270k lb·in.

- 3.68 452 lb

- 3.70 T1 = 654 N, T2 = 425 N, R = −1441 N

- Chapter 4

- 4.2 3 unknowns 4.4 4 unknowns 4.6 (a) 3 unknowns; (b) 4 unknowns; (c) 3 unknowns;

(b) NA = 101.1 lb, NB = 63.9 lb

(d) 3 unknowns

4.98 2690 N 4.100 PBC = 10.0 kips, PBD = 20.0 kips, E = 19.70 kips 4.102 623 lb·in. 4.104 21.2 N 4.106 27.8 kips at A, 31.6 kips at C 4.108 PAB = 3.13 MN, PCD = 5.50 MN 4.110 877 N 4.112 A = 672 lb, C = 582 lb, E = 336 lb 4.114 55.6 mm 4.116 E = 6P 4.118 10P 4.120 1294 lb 4.122 RC = 169.7 lb, NB = 120.0 lb 4.124 29.6 mm 4.126 14.48◦ 4.128 17.5 mm 4.130 (a) 59.0 lb; (b) 39.2 lb 4.132 PAB = 0.6P (T), PAC = 0.8P (C),

4.8 3 unknowns 4.10 4 unknowns 4.12 θ = 33.7◦, NA = 0.555W, NB = 0.832W 4.14 53.6 lb 4.16 38.4 lb·in. 4.18 RB = 2940 N, Cx = 1766 N, Cy = −883 N 4.20 39.0◦ 4.22 T = 112.2 N, Ax = −38.4 N, Ay = 182.4 N 4.24 T1 = 133.3 lb, T2 = 100.0 lb, T3 = 166.7 lb 4.26 NB = 8.66 lb, Ax = 8.66 lb, Ay = 30.0 lb 4.28 NB = 660 lb, Ax = 0, Ay = 480 lb 4.30 5.36P

4.344.32 TRABA ==0,34R.6Blb,= T1BC.0 kN= 727  lb 4.36 533 N 4.38 P = 340 N, C = 101.9 N·m 4.40 RA = RB = 960 N 4.42 6.43 N 4.44 P = 5W/8 (θ does not appear in the

###### PBC = 0.64P (T), PCD = 0.48P (C)

4.134 PAE = 2820 lb (C), PAB = 2200 lb (T), PBC = 1200 lb (T), PBE = 2240 lb (T), PCE = 1342 lb (T), PCD = 1800 lb (T), PDE = 2310 lb (C)

expression for P) 4.46 (a) RA = 647 N, NB = 858 N; (b) 2.61 m 4.48 T = 13.66 N, RA = 27.4 N 4.50 NA = 434 N, C = 985 N 4.52 TA = 25.2 lb, TB = 324 lb, TC = 356 lb 4.54 1.975 ft 4.56 1627 N 4.58 238 N 4.60 50.4 mm 4.62 (a) 6 unknowns, 6 independent eqs.;

4.136 PAB = 358 kN (T), PAD = PDE = 320 kN (C), PBD = 160 kN (T), PBC = 537 kN (T), PBE = 178.9 kN (C), PCE = 240 kN (C)

4.138 PAB = 11.87 kN (C), PAD = 8.39 kN (T), PBC = 6.21 kN (C), PCD = 4.0 kN (T), PBD = 5.66 kN (C), PDE = 4.39 kN (C), PCE = 8.78 kN (C)

- (b) 8 unknowns, 8 independent eqs.;
- (c) 8 unknowns, 8 independent eqs.

4.140 PAB = 979 kN (T), PBC = 861 kN (T), PBD = 171 kN (T), PCD = 950 kN (C)

4.64 6 unknowns, 6 independent eqs.

- 4.142 1.506 ft

5.32 PEF = 1000 lb (C), C = 318 lb 5.34 286 lb 5.36 TCD = 193.5 N, A = 15.7i + 86.5j + 83.9k N,

###### 4.144 PHC = 0.901P (T), PHG = 0.901P (C)

- 4.146 3200 lb (T)

- B = 157.3i + 6.14k N 5.38 a = 3.43 m, b = 1.93 m 5.40 P = 51.4 lb, A = 87.0k lb, B = 134.4k lb 5.42 T = 104.4 lb, A = 39.3 lb 5.44 PBD = 1.786P, PBE = 1.515P 5.46 21.9 lb 5.48 PBE = 800 N (T), PCF = 640 N (C) 5.50 PCB = 171.6 lb (C), PCD = 671 lb (T) 5.52 4600 lb 5.54 T = 25.3 lb, NB = 32.8 lb 5.56 T = 161.3 lb, A = 12.0 lb, B = 12.0 lb,
- C = 140.5 lb 5.58 8600 N 5.60 T = 4750 N, A = 2000j N 5.62 T = 74.7 lb, B = 94.2 lb

###### 4.148 1.25P (T)

- 4.150 PBC = 13420 lb (C), PBG = 4470 lb (C), PFG = 16000 lb (T)

- 4.152 PEF = 240 kN (C), PNF = 82.0 kN (T), PNO = 187.5 kN (T)

4.154 PBG = 0.250P (T), PCI = 0.354P (T),

PCD = 0.750P (C) 4.156 (PBC)max = 168.0 kN, θ = 45◦ 4.158 PCD = 12.75 kN (T), PDF = 7.39 kN (C) 4.160 P = 5170 lb, Q = 370 lb 4.162 PDE = 40 kips (T), PAD = 0, PAC = 50 kips (C) 4.164 PCD = 4.0P (T), PIJ = 4.0P (C),

PNJ = 0.559P (C)

- 4.166 PBC = 4.47P (C), PBG = 2.0P (C)

- 4.168 PEF = 1.828W (T), PKL = 2.83W (C)

- 4.170 Wb/√R2 − b2

- 4.172 0.366WL

- 4.174 4.39 kN

- 4.176 A = D = 4.22 kN

- 4.178 15.12◦

- 4.180 (a) 361 kN (C); (b) 300 kN (T); (c) 631 kN (T)

- 4.182 20 lb

- 4.184 (a) 375 lb (T); (b) 4875 lb (T)

- 4.186 178 lb 4.188 643 N

Chapter 5

5.2 5 unknowns 5.4 6 unknowns 5.6 6 unknowns 5.8 6 unknowns

- 5.10 12 unknowns

- 5.12 6 unknowns

- 5.14 12 770 lb

- 5.16 27.3 kN

- 5.18 TA = TB = 145.8 N, TC = 134.9 N, TD = 61.3 N

- 5.20 T = 473 lb, A = 249 lb

- 5.22 TBC = 5.82 kN, TBD = 14.95 kN, RA = 18.66 kN

- 5.24 14.04◦

- 5.26 PCB = 9690 lb (T), PCE = 8050 lb (T)

- 5.28 PAD = 29.2 kN (C), PCD = 0, PBD = 65.0 kN (T)

- 5.30 C= 400k N, D = −400k N

###### Chapter 6

6.2 P1 = 0, V1 = 40 kN, M1 = 60 kN·m 6.4 P1 = 240 lb (C), V1 = 0, M1 = 600 lb·ft, P2 = 0, V2 = 60 lb, M2 = 300 lb·ft

6.6 P1 = V1 = 0, M1 = 720 lb ·ft, P2 = 0, V2 = 72 lb, M2 = 360 lb·ft 6.8 P1 = 28 lb (T), V1 = 0, M1 = 21 lb·in.,

P2 = 34.6 lb (T), V2 = 8 lb, M2 = 10 lb·in. 6.10 P1 = 644 N (C), V1 = 0, M1 = 162 N·m,

P2 = 644 N (C), V2 = 540 N, M2 = 324 N·m 6.12 M2 = 135.0 N·m, P2 = 969 N, V2 = 300 N 6.14 P3 = 255 N (C), V3 = 0, M3 = 29.8 N·m 6.16 P1 = 50 lb (T), V1 = 0, M1 = 600 lb·in.,

P2 = 50 lb (C), V2 = 37.5 lb, M2 = 150 lb·in. 6.18 P2 = Wx/(

√5a) (T), V2 = Wx/(2√5a),

M2 = 3Wx/4 6.20 P1 = 555 lb (C), V1 = 832 lb, M1 = 4000 lb·ft 6.22 V = C0/L, M = −C0 + C0x/L 6.24 V = −w0x + w0x2/(2L),

M = −w0x2/2 + w0x3/(6L) 6.26 AB: V = Pb/(a − b), M = Pbx/(a + b); BC:

V = −Pa/(a + b), M = Pa [1 − x/(a + b)] 6.28 AB: V = −120x lb, M = −60x2 lb·ft; BC:

V = −960 lb, M = −960x + 3840 lb·ft

6.30 AB: V = −120x lb, M = −60x2 lb·ft; BC: V = 810 − 120x lb, M = −60x2 + 810x − 2430 lb·ft

6.32 AB: V = 29 − 8x kN, M = 29x − 4x2 kN·m; BC: V = −11 kN, M = 88 − 11x kN·m

Chapter 8 573

6.34 AB: V = P/3, M = Px/3; BC: V = −2P/3, M = P(L − 2x)/3; CD: V = P/3, M = −P(L − x)/3

7.22 Disk is in equilibrium 7.24 (a) Plank will slide at A;

(b) Plank will not move 7.26 1.688 m 7.28 3.75 ft 7.30 176.6 N 7.32 115.3 N 7.34 4.50 lb·in. 7.36 47.1◦ 7.38 Blocks tip 7.40 353 lb 7.42 10.83 kN 7.44 0.268 7.46 13.14 ft 7.48 8.33 in. 7.50 18.15◦ 7.52 27.0◦ 7.54 (a) 114.5 lb·ft; (b) 60.2 lb·ft 7.56 (a) 1086 N; (b) 0.711 N·m 7.58 (a) 125.3 lb·in.; (b) 0 7.60 P = 76.2 lb, C = 15 960 lb·in. 7.62 64.1 N 7.64 11.69 lb < P < 77.0 lb 7.66 40.3◦ 7.68 0.201 7.70 (8/15)µsPR 7.72 (a) 6.01 N·m; (b) 5.89 N·m 7.74 4.73 N·m 7.76 17.25 in. 7.78 55.5 lb 7.80 4.80 lb 7.82 1.461W 7.84 β = 71.6◦, P = 316 lb 7.86 22.6◦ 7.88 2.0 m 7.90 (a) 11.73 lb·in.; (b) 7.24 lb·in. 7.92 0.325

6.36 AB: V = 12 kips, M = 12x kip·ft; BC: V = 0, M = 48 kip·ft; CD: V = M = 0

6.38 AB: V = 670 − 60x lb, M = 670x − 30x2 lb·ft; BC: V = −230 − 60x lb, M = −30x2 − 230x + 3600 lb·ft; CD: V = 1480 − 60x lb, M = −30x2 + 1480x − 16 920 lb·ft

6.40 AB: V = (P/2) sinθ, M = (PR/2)(1 − cosθ); BC: V = −(P/2)sinθ, M = (PR/2)(1 + cosθ)

6.42 (1) For 0 < x < L/2: V = P/2, M = Px/2; for L/2 < x < L: V = −P/2, M = P(L − x)/2;

(2) For 0 < x < L/2: V = −Px/L, M = Px/2; for L/2 < x < L: V = P(L − x)/L, M = P(L − x)/2

- 6.44-6.62 (No answers) 6.64 1.043 GN 6.66 s = 86.0 ft, T = 960 lb 6.68 s = 62.0 ft, H = 16.01 ft 6.70 (a) 440 N; (b) 33.7 m 6.72 0.338 6.74 36.4 kg 6.76 35.9 ft 6.78 26.7 ft 6.80 h = 8.13 ft, TBC = 72.1 lb, TCD = 100 lb 6.82 β2 = 27.8◦, β3 = −3.53◦, TAB = 5.04 kips,

TBC = 4.36 kips, TCD = 3.87 kips 6.84 13.03 ft 6.86 P = 48.0 kN, TAB = 26.8 kN, TBC = 12.0 kN,

TCD = 16.97 kN 6.88 0.420 6.90 1.50 kN

Chapter 7

- 7.2 29.3 lb ≤ P ≤ 109.3 lb

- 7.4 10.57◦

- 7.6 36.9◦

- 7.8 297 lb

- 7.10 (a) 5.89◦; (b) 7.10◦

- 7.94 Bars are in equilibrium

Chapter 8

- 8.2 x¯ = 2.86 ft, y¯ = 0.625 ft 8.4 x¯ = 0.1543 m, y¯ = 0.281 m 8.6 x¯ = 2.94 in., y¯ = 2.03 in. 8.8 x¯ = 6.33 in., y¯ = 3.67 in.

- 7.12 6.74 N

- 7.14 (a) NA = 94.2 N, NB = 141.2 N, NC = 377 N; (b) 0.50

3R2 + 3Rt + t2 2R + t

4 3π

8.10 (a) x¯ = y¯ =

8.12 x¯ = y¯ = 2R/π 8.14 x¯ = 2.47 in., y¯ = 0 8.16 x¯ = 0, y¯ = 0.557 in.

- 7.16 Cylinder cannot be at rest

- 7.18 0.270

- 7.20 153.2 N

###### 8.112 (a) πa2p0; (b) πa2p0; (c) 2.22a2p0;

- 8.18 x¯ = 20.2 mm, y¯ = 9.81 mm

√4h2 + π2a2

- 8.20 x¯ = 0.872 in., y¯ = 5.96 in.

(d) (ap0/2)

√5R/2

- 8.114 1.111p0d2

- 8.116 (a) γc(h2 + b2)/6; (b) γc(h2/6 + 4b2/15); (c) γc(h2/6 + b2/2)

- 8.118 Safe against tipping

- 8.120 R = 0.622 N, y¯ = 0, z¯ = 28.8 mm

- 8.122 19 970 lb

- 8.124 A = 3.22 × 106 N, NB = 3.79 × 106 N

- 8.126 x¯ = 8.84 in., y¯ = 0, z¯ = 21.45 in.

- 8.128 52.1 × 103 mm2

- 8.130 TA = TC = 16.94 lb, TB = 13.68 lb

- 8.132 x¯ = (11/28)b, y¯ = (93/280)h

- 8.134 44.3 in.

- 8.136 (a) 276 in.2; (b) 276 in.2

- 8.138 x¯ = 0, y¯ = −0.50 in.

- 8.140 R = 140.4 lb, y¯ = 0, z¯ = −0.884 ft

- 8.142 x¯ = 0, y¯ = 47.0 mm

Chapter 9

- 9.2 A = 360 mm2, I¯x = 24 × 103 mm4, I¯y = 26 × 103 mm4

9.4 826 mm 9.6 21.3 in.4 9.8 R4α/2

- 9.10 Ix = 1/28 m4, Iy = 1/20 m4

- 9.12 23.15 × 103 in.4

- 9.14 b = 7.35 in., h = 12.87 in.

- 9.16 I¯x = 157.8 in.4, I¯y = 9.94 in.4

- 9.18 Ix = 48.7 × 106 mm4, Iy = 18.42 × 106 mm4

- 9.20 12.96 × 106 mm4

- 9.22 6230 in.4

- 9.24 16.89 in.4

- 9.26 0.433R

- 9.28 1.0

- 9.30 32.7◦

- 9.32 Ix = 63.0 × 106 mm4, Iy = 7.90 × 106 mm4

- 9.34 h2b2/12

- 9.36 t R3/2

- 8.22 h =

b2 + bt − t2 2(2b − t)

- 8.24 x¯ = y¯ =

- 8.26 h = y¯max = 2.34 ft

- 8.28 x¯ = −3.6 mm, y¯ = 50.9 mm

- 8.30 x¯ = 1.0 ft, y¯ = 1.5 ft

- 8.32 x¯ = 0, y¯ = −10.30 mm

- 8.34 √3

- 8.36 x¯ = 3.28 in., y¯ = 3.59 in. 8.38 119.7 ft 8.40 x¯ = y¯ = 0, z¯ = R/2 8.42 x¯ = z¯ = 0, y¯ = 3.125 in. 8.44 x¯ = z¯ = 0, y¯ = h/3 8.46 R/π

- 2(2h1 + h2)

- 3(3h1 + h2)

2(2h1 + h2) 3(3h1 + h2)

8.48 x¯ =

a, y¯ =

b

8.50 x¯ = −(2/π)2R, y¯ = 2R/π, z¯ = h/3 8.52 x¯ = 9.95 in., y¯ = 4.0 in., z¯ = 1.75 in. 8.54 x¯ = 46.7 mm, y¯ = 40.0 mm, z¯ = 28.9 mm 8.56 x¯ = 124.1 mm, y¯ = 55.0 mm, z¯ = 41.1 mm 8.58 −29.4 mm 8.60 x¯ = −5.15 in., y¯ = z¯ = 0 8.62 x¯ = 77.8 mm, y¯ = 161.1 mm, z¯ = 100.0 mm 8.64 x¯ = y¯ = 7.70 in., z¯ = 2.70 in. 8.66 166.7 mm

- 8.68 x¯ = 0, y¯ = 1.74 in., z¯ = 3.21 in.

- 8.70 x¯ = 108.7 mm, y¯ = z¯ = 0

- 8.72 x¯ = 12 in., y¯ = 3.83 in., z¯ = 0

- 8.74 x¯ = z¯ = 0, y¯ = 1.640 m

- 8.76 V = 1257 in.3, A = 766 in.2

- 8.78 A = 258 in.2, V = 366 in.3

- 8.80 50.3 in.2

- 8.82 1487 in.3

- 8.84 12.73 ft

- 8.86 7850 m3

- 8.88 1.702

- 8.90 x¯ = y¯ = 0, z¯ = 0.788 m

- 8.92 x¯ = 2.5 in., y¯ = 4.14 in., z¯ = 0.858 in.

- 8.94 3.39 in.

###### 9.38 −120 × 103 mm4 9.40 −1.131 × 106 mm4 9.42 −61.4 × 106 mm4 9.44 −323 × 103 mm4 9.46 792 in.4 9.48 −2.76 × 109 mm4 9.50 (a) I1 = 16 in.4, I2 = 9 in.4, x- and y-axes are

- 8.96 x¯ = 2.16 in., y¯ = 4.56 in., z¯ = 0.71 in.

- 8.98 x¯ = 0, y¯ = −3.12 mm, z¯ = 5.21 mm

- 8.100 3.10 ft

- 8.102 27.7◦

- 8.104 R = 609 lb, x¯ = 8.16 ft

- 8.106 R = 2w0a, x¯ = 0, y¯ = πa/4

- 8.108 R = 0, CR = 9000 lb ·in. CCW

principal axes; (b) Iu = 14.25 in.4, Iv = 10.75 in.4, Iuv = 3.03 in.4

- 8.110 R = 149.1 N, x¯ = 0.0483 m,

y¯ = 0.0644 m

###### Chapter 10 575

- 9.52 I¯1 = 103.7 in.4, I¯2 = 29.6 in.4, θ1 = 29.9◦, θ2 = 119.9◦

###### Chapter 10

10.2 (WLsinθ)/2 10.4 3.53 kN·m 10.6 17.32 lb

- 9.54 Iu = 1817 in.4, Iv = 3180 in.4, Iuv = −183.0 in.4

- 9.56 Ix = 6800 in.4, Iy = 5800 in.4, Ixy = −1200 in.4

P(a + b) 2b

10.8

cotθ

- 9.58 60 × 106 mm4

10.10 332 lb 10.12 1.697 kN 10.14 624 lb·in. 10.16 24 N·m 10.18 2.07 kN·m 10.20 (No answer) 10.22 120tanθ lb 10.24 400 lb·ft 10.26 55.2 N 10.28 120 kN 10.30 240 N 10.32 15.37 kN 10.34 10.19 lb 10.36 Gripping force = 6.0P 10.38 (a) 27.5 in. directly below B; (b) 700 lb·in. 10.40 Unstable 10.42 θ = 32.5◦ is stable 10.44 h/R < 1/√2 10.46 θ = sin−1 W/(2kL), stable if Lk/W >

- 9.60 1.907 × 106 mm4

√3a4/96, Iuv = 0 for all θ. Therefore, every axis is a principal axis.

- 9.62 Iu = Iv =

- 9.64 (a) I1 = 0.983 × 106 mm4; (b) θ1 = 28.5◦, θ2 = 118.5◦

- 9.66 θ1 = −18.84◦

- 9.68 I1 = 143.6 × 106 mm4, I2 = 19.8 × 106 mm4, θ1 = 41.4◦, θ2 = 131.4◦

- 9.70 Iu = 33.3 × 106 mm4, Iv = 71.0 × 106 mm4, Iuv = 22.5 × 106 mm4

- 9.72 Iu = 115.2 in.4, Iv = 777 in.4, Iuv = 259 in.4

- 9.74 Iu = 2 × 106 mm4, Iv = 28 × 106 mm4, Iuv = 0

- 9.76 (a) 45◦; (b) Iu = Iv = 5 × 106 mm4, |Iuv| = 3 × 106 mm4

- 9.78 (a) 0.983 × 106 mm4; (b) θ1 = 28.5◦, θ2 = 118.5◦

- 9.80 (a) Ix = 56.2 × 106 mm4, Iy = 33.8 ×106 mm4; (b) Iu = 33.2 × 106 mm4, Iv = 56.8 × 106 mm4

- 9.82 I¯x = 4.084 × 106 mm4, I¯y = 0.816 × 106 mm4

√3/2

10.48 √WL/k/2 10.50 θ = 90◦ is stable, θ = 2.87◦ is unstable 10.52 Stable 10.54 θ = 45◦ is unstable 10.56 2.06 kg, unstable 10.58 79.1◦, stable 10.60 θ = 29.6◦ is unstable, θ = 53.1◦ is stable 10.62 6.15◦

- 9.84 I1 = 380 × 106 mm4, I2 = 120 × 106 mm4, θ1 = 56.3◦, θ2 = 146.3◦

- 9.86 3.21%

- 9.88 I¯x = 645 in.4, I¯y = 1438 in.4, I¯xy = −442 in.4

- 9.90 I¯x = 1.544 × 106 mm4, I¯y = 0.287 × 106 mm4, I¯xy = 0

- 9.92 Ix = Iy = 21.9 in.4, Ixy = 21.3 in.4

- 9.94 Iu = 90.5 in.4, Iv = 313.5 in.4, Iuv = −69.7 in.4

### Index

- A Absolute system of units, 5 Acceleration, Newton’s second law for, 5 Active-force diagram, 530 Addition:

of couples, 76 of vectors:

parallelogram law for addition, 12–13 polygon rule for addition, 12

Angle, between vectors, 27–28 Angle of friction:

angle of kinetic friction, 369–371 angle of static friction, 369–371 cone of kinetic friction, 369–371 cone of static friction, 369–371

Applied forces, 144 Area method:

concentrated forces and couples, 307 distributed loading, 303–304 equations for, 307 theorems for, 304–305

Areas, plane (See Plane areas) Axial forces:

deﬁnition of, 215 in disk friction, 386

Axis, centroidal, 283 Axis of the wrench, 119

- B Ball and socket joint, 239–240 Beams:

bending moment equations and diagrams for, 293 deﬁnition of, 291 differential equilibrium equations for, 304–305 internal forces systems in: analysis of, 282–285 determination of, 282 loads and supports for, 291 shear force equations and diagrams for, 293 sign convention for analysis of internal forces in,

292–293

Bending moment: area method diagram and, 303 deﬁnition of, 283 diagrams (M-diagrams) for, 303 equations (M-equations) for, 303 Built-in (cantilever) support, 241, 242

###### C

Cables: catenary, 321–322 under concentrated loads:

horizontal spacing given, 331–332 segment length given, 332 sign conventions for, 331

under distributed loads, 318-322 ﬂexible:

deﬁnition of, 318 equations for, 319–322 guidelines for problem solution, 322 parabolic, 319 (See also Flexible cable)

area method for: concentrated forces, 307 couples, 307 distributed loads, 303–304 equations for, 304

Catenary cable, 321–322 Center of gravity:

as centroid of volume for homogeneous body, 145, 443 for composite bodies, 444

###### 576

contrasted with center of mass, 442–443 deﬁnition of, 442 weight and, 443 (See also Center of mass)

Concentrated force: in beams, 307 in cables, 330 contrasted with distributed normal

Center of mass: of composite bodies, 444 contrasted with center of gravity, 442–443 deﬁnition of, 443–444

loads, 128

deﬁnition of, 38 Concentrated loads (See Concentrated force) Concurrent force systems:

Center of weight (See Center of gravity) Centroidal axis, 283 Centroids:

coplanar, 107, 154 reduction of, 39–40 resultant forces of, 40 three-dimensional, 117, 250 Cone of kinetic friction, 369–371 Cone of static friction, 369–371 Conservative systems, 548 Constraints:

center of gravity and, 442–445 center of mass and, 442–445 of common geometric shapes, 132 of composite shapes:

method of composite areas, 405 method of composite curves, 405

improper, 252 kinematic, 529

coordinates for three-dimensional shapes and, 419–422 of curved surfaces, volumes, and space curves: ﬁrst moment of the area for three-dimensional

Conversion factors, units, 6 Coordinate systems:

kinematically independent coordinates, 529 left-handed, 30 local, 293 rectangular reference frame

shapes, 419–422 method of composite shapes for, 421 symmetry and, 420

of plane areas and plane curves: centroid of the area, 401 centroid of the curve, 403–406 ﬁrst moments of the area, 402 ﬁrst moments of the curve, 403 integration techniques for, 403–404 moment of inertia, 402

and, 18–19 right-handed, 30 (See also Reference frames)

Coplanar equilibrium analysis: composite body: analysis, 179–184

of surface loads, 130 table of plane ﬁgures, 406

equations for: concurrent force systems, 154 general coplanar force systems, 153 parallel coplanar force systems, 154

Coefﬁcient of kinetic friction, 343 Coefﬁcient of static friction, 342 Components:

free-body diagram for, 144–147 plane trusses:

deﬁnition of, 18 orthogonal, 28 rectangular, 18–21 scalar, 19 vector, 19

assumptions for, 214 method of joints, 215–218 method of pins, 217 method of sections, 224–226

Composite areas, 405, 421, 476, 493 Composite bodies:

single-body:

analysis, 144–155 support reactions in, 144–147 three-force bodies, 202–203 two-force bodies, 201–202

center of gravity of, 444 center of mass of, 444 coplanar equilibrium analysis of, 179–184

Composite curves, 405, 421 Composite shapes, 405, 421 Composite volumes, 421 Compression, 214

Coplanar force systems: concurrent, 107, 154 general, 106–107, 153 parallel, 108, 154

###### D

Coplanar loads: bending moment, 283, 291–292 normal force, 283, 291–292 shear force, 283, 291–292 torque, 283

Densities table, 567 Diagrams:

active-force diagram, 530 bending moment (M-diagrams), 293 load diagram:

Coplanar support reactions: built-in support, 147 ﬂexible cable, 145 frictionless surface, 145 pin support, 147 roller support, 145 surface with friction, 145

area method and, 303 line loads along plane curves, 452–453 line loads along straight lines, 130–131

shear force (V-diagrams), 293 Differential equilibrium equations, 304 Dimensions, in Newtonian mechanics, 4–5 Direction cosines:

Coulomb’s theory of dry friction: dynamic case, 343 impending sliding case, 343 impending tipping case, 361–362 limitations of, 344 static case, 342 (See also Dry friction)

deﬁnition of, 18–19 writing vectors in rectangular form, 21

Disk friction: axial force in, 386 new surfaces, 387 torque requirements in, 386 worn surfaces, 387–388

Couple of transfer, 87 Couple-vector, 76 Couples:

Distributed loads: beams, 303–306 ﬂexible cables, 318–322

addition of, 76 in beams:

Distributed normal loads: computation of, 131–132 contrasted with concentrated forces, 128 for ﬂuid pressure, 454–455 general case of, 450–451 line loads along plane curves:

area method and, 307 bending moment in, 283 torque in, 283

couple-vector, 76 deﬁnition of, 73 equivalent, 75 line of action, changing:

load diagram for, 452–453 load intensity for, 452–453

line loads along straight lines: load diagram for, 130–131 load intensity for, 130 pressure as example of, 128 resultants of, 128–132 surface loads:

couple of transfer, 87 force-couple system, 87

moment of a couple about a point, 73–74 moment of a couple as a free vector, 74 notation and terminology for, 75–76 plane of a couple, 73 resolution of, 76 scalar method for, 73 vector method for, 74 virtual work of, 526

centroid of the volume and, 130 on ﬂat surfaces, 451–452 load area of, 129 load intensity of, 129 uniform pressure on curved surfaces, 453–454

Cross (vector) product, 29–31 Curved surfaces:

Dot (scalar) product: deﬁnition of, 27 ﬁnding angle between two vectors, 28 orthogonal components and, 28

centroids of, 419–437 uniform pressure and, 453–454

Curves, plane (See Plane curves) Curves, space (See Space curves) Cylindrical roller on friction surface or on guide

Dry friction: angle of kinetic friction, 369–371 angle of static friction, 369–371 coefﬁcient of kinetic friction, 343

rail, 238–240

coefﬁcient of static friction, 342 cone of kinetic friction, 371 cone of static friction, 370 Coulomb’s theory of, 342–345

for moment of a force about a point, 49–51 for moment of a force about an axis, 60–64 for reducing force system to force-couple system,

97–99 for resultant of concurrent force systems, 39–40 transformation equations for moments and products of

dynamic case, 343 impending sliding case, 343 impending tipping case, 361–362 limitations of, 344 static case, 342–343

inertia, 500 Equations of constraint, 529 Equilibrium analysis:

disk friction: axial force in, 386 new surfaces, 387 torque requirements in, 386 worn surfaces, 387–388

coplanar: composite bodies, 179–213 concurrent force systems, 154 free-body diagrams for, 144–147 general coplanar force systems, 153 independent equilibrium equations for, 153–155 parallel coplanar force systems, 154 plane trusses, 214–226 single-body problems, 166 support reactions in, 144–147 three-force bodies, 202 two-force bodies, 201

for ﬂat belts, 379–381 method of analysis by problem type, 345, 362 for ropes, 379–381 for square-threaded screws, 372–373 for wedges, 371

Dynamic friction force, 343 (See also Kinetic friction)

deﬁnition of equilibrium, 144, 238 equations of equilibrium, 144, 238 free-body diagram:

- E Elastic potential energy, 549 Engineering, deﬁned, 1–2 Engineering mechanics:

applied forces on, 144 deﬁnition of, 144 determining support reactions, 144–145 procedure for constructing, 145 reactive forces on, 144

deﬁnition of, 1–2 problem analysis in, 2–3

Equal and opposite pin reactions, 183, 184 Equality of vectors, 12 Equations:

three-dimensional: free-body diagrams for, 238–242 improper constraints in, 252 independent equilibrium equations for, 249–252 method for, 263 steps in analysis, 253 support reactions in, 238–242

for area method, 304–307 for bending moment (M-equations), 293 for composite volumes, 421 equilibrium:

coplanar, 144 differential equilibrium equations for beams, 304 three-dimensional, 237

trusses, equilibrium of pins, 217 trusses, method of joints, 215–218 trusses, method of sections, 224–226 writing and solving equations:

for ﬂexible cable, 318–320 independent equilibrium equations: all forces intersect an axis, 252 concurrent force systems, 154 concurrent, three-dimensional force system, 250 general, coplanar force systems, 153 general, three-dimensional force system,

method of analysis, 155 statically determinate force systems, 155 statically indeterminate force systems, 155

Equilibrium and stability of conservative systems: deﬁnition of conservative systems, 548 elastic potential energy, 549 gravitational potential energy, 549 potential energy, 548 stationary potential energy and stability, 549–550

249–250 parallel, coplanar force systems, 154 parallel, three-dimensional force system,

251–252 for moment of a couple about a point, 73

Equilibrium, deﬁned, 144, 238

Equilibrium equations: coplanar, 144 differential equilibrium equations for beams, 306 three-dimensional, 238

Force systems: all forces intersect an axis, 252 concurrent force systems:

reduction of, 39–40 resultant forces of, 40

Equivalence: of couples, 75 deﬁnition of, 38 of force systems: general, 39 statically equivalent force systems, 106

coplanar: concurrent, 107, 154 general, 106, 153 parallel, 108, 154 resultants in, 106–108

of vectors: ﬁxed vectors, 38 free vectors, 38 sliding vectors, 38

equivalence of, 39 force-couple system, 86–87 statically determinate, 155 statically equivalent, 106 statically indeterminate, 155 three-dimensional:

Expansion by minors using the ﬁrst row, 31 External effects:

in beams, 282 of a force, 38–39 resultant of a force system and, 105

concurrent, 117, 250–251 general, 118, 249–250 parallel, 117–118, 251–252 resultants in, 116–119 wrench, 116, 118–119

- F First moments of an area:

(See also Force)

Force: applied, 144 concentrated, 38 deﬁnition of, 38 distributed normal loads (See Distributed normal loads) as external effects, 38 as ﬁxed vectors, 38 friction, 341 generalized, 548 line of action of:

Pappus-Guldinus theorems and, 438–439 for plane ﬁgures, 401–406 for three-dimensional shapes, 419–422

First moments of a curve: Pappus-Guldinus theorems and, 438–439 for plane curves, 401–406

Fixed vector: deﬁnition of, 38 force as, 38–39

Flat belts, dry friction analysis, 379–381 Flat surfaces, distributed normal loads, 451 Flexible cable:

changing, 86–87 deﬁnition of, 38

moment of a force about a point, 49–51 deﬁnition of, 49 geometric interpretation of, 49–50 moment arm, 49 moment center, 49 Newton’s second law and, 49 principle of moments (Varignon’s theorem) for, 51 scalar method for, 51 vector method for, 51

catenary, 321–322 coplanar support reactions, 144–146 deﬁnition of ﬂexible, 318 equations for, 319–322 guidelines for problem solution, 322 parabolic, 319 three-dimensional support reactions and, 238, 240

Fluid friction, 342, 344 Fluid pressure, distributed normal loads, 454–455 Force-couple system:

moment of a force about an axis: deﬁnition of, 60–61 geometric interpretation of, 62–64 scalar method for, 64 vector method for, 64

changing line of action of a force, 86–87 reduction to, 97–99 scalar equations for determining, 99 vector equations for determining, 98 wrench, 116, 118–119

Newton’s second law, 5 point of application of, 38

reactive (reactions): compared with applied forces, 144 internal reactions at connections, 180–184 internal reactions in members, 179–180

Friction: angle of, 369–373 Coulomb, 342 disk, 386 dry (See Dry friction) ﬂuid, 342, 344 friction surfaces (single point of contact), 145–146,

resultants: coplanar systems, 106–108 deﬁnition of, 105 distributed normal loads, 128–132 reduction to a force and a couple, 97–99 three-dimensional systems, 116–119

239–240 frictionless surfaces, 145–146, 341 kinetic or dynamic, 343 static, 342–343

as sliding vectors, 39 virtual work of, 525–526 working component of, 526 (See also Force systems)

Friction force: analysis of, 345–346 deﬁnition of, 341–342 (See also Dry friction)

Frames, 143, 179 Frames, reference:

Friction surface (single point of contact), 145–146, 239–240 Frictionless surface (single point of contact), 145–146, 342

inertial, 4 rectangular, 20 Free-body diagram: applied forces, 144 coplanar support reactions:

###### G

Galilean reference frames, 4 General force systems:

built-in (cantilever) support, 147 ﬂexible cable (negligible weight), 145 frictionless surface (single point of contact), 145 pin support, 147 roller support, 145 surface with friction (single point of contact), 145

coplanar, 106, 153–154 three-dimensional, 118–119, 249–253

General virtual plane motion, 525 Generalized forces, 548 Geometric center of the region (See Centroids) Geometric interpretation:

deﬁnition of, 144 internal reactions:

of moment of a force about a point, 49–50 of moment of a force about an axis, 60–63

at connections, 180–184 in members, 179–180

Geometric tables: centroids of common shapes, 130 inertial properties of plane areas, 472–478 plane ﬁgures, 406 surfaces and volumes, 422

pin reactions, 180 procedure for constructing, 144, 242 reactive forces on, 144 three-dimensional support reactions:

ball and socket joint, 239–240 built-in (cantilever) support, 241–242 cylindrical roller on friction surface or on guide

Graphic addition, 12 Gravitational potential energy, 549 Gravitational system of measurement, 4 Gravity, weight and, 442 (See also Center of gravity)

rail, 238–240 ﬂexible cable (negligible weight), 238, 240 friction surface (single point of contact),

239–240 slider (radial) bearing or hinge, 241 spherical roller or single point of contact on

###### I

Impending sliding: in dry friction, 343 method of analysis by problem type, 345–346

frictionless surface, 238–239 thrust bearing or hinge, 241–242 universal joint, 241–242

Impending tipping: in dry friction, 361–362 method of analysis by problem type, 362

Free vectors: deﬁnition of, 37 moment of a couple as a free vector, 74

Improper constraints, 252

Independent equilibrium equations: all forces intersect an axis, 252 concurrent coplanar force systems, 154 concurrent, three-dimensional force system, 250 general coplanar force systems, 153–154 general, three-dimensional force system, 249–253 parallel coplanar force systems, 154 parallel, three-dimensional force system,

number of degrees of freedom (DOF), 529 planar kinematics of a rigid body, 523–526

Kinetic friction: angle of, 369–371 cone of, 369–371 in dry friction, 342

###### L

251–253 Inertia (See Moment of inertia of a plane area;

Law of universal gravitation, 6 Laws of particle motion, 3–4 Left-handed coordinate systems, 30 Line loads:

Product of inertia of a plane area) Inertial reference frames, 4 Instant center of rotation:

along plane curves: load diagram, 452–453 load intensity, 452

body extended in, 540 deﬁnition of, 539 Internal force systems: analysis in beams:

along straight lines:

load diagram, 130 load intensity, 130

bending moment equations and

diagrams, 293 loading and supports, 291 shear force equations and diagrams, 293

Line of action of a force:

changing: couple of transfer, 87 force-couple system, 87

bending moment, 283 normal force, 283 shear force, 283 torque, 283

deﬁnition of, 38

Load area, 129 Load diagram:

Internal forces (See Internal reactions) Internal reactions:

area method, 303 line loads along plane curves, 452–453 line loads along straight lines, 130

in beams, 282–284 at connections, 180–184 in members, 179–180 normal force, 283 shear forces, 283 in trusses:

Load intensity: deﬁnition of, 129, 130 distributed normal loads, 450–455 line loads along plane curves, 452–453 line loads along straight lines, 130 uniform pressure on curved surfaces, 453–454

method of joints, 215–218 method of sections, 224–226

Load surface, 128–129 Loads:

in two-force body: compression, 214 tension, 214

concentrated, on cables, 330–332 coplanar:

bending moment, 283, 292–293 normal force, 283, 292–293 shear force, 283, 292–293 torque, 283

###### J

Joints, in trusses, 216–217

distributed:

###### K

on beams, 303–307 on cables, 318–322

Kinematic constraints, 529 Kinematically independent coordinates, 529 Kinematics:

line, 130–131 surface, 128–130 transverse, 291 (See also Distributed normal loads)

equations of constraint, 529 kinematically independent coordinates, 529

###### M

Moment axis (See Moment of a force about an axis) Moment center, 49 Moment of a couple about a point, 73–74 Moment of a couple as a free vector, 74 Moment of a force about a point:

M-diagrams, 293

- M-equations, 293 Machines, 179 Mass center (See Center of mass) Mass, Newton’s second law and, 5 Measurement:

deﬁnition of, 49 geometric interpretation of, 49–50 moment arm and, 49 moment center and, 49 Newton’s second law and, 49 principle of moments (Varignon’s theorem) for, 51 scalar method for, 51 special case: moment axis perpendicular to

conversion factors for, 5–6 dimensions, 4 standards:

Système internationale d’unités (SI), 4 U.S. Customary system, 4

systems: absolute, 4 gravitational, 4

force, 62 vector method for, 51

units, 4 Mechanics: deﬁnition of, 1 Newtonian, 3 quantum, 3 relativistic, 3

Moment of a force about an axis: deﬁnition of, 61–62 geometric interpretation of, 62–64 rectangular components of, 61–62 scalar method for, 64 special case: moment axis perpendicular to force, 62 vector method for, 64

Method of composite areas: determining centroids with, 405 for moment of inertia of a plane area, 476 for product of inertia of a plane area, 493

Moment of couple (See Couples) Moment of inertia of a plane area:

about the centroidal axis, 473–474 deﬁnition of, 471–472 integration techniques for, 475–476 method of composite areas for, 476–478 Mohr’s circle for, 508–512 parallel-axis theorems for, 473–475 polar moment of inertia using, 473 principal moments of inertia:

Method of composite curves, 405 Method of composite shapes:

applied to curved surfaces, volumes, and space

curves, 421 center of gravity and, 444 centroids by, 405

Method of joints: equilibrium analysis of joints, 215–218 equilibrium analysis of pins, 217 support reactions, 215 zero-force members, 218 Method of sections, 224–226 Method of virtual work:

principal axes, 501 principal directions, 501

radius of gyration, 475 transformation equations for, 500–501

Moments: bending moment, 283 ﬁrst moments of an area:

active-force diagram for, 530 generalized forces in, 530 implementation of, 529–530

Pappus-Guldinus theorems and, 438 for plane ﬁgures, 402 for three-dimensional shapes, 419

Mohr’s circle: construction of, 509 properties of, 510 veriﬁcation of, 511–512

ﬁrst moments of a curve: Pappus-Guldinus theorems and, 439 for plane curves, 403

Moment about a point (See Moment of a force about a point) Moment about an axis (See Moment of a force about an axis) Moment arm, 49

moment of inertia of a plane area, 402,

471–472 polar moment of inertia, 472–473 twisting moment or torque, 283

- N Newton, Sir Isaac, 3 Newtonian mechanics:

conversion of units in, 6 inertial reference frames in, 4 law of universal gravitation, 6 laws of particle motion, 4 Newton’s second law, 5 scope of, 3–4 units and dimensions in, 4–5

Newtonian reference frames (See Inertial reference

frames) Newton’s method, for roots, 563–564 Newton’s second law: acceleration in, 5 force in, 5 mass in, 5 moment of force about a point and, 49–50 weight in, 5

Newton’s third law, 4, 169 Normal force, 283, 291, 341 Normal loads (See Distributed normal

loads) Number of degrees of freedom (DOF), 529 Numerical integration: deﬁnition of, 559 Simpson’s rule, 560–561 trapezoidal rule, 560 when to use, 559

- O Orthogonal components, 28
- P Pappus-Guldinus:

resolution and, 12 resultants of, 12 triangle law and, 12

Physics, deﬁned, 1 Pins:

equilibrium analysis in trusses, 216–218, 224–226 pin reactions:

equal and opposite, 183–184 not equal and opposite, 184

pin support, 146–147 Planar kinematics of a rigid body:

virtual displacements: deﬁnition of, 524 general virtual plane motion, 525 notation for, 524 virtual rotation about a ﬁxed point, 524 virtual translation, 524

Plane areas: centroid of an area, 402 ﬁrst moments of an area, 402 inertial properties of, 477–478 second moments of an area (moments of inertia), 402

Plane curves: centroid of a curve, 403 ﬁrst moments of a curve, 403 Pappus-Guldinus theorems and, 438

Plane ﬁgures, property tables of, 406 Plane motion (See Planar kinematics of a

rigid body) Plane of the couple, 73 Point of application of a force, 38 Polar moment of inertia:

moments of inertia and, 472–473 parallel-axis theorems for, 473–475

Polygon rule for addition, 12 Position vector, 20 Potential energy:

Theorem I, 438 Theorem II, 439

deﬁnition of, 548 elastic, 549 gravitational, 549 principle of minimum potential energy, 550 principle of stationary potential energy, 550

Parabolic cable, 319–320 Parallel-axis theorem:

for moments of inertia, 473–475 for polar moments of inertia, 473–475 for products of inertia, 493 transfer distance, 474

Pressure: distributed normal loads and, 128 ﬂuid, 454–455 uniform, 453–454

Parallel force system: coplanar, 108, 155 three-dimensional, 117, 251

Principal moments of inertia: principal axes, 501 principal directions, 501

Parallelogram law for addition: components of, 12

Principia (Mathematical Principles of Natural

Relativistic mechanics, 3 Resolution:

Philosophy), 3 Principle of minimum potential energy, 550 Principle of moments, 51 Principle of stationary potential energy, 550 Principle of transmissibility, 39 Principle of virtual work, 525–526 Product of area (See Product of inertia of a plane area) Product of inertia of a plane area:

of couples, 76 of forces, 12

Resultants of force systems: concurrent force systems, 39–40 coplanar systems:

concurrent, 107 general, 106 parallel, 108

deﬁnition of, 492 inertial properties tables for, 477–478 method of composite areas for, 492–493 Mohr’s circle and, 508–512 parallel-axis theorem for, 493 transformation equations for, 500–501

deﬁnition of, 12, 105–106 distributed normal loads line loads, 130–131 surface loads, 128–130

external effects and, 105 reduction to a force and a couple,

97–99

- Q Quadrature (See Numerical integration) Quantum mechanics, 3–4
- R Radius of gyration, 475 Reactive forces (reactions):

three-dimensional systems: concurrent, 117 general, 118–119 parallel, 117–118

Right-handed coordinate systems, 29 Rigid bodies:

equivalent couples and, 75 equivalent force systems and, 39 general plane motion for, 462–463 general virtual plane motion for, 525 instant center of rotation in, 539 resultant of a force system for, 105 virtual work for a system of, 528

coplanar supports, 145–147 internal reactions:

at connections, 180–184 in members, 179–180

pin reactions, 147, 180–184 support reactions in trusses, 215 three-dimensional supports, 238–242

Rigid-body equivalent, 39 Roller support, 145 Roots:

Rectangular components: of moment of a force about an axis,

deﬁnition of, 564 Newton’s method for ﬁnding, 564–565 secant method for ﬁnding, 565

61–62 representation of vectors with, 18–21 vector addition with, 20 writing vectors with, 21

Ropes, dry friction analysis, 379–381 Rotation:

Rectangular coordinate systems: left-handed, 30 right-handed, 30

about a ﬁxed point, 524 instant center of, 539–541 virtual, 524

Rectangular reference frame, 20 Reduction of concurrent force systems, 39–40 Reference frames:

###### S

inertial, 4 rectangular, 18–21 Relative position vector: deﬁnition of, 20 using to write a vector in rectangular

Scalar equations: for moment of a couple about a point, 73–74 for moment of a force about a point, 51 for moment of a force about an axis, 64 noncoplanar, 238

form, 20–21

Scalar equations: (continued) for reducing force system to force-couple system, 97–98 for resultant of concurrent force

beams, 291–293 deﬁnition of, 155

Statically equivalent force systems, 106 Statically indeterminate force systems:

systems, 39–40 Scalar method (See Scalar equations) Scalar triple product, 31 Scalar-vector multiplication, 12 Scalars:

beams, 291–293 deﬁnition of, 155

Stationary potential energy, 549–550 Stiffness, 549 Support reactions:

compared with vectors, 11, 12 as components, 18–21 dot (scalar) product and, 27 notation for, 10–12 scalar-vector multiplication, 12

in beams, 291–293 coplanar:

built-in (cantilever) support, 146–147 determining, 144–145 frictionless surface (single point of contact), 145–147 pin support, 147 roller support, 145 surface with friction (single point of contact),

Screws: lead angle of, 372–373 pitch of, 372–373 self-locking, 373 torque required by, 372–373

145–147 three-dimensional, 238–242 in trusses, 215

Secant method, 564–565 Second moment of the area (See Moment of inertia

Surface friction: frictionless surface (single point of contact), 145 new surfaces and, 387 surface with friction (single point of contact), 145–147 worn surfaces and, 387–388

of a plane area)

Shear force: deﬁnition of, 283 diagram (V-diagram) for, 293, 305 equations (V-equation) for, 293 as part of internal force system of coplanar

Surface loads: centroid of the volume, 130 load area, 129 load intensity, 129 load surface, 128–130

loads, 291 SI system (See Système internationale d’unités) Simpson’s rule, 405, 560 Single bodies, coplanar equilibrium analysis

Surfaces: ﬂat, 451–452 geometric tables for, 422

of, 144–158 Slider (radial) bearing or hinge, 241 Sliding (See Impending sliding) Sliding vector:

Système internationale d’unités (SI), 4–5

deﬁnition of, 38 treating force as, 39

###### T

Tension, 214 Theorems:

Slug, as mass unit, 5 Space curves, 419–437 Spherical roller or single point of contact on frictionless

area method diagrams and, 303–308 for bending moment, 303–308 for load, 303–308 Pappus-Guldinus theorems, 438–439 parallel-axis theorem, 473–475 for shear force, 303–305 theorem for virtual work performed on

surface, 238 Spring constant, 549 Standards of measurement:

Système internationale d’unités (SI), 4 U.S. Customary system, 4

Static friction:

a rigid body, 527 Varignon’s theorem, 51 Three-dimensional equilibrium analysis: free-body diagram of, 238–242

angle of, 369–371 coefﬁcient of, 342 cone of, 369–371

Statically determinate force systems:

improper constraints in, 252 independent equilibrium equations of, 249–250 method for, 263 support reactions in, 238–242 writing and solving equations for, 253

equilibrium analysis of pins, 217 support reactions, 215 zero-force members, 218

method of sections, 224–226 Twisting moment (See Torque) Two-dimensional shapes, 401–406 Two-force body:

Three-dimensional shapes: centroids of, 419–422 coordinate systems for, 419 ﬁrst moments for, 419

compression, 214 equilibrium, 201 tension, 214

Three-dimensional support reactions: ball and socket joint, 239–240 built-in (cantilever) support, 241–242 cylindrical roller on friction surface or on guide

Two-force principle, 201

- U Uniform pressure, distributed normal loads, 453–454 Unit vectors, 12, 20–21 Units:

conversion: factor list for, 6 method for, 5–6

in Newtonian mechanics, 4 Universal joint, 241, 242

- U.S. Customary system, 4–5
- V

- V-diagrams, 293 V-equations, 293 Varignon’s theorem, 51 Vector equations:

rail, 239–240 ﬂexible cable (negligible weight), 238, 240 friction surface (single point of contact),

238, 240 slider (radial) bearing or hinge, 241 spherical roller or single point of contact on

frictionless surface, 238, 240 thrust bearing or hinge, 241 universal joint, 241–242

Three-dimensional systems: concurrent, 117, 250 general, 118–119, 249–250 parallel, 117–118, 251–252 wrench, 116, 118–119

Three-force principle, 202 Thrust bearing or hinge, 241 Tipping (See Impending tipping) Torque:

for moment of a couple about a point, 73 for moment of a force about a point, 51 for moment of a force about an axis, 64 for reducing force system to force-couple system, 97 three-dimensional, 238

deﬁnition of, 283 required by screws, 372 requirements in disk friction, 386

Transfer distance, 474 Transformation equations for moments

Vector method

(See Vector equations) Vector product, 29 Vectors:

and products of inertia: deﬁnition of, 500–501 properties of, 510 veriﬁcation of, 511

addition of: parallelogram law for addition, 12 polygon rule for addition, 12 triangle law, 12 using rectangular components, 18–20

Translation, rigid bodies, 524 Trapezoidal rule, 404, 560 Triangle law, 12–13 Truss:

compared with scalars, 11 as components, 12, 18 couple-vector, 76 as directed line segments, 11 equality of vectors, 12 equivalent:

assumptions for analysis,

214–215 description of, 214–215 members as two-force bodies, 214 method of joints:

equilibrium analysis of joints, 216

Vectors: (continued) ﬁxed vectors, 38 free vectors, 38 sliding vectors, 38

work-absorbing component, 526 working component, 526

kinematic constraints and independent coordinates

for, 529 method of, 528–530 principle of, 528–529 for a system of rigid bodies, 528 theorem for virtual work performed on a rigid body,

multiplication of: cross (vector) product, 29–31 dot (scalar) product, 27–28 scalar triple product, 31 scalar-vector multiplication, 12

527–528

notation for, 11 position vector, 20–21 relative position vector, 20–21 representation:

Volumes: centroids of, 130, 419–422 composite, 421 geometric tables for, 422 Pappus-Guldinus theorems for, 438

with direction cosines, 18–19 by rectangular components, 18–19

resolution of, 12 resultant, 12 unit, 12, 18–20 writing a vector in rectangular form: using direction cosines, 18–19 using relative position vector, 20

###### W

Wedge angle, 371 Wedges, 371 Weight:

Newton’s second law and, 5 as resultant force of gravity, 442

Virtual displacements: deﬁnition of, 524 general virtual plane motion, 525 notation for, 524 virtual rotation about a ﬁxed point, 524 virtual translation, 524

Work-absorbing component of a force, 526 Working component of a force, 526 Wrench, 116, 118–119

Virtual work: of a couple, 526 of a force:

###### Z

Zero-force members, 218
