import numpy as np
from .generic import BinaryGeneric, BinaryLocalAlgorithm
from .chromosome import BinaryChromosome
from .generation import Fronting


class ParetoOptimizer(object):
    # generation_list - chromosome, objective value
    def __init__(self, generation_generator, generic_parameter_dict):
        self.num_chromosome_in_generation = 50
        self.max_generation = 10
        self.num_objective = 2
        self.generation_generator = generation_generator
        self.objective_function = generation_generator.fitness_func
        self.local_algorithm = generation_generator.local_algorithm_enum
        self.generic_parameter_dict = generic_parameter_dict
        self.generation_list = []
        Fronting.num_objective = self.num_objective

    def setting(self, num_chromosome_in_generation=50, max_generation=10, num_objective=2):
        self.num_chromosome_in_generation = num_chromosome_in_generation
        self.max_generation = max_generation
        self.num_objective = num_objective

    def optimize(self):
        self.initialization()
        for idx in range(0, self.max_generation):
            print(idx)
            self.next_generation()

    def initialization(self):
        num = self.num_chromosome_in_generation
        chromosome_list = BinaryChromosome.get_random_chromosome_from_geno_shape(num)
        local_optimized_chromosome_list = []
        for chromosome in chromosome_list:
            chromosome, objective_values = self.local_algorithm(chromosome, self.objective_function)
            local_optimized_chromosome_list.append((chromosome, objective_values))
        self.generation_list.append(np.array(local_optimized_chromosome_list))

    def next_generation(self):
        self.generation_generator.set_generation(self.generation_list[-1])
        new_generation_info = self.generation_generator.get_new_generation(self.num_chromosome_in_generation * 2)
        Fronting.fronting(new_generation_info)
        new_generation_info = Fronting.get_survived_chromosome(self.num_chromosome_in_generation)
        self.generation_list.append(new_generation_info)
        return new_generation_info



