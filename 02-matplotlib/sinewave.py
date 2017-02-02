#!/usr/bin/python3
from pymoos import pymoos
import time
import math

class sinewave(pymoos.comms):
    """sinewave is an example python MOOS app.
    It generates data = sin(time) and publishes it as DATA.

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """

    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(sinewave, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'sinewave'

        self.set_on_connect_callback(self.__on_connect)

        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return True



def main():
    pinger = sinewave('localhost', 9003)

    while True:
        time.sleep(.1)
        pinger.notify('DATA_SIN', math.sin(pymoos.time()), -1);
        pinger.notify('DATA_COS', math.cos(pymoos.time()), -1);
        pinger.notify('DATA_OK', 'OK', -1);

if __name__ == "__main__":
    main()
