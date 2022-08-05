import numpy as np
import pandas as pd
from com_fun_get_vertex_index import get_vertex_index_only_surface_parcel
from com_fun_get_vertex_index import get_vertex_index_surface_medial_wall_parcel

parcel_num = 180
parcels_L = list(np.arange(parcel_num+1, parcel_num*2+1))
parcels_R = list(np.arange(1, parcel_num+1))

parcel_vertices_index_only_surface_L = get_vertex_index_only_surface_parcel(parcels_L)
parcel_vertices_index_only_surface_R = get_vertex_index_only_surface_parcel(parcels_R)

parcel_vertices_index_surface_medial_wall_L = get_vertex_index_surface_medial_wall_parcel(parcel_vertices_index_only_surface_L)
parcel_vertices_index_surface_medial_wall_R = get_vertex_index_surface_medial_wall_parcel(parcel_vertices_index_only_surface_R)

def convert_data_surface_only_to_parcels_180(data_vertex_surface_only, hemi):
    """
    convert the data from 32k to 180 parcels of each hemi
    :param data_vertex_surface_only: the array: shape: N_subj, total_vertex_ID on the hemi
    :param hemi: hemi = 'L' or 'R
    :return:
    """

    if hemi == 'L':
        parcel_vertices_index_only_surface = parcel_vertices_index_only_surface_L

    elif hemi == 'R':
        parcel_vertices_index_only_surface = parcel_vertices_index_only_surface_R

    data_parcels = pd.DataFrame()
    for parcel_ID in parcel_vertices_index_only_surface.keys():

        # get the vertices index of this parcel
        vertices_parcel = parcel_vertices_index_only_surface[parcel_ID]

        # get the mean value of this parcel
        data_32k_parcel = data_vertex_surface_only[:, vertices_parcel].mean(axis=1)

        # add it to a df
        data_parcels[parcel_ID] = data_32k_parcel

    return data_parcels


def convert_data_32k_to_parcels_180(data_32k, hemi):
    """
    convert the data from 32k to 180 parcels of each hemi
    :param data_32k: the array: shape: N_subj, total_vertex_ID on the hemi
    :param hemi: hemi = 'L' or 'R
    :return:
    """

    if hemi == 'L':
        parcel_vertices_index_surface_medial_wall = parcel_vertices_index_surface_medial_wall_L

    elif hemi == 'R':
        parcel_vertices_index_surface_medial_wall = parcel_vertices_index_surface_medial_wall_R

    data_parcels = pd.DataFrame()
    for parcel_ID in parcel_vertices_index_surface_medial_wall.keys():

        # get the vertices index of this parcel
        vertices_parcel = parcel_vertices_index_surface_medial_wall[parcel_ID]

        # get the mean value of this parcel
        data_32k_parcel = data_32k[:, vertices_parcel].mean(axis=1)

        # add it to a df
        data_parcels[parcel_ID] = data_32k_parcel

    return data_parcels
