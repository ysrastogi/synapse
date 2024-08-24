from django.urls import path
from .views import GetLLMView, ChatCompletionsView, PromptTemplateView

urlpatterns = [
    path('get-llm/', GetLLMView.as_view(), name='get-llm'),
    path('chat-completions/', ChatCompletionsView.as_view(), name='chat-completions'),
    path('prompt-template/', PromptTemplateView.as_view(), name='prompt-template'),
]