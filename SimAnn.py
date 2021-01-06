def simnann(probl):
	# Compute cost ini
	c = probl.cost()
	print(f'initial cost = {c}')
	
	#start at a high temperature
	T0 = 0.5
	anneal_steps = 5
	mcmc_steps = 500
	#cycle lowering T gradually
	
	for T in np.linspace(T0, 0, anneal_steps):
		print(f'T = {T}')
		accepted = 0
		#few sampling steps with MCMC
		for step in range(mcmc_steps):
			#propose a random move
			move = probl.propose_move()
			#compute the difference in cost
			delta_c = probl.compute_delta_cost(move)
			#Valid move ?
			if accept(delta_c, T):
				probl.accept_move(move)
				c = c + delta_c
				assert abs(c - probl.cost()) < 1**-10
				accepted += 1
				
				
			#we display the status every few steps
			if step % 100 == 0:
				probl.display()
				plt.pause(0.1)
				
		
		print(f'accept.rate = {accepted / mcmc_steps} curr.cost = {c}')				
	#return the best lap
	print(f'final cost = {c}')
	return probl
