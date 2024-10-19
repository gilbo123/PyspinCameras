
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for build-url, contributors-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Build Status][build-shield]][build-url]
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/gilbo123/PyspinCameras">
    <img src="assets/firefly-s.png" alt="Logo" width="500">
  </a>

  <h3 align="center">Pyspin Cameras</h3>

  <p align="center">
    A simple wrapper for the PySpin library to allow for easy control of FLIR cameras.
    <br />
    <a href="https://github.com/gilbo123/PyspinCameras"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/gilbo123/PyspinCameras">View Demo</a>
    ·
    <a href="https://github.com/gilbo123/PyspinCameras/issues">Report Bug</a>
    ·
    <a href="https://github.com/gilbo123/PyspinCameras/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Cameras blackfly-s][product-screenshot]](https://example.com)

This project is a simple wrapper for the PySpin library to allow for easy control of FLIR cameras.

Features:
* Fast and easy to use.
  * Get camera information.
  * Set camera parameters.
  * Acquire images.
* Image queueing.
* Image callback function.

### Built With

Frameworks used in the application:

* [![Python][python-shield]](https://www.python.org/)


<!-- GETTING STARTED -->
## Getting Started

This project requires a FLIR camera and the PySpin library to be installed.

### Prerequisites

* PySpin

Follow the instructions [here](https://www.teledynevisionsolutions.com/products/spinnaker-sdk/) to install the PySpin library.
__Note:__ You may need to install the SDK depending on the camera you have. This package has been tested using SDK version 3.0.0.117 and 3.1.0.79.

### Installation

1. Clone the repo
```sh
git clone https://github.com/gilbo123/PyspinCameras.git
```
```sh
cd PyspinCameras
```
3. Install requirements
```sh
pip3 install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

```python
# reference to PySpin
system: PySpin.System = PySpin.System.GetInstance()

# reference to the cameras
cameras: Cameras = Cameras(system=system)
print(cameras)

# initialise the cameras
cameras.initialise_cameras()

# acquire 10 images
cameras.acquire_images(num_images=10)

# cameras.deinitialise_cameras()
cameras.release_all_cameras()
del cameras

# dereference the system
system.ReleaseInstance()

```

```python
# go through each camera 
for i, cam in enumerate(cameras):
    # get the camera by serial number
    # camera: Camera = cameras.get_camera_by_serial(cam.device_serial_number)
    
    print(cam)

    # set parameters
    cam.set_pixel_format(PySpin.PixelFormat_Mono8)
    cam.set_acquisition_mode(acq_mode="continuous")
    cam.set_frame_rate(frame_rate=20.0)
    cam.set_stream_buffer_mode(buffer_mode="newest_only")
    cam.set_trigger_mode(trigger_mode="off")

    #set callback
    cam.set_callback_function(callback)
```


_For more examples, please refer to the [Documentation](https://example.com)_



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

* Gilbert Eaton - [@mechatronicdoc](https://x.com/mechatronicdoc) - gilberteaton@gmail.com
* Jonathon Holder - [@]() - jonathon.holder.90@gmail.com

Project Link: [https://github.com/gilbo123/PyspinCameras](https://github.com/gilbo123/PyspinCameras)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[build-shield]: https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square
[build-url]: #
[contributors-shield]: https://img.shields.io/github/contributors/gilbo123/PyspinCameras.svg?style=flat-square
[contributors-url]: https://github.com/gilbo123/PyspinCameras/graphs/contributors
[license-shield]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-url]: https://github.com/gilbo123/PyspinCameras/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com
[product-screenshot]: assets/firefly-s.png
[python-shield]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
