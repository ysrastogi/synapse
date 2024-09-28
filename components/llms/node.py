import asyncio
from typing import Dict, Any, List

from connections.nodes.base import NodeBase

from components.llms.handlers import handle_prompt, handle_functions, handle_tools
from components.constants import LLMSource, LLMModelSource
from components.llms.llm import get_llm

from synapse.memory_manager.shared_memory_manager import SharedMemoryManager

class LLMNode(NodeBase):
    def __init__(self, node_id:int , channel:int , llm_source:LLMSource, model:LLMModelSource):
        super().__init__(node_id, channel)
        self.llm = get_llm(llm_source, model)
        self.node_id = node_id
        self.channel = channel
        self.memory = SharedMemoryManager(service_id=self.node_id, num_partitions=4, cache_capacity=100000000, cache_expire_time=3600)
    
    async def input(self, inputs: List[Dict[str, Any]]):
        tasks = [self.process_input(input_item) for input_item in inputs]
        await asyncio.gather(*tasks)

    async def process_input(self, input_item):
        """
        Process a single input item.
        :param input_item: A dictionary containing 'input_type' and 'data'.
        """
        input_type = input_item.get('input')
        channel = input_item.get('channel')
        key = input_item.get('key')
        version = input_item.get('version')

        if input_type == "Prompt":
            ...
        elif input_type == "Tools":
            ...
        elif input_type == "Functions":
            ...
        elif input_type == "Short Memory":
            ...
        else:
            raise ValueError(f"Unsupported input type: {input_type}")

    def output(self):
        ...
        
    def properties(self):
        ...

    def handle_message(self, message):
        ...
    
    def possible_inputs(self):
        """
        Define the possible inputs for the LLMNode.
        
        :return: A dictionary describing the possible input types.
        """
        return {
            "Prompt": "text",
            "Tools": "various data structures or functions",
            "Functions": "callable code snippets",
            "Short Memory":"To track previous conversation"
        }