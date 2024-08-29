from modeltranslation.translator import TranslationOptions, register, translator
from .models import Project, Blog, Faq, TeamCategory,TeamPosition


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'type', 'description_short', 'project_type', 'description_long')


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(TeamCategory)
class TeamCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(TeamPosition)
class TeamPositionTranslationOptions(TranslationOptions):
    fields = ('title',)
