import sys
import pyudev
import time
import threading
from src.meowflash import interface
             
context = pyudev.Context()
loop = threading.Event()

def close():
    loop.set()

pendrives = []

def monitor_usb():
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    while not loop.is_set():
        device = monitor.poll(timeout=1)

        if device is None:
               continue
        
        if device.action == "add":
                if device.find_parent("usb"):
                
                        if device.device_type == "partition":
                                for sn in pendrives:
                                        if sn["Número de Série"] == device.properties.get("ID_SERIAL_SHORT"):
                                                particao = {}
                                                particao["Label"] = device.properties.get("ID_FS_LABEL")
                                                particao["Sistema de arquivos"] = device.properties.get("ID_FS_TYPE")

                                                tamanhop = int(device.attributes.get("size", 0))
                                                tamanhop_cont = (tamanhop * 512) / (1024 ** 3) 
                                                tamanhop_formatado = int(tamanhop_cont)
                                                particao["Tamanho"] = tamanhop_formatado

                                                particao["Caminho"] = device.properties.get("DEVNAME")

                                                sn["Partições"].append(particao)

                        elif device.device_type == "disk":

                                if len(pendrives) == 0:
                                        device_atual = {}
                                        device_atual["Modelo"] = device.properties.get("ID_MODEL")
                                        device_atual["Fabricante"] = device.get("ID_VENDOR")
                                        device_atual["Número de Série"] = device.properties.get("ID_SERIAL_SHORT")
                                       
                                        tamanho = int(device.attributes.get("size", 0))
                                        tamanho_cont = (tamanho * 512) / (1024 ** 3)
                                        tamanho_formatado = int(tamanho_cont)
                                        device_atual["Tamanho"] = f"{tamanho_formatado}GB"
                                       
                                        device_atual["Caminho"] = device.properties.get("DEVNAME")
                                        device_atual["Partições"] = []
                                       
                                        pendrives.append(device_atual)
                                        interface.criar_aba(device_atual)
                                       
                                for pendrive in pendrives:
                                        if not device.properties.get("ID_SERIAL_SHORT") in pendrive["Número de Série"]:
                                                device_atual = {}
                                                device_atual["Modelo"] = device.properties.get("ID_MODEL")
                                                device_atual["Fabricante"] = device.get("ID_VENDOR")
                                                device_atual["Número de Série"] = device.properties.get("ID_SERIAL_SHORT")

                                                tamanho = int(device.attributes.get("size", 0))
                                                tamanho_formatado = (tamanho * 512) / (1024 ** 3)
                                                device_atual["Tamanho"] = tamanho_formatado

                                                device_atual["Caminho"] = device.properties.get("DEVNAME")
                                                device_atual["Partições"] = []

                                                pendrives.append(device_atual)

                                                interface.criar_aba(device_atual)

                        print(pendrives)

        elif device.action == "remove":
               if device.find_parent("usb"):
                      if device.device_type == "disk":
                        for pendriverm in pendrives:
                                if pendriverm["Número de Série"] == device.properties.get("ID_SERIAL_SHORT"):
                                        pendrives.remove(pendriverm)
                                        interface.excluir_aba(pendriverm["Modelo"])

               print(pendrives)

                             