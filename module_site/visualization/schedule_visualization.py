import win32com.client
import time
from pandas import DataFrame, ExcelWriter


print_info_list = ['work_type', 'idx', 'duration', 'units', 'ES', 'EF']


def schedule_to_pandas(schedule):
    row_list = []
    for key, act in schedule.activity_dict.items():
        work_type, idx = key
        ES, EF = act.cpm_value_dict['ES'], act.cpm_value_dict['EF']
        row_list.append([work_type, idx, act.duration, act.allocated_module_list, ES, EF])
    return DataFrame(row_list, columns=print_info_list)


# filename have to be absolute path
def schedule_to_excel(schedule, filename):
    df = schedule_to_pandas(schedule)
    with ExcelWriter(filename) as writer:
        df.to_excel(
            excel_writer=writer, sheet_name='result', header=True, index=False
        )
    time.sleep(1)
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    wb = excel.Workbooks.Open(filename)
    ws = wb.ActiveSheet
    for column_idx in range(len(print_info_list) + 1, schedule.project_duration + len(print_info_list) + 1):
        column = ws.Columns(column_idx)
        column.ColumnWidth = 0.08

    for idx, act in enumerate(list(schedule.activity_dict.values())):
        row = idx + 2
        ES = act.cpm_value_dict['ES']
        EF = act.cpm_value_dict['EF']
        if ES == EF:
            column_idx = ES + len(print_info_list) + 1
            ws.Cells(row, column_idx).Interior.ColorIndex = 37
        else:
            for column_idx in range(ES + len(print_info_list) + 1, EF + len(print_info_list) + 1):
                ws.Cells(row, column_idx).Interior.ColorIndex = 37
