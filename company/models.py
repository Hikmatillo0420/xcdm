from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model, CharField, TextField, ImageField, ForeignKey, FileField, DateField, \
    URLField, EmailField, IntegerField
from re import match
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel
from datetime import date


def phone_validators(value):
    if not re.fullmatch(r'\+\d{12}', value):
        raise ValidationError(
            _('Phone number must start with "+" . No letters or symbols allowed.'),
            params={'value': value},
        )


import re
def validate_linkedin_url(value):
    linkedin_pattern = r'^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$'
    if not match(linkedin_pattern, value):
        raise ValidationError(
            _('Invalid LinkedIn profile URL.'),
            params={'value': value},
        )
def validators_email_link(value):
    allowed_domains = ['gmail.com', 'mail.ru']
    if not any(value.endswith(f"@{domain}") for domain in allowed_domains):
        raise ValidationError(_('Only Gmail or Mail.ru addresses are allowed.'), params={'value': value})


class BaseModel(Model):
    class Meta:
        abstract = True


class Category(BaseModel):
    title = CharField(max_length=256)
    image = ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Project(OrderedModel):
    category = ForeignKey('company.Category', on_delete=models.CASCADE, )
    title = CharField(max_length=255)
    type = CharField(max_length=255)
    image_logo = ImageField(upload_to='project_image_logo/', null=True, blank=True)
    description_short = TextField()
    project_type = CharField(max_length=255)
    preview = CharField(max_length=255, verbose_name='Previw Link')
    description_long = TextField()
    video = FileField(upload_to='project_video/', null=True, blank=True)
    image = ImageField(upload_to='project_image/', null=True, blank=True)
    youtube_link = URLField(max_length=255, null=True, blank=True)

    def change(self, *args, **kwargs):
        video_id = self.youtube_link.split('youtu.be/')[1].split('?')[0]
        params = "si=7Yl10RyvzR8oavkv"
        self.youtube_link = f"https://www.youtube.com/embed/{video_id}?{params}"
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class Blog(BaseModel):
    title = CharField(max_length=256)
    create_at = DateField(default=date.today)
    banner = ImageField(upload_to='blog/')
    description = TextField()
    description_back = TextField()
    image = ImageField(upload_to='blog/', null=True, blank=True)
    link= URLField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title


class Faq(BaseModel):
    title = CharField(max_length=256, verbose_name="Title")
    description = TextField(verbose_name="Description")

    def __str__(self):
        return self.title


class TeamCategory(OrderedModel):
    title = CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = 'Team Category'
        verbose_name_plural = 'Team Categories'


class TeamPosition(BaseModel):
    title = CharField(max_length=256)

    def __str__(self):
        return self.title





class TeamMember(OrderedModel):
    category = models.ForeignKey('company.TeamCategory', on_delete=models.CASCADE, related_name='members', )
    full_name = CharField(max_length=256)
    image = ImageField(upload_to='team/')
    position = ForeignKey('company.TeamPosition', on_delete=models.CASCADE)
    linkedin = URLField(max_length=256, validators=[validate_linkedin_url], null=True,blank=True)

    def __str__(self):
        return self.full_name

    class Meta(OrderedModel.Meta):
        pass

class ContactUs(BaseModel):
    first_name = CharField(max_length=256)
    last_name = CharField(max_length=256)
    email = EmailField(max_length=256, null=True, blank=True)
    phone = IntegerField()
    message = TextField()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
