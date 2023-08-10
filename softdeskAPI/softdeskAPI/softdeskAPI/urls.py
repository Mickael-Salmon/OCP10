"""
URL configuration for softdeskAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from projects import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

urlpatterns = [
    path('', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('projects/<int:pk>/contributors/', views.ContributorList.as_view()),
    path('projects/<int:pk>/contributors/<int:contributor_pk>/', views.ContributorDetail.as_view()),
    path('projects/<int:pk>/issues/', views.IssueList.as_view()),
    path('projects/<int:pk>/issues/<int:issue_pk>/', views.IssueDetail.as_view()),
    path('projects/<int:pk>/issues/<int:issue_pk>/comments/', views.CommentList.as_view()),
    path('projects/<int:pk>/issues/<int:issue_pk>/comments/<int:comment_pk>/', views.CommentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

