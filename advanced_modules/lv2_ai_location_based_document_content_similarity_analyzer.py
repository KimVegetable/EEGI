# # -*- coding: utf-8 -*-
# """module for LV2."""
# import os, sys, dateutil
# from datetime import datetime
#
# from advanced_modules import manager
# from advanced_modules import interface
# from advanced_modules import logger
# from dfvfs.lib import definitions as dfvfs_definitions
#
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
#
# class LV2AiLocationbasedDocumentContentSimilarityAnalyzer(interface.AdvancedModuleAnalyzer):
#     NAME = 'lv2_ai_location_based_document_content_similarity_analyzer'
#     DESCRIPTION = 'Module for LV2 Location-based Document Content Similarity Analyzer'
#
#     def __init__(self):
#         super(LV2AiLocationbasedDocumentContentSimilarityAnalyzer, self).__init__()
#
#     def Analyze(self, par_id, configuration, source_path_spec, knowledge_base):
#
#         this_file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'schema' + os.sep
#         # 모든 yaml 파일 리스트
#         yaml_list = [this_file_path + 'lv2_ai_location_based_document_content_similarity.yaml']
#
#         # 모든 테이블 리스트
#         table_list = ['lv2_ai_location_based_document_content_similarity']
#
#         if not self.check_table_from_yaml(configuration, yaml_list, table_list):
#             return False
#
#         # 문서 데이터 추출
#         query = f"SELECT parent_full_path, name, content " \
#                 f"FROM lv1_file_document WHERE par_id='{par_id}';"
#         results = configuration.cursor.execute_query_mul(query)
#
#         contents = list()
#         for result in results:
#             contents.append(result[2])
#         tfidf_vectorizer = TfidfVectorizer()
#
#         tfidf_matrix = tfidf_vectorizer.fit_transform(contents)
#         tfidf_norm_l1 = self.l1_normalize(tfidf_matrix)
#         similarity_list = list()
#
#         for i in range(0, 12962):
#             similarity_list.append([i, cosine_similarity(tfidf_matrix[8857], tfidf_matrix[i])[0][0], euclidean_distances(tfidf_norm_l1[8967], tfidf_norm_l1[i])[0][0], manhattan_distances(tfidf_norm_l1[8967], tfidf_norm_l1[i])[0][0], results[i][0], results[i][1]])
#
#         df = pd.DataFrame(similarity_list)
#         df.to_excel(datetime.now().strftime("%H-%M-%S") + '.xlsx', index=False, header=False)
#
#     def l1_normalize(self, v):
#         norm = np.sum(v)
#         return v / norm
#
#
# manager.AdvancedModulesManager.RegisterModule(LV2AiLocationbasedDocumentContentSimilarityAnalyzer)