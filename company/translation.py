from modeltranslation.translator import TranslationOptions, register, translator
from .models import Project, Blog, Faq, Team_category, Team


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'type', 'description_short', 'project_type', 'preview', 'description_long')


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description_front')


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Team_category)
class TeamCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ('position',)
