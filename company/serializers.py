from rest_framework import serializers
from .models import Category, Project, Blog, Faq, TeamCategory, TeamMember


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"


class TeamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        exclude = 'title',


class TeamMemberSerializer(serializers.ModelSerializer):
    category = TeamCategorySerializer()

    class Meta:
        model = TeamMember
        fields = "__all__"
