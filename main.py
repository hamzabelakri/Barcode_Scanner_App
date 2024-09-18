import serial
import json
import requests
from env_config import (
    BACK_APP_API_URL,
    BACK_APP_API_PORT,
    BACK_APP_API_ENDPOINT,
    BARCODE_SERIAL_PORT,
    BARCODE_SERIAL_BAUDRATE,
    TICKET_TYPE,
    TICKET_TARIFF_CLASS
)
from loguru import logger
import base64
import os
from typing import Optional


logger.add("barcode_scanner.log", rotation="1 day")
logger.info(f"Configuration values: BACK_APP_API: {BACK_APP_API_URL}:{BACK_APP_API_PORT}, "
            f"BARCODE_SERIAL_PORT: {BARCODE_SERIAL_PORT}, BARCODE_SERIAL_BAUDRATE: {BARCODE_SERIAL_BAUDRATE}")


ICON_PATH = "barcode-icon.png"

def load_icon_as_base64(icon_path: str) -> Optional[str]:
    """Load and encode the icon file as base64."""
    if not os.path.exists(icon_path):
        logger.error(f"Icon file does not exist: {icon_path}")
        return None
    
    try:
        with open(icon_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        logger.error(f"Failed to load image from path '{icon_path}'. Error: {e}")
        return None
    

def send_to_api(valid_barcode: str, icon_base64: Optional[str]) -> None:

    data = {
        "ticket_type": TICKET_TYPE,
        "LPN": valid_barcode,
        "epan": "",
        "bar_code": valid_barcode,
        "image": icon_base64,
        "tariff_class": TICKET_TARIFF_CLASS
    }
    
    data_for_logging = {k: v for k, v in data.items() if k != "image"}
    
    api_url = f"{BACK_APP_API_URL}:{BACK_APP_API_PORT}/{BACK_APP_API_ENDPOINT}"
    logger.info(f"Sending request to API endpoint: {api_url}")
    logger.debug(f"Request payload: {json.dumps(data_for_logging, indent=4)}")
    
    try:
        response = requests.post(api_url, json=data, timeout=5)
        response.raise_for_status()
        logger.info(f"Data sent successfully. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data to API: {e}")


icon_base64 = load_icon_as_base64(ICON_PATH)


try:
    with serial.Serial(BARCODE_SERIAL_PORT, baudrate=BARCODE_SERIAL_BAUDRATE) as ser:
        logger.info(f"Successfully connected to serial port '{BARCODE_SERIAL_PORT}' "
                    f"with baud rate {BARCODE_SERIAL_BAUDRATE}. Waiting for barcode messages...")
        
        while True:
            raw_barcode = ser.read_until(expected=b'\r')
            valid_barcode = raw_barcode.rstrip(b'\r').decode('utf-8')
            logger.debug(f"Received Raw Barcode: {raw_barcode}/ Length: {len(raw_barcode)} / Valid Barcode: {valid_barcode}")
            send_to_api(valid_barcode, icon_base64)

except serial.SerialException as e:
    logger.error(f"Error connecting to serial port: {e}")
except KeyboardInterrupt:
    logger.info("Program terminated by user.")
except Exception as e:
    logger.error(f"Unexpected error: {e}")