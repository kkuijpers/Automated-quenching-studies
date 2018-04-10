from tkinter import *
import logging
from Parameters_Auto import ImportparAuto
from tkinter import messagebox
from ShowSampleGUI import ShowSample
import datetime
import sqlite3 as lite
import subprocess

class AutomationInterface1:
    def __init__(self, par):
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('GUI1 has been created')
        self.root = Tk()
        self.root.title('Set Parameters')

        self.par = par
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'


        # set up database connection
        self.connection = lite.connect(self.par.databaseName)
        self.cursor = self.connection.cursor()


        # creating self.frame and adding that to self
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()

        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=1, columnspan=4)
        self.logger.debug('Group logo has been created')

        self.label1 = Label(self.frame, font=(self.font1, self.size))
        self.label1.configure(text=" ", bg='#1D265E', fg='white', bd=6, width=80)
        self.label1.grid(row=2, columnspan=4)

        self.empty1 = Label(self.frame, font=(self.font1, self.size))
        self.empty1.configure(text=" ", bg='white')
        self.empty1.grid(row=3)
        self.logger.debug('Group logo has been created')

        # ask for name of experiment
        self.label2 = Label(self.frame, font=(self.font1, self.size))
        self.label2.configure(text="Name of experiment", bg='white', fg='#1D265E', bd=6)
        self.label2.grid(row=4, column=0, columnspan=2, sticky="W")

        self.inputW1 = IntVar()
        self.inputW1.set(self.par.name)
        self.widget1 = Entry(self.frame, textvariable=self.inputW1, width=25,
                             fg='#1D265E', font=(self.font1, self.size))
        self.widget1.grid(row=4, column=2, columnspan=1)
        self.logger.debug('Name experiment input is created')

        # ask for number of experiments and give a help button
        self.label3 = Label(self.frame, font=(self.font1, self.size))
        self.label3.configure(text="Number of experiments [1-48]", bg='white', fg='#1D265E', bd=6)
        self.label3.grid(row=6, column=0, columnspan=2, sticky="W")

        self.inputW2 = IntVar()
        self.inputW2.set(self.par.experimentNumber)
        self.widget2 = Entry(self.frame, textvariable=self.inputW2, width=25,
                             fg='#1D265E', font=(self.font1, self.size))
        self.widget2.grid(row=6, column=2, columnspan=1)

        self.button1 = Button(self.frame, font=(self.font1, self.size),
                              text="Help", width=15, command=self.HelpButton1,
                              bg='#1D265E', fg='white')
        self.button1.grid(row=6, column=3)
        self.logger.debug('Name experiment input and help button is created')

        # multiple entries to most data
        # name catalyst
        self.label4 = Label(self.frame, font=(self.font1, self.size))
        self.label4.configure(text="Catalyst used", bg='white', fg='#1D265E', bd=6)
        self.label4.grid(row=8, column=0, columnspan=2, sticky="W")

        self.varDropDown = StringVar()
        optionList = self.MakeDropdown()
        self.varDropDown.set(optionList[0])
        self.dropDown = OptionMenu(self.frame, self.varDropDown, *optionList)
        self.dropDown.config(bg='white',  bd=1, width=20, fg='#1D265E', font=(self.font1, self.size),
                             background='white', activebackground='white')
        self.dropDown['menu'].config(font=(self.font1, self.size), bg='white', fg='#1D265E')
        self.dropDown.grid(row=8, column=2, columnspan=1)
        self.logger.debug('Dropdown menu has been created')

        # email
        self.label8 = Label(self.frame, font=(self.font1, self.size))
        self.label8.configure(text="Email address", bg='white', fg='#1D265E', bd=6 )
        self.label8.grid(row=12, column=0, columnspan=2, sticky="W")

        self.inputW7 = IntVar()
        self.inputW7.set(self.par.email)
        self.widget7 = Entry(self.frame, textvariable=self.inputW7, width=25, fg='#1D265E', font=(self.font1, self.size))
        self.widget7.grid(row=12, column=2, columnspan=1)
        self.logger.debug('Name email input is created')

        self.empty6 = Label(self.frame, font=(self.font1, self.size))
        self.empty6.configure(text=" ", bg='white')
        self.empty6.grid(row=13)

        # create a button to start Avasoft and LED software
        self.label3 = Label(self.frame, font=(self.font1, self.size))
        self.label3.configure(text="Open required software", bg='white', fg='#1D265E', bd=6)
        self.label3.grid(row=14, column=0, columnspan=2, sticky="W")

        self.button2 = Button(self.frame, font=(self.font1, self.size),
                              text="Open Avasoft", width=15, command=self.OpenAvasoft,
                              bg='#1D265E', fg='white')
        self.button2.grid(row=14, column=2, columnspan=1)
        self.logger.debug('Avasoft button is created')

        self.button3 = Button(self.frame, font=(self.font1, self.size),
                              text="Open LED software", width=15, command=self.OpenLEDDriver,
                              bg='#1D265E', fg='white')
        self.button3.grid(row=14, column=3, columnspan=1)
        self.logger.debug('LED button is created')

        self.empty4 = Label(self.frame, font=(self.font1, self.size))
        self.empty4.configure(text=" ", bg='white')
        self.empty4.grid(row=15)

        # Next button
        self.button4 = Button(self.frame, font=(self.font1, self.size),
                              text="Next", width=15, command=self.NextButton,
                              bg='#1D265E', fg='white')
        self.button4.grid(row=16, column=2, columnspan=1)

        self.empty5 = Label(self.frame, font=(self.font1, self.size))
        self.empty5.configure(text=" ", bg='white')
        self.empty5.grid(row=17)
        self.logger.debug('Next button is created')

    # the second part of the GUI
    # this part destroys the first part of the GUI and recreates a frame with new buttons
    def RenewFrame(self):
        self.logger.info('Renewed the frame')

        # destroy olf frame and create a new
        self.frame.destroy()
        frame = Frame(self.root, bg='white')
        frame.grid()
        self.logger.debug('Old frame destroyed and new one created')

        # logo
        photo = PhotoImage(file="NRGLogo.ppm")
        imageLabel = Label(frame, image=self.photo, bg='white')
        imageLabel.grid(row=1, columnspan=4)

        label1 = Label(frame, font=(self.font1, self.size))
        label1.configure(text=" ", bg='#1D265E', fg='white', bd=6, width=80)
        label1.grid(row=2, columnspan=4)

        empty1 = Label(frame, font=(self.font1, self.size))
        empty1.configure(text=" ", bg='white')
        empty1.grid(row=3)
        self.logger.debug('Group logo has been created')

        # make line with the name for the Avasoft file
        label2 = Label(frame, font=(self.font1, self.size))
        label2.configure(text="Name Avasoft file", bg='white', fg='#1D265E', bd=6)
        label2.grid(row=4, column=0, columnspan=2, sticky="W")

        inputW1 = IntVar()
        inputW1.set(self.par.nameFileAvasoft)
        widget1 = Entry(frame, textvariable=inputW1, width=25, fg='#1D265E', font=(self.font1, self.size))
        widget1.grid(row=4, column=2, columnspan=1)

        empty2 = Label(frame, font=(self.font1, self.size))
        empty2.configure(text=" ", bg='white')
        empty2.grid(row=5)
        self.logger.debug('Show Avasoft file name created')

        # ask for to individually name quenchers
        label3 = Label(frame, font=(self.font1, self.size))
        label3.configure(text="Do you want to individually name the experiments?", bg='white', fg='#1D265E', bd=6)
        label3.grid(row=6, column=0, columnspan=2, sticky="W")

        self.inputW8 = BooleanVar()
        self.inputW8.set(self.par.setSelfNaming)
        self.widget8 = Checkbutton(frame, text="Yes", variable=self.inputW8,
                              width=25, bg='white', fg='#1D265E', onvalue=True, offvalue=False)
        self.widget8.grid(row=6, column=2, columnspan=1)

        button1 = Button(frame, font=(self.font1, self.size),
                              text="Help", width=15, command=self.HelpButton2,
                              bg='#1D265E', fg='white')
        button1.grid(row=6, column=3)
        self.logger.debug('Check button 1 and help button created')

        empty3 = Label(frame, font=(self.font1, self.size))
        empty3.configure(text=" ", bg='white')
        empty3.grid(row=7)

        label4 = Label(frame, font=(self.font1, self.size))
        label4.configure(text="Are you running the experiment overnight?", bg='white', fg='#1D265E', bd=6)
        label4.grid(row=8, column=0, columnspan=2, sticky="W")

        self.inputW9 = BooleanVar()
        self.inputW9.set(self.par.setOverNight)
        self.widget9 = Checkbutton(frame, text="Yes", variable=self.inputW9,
                                   width=25, bg='white', fg='#1D265E', onvalue=True, offvalue=False)
        self.widget9.grid(row=8, column=2, columnspan=1)

        button2 = Button(frame, font=(self.font1, self.size),
                         text="Help", width=15, command=self.HelpButton3,
                         bg='#1D265E', fg='white')
        button2.grid(row=8, column=3)

        empty3 = Label(frame, font=(self.font1, self.size))
        empty3.configure(text=" ", bg='white')
        empty3.grid(row=9)
        self.logger.debug('Check button 2 and help button created')

        label1 = Label(frame, font=(self.font1, self.size))
        label1.configure(text=" ", bg='#1D265E', fg='white', bd=6, width=80)
        label1.grid(row=10, columnspan=4)

        # present calculated values
        label5 = Label(frame, font=(self.font1, self.size))
        label5.configure(text="Amount of solution required [ml]", bg='white', fg='#1D265E', bd=6)
        label5.grid(row=11, column=0, columnspan=2, sticky="W")
        self.logger.debug('Present estimate amount of solution required for experiment')

        labelout1 = Label(frame, font=(self.font1, self.size))
        labelout1.configure(text=str(round(self.requiredSolvent, 2)), bg='white', fg='#1D265E', bd=6)
        labelout1.grid(row=11, column=2, columnspan=1)

        # estimate amount of catalyst solution
        label6 = Label(frame, font=(self.font1, self.size))
        label6.configure(text="Amount of catalyst required [ml]", bg='white', fg='#1D265E', bd=6)
        label6.grid(row=12, column=0, columnspan=2, sticky="W")
        self.logger.debug('Present estimate amount of cat required for experiment')

        labelout2 = Label(frame, font=(self.font1, self.size))
        labelout2.configure(text=str(round(self.requiredCat,2)), bg='white', fg='#1D265E', bd=6)
        labelout2.grid(row=12, column=2, columnspan=1)

        # estimate waiting time
        label7 = Label(frame, font=(self.font1, self.size))
        label7.configure(text="Estimated time when experiments are finished", bg='white', fg='#1D265E', bd=6)
        label7.grid(row=13, column=0, columnspan=2, sticky="W")
        self.logger.debug('Present estimate when experiment is finished')

        labelout3 = Label(frame, font=(self.font1, self.size))
        labelout3.configure(text=str(self.estimatedTime.strftime('%H:%M:%S')), bg='white', fg='#1D265E', bd=6)
        labelout3.grid(row=13, column=2, columnspan=1)

        # end
        empty4 = Label(frame, font=(self.font1, self.size))
        empty4.configure(text=" ", bg='white')
        empty4.grid(row=14)

        button2 = Button(frame, font=("Roboto Condensed", 11),
                         text="Start Experiment", width=15, command=self.EndGui,
                         bg='#1D265E', fg='white')
        button2.grid(row=15, column=2)
        self.logger.debug('Next button is created')

    # draw input from fields of first GUI
    # check if input is correct
    # initiates second part of GUI
    def NextButton(self):
        self.logger.info('Next button pressed. Start checking input values')
        # check if the number of experiments has a correct input
        try:
            pullexp = int(self.widget2.get())
            if (pullexp >= 1) & (pullexp <= 48):
                self.par.experimentNumber = pullexp
                self.logger.debug('Number of experiments is {}'.format(self.par.experimentNumber))
            else:
                raise ValueError
        except:
            messagebox.showerror('Wrong input', 'The number of experiments has a wrong input.\n'
                                                'Please make sure that this value is an integer between the 1 and 48.')
            self.logger.error('Number of experiments input crashed (widget2):', exc_info=True)
            return False
        # file name
        try:
            pullName = str(self.widget1.get())
            self.par.name = pullName
            self.par.nameFileAvasoft = '{0}{1}'.format(pullName, '.txt')
            self.par.nameFileExcel = '{0}{1}'.format(pullName, '.xlsx')
            self.logger.debug('Name of Avasoft file is {}'.format(self.par.nameFileAvasoft))
            self.logger.debug('Name of excel file is {}'.format(self.par.nameFileExcel))
        except:
            messagebox.showerror('Wrong input', 'The name of the file could not be converted to a string.\n'
                                                'Please insert a valid name.')
            self.logger.error('Name Avasoft/excel file input crashed(widget1): ', exc_info=True)
            return False

        try:
            self.par.catalystName = self.varDropDown.get()
            self.logger.debug('Cat name is {}'.format(self.par.catalystName))
        except:
            messagebox.showerror('Wrong input', 'The catalyst name setting went wrong.')
            self.logger.error('Could not properly read the cat name  from widget6: ', exc_info=True)
            return False

        # email address
        try:
            self.par.email = str(self.widget7.get())
            self.logger.debug('Email name is {}'.format(self.par.email))
        except:
            messagebox.showerror('Wrong input', 'The email setting went wrong.')
            self.logger.error('Could not properly read the email adress from widget7: ', exc_info=True)
            return False

        self.CalculateRequiredVolumes()
        self.RenewFrame()

    # calculates the estimated volume of solvent required for the experiment
    def CalculateRequiredVolumes(self):
        self.logger.info('Volume and residence time calculations have started.')
        # calculate residence times
        pi = 3.14159265359
        # calculate required solvent
        self.requiredSolvent = (self.par.experimentNumber * self.par.timeAnalysis) / 60.0 * (self.par.flowRateSolvent / 1000.0) + 25
        self.requiredCat = ((self.par.experimentNumber * self.par.timeAnalysis) / 60.0) * (self.par.flowRateCat / 1000.0) + 10
        self.logger.debug('The required amount of solvent is is {}'.format(self.requiredSolvent))
        self.logger.debug('The required amount of cat is is is {}'.format(self.requiredCat))

        curTime = datetime.datetime.now()
        addTime = datetime.timedelta(seconds=((self.par.experimentNumber - 1) * (self.par.timeAnalysis - 90)
                                              + 420 + 420))
        self.par.date = curTime.strftime('%Y/%m/%d')
        self.estimatedTime = curTime + addTime
        self.logger.debug('The estimated time that the experiment is finished is {}'.format(self.estimatedTime))

    # check value in checkbox
    # if checkbox is checked than open a other GUI that allows input
    # otherwise create the names according to input
    def EndGui(self):
        self.logger.info('Function EndGUI in GUI1')
        self.par.namesExperiments = [None] * self.par.experimentNumber
        self.par.namesPositions = [None] * self.par.experimentNumber
        self.par.colorCodes = [None] * self.par.experimentNumber
        self.par.legend = [None] * self.par.experimentNumber

        try:
            self.par.selfNaming = bool(self.inputW8.get())
            self.logger.debug('The self-naming check button is set to {}'.format(self.par.selfNaming))
        except:
            messagebox.showerror('Wrong input', 'The program could not properly read the checkbox value for Naming')
            self.logger.error('The self naming checkbox did not return a value (widget8):', exc_info=True)
            return False

        try:
            self.par.overNight = bool(self.inputW9.get())
            self.logger.debug('The overnight check button is set to {}'.format(self.par.selfNaming))
        except:
            messagebox.showerror('Wrong input', 'The program could not properly read the checkbox value for Overnight')
            self.logger.error('The overnight checkbox did not return a value (widget9):', exc_info=True)
            return False

        self.AutoNaming()
        self.root.quit()
        self.root.destroy()

    # gives all the experiments a standard name (A1, A2, etc.)
    def AutoNaming(self):
        self.logger.info('Started to automatically name the quencher to their position.')
        for i in range(len(self.par.namesExperiments)):
            letter = int(i/8) + 65
            position = (i % 8) + 1
            self.par.namesExperiments[i] = '{}{}'.format(chr(letter), str(position))
            self.par.namesPositions[i] = '{}{}'.format(chr(letter), str(position))
            self.par.legend[i] = '{} = {}'.format(self.par.namesPositions[i], self.par.namesExperiments[i])
            self.logger.debug('In GUI1, in function AutoNaming fame {0} is {1}'.format(i, self.par.namesExperiments[i]))

    # displays a picture of how the rows and columns of the tray are defined
    def HelpButton1(self):
        self.logger.info('The help button that tells how to fill the sample tray was called.')
        help1 = ShowSample()
        help1.root2.mainloop()

    # gives a pop-up explaineng the checkbox for the NamingGUI, and its consequences
    def HelpButton2(self):
        self.logger.info('The help button for the Self naming GUI was called.')

        messagebox.showinfo('Explanation checkbox', 'By checking this checkbox you confirm that you want to manually '
                                                    'name all the quenchers you are going to use in your experiment.\n\n'
                                                    'If the checkbox is checked, after pressing the "Next" button '
                                                    'an GUI will appear that allows you to '
                                                    'individually name the quenchers. \n\n'
                                                    'If not selected. The program will automatically generate names '
                                                    'according to the position of the vial\'s. (A1, A2, ... etc.)\n\n'
                                                    'All samples that are not named, or have a name shorter than 3 characters, '
                                                    'will have the standard names according to their position.')

    # gives a pop-up explaining the checkbox for the "overnight" option, and its consequences
    def HelpButton3(self):
        self.logger.info('The help button for the overnight experiment is called.')
        messagebox.showinfo('Explanation checkbox', 'By checking this checkbox you confirm that you are running'
                                                    'the experiment over night. \n\n'
                                                    'This means that the program finishes it will automatically shut down; the pumps, '
                                                    'Avasoft and the PC this program is running on.\n\n'
                                                    'In order to keep the data of the Avasoft run, a screen shot will be taken. \n'
                                                    'Please make sure the Avasoft plot is fully visible when you leave this system. \n\n'
                                                    'If this setting is on the system will not be cleaned, Please clean the system in the morning.')

    # opens Avasoft
    def OpenAvasoft(self):
        self.logger.info('Avasoft is launched with help of a button.')
        subprocess.Popen(r"C:\Program Files (x86)\Avasoft8\Avasoft8.exe")

    # opens the software of the LED
    def OpenLEDDriver(self):
        self.logger.info('LED software is launched with help of a button.')
        subprocess.Popen(r"C:\Program Files (x86)\Mightex LEDDriver\LEDDriver.exe")

    def MakeDropdown(self):
        listOfNames = []
        self.cursor.execute("SELECT Catalysts.catalyst FROM Catalysts")
        rows = self.cursor.fetchall()

        for i in range(len(rows)):
            listOfNames.append(rows[i][0])

        return listOfNames


if __name__ == '__main__':
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparAuto()
    gui1 = AutomationInterface1(par)
    gui1.root.mainloop()