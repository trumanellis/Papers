from pylab import *

dpgData0 = loadtxt('MinNSDecoupled/LineData0.csv', delimiter=',', skiprows=1)
dpgData8 = loadtxt('MinNSDecoupled/LineData8.csv', delimiter=',', skiprows=1)
xExact = linspace(-.5,.5,1000)
def DenExact(x):
	if abs(x) <= 1./3:
		return 4
	else:
		return 1
DenExact = vectorize(DenExact)
denExact = DenExact(xExact)
xDPG0 = dpgData0[:,5]-.5
denDPG0 = dpgData0[:,0]
xDPG8 = dpgData8[:,5]-.5
denDPG8 = dpgData8[:,0]

figure(1)
plot(xExact,denExact, 'k-', label='Exact')
plot(xDPG0,denDPG0, 'b-', label='Initial 6 Elements')
plot(xDPG8,denDPG8, 'r-', label='After 8 Refinements')
xlim((-.5,.5))
ylim((0,6))
legend()
xlabel('x')
ylabel('density')

show()