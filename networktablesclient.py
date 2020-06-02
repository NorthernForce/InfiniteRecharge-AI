import sys, time, logging
from networktables import NetworkTables

class NetworkTablesClient:
    def __init__(self):
        self.ConnectToServerWithChecks()
        sdtable = self.GetTableFromServer()
        self.SetLocalTable(sdtable)
        self.SendValuePair("PC Offset in AI Cam:", 9999)

    def SendValuePair(self, key, value):
        self.localTable.putNumber(key, value)

    def SendValueArray(self, key, valueArray):
        self.localTable.putNumberArray(key, valueArray)
        
    def GetValueFrom(self, key):
        value = self.localTable.getNumber(key, 0)
        return value
        
    def SetLocalTable(self, table):
        self.localTable = table
        
    def GetTableFromServer(self, table="SmartDashboard"):
        table = NetworkTables.getTable(table)
        return table
    
    def ConnectToServerWithChecks(self):
        self.__SetServerAddress()
        self.__SetupLogging()
        NetworkTables.initialize(server=self.robotIP)
    
    def __SetServerAddress(self, ipAddress= "10.1.72.2"):  # change to ip of robot
        self.robotIP = ipAddress
    
    def __SetupLogging(self):
        logging.basicConfig(level=logging.DEBUG)
    
    localTable = GetTableFromServer("SmartDashboard")
    robotIP = "10.1.72.2"
