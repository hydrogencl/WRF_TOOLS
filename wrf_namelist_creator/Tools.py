#!/usr/bin/python
import math, re, os
import json
class Tools:
    def run_time_cal(ARR_TIME_IN, IF_LEAP=False, NUM_MON=0):
        if IF_LEAP == True: 
            ARR_DAY_LIM = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
        else:
            ARR_DAY_LIM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
        if NUM_MON == 0:
            DAYS    = ARR_TIME_IN[0] * sum(ARR_DAY_LIM) + ARR_DAY_LIM[ ARR_TIME_IN[1] ] + ARR_TIME_IN[2]
        else:
            DAYS    = ARR_TIME_IN[0] * sum(ARR_DAY_LIM) + ARR_TIME_IN[1] * NUM_MON + ARR_TIME_IN[2]
        HOURS   = DAYS * 24 + ARR_TIME_IN[3]
        MINUTES = HOURS * 60 + ARR_TIME_IN[4] 
        return {"DAYS": DAYS, "HOURS": HOURS, "MINUTES": MINUTES }

    def calendar_cal(ARR_START_TIME, ARR_INTERVAL, ARR_END_TIME_IN=[0, 0, 0, 0, 0, 0.0], IF_LEAP=False):
        """Calculaing the Data and Time base on the intervals 
           Input: ARR_START_TIME=[ %d %d %d %d %d %d ] 
                  ARR_INTERAL=   [ %d %d %d %d %d %d ]         """
        ARR_END_TIME  = [ 0,0,0,0,0,0.0]
        ARR_DATETIME  = ["SECOND", "MINUTE", "HOUR","DAY", "MON", "YEAR"]
        NUM_ARR_DATETIME = len(ARR_DATETIME)
        IF_FERTIG = False
        ARR_FERTIG = [0,0,0,0,0,0]
        DIC_TIME_LIM = \
        {"YEAR"  : {"START": 0 , "LIMIT": 9999 },\
         "MON"   : {"START": 1 , "LIMIT": 12 },\
         "DAY"   : {"START": 1 , "LIMIT": 31 },\
         "HOUR"  : {"START": 0 , "LIMIT": 23 },\
         "MINUTE": {"START": 0 , "LIMIT": 59 },\
         "SECOND": {"START": 0 , "LIMIT": 59 },\
        }
        for I, T in enumerate(ARR_START_TIME):
            ARR_END_TIME[I] = T + ARR_INTERVAL[I]
        while IF_FERTIG == False:
            if math.fmod(ARR_END_TIME[0],4) == 0: IF_LEAP=True
            if IF_LEAP:
                ARR_DAY_LIM = [0,31,29,31,30,31,30,31,31,30,31,30,31]
            else:
                ARR_DAY_LIM = [0,31,28,31,30,31,30,31,31,30,31,30,31]
            for I, ITEM in enumerate(ARR_DATETIME):
                NUM_ARR_POS = NUM_ARR_DATETIME-I-1
                if ITEM == "DAY":
                    if ARR_END_TIME[NUM_ARR_POS] > ARR_DAY_LIM[ARR_END_TIME[1]]:
                        ARR_END_TIME[NUM_ARR_POS] = ARR_END_TIME[NUM_ARR_POS] - ARR_DAY_LIM[ARR_END_TIME[1]]
                        ARR_END_TIME[NUM_ARR_POS - 1] += 1
                else:
                    if ARR_END_TIME[NUM_ARR_POS] > DIC_TIME_LIM[ITEM]["LIMIT"]:
                        ARR_END_TIME[NUM_ARR_POS - 1] += 1
                        ARR_END_TIME[NUM_ARR_POS] = ARR_END_TIME[NUM_ARR_POS] - DIC_TIME_LIM[ITEM]["LIMIT"] - 1
            for I, ITEM in enumerate(ARR_DATETIME):
                NUM_ARR_POS = NUM_ARR_DATETIME-I-1
                if ITEM == "DAY":
                    if ARR_END_TIME[NUM_ARR_POS] <= ARR_DAY_LIM[ARR_END_TIME[1]]: ARR_FERTIG[NUM_ARR_POS] = 1
                else:
                    if ARR_END_TIME[NUM_ARR_POS] <= DIC_TIME_LIM[ITEM]["LIMIT"]:  ARR_FERTIG[NUM_ARR_POS] = 1
                if sum(ARR_FERTIG) == 6: IF_FERTIG = True
        return ARR_END_TIME
