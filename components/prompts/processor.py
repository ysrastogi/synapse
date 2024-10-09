from components.prompts.handlers import handle_context_prompt, handle_properties, handle_system_prompt, handle_user_prompt
from components.prompts.prompt_template import create_prompt_template
from components.prompts.constant import PromptPartType

async def processor(system_prompt:str, user_prompt:str, context:str):
    template = create_prompt_template(system_prompt= user_prompt, user_prompt=user_prompt)
    rendered_prompt = template.render(context)
    # await handle_properties(properties)
    return rendered_prompt