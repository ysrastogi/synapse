from components.llms.llm import get_llm

class chat_completions:
    def __init__(self, llm_source, model, messages):
        self.llm_source = llm_source
        self.model = model
        self.messages = messages
        self.llm = get_llm(llm_source, model)

    def generate_chat(self):
        response = self.llm.chat.completions.create(
            model=self.model,
            messages = self.messages
        )
        return response
