import os
import math
import time
from PIL import ImageGrab
import smtplib
import logging
import errno
import shutil

def OverNightCommand(par):
    logger = logging.getLogger('AutosamplerLog')
    logger.info('The overnight function has been activated.')
    # make a print screen and save that in the data folder
    saveDirectory = par.dataDir
    img = ImageGrab.grab()
    logger.debug('A screenshot is made.')
    saveas = os.path.join(saveDirectory, 'ScreenShot_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.jpg')
    img.save(saveas)
    logger.debug('The image is saved at location: {0} \nWith name :{1} '.format(saveDirectory, ('ScreenShot_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.jpg')))

    # stop the pumps
    # logger.debug('In function overnightCommand the pumps are told to stop.')

    # shut down the pc
    logger.debug('System will now be shut down.')
    try:
        os.system("shutdown -t 0 -f")
    except:
        logger.error('System was unable to shut down.', exc_info=True)

def SendEmail(par):
    logger = logging.getLogger('AutosamplerLog')
    logger.info('Function SendEmail was called.')

    receiver = par.email
    logger.debug('receiver is: {}'.format(receiver))

    subject = "Autosampler {}".format(par.quencherName)
    logger.debug('The subject is: {}'.format(subject))

    message = 'The Autosampler experiment of {0} is finished and can be viewed in the file {1}.'\
        .format(time.strftime('%Y_%m_%d'), par.nameExcelFile)
    text = ('Hello, \n\n' + message + '\n\nKoen, Koen & Niels')

    # Gmail Sign In
    gmail_sender = "noelresearchgroup.automation@gmail.com"
    gmail_passwd = "K2automation"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_sender, gmail_passwd)
    logger.info('A server has been set up with Gmail account details')

    BODY = '\r\n'.join(['To: %s' % receiver,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % subject,
                        '', text])

    try:
        server.sendmail(gmail_sender, [receiver], BODY)
        logger.debug('The Email has been send.')
    except:
        logger.error('A error occurred sending the email.', exc_info=True)

    logger.debug('Destroying server object.')
    server.quit()

def Pauser(pauseTime):
    numberDevider = math.modf(pauseTime)
    decimalPart = numberDevider[0]
    intergerPart = int(numberDevider[1])
    time.sleep(decimalPart)
    for i in range(0, (10 * intergerPart)):
        time.sleep(0.1)

def CalculatePausetime(startTime, resTimeDv):
    pause1 = time.time() - startTime
    pause2 = resTimeDv - pause1
    if pause2 > 0:
        pauseTime = pause2
    else:
        pauseTime = 0.0

    return pauseTime

def make_sure_path_exists(path):
    # this function checks if a folder exists and otherwise make it.
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def CopyAvasoftFile(fileLocation, targetFolder):
    try:
        shutil.copy2(fileLocation, targetFolder)
        # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
        # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

def waitingThread(pauzetime):
    time.sleep(pauzetime)
    pass