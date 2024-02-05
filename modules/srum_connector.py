# -*- coding: utf-8 -*-
"""module for SRUM."""
import os
import subprocess
from pytz import timezone

import xlrd
import openpyxl
import pandas

from modules import manager
from modules import interface
from modules import logger
from modules.windows_srum import srum_dump2
from modules.windows_srum import sru2usage


class SRUMConnector(interface.ModuleConnector):

    NAME = 'srum_connector'
    DESCRIPTION = 'Module for Srum'

    _plugin_classes = {}

    def __init__(self):
        super(SRUMConnector, self).__init__()

    def Connect(self, par_id, configuration, source_path_spec, knowledge_base):

        query_separator = self.GetQuerySeparator(source_path_spec, configuration)
        path_separator = self.GetPathSeparator(source_path_spec)
        this_file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'schema' + os.sep

        yaml_list = [this_file_path + 'lv1_os_win_srum_application_resource_usage.yaml',
                     this_file_path + 'lv1_os_win_srum_unknown1.yaml']

        table_list = ['lv1_os_win_srum_application_resource_usage',
                      'lv1_os_win_srum_unknown1']

        if not self.check_table_from_yaml(configuration, yaml_list, table_list):
            return False

        query = f"SELECT name, parent_path, extension FROM file_info WHERE (par_id='{par_id}' " \
                f"and name like 'SRUDB.dat' and parent_path like '%Windows{query_separator}System32{query_separator}sru');"

        srum_file = configuration.cursor.execute_query_mul(query)

        if len(srum_file) == 0:
            print("There are no srum files.")
            return False

        srum_path = srum_file[0][1][srum_file[0][1].find(path_separator):] + path_separator + srum_file[0][0]
        file_name = srum_file[0][0]
        output_path = configuration.root_tmp_path + os.sep + configuration.case_id + os.sep + configuration.evidence_id + os.sep + par_id

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # self.ExtractTargetFileToPath(
        #     source_path_spec=source_path_spec,
        #     configuration=configuration,
        #     file_path=srum_path,
        #     output_path=output_path)

        srum_dump2.main(output_path + os.sep + file_name, output_path + os.sep + 'result.xlsx')

        xlsx_unknown1 = pandas.read_excel(output_path + os.sep + 'result.xlsx', sheet_name='Unknown1')
        xlsx_unknown1 = pandas.DataFrame(xlsx_unknown1, columns=["Srum ID Number","Srum Entry Creation","Application","User SID","EndTime","Cycles","InFocusS","UserInputS","AudioInS","AudioOutS","KeyboardInputS","MouseInputS"])
        xlsx_application_resource_usage = pandas.read_excel(output_path + os.sep + 'result.xlsx', sheet_name='Application Resource Usage')
        xlsx_application_resource_usage = pandas.DataFrame(xlsx_application_resource_usage, columns=["Srum ID Number","Srum Entry Creation","Application","CPU time in Forground","FaceTime"])
        insert_unknown1 = []
        for i in xlsx_unknown1.index:
            insert_unknown1.append([par_id, configuration.case_id, configuration.evidence_id, str(xlsx_unknown1.at[i, "Srum ID Number"]),
            str(xlsx_unknown1.at[i, "Srum Entry Creation"]), str(xlsx_unknown1.at[i, "Application"]), str(xlsx_unknown1.at[i, "User SID"]), str(xlsx_unknown1.at[i, "EndTime"]),
            str(xlsx_unknown1.at[i, "Cycles"]), str(xlsx_unknown1.at[i, "InFocusS"]), str(xlsx_unknown1.at[i, "UserInputS"]), str(xlsx_unknown1.at[i, "AudioInS"]),
            str(xlsx_unknown1.at[i, "AudioOutS"]), str(xlsx_unknown1.at[i, "KeyboardInputS"]), str(xlsx_unknown1.at[i, "MouseInputS"])])

        insert_application_resource_usage = []
        for i in xlsx_application_resource_usage.index:
            insert_application_resource_usage.append(
                [par_id, configuration.case_id, configuration.evidence_id, str(xlsx_application_resource_usage.at[i, "Srum ID Number"]),
                 str(xlsx_application_resource_usage.at[i, "Srum Entry Creation"]), str(xlsx_application_resource_usage.at[i, "Application"]),
                 str(xlsx_application_resource_usage.at[i, "CPU time in Forground"]),
                 str(xlsx_application_resource_usage.at[i, "FaceTime"])])

        query = "Insert into lv1_os_win_srum_unknown1 " \
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        configuration.cursor.bulk_execute(query, insert_unknown1)

        query = "Insert into lv1_os_win_srum_application_resource_usage " \
                "values (%s, %s, %s, %s, %s, %s, %s, %s);"
        configuration.cursor.bulk_execute(query, insert_application_resource_usage)

        sru2usage.main(output_path + os.sep + 'result.xlsx', output_path + os.sep + 'srum.db', output_path + os.sep + 'graph.html', 9)  # 9 UTC 시간을 넣어줘야함


manager.ModulesManager.RegisterModule(SRUMConnector)
