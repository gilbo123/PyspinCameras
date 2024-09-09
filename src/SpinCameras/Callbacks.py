"""
Callbacks.py

This module contains callback classes for Processing images
"""

from __future__ import annotations

import time
import importlib
from functools import wraps


def lazy_import_attributes(*attribute_names):
    def decorator(cls):
        original_init = cls.__init__

        @wraps(cls.__init__)
        def new_init(self, *args, **kwargs):
            # print(f"Initializing {cls.__name__}")  # Debug print

            global_dict = globals()

            for name in attribute_names:
                # print(f"Importing {name}")  # Debug print

                # Split the name into module and attribute parts
                parts = name.split(".")
                module_name = parts[0]

                # Import the module if it's not already in globals
                if module_name not in global_dict:
                    # print(f"Importing new module {module_name}")  # Debug print
                    module = importlib.import_module(module_name)
                    global_dict[module_name] = module
                    if name == "gi":
                        module.require_version("Gst", "1.0")
                    if len(parts) > 1:
                        attr_name = ".".join(parts[1:])
                        attr = getattr(module, attr_name)
                        global_dict[parts[-1:]] = attr
                        # print(f"Added {attr_name} to global namespace")  # Debug print
                    else:
                        # If it's just a module, make sure it's in the class namespace
                        setattr(cls, module_name, module)
                        # print(f"Added {module_name} to class namespace")  # Debug print
                elif (
                    module_name in global_dict
                    and len(parts) > 1
                    and parts[-1] not in global_dict
                ):
                    # print(f"Importing new attribute {parts[-1]}")  # Debug print
                    if module_name == "gi":
                        module = importlib.import_module(name)
                        global_dict[parts[-1]] = module
                    else:
                        attr_name = ".".join(parts[1:])
                        attr = getattr(global_dict[module_name], attr_name)
                        global_dict[parts[-1:]] = attr
                    # print(f"Added {attr_name} to global namespace")  # Debug print

                else:
                    # print(f"Using existing module {module_name}")  # Debug print
                    pass
                    # module = global_dict[module_name]

            # Call the original __init__
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    return decorator


@lazy_import_attributes("cv2")
class SaveImageCallback:
    """
    Callback class to save images.

    Attributes:
        save_folder (str): The folder where images will be saved.
    """

    def __init__(self, save_folder: str) -> None:
        self.save_folder = save_folder

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to save an image.

        Args:
            image_converted (Image): Image object that can be converted to a numpy array.
            filename (str): Filename for the saved image.
        """
        image_converted_numpy = image_converted.GetNDArray()
        # convert BGR to RGB
        image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)  # type: ignore
        # print(image_converted_numpy.shape)

        # save the image
        cv2.imwrite(f"{self.save_folder}/{filename}", image_converted_numpy)  # type: ignore
        print(f"Callback CLASS - Image {filename} saved.")


@lazy_import_attributes("cv2")
class SaveVideoCallback:
    """
    Callback class to save videos.

    Attributes:
        save_folder (str): The folder where videos will be saved.
        fourcc (str): FourCC code for the video codec.
        fps (int): Frames per second for the video.
        image_size (tuple[int, int]): Size of the video frames.
        vid_name (str): Name of the output video file.
    """

    def __init__(
        self,
        save_folder: str,
        fourcc: str = "mp4v",
        fps: int = 15,
        image_size: tuple[int, int] = (3072, 2048),
        vid_name: str = "output.mp4",
    ) -> None:
        self.save_folder = save_folder
        self.fourcc = fourcc
        self.fps = fps
        self.image_size = image_size
        self.vid_name = vid_name
        self.frame_count = 0

        # Initalise video writer object
        self.out = cv2.VideoWriter(
            f"{self.save_folder}/{self.vid_name}",
            cv2.VideoWriter_fourcc(*f"{self.fourcc}"),
            self.fps,
            (self.image_size),
        )

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to save a video frame.

        Args:
            image_converted (Image): Image object that can be converted to a numpy array.
            filename (str): Filename for the saved frame (not used in this method).
        """
        image_converted_numpy = image_converted.GetNDArray()
        # convert BGR to RGB
        image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)
        self.out.write(image_converted_numpy)
        self.frame_count += 1
        print(f"Frame {self.frame_count} added to video.")

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")


@lazy_import_attributes("ffmpegcv")
class SaveVideoffmpegcvCPU:
    """
    Callback class to save videos using ffmpegcv.

    Attributes:
        save_folder (str): The folder where videos will be saved.
        fourcc (str): FourCC code for the video codec.
        fps (int): Frames per second for the video.
        image_size (tuple[int, int]): Size of the video frames.
        vid_name (str): Name of the output video file.
    """

    def __init__(
        self,
        save_folder: str,
        fourcc: str,
        fps: int,
        image_size: tuple[int, int] = (3072, 2048),
        vid_name: str = "output.mp4",
    ) -> None:

        self.save_folder = save_folder
        self.fourcc = fourcc
        self.fps = fps
        self.image_size = image_size
        self.vid_name = vid_name

        # Initialise video writer object
        self.out = ffmpegcv.noblock(
            ffmpegcv.VideoWriter,
            f"{self.save_folder}/{self.vid_name}",
            self.fourcc,
            self.fps,
            pix_fmt="rgb24",
        )

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to save a video frame.

        Args:
            image_converted (Image): Image object that can be converted to a numpy array.
            filename (str): Filename for the saved frame (not used in this method).
        """
        image_converted_numpy = image_converted.GetNDArray()

        self.out.write(image_converted_numpy)
        time.sleep(0.000001)

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")


@lazy_import_attributes("ffmpegcv")
class SaveVideoffmpegcvGPU:
    """
    Callback class to save videos using ffmpegcv with GPU.

    Attributes:
        save_folder (str): The folder where videos will be saved.
        fourcc (str): FourCC code for the video codec.
        fps (int): Frames per second for the video.
        image_size (tuple[int, int]): Size of the video frames.
        vid_name (str): Name of the output video file.
    """

    def __init__(
        self,
        save_folder: str,
        fourcc: str,
        fps: int,
        image_size: tuple[int, int] = (3072, 2048),
        vid_name: str = "output.mp4",
    ) -> None:

        self.save_folder = save_folder
        self.fourcc = fourcc
        self.fps = fps
        self.image_size = image_size
        self.vid_name = vid_name

        self.frame_count = 0

        # Initialise video writer object
        self.out = ffmpegcv.VideoWriterNV(
            f"{self.save_folder}/{self.vid_name}",
            self.fourcc,
            self.fps,
            pix_fmt="rgb24",
        )

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to save a video frame.

        Args:
            image_converted (Image): Image object that can be converted to a numpy array.
            filename (str): Filename for the saved frame (not used in this method).
        """
        image_converted_numpy = image_converted.GetNDArray()

        self.out.write(image_converted_numpy)
        self.frame_count += 1
        print(f"Frame {self.frame_count} added to video.")
        time.sleep(0.000001)

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")


@lazy_import_attributes("gi", "gi.repository.Gst", "gi.repository.GObject")
class SaveVideoGstreamer:
    """
    Callback class to save video using GStreamer.

    Attributes:
        save_folder (str): The folder where the video will be saved.
        video_pipeline (str): Gstreamer pipeline for video processing. options (default, nvenc) or custom.
        fps (int): Frames per second for the output video.
        image_size (tuple[int, int]): The size of the input images (width, height).
        vid_name (str): The name of the output video file.
    """

    def __init__(
        self,
        save_folder: str,
        video_pipeline: str = "default",
        fps: int = 10,
        image_size: tuple[int, int] = (3072, 2048),
        vid_name: str = "output.mp4",
    ) -> None:

        self.save_folder = save_folder
        self.video_pipeline = video_pipeline
        self.fps = fps
        self.image_size = image_size
        self.vid_name = vid_name

        # Initialize GStreamer
        Gst.init(None)

        # Define the pipeline
        if video_pipeline == "default":
            pipeline_str = (
                f"appsrc name=source is-live=true format=time ! "
                f"video/x-raw,format=RGB,width={image_size[0]},height={image_size[1]},framerate={fps}/1 ! "
                f"videoconvert ! x265enc ! h265parse ! mp4mux ! "
                f"filesink location={save_folder}/{vid_name}"
            )

        elif video_pipeline == "nvenc":
            pipeline_str = (
                f"appsrc name=source is-live=true format=time ! "
                f"video/x-raw,format=RGB,width={image_size[0]},height={image_size[1]},framerate={fps}/1 ! "
                f"videoconvert ! nvvidconv ! nvv4l2h265enc ! h265parse ! mp4mux ! "
                f"filesink location={save_folder}/{vid_name}"
            )

        elif video_pipeline == "nvenc-bayer":
            pipeline_str = (
                f"appsrc name=source is-live=true format=time !"
                f"video/x-bayer,format=rggb,width={image_size[0]},height={image_size[1]},framerate={fps}/1 ! "
                f"bayer2rgb !"
                f"videoconvert ! nvvidconv ! nvv4l2h265enc ! h265parse ! matroskamux ! "
                f"filesink location={save_folder}/{vid_name}"
            )

        else:
            pipeline_str = video_pipeline

        # Create the pipeline
        self.pipeline = Gst.parse_launch(pipeline_str)
        self.appsrc = self.pipeline.get_by_name("source")

        # Configure appsrc
        self.appsrc.set_property("format", Gst.Format.TIME)
        self.appsrc.set_property("do-timestamp", True)

        # Start the pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

        self.frame_count = 0
        self.start_time = time.time()

    def __call__(self, image_converted, filename: str) -> None:
        """
        Callback to add a frame to the video.

        Args:
            image_converted (Image): Image object that can be converted to a numpy array.
            filename (str): Filename for the frame (not used in video saving, but kept for compatibility).
        """
        image_data = image_converted.GetNDArray()

        if image_data.shape[2] != 3:
            raise ValueError("Image must be in BGR format")

        buffer = Gst.Buffer.new_wrapped(image_data.tobytes())

        # Calculate timestamp
        timestamp = int((time.time() - self.start_time) * Gst.SECOND)
        buffer.pts = timestamp
        buffer.duration = int(Gst.SECOND / self.fps)

        # Push the buffer into appsrc
        ret = self.appsrc.emit("push-buffer", buffer)
        # if ret != Gst.FlowReturn.OK:
        #     print(f"push-buffer returned {ret}")

        self.frame_count += 1
        print(f"Frame {self.frame_count} added to video.")

    def stop(self):
        """
        Stop the video recording and finalize the file.
        """
        # Send EOS event
        self.appsrc.emit("end-of-stream")

        # Wait for EOS to propagate
        bus = self.pipeline.get_bus()
        bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)

        # Stop the pipeline
        self.pipeline.set_state(Gst.State.NULL)

        print(
            f"Video {self.save_folder}/{self.vid_name} saved. Total frames: {self.frame_count}"
        )

    def __del__(self):
        self.stop()
