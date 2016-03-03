from pylab import *

dpgData10 = loadtxt('Robust10.csv', delimiter=',', skiprows=1)
entData10 = loadtxt('EntropyRobust10.csv', delimiter=',', skiprows=1)
xExact = linspace(-1,0,1000)
def DenExact(x):
	if abs(x) <= 1./3:
		return 4
	else:
		return 1
DenExact = vectorize(DenExact)
denExact = DenExact(xExact)
xDPG10 = dpgData10[:,7]
xEnt10 = entData10[:,7]
denDPG10 = dpgData10[:,0]
denEnt10 = entData10[:,0]

figure(1)
plot(xExact,denExact, 'k-', label='Exact')
plot(xDPG10,denDPG10, '-', color='blue', label='Robust Norm')
plot(xEnt10,denEnt10, '-', color='red', label='Entropy Scaled Robust Norm')
# xlim((-.5,.5))
# ylim((0,6))
legend(loc='best')
xlabel('x')
ylabel('density')

show()