from time import strftime


def time():
    return strftime("%Y/%m/%d_%H:%M:%S")


class Logger:
    def Init(self, path):
        self.file = open(path, 'a')

    def __call__(self, text):
        self.Log("[" + time() + "]" + text)

    def Log(self, text):
        self.file.write(text)

    def BackColour(self, r, g, b):
        self.Log('\x1b[48;5;%sm' % (16 + 36 * r + 6 * g + b))

    def ForeColour(self, r, g, b):
        self.Log('\x1b[38;5;%sm' % (16 + 36 * r + 6 * g + b))

    def Severe(self, text):
        self.ForeColour(5, 5, 0)
        self("[Severe]" + text)
        self.ForeColour(5, 5, 5)

    def Critical(self, text):
        self.ForeColour(5, 0, 0)
        self("[CRITICAL]" + text)
        self.ForeColour(5, 5, 5)

