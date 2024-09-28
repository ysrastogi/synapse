import numpy as np
import torch
import zlib
from typing import Union

class CompressionService:
    def compress(self, data: Union[np.ndarray, torch.Tensor, bytes]) -> bytes:
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        if isinstance(data, np.ndarray):
            data = data.tobytes()
        return zlib.compress(data)
    
    def decompress(self, compressed_data: bytes) -> Union[np.ndarray, bytes]:
        if not isinstance(compressed_data, bytes):
            raise TypeError("compressed_data must be of type bytes")
        
        decompressed_data = zlib.decompress(compressed_data)
        try:
            return np.frombuffer(decompressed_data, dtype=np.float32)
        except ValueError:
            return decompressed_data