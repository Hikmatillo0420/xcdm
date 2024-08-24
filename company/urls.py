from django.urls import path
from company.views import CategoryView, ProjectView, ProjectListAPIView, BlogListAPIView, FaqListAPIView, \
    Team_categoryListAPIView, TeamListView, TeamView

urlpatterns = [

    path('category', CategoryView.as_view(), name='category'),
    path('project', ProjectListAPIView.as_view(), name='project'),
    path('project/<slug:slug>', ProjectView.as_view(), name='project_products'),
    path('blog', BlogListAPIView.as_view(), name='blog'),
    path('faq', FaqListAPIView.as_view(), name='faq'),
    path('team_category', Team_categoryListAPIView.as_view(), name='team_category'),
    path('team', TeamListView.as_view(), name='team'),
    path('team/<slug:slug>', TeamView.as_view(), name='team_detail'),

]
