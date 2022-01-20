# ConFixel
Convert Fixels back and forth from h5 files!

## Prepare data
To convert (a list of) fixel data from .mif format to .h5 format, you need to prepare a cohort csv file that provides several basic informations of all .mif files you want to include. We recommend that, for each scalar (e.g. FD/FC/FDC), prepare one .csv file, and thus getting one .h5 file.

### Cohort's csv file (for each scalar)
Each row of a cohort .csv is for one mif file you want to include. The file should at least include these columns (Notes: these column names are fixed, i.e. not user-defined):

* "scalar_name": name of fixel data metric, e.g. FD, FC, or FDC 
* "source_file": filename of a mif file. ConFixel argument "--relative-root" and "source_file" here will be combined and together define the directory and filenames of the mif file. Notice that if "--relative-root" does not completely (but only partially) point to the folder where this mif file locates, you should add necessary folders (paths) in "source_file" here. For example, If a mif file is in folder "/home/username/myProject/FD", and when you run ConFixel, you specify "--relative-root" as "/home/username/myProject/", then, source_file should be "FD/sub1_fd.mif" for this mif file. See example below for more.

### Example
#### Example **folder structure**:

```
/home/username/myProject/data
|
├── cohort_FD.csv   
│
├── FD
│   ├── index.mif
│   ├── directions.mif
|   ├── sub1_fd.mif
|   ├── sub2_fd.mif
|   ├── sub3_fd.mif
│   ├── ...
│
├── FC
│   ├── index.mif
│   ├── directions.mif
|   ├── sub1_fc.mif
|   ├── sub2_fc.mif
|   ├── sub3_fc.mif
|   ├── ...
└── ...
```
These mif files are generated by MRtrix.

#### Corresponding **csv file for scalar FD** can look like this:
"cohort_FD.csv":
| ***scalar_name*** | ***source_file***  | subject_id    | age    | sex     | 
| :----:        | :----:         | :----:        | :----: |  :----: |
| FD            | FD/sub1_fd.mif | sub1          | 10     | F       |
| FD            | FD/sub2_fd.mif | sub2          | 20     | M       |
| FD            | FD/sub3_fd.mif | sub3          | 15     | F       |
| ...            | ... | ...          | ...     | ...       |

Notes:
* Columns that must be included are highlighted in ***bold and italics***;
* The order of columns can be changed.

For this case, when running ConFixel creating hdf5 fixel data, argument **--relative-root** should be "/home/username/myProject/data" 


## Run ConFixel
### Install from github
``` console
foo@bar:~$ git clone https://github.com/PennLINC/ConFixel.git
foo@bar:~$ cd ConFixel
foo@bar:~$ pip install .   # for end user
# you may remove the original repository if you are an end user:
foo@bar:~$ cd ..
foo@bar:~$ rm -r ConFixel
```
If you are a developer, if there is any update in the scripts locally, you may update the installation with:
``` console
foo@bar:~$ pip install -e .    # for developer to update
```

### Convert .mif files to an HDF5 (.h5) file
Using above described scenario as an example, for FD dataset:
``` console
foo@bar:~$ fixeldb_create \
                --index-file FD/index.mif \
                --directions-file FD/directions.mif \
                --cohort-file cohort_FD.csv \
                --relative-root /home/username/myProject/data \
                --output-hdf5 FD.h5
```
<!-- ^ above is tested -->

Now you should get the HDF5 file "FD.h5" in folder "/home/username/myProject/data". You may use [ModelArray](https://github.com/PennLINC/ModelArray) to perform statistical analysis.

### Convert result .h5 file to .mif files:
After getting statistical results in FD.h5 file, you can use `fixelstats_write` to convert results into a list of .mif files in a folder specified by you. This command will also copy the original index.mif and directions.mif to this folder.
``` console 
foo@bar:~$ fixelstats_write \
                --index-file FD/index.mif \
                --directions-file FD/directions.mif \
                --cohort-file cohort_FD.csv \
                --relative-root /home/username/myProject/data \
                --input-hdf5 FD.h5 \
                --output-hdf5 FD_stats 
```
Now you can view the results in folder FD_stats in `mrview`.

<!-- TODO: push to github + pip install -e . + test out ^^^ -->

<!--TODO: use conda + terminal command `fixeldb_create` and `fixelstats_write`; Still using case above as an example -->
<!-- TODO: also update example*.py and .sh -->