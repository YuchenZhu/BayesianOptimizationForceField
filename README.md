# BayesianOptimizationForceField
This project is my thesis of "Optimize ionic force field with bayesian optimization" at TUDelft. The aim of this research it to optimize ion force field parameters with a probablistic machine learning technique called bayesian optimization. This modle use gaussian process to model the unknown region in the parameter space and use acquisition function to guide the search. Previous work carried the parameter search mainly based on brute force method which are usually time comsuing. The advantage of this method is that it allows researcher to carry out parameters search without human interaction, thus the tieous force field optimization process can be speeded up. 
The considered ionic properties are:
- Item 1

## 1. Normalize parameter space, resulting smooth contour plot.
## 2. Train a Bayesian Optimization model, kernel function, balance parameters, normalize data, extend to different species and ionic properties.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/obs.png)
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/convergence.png)
## 3. MD simulations to compute the target properties.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/properties.png)
## 4. Find the optimum regions of primary targets: solvation free energy and ion oxygen distances.
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/primaryTgs.png)
## 5. Compute the secondary targets: diffusivity, ion pairing
![Image text](https://raw.githubusercontent.com/YuchenZhu/BayesianOptimizationForceField/main/img/ionPairs.png)
