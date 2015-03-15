
import SocketServer
from pkgTransceiver.implementation import Transceiver


class AssistanceTransceiverProgramServer(SocketServer.StreamRequestHandler):
  
    def handle(self):
        # security
        self.authToken = self.rfile.readline().strip()
        if not Transceiver.authenticate(self.authToken):
            raise ValueError("Security Alert! A client tryed to connect to a Assistance Socket without the proper Authentication Token!")    
        # getting the data
        self.data = self.rfile.readline().strip()
        # processing the data
        print "processing the data"
        self.data = str(self.data).upper()
        # writeback
        self.wfile.write(self.data)