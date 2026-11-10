import sys
import pyudev
import time
import threading

context = pyudev.Context()

pendrives_cam = []
pendrives = {}

evento = threading.Event()

def verif_usb():

    while not evento.is_set():

        time.sleep(1)
    
        pendrives_cam_atu = []
        
        if sys.platform.startswith("win32"):
                print()
        elif sys.platform.startswith("linux"):
                for device in context.list_devices(subsystem="block"):
                        if device.find_parent("usb"):
                                pendrives_cam_atu.append(device.device_node)
                                if not device.device_node in pendrives_cam:
                                        pendrives_cam.append(device.device_node)
                                        pendrives["Label"] = device.properties.get("ID_FS_LABEL")
                                        pendrives["Caminho"] = device.properties.get("DEVNAME")
                                        pendrives["Modelo"] = device.properties.get("ID_MODEL")
                                        pendrives["Tamanho"] = device.attributes.get(attribute="size")
                                        

        for desativo in pendrives_cam:
                if not desativo in pendrives_cam_atu:
                        pendrives_cam.remove(desativo)
        
        print(pendrives)

def close():
   evento.set()