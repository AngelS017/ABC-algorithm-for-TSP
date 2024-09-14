"""
File: ArtificialBeeColony.py
Author: Angel Sanz Gutierrez
Contact: sanzangel017@gmail.com
GitHub: AngelS017
Description: All clases and function to apply ABC in the TSP
Version: 1.0

This file is the ABC algorithm for TSP, which is licensed under the MIT License.
See the LICENSE file in the project root for more information.
"""

import numpy as np
import math
import random
from tqdm import tqdm
import time
import itertools


class Bee:
    def __init__(self, random_path, mutation_strategy) -> None:
        self.role = ''
        self.path = random_path
        self.path_len = len(random_path) - 2
        self.path_distance = 0
        self.trial = 0
        self.mutation_strategy = self._select_mutation_strategy(mutation_strategy)


    def _select_mutation_strategy(self, mutation_strategy):
        """Selects the appropriate mutation strategy based on the provided strategy name.

        Parameters
        ----------
        self : Bee
            The instance of the bee.

        mutation_strategy : str
            The name of the mutation strategy to be used. Must be one of the keys 
            in the dictionary all_mutation_strategies.

        Returns
        -------
        function
            The mutation function corresponding to the selected strategy.

        """
        all_mutation_strategies = {
            'swap': self.swap,
            'insertion': self.insertion,
            'k_opt':self.k_opt
        }
        return all_mutation_strategies[mutation_strategy]

    @staticmethod
    def swap(len_path, path, k):
        """Compute the new path, using two different indexes (except the first and the last) of the 
           actual path and change its values.

        Parameters
        ----------
        len_path : int
            The len of the path - 2, is needed to select the possible indexes for the swap method.
        
        path : array-like
            The actual path that conteins all the points, where the start and the end is the same point.

        k : int

        Returns
        -------
        new_path: The new path.

        """
        new_path = path[:]

        # Other way, but slower: random_index, random_index_2 = sorted(random.sample(range(1, len_path), 2))
        random_index = random.randint(1, len_path)
        random_index_2 = random.randint(1, len_path)
        while random_index == random_index_2:
            random_index_2 = random.randint(1, len_path)
        
        new_path[random_index], new_path[random_index_2] = new_path[random_index_2], new_path[random_index]
        
        return [new_path]

    @staticmethod
    def insertion(len_path, path, k):
        """
        
        Parameters
        ----------
        len_path : int
            The len of the path - 2, is needed to select the possible indexes for the insertion method.

        path : array-like
            The actual path that conteins all the points, where the start and the end is the same point.

        k : int

        Returns
        -------
        new_path: The new path.

        """
        new_path = path[:]

        random_index = random.randint(1, len_path)
        random_index_2 = random.randint(1, len_path)
        while random_index == random_index_2:
            random_index_2 = random.randint(1, len_path)

        #value = new_path[random_index]
        #new_path = np.delete(new_path, random_index)
        #new_path = np.insert(new_path, random_index_2, value)
        new_path = np.concatenate((new_path[:random_index], new_path[random_index+1:random_index_2], [new_path[random_index]], new_path[random_index_2:]))
        
        return [new_path]

    @staticmethod
    def k_opt(len_path, path, k):
        """Apply the k-opt method for creating a new path, where the k means the number of
           edges that is going to be remove in order to create the new conections for the path.

           Steps:
               1. Generate the random indexes for the methos, the init and end of these values can´t be
                  the first and last position of the path, taht why it starts at 1 and ends at len(path) - 2
               2. Create the segments of the path with the random indexes generated.
               3. Save the middle segments of the path, this are the ones that will be use for the k-opt method.
               4. Crete all the possible combinations for the new connections of the segments (the new edges)
               5. Create all the possibles paths.

        Parameters
        ----------
        len_path : int
            The len of the path - 2, is needed to select the possible indexes for the k_opt method.

        path : array-like
            The actual path that conteins all the points, where the start and the end is the same point.

        k : int
            The number of the k-opt method that is going to perform

        Returns
        -------
        new_path: The new path.

        """
        random_index = sorted(random.sample(range(1, len_path), k))

        segments = [path[:random_index[0]+1]]
        segments.extend([path[random_index[i]+1:random_index[i+1]+1] for i in range(k-1)])
        segments.append(path[random_index[-1]+1:])

        middle_segments = [[segmento, segmento[::-1]] for segmento in segments[1:-1]]

        possible_permutations = list(itertools.product(*middle_segments)) + list(itertools.product(*middle_segments[::-1]))
        
        new_path = [np.concatenate((segments[0], *perm, segments[-1])) for perm in possible_permutations]
        new_path = new_path[1:]

        return new_path
    
    def mutate_path(self, distance_matrix, k):
        """

        Parameters
        ----------
        self : Bee
            The instance of the bee.

        distance_matrix: array-like
            The matrix that conteins the euclidian distance between each point.

        k : int
            The number of the k-opt method that is going to perform.

        Returns
        -------
        best_path : The best path found during the generation of the new solution

        """
        all_paths = self.mutation_strategy(self.path_len, self.path, k)
        best_path = min(all_paths, key=lambda path: self.distance_path(path, distance_matrix))

        return best_path

    def distance_path(self, path, distance_matrix):
        """Compute the distance of all the points in the path.

        Parameters
        ----------
        self : Bee
            The instance of the bee. 

        path : array-like
            The actual path that conteins all the points, where the start and the end is the same point.
        
        distance_matrix: array-like
            The matrix that conteins the euclidian distance between each point.

        Returns
        -------
        distance: The total distance of the path.

        """
        return np.sum(distance_matrix[path[:-1], path[1:]])



class ArtificialBeeColonyOptimizer:
    def __init__(self, ini_end_city, population, employed_percentage, limit, epochs, distance_matrix, employed_mutation_strategy, onlooker_mutation_strategy, 
                 k_employed=3, k_onlooker=3, seed=1234, verbose=1):
        all_stategies = ['swap', 'insertion', 'k_opt']
        # Check that all parameters have the correct values
        assert ini_end_city < distance_matrix.shape[0], "You must choose a correct city"
        assert 0.1 <= employed_percentage <= 0.9, "The value of employed_percentage must be between 0.1 and 0.9"
        assert epochs > 0, "The number of epochs must be greater than 0"
        assert employed_mutation_strategy in all_stategies, "Unknown employed mutation strategy, must be one of theese: " + ', '.join(all_stategies)
        assert onlooker_mutation_strategy in all_stategies, "Unknown onlooker mutation strategy, must be one of theese: " + ', '.join(all_stategies)

        if employed_mutation_strategy == 'k_opt':
            assert k_employed >= 2, "The value of k_employed for k_opt must be 2 or more"
        if onlooker_mutation_strategy == 'k_opt':
            assert k_onlooker >= 2, "The value of k_onlooker for k_opt must be 2 or more"

        np.random.seed(seed)
        random.seed(seed)

        self.ini_end_city = ini_end_city
        self.population = population
        self.employed_percentage = employed_percentage
        self.limit = limit
        self.epochs = epochs
        self.distance_matrix = distance_matrix
        self.employed_mutation_strategy = employed_mutation_strategy
        self.onlooker_mutation_strategy = onlooker_mutation_strategy
        self.k_employed = k_employed
        self.k_onlooker = k_onlooker
        self.verbose = verbose
        self.colony = self.initialize_colony_with_roles()

    def initialize_colony_with_roles(self):
        """

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony. 

        Returns
        -------
        colony : 

        """
        num_cities = self.distance_matrix.shape[0]
        other_cities = np.delete(np.arange(num_cities), self.ini_end_city)
        num_employed_bees = math.floor(self.population * self.employed_percentage)
        
        colony = []
        for i in range(self.population):
            random_path = np.insert(np.random.permutation(other_cities), [0, len(other_cities)], self.ini_end_city)
            if i >= num_employed_bees:
                bee = Bee(random_path, self.onlooker_mutation_strategy)
                bee.role = 'Onlooker'
            else:
                bee = Bee(random_path, self.employed_mutation_strategy)
                bee.role = 'Employed'
        
            bee.path_distance = bee.distance_path(bee.path, self.distance_matrix)
            colony.append(bee)

        return colony

    def employed_bee_behavior(self, bee):
        """The bee will perform the employed behavior, in which a new path is generated and 
           if the new path distance is better than the old one the path and his distance is 
           actualized in the bee. The number of trials increase only when the new distance is worse.

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony. 

        bee : Bee
            The bee of the colony which is going to perform the employed behavior.

        Returns
        -------
        bee : The bee of the colony with updated parameters.

        """
        new_path = bee.mutate_path(self.distance_matrix, self.k_employed)
        new_path_distance = bee.distance_path(new_path, self.distance_matrix)
        
        if new_path_distance < bee.path_distance:
            bee.path = new_path
            bee.path_distance = new_path_distance
            bee.trial = 0
        else:
            bee.trial += 1

    def caclulate_probabilities(self):
        """Compute the probability of choosing each solution in the colony, where the distance path of
           each bee is divided by the sum of all distances in the colony

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony. 

        Returns
        -------
        probabilities_bee_solution : The array of probabilities.

        """
        path_distances = np.array([bee.path_distance for bee in self.colony], dtype=float)
        return path_distances / np.sum(path_distances)

    def roulette_wheel_selection(self, probabilities):
        """Apply the roulet wheel selction to choose the best solution in the colony 
           for the onlooker bee

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony. 

        probabilities : array-like
            The array of probabilities.

        Returns
        -------
        bee : The best bee to choose in the colony

        """
        return self.colony[np.random.choice(len(probabilities), p=probabilities)]
    
        # Another way to make roulette wheel selection, more interpretable but more computationally expensive:
        """
        cumulative_probabilities = np.cumsum(probabilities)
        r = np.random.rand()
        for index, cumulative_probability in enumerate(cumulative_probabilities):
            if r < cumulative_probability:
                return self.colony[index]
        return self.colony[-1]
        """
       

    def onlooker_bee_behavior(self, bee, probabilities_bee_solution):
        """The bee will perform the onlooker behavior, in which a possible solution will be 
            choosen if a random numeber is lower than the probability of that solution 
            (the solutions with high probability will be the ones most likely to be chosen) then
            a new path is generated and if the new path distance is better than the old one 
            the path and his distance is actualized in the bee. The number of trials increase 
            only when the new distance is worse.

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony.

        bee : Bee
            The bee of the colony which is going to perform the employed behavior.
        
        probabilities_bee_solution : array-like
            The array of probabilities of all bees in the colony.

        Returns
        -------
        None
            This method updates the bee 

        """
        best_bee_colony = self.roulette_wheel_selection(probabilities_bee_solution)

        # Create a new path from the best bee found (path) local search
        new_path = best_bee_colony.mutate_path(self.distance_matrix, self.k_onlooker)
        new_path_distance = best_bee_colony.distance_path(new_path, self.distance_matrix)
        
        if new_path_distance < best_bee_colony.path_distance:
            bee.path = new_path
            bee.path_distance = new_path_distance
            bee.trial = 0
        else:
            # Update the current onlooker bee with the best solution found until now
            # because the new posible solution is worst
            bee.path = best_bee_colony.path
            bee.path_distance = best_bee_colony.path_distance

            bee.trial += 1

    def scout_bee_behavior(self):
        """The bee will perform the scout behavior, where all the bees in the 
       colony that have passed the threshold of trials have initialized 
       their parameters.

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony.

        Returns
        -------
        None

        """

        num_cities = self.distance_matrix.shape[0]
        other_cities = np.delete(np.arange(num_cities), self.ini_end_city)
        for bee in self.colony:
            if bee.trial > self.limit:
                random_path = np.insert(np.random.permutation(other_cities), [0, len(other_cities)], self.ini_end_city)

                bee.trial = 0
                bee.path = random_path
                bee.path_distance = bee.distance_path(bee.path, self.distance_matrix)

    def find_best_path(self):
        """Find the best path among all the bees in the colony and also the sitance of
           that path.

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony. 

        Returns
        -------
        path : The best path found among all the bees in the colony
        path_distance : The total distance of the best path found

        """
        min_bee = min(self.colony, key=lambda bee: bee.path_distance)
        return min_bee.path, min_bee.path_distance

    def fit(self):
        """Train the ABC algorithm to find the best path in the TSP.

        Parameters
        ----------
        self : ArtificialBeeColonyOptimizer
            The instance of the optimizer that manages the bee colony.

        Returns
        -------
        execution_time : The time taken to train the ABC model
        paths_distances : The distance of all the paths founds during training
        final_best_path : The best path found after training
        final_best_path_distance : The distance of the best path found

        """
        start = time.time()

        paths_distances = []
        num_employed_bees = math.floor(self.population * self.employed_percentage)

        for _ in tqdm(range(self.epochs), desc="Training Progress", unit="epoch"):
            for employed_index in range(num_employed_bees):
                self.employed_bee_behavior(self.colony[employed_index])
            
            probabilities_bee_solution = self.caclulate_probabilities()
            
            for onlooker_index in range(num_employed_bees, self.population):
                self.onlooker_bee_behavior(self.colony[onlooker_index], probabilities_bee_solution)
                
            self.scout_bee_behavior()

            _, best_path_distance = self.find_best_path()
            paths_distances.append(best_path_distance)

        final_best_path_distance = np.min(paths_distances)
        final_best_path, _ = self.find_best_path()
        if self.verbose == 1:
            print(f"Params:\n\t("
                  f"ini_end_city={self.ini_end_city}, "
                  f"population={self.population}, "
                  f"epochs={self.epochs},",
                  f"limit={self.limit},",
                  f"employed_percentage={self.employed_percentage},",
                  f"onlooker_percentage={1-self.employed_percentage})"
                )
            print("\nMin path distance: ", final_best_path_distance)
            print("The best path found is: \n", final_best_path)

        end = time.time()
        execution_time = end - start

        return execution_time, paths_distances, final_best_path, final_best_path_distance
