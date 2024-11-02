import logging
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def download_image(url, save_path):
    logging.debug(f"Attempting to download image from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Image downloaded and saved to {save_path}")
    else:
        logging.error("Failed to download image. Status code: %s", response.status_code)
