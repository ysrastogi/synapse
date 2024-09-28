import numpy as np
import torch
from typing import Union, Tuple, Dict, Any, List

from synapse.memory_manager.synchronization import SynchronizationService
from synapse.memory_manager.compression_service import CompressionService
from synapse.memory_manager.data_type_manager import DataTypeManager
from synapse.memory_manager.control import PartitioningService, VersionControl, AccessControl, MemoryAllocator
from synapse.memory_manager.file_manager import MemoryMappedFileManager
from synapse.memory_manager.cache_manager import CacheManager
from synapse.memory_manager.gpu_manager import GPUMemoryManager
from synapse.memory_manager.synchronization import DistributedLockManager
from connections.pubsub import Publisher

class SharedMemoryManager:
    def __init__(self, service_id: str, num_partitions: int, mmap_directory: str, cache_capacity: int, cache_expire_time:int, gpu_device_ids: List[int]):
        self.tensor_storage = {}
        self.vector_storage = {}
        self.metadata_store = {}
        self.text_storage = {}
        self.service_id = service_id
        self.version_control = VersionControl()
        self.compression_service = CompressionService()
        self.access_control = AccessControl()
        self.synchronization_service = SynchronizationService()
        self.memory_allocator = MemoryAllocator()
        self.data_type_manager = DataTypeManager()
        self.partitioning_service = PartitioningService(num_partitions)
        self.mmap_manager = MemoryMappedFileManager(mmap_directory)
        self.cache_manager = CacheManager(capacity=cache_capacity, expire_time=cache_expire_time)
        self.gpu_memory_manager = GPUMemoryManager(gpu_device_ids)
        self.distributed_lock_manager = DistributedLockManager()

    def store_text(self, key:str, text: str, metadata: Dict[str, Any] = None):
        with self.distributed_lock_manager.lock(key):
            compressed_text = self.compression_service.compress(text.encode('utf-8'))
            self.text_storage[key] = compressed_text
            self.metadata_store[key] = metadata or {}
            self.version_control.create_version(key)

    def retrieve_text(self, key:str, version:int = None) -> str:
        with self.distributed_lock_manager.lock(key):
            text_data = self.text_storage[key]
            if version is not None:
                text_data = self.version_control.get_version(key, version)
            else:
                text_data = self.version_control.get_latest_version(key)
            decompressed_text = self.compression_service.decompress(text_data)
            return decompressed_text.decode('utf-8')

    def store_tensor(self, key: str, tensor: Union[np.ndarray, torch.Tensor], metadata: Dict[str, Any] = None):
        with self.distributed_lock_manager.lock(key):
            if tensor.nbytes > self.cache_manager.capacity:
                self.mmap_manager.store_mmap(key, tensor)
            else:
                compressed_tensor = self.compression_service.compress(tensor)
                self.partitioning_service.store_partitioned(key, compressed_tensor)
                self.cache_manager.put(key, compressed_tensor)
            self.metadata_store[key] = metadata or {}
            stored_version = self.version_control.create_version(key)

    def retrieve_tensor(self, key: str, version: int = None) -> Union[np.ndarray, torch.Tensor]:
        with self.distributed_lock_manager.lock(key):
            cached_tensor = self.cache_manager.get(key)
            if cached_tensor is not None:
                tensor_data = cached_tensor
            else:
                try:
                    tensor_data = self.partitioning_service.retrieve_partitioned(key)
                except KeyError:
                    tensor_data = self.mmap_manager.retrieve_mmap(key)
            
            if version is not None:
                tensor_data = self.version_control.get_version(key, version)
            
            return self.compression_service.decompress(tensor_data)

    def store_vector(self, key:str, vector:Union[np.ndarray, torch.Tensor], metadata: Dict[str, Any] = None):
        vector_data = self.compression_service.compress(vector)
        self.vector_storage[key] = vector_data
        self.metadata_store[key] = metadata or {}
        self.version_control.create_version(key)
    
    
    def retrieve_vector(self, key:str, version:int =None) -> Union[np.ndarray, torch.Tensor]:
        vector_data = self.vector_storage[key]
        if version is not None:
            vector_data = self.version_control.get_version(key,version)
        return self.compression_service.decompress(vector_data)
    
    def update_tensor(self, key:str, tensor:Union[np.ndarray, torch.Tensor]):
        with self.synchronization_service.lock(key):
            self.store_tensor(key, tensor)
            self.version_control.create_version(key)

    def store_on_gpu(self, key: str, tensor: torch.Tensor, device_index: int):
        with self.distributed_lock_manager.lock(f"gpu:{key}"):
            self.gpu_memory_manager.store_on_gpu(key, tensor, device_index)

    def retrieve_from_gpu(self, key: str, device_index: int) -> torch.Tensor:
        with self.distributed_lock_manager.lock(f"gpu:{key}"):
            return self.gpu_memory_manager.retrieve_from_gpu(key, device_index)

    
    def get_metadata(self,key:str)-> Dict[str, Any]:
        return self.metadata_store[key]
    
    def set_metadata(self, key: str, metadata: Dict[str, Any]):
        self.metadata_store[key] = metadata