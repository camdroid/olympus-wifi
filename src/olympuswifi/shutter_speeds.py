import datetime
import pdb

class ShutterSpeeds():
    exposure_duration = None

    def __init__(self, shutter_speed):
        pdb.set_trace()
        if '"' in shutter_speed:
            exposure_duration = datetime.timedelta(0, int(shutter_speed[:-1]))
            
        pass

if __name__ == '__main__':
    ShutterSpeeds("60'")
