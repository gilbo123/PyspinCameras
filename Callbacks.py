"""
Callbacks.py

This module contains callback classes for Processing images
"""

from __future__ import annotations

from dataclasses import dataclass
import cv2
import ffmpegcv


@dataclass
class SaveImageCallback:
    """
    Callback class to save images.

    Attributes:
        save_folder (str): The folder where images will be saved.
    """

    save_folder: str

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
        print(image_converted_numpy.shape)

        # save the image
        cv2.imwrite(f"{self.save_folder}/{filename}", image_converted_numpy)  # type: ignore
        print(f"Callback CLASS - Image {filename} saved.")


@dataclass
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
    fourcc: str
    fps: int
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Initializes the video writer object.
        """
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
class SaveVideoffmpegcv:
    save_folder: str
    fourcc: str
    fps: int
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self) -> None:
        """
        Initializes the video writer object.
        """
        self.out = ffmpegcv.VideoWriterNV(
            f"{self.save_folder}/{self.vid_name}", self.fourcc, self.fps
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
        # image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)
        self.out.write(image_converted_numpy)

    def __del__(self):
        """
        Releases the video writer object and saves the video file.
        """
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")
