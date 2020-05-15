import numpy as np
from .generic import BinaryGeneric


class Generation(list):
    pass


class GeneralOptimizer(object):
    pass


class ParetoOptimizer(list):
    def __init__(self, generic_info, objectives):
        self.hyper_parameters = generic_info
        self.generation_list = []
        self.objective_function = []
        pass

    def initialization(self):
        pass

    def next_generation(self):
        last_generation = self.generation_list[-1]

        return


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
