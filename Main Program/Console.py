import threading, Module

class Console(Module.Module):
    def __init__(self):
        self.buf = []
        self.run = True
        self.empty = True
        self.trd = threading.Thread()
        self.trd.daemon = True
        self.trd.start()

    def mainloop(self):
        while self.run:
            s = input()
            print(s)
            if s == 'exec':
                print('exec')
                print(exec(input()))
            else:
                self.buf.append(s)
                self.empty = False

    def available(self):
        return not self.empty

    def readLine(self):
        str = self.buf[0]
        del self.buf[0]
        if len(self.buf) == 0:
            self.empty = True

print('Library, Console is Loaded')