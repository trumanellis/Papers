# Proposal Presentation Notes
## TODO

## Title Slide
Good afternoon, everyone. Thank you for coming to my talk. 
I wanted to present some work I've been doing with my collaborators Leszek Demkowicz, 
Bob Moser, Nate Roberts, and Jesse Chan developing a new framework for scientific computing: the discontinuous Petrov-Galerkin finite element method.

## Motivation
Here is a brief outline of my talk. We will start with the motivations behind the method: to create an automated computing technology. Then I'll discuss the abstract derivation of the method and some of its properties. After this, I'll jump into some of my more recent work deriving a space-time version of the method for transient simulations. Throughout my PhD program, I've been working with Nate and Jesse on developing a parallel C++ code for DPG computations called Camellia, so I wanted to give some highlights of how that code works. Next, I'll show some of our computations of transient shock-tube problems with the full compressible Navier-Stokes equations and then conclude by mentioning some exciting related research.

### Navier-Stokes Equations
We will motivate with computational fluid dynamics, since that is what I am most familiar with, but each field of computational mechanics has its own challenges that we are interested in addressing.

Basically what I want to say on this slide is that Navier-Stokes is hard. Despite the decades of research that have been invested in simulating fluid flows, robust simulation is still a challenge.

* Numerical methods need to resolve a wide variety of flow features from shocks to boundary layers to turbulence.
* On top of that, most numerical methods have minimum mesh resolution requirements before convergence can be guaranteed. Meshes that are too coarse for the numerical method to converge on are termed to be in the pre-asymptotic regime. This means that in some sense, the mesh for the simulation to the phenomena on the right needs to anticipate the flow features before they are known.

### Initial Mesh Design
This requirement can present additional challenges to the CFD practitioner designing a mesh. At the minimum level, the surface mesh needs to adequately represent the physical geometry of the problem under consideration. But the stability of the numerical methods presents additional requirements on the volume mesh surrounding the surface mesh. This often leads to a trial and error process for the CFD engineer. 

### DPG on Coarse Meshes
My goal with this research is to remove one of those constraints on computational mechanics practitioners. In contrast to most other methods out there, the DGP method does not suffer convergence issues on coarse meshes. We are able to start on the coarsest mesh possible which sufficiently resolves the geometry and adaptively refine towards a resolves solution.
These are results from Jesse Chan's thesis on supersonic flow over a flat plate. This is not a remarkably difficult problem, but what is notable is that we were able to start the simulation on a mesh of only two elements, sit back, and let the method take over as it solved, refined, and converged to a resolved solution after 11 adaptive steps.

## Lessons from Other Methods
Before I jump into the particulars of DPG, I wanted to briefly touch on some of the methods that influenced our work and the lessons we learned from them. 
* The streamline Upwind Petrov-Galerkin method was really the first finite element method to successfully solve fluid problems. Put simply, SUPG was able to solve convection-diffusion type problems by adaptively upwinding the test functions based on the elements Peclet number. This introduced the idea that you could improve the stability of a finite element method by modifying your test space.
* Despite the similar name, DG methods only really have one significant influence on the DPG method. The realization that discontinuous basis functions or broken Sobolev spaces were fair game for finite element methods allowed the DPG method to progress from being an interesting trick to a practically computable method.
* Hybridized DG, or HDG is a newer variation of the DG method that seeks to address the main criticism of DG methods: that of proliferation of unknowns. For the lowest order DG method on a 3D hex mesh, the global solve will have 8 times as many unknowns as an equivalent continuous Galerkin method. HDG addresses this by adding new interface unknowns that couple elements together. Internal dofs no longer directly communicate with each other, and can be statically condensed out of the global solve, resulting in a global solve of comparable size to a continuous discretization. DPG likewise makes use of interface unknowns and static condensation.
* Least-Squares finite element methods attempt to turn any PDE into a least-squares solve, bypassing the LBB inf-sup stability conditions and producing a symmetric, positive definite global stiffness matrix. The insight is that finite element methods are most powerful in a Ritz type framework. DPG can be interpreted as a generalized least-squares method where instead of minimizing the residual in L2, we minimized it in a user-defined dual norm.
* Finally, space-time finite elements were proposed as a means to handle some of the disadvantages to attempting to time step a highly adapted mesh. Analysis shows that a unified treatment of space and time within one method can produce superior results for moving boundary problems, but producing a method which is stable both spatially and temporally has historically been a challenge.

## Overview of DPG
Now I'm going to present a brief mathematical overview of the DPG method. 

### Dual Minimum Residual Method
We will start with a variational formulation of our problem. Any variational formulation, as long as it is well posed. 

* So we are looking for a solution u in some trial space, big U.
* We've multiplied both sides by some test function v and somehow come out with a bilinear form on u and v.
* This bilinear form defines an operator which maps values from the trial space to the dual of the test space.
* We can then write the operator equation in V'
* Now we wish to find the solution u_h which minimizes the residual for some finite dimensional subset of big U
* The dual space norm is not especially convenient to work with computationally, but another functional analysis construct makes this more accessible. 
* The inverse Riesz map, which is an isometry, turns this into a standard norm.
* Before I move on with the derivation of the method, I wanted to point out that really, this is a generalization of the least squares finite element method. If we chose the L2 topology for V, we would get the standard least squares method. But now we are free to define the test space topology however we want.

### Optimal Petrov-Galerkin Methods
* Since we have a minimization problem, we want to find the critical points, so we take the Gateaux derivative.
* We can then reverse one of the Riesz maps to give this duality pairing, which if you squint your eyes, kind of looks like a new bilinear form with a very special test function defined through the inverse Riesz map and operator B.
* The one complication is that the Riesz map is defined through the test space inner product, so evaluation of the optimal test functions requires an auxiliary problem with the test space inner product on the LHS and the bilinear form operator on the RHS.

### Mixed Formulation
In addition to a minimum-residual method and a Petrov-Galerkin method with optimal test functions, there is a third interpretation of DPG as a mixed problem. If we identify the error representation function as the inverse Riesz map of the residual,
we can write an equivalent saddle-point mixed formulation where you are simultaneously solving for the error representation function and the approximate solution. The curious thing about this formulation is that the approximate solution, uh, plays the role of Lagrange multiplier for the error representation function. This particular interpretation carrier much larger global solve, but is useful for analytical purposes and when defining a non-Hilber Lp version of DPG which I will touch on later.

### The Most Stable Petrov-Galerkin Method
Babuska's theorem guarantees that discrete stability and approximability imply convergence. So given a bilinear form with discrete inf-sup constant gamma_h, then the Galerkin error will be bounded by M, gamma_h, and the best approximation error.
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

* Exceptional stability properties prevent a solve from crashing, eliminating expensive restarts
* The method runs robustly on a wide range of Reynolds numbers
* Adaptivity allocates degrees of freedom efficiently to allow larger simulations with fewer resources
* Automaticity means that you can start a simulation and let it solve and adapt without needing to jump in and fix things part way through
* DPG is very compute intensive, with a large portion of the work being done in the embarrassingly parallel local solves and stiffness matrix assembly. 
* In our code, we do the local solves via QR factorization. But the local solve can be viewed as having multiple right hand sides, so that QR factorization can be recycled multiple times.
* Degrees of freedom can be separated into two categories: internal and trace. The internal degrees of freedom can be condensed out and the global solve can be conducted purely in terms of the trace variables which have limited coupling, reducing fill in of the stiffness matrix. The internal DOFs can then be solved for in an embarrassingly parallel post-processing phase. This is a similar process behind the hybridized DG method.
* As I mentioned earlier, an SPD stiffness matrix seems like a promising thing for iterative solvers, but we haven't really explored the benefits.
* Many supercomputer simulations are increasingly coupling multiphysics. The only stability requirement for a DPG method is that the continuous problem is well-posed. As such, it has successfully been applied to a wide range of problems from Helmholtz to solid mechanics to Navier-Stokes and Maxwell's equations.

## Space-Time Model Problem
That's enough for the features of DPG in abstract, let's derive a DPG method for a simple model problem of transient fluid flow, the convection-diffusion equation.
### Motivation
But before I put some equations down, let's briefly explore why we might want to work in a space-time framework rather than a traditional finite difference based time stepper. Adaptivity has been an integral part of DPG from day one, and we typically get refined elements which are several orders smaller magnitude than other elements in the mesh. Classical time stepping techniques propagate the entire solution forward in lockstep at the pace of the most restrictive element. Implicit techniques allow you to take larger steps but for the sake of temporal accuracy, you may not want to. Now, there are techniques out there that do allow different elements to proceed at different time steps, such as asynchronous variational integrators, but for us, this is not an ideal solution. Bolting on a different temporal integrator to a DPG spatial integrator produces a kind of Frankenstein of properties. We know we have great stability in space, but where does that leave us temporally? If we instead decide to just treat time as another dimension to be discretized with a DPG method, then we get a unified treatment and preserve all of our nice stability and adaptivity properties. We get automatic local time stepping and a kind of parallel-in-time integration as we can solve an entire time slab at once, distributing different space-time elements within the slab to different processors. I mentioned that space-time presents a challenge for classical finite elements as equations may have different spatial and temporal characteristics, but DPG addresses this concern. Is your space-time formulation well-posed? Yes, then we are in business. The big complication is on the computational and implementation side. Your code now has to support higher dimensional meshes or as we are implementing, a kind of tensor product of spatial and temporal elements.

### Space-Time DPG for Convection-Diffusion
The heat equation is the simplest transient fluid problem we can think of. As we will see later, it actually serves as a decent model problem for something as complicated as compressible Navier-Stokes. Just like Navier-Stokes, it is parabolic in space-time. 
I am going to derive one variational problem for this equation, but there are other choices we could make. In particular, early in DPG's history, we decided to focus on the ultra-weak first order formulation because we believed it presented the most flexibility, but increasingly we have been working with the original second order problem.
So as we decompose this into a system of first order equations, we get a constitutive law in space and conservation of mass. The key insight is that we can rewrite our conservation law as a space-time divergence operator.

### Ultra-Weak Formulation
This is still in strong form, so let's multiply by test functions tau and v, and integrating by parts over each element. IBP of the stress equation introduces a trace unknown u hat.
If we were working with a conforming test space, the integration of this term against tau dot n over element boundaries would cancel, but the cost of a discontinuous test space is new interface unknowns.
Similarly, IBP of the conservation equation introduces flux t hat. The trace only exists on spatial boundaries because the stress equation is only integrated by parts over spatial dimensions. Note that the flux changes nature depending on whether it is on a temporal or spatial boundary or a mix of the two.

### Robust Norms
So you're probably thinking, this sounds awesome: any formulation I like, choose the norm I converge in, unlimited stability, that's great. Here is where I bring up the little caveat in the method.
Let's say we want to develop a method that converges in a norm that is bounded by L2.
So let's write our bilinear form in group variables where u represents the volume parts and uhat the interface parts. And since we are working with the ultra-weak first order system, we have the adjoint on the volume integrated test functions. Now the space of continuous test functions is a subspace of our discontinuous test functions, so lets take a conforming test function v* which satisfies the adjoint equation. If we plug this into our bilinear form, we get the L2 norm of u. Then multiplying and dividing by the V norm of v*, we can bound this by the supremum, which is by definition of the energy norm in which we are guaranteed best approximation. So as long as the V norm of v* is bounded by the L2 norm of u, then convergence in the energy norm implies convergence in L2.
I've put together a little space-time test problem to numerically check this assertion.

### Norm Comparison
There are an infinite number of norms with this property, so lets pick two of them and compare. The graph norm, defined by the adjoint equation is on the left and another norm, I will call the robust norm is on the right. In the plots, we see the L2 and energy error during an adaptive solve for decreasing diffusion parameters. Ideally the L2 error (dashes) and energy error (dots) should parallel each other and monotonically decrease. Yet we only see the desired behavior in robust norm. This comes down to conditioning and approximability of the optimal test functions.

### Ideal Optimal Test Functions
The very desirable properties of DPG assume that we are using optimal test functions from an infinite dimensional space V, but in order to make this computationally tractable, in practice we use a finite dimensional enriched space in the auxiliary problem. Different test norms will produce different ideal optimal test functions. Here we see the optimal test functions corresponding to a linear trial basis function with the two norms. The graph norm optimal test functions have very strong boundary layers that we could not hope to approximate with any reasonable enriched space. 

### Approximated Optimal Test Functions
Here we see what the actual approximated test functions would look like for the two norms. There is little difference between the ideal and approximated shape functions with the robust norm, but a cubic approximation of the sharp boundary layers in the graph norm is not sufficient, and our overall convergence suffers. Most of the labor of designing a DPG method goes into analysis of the auxiliary solve to make sure we get boundedness by L2, approximable test functions, and good conditioning. But ultimately, this boils down to some fairly basic functional analysis and understanding of PDEs.

## Camellia: DPG for the Masses
Before I show some real numerical results, I wanted to highlight some of the features of the code we have spent the last few years developing. Camellia is named after camellia sinensis, the tea plant, because Nate, our code architect is kind of into his tea.
Camellia aims to make DPG research and experimentation as simple as possible while simultaneously scaling to HPC systems. Camellia is heavily inspired by Fenics, Deal II, and libMesh and has a syntax that mirrors the variational forms very closely. It uses MPI for distributed stiffness matrix computations, supports 1, 2, and 3 dimensional problems, curvilinear elements in 2D so far, h- and p- refinements, arbitrarily irregular meshes, and modular refinement strategies. We experimentally support space-time computations and some basic iterative solvers which have scaled well up to 32,000 cores.

### Building the Bilinear Form
Excluding the #includes, I'm going to walk through a simple driver for convection-diffusion in 3 slides. The mathematical representation will be on the right, and the code implementation on the left. First, we need to define our trial variables. The field variables u and sigma live in L2 on element interiors while traces uhat and tn are traces and fluxes in H1/2 and H-1/2, respectively. Then, for a diffusion parameter of 0.01, and convection field (1,2) we define our bilinear form. You can see that the terms on the right are mirrored in the code.

### Boundary Conditions and Mesh
Next, we need to create a mesh and boundary conditions. We will use second order polynomials and a square mesh. Delta k is the degree of enrichment for our enriched space, so the auxiliary solves will be carried out on 4th order polynomials element-by-element. We will apply flux boundary conditions on the inflow and trace conditions on the outflow to create a boundary layer. Note that we are using convenience functions for our simple boundaries, but it is possible to subclass SpatialFilter to match any geometry you want. 

### Solving
The last thing we need to specify is the test norm. I know I said that the graph norm was not robust for convection-diffusion, but it wasn't so bad with a mild diffusion parameter of 10^-2. And since it is based on the adjoint, Camellia can provide a convenience function to assemble it automatically. If we wanted to choose something else, the syntax is similar to the bilinear form assembly in the first slide. The default refinement strategy integrates the error representation function over each element and refines every element within a certain threshold of the max value. Camellia supports parallel HDF5 based solution output. We then enter into a solve and refine loop where we output the solution and energy error after each solve.

### Computed Solution
After the loop, we've fully resolved the solution features, and we can see that the method automatically picks up the boundary layers. The initial mesh was a single element.
We could also display the stress and flux, but you get the idea from these two plots.

## Towards a Robust Iterative Solver
Iterative solvers are a fairly recent addition to the DPG fold, but some of the initial results are pretty encouraging. We recently started experimenting with a combination of conjugate gradient, p-multigrid preconditioners and Schwarz smoothers for Poisson and Stokes flow. The encourage fair comparisons, each element resides on its own MPI rank.

### Poisson 1D
Starting with 1D Poisson, we can see that the required number of iterations to reduce error by a factor of 10^10 quickly becomes mesh independent and settles at a mere 19 iterations regardless of the polynomial order.

### Stokes 2D
Moving onto a slightly more challenging case of 2D Stokes, we start seeing a dependence between the number of iterations and the solution polynomial order, but this too levels off after a point.

### Stokes 3D
Finally, moving to 3D Stokes on a 16 cubed mesh (4096 elements). Here, we throw in the use of incomplete Cholesky factorization. It appears that the curve is leveling off, but one more level of refinements would require 32,000 cores. We have scaled the code to this level so far, but that was just 3D Poisson.
These results were only generate in December, and it's unclear how well the techniques will extend to convection dominated diffusion, but you have to start somewhere.


## Space-Time Compressible Navier-Stokes
Now that I've finished that little advertisement for Camellia, I'll get into some of our results applying the space-time methodology to compressible Navier-Stokes. I mentioned that space-time support in Camellia is still experimental, so the numerical results so far are limited to 1D space + time, but we are on the cusp of getting a tensor topology thing working for 2D and 3D computations. That is basically the last thing I need to do to graduate, actually. But here are the preliminary 1D results.

### First Order System
For the sake of simplicity, we assume Stokes hypothesis, ideal gas, and constant viscosity, but if we wanted to choose something more realistic for these, it would just make the linearization process a little messier. We start by splitting up our conservation equations into a first order system as we did with convection-diffusion, but here we jump straight into the space-time divergence form. Since the Navier-Stokes equations are incompletely parabolic, we only get 2 constitutive laws to the 3 conservation equations.

### Compact Notation
For our own sanity, I introduce a compact notation so I can focus on the overall structure of the equations. So we have our conserved quantities C, for each equation, the Euler fluxes, the viscous fluxes, the viscous fluxes, and what I am calling the viscous relations.

### Group Variables
The I further compact things by introducing group variables. This lets me rewrite my system to look nearly identical to convection-diffusion. I am going to skip the ugly linearization process and definitions of test norms, but we the test norm was chosen by a combination of numerical experiments and analogy to convection-diffusion. Note that we have not introduced any kind of artificial viscosity or shock capturing. In the long run, we think some sort of shock capturing could allow us to produce better results, but I just wanted to demonstrate that we were able to get decent results with vanilla DPG.

### Sod Problem
We start with everyone's favorite shock tube problem, the Sod problem. This is a spatially 1D problem from 0 to 1 with a final time of 0.2. So we introduce a starting space-time mesh with 4 quadratic elements where the y=0 axis corresponds to the initial conditions and y=0.2 is the final time.