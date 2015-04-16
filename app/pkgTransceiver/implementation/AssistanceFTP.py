import socket, hashlib, urllib
from pkgTransceiver.implementation.PyBitTorrent import bencode, torrent
from cpnLibrary.implementation.Constants import *
from pkgOfficer.implementation import TaskDescription
import base64


def makeTorrentFiles(taskDescription):
    trackers = [str(socket.gethostbyname(socket.gethostname()))+':'+str(PORT_FTP)]
    cmnt = "Assistance Torrent File by Token "+TOKEN_TESTS_VERSION
    torrent.write_torrent_file(torrent = taskDescription.STDOUT+'.torrent', file = taskDescription.STDOUT, tracker = trackers, comment = cmnt)
    torrent.write_torrent_file(torrent = taskDescription.STDERR+'.torrent', file = taskDescription.STDOUT, tracker = trackers, comment = cmnt)
    return taskDescription.STDOUT+'.torrent', taskDescription.STDERR+'.torrent'


def assistanceMagnet(torrentData):
    metadata = bencode.decode(torrentData)
    hashContents = bencode.encode(metadata['info'])
    hashDigest = hashlib.sha1(hashContents).digest()
    uriMeta={"xt": "urn:btih:"+base64.b32encode(hashDigest), "dn": metadata['info']['name'], "tr": metadata['announce'], "xl": metadata['info']['length']}
    return ("magnet:?"+urllib.urlencode(uriMeta)).replace('%2F','/').replace('%3A', ':')
    

def makeMagnets(taskDescription):
    stdout, stderr = makeTorrentFiles(taskDescription)
    stdoutMagnet = assistanceMagnet(open(stdout, 'r').read())
    stderrMagnet = assistanceMagnet(open(stderr, 'r').read())
    return stderrMagnet, stderrMagnet