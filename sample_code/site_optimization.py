from module_site.optimization.chromosome import BinaryChromosome
from module_site.optimization.generic import BinaryGeneric, BinaryLocalAlgorithm
from module_site.optimization.generation import Fronting, MultiObjectiveGenerator, MultiObjGenericEnum
from module_site.optimization.optimizer import ParetoOptimizer
from module_site.core.component import ScheduleInformation, WorkType
from module_site.core.cpm import CPM
import numpy as np
import time
import module_site.optimization.chromosome as test

# Set Schedule Activity
schedule_info = ScheduleInformation()

work_type_info_1 = {'id': 'Electrical_Work', 'manhour': '345'}
work_type_info_2 = {'id': 'Plumbing_Work', 'manhour': '127'}
work_type_info_3 = {'id': 'Tile_Work', 'manhour': '390'}
work_type_info_4 = {'id': 'Pannel_Work', 'manhour': '127'}
work_type_info_5 = {'id': 'Finishing Work', 'manhour': '448'}
work_type_info_6 = {'id': 'Equip_Installation', 'manhour': '256'}
work_type_info_7 = {'id': 'Panel Joints', 'manhour': '96'}
work_type_info_list = [work_type_info_1, work_type_info_2, work_type_info_3, work_type_info_4,
                       work_type_info_5, work_type_info_6, work_type_info_7]

for idx, work_type_info in enumerate(work_type_info_list):
    work_type = WorkType(idx + 1, **work_type_info)
    schedule_info.add_work_type(work_type)

# Set Initial Parameter
schedule_info.unit_install_time = 30
schedule_info.num_unit_in_floor = 8
schedule_info.num_floor = 4
schedule_info.floor_buffer = 1

# Set optimized value
# schedule_info.modular_unit_rate = 4
# schedule_info.unit_arrived_interval = 60

num_work_type = schedule_info.num_work_type()
num_total_unit = schedule_info.total_unit

labor_content = {'num': num_work_type, 'min': 1, 'max': 4, 'digit': 2, 'offspring': -1}
unit_in_group_content = {'num': num_work_type, 'min': 1, 'max': 4, 'digit': 2, 'offspring': -1}
modular_unit_rate_content = {'num': 1, 'min': 1, 'max': num_total_unit, 'digit': 5, 'offspring': -1}
unit_arrived_interval_content = {'num': 1, 'min': 128, 'max': 255, 'digit': 7, 'offspring': -128}
# num of value of each content, min value of each content, max_value of each content, num_digit of each content
geno_shape = {'num_labor': labor_content, 'num_unit_in_group': unit_in_group_content,
              'unit_rate': modular_unit_rate_content, 'unit_arrived_interval': unit_arrived_interval_content}

BinaryChromosome.set_geno_shape(**geno_shape)
gene_list = BinaryChromosome.get_random_chromosome_from_geno_shape(10)
work_type_list = list(schedule_info.work_type_dict.values())

cpm = CPM()


# for chromosome in gene_list:
#     print(BinaryChromosome.get_phenotype_element(chromosome, 'num_labor', 0))



def test_function(chro_str):
    num_labor_key = 'num_labor'
    for idx, work_type in enumerate(work_type_list):
        value = BinaryChromosome.get_phenotype_element(chro_str, num_labor_key, idx)
        work_type.num_labor = value

    num_unit_in_group_key = 'num_unit_in_group'
    for idx, work_type in enumerate(work_type_list):
        value = BinaryChromosome.get_phenotype_element(chro_str, num_unit_in_group_key, idx)
        work_type.num_unit_in_group = value

    unit_arrived_key = 'unit_arrived_interval'
    value = BinaryChromosome.get_phenotype_element(chro_str, unit_arrived_key, 0)
    schedule_info.modular_unit_rate = value

    unit_rate_key = 'unit_rate'
    value = BinaryChromosome.get_phenotype_element(chro_str, unit_rate_key, 0)
    schedule_info.unit_arrived_interval = value
    schedule = schedule_info.to_schedule()
    cpm.compute_critical_path(schedule)

    return np.array([cpm._make_span, schedule_info.total_num_labor()])

test_function(gene_list[0])
schedule = schedule_info.to_schedule()
print(cpm._make_span)
test_function(gene_list[1])
print(cpm._make_span)
exit()
# def test_function_2(chro_str):


# schedule = schedule_info.to_schedule()
# cpmExample = CPM()
# cpmExample.compute_critical_path(schedule)
# schedule.print_dependency_list()

#
generic_parameter_dict = {
    MultiObjGenericEnum.SUPERIOR: 0.2,
    MultiObjGenericEnum.ONE_POINT_CROSSOVER: 0.4,
    MultiObjGenericEnum.LOCAL_MUTATION: 0.2,
    MultiObjGenericEnum.GLOBAL_MUTATION: 0.2
}


multi_objective = MultiObjectiveGenerator(test_function, generic_parameter_dict)
multi_objective.local_algorithm_enum = BinaryLocalAlgorithm.LK

p = ParetoOptimizer(multi_objective, generic_parameter_dict)
p.setting(
    num_chromosome_in_generation=20,
    max_generation=10,
    num_objective=2
)

p.optimize()
