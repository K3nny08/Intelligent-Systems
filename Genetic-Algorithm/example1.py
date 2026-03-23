import random

def get_fitness(genome):
    """Objective: Maximize the number of 1s in the list."""
    return sum(genome)

def create_genome(length):
    """Generates a random binary list."""
    return [random.randint(0, 1) for _ in range(length)]

def evolve_population(pop, pop_size, genome_length, mutation_rate=0.1):
    """Performs selection, crossover, and mutation to create a new generation."""
    # 1. Sort by fitness (Descending)
    pop = sorted(pop, key=get_fitness, reverse=True)
    
    # 2. Elitism: Keep the top 2 individuals
    next_gen = pop[:2]
    
    # 3. Fill the rest of the population
    while len(next_gen) < pop_size:
        # Selection: Pick parents from the top half of the current population
        parent1, parent2 = random.sample(pop[:pop_size // 2], 2)
        
        # Crossover: Single-point split
        split = genome_length // 2
        child = parent1[:split] + parent2[split:]
        
        # Mutation: Flip a bit based on probability
        if random.random() < mutation_rate:
            idx = random.randrange(genome_length)
            child[idx] ^= 1
            
        next_gen.append(child)
        
    return next_gen

# --- Configuration ---
POP_SIZE = 20
GENOME_LEN = 10
GENERATIONS = 50

# Initialize and Run
population = [create_genome(GENOME_LEN) for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    population = evolve_population(population, POP_SIZE, GENOME_LEN)

best_solution = max(population, key=get_fitness)
print(f"Best solution: {best_solution} (Fitness: {get_fitness(best_solution)})")