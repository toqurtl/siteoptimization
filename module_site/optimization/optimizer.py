import numpy as np
from .generic import BinaryGeneric, BinaryLocalAlgorithm
from .chromosome import BinaryChromosome


class GeneralOptimizer(object):
    pass


class ParetoOptimizer(list):
    def __init__(self, generation_generator, generic_parameter_dict):
        self.num_chromosome_in_generation = 100
        self.max_generation = 10
        self.generation_generator = generation_generator
        self.generic_parameter_dict = generic_parameter_dict
        self.generation_list = []

    def initialization(self):
        num = self.num_chromosome_in_generation
        gene_list = BinaryChromosome.get_random_chromosome_from_geno_shape(num)
        objective_function = self.generation_generator.fitness_func
        new_list = []
        for chromosome in gene_list:
            new_list.append(BinaryLocalAlgorithm.local_algorithm_lk(chromosome, objective_function))
        self.generation_list.append(new_list)

    def next_generation(self):
        self.generation_generator.set_generation(self.generation_list[-1])
        new_generation = []
        generic_parameter_dict = self.generation_generator.generic_parameter_dict
        for generic_function, generic_ratio in generic_parameter_dict.items():
            num = int(generic_ratio * self.num_chromosome_in_generation)
            new_generation += generic_function(self.generation_generator, num)
        self.generation_list.append(new_generation)


