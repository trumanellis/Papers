from pylab import *

h = [
    1./4,
    1./8,
    1./16,
    ]
l2error = [
0.000196704,
1.60502e-05,
1.60833e-06,
    ]

slope,intercept=polyfit(log(h),log(l2error),1)

loglog(h, l2error, label='slope = '+"{:.2f}".format(slope))
xlabel('h, dt')
ylabel('error')
legend(loc='best')
show()
