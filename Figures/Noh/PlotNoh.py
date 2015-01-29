from pylab import *

for ref in range(0,9):
	dpgData = loadtxt('MinNSDecoupled/LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	xExact = linspace(-.5,.5,1000)
	def DenExact(x):
		if abs(x) <= 1./3:
			return 4
		else:
			return 1
	DenExact = vectorize(DenExact)
	denExact = DenExact(xExact)
	xDPG = dpgData[:,5]-.5
	denDPG = dpgData[:,0]
	velDPG = dpgData[:,1]
	tempDPG = dpgData[:,2]

	figure(ref)
	plot(xExact,denExact, 'k-', label='Exact')
	plot(xDPG,denDPG, 'b-', label=str(ref)+' Refinements')
	xlim((-.5,.5))
	ylim((0,6))
	legend()
	xlabel('x')
	ylabel('density')

show()