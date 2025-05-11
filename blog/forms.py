from django import forms
from django.core.validators import FileExtensionValidator

from .models import Article, Message
from django_ckeditor_5.widgets import CKEditor5Widget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='default'
            ),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'contact_type', 'contact_info', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您的姓名'}),
            'contact_type': forms.Select(attrs={'class': 'form-control', 'id': 'contact-type'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您的联系方式'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '请输入您的留言内容'}),
        }

