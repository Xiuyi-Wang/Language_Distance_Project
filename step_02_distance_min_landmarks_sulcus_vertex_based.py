import numpy as np
import nibabel as nib
import os
import pandas as pd



import sys
import collections
import glob

from copy import deepcopy

sys.path.append('PycharmProjects/Language_Distance_Project')
from com_fun_get_vertex_index import get_vertex_index_medial_wall_l_r
from pylab import *
from function_get_vertex_index_surface_medial_wall_landmarks import get_vertex_index_surface_medial_wall_landmarks

rcParams['figure.figsize'] = (12, 12)

# get the vertex id of one landmark sulcus (central sulcus; LH & RH) on the surface only, on the surface and medial wall
# read the distance matrix data of one participant(LH & RH): 32k * 32k
# select part of the surf matrix  n * 32k (n is the number of vertex in V1)
# get the min of the surf matrix: so each vertex has a min distance to other vertices in the sulcus
# get all the data for each participant
# run paired t test
# using spin permutation to (at least partically) control for the autocorrlation.

path_base = '/HCP/02_dconn_data'
path_output = '/HCP/03_dconn_data_part/vertex_based_min_dist_to_landmarks_sulcus'

os.makedirs(path_output, exist_ok = True)


# parcels id of sensory: landmark sulcus info
# central sulcus
central_L = 46
central_R = 121

# calcarine sulcus
calcarine_L = 45
calcarine_R = 120

# temporal transverse
temporal_transverse_L = 75
temporal_transverse_R = 150

landmarks = [[central_L, central_R], [calcarine_L, calcarine_R], [temporal_transverse_L, temporal_transverse_R]]
landmarks_names = ['central_sulcus','calcarine_sulcus','temporal_transverse']

# todo to change this later
perm_t_num = 10000

thre_p = 0.05

# This is the template to display the result
path_surf_gii = '/HCP/HCP_S1200_GroupAvg_v1'
filename_surf_gii_L = 'S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii'
filename_surf_gii_R = 'S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii'

# %% step 1: get all the indexes of vertices on the 32k of the landmarks for each participant

# get all the vertices on the medial wall
vertices_medial_wall_L, vertices_medial_wall_R = get_vertex_index_medial_wall_l_r()

# %% step 2: read the dconn data
# Read one dconn.data to get the matrix
file_base = '.32k.distance.all.dconn.nii'
hemis = ['L','R']

#%% step 1: calculate the vertex based distance to each landmark


sub_IDs = os.listdir(path_base)
sub_IDs.sort()

for sub_ID in sub_IDs:

for hemi in hemis:

    file_dist_min = os.path.join(path_output, '%s_vertex_min_dist_landmark_sulcus_%s.xlsx' % (sub_ID, hemi))

    if not os.path.exists(file_dist_min):
        # read the dconn data of each participant
        dconn_file = os.path.join(path_base, sub_ID, sub_ID+'.'+ hemi +file_base)
        dconn_mat = nib.load(dconn_file).get_fdata()

        df_dist_min = pd.DataFrame()

        # get the vertices of each landmark sulcus
        for i in range(len(landmarks_names)):
            landmark_L = landmarks[i][0]
            landmark_R = landmarks[i][1]
            landmarks_name = landmarks_names[i]

            vertices_32k_landmark_L, vertices_32k_landmark_R = get_vertex_index_surface_medial_wall_landmarks(participant_ID= sub_ID, landmark_L = landmark_L, landmark_R = landmark_R)

            if hemi == hemis[0]:
                vertices_32k_landmark = vertices_32k_landmark_L
            elif hemi == hemis[1]:
                vertices_32k_landmark = vertices_32k_landmark_R

            # choose the distance to landmark sulcus, respectively
            dconn_mat_landmark = dconn_mat[vertices_32k_landmark][:]

            # get the minimum distance of each vertex
            dconn_landmark_dim = dconn_mat_landmark.min(axis=0)

            # write it to df
            df_dist_min[landmarks_name] = dconn_landmark_dim
        # save the file_ori
        df_dist_min.to_excel(file_dist_min, index=False)



