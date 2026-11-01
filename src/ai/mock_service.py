import shutil
import time
from pathlib import Path

from src.core.file_manager import generate_output_path


_SAMPLE_MODEL = Path(__file__).resolve().parents[2] / "assets" / "sample_model.glb"


def run_mock_inference(image_path: str) -> tuple[str, bool]:
    time.sleep(1.5)
    output_path = generate_output_path("mock_result.glb")
    shutil.copyfile(_SAMPLE_MODEL, output_path)
    return output_path, True
