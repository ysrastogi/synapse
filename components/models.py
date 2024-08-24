from django.db import models
from typing import ClassVar
from pydantic import BaseModel, ConfigDict

class LLMProperties(models.Model):
    response_format = models.CharField(null=True, blank=True)
    seed = models.IntegerField(null=True, blank=True)
    stop = models.CharField(max_length=255, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    mirostat = models.FloatField(default=False)
    mirostat_eta = models.FloatField(null=True, blank=True)
    mirostat_tau = models.FloatField(null=True, blank=True)
    top_k = models.IntegerField(null=True, blank=True)
    top_p = models.FloatField(null=True, blank=True)
    min_p = models.FloatField(null=True, blank=True)
    frequency_penalty = models.FloatField(null=True, blank=True)
    repeat_last_n = models.IntegerField(null=True, blank=True)
    tfs_z = models.FloatField(null=True, blank=True)
    context_length = models.IntegerField(null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
    tokens_to_keep_on_context_refresh = models.IntegerField(null=True, blank=True)
    max_tokens = models.IntegerField(null=True, blank=True)
    use_mmap = models.BooleanField(default=False)
    use_mlock = models.BooleanField(default=False)
    num_thread = models.IntegerField(null=True, blank=True)
    logit_bias = models.JSONField(null=True, blank=True)
    logprobs = models.BooleanField(default=False)
    top_logprobs = models.IntegerField(null=True, blank=True)
    stream = models.BooleanField(null=True, blank=True)
    tool_choice = models.CharField(null=True, blank=True, default="none")

    def __str__(self):
        return f"LLMProperties(id={self.id})"

class ModelMeta(models.Model):
    description= models.CharField(null=True, blank=True)
    capabilities = models.JSONField(null=True, blank=True)

    class Config:
        orm_mode=True

class LLM(models.Model):
    id= models.IntegerField(primary_key=True)
    user_id = models.CharField(null=False, blank=False)
    name=models.CharField(null=True, blank=True)
    properties = models.OneToOneField(LLMProperties, on_delete=models.CASCADE, related_name='llm')
    
    def __str__(self):
        return self.name

class PromptTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    variables = models.JSONField()  # Store as a JSON array of variable names
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PromptCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Prompt(models.Model):
    template = models.ForeignKey(PromptTemplate, on_delete=models.CASCADE)
    category = models.ForeignKey(PromptCategory, on_delete=models.SET_NULL, null=True)
    variables_values = models.JSONField()  # Store as a JSON object of variable name-value pairs
    generated_prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template.name} - {self.created_at}"

class PromptPerformanceMetric(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=50)
    metric_value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt.template.name} - {self.metric_name}: {self.metric_value}"