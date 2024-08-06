from __future__ import annotations

from dataclasses import dataclass

import cv2


@dataclass
class SaveImageCallback:
    save_folder: str

    def __call__(self, image_converted, filename: str):
        """
        Callback to save images

        :param image_converted: Image
        :type image_converted: Image
        :param filename: Filename
        :type filename: str
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
    save_folder: str
    fourcc: str
    fps: int
    image_size: tuple[int, int] = (3072, 2048)
    vid_name: str = "output.mp4"

    def __post_init__(self):
        self.out = cv2.VideoWriter(
            f"{self.save_folder}/{self.vid_name}",
            cv2.VideoWriter_fourcc(f"*{self.fourcc}"),
            self.fps,
            (self.image_size),
        )

    def __call__(self, image_converted, filename: str):
        """
        Callback to save video

        :param image_converted: Image
        :type image_converted: Image
        :param filename: str
        """

        image_converted_numpy = image_converted.GetNDArray()
        # convert BGR to RGB
        image_converted_numpy = cv2.cvtColor(image_converted_numpy, cv2.COLOR_BGR2RGB)
        self.out.write(image_converted_numpy)
        # print(image

    def __del__(self):
        self.out.release()
        print(f"Video {self.save_folder}/{self.vid_name} saved.")
