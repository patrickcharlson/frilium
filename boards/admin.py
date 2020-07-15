from django.contrib import admin

from .models import Board, Topic, Post, Category

admin.site.register(Category)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
