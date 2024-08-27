from modeltranslation.translator import TranslationOptions, register, translator
from .models import Project, Blog, Faq, TeamCategory, TeamMember


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'type', 'description_short', 'project_type', 'preview', 'description_long')


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(TeamCategory)
class TeamCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('position',)
