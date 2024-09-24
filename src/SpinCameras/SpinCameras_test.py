from dataclasses import dataclass
from queue import Queue
from time import sleep
from typing import Any
from Cameras import Camera, Cameras
import PySpin

@dataclass
class MultipleCameraImageCallBack:
    """Callback to save images"""

    save_folder: str
    cameras: Cameras
    index: int

    def __post_init__(self) -> None:
        """
        Post-initialisation method
        """

        # get the camera using `index`
        # self.camera: Camera = self.cameras[self.index]
        

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to save images

        :param image_converted: Image
        :type image_converted: Image
        :param filename: Filename
        :type filename: str
        """

        print(f"Callback CLASS - Image {filename} saved.")

        # convert to numpy array
        image_converted_numpy = image_converted.GetNDArray()
        # convert BGR to RGB
        # image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)  # type: ignore

        print(f"Image shape: {image_converted_numpy.shape}")
        
        # cv2.imshow(cam_id, image_converted_numpy)  # type: ignore
        # cv2.waitKey(1)  # type: ignore
        # save the image
        # cv2.imwrite(f"{self.save_folder}/{filename}", image_converted_numpy)  # type: ignore


if __name__ == "__main__":

    system: PySpin.System = PySpin.System.GetInstance()
    cameras: Cameras = Cameras(system=system)

    print(cameras)

    cameras.initialise_cameras()

    callback = MultipleCameraImageCallBack(save_folder="/home/temp/images", cameras=cameras, index=0)

    for i, cam in enumerate(cameras):
        # camera: Camera = cameras.get_camera_by_serial(cam.device_serial_number)
        # print(camera)

        cam.set_pixel_format(PySpin.PixelFormat_RGB8Packed) # good - success

        cam.set_acquisition_mode(acq_mode="continuous")
        # cam.se
        cam.set_frame_rate(frame_rate=20.0)
        cam.set_stream_buffer_mode()
        # set softwatre trigger
        print(cam.set_trigger_mode(trigger_mode="off"))

        #set callback
        cam.set_callback_function(callback)

        # start acquisition
        # cam.start_acquisition()
        # cam.get_next_image()
        # cam.stop_acquisition()

        # sleep(3)

        
        
        # del camera    
        del cam


    cameras.deinitialise_cameras()
    cameras.release_all_cameras()
    del cameras

    system.ReleaseInstance()