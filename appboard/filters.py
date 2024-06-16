from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, IsoDateTimeFilter
from .models import *


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ArticleFilter(FilterSet):
    # Поиск по автору
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Article.objects.all(),
        empty_label='любой',
        label='Автор статьи',
    )
    # Поиск по названию
    article_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название статьи',
    )
    # Поиск по категории
    article_category = ModelChoiceFilter(
        field_name='category',
        queryset=Article.objects.all(),
        empty_label='любой',
        label='Категория',
        #conjoined=True,
    )
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