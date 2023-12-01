from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class UserData(models.Model):
    """
    Model representing user data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

class UserConsent(models.Model):
    """
    Represents a user's consent for data processing.

    Attributes:
        user (User): The user associated with the consent.
        data_processing_consent (bool): Indicates whether the user has given consent for data processing.
        date_given (datetime): The date and time when the consent was given.
        consent_type (str): The type of consent (e.g., "inscription", "newsletter", etc.).
        details (str): Specific details about the given consent.
        can_be_contacted (bool): Indicates whether the user can be contacted.
        can_data_be_shared (bool): Indicates whether the user's data can be shared.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_processing_consent = models.BooleanField(default=False)
    date_given = models.DateTimeField(auto_now_add=True)
    consent_type = models.CharField(max_length=200)
    details = models.TextField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.consent_type}"