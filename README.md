# WRF_TOOLS

To creating WRF namelist in the Object-Oriented manner. 
Test

## Usage Example:

The file `example.py` is a very simple example for you

 * What to write to activate the modulde
 * How to set the physics
 * Example for large ensemble simulation

### Initialing 
`import WRF_NAMELIST_CREATOR as WNC`
`NCC = WNC.namelist_creater("namelist.input", STR_DIR='./TEST_GROUND/')`
`NLC = WNC.namelist_checker()`

### Specific the time
`NCC.read_user_specific(ARR_run_time_in=[0,0,0,12,0,0], ARR_start_time_in=[2015, 8, 21, 0,0,0], ARR_end_time_in=[2015, 8, 21, 12, 0, 0])`

### Changing the namelist input (e.g. microphysics)
`NCC.DIC_physics_common_para["mp_physics"]["VALUE"] = 6`

### Making the namelist
`NCC.create_a_namelist()`

## Advance Example:
  change the namelist's format to fit your need:

### to change the default values:
  `NCC.DIC_user["starting_time_step"]["VALUE"] = [24, 12, 6] `

### to change the format to generate the different namelist:
  `NCC.DIC_time_control_common_para["bdy_inname"]["VALUE"] = "ecmwf" `
   ... and then your input for `wrfbdy` will become: `ecmwf_d<domain>`  

  `NCC.DIC_time_control_common_para["bdy_inname"]["STR_FMT"] = "\'{0:s}{1:s}_d<domain>_<date>\'," `

   ... and then your input for `wrfbdy` will include the "date"

## Additional Setup

   `NCC.IF_ensemble_run` to activate the ensemble simulation namelist for `ESIAS-met`, which an ensemble version of WRF by Rheinisches Institut für Umweltforschung an der Universität zu Köln and IEK-8 Forschungszentrum Juelich. 
   This option will be only useful when using this version of WRF. 
   Also this is a good example to setup additional namelist for specific version fo WRF. 

