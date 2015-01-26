from pylab import *

exactData = loadtxt('sedovExact.dat', skiprows=2)
dpgData = loadtxt('MinNSDecoupled/DoubleSedov1e-3LineData8.csv', delimiter=',', skiprows=1)
xExact = exactData[:,1]
denExact = exactData[:,2]
enerExact = exactData[:,3]
presExact = exactData[:,4]
velExact = exactData[:,5]
xDPG = dpgData[:,5]
denDPG = dpgData[:,0]
velDPG = dpgData[:,1]
tempDPG = dpgData[:,2]

figure(1)
plot(xExact,denExact, 'k-', label='Exact')
plot(xDPG,denDPG, 'b-', label='DPG')
xlabel('x')
ylabel('density')
# figure(2)
# plot(xExact,presExact, label='Exact')
# xlabel('x')
# ylabel('pressure')
figure(3)
plot(xExact,velExact, 'k-', label='Exact')
plot(xDPG,velDPG, 'b-', label='DPG')
xlabel('x')
ylabel('velocity')
show()