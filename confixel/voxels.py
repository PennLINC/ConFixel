#!/usr/bin/env python
import os.path as op
import nibabel as nb
import pandas as pd
import numpy as np
from collections import defaultdict
import h5py



def flattened_image(scalar_image, scalar_mask, group_mask_matrix):
    scalar_mask_img = nb.load(scalar_mask)
    scalar_mask_matrix = scalar_mask_img.get_fdata() > 0
    
    scalar_img = nb.load(scalar_image)
    scalar_matrix = scalar_img.get_fdata()

    scalar_matrix[np.logical_not(scalar_mask_matrix)] = np.nan
    return scalar_matrix[group_mask_matrix]
    

def back_to_3d(group_mask_file, results_array, out_file):

    group_mask_img = nb.load(group_mask_file)
    group_mask_matrix = group_mask_img.get_fdata() > 0

    output = np.zeros(group_mask_matrix.shape)
    output[group_mask_matrix] = results_array
    output_img = nb.Nifti1Image(output, affine=group_mask_img.affine,
                                header=group_mask_img.header)
    output_img.to_filename(out_file)



def write_hdf5(group_mask_file, cohort_file, 
               output_h5='voxeldb.h5',
               relative_root='/'):
    """
    Load all fixeldb data.
    Parameters
    -----------
    group_mask_file: str
        path to a Nifti1 binary group mask file
    cohort_file: str
        path to a csv with demographic info and paths to data
    output_h5: str
        path to a new .h5 file to be written
    relative_root: str
        path to which index_file, directions_file and cohort_file (and its contents) are relative
    """
    # gather cohort data
    cohort_df = pd.read_csv(op.join(relative_root, cohort_file))

    # Load the group mask image to define the rows of the matrix
    group_mask_img = nb.load(group_mask_file)
    group_mask_matrix = group_mask_img.get_fdata() > 0

    # upload each cohort's data
    scalars = defaultdict(list)
    sources_lists = defaultdict(list)
    print("Extracting .mif data...")
    for ix, row in tqdm(cohort_df.iterrows(), total=cohort_df.shape[0]):   # ix: index of row (start from 0); row: one row of data
        scalar_file = op.join(relative_root, row['source_file'])
        scalar_mask_file = op.join(relative_root, row['source_mask_file'])
        scalar_data = flattened_image(scalar_file, scalar_mask_file, group_mask_matrix)
        scalars[row['scalar_name']].append(scalar_data)   # append to specific scalar_name
        sources_lists[row['scalar_name']].append(row['source_file'])  # append source mif filename to specific scalar_name

    # Write the output
    output_file = op.join(relative_root, output_h5)
    f = h5py.File(output_file, "w")
    
    # voxelsh5 = f.create_dataset(name="voxels", data=voxel_table.to_numpy().T)
    # voxelsh5.attrs['column_names'] = list(voxel_table.columns)
    
    for scalar_name in scalars.keys():  # in the cohort.csv, two or more scalars in one sheet is allowed, and they can be separated to different scalar group.
        one_scalar_h5 = f.create_dataset('scalars/{}/values'.format(scalar_name),
                         data=np.row_stack(scalars[scalar_name]))
        one_scalar_h5.attrs['column_names'] = list(sources_lists[scalar_name])  # column names: list of source .mif filenames
    f.close()
    return int(not op.exists(output_file))