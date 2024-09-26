import torch
from typing import List

class GPUMemoryManager:
    def __init__(self, device_ids: List[int]):
        self.devices = [torch.device(f'cuda:{i}') for i in device_ids]
        self.gpu_storage = {device: {} for device in self.devices}

    def store_on_gpu(self, key: str, tensor: torch.Tensor, device_index: int):
        device = self.devices[device_index]
        self.gpu_storage[device][key] = tensor.to(device)

    def retrieve_from_gpu(self, key: str, device_index: int) -> torch.Tensor:
        device = self.devices[device_index]
        return self.gpu_storage[device][key]

    def update_on_gpu(self, key: str, new_tensor: torch.Tensor, device_index: int):
        device = self.devices[device_index]
        self.gpu_storage[device][key] = new_tensor.to(device)

    def clear_gpu_memory(self, device_index: int):
        device = self.devices[device_index]
        self.gpu_storage[device].clear()
        torch.cuda.empty_cache()