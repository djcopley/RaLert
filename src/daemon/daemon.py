#!/usr/local/bin/python3
import serial
import os
import time

# TODO add thread to check for timeouts
# import threading

__version__ = "0.1"
__author__ = "Daniel Copley"


class RlDaemon:
    def __init__(self, arduino, timeout=30):
        """
        :param arduino: type serial.Serial
        """
        self._arduino = arduino

        # Conversion from radioNum to user location name
        self._nodes = {1: "West Stairwell", 2: "East Stairwell"}  # MAKE SURE TO EDIT THIS IF CONFIGURATION CHANGES
        self._detector_checkin_delta = {}  # Lookup table of time between pings for each detector

        for i in self._nodes:
            self._detector_checkin_delta[i] = time.time()

    def run(self):
        while True:
            in_byte = self._arduino.read()[0]  # Read the incoming serial byte
            movement = in_byte & 0b1  # Retrieve movement status
            radioNum = (in_byte & 0b110) >> 1  # Retrieve radioNum

            if movement:
                print(f"Movement detected - {self._nodes[radioNum]}")
                os.system("osascript ../scripts/kill_music.scpt")

            else:
                try:
                    self._detector_checkin_delta[radioNum] = time.time()

                except KeyError as err:
                    print(f"Check configuration!\n\n{err}\n")
                    os.system("osascript ../scripts/kill_music.scpt")
                    exit(1)


if __name__ == '__main__':
    try:
        # Current node configuration
        # Node1 = Receiver
        # Node2 = W Corridor
        # Node3 = E Corridor

        print("RaLert Daemon Started")
        arduino = serial.Serial(port="/dev/cu.usbmodem14301", baudrate=115200)
        daemon = RlDaemon(arduino)
        daemon.run()

    except KeyboardInterrupt:
        print("\nExiting RaLert. You're on your own now.")
        exit(0)
