																		### TRAVELING SLAESMAN PROBLEM USING SIMULATED ANNEALING ###		

import numpy as np
import matplotlib.pyplot as plt																																

# DEFINING THE TSM

class TSP:
	
	def __init__(self, n, seed = None):
		if not (isinstance(n, int) and (n > 0)):
			raise Exception('n must be a positive int')
		
		if seed is not None:
			np.random.seed(seed)
		
		
		x = np.random.rand(
			n)
		y = np.random.rand(n)
		walk = np.arange(n)
		
		dist = np.sqrt((x - np.reshape(x, (n,1)))**2 + (y - np.reshape(y, (n,1)))**2)
		
		
				
		self.x, self.y = x, y 
		self.n = n
		self.walk = walk
		self.dist = dist
		
		
		
	def cost(self):
		cost = 0.0
		for i in range(self.n):
			city1 = self.walk[i]
			city2 = self.walk[(i + 1) % self.n]
			coord1 = (self.x[city1], self.y [city1])
			coord2 = (self.x[city2], self.y[city2])
			cost += distance(coord1, coord2)
		return cost
		
		
	def propose_move(self):
		n = self.n 
		while True:
			i = np.random.randint(n)
			j = np.random.randint(n)
			if i > j:
				i, j = j, i
			if abs(i - j) > 1 and not (i == 0 and j == n -1):
				break
				
		assert j != i
		assert j != i + 1
		assert not (i == 0 and j == n - 1)
			
		return (i, j)
			
			
			
			
			
		return None
		
		
	def compute_delta_cost(self, move):
		n = self.n
		walk = self.walk
		x, y = self.x, self.y
		i, j = move #unpack the move
		
		city_i0 = walk[i]
		city_i1 = walk[i + 1]
		city_j0 = walk[j]
		city_j1 = walk[(j + 1) % n] # %n in case j = n-1
		
		coord_i0 = (x[city_i0], y[city_i0])
		coord_i1 = (x[city_i1], y[city_i1])
		coord_j0 = (x[city_j0], y[city_j0])
		coord_j1 = (x[city_j1], y[city_j1])
		
		old_c = distance(coord_i0, coord_i1) + distance(coord_j0, coord_j1)
		
		new_c = distance(coord_i0, coord_j0) + distance(coord_i1, coord_j1)

		delta_c = new_c - old_c #how much I gain from this move		
		
		return delta_c

		
				
						
	def accept_move(self, move):
		walk = self.walk
		i, j = move
		assert i < j
		
		walk[i + 1: j + 1] = walk[j:i:-1]
		
		
						
	def display(self):
		x, y = self.x, self.y
		walk = self.walk
		
		plt.clf()
		plt.plot(x, y, 'o')
		plt.plot(x[walk], y[walk], color='orange')
		# plot the last line connecting the loop
		last_line = [walk[-1], walk[0]]
		plt.plot(x[last_line], y[last_line], color='orange')
		
		plt.show()
		
	
# USING SIM ANN



def simnann(probl):
	# Compute cost ini
	c = probl.cost()
	print(f'initial cost = {c}')
	
	#start at a high temperature
	T0 = 0.5
	anneal_steps = 10
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






def distance(coor1, coor2):
	
	x1, y1 = coor1
	x2, y2 = coor2
	
	dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	return dist
	
	
def accept(delta_c, T):
	if delta_c <= 0:
		return True
	if T == 0:
		return False
	p = np.exp(-delta_c / T)
	return np.random.rand() < p
	
	
	
if __name__ == "__main__":
	prob = TSP(40)
	simnann(prob)
