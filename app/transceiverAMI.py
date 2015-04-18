from pkgTransceiver.implementation.pkgTransceiver import Transceiver

def createTransceiverObject(missionControlOAuthID, transceiverOAuthToken, antennaPorts):
    if (missionControlOAuthID+":"+transceiverOAuthToken) == "intendant:0123456789ABCDEF":
        print ("Intendant -||- Transceiver : Successfully Authenticated")
        return Transceiver(antennaPorts[0], antennaPorts[1], antennaPorts[2])
    else:
        print ("Intendant -|x|- Transceiver : Authentication Failure!")

    