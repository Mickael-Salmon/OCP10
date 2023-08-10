#from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserConsent
from rest_framework.views import APIView


class SignupView(generics.CreateAPIView):
    """API endpoint to register a new user."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

class ExportDataView(APIView):

    def get(self, request):
        user = self.request.user

        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            # ... Ajoutez d'autres champs que vous souhaitez exporter ici ...
        }

        return Response(data)

class DeleteDataView(APIView):

    def delete(self, request):
        user = self.request.user

        # Supprimez ou anonymisez toutes les données associées à cet utilisateur
        user.email = "deleted@domain.com"
        user.first_name = ""
        user.last_name = ""
        # ... Autres champs à anonymiser ...

        # Pour supprimer réellement l'utilisateur (ceci est irréversible) :
        # user.delete()

        user.save()

        return Response({"message": "User data deleted or anonymized successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserConsentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserConsent.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{"date_given": consent.date_given, "consent_type": consent.consent_type, "details": consent.details} for consent in queryset]
        return Response(data, status=status.HTTP_200_OK)