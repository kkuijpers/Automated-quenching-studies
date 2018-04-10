from dotmap import DotMap

def ImportparAuto ():
    par = DotMap()
    # constants
    pi = 3.14159265359
    lenghtAuto = 1.4;  # Length death volume capillary [m]
    diameter = 0.75e-3;  # Diameter capillary [m]
    volumeFlowCel = 100;  # microliter
    cycleTime = 6;  # times residence time (rt_dv) per cycle (measurement)

    # flow rates and residence times
    par.flowRateSolvent =1750; # round(solventFrac * totalFlowRate, 0)
    par.flowRateCat =250; # round((1 - solventFrac) * totalFlowRate, 0)
    par.flowrateCleaning = 2000;  # ul/min

    par.resTimeAuto = (((lenghtAuto * (pi / 4) * diameter ** 2) /
                        (par.flowRateSolvent * (10 ** -9) / 60) +
                        (volumeFlowCel / par.flowRateSolvent) * 60) *
                         cycleTime);
    par.resTimePump = (((lenghtAuto * (pi / 4) *
                         diameter ** 2) /
                        (par.flowRateCat * (10 ** -9) / 60)) +
                        (volumeFlowCel / par.flowRateCat) * 60) * \
                         cycleTime;

    # values showed in interface 1
    par.experimentNumber =1 ;

    # file and locations
    par.name = "KK-000";
    par.email = 'noelresearchgroup.automation@gmail.com';  # adjustable in interface;

    # time
    par.timeAnalysis = 420; # 7 min that it takes for tracer to leave the reactor
    par.timeBetweenInjects = 400;
    par.timeCatFlow = 240; # emperically determined time that is neccesary for cat flow to develop

    # self checkboxes
    par.setSelfNaming = False;
    par.setOverNight = False;
    par.mainRunParcing = False;

    par.databaseName = "Database_Automation.db";
    return par