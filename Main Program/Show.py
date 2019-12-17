import threading, Module, pygame, datetime, time

class Show(Module.Module):
    module_name = 'Show'
    show_name = 'default'

    isDied = False
    isEmpty = True
    flagQuit = False
    err_refresh = ''
    last_refresh = datetime.datetime.min
    
    def Load(self):
        pass
    def __init__(self, w, h):
        try:
            print('Staring Show, %s' % (self.show_name))
            self.surf = pygame.Surface((w, h))
            self.W = w
            self.H = h
            self.Load()
            self.trd = threading.Thread(target=self.Loop)
            self.trd.daemon = True
            self.trd.start()
            self.mutex.acquire()
            print('Success to start Show, %s' % (self.show_name))
            self.mutex.release()
        except Exception as e:
            self.mutex.acquire()
            print('%s Failed to start Show, %s\n%s' % (str(datetime.datetime.now()), self.show_name, str(e)))
            self.mutex.release()
            self.isDied = True

    def isFresh(self):
        return True
    
    def Refresh(self):
        try:
            pass
        except Exception as e:
            self.err_refresh = str(e)
            pass

    def Render(self):
        def w(n):
            return self.W * n / 100
        def h(n):
            return self.H * n / 100
        return self.surf

    def Loop(self):
        while not self.flagQuit:
            if not self.isFresh():
                self.Refresh()
                time.sleep(1)
                

    def isFresh(self):
        now = datetime.datetime.now()
        if (now - self.last_refresh) > self.period:
            self.last_refresh = now
            return False
        
        return True
    
    def Loop(self):
        while not self.flagQuit:
            if not self.isFresh():
                try:
                    self.Refresh()
                    self.mutex.acquire()
                    print('%s %s is Refresh'%(str(datetime.datetime.now()), self.show_name))
                    self.mutex.release()
                    time.sleep(self.period.seconds)
                except Exception as e:
                    self.mutex.acquire()
                    print('%s %s is Failed to Refresh %s'%(str(datetime.datetime.now()), self.show_name, str(e)))
                    self.mutex.release()
                
    
print('Library, Show is Loaded')
