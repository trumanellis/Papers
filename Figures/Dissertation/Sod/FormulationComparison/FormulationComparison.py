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
refs = [0,4,9,14]
# for ref in range(0,15):
for ref in refs:
	exactData = loadtxt('../sod.out', skiprows=2)
	primData = loadtxt('Form0LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	consData = loadtxt('Form1LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	entData = loadtxt('Form2LineData'+str(ref)+'.csv', delimiter=',', skiprows=1)
	xExact = exactData[:,0]
	denExact = exactData[:,1]
	velExact = exactData[:,2]
	presExact = exactData[:,3]
	# enerExact = exactData[:,3]
	xPrim = primData[:,5]
	denPrim = primData[:,0]
	velPrim = primData[:,1]
	tempPrim = primData[:,2]
	xCons = consData[:,5]
	denCons = consData[:,0]
	momCons = consData[:,1]
	ECons = consData[:,2]
	xEnt = entData[:,5]
	zcEnt = entData[:,0]
	zmEnt = entData[:,1]
	zeEnt = entData[:,2]

	# Primal
	rhoPrim = denPrim
	vPrim = velPrim
	pPrim = R*denPrim*tempPrim
	# Conservation
	rhoCons = denCons
	vCons = momCons/denCons
	pCons = (gamma-1)*(ECons-0.5*momCons*momCons/denCons)
	# Entropy
	alpha = ((gamma-1)/((-zeEnt)**gamma))**(1./(gamma-1))*exp((-gamma+zcEnt-0.5*zmEnt*zmEnt/zeEnt)/(gamma-1))
	rhoEnt = -alpha*zeEnt
	mEnt = alpha*zmEnt
	EEnt = alpha*(1-0.5*zmEnt*zmEnt/zeEnt)
	vEnt = mEnt/rhoEnt
	pEnt = (gamma-1)*(EEnt-0.5*mEnt*mEnt/rhoEnt)

	figure("primitive-den")
	if (ref == 0):
		plot(xExact,denExact, 'k-', label='Exact')
	plot(xPrim,rhoPrim, '-', label='Refinement '+str(ref))

	figure("primitive-vel")
	if (ref == 0):
		plot(xExact,velExact, 'k-', label='Exact')
	plot(xPrim,vPrim, '-', label='Refinement '+str(ref))

	figure("primitive-pres")
	if (ref == 0):
		plot(xExact,presExact, 'k-', label='Exact')
	plot(xPrim,pPrim, '-', label='Refinement '+str(ref))


	figure("conservation-den")
	if (ref == 0):
		plot(xExact,denExact, 'k-', label='Exact')
	plot(xCons,rhoCons, '-', label='Refinement '+str(ref))

	figure("conservation-vel")
	if (ref == 0):
		plot(xExact,velExact, 'k-', label='Exact')
	plot(xCons,vCons, '-', label='Refinement '+str(ref))

	figure("conservation-pres")
	if (ref == 0):
		plot(xExact,presExact, 'k-', label='Exact')
	plot(xCons,pCons, '-', label='Refinement '+str(ref))


	figure("entropy-den")
	if (ref == 0):
		plot(xExact,denExact, 'k-', label='Exact')
	plot(xEnt,rhoEnt, '-', label='Refinement '+str(ref))

	figure("entropy-vel")
	if (ref == 0):
		plot(xExact,velExact, 'k-', label='Exact')
	plot(xEnt,vEnt, '-', label='Refinement '+str(ref))

	figure("entropy-pres")
	if (ref == 0):
		plot(xExact,presExact, 'k-', label='Exact')
	plot(xEnt,pEnt, '-', label='Refinement '+str(ref))
	# figure(1)
	# plot(xExact,denExact, 'k-', label='Exact')
	# plot(xPrim,rhoPrim, 'b-', label='Primal')
	# plot(xPrim,rhoCons, 'g-', label='Conservation')
	# plot(xEnt,rhoEnt, 'r-', label='Entropy')
	# # title('Density '+str(ref)+' Refinements')
	# xlabel('x')
	# ylabel('density')
	# ylim((0,1.1))
	# legend()
	# savefig("den"+str(ref+1)+".pdf")
	# figure(2)
	# plot(xExact,velExact, 'k-', label='Exact')
	# plot(xPrim,vPrim, 'b-', label='Primal')
	# plot(xCons,vCons, 'g-', label='Conservation')
	# plot(xEnt,vEnt, 'r-', label='Entropy')
	# # title('Velocity '+str(ref)+' Refinements')
	# xlabel('x')
	# ylabel('velocity')
	# ylim((-.2,1.2))
	# legend(loc='upper left')
	# savefig("vel"+str(ref+1)+".pdf")
	# figure(3)
	# plot(xExact,presExact, 'k-', label='Exact')
	# plot(xPrim,pPrim, 'b-', label='Primal')
	# plot(xCons,pCons, 'g-', label='Conservation')
	# plot(xEnt,pEnt, 'r-', label='Entropy')
	# # title('Pressure '+str(ref)+' Refinements')
	# xlabel('x')
	# ylabel('pressure')
	# ylim((0,1.1))
	# legend(loc='upper right')
	# savefig("pres"+str(ref+1)+".pdf")
	# close('all')

figure("primitive-den")
xlabel('x')
ylabel('density')
legend()
savefig("primitive-den.pdf")
figure("primitive-vel")
xlabel('x')
ylabel('velocity')
legend(loc='upper left')
savefig("primitive-vel.pdf")
figure("primitive-pres")
xlabel('x')
ylabel('pressure')
legend()
savefig("primitive-pres.pdf")

figure("conservation-den")
xlabel('x')
ylabel('density')
legend()
savefig("conservation-den.pdf")
figure("conservation-vel")
xlabel('x')
ylabel('velocity')
legend(loc='upper left')
savefig("conservation-vel.pdf")
figure("conservation-pres")
xlabel('x')
ylabel('pressure')
legend()
savefig("conservation-pres.pdf")

figure("entropy-den")
xlabel('x')
ylabel('density')
legend()
savefig("entropy-den.pdf")
figure("entropy-vel")
xlabel('x')
ylabel('velocity')
legend(loc='upper left')
savefig("entropy-vel.pdf")
figure("entropy-pres")
xlabel('x')
ylabel('pressure')
legend()
savefig("entropy-pres.pdf")
# show()
# close('all')