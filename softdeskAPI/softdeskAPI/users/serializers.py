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
    input_date_of_birth = serializers.DateField(write_only=True, required=True)
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

    def to_representation(self, instance):
        """Modifier la représentation de sortie pour exclure date_of_birth."""
        ret = super().to_representation(instance)
        ret.pop('date_of_birth', None)
        return ret

    def get_date_of_birth(self, obj):
        try:
            user_data = UserData.objects.get(user=obj)
            return user_data.date_of_birth
        except UserData.DoesNotExist:
            return None

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
            "input_date_of_birth"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
    def get_date_of_birth(self, obj):
        return UserData.objects.get(user=obj).date_of_birth
    def validate(self, attrs):
        """
        Validates the attributes of the serializer.

        Args:
            attrs (dict): The attributes to be validated.

        Returns:
            dict: The validated attributes.

        Raises:
            serializers.ValidationError: If the password fields do not match or if the user is not over 15.
        """

        # Vérification de l'âge
        date_of_birth = attrs.get("input_date_of_birth")
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 15:
                raise serializers.ValidationError({"date_of_birth": "Vous devez avoir au moins 15 ans pour vous inscrire."})

        # Vérification de la correspondance des mots de passe
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields did not match."})

        return attrs


    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées fournies.

        Args:
            validated_data (dict): Les données validées contenant les informations de l'utilisateur.

        Returns:
            User: Le nouvel objet utilisateur créé.
        """

        # Extraire la date de naissance et la retirer des données validées
        date_of_birth_data = validated_data.pop('input_date_of_birth', None)

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        user.set_password(validated_data.get("password"))
        user.save()

        # Créer UserData pour la date de naissance, si elle est fournie
        if date_of_birth_data:
            UserData.objects.create(user=user, date_of_birth=date_of_birth_data)

        # Enregistrer le consentement pour le traitement des données
        user.data_processing_consent = validated_data.get("data_processing_consent", False)
        user.save()

        # Enregistrer le consentement dans le modèle UserConsent
        UserConsent.objects.create(
            user=user,
            consent_type="Inscription",
            details="Consentement donné lors de l'inscription pour le traitement des données."
        )

        return user

