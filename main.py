import threading
from src.meowflash.interface import ini_interface
from src.meowflash.hardware import verif_usb

def main():

    threading.Thread(target=ini_interface).start()
    threading.Thread(target=verif_usb).start()

if __name__ == "__main__":
    main()