from tkinter import *
from Parameters_Auto import ImportparAuto
import SimpleOneTimeTask as ST
import datetime
import os
import sys
import time
import logging
import threading

class AutomationInterface2:
    def __init__(self, par, Autosampler, Solventpump, Catalystpump):
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('GUI2 has been created')

        self.root = Tk()
        self.root.title('Executing experiment')

        self.par = par
        self.autosampler = Autosampler
        self.solventPump = Solventpump
        self.catalystPump = Catalystpump
        self.font1 = "Roboto Condensed"
        self.size = 11
       
        # creating self.frame and adding that to self
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()

        # create logo
        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=1, columnspan=4)

        self.label1 = Label(self.frame, font=(self.font1, self.size))
        self.label1.configure(text=" ", bg='#1D265E', fg='white', bd=6, width=80)
        self.label1.grid(row=2, columnspan=2)

        self.empty1 = Label(self.frame, font=(self.font1, self.size))
        self.empty1.configure(text=" ", bg='white')
        self.empty1.grid(row=3)
        self.logger.debug('Group logo has been created')

        # creating textbox
        self.textbox = Text(self.frame, bg='white', font=(self.font1, self.size), state=DISABLED)
        self.textbox.grid(row=4, column=0, columnspan=5, sticky='E')
        self.textbox.tag_configure("stderr", foreground="#b22222")
        self.scrollbar = Scrollbar(self.frame)
        self.logger.debug('Textbox is created')

        # connect the scrollbar with the textbox
        self.scrollbar.configure(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=4, column=4, sticky=N + S + W)
        self.logger.debug('Scroll bar is created and linked to the textbox.')

        # redirect print statements to textbox
        self.stdoutOld = sys.__stdout__
        sys.stdout = TextRedirector(self.textbox, "stdout")
        self.logger.debug('stdout is redirected to the textbox')

        self.empty2 = Label(self.frame, font=(self.font1, self.size))
        self.empty2.configure(text=" ", bg='white')
        self.empty2.grid(row=5, column=0, columnspan=5, rowspan=2)

        # start the functions of the GUI
        self.textbox.insert(END, 'GUI3 has been initialized')
        self.root.update()

        # start flow development
        self.StartFlowDevelopmentWithThread()

    # waits for flow to establish
    # starts the cat pump and takes time stamp
    def StartFlowDevelopmentWithThread(self):
        # use multi processing to wait the correct amount of time
        # event signalling is used to let the program know that the pumps are ready
        # https://pymotw.com/3/multiprocessing/communication.html
        # https://www.ploggingdev.com/2017/01/multiprocessing-and-multithreading-in-python-3/

        waiting = round(self.par.resTimeAuto - (time.time() - self.par.time101) - self.par.timeCatFlow, 0)
        if waiting <= 0:
            waiting = 1
        self.logger.debug('Waiting time of first worker is set to: {}'.format(waiting))

        threadSolvent = threading.Thread(target=self.waitingThread, args=(waiting,))
        threadCat = threading.Thread(target=self.waitingThread, args=(self.par.timeCatFlow,))
        self.logger.debug('both the threads have been created')

        loopm = 0
        threadSolvent.start()
        self.logger.debug('The solvent thread has started')

        while True:
            time.sleep(1)
            self.root.update()
            if loopm % 25 == 0:
                waiting = round(self.par.resTimeAuto - (time.time() - self.par.time101), 0)
                print('Waiting for capillary to be cleaned and the flow to develop.\n '
                      'Estimated waiting time is: {}'.format(round(waiting, 2)))

                self.logger.debug('Waiting for capillary to be cleaned and the flow to develop.\n '
                                  'Estimated waiting time is: {}'.format(waiting))
                self.root.update()
                self.textbox.see(END)

            loopm += 1
            # check every loop instance if the pumps are ready
            if not threadSolvent.is_alive():
                print('The capillary is clean.\n Starting catalyst pump. \n')
                self.logger.debug('Solvent worker event is set to true.')
                break

        self.logger.debug('First waiting loop in StartFlowDevelopment has ended.')

        # start cat pump and next worker
        self.catalystPump.SetFlowrate(int(self.par.flowRateCat))

        threadCat.start()
        self.logger.debug('The Cat thread has started.')
        self.par.time101 = time.time()

        while True:
            time.sleep(1)
            self.root.update()
            if loopm % 25 == 0:
                waiting = round(self.par.timeCatFlow - (time.time() - self.par.time101), 0)
                print('Waiting for catalyst flow to develop.\n '
                      'Estimated waiting time is: {}'.format(round(waiting, 2)))
                self.root.update()
                self.textbox.see(END)

            loopm += 1
            # check every loop instance if the pumps are ready
            if not threadCat.is_alive():
                print('Catalyst pump is ready')
                self.root.update()
                self.textbox.see(END)
                break

        self.logger.debug('Second waiting loop in StartFlowDevelopment has ended.')
        # start the experiment
        print('\nStart experiment\n')

        self.root.update()
        self.textbox.see(END)

        # take time measurement
        self.ReadFirstData()

        # start main loop
        self.MainLoop()

    # this function reads the first data point from the Avasoft text file and saves the found results in par
    def ReadFirstData(self):
        self.logger.info('GUI2, function ReadFirstData, data is read from file')
        print('Reading data from Avasoft file ... ')

        # create parameters
        data = []

        # change working directory
        self.par.scriptDir = os.getcwd()
        self.par.dataDir = os.path.join(self.par.scriptDir, 'Data_Automation')
        self.par.workingDir = os.path.join(self.par.dataDir, self.par.name)
        ST.make_sure_path_exists(self.par.workingDir)

        # self.make_sure_path_exists(self.par.dataDir)
        os.chdir(self.par.dataDir)
        self.logger.debug('The data will be stored in: {}'.format(self.par.dataDir))

        # open and close file
        filePathFinal = os.path.join(self.par.dataDir, self.par.nameFileAvasoft)
        file = open(filePathFinal, "r")
        lines = file.readlines()
        file.close()
        # extract data
        endline = lines[-1]
        parts = endline.split(' ')
        for part in parts:
            try:
                data.append(float(part))
            except ValueError:
                continue
        self.par.dataStartTime = data[0]
        self.par.dataStartIntensity = data[1]
        # print found data to console
        print('Time from Avasoft file that experiment started was {}'.format(self.par.dataStartTime))
        print('The intensity found at this time is {}\n'.format(self.par.dataStartIntensity))
        self.logger.debug('Time from Avasoft file that experiment started was {}'.format(self.par.dataStartTime))
        self.logger.debug('The intensity found at this time is {}\n'.format(self.par.dataStartIntensity))
        self.root.update()
        self.textbox.see(END)

        # reset the working directory
        os.chdir(self.par.scriptDir)

        # save starting data to log file
        with open('Auto_StartData_Log.txt', 'a') as file:
            file.write("{0}\t{1}\t{2}\t\t{3}\t\t{4}\t\t{5}\n".format(self.par.date,
                                                                     self.par.name,
                                                                     self.par.catalystName,
                                                                     self.par.experimentNumber,
                                                                     self.par.dataStartTime,
                                                                     self.par.dataStartIntensity))

    # main loop that starts the experiment by giving this command to the autosampler
    # in each part of the loop it waits for 200 seconds and than asks the autosampler what it is doing
    def MainLoop(self):
        self.logger.info('GUI2, function MainLoop, main loop has started')

        print('Estimated waiting time for the experiment is: {} minutes'.format(
            str(round(7 + (self.par.experimentNumber - 1) * (self.par.timeBetweenInjects / 60), 2))))
        self.root.update()
        self.textbox.see(END)

        # start the Autosampler
        self.autosampler.StartAutosampler()
        print('Autosampler has started.')

        # set timers and loops
        startTimer1 = time.time()
        self.logger.debug('Time that the main loop is started is: {}'.format(startTimer1))
        loop3 = 0
        totalWaitingTimeMain = self.par.experimentNumber * self.par.timeBetweenInjects + 120
        self.logger.debug('The total time that the main '
                          'loop has to wait is estimated at : {}'.format(totalWaitingTimeMain))

        # create multiprocessing event and worker
        threadMain = threading.Thread(target=self.waitingThread, args=(totalWaitingTimeMain,))
        self.logger.debug('Main loop thread created.')

        threadMain.start()
        while True:
            time.sleep(0.3)
            self.root.update()
            if loop3 % 555 == 0:
                currentSample = self.autosampler.CurrentSample()
                currTime = datetime.datetime.now()
                print('The current sample is {} at time: '
                      '{}\n'.format(currentSample, currTime.strftime("%a - %H:%M:%S")))
                self.logger.debug('The current sample is {} at time: '
                                  '{}\n'.format(currentSample, currTime.strftime("%a - %H:%M:%S")))
                self.root.update()
                self.textbox.see(END)
            loop3 += 1

            if not threadMain.is_alive():
                print('Main measurement has ended.')
                self.logger.info('Main measurement loop has ended.')
                self.root.update()
                self.textbox.see(END)
                break

        # set end time and calculate how long the script ran.
        endTimer1 = time.time()
        print('This is how long the script ran {}'.format(endTimer1 - startTimer1))
        print('This is how long the script should have run {}'.format(totalWaitingTimeMain))
        self.logger.debug('This is how long the script ran {}'.format(endTimer1 - startTimer1))
        self.logger.debug('This is how long the script should have run {}'.format(totalWaitingTimeMain))

        # let solvent pump run in order to clean the cuvet
        print('The flow will continue on for 1 minute, just to make sure no sample is left behind.')
        for looppause in range(0, 700):
            if (looppause % 50) == 0:
                self.logger.debug('An additional pause loop is running for {}'.format(looppause))
            time.sleep(0.1)
            self.root.update()
            self.textbox.see(END)

        self.logger.info('Autosampler completed')
        self.root.update()
        self.textbox.see(END)

        # stop Pumps
        self.catalystPump.StopPump()
        self.solventPump.StopPump()
        print('Stopping pumps')
        self.logger.info('Stopping pumps')
        self.root.update()
        self.textbox.see(END)

        # put tray in front position
        position = 'front'
        self.autosampler.MoveTray(position)
        print('The sample tray is moved forward')
        self.root.update()
        self.textbox.see(END)

        print('This GUI will close itself after 10 seconds.')
        for loop2 in range(0, 100):
            time.sleep(0.1)
            self.root.update()

        # start next part of script
        self.Finalize()

    # returns the standard output to the screen
    # changes the working folder to the current folder /( not data folder)
    # and waits of 3 seconds to do this and self-terminate the GUI
    def Finalize(self):
        self.logger.info('GUI2, function Finalize, finalization of script.')

        os.chdir(self.par.scriptDir)
        sys.stdout = self.stdoutOld
        self.logger.info('Reset the working directory and the standard output before GUI2 gets destroyed')

        self.root.quit()
        self.root.destroy()

    @staticmethod
    def waitingThread(pauzetime):
        time.sleep(pauzetime)
        pass

 class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state=DISABLED)

    def flush(self):
        pass

if __name__ == '__main__':
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparAuto()
    par.time101 = 1000
    gui2 = AutomationInterface2(par, 'hi', 'durp', 'thing')
    gui2.root.mainloop()