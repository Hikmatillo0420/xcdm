from rest_framework.generics import (ListAPIView, RetrieveAPIView)

from company.models import Category, Project, Blog, Faq, Team_category, Team
from company.serializers import CategorySerializer, ProjectSerializer, BlogSerializer, FaqSerializer, TeamSerializer, \
    Team_categorySerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


class BlogListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class FaqListAPIView(ListAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class Team_categoryListAPIView(ListAPIView):
    queryset = Team_category.objects.all()
    serializer_class = Team_categorySerializer


class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamView(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'slug'
