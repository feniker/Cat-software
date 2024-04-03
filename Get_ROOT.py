from Load_ROOT import loadSignal
import matplotlib.pyplot as plt
import numpy as np
from Utils import Timer
import Utils


def loadLeafs(archiveName, names = {"Vacuum": ["neCenterProbe", "TeCenterProbe"]}, shot = 0):
    dataSet = []
    for kust, leafs in names.items():
        for leaf in leafs:
            # print(kust, leaf)
            try:
                data, dt, timeShift = loadSignal(archiveName, kust, leaf, shot)
            except TypeError:
                print("Can't read archive")
            timeline = np.linspace(timeShift, timeShift + dt*data.shape[0], data.shape[0])
            dataSet.append([timeline, data * Utils.koef.get(leaf, 1), f"{kust}/{leaf}"])
    return dataSet

if __name__=="__main__":
    archiveName = "/CAT/work_2023.root"
    kustName = "Vacuum"
    signalName = "neProbePG"
    shot = 0
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