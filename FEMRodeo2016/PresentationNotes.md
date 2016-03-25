### Title Slide
Talk number: 29, second session Saturday morning.
du/dx + dv/dy + dw/dz - 1/3(du/dx+dv/dy+dw/dz) - 1/3(du/dx+dv/dy+dw/dz) - 1/3(du/dx+dv/dy+dw/dz)
w = 0
du/dx + dv/dy - 1/3(du/dx+dv/dy) - 1/3(du/dx+dv/dy) - 1/3(du/dx+dv/dy)

|du/dx+du/dx dv/dx+du/dy dw/dx+du/dz|    |du/dx+dv/dy+dw/dz      0                 0           |
|du/dy+dv/dx dv/dy+dv/dy dw/dy+dv/dz|-2/3|     0            du/dx+dv/dy+dw/dz      0           |
|du/dz+dw/dx dv/dz+dw/dy dw/dz+dw/dz|    |     0                 0            du/dx+dv/dy+dw/dz|
w = 0
|du/dx+du/dx dv/dx+du/dy 0|    |du/dx+dv/dy      0           0     |
|du/dy+dv/dx dv/dy+dv/dy 0|-2/3|     0      du/dx+dv/dy      0     |
|     0           0      0|    |     0           0      du/dx+dv/dy|

d(w)/dt + d(uw)/dx+d(vw)/dy+d(ww)/dz+d(rho*R*T)/dz+2/3*d(du/dx+dv/dy)/dz

Good afternoon, everyone. Thank you for coming to my talk. 
I wanted to present some work I've been doing with my collaborators Leszek Demkowicz, 
Bob Moser, Nate Roberts, and Jesse Chan developing a space-time DPG method for transient fluid flow applications.

### Overview of DPG
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

### Space-Time DPG
But before I put some equations down, let's briefly explore why we might want to work in a space-time framework rather than a traditional finite difference based time stepper. Adaptivity has been an integral part of DPG from day one, and we typically get refined elements which are several orders smaller magnitude than other elements in the mesh. Classical time stepping techniques propagate the entire solution forward in lockstep at the pace of the most restrictive element. Implicit techniques allow you to take larger steps but for the sake of temporal accuracy, you may not want to. Now, there are techniques out there that do allow different elements to proceed at different time steps, such as asynchronous variational integrators, but for us, this is not an ideal solution. Bolting on a different temporal integrator to a DPG spatial integrator produces a kind of Frankenstein of properties. We know we have great stability in space, but where does that leave us temporally? If we instead decide to just treat time as another dimension to be discretized with a DPG method, then we get a unified treatment and preserve all of our nice stability and adaptivity properties. We get automatic local time stepping and a kind of parallel-in-time integration as we can solve an entire time slab at once, distributing different space-time elements within the slab to different processors. I mentioned that space-time presents a challenge for classical finite elements as equations may have different spatial and temporal characteristics, but DPG addresses this concern. Is your space-time formulation well-posed? Yes, then we are in business. The big complication is on the computational and implementation side. Your code now has to support higher dimensional meshes or as we are implementing, a kind of tensor product of spatial and temporal elements.

### Space-Time Model Problem
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

### Two Robust Norms for Steady Convection-Diffusion
We've successfully used the following norms for steady state convection-diffusion problems. The first norm was derived and proved to be robust by Jesse Chan, Norbert Heuer, and Leszek Demkowicz. Jesse and I later realized that for some problems we could get much better results by replacing the Div Tau term with a term coupling Div Tau and Beta dot Grad V. Based on the previous proof of robustness, this norm was also trivially robust.

### Two Robust Norms for Transient Convection-Diffusion
In adapting these norms for transient convection-diffusion, we treat dv/dt as if it were just convection in time and write Beta tilde as the spatial convection field augmented with 1 for temporal convection while defining a space-time gradient operator. The only change we make to our norms is replacing Beta dot Grad v with Beta tilde dot Gradxt V.

### Adjoint Operator
Now I'm going to outline to proof of robustness. We begin by writing the first order system with homogeneous boundary conditions: flux conditions on the inflow and trace on the outflow. I can go through the derivation later if you care, but the adjoint can essentially be thought of as reversing any convection directions. So we get our adjoint operator A*.

### Controlling Different Field Variables
We begin by splitting our adjoint into two parts, one with a forcing term on the conservation law and the other with forcing on the constitutive law. We then try to derive bounds on the two parts independently. Bounds on v1 and tau1 correspond to having robust control of our primary field variable u while v2 and tau2 corresponds to controlling the stress sigma.

### Proved Bounds at Our Disposal
In our recently submitted paper, we prove the following lemmas. The first one holds for both v1 and v2 while the second we could only prove for v1.

### Control of u
We can use the previous two lemmas and definition of the first split adjoint equation to develop the following bounds. These account for all the terms in both the robust and the coupled robust norm guaranteeing at the very least that we get robust control of our primary field variable u.

### Control of sigma
However for v2 and tau2, we only have lemma 1 at our disposal which means that we can only develop bounds on the following terms which means that we can not mathematically guarantee that either of these norms gives us robust control of sigma.

### Transient Analytical Solution
We developed the following analytical solution to test our claims of robustness. We have a transient impulse that dies away to a solution of the steady state convection-diffusion problem.

### Robust Convergence to Analytical Solution
We try this out for a range of different diffusion coefficients from 10^-2 to 10^-8 and plot the reported energy error and L2 error for different polynomial orders with the two norms. As expected, we get robust convergence in every case.



