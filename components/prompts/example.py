from components.prompts.prompt_template import create_prompt_template

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