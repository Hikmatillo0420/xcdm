from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, Project, Blog, Faq, TeamCategory, TeamMember, TeamPosition, ContactUs
import re
from django.utils.translation import gettext_lazy as _

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_category_title(self, obj):
        return obj.category.title


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"


class TeamPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPosition
        exclude = 'title', 'id'


class TeamMemberSerializer(serializers.ModelSerializer):
    position = TeamPositionSerializer()

    class Meta:
        model = TeamMember
        exclude = 'category', 'order'


class TeamCategorySerializer(serializers.ModelSerializer):
    # members = TeamMemberSerializer(many=True)

    class Meta:
        model = TeamCategory
        exclude = 'title', 'id', 'order'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['members'] = TeamMemberSerializer(instance.members.all(), many=True).data
        return data

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']

    def validate_email(self, value):
        if value:
            allowed_domains = ['gmail.com', 'mail.ru']
            if not any(value.endswith(f"@{domain}") for domain in allowed_domains):
                raise ValidationError(_('Only Gmail or Mail.ru addresses are allowed.'), params={'value': value})
        return value
