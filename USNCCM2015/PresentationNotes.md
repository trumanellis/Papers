# Proposal Presentation Notes

## Title Slide
Good afternoon, everyone. Thank you for coming to my talk. 
I wanted to present some work I've been doing with my collaborators Leszek Demkowicz, 
Bob Moser, Nate Roberts, and Jesse Chan developing a space-time DPG method for transient fluid flow applications.

## Overview of DPG
I'll start with a brief mathematical overview of the DPG method. 
I call DPG a framework for computational mechanics because it provides a methodology to derive families of stable finite element methods for any well posed variational problem.

This is a derivation of DPG for some abstract variational problem.

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

### Other Features
A few other interesting features of the DPG method.

The test space so far has not been defined, but if we were to use continuous test functions, then the auxiliary problem would turn into a global solve of similar complexity to the original problem. Introducing a broken test space localizes these solves making it embarrassingly parallel. The downside is that this introduces additional interface unknowns, which I will illustrate later with an example.

As a minimum residual method, the method always produces a hermitian positive definite stiffness matrix (SPD for real valued problems). We haven't really explored the implications for iterative solvers, but this seems like it would be a positive feature.

We can also evaluate the residual error without knowing the exact solution. This can be used to robustly drive adaptivity.

### Space-Time DPG
But before I put some equations down, let's briefly explore why we might want to work in a space-time framework rather than a traditional finite difference based time stepper. Adaptivity has been an integral part of DPG from day one, and we typically get refined elements which are several orders smaller magnitude than other elements in the mesh. Classical time stepping techniques propagate the entire solution forward in lockstep at the pace of the most restrictive element. Implicit techniques allow you to take larger steps but for the sake of temporal accuracy, you may not want to. Now, there are techniques out there that do allow different elements to proceed at different time steps, such as asynchronous variational integrators, but for us, this is not an ideal solution. Bolting on a different temporal integrator to a DPG spatial integrator produces a kind of Frankenstein of properties. We know we have great stability in space, but where does that leave us temporally? If we instead decide to just treat time as another dimension to be discretized with a DPG method, then we get a unified treatment and preserve all of our nice stability and adaptivity properties. We get automatic local time stepping and a kind of parallel-in-time integration as we can solve an entire time slab at once, distributing different space-time elements within the slab to different processors. I mentioned that space-time presents a challenge for classical finite elements as equations may have different spatial and temporal characteristics, but DPG addresses this concern. Is your space-time formulation well-posed? Yes, then we are in business. The big complication is on the computational and implementation side. Your code now has to support higher dimensional meshes or as we are implementing, a kind of tensor product of spatial and temporal elements.

## Space-Time Model Problem
That's enough for the features of DPG in abstract, let's derive a DPG method for a simple model problem of transient fluid flow, the convection-diffusion equation.
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

### Robust Norms for 2D Space-Time
We recently added the capability to perform 2D space-time computations in our DPG code. So here I just wanted to demonstrate that we get robust convergence in 2D for the same coupled robust norm norm on the left and another norm which I stumbled when experimenting with compressible Navier-Stokes solves.

## Space-Time Incompressible Navier-Stokes
Now that we are reasonably confident that 2D space-time DPG produces robust results, we can experiment with space-time incompressible Navier-Stokes. We begin by rewriting the equations in first order form with a space-time divergence operator as before.

### Ultra-Weak Formulation
Now we follow the same machinery as before of multiplying by test functions and IBP, introducing spatial trace unknowns for the velocity and flux unknowns from the conservation equations. I'm going to skip the linearization process in this talk.

### Taylor-Green Vortex Problem
Similar to our analytical convection-diffusion problem, we demonstrate robust convergence of L2 and energy error on the Taylor-Green vortex problem. We are currently working on solving more complicated problems, but are running into the realization that space-time can be very expensive. We are trying to mitigate this problem by implementing multigrid solvers in space-time with some promising initial results, but the work is ongoing.

## Space-Time Compressible Navier-Stokes
I'll get into some of our results applying the space-time methodology to compressible Navier-Stokes. I mentioned that space-time support in Camellia is still experimental, so the numerical results so far are limited to 1D space + time, but we are on the cusp of getting a tensor topology thing working for 2D and 3D computations. That is basically the last thing I need to do to graduate, actually. But here are the preliminary 1D results.

### First Order System
For the sake of simplicity, we assume Stokes hypothesis, ideal gas, and constant viscosity, but if we wanted to choose something more realistic for these, it would just make the linearization process a little messier. We start by splitting up our conservation equations into a first order system as we did with convection-diffusion, but here we jump straight into the space-time divergence form. Since the Navier-Stokes equations are incompletely parabolic, we only get 2 constitutive laws to the 3 conservation equations.

### Sod Problem
We start with everyone's favorite shock tube problem, the Sod problem. This is a spatially 1D problem from 0 to 1 with a final time of 0.2. So we introduce a starting space-time mesh with 4 quadratic elements where the y=0 axis corresponds to the initial conditions and y=0.2 is the final time. Now we are going to track the refinement process as the method automatically resolves the solution features. After 14 refinements, we've pretty much gotten our mesh down to the viscous scale along the shock.
I want to point out that we are now getting to the point where we can apply a multigrid solution strategy to the series of adaptive meshes that we generate here.

### Related Research
DPG is currently the subject of a lot of active research, and since I could only touch on a small part of that, I wanted to outline some of the other work being done. I only really talked about the fluid applications of DPG, but we've had very successful results with heat transfer, Helmholtz, Maxwell, solid mechanics, and a range of different fluid equations. In the future, we would like to start combining these to do true multiphysics simulations. 
The way we've currently been handling nonlinear problems is to just apply DPG to the linearized problem and perform a Gauss-Newton iteration to converge to the nonlinear solution. My advisor is currently exploring ideas to apply DPG directly to the nonlinear problem. 
Recently, we made some breakthroughs developing a non-Hilbert DPG theory. The motivation for working with non L2 spaces is Gibbs phenomenon. When you perform an L2 projection of a discontinuous function on continuous basis functions, you run into Gibbs phenomenon. But an L1 projection is known to eliminate overshoots and undershoots. Additionally, L1 is supposed to be a better function space for solutions of Navier-Stokes and Euler than L2.
One topic that has come up several times in the context of DPG for fluid problems is local conservation. For finite elements, local conservation is equivalent to having your test space span the set of constants. But we compute our test space on the fly, so it is not guaranteed that a linear combination of optimal test functions produces a constant. So a while back, I developed a theory for locally conservative DPG that uses Lagrange multipliers to explicitly enforce conservation element-by-element.
I touched on some of the recent work on iterative solvers, but this is currently becoming a priority for DPG research and we expect to see a lot more in the next year or so.
I've also been working on a way to use entropy to create physically meaningful test norms.
We also think that DPG, especially in the ultra-weak formulation, would be ideal for solving on general polyhedral elements. Since we can statically condense the internal degrees of freedom out of the global solve, we don't have to worry about creating conforming spaces for weird polyhedra, only their boundaries, which could just be a combination of triangles and quads. The internal degrees of freedom only live in L2 and are computed as a post-processing stage, so it would be easy to define basis functions for these. This work is still in conceptual phases since it would require a significant investment to work on the new data structures, but mathematically, we don't expect any significant obstacles.

