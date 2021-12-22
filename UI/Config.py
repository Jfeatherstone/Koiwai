import sys
import os

# Here are all of the default settings, which is also the
# list of settings that be set in the config file
settings = {
    "showHiddenFiles": False,
    "showNonImageFiles": True,
    "imageFileTypes": ['jpg', 'png'],
    "configFileFolder": '~/.config/Koiwai',
    "configFileName": 'koiwai.conf',
           }

def loadConfigFile():
    # Join to handle missing/included '/' at end of folder
    configFilePath = os.path.join(settings["configFileFolder"], settings["configFileName"])

    # Open the file itself
    if not os.path.exists(configFilePath):
        print(f'Provided config file ({configFilePath}) does not exist!')
        return

    lines = None

    with open(configFilePath, 'r') as confFile:
        lines = confFile.readlines()

    if lines is not None:
        # First three lines can be ignored as they are:
        lines = lines[3:]


def writeConfigFile():
    # Join to handle missing/included '/' at end of folder
    configFilePath = os.path.join(settings["configFileFolder"], settings["configFileName"])

    # Make sure the directory exists
    if not os.path.exists(settings["configFileFolder"]):
        os.mkdir(settings["configFileFolder"])

    # We write into a temp file and then copy over afterwards
    # (so if something goes wrong, we don't lose all of our data/settings)
    tempFilePath = configFilePath + ".tmp"

    # The header
    lines = ['####################',
             ' KOIWAI CONFIG FILE ',
             '####################']

    # Now copy down each setting
    for k,v in settings.items():
        lines.append(f'{k}={v}')


    # Open the file itself
    with open(tempFilePath, 'w') as confFile:
        confFile.writelines(lines)

