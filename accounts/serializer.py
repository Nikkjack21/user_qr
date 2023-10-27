from django.forms import ValidationError
from rest_framework import serializers
from accounts.models import Accounts, ShortenURL
from accounts.utils import generate_qr_code, generate_short_url


symbols = "[()[\]{}|\\`~!@#$%^*_\-+=:;'\",<>./?]"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Accounts
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, data):
        if len(data) < 8:
            raise ValidationError("Password should have minimum lenght 8")
        elif not any(i.isupper() for i in data):
            raise ValidationError("Password should have one upeercase [A_Z]")
        elif not any(i.isdigit() for i in data):
            raise ValidationError("Password should have atleast a digit")
        elif not any(char in symbols for char in data):
            raise ValidationError("Password should have atleast one character")
        return data

    def validate(self, attrs):
        if attrs.get("password", None) != attrs.get("confirm_password", None):
            raise ValidationError("Passwords donot match")
        attrs.pop("confirm_password", None)
        return attrs

    def create(self, validated_data):
        return Accounts.objects.create_user(**validated_data)


class shortenUrlSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ShortenURL
        fields = [
            "id",
            "original_url",
            "shorten_url",
            "token",
            "qr_image"
        ]

    
    def update(self, instance, validated_data):
        new_url = validated_data.get("original_url")
        token, short_url = generate_short_url()
        qr_code_img = generate_qr_code(url=short_url)
        if token and short_url and new_url and qr_code_img:
            instance.original_url = new_url
            instance.token = token
            instance.shorten_url = short_url
            instance.qr_image=qr_code_img
            instance.save()
        return instance