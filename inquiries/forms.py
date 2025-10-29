from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '내용을 입력하세요'
            })
        }

