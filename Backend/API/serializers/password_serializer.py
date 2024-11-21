from rest_framework import serializers
from ..models import UserInfo

class PasswordUpdatingSerializer(serializers.ModelSerializer):

    """
    Serializer for updating a user's password. Requires the old password to verify the user, 
    and allows setting a new password if the old password is correct and the new passwords match.
    """
    
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    re_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserInfo
        fields = ['old_password', 'new_password', 're_new_password']

    def validate(self, data):

        """
        Validates that the new password and re-entered password match.
        """

        if data['new_password'] != data['re_new_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match'})
        return data
    
    def validate_old_password(self, value):

        """
        Validates that the old password entered matches the current password of the user.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value

    def update(self, instance, validated_data):

        """
        Updates the user's password to the new password provided.
        """

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class PasswordResettingSerializer(serializers.ModelSerializer):

    """
    Serializer for resetting a user's password, allowing the user to set a new password and confirm it.
    """
    
    new_password = serializers.CharField(write_only=True, required=True)
    re_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserInfo
        fields = ['new_password', 're_new_password']

    def validate(self, data):

        """
        Validates that the new password and re-entered password match.
        """

        if data['new_password'] != data['re_new_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match'})
        return data

    def update(self, instance, validated_data):

        """
        Updates the user's password to the new password provided, typically after a reset process.
        """

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
