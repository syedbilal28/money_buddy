class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name']
class ThreadSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first = UserSerializer()
    second = UserSerializer()
    updated = serializers.DateTimeField()
    timestamp = serializers.DateTimeField()
class ThreadSerializerStart(serializers.ModelSerializer):
    class Meta:
        model=Thread    
        fields="__all__"