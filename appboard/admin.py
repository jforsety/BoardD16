from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from appboard.models import Article, User, Comment, Subscription


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Subscription)
