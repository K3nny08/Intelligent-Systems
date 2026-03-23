import random

# --- Hyperparameters ---
NUM_PARTICLES = 20
NUM_ITERATIONS = 40
INERTIA = 0.7
COGNITIVE = 1.2
SOCIAL = 1.2
V_MAX = 2.0  # Velocity clamping to prevent "explosion"

def objective_function(x):
    """f(x) = (x - 3)^2 + 4. Global min at x=3, f(x)=4."""
    return (x - 3) ** 2 + 4

class Particle:
    def __init__(self, bounds=(-10, 10)):
        self.position = random.uniform(*bounds)
        self.velocity = random.uniform(-1, 1)
        
        # Initial evaluation
        self.current_val = objective_function(self.position)
        self.pbest_pos = self.position
        self.pbest_val = self.current_val

    def move(self, gbest_pos):
        # 1. Update Velocity
        r1, r2 = random.random(), random.random()
        cog_component = COGNITIVE * r1 * (self.pbest_pos - self.position)
        soc_component = SOCIAL * r2 * (gbest_pos - self.position)
        
        self.velocity = (INERTIA * self.velocity) + cog_component + soc_component
        
        # 2. Velocity Clamping
        self.velocity = max(min(self.velocity, V_MAX), -V_MAX)
        
        # 3. Update Position
        self.position += self.velocity
        
        # 4. Re-evaluate
        self.current_val = objective_function(self.position)
        
        # 5. Update Personal Best
        if self.current_val < self.pbest_val:
            self.pbest_val = self.current_val
            self.pbest_pos = self.position

def pso_1d():
    swarm = [Particle() for _ in range(NUM_PARTICLES)]
    
    # Initialize global best from the starting population
    best_p = min(swarm, key=lambda p: p.pbest_val)
    gbest_pos = best_p.pbest_pos
    gbest_val = best_p.pbest_val

    for t in range(NUM_ITERATIONS):
        for p in swarm:
            p.move(gbest_pos)
            
            # Update Global Best if a particle found a better spot
            if p.current_val < gbest_val:
                gbest_val = p.current_val
                gbest_pos = p.position
        
        if t % 5 == 0 or t == NUM_ITERATIONS - 1:
            print(f"Iter {t:02} | Best x: {gbest_pos: .4f} | f(x): {gbest_val: .4f}")

    print(f"\nOptimization Complete.")
    print(f"Final Solution: x ≈ {gbest_pos:.6f}, f(x) ≈ {gbest_val:.6f}")

if __name__ == "__main__":
    pso_1d()