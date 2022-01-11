from Millify import millify
class Column:
    def __init__(self, keyName, niceName, formatType="string"):
        self.keyName = keyName 
        self.niceName = niceName
        self.formatType = formatType
        
    def format(self, data):
        try:
            if self.formatType == "test":
                return f"{data}mmm"
            elif self.formatType == "millify":
                return millify(data)
            return data
            
        except Exception as e:
            print("Exception formatting data")
            print(e)
            print(data)
            
            return "null"