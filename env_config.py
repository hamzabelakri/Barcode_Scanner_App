import os
from dotenv import load_dotenv

load_dotenv('.env') 


BACK_APP_API_URL = os.getenv("BACK_APP_API_URL", "http://127.0.0.1/")
BACK_APP_API_PORT = os.getenv("BACK_APP_API_PORT", "8000")
BACK_APP_API_ENDPOINT = os.getenv("BACK_APP_API_ENDPOINT", "consult_ticket")

BARCODE_SERIAL_PORT = os.getenv("BARCODE_SERIAL_PORT", "/dev/scanner")
BARCODE_SERIAL_BAUDRATE = int(os.getenv("BARCODE_SERIAL_BAUDRATE", 115200))

TICKET_TYPE = os.getenv("TICKET_TYPE", "barcode")
TICKET_TARIFF_CLASS = int(os.getenv("TICKET_TARIFF_CLASS", 0))

