
from rest_framework import serializers
from .models import User,Thread,Profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name']
class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=['user','profile_picture']
class ThreadSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first = UserSerializer()
    second = UserSerializer()
    updated = serializers.DateTimeField()
    timestamp = serializers.DateTimeField()
class ThreadSerializerStart(serializers.ModelSerializer):
    admin=ProfileSerializer()
    class Meta:
        model=Thread    
        fields="__all__"
