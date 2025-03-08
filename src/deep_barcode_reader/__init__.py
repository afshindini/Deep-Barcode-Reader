""" It can read different types of barcodes """

__version__ = "0.3.0"

from .barcode import Wrapper, QRreader, BarcodeOpencv, BarcodeQRZbar
from .base import ReaderResults

__all__ = [
    "Wrapper",
    "QRreader",
    "BarcodeOpencv",
    "BarcodeQRZbar",
    "ReaderResults",
]
