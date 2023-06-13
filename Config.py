import os
import datetime
import numpy as np

class config(object):
    
    LAT_MIN_BORNHOLM = 54.5
    LAT_MAX_BORNHOLM = 56
    LON_MIN_BORNHOLM = 13
    LON_MAX_BORNHOLM = 16
    SOG_MAX_BORNHOLM = 20
    
    LAT_MIN_SJÆLLAND = 54.4
    LAT_MAX_SJÆLLAND = 56.4
    LON_MIN_SJÆLLAND = 10.5
    LON_MAX_SJÆLLAND = 13.5
    SOG_MAX_SJÆLLAND = 20
    
    LAT_RES = 0.01
    LON_RES = 0.01
    SOG_RES = 0.5
    COG_RES = 5
    
    LAT_EDGES = np.around(np.arange(LAT_MIN_BORNHOLM, LAT_MAX_BORNHOLM+(LAT_RES/10000), LAT_RES), decimals=2)
    LON_EDGES = np.around(np.arange(LON_MIN_BORNHOLM, LON_MAX_BORNHOLM+(LON_RES/10000), LON_RES), decimals=2)
    SOG_EDGES = np.around(np.arange(0, SOG_MAX_BORNHOLM+(SOG_RES/10000), SOG_RES), decimals=1)
    COG_EDGES = np.around(np.arange(0, 360+(COG_RES/10000), COG_RES), decimals=0)

    #AIS INDEX MEANINGS
    STAT_NAV_STATUSES = [1, 5, 6, 15, 95, 98]
    MOV_NAV_STATUSES = [0, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 96, 97, 99]
        
    SHIPTYPE_FISHING = [30]
    SHIPTYPE_TOWING = [31, 32, 52]
    SHIPTYPE_DREDGING = [33]
    SHIPTYPE_DIVING = [34]
    SHIPTYPE_MILITARY = [35]
    SHIPTYPE_SAILING = [36]
    SHIPTYPE_PLEASURE = [37]
    SHIPTYPE_PILOT = [50]
    SHIPTYPE_RESEARCH = [90]
    SHIPTYPE_HSV = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    SHIPTYPE_PASSENGER = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
    SHIPTYPE_CARGO = [70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
    SHIPTYPE_TANKER = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
