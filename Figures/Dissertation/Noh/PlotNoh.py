from pylab import *

dpgData0 = loadtxt('Robust0.csv', delimiter=',', skiprows=1)
dpgData2 = loadtxt('Robust2.csv', delimiter=',', skiprows=1)
dpgData4 = loadtxt('Robust4.csv', delimiter=',', skiprows=1)
dpgData5 = loadtxt('Robust5.csv', delimiter=',', skiprows=1)
dpgData6 = loadtxt('Robust6.csv', delimiter=',', skiprows=1)
dpgData8 = loadtxt('Robust8.csv', delimiter=',', skiprows=1)
dpgData10 = loadtxt('Robust10.csv', delimiter=',', skiprows=1)
xExact = linspace(-1,0,1000)
def DenExact(x):
	if abs(x) <= 1./3:
		return 4
	else:
		return 1
DenExact = vectorize(DenExact)
denExact = DenExact(xExact)
xDPG0 = dpgData0[:,7]
xDPG2 = dpgData2[:,7]
xDPG4 = dpgData4[:,7]
xDPG5 = dpgData5[:,7]
xDPG6 = dpgData6[:,7]
xDPG8 = dpgData8[:,7]
denDPG0 = dpgData0[:,0]
denDPG2 = dpgData2[:,0]
denDPG4 = dpgData4[:,0]
denDPG5 = dpgData5[:,0]
denDPG6 = dpgData6[:,0]
denDPG8 = dpgData8[:,0]
xDPG10 = dpgData10[:,7]
denDPG10 = dpgData10[:,0]

figure(1)
plot(xExact,denExact, 'k-', label='Exact')
plot(xDPG0,denDPG0, 'b-', label='Initial 4 Elements')
# plot(xDPG2,denDPG2, '-', color='cyan', label='2 Refinements')
# plot(xDPG4,denDPG4, '-', color='green', label='4 Refinements')
plot(xDPG5,denDPG5, '-', color='green', label='5 Refinements')
# plot(xDPG6,denDPG6, '-', color='orange', label='6 Refinements')
# plot(xDPG8,denDPG8, '-', color='red', label='8 Refinements')
plot(xDPG10,denDPG10, '-', color='red', label='10 Refinements')
# xlim((-.5,.5))
# ylim((0,6))
legend(loc='best')
xlabel('x')
ylabel('density')

show()