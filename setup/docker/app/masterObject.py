import json


class MasterObject:
    types = {"face_print":[],"forehead_coordinate":[],"temperature":-1,"frame":None,"time":-1}
    def __init__(self,face_print,forehead,temp,frame,time,id_in):
        self.face_print = face_print
        self.forehead = forehead
        self.temp = temp
        self.time = time
        self.id = id_in
    def toJSON(self):
        dicts = {}
        for t in types.keys():
            dicts[t] = eval(t)
        return json.dumps(dicts)

    def fromJSON(self,mjson):
        dictJson = json.loads(mjson)

        self.face_print = dictJson["face_print"]
        self.forehead_coordinate = dictJson["forehead_coordinate"]
        self.temperature = dictJson["temperature"]
        self.frame = dictJson["frame"]
        self.time = dictJson["time"]
        return self
if __name__=="__main__":
    #doing some simple testing on MasterObject
    obj = MasterObject()

