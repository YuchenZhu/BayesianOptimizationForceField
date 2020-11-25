# BayesianOptimizationForceField
IonicForceFieldOptimization
Optimize ionic force field with bayesian optimization, search the most appropriate combinations without human interactions. 

# 1. Normalize parameter space, resulting smooth contour plot.
# 2. Train a Bayesian Optimization model, kernel function, balance parameters, normalize data, extend to different species and ionic properties.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/obs.png)
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/convergence.png)
# 3. MD simulations to compute the target properties.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/properties.png)
# 4. Find the optimum regions of primary targets: solvation free energy and ion oxygen distances.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/primaryTgs.png)
# 5. Compute the secondary targets: diffusivity, ion pairing
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/ionPairs.png)
