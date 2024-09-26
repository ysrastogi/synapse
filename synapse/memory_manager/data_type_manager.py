import numpy as np
import torch
from typing import Union

class DataTypeManager:
    def __init__(self):
        self.dtype_map = {
            'float32': np.float32,
            'float64': np.float64,
            'int32': np.int32,
            'int64': np.int64,
            'float16': np.float16
        }
    
    def get_numpy_dtype(self, dtype_str: str):
        return self.dtype_map.get(dtype_str, np.float32)
    
    def get_torch_dtype(self, dtype_str:str):
        return getattr(torch, dtype_str)
    
    def convert_dtype(self, data: Union[np.ndarray, torch.Tensor], dtype_str: str):
        if isinstance(data, np.ndarray):
            return data.astype(self.get_numpy_dtype(dtype_str))
        elif isinstance(data, torch.Tensor):
            return data.to(self.get_torch_dtype(dtype_str))
        else:
            raise ValueError("Unsupported data type")