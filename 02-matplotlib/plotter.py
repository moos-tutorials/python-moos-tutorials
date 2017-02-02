#!/usr/bin/python3
from pymoos import pymoos
import time
import matplotlib.pyplot as plt
import numpy as np
import threading

fig, ax = plt.subplots()
sin_line, cos_line, = ax.plot([], [], 'r', [], [], 'b')
sin_line.set_label('DATA_SIN')
cos_line.set_label('DATA_COS')
ax.legend()

class plotter(pymoos.comms):
    """plotter is a simple app that connects to MOOSDB and plots data."""

    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(plotter, self).__init__()
        self.server = moos_community
        self.port   = moos_port
        self.name   = 'plotter'

        # getting a lock to threadsafely draw
        self.lock = threading.Lock()

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('data_sin_queue', self.on_data_sin)
        self.add_message_route_to_active_queue('data_sin_queue', 'DATA_SIN')

        self.add_active_queue('data_cos_queue', self.on_data_cos)
        self.add_message_route_to_active_queue('data_cos_queue', 'DATA_COS')

        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return (self.register("DATA_COS", 0)
                and self.register("DATA_SIN", 0)
                and self.register("DATA_OK", 0))

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            if msg.key() == 'DATA_OK' and msg.string() == 'OK':
                # using locks to threadsafe plotting
                self.lock.acquire()
                try:
                    ax.relim()
                    ax.autoscale_view(True, True, True)
                    plt.autoscale()
                    plt.draw()
                finally:
                    self.lock.release()
            else:
                print("Unhandled mail received:", msg.key(), "!")
        return True

    def on_data_sin(self, msg):
        """Special callback for DATA_SIN"""
        print("on_data_sin activated by",
              msg.key(), "with value", msg.double())
        self.lock.acquire()
        try:
            # only plot the last 101 pts
            sin_line.set_xdata(np.append(sin_line.get_xdata()[-100:], msg.time()))
            sin_line.set_ydata(np.append(sin_line.get_ydata()[-100:], msg.double()))
        finally:
            self.lock.release()
        return True

    def on_data_cos(self, msg):
        """Special callback for DATA_COS"""
        print("on_data_cos activated by",
              msg.key(), "with value", msg.double())
        self.lock.acquire()
        try:
            # only plot the last 101 pts
            cos_line.set_xdata(np.append(cos_line.get_xdata()[-100:], msg.time()))
            cos_line.set_ydata(np.append(cos_line.get_ydata()[-100:], msg.double()))
        finally:
            self.lock.release()
        return True



def main():
    plottr = plotter('localhost', 9003)

    plt.show()

if __name__=="__main__":
    main()
