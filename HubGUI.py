from tkinter import *
from MainRunAuto import MainRunAutosampler
from MainRunSV import MainRunSternVolmer
from InsertIntoDatabaseGUI import InsertDataGUI
import time
# http://www.sciosoft.com/blogs/post/2011/10/04/Launch-PowerShell-Script-from-Shortcut.aspx

class MainHubGUI:
    def __init__(self):
        # make root
        self.root2 = Tk()
        self.root2.title('Insert into Database')
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.colorBlue = '#1D265E'
        self.colorOrange = '#f39200'
        self.colorGreen = '#00f392'

        # create frame on root
        self.frame = Frame(self.root2, bg='white')
        self.frame.grid()
        line = 1

        # group logo
        self.photo = PhotoImage(file="NRGLogo.ppm")
        self.imageLabel = Label(self.frame, image=self.photo, bg='white')
        self.imageLabel.grid(row=line, columnspan=4)
        line += 1

        # upper blue bar
        self.labels1 = Label(self.frame, font=(self.font1, self.size))
        self.labels1.configure(text="", bg='#1D265E', fg='white', bd=6, width=80)
        self.labels1.grid(row=line, columnspan=4)
        line += 1

        self.labels2 = Label(self.frame, font=(self.font1, self.size))
        self.labels2.configure(text=" ", bg='white')
        self.labels2.grid(row=line, columnspan=4, rowspan=2)
        line += 2

        # title bar for Automation (screening) and Stern-Volmer
        self.labels3 = Label(self.frame, font=(self.font1, self.size))
        self.labels3.configure(text="Automation", bg='white')
        self.labels3.grid(row=line, column=1, sticky='W')

        self.labels4 = Label(self.frame, font=(self.font1, self.size))
        self.labels4.configure(text="Stern Volmer", bg='white')
        self.labels4.grid(row=line, column=3, sticky='W')
        line += 1

        # button bar Automation and SV
        self.buttons5 = Button(self.frame, font=(self.font1, self.size))
        self.buttons5.configure(text='Automation', width=15, height=2, command=self.StartAutomation, bg='#1D265E', fg='white')
        self.buttons5.grid(row=line, column=1, sticky='W')

        self.buttons6 = Button(self.frame, font=(self.font1, self.size))
        self.buttons6.configure(text='Stern Volmer', width=15, height=2, command=self.StartSternVolmer, bg='#1D265E', fg='white')
        self.buttons6.grid(row=line, column=3, sticky='W')
        line += 1

        #whitespace
        self.labelm1 = Label(self.frame, font=(self.font1, self.size))
        self.labelm1.configure(text=" ", bg='white')
        self.labelm1.grid(row=line, columnspan=4, rowspan=1)
        line += 1

        # announcement bar
        self.announce = Label(self.frame, font=(self.font1, self.size))
        self.announce.configure(text=" ", bg='white')
        self.announce.grid(row=line, columnspan=4, rowspan=2, sticky='WE')
        line += 2

        # whitespace
        self.labelm3 = Label(self.frame, font=(self.font1, self.size))
        self.labelm3.configure(text=" ", bg='white')
        self.labelm3.grid(row=line, columnspan=4, rowspan=1)
        line += 1

        # title bar input output
        self.labeli1 = Label(self.frame, font=(self.font1, self.size))
        self.labeli1.configure(text="Input Database", bg='white')
        self.labeli1.grid(row=line, column=1, sticky='W')

        self.labeli2 = Label(self.frame, font=(self.font1, self.size))
        self.labeli2.configure(text="Output Database", bg='white')
        self.labeli2.grid(row=line, column=3, sticky='W')
        line += 1

        # button bar for input and output
        self.buttoni3 = Button(self.frame, font=(self.font1, self.size))
        self.buttoni3.configure(text='Input', width=15, height=2, command=self.InputDB, bg='#1D265E', fg='white')
        self.buttoni3.grid(row=line, column=1, sticky='W')

        self.buttoni4 = Button(self.frame, font=(self.font1, self.size))
        self.buttoni4.configure(text='Output', width=15, height=2, command=self.OutputDB, bg='#1D265E', fg='white')
        self.buttoni4.grid(row=line, column=3, sticky='W')
        line += 2

        #empty line
        self.labele1 = Label(self.frame, font=(self.font1, self.size))
        self.labele1.configure(text=" \n ", bg='white')
        self.labele1.grid(row=line, columnspan=4, rowspan=2)
        line += 2

        self.buttone2 = Button(self.frame, font=(self.font1, self.size))
        self.buttone2.configure(text='Quit', width=15, command=self.root2.destroy, bg='#1D265E', fg='white')
        self.buttone2.grid(row=line, column=2, sticky='W')
        line += 1

    def StartAutomation(self):
        '''
        Deactivates all buttons and tels which program has launched
        returns everything to normal when GUI is finished
        :return:
        '''

        #Deactivate all buttons
        self.ActivateButtons(False)

        # make an announcement on the announcement bar
        self.announce.configure(text="Automation Program is now running. Please wait a while until it has finished ...",
                                bg=self.colorOrange, fg=self.colorBlue,
                                font=(self.font1, self.size + 2))

        # launch the automation Gui
        MainRunAutosampler()

        # Return the announcementbar to blank
        self.announce.configure(text=" ", bg='white', font=(self.font1, self.size))

        # activate all the buttons
        self.ActivateButtons(True)

        pass

    def StartSternVolmer(self):
        '''
                Deactivates all buttons and tels which program has launched
                returns everything to normal when GUI is finished
                :return:
                '''

        # deactivate all buttons
        self.ActivateButtons(False)

        # make an announcement on the announcement bar
        self.announce.configure(text="Stern-Volmer Program is now running. Please wait a while until it starts ...",
                                bg=self.colorOrange, fg=self.colorBlue,
                                font=(self.font1, self.size + 2))

        # launch the Stern Volmer Gui
        MainRunSternVolmer()

        # Return the announcementbar to blank
        self.announce.configure(text=" ", bg='white', font=(self.font1, self.size))

        # activate all the buttons
        self.ActivateButtons(True)

        pass

    def InputDB(self):
        '''
                Deactivates all buttons and tels which program has launched
                returns everything to normal when GUI is finished
                :return:
                '''

        # deactivate all buttons
        self.ActivateButtons(False)

        # make an announcement on the announcement bar
        self.announce.configure(text="Waiting until you have finished working with the database",
                                bg=self.colorGreen, fg=self.colorBlue,
                                font=(self.font1, self.size + 2))

        # launch the input db Gui
        try:
            gui = InsertDataGUI()
            gui.root.mainloop()
            print('hi')
        except Exception as e:
            print(e)

        # Return the announcementbar to blank
        self.announce.configure(text=" ", bg='white', font=(self.font1, self.size))

        # activate all the buttons
        self.ActivateButtons(True)

        pass

    def OutputDB(self):
        '''
                Deactivates all buttons and tels which program has launched
                returns everything to normal when GUI is finished
                :return:
                '''

        # deactivate all buttons
        self.ActivateButtons(False)

        # make an announcement on the announcement bar
        self.announce.configure(text="Waiting until you have finished working with the database",
                                bg=self.colorGreen, fg=self.colorBlue,
                                font=(self.font1, self.size + 2))
        self.root2.update()

        # return the announcementbar to blank
        self.announce.configure(text=" ", bg='white', font=(self.font1, self.size))
        self.root2.update()
        # activate all the buttons
        self.ActivateButtons(True)

        pass

    def ActivateButtons(self, onSwitch=True):
        # swiches all buttons on or off

        if onSwitch:
            self.buttons5.configure(state=NORMAL)
            self.buttons6.configure(state=NORMAL)
            self.buttoni3.configure(state=NORMAL)
            self.buttoni4.configure(state=NORMAL)

        else:
            self.buttons5.configure(state=DISABLED)
            self.buttons6.configure(state=DISABLED)
            self.buttoni3.configure(state=DISABLED)
            self.buttoni4.configure(state=DISABLED)

        pass

    def Stuff(self):
        print('hi')
        time.sleep(2)
        print('this is a test')
        pass

if __name__ == '__main__':
    gui = MainHubGUI()
    gui.root2.mainloop()
    pass