from tkinter import *
from math import pi
from tkinter import messagebox
from DatabaseCommander import DatabaseHandler
import numpy as np
import time
import datetime
import logging
from Parameters_SV import ImportparSV
import sqlite3 as lite

class SVInterface1:
    def __init__(self, par):
        self.logger = logging.getLogger('SternVolmerLog')
        self.logger.info('GUI1 has been created')
        self.root = Tk()
        self.root.title('Set Parameters')

        self.par = par
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'
        # creating self.frame and adding that to self
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()

        self.connection = lite.connect(self.par.databaseName)
        self.cursor = self.connection.cursor()

        # creating photo and adding that to a label
        # which is than added to the self.frame in a grid layout
        # code for creating the .ppm picture and rescaling it
        # image = Image.open('NRGLogo.png')
        # image = image.resize((183, 78), Image.ANTIALIAS)
        # image.save('NRGLogo.ppm', 'ppm')
        line = 1
        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=line, columnspan=4)
        self.logger.debug('Photo label has been created')
        line+=1

        # adding the first banner to the self.frame,
        # determining the with of the screen
        self.label = Label(self.frame,
                           font=(self.font1, self.size),
                           text="Give the desired parameters of the system",
                           bg='#1D265E', fg='white', bd=6, width=130)
        self.label.grid(row=line, columnspan=4)
        line += 1
        self.label1A = Label(self.frame, text=" ", fg='#1D265E', bg='white')
        self.label1A.grid(row=line)
        self.logger.debug('Give parameter banner created')
        line += 1

        # ask for excel save file data
        self.label9A = Label(self.frame, font=(self.font1, self.size))
        self.label9A.configure(text="Name of experiment", fg='#1D265E', bg='white')
        self.label9A.grid(row=line, sticky="W")

        self.intG9 = IntVar()
        self.intG9.set(self.par.setNameFile)
        self.nameFile = Entry(self.frame, textvariable=self.intG9, width=25)
        self.nameFile.grid(row=line, column=2)

        self.label9B = Label(self.frame, font=(self.font1, self.size))
        self.label9B.configure(text="", fg='#1D265E', bg='white')
        self.label9B.grid(row=line, column=3, sticky=W)
        self.logger.debug('Name excelfile field created')
        line += 1

        # add a label to ask for desired flow rate, add standard value of 1000
        self.label2A = Label(self.frame,
                             font=(self.font1, self.size),
                             text="Desired total throughput of the system",
                             fg='#1D265E', bg='white')
        self.label2A.grid(row=line, sticky='W')
        self.intG2 = IntVar()
        self.intG2.set(self.par.setTotalFlowRate)
        self.speed = Entry(self.frame, textvariable=self.intG2, width=25)
        self.speed.grid(row=line, column=2)
        self.label2B = Label(self.frame,
                             font=(self.font1, self.size),
                             text=(u'\u03bc' + 'l/min'),
                             fg='#1D265E', bg='white')
        self.label2B.grid(row=line, column=3, sticky="W")
        self.logger.debug('Set flow rate, created')
        line += 1

        # ask for the amount of concentrations to test
        self.label4A = Label(self.frame, font=(self.font1, self.size))
        self.label4A.configure(text="Number of concentrations to test", fg='#1D265E', bg='white')
        self.label4A.grid(row=line, sticky="W")

        self.intG4 = IntVar()
        self.intG4.set(self.par.setConLoop)
        self.nConcen = Entry(self.frame, textvariable=self.intG4, width=25)
        self.nConcen.grid(row=line, column=2)

        self.label4B = Label(self.frame, font=(self.font1, self.size))
        self.label4B.configure(text="", fg='#1D265E', bg='white')
        self.label4B.grid(row=line, column=3)
        self.logger.debug('Number of concentrations field crated')
        line += 1

        # number of experiments at each concentration
        self.label5A = Label(self.frame, font=(self.font1, self.size))
        self.label5A.configure(text="Number of measurements per concentration", fg='#1D265E', bg='white')
        self.label5A.grid(row=line, sticky="W")

        self.intG5 = IntVar()
        self.intG5.set(self.par.setRepeatConLoop)
        self.nMeasure = Entry(self.frame, textvariable=self.intG5, width=25)
        self.nMeasure.grid(row=line, column=2)

        self.label5B = Label(self.frame, font=(self.font1, self.size))
        self.label5B.configure(text="", fg='#1D265E', bg='white')
        self.label5B.grid(row=line, column=3)
        self.logger.debug('Number of measurements taken at each concentration')
        line += 1

        # time to be taken between measurements
        self.label6A = Label(self.frame, font=(self.font1, self.size))
        self.label6A.configure(text="Time between measurements", fg='#1D265E', bg='white')
        self.label6A.grid(row=line, sticky="W")

        self.intG6 = IntVar()
        self.intG6.set(self.par.setTimeBetweenMeasurments)
        self.pauseTime = Entry(self.frame, textvariable=self.intG6, width=25)
        self.pauseTime.grid(row=line, column=2)

        self.label6B = Label(self.frame, font=(self.font1, self.size))
        self.label6B.configure(text="s", fg='#1D265E', bg='white')
        self.label6B.grid(row=line, column=3, sticky="W")
        self.logger.debug('Time to be taken between measurments field is crated')
        line += 1

        # empty line for style reasons
        self.empty0 = Label(self.frame)
        self.empty0.configure(text=" ", fg='#1D265E', bg='white')
        self.empty0.grid(row=line, column=1)
        line += 1

        # quencher concentration
        self.label7A = Label(self.frame, font=(self.font1, self.size))
        self.label7A.configure(text="Quencher concentration", fg='#1D265E', bg='white')
        self.label7A.grid(row=line, sticky="W")

        self.intG7 = IntVar()
        self.intG7.set(self.par.quenSolv)
        self.quenCon = Entry(self.frame, textvariable=self.intG7, width=25)
        self.quenCon.grid(row=line, column=2)

        self.label7B = Label(self.frame, font=(self.font1, self.size))
        self.label7B.configure(text="M", fg='#1D265E', bg='white')
        self.label7B.grid(row=line, column=3, sticky="W")
        self.logger.debug('Quencher concentration field created')
        line += 1

        # name quencher
        self.label8A = Label(self.frame, font=(self.font1, self.size))
        self.label8A.configure(text="Name Quencher", fg='#1D265E', bg='white')
        self.label8A.grid(row=line, sticky="W")

        self.intG8 = IntVar()
        self.intG8.set(self.par.setNameQuencher)
        self.nameQuen = Entry(self.frame, textvariable=self.intG8, width=25)
        self.nameQuen.grid(row=line, column=2)
        self.logger.debug('quencher name field created')
        line += 1

        # create the dropdown menus for cat
        self.label11 = Label(self.frame, font=(self.font1, self.size))
        self.label11.configure(text="Name Catalyst", fg='#1D265E', bg='white')
        self.label11.grid(row=line, sticky="W")

        optionListCat, optionListSol = self.MakeDropdowns()
        self.varDropDownCat = StringVar()
        self.varDropDownCat.set(optionListCat[0])
        self.dropDownCat = OptionMenu(self.frame, self.varDropDownCat, *optionListCat)
        self.dropDownCat.config(bg='white', bd=1, width=20, fg='#1D265E',
                                background='white', activebackground='white')
        self.dropDownCat['menu'].config(bg='white', fg='#1D265E')
        self.dropDownCat.grid(row=line, column=2, columnspan=1)
        self.logger.debug('Dropdown for the Cat menu has been created')
        line += 1

        # create drop down for solvent
        self.label12 = Label(self.frame, font=(self.font1, self.size))
        self.label12.configure(text="Name Solvent", fg='#1D265E', bg='white')
        self.label12.grid(row=line, sticky="W")

        self.varDropDownSol = StringVar()
        self.varDropDownSol.set(optionListSol[0])
        self.dropDownSol = OptionMenu(self.frame, self.varDropDownSol, *optionListSol)
        self.dropDownSol.config(bg='white', bd=1, width=20, fg='#1D265E',
                                background='white', activebackground='white')
        self.dropDownSol['menu'].config(bg='white', fg='#1D265E')
        self.dropDownSol.grid(row=line, column=2, columnspan=1)
        self.logger.debug('Dropdown for the Solvent menu has been created')
        line += 1

        # # ask for extra I0 measurement
        # self.label20A = Label(self.frame, font=(self.font1, self.size))
        # self.label20A.configure(text="Extra I" + u'\u2080' + " Measurement", fg='#1D265E', bg='white')
        # self.label20A.grid(row=line, sticky="W")

        self.getExtraI0 = BooleanVar()
        self.getExtraI0.set(False)
        # self.checkmark1 = Checkbutton(self.frame, variable=self.getExtraI0, onvalue=True, offvalue=False)
        # self.checkmark1.configure(fg='#1D265E', bg='white')
        # self.checkmark1.grid(row=line, column=2)
        # self.logger.debug('checkbox for extraI0 created')
        # line += 1

        # empty line for style reasons
        self.empty0 = Label(self.frame)
        self.empty0.configure(text=" ", fg='#1D265E', bg='white')
        self.empty0.grid(row=line, column=1)
        line += 1

        # ask for email address / conformation
        self.label10A = Label(self.frame, font=(self.font1, self.size))
        self.label10A.configure(text="email address", fg='#1D265E', bg='white')
        self.label10A.grid(row=line, sticky="W")

        self.intG10 = IntVar()
        self.intG10.set(self.par.email)
        self.email = Entry(self.frame, textvariable=self.intG10, width=25)
        self.email.grid(row=line, column=2)

        self.label10B = Label(self.frame, font=(self.font1, self.size))
        self.label10B.configure(text="", fg='#1D265E', bg='white')
        self.label10B.grid(row=line, column=3, sticky=W)
        self.logger.debug('mail address field created')
        line += 1

        # create bottom line button which calls check do for final command
        self.nextStageButton = Button(self.frame, font=(self.font1, self.size))
        self.nextStageButton.configure(text='OK', width=15, command=self.CheckDo, bg='#1D265E', fg='white')
        self.nextStageButton.grid(row=line, column=1)
        line += 1

        self.empty1 = Label(self.frame)
        self.empty1.configure(text=" ", fg='#1D265E', bg='white')
        self.empty1.grid(row=line, column=0, columnspan=4, sticky="W")
        line += 1

        # make new section with output parameters
        self.label13 = Label(self.frame, font=(self.font1, self.size))
        self.label13.configure(text=" Output Parameters ", bg='#1D265E', fg='white', bd=6, width=130)
        self.label13.grid(row=line, columnspan=4, sticky="W")
        line += 1

        self.empty2 = Label(self.frame, font=(self.font1, self.size))
        self.empty2.configure(text=" ", fg='#1D265E', bg='white')
        self.empty2.grid(row=line, sticky="W")
        line += 1

        # reveal estimate time of experiment
        self.label14A = Label(self.frame, font=(self.font1, self.size))
        self.label14A.configure(text="Approximation time that experiments are ready", fg='#1D265E', bg='white')
        self.label14A.grid(row=line, sticky="W")

        self.intG14 = IntVar()
        self.finalTime = Entry(self.frame, textvariable=self.intG14, width=25)
        self.finalTime.grid(row=line, column=2)
        line += 1

        # show catalyst concentrations
        self.label16A = Label(self.frame, font=(self.font1, self.size))
        self.label16A.configure(text="Catalyst concentrations that will be tested (M)", fg='#1D265E', bg='white')
        self.label16A.grid(row=line, sticky="W")
        line += 1

        self.concentration = Text(self.frame, wrap=WORD, height=3, font=(self.font1, self.size))
        self.concentration.grid(row=line, column=1, columnspan=3)
        self.logger.debug('list of concentrations is printed')
        line += 1

        # ask for flow rates of different pumps
        self.label17A = Label(self.frame, font=(self.font1, self.size))
        self.label17A.configure(text="Solvent Pump", fg='#1D265E', bg='white')
        self.label17A.grid(row=line, column=1)

        self.label17B = Label(self.frame, font=(self.font1, self.size))
        self.label17B.configure(text="Quencher Pump", fg='#1D265E', bg='white')
        self.label17B.grid(row=line, column=2)

        self.label17C = Label(self.frame, font=(self.font1, self.size))
        self.label17C.configure(text="Catalyst Pump", fg='#1D265E', bg='white')
        self.label17C.grid(row=line, column=3)
        line += 1

        self.label18A = Label(self.frame, font=(self.font1, self.size))
        self.label18A.configure(text="Approximation of volume needed (ml)", fg='#1D265E', bg='white')
        self.label18A.grid(row=line, sticky="W")

        self.intG18A = IntVar()
        self.VolSy_p1 = Entry(self.frame, textvariable=self.intG18A, width=25)
        self.VolSy_p1.grid(row=line, column=1)

        self.intG18B = IntVar()
        self.VolSy_p2 = Entry(self.frame, textvariable=self.intG18B, width=25)
        self.VolSy_p2.grid(row=line, column=2)

        self.intG18C = IntVar()
        self.VolSy_p3 = Entry(self.frame, textvariable=self.intG18C, width=25)
        self.VolSy_p3.grid(row=line, column=3)
        line += 1

        self.label19A = Label(self.frame, font=(self.font1, self.size))
        self.label19A.configure(text=" ", fg='white', bg='white')
        self.label19A.grid(row=line, column=1)
        self.logger.debug('fields have been created that ask for different pumps'
                          ' each of these fields return an estimate')
        line += 1

        # testing buttons
        self.quitButton = Button(self.frame, font=(self.font1, self.size),
                                 text="Quit", command=self.Quit,
                                 width=15, bg='#1D265E', fg='white')
        self.quitButton.grid(row=line, column=1)
        line += 1

    # checks if everything is filled in and gives warnings if errors occur
    def WarningCheck(self):
        try:
            self.par.totalThroughput = int(self.speed.get())
        except ValueError:
            messagebox.showwarning('Warning', 'Throughput of the system is Not OK')
            self.logger.error('Throughput could not be read')
            return False

        # read values for concentration loop
        try:
            self.par.numberOfConcentrations = int(self.nConcen.get())
        except ValueError:
            messagebox.showwarning('Warning', 'Number of concentrations is Not OK')
            self.logger.error('Number of concentrations could not be read')
            return False

        # read amount of experiments per concentration
        try:
            self.par.numberOfMeasurmentsPerConcentration = int(self.nMeasure.get())
        except ValueError:
            messagebox.showwarning('Warning', 'Number of measurements per concentration is Not OK')
            self.logger.error('Number of measurements could not be read')
            return False

        # get interval
        try:
            self.par.interval = int(self.pauseTime.get())
            if self.par.interval < 1:
                self.logger.error('Interval is smaller than 1')
                return False
        except ValueError:
            messagebox.showwarning('Warning', 'Time between measurements is Not OK')
            self.logger.error('Time between measurements could not be read')
            return False

        # get quenching solution concentration
        try:
            self.par.concentrationQuen = float(self.quenCon.get())
            self.par.maxConcentrationQuen = self.par.concentrationQuen * self.par.partSolQuen
        except ValueError:
            messagebox.showwarning('Warning', 'Quencher concentration is Not OK')
            self.logger.error('Quencher concentration could not be read')
            return False

        # get name quencher
        try:
            self.par.quencherName = str(self.nameQuen.get())
        except ValueError:
            messagebox.showwarning('Warning', 'Name Quencher is Not OK')
            self.logger.error('Quencher name could not be read')
            return False

        # get name catalyst
        try:
            self.par.catalystName = self.varDropDownCat.get()
        except ValueError:
            messagebox.showwarning('Warning', 'Name Catalyst is Not OK')
            self.logger.error('Catalyst name could not be read')
            return False

        # get name Solvent
        try:
            self.par.solventName = self.varDropDownSol.get()
        except ValueError:
            messagebox.showwarning('Warning', 'Name Solvent is Not OK')
            self.logger.error('Solvent name could not be read')
            return False

        # get mail
        try:
            self.par.email = str(self.email.get())
        except ValueError:
            messagebox.showwarning('Warning', 'Email name is Not OK')
            self.logger.error('Email could not be read')
            return False

        # excel file name
        try:
            self.par.nameExperiment = str(self.nameFile.get())
            self.par.nameTxtFile = "{}{}".format(self.par.nameExperiment, '.txt')
            self.par.nameExcelFile = "{}{}".format(self.par.nameExperiment, '.xlsx')
        except ValueError:
            messagebox.showwarning('Warning', 'File name is Not OK')
            self.logger.error('Excel file name could not be read')
            return False

        return True

    # this function creates the throughput vectors for the pumps
    def ThroughputCalculations(self):
        fracQuenPump0 = self.par.partSolQuen
        self.par.fractionSolventPump = []
        self.par.fractionQuencherPump = []
        speedError1 = int(0)
        speedError2 = int(0)

        # linStepSize = float(self.par.maxConcentrationQuen / (self.par.numberOfConcentrations-1))
        linFractionstep = self.par.partSolQuen/(self.par.numberOfConcentrations-1)

        for u in range(1, self.par.numberOfConcentrations - 1):
            fracQuenPump = fracQuenPump0 - u*linFractionstep
            fracSolventPump = self.par.partSolQuen - fracQuenPump

            # flip fractions for reverse concentration measurement
            #fracQuenPump = self.par.partSolQuen-fracQuenPump
            #fracSolventPump = self.par.partSolQuen-fracSolventPump

            # calculate flow rates
            throughSolventPump = float(fracSolventPump * self.par.totalThroughput)
            throughQuenPump = float(fracQuenPump * self.par.totalThroughput)

            # check if flow is to small for pumps to handle
            if 0.0 < throughSolventPump < 1.0:
                fracSolventPump = (1.0 / float(self.par.totalThroughput))
                fracQuenPump = self.par.partSolQuen - fracSolventPump
                speedError1 += 1
                self.logger.error('Error in throughput solvent pump')

            if 0.0 < throughQuenPump < 1.0:
                fracQuenPump = (1.0 / float(self.par.totalThroughput))
                fracSolventPump = self.par.partSolQuen - fracQuenPump
                speedError2 += 1
                self.logger.error('Error in throughput quencher pump')

            self.par.fractionSolventPump.append(fracSolventPump)
            self.par.fractionQuencherPump.append(fracQuenPump)

        if speedError2 > 1:
            speedError2 -= 1
            self.par.numberOfConcentrations -= speedError2
            messagebox.showinfo('Number of Concentrations',
                                ('The number of concentrations that will be tested is changed to '
                                 '' + self.par.numberOfConcentrations + ' due to speed limit of quencher pump.'))
            self.logger.info('The number of concentrations that will be tested is changed to '
                             '' + self.par.numberOfConcentrations + ' due to speed limit of quencher pump.')

            for i in range(0, speedError2):
                self.par.fractionSolventPump.pop(-1)
                self.par.fractionQuencherPump.pop(-1)

        if speedError1 > 1:
            speedError1 -= 1
            self.par.numberOfConcentrations -= speedError1
            messagebox.showinfo('Number of Concentrations',
                                ('The number of concentrations that will be tested is changed to '
                                 '' + self.par.numberOfConcentrations + ' due to speed limit of solvent pump.'))
            self.logger.info('The number of concentrations that will be tested is changed to '
                             '' + self.par.numberOfConcentrations + ' due to speed limit of solvent pump.')

            for j in range(0, speedError1):
                self.par.fractionSolventPump.pop(0)
                self.par.fractionQuencherPump.pop(0)

        self.par.fractionSolventPump.reverse()
        self.par.fractionQuencherPump.reverse()

        self.par.fractionSolventPump.insert(0, self.par.partSolQuen)
        self.par.fractionSolventPump.append(0)

        self.par.fractionQuencherPump.insert(0, 0)
        self.par.fractionQuencherPump.append(self.par.partSolQuen)

        # Extra I0 at the end
        self.par.ExtraI0 = self.getExtraI0.get()

        if self.par.ExtraI0:
            self.par.fractionSolventPump.append(self.par.partSolQuen)
            self.par.fractionQuencherPump.append(0)
            self.par.numberOfConcentrations += 1

    # checks if the flow rates, that are send to the pumps,
    # are correct / do not damage the pumps
    def FlowRateCheck(self):
        # calculate concentrations
        self.par.con = self.par.concentrationQuen * np.array(self.par.fractionQuencherPump)
        self.concentration.delete(0.0, END)
        self.concentration.insert(0.0, self.par.con)

        # check if flow rates are okay
        throughputSolventPump = (np.array(self.par.fractionSolventPump) * self.par.totalThroughput)
        throughputQuenPump = (np.array(self.par.fractionQuencherPump) * self.par.totalThroughput)

        for h in range(0, self.par.numberOfConcentrations):
            if 0.0 < throughputSolventPump[h] < 1.0 or 0.0 < throughputQuenPump[h] < 1.0:
                messagebox.showwarning('Warning', 'Speed minimum of pump reached. Change the parameters')
                self.logger.error('Speed minimum of pump reached. Change the parameters')
                return False
            if 5000.0 < throughputSolventPump[h] or 5000.0 < throughputQuenPump[h] < 1.0:
                messagebox.showwarning('Warning', 'Speed maximum of the system reached. Change the parameters')
                self.logger.error('Speed maximum of pump reached. Change the parameters')
                return False

        # check for diffusion limitation
        Pe = self.par.length * (self.par.totalThroughput / 6e10) * (4 / (pi * self.par.diameter ** 2)) / self.par.diff
        if Pe < 100:
            messagebox.showwarning('Warning', 'You are working in a diffusion limited regime!')
            self.logger.error('You are working in a diffusion limited regime!')
            return False

        # calculate flow rate of the pumps
        self.par.catThroughput = int(float(self.par.partCat * self.par.totalThroughput))

        # pump rate of solvent and cat
        self.par.solQuenThroughput = int(float(self.par.partSolQuen * self.par.totalThroughput))
        self.par.resTimeDv = (((self.par.length * (pi / 4) * self.par.diameter ** 2) / (self.par.totalThroughput *1e-9 / 60)) + (self.par.volumeFlowCel/self.par.totalThroughput) * 60) * self.par.cycleTime

        # calculate amount of material needed
        # amount of catalyst solution needed ( pump 3 )
        catDuringSv = (self.par.catThroughput * self.par.numberOfConcentrations * (self.par.numberOfMeasurmentsPerConcentration - 1) * (self.par.interval/60) + self.par.resTimeDv/60 * (self.par.numberOfConcentrations-1) * self.par.catThroughput) * 1.1
        self.par.totCatMl = round(float(catDuringSv) / float(1000), 2)

        # amount of quench + solvent needed (pump 1 and 3)
        solBeforeSv = self.par.timeToDoSettings * self.par.totalThroughput

        solDuringSv = 0
        quenDuringSv = 0

        for g in range(0, self.par.numberOfConcentrations):
            # change pump 1
            throughputSolventPumpInt = int(float(self.par.fractionSolventPump[g] * self.par.totalThroughput))
            throughputQuenPumpInt = int(float(self.par.fractionQuencherPump[g] * self.par.totalThroughput))

            amountSol = throughputSolventPumpInt * (self.par.numberOfMeasurmentsPerConcentration-1) * (self.par.interval/60) + throughputSolventPumpInt * self.par.resTimeDv/60
            amountQuen = throughputQuenPumpInt * (self.par.numberOfMeasurmentsPerConcentration - 1) * (self.par.interval / 60) + throughputQuenPumpInt * self.par.resTimeDv / 60

            solDuringSv += amountSol
            quenDuringSv += amountQuen

        self.par.totSolMl = round((solBeforeSv + solDuringSv) / 1000 * 1.1, 2)
        self.par.totQuenMl = round(quenDuringSv / 1000 * 1.1, 2)
        
        # insert amount of liquid in interface
        self.intG18A.set(self.par.totSolMl)
        self.intG18B.set(self.par.totQuenMl)
        self.intG18C.set(self.par.totCatMl)

        # insert final time in inteface
        currentTime = time.time()
        runTime = self.par.timeToDoSettings * 60 + self.par.numberOfConcentrations * (self.par.numberOfMeasurmentsPerConcentration-1) * self.par.interval + self.par.resTimeDv * self.par.numberOfConcentrations
        finalTime = currentTime + runTime
        t = datetime.datetime.fromtimestamp(float(finalTime))
        finalTimeGues = t.strftime('%H:%M:%S')
        date = datetime.datetime.fromtimestamp(currentTime)
        self.par.date = date.strftime('%Y/%m/%d')
        self.intG14.set(finalTimeGues)

        return True

    # communicate to database and see if lifetime exists
    def CheckLifetime(self):
        databaseCommander = DatabaseHandler(self.par.databaseName)
        data = (self.par.catalystName, self.par.solventName)
        self.par.lifetime = databaseCommander.AskForLifetime(data)

        if self.par.lifetime is None:
            self.empty1.configure(text="No lifetime is known for this catalyst solvent couple. No Kq will be calculated.",
                                  fg='#1D265E', bg=self.colorOrange,
                                  font=(self.font1, self.size + 2),
                                  bd=6, width=130)
        else:
            self.empty1.configure(text=" ", fg='#1D265E', bg='white')

        pass

    # combines all the checks for the system and gives the final go
    def CheckDo(self):
        if not self.WarningCheck():
            return False

        self.ThroughputCalculations()

        if not self.FlowRateCheck():
            return False

        self.CheckLifetime()

        if messagebox.askyesno('Measurements', 'Are the concentrations of quencher OK?'):
            self.root.destroy()
        else:
            return False

    def MakeDropdowns(self):
        listOfCat = []
        listOfSol = []
        self.cursor.execute("SELECT catalyst FROM Catalysts")
        rows = self.cursor.fetchall()

        for i in range(len(rows)):
            listOfCat.append(rows[i][0])

        self.cursor.execute("SELECT solvent FROM Solvents")
        rows = self.cursor.fetchall()

        for i in range(len(rows)):
            listOfSol.append(rows[i][0])

        return listOfCat, listOfSol

    def Quit(self):
        self.par.quit = True
        self.root.quit()
        self.root.destroy()
        exit()

if __name__ == '__main__':
    logger = logging.getLogger('SternVolmerLog')
    logging.basicConfig(filename='SternVolmerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparSV()
    gui1 = SVInterface1(par)
    gui1.root.mainloop()
    par = gui1.par

    print(par.fractionSolventPump)
    print(par.fractionQuencherPump)
    print(par.numberOfMeasurmentsPerConcentration)
    print(par.solventName)
    print(par.catalystName)