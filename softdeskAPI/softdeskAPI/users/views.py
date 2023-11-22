# from django.shortcuts import render
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
    """
    API endpoint to register a new user.

    This view allows users to register by sending a POST request with their
    desired username, email, and password. Upon successful registration,
    a new user will be created in the database.

    Methods:
        - POST: Create a new user.

    Attributes:
        - queryset: Queryset of all User objects.
        - permission_classes: List of permission classes for this view.
        - serializer_class: Serializer class used for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

class ExportDataView(APIView):
    """
    A view for exporting user data.

    This view allows authenticated users to export their data, including
    username, email, first name, last name, and any other desired fields.

    Endpoint: /export-data/
    Method: GET
    """

    def get(self, request):
            """
            Retrieve the user's information.

            Args:
                request (HttpRequest): The HTTP request object.

            Returns:
                Response: The response containing the user's information.
            """
            user = self.request.user

            data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                # "date_of_birth": user.date_of_birth,
                # ... Add any other fields to export here ...
            }

            return Response(data)


class DeleteDataView(APIView):
    """
    View for deleting or anonymizing user data.

    This view is used to delete or anonymize all data associated with a user.
    The user's email, first name, last name, and other fields can be modified
    to remove personal information. The user can also be permanently deleted
    by calling the `delete()` method.

    Methods:
    - delete: Deletes or anonymizes user data and returns a success message.

    Returns:
    - Response: A response object with a success message and a status code.
    """
    def delete(self, request):
            """
            Delete or anonymize user data.

            This method deletes or anonymizes all data associated with the user.
            The user's email is set to "deleted@domain.com" and their first name and last name are cleared.
            Other fields that need to be anonymized should be handled accordingly.

            To permanently delete the user (this action is irreversible), uncomment the line `user.delete()`.

            Returns:
                A Response object with a message indicating that the user data has been deleted or anonymized successfully.
            """
            user = self.request.user

            user.email = "deleted@domain.com"
            user.first_name = ""
            user.last_name = ""
            # ... Other fields to be anonymized ...

            # To permanently delete the user (this action is irreversible):
            # user.delete()

            user.save()

            return Response(
                {"message": "User data deleted or anonymized successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )


class UserConsentView(generics.ListAPIView):
    """
    API view for retrieving user consents.

    This view requires authentication and returns a list of user consents.
    Each consent includes the date given, consent type, and details.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of UserConsent objects filtered by the current user.
        """
        return UserConsent.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
            """
            Retrieve a list of consents.

            Returns:
                Response: A response containing the list of consents.
            """
            queryset = self.get_queryset()
            data = [
                {
                    "date_given": consent.date_given,
                    "consent_type": consent.consent_type,
                    "details": consent.details,
                }
                for consent in queryset
            ]
            return Response(data, status=status.HTTP_200_OK)
