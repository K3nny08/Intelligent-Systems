import random

# --- Hyperparameters ---
W = 0.5   # Inertia: Resistance to change in direction
C1 = 1.5  # Cognitive: Attraction to personal best
C2 = 1.5  # Social: Attraction to swarm best
NUM_PARTICLES = 30
ITERATIONS = 50
DIMENSIONS = 2
BOUNDS = (-10, 10)

def sphere_function(position):
    """f(x, y) = x^2 + y^2. Global min at (0,0)."""
    return sum(x**2 for x in position)

class Particle:
    def __init__(self, dims, bounds):
        self.position = [random.uniform(*bounds) for _ in range(dims)]
        self.velocity = [random.uniform(-1, 1) for _ in range(dims)]
        self.best_pos = list(self.position)
        self.best_score = sphere_function(self.position)

    def update_velocity(self, global_best_pos):
        for i in range(len(self.position)):
            r1, r2 = random.random(), random.random()
            
            # Velocity = Inertia + Cognitive + Social
            vel_cognitive = C1 * r1 * (self.best_pos[i] - self.position[i])
            vel_social = C2 * r2 * (global_best_pos[i] - self.position[i])
            
            self.velocity[i] = (W * self.velocity[i]) + vel_cognitive + vel_social

    def update_position(self, bounds):
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]
            
            # Boundary control (Keep particles within the search space)
            if self.position[i] < bounds[0]: self.position[i] = bounds[0]
            if self.position[i] > bounds[1]: self.position[i] = bounds[1]

def run_pso():
    # Initialize swarm
    swarm = [Particle(DIMENSIONS, BOUNDS) for _ in range(NUM_PARTICLES)]
    
    # Initialize global best
    gbest_particle = min(swarm, key=lambda p: p.best_score)
    gbest_pos = list(gbest_particle.best_pos)
    gbest_score = gbest_particle.best_score

    for it in range(ITERATIONS):
        for p in swarm:
            # 1. Evaluate fitness
            score = sphere_function(p.position)
            
            # 2. Update Personal Best
            if score < p.best_score:
                p.best_score = score
                p.best_pos = list(p.position)
            
            # 3. Update Global Best
            if score < gbest_score:
                gbest_score = score
                gbest_pos = list(p.position)

        # 4. Movement Phase
        for p in swarm:
            p.update_velocity(gbest_pos)
            p.update_position(BOUNDS)

        if (it + 1) % 10 == 0 or it == 0:
            print(f"Iteration {it+1:02} | Best Score: {gbest_score:.6f} at {gbest_pos}")

    return gbest_pos, gbest_score

if __name__ == "__main__":
    run_pso()