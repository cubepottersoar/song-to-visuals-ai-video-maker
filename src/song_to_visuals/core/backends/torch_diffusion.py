"""CUDA/ROCm diffusion backend via torch + diffusers."""
from __future__ import annotations

from song_to_visuals.core.backend import VisualBackend
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class TorchDiffusionBackend(VisualBackend):
    name = "cuda"

    def __init__(self, device: str = "cuda", fp16: bool = True) -> None:
        self.device = device
        self.fp16 = fp16
        self._pipe = None

    def warmup(self) -> None:
        import torch
        from diffusers import StableDiffusionPipeline

        dtype = torch.float16 if self.fp16 else torch.float32
        self._pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
        ).to(self.device)
        self._pipe.set_progress_bar_config(disable=True)
        log.info("torch backend warm device=%s fp16=%s", self.device, self.fp16)

    def render_frame(self, prompt, seed, size, strength):
        assert self._pipe is not None, "warmup() not called"
        import torch

        gen = torch.Generator(device=self.device).manual_seed(seed)
        img = self._pipe(
            prompt, height=size[1], width=size[0], num_inference_steps=24, generator=gen
        ).images[0]
        return img

    def close(self) -> None:
        self._pipe = None