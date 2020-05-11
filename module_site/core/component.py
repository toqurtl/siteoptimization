import pandas as pd
import math


class WorkType(object):
    def __init__(self, order, **info):
        # id can't be 'unit_arrived' and 'unit_installation'
        self.order = order + 2
        self.id = info.get('id')
        try:
            self.manhour = int(info.get('manhour'))
            self.num_labor = int(info.get('num_labor'))
            self.num_unit_in_group = int(info.get('num_unit_in_group'))
            self.productivity = int(info.get('productivity'))
        except TypeError:
            pass

    def get_duration(self):
        return (self.num_unit * self.manhour) / (self.num_labor * self.productivity)

    def get_num_group(self, total_unit):
        return math.ceil(total_unit / self.num_unit_in_group)


dict_installation = {
    'id': 'unit_installation',
    'order': 1,
}

dict_arrived ={
    'order': 0,
    'id': 'unit_arrived'
}

work_type_installation = WorkType(**dict_installation)
work_type_arrived = WorkType(**dict_arrived)


class Activity(object):
    def __init__(self, work_type, idx):
        self.__work_type = work_type
        self.__idx = idx
        self.allocated_module_list = []

    @property
    def work_type(self):
        return self.__work_type

    @property
    def idx(self):
        return self.__idx

    def allocate_module(self, module_idx_list):
        self.allocated_module_list = module_idx_list


class ScheduleInformation(object):
    def __init__(self):
        self.work_type_dict = {}
        self.__total_unit = 0
        self.__modular_unit_rate = 0
        self.__unit_install_time = 0

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

    @property
    def unit_install_time(self):
        return self.__unit_install_time

    @unit_install_time.setter
    def unit_install_time(self, unit_install_time):
        self.__unit_install_time = unit_install_time

    def get_work_type_from_file(self, filename):
        work_types = pd.read_csv(filename)
        for order, type_info in work_types.iterrows():
            work_type = WorkType(order, **type_info.to_dict())
            self.work_type_dict[work_type.id] = work_type

    def to_schedule(self):
        schedule = Schedule()
        self.__unit_to_activity(schedule)
        self.__work_type_to_activity(schedule)
        self.__set_dependency()
        return schedule

    def get_unit_arrived_idx(self):
        return math.ceil(self.__total_unit / self.__modular_unit_rate)

    def __unit_to_activity(self, schedule):
        total_arrived_idx = self.get_unit_arrived_idx()
        for arrived_idx in range(0, total_arrived_idx):
            key = (work_type_arrived.id, arrived_idx)
            act = Activity(work_type_arrived, arrived_idx)
            for unit_idx in range(0, self.__modular_unit_rate):
                idx = arrived_idx * self.__modular_unit_rate + unit_idx
                if self.total_unit > idx:
                    act.allocated_module_list.append(idx)
            schedule.activity_map[key] = act

        for idx in range(0, self.__total_unit):
            key = (work_type_installation.id, idx)
            act = Activity(work_type_installation, idx)
            act.allocated_module_list.append(idx)
            schedule.activity_map[key] = act

    def __work_type_to_activity(self, schedule):
        for work_type_idx, work_type in self.work_type_dict.items():
            num_group = work_type.get_num_group(self.__total_unit)
            schedule.work_type_list.append(work_type_idx)
            for group_idx in range(0, num_group):
                act = Activity(work_type, group_idx)
                key = (work_type.id, group_idx)
                for unit_idx in range(0, work_type.num_unit_in_group):
                    idx = unit_idx + work_type.num_unit_in_group * group_idx
                    if self.total_unit > idx:
                        act.allocated_module_list.append(idx)
                schedule.activity_map[key] = act


    def __set_dependency(self):
        pass


class Schedule(object):
    def __init__(self):
        self.work_type_list = [work_type_arrived.id, work_type_installation.id]
        self.activity_map = {}
        self.dependency_list = []

    def __set_dependency(self):
        pass

    def get_activity_list_with_work_type(self, work_type_idx):
        activity_list = []
        for key, value in self.activity_map.items():
            if key[0] == work_type_idx:
                activity_list.append(value)
        return activity_list


class WorkTypeNameException(Exception):
    def __init__(self):
        pass