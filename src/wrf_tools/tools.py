#!/usr/bin/python
"""
This main program body contains the tools 
    1) tools: 
        The tools are mainly used to check the calculation of calendar stuff
        e.g. the caluclation of the time and the date and examine them when
        creating the run time and ending time. 

"""
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

    def make_wrf_datetime(ARR_TIME_IN):
        return "{0:04d}-{1:02d}-{2:02d}_{3:02d}:{4:02d}:{5:02d}".format(\
                ARR_TIME_IN[0], ARR_TIME_IN[1], ARR_TIME_IN[2],\
                ARR_TIME_IN[3], ARR_TIME_IN[4], ARR_TIME_IN[5]  )

    def make_alphabet_index(indexIn):
        """
        The index for Alphabet which will turn index from 0 to AAA as
        based-26 positional notation. The largest index is 17575 as ZZZ.
        This function should provide a very elastic function to provide
        the alphabet index. Question: why not use number index? 
        """
        if indexIn >= 26**26:
            print("Running out of suffixes, maximum is 17575")
            return "RUNNING_OUT_OF_INDEX"
        else:
            arrAlphabetOrder = ["A", "B", "C", "D", "E", "F", "G","H",  \
                                "I", "J", "K", "L", "M", "N", "O","P",  \
                                "Q", "R", "S", "T", "U", "V", "W",      \
                                "X", "Y", "Z"]
            ind_out1 = int(  indexIn/26**2) 
            ind_out2 = int( (math.fmod( indexIn - ind_out1*26**2, 26**2))/26)
            ind_out3 = int( (math.fmod( indexIn - ind_out1*26**2 - ind_out2*26, 26)))
            strOut   = "{0:s}{1:s}{2:s}".format(arrAlphabetOrder[ind_out1], \
                                                arrAlphabetOrder[ind_out2], \
                                                arrAlphabetOrder[ind_out3])
            return strOut

