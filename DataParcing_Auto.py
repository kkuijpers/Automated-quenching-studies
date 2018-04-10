import logging
import os
import SimpleOneTimeTask as ST
import datetime
import shutil
from Parameters_Auto import ImportparAuto
from DatabaseCommander import DatabaseHandler
import numpy as np
from scipy.stats import linregress  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas

# For user:
# Things to change in order to run data analysis separately.
# first injection time on line 31
# t_0 and I_0 at the bottom of the file as well as the name of the experiment and the number of samples
# on line 504-508

def ParceData(par):
    logger = logging.getLogger('Data_parsing_Log')
    logging.basicConfig(filename='Data_parsing_Log.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # copy the Avasoft file to the newly created directory
    CopyAvasoftFile(os.path.join(par.dataDir, par.nameFileAvasoft), par.workingDir)

    # set parameters
    par.firstInjectionTime = 440 #630 2CzPN #440 Mes-Acr #540 RA-48
    par.timestep = 410  # 410

    # set standard data
    par.screeningWidth = 5
    par.stepSize = 3
    logger.debug('The screening with is set to: {}'.format(par.screeningWidth))
    logger.debug('The step size is set to: {}'.format(par.stepSize))
    logger.debug('The file name is: {}'.format(par.name))

    # extract two vectors from the Avasoft data file
    [sec, intensity] = ExtractData(par, par.nameFileAvasoft)

    # removes the start up data from the previous made vectors
    [sec, intensity] = RemoveStardUp(sec, intensity, par.dataStartTime, par.dataStartIntensity)
    sec = StartSecondsAtZero(sec)

    # return the averages of the vectors.
    sec = ReturnAverage(sec, par.screeningWidth, par.stepSize)
    intensity = ReturnAverage(intensity, par.screeningWidth, par.stepSize)

    # start doing stuff with data and saving it in designated folder
    os.chdir(par.workingDir)
    # plot the (first time) averaged data and place vertical lines at the begin and end of each peak
    CreateVerticalLines(sec, intensity, par, saveFigure=True)
    # partition data according to previous line placements
    [partitionedTime, partitionedInt] = PartitionLists(sec, intensity, par)
    # plot the partitioned data
    PloteffectiveQuenching(partitionedTime, partitionedInt, par)

    os.chdir(par.scriptDir)
    if par.mainRunParcing:
        WriteToDatabase(par, partitionedInt)

def ExtractData(par, fileName):
    # this function extracts the time and intensity data from the Avasoft text file.
    # this data is saved in two vectors while extraction takes place.
    # these two vectors are returned from the function
    logger = logging.getLogger('Data_parsing_Log')
    logger.info('Data extraction from text file has started.')

    os.chdir(par.dataDir)

    # create empty vectors to be filled
    seconds = []
    intensity = []
    data = []

    # open file and read all the lines
    with open(fileName, 'r') as file:
        lines = file.readlines()
        lines = lines[13::]

    # in each line tries to read a number and store it in the corresponding vector
    for line in lines:
        del data[:]
        parts = line.split(' ')
        for part in parts:
            try:
                data.append(float(part))
            except ValueError:
                continue
        seconds.append(data[0])
        intensity.append(data[1])
    os.chdir(par.scriptDir)
    logger.info('Data extraction from text file has ended.')
    return seconds, intensity

def RemoveStardUp(timeArray, intensityArray, timeOfFirstInject, IntOfFirstInject):
    # this function looks for the time when the first injection is commanded to the autosampler.
    # the function than takes these values and return a list without the startup from the Avasoft file.

    logger = logging.getLogger('Data_parsing_Log')
    logger.info('Start up is being removed from the date file.')
    # find the index at which stability was reached
    index1 = timeArray.index(timeOfFirstInject)
    index2 = intensityArray.index(IntOfFirstInject)

    # return the cut of array
    if index1 == index2:
        logger.debug('Both indexes where the same.')
        return timeArray[index1:len(timeArray)], intensityArray[index2:len(intensityArray)]
    elif index1 < index2:
        logger.debug('index1 was smaller than index2.')
        return timeArray[index1:len(timeArray)], intensityArray[index1:len(intensityArray)]
    elif index1 > index2:
        logger.debug('index2 was smaller than index1.')
        return timeArray[index2:len(timeArray)], intensityArray[index2:len(intensityArray)]
    else:
        logger.error('index exception was chosen.')
        return timeArray, intensityArray

def StartSecondsAtZero(timeArray):
    # this function subtracts the begin time from the complete time vector. than returns it.
    start = timeArray[0]
    for k in range(len(timeArray)):
        timeArray[k] = timeArray[k] - start
    return timeArray


def ReturnAverage(array, width, step):
    # this function returns a vector of local averages.
    # removing noise from the data signal
    # the function takes /width number of data points and calculates the average
    # than the functions takes a step of size /step and repeats until it is at the end of the vector.
    logger = logging.getLogger('Data_parsing_Log')
    logger.info('The average of a vector is being returned '
                'with {} width and a step size of {}'.format(width, step))

    average = []
    for i in range(int(len(array) / step)):
        part = array[(i * step):((i * step) + width)]
        average.append(float(np.average(part)))

    return average

def PartitionLists(time, data, par):
    # this function returns a list of lists
    # with each inner list all the data of one peak / injection interval.
    # these inner list can have variable lengths. There length is determined by
    # empirical time steps sizes.
    logger = logging.getLogger('Data_parsing_Log')
    logger.info('The list partition function is started.')

    listOfListsTime = [None] * par.experimentNumber
    listOfListsInt = [None] * par.experimentNumber
    index = [None] * par.experimentNumber
    logger.debug('The list of list Time has a length of :{}'.format(len(listOfListsTime)))
    logger.debug('The list of list Int has a length of :{}'.format(len(listOfListsInt)))
    logger.debug('The number of experiments is :{}'.format(par.experimentNumber))

    for i in range(par.experimentNumber):
        if i == 0:
            index[i] = indexEstimator(time, par.firstInjectionTime)
            listOfListsTime[i] = time[0:index[i]]
            listOfListsInt[i] = data[0:index[i]]
            logger.debug('loop of assigning lists in lists is in iteration {}'.format(str(i)))
            logger.debug('index measured is {} for value {}'.format(index[i], par.firstInjectionTime))
            logger.debug('All values are saved from index:{} until index:{}'.format(0, index[i]))
            logger.debug('length of inner list of time is:{}'.format(len(listOfListsTime[i])))
            logger.debug('length of inner list of int is:{}'.format(len(listOfListsInt[i])))

        else:
            valueNextLine= par.firstInjectionTime + par.timestep * i
            index[i] = indexEstimator(time, valueNextLine)
            listOfListsTime[i] = time[index[i - 1]:index[i]]
            listOfListsInt[i] = data[index[i - 1]:index[i]]
            logger.debug('loop of assigning lists in lists is in iteration {}'.format(str(i)))
            logger.debug('index measured is {} for value {}'.format(index[i], valueNextLine))
            logger.debug('All values are saved from index:{} until index:{}'.format(index[i - 1], index[i]))
            logger.debug('length of inner list of time is:{}'.format(len(listOfListsTime[i])))
            logger.debug('length of inner list of int is:{}'.format(len(listOfListsInt[i])))

    return listOfListsTime, listOfListsInt

def CreateVerticalLines(timeArray, intensityArray, par, saveFigure=False):
    # this function takes the time and intensity vector's and plots these in a graph
    # than puts red vertical lines in the graph in order to visualize how the complete vector is cut up.
    # if saveFigure is set to true than the figure is not displayed but saved.
    logger = logging.getLogger('Data_parsing_Log')
    logger.info('Lines are plotted into the original graph.')

    begin = timeArray[0]
    step1 = par.firstInjectionTime
    step2 = par.timestep
    nlines = par.experimentNumber
    endx = begin + step1 + (nlines-1) * step2 + 20

    # creates figure to plot
    fig = plt.figure()
    plt.plot(timeArray, intensityArray)
    plt.axis([(begin - 20), endx, 0, np.amax(intensityArray)])
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity')

    # plots the vertical lines
    for i in range((nlines + 1)):
        if i == 0:
            plt.axvline(begin, color='r')
            continue
        else:
            plt.axvline((begin + step1 + ((i-1) * step2)), color='r')

    # check if the figure has to be shown or saved
    if not saveFigure:
        plt.show()
    if saveFigure:
        plt.savefig('cut_visualization.png', format='png')
        plt.close(fig)

def indexEstimator(list, value):
    # this function takes a list and a value
    # and return the first index of that list that has a value larger than
    # the given value.
    for i in range(len(list)):
        if list[i] < float(value):
            continue
        else:
            index = i
            return index

def PloteffectiveQuenching(ListOfListsTime, ListOfListInt, par):
    logger = logging.getLogger('Data_parsing_Log')
    logger.info('The plot effective quenching  function is called.')

    step = par.stepSize
    width = par.screeningWidth

    # create a file where the brute data will be saved
    SaveDiffSlope(0, 0, par.namesExperiments[0], par, start=True)

    # color definition that are used to plot: http://www.color-hex.com
    green = "#00b300"
    red = "#e7001d"
    orange = "#ff6101"
    yellow = "#e7ca00"
    blue = "#0000ff"
    white = "#f2f2f2"
    logger.debug('The colors for the overview plot have been defined.')

    # calculate the number of rows and columns required for the subplot
    rows = int((par.experimentNumber - 1) / 8) + 1
    if par.experimentNumber <= 8:
        cols = par.experimentNumber
    else:
        cols = 8
    logger.debug("The number of rows is set to {}, and the there are {} columns".format(rows, cols))

    # create figure 1
    plt.figure(1)
    fig1, axes1 = plt.subplots(nrows=rows, ncols=cols, dpi=100,
                               frameon=False, facecolor=white, edgecolor='w',
                               sharey=True)

    # start of main loop ( loops over every part(peak) of the original data
    for i in range(par.experimentNumber):
        # create new variable for the inner list data
        partTime = ListOfListsTime[i]
        partInt = ListOfListInt[i]

        # create empty list to fill in and use
        # stdInt = []
        averageInt = []
        averageSec = []
        stdErr = []
        slopeInt = []
        stdInt = []

        # current row and column in subplot matrix
        plt.figure(1)
        if rows == 1:
            col = (i % 8)
            axes1[col].get_xaxis().set_visible(False)
            axes1[col].set_ylim([0, 100])
        else:
            row = int(i / 8)
            col = (i % 8)
            axes1[row, col].get_xaxis().set_visible(False)
            axes1[row, col].set_ylim([0, 100])
        logger.debug('configuring position: {}'.format(par.namesExperiments[i]))

        # start inner loop to create vectors
        for j in range(int(len(partInt) / step)):
            # piece of data
            data = partInt[(j * step):((j * step) + width)]
            sec = partTime[(j * step):((j * step) + width)]

            # calculate the averages
            averagePartSec = np.average(sec)
            averagePartInt = np.average(data)
            averageInt.append(averagePartInt)
            averageSec.append(averagePartSec)

            # calculate the slope and the standard deviation from this line (stderr)
            # stdInt.append(np.std(data))
            lineData = linregress(sec, data)
            slopeInt.append(lineData[0])
            stdErr.append(lineData[4])
            stdInt.append(np.std(data))

        # normalize the created vectors
        # stdInt = NormalizePercent(stdInt)
        averageInt = NormalizePercent(averageInt)
        slopeInt = NormalizePercent(slopeInt, averageInt)

        # calculate the intensity fraction and the slope difference
        intFrac = (round(min(averageInt) / max(averageInt), 3))
        slopeDiff = (round(max(slopeInt) - min(slopeInt), 3))

        # calculate the maximum difference in the slope and the I/I0 and write them to file
        if intFrac < 0:
            intFrac = 0
        SaveDiffSlope(slopeDiff, intFrac, par.namesExperiments[i], par)
        logger.debug('The intensity fraction is : {}'.format(intFrac))
        logger.debug('The slope difference is {}'.format(slopeDiff))

        # set color for overview plot
        if intFrac <= 0.5:
            clr = green
            colorCode = "Green"
        elif (intFrac <= 0.75) and (slopeDiff >= 4.0):
            clr = orange
            colorCode = "Orange"
        elif (intFrac <= 0.75) and (slopeDiff < 4.0):
            clr = orange
            colorCode = "Orange"
        else:
            clr = red
            colorCode = "Red"
        logger.debug('The chosen color is: {}'.format(clr))
        par.colorCodes[i] = colorCode

        # plot the individual peaks in the subplot with their corresponding color
        plt.figure(1)
        if rows == 1:
            axes1[col].plot(averageSec, averageInt, color=clr)
            axes1[col].patch.set_facecolor(white)
            axes1[col].set_title(par.namesPositions[i])
        else:
            axes1[row, col].plot(averageSec, averageInt, color=clr)
            axes1[row, col].patch.set_facecolor(white)
            axes1[row, col].set_title(par.namesPositions[i])
        logger.debug('The overview subplot has been created.')

        # plot the individual peak data with
        # average, slope and standard error
        plt.figure(2)
        fig2, ax1 = plt.subplots()
        # lns2 = ax1.plot(averageSec, stdInt, 'bo', label='Std')
        lns1 = ax1.plot(averageSec, averageInt, 'k', label='Intensity')
        # lns3 = ax1.plot(averageSec, stdErr, 'g^', label='Stderr')
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('Normalized data in percent %')

        # create additional y-axis
        ax2 = ax1.twinx()
        lns4 = ax2.plot(averageSec, slopeInt, 'r--', label='Rel Slope')
        ax2.set_ylabel('Relative Slope (data)')
        # create the legend in the figure
        fig2.tight_layout()
        lns = lns1 + lns4  # + lns2 +lns3
        labs = [l.get_label() for l in lns]
        plt.legend(lns, labs, loc=2)

        # save the figure
        plt.savefig('Data_{1}_exp_{0}{2}'.format(par.namesExperiments[i], par.name, '.png'))
        plt.close(fig2)

        logger.debug('The individual plot has been created and saved.')

    # remove the empty subplots from the figure and save it to pdf
    plt.figure(2)
    if (par.experimentNumber % 8 != 0) and (par.experimentNumber > 8):
        for k in range((rows * 8) - par.experimentNumber):
            place = (k * (-1)) - 1
            axes1[(rows - 1), place].set_visible(False)

    pdfname2S = 'fast_overview.pdf'
    pdfname2 = PdfPages(pdfname2S)
    pdfname2.savefig()
    pdfname2.close()
    logger.debug('Saved the complete overview figure to pdf.')

    if par.selfNaming:
        CreateOvervieuwPDF(par, pdfname2S)

def NormalizePercent(vector, vector2=[None]):
    # normalize a input vector
    # the vector is normalized either to itself (if vector2 is None)
    # or to the second vector / used for the slope vector
    normalized = []

    if vector2[0] is None:
        max_val = max(np.absolute(vector))
        for item in vector:
            normalized.append((item / max_val) * 100)
    else:
        max_val = max(np.absolute(vector2))
        for item in vector:
            normalized.append((item / max_val))

    return normalized

def SaveDiffSlope(slopeDiff, intData, sampleName, par, start=False):
    # this function saves some core data from the function ParseAndPlotPartitions to a file
    # this function creates / overwrites a text file if start==True
    # otherwise this function adds the data
    filename = '{0}{1}{2}'.format('Data_slope_', par.name, ".txt")

    currTime = datetime.datetime.now()
    currTime1 = currTime.strftime('%Y/%m/%d %H:%M:%S')
    currTime2 = currTime.strftime('%Y/%m/%d')

    if start:
        with open(filename, 'w') as file:
            file.write("This data is the difference between the relative slopes.\n"
                       "These the larger the measured difference the better the quencher.\n"
                       "Today is {0},\nand the experiment is {1}. \n"
                       "In this experiment the values for time and intensity at the first injection,\n"
                       "where {2} and {3} respectively.\n\n".format(currTime1, par.name, par.dataStartTime,
                                                                    par.dataStartIntensity))
            file.write("****************************************************************************************\n")
            file.write('Date\t\tsample name\t\tdifference\t I/I0\n')
    else:
        with open(filename, 'a') as file:
            file.write('{}\t{}\t\t\t\t{}\t\t{}\n'.format(currTime2, sampleName, slopeDiff, intData))

def WriteToDatabase(par, partitionedInt):
    # create database handler class

    databaseCommander = DatabaseHandler(par.databaseName)

    for i in range(par.experimentNumber):
        if par.namesExperiments[i] == 'Solvent' or par.namesExperiments[i] == 'solvent' or par.namesExperiments[i] == 'SOLVENT':
            continue
        else:
            # Date, Name, ID_Cat, Number_experiments, I0, t0,
            # Position, Name_sample, Quenching_code, Peak_data)
            data = (par.date, par.name, par.catalystName,
                    str(par.experimentNumber), par.dataStartIntensity,
                    par.dataStartTime, par.namesPositions[i],
                    par.namesExperiments[i], par.colorCodes[i],
                    str(partitionedInt[i]))

            databaseCommander.InsertAutomationExperiment(data)

def CopyAvasoftFile(fileName, targetFolder):
    try:
        shutil.copy2(fileName, targetFolder)
        # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
        # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

def CreateOvervieuwPDF(par, originalPDF):
    """
    Create the overvieuw pdf with legend on the next page
    :param par:
    :param originalPDF:
    :return:
    """

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet)

    # write the legend to a separate file
    y = 800
    for line in range(len(par.legend)):
        can.drawString(40, y, par.legend[line])
        y -= 15
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existingFile = open(originalPDF, 'rb')
    existing_pdf = PdfFileReader(existingFile)
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    output.addPage(page)
    output.addPage(new_pdf.getPage(0))
    # finally, write "output" to a real file
    outputStream = open("overview and legend.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

if __name__ == '__main__':
    par = ImportparAuto()
    par.name = "KK-20180228-1"
    par.nameFileAvasoft = "{}{}".format(par.name, '.txt')
    par.dataStartTime = 144.951
    par.dataStartIntensity = 1587804.3769
    par.experimentNumber = 6

    par.mainRunParcing = False
    par.selfNaming = False
    par.databaseName = "Database_Automation.db"

    curTime = datetime.datetime.now()
    par.date = curTime.strftime('%Y/%m/%d')
    par.catalystName = '4CzIPN'

    par.scriptDir = os.getcwd()
    par.dataDir = os.path.join(par.scriptDir, 'Data_Automation')
    par.workingDir = os.path.join(par.dataDir, par.name)
    ST.make_sure_path_exists(par.workingDir)

    par.namesExperiments = [None] * par.experimentNumber
    par.namesPositions = [None] * par.experimentNumber
    par.colorCodes = [None] * par.experimentNumber
    par.legend = [None] * par.experimentNumber
    for i in range(len(par.namesExperiments)):
        letter = int(i / 8) + 65
        position = (i % 8) + 1
        par.namesExperiments[i] = '{}{}'.format(chr(letter), str(position))
        par.namesPositions[i] = '{}{}'.format(chr(letter), str(position))
        par.legend[i] = '{} = {}'.format(par.namesPositions[i], par.namesExperiments[i])

    ParceData(par)