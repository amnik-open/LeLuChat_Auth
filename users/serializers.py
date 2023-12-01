"""Define serializers for different models classes"""
from rest_framework import serializers
from users.models import LeluUser, WebsiteUser


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering user"""
    class Meta:
        model = LeluUser
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = LeluUser(email=self.validated_data['email'], name=self.validated_data['name'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value


class LeluUserSerializer(serializers.ModelSerializer):
    """Serializer for Leluuser model"""

    uuid = serializers.UUIDField(read_only=True)
    type = serializers.ReadOnlyField(default='LeluUser')

    class Meta:
        model = LeluUser
        fields = ['uuid', 'email', 'name', 'type']

class WebsiteUserSerializer(serializers.ModelSerializer):
    """Serializer for WebsiteUser model"""

    uuid = serializers.UUIDField(read_only=True)
    type = serializers.ReadOnlyField(default='WebsiteUser', read_only=True)
    auth_token = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WebsiteUser
        fields = ['uuid', 'type', 'auth_token']

    def create(self, validated_data):
        return WebsiteUser.objects.create()
