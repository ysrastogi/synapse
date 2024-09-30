from typing import Dict, Any, List, Optional
import re

from components.prompts.constant import PromptPartType


class PromptPart:
    def __init__(self, type: PromptPartType, content: str):
        self.type = type
        self.content = content

class ConditionalPromptPart(PromptPart):
    def __init__(self, condition: str, true_content: List[PromptPart], false_content: Optional[List[PromptPart]] = None):
        super().__init__(PromptPartType.CONDITIONAL, condition)
        self.true_content = true_content
        self.false_content = false_content

class LoopPromptPart(PromptPart):
    def __init__(self, loop_var: str, iterable: str, content: List[PromptPart]):
        super().__init__(PromptPartType.LOOP, f"for {loop_var} in {iterable}")
        self.loop_var = loop_var
        self.iterable = iterable
        self.content = content

class PromptInstance:
    def __init__(self, parts: List[PromptPart], role: str):
        self.parts = parts
        self.role = role

    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        return {
            "role": self.role,
            "content": self._render_parts(self.parts, context)
        }

    def _render_parts(self, parts: List[PromptPart], context: Dict[str, Any]) -> str:
        result = []
        for part in parts:
            if part.type == PromptPartType.TEXT:
                result.append(part.content)
            elif part.type == PromptPartType.VARIABLE:
                if part.content in context:
                    result.append(str(context[part.content]))
                else:
                    result.append(f"{{{part.content}}}")
            elif part.type == PromptPartType.CONDITIONAL:
                if isinstance(part, ConditionalPromptPart):
                    condition_result = eval(part.content, {}, context)
                    if condition_result:
                        result.append(self._render_parts(part.true_content, context))
                    elif part.false_content:
                        result.append(self._render_parts(part.false_content, context))
            elif part.type == PromptPartType.LOOP:
                if isinstance(part, LoopPromptPart):
                    iterable = eval(part.iterable, {}, context)
                    for item in iterable:
                        loop_context = context.copy()
                        loop_context[part.loop_var] = item
                        result.append(self._render_parts(part.content, loop_context))
        return "".join(result)

class PromptTemplate:
    def __init__(self, system: PromptInstance, user: PromptInstance):
        self.system = system
        self.user = user

    def render(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        return [
            self.system.render(context),
            self.user.render(context)
        ]

def parse_instance(template: str, role: str) -> PromptInstance:
    parts = []
    current_text = []

    def add_text_part():
        if current_text:
            parts.append(PromptPart(PromptPartType.TEXT, "".join(current_text)))
            current_text.clear()

    tokens = re.split(r'(\{[^}]+\}|\{% if [^%]+%\}|\{% endif %\}|\{% for [^%]+%\}|\{% endfor %\})', template)
    
    i = 0
    while i < len(tokens):
        token = tokens[i].strip()
        if token.startswith('{') and token.endswith('}') and not token.startswith('{%'):
            add_text_part()
            parts.append(PromptPart(PromptPartType.VARIABLE, token[1:-1].strip()))
        elif token.startswith('{% if'):
            add_text_part()
            condition = token[5:-2].strip()
            true_content = []
            false_content = []
            nesting = 1
            i += 1
            while nesting > 0 and i < len(tokens):
                if tokens[i].strip() == '{% endif %}':
                    nesting -= 1
                elif tokens[i].strip().startswith('{% if'):
                    nesting += 1
                if nesting == 0:
                    break
                true_content.append(tokens[i])
                i += 1
            if i + 1 < len(tokens) and tokens[i + 1].strip().startswith('{% else %}'):
                i += 2
                nesting = 1
                while nesting > 0 and i < len(tokens):
                    if tokens[i].strip() == '{% endif %}':
                        nesting -= 1
                    elif tokens[i].strip().startswith('{% if'):
                        nesting += 1
                    if nesting == 0:
                        break
                    false_content.append(tokens[i])
                    i += 1
            parts.append(ConditionalPromptPart(condition, parse_instance("".join(true_content), role).parts, parse_instance("".join(false_content), role).parts if false_content else None))
        elif token.startswith('{% for'):
            add_text_part()
            loop_def = token[6:-2].strip().split()
            loop_var = loop_def[0]
            iterable = " ".join(loop_def[2:])
            loop_content = []
            nesting = 1
            i += 1
            while nesting > 0 and i < len(tokens):
                if tokens[i].strip() == '{% endfor %}':
                    nesting -= 1
                elif tokens[i].strip().startswith('{% for'):
                    nesting += 1
                if nesting == 0:
                    break
                loop_content.append(tokens[i])
                i += 1
            parts.append(LoopPromptPart(loop_var, iterable, parse_instance("".join(loop_content), role).parts))
        else:
            current_text.append(token)
        i += 1

    add_text_part()
    return PromptInstance(parts, role)

def create_prompt_template(system: str, user: str) -> PromptTemplate:
    return PromptTemplate(
        system=parse_instance(system, "system"),
        user=parse_instance(user, "user")
    )

