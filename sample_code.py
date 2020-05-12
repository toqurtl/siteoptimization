from module_site.core.component import ScheduleInformation
from module_site.core.cpm import CPM
import networkx as nx

schedule_info = ScheduleInformation()
schedule_info.get_work_type_from_file('sample_data/sample.csv')
schedule_info.modular_unit_rate = 4
schedule_info.unit_install_time = 30
schedule_info.num_unit_in_floor = 4
schedule_info.num_floor = 10
schedule_info.floor_buffer = 2
schedule = schedule_info.to_schedule()

cpmExample = CPM()
cpmExample.compute_critical_path(schedule)
floor_list = schedule.get_activity_list_with_work_type('floor_buffer')

schedule.print_dependency_list()

print(cpmExample._make_span)