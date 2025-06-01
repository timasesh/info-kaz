from django import forms
from .models import Contact, News, Category
from django_summernote.widgets import SummernoteWidget

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение', 'rows': 5}),
        }

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'image', 'is_published', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        } 