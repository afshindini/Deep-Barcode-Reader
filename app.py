"""This is a demo for running the barcode QR code reader usng streamlit library"""

from dataclasses import dataclass, field
from typing import Any, Optional
import asyncio

import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

from src.deep_barcode_reader.barcode import Wrapper


@dataclass
class DemoBarcodeReader:
    """This is a demo class for barcode/qr code reader using different methods"""

    image: Optional[Any] = field(init=False, default=None)
    model_option: str = field(init=False, default="opencv")
    model_size: str = field(init=False, default="n")

    def upload_image(self) -> None:
        """Upload an image from the streamlit page"""
        uploaded_file = st.file_uploader(
            "Choose an image...", type=["jpg", "png", "jpeg"]
        )
        if uploaded_file is not None:
            self.image = Image.open(uploaded_file)
        else:
            self.image = Image.open("tests/test_data/sample.jpg")

        st.image(
            self.image, caption="Original/Uploaded Image", use_container_width=True
        )

    def select_model(self) -> None:
        """Select a model for barcode/qr code reader"""
        self.model_option = st.selectbox(
            "Choose a reader/decoder model", ["zbar", "opencv", "qrreader"]
        )
        if self.model_option == "qrreader":
            ml_size = st.selectbox(
                "Choose a model size for QRReader method",
                ["nano", "small", "medium", "large"],
            )
            self.model_size = (
                "n"
                if ml_size == "nano"
                else "s" if ml_size == "small" else "m" if ml_size == "medium" else "l"
            )

    def process_image(self) -> None:
        """Process the image for barcode/qr code reader"""
        if st.button("Read/Decode Barcode/QR Code"):
            reader = Wrapper(model_size=self.model_size, method=self.model_option)
            detections, result_img = asyncio.run(
                reader.method_selection(image=np.array(self.image), result_path="")
            )
            st.markdown("<h3>Detected Results</h3>", unsafe_allow_html=True)
            st.image(result_img, caption="Decoded Result", use_container_width=True)
            results = pd.DataFrame(
                {
                    "Barcode/QR Types": detections.decoded_types,
                    "Data": detections.decoded_data,
                    "Boundary Box": [str(bbx) for bbx in detections.bbox_data],
                }
            )
            st.markdown('<div class="center-container">', unsafe_allow_html=True)
            st.markdown(
                "<h3>Detailed Information of Detections</h3>", unsafe_allow_html=True
            )
            st.table(results)
            st.markdown("</div>", unsafe_allow_html=True)

    def design_page(self) -> None:
        """Design the streamlit page for barcode/qr code reader"""
        st.title("Image Barcode/QR Code Reader and Detector")
        self.upload_image()
        self.select_model()
        self.process_image()


demo = DemoBarcodeReader()
demo.design_page()
