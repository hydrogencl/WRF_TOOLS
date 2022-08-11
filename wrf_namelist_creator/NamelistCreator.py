from . import Tools
class NamelistCreater:
    # Important Parameters
    # Time control :
    # Format: YYYY MM DD hh mm ss
    ARR_run_time       = [    0,  0,  0, 48,  0,  0 ]  
    ARR_start_time     = [ 2008,  8,  8,  0,  0,  0 ]
    ARR_end_time       = [ 2008,  8, 10,  0,  0,  0 ]

    # Domains:
    NUM_MAX_DOM               = 2
    ARR_e_we                  = [  180, 223, 436 ]
    ARR_e_SN                  = [  180, 223, 436 ]
    ARR_e_vert                = [   50,  50,  50  ] 
    ARR_dx                    = [ 20000, 6666.666, 3333.333 ]
    ARR_dy                    = [ 20000, 6666.666, 3333.333 ]
    ARR_grid_id               = [     1,        2,        3 ]
    ARR_parent_id             = [     1,        1,        2 ]
    ARR_i_parent_start        = [     1,       65,        2 ]
    ARR_j_parent_start        = [     1,       58,        2 ]
    ARR_parent_grid_ratio     = [     1,        3,        3 ]
    ARR_max_step_increase_pct = [     5,       51,       51 ]
    ARR_starting_time_step    = [    20,       10,        5 ]
    ARR_max_time_step         = [   100,       24,       10 ]

    # Ensembles:
    NUM_ensemble_member       = 0
    NUM_input_ensemble_member = 0
    IF_ensemble_run           = False
    # Others:
    STR_DIR="./"

    def __init__(self, STR_namelist="namelist.input", STR_DIR="./"):
        print("Start the namelist creator by Python")
        print("    Author: Y.-S. Lu                ")
        print("    First Edition: 24.04.2020       ")
        print("              ... during COVID-19   ")

        # ENSEMBLE SETTING UP
        self.IF_SPPT  = False
        self.IF_SKEBS = False
        self.STR_connect_symbol = "_"

        # FILENAME

        self.STR_namelist = STR_namelist
        self.STR_DIR      = STR_DIR

        self.ARR_time_control = ['run_days', 'run_hours', 'run_minutes', 'run_seconds', 'start_year', 'start_month', 'start_day', 'start_hour', 'start_minute', 'start_second', 'end_year', 'end_month', 'end_day', 'end_hour', 'end_minute', 'end_second', 'interval_seconds', 'input_from_file', 'history_interval', 'history_outname', 'bdy_inname', 'input_inname', 'frames_per_outfile', 'auxhist1_outname', 'auxhist2_outname', 'auxhist1_interval', 'auxhist2_interval', 'frames_per_auxhist1', 'frames_per_auxhist2', 'aux1_time', 'aux2_time', 'interpolation_time', 'interpolation_number', 'restart', 'restart_interval', 'override_restart_timers', 'io_form_history', 'io_form_restart', 'io_form_input', 'io_form_boundary', 'debug_level', 'io_form_auxinput2', 'io_form_auxhist1', 'io_form_auxhist2', 'auxinput1_inname']

        self.ARR_domains = ['time_step', 'time_step_fract_num', 'time_step_fract_den', 'max_dom', 'e_we', 'e_sn', 'e_vert', 'p_top_requested', 'num_metgrid_levels', 'num_metgrid_soil_levels', 'dx', 'dy', 'grid_id', 'parent_id', 'i_parent_start', 'j_parent_start', 'parent_grid_ratio', 'feedback', 'use_adaptive_time_step', 'step_to_output_time', 'target_cfl', 'max_step_increase_pct', 'starting_time_step', 'max_time_step', 'min_time_step', 'adaptation_domain', 'interp_type', 'smooth_option', 'sfcp_to_sfcp']

        self.ARR_physics = ['mp_physics', 'ra_lw_physics', 'ra_sw_physics', 'sf_sfclay_physics', 'sf_surface_physics', 'bl_pbl_physics', 'cu_physics', 'radt', 'bldt', 'cudt', 'isftcflx', 'isfflx', 'ifsnow', 'icloud', 'surface_input_source', 'num_soil_layers', 'sf_urban_physics', 'maxiens', 'maxens', 'maxens2', 'maxens3', 'ensdim', 'topo_wind', 'num_land_cat', 'ysu_st']

        self.ARR_dynamics = ['w_damping', 'diff_opt', 'km_opt', 'diff_6th_opt', 'diff_6th_factor', 'time_step_sound', 'base_temp', 'damp_opt', 'dampcoef', 'khdif', 'kvdif', 'non_hydrostatic', 'moist_adv_opt', 'scalar_adv_opt']

        self.ARR_bdy_control = ['spec_bdy_width', 'spec_zone', 'relax_zone', 'specified', 'nested']
        
        self.ARR_namelist_quilt = ['nio_tasks_per_group', 'nio_groups']

        self.ARR_stoch_skebs = ['skebs', 'stoch_vertstruc_opt', 'tot_backscat_psi', 'tot_backscat_t', 'ztau_psi', 'ztau_t', 'nens', 'ISEED_SKEBS']

        self.ARR_stoch_sppt = ['sppt', 'nens', 'timescale_sppt', 'gridpt_stddev_sppt', 'ISEED_SPPT']


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
        "history_outname"                  : { "VALUE":  'wrfout'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
        "bdy_inname"                       : { "VALUE":  'wrfbdy'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}{1:s}_d<domain>\',"},
        "input_inname"                     : { "VALUE":  'wrfinput'    , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}{1:s}_d<domain>\',"},
        "rst_outname"                      : { "VALUE":  'wrfrst'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
        "rst_inname"                       : { "VALUE":  'wrfrst'      , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
        "frames_per_outfile"               : { "VALUE":  1000          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"M"},
        "auxhist1_outname"                 : { "VALUE":  'auxhist1'    , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
        "auxhist2_outname"                 : { "VALUE":  'meteofrance' , "DATA_TYPE" : "STR" , "ARR_TYPE" :"S", "STR_FMT" : "\'{0:s}_d<domain>{2:s}{1:s}\',"},
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
        "e_we"                             : { "VALUE":  180         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "e_sn"                             : { "VALUE":  180         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "e_vert"                           : { "VALUE":  50          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "p_top_requested"                  : { "VALUE":  5000        , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
        "num_metgrid_levels"               : { "VALUE":  42          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
        "num_metgrid_soil_levels"          : { "VALUE":  4           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
        "dx"                               : { "VALUE":  20000       , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"P"},
        "dy"                               : { "VALUE":  20000       , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"P"},
        "grid_id"                          : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "parent_id"                        : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "i_parent_start"                   : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "j_parent_start"                   : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "parent_grid_ratio"                : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "feedback"                         : { "VALUE":  1           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"S"},
        "use_adaptive_time_step"           : { "VALUE":  True        , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
        "step_to_output_time"              : { "VALUE":  False       , "DATA_TYPE" : "BLN" , "ARR_TYPE" :"S"},
        "target_cfl"                       : { "VALUE":  1.2         , "DATA_TYPE" : "FLT" , "ARR_TYPE" :"M"},
        "max_step_increase_pct"            : { "VALUE":  5           , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "starting_time_step"               : { "VALUE":  20          , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
        "max_time_step"                    : { "VALUE":  100         , "DATA_TYPE" : "INT" , "ARR_TYPE" :"P"},
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

    def read_user_specific(self, ARR_run_time_in=[], ARR_start_time_in=[], ARR_end_time_in=[], NUM_MAX_DOM_in=0):
        if len(ARR_run_time_in) == 0 :
            ARR_run_time = self.ARR_run_time
        else:
            ARR_run_time = ARR_run_time_in

        if len(ARR_start_time_in) == 0 :
            ARR_start_time = self.ARR_start_time
        else:
            ARR_start_time = ARR_start_time_in

        if len(ARR_end_time_in) == 0 :
            ARR_end_time = self.ARR_end_time
        else:
            ARR_end_time = ARR_end_time_in

        # Checking Date and Time based on the intervals
        ARR_END_DATE_CHK  = Tools.calendar_cal(ARR_start_time, ARR_run_time)

        if Tools.run_time_cal(ARR_END_DATE_CHK) != Tools.run_time_cal(ARR_end_time):
            ARR_end_time  = ARR_END_DATE_CHK
            print("WARNING: The end date is not match with the interval time")
            print("       : The end date is changed as:{0:04d}-{1:02d}-{2:02d}_{3:02d}:{4:02d}:{5:02d}".format(\
                    ARR_end_time[0], ARR_end_time[1],ARR_end_time[2],ARR_end_time[3],ARR_end_time[4],ARR_end_time[5]))

        if NUM_MAX_DOM_in == 0 :
            NUM_MAX_DOM  = self.NUM_MAX_DOM 
        else:
            NUM_MAX_DOM  = NUM_MAX_DOM_in

        self.DIC_user = {\
        "run_days"                         : {"VALUE": [ ARR_run_time[2] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d}," },\
        "run_hours"                        : {"VALUE": [ ARR_run_time[3] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "run_minutes"                      : {"VALUE": [ ARR_run_time[4] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "run_seconds"                      : {"VALUE": [ ARR_run_time[5] ], "DATA_TYPE": "IND" ,"STR_FMT": "     {0:02d},"},\
        "start_year"                       : {"VALUE": [ ARR_start_time[0] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "   {0:04d},"},\
        "start_month"                      : {"VALUE": [ ARR_start_time[1] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "start_day"                        : {"VALUE": [ ARR_start_time[2] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "start_hour"                       : {"VALUE": [ ARR_start_time[3] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "start_minute"                     : {"VALUE": [ ARR_start_time[4] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "start_second"                     : {"VALUE": [ ARR_start_time[5] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "end_year"                         : {"VALUE": [ ARR_end_time[0] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "   {0:04d},"},\
        "end_month"                        : {"VALUE": [ ARR_end_time[1] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "end_day"                          : {"VALUE": [ ARR_end_time[2] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "end_hour"                         : {"VALUE": [ ARR_end_time[3] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "end_minute"                       : {"VALUE": [ ARR_end_time[4] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "end_second"                       : {"VALUE": [ ARR_end_time[5] for d in range(self.NUM_MAX_DOM)], "DATA_TYPE": "IND","STR_FMT": "     {0:02d},"},\
        "max_dom"                     : {"VALUE": [ NUM_MAX_DOM ], "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "e_we"                        : {"VALUE": self.ARR_e_we, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "e_sn"                        : {"VALUE": self.ARR_e_SN, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "e_vert"                      : {"VALUE": self.ARR_e_vert, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "dx"                          : {"VALUE": self.ARR_dx, "DATA_TYPE": "FLT","STR_FMT": "{0:7.3f},"},\
        "dy"                          : {"VALUE": self.ARR_dy, "DATA_TYPE": "FLT","STR_FMT": "{0:7.3f},"},\
        "grid_id"                     : {"VALUE": self.ARR_grid_id, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "parent_id"                   : {"VALUE": self.ARR_parent_id, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "i_parent_start"              : {"VALUE": self.ARR_i_parent_start, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "j_parent_start"              : {"VALUE": self.ARR_j_parent_start, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "parent_grid_ratio"           : {"VALUE": self.ARR_parent_grid_ratio, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "max_step_increase_pct"       : {"VALUE": self.ARR_max_step_increase_pct, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "starting_time_step"          : {"VALUE": self.ARR_starting_time_step, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
        "max_time_step"               : {"VALUE": self.ARR_max_time_step, "DATA_TYPE": "IND","STR_FMT": "{0:7d},"},\
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
                        self.FILE.write(DIC_DATA_TYPE_STR[DIC_in[ARR_item]["DATA_TYPE"]].format(DIC_in[ARR_item]["VALUE"]))

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

    def create_a_namelist(self):
        if self.IF_ensemble_run :
            self.FILE     = open("{0:s}/{1:s}{2:05d}".format(self.STR_DIR, self.STR_namelist, self.NUM_ensemble_member), "w")
        else: 
            self.FILE     = open("{0:s}/{1:s}".format(self.STR_DIR, self.STR_namelist), "w")

        print("starting creating the namelist: {0:s}".format(self.STR_namelist))
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
