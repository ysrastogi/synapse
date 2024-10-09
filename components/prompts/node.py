import asyncio
from typing import Dict, Any, List

from components.prompts.constant import PromptPartType
from connections.nodes.base import NodeBase
from connections.pubsub import Publisher
from components.prompts.constant import InputType
from components.prompts.handlers import handle_context_prompt, handle_system_prompt, handle_user_prompt
from components.prompts.processor import processor
from synapse.memory_manager.shared_memory_manager import SharedMemoryManager

class PromptNode(NodeBase):
    def __init__(self, node_id:int, channel:int):
        super().__init__(node_id, channel)
        self.node_id = node_id
        self.channel = channel
        self.memory = SharedMemoryManager(service_id=self.node_id, cache_capacity=100000000, cache_expire_time=3600)

    async def input(self, inputs:List[Dict[str, Any]]):
        tasks = [self.process_input(input_item) for input_item in inputs]
        await asyncio.gather(*tasks)
    
    async def process_input(self, input_item:Dict[str, Any], system_prompt:str= None, user_prompt:str= None):
        """
        Process a single input item.
        :param input_item: A dictionary containing 'input_type' and 'data'.
        """
        input_type = input_item.get('input')
        channel = input_item.get('channel')
        key = input_item.get('key')
        version = input_item.get('version')

        if input_type == InputType.SYSTEM.value:
            system_prompt=handle_system_prompt(system_prompt)
        
        elif input_type == InputType.USER.value:
            user_prompt=handle_user_prompt(user_prompt)

        elif input_type == InputType.CONTEXT.value:
            context=handle_context_prompt(channel,key,version)

        else:
            raise ValueError(f"Unsupported input type: {input_type}")
        
        rendered_prompt = await processor(system_prompt, user_prompt, context)
        self.memory.store_text(key, rendered_prompt)
        Publisher(channel).publish("Prompt is Ready")