from Queue import Queue, Empty
import threading, time, traceback
from PyQt4.QtCore import QEvent, QCoreApplication

class CustomEvent(QEvent):
    _data = None
    def __init__(self, typ, data):
        QEvent.__init__(self, typ)
        self._data = data    
    def data(self):
        return self._data

class CommsThread(object):

    def __init__(self, parent):
        self.parent = parent
        self.CSNum = 1
        self.gen = None
        self.resultQueue = Queue()     # a queue object that stores the results of each polling update        
        self.inputQueue = Queue()    # a queue object that stores things to do
        self.updateReadyEvent = None        
        # Flags controlling polling of axis position/velocity/following error
        self.disablePollingStatus = False
        self.updateThreadHandle = threading.Thread(target = self.updateThread)
        self.updateThreadHandle.start()

    def sendTick(self, lineNumber, err):
        # Post a Qt event with current progress data
        ev = CustomEvent( self.parent.progressEventType, (lineNumber, err))
        QCoreApplication.postEvent( self.parent, ev )  

    def sendComplete(self, message):
        self.gen = None    
        evDone = CustomEvent( self.parent.downloadDoneEventType, message)
        QCoreApplication.postEvent(self.parent, evDone )          

    # Thread that sends the PMAC command to retrieve status, position, velocity and following error for each motor.
    # The thread then puts the retrieved data on a queue which is read by the gui.
    def updateThread(self):
        die = False
        while die is not True:
            try:
                die = self.updateFunc()
            except:
                traceback.print_exc()
                continue    
            
    def updateFunc(self):
        try:
            # see if the gui wants us to do anything
            cmd, data = self.inputQueue.get(block = False)
        except Empty:
            # nope, nothing to do
            pass
        else:
            # work out what it wants us to do
            if cmd == "die":
                return True          
            elif cmd == "sendSeries":
                try:
                    self.gen = self.parent.pmac.sendSeries(data)
                except:
                    self.sendComplete("Couldn't start download")                    
                    traceback.print_exc()
            elif cmd == "disablePollingStatus":
                self.disablePollingStatus = data
            elif cmd == "cancelSendSeries":
                if self.gen:
                    self.gen.close()
                    self.sendComplete("Download cancelled by the user")
            else:
                print "WARNING: don't know what to do with cmd %s" % cmd
        if self.disablePollingStatus:
            return
        if self.parent.pmac is None or not self.parent.pmac.isConnectionOpen:
            return
        if self.gen:
            # should be downloading a text file
            try:
                wasSuccessful, self.lineNumber, command, pmacResponseStr = self.gen.next()
            except StopIteration:
                self.sendComplete("Downloaded "+str(self.lineNumber)+" lines from pmc file.")                      
            else:
                err = ""
                if not wasSuccessful:
                    err = "%s: command '%s' generated '%s'" %(self.lineNumber, command, pmacResponseStr.replace("\r", " ").replace("\x07", ""))
                self.sendTick(self.lineNumber, err)
                time.sleep(0.1)          
            return
            
        cmd = "i65???&%s??%%"
        axes = self.parent.pmac.getNumberOfAxes() + 1
        for motorNo in range(1, axes):
            cmd = cmd +  "#" + str(motorNo) + "?PVF"                
        (returnStr, wasSuccessful) = self.parent.pmac.sendCommand(cmd%self.CSNum)
        if wasSuccessful:
            valueList = returnStr.rstrip("\x06\r").split('\r')
            # fourth is the PMAC identity
            if valueList[0].startswith("\x07"):
                # error, probably in buffer
                print "i65 returned %s, sending CLOSE command" % valueList[0].__repr__()
                self.parent.pmac.sendCommand("CLOSE") 
                return
            self.resultQueue.put([valueList[0], 0, 0, 0, "IDENT"])                                
            # first value is global status
            self.resultQueue.put([valueList[1], 0, 0, 0, "G"])
            # second value is the CS
            self.resultQueue.put([valueList[2], 0, 0, 0, "CS%s" % self.CSNum])
            # third is feedrate
            self.resultQueue.put([valueList[3], 0, 0, 0, "FEED%s" % self.CSNum])                
            valueList = valueList[4:]
            cols = 4
            for motorRow, i in enumerate(range(0, len(valueList), cols)):
                returnList = valueList[i:i+cols]
                returnList.append(motorRow)
                self.resultQueue.put( returnList, False)
            evUpdatesReady = CustomEvent(self.parent.updatesReadyEventType, None )
            QCoreApplication.postEvent( self.parent, evUpdatesReady )
            time.sleep(0.1)
        else:
            print 'WARNING: Error while sending update request ("%s")' % returnStr

