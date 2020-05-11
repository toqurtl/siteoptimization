from module_site.core.component import ScheduleInformation



schedule_info = ScheduleInformation()
schedule_info.get_work_type_from_file('sample_data/sample.csv')
schedule_info.total_unit = 13
schedule_info.modular_unit_rate = 2
schedule_info.unit_install_time = 30
schedule = schedule_info.to_schedule()
for key, act in schedule.activity_map.items():
    print(key, act.allocated_module_list)