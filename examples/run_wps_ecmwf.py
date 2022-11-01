import re,os
from  WRF_NAMELIST_CREATOR import NamelistCreater as WNC
from  WRF_NAMELIST_CREATOR import Executors as RUN_EXE
from  WRF_NAMELIST_CREATOR import Tools 
from  subprocess import run

WNC = WNC(STR_DIR="./WPS")
WNC.debug = True

arrStartDateIn = [2018, 10, 10, 0, 0, 0]
arrEndDateIn   = [2018, 10, 13, 0, 0, 0]

WNC.read_user_specific(run_time      = [0, 0, 0, 72, 0, 0],
                       start_time    = [2018, 10, 10, 0, 0, 0], 
                       end_time      = [2018, 10, 13, 0, 0, 0],
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
RUN_WPS = RUN_EXE()
RUN_WPS.strFolder_WPS = DIR_WPS
RUN_WPS.run_geogrid()

# 


# Running the ungrib

#        ARR_METGRID_LEVELS[$INDEX_MDI]=138
#        STR_MODELDUMMY=''
#        FILE_UNGRIB_NAME_OUT='ECMWF_OUT'
#        FILE_UNGRIB_NAME_IN="ECMWF_ML','ECMWF_SFC','PRES"


# Running the metgrid




#WNC.create_wps_namelist()





