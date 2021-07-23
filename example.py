#!/usr/bin/python
import WRF_NAMELIST_CREATOR as WNC
from WRF_NAMELIST_CREATOR import namelist_checker as NLC
NCC = WNC.namelist_creater("namelist.input", STR_DIR='./')

NCC.NUM_MAX_DOM     = 2

NCC.read_user_specific(ARR_run_time_in   =  [   0, 0, 0, 72, 0, 0],\
                       ARR_start_time_in =  [2021, 7, 14, 0, 0, 0],\
                       ARR_end_time_in   =  [2021, 7, 12, 0, 0, 0] )
NCC.DIC_user["e_we"]             ["VALUE"] = [128, 372, 158 ]
NCC.DIC_user["e_sn"]             ["VALUE"] = [128, 372, 158 ]
NCC.DIC_user["dy"               ]["VALUE"] = [12000, 3000, 1000    ]
NCC.DIC_user["dx"               ]["VALUE"] = [12000, 3000, 1000    ]
NCC.DIC_user["i_parent_start"   ]["VALUE"] = [  1,  40,  26 ]
NCC.DIC_user["j_parent_start"   ]["VALUE"] = [  1,  40,  26 ]
NCC.DIC_user["parent_grid_ratio"]["VALUE"] = [  1,   3,   3 ]
NCC.DIC_domains_common_para["num_metgrid_levels"]["VALUE"]    = 138  # ECMWF
NCC.DIC_domains_common_para["interp_type"]["VALUE"]           = 1  # ECMWF
NCC.DIC_domains_common_para["sfcp_to_sfcp"]["VALUE"]          = False
NCC.DIC_time_control_common_para["restart"]["VALUE"]          = False
NCC.DIC_time_control_common_para["restart_interval"]["VALUE"] = 24*60               
NCC.DIC_time_control_common_para["override_restart_timers"]["VALUE"] = True

NCC.DIC_time_control_common_para["interval_seconds"]["VALUE"]  = 10800

NCC.DIC_dynamics_common_para['non_hydrostatic']["VALUE"] = True 
NCC.DIC_physics_common_para["mp_physics"]["VALUE"]         = 6
NCC.DIC_physics_common_para["cu_physics"]["VALUE"]         = [ 6, 0 ] 

NCC.DIC_physics_common_para["bl_pbl_physics"]["VALUE"]     = 5


NCC.DIC_physics_common_para["ra_sw_physics"]["VALUE"]      = 5
NCC.DIC_physics_common_para["ra_lw_physics"]["VALUE"]      = 5
NCC.DIC_physics_common_para["sf_sfclay_physics"]["VALUE"]  = \
        NLC.DIC_BL_PBL_PHYSICS["5"]["ARR_SFCLAY"][0]
NCC.DIC_physics_common_para["sf_surface_physics"]["VALUE"] = 1

NCC.create_a_namelist()



