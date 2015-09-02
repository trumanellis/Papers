from pylab import *

# prefix = 'RitzData/spacetimeConfusion2D'
prefix = 'RitzData/spacetimeConfusion2D'
norms = ['Graph', 'CoupledRobust', 'NSDecoupledH1']
# norms = ['NSDecoupledH1']
# epsilons = ['0.01','0.0001','1e-06','1e-08']
epsilons = ['0.01','0.0001','1e-06']
# epsilons = ['1e-06']
epsNames = ['$10^{-2}$','$10^{-4}$','$10^{-6}$',]
# epsNames = ['$10^{-6}$',]
epsDict = dict(zip(epsilons, epsNames))
ps = ['1','2','4']
# ps = ['0','1','2','4']
# solvers = ['MUMPS','SuperLUDist','GMG-Direct']
# solvers = ['MUMPS']
# solvers = ['SuperLUDist']
solvers = ['GMG-Direct']
# solvers = ['KLU']
# solvers = ['SuperLuDist','GMG-Direct']
linestyles = ['-' , '--' , ':' , '-.']
markers = ['o','s','D','8','h']
colors = ['k','r','b','g','c','m']
epsToLine = dict(zip(epsilons,linestyles))
pToColor = dict(zip(ps,colors))
solverToMarker = dict(zip(solvers,markers))
normToMarker = dict(zip(norms,markers))

for norm in norms:
	for epsilon in epsilons:
		for p in ps:
			for solver in solvers:
				filename = prefix+'_'+norm+'_'+epsilon+'_p'+p+'_'+solver+'.txt'
				data = loadtxt(filename, skiprows=1)
				ref = data[:,0]
				el = data[:,1]
				dofs = data[:,2]
				energy = data[:,3]
				l2 = data[:,4]
				time = data[:,5]
				iterations = data[:,6]
				cumulativeTime = cumsum(time)

				# figure('Graph Robustness')
				# if (norm == 'Graph'):
				# 	plot(ref, energy/l2, linestyle=epsToLine[epsilon], color=pToColor[p],label='$p='+p+'$ $\epsilon=$'+epsDict[epsilon])
				# figure('CoupledRobust Robustness')
				# if (norm == 'CoupledRobust'):
				# 	plot(ref, energy/l2, linestyle=epsToLine[epsilon], color=pToColor[p],label='$p='+p+'$ $\epsilon=$'+epsDict[epsilon])
				# figure('NSDecoupledH1 Robustness')
				# if (norm == 'NSDecoupledH1'):
				# 	plot(ref, energy/l2, linestyle=epsToLine[epsilon], color=pToColor[p],label='$p='+p+'$ $\epsilon=$'+epsDict[epsilon])

				figure('Graph Convergence')
				if (norm == 'Graph'):
					loglog(dofs, l2, linestyle=epsToLine[epsilon], color=pToColor[p], linewidth=2, label='$L^2$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')
					loglog(dofs, energy, linestyle=epsToLine[epsilon], marker='o', linewidth=0.5, color=pToColor[p],label='$V^*$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')
				figure('CoupledRobust Convergence')
				if (norm == 'CoupledRobust'):
					loglog(dofs, l2, linestyle=epsToLine[epsilon], color=pToColor[p], linewidth=2, label='$L^2$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')
					loglog(dofs, energy, linestyle=epsToLine[epsilon], marker='o', linewidth=0.5, color=pToColor[p],label='$V^*$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')
				figure('NSDecoupledH1 Convergence')
				if (norm == 'NSDecoupledH1'):
					loglog(dofs, l2, linestyle=epsToLine[epsilon], color=pToColor[p], linewidth=2, label='$L^2$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')
					loglog(dofs, energy, linestyle=epsToLine[epsilon], marker='o', linewidth=0.5, color=pToColor[p],label='$V^*$ '+' $\epsilon=$'+epsDict[epsilon]+' $p='+p+'$')

				# figure('Iterations')
				# if (solver == 'GMG-Direct'):
				# 	plot(ref, iterations, linestyle=epsToLine[epsilon], color=pToColor[p],label='$p='+p+'$ $\epsilon=$'+epsDict[epsilon])
				# figure('Error 1e-2')
				# if (epsilon == '0.01'):
				# 	loglog(cumulativeTime, l2, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# figure('Error 1e-4')
				# if (epsilon == '0.0001'):
				# 	loglog(cumulativeTime, l2, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# figure('Error 1e-6')
				# if (epsilon == '1e-06'):
				# 	loglog(cumulativeTime, l2, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# # figure('Error 1e-8')
				# # if (epsilon == '1e-08'):
				# # 	loglog(cumulativeTime, l2, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# figure('Time 1e-2')
				# if (epsilon == '0.01'):
				# 	plot(ref, time, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# figure('Time 1e-4')
				# if (epsilon == '0.0001'):
				# 	plot(ref, time, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# figure('Time 1e-6')
				# if (epsilon == '1e-06'):
				# 	plot(ref, time, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)
				# # figure('Time 1e-8')
				# # if (epsilon == '1e-08'):
				# # 	plot(ref, time, linestyle=epsToLine[epsilon], color=pToColor[p], marker=solverToMarker[solver],label='$p='+p+'$ '+solver)

# figure('Graph Robustness')
# title('Graph Norm')
# xlabel('Adaptive Refinements')
# ylabel('Energy Error / L2 Error')
# legend(loc='best')
# figure('CoupledRobust Robustness')
# title('Coupled Robust Norm')
# xlabel('Adaptive Refinements')
# ylabel('Energy Error / L2 Error')
# legend(loc='best')
# figure('NSDecoupledH1 Robustness')
# title('NS Decoupled Norm')
# xlabel('Adaptive Refinements')
# ylabel('Energy Error / L2 Error')
# legend(loc='best')

figure('Graph Convergence')
title('Graph Norm')
xlabel('Degrees of Freedom')
ylabel('Error')
ylim([1e-6,1])
ax = subplot(1,1,1)
handles, labels = ax.get_legend_handles_labels()
import operator
hl = sorted(zip(handles, labels),
            key=operator.itemgetter(1))
handles2, labels2 = zip(*hl)
ax.legend(handles2, labels2, ncol=2, loc='bottom left')
figure('CoupledRobust Convergence')
title('Coupled Robust Norm')
xlabel('Degrees of Freedom')
ylabel('Error')
ylim([1e-5,1])
ax = subplot(1,1,1)
handles, labels = ax.get_legend_handles_labels()
import operator
hl = sorted(zip(handles, labels),
            key=operator.itemgetter(1))
handles2, labels2 = zip(*hl)
ax.legend(handles2, labels2, ncol=2, loc='bottom left')
figure('NSDecoupledH1 Convergence')
title('NS Decoupled Norm')
xlabel('Degrees of Freedom')
ylabel('Error')
ylim([1e-5,1])
ax = subplot(1,1,1)
handles, labels = ax.get_legend_handles_labels()
import operator
hl = sorted(zip(handles, labels),
            key=operator.itemgetter(1))
handles2, labels2 = zip(*hl)
ax.legend(handles2, labels2, ncol=2, loc='bottom left')

# figure('Iterations')
# title('GMG-Direct')
# xlabel('Adaptive Refinements')
# ylabel('Iterations to Converge')
# legend()
# figure('Error 1e-2')
# title('$\epsilon=10^{-2}$')
# xlabel('Solve Time')
# ylabel('L2 Error')
# legend(loc='best')
# figure('Error 1e-4')
# title('$\epsilon=10^{-4}$')
# xlabel('Solve Time')
# ylabel('L2 Error')
# legend(loc='best')
# figure('Error 1e-6')
# title('$\epsilon=10^{-6}$')
# xlabel('Solve Time')
# ylabel('L2 Error')
# legend(loc='best')
# # figure('Error 1e-8')
# # title('$\epsilon=10^{-8}$')
# # xlabel('Solve Time')
# # ylabel('L2 Error')
# # legend(loc='best')
# figure('Time 1e-2')
# title('$\epsilon=10^{-2}$')
# xlabel('Adaptive Refinements')
# ylabel('Solve Time')
# legend(loc='upper left')
# figure('Time 1e-4')
# title('$\epsilon=10^{-4}$')
# xlabel('Adaptive Refinements')
# ylabel('Solve Time')
# legend(loc='upper left')
# figure('Time 1e-6')
# title('$\epsilon=10^{-6}$')
# xlabel('Adaptive Refinements')
# ylabel('Solve Time')
# legend(loc='upper left')
# # figure('Time 1e-8')
# # title('$\epsilon=10^{-8}$')
# # xlabel('Adaptive Refinements')
# # ylabel('Solve Time')
# # legend(loc='upper left')
show()

