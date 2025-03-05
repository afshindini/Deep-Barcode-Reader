"""Run the main code for Deep-Barcode-Reader"""

# pylint: disable=E1101
from pathlib import Path
import logging
import asyncio
import click
import cv2


from deep_barcode_reader import __version__
from deep_barcode_reader.logging import config_logger
from deep_barcode_reader.barcode import Wrapper

logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Shorthand for info/debug/warning/error loglevel (-v/-vv/-vvv/-vvvv)",
)
@click.option(
    "-s",
    "--result_path",
    type=str,
    default="output/test.png",
    help="Path to save the result file.",
)
@click.option(
    "-d",
    "--data_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to data file.",
)
@click.option(
    "-m",
    "--method",
    type=click.Choice(["opencv", "zbar", "qrreader"], case_sensitive=False),
    default="opencv",
    help="Path to data file.",
)
@click.option(
    "--model_size",
    type=click.Choice(["n", "s", "m", "l"], case_sensitive=False),
    default="m",
    help="Model size for the barcode reader.",
)
def deep_barcode_reader_cli(
    verbose: int, result_path: str, data_path: Path, method: str, model_size: str
) -> None:
    """It can read different types of barcodes"""
    if verbose == 1:
        log_level = 10
    elif verbose == 2:
        log_level = 20
    elif verbose == 3:
        log_level = 30
    else:
        log_level = 40
    config_logger(log_level)

    reader = Wrapper(model_size=model_size, method=method)
    _ = asyncio.get_event_loop().run_until_complete(
        reader.method_selection(
            image=cv2.imread(str(data_path)), result_path=result_path
        )
    )
