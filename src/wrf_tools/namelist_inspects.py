#!/usr/bin/python
import math, re, os
from subprocess import run
"""
This main program body contains following:
    1) tools: 
        The tools are mainly used to check the calculation of calendar stuff
        e.g. the caluclation of the time and the date and examine them when
        creating the run time and ending time. 

    2) Namelist Inspects:  
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
class Namelist_inspector: 
    """
    The namelist informations. Format:
    "Index Number": {OPT     : the WRF Option, same as Index Number
                     SCHEME  : the NAME of the scheme
                     REF     : Reference
                    }
    ADDITIONS: OPT_SFCLAY    : The forced Surface Layer Physics by WRF. Using the wrong one will be rejected
               OPT_RA_PHYSIC : Recommending Radiation Scheme for DIC_SF_SURFACE_PHYSICS.  
    """
    DIC_BL_PBL_PHYSICS = {\
        "1" : {"OPT": 1, "SCHEME": "YSU", "OPT_SFCLAY": [1], "REF": "Hong, Noh and Dudhia (2006, MWR)" },\
        "2" : {"OPT": 2, "SCHEME": "MYJ", "OPT_SFCLAY": [2], "REF":  "Janjic (1994, MWR)" },\
        "3" : {"OPT": 3, "SCHEME": "GFS", "OPT_SFCLAY": [3], "REF":  "Hong and Pan (1996, MWR)" },\
        "4" : {"OPT": 4, "SCHEME": "QNSE", "OPT_SFCLAY": [4], "REF": "Sukoriansky, Galperin and Perov (2005, BLM)" },\
        "5" : {"OPT": 5, "SCHEME": "MYNN2", "OPT_SFCLAY": [1, 2, 5], "REF": "Nakanishi and Niino (2006, BLM)"  },\
        "6" : {"OPT": 6, "SCHEME": "MYNN3", "OPT_SFCLAY": [5], "REF": "Nakanishi and Niino (2006, BLM)"  },\
        "7" : {"OPT": 7, "SCHEME": "ACM2", "OPT_SFCLAY": [1, 7], "REF": "Pleim (2007, JAMC)" },\
        "8" : {"OPT": 8, "SCHEME": "BouLac", "OPT_SFCLAY": [1, 2], "REF": "Bougeault and Lacarrere (1989, MWR)" },\
        "9" : {"OPT": 9, "SCHEME": "UW", "OPT_SFCLAY": [1, 2], "REF": "Bretherton and Park (2009, JC)" },\
        "10" : {"OPT": 10, "SCHEME": "TEMF", "OPT_SFCLAY": [10], "REF": "Angevine, Jiang and Mauriten (2010, MWR)" },\
        "12" : {"OPT": 12, "SCHEME": "GBM", "OPT_SFCLAY": [1], "REF": "Grenier and Bretherton (2001, MWR)" },\
        "99" : {"OPT": 99, "SCHEME": "MRF", "OPT_SFCLAY": [0], "REF": "Hong and Pan (1996, MWR)" },\
        "11" : {"OPT": 11, "SCHEME": "Shin-Hong", "OPT_SFCLAY": [0], "REF": "Shin and Hong (2015, MWR)" }}

    DIC_CU_PHYSICS = {\
        "1" : {"OPT": 1, "SCHEME": "Kain-Fritsch", "REF": "Kain (2004, JAM)" },\
        "2" : {"OPT": 2, "SCHEME": "Betts-Miller-Janjic", "REF": "Janjic (1994, MWR; 2000, JAS)" },\
        "3" : {"OPT": 3, "SCHEME": "Grell-Freitas", "REF": "Grell et al. (2013)" },\
        "4" : {"OPT": 4, "SCHEME": "Old Simplied Arakawa-Schubert", "REF": "Pan and Wu (1995), NMC Office Note 409" },\
        "5" : {"OPT": 5, "SCHEME": "Grell-3", "REF": "" },\
        "6" : {"OPT": 6, "SCHEME": "Tiedtke", "REF": "Tiedtke (1989, MWR), Zhang et al. (2011, MWR)" },\
        "7" : {"OPT": 7, "SCHEME": "Zhang-McFarlane", "REF": "Zhang and McFarlane (1995, AO)" },\
        "11" : {"OPT": 11, "SCHEME": "Multi-scale KF", "REF": "Zheng et al. (2015, MWR)" },\
        "14" : {"OPT": 14, "SCHEME": "New SAS", "REF": "Han and Pan (2011, Wea. Forecasting)" },\
        "16" : {"OPT": 16, "SCHEME": "New Tiedtke", "REF": "" },\
        "84" : {"OPT": 84, "SCHEME": "New SAS (HWRF)", "REF": "Han and Pan (2011, Wea. Forecasting)" },\
        "93" : {"OPT": 93, "SCHEME": "Grell-Devenyi", "REF": "Grell and Devenyi (2002, GRL)" },\
        "99" : {"OPT": 99, "SCHEME": "Old Kain-Fritsch", "REF": "Kain and Fritsch (1990, JAS; 1993, Meteo. Monogr.)" }} 

    DIC_MP_PHYSICS = {\
        "1" : {"OPT": 1, "SCHEME": "Kessler", "REF": "Kessler (1969)" },\
        "2" : {"OPT": 2, "SCHEME": "Lin (Purdue)", "REF": "Lin, Farley and Orville (1983, JCAM)" },\
        "3" : {"OPT": 3, "SCHEME": "WSM3", "REF": "Hong, Dudhia and Chen (2004, MWR)" },\
        "4" : {"OPT": 4, "SCHEME": "WSM5", "REF": "Hong, Dudhia and Chen (2004, MWR)" },\
        "5" : {"OPT": 5, "SCHEME": "Eta (Ferrier)", "REF": "Rogers, Black, Ferrier, Lin, Parrish and DiMego (2001, web doc)" },\
        "6" : {"OPT": 6, "SCHEME": "WSM6", "REF": "Hong and Lim (2006, JKMS)" },\
        "7" : {"OPT": 7, "SCHEME": "Goddard", "REF": "Tao, Simpson and McCumber (1989, MWR)" },\
        "8" : {"OPT": 8, "SCHEME": "Thompson", "REF": "Thompson, Field, Rasmussen and Hall (2008, MWR)" },\
        "9" : {"OPT": 9, "SCHEME": "Milbrandt 2-mom", "REF": "Milbrandt and Yau (2005, JAS)" },\
        "10" : {"OPT": 10, "SCHEME": "Morrison 2-mom", "REF": "Morrison, Thompson and Tatarskii (2009, MWR)" },\
        "11" : {"OPT": 11, "SCHEME": "CAM 5.1", "REF": "Neale et al. (2012, NCAR Tech Note)" },\
        "13" : {"OPT": 12, "SCHEME": "SBU-YLin", "REF": "Lin and Colle (2011, MWR)" },\
        "14" : {"OPT": 13, "SCHEME": "WDM5", "REF": "Lim and Hong (2010, MWR)" },\
        "16" : {"OPT": 14, "SCHEME": "WDM6", "REF": "Lim and Hong (2010, MWR)" },\
        "17" : {"OPT": 16, "SCHEME": "NSSL 2-mom", "REF": "Mansell, Ziegler and Bruning (2010, JAS)" },\
        "18" : {"OPT": 17, "SCHEME": "NSSL 2-mom w/ CCN prediction", "REF": "Mansell, Ziegler and Bruning (2010, JAS)" },\
        "19" : {"OPT": 18, "SCHEME": "NSSL 1-mom", "REF": "" },\
        "21" : {"OPT": 19, "SCHEME": "NSSL 1-momlfo", "REF": "" },\
        "22" : {"OPT": 21, "SCHEME": "NSSL 2-mom w/o hail", "REF": "" },\
        "28" : {"OPT": 22, "SCHEME": "Thompson aerosol-aware", "REF": "Thompson and Eidhammer (2014, JAS)" },\
        "30" : {"OPT": 28, "SCHEME": "HUJI SBM (fast)", "REF": "Khain et al. (2010, JAS)" },\
        "32" : {"OPT": 30, "SCHEME": "HUJI SBM full", "REF": "Khain et al. (2004, JAS)" }}

    DIC_RA_SW_PHYSICS = {\
        "1" : {"OPT": 1, "SCHEME": "Dudhia", "REF": "Dudhia (1989, JAS)" },\
        "2" : {"OPT": 2, "SCHEME": "Goddard", "REF": "Chou and Suarez (1994, NASA Tech Memo)" },\
        "3" : {"OPT": 3, "SCHEME": "CAM", "REF": "Collins et al. (2004, NCAR Tech Note)" },\
        "4" : {"OPT": 4, "SCHEME": "RRTMG", "REF": "Iacono et al. (2008, JGR)" },\
        "24" : {"OPT": 24 , "SCHEME": "RRTMG", "REF": "Fast version" },\
        "5" : {"OPT": 5, "SCHEME": "New Goddard", "REF": "Chou and Suarez (1999, NASA Tech Memo)" },\
        "7" : {"OPT": 7, "SCHEME": "FLG", "REF": "Gu et al. (2011, JGR), Fu and Liou (1992, JAS)" },\
        "99" : {"OPT": 99, "SCHEME": "GFDL", "REF": "Fels and Schwarzkopf (1981, JGR)" }}

    DIC_RA_LW_PHYSICS = {\
        "1" : {"OPT": 1, "SCHEME": "RRTM", "REF": "Mlawer et al. (1997, JGR)" },\
        "3" : {"OPT": 3, "SCHEME": "CAM", "REF": "Collins et al. (2004, NCAR Tech Note)" },\
        "4" : {"OPT": 4, "SCHEME": "RRTMG", "REF": "Iacono et al. (2008, JGR)" },\
        "24" : {"OPT": 24, "SCHEME": "RRTMG", "REF": "Fast version" },\
        "5" : {"OPT": 5, "SCHEME": "New Goddard", "REF": "Chou and Suarez (1999, NASA Tech Memo)" },\
        "7" : {"OPT": 7, "SCHEME": "FLG", "REF": "Gu et al. (2011, JGR), Fu and Liou (1992, JAS)" },\
        "31" : {"OPT": 31, "SCHEME": "Held-Suarez", "REF": "" },\
        "99" : {"OPT": 99, "SCHEME": "GFDL", "REF": "Fels and Schwarzkopf (1981, JGR)" }}

    DIC_SF_SFCLAY_PHYSICS = {\
        "0" : {"OPT": 0, "SCHEME": "None", "REF": "" },\
        "1" : {"OPT": 1, "SCHEME": "Revised MM5 Monin-Obukhov scheme", "REF": "" },\
        "2" : {"OPT": 2, "SCHEME": "Monin-Obukhov (Janjic Eta) scheme", "REF": "" },\
        "3" : {"OPT": 3, "SCHEME": "NCEP GFS scheme (NMM only)", "REF": "" },\
        "4" : {"OPT": 4, "SCHEME": "QNSE", "REF": "" },\
        "5" : {"OPT": 5, "SCHEME": "MYNN", "REF": "" },\
        "7" : {"OPT": 7, "SCHEME": "Pleim-Xiu (ARW only), only tested with Pleim-Xiu surface and ACM2 PBL", "REF": "" },\
        "10" : {"OPT": 10, "SCHEME": "TEMF (ARW only)", "REF": "" },\
        "91" : {"OPT": 91, "SCHEME": "old MM5 surface layer scheme (previously option 1)", "REF": "" }}

    DIC_SF_SURFACE_PHYSICS = {\
        "0" : {"OPT": 0, "SCHEME": "old, or non-vegetation dependent thermal roughness length over land", "REF": "" },\
        "1" : {"OPT": 1, "SCHEME": "thermal diffusion scheme", "REF": "" },\
        "2" : {"OPT": 2, "SCHEME": "unified Noah land-surface model", "REF": "" },\
        "3" : {"OPT": 3, "SCHEME": "RUC land-surface model", "REF": "" },\
        "4" : {"OPT": 4, "SCHEME": "Noah-MP land-surface model (additional options under the &noah_mp section)", "REF": "" },\
        "5" : {"OPT": 5, "SCHEME": "CLM4 (Community Land Model Version 4)", "REF": "" },\
        "7" : {"OPT": 7, "SCHEME": "Pleim-Xiu scheme (ARW only)", "REF": "" },\
        "8" : {"OPT": 8, "SCHEME": "SSiB land-surface model (ARW only).", "DESCRIPTION": "works with ra_lw_physics = 1, 3, or 4, and ra_sw_physics = 1, 3, or 4", "OPT_RA_PHYSIC" : [1, 3, 4 ],  "REF": "" }}

#    DIC_ = {\
#        "" : {"OPT": , "SCHEME": "", "REF": "" },\
#        "" : {"OPT": , "SCHEME": "", "REF": "" }}

