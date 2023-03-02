# python : version 3.11.2

import os
import re
import sys
from pathlib import Path

DEBUG = False
DEBUG_REGEX = False

VERSION = '1.0'

## File path of DCM
DCM_FILE = 'C:\ETKRData\Workspace\VSC\TouchDCM\dcm\dcm_test_01.DCM'
BAK_EXT = '.bak'

## Regular expression for variables
VAL_EXP = '[a-zA-Z_][a-zA-Z0-9_.]{1,62}'    # Max length 63
## Regular expression for number
NUM_EXP = '[1-9][0-9]{0,4}'                 # Max length 5

## Regular expression for elements
REGEX_PARAMETER = '^FESTWERT\s'+VAL_EXP+'\s?$'
REGEX_ARRAY = '^FESTWERTEBLOCK\s'+VAL_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_MATRIX = '^FESTWERTEBLOCK\s'+VAL_EXP+'\s'+NUM_EXP+'\s@\s'+NUM_EXP+'\s?$'
REGEX_CHAR_LINE = '^KENNLINIE\s'+VAL_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_CHAR_MAP = '^KENNFELD\s'+VAL_EXP+'\s'+NUM_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_FIXED_CHAR_LINE = '^FESTKENNLINIE\s'+VAL_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_FIXED_CHAR_MAP = '^FESTKENNFELD\s'+VAL_EXP+'\s'+NUM_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_GROUP_CHAR_LINE = '^GRUPPENKENNLINIE\s'+VAL_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_GROUP_CHAR_MAP = '^GRUPPENKENNFELD\s'+VAL_EXP+'\s'+NUM_EXP+'\s'+NUM_EXP+'\s?$'
REGEX_DISTRIBUTION = '^STUETZSTELLENVERTEILUNG\s'+VAL_EXP+'\s'+NUM_EXP+'\s?$'

regex_element_array = {REGEX_PARAMETER, REGEX_ARRAY, REGEX_MATRIX, \
                REGEX_CHAR_LINE, REGEX_CHAR_MAP, \
                REGEX_FIXED_CHAR_LINE, REGEX_FIXED_CHAR_MAP, \
                REGEX_GROUP_CHAR_LINE, REGEX_GROUP_CHAR_MAP, \
                REGEX_DISTRIBUTION }

## Check regular expression for elements
if DEBUG_REGEX == True:
    for element in regex_element_array:
        print(element)

###############################################################
## FUNCTION : prep
##  - Argument 1    : None
##  - Return        : None
###############################################################
def prep(sysArgs):
    # Check input arguments
    # - arg 1 : python file (*.py)
    # - arg 2 : [required] dcm file path
    # - arg 3 : [optional] debug (d or D)
    
    global DEBUG
    global DCM_FILE
    global VERSION
    
    if DEBUG == True:
        i = 0
        for arg in sysArgs:
            print('arg' + str(i) + ' : ' + arg)
            i += 1
    
    # [required] dcm file path
    if (len(sysArgs) < 2) or (os.path.isfile(sysArgs[1]) != True):
        print('Add the FUNKTION name to the end of the element name in the DCM file.')
        print('  Version : V' + VERSION)
        print('  Usage   : touch_dcm.exe [path]')
        print('    ex)   : touch_dcm.exe C:\data.dcm')
        print('    [path]  dcm file path')
        sys.exit()
    else:
        DCM_FILE = sysArgs[1]

    if DEBUG == True:    
        print('DCM_FILE : ' + DCM_FILE)

    # [optional] debug
    if (len(sysArgs) >= 3) and (sysArgs[2].lower() == 'd'):
        DEBUG = True
        

###############################################################
## FUNCTION : readDCMFile
##  - Argument 1    : DCM file path
##  - Return        : Dictionary {Key:matching element, Value:Function}
###############################################################
def readDCMFile(path_dcm):
    dicData = dict = {}     # dictionary {Key:matching element, Value:Function}

    try:
        with open(path_dcm, mode = 'r') as dcm:
            find_element = True     # toggle for searching
            element = ''
            lines = dcm.readlines()
            for line in lines:      # Read lines of entire document
                if DEBUG == True:
                    print(line)
                if find_element == True:    # Search element
                    element = ''
                    for element in regex_element_array:
                        if re.compile(element).match(line):
                            if DEBUG == True:
                                print('[readDCMFile] REGEX matched element : ' + element)
                                print('[readDCMFile] REGEX matched line : ' + line)
                            find_element = False
                            element = line
                            break
                else:                       # Search 'FUNKTION' in element section
                    if 'FUNKTION' in line:
                        temp = line.split()
                        if DEBUG == True:
                            print('[readDCMFile] FUNKTION : ' + line)
                        dicData[element] = temp[1]
                        if DEBUG == True:
                            print('[readDCMFile] FUNKTION : key : ' + element)
                            print('[readDCMFile] FUNKTION : value : ' + temp[1])
                        find_element = True
                    elif line == 'END':
                        find_element = True
            dcm.close()
        return dicData
    except Exception as e:
        print('[readDCMFile] Exception : ' + e)


###############################################################
## FUNCTION : backupFile
##  - Argument 1    : source file path
##  - Return        : None
###############################################################
def backupFile(src):
    dst = src + BAK_EXT
    try:
        with open(src, mode = 'r') as srcFile:
            srcLines = srcFile.readlines()
            if DEBUG == True:
                print('[backupFile] src : ' + src)
            srcFile.close()
        with open(dst, mode = 'w') as dstFile:
            dstFile.writelines(srcLines)
            if DEBUG == True:
                print('[backupFile] dst : ' + dst)
            dstFile.close()
    except Exception as e:
        print('[backupFile] Exception : ' + e)


###############################################################
## FUNCTION : writeDCMFile
##  - Argument 1    : DCM file path
##  - Argument 2    : Dictionary {Key:matching element, Value:Function}
##  - Return        : None
###############################################################
def writeDCMFile(path_dcm, dicData):
    # new name for dcm file
    path_dcm_new = path_dcm
    p = Path(path_dcm_new)
    ext = p.suffix
    path_dcm_new = path_dcm_new.removesuffix(ext)
    path_dcm_new = path_dcm_new + '_NEW' + ext
    if DEBUG == True:
        print('[writeDCMFile] path_dcm_new : ' + path_dcm_new)

    try:
        # read dcm file
        with open(path_dcm, mode = 'r') as dcm:
            dcmLines = dcm.readlines()
            dcm.close()
        # write new dcm file
        with open(path_dcm_new, mode = 'w') as new_dcm:
            for dcmLine in dcmLines:      # Read lines of entire document
                for element in regex_element_array:
                    if re.compile(element).match(dcmLine):
                        if DEBUG == True:
                            print('[writeDCMFile] REGEX matched element : ' + element)
                            print('[writeDCMFile] REGEX matched line : ' + dcmLine)
                        temp = dcmLine.split()
                        if '.'+ dicData[dcmLine] not in temp[1]:                             
                            temp[1] = temp[1] + '.' + dicData[dcmLine]  # Add FUNKTION name to variable name
                            sep = ' '                                   # Combining temp array with space(' ')
                            dcmLine = sep.join(temp) + '\n'             # Insert newline character
                            if DEBUG == True:
                                print('[writeDCMFile] dcmLine : ' + dcmLine)
                            break
                new_dcm.write(dcmLine)
            new_dcm.close()
            if os.path.isfile(path_dcm_new):
                print('Done!')
                print('Check the created DCM file. [' + path_dcm_new + ']')
    except Exception as e:
        print('[writeDCMFile] Exception : ' + e)


###############################################################

# preparation
prep(sys.argv)
# read DCM file
dicData = readDCMFile(DCM_FILE)
# write DCM file
writeDCMFile(DCM_FILE, dicData)

