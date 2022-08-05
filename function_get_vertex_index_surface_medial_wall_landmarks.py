# get the vertex ID in the 32k space of central sulcus in the LH and RH for each participant

# https://www.mail-archive.com/hcp-users@humanconnectome.org/msg01989.html
import os
import nibabel as nib
import numpy as np

path_base = '/home/xiuyi/Data/HCP/01_lable_data'
folder_sub = 'MNINonLinear/fsaverage_LR32k'

# the total vertices number of LH in the surface only space
vertex_surface_only_num_L = 29696

# only left central sulcus (46 ==1; right central sulcus 121 == 2)
# this info can be checked by
# wb_command  -file_ori-information  100206.aparc.a2009s.32k_fs_LR.dlabel.nii

# the input is 'participant_ID.aparc.a2009s.32k_fs_LR.dlabel.nii'
def get_vertex_ID_surface_only(participant_ID,landmark_L,landmark_R):
    """
    get the vertex id of central sulcus(LH & RH)
    :param participant_ID:
    :return:
    """
    file = os.path.join(path_base, participant_ID, folder_sub, '%s.aparc.a2009s.32k_fs_LR.dlabel.nii' % (participant_ID))
    data = nib.load(file).get_fdata()[0]

    # get the vertices of left central
    vertices_landmark_L = np.where(data == landmark_L)[0]
    vertices_landmark_R_59k = np.where(data == landmark_R)[0]

    # subtract the R id from the total vertex on the LH, otherwise, the index in the 32k would be out of range
    vertices_landmark_R = [x - vertex_surface_only_num_L for x in vertices_landmark_R_59k]

    return vertices_landmark_L, vertices_landmark_R


def get_vertex_index_surface_medial_wall_landmarks(participant_ID,landmark_L,landmark_R):
    """
    get the vertex_index of central sulcus in 32k space of each participant
    :param participant_ID:
    :return:
    """
    # the file_ori of the cifti 91282
    greyordinates_path = '/home/xiuyi/Data/HCP/standard_mesh_atlases/standard_mesh_definition'
    greyordinates_file = 'cifti2_91282_Greyordinates.dscalar.nii'

    greyordinates_img = nib.load(os.path.join(greyordinates_path, greyordinates_file))

    # choose the vertex on the left and right surface
    # if it is not on the surface, the brain_model structure would be
    # CIFTI_STRUCTURE_ACCUMBENS_LEFT (subcortical_name)
    # CIFTI_STRUCTURE_ACCUMBENS_RIGHT
    for brain_model in greyordinates_img.header.get_index_map(1).brain_models:

        if brain_model.brain_structure == 'CIFTI_STRUCTURE_CORTEX_LEFT':
            cortex_left = brain_model

        if brain_model.brain_structure == 'CIFTI_STRUCTURE_CORTEX_RIGHT':
            cortex_right = brain_model

    # list the vertex index in the 32k, including the surface and medial wall
    # the index [i] in the vertex_indices_left is the index on the surface only
    # vertex_indices_left[i] is the index in the 32k
    vertex_indices_L  = list(cortex_left.vertex_indices)
    vertex_indices_R  = list(cortex_right.vertex_indices)

    # get the vertices of central sulcus on the surface only
    vertices_landmark_L, vertices_landmark_R = get_vertex_ID_surface_only(participant_ID=participant_ID,landmark_L=landmark_L,landmark_R=landmark_R)

    vertices_32k_landmark_L =[]
    vertices_32k_landmark_R =[]

    for index in vertices_landmark_L:
        vertices_32k_landmark_L.append(vertex_indices_L[index])

    for index in vertices_landmark_R:
        vertices_32k_landmark_R.append(vertex_indices_R[index])


    return vertices_32k_landmark_L, vertices_32k_landmark_R

