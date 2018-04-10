from Parameters_Auto import ImportparAuto
from AutoGUI1 import AutomationInterface1
from NamingGUI import NamingGUI
from AutoGUI2 import AutomationInterface2
from DataParcing_Auto_2 import ParceData
import SimpleOneTimeTask as ST
import logging
from DeviceClasses import HPLCPumpAzura, HPLCPumpSmartline, Autosampler, SyringePump
import time
import os

def MainRunAutosampler():
    # create main logger for Autosampler experiment
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    logger.info('Start experiment')

    # import all the standard / pre-determined parameters
    par = ImportparAuto()
    par.mainRunParcing = True

    # create and make connection with the devices
    autosampler = Autosampler(comnumber=7, name='Autosampler')
    solventPump = HPLCPumpSmartline(comnumber=6, baudrate=115200, name='Solvent_Pump')
    catPump = HPLCPumpSmartline(comnumber=5, baudrate=115200, name='Catalyst_Pump')  # 4 = purple / 10 = green / 5 = orange

    # start solvent pump
    par.time101 = time.time()
    solventPump.SetFlowrate(par.flowRateSolvent)

    # create GUI1
    gui1 = AutomationInterface1(par)
    gui1.root.mainloop()
    par = gui1.par

    # tell the autosampler how many samples there are
    autosampler.SetExperiments(par.experimentNumber)

    # launch the naming GUI if checkbox was checked
    if par.selfNaming:
        namingWindow = NamingGUI(par)
        namingWindow.root.mainloop()
        par = namingWindow.par

        for name in par.namesExperiments:
            logger.debug('The name on index {0} is {1}'.format(par.namesExperiments.index(name), name))

    # start the second GUI
    gui2 = AutomationInterface2(par, autosampler, solventPump, catPump)
    gui2.root.mainloop()
    par = gui2.par

    # calculate data and make graphs
    ParceData(par)

    # send a email that the experiment is finished
    ST.SendEmail(par)

    # remove the fast overview pdf if self naming occurred
    if par.selfNaming:
        try:
            os.remove(os.path.join(par.workingDir, 'fast_overview.pdf'))
        except Exception as e:
            logger.error('redundant fast overview pdf could not be removed: {}'.format(e))
            pass

    # if overnight was checked, shut the pc down
    if par.overNight:
        ST.OverNightCommand(par)

    logger.info('Code has finished')

if __name__ == '__main__':
    MainRunAutosampler()