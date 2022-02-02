#!/bin/bash 

#SBATCH --partition=short-serial 
#SBATCH --array=0-2
#SBATCH --job-name=py2nc_array
#SBATCH -o py2nc_array_%A_%a.out 
#SBATCH -e py2nc_array_%A_%a.err 
#SBATCH --time=00:30:00

module add jaspy/3.7


#year=( 1999 2000 2001 2002 2003 2004 )

input_base='/gws/nopw/j04/cidar/data/incoming/UM_control/'
run_name='ba751'
stashfolder='p1'

output_base='/work/scratch-nopw/dlowe/nc3/'

variable_names=( 'rain' 'low_cloud' 'mid_cloud' )

variable_sources=( 'm01s04i203' 'm01s09i203' 'm01s09i205' )

# year will be not set, so all years will be processed



### array job specific code

jobid=$SLURM_ARRAY_TASK_ID


input_args="--input_base ${input_base} --run_name ${run_name} --stashfolder ${stashfolder}"

output_args="--output_base ${output_base}"

variable_args="--met_variable_name ${variable_sources[$jobid]} --new_variable_name ${variable_names[$jobid]}"

python pp2nc_general.py ${input_args} ${output_args} ${variable_args}

