from .chromosome import BinaryChromosome
import random
import numpy as np
from functools import reduce
from enum import Enum
from time import time


# to control function (chromosome to chromosome)
class BinaryGeneric(object):

    @classmethod
    def change_ith_gene(cls, chro_str, idx):
        insert_str = '0' if chro_str[idx] == '1' else '1'
        new_chro_str = chro_str[:idx] + insert_str + chro_str[idx + 1:]
        return new_chro_str

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
        split_position = random.randint(0, len_chro - 1)
        return chro_1[:split_position] + chro_2[split_position:]

    @classmethod
    def local_mutation(cls, chro_str, num=1):
        new_chro = chro_str
        for i in range(0, num):
            random_idx = random.randint(0, len(chro_str) - 1)
            new_chro = cls.change_ith_gene(new_chro, random_idx)
        return new_chro

    @classmethod
    def global_mutation(cls, chro_class):
        return chro_class.get_random_chromosome()


class BinaryLocalAlgorithm(Enum):

    # best value is ndarray
    @classmethod
    def local_algorithm_lk(cls, chro_str, func):
        best_chro, best_value = chro_str, func(chro_str)
        for idx in range(0, len(chro_str)):
            new_chro = BinaryGeneric.change_ith_gene(chro_str, idx)
            if BinaryChromosome.chromosome_fitted_in_geno_space(new_chro):
                new_value = func(new_chro)
                compare_array = best_value <= new_value
                if reduce(lambda x, y: x & y, compare_array):
                    best_chro, best_value = new_chro, new_value
        return best_chro, best_value

    @classmethod
    def local_algorithm_none(cls, chro_str, func):
        return chro_str, func(chro_str)

    NONE = local_algorithm_none
    LK = local_algorithm_lk
