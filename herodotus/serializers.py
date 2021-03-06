from .models import Content, User, Feed, Tag
from rest_framework import serializers

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'color', 'url']

class ContentSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(
        required=False, allow_null=True, format='%m/%d/%Y', input_formats=['%m/%d/%Y'])

    tags = TagSerializer(many=True, read_only=True)

    tags_id = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(), source='tags', view_name='tag-detail', write_only=True, many=True)

    class Meta:
        model = Content
        fields = ['id', 'content_type', 'url',
                  'author', 'publisher', 'date', 'title', 'content', 'richtext', 'tags_id', 'tags']

class FeedSerializer(serializers.ModelSerializer):
    last_updated = serializers.DateTimeField(
        required=False, allow_null=True)
    
    tags = TagSerializer(many=True, read_only=True)

    tags_id = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(), source='tags', view_name='tag-detail', write_only=True, many=True)

    class Meta:
        model = Feed
        fields = ['id', 'title', 'url', 'last_updated', 'tags', 'tags_id']


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
        fields = ('id', 'username', 'is_staff', 'first_name',
                  'last_name', 'email', 'password')

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
