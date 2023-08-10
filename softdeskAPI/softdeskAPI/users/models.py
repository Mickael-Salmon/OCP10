from django.db import models
from django.contrib.auth.models import User

class UserConsent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_processing_consent = models.BooleanField(default=False)
    date_given = models.DateTimeField(auto_now_add=True)
    consent_type = models.CharField(max_length=200)  # Exemple : "inscription", "newsletter", etc.
    details = models.TextField()  # Détails spécifiques sur le consentement donné

    def __str__(self):
        return f"{self.user.username} - {self.consent_type}"


