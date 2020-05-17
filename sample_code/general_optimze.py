import numpy as np
from module_site.optimization.chromosome import BinaryChromosome
from module_site.optimization.generic import BinaryGeneric, GenericEnum
import math

num_labor_list = np.array([2, 2, 4, 3, 2, 4])
num_unit_in_group_list = np.array([3, 3, 4, 5, 6, 10])
unit_arrived_rate_list = np.array([5])

element_info = {'num_labor': num_labor_list, 'num_unit':num_unit_in_group_list, 'unit_arrived': unit_arrived_rate_list}


content_1 = {'num': 6, 'min': 1, 'max': 6, 'digit': 3}
content_2 = {'num': 6, 'min': 1, 'max': 40, 'digit': 6}
content_3 = {'num': 1, 'min': 1, 'max': 40, 'digit': 6}

# num of value of each content, min value of each content, max_value of each content, num_digit of each content
geno_shape = {'num_labor': content_1, 'num_unit': content_2, 'unit_arrived': content_3 }


def next_genertation(pre_generation, generic_setting):
    new_generation = []
    for generic_operator, ratio in generic_setting.items():
        num_chromosome = int(ratio * len(pre_generation))
        new_generation += generic_operator(pre_generation, num_chromosome)
    return new_generation


def containable_in_generation(chromosome, generation):
    return chromosome in generation

generic_setting = {
    GenericEnum.SELECTION: 0,
    GenericEnum.ONE_POINT_CROSSOVER: 0.3,
    GenericEnum.LOCAL_MUTATION: 0.3,
    GenericEnum.GLOBAL_MUTATION: 0.1
}

BinaryChromosome.set_geno_shape(**geno_shape)
check = BinaryChromosome.get_genotype(**element_info)
print(BinaryChromosome.get_phenotype(check))
print(BinaryChromosome.len_str_chromosome)
chro = BinaryGeneric.global_mutation(BinaryChromosome)
first_generation = BinaryChromosome.get_random_chromosome_from_geno_shape(100)
# second_generation = next_genertation(first_generation)

