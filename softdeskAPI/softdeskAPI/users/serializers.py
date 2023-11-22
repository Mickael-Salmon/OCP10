from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import UserConsent, UserData
from datetime import date

"""Serializer for user registration."""


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer class for user signup.

    This serializer is used to validate and create a new user during the signup process.
    It includes fields for username, email, password, password2, first_name, last_name,
    and data_processing_consent.

    Attributes:
        email (serializers.EmailField): The email field for the user's email address.
        password (serializers.CharField): The password field for the user's password.
        password2 (serializers.CharField): The confirmation password field.
        data_processing_consent (serializers.BooleanField): The field to indicate the user's consent for data processing.

    Methods:
        validate(attrs): Custom validation method to check if the password and password2 fields match.
        create(validated_data): Method to create a new user with the provided data and save it to the database.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    data_processing_consent = serializers.BooleanField(required=True)
    date_of_birth = serializers.DateField()

    class Meta:
        """
        Meta class for UserSerializer.

        Defines the metadata options for the UserSerializer class.
        """
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "data_processing_consent",
            "date_of_birth"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value

    def validate(self, attrs):
            """
            Validates the attributes of the serializer.

            Args:
                attrs (dict): The attributes to be validated.

            Returns:
                dict: The validated attributes.

            Raises:
                serializers.ValidationError: If the password fields do not match.
            """
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields did not match."}
                )

            return attrs

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.

        Args:
            validated_data (dict): The validated data containing user information.

        Returns:
            User: The newly created user object.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        # Ajout de cette ligne pour sauvegarder le consentement de l'utilisateur au traitement des données
        user.data_processing_consent = validated_data.get(
            "data_processing_consent", False
        )

        user.save()

        UserData.objects.create(
        user=user,
        date_of_birth=validated_data["date_of_birth"]
        )

        # Enregistrer le consentement dans le modèle UserConsent
        UserConsent.objects.create(
            user=user,
            consent_type="Inscription",
            details="Consentement donné lors de l'inscription pour le traitement des données.",
        )

        return user
