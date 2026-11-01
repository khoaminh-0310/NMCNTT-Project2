import logging
import shutil
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from pathlib import Path

from src.ai.mock_service import run_mock_inference
from src.core.file_manager import generate_output_path


_SPACE_ID = "microsoft/TRELLIS"
_API_NAME = "/generate_and_extract_glb"
_REQUEST_TIMEOUT_SECONDS = 120
_LOGGER = logging.getLogger(__name__)


def _predict(image_path: str) -> object:
    from gradio_client import Client

    client = Client(_SPACE_ID, hf_token=os.getenv("HF_TOKEN"), verbose=False)
    return client.predict(image_path, api_name=_API_NAME)


def _predict_with_timeout(image_path: str) -> object:
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_predict, image_path)
    try:
        return future.result(timeout=_REQUEST_TIMEOUT_SECONDS)
    except FutureTimeoutError as exc:
        future.cancel()
        raise TimeoutError(
            f"TRELLIS inference exceeded {_REQUEST_TIMEOUT_SECONDS} seconds"
        ) from exc
    finally:
        executor.shutdown(wait=False)


def _glb_path_from_result(result: object) -> Path:
    if isinstance(result, (list, tuple)):
        if not result:
            raise ValueError("TRELLIS returned no outputs")
        result = result[-1]

    if isinstance(result, dict):
        result = result.get("path")

    if not isinstance(result, str) or not result:
        raise TypeError("TRELLIS did not return a local GLB file path")

    path = Path(result)
    if not path.is_file():
        raise FileNotFoundError(f"TRELLIS output file was not found: {path}")
    return path


def run_inference(image_path: str) -> tuple[str, bool]:
    try:
        result = _predict_with_timeout(image_path)
        source_path = _glb_path_from_result(result)
        output_path = Path(generate_output_path("trellis_result.glb"))
        shutil.copyfile(source_path, output_path)
        return str(output_path), False
    except Exception:
        _LOGGER.exception("TRELLIS inference failed; using the mock model instead")
        return run_mock_inference(image_path)
