from .generic import BinaryGeneric, BinaryLocalAlgorithm
from .chromosome import BinaryChromosome
from .exception import HyperParameterSettingError
import random
import numpy as np
from enum import Enum
from functools import reduce

class Fronting(object):
    num_objective = 0
    max_objective_list = []
    min_objective_list = []
    front_list = []

    @classmethod
    def fronting(cls, generation):
        cls.__initialize()
        cls.__set_max_min_list(generation)
        cls.__fronting(generation)
        cls.__set_crowding_distance()

    @classmethod
    def __initialize(cls):
        cls.max_objective_list.clear()
        cls.min_objective_list.clear()
        cls.front_list.clear()

    @classmethod
    # generation is the list contains chromosome information as tuple
    def __set_max_min_list(cls, generation):
        objective_values = [chromosome_info[1] for chromosome_info in generation]
        objective_values = np.array(objective_values)
        cls.max_objective_list = np.max(objective_values, axis=0)
        cls.min_objective_list = np.min(objective_values, axis=0)


    def __check_dominate(cls, nparray):
        dominated_condition_1 = np.sum(nparray[:-1]) == cls.num_objective
        dominated_condition_2 = np.sum(nparray[:])
    @classmethod
    # front - (rank, chromosome_info_list)
    # chromosome_info = chromosome, objective, crowding_distance
    def __fronting(cls, generation):
        not_fronted_chromosome_dict = {}
        for chromosome, objective_values in generation:
            not_fronted_chromosome_dict[chromosome] = objective_values

        objective_value_list = np.array([chromosome_info[1] for chromosome_info in generation])
        while len(not_fronted_chromosome_dict) > 0:
            new_front = []
            dominated_list = []
            for chromosome, objective_1 in not_fronted_chromosome_dict.items():
                compare_array = objective_value_list > objective_1
                # equal_array = objective_value_list == objective_1
                # equal_array = np.apply_along_axis(lambda a: np.sum(a) == cls.num_objective - 1, 1, equal_array)
                # equal_array = np.expand_dims(equal_array, axis=0)
                # compare_array = np.concatenate((compare_array, equal_array.T), axis=1)
                compare_array = np.apply_along_axis(
                    lambda a: np.sum(a) == 1 or np.sum(a) == cls.num_objective, compare_array)
                print(compare_array)
                compare_array = reduce(lambda x, y: x & y, compare_array.T)


                print(compare_array)
                dominated = reduce(lambda x, y: x or y, compare_array)
                dominated_list.append(dominated)
                if not dominated:
                    new_front.append((chromosome, objective_1))
            for chromosome, objective_1 in new_front:
                del not_fronted_chromosome_dict[chromosome]
            objective_value_list = objective_value_list[dominated_list]
            cls.front_list.append(new_front)
            exit()


    @classmethod
    def __set_crowding_distance(cls):
        for front in cls.front_list:
            cls.__crowd_distancing_in_the_front(front)

    @classmethod
    def __crowd_distancing_in_the_front(cls, front):
        objective_diff_list = cls.max_objective_list - cls.min_objective_list
        for idx, chromosome_info in enumerate(front):
            chromosome, objectives = chromosome_info[0], chromosome_info[1]
            try:
                previous_chromosome, previous_objectives = front[idx - 1][0], front[idx - 1][1]
                behind_chromosome, behind_objectives = front[idx + 1][0], front[idx + 1][1]
                crowding_distance_list = (previous_objectives + behind_objectives) / objective_diff_list
                crowding_distance = crowding_distance_list.sum()
                return chromosome, objectives, crowding_distance
            except ZeroDivisionError:
                return chromosome, objectives, 10000
            except IndexError:
                return chromosome, objectives, 10000


# this script define methodology to make next generation
# chromosome_info -> numpy (chromosome, objective value)
def fill_chromosome_list(func):
    chromosome_info_list = []
    chromosome_list = []

    def wrapper_function(*args):
        generation, num_chromosome = args[0].generation, args[1]
        pre_chromosome_list = generation.T[0]
        local_algorithm, fitness_func = args[0].local_algorithm_enum, args[0].fitness_func
        while len(chromosome_list) < num_chromosome:
            new_chromosome = func(*args)
            new_chromosome, objective_values = local_algorithm(new_chromosome, fitness_func)
            if new_chromosome not in pre_chromosome_list and new_chromosome not in chromosome_list:
                chromosome_info_list.append((new_chromosome, objective_values))
                chromosome_list.append(new_chromosome)
        return chromosome_info_list
    return wrapper_function


class MultiObjectiveGenerator(object):

    def __init__(self, fitness_func, generic_parameter_dict):
        self.__local_algorithm_enum = BinaryLocalAlgorithm.NONE
        self.fitness_func = fitness_func
        self.generic_parameter_dict = generic_parameter_dict
        self.__check_genericparameter()
        self.generation = np.array([])

    def set_generation(self, generation):
        self.generation = generation

    @property
    def local_algorithm_enum(self):
        return self.__local_algorithm_enum

    @local_algorithm_enum.setter
    def local_algorithm_enum(self, local_enum):
        self.__local_algorithm_enum = local_enum

    def clear(self):
        self.generation.clear()

    def get_new_generation(self, num_chromosome_in_generation):
        new_generation = []
        for generic_function, generic_ratio in self.generic_parameter_dict.items():
            num = int(generic_ratio * num_chromosome_in_generation)
            new_generation += generic_function(self, num)
        return np.array(new_generation)

    def superior(self, num_chromosome):
        return self.generation[:num_chromosome].tolist()

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
        return self.generation[random_idx][0]

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