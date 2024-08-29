from django.urls import path
from company.views import CategoryView, ProjectView, ProjectListAPIView, BlogListAPIView, FaqListAPIView, \
    TeamCategoryListAPIView

urlpatterns = [

    path('categories', CategoryView.as_view(), name='category'),
    path('projects', ProjectListAPIView.as_view(), name='project'),
    path('projects/<slug:slug>', ProjectView.as_view(), name='project_products'),
    path('blogs', BlogListAPIView.as_view(), name='blog'),
    path('faqs', FaqListAPIView.as_view(), name='faq'),
    path('team-categories', TeamCategoryListAPIView.as_view(), name='team_category'),

]
