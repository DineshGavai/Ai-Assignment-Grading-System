from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'rubric', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'rubric': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter JSON, e.g., {"grammar": 10, "content": 20}'}),
        }

    def clean_rubric(self):
        rubric = self.cleaned_data['rubric']
        if rubric:
            import json
            try:
                json.loads(rubric)  # Validate JSON
            except json.JSONDecodeError:
                raise forms.ValidationError("Rubric must be valid JSON (e.g., {\"grammar\": 10, \"content\": 20}).")
        return rubric