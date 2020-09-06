from .models import Content, User
from rest_framework import serializers


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(
        required=False, allow_null=True, format='%m/%d/%Y', input_formats=['%m/%d/%Y'])

    class Meta:
        model = Content
        fields = ['id', 'content_type', 'url',
                  'author', 'date', 'title', 'content']


class ScrapedArticleSerializer(serializers.Serializer):
    url = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.CharField()
    date = serializers.DateTimeField(format='%m/%d/%Y')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        print(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        print(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
