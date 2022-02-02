#!/usr/bin/env python
# python script to load ppfiles and save to netcdf

#libs
import cf
import os
import time
import glob


def create_full_filelisting(dirname,runname,stashfolder,file_years):
    filelisting = []
    for year in file_years:
        fileinname=os.path.join(dirname, "mi-" + runname, stashfolder, runname + "a." + stashfolder  + year + "*")
        try:
            files = glob.glob(fileinname)
            if isinstance(files, str):
                filelisting.append(files)
            elif isinstance(files, list):
                filelisting += glob.glob(fileinname)
        except:
            pass
    return(filelisting)

def create_monthly_glob_filelisting(dirname,runname,stashfolder,file_year,file_months):
    filelisting = []
    for fmonth in file_months:
        filelisting.append(os.path.join(dirname, "mi-" + runname, stashfolder, 
                        runname + "a." + stashfolder  + file_year + fmonth + "*"))
    return(filelisting)

# set variable names as the long name (some variables have missing standard names)
def long_name_function(f):
    for x in range(0, len(f), 1):
        f[x].standard_name=f[x].long_name 

def convert_data(filelisting,variablename,diroutname,varname):
    # loop through open all files and save as netcdf
    for x in filelisting:
        print(x)
        #f=cf.read(x, select=variablename, verbose=3, fmt='UM', um={'fmt':'PP'})
        f=cf.read(x, select=variablename)
        long_name_function(f)
    
        fileoutname=x.split("/")[-1]
        fileoutname=fileoutname.replace(".pp", "")
        fileoutname=os.path.join(diroutname, varname, fileoutname + "." + varname + ".nc")

        cf.write(f, fileoutname, verbose=-1, compress=1)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Script for converting PP data to netcdf")

    parser.add_argument("--input_base",help="Base directory for input files")
    
    parser.add_argument("--run_name",help="Met Office run name (e.g. 'ba751')")
    parser.add_argument("--stashfolder",help="Stash directory within run directory (e.g. 'p1')")

    parser.add_argument("--met_variable_name",help="Variable name within met file (e.g. 'm01s04i203')")

    parser.add_argument("--output_base",help="Base directory for output files")
    
    parser.add_argument("--new_variable_name",help="Variable name for created netcdf file")
        
    parser.add_argument("--year", default=[''], metavar='YYYY', dest="file_years", type=str, nargs='+', 
                        help="Years to process. Default is an empty list (all).")
    
    args = parser.parse_args()
    
    # set directory
    if args.input_base:
        dirname = args.input_base
    else:
        print('Using default input base')
        dirname='/gws/nopw/j04/cidar/data/incoming/UM_control/'
    
    if args.output_base:
        diroutname = args.output_base
    else:
        print('Using default output base')
        diroutname='/work/scratch-nopw/dlowe/nc3/'

    # set model run and folder
    if args.run_name:
        runname = args.run_name
    else:
        print("using default runname")
        runname='ba751'
    
    if args.stashfolder:
        stashfolder = args.stashfolder
    else:
        print("using default stashfolder")
        stashfolder='p1'

    file_years = args.file_years
    #file_year='' # leave blank for all years or enter year to do a subset

    # what to call the variable in the filename out, and make a new directory
    if args.new_variable_name:
        varname = args.new_variable_name
    else:
        print("using default output variable name")
        varname='rain'
    
    # p1 variable list, uncomment a single variables for which is required
    if args.met_variable_name:
        variablename = f'um_stash_source={args.met_variable_name}'
    else:
        print("using default met variable name")
        variablename = 'um_stash_source=m01s04i203' # | LARGE SCALE RAINFALL RATE    KG/M2/S
    
    #variablename='um_stash_source=m01s00i030' # | LAND MASK (No halo) (LAND=TRUE)
    #variablename='um_stash_source=m01s00i033' # | OROGRAPHY (/STRAT LOWER BC)
    #variablename='um_stash_source=m01s00i409' # | SURFACE PRESSURE AFTER TIMESTEP
    #variablename='um_stash_source=m01s01i215' # | DIRECT SURFACE SW FLUX : CORRECTED
    #variablename='um_stash_source=m01s01i216' # | DIFFUSE SURFACE SW FLUX : CORRECTED
    #variablename='um_stash_source=m01s02i207' # | DOWNWARD LW RAD FLUX: SURFACE
    #variablename='um_stash_source=m01s03i209' # | 10 METRE WIND U-COMP
    #variablename='um_stash_source=m01s03i210' # | 10 METRE WIND V-COMP
    #variablename='um_stash_source=m01s03i236' # | TEMPERATURE AT 1.5M
    #variablename='um_stash_source=m01s03i245' # | RELATIVE HUMIDITY AT 1.5M
    
    #variablename='um_stash_source=m01s04i204' # | LARGE SCALE SNOWFALL RATE    KG/M2/S
    #variablename='um_stash_source=m01s09i203' # | LOW CLOUD AMOUNT
    #variablename='um_stash_source=m01s09i204' # | MEDIUM CLOUD AMOUNT
    #variablename='um_stash_source=m01s09i205' # | HIGH CLOUD AMOUNT


    print("years = ",file_years)
    
    
    # create output directory, if needed
    try:
        os.mkdir(os.path.join(diroutname, varname))
    except FileExistsError :
        pass
    except :
        raise


    filelisting = create_full_filelisting(dirname,runname,stashfolder,file_years)

    print(filelisting)
    
    #convert_data(filelisting,variablename,diroutname,varname)







