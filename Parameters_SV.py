import os
from dotmap import DotMap

def ImportparSV():
    par = DotMap()
    par.length = 0.5;  # Length death volume capillary [m]
    par.diameter = 1e-3;  # Diameter capillary [m]
    par.diff = 1e-9;  # Diffusion coefficient ~1e-9
    par.partCat = 0.2;  # Part of total throughput that is catalyst
    par.partSolQuen = 1 - par.partCat;
    par.volumeFlowCel = 100;  # microliter
    par.timeToDoSettings = 1;  # minutes
    par.cycleTime = 6;  # times residence time (rt_dv) per cycle (measurement)
    par.factorFirstMeasurement = 1.5;

    # values showed in interface 1
    par.setTotalFlowRate = 4000;
    par.setConLoop = 6;
    par.setRepeatConLoop = 10;
    par.setTimeBetweenMeasurments = 1;
    par.setNameQuencher = 'Quencher';
    par.setNameFile = "KK-SV-20180101-1";
    par.email = 'noelresearchgroup.automation@gmail.com';  # adjustable in interface;
    par.quenSolv = 0.1; # M
    par.location = os.path.join(os.getcwd(), 'Data')

    # name database
    par.databaseName = "Database_Automation.db";

    # for main_sv run
    par.quit = False;

    return par