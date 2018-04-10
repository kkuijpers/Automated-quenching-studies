from tkinter import *
from Parameters_Auto import ImportparAuto
import logging

class ShowSample:
    def __init__(self):
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('The Show Sample GUI has started.')
        self.root2 = Tk()
        self.root2.title('Name quenchers individually')
        self.root2.configure(bg='white')

        self.font1 = "Roboto Condensed"
        self.size = 11

        self.frame = Frame(self.root2, bg='white')
        self.frame.grid()

        # create some labels to visualize , how to put the vile in the tray
        self.img = PhotoImage(file='SmallRekje.ppm')
        self.imageLabel = Label(self.frame)
        self.imageLabel.image = self.img
        self.imageLabel.configure(image=self.img, bg='white')
        self.imageLabel.grid(row=0, column=0, rowspan=10, columnspan=10)
        self.logger.debug('Sample tray figure has been loaded.')

        self.empty1 = Label(self.frame, font=(self.font1, self.size))
        self.empty1.configure(text=" ", bg='white', fg='#1D265E', bd=6, width=80)
        self.empty1.grid(row=11)

        self.explanation = "One should always fill the sample tray from left to right and from top to bottom." \
                           "\nAs shown in the picture above the first sample should always go in position A1,\n" \
                           "and the second vail in A2 and so on. \n\n" \
                           "Please remember which vial goes in which position. \nIn the next part of the GUI you can " \
                           "choose if you want to individually name the samples. \n" \
                           "If you do not do this, then the program will automatically " \
                           "name the samples after their position."

        self.label1 = Label(self.frame, font=(self.font1, self.size), justify=LEFT)
        self.label1.configure(text=self.explanation, bg='white', fg='#1D265E', bd=6, width=80)
        self.label1.grid(row=13, columnspan=5, sticky=W)
        self.logger.debug('Text under the figure has been placed.')

        self.empty2 = Label(self.frame, font=(self.font1, self.size))
        self.empty2.configure(text=" ", bg='white', fg='#1D265E', bd=6, width=80)
        self.empty2.grid(row=14, columnspan=5)

if __name__ == '__main__':
    logger = logging.getLogger('AutosamplerLog')
    logging.basicConfig(filename='AutosamplerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparAuto()
    gui2 = ShowSample()
    gui2.root2.mainloop()