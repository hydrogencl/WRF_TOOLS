# WRF_TOOLS

To creating WRF namelist in the Object-Oriented manner. 

## Usage Example:


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
