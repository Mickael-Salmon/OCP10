from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import UserConsent

"""Serializer for user registration."""
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    data_processing_consent = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'data_processing_consent')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields did not match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Ajout de cette ligne pour sauvegarder le consentement de l'utilisateur au traitement des données
        user.data_processing_consent = validated_data.get('data_processing_consent', False)

        user.save()

        # Enregistrer le consentement dans le modèle UserConsent
        UserConsent.objects.create(
            user=user,
            consent_type="Inscription",
            details="Consentement donné lors de l'inscription pour le traitement des données."
        )

        return user