import random
import string

# Configuration
TARGET = "GENETIC"
CHARS = string.ascii_uppercase
POP_SIZE = 100
ELITE_SIZE = 10    # Top 10% stay unchanged
BREED_POOL = 20    # Top 20% can be parents
GEN_LIMIT = 1000

def get_fitness(guess):
    """Calculates how many characters match the target positionally."""
    return sum(1 for i, j in zip(guess, TARGET) if i == j)

def mutate(parent):
    """Randomly alters one character in the string."""
    child_list = list(parent)
    idx = random.randrange(len(TARGET))
    child_list[idx] = random.choice(CHARS)
    return "".join(child_list)

# 1. Initialize Population
population = ["".join(random.choice(CHARS) for _ in TARGET) for _ in range(POP_SIZE)]

for gen in range(GEN_LIMIT):
    # 2. Rank population by fitness
    population.sort(key=get_fitness, reverse=True)
    
    # 3. Check for Success
    if population[0] == TARGET:
        break
        
    # 4. Selection & Reproduction
    # Keep the Elites (Top 10%)
    next_gen = population[:ELITE_SIZE]
    
    # Fill the rest via mutation of the top performers
    while len(next_gen) < POP_SIZE:
        parent = random.choice(population[:BREED_POOL])
        next_gen.append(mutate(parent))
        
    population = next_gen

print(f"Evolved String: {population[0]} at Generation {gen}")