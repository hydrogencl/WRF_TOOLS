import re,os
from  WRF_TOOLS import NamelistCreater as WNC
from  WRF_TOOLS import Executors as RUN_EXECS
from  WRF_TOOLS import Tools 

from WRF_TOOLS import NamelistInformation as NameIn

import LightweightEnsembleFramework as LEF

from  subprocess import run
import argparse

###############
# Parsers
###############

parser = argparse.ArgumentParser(description='Reading input date')

parser.add_argument("-wg","--wps-geogrid", action='store_true', 
                    dest='if_exec_wps_geogrid', default=False, help='if the script execute the geogrid.exe')
parser.add_argument("-wu","--wps-ungrib",  action='store_true', 
                    dest='if_exec_wps_ungrib' , default=False, help='if the script execute the ungrib.exe ')
parser.add_argument("-wm","--wps-metgrid", action='store_true', 
                    dest='if_exec_wps_metgrid', default=False, help='if the script execute the metgrid.exe')

parser.add_argument("-lg","--link_grib",   action='store_true', 
                    dest='if_link_grib'       , default=False, help='if link the gribecute the ungrib.exe ')
parser.add_argument("-r","--wrf-real", action='store_true', 
                    dest='if_exec_wrf_real', default=False, help='if the script execute the real.exe')
parser.add_argument("-w","--wrf-wrf",  action='store_true', 
                    dest='if_exec_wrf_wrf' , default=False, help='if the script execute the wrf.exe ')
parser.add_argument("-nlw","--namelist-wrf",  action='store_true', 
                    dest='if_namelist_wrf' , default=False, help='if the script only create the namelist.input')
parser.add_argument("-ew","--ensemble-wrf",  action='store_true', 
                    dest='if_ensemble_wrf' , default=False, help='if the script execute the wrf.exe ')

parser.add_argument("-id","--input-data-set", type=str, 
                    dest='str_input_dataset'    , default='ECMWF', help='The choosing dataset, default: ECMWF ')

args = parser.parse_args()

###############
#   Namelist
###############

WNC = WNC()
WNC.debug = True

arrStartDateIn = [2015,  8,  6, 0, 0, 0]
arrEndDateIn   = [2015,  8,  9, 0, 0, 0]

arrRunTimeIn   = [ arrEndDateIn[i] - arrStartDateIn[i] for i in range(6)]
arrRunTime     = [0,0,0, Tools.run_time_cal(arrRunTimeIn)["HOURS"],0,0 ]

arrIParentSta  = [    1, 158  ]
arrJParentSta  = [    1, 141  ]

numCenLat       = 25.0
numCenLon       = 140.0
numTrueLat1     = 0
numTrueLat2     = 50

numMaxDom       = 2

arrEdgesWE     = [  501, 301  ]
arrEdgesSN     = [  401, 301  ]

arrIParentSta  = [    1, 158  ]
arrJParentSta  = [    1, 141  ]

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

arrStartDate = [ Tools.make_wrf_datetime(arrStartDateIn), Tools.make_wrf_datetime(arrStartDateIn) ]
arrEndDate   = [ Tools.make_wrf_datetime(arrEndDateIn), Tools.make_wrf_datetime(arrEndDateIn) ]

# Parameters:

DIR_GEODATA="/p/project/cjiek80/ESIAS-MET/DATA/GEODATA"
DIR_GEFS   ="/gpfs/arch/jiek80/jiek8002/GEFS"
DIR_ECMWF  ="/p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib"

# Folders:

DIR_WPS    = "/p/scratch/cjiek80/jiek8010/WRFV4/WPS"
DIR_WRF    = "/p/scratch/exaww/lu3/WRFV4/WRF_MND"
DIR_RUN    = "{0:s}/.".format(DIR_WRF)
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
#     Moving Nest 
##########################

DIC_MOVING_NEST = { "0806" : {
    "move_interval"            :   [  0,   60,  120,  180,  240,  300,  360,  420,  480,  540,\
 585,  630,  675,  720,  780,  840,  900,  945,  990, 1035,\
1080, 1125, 1170, 1215, 1260, 1320, 1380, 1440, 1500, 1560,\
1620, 1680, 1740, 1800, 1860, 1920, 1980, 2040, 2100, 2160,\
2250, 2340, 2400, 2460, 2520, 2565, 2610, 2655, 2700, 2730,\
2760, 2790, 2820, 2850],
    "move_cd_x"                :   [  -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,   -1,   -1,   -1],
    "move_cd_y"                :   [ 0, 1,    0,    0,    1,    1,    0,    1,    1,    0,    1,\
   0,    0,    0,    1,    0,    0,    1,    1,    0,    0,\
   1,    0,    0,    0,    1,    1,    0,    1,    0,    0,\
   1,    1,    0,    1,    1,    1,    1,    1,    0,    1,\
   1,    1,    1,    1,    1,    1,    1,    0,    1,    1,\
   0,    0,    0,    0],
    "move_id"                  :   [  2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2],
    "num_moves" : 54
},
"0808": {
    "move_id"                   : [    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2,\
   2,    2,    2,    2,    2,    2,    2,    2,    2,    2],
    "move_interval"             : [    0,   45,   90,  135,  180,  225,  270,  315,  360,  450,\
 540,  600,  660,  720,  780,  840,  900,  990, 1080, 1140,\
1200, 1260, 1320, 1380, 1440, 1530, 1620, 1710, 1800, 1860,\
1920, 1980, 2025, 2070, 2115, 2160, 2220, 2280, 2340, 2385,\
2430, 2475, 2520, 2565, 2610, 2655, 2700, 2745, 2790, 2835],
    "move_cd_x"                 : [   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
  -1,    0,    0,   -1,   -1,    0,   -1,   -1,   -1,   -1,\
   0,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,\
   0,   -1,    0,    0,    0,   -1,    0,    0,    0,    0,\
   0,    0,    1,    0,    0,    0,    1,    1,    0,    0],
    "move_cd_y"                 : [    1,    0,    0,    0,    0,    0,    0,    0,    1,    0,\
   1,    1,    1,    1,    1,    1,    1,    1,    1,    1,\
   1,    1,    1,    0,    1,    1,    1,    1,    1,    1,\
   1,    1,    1,    1,    1,    1,    1,    1,    1,    1,\
   1,    1,    1,    1,    1,    1,    1,    1,    1,    1],
    "num_moves" : 50
}}

##########################
#     WRF namelist
##########################

WNC.ARR_domains.append("zap_close_levels")
WNC.DIC_domains_common_para["zap_close_levels"] = {"VALUE": 100, 
                                                   "DATA_TYPE": "INT", "ARR_TYPE": "S"}
WNC.ARR_domains.append("smooth_cg_topo")
WNC.DIC_domains_common_para["smooth_cg_topo"] = {"VALUE": False, 
                                                 "DATA_TYPE": "BLN", "ARR_TYPE": "S"}



WNC.DIC_domains_common_para["num_metgrid_levels"]["VALUE"]    = 138  # ECMWF
WNC.DIC_domains_common_para["interp_type"]["VALUE"]           = 1  # ECMWF
WNC.DIC_domains_common_para["sfcp_to_sfcp"]["VALUE"]          = False


WNC.DIC_time_control_common_para["override_restart_timers"]["VALUE"] = True
WNC.DIC_time_control_common_para["history_interval"]["VALUE"] = 15
WNC.DIC_time_control_common_para["history_outname"]["STR_FMT"] = "\'{0:s}_d<domain>{2:s}{1:s}\',"
WNC.DIC_time_control_common_para["restart_interval"]["VALUE"] = 1440
WNC.DIC_time_control_common_para["interval_seconds"]["VALUE"] = 10800

arr_new = ["auxhist3_outname","io_form_auxhist3", "frames_per_auxhist3",\
           "auxhist3_interval", "iofields_filename"]

for item in arr_new:
    WNC.ARR_time_control.append(item)
                           
WNC.DIC_time_control_common_para["history_outname"] = \
    { "VALUE": "wrfout", "DATA_TYPE": "STR", "ARR_TYPE": "S", \
      "STR_FMT": "\'{0:s}.d<domain>{2:s}{1:s}.<date>\'," }

WNC.DIC_time_control_common_para["auxhist3_outname"] = \
    { "VALUE": "gw_out", "DATA_TYPE": "STR", "ARR_TYPE": "S", \
      "STR_FMT": "\'{0:s}.d<domain>{2:s}{1:s}.<date>\'," }

WNC.DIC_time_control_common_para["io_form_auxhist3"] = \
    { "VALUE": 2, "DATA_TYPE": "INT", "ARR_TYPE": "S" }

WNC.DIC_time_control_common_para["frames_per_auxhist3"] = \
    { "VALUE": 1000, "DATA_TYPE": "INT", "ARR_TYPE": "M" }

WNC.DIC_time_control_common_para["auxhist3_interval"] = \
    { "VALUE": 6, "DATA_TYPE": "INT", "ARR_TYPE": "M" }

WNC.DIC_time_control_common_para["iofields_filename"] = \
    { "VALUE": "outlist.txt", "DATA_TYPE": "STR", "ARR_TYPE": "M" }

WNC.DIC_domains_common_para["time_step"]["VALUE"]              =   18      
WNC.DIC_domains_common_para["time_step_fract_den"]["VALUE"]    =   10      
WNC.DIC_domains_common_para["use_adaptive_time_step"]["VALUE"] = False
WNC.DIC_domains_common_para["e_vert"]["VALUE"]                 =  120
WNC.DIC_domains_common_para["p_top_requested"]["VALUE"]        =   10

WNC.DIC_domains_common_para["max_step_increase_pct"]["VALUE"]  = [   5, 51 ]
WNC.DIC_domains_common_para["starting_time_step"]["VALUE"]     = [  -1, -1 ]
WNC.DIC_domains_common_para["max_time_step"]["VALUE"]          = [  -1, -1 ]

WNC.DIC_physics_common_para["mp_physics"]["VALUE"]         = 7
WNC.DIC_physics_common_para["cu_physics"]["VALUE"]         = [ 5 , 0  ]
WNC.DIC_physics_common_para["bl_pbl_physics"]["VALUE"]     = 6 
WNC.DIC_physics_common_para["ra_sw_physics"]["VALUE"]      = 4 
WNC.DIC_physics_common_para["ra_lw_physics"]["VALUE"]      = 4 
WNC.DIC_physics_common_para["sf_sfclay_physics"]["VALUE"]  = 1 
WNC.DIC_physics_common_para["sf_surface_physics"]["VALUE"] = 2

WNC.ARR_physics.append("o3input")
WNC.DIC_physics_common_para["o3input"] = {"VALUE" : 0, "DATA_TYPE": "INT", "ARR_TYPE": "S"}

WNC.ARR_dynamics = ['w_damping', 'diff_opt', 'km_opt', 'diff_6th_opt', 'diff_6th_factor',\
                    'time_step_sound', 'base_temp', 'damp_opt', 'dampcoef', 'zdamp', \
                    'khdif', 'kvdif',\
                    'non_hydrostatic', 'moist_adv_opt', 'scalar_adv_opt',"epssm"]

WNC.DIC_dynamics_common_para["zdamp"] = {"VALUE":  5000,"DATA_TYPE": "INT", "ARR_TYPE": "M" }
WNC.DIC_dynamics_common_para["epssm"] = {"VALUE":  0.2,"DATA_TYPE": "FLT", "ARR_TYPE": "M" }

WNC.DIC_bdy_control_common_para["spec_bdy_width"]["VALUE"] = 1

##########################
# Preparing the sensitivity dict
##########################

ARR_PhySet = []
for mp in [6]:
    for pbl in [1,2,3,7,8]:
        ARR_PhySet.append(
                {"MP"  : mp,
                 "PBL" : pbl
                })

if args.if_namelist_wrf: 
    WNC.DIC_dynamics_common_para["damp_opt"]["VALUE"]     =      3
    WNC.DIC_bdy_control_common_para["specified"]["VALUE"] = [ True, True  ]
    WNC.DIC_bdy_control_common_para["nested"]["VALUE"]    = [ True, True  ]
    for ind, dicIn in enumerate(ARR_PhySet):
        WNC.STR_wrf_namelist = "run_mod_{0:03d}/namelist.input.real".format(ind+1)
        arrRunTime     = [0,0,0, 72,0,0 ]
        WNC.read_user_specific(run_time      = arrRunTime,
                               start_time    = [ 2015, 8, 6, 0, 0, 0 ], 
                               end_time      = [ 2015, 8, 9, 0, 0, 0 ], 
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
        print("working on the files: {0:s}".format(WNC.STR_wrf_namelist))
        WNC.DIC_time_control_common_para["restart"]["VALUE"] = False
        WNC.DIC_physics_common_para["mp_physics"]["VALUE"]         = dicIn["MP"] 
        WNC.DIC_physics_common_para["bl_pbl_physics"]["VALUE"]     = dicIn["PBL"]
        WNC.DIC_physics_common_para["sf_sfclay_physics"]["VALUE"]  = \
                NameIn.DIC_BL_PBL_PHYSICS[str(dicIn["PBL"])]["OPT_SFCLAY"][0]
        WNC.create_wrf_namelist(STR_DIR = DIR_RUN)

        for item in ["num_moves", "move_interval", "move_cd_x", "move_cd_y", "move_id"]:
            WNC.ARR_domains.append(item)

        strDate = "0806"
        arrRunTime     = [0,0,0, 48,0,0 ]
        WNC.read_user_specific(run_time      = arrRunTime,
                               start_time    = [ 2015, 8, 6, 0, 0, 0 ], 
                               end_time      = [ 2015, 8, 8, 0, 0, 0 ], 
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
        WNC.STR_wrf_namelist = "run_mod_{0:03d}/namelist.input.hf.{1:s}".format(ind+1, strDate)
        WNC.DIC_time_control_common_para["restart"]["VALUE"] = False
        WNC.DIC_domains_common_para["num_moves"] = {"VALUE": DIC_MOVING_NEST[strDate]["num_moves"],
                                                    "DATA_TYPE": "INT", "ARR_TYPE": "S"}
        for item in ["move_interval", "move_cd_x", "move_cd_y", "move_id"]:
            WNC.DIC_domains_common_para[item] = {"VALUE": DIC_MOVING_NEST[strDate][item] ,
                                                 "DATA_TYPE": "INT", "ARR_TYPE": "N"}
        WNC.create_wrf_namelist(STR_DIR = DIR_RUN)

        strDate = "0808"

        arrRunTime     = [0,0,0, 24,0,0 ]
        WNC.read_user_specific(run_time      = arrRunTime,
                               start_time    = [ 2015, 8, 8, 0, 0, 0 ], 
                               end_time      = [ 2015, 8, 9, 0, 0, 0 ], 
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
        WNC.STR_wrf_namelist = "run_mod_{0:03d}/namelist.input.hf.{1:s}".format(ind+1, strDate)
        WNC.DIC_time_control_common_para["restart"]["VALUE"] =True
        WNC.DIC_domains_common_para["num_moves"] = {"VALUE": DIC_MOVING_NEST[strDate]["num_moves"], 
                                                    "DATA_TYPE": "INT", "ARR_TYPE": "S"}
        for item in ["move_interval", "move_cd_x", "move_cd_y", "move_id"]:
            WNC.DIC_domains_common_para[item] = {"VALUE": DIC_MOVING_NEST[strDate][item] ,
                                             "DATA_TYPE": "INT", "ARR_TYPE": "N"}
        WNC.create_wrf_namelist(STR_DIR = DIR_RUN)


if args.if_ensemble_wrf:
    SC = LEF.SlurmController(
            strProject      = "Test",
            strPartition    = "devel",
            numCoresPerNode = 48,
            strJobname      = "TestFEL",
            strRootdir      = "/p/scratch/cjiek80/jiek8010/WRFV4/WRF",
            ifServerLog     = True
            )
    SC.InitEnsemble(members=4, UsingNodes=1)
    print(SC.corespermember)
    print(SC.arr_hostpermember) 
    SC.CreateMembers()

    # Remove the 
    SC.FileControl("./wrfout_d01","remove")
    SC.FileControl("./wrfout_d02","remove")
    SC.FileControl("./gw_d01","remove")
    SC.FileControl("./gw_d01","remove")

    # run all the executor with the member
    SC.RunMembers("wrf.exe")

    # To keep this Server alive 
    SC.CheckMembersWRF()


