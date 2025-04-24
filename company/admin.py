from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.validators import validate_email
from django.db.models import TextField
from django.utils.html import format_html, strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin
from pyexpat.errors import messages

from .models import Category, Project, Blog, Faq, TeamCategory, TeamMember, TeamPosition, ContactUs
from re import search


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_image')

    def display_image(self, obj: Category):
        if obj.image:
            return format_html(f'<img style="border-radius: 7px;" width="60px" height="40px" src="{obj.image.url}"/>')
        return "No Image"

    display_image.short_description = 'Category Image'


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    exclude = ('slug',)
    list_display = ['id', 'title', 'type', 'display_image_logo']

    def display_image_logo(self, obj: Project):
        if obj.image_logo:
            return format_html(
                f'<img style="border-radius: 5px;" width="120px" height="100px" src="{obj.image_logo.url}"/>')
        return "No Image"

    display_image_logo.short_description = 'Logo'

    def display_image(self, obj: Project):
        if obj.image:
            return format_html(f'<img style="border-radius: 150px;" width="150px" height="50px" src="{obj.image.url}"/>')
        return "No Image"

    display_image.short_description = 'Project Image'


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'create_at', 'banner_image']
    formfield_overrides = {
        TextField: {'widget': CKEditor5Widget},
    }
    list_display_links = ('id', 'title')

    def banner_image(self, obj: Blog):
        if obj.banner:
            return format_html(f'<img style="border-radius: 5px;" width="120px" height="100px" src="{obj.banner.url}"/>')
        return "No Image"

    banner_image.short_description = 'Banner'


@admin.register(Faq)
class FaqAdmin(TranslationAdmin):
    list_display = ['id', 'title']


@admin.register(TeamCategory)
class TeamCategoryAdmin(OrderedModelAdmin):
    list_display = ['id', 'title', 'move_up_down_links']


@admin.register(TeamPosition)
class TeamPositionAdmin(TranslationAdmin):
    list_display = ['id', 'title']


@admin.register(TeamMember)
class TeamMemberAdmin(OrderedModelAdmin):
    exclude = ('slug',)
    list_display = ['id', 'full_name', 'image_html', 'position', 'move_up_down_links']
    list_display_links = ('id', 'full_name')
    sortable_by = 'position', 'full_name'

    def image_html(self, obj: TeamMember):
        if obj.image:
            return format_html(f'<img style="border-radius: 5px;" width="100px" height="95px" src="{obj.image.url}"/>')
        return "No Image"

    image_html.short_description = 'Image'

    def linkedin_url(self, obj: TeamMember):

        pattern = r'linkedin\.com\/(?:in|company)\/([a-zA-Z0-9\-]+)\/?'
        match = search(pattern, obj.linkedin)
        if match:
            return format_html(f'<a href="{obj.linkedin}">{match.group(1)}</a>')
        return format_html(f'<a href="{obj.linkedin}">{obj.linkedin}</a>')

    linkedin_url.short_description = 'Linkedin'


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone',)

    def email_url(self, obj):
        validate_email(obj.email)
        return format_html(f'<a href="mailto:{obj.email}">{obj.email}</a>')

    email_url.short_description = 'Email'
