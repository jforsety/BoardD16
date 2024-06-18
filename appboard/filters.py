import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, IsoDateTimeFilter
from .models import *


class ArticleFilter(FilterSet):
    model = Article
    # Поиск по автору
    author = ModelChoiceFilter(
        field_name='text',
        queryset=User.objects.all(),
        empty_label='любой',
        label='Автор статьи',
    )
    # Поиск по названию
    article_title = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Название статьи',
    )
    #Поиск по категории
    # article_category = ModelChoiceFilter(
    #     field_name='category',
    #     queryset=Article.objects.all(),
    #     empty_label='любой',
    #     label='Категория',
    # )
    # Поиск по дате
    date = IsoDateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата создания',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )


class CommentFilter(FilterSet):
    model = Comment
    fields = {'commentPost', 'Article', 'dateCreation'}
    commentPost = django_filters.CharFilter(
        field_name='commentPost',
        lookup_expr='icontains',
        label='Комментарий',
    )
    search_category = ModelChoiceFilter(
        field_name='category',
        queryset=Article.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )
    date = django_filters.IsoDateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата публикации',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )