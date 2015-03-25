# This is an example of how to connect to and use the Bitmessage API.
# See https://bitmessage.org/wiki/API_Reference

import xmlrpclib
import unittest
import json


class TestFuncionality(unittest.TestCase):
    # ---------- Buffers ----------
    global api
    

    # ---------- Setup ----------
    # Needs the BitMessage Service to already has been started, maybe in a command-line tool
    # Connecting to the BitMessage Service
    api = xmlrpclib.ServerProxy("http://assistanceMaster:friendsAreFamily@localhost:8442/")

    def test_API(self):
        #print 'Testing the avaliability of the API.'
        inputstr1 = "hello"
        inputstr2 = "world"
        self.assertEqual(api.helloWorld(inputstr1, inputstr2), "hello-world")
        self.assertEqual(api.add(2,3), 5)
        

    def test_SendAck(self):
        #print 'Sending a message.'
        subject = 'subject!'.encode('base64')
        message = 'Hello, this is the message'.encode('base64')
        ackData = api.sendMessage('BM-2cVt4x98T4NT2Ews9CBGQmbf9diS84Mhof', 'BM-2cUBjVpVq3vv1VJBgPr1eyk9r3yc1SKVxL', subject,message)
        #print 'The ackData is:', ackData
        ackData = api.sendMessage('BM-2cUBjVpVq3vv1VJBgPr1eyk9r3yc1SKVxL', 'BM-2cVt4x98T4NT2Ews9CBGQmbf9diS84Mhof', subject,message)
        #print 'The second ackData is:', ackData
        #print 'deleting the second message'
        api.trashSentMessageByAckData(ackData)

        
        
    def test_MyAddresses(self):
        #print 'Getting One of My Addresses.'
        myAddresses = json.loads(api.listAddresses())['addresses']
        self.assertEqual(myAddresses[0]['address'], "BM-2cVt4x98T4NT2Ews9CBGQmbf9diS84Mhof")
        self.assertEqual(myAddresses[1]['address'], "BM-2cUBjVpVq3vv1VJBgPr1eyk9r3yc1SKVxL")
        # creating more addresses
        addressLabel = 'even new address label'.encode('base64')
        api.createRandomAddress(addressLabel,False,0.0001,0.0001)
        addressLabel = 'another new address label'.encode('base64')
        api.createRandomAddress(addressLabel,False,0.0001,0.0001)
        #deleting the newly created addresses
        myAddresses = json.loads(api.listAddresses())['addresses']
        numOfAdrs = len(myAddresses)
        #print numOfAdrs
        for currentAdrsNum in range(2,numOfAdrs):
            api.deleteAddress(myAddresses[currentAdrsNum]['address'])
        #verifying the final number of addresses 
        myAddresses = json.loads(api.listAddresses())['addresses']
        numOfAdrs = len(myAddresses)
        #print numOfAdrs
        self.assertEqual(numOfAdrs, 2)
        
        
    def test_Inbox(self):
        #print 'Number of Messages on My Inbox, and the message:'
        myInbox = json.loads(api.getAllInboxMessages())['inboxMessages']
        #print len(myInbox)
        #print myInbox
        #print ""
        
        
    def test_ThrasAllMsgs(self):
        #print 'Number of Messages on My Inbox before: '
        myInboxIDs = json.loads(api.getAllInboxMessageIDs())['inboxMessageIds']
        numOfMsgs = len(myInboxIDs)
        #print numOfMsgs
        for currentMsgNum in range(0, numOfMsgs):
            api.trashMessage(myInboxIDs[currentMsgNum]['msgid'])
        #print 'Number of Messages on My Inbox after: '
        myInboxIDs = json.loads(api.getAllInboxMessageIDs())['inboxMessageIds']
        #print len(myInboxIDs)
        self.assertEqual(len(myInboxIDs), 0)


if __name__ == '__main__':
    unittest.main()