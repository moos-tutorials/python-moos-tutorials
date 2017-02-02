#!/usr/bin/python3
from pymoos import pymoos
import time

class pingMOOS(pymoos.comms):
    """pingMOOS is an example python MOOS app.
    It basically just connects to the MOOSDB

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """

    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(pingMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'pingMOOS'

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('pong_queue', self.on_pong_message)
        self.add_message_route_to_active_queue('pong_queue', 'PONG')

        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        self.register ('PING', 0) # just to prove that the callback work
        return self.register('PONG', 0)

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            print("OnNewMail caught", msg.key(), "!")
        return True

    def on_pong_message(self, msg):
        """Special callback for PONG"""
        print("on_pong_message activated by",
              msg.key(), "with value", msg.double())
        return True



def main():
    pinger = pingMOOS('localhost', 9002)

    while True:
        time.sleep(1)
        pinger.notify('PING', 'Hello world!', -1);

if __name__ == "__main__":
    main()
