"""Data Contracts between UI, Core, and AI Modules.

Specification strictly adheres to Section 6.1 in 'Tài liệu kỹ thuật project AI':
GenerationResult(success, glb_path, message, inference_time, is_mock).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GenerationResult:
    """Standardized result contract returned by 3D generation pipelines.

    Attributes:
        success: True if generation succeeded, False otherwise.
        glb_path: File path to the generated or mock .glb file on local disk (None if failed).
        message: Informational or error message in Vietnamese for UI display.
        inference_time: Elapsed processing time in seconds.
        is_mock: Clear indicator of whether this result came from mock mode (True) or real AI (False).
    """

    success: bool
    glb_path: Optional[str]
    message: str
    inference_time: float
    is_mock: bool = False
