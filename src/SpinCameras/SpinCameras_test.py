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

    cam.set_pixel_format(PySpin.PixelFormat_Mono16) # good - success
    # cam.set_pixel_format(PySpin.PixelFormat_RGB8Packed) # good - success
    # cam.set_pixel_format(PySpin.PixelFormat_BayerBG8) # good - success
    # cam.set_pixel_format(PySpin.PixelFormat_BayerGB8) # good - fail
    # cam.set_pixel_format(PySpin.PixelFormat_BayerRG8) # good - fail
    # cam.set_pixel_format(PySpin.PixelFormat_BGR8) # PySpin error? - wrong pixel format reported as 'BayerGB10p
    # cam.set_pixel_format(PySpin.PixelFormat_RGB8) # good - oob failure
    # cam.set_pixel_format(PySpin.PixelFormat_YUV422_8) # good - oob failure
    # cam.set_pixel_format(PySpin.PixelFormat_BayerRGPolarized10p) # good - oob failure
    
    del cam


cameras.deinitialise_cameras()
cameras.release_all_cameras()
del cameras

system.ReleaseInstance()