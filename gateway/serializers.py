from django.contrib.auth import authenticate
from rest_framework_simplejwt import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'phone_number': attrs.get("phone_number"),
            "otp": attrs.get("otp"),
        }

        if credentials['phone_number'] and credentials['password']:
            user = authenticate(request=self.context.get('request'), phone_number=credentials['phone_number'],
                                password=credentials['password'])

            if user is None:
                raise serializers.ValidationError(_("No active account found with the given credentials"))

            if not user.is_active:
                raise serializers.ValidationError(_("User account is disabled"))

            data = super().validate(attrs)
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError(_("Must include 'phone_number' and 'password'."))

    def get_token(cls, user: AuthUser) -> Token:
        token = cls.token_class.for_user(user)
        token.payload["user_data"] = {
            "user_id": user.id,

        }

        return token
