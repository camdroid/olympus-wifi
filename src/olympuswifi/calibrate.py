import datetime, os, sys, time
import argparse
from .camera import OlympusCamera, EM10Mk4

import pdb

##############################################################################
#     class LiveViewWindow displays the camera's live view in a window.      #
##############################################################################

DEFAULT_ISO = "800"
DEFAULT_EXPOSURE = "60\""
DEBUG = True

# TODO: Allow the parent function to sort how these are sorted into folders.
# That way, we can automatically sort them into darks/biases/flats.
def download_image(camera, file_name):
    print('Downloading images')
    if camera is not None:
        image = camera.download_image(file_name)
        # The file name starts with "/", so trim that before replacing them with
        # underscores
        file_name = file_name[1:].replace("/", "_")
        with open(f'/tmp/{file_name}', 'wb') as file:
            file.write(image)

    image = None
    from exif import Image
    import exifread

    TAGS_FOR_CALIBRATION = [
        'EXIF ExposureTime',
        'EXIF ISOSpeedRatings',
    ]

    with open(f'/tmp/{file_name}', 'rb') as image_file:
        # pdb.set_trace()
        tags = exifread.process_file(image_file)
        for tag in TAGS_FOR_CALIBRATION:
            print(f'{tag}: {tags[tag]}')
        print('done')
    return None


class Calibrations:
    camera = None

    def __init__(self, camera, iso, exposure):
        self.camera = camera
        self.iso = iso
        self.lights_exposure = exposure
        self.reset_camprops()

    def reset_camprops(self):
        self.camera.set_camprop('shutspeedvalue', self.lights_exposure)
        self.camera.set_camprop('isospeedvalue', self.iso)

    def take_n_pictures(self, n=50, picture_type="(Unknown)"):
        for i in range(n):
            print(f'Taking {picture_type} image {i}/{n}')
            self.camera.take_picture()
        print(f'Done taking {n} {picture_type} photos')

    def biases(self):
        self.reset_camprops()
        self.camera.set_camprop('shutspeedvalue', '4000')
        self.take_n_pictures(50, 'bias')

    def darks(self):
        self.reset_camprops()
        self.take_n_pictures(50, 'darks')

    def flats(self):
        self.reset_camprops()
        self.take_n_pictures(25, 'flats')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--iso', help='ISO that the lights were taken at', default=DEFAULT_ISO)
    parser.add_argument('--shutter-speed', help='Shutter speed that the lights were taken at', default=DEFAULT_EXPOSURE)
    parser.add_argument('--tag', action='store_true')
    args = parser.parse_args()

    if args.tag:
        download_image(None, '/_DCIM_100OLYMP_PC031944.ORF')


    # Connect to camera.
    camera = EM10Mk4()
    calibrations = Calibrations(camera, args.iso, args.shutter_speed)
    input('Hit enter when the lens cap is on')
    calibrations.biases()
    calibrations.darks()
    print('For flats, you need:\n1) The lens cap off\n2) A white t-shirt over the lens,\n3) pointing at a phone screen')
    input('Hit enter when the above is set up')
    calibrations.flats()
    return True


if __name__ == '__main__':
    main()
