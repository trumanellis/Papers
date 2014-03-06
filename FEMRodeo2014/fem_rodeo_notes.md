<!--# FEM Rodeo Notes-->
## Space-Time DPG
Good afternoon. Looks like I'm the only thing between you and your evening, so I'm going to try to keep this brief.
My name is Truman Ellis, and I've been working with Dr. Demkowicz on DPG for fluid problems.
At past FEM rodeos I talked about some of our work on a locally conservative formulation of DPG. 
In this talk, I'm going to present some of our preliminary results on space-time DPG for transient CFD problems.
Implicit in all of this is our ultimate goal of designing a method that would be ideal for parallel CFD on future architectures, but this talk will not explicitly address the parallel programming side of things.

## Motivation
Before I begin, we'll start with an ultra-brief summary of DPG and why we might 
want to apply it to problems in CFD.
For one, DPG has proven very robust in the face of singularly
perturbed problems (think high Reynolds number flows).
You do not need a domain expert to craft well designed meshes for each new
problem. We are mathematically guaranteed to remain stable under very coarse
meshes while adaptively refining toward a solution.

Mathematically, DPG can be characterized as a minimum
residual method. This means that through the choice of specific optimal test
functions we automatically minimize the residual in the dual norm of a
Hilbert space V. We also have a well-defined process to generate the optimal
test functions which is computationally feasible.

## Heat Equation
### Simplest Nontrivial Space-Time Problem
We're just going to jump into a concrete problem and work from there.
The simplest representative spatial-temporal problem is the heat equation.
The interesting thing about this equation is that it is elliptic in space, but hyperbolic in time.
We can split this into two first order equations: conservation of energy and Fourier's law.
Notice that we can rewrite this as a constitutive equation and a space-time divergence.

### DPG Formulation
We then follow standard DPG procedure and multiply by test functions tau and v 
where tau is vector valued with dimension equal to the spatial dimension.
Then we integrate each equation by parts.
But the first equation is only integrated over spatial dimensions, so the resulting trace term is limited
to boundaries with a nonzero spatial normal component.
The integration by parts in space-time yields a flux that is defined on all boundaries, but with different
character across spatial and temporal boundaries.

### Pulsed Source Problem
Here we have a very contrived example problem. 
We start with a completely zero initial condition and then turn on a unit source from t = 1/4 to t=1/2,
then watch the inputted heat diffuse over the rest of the time interval.
The key thing to watch for is making sure we don't get any heat bleeding backwards in time. 
Indeed we get  very clean start at t=1/4.
Notice also how u hat exists only on vertical boundaries, while the flux lives on the entire mesh skeleton.
We also see how the method naturally picks on on areas of rapid temporal or spatial changes and adapts to resolve them.

## Compressible Navier-Stokes
### Strong Form
Now we make a giant leap of faith to the compressible Navier-Stokes equations, 
but all of the same ideas carry over.
We write our conservation equations in strong form with constitutive laws for the deviatoric stress tensor, heat flux, and pressure.

### First Order Space-Time Form
We follow the same course as we did for the heat equation and write this as a first order system of equations
with the conservation laws in space-time divergence form.

### DPG Formulation
Again we multiply by test functions and integrate by parts. In this case S is a symmetric tensor valued test function,
tau is a vector valued test function of spatial dimension, v_c and v_e are scalar valued, and v_m is vector valued matching the spatial dimension.
We've also introduced spatial traces u hat and T had and fluxes for each conservation law.

### Flux and Trace Variables
The above integration by parts gives the following definitions for the spatial traces and fluxes.
Notice the analog to the heat equation where the fluxes change nature depending on whether they are on temporal or spatial boundaries.

In the above bilinear form, the fluxes, traces, and heat flux are linear.
All of the other variables are involved in nonlinearities and will need to be linearized and solved via a Gauss-Newton iteration.

### Test Norm
Choice of test norm can be one of the most influential factors in the success of a particular DPG method.
For steady Navier-Stokes we developed a robust test norm by analogy to steady convection-diffusion.
We need to perform a similar analysis for space-time convection-diffusion, but we've found that the following norm
for Navier-Stokes seems to work better than the standard graph norm.
Essentially, we've taken the standard graph norm based off the adjoint equation and decoupled the Eulerian and viscous terms.

### Sod Shock Tube
We illustrate our space-time formulation with the Sod shock tube problem starting on an initially very coarse mesh of 4
space-time elements. 
Traditionally the Sod shock tube is defined for the Euler equations, 
but every numerical method that I know uses some sort of artificial viscosity to handle the shock.
We instead just solve the problem with a small physical viscosity of order 10^-5.
You can see that even on this extremely coarse mesh, we have a somewhat sound solution.
Moreover, the adaptive error control of DPG begins to work to refine the mesh in the correct areas in order to
resolve the flow features.
We'll step through each adaptive refinement step to see how the DPG solution converges to the exact solution.
You can see that after 14 refinement steps we are nearly right on top of the exact solution. 
With one or two more steps we could probably completely eliminate the tiny overshoots at the shock.

## Conclusions and Future Work
It is extremely helpful to be able to write the governing equations in terms of a space-time divergence
since that frames things in a way that we are familiar with from steady DPG.
The oddity is that this leaves traces on temporal edges undefined, so our code needs to know not to put degrees
of freedom there. 

These are all very preliminary results, but they give an indication of what we can expect in the future.
We still need to analyze the space-time convection-diffusion equation and develop robust norms in this context
before we can extend the ideas to Navier-Stokes.
We also have some rough work done on time-slabs which should improve the computational efficiency.
Obviously, we are going to need to move to two and three dimensional problems in order to simulate anything of interest.
My primary target is actually incompressible Navier-Stokes, which should be easier since we don't have to deal with shocks.
But in 1D incompressible gives absolutely trivial solutions, so we didn't pursue it here.
I don't know if we will get to this during my dissertation, but if we really want a scalable method, we need to address the 
lack of preconditioners for DPG and develop a decent iterative solver.