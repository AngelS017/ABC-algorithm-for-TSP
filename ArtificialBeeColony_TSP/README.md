# Artificial Bee Colony (ABC) for Solving the Traveling Salesman Problem (TSP)

![Artificial Bee Colony](https://img.shields.io/badge/Artificial%20Bee%20Colony-ABC%20Algorithm-blue.svg) 
![Python](https://img.shields.io/badge/Python-3.7%2B-brightgreen.svg)
![TSP](https://img.shields.io/badge/Problem-TSP-orange.svg) 
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


This project implements an Artificial Bee Colony (ABC) algorithm for solving the Traveling Salesman Problem (TSP), where the goal is to find the shortest possible route that visits a set of cities exactly once and returns to the starting point.

## Table of Contents
- [Author and contact](#author-and-contact)
- [Overview](#overview)
- [Algorithm Workflow](#algorithm-workflow)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Classes and Functions](#classes-and-functions)
- [Usage](#usage)
- [Tuning Parameters](#tuning-parameters)
- [Contributing](#contributing)
- [License](#license)


## Author and contact

Author: Angel Sanz Gutierrez\
Contact: sanzangel017@gmail.com\
GitHub: AngelS017\
License: MIT License


## Overview

The Artificial Bee Colony (ABC) algorithm is a bio-inspired optimization technique modeled after the intelligent foraging behavior of honeybees. This algorithm is highly effective for solving complex optimization problems like the Traveling Salesman Problem (TSP), where the objective is to find the shortest path that visits all cities exactly once and returns to the starting city.

In this implementation, bees are divided into three roles: employed bees, onlooker bees, and scout bees. 
Each role contributes to exploring the search space and improving potential solutions. 

* Employed bees focus on exploitation new food sources (solutions). 

* Onlooker bees focus on selective exploitation, probabilistically select and improve upon the best-found solutions.

* Scout bees introduce exploration by abandoning poor solutions.

This implementation provides a flexible ABC framework, allowing users to:

* Customize the mutation strategies for exploring different paths.

* Customize the porcentage of bees of each role (Employed and Onlooker).

* Adjust the colony size, exploitation limits and the number of epochs to optimize the problem.


## Algorithm Workflow

1. Initialization:

    A population of bees (solutions) is randomly initialized. The population is divided into employed bees and onlooker bees.
    Each employed bee is assigned a random TSP route, and the initial distance for each route is calculated.

2. Employed Bee Phase:

    Employed bees explore new routes by applying mutation strategies.
    If the new route is shorter, the employed bee updates its current route.

3. Onlooker Bee Phase:

    Onlooker bees choose solutions based on the probability proportional to the solution’s quality (distance).
    Onlookers explore new routes and improve upon the best ones found by employed bees.

4. Scout Bee Phase:

    If an employed bee fails to find a better route for a predefined number of trials, it becomes a scout bee and is reinitialized with a new random route.

5. Convergence:

    The algorithm is executed for a defined number of epochs, constantly trying to improve the routes and recording the best solution found.


## Folder Structure

    ArtificialBeeColony_TSP
    ├── abc_tsp
    |   ├── ArtificialBeeColony_TSP.py
    |   └── __init__.py
    ├── README.md
    ├── LICENSE
    └── setup.py

## Prerequisites

The following open source packages are used to develop this algorithm:
* numpy >= 1.20
* tqdm

Additionally, the software requires the Python 3.7 or higher version, as this is the minimum version supported by the tqmd packages.

However, it is recommended that the most recent versions of Numpy and Python be installed in order to achieve optimal performance and the fastest results.

## Installation

To install the ABC algorithm for the TSP, you just need to:

    pip install abc-tsp

    
## Classes and Functions
* Bee
  * Attributes:
    * **role:** Defines whether the bee is Employed, Onlooker, or Scout.
    * **path:** The current TSP path the bee is exploring.
    * **path_len:** The len of the path - 2 (used to select the indexes of the   path for the mutation strategy)
    * **path_distance:** The total distance of the current path.
    * **trial:** Number of unsuccessful attempts to improve the current path.
    * **mutation_strategy:** The mutation startegy used by the bees to generate new solutions.

  * Methods:

    * **_select_mutation_strategy():** Selects the appropriate mutation strategy based on the provided strategy name
    * **swap():** The swap strategy
    * **insertion():** The insertion strategy
    * **k_opt():** The k-opt strategy
    * **mutate_path():** Applies a mutation strategy (e.g., swap, insertion, k-opt) to generate new paths.
    * **distance_path():** Calculates the total distance of the given path using the distance matrix.

* ArtificialBeeColonyOptimizer
  * Attributes:
    * **ini_end_city:** The city where the path starts and ends.
    * **population:** Total number of bees in the colony.
    * **employed_percentage:** Percentage of employed bees in the colony.
    * **limit:** Trial limit before a bee becomes a scout.
    * **epochs:** Number of iterations the algorithm will run.
    * **distance_matrix:** Matrix containing the distances between cities.
    * **employed_mutation_strategy:** The mutation strategy used by the employed bees.
    * **onlooker_mutation_strategy:** The mutation strategy used by the onlooker bees.
    * **k_employed:** The number of edges to remove in the k-opt startegy if selected in the employed_mutation_strategy for the employed bees.
    * **k_onlooker:** The number of edges to remove in the k-opt startegy if selected in the onlooker_mutation_strategy for the onlooker bees.
    * **seed:** The seed for the random numbers.
    * **verbose:** If you want to see the information after de training of the algorithm.

  * Methods:
    * **initialize_colony_with_roles():** Initializes the bee colony with random paths and their roles.
    * **employed_bee_behavior():** The logic behind employed bees improving their solutions.
    * **caclulate_probabilities:** Compute the probability of choosing each solution in the colony.
    * **roulette_wheel_selection:** Apply the roulet wheel selction to choose the best solution in the colony for the onlooker bee.
    * **onlooker_bee_behavior():** Onlooker bees probabilistically select solutions and improve them.
    * **scout_bee_behavior():** Resets bees that haven’t improved after several trials.
    * **find_best_path():** Finds and returns the best path in the current colony.
    * **fit():** The main loop for optimizing the TSP solution using the ABC algorithm.


## Usage

To use this implementation of the Artificial Bee Colony (ABC) algorithm for solving TSP, follow the basic structure provided below:

~~~python

from abc_tsp import ArtificialBeeColonyOptimizer

# Define the TSP problem as a distance matrix
distance_matrix = np.array([...]) #Square matrix of distances: cities x cities

# Create an instance of the ABC optimizer
abc_optimizer = ArtificialBeeColonyOptimizer(
    ini_end_city=0,  
    population=25,  
    employed_percentage=0.5,  
    limit=2000,  
    epochs=60000,  
    distance_matrix=distance_matrix, 
    employed_mutation_strategy='k_opt',  
    onlooker_mutation_strategy='k_opt',  
    k_employed=6,  
    k_onlooker=6,  
    seed=1234, 
    verbose=1  
)

# Fit the model and solve the TSP
execution_time, paths_distances, final_best_path, final_best_path_distance = abc_optimizer.fit()

# Results
print(f"Best Path: {final_best_path}")
print(f"Best Path Distance: {final_best_path_distance}")
print(f"Execution Time: {execution_time} seconds")
~~~


## Tuning Parameters

The ArtificialBeeColonyOptimizer class allows you to customize key parameters for tuning the algorithm:

* population
* employed_percentage
* limit
* epochs
* employed_mutation_strategy and onlooker_mutation_strategy
* k_employed and k_onlooker

Depending on the data, you may need to search for the optimal values of these parameters in order to get the best result (probably taking into account the time and the path distance).


## Contributing

If you wish to contribute, please fork the repository and create a pull request with a detailed description of the changes. 

Contributions for adding new features, fixing bugs, or improving performance are welcome!


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center"> <img src="https://img.shields.io/badge/License-MIT-blue.svg"> </div>








