from pylab import *

# 1D Solution
eps = 1e-2
l = 4
x = 0-logspace(-6,0,1000)
# x = linspace(0,1,1000)
t = linspace(0,1,1000)

X, T = meshgrid(x,t)
lambda1 = (-1.+sqrt(1.-4.*eps*l))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*l))/(-2*eps)
# u = exp(-l*T)*(exp(lambda1*(X-1))-exp(lambda2*(X-1)))
u = exp(-l*T)*(exp(lambda1*(X))-exp(lambda2*(X))) + 1-exp(1./eps*X)

figure("1D Problem")
contourf(X,T,u,100)
colorbar()

# 2D Solution 1a
eps = 1e-2
k = eps
l = k + pi*pi/eps
x = linspace(0,1,100)
y = linspace(0,1,100)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
a1 = 0
a2 = 1
t = 0

# for i in arange(1,3):
# 	t = eps*(i-1)
# 	u = exp(-l*t)*(exp(lambda1*(X-1))-exp(lambda2*(X-1)))*(a1*sin(sqrt(eps*(l-k))*Y)+a2*cos(sqrt(eps*(l-k))*Y))
# 	figure(i+1)
# 	contourf(X,Y,u,100)
# 	colorbar()

# 2D Solution 1b
eps = 1e-1
k = 1-pi**2/eps
l = k + pi**2/eps
x = linspace(0,1,100)
y = linspace(0,1,100)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
a1 = 0
a2 = 1
t = 0

# for i in arange(1,3):
# 	t = eps*(i-1)
# 	u = exp(-l*t)*(exp(lambda1*(X-1))-exp(lambda2*(X-1)))*(a1*sin(sqrt(eps*(l-k))*Y)+a2*cos(sqrt(eps*(l-k))*Y))
# 	figure(i+1)
# 	contourf(X,Y,u,100)
# 	colorbar()

# 2D Solution 2
eps = 1e-2
l = 1
# k = l + arcsinh(1)**2/eps
k = l + 1
x = linspace(0,1,100)
y = linspace(0,1,100)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
a1 = 1
a2 = 0
t = 0

# for i in arange(1,3):
# 	t = .5*(i-1)
# 	u = exp(-l*t)*(exp(lambda1*(X-1))-exp(lambda2*(X-1)))*(a1*sinh(sqrt(eps*(k-l))*(Y-.5))+a2*cosh(sqrt(eps*(k-l))*(Y-.5)))
# 	figure(i+1)
# 	contourf(X,Y,u,100)
# 	colorbar()

# 2D Solution 3
eps = 1e-2
l = 4
k = l
x = linspace(-1,0,100)
y = linspace(-.5,.5,100)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
n = 1
nu1 = pi**2*eps
r1 = (1+sqrt(1+4*eps*nu1))/(2*eps)
s1 = (1-sqrt(1+4*eps*nu1))/(2*eps)
u0 = 0.1*(exp(s1*X)-exp(r1*X))/(r1*exp(-r1)-s1*exp(-s1))*cos(pi*Y)
a1 = 1
a2 = 0
t = 0

for i in arange(1,4):
	t = .5*(i-1)
	u = u0+exp(-l*t)*(exp(lambda1*X)-exp(lambda2*X))#*(2*Y)
	# u = exp(-l*t)*(exp(lambda1*X)-exp(lambda2*X))#*(2*Y)
	# u = u0
	figure("2D Problem t = "+str(t))
	contourf(X,Y,u,100)
	colorbar()

# 2D Solution 4
eps = 1e-2
l = 1
k = l
x = linspace(-1,0,100)
y = linspace(-1,0,100)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
mu1 = (-2.+sqrt(4.-4.*eps*k))/(-2*eps)
mu2 = (-2.-sqrt(4.-4.*eps*k))/(-2*eps)
a1 = 1
a2 = 0
t = 0

# for i in arange(1,3):
# 	t = .5*(i-1)
# 	# u = -exp(-l*t)*((exp(lambda1*X)-exp(lambda2*X))*Y+(exp(mu1*Y)-exp(mu2*Y))*X)
# 	u = -exp(-l*t)*(exp(lambda1*X)-exp(lambda2*X))*Y
# 	# u = -exp(-l*t)*(exp(mu1*Y)-exp(mu2*Y))*X
# 	figure(i+1)
# 	contourf(X,Y,u,100)
# 	colorbar()

show()