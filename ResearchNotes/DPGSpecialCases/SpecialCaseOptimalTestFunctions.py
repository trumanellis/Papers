from dolfin import *
import numpy as np
import pylab as pl

# Create mesh and define function space
N = 10000;
p = 1;
pfine = 1;
r = 1
mesh = IntervalMesh(N, -2, 2)
finemesh = IntervalMesh(r*N, -2, 2)

# For Primal
Vp = FunctionSpace(mesh, "Lagrange", p)
Vpfine = FunctionSpace(finemesh, "Lagrange", pfine)
# TAU = VectorFunctionSpace(mesh, "CG", p)
# E = V*TAU
# TAUfine = VectorFunctionSpace(finemesh, "CG", pfine)
# Efine = Vfine*TAUfine

u0 = Constant(0)
# u0 = Expression('-x[0]/4')

def u0_boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(Vp, u0, u0_boundary)

epsilon = 1
beta = Constant((1,))

# Define variational problem
v = TrialFunction(Vp)
dv = TestFunction(Vp)

class HatExpression(Expression):
    def eval(self, value, x):
    	if (x > -1 and x <= 0):
    		value[0] = 1+x[0]
    	elif (x > 0 and x < 1):
    		value[0] = 1-x[0]
    	else:
    		value[0] = 0
u = HatExpression(domain=mesh)

# L2 Norm
# a = inner(v,dv)*dx

# Scaled H1 Norm
c = 1e-0;
a = c*inner(v,dv)*dx + inner(grad(v),grad(dv))*dx

# Grad Norm (requires boundary conditions for a unique solution)
# a = inner(grad(v),grad(dv))*dx

# Right hand side defined by the operator
# beta=0, epsilon=1 => Poisson
# beta=1, epsilon=0 => Convection
# beta=1, epsilon=1e-1 => Confusion

# Primal Formulation
L = -inner(beta*u,grad(dv))*dx + inner(epsilon*grad(u),grad(dv))*dx

# Ultra-Weak Formulation
# L = -inner(beta*u,grad(dv))*dx + inner(epsilon*grad(u),grad(dv))*dx

# Compute solution
v = Function(Vp)

# With boundary conditions
solve(a == L, v, bc)

# Without boundary conditions
# solve(a == L, v)

vfine = project(v,Vpfine)

vfine_vals = vfine.vector().array()

pl.figure(1)
x_vals = pl.linspace(-2,2,r*pfine*N+1) 
u_vals = pl.zeros((r*pfine*N+1,))
for i in range(0,x_vals.size):
	u_vals[i] = u(x_vals[i])
pl.plot(x_vals,u_vals,linewidth=2,label='Trial Function')
pl.plot(x_vals,vfine_vals,'-',linewidth=2,label='Test Function')
pl.xlim((-2,2))
pl.ylim((-2,2))
pl.legend()

pl.show()
