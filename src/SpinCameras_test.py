from dataclasses import dataclass
from queue import Queue
from threading import Thread
from time import sleep
from typing import Any

from numpy import ndarray
from PyspinCameras.Cameras import Camera, Cameras
import PySpin

@dataclass
class MultipleCameraImageCallBack:
    """Callback to save images"""

    save_folder: str

    def __call__(self, image_converted: PySpin.Image, filename: str) -> None:
        """
        Callback to save images

        :param image_converted: Image
        :type image_converted: Image
        :param filename: Filename
        :type filename: str
        """

        # convert to numpy array
        image_converted_numpy: ndarray = image_converted.GetNDArray()

        print(f"Image shape: {image_converted_numpy.shape}")

        # save the image
        print(f"Callback CLASS - Image {filename} saved.")

        # anything else you want to do with the image
        ## convert to RGB
        # image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)  # type: ignore

        ## display the image
        # cv2.imshow(cam_id, image_converted_numpy)  # type: ignore
        # cv2.waitKey(1)  # type: ignore

        ## save the image
        # cv2.imwrite(f"{self.save_folder}/{filename}", image_converted_numpy)  # type: ignore


if __name__ == "__main__":


    # reference to PySpin
    system: PySpin.System = PySpin.System.GetInstance()

    # reference to the queue
    queue: Queue = Queue()

    # pass the queue to the cameras
    cameras: Cameras = Cameras(system=system, queue=queue)

    # initialise the cameras
    cameras.initialise_cameras()

    print(cameras)
    print(cameras[0])
    
    # acquire 10 images
    Thread(target=cameras.acquire_images, kwargs={"num_images": 10}).start()

    # access the queue
    for i in range(10):
        image_dict: dict[str, str | PySpin.Image] = queue.get()
        # convert to numpy array
        image_numpy: ndarray = image_dict["image"].GetNDArray()
        
        print(image_numpy.shape)
        print(image_dict["filename"])
        
        # do something with the image



    """
    TOP = "24132701"
    BOTTOM = "24025827"
    IR_TOP = "24236109"
    IR_BOTTOM = "24236108"

    system: PySpin.System = PySpin.System.GetInstance()
    cameras: Cameras = Cameras(system=system)
    print(cameras.get_camera_info())
    # print(cameras)

    cameras.initialise_cameras()

    callback = MultipleCameraImageCallBack(save_folder="/home/temp/images")

    for i, cam in enumerate(cameras):
        # camera: Camera = cameras.get_camera_by_serial(cam.device_serial_number)
        # print(camera)

        if cam.device_serial_number in [TOP, BOTTOM]:
            print("RGB camera")
            cam.set_pixel_format(PySpin.PixelFormat_RGB8Packed) # good - success
        elif cam.device_serial_number in [IR_TOP, IR_BOTTOM]:
            print("IR camera")
            cam.set_pixel_format(PySpin.PixelFormat_Mono8)
        else:
            print("Unknown camera")
            break

        cam.set_acquisition_mode(acq_mode="continuous")
        # cam.se
        cam.set_frame_rate(frame_rate=20.0)
        cam.set_stream_buffer_mode(buffer_mode="newest-only")
        # set softwatre trigger
        print(cam.set_trigger_mode(trigger_mode="off"))

        #set callback
        cam.set_callback_function(callback)

        # start acquisition
        # cam.start_acquisition()
        # cam.get_next_image()
        # cam.stop_acquisition()

        
        
        # del camera    
        del cam

    cameras.acquire_images()

    cameras.release_all_cameras()

    system.ReleaseInstance()
    """