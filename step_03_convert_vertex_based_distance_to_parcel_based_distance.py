import pandas as pd
import os
import glob
from com_fun_convert_data_32k_to_parcels import convert_data_32k_to_parcels_180


# convert vertex-based surf to parcel-based surf

path_input = '/home/xiuyi/Data/HCP/03_dconn_data_part/vertex_based_min_dist_to_landmarks_sulcus'
path_output = '/home/xiuyi/Data/HCP/03_dconn_data_part/parcel_based_min_dist_to_landmarks_sulcus'

os.makedirs(path_output, exist_ok = True)
file_name_base_L = 'parcel_min_dist_landmark_sulcus_L.xlsx'
file_name_base_R = 'parcel_min_dist_landmark_sulcus_R.xlsx'

file_names_L = glob.glob('%s/*_vertex_min_dist_landmark_sulcus_L.xlsx'%(path_input))
file_names_R = glob.glob('%s/*_vertex_min_dist_landmark_sulcus_R.xlsx'%(path_input))

file_names_L.sort()
file_names_R.sort()

for file_name in file_names_L:

    # get subj_ID
    subj_ID = os.path.basename(file_name)[0:6]

    file_parcel = os.path.join(path_output,'%s_%s'%(subj_ID,file_name_base_L))
    if not os.path.exists(file_parcel):
        df_vertex = pd.read_excel(file_name)
        data = df_vertex.T.to_numpy()
        data_parcels = convert_data_32k_to_parcels_180(data_32k=data, hemi='L')

        data_parcels_T = pd.DataFrame(data_parcels.T )
        data_parcels_T.rename(columns = {0:'central_sulcus',1: 'calcarine_sulcus',2:'temporal_transverse'},inplace=True)
        data_parcels_T.index.name = 'parcel_ID'
        data_parcels_T.to_excel(file_parcel)

for file_name in file_names_R:

    # get subj_ID
    subj_ID = os.path.basename(file_name)[0:6]

    file_parcel = os.path.join(path_output,'%s_%s'%(subj_ID,file_name_base_R))

    if not os.path.exists(file_parcel):
        df_vertex = pd.read_excel(file_name)
        data = df_vertex.T.to_numpy()
        data_parcels = convert_data_32k_to_parcels_180(data_32k=data, hemi='R')

        data_parcels_T = pd.DataFrame(data_parcels.T )
        data_parcels_T.rename(columns = {0:'central_sulcus',1: 'calcarine_sulcus',2:'temporal_transverse'},inplace=True)
        data_parcels_T.index.name = 'parcel_ID'
        data_parcels_T.to_excel(file_parcel)