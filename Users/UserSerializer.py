from django.contrib.auth.models import Group
from rest_framework.authentication import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import PasswordReset, UserProfile


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    def validate_username(self):
        print("valiate")


class ListAllUsersSerializer(ModelSerializer):
    user_list = UserSerializer(source='user', required=True)

    class Meta:
        model = UserProfile
        fields = ['user_list', 'mobile_number']

    def to_representation(self, name):
        resp = {}
        if not name.user.is_superuser:
            try:
                resp = {
                    "user": {
                        "username": name.user.username,
                        "first_name": name.user.first_name,
                        "last_name": name.user.last_name,
                        "email": name.user.email,
                        "last_login": name.user.last_login,
                        "date_joined": name.user.date_joined
                    },
                    "mobile_number": name.mobile_number,
                }
            except FileNotFoundError as e:
                resp = {
                    "user": {
                        "username": name.user.username,
                        "first_name": name.user.first_name,
                        "last_name": name.user.last_name,
                        "email": name.user.email,
                        "last_login": name.user.last_login,
                        "date_joined": name.user.date_joined
                    },
                    "mobile_number": name.mobile_number,
                }

        return resp


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["is_active"]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class PasswordResetSerializers(ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'
