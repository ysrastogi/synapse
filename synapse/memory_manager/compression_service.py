import numpy as np
import torch
import zlib
from typing import Union

class CompressionService:
    def compress(self, data: Union[np.ndarray, torch.Tensor]) -> bytes:
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        return zlib.compress(data.tobytes())
    
    def decompress(self, compressed_data: bytes) -> np.ndarray:
        return np.frombuffer(zlib.decompress(compressed_data), dtype=np.float32)