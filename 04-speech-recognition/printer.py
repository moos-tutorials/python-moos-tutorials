#!/usr/bin/env python3
from pymoos import pymoos
import time

class printerMOOS(pymoos.comms):
    """printerMOOS is an example python MOOS app.

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(printerMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'printerMOOS'
        self.iter = 0

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return self.register('SPHINX_SR', 0)

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            if msg.key() == "SPHINX_SR":
                print("SPHINX heard:" + msg.string())
            elif msg.key() == "GOOGLE_SR":
                print("GOOGLE heard:" + msg.string())
        return True



def main():
    prntr = printerMOOS('localhost', 9000)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
