from pylab import *

h = [
    1./2,
    1./4,
    1./8,
    1./16,
    1./32,
    ]
l2error = [
0.0734026,
0.00742863,
0.00091828,
0.000113789,
1.40905e-05,
    ]

slope,intercept=polyfit(log(h),log(l2error),1)

loglog(h, l2error, label='slope = '+"{:.2f}".format(slope))
xlabel('h')
ylabel('error')
legend(loc='best')
show()
