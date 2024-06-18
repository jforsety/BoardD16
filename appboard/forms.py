from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Textarea

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Article
        fields = [
            'upload',
            'title',
            'text',
            'author',
            'category',
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )
        return title

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Описание должно начинаться с заглавной буквы"
            )
        if text is not None and len(text) < 20:
            raise ValidationError(
                "Описание статьи не может быть менее 20 символов."
            )
        return text

    class Meta:
        model = Article
        fields = ['upload', 'title', 'text', 'category']

        widgets = {
            'upload': TextInput(attrs={'class': 'form-control', 'placeholder': 'Загрузите файл'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок объявления'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание объявления'}),
            'category_': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Введите текст отклика:'
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 150, 'rows': 1}),
        }
