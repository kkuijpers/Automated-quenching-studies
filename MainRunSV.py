from Parameters_SV import ImportparSV
from SVGUI1 import SVInterface1
from SVGUI2 import SVInterface2
from SVGUI3 import SVInterface3
import SimpleOneTimeTask as ST
import logging
from DeviceClasses import HPLCPumpAzura, HPLCPumpSmartline, Autosampler, SyringePump

def MainRunSternVolmer():
    # create main logger for Autosampler experiment
    logger = logging.getLogger('SternVolmerLog')
    logging.basicConfig(filename='SternVolmerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # import all the standard / pre-determined parameters
    par = ImportparSV()

    # Make connection with the pumps
    # 4 = purple / 5 = red / 6 = yellow / 10 = green
    solventPump = HPLCPumpSmartline(comnumber=6 , baudrate=115200, name='Solvent_Pump')
    catPump = HPLCPumpSmartline(comnumber=5, baudrate=115200, name='Catalyst_Pump')
    quenchPump = HPLCPumpSmartline(comnumber=4, baudrate=115200, name='Quenchpump_Pump')

    # launch first interface
    gui1 = SVInterface1(par)
    gui1.root.mainloop()
    par = gui1.par
    if par.quit:
        return False

    # start solvent pump
    solventPump.SetFlowrate(par.totalThroughput)

    # launch second interface
    gui2 = SVInterface2(par)
    gui2.root.mainloop()
    par = gui2.par
    if par.quit:
        return False

    # launch third and operating interface
    gui3 = SVInterface3(par, solventPump, quenchPump, catPump)
    gui3.root.mainloop()
    if par.quit:
        return False

    # send email
    ST.SendEmail(par)

if __name__ == '__main__':
    MainRunSternVolmer()