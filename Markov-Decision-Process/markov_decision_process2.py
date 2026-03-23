import math

# --- Configuration & Data Structures ---
STATES = {0: "Good", 1: "Broken"}
ACTIONS = {0: "Maintain", 1: "Replace"}
GAMMA = 0.9
EPSILON = 1e-6

# Transition Probabilities: P[state][action][next_state]
P = {
    0: {0: {0: 0.8, 1: 0.2}, 1: {0: 1.0, 1: 0.0}},
    1: {0: {0: 0.0, 1: 1.0}, 1: {0: 1.0, 1: 0.0}}
}

# Rewards: R[state][action][next_state]
# Note: Using a slightly flattened reward structure for easier access
R = {
    0: {0: {0: 10, 1: -5},  1: {0: -10, 1: -10}},
    1: {0: {0: -20, 1: -20}, 1: {0: -10, 1: -10}}
}

def get_q_value(s, a, V):
    """Calculates the expected value (Q-value) of taking action 'a' in state 's'."""
    q_val = 0
    for next_s, prob in P[s][a].items():
        reward = R[s][a][next_s]
        q_val += prob * (reward + GAMMA * V[next_s])
    return q_val

def run_value_iteration():
    V = {s: 0.0 for s in STATES}
    
    # 1. Estimation Phase
    for i in range(1, 100):
        delta = 0
        new_V = V.copy()
        
        for s in STATES:
            # Find the maximum Q-value across all available actions
            action_values = [get_q_value(s, a, V) for a in ACTIONS]
            best_value = max(action_values)
            
            delta = max(delta, abs(best_value - V[s]))
            new_V[s] = best_value
            
        V = new_V
        print(f"Iter {i:02}: V(Good)={V[0]:>6.2f}, V(Broken)={V[1]:>6.2f}")
        
        if delta < EPSILON:
            print(f"--- Converged in {i} iterations ---")
            break

    # 2. Policy Extraction
    policy = {}
    for s in STATES:
        # Select action index that results in the highest Q-value
        best_a = max(ACTIONS.keys(), key=lambda a: get_q_value(s, a, V))
        policy[STATES[s]] = ACTIONS[best_a]
        
    return V, policy

if __name__ == "__main__":
    final_v, final_policy = run_value_iteration()
    print(f"\nOptimal Policy: {final_policy}")