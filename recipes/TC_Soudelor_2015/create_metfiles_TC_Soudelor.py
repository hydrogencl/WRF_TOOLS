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
parser.add_argument("-wg","--wps-geogrid", action='store_true',            
                    dest='if_exec_wps_geogrid', default=False, help='if the script execute the geogrid.exe')
parser.add_argument("-wu","--wps-ungrib", action='store_true',            
                    dest='if_exec_wps_ungrib' , default=False, help='if the script execute the ungrib.exe ')
parser.add_argument("-wm","--wps-metgrid", action='store_true',            
                    dest='if_exec_wps_metgrid', default=False, help='if the script execute the metgrid.exe')

parser.add_argument("-lg","--link_grib",  action='store_true',             
                    dest='if_link_grib'       , default=False, help='if link the gribecute the ungrib.exe ')
parser.add_argument("-id","--input-data-set", type=str, 
                    dest='str_input_dataset'    , default='ECMWF', help='The choosing dataset, default: ECMWF ')

parser.add_argument("-r","--wrf-real", action='store_true',            
                    dest='if_exec_wrf_real', default=False, help='if the script execute the real.exe')
parser.add_argument("-w","--wrf-wrf",  action='store_true',            
                    dest='if_exec_wrf_wrf' , default=False, help='if the script execute the wrf.exe ')
parser.add_argument("-nlw","--namelist-wrf",  action='store_true',            
                    dest='if_namelist_wrf' , default=False, help='if create the namescript in the run folder' )
args = parser.parse_args()

###############
#   Namelist
###############

WNC = WNC()
WNC.debug = True

arrStartDateIn = [2018,  8,  6,  0, 0, 0]
arrEndDateIn   = [2018,  8,  9,  0, 0, 0]
arrRunTimeIn   = [ arrEndDateIn[i] - arrStartDateIn[i] for i in range(6)]
arrRunTime     = [0,0,0, Tools.run_time_cal(arrRunTimeIn)["HOURS"],0,0 ]

arrEdgesWE     = [  501, 301  ]
arrEdgesSN     = [  401, 301  ]
# Exp3
#arrIParentSta  = [    1, 367  ] 
#arrJParentSta  = [    1, 103  ]
# Exp4
arrIParentSta  = [    1, 158  ] 
arrJParentSta  = [    1, 141  ]
numMaxDom      = 2
arrIntervalHour= [0,0,0,3,0,0]

numCenLat       = 25.0
numCenLon       = 140.0
numTrueLat1     = 0
numTrueLat2     = 50


WNC.read_user_specific(run_time      = arrRunTime,
                       start_time    = arrStartDateIn, 
                       end_time      = arrEndDateIn,
                       max_dom       = numMaxDom,
                       e_we          = arrEdgesWE,
                       e_sn          = arrEdgesSN,
                       dx            = 15000,
                       dy            = 15000,
                       grid_id       = [1,2],
                       parent_id     = [1,1],
                       i_parent_start = arrIParentSta,
                       j_parent_start = arrJParentSta,
                       parent_grid_ratio = [1,5])

arrStartDateStr = [ Tools.make_wrf_datetime(arrStartDateIn), Tools.make_wrf_datetime(arrStartDateIn) ]
arrEndDateStr   = [ Tools.make_wrf_datetime(arrEndDateIn), Tools.make_wrf_datetime(arrEndDateIn) ]

# Parameters:

DIR_GEODATA=""
DIR_GEFS   =""
DIR_ECMWF  =""

# Folders:

DIR_WPS    = "/p/scratch/exaww/lu3/WRFV4/WPS"
DIR_WRF    = "/p/scratch/exaww/lu3/WRFV4/WRF_MND"
DIR_RUN    = "{0:s}/run_mod_01".format(DIR_WRF)

# Running the geogrid
# Namelist of share

WNC.DIC_share_common_para["start_date"]["VALUE"] = arrStartDateStr
WNC.DIC_share_common_para["end_date"]["VALUE"]   = arrEndDateStr
WNC.DIC_share_common_para["wrf_core"]["VALUE"]   = "ARW"
WNC.DIC_share_common_para["max_dom" ]["VALUE"]   = numMaxDom

print("starting date: ", arrStartDateStr)
print("ending   date: ", arrEndDateStr)


# Namelist of geogrid

WNC.DIC_geogrid_common_para["geog_data_res"]["VALUE"] = \
        [ 'modis_30s+2m', 'modis_30s', 'modis_30s' ]
WNC.DIC_geogrid_common_para["dx"]["VALUE"]                =  15000.0
WNC.DIC_geogrid_common_para["dx"]["VALUE"]                =  15000.0

WNC.DIC_geogrid_common_para["parent_id"]["VALUE"]         = [   1,   1 ]
WNC.DIC_geogrid_common_para["parent_grid_ratio"]["VALUE"] = [   1,   5 ]

WNC.DIC_geogrid_common_para["i_parent_start"]["VALUE"]    = arrIParentSta  
WNC.DIC_geogrid_common_para["j_parent_start"]["VALUE"]    = arrJParentSta  
WNC.DIC_geogrid_common_para["e_we"]["VALUE"]              = arrEdgesWE    
WNC.DIC_geogrid_common_para["e_sn"]["VALUE"]              = arrEdgesSN   

WNC.DIC_geogrid_common_para["ref_lat"]["VALUE"]           = numCenLat
WNC.DIC_geogrid_common_para["ref_lon"]["VALUE"]           = numCenLon
WNC.DIC_geogrid_common_para["truelat1"]["VALUE"]          = numTrueLat1
WNC.DIC_geogrid_common_para["truelat2"]["VALUE"]          = numTrueLat2
WNC.DIC_geogrid_common_para["stand_lon"]["VALUE"]         = numCenLon

WNC.DIC_geogrid_common_para["geog_data_path"]["VALUE"]    = DIR_GEODATA  

##########################
#     WRF namelist
##########################

WNC.DIC_domains_common_para["num_metgrid_levels"]["VALUE"]    = 138  # ECMWF
WNC.DIC_domains_common_para["interp_type"]["VALUE"]           = 1  # ECMWF
WNC.DIC_domains_common_para["sfcp_to_sfcp"]["VALUE"]          = False
WNC.DIC_time_control_common_para["override_restart_timers"]["VALUE"] = True

WNC.DIC_time_control_common_para["history_outname"]["STR_FMT"] = "\'{0:s}_d<domain>{2:s}{1:s}\',"

WNC.DIC_domains_common_para["starting_time_step"]["VALUE"]     = [ 24, 12  ]
WNC.DIC_domains_common_para["max_time_step"]["VALUE"]          = [ 144, 24 ]
WNC.DIC_domains_common_para["time_step"]["VALUE"]              = [  60, 12] 
WNC.DIC_domains_common_para["time_step"]["ARR_TYPE"]           = "N"
WNC.DIC_domains_common_para["use_adaptive_time_step"]["VALUE"] = True 

WNC.DIC_time_control_common_para["interval_seconds"]["VALUE"] = Tools.run_time_cal(arrIntervalHour)["MINUTES"] 

WNC.DIC_physics_common_para["mp_physics"]["VALUE"]         = [ 7, 7 ]
WNC.DIC_physics_common_para["cu_physics"]["VALUE"]         = [ 0 , 0 ]
WNC.DIC_physics_common_para["bl_pbl_physics"]["VALUE"]     = [ 6, 6 ]
WNC.DIC_physics_common_para["ra_sw_physics"]["VALUE"]      = [ 5, 5 ] 
WNC.DIC_physics_common_para["ra_lw_physics"]["VALUE"]      = [ 5, 5 ]
WNC.DIC_physics_common_para["sf_sfclay_physics"]["VALUE"]  = [ 1, 1 ]
WNC.DIC_physics_common_para["sf_surface_physics"]["VALUE"] = [ 2, 2 ]



##########################
# Preparing the exec
##########################

RUN_EXE = RUN_EXECS()
RUN_EXE.strFolder_WPS = DIR_WPS
RUN_EXE.strFolder_WRF = DIR_WRF

# Execute geogrid.exe 
if args.if_exec_wps_geogrid:
    WNC.create_wps_namelist(DIR_WPS)
    RUN_EXE.run_geogrid()

# Execute the link of grib input
if args.if_link_grib:

    arrGFS_Files = []
    WNC.STR_DIR  = DIR_WPS
    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)

#Execute ungrib.exe for ecmwf-era5
if args.if_exec_wps_ungrib and args.str_input_dataset == 'ECMWF':
    
    numFiles       = int( Tools.run_time_cal(arrRunTimeIn)["HOURS"] /
                          Tools.run_time_cal(arrIntervalHour)["HOURS"] ) + 1

    arrECMWF_Files = []
    for n in range(numFiles):
        arrIntervalHourIn = [ 0,0,0, arrIntervalHour[3] * n,0,0 ]
        arrDateTimeIn = Tools.calendar_cal(arrStartDateIn, arrIntervalHourIn  )
        strFullDate   = "{0:04d}{1:02d}{2:02d}{3:02d}".format(arrDateTimeIn[0],
                                                              arrDateTimeIn[1],
                                                              arrDateTimeIn[2],
                                                              arrDateTimeIn[3])
        arrECMWF_Files.append("{0:s}/{1:04d}/{2:02d}/{3:s}_ml.grb".format(DIR_ECMWF,
                                                                      arrDateTimeIn[0],
                                                                      arrDateTimeIn[1],
                                                                      strFullDate))

    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)
    RUN_EXE.strTargetVtableName = 'Vtable.ECMWF.ml.grib2' 
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_ML'
    WNC.DIC_metgrid_common_para["fg_name"]["VALUE"] = ["ECMWF_ML','ECMWF_SFC','PRES"]
    WNC.create_wps_namelist(DIR_WPS)
    RUN_EXE.run_ungrib()

    arrECMWF_Files = []
    for n in range(numFiles):
        arrIntervalHourIn = [ 0,0,0, arrIntervalHour[3] * n,0,0 ]
        arrDateTimeIn = Tools.calendar_cal(arrStartDateIn, arrIntervalHourIn   )
        print(arrDateTimeIn)
        strFullDate   = "{0:04d}{1:02d}{2:02d}{3:02d}".format(arrDateTimeIn[0],
                                                              arrDateTimeIn[1],
                                                              arrDateTimeIn[2],
                                                              arrDateTimeIn[3])
        arrECMWF_Files.append("{0:s}/{1:04d}/{2:02d}/{3:s}_sf.grb".format(DIR_ECMWF,
                                                                      arrDateTimeIn[0],
                                                                      arrDateTimeIn[1],
                                                                      strFullDate))
    RUN_EXE.link_ungrib(arrFiles=arrECMWF_Files)
    RUN_EXE.strTargetVtableName = 'Vtable.ERA-interim.ml' 
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_SFC'
    WNC.DIC_metgrid_common_para["fg_name"]["VALUE"] = ["ECMWF_ML','ECMWF_SFC','PRES"]
    WNC.create_wps_namelist(DIR_WPS)
    RUN_EXE.run_ungrib()

    #WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_SFC'
    #WNC.create_wps_namelist(DIR_WPS)
    RUN_EXE.run_calc_ecmwf_p()

# Running the metgrid

if args.if_exec_wps_metgrid and args.str_input_dataset == 'ECMWF':
    WNC.DIC_ungrib_common_para["prefix"]["VALUE"] = 'ECMWF_SFC'
    WNC.DIC_metgrid_common_para["fg_name"]["VALUE"] = ["ECMWF_ML','ECMWF_SFC','PRES"]
    WNC.create_wps_namelist(DIR_WPS)
    RUN_EXE.run_metgrid()

if args.if_exec_wrf_real:
    WNC.create_wrf_namelist(STR_WRF_DIR = DIR_RUN)
    RUN_EXE.run_real()

if args.if_exec_wrf_wrf: 
    WNC.create_wrf_namelist(STR_WRF_DIR = DIR_RUN)
    RUN_EXE.run_wrf() 

if args.if_namelist_wrf: 
    WNC.create_wrf_namelist(STR_WRF_DIR = DIR_RUN)

