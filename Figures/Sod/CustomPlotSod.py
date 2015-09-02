from pylab import *

Pr = 0.713
gamma = 1.4
p0 = 1
rho0 = 1
u0 = 1
a0 = sqrt(gamma*p0/rho0)
M_inf = u0/a0
Cv = 1./(gamma*(gamma-1)*M_inf*M_inf)
Cp = gamma*Cv
R = Cp-Cv
exactData = loadtxt('sod.out', skiprows=2)
dpgData0 = loadtxt('MinNSDecoupled1e-5/LineData0.csv', delimiter=',', skiprows=1)
dpgData14 = loadtxt('MinNSDecoupled1e-5/LineData14.csv', delimiter=',', skiprows=1)
xExact = exactData[:,0]
denExact = exactData[:,1]
velExact = exactData[:,2]
presExact = exactData[:,3]
# enerExact = exactData[:,3]
xDPG0 = dpgData0[:,5]
denDPG0 = dpgData0[:,0]
xDPG14 = dpgData14[:,5]
denDPG14 = dpgData14[:,0]

figure(1)
plot(xExact,denExact, 'k-', label='Exact')
plot(xDPG0,denDPG0, 'b-', label='Initial 4 Elements')
plot(xDPG14,denDPG14, 'r-', label='After 14 Refinements')
xlabel('x')
ylabel('density')
ylim((0,1.1))
legend()
# savefig("MinNSDecoupled1e-5/den"+str(ref+1)+".pdf")
# figure(2)
# plot(xExact,velExact, 'k-', label='Exact')
# plot(xDPG,velDPG, 'b-', label=str(ref)+' Refinements')
# xlabel('x')
# ylabel('velocity')
# ylim((-.2,1.2))
# legend(loc='upper left')
# savefig("MinNSDecoupled1e-5/vel"+str(ref+1)+".pdf")
# figure(3)
# plot(xExact,presExact, 'k-', label='Exact')
# plot(xDPG,R*denDPG*tempDPG, 'b-', label=str(ref)+' Refinements')
# xlabel('x')
# ylabel('pressure')
# ylim((0,1.1))
# legend(loc='upper right')
# savefig("MinNSDecoupled1e-5/pres"+str(ref+1)+".pdf")
# close('all')
show()