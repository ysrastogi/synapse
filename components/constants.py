class LLMSource:
    AZURE = "azure"
    OPENAI = "openai"
    OLLAMA = "ollama"

class ModelSource:
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"


class LLMModelSource:
    AZURE = ["gpt-4o", "gpt-4-turbo-preview"]
    OPENAI = ["gpt-4o", ""]


class RelevantParameters:
    AZURE_CHAT_COMPLETION = ['temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty', 'stop', 'logit_bias', 'stream', 'logprobs', 'top_logprobs', 'response_format', 'seed']
    OPENAI_CHAT_COMPLETION = [ 'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty', 'stop', 'logit_bias', 'stream', 'logprobs', 'top_logprobs', 'response_format', 'seed']

