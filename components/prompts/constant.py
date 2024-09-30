from enum import Enum

class PromptPartType(Enum):
    TEXT = "text"
    VARIABLE = "variable"
    CONDITIONAL = "conditional"
    LOOP = "loop"

class InputType(Enum):
    SYSTEM = "System"
    USER = "User"
    CONTEXT = "Context"