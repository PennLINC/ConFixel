# ConFixel
Companion "converter" software for [ModelArray](https://pennlinc.github.io/ModelArray/) for converting data back and forth from the HDF5 file format.

Below we show you how to use `ConFixel`. Here we focus on `ConFixel` only.

As usually `ConFixel` is used together with [ModelArray](https://pennlinc.github.io/ModelArray/), we also provide [a combined walkthrough](https://pennlinc.github.io/ModelArray/articles/walkthrough.html) of ConFixel + ModelArray with example fixel data.

## Prepare data
To convert (a list of) fixel data from .mif format to .h5 format, you need to prepare a cohort CSV file that provides several basic informations of all .mif files you want to include. We recommend that, for each scalar (e.g. FD/FC/FDC), prepare one .csv file, and thus getting one .h5 file.

### Cohort's csv file (for each scalar)
Each row of a cohort .csv is for one mif file you want to include. The file should at least include these columns (Notes: these column names are fixed, i.e. not user-defined):

* "scalar_name": which tells us what metric is being analyzed, e.g. FD, FC, or FDC 
* "source_file": which tells us which mif file will be used for this subject

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
These mif files are generated by `MRtrix`.

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

You may want to create a conda environment before installing ConFixel - see [here](https://pennlinc.github.io/ModelArray/articles/installations.html) for more.

``` console
foo@bar:~$ git clone https://github.com/PennLINC/ConFixel.git
foo@bar:~$ cd ConFixel
foo@bar:~$ pip install .   # for end user
# you may remove the original source code if you are an end user:
foo@bar:~$ cd ..
foo@bar:~$ rm -r ConFixel
```
If you are a developer, and if there is any update in the source code locally, you may update the installation with:
``` console
# Supporse you're in root directory of ConFixel source code:
foo@bar:~$ pip install -e .    # for developer to update
```

### Convert .mif files to an HDF5 (.h5) file
Using above described scenario as an example, for FD dataset:
``` console
foo@bar:~$ # first, activate conda environment with `conda activate <env_name>`
foo@bar:~$ confixel \
                --index-file FD/index.mif \
                --directions-file FD/directions.mif \
                --cohort-file cohort_FD.csv \
                --relative-root /home/username/myProject/data \
                --output-hdf5 FD.h5
```
<!-- ^ above is tested -->

Now you should get the HDF5 file "FD.h5" in folder "/home/username/myProject/data". You may use [ModelArray](https://pennlinc.github.io/ModelArray/) to perform statistical analysis.

### Convert result .h5 file to .mif files:
After running `ModelArray` and getting statistical results in FD.h5 file (say, the analysis name is called "mylm"), you can use `fixelstats_write` to convert results into a list of .mif files in a folder specified by you. This command will also copy the original index.mif and directions.mif to this folder.
``` console 
foo@bar:~$ # first, activate conda environment with `conda activate <env_name>`
foo@bar:~$ fixelstats_write \
                --index-file FD/index.mif \
                --directions-file FD/directions.mif \
                --cohort-file cohort_FD.csv \
                --relative-root /home/username/myProject/data \
                --analysis-name mylm \
                --input-hdf5 FD.h5 \
                --output-dir FD_stats 
```
Now you can view the results in folder "FD_stats" in `mrview`.

### For additional description:
You can refer to `--help` for additional information:
``` console 
foo@bar:~$ confixel --help
foo@bar:~$ fixelstats_write --help
```

<!--TODO: after update please test out: use conda + terminal command `confixel` and `fixelstats_write`; Still using case above as an example -->
<!-- fixelstats_write: can be tested out with existing results; otherwise have to run for all fixels.. -->

<!-- TODO: also update example*.py and .sh -->