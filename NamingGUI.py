from tkinter import *
from tkinter import messagebox
from Parameters_Auto import ImportparAuto
import logging

class NamingGUI:
    def __init__(self, par):
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('NamingGUI, has started')
        self.root = Tk()
        self.root.title('Name quenchers individually')
        self.root.configure(bg='white')

        self.par = par
        self.font1 = "Roboto Condensed"
        self.size = 11

        # create naming vectors
        self.CreateNames()

        # creating self.canvas with scrollbar and adding that to self
        self.canvas = Canvas(self.root, bg='white')
        self.canvas.grid(row=0, column=0, rowspan=10, columnspan=5, sticky=E)
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=5, rowspan=10, sticky=N+S+W)
        self.logger.debug('Canvas with scrollbar has been crated.')

        # add frame to canvas
        self.frame = Frame(self.canvas, bg='white')
        self.frame.grid(row=0, column=0, rowspan=8, columnspan=4)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.logger.debug('Frame is placed in canvas.')

        self.empty1 = Label(self.frame, bg='white', text="Name each individual quencher", bd=6, fg='#1D265E')
        self.empty1.grid()

        # create entry points for every position
        i = 1
        self.logger.debug('Loop to create names has started.')
        for name in self.names:
            e = Entry(self.frame, width=25)
            e.grid(row=i, column=1, sticky=E)
            self.entry[name] = e

            lb = Label(self.frame, font=(self.font1, self.size), text=name, bg='white', fg='#1D265E', bd=6)
            lb.grid(row=i, column=0, sticky=W)
            self.label[name] = lb
            i += 1

        # frame for the bottom button
        self.frame2 = Frame(self.root, bg='white')
        self.frame2.grid(row=13, column=0, rowspan=1, columnspan=4)
        self.button1 = Button(self.frame2, font=(self.font1, self.size),
                              text="Finalize naming", width=20, command=self.PullNamesToPar,
                              bg='#1D265E', fg='white')
        self.button1.grid(row=11, column=1, columnspan=5)
        self.logger.debug('The button to save the names has been created.')

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.logger.debug('Reset the scroll region to encompass the inner frame.')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # checks if all entry's are filled in and puts these names to par so they can be returned to main GUI
    def PullNamesToPar(self):
        self.logger.debug('Pull the names from the entry boxes.')
        k = 0
        try:
            for name in self.names:
                if len(str(self.entry[name].get())) > 2:
                    self.par.namesExperiments[k] = str(self.entry[name].get())
                    self.logger.debug('Experiment name on position {} is {}.'.format(k, self.par.namesExperiments[k]))
                    k += 1
                else:
                    k += 1
                    pass

            self.CheckDuplicates()
            self.root.quit()
            self.root.destroy()
        except:
            messagebox.showerror('Wrong input', 'There was an error with the importing of '
                                                'the custom names of the quenchers. \n'
                                                'Please shut down the pumps and try again.')
            self.logger.error('A error has occurred while pulling the names from an entry', exc_info=True)
            return False
        finally:
            for item in range(len(self.par.namesExperiments)):
                self.par.legend[item] = '{} = {}'.format(self.par.namesPositions[item], self.par.namesExperiments[item])
 
    def CreateNames(self):
        # creates a list of names and the needed vectors
        # logs all the data appropriately
        self.entry = {}
        self.label = {}
        self.names = []

        for i in range(self.par.experimentNumber):
            self.names.append(('experiment ' + str(i+1)))
            self.logger.debug('Experiment name created is {}'.format(self.names[-1]))

    def CheckDuplicates(self):
        # checks if given names are duplicates of one another and gives them a sequential number if so.
        for i in range(len(self.par.namesExperiments) - 1):
            b = 1
            for j in range(i + 1, len(self.par.namesExperiments) ):
                if (self.par.namesExperiments[i] == self.par.namesExperiments[j]):
                    self.par.namesExperiments[j] = "{}_{}".format(self.par.namesExperiments[i], str(b))
                    b += 1
                else:
                    pass

if __name__ == '__main__':
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparAuto()
    par.experimentNumber = 5
    par.namesExperiments = [None] * par.experimentNumber
    for i in range(len(par.namesExperiments)):
        letter = int(i / 8) + 65
        position = (i % 8) + 1
        par.namesExperiments[i] = '{}{}'.format(chr(letter), str(position))

    gui2 = NamingGUI(par)
    gui2.root.mainloop()

    for i in range(len(par.namesExperiments)):
        print(par.namesExperiments[i])