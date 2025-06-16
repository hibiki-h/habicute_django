from rest_framework import serializers

from .models import TaskModel, UserModel, CalendarTaskModel


class BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['user']


class TaskSerializers(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta):
        model = TaskModel


class CalendarTasktSerializers(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta):
        model = CalendarTaskModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user
