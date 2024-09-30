# Guide to Writing Effective Prompts

This document provides an overview of how to write effective prompts using our custom prompt template system. It covers the supported prompt types and best practices for creating dynamic and flexible prompts.

## Supported Prompt Types

Our system supports the following types of prompt parts:

1. **Text**: Regular text content.
2. **Variable**: Dynamic content inserted from the context.
3. **Conditional**: Content that is included based on a condition.
4. **Loop**: Content that is repeated for each item in an iterable.

## Prompt Structure

A complete prompt template consists of two main parts:

1. **System Prompt**: Sets the context and provides instructions for the AI model.
2. **User Prompt**: Contains the specific query or task for the AI model.

Both system and user prompts can utilize all supported prompt types.

## Writing Prompts

### Basic Text

Simply write the text as you normally would:

```
This is a basic text prompt.
```

### Variables

To insert dynamic content, use curly braces `{}`:

```
Hello, {name}! Welcome to {company_name}.
```

### Conditional Statements

Use `{% if condition %}` and `{% endif %}` for conditional content:

```
{% if is_premium_user %}
Thank you for being a premium user!
{% endif %}
```

You can also use `{% else %}` for alternative content:

```
{% if is_logged_in %}
Welcome back, {username}!
{% else %}
Please log in to continue.
{% endif %}
```

### Loops

Use `{% for item in items %}` and `{% endfor %}` to iterate over lists:

```
Your shopping cart contains:
{% for item in cart_items %}
- {item.name}: ${item.price}
{% endfor %}
```

## Best Practices

1. **Use variables for dynamic content**: This allows for easy customization of prompts based on context.

2. **Leverage conditional statements**: Tailor the prompt based on user characteristics or specific conditions.

3. **Utilize loops for repetitive content**: When dealing with lists or collections, use loops to avoid repetition in your prompt template.

4. **Combine different prompt types**: Mix and match text, variables, conditionals, and loops to create flexible and powerful prompts.

5. **Keep it readable**: Even though the prompt includes logic, try to maintain readability for easier maintenance.

6. **Test thoroughly**: Ensure your prompts work as expected with various inputs and conditions.

7. **Use context effectively**: Always be aware of the context dictionary and use it to populate your prompts with relevant information.

## Specialized Prompt Types

### 1. Customer Support Prompt

This type of prompt is designed for customer support scenarios. It includes:

- Customer information (name, account type, product)
- Current inquiry
- Previous interactions

Example:

```python
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
```

### 2. Language Learning Prompt

This prompt type is tailored for language learning applications. It includes:

- Student information (name, native language, proficiency level)
- Learning goals
- Current request
- Previous lessons

Example:

```python
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
```

### 3. Fitness Coach Prompt

This prompt type is designed for personalized fitness coaching. It includes:

- User profile (name, age, gender, height, weight)
- Fitness level and goals
- Health conditions
- Current request
- Workout history

Example:

```python
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
```

## Using Context Effectively

When creating prompts, it's crucial to be aware of the context dictionary and use it effectively. The context contains all the dynamic information that will be inserted into your prompt template. Here are some tips for using context:

1. **Understand your context**: Before writing your prompt, make sure you know what information will be available in the context dictionary.

2. **Use consistent keys**: When referencing variables in your prompt, ensure that the keys match those in your context dictionary.

3. **Handle missing data**: Consider using conditional statements to handle cases where certain context information might be missing.

4. **Iterate over lists**: For context items that are lists (like previous interactions or workout history), use loops to display all relevant information.

5. **Conditional formatting**: Use conditional statements to adjust the prompt based on context values (e.g., proficiency level in the language learning example).

Remember, the power of these prompt templates comes from their ability to adapt based on the provided context. By effectively using the context in your prompts, you can create highly personalized and relevant interactions for each user.

## Example Usage

To use these prompt templates, you would typically follow these steps:

1. Define your system and user prompts as strings.
2. Create a prompt template using the `create_prompt_template` function.
3. Prepare your context dictionary with all necessary information.
4. Render the prompt using the `render` method of your template.

Example:

```python
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
```

This approach allows you to create highly dynamic and context-aware prompts for various applications.