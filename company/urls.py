from django.urls import path
from company.views import CategoryView, ProjectView, ProjectListAPIView, BlogListAPIView, FaqListAPIView, \
    TeamCategoryListAPIView, TeamMemberListView, TeamMemberRetrieveAPIView

urlpatterns = [

    path('categories', CategoryView.as_view(), name='category'),
    path('projects', ProjectListAPIView.as_view(), name='project'),
    path('projects/<slug:slug>', ProjectView.as_view(), name='project_products'),
    path('blogs', BlogListAPIView.as_view(), name='blog'),
    path('faqs', FaqListAPIView.as_view(), name='faq'),
    path('team-categories', TeamCategoryListAPIView.as_view(), name='team_category'),
    path('team-members', TeamMemberListView.as_view(), name='team'),
    path('team-members/<slug:slug>', TeamMemberRetrieveAPIView.as_view(), name='team_detail'),

]
