from django.db import models
from django.utils.text import slugify
from django.db.models import Model, CharField, TextField, ImageField, SlugField, ForeignKey, FileField, DateField
from re import sub as re_sub
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class BaseModel(Model):
    objects = None

    class Meta:
        abstract = True


class Category(BaseModel):
    title = CharField(max_length=256, verbose_name="Title")
    image = ImageField(upload_to="images/", verbose_name="Image", null=True, blank=True)

    def __str__(self):
        return self.title


class Project(BaseModel):
    category = ForeignKey('company.Category', on_delete=models.CASCADE, verbose_name=_("Category"))
    title = CharField(max_length=255, verbose_name="title")
    type = CharField(max_length=255, verbose_name="type")
    image_logo = ImageField(upload_to='project_image_logo/', verbose_name="image_logo", null=True, blank=True)
    description_short = TextField(verbose_name="description_short")
    project_type = CharField(max_length=255, verbose_name="project_type")
    preview = CharField(max_length=255, verbose_name="preview")
    description_long = TextField(verbose_name="description_long")
    video = FileField(upload_to='project_video/', verbose_name="video", null=True, blank=True)
    image = ImageField(upload_to='project_image/', verbose_name="image", null=True, blank=True)
    youtube_link = CharField(max_length=255, verbose_name="youtube_link", null=True, blank=True)
    slug = SlugField(max_length=255, verbose_name=_('Slug'), unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def change(self, *args, **kwargs):
        video_id = self.youtube_link.split('youtu.be/')[1].split('?')[0]
        params = "si=7Yl10RyvzR8oavkv"
        self.youtube_link = f"https://www.youtube.com/embed/{video_id}?{params}"
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'company'


class Blog(BaseModel):
    title = CharField(max_length=256, verbose_name="Title")
    data = DateField(verbose_name="Data")
    image_front = ImageField(upload_to='blog/', verbose_name="image front")
    description_front = TextField(verbose_name="description front")
    image_back = ImageField(upload_to='blog/', verbose_name="image back", null=True, blank=True)
    description_uz = CKEditor5Field(config_name="extends", verbose_name="description uz", null=True, blank=True)
    description_ru = CKEditor5Field(config_name="extends", verbose_name="description ru", null=True, blank=True)
    description_eng = CKEditor5Field(config_name="extends", verbose_name="description eng", null=True, blank=True)

    def __str__(self):
        return self.title


class Faq(BaseModel):
    title = CharField(max_length=256, verbose_name="Title")
    description = TextField(verbose_name="Description")

    def __str__(self):
        return self.title


class Team_category(BaseModel):
    title = CharField(max_length=256, verbose_name="Title")

    def __str__(self):
        return self.title


class Team(BaseModel):
    team_category = models.ForeignKey('company.Team_category', on_delete=models.CASCADE, verbose_name="Category")
    full_name = CharField(max_length=256, verbose_name="Full name")
    image = ImageField(upload_to='team/', verbose_name="image")
    position = CharField(max_length=256, verbose_name="Position")
    linkedin_link = CharField(max_length=256, verbose_name="Linkedin link")
    slug = SlugField(max_length=255, verbose_name=_('Slug'), unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.position)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
