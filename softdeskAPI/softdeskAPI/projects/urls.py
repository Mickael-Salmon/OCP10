from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from projects import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('projects/<int:pk>/contributors/', views.ContributorList.as_view()),
    path('projects/<int:pk>/contributors/<int:contributor_pk>/', views.ContributorDetail.as_view()),
    path('projects/<int:pk>/issues/', views.IssueList.as_view()),
    path('projects/<int:pk>/issues/<int:issue_pk>/', views.IssueDetail.as_view()),
    path('projects/<int:pk>/issues/<int:issue_pk>/comments/', views.CommentList.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
