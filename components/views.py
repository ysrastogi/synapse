from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .llms.llm import get_llm
from .llms.chat_helper import ChatCompletions
from .prompts.prompt_template import create_prompt_template
from .serializers import ChatCompletionSerializer, PromptTemplateSerializer

class GetLLMView(APIView):
    def get(self, request, format=None):
        llm_source = request.query_params.get('llm_source')
        model = request.query_params.get('model')
        if not llm_source or not model:
            return Response({"error": "llm_source and model are required"}, status=status.HTTP_400_BAD_REQUEST)
        llm = get_llm(llm_source, model)
        return Response({"message": "LLM initialized successfully"}, status=status.HTTP_200_OK)

class ChatCompletionsView(APIView):
    def post(self, request, format=None):
        serializer = ChatCompletionSerializer(data=request.data)
        if serializer.is_valid():
            llm_source = serializer.validated_data['llm_source']
            model = serializer.validated_data['model']
            messages = serializer.validated_data['messages']
            tools = serializer.validated_data.get('tools')
            chat_completion = ChatCompletions(llm_source=llm_source, model=model, messages=messages)
            response = chat_completion.generate_chat(tools=tools)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PromptTemplateView(APIView):
    def post(self, request, format=None):
        serializer = PromptTemplateSerializer(data=request.data)
        if serializer.is_valid():
            system_prompt = serializer.validated_data['system_prompt']
            user_prompt = serializer.validated_data['user_prompt']
            context = serializer.validated_data['context']
            template = create_prompt_template(system_prompt, user_prompt)
            rendered_prompt = template.render(context)
            return Response(rendered_prompt, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)