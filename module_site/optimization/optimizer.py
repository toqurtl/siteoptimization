import numpy as np
from .generic import BinaryGeneric, BinaryLocalAlgorithm
from .chromosome import BinaryChromosome


class GeneralOptimizer(object):
    pass


class ParetoOptimizer(object):
    # generation_list - chromosome, objective value
    def __init__(self, generation_generator, generic_parameter_dict):
        self.num_chromosome_in_generation = 10
        self.max_generation = 10
        self.generation_generator = generation_generator
        self.objective_function = generation_generator.fitness_func
        self.local_algorithm = generation_generator.local_algorithm_enum
        self.generic_parameter_dict = generic_parameter_dict
        self.generation_list = []

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
        new_generation_info = self.generation_generator.get_new_generation(self.num_chromosome_in_generation)
        self.generation_list.append(new_generation_info)
        return new_generation_info

    def __get_chromosome_list(self, generation_info):
        pass


