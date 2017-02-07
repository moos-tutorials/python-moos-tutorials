#!/usr/bin/env python3
from pymoos import pymoos
import time
import speech_recognition as sr

class srMOOS(pymoos.comms):
    """srMOOS is an example python MOOS app.

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(srMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'srMOOS'
        self.iter = 0

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return True

    def __on_new_mail(self):
        """OnNewMail callback"""
        return True



def main():
    sr_app = srMOOS('localhost', 9000)
    r = sr.Recognizer()

    n_iter = 0

    while True:
        with sr.Microphone() as source:
            print("Listening... ")
            audio = r.listen(source)
        print("Processing... ")
        
        # save the audio file
        with open("recording"+str(n_iter)+".wav", "wb") as f:
            f.write(audio.get_wav_data())
        try:
            sr_app.notify("SPHINX_SR", r.recognize_sphinx(audio), -1)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        try:
            sr_app.notify("GOOGLE_SR", r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech"
                    "Recognition service; {0}".format(e))

        n_iter += 1
        time.sleep(.1)


if __name__ == "__main__":
    main()
