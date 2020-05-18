from .generic import BinaryGeneric, BinaryLocalAlgorithm
from .chromosome import BinaryChromosome
from .exception import HyperParameterSettingError
import random
import numpy as np
from enum import Enum


class Fronting(object):
    num_objective = 0
    max_objective_list = []
    min_objective_list = []
    front_list = []

    @classmethod
    def __initialize(cls):
        cls.max_objective_list.clear()
        cls.min_objective_list.clear()
        cls.front_list.clear()

    @classmethod
    def fronting(cls, generation):
        cls.__set_max_min_list(generation)
        cls.__fronting(generation)
        cls.__set_crowding_distance()

    @classmethod
    # generation is the list contains chromosome information as tuple
    def __set_max_min_list(cls, generation):
        for idx in range(0, cls.num_objective):
            chromosome_objective_list = list(map(lambda chro_info_tuple: chro_info_tuple[1][1], generation))
            cls.max_objective_list.append(max(chromosome_objective_list))
            cls.min_objective_list.append(min(chromosome_objective_list))

    @classmethod
    # front - (rank, chromosome_info_list)
    # chromosome_info = chromosome, objective, crowding_distance
    def __fronting(cls, generation):
        not_fronted_chromosome_list = []
        for chromo_info in generation:
            not_fronted_chromosome_list.append(chromo_info)
        infinite_check = 0
        rank = 0
        while len(not_fronted_chromosome_list) > 0:
            infinite_check += 1
            new_front = (rank, [])
            for chromosome_1, objective_1 in not_fronted_chromosome_list:
                num_dominates = sum([1 for chromosome_2, objective_2 in not_fronted_chromosome_list if objective_1 < objective_2])
                if num_dominates is 0:
                    new_front[1].append((chromosome_1, objective_1))
            for chromosome in new_front[1]:
                not_fronted_chromosome_list.remove(chromosome)
            rank += 1
            cls.front_list.append(new_front)
            if infinite_check >= 1000:
                print('infinite loop in _fronting function in front.py')
                exit()

    @classmethod
    def __set_crowding_distance(cls):
        for front in cls.front_list:
            cls.__crowd_distancing_in_the_front(front)

    @classmethod
    def __crowd_distancing_in_the_front(cls, front):
        rank, chro_info_list = front
        objective_diff_list = np.array(cls.max_objective_list) - np.array(cls.min_objective_list)
        for idx, chro_info in enumerate(chro_info_list):
            chromosome, objectives, _ = chro_info
            try:
                previous_chromosome, previous_objectives = chro_info_list[idx - 1]
                behind_chromosome, behind_objectives = chro_info_list[idx + 1]
                crowding_distance_list = (np.array(previous_objectives) + np.array(behind_objectives)) \
                                                  / np.array(objective_diff_list)
                crowding_distance = crowding_distance_list.sum()
                return chromosome, objectives, crowding_distance
            except ZeroDivisionError:
                return chromosome, objectives, 10000
            except IndexError:
                return chromosome, objectives, 10000


# this script define methodology to make next generation
def fill_chromosome_list(func):
    chromosome_list = []

    def wrapper_function(*args):
        generation, num_chromosome = args[0].generation, args[1]
        local_algorithm, fitness_func = args[0].local_algorithm_enum, args[0].fitness_func
        while len(chromosome_list) < num_chromosome:
            new_chromosome = func(*args)
            new_chromosome = local_algorithm(new_chromosome, fitness_func)
            if (new_chromosome not in generation) and (new_chromosome not in chromosome_list):
                chromosome_list.append(new_chromosome)
        return chromosome_list
    return wrapper_function


class MultiObjectiveGenerator(object):

    def __init__(self, fitness_func, generic_parameter_dict):
        self.__local_algorithm_enum = BinaryLocalAlgorithm.NONE
        self.fitness_func = fitness_func
        self.generic_parameter_dict = generic_parameter_dict
        self.__check_genericparameter()
        self.generation = []

    def set_generation(self, generation):
        self.generation.clear()
        for chromosome in generation:
            self.generation.append(chromosome)

    @property
    def local_algorithm_enum(self):
        return self.__local_algorithm_enum

    @local_algorithm_enum.setter
    def local_algorithm_enum(self, local_enum):
        self.__local_algorithm_enum = local_enum

    def clear(self):
        self.generation.clear()

    def get_new_generation(self):
        pass

    def superior(self, num_chromosome):
        return self.generation[:num_chromosome]

    @fill_chromosome_list
    def multi_point_crossover(self, num_chromosome):
        # TODO - point_list setting process
        point_list = [5, 10]
        return BinaryGeneric.multi_point_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome(), point_list)

    @fill_chromosome_list
    def one_point_crossover(self, num_chromosome):
        return BinaryGeneric.one_point_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome())

    @fill_chromosome_list
    def random_point_crossover(self, num_chromosome):
        return BinaryGeneric.random_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome())

    @fill_chromosome_list
    def local_mutation(self, num_chromosome):
        num_mutation_gene = 1
        return BinaryGeneric.local_mutation(self.__get_random_chromosome(), num_mutation_gene)

    @fill_chromosome_list
    def global_mutation(self, num_chromosome):
        chromosome_class = BinaryChromosome
        return BinaryGeneric.global_mutation(chromosome_class)

    def __get_random_chromosome(self):
        random_idx = random.randint(0, len(self.generation)-1)
        return self.generation[random_idx]

    def __check_genericparameter(self):
        if sum(list(self.generic_parameter_dict.values())) != 1:
            raise HyperParameterSettingError


class MultiObjGenericEnum(Enum):
    SUPERIOR = MultiObjectiveGenerator.superior
    ONE_POINT_CROSSOVER = MultiObjectiveGenerator.one_point_crossover
    MULTI_POINT_CROSSOVER = MultiObjectiveGenerator.multi_point_crossover
    RANDOM_POINT_CROSSOVER = MultiObjectiveGenerator.random_point_crossover
    LOCAL_MUTATION = MultiObjectiveGenerator.local_mutation
    GLOBAL_MUTATION = MultiObjectiveGenerator.global_mutation