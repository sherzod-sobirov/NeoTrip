from django.contrib import admin
from .models import Contact, Comment, TeamMember
from modeltranslation.admin import TranslationAdmin


@admin.register(TeamMember)
class TeamMemberAdminModel(TranslationAdmin, admin.ModelAdmin):
    pass



admin.site.register([Contact, Comment])