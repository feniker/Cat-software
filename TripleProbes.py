from Load_ROOT import loadLeafs
import Utils
import numpy as np
import matplotlib.pyplot as plt

def fromEvToErg(Te):
    return Te * 1.6 * 10 ** -12

def fromAmpToStatAmp(I):
    return I * 3 * 10 ** 9

def temper(u23, ):
    Te = Utils.Ufactor * u23 / np.log(2)  # eV electron temperature
    Te -= np.mean(Te[-2000:])
    return Te

def elDen(I, Te):
	# cutting off all temperature less than 1/30 of max
	Te = np.abs(Te)
	epsilon = np.max(Te[Te.nonzero()])/30
	Te[Te < epsilon] = epsilon
	Te = fromEvToErg(Te)
	ne = Utils.Ifactor * fromAmpToStatAmp(I) * np.exp(0.5) / Utils.S \
        / Utils.e * np.sqrt(2 * Utils.Mp / Te)  # sm-3 electron density
	return ne

def getTeDen(TeRaw, neRaw):
    Te = temper(TeRaw)
    ne = -elDen(neRaw, Te)
    ne = ne - np.mean(ne[-2000:])
    return (Te, ne)


def getTriple(archiveName, shot = 0, tStart = -1e-3, tFinish = 6e-3):
    names = {"Vacuum": ["TeProbeAbsorber", "neProbeAbsorber", "TeProbeMirror",\
             "neProbeMirror", "TeProbeCone", "neProbeCone"]}
    dataSet = loadLeafs(archiveName, names, shot)
    timeline = dataSet[0][0][:-1] # delete last element because of elDen
    N1 = Utils.timeToInd(tStart, timeline[0], timeline[-1], len(timeline))
    N2 = Utils.timeToInd(tFinish, timeline[0], timeline[-1], len(timeline))    
    TePG, nePG = getTeDen(dataSet[0][1], dataSet[1][1]) # size ne more
    TeMirror, neMirror = getTeDen(dataSet[2][1], dataSet[3][1])
    TeCenter, neCenter = getTeDen(dataSet[4][1], dataSet[5][1]) 
    return (timeline[N1:N2], TePG[N1:N2], nePG[N1:N2], TeMirror[N1:N2], 
         neMirror[N1:N2], TeCenter[N1:N2], neCenter[N1:N2]) 

if __name__=="__main__":
    archiveName = "/CAT/1945_work_2024.root"
    timeline, TePG, nePG, TeMir, neMir, TeCen, neCen = getTriple(archiveName)
    plt.plot(timeline, TePG)
    plt.plot(timeline, TeMir)
    plt.plot(timeline, TeCen)
    plt.show()