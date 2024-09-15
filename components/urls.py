from django.urls import path
from .views import GetLLMView, ChatCompletionsView, PromptTemplateView, KnowledgeBaseView

urlpatterns = [
    path('get-llm/', GetLLMView.as_view(), name='get-llm'),
    path('chat-completions/', ChatCompletionsView.as_view(), name='chat-completions'),
    path('prompt-template/', PromptTemplateView.as_view(), name='prompt-template'),
    path('knowledge-base/', KnowledgeBaseView.as_view(), name='knowledge_base'),
]