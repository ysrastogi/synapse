from enum import Enum

class InputType(Enum):
    PROMPT = "Prompt"
    TOOLS = "Tools"
    FUNCTIONS = "Functions"
    SHORT_MEMORY = "Short Memory"