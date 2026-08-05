# Cross-section progression — Calculus I (OpenStax Calculus Vol. 1), Calculus II (OpenStax Calculus Vol. 2), Calculus III (OpenStax Calculus Vol. 3)

Section-level progression from OpenStax structure (chapter/section order + learning objectives).
Skill-level dependency edges are a later stage.

```mermaid
flowchart TD
  subgraph calculus_volume_1 [Calculus I (OpenStax Calculus Vol. 1)]
    subgraph calculus_volume_1_ch1 ["Ch 1: Functions and Graphs"]
      calculus_volume_1_c1intro["Functions and Graphs (overview)"]
      calculus_volume_1_c1s1["Review of Functions"]
      calculus_volume_1_c1s2["Basic Classes of Functions"]
      calculus_volume_1_c1s3["Trigonometric Functions"]
      calculus_volume_1_c1s4["Inverse Functions"]
      calculus_volume_1_c1s5["Exponential and Logarithmic Functions"]
    end
    subgraph calculus_volume_1_ch2 ["Ch 2: Limits"]
      calculus_volume_1_c2intro["Limits (overview)"]
      calculus_volume_1_c2s1["A Preview of Calculus"]
      calculus_volume_1_c2s2["The Limit of a Function"]
      calculus_volume_1_c2s3["The Limit Laws"]
      calculus_volume_1_c2s4["Continuity"]
      calculus_volume_1_c2s5["The Precise Definition of a Limit"]
    end
    subgraph calculus_volume_1_ch3 ["Ch 3: Derivatives"]
      calculus_volume_1_c3intro["Derivatives (overview)"]
      calculus_volume_1_c3s1["Defining the Derivative"]
      calculus_volume_1_c3s2["The Derivative as a Function"]
      calculus_volume_1_c3s3["Differentiation Rules"]
      calculus_volume_1_c3s4["Derivatives as Rates of Change"]
      calculus_volume_1_c3s5["Derivatives of Trigonometric Functions"]
      calculus_volume_1_c3s6["The Chain Rule"]
      calculus_volume_1_c3s7["Derivatives of Inverse Functions"]
      calculus_volume_1_c3s8["Implicit Differentiation"]
      calculus_volume_1_c3s9["Derivatives of Exponential and Logarithmic ..."]
    end
    subgraph calculus_volume_1_ch4 ["Ch 4: Applications of Derivatives"]
      calculus_volume_1_c4intro["Applications of Derivatives (overview)"]
      calculus_volume_1_c4s1["Related Rates"]
      calculus_volume_1_c4s2["Linear Approximations and Differentials"]
      calculus_volume_1_c4s3["Maxima and Minima"]
      calculus_volume_1_c4s4["The Mean Value Theorem"]
      calculus_volume_1_c4s5["Derivatives and the Shape of a Graph"]
      calculus_volume_1_c4s6["Limits at Infinity and Asymptotes"]
      calculus_volume_1_c4s7["Applied Optimization Problems"]
      calculus_volume_1_c4s8["L’Hôpital’s Rule"]
      calculus_volume_1_c4s9["Newton’s Method"]
      calculus_volume_1_c4s10["Antiderivatives"]
    end
    subgraph calculus_volume_1_ch5 ["Ch 5: Integration"]
      calculus_volume_1_c5intro["Integration (overview)"]
      calculus_volume_1_c5s1["Approximating Areas"]
      calculus_volume_1_c5s2["The Definite Integral"]
      calculus_volume_1_c5s3["The Fundamental Theorem of Calculus"]
      calculus_volume_1_c5s4["Integration Formulas and the Net Change The..."]
      calculus_volume_1_c5s5["Substitution"]
      calculus_volume_1_c5s6["Integrals Involving Exponential and Logarit..."]
      calculus_volume_1_c5s7["Integrals Resulting in Inverse Trigonometri..."]
    end
    subgraph calculus_volume_1_ch6 ["Ch 6: Applications of Integration"]
      calculus_volume_1_c6intro["Applications of Integration (overview)"]
      calculus_volume_1_c6s1["Areas between Curves"]
      calculus_volume_1_c6s2["Determining Volumes by Slicing"]
      calculus_volume_1_c6s3["Volumes of Revolution: Cylindrical Shells"]
      calculus_volume_1_c6s4["Arc Length of a Curve and Surface Area"]
      calculus_volume_1_c6s5["Physical Applications"]
      calculus_volume_1_c6s6["Moments and Centers of Mass"]
      calculus_volume_1_c6s7["Integrals, Exponential Functions, and Logar..."]
      calculus_volume_1_c6s8["Exponential Growth and Decay"]
      calculus_volume_1_c6s9["Calculus of the Hyperbolic Functions"]
    end
  end
  calculus_volume_1_c1intro --> calculus_volume_1_c1s1
  calculus_volume_1_c1s1 --> calculus_volume_1_c1s2
  calculus_volume_1_c1s2 --> calculus_volume_1_c1s3
  calculus_volume_1_c1s3 --> calculus_volume_1_c1s4
  calculus_volume_1_c1s4 --> calculus_volume_1_c1s5
  calculus_volume_1_c1s5 --> calculus_volume_1_c2intro
  calculus_volume_1_c2intro --> calculus_volume_1_c2s1
  calculus_volume_1_c2s1 --> calculus_volume_1_c2s2
  calculus_volume_1_c2s2 --> calculus_volume_1_c2s3
  calculus_volume_1_c2s3 --> calculus_volume_1_c2s4
  calculus_volume_1_c2s4 --> calculus_volume_1_c2s5
  calculus_volume_1_c2s5 --> calculus_volume_1_c3intro
  calculus_volume_1_c3intro --> calculus_volume_1_c3s1
  calculus_volume_1_c3s1 --> calculus_volume_1_c3s2
  calculus_volume_1_c3s2 --> calculus_volume_1_c3s3
  calculus_volume_1_c3s3 --> calculus_volume_1_c3s4
  calculus_volume_1_c3s4 --> calculus_volume_1_c3s5
  calculus_volume_1_c3s5 --> calculus_volume_1_c3s6
  calculus_volume_1_c3s6 --> calculus_volume_1_c3s7
  calculus_volume_1_c3s7 --> calculus_volume_1_c3s8
  calculus_volume_1_c3s8 --> calculus_volume_1_c3s9
  calculus_volume_1_c3s9 --> calculus_volume_1_c4intro
  calculus_volume_1_c4intro --> calculus_volume_1_c4s1
  calculus_volume_1_c4s1 --> calculus_volume_1_c4s2
  calculus_volume_1_c4s2 --> calculus_volume_1_c4s3
  calculus_volume_1_c4s3 --> calculus_volume_1_c4s4
  calculus_volume_1_c4s4 --> calculus_volume_1_c4s5
  calculus_volume_1_c4s5 --> calculus_volume_1_c4s6
  calculus_volume_1_c4s6 --> calculus_volume_1_c4s7
  calculus_volume_1_c4s7 --> calculus_volume_1_c4s8
  calculus_volume_1_c4s8 --> calculus_volume_1_c4s9
  calculus_volume_1_c4s9 --> calculus_volume_1_c4s10
  calculus_volume_1_c4s10 --> calculus_volume_1_c5intro
  calculus_volume_1_c5intro --> calculus_volume_1_c5s1
  calculus_volume_1_c5s1 --> calculus_volume_1_c5s2
  calculus_volume_1_c5s2 --> calculus_volume_1_c5s3
  calculus_volume_1_c5s3 --> calculus_volume_1_c5s4
  calculus_volume_1_c5s4 --> calculus_volume_1_c5s5
  calculus_volume_1_c5s5 --> calculus_volume_1_c5s6
  calculus_volume_1_c5s6 --> calculus_volume_1_c5s7
  calculus_volume_1_c5s7 --> calculus_volume_1_c6intro
  calculus_volume_1_c6intro --> calculus_volume_1_c6s1
  calculus_volume_1_c6s1 --> calculus_volume_1_c6s2
  calculus_volume_1_c6s2 --> calculus_volume_1_c6s3
  calculus_volume_1_c6s3 --> calculus_volume_1_c6s4
  calculus_volume_1_c6s4 --> calculus_volume_1_c6s5
  calculus_volume_1_c6s5 --> calculus_volume_1_c6s6
  calculus_volume_1_c6s6 --> calculus_volume_1_c6s7
  calculus_volume_1_c6s7 --> calculus_volume_1_c6s8
  calculus_volume_1_c6s8 --> calculus_volume_1_c6s9
  subgraph calculus_volume_2 [Calculus II (OpenStax Calculus Vol. 2)]
    subgraph calculus_volume_2_ch1 ["Ch 1: Integration"]
      calculus_volume_2_c1intro["Integration (overview)"]
      calculus_volume_2_c1s1["Approximating Areas"]
      calculus_volume_2_c1s2["The Definite Integral"]
      calculus_volume_2_c1s3["The Fundamental Theorem of Calculus"]
      calculus_volume_2_c1s4["Integration Formulas and the Net Change The..."]
      calculus_volume_2_c1s5["Substitution"]
      calculus_volume_2_c1s6["Integrals Involving Exponential and Logarit..."]
      calculus_volume_2_c1s7["Integrals Resulting in Inverse Trigonometri..."]
    end
    subgraph calculus_volume_2_ch2 ["Ch 2: Applications of Integration"]
      calculus_volume_2_c2intro["Applications of Integration (overview)"]
      calculus_volume_2_c2s1["Areas between Curves"]
      calculus_volume_2_c2s2["Determining Volumes by Slicing"]
      calculus_volume_2_c2s3["Volumes of Revolution: Cylindrical Shells"]
      calculus_volume_2_c2s4["Arc Length of a Curve and Surface Area"]
      calculus_volume_2_c2s5["Physical Applications"]
      calculus_volume_2_c2s6["Moments and Centers of Mass"]
      calculus_volume_2_c2s7["Integrals, Exponential Functions, and Logar..."]
      calculus_volume_2_c2s8["Exponential Growth and Decay"]
      calculus_volume_2_c2s9["Calculus of the Hyperbolic Functions"]
    end
    subgraph calculus_volume_2_ch3 ["Ch 3: Techniques of Integration"]
      calculus_volume_2_c3intro["Techniques of Integration (overview)"]
      calculus_volume_2_c3s1["Integration by Parts"]
      calculus_volume_2_c3s2["Trigonometric Integrals"]
      calculus_volume_2_c3s3["Trigonometric Substitution"]
      calculus_volume_2_c3s4["Partial Fractions"]
      calculus_volume_2_c3s5["Other Strategies for Integration"]
      calculus_volume_2_c3s6["Numerical Integration"]
      calculus_volume_2_c3s7["Improper Integrals"]
    end
    subgraph calculus_volume_2_ch4 ["Ch 4: Introduction to Differential Equations"]
      calculus_volume_2_c4intro["Introduction to Differential Equations (ove..."]
      calculus_volume_2_c4s1["Basics of Differential Equations"]
      calculus_volume_2_c4s2["Direction Fields and Numerical Methods"]
      calculus_volume_2_c4s3["Separable Equations"]
      calculus_volume_2_c4s4["The Logistic Equation"]
      calculus_volume_2_c4s5["First-order Linear Equations"]
    end
    subgraph calculus_volume_2_ch5 ["Ch 5: Sequences and Series"]
      calculus_volume_2_c5intro["Sequences and Series (overview)"]
      calculus_volume_2_c5s1["Sequences"]
      calculus_volume_2_c5s2["Infinite Series"]
      calculus_volume_2_c5s3["The Divergence and Integral Tests"]
      calculus_volume_2_c5s4["Comparison Tests"]
      calculus_volume_2_c5s5["Alternating Series"]
      calculus_volume_2_c5s6["Ratio and Root Tests"]
    end
    subgraph calculus_volume_2_ch6 ["Ch 6: Power Series"]
      calculus_volume_2_c6intro["Power Series (overview)"]
      calculus_volume_2_c6s1["Power Series and Functions"]
      calculus_volume_2_c6s2["Properties of Power Series"]
      calculus_volume_2_c6s3["Taylor and Maclaurin Series"]
      calculus_volume_2_c6s4["Working with Taylor Series"]
    end
    subgraph calculus_volume_2_ch7 ["Ch 7: Parametric Equations and Polar Coordinates"]
      calculus_volume_2_c7intro["Parametric Equations and Polar Coordinates ..."]
      calculus_volume_2_c7s1["Parametric Equations"]
      calculus_volume_2_c7s2["Calculus of Parametric Curves"]
      calculus_volume_2_c7s3["Polar Coordinates"]
      calculus_volume_2_c7s4["Area and Arc Length in Polar Coordinates"]
      calculus_volume_2_c7s5["Conic Sections"]
    end
  end
  calculus_volume_2_c1intro --> calculus_volume_2_c1s1
  calculus_volume_2_c1s1 --> calculus_volume_2_c1s2
  calculus_volume_2_c1s2 --> calculus_volume_2_c1s3
  calculus_volume_2_c1s3 --> calculus_volume_2_c1s4
  calculus_volume_2_c1s4 --> calculus_volume_2_c1s5
  calculus_volume_2_c1s5 --> calculus_volume_2_c1s6
  calculus_volume_2_c1s6 --> calculus_volume_2_c1s7
  calculus_volume_2_c1s7 --> calculus_volume_2_c2intro
  calculus_volume_2_c2intro --> calculus_volume_2_c2s1
  calculus_volume_2_c2s1 --> calculus_volume_2_c2s2
  calculus_volume_2_c2s2 --> calculus_volume_2_c2s3
  calculus_volume_2_c2s3 --> calculus_volume_2_c2s4
  calculus_volume_2_c2s4 --> calculus_volume_2_c2s5
  calculus_volume_2_c2s5 --> calculus_volume_2_c2s6
  calculus_volume_2_c2s6 --> calculus_volume_2_c2s7
  calculus_volume_2_c2s7 --> calculus_volume_2_c2s8
  calculus_volume_2_c2s8 --> calculus_volume_2_c2s9
  calculus_volume_2_c2s9 --> calculus_volume_2_c3intro
  calculus_volume_2_c3intro --> calculus_volume_2_c3s1
  calculus_volume_2_c3s1 --> calculus_volume_2_c3s2
  calculus_volume_2_c3s2 --> calculus_volume_2_c3s3
  calculus_volume_2_c3s3 --> calculus_volume_2_c3s4
  calculus_volume_2_c3s4 --> calculus_volume_2_c3s5
  calculus_volume_2_c3s5 --> calculus_volume_2_c3s6
  calculus_volume_2_c3s6 --> calculus_volume_2_c3s7
  calculus_volume_2_c3s7 --> calculus_volume_2_c4intro
  calculus_volume_2_c4intro --> calculus_volume_2_c4s1
  calculus_volume_2_c4s1 --> calculus_volume_2_c4s2
  calculus_volume_2_c4s2 --> calculus_volume_2_c4s3
  calculus_volume_2_c4s3 --> calculus_volume_2_c4s4
  calculus_volume_2_c4s4 --> calculus_volume_2_c4s5
  calculus_volume_2_c4s5 --> calculus_volume_2_c5intro
  calculus_volume_2_c5intro --> calculus_volume_2_c5s1
  calculus_volume_2_c5s1 --> calculus_volume_2_c5s2
  calculus_volume_2_c5s2 --> calculus_volume_2_c5s3
  calculus_volume_2_c5s3 --> calculus_volume_2_c5s4
  calculus_volume_2_c5s4 --> calculus_volume_2_c5s5
  calculus_volume_2_c5s5 --> calculus_volume_2_c5s6
  calculus_volume_2_c5s6 --> calculus_volume_2_c6intro
  calculus_volume_2_c6intro --> calculus_volume_2_c6s1
  calculus_volume_2_c6s1 --> calculus_volume_2_c6s2
  calculus_volume_2_c6s2 --> calculus_volume_2_c6s3
  calculus_volume_2_c6s3 --> calculus_volume_2_c6s4
  calculus_volume_2_c6s4 --> calculus_volume_2_c7intro
  calculus_volume_2_c7intro --> calculus_volume_2_c7s1
  calculus_volume_2_c7s1 --> calculus_volume_2_c7s2
  calculus_volume_2_c7s2 --> calculus_volume_2_c7s3
  calculus_volume_2_c7s3 --> calculus_volume_2_c7s4
  calculus_volume_2_c7s4 --> calculus_volume_2_c7s5
  calculus_volume_1_c6s9 --> calculus_volume_2_c1intro
  subgraph calculus_volume_3 [Calculus III (OpenStax Calculus Vol. 3)]
    subgraph calculus_volume_3_ch1 ["Ch 1: Parametric Equations and Polar Coordinates"]
      calculus_volume_3_c1intro["Parametric Equations and Polar Coordinates ..."]
      calculus_volume_3_c1s1["Parametric Equations"]
      calculus_volume_3_c1s2["Calculus of Parametric Curves"]
      calculus_volume_3_c1s3["Polar Coordinates"]
      calculus_volume_3_c1s4["Area and Arc Length in Polar Coordinates"]
      calculus_volume_3_c1s5["Conic Sections"]
    end
    subgraph calculus_volume_3_ch2 ["Ch 2: Vectors in Space"]
      calculus_volume_3_c2intro["Vectors in Space (overview)"]
      calculus_volume_3_c2s1["Vectors in the Plane"]
      calculus_volume_3_c2s2["Vectors in Three Dimensions"]
      calculus_volume_3_c2s3["The Dot Product"]
      calculus_volume_3_c2s4["The Cross Product"]
      calculus_volume_3_c2s5["Equations of Lines and Planes in Space"]
      calculus_volume_3_c2s6["Quadric Surfaces"]
      calculus_volume_3_c2s7["Cylindrical and Spherical Coordinates"]
    end
    subgraph calculus_volume_3_ch3 ["Ch 3: Vector-Valued Functions"]
      calculus_volume_3_c3intro["Vector-Valued Functions (overview)"]
      calculus_volume_3_c3s1["Vector-Valued Functions and Space Curves"]
      calculus_volume_3_c3s2["Calculus of Vector-Valued Functions"]
      calculus_volume_3_c3s3["Arc Length and Curvature"]
      calculus_volume_3_c3s4["Motion in Space"]
    end
    subgraph calculus_volume_3_ch4 ["Ch 4: Differentiation of Functions of Several Var..."]
      calculus_volume_3_c4intro["Differentiation of Functions of Several Var..."]
      calculus_volume_3_c4s1["Functions of Several Variables"]
      calculus_volume_3_c4s2["Limits and Continuity"]
      calculus_volume_3_c4s3["Partial Derivatives"]
      calculus_volume_3_c4s4["Tangent Planes and Linear Approximations"]
      calculus_volume_3_c4s5["The Chain Rule"]
      calculus_volume_3_c4s6["Directional Derivatives and the Gradient"]
      calculus_volume_3_c4s7["Maxima/Minima Problems"]
      calculus_volume_3_c4s8["Lagrange Multipliers"]
    end
    subgraph calculus_volume_3_ch5 ["Ch 5: Multiple Integration"]
      calculus_volume_3_c5intro["Multiple Integration (overview)"]
      calculus_volume_3_c5s1["Double Integrals over Rectangular Regions"]
      calculus_volume_3_c5s2["Double Integrals over General Regions"]
      calculus_volume_3_c5s3["Double Integrals in Polar Coordinates"]
      calculus_volume_3_c5s4["Triple Integrals"]
      calculus_volume_3_c5s5["Triple Integrals in Cylindrical and Spheric..."]
      calculus_volume_3_c5s6["Calculating Centers of Mass and Moments of ..."]
      calculus_volume_3_c5s7["Change of Variables in Multiple Integrals"]
    end
    subgraph calculus_volume_3_ch6 ["Ch 6: Vector Calculus"]
      calculus_volume_3_c6intro["Vector Calculus (overview)"]
      calculus_volume_3_c6s1["Vector Fields"]
      calculus_volume_3_c6s2["Line Integrals"]
      calculus_volume_3_c6s3["Conservative Vector Fields"]
      calculus_volume_3_c6s4["Green’s Theorem"]
      calculus_volume_3_c6s5["Divergence and Curl"]
      calculus_volume_3_c6s6["Surface Integrals"]
      calculus_volume_3_c6s7["Stokes’ Theorem"]
      calculus_volume_3_c6s8["The Divergence Theorem"]
    end
    subgraph calculus_volume_3_ch7 ["Ch 7: Second-Order Differential Equations"]
      calculus_volume_3_c7intro["Second-Order Differential Equations (overview)"]
      calculus_volume_3_c7s1["Second-Order Linear Equations"]
      calculus_volume_3_c7s2["Nonhomogeneous Linear Equations"]
      calculus_volume_3_c7s3["Applications"]
      calculus_volume_3_c7s4["Series Solutions of Differential Equations"]
    end
  end
  calculus_volume_3_c1intro --> calculus_volume_3_c1s1
  calculus_volume_3_c1s1 --> calculus_volume_3_c1s2
  calculus_volume_3_c1s2 --> calculus_volume_3_c1s3
  calculus_volume_3_c1s3 --> calculus_volume_3_c1s4
  calculus_volume_3_c1s4 --> calculus_volume_3_c1s5
  calculus_volume_3_c1s5 --> calculus_volume_3_c2intro
  calculus_volume_3_c2intro --> calculus_volume_3_c2s1
  calculus_volume_3_c2s1 --> calculus_volume_3_c2s2
  calculus_volume_3_c2s2 --> calculus_volume_3_c2s3
  calculus_volume_3_c2s3 --> calculus_volume_3_c2s4
  calculus_volume_3_c2s4 --> calculus_volume_3_c2s5
  calculus_volume_3_c2s5 --> calculus_volume_3_c2s6
  calculus_volume_3_c2s6 --> calculus_volume_3_c2s7
  calculus_volume_3_c2s7 --> calculus_volume_3_c3intro
  calculus_volume_3_c3intro --> calculus_volume_3_c3s1
  calculus_volume_3_c3s1 --> calculus_volume_3_c3s2
  calculus_volume_3_c3s2 --> calculus_volume_3_c3s3
  calculus_volume_3_c3s3 --> calculus_volume_3_c3s4
  calculus_volume_3_c3s4 --> calculus_volume_3_c4intro
  calculus_volume_3_c4intro --> calculus_volume_3_c4s1
  calculus_volume_3_c4s1 --> calculus_volume_3_c4s2
  calculus_volume_3_c4s2 --> calculus_volume_3_c4s3
  calculus_volume_3_c4s3 --> calculus_volume_3_c4s4
  calculus_volume_3_c4s4 --> calculus_volume_3_c4s5
  calculus_volume_3_c4s5 --> calculus_volume_3_c4s6
  calculus_volume_3_c4s6 --> calculus_volume_3_c4s7
  calculus_volume_3_c4s7 --> calculus_volume_3_c4s8
  calculus_volume_3_c4s8 --> calculus_volume_3_c5intro
  calculus_volume_3_c5intro --> calculus_volume_3_c5s1
  calculus_volume_3_c5s1 --> calculus_volume_3_c5s2
  calculus_volume_3_c5s2 --> calculus_volume_3_c5s3
  calculus_volume_3_c5s3 --> calculus_volume_3_c5s4
  calculus_volume_3_c5s4 --> calculus_volume_3_c5s5
  calculus_volume_3_c5s5 --> calculus_volume_3_c5s6
  calculus_volume_3_c5s6 --> calculus_volume_3_c5s7
  calculus_volume_3_c5s7 --> calculus_volume_3_c6intro
  calculus_volume_3_c6intro --> calculus_volume_3_c6s1
  calculus_volume_3_c6s1 --> calculus_volume_3_c6s2
  calculus_volume_3_c6s2 --> calculus_volume_3_c6s3
  calculus_volume_3_c6s3 --> calculus_volume_3_c6s4
  calculus_volume_3_c6s4 --> calculus_volume_3_c6s5
  calculus_volume_3_c6s5 --> calculus_volume_3_c6s6
  calculus_volume_3_c6s6 --> calculus_volume_3_c6s7
  calculus_volume_3_c6s7 --> calculus_volume_3_c6s8
  calculus_volume_3_c6s8 --> calculus_volume_3_c7intro
  calculus_volume_3_c7intro --> calculus_volume_3_c7s1
  calculus_volume_3_c7s1 --> calculus_volume_3_c7s2
  calculus_volume_3_c7s2 --> calculus_volume_3_c7s3
  calculus_volume_3_c7s3 --> calculus_volume_3_c7s4
  calculus_volume_2_c7s5 --> calculus_volume_3_c1intro
```

## Calculus I (OpenStax Calculus Vol. 1) (`calculus-volume-1`)

### Chapter 1

- **intro Functions and Graphs (overview)**
- **1.1 Review of Functions**
  - Use functional notation to evaluate a function.
  - Determine the domain and range of a function.
  - Draw the graph of a function.
  - Find the zeros of a function.
  - Recognize a function from a table of values.
  - Make new functions from two or more given functions.
  - Describe the symmetry properties of a function.
- **1.2 Basic Classes of Functions**
  - Calculate the slope of a linear function and interpret its meaning.
  - Recognize the degree of a polynomial.
  - Find the roots of a quadratic polynomial.
  - Describe the graphs of basic odd and even polynomial functions.
  - Identify a rational function.
  - Describe the graphs of power and root functions.
  - Explain the difference between algebraic and transcendental functions.
  - Graph a piecewise-defined function.
  - Sketch the graph of a function that has been shifted, stretched, or reflected from its initial graph position.
- **1.3 Trigonometric Functions**
  - Convert angle measures between degrees and radians.
  - Recognize the triangular and circular definitions of the basic trigonometric functions.
  - Write the basic trigonometric identities.
  - Identify the graphs and periods of the trigonometric functions.
  - Describe the shift of a sine or cosine graph from the equation of the function.
- **1.4 Inverse Functions**
  - Determine the conditions for when a function has an inverse.
  - Use the horizontal line test to recognize when a function is one-to-one.
  - Find the inverse of a given function.
  - Draw the graph of an inverse function.
  - Evaluate inverse trigonometric functions.
- **1.5 Exponential and Logarithmic Functions**
  - Identify the form of an exponential function.
  - Explain the difference between the graphs of x b x b and b x . b x .
  - Recognize the significance of the number e . e .
  - Identify the form of a logarithmic function.
  - Explain the relationship between exponential and logarithmic functions.
  - Describe how to calculate a logarithm to a different base.
  - Identify the hyperbolic functions, their graphs, and basic identities.
### Chapter 2

- **intro Limits (overview)**
- **2.1 A Preview of Calculus**
  - Describe the tangent problem and how it led to the idea of a derivative.
  - Explain how the idea of a limit is involved in solving the tangent problem.
  - Recognize a tangent to a curve at a point as the limit of secant lines.
  - Identify instantaneous velocity as the limit of average velocity over a small time interval.
  - Describe the area problem and how it was solved by the integral.
  - Explain how the idea of a limit is involved in solving the area problem.
  - Recognize how the ideas of limit, derivative, and integral led to the studies of infinite series and multivariable calculus.
- **2.2 The Limit of a Function**
  - Using correct notation, describe the limit of a function.
  - Use a table of values to estimate the limit of a function or to identify when the limit does not exist.
  - Use a graph to estimate the limit of a function or to identify when the limit does not exist.
  - Define one-sided limits and provide examples.
  - Explain the relationship between one-sided and two-sided limits.
  - Using correct notation, describe an infinite limit.
  - Define a vertical asymptote.
- **2.3 The Limit Laws**
  - Recognize the basic limit laws.
  - Use the limit laws to evaluate the limit of a function.
  - Evaluate the limit of a function by factoring.
  - Use the limit laws to evaluate the limit of a polynomial or rational function.
  - Evaluate the limit of a function by factoring or by using conjugates.
  - Evaluate the limit of a function by using the squeeze theorem.
- **2.4 Continuity**
  - Explain the three conditions for continuity at a point.
  - Describe three kinds of discontinuities.
  - Define continuity on an interval.
  - State the theorem for limits of composite functions.
  - Provide an example of the intermediate value theorem.
- **2.5 The Precise Definition of a Limit**
  - Describe the epsilon-delta definition of a limit.
  - Apply the epsilon-delta definition to find the limit of a function.
  - Describe the epsilon-delta definitions of one-sided limits and infinite limits.
  - Use the epsilon-delta definition to prove the limit laws.
### Chapter 3

- **intro Derivatives (overview)**
- **3.1 Defining the Derivative**
  - Recognize the meaning of the tangent to a curve at a point.
  - Calculate the slope of a tangent line.
  - Identify the derivative as the limit of a difference quotient.
  - Calculate the derivative of a given function at a point.
  - Describe the velocity as a rate of change.
  - Explain the difference between average velocity and instantaneous velocity.
  - Estimate the derivative from a table of values.
- **3.2 The Derivative as a Function**
  - Define the derivative function of a given function.
  - Graph a derivative function from the graph of a given function.
  - State the connection between derivatives and continuity.
  - Describe three conditions for when a function does not have a derivative.
  - Explain the meaning of a higher-order derivative.
- **3.3 Differentiation Rules**
  - State the constant, constant multiple, and power rules.
  - Apply the sum and difference rules to combine derivatives.
  - Use the product rule for finding the derivative of a product of functions.
  - Use the quotient rule for finding the derivative of a quotient of functions.
  - Extend the power rule to functions with negative exponents.
  - Combine the differentiation rules to find the derivative of a polynomial or rational function.
- **3.4 Derivatives as Rates of Change**
  - Determine a new value of a quantity from the old value and the amount of change.
  - Calculate the average rate of change and explain how it differs from the instantaneous rate of change.
  - Apply rates of change to displacement, velocity, and acceleration of an object moving along a straight line.
  - Predict the future population from the present value and the population growth rate.
  - Use derivatives to calculate marginal cost and revenue in a business situation.
- **3.5 Derivatives of Trigonometric Functions**
  - Find the derivatives of the sine and cosine function.
  - Find the derivatives of the standard trigonometric functions.
  - Calculate the higher-order derivatives of the sine and cosine.
- **3.6 The Chain Rule**
  - State the chain rule for the composition of two functions.
  - Apply the chain rule together with the power rule.
  - Apply the chain rule and the product/quotient rules correctly in combination when both are necessary.
  - Recognize the chain rule for a composition of three or more functions.
  - Describe the proof of the chain rule.
- **3.7 Derivatives of Inverse Functions**
  - Calculate the derivative of an inverse function.
  - Recognize the derivatives of the standard inverse trigonometric functions.
- **3.8 Implicit Differentiation**
  - Find the derivative of a complicated function by using implicit differentiation.
  - Use implicit differentiation to determine the equation of a tangent line.
- **3.9 Derivatives of Exponential and Logarithmic Functions**
  - Find the derivative of exponential functions.
  - Find the derivative of logarithmic functions.
  - Use logarithmic differentiation to determine the derivative of a function.
### Chapter 4

- **intro Applications of Derivatives (overview)**
- **4.1 Related Rates**
  - Express changing quantities in terms of derivatives.
  - Find relationships among the derivatives in a given problem.
  - Use the chain rule to find the rate of change of one quantity that depends on the rate of change of other quantities.
- **4.2 Linear Approximations and Differentials**
  - Describe the linear approximation to a function at a point.
  - Write the linearization of a given function.
  - Draw a graph that illustrates the use of differentials to approximate the change in a quantity.
  - Calculate the relative error and percentage error in using a differential approximation.
- **4.3 Maxima and Minima**
  - Define absolute extrema.
  - Define local extrema.
  - Explain how to find the critical points of a function over a closed interval.
  - Describe how to use critical points to locate absolute extrema over a closed interval.
- **4.4 The Mean Value Theorem**
  - Explain the meaning of Rolle’s theorem.
  - Describe the significance of the Mean Value Theorem.
  - State three important consequences of the Mean Value Theorem.
- **4.5 Derivatives and the Shape of a Graph**
  - Explain how the sign of the first derivative affects the shape of a function’s graph.
  - State the first derivative test for critical points.
  - Use concavity and inflection points to explain how the sign of the second derivative affects the shape of a function’s graph.
  - Explain the concavity test for a function over an open interval.
  - Explain the relationship between a function and its first and second derivatives.
  - State the second derivative test for local extrema.
- **4.6 Limits at Infinity and Asymptotes**
  - Calculate the limit of a function as x x increases or decreases without bound.
  - Recognize a horizontal asymptote on the graph of a function.
  - Estimate the end behavior of a function as x x increases or decreases without bound.
  - Recognize an oblique asymptote on the graph of a function.
  - Analyze a function and its derivatives to draw its graph.
- **4.7 Applied Optimization Problems**
  - Set up and solve optimization problems in several applied fields.
- **4.8 L’Hôpital’s Rule**
  - Recognize when to apply L’Hôpital’s rule.
  - Identify indeterminate forms produced by quotients, products, subtractions, and powers, and apply L’Hôpital’s rule in each case.
  - Describe the relative growth rates of functions.
- **4.9 Newton’s Method**
  - Describe the steps of Newton’s method.
  - Explain what an iterative process means.
  - Recognize when Newton’s method does not work.
  - Apply iterative processes to various situations.
- **4.10 Antiderivatives**
  - Find the general antiderivative of a given function.
  - Explain the terms and notation used for an indefinite integral.
  - State the power rule for integrals.
  - Use antidifferentiation to solve simple initial-value problems.
### Chapter 5

- **intro Integration (overview)**
- **5.1 Approximating Areas**
  - Use sigma (summation) notation to calculate sums and powers of integers.
  - Use the sum of rectangular areas to approximate the area under a curve.
  - Use Riemann sums to approximate area.
- **5.2 The Definite Integral**
  - State the definition of the definite integral.
  - Explain the terms integrand, limits of integration, and variable of integration.
  - Explain when a function is integrable.
  - Describe the relationship between the definite integral and net area.
  - Use geometry and the properties of definite integrals to evaluate them.
  - Calculate the average value of a function.
- **5.3 The Fundamental Theorem of Calculus**
  - Describe the meaning of the Mean Value Theorem for Integrals.
  - State the meaning of the Fundamental Theorem of Calculus, Part 1.
  - Use the Fundamental Theorem of Calculus, Part 1, to evaluate derivatives of integrals.
  - State the meaning of the Fundamental Theorem of Calculus, Part 2.
  - Use the Fundamental Theorem of Calculus, Part 2, to evaluate definite integrals.
  - Explain the relationship between differentiation and integration.
- **5.4 Integration Formulas and the Net Change Theorem**
  - Apply the basic integration formulas.
  - Explain the significance of the net change theorem.
  - Use the net change theorem to solve applied problems.
  - Apply the integrals of odd and even functions.
- **5.5 Substitution**
  - Use substitution to evaluate indefinite integrals.
  - Use substitution to evaluate definite integrals.
- **5.6 Integrals Involving Exponential and Logarithmic Functions**
  - Integrate functions involving exponential functions.
  - Integrate functions involving logarithmic functions.
- **5.7 Integrals Resulting in Inverse Trigonometric Functions**
  - Integrate functions resulting in inverse trigonometric functions
### Chapter 6

- **intro Applications of Integration (overview)**
- **6.1 Areas between Curves**
  - Determine the area of a region between two curves by integrating with respect to the independent variable.
  - Find the area of a compound region.
  - Determine the area of a region between two curves by integrating with respect to the dependent variable.
- **6.2 Determining Volumes by Slicing**
  - Determine the volume of a solid by integrating a cross-section (the slicing method).
  - Find the volume of a solid of revolution using the disk method.
  - Find the volume of a solid of revolution with a cavity using the washer method.
- **6.3 Volumes of Revolution: Cylindrical Shells**
  - Calculate the volume of a solid of revolution by using the method of cylindrical shells.
  - Compare the different methods for calculating a volume of revolution.
- **6.4 Arc Length of a Curve and Surface Area**
  - Determine the length of a curve, y = f ( x ) , y = f ( x ) , between two points.
  - Determine the length of a curve, x = g ( y ) , x = g ( y ) , between two points.
  - Find the surface area of a solid of revolution.
- **6.5 Physical Applications**
  - Determine the mass of a one-dimensional object from its linear density function.
  - Determine the mass of a two-dimensional circular object from its radial density function.
  - Calculate the work done by a variable force acting along a line.
  - Calculate the work done in pumping a liquid from one height to another.
  - Find the hydrostatic force against a submerged vertical plate.
- **6.6 Moments and Centers of Mass**
  - Find the center of mass of objects distributed along a line.
  - Locate the center of mass of a thin plate.
  - Use symmetry to help locate the centroid of a thin plate.
  - Apply the theorem of Pappus for volume.
- **6.7 Integrals, Exponential Functions, and Logarithms**
  - Write the definition of the natural logarithm as an integral.
  - Recognize the derivative of the natural logarithm.
  - Integrate functions involving the natural logarithmic function.
  - Define the number e e through an integral.
  - Recognize the derivative and integral of the exponential function.
  - Prove properties of logarithms and exponential functions using integrals.
  - Express general logarithmic and exponential functions in terms of natural logarithms and exponentials.
- **6.8 Exponential Growth and Decay**
  - Use the exponential growth model in applications, including population growth and compound interest.
  - Explain the concept of doubling time.
  - Use the exponential decay model in applications, including radioactive decay and Newton’s law of cooling.
  - Explain the concept of half-life.
- **6.9 Calculus of the Hyperbolic Functions**
  - Apply the formulas for derivatives and integrals of the hyperbolic functions.
  - Apply the formulas for the derivatives of the inverse hyperbolic functions and their associated integrals.
  - Describe the common applied conditions of a catenary curve.

## Calculus II (OpenStax Calculus Vol. 2) (`calculus-volume-2`)

### Chapter 1

- **intro Integration (overview)**
- **1.1 Approximating Areas**
  - Use sigma (summation) notation to calculate sums and powers of integers.
  - Use the sum of rectangular areas to approximate the area under a curve.
  - Use Riemann sums to approximate area.
- **1.2 The Definite Integral**
  - State the definition of the definite integral.
  - Explain the terms integrand, limits of integration, and variable of integration.
  - Explain when a function is integrable.
  - Describe the relationship between the definite integral and net area.
  - Use geometry and the properties of definite integrals to evaluate them.
  - Calculate the average value of a function.
- **1.3 The Fundamental Theorem of Calculus**
  - Describe the meaning of the Mean Value Theorem for Integrals.
  - State the meaning of the Fundamental Theorem of Calculus, Part 1.
  - Use the Fundamental Theorem of Calculus, Part 1, to evaluate derivatives of integrals.
  - State the meaning of the Fundamental Theorem of Calculus, Part 2.
  - Use the Fundamental Theorem of Calculus, Part 2, to evaluate definite integrals.
  - Explain the relationship between differentiation and integration.
- **1.4 Integration Formulas and the Net Change Theorem**
  - Apply the basic integration formulas.
  - Explain the significance of the net change theorem.
  - Use the net change theorem to solve applied problems.
  - Apply the integrals of odd and even functions.
- **1.5 Substitution**
  - Use substitution to evaluate indefinite integrals.
  - Use substitution to evaluate definite integrals.
- **1.6 Integrals Involving Exponential and Logarithmic Functions**
  - Integrate functions involving exponential functions.
  - Integrate functions involving logarithmic functions.
- **1.7 Integrals Resulting in Inverse Trigonometric Functions**
  - Integrate functions resulting in inverse trigonometric functions
### Chapter 2

- **intro Applications of Integration (overview)**
- **2.1 Areas between Curves**
  - Determine the area of a region between two curves by integrating with respect to the independent variable.
  - Find the area of a compound region.
  - Determine the area of a region between two curves by integrating with respect to the dependent variable.
- **2.2 Determining Volumes by Slicing**
  - Determine the volume of a solid by integrating a cross-section (the slicing method).
  - Find the volume of a solid of revolution using the disk method.
  - Find the volume of a solid of revolution with a cavity using the washer method.
- **2.3 Volumes of Revolution: Cylindrical Shells**
  - Calculate the volume of a solid of revolution by using the method of cylindrical shells.
  - Compare the different methods for calculating a volume of revolution.
- **2.4 Arc Length of a Curve and Surface Area**
  - Determine the length of a curve, y = f ( x ) , y = f ( x ) , between two points.
  - Determine the length of a curve, x = g ( y ) , x = g ( y ) , between two points.
  - Find the surface area of a solid of revolution.
- **2.5 Physical Applications**
  - Determine the mass of a one-dimensional object from its linear density function.
  - Determine the mass of a two-dimensional circular object from its radial density function.
  - Calculate the work done by a variable force acting along a line.
  - Calculate the work done in pumping a liquid from one height to another.
  - Find the hydrostatic force against a submerged vertical plate.
- **2.6 Moments and Centers of Mass**
  - Find the center of mass of objects distributed along a line.
  - Locate the center of mass of a thin plate.
  - Use symmetry to help locate the centroid of a thin plate.
  - Apply the theorem of Pappus for volume.
- **2.7 Integrals, Exponential Functions, and Logarithms**
  - Write the definition of the natural logarithm as an integral.
  - Recognize the derivative of the natural logarithm.
  - Integrate functions involving the natural logarithmic function.
  - Define the number e e through an integral.
  - Recognize the derivative and integral of the exponential function.
  - Prove properties of logarithms and exponential functions using integrals.
  - Express general logarithmic and exponential functions in terms of natural logarithms and exponentials.
- **2.8 Exponential Growth and Decay**
  - Use the exponential growth model in applications, including population growth and compound interest.
  - Explain the concept of doubling time.
  - Use the exponential decay model in applications, including radioactive decay and Newton’s law of cooling.
  - Explain the concept of half-life.
- **2.9 Calculus of the Hyperbolic Functions**
  - Apply the formulas for derivatives and integrals of the hyperbolic functions.
  - Apply the formulas for the derivatives of the inverse hyperbolic functions and their associated integrals.
  - Describe the common applied conditions of a catenary curve.
### Chapter 3

- **intro Techniques of Integration (overview)**
- **3.1 Integration by Parts**
  - Recognize when to use integration by parts.
  - Use the integration-by-parts formula to solve integration problems.
  - Use the integration-by-parts formula for definite integrals.
- **3.2 Trigonometric Integrals**
  - Solve integration problems involving products and powers of sin x sin x and cos x . cos x .
  - Solve integration problems involving products and powers of tan x tan x and sec x . sec x .
  - Use reduction formulas to solve trigonometric integrals.
- **3.3 Trigonometric Substitution**
  - Solve integration problems involving the square root of a sum or difference of two squares.
- **3.4 Partial Fractions**
  - Integrate a rational function using the method of partial fractions.
  - Recognize simple linear factors in a rational function.
  - Recognize repeated linear factors in a rational function.
  - Recognize quadratic factors in a rational function.
- **3.5 Other Strategies for Integration**
  - Use a table of integrals to solve integration problems.
  - Use a computer algebra system (CAS) to solve integration problems.
- **3.6 Numerical Integration**
  - Approximate the value of a definite integral by using the midpoint and trapezoidal rules.
  - Determine the absolute and relative error in using a numerical integration technique.
  - Estimate the absolute and relative error using an error-bound formula.
  - Recognize when the midpoint and trapezoidal rules over- or underestimate the true value of an integral.
  - Use Simpson’s rule to approximate the value of a definite integral to a given accuracy.
- **3.7 Improper Integrals**
  - Evaluate an integral over an infinite interval.
  - Evaluate an integral over a closed interval with an infinite discontinuity within the interval.
  - Use the comparison theorem to determine whether a definite integral is convergent.
### Chapter 4

- **intro Introduction to Differential Equations (overview)**
- **4.1 Basics of Differential Equations**
  - Identify the order of a differential equation.
  - Explain what is meant by a solution to a differential equation.
  - Distinguish between the general solution and a particular solution of a differential equation.
  - Identify an initial-value problem.
  - Identify whether a given function is a solution to a differential equation or an initial-value problem.
- **4.2 Direction Fields and Numerical Methods**
  - Draw the direction field for a given first-order differential equation.
  - Use a direction field to draw a solution curve of a first-order differential equation.
  - Use Euler’s Method to approximate the solution to a first-order differential equation.
- **4.3 Separable Equations**
  - Use separation of variables to solve a differential equation.
  - Solve applications using separation of variables.
- **4.4 The Logistic Equation**
  - Describe the concept of environmental carrying capacity in the logistic model of population growth.
  - Draw a direction field for a logistic equation and interpret the solution curves.
  - Solve a logistic equation and interpret the results.
- **4.5 First-order Linear Equations**
  - Write a first-order linear differential equation in standard form.
  - Find an integrating factor and use it to solve a first-order linear differential equation.
  - Solve applied problems involving first-order linear differential equations.
### Chapter 5

- **intro Sequences and Series (overview)**
- **5.1 Sequences**
  - Find the formula for the general term of a sequence.
  - Calculate the limit of a sequence if it exists.
  - Determine the convergence or divergence of a given sequence.
- **5.2 Infinite Series**
  - Explain the meaning of the sum of an infinite series.
  - Calculate the sum of a geometric series.
  - Evaluate a telescoping series.
- **5.3 The Divergence and Integral Tests**
  - Use the divergence test to demonstrate that a series diverges.
  - Use the integral test to determine the convergence of a series.
  - Estimate the value of a series by finding bounds on its remainder term.
- **5.4 Comparison Tests**
  - Use the comparison test to test a series for convergence.
  - Use the limit comparison test to determine convergence of a series.
- **5.5 Alternating Series**
  - Use the alternating series test to test an alternating series for convergence.
  - Estimate the sum of an alternating series.
  - Explain the meaning of absolute convergence and conditional convergence.
- **5.6 Ratio and Root Tests**
  - Use the ratio test to determine absolute convergence of a series.
  - Use the root test to determine absolute convergence of a series.
  - Describe a strategy for testing the convergence of a given series.
### Chapter 6

- **intro Power Series (overview)**
- **6.1 Power Series and Functions**
  - Identify a power series and provide examples of them.
  - Determine the radius of convergence and interval of convergence of a power series.
  - Use a power series to represent a function.
- **6.2 Properties of Power Series**
  - Combine power series by addition or subtraction.
  - Create a new power series by multiplication by a power of the variable or a constant, or by substitution.
  - Multiply two power series together.
  - Differentiate and integrate power series term-by-term.
- **6.3 Taylor and Maclaurin Series**
  - Describe the procedure for finding a Taylor polynomial of a given order for a function.
  - Explain the meaning and significance of Taylor’s theorem with remainder.
  - Estimate the remainder for a Taylor series approximation of a given function.
- **6.4 Working with Taylor Series**
  - Write the terms of the binomial series.
  - Recognize the Taylor series expansions of common functions.
  - Recognize and apply techniques to find the Taylor series for a function.
  - Use Taylor series to solve differential equations.
  - Use Taylor series to evaluate nonelementary integrals.
### Chapter 7

- **intro Parametric Equations and Polar Coordinates (overview)**
- **7.1 Parametric Equations**
  - Plot a curve described by parametric equations.
  - Convert the parametric equations of a curve into the form y = f ( x ) . y = f ( x ) .
  - Recognize the parametric equations of basic curves, such as a line and a circle.
  - Recognize the parametric equations of a cycloid.
- **7.2 Calculus of Parametric Curves**
  - Determine derivatives and equations of tangents for parametric curves.
  - Find the area under a parametric curve.
  - Use the equation for arc length of a parametric curve.
  - Apply the formula for surface area to a volume generated by a parametric curve.
- **7.3 Polar Coordinates**
  - Locate points in a plane by using polar coordinates.
  - Convert points between rectangular and polar coordinates.
  - Sketch polar curves from given equations.
  - Convert equations between rectangular and polar coordinates.
  - Identify symmetry in polar curves and equations.
- **7.4 Area and Arc Length in Polar Coordinates**
  - Apply the formula for area of a region in polar coordinates.
  - Determine the arc length of a polar curve.
- **7.5 Conic Sections**
  - Identify the equation of a parabola in standard form with given focus and directrix.
  - Identify the equation of an ellipse in standard form with given foci.
  - Identify the equation of a hyperbola in standard form with given foci.
  - Recognize a parabola, ellipse, or hyperbola from its eccentricity value.
  - Write the polar equation of a conic section with eccentricity e e .
  - Identify when a general equation of degree two is a parabola, ellipse, or hyperbola.

## Calculus III (OpenStax Calculus Vol. 3) (`calculus-volume-3`)

### Chapter 1

- **intro Parametric Equations and Polar Coordinates (overview)**
- **1.1 Parametric Equations**
  - Plot a curve described by parametric equations.
  - Convert the parametric equations of a curve into the form y = f ( x ) . y = f ( x ) .
  - Recognize the parametric equations of basic curves, such as a line and a circle.
  - Recognize the parametric equations of a cycloid.
- **1.2 Calculus of Parametric Curves**
  - Determine derivatives and equations of tangents for parametric curves.
  - Find the area under a parametric curve.
  - Use the equation for arc length of a parametric curve.
  - Apply the formula for surface area to a volume generated by a parametric curve.
- **1.3 Polar Coordinates**
  - Locate points in a plane by using polar coordinates.
  - Convert points between rectangular and polar coordinates.
  - Sketch polar curves from given equations.
  - Convert equations between rectangular and polar coordinates.
  - Identify symmetry in polar curves and equations.
- **1.4 Area and Arc Length in Polar Coordinates**
  - Apply the formula for area of a region in polar coordinates.
  - Determine the arc length of a polar curve.
- **1.5 Conic Sections**
  - Identify the equation of a parabola in standard form with given focus and directrix.
  - Identify the equation of an ellipse in standard form with given foci.
  - Identify the equation of a hyperbola in standard form with given foci.
  - Recognize a parabola, ellipse, or hyperbola from its eccentricity value.
  - Write the polar equation of a conic section with eccentricity e e .
  - Identify when a general equation of degree two is a parabola, ellipse, or hyperbola.
### Chapter 2

- **intro Vectors in Space (overview)**
- **2.1 Vectors in the Plane**
  - Describe a plane vector, using correct notation.
  - Perform basic vector operations (scalar multiplication, addition, subtraction).
  - Express a vector in component form.
  - Explain the formula for the magnitude of a vector.
  - Express a vector in terms of unit vectors.
  - Give two examples of vector quantities.
- **2.2 Vectors in Three Dimensions**
  - Describe three-dimensional space mathematically.
  - Locate points in space using coordinates.
  - Write the distance formula in three dimensions.
  - Write the equations for simple planes and spheres.
  - Perform vector operations in ℝ 3 . ℝ 3 .
- **2.3 The Dot Product**
  - Calculate the dot product of two given vectors.
  - Determine whether two given vectors are perpendicular.
  - Find the direction cosines of a given vector.
  - Explain what is meant by the vector projection of one vector onto another vector, and describe how to compute it.
  - Calculate the work done by a given force.
- **2.4 The Cross Product**
  - Calculate the cross product of two given vectors.
  - Use determinants to calculate a cross product.
  - Find a vector orthogonal to two given vectors.
  - Determine areas and volumes by using the cross product.
  - Calculate the torque of a given force and position vector.
- **2.5 Equations of Lines and Planes in Space**
  - Write the vector, parametric, and symmetric equations of a line through a given point in a given direction, and a line through two given points.
  - Find the distance from a point to a given line.
  - Write the vector and scalar equations of a plane through a given point with a given normal.
  - Find the distance from a point to a given plane.
  - Find the angle between two planes.
- **2.6 Quadric Surfaces**
  - Identify a cylinder as a type of three-dimensional surface.
  - Recognize the main features of ellipsoids, paraboloids, and hyperboloids.
  - Use traces to draw the intersections of quadric surfaces with the coordinate planes.
- **2.7 Cylindrical and Spherical Coordinates**
  - Convert from cylindrical to rectangular coordinates.
  - Convert from rectangular to cylindrical coordinates.
  - Convert from spherical to rectangular coordinates.
  - Convert from rectangular to spherical coordinates.
### Chapter 3

- **intro Vector-Valued Functions (overview)**
- **3.1 Vector-Valued Functions and Space Curves**
  - Write the general equation of a vector-valued function in component form and unit-vector form.
  - Recognize parametric equations for a space curve.
  - Describe the shape of a helix and write its equation.
  - Define the limit of a vector-valued function.
- **3.2 Calculus of Vector-Valued Functions**
  - Write an expression for the derivative of a vector-valued function.
  - Find the tangent vector at a point for a given position vector.
  - Find the unit tangent vector at a point for a given position vector and explain its significance.
  - Calculate the definite integral of a vector-valued function.
- **3.3 Arc Length and Curvature**
  - Determine the length of a particle’s path in space by using the arc-length function.
  - Explain the meaning of the curvature of a curve in space and state its formula.
  - Describe the meaning of the normal and binormal vectors of a curve in space.
- **3.4 Motion in Space**
  - Describe the velocity and acceleration vectors of a particle moving in space.
  - Explain the tangential and normal components of acceleration.
  - State Kepler’s laws of planetary motion.
### Chapter 4

- **intro Differentiation of Functions of Several Variables (overview)**
- **4.1 Functions of Several Variables**
  - Recognize a function of two variables and identify its domain and range.
  - Sketch a graph of a function of two variables.
  - Sketch several traces or level curves of a function of two variables.
  - Recognize a function of three or more variables and identify its level surfaces.
- **4.2 Limits and Continuity**
  - Calculate the limit of a function of two variables.
  - Learn how a function of two variables can approach different values at a boundary point, depending on the path of approach.
  - State the conditions for continuity of a function of two variables.
  - Verify the continuity of a function of two variables at a point.
  - Calculate the limit of a function of three or more variables and verify the continuity of the function at a point.
- **4.3 Partial Derivatives**
  - Calculate the partial derivatives of a function of two variables.
  - Calculate the partial derivatives of a function of more than two variables.
  - Determine the higher-order derivatives of a function of two variables.
  - Explain the meaning of a partial differential equation and give an example.
- **4.4 Tangent Planes and Linear Approximations**
  - Determine the equation of a plane tangent to a given surface at a point.
  - Use the tangent plane to approximate a function of two variables at a point.
  - Explain when a function of two variables is differentiable.
  - Use the total differential to approximate the change in a function of two variables.
- **4.5 The Chain Rule**
  - State the chain rules for one or two independent variables.
  - Use tree diagrams as an aid to understanding the chain rule for several independent and intermediate variables.
  - Perform implicit differentiation of a function of two or more variables.
- **4.6 Directional Derivatives and the Gradient**
  - Determine the directional derivative in a given direction for a function of two variables.
  - Determine the gradient vector of a given real-valued function.
  - Explain the significance of the gradient vector with regard to direction of change along a surface.
  - Use the gradient to find the tangent to a level curve of a given function.
  - Calculate directional derivatives and gradients in three dimensions.
- **4.7 Maxima/Minima Problems**
  - Use partial derivatives to locate critical points for a function of two variables.
  - Apply a second derivative test to identify a critical point as a local maximum, local minimum, or saddle point for a function of two variables.
  - Examine critical points and boundary points to find absolute maximum and minimum values for a function of two variables.
- **4.8 Lagrange Multipliers**
  - Use the method of Lagrange multipliers to solve optimization problems with one constraint.
  - Use the method of Lagrange multipliers to solve optimization problems with two constraints.
### Chapter 5

- **intro Multiple Integration (overview)**
- **5.1 Double Integrals over Rectangular Regions**
  - Recognize when a function of two variables is integrable over a rectangular region.
  - Recognize and use some of the properties of double integrals.
  - Evaluate a double integral over a rectangular region by writing it as an iterated integral.
  - Use a double integral to calculate the area of a region, volume under a surface, or average value of a function over a plane region.
- **5.2 Double Integrals over General Regions**
  - Recognize when a function of two variables is integrable over a general region.
  - Evaluate a double integral by computing an iterated integral over a region bounded by two vertical lines and two functions of x , x , or two horizontal lines and two functions of y . y .
  - Simplify the calculation of an iterated integral by changing the order of integration.
  - Use double integrals to calculate the volume of a region between two surfaces or the area of a plane region.
  - Solve problems involving double improper integrals.
- **5.3 Double Integrals in Polar Coordinates**
  - Recognize the format of a double integral over a polar rectangular region.
  - Evaluate a double integral in polar coordinates by using an iterated integral.
  - Recognize the format of a double integral over a general polar region.
  - Use double integrals in polar coordinates to calculate areas and volumes.
- **5.4 Triple Integrals**
  - Recognize when a function of three variables is integrable over a rectangular box.
  - Evaluate a triple integral by expressing it as an iterated integral.
  - Recognize when a function of three variables is integrable over a closed and bounded region.
  - Simplify a calculation by changing the order of integration of a triple integral.
  - Calculate the average value of a function of three variables.
- **5.5 Triple Integrals in Cylindrical and Spherical Coordinates**
  - Evaluate a triple integral by changing to cylindrical coordinates.
  - Evaluate a triple integral by changing to spherical coordinates.
- **5.6 Calculating Centers of Mass and Moments of Inertia**
  - Use double integrals to locate the center of mass of a two-dimensional object.
  - Use double integrals to find the moment of inertia of a two-dimensional object.
  - Use triple integrals to locate the center of mass of a three-dimensional object.
- **5.7 Change of Variables in Multiple Integrals**
  - Determine the image of a region under a given transformation of variables.
  - Compute the Jacobian of a given transformation.
  - Evaluate a double integral using a change of variables.
  - Evaluate a triple integral using a change of variables.
### Chapter 6

- **intro Vector Calculus (overview)**
- **6.1 Vector Fields**
  - Recognize a vector field in a plane or in space.
  - Sketch a vector field from a given equation.
  - Identify a conservative field and its associated potential function.
- **6.2 Line Integrals**
  - Calculate a scalar line integral along a curve.
  - Calculate a vector line integral along an oriented curve in space.
  - Use a line integral to compute the work done in moving an object along a curve in a vector field.
  - Describe the flux and circulation of a vector field.
- **6.3 Conservative Vector Fields**
  - Describe simple and closed curves; define connected and simply connected regions.
  - Explain how to find a potential function for a conservative vector field.
  - Use the Fundamental Theorem for Line Integrals to evaluate a line integral in a vector field.
  - Explain how to test a vector field to determine whether it is conservative.
- **6.4 Green’s Theorem**
  - Apply the circulation form of Green’s theorem.
  - Apply the flux form of Green’s theorem.
  - Calculate circulation and flux on more general regions.
- **6.5 Divergence and Curl**
  - Determine divergence from the formula for a given vector field.
  - Determine curl from the formula for a given vector field.
  - Use the properties of curl and divergence to determine whether a vector field is conservative.
- **6.6 Surface Integrals**
  - Find the parametric representations of a cylinder, a cone, and a sphere.
  - Describe the surface integral of a scalar-valued function over a parametric surface.
  - Use a surface integral to calculate the area of a given surface.
  - Explain the meaning of an oriented surface, giving an example.
  - Describe the surface integral of a vector field.
  - Use surface integrals to solve applied problems.
- **6.7 Stokes’ Theorem**
  - Explain the meaning of Stokes’ theorem.
  - Use Stokes’ theorem to evaluate a line integral.
  - Use Stokes’ theorem to calculate a surface integral.
  - Use Stokes’ theorem to calculate a curl.
- **6.8 The Divergence Theorem**
  - Explain the meaning of the divergence theorem.
  - Use the divergence theorem to calculate the flux of a vector field.
  - Apply the divergence theorem to an electrostatic field.
### Chapter 7

- **intro Second-Order Differential Equations (overview)**
- **7.1 Second-Order Linear Equations**
  - Recognize homogeneous and nonhomogeneous linear differential equations.
  - Determine the characteristic equation of a homogeneous linear equation.
  - Use the roots of the characteristic equation to find the solution to a homogeneous linear equation.
  - Solve initial-value and boundary-value problems involving linear differential equations.
- **7.2 Nonhomogeneous Linear Equations**
  - Write the general solution to a nonhomogeneous differential equation.
  - Solve a nonhomogeneous differential equation by the method of undetermined coefficients.
  - Solve a nonhomogeneous differential equation by the method of variation of parameters.
- **7.3 Applications**
  - Solve a second-order differential equation representing simple harmonic motion.
  - Solve a second-order differential equation representing damped simple harmonic motion.
  - Solve a second-order differential equation representing forced simple harmonic motion.
  - Solve a second-order differential equation representing charge and current in an RLC series circuit.
- **7.4 Series Solutions of Differential Equations**
  - Use power series to solve first-order and second-order differential equations.
