import datetime, os, sys, time
import argparse
from .camera import OlympusCamera, EM10Mk4
from .calibrate import download_image
import logging

import pdb

##############################################################################
#     class LiveViewWindow displays the camera's live view in a window.      #
##############################################################################

class Lights():
    camera = None
    def get_logger(self):
        logger = logging.getLogger('camera-logger')
        level = logging.getLevelName('DEBUG')
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        #Create a formatter for the logs
        time_format = "%Y-%m-%d %H:%M:%S"
        log_format = '%(created)f:%(levelname)s:%(name)s:%(module)s: %(message)s'
        formatter = logging.Formatter(log_format, datefmt=time_format)
        #Set the created formatter as the formatter of the handler
        handler.setFormatter(formatter)
        #Add the created handler to this logger
        logger.addHandler(handler)
        return logger


    def __init__(self, camera):
        self.camera = camera
        self.camera.set_logger(self.get_logger())

    def capture(self, shutter_speed):
        if shutter_speed:
            pass
        self.camera.set_camprop('shutspeedvalue', "5\"")
        self.camera.set_camprop('isospeedvalue', "800")
        self.camera.take_picture()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--iso', default='800', help='ISO to take the lights at')
    parser.add_argument('--shutter-speed', default='5"', help='Shutter speed to take the lights at')
    parser.add_argument('--tag', action='store_true')
    args = parser.parse_args()

    camera = EM10Mk4()
    # TODO: verify camera connection
    lights = Lights(camera)
    lights.capture("5\"")


if __name__ == '__main__':
    main()
