from typing import Dict, Any
from connections.nodes.base import NodeBase
from components.llms.node import LLMNode

class NodeFactory:
    @staticmethod
    def create_node(node_type:str, config:Dict[str, Any]) -> NodeBase:
        """define all the nodes here and call using config file"""
        # if node_type == "LLM":
        #     return LLMNode(
        #         node_id=config['node_id'],
        #         channel=config['channel'],
        #         llm_source=config['llm_source'],
        #         model=config['model']
        #     )
        # elif node_type == "KnowledgeBase":
        #     return KnowledgeBaseNode(
        #         node_id=config['node_id'],
        #         channel=config['channel']
        #     )
        # # Add other node types as needed
        # else:
        #     raise ValueError(f"Unknown node type: {node_type}")
        ...

# Usage
# config = {
#     "node_id": "llm_1",
#     "channel": "main_channel",
#     "llm_source": "openai",
#     "model": "gpt-3.5-turbo"
# }
# llm_node = NodeFactory.create_node("LLM", config)

# kb_config = {
#     "node_id": "kb_1",
#     "channel": "kb_channel"
# }
# kb_node = NodeFactory.create_node("KnowledgeBase", kb_config)