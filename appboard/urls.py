from django.urls import path, include
from appboard.views import ArticleList, ArticleDetail, ArticleSearch, ArticleCreate, ArticleDelete, ArticleUpdate, \
    subscriptions

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', (ArticleDetail.as_view()), name='article_detail'),
    path('search/', ArticleSearch.as_view(), name='article_search'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('subscriptions/', subscriptions, name='subscriptions'),

]