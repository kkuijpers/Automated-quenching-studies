from tkinter import *
from DatabaseCommander import DatabaseHandler
import logging

class InsertDataGUI:
    def __init__(self):
        # create logger
        self.logger = logging.getLogger('InserLog')
        logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger.info('Insert GUI has been created')

        # make root
        self.root = Tk()
        self.root.title('Insert into Database')
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'
        self.colorGreen = '#00f392'

        # database
        self.databaseCommander = DatabaseHandler('Database_Automation.db')
        self.basicCatName = 'New_Catalyst'
        self.basicSolName = 'New_Solvent'

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

        # insert solvent
        self.labels1 = Label(self.frame, font=(self.font1, self.size))
        self.labels1.configure(text="Insert solvent into database ", bg='#1D265E', fg='white', bd=6, width=80)
        self.labels1.grid(row=line, columnspan=4)
        line += 1

        self.labels2 = Label(self.frame, font=(self.font1, self.size))
        self.labels2.configure(text=" ", bg='white')
        self.labels2.grid(row=line)
        line += 1

        self.labels3 = Label(self.frame, font=(self.font1, self.size))
        self.labels3.configure(text="New solvent name:", bg='white')
        self.labels3.grid(row=line, column=0, columnspan=2, sticky='W')

        # text box
        self.ins3 = IntVar()
        self.ins3.set(self.basicSolName)
        self.entrys3 = Entry(self.frame, textvariable=self.ins3, width=25)
        self.entrys3.grid(row=line, column=2)

        # button
        self.buttons3 = Button(self.frame, font=(self.font1, self.size))
        self.buttons3.configure(text='Insert', width=15, command=self.InsertSolvent, bg='#1D265E', fg='white')
        self.buttons3.grid(row=line, column=3)
        line += 1

        self.labels4 = Label(self.frame, font=(self.font1, self.size))
        self.labels4.configure(text=" ", bg='white')
        self.labels4.grid(row=line, columnspan=4, sticky='WE')
        line += 1

        # insert catalyst
        self.labelc1 = Label(self.frame, font=(self.font1, self.size))
        self.labelc1.configure(text="Insert catalyst into database ", bg='#1D265E', fg='white', bd=6, width=80)
        self.labelc1.grid(row=line, columnspan=4)
        line += 1

        self.labelc2 = Label(self.frame, font=(self.font1, self.size))
        self.labelc2.configure(text=" ", bg='white')
        self.labelc2.grid(row=line)
        line += 1

        self.labelc3 = Label(self.frame, font=(self.font1, self.size))
        self.labelc3.configure(text="New catalyst name:", bg='white')
        self.labelc3.grid(row=line, column=0, columnspan=2, sticky='W')

        # text box
        self.inc3 = IntVar()
        self.inc3.set(self.basicCatName)
        self.entryc3 = Entry(self.frame, textvariable=self.inc3, width=25)
        self.entryc3.grid(row=line, column=2)

        # button
        self.buttonc3 = Button(self.frame, font=(self.font1, self.size))
        self.buttonc3.configure(text='Insert', width=15, command=self.InsertCatalyst, bg='#1D265E', fg='white')
        self.buttonc3.grid(row=line, column=3)
        line += 1

        self.labelc4 = Label(self.frame, font=(self.font1, self.size))
        self.labelc4.configure(text=" ", bg='white')
        self.labelc4.grid(row=line, columnspan=4, sticky='WE')
        line += 1

        # insert lifetime
        # lifetime bar
        self.labell1 = Label(self.frame, font=(self.font1, self.size))
        self.labell1.configure(text="Insert lifetime into database ", bg='#1D265E', fg='white', bd=6, width=80)
        self.labell1.grid(row=line, columnspan=4, sticky="W")
        line += 1

        self.labell2 = Label(self.frame, font=(self.font1, self.size))
        self.labell2.configure(text=" ", bg='white')
        self.labell2.grid(row=line)
        line += 1

        # bar with buttons
        self.labell3 = Label(self.frame, font=(self.font1, self.size))
        self.labell3.configure(text="New life time: (ns)", bg='white')
        self.labell3.grid(row=line, columnspan=2, sticky='W')

        # catalyst dropdown
        self.varDropDownCat = StringVar(self.root)
        self.optionListCat = [' ']
        self.varDropDownCat.set(self.optionListCat[0])
        self.dropDownCat = OptionMenu(self.frame, self.varDropDownCat, *self.optionListCat)
        self.dropDownCat.config(bg='white', bd=1, width=20, fg='#1D265E', font=(self.font1, self.size),
                             background='white', activebackground='white')
        self.dropDownCat['menu'].config(font=(self.font1, self.size), bg='white', fg='#1D265E')
        self.dropDownCat.grid(row=line, column=2, columnspan=1)

        # lifetime bar
        self.inl3 = IntVar()
        self.inl3.set("New_Lifetime")
        self.entryl3 = Entry(self.frame, textvariable=self.inl3, width=25)
        self.entryl3.grid(row=line, column=3)
        line += 1

        self.labell4 = Label(self.frame, font=(self.font1, self.size))
        self.labell4.configure(text=" ", bg='white')
        self.labell4.grid(row=line, columnspan=4, sticky='WE')
        line += 1

        # solvent dropdownbar
        self.varDropDownSol = StringVar(self.root)
        self.optionListSol = [' ']
        self.varDropDownSol.set(self.optionListSol[0])
        self.dropDownSol = OptionMenu(self.frame, self.varDropDownSol, *self.optionListSol)
        self.dropDownSol.config(bg='white', bd=1, width=20, fg='#1D265E', font=(self.font1, self.size),
                                background='white', activebackground='white')
        self.dropDownSol['menu'].config(font=(self.font1, self.size), bg='white', fg='#1D265E')
        self.dropDownSol.grid(row=line, column=2, columnspan=1)

        # insert button
        self.buttonl5 = Button(self.frame, font=(self.font1, self.size))
        self.buttonl5.configure(text='Insert', width=15, command=self.InsertLifetime, bg='#1D265E', fg='white')
        self.buttonl5.grid(row=line, column=3)
        line += 1

        self.labell6 = Label(self.frame, font=(self.font1, self.size))
        self.labell6.configure(text=" ", bg='white')
        self.labell6.grid(row=line, columnspan=4, sticky='WE')
        line += 1

        # quit button
        self.quitButton = Button(self.frame, font=(self.font1, self.size),
                                text="Quit", command=self.Quit,
                                width=15, bg='#1D265E', fg='white')
        self.quitButton.grid(row=line, column=2)

        # create and fill dropdown menus
        self.CreateDropDowns()

    def InsertSolvent(self):
        # pull solvent name
        newSol = self.entrys3.get()

        # check if name is changed
        if newSol == self.basicSolName or newSol == '' or newSol == ' ' or newSol == '  ':
            self.labels4.configure(text="Please enter a new Solvent",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False

        # check if solvent is already in database
        for sol in self.optionListSol:
            if newSol == sol[0]:
                self.labels4.configure(text="Solvent is already in database",
                                       fg=self.colorBlue, bg=self.colorOrange,
                                       font=(self.font1, self.size),
                                       bd=6)
                return False
        # add to database
        try:
            self.databaseCommander.CreateSolvent((newSol, ))
        except Exception as e:
            self.labels4.configure(text="Solvent could not be inserted into the database",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False

        # confirm that solvent has been added to the database
        self.labels4.configure(text="Solvent with name: {} has successfully been added to the database".format(newSol),
                               fg=self.colorBlue, bg=self.colorGreen,
                               font=(self.font1, self.size),
                               bd=6)
        self.CreateDropDowns()
        pass

    def InsertCatalyst(self):
        # pull catalyst name
        newCat = self.entryc3.get()

        # check if name is changed
        if newCat == self.basicCatName or newCat == '' or newCat == ' ' or newCat == '  ':
            self.labelc4.configure(text="Please enter a new Catalyst",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False

        # check if catalyst is already in database
        for cat in self.optionListCat:
            if newCat == cat[0]:
                self.labelc4.configure(text="Catalyst is already in database",
                                       fg=self.colorBlue, bg=self.colorOrange,
                                       font=(self.font1, self.size),
                                       bd=6)
                return False
        # add to database
        try:
            self.databaseCommander.CreateCatalyst((newCat, ))
        except Exception as e:
            self.labelc4.configure(text="Catalyst could not be inserted into the database",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False

        # if all is good, then confirm that the catalyst has been inserted into the database
        self.labelc4.configure(text="Catalyst with name: {} has successfully been added to the database".format(newCat),
                               fg=self.colorBlue, bg=self.colorGreen,
                               font=(self.font1, self.size),
                               bd=6)
        self.CreateDropDowns()
        pass

    def InsertLifetime(self):
        # pull life time from entry box
        lifetime = self.entryl3.get()

        # check if lifetime is a number else give warning
        try:
            lifetime = float(lifetime)
        except Exception as e:
            self.labell6.configure(text="Life time is not a number",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False
        # overwrite / input lifetime into database
        try:
            self.databaseCommander.InsertLifetime((lifetime, self.varDropDownCat.get(), self.varDropDownSol.get()))
        except Exception as e:
            self.labell6.configure(text="life time could not be added to the data base",
                                   fg=self.colorBlue, bg=self.colorOrange,
                                   font=(self.font1, self.size),
                                   bd=6)
            return False
        # confirm that data has been added to database
        self.labell6.configure(text="Life time has successfully been updated to {}".format(lifetime),
                               fg=self.colorBlue, bg=self.colorGreen,
                               font=(self.font1, self.size),
                               bd=6)

        pass

    def CreateDropDowns(self):
        # create vectors for names of both cat and solvent
        # create and fill catalyst dropdown menu
        # retrieve all catalysts in a list
        self.optionListCat = self.databaseCommander.GetAllCatalysts()

        # set the new list to the dropdown menues
        self.varDropDownCat.set(self.optionListCat[0])
        menuCat = self.dropDownCat['menu']
        menuCat.delete(0, 'end')
        for line in self.optionListCat:
            menuCat.add_command(label=line, command=lambda value=line: self.varDropDownCat.set(value))

        # create and fill solvent dropdown menu
        # retrieve all solvents from list
        self.optionListSol = self.databaseCommander.GetAllSolvents()

        # set new list to the dropdown menues
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
    gui = InsertDataGUI()
    gui.root.mainloop()
    pass