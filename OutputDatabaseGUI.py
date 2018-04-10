from tkinter import *
from DatabaseCommander import DatabaseHandler
import os
import logging

class OutputDataGUI:

    def __init__(self):
        # create logger
        self.logger = logging.getLogger('InserLog')
        logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger.info('Insert GUI has been created')

        # make root
        self.root = Tk()
        self.root.title('Output data from Database')
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'
        self.colorGreen = '#00f392'

        # database
        self.databaseCommander = DatabaseHandler('Database_Automation.db')
        self.possibleQuencher = 'TMEDA'

        # create frame on root
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()
        line = 1

        # group logo
        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=line, columnspan=4)
        self.logger.debug('Group logo created')
        line += 1

        self.label01 = Label(self.frame, font=(self.font1, self.size))
        self.label01.configure(text="Pull data from the database ", bg='#1D265E', fg='white', bd=6, width=80)
        self.label01.grid(row=line, columnspan=4, sticky="WE")
        line += 1

        self.label02 = Label(self.frame, font=(self.font1, self.size))
        self.label02.configure(text="  ", bg='white')
        self.label02.grid(row=line, columnspan=4)
        line += 1

        # select catalyst and solvent bar
        self.label11 = Label(self.frame, font=(self.font1, self.size))
        self.label11.configure(text="Catalyst:",
                               bg='white', fg=self.colorBlue)
        self.label11.grid(row=line, column=0, columnspan=1, sticky='W')

        # catalyst dropdown
        self.varDropDownCat = StringVar(self.root)
        self.optionListCat = [' ']
        self.varDropDownCat.set(self.optionListCat[0])
        self.dropDownCat = OptionMenu(self.frame, self.varDropDownCat, *self.optionListCat)
        self.dropDownCat.config(bg='white', bd=1, width=20, fg='#1D265E', font=(self.font1, self.size),
                                background='white', activebackground='white')
        self.dropDownCat['menu'].config(font=(self.font1, self.size), bg='white', fg='#1D265E')
        self.dropDownCat.grid(row=line, column=1, columnspan=1, sticky="W")

        # solvent
        self.label12 = Label(self.frame, font=(self.font1, self.size))
        self.label12.configure(text="Solvent:",
                               bg='white', fg=self.colorBlue)
        self.label12.grid(row=line, column=2, columnspan=1)

        # solvent dropdownbar
        self.varDropDownSol = StringVar(self.root)
        self.optionListSol = [' ']
        self.varDropDownSol.set(self.optionListSol[0])
        self.dropDownSol = OptionMenu(self.frame, self.varDropDownSol, *self.optionListSol)
        self.dropDownSol.config(bg='white', bd=1, width=20, fg='#1D265E', font=(self.font1, self.size),
                                background='white', activebackground='white')
        self.dropDownSol['menu'].config(font=(self.font1, self.size), bg='white', fg='#1D265E')
        self.dropDownSol.grid(row=line, column=3, columnspan=1)
        line += 1

        # part automation data
        # empty line
        self.label13 = Label(self.frame, font=(self.font1, self.size))
        self.label13.configure(text="  ", bg='white')
        self.label13.grid(row=line, columnspan=4)
        line += 1

        # ask automation
        self.label14 = Label(self.frame, font=(self.font1, self.size))
        self.label14.configure(text="Display the quenchers that with the selected catalyst",
                               bg='white', fg=self.colorBlue)
        self.label14.grid(row=line, column=0, columnspan=2, sticky='W')
        # button
        self.button1 = Button(self.frame, font=(self.font1, self.size))
        self.button1.configure(text='Pull', width=15, command=self.OutputAutomation, bg='#1D265E', fg='white')
        self.button1.grid(row=line, column=3, columnspan=1)
        line += 1

        # part simple sv data
        # empty line
        self.label21 = Label(self.frame, font=(self.font1, self.size))
        self.label21.configure(text="  ", bg='white')
        self.label21.grid(row=line, columnspan=4)
        line += 1

        # ask simple sv data
        self.label22 = Label(self.frame, font=(self.font1, self.size))
        self.label22.configure(text="Display the quenchers for the "
                                    "chosen catalyst and solvent where R\u00B2 > 0.9",
                               bg='white', fg=self.colorBlue)
        self.label22.grid(row=line, column=0, columnspan=2, sticky='W')
        # button
        self.button2 = Button(self.frame, font=(self.font1, self.size))
        self.button2.configure(text='Pull', width=15, command=self.OutputSimpleSV, bg='#1D265E', fg='white')
        self.button2.grid(row=line, column=3, columnspan=1)
        line += 1

        # part detailed sv data
        # empty line
        self.label31 = Label(self.frame, font=(self.font1, self.size))
        self.label31.configure(text="  ", bg='white')
        self.label31.grid(row=line, columnspan=4)
        line += 1

        # ask complicated sv data
        self.label32 = Label(self.frame, font=(self.font1, self.size))
        self.label32.configure(text="Display detailed information for the "
                                    "chosen catalyst and solvent where R\u00B2 > 0.97",
                               bg='white', fg=self.colorBlue)
        self.label32.grid(row=line, column=0, columnspan=2, sticky='W')
        # button
        self.button3 = Button(self.frame, font=(self.font1, self.size))
        self.button3.configure(text='Pull', width=15, command=self.OutputHighSV, bg='#1D265E', fg='white')
        self.button3.grid(row=line, column=3, columnspan=1)
        line += 1

        # empty line
        self.label41 = Label(self.frame, font=(self.font1, self.size))
        self.label41.configure(text="  ", bg='white')
        self.label41.grid(row=line, columnspan=4)
        line += 1

        # quit button
        self.button4 = Button(self.frame, font=(self.font1, self.size))
        self.button4.configure(text='Quit', width=15, command=self.Quit, bg='#1D265E', fg='white')
        self.button4.grid(row=line, column=0, columnspan=4)
        line += 1

        self.CreateDropDowns()

    def OutputAutomation(self):
        # pull selected catalyst from dropdown menu
        catalyst = self.varDropDownCat.get()[2:-3]
        # execute the database request
        answer = self.databaseCommander.PullAutomationData((catalyst,))

        # clear the commandline
        os.system('cls')
        i = 1

        # check if answer is empty, and tell that to the user if necessary
        if answer == []:
            print('No screening experiments are done yet '
                  'with the currently selected catalyst\n')

        # print answers to the screen for the user
        for data in answer:
            print("{}.    In experiment {}, quencher/position {} had a working\n"
                  "quencher with color code {} for catalyst {}\n".format(i,
                                                                         data[0],
                                                                         data[1],
                                                                         data[2],
                                                                         catalyst))
            i += 1

        pass

    def OutputSimpleSV(self):
        # pull catalyst and solvent from the dropdown menu's
        catalyst = self.varDropDownCat.get()[2:-3]
        solvent = self.varDropDownSol.get()[2:-3]

        # execute the data pull request
        answer = self.databaseCommander.PullSVlight((catalyst, solvent))

        # clear the commandline
        os.system('cls')
        i = 1

        # check if answer is empty, and tell that to the user if necessary
        if answer == []:
            print('No Stern-Volmer data present for currently selected catalyst/'
                  'Solvent combination\n')

        # print answers to the screen for the user
        for data in answer:
            print("{}.    Using {} to quench {}\ndesolved in {}, "
                  "giving a relative good fit\n".format(i,
                                                    data[2],
                                                    data[1],
                                                    data[0]))
            i += 1

        pass

    def OutputHighSV(self):
        # pull catalyst and solvent from the dropdown menu's
        catalyst = self.varDropDownCat.get()[2:-3]
        solvent = self.varDropDownSol.get()[2:-3]

        # execute the data pull request
        answer = self.databaseCommander.PullSVHard((catalyst, solvent))

        # clear the command line
        os.system('cls')
        i = 1

        # check if answer is empty, and tell that to the user if necessary
        if answer == []:
            print('No accurate Stern-Volmer data present for currently selected catalyst/'
                  'Solvent combination\n')

        # print answers to the screen for the user
        for data in answer:
            print("{}.    In experiment {}, {} was used to quench {}\n"
                  "desolved in {}. Giving a excellent fit with a R\u00B2 of {},\n"
                  "a slope of {} and a Kq of {}\n".format(i,
                                          data[0],
                                          data[3],
                                          data[1],
                                          data[2],
                                          data[6],
                                          data[4],
                                          data[5]))
            i += 1
        pass

    def CreateDropDowns(self):
        # create vectors for names of both cat and solvent

        # create and fill catalyst dropdown menu
        # retrieve all catalysts in a list
        self.optionListCat = self.databaseCommander.GetAllCatalysts()

        # set the new list to the dropdown menus
        self.varDropDownCat.set(self.optionListCat[0])
        menuCat = self.dropDownCat['menu']
        menuCat.delete(0, 'end')
        for line in self.optionListCat:
            menuCat.add_command(label=line, command=lambda value=line: self.varDropDownCat.set(value))

        # create and fill solvent dropdown menu
        # retrieve all solvents from list
        self.optionListSol = self.databaseCommander.GetAllSolvents()

        # set new list to the dropdown menus
        self.varDropDownSol.set(self.optionListSol[0])
        menuSol = self.dropDownSol['menu']
        menuSol.delete(0, 'end')
        for line in self.optionListSol:
            menuSol.add_command(label=line, command=lambda value=line: self.varDropDownSol.set(value))
        pass

    def Quit(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    gui = OutputDataGUI()
    gui.root.mainloop()
    pass