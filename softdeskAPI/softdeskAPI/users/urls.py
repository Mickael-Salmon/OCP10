from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from .views import SignupView, ExportDataView, DeleteDataView, UserConsentView

from . import views


urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("export-data/", ExportDataView.as_view(), name="export-data"),
    path("export-data/", ExportDataView.as_view(), name="export-data"),
    path("delete-data/", DeleteDataView.as_view(), name="delete-data"),
    path("consent/", UserConsentView.as_view(), name="user-consent"),
]

"""
URL patterns for user-related endpoints.

This module defines the URL patterns for user-related endpoints in the Softdesk API.

- signup: Endpoint for user registration.
- login: Endpoint for user login and token generation.
- export-data: Endpoint for exporting user data.
- delete-data: Endpoint for deleting user data.
- consent: Endpoint for user consent.

"""
