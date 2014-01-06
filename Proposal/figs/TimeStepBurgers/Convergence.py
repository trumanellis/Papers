from pylab import *

h = [
	# 1./2,
    1./4,
    1./8,
    1./16,
    ]
l2error = [
# 0.0020879,
0.000174044,
1.18334e-05,
7.53293e-07,
    ]

slope,intercept=polyfit(log(h),log(l2error),1)

loglog(h, l2error, label='slope = '+"{:.2f}".format(slope))
xlabel('h, dt')
ylabel('error')
legend(loc='best')
show()
