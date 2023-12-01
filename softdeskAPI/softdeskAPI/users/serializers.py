from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import UserConsent, UserData
from datetime import date

"""Serializer for user registration."""

class SignupSerializer(serializers.ModelSerializer):
    input_date_of_birth = serializers.DateField(write_only=True, required=True)
    data_processing_consent = serializers.BooleanField(write_only=True,required=True)
    can_be_contacted = serializers.BooleanField(write_only=True,required=True)
    can_data_be_shared = serializers.BooleanField(write_only=True,required=True)
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

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "input_date_of_birth",
            "data_processing_consent",
            "can_be_contacted",
            "can_data_be_shared"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        print(attrs)
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields did not match."})

        date_of_birth = attrs.get("input_date_of_birth")
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 15:
                raise serializers.ValidationError({"date_of_birth": "Vous devez avoir au moins 15 ans pour vous inscrire."})

        if attrs.get('data_processing_consent') is None:
            raise serializers.ValidationError({"data_processing_consent": "Ce champ est obligatoire."})

        if attrs.get('can_be_contacted') is None:
            raise serializers.ValidationError({"can_be_contacted": "Ce champ est obligatoire."})

        if attrs.get('can_data_be_shared') is None:
            raise serializers.ValidationError({"can_data_be_shared": "Ce champ est obligatoire."})

        return attrs

    def create(self, validated_data):
        date_of_birth_data = validated_data.pop('input_date_of_birth', None)
        data_processing_consent = validated_data.pop('data_processing_consent', None)
        can_be_contacted = validated_data.pop('can_be_contacted', None)
        can_data_be_shared = validated_data.pop('can_data_be_shared', None)

        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        user.set_password(validated_data.get("password"))
        user.save()

        if date_of_birth_data:
            UserData.objects.create(user=user, date_of_birth=date_of_birth_data)

        UserConsent.objects.create(
            user=user,
            consent_type="Inscription",
            details="Consentement donné lors de l'inscription pour le traitement des données.",
            data_processing_consent=data_processing_consent,
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared
        )

        return user