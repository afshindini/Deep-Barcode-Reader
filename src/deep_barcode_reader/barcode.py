"""Barcode detector and reader models"""

# pylint: disable=E1101
import logging
from typing import Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import cv2

from pyzbar.pyzbar import decode
from qreader import QReader

from .base import BarcodeBase, ReaderResults

logger = logging.getLogger(__name__)


@dataclass
class BarcodeOpencv(BarcodeBase):
    """This a simple 1D barcode reader using OpenCV. It can be used with
    EAN-8, EAN-13, UPC-A and UPC-E types of barcodes"""

    proto_file: Path = field(
        init=False, default=Path("./src/deep_barcode_reader/models/sr.prototxt")
    )
    model_file: Path = field(
        init=False, default=Path("./src/deep_barcode_reader/models/sr.caffemodel")
    )

    def __post_init__(self) -> None:
        """Post initialization of the barcode reader class"""
        if not self.model_file.exists():
            logger.error(
                "The model file does not exist for the BarcodeOpencv model. Please check the path."
            )
        if not self.proto_file.exists():
            logger.error(
                "The proto file does not exist for the BarcodeOpencv model. Please check the path."
            )

    async def detect_decode(self, image: Any) -> ReaderResults:
        """Detect and decode barcode method from an image"""
        result = ReaderResults(image=image)
        barcode_reader = cv2.barcode.BarcodeDetector(
            str(self.proto_file), str(self.model_file)
        )
        retval, decoded_info, barcode_types, boundary_boxs = (
            barcode_reader.detectAndDecodeWithType(image)
        )
        if retval:
            for idx, barc_txt in enumerate(decoded_info):
                if barc_txt:
                    result.decoded_data.append(barc_txt)
                    result.bbox_data.append(
                        np.array(boundary_boxs[idx], dtype=np.int32)
                    )
                    result.decoded_types.append(barcode_types[idx])
        if result.decoded_data:
            logger.info(
                "The barcode/qr code is detected and decoded successfully with BarcodeOpencv method."
            )
        else:
            logger.warning(
                "The barcode/qr code is not detected or decoded with BarcodeOpencv method."
            )

        return result


@dataclass
class BarcodeQRZbar(BarcodeBase):
    """This is a QR code and barcode reader using Zbar library"""

    async def detect_decode(self, image: Any) -> ReaderResults:
        """Detect and decode barcode/qr method from an image"""
        result = ReaderResults(image=image)
        decoder = decode(image)
        decoded_data = []
        decoded_types = []
        bbox_data = []
        if decoder:
            for decoded in decoder:
                if decoded.data.decode("utf-8"):
                    decoded_data.append(decoded.data.decode("utf-8"))
                    decoded_types.append(decoded.type)
                    bbox_data.append(np.array(decoded.polygon, np.int64))
        result.decoded_data = decoded_data
        result.decoded_types = decoded_types
        result.bbox_data = bbox_data
        if result.decoded_data:
            logger.info(
                "The barcode/qr code is detected and decoded successfully with BarcodeQRZbar method."
            )
        else:
            logger.warning(
                "The barcode/qr code is not detected or decoded with BarcodeQRZbar method."
            )
        return result


@dataclass
class QRreader(BarcodeBase):
    """This is a QR code reader using Qreader library"""

    model_size: str = field(default="l")

    async def detect_decode(self, image: Any) -> ReaderResults:
        """Detect and decode barcode/qr method from an image"""
        result = ReaderResults(image=image)
        qr_reader = QReader(model_size=self.model_size)
        detections = qr_reader.detect(image=image)
        decoded_data = []
        decoded_types = []
        bbox_data = []
        if detections:
            for detection in detections:
                decoded_text = qr_reader.decode(image, detection)
                if decoded_text:
                    decoded_data.append(decoded_text)
                    decoded_types.append("QR")
                    bbox_data.append(np.array(detection["polygon_xy"], np.int64))
            if decoded_data:
                result.decoded_data = decoded_data
                result.decoded_types = decoded_types
                result.bbox_data = bbox_data
                logger.info(
                    "The barcode/qr code is detected and decoded successfully with QRreader method."
                )
            else:
                logger.warning(
                    "The barcode/qr code is not detected or decoded with QRreader method."
                )
        else:
            logger.warning("The barcode/qr code is not detected with QRreader method.")

        return result


@dataclass
class Wrapper:
    """Wrapper class for barcode readers"""

    method: str = field(default="opencv")
    model_size: str = field(default="l")

    async def method_selection(self, image: Any, result_path: str) -> Tuple[Any, Any]:
        """Wrap the method selection for barcode reader"""
        if self.method == "opencv":
            barcode: Any = BarcodeOpencv()
        elif self.method == "zbar":
            barcode = BarcodeQRZbar()
        elif self.method == "qrreader":
            barcode = QRreader(model_size=self.model_size)
        else:
            barcode = BarcodeOpencv()
        detections = await barcode.detect_decode(image)
        result_image = await detections.visualize_results_async(result_path)
        return detections, result_image
