from django.contrib import admin
from .models import Post, Comment
from modeltranslation.admin import TranslationAdmin


@admin.register(Post)
class PostAdminModel(TranslationAdmin, admin.ModelAdmin):
    pass


# @admin.register(Comment)
# class CommentAdminModel(admin.ModelAdmin):
#     pass

