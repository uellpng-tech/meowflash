import threading
from src.meowflash.interface import ini_interface
from src.meowflash.hardware import monitor_usb

def main():

    threading.Thread(target=ini_interface).start()
    threading.Thread(target=monitor_usb).start()

if __name__ == "__main__":
    main()