from components.llms.llm import get_llm
from components.models import LLMProperties
from components.constants import LLMSource, RelevantParameters

class llm_parameters:
    def __init__(self, **kwargs):
        self.properties = LLMProperties(**kwargs)

class TextContentBlock:
    def __init__(self, content):
        self.content = content

    def to_dict(self):
        return {
            'content': self.content
        }
    
class ChatCompletions:
    def __init__(self, llm_source, model, messages, **kwargs):
        self.llm_source = llm_source
        self.model = model
        self.messages = messages
        self.llm = get_llm(llm_source, model)
        self.parameters = llm_parameters(**kwargs) 

    def generate_chat(self, tools=None):
        if self.llm_source is LLMSource.AZURE or LLMSource.OPENAI:
            relevant_params = RelevantParameters.OPENAI_CHAT_COMPLETION
        
        filtered_params = {k: v for k, v in self.parameters.properties.__dict__.items() if k in relevant_params and v is not None}
        serializable_messages = []
        for message in self.messages:
            if isinstance(message, TextContentBlock):
                serializable_messages.append(message.to_dict())
            else:
                serializable_messages.append(message)
        response = self.llm.chat.completions.create(
            model=self.model,
            messages = serializable_messages,
            tools=tools,
            # **filtered_params
        )
        return response
