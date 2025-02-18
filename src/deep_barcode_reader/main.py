"""Run the main code for Deep-Barcode-Reader"""
from pathlib import Path
import logging
import asyncio
import click
import cv2

from deep_barcode_reader import __version__
from deep_barcode_reader.logging import config_logger
from deep_barcode_reader.barcode import BarcodeOpencv, BarcodeQRZbar

logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug/warning/error loglevel (-v/-vv/-vvv/-vvvv)")
@click.option("-s", "--result_path", type=click.Path(), default=Path("output"), help="Path to save the result file.")
@click.option("-d", "--data_path", required=True, type=click.Path(exists=True), help="Path to data file.")
@click.option("--model_size", type=click.Choice(["n", "s", "m", "l"], case_sensitive=False), help="Path to data file.")
def deep_barcode_reader_cli(verbose: int, result_path: Path, data_path: Path, model_size: str) -> None:
    """It can read different types of barcodes """
    if verbose == 1:
        log_level = 10
    elif verbose == 2:
        log_level = 20
    elif verbose == 3:
        log_level = 30
    else:
        log_level = 40
    config_logger(log_level)

    click.echo("Run the main code.")
    barcode = BarcodeQRZbar()
    _ = asyncio.get_event_loop().run_until_complete(barcode.test_run())
