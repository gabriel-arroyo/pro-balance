from pyzbar.pyzbar import decode
# from PIL import Image
import cv2
import pandas as pd

# Function to decode barcodes


def extract_barcodes(image_path):
    img = cv2.imread(image_path)
    barcodes = decode(img)
    barcode_data = [barcode.data.decode('utf-8') for barcode in barcodes]
    return barcode_data


# def process_barcode(image_path):
#     img = Image.open(image_path)
#     barcode = decode(img)
#     return barcode[0].data.decode('utf-8') if barcode else None
