import argparse, datetime, io, os, queue, socket, sys, threading, tkinter, time
import pdb
from threading import Thread

from dataclasses import dataclass   # needs Python 3.7 or later
from typing import Tuple, Optional

from PIL import Image, ImageTk # on Ubuntu install with "apt install -y python3-pil"

from .camera import OlympusCamera, EM10Mk4
from .liveview import LiveViewWindow

PROP_NAMES = ['touchactiveframe', 'takemode', 'drivemode', 'focalvalue',
              'expcomp', 'shutspeedvalue', 'isospeedvalue', 'wbvalue',
              'noisereduction', 'lowvibtime', 'bulbtimelimit', 'artfilter',
              'digitaltelecon', 'exposemovie', 'cameradrivemode',
              'colorphase', 'SceneSub', 'SilentNoiseReduction', 'SilentTime',
              'ArtEffectTypePopart', 'ArtEffectTypeRoughMonochrome',
              'ArtEffectTypeToyPhoto', 'ArtEffectTypeDaydream',
              'ArtEffectTypeCrossProcess', 'ArtEffectTypeDramaticTone',
              'ArtEffectTypeLigneClair', 'ArtEffectTypePastel',
              'ArtEffectTypeMiniature', 'ArtEffectTypeVintage',
              'ArtEffectTypePartcolor', 'ArtEffectTypeBleachBypass']


# *****
# This script is intended to help with scheduling multiple shots in a row of a particular setting.
# Specifically for use with astrophotography, in my case.
# *****

def threaded_window(camera, options):
    pdb.set_trace()
    camera.get_commands()

def main() -> None:
    PORT = 12000
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-P', type=int, default=PORT,
                        help=f"UPD port for liveview (default: {PORT}).")
    parser.add_argument('--shutter-speed SPD', '-S', type=str, default='60',
                        help=f"Shutter speed for captured photos (default: 1/60)"), 
    args = parser.parse_args()

    # Connect to camera.
    camera = EM10Mk4()

    # Report camera model.
    camera.report_model()
    options = {
        'shutspeedvalue': args.shutter_speed,
    }

    res = camera.get_commands()
    t = Thread(target=threaded_window, args=(camera, options))
    # Window must be run from the main thread (Mac requirement)
    LiveViewWindow(camera, args.port)
    # camera.send_command('switch_cammode')
    # camera.take_picture()
    pdb.set_trace()
    # res[‘get_camprop’].args[‘com’][‘get’][‘propname’]
    print(res)


    print("hello world, I'm still here")
    t.join()

if __name__ == '__main__':
    main()
