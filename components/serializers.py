from rest_framework import serializers

class ChatCompletionSerializer(serializers.Serializer):
    llm_source = serializers.ChoiceField(choices=['AZURE', 'OPENAI'])
    model = serializers.CharField(max_length=100)
    messages = serializers.ListField(child=serializers.DictField())
    tools = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)

class PromptTemplateSerializer(serializers.Serializer):
    system_prompt = serializers.CharField()
    user_prompt = serializers.CharField()
    context = serializers.DictField()