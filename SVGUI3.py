from tkinter import *
import sys
import os
import SimpleOneTimeTask as ST
import time
import xlsxwriter
import logging
from Parameters_SV import ImportparSV
from DatabaseCommander import DatabaseHandler
import threading
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import datetime

class SVInterface3:
    def __init__(self, par, SolventPump, QuencherPump, CatalystPump):
        self.logger = logging.getLogger('SternVolmerLog')
        self.logger.info('GUI1 has been created')
        self.log = logging.getLogger('Log.GUI3')
        self.log.debug('Gui3 has been called')
        self.root = Tk()
        self.root.title('Calculations in progress')
        self.par = par
        self.font1 = "Roboto Condensed"
        self.size = 11
        self.solventPump = SolventPump
        self.quencherPump = QuencherPump
        self.catalystPump = CatalystPump

        # creating self.frame and adding that to self
        self.frame = Frame(self.root, bg='white')
        self.frame.grid()

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
        self.logger.debug('Logo created')

        # creating the textbox and its scrollbar
        self.textbox = Text(self.frame, bg='white', font=(self.font1, self.size), state=DISABLED)
        self.textbox.grid(row=4, column=0, columnspan=5, sticky='E')
        self.textbox.tag_configure("stderr", foreground="#b22222")
        self.scrollbar = Scrollbar(self.frame)

        # connect the scrollbar with the textbox
        self.scrollbar.configure(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=4, column=4, sticky=N+S+W)
        self.logger.debug('textbox with scrollbar created')

        # connects print statement to system , Source:
        # https://stackoverflow.com/questions/20933639/tkinter-button-events-firing-on-load
        self.stdoutOld = sys.__stdout__
        sys.stdout = TextRedirector(self.textbox, "stdout")

        self.empty2 = Label(self.frame, font=(self.font1, self.size))
        self.empty2.configure(text=" ", bg='white')
        self.empty2.grid(row=5, column=0, columnspan=5, rowspan=2)

        # start the functions of the GUI
        self.log.debug('GUI3 initialization has finished')
        self.textbox.insert(END, 'GUI3 has been initialized')
        self.root.update()
        self.StartPumps()

    def StartPumps(self):
        # change OS path to Data sub-directory
        self.par.scriptDir = os.getcwd()
        self.par.dataDir = os.path.join(self.par.scriptDir, 'Data_SV')
        ST.make_sure_path_exists(self.par.dataDir)
        self.par.fileDataDir = os.path.join(self.par.dataDir, self.par.nameTxtFile)

        #create own folder for experiment
        self.par.workingDir = os.path.join(self.par.dataDir, self.par.nameExperiment)
        ST.make_sure_path_exists(self.par.workingDir)

        # copy avasoft txt file to its private folder
        ST.CopyAvasoftFile(self.par.fileDataDir, self.par.workingDir)

        os.chdir(self.par.dataDir)
        print('Working directory has changed')
        self.log.debug('GUI3 has changed working directory')

        # set correct flow rate to the pumps
        self.solventPump.SetFlowrate(self.par.solQuenThroughput)
        self.catalystPump.SetFlowrate(self.par.catThroughput)

        print("Throughput's are send to pumps")
        self.log.debug('Pumps have successfully been turned on.\n Main loop is starting')
        self.root.update()
        self.MainLoop()

    def MainLoop(self):
        print('main loop started')
        # check if path is correcct
        self.root.update()
        self.log.debug('Main loop has started')
        self.root.update()

        # create working vector for data, average and deviation
        self.measuredData = [[0]*self.par.numberOfMeasurmentsPerConcentration for n in range(self.par.numberOfConcentrations)]
        self.measuredAvr = [0] * self.par.numberOfConcentrations
        self.measuredDiv = [0] * self.par.numberOfConcentrations
        self.measuredInt = [0] * self.par.numberOfConcentrations

        # print the directory where the avasoft.txt file is / should be
        print('Path Avasoft is: {}'.format(self.par.dataDir))
        self.root.update()

        # start internal main loop
        # this loop changes the flow rate of the pumps
        # and reads data from the Avasoft text file to a Excel file
        print('Start experiment')

        # give a time estimate when the experiment will be finished
        currentTime = time.time()
        runTime = self.par.numberOfConcentrations * (self.par.numberOfMeasurmentsPerConcentration - 1) * self.par.interval + self.par.resTimeDv * self.par.numberOfConcentrations
        finalTime = currentTime + runTime
        timeFinal = datetime.datetime.fromtimestamp(float(finalTime))
        fmt = "%H:%M:%S"
        finalTg = str(timeFinal.strftime(fmt))
        print('The experiment is expected to be finished at: {}'.format(finalTg))
        self.root.update()

        # start main loop of experiment
        for row in range(0, self.par.numberOfConcentrations):
            currentRow = row
            writingRow = row + 1
            print('Concentration {} is tested'.format(row + 1))
            self.root.update()
            self.textbox.see(END)

            # calculate and set value for the solvent pump
            throughputSolventPump = round(self.par.fractionSolventPump[row] * self.par.totalThroughput)
            self.root.update()
            if throughputSolventPump == 0.0:
                self.solventPump.StopPump()
            else:
                self.solventPump.SetFlowrate(throughputSolventPump)

            print("The flow rate of the solvent pump has changed to {0}".format(str(throughputSolventPump)))
            self.root.update()
            self.textbox.see(END)

            # Calculate and set value for the quencher pump
            throughputQuenPump = round(self.par.fractionQuencherPump[row] * self.par.totalThroughput)
            if throughputQuenPump == 0.0:
                self.quencherPump.StopPump()
            else:
                self.quencherPump.SetFlowrate(throughputQuenPump)

            print("The flow rate of the quencher pump has changed to {0}".format(str(throughputQuenPump)))
            self.root.update()
            self.textbox.see(END)

            # Calculate the time delay necessary to develop flow
            if row == 0:
                self.Pauser(self.par.factorFirstMeasurement * self.par.resTimeDv)
            else:
                self.Pauser(self.par.resTimeDv)

            # Start inner loop
            # This loop reads the last value from the Avasoft.txt file
            # And puts it into excel
            # Inbuild catch to differ between 0.2 and 0,2 value
            startTime = time.time()
            for col in range(0, self.par.numberOfMeasurmentsPerConcentration):
                writingCol = col + 1

                # read last line of data from the avasoft txt file
                try:
                    file = open(self.par.fileDataDir, "r")
                    lines = file.readlines()
                    file.close()
                except:
                    self.quencherPump.StopPump()
                    self.solventPump.StopPump()
                    self.catalystPump.StopPump()
                    self.logger.error('File could not be read because: {}'.format('avasoft blocked toegang tot txt file'))
                    exit()

                endLine = lines[-1]
                split = endLine.split(' ')
                value = split[-1]
                self.logger.debug('Last read data from txt file is : {}'.format(value))
                self.root.update()

                # catch a . or , failure
                try:
                    value = float(value)
                except:
                    val = value.split(',')
                    nval = val[0] + '.' + val[1]
                    value = float(nval)

                # if extraI0 is checked than create and extra column
                if row == (self.par.numberOfConcentrations - 1) and self.par.ExtraI0:
                    row += 2
                    writingRow = row + 1

                # Write the found value to the excel sheet
                self.measuredData[currentRow][col] = value
                print('Experiment number {} is now measured {} time(s)\n'.format(writingRow, writingCol))
                self.root.update()
                self.textbox.see(END)

                # Calculate the time needed tho match the interval for this cycle
                self.Pauser(self.par.interval - (time.time() - col * self.par.interval - startTime))

        # close main loop and Excel file
        print("Measurements for concentration {0} has finished".format(writingRow))
        print("The excel writer has been closed,\n file is safe to open.")
        self.root.update()
        self.textbox.see(END)

        # change current folder to specified working directory
        os.chdir(self.par.workingDir)

        # create excel file
        self.ExcelDataWriter()

        # create plot
        self.PlotDataFigure()

        # go back to origina diroectory
        os.chdir(self.par.scriptDir)

        # write data to database
        self.WriteToDatabase()

        # finalize script
        self.Finalize()

    def ExcelDataWriter(self):
        # create a xls work book
        self.book1 = xlsxwriter.Workbook(self.par.nameExcelFile)
        self.sheet = self.book1.add_worksheet('Sheet1')
        print('Excel file is being created')
        self.root.update()
        self.textbox.see(END)
        self.log.debug('Excel file has been created and is open in memory')

        # print headers into the excel file
        self.sheet.write(0, 0, "Quencher concentration [M]")
        for i in range(1, self.par.numberOfMeasurmentsPerConcentration + 1):
            self.sheet.write(0, i, 'Peak Area {}'.format(i))
        self.sheet.write(0, self.par.numberOfMeasurmentsPerConcentration + 1,
                         'Average')
        self.sheet.write(0, self.par.numberOfMeasurmentsPerConcentration + 2,
                         'Deviation (%)')
        self.sheet.write(0, self.par.numberOfMeasurmentsPerConcentration + 3,
                         'I0/I')

        # write down the quencher concentrations
        for row in range(len(self.par.con)):
            self.sheet.write(row + 1, 0, self.par.con[row])

        # write the obtained data from the main loop to the Excel file
        for row in range(len(self.measuredData)):
            for col in range(len(self.measuredData[0])):
                self.sheet.write(row + 1, col + 1,
                                 self.measuredData[row][col])

        # write the averages
        for row in range(len(self.measuredData)):
            writeAverage = '=AVERAGE({0}{1}:{2}{1})'.format(chr(66), (row + 2),
                                                            chr(65 + self.par.numberOfMeasurmentsPerConcentration))
            self.sheet.write(row + 1,
                             self.par.numberOfMeasurmentsPerConcentration + 1,
                             writeAverage)

        # write standard deviation
        for row in range(len(self.measuredData)):
            writeDev = '=_xlfn.STDEV.P({0}{1}:{2}{1})/{3}{1}'.format(chr(66), (row + 2),
                                                                     chr(
                                                                         65 + self.par.numberOfMeasurmentsPerConcentration),
                                                                     chr(
                                                                         65 + self.par.numberOfMeasurmentsPerConcentration + 1))
            self.sheet.write(row + 1,
                             self.par.numberOfMeasurmentsPerConcentration + 2,
                             writeDev)

        # write I0/I
        for row in range(len(self.measuredData)):
            writeIntensity = '={0}{1}/{0}{2}'.format(chr(65 + self.par.numberOfMeasurmentsPerConcentration + 1), 2,
                                                     (row + 2))
            self.sheet.write(row + 1,
                             self.par.numberOfMeasurmentsPerConcentration + 3,
                             writeIntensity)

        # add slope, intercept and statistical data
        # write text
        try:
            self.sheet.write(len(self.measuredData) + 1,
                             self.par.numberOfMeasurmentsPerConcentration + 1, "SLOPE")
            self.sheet.write(len(self.measuredData) + 2,
                             self.par.numberOfMeasurmentsPerConcentration + 1, "INTERCEPT")
            self.sheet.write(len(self.measuredData) + 3,
                             self.par.numberOfMeasurmentsPerConcentration + 1, "CORRELATION R2")
        except EXCEPTION as e:
            self.logger.debug('{}'.format(e))
            pass

        try:
            # write formulas for slope
            self.sheet.write(len(self.measuredData) + 1,
                             self.par.numberOfMeasurmentsPerConcentration + 3,
                             "=SLOPE({0}{1}:{0}{2},{3}{1}:{3}{2})".format(chr(65 + self.par.numberOfMeasurmentsPerConcentration + 3),
                                                                          1,
                                                                          len(self.measuredData),
                                                                          chr(65)))
            # intercept
            self.sheet.write(len(self.measuredData) + 2,
                             self.par.numberOfMeasurmentsPerConcentration + 3,
                             "=INTERCEPT({0}{1}:{0}{2},{3}{1}:{3}{2})".format(
                                 chr(65 + self.par.numberOfMeasurmentsPerConcentration + 3),
                                 1,
                                 len(self.measuredData),
                                 chr(65)))
            # correlation R2
            self.sheet.write(len(self.measuredData) + 3,
                             self.par.numberOfMeasurmentsPerConcentration + 3,
                             "=CORREL({0}{1}:{0}{2},{3}{1}:{3}{2})^2".format(
                                 chr(65 + self.par.numberOfMeasurmentsPerConcentration + 3),
                                 1,
                                 len(self.measuredData),
                                 chr(65)))
        except EXCEPTION as e:
            self.logger.debug('{}'.format(e))
            pass

        # create chart
        chart1 = self.book1.add_chart({'type': 'scatter'})
        cat = '={0}!A2:A{1}'.format('Sheet1', (self.par.numberOfConcentrations + 1))
        val = '={0}!{1}2:{1}{2}'.format('Sheet1',
                                        chr(65 + self.par.numberOfMeasurmentsPerConcentration + 3),
                                        (self.par.numberOfConcentrations + 1))
        chart1.add_series({
            'categories': cat,
            'values': val,
            'trendline': {'type': 'linear',
                          'display_r_squared': True,
                          'display_equation': True,
                          },
        })

        chart1.set_title({'name': 'Stern-Volmer {0}'.format(self.par. quencherName)})
        chart1.set_x_axis({'name': 'Concentration Quencher [M]'})
        chart1.set_y_axis({'name': 'I0/I'})
        self.sheet.insert_chart('I14', chart1)
        self.book1.close()
        self.logger.info('Excel file has been created')
        pass

    def PlotDataFigure(self):

        # calculate average
        for row in range(len(self.measuredData)):
            self.measuredAvr[row] = np.average(self.measuredData[row])

        # calculate standard deviation
        for row in range(len(self.measuredData)):
            self.measuredDiv[row] = np.std(self.measuredData[row])

        # calculate I0/I
        for row in range(len(self.measuredData)):
            self.measuredInt[row] = self.measuredAvr[0] / self.measuredAvr[row]

        # plot the data and create the figure
        # create a plot of the data gained from the experiment
        # link to information:
        # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        fig = plt.figure()
        ax = plt.subplot(111)

        # calculate the trendline
        self.slope, self.intercept, self.rValue, self.pValue, self.stdErr = stats.linregress(self.par.con, self.measuredInt)
        self.rSquared = self.rValue ** 2

        # plot data and trendline
        ax.plot(self.par.con, self.measuredInt, 'bo', label='data')
        ax.plot(self.par.con, (self.intercept + self.slope * np.array(self.par.con)), 'r--', label='trendline')

        # name axes
        plt.xlabel('Concentration Quencher [M]')
        plt.ylabel('I0/I')
        # plt.title('Stern Volmer experiment: {}'.format(self.par.nameExperiment))
        plt.grid(True)
        plt.axis([0, 1.1 * max(self.par.con), 0, 1.1 * max(self.measuredInt)])

        # write text into graph
        ax.text(0.1 * self.par.con[1], 0.0, '{}{} = {}\nformula = {} + X{}{}\n'.format(
            'R', chr(0x00B2), round(self.rSquared, 4), round(self.intercept, 4), r'$\cdot$', round(self.slope, 4)), fontsize=14)

        # Shrink current axis's height by 10% on the bottom
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0., -0.01, 1., -.101),
                  ncol=2, mode="expand", borderaxespad=0., fancybox=True)

        plt.savefig('SV_Exp_{}{}'.format(self.par.nameExperiment, '.png'))
        self.logger.info('Graph has been created and saved')

        pass

    def WriteToDatabase(self):
        # calculate the quenching rate kq
        if self.par.lifetime is None:
            self.par.kq = None
        else:
            self.par.kq = self.slope / self.par.lifetime

        # prepare datablob
        # create new vectors with titles
        con = self.par.con.tolist()
        avr = self.measuredAvr
        std = self.measuredDiv
        frac = self.measuredInt

        #loop for raw data
        mes = self.measuredData
        self.logger.debug('con {}'.format(con))
        self.logger.debug('avr {}'.format(avr))
        self.logger.debug('std {}'.format(std))
        self.logger.debug('frac {}'.format(frac))
        self.logger.debug('mes {}'.format(mes))

        # merge all list together horizontally
        dataBlob = str([con + mes + avr + std + frac])

        # create data tuple as input for the database
        # Name, Date, Catalyst, Solution, Quencher, Num_points, Slope, R2, Kq, Data

        data = (self.par.date, self.par.nameExperiment,
                self.par.catalystName, self.par.solventName,
                self.par.quencherName, self.par.numberOfConcentrations,
                self.slope, self.rSquared,
                self.par.kq, dataBlob)

        # write the data to the database
        databaseCommander = DatabaseHandler(self.par.databaseName, self.par.scriptDir)
        databaseCommander.InsertSVExperiment(data)

        pass

    def Finalize(self):
        # copy avasoft txt file to its private folder
        ST.CopyAvasoftFile(self.par.fileDataDir, self.par.workingDir)

        # send a email
        print('Sending email that results are ready.')
        self.root.update()
        self.textbox.see(END)
        ST.SendEmail(self.par)

        print('Stern-Volmer experiment Finished')
        self.root.update()
        self.textbox.see(END)

        message = 'OFF\r'
        self.solventPump.StopPump()
        self.quencherPump.StopPump()
        self.catalystPump.StopPump()

        print('The pumps are Stopped')
        print('This program will shut itself down in 10 seconds')

        self.root.update()
        self.textbox.see(END)

        # reset system changes
        sys.stdout = self.stdoutOld
        os.chdir(self.par.scriptDir)

        self.Pauser(10)
        print('program ended')
        self.root.quit()
        self.root.destroy()

    def Pauser(self, pauzetime):
        pauzetime = max(pauzetime, 0.1)
        threadPauser = threading.Thread(target=self.waitingThread, args=(pauzetime,))
        self.logger.debug('Pausing thread created.')

        threadPauser.start()
        while True:
            time.sleep(0.3)
            self.root.update()

            if not threadPauser.is_alive():
                self.logger.debug('Pausing thread has terminated.')
                self.root.update()
                self.textbox.see(END)
                break

    @staticmethod
    def waitingThread(pauzetime):
        time.sleep(pauzetime)
        pass

# class that is needed to print in textwriter
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
    logger = logging.getLogger('SternVolmerLog')
    logging.basicConfig(filename='SternVolmerLog.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    par = ImportparSV()
    par.nameExperiment = 'excelfile'
    par.nameOutputAvas = 'file.txt'
    par.numberOfConcentrations = 6
    par.numberOfMeasurmentsPerConcentration = 10
    par.interval = 1
    par.resTimeDv = 20
    par.resTimeDv = 20
    gui1 = SVInterface3(par)
    gui1.root.mainloop()