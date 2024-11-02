import win32serviceutil
import win32service
import win32event
import servicemanager
import ctypes
import logging
import os
import platform
import util
import sys

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrative privileges."""    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def set_wallpaper(image_path):
    logging.debug(f"Setting wallpaper to {image_path}")
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    if result:
        logging.info("Wallpaper set successfully.")
    else:
        logging.error("Failed to set wallpaper.")


class WallpaperService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WallpaperGeneratorService"
    _svc_display_name_ = "Wallpaper Generator Service"
    _svc_description_ = "A service that downloads and sets wallpapers."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                               servicemanager.PYS_SERVICE_STARTED,
                               (self._svc_name_, ''))
        self.main()

    def main(self):
        logging.info("Running wallpaper generator service...")
        
        image_url = "https://github.com/theonlysinjin/wallpaper-generator/releases/download/generate%2F24-10-27-16/Cape.Town.png"
        image_path = os.path.join(os.path.expanduser("~"), "Cape.Town.png")
        util.download_image(image_url, image_path)

        if platform.system() == "Windows":
            logging.info("Setting Windows Wallpaper: %s", image_path)
            set_wallpaper(image_path)

# Entry point for the service
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WallpaperService)
