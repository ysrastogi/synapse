from django import forms
from components.models import LLMProperties

class LLMPropertiesForm(forms.ModelForm):
    class Meta:
        model = LLMProperties
        fields = '__all__'

    def clean_tool_choice(self):
        tool_choice = self.cleaned_data.get('tool_choice')
        allowed_values = ['none', 'auto', 'required']
        if isinstance(tool_choice, str) and tool_choice not in allowed_values:
            raise forms.ValidationError("tool_choice must be 'none', 'auto', 'required', or a specific tool JSON object.")
        return tool_choice