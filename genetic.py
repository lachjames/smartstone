import copy, random

class Genetic:
	def __init__(self, iterations, pop_count, aClass, aClassParamList, crossoverFunc, mutationFunc, score_function, goal_func, mutation_probability):
		self.iterations = iterations
		self.aClass = aClass
		self.aClassParamList = aClassParamList
		self.crossoverFunc = crossoverFunc
		self.mutationFunc = mutationFunc
		self.score_function = score_function
		self.goal_func = goal_func
		self.pop_count = pop_count
		self.mutation_probability = mutation_probability
	
	def run(self):
		population = [self.aClass(*x) for x in self.aClassParamList]
		print(population)
		for _ in range(self.iterations):
			#Check if we've met our goal
			for x in population:
				if self.goal_func(x):
					print("Reached Goal")
					return x
				else:
					#print(self.score_function(x))
					pass
			
			#Perform selection
			population.sort(key = lambda x: self.score_function(x))
			population = population[:int(self.pop_count / 2)]
			
			#Perform crossover
			children = []
			
			while len(children) < self.pop_count:
				A = population[random.randint(0, len(population) - 1)]
				B = population[random.randint(0, len(population) - 1)]
				children += [self.crossoverFunc(A, B)]
				
			#Replace the old population with the new one
			population = children
			
			#Perform mutation
			for i in range(0, len(population)):
				if random.random() > 1 - self.mutation_probability:
					self.mutationFunc(population[i])
		return population
	
	def simulate(self, X, T):
		last_score = self.score_function(X)
		
		newX = copy.deepcopy(X)
		newX.peturb()
		
		#print(self.score_function(X))
			
		if self.compare_func(newX, X):
			X = newX
		elif self.accept(newX, X, T):
			X = newX
				
		return X
	
	def accept(self, new, old, T):
		e = 2.71828182845904523536028747135266249775724709369995
		x = random.random()
		#print(e**((self.score_function(old) - self.score_function(new)) / T))
		return x > e**((self.score_function(old) - self.score_function(new)) / T)

	
if __name__ == "__main__": main()