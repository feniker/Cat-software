# Loading data from root-archives
import sys
import numpy as np
sys.path.append("/usr/lib64/python3.6/site-packages")
import ROOT as RT
sys.path.remove("/usr/lib64/python3.6/site-packages")
RT.gInterpreter.ProcessLine('#include "/usr/include/dasarchive/service.h"')
RT.gSystem.Load('libDASArchive.so')

from Utils import Timer
import Utils
import matplotlib.pyplot as plt
    
def getLastShot(archiveFile):
    shots = [int(key.GetName()) for key in archiveFile.GetListOfKeys() if key.GetName().isdigit()]
    return max(shots)

def getKeyNames(archiveFile):
    return [key.GetName() for key in archiveFile.GetListOfKeys()]

def loadSignal(archiveName, kustName, signalName, shot):
    """ This script works with unpacking root-archives.
        it takes one signal and transfroms it to numpy array \n
        This method is faster np.array(THist) \n
        Input: archiveName, kustName, signalName, shot \n
        Output: (data, dt, timeShift)
        ## ATTENTION!
        DATA FORMAT is "unsigned short int"
    """
    try:
        shotnum = int(shot)
        RT.OpenArchive(archiveName)
        
        if shotnum <= 0:
            shotnum = shotnum + RT.GetLastShot()

        s = RT.GetSignal(signalName, kustName, shotnum)
        size = s.GetSize() # длина сигнала
        timeShift = s.GetXShift()/1e6 # time shift in s
        # Важно!
        # DATA FORMAT IS "unsigned short int"
        data = s.GetYQuant() * np.frombuffer(s.GetArray(), np.uint16, size) + s.GetYShift()
        dt = s.GetXQuant()/1e6
        RT.CloseArchive()
        return (data, dt, timeShift, shotnum)
    except:
        print(f"Failure reading {archiveName}/{kustName}/{signalName} !")
        return None
    
def loadSignalBySteps(archiveName, kustName, signalName, shot):
    """ This script works with unpacking root-archives.
        it takes one signal and transfroms it to numpy array \n
        This method is faster np.array(THist) \n
        Input: archiveName, kueditor.renderIndentGuidestName, signalName, shot \n
        Output: (data, dt, timeShift)
        ## ATTENTION!
        DATA FORMAT is "unsigned short int"
    """
    shotnum = int(shot)
    # try to open archive
    try:
        archiveFile = RT.TFile.Open(archiveName)
    except OSError:
        print(f"INCORRECT name of archive file '{archiveName}'")
        print(f"You can use example: '/CAT/work_2023.root'")
        return None
    # choose shot
    if shotnum <= 0:
        shotnum = shotnum + getLastShot(archiveFile)
    archiveShot = archiveFile.Get(str(shotnum))
    if not archiveShot:
        print(f"INCORRECT number of archive shot '{shotnum}', The last shot is {getLastShot(archiveFile)}")
        return None
    # choose kust
    archiveKust = archiveShot.Get(kustName)
    if not archiveKust:
        print(f"INCORRECT kustname of archive shot '{kustName}'")
        print(f"The kust List of shot {shotnum}: {getKeyNames(archiveShot)}")
        return None
    # choose signal(leaf)
    archiveLeaf = archiveKust.Get(signalName)
    if not archiveLeaf:
        print(f"INCORRECT signalName of archive shot '{signalName}'")
        print(f"The kust List of shot {shotnum}/{kustName}: {getKeyNames(archiveKust)}")
        return None
    # get signal
    s = archiveLeaf
    size = s.GetSize() # длина сигнала
    timeShift = s.GetXShift()/1e6 # time shift in s
    # Важно!
    # DATA FORMAT IS "unsigned short int"
    data = s.GetYQuant() * np.frombuffer(s.GetArray(), np.uint16, size) + s.GetYShift()
    dt = s.GetXQuant()/1e6
    return (data, dt, timeShift, shotnum) 
    
def loadLeafs(archiveName, names = {"Vacuum": ["neCenterProbe", "TeCenterProbe"]}, shot = 0):
    dataSet = []
    for kust, leafs in names.items():
        for leaf in leafs:
            # print(kust, leaf)
            try:
                data, dt, timeShift, shotnum = loadSignalBySteps(archiveName, kust, leaf, shot)
            except TypeError:
                print(f"Can't read {kust}/{leaf}")
                continue
            timeline = np.linspace(timeShift, timeShift + dt*data.shape[0], data.shape[0])
            dataSet.append([timeline, data * Utils.koef.get(leaf, 1), f"{kust}/{leaf}"])
    return dataSet

if __name__=="__main__":
    archiveName = "/CAT/work_2023.root"
    kustName = "Vacuum"
    signalName = "neProbePG"
    shot =  873
    with Timer() as timer:
        dataSet = loadLeafs(archiveName, {"Vacuum": ["CathodePG", "AnodePG", "TeProbePG", \
            "neProbePG", "TeProbeMirror", "neProbeMirror", "TeProbeCenter", "neProbeCenter"]})
    potentials = ["R000R025", "R025R070", "R070R103", "R103R136", "R136R170", "R170R203", \
            "R203R236", "R236R269", "R269R303", "R303R336", "R336R368", "R368R402", \
            "Vacuum_cell", "Ground"]
    magneticProbes = ["MirnovProbe" + str(i) for i in range(1,13)]
    with Timer() as timer:
        dataSet = loadLeafs(archiveName, {"PlasmaDump": magneticProbes + potentials})
    for i in range (20):
        plt.plot(dataSet[i][0], dataSet[i][1], label = dataSet[i][2])
    plt.legend(loc='upper left')
    plt.show()
    # data = loadSignalBySteps(archiveName, kustName, signalName, shot)