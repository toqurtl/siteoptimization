import numpy as np
from module_site.optimization.chromosome import BinaryChromosome
from module_site.optimization.generic import BinaryGeneric, BinaryLocalAlgorithm
from module_site.optimization.generation import Fronting, MultiObjectiveGenerator, MultiObjGenericEnum
from module_site.optimization.optimizer import ParetoOptimizer
from module_site.core.component import ScheduleInformation
from module_site.core.cpm import CPM
import time

schedule_info = ScheduleInformation()
schedule_info.get_work_type_from_file('../sample_data/sample_2.csv')
schedule_info.modular_unit_rate = 4
schedule_info.unit_install_time = 30
schedule_info.num_unit_in_floor = 10
schedule_info.num_floor = 4
schedule_info.floor_buffer = 1
schedule_info.unit_arrived_interval = 60

content_1 = {'num': 6, 'min': 1, 'max': 4, 'digit': 3 }
content_2 = {'num': 6, 'min': 1, 'max': 40, 'digit': 6 }
content_3 = {'num': 1, 'min': 1, 'max': 40, 'digit': 6 }
# num of value of each content, min value of each content, max_value of each content, num_digit of each content
geno_shape = {'num_labor': content_1, 'num_unit_in_group': content_2, 'unit_arrived': content_3 }

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
p.setting(
    num_chromosome_in_generation=100,
    max_generation=10,
    num_objective=2
)
a = time.time()

p.optimize()
