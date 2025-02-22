"""This is the base class for implementing barcode reader and decoder models"""

# pylint: disable=E1101
import logging
from typing import Any, List, Optional
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import cv2


logger = logging.getLogger(__name__)


@dataclass
class BarcodeBase(ABC):
    """This is the base class for implementing different methods of barcode/qr code reading and decoding"""

    @abstractmethod
    async def detect_decode(self, image: Any) -> Any:
        """Detect and decode barcode/qr method from an image"""
        raise NotImplementedError()


@dataclass
class ReaderResults:
    """Dataclass for saving/visualizing barcode/qr code reader results"""

    image: Any
    decoded_data: List[str] = field(default_factory=list)
    decoded_types: List[str] = field(default_factory=list)
    bbox_data: List[Any] = field(default_factory=list)

    def save_image(self, img: Any, file_name: str = "") -> None:
        """Save the image to the output path for debugging"""
        if file_name != "":
            Path(file_name).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(file_name, img)
            logger.info("Image is saved to %s", file_name)

    async def visualize_results_async(self, file_name: str) -> Optional[Any]:
        """Visualize the results of the barcode/qr code reader"""
        if self.image is None:
            logger.error(
                "The image is not provided as the image is not loaded properly or does not exist."
            )
            return None
        img_bounding_box = self.image.copy()
        if self.decoded_data is not None and self.bbox_data is not None:
            for data, bbox in zip(self.decoded_data, self.bbox_data):
                cv2.polylines(
                    img_bounding_box,
                    [bbox],
                    isClosed=True,
                    color=(0, 0, 255),
                    thickness=1,
                )
                cv2.putText(
                    img_bounding_box,
                    str(data),
                    (int(bbox[0][0]) - 10, int(bbox[0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                )

        self.save_image(img_bounding_box, file_name)
        return img_bounding_box
