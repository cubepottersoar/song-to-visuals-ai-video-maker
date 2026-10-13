"""CPU diffusion backend via onnxruntime."""
from __future__ import annotations

from song_to_visuals.core.backend import VisualBackend
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class OnnxDiffusionBackend(VisualBackend):
    name = "cpu"

    def __init__(self, device: str = "cpu", threads: int = 8) -> None:
        self.device = device
        self.threads = threads
        self._sess = None

    def warmup(self) -> None:
        import onnxruntime as ort

        opts = ort.SessionOptions()
        opts.intra_op_num_threads = self.threads
        self._sess = ort.InferenceSession("models/sd15.onnx", sess_options=opts)
        log.info("onnx backend warm threads=%d", self.threads)

    def render_frame(self, prompt, seed, size, strength):
        raise NotImplementedError("onnx decoder post-processing lands in 0.5")

    def close(self) -> None:
        self._sess = None