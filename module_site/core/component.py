import pandas as pd
import math
from enum import Enum


class WorkType(object):
    def __init__(self, order, **info):
        # id can't be 'unit_arrived' and 'unit_installation'
        self.order = order
        self.id = info.get('id')
        self.manhour = int(str(info.get('manhour')))
        try:
            self.values = {
                'num_labor': int(info.get('num_labor')),
                'num_unit_in_group': int(info.get('num_unit_in_group'))
            }
        except TypeError:
            self.values = {
                'num_labor': 1,
                'num_unit_in_group': 1
            }

    def __str__(self):
        return str(self.order) + ' '+ str(self.id) + ' ' + str(self.manhour) + \
               ' ' + str(self.num_labor) + ' ' + str(self.num_unit_in_group)

    @property
    def num_unit_in_group(self):
        return self.values['num_unit_in_group']

    @num_unit_in_group.setter
    def num_unit_in_group(self, num_unit_in_group):
        self.values['num_unit_in_group'] = num_unit_in_group

    @property
    def num_labor(self):
        return self.values['num_labor']

    @num_labor.setter
    def num_labor(self, num_labor):
        self.values['num_labor'] = num_labor

    def get_duration(self):
        if self.id == 'unit_arrived':
            return 0
        elif self.id == 'unit_installation':
            print('unit_installation work_type cannot use this function')
            exit()
            return 0
        else:
            return math.ceil((self.num_unit_in_group * self.manhour) / (self.num_labor * self.num_unit_in_group))

    def get_num_group(self, total_unit):
        return math.ceil(total_unit / self.num_unit_in_group)


dict_installation = {
    'id': 'unit_installation',
    'order': -1,
    'manhour': 0
}

dict_arrived = {
    'order': -2,
    'id': 'unit_arrived',
    'manhour': 0
}

dict_floor_buffer = {
    'order': 0,
    'id': 'floor_buffer',
    'manhour': 0
}

dict_arrived_interval = {
    'order': -3,
    'id': 'arrived_interval',
    'manhour': 0
}


class BasicWorkType(Enum):
    UNIT_INSTALLATION = dict_installation
    UNIT_ARRIVED = dict_arrived
    FLOOR_BUFFER = dict_floor_buffer
    ARRIVED_INTERVAL = dict_arrived_interval


work_type_installation = WorkType(**dict_installation)
work_type_arrived = WorkType(**dict_arrived)
work_type_floor_buffer = WorkType(**dict_floor_buffer)
work_type_arrived_interval = WorkType(**dict_arrived_interval)


class Activity(object):
    def __init__(self, work_type, idx):
        self.__work_type = work_type
        self.__idx = idx
        self.allocated_module_list = []
        self.__id = work_type.id + str(idx)
        self.__duration = 0
        self.cpm_value_dict = {}

    def __str__(self):
        return str(self.__work_type.id) + str(self.__idx) + " " + str(self.allocated_module_list)

    def cpm_info(self):
        return self.__id + " "+ str(self.cpm_value_dict) + " " + str(self.duration)

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration

    @property
    def work_type(self):
        return self.__work_type

    @property
    def id(self):
        return self.__id

    @property
    def idx(self):
        return self.__idx

    def allocate_module(self, module_idx_list):
        self.allocated_module_list = module_idx_list

    @property
    def order(self):
        return self.__work_type.order


class ScheduleInformation(object):
    def __init__(self):
        self.work_type_dict = {}
        self.__modular_unit_rate = 0
        self.__unit_arrived_interval = 0
        self.__unit_install_time = 0
        self.__num_unit_in_floor = 0
        self.__num_floor = 0
        self.__floor_buffer = 0

    @property
    def unit_arrived_interval(self):
        return self.__unit_arrived_interval

    @unit_arrived_interval.setter
    def unit_arrived_interval(self, unit_arrived_interval):
        self.__unit_arrived_interval = unit_arrived_interval

    @property
    def floor_buffer(self):
        return self.__floor_buffer

    @floor_buffer.setter
    def floor_buffer(self, floor_buffer):
        if floor_buffer > 0:
            self.__floor_buffer = floor_buffer
        else:
            print('floor buffer have to positive value')
            exit()
            return

    @property
    def num_unit_in_floor(self):
        return self.__num_unit_in_floor

    @num_unit_in_floor.setter
    def num_unit_in_floor(self, num_unit_in_floor):
        self.__num_unit_in_floor = num_unit_in_floor
        self.__total_unit = self.__num_floor * self.__num_unit_in_floor

    @property
    def num_floor(self):
        return self.__num_floor

    @num_floor.setter
    def num_floor(self, num_floor):
        self.__num_floor = num_floor
        self.__total_unit = self.__num_floor * self.__num_unit_in_floor

    @property
    def modular_unit_rate(self):
        return self.__modular_unit_rate

    @modular_unit_rate.setter
    def modular_unit_rate(self, modular_unit_rate):
        self.__modular_unit_rate = modular_unit_rate

    @property
    def total_unit(self):
        return self.__num_unit_in_floor * self.__num_floor

    @property
    def unit_install_time(self):
        return self.__unit_install_time

    @unit_install_time.setter
    def unit_install_time(self, unit_install_time):
        self.__unit_install_time = unit_install_time

    def total_num_labor(self):
        sum = 0
        for work_type in self.work_type_dict.values():
            sum += work_type.num_labor
        return sum

    def num_work_type(self):
        return len(self.work_type_dict)

    def get_work_type_from_file(self, filename):
        work_types = pd.read_csv(filename)
        for order, type_info in work_types.iterrows():
            work_type = WorkType(order + 1, **type_info.to_dict())
            self.work_type_dict[work_type.id] = work_type

    def add_work_type(self, work_type):
        self.work_type_dict[work_type.id]= work_type

    def print(self):
        for work_type in self.work_type_dict.values():
            print(work_type)

    def to_schedule(self):
        schedule = Schedule()
        schedule.floor_buffer = self.__floor_buffer
        schedule.num_unit_in_floor = self.__num_unit_in_floor
        schedule.unit_arrived_interval = self.__unit_arrived_interval
        self.__unit_to_activity(schedule)
        self.__floor_to_activity(schedule)
        self.__work_type_to_activity(schedule)
        schedule.set_dependency_list()
        return schedule

    def get_unit_arrived_idx(self):
        return math.ceil(self.__total_unit / self.__modular_unit_rate)

    def __unit_to_activity(self, schedule):
        total_arrived_idx = self.get_unit_arrived_idx()
        # arrived
        for arrived_idx in range(0, total_arrived_idx):
            key = (work_type_arrived.id, arrived_idx)
            act = Activity(work_type_arrived, arrived_idx)
            for unit_idx in range(0, self.__modular_unit_rate):
                idx = arrived_idx * self.__modular_unit_rate + unit_idx
                if self.total_unit > idx:
                    act.allocated_module_list.append(idx)
            act.duration = 0
            schedule.activity_dict[key] = act

        # arrived_interval
        for arrived_idx in range(1, total_arrived_idx):
            key = (work_type_arrived_interval.id, arrived_idx)
            act = Activity(work_type_arrived_interval, arrived_idx)
            for unit_idx in range(0, self.__modular_unit_rate):
                idx = arrived_idx * self.__modular_unit_rate + unit_idx
                if self.total_unit > idx:
                    act.allocated_module_list.append(idx)
            act.duration = self.__unit_arrived_interval
            schedule.activity_dict[key] = act

        # unit_installation
        for idx in range(0, self.__total_unit):
            key = (work_type_installation.id, idx)
            act = Activity(work_type_installation, idx)
            act.allocated_module_list.append(idx)
            act.duration = self.unit_install_time
            schedule.activity_dict[key] = act

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
                # print(work_type.id, work_type.num_labor, work_type.num_unit_in_group)
                act.duration = work_type.get_duration()
                schedule.activity_dict[key] = act

    def __floor_to_activity(self, schedule):
        for floor_idx in range(0, self.__num_floor):
            key = (work_type_floor_buffer.id, floor_idx)
            act = Activity(work_type_floor_buffer, floor_idx)
            for unit_idx in range(0, self.__num_unit_in_floor):
                idx = unit_idx + floor_idx * self.__num_unit_in_floor
                act.allocated_module_list.append(idx)
            act.duration = 0
            schedule.activity_dict[key] = act


class Schedule(object):
    def __init__(self):
        self.work_type_list = [work_type_arrived.id, work_type_installation.id]
        self.activity_dict = {}
        self.dependency_list = []
        self.floor_buffer = 0
        self.num_unit_in_floor = 0
        self.unit_arrived_interval = 0
        self.project_duration = 0

    def get_activity_list_with_work_type(self, work_type_idx):
        activity_list = []
        for key, value in self.activity_dict.items():
            if key[0] == work_type_idx:
                activity_list.append(value)
        return activity_list

    def get_activity_list_with_order(self, order):
        activity_list = []
        for act in self.activity_dict.values():
            if act.order == order:
                activity_list.append(act)
        return activity_list

    def set_dependency_list(self):
        self.dependency_list.clear()
        for act in self.activity_dict.values():
            self.dependency_list += self.__find_predecessors_of_activity(act)

    def print_dependency_list(self, pre_id=None, suc_id=None):
        for pre_act, act in self.dependency_list:
            if pre_id == None and suc_id == None:
                print(pre_act, act)
            if pre_id != None and suc_id == None:
                if pre_act.id == pre_id:
                    print(pre_act, act)
            if pre_id == None and suc_id != None:
                if act.id == suc_id:
                    print(pre_act, act)

    def __find_predecessors_of_activity(self, activity):
        predecessor_list = []
        self.__find_same_type_predecessor(activity, predecessor_list)
        self.__find_arrived_interval_predecessor(activity, predecessor_list)
        self.__find_other_type_predecessor(activity, predecessor_list)
        self.__find_floor_predecessor(activity, predecessor_list)
        return predecessor_list

    def __find_arrived_interval_predecessor(self, activity, predecessor_list):
        arrived_Interval_order = BasicWorkType.ARRIVED_INTERVAL.value['order']
        exist, predecessor = activity.order == arrived_Interval_order, None
        if exist:
            predecessor_key = (dict_arrived['id'], activity.idx - 1)
            successor_key = (dict_arrived['id'], activity.idx)
            predecessor = self.activity_dict[predecessor_key]
            successor = self.activity_dict[successor_key]
            predecessor_list.append((predecessor, activity))
            predecessor_list.append((activity, successor))
        return exist

    def __find_same_type_predecessor(self, activity, predecessor_list):
        arrived_Interval_order = BasicWorkType.ARRIVED_INTERVAL.value['order']
        exist, predecessor = activity.idx != 0 and activity.order != arrived_Interval_order, None
        if exist:
            predecessor_key = (activity.work_type.id, activity.idx - 1)
            predecessor = self.activity_dict[predecessor_key]
            predecessor_list.append((predecessor, activity))
        return exist

    def __find_floor_predecessor(self, activity, predecessor_list):
        unit_arrived_order = BasicWorkType.UNIT_ARRIVED.value['order']
        exist, predecessor = activity.order == unit_arrived_order, None
        last_unit = activity.allocated_module_list[-1]
        required_unit = last_unit + self.floor_buffer * self.num_unit_in_floor
        if exist:
            floor_constraint = False
            floor_buffer_order = BasicWorkType.FLOOR_BUFFER.value['order']
            floor_activity_list = self.get_activity_list_with_order(floor_buffer_order)
            for floor_act in reversed(floor_activity_list):
                if required_unit in floor_act.allocated_module_list:
                    predecessor = floor_act
                    predecessor_list.append((predecessor, activity))
                    floor_constraint = True
                    break

        if exist and floor_constraint is True and predecessor is None:
            print('find floor type predecessor logic is wrong')
            exit()
        return exist

    def __find_other_type_predecessor(self, activity, predecessor_list):
        floor_buffer_order = BasicWorkType.FLOOR_BUFFER.value['order']
        exist, predecessor = activity.order > 0 or activity.order == floor_buffer_order, None
        last_unit = activity.allocated_module_list[-1]
        if exist:
            other_type_list = self.get_activity_list_with_order(activity.order - 1)
            for pre_work_type_act in other_type_list:
                if last_unit in pre_work_type_act.allocated_module_list:
                    predecessor = pre_work_type_act
                    predecessor_list.append((predecessor, activity))
                    break
        if exist is True and predecessor is None:
            print('find other type predecessor logic is wrong')
            exit()
        return exist


class WorkTypeNameException(Exception):
    def __init__(self):
        pass