######################################################################################################
# @file DataDemo_Callback.py
# @copyright HighFinesse GmbH.
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#

# wlmData.dll related imports
import wlmData
import wlmConst
import ctypes, time

# others
import sys

#########################################################
# Set the DLL_PATH variable according to your environment
#########################################################
DLL_PATH = "./wlmData.dll" # If you are using a wavemeter connected via USB: no need to change anything.
#If you are using a wavemeter connected via Ethernet: Put this script in the same path where you put the wlmData.dll
#DLL_PATH = "libwlmData.so" # Uncomment this to use the Linux NetAccess client instead

# Load DLL from DLL_PATH

try:
    wlmData.LoadDLL(DLL_PATH)
    print('ok')
except:
    sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % DLL_PATH)

# Checks the number of WLM server instance(s)
if wlmData.dll.GetWLMCount(0) == 0:
    print("There is no running wlmServer instance(s).")
else:
    # Read type, version, revision and build number
    Version_type = wlmData.dll.GetWLMVersion(0)
    Version_ver = wlmData.dll.GetWLMVersion(1)
    Version_rev = wlmData.dll.GetWLMVersion(2)
    Version_build = wlmData.dll.GetWLMVersion(3)
    print("WLM Version: [%s.%s.%s.%s]" % (Version_type, Version_ver, Version_rev, Version_build))

    # Specify number of measurements that you would like to print
    num_m = 100
    n = 0

    # Set up callback mechanism
    def callback(Mode, IntVal, DblVal):
        global num_m, n,wlmData
        if Mode == wlmConst.cmiWavelength1:
            print("Wavelength result: {:.6f}".format(DblVal))
            n = n + 1
            
    callbacktype = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_int32, ctypes.c_double)
    callbackpointer = callbacktype(callback)
    wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallback, callbackpointer, 0)

    # Wait for events (wavelength) until the number of triggers is reached
    while n < num_m:
        time.sleep(1)
    
    wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)
    print('Done')