import math

# Configuration
NUM_STATES = 5
GOAL_STATE = 4
GAMMA = 0.9          # Discount Factor
EPSILON = 1e-6       # Convergence threshold
ACTIONS = [0, 1]     # 0: Left, 1: Right
ACTION_NAMES = {0: "Left", 1: "Right"}

# Rewards: Goal-oriented structure
REWARDS = [0, 0, 0, 0, 10]

def get_next_state(state, action):
    """Deterministic transition logic."""
    if action == 0: return max(0, state - 1)
    return min(NUM_STATES - 1, state + 1)

def get_action_value(state, action, values):
    """Calculates the Q-value for a state-action pair."""
    next_s = get_next_state(state, action)
    # Bellman Equation: R(s) + γ * V(s')
    return REWARDS[state] + GAMMA * values[next_s]

def value_iteration():
    V = [0.0] * NUM_STATES
    
    # --- 1. Value Estimation Loop ---
    for i in range(1, 100):
        delta = 0
        new_V = list(V)
        
        for s in range(NUM_STATES):
            if s == GOAL_STATE:
                new_V[s] = float(REWARDS[s])
                continue
            
            # Find the max value across all possible actions
            best_val = max(get_action_value(s, a, V) for a in ACTIONS)
            
            delta = max(delta, abs(best_val - V[s]))
            new_V[s] = best_val
            
        V = new_V
        print(f"Iter {i:02}: {[round(v, 2) for v in V]}")
        
        if delta < EPSILON: # Stop early if values stop changing
            print(f"Converged at iteration {i}.")
            break

    # --- 2. Policy Extraction ---
    policy = []
    for s in range(NUM_STATES):
        if s == GOAL_STATE:
            policy.append("Goal")
        else:
            # Pick the action that yields the max value
            best_a = max(ACTIONS, key=lambda a: get_action_value(s, a, V))
            policy.append(ACTION_NAMES[best_a])
            
    print(f"\nFinal Policy: {policy}")

if __name__ == "__main__":
    value_iteration()