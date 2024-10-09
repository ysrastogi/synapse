import asyncio
from connections.pubsub import Subsciber
from synapse.memory_manager.shared_memory_manager import SharedMemoryManager

async def handle_prompt(channel:str, key:str, version:int):
    """
    Handle user message input.
    :param channel: The channel of the input
    """
    listener = Subsciber(channel)
    while True:
        message = await listener.listen()
        if message == "Prompt is Ready":
            storage = SharedMemoryManager(service_id=channel)
            prompt = storage.retrieve_text(key, version)
            return prompt
        asyncio.sleep(0.1)
    

async def handle_tools(channel:str, key:str, version:int):
    """
    Handle tools input.
    :param channel: The channel of the input
    """
    # Process the tools data
    ...

async def handle_functions(channel:str, key:str, version:int):
    """
    Handle functions input.
    :param channel: The channel of the input
    """
    # Process the functions data
    ...