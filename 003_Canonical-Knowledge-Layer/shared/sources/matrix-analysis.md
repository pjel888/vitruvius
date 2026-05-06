---
id: source-matrix-analysis-for-scientists-and-engineers
title: Matrix Analysis
page_type: source
trust_level: unknown
canonical_status: draft
source_relative_markdown_path: 006 -Structural/refined_markdown/Matrix Analysis For Scientists and Engineers.md
last_canonicalized_utc: '2026-05-05T11:49:09.740611+00:00'
---

# Matrix Analysis

## Overview

Copyright © 2005 by the Society for Industrial and Applied Mathematics.

## Coverage

- Chapter 1. Introduction and Review
- Chapter 2. Vector Spaces
- Part 4 of Theorem 3.19 suggests looking at the general problem of the four fundamental subspaces of matrix products. The basic results are contained in the following easily proved theorem.
- 3. The singular vectors satisfy the relations
- 9. Let
- 3. For each independent x(2) from step 2, solve
- 7. Let
- 5. Let
- 1. Let
- 2. Recall the real JCF
- 10. Block Diagonalization: Let

## Key Points

- University of California Davis, California slam.

## Referenced Concepts

- concept-floor-area-ratio
- concept-approved-budget-for-the-contract

## Source Text

![image 1](<Matrix Analysis For Scientists and Engineers_images/imageFile1.png>)

![image 2](<Matrix Analysis For Scientists and Engineers_images/imageFile2.png>)

# Matrix Analysis

##### for Scientists & Engineers

###### This page intentionally left blank

![image 3](<Matrix Analysis For Scientists and Engineers_images/imageFile3.png>)

![image 4](<Matrix Analysis For Scientists and Engineers_images/imageFile4.png>)

## Matrix Analysis

#### for Scientists & Engineers

### Alan J. Laub

University of California Davis, California

slam.

![image 5](<Matrix Analysis For Scientists and Engineers_images/imageFile5.png>)

Copyright © 2005 by the Society for Industrial and Applied Mathematics.

1 0 9 8 7 6 5 4 3 2 1

All rights reserved. Printed in the United States of America. No part of this book may be reproduced, stored, or transmitted in any manner without the written permission of the publisher. For information, write to the Society for Industrial and Applied Mathematics, 3600 University City Science Center, Philadelphia, PA 19104-2688.

MATLAB® is a registered trademark of The MathWorks, Inc. For MATLAB product information, please contact The MathWorks, Inc., 3 Apple Hill Drive, Natick, MA 01760-2098 USA, 508-647-7000, Fax: 508-647-7101, info@mathworks.com, www.mathworks.com

Mathematica is a registered trademark of Wolfram Research, Inc.

Mathcad is a registered trademark of Mathsoft Engineering & Education, Inc.

###### Library of Congress Cataloging-in-Publication Data

Laub, Alan J., 1948Matrix analysis for scientists and engineers / Alan J. Laub.

p. cm.

Includes bibliographical references and index. ISBN 0-89871-576-8 (pbk.)

1. Matrices. 2. Mathematical analysis. I. Title.

QA188138 2005 512.9'434—dc22

2004059962

About the cover: The original artwork featured on the cover was created by freelance artist Aaron Tallon of Philadelphia, PA. Used by permission.

slam isaregisteredtrademark.

![image 6](<Matrix Analysis For Scientists and Engineers_images/imageFile6.png>)

###### To my wife, Beverley

(who captivated me in the UBC math library nearly forty years ago)

![image 7](<Matrix Analysis For Scientists and Engineers_images/imageFile7.png>)

###### This page intentionally left blank

![image 8](<Matrix Analysis For Scientists and Engineers_images/imageFile8.png>)

![image 9](<Matrix Analysis For Scientists and Engineers_images/imageFile9.png>)

###### Contents

Preface xi

- 1 Introduction and Review 1

- 1.1 Some Notation and Terminology 1
- 1.2 Matrix Arithmetic 3
- 1.3 Inner Products and Orthogonality 4
- 1.4 Determinants 4

- 2 Vector Spaces 7

- 2.1 Definitions and Examples 7
- 2.2 Subspaces 9
- 2.3 Linear Independence 10
- 2.4 Sums and Intersections of Subspaces 13

- 3 Linear Transformations 17

- 3.1 Definition and Examples 17
- 3.2 Matrix Representation of Linear Transformations 18
- 3.3 Composition of Transformations 19
- 3.4 Structure of Linear Transformations 20
- 3.5 Four Fundamental Subspaces 22

- 4 Introduction to the Moore-Penrose Pseudoinverse 29

- 4.1 Definitions and Characterizations 29
- 4.2 Examples 30
- 4.3 Properties and Applications 31

- 5 Introduction to the Singular Value Decomposition 35

- 5.1 The Fundamental Theorem 35
- 5.2 Some Basic Properties 38
- 5.3 Row and Column Compressions 40

- 6 Linear Equations 43

- 6.1 Vector Linear Equations 43
- 6.2 Matrix Linear Equations 44
- 6.3 A More General Matrix Linear Equation 47
- 6.4 Some Useful and Interesting Inverses 47

vii

![image 10](<Matrix Analysis For Scientists and Engineers_images/imageFile10.png>)

viii Contents

###### 7 Projections, Inner Product Spaces, and Norms 51

- 7.1 Projections 51 7.1.1 The four fundamental orthogonal projections 52
- 7.2 Inner Product Spaces 54
- 7.3 Vector Norms 57
- 7.4 Matrix Norms 59

###### 8 Linear Least Squares Problems 65

- 8.1 The Linear Least Squares Problem 65
- 8.2 Geometric Solution 67
- 8.3 Linear Regression and Other Linear Least Squares Problems 67

- 8.3.1 Example: Linear regression 67
- 8.3.2 Other least squares problems 69

- 8.4 Least Squares and Singular Value Decomposition 70
- 8.5 Least Squares and QR Factorization 71

###### 9 Eigenvalues and Eigenvectors 75

- 9.1 Fundamental Definitions and Properties 75
- 9.2 Jordan Canonical Form 82
- 9.3 Determination of the JCF 85

- 9.3.1 Theoretical computation 86
- 9.3.2 On the +1's in JCF blocks 88

- 9.4 Geometric Aspects of the JCF 89
- 9.5 The Matrix Sign Function 91

###### 10 Canonical Forms 95

- 10.1 Some Basic Canonical Forms 95
- 10.2 Definite Matrices 99
- 10.3 Equivalence Transformations and Congruence 102 10.3.1 Block matrices and definiteness 104
- 10.4 Rational Canonical Form 104

###### 11 Linear Differential and Difference Equations 109

- 11.1 Differential Equations 109

- 11.1.1 Properties of the matrix exponential 109
- 11.1.2 Homogeneous linear differential equations 112
- 11.1.3 Inhomogeneous linear differential equations 112
- 11.1.4 Linear matrix differential equations 113
- 11.1.5 Modal decompositions 114
- 11.1.6 Computation of the matrix exponential 114

- 11.2 Difference Equations 118

- 11.2.1 Homogeneous linear difference equations 118
- 11.2.2 Inhomogeneous linear difference equations 118
- 11.2.3 Computation of matrix powers 119

- 11.3 Higher-Order Equations 120

![image 11](<Matrix Analysis For Scientists and Engineers_images/imageFile11.png>)

Contents ix

###### 12 Generalized Eigenvalue Problems 125

- 12.1 The Generalized Eigenvalue/Eigenvector Problem 125
- 12.2 Canonical Forms 127
- 12.3 Application to the Computation of System Zeros 130
- 12.4 Symmetric Generalized Eigenvalue Problems 131
- 12.5 Simultaneous Diagonalization 133

- 12.5.1 Simultaneous diagonalization via SVD 133

12.6 Higher-Order Eigenvalue Problems 135

- 12.6.1 Conversion to first-order form 135

###### 13 Kronecker Products 139

- 13.1 Definition and Examples 139
- 13.2 Properties of the Kronecker Product 140
- 13.3 Application to Sylvester and Lyapunov Equations 144

###### Bibliography 151 Index 153

###### This page intentionally left blank

![image 12](<Matrix Analysis For Scientists and Engineers_images/imageFile12.png>)

![image 13](<Matrix Analysis For Scientists and Engineers_images/imageFile13.png>)

###### Preface

This book is intended to be used as a text for beginning graduate-level (or even senior-level) students in engineering, the sciences, mathematics, computer science, or computational science who wish to be familar with enough matrix analysis that they are prepared to use its tools and ideas comfortably in a variety of applications. By matrix analysis I mean linear algebra and matrix theory together with their intrinsic interaction with and application to linear dynamical systems (systems of linear differential or difference equations). The text can be used in a one-quarter or one-semester course to provide a compact overview of much of the important and useful mathematics that, in many cases, students meant to learn thoroughly as undergraduates, but somehow didn't quite manage to do. Certain topics that may have been treated cursorily in undergraduate courses are treated in more depth and more advanced material is introduced. I have tried throughout to emphasize only the more important and "useful" tools, methods, and mathematical structures. Instructors are encouraged to supplement the book with specific application examples from their own particular subject area.

The choice of topics covered in linear algebra and matrix theory is motivated both by applications and by computational utility and relevance. The concept of matrix factorization is emphasized throughout to provide a foundation for a later course in numerical linear algebra. Matrices are stressed more than abstract vector spaces, although Chapters 2 and 3 do cover some geometric (i.e., basis-free or subspace) aspects of many of the fundamental notions. The books by Meyer [18], Noble and Daniel [20], Ortega [21], and Strang [24] are excellent companion texts for this book. Upon completion of a course based on this text, the student is then well-equipped to pursue, either via formal courses or through selfstudy, follow-on topics on the computational side (at the level of [7], [11], [23], or [25], for example) or on the theoretical side (at the level of [12], [13], or [16], for example).

Prerequisites for using this text are quite modest: essentially just an understanding of calculus and definitely some previous exposure to matrices and linear algebra. Basic concepts such as determinants, singularity of matrices, eigenvalues and eigenvectors, and positive definite matrices should have been covered at least once, even though their recollection may occasionally be "hazy." However, requiring such material as prerequisite permits the early (but "out-of-order" by conventional standards) introduction of topics such as pseudoinverses and the singular value decomposition (SVD). These powerful and versatile tools can then be exploited to provide a unifying foundation upon which to base subsequent topics. Because tools such as the SVD are not generally amenable to "hand computation," this approach necessarily presupposes the availability of appropriate mathematical software on a digital computer. For this, I highly recommend MATLAB® although other software such as

xi

![image 14](<Matrix Analysis For Scientists and Engineers_images/imageFile14.png>)

xii Preface

Mathematica® or Mathcad® is also excellent. Since this text is not intended for a course in numerical linear algebra per se, the details of most of the numerical aspects of linear algebra are deferred to such a course.

The presentation of the material in this book is strongly influenced by computational issues for two principal reasons. First, "real-life" problems seldom yield to simple closed-form formulas or solutions. They must generally be solved computationally and it is important to know which types of algorithms can be relied upon and which cannot. Some of the key algorithms of numerical linear algebra, in particular, form the foundation upon which rests virtually all of modern scientific and engineering computation. A second motivation for a computational emphasis is that it provides many of the essential tools for what I call "qualitative mathematics." For example, in an elementary linear algebra course, a set of vectors is either linearly independent or it is not. This is an absolutely fundamental concept. But in most engineering or scientific contexts we want to know more than that. If a set of vectors is linearly independent, how "nearly dependent" are the vectors? If they are linearly dependent, are there "best" linearly independent subsets? These turn out to be much more difficult problems and frequently involve research-level questions when set in the context of the finite-precision, finite-range floating-point arithmetic environment of most modern computing platforms.

Some of the applications of matrix analysis mentioned briefly in this book derive from the modern state-space approach to dynamical systems. State-space methods are now standard in much of modern engineering where, for example, control systems with large numbers of interacting inputs, outputs, and states often give rise to models of very high order that must be analyzed, simulated, and evaluated. The "language" in which such models are conveniently described involves vectors and matrices. It is thus crucial to acquire a working knowledge of the vocabulary and grammar of this language. The tools of matrix analysis are also applied on a daily basis to problems in biology, chemistry, econometrics, physics, statistics, and a wide variety of other fields, and thus the text can serve a rather diverse audience. Mastery of the material in this text should enable the student to read and understand the modern language of matrices used throughout mathematics, science, and engineering.

While prerequisites for this text are modest, and while most material is developed from basic ideas in the book, the student does require a certain amount of what is conventionally referred to as "mathematical maturity." Proofs are given for many theorems. When they are not given explicitly, they are either obvious or easily found in the literature. This is ideal material from which to learn a bit about mathematical proofs and the mathematical maturity and insight gained thereby. It is my firm conviction that such maturity is neither encouraged nor nurtured by relegating the mathematical aspects of applications (for example, linear algebra for elementary state-space theory) to an appendix or introducing it "on-the-fly" when necessary. Rather, one must lay a firm foundation upon which subsequent applications and perspectives can be built in a logical, consistent, and coherent fashion.

I have taught this material for many years, many times at UCSB and twice at UC Davis, and the course has proven to be remarkably successful at enabling students from disparate backgrounds to acquire a quite acceptable level of mathematical maturity and rigor for subsequent graduate studies in a variety of disciplines. Indeed, many students who completed the course, especially the first few times it was offered, remarked afterward that if only they had had this course before they took linear systems, or signal processing,

![image 15](<Matrix Analysis For Scientists and Engineers_images/imageFile15.png>)

Preface xiii

or estimation theory, etc., they would have been able to concentrate on the new ideas they wanted to learn, rather than having to spend time making up for deficiencies in their background in matrices and linear algebra. My fellow instructors, too, realized that by requiring this course as a prerequisite, they no longer had to provide as much time for "review" and could focus instead on the subject at hand. The concept seems to work.

— AJL, June 2004

###### This page intentionally left blank

![image 16](<Matrix Analysis For Scientists and Engineers_images/imageFile16.png>)

![image 17](<Matrix Analysis For Scientists and Engineers_images/imageFile17.png>)

- Chapter 1

###### Introduction and Review

###### 1.1 Some Notation and Terminology

We begin with a brief introduction to some standard notation and terminology to be used throughout the text. This is followed by a review of some basic notions in matrix analysis and linear algebra.

The following sets appear frequently throughout subsequent chapters:

- 1. Rn= the set of n-tuples of real numbers represented as column vectors. Thus, x e Rn means

where xi e R for i e n. Henceforth, the notation n denotes the set {1, ..., n}.

Note: Vectors are always column vectors. A row vector is denoted by yT, where y G Rn and the superscript T is the transpose operation. That a vector is always a column vector rather than a row vector is entirely arbitrary, but this convention makes it easy to recognize immediately throughout the text that, e.g., XTy is a scalar while xyT is an n x n matrix.

- 2. Cn = the set of n-tuples of complex numbers represented as column vectors.
- 3. Rmxn = the set of real (or real-valued) m x n matrices.
- 4. Rmxnr = the set of real m x n matrices of rank r. Thus, Rnxnn denotes the set of real nonsingular n x n matrices.
- 5. Cmxn = the set of complex (or complex-valued) m x n matrices.
- 6. Cmxn = the set of complex m x n matrices of rank r.

1

![image 18](<Matrix Analysis For Scientists and Engineers_images/imageFile18.png>)

Chapter 1. Introduction and Review

- 2

We now classify some of the more familiar "shaped" matrices. A matrix A e (or A eC"x")is

- • diagonal if a,7 = 0 for i ^ j.
- • upper triangular if a,; = 0 for i > j.
- • lower triangular if a,7 = 0 for / < j.
- • tridiagonal if a(y = 0 for |z — j\ > 1.
- • pentadiagonal if ai; = 0 for |/ — j\ > 2.
- • upper Hessenberg if afj = 0 for i — j > 1.
- • lower Hessenberg if a,; = 0 for j — i > 1.

Each of the above also has a "block" analogue obtained by replacing scalar components in the respective definitions by block submatrices. For example, if A e Rnxn, B e Rmxn, and C e Rmxm, then the (m + n) x (m + n) matrix [ A0 Bc ] is block upper triangular.

The transpose of a matrix A is denoted by AT and is the matrix whose (i, j)th entry is the (7, Oth entry of A, that is, (A7),, = a,,. Note that if A e Rmx", then A7" e E"xm. If A e Cmx", then its Hermitian transpose (or conjugate transpose) is denoted by AH (or sometimes A*) and its (i, j)\h entry is (AH),7 = («77), where the bar indicates complex conjugation; i.e., if z = a + jf$ (j = i = v^T), then z = a — jfi. A matrix A is symmetric if A = AT and Hermitian if A = AH. We henceforth adopt the convention that, unless otherwise noted, an equation like A = AT implies that A is real-valued while a statement like A = AH implies that A is complex-valued.

- Remark 1.1. While \/—\ is most commonly denoted by i in mathematics texts, j is the more common notation in electrical engineering and system theory. There is some advantage to being conversant with both notations. The notation j is used throughout the text but reminders are placed at strategic locations.

###### Example 1.2.

is symmetric (and Hermitian).

is complex-valued symmetric but not Hermitian.

is Hermitian (but not symmetric).

Transposes of block matrices can be defined in an obvious way. For example, it is easy to see that if A,, are appropriately dimensioned subblocks, then

![image 19](<Matrix Analysis For Scientists and Engineers_images/imageFile19.png>)

- 1.2. Matrix Arithmetic

3

###### 1.2 Matrix Arithmetic

It is assumed that the reader is familiar with the fundamental notions of matrix addition, multiplication of a matrix by a scalar, and multiplication of matrices.

A special case of matrix multiplication occurs when the second matrix is a column vector x, i.e., the matrix-vector product Ax. A very important way to view this product is to interpret it as a weighted sum (linear combination) of the columns of A. That is, suppose

Then

The importance of this interpretation cannot be overemphasized. As a numerical example, take A = [96 85 74]x = 2 . Then we can quickly calculate dot products of the rows of A with the column x to find Ax =[50 32]' but this matrix-vector product can also be computed

v1a

For large arrays of numbers, there can be important computer-architecture-related advantages to preferring the latter calculation method.

For matrix multiplication, suppose A e Rmxn and B = [bi,...,bp] e Rnxp with bi e W1. Then the matrix product A B can be thought of as above, applied p times:

There is also an alternative, but equivalent, formulation of matrix multiplication that appears frequently in the text and is presented below as a theorem. Again, its importance cannot be overemphasized. It is deceptively simple and its full understanding is well rewarded.

- Theorem 1.3. Let U = [MI, ..., un] e Rmxn with ut e Rm and V = [v{,..., vn] e Rpxn with vt e Rp. Then

If matrices C and D are compatible for multiplication, recall that (CD)T = DTCT (or (CD}H — DHCH). This gives a dual to the matrix-vector result above. Namely, if C eRmxn has row vectors cj e Elx", and is premultiplied by a row vector yTe Rlxm, then the product can be written as a weighted linear sum of the rows of C as follows:

- Theorem 1.3 can then also be generalized to its "row dual." The details are left to the readei

![image 20](<Matrix Analysis For Scientists and Engineers_images/imageFile20.png>)

4

Chapter 1. Introduction and Review

###### 1.3 Inner Products and Orthogonality

For vectors x, y e R", the Euclidean inner product (or inner product, for short) of x and y is given by

Note that the inner product is a scalar.

If x, y e C", we define their complex Euclidean inner product (or inner product, for short) by

Note that (x, y)c = (y, x)c, i.e., the order in which x and y appear in the complex inner product is important. The more conventional definition of the complex inner product is (x,y)c = yHx = Eni=1 xiyi but throughout the text we prefer the symmetry with the real case.

- Example 1.4. Let x = [ 1j ] and y = [ 1/2 ]. Then

while

and we see that, indeed, (x, y)c = (y, x)c.

Note that x Tx = 0 if and only if x = 0 when x e Rn but that this is not true if x e Cn. What is true in the complex case is that XH x = 0 if and only if x = 0. To illustrate, consider the nonzero vector x above. Then XTX = 0 but XHX = 2.

Two nonzero vectors x, y e R are said to be orthogonal if their inner product is zero, i.e., xTy = 0. Nonzero complex vectors are orthogonal if XHy = 0. If x and y are orthogonal and XTX = 1 and yTy = 1, then we say that x and y are orthonormal. A matrix A e Rnxn is an orthogonal matrix if ATA = AAT = /, where / is the n x n identity matrix. The notation /„ is sometimes used to denote the identity matrix in Rnx" (orC"x"). Similarly, a matrix A e Cnxn is said to be unitary if AH A = AAH = I. Clearly an orthogonal or unitary matrix has orthonormal rows and orthonormal columns. There is no special name attached to a nonsquare matrix A e Rmxn (or € Cmxn) with orthonormal rows or columns.

###### 1.4 Determinants

It is assumed that the reader is familiar with the basic theory of determinants. For A e R nxn (or A 6 Cnxn) we use the notation det A for the determinant of A. We list below some of

![image 21](<Matrix Analysis For Scientists and Engineers_images/imageFile21.png>)

- 1.4. Determinants

5

the more useful properties of determinants. Note that this is not a minimal set, i.e., several properties are consequences of one or more of the others.

- 1. If A has a zero row or if any two rows of A are equal, then det A = 0.
- 2. If A has a zero column or if any two columns of A are equal, then det A = 0.
- 3. Interchanging two rows of A changes only the sign of the determinant.
- 4. Interchanging two columns of A changes only the sign of the determinant.
- 5. Multiplying a row of A by a scalar a results in a new matrix whose determinant is a det A.
- 6. Multiplying a column of A by a scalar a results in a new matrix whose determinant is a det A.
- 7. Multiplying a row of A by a scalar and then adding it to another row does not change the determinant.
- 8. Multiplying a column of A by a scalar and then adding it to another column does not change the determinant.
- 9. det AT = det A (det AH = det A if A e Cnxn).
- 10. If A is diagonal, then det A = a11a22 • • • ann, i.e., det A is the product of its diagonal elements.
- 11. If A is upper triangular, then det A = a11a22 • • • ann.
- 12. If A is lower triangular, then det A = a11a22 • • • ann.
- 13. If A is block diagonal (or block upper triangular or block lower triangular), with square diagonal blocks A11, A22, • • •, Ann (of possibly different sizes), then det A = det A11 det A22 • • • det Ann.
- 14. If A, B eRnxn,thendet(AB) = det A det 5.
- 15. If A € Rnxn, then det(A-1) = 1det A.
- 16. If A e Rnxnand D e Rmxm, then det [AcBD] = del A det(D – CA–l B). Proof: This follows easily from the block LU factorization
- 17. If A eRn xn and D e RMmxm, then det [Ac BD] = det D det(A – BD–1C). Proof: This follows easily from the block UL factorization

![image 22](<Matrix Analysis For Scientists and Engineers_images/imageFile22.png>)

Chapter 1. Introduction and Review

- 6

- Remark 1.5. The factorization of a matrix A into the product of a unit lower triangular matrix L (i.e., lower triangular with all 1's on the diagonal) and an upper triangular matrix

- U is called an LU factorization; see, for example, [24]. Another such factorization is UL where U is unit upper triangular and L is lower triangular. The factorizations used above are block analogues of these.

- Remark 1.6. The matrix D — CA–1B is called the Schur complement of A in [AC BD]. Similarly, A – BD–lC is the Schur complement of D in [AC BD ].

###### EXERCISES

- 1. If A e Rnxn and or is a scalar, what is det(aA)? What is det(–A)?
- 2. If A is orthogonal, what is det A? If A is unitary, what is det A?
- 3. Let x, y e Rn. Show that det(I – xyT) = 1 – yTx.
- 4. Let U1, U2, . . ., Uk € Rnxn be orthogonal matrices. Show that the product U = U1 U2 • • • Uk is an orthogonal matrix.
- 5. Let A e Rnxn. The trace of A, denoted TrA, is defined as the sum of its diagonal elements, i.e., TrA = Eni=1 aii.

- (a) Show that the trace is a linear function; i.e., if A, B e Rnxn and a, ft e R, then Tr(aA + fiB)= aTrA + fiTrB.
- (b) Show that Tr(Afl) = Tr(£A), even though in general AB ^ B A.
- (c) Let S € Rnxn be skew-symmetric, i.e., ST = -S. Show that TrS = 0. Then either prove the converse or provide a counterexample.

- 6. A matrix A e Wx" is said to be idempotent if A2 = A. / x ™ . , • , ! T 2cos2<9 sin 20 1 . . _,

- (a) Show that the matrix A = - . _.. _ . 2rt is idempotent for all #. 2 |_ sin 2^ 2smz# J r
- (b) Suppose A e IR"X" is idempotent and A ^ I. Show that A must be singular.

![image 23](<Matrix Analysis For Scientists and Engineers_images/imageFile23.png>)

- Chapter 2

###### Vector Spaces

In this chapter we give a brief review of some of the basic concepts of vector spaces. The emphasis is on finite-dimensional vector spaces, including spaces formed by special classes of matrices, but some infinite-dimensional examples are also cited. An excellent reference for this and the next chapter is [10], where some of the proofs that are not given here may be found.

###### 2.1 Definitions and Examples

- Definition 2.1. A field is a set F together with two operations +, • : F x F —> F such that

(Al) a + (P + y) = (a + p) + yfor all a, ft, y € F.

- (A2) there exists an element 0 e F such that a + 0 = a. for all a e F.
- (A3) for all a e F, there exists an element (—a) e F such that a + (—a) = 0.
- (A4) a + p = ft + afar all a, ft e F. (Ml) a - ( p - y ) = (a- p ) - y f o r all a, p, y e F. (M2) there exists an element 1 e F such that a • I = a for all a e F. (M3) for all a e ¥, a ^ 0, there exists an element a"1 € F such that a • a~l = 1. (M4) a • p = P • a for all a, p e F. (D) a - ( p + y)=ci-p+a- y for alia, p,ye¥.

Axioms (A1)-(A3) state that (F, +) is a group and an abelian group if (A4) also holds. Axioms (M1)-(M4) state that (F \ {0}, •) is an abelian group.

Generally speaking, when no confusion can arise, the multiplication operator "•" is not written explicitly.

7

![image 24](<Matrix Analysis For Scientists and Engineers_images/imageFile24.png>)

Chapter 2. Vector Spaces

###### Example 2.2.

- 1. R with ordinary addition and multiplication is a field.
- 2. C with ordinary complex addition and multiplication is a field.
- 3. Raf.r] = the field of rational functions in the indeterminate x

8

where Z+ = {0,1,2, ...}, is a field.

- 4. RMrmxn = { m x n matrices of rank r with real coefficients) is clearly not a field since, for example, (Ml) does not hold unless m = n. Moreover, R"x" is not a field either since (M4) does not hold in general (although the other 8 axioms hold).

###### Definition 2.3. A vector space over a field F is a set V together with two operations

+ :V x V -^V and- : F xV -»• V such that

(VI) (V, +) is an abelian group. (V2) ( a - p ) - v = a - ( P ' V ) f o r all a, p e F and for all v e V. (V3) (a + ft) • v = a • v + p • v for all a, p € F and for all v e V. (V4) a-(v + w)=a-v + a- w for all a e F and for all v, w e V. (V5) 1 • v = v for all v e V (1 e F).

A vector space is denoted by (V, F) or, when there is no possibility of confusion as to the underlying fie Id, simply by V.

- Remark 2.4. Note that + and • in Definition 2.3 are different from the + and • in Definition

- 2.1 in the sense of operating on different objects in different sets. In practice, this causes no confusion and the • operator is usually not even written explicitly.

###### Example 2.5.

- 1. (R", R) with addition defined by

and scalar multiplication defined by

is a vector space. Similar definitions hold for (C", C).

![image 25](<Matrix Analysis For Scientists and Engineers_images/imageFile25.png>)

###### 2.2. Subspaces

9

2. (Emxn, E) is a vector space with addition defined by

and scalar multiplication defined by

3. Let (V, F) be an arbitrary vector space and V be an arbitrary set. Let O(X>, V) be the set of functions / mapping D to V. Then O(D, V) is a vector space with addition defined by

and scalar multiplication defined by

###### Special Cases:

(a) V = [to, t\], (V, F) = (IR", E), and the functions are piecewise continuous

=: (PC[f0, t\])n or continuous =: (C[?0, h])n.

4. Let A € R"x". Then (x(t) : x(t) = Ax(t}} is a vector space (of dimension n).

###### 2.2 Subspaces

- Definition 2.6. Let (V, F) be a vector space and let W c V, W = 0. Then (W, F) is a subspace of (V, F) if and only if (W, F) is itself a vector space or, equivalently, if and only if(aw1 + ßW2) e W for all a, ß e ¥ and for all w1, w2 e W.

Remark 2.7. The latter characterization of a subspace is often the easiest way to check or prove that something is indeed a subspace (or vector space); i.e., verify that the set in question is closed under addition and scalar multiplication. Note, too, that since 0 e F, this implies that the zero vector must be in any subspace.

Notation: When the underlying field is understood, we write W c V, and the symbol c, when used with vector spaces, is henceforth understood to mean "is a subspace of." The less restrictive meaning "is a subset of" is specifically flagged as such.

![image 26](<Matrix Analysis For Scientists and Engineers_images/imageFile26.png>)

10 Chapter 2. Vector Spaces

###### Example 2.8.

- 1. Consider (V, F) = (R"X",R) and let W = [A e R"x" : A is symmetric}. Then We V.

Proof: Suppose A\, A2 are symmetric. Then it is easily shown that ctA\ + fiAi is symmetric for all a, ft e R.

- 2. Let W = {A € R"x" : A is orthogonal}. Then W is /wf a subspace of R"x".
- 3. Consider (V, F) = (R2, R) and for each v € R2 of the form v = [v1v2 ] identify v1 with the jc-coordinate in the plane and u2 with the y-coordinate. For a, ß e R, define

Then Wa,ß is a subspace of V if and only if ß = 0. As an interesting exercise, sketch W2,1, W2,o, W1/2,1, and W1/2,0. Note, too, that the vertical line through the origin (i.e., a = oo) is also a subspace.

All lines through the origin are subspaces. Shifted subspaces Wa,ß with ß = 0 are called linear varieties.

Henceforth, we drop the explicit dependence of a vector space on an underlying field. Thus, V usually denotes a vector space with the underlying field generally being R unless explicitly stated otherwise.

- Definition 2.9. If 12, and S are vector spaces (or subspaces), then R = S if and only if

- R C S and S C R.

Note: To prove two vector spaces are equal, one usually proves the two inclusions separately: An arbitrary r e R is shown to be an element of S and then an arbitrary 5 € S is shown to be an element of R.

2.3 Linear Independence

Let X = {v1, v2, • • •} be a nonempty collection of vectors u, in some vector space V.

- Definition 2.10. X is a linearly dependent set of vectors if and only if there exist k distinct elements v1, . . . , vk e X and scalars a1, . . . , ak not all zero such that

X is a linearly independent set of vectors if and only if for any collection of k distinct elements v1, . . . ,Vk of X and for any scalars a1, . . . , ak,

![image 27](<Matrix Analysis For Scientists and Engineers_images/imageFile27.png>)

- 2.3. Linear Independence 11

###### Example 2.11.

- 1. LetV = R3. Then

is a linearly independent set. Why?

However, s a linearly dependent set

(since 2v\ — v2 + v3 = 0).

2. Let A e R xn and 5 e R" xm. Then consider the rows of etA B as vectors in Cm [t0, t1] (recall that efA denotes the matrix exponential, which is discussed in more detail in Chapter 11). Independence of these vectors turns out to be equivalent to a concept called controllability, to be studied further in what follows.

Let vf e R", i e k, and consider the matrix V = [v1, ... ,Vk] e Rnxk. The linear dependence of this set of vectors is equivalent to the existence of a nonzero vector a e Rk such that Va = 0. An equivalent condition for linear dependence is that the k x k matrix VT V is singular. If the set of vectors is independent, and there exists a e R* such that Va = 0, then a = 0. An equivalent condition for linear independence is that the matrix VTV is nonsingular.

- Definition 2.12. Let X = [v1, v2,...} be a collection of vectors vi. e V. Then the span of X is defined as

where N = {1, 2, ...}.

Example 2.13. Let V = Rn and define

Then Sp{e1, e2, ...,en} = Rn.

- Definition 2.14. A set of vectors X is a basis for V if and only ij

- 1. X is a linearly independent set (of basis vectors), and
- 2. Sp(X) = V.

![image 28](<Matrix Analysis For Scientists and Engineers_images/imageFile28.png>)

12 Chapter 2. Vector Spaces

- Example 2.15. [e\,..., en} is a basis for IR" (sometimes called the natural basis).

Now let b1, ..., bn be a basis (with a specific order associated with the basis vectors) for V. Then for all v e V there exists a unique n-tuple {E1 ,...,En} such that

where

- Definition 2.16. The scalars {Ei} are called the components (or sometimes the coordinates)

of v with respect to the basis (b1, ..., bn] and are unique. We say that the vector x of components represents the vector v with respect to the basis B.

###### Example 2.17. In Rn,

We can also determine components of v with respect to another basis. For example, while

with respect to the basis

we have

To see this, write

Then

- Theorem 2.18. The number of elements in a basis of a vector space is independent of the particular basis considered.

- Definition 2.19. If a basis X for a vector space V= 0) has n elements, V is said to be n-dimensional or have dimension n and we write dim(V) = n or dim V — n. For

![image 29](<Matrix Analysis For Scientists and Engineers_images/imageFile29.png>)

- 2.4. Sums and Intersections of Subspaces 13

consistency, and because the 0 vector is in any vector space, we define dim(O) = 0. A vector space V is finite-dimensional if there exists a basis X with n < +00 elements; otherwise, V is infinite-dimensional.

Thus, Theorem 2.18 says that dim(V) = the number of elements in a basis.

###### Example 2.20.

- 1. dim(Rn)=n.
- 2. dim(Rmxn) = mn.

Note: Check that a basis for Rmxn is given by the mn matrices Eij; i e m, j e n, where Efj is a matrix all of whose elements are 0 except for a 1 in the (i, j)th location. The collection of Eij matrices can be called the "natural basis matrices."

- 3. dim(C[to, t1]) - +00.
- 4. dim{A € Rnxn : A = AT} = {1/2(n + 1).

1

(To see why, determine 1/22 n(n + 1) symmetric basis matrices.)

- 5. dim{A e Rnxn : A is upper (lower) triangular} = 1/2n(n + 1).

###### 2.4 Sums and Intersections of Subspaces

Definition 2.21. Let (V, F) be a vector space and let 71, S c V. The sum and intersection of R, and S are defined respectively by:

- 1. n + S = {r + s : r e U, s e 5}.
- 2. ft H 5 = {v : v e 7^ and v e 5}.

- Theorem 2.22.

K

- 1. K + S C V (in general, U\ -\ h 7^ =: ]T ft/ C V, for finite k). 1=1
- 2. 72. D 5 C V (in general, f] *R,a C V/or an arbitrary index set A). a e A

Remark 2.23. The union of two subspaces, R C S, is not necessarily a subspace.

- Definition 2.24. T = R 0 S is the direct sum of R and S if

- 1. n n S = 0, and
- 2. U + S = T (in general ft; n (^ ft,-) = 0 am/ ]P ft,- = T). y>f «

The subspaces R, and S are said to be complements of each other in T.

![image 30](<Matrix Analysis For Scientists and Engineers_images/imageFile30.png>)

14 Chapter 2. Vector Spaces

- Remark 2.25. The complement of ft (or S) is not unique. For example, consider V = R2 and let ft be any line through the origin. Then any other distinct line through the origin is a complement of ft. Among all the complements there is a unique one orthogonal to ft. We discuss more about orthogonal complements elsewhere in the text.

- Theorem 2.26. Suppose T =R O S. Then

- 1. every t € T can be written uniquely in the form t = r + s with r e R and s e S.
- 2. dim(T) = dim(ft) + dim(S).

Proof: To prove the first part, suppose an arbitrary vector t e T can be written in two ways as t = r1 + s1 = r2 + S2, where r1, r2 e R. and s1, S2 e S. Then r1 — r2 = s2— s\. But r1 –r2 £ ft and 52 — si e S. Since ft fl S = 0, we must have r\ = r-i and s\ = si from which uniqueness follows.

The statement of the second part is a special case of the next theorem. D

- Theorem 2.27. For arbitrary subspaces ft, S of a vector space V,

- Example 2.28. Let U be the subspace of upper triangular matrices in E" x" and let £ be the subspace of lower triangular matrices in Rnxn. Then it may be checked that U + L = Rnxn while U n £ is the set of diagonal matrices in Rnxn. Using the fact that dim (diagonal matrices} = n, together with Examples 2.20.2 and 2.20.5, one can easily verify the validity of the formula given in Theorem 2.27.
- Example 2.29. Let (V, F) = (Rnxn, R), let ft be the set of skew-symmetric matrices in R"x", and let S be the set of symmetric matrices in R"x". Then V = U 0 S. Proof: This follows easily from the fact that any A e R"x" can be written in the form

The first matrix on the right-hand side above is in S while the second is in ft.

###### EXERCISES

- 1. Suppose {vi,..., Vk} is a linearly dependent set. Then show that one of the vectors must be a linear combination of the others.
- 2. Let x\, *2, ..., x/c E R" be nonzero mutually orthogonal vectors. Show that [x\,..., Xk} must be a linearly independent set.
- 3. Let v\,... ,vn be orthonormal vectors in R". Show that Av\,..., Avn are also orthonormal if and only if A e R"x" is orthogonal.
- 4. Consider the vectors v\ — [2 l]r and 1*2 = [3 l]r. Prove that vi and V2 form a basis for R2. Find the components of the vector v = [4 l]r with respect to this basis.

![image 31](<Matrix Analysis For Scientists and Engineers_images/imageFile31.png>)

Exercises 15

- 5. Let P denote the set of polynomials of degree less than or equal to two of the form Po + p\x + pix2, where po, p\, p2 e R. Show that P is a vector space over E. Show that the polynomials 1, *, and 2x2 — 1 are a basis for P. Find the components of the polynomial 2 + 3x + 4x2 with respect to this basis.
- 6. Prove Theorem 2.22 (for the case of two subspaces R and S only).
- 7. Let Pn denote the vector space of polynomials of degree less than or equal to n, and of the form p(x) = po + p\x + • • • + pnxn, where the coefficients /?, are all real. Let PE denote the subspace of all even polynomials in Pn, i.e., those that satisfy the property p(—x} = p(x). Similarly, let PQ denote the subspace of all odd polynomials, i.e., those satisfying p(—x} = –p(x). Show that Pn = PE © PO-
- 8. Repeat Example 2.28 using instead the two subspaces 7" of tridiagonal matrices and U of upper triangular matrices.

###### This page intentionally left blank

![image 32](<Matrix Analysis For Scientists and Engineers_images/imageFile32.png>)

![image 33](<Matrix Analysis For Scientists and Engineers_images/imageFile33.png>)

- Chapter 3

###### Linear Transformations

###### 3.1 Definition and Examples

We begin with the basic definition of a linear transformation (or linear map, linear function, or linear operator) between two vector spaces.

- Definition 3.1. Let (V, F) and (W, F) be vector spaces. Then C : V -> W is a linear transformation if and only if

£(avi + pv2) = aCv\ + fi£v2 far all a, £ e F and far all v},v2e V.

The vector space V is called the domain of the transformation C while VV, the space into which it maps, is called the co-domain.

###### Example 3.2.

- 1. Let F = R and take V = W = PC[f0, +00). Define £ : PC[t0, +00) -> PC[t0, +00) by
- 2. Let F = R and take V = W = Rmx". Fix M e Rmxm. Define £ : Rmx" -> Mmxn by
- 3. Let F = R and take V = P" = (p(x) = a0 + ct}x H h anx" : a, E R} and w = -pn-1. Define C.: V —> W by Lp — p', where' denotes differentiation with respect to x.

17

![image 34](<Matrix Analysis For Scientists and Engineers_images/imageFile34.png>)

18 Chapters. Li near Transformations

###### 3.2 Matrix Representation of Linear Transformations

Linear transformations between vector spaces with specific bases can be represented conveniently in matrix form. Specifically, suppose £ : (V, F) —>• (W, F) is linear and further suppose that {u,, i e n} and {Wj, j e m] are bases for V and W, respectively. Then the ith column of A = Mat £ (the matrix representation of £ with respect to the given bases for V and W) is the representation of £i>, with respect to {w}•, j e raj. In other words,

represents £ since

where W = [w\,..., wm] and

is the z'th column of A. Note that A = Mat £ depends on the particular bases for V and W. This could be reflected by subscripts, say, in the notation, but this is usually not done.

The action of £ on an arbitrary vector v e V is uniquely determined (by linearity) by its action on a basis. Thus, if v = E1v1 + • • • + Envn = Vx (where u, and hence jc, is arbitrary), then

Thus, £V = WA since x was arbitrary.

When V = R", W = Rm and [vi, i e n}, [wj, j e m} are the usual (natural) bases the equation £V = WA becomes simply £ = A. We thus commonly identify A as a linea transformation with its matrix representation, i.e.,

Thinking of A both as a matrix and as a linear transformation from Rn to Rm usually causes no confusion. Change of basis then corresponds naturally to appropriate matrix multiplication.

![image 35](<Matrix Analysis For Scientists and Engineers_images/imageFile35.png>)

- 3.3. Composition of Transformations 19

###### 3.3 Composition of Transformations

Consider three vector spaces U, V, and W and transformations B from U to V and A from

- V to W. Then we can define a new transformation C as follows:

The above diagram illustrates the composition of transformations C = AB. Note that in most texts, the arrows above are reversed as follows:

However, it might be useful to prefer the former since the transformations A and B appear in the same order in both the diagram and the equation. If dimZ// = p, dimV = n, and dim W = m, and if we associate matrices with the transformations in the usual way, then composition of transformations corresponds to standard matrix multiplication. That is, we have C — A B . The above is sometimes expressed componentwise by the

formula

Two Special Cases: Inner Product: Let x, y e Rn. Then their inner product is the scalar

Outer Product: Let x e Rm, y e Rn. Then their outer product is the m x n matrix

Note that any rank-one matrix A e Rmxn can be written in the form A = xyT above (or xyH if A e Cmxn). A rank-one symmetric matrix can be written in the form XXT (or XXH).

![image 36](<Matrix Analysis For Scientists and Engineers_images/imageFile36.png>)

20 Chapter 3. Li near Transformations

###### 3.4 Structure of Linear Transformations Let A : V —> W be a linear transformation.

Definition 3.3. The range of A, denotedlZ( A), is the set {w e W : w = Av for some v e V}. Equivalently, R(A) — {Av : v e V}. The range of A is also known as the image of A and denoted Im(A).

The nullspace of A, denoted N(A), is the set {v e V : Av = 0}. The nullspace of

- A is also known as the kernel of A and denoted Ker (A).

- Theorem 3.4. Let A : V —>• W be a linear transformation. Then

- 1. R(A) C W.
- 2. N(A) c V. Note that N(A) and R(A) are, in general, subspaces of different spaces.

- Theorem 3.5. Let A e Rmxn. If A is written in terms of its columns as A = [a\,... ,an],

then

then

Proof: The proof of this theorem is easy, essentially following immediately from the definition. D

- Remark 3.6. Note that in Theorem 3.5 and throughout the text, the same symbol (A) is used to denote both a linear transformation and its matrix representation with respect to the usual (natural) bases. See also the last paragraph of Section 3.2.

- Definition 3.7. Let {v1,..., vk] be a set of nonzero vectors u, e Rn. The set is said to

be orthogonal if' vjvj = 0 for i ^ j and orthonormal if vf vj = 8ij, where 8tj is the Kronecker delta defined by

- Example 3.8. is an orthogonal set.

is an orthonormal set.

3. If {t>i,..., Vk} with u, € M." is an orthogonal set, then I —/==, - -., —/=== | is an

I ^/v, vi ^/v'k vk ]

orthonormal set.

![image 37](<Matrix Analysis For Scientists and Engineers_images/imageFile37.png>)

- 3.4. Structure of Linear Transformations 21

- Definition 3.9. Let S c Rn. Then the orthogonal complement of S is defined as the set S1- = {v e Rn : VTS = 0 for all s e S}.

###### Example 3.10. Let

Then it can be shown that

Working from the definition, the computation involved is simply to find all nontrivial (i.e., nonzero) solutions of the system of equations

Note that there is nothing special about the two vectors in the basis defining S being orthogonal. Any set of vectors will do, including dependent spanning vectors (which would, of course, then give rise to redundant equations).

Theorem 311 Let R S C Rn The

Proof: We prove and discuss only item 2 here. The proofs of the other results are left as exercises. Let {v1, ..., vk} be an orthonormal basis for S and let x e Rn be an arbitrary vector. Set

![image 38](<Matrix Analysis For Scientists and Engineers_images/imageFile38.png>)

22 Chapters. Li near Transformations

Then x\ e <S and, since

we see that x2 is orthogonal to v1, ..., Vk and hence to any linear combination of these vectors. In other words, X2 is orthogonal to any vector in S. We have thus shown that

- S + S1 = Rn. We also have that S U S1 =0 since the only vector s e S orthogonal to everything in S (i.e., including itself) is 0.

It is also easy to see directly that, when we have such direct sum decompositions, we can write vectors in a unique way with respect to the corresponding subspaces. Suppose, for example, that x = x1 + x2. = x'1+ x'2, where x\, x 1 E S and x2, x'2 e S1. Then (x'1 — x1)T(x'2 — x2) = 0 by definition of ST. But then (x'1 — x1)T(x'1 – x1) = 0 since x2 — X2 = — (x'1 — x1) (which follows by rearranging the equation x1+x2 = x'1 + x'2). Thus, x1 — x'1 and x2 = x2. D

- Theorem 3.12. Let A : Rn —> Rm. Then

- 1. N(A)1" = 7£(Ar). (Note: This holds only for finite-dimensional vector spaces.)
- 2. 'R,(A)1~ — J\f(AT). (Note: This also holds for infinite-dimensional vector spaces.)

Proof: To prove the first part, take an arbitrary x e A/"(A). Then Ax = 0 and this is equivalent to yT Ax = 0 for all v. But yT Ax = (ATy) x. Thus, Ax = 0 if and only if x is orthogonal to all vectors of the form AT v, i.e., x e R(Ar) . Since x was arbitrary, we have established that N(A)1 = U(AT}.

The proof of the second part is similar and is left as an exercise. D

- Definition 3.13. Let A : Rn -> Rm. Then {v e R" : Av = 0} is sometimes called the right nullspace of A. Similarly, (w e Rm : WT A = 0} is called the left nullspace of A. Clearly, the right nullspace is A/"(A) while the left nullspace is J\f(AT).

Theorem 3.12 and part 2 of Theorem 3.11 can be combined to give two very fundamental and useful decompositions of vectors in the domain and co-domain of a linear transformation A. See also Theorem 2.26.

###### Theorem 3.14 (Decomposition Theorem). Let A : R" -> Rm. Then

7. every vector v in the domain space R" can be written in a unique way as v = x + y, where x € M(A) and y € J\f(A)± = ft(Ar) (i.e., R" = M(A) 0 ft(Ar)).

- 2. every vector w in the co-domain space Rm can be written in a unique way asw = x+y, where x e U(A) and y e ft(A)1- = Af(AT) (i.e., Rm = 7l(A) 0 M(AT)).

This key theorem becomes very easy to remember by carefully studying and understanding Figure 3.1 in the next section.

- 3.5 Four Fundamental Subspaces

Consider a general matrix A € E^x". When thought of as a linear transformation from E" to Rm, many properties of A can be developed in terms of the four fundamental subspaces

![image 39](<Matrix Analysis For Scientists and Engineers_images/imageFile39.png>)

- 3.5. Four Fundamental Subspaces 23

Figure 3.1. Four fundamental subspaces.

- 7£(A), 'R.(A)^, Af(A), and N(A)T. Figure 3.1 makes many key properties seem almost obvious and we return to this figure frequently both in the context of linear transformations and in illustrating concepts such as controllability and observability.

- Definition 3.15. Let V and W be vector spaces and let A : V motion.

- 1. A is onto (also called epic or surjective) ifR,(A) = W.

W be a linear transfor-

- 2. A is one-to-one or 1-1 (also called monic or infective) ifJ\f(A) = 0. Two equivalent characterizations of A being 1-1 that are often easier to verify in practice are the following:

- Definition 3.16. Let A : E" -> Rm. Then rank(A) = dimftCA). This is sometimes called the column rank of A (maximum number of independent columns). The row rank of A is

![image 40](<Matrix Analysis For Scientists and Engineers_images/imageFile40.png>)

24 Chapter3. Linear Transformations

dim 7£(Ar) (maximum number of independent rows). The dual notion to rank is the nullity of A, sometimes denoted nullity(A) or corank(A), and is defined as dim A/"(A).

- Theorem 3.17. Let A : Rn -> Rm. Then dim K(A) = dimA/'(A)±. (Note: Since A/^A)1" = 7l(AT), this theorem is sometimes colloquially stated "row rank of A = column rank of A.") Proof: Define a linear transformation T : J\f(A)~L —>• 7£(A) by

Clearly T is 1-1 (since A/"(T) = 0). To see that T is also onto, take any w e 7£(A). Then by definition there is a vector x e R" such that Ax — w. Write x = x\ + X2, where x\ e A/^A)1- and jc2 e A/"(A). Then Ajti = u; = r*i since *i e A/^A)-1. The last equality shows that T is onto. We thus have that dim7?.(A) = dimA/^A^ since it is easily shown that if {ui, ..., iv} is abasis forA/'CA)1, then {Tv\, ..., Tvr] is abasis for 7?.(A). Finally, if we apply this and several previous results, the following string of equalities follows easily: "column rank of A" = rank(A) = dim7e(A) = dim A/^A)1 = dim7l(AT) = rank(Ar) = "row rank of A." D

The following corollary is immediate. Like the theorem, it is a statement about equality of dimensions; the subspaces themselves are not necessarily in the same vector space. Corollary 3.18. Let A : R" -> Rm. Then dimA/"(A) + dimft(A) = n, where n is the dimension of the domain of A. Proof: From Theorems 3.11 and 3.17 we see immediately that

For completeness, we include here a few miscellaneous results about ranks of sums and products of matrices.

- Theorem 3.19. Let A, B e R"xn. Then

Part 4 of Theorem 3.19 suggests looking at the general problem of the four fundamental subspaces of matrix products. The basic results are contained in the following easily proved theorem.

![image 41](<Matrix Analysis For Scientists and Engineers_images/imageFile41.png>)

###### 3.5. Four Fundamental Subspaces 25

- Theorem 3.20. Let A e Rmxn, B e Rnxp. Then

The next theorem is closely related to Theorem 3.20 and is also easily proved. It is extremely useful in text that follows, especially when dealing with pseudoinverses and linear least squares problems.

- Theorem 3.21. Let A e Rmxn. Then

We now characterize 1-1 and onto transformations and provide characterizations in terms of rank and invertibility.

- Theorem 3.22. Let A : Rn -» Rm. Then

- 1. A is onto if and only //"rank(A) — m (A has linearly independent rows or is said to have full row rank; equivalently, AAT is nonsingular).
- 2. A is 1-1 if and only z/rank(A) = n (A has linearly independent columns or is said to have full column rank; equivalently, AT A is nonsingular).

Proof: Proof of part 1: If A is onto, dim7?,(A) — m — rank (A). Conversely, let y e Rm be arbitrary. Let jc = AT(AAT)~]y e Rn. Then y = Ax, i.e., y e 7?.(A), so A is onto.

Proof of part 2: If A is 1-1, then A/"(A) = 0, which implies that dim A/^A)-1 —n dim 7£(Ar), and hence dim 7£(A) = n by Theorem 3.17. Conversely, suppose Ax\ = Ax^. Then ArA;ti = AT Ax2, which implies x\ = x^. since ArA is invertible. Thus, A is

1-1. D

- Definition 3.23. A : V —» W is invertible (or bijective) if and only if it is 1-1 and onto. Note that if A is invertible, then dim V — dim W. Also, A : W1 -»• E" is invertible or nonsingular if and only z/rank(A) = n.

Note that in the special case when A € R"x", the transformations A, Ar, and A"1 are all 1-1 and onto between the two spaces M(A)± and 7£(A). The transformations AT and A~! have the same domain and range but are in general different maps unless A is orthogonal. Similar remarks apply to A and A~T.

![image 42](<Matrix Analysis For Scientists and Engineers_images/imageFile42.png>)

26 Chapters. Li near Transformations

If a linear transformation is not invertible, it may still be right or left invertible. Definitions of these concepts are followed by a theorem characterizing left and right invertible transformations.

- Definition 3.24. Let A : V -> W. Then

- 1. A is said to be right invertible if there exists a right inverse transformation A~R : W —> V such that AA~R = Iw, where Iw denotes the identity transformation on W.
- 2. A is said to be left invertible if there exists a left inverse transformation A~L : W —> V such that A~LA = Iv, where Iv denotes the identity transformation on V.

- Theorem 3.25. Let A : V -> W. Then

- 1. A is right invertible if and only if it is onto.
- 2. A is left invertible if and only if it is 1-1.

Moreover, A is invertible if and only if it is both right and left invertible, i.e., both 1-1 and onto, in which case A~l = A~R = A~L.

Note: From Theorem 3.22 we see that if A : E" ->• Em is onto, then a right inverse is given by A~R = AT(AAT) . Similarly, if A is 1-1, then a left inverse is given by A~L = (ATA)~1AT.

- Theorem 3.26. Let A : V -» V.

- 1. If there exists a unique right inverse A~R such that AA~R = I, then A is invertible.
- 2. If there exists a unique left inverse A~L such that A~LA = I, then A is invertible.

Proof: We prove the first part and leave the proof of the second to the reader. Notice the following:

Thus, (A R + A RA — /) must be a right inverse and, therefore, by uniqueness it must be the case that A~R + A~RA — I = A~R. But this implies that A~RA = /, i.e., that A~R is a left inverse. It then follows from Theorem 3.25 that A is invertible. D

###### Example 3.27.

1. Let A = [1 2] : E2 -»• E1. Then A is onto. (Proof: Take any a € E1; then one can always find v e E2 such that [1 2][^] = a). Obviously A has full row rank (=1) and A~R = [ _j j is a right inverse. Also, it is clear that there are infinitely many right inverses for A. In Chapter 6 we characterize all right inverses of a matrix by characterizing all solutions of the linear matrix equation AR = I.

![image 43](<Matrix Analysis For Scientists and Engineers_images/imageFile43.png>)

Exercises 27

- 2. Let A = [J] : E1 -> E2. ThenAis 1-1. (Proof: The only solution to 0 = Av = [I2]v is v = 0, whence A/"(A) = 0 so A is 1-1). It is now obvious that A has full column rank (=1) and A~L = [3 — 1] is a left inverse. Again, it is clear that there are infinitely many left inverses for A. In Chapter 6 we characterize all left inverses of a matrix by characterizing all solutions of the linear matrix equation LA = I.
- 3. The matrix

when considered as a linear transformation on IE below bases for its four fundamental subspaces.

\ is neither 1-1 nor onto. We give

###### EXERCISES

- 1. Let A = [8 53 J4 and consider A as a linear transformation mapping E3 to E2. Find the matrix representation of A with respect to the bases
- 2. Consider the vector space Rnx" over E, let S denote the subspace of symmetric matrices, and let 7£ denote the subspace of skew-symmetric matrices. For matrices X, Y e Enx" define their inner product by (X, Y) = Tr(XrF). Show that, with respect to this inner product, 'R, — S^.
- 3. Consider the differentiation operator C defined in Example 3.2.3. Is £ 1-1? Is£ onto?
- 4. Prove Theorem 3.4.

of R3 and

of E2.

![image 44](<Matrix Analysis For Scientists and Engineers_images/imageFile44.png>)

- 28 Chapters. Linear Transformations

- 5. Prove Theorem 3.11.4.
- 6. Prove Theorem 3.12.2.
- 7. Determine bases for the four fundamental subspaces of the matrix
- 8. Suppose A e Rmxn has a left inverse. Show that AT has a right inverse.
- 9. Let A = [ J o]. Determine A/"(A) and 7£(A). Are they equal? Is this true in general? If this is true in general, prove it; if not, provide a counterexample.
- 10. Suppose A € Mg9x48. How many linearly independent solutions can be found to the homogeneous linear system Ax = 0?
- 11. Modify Figure 3.1 to illustrate the four fundamental subspaces associated with AT e Rnxm thought of as a transformation from Rm to R".

![image 45](<Matrix Analysis For Scientists and Engineers_images/imageFile45.png>)

- Chapter 4

###### Introduction to the Moore-Pen rose Pseudoinverse

In this chapter we give a brief introduction to the Moore-Penrose pseudoinverse, a generalization of the inverse of a matrix. The Moore-Penrose pseudoinverse is defined for any matrix and, as is shown in the following text, brings great notational and conceptual clarity to the study of solutions to arbitrary systems of linear equations and linear least squares problems.

###### 4.1 Definitions and Characterizations

Consider a linear transformation A : X —>• y, where X and y are arbitrary finitedimensional vector spaces. Define a transformation T : Af(A)1- —>• Tl(A) by

Then, as noted in the proof of Theorem 3.17, T is bijective (1-1 and onto), and hence we can define a unique inverse transformation T~l : 7£(A) —>• J\f(A}~L. This transformation can be used to give our first definition of A+, the Moore-Penrose pseudoinverse of A. Unfortunately, the definition neither provides nor suggests a good computational strategy for determining A+.

- Definition 4.1. With A and T as defined above, define a transformation A+ : y —»• X by

where y = y\ + j2 with y\ e 7£(A) and yi e Tl(A}L. Then A+ is the Moore-Penrose pseudoinverse of A.

Although X and y were arbitrary vector spaces above, let us henceforth consider the case X = W1 and y = Rm. We have thus defined A+ for all A e IR™X". A purely algebraic characterization of A+ is given in the next theorem, which was proved by Penrose in 1955;

see [22].

29

![image 46](<Matrix Analysis For Scientists and Engineers_images/imageFile46.png>)

- 30 Chapter 4. Introduction to the Moore-Penrose Pseudoinverse

- Theorem 4.2. Let A e R?xn. Then G = A+ if and only if (PI) AGA = A.

- (P2) GAG = G.
- (P3) (AGf = AG.
- (P4) (GA)T = GA. Furthermore, A+ always exists and is unique.

Note that the inverse of a nonsingular matrix satisfies all four Penrose properties. Also, a right or left inverse satisfies no fewer than three of the four properties. Unfortunately, as with Definition 4.1, neither the statement of Theorem 4.2 nor its proof suggests a computational algorithm. However, the Penrose properties do offer the great virtue of providing a checkable criterion in the following sense. Given a matrix G that is a candidate for being the pseudoinverse of A, one need simply verify the four Penrose conditions (P1)-(P4). If G satisfies all four, then by uniqueness, it must be A+. Such a verification is often relatively straightforward.

- Example 4.3. Consider A = [']. Verify directly that A+ = [| f ] satisfies (P1)-(P4).

Note that other left inverses (for example, A~L = [3 — 1]) satisfy properties (PI), (P2),

and (P4) but not (P3).

Still another characterization of A+ is given in the following theorem, whose proof can be found in [1, p. 19]. While not generally suitable for computer implementation, this characterization can be useful for hand calculation of small examples.

- Theorem 4.4. Let A e R™xn. Then

4.2 Examples

Each of the following can be derived or verified by using the above definitions or characterizations.

- Example 4.5. A+ = AT(AAT)~ if A is onto (independent rows) (A is right invertible).
- Example 4.6. A+ = (AT A)~ AT if A is 1-1 (independent columns) (A is left invertible).
- Example 4.7. For any scalar a,

![image 47](<Matrix Analysis For Scientists and Engineers_images/imageFile47.png>)

- 4.3. Properties and Applications 31

- Example 4.8. For any vector v e M",
- Example 4.9.
- Example 4.10.

###### 4.3 Properties and Applications

This section presents some miscellaneous useful results on pseudoinverses. Many of these are used in the text that follows.

- Theorem 4.11. Let A e Rmx" and suppose U e Rmxm, V e Rnx" are orthogonal (M is orthogonal if MT = M-1). Then

Proof: For the proof, simply verify that the expression above does indeed satisfy each c the four Penrose conditions. D

- Theorem 4.12. Let S e Rnxn be symmetric with UTSU = D, where U is orthogonal an D is diagonal. Then S+ = UD+UT, where D+ is again a diagonal matrix whose diagonc elements are determined according to Example 4.7.

###### Theorem 4.13. For all A e Rmxn,

Proof: Both results can be proved using the limit characterization of Theorem 4.4. The proof of the first result is not particularly easy and does not even have the virtue of being especially illuminating. The interested reader can consult the proof in [1, p. 27]. The proof of the second result (which can also be proved easily by verifying the four Penrose conditions) is as follows:

![image 48](<Matrix Analysis For Scientists and Engineers_images/imageFile48.png>)

32 Chapter 4. Introduction to the Moore-Penrose Pseudoinverse

Note that by combining Theorems 4.12 and 4.13 we can, in theory at least, compute the Moore-Penrose pseudoinverse of any matrix (since A AT and AT A are symmetric). This turns out to be a poor approach in finite-precision arithmetic, however (see, e.g., [7], [11], [23]), and better methods are suggested in text that follows.

Theorem 4.11 is suggestive of a "reverse-order" property for pseudoinverses of prodnets of matrices such as exists for inverses of nroducts TTnfortnnatelv. in peneraK

As an example consider A = [0 1J and B = LI. Then

while

However, necessary and sufficient conditions under which the reverse-order property does hold are known and we quote a couple of moderately useful results for reference.

- Theorem 4.14. (AB)+ = B+A+ if and only if

Proof: For the proof, see [9]. D

- Theorem 4.15. (AB)+ = B?A+, where BI = A+AB and A) = AB\B+. Proof: For the proof, see [5]. D
- Theorem 4.16. If A e Rnrxr, B e Rrrxm, then (AB)+ = B+A+.

Proof: Since A e Rnrxr, then A+ = (ATA)~lAT, whence A+A = Ir. Similarly, since B e Wrxm, we have B+ = BT(BBT)~\ whence BB+ = Ir. The result then follows by taking BI = B, A\ = A in Theorem 4.15. D

The following theorem gives some additional useful properties of pseudoinverses.

- Theorem 4.17. For all A e Rmxn,

![image 49](<Matrix Analysis For Scientists and Engineers_images/imageFile49.png>)

Exercises 33

Note: Recall that A e R"xn is normal if AAT = AT A. For example, if A is symmetric, skew-symmetric, or orthogonal, then it is normal. However, a matrix can be none of the preceding but still be normal, such as

for scalars a, b e E.

The next theorem is fundamental to facilitating a compact and unifying approach to studying the existence of solutions of (matrix) linear equations and linear least squares problems.

- Theorem 4.18. Suppose A e Rnxp, B e EMXm. Then K(B) c U(A) if and only if AA+B = B.

Proof: Suppose K(B) c U(A) and take arbitrary jc e Rm. Then Bx e H(B) c H(A), so there exists a vector y e Rp such that Ay = Bx. Then we have

where one of the Penrose properties is used above. Since x was arbitrary, we have shown that B = AA+B.

To prove the converse, assume that AA+B = B and take arbitrary y e K(B). Then there exists a vector x e Rm such that Bx = y, whereupon

###### EXERCISES

- 1. Use Theorem 4.4 to compute the pseudoinverse of \2 21 •
- 2. If jc, y e R", show that (xyT)+ = (xTx)+(yTy)+yxT.
- 3. For A e Rmxn, prove that 7£(A) = 7£(AAr) using only definitions and elementary properties of the Moore-Penrose pseudoinverse.
- 4. For A e Rmxn, prove that ft(A+) = ft(Ar).
- 5. For A e Rpxn and 5 € Rmx", show that JV(A) C A/"(S) if and only if fiA+A = B.
- 6. Let A G M"xn, 5 e Enxm, and D € Emxm and suppose further that D is nonsingular.

- (a) Prove or disprove that
- (b) Prove or disprove that

###### This page intentionally left blank

![image 50](<Matrix Analysis For Scientists and Engineers_images/imageFile50.png>)

![image 51](<Matrix Analysis For Scientists and Engineers_images/imageFile51.png>)

- Chapter 5

###### Introduction to the Singular Value Decomposition

In this chapter we give a brief introduction to the singular value decomposition (SVD). We show that every matrix has an SVD and describe some useful properties and applications of this important matrix factorization. The SVD plays a key conceptual and computational role throughout (numerical) linear algebra and its applications.

###### 5.1 The Fundamental Theorem

- Theorem 5.1. Let A e R™xn. Then there exist orthogonal matrices U e Rmxm and V € Rnxn such that

where S = [J °0], S = diagfcri, ... ,o>) e Rrxr, and a\ > • • • > or > 0. More specifically, we have

The submatrix sizes are all determined by r (which must be < min{m, «}), i.e., U\ e Wnxr, U2 e ^x(m-r); Vi e R«xrj y2 € Rnxfo-r^ and the 0-JM^/ocJb in E are compatibly dimensioned.

Proof: Since A r A > 0 ( A r A i s symmetric and nonnegative definite; recall, for example, [24, Ch. 6]), its eigenvalues are all real and nonnegative. (Note: The rest of the proof follows analogously if we start with the observation that A AT > 0 and the details are left to the reader as an exercise.) Denote the set of eigenvalues of AT A by {of , / e n} with a\ > • • • > ar > 0 = o>+i = • • • = an. Let {u, , i e n} be a set of corresponding orthonormal eigenvectors and let V\ = [v\, ..., vr], Vi = [vr+\, ..., vn]. Letting S — diag(cri, ..., cfr), we can write ArAVi = ViS2. Premultiplying by Vf gives Vf ATAVi = VfV^S2 = S2, the latter equality following from the orthonormality of the r;, vectors. Pre- and postmultiplying by S~l eives the emotion

35

![image 52](<Matrix Analysis For Scientists and Engineers_images/imageFile52.png>)

36 Chapter 5. Introduction to the Singular Value Decomposition

Turning now to the eigenvalue equations corresponding to the eigenvalues or+\, ..., an we have that ATAV2 = V20 = 0, whence Vf ATAV2 = 0. Thus, AV2 = 0. Now define the matrix Ui e Mmx/" by U\ = AViS~l. Then from (5.4) we see that UfU\ = /; i.e., the columns of U\ are orthonormal. Choose any matrix U2 £ ^77IX(™~r) such that [U\ U2] is orthogonal. Then

since A V2 =0. Referring to the equation U\ = A V\ S l defining U\, we see that U{ AV\ = S and 1/2 AVi = U^UiS = 0. The latter equality follows from the orthogonality of the

columns of U\ andU2. Thus, we see that, in fact, UTAV = [Q Q], and defining this matrix to be S completes the proof. D

- Definition 5.2. Let A = t/E VT be an SVD of A as in Theorem 5.1.

- 1. The set [a\,..., ar} is called the set of (nonzero) singular values of the matrix A and i

is denoted £(A). From the proof of Theorem 5.1 we see that cr,(A) = A(2 (ATA) = A.? (AAT). Note that there are also min{m, n] — r zero singular values.

- 2. The columns ofU are called the left singular vectors of A (and are the orthonormal eigenvectors of AAT).
- 3. The columns of V are called the right singular vectors of A (and are the orthonormal eigenvectors of A1A).

- Remark 5.3. The analogous complex case in which A e C™x" is quite straightforward. The decomposition is A = t/E VH, where U and V are unitary and the proof is essentially identical, except for Hermitian transposes replacing transposes.
- Remark 5.4. Note that U and V can be interpreted as changes of basis in both the domain and co-domain spaces with respect to which A then has a diagonal matrix representation. Specifically, let C, denote A thought of as a linear transformation mapping W to W. Then rewriting A = U^VT as AV = U E we see that Mat £ is S with respect to the bases [v\,..., vn} for R" and {u\,..., um] for Rm (see the discussion in Section 3.2). See also

- Remark 5.16.

- Remark 5.5. The singular value decomposition is not unique. For example, an examination of the proof of Theorem 5.1 reveals that

• any orthonormal basis for jV(A) can be used for V2.

there may be nonuniqueness associated with the columns of V\ (and hence U\) corresponding to multiple cr/'s.

![image 53](<Matrix Analysis For Scientists and Engineers_images/imageFile53.png>)

- 5.1. The Fundamental Theorem 37

- • any C/2 can be used so long as [U\ Ui] is orthogonal.
- • columns of U and V can be changed (in tandem) by sign (or multiplier of the form eje in the complex case).

What is unique, however, is the matrix E and the span of the columns of U\, f/2, Vi, and ¥2 (see Theorem 5.11). Note, too, that a "full SVD" (5.2) can always be constructed from a "compact SVD" (5.3).

- Remark 5.6. Computing an SVD by working directly with the eigenproblem for AT A or AAT is numerically poor in finite-precision arithmetic. Better algorithms exist that work directly on A via a sequence of orthogonal transformations; see, e.g., [7], [11], [25].

F/vamnlp 5.7.

where U is an arbitrary 2x2 orthogonal matrix, is an SVD.

- Example 5.8.

where 0 is arbitrary, is an SVD.

- Example 5.9.

is an SVD.

- Example 5.10. Let A e RMX" be symmetric and positive definite. Let V be an orthogonal matrix of eigenvectors that diagonalizes A, i.e., VT AV = A > 0. Then A = VAVT is an SVD of A.

A factorization t/SVr ofanm x n matrix A qualifies as an SVD if U and V are orthogonal and £ is an m x n "diagonal" matrix whose diagonal elements in the upper left corner are positive (and ordered). For example, if A = f/E VT is an SVD of A, then VSrC/risanSVDof AT.

![image 54](<Matrix Analysis For Scientists and Engineers_images/imageFile54.png>)

38 Chapter 5. Introduction to the Singular Value Decomposition

###### 5.2 Some Basic Properties

- Theorem 5.11. Let A e Rmxn have a singular value decomposition A = VLVT. Using the notation of Theorem 5.1, the following properties hold:

- 1. rank(A) = r = the number of nonzero singular values of A.
- 2. Let U =. [HI, ..., um] and V = [v\, ..., vn]. Then A has the dyadic (or outer product) expansion

3. The singular vectors satisfy the relations

- Remark 5.12. Part 4 of the above theorem provides a numerically superior method for finding (orthonormal) bases for the four fundamental subspaces compared to methods based on, for example, reduction to row or column echelon form. Note that each subspace requires knowledge of the rank r. The relationship to the four fundamental subspaces is summarized nicely in Figure 5.1.
- Remark 5.13. The elegance of the dyadic decomposition (5.5) as a sum of outer products and the key vector relations (5.6) and (5.7) explain why it is conventional to write the SVD as A = UZVT rather than, say, A = UZV.

- Theorem 5.14. Let A e Emx" have a singular value decomposition A = UHVT as in TheoremS.]. Then

where

![image 55](<Matrix Analysis For Scientists and Engineers_images/imageFile55.png>)

- 5.2. Some Basic Properties 39

Figure 5.1. SVD and the four fundamental subspaces.

with the Q-subblocks appropriately sized. Furthermore, if we let the columns of U and V be as defined in Theorem 5.11, then

Proof: The proof follows easily by verifying the four Penrose conditions. D

- Remark 5.15. Note that none of the expressions above quite qualifies as an SVD of A+ if we insist that the singular values be ordered from largest to smallest. However, a simple reordering accomplishes the task:

This can also be written in matrix terms by using the so-called reverse-order identity matrix (or exchange matrix) P = \er,er^\, ..., e^, e\\, which is clearly orthogonal and symmetric.

![image 56](<Matrix Analysis For Scientists and Engineers_images/imageFile56.png>)

40 Chapters. Introduction to the Singular Value Decomposition

Then

is the matrix version of (5.11). A "full SVD" can be similarly constructed.

- Remark 5.16. Recall the linear transformation T used in the proof of Theorem 3.17 and in Definition 4.1. Since T is determined by its action on a basis, and since (v\, . . . , vr} is a basis forJ\f(A)±, then T can be defined by TV; = cr, w, , / e r. Similarly, since [u\, ... ,ur} isabasisfor7£(.4), then T~l can be defined by T^'M, = ^-u, , / e r. From Section 3.2, the

matrix representation for T with respect to the bases {v\, ..., vr} and {MI , ..., ur] is clearly S, while the matrix representation for the inverse linear transformation T~l with respect to the same bases is 5""1.

###### 5.3 Row and Column Compressions

Row compression Let A E Rmxn have an SVD given by (5.1). Then

Notice that M(A) - M(UT A) = A/"(SV,r) and the matrix SVf e Rrx" has full row rank. In other words, premultiplication of A by UT is an orthogonal transformation that "compresses" A by row transformations. Such a row compression can also be accomplished

D _

by orthogonal row transformations performed directly on A to reduce it to the form 0 , where R is upper triangular. Both compressions are analogous to the so-called row-reduced echelon form which, when derived by a Gaussian elimination algorithm implemented in finite-precision arithmetic, is not generally as reliable a procedure.

###### Column compression

Again, let A e Rmxn have an SVD given by (5.1). Then

This time, notice that H(A) = K(AV) = K(UiS) and the matrix UiS e Rmxr has full column rank. In other words, postmultiplication of A by V is an orthogonal transformation that "compresses" A by column transformations. Such a compression is analogous to the

![image 57](<Matrix Analysis For Scientists and Engineers_images/imageFile57.png>)

Exercises 41

so-called column-reduced echelon form, which is not generally a reliable procedure when performed by Gauss transformations in finite-precision arithmetic. For details, see, for example, [7], [11], [23], [25].

###### EXERCISES

- 1. Let X € Mmx". If XTX = 0, show that X = 0.
- 2. Prove Theorem 5.1 starting from the observation that AAT > 0.
- 3. Let A e E"xn be symmetric but indefinite. Determine an SVD of A.
- 4. Let x e Rm, y e Rn be nonzero vectors. Determine an SVD of the matrix A e R™ defined by A = xyT.

- 6. Let A e Rmxn and suppose W eRmxm and 7 e Rnxn are orthogonal.

(a) Show that A and W A F have the same singular values (and hence the same rank). (b) Suppose that W and Y are nonsingular but not necessarily orthogonal. Do A

and WAY have the same singular values? Do they have the same rank?

- 7. Let A € R"XM. Use the SVD to determine a polar factorization of A, i.e., A = QP where Q is orthogonal and P = PT > 0. Note: this is analogous to the polar form z = rel&ofa complex scalar z (where i = j = V^T).

- 5. Determine SVDs of the matrices

###### This page intentionally left blank

![image 58](<Matrix Analysis For Scientists and Engineers_images/imageFile58.png>)

![image 59](<Matrix Analysis For Scientists and Engineers_images/imageFile59.png>)

- Chapter 6

###### Linear Equations

In this chapter we examine existence and uniqueness of solutions of systems of linear equations. General linear systems of the form

are studied and include, as a special case, the familiar vector system

###### 6.1 Vector Linear Equations

We begin with a review of some of the principal results associated with vector linear systems.

- Theorem 6.1. Consider the system of linear equations

- 1. There exists a solution to (6.3) if and only ifbeH(A).
- 2. There exists a solution to (6.3} for all b e Rm if and only ifU(A) = W", i.e., A is onto; equivalently, there exists a solution if and only j/"rank([A, b]) = rank(A), and this is possible only ifm < n (since m = dimT^(A) = rank(A) < min{m, n}).
- 3. A solution to (6.3) is unique if and only ifJ\f(A) = 0, i.e., A is 1-1.
- 4. There exists a unique solution to (6.3) for all b e W" if and only if A is nonsingular; equivalently, A G Mmxm and A has neither a 0 singular value nor a 0 eigenvalue.
- 5. There exists at most one solution to (6.3) for all b e W1 if and only if the columns of A are linearly independent, i.e., A/"(A) = 0, and this is possible only ifm > n.
- 6. There exists a nontrivial solution to the homogeneous system Ax = 0 if and only if rank(A) < n.

43

![image 60](<Matrix Analysis For Scientists and Engineers_images/imageFile60.png>)

44 Chapter 6. Linear Equations

Proof: The proofs are straightforward and can be consulted in standard texts on linear algebra. Note that some parts of the theorem follow directly from others. For example, to prove part 6, note that x = 0 is always a solution to the homogeneous system. Therefore, we must have the case of a nonunique solution, i.e., A is not 1-1, which implies rank(A) < n by part 3. D

###### 6.2 Matrix Linear Equations

In this section we present some of the principal results concerning existence and uniqueness of solutions to the general matrix linear system (6.1). Note that the results of Theorem

- 6.1 follow from those below for the special case k = 1, while results for (6.2) follow by specializing even further to the case m = n.

- Theorem 6.2 (Existence). The matrix linear equation

has a solution if and only ifl^(B) C 7£(A); equivalently, a solution exists if and only if AA+B = B.

Proof: The subspace inclusion criterion follows essentially from the definition of the range of a matrix. The matrix criterion is Theorem 4.18.

- Theorem 6.3. Let A e Rmxn, B eRmxk and suppose that AA+B = B. Then any matrix of the form

is a solution of

Furthermore, all solutions of (6.6) are of this form. Proof: To verify that (6.5) is a solution, premultiply by A:

That all solutions arc of this form can be seen as follows. Let Z be an arbitrary solution of (6.6), i.e., AZ — B. Then we can write

and this is clearly of the form (6.5).

![image 61](<Matrix Analysis For Scientists and Engineers_images/imageFile61.png>)

- 6.2. Matrix Linear Equations 45

- Remark 6.4. When A is square and nonsingular, A+ = A"1 and so (/ — A+A) = 0. Thus, there is no "arbitrary" component, leaving only the unique solution X• = A~1B.

- Remark 6.5. It can be shown that the particular solution X = A+B is the solution of (6.6) that minimizes TrX7 X. (Tr(-) denotes the trace of a matrix; recall that TrXr X = £\ • jcj.)

- Theorem 6.6 (Uniqueness). A solution of the matrix linear equation

is unique if and only if A+A = /; equivalently, (6.7) has a unique solution if and only if

###### M(A) = 0.

Proof: The first equivalence is immediate from Theorem 6.3. The second follows by noting that A+A = / can occur only if r — n, where r = rank(A) (recall r < h). But rank(A) = n if and only if A is 1-1 or _/V(A) = 0. D

- Example 6.7. Suppose A e E"x". Find all solutions of the homogeneous system Ax — 0. Solution:

where y e R" is arbitrary. Hence, there exists a nonzero solution if and only if A+A /= I. This is equivalent to either rank (A) = r < n or A being singular. Clearly, if there exists a nonzero solution, it is not unique.

Computation: Since y is arbitrary, it is easy to see that all solutions are generated from a basis for 7£(7 — A+A). But if A has an SVD given by A = f/E VT, then it is easily checked that / - A+A = V2V2r and U(V2V^) = K(V2) = N(A).

- Example 6.8. Characterize all right inverses of a matrix A e ]Rmx"; equivalently, find all

solutions R of the equation AR = Im. Here, we write Im to emphasize the m x m identity matrix.

Solution: There exists a right inverse if and only if 7£(/m) c 7£(A) and this is equivalent to AA+Im = Im. Clearly, this can occur if and only if rank(A) = r = m (since r < m) and this is equivalent to A being onto (A+ is then a right inverse). All right inverses of A are then of the form

where Y e E"xm is arbitrary. There is a unique right inverse if and only if A+A = / (AA(A) = 0), in which case A must be invertible and R = A"1.

- Example 6.9. Consider the system of linear first-order difference equations

![image 62](<Matrix Analysis For Scientists and Engineers_images/imageFile62.png>)

46 Chapter 6. Linear Equations

with A e R"xn and fieR"xm(rc>l,ra>l). The vector Jt* in linear system theory is known as the state vector at time k while Uk is the input (control) vector. The general solution of (6.8) is given by

for k > 1. We might now ask the question: Given XQ = 0, does there exist an input sequence {uj }y~Q suc that x^ takes an arbitrary va

[Uj }kjj^ such that Xk takes an arbitrary value in W ? In linear system theory, this is a question of reachability. Since m > 1, from the fundamental Existence Theorem, Theorem 6.2, we

of reachability e m > 1, from the see that (6.8) is reachable if and only if

or, equivalently, if and only if

A related question is the following: Given an arbitrary initial vector XQ, does there exist an input sequence {"y}"~o such that xn = 0? In linear system theory, this is called controllability. Again from Theorem 6.2, we see that (6.8) is controllable if and only if

Clearly, reachability always implies controllability and, if A is nonsingular, control-

lability and reachability are equivalent. The matrices A = [ ° 1Q1 and 5 = f ^ 1 provide an example of a system that is controllable but not reachable.

The above are standard conditions with analogues for continuous-time models (i.e., linear differential equations). There are many other algebraically equivalent conditions.

- Example 6.10. We now introduce an output vector yk to the system (6.8) of Example 6.9 by appending the equation

with C e Rpxn and D € Rpxm (p > 1). We can then pose some new questions about the overall system that are dual in the system-theoretic sense to reachability and controllability. The answers are cast in terms that are dual in the linear algebra sense as well. The condition dual to reachability is called observability: When does knowledge of {"7 }"!Q and {y_/}"~o suffice to determine (uniquely) Jt0? As a dual to controllability, we have the notion of reconstructibility: When does knowledge of {wy}"~Q and {;y/}"Io suffice to determine (uniquely) xnl The fundamental duality result from linear system theory is the following:

(A, B) is reachable [controllable] if and only if(AT, BT] is observable [reconstructive].

![image 63](<Matrix Analysis For Scientists and Engineers_images/imageFile63.png>)

- 6.4 Some Useful and Interesting Inverses 47

To derive a condition for observability, notice that

Thus,

Let v denote the (known) vector on the left-hand side of (6.13) and let R denote the matrix on the right-hand side. Then, by definition, v e Tl(R), so a solution exists. By the fundamental Uniqueness Theorem, Theorem 6.6, the solution is then unique if and only if N(R) = 0, or, equivalently, if and only if

###### 6.3 A More General Matrix Linear Equation

- Theorem 6.11. Let A e Rmxn, B e Rmxq, and C e Rpxti. Then the equation

has a solution if and only if AA+BC+C = B, in which case the general solution is of the

where Y € Rn*p is arbitrary.

A compact matrix criterion for uniqueness of solutions to (6.14) requires the notion of the Kronecker product of matrices for its statement. Such a criterion (CC+ <g) A+A — I) is stated and proved in Theorem 13.27.

###### 6.4 Some Useful and Interesting Inverses

In many applications, the coefficient matrices of interest are square and nonsingular. Listed below is a small collection of useful matrix identities, particularly for block matrices, associated with matrix inverses. In these identities, A e Rnxn, B E Rnxm, C e Rmxn, and D € Emxm. Invertibility is assumed for any component or subblock whose inverse is indicated. Verification of each identity is recommended as an exercise for the reader.

![image 64](<Matrix Analysis For Scientists and Engineers_images/imageFile64.png>)

48 Chapter 6. Linear Equations

1. (A + BDCr1 = A~l - A~lB(D~l + CA~lB)~[CA~l.

This result is known as the Sherman-Morrison-Woodbury formula. It has many applications (and is frequently "rediscovered") including, for example, formulas for the inverse of a sum of matrices such as (A + D)"1 or (A"1 + D"1) . It also yields very efficient "updating" or "downdating" formulas in expressions such as

(A + JUT ) (with symmetric A e R"x" and ;c e E") that arise in optimization theory.

T — 1

Both of these matrices satisfy the matrix equation X^ = I from which it is obvious that X~l = X. Note that the positions of the / and — / blocks may be exchanged.

- where E = (D — CA B) (E is the inverse of the Schur complement of A). This result follows easily from the block LU factorization in property 16 of Section 1.4.
- where F = (A — ED C) . This result follows easily from the block UL factorization in property 17 of Section 1.4.

###### EXERCISES

- 1. As in Example 6.8, characterize all left inverses of a matrix A e Mmx".
- 2. Let A € Emx", B e Rmxk and suppose A has an SVD as in Theorem 5.1. Assuming 7Z(B) c 7£(A), characterize all solutions of the matrix linear equation

in terms of the SVD of A

![image 65](<Matrix Analysis For Scientists and Engineers_images/imageFile65.png>)

Exercises 49

- 3. Let jc, y e E" and suppose further that XTy ^ 1. Show that
- 4. Let x, y € E" and suppose further that XTy ^ 1. Show that

where c = 1/(1 — xTy).

- 5. Let A e R"x" and let A"1 have columns c\, ..., cn and individual elements y;y. Assume that x/( 7^ 0 for some / and j. Show that the matrix B — A —l—eieT: (i.e., A with — subtracted from its (zy)th element) is singular. Hint: Show that ct <= M(B).
- 6. As in Example 6.10, check directly that the condition for reconstructibility takes the form

###### This page intentionally left blank

![image 66](<Matrix Analysis For Scientists and Engineers_images/imageFile66.png>)

![image 67](<Matrix Analysis For Scientists and Engineers_images/imageFile67.png>)

- Chapter 7

###### Projections, Inner Product Spaces, and Norms

###### 7.1 Projections

Definition 7.1. Let V be a vector space with V = X 0 y. By Theorem 2.26, every v e V has a unique decomposition v = x + y with x e X and y e y. Define PX y • V —>• X c V

by

Px,y is called the (oblique) projection on X along 3^. Figure 7.1 displays the projection of v on both X and 3^ in the case V =

Figure 7.1. Oblique projections.

- Theorem 7.2. Px,y is linear and P# y — Px,y-

- Theorem 7.3. A linear transformation P is a projection if and only if it is idempotent, i.e.,

- P2 = P. Also, P is a projection if and only if I —P is a projection. Infact, Py,x — I — Px,yProof: Suppose P is a projection, say on X along y (using the notation of Definition 7.1).

51

![image 68](<Matrix Analysis For Scientists and Engineers_images/imageFile68.png>)

52 Chapter 7. Projections, Inner Product Spaces, and Norms

Let u e V be arbitrary. Then Pv = P(x + y) = Px = x. Moreover, P2v = PPv Px = x = Pv. Thus, P2 = P. Conversely, suppose P2 = P. Let X = {v e V : Pv = v} and y = {v € V : Pv = 0}. It is easy to check that X and 3^ are subspaces. We now prove that V = X 0 y. First note that tfveX, then Pv = v. If v e y, then Pv = 0. Hence if v € X n y, then v = 0. Now let u e V be arbitrary. Then v = Pv + (I - P)v. Let

- x = Pv, y = (I - P)v. Then Px = P2v = Pv = x so x e X, while Py = P(I - P}v = Pv - P2v = 0 so y e y. Thus, V = X 0 y and the projection on X along y is P. Essentially the same argument shows that / — P is the projection on y along X. D

Definition 7.4. In the special case where y = X^, PX.XL *s called an orthogonal projection and we then use the notation PX = PX,XL-

- Theorem 7.5. P e E"xn is the matrix of an orthogonal projection (onto K(P)} if and only ifP2 = p = PT.

Proof: Let P be an orthogonal projection (on X, say, along XL} and let jc, y e R" be arbitrary. Note that (/ - P)x = (I - PX,X^X = Px±,xx by Theorem 7.3. Thus, (/ - P)x e XL. Since Py e X, we have ( P y f ( I - P)x = yTPT(I - P)x = 0.

- Since x and y were arbitrary, we must have PT (I — P) = 0. Hence PT = PTP = P, with the second equality following since PTP is symmetric. Conversely, suppose P is a symmetric projection matrix and let x be arbitrary. Write x = Px + (I — P)x. Then xTPT(I - P)x = xTP(I - P}x = 0. Thus, since Px e U(P), then (/ - P)x 6 ft(P)1 and P must be an orthogonal projection. D

###### 7.1.1 The four fundamental orthogonal projections

Using the notation of Theorems 5.1 and 5.11, let A 6 Rmxn with SVD A = UT,VT = UtSVf. Then

are easily checked to be (unique) orthogonal projections onto the respective four fundamental subspaces,

![image 69](<Matrix Analysis For Scientists and Engineers_images/imageFile69.png>)

- 7.1. Projections 53

- Example 7.6. Determine the orthogonal projection of a vector v e M" on another nonzero vector w e Rn.

Solution: Think of the vector w as an element of the one-dimensional subspace IZ(w). Then the desired projection is simply

(using Example 4.8)

Moreover, the vector z that is orthogonal to w and such that v = Pv + z is given by z = PK(W)±V = (/ — PK(W))V = v — (^-^ j w. See Figure 7.2. A direct calculation shows that z and u; are, in fact, orthogonal:

Figure 7.2. Orthogonal projection on a "line."

- Example 7.7. Recall the proof of Theorem 3.11. There, {v\,..., Vk} was an orthornormal basis for a subset S of W1. An arbitrary vector x e R" was chosen and a formula for x\ appeared rather mysteriously. The expression for x\ is simply the orthogonal projection of

- x on S. Specifically,

- Example 7.8. Recall the diagram of the four fundamental subspaces. The indicated direct sum decompositions of the domain E" and co-domain Rm are given easily as follows.

Let x e W1 be an arbitrary vector. Then

![image 70](<Matrix Analysis For Scientists and Engineers_images/imageFile70.png>)

54 Chapter 7. Projections, Inner Product Spaces, and Norms

Similarly, let y e ]Rm be an arbitrary vector. Then

###### Example 7.9. Let

Then

and we can decompose the vector [2 3 4]r uniquely into the sum of a vector in A/'CA)-1 and a vector in J\f(A), respectively, as follows:

###### 7.2 Inner Product Spaces

Definition 7.10. Let V be a vector space over R. Then {•,•): V x V product if

###### is a real inner

- 1. (x, x) > Qfor all x 6V and (x,x} =0 if and only ifx = 0.
- 2. (x, y) = (y,x)forallx,y e V.
- 3. {*, cryi + ^2) = a(x, y\) + /3(jt, y^} for all jc, yi, j2 ^ V and for alia, ft e R.

- Example 7.11. Let V = R". Then {^, y} = XTy is the "usual" Euclidean inner product or dot product.
- Example 7.12. Let V = E". Then (jc, y)Q = XTQy, where Q = QT > 0 is an arbitrary n x n positive definite matrix, defines a "weighted" inner product.

- Definition 7.13. If A e Rmx", then AT e Rnxm is the unique linear transformation or map such that (x, Ay) - (ATx, y) for all x € Rm and for all y e R".

![image 71](<Matrix Analysis For Scientists and Engineers_images/imageFile71.png>)

- 7.2. Inner Product Spaces 55

It is easy to check that, with this more "abstract" definition of transpose, and if the (/, y)th element of A is a(;, then the (i, y)th element of AT is a/,. It can also be checked that all the usual properties of the transpose hold, such as (Afl) = BT AT. However, the definition above allows us to extend the concept of transpose to the case of weighted inner products in the following way. Suppose A e Rmxn and let {-, -}g and (•, -}R, with Q and

R positive definite, be weighted inner products on Rm and W, respectively. Then we can define the "weighted transpose" A# as the unique map that satisfies

(x, Ay)Q = (A#x, y)R for all x e Rm and for all y e W1.

By Example 7.12 above, we must then have XT QAy = xT(A#) Ry for all x, y. Hence we must have QA = (A#) R. Taking transposes (of the usual variety) gives AT Q = RA#. Since R is nonsingular, we find

A* = /r'A' Q.

We can also generalize the notion of orthogonality (xTy = 0) to Q -orthogonality (Q is a positive definite matrix). Two vectors x, y e W are <2-orthogonal (or conjugate with respect to Q) if (x,y}Q = XT Qy = 0. Q -orthogonality is an important tool used in studying conjugate direction methods in optimization theory.

- Definition 7.14. Let V be a vector space over C. Then {-, •} : V x V -> C is a complex inner product if

- 1. (x,x) > Qfor all x e V and (x,x) =0 if and only ifx = 0.
- 2. (x, y) = (y, x) for all x, y e V.
- 3. (x,ayi + fiy2) = a(x, y\) + fi(x, y2}forallx, y\, y2 e V and for alia, ft 6 C.

- Remark 7.15. We could use the notation {•, -}c to denote a complex inner product, but if the vectors involved are complex-valued, the complex inner product is to be understood. Note, too, from part 2 of the definition, that (x,x) must be real for all x.

- Remark 7.16. Note from parts 2 and 3 of Definition 7.14 that we have (ax\ + fix2, y) = a(x\, y) + P(x2, y}.

- Remark 7.17. The Euclidean inner product of x, y e C" is given by

The conventional definition of the complex Euclidean inner product is (x, y} = yHx but we use its complex conjugate xHy here for symmetry with the real case.

- Remark 7.18. A weighted inner product can be defined as in the real case by (x, y}Q XH Qy, for arbitrary Q = QH > 0. The notion of Q -orthogonality can be similarly generalized to the complex case.

![image 72](<Matrix Analysis For Scientists and Engineers_images/imageFile72.png>)

56 Chapter 7. Projections, Inner Product Spaces, and Norms

Definition 7.19. A vector space (V, F) endowed with a specific inner product is called an inner product space. If F = C, we call V a complex inner product space. If F = R, we call V a real inner product space.

###### Example 7.20.

- 1. Check that V = R"x" with the inner product (A, B) = Tr AT B is a real inner product space. Note that other choices are possible since by properties of the trace function, TrATB = TrBTA = TrABT = TrBAT.
- 2. Check that V = Cnx" with the inner product (A, B) = Tr AHB is a complex inner product space. Again, other choices are possible.

Definition 7.21. Let V be an inner product space. For v e V, we define the norm (or length) ofv by \\v\\ = */(v, v). This is called the norm induced by (-,-).

###### Example 7.22.

- 1. If V = E." with the usual inner product, the induced norm is given by ||i>|| =

xV—*« 9\ 7

(E,=i<Y)2-

- 2. If V = C" with the usual inner product, the induced norm is given by \\v\\ =

###### (£?=,l»,-l2)*.

- Theorem 7.23. Let P be an orthogonal projection on an inner product space V. Then \\Pv\\ < \\v\\forallv e V.

Proof: Since P is an orthogonal projection, P2 = P = P#. (Here, the notation P# denotes the unique linear transformation that satisfies (Pu,v} = (u, P#v) for all u, v e V. If this seems a little too abstract, consider V = R" (or C"), where P# is simply the usual PT (or PH)). Hence (Pv, v) = (P2v, v) = (Pv, P#v) = (Pv, Pv) = \\Pv\\2 > 0. Now / - P is

also a projection, so the above result applies and we get

from which the theorem follows. Definition 7.24. The norm induced on an inner product space by the "usual" inner product is called the natural norm.

In case V = C" or V = R", the natural norm is also called the Euclidean norm. In the next section, other norms on these vector spaces are defined. A converse to the above procedure is also available. That is, given a norm defined by \\x\\ — •>/(•*> x), an inner product can be defined via the following.

![image 73](<Matrix Analysis For Scientists and Engineers_images/imageFile73.png>)

- 7.3. Vector Norms 57

###### Theorem 7.25 (Polarization Identity).

1. For x, y € R", an inner product is defined by

2. For x, y e C", an inner product is defined by

where j = i = \/—T.

###### 7.3 Vector Norms

Definition 7.26. Let (V, F) be a vector space. Then \\-\\ : V ->• R is a vector norm if it satisfies the following three properties:

(This is called the triangle inequality, as seen readily from the usual diagram illus trating the sum of two vectors in R2.)

- Remark 7.27. It is convenient in the remainder of this section to state results for complexvalued vectors. The specialization to the real case is obvious.

Definition 7.28. A vector space (V, F) is said to be a normed linear space if and only if there exists a vector norm || • || : V -> R satisfying the three conditions of Definition 7.26.

###### Example 7.29.

1. For x e C", the Holder norms, or p-norms, are defined by

Special cases:

(The second equality is a theorem that requires proof.)

![image 74](<Matrix Analysis For Scientists and Engineers_images/imageFile74.png>)

58 Chapter 7. Projections, Inner Product Spaces, and Norms

- 2. Some weighted p-norms:

- (a) ||JC||,.D = E^rf/l*/!, where 4 > 0.
- (b) Ikllz.g — (xh QXY > where Q = QH > 0 (this norm is more commonly denoted || • ||c).

- 3. On the vector space (C[to, t\], R), define the vector norm

On the vector space ((C[to, t\])n, R), define the vector norm

###### Fhcorem 7.30 (Holder Inequality). Let x, y e C". Ther,

A particular case of the Holder inequality is of special interest.

###### Theorem 7.31 (Cauchy-Bunyakovsky-Schwarz Inequality). Let x, y e C". Then

with equality if and only if x and y are linearly dependent.

Proof: Consider the matrix [x y] e C"x2. Since

is a nonnegative definite matrix, its determinant must be nonnegative. In other words, 0 < (xHx)(yHy) — (xHy)(yHx). Since yHx = xHy, we see immediately that \XHy\ <

\\X\\2\\y\\2- D

Note: This is not the classical algebraic proof of the Cauchy-Bunyakovsky-Schwarz (C-B-S) inequality (see, e.g., [20, p. 217]). However, it is particularly easy to remember.

- Remark 7.32. The angle 0 between two nonzero vectors x, y e C" may be defined by

cos# = Il-MmlylbI, „ |.^|| , 0 < 0 —< 5-.^ The C-B-S inequality is thus equivalent to the statement

| COS 0 | < 1.

- Remark 7.33. Theorem 7.31 and Remark 7.32 are true for general inner product spaces.
- Remark 7.34. The norm || • ||2 is unitarily invariant, i.e., if U € C"x" is unitary, then \\Ux\\2 = \\x\\2 (Proof. \\Ux\\l = xHUHUx = XHX = \\x\\\). However, || - ||, and || - 1^

![image 75](<Matrix Analysis For Scientists and Engineers_images/imageFile75.png>)

- 7.4. Matrix Norms 59

are not unitarily invariant. Similar remarks apply to the unitary invariance of norms of real vectors under orthogonal transformation.

- Remark 7.35. If x, y € C" are orthogonal, then we have the Pythagorean Identity

the proof of which follows easily from ||z||22 =_ z_//.z. Theorem 7.36. All norms on C" are equivalent; i.e., there exist constants c\, c-i (possibly depending onn) such that

Example 7.37. For x G C", the following inequalities are all tight bounds; i.e., there exist vectors x for which equality holds:

Finally, we conclude this section with a theorem about convergence of vectors. Convergence of a sequence of vectors to some limit vector can be converted into a statement about convergence of real numbers, i.e., convergence in terms of vector norms.

- Theorem 7.38. Let \\ • \\ be a vector norm and suppose v, i»(1), v(2\ ... e C". Then

###### 7.4 Matrix Norms

In this section we introduce the concept of matrix norm. As with vectors, the motivation for using matrix norms is to have a notion of either the size of or the nearness of matrices. The former notion is useful for perturbation analysis, while the latter is needed to make sense of "convergence" of matrices. Attention is confined to the vector space (Wnxn, R) since that is what arises in the majority of applications. Extension to the complex case is straightforward and essentially obvious.

Definition 7.39. || • || : Rmx" -> E is a matrix norm if it satisfies the following three properties:

![image 76](<Matrix Analysis For Scientists and Engineers_images/imageFile76.png>)

60 Chapter 7. Projections, Inner Product Spaces, and Norms

- Example 7.40. Let A e Rmx". Then the Frobenius norm (or matrix Euclidean norm) is defined by

^wncic r = laiiK^/i;;.

- Example 7.41. Let A e Rmxn. Then the matrix p-norms are defined by

The following three special cases are important because they are "computable." Each is a theorem and requires a proof.

- 1. The "maximum column sum" norm is
- 2. The "maximum row sum" norm is
- 3. The spectral norm is

- Example 7.42. Let A E Rmxn. The Schatten/7-norms are defined by

Some special cases of Schatten /?-norms are equal to norms defined previously. For example, || . ||52 = || . \\F and || • ||5i00 = || • ||2. The norm || • ||5>1 is often called the trace norm.

- Example 7.43. Let A e Kmx". Then "mixed" norms can also be defined by
- Example 7.44. The "matrix analogue of the vector 1-norm," || A\\s = ^ j \ai}; |, is a norm.

The concept of a matrix norm alone is not altogether useful since it does not allow us to estimate the size of a matrix product A B in terms of the sizes of A and B individually.

![image 77](<Matrix Analysis For Scientists and Engineers_images/imageFile77.png>)

- 7.4. Matrix Norms 61

Notice that this difficulty did not arise for vectors, although there are analogues for, e.g., inner products or outer products of vectors. We thus need the following definition.

Definition 7.45. Let A e Rmxn, B e Rnxk. Then the norms \\ • \\a, \\ • \\p, and \\ • \\y are mutually consistent if \\ A B \\a < \\A\\p\\B\\y. A matrix norm \\ • \\ is said to be consistent if \\AB\\ < || A || || fi|| whenever the matrix product is defined.

###### Example 7.46.

- 1. || • ||/7 and || • ||p for all p are consistent matrix norms.
- 2. The "mixed" norm

is a matrix norm but it is not consistent. For example, take A = B = \ \ J1. Then ||Afl||li00 = 2while||A||li00||B||1>00 = l.

###### The p -norms are examples of matrix norms that are subordinate to (or induced by) a vector norm, i.e.,

(or, more generally, ||A|| = max^o 11^4^11., ..p). For such subordinate norms, also called operator norms, we clearly have ||Ajc|| < ||A||1|jt||. Since ||Afijc|| < ||A||||fljc|| < ||A||||fl||||jt||, it follows that all subordinate norms are consistent.

- Theorem 7.47. There exists a vector x* such that ||Ajt*|| = ||A|| ||jc*|| if the matrix norm is subordinate to the vector norm.
- Theorem 7.48. If \\ • \\m is a consistent matrix norm, there exists a vector norm \\ • \\v consistent with it, i.e.,HAjcJI^ < \\A\\m \\x\\v.

Not every consistent matrix norm is subordinate to a vector norm. For example, consider || • \\F. Then||A^||2 < ||A||F||jc||2, so || • ||2 is consistent with || • ||F, but there does not exist a vector norm || • || such that ||A||F is given by max^o \^ •

###### Useful Results

The following miscellaneous results about matrix norms are collected for future reference. The interested reader is invited to prove each of them as an exercise.

2. For A e R"x", the following inequalities are all tight, i.e., there exist matrices A for which equality holds:

![image 78](<Matrix Analysis For Scientists and Engineers_images/imageFile78.png>)

62 Chapter 7. Projections, Inner Product Spaces, and Norms

- 3. For A eRmxa.
- 4. The norms || • \\F and || • ||2 (as well as all the Schatten /?-norms, but not necessarily other p-norms) are unitarily invariant; i.e., for all A e Rmx" and for all orthogonal matrices Q zRmxm and Z e M"x", ||(MZ||a = ||A||afora = 2 or F.

###### Convergence

The following theorem uses matrix norms to convert a statement about convergence of a sequence of matrices into a statement about the convergence of an associated sequence of scalars.

- Theorem 7.49. Let \\ -\\bea matrix norm and suppose A, A(1), A(2), ... e Rmx". Then

###### EXERCISES

- 1. If P is an orthogonal projection, prove that P+ = P.
- 2. Suppose P and Q are orthogonal projections and P + Q = I. Prove that P — Q must be an orthogonal matrix.
- 3. Prove that / — A+A is an orthogonal projection. Also, prove directly that V2 V/ is an orthogonal projection, where ¥2 is defined as in Theorem 5.1.
- 4. Suppose that a matrix A e Wnxn has linearly independent columns. Prove that the orthogonal projection onto the space spanned by these column vectors is given by the matrix P = A(ATA)~}AT.
- 5. Find the (orthogonal) projection of the vector [2 3 4]r onto the subspace of R3 spanned by the plane 3;c — v + 2z = 0.
- 6. Prove that E"x" with the inner product (A, B) = Tr ATB is a real inner product space.
- 7. Show that the matrix norms || • ||2 and || • \\F are unitarily invariant.
- 8. Definition: Let A e Rnxn and denote its set of eigenvalues (not necessarily distinct) by {A-i ,...,>.„}. The spectral radius of A is the scalar

![image 79](<Matrix Analysis For Scientists and Engineers_images/imageFile79.png>)

Exercises 63

###### Let

Determine ||A||F, \\A\\lt ||A||2, HA^, and p(A).

9. Let

Determine ||A||F, HAId, ||A||2, HAH^, and p(A). (An n x n matrix, all of whose columns and rows as well as main diagonal and antidiagonal sum to s = n(n2 + l)/2, is called a "magic square" matrix. If M is a magic square matrix, it can be proved that || M Up = s for all/?.)

10. Let A = xyT, where both x, y e R" are nonzero. Determine ||A||F, ||A||j, ||A||2, and ||A||oo in terms of \\x\\a and/or \\y\\p, where a and ft take the value 1, 2, or oo as appropriate.

###### This page intentionally left blank

![image 80](<Matrix Analysis For Scientists and Engineers_images/imageFile80.png>)

![image 81](<Matrix Analysis For Scientists and Engineers_images/imageFile81.png>)

- Chapter 8

###### Linear Least Squares Problems

###### 8.1 The Linear Least Squares Problem

Problem: Suppose A e Rmx" with m > n and b <= Rm is a given vector. The linear least squares problem consists of finding an element of the set

Solution: The set X has a number of easily verified properties:

- 1. A vector x e X if and only if ATr = 0, where r = b — Ax is the residual associated with x. The equations ATr — 0 can be rewritten in the form ATAx = ATb and the latter form is commonly known as the normal equations, i.e., x e X if and only if x is a solution of the normal equations. For further details, see Section 8.2.
- 2. A vector x E X if and onlv if x is of the form

To see why this must be so, write the residual r in the form

Now, (Pn(A)b — AJC) is clearly in 7£(A), while

so these two vectors are orthogonal. Hence,

from the Pythagorean identity (Remark 7.35). Thus, ||A.x — b\\\ (and hence p(x) = \\Ax —b\\2) assumes its minimum value if and only if

65

![image 82](<Matrix Analysis For Scientists and Engineers_images/imageFile82.png>)

66 Chapter 8. Linear Least Squares Problems

and this equation always has a solution since AA+b e 7£(A). By Theorem 6.3, all solutions of (8.2) are of the form

where y e W is arbitrary. The minimum value of p(x) is then clearly equal to

the last inequality following by Theorem 7.23.

- 3. X is convex. To see why, consider two arbitrary vectors jci = A+b + (I — A+A)y and *2 = A+b + (I — A+A)z in X. Let 6 e [0, 1]. Then the convex combination 0*i + (1 - #)*2 = A+b + (I - A+A)(Oy + (1 - 0)z) is clearly in X.
- 4. X has a unique element x* of minimal 2-norm. In fact, x* = A+b is the unique vector that solves this "double minimization" problem, i.e., x* minimizes the residual p(x) and is the vector of minimum 2-norm that does so. This follows immediately from convexity or directly from the fact that all x e X are of the form (8.1) and

which follows since the two vectors are orthogonal.

- 5. There is a unique solution to the least squares problem, i.e., X = {x*} = {A+b}, if and only if A+A = I or, equivalently, if and only if rank (A) = n.

Just as for the solution of linear equations, we can generalize the linear least squares problem to the matrix case.

- Theorem 8.1. Let A e Emx" and B € Rmxk. The general solution to

is of the form

where Y € R"xfc is arbitrary. The unique solution of minimum 2-norm or F-norm is

X = A+B.

- Remark 8.2. Notice that solutions of the linear least squares problem look exactly the same as solutions of the linear system AX = B. The only difference is that in the case of linear least squares solutions, there is no "existence condition" such as K(B) c 7£(A). If the existence condition happens to be satisfied, then equality holds and the least squares

![image 83](<Matrix Analysis For Scientists and Engineers_images/imageFile83.png>)

- 8.3 Linear Regression and Other Linear Least Squares Problems 67

residual is 0. Of all solutions that give a residual of 0, the unique solution X = A+B has minimum 2-norm or F-norm.

- Remark 8.3. If we take B = Im in Theorem 8.1, then X = A+ can be interpreted as saying that the Moore-Penrose pseudoinverse of A is the best (in the matrix 2-norm sense) matrix such that AX approximates the identity.

- Remark 8.4. Many other interesting and useful approximation results are available for the matrix 2-norm (and F-norm). One such is the following. Let A e M™x" with SVD

Then a best rank k approximation to A for l < f c < r , i . e . , a solution to

is given by

The special case in which m = n and k = n — 1 gives a nearest singular matrix to A e

###### 8.2 Geometric Solution

Looking at the schematic provided in Figure 8.1, it is apparent that minimizing || Ax — b\\2 is equivalent to finding the vector x e W1 for which p — Ax is closest to b (in the Euclidean norm sense). Clearly, r = b — Ax must be orthogonal to 7£(A). Thus, if Ay is an arbitrary vector in 7£(A) (i.e., y is arbitrary), we must have

- Since y is arbitrary, we must have ATb — ATAx = 0 or ArA;c = ATb. Special case: If A is full (column) rank, then x = (AT A) ATb.

###### 8.3 Linear Regression and Other Linear Least Squares Problems

###### 8.3.1 Example: Linear regression

Suppose we have m measurements (t\,y\), ..., (tm,ym) for which we hypothesize a linear (affine) relationship

![image 84](<Matrix Analysis For Scientists and Engineers_images/imageFile84.png>)

68 Chapter 8. Linear Least Squares Problems

Figure 8.1. Projection of b on K(A).

for certain constants a. and ft. One way to solve this problem is to find the line that best fits the data in the least squares sense; i.e., with the model (8.3), we have

where &\,..., 8m are "errors" and we wish to minimize 8\ + • • • + 8^- Geometrically, we are trying to find the best line that minimizes the (sum of squares of the) distances from the given data points. See, for example, Figure 8.2.

Figure 8.2. Simple linear regression.

Note that distances are measured in the vertical sense from the points to the line (as indicated, for example, for the point (t\, y\}}. However, other criteria arc possible. For example, one could measure the distances in the horizontal sense, or the perpendicular distance from the points to the line could be used. The latter is called total least squares. Instead of 2-norms, one could also use 1-norms or oo-norms. The latter two are computationally

![image 85](<Matrix Analysis For Scientists and Engineers_images/imageFile85.png>)

- 8.3. Linear Regression and Other Linear Least Squares Problems 69

much more difficult to handle, and thus we present only the more tractable 2-norm case in text that follows.

The ra "error equations" can be written in matrix form as

where

We then want to solve the problem

or, equivalently,

Solution: x — [^1 is a solution of the normal equations ATAx = ATy where, for the special form of the matrices above, we have

and

The solution for the parameters a and ft can then be written

- 8.3.2 Other least squares problems Suppose the hypothesized model is not the linear equation (8.3) but rather is of the form

y = f ( t ) = Cl0!(0 + • • • 4- cn<t>n(t). (8.5)

In (8.5) the </>,(0 are given (basis) functions and the c; are constants to be determined to minimize the least squares error. The matrix problem is still (8.4), where we now have

An important special case of (8.5) is least squares polynomial approximation, which corresponds to choosing 0,• (?) = t'~l, i; e n, although this choice can lead to computational

![image 86](<Matrix Analysis For Scientists and Engineers_images/imageFile86.png>)

70 Chapter 8. Linear Least Squares Problems

difficulties because of numerical ill conditioning for large n. Numerically better approaches are based on orthogonal polynomials, piecewise polynomial functions, splines, etc.

The key feature in (8.5) is that the coefficients c, appear linearly. The basis functions </>,- can be arbitrarily nonlinear. Sometimes a problem in which the c, 's appear nonlinearly can be converted into a linear problem. For example, if the fitting function is of the form

- y = f ( t ) = c\eC2i, then taking logarithms yields the equation logy = logci + cjt. Then defining y — logy, c\ = logci, and GI = cj_ results in a standard linear least squares problem.

###### 8.4 Least Squares and Singular Value Decomposition

In the numerical linear algebra literature (e.g., [4], [7], [11], [23]), it is shown that solution of linear least squares problems via the normal equations can be a very poor numerical method in finite-precision arithmetic. Since the standard Kalman filter essentially amounts to sequential updating of normal equations, it can be expected to exhibit such poor numerical behavior in practice (and it does). Better numerical methods are based on algorithms that work directly and solely on A itself rather than AT A. Two basic classes of algorithms are based on S VD and QR (orthogonal-upper triangular) factorization, respectively. The former is much more expensive but is generally more reliable and offers considerable theoretical insight.

In this section we investigate solution of the linear least squares problem

via the SVD. Specifically, we assume that A has an SVD given by A = UT, VT = U\SVf as in Theorem 5.1. We now note that

The last equality follows from the fact that if v = [£ ], then ||u||^ = ||i>i \\\ + \\vi\\\ (note that orthogonality is not what is used here; the subvectors can have different lengths). This explains why it is convenient to work above with the square of the norm rather than the norm. As far as the minimization is concerned, the two are equivalent. In fact, the last quantity above is clearly minimized by taking z\ = S~lc\. The subvector z2 is arbitrary, while the minimum value of \\Ax — b\\^ is l^llr

![image 87](<Matrix Analysis For Scientists and Engineers_images/imageFile87.png>)

- 8.5. Least Squares and QR Factorization 71

Now transform back to the original coordinates:

The last equality follows from

Note that since 12 is arbitrary, V2z2 is an arbitrary vector in 7Z(V2) = A/"(A). Thus, x has been written in the form x = A+b + (/ — A+A)_y, where y e Rm is arbitrary. This agrees, of course, with (8.1).

The minimum value of the least squares residual is

and we clearly have that minimum least squares residual is 0 -4=> b is orthogonal to all vectors in U2

•<=^ b is orthogonal to all vectors in 7l(A}L

Another expression for the minimum residual is || (/ — AA+)b||2. This follows easily since ||(7 - AA+)b\\22 - \\U2Ufb\\l = bTU2U^U2UJb = bTU2U*b = \\U?b\\22.

Finally, an important special case of the linear least squares problem is the so-called full-rank problem, i.e., A e 1R™X". In this case the SVD of A is given by A = UZVT = [U{ t/2][o]^ir> and there is thus "no V2 part" to the solution.

###### 8.5 Least Squares and QR Factorization

In this section, we again look at the solution of the linear least squares problem (8.6) but this time in terms of the QR factorization. This matrix factorization is much cheaper to compute than an SVD and, with appropriate numerical enhancements, can be quite reliable.

To simplify the exposition, we add the simplifying assumption that A has full column rank, i.e., A e R™XM. It is then possible, via a sequence of so-called Householder or Givens transformations, to reduce A in the following way. A finite sequence of simple orthogonal row transformations (of Householder or Givens type) can be performed on A to reduce it to triangular form. If we label the product of such orthogonal row transformations as the orthogonal matrix QT € Rmxm, we have

![image 88](<Matrix Analysis For Scientists and Engineers_images/imageFile88.png>)

72 Chapter 8. Linear Least Squares Problems

where R e M£x" is upper triangular. Now write Q = [Q\ Q2], where Q\ e Rmx" and

- Q2 € K"IX(m~"). Both Q\ and <22 have orthonormal columns. Multiplying through by Q in (8.7), we see that

Any of (8.7), (8.8), or (8.9) are variously referred to as QR factorizations of A. Note that (8.9) is essentially what is accomplished by the Gram-Schmidt process, i.e., by writing AR~l = Q\ we see that a "triangular" linear combination (given by the coefficients of R~l) of the columns of A yields the orthonormal columns of Q\.

Now note that

The last quantity above is clearly minimized by taking x = R lc\ and the minimum residual is \\C2\\2- Equivalently, we have x = R~lQ\b = A+b and the minimum residual is IIC?^!^-

###### EXERCISES

- 1. For A € Wxn, b e Em, and any y e R", check directly that (I - A+A)y and A+b are orthogonal vectors.
- 2. Consider the following set of measurements (*,, yt):

- (a) Find the best (in the 2-norm sense) line of the form y = ax + ft that fits this data.
- (b) Find the best (in the 2-norm sense) line of the form jc = ay + (3 that fits this data.

- 3. Suppose qi and q2 are two orthonormal vectors and b is a fixed vector, all in R".

- (a) Find the optimal linear combination aq^ + fiq2 that is closest to b (in the 2-norm sense).
- (b) Let r denote the "error vector" b — ctq\ — flq2- Show that r is orthogonal to both^i and q2.

![image 89](<Matrix Analysis For Scientists and Engineers_images/imageFile89.png>)

Exercises 73

- 4. Find all solutions of the linear least squares problem
- 5. Consider the problem of finding the minimum 2-norm solution of the linear least «rmarp« nrr»h1<=>m

- (a) Consider a perturbation E\ = [0 pi of A, where 8 is a small positive number. Solve the perturbed version of the above problem,

where AI = A + E\. What happens to ||jt* — y ||2 as 8 approaches 0?

- (b) Now consider the perturbation EI = \0 s~\ of A, where again 8 is a small positive number. Solve the perturbed problem

where A2 — A + E2. What happens to \\x* — z||2 as 8 approaches 0?

- 6. Use the four Penrose conditions and the fact that Q\ has orthonormal columns to verify that if A e R™x" can be factored in the form (8.9), then A+ = R~l Q\.

1. Let A e R"x", not necessarily nonsingular, and suppose A = QR, where Q is orthogonal. Prove that A+ = R+QT.

###### This page intentionally left blank

![image 90](<Matrix Analysis For Scientists and Engineers_images/imageFile90.png>)

![image 91](<Matrix Analysis For Scientists and Engineers_images/imageFile91.png>)

- Chapter 9

###### Eigenvalues and Eigenvectors

###### 9.1 Fundamental Definitions and Properties

- Definition 9.1. A nonzero vector x e C" is a right eigenvector of A e Cnxn if there exists a scalar A. e C, called an eigenvalue, such that

Similarly, a nonzero vector y e C" is a left eigenvector corresponding to an eigenvalue

a if

By taking Hermitian transposes in (9.1), we see immediately that XH is a left eigenvector of AH associated with A. Note that if x [y] is a right [left] eigenvector of A, then so is ax [ay] for any nonzero scalar a E C. One often-used scaling for an eigenvector is a — \j'||;t|| so that the scaled eigenvector has norm 1. The 2-norm is the most common norm used for such scaling.

- Definition 9.2. The polynomial n (A.) = det(A—A,/) is called the characteristic polynomial of A. (Note that the characteristic polynomial can also be defined as det(A./ — A). This results in at most a change of sign and, as a matter of convenience, we use both forms throughout the text.}

The following classical theorem can be very useful in hand calculation. It can be proved easily from the Jordan canonical form to be discussed in the text to follow (see, for example, [21]) or directly using elementary properties of inverses and determinants (see, for example, [3]).

###### Theorem 9.3 (Cayley-Hamilton). For any A e Cnxn, n(A) = 0.

Example 9.4. Let A = [~g ~g]. Then n(k) = X2 + 2A, — 3. It is an easy exercise to verify that n(A) = A2 + 2A - 31 = 0.

It can be proved from elementary properties of determinants that if A e C"x", then 7t (X) is a polynomial of degree n. Thus, the Fundamental Theorem of Algebra says that

75

![image 92](<Matrix Analysis For Scientists and Engineers_images/imageFile92.png>)

76 Chapter 9. Eigenvalues and Eigenvectors

7r(A) has n roots, possibly repeated. These roots, as solutions of the determinant equation

are the eigenvalues of A and imply the singularity of the matrix A — XI, and hence further guarantee the existence of corresponding nonzero eigenvectors.

Definition 9.5. The spectrum of A e C"x" is the set of all eigenvalues of A, i.e., the set of all roots of its characteristic polynomial n(X). The spectrum of A is denoted A (A).

Let the eigenvalues of A e C"x" be denoted X\,..., Xn. Then if we write (9.3) in the form

and set X = 0 in this identity, we get the interesting fact that del (A) = AI • A.2 • • • AM (see also Theorem 9.25).

If A e Wxn, then n(X) has real coefficients. Hence the roots of 7r(A), i.e., the eigenvalues of A, must occur in complex conjugate pairs. Example 9.6. Let a, ft e R and let A = [ _^ £ ]. Then jr(A.) = A.2 - 2aA + a2 + ft2 and A has eigenvalues a ± fij (where j = i = •>/—!)•

If A € R"x", then there is an easily checked relationship between the left and right eigenvectors of A and AT (take Hermitian transposes of both sides of (9.2)). Specifically, if

- y is a left eigenvector of A corresponding to A e A(A), then y is a right eigenvector of AT corresponding to A. € A (A). Note, too, that by elementary properties of the determinant, we always have A(A) = A(Ar), but that A(A) = A(A) only if A e R"x".

- Definition 9.7. IfX is a root of multiplicity m ofjr(X), we say that X is an eigenvalue of A of algebraic multiplicity m. The geometric multiplicity ofX is the number of associated independent eigenvectors = n — rank(A — A/) = dim J\f(A — XI).

If A € A(A) has algebraic multiplicity m, then 1 < dimA/"(A — A/) < m. Thus, if we denote the geometric multiplicity of A by g, then we must have 1 < g < m.

- Definition 9.8. A matrix A e Wx" is said to be defective if it has an eigenvalue whose geometric multiplicity is not equal to (i.e., less than) its algebraic multiplicity. Equivalently, A is said to be defective if it does not have n linearly independent (right or left) eigenvectors.

From the Cayley-Hamilton Theorem, we know that n(A) = 0. However, it is possible for A to satisfy a lower-order polynomial. For example, if A = \1Q ®], then A sat-

isfiesa - n(1=—o.I)2 = 0. Butitalsoclearlysatisfies thesmallerdegree polynomialequation

Definition 5.5. The minimal polynomial of A G K""" is the polynomial o/(X) of least degree such that a (A) =0.

It can be shown that or(l) is essentially unique (unique if we force the coefficient of the highest power of A to be +1, say; such a polynomial is said to be monic and we generally write et (A) as a monic polynomial throughout the text). Moreover, it can also be

![image 93](<Matrix Analysis For Scientists and Engineers_images/imageFile93.png>)

- 9.1. Fundamental Definitions and Properties 77

shown that a (A.) divides every nonzero polynomial fi(k} for which ft (A) = 0. In particular, a(X) divides n(X).

There is an algorithm to determine or (A.) directly (without knowing eigenvalues and associated eigenvector structure). Unfortunately, this algorithm, called the Bezout algorithm, is numerically unstable.

Example 9.10. The above definitions are illustrated below for a series of matrices, each of which has an eigenvalue 2 of algebraic multiplicity 4, i.e., 7r(A) = (A — 2)4. We denote the geometric multiplicity by g.

At this point, one might speculate that g plus the degree of a must always be five. Unfortunately, such is not the case. The matrix

- Theorem 9.11. Let A e C«x" ana [et A., be an eigenvalue of A with corresponding right eigenvectorjc,-. Furthermore, let yj be a left eigenvector corresponding to any A; e A (A) such that Xj =£ A.,. Then yfx{ = 0. Proof: Since Axt = A,*,,

![image 94](<Matrix Analysis For Scientists and Engineers_images/imageFile94.png>)

78 Chapter 9. Eigenvalues and Eigenvectors

Similarly, since y" A = Xjyf,

Subtracting (9.6) from (9.5), we find 0 = (A.,- — Ay)j^jc,. Since A,,- — A.7- ^ 0, we must have yfxt =0.

The proof of Theorem 9.11 is very similar to two other fundamental and important results.

- Theorem 9.12. Let A e C"x" be Hermitian, i.e., A = AH. Then all eigenvalues of A must be real. Proof: Suppose (A., x) is an arbitrary eigenvalue/eigenvector pair such that Ax = A.JC. Then

Taking Hermitian transposes in (9.7) yields

Using the fact that A is Hermitian, we have that XxHx = XxHx. However, since x is an eigenvector, we have XHX /= 0, from which we conclude A. = A, i.e., A. is real. D

- Theorem 9.13. Let A e C"x" be Hermitian and suppose X and /JL are distinct eigenvalues of A with corresponding right eigenvectors x and z, respectively. Then x and z must be orthogonal.

Proof: Premultiply the equation Ax = A.JC by ZH to get ZH Ax = XzHx. Take the Hermitian transpose of this equation and use the facts that A is Hermitian and A. is real to get XH Az = XxHz. Premultiply the equation Az = i^z by XH to get XHAz = /^XHZ = XxHz. Since A, ^ /z, we must have that XHz = 0, i.e., the two vectors must be orthogonal. D

Let us now return to the general case.

- Theorem 9.14. Let A €. Cnxn have distinct eigenvalues A,1?..., A.n with corresponding right eigenvectors x\,... ,xn. Then [x\,..., xn} is a linearly independent set. The same result holds for the corresponding left eigenvectors. Proof: For the proof see, for example, [21, p. 118].

If A e Cnx" has distinct eigenvalues, and if A., e A(A), then by Theorem 9.11, jc, is orthogonal to all yj's for which j ^ i. However, it cannot be the case that yf*xt = 0 as well, or else xf would be orthogonal to n linearly independent vectors (by Theorem 9.14) and would thus have to be 0, contradicting the fact that it is an eigenvector. Since yf*Xi ^ 0 for each i, we can choose the normalization of the *, 's, or the y, 's, or both, so that ytHx; = 1

for/ € n.

![image 95](<Matrix Analysis For Scientists and Engineers_images/imageFile95.png>)

- 9.1. Fundamental Definitions and Properties 79

- Theorem 9.15. Let A e C"x" have distinct eigenvalues A.I , ..., A.n and let the corresponding right eigenvectors form a matrix X = [x\, ..., xn]. Similarly, let Y — [y\, ..., yn] be the matrix of corresponding left eigenvectors. Furthermore, suppose that the left and right eigenvectors have been normalized so that yf1 Xi = 1, / en. Finally, let A = diag(A,j, ..., Xn) e Wtxn. Then AJC, = A.,-*/, / e n, can be written in matrix form as

while y^Xj = 5,;, / en, y' e n, is expressed by the equation

These matrix equations can be combined to yield the following matrix factorizations:

and

###### Example 9.16. Let

Then n(X) = det(A - A./) = -(A.3 + 4A.2 + 9 A. + 10) = -(A. + 2)(A.2 + 2A, + 5), from which we find A (A) = {—2, — 1 ± 2j}. We can now find the right and left eigenvectors corresponding to these eigenvalues.

For A-i = —2, solve the 3 x 3 linear system (A — (—2}I)x\ = 0 to get

Note that one component of ;ci can be set arbitrarily, and this then determines the other two (since dimA/XA — (—2)7) = 1). To get the corresponding left eigenvector y\, solve the linear system y\(A + 21) = 0 to get

This time we have chosen the arbitrary scale factor for y\ so that yfx\ = 1. For A2 = — 1 + 2j, solve the linear system (A — (—1 + 2j)I)x2 = 0 to get

![image 96](<Matrix Analysis For Scientists and Engineers_images/imageFile96.png>)

80 Chapter 9. Eigenvalues and Eigenvectors

Solve the linear system y" (A — (-1 + 27')/) = 0 and normalize y>2 so that y"x2 = 1 to get

For XT, = — 1 — 2j, we could proceed to solve linear systems as for A.2. However, we can also note that x$ =x2' and yi = jj. To see this, use the fact that A, 3 = A.2 and simply conjugate the equation A;c2 — ^.2*2 to get Ax^ = ^2X2- A similar argument yields the result for left eigenvectors.

Now define the matrix X of right eigenvectors:

It is then easy to verify that

Other results in Theorem 9.15 can also be verified. For example,

Finally, note that we could have solved directly only for *i and x2 (and XT, = x2). Then, instead of determining the j,'s directly, we could have found them instead by computing X~l and reading off its rows.

###### Example 9.17. Let

Then 7r(A.) = det(A - A./) = -(A3 + 8A2 + 19X + 12) = -(A. + 1)(A. + 3)(A, + 4), from which we find A (A) = {—1, —3, —4}. Proceeding as in the previous example, it is straightforward to compute

and

![image 97](<Matrix Analysis For Scientists and Engineers_images/imageFile97.png>)

- 9.1. Fundamental Definitions and Properties 81

We also have X~l AX = A = diag(—1, —3, —4), which is equivalent to the dyadic expansion

- Theorem 9.18. Eigenvalues (but not eigenvectors) are invariant under a similarity transformation T.

Proof: Suppose (A, jc) is an eigenvalue/eigenvector pair such that Ax = Xx. Then, since T is nonsingular, we have the equivalent statement (T~lAT)(T~lx) = X(T~lx), from which the theorem statement follows. For left eigenvectors we have a similar statement, namely yHA = XyH ifandon\yif(THy)H(T~1AT) =X(THyf. D

- Remark 9.19. If / is an analytic function (e.g., f ( x ) is a polynomial, or ex, or sin*, or, in general, representable by a power series X^^ofln*n)> then it is easy to show that the eigenvalues of /(A) (defined as X^o^-A") are /(A), but /(A) does not necessarily have all the same eigenvectors (unless, say, A is diagonalizable). For example, A = T0 Oj

has only one right eigenvector corresponding to the eigenvalue 0, but A2 = f0 01 has two independent right eigenvectors associated with the eigenvalue 0. What is true is that the eigenvalue/eigenvector pair (A, x) maps to (/(A), x) but not conversely.

The following theorem is useful when solving systems of linear differential equations. Details of how the matrix exponential e'A is used to solve the system x = Ax are the subject of Chapter 11.

- Theorem 9.20. Let A e R"xn and suppose X~~1AX — A, where A is diagonal. Then

![image 98](<Matrix Analysis For Scientists and Engineers_images/imageFile98.png>)

82 Chapter 9. Eigenvalues and Eigenvectors

Proof: Starting from the definition, we have

The following corollary is immediate from the theorem upon setting t = I.

- Corollary 9.21. If A e Rnx" is diagonalizable with eigenvalues A.,-, /' en, and right eigenvectors xt•, / € n_, then eA has eigenvalues eXi, i € n_, and the same eigenvectors.

There are extensions to Theorem 9.20 and Corollary 9.21 for any function that is analytic on the spectrum of A, i.e., f ( A ) = X f ( A ) X ~ l = Xdiag(/(A.i),..., f(Xtt))X~l.

It is desirable, of course, to have a version of Theorem 9.20 and its corollary in which A is not necessarily diagonalizable. It is necessary first to consider the notion of Jordan canonical form, from which such a result is then available and presented later in this chapter.

###### 9.2 Jordan Canonical Form

###### Theorem 9.22.

1. Jordan Canonical Form (/CF): For all A e C"x" with eigenvalues X\,..., kn e C (not necessarily distinct), there exists X € C^x" such that

where each of the Jordan block matrices /i,..., Jq is of the form

![image 99](<Matrix Analysis For Scientists and Engineers_images/imageFile99.png>)

- 9.2. Jordan Canonical Form 83

2. Real Jordan Canonical Form: For all A € Rnx" with eigenvalues Xi, . . . , Xn (not necessarily distinct), there exists X € R"xn such that

where each of the Jordan block matrices J\, ..., Jq is of the form

in the case of real eigenvalues A., e A (A), and

where M; = [ _»' ^ 1 and I2 = \0 A in the case of complex conjugate eigenvalues ai±jpieA(A>).

Proof: For the proof see, for example, [21, pp. 120-124]. D

Transformations like T = I" _, "•{"] allow us to go back and forth between a real JCF and its complex counterpart:

For nontrivial Jordan blocks, the situation is only a bit more complicated. With

![image 100](<Matrix Analysis For Scientists and Engineers_images/imageFile100.png>)

84 Chapter 9. Eigenvalues and Eigenvectors

it is easily checked that

- Definition 9.23. The characteristic polynomials of the Jordan blocks defined in Theorem

###### 9.22 are called the elementary divisors or invariant factors of A.

- Theorem 9.24. The characteristic polynomial of a matrix is the product of its elementary divisors. The minimal polynomial of a matrix is the product of the elementary divisors of highest degree corresponding to distinct eigenvalues.
- Theorem 9.25. Let A e C"x" with eigenvalues AI, ..., Xn. Then

Proof:

- 1. From Theorem 9.22 we have that A = X J X ~ l . Thus, det(A) = det(XJX-1) = det(7) = ]~["=l A,-.
- 2. Again, from Theorem 9.22 we have that A = X J X ~ l . Thus, Tr(A) = Tr(XJX~l) = TrC/X"1*) = Tr(/) = £"=1 A.,-. D

- Example 9.26. Suppose A e E7x7 is known to have 7r(A) = (A. - 1)4(A - 2)3 and a (A.) = (A. — I)2 (A. — 2)2. Then A has two possible JCFs (not counting reorderings of the diagonal blocks):

Note that 7(1) has elementary divisors (A - I)2, (A. - 1), (A. - 1), (A, - 2)2, and (A - 2), while /(2) has elementary divisors (A - I)2, (A - I)2, (A - 2)2, and (A - 2).

![image 101](<Matrix Analysis For Scientists and Engineers_images/imageFile101.png>)

- 9.3. Determination of the JCF &5

- Example 9.27. Knowing TT (A.), a (A), and rank (A — A,,7) for distinct A., is not sufficient to determine the JCF of A uniquely. The matrices

both have 7r(A.) = (A. — a) , a(A.) = (A. — a) , and rank(A — al) = 4, i.e., three eigenvectors.

###### 9.3 Determination of the JCF

The first critical item of information in determining the JCF of a matrix A e Wlxn is its number of eigenvectors. For each distinct eigenvalue A,,, the associated number of linearly independent right (or left) eigenvectors is given by dim A^(A — A.,7) = n — rank(A — A.(7). The straightforward case is, of course, when X,- is simple, i.e., of algebraic multiplicity 1; it then has precisely one eigenvector. The more interesting (and difficult) case occurs when A, is of algebraic multiplicity greater than one. For example, suppose

Then

has rank 1, so the eigenvalue 3 has two eigenvectors associated with it. If we let [^i £2 &]T denote a solution to the linear system (A — 3/)£ = 0, we find that 2£2 + £3=0. Thus, both

are eigenvectors (and are independent). To get a third vector JC3 such that X = [x\ KJ_ XT,] reduces A to JCF, we need the notion of principal vector.

- Definition 9.28. Let A e C"xn (or R"x"). Then x is a right principal vector of degree k associated with X e A (A) if and only if (A - XI)kx = 0 and (A - U}k~lx ^ 0.

###### Remark 9.29.

- 1. An analogous definition holds for a left principal vector of degree k.

![image 102](<Matrix Analysis For Scientists and Engineers_images/imageFile102.png>)

86 Chapter 9. Eigenvalues and Eigenvectors

- 2. The phrase "of grade k" is often used synonymously with "of degree k."
- 3. Principal vectors are sometimes also called generalized eigenvectors, but the latter term will be assigned a much different meaning in Chapter 12.
- 4. The case k = 1 corresponds to the "usual" eigenvector.
- 5. A right (or left) principal vector of degree k is associated with a Jordan block ji of dimension k or larger.

###### 9.3.1 Theoretical computation

To motivate the development of a procedure for determining principal vectors, consider a 2x2 Jordan block {h0 h1. Denote by x(1) and x(2) the two columns of a matrix X e R2,x2 that reduces a matrix A to this JCF. Then the equation AX = XJ can be written

The first column yields the equation Ax(1) = hx(1) which simply says that x(1) is a right eigenvector. The second column yields the following equation for x(2), the principal vector of degree 2:

If we premultiply (9.17) by (A - XI), we find (A - XI)zx( 2) = (A - XI)xw = 0. Thus, the definition of principal vector is satisfied.

This suggests a "general" procedure. First, determine all eigenvalues of A e R"x" (or Cnxn). Then for each distinct X e A (A) perform the following:

- 1. Solve

This step finds all the eigenvectors (i.e., principal vectors of degree 1) associated with X. The number of eigenvectors depends on the rank of A — XI. For example, if rank(A — XI) = n — 1, there is only one eigenvector. If the algebraic multiplicity of

X is greater than its geometric multiplicity, principal vectors still need to be computed from succeeding steps.

- 2. For each independent jc(1), solve

The number of linearly independent solutions at this step depends on the rank of (A — XI)2. If, for example, this rank is n — 2, there are two linearly independent solutions to the homogeneous equation (A — XI)2x^ = 0. One of these solutions is, of course, x(l) (^ 0), since (A - XI)2x(l) = (A - XI)0 = 0. The other solution is the desired principal vector of degree 2. (It may be necessary to take a linear combination of jc(1) vectors to get a right-hand side that is in 7£(A — XI). See, for example, Exercise 7.)

![image 103](<Matrix Analysis For Scientists and Engineers_images/imageFile103.png>)

- 9.3. Determination of the JCF 87

3. For each independent x(2) from step 2, solve

4. Continue in this way until the total number of independent eigenvectors and principal vectors is equal to the algebraic multiplicity of A.

Unfortunately, this natural-looking procedure can fail to find all Jordan vectors. For more extensive treatments, see, for example, [20] and [21]. Determination of eigenvectors and principal vectors is obviously very tedious for anything beyond simple problems (n = 2 or 3, say). Attempts to do such calculations in finite-precision floating-point arithmetic generally prove unreliable. There are significant numerical difficulties inherent in attempting to compute a JCF, and the interested student is strongly urged to consult the classical and very readable [8] to learn why. Notice that high-quality mathematical software such as MATLAB does not offer a jcf command, although a jordan command is available in MATLAB'S Symbolic Toolbox.

- Theorem 9.30. Suppose A e Ckxk has an eigenvalue A, of algebraic multiplicity k and suppose further that rank(A — AI) = k — 1. Let X = [x( l) , . . . , x(k)], where the chain of vectors x(i) is constructed as above. Then
- Theorem 9.31. (x(1), . . . , x(k)} is a linearly independent set.
- Theorem 9.32. Principal vectors associated with different Jordan blocks are linearly independent.

###### Example 9.33. Let

The eigenvalues of A are A1 = 1, h2 = 1, and h3 = 2. First, find the eigenvectors associated with the distinct eigenvalues 1 and 2. (A - 2/)x3(1),(1) = 0 yields

![image 104](<Matrix Analysis For Scientists and Engineers_images/imageFile104.png>)

88 Chapter 9. Eigenvalues and Eigenvectors

(A- l/)x,(1) =0 yields

To find a principal vector of degree 2 associated with the multiple eigenvalue 1, solve (A – l/)x,(2) = x,(1)toeet

Now let

Then it is easy to check that

###### 9.3.2 On the +1 's in JCF blocks

In this subsection we show that the nonzero superdiagonal elements of a JCF need not be 1 's but can be arbitrary — so long as they are nonzero. For the sake of defmiteness, we consider below the case of a single Jordan block, but the result clearly holds for any JCF. Supposed A € Rnxn and

Let D = diag(d1, . . . , dn) be a nonsingular "scaling" matrix. Then

![image 105](<Matrix Analysis For Scientists and Engineers_images/imageFile105.png>)

- 9.4. Geometric Aspects of the JCF 89

Appropriate choice of the di 's then yields any desired nonzero superdiagonal elements. This result can also be interpreted in terms of the matrix X = [x\,..., xn] of eigenvectors and principal vectors that reduces A to its JCF. Specifically, J is obtained from A via the similarity transformation XD = \d\x\,..., dnxn}.

In a similar fashion, the reverse-order identity matrix (or exchange matrix)

can be used to put the superdiagonal elements in the subdiagonal instead if that is desired:

###### 9.4 Geometric Aspects of the JCF

The matrix X that reduces a matrix A e IR"X" (or C nxn) to a JCF provides a change of basis with respect to which the matrix is diagonal or block diagonal. It is thus natural to expect an associated direct sum decomposition of R. Such a decomposition is given in the following theorem.

- Theorem 9.34. Suppose A e R"x" has characteristic polynomial

and minimal polynomial

withA-i, ..., A.m distinct. Then

Note that dimM(A — A.,/)w = «,-.

- Definition 9.35. Let V be a vector space over F and suppose A : V —>• V is a linear transformation. A subspace S c V is A-invariant if AS c S, where AS is defined as the set {As : s e S}.

![image 106](<Matrix Analysis For Scientists and Engineers_images/imageFile106.png>)

90 Chapter 9. Eigenvalues and Eigenvectors

If V is taken to be R" over R, and S e R"x* is a matrix whose columns s\,..., s/t span a /^-dimensional subspace <S, i.e., K(S) = <S, then <S is A-invariant if and only if there exists M eRkxk such that

This follows easily by comparing the /th columns of each side of (9.19):

- Example 9.36. The equation Ax = A* = x A defining a right eigenvector x of an eigenvalue X says that * spans an A-invariant subspace (of dimension one).
- Example 9.37. Suppose X block diagonalizes A, i.e.,

Rewriting in the form

we have that A A, = A", /,, / = 1, 2, so the columns of A, span an A-mvanant subspace. Theorem 9.38. Suppose A e E"x".

7. Let p(A) = «o/ + o?i A + • • • + <xqAq be a polynomial in A. Then N(p(A)) and 7£(p(A)) are A-invariant.

2. S is A-invariant if and only ifS1- is AT-invariant.

Theorem 9.39. If V is a vector space over F such that V = N\ ® • • • 0 Nm, where each A// is A-invariant, then a basis for V can be chosen with respect to which A has a block diagonal representation.

The Jordan canonical form is a special case of the above theorem. If A has distinct eigenvalues A,,- as in Theorem 9.34, we could choose bases for N(A — A.,-/)"' by SVD, for example (note that the power n, could be replaced by v,). We would then get a block diagonal representation for A with full blocks rather than the highly structured Jordan blocks. Other such "canonical" forms are discussed in text that follows.

Suppose A" = [ X i , . . . , Xm] e R"nxn is such that X^AX = diag(7i,..., Jm), where

each Ji = diag(/,i,..., //*,.) and each /,* is a Jordan block corresponding to A, e A(A). We could also use other block diagonal decompositions (e.g., via SVD), but we restrict our attention here to only the Jordan block case. Note that A A", = A*,- /,, so by (9.19) the columns of A", (i.e., the eigenvectors and principal vectors associated with A.,) span an A-invariant subspace of W.

Finally, we return to the problem of developing a formula for e'A in the case that A is not necessarily diagonalizable. Let 7, € C"x"' be a Jordan basis for N(AT — A.,/)"'. Equivalently, partition

![image 107](<Matrix Analysis For Scientists and Engineers_images/imageFile107.png>)

- 9.5. The Matrix Sign Function 91

compatibly. Then

In a similar fashion we can compute

which is a useful formula when used in conjunction with the result

for a k x k Jordan block 7, associated with an eigenvalue A. = A.,.

###### 9.5 The Matrix Sign Function

In this section we give a very brief introduction to an interesting and useful matrix function called the matrix sign function. It is a generalization of the sign (or signum) of a scalar. A survey of the matrix sign function and some of its applications can be found in [15].

- Definition 9.40. Let z E C with Re(z) ^ 0. Then the sign of z is defined by
- Definition 9.41. Suppose A e C"x" has no eigenvalues on the imaginary axis, and let

be a Jordan canonical form for A, with N containing all Jordan blocks corresponding to the eigenvalues of A in the left half-plane and P containing all Jordan blocks corresponding to eigenvalues in the right half-plane. Then the sign of A, denoted sgn(A), is given by

![image 108](<Matrix Analysis For Scientists and Engineers_images/imageFile108.png>)

92 Chapter 9. Eigenvalues and Eigenvectors

where the negative and positive identity matrices are of the same dimensions as N and P, respectively.

There are other equivalent definitions of the matrix sign function, but the one given here is especially useful in deriving many of its key properties. The JCF definition of the matrix sign function does not generally lend itself to reliable computation on a finite-wordlength digital computer. In fact, its reliable numerical calculation is an interesting topic in its own right.

We state some of the more useful properties of the matrix sign function as theorems. Their straightforward proofs are left to the exercises.

- Theorem 9.42. Suppose A e C"x" has no eigenvalues on the imaginary axis, and let S = sgn(A). Then the following hold:

- 1. S is diagonalizable with eigenvalues equal to del.
- 2. S2 = I.
- 3. AS = SA.
- 4. sgn(A") = (sgn(A))".
- 5. sgn(T-lAT) = T-lsgn(A)TforallnonsingularT e C"x".
- 6. sgn(cA) = sgn(c) sgn(A)/or all nonzero real scalars c.

- Theorem 9.43. Suppose A e C"x" has no eigenvalues on the imaginary axis, and let S — sgn(A). Then the following hold:

- 1. 7l(S — /) is an A-invariant subspace corresponding to the left half-plane eigenvalues of A (the negative invariant subspace).
- 2. R(S+/) is an A-invariant subspace corresponding to the right half-plane eigenvalues of A (the positive invariant subspace).
- 3. negA = (/ — S)/2 is a projection onto the negative invariant subspace of A.
- 4. posA = (/ + S)/2 is a projection onto the positive invariant subspace of A.

###### EXERCISES

1. Let A e Cnxn have distinct eigenvalues AI, ..., Xn with corresponding right eigenvectors Xi, ... ,xn and left eigenvectors y\, ..., yn, respectively. Let v e C" be an arbitrary vector. Show that v can be expressed (uniquely) as a linear combination

of the right eigenvectors. Find the appropriate expression for v as a linear combination of the left eigenvectors as well.

![image 109](<Matrix Analysis For Scientists and Engineers_images/imageFile109.png>)

Exercises 93

- 2. Suppose A € C"x" is skew-Hermitian, i.e., AH = —A. Prove that all eigenvalues of a skew-Hermitian matrix must be pure imaginary.
- 3. Suppose A e C"x" is Hermitian. Let A be an eigenvalue of A with corresponding right eigenvector x. Show that x is also a left eigenvector for A. Prove the same result if A is skew-Hermitian.

4. Suppose a matrix A € R5x5 has eigenvalues {2, 2, 2, 2, 3}. Determine all possible JCFs for A.

- 5. Determine the eigenvalues, right eigenvectors and right principal vectors if necessary, and (real) JCFs of the following matrices:
- 6. Determine the JCFs of the following matrices:

###### 7. Let

Find a nonsingular matrix X such that X 1AX = J, where J is the JCF

Hint: Use[— 1 1 — l]r as an eigenvector. The vectors [0 1 — l]rand[l 0 0]r are both eigenvectors, but then the equation (A — /)jc(2) = x(1) can't be solved.

- 8. Show that all right eigenvectors of the Jordan block matrix in Theorem 9.30 must be multiples of e\ e R*. Characterize all left eigenvectors.
- 9. Let A e R"x" be of the form A = xyT, where x, y e R" are nonzero vectors with xTy = 0. Determine the JCF of A.
- 10. Let A e R"xn be of the form A = / + xyT, where x, y e R" are nonzero vectors with xTy = 0. Determine the JCF of A.
- 11. Suppose a matrix A e R16x16 has 16 eigenvalues at 0 and its JCF consists of a single Jordan block of the form specified in Theorem 9.22. Suppose the small number 10~16 is added to the (16,1) element of J. What are the eigenvalues of this slightly perturbed matrix?

![image 110](<Matrix Analysis For Scientists and Engineers_images/imageFile110.png>)

94 Chapter 9. Eigenvalues and Eigenvectors

- 12. Show that every matrix A e R"x" can be factored in the form A = Si$2, where Si and £2 are real symmetric matrices and one of them, say Si, is nonsingular. Hint: Suppose A = X J X ~ l is a reduction of A to JCF and suppose we can construct

the "symmetric factorization" of J. Then A = (XSiXT)(X~T S2X~l) would be the required symmetric factorization of A. Thus, it suffices to prove the result for the JCF. The transformation P in (9.18) is useful.

- 13. Prove that every matrix A e Wx" is similar to its transpose and determine a similarity transformation explicitly. Hint: Use the factorization in the previous exercise.
- 14. Consider the block upper triangular matrix

where A e M"xn and An e Rkxk with 1 < k < n. Suppose Au ^ 0 and that we want to block diagonalize A via the similarity transformation

where X e R*x <«-*), i.e.,

Find a matrix equation that X must satisfy for this to be possible. If n = 2 and k = 1, what can you say further, in terms of AU and A 22, about when the equation for X is solvable?

- 15. Prove Theorem 9.42.
- 16. Prove Theorem 9.43.
- 17. Suppose A e C"xn has all its eigenvalues in the left half-plane. Prove that sgn(A) = -/.

![image 111](<Matrix Analysis For Scientists and Engineers_images/imageFile111.png>)

- Chapter 10

###### Canonical Forms

###### 10.1 Some Basic Canonical Forms

Problem: Let V and W be vector spaces and suppose A : V —>• W is a linear transformation. Find bases in V and W with respect to which Mat A has a "simple form" or "canonical form." In matrix terms, if A e Rmxn, find P e R™xm and Q e Rnnxn such that PAQ has a "canonical form." The transformation A M» PAQ is called an equivalence; it is called an orthogonal equivalence if P and Q are orthogonal matrices.

- Remark 10.1. We can also consider the case A e Cmxn and unitary equivalence if P and <2 are unitary. Two special cases are of interest:

- 1. If W = V and <2 = P"1, the transformation A H> PAP"1 is called a similarity.
- 2. If W = V and if Q = PT is orthogonal, the transformation A i-» PAPT is called an orthogonal similarity (or unitary similarity in the complex case).

The following results are typical of what can be achieved under a unitary similarity. If A = AH 6 C"x" has eigenvalues AI, ..., An, then there exists a unitary matrix £7 such that

UHAU — D, where D = diag(A.j,..., A.n). This is proved in Theorem 10.2. What other matrices are "diagonalizable" under unitary similarity? The answer is given in Theorem

- 10.9, where it is proved that a general matrix A e C"x" is unitarily similar to a diagonal matrix if and only if it is normal (i.e., AAH = AH A). Normal matrices include Hermitian, skew-Hermitian, and unitary matrices (and their "real" counterparts: symmetric, skewsymmetric, and orthogonal, respectively), as well as other matrices that merely satisfy the

definition, such as A = [ _ab ^1 for real scalars a and b. If a matrix A is not normal, the most "diagonal" we can get is the JCF described in Chapter 9.

- Theorem 10.2. Let A = AH e C"x" have (real) eigenvalues A.I, ..., Xn. Then there exists a unitary matrix X such that XHAX = D = diag(A.j, ..., Xn) (the columns ofX are orthonormal eigenvectors for A).

###### 95

![image 112](<Matrix Analysis For Scientists and Engineers_images/imageFile112.png>)

96 Chapter 10. Canonical Forms

Proof: Let x\ be a right eigenvector corresponding to X\, and normalize it such that xf*x\ = 1. Then there exist n — 1 additional vectors x2, ..., xn such that X = [x\,..., xn] = [x\ X2] is unitary. Now

In (10.1) we have used the fact that Ax\ = k\x\. When combined with the fact that x"xi = 1, we get A-i remaining in the (l,l)-block. We also get 0 in the (2,l)-block by noting that x\ is orthogonal to all vectors in X2. In (10.2), we get 0 in the (l,2)-block by noting that XH AX is Hermitian. The proof is completed easily by induction upon noting that the (2,2)-block must have eigenvalues X2,..., A.n. D

Given a unit vector x\ e E", the construction of X2 e ]R"X("-1) such that X [x\ X2] is orthogonal is frequently required. The construction can actually be performed quite easily by means of Householder (or Givens) transformations as in the proof of the following general result.

- Theorem 10.3. Let X\ e Cnxk have orthonormal columns and suppose U is a unitary matrix such that UX\ = \ 0 1, where R € Ckxk is upper triangular. Write UH = [U\ U2] with Ui € Cnxk. Then [Xi U2] is unitary. Proof: Let X\ = [x\,..., Xk]. Construct a sequence of Householder matrices (also known

- as elementary reflectors) H\,..., Hk in the usual way (see below) such that

where R is upper triangular (and nonsingular since x\, ..., Xk are orthonormal). Let U = Hk...Hv. Then UH = //,-•• Hk and

Then x^U2 = 0 (/ € k) means that xf is orthogonal to each of the n — k columns of U2. But the latter are orthonormal since they are the last n — k rows of the unitary matrix U. Thus, [Xi f/2] is unitary. D

The construction called for in Theorem 10.2 is then a special case of Theorem 10.3 for k = 1. We illustrate the construction of the necessary Householder matrix for k — 1. For simplicity, we consider the real case. Let the unit vector x\ be denoted by [£i, ..., %n]T.

![image 113](<Matrix Analysis For Scientists and Engineers_images/imageFile113.png>)

- 10.1. Some Basic Canonical Forms 97

Then the necessary Householder matrix needed for the construction of X^ is given by U = I — 2uu+ = I — -^UUT, where u = [t-\ ± 1, £2, • • •» £«]r- It can easily be checked that U is symmetric and UTU = U2 = I, so U is orthogonal. To see that U effects the necessary compression of jci, it is easily verified that UTU = 2 ± 2£i and UTX\ = 1 ± £1. Thus,

Further details on Householder matrices, including the choice of sign and the complex case, can be consulted in standard numerical linear algebra texts such as [7], [11], [23], [25].

The real version of Theorem 10.2 is worth stating separately since it is applied frequently in applications.

- Theorem 10.4. Let A = AT e Enxn have eigenvalues k\, ... ,Xn. Then there exists an orthogonal matrix X e Wlxn (whose columns are orthonormal eigenvectors of A) such that XTAX = D = diag(Xi, ..., Xn).

Note that Theorem 10.4 implies that a symmetric matrix A (with the obvious analogue from Theorem 10.2 for Hermitian matrices) can be written

which is often called the spectral representation of A. In fact, A in (10.3) is actually a weighted sum of orthogonal projections P, (onto the one-dimensional eigenspaces corresponding to the A., 's), i.e.,

where P, = PUM — xixf = xixj since xj xi — 1.

The following pair of theorems form the theoretical foundation of the double-FrancisQR algorithm used to compute matrix eigenvalues in a numerically stable and reliable way.

![image 114](<Matrix Analysis For Scientists and Engineers_images/imageFile114.png>)

98 Chapter 10. Canonical Forms

- Theorem 10.5 (Schur). Let A e C"x". Then there exists a unitary matrix U such that UH AU = T, where T is upper triangular.

Proof: The proof of this theorem is essentially the same as that of Theorem 10.2 except that in this case (using the notation U rather than X) the (l,2)-block wf AU2 is not 0. D

In the case of A e R"x", it is thus unitarily similar to an upper triangular matrix, but if A has a complex conjugate pair of eigenvalues, then complex arithmetic is clearly needed to place such eigenvalues on the diagonal of T. However, the next theorem shows that every A e Wxn is also orthogonally similar (i.e., real arithmetic) to a quasi-upper-triangular matrix. A quasi-upper-triangular matrix is block upper triangular with 1 x 1 diagonal blocks corresponding to its real eigenvalues and 2x2 diagonal blocks corresponding to its complex conjugate pairs of eigenvalues.

Theorem 10.6 (Murnaghan-Wintner). Let A e R"x". Then there exists an orthogonal matrix U such that UTAU = S, where S is quasi-upper-triangular.

- Definition 10.7. The triangular matrix T in Theorem 10.5 is called a Schur canonical form or Schur form. The quasi-upper-triangular matrix S in Theorem 10.6 is called a real Schur canonical form or real Schur form (RSF). The columns of a unitary [orthogonal] matrix U that reduces a matrix to [real] Schur form are called Schur vectors.

- Example 10.8. The matrix

is in RSF. Its real JCF is

Note that only the first Schur vector (and then only if the corresponding first eigenvalue is real if U is orthogonal) is an eigenvector. However, what is true, and sufficient for virtually all applications (see, for example, [17]), is that the first k Schur vectors span the same Ainvariant subspace as the eigenvectors corresponding to the first k eigenvalues along the diagonal of T (or S).

While every matrix can be reduced to Schur form (or RSF), it is of interest to know when we can go further and reduce a matrix via unitary similarity to diagonal form. The following theorem answers this question.

Theorem 10.9. A matrix A e C"x" is unitarily similar to a diagonal matrix if and only if

- A is normal (i.e., AHA = AAH). Proof: Suppose U is a unitary matrix such that UH AU = D, where D is diagonal. Then

so A is normal.

![image 115](<Matrix Analysis For Scientists and Engineers_images/imageFile115.png>)

- 10.2. Definite Matrices 99

Conversely, suppose A is normal and let U be a unitary matrix such that UH AU = T, where T is an upper triangular matrix (Theorem 10.5). Then

It is then a routine exercise to show that T must, in fact, be diagonal. D

###### 10.2 Definite Matrices

- Definition 10.10. A symmetric matrix A e Wxn is

- 1. positive definite if and only ifxTAx > Qfor all nonzero x G W1. We write A > 0.
- 2. nonnegative definite (or positive semidefinite) if and only if XT Ax > 0 for all nonzero x e W. We write A > 0.
- 3. negative definite if—A is positive definite. We write A < 0.
- 4. nonpositive definite (or negative semidefinite) if— A is nonnegative definite. We write A < 0.

Also, if A and B are symmetric matrices, we write A > B if and only if A — B > 0 or

- B — A < 0. Similarly, we write A > B if and only ifA — B>QorB — A < 0.

- Remark 10.11. If A e C"x" is Hermitian, all the above definitions hold except that superscript //s replace Ts. Indeed, this is generally true for all results in the remainder of this section that may be stated in the real case for simplicity.
- Remark 10.12. If a matrix is neither definite nor semidefinite, it is said to be indefinite.

- Theorem 10.13. Let A = AH e Cnxn with eigenvalues X{ > A2 > • • • > An. Then for all x eC",

Proof: Let U be a unitary matrix that diagonalizes A as in Theorem 10.2. Furthermore, let v = UHx, where x is an arbitrary vector in CM, and denote the components of y by j]i, i € n. Then

But clearly

![image 116](<Matrix Analysis For Scientists and Engineers_images/imageFile116.png>)

100 Chapter 10. Canonical Forms

and

from which the theorem follows. D

- Remark 10.14. The ratio ^^ for A = AH <= Cnxn and nonzero jc e C" is called the

Rayleigh quotient of jc. Theorem 10.13 provides upper (AO and lower (A.w) bounds for the Rayleigh quotient. If A = AH e C"x" is positive definite, XHAx > 0 for all nonzero x E C",soO < Xn < ••• < A.I.

- Corollary 10.15. Let A e C"x". Then \\A\\2 = ^m(AH A}. Proof: For all x € C" we have

Let jc be an eigenvector corresponding to Xmax(AHA). Then ^pjp2 = ^^(A" A), whence

- Definition 10.16. A principal submatrix of an nxn matrix A is the (n — k)x(n — k) matrix that remains by deleting k rows and the corresponding k columns. A leading principal submatrix of order n — k is obtained by deleting the last k rows and columns.

- Theorem 10.17. A symmetric matrix A e E"x" is positive definite if and only if any of the following three equivalent conditions hold:

- 1. The determinants of all leading principal submatrices of A are positive.
- 2. All eigenvalues of A are positive.
- 3. A can be written in the form MT M, where M e R"x" is nonsingular.

- Theorem 10.18. A symmetric matrix A € R"x" is nonnegative definite if and only if any of the following three equivalent conditions hold:

- 1. The determinants of all principal submatrices of A are nonnegative.
- 2. All eigenvalues of A are nonnegative.
- 3. A can be written in the form MT M, where M 6 Rix" and k > rank(A) — rank(M).

- Remark 10.19. Note that the determinants of all principal eubmatrioes muet bQ nonnogativo in Theorem 10.18.1, not just those of the leading principal submatrices. For example,

consider the matrix A — [0 _l 1. The determinant of the 1x1 leading submatrix is 0 and the determinant of the 2x2 leading submatrix is also 0 (cf. Theorem 10.17). However, the

![image 117](<Matrix Analysis For Scientists and Engineers_images/imageFile117.png>)

- 10.2. Definite Matrices 101

principal submatrix consisting of the (2,2) element is, in fact, negative and A is nonpositive definite.

- Remark 10.20. The factor M in Theorem 10.18.3 is not unique. For example, if

then M can be

Recall that A > B if the matrix A — B is nonnegative definite. The following theorem is useful in "comparing" symmetric matrices. Its proof is straightforward from basic definitions.

- Theorem 10.21. Let A, B e Rnxn be symmetric.

- 1. If A >BandMe Rnxm, then MT AM > MTBM.
- 2. Ifj A > B and M e Rmnxm, then MT AM > M.TBM.

The following standard theorem is stated without proof (see, for example, [16, p. 181]). It concerns the notion of the "square root" of a matrix. That is, if A € E"xn, we say that S e Rnx" is a square root of A if S2 — A. In general, matrices (both symmetric and nonsymmetric) have infinitely many square roots. For example, if A = /2, any matrix S of

the form [cs°*ee _cs™9e ] is a square root.

- Theorem 10.22. Let A e R"x" be nonnegative definite. Then A has a unique nonnegative definite square root S. Moreover, SA = AS and rankS = rank A (and hence S is positive definite if A is positive definite).

A stronger form of the third characterization in Theorem 10.17 is available and is known as the Cholesky factorization. It is stated and proved below for the more general Hermitian case.

- Theorem 10.23. Let A e <Cnxn be Hermitian and positive definite. Then there exists a unique nonsingular lower triangular matrix L with positive diagonal elements such that A = LLH.

Proof: The proof is by induction. The case n = 1 is trivially true. Write the matrix A in the form

By our induction hypothesis, assume the result is true for matrices of order n — 1 so that B may be written as B = L\L^, where L\ e C1-""1^""^ is nonsingular and lower triangular

![image 118](<Matrix Analysis For Scientists and Engineers_images/imageFile118.png>)

102 Chapter 10. Canonical Forms

with positive diagonal elements. It remains to prove that we can write the n x n matrix A

in the form

where a is positive. Performing the indicated matrix multiplication and equating the corresponding submatrices, we see that we must have L\c = b and ann = CHC + a2. Clearly c is given simply by c = L^b. Substituting in the expression involving a, we find a2 = ann — bHL\H L\lb = ann — bH B~lb (= the Schur complement of B in A). But we know that

Since det(fi) > 0, we must have ann —bHB lb > 0. Choosing a to be the positive square root of «„„ — bHB~lb completes the proof. D

###### 10.3 Equivalence Transformations and Congruence

- Theorem 10.24. Let A € C™*71. Then there exist matrices P e C™xm and Q e C"nx" such that

Proof: A classical proof can be consulted in, for example, [21, p. 131]. Alternatively, suppose A has an SVD of the form (5.2) in its complex version. Then

Note that the greater freedom afforded by the equivalence transformation of Theorem

- 10.24, as opposed to the more restrictive situation of a similarity transformation, yields a far "simpler" canonical form (10.4). However, numerical procedures for computing such an equivalence directly via, say, Gaussian or elementary row and column operations, are generally unreliable. The numerically preferred equivalence is, of course, the unitary equivalence known as the SVD. However, the SVD is relatively expensive to compute and other canonical forms exist that are intermediate between (10.4) and the SVD; see, for example [7, Ch. 5], [4, Ch. 2]. Two such forms are stated here. They are more stably computable than (10.4) and more efficiently computable than a full SVD. Many similar results are also available.

![image 119](<Matrix Analysis For Scientists and Engineers_images/imageFile119.png>)

- 10.3. Equivalence Transformations and Congruence 103

- Theorem 10.25 (Complete Orthogonal Decomposition). Let A e C™x". Then there exist unitary matrices U e Cmxm and V e Cnxn such that

where R e €,rrxr is upper (or lower) triangular with positive diagonal elements. Proof: For the proof, see [4]. D

- Theorem 10.26. Let A e C™x". Then there exists a unitary matrix Q e Cmxm and a permutation matrix Fl e C"x" such that

where R E Crrxr is upper triangular and S e Crx("r) is arbitrary but in general nonzero. Proof: For the proof, see [4]. D

- Remark 10.27. When A has full column rank but is "near" a rank deficient matrix, various rank revealing QR decompositions are available that can sometimes detect such phenomena at a cost considerably less than a full SVD. Again, see [4] for details.

- Definition 10.28. Let A e Cnxn and X e Cnnxn. The transformation A i-> XH AX is called a congruence. Note that a congruence is a similarity if and only ifX is unitary.

Note that congruence preserves the property of being Hermitian; i.e., if A is Hermitian, then XH AX is also Hermitian. It is of interest to ask what other properties of a matrix are preserved under congruence. It turns out that the principal property so preserved is the sign of each eigenvalue.

- Definition 10.29. Let A = AH e C"x" and let 7t, v, and £ denote the numbers of positive, negative, and zero eigenvalues, respectively, of A. Then the inertia of A is the triple of numbers In(A) = (n, v, £). The signature of A is given by sig(A) = n — v.

###### Example 10.30.

- 2. If A = A" eCnx",thenA > 0 if and only if In (A) = (n,0,0).
- 3. If In(A) = (TT, v, £), then rank(A) = n + v.

- Theorem 10.31 (Sylvester's Law of Inertia). Let A = AHe Cnxn and X e Cnnxn. Then In(A) = ln(XHAX). Proof: For the proof, see, for example, [21, p. 134]. D

Theorem 10.31 guarantees that rank and signature of a matrix are preserved under congruence. We then have the following.

![image 120](<Matrix Analysis For Scientists and Engineers_images/imageFile120.png>)

104 Chapter 10. Canonical Forms

- Theorem 10.32. Let A = AHe C"xn with In(A) = (jt, v, £). Then there exists a matrix

X e C"nxn such that XHAX = diag(l, ..., 1, -1,..., -1, 0, ..., 0), where the number of 1 's is 7i, the number of — l's is v, and the number 0/0 's is (,.

Proof: Let AI , ..., Xw denote the eigenvalues of A and order them such that the first TT are positive, the next v are negative, and the final £ are 0. By Theorem 10.2 there exists a unitary matrix U such that UHAU = diag(Ai, ..., Aw). Define the n x n matrix

Then it is easy to check that X = U W yields the desired result. D

10.3.1 Block matrices and definiteness

- Theorem 10.33. Suppose A = AT and D = DT. Then

if and only if either A > 0 and D - BT A~l B > 0, or D > 0 and A - BD^BT > 0. Proof: The proof follows by considering, for example, the congruence

The details are straightforward and are left to the reader. D

- Remark 10.34. Note the symmetric Schur complements of A (or D) in the theorem.

- Theorem 10.35. Suppose A = AT and D = DT. Then

if and only ifA>0, AA+B = B, and D - BT A+B > 0. Proof: Consider the congruence with

and proceed as in the proof of Theorem 10.33. D

###### 10.4 Rational Canonical Form One final canonical form to be mentioned is the rational canonical form.

![image 121](<Matrix Analysis For Scientists and Engineers_images/imageFile121.png>)

- 10.4. Rational Canonical Form 105

- Definition 10.36. A matrix A e M"x" is said to be nonderogatory if its minimal polynomial and characteristic polynomial are the same or, equivalently, if its Jordan canonical form has only one block associated with each distinct eigenvalue.

Suppose A E Wxn is a nonderogatory matrix and suppose its characteristic polyno-

mial is 7r(A) = A" — (a0 + «A + is similar to a matrix of the form

+ an_iAn~')- Then it can be shown (see [12]) that A

- Definition 10.37. A matrix A e Enx" of the form (10.7) is called a companion matrix or is said to be in companion form.

Companion matrices also appear in the literature in several equivalent forms. To illustrate, consider the companion matrix

This matrix is a special case of a matrix in lower Hessenberg form. Using the reverse-order identity similarity P given by (9.18), A is easily seen to be similar to the following matrix in upper Hessenberg form:

Moreover, since a matrix is similar to its transpose (see exercise 13 in Chapter 9), the following are also companion matrices similar to the above:

Notice that in all cases a companion matrix is nonsingular if and only if aO /= 0. In fact, the inverse of a nonsingular companion matrix is again in companion form. For

£*Yamr\1j=»

![image 122](<Matrix Analysis For Scientists and Engineers_images/imageFile122.png>)

106 Chapter 10. Canonical Forms

with a similar result for companion matrices of the form (10.10).

If a companion matrix of the form (10.7) is singular, i.e., if ao = 0, then its pseudoinverse can still be computed. Let a e M""1 denote the vector \a\, 02,..., an-i] and let c = l+lara. Then it is easily verified that

Note that / — caaT = (I + aaT) , and hence the pseudoinverse of a singular companion matrix is not a companion matrix unless a = 0.

Companion matrices have many other interesting properties, among which, and perhaps surprisingly, is the fact that their singular values can be found in closed form; see

[14].

- Theorem 10.38. Let a\ > GI > • • • > an be the singular values of the companion matrix A in (10.7). Let a = a\ + a\ + • • • + a%_{ and y = 1 + «.Q + a. Then

Ifao ^ 0, the largest and smallest singular values can also be written in the equivalent form

- Remark 10.39. Explicit formulas for all the associated right and left singular vectors can also be derived easily.

If A € Rnx" is derogatory, i.e., has more than one Jordan block associated with

- at least one eigenvalue, then it is not similar to a companion matrix of the form (10.7). However, it can be shown that a derogatory matrix is similar to a block diagonal matrix, each of whose diagonal blocks is a companion matrix. Such matrices are said to be in rational canonical form (or Frobenius canonical form). For details, see, for example, [12].

Companion matrices appear frequently in the control and signal processing literature but unfortunately they are often very difficult to work with numerically. Algorithms to reduce an arbitrary matrix to companion form are numerically unstable. Moreover, companion matrices are known to possess many undesirable numerical properties. For example, in general and especially as n increases, their eigenstructure is extremely ill conditioned, nonsingular ones are nearly singular, stable ones are nearly unstable, and so forth [14].

![image 123](<Matrix Analysis For Scientists and Engineers_images/imageFile123.png>)

Exercises 107

Companion matrices and rational canonical forms are generally to be avoided in floatingpoint computation.

- Remark 10.40. Theorem 10.38 yields some understanding of why difficult numerical behavior might be expected for companion matrices. For example, when solving linear systems of equations of the form (6.2), one measure of numerical sensitivity is KP(A) =

II ^ IIp II A~l IIp>me so-called condition number of A with respect to inversion and with respect to the matrix P-norm. If this number is large, say 0(10*), one may lose up to k digits of precision. In the 2-norm, this condition number is the ratio of largest to smallest singular values which, by the theorem, can be determined explicitly as

It is easy to show that y/2/ao < k2(A) < -£-,, and when GO is small or y is large (or both), then K2(A) ^ T~I. It is not unusual for y to be large for large n. Note that explicit formulas for K\ (A) and Koo(A) can also be determined easily by using (10.11).

###### EXERCISES

- 1. Show that if a triangular matrix is normal, then it must be diagonal.
- 2. Prove that if A e M"x" is normal, then Af(A) = A/"(Ar).
- 3. Let A G Cnx" and define p(A) = maxx€A(A) I'M- Then p(A) is called the spectral radius of A. Show that if A is normal, then p(A) = ||A||2. Show that the converse is true if n = 2.
- 4. Let A € Cnxn be normal with eigenvalues y1 , ..., yn and singular values a\ > a2 >

• • • > on > 0. Show that a, (A) = |A.,-(A)| for i e n.

- 5. Use the reverse-order identity matrix P introduced in (9.18) and the matrix U in Theorem 10.5 to find a unitary matrix Q that reduces A e C"x" to lower triangular form.
- 6. Let A = I J MeC2 x 2. Find a unitary matrix U such that
- 7. If A e Wxn is positive definite, show that A [ must also be positive definite.

3. Suppose A e E"x" is positive definite. Is [ ^ /i 1 > 0?

}. Let R, S 6 Enxn be symmetric. Show that [ * J 1 > 0 if and only if S > 0 and

R> S

![image 124](<Matrix Analysis For Scientists and Engineers_images/imageFile124.png>)

108 Chapter 10. Canonical Forms

10. Find the inertia of the following matrices:

![image 125](<Matrix Analysis For Scientists and Engineers_images/imageFile125.png>)

- Chapter 11

###### Linear Differential and Difference Equations

###### 11.1 Differential Equations

In this section we study solutions of the linear homogeneous system of differential equations

for t > IQ. This is known as an initial-value problem. We restrict our attention in this chapter only to the so-called time-invariant case, where the matrix A e Rnxn is constant and does not depend on t. The solution of (11.1) is then known always to exist and be unique. It can be described conveniently in terms of the matrix exponential.

- Definition 11.1. For all A e Rnxn, the matrix exponential eA e Rnxn is defined by the power series

The series (11.2) can be shown to converge for all A (has radius of convergence equal to +00). The solution of (11.1) involves the matrix

which thus also converges for all A and uniformly in t.

###### 11.1.1 Properties of the matrix exponential

1. e° = I.

Proof: This follows immediately from Definition 11.1 by setting A = 0.

2. For all A G R"XM, (eAf - e^. Proof: This follows immediately from Definition 11.1 and linearity of the transpose.

109

![image 126](<Matrix Analysis For Scientists and Engineers_images/imageFile126.png>)

110 Chapter 11. Linear Differential and Difference Equations

- 3. For all A e R"x" and for all t, r e R, e(t+T)A = e'AerA = elAe'A. Proof: Note that

Compare like powers of A in the above two equations and use the binomial theorem

on (t + T)*.

- 4. For all A, B e R"xn and for all t e R, et(A+B) =^e'Ae'B = e'Be'A if and only if A and B commute, i.e., AB = B A. Proof: Note that

and

and

while

Compare like powers of t in the first equation and the second or third and use the binomial theorem on (A + B)k and the commutativity of A and B.

- 5. For all A e R"x" and for all t e R, (e'A)~l = e~'A. Proof: Simply take T = — t in property 3.
- 6. Let £ denote the Laplace transform and £~! the inverse Laplace transform. Then for all A € R"x" and for all t € R,

(a) C{etA} = (sI-Arl. (b) £-1{(j/-A)-1} = «M.

Proof: We prove only (a). Part (b) follows similarly.

![image 127](<Matrix Analysis For Scientists and Engineers_images/imageFile127.png>)

- 11.1. Differential Equations 111

= (sl -A)-1.

The matrix (s I — A) ~' is called the resolvent of A and is defined for all s not in A (A). Notice in the proof that we have assumed, for convenience, that A is diagonalizable. If this is not the case, the scalar dyadic decomposition can be replaced by

using the JCF. All succeeding steps in the proof then follow in a straightforward way.

7. For all A e R"x" and for all t e R, £(e'A) = AetA = e'AA.

Proof: Since the series (11.3) is uniformly convergent, it can be differentiated term-byterm from which the result follows immediately. Alternatively, the formal definition

can be employed as follows. For any consistent matrix norm,

![image 128](<Matrix Analysis For Scientists and Engineers_images/imageFile128.png>)

112 Chapter 11. Linear Differential and Difference Equations

For fixed t, the right-hand side above clearly goes to 0 as At goes to 0. Thus, the limit exists and equals Ae'A. A similar proof yields the limit e'A A, or one can use the fact that A commutes with any polynomial of A of finite degree and hence with e'A.

###### 11.1.2 Homogeneous linear differential equations

- Theorem 11.2. Let A e Rnxn. The solution of the linear homogeneous initial-value problem

Proof: Differentiate (11.5) and use property 7 of the matrix exponential to get x(t) = Ae(t~to)Axo = Ax(t). Also, x(t0) — e(fo~t°')AXQ — XQ so, by the fundamental existence and uniqueness theorem for ordinary differential equations, (11.5) is the solution of (11.4). D

###### 11.1.3 Inhomogeneous linear differential equations

- Theorem 11.3. Let A e Rnxn, B e Wxm and let the vector-valued function u be given and, say, continuous. Then the solution of the linear inhomogeneous initial-value problem

###### for t > IQ is given by the variation of parameters formula

Proof: Differentiate (11.7) and again use property 7 of the matrix exponential. The general formula

is used to get x(t) = Ae{'-to)Ax0 + f'o Ae('-s)ABu(s) ds + Bu(t) = Ax(t) + Bu(t). Also, *('o) = <?(f°~fo)/1.¥o + 0 = XQ so, by the fundamental existence and uniqueness theorem for ordinary differential equations, (11.7) is the solution of (11.6). D

- Remark 11.4. The proof above simply verifies the variation of parameters formula by direct differentiation. The formula can be derived by means of an integrating factor "trick" as follows. Premultiply the equation x — Ax = Bu by e~tA to get

![image 129](<Matrix Analysis For Scientists and Engineers_images/imageFile129.png>)

- 11.1. Differential Equations 113

Now integrate (11.8) over the interval [to, t]:

Thus,

and hence

###### 11.1.4 Linear matrix differential equations

Matrix-valued initial-value problems also occur frequently. The first is an obvious generalization of Theorem 11.2, and the proof is essentially the same.

Theorem 11.5. Let A e Wlxn. The solution of the matrix linear homogeneous initial-value nrohlcm

for t > to is given by

In the matrix case, we can have coefficient matrices on both the right and left. For convenience, the following theorem is stated with initial time to = 0. Theorem 11.6. Let A e Rnxn, B e Rmxm, and C e Rnxm. Then the matrix initial-value problem

has the solution X(t) —= eatACeratB Proof: Differentiate etACetB with respect to t and use property 7 of the matrix exponential. The fact that X(t) satisfies the initial condition is trivial. D Corollary 11.7. Let A, C e IR"X". Then the matrix initial-value problem

has the solution X(t} = etACetAT.

When C is symmetric in (11.12), X(t) is symmetric and (11.12) is known as a Lyapunov differential equation. The initial-value problem (11.11) is known as a Sylvester differential equation.

![image 130](<Matrix Analysis For Scientists and Engineers_images/imageFile130.png>)

114 Chapter 11. Linear Differential and Difference Equations

###### 11.1.5 Modal decompositions

Let A E Wxn and suppose, for convenience, that it is diagonalizable (if A is not diagonalizable, the rest of this subsection is easily generalized by using the JCF and the decomposition A — ^ Xf Ji YtH as discussed in Chapter 9). Then the solution x(t) of (11.4) can be written

The ki s are called the modal velocities and the right eigenvectors *, are called the modal directions. The decomposition above expresses the solution x(t) as a weighted sum of its modal velocities and directions.

This modal decomposition can be expressed in a different looking but identical form if we write the initial conditionXQ as a weighted sum of the right eigenvectors Then

In the last equality we have used the fact that yf*Xj = Sfj. Similarly, in the inhomogeneous case we can write

###### 11.1.6 Computation of the matrix exponential JCF method

Let A e R"x" and suppose X e Rnxn is such that X"1 AX = J, where J is a JCF for A. Then

![image 131](<Matrix Analysis For Scientists and Engineers_images/imageFile131.png>)

- 11.1. Differential Equations 115

If A is diagonalizable, it is then easy to compute etA via the formula etA = XetJ X ' since etj is simply a diagonal matrix.

In the more general case, the problem clearly reduces simply to the computation of the exponential of a Jordan block. To be specific, let .7, e <Ckxk be a Jordan block of the form

Clearly A/ and N commute. Thus, etJi = e'uetN by property 4 of the matrix exponential. The diagonal part is easy: etu = diag(ex',..., ext}. But etN is almost as easy since N is nilpotent of degree k.

- Definition 11.8. A matrix M e Mnx" Mp = 0, while Mp~l ^ 0.

is nilpotent of degree (or index, or grade) p if

For the matrix N defined above, it is easy to check that while N has 1's along only its first superdiagonal (and O's elsewhere), N2 has 1's along only its second superdiagonal, and so forth. Finally, Nk~l has a 1 in its (1, k) element and has O's everywhere else, and Nk = 0. Thus, the series expansion of e'N is finite, i.e.,

Thus,

In the case when A. is complex, a real version of the above can be worked out.

![image 132](<Matrix Analysis For Scientists and Engineers_images/imageFile132.png>)

116 Chapter 11. Linear Differential and Difference Equations

- Example 11.9. Let A = [ ~_\ J]. Then A (A) = {-2, -2} and

###### Interpolation method

This method is numerically unstable in finite-precision arithmetic but is quite effective for hand calculation in small-order problems. The method is stated and illustrated for the exponential function but applies equally well to other functions.

Given A € E.nxn and /(A) = etx, compute f(A) = e'A, where t is a fixed scalar. Suppose the characteristic polynomial of A can be written as n ( X ) = Yi?=i (^ ~~ ^i)"'» where the A.,- s are distinct. Define

where OTQ, ..., an-i are n constants that are to be determined. They are, in fact, the unique solution of the n equations:

Here, the superscript (&) denotes the fcth derivative with respect to X. With the a,s then known, the function g is known and /(A) = g(A). The motivation for this method is the Cayley-Hamilton Theorem, Theorem 9.3, which says that all powers of A greater than n — 1 can be expressed as linear combinations of Ak for k = 0, 1, ..., n — 1. Thus, all the terms of order greater than n — 1 in the power series for e'A can be written in terms of these lower-order powers as well. The polynomial g gives the appropriate linear combination.

###### Example 11.10. Let

and /(A) = etK. Then jr(A.) = -(A. + I)3, so m = 1 and n{ = 3. Let g(X) — UQ + a\X + o^A.2. Then the three equations for the a,s are given by

![image 133](<Matrix Analysis For Scientists and Engineers_images/imageFile133.png>)

11.1. Differential Equations 117

Solving for the a, s, we find

Thus,

- Example 11.11. Let A = [~4_* J]4i andt /(A)f f > \ = eatk. Then 7r(X)TU^^ _/"i\ = (Af\ +i 2)o\22 so m = 1 and «i = 2.

Let g(A.) = «o + ofiA.. Then the defining equations for the a,-s are given by

Solving for the a,s, we find

Thus,

###### Other methods

- 1. Use etA = £~l{(sl — A)^1} and techniques for inverse Laplace transforms. This is quite effective for small-order problems, but general nonsymbolic computational techniques are numerically unstable since the problem is theoretically equivalent to knowing precisely a JCF.
- 2. Use Pade approximation. There is an extensive literature on approximating certain nonlinear functions by rational functions. The matrix analogue yields eA =

![image 134](<Matrix Analysis For Scientists and Engineers_images/imageFile134.png>)

118 Chapter 11. Linear Differential and Difference Equations

D~l(A)N(A), where D(A) = 80I + Si A H h SPAP and N(A) = v0I + vlA + • • • + vq Aq. Explicit formulas are known for the coefficients of the numerator and denominator polynomials of various orders. Unfortunately, a Fade approximation for the exponential is accurate only in a neighborhood of the origin; in the matrix case this means when || A|| is sufficiently small. This can be arranged by scaling A, say, by

multiplying it by 1/2* for sufficiently large k and using the fact that eA = (e/ { ] /2 *)A j\2*. Numerical loss of accuracy can occur in this procedure from the successive squarings.

- 3. Reduce A to (real) Schur form S via the unitary similarity U and use eA = UesUH and successive recursions up the superdiagonals of the (quasi) upper triangular matrix es.
- 4. Many methods are outlined in, for example, [19]. Reliable and efficient computation of matrix functions such as eA and log(A) remains a fertile area for research.

###### 11.2 Difference Equations

In this section we outline solutions of discrete-time analogues of the linear differential equations of the previous section. Linear discrete-time systems, modeled by systems of difference equations, exhibit many parallels to the continuous-time differential equation case, and this observation is exploited frequently.

###### 11.2.1 Homogeneous linear difference equations

- Theorem 11.12. Let A e Rnxn. The solution of the linear homogeneous system of difference equations

for k > 0 is given by

Proof: The proof is almost immediate upon substitution of (11.14) into (11.13). D

- Remark 11.13. Again, we restrict our attention only to the so-called time-invariant case, where the matrix A in (11.13) is constant and does not depend on k. We could also consider an arbitrary "initial time" ko, but since the system is time-invariant, and since we want to keep the formulas "clean" (i.e., no double subscripts), we have chosen ko = 0 for convenience.

###### 11.2.2 Inhomogeneous linear difference equations

- Theorem 11.14. Let A e Rnxn, B e Rnxm and suppose {«*}£§ « a given sequence of m-vectors. Then the solution of the inhomogeneous initial-value problem

![image 135](<Matrix Analysis For Scientists and Engineers_images/imageFile135.png>)

- 11.2. Difference Equations 119

is given by

Proof: The proof is again almost immediate upon substitution of (11.16) into (11.15). D

###### 11.2.3 Computation of matrix powers

It is clear that solution of linear systems of difference equations involves computation of Ak. One solution method, which is numerically unstable but sometimes useful for hand calculation, is to use z-transforms, by analogy with the use of Laplace transforms to compute a matrix exponential. One definition of the z-transform of a sequence {gk} is

Assuming |z| > max |A|, the z-transform of the sequence {Ak} is then given by

X€A(A)

Methods based on the JCF are sometimes useful, again mostly for small-order problems. Assume that A e M"xn and let X e R^n be such that X~1AX = /, where J is a JCF for A. Then

If A is diagonalizable, it is then easy to compute Ak via the formula Ak — XJkX l since /* is simply a diagonal matrix.

![image 136](<Matrix Analysis For Scientists and Engineers_images/imageFile136.png>)

120 Chapter 11. Linear Differential and Difference Equations

In the general case, the problem again reduces to the computation of the power of a Jordan block. To be specific, let 7, e Cpxp be a Jordan block of the form

Writing /,• = XI + N and noting that XI and the nilpotent matrix N commute, it is then straightforward to apply the binomial theorem to (XI + N)k and verify that

The symbol ( ) has the usual definition of ,(^ ., and is to be interpreted as 0 if k < q. In the case when A. is complex, a real version of the above can be worked out.

- Example 11.15. Let A = [_J-4 J]. Then

Basic analogues of other methods such as those mentioned in Section 11.1.6 can also be derived for the computation of matrix powers, but again no universally "best" method exists. For an erudite discussion of the state of the art, see [11, Ch. 18].

###### 11.3 Higher-Order Equations

It is well known that a higher-order (scalar) linear differential equation can be converted to a first-order linear system. Consider, for example, the initial-value problem

with 4>(t} a given function and n initial conditions

![image 137](<Matrix Analysis For Scientists and Engineers_images/imageFile137.png>)

Exercises 121

Here, v(m) denotes the mth derivative of y with respect to t. Define a vector x (?) e R" with components *i(0 = y(t), x2(t) = y(t), ..., xn(t) = y{n~l)(t). Then

These equations can then be rewritten as the first-order linear system

The initial conditions take the form ^(0) = c = [CQ, c\,..., CM_I] . Note that det(X7 — A) = A." + an-\Xn~l H h a\X + ao. However, the companion

matrix A in (11.19) possesses many nasty numerical properties for even moderately sized n and, as mentioned before, is often well worth avoiding, at least for computational purposes.

A similar procedure holds for the conversion of a higher-order difference equation

with n initial conditions, into a linear first-order difference equation with (vector) initial condition.

###### EXERCISES

- 1. Let P € Rnxn be a projection. Show that ep % / + 1.718P.
- 2. Suppose x, y € R" and let A = xyT. Further, let a = xTy. Show that e'A I + g(t, a)xyT, where
- 3. Let

![image 138](<Matrix Analysis For Scientists and Engineers_images/imageFile138.png>)

122 Chapter 11. Linear Differential and Difference Equations

where X e M'nx" is arbitrary. Show that

- 4. Let K denote the skew-symmetric matrix

where /„ denotes the n x n identity matrix. A matrix A e R2nx2n is said to be Hamiltonian if K~1ATK = -A and to be symplectic if K~l ATK - A - 1 .

- (a) Suppose E is Hamiltonian and let A, be an eigenvalue of H. Show that —A, must also be an eigenvalue of H.
- (b) Suppose S is symplectic and let A. be an eigenvalue of S. Show that 1 /A, must also be an eigenvalue of S.
- (c) Suppose that H is Hamiltonian and S is symplectic. Show that S~1HS must be Hamiltonian.
- (d) Suppose H is Hamiltonian. Show that eH must be symplectic.

- 5. Let a, ft € R and

Then show that

- 6. Find a general expression for
- 7. Find eM when A =

5. Let

(a) Solve the differential equation

![image 139](<Matrix Analysis For Scientists and Engineers_images/imageFile139.png>)

Exercises 123

Show that the eigenvalues of the solution X(t) of this problem are the same as those of Cf or all?.

- 11. The year is 2004 and there are three large "free trade zones" in the world: Asia (A), Europe (E), and the Americas (R). Suppose certain multinational companies have total assets of $40 trillion of which $20 trillion is in E and $20 trillion is in R. Each year half of the Americas' money stays home, a quarter goes to Europe, and a quarter goes to Asia. For Europe and Asia, half stays home and half goes to the Americas.

- (a) Find the matrix M that gives
- (b) Find the eigenvalues and right eigenvectors of M. (c) Find the distribution of the companies' assets at year k. (d) Find the limiting distribution of the $40 trillion as the universe ends, i.e., as

k —»• +00 (i.e., around the time the Cubs win a World Series). (Exercise adapted from Problem 5.3.11 in [24].)

(b) Solve the differential equation

- 9. Consider the initial-value problem

for t > 0. Suppose that A e E"x" is skew-symmetric and let a = \\XQ\\2. Show that ||*(OII2 = aforallf > 0.

- 10. Consider the n x n matrix initial-value problem

- 12. (a) Find the solution of the initial-value problem

(b) Consider the difference equation

If £0 = 1 and z\ = 2, what is the value of ZIQOO? What is the value of Zk in general?

###### This page intentionally left blank

![image 140](<Matrix Analysis For Scientists and Engineers_images/imageFile140.png>)

![image 141](<Matrix Analysis For Scientists and Engineers_images/imageFile141.png>)

- Chapter 12

###### Generalized Eigenvalue Problems

###### 12.1 The Generalized Eigenvalue/Eigenvector Problem In this chapter we consider the generalized eigenvalue problem

where A, B e C"xn. The standard eigenvalue problem considered in Chapter 9 obviously corresponds to the special case that B = I.

- Definition 12.1. A nonzero vector x e C" is a right generalized eigenvector of the pair (A, B) with A, B e CMX" if there exists a scalar A. e C, called a generalized eigenvalue, such that

Similarly, a nonzero vector y e C" is a left generalized eigenvector corresponding to an eigenvalue X if

When the context is such that no confusion can arise, the adjective "generalized" is usually dropped. As with the standard eigenvalue problem, if x [y] is a right [left] eigenvector, then so is ax [ay] for any nonzero scalar a. e C.

- Definition 12.2. The matrix A — XB is called a matrix pencil (or pencil of the matrices A and B).

As with the standard eigenvalue problem, eigenvalues for the generalized eigenvalue problem occur where the matrix pencil A — XB is singular.

- Definition 12.3. The polynomial 7r(A.) = det(A — A.5) is called the characteristic polynomial of the matrix pair (A, B). The roots ofn(X.) are the eigenvalues of the associated generalized eigenvalue problem.

- Remark 12.4. When A, B e E"xn, the characteristic polynomial is obviously real, and hence nonreal eigenvalues must occur in complex conjugate pairs.

125

![image 142](<Matrix Analysis For Scientists and Engineers_images/imageFile142.png>)

126 Chapter 12. Generalized Eigenvalue Problems

- Remark 12.5. If B = I (or in general when B is nonsingular), then n(X) is a polynomial of degree n, and hence there are n eigenvalues associated with the pencil A — XB. However, when B = I, in particular, when B is singular, there may be 0, k e n, or infinitely many eigenvalues associated with the pencil A — XB. For example, suppose

where a and ft are scalars. Then the characteristic polynomial is

and there are several cases to consider.

- Case 1: a ^ 0, ft ^ 0. There are two eigenvalues, 1 and |.
- Case 2: a = 0, f3 / 0. There are two eigenvalues, 1 and 0.
- Case 3: a = 0, f3 = 0. There is only one eigenvalue, 1 (of multiplicity 1).
- Case 4: a = 0, f3 = 0. All A e C are eigenvalues since det(A — A.B) =0.

- Definition 12.6. If del (A — XB) is not identically zero, the pencil A — XB is said to be regular; otherwise, it is said to be singular.

Note that if AA(A) n J\f(B) ^ 0, the associated matrix pencil is singular (as in Case

- 4 above). Associated with any matrix pencil A — X B is a reciprocal pencil B — n,A and cor-

responding generalized eigenvalue problem. Clearly the reciprocal pencil has eigenvalues (JL = £. It is instructive to consider the reciprocal pencil associated with the example in

- Remark 12.5. With A and B as in (12.3), the characteristic polynomial is

and there are again four cases to consider.

- Case 1: a ^ 0, ft ^ 0. There are two eigenvalues, 1 and ^.
- Case 2: a = 0, ft ^ 0. There is only one eigenvalue, 1 (of multiplicity 1).
- Case 3: a ^ 0, f3 = 0. There are two eigenvalues, 1 and 0.
- Case 4: a = 0, (3 = 0. All A 6 C are eigenvalues since det(B — uA) = 0.

At least for the case of regular pencils, it is apparent where the "missing" eigenvalues have gone in Cases 2 and 3. That is to say, there is a second eigenvalue "at infinity" for Case 3 of A — A.B, with its reciprocal eigenvalue being 0 in Case 3 of the reciprocal pencil B — nA. A similar reciprocal symmetry holds for Case 2.

While there are applications in system theory and control where singular pencils appear, only the case of regular pencils is considered in the remainder of this chapter. Note that A and/or B may still be singular. If B is singular, the pencil A — KB always has

![image 143](<Matrix Analysis For Scientists and Engineers_images/imageFile143.png>)

12.2. Canonical Forms 127

fewer than n eigenvalues. If B is nonsingular, the pencil A-A.fi always has precisely n eigenvalues, since the generalized eigenvalue problem is then easily seen to be equivalent to the standard eigenvalue problem B~lAx = Xx (or AB~lw = Xw). However, this turns out to be a very poor numerical procedure for handling the generalized eigenvalue problem if B is even moderately ill conditioned with respect to inversion. Numerical methods that work directly on A and B are discussed in standard textbooks on numerical linear algebra; see, for example, [7, SECTION 7.7] or [25, SECTION 6.7].

###### 12.2 Canonical Forms

Just as for the standard eigenvalue problem, canonical forms are available for the generalized eigenvalue problem. Since the latter involves a pair of matrices, we now deal with equivalencies rather than similarities, and the first theorem deals with what happens to eigenvalues and eigenvectors under equivalence.

- Theorem 12.7. Let A, fl, Q, Z e Cnxn with Q and Z nonsingular. Then

- 1. the eigenvalues of the problems A — XB and QAZ — XQBZ are the same (the two problems are said to be equivalent).
- 2. ifx is a right eigenvector of A—XB, then Z~lx is a right eigenvector of QAZ—XQ B Z.
- 3. ify is a left eigenvector of A —KB, then Q~Hy isa left eigenvector ofQAZ — XQBZ.

Proof:

- 1. det(QAZ-XQBZ) = det[0(A - XB)Z] = det gdet Zdet(A - XB). Since det 0 and det Z are nonzero, the result follows.
- 2. The result follows by noting that (A –yB)x - Oif andonly if Q(A-XB)Z(Z~lx) = 0.
- 3. Again, the result follows easily by noting that yH(A — XB) — 0 if and only if ( Q ~ H y ) H Q ( A – X B ) Z = Q. D

The first canonical form is an analogue of Schur's Theorem and forms, in fact, the theoretical foundation for the QZ algorithm, which is the generally preferred method for solving the generalized eigenvalue problem; see, for example, [7, SECTION 7.7] or [25, SECTION 6.7].

- Theorem 12.8. Let A, B e Cnxn. Then there exist unitary matrices Q, Z e Cnxn such that

where Ta and Tp are upper triangular.

By Theorem 12.7, the eigenvalues of the pencil A — XB are then the ratios of the diagonal elements of Ta to the corresponding diagonal elements of Tp, with the understanding that a zero diagonal element of Tp corresponds to an infinite generalized eigenvalue.

There is also an analogue of the Murnaghan-Wintner Theorem for real matrices.

![image 144](<Matrix Analysis For Scientists and Engineers_images/imageFile144.png>)

- 128 Chapter 12. Generalized Eigenvalue Problems
- Theorem 12.9. Let A, B e Rnxn. Then there exist orthogonal matrices Q, Z e R"xn such

thnt

where T is upper triangular and S is quasi-upper-triangular.

When S has a 2 x 2 diagonal block, the 2 x 2 subpencil formed with the corresponding 2x2 diagonal subblock of T has a pair of complex conjugate eigenvalues. Otherwise, real eigenvalues are given as above by the ratios of diagonal elements of S to corresponding elements of T.

There is also an analogue of the Jordan canonical form called the Kronecker canonical form (KCF). A full description of the KCF, including analogues of principal vectors and so forth, is beyond the scope of this book. In this chapter, we present only statements of the basic theorems and some examples. The first theorem pertains only to "square" regular pencils, while the full KCF in all its generality applies also to "rectangular" and singular pencils.

- Theorem 12.10. Let A, B e Cnxn and suppose the pencil A — XB is regular. Then there exist nonsingular matrices P, Q € C"x" such that

where J is a Jordan canonical form corresponding to the finite eigenvalues of A -A.fi and N is a nilpotent matrix of Jordan blocks associated with 0 and corresponding to the infinite eigenvalues of A — XB.

- Example 12.11. The matrix pencil

with characteristic polynomial (X — 2)2 has a finite eigenvalue 2 of multiplicty 2 and three infinite eigenvalues.

- Theorem 12.12 (Kronecker Canonical Form). Let A, B e Cmxn. Then there exist nonsingular matrices P e Cmxm and Q e Cnxn such that

![image 145](<Matrix Analysis For Scientists and Engineers_images/imageFile145.png>)

- 12.2. Canonical Forms 129

where N is nilpotent, both N and J are in Jordan canonical form, and L^ is the (k + 1) x k bidiagonal pencil

The /( are called the left minimal indices while the r, are called the right minimal indices. Left or right minimal indices can take the value 0.

Such a matrix is in KCF. The first block of zeros actually corresponds to LQ, LQ, LQ, LQ , LQ, where each LQ has "zero columns" and one row, while each LQ has "zero rows" and one column. The second block is L\ while the third block is L\. The next two blocks correspond to

while the nilpotent matrix N in this example is

Just as sets of eigenvectors span A-invariant subspaces in the case of the standard eigenproblem (recall Definition 9.35), there is an analogous geometric concept for the generalized eigenproblem.

- Definition 12.14. Let A, B e Wlxn and suppose the pencil A — XB is regular. Then V is a deflating subspace if

Just as in the standard eigenvalue case, there is a matrix characterization of deflating subspace. Specifically, suppose S e Rn*xk is a matrix whose columns span a ^-dimensional subspace S of Rn, i.e., R(S) = <S. Then S is a deflating subspace for the pencil A — XB if and only if there exists M e Rkxk such that

![image 146](<Matrix Analysis For Scientists and Engineers_images/imageFile146.png>)

130 Chapter 12. Generalized Eigenvalue Problems

If B = /, then (12.4) becomes dim(AV + V) = dimV, which is clearly equivalent to AV c V. Similarly, (12.5) becomes AS = SM as before. If the pencil is not regular, there is a concept analogous to deflating subspace called a reducing subspace.

###### 12.3 Application to the Computation of System Zeros Consider the linear svstem

with A € Mnxn, B € R"xm, C e Rpxn, and D € Rpxm. This linear time-invariant statespace model is often used in multivariable control theory, where x(= x(t)) is called the state vector, u is the vector of inputs or controls, and y is the vector of outputs or observables. For details, see, for example, [26].

In general, the (finite) zeros of this system are given by the (finite) complex numbers z, where the "system pencil"

drops rank. In the special case p = m, these values are the generalized eigenvalues of the (n + m) x (n + m) pencil.

###### Example 12.15. Let

Then the transfer matrix (see [26]) of this system is

which clearly has a zero at —2.8. Checking the finite eigenvalues of the pencil (12.6), we find the characteristic polynomial to be

which has a root at —2.8.

The method of finding system zeros via a generalized eigenvalue problem also works well for general multi-input, multi-output systems. Numerically, however, one must be careful first to "deflate out" the infinite zeros (infinite eigenvalues of (12.6)). This is accomplished by computing a certain unitary equivalence on the system pencil that then yields a smaller generalized eigenvalue problem with only finite generalized eigenvalues (the finite zeros).

The connection between system zeros and the corresponding system pencil is nontrivial. However, we offer some insight below into the special case of a single-input,

![image 147](<Matrix Analysis For Scientists and Engineers_images/imageFile147.png>)

- 12.4. Symmetric Generalized Eigenvalue Problems 131

single-output system. Specifically, let B = b e Rn, C = c1 e Rl x n, and D = d e R. Furthermore, let g(.s) = cr(s7 — A)~!Z? + d denote the system transfer function (matrix), and assume that g(s) can be written in the form

where TT(S) is the characteristic polynomial of A, and v(s) and TT(S) are relatively prime (i.e., there are no "pole/zero cancellations").

Suppose z € C is such that

is singular. Then there exists a nonzero solution to

or

Assuming z is not an eigenvalue of A (i.e., no pole/zero cancellations), then from (12.7) we

get

Substituting this in (12.8), we have

or g(z)y = 0 by the definition of g. Now _y ^ 0 (else x = 0 from (12.9)). Hence g(z) = 0, i.e., z is a zero of g.

###### 12.4 Symmetric Generalized Eigenvalue Problems A very important special case of the generalized eigenvalue problem

for A, B e Rnxn arises when A = A and B = B1 > 0. For example, the second-order system of differential equations

where M is a symmetric positive definite "mass matrix" and K is a symmetric "stiffness matrix," is a frequently employed model of structures or vibrating systems and yields a generalized eigenvalue problem of the form (12.10).

Since B is positive definite it is nonsingular. Thus, the problem (12.10) is equivalent to the standard eigenvalue problem B~l Ax = AJC. However, B~1A is not necessarily symmetric.

![image 148](<Matrix Analysis For Scientists and Engineers_images/imageFile148.png>)

132 Chapter 12. Generalized Eigenvalue Problems

- Example 12.16. Let A ThenB~lA

Nevertheless, the eigenvalues of B l A are always real (and are approximately 2.1926 and -3.1926 in Example 12.16).

- Theorem 12.17. Let A, B e Rnxn with A = AT and B = BT > 0. Then the generalized eigenvalue problem

has n real eigenvalues, and the n corresponding right eigenvectors can be chosen to be orthogonal with respect to the inner product (x, y)B = XTBy. Moreover, if A > 0, then the eigenvalues are also all positive.

Proof: Since B > 0, it has a Cholesky factorization B = LLT, where L is nonsingular (Theorem 10.23). Then the eigenvalue problem

can be rewritten as the equivalent problem

Letting C = L 1AL J and z = L1 x, (12.11) can then be rewritten as

Since C = CT, the eigenproblem (12.12) has n real eigenvalues, with corresponding eigenvectors zi,..., zn satisfying

Then x, = L Tzi, i € n, are eigenvectors of the original generalized eigenvalue problem and satisfy

Finally, if A = AT > 0, then C = CT > 0, so the eigenvalues are positive. D

- Example 12.18. The Cholesky factor for the matrix B in Example 12.16 is

Then it is easily checked thai

whose eigenvalues are approximately 2.1926 and —3.1926 as expected.

The material of this section can, of course, be generalized easily to the case where A and B are Hermitian, but since real-valued matrices are commonly used in most applications, we have restricted our attention to that case only.

![image 149](<Matrix Analysis For Scientists and Engineers_images/imageFile149.png>)

- 12.5. Simultaneous Diagonalization 133

###### 12.5 Simultaneous Diagonalization

Recall that many matrices can be diagonalized by a similarity. In particular, normal matrices can be diagonalized by a unitary similarity. It turns out that in some cases a pair of matrices (A, B) can be simultaneously diagonalized by the same matrix. There are many such results and we present only a representative (but important and useful) theorem here. Again, we restrict our attention only to the real case, with the complex case following in a straightforward way.

- Theorem 12.19 (Simultaneous Reduction to Diagonal Form). Let A, B e E"x" with A = AT and B = BT > 0. Then there exists a nonsingular matrix Q such that

\ 2.5.1 Simultaneous diagonalization via SVD

There are situations in which forming C = L~1AL~T as in the proof of Theorem 12.19 is numerically problematic, e.g., when L is highly ill conditioned with respect to inversion. In such cases, simultaneous reduction can also be accomplished via an SVD. To illustrate, let

where D is diagonal. In fact, the diagonal elements of D are the eigenvalues of B 1A.

Proof: Let B = LLT be the Cholesky factorization of B and setC = L~1AL~T. Since C is symmetric, there exists an orthogonal matrix P such that PTCP = D, where D is diagonal. Let Q = L~TP. Then

and

Finally, since QDQ~l = QQT AQQ~l = L-TPPTL~1A = L~TL~1A = B~1A, we haveA(D) = A(B~1A). D

Note that Q is not in general orthogonal, so it does not preserve eigenvalues of A and B individually. However, it does preserve the eigenvalues of A — XB. This can be seen directly. LetA = QTAQandB = QTBQ. Then/HA = Q~l B~l Q~T QT AQ = Q~1B~1AQ.

Theorem 12.19 is very useful for reducing many statements about pairs of symmetric matrices to "the diagonal case." The following is typical.

- Theorem 12.20. Let A, B e M"xn be positive definite. Then A > B if and only if B~l > A-1.

Proof: By Theorem 12.19, there exists Q e E"x" such that QT AQ = D and QT BQ = I, where D is diagonal. Now D > 0 by Theorem 10.31. Also, since A > B, by Theorem 10.21 we have that QTAQ > QTBQ, i.e., D > I. But then D"1 < / (this is trivially true since the two matrices are diagonal). Thus, QD~l QT < QQT, i.e., A~l < B~l. D

![image 150](<Matrix Analysis For Scientists and Engineers_images/imageFile150.png>)

- where D is diagonal and P is orthogonal, but in writing A — PDDP~ ~ = PD(PD)~ ~ T with D diagonal, D may have pure imaginary elements.

134 Chapter 12. Generalized Eigenvalue Problems

us assume that both A and B are positive definite. Further, let A = LALTA and B — LsLTB be Cholesky factorizations of A and B, respectively. Compute the SVD

- where E e R£x" is diagonal. Then the matrix Q = LBTU performs the simultaneous diagonalization. To check this, note that

while

- Remark 12.21. The SVD in (12.13) can be computed without explicitly forming the indicated matrix product or the inverse by using the so-called generalized singular value decomposition (GSVD). Note that

and thus the singular values of LB LA can be found from the eigenvalue problem

Letting x = LB z we see that (12.14) can be rewritten in the form LALAx = XLBz = ALgL^Lg7z, which is thus equivalent to the generalized eigenvalue problem

The problem (12.15) is called a generalized singular value problem and algorithms exist to solve it (and hence equivalently (12.13)) via arithmetic operations performed only on LA and LB separately, i.e., without forming the products LALTA or LBLTB explicitly; see, for example, [7, SECTION 8.7.3]. This is analogous to finding the singular values of a matrix M by operations performed directly on M rather than by forming the matrix MT M and solving the eigenproblem MT MX = Xx.

- Remark 12.22. Various generalizations of the results in Remark 12.21 are possible, for example, when A = AT > 0. The case when A is symmetric but indefinite is not so straightforward, at least in real arithmetic. For example, A can be written as A = PDPT,

![image 151](<Matrix Analysis For Scientists and Engineers_images/imageFile151.png>)

- 12.6. Higher-Order Eigenvalue Problems 135

###### 12.6 Higher-Order Eigenvalue Problems Consider the second-order system of differential equations

where q(t} e W1 and M, C, K e Rnxn. Assume for simplicity that M is nonsingular. Suppose, by analogy with the first-order case, that we try to find a solution of (12.16) of the form q(t) = ext p, where the n-vector p and scalar A. are to be determined. Substituting in (12.16) we get

or, since

To get a nonzero solution /?, we thus seek values of A. for which the matrix A.2M + A.C + K is singular. Since the determinantal equation

yields a polynomial of degree 2rc, there are 2n eigenvalues for the second-order (or quadratic) eigenvalue problem A.2M + A.C + K.

A special case of (12.16) arises frequently in applications: M = I, C = 0, and K = KT. Suppose K has eigenvalues

Let a>k = |fjik 12 • Then the 2n eigenvalues of the second-order eigenvalue problem A.2/ + K

are

If r = n (i.e., K = KT > 0), then all solutions of q + Kq = 0 are oscillatory.

###### 12.6.1 Conversion to first-order form

Let x\ = q and \i = q. Then (12.16) can be written as a first-order system (with block companion matrix)

where x(t) €. E2". If M is singular, or if it is desired to avoid the calculation of M l because M is too ill conditioned with respect to inversion, the second-order problem (12.16) can still be converted to the first-order generalized linear system

![image 152](<Matrix Analysis For Scientists and Engineers_images/imageFile152.png>)

136 Chapter 12. Generalized Eigenvalue Problems

Many other first-order realizations are possible. Some can be useful when M, C, and/or K have special symmetry or skew-symmetry properties that can exploited.

Higher-order analogues of (12.16) involving, say, the kth derivative of q, lead naturally to higher-order eigenvalue problems that can be converted to first-order form using aknxkn block companion matrix analogue of (11.19). Similar procedures hold for the general k\horder difference equation

which can be converted to various first-order systems of dimension kn.

###### EXERCISES

1. Suppose A e Rnx" and D e R™xm. Show that the finite generalized eigenvalues of the pencil

are the eigenvalues of the matrix A — BD 1C.

2. Let F, G € CMX". Show that the nonzero eigenvalues of FG and GF are the same. Hint: An easy "trick proof is to verify that the matrices

are similar via the similarity transformation

- 3. Let F e Cnxm, G e Cmx". Are the nonzero singular values of FG and GF the same?
- 4. Suppose A € Rnxn, B e Rn*m, and C e Ewx". Show that the generalized eigenvalues of the pencils

and

are identical for all F 6 E"1*" and all G G R"xm. Hint: Consider the equivalence

(A similar result is also true for "nonsquare" pencils. In the parlance of control theory, such results show that zeros are invariant under state feedback or output injection.)

![image 153](<Matrix Analysis For Scientists and Engineers_images/imageFile153.png>)

Exercises 137

5. Another family of simultaneous diagonalization problems arises when it is desired that the simultaneous diagonalizing transformation Q operates on matrices A, B e ]Rnx" in such a way that Q~l AQ~T and QTBQ are simultaneously diagonal. Such a transformation is called contragredient. Consider the case where both A and B are positive definite with Cholesky factorizations A = L&LTA and B = L#Lg, respectively, and let UWT be an SVD of LTBLA.

- (a) Show that Q = LA V£~5 is a contragredient transformation that reduces both A and B to the same diagonal matrix.
- (b) Show that Q~l = ^~^UT LTB.
- (c) Show that the eigenvalues of A B are the same as those of E2 and hence are positive.

###### This page intentionally left blank

![image 154](<Matrix Analysis For Scientists and Engineers_images/imageFile154.png>)

![image 155](<Matrix Analysis For Scientists and Engineers_images/imageFile155.png>)

- Chapter 13

###### Kronecker Products

###### 13.1 Definition and Examples

- Definition 13.1. Let A e Rmx", B e Rpxq. Then the Kronecker product (or tensor product) of A and B is defined as the matrix

Obviously, the same definition holds if A and B are complex-valued matrices. We restrict our attention in this chapter primarily to real-valued matrices, pointing out the extension to the complex case only where it is not obvious.

###### Example 13.2.

Note that B<g> A / A <g> B.

- 2. Foranyfl e!FX(7, /2<8>fl = [o l\

Replacing I2 by /„ yields a block diagonal matrix with n copies of B along the diagonal.

- 3. Let B be an arbitrary 2x2 matrix. Then

139

![image 156](<Matrix Analysis For Scientists and Engineers_images/imageFile156.png>)

140 Chapter 13. Kronecker Products

The extension to arbitrary B and /„ is obvious.

- 4. Let Jt € Rm, y e R". Then
- 5. Let* eRm, y eR". Then

###### 13.2 Properties of the Kronecker Product

- Theorem 13.3. Let A e Rmx", 5 e Rrxi, C e R"x^ and D e Rsxt. Then

Proof: Simply verify that

- Theorem 13.4. For all A and B,

Proof: For the proof, simply verify using the definitions of transpose and Kronecker product. D

Corollary 13.5. If A e R"xn and B e Rmxm are symmetric, then A® B is symmetric.

- Theorem 13.6. If A and B are nonsingular, Proof: Using Theorem 13.3, simply note that

![image 157](<Matrix Analysis For Scientists and Engineers_images/imageFile157.png>)

- 13.2. Properties of the Kronecker Product 141

- Theorem 13.7. If A e IR"xn am/ B eRmxm are normal, then A® B is normal. Proof:

Corollary 13.8. If A € E"xn is orthogonal and B e Mmxm 15 orthogonal, then A <g> B is orthogonal.

- Example 13.9. Let A and B - Then it is easily seen that

A is orthogonal with eigenvalues e±j9 and B is orthogonal with eigenvalues e±j(i>. The 4x4 matrix A ® 5 is then also orthogonal with eigenvalues e^'^+'W and e±^(6>~^>\

Theorem 13.10. Lgf A G Emx" have a singular value decomposition l/^E^Vj an^ /ef fi e ^pxq have a singular value decomposition UB^B^B- Then

yields a singular value decomposition of A <8> B (after a simple reordering of the diagonal elements O/£A <8> £5 and the corresponding right and left singular vectors).

Corollary 13.11. Let A e R™x" have singular values a\ > • • • > ar > 0 and let B e have singular values T\ > • • • > TS > 0. Then A <g) B (or B <8> A) has rs singular values ^iT\ > • • • > ffrTs > Qand

Theorem 13.12. Let A e Rnx" have eigenvalues A.,-, / e n, and let B e Rmxw /zave eigenvalues jJij, 7 € m. TTzen ?/ze mn eigenvalues of A® B are

Moreover, if x\, ..., xp are linearly independent right eigenvectors of A corresponding to A-i,..., A.p (p < n), and zi, • • •, zq are linearly independent right eigenvectors of B corresponding to JJL\ , ..., \Juq (q < m), then ;c, <8> Zj € ffi.m" are linearly independent right eigenvectors of A® B corresponding to A.,/u,7, i e /?, 7 e q.

Proof: The basic idea of the proof is as follows:

If A and B are diagonalizable in Theorem 13.12, we can take p = n and q —m and thus get the complete eigenstructure of A <8> B. In general, if A and fi have Jordan form

![image 158](<Matrix Analysis For Scientists and Engineers_images/imageFile158.png>)

142 Chapter 13. Kronecker Products

decompositions given by P~l AP = JA and Q~] BQ = JB, respectively, then we get the following Jordan-like structure:

Note that JA® JB, while upper triangular, is generally not quite in Jordan form and needs further reduction (to an ultimate Jordan form that also depends on whether or not certain eigenvalues are zero or nonzero).

A Schur form for A ® B can be derived similarly. For example, suppose P and Q are unitary matrices that reduce A and 5, respectively, to Schur (triangular) form, i.e., PHAP = TA and QHBQ = TB (and similarly if P and Q are orthogonal similarities reducing A and B to real Schur form). Then

Corollary 13.13. Let A e Rnxn and B e Rmxm. Then

- Definition 13.14. Let A e Rnxn and B e Rmxm. Then the Kronecker sum (or tensor sum)

of A and B, denoted A © B, is the mn x mn matrix (Im <g> A) + (B ® /„). Note that, in general, A ® B ^ B © A.

###### Example 13.15.

###### 1. Let

Then

The reader is invited to compute B 0 A = (/3 ® B) + (A<g> /2) and note the difference with A © B.

![image 159](<Matrix Analysis For Scientists and Engineers_images/imageFile159.png>)

- 13.2. Properties of the Kronecker Product 143

2. Recall the real JCF

where M =

Then J can be written in the very compact form J = (4 <8> M) + (E^®l2) = M 0 Ek. Theorem 13.16. Let A e E"x" have eigenvalues A,-,i e n, and let B e Rmx'" have eigenvalues /z;, 7 e ra. TTzen r/ze Kronecker sum A® B = (Im (g> A) + (B <g> /„) /za^ ran e/genva/wes

Moreover, if x\,... ,xp are linearly independent right eigenvectors of A corresponding to AI, ..., Xp (p < n), and z\, ..., zq are linearly independent right eigenvectors of B corresponding to f j i \ , . . . , f^q (q < ra), then Zj <8> Xi € W1" are linearly independent right eigenvectors of A® B corresponding to A., + [ij, i € p, j e q.

Proof: The basic idea of the proof is as follows:

If A and B are diagonalizable in Theorem 13.16, we can take p = n and q = m and thus get the complete eigenstructure of A 0 B. In general, if A and B have Jordan form decompositions given by P~1AP = JA and Q"1 BQ = JB, respectively, then

is a Jordan-like structure for A © B.

![image 160](<Matrix Analysis For Scientists and Engineers_images/imageFile160.png>)

144 Chapter 13. Kronecker Products

A Schur form for A © B can be derived similarly. Again, suppose P and Q are unitary matrices that reduce A and B, respectively, to Schur (triangular) form, i.e., PHAP = TA and QHBQ = TB (and similarly if P and Q are orthogonal similarities reducing A and B to real Schur form). Then

((Q ® /„)(/« ® P)]"[(/m <8> A) + (B ® /B)][(e (g) /„)(/„, ® P)] = (/m <8> rA) + (7* (g) /„), where [(Q <8> /„)(/« ® P)] = (<2 ® P) is unitary by Theorem 13.3 and Corollary 13.8.

###### 13.3 Application to Sylvester and Lyapunov Equations In this section we study the linear matrix equation

where A e R"x", B e Rmxm, and C e M"xm. This equation is now often called a Sylvester equation in honor of J.J. Sylvester who studied general linear matrix equations of the form

A special case of (13.3) is the symmetric equation

obtained by taking B = AT. When C is symmetric, the solution X e Wx" is easily shown also to be symmetric and (13.4) is known as a Lyapunov equation. Lyapunov equations arise naturally in stability theory.

The first important question to ask regarding (13.3) is, When does a solution exist? By writing the matrices in (13.3) in terms of their columns, it is easily seen by equating the z'th columns that

These equations can then be rewritten as the mn x mn linear system

The coefficient matrix in (13.5) clearly can be written as the Kronecker sum (Im * A) + (BT ® /„). The following definition is very helpful in completing the writing of (13.5) as an "ordinary" linear system.

![image 161](<Matrix Analysis For Scientists and Engineers_images/imageFile161.png>)

- 13.3. Application to Sylvester and Lyapunov Equations 145

- Definition 13.17. Let c( € E.n denote the columns ofC e Rnxm so that C = [n,..., cm}. Then vec(C) is defined to be the mn-vector formed by stacking the columns ofC on top of

one another, i.e., vec(C) =

Using Definition 13.17, the linear system (13.5) can be rewritten in the form

There exists a unique solution to (13.6) if and only if [(Im ® A) + (BT ® /„)] is nonsingular. But [(Im <8> A) + (BT (g) /„)] is nonsingular if and only if it has no zero eigenvalues. From Theorem 13.16, the eigenvalues of [(/m <g> A) + (BT <8> /„)] are A., + IJLJ, where A,,- e A (A), i e n_, and ^j e A(fi), j e m. We thus have the following theorem.

- Theorem 13.18. Let A e Rnxn, B G Rmxm, and C e R"xm. 77ie/i the Sylvester equation

has a unique solution if and only if A and —B have no eigenvalues in common.

Sylvester equations of the form (13.3) (or symmetric Lyapunov equations of the form (13.4)) are generally not solved using the mn x mn "vec" formulation (13.6). The most commonly preferred numerical algorithm is described in [2]. First A and B are reduced to (real) Schur form. An equivalent linear system is then solved in which the triangular form of the reduced A and B can be exploited to solve successively for the columns of a suitably transformed solution matrix X. Assuming that, say, n > m, this algorithm takes only O(n3) operations rather than the O(n6) that would be required by solving (13.6) directly with Gaussian elimination. A further enhancement to this algorithm is available in [6] whereby the larger of A or B is initially reduced only to upper Hessenberg rather than triangular Schur form.

The next few theorems are classical. They culminate in Theorem 13.24, one of many elegant connections between matrix theory and stability theory for differential equations.

- Theorem 13.19. Let A e Rnxn, B e Rmxm, and C e Rnxm. Suppose further that A and B are asymptotically stable (a matrix is asymptotically stable if all its eigenvalues have real parts in the open left half-plane). Then the (unique) solution of the Sylvester equation

can be written as

Proof: Since A and B are stable, A., (A) + A;-(B) ^ 0 for all i, j so there exists a unique solution to(13.8)by Theorem 13.18. Now integrate the differential equation X = AX + XB (with X(0) = C) on [0, +00):

![image 162](<Matrix Analysis For Scientists and Engineers_images/imageFile162.png>)

146 Chapter 13. Kronecker Products

Using the results of Section 11.1.6, it can be shown easily that lim e = lim e = 0.

r—>+oo t—v+oo

Hence, using the solution X(t) = etACetB from Theorem 11.6, we have that lim X(t) — 0.

/—<-+3C

Substituting in (13.10) we have

and so X

- Remark 13.20. An equivalent condition for the existence of a unique solution to AX + XB = C is that [ J _cfi ] be similar to [ J _°B ] (via the similarity [ J _* ]).

Theorem 13.21. Lef A, C e R"x". TTzen r/ze Lyapunov equation

has a unique solution if and only if A and —AT have no eigenvalues in common. If C is symmetric and (13.11) has a unique solution, then that solution is symmetric.

- Remark 13.22. If the matrix A e Wxn has eigenvalues A.I ,...,!„, then — AT has eigen-

values —A.], ..., —kn. Thus, a sufficient condition that guarantees that A and — AT have no common eigenvalues is that A be asymptotically stable. Many useful results exist concerning the relationship between stability and Lyapunov equations. Two basic results due to Lyapunov are the following, the first of which follows immediately from Theorem 13.19.

- Theorem 13.23. Let A,C e R"x" and suppose further that A is asymptotically stable. Then the (unique) solution of the Lyapunov equation

can be written as

- Theorem 13.24. A matrix A e R"x" is asymptotically stable if and only if there exists a positive definite solution to the Lyapunov equation

where C -

Proof: Suppose A is asymptotically stable. By Theorems 13.21 and 13.23 a solution to (13.13) exists and takes the form (13.12). Now let v be an arbitrary nonzero vector in E". Then

![image 163](<Matrix Analysis For Scientists and Engineers_images/imageFile163.png>)

13.3. Application to Sylvester and Lyapunov Equations 147

Since — C > 0 and etA is nonsingular for all t, the integrand above is positive. Hence vTXv > 0 and thus X is positive definite.

Conversely, suppose X = XT > 0 and let A. e A (A) with corresponding left eigenvector y. Then

Since yHXy > 0, we must have A + A = 2 R e A < 0 . Since A was arbitrary, A must be asymptotically stable. D

- Remark 13.25. The Lyapunov equation AX + XAT = C can also be written using the vec notation in the equivalent form

A subtle point arises when dealing with the "dual" Lyapunov equation ATX + XA = C. The equivalent "vec form" of this equation is

However, the complex-valued equation AHX + XA = C is equivalent to

The vec operator has many useful properties, most of which derive from one key result.

- Theorem 13.26. For any three matrices A, B, and C for which the matrix product ABC is defined,

Proof: The proof follows in a fairly straightforward fashion either directly from the definitions or from the fact that vec(;t;yr) = y <8> x. D

An immediate application is to the derivation of existence and uniqueness conditions for the solution of the simple Sylvester-like equation introduced in Theorem 6.11.

- Theorem 13.27. Let A e Rmxn, B e Rpx(}, and C e Rmxq. Then the equation

has a solution X e R.nxp if and only ifAA+CB+B = C, in which case the general solution is of the form

where Y e Rnxp is arbitrary. The solution of (13.14) is unique if BB+ ® A+A = I. Proof: Write (13.14) as

![image 164](<Matrix Analysis For Scientists and Engineers_images/imageFile164.png>)

148 Chapter 13. Kronecker Products

by Theorem 13.26. This "vector equation" has a solution if and only if

It is a straightforward exercise to show that (M ® N)+ = M+ <8> N+. Thus, (13.16) has a solution if and only if

and hence if and only if AA+CB+B = C. The general solution of (13.16) is then given by

where Y is arbitrary. This equation can then be rewritten in the form

or, using Theorem 13.26,

The solution is clearly unique if BB+ <8> A+A = I. D

###### EXERCISES

- 1. For any two matrices A and B for which the indicated matrix product is defined, show that (vec(A))r(vec(fl)) = Tr(Ar£). In particular, if B e Rnxn, then Tr(fl) = vec(/Jrvec(fl).
- 2. Prove that for all matrices A and B, (A ® B)+ = A+ ® B+.
- 3. Show that the equation AX B = C has a solution for all C if A has full row rank and B has full column rank. Also, show that a solution, if it exists, is unique if A has full column rank and B has full row rank. What is the solution in this case?
- 4. Show that the general linear equation

can be written in the form

![image 165](<Matrix Analysis For Scientists and Engineers_images/imageFile165.png>)

Exercises 149

- 5. Let x € Mm and y e E". Show that *r <8> y = yxT.
- 6. Let A e R"xn and £ e Mmxm.

- (a) Show that ||A <8> B||2 = ||A||2||£||2.
- (b) What is ||A ® B\\F in terms of the Frobenius norms of A and B? Justify your answer carefully.
- (c) What is the spectral radius of A <8> B in terms of the spectral radii of A and B? Justify your answer carefully.

- 7. Let A, 5 eR"x".

- (a) Show that (/ ® A)* = / <8> A* and (fl <g> /)* = Bfc ® / for all integers &.
- (b) Show that el®A = I <g) eA and e5®7 = eB (g) /.
- (c) Show that the matrices / (8) A and B ® / commute.
- (d) Show that

(Note: This result would look a little "nicer" had we defined our Kronecker sum the other way around. However, Definition 13.14 is conventional in the literature.)

- 8. Consider the Lyapunov matrix equation (13.11) with

and C the symmetric matrix

Clearly

is a symmetric solution of the equation. Verify that

is also a solution and is nonsymmetric. Explain in light of Theorem 13.21.

- 9. Block Triangularization: Let

where A e Rnxn and D e Rmxm. It is desired to find a similarity transformation of the form

such that T l ST is block upper triangular.

![image 166](<Matrix Analysis For Scientists and Engineers_images/imageFile166.png>)

150 Chapter 13. Kronecker Products

(a) Show that S is similar to

###### if X satisfies the so-called matrix Riccati equation

(b) Formulate a similar result for block lower triangularization of S.

###### 10. Block Diagonalization: Let

where A e Rnxn and D E Rmxm. It is desired to find a similarity transformation of the form

such that T l ST is block diagonal,

- (a) Show that S is similar to

if Y satisfies the Sylvester equation

- (b) Formulate a similar result for block diagonalization of

![image 167](<Matrix Analysis For Scientists and Engineers_images/imageFile167.png>)

###### Bibliography

- [1] Albert, A., Regression and the Moore-Penrose Pseudoinverse, Academic Press, New York, NY, 1972.
- [2] Bartels, R.H., and G.W. Stewart, "Algorithm 432. Solution of the Matrix Equation AX + XB = C," Cornm. ACM, 15(1972), 820-826.
- [3] Bellman, R., Introduction to Matrix Analysis, Second Edition, McGraw-Hill, New York, NY, 1970.
- [4] Bjorck, A., Numerical Methods for Least Squares Problems, SIAM, Philadelphia, PA, 1996.
- [5] Cline, R.E., "Note on the Generalized Inverse of the Product of Matrices," SIAM Rev., 6(1964), 57–58.
- [6] Golub, G.H., S. Nash, and C. Van Loan, "A Hessenberg-Schur Method for the Problem AX + XB = C," IEEE Trans. Autom. Control, AC-24(1979), 909-913.
- [7] Golub, G.H., and C.F. Van Loan, Matrix Computations, Third Edition, Johns Hopkins Univ. Press, Baltimore, MD, 1996.
- [8] Golub, G.H., and J.H. Wilkinson, "Ill-Conditioned Eigensystems and the Computation of the Jordan Canonical Form," SIAM Rev., 18(1976), 578-619.
- [9] Greville, T.N.E., "Note on the Generalized Inverse of a Matrix Product," SIAM Rev., 8(1966), 518–521 [Erratum, SIAM Rev., 9(1967), 249].
- [10] Halmos, PR., Finite-Dimensional Vector Spaces, Second Edition, Van Nostrand, Princeton, NJ, 1958.
- [11] Higham, N.J., Accuracy and Stability of'Numerical Algorithms, Second Edition, SIAM, Philadelphia, PA, 2002.
- [12] Horn, R.A., and C.R. Johnson, Matrix Analysis, Cambridge Univ. Press, Cambridge, UK, 1985.
- [13] Horn, R.A., and C.R. Johnson, Topics in Matrix Analysis, Cambridge Univ. Press, Cambridge, UK, 1991.

![image 168](<Matrix Analysis For Scientists and Engineers_images/imageFile168.png>)

152 Bibliography

- [14] Kenney, C, and A.J. Laub, "Controllability and Stability Radii for Companion Form Systems," Math, of Control, Signals, and Systems, 1(1988), 361-390.
- [15] Kenney, C.S., and A.J. Laub, "The Matrix Sign Function," IEEE Trans. Autom. Control, 40(1995), 1330–1348.
- [16] Lancaster, P., and M. Tismenetsky, The Theory of Matrices, Second Edition with Applications, Academic Press, Orlando, FL, 1985.
- [17] Laub, A.J., "A Schur Method for Solving Algebraic Riccati Equations," IEEE Trans.. Autom. Control, AC-24( 1979), 913–921.
- [18] Meyer, C.D., Matrix Analysis and Applied Linear Algebra, SIAM, Philadelphia, PA, 2000.
- [19] Moler, C.B., and C.F. Van Loan, "Nineteen Dubious Ways to Compute the Exponential of a Matrix," SIAM Rev., 20(1978), 801-836.
- [20] Noble, B., and J.W. Daniel, Applied Linear Algebra, Third Edition, Prentice-Hall, Englewood Cliffs, NJ, 1988.
- [21] Ortega, J., Matrix Theory. A Second Course, Plenum, New York, NY, 1987.
- [22] Penrose, R., "A Generalized Inverse for Matrices," Proc. Cambridge Philos. Soc., 51(1955), 406–413.
- [23] Stewart, G. W., Introduction to Matrix Computations, Academic Press, New York, NY, 1973.
- [24] Strang, G., Linear Algebra and Its Applications, Third Edition, Harcourt Brace Jovanovich, San Diego, CA, 1988.
- [25] Watkins, D.S., Fundamentals of Matrix Computations, Second Edition, WileyInterscience, New York, 2002.
- [26] Wonham, W.M., Linear Multivariable Control. A Geometric Approach, Third Edition, Springer-Verlag, New York, NY, 1985.

![image 169](<Matrix Analysis For Scientists and Engineers_images/imageFile169.png>)

###### Index

congruence, 103 conjugate transpose, 2 contragredient transformation, 137 controllability, 46

A–invariant subspace, 89

matrix characterization of, 90 algebraic multiplicity, 76 angle between vectors, 58

defective, 76 degree

basis, 11 natural, 12

of a principal vector, 85

block matrix, 2 definiteness of, 104 diagonalization, 150 inverse of, 48 LU factorization, 5 triangularization, 149

determinant, 4 of a block matrix, 5 properties of, 4–6

dimension, 12 direct sum

of subspaces, 13 domain, 17 eigenvalue, 75

C", 1

(pmxn i (p/nxn 1

invariance under similarity transfor-

Cauchy–Bunyakovsky–Schwarz Inequal-

mation, 81 elementary divisors, 84 equivalence transformation, 95

ity, 58

Cayley–Hamilton Theorem, 75 chain

orthogonal, 95 unitary, 95

of eigenvectors, 87

characteristic polynomial of a matrix, 75 of a matrix pencil, 125

equivalent generalized eigenvalue prob-

lems, 127 equivalent matrix pencils, 127 exchange matrix, 39, 89 exponential of a Jordan block, 91, 115 exponential of a matrix, 81, 109

Cholesky factorization, 101 co–domain, 17 column

rank, 23 vector, 1 companion matrix inverse of, 105 pseudoinverse of, 106 singular values of, 106 singular vectors of, 106

computation of, 114–118 inverse of, 110 properties of, 109–112

field, 7 four fundamental subspaces, 23 function of a matrix, 81

complement of a subspace, 13 orthogonal, 21

generalized eigenvalue, 125 generalized real Schur form, 128

![image 170](<Matrix Analysis For Scientists and Engineers_images/imageFile170.png>)

154 Index

generalized Schur form, 127 generalized singular value decomposition,

Kronecker product, 139 determinant of, 142 eigenvalues of, 141 eigenvectors of, 141 products of, 140 pseudoinverse of, 148 singular values of, 141 trace of, 142 transpose of, 140

134

geometric multiplicity, 76

Holder Inequality, 58 Hermitian transpose, 2 higher–order difference equations

conversion to first–order form, 121 higher–order differential equations

Kronecker sum, 142 eigenvalues of, 143 eigenvectors of, 143 exponential of, 149

conversion to first–order form, 120 higher–order eigenvalue problems

conversion to first–order form, 136

i, 2

leading principal submatrix, 100 left eigenvector, 75 left generalized eigenvector, 125 left invertible, 26 left nullspace, 22 left principal vector, 85 linear dependence, 10 linear equations

idempotent, 6, 51 identity matrix, 4 inertia, 103 initial–value problem, 109

for higher–order equations, 120 for homogeneous linear difference

equations, 118 for homogeneous linear differential equations, 112 for inhomogeneous linear difference equations, 119 for inhomogeneous linear differential equations, 112

characterization of all solutions, 44 existence of solutions, 44 uniqueness of solutions, 45

linear independence, 10 linear least squares problem, 65 general solution of, 66 geometric solution of, 67 residual of, 65 solution via QR factorization, 71 solution via singular value decom-

inner product complex, 55 complex Euclidean, 4 Euclidean, 4, 54 real, 54 usual, 54 weighted, 54

position, 70 statement of, 65 uniqueness of solution, 66

invariant factors, 84 inverses

linear regression, 67 linear transformation, 17

of block matrices, 47

co–domain of, 17 composition of, 19 domain of, 17 invertible, 25 left invertible, 26 matrix representation of, 18 nonsingular, 25 nullspace of, 20

7, 2

Jordan block, 82 Jordan canonical form (JCF), 82

Kronecker canonical form (KCF), 129 Kronecker delta, 20

![image 171](<Matrix Analysis For Scientists and Engineers_images/imageFile171.png>)

Index 155

/?–, 60

range of, 20 right invertible, 26

consistent, 61 Frobenius, 60 induced by a vector norm, 61 mixed, 60 mutually consistent, 61 relations among, 61 Schatten, 60 spectral, 60 subordinate to a vector norm, 61 unitarily invariant, 62

LU factorization, 6

block, 5 Lyapunov differential equation, 113 Lyapunov equation, 144

and asymptotic stability, 146 integral form of solution, 146 symmetry of solution, 146 uniqueness of solution, 146

matrix asymptotically stable, 145 best rank k approximation to, 67 companion, 105 defective, 76 definite, 99 derogatory, 106 diagonal, 2 exponential, 109 Hamiltonian, 122 Hermitian, 2 Householder, 97 indefinite, 99 lower Hessenberg, 2 lower triangular, 2 nearest singular matrix to, 67 nilpotent, 115 nonderogatory, 105 normal, 33, 95 orthogonal, 4 pentadiagonal, 2 quasi–upper–triangular, 98 sign of a, 91 square root of a, 101 symmetric, 2 symplectic, 122 tridiagonal, 2 unitary, 4 upper Hessenberg, 2 upper triangular, 2

matrix pencil, 125 equivalent, 127 reciprocal, 126 regular, 126 singular, 126 matrix sign function, 91 minimal polynomial, 76 monic polynomial, 76 Moore–Penrose pseudoinverse, 29 multiplication

matrix–matrix, 3 matrix–vector, 3

Murnaghan–Wintner Theorem, 98

negative definite, 99 negative invariant subspace, 92 nonnegative definite, 99

criteria for, 100 nonpositive definite, 99 norm

induced, 56 natural, 56 normal equations, 65 normed linear space, 57 nullity, 24 nullspace, 20

left, 22 right, 22

observability, 46 one–to–one (1–1), 23

matrix exponential, 81, 91, 109 matrix norm, 59

conditions for, 25 onto, 23

- 1–.60
- 2–, 60 oo–, 60

conditions for, 25

![image 172](<Matrix Analysis For Scientists and Engineers_images/imageFile172.png>)

156 Index

Q –orthogonality, 55 QR factorization, 72

orthogonal complement, 21 matrix, 4 projection, 52 subspaces, 14 vectors, 4, 20

TO"IK , 11

M mxn , 1i M mxnr ' 1 Mnxn 1

orthonormal vectors, 4, 20

n ' '

range, 20 range inclusion

outer product, 19 and Kronecker product, 140 exponential of, 121 pseudoinverse of, 33 singular value decomposition of, 41 various matrix norms of, 63

characterized by pseudoinverses, 33 rank, 23

column, 23

row, 23

rank–one matrix, 19 rational canonical form, 104 Rayleigh quotient, 100 reachability, 46 real Schur canonical form, 98 real Schur form, 98 reciprocal matrix pencil, 126 reconstructibility, 46 regular matrix pencil, 126 residual, 65 resolvent, 111 reverse–order identity matrix, 39, 89 right eigenvector, 75 right generalized eigenvector, 125 right invertible, 26 right nullspace, 22 right principal vector, 85

pencil equivalent, 127 of matrices, 125 reciprocal, 126 regular, 126 singular, 126

Penrose theorem, 30 polar factorization, 41 polarization identity, 57 positive definite, 99

criteria for, 100 positive invariant subspace, 92 power (Kth) of a Jordan block, 120 powers of a matrix

computation of, 119–120 principal submatrix, 100 projection

row

rank, 23 vector, 1

oblique, 51 on four fundamental subspaces, 52 orthogonal, 52

Schur canonical form, 98

generalized, 127 Schur complement, 6, 48, 102, 104 Schur Theorem, 98 Schur vectors, 98 second–order eigenvalue problem, 135

pseudoinverse, 29 four Penrose conditions for, 30 of a full–column–rank matrix, 30 of a full–row–rank matrix, 30 of a matrix product, 32 of a scalar, 31 of a vector, 31 uniqueness, 30 via singular value decomposition, 38

conversion to first–order form, 135 Sherman–Morrison–Woodbury formula,

48

signature, 103 similarity transformation, 95

Pythagorean Identity, 59

and invariance of eigenvalues, h

![image 173](<Matrix Analysis For Scientists and Engineers_images/imageFile173.png>)

Index 157

Sylvester's Law of Inertia, 103 symmetric generalized eigenvalue prob-

orthogonal, 95 unitary, 95

lem, 131

simple eigenvalue, 85 simultaneous diagonalization, 133

total least squares, 68 trace, 6 transpose, 2

via singular value decomposition, 134 singular matrix pencil, 126 singular value decomposition (SVD), 35 and bases for four fundamental

characterization by inner product, 54 of a block matrix, 2

subspaces, 38 and pseudoinverse, 38 and rank, 38 characterization of a matrix factor-

triangle inequality

for matrix norms, 59 for vector norms, 57

unitarily invariant

ization as, 37 dyadic expansion, 38 examples, 37 full vs. compact, 37 fundamental theorem, 35 nonuniqueness, 36

matrix norm, 62 vector norm, 58

variation of parameters, 112

vec

of a matrix, 145 of a matrix product, 147

singular values, 36 singular vectors

vector norm, 57

left, 36 right, 36

l–, 57 2–, 57 oo–, 57

span, 11 spectral radius, 62, 107 spectral representation, 97 spectrum, 76 subordinate norm, 61 subspace, 9

P–, 51

equivalent, 59 Euclidean, 57 Manhattan, 57 relations among, 59 unitarily invariant, 58 weighted, 58 weighted p–, 58

A–invariant, 89 deflating, 129 reducing, 130

vector space, 8 dimension of, 12

subspaces complements of, 13 direct sum of, 13 equality of, 10 four fundamental, 23 intersection of, 13 orthogonal, 14

vectors, 1 column, 1 linearly dependent, 10 linearly independent, 10 orthogonal, 4, 20 orthonormal, 4, 20

row, 1

sum of, 13

span of a set of, 11 zeros

Sylvester differential equation, 113 Sylvester equation, 144

integral form of solution, 145 uniqueness of solution, 145

of a linear dynamical system, 130
