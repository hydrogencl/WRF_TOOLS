import pytest
from wrf_namelist_creator import WRF_NAMELIST_CREATOR as WNC
from WNC import Tools as TOOLS
from WNC import NamelistChecker as NChk
from WNC import NamelistCreater as NCrt

class testAll:
    def test_necessary_libs(self):
        import os
        import re
        import math
    def test_tools(self):
        # Test on a leap year
        ARR_DATE_LY  = [2020,  2,  1,  0,  0,  0 ]
        # Test on a normal year
        ARR_DATE     = [2022,  2,  1,  0,  0,  0 ]
        ARR_INTERVAL = [   0,  0, 30,  0,  0,  0 ] 

        # Test on running time
        ARR_SIMTIME = [0, 0, 3, 0, 0, 0    ] 
        DIC_SIMTIME_OUT = TOOLS.run_time_cal(ARR_SIMTIME)
        assert DIC_SIMTIME_OUT["DAYS"]    =    3
        assert DIC_SIMTIME_OUT["HOURS"]   =   72
        assert DIC_SIMTIME_OUT["MINUTES"] = 4320

        ARR_ENDTIME_LY  = TOOLS.calendar_cal(ARR_DATE_LY, ARR_INTERVAL)
        ARR_ENDTIME     = TOOLS.calendar_cal(ARR_DATE   , ARR_INTERVAL)

        assert ARR_ENDTIME_LY[2] = 2 
        assert ARR_ENDTIME   [2] = 3 
