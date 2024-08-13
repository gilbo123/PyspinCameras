"""
Callbacks.py

This module contains callback classes for Processing images
"""

from __future__ import annotations

from dataclasses import dataclass

import time
import importlib
from functools import wraps


def lazy_import_attributes(*attribute_names):
    def decorator(cls):
        original_getattribute = cls.__getattribute__

        @wraps(cls.__getattribute__)
        def new_getattribute(self, name):
            if name in attribute_names:
                if not hasattr(self, f"_{name}"):
                    module_name, attr_name = name.split(".")

                    # Check if the attribute is already in the global namespace
                    global_dict = globals()
                    if module_name in global_dict and hasattr(
                        global_dict[module_name], attr_name
                    ):
                        attr = getattr(global_dict[module_name], attr_name)
                    else:
                        # If not in global namespace, import it
                        module = importlib.import_module(module_name)
                        attr = getattr(module, attr_name)

                    setattr(self, f"_{name}", attr)
                return getattr(self, f"_{name}")
            return original_getattribute(self, name)

        cls.__getattribute__ = new_getattribute
        return cls

    return decorator


@dataclass
@lazy_import_attributes("cv2.imwrite", "cv2.cvtColor", "cv2.COLOR_BGR2RGB")
class SaveImageCallback:
    """
    Callback class to save images.

    Attributes:
        save_folder (str): The folder where images will be saved.
    """

    save_folder: str

    def __post_init__(self) -> None:
        """Use Lazy import to avoid importing cv2 if not needed."""

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


@dataclass
@lazy_import_attributes(
    "cv2.VideoWriter", "cv2.VideoWriter_fourcc", "cv2.cvtColor", "cv2.COLOR_BGR2RGB"
)
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

    save_folder: str
    fourcc: str = "mp4v"
    fps: int = 15
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Use Lazy import to avoid importing cv2 if not needed.
        Initializes the video writer object.
        """

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

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")


@dataclass
@lazy_import_attributes("ffmpegcv.VideoWriter", "ffmpegcv.noblock")
class SaveVideoffmpegcvCPU:
    save_folder: str
    fourcc: str
    fps: int
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Use Lazy import to avoid importing ffmpegcv if not needed.
        Initializes the video writer object.
        """

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


@dataclass
@lazy_import_attributes("ffmpegcv.VideoWriterNV")
class SaveVideoffmpegcvGPU:
    save_folder: str
    fourcc: str
    fps: int
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Use Lazy import to avoid importing ffmpegcv if not needed.
        Initializes the video writer object.
        """

        # Initialise Video writer object
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
        time.sleep(0.000001)

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")


@dataclass
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

    save_folder: str
    video_pipeline: str = "default"
    fps: int = 10
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Use lazy import to avoid importing GStreamer if not needed.
        Initializes the GStreamer pipeline and starts the video recording.
        """

        # Lazy imports
        import gi

        gi.require_version("Gst", "1.0")
        from gi.repository import Gst, GObject

        # Initialize GStreamer
        Gst.init(None)

        # Define the pipeline
        if self.video_pipeline == "default":
            pipeline_str = (
                f"appsrc name=source is-live=true format=time ! "
                f"video/x-raw,format=RGB,width={self.image_size[0]},height={self.image_size[1]},framerate={self.fps}/1 ! "
                f"videoconvert ! x264enc ! h264parse ! mp4mux ! "
                f"filesink location={self.save_folder}/{self.vid_name}"
            )

        elif self.video_pipeline == "nvenc":
            pipeline_str = (
                f"appsrc name=source is-live=true format=time ! "
                f"video/x-raw,format=RGB,width={self.image_size[0]},height={self.image_size[1]},framerate={self.fps}/1 ! "
                f"videoconvert ! nvvidconv ! nvv4l2h264enc ! h264parse ! mp4mux ! "
                f"filesink location={self.save_folder}/{self.vid_name}"
            )

        else:
            pipeline_str = self.video_pipeline

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
        if ret != Gst.FlowReturn.OK:
            print(f"push-buffer returned {ret}")

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
