from pylab import *

# 1D Solution
eps = 1e-2
l = 4
x = 0-logspace(-6,0,2000)
# x = linspace(0,1,1000)
t = linspace(0,1,1000)

X, T = meshgrid(x,t)
lambda1 = (-1.+sqrt(1.-4.*eps*l))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*l))/(-2*eps)
# u = exp(-l*T)*(exp(lambda1*(X-1))-exp(lambda2*(X-1)))
u = exp(-l*T)*(exp(lambda1*(X))-exp(lambda2*(X))) + 1-exp(1./eps*X)

# figure("1D Problem")
# contourf(X,T,u,100)
# colorbar()

# 2D Solution 1a
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
l = 4
k = l
# x = linspace(-1,0,100)
x = 0-logspace(-6,0,100)
# y = linspace(0,1,1000)
y = linspace(-.5,.5,1000)
X, Y = meshgrid(x,y)
lambda1 = (-1.+sqrt(1.-4.*eps*k))/(-2*eps)
lambda2 = (-1.-sqrt(1.-4.*eps*k))/(-2*eps)
n = 1
r1 = (1+sqrt(1+4*eps**2*pi**2*n**2))/(2*eps)
s1 = (1-sqrt(1+4*eps**2*pi**2*n**2))/(2*eps)
# n = 1
# u0 = 0*X
# inflow = 0*y
# for n in range(1,21):
# 	coeff = 0
# 	if (n % 4 == 0):
# 		coeff = 1/(n*pi)
# 	if (n % 4 == 2):
# 		coeff = -1/(n*pi)
# 	# if (n % 2 == 0):
# 	# 	coeff = 1/(n**2*pi**2)
# 	# if (n % 2 == 0):
# 		# coeff = -1 + cos(n*pi/2)+.5*n*pi*sin(n*pi/2)+sin(n*pi/4)*(n*pi*cos(n*pi/4)-2*sin(3*n*pi/4))
# 		# coeff = eps*coeff/(n*pi)
# 	# if (n % 4 == 1):
# 	# 	# coeff = 1./(n*pi)
# 	# 	coeff = 2./(n**2*pi**2)
# 	# if (n % 4 == 2):
# 	# 	coeff = 1./(n*pi)
# 	# 	# coeff = 2./(n**2*pi**2)
# 	# if (n % 4 == 3):
# 	# 	# coeff = -1./(n*pi)
# 	# 	coeff = -2./(n**2*pi**2)
# 	# if (n % 4 == 0):
# 	# 	coeff = -1./(n*pi)
# 	# 	# coeff = -2./(n**2*pi**2)
# 	# if (n % 2 == 0):
# 	# 	coeff = 2*coeff
# 	# else:
# 	# 	coeff = 0

# 	r1 = (1+sqrt(1+4*eps**2*pi**2*n**2))/(2*eps)
# 	s1 = (1-sqrt(1+4*eps**2*pi**2*n**2))/(2*eps)
# 	u0 = u0 + coeff*(exp(s1*X)-exp(r1*X))/(r1*exp(-r1)-s1*exp(-s1))*sin(pi*Y*n)
# 	inflow = inflow + coeff*sin(n*pi*y)
# u0 = 10*eps*(exp(s1*X)-exp(r1*X))/(r1*exp(-r1)-s1*exp(-s1))*cos(pi*Y)
u0 = (exp(s1*X)-exp(r1*X))/(exp(-s1)-exp(-r1))*cos(pi*Y)
a1 = 1
a2 = 0
t = 0

# figure("inflow")
# plot(y,inflow)
# print(inflow)

for i in arange(1,4):
# for i in arange(1,2):
	t = .5*(i-1)
	u = u0+1*exp(-l*t)*(exp(lambda1*X)-exp(lambda2*X))#*(Y)
	# u = exp(-l*t)*(exp(lambda1*X)-exp(lambda2*X))#*(2*Y)
	# u = u0
	figure("2D Problem t = "+str(t))
	contourf(X,Y,u,100)
	colorbar()

# 2D Solution 4
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