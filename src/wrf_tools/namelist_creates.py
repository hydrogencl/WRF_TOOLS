#!/usr/bin/python
import math, re, os
from subprocess import run
"""
This main program body contains following:

    3) NamelistCreator:
        The namelist creater is used to create the namelists for WRF and 
        WPS. The program is very flexible and thus any namelist can be 
        modified due to different usage or systems. 

"""

class Namelist_creator:
    """ 

    """
    # Important Parameters
    # Time control :
    # Format: YYYY MM DD hh mm ss

    # Domains:

    # Ensembles:
    NUM_ensemble_member       = 0
    NUM_input_ensemble_member = 0
    IF_ensemble_run           = False
    # Others:
    STR_DIR="./"

    def __init__(self, STR_wrf_namelist="namelist.input", STR_wps_namelist="namelist.wps", STR_DIR="./", debug_in = False):
        print("Start the namelist creator by Python")
        print("    Author: Y.-S. Lu                ")
        print("    First Edition: 24.04.2020       ")
        print("              ... during COVID-19   ")

        # ENSEMBLE SETTING UP
        self.IF_SPPT  = False
        self.IF_SKEBS = False
        self.STR_connect_symbol = "_"
        self.debug    = debug_in
        # FILENAME

        self.STR_wrf_namelist = STR_wrf_namelist
        self.STR_wps_namelist = STR_wps_namelist
        self.STR_DIR          = STR_DIR

        # ARR of press_pa
        self.ARR_press_pa = [ 201300, 200100, 100000, 95000, 90000, 85000, 80000, 75000, \
                               70000,  65000,  60000, 55000, 50000, 45000, 40000, 35000, \
                               30000,  25000,  20000, 15000, 10000,  5000,  1000 ]

        self.ARR_wps_share_all   = ["wrf_core","max_dom","start_date","end_date","interval_seconds","active_grid","subgrid_ratio_x","subgrid_ratio_y","io_form_geogrid","opt_output_from_geogrid_path","debug_level","start_date","end_date","start_year","start_month","start_day","start_hour","start_minute","start_second","end_year","end_month","end_day","end_hour","end_minute","end_second"]

        self.ARR_wps_geogrid_all =  ["parent_id","parent_grid_ratio","i_parent_start","j_parent_start","s_we","e_we","s_sn","e_sn","geog_data_res","dx","dy","map_proj","ref_lat","ref_lon","ref_x","ref_y","truelat1","truelat2","stand_lon","geog_data_path","opt_geogrid_tbl_path","geog_data_res","geog_data_res"]

        self.ARR_ungrib_all      = ["out_format","prefix","ec_rec_len","pmin"]

        self.ARR_metgrid_all     = ["fg_name", "constants_name", "io_form_metgrid", "opt_output_from_metgrid_path", "opt_metgrid_tbl_path", "process_only_bdy"]

        self.ARR_mod_levs_all    = ["press_pa"]

        self.ARR_plotfmt_all     = ["ix","jx","ioff","joff"]

        self.ARR_share           = [ "wrf_core",            "max_dom",     "start_date",       "end_date",\
                                     "interval_seconds","active_grid","subgrid_ratio_x","subgrid_ratio_y",\
                                     "io_form_geogrid", "opt_output_from_geogrid_path"]

        self.ARR_geogrid         = [ "parent_id", "parent_grid_ratio", "i_parent_start", "j_parent_start",\
                                     "e_we", "e_sn","geog_data_res","dx","dy",\
                                     "map_proj","ref_lat","ref_lon",\
                                     "truelat1","truelat2","stand_lon","geog_data_path","geog_data_res"]

        self.ARR_ungrib          = ["out_format", "prefix"]

        self.ARR_metgrid         = ["fg_name"   , "io_form_metgrid"]

        self.ARR_mod_levs        = ["press_pa"]

        self.ARR_plotfmt         = ["ix","jx","ioff","joff"]

        # ARR of WRFs

        self.ARR_time_control = ['run_days', 'run_hours', 'run_minutes', 'run_seconds', 'start_year', 'start_month', 'start_day', 'start_hour', 'start_minute', 'start_second', 'end_year', 'end_month', 'end_day', 'end_hour', 'end_minute', 'end_second', 'interval_seconds', 'input_from_file', 'history_interval', 'history_outname', 'bdy_inname', 'input_inname', 'frames_per_outfile', 'auxhist1_outname', 'auxhist2_outname', 'auxhist1_interval', 'auxhist2_interval', 'frames_per_auxhist1', 'frames_per_auxhist2', 'aux1_time', 'aux2_time', 'interpolation_time', 'interpolation_number', 'restart', 'restart_interval', 'override_restart_timers', 'io_form_history', 'io_form_restart', 'io_form_input', 'io_form_boundary', 'debug_level', 'io_form_auxinput2', 'io_form_auxhist1', 'io_form_auxhist2', 'auxinput1_inname']

        self.ARR_domains     = ['time_step', 'time_step_fract_num', 'time_step_fract_den', 'max_dom', 'e_we', 'e_sn', 'e_vert', 'p_top_requested', 'num_metgrid_levels', 'num_metgrid_soil_levels', 'dx', 'dy', 'grid_id', 'parent_id', 'i_parent_start', 'j_parent_start', 'parent_grid_ratio', 'feedback', 'use_adaptive_time_step', 'step_to_output_time', 'target_cfl', 'max_step_increase_pct', 'starting_time_step', 'max_time_step', 'min_time_step', 'adaptation_domain', 'interp_type', 'smooth_option', 'sfcp_to_sfcp']

        self.ARR_physics     = ['mp_physics', 'ra_lw_physics', 'ra_sw_physics', 'sf_sfclay_physics', 'sf_surface_physics', 'bl_pbl_physics', 'cu_physics', 'radt', 'bldt', 'cudt', 'isftcflx', 'isfflx', 'ifsnow', 'icloud', 'surface_input_source', 'num_soil_layers', 'sf_urban_physics', 'maxiens', 'maxens', 'maxens2', 'maxens3', 'ensdim', 'topo_wind', 'num_land_cat', 'ysu_st']

        self.ARR_dynamics    = ['w_damping', 'diff_opt', 'km_opt', 'diff_6th_opt', 'diff_6th_factor', 'time_step_sound', 'base_temp', 'damp_opt', 'dampcoef', 'khdif', 'kvdif', 'non_hydrostatic', 'moist_adv_opt', 'scalar_adv_opt']

        self.ARR_bdy_control = ['spec_bdy_width', 'spec_zone', 'relax_zone', 'specified', 'nested']
        
        self.ARR_namelist_quilt = ['nio_tasks_per_group', 'nio_groups']

        self.ARR_stoch_skebs = ['skebs', 'stoch_vertstruc_opt', 'tot_backscat_psi', 'tot_backscat_t', 'ztau_psi', 'ztau_t', 'nens', 'ISEED_SKEBS']

        self.ARR_stoch_sppt  = ['sppt', 'nens', 'timescale_sppt', 'gridpt_stddev_sppt', 'ISEED_SPPT']

        # WPS NAMELISTS:
        # Share:
        self.DIC_share_common_para = {\
            "wrf_core"                         : {"VALUE":   "ARW"          , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "max_dom"                          : {"VALUE":   0              , "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "interval_seconds"                 : {"VALUE":   10800          , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "active_grid"                      : {"VALUE":   True           , "DATA_TYPE": "BLN", "ARR_TYPE" :"M"   },
            "subgrid_ratio_x"                  : {"VALUE":   1              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "subgrid_ratio_y"                  : {"VALUE":   1              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "io_form_geogrid"                  : {"VALUE":   2              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "opt_output_from_geogrid_path"     : {"VALUE":   "./"           , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "debug_level"                      : {"VALUE":   0              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "start_date"                       : {"VALUE":  ["2006-08-16_12:00:00", "2006-08-16_12:00:00"],\
                                                                              "DATA_TYPE": "STR", "ARR_TYPE" :"M",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "end_date"                         : {"VALUE":  ["2006-08-16_18:00:00", "2006-08-16_18:00:00"],\
                                                                              "DATA_TYPE": "STR", "ARR_TYPE" :"M",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "start_year"                       : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "start_month"                      : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "start_day"                        : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "start_hour"                       : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "start_minute"                     : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "start_second"                     : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_year"                         : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_month"                        : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_day"                          : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_hour"                         : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_minute"                       : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "end_second"                       : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   }}

        # Geogrid
        self.DIC_geogrid_common_para = {\
            "parent_id"                        : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "parent_grid_ratio"                : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "i_parent_start"                   : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "j_parent_start"                   : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "s_we"                             : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "e_we"                             : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "s_sn"                             : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "e_sn"                             : {"VALUE":  [ 0, 0         ], "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "geog_data_res"                    : {"VALUE":  ['modis_30s+2m','modis_30s','modis_30s']   ,\
                                                                              "DATA_TYPE": "STR", "ARR_TYPE" :"M",\
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "dx"                               : {"VALUE":  15000           , "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "dy"                               : {"VALUE":  15000           , "DATA_TYPE": "INT", "ARR_TYPE" :"P"   },
            "map_proj"                         : {"VALUE":  'lambert'       , "DATA_TYPE": "STR", "ARR_TYPE" :"S"   ,\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "ref_lat"                          : {"VALUE":  45              , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "ref_lon"                          : {"VALUE":  8.5             , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "ref_x"                            : {"VALUE":  45              , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "ref_y"                            : {"VALUE":  8.5             , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "truelat1"                         : {"VALUE":  30.0            , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "truelat2"                         : {"VALUE":  60.0            , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "stand_lon"                        : {"VALUE":   8.5            , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   },
            "geog_data_path"                   : {"VALUE": '/path/to/geo'   , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "opt_geogrid_tbl_path"             : {"VALUE": 'geogrid'       ,  "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"},
            "geog_data_res"                    : {"VALUE": ['usgs_lakes+10m','usgs_lakes+2m']   ,\
                                                                              "DATA_TYPE": "STR", "ARR_TYPE" :"M",\
                                                                              "STR_FMT" : "\'{0:s}\',"}}

        # Ungrib
        self.DIC_ungrib_common_para = {\
            "out_format"                       : {"VALUE": "WPS"            , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "prefix"                           : {"VALUE": "FILE"           , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "ec_rec_len"                       : {"VALUE": 26214508         , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "pmin"                             : {"VALUE": 100              , "DATA_TYPE": "FLT", "ARR_TYPE" :"S"   }}

        # Metgrid
        self.DIC_metgrid_common_para = {\
            "fg_name"                          : {"VALUE": ["FILE"]         , "DATA_TYPE": "STR", "ARR_TYPE" :"N",\
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "constants_name"                   : {"VALUE": "./TAVGSFC"      , "DATA_TYPE": "STR", "ARR_TYPE" :"S",\
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "io_form_metgrid"                  : {"VALUE": 2                , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "opt_output_from_metgrid_path"     : {"VALUE": "./"             , "DATA_TYPE": "STR", "ARR_TYPE" :"S"   ,
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "opt_metgrid_tbl_path"             : {"VALUE": "metgrid/"       , "DATA_TYPE": "STR", "ARR_TYPE" :"S"   ,
                                                                              "STR_FMT" : "\'{0:s}\',"              },
            "process_only_bdy"                 : {"VALUE": 5                , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   }}

        # mod_levs
        self.DIC_mod_levs_common_para = {\
            "press_pa"                         : {"VALUE": self.ARR_press_pa, "DATA_TYPE": "FLT", "ARR_TYPE" :"M"   }}

        # Plotfmt
        self.DIC_plotfmt_common_para = {\
            "ix"                               : {"VALUE": 100              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "jx"                               : {"VALUE": 100              , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "ioff"                             : {"VALUE": 30               , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   },
            "joff"                             : {"VALUE": 30               , "DATA_TYPE": "INT", "ARR_TYPE" :"S"   }}

        # WRF NAMELIST:
        # Time_Control common parameters:
        self.DIC_time_control_common_para = {\
            "run_days"                         : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "run_hours"                        : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "run_minutes"                      : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "run_seconds"                      : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_year"                       : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_month"                      : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_day"                        : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_hour"                       : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_minute"                     : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "start_second"                     : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_year"                         : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_month"                        : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_day"                          : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_hour"                         : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_minute"                       : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "end_second"                       : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "interval_seconds"                 : { "VALUE":  10800       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "input_from_file"                  : { "VALUE":  True        , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"M"},
            "history_interval"                 : { "VALUE":  60          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "history_outname"                  : { "VALUE":  'wrfout'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
            "bdy_inname"                       : { "VALUE":  'wrfbdy'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}{1:s}_d<domain>\',"},
            "input_inname"                     : { "VALUE":  'wrfinput'    , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}{1:s}_d<domain>\',"},
            "rst_outname"                      : { "VALUE":  'wrfrst'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
            "rst_inname"                       : { "VALUE":  'wrfrst'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
            "frames_per_outfile"               : { "VALUE":  1000          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "auxhist1_outname"                 : { "VALUE":  'auxhist1'    , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
            "auxhist2_outname"                 : { "VALUE":  'meteofrance' , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
            "auxhist1_interval"                : { "VALUE":  15          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "auxhist2_interval"                : { "VALUE":  60          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "frames_per_auxhist1"              : { "VALUE":  1000        , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "frames_per_auxhist2"              : { "VALUE":  1000        , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "aux1_time"                        : { "VALUE":  15          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "aux2_time"                        : { "VALUE":  60          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "interpolation_time"               : { "VALUE":  10          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "interpolation_number"             : { "VALUE":  8           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "restart"                          : { "VALUE":  False       , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
            "override_restart_timers"          : { "VALUE":  False       , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
            "restart_interval"                 : { "VALUE":  50000       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_history"                  : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_restart"                  : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_input"                    : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_boundary"                 : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "debug_level"                      : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_auxinput2"                : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_auxhist1"                 : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "io_form_auxhist2"                 : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "auxinput1_inname"                 : { "VALUE":  'met_em'    , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S",\
                                                   "STR_FMT" : "\'{0:s}{2:s}.d<domain>.<date>\',"}}

        # Domain Common Parameters:
        self.DIC_domains_common_para= {\
            "time_step"                        : { "VALUE":  20          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "time_step_fract_num"              : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "time_step_fract_den"              : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "max_dom"                          : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "e_we"                             : { "VALUE":  180         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "e_sn"                             : { "VALUE":  180         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "e_vert"                           : { "VALUE":  50          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "p_top_requested"                  : { "VALUE":  5000        , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "num_metgrid_levels"               : { "VALUE":  42          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "num_metgrid_soil_levels"          : { "VALUE":  4           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "dx"                               : { "VALUE":  20000       , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"P"},
            "dy"                               : { "VALUE":  20000       , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"P"},
            "grid_id"                          : { "VALUE":  [1,1]       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "parent_id"                        : { "VALUE":  [1,1]       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "i_parent_start"                   : { "VALUE":  [1,1]       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "j_parent_start"                   : { "VALUE":  [100,100]   , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "parent_grid_ratio"                : { "VALUE":  [1,3]       , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
            "feedback"                         : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "use_adaptive_time_step"           : { "VALUE":  True        , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
            "step_to_output_time"              : { "VALUE":  False       , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
            "target_cfl"                       : { "VALUE":  1.2         , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"M"},
            "max_step_increase_pct"            : { "VALUE":  5           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "starting_time_step"               : { "VALUE":  20          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "max_time_step"                    : { "VALUE":  100         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "min_time_step"                    : { "VALUE":  -1          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "interp_type"                      : { "VALUE":  2           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "adaptation_domain"                : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "smooth_option"                    : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "sfcp_to_sfcp"                     : { "VALUE":  False       , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"}}

        # PHYSICS
        self.DIC_physics_common_para = {\
            "mp_physics"                       : { "VALUE":  6           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "ra_lw_physics"                    : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "ra_sw_physics"                    : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "sf_sfclay_physics"                : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "sf_surface_physics"               : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "bl_pbl_physics"                   : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "cu_physics"                       : { "VALUE":  [  1,  0 ]  , "DATA_TYPE" : "INT" , "ARR_TYPE" :"A"},
            "radt"                             : { "VALUE":  [ 20,  6 ]  , "DATA_TYPE" : "INT" , "ARR_TYPE" :"A"},
            "bldt"                             : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "cudt"                             : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "isftcflx"                         : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "isfflx"                           : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ifsnow"                           : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "icloud"                           : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "surface_input_source"             : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "num_soil_layers"                  : { "VALUE":  5           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "sf_urban_physics"                 : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "maxiens"                          : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "maxens"                           : { "VALUE":  3           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "maxens2"                          : { "VALUE":  3           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "maxens3"                          : { "VALUE":  16          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ensdim"                           : { "VALUE":  144         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "topo_wind"                        : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "num_land_cat"                     : { "VALUE":  20          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "hail_opt"                         : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ysu_st"                           : { "VALUE":  0.25        , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"S"}}

        #       DYNAMICS 
        self.DIC_dynamics_common_para = {\
            "w_damping"                        : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "diff_opt"                         : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "km_opt"                           : { "VALUE":  4           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "diff_6th_opt"                     : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "diff_6th_factor"                  : { "VALUE":  0.12        , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"M"},
            "time_step_sound"                  : { "VALUE":  6           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "base_temp"                        : { "VALUE":  290.        , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"S"},
            "damp_opt"                         : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "dampcoef"                         : { "VALUE":  0.2         , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"S"},
            "khdif"                            : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "kvdif"                            : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "non_hydrostatic"                  : { "VALUE":  True        , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"M"},
            "moist_adv_opt"                    : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
            "scalar_adv_opt"                   : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"}}

        #       BDY_CONTROL
        self.DIC_bdy_control_common_para = {\
            "spec_bdy_width"                   : { "VALUE":  5             , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "spec_zone"                        : { "VALUE":  1             , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "relax_zone"                       : { "VALUE":  4             , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "specified"                        : { "VALUE":  [True ,False] , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"A"},
            "nested"                           : { "VALUE":  [False, True] , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"A"}}

        #       NAMELIST_QUILT
        self.DIC_namelist_quilt_common_para = {\
            "nio_tasks_per_group"              : { "VALUE":  0           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "nio_groups"                       : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"}}

        #       STOCK: SKEB   
        self.DIC_stoch_skebs_common_para = {\
            "skebs"                            : { "VALUE":      1      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "stoch_vertstruc_opt"              : { "VALUE":      0      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "tot_backscat_psi"                 : { "VALUE": 1.0E-5      , "DATA_TYPE" : "SCI" , "ARR_TYPE" :"S"},
            "tot_backscat_t"                   : { "VALUE": 1.0E-6      , "DATA_TYPE" : "SCI" , "ARR_TYPE" :"S"},
            "ztau_psi"                         : { "VALUE":  10800      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ztau_t"                           : { "VALUE":  10800      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "nens"                             : { "VALUE":      0      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ISEED_SKEBS"                      : { "VALUE":    100      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"}}
    
        #       STOCK: SPPT   
        self.DIC_stoch_sppt_common_para = {\
            "sppt"                             : { "VALUE":      1      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "nens"                             : { "VALUE":      0      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "ISEED_SPPT"                       : { "VALUE":    100      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "timescale_sppt"                   : { "VALUE":  21600      , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
            "gridpt_stddev_sppt"               : { "VALUE":    0.3      , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"S"}}

    def read_user_specific(self, run_time=[], start_time= [], end_time=[], max_dom=0, \
                                 e_we=[], e_sn=[], dx=15000, dy=15000,\
                                 grid_id =[], parent_id = [], \
                                 i_parent_start=[], j_parent_start=[], parent_grid_ratio=[]):
        ARR_run_time   = run_time
        ARR_start_time = start_time
        ARR_end_time   = end_time


        # Checking Date and Time based on the intervals
        ARR_END_DATE_CHK  = Tools.calendar_cal(ARR_start_time, ARR_run_time)

        if Tools.run_time_cal(ARR_END_DATE_CHK) != Tools.run_time_cal(ARR_end_time):
            ARR_end_time  = ARR_END_DATE_CHK
            print("WARNING: The end date is not match with the interval time")
            print("       : The end date is changed as:{0:04d}-{1:02d}-{2:02d}_{3:02d}:{4:02d}:{5:02d}".format(\
                    ARR_end_time[0], ARR_end_time[1],ARR_end_time[2],ARR_end_time[3],ARR_end_time[4],ARR_end_time[5]))

        if max_dom == 0 :
            NUM_MAX_DOM  = 1                
        else:
            NUM_MAX_DOM  = max_dom
        self.NUM_MAX_DOM = NUM_MAX_DOM
        self.DIC_user = {\
        "run_days"                         : {"VALUE": [ ARR_run_time[2] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d}," },\
        "run_hours"                        : {"VALUE": [ ARR_run_time[3] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "run_minutes"                      : {"VALUE": [ ARR_run_time[4] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "run_seconds"                      : {"VALUE": [ ARR_run_time[5] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "start_year"                       : {"VALUE": [ ARR_start_time[0] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "   {0:04d},"},\
        "start_month"                      : {"VALUE": [ ARR_start_time[1] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "start_day"                        : {"VALUE": [ ARR_start_time[2] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "start_hour"                       : {"VALUE": [ ARR_start_time[3] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "start_minute"                     : {"VALUE": [ ARR_start_time[4] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "start_second"                     : {"VALUE": [ ARR_start_time[5] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "end_year"                         : {"VALUE": [ ARR_end_time[0] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "   {0:04d},"},\
        "end_month"                        : {"VALUE": [ ARR_end_time[1] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "end_day"                          : {"VALUE": [ ARR_end_time[2] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "end_hour"                         : {"VALUE": [ ARR_end_time[3] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "end_minute"                       : {"VALUE": [ ARR_end_time[4] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "end_second"                       : {"VALUE": [ ARR_end_time[5] for d in range(NUM_MAX_DOM)], "DATA_TYPE": "INT","STR_FMT": "     {0:02d},"},\
        "max_dom"                     : {"VALUE":  [ NUM_MAX_DOM ]            , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "e_we"                        : {"VALUE":          e_we               , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "e_sn"                        : {"VALUE":          e_sn               , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
#        "e_vert"                      : {"VALUE": self.ARR_e_vert, "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "dx"                          : {"VALUE":        [ dx ]               , "DATA_TYPE": "INT","STR_FMT": "{0:7.3f},"},\
        "dy"                          : {"VALUE":        [ dy ]               , "DATA_TYPE": "INT","STR_FMT": "{0:7.3f},"},\
        "grid_id"                     : {"VALUE":          grid_id            , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "parent_id"                   : {"VALUE":          parent_id          , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "i_parent_start"              : {"VALUE":          i_parent_start     , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "j_parent_start"              : {"VALUE":          j_parent_start     , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        "parent_grid_ratio"           : {"VALUE":          parent_grid_ratio  , "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
#        "max_step_increase_pct"       : {"VALUE": self.ARR_max_step_increase_pct, "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
#        "starting_time_step"          : {"VALUE": self.ARR_starting_time_step, "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
#        "max_time_step"               : {"VALUE": self.ARR_max_time_step, "DATA_TYPE": "INT","STR_FMT": "{0:7d},"},\
        }
        return 0    

    def BLN2WRFSTR(self, BL_in):
        if BL_in:
            STR_out = " .true."
        else:
            STR_out = ".false."
        return STR_out

    def write_namelist(self, DIC_in, ARR_in):
        DIC_DATA_TYPE_STR = {"FLT": "{0:7.2f},","BLN": "{0:s},","INT": "{0:7d},", "SCI": "{0:1.1E}," , "STR": "\'{0:s}\'," }
        for ARR_item in ARR_in :
            self.FILE.write(" {0:s} = ".format(ARR_item.ljust(25, ' ')))
            if self.debug: print("Working on var: {0:s}".format(ARR_item))
            if DIC_in[ARR_item]["ARR_TYPE"] == "S":
                # the ARR_TYPE as single input number
                if DIC_in[ARR_item]["DATA_TYPE"] == "BLN":
                    self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(self.BLN2WRFSTR(DIC_in[ARR_item]["VALUE"])))
                elif DIC_in[ARR_item]["DATA_TYPE"] == "STR":
                    if self.IF_ensemble_run:
                        self.FILE.write(DIC_in[ARR_item]["STR_FMT"].format(DIC_in[ARR_item]["VALUE"],\
                                "{0:05d}".format(self.NUM_ensemble_member), \
                                self.STR_connect_symbol, \
                                "{0:05d}".format(self.NUM_input_ensemble_member)))
                    else:
                        self.FILE.write(DIC_in[ARR_item]["STR_FMT"].format(DIC_in[ARR_item]["VALUE"], ""              , ""))
                else:
                    self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"]))
            elif DIC_in[ARR_item]["ARR_TYPE"] == "M":
                # the ARR_TYPE as multi input number but same all in a row
                for d in range(self.NUM_MAX_DOM):
                    if DIC_in[ARR_item]["DATA_TYPE"] == "BLN":
                        self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(self.BLN2WRFSTR(DIC_in[ARR_item]["VALUE"])))
                    else:
                        self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"][d]))

            elif DIC_in[ARR_item]["ARR_TYPE"] == "N":
                # the ARR_TYPE as multi input number but same all in a row
                for d in range( len(DIC_in[ARR_item]["VALUE"]) ): 
                    if DIC_in[ARR_item]["DATA_TYPE"] == "BLN":
                        self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(self.BLN2WRFSTR(DIC_in[ARR_item]["VALUE"])))
                    else:
                        self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"][d]))
            elif DIC_in[ARR_item]["ARR_TYPE"] == "P":
            # the ARR_TYPE as multi input number but must be user specific
                if len(self.DIC_user[ARR_item]["VALUE"]) == 1:
                    self.FILE.write(self.DIC_user[ARR_item]["STR_FMT"].format(self.DIC_user[ARR_item]["VALUE"][0]))
                else:
                    for d in range(self.NUM_MAX_DOM):
                        if DIC_in[ARR_item]["DATA_TYPE"] == "BLN":
                            self.FILE.write(self.DIC_user[ARR_item]["STR_FMT"].format(self.BLN2WRFSTR(self.DIC_user[ARR_item]["VALUE"][d])))
                        else:
                            self.FILE.write(self.DIC_user[ARR_item]["STR_FMT"].format(self.DIC_user[ARR_item]["VALUE"][d]))

            elif DIC_in[ARR_item]["ARR_TYPE"] == "A":
            # the ARR_TYPE as multi input number but can be different in a row
                for d in range(self.NUM_MAX_DOM):
                    if DIC_in[ARR_item]["DATA_TYPE"] == "BLN":
                        if d == 0:
                            self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(self.BLN2WRFSTR(DIC_in[ARR_item]["VALUE"][0])))
                        else:
                            self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(self.BLN2WRFSTR(DIC_in[ARR_item]["VALUE"][-1])))

                    else:
                        if d == 0:
                            self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"][0]))
                        else:
                            self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"][-1]))

            self.FILE.write("\n")

    def create_wps_namelist(self):
        self.FILE     = open("{0:s}/{1:s}".format(self.STR_DIR, self.STR_wps_namelist), "w")
        print("Starting creating the namelist for wps: {0:s}".format(self.STR_wps_namelist))
        print("starting creating the namelist: {0:s}".format(self.STR_wps_namelist))
        self.FILE.write("&share\n")
        self.write_namelist(self.DIC_share_common_para, self.ARR_share)
        self.FILE.write("/\n")
        self.FILE.write("&geogrid\n")
        self.write_namelist(self.DIC_geogrid_common_para, self.ARR_geogrid)
        self.FILE.write("/\n")
        self.FILE.write("&ungrib\n")
        self.write_namelist(self.DIC_ungrib_common_para, self.ARR_ungrib)
        self.FILE.write("/\n")
        self.FILE.write("&metgrid\n")
        self.write_namelist(self.DIC_metgrid_common_para, self.ARR_metgrid)
        self.FILE.write("/\n")



        self.FILE.close()
        return 0


 
    def create_a_namelist(self):
        if self.IF_ensemble_run :
            self.FILE     = open("{0:s}/{1:s}{2:05d}".format(self.STR_DIR, self.STR_wrf_namelist, self.NUM_ensemble_member), "w")
        else: 
            self.FILE     = open("{0:s}/{1:s}".format(self.STR_DIR, self.STR_wrf_namelist), "w")

        print("starting creating the namelist: {0:s}".format(self.STR_wrf_namelist))
        self.FILE.write("&time_control\n")
        self.write_namelist(self.DIC_time_control_common_para, self.ARR_time_control)
        self.FILE.write("/\n")
        self.FILE.write("&domains\n")
        self.write_namelist(self.DIC_domains_common_para, self.ARR_domains)
        self.FILE.write("/\n")
        self.FILE.write("&physics\n")
        self.write_namelist(self.DIC_physics_common_para, self.ARR_physics)
        self.FILE.write("/\n")
        self.FILE.write("&fdda\n")
        self.FILE.write("/\n")
        self.FILE.write("&dynamics\n")
        self.write_namelist(self.DIC_dynamics_common_para, self.ARR_dynamics)
        self.FILE.write("/\n")
        self.FILE.write("&bdy_control\n")
        self.write_namelist(self.DIC_bdy_control_common_para, self.ARR_bdy_control)
        self.FILE.write("/\n")
        self.FILE.write("&namelist_quilt\n")
        self.write_namelist(self.DIC_namelist_quilt_common_para, self.ARR_namelist_quilt)
        self.FILE.write("/\n")
        if self.IF_SKEBS:
            self.FILE.write("&stoch\n")
            self.write_namelist(self.DIC_stoch_skebs_common_para, self.ARR_stoch_skebs)
            self.FILE.write("/\n")
        elif self.IF_SPPT:
            self.FILE.write("&stoch\n")
            self.write_namelist(self.DIC_stoch_sppt_common_para, self.ARR_stoch_sppt)
            self.FILE.write("/\n")

        self.FILE.close()
        return 0

if __name__ == "main" :
    print("No Warranty for usage.")


