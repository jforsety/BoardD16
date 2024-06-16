from django import forms
from django.core.exceptions import ValidationError
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'author',
            'title',
            'category',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Описание новости не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data