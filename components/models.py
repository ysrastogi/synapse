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
    stream = models.BooleanField(null=False, blank=True)
    
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