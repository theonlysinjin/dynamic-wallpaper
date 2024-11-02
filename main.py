import os
import platform
import sys
import requests
import logging
import argparse
import util
import win32serviceutil
import win32service

# Import the Windows service
if platform.system() == "Windows":
    import windows
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wallpaper Generator Service")
    parser.add_argument('--install', action='store_true', help='Install the Windows service')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the Windows service')
    parser.add_argument('--platform-check', action='store_true', help='Check the platform and exit')
    args = parser.parse_args()

    if not windows.is_admin():
        print("This script requires administrative privileges. Attempting to elevate...")
        windows.run_as_admin()
    else:
        # Your main code here
        print("Running with administrative privileges.")
        # ... existing code for installing the service ...

    if args.platform_check:
        logging.info(f"Platform check: {platform.system()}")
        sys.exit(0)

    if args.install and platform.system() == "Windows":
        logging.info("Installing Windows service...")
        try:
            win32serviceutil.InstallService(windows.WallpaperService, windows.WallpaperService._svc_name_, windows.WallpaperService._svc_display_name_)
            logging.info("Service installed successfully.")
        except Exception as e:
            logging.error(f"Failed to install service: {e}")
        sys.exit(0)

    if args.uninstall and platform.system() == "Windows":
        logging.info("Uninstalling Windows service...")
        try:
            win32serviceutil.UninstallService(windows.WallpaperService)
            logging.info("Service uninstalled successfully.")
        except Exception as e:
            logging.error(f"Failed to uninstall service: {e}")
        sys.exit(0)
