# # -*- coding: utf-8 -*-
# """module for LV2."""
# import os, sys, dateutil, hashlib, struct
# from datetime import datetime
# from multiprocessing import Pool
#
# from advanced_modules import manager
# from advanced_modules import interface
# from advanced_modules import logger
# from dfvfs.lib import definitions as dfvfs_definitions
#
# from advanced_modules.ai.ai_image_based_document_layout_similarity_analyzer import create_representive_image
#
# class LV2AiImagebasedDocumentLayoutSimilarityAnalyzer(interface.AdvancedModuleAnalyzer):
#     NAME = 'lv2_ai_image_based_document_layout_similarity_analyzer'
#     DESCRIPTION = 'Module for LV2 Image-based Document Layout Similarity Analyzer'
#
#     def __init__(self):
#         super(LV2AiImagebasedDocumentLayoutSimilarityAnalyzer, self).__init__()
#
#     def Analyze(self, par_id, configuration, source_path_spec, knowledge_base):
#
#         this_file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'schema' + os.sep
#         # 모든 yaml 파일 리스트
#         yaml_list = [this_file_path + 'lv2_ai_image_based_document_layout_similarity.yaml']
#
#         # 모든 테이블 리스트
#         table_list = ['lv2_ai_image_based_document_layout_similarity']
#
#         if not self.check_table_from_yaml(configuration, yaml_list, table_list):
#             return False
#
#         path_separator = self.GetPathSeparator(source_path_spec)
#
#         # 대표 이미지 생성을 위해 모든 문서 추출 ( xls, xlsx 제외 )
#         query = f"SELECT name, parent_path, extension, ctime, ctime_nano, inode " \
#                 f"FROM file_info WHERE par_id='{par_id}' AND (LOWER(extension)='hwp' OR LOWER(extension)='pdf' OR LOWER(extension)='ppt' OR LOWER(extension)='pptx' OR LOWER(extension)='doc' OR LOWER(extension)='docx');"
#         results = configuration.cursor.execute_query_mul(query)
#
#         # 만약 이미지 파일이 입력된다면 빠르게 파일 추출을 위함
#         if configuration.source_type == 'storage media device' or configuration.source_type == 'storage media image':
#             tsk_file_system = self.get_tsk_file_system(source_path_spec, configuration)
#
#         # document_list = list()
#         # for document in results:
#         #
#         #     file_name = document[0]
#         #     file_path = document[1]
#         #     document_path = file_path + path_separator + file_name
#         #     path_md5 = hashlib.md5(document_path.encode('UTF-8')).hexdigest()
#         #
#         #     output_path = configuration.root_tmp_path + os.path.sep + configuration.case_id \
#         #                   + os.path.sep + configuration.evidence_id + os.path.sep + par_id + os.path.sep + 'ai_image_based_document_layout_similarity_analyzer'
#         #
#         #     if not os.path.exists(output_path):
#         #         os.mkdir(output_path)
#         #
#         #     if not os.path.exists(output_path + os.path.sep + path_md5):
#         #         os.mkdir(output_path + os.path.sep + path_md5)
#         #
#         #     if configuration.source_type == 'storage media device' or configuration.source_type == 'storage media image':
#         #         self.extract_file_to_path(tsk_file_system=tsk_file_system,
#         #                                   inode=int(document[5]),
#         #                                   file_name=file_name,
#         #                                   output_path=output_path + os.path.sep + path_md5)
#         #     elif configuration.source_type == 'directory' or configuration.source_type == 'file':
#         #         self.ExtractTargetFileToPath(
#         #             source_path_spec=source_path_spec,
#         #             configuration=configuration,
#         #             file_path=file_name,
#         #             output_path=output_path + os.path.sep + path_md5)
#         #
#         #     document_list.append([par_id, configuration.case_id, configuration.evidence_id, len(document_list), path_md5, file_name, file_path, output_path])
#         #
#         # query = "Insert into lv2_ai_image_based_document_layout_similarity values (%s, %s, %s, %s, %s, %s, %s, %s);"
#         # configuration.cursor.bulk_execute(query, document_list)
#
#         query = f"SELECT count, path_md5, file_name, file_path, output_path " \
#                 f"FROM lv2_ai_image_based_document_layout_similarity;"
#         document_list = configuration.cursor.execute_query_mul(query)
#         hash_list = list()
#
#         # # ### 대표 이미지 생성
#         # pool = Pool(processes=8)
#         #
#         # # 작업을 Pool에 매핑하여 병렬 처리
#         # hash_list.append(pool.map(create_representive_image, document_list))
#         #
#         # pool.close()
#         # pool.join()
#
#         # # 단일 테스트
#         # hash_list.append(create_representive_image(document_list[69]))    # 암호화
#         # hash_list.append(create_representive_image(document_list[16496]))   # 글꼴? 아닌데 잘되는데
#
#         # # 다중 테스트
#         # for i in range(0, len(document_list)):
#         #     hash_list.append(create_representive_image(document_list[i]))
#
#         # 속도 업 테스트
#         hash_list = create_representive_image(document_list)
#
#         print(hash_list)
#         pass
#
#
#
#
#
# manager.AdvancedModulesManager.RegisterModule(LV2AiImagebasedDocumentLayoutSimilarityAnalyzer)