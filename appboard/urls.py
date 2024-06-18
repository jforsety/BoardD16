from django.urls import path
from appboard.views import ArticleList, ArticleDetail, ArticleCreate, ArticleDelete, ArticleUpdate, \
     ConfirmUser, ProfileView, CommentCreate, CommentUpdate, CommentDelete, accept_response

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    # path('search/', ArticleSearch.as_view(), name='article_search'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    # path('subscriptions/', subscriptions, name='subscriptions'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'), # Профиль пользователя
    path('<int:pk>/comment/create/', CommentCreate.as_view(), name='comment_create'), # Создание комментария
    path('<int:pk>/comment/update/', CommentUpdate.as_view(), name='comment_update'), # изменение комментария
    path('<int:pk>/comment/delete/', CommentDelete.as_view(), name='comment_delete'), # удаление комментария
    path('<int:pk>/comment/confirm/', accept_response, name='confirm_comment'),  # принять отклик
    path('<int:pk>/comment/reject/', accept_response, name='reject_comment'),  # отклонить отклик
]