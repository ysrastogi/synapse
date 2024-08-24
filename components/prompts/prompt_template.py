from typing import Dict, Any, List, Optional
from enum import Enum
import re

class PromptPartType(Enum):
    TEXT = "text"
    VARIABLE = "variable"
    CONDITIONAL = "conditional"
    LOOP = "loop"

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


class PromptExample:
    @staticmethod
    def customer_support_example():
        system_prompt = """
        You are a customer support AI assistant for a tech company.
        You specialize in helping customers with product inquiries and technical issues.
        Always be polite, professional, and helpful.
        """

        user_prompt = """
        Customer Information:
        Name: {name}
        Account Type: {account_type}
        Product: {product}

        The customer's current inquiry is: {current_inquiry}

        Previous Interactions:
        {% for interaction in previous_interactions %}
        Customer: {interaction['customer']}
        Support: {interaction['support']}
        {% endfor %}

        Please provide a helpful response addressing their concern.
        """

        template = create_prompt_template(system_prompt, user_prompt)

        context = {
            "name": "John Doe",
            "account_type": "Premium",
            "product": "SmartHome Hub",
            "current_inquiry": "My SmartHome Hub isn't connecting to my Wi-Fi network. What should I do?",
            "previous_interactions": [
                {
                    "customer": "How do I set up my SmartHome Hub?",
                    "support": "To set up your SmartHome Hub, please follow these steps: 1. Plug in the device..."
                }
            ]
        }

        rendered_prompt = template.render(context)
        print("Customer Support Example:")
        for message in rendered_prompt:
            print(f"\nRole: {message['role']}")
            print(f"Content: {message['content']}")

    @staticmethod
    def language_learning_example():
        system_prompt = """
        You are a language learning AI assistant specializing in {target_language}.
        Your role is to help students practice and improve their language skills.
        Adjust your language complexity based on the student's proficiency level.
        """

        user_prompt = """
        Student Information:
        Name: {student_name}
        Native Language: {native_language}
        Proficiency Level: {proficiency_level}
        Learning Goals: {learning_goals}

        The student's current request is: {current_request}

        Previous Lessons:
        {% for lesson in previous_lessons %}
        Topic: {lesson['topic']}
        Key Vocabulary: {', '.join(lesson['vocabulary'])}
        {% endfor %}

        Please provide a response in {target_language} that addresses their request and aligns with their learning goals.
        {% if proficiency_level == 'Beginner' %}
        Include translations for difficult words or phrases.
        {% endif %}
        """

        template = create_prompt_template(system_prompt, user_prompt)

        context = {
            "target_language": "Spanish",
            "student_name": "Emily",
            "native_language": "English",
            "proficiency_level": "Intermediate",
            "learning_goals": "Improve conversation skills and expand vocabulary",
            "current_request": "Can you help me practice talking about my hobbies?",
            "previous_lessons": [
                {
                    "topic": "Daily Routines",
                    "vocabulary": ["despertarse", "ducharse", "desayunar", "trabajar"]
                },
                {
                    "topic": "Weather",
                    "vocabulary": ["soleado", "lluvioso", "nublado", "temperatura"]
                }
            ]
        }

        rendered_prompt = template.render(context)
        print("\nLanguage Learning Example:")
        for message in rendered_prompt:
            print(f"\nRole: {message['role']}")
            print(f"Content: {message['content']}")

    @staticmethod
    def fitness_coach_example():
        system_prompt = """
        You are an AI fitness coach specialized in creating personalized workout plans.
        Your goal is to provide safe, effective, and tailored exercise recommendations.
        Always prioritize the user's safety and adjust plans based on their fitness level and any health conditions.
        """

        user_prompt = """
        User Profile:
        Name: {user_name}
        Age: {age}
        Gender: {gender}
        Height: {height}
        Weight: {weight}
        Fitness Level: {fitness_level}
        Health Conditions: {% for condition in health_conditions %}{condition}, {% endfor %}
        Fitness Goals: {fitness_goals}

        The user's current request is: {current_request}

        Previous Workout Sessions:
        {% for session in workout_history %}
        Date: {session['date']}
        Exercises: {', '.join(session['exercises'])}
        Duration: {session['duration']} minutes
        Difficulty Rating: {session['difficulty']}/10
        {% endfor %}

        Please provide a detailed response that includes:
        1. A personalized workout plan
        2. Nutritional advice
        3. Safety precautions based on their health conditions
        """

        template = create_prompt_template(system_prompt, user_prompt)

        context = {
            "user_name": "Sarah Johnson",
            "age": 35,
            "gender": "Female",
            "height": "5'6\"",
            "weight": "140 lbs",
            "fitness_level": "Intermediate",
            "health_conditions": ["mild asthma", "previous knee injury"],
            "fitness_goals": "Improve overall strength and endurance",
            "current_request": "I want to start incorporating more strength training into my routine. Can you suggest a plan?",
            "workout_history": [
                {
                    "date": "2023-05-01",
                    "exercises": ["Jogging", "Push-ups", "Squats"],
                    "duration": 45,
                    "difficulty": 7
                },
                {
                    "date": "2023-05-03",
                    "exercises": ["Cycling", "Planks", "Lunges"],
                    "duration": 60,
                    "difficulty": 6
                }
            ]
        }

        rendered_prompt = template.render(context)
        print("\nFitness Coach Example:")
        for message in rendered_prompt:
            print(f"\nRole: {message['role']}")
            print(f"Content: {message['content']}")
        return rendered_prompt

