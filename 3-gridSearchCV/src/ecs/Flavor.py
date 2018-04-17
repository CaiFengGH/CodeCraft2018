class Flavor:
    def __init__(self,name,cpu,mem):
        self.name = name
        self.cpu = cpu
        self.mem = mem / 1024
        self.target = None
        self.other = None
    def setTarget(self,TARGET_NAME):
        if TARGET_NAME == "CPU":
            self.target = self.cpu
            self.other = self.mem
        else:
            self.target = self.mem
            self.other = self.cpu
