import logging
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from pathlib import Path

from src.ai.mock_service import run_mock_inference
from src.core.contracts import GenerationResult
from src.core.file_manager import generate_output_path


_SPACE_ID = os.getenv("HF_SPACE_ID", "microsoft/TRELLIS.2")
_API_NAME = "/generate_and_extract_glb"
_REQUEST_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "180"))
_LOGGER = logging.getLogger(__name__)


def _predict(image_path: str) -> object:
    from gradio_client import Client, handle_file

    space_id = os.getenv("HF_SPACE_ID", _SPACE_ID)
    token = os.getenv("HF_TOKEN")
    client = Client(space_id, token=token, verbose=False)

    named_endpoints = {
        getattr(e, "api_name", None) for e in client.endpoints.values()
    }

    if _API_NAME in named_endpoints:
        return client.predict(handle_file(image_path), api_name=_API_NAME)

    if "/extract_glb" in named_endpoints and "/preprocess_image" in named_endpoints:
        preprocessed = client.predict(
            input=handle_file(image_path),
            api_name="/preprocess_image",
        )
        client.predict(
            image=handle_file(preprocessed),
            seed=0,
            resolution="1024",
            ss_guidance_strength=7.5,
            ss_guidance_rescale=0.7,
            ss_sampling_steps=12,
            ss_rescale_t=5.0,
            shape_slat_guidance_strength=7.5,
            shape_slat_guidance_rescale=0.5,
            shape_slat_sampling_steps=12,
            shape_slat_rescale_t=3.0,
            tex_slat_guidance_strength=1.0,
            tex_slat_guidance_rescale=0.0,
            tex_slat_sampling_steps=12,
            tex_slat_rescale_t=3.0,
            api_name="/image_to_3d",
        )
        return client.predict(
            decimation_target=300000,
            texture_size=2048,
            api_name="/extract_glb",
        )

    return client.predict(handle_file(image_path))


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
    """Execute 3D reconstruction inference with automatic fallback to mock."""
    try:
        result = _predict_with_timeout(image_path)
        source_path = _glb_path_from_result(result)
        output_path = Path(generate_output_path("trellis_result.glb"))
        shutil.copyfile(source_path, output_path)
        return str(output_path), False
    except Exception:
        _LOGGER.exception("TRELLIS inference failed; using the mock model instead")
        return run_mock_inference(image_path)


def generate_3d_from_image(image_path: str) -> GenerationResult:
    """Generate 3D model from image, returning standardized GenerationResult.

    Adheres strictly to Technical Contract in Section 6.1 of the Technical Playbook.
    """
    start_time = time.time()
    try:
        glb_path, is_mock = run_inference(image_path)
        elapsed = round(time.time() - start_time, 2)

        if not glb_path or not os.path.exists(glb_path):
            return GenerationResult(
                success=False,
                glb_path=None,
                message="Không thể tạo hoặc tìm thấy file mô hình 3D (.glb).",
                inference_time=elapsed,
                is_mock=is_mock,
            )

        if is_mock:
            message = "Đã tải xong mô hình bằng dữ liệu mẫu cục bộ (Mock Mode)."
        else:
            message = "Tạo mô hình 3D từ AI TRELLIS thành công."

        return GenerationResult(
            success=True,
            glb_path=glb_path,
            message=message,
            inference_time=elapsed,
            is_mock=is_mock,
        )
    except Exception as exc:
        elapsed = round(time.time() - start_time, 2)
        _LOGGER.exception("Unexpected error in generate_3d_from_image: %s", exc)
        return GenerationResult(
            success=False,
            glb_path=None,
            message=f"Lỗi hệ thống khi tạo mô hình 3D: {str(exc)}",
            inference_time=elapsed,
            is_mock=False,
        )
