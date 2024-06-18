from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django_filters import FilterSet

from appboard.filters import ArticleFilter, CommentFilter
from appboard.forms import ArticleForm, CommentForm
from appboard.models import Article, Subscription, User, Comment


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 5


class ArticleDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Article
    # Используем другой шаблон — news_id.html
    template_name = 'article_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'articleid'


# class ArticleSearch(ListView):
#     model = Article
#     # Используем другой шаблон — news_id.html
#     template_name = 'article_search.html'
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = 'article_search'
#     paginate_by = 5
#
#     def get_queryset(self):
#         # Получаем обычный запрос
#         queryset = super().get_queryset()
#         # Используем наш класс фильтрации.
#         # self.request.GET содержит объект QueryDict, который мы рассматривали
#         # в этом юните ранее.
#         # Сохраняем нашу фильтрацию в объекте класса,
#         # чтобы потом добавить в контекст и использовать в шаблоне.
#         self.filterset = ArticleFilter(self.request.GET, queryset)
#         # Возвращаем из функции отфильтрованный список товаров
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         # С помощью super() мы обращаемся к родительским классам
#         # и вызываем у них метод get_context_data с теми же аргументами,
#         # что и были переданы нам.
#         # В ответе мы должны получить словарь.
#         context = super().get_context_data(**kwargs)
#         # К словарю добавим текущую дату в ключ 'time_now'.
#         context['time_now'] = datetime.utcnow()
#         # Добавим ещё одну пустую переменную,
#         # чтобы на её примере рассмотреть работу ещё одного фильтра.
#         context['next_sale'] = None
#         context['filterset'] = self.filterset
#         return context


# Добавляем представление для создания статьи.
class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('testapp.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        new_article = form.save(commit=False)
        if self.request.method == 'POST':
            new_article.author = self.request.user
        new_article.save()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Article.objects.get(pk=self.kwargs.get('pk')).author
        return context


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
                user_id=OuterRef('pk'),
            )
        )
    ).order_by('user_subscribed')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')


class ProfileView(LoginRequiredMixin, ListView):
    form_class = CommentFilter
    model = Comment
    template_name = 'profile.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author__id=self.request.user.id)
        self.filterset = ArticleFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Comment
    template_name = 'article_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs['pk']
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('appboard.update_comment',)
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_update.html'
    success_url = reverse_lazy('article_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentUser'] = Comment.objects.get(pk=self.kwargs.get('pk')).commentUser
        return context


class CommentDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('appboard.delete_comment',)
    raise_exception = True
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('article_list')


@login_required
@csrf_protect
def accept_response(request, **kwargs):
    if request.method == 'POST':
        comment = Comment.objects.get(id=kwargs['pk'])
        action = request.POST.get('action')

        if action == 'accepted':
            comment.status = True
            comment.save()
        elif action == 'rejected':
            comment.status = False
            comment.save()

    return redirect(request.META['HTTP_REFERER'])


class ArticleFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ['commentPost']

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)
        self.filters['commentPost'].queryset = Article.objects.filter(author__id=kwargs['request'])
