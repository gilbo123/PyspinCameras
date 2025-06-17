"""Cam reset module - allows resetting camera via software and force IP protocol."""

from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Any

import PySpin

from yaml import FullLoader
from yaml import load as yaml_load


@dataclass
class CamReset:
    """Class for camera operations to reset and force IP."""

    # PySpin system
    system: PySpin.System

    def force_all_ips(self) -> None:
        """Force the IP on ALL cameras."""

        cams: PySpin.CameraList = self.system.GetCameras()

        # check there are cameras first
        if len(cams) == 0:
            # self.fmtr.print_error("No cameras found")
            print("No Cameras...")
            return

        print(f"Found {len(cams)} cameras...")

        for ifp in self.system.GetInterfaces():
            interface: PySpin.InterfacePtr = ifp
            tl: PySpin.TransportLayerInterface = interface.TLInterface
            dc: PySpin.IInteger = tl.DeviceCount

            # if any devices connected to this interface
            if dc.GetValue() > 0:
                # resets the gateway (GEV device)
                print("Forcing IPs....")

                # get the cams
                cams: PySpin.CameraList = interface.GetCameras()
                try:
                    for cam in cams:
                        # cam pointer
                        cam: PySpin.CameraPtr
                        dev: PySpin.TransportLayerDevice = cam.TLDevice
                        force: PySpin.ICommand = dev.GevDeviceAutoForceIP
                        force.ImposeAccessMode(PySpin.RW)
                        force.Execute(Verify=True)
                except PySpin.SpinnakerException as ex:
                    print(f"Error - {ex}")

    def force_ip_by_cam(self, cam: PySpin.CameraPtr) -> None:
        """Force the IP on single PySPin camera."""

        # check cam is valid
        if not cam.IsValid():
            # self.fmtr.print_error("No cameras found")
            print("Camera not available. Exiting...")
            return
        
        # get serial number
        device_serial_number: str = PySpin.CStringPtr(
            cam.GetTLDeviceNodeMap().GetNode("DeviceSerialNumber")
        ).GetValue()

        # get the current ip address
        current_ip_str: str = self.convert_ip_to_str(cam.GevPersistentIPAddress.GetValue())

        # perform forceIP
        # Init() not required for TL Force
        try:
            cam: PySpin.CameraPtr
            dev: PySpin.TransportLayerDevice = cam.TLDevice
            force: PySpin.ICommand = dev.GevDeviceAutoForceIP
            force.ImposeAccessMode(PySpin.RW)
            print(f"Forcing IP for cam {device_serial_number} on ip {current_ip_str}...")
            force.Execute(Verify=True)
        except PySpin.SpinnakerException as ex:
            print(f"Error - {ex}")

    def force_ip_by_cam_id(self, cam_id: str) -> None:
        """Force the IP on single PySPin camera by cam id."""

        # get the cams
        cams: PySpin.CameraList = self.system.GetCameras()

        # find the cam id
        cam: PySpin.CameraPtr = cams.GetBySerial(cam_id)

        # check cam is valid
        if not cam.IsValid():
            # self.fmtr.print_error("No cameras found")
            print("Camera not available. Exiting...")
            return

        # perform forceIP
        # Init() not required for TL Force
        try:
            cam: PySpin.CameraPtr
            dev: PySpin.TransportLayerDevice = cam.TLDevice
            force: PySpin.ICommand = dev.GevDeviceAutoForceIP
            force.ImposeAccessMode(PySpin.RW)
            print(f"Forcing IP for cam {cam_id}...")
            force.Execute(Verify=True)
        except PySpin.SpinnakerException as ex:
            print(f"Error - {ex}")

    def reset_all_cams(self) -> None:
        """Resets ALL the cameras in connected."""

        cams: PySpin.CameraList = self.system.GetCameras()

        # check there are cameras first
        if len(cams) == 0:
            # self.fmtr.print_error("No cameras found")
            print("No Cameras...")
            return

        print(f"Found {len(cams)} cameras...")

        # go through and reset
        for cam in cams:
            # cam pointer
            cam: PySpin.CameraPtr
            # init if not
            if not cam.IsInitialized():
                cam.Init()

            # get serial number
            device_serial_number: str = PySpin.CStringPtr(
                cam.GetTLDeviceNodeMap().GetNode("DeviceSerialNumber")
            ).GetValue()

            ret = None
            reset: PySpin.ICommand = cam.DeviceReset
            try:
                print("Forcing RW..")
                reset.ImposeAccessMode(PySpin.RW)
                print(f"Resetting cam {device_serial_number}...")
                ret = reset.Execute(Verify=True)
                print(ret)
            except PySpin.SpinnakerException as ex:
                print(f"Error - {ex}")

    def reset_cam(self, cam: PySpin.CameraPtr) -> None:
        """Resets a single cam via PySpin pointer."""

        # check cam is valid
        if not cam.IsValid():
            # self.fmtr.print_error("No cameras found")
            print("Camera not available. Exiting...")
            return

        # init if not
        if not cam.IsInitialized():
            cam.Init()

        # get serial number
        device_serial_number: str = PySpin.CStringPtr(
            cam.GetTLDeviceNodeMap().GetNode("DeviceSerialNumber")
        ).GetValue()

        # perform reset
        reset: PySpin.ICommand = cam.DeviceReset
        try:
            print("Forcing RW..")
            reset.ImposeAccessMode(PySpin.RW)

            print(f"Resetting cam {device_serial_number}...")
            reset.Execute(Verify=True)

        except PySpin.SpinnakerException as ex:
            print(f"Error - {ex}")

    def reset_cam_by_id(self, cam_id: str) -> None:
        """Resets a single cam via camera id."""

        # get the cams
        cams: PySpin.CameraList = self.system.GetCameras()

        # find the cam id
        cam: PySpin.CameraPtr = cams.GetBySerial(cam_id)

        # check cam is valid
        if not cam.IsValid():
            # self.fmtr.print_error("No cameras found")
            print("Camera not available. Skipping...")
            return

        # init if not
        if not cam.IsInitialized():
            cam.Init()

        # perform reset
        reset: PySpin.ICommand = cam.DeviceReset
        try:
            print("Forcing RW..")
            reset.ImposeAccessMode(PySpin.RW)

            print(f"Resetting cam {cam_id}...")
            reset.Execute(Verify=True)

        except PySpin.SpinnakerException as ex:
            print(f"Error - {ex}")
        # finally:
        #     del cam
        #     cams.Clear()
        #     del cams


    #########################
    ### CONVERT_IP_TO_STR ###
    #########################

    def convert_ip_to_str(self, ip: int) -> str:
        """Convert the ip address to a string."""

        return f"{ip >> 24 & 0xFF}.{ip >> 16 & 0xFF}.{ip >> 8 & 0xFF}.{ip & 0xFF}"


def main() -> None:
    """Main method."""

    # read config file
    with open("../config.yaml", encoding="utf-8") as f:
        config = yaml_load(f, Loader=FullLoader)

    cam_raceway_dict: dict[str, Any] = dict(config["cam_raceway_dict"])

    # PySpin system
    system: PySpin.System = PySpin.System.GetInstance()
    cams: PySpin.CameraList = system.GetCameras()

    # create reset object
    # needs to be same PySpin system
    # as main app ???
    cr = CamReset(system=system)

    ## RESET ALL CAMS 
    # cr.reset_all_cams()

    ## FORCE ALL CAMS
    # cr.force_all_ips()


    # INDIVIDUALLY - go through cams
    for cam_id, rw in cam_raceway_dict.items():
        # get a PySpin camera by id
        # cam: PySpin.CameraPtr = cams.GetBySerial(cam_id)
        
        ## RESET
        # cr.reset_cam(cam=cam)
        # cr.reset_cam_by_id(cam_id=cam_id)
    
        ## FORCE_IP
        # cr.force_ip_by_cam(cam=cam)
        cr.force_ip_by_cam_id(cam_id=cam_id)

        # if cam is created, delete it
        # del cam

    # cleanup
    cams.Clear()


if __name__ == "__main__":
    main()
