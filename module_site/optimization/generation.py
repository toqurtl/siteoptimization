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

    @classmethod
    def save_front(cls):
        pass

    @classmethod
    def get_survived_chromosome(cls, num_chromosome_in_generation):
        new_generation_info = []
        sum = 0
        for idx, front in enumerate(cls.front_list):
            sum += len(front)
            if sum < num_chromosome_in_generation:
                new_generation_info += front
            else:
                remained_num = num_chromosome_in_generation - (sum - len(front))
                sorted_list = cls.__crowd_distancing_in_the_front(front, remained_num)
                new_generation_info += sorted_list
                break
        return np.array(new_generation_info)

    @classmethod
    def __initialize(cls):
        cls.max_objective_list = []
        cls.min_objective_list = []
        cls.front_list.clear()

    @classmethod
    # generation is the list contains chromosome information as tuple
    def __set_max_min_list(cls, generation):
        objective_values = [chromosome_info[1] for chromosome_info in generation]
        objective_values = np.array(objective_values)
        cls.max_objective_list = np.max(objective_values, axis=0)
        cls.min_objective_list = np.min(objective_values, axis=0)

    @classmethod
    def __fronting(cls, generation):
        not_fronted_chromosome_list = []
        for chromosome, objective_values in generation:
            not_fronted_chromosome_list.append((chromosome, objective_values))
        while len(not_fronted_chromosome_list) > 0:
            print(len(not_fronted_chromosome_list), end=', ')
            new_front = []
            for chromosome_1, objective_1 in not_fronted_chromosome_list:
                num_dominates = 0
                for chromosome_2, objective_2 in not_fronted_chromosome_list:
                    dominated = np.sum(objective_1 <= objective_2) == cls.num_objective
                    dominated = dominated and not np.sum(objective_1 == objective_2) == cls.num_objective
                    if dominated:
                        num_dominates += 1
                if num_dominates is 0:
                    new_front.append((chromosome_1, objective_1))
            for chromosome_1, objective_1 in new_front:
                not_fronted_chromosome_list.remove((chromosome_1, objective_1))
            cls.front_list.append(new_front)
        print()

    @classmethod
    def __crowd_distancing_in_the_front(cls, front, remained_num):
        objective_diff_list = cls.max_objective_list - cls.min_objective_list
        sorted_list = []
        for idx, chromosome_info in enumerate(front):
            chromosome, objectives = chromosome_info[0], chromosome_info[1]
            try:
                previous_chromosome, previous_objectives = front[idx - 1][0], front[idx - 1][1]
                behind_chromosome, behind_objectives = front[idx + 1][0], front[idx + 1][1]
                crowding_distance_list = (previous_objectives + behind_objectives) / objective_diff_list
                crowding_distance = crowding_distance_list.sum()
                sorted_list.append((chromosome, objectives, crowding_distance))
            except ZeroDivisionError:
                sorted_list.append((chromosome, objectives, 100000))
            except IndexError:
                sorted_list.append((chromosome, objectives, 100000))
        sorted_list.sort(key=lambda chromosome: chromosome[2], reverse=True)
        new_list = []
        for chromosome, objectives, crowding_distance in sorted_list[:remained_num]:
            new_list.append((chromosome, objectives))

        return new_list


# this script define methodology to make next generation
# chromosome_info -> numpy (chromosome, objective value)
def fill_chromosome_list(func):
    def wrapper_function(*args):
        chromosome_info_list = []
        chromosome_list = []
        num_chromosome, new_generation = args[1], args[2]
        local_algorithm, fitness_func = args[0].local_algorithm_enum, args[0].fitness_func
        new_generation_list = np.array(new_generation).T[0].tolist()
        while len(chromosome_list) < num_chromosome:
            new_chromosome = func(*args)
            new_chromosome, objective_values = local_algorithm(new_chromosome, fitness_func)
            if new_chromosome not in new_generation_list and new_chromosome not in chromosome_list:
                chromosome_info_list.append((new_chromosome, objective_values))
                chromosome_list.append(new_chromosome)
        return chromosome_info_list
    return wrapper_function


class MultiObjectiveGenerator(object):

    def __init__(self, fitness_func, generic_parameter_dict):
        self.__local_algorithm_enum = BinaryLocalAlgorithm.NONE
        self.fitness_func = fitness_func
        self.generic_parameter_dict = generic_parameter_dict
        self.__check_generic_parameter()
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
            new_generation += generic_function(self, num, new_generation)
        return np.array(new_generation)

    def superior(self, num_chromosome, new_generation):
        return self.generation[:num_chromosome].tolist()

    @fill_chromosome_list
    def multi_point_crossover(self, num_chromosome, new_generation):
        # TODO - point_list setting process
        point_list = [5, 10]
        return BinaryGeneric.multi_point_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome(), point_list)

    @fill_chromosome_list
    def one_point_crossover(self, num_chromosome, new_generation):
        return BinaryGeneric.one_point_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome())

    @fill_chromosome_list
    def random_point_crossover(self, num_chromosome, new_generation):
        return BinaryGeneric.random_crossover(
            self.__get_random_chromosome(), self.__get_random_chromosome())

    @fill_chromosome_list
    def local_mutation(self, num_chromosome, new_generation):
        num_mutation_gene = 1
        return BinaryGeneric.local_mutation(self.__get_random_chromosome(), num_mutation_gene)

    @fill_chromosome_list
    def global_mutation(self, num_chromosome, new_generation):
        chromosome_class = BinaryChromosome
        return BinaryGeneric.global_mutation(chromosome_class)

    def __get_random_chromosome(self):
        random_idx = random.randint(0, len(self.generation)-1)
        return self.generation[random_idx][0]

    def __check_generic_parameter(self):
        if sum(list(self.generic_parameter_dict.values())) != 1:
            raise HyperParameterSettingError


class MultiObjGenericEnum(Enum):
    SUPERIOR = MultiObjectiveGenerator.superior
    ONE_POINT_CROSSOVER = MultiObjectiveGenerator.one_point_crossover
    MULTI_POINT_CROSSOVER = MultiObjectiveGenerator.multi_point_crossover
    RANDOM_POINT_CROSSOVER = MultiObjectiveGenerator.random_point_crossover
    LOCAL_MUTATION = MultiObjectiveGenerator.local_mutation
    GLOBAL_MUTATION = MultiObjectiveGenerator.global_mutation