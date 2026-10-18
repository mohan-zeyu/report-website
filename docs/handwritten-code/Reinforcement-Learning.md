Let's get straight to the point.
## Q-learning

I suspect it's the concise method used in simple cases like discrete states and actions maybe.
I'm not going to talk about the RL so formally like defining the `agent`, `reward`, `state` ... so cleanly because they are all intuitive.

Let's directly get into a scenario:

```text
S 0 0 0 0 0 0 0 G
```

Here's a "maze", where `S` is the starting point while `G` stands for "Goal", at which the game will finalize.

Let's consider the sequence of points to be an array with index from 0 to 8, which then represent the number of each `state` in this `world`.

So the **starting state** is 0 and **goal** state is 8. We want the agent to learn how to find the G from S after exploring for some time.

Q table stores the reward the agent thinks under specific state and doing actions, as far as it learnt so far.

So now the Q table will be a two-dimension matrix, where dim 0 is for different actions, dim 1 is for states, a.k.a **Q\[state\]\[action\]**. The size will be $num_{state} \times num_{action}$

Initially, the Q-table will be empty, filled by all 0.

We give an environment for our agent kept trying:

1. For every trial, it will be $\epsilon$ probability for the agent to randomly choose an action; And $1 - \epsilon$ probability to choose the action with highest value in Q table.

2. Make a step. And the world state changed. The agent will get some reward.

3. Update the Q table based on this action. 

	The formula is:
	
	$$
	Q[state][action] += \alpha \times (reward + \gamma \times max(Q[next\_state]) - Q[state][action])
	$$
	
	Here $\alpha$ is the learning rate, each time we only add some portion of update.
	
	$\gamma$ is the discount rate, we encourage a sooner reward is it's less than 1.
	
	$reward$ is simply the achievement from this step.
	
4. Move the state to the next and continue doing above steps.

Code is below:
```python linenums="1"
import random as rd
import numpy as np

# let's consider a scenario:
# [S 0 0 0 0 0 0 0 G]
# where S stands for "start", G stands for "Goal"
# The agent should start from S and then finalize to G, a very easy problem

# ---------- environment ----------
n_states = 9
goal = 8

alpha = 0.1       # learning rate
gamma = 0.99      # discount factor
epsilon = 0.1     # exploration rate

def step(state, action):
    r"""
    handle the action influence and state transition

    return:
        [next_state, reward, done]
    1 for success, -0.01 for others, encouraging for being quicker

    """
    # action 0 for Left and 1 for Right
    nxt = state + (1 if action else -1)
    # in case it moves too left
    nxt = max(nxt, 0)
    if nxt == goal:
        return nxt, 1, True
    else:
        return nxt, -0.01, False

def main():
    Q = np.zeros((n_states, 2))
    
    for _ in range(2000):
        # We train 2000 steps
        state = 0
        action = 0
        for _ in range(100):
            # During each episode, the agent can run 100 steps
            if rd.random() < epsilon:
                action = rd.randint(0, 1)
            else:
                action = np.argmax(Q[state])

            nxt, reward, done = step(state=state, action=action)
            
            # Update Q table
            Q[state][action] += alpha * (reward + gamma * (not done) * np.max(Q[nxt]) - Q[state][action])
            
            if done:
                break

            state = nxt
    
    print(Q)
    state = 0
    for i in range(20):
        action = np.argmax(Q[state])
        state, _, done = step(state, action)
        print(f"step{i}: state: {state}, action: {action}")
        if done:
            break

if __name__ == '__main__':
    main()

```