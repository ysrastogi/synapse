import asyncio
from connections.pubsub import Subscriber
from components.prompts.constant import PromptPartType
from synapse.memory_manager.shared_memory_manager import SharedMemoryManager

async def handle_system_prompt(system_prompt:str):
    return system_prompt

async def handle_user_prompt(user_prompt:str):
    return user_prompt

async def handle_context_prompt(channel:str, key:str, version:int):
    listerner = Subscriber(channel)
    while True:
        message = await listerner.listen()
        if message == "Context is Ready":
            storage = SharedMemoryManager(service_id=channel)
            context = storage.retrieve_text(key, version)
            return context
        await asyncio.sleep(0.1)