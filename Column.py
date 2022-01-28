from Millify import millify

import datetime
class Column:
    def __init__(self, keyName, niceName, formatType="string"):
        self.keyName = keyName 
        self.niceName = niceName
        self.formatType = formatType
        
    def format(self, data):
        try:
            if self.formatType == "test":
                return f"{data}mmm"
            elif self.formatType == "millifyLarge":
                return millify(data)
            elif self.formatType == "millifyPercentage":
                return f"{millify(data * 100, precision=2)}%"
            elif self.formatType == "epochToDate":
                currDate = datetime.datetime.fromtimestamp(data)
                
                return currDate.strftime("%d/%m/%Y")
                
            return data
            
        except Exception as e:
            print("Exception formatting data")
            print(e)
            print(data)
            
            return "null"