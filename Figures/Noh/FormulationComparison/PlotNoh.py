from pylab import *

for ref in range(8,9):
	primData = loadtxt('Noh0LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	consData = loadtxt('Noh1LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	xExact = linspace(-.5,.5,1000)
	def DenExact(x):
		if abs(x) <= 1./3:
			return 4
		else:
			return 1
	DenExact = vectorize(DenExact)
	denExact = DenExact(xExact)
	xPrim = primData[:,5]-.5
	denPrim = primData[:,0]
	velPrim = primData[:,1]
	tempPrim = primData[:,2]
	xCons = consData[:,5]-.5
	denCons = consData[:,0]
	velCons = consData[:,1]
	tempCons = consData[:,2]

	figure(ref)
	plot(xExact,denExact, 'k-', linewidth=1, label='Exact')
	plot(xPrim,denPrim, 'b-', linewidth=1, label='Primitive')
	plot(xCons,denCons, 'r-', linewidth=1, label='Conservation')
	xlim((-.5,.5))
	ylim((0,6))
	legend()
	xlabel('x')
	ylabel('density')
	savefig("den"+str(ref+1)+".pdf")

show()