#!/usr/bin/python3
from pymoos import pymoos
import time
import matplotlib.pyplot as plt
import numpy as np
import threading

fig, ax = plt.subplots(subplot_kw=dict(polar=True))
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
nav_line, des_line, = ax.plot([], [], 'r', [], [], 'b')
nav_line.set_label('NAV')
des_line.set_label('DESIRED')
ax.legend()

class plotter(pymoos.comms):
    """plotter is a simple app that connects to MOOSDB and plots data."""

    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(plotter, self).__init__()
        self.server = moos_community
        self.port   = moos_port
        self.name   = 'plotter'

        self.d_heading = 0
        self.d_speed = 0
        self.n_heading = 0
        self.n_speed = 0

        # getting a lock to threadsafely draw
        self.lock = threading.Lock()

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('nav_queue', self.on_nav)
        self.add_message_route_to_active_queue('nav_queue', 'NAV_HEADING')
        self.add_message_route_to_active_queue('nav_queue', 'NAV_SPEED')

        self.add_active_queue('desired_queue', self.on_desired)
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_HEADING')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_SPEED')

        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return (self.register("NAV_SPEED", 0)
                and self.register("NAV_HEADING", 0)
                and self.register("DESIRED_SPEED", 0)
                and self.register("DESIRED_HEADING", 0))

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

    def on_nav(self, msg):
        """Special callback for NAV_*"""
        print("on_nav activated by",
              msg.key(), "with value", msg.double())

        if msg.key() == 'NAV_HEADING':
            self.n_heading = msg.double()
        elif msg.key() == 'NAV_SPEED':
            self.n_speed = msg.double()

        r = np.arange(0, self.n_speed, 0.1)
        theta = np.deg2rad(self.n_heading)

        self.lock.acquire()
        try:
            nav_line.set_xdata(theta)
            nav_line.set_ydata(r)
            ax.set_rmax(5)
            plt.draw()
        finally:
            self.lock.release()
        return True

    def on_desired(self, msg):
        """Special callback for DESIRED_*"""
        print("on_desired activated by",
              msg.key(), "with value", msg.double())

        if msg.key() == 'DESIRED_HEADING':
            self.d_heading = msg.double()
        elif msg.key() == 'DESIRED_SPEED':
            self.d_speed = msg.double()

        r = np.arange(0, self.d_speed, 0.1)
        theta = np.deg2rad(self.d_heading)

        self.lock.acquire()
        try:
            des_line.set_xdata(theta)
            des_line.set_ydata(r)
            ax.set_rmax(5)
            plt.draw()
        finally:
            self.lock.release()
        return True



def main():
    plottr = plotter('localhost', 9000)

    plt.show()

if __name__=="__main__":
    main()
