
# step 1 run it for each folder


# export source_base=/home/xiuyi/Data/HCP/01_Gifti_data/${sub_folder}/

export source_base=/HCP/01_Gifti_data
export destination_base=/HCP/02_dconn_data/



cd ${source_base}


for f in `ls`

do

   echo ${f}

   source_path=${source_base}/${f}/${middle_folder}

   destination_path=${destination_base}/${f}/

   mkdir -p ${destination_path}

	   

   wb_command -surface-geodesic-distance-all-to-all  ${source_path}/${f}.L.midthickness_MSMAll.32k_fs_LR.surf.gii    ${destination_path}/${f}.L.32k.distance.all.dconn.nii

   wb_command -surface-geodesic-distance-all-to-all  ${source_path}/${f}.R.midthickness_MSMAll.32k_fs_LR.surf.gii    ${destination_path}/${f}.R.32k.distance.all.dconn.nii

done


