# 🤖 Maze Environment: Value and Policy Iteration  

Academic Project for CE/CZ4046: Intelligent Agents (NTU).

## Overview  
This project explores **Reinforcement Learning (RL)** in a grid-world maze environment. The agent navigates the maze using a probabilistic transition model and earns rewards or penalties based on the type of square it lands on. The goal is to compute the **optimal policy** and **state utility values** using **Value Iteration** and **Policy Iteration** algorithms.  

---

## Environment Details  

### Transition Model   
- The agent moves with:  
  - **80% probability** in the intended direction.  
  - **10% probability** to move left or right of the intended direction.  
  - Stays in the same position if encountering a wall.  

### Rewards  
- **White squares**: Score **-0.04**.  
- **Brown squares**: Score **-1**.  
- **Green squares**: Score **+1**.  

### Environment Characteristics   
- **Infinite sequence**: There are no terminal states.  
- **Discount Factor**: 0.99.  

---

## Assignment Objectives  

### Part A  
1. **Compute Optimal Policy**: Find and display the optimal policy for all non-wall states using **Value Iteration** and **Policy Iteration**.  
2. **Utility Estimates**: Display the final state utility values for all non-wall states.  
3. **Plot Convergence**: Visualize utility estimates as a function of the number of iterations.  

### Part B (Bonus)  
1. Design a **more complex maze environment** and re-run the algorithms.  
2. Analyze:  
   - How does the number of states and complexity impact convergence?  
   - How complex can the environment get while still learning the optimal policy?  

---

## Implementation  

### Algorithms Used  
1. **Value Iteration**: Iteratively updates utility values until convergence, then derives the optimal policy.  
2. **Policy Iteration**: Alternates between policy evaluation and policy improvement to compute the optimal policy.  

### Libraries/Tools  
- Python (NumPy, Matplotlib)  

---

## Results  
- Displayed the **optimal policy** for the given maze environment.  
- Showed **state utility values** for all non-wall states.  
- Plotted utility estimates vs. the number of iterations.  
- Designed and tested on a **custom complex maze**, observing how complexity affects convergence.  
