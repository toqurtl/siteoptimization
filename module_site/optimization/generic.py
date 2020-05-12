import numpy as np
import random


class BinaryGeneric(object):
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
            if idx != len(point_list) -1:
                start = point_list[idx]
                last = point_list[idx + 1]
                chro = chro_list[idx % 2]
                new_chr += chro[start:last]
        return new_chr

    @classmethod
    def one_point_crossover(cls, chro_1, chro_2):
        len_chro = len(chro_1)
        split_position = random.randint(0, len_chro)
        print(split_position)
        return chro_1[:split_position] + chro_2[split_position:]

    @classmethod
    def local_mutation(cls, chro_str, num=1):
        len_chro = len(chro_str)
        new_chro = chro_str
        for i in range(0, num):
            idx = random.randint(0, len_chro)
            print(idx)
            insert_str = '0' if chro_str[idx] == '1' else '1'
            new_chro = new_chro[:idx] + insert_str + new_chro[idx+1:]
        return new_chro

    @classmethod
    def global_mutation(cls, chro_class):
        return chro_class.get_random_chromosome()




