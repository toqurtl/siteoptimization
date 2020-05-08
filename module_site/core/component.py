import pandas as pd
import math


class WorkType(object):
    def __init__(self, **info):
        self.id = info.get('id')
        self.manhour = info.get('manhour')
        self.num_labor = info.get('num_labor')
        self.num_unit = info.get('num_unit')
        self.productivity = info.get('productivity')

    def get_duration(self):
        return (self.num_unit * self.manhour) / (self.num_labor * self.productivity)

    def get_num_activity(self, total_unit):
        return math.ceil(total_unit / self.num_unit)


class Activity(object):
    def __init__(self, work_type, idx):
        self.__work_type = work_type
        self.__idx = idx
        self.allocated_module_list = []

    @property
    def work_type(self):
        return self.__work_type

    def allocate_module(self, module_idx_list):
        self.allocated_module_list = module_idx_list


class ScheduleInformation(object):
    def __init__(self):
        self.work_type_dict = {}
        self.__total_unit = 0
        self.__modular_unit_rate = 0

    @property
    def modular_unit_rate(self):
        return self.__modular_unit_rate

    @modular_unit_rate.setter
    def modular_unit_rate(self, modular_unit_rate):
        self.__modular_unit_rate = modular_unit_rate

    @property
    def total_unit(self):
        return self.__total_unit

    @total_unit.setter
    def total_unit(self, total_unit):
        self.__total_unit = total_unit

    def get_work_type_from_file(self, filename):
        work_types = pd.read_csv(filename)
        for _, type_info in work_types.iterrows():
            type = WorkType(**type_info.to_dict())
            self.activity_dict[type.id] = type

    def to_schedule(self):
        for work_type_idx, work_type in self.work_type_dict.items():



class Schedule(object):
    def __init__(self):
        self.activity_list = [[]]

    def get_activity_list_with_work_type(self, work_type_idx):
        return