import os
import nibabel as nib
import numpy as np
import itertools

# This is the Glassier 360 rois. 1- 180 is right hemisphere; 181 - 360 is left hemisphere.
# Left has 29696 vertices; right has 29716 vertices
group_parcel_path = '/home/xiuyi/Data/HCP/HCP_S1200_GroupAvg_v1'
parcel_name = 'Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii'

parcel_num = 180

# This is the 91282_Greyordinates template file_ori downloaded from
# https://github.com/Washington-University/HCPpipelines/tree/master/global/templates/91282_Greyordinates
greyordinates_path = '/home/xiuyi/Data/HCP/standard_mesh_atlases/standard_mesh_definition'
greyordinates_file = 'cifti2_91282_Greyordinates.dscalar.nii'


# get all the indexes of vertices on the surface only of each parcel
def get_vertex_index_only_surface_parcel(parcels):
    """
    get all the vertex index of each parcel on the surface only and then store it to a dict
    both the left and right parcels start with 0
    :param parcels:  a list or array: the parcels ID
    :return: parcel_vertices_index_only_surface = dict; key - value: parcel_id - indexes of vertices on the surface
    """
    # read the parcel data
    parcel_label = nib.load(os.path.join(group_parcel_path, parcel_name)).get_fdata()[0]

    # parcel_label is a np.memmap, including the vertex number of each vertex on the surface
    # type(parcel_label) is (1,59412) = 29696 (left) + 29716 (right)
    # left parcel: 181- 360
    # right parcel: 1 - 180  # This is different from Cole-Anticevic Brain-wide network partition.

    # get the maximum vertices on the LH
    vertices_left_max = max(np.where(parcel_label > parcel_num)[0])

    # get all the vertices index of each parcel
    parcel_vertices_index_only_surface = {}

    for parcel in parcels:

        # adjust the row number of the right hemisphere, make it starts with 0 not 29696 or 1
        if parcel > 0 and parcel <= parcel_num:
            vertices_each_parcel = np.squeeze(np.where(parcel_label == parcel)) - vertices_left_max - 1
            parcel_vertices_index_only_surface[parcel] = vertices_each_parcel

        elif parcel > parcel_num and parcel <= parcel_num *2 :
            vertices_each_parcel = np.squeeze(np.where(parcel_label == parcel))
            parcel_vertices_index_only_surface[parcel] = vertices_each_parcel

        else:
            print (parcel, 'parcel num is not correct')

    return parcel_vertices_index_only_surface

# get_vertex_index_surface_medial_wall_parcel
def get_vertex_index_surface_medial_wall_parcel (parcel_vertices_index_only_surface):
    """
    get all the vertex index of each parcel on the surface and medial wall (32k) and then store it to a dict
    :param parcel_vertices_index_only_surface: is a dict, keys are parcel_ids, values are vertices_index_only_surface
    :return: parcel_vertices_index_surface_medial_wall
    a dict, key - value : parcel_ids - parcel_vertices_index_surface_medial_wall
    """
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
    vertex_indices_left  = list(cortex_left.vertex_indices)
    vertex_indices_right = list(cortex_right.vertex_indices)

    # create a dict, keys are parcels, values are the vertex_indeces_in 32k
    parcel_vertices_index_surface_medial_wall = {}

    # find the corresponding vertex id of each row id
    for parcel in parcel_vertices_index_only_surface.keys():
        vertices_32k_each_parcel =[]

        if parcel> 0 and parcel <= parcel_num:
            vertex_indices = vertex_indices_right

        elif  parcel > parcel_num and parcel <= parcel_num * 2 :
            vertex_indices = vertex_indices_left

        else:
            print(parcel, 'parcel num is not in the range')

        for index in parcel_vertices_index_only_surface[parcel]:
            vertices_32k_each_parcel.append(vertex_indices[index])

        parcel_vertices_index_surface_medial_wall[parcel] = vertices_32k_each_parcel

    return parcel_vertices_index_surface_medial_wall

vertex_num = 32492
vertices_all = np.arange(vertex_num)

parcels_all_right = np.arange(1, parcel_num + 1)
parcels_all_left = np.arange(parcel_num + 1, parcel_num * 2 + 1)

def get_vertex_index_medial_wall_each_hemi(parcels_all):
    """
    parcels_all: is the parcel ids of left or right H.
    :return: vertices_medial_wall: the vertex id on the medial wall
    """
    vertices_index_only_surface = get_vertex_index_only_surface_parcel(parcels_all)
    vertices_index_surface_medial_wall = get_vertex_index_surface_medial_wall_parcel(vertices_index_only_surface)
    vertices_surface = list(vertices_index_surface_medial_wall.values())
    vertices_surface = np.array(list(itertools.chain(*vertices_surface)))

    # choose all the vertex not on the surface
    vertices_medial_wall = np.setdiff1d(vertices_all, vertices_surface)

    return vertices_medial_wall

def get_vertex_index_medial_wall_l_r():
    """
    :return: the vertex id on the medial on the left H and right H, respectively
    """
    vertices_medial_wall_left = get_vertex_index_medial_wall_each_hemi(parcels_all_left)
    vertices_medial_wall_right = get_vertex_index_medial_wall_each_hemi(parcels_all_right)

    return vertices_medial_wall_left, vertices_medial_wall_right



