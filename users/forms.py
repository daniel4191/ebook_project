from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import re

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일을 입력하세요'
        })
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'username')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '사용자 이름을 입력하세요'
        })
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # 비밀번호 정책 검증
        if not re.search(r'\d', password1):
            raise forms.ValidationError('비밀번호에 숫자를 포함해야 합니다.')
        if not re.search(r'[a-zA-Z]', password1):
            raise forms.ValidationError('비밀번호에 문자를 포함해야 합니다.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError('비밀번호에 특수문자를 포함해야 합니다.')
        
        # 3개 이상 연속된 문자 검증
        for i in range(len(password1) - 2):
            if password1[i] == password1[i+1] == password1[i+2]:
                raise forms.ValidationError('3개 이상 연속된 문자는 사용할 수 없습니다.')
        
        return password1

