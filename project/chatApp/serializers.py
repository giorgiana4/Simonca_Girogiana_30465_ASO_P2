from chatApp.models import Message
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

class MessageSerializer(serializers.ModelSerializer):
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'time']