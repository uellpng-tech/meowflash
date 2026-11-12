import sys
import pyudev
import time
import threading
from src.meowflash import interface

context = pyudev.Context()

pendrives_cam = []
pendrives = []

evento = threading.Event()


def aba_pendrive(criar=True, remover=None):
       if criar:
           interface.criar_aba(pendrives)
       else:
           interface.excluir_aba(remover)
             

def verif_usb():
    global pendrives

    while not evento.is_set():

        time.sleep(1)
    
        pendrives_cam_atu = []
        
        if sys.platform.startswith("win32"):
                print()
        elif sys.platform.startswith("linux"):
                for device in context.list_devices(subsystem="block", DEVTYPE="disk"):
                        if device.find_parent("usb"):
                                pendrives_cam_atu.append(device.device_node)
                                if not device.device_node in pendrives_cam:
                                        pendrives_cam.append(device.device_node)
                                        pendrivesdic = {}
                                        pendrivesdic["Label"] = device.properties.get("ID_FS_LABEL")
                                        pendrivesdic["Caminho"] = device.properties.get("DEVNAME")
                                        pendrivesdic["Modelo"] = device.properties.get("ID_MODEL")
                                        pendrivesdic["Tamanho"] = device.attributes.get(attribute="size").decode('utf-8')
                                        pendrivesdic["Modo"] = device.attributes.get(attribute="ro")
                                        pendrives.append(pendrivesdic)
                                        aba_pendrive()
                                        

        for desativoc in pendrives_cam:
                if not desativoc in pendrives_cam_atu:
                        pendrives_cam.remove(desativoc)

        for desativo in pendrives:
               if not desativo["Caminho"] in pendrives_cam_atu:
                      aba_pendrive(criar=False, remover=desativo["Label"])
                      pendrives.remove(desativo)

               
                      
        print(pendrives)

def close():
   evento.set()