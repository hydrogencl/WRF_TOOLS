import re,os
from  WRF_TOOLS import NamelistCreater as WNC
from  WRF_TOOLS import Executors as RUN_EXECS
from  WRF_TOOLS import Tools 
from  subprocess import run
import argparse

###############
# Parsers
###############

parser = argparse.ArgumentParser(description='Reading input date')
parser.add_argument("-wg","--wps-geogrid", action=argparse.BooleanOptionalAction, 
                    dest='if_exec_wps_geogrid', default=False, help='if the script execute the geogrid.exe')
parser.add_argument("-wu","--wps-ungrib",  action=argparse.BooleanOptionalAction, 
                    dest='if_exec_wps_ungrib' , default=False, help='if the script execute the ungrib.exe ')
parser.add_argument("-wm","--wps-metgrid", action=argparse.BooleanOptionalAction, 
                    dest='if_exec_wps_metgrid', default=False, help='if the script execute the metgrid.exe')
parser.add_argument("-lg","--link_grib",   action=argparse.BooleanOptionalAction, 
                    dest='if_link_grib'       , default=False, help='if link the gribecute the ungrib.exe ')
parser.add_argument("-id","--input-data-set", type=str, 
                    dest='str_input_dataset'    , default='ECMWF', help='The choosing dataset, default: ECMWF ')
args = parser.parse_args()

###############
#   Namelist
###############

WNC = WNC()
WNC.debug = True

arrStartDateIn = [2022,  3,  3, 0, 0, 0]
arrEndDateIn   = [2022,  3,  3,12, 0, 0]

WNC.read_user_specific(run_time      = [0, 0, 0, 12, 0, 0],
                       start_time    = [2022,  3,  3, 0, 0, 0], 
                       end_time      = [2022,  3,  3,12, 0, 0],
                       max_dom       = 2, 
                       e_we          = [221, 341],
                       e_sn          = [221, 341],
                       dx            = 15000,
                       dy            = 15000,
                       grid_id       = [1,2],
                       parent_id     = [1,1],
                       i_parent_start = [1,94],
                       j_parent_start =  [1,54],
                       parent_grid_ratio = [1,5])

arrStartDate = [ Tools.make_wrf_datetime(arrStartDateIn), Tools.make_wrf_datetime(arrStartDateIn) ]
arrEndDate   = [ Tools.make_wrf_datetime(arrEndDateIn), Tools.make_wrf_datetime(arrEndDateIn) ]

# Parameters:

DIR_GEODATA="/p/project/cjiek80/ESIAS-MET/DATA/GEODATA"
DIR_GEFS   ="/gpfs/arch/jiek80/jiek8002/GEFS"
DIR_ECMWF  ="/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib"

# Folders:

DIR_WPS    = "/p/scratch/cjiek80/jiek8010/WRFV4/WPS"

# Running the geogrid
# Namelist of share

WNC.DIC_share_common_para["start_date"]["VALUE"] = arrStartDate
WNC.DIC_share_common_para["end_date"]["VALUE"]   = arrEndDate
WNC.DIC_share_common_para["wrf_core"]["VALUE"]   = "ARW"
WNC.DIC_share_common_para["max_dom" ]["VALUE"]   = 2

# Namelist of geogrid

WNC.DIC_geogrid_common_para["geog_data_res"]["VALUE"] = \
        [ 'modis_30s+2m', 'modis_30s', 'modis_30s' ]
WNC.DIC_geogrid_common_para["dx"]["VALUE"]                =  15000.0
WNC.DIC_geogrid_common_para["dx"]["VALUE"]                =  15000.0

WNC.DIC_geogrid_common_para["parent_id"]["VALUE"]         = [   1,   1 ]
WNC.DIC_geogrid_common_para["parent_grid_ratio"]["VALUE"] = [   1,   3 ]

WNC.DIC_geogrid_common_para["i_parent_start"]["VALUE"]    = [   1,  94 ]
WNC.DIC_geogrid_common_para["j_parent_start"]["VALUE"]    = [   1,  54 ]
WNC.DIC_geogrid_common_para["e_we"]["VALUE"]              = [ 221, 341 ] 
WNC.DIC_geogrid_common_para["e_sn"]["VALUE"]              = [ 221, 341 ]

WNC.DIC_geogrid_common_para["ref_lat"]["VALUE"]           = 54.0 
WNC.DIC_geogrid_common_para["ref_lon"]["VALUE"]           =  8.5
WNC.DIC_geogrid_common_para["truelat1"]["VALUE"]          = 30.0
WNC.DIC_geogrid_common_para["truelat2"]["VALUE"]          = 60.0
WNC.DIC_geogrid_common_para["stand_lon"]["VALUE"]         =  8.5

WNC.DIC_geogrid_common_para["geog_data_path"]["VALUE"]    = DIR_GEODATA  

WNC.create_wps_namelist()


RUN_EXE = RUN_EXECS()
RUN_EXE.strFolder_WPS = DIR_WPS

# Execute geogrid.exe 
if args.if_exec_wps_geogrid:
    RUN_EXE.run_geogrid()

# Execute the link of grib input
if args.if_link_grib:
    arrECMWF_Files = \
    [ "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030300_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030303_ml.grb",     
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030306_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030309_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030312_ml.grb"]
    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)

#Execute ungrib.exe for ecmwf-era5
if args.if_exec_wps_ungrib and args.str_input_dataset == 'ECMWF':
    arrECMWF_Files = \
    [ "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030300_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030303_ml.grb",     
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030306_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030309_ml.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030312_ml.grb"]
    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)
    RUN_EXE.strTargetVtableName = 'Vtable.ECMWF.ml.grib2' 
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_ML'
    WNC.DIC_metgrid_common_para["fg_name"]["VALUE"] = ["ECMWF_ML','ECMWF_SFC','PRES"]
    WNC.create_wps_namelist()
    RUN_EXE.run_ungrib()

    arrECMWF_Files = \
    [ "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030300_sf.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030303_sf.grb",     
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030306_sf.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030309_sf.grb",
      "/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2022/03/2022030312_sf.grb"]
    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)
    RUN_EXE.strTargetVtableName = 'Vtable.ERA-interim.ml' 
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_SFC'
    WNC.create_wps_namelist()
    RUN_EXE.run_ungrib()

    WNC.create_wps_namelist()
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_SFC'
    RUN_EXE.run_calc_ecmwf_p()

# Running the metgrid

#        ARR_METGRID_LEVELS[$INDEX_MDI]=138
#        FILE_UNGRIB_NAME_IN="ECMWF_ML','ECMWF_SFC','PRES"


if args.if_exec_wps_metgrid:
    WNC.DIC_metgrid_common_para["fg_name"]["VALUE"] = ["ECMWF_ML','ECMWF_SFC','PRES"]
    WNC.create_wps_namelist()
    RUN_EXE.run_metgrid()

if args.if_exec_wrf_real:
    RUN_EXE.run_real()

