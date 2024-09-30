import asyncio
from connections.pubsub import Subscriber
from synapse.memory_manager.shared_memory_manager import SharedMemoryManager

async def handle_system_prompt(channel:str, key:str, version:int):
    ...

async def handle_user_prompt(channel:str, key:str, version:int):
    ...

async def handle_context_prompt(channel:str, key:str, version:int):
    ...