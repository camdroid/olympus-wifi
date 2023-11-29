import datetime, os, sys, time
import argparse
from .camera import OlympusCamera, EM10Mk4

import pdb

##############################################################################
#     class LiveViewWindow displays the camera's live view in a window.      #
##############################################################################

# TODO: Allow the parent function to sort how these are sorted into folders.
# That way, we can automatically sort them into darks/biases/flats.
def download_image(camera, file_name):
    print('Downloading images')
    image = camera.download_image(file_name)
    with open(f'/tmp/{file_name.replace("/", "_")}', 'wb') as file:
        file.write(image)


class Calibrations:
    camera = None

    def __init__(self, camera):
        self.camera = camera

    def biases(self):
        camera = self.camera
        camera.set_camprop('shutspeedvalue', '4000')
        total_biases = 3
        for i in range(total_biases):
            print(f'Taking bias image {i}/{total_biases}')
            camera.take_picture()

        # For some reason, RAW photos are still being taken as RAW+JPEG, even when the camera mode is only on RAW.
        # Because of this, we need to look at twice as many previous photos, then exclude the JPEG ones.
        to_download = camera.list_images()[-2*total_biases:]
        [download_image(camera, i.file_name) 
         for i in to_download 
         if 'JPG' not in i.file_name.upper() ]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--iso', help='ISO that the lights were taken at')
    parser.add_argument('--shutter-speed', help='Shutter speed that the lights were taken at')
    args = parser.parse_args()

    # Connect to camera.
    camera = EM10Mk4()
    calibrations = Calibrations(camera)
    calibrations.biases()
    return True


if __name__ == '__main__':
    main()
