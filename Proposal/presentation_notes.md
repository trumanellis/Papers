# Proposal Presentation Notes
## Title Slide
Good afternoon, everyone. My name is Truman Ellis. Thank you for coming to my proposal.
I'm going to be discussing some of my preliminary work toward a space-time discontinuous Petrov-Galerkin finite element method for transient fluid dynamics problems and the proposed extensions to this work.

## Motivation
I'll start with some motivations for why we would want to apply DPG to CFD, then I'll give you a brief mathematical overview of the DPG method, followed by some of my completed work on a locally conservative DPG formulation. Next, we will look at some of the challenges that exist in space-time along with some preliminary numerical results and finally what I propose to do next.

### Navier-Stokes Equations
The Navier-Stokes equations govern fluid motion, and solving them is a vital factor in many fields of engineering design. However, the nature of the equations has rendered them much more difficult to solve than many other governing equations. 

* Resolution of solution features can require several orders of magnitude difference between different parts of the domain
  * Uniform resolution at the finest level is impractical
  * Additionally, we have different resolution demands for different flow features such as shocks, boundary layers, and turbulence
* The equations are nonlinear and convergence can often be very difficult
* Most numerical methods experience limitations when it comes to solving on coarse or adaptive grids
* Higher order in particular can be an issue

### Initial Mesh Design
Due to stability limitations on coarse meshes, mesh design becomes a laborious and time-consuming process. Most numerical methods have a pre-asymptotic regime which means that unless the simulation mesh is fine enough, convergence is not guaranteed.
Thus, the initial mesh must be fine enough to put the simulation within the asymptotic regime.

The CFD engineer then has several constraints on their initial mesh design.

* The absolute minimum requirement is that physical geometry must be adequately represented
* Stability requirements require the volume mesh to sufficiently resolve flow features before those flow features are known. The engineer has to guess and estimate where greater resolution will be necessary.
* Turbulence models often have further requirements about the size of the mesh elements closest to the wall.
* This often becomes a process of trial and error. The engineer designs a mesh, attempts to run CFD on it, discovers that it crashes, investigates the error, attempts to correct it, and repeats.
* This is not an acceptable coarse of action on high performance computing systems where a single run can take up tens or hundreds of thousands of processors.

### DPG on Coarse Meshes (11 meshes)
Contrary to most other methods out there, DPG does not have a pre-asymptotic regime, which means that we can start simulations on the coarsest possible mesh that adequately represents the geometry. Here we have supersonic flow over a flat plate. The exact solution will have both an oblique shock and boundary layer that need to be resolved. 

You can see that we are able to start on a mesh of only 2 elements, and the simulation converges. It is way underresolved, but at least things are sane.

DPG comes with an error representation function which represents the solution residual, allowing us to adaptively drive refinements which eventually resolve the solution.

This capability to start on extremely coarse meshes and automatically resolve the solution removes a major requirement from the mesh design process, potentially saving a lot of time.

## Overview of DPG
Now I'm going to present a brief mathematical overview of the DPG method. For more on the method, I would recommend Dr. Demkowicz's DPG Overview paper.
### Dual Minimum Residual Method
We start with an abstract variational form and apply some basic functional analysis to it.

* So we are looking for a solution u in some trial space, big U.
* We've multiplied both sides by some test function v and somehow come out with a bilinear form on u and v.
* This bilinear form defines an operator which maps values from the trial space to the dual of the test space.
* We can then write teh operator equation in V'
* Now we wish to find the solution u_h which minimizes the residual for some finite dimensional subset of big U
* The dual space norm is not especially convenient to work with computationally, but another functional analysis construct makes this more accessible. 
* The inverse Riesz map, which is an isometry, turns this into a standard norm.
* Before I move on with the derivation of the method, I wanted to point out that really, this is a generalization of the least squares finite element method. If we chose the L2 topology for V, we would get the standard least squares method. But now we are free to define the test space topology however we want.

### Optimal Petrov-Galerkin Methods
* Since we have a minimization problem, we want to find the critical points, so we take the Gateaux derivative.
* We can then reverse one of the Riesz maps.
* This gives us a new bilinear form with new optimal test functions defined through the inverse Riesz map and B operator applied to the trial functions.
* The one complication is that the Riesz map is defined through the test space inner product, so evaluation of the optimal test functions requires an auxiliary problem with the test space inner product on the LHS and the bilinear form operator on the RHS.
* We might call these optimal Petrov-Galerkin methods.

### The Most Stable Petrov-Galerkin Method
Babuska's theorem guarantees that discrete stability and approximability impy convergence. So given a bilinear form with discrete inf-sup constant gamma_h, then the Galerkin error will be bounded by M, gamma_h, and the best approximation error.
But the optimal test functions are defined such that they realize the supremum and the discrete gamma_h is greater than or equal to the continuous constant gamma.
If continuous problem is well-posed, OPG will be as well.
Furthermore, using the energy norm in the above estimates gives M = gamma = 1, and the optimal Petrov-Galerkin method is the most stable Petrov-Galerkin method possible.

### Other Features
A few other interesting features of the DPG method.

The test space so far has not been defined, but if we were to use continuous test functions, then the auxiliary problem would turn into a global solve of similar complexity to the original problem. Introducing a broken test space localizes these solves making it embarrassingly parallel. The downside is that this introduces additional interface unknowns, which I will illustrate later with an example.

As a minimum residual method, the method always produces a hermitian positive definite stiffness matrix (SPD for real valued problems). We haven't really explored the implications for iterative solvers, but this seems like it would be a positive feature.

We can also evaluate the residual error without knowing the exact solution. This can be used to robustly drive adaptivity.

### High Performance Computing
Finally a few notes on some of the implications for high performance computing.
The goal is to design a method that eliminates human intervention as much as possible.

* Exceptional stability properties prevent a solution from crashing, eliminating expensive restarts
* The method runs robustly on a wide range of Reynolds numbers
* Adaptivity allocates degrees of freedom efficiently to allow larger simulations with fewer resources
* Automaticity means that you can start a simulation and let it solve and adapt without needing to jump in and fix things part way through
* DPG is very compute intensive, with a large portion of the work being done in the embarrassingly parallel local solves and stiffness matrix assembly. Also, higher order methods tend to prevent a better compute/memory/communication profile than low order methods, and exceptional stability makes high order very easy.
* In our code, we do the local solves via QR factorization. But the local solve can be viewed as having multiple right hand sides, so that QR factorization can be recycled multiple times.
* Degrees of freedom can be separated into two categories: internal and trace. The internal degrees of freedom can be condensed out and the global solve can be conducted purely in terms of the trace variables which have limited coupling, reducing fill in of the stiffness matrix. The internal DOFs can then be solved for in an embarrassingly parallel post-processing phase. This is a similar process behind the hybridized DG method.
* As I mentioned earlier, an SPD stiffness matrix seems like a promising thing for iterative solvers, but we haven't really explored the benefits.
* Many supercomputer simulations are increasingly coupling multiphysics. The only stability requirement for a DPG method is that the continuous problem is well-posed. As such, it has successfully been applied to a wide range of problems from Helmholtz to solid mechanics to Navier-Stokes and Maxwell's equations.

## Local Conservation
Now I'll go over some of my work developing 
### DPG for Convection-Diffusion
We'll start with the convection-diffusion equation as a model problem, but later get into some numerical tests with Stokes. Here we see the strong form of the PDE with concentration u, convection vector beta, diffusion epsilon, and source/sink g.

We prefer to work with a system of first order PDEs, but it's possible to do DPG directly on the second order problem. The first equation represents our conservation law, and the second a constitutive law for stress sigma.

Proceed by multiplying by test functions v and tau, then integrating by parts over each element K. Note that the test functions are discontinuous between elements. We seek field variables u and sigma in L2, but this leaves their traces between elements undefined. So we introduce new flux and trace unknowns t hat and u hat. Putting it all together we get our new bilinear form.

### Local Conservation for Convection-Diffusion
What does local conservation mean in the context of convection-diffusion? We essentially just want the net flux through element edges to be balanced by any source terms internal. If we were to look at the bilinear form on the previous slide, this is equivalent to having a particular test function in the test space, namely v = 1 and tau = 0. Unfortunately, due to the dynamically computed nature of DPG, we can't guarantee that this will happen with standard DPG. However, we can explicitly augment our test space via Lagrange multipliers. The Lagrangian for our newly conservative scheme appears below.

### Locally Conservative Saddle Point System
Proceeding as before, we find the critical points, but now we end up with a saddle point system rather than the symmetric positive definite stiffness matrix (which still resides in the upper left hand corner). We've also added an additional unknown for each element. An additional nicety is that since we've explicitly added constants to the test space, we only need to search for optimal test functions in a space orthogonal to constants.

### Optimal Test Functions
Here is how we do our optimal test function solve. For each trial function u, we need to find it's complementary optimal test function v_u such that the inner product of v_u with some w equals the bilinear form acting on u and w for all w in V. Technically space V is infinite dimensional, but in order to make this computationally tractable, we use an enriched space to approximate the optimal test functions. This approximation can be troublesome when the inner product contains boundary layers as it can with convection-diffusion. Fortunately, the topology of the V space is our choice, and we can choose the test norm that we want. We've found that the following one works well for convection-diffusion. The only caveat is that the theoretical development of this norm required certain assumptions. Namely, the final L2 norm on v was slightly annoying when the convection term degenerated to zero. This term was only added to make this a full norm, but since we now only need to search for test functions in a space orthogonal to constants, we can replace this with a weaker term. Adding a zero mean term singles out a single test function from orthogonal space. We've also found that this zero mean term has better conditioning properties as we shrink the mesh elements.

### Stability and Robustness Analysis
In our paper, we go through a proof that this locally conservative DPG formulation is still stable and robust, but I'll just give the outline here. Since we are now working with a saddle point problem, it makes sense to follow a Brezzi style analysis. So the a bilinear form is our standard DPG system and c is the Lagrange multiplier terms. We proved that we satisfy the separate inf-sup and inf-sup in kernel conditions. Then we showed robustness by switching to the energy norm in the Brezzi analysis. If you want to read the details, they are in our paper, but since I'm more of a computational person, I'm going to jump right into the numerical tests of the method.

### Erickson-Johnson Problem
This is one of the few convection-diffusion problems with an exact solution, shown below. On the left we see our energy and L2 error for standard DG vs the conservative formulation. You can see that the conservative one lies nearly on top of the standard, showing at the least that it is not hurting us. You can also see plots of two different measures of conservation for the two methods. You can see that standard DPG isn't too bad and gets better with refinements, while the conservative one bumps around near machine precision.

### Stokes Cylinder
That was an easy problem, but let's see how the method does on a notoriously bad one. This is Stokes flow over a cylinder with a narrow channel on either side. Least squares methods will lose nearly 100% of the mass flux around the cylinder, and since DPG can be viewed as a kind of generalized least squares, we might expect a similar issue. On coarse meshes, standard DPG does indeed produce a poor solution, but converges with resolution. THe locally conservative one produces a decent solution on even very coarse meshes.

Here you can see measures of mass loss at different points in the domain, and indeed you do see the standard DPG method getting better with refinement. Conservative DPG on the other hand bumps around at almost exactly zero mass loss.

### Stokes Step
The reentrant corner in this problem again causes problems for least squares methods, but the conservative DPG method handles in beautifully. It's not until the standard method resolves the singularity at the corner that it really gets the flow profile correct.

And we see the same kind of story with the mass loss profiles. 

## Space-Time DPG
### Motivation
Now I'm going to get into some of the details of my recent work on a space-time DPG formulation for transient problems. The work of Nate Roberts and Jesse Chan on incompressible and compressible Navier-Stokes focused entirely on steady-state problems, but that limits possible applications considerably.

We did explore the possibility of tacking on a finite difference based time stepping algorithm like most of the other methods out there, but ultimately decided it was not the best course of action. Standard time stepping methods require the entire mesh to move forward at the pace of the most restrictive element. For adaptive meshes we may have several orders of magnitude between the largest and smallest elements, which results in a very inefficient technique. There are technique out there to allow different elements to march at different time steps such as asynchronous variational integrators, but that means bolting on another complicated technology to DPG. At the same time, we would lose a lot of the attractive stability and adaptivity features of DPG in the time domain.

* The advantages of doing DPG in full space-time is that we preserve the exceptional stability and robustness properties of DPG.
* We treat time just like another dimension and get a unified theory for the whole thing
* Local spatial adaptivity usually requires temporal adaptivity as well, and this happens naturally in this case. We also have the option of doing anisotropic refinements if needed.
* Space-time has also become a popular framework for moving with moving meshes

* The downsides are that this is significantly more difficult to implement
* We now have to deal with meshes of one higher dimension. For 3D simulations, you would need a 4D mesh, which is a bit harder to think about. We only plan on doing 2D, but it is still a challenge.
* Equations also tend to have different characteristics in space vs time. For example, Navier-Stokes is second order in space with a diffusion operator, but only first in space. This means that certain traces are defined on spatial boundaries but not temporal ones.
* Each solve will be more expensive since it has a higher dimensionality, but hopefully we can make up for that by advancing larger elements at larger effective time steps. Also, time slabs should cut down on the overall cost.

### Heat Equation
The heat equation is the simplest nontrivial space-time PDE. As we will see later, it actually serves as a decent model problem for something as complicated as compressible Navier-Stokes. Just like Navier-Stokes, it is parabolic in space-time. So as we decompose this into a system of first order equations, we get a Fourier's law in space and conservation of energy. The key insight is that we can rewrite our conservation law as a space-time divergence operator.

### DPG Formulation
We then proceed as usual, multiplying by test functions tau and v, and integrating by parts over each element. IBP of Fourier's law introduces a trace unknown u hat, while conservation of energy introduces flux t hat. The trace only exists on spatial boundaries Fourier's law is only integrated by parts over spatial dimensions. Note that the flux changes nature depending on whether it is on a temporal or spatial boundary or a mix of the two.

### Pulsed Source Problem
We have one simple proof of concept numerical test. 

# Exam Notes
## Boundary Layer Equations
1. Nondimensionalize variables
2. Substitute into incompressible Navier-Stokes equations
3. Following Prandtl, assume thickness of boundary layers small relative to characteristic length in streamwise direction
4. Estimate magnitude of terms
5. Drop smaller magnitude terms

## Turbulence Modeling
Nonlinear convection-diffusion-reaction with positivity requirements

# TODO
* Proof outline
* Study
    * Boundary layer equations
    * Rankine-Hugoniot conditions
    * Static Condensation
    * Derivation of interface unknowns
* Suit
* Food