import numpy as np
from module_site.optimization.chromosome import BinaryChromosome
from module_site.optimization.generic import BinaryGeneric, BinaryLocalAlgorithm
from module_site.optimization.generation import Fronting, MultiObjectiveGenerator, MultiObjGenericEnum
from module_site.optimization.optimizer import ParetoOptimizer
from functools import reduce


def test_function_1(chro_str):
    unit_chromosome = BinaryChromosome.get_phenotype_part(chro_str, 'num_unit')
    return np.array([int('0b' + unit_chromosome, 2)])


def test_function_2(chro_str):
    unit_chromosome = BinaryChromosome.get_phenotype_part(chro_str, 'num_unit')
    labor_chromosome = BinaryChromosome.get_phenotype_part(chro_str, 'num_labor')
    return np.array([int('0b'+unit_chromosome, 2), int('0b'+labor_chromosome, 2)])


num_labor_list = np.array([2, 2, 4])
num_unit_in_group_list = np.array([5, 6, 10])
unit_arrived_rate_list = np.array([5])

element_info = {'num_labor': num_labor_list, 'num_unit':num_unit_in_group_list, 'unit_arrived': unit_arrived_rate_list}

content_1 = {'num': 3, 'min': 1, 'max': 6, 'digit': 3}
content_2 = {'num': 5, 'min': 1, 'max': 63, 'digit': 6}
content_3 = {'num': 1, 'min': 1, 'max': 40, 'digit': 6}

# num of value of each content, min value of each content, max_value of each content, num_digit of each content
geno_shape = {'num_labor': content_1, 'num_unit': content_2, 'unit_arrived': content_3 }

BinaryChromosome.set_geno_shape(**geno_shape)
gene_list = BinaryChromosome.get_random_chromosome_from_geno_shape(10)

optimizer_parameter_dict = {
    'num_chromosome_in_generation': 100,
    'max_generation': 10
}

generic_parameter_dict = {
    MultiObjGenericEnum.SUPERIOR: 0.2,
    MultiObjGenericEnum.ONE_POINT_CROSSOVER: 0.4,
    MultiObjGenericEnum.LOCAL_MUTATION: 0.2,
    MultiObjGenericEnum.GLOBAL_MUTATION: 0.2
}

multi_objective = MultiObjectiveGenerator(test_function_2, generic_parameter_dict)
multi_objective.local_algorithm_enum = BinaryLocalAlgorithm.LK


p = ParetoOptimizer(multi_objective, generic_parameter_dict)
p.initialization()
for i in range(0, 10):
    p.next_generation()

generation = p.generation_list[-1]
for chromosome, objectives in generation:
    print(objectives)
Fronting.num_objective = 2
Fronting.fronting(generation)
idx = 0
for front in Fronting.front_list:
    print(idx)
    for a in front:
        print(a)
    idx+=1
# print(p.generation_list[-1].T[0].tolist().sort(key=lambda x: test_function_2(x)[0], reverse=True))
