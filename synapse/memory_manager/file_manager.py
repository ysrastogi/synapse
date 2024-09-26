import numpy as np
import os

class MemoryMappedFileManager:
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def store_mmap(self, key: str, data: np.ndarray):
        filename = os.path.join(self.directory, f"{key}.mmap")
        mmap_file = np.memmap(filename, dtype=data.dtype, mode='w+', shape=data.shape)
        mmap_file[:] = data[:]
        mmap_file.flush()

    def retrieve_mmap(self, key: str) -> np.memmap:
        filename = os.path.join(self.directory, f"{key}.mmap")
        mmap_file = np.memmap(filename, dtype=np.float32, mode='r')
        return mmap_file

    def update_mmap(self, key: str, new_data: np.ndarray):
        filename = os.path.join(self.directory, f"{key}.mmap")
        mmap_file = np.memmap(filename, dtype=new_data.dtype, mode='r+', shape=new_data.shape)
        mmap_file[:] = new_data[:]
        mmap_file.flush()