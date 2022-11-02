#!/usr/bin/python
import math, re, os
from subprocess import run
"""
This main program body contains following:
    1) exectutes
        The tools are mainly used to check the calculation of calendar stuff
        e.g. the caluclation of the time and the date and examine them when
        creating the run time and ending time. 

    2) NamelistInformation:
        The namelist checker is used to provide the information for the  
        namelist as it's index number or description based on the user's 
        manuel. Some is important e.g. the PBL is coped with different land 
        surface physics schemes (MYNN or different type of MO). 


        Please raise the issue in the github.com/hydrogencl/WRF_TOOLS to 
        improve the problem and to correct errors. 

    3) NamelistCreator:
        The namelist creater is used to create the namelists for WRF and 
        WPS. The program is very flexible and thus any namelist can be 
        modified due to different usage or systems. 

"""
class Executor:

    def __init__(self):
        self.strFolder_ROOT        = "."
        self.strFolder_WPS         = "{}/WPS".format(self.strFolder_ROOT)
        self.strFolder_WRF         = "{}/WRF".format(self.strFolder_ROOT)
        self.strFolder_GRIB        = "./Path/To/GRIB"
        self.Interval_Hour         = 3
        self.strGribLinkName       = 'GRIBFILE'
        self.strFolderVTable       = './ungrib/Variable_Tables'
        self.strLinkVtableName     = 'Vtable'
        self.strTargetVtableName   = 'Vtable.GFS'
        self.input_global          = 'GFS'

    def run_geogrid(self):
        os.chdir(self.strFolder_WPS)
        run(["{0:s}/geogrid.exe".format(self.strFolder_WPS)])

    def run_ungrib(self, input_global=None):
        os.chdir(self.strFolder_WPS)
        #if input_global == None:
        #    input_global = self.input_global
        try: 
            os.remove(self.strLinkVtableName)
        except:
            print("There is no Vtable as:{0:s}".format(self.strLinkVtableName))
        os.symlink("{0:s}/{1:s}".format(self.strFolderVTable, self.strTargetVtableName), 
                   "{0:s}/{1:s}".format("./", self.strLinkVtableName))
        run(["{0:s}/ungrib.exe".format(self.strFolder_WPS)])
        # check which type of input

    def run_metgrid(self):
        os.chdir(self.strFolder_WPS)
        run(["{0:s}/metgrid.exe".format(self.strFolder_WPS)])

    def run_calc_ecmwf_p(self):
        os.chdir(self.strFolder_WPS)
        run(["{0:s}/calc_ecmwf_p.exe".format(self.strFolder_WPS)])

    def link_ungrib(self, arrFiles=[]): 
        # Remove the old grib link
        os.chdir(self.strFolder_WPS)
        for strFile in os.listdir():
            if re.match(self.strGribLinkName, strFile):
                os.remove(strFile)
                print("remove {0:s}".format(strFile) ) 
        for ind, files in enumerate(arrFiles):
            strIndex = Tools.make_alphabet_index(ind)
            os.symlink(files, "./{0:s}.{1:s}".format(self.strGribLinkName, strIndex, self.strFolder_WRF))
            print("done link: {0:s}.{1:s} --> {2:s}".format(self.strGribLinkName, strIndex, files))
        

