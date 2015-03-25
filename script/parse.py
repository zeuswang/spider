import json
class Parser:
    def __init__(self):
        pass
    def init(self,template):
        fp = open(template,'r')
        text = fp.read()
        s = json.load(text)
        print s
