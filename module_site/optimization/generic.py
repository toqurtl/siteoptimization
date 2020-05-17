import numpy as np
import random
from enum import Enum
import time


class BinaryGeneric(object):

    @classmethod
    def change_ith_gene(cls, chro_str, idx):
        insert_str = '0' if chro_str[idx] == '1' else '1'
        new_chro_str = chro_str[:idx] + insert_str + chro_str[idx + 1:]
        return new_chro_str

    @classmethod
    def selection(cls, generation):
        pass

    @classmethod
    def superior(cls, generation):
        pass

    @classmethod
    def random_crossover(cls, chro_1, chro_2):
        len_chro = len(chro_1)
        new_chro = ''
        for idx in range(0, len_chro):
            check = random.choice([True, False])
            new_chro += chro_1[idx] if check else chro_2[idx]
        return new_chro

    @classmethod
    # point_list have to contain 0 and last value
    def multi_point_crossover(cls, chro_1, chro_2, point_list):
        chro_list = [chro_1, chro_2]
        new_chr = ''
        for idx, point in enumerate(point_list):
            if idx != len(point_list) - 1:
                chro = chro_list[idx % 2]
                new_chr += chro[point_list[idx]: point_list[idx + 1]]
        return new_chr

    @classmethod
    def one_point_crossover(cls, chro_1, chro_2):
        len_chro = len(chro_1)
        split_position = random.randint(0, len_chro)
        return chro_1[:split_position] + chro_2[split_position:]

    @classmethod
    def local_mutation(cls, chro_str, num=1):
        new_chro = chro_str
        for i in range(0, num):
            random_idx = random.randint(0, len(chro_str))
            new_chro = cls.change_ith_gene(new_chro, random_idx)
        return new_chro

    @classmethod
    def global_mutation(cls, chro_class):
        return chro_class.get_random_chromosome()

    @classmethod
    def local_algorithm_lk(cls, chro_str, func):
        best_chro, best_value = chro_str, func(chro_str)
        for idx in range(0, len(chro_str)):
            new_chro = cls.change_ith_gene(chro_str, idx)
            new_value = func(new_chro)
            if best_value < func(new_chro):
                best_chro, best_value = new_chro, new_value
        return best_chro


class BinaryOperator(object):

    @classmethod
    def superior(cls, generation, num_chromosome):
        pass

    @classmethod
    def selection(cls, generation, num_chromosome):
        pass

    @classmethod
    def multi_point_crossover(cls, generation, num_chromosome):
        pass

    @classmethod
    def one_point_crossover(cls, generation, num_chromosome):
        pass

    @classmethod
    def random_crossover(cls, generation, num_chromosome):
        pass

    @classmethod
    def local_mutation(cls, generation, num_chromosome):
        pass

    @classmethod
    def global_mutation(cls, generation, num_chromosome):
        pass

    @classmethod
    def local_algorithm_lk(cls, generation, num_chromosome):
        pass

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


class GenericEnum(Enum):
    SELECTION = BinaryOperator.selection
    ONE_POINT_CROSSOVER = BinaryOperator.one_point_crossover
    MULTI_POINT_CROSSOVER = BinaryOperator.multi_point_crossover
    RANDOM_CROSSOVER = BinaryOperator.random_crossover
    LOCAL_MUTATION = BinaryOperator.local_mutation
    GLOBAL_MUTATION = BinaryOperator.global_mutation
    LOCAL_OPTIMIZATION_KL = BinaryOperator.local_algorithm_lk
