from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .llms.llm import get_llm
from .llms.chat_helper import ChatCompletions
from .prompts.prompt_template import create_prompt_template
from .serializers import ChatCompletionSerializer, PromptTemplateSerializer
from qdrant_client.http.exceptions import ResponseHandlingException
from connections.db import VectorDB

import logging

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
    
class KnowledgeBaseView(APIView):
    client = VectorDB()

    def post(self, request, format=None):
        action = request.data.get('action')
        if action == 'create_collection':
            return self.create_collection(request)
        elif action == 'upsert':
            return self.upsert(request)
        elif action == 'search':
            return self.search(request)
        elif action == 'search_with_filter':
            return self.search_with_filter(request)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    def create_collection(self, request):
        collection_name = request.data.get('collection_name')
        vector_size = request.data.get('vector_size')
        distance = request.data.get('distance')
        if not collection_name or not vector_size or not distance:
            return Response({"error": "collection_name, vector_size, and distance are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.client.create_collection(vector_size=vector_size, distance=distance, collection_name=collection_name)
            return Response({"status": "collection created"}, status=status.HTTP_200_OK)
        except ResponseHandlingException as e:
            logging.error(f"Error creating collection: {e}")
            return Response({"error": "Failed to connect to Qdrant server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def upsert(self, request):
        collection_name = request.data.get('collection_name')
        points_data = request.data.get('points')
        if not collection_name or not points_data:
            return Response({"error": "collection_name and points are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            points = [PointStruct(**point) for point in points_data]
            operation_info = self.client.upsert(collection_name=collection_name, points=points)
            return Response(operation_info, status=status.HTTP_200_OK)
        except ResponseHandlingException as e:
            logging.error(f"Error upserting points: {e}")
            return Response({"error": "Failed to connect to Qdrant server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search(self, request):
        collection_name = request.data.get('collection_name')
        query = request.data.get('query')
        limit = request.data.get('limit')
        if not collection_name or not query or not limit:
            return Response({"error": "collection_name, query, and limit are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            search_result = self.client.search(collection_name=collection_name, query=query, limit=limit)
            return Response(search_result, status=status.HTTP_200_OK)
        except ResponseHandlingException as e:
            logging.error(f"Error searching collection: {e}")
            return Response({"error": "Failed to connect to Qdrant server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search_with_filter(self, request):
        collection_name = request.data.get('collection_name')
        query = request.data.get('query')
        filter_key = request.data.get('filter_key')
        filter_value = request.data.get('filter_value')
        limit = request.data.get('limit')
        if not collection_name or not query or not filter_key or not filter_value or not limit:
            return Response({"error": "collection_name, query, filter_key, filter_value, and limit are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            search_result = self.client.search_with_filter(collection_name=collection_name, query=query, filter_key=filter_key, filter_value=filter_value, limit=limit)
            return Response(search_result, status=status.HTTP_200_OK)
        except ResponseHandlingException as e:
            logging.error(f"Error searching collection with filter: {e}")
            return Response({"error": "Failed to connect to Qdrant server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)