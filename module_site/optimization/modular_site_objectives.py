from enum import Enum
from module_site.core.component import Schedule


class ObjEnum(Enum):
    DURATION = 0
    NUM_LABOR = 1


class OrderEnum(Enum):
    MAX = 1
    MIN = -1


def call_objective_function(idx):
    def get_duration(schedule, extrema):
        return

    def get_num_labor(schedule, extrema):
        return

    objective_function_list ={
        ObjEnum.DURATION: get_duration,
        ObjEnum.NUM_LABOR: get_num_labor
    }

    return objective_function_list.get(idx)