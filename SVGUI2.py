from tkinter import *
import subprocess
from tkinter import messagebox
import time
import datetime
import logging
from Parameters_SV import ImportparSV
import threading

class SVInterface2:
    def __init__(self, par):
        self.logger = logging.getLogger('SternVolmerLog')
        self.logger.info('GUI1 has been created')
        self.root = Tk()
        self.root.title('Experiment settings')
        self.par = par
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()
        self.startTime = time.time()

        # group logo
        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=1, columnspan=4)

        self.label1 = Label(self.frame, font=(self.font1, self.size))
        self.label1.configure(text=" ", bg='#1D265E', fg='white', bd=6, width=80)
        self.label1.grid(row=2, columnspan=2)

        self.empty1 = Label(self.frame, font=(self.font1, self.size))
        self.empty1.configure(text=" ", bg='white')
        self.empty1.grid(row=3)
        self.logger.debug('Group logo created')

        # create a button for opening avasoft
        self.label01 = Label(self.frame, font=(self.font1, self.size), anchor=W)
        self.label01.configure(text="Do you want to open Avasoft? ", fg='#1D265E', bg='white', width=30)
        self.label01.grid(row=4, sticky='W')

        self.but1 = Button(self.frame, font=(self.font1, self.size))
        self.but1.configure(text="Open Avasoft", width=15, command=self.OpenAvasoft, bg='#1D265E', fg='white')
        self.but1.grid(row=4, column=1, columnspan=2)

        self.label2 = Label(self.frame, font=(self.font1, self.size), anchor=W)
        self.label2.configure(text="Do you want to open LEDDriver?", fg='#1D265E', bg='white', width=30)
        self.label2.grid(row=5, sticky="W")

        self.but2 = Button(self.frame, font=(self.font1, self.size))
        self.but2.configure(text="Open LEDDriver", width=15, command=self.OpenLEDDriver, bg='#1D265E', fg='white')
        self.but2.grid(row=5, column=1, columnspan=2)

        self.empty2 = Label(self.frame, font=(self.font1, self.size))
        self.empty2.configure(text=" ", bg='white')
        self.empty2.grid(row=6)

        # create the reminders
        self.label3 = Label(self.frame, font=(self.font1, self.size), anchor=W)
        self.label3.configure(text="Turn the lamp ON", fg='#1D265E', bg='white', width=30)
        self.label3.grid(row=7, sticky="W")
        self.logger.debug('opening window has been created')

        self.label4 = Label(self.frame, font=(self.font1, self.size))
        self.label4.configure(text="Set Time Series in Avasoft", fg='#1D265E', bg='white')
        self.label4.grid(row=8, sticky="W")
        self.logger.debug('Time series has been asked for')

        # create Avasoft name field
        self.label5 = Label(self.frame, font=(self.font1, self.size), anchor=W)
        self.label5.configure(text="Name output file Avasoft (.txt)", fg='#1D265E', bg='white')
        self.label5.grid(row=9, sticky="W")

        self.name = StringVar()
        self.name.set(self.par.nameTxtFile)
        self.nameOutput = Entry(self.frame, textvariable=self.name, width=35)
        self.nameOutput.grid(row=9, column=1)

        self.but5 = Button(self.frame, font=(self.font1, self.size))
        self.but5.configure(text="OK", width=15, command=self.StartExperiments, bg='#1D265E', fg='white')
        self.but5.grid(row=10, column=1, columnspan=2)

        self.empty5 = Label(self.frame, font=(self.font1, self.size))
        self.empty5.configure(text=" ", bg='white')
        self.empty5.grid(row=11)
        self.logger.debug('Avasoft text file banner has been created')

    # opens avasoft
    @staticmethod
    def OpenAvasoft():
        subprocess.Popen(r"C:\Program Files (x86)\Avasoft8\Avasoft8.exe")

    # opens the software of the LED
    @staticmethod
    def OpenLEDDriver():
        subprocess.Popen(r"C:\Program Files (x86)\Mightex LEDDriver\LEDDriver.exe")

    # when time series is called it transforms the GUI
    # TimeSeries calls the functions NameTs and start experiment
    # in sequence, so the user can not do damage to the data.
    def StartExperiments(self):
        self.but5.destroy()
        self.empty5.destroy()

        self.label6 = Label(self.frame, font=(self.font1, self.size))
        self.label6.configure(text="Have moment of patience until the flow is fully developed", fg='#1D265E', bg='#fd9200')
        self.label6.grid(row=11, sticky="WE", columnspan=3)

        self.empty6 = Label(self.frame, font=(self.font1, self.size))
        self.empty6.configure(text=" ", bg='white')
        self.empty6.grid(row=12)

        # Update interface
        self.frame.update()

        waitingForFlowDevelopment = self.par.resTimeDv + self.startTime - time.time()
        if waitingForFlowDevelopment < 0:
            waitingForFlowDevelopment = 1

        # create multiprocessing event and worker
        threadFlowDevelompent = threading.Thread(target=self.waitingThread, args=(waitingForFlowDevelopment,))
        self.logger.debug('Main loop thread created.')

        threadFlowDevelompent.start()
        while True:
            time.sleep(0.3)
            self.root.update()

            if not threadFlowDevelompent.is_alive():
                self.root.update()
                break

        self.logger.debug('Gui done sleeping')

        self.frame.update()
        self.label6.destroy()

        self.label6 = Label(self.frame, font=(self.font1, self.size), anchor=W)
        self.label6.configure(text="Start experiments", fg='#1D265E', bg='white')
        self.label6.grid(row=11, sticky="W")

        self.SettingsReady()

    def SettingsReady(self):
        try:
            self.par.nameOutputAvas = str(self.nameOutput.get())
            self.check10 = 1
        except ValueError:
            self.check10 = 0
            messagebox.showwarning('Warning', 'Name of output file is Not OK')
            self.logger.error('Name of the output file is not OK')

        testTxt = self.par.nameOutputAvas[-4:]
        if '.txt' in testTxt:
            self.check11 = 1
        else:
            self.check11 = 0
            messagebox.showwarning('Name output file', 'The output file needs to end with .txt')
            self.logger.error('the output file does not end with .txt')

        currentTime = time.time()
        runTime = self.par.numberOfConcentrations * (self.par.numberOfMeasurmentsPerConcentration - 1) * self.par.interval + self.par.resTimeDv * self.par.numberOfConcentrations
        finalTime = currentTime + runTime
        t = datetime.datetime.fromtimestamp(float(finalTime))
        fmt = "%H:%M:%S"
        finalTg = str(t.strftime(fmt))

        messageEndTime = "Expected end time of measurements : \n {}".format(finalTg)
        self.logger.debug("Expected end time of measurements : {}".format(finalTg))

        if self.check10 and self.check11 == 1:
            # messagebox.showinfo('End time', messageEndTime)
            self.root.quit()
            self.root.destroy()

    @staticmethod
    def waitingThread(pauzetime):
        time.sleep(pauzetime)
        pass

if __name__ == '__main__':
    logger = logging.getLogger('SternVolmerLog')
    logging.basicConfig(filename='SternVolmerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparSV()
    par.nameExperiment = 'excelfile'
    par.nameTxtFile = 'file.txt'
    par.numberOfConcentrations = 6
    par.numberOfMeasurmentsPerConcentration = 10
    par.interval = 1
    par.resTimeDv = 20
    par.resTimeDv = 20
    gui1 = SVInterface2(par)
    gui1.root.mainloop()