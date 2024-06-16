from django.contrib import admin
from appboard.models import Article, User, Comment, Subscription

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Subscription)
