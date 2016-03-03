from pylab import *

Pr = 0.713
gamma = 1.4
p0 = 1
rho0 = 1
u0 = 1
# a0 = sqrt(gamma*p0/rho0)
# M_inf = u0/a0
# Cv = 1./(gamma*(gamma-1)*M_inf*M_inf)
Cv = 1
Cp = gamma*Cv
R = Cp-Cv
prefix = 'NSDecoupled'
for ref in range(0,13,2):
	# exactData = loadtxt('sod.out', skiprows=2)
	exactData = loadtxt('sod.out')
	dpgData = loadtxt(prefix+str(ref)+'.csv', delimiter=',', skiprows=1)
	xExact = exactData[:,0]
	denExact = exactData[:,1]
	velExact = exactData[:,2]
	presExact = exactData[:,3]
	# enerExact = exactData[:,3]
	xDPG = dpgData[:,7]
	denDPG = dpgData[:,0]
	velDPG = dpgData[:,1]
	tempDPG = dpgData[:,2]

	figure(1)
	plot(xExact,denExact, 'k-', label='Exact')
	plot(xDPG,denDPG, 'b-', label=str(ref)+' Refinements')
	xlabel('x')
	ylabel('density')
	ylim((0,1.1))
	legend()
	savefig(prefix+"-den"+str(ref+1)+".pdf")
	figure(2)
	plot(xExact,velExact, 'k-', label='Exact')
	plot(xDPG,velDPG, 'b-', label=str(ref)+' Refinements')
	xlabel('x')
	ylabel('velocity')
	ylim((-.2,1.2))
	legend(loc='upper left')
	savefig(prefix+"-vel"+str(ref+1)+".pdf")
	figure(3)
	plot(xExact,presExact, 'k-', label='Exact')
	plot(xDPG,R*denDPG*tempDPG, 'b-', label=str(ref)+' Refinements')
	xlabel('x')
	ylabel('pressure')
	ylim((0,1.1))
	legend(loc='upper right')
	savefig(prefix+"-pres"+str(ref+1)+".pdf")
	close('all')
show()