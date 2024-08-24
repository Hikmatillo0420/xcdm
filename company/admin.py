from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from .models import Category, Project, Blog, Faq, Team_category, Team


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    exclude = ('slug',)
    list_display = ['id', 'title', 'type', 'image_logo', 'description_short', 'project_type', 'preview',
                    'description_long', 'video', 'image', 'youtube_link']

    def image(self, obj: Project):
        if obj.image:
            return format_html(f'<img style="border-radius: 5px;" width="50px" height="50px" src="{obj.image.url}"/>')
        return "No Image"

    image.short_description = 'Project Image'


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'data', 'image_front', 'description_front', 'image_back', 'description_uz',
                    'description_ru',
                    'description_eng']


@admin.register(Faq)
class FaqAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'description']


@admin.register(Team_category)
class TeamCategoryAdmin(TranslationAdmin):
    list_display = ['id', 'title']


@admin.register(Team)
class TeamAdmin(TranslationAdmin):
    exclude = ('slug',)
    list_display = ['id', 'full_name', 'image', 'position', 'linkedin_link']
