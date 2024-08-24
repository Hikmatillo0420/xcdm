from rest_framework import serializers
from .models import Category, Project, Blog, Faq, Team_category, Team


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


class Team_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_category
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
