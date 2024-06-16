from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from appboard.filters import ArticleFilter
from appboard.forms import ArticleForm
from appboard.models import Article, Subscription


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 2


class ArticleDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Article
    # Используем другой шаблон — news_id.html
    template_name = 'article_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'articleid'


class ArticleSearch(ListView):
    model = Article
    # Используем другой шаблон — news_id.html
    template_name = 'article_search.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'article_search'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ArticleFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


# Добавляем представление для создания статьи.
class ArticleCreate(CreateView, LoginRequiredMixin):
    raise_exception = True
    permission_required = ('appboard.add_article',)
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель статей
    model = Article
    template_name = 'article_create.html'

    def form_valid(self, form):
        news_type = form.save(commit=False)
        news_type.type = 'article'
        news_rating = form.save(commit=False)
        news_rating.rating = 0
        article = form.save(commit=False)
        if self.request.path == '/article/create/':
            article.category = 'tank'  # если вызывается этот путь - сохраняется как NW
        article.save()  # сохраняем форму (создали пост, которому присвоился id)
        # вызываем таску (уведомление на email о появлении новой новости подписанной категории)
        # send_email_task.delay(post.pk)  # получаем pk созданного поста и передаем его в таску (тк это обяз-ый аргумент для таски)
        return super().form_valid(form)


# Представление удаляющее статью.
class ArticleDelete(DeleteView, LoginRequiredMixin):
    raise_exception = True
    permission_required = ('appboard.delete_article',)
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


# Представление для изменения статьи.
class ArticleUpdate(UpdateView, LoginRequiredMixin):
    raise_exception = True
    permission_required = ('appboard.update_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_update.html'


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Article.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Article.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                article=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


