from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from .views import SignupView, ExportDataView, DeleteDataView, UserConsentView

from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('export-data/', ExportDataView.as_view(), name='export-data'),
    path('export-data/', ExportDataView.as_view(), name='export-data'),
    path('delete-data/', DeleteDataView.as_view(), name='delete-data'),
    path('consent/', UserConsentView.as_view(), name='user-consent')
]