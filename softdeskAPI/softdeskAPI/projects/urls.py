from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from projects import views

urlpatterns = [
    path('', views.ProjectList.as_view()),
    path('<int:pk>/', views.ProjectDetail.as_view()),
    path('<int:project_pk>/contributors/', views.ContributorList.as_view()),
    path('<int:project_pk>/users/', views.ContributorList.as_view(), name='project-contributors'),
    path('<int:project_pk>/contributors/<int:contributor_pk>/', views.ContributorDetail.as_view(), name='project-contributor-detail'),
    path('<int:project_pk>/issues/', views.IssueList.as_view()),
    path('<int:project_pk>/issues/<int:issue_pk>/', views.IssueDetail.as_view()),
    path('<int:project_pk>/issues/<int:issue_pk>/comments/', views.CommentList.as_view()),
    path('<int:project_pk>/issues/<int:issue_pk>/comments/<int:comment_pk>/', views.CommentDetail.as_view()),
]




