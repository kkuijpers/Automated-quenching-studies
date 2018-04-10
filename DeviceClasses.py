import serial
import time
import logging
from tkinter import messagebox

class Device:
    def __init__(self, comnumber=1, baudrate=9600, name='Jack'):
        # initiation that is needed for every device
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('Serial is intitiated')

        # give the device a name
        self.name = name

        # create a serial port connection with the device
        self.serialObj = serial.Serial()
        self.serialObj.timeout = 1
        self.serialObj.baudrate = baudrate
        self.serialObj.port = "COM%s" % str(comnumber)  # com port name start from 0
        self.serialObj.open()  # opens serial port

        # print port open or closed
        if self.serialObj.isOpen():
            print("Open" + self.serialObj.portstr)
        self.logger.debug('The following serial port is now open: {0}'.format(self.serialObj.portstr))

    def __str__(self):
        print(self.name)

class Autosampler(Device):
    def __init__(self, comnumber=1, baudrate=9600, name='Jack'):
        super().__init__(comnumber, baudrate, name)
        # launches the startup functions for the autosampler
        self.CheckAvailability()
        self.SetStandardSettings()

    def CheckAvailability(self):
        # checks if the autosampler is available
        task = "1001"
        message = "000152"
        send = 0
        checkAvailability = True
        while checkAvailability:
            answer = self.SendCommand(task, message, send)
            if '61010152000000' in answer:
                checkAvailability = False
                self.logger.debug('Auto sampler is available.')
            else:
                checkAvailability = True
                self.logger.debug('Auto sampler is not available. answer is: {}'.format(answer))

    def SendCommand(self, task, message, send=1):
        # send a command to the autosampler
        message = '6101{0}{1}'.format(task, message)
        mss = str.encode(chr(2) + message + chr(3))
        self.serialObj.write(mss)

        self.logger.debug('The following message was send to the autosampler: {}.'.format(message))
        time.sleep(0.1)

        # wait for an answer
        while True:
            answer = self.serialObj.readline()
            if len(answer) > 0:
                break
            time.sleep(0.1)
            self.logger.debug('No answer from the auto sampler yet.')

        # read the answer
        answer = answer.decode()

        # send the message to the autosampler to accept and execute previous command
        if send == 1:
            # create and send message
            message = '6101100000{0}'.format(task)
            mss = str.encode(chr(2) + message + chr(3))
            self.serialObj.write(mss)
            self.logger.debug('The message was successfully send to the autosampler.')
            time.sleep(0.1)
            # wait for answer
            while True:
                answer = self.serialObj.readline()
                if len(answer) > 0:
                    break
                time.sleep(0.1)

            answer = answer.decode()
            self.logger.debug('Autosampler gave the following answer: '
                              '{} to the request: {}'.format(answer, message))
        # return the answer from the autosampler
        return answer

    def SetStandardSettings(self):
        # this function sends the standard system values to the autosampler
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('Sending standard configuration to Auto sampler')

        # Loop Volume (ul)
        task = "0107"
        message = "000800"  # swich from 800 to 700 ul to prevent air bubble
        self.SendCommand(task, message)

        # Flush Volume (ul)
        task = "0111"
        message = "000030"
        self.SendCommand(task, message)

        # Needle Height (mm)
        task = "0130"
        message = "000020"
        self.SendCommand(task, message)

        # Full Loop injection
        task = "0124"
        message = "000002"
        self.SendCommand(task, message)

        # Air Segment (yes==1  no==0)
        task = "0192"
        message = "000000"
        self.SendCommand(task, message)

        # Wash between (vials or injections)
        task = "0500"
        message = "000002"
        self.SendCommand(task, message)

        # Skip missing sample
        task = "0193"
        message = "000001"
        self.SendCommand(task, message)

        # Syringe Speed
        task = "0131"
        message = "000002"
        self.SendCommand(task, message)

        # Number of Injections
        task = "0112"
        message = "000001"
        self.SendCommand(task, message)

        # finish this part by moving tray to the front
        self.MoveTray('front')

    def MoveTray(self, position):
        # move the tray of the autosampler to the back or front position
        self.logger = logging.getLogger('AutosamplerLog')
        task = "0830"
        if position == 'front':
            message = "000001"
            self.logger.debug('Tray is moved to the front.')
            Move = True
        elif position == 'back':
            message = "000000"
            self.logger.debug('Tray is moved to the back.')
            Move = True
        else:
            self.logger.error('Position parameter was wrong.')
            Move = False
        if Move:
            self.SendCommand(task, message)
            task = "5100"
            message = "100000"
            send = 0
            self.SendCommand(task, message, send)

    def SetExperiments(self, numberOfExperiments):
        # sets the wash volume, time between analysis
        # and the first and last sample position to the autosampler
        self.logger.info('Function Set Experiments has been called.')

        # set settings for experiment
        # Wash Volume (times syringe)
        task = "0501"
        message = "000003"
        self.SendCommand(task, message)

        # Analysis Time message =[ 0.hr-min.min-sec.sec]
        task = "0100"
        message = "000530"  # 7 min minus the fill time of 1.5 min
        self.SendCommand(task, message)

        # First Sample
        task = "0108"
        message = "010001"
        self.SendCommand(task, message)

        # Last Sample
        task = "0109"
        vialRow = int((numberOfExperiments - 1) / 8)
        vialCol = int((numberOfExperiments - 1) % 8) + 1
        message = "010{0}0{1}".format(vialRow, vialCol)
        self.SendCommand(task, message)

    def CurrentSample(self):
        
        self.logger.debug('Current sample is asked by the main script.')
        task = "1001"
        message = "000150"
        send = 0
        answer = self.SendCommand(task, message, send)
        task = answer[5:-7]
        if task == "0150":
            # Plate
            plateCode = answer[10:-5]
            if plateCode == "1":
                plate = "left"
            elif plateCode == "2":
                plate = "right"
            else:
                plate = "not known"

            # Vial
            vailLetter = int(answer[11:-3])
            letter = chr(65 + vailLetter)
            vialNumber = answer[14:-1]
            outcome = "{0}{1} - {2} plate".format(letter, vialNumber, plate)
            self.logger.debug('The plateCode of Current sample is: {}'.format(outcome))
            return outcome

    def StartAutosampler(self):
        task = "5100"
        message = "000001"
        send = 0
        self.SendCommand(task, message, send)
        self.logger.debug('Autosampler has started the experiment')

class Pump(Device):
    def __init__(self, comnumber=1, baudrate=9600, name='Jack'):
        super().__init__(comnumber, baudrate, name)
        self.pumpOn = False
        self.SetRemote()

    def SetRemote(self):
        try:
            message = 'REMOTE\r'
            self.SendCommand(message)
        except:
            messagebox.showerror('Error Setting Remote',
                                 'There was an error during sending the remote command. \n '
                                 'Run the script again.')
            self.logger.error('Error during sending Remote', exc_info=True)
            quit(1)

    def SendCommand(self, message):
        message = str.encode(message)
        repeat = True
        while repeat:
            self.serialObj.write(message)
            time.sleep(0.)
            while True:
                answer = self.serialObj.readline()
                if len(answer) > 0:
                    break
                time.sleep(0.)
                self.logger.debug('The pump did not respond yet.')

            answer = answer.decode()
            if "OK" in answer:  # check if command is received and done
                repeat = False
                print('{0} gave {1}'.format(self.name, answer))
                self.logger.debug('{0} gave {1}'.format(self.name, answer))
            else:
                print('{0} had an error and gave {1}'.format(self.name, answer))
                self.logger.debug('{0} had an error and gave {1}'.format(self.name, answer))
                repeat = True

class SyringePump(Device):
    def __init__(self, comnumber=1, baudrate=9600, name='Jack', diameter=20.0, numberOfSyringes=1):
        super().__init__(comnumber, baudrate, name)
        self.diameter = diameter
        self.NSyringes = numberOfSyringes
        self.SetRemote()

    def SetRemote(self):
        message = 'set diameter {0}\r\n'.format(self.diameter)
        self.SendCommand(message)
        self.logger.debug('The diameter of pump: {} has been set to: {}'.format(self.name, self. diameter))

    def SendCommand(self, message):
        message = str.encode(message)
        repeat = True
        while repeat:
            self.serialObj.write(message)
            time.sleep(0.)
            while True:
                answer = self.serialObj.readline()
                if len(answer) > 0:
                    repeat = False
                    break
                time.sleep(0.)
                self.logger.debug('The pump did not respond yet.')
            answer = answer.decode()
            self.logger.debug('{0} gave {1}'.format(self.name, answer))

    def SetFlowrate(self, flowrate):
        actualRate = round(float(flowrate) / self.NSyringes, 0)
        message = 'set rate {}\r\n'.format(str(actualRate))
        self.SendCommand(message)
        self.logger.debug('Pump: {} is set to flowrate: {}'.format(self.name, flowrate))

    def StopPump(self):
        message = 'stop\r\n'
        self.SendCommand(message)
        self.logger.debug('Pump: {} has been stopped'.format(self.name))

class HPLCPumpAzura(Pump):
    def SetFlowrate(self, flowrate):
        message = 'FLOW {0}.00\r'.format(flowrate)
        self.SendCommand(message)
        self.logger.debug('Pump: {} is set to flowrate:'
                          ' {}'.format(self.name, flowrate))

        message = 'ON\r'
        self.SendCommand(message)
        self.logger.debug('Pump: {} is set on'.format(self.name))
        self.pumpOn = True

    def StopPump(self):
        message = 'OFF\r'
        self.SendCommand(message)
        self.logger.debug('Pump: {} has been stopped'.format(self.name))
        self.pumpOn = False

class HPLCPumpSmartline(Pump):
    def SetFlowrate(self, flowrate):
        message = "RAMP:0,{0},100,0,0,0,0,0,0,0,0,0,0,0,0\r".format(int(flowrate))
        self.SendCommand(message)
        self.logger.debug('Pump: {} is set to flowrate:'
                          ' {}'.format(self.name, flowrate))

    def StopPump(self):
        message = "stop\r"
        self.SendCommand(message)
        self.logger.debug('Pump: {} has been stopped'.format(self.name))

if __name__ == '__main__':
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')