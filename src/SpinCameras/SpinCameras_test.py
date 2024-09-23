from time import sleep
from typing import Any
from Cameras import Camera, Cameras
import PySpin

system: PySpin.System = PySpin.System.GetInstance()
cameras: Cameras = Cameras(system=system)


version: PySpin.LibraryVersion = system.GetLibraryVersion()
print(
    "Spinnaker library version: "
    f"{version.major}.{version.minor}.{version.type}.{version.build}\n"
)

cameras.initialise_cameras()

for cam in cameras:
    # print(cam.get_serial_number())
    print(f"Serial number: {cam.get_serial_number()}")
    print(f"Model: {cam.get_device_name()}")

    # cam.set_pixel_format(PySpin.PixelFormat_Mono16) # good - success


    
    del cam


cameras.deinitialise_cameras()
cameras.release_all_cameras()
del cameras

system.ReleaseInstance()