# -*- coding: utf-8 -*-

import threading
from time import sleep

class Thread(threading.Thread):
    def __init__(self, name, function, period= 0, loop= True):
        threading.Thread.__init__(self)
        self.name = name
        self.function = function
        self.period = period
        self.loop = loop
        self._running = True


    def run(self):
        while True:
            if self._running == False:
                break
            self.function()
            if self.loop == False:
                return
            sleep(self.period)
